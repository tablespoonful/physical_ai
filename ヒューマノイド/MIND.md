---
title: "MIND: Multi-Scale Intent Diffusion for Text-Driven Physics-Based Humanoid Control"
date: "2026-05-25"
authors: "Bin Li; Ruichi Zhang; Han Liang; Jingyan Zhang; Juze Zhang; Xin Chen"
url: https://arxiv.org/abs/2605.26006
pdf: https://arxiv.org/pdf/2605.26006
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.26006)** / [論文ページ](https://arxiv.org/abs/2605.26006)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# MIND: Multi-Scale Intent Diffusion for Text-Driven Physics-Based Humanoid Control 

BIN LI<sup>∗</sup> , ShanghaiTech University, China RUICHI ZHANG<sup>∗</sup> , University of Pennsylvania, USA HAN LIANG<sup>†</sup> , Bytedance Seed, China JINGYAN ZHANG, ShanghaiTech University, China JUZE ZHANG, Stanford University, USA XIN CHEN, Bytedance Seed, USA JINGYA WANG<sup>†</sup> , ShanghaiTech University, InstAdapt, China 


Fig. 1. **MIND** is a novel end-to-end diffusion framework tailored for text-driven physics-based humanoid control, capable of generating high-quality, diverse, and physically plausible humanoid behaviors such as dancing, kickboxing, and cartwheels. 

Enabling physics-based humanoids to execute diverse behaviors from highlevel textual commands remains a significant challenge. Existing methods typically follow either a two-stage paradigm that combines kinematic motion generation with physics-based tracking, or an end-to-end imitation-learning paradigm that directly generates actions from text. However, the former suffers from the inherent domain shift between kinematic generation and physics-based tracking, while the latter struggles with the substantial modality gap between textual commands and low-level actions, limiting effective semantic alignment. Notably, humanoid states encode rich motion dynamics that are more semantically aligned with textual descriptions than low-level actions, making them a natural basis for deriving behavioral intent. Building 

∗Equal contribution. 

†Corresponding author. 

Authors’ Contact Information: Bin Li, ShanghaiTech University, China, libin3@ shanghaitech.edu.cn; Ruichi Zhang, University of Pennsylvania, USA, rczhang@ seas.upenn.edu; Han Liang, Bytedance Seed, China, lianghan@shanghaitech.edu.cn; Jingyan Zhang, ShanghaiTech University, China, zhangjy7@shanghaitech.edu.cn; Juze Zhang, Stanford University, USA, juze@stanford.edu; Xin Chen, Bytedance Seed, USA, chenxin2@shanghaitech.edu.cn; Jingya Wang, ShanghaiTech University, InstAdapt, China, wangjingya@shanghaitech.edu.cn. 

upon this insight, we propose MIND, a novel end-to-end diffusion framework for text-driven physics-based humanoid control that leverages behavioral intent as a semantic bridge between textual commands and low-level actions. At its core, MIND introduces a multi-scale intent diffusion mechanism, where a holistic intent predictor captures global behavioral dynamics to guide overall behavior synthesis, while an immediate intent predictor provides step-wise, fine-grained signals for local behavior refinement at each diffusion step. This hierarchical intent formulation imposes a structured inductive bias for humanoid control, improving semantic alignment and behavioral naturalness. Furthermore, MIND encodes humanoid states into a latent space to enable more effective semantic intent modeling. Extensive experiments demonstrate that MIND outperforms existing methods and synthesizes coherent, physically plausible, and semantically aligned humanoid behaviors from text commands. Our code will be released to facilitate future research. Project page: https://binlee26.github.io/MIND_page. 

#### CCS Concepts: • **Computing methodologies** → **Physical simulation** . 

Additional Key Words and Phrases: character animation, imitation learning, diffusion policy, language commands 

2 • Bin Li, Ruichi Zhang, Han Liang, Jingyan Zhang, Juze Zhang, Xin Chen, and Jingya Wang 

### 1 Introduction 

Generating controllable, natural, and physically plausible humanoid behaviors is a long-standing goal in character animation, games, embodied simulation, and robotics. Early works [Luo et al. 2023a,b, 2021; Peng et al. 2018, 2022, 2021] primarily adopt a tracking-based paradigm, where goal-conditioned reinforcement learning (RL) [Liu et al. 2022] policies are trained to imitate reference motion trajectories. While effective, these approaches require high-quality kinematic motion data as control signals, whose acquisition is usually expensive and labor-intensive. In contrast, textual commands provide a more intuitive, flexible, and user-friendly interface for specifying humanoid behaviors, without requiring motion references or any additional predefined control signals [Tessler et al. 2024]. However, due to the substantial modality gap between textual commands and humanoid behaviors, achieving semantically aligned and physically realistic behavioral control, as shown in Fig. 1, remains a non-trivial task. 

Recent works [Bao et al. 2026; Li et al. 2025a; Tevet et al. 2024; Xie et al. 2026; Yuan et al. 2023] attempt to handle this problem through a generation-tracking paradigm, which combines a kinematic motion planner with an RL-based tracking policy. Although these approaches achieve competitive performance, the inherent domain shift between kinematic planners and physics-based trackers makes it difficult for the tracking policy to faithfully reproduce the planned motions. While task-specific fine-tuning [Tevet et al. 2024] has been shown to partially alleviate this discrepancy, it cannot be fully eliminated. To address this limitation, another line of work [Liao et al. 2025; Truong et al. 2024; Wang et al. 2025a; Wu et al. 2025] employs diffusion-based imitation policies [Chi et al. 2025] to directly generate actions conditioned on textual commands in an end-to-end manner, thereby circumventing the issue of domain shift. Nevertheless, these existing end-to-end approaches still suffer from suboptimal text-action alignment, largely due to the absence of an effective intermediate representation for bridging the substantial modality gap between text commands and low-level motor actions. 

Notably, compared with low-level motor actions, textual semantics are more naturally manifested in humanoid states. Specifically, humanoid states inherently encode rich dynamic information of body movements, including joint configurations, motion tendencies, and temporal evolution, which collectively provide a concrete characterization of the underlying behavioral semantics. In contrast, actions mainly function as low-level motor control signals for physical actuation, with limited capacity to convey high-level behavioral semantics. Based on this, we argue that humanoid states can serve as a semantic basis for behavior modeling, where the encoded dynamic information acts as a bridge between textual commands and actions, mitigating the substantial modality gap. In this work, we refer to the dynamic information embedded in humanoid states that corresponds to underlying behavioral patterns as intent. 

Building upon this insight, we propose MIND, a novel end-to-end framework for text-driven physics-based humanoid control that explicitly predicts intent as an effective semantic guidance signal. The core of MIND is a multi-scale intent mechanism that models humanoid intent at different temporal granularities within a unified diffusion framework. Specifically, a holistic intent predictor (HIP) 


Fig. 2. **Framework overview.** Given text commands and humanoid states, MIND models humanoid intent at multiple temporal scales under a within diffusion framework. Specifically, the Holistic Intent Predictor (HIP) captures global behavioral dynamics to provide high-level planning guidance, while the Immediate Intent Predictor (IIP) models step-wise intent from current states for fine-grained action refinement. The predicted holistic and immediate intents, together with the textual commands, are jointly used to condition the Action Diffusion Transformer (ADiT), guiding autoregressive (AR) action generation. Dashed lines indicate components that are used only during training. 

is designed to capture overall behavioral dynamics for global planning, while an immediate intent predictor (IIP) models step-wise intent to provide fine-grained guidance for action refinement. By seamlessly integrating this hierarchical intent structure into the action diffusion transformer (ADiT), MIND effectively combines holistic planning with immediate refinement, substantially improving semantic alignment and behavioral naturalness. Furthermore, MIND encodes humanoid states into a compact latent space to obtain more structured intent representations, thereby enhancing the semantic expressiveness of the predicted intents and further improving text-action alignment. Extensive experiments demonstrate that MIND consistently outperforms several strong baselines, achieving semantically aligned and physically plausible humanoid behavior synthesis. 

To summarize, our contributions are threefold: 

- We propose MIND, a novel end-to-end framework for textdriven physics-based humanoid control, which explicitly models intent as effective semantic guidance for humanoid behavior synthesis within a unified diffusion framework. 

- We introduce a multi-scale intent mechanism that operates in a latent space and captures intent at multiple temporal granularities, enabling structured modeling of semantic dynamics. 

- Extensive experiments demonstrate the superiority of MIND over competitive baselines, and comprehensive ablation studies validate the effectiveness of each individual design. 

MIND: Multi-Scale Intent Diffusion for Text-Driven Physics-Based Humanoid Control • 3 

### 2 Related Work 

_Physics-Based Humanoid Control._ Early works on physics-based humanoid control [Peng et al. 2018] primarily focused on tracking single motion trajectories. Subsequent approaches [Dou et al. 2023; Peng et al. 2022, 2021; Serifi et al. 2024; Tessler et al. 2023] extended to limited-scale motion datasets, leveraging adversarial imitation learning to produce diverse and natural behaviors. Later, methods such as UHC [Luo et al. 2021], PHC [Luo et al. 2023a], and PULSE [Luo et al. 2023b] achieved impressive performance on the large-scale AMASS [Mahmood et al. 2019] dataset. MaskedMimic [Tessler et al. 2024] learns a versatile physics-based controller through motion inpainting. However, these approaches rely on reference motion trajectories or predefined control signals, which are often costly to acquire in practice. In contrast, textual commands provide a more accessible and user-friendly interface for behavior specification. More recent methods [Huang et al. 2025; Mu et al. 2025; Wang et al. 2025b; Xu et al. 2025; Zhang et al. 2025a] have demonstrated promising progress, but still struggle to achieve robust text-driven control. 

_Text-Driven Behavior Synthesis._ In recent years, a large body of work has explored text-conditioned behavior synthesis for humanoid control. A dominant line of approaches focuses on kinematic motion modeling [Chen et al. 2025, 2023; Guo et al. 2025; He et al. 2025; Jiang et al. 2023; Li et al. 2026; Tevet et al. 2022; Yu et al. 2026; Zhang et al. 2024, 2023; Zhu et al. 2025]. MotionGPT [Jiang et al. 2023] discretizes motion sequences into token indices via VQVAE [Van Den Oord et al. 2017], enabling motion generation with large language models. Molingo [He et al. 2025] and CMDM [Yu et al. 2026] improve text-motion alignment by learning a semantically structured latent space. Despite their effectiveness in text-driven kinematic motion generation, these methods largely ignore physical constraints and dynamic consistency, often resulting in physically implausible artifacts such as penetration and floating. For physicsbased behavior control, existing methods can be broadly categorized into two paradigms. One is the kinematic-tracking pipeline [Tevet et al. 2024; Yuan et al. 2023], which inevitably suffers from domain shift between kinematic generation and physics-based tracking control. The other is based on imitation learning, including PADL [Juravsky et al. 2022], SuperPADL [Juravsky et al. 2024], PDP [Truong et al. 2024], UniPhys [Wu et al. 2025], Beyondmimic [Liao et al. 2025], and InterAgent [Li et al. 2025c], which learn from expert knowledge conditioned on text. While these approaches can mitigate the domain shift issue, they introduce a new bottleneck in bridging the substantial modality gap between high-level textual commands and low-level motor actions, hindering effective control. 

_Diffusion Policies for Humanoid Control._ Recent advances in diffusion models [Ho and Salimans 2022; Lukoianov et al. 2024; Nichol and Dhariwal 2021; Peebles and Xie 2023; Song et al. 2020] have established them as a powerful paradigm for control [Li et al. 2024; Wolf et al. 2025], owing to their powerful generative capability, effective modeling of multi-modal distributions, and flexible conditioning mechanisms. Diffusion Policies [Chi et al. 2025; Wang et al. 2024; Zhang et al. 2025b] demonstrate the effectiveness of diffusion models in manipulation tasks, achieving strong performance in learning complex action distributions from demonstrations. Building upon 

this line of research, PDP [Truong et al. 2024] extends diffusion policies to physics-based humanoid control, validating its effectiveness in motion tracking and perturbation recovery. More recently, several works [Huang et al. 2025; Li et al. 2025c; Liao et al. 2025; Wu et al. 2025] have explored the joint modeling of states and actions within a single generative framework, enabling flexible task-specific control and facilitating a wide range of downstream applications. However, we argue that such formulations hinder text-to-behavior alignment. By conditioning on state-action pairs rather than actions alone, these methods require jointly modeling text-to-state and textto-action correspondences, which introduces interference between states and actions representations. This leads to entangled optimization objectives, thereby weakening text-to-action alignment. 

### 3 Preliminaries 

_Physics Simulation Setup._ We simulate a physics-based character with an SMPL-like [Loper et al. 2023] skeleton in the Isaac Gym [Liang et al. 2018]. The humanoid comprises 24 joints and 69 actuators, each driven by a proportional-derivative (PD) controller. At each time step, the policy outputs an action _𝒂𝑡_ ∈ R<sup>69</sup> , which specifies the target joint positions for all actuators. Given the current state _𝒔𝑡_ ∈ R<sup>358</sup> , the simulator advances the system to the next state _𝒔𝑡_ +1 according to the dynamic transition _𝒔𝑡_ +1 ∼ _𝑝_ ( _𝒔𝑡_ +1 | _𝒔𝑡, 𝒂𝑡_ ). 

_Data Collection._ We track reference motions from the HumanML3D dataset [Guo et al. 2022] using the PHC tracking policy [Luo et al. 2023a] in a physics-based simulation environment. According to the success criteria defined in PHC [Luo et al. 2023a], only successfully tracked trajectories are collected, ensuring high-quality physically plausible expert demonstrations. Each retained trajectory is then paired with its corresponding text annotation, forming state-action-text triplets. The resulting datasets are subsequently used to train a diffusion policy via behavior cloning, enabling it to learn mappings from textual commands and humanoid states to corresponding actions. 

_Humanoid State Representation._ We define the humanoid state as _𝒔_ = ( _ℎ, 𝒑, 𝒓, 𝒗, 𝝎_ ), where _ℎ_ ∈ R denotes the height of the humanoid’s root joint above the ground plane. _𝒑_ ∈ R<sup>23×3</sup> represents the positions of all non-root joints in the humanoid root coordinate frame. _𝒓_ ∈ R<sup>24×6</sup> encodes the local orientations using a continuous 6D rotation representation. Additionally, _𝒗_ ∈ R<sup>24×3</sup> and _𝝎_ ∈ R<sup>24×3</sup> correspond to the local linear and angular velocities of each joint, respectively. The root joint is defined at the humanoid’s pelvis. 

### 4 Method 

### 4.1 Overview 

Our goal is to control a humanoid to perform natural, physically plausible behaviors that are consistent with the given textual commands. To this end, we propose MIND (Fig. 2), a novel end-to-end diffusion framework for text-driven physics-based humanoid control, which integrates multi-scale intent modeling into an action diffusion transformer (ADiT). To obtain compact intent representations, we first train a variational autoencoder (VAE) to encode the high-dimensional states into a latent space (section 4.2). Building upon this latent representation, we introduce a multi-scale intent 

4 • Bin Li, Ruichi Zhang, Han Liang, Jingyan Zhang, Juze Zhang, Xin Chen, and Jingya Wang 

Table 1. **Quantitative comparison of text-driven physics-based humanoid control** on the HumanML3D [Guo et al. 2022] test set, where ± indicates 95% confidence interval and →/↑/↓ means the closer / larger / smaller the better. **Bold** and underline indicate the best and second-best results, respectively. Phys-GT refers to the physics-based trajectories that are tracked from the MoCap dataset. 

||Top 1|R-precision↑<br>Top 2|Top 3|FID↓|MM Dist↓|Diversity→|MModality↑|
|---|---|---|---|---|---|---|---|
|Phys-GT|0_._5590<sup>±0</sup><sup>_._0031</sup>|0_._7442<sup>±0</sup><sup>_._0027</sup>|0_._8259<sup>±0</sup><sup>_._0023</sup>|0_._0001<sup>±0</sup><sup>_._000</sup>|1_._2839<sup>±0</sup><sup>_._0005</sup>|1_._2355<sup>±0</sup><sup>_._0083</sup>|-|
|PDP [Truong et al. 2024]<br>CLoSD [Tevet et al. 2024]<br>UniPhys [Wu et al. 2025]|0_._0324<sup>±0</sup><sup>_._0013</sup><br>0_._1717<sup>±0</sup><sup>_._0018</sup><br>0_._0865<sup>±0</sup><sup>_._0019</sup>|0_._0646<sup>±0</sup><sup>_._0011</sup><br>0_._2723<sup>±0</sup><sup>_._0017</sup><br>0_._1490<sup>±0</sup><sup>_._0020</sup>|0_._0967<sup>±0</sup><sup>_._0025</sup><br>0_._3468<sup>±0</sup><sup>_._0026</sup><br>0_._2053<sup>±0</sup><sup>_._0029</sup>|1_._6199<sup>±0</sup><sup>_._0146</sup><br>1_._5416<sup>±0</sup><sup>_._0044</sup><br>0_._6028<sup>±0</sup><sup>_._0068</sup>|2_._4715<sup>±0</sup><sup>_._0027</sup><br>2_._0941<sup>±0</sup><sup>_._0021</sup><br>2_._2846<sup>±0</sup><sup>_._0025</sup>|0_._9713<sup>±0</sup><sup>_._0091</sup><br>0_._9806<sup>±0</sup><sup>_._0074</sup><br>1_._1524<sup>±0</sup><sup>_._0064</sup>|1_._8902<sup>±0</sup><sup>_._0013</sup><br>0_._3727<sup>±0</sup><sup>_._0537</sup><br>1_._7484<br>±0_._0010|
|Kimodo++ [Rempe et al. 2026]|0_._3860<br>±0_._0046|0_._5591<br>±0_._0060|0_._6617<br>±0_._0054|0_._2680<br>±0_._0043|1_._6086<br>±0_._0022|1_._2047<br>±0_._0086|1_._1847<sup>±0</sup><sup>_._0025</sup>|
|MIND (Ours)|0_._4679<sup>±0</sup><sup>_._0032</sup>|0_._6374<sup>±0</sup><sup>_._0054</sup>|0_._7299<sup>±0</sup><sup>_._0042</sup>|0_._1184<sup>±0</sup><sup>_._0009</sup>|1_._4576<sup>±0</sup><sup>_._0039</sup>|1_._2278<sup>±0</sup><sup>_._0073</sup>|0_._9864<sup>±0</sup><sup>_._007</sup>|


mechanism (Fig. 3) that models behavioral intent at different temporal granularities (section 4.3). Specifically, a holistic intent predictor (HIP) captures global and long-horizon intent, while an immediate intent predictor (IIP) provides fine-grained, step-wise intent. Both HIP and IIP are jointly trained with the action diffusion transformer within a unified framework. This formulation enables the generation of actions that are coherent, physically grounded, and aligned with the underlying intent. 

### 4.2 Intent Variational Autoencoder 

To capture the underlying intent embedded in humanoid state to facilitate subsequent learning, in practice, we employ a 1D causal convolutional architecture [Xiao et al. 2025] to construct a temporal encoder-decoder that maps raw state sequences into a compact latent space. The use of causal convolutions preserves temporal causality, making the learned latent representation more suitable for sequential behavior modeling. Given a state clip _𝑆_ ∈ R<sup>_𝑁_×</sup><sup>_𝑑_</sup> , the encoder E produces a sequence of latent vectors _𝐼_ ∈ R<sup>_𝑙_×</sup><sup>_𝑑𝑙_</sup> , which is then decoded by D to reconstruct the raw state sequence _𝑆_<sup>ˆ</sup> = D( _𝐼_ ). We use the same loss function as _𝜎_ -VAE [Rybkin et al. 2021] to optimize the intent VAE. The full loss function is defined as: 


where L _𝑟𝑒𝑐_ = || _𝑆_ − _𝑆_<sup>ˆ</sup> ||<sup>2</sup> 2<sup>denotes the standard VAE reconstruction</sup> loss and L _𝐾𝐿_ = _𝐷𝐾𝐿_ ( _𝑞_ ( _𝐼_ | _𝑆_ )|| _𝑝_ ( _𝐼_ )) is the KL divergence. _𝜆𝐾𝐿_ is the balancing hyperparameter. This formulation induces a compact and temporally coherent latent space that reduces redundancy and noise inherent in the raw state representations, thereby facilitating more effective intent modeling. Once training is completed, the VAE is fixed, and only the encoder E is retained to extract intent representations for the subsequent stage. 

### 4.3 Multi-Scale Intent Mechanism 

To achieve semantically grounded and intent-aware humanoid control, we propose a multi-scale intent mechanism that consists of two components: the HIP and IIP. Given textual commands, the HIP predicts global intent representations _𝐼𝐻_<sup>˜</sup> that serve as shared global contextual guidance for both the IIP and ADiT. Guided by the commands, the history intent, and the predicted global intent from HIP, the IIP generates step-wise intents at a finer temporal scale. Finally, 

the ADiT generates physically plausible and text-aligned behaviors conditioned on the resulting multi-scale intent representation. 

_Holistic Intent Predictor._ As mentioned above, the HIP provides high-level holistic guidance for humanoid command execution. Given a full state sequence _𝑆𝐻_ = ( _𝑠_ 1 _,𝑠_ 2 _, ...,𝑠𝑛_ ) ∈ R<sup>_𝑛_×358</sup> , we encode it into a compact latent representation using the frozen VAE encoder E, yielding holistic intent _𝐼𝐻_ = E( _𝑆𝐻_ ) ∈ R<sup>_𝑙𝐻_×</sup><sup>_𝑑𝑙_</sup> . As illustrated in Fig. 3, we train a diffusion model M _𝐻_ to generate holistic intent conditioned on textual input. Specifically, the model predicts the denoised holistic intent sequence as M _𝐻_ ( _𝐼𝐻_<sup>_𝑘,𝑘,𝑐_), where</sup><sup>_𝐼_</sup> _𝐻_<sup>_𝑘_is a</sup> holistic intent sequence with added Gaussian noise, _𝑘_ is the diffusion step, and _𝑐_ represents the text conditioning tokens. The training loss is given by: 


where _𝐼𝐻_<sup>0=</sup><sup>_𝐼𝐻_is the clean holistic intent sequence.</sup> 

_Immediate Intent Predictor._ Relying solely on coarse-grained holistic intent to guide action generation may compromise fine-grained control over the underlying dynamics. As the global holistic intent remains temporally invariant, it does not specify which components are relevant at each timestep, resulting in ambiguous credit assignment and blurry supervision. To address this limitation, we introduce an immediate intent predictor that provides step-wise, fine-grained guidance. As illustrated in Fig. 3, at timestep _𝑡_ , we define a history state sequence _𝑆ℎ_ = ( _𝑠𝑡_ − _ℎ, ...,𝑠𝑡_ ) and a short-horizon future state sequence _𝑆𝐼_ = ( _𝑠𝑡_ +1 _, ...,𝑠𝑡_ + _𝐿_ ). The corresponding immediate intent is obtained as _𝐼𝐼_ = E( _𝑆𝐼_ ). We encode _𝑆ℎ_ into _𝐼ℎ_ = E( _𝑆ℎ_ ), and train an autoregressive diffusion model M _𝐼_ to predict _𝐼𝐼_ conditioned on text tokens _𝑐_ , _𝐼ℎ_ , and _𝐼𝐻_<sup>˜</sup> . The training loss of IIP is defined as: 


where _𝐼𝐼_<sup>_𝑘_is an immediate intent sequence clip with added Gaussian</sup> noise, _𝑘_ is the diffusion step, _𝐼𝐼_<sup>0=</sup><sup>_𝐼𝐼_is the clean immediate intent</sup> sequence clip. In practice, _𝐼𝐻_<sup>˜</sup> is instantiated as the final-layer hidden representation of the HIP. 

MIND: Multi-Scale Intent Diffusion for Text-Driven Physics-Based Humanoid Control • 5 


Fig. 3. **Multi-scale intent mechanism.** Given a textual command, a frozen CLIP text encoder with a lightweight text adapter first extracts semantic representations, which are then simultaneously injected into two complementary branches via cross-attention: a Holistic Intent Predictor for capturing global, sequence-level intent, and an Immediate Intent Predictor for modeling fine-grained, step-wise dynamics. Meanwhile, a pretrained VAE encoder is employed to encode the states into a compact latent space to capture the underlying intent. The light pink lines indicate processes related to HIP, while the light blue lines correspond to those related to IIP. 

Table 2. **Ablation study on the effect of each design choice.** 

|AdaLN|CrossAttn|IIP|HIP|VAE|R-<br>Top 1|precision <br>Top 2|↑<br>Top 3|FID↓|
|---|---|---|---|---|---|---|---|---|
|✓|||||0.1735|0.2827|0.3608|0.7513|
||✓||||0.3155|0.4645|0.5530|0.3632|
||✓|✓|||0.3233|0.4813|0.5759|0.3314|
||✓|✓||✓|0_._3601|0_._5174|0_._6084|0_._2007|
||✓||✓|✓|0.2917|0.4372|0.5273|0.5362|
||✓|✓|✓|✓|0_._4679|0_._6374|0_._7299|0_._1184|


### 4.4 Multi-Scale Intent Informed Diffusion Policy 

Based on the HIP and IIP, we leverage the multi-scale intent to jointly inform action generation. The holistic intent captures longhorizon planning, while the immediate intent provides step-wise refinement. This hierarchical formulation enables a comprehensive modeling of humanoid behavioral dynamics, facilitating more precise and temporally consistent control. As shown in Fig. 2, ADiT adopts the diffusion transformer (DiT) [Peebles and Xie 2023] as its backbone. Text tokens, along with the holistic intent and immediate intent representations, are incorporated via cross attention to inform action synthesis. Formally, given the history state _𝑆ℎ_ , we train an autoregressive DiT M _𝐴_ to generate actions conditioned on text and multi-scale intent. The training loss of ADiT is formulated as: 


where _𝑎_<sup>_𝑘_</sup> denotes the noisy action at diffusion step _𝑘_ , _𝑎_<sup>0</sup> is the clean action sequence, _𝐼𝐻_<sup>˜</sup> and _𝐼_<sup>˜</sup> _𝐼_ denote the final-layer hidden representations from the HIP and the IIP, respectively. In contrast to intent modeling, the ADiT directly operates on state history sequence _𝑆ℎ_ without latent projection. This design choice preserves fidelity of humanoid states, enabling accurate perception of the current behavioral dynamics essential for physically grounded control. 

Table 3. **Quantitative evaluation of physical correctness.** Following [Tevet et al. 2024; Wu et al. 2025; Yuan et al. 2023], we report footfloating to assess the physical plausibility and motion jerk to evaluate the smoothness. 

||Floating [mm] ↓|Jerk [mm/frame<sup>3</sup>] ↓|
|---|---|---|
|Phys-GT|15.5840|2_._7172×10<sup>−3</sup>|
|PDP [Truong et al. 2024]|24.8511|6_._5476×10<sup>−3</sup>|
|CLoSD [Tevet et al. 2024]|19.2958|12_._0022×10<sup>−3</sup>|
|UniPhys [Wu et al. 2025]|20.4853|3_._6054×10<sup>−3</sup>|
|Kimodo++ [Rempe et al. 2026]|33.7176|10_._2709×10<sup>−3</sup>|
|MIND (Ours)|17_._1173|2_._5966×10<sup>−3</sup>|


_Training and Inference._ During training, all components, including the HIP, IIP, and ADiT, are jointly optimized in an end-to-end manner, as illustrated in Fig. 2: 


This unified training paradigm promotes consistent representation learning across intent and action spaces, facilitates information flow across temporal scales, and enables mutual refinement between high-level intent planning and low-level motor action generation. 

For inference, as shown in Fig. 2, the model continuously receives states from the simulator and stores them in a first-in-first-out history buffer. Given the textual command, the HIP generates the corresponding holistic intent to provide global behavioral guidance. In parallel, the IIP first encodes the history states stored in the buffer into a compact latent space, and then predicts the corresponding immediate intent conditioned on both the history latent representations and the textual tokens. ADiT jointly takes the predicted holistic intent, immediate intent and the given command as conditions to generate the corresponding actions. The predicted actions are then executed to drive the humanoid, repeated autoregressively for the desired steps. 

### 5 Experiments 

### 5.1 Experiment Setup 

_Dataset and evaluation metrics._ We evaluate our model on the HumanML3D [Guo et al. 2022] dataset, a large-scale human motion capture dataset with fine-grained textual annotations, where the vast majority of motions are sourced from the AMASS dataset [Mahmood et al. 2019]. We follow the standard evaluation protocol commonly used in text-to-motion literature, which includes five metrics: (1) _R-Precision_ evaluates text-motion consistency by measuring motion-to-text retrieval accuracy. (2) _Fréchet Inception Distance (FID)_ measures the distributional discrepancy between generated motions and ground truth. (3) _Multimodal Distance (MM Dist)_ assesses the alignment between text and its corresponding motion in the shared latent space. (4) _Diversity_ quantifies the variability across different generated sequences. (5) _Multimodality (MModality)_ evaluates the variation among motions generated from the same textual input. To compute these metrics, we train a behavior encoder and a text encoder using a contrastive learning objective, which maps paired text-state samples to a shared latent space. Following PhysDiff [Yuan et al. 2023], CLoSD [Tevet et al. 2024] and UniPhys [Wu 

6 • Bin Li, Ruichi Zhang, Han Liang, Jingyan Zhang, Juze Zhang, Xin Chen, and Jingya Wang 


Fig. 4. **Qualitative comparison.** Our MIND generates coherent and natural humanoid behaviors with stronger alignment to textual inputs, outperforming all existing baselines. 

et al. 2025], we further evaluate the physical plausibility of the generated motions using foot-floating and jerk, which measure stability and smoothness, respectively. We do not report foot skating or penetration, as they are negligible across all physics-based methods. For a fair comparison, all methods (except Kimodo++) are initialized from a standardized neutral standing pose during evaluation. 

### 5.2 Comparison 

We compare our method against four baselines. PDP [Truong et al. 2024] and UniPhys [Wu et al. 2025] directly generate actions conditioned solely on textual inputs in an end-to-end manner. CLoSD [Tevet et al. 2024] employs a diffusion-based planner followed by an RLbased tracking controller to execute the planned kinematic motions. Kimodo++ first synthesizes kinematic trajectories from textual commands using Kimodo [Rempe et al. 2026], and then employs the PHC+ [Luo et al. 2023b] tracking policy, which achieves nearly 100% success rate on AMASS [Mahmood et al. 2019], to obtain physically plausible motions. 


Fig. 5. **Qualitative ablation study.** We qualitatively evaluate the effect of each component of our proposed MIND. In each subfigure, bold black text in parentheses indicates the corresponding row index in Tab.2 

_Quantitative Results._ As shown in Tab. 1, our proposed MIND achieves consistently strong performance across most evaluation metrics, demonstrating a favorable balance between semantic alignment, behavior quality, and diversity. Notably, while MIND lags behind PDP [Truong et al. 2024] and UniPhys [Wu et al. 2025] on the MModality metric, this is primarily because these end-to-end methods suffer from weak text conditioning, leading to nearly random generation, which significantly increases variability without meaningful semantic control. For physical evaluation metrics, shown in Tab. 3, MIND outperforms all baseline methods, achieving the lowest floating error and even surpassing Phys-GT in jerk. Notably, even though Kimodo [Rempe et al. 2026] is trained on large-scale datasets and coupled with the strong RL-based tracker, its performance remains suboptimal. We also observe that methods based on the kinematic–tracking paradigm consistently exhibit higher jerk score than the end-to-end methods. This may be attributed to the domain shift introduced by the kinematic-tracking paradigm, where kinematic generation and tracking are decoupled and optimized independently, as also noted in prior works [Huang et al. 2025; Wu et al. 2025]. This evidence further substantiates the superiority of our framework, which jointly models intent and action in a unified formulation, effectively eliminating such mismatch. 

_Qualitative Results._ As shown in Fig. 4, PDP [Truong et al. 2024], UniPhys [Wu et al. 2025], and CLoSD [Tevet et al. 2024] exhibit poor text-behavior alignment, with the generated behaviors often failing to correspond to the input textual commands. Kimodo++, benefiting from the powerful kinematic motion generation capability of Kimodo [Rempe et al. 2026], can only roughly produce the expected actions, yet still suffers from noticeably unnatural behaviors 

MIND: Multi-Scale Intent Diffusion for Text-Driven Physics-Based Humanoid Control • 7 

Table 4. **Ablation study on physics-based metrics.** 

|AdaLN|CrossAttn|IIP|HIP|VAE|Floating [mm] ↓|Jerk [mm/frame<sup>3</sup>] ↓|
|---|---|---|---|---|---|---|
|✓|||||20.8682|3_._8597×10<sup>−3</sup>|
||✓||||20.1482|3_._3839×10<sup>−3</sup>|
||✓|✓|||19.3830|2_._8497×10<sup>−3</sup>|
||✓|✓||✓|17_._4492|2_._6982×10<sup>−3</sup>|
||✓||✓|✓|21.5535|4_._3387×10<sup>−3</sup>|
||✓|✓|✓|✓|17_._1173|2_._5966×10<sup>−3</sup>|


Fig. 6. **Behavioral diversity under the same textual command.** Given an identical text prompt, MIND is able to generate diverse humanoid behaviors that are all semantically consistent while exhibiting different motion patterns and dynamics. 

and incomplete semantic execution. For example, in the first generated case of Kimodo++, the model fails to perform the “raise right hand” behavior, while in the second case, the generated “petting” behavior appears particularly rigid and unnatural. In contrast, our method is able to generate highly vivid, semantically aligned and physically consistent humanoid behaviors, demonstrating that our multi-scale intent framework enables effective and robust guidance for humanoid command execution. Moreover, as shown in Fig. 6, given identical textual commands, our proposed MIND is capable of generating diverse behavior patterns. For instance, for the concept of "waving goodbye" , both one-hand waving and two-hand waving are valid behavioral realizations, indicating that our method not only achieves strong semantic alignment but also captures rich and semantically grounded behavioral multimodality. 

### 5.3 Ablation Study 

_Effect of Text Condition Mechanism._ We first investigate the impact of two text conditioning mechanisms, global token adaptive layer normalization [Peebles and Xie 2023] and multi-token cross attention, as shown in the first two rows of Tab. 2. It is observed that multi-token cross attention significantly outperforms the single global token adaptive layer normalization. This improvement likely stems from the richer and more expressive semantic representations provided by multiple tokens, which enable more precise conditioning for action generation. This also suggests that the suboptimal text-semantic alignment observed in PDP [Truong et al. 2024] and UniPhys [Wu et al. 2025], which share the same end-toend paradigm as our proposed MIND, may be partly attributed to their reliance on single global token adaptive layer normalization for text conditioning, which limits the expressiveness of textual representations. 


Fig. 7. **Effect of latent dimension and temporal downsampling rate.** 

_Effect of Multi-scale Intent._ As shown in Tab. 2 and Fig. 5, row 1 (R1) and R3 demonstrate that the immediate intent predicted by the IIP effectively provides fine-grained guidance for action generation. R3 and R4 indicate that a more compact latent space facilitates better semantic intent modeling, leading to further performance gains. R4, R5 and R6 verify that our proposed multi-scale intent mechanism effectively integrates long-term planning with immediate expectations, substantially improving overall performance. Notably, comparing R2 and R5, it is observed that relying solely on holistic intent to guide action generation instead degrades performance. This may stem from its tendency to overemphasize global average structure while lacking sufficient temporal specificity, thereby undermining the fine-grained dynamics required at each timestep. Furthermore, as shown in Tab. 4, each part of the proposed multi-scale intent mechanism also consistently improves all physics-based metrics. In particular, the comparison between R2 and R3 demonstrates that incorporating the immediate intent contributes to alleviate both floating artifacts and motion jerkiness, highlighting the effectiveness of the IIP in refining motion dynamics. Meanwhile, R3 and R4 further suggest that modeling intent in a compact latent space can mitigate the negative impact of redundancy and noise inherent in raw state representations, leading to more stable and physically plausible behaviors. 

_Effect of Latent Size._ We conduct an exploration on both latent dimension and downsampling rate. As illustrated in the left panel of Fig. 7, a latent dimension of 32 achieves the best performance in terms of both R-Precision and FID. Increasing the dimension leads to slight degradation, while reducing it to 16 results in insufficient representational capacity and thus inferior performance. In the right panel, with the latent dimension fixed at 32, it is observed that a 1/4 downsampling rate significantly outperforms both 1/2 downsampling and no downsampling. Overall, these results suggest that a compact latent space facilitates improving semantic alignment between behavioral intent and textual commands, thereby enabling more semantically consistent action generation. 

### 6 Conclusions 

In this work, we presented MIND, a novel end-to-end diffusion framework for text-driven physics-based humanoid control. Unlike existing approaches that either suffer from the domain discrepancy between kinematic motion generation and physics-based tracking or struggle with the substantial modality gap between textual commands and low-level actions, our proposed MIND explicitly models 

8 • Bin Li, Ruichi Zhang, Han Liang, Jingyan Zhang, Juze Zhang, Xin Chen, and Jingya Wang 

behavioral intent as an intermediate semantic representation to bridge text and action under a unified diffusion framework. By introducing a multi-scale intent mechanism that captures humanoid intent at different temporal granularities, MIND combines holistic behavioral guidance with step-wise intent refinement for more semantically aligned and physically plausible behavior synthesis. Furthermore, by encoding humanoid states into a compact latent space, MIND obtains more structured intent representations, further enhancing semantic expressiveness and text-action alignment. Comprehensive quantitative and qualitative analysis demonstrates that our proposed MIND consistently outperforms all existing baselines in semantic alignment and physical realism. We believe this work can inspire future research on physics-based humanoid control and facilitate the development of more natural, controllable, and semantically aware physics-based character animation systems. 

### 7 Acknowledgement 

This project was supported by Shanghai Local College Capacity Building Program (23010503100), NSFC (No.62406195, W2431046, W2431046), Shanghai Frontiers Science Center of Human-centered Artificial Intelligence (ShangHAI), MoE Key Laboratory of Intelligent Perception and Human-Machine Collaboration (ShanghaiTech University), the Shanghai Frontiers Science Center of Human-centered Artificial Intelligence, HPC Platform and Core Facility Platform of Computer Science and Communication of ShanghaiTech University and Shanghai Engineering Research Center of Intelligent Vision and Imaging. 

### References 

- Jiacheng Bao, Haoran Yang, Yucheng Xin, Junhong Liu, Yuecheng Xu, Han Liang, Pengfei Han, Xiaoguang Ma, Dong Wang, and Bin Zhao. 2026. PhyGile: PhysicsPrefix Guided Motion Generation for Agile General Humanoid Motion Tracking. _arXiv preprint arXiv:2603.19305_ (2026). 

- Changan Chen, Juze Zhang, Shrinidhi K Lakshmikanth, Yusu Fang, Ruizhi Shao, Gordon Wetzstein, Li Fei-Fei, and Ehsan Adeli. 2025. The language of motion: Unifying verbal and non-verbal language of 3d human motion. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ . 6200–6211. 

- Xin Chen, Biao Jiang, Wen Liu, Zilong Huang, Bin Fu, Tao Chen, and Gang Yu. 2023. Executing your commands via motion diffusion in latent space. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . 18000–18010. 

- Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. 2025. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ 44, 10-11 (2025), 1684–1704. 

- Zhiyang Dou, Xuelin Chen, Qingnan Fan, Taku Komura, and Wenping Wang. 2023. C· ase: Learning conditional adversarial skill embeddings for physics-based characters. In _SIGGRAPH Asia 2023 Conference Papers_ . 1–11. 

- Chuan Guo, Inwoo Hwang, Jian Wang, and Bing Zhou. 2025. Snapmogen: Human motion generation from expressive texts. _arXiv preprint arXiv:2507.09122_ (2025). 

- Chuan Guo, Shihao Zou, Xinxin Zuo, Sen Wang, Wei Ji, Xingyu Li, and Li Cheng. 2022. Generating diverse and natural 3d human motions from text. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . 5152–5161. 

- Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. 2016. Deep residual learning for image recognition. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ . 770–778. 

- Yannan He, Garvita Tiwari, Xiaohan Zhang, Pankaj Bora, Tolga Birdal, Jan Eric Lenssen, and Gerard Pons-Moll. 2025. MoLingo: Motion-Language Alignment for Text-toMotion Generation. _arXiv preprint arXiv:2512.13840_ (2025). 

- Jonathan Ho and Tim Salimans. 2022. Classifier-free diffusion guidance. _arXiv preprint arXiv:2207.12598_ (2022). 

- Xiaoyu Huang, Takara Truong, Yunbo Zhang, Fangzhou Yu, Jean Pierre Sleiman, Jessica Hodgins, Koushil Sreenath, and Farbod Farshidian. 2025. Diffuse-cloc: Guided diffusion for physics-based character look-ahead control. _ACM Transactions on Graphics (TOG)_ 44, 4 (2025), 1–12. 

- Biao Jiang, Xin Chen, Wen Liu, Jingyi Yu, Gang Yu, and Tao Chen. 2023. Motiongpt: Human motion as a foreign language. _Advances in Neural Information Processing Systems_ 36 (2023), 20067–20079. 

- Jordan Juravsky, Yunrong Guo, Sanja Fidler, and Xue Bin Peng. 2022. Padl: Languagedirected physics-based character control. In _SIGGRAPH Asia 2022 Conference Papers_ . 1–9. 

- Jordan Juravsky, Yunrong Guo, Sanja Fidler, and Xue Bin Peng. 2024. Superpadl: Scaling language-directed physics-based control with progressive supervised distillation. In _ACM SIGGRAPH 2024 Conference Papers_ . 1–11. 

- Bin Li, Ruichi Zhang, Han Liang, Jingyan Zhang, Juze Zhang, Xin Chen, Lan Xu, Jingyi Yu, and Jingya Wang. 2025c. InterAgent: Physics-based Multi-agent Command Execution via Diffusion on Interaction Graphs. _arXiv preprint arXiv:2512.07410_ (2025). 

- Haoran Li, Yaocheng Zhang, Haowei Wen, Yuanheng Zhu, and Dongbin Zhao. 2024. Stabilizing diffusion model for robotic control with dynamic programming and transition feasibility. _IEEE Transactions on Artificial Intelligence_ 5, 9 (2024), 4585– 4594. 

- Yingyan Li, Lue Fan, Jiawei He, Yuqi Wang, Yuntao Chen, Zhaoxiang Zhang, and Tieniu Tan. 2025b. Enhancing end-to-end autonomous driving with latent world model. In _International Conference on Learning Representations_ , Vol. 2025. 42942–42959. 

- Zekun Li, Sizhe An, Chengcheng Tang, Chuan Guo, Ivan Shugurov, Linguang Zhang, Amy Zhao, Srinath Sridhar, Lingling Tao, and Abhay Mittal. 2026. Llamo: Scaling pretrained language models for unified motion understanding and generation with continuous autoregressive tokens. _arXiv preprint arXiv:2602.12370_ (2026). 

- Zhe Li, Cheng Chi, Yangyang Wei, Boan Zhu, Yibo Peng, Tao Huang, Pengwei Wang, Zhongyuan Wang, Shanghang Zhang, and Chang Xu. 2025a. From language to locomotion: Retargeting-free humanoid control via motion latent guidance. _arXiv preprint arXiv:2510.14952_ (2025). 

- Jacky Liang, Viktor Makoviychuk, Ankur Handa, Nuttapong Chentanez, Miles Macklin, and Dieter Fox. 2018. Gpu-accelerated robotic simulation for distributed reinforcement learning. In _Conference on Robot Learning_ . PMLR, 270–282. 

- Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C Karen Liu. 2025. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ (2025). 

- Minghuan Liu, Menghui Zhu, and Weinan Zhang. 2022. Goal-conditioned reinforcement learning: Problems and solutions. _arXiv preprint arXiv:2201.08299_ (2022). 

- Matthew Loper, Naureen Mahmood, Javier Romero, Gerard Pons-Moll, and Michael J Black. 2023. SMPL: A skinned multi-person linear model. In _Seminal Graphics Papers: Pushing the Boundaries, Volume 2_ . 851–866. 

- Artem Lukoianov, Haitz S de Ocáriz Borde, Kristjan Greenewald, Vitor C Guizilini, Timur Bagautdinov, Vincent Sitzmann, and Justin Solomon. 2024. Score distillation via reparametrized ddim. _Advances in Neural Information Processing Systems_ 37 (2024), 26011–26044. 

- Zhengyi Luo, Jinkun Cao, Kris Kitani, Weipeng Xu, et al. 2023a. Perpetual humanoid control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . 10895–10904. 

- Zhengyi Luo, Jinkun Cao, Josh Merel, Alexander Winkler, Jing Huang, Kris Kitani, and Weipeng Xu. 2023b. Universal humanoid motion representations for physics-based control. _arXiv preprint arXiv:2310.04582_ (2023). 

- Zhengyi Luo, Ryo Hachiuma, Ye Yuan, and Kris Kitani. 2021. Dynamics-regulated kinematic policy for egocentric pose estimation. _Advances in Neural Information Processing Systems_ 34 (2021), 25019–25032. 

- Naureen Mahmood, Nima Ghorbani, Nikolaus F Troje, Gerard Pons-Moll, and Michael J Black. 2019. AMASS: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ . 5442–5451. 

- Siyuan Mu and Sen Lin. 2025. A comprehensive survey of mixture-of-experts: Algorithms, theory, and applications. _arXiv preprint arXiv:2503.07137_ (2025). 

- Yuxuan Mu, Ziyu Zhang, Yi Shi, Minami Matsumoto, Kotaro Imamura, Guy Tevet, Chuan Guo, Michael Taylor, Chang Shu, Pengcheng Xi, et al. 2025. SMP: Reusable Score-Matching Motion Priors for Physics-Based Character Control. _arXiv preprint arXiv:2512.03028_ (2025). 

- Alexander Quinn Nichol and Prafulla Dhariwal. 2021. Improved denoising diffusion probabilistic models. In _International conference on machine learning_ . PMLR, 8162– 8171. 

- William Peebles and Saining Xie. 2023. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ . 4195–4205. 

- Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. 2018. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ 37, 4 (2018), 1–14. 

- Xue Bin Peng, Yunrong Guo, Lina Halper, Sergey Levine, and Sanja Fidler. 2022. Ase: Large-scale reusable adversarial skill embeddings for physically simulated characters. _ACM Transactions On Graphics (TOG)_ 41, 4 (2022), 1–17. 

- Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. 2021. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ 40, 4 (2021), 1–20. 

MIND: Multi-Scale Intent Diffusion for Text-Driven Physics-Based Humanoid Control • 9 

- Ethan Perez, Florian Strub, Harm De Vries, Vincent Dumoulin, and Aaron Courville. 2018. Film: Visual reasoning with a general conditioning layer. In _Proceedings of the AAAI conference on artificial intelligence_ , Vol. 32. 

- Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. 2021. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ . PmLR, 8748–8763. 

- Davis Rempe, Mathis Petrovich, Ye Yuan, Haotian Zhang, Xue Bin Peng, Yifeng Jiang, Tingwu Wang, Umar Iqbal, David Minor, Michael de Ruyter, et al. 2026. Kimodo: Scaling Controllable Human Motion Generation. _arXiv preprint arXiv:2603.15546_ (2026). 

- Oleh Rybkin, Kostas Daniilidis, and Sergey Levine. 2021. Simple and effective VAE training with calibrated decoders. In _International conference on machine learning_ . PMLR, 9179–9189. 

- Agon Serifi, Ruben Grandia, Espen Knoop, Markus Gross, and Moritz Bächer. 2024. Vmp: Versatile motion priors for robustly tracking motion on physical characters. In _Computer graphics forum_ , Vol. 43. Wiley Online Library, e15175. 

model. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . 364–373. Qinglun Zhang, Zhen Liu, Haoqiang Fan, Guanghui Liu, Bing Zeng, and Shuaicheng Liu. 2025b. Flowpolicy: Enabling fast and robust 3d flow-based policy via consistency flow matching for robot manipulation. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , Vol. 39. 14754–14762. Ziyu Zhang, Sergey Bashkirov, Dun Yang, Yi Shi, Michael Taylor, and Xue Bin Peng. 2025a. Physics-Based Motion Imitation with Adversarial Differential Discriminators. In _Proceedings of the SIGGRAPH Asia 2025 Conference Papers_ . 1–12. Yanqi Zhou, Tao Lei, Hanxiao Liu, Nan Du, Yanping Huang, Vincent Zhao, Andrew M Dai, Quoc V Le, James Laudon, et al. 2022. Mixture-of-experts with expert choice routing. _Advances in Neural Information Processing Systems_ 35 (2022), 7103–7114. Bingfan Zhu, Biao Jiang, Sunyi Wang, Shixiang Tang, Tao Chen, Linjie Luo, Youyi Zheng, and Xin Chen. 2025. Motiongpt3: Human motion as a second modality. _arXiv preprint arXiv:2506.24086_ (2025). 

- Jiaming Song, Chenlin Meng, and Stefano Ermon. 2020. Denoising diffusion implicit models. _arXiv preprint arXiv:2010.02502_ (2020). 

- Chen Tessler, Yunrong Guo, Ofir Nabati, Gal Chechik, and Xue Bin Peng. 2024. Maskedmimic: Unified physics-based character control through masked motion inpainting. _ACM Transactions On Graphics (TOG)_ 43, 6 (2024), 1–21. 

- Chen Tessler, Yoni Kasten, Yunrong Guo, Shie Mannor, Gal Chechik, and Xue Bin Peng. 2023. Calm: Conditional adversarial latent models for directable virtual characters. In _ACM SIGGRAPH 2023 conference proceedings_ . 1–9. 

- Guy Tevet, Sigal Raab, Setareh Cohan, Daniele Reda, Zhengyi Luo, Xue Bin Peng, Amit H Bermano, and Michiel van de Panne. 2024. Closd: Closing the loop between simulation and diffusion for multi-task character control. _arXiv preprint arXiv:2410.03441_ (2024). 

- Guy Tevet, Sigal Raab, Brian Gordon, Yonatan Shafir, Daniel Cohen-Or, and Amit H Bermano. 2022. Human motion diffusion model. _arXiv preprint arXiv:2209.14916_ (2022). 

- Takara Everest Truong, Michael Piseno, Zhaoming Xie, and Karen Liu. 2024. Pdp: Physics-based character animation via diffusion policy. In _SIGGRAPH Asia 2024 Conference Papers_ . 1–10. 

- Aaron Van Den Oord, Oriol Vinyals, et al. 2017. Neural discrete representation learning. _Advances in neural information processing systems_ 30 (2017). 

- Jiashun Wang, Yifeng Jiang, Haotian Zhang, Chen Tessler, Davis Rempe, Jessica Hodgins, and Xue Bin Peng. 2025b. Hil: Hybrid imitation learning of diverse parkour skills from videos. _arXiv preprint arXiv:2505.12619_ (2025). 

- Yuxuan Wang, Haobin Jiang, Shiqing Yao, Ziluo Ding, and Zongqing Lu. 2025a. Sentinel: A fully end-to-end language-action model for humanoid whole body control. _arXiv preprint arXiv:2511.19236_ (2025). 

- Zhendong Wang, Zhaoshuo Li, Ajay Mandlekar, Zhenjia Xu, Jiaojiao Fan, Yashraj Narang, Linxi Fan, Yuke Zhu, Yogesh Balaji, Mingyuan Zhou, et al. 2024. One-step diffusion policy: Fast visuomotor policies via diffusion distillation. _arXiv preprint arXiv:2410.21257_ (2024). 

- Rosa Wolf, Yitian Shi, Sheng Liu, and Rania Rayyes. 2025. Diffusion models for robotic manipulation: A survey. _Frontiers in Robotics and AI_ 12 (2025), 1606247. 

- Yan Wu, Korrawe Karunratanakul, Zhengyi Luo, and Siyu Tang. 2025. Uniphys: Unified planner and controller with diffusion for flexible physics-based character control. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . 13214– 13224. 

- Lixing Xiao, Shunlin Lu, Huaijin Pi, Ke Fan, Liang Pan, Yueer Zhou, Ziyong Feng, Xiaowei Zhou, Sida Peng, and Jingbo Wang. 2025. Motionstreamer: Streaming motion generation via diffusion-based autoregressive model in causal latent space. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . 10086– 10096. 

- Weiji Xie, Jiakun Zheng, Jinrui Han, Jiyuan Shi, Weinan Zhang, Chenjia Bai, and Xuelong Li. 2026. Textop: Real-time interactive text-driven humanoid robot motion generation and control. _arXiv preprint arXiv:2602.07439_ (2026). 

- Michael Xu, Yi Shi, KangKang Yin, and Xue Bin Peng. 2025. Parc: Physics-based augmentation with reinforcement learning for character controllers. In _Proceedings of the Special Interest Group on Computer Graphics and Interactive Techniques Conference Conference Papers_ . 1–11. 

- Qing Yu, Akihisa Watanabe, and Kent Fujiwara. 2026. Causal motion diffusion models for autoregressive motion generation. _arXiv preprint arXiv:2602.22594_ (2026). 

- Ye Yuan, Jiaming Song, Umar Iqbal, Arash Vahdat, and Jan Kautz. 2023. Physdiff: Physicsguided human motion diffusion model. In _Proceedings of the IEEE/CVF international conference on computer vision_ . 16010–16021. 

- Mingyuan Zhang, Zhongang Cai, Liang Pan, Fangzhou Hong, Xinying Guo, Lei Yang, and Ziwei Liu. 2024. Motiondiffuse: Text-driven human motion generation with diffusion model. _IEEE transactions on pattern analysis and machine intelligence_ 46, 6 (2024), 4115–4128. 

Mingyuan Zhang, Xinying Guo, Liang Pan, Zhongang Cai, Fangzhou Hong, Huirong Li, Lei Yang, and Ziwei Liu. 2023. Remodiffuse: Retrieval-augmented motion diffusion 

10 • Bin Li, Ruichi Zhang, Han Liang, Jingyan Zhang, Juze Zhang, Xin Chen, and Jingya Wang 

### A Additional Implementation Details 

In practice, the HIP, IIP, and ADiT are implemented with 6 DiT [Peebles and Xie 2023] blocks whose latent dimension is set to 768, and each attention layer consists of 8 heads. For the Intent VAE, both the encoder and decoder are based on 1D causal ResNet blocks [He et al. 2016], and the temporal downsampling rate and the latent dimension are set to 4 and 32, respectively. We set _𝜆𝐾𝐿_ = 1 × 10<sup>−5</sup> . For HIP, each full state sequence is uniformly downsampled to 16 frames before encoding into the latent space for computational efficiency. The horizon of immediate intent is set to _𝐿_ = 16, while the action prediction horizon is set to 4. The history state horizon is _ℎ_ = 16. To ensure consistent intent representations, HIP and IIP are formulated within a shared latent space. We use CLIP-ViT-L/14 [Radford et al. 2021] as the text encoder, and a two-layer transformer encoder as the text adapter. We further adopt classifier-free guidance [Ho and Salimans 2022] by randomly masking 10% of text tokens during training, and apply a guidance scale of 3.5 during diffusion sampling. All our models are trained for 80K iterations with batch size of 448 on 8 NVIDIA GeForce RTX 4090 GPUs, requiring approximately 12 hours in total. 

### B Failure Analysis of Existing End-to-End Baselines 

Although two-stage approaches generally suffer from performance degradation due to the domain shift issue discussed in the main paper, an important question remains: why PDP [Truong et al. 2024] and UniPhys [Wu et al. 2025], which both follow an end-to-end paradigm, exhibit particularly poor performance? As shown in the quantitative comparison Tab.1 of the main paper, the R-Precision of PDP is nearly indistinguishable from random generation (the evaluation batch size is 32). We further study the reasons behind this result. Specifically, we carefully examine the official implementation of PDP, which introduces textual conditioning through FiLM modulation [Perez et al. 2018]. However, we find that the textual conditioning is applied exclusively to the history state representation, without any explicit fusion of textual semantics into the action. As a result, the model is unable to effectively establish text-to-action controllability. For UniPhys, textual information is incorporated via adaptive layer norm [Peebles and Xie 2023]. However, it employs a shared transformer decoder to jointly model states and latent actions, which weakens the direct effect of textual semantics on actions and instead biases the model toward learning the mapping between text and the joint state-action representation. Since states and actions inherently exhibit a modality gap, their joint modeling inevitably introduces mutual interference, which further hinders fine-grained text-action alignment. 

### C Discussion 

_Limitations and failure cases._ Although the proposed framework achieves strong performance across most cases, several highly challenging behaviors remain difficult to execute robustly, as illustrated in Fig. 8. In particular, behaviors that require simultaneous multilimb coordination and precise balance control still present significant challenges for our method. For example, in the "crawling around" case on the left side of Fig. 8, our approach is initially able 


Fig. 8. **Failure cases.** Our method shows limitations in highly dynamic behaviors such as crawling. 

to generate behaviors that closely match the textual command. However, the humanoid gradually loses balance during crawling and eventually falls. Similarly, in the "reaches for their toes" case, the humanoid is required to sit on the ground while supporting the body with both hands and lifting one leg simultaneously, which introduces extremely unstable body configurations and often leads to failure. These failure cases suggest that a unified policy may still struggle to fully capture highly specialized balance strategies required by certain complex behaviors. One possible direction is to introduce expert-specialized modules, similar to a mixture-ofexperts (MoE) framework [Mu and Lin 2025; Zhou et al. 2022], where different experts focus on distinct categories of challenging motions such as crawling, balancing, or acrobatic behaviors. Another promising direction is to incorporate explicit contact-aware planning, balance constraints, or differentiable stability objectives into the policy learning process to improve robustness under complex dynamics. Furthermore, integrating a predictive world model [Li et al. 2025b] or a dedicated recovery mechanism [Luo et al. 2023a] may help the humanoid better handle instability in complex dynamic behaviors. 

_Discussion and future work._ Although MIND demonstrates strong capability in generating diverse, natural, physically plausible, and text-aligned humanoid behaviors, several future directions remain worth exploring. First, the current framework mainly focuses on short-to-medium horizon behavior generation, while modeling longhorizon behaviors with complex temporal dependencies remains challenging. Incorporating hierarchical memory mechanisms or world models may further improve long-term planning and behavioral consistency. Second, although MIND achieves promising semantic alignment between textual commands and generated behaviors, handling more compositional and fine-grained language instructions is still non-trivial. Future work could explore stronger large language model (LLM)-based semantic representations or multimodal reasoning mechanisms to improve semantic understanding and controllability. Furthermore, the diffusion model adopted in our framework inherently requires iterative denoising during inference, which limits runtime efficiency and increases computational overhead. Although our framework enables strong generative capability and stable behavior synthesis, it may hinder real-time deployment in latency-sensitive applications such as interactive control and robotics. Future work could explore model distillation and diffusion acceleration techniques to reduce inference cost while maintaining motion quality, semantic alignment, and physical realism. 

MIND: Multi-Scale Intent Diffusion for Text-Driven Physics-Based Humanoid Control • 11 


## **A person is walking forward and dancing at the same time.** 


**A person swings his left arm in a windmill fashion.** 

**A person is picking up something heavy with both hands.** 


Fig. 9. **Visual snapshots of text-driven humanoid behaviors via MIND.** (Part I). 

12 • Bin Li, Ruichi Zhang, Han Liang, Jingyan Zhang, Juze Zhang, Xin Chen, and Jingya Wang 

## **The person runs large strides and then begins to slow down.** 

## **A person jogs around in a counterclockwise circle.** 


**A person keeps shuffling steadily to their left side.** 

**A person walks forward, turn to their right, and walks back.** 


Fig. 10. **Visual snapshots of text-driven humanoid behaviors via MIND.** (Part II). 

