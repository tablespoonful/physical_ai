---
title: "FAVLA: A Force-Adaptive Fast-Slow VLA model for Contact-Rich Robotic Manipulation"
date: "2026-02-27"
authors: "Yao Li; Peiyuan Tang; Wuyang Zhang; Chengyang Zhu; Yifan Duan; Weikai Shi"
url: https://arxiv.org/abs/2602.23648
pdf: https://arxiv.org/pdf/2602.23648
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.23648)** / [論文ページ](https://arxiv.org/abs/2602.23648)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**FAVLA: A Force-Adaptive Fast–Slow VLA model for Contact-Rich Robotic Manipulation** 

**Yao Li**<sup>* 1</sup> **Peiyuan Tang**<sup>* 2</sup> **Wuyang Zhang**<sup>1</sup> **Chengyang Zhu**<sup>3</sup> **Yifan Duan**<sup>1</sup> **Weikai Shi**<sup>1</sup> **Xiaodong Zhang**<sup>1</sup> **Zijiang Yang**<sup>1</sup> **Jianmin Ji**<sup>1</sup> **Yanyong Zhang**<sup>1</sup> 

# **Abstract** 

Force/torque feedback can substantially improve Vision–Language–Action (VLA) models on contact-rich manipulation, but most existing approaches fuse all modalities at a single operating frequency. This design ignores the mismatched sampling rates of real robot sensors, forcing downsampling of the high-frequency contact cues needed for reactive correction. Combined with common VLM–action-expert (AE) pipelines that execute action chunks largely open loop between expensive VLM updates, unified-frequency fusion often yields delayed responses to impacts, stick–slip, and force spikes. We propose FAVLA, a force-adaptive fast-slow VLA that decouples slow perception planning from fast contact-aware control. FAVLA runs a slow VLM at a fixed low frequency to encode modalities to produce latent representations and to predict near-future force variation. A fast AE then executes at a variable high frequency, conditioning on the latest force sequence data to generate reactive actions. We further introduce a force adapter that injects highfrequency force features into multiple AE layers, and adaptively schedules the AE’s execution frequency based on the VLM’s predicted force variation. Extensive experiments on contact-rich tasks demonstrate that FAVLA significantly outperforms baselines, achieving superior reactivity and success rates, especially with a smaller contact force during manipulation. 

# **1. Introduction** 

Vision–Language–Action (VLA) models have recently become practical toward general-purpose robotic manipula- 

> 1University of Science and Technology of China, Hefei, China<sup>2</sup> Xi’an Jiaotong University, Xi’an, China<sup>3</sup> Central South University, Changsha, China. Correspondence to: Wuyang Zhang _<_ wuyangz@ustc.edu.cn _>_ , Yanyong Zhang _<_ yanyongz@ustc.edu.cn _>_ . 

_Preprint. March 2, 2026._ 


_Figure 1._ **A comparison between the previous unified-frequency scheme and our force-adaptive fast–slow scheme for the VLA model.** (a) Previous methods process the vision, force, and proprioceptive state at a unified input frequency, generating openloop action chunks that cannot promptly exploit high-frequency force feedback. (b) Our scheme applies a force-adaptive fast-slow scheme. The VLM runs at a slow frequency to encode visual and language context, while the AE runs at a force-adaptive high frequency using the latest force data to generate closed-loop action chunks, enabling reactive robot control. 

tion by coupling the semantic generalization of large vision–language models (VLMs) with continuous control policies, often implemented as an action expert. With large-scale multi-task robot pretraining, _π_ 0-style VLA models (Black et al., 2024; 2025; Pertsch et al., 2025) have shown promising transfer across robots and tasks using vision, language, and proprioceptive state. However, reliable performance on contact-rich manipulation, such as insertion and tight-tolerance assembly, remains harder than free-space pick-and-place. In these settings, success depends not only on visual alignment, but on rapid motion correction as contact conditions change, including coping with abrupt events (impacts, stick–slip, jamming) that are weakly observable from vision alone. 

A natural response is to incorporate interaction signals including force/torque data into VLA inputs. Recent work has demonstrated improved success on contact-rich tasks 

1 

**FAVLA: A Force-Adaptive Fast–Slow VLA model for Contact-Rich Robotic Manipulation** 

by adding force/torque feedback to VLA models (Yu et al., 2025; Zhang et al., 2025b; Shahidzadeh et al., 2025) or to action policies (Xue et al., 2025; Chen et al., 2025b). Most existing approaches, however, fuse modalities under a single operating frequency and a single token stream ( _e.g._ , concatenating force tokens with visual tokens). In practice, this leaves two challenges unresolved. First, modality tokenization is typically imbalanced: vision contributes far more tokens than force, which can bias attention away from sparse force cues even when those cues are critical for contact regulation. Second, sensors operate at mismatched sampling rates ( _e.g._ , 15 Hz cameras _vs._ 100–1000 Hz force/torque sensors). In standard unified-frequency pipelines, highfrequency force data is downsampled to match the slowest modality, discarding the reactive signals that indicate failure and demand immediate correction information. 

This frequency mismatch is an important influencing factor in the VLM–AE control pattern. The mainstream VLMAE paradigm applies a low-frequency VLM inference and open-loop action chunk execution strategy to achieve robot control. This makes it difficult to reactively adjust actions in response to state/force changes during execution. This issue is especially critical in industrial contact-rich scenarios, such as high-precision assembly, where delayed action adjustment can lead to excessive manipulation forces and component damage. These limitations currently hinder the practical deployment of force-based VLA in real-world industrial manipulation. 

This paper argues that contact-rich VLA control should explicitly respect fast-slow sensing and control: semantic scene understanding is naturally “slow”, while contact feedback and corrective control should be “fast”. We operationalize this idea with FAVLA, a force-adaptive fast–slow VLA model that decouples semantic reasoning from forcereactive execution while preserving an end-to-end learning scheme. Concretely, we first introduce a _force-injected fast–slow VLA architecture_ to integrate “fast” and “slow” modalities into an end-to-end VLA model: (i) a slow VLM backbone that runs at a fixed low frequency to integrate vision, language, and a history of force measurements into a latent contextual representation, and (ii) a fast action expert that runs at a higher frequency on the latest proprioceptive state and force measurements to refine action chunks in a closed-loop manner. Meanwhile, to make the AE adjust the action directly according to the contact force data (rather than merely appended as extra tokens), we introduce a force adapter that injects the latest force information into multiple AE layers. Second, to enable reactive action adjustment, we further propose a _force-adaptive fast-slow inference strategy_ . Different from VLM, the AE runs at a variable high frequency that is adaptively scheduled based on future force variations predicted by the VLM. This design lets FAVLA keep low-frequency semantic reasoning and ac- 

tion output during free-space motion, while improving to high-frequency action adjustment when contact transitions are imminent or underway. Therefore, the system can reactively adjust actions to avoid large manipulation forces in industrial applications. 

We evaluate FAVLA on a suite of contact-rich manipulation tasks that require precise force regulation and rapid response to adjust actions. The results demonstrate that the forceadaptive fast-slow mechanism significantly improves both success rates and reactivity while maintaining lower peak contact forces. Compared to the strongest baseline methods, FAVLA improves task success rate by 13.8% and achieves an average success rate of 80.8%, validating its effectiveness for high-precision industrial manipulation. 

In summary, this paper makes the following contributions: 

- We propose a force-adaptive fast–slow VLA framework namely FAVLA that fuses slow semantic modalities (vision, language and force history) with fast interaction signals (latest force data) for closed-loop contact-rich control. 

- We present a force-injected action expert design with a force adapter that integrates high-frequency force feedback, enabling direct force-conditioned correction of action chunks. 

- A force-adaptive fast–slow inference strategy in which the slow VLM predicts near-future force variation is introduced to schedule the fast AE’s execution frequency, improving responsiveness during contact with a smaller manipulation force. 

- Extensive real-world experiments on contact-rich tasks show improved success rates and reduced peak contact forces compared to force-aware and vision-only baseline methods. 

# **2. Related Works** 

**Vision-Language-Action Models.** Nowadays, VLA models have emerged as a powerful paradigm for learning generalist robotic policies by large-scale multimodal pretraining (Zhang et al., 2025a). Autoregressive approaches (Brohan et al., 2022; Zitkovich et al., 2023; Kim et al., 2024) formulate control as next-token prediction over discretized actions, enabling scalable learning from large, heterogeneous datasets. Building on this foundation, generative VLA models (Black et al., 2024; 2025; Pertsch et al., 2025; Zhai et al., 2025) address action discretization by modeling continuous action trajectories via flow matching or diffusion-style objectives. More recently, hierarchical VLA architectures (Chen et al., 2025a; Zhang et al., 2024; Wen et al., 2025) introduce paradigms that decouple high-level reasoning from lowlevel execution, improving stability and efficiency. Inspired 

2 

**FAVLA: A Force-Adaptive Fast–Slow VLA model for Contact-Rich Robotic Manipulation** 

by these works, we leverage the strength of large-scale pretrained VLA models and promote a fast-slow strategy for contact-rich robotic manipulation. 

**Contact-Rich Manipulation Models.** Recent work on contact-rich manipulation extends learning-based policies by explicitly incorporating physical interaction signals beyond vision (Feng et al., 2024; Liu et al., 2025; He et al., 2025). Force-aware policies (Xue et al., 2025; Chen et al., 2025b) introduce slow–fast diffusion architectures that leverage force or force-related feedback to enable rapid corrective behaviors during contact while maintaining stable long-horizon execution. Subsequent works (Yu et al., 2025; Zhang et al., 2025b; Cheng et al., 2025) integrate force or torque signals into vision–language–action frameworks, allowing pretrained VLAs to adapt execution strategies based on contact states. Another line of research prefers tactilebased approaches (Huang et al., 2025a; Li et al., 2025; Huang et al., 2025b; Bi et al., 2025) that incorporate visuotactile sensing to provide fine-grained contact perception and tactile-aware execution. However, existing methods typically assume a unified operating frequency, which discards high-frequency force cues and limits reactive contact control. Our approach introduces a force-adaptive fast–slow framework that decouples semantic reasoning and force feedback across time scales, improving control responsiveness. 

In summary, current typical force-based VLA models treat all modalities to a single input frequency ( _e.g._ , applying the downsampling method on high-frequency modalities to match low-frequency modalities), which discards highfrequency contact cues and may cause to open-loop behaviors with force spikes. In contrast to mainstream VLM-AE pipelines that use a consistent running frequency, FAVLA introduces a force-injected fast–slow fusion strategy, which can adaptively adjust the action according to the future contact force. Meanwhile, the VLM runs at a rigid slow rate using vision, language, and force history data to predict future contact-force trends, while the AE runs at a higher and variable rate using the latest high-frequency force signals for reactive action correction. With these designs, FAVLA can effectively reduce force spikes and improve safety and success rates in high-precision industrial contact tasks. 

# **3. Methods** 

We propose FAVLA, a force adaptive Vision Language Action (VLA) model that applies a fast–slow fusion strategy: vision and language provide slowly varying semantic context, while proprioception and force require high-rate updates to regulate contact and respond to interaction transients. Sec. 3.1 formalizes the contact-rich tasks that require responsive control and reviews the standard _π_ 0 (Black et al., 2024) and our FAVLA frameworks. Sec. 3.2 describes the force-injected fast-slow VLA architecture. Sec. 3.3 presents 

a force-adaptive inference strategy that schedules the AE at a variable frequency based on predicted future force variation. 

## **3.1. Preliminary** 

**Problem Formulation.** We attempt to build a fast-slow VLA model to achieve high-precision industrial manipulation tasks with multimodal observations at different frequencies. These tasks require handling industrial products with low contact forces, enabling reactive and closed-loop control according to the robot’s observations, particularly when contact forces become large. At the timestep _t_ , we denote the robot’s observations as follows: 


where _It_<sup>(</sup><sup>_k_)</sup> denotes _k_ -th RGB images (an external camera and a wrist camera in our setting), **s** _t ∈_ R<sup>7</sup> is the proprioceptive state of the 6-DoF TCP (Tool Center Point of the end effector) pose and gripper width, **f** _t−τ_ +1: _t ∈_ R<sup>_τ×_6</sup> denotes a history force data sequence of 6-axis force measurements over a time window of length _τ_ , and **f**<sup>_′_</sup> _t−τ_ +1: _t ∈_ R<sup>_τ×_6</sup> is the latest force data sequence at time _t_ with a same time window length _τ_ . In our setting, we use a 6-axis force sensor mounted on the end effector, meanwhile, **f** _t_ = _{fx_<sup>_t, f_</sup> _y_<sup>_t, f_</sup> _z_<sup>_t, mt_</sup> _x_<sup>_, mt_</sup> _y_<sup>_, m_</sup> _z_<sup>_t}_,whichincludestheend-</sup> effector 3D force and torque components. Given a language manipulation instruction _L_ and observation _Ot_ , we aim to learn an end-to-end VLA model _π_ ( _At|Ot, L_ ) that outputs low-level action chunk _At_ = _{at, at_ +1 _, ..., at_ + _H−_ 1 _}_ to maximize the likelihood of real manipulation trajectory. Meanwhile, in the observation, the **s** _t_ and **f**<sup>_′_</sup> _t−τ_ +1: _t_ are updated at a higher frequency, _It_<sup>(</sup><sup>_k_)</sup> and **f** _t−τ_ +1: _t_ are updated at a low frequency. We aim to make the VLA adjust the action chunk reactively based on high-frequency inputs, particularly with the latest contact force. 

**Frameworks of** _π_ **0 and our FAVLA.** FAVLA is a forceadaptive fast-slow VLA model for contact-rich manipulation tasks based on the _π_ 0 (Black et al., 2024) framework. It consists of a larger VLM backbone and a smaller action expert of PaliGemma (Beyer et al., 2024). As shown in Fig. 2, FAVLA takes the multimodal inputs at different frequencies as input to the VLM and action expert, then generates action trajectories using a conditional flow matching model. The different modalities are encoded as tokens and fed into the FAVLA at different frequencies. Meanwhile, the smaller action expert has a higher inference frequency, with its frequency adaptively adjusted based on predicted future contact force variation. 

## **3.2. Force-Injected Fast–Slow VLA Model Architecture** 

FAVLA is designed to fuse multimodal sensory data at different sampling rates. We decompose the VLA model into (i) a slow VLM backbone that performs semantic scene- 

3 

**FAVLA: A Force-Adaptive Fast–Slow VLA model for Contact-Rich Robotic Manipulation** 


_Figure 2._ **Overview of the FAVLA** . FAVLA integrates a large Slow VLM Backbone for semantic reasoning, and a smaller Fast Action Expert for responsive action control. The model processes multimodal inputs at different frequencies and generates action trajectories via the conditional Flow Matching. Notably, the inference frequency of the Action Expert is adaptively adjusted by the Force-Adaptive Fast-Slow Inference Strategy, ensuring there is a smaller contact force during manipulation. 

and-instruction conditioning using vision, language and a low-rate force history sequence, and (ii) a fast action expert that performs force-reactive control using the latest highrate force measurements. The slow backbone produces a reusable context (denoted as KV Cache) for the fast module, while the fast action expert injects force information to refine actions across multiple layers. 

**Slow VLM Backbone.** The _slow_ component is a VLM transformer that integrates vision, language, and historical force data. RGB images from the external and wrist cameras are encoded into patch tokens by a SigLIP image encoder, and the language instruction is embedded by the Gemma tokenizer. Additionally, we apply a lightweight Temporal Convolutional Network (TCN) tokenizer to encode the history force data **f** _t−τ_ +1: _t_ into history force tokens **z** _f_ . Specifically, we first apply a 1 _×_ 1 temporal convolution to project each per-timestep force vector to a _df_ -dimensional feature, followed by a stack of causal dilated temporal blocks with residual connections. Each block uses two causal 1D convolutions with a dilation operation and layer normalization. Finally, we downsample the resulting sequence to _Nf_ tokens and generate history force tokens **z** _f ∈_ R<sup>_Nf ×df_</sup> _._ 

We concatenate vision tokens, language tokens, and force tokens **z** _f_ as prefix tokens for the slow VLM backbone, enabling full self-attention across modalities. The backbone outputs final Vision-Language-Force (VLF) tokens **H** VLF _∈_ R<sup>_S_pre</sup><sup>_×d_</sup> , where _S_ pre is the number of prefix tokens and _d_ is the model width. For reuse by the fast module, we cache the intermediate-layer key/value states for the prefix tokens at each layer **K**<sup>(</sup><sup>_ℓ_)</sup> _∈_ R<sup>_S_pre</sup><sup>_×nkv×dh_</sup> _,_ and **V**<sup>(</sup><sup>_ℓ_)</sup> _∈_ R<sup>_S_pre</sup><sup>_×nkv×dh_</sup> , where _nkv_ is the number of key/value heads, and _dh_ is the 

head dimension. 

**Fast Force-Injected Action Expert.** The _fast_ component is a small transformer that refines action chunks using highfrequency feedback. At time _t_ , it generates action chunks via flow matching, conditioned on the latest force sequence **f**<sup>_′_</sup> _t−τ_ +1: _t_ and robot state **s** _t_ , in addition to the slow updated VLM key/value cache _{_ **K**<sup>(</sup><sup>_ℓ_)</sup> _,_ **V**<sup>(</sup><sup>_ℓ_)</sup> _}_ . Meanwhile, rather than feeding force sequence into the action expert’s input sequence (which can dilute sparse force cues), we inject it into different layers through a _force adapter_ . Concretely, we apply the same TCN tokenizer on the **f**<sup>_′_</sup> _t−τ_ +1: _t_ to obtain the latest force tokens **z**<sup>_′_</sup> _f_ . Then, in each transformer layer, after self-attention with key/value cache, the noisy action token **z** _a_ performs cross-attention to **z**<sup>_′_</sup> _f_ , and we inject the resulting force-conditioned update additively: 


where ( **K** _f ,_ **V** _f_ ) are obtained by projecting **z**<sup>_′_</sup> _f_ into force keys/values, and **Q** _a_ are the noisy action queries. This force injection allows the AE to adjust action chunks based on high-frequency contact signals directly. 

**Force Variance Head.** Based on this fast-slow VLA model architecture, we add an auxiliary force variance head to predict future volatility of the contact force during manipulation. It instructs how to dynamically adjust the inference frequency discussed in Sec. 3.3. We select the VLF token from **H** VLF corresponding to the learnable input token for variance prediction. We then feed it to a MLP head to generate a scalar prediction. The prediction target is an EMA-filtered and weighted variance of the 6D force/torque 

4 

**FAVLA: A Force-Adaptive Fast–Slow VLA model for Contact-Rich Robotic Manipulation** 


_Figure 3._ **Our force-adaptive fast-slow inference strategy.** The fast AE runs multiple times within each action chunk, conditioned on real-time force. In each cycle, we fix the sampled noise and robot state, then perform the temporal ensemble on overlapped action chunks. The AE execution frequency is adaptively set from the VLM-predicted force variance. 

signal over a short future window defined by the action chunk size. We next introduce how to calculate the supervision label for force variance used in training. Given the future force sequence _ft_ : _t_ + _W −_ 1 _∈_ R<sup>_W ×_6</sup> from the dataset, we compute the raw volatility value as a weighted variance: 


Then we use the exponential moving average (EMA) smoothing algorithm over time to reduce measurement noise: 


After that, we perform a normalization operation on the _ν_ ¯ _t_ with the _tanh_ function of _ν_ ˜ _t_ = tanh� _~~<u>√</u>~~ σν_ <u>¯</u> _<u>t</u>_ �, and then train the force variance head to regress the normalized _ν_ ˜ _t_ . The supervision label is generated during dataset preprocessing. 

**Training objectives.** We jointly optimize the slow VLM, the fast action expert, and the force-variance predictor using a weighted sum between the action generation loss and the auxiliary variance prediction loss: 


where _λ_ is a hyperparameter to balance the auxiliary objective. We set _λ_ = 0 _._ 1 in all experiments. 

## **3.3. Force-Adaptive Fast-slow Inference Strategy** 

To enable high-frequency closed-loop control within an action chunk, we propose a Force-Adaptive Fast–Slow Infer- 

ence Strategy. The core idea is to decouple low-frequency visual reasoning from high-frequency force feedback, thereby leveraging their complementary strengths. 

In each cycle, the VLM performs a single forward pass to process multimodal observations and construct the KV cache, providing semantic context. Conditioned on the KV Cache and the latest force observations, the AE run multimes to generate high-frequency actions, thereby enabling closed-loop and reactive control. However, this naive inference strategy has two key limitations: (1) Fixed frequency cannot adapt to the task phase. Free-space motion and contact-rich phases demand fundamentally different inference frequencies, yet a static schedule treats them uniformly. (2) Lack of action chunk consistency. Due to the stochastic nature of the model, independent AE inferences within the same chunk may produce inconsistent actions, leading to jerky and unstable motion. We address these limitations with two targeted designs below. 

**Adaptive Inference Frequency.** Rather than using a fixed inference frequency, we make it a dynamic parameter that changes based on the contact situation. When contact is imminent or ongoing, we run the AE more frequently for better reactive control; during free-space motion, we run it less to save computation. 

Specifically, we use the VLM’s predicted force variance _ν_ ˜ _t ∈_ [0 _,_ 1] to measure how active the contact dynamics will be in the next cycle. Given a maximum frequency ratio _N_ max, we schedule the number of AE executions as: 


When ˜ _νt_ is small, the system runs at low frequency ( _nt_ = 1). As _ν_ ˜ _t_ approaches 1, more AE inferences are scheduled, providing faster response when contact occurs. 

**Consistent Action Ensemble.** To address within-chunk inconsistency caused by the stochastic nature of repeated AE inferences, we adopt two strategies. First, we fix the sampled noise **_ϵ_** across all AE calls within the same visual cycle, ensuring that all inferences share the same stochastic sample. Second, as shown in Fig. 3, we apply temporal ensemble (Zhao et al., 2023) to aggregate overlapping chunk predictions across visual cycles, producing smoother action execution across cycles. 

# **4. Experiments** 

In this section, we present a comprehensive evaluation of our proposed method on diverse real-world contact-rich tasks. We evaluate three key aspects: (1) the effectiveness of our method compared to strong baselines, (2) ablation studies validating each module’s contribution, and (3) visualization results and analysis. 

5 

**FAVLA: A Force-Adaptive Fast–Slow VLA model for Contact-Rich Robotic Manipulation** 


_Figure 4._ Real-world task scenarios and execution phases. Tasks include (1) USB Insertion, (2) Gear Assembly, (3) Box Flipping, and (4) Board Wiping. These tasks present diverse challenges: tasks 1 and 2 require millimeter-level precision for successful alignment, while tasks 3 and 4 demand real-time force adjustment to handle constantly changing contact dynamics. 


_Figure 5._ Experimental setup for robotic manipulation. (a) Overview of the hardware configuration, including the teleoperation device (3D Space Mouse), 6D-force and vision sensors, and the robotic gripper. (b) The set of experimental tasks. 

## **4.1. Experimental Setups** 

**Hardware Platform.** We use the Monte robot, a dual-arm whole-body robot with 7 degrees of freedom X-ARM arms. Each arm is equipped with a wrist-mounted RGB-D camera and a 6-axis force/torque sensor at the end-effector flange. We capture visual observations using a wrist camera and an external fixed camera as shown in Fig.5. 

**Experimental Tasks.** To evaluate the effectiveness of our proposed method, we conduct experiments on four tasks: USB Insertion, Gear Assembly, Box Flipping, and Board Wiping, as shown in Fig. 4. These tasks can be categorized into two groups: the first two are high-precision tasks requiring millimeter-level accuracy and real-time force feedback to prevent task failure due to excessive force, while the latter two are contact-rich tasks involving dynamic interactions and force feedback. We collect 80 demonstration trajectories for each high-precision task and 50 trajectories for each contact-rich task. Human demonstrations are collected 

through teleoperation with a 3D SpaceMouse, and all trajectories are synchronized and downsampled to a uniform frame rate of 30Hz. 

**Compared Baselines.** We compare our method with the following strong baselines: _π_ 0 (Black et al., 2024), _π_ 0 + Force, TA-VLA (Zhang et al., 2025b), and ForceVLA (Yu et al., 2025). _π_ 0 is a flow-matching based VLA model pretrained on large-scale data that demonstrates strong generalization on real-world tasks. _π_ 0 + Force incorporates force information by converting force data into tokens and concatenating them with the input sequence. TA-VLA introduces an auxiliary objective for future force prediction to enhance the model’s attention to force information. ForceVLA employs a Mixture-of-Experts (MoE) (Shazeer et al., 2017) architecture to learn features from both force and image modalities. All methods are fine-tuned on our collected dataset using LoRA (Hu et al., 2022) for fair comparison. 

**Evaluation Metrics.** We evaluate model performance using the task Success Rate. For each manipulation task, we establish binary success criteria based on task completion ( _e.g._ , full USB insertion, correct gear alignment). The success rate is computed as the ratio of successful trials to total trials, providing a direct measure of policy performance. Evaluation was conducted over 25 trials for USB Insertion, 30 trials for Gear Assembly, 20 trials for Box Flipping, and 10 trials for Board Wiping. We also use Average peak contact forces (N) to evaluate contact forces during manipulation. 

**Implementation Details.** We follow the _π_ 0 architecture, where the VLA consists of a VLM and an action expert. We initialize the model using the _π_ 0 weights and apply LoRA (Hu et al., 2022) to fine-tune both the VLM and action expert. The LoRA parameters are configured with _r_ = 16 _, α_ = 16 for the VLM and _r_ = 32 _, α_ = 32 for the action expert, applied to both attention and feedforward layers. We train all models for 30,000 iterations with a 

6 

**FAVLA: A Force-Adaptive Fast–Slow VLA model for Contact-Rich Robotic Manipulation** 


_Figure 6._ Comparison of the success rate of our proposed method with baselines on four real-world tasks. Our method significantly outperforms all baselines on four contact-rich tasks. 

learning rate of 2 _._ 5 _×_ 10<sup>_−_5</sup> using a cosine decay schedule. The batch size is set to 8, and training is conducted on an Nvidia A100 GPU with 80GB of memory. 

## **4.2. Evaluation Results** 

**Overall Performance.** As shown in Fig. 6, FAVLA achieves the best performance across all contact-rich manipulation tasks. Our method achieves an average success rate of 80.8%, outperforming the vision-only _π_ 0 baseline by 38.0 percentage points and surpassing the best baseline ForceVLA by 13.8 percentage points. These results highlight the effectiveness of our approach. 

We observe particularly significant improvements on Gear Assembly (93.3%) and Board Wiping (70.0%). This is attributed to the force-sensitive nature of these tasks. Notably, gear assembly is highly sensitive to excessive force, where even a slight over-application can trigger safety thresholds and cause failure, while board wiping requires maintaining a consistent contact force throughout the motion. Our proposed Force-Adaptive Fast-Slow inference mechanism addresses this by providing closed-loop force control, enabling reactive action adjustments based on high-frequency force feedback. 

**Capabilities of Force Control.** We further validate the force control capability by measuring average peak contact forces. This metric captures the maximum contact force at the end effector during each trial, averaged across all trials per task. We select Box Flipping and Gear Assembly tasks for evaluation because the gear and carton box can easily break under high manipulation force. As shown in Table 1, FAVLA maintains forces within safe and effective ranges, achieving peak contact forces of 7.7 N on the Gear Assembly task and 9.9 N on the Box Flipping task, representing reductions of 4.3 N and 2.3 N respectively compared to the vision-only baseline. In contrast, baselines such as _π_ 0 and _π_ 0 + Force frequently apply excessive force to complete tasks, potentially causing damage to objects or the 

_Table 1._ Average peak contact forces (N) across contact-rich tasks. Lower values indicate safer and more compliant manipulation. 

|**Method**|**Gear Assembly**|**Box Flipping**|
|---|---|---|
|_π_0|12.0 N|12.2 N|
|_π_0 + Force|13.0 N|13.8 N|
|TA-VLA|11.3 N|10.0 N|
|ForceVLA|10.9 N|12.4 N|
|**FAVLA (Ours)**|**7.7 N**|**9.9 N**|


_Table 2._ **Ablation study on proposed components.** We validate the effectiveness of each component by incrementally adding it to the vision-only baseline. 

|**Configuration**|**Box Flipping**|**Board Wiping**|
|---|---|---|
|Vision-Only|50%|10%|
|+ Force-Injected AE|65%|60%|
|+ Force Variance Prediction|70%|60%|
|+ Force-Adaptive Inference|**80**%|**70**%|


robot itself. This significant reduction in peak forces demonstrates the effectiveness of our adaptive fast-slow inference strategy, which enables precise force regulation through high-frequency closed-loop action control. 

## **4.3. Ablation Studies** 

**Ablation Study on Proposed Components.** To validate our architectural design, we conduct an ablation study by progressively integrating each proposed component into a vision-only baseline, as shown in Table 2. The Vision-Only baseline shows limited capability, achieving only 50% and 10% on Box Flipping and Board Wiping, respectively. Force injection to the Action Expert improves performance to 65% and 60%, demonstrating the effectiveness of incorporating force modality. The introduction of Force Variance Prediction further boosts the success rate of Box Flipping to 

7 

**FAVLA: A Force-Adaptive Fast–Slow VLA model for Contact-Rich Robotic Manipulation** 


_Figure 7._ **Ablation study on frequency ratio.** Performance comparison between static frequency ratios ( _n_ AE steps per VLM step) and our proposed adaptive frequency mechanism. Our adaptive approach significantly outperforms all static frequency settings across both tasks. 

70%, demonstrating that modeling the uncertainty of future contact forces helps the model better understand complex manipulation physics for action generation. Finally, the addition of the Force Variance Prediction module with an adaptive frequency mechanism leads to performance improvements of 80% and 70%, validating its effectiveness. 

**Ablation Study on Force-Adaptive Frequency Adjustment.** To evaluate the effectiveness of the force-adaptive frequency mechanism, we conduct ablation experiments on two manipulation tasks of USB Insertion and Gear Assembly. We compare three inference strategies: (1) static frequency with fixed ratios of _n_ = 1 _,_ 2 _,_ 4, and (2) our proposed force-adaptive frequency mechanism. As shown in Fig. 7, the results indicate that within the fixed-frequency strategies, the success rate consistently improves as the execution frequency _n_ increases. This suggests that a higher inference frequency generally provides better responsiveness for contact-rich tasks. Notably, our proposed force-adaptive strategy consistently outperforms all fixed-frequency approaches, achieving a 93% success rate in the Gear Assembly task and a significant boost to 80% in the USB Insertion task. This demonstrates that dynamically adjusting the frequency based on real-time force demands is more effective than maintaining a constant high frequency, as it avoids frequent switching between different action chunks during non-contact phases, thereby ensuring better temporal execution of the predicted action trajectories. 

## **4.4. Visualization of Adaptive Frequency Prediction** 

Fig. 8 shows the model’s ability to adjust execution frequency based on predictions of future force variances, derived from current multi-modal observations. Although the model does not have access to future data during inference, we utilize future force variance (Fig. 8b) as a post-hoc metric to validate its predictions. The results show that the model can accurately predict upcoming physical interactions. As shown in Fig. 8c, it increases its update frequency just before entering phases where contact is expected, which 


_Figure 8._ **Visualization of adaptive frequency prediction.** (a) Raw force measurements. (b) Computed force variance is used to identify environmental dynamics. (c) Model-predicted frequency ratio, demonstrating increased execution frequency in areas where contact is more likely to occur. 

require high-precision control. Conversely, it reduces the frequency to 1× during stable periods with little or no contact. This adaptive behavior highlights the system’s ability to adjust based on predicted contact events, ensuring precise control during critical interactions without the need for manual rules or prior knowledge. 

# **5. Conclusion** 

In this paper, we present FAVLA, a force-adaptive VLA framework designed to fuse “slow” semantic modalities (vision, language, and history force) with “fast” proprioceptive state and force signals into a single end-to-end VLA model. Meanwhile, our force-injected fast–slow architecture employs a large VLM model to extract the vision–language–force context and to predict future contact force variations. In parallel, an action expert is proposed to leverage high-frequency force measurements to reactive action adjustment by using a force adapter that injects contact force information into multiple layers. With this architecture, we further introduce a force-adaptive fast–slow inference strategy that uses predicted force variations to adjust the action expert’s execution frequency. This allows the model to correct the action trajectoies timely, especially when there is a large contact force. Extensive real-robot experiments on contact-rich industrial tasks show that FAVLA achieves an 80 _._ 8% overall success rate and reduces peak contact forces, outperforming baseline VLA methods by an average of 13 _._ 8% in success rate. These results demonstrate that employing the force-adaptive fast–slow strategy in the end-to-end VLA model is an effective way to realize reactive and high-precision manipulation. 

8 

**FAVLA: A Force-Adaptive Fast–Slow VLA model for Contact-Rich Robotic Manipulation** 

# **Impact Statement** 

This paper presents work whose goal is to advance the field of deep learning for robotic manipulation, particularly in contact-rich and high-precision industrial tasks. By enabling force-adaptive, reactive control within Vision–Language–Action models, our approach has the potential to improve the safety, reliability, and efficiency of robotic systems operating in physical environments. These capabilities may benefit industrial automation and related applications. 

# **References** 

- Beyer, L., Steiner, A., Pinto, A. S., Kolesnikov, A., Wang, X., Salz, D., Neumann, M., Alabdulmohsin, I., Tschannen, M., Bugliarello, E., et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- Bi, J., Ma, K. Y., Hao, C., Shou, M. Z., and Soh, H. VLATouch: Enhancing Vision-Language-Action Models with Dual-Level Tactile Feedback. (arXiv:2507.17294), 2025. doi: 10.48550/arXiv.2507.17294. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M. R., Finn, C., Fusai, N., Galliker, M. Y., et al. _π_ 0 _._ 5: A vision-language-action model with open-world generalization. In _9th Annual Conference on Robot Learning_ , 2025. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- Chen, H., Liu, J., Gu, C., Liu, Z., Zhang, R., Li, X., He, X., Guo, Y., Fu, C.-W., Zhang, S., et al. Fast-in-slow: A dual-system foundation model unifying fast manipulation within slow reasoning. _arXiv preprint arXiv:2506.01953_ , 2025a. 

- Chen, W., Xue, H., Wang, Y., Zhou, F., Lv, J., Jin, Y., Tang, S., Wen, C., and Lu, C. Implicitrdp: An end-to-end visualforce diffusion policy with structural slow-fast learning. (arXiv:2512.10946), 2025b. doi: 10.48550/arXiv.2512. 10946. 

- Cheng, Z., Zhang, Y., Zhang, W., Li, H., Wang, K., Song, L., and Zhang, H. Omnivtla: Vision-tactile-languageaction model with semantic-aligned tactile sensing. _arXiv preprint arXiv:2508.08706_ , 2025. 

- Feng, R., Hu, D., Ma, W., and Li, X. Play to the score: Stage-guided dynamic multi-sensory fusion for robotic manipulation. _arXiv preprint arXiv:2408.01366_ , 2024. 

- He, Z., Fang, H., Chen, J., Fang, H.-S., and Lu, C. Foar: Force-aware reactive policy for contact-rich robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 

- Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., Chen, W., et al. Lora: Low-rank adaptation of large language models. _ICLR_ , 1(2):3, 2022. 

- Huang, B., Wang, Y., Yang, X., Luo, Y., and Li, Y. 3DViTac: Learning Fine-Grained Manipulation with VisuoTactile Sensing. (arXiv:2410.24091), 2025a. doi: 10. 48550/arXiv.2410.24091. 

- Huang, J., Wang, S., Lin, F., Hu, Y., Wen, C., and Gao, Y. Tactile-VLA: Unlocking Vision-Language-Action Model’s Physical Knowledge for Tactile Generalization. (arXiv:2507.09160), 2025b. doi: 10.48550/arXiv.2507. 09160. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Langley, P. Crafting papers on machine learning. In Langley, P. (ed.), _Proceedings of the 17th International Conference on Machine Learning (ICML 2000)_ , pp. 1207–1216, Stanford, CA, 2000. Morgan Kaufmann. 

- Li, J., Wu, T., Zhang, J., Chen, Z., Jin, H., Wu, M., Shen, Y., Yang, Y., and Dong, H. Adaptive VisuoTactile Fusion with Predictive Force Attention for Dexterous Manipulation. (arXiv:2505.13982), 2025. doi: 10.48550/arXiv.2505.13982. 

- Liu, W., Wang, J., Wang, Y., Wang, W., and Lu, C. Forcemimic: Force-centric imitation learning with forcemotion capture system for contact-rich manipulation. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 1105–1112. IEEE, 2025. 

- Pertsch, K., Stachowicz, K., Ichter, B., Driess, D., Nair, S., Vuong, Q., Mees, O., Finn, C., and Levine, S. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- Shahidzadeh, A.-H., Caddeo, G. M., Alapati, K., Natale, L., Fermuler, C., and Aloimonos, Y.¨ Feelanyforce: Estimating contact force feedback from tactile sensation for vision-based tactile sensors. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 251–257. IEEE, 2025. 

9 

**FAVLA: A Force-Adaptive Fast–Slow VLA model for Contact-Rich Robotic Manipulation** 

- Shazeer, N., Mirhoseini, A., Maziarz, K., Davis, A., Le, Q. V., Hinton, G. E., and Dean, J. Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. _ArXiv_ , abs/1701.06538, 2017. URL https://api. semanticscholar.org/CorpusID:12462234. 

- Wen, J., Zhu, Y., Zhu, M., Tang, Z., Li, J., Zhou, Z., Liu, X., Shen, C., Peng, Y., and Feng, F. Diffusionvla: Scaling robot foundation models via unified diffusion and autoregression. In _Forty-second International Conference on Machine Learning_ , 2025. 

- Xue, H., Ren, J., Chen, W., Zhang, G., Fang, Y., Gu, G., Xu, H., and Lu, C. Reactive diffusion policy: Slow-fast visualtactile policy learning for contact-rich manipulation. (arXiv:2503.02881), 2025. doi: 10.48550/arXiv.2503. 02881. 

- Yu, J., Liu, H., Yu, Q., Ren, J., Hao, C., Ding, H., Huang, G., Huang, G., Song, Y., Cai, P., et al. Forcevla: Enhancing vla models with a force-aware moe for contact-rich manipulation. _arXiv preprint arXiv:2505.22159_ , 2025. 

- Zhai, A., Liu, B., Fang, B., Cai, C., Ma, E., Yin, E., Wang, H., Zhou, H., Wang, J., Shi, L., et al. Igniting vlms toward the embodied space. _arXiv preprint arXiv:2509.11766_ , 2025. 

- Zhang, J., Guo, Y., Chen, X., Wang, Y.-J., Hu, Y., Shi, C., and Chen, J. Hirt: Enhancing robotic control with hierarchical robot transformers. _arXiv preprint arXiv:2410.05273_ , 2024. 

- Zhang, J., Guo, Y., Hu, Y., Chen, X., Zhu, X., and Chen, J. UP-VLA: A unified understanding and prediction model for embodied agent. In _Forty-second International Conference on Machine Learning_ , 2025a. 

- Zhang, Z., Xu, H., Yang, Z., Yue, C., Lin, Z., Gao, H.a., Wang, Z., and Zhao, H. Ta-vla: Elucidating the design space of torque-aware vision-language-action models. _arXiv preprint arXiv:2509.07962_ , 2025b. 

- Zhao, T., Kumar, V., Levine, S., and Finn, C. Learning fine-grained bimanual manipulation with low-cost hardware. _ArXiv_ , abs/2304.13705, 2023. URL https: //api.semanticscholar.org/CorpusID: 258331658. 

- Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. 

10 

**FAVLA: A Force-Adaptive Fast–Slow VLA model for Contact-Rich Robotic Manipulation** 

# **A. Appendix** 

## **A.1. Teleoperation System** 

Our teleoperation system is shown in Fig. 9. An operator controls the robot in end-effector space using a 3D SpaceMouse. The relative motion of the SpaceMouse is scaled and mapped to the robot’s relative end-effector motion. To address the lack of force feedback, we convert the force readings into audio signals. Each of the 6 force dimensions is mapped to a distinct audio frequency (220-880 Hz), enabling the operator to identify which direction is experiencing force. The sound volume is proportional to the force magnitude. The operator wears headphones to perceive both the direction and magnitude of contact forces through real-time audio feedback. 

## **A.2. Data Collection Details** 


We collect demonstration data through human teleoperation using the system described in Section A.1. A human operator controls the robot arm via a 3D SpaceMouse to complete manipulation tasks, while the _Figure 9._ Teleoperation system setup. system simultaneously records trajectory data, including robot states, force/torque measurements, and camera observations. 

To increase trajectory diversity, we randomize the initial positions of both the robot arm and task objects at the beginning of each demonstration. We find that varying positions helps the model learn more generalizable manipulation strategies. 

During teleoperation, we record multiple data streams at different frequencies: end-effector poses and 6D force/torque readings at 200 Hz, along with external camera and wrist camera images at 30 Hz with a resolution of 640 _×_ 360. All streams are synchronized and downsampled to 30 Hz for temporal alignment. The collected dataset is then converted to the LeRobot v2.1 format for subsequent training. 

## **A.3. Dataset Statistics** 

We present dataset statistics for our collected datasets in Table 3, including the number of trajectories and frames per task. Our dataset comprises four contact-rich manipulation tasks, with a total of 260 trajectories and 198,250 frames, corresponding to approximately 1.84 hours of real-world time. Although the dataset size is relatively small, we find that the high diversity of trajectories enables the model to learn how to perform the tasks effectively. 

_Table 3._ Dataset statistics for the four manipulation tasks. 

|**Task**|**Trajectories**|**Frames**|**Hours**|
|---|---|---|---|
|USB Insertion|80|44,716|0.41 h|
|Gear Assembly|80|58,038|0.54 h|
|Box Flipping|50|47,476|0.44 h|
|Board Wiping|50|48,020|0.45 h|
|**Total**|**260**|**198,250**|**1.84 h**|


## **A.4. Task Description** 

**USB Insertion.** The goal of this task is to fully insert a USB drive into a standard USB port. The robot initially holds a USB drive in its gripper. To successfully complete the task, it must first move above the target port, align the drive with the port, and finally perform the insertion. This task demands sub-millimeter precision, as even slight misalignment can result in insertion failure. 

**Gear Assembly.** The goal is to mount a gear held by the robot gripper onto a central pillar on the base, ensuring its teeth fully mesh with two pre-installed adjacent gears on both sides. This task presents two main challenges: First, the gear’s hole must be aligned with the pillar. Since the hole is not visible, the robotic arm must rely on real-time force feedback to 

11 

**FAVLA: A Force-Adaptive Fast–Slow VLA model for Contact-Rich Robotic Manipulation** 

_Table 4._ Specification of the observation and action spaces. 

|**Field**|**Components**|**Shape**|
|---|---|---|
|**Action (Chunk Size = 32)**|||
|Delta End-Effector Pose + Gripper Width|∆_x,_∆_y,_∆_z,_∆_ϕ,_∆_θ,_∆_ψ, g_|32_×_7|
|**Observation**|||
|End-Effector Pose + Gripper Width|_x, y, z, ϕ, θ, ψ, g_|7|
|Force / Torque History (10 Steps)|_fx, fy, fz, τx, τy, τz_|10_×_6|
|Head Image|RGB|360_×_640_×_3|
|Wrist Image|RGB|360_×_640_×_3|
|Text Instruction|Tokenized Text Sequence|48|


determine alignment. Second, for proper meshing, the robot also needs to use force feedback to ensure the gear is aligned during the final engagement. 

**Box Flipping.** The objective of this task is to flip a horizontally placed cardboard box to a vertical orientation. This task requires the robot to adapt to constantly changing contact forces and, based on force feedback, adjust the direction and magnitude of the applied force to avoid damaging the cardboard box with excessive force or causing it to slip due to insufficient contact. 

**Board Wiping.** This task requires the robot to grasp the eraser and erase the markings on the board. The challenge lies in ensuring stable contact between the eraser and the board surface to apply sufficient force for effective erasure. 

## **A.5. Training Details** 

The observation and action spaces are defined in Table 4. The robot’s input consists of multi-modal observations, including RGB images from wrist and external cameras, proprioceptive state, 6-axis force/torque data, and language instructions. The output is an action chunk with a chunk size of 32. 

We present the model architecture and parameters in Table 5. We adopt the _π_ 0 architecture, which integrates a VisionLanguage Model (VLM) and an action expert, and add a new force variance network to predict the force variance. The VLM and action expert are initialized with _π_ 0 pre-trained weights, and using LoRA to fine-tune the model, while the force variance network is trained from scratch. 

We train a task-specific model on each dataset for 30,000 iterations with a batch size of 8, using the AdamW optimizer and a cosine decay learning rate schedule (initial learning rate 2 _._ 5 _×_ 10<sup>_−_5</sup> , minimum learning rate 1 _×_ 10<sup>_−_6</sup> ). Training takes approximately 6 hours on a single NVIDIA A100 80GB GPU. 

To enhance robustness, we apply data augmentation that includes random cropping and _±_ 15<sup>_◦_</sup> rotation for non-wrist images, as well as color adjustments with _±_ 0 _._ 2 in brightness, contrast, and saturation for all cameras. 

## **A.6. Qualitative results** 

**Real-World Visualizations.** As shown in Fig. 10, Fig. 11, Fig. 12, and Fig. 13, we visualize the execution process of the tasks in detail. Our observations show that our model can adapt to various perturbations, including angular rotation, unseen colors, and boxes of different shapes, with strong generalization ability and robustness. For the USB Insertion task, the model can adapt to angularly rotated sockets and adjust its position via force feedback to achieve precise insertion even when misaligned. For the Gear Assembly task, the model possesses strong generalization to unseen gears, including those with unseen colors that were not included in training, and can successfully insert such gears. For the Box Flipping task, the model has excellent force control to prevent box slipping and features effective adaptation to various unseen box sizes. For the Board Wiping task, the model can generalize to markers of different colors and text. Overall, our model demonstrates strong robustness and generalization ability in real-world manipulation tasks, which verifies its practical applicability and reliability. 

**Failure Case Analysis.** We conduct a systematic analysis of typical failure cases across all four manipulation tasks to identify key limitations and their root causes, as shown in in Fig. 14. 

12 

**FAVLA: A Force-Adaptive Fast–Slow VLA model for Contact-Rich Robotic Manipulation** 

_Table 5._ Summary of model architecture and hyperparameters 

|**Module**|**Configuration**|
|---|---|
|**Vision-Language Model**||
|Total Parameters|2.6B|
|Transformer Layers|18|
|Hidden Dimension|2048|
|FFN Hidden Dimension|16384|
|Attention Mechanism|Grouped Query Attention, 8 query heads, 1 key-value head, head<br>~~d~~im = 256|
|LoRA|rank_r_ = 16, scaling factor_α_= 16|
|**Action Expert**||
|Total Parameters|300M|
|Transformer Layers|18|
|Hidden Dimension|1024|
|FFN Hidden Dimension|4096|
|Attention Mechanism|Grouped Query Attention, 8 query heads, 1 key-value head, head<br>~~d~~im = 256|
|LoRA|rank_r_ = 32, scaling factor_α_= 32|
|**TCN Force Encoder**||
|Total Parameters|25.2M|
|TCN Blocks|4|
|Hidden Dimension|1024|
|Convolution Kernel Size|3|
|Dilation Rates|[1_,_2_,_4_,_8]|
|Dropout Rate|0.1|
|Activation Function|Swish|
|Number of Output Force Tokens|4|
|**Force Variance Predictor**||
|Total Parameters|1.6M|
|MLP Hidden Dimensions|(256_,_128)|
|Input Dimension|6144|
|Output Dimension|1|
|Dropout Rate|0.1|
|Activation Function|GELU|


For the USB Insertion task, the robot sometimes opens the gripper before a successful insertion, and this situation only occurs when the USB disk is misaligned with the socket. This failure is caused by the robot’s wrong understanding of force feedback: the large contact force from misalignment is similar to the force when the USB disk is fully inserted, making the robot mistakenly believes the task is finished and open the gripper. 

For the Gear Assembly task, the main failure is that the contact force is too large and exceeds the safety limit, which makes the system stop working. This problem happens when the gear and the central pillar are not aligned properly, and the robot still applies downward force to insert the gear, leading to a large contact force that triggers the safety stop. 

For the Box Flipping task, the main failure is that the contact force is insufficient, which causes the box to slip. This problem happens because the robot applies too little force to avoid damaging the object, and this insufficient contact force leads to the box slipping. 

For the Board Wiping task, the main failure is that the board is not wiped clean, with visible ink residue remaining on the board. This problem happens because the wiping trajectory is not correct, and the robot fails to cover the upper markers, which leads to the board not being wiped clean. 

13 

**FAVLA: A Force-Adaptive Fast–Slow VLA model for Contact-Rich Robotic Manipulation** 


_Figure 10._ Qualitative results on the real-world **USB Insertion** task. Our model successfully handles power strip rotations of up to 30<sup>_◦_</sup> . 


_Figure 11._ Qualitative results on the real-world **Gear Assembly** task. Our model successfully generalizes to gears of unseen colors. 

14 

**FAVLA: A Force-Adaptive Fast–Slow VLA model for Contact-Rich Robotic Manipulation** 


_Figure 12._ Qualitative results on the real-world **Box Flipping** task. Our model generalizes to boxes of unseen sizes. 


_Figure 13._ Qualitative results on the real-world **Board Wiping** task. Our model generalizes to marker ink of unseen colors. 

15 

**FAVLA: A Force-Adaptive Fast–Slow VLA model for Contact-Rich Robotic Manipulation** 


_Figure 14._ Visualization of failure cases across different tasks. 

16 

