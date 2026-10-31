---
title: "Say, Dream, and Act: Learning Video World Models for Instruction-Driven Robot Manipulation"
date: "2026-02-11"
authors: "Songen Gu; Yunuo Cai; Tianyu Wang; Simo Wu; Yanwei Fu"
url: https://arxiv.org/abs/2602.10717
pdf: https://arxiv.org/pdf/2602.10717
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.10717)** / [論文ページ](https://arxiv.org/abs/2602.10717)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Say, Dream, and Act: Learning Video World Models for Instruction-Driven Robot Manipulation** 

**Songen Gu**<sup>* 1</sup> **Yunuo Cai**<sup>* 1</sup> **Tianyu Wang**<sup>1</sup> **Simo Wu**<sup>1</sup> **Yanwei Fu**<sup>1</sup> 

# **Abstract** 

Robotic manipulation requires anticipating how the environment evolves in response to actions, yet most existing systems lack this predictive capability, often resulting in errors and inefficiency. While Vision-Language Models (VLMs) provide high-level guidance, they cannot explicitly forecast future states, and existing world models either predict only short horizons or produce spatially inconsistent frames. To address these challenges, we propose a framework for fast and predictive video-conditioned action. Our approach first selects and adapts a robust video generation model to ensure reliable future predictions, then applies adversarial distillation for fast, few-step video generation, and finally trains an action model that leverages both generated videos and real observations to correct spatial errors. Extensive experiments show that our method produces temporally coherent, spatially accurate video predictions that directly support precise manipulation, achieving significant improvements in embodiment consistency, spatial referring ability, and task completion over existing baselines. Codes&Models will be released. 

# **1. Introduction** 

Robotic manipulation in real-world environments is challenging because it requires both understanding the current scene and anticipating how it will evolve. Humans naturally predict object motion, spatial relationships, and environmental changes, allowing smooth and adaptive manipulation. Most robotic systems, however, lack this predictive ability, often resulting in errors, inefficiency, or unsafe behavior. Therefore, models that can forecast future states are essential for precise, long-horizon control. 

Recent Vision-Language Models (VLMs) demonstrate strong decision-making capabilities (Zitkovich et al., 2023; 

*Equal contribution 1Fudan University. 

_Preprint. February 12, 2026._ 

Kim et al., 2024a), conditioning actions on high-level instructions or observations. Despite their promise, VLMs often fail at producing accurate low-level actions due to limited spatial reasoning and slow inference (Black et al., 2024; NVIDIA et al., 2025; Wen et al., 2025). Crucially, they do not explicitly model the consequences of actions, which limits their effectiveness in complex, multi-step manipulation tasks. 

World models, which predict future observations (Du et al., 2023; Tian et al., 2024; Zhang et al., 2025a; Li et al., 2025), provide a more suitable solution. By forecasting how the environment evolves over time, they supply rich visual context that downstream action models can leverage for informed decision-making. Despite their promise, current world model approaches face several critical limitations. (1) _Limited temporal horizon_ : many models can only predict a short sequence of future frames, necessitating repeated rollouts to handle long-horizon tasks (Hu et al., 2024). (2) _Poor spatial consistency_ : predictions often suffer from distortions or inconsistent robot embodiments, compromising spatial accuracy and reducing their usefulness for precise manipulation. (3) _High computational cost_ : while large video generation models achieve high predictive quality, their iterative nature incurs substantial computational cost, making real-time deployment challenging (Jang et al., 2025). 

On the other hand, diffusion-based video generators achieve strong predictive quality, but rely on iterative denoising, which is computationally expensive. Techniques such as distillation and adversarial training (Salimans & Ho, 2022; Sauer et al., 2024b; Zhang et al., 2024) can accelerate inference, but maintaining spatial and temporal fidelity—crucial for manipulation—remains challenging. 

To address these challenges, we propose a Dream4manip framework of **Say, Dream, and Act** that integrates highfidelity video world models with an in-context conditioned action model for instruction-driven robot manipulation. Our approach is guided by three core principles: _Say_ of learning a robust video-based world model capturing task-relevant dynamics; _Dream_ of enabling length-agnostic imagination of future outcomes via frame-rate-agnostic video prediction; and _Act_ of producing executable actions by treating imagined trajectories as in-context examples grounded in real 

1 

**Submission and Formatting Instructions for ICML 2026** 

observations. 

Formally, our method proceeds in three stages: (1) **World model selection and adaptation:** We benchmark several state-of-the-art video generation models on metrics such as embodiment consistency, spatial referring ability, and task completion, and select a strong foundation model. Domain adaptation ensures reliability across new scenes, camera viewpoints, and robot embodiments. (2) **Adversarial distillation for fast generation:** We distill the adapted model using latent-space adversarial loss and reconstruction supervision, enabling few-step denoising that preserves spatial and temporal fidelity while reducing computational cost. (3) **In-context conditioned action modeling:** We train an action model that consumes both imagined trajectories and real observations, correcting spatial errors in the world model and producing accurate action sequences. 

Our approach is motivated by the need for robots to anticipate and reason about future states in complex, dynamic environments. By integrating high-fidelity video prediction with in-context action generation, we enable reliable and efficient manipulation in cluttered scenes. **Say, Dream, and Act** unifies world modeling and action prediction into a single, fast policy capable of imagining, anticipating, and acting robustly across diverse tasks. Extensive experiments demonstrate state-of-the-art performance in long-horizon manipulation, with improvements in Embodiment Consistency (EC), Referring Success Rate (RSR), Interaction Success Rate (ISR), and Task Completion Rate (TCR). In particular, Cosmos2 models, after domain adaptation and distillation, significantly outperform baselines in EC and RSR, highlighting the critical role of accurate and robust world models for instruction-driven robotic control. 

**Contributions** . We make several contributions toward enabling fast, long-horizon robot manipulation. First, we develop a robust video-based world model by selecting and adapting a state-of-the-art video generation backbone (COSMOS-PREDICT2) to the robotic domain, applying domain adaptation and latent-space adversarial distillation to achieve high-fidelity predictions with few-step denoising. Second, we introduce a length-agnostic imagination mechanism that compresses arbitrary-length execution trajectories into a fixed set of keyframes, enabling frame-rate-agnostic prediction of long-horizon outcomes without relying on low-level action alignment. Third, we propose an in-context conditioned action model that treats imagined trajectories as examples while grounding predictions in real observations, allowing the system to correct spatial errors and produce executable actions. Finally, we integrate these components into a unified framework: **Say, Dream, and Act** that combines predictive world modeling and action reasoning into a single, fast policy capable of anticipating, planning, and executing manipulation tasks across diverse environments. 

# **2. Related Work** 

**Action Models** . Developing action models that can control robots under varied observation conditions has long been a central goal in robotics. Early methods such as ACT (Zhao et al., 2023) generate action chunks directly from image observations, while Diffusion Policy (Chi et al., 2023) uses a diffusion-based framework for action generation. More recent approaches, including RT-2 (Zitkovich et al., 2023) and OpenVLA (Kim et al., 2024a), integrate Vision-Language Models (VLMs) to produce actions directly. However, follow-up work (Black et al., 2024; NVIDIA et al., 2025; Wen et al., 2025) shows that VLMs alone often struggle with precise action generation because they are slow at inference and lack a detailed understanding of low-level dynamics. As a result, VLMs are commonly used as high-level decision modules that provide conditions for diffusion- or flow-matching–based action policies. Still, VLMs cannot predict future environmental changes, which motivates combining them with world models that offer predictive visual feedback in addition to high-level decision guidance. 

**World Models** . World models, particularly video or image generation models, have been widely used to enhance action models. (1) _World models for fast manipulation._ These models predict future states of the environment to provide visual conditions for action planning. UniPi (Du et al., 2023) predicts two future frames and applies temporal super-resolution to form short videos for action extraction. Seer (Tian et al., 2024) predicts a single future frame along with actions, while GVF-TAPE (Zhang et al., 2025a) additionally predicts depth frames. Unified Video Action Model (Li et al., 2025) jointly predicts future frames and actions. LaDi-WM (Huang et al., 2025) generates geometric and semantic future frames instead of raw images, and FLARE (Zheng et al., 2025) predicts latent visual features alongside actions. While effective, these models often predict only a few future frames, requiring multiple execution steps to complete tasks and incurring significant time overhead. Video Prediction Policy (Hu et al., 2024) uses one-step denoised latents as visual conditions, but these carry less information than fully denoised frames. (2) _World models for data generation._ Large video generation models have also been used to generate synthetic training data for pretraining vision-language action models. For example, DreamGen (Jang et al., 2025) leverages cosmos-predict2 to create large-scale video datasets labeled with neural trajectories. While such models excel at predicting future states, their inference speed is insufficient for ‘intime’ applications. Our Dream4manip runs very fast as shown in results. 

**Accelerating Diffusion Models** . Most modern video generation models rely on diffusion pipelines, which require iterative denoising and are computationally expensive. Distillation-based methods have been proposed to acceler- 

2 

**Submission and Formatting Instructions for ICML 2026** 


_Figure 1._ (a) The training pipeline for world model distillation. Additional details are provided in Section 3.1.2. (b) The pipeline of our proposed policy model. Given the current observation and the instruction, the world model first generates imagined future frames. The in-context conditioned action model then produces actions in a closed-loop manner. Each new observation is fed back into the model to generate the next action. 

ate inference. Trajectory-preserving distillation (Salimans & Ho, 2022; Liu et al., 2022; Luo et al., 2023) trains a student model to approximate the teacher’s ODE sampling trajectory with fewer steps, but low-step outputs often suffer from blurriness. Distribution-matching and adversarial distillation address this limitation. Adversarial Diffusion Distillation (Sauer et al., 2024b) and LADD (Sauer et al., 2024a) combine adversarial losses with score distillation to improve both speed and quality. SV-F (Zhang et al., 2024) adapts this approach to video, successfully accelerating SVD (Blattmann et al., 2023) to one-step generation. Although acceleration may degrade for very large models, adversarial distillation remains a promising strategy for fast, high-quality video prediction. 

# **3. Method** 

Our goal is to enable fast, long-horizon robotic manipulation using a learned world model. As illustrated in Figure 1, our framework integrates a high-fidelity video-based world model with an action model trained via in-context conditioning. The method consists of three stages: (1) selecting and adapting a robust world model to the robotic domain, (2) distilling the adapted model for efficient few-step denoising, and (3) training an in-context conditioned action model using both imagined and real trajectories. Together, these components form a world-model–driven manipulation 

policy capable of fast execution. 

## **3.1. Say: World Model** 

## 3.1.1. SELECTION 

**Key Idea:** Choose a world model that preserves spatial consistency and task-relevant dynamics. 

We benchmark several recent video generation models on metrics critical for embodied decision-making: embodiment consistency, task completion rate, and spatial referring ability. Based on these evaluations, we select COSMOSPREDICT2 as the backbone of our world model. Quantitative and qualitative comparisons are reported in Section 4.2. Despite strong performance, the model may degrade in novel scenes, unseen camera viewpoints, or alternative embodiments, motivating domain adaptation and distillation. 

## 3.1.2. DOMAIN ADAPTATION AND DISTILLATION 

We introduce a latent-space adversarial loss to enable fewstep denoising, reducing computational cost while maintaining prediction fidelity. Even state-of-the-art video generation models can produce spatial inconsistencies when deployed in novel environments. To address this, we first perform domain adaptation to align the world model with the target robotic domain. We then distill the adapted model using a combination of latent adversarial supervision and 

3 

**Submission and Formatting Instructions for ICML 2026** 


_Figure 2._ The structure of the in-context conditioned action model. We use a transformer-based backbone inherited from ACT (Zhao et al., 2023) for our action model, separated vision encoder is assembled to process videos and observations. The model will output an action chunk for each observation. 

reconstruction loss, resulting in a world model that is both robust and computationally efficient for fast manipulation. 

**Denoising Formulation** . Let _x_ 0 denote a 16 dimension encoded video latent. The diffusion transformer _Tθ_ in COSMOS-PREDICT2 predicts a denoised latent _x_ ˆ0 from a noisy input _xt_ conditioned on auxiliary information _cond_ : 


where _x_<sup>_cond_</sup> _t_ denotes a conditioned version of _xt_ in which the first frame is replaced by a clean latent for image-tovideo generation. And the preconditioning factors are defined as 


The noise level _σt_ is sampled using different strategies during distillation training and inference. 

**Noise Schedule for Few-Step Distillation** . To reduce denoising steps, we sample _σt_ from a discrete set _{σ_ 1 _, . . . , σTg }_ : 


where _p_ is a hyper-parameter that controls the emphasis on low noise levels. The parameter _Tg_ is chosen to match the target number of denoising steps in the distilled model; unless otherwise specified, we set _Tg_ = 8. 

Given the sampled noise level _σt_ , we construct a noisy latent _xt ∼N_ ( _x_ 0 _, σt_ ) and apply Equation (1) to obtain the denoised prediction _x_ ˆ0. 

**Latent Adversarial Distillation** . To accelerate the iterative denoising process, we introduce a _latent adversarial loss_ that encourages high-fidelity prediction under a small 

number of denoising steps. As illustrated in Figure 1, we initialize a discriminator _D_ using the pretrained diffusion transformer (DiT) weights from COSMOS-PREDICT2, and augment it with several lightweight 3D convolutional heads that operate on intermediate DiT feature maps and produce a pixel-wise score map. During training, we freeze the DiT backbone and optimize only the added convolutional heads, encouraging the discriminator to output scores close to 1 for clean latents _x_ 0 and close to _−_ 1 for denoised predictions _x_ ˆ0. 

Before passing _x_ 0 or _x_ ˆ0 to the discriminator, we inject additional noise by sampling _σ_<sup>_′_</sup> such that log( _σ_<sup>_′_</sup> ) _∼N_ (0 _,_ 1), and diffusing both latents to obtain _x_<sup>_′_</sup> and _x_ ˆ<sup>_′_</sup> , respectively. This design choice is motivated by the fact that the pretrained DiT is optimized to process noisy inputs and exhibits more stable and informative features under moderate noise than on clean latents. 

The adversarial objectives for the discriminator _D_ and the generator _G_ are defined as 


**Reconstruction Loss and Domain Adaptation** . We retain the reconstruction loss _Lrec_ from the original training objective of COSMOS-PREDICT2 to facilitate domain adaptation: 


where the weighting factor amplifies the contribution of noisier samples, encouraging accurate denoising across a wide range of noise levels. 

In summary, the generator _LG_ is distilled by optimizing the combined objective 


where _λ_ is a scaling hyperparameter that balances adversarial supervision and reconstruction fidelity; unless otherwise stated, we set _λ_ = 0 _._ 1. 

Within the same training iteration, we additionally apply the reconstruction loss to perform domain adaptation. Specifically, we sample a noise level _σ_ such that log( _σ_ ) _∼N_ (0 _,_ 1), diffuse the clean latent _x_ 0 accordingly, and compute the reconstruction loss between the original latent _x_ 0 and the corresponding denoised prediction _x_ ˆ0. This auxiliary objective further aligns the world model with the target robotic domain while preserving the generative prior. 

## **3.2. Dream: Length-Agnostic World Imagination** 

**Key Idea:** Compress trajectories and generate videos independent of execution length. 

4 

**Submission and Formatting Instructions for ICML 2026** 

||||||**Model**|**FVD** _↓_|**SSIM** _↑_|**PSNR** _↑_|**LPIPS** _↓_|
|---|---|---|---|---|---|---|---|---|---|
|**Task**|**FVD** _↓_|**SSIM** _↑_|**PSNR** _↑_|**LPIPS** _↓_|WAN2.2-14B<br>WAN2214BDi|714.24<br>57862|0.63_±_0.15<br>062_±_018|21.49_±_3.98<br>2158_±_446|0.11_±_0.05<br>009_±_006|
|L-10<br>L-Object<br>L-Spatial<br>L-Goal|104.00<br>177.04<br>119.32<br>127.86|0.82_±_0.10<br>0.89_±_0.05<br>0.85_±_0.09<br>0.88_±_0.07|21.44_±_6.97<br>25.30_±_5.47<br>25.16_±_6.14<br>26.12_±_6.06|0.06_±_0.05<br>0.04_±_0.03<br>0.03_±_0.03<br>0.03_±_0.02|.--s<br>C-2B<br>C-14B<br>C-14B-Droid-F.T.<br>C-2B-DA|.<br>571.46<br>522.66<br>1098.24<br>**211.84**|. .<br>0.70_±_0.10<br>0.67_±_0.11<br>0.23_±_0.04<br>0.82_±_0.09|. .<br>22.09_±_5.78<br>21.56_±_5.95<br>14.73_±_0.67<br>25.19_±_5.48|. .<br>0.11_±_0.05<br>0.12_±_0.05<br>0.26_±_0.05<br>0.05_±_0.03|
||||||C-2B-DA+Dis|238.09|**0.84**_±_0.11|**26.82**_±_6.18|**0.04**_±_0.04|
|||(a)|||||(b)|||


_Table 1._ Quantitative results are compared in (a) World model evaluation results of Cosmos-2B on LIBERO benchmarks. and (b) Model comparison with base model simplified and configuration column (values rounded to two decimals). ’L’, and ’C’ are short for LIBERO and Cosmos, DA: Domain Adaptation. 

We introduce a _length-agnostic imagination_ mechanism that compresses arbitrary-length trajectories into a fixed set of keyframes, enabling holistic, frame-rate-agnostic video generation. Unlike prior approaches (Du et al., 2023; Yang et al., 2023; Zhou et al., 2024) that strictly align video frames with low-level action steps, our insight is that robotic manipulation is fundamentally a low-frequency prediction problem: generating a frame for every action step is unnecessary, redundant, and computationally expensive. 

To address this, we compress robotic execution trajectories of arbitrary length into a fixed number of keyframes via uniform temporal sampling: 


where _n ≪ T_ is a predefined constant independent of the trajectory length _T_ . In our experiments, we set _n_ = 93. 

We then finetune a video diffusion model to learn a framerate-agnostic video generation capability, enabling holistic imagination of the entire execution process without dependence on the specific execution length. This allows the model to anticipate long-horizon outcomes while remaining computationally efficient. 

## **3.3. Act: In-Context Conditioned Action Model** 

**Key Idea:** Treat imagined trajectories as in-context examples to guide action prediction. 

Even with state-of-the-art video generation models, the distilled world model may exhibit occasional spatial inaccuracies. To address this, we treat imagined trajectories as _in-context examples_ for action prediction rather than strict commands (Vuong et al., 2025), allowing the action model to ground its predictions in real observations and correct errors in the generated video. 

As illustrated in Figure 2, our action model receives both the generated future frames and the real historical observations. This design allows the model to correct spatial errors present in the generated video by continuously grounding its 

predictions in actual observations. Functionally, the model operates similarly to a next-token predictor: given an execution example in the form of generated frames, it outputs actions whose execution produces real-world observations that follow the general pattern demonstrated in the example. 

|**Model**|**EC**_↑_|**RSR**_↑_|**ISR**_↑_|**TSR**_↑_|
|---|---|---|---|---|
|Cosmos-2B|1.58|**96.00**|**86.00**|70.00|
|Cosmos-14B|**1.62**|90.00|82.00|**76.00**|
|Cosmos-14B-Droid|1.58|78.00|58.00|34.00|
|Wan-14B|1.56|54.00|44.00|20.00|


_Table 2._ Percentage-based evaluation across Image-to-Video models, with best scores in bold. 

# **4. Experiments** 

**Experimental Setup** . We evaluate our approach in two stages. First, we assess the world model by testing the zero-shot spatial referring capabilities of four baseline video generation models—Cosmos-2B, Cosmos-14B, CosmosDroid, and Wan-14B—using a task-specific metric to select the best candidate for domain adaptation. We further validate improvements through real-world qualitative analyses after adaptation and adversarial distillation. Second, we perform rollouts in both simulated and real-world tasks to evaluate the effectiveness of our proposed policy in guiding robust and precise manipulation. 

**Simulation benchmark** : In the assessment of the whole policy, we conduct close loop evaluation on LIBERO benchmark (Liu et al., 2023). For the LIBERO benchmark, each task suite contains approximately 500 training samples (Specifically: Spatial—433, Object—456, Goal—436, and Long—389) and 10 test subtask samples. During evaluation, each test sample is executed 50 times, resulting in a total of 500 test runs per suite. 

**Real-world setup** : To evaluate the effectiveness of our method in real-world settings, we build a physical robotic experimental setup as illustrated in Figure 3. The platform employs a Franka 7-DoF robotic arm as the manipulation agent. An Intel RealSense D435 camera is mounted in a third-person view to provide visual observations of the 

5 

**Submission and Formatting Instructions for ICML 2026** 

_Table 3._ Quantitative comparison on the LIBERO (Liu et al., 2023) benchmark. Param denotes the scale of the VLM backbone. 

|Method|Param||Task S<br>|uite<br>||Total|
|---|---|---|---|---|---|---|
|||Spatial|Object|Goal|Long||
|OpenVLA (Kim et al.,2024b)|7|84.7|88.4|79.2|53.7|76.5|
|OpenVLA-OFT (Kim et al.,2025)|7|97.6|98.4|97.9|94.5|97.1|
|CoT-VLA (Zhao et al.,2025)|7|87.5|91.6|87.6|69.0|81.1|
|UniVLA (Bu et al.,2025)|7|96.5|96.8|95.6|92.0|95.2|
|WorldVLA (Cen et al.,2025)|7|87.6|85.2|75.1|54.1|74.8|
|4D-VLA (Zhang et al.,2025b)|4|88.9|95.2|90.9|79.1|88.6|
|SpatialVLA (Qu et al.,2025)|4|88.2|95.2|90.9|79.1|88.6|
|_π_0 (Black et al.,2025)|3|96.8|98.8|95.8|85.2|94.2|
|_π_0-FAST (Pertsch et al.,2025)|3|96.4|96.8|88.6|60.2|85.5|
|SmolVLA (Shukor et al.,2025)|2.25|93.0|94.0|91.0|77.0|88.8|
|GR00t N1 (Bjorck et al.,2025)|2|94.4|97.6|93.0|90.6|93.9|
|DreamVLA(Zhanget al.,2025c)|0.57|97.5|94.0|89.5|89.5|92.6|
|**Dream4manip (Ours)**|1.22|99.4|99.2|98.2|95.4|98.1|


robot. Teleoperation data are collected using a 3Dconnexion SpaceMouse. 

**Implementation Details** . For the world model, we train our model based on cosmos-predict2. We adopt FusedAdamW as the optimizer with a learning rate of 2<sup>_−_14</sup><sup>_._5</sup> . A lambda linear scheduler is used, with zero warm-up steps, a singlecycle length of 1,000 steps, _f_ max = 0 _._ 6, and _f_ min = 0. Training is conducted with FSDP-based distributed parallelism, where the context parallel size is set to 2, and exponential moving average (EMA) is enabled to stabilize convergence. The world model is trained for 10,000 iterations on the LIBERO benchmark, while real-world training is performed for 1,000 iterations. When training the action model, we initialize the VLM with Qwen2.5 and perform parameter-efficient fine-tuning of the VLM backbone using LoRA with a rank of 64. Training is conducted on 8 GPUs with a total batch size of 128. During training, we incorporate future video predictions generated by the world model as additional contextual inputs, and uniformly sample 8 frames from historical video segments as conditioning context. The learning rate is set to 2 _×_ 10<sup>_−_4</sup> , and the total number of training steps is 20,000. 

|**D**|**Time(s)**|**FVD** _↓_|**SSIM** _↑_|**PSNR** _↑_|**LPIPS** _↓_|
|---|---|---|---|---|---|
|1|10.72|1128.10|0.54_±_0.14|17.89_±_6.95|0.20_±_0.07|
|5|19.43|1445.19|-0.02_±_0.29|12.43_±_8.43|0.30_±_0.10|
|10|29.80|579.90|0.70_±_0.09|22.10_±_5.78|0.11_±_0.05|
|20|52.59|496.06|**0.72**_±_**0.09**|**22.48**_±_**5.67**|**0.10**_±_**0.04**|
|35|86.20|**488.06**|**0.72**_±_**0.09**|22.39_±_5.70|**0.10**_±_**0.04**|


_Table 4._ Ablation study on different denoise steps (D) on Cosmospredict2 2B model. Metrics are rounded to two decimals. 

## **4.1. Zero-shot Spatial Referring Abilities.** 

We evaluate four base image-to-video generation models on their spatial referring ability using four metrics on the task “Pick the block of a specific color and place it.” 

**Embodiment Consistency (EC)** is quantified by analyzing 

the frequency of three predefined cases in the generated videos, reflecting different levels of embodiment stability over time. Specifically, **Case I** corresponds to scenarios where the embodiment remains fully consistent across all frames and is assigned 3 points; **Case II** captures situations in which the embodiment undergoes changes but remains recognizable, receiving 2 points; and **Case III** denotes cases where the embodiment becomes difficult to recognize or is heavily distorted, which are assigned 1 point. 

EC is the average score across all generated videos. A higher EC indicates better consistency in predicting the robot embodiment. 

**Referring Success Rate (RSR)** measures whether the generated embodiment moves toward the correct target object based on its color. A success is recorded when the embodiment moves more than halfway toward the correct object. 

**Interaction Success Rate (ISR)** evaluates whether the embodiment successfully grasps the correct target object during the interaction. An interaction is considered a failure if any of the following conditions occur: (1) the target object moves unnaturally toward the gripper without physical contact; (2) the gripper fails to reach the target object’s position relative to the first frame; or (3) the gripper becomes severely distorted, rendering the interaction outcome ambiguous. 

**Task Completion Rate (TCR)** counts a success when the generated video shows the target object being correctly placed into the wooden box. 

We demonstrate those evaluation metrics in Table 2. Overall, the original Cosmos2 series models exhibit stronger spatial referring and manipulation abilities. In contrast, Cosmos14B-Droid suffers from a domain gap due to multiview fine-tuning, and the Wan model performs poorly because it lacks manipulation-focused training. 

The qualitative results can be observed in Figure 3. General- 

6 

**Submission and Formatting Instructions for ICML 2026** 


_Figure 3._ Qualitative results generated by different video generation models for the instruction “Move the blue block into the wooden box.” (a) Output from the Cosmos-predict2 2B model. The model incorrectly replaces the robot gripper with a Robotiq-style two-finger gripper, likely reflecting common embodiments in its training data. (b) Output from the Cosmos-predict2 14B model fine-tuned on DROID. This version predicts multiview videos from left, right, and wrist cameras, but the camera poses still differ from our test setup, leading to incorrect arm scale. (c) Output from the Wan2.2 14B model. Wan struggles to interpret complex instructions: it fails to infer that the robot should first pick up the block before moving it, and instead assumes the robot is already holding the blue block while moving toward the box. (d) Output from the Cosmos-predict2 2B model after domain adaptation. Domain adaptation enables the model to generate future predictions that remain consistent with the robot’s true embodiment. 


_Figure 4._ **Qualitative results on LIBERO** . We show world model generation results across different tasks. The red-bordered frame denotes the conditioning frame, while the remaining frames are generated. 

purpose video generation models such as WAN often fail to faithfully capture robot embodiment and task semantics, leading to incorrect gripper structures, mismatched camera poses, or flawed action reasoning. Large-scale pretrained Cosmos models exhibit better physical motion modeling, but still struggle to align with the real execution setup, whereas domain-adapted models produce predictions that remain consistent with the true robot configuration and task dynamics. 

## **4.2. Generation Quality among Video Models** 

We evaluate the generation quality of several video models, with quantitative results reported in Table 1. Across all metrics, the raw Cosmos models outperform the Wan model. Applying domain adaptation yields substantial improvements: for instance, FVD drops from 571.46 (C-2B) to 211.84 (C-2B-DA), while SSIM rises from 0.70 to 0.82, reflecting enhanced temporal coherence and frame-level fidelity. Notably, Cosmos-14B-Droid-F.T., despite being finetuned on robotic data, performs worse than the base Cosmos models (FVD 1098.24, SSIM 0.23). We attribute this degradation to the domain gap introduced by its multi-view training, which assumes camera configurations differing from our single third-person observations. This highlights that naive fine-tuning on robotic data can hurt performance when observation setups mismatch, motivating our targeted domain adaptation approach. 

7 

**Submission and Formatting Instructions for ICML 2026** 

Table 1(a) further shows consistent performance of our adapted world model across the LIBERO task suites. L- Goal achieves the highest PSNR (26.12), while L-Object exhibits the strongest SSIM (0.89) and lowest FVD (177.04). The relatively uniform metrics across all suites suggest that our adapted model generalizes effectively to manipulation tasks of varying complexity. Combining domain adaptation with latent adversarial distillation (C-2B-DA+Dis) in Table 1(b) maintains strong performance while enabling efficient few-step inference: SSIM improves slightly from 0.82 to 0.84, PSNR increases from 25.19 to 26.82, and FVD experiences a minor increase (211.84 _→_ 238.09), representing a modest trade-off for significant computational gains. 

off between video quality and generation speed, with 10 denoising steps offering a good balance. 

**Discussion** . While our results demonstrate significant improvements, several challenges remain. First, although adversarial distillation accelerates video prediction, achieving low-latency, fast control on resource-constrained robots requires further optimization. Second, long-horizon predictions can still accumulate errors, particularly in dynamic or cluttered environments; online correction, hybrid planning, or uncertainty-aware rollouts may help mitigate drift. Third, the performance of our in-context conditioned action model depends on the fidelity of generated videos, motivating methods robust to imperfect or partially inconsistent rollouts. 

## **4.3. Close-Loop Policy Evaluation** 

We first present the world model generation results in Figure 4. As shown, our model successfully predicts the task execution process by generating complete sequences of robot manipulation frames, demonstrating its ability to anticipate future trajectories. In particular, the third task in Figure 4, which requires picking up the alphabet soup can before placing the cream cheese box, represents a long-horizon manipulation challenge that our model handles effectively. Qualitative results in Table 1 further confirm this, with low FVD scores across all four task suites. 

Table 3 reports quantitative results across the LIBERO task suites, evaluating different types of generalization. All the methods are trained and evaluated under the same settings. Dream4manip consistently achieves the best overall performance, reaching a total success rate of 98.2% while using a moderate-sized backbone compared to large-scale VLA models. 

On LIBERO-Spatial, Dream4manip achieves a success rate of 99.4%, demonstrating strong robustness to spatial variations. On LIBERO-Object, it maintains 99.2%, indicating effective object-level generalization. For LIBERO-Goal, it reaches 98.6%, highlighting the benefit of imagination for multi-stage reasoning. On the challenging LIBEROLong suite, it achieves 95.4%, confirming its strength on long-horizon tasks. Overall, these results show that a videobased world model significantly improves closed-loop control across diverse generalization settings. 

## **4.4. Ablation of denoising steps** 

We analyze the effect of different denoising steps when generating videos using the Cosmos2 2B model, which is originally trained with 35 denoising steps for high-fidelity video synthesis. As shown in Table 4, SSIM and PSNR increase sharply, while FVD and LPIPS decrease sharply as the number of denoising steps increases from 1 to 10. Beyond 10 steps, the improvement slows and the metrics fluctuate around a stable value. Overall, this reveals a trade- 

**Future Work** . Looking forward, scaling to diverse embodiments and complex multi-step tasks remains a key challenge. Generalization across radically different robots, viewpoints, or environments may require broader pretraining and stronger embodiment-conditioned representations. Moreover, integrating predictive world models with language-driven policies offers a path toward compositional, instruction-aware manipulation, enabling robots to anticipate, plan, and adapt in novel scenarios—an important step toward general-purpose, adaptive embodied intelligence. 

# **5. Conclusion** 

We presented a unified framework that combines accelerated world modeling with in-context conditioned action prediction to enable precise, efficient robotic manipulation. Our three-stage design—world model selection and adaptation, adversarial distillation for fast video prediction, and in-context action modeling—overcomes key limitations of prior approaches, including limited temporal foresight, spatial inconsistency, and high computational cost. Extensive evaluation shows that high-quality, long-horizon video predictions significantly improve downstream action generation, with Cosmos2 models benefiting from domain adaptation and adversarial distillation to yield more reliable and robust manipulation. By bridging predictive visual foresight and control, our framework moves toward adaptive, anticipatory robots capable of planning and acting effectively in complex, real-world environments. 

# **Impact Statement** 

We enable robots to anticipate and act on future states by combining fast, predictive video generation with action modeling, significantly improving spatial reasoning, embodiment consistency, and task performance in real-world manipulation. While our work could influence a range of societal applications from manufacturing automation to assistive robotics, we do not identify any immediate ethical or 

8 

**Submission and Formatting Instructions for ICML 2026** 

safety concerns that require special emphasis here. 

# **References** 

- Bjorck, J., Castaneda, F., Cherniadev, N., Da, X., Ding, R.,˜ Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for general robot control. In _Robotics: Science and Systems_ , 2025. 

- Blattmann, A., Dockhorn, T., Kulal, S., Mendelevitch, D., Kilian, M., Lorenz, D., Levi, Y., English, Z., Voleti, V., Letts, A., et al. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_ , 2023. 

- Bu, Q., Yang, Y., Cai, J., Gao, S., Ren, G., Yao, M., Luo, P., and Li, H. Univla: Learning to act anywhere with taskcentric latent actions. In _Robotics: Science and Systems_ , 2025. 

- Cen, J., Yu, C., Yuan, H., Jiang, Y., Huang, S., Guo, J., Li, X., Song, Y., Luo, H., Wang, F., et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 

- Chi, C., Feng, S., Du, Y., Xu, Z., Cousineau, E., Burchfiel, B., and Song, S. Diffusion policy: Visuomotor policy learning via action diffusion. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

- Du, Y., Yang, S., Dai, B., Dai, H., Nachum, O., Tenenbaum, J., Schuurmans, D., and Abbeel, P. Learning universal policies via text-guided video generation. _Advances in neural information processing systems_ , 36:9156–9172, 2023. 

- Hu, Y., Guo, Y., Wang, P., Chen, X., Wang, Y.-J., Zhang, J., Sreenath, K., Lu, C., and Chen, J. Video prediction policy: A generalist robot policy with predictive visual representations. _arXiv preprint arXiv:2412.14803_ , 2024. 

- Huang, Y., Zhang, J., Zou, S., Liu, X., Hu, R., and Xu, K. Ladi-wm: A latent diffusion-based world model for predictive manipulation. _arXiv preprint arXiv:2505.11528_ , 2025. 

- Jang, J., Ye, S., Lin, Z., Xiang, J., Bjorck, J., Fang, Y., Hu, F., Huang, S., Kundalia, K., Lin, Y.-C., et al. Dreamgen: Unlocking generalization in robot learning through video world models. _arXiv preprint arXiv:2505.12705_ , 2025. 

- Kim, M., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., Vuong, Q., Kollar, T., Burchfiel, B., Tedrake, R., Sadigh, D., Levine, S., Liang, P., and Finn, C. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024a. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E. P., Sanketi, P. R., Vuong, Q., et al. Openvla: An open-source visionlanguage-action model. In _Conference on Robot Learning_ , pp. 2679–2713, 2024b. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. In _Robotics: Science and Systems_ , 2025. 

- Li, S., Gao, Y., Sadigh, D., and Song, S. Unified video action model. _arXiv preprint arXiv:2503.00200_ , 2025. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

- Liu, X., Gong, C., and Liu, Q. Flow straight and fast: Learning to generate and transfer data with rectified flow. _arXiv preprint arXiv:2209.03003_ , 2022. 

- Luo, S., Tan, Y., Huang, L., Li, J., and Zhao, H. Latent consistency models: Synthesizing high-resolution images with few-step inference. _arXiv preprint arXiv:2310.04378_ , 2023. 

- NVIDIA, Johan Bjorck andFernando Castaneda, N. C., Da,˜ X., Ding, R., Fan, L. J., Fang, Y., Fox, D., Hu, F., Huang, S., Jang, J., Jiang, Z., Kautz, J., Kundalia, K., Lao, L., Li, Z., Lin, Z., Lin, K., Liu, G., Llontop, E., Magne, L., Mandlekar, A., Narayan, A., Nasiriany, S., Reed, S., Tan, Y. L., Wang, G., Wang, Z., Wang, J., Wang, Q., Xiang, J., Xie, Y., Xu, Y., Xu, Z., Ye, S., Yu, Z., Zhang, A., Zhang, H., Zhao, Y., Zheng, R., and Zhu, Y. GR00T N1: An open foundation model for generalist humanoid robots. In _ArXiv Preprint_ , March 2025. 

- Pertsch, K., Stachowicz, K., Ichter, B., Driess, D., Nair, S., Vuong, Q., Mees, O., Finn, C., and Levine, S. Fast: Efficient action tokenization for vision-language-action models. In _Robotics: Science and Systems_ , 2025. 

- Qu, D., Song, H., Chen, Q., Yao, Y., Ye, X., Ding, Y., Wang, Z., Gu, J., Zhao, B., Wang, D., et al. Spatialvla: Exploring spatial representations for visual-language-action model. In _Robotics: Science and Systems_ , 2025. 

9 

**Submission and Formatting Instructions for ICML 2026** 

- Salimans, T. and Ho, J. Progressive distillation for fast sampling of diffusion models. _arXiv preprint arXiv:2202.00512_ , 2022. 

- Sauer, A., Boesel, F., Dockhorn, T., Blattmann, A., Esser, P., and Rombach, R. Fast high-resolution image synthesis with latent adversarial diffusion distillation. In _SIGGRAPH Asia 2024 Conference Papers_ , pp. 1–11, 2024a. 

- Sauer, A., Lorenz, D., Blattmann, A., and Rombach, R. Adversarial diffusion distillation. In _European Conference on Computer Vision_ , pp. 87–103. Springer, 2024b. 

- Shukor, M., Aubakirova, D., Capuano, F., Kooijmans, P., Palma, S., Zouitine, A., Aractingi, M., Pascal, C., Russi, M., Marafioti, A., et al. Smolvla: A vision-languageaction model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

- Tian, Y., Yang, S., Zeng, J., Wang, P., Lin, D., Dong, H., and Pang, J. Predictive inverse dynamics models are scalable learners for robotic manipulation. _arXiv preprint arXiv:2412.15109_ , 2024. 

- Vuong, A. D., Vu, M. N., An, D., and Reid, I. Action tokenizer matters in in-context imitation learning. _arXiv preprint arXiv:2503.01206_ , 2025. 

- Wen, J., Zhu, Y., Li, J., Tang, Z., Shen, C., and Feng, F. Dexvla: Vision-language model with plug-in diffusion expert for general robot control. _arXiv preprint arXiv:2502.05855_ , 2025. 

_Advances in Neural Information Processing Systems_ , 37: 103599–103618, 2024. 

   - Zhao, Q., Lu, Y., Kim, M. J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 1702–1713, 2025. 

   - Zhao, T. Z., Kumar, V., Levine, S., and Finn, C. Learning fine-grained bimanual manipulation with low-cost hardware, 2023. URL https://arxiv.org/abs/ 2304.13705. 

   - Zheng, R., Wang, J., Reed, S., Bjorck, J., Fang, Y., Hu, F., Jang, J., Kundalia, K., Lin, Z., Magne, L., et al. Flare: Robot learning with implicit world modeling. _arXiv preprint arXiv:2505.15659_ , 2025. 

   - Zhou, S., Du, Y., Chen, J., Li, Y., Yeung, D.-Y., and Gan, C. Robodreamer: Learning compositional world models for robot imagination. _arXiv preprint arXiv:2404.12377_ , 2024. 

   - Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. 

- Yang, M., Du, Y., Ghasemipour, K., Tompson, J., Schuurmans, D., and Abbeel, P. Learning interactive realworld simulators. _arXiv preprint arXiv:2310.06114_ , 1(2): 6, 2023. 

- Zhang, C., Zhang, X., Pan, W., Zheng, L., and Zhang, W. Generative visual foresight meets task-agnostic pose estimation in robotic table-top manipulation, 2025a. URL https://arxiv.org/abs/2509.00361. 

- Zhang, J., Chen, Y., Xu, Y., Huang, Z., Zhou, Y., Yuan, Y.-J., Cai, X., Huang, G., Quan, X., Xu, H., et al. 4d-vla: Spatiotemporal vision-language-action pretraining with cross-scene calibration. In _Advances in Neural Information Processing Systems_ , 2025b. 

- Zhang, W., Liu, H., Qi, Z., Wang, Y., Yu, X., Zhang, J., Dong, R., He, J., Wang, H., Zhang, Z., et al. Dreamvla: A vision-language-action model dreamed with comprehensive world knowledge. In _Advances in Neural Information Processing Systems_ , 2025c. 

- Zhang, Z., Li, Y., Wu, Y., Kag, A., Skorokhodov, I., Menapace, W., Siarohin, A., Cao, J., Metaxas, D., Tulyakov, S., et al. Sf-v: Single forward video generation model. 

10 

**Submission and Formatting Instructions for ICML 2026** 


_Figure 5_ 

# **A. Detailed definition of spatial referring abilities metrics.** 

We evaluate four base image-to-video generation models on their spatial referring ability using four metrics: Embodiment Consistency (EC), Referring Success Rate (RSR), Interaction Success Rate (ISR) and Task Completion Rate (TCR). Here we give the accurate definition and examples for these metrics. 

**Embodiment Consistency (EC)** is quantified by analyzing the frequency of three predefined cases in the generated videos, reflecting different levels of embodiment stability over time. Specifically, **Case I** corresponds to scenarios where the embodiment remains fully consistent across all frames and is assigned 3 points; **Case II** captures situations in which the embodiment undergoes changes but remains recognizable, receiving 2 points; and **Case III** denotes cases where the embodiment becomes difficult to recognize or is heavily distorted, which are assigned 1 point. 

EC is the average score across all generated videos. A higher EC indicates better consistency in predicting the robot embodiment. 

**Referring Success Rate (RSR)** measures whether the generated embodiment moves toward the correct target object based on its color. A success is recorded when the embodiment moves more than halfway toward the correct object. 

**Interaction Success Rate (ISR)** evaluates whether the embodiment successfully grasps the correct target object during the interaction. An interaction is considered a failure if any of the following conditions occur: (1) the target object moves unnaturally toward the gripper without physical contact; (2) the gripper fails to reach the target object’s position relative to the first frame; or (3) the gripper becomes severely distorted, rendering the interaction outcome ambiguous. 

**Task Completion Rate (TCR)** counts a success when the generated video shows the target object being correctly placed into the wooden box. 

# **B. Out-of-distribution test on spatial referring abilities of the selected world model.** 

As shown in Figure 5, we place 3 blocks with different colors (red, blue and yellow) 

11 

