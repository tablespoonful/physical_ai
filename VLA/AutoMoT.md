---
title: "AutoMoT: A Unified Vision-Language-Action Model with Asynchronous Mixture-of-Transformers for End-to-End Autonomous Driving"
date: "2026-03-16"
authors: "Wenhui Huang; Songyan Zhang; Qihang Huang; Zhidong Wang; Zhiqi Mao; Collister Chua"
venue: "ICML 2026"
url: https://arxiv.org/abs/2603.14851
pdf: https://arxiv.org/pdf/2603.14851
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.14851)** / [論文ページ](https://arxiv.org/abs/2603.14851)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **AutoMoT: A Unified Vision-Language-Action Model with Asynchronous Mixture-of-Transformers for End-to-End Autonomous Driving** 

**Wenhui Huang**<sup>* 1 2</sup> **Songyan Zhang**<sup>* 1 3</sup> **Qihang Huang**<sup>* 1</sup> **Zhidong Wang**<sup>1</sup> **Zhiqi Mao**<sup>1</sup> **Collister Chua**<sup>1</sup> **Zhan Chen**<sup>1</sup> **Long Chen**<sup>3</sup> **Chen Lv**<sup>_†_1</sup> **AutoMoT Project Page** 

## **Abstract** 

Integrating vision-language models (VLMs) into end-to-end (E2E) autonomous driving (AD) systems has shown promise in improving scene understanding. However, existing integration strategies suffer from several limitations: they either struggle to resolve distribution misalignment between reasoning and action spaces, underexploit the general reasoning capabilities of pretrained VLMs, or incur substantial inference latency during action policy generation, which degrades driving performance. To address these challenges, we propose AutoMoT in this work, an end-toend AD framework that unifies reasoning and action generation within a single vision-languageaction (VLA) model. Our approach leverages a mixture-of-transformer (MoT) architecture with layer-wise joint attention sharing, which preserves the general reasoning capabilities of pre-trained VLMs while enabling efficient asynchronous inference over various tasks at different frequencies. Additionally, we explore a VLA-oriented action refiner that further enhances driving performance via diffusion-based fine-tuning. Extensive experiments on multiple benchmarks, under both open- and closed-loop settings, demonstrate that AutoMoT achieves state-of-the-art (SOTA) performance compared to existing methods. We further investigate the functional boundary of pre-trained VLMs in AD, examining when and to what extent AD-tailored fine-tuning is necessary. 

*Equal contribution 1Nanyang Technological University, Singapore<sup>2</sup> Harvard University, US<sup>3</sup> Xiaomi EV, China. Correspondence to: Chen Lv _<_ lyuchen@ntu.edu.sg _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 


_Figure 1._ Comparison of different paradigms for integrating VLMs into conventional end-to-end autonomous driving frameworks. Our AutoMoT framework unifies reasoning and action-policy learning within a single vision–language–action (VLA) model through layer-wise joint attention sharing, while enabling asynchronous inference across tasks with different execution frequencies. 

## **1. Introduction** 

The hierarchical modular pipeline, typically comprising perception, prediction, and planning, has been widely adopted in end-to-end (E2E) autonomous driving (AD) systems in recent years (Hu et al., 2023; Jiang et al., 2023; Liu et al., 2025a; Jaeger et al., 2023b; Liao et al., 2025). Recent advances in vision–language models (VLMs) have further benefited AD by enhancing high-level scene understanding, a capability that is often insufficient in conventional datadriven E2E systems when deployed in complex open-world scenarios. By leveraging their strong generalization and reasoning capabilities, VLMs endow AD systems with the potential to handle complex interactions and provide semantic explanations, thereby improving the interpretability. 

The integration of vision–language models (VLMs) with end-to-end (E2E) autonomous driving systems is under- 

1 

**AutoMoT: An Asynchronous VLA Model for E2E Autonomous Driving** 

going rapid development, giving rise to a diverse set of emerging design paradigms. A natural extension of the E2E framework incorporates VLMs into the upstream stages of the pipeline (Fu et al., 2025a; Li et al., 2025c), where pretrained models provide rich scene understanding to support downstream planning, as illustrated in Fig. 1(a). Another line of work adopts a dual-system architecture (Fig. 1(b)), in which the VLM operates as an auxiliary module that assists conventional E2E pipelines by supplying high-level conditioning signals (Jiang et al., 2025; Tian et al., 2025). However, these approaches suffer from inherent distributional misalignment between the reasoning space of VLMs and the action space of planners. Furthermore, fine-tuning VLMs to generate intermediate conditioning signals inevitably constrains them to task-specific roles, diminishing the general capabilities of pretrained models. 

More recently, as illustrated in Fig. 1c, emerging vision– language–action (VLA) architectures integrate reasoning and planning within a single pre-trained VLM backbone via autoregressive modeling (Wang et al., 2025; Zhou et al., 2026). While this unified design is compact and effectively leverages the strong reasoning capabilities of VLMs, tightly coupling action policy execution with high-level reasoning at a synchronized temporal frequency is impractical for real-world autonomous driving. This limitation becomes particularly severe in complex interactive environments, where low-latency control and rapid replanning are critical. Prior vision–language models that generate actions in textual form (Huang et al., 2026; Hwang et al., 2024; Zhang et al., 2024) can also be viewed as instances of this paradigm. In addition to the aforementioned limitations, these approaches rely on textual token supervision, which is inherently weaker than direct supervision on numerical action representations. Taking all these limitations into consideration, we pose the following key question: _How can VLA models fully leverage the generalist intelligence of a pre-trained VLM while mastering domain-specific capabilities and simultaneously satisfying real-time inference requirements?_ 

In this work, we propose **AutoMoT** , an end-to-end autonomous driving framework that seamlessly unifies asynchronous reasoning and action within a single vision– language–action (VLA) model, while avoiding both the degradation of VLM capabilities and distributional discrepancies across task spaces. As illustrated in Fig. 1d, AutoMoT adopts a mixture-of-transformers (MoT) architecture that bridges high-level reasoning (scene understanding) and low-level action policies (decision-making and trajectory planning) through joint attention in a shared latent space. This design enables asynchronous execution of textual reasoning and action generation at different temporal frequencies, thereby facilitating asynchronous inference. We comprehensively evaluate AutoMoT on both simulation 

and real-world benchmarks under closed-loop and openloop settings. Experimental results demonstrate competitive performance against state-of-the-art (SOTA) baselines, validating both the feasibility of the proposed framework and its effectiveness across diverse evaluation benchmarks. Moreover, through the comprehensive ablation studies, we found that pre-trained VLMs can achieve competitive multitask scene understanding performance through semantic prompting alone, while fine-tuning remains essential for action-level tasks such as decision-making and trajectory planning. 

The primary contributions of this work are as follows: 1) We propose AutoMoT, an end-to-end autonomous driving (AD) framework that seamlessly unifies scene understanding, decision-making, and planning within a single asynchronous VLA model via layer-wise joint attention sharing, while enabling asynchronous inference across tasks through different frequencies; 2) We investigate the functional boundaries of pretrained VLMs in autonomous driving, clarifying when and to what extent AD-specific finetuning is necessary across different tasks; 3) We explore a VLA-oriented action refiner that enhances driving performance through diffusion-based fine-tuning; 4) Extensive experiments demonstrate competitive performance against state-of-the-art baselines, validating both the feasibility of the proposed framework and its effectiveness across diverse evaluation benchmarks. 

## **2. Related Work** 

### **2.1. End-to-End Autonomous Driving** 

Planning-oriented methods have been widely adopted in end-to-end autonomous driving frameworks in recent years. For instance, UniAD (Hu et al., 2023) proposes a hierarchical modular architecture that enables multiple tasks to be jointly learned in an end-to-end manner, mitigating error accumulation and consequently improving planning performance. The VAD series (Jiang et al., 2023; Chen et al., 2024) follows this design while introducing vectorized scene representations, which simplify the overall architecture and improve inference efficiency. Subsequently, Para-Drive (Weng et al., 2024) extends the hierarchical paradigm to a fully parallel formulation by unifying multiple tasks within the bird’s-eye-view (BEV) space. More recently, diffusionbased policies (Chi et al., 2024) have attracted increasing attention in autonomous driving. Existing approaches typically apply diffusion models either as the core planner (Liao et al., 2025; Liu et al., 2025b) or as a trajectory refiner (Zhou et al., 2025a), leveraging their strong generative capabilities (Song et al., 2021; Ho et al., 2020) to improve driving performance. Nevertheless, these conventional end-to-end approaches still struggle with complex scene understanding, particularly when encountering long-tail and rare scenarios. 

2 

**AutoMoT: An Asynchronous VLA Model for E2E Autonomous Driving** 


_Figure 2._ As an end-to-end autonomous driving framework, AutoMoT unifies scene understanding, decision-making, and trajectory planning within a single VLA model. AutoMoT adopts a MoT architecture that connects the understanding expert and the action expert via layer-wise joint attention sharing, while enabling asynchronous inference at different frequencies through KV Caching. A VLA-oriented action refiner is further explored to enhance driving performance via diffusion-based refinement. 

### **2.2. Vision-Language Models for Autonomous Driving** 

The strong scene understanding and semantic reasoning capabilities of VLMs have motivated their rapid integration into E2E AD systems, resulting in several emerging design paradigms. Representative works such as Orion (Fu et al., 2025a) and ReCogDrive (Li et al., 2025c) introduce VLMs as upstream modules to enhance scene understanding and interpretability. Another line of work incorporates VLMs as secondary systems through intermediate representations, where DriveVLM (Tian et al., 2025) generates initial trajectory proposals, while Senna (Jiang et al., 2024) and ReCogDrive (Li et al., 2025c) provide high-level decisions to guide downstream planning. Vision–language–action (VLA) architectures, including AutoVLA (Zhou et al., 2025b), Simlingo (Renz et al., 2025), and Alpamayo-R1 (Wang et al., 2025), further unify multiple tasks within a single pretrained VLM backbone. However, the single-transformer design tightly couples reasoning and planning at a synchronized frequency, resulting in substantial inference latency, especially when chain-of-thought (CoT) reasoning is re- 

quired for complex scene understanding. In contrast, our MoT-based VLA architecture systematically unifies scene understanding, decision-making, and planning in a single model through joint attention sharing (Deng et al., 2025; Huang et al., 2025a), while remaining functionally decomposed. This design enables asynchronous inference at different frequencies, thereby alleviating latency bottlenecks. 

## **3. AutoMoT** 

### **3.1. Network Architecture** 

The overall framework of AutoMoT is illustrated in Fig. 2. AutoMoT comprises three core components: a scene understanding expert, an action expert, and an action refiner, all implemented using transformer-based architectures. In the following sections, we detail the design of each component as well as its corresponding training strategies. A detailed illustration of the data flow in AutoMoT is provided in Fig. 5 of Appendix A.1. 

3 

**AutoMoT: An Asynchronous VLA Model for E2E Autonomous Driving** 


_Figure 3._ Our mask coordinates understanding, decision-making, and planning within a unified attention space. It enables intra-task multi-modal aggregation and cross-task information flow while preserving task-level causal ordering. This hybrid design maintains hierarchical causality and supports rich contextual integration, enabling AutoMoT to achieve coherent multi-task reasoning, decision-making, and trajectory planning. 

**Understanding Expert** The primary role of the understanding expert (UE) in AutoMoT is to perform scene understanding and generate chain-of-thought (CoT) reasoning for complex scenarios, particularly long-tail and rare cases, while transferring its general knowledge to facilitate action policy learning. The UE adopts Qwen3-VL-4B dense model as its vision–language backbone, which takes as input multiview and multi-frame RGB images _I_<sup>_RGB_</sup> _∈_ R<sup>_N×H×W ×C_</sup> captured by onboard cameras, together with textual prompts _ℓ_ consisting of system prompts and user instructions, and outputs semantic reasoning results. To fully leverage the general knowledge of the pretrained Qwen3-VL model and avoid catastrophic degradation of reasoning performance, we freeze the understanding expert throughout the entire training process. The rationale behind this design is further investigated and discussed in Section 4.3. 

**Action Expert** The Action Expert (AE) in AutoMoT is responsible for decision-making and trajectory planning within the unified VLA framework. At each timestep _t_ , the AE takes the current observation _ot_ = _{It_<sup>_RGB_</sup> _, It_<sup>_BEV_</sup> _, Q_ ( _t_ ) _}_ as input and produces action-side latent representations. Here, _It_<sup>_BEV_</sup> denotes the LiDAR BEV feature and _Q_ ( _t_ ) represents the action queries. From these latent representations, the layer-wise query, key, and value embeddings _{Q_<sup>_l_</sup> ( _t_ ) _, K_<sup>˜</sup><sup>_l_</sup> ( _t_ ) _, V_<sup>˜</sup><sup>_l_</sup> ( _t_ ) _}_ are derived, where _l_ indexes the l-th attention layer. Based on these latent representations, the AE generates semantic decisions for the next three consecutive frames (semantic decisions for 

the next 3 seconds), along with temporal and spatial trajectory proposals over the same horizon. More specifically, given the current observation _ot_ and a set of action queries _Q_ ( _t_ ), the AE jointly produces latent representations for decision-making and trajectory planning. These representations are decoded into three outputs: (i) concrete meta-actions _Z_<sup>ˆ</sup> _t_ = _{z_ ˆ _t_ + _h}_<sup>_H_</sup> _h_ =1<sup>,(ii)futuretemporalway-</sup> points _Y_<sup>ˆ</sup> _t_ = _{y_ ˆ _t_ + _m}_<sup>_M_</sup> _m_ =1<sup>,and(iii)spatialroutepoints</sup> _Y_ ¯ _t_ = _{y_ ¯ _t_ + _n}_<sup>_N_</sup> _n_ =1<sup>.Here,</sup><sup>_H_=3denotesa3-secondpre-</sup> diction horizon at 1s intervals for meta-actions, _M_ = 6 denotes temporal waypoints sampled at 0.5s intervals over the same horizon, and _N_ represents the number of spatial route nodes used to parameterize the reference path. Notably, language, cross-modal, and cross-task interactions are constrained to follow causal attention, while intra-task and self-modal interactions adopt bidirectional attention. 

By operating in a shared attention space with the UE, the AE conditions the latent reasoning generated by the UE into the action generation process, thereby grounding decisionmaking and planning in high-level scene understanding and enabling knowledge transfer from the pretrained VLM to policy learning. The attention patterns are visualized in Fig. 3. As shown, understanding, decision-making, and planning are regulated through cross-task causal attention, where decision representations are conditioned on understanding, and planning is further conditioned on both understanding and decision in the latent space. Within each task, latent features follow bidirectional attention across modalities, while cross-task interactions are governed by causal attention. The AE is implemented as a task-specialized transformer with approximately 1.6B parameters and is trained from scratch to capture domain-specific knowledge for autonomous driving. Notably, the AE operates at a higher frequency than the UE, enabling efficient inference and supporting real-time autonomous driving in complex environments. 

**Action Refiner** Recently, generative planners such as diffusion policies (Chi et al., 2024) have demonstrated strong potential for autonomous driving. In our framework, we implement the policy module as a diffusion-based policy built on the Diffusion Transformer (DiT). Instead of starting the reverse process from clustered trajectories (Zou et al., 2025) or pure white noise (Chi et al., 2024), we use the spatialtemporal trajectories predicted by the AE as informative priors and perform truncated reverse denoising to generate the refined trajectories. This design provides a more reliable initialization and significantly accelerates inference. 

Concretely, the AE trajectory proposals are perturbed with multiplicative Gaussian noise (Zou et al., 2025), formulated as _τ_<sup>_′_</sup> = (1+ _ϵ_ mul) _⊙τ_ . Based on the noisy trajectory samples, we construct temporal trajectory queries _Q_ temp _∈_ R<sup>_B×M×_2</sup> , and the spatial queries _Q_ spatial _∈_ R<sup>_B×N×_2</sup> , and concatenate them as: _X_ = [ _Q_ temp _∥Q_ spatial], and processed by a stack of 

4 

**AutoMoT: An Asynchronous VLA Model for E2E Autonomous Driving** 


_Figure 4._ The architecture of DiT-based action refiner with Mixtureof-Attention blocks. 

_N_ DiT decoder blocks. The conditioning signal _c_ , which integrates the diffusion timestep, the current ego state, and lower-dimensional state history, is injected into each block through adaptive layer normalization (AdaLN). 

To effectively exploit heterogeneous information during denoising, the diffusion policy leverages two complementary sources: the latent decision states _h_ de from the AE for decision-aware trajectory generation, and the BEV feature _F_ bev from the vision encoder for spatial guidance. Existing diffusion planners either flatten heterogeneous modalities into a single token sequence for joint attention (Li et al., 2025c), or process them through sequential crossattention (Liao et al., 2025). The former dilutes the structural guidance of trajectory priors, while the latter imposes a fixed attention ordering that ties modality importance to processing sequence. To address this issue, we propose a Mixture-of-Attention (MoA) mechanism (Fig. 4) that adaptively balances attention sources between language and vision, enabling parallel and adaptive multi-source fusion while preserving anchor trajectory priors. 

Specifically, MoA adopts a main-bypass fusion design. In the main pathway, attention is computed in parallel over three sources: self-attention among temporal and spatial queries, cross-attention to BEV features, and cross-attention to latent decision states. In addition, the contribution of latent decision states is modulated by a learnable factor _g_ = tanh( _γ_ ), enabling adaptive control over multi-frame metaactions. To further stabilize information propagation across diffusion stages, we introduce residual bypass pathways that preserve global contextual cues from different modalities. Specifically, _R_ bev is obtained by mean pooling over BEV features, while _R_ reason is obtained by attention pooling over reasoning tokens. The final fused representation is computed as _X_<sup>_′_</sup> = _X_ + _α ·_ � _O_ main + _σ_ ( _βb_ ) _R_ bev + _σ_ ( _βr_ ) _R_ reason�, where _O_ main denotes the fused output of the main pathway, _α_ is a scaling factor derived from AdaLN conditioned on _c_ , and _σ_ ( _βb_ ) and _σ_ ( _βr_ ) are learnable gating coefficients. 

### **3.2. Training Strategy** 

**Decision Making** We formulate decision-making as a token-level sequence modeling problem over meta-actions, conditioned on multi-frame driving observations. For realworld evaluation, we construct a multi-frame decision- 

making dataset based on nuScenes, termed _NuSync_ . 

Specifically, _NuSync_ takes four consecutive historical RGB observations along with an additional RGB-BEV pair as input. In the synchronous setting, the RGB-BEV pair shares the same timestamp as the last historical frame, i.e., _It_<sup>sync</sup> = _{It_<sup>_RGB_</sup> _, It_<sup>_RGB_</sup> +1<sup>_, I_</sup> _t_<sup>_RGB_</sup> +2<sup>_, I_</sup> _t_<sup>_RGB_</sup> +3<sup>_, I_</sup> _t_<sup>_RGB_</sup> +3<sup>_, I_</sup> _t_<sup>_BEV_</sup> +3<sup>_}_.In</sup> the asynchronous setting, we construct temporally asynchronous samples in which the four historical frames remain consecutive, while RGB–BEV pairs are constructed at both 1-frame and 2-frame future offsets, correspond= ing to 0.5s and 1s at 2Hz. For example, _It_<sup>async</sup> _{It_<sup>_RGB_</sup> _, It_<sup>_RGB_</sup> +1<sup>_, I_</sup> _t_<sup>_RGB_</sup> +2<sup>_, I_</sup> _t_<sup>_RGB_</sup> +3<sup>_, I_</sup> _t_<sup>_RGB_</sup> + _k_<sup>_, I_</sup> _t_<sup>_BEV_</sup> + _k_<sup>_}_,where</sup><sup>_k∈_</sup> _{_ 4 _,_ 5 _}_ . In the output space, _NuSync_ annotates meta-actions over a 3-second horizon, providing up to twenty possible combinations of longitudinal and lateral actions at 1s, 2s, and 3s. After curation, _NuSync_ contains 80.1K samples in total. More details about _NuSync_ and the associated decision benchmark are provided in Appendix A.2. To the best of our knowledge, _NuSync_ is the first open-source decision dataset that supports asynchronous multi-frame meta-action inference. Similarly, for CARLA simulation, we construct the _PDM-Meta_ dataset based on PDM-Lite following the same protocol. Due to the ambiguous boundaries between lateral meta-actions in simulation, we only annotate longitudinal decisions. 

Based on the constructed meta-action datasets, given an observation sequence _ot_ , the AE predicts a sequence of metaaction tokens _z_ ˆ _t_ = _{z_ ˆ _t_<sup>_j}J_</sup> _j_ =1<sup>, where</sup><sup>_j_represents j-th token</sup> and M depicts the necessary amount of tokens to be encoded as a meta-action. Unlike the next-token prediction used by the UE, the AE adopts a token-wise prediction paradigm and optimizes the policy by minimizing the negative loglikelihood of the target decision tokens: 


where _D_ denotes the corresponding dataset. 

**Trajectory Planning** AutoMoT follows the original nuScenes setting, using four historical frames to predict a 3-second future trajectory. Following PDM-Lite, the 3- second trajectory is represented by temporal waypoints for capturing motion dynamics and 20 spatial route points for road geometry. For the AE, we optimize the trajectory planning with an _ℓ_ 1 loss: 


5 

**AutoMoT: An Asynchronous VLA Model for E2E Autonomous Driving** 

_Table 1._ Comparison of closed-loop planning performance on the CARLA Bench2Drive leaderboard. DS and SR represent Driving Score and Success Rate, respectively. 

|**Method**|**Expert**|**VLM**|**Generative**|**Closed-l**|**oop Metric**|
|---|---|---|---|---|---|
||||**Planner**|**DS**_↑_|**SR(%)**_↑_|
|MomAD (Song et al.,2025)|Think2Drive|-|-|44.54|16.71|
|UniAD-Base (Hu et al.,2023)|Think2Drive|-|-|45.81|16.36|
|TCP-traj (Wu et al.,2022)|Think2Drive|-|-|59.90|30.00|
|DriveTransformer-Large (Jia et al.,2025)|Think2Drive|-|-|63.46|35.01|
|DriveAdapter (Jia et al.,2023)|Think2Drive|-|-|64.22|33.08|
|<br>Raw2Drive (Yang et al.,2026)|Think2Drive|-|-|71.36|50.24|
|DiffusionDrive (Liao et al.,2025)|PDM-Lite|-|✓|77.68|57.72|
|TransFuser++ (Jaeger et al.,2023b)|PDM-Lite|-|-|84.21|67.27|
|ReasonPlan (Liu et al.,2025c)|Think2Drive|✓|-|64.01|34.55|
|Recogdrive (Li et al.,2025c)|Think2Drive|✓|✓|71.36|45.45|
|<br>DriveMoE (Yang et al.,2025)|Think2Drive|✓|-|74.22|48.64|
|ORION (Fu et al.,2025a)|Think2Drive|✓|✓|77.74|54.62|
|SpaceDrive+ (Li et al.,2025a)|PDM-Lite|✓|-|78.02|55.11|
|MindDrive (Fu et al.,2025b)|Think2Drive|✓|✓|78.04|55.09|
|AutoVLA (Zhou et al.,2025b)|PDM-Lite|✓|-|78.84|57.73|
|SimLingo (Renz et al.,2025)|PDM-Lite|✓|-|85.07|67.27|
|AutoMoT (ours)|PDM-Lite|✓|-|**87.34**|**70.00**|
|AutoMoT + (ours)|PDM-Lite|✓|✓|**89.42**|**74.09**|


where _Yt_<sup>temp</sup> and _Yt_<sup>spatial</sup> denote ground-truth temporal and spatial trajectories. Notably, the decision-making and trajectory planning are jointly optimized within the AE, enabling AutoMoT to learn coherent action policies grounded in semantic representations from the UE. 

To further enhance the driving behaviors, we employ a diffusion policy to refine the trajectory proposals. Unlike standard diffusion processes that initialize from Gaussian noise, we implement a truncated diffusion paradigm. This approach treats the proposal trajectories from the AutoMoT as an anchor, performing reverse denoising from this informed prior to the expert ground truth. For training and evaluation, we utilize the PDM-Lite dataset, which contains over 700,000 samples across 5,000+ scenarios. Each sample consists of 4 historical frames at a 2Hz sampling rate, with the model tasked to refine spatial-temporal waypoints proposed by AE. We employ L1 reconstruction error as the loss function for trajectory refinement. 

### **3.3. Asynchronous Inference with KV Caching** 

We formulate asynchronous inference as a multi-rate process in which reasoning and action inference evolve at different temporal resolutions, while both remain grounded in realtime visual observations. The interaction between these two processes is mediated by a shared key–value (KV) cache, as illustrated in Fig. 2. At an arbitrary timestep _t_ , given the current observation _ot_ , the AE derives layer-wise queries, keys, and values _{Q_<sup>_l_</sup> act<sup>(</sup><sup>_t_)</sup><sup>_, K_</sup> act<sup>_l_(</sup><sup>_t_)</sup><sup>_, V_</sup> act<sup>_l_(</sup><sup>_t_)</sup><sup>_}_foreachatten-</sup> tion layer. Correspondingly, _τ_ ( _t_ ) denotes the time index of the most recent scene representation update available at action step _t_ , satisfying _τ_ ( _t_ ) _≤ t_ . At the update time _τ_ ( _t_ ), 

the UE produces a set of layer-wise KV representations, which are stored in a persistent KV cache: 


Therefore, the keys and values involved in the final attention computation are formed by combining the KV cache from the UE at time _τ_ ( _t_ ) with the KV representations derived from the AE at time _t_ , which can be expressed as: 


where [ _·∥·_ ] denotes concatenation along the sequence dimension, and all keys and values share the same embedding dimensionality _d_ . The joint attention is then computed as 


The joint attention and asynchronous inference with KV Caching constitute the core characteristics of AutoMoT. By allowing action inference to reuse scene representations that are updated at a different temporal frequency, the proposed framework enables decision-making and trajectory planning to operate with a higher execution frequency than scene understanding, while remaining grounded in real-time perceptual inputs. This design aligns with the real-time requirements of real-world autonomous driving. 

6 

**AutoMoT: An Asynchronous VLA Model for E2E Autonomous Driving** 

_Table 2._ Comparison of the Open-loop planning in nuScenes. The ST-P3 evaluation protocol is used by default. 

|**Method**|**Ego Status**|**Fin**|**etuning**|||**L2 (**|**m)**_↓_|||**Collisio**|**n (%)**|_↓_|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||**Understanding**|**Decision**|**Planning**|**1s**|**2s**|**3s**|**Avg.**|**1s**|**2s**|**3s**|**Avg.**|
|UniAD (Hu et al.,2023)|Vector|-|-|✓|0.44|0.67|0.96|0.69|0.04|0.08|0.23|0.12|
|VAD (Jiang et al.,2023)|Vector|-|-|✓|0.17|0.34|0.60|0.37|0.07|0.10|0.24|0.14|
|Ego-MLP (Li et al.,2024)|Vector|-|-|✓|0.15|0.32|0.59|0.35|0.00|0.27|0.85|0.37|
|DriveTransformer-Large (Jia et al.,2025)|Vector|-|-|✓|0.16|0.30|0.55|0.33|0.01|0.06|0.15|0.07|
|AutoVLA (Zhou et al.,2025b)|Text|✓|-|✓|0.21|0.38|0.60|0.40|0.13|0.18|0.28|0.20|
|ORION(Chat-B2D)(Fu et al.,2025a)|-|✓|-|✓|0.17|0.31|0.55|0.34|0.05|0.25|0.80|0.37|
|RoboTron-Drive (Huang et al.,2025b)|-|✓|-|✓|0.14|0.30|0.57|0.33|0.03|0.12|0.63|0.26|
|OpenDrive-VLA (Zhou et al.,2026)|Text|✓|-|✓|0.15|0.31|0.55|0.33|0.01|0.08|0.21|0.10|
|OmniDrive (Wang et al.,2024)|Vector|✓|-|✓|0.14|0.29|0.55|0.33|0.00|0.13|0.78|0.30|
|EMMA<sup>_†_ </sup>(Hwang et al.,2024)|Text|✓|-|✓|0.14|0.29|0.54|0.32|-|-|-|-|
|SpaceDrive (Zhou et al.,2025b)|Vector|✓|-|✓|0.15|0.29|0.51|0.32|0.04|0.18|0.49|0.23|
|OpenREAD (Zhang et al.,2025)|Vector|✓|-|✓|0.17|0.34|0.56|0.36|0.04|0.08|0.22|0.11|
|Drive-R1 (Li et al.,2026)|Text|✓|-|✓|0.14|**0.28**|0.50|**0.31**|0.02|0.06|0.19|0.09|
|DriveVLM-Dual (Tian et al.,2025)|Vector|✓|-|✓|0.15|0.29|**0.48**|**0.31**|0.05|0.08|0.17|0.10|
|OpenEMMA (Xing et al.,2025)|Text|-|-|-|1.45|3.21|3.76|2.81|-|-|-|-|
|AutoMoT (Ours)|Vector|-|✓|✓|**0.14**|0.29|0.54|0.32|**0.01**|**0.06**|**0.15**|**0.07**|


## **4. Experiments** 

### **4.1. Experimental Setup** 

**Datasets.** For the reasoning tasks, we evaluate the general performance of all models on both autonomous driving benchmarks and general-domain datasets, including OmniDrive (Wang et al., 2024), ScienceQA, and FigureQA. For action-level tasks, AutoMoT is primarily trained on three datasets: nuSync, which is annotated and curated in this work for decision-making, nuScenes (Caesar et al., 2020), and the CARLA-Garage dataset (Jaeger et al., 2023a) for trajectory planning. We follow the original training and evaluation protocols provided by the trajectory planning benchmarks. Additionally, as part of our ablation study, we finetune the understanding expert of AutoMoT exclusively on two autonomous driving VQA datasets, LingoQA (Marcu et al., 2024) and CODA-LM (Chen et al., 2025). 

**Benchmarks and Metrics.** Scene understanding performance is evaluated on the LingoQA (Marcu et al., 2024) benchmark using its native metric, Lingo-Judge, as well as on other AD-tailored and general VQA datasets using GPT-based scores. We further evaluate the open-loop performance of AutoMoT on the nuScenes (Caesar et al., 2020) benchmark, using average accuracy (AA) for decisionmaking, as well as L2 distance and collision rate for trajectory planning. Closed-loop performance is assessed on the Bench2Drive (Jia et al., 2024) benchmark following the officially provided evaluation metrics. 

GPUs. 

### **4.2. Main Results** 

In this section, we present detailed quantitative comparisons between AutoMoT and representative prior and SOTA methods across both reasoning and action-level tasks. Due to space limitations, detailed decision-making results are reported in Appendix A.2. 

**Closed-Loop Planning Benchmark Results.** We first evaluate AutoMoT on a closed-loop evaluation benchmark and report the quantitative results in Table 1. It is clear that AutoMoT outperforms all VLM-augmented baseline methods and achieves SOTA performance in terms of both driving score (DS) and the success rate (SR). It is worth noting that SimLingo employs action dreamer–based simulation for data augmentation to increase the amount of training data, while AutoMoT is trained solely on the original dataset, yet dominates SimLingo (Renz et al., 2025) in terms of both main metrics. In addition, incorporating the AR further improves closed-loop driving performance, demonstrating the benefit of diffusion-based trajectory refinement. For AutoMoT +, we report the average performance over multiple runs, although higher peak performance is observed. This is because the intrinsic stochasticity of diffusion policies can be amplified in closed-loop driving, where small trajectory deviations may accumulate over time and lead to different outcomes. 

**Implementation Details.** For action policy learning, we adopt a learning rate ranging from 1 _×_ 10<sup>_−_4</sup> to 2 _×_ 10<sup>_−_5</sup> and employ the Fully Sharded Data Parallel (FSDP) training strategy. All models are trained using eight NVIDIA A100 

**Open-Loop Planning Benchmark Results.** The openloop planning performance of AutoMoT compared with various baselines is reported in Table 2. AutoMoT achieves competitive performance in terms of L2 displacement and 

7 

**AutoMoT: An Asynchronous VLA Model for E2E Autonomous Driving** 

_Table 3._ Comparison of reasoning capabilities across both generaldomain and autonomous driving–specific datasets. _†_ : Results are reproduced using the official checkpoints and evaluation environments. 

|**Method**|**LingoQA**|**OmniDrive**|**CODA-LM**|**TallyQA**|**InfoVQA**|
|---|---|---|---|---|---|
|ReCogDrive|**67.20**|0.82|5.90|69.60|75.80|
|Robotron-Drive<sup>_†_</sup>|59.20|0.82|**6.20**|63.40|42.60|
|OpenEMMA|48.00|0.43|4.80|80.00|71.40|
|AutoMoT|67.00|**0.89**|6.07|**81.40**|**89.30**|


attains SOTA results on collision rate. Notably, most existing methods adapt scene understanding to the autonomous driving domain by fine-tuning the VLM backbone, whereas only OpenEMMA and AutoMoT refrain from such domainspecific adaptation, yet exhibit a clear performance distinction in terms of L2 displacement. These results indicate that policy learning in VLA models plays a critical role in action-level tasks, extending beyond the inherent expertise of pre-trained VLMs. In contrast, fine-tuning the VLM backbone on AD datasets yields only marginal improvements in planning metrics. More importantly, such minor gains (e.g., a few centimeters in L2 displacement) may come at the cost of severe degradation in scene understanding capability due to catastrophic forgetting. To examine this trade-off more comprehensively, we further evaluate AutoMoT together with other open-source methods on both AD-specific and general-domain VQA datasets to assess their scene understanding performance. 

**General VQA Benchmark Results.** Observations from the planning benchmarks further motivate a deeper investigation into whether additional domain-specific adaptation of scene understanding on top of pre-trained VLMs is indeed beneficial for overall autonomous driving performance. To clarify this question, we evaluate AutoMoT against other open-source baseline approaches on a diverse set of VQA benchmarks spanning both autonomous-driving–specific and general-domain tasks, as summarized in Table 3. Although both ReCogDrive and Robotron-Drive fine-tune their VLM backbones on LingoQA, OmniDrive, and CODA-LM, the resulting improvements are either marginal or even inferior to AutoMoT, which keeps the VLM backbone frozen. For example, ReCogDrive only marginally outperforms AutoMoT by 0.2 on the Lingo-Judge metric, while both ReCogDrive and Robotron-Drive underperform AutoMoT on the perception task of OmniDrive. More importantly, their performance on general-domain VQA benchmarks degrades substantially after fine-tuning, falling well below that of OpenEMMA and AutoMoT. Taken together with the analysis on planning benchmarks, these results suggest that fine-tuning the VLM backbone on AD-tailored scene understanding tasks provides only limited benefits for subsequent planning behaviors. Such gains are often marginal and accompanied by overfitting to specific benchmarks, leading to catastrophic forgetting and degraded generalization. In 

_Table 4._ Ablation study results of investigating the performance boundary of the pre-trained backbone. _†_ : System prompt is provided; _‡_ : Fine-tuned on autonomous driving datasets; L: LingoJudge; G:GPT-Score; A: Token Accuracy. 

|**Benchmark**|**Task Category**|**AutoMoT**<sup>_†_</sup>|**AutoMoT**<sup>_‡_</sup>|
|---|---|---|---|
|LingoQA (L)|Scene Understanding|67.00|**67.20**|
|OmniDrive (G)|Counterfactual Planning|18.20|**67.80**|
|ScienceQA (A)|General Knowledge|**88.60**|87.80|
|FigureQA (A)|General Knowledge|**97.60**|91.20|
|TallyQA (A)|General Knowledge|**81.40**|52.40|
|InfographicVQA (G)|General Knowledge|**89.30**|50.20|
|VizWiz (G)|General Knowledge|**75.60**|50.20|


the following section, we further investigate the functional boundaries of pre-trained VLMs in autonomous driving, examining whether domain-specific fine-tuning is necessary across different AD tasks. 

### **4.3. Performance Boundary of Pretrained Backbone** 

In this section, we aim to investigate when and to what extent AD-tailored fine-tuning is beneficial under a more controlled and fair setting, as direct comparisons with existing methods are often confounded by various factors. To this end, we fine-tune the VLM backbone of AutoMoT on two autonomous driving datasets: LingoQA (Marcu et al., 2024) and the counterfactual reasoning subset of OmniDrive (Wang et al., 2024). The former is widely used for scene understanding in the autonomous driving domain, while the latter is closely related to planning performance, as it shares the same visual inputs as the nuScenes (Caesar et al., 2020) benchmark and its question prompts explicitly contain trajectory-related information. We then evaluate the fine-tuned model on the test splits of these two datasets, together with five additional general-domain knowledge benchmarks, ScienceQA (Lu et al., 2022), FigureQA (Kahou et al., 2017), TallyQA (Acharya et al., 2019), InfographicVQA (Mathew et al., 2022), and VizWiz (Gurari et al., 2018), as summarized in Table 4. 

As shown by the quantitative results, fine-tuning the VLM backbone yields marginal improvements on scene understanding performance in LingoQA, but leads to substantial gains on the counterfactual planning task. This suggests that pre-trained VLMs can already support competitive multi-task scene understanding through semantic prompting alone, whereas fine-tuning remains essential for actionlevel tasks such as trajectory planning. Notably, the impact of fine-tuning on general-domain reasoning is highly taskdependent. On datasets with relatively simple answer spaces, such as ScienceQA and FigureQA, fine-tuning results in only minor performance changes, indicating that basic recognition and short-form reasoning capabilities are largely preserved. In contrast, for more complex VQA benchmarks that require compositional reasoning and multi-step inference, such as TallyQA, InfographicVQA, and VizWiz, per- 

8 

**AutoMoT: An Asynchronous VLA Model for E2E Autonomous Driving** 

_Table 5._ Trajectory planning performance under synchronized and asynchronous settings. AutoMoT refers to the proposed model with the KV cache enabled, while AutoMoT-S denotes the synchronized variant that runs the understanding expert (UE) and action expert (AE) at the same frequency, without introducing temporal misalignment between UE and AE. 

|Setting|L2@1s_↓_|L2@2s_↓_|L2@3s_↓_|L2avg _↓_|
|---|---|---|---|---|
|AutoMoT-S|0.140|0.290|0.537|**0.322**|
|AutoMoT|0.141|0.293|0.544|0.324|


formance degrades substantially after fine-tuning. For instance, accuracy on TallyQA drops from 81.40 to 52.40, and on InfographicVQA from 89.30 to 50.20, corresponding to an almost 50% reduction relative to the pre-trained baseline. These results demonstrate that domain-specific fine-tuning mainly degrades high-level reasoning ability, providing clear evidence of catastrophic forgetting when VLMs are directly adapted to the autonomous driving domain. A similar phenomenon has also been observed in other work (Li et al., 2025b). 

Beyond validating our design choice, these results prompt a rethinking of the role of pre-trained VLMs in autonomous driving systems. Rather than uniformly adapting VLMs across all task levels, our findings suggest a clearer functional boundary: high-level scene understanding and reasoning do not necessarily require extensive domain-specific adaptation, whereas task-specific fine-tuning should primarily target action-level components that operate under domain-specific constraints. In this regard, our design preserves the general intelligence of the UE and transfers its reasoning knowledge to the AE through joint attention sharing, enabling effective action-level learning without sacrificing general reasoning ability. 

### **4.4. Asynchronous versus Synchronous Inference** 

In this ablation, we study whether decoupling reasoning and action inference at different temporal resolutions hurts planning performance because the action expert may receive slightly outdated visual context. To test this, we build two dedicated validation settings by introducing controlled temporal offsets between the visual inputs used by the understanding expert (UE) and the action expert (AE). In the decoupled setting, UE and AE are asynchronous, with twostep (1.0 s) offsets. In the coupled setting, both experts operate synchronously. We compare AutoMoT, which uses asynchronous inference with a persistent KV cache, against a synchronized variant, AutoMoT-S, which disables the KV cache and recomputes both UE and AE outputs at every step. 

Table 5 shows that AutoMoT retains nearly the same planning accuracy as the synchronized variant AutoMoT-S, despite the temporal decoupling between UE and AE. The 

_Table 6._ Latency breakdown of AutoMoT under synchronized (AutoMoT-S) and default AutoMoT settings. 

|Setting|Generative||Time|(ms)||Frequency|
|---|---|---|---|---|---|---|
||Planner|UE|AE|AR|Total|Hz|
|AutoMoT-S|-|80.3|37.0|-|117.3|8.5|
|AutoMoT|-|0.0|37.0|-|37.0|27.0|
|AutoMoT-S|✓|80.3|37.0|26.0|143.3|7.0|
|AutoMoT|✓|0.0|37.0|26.0|63.0|16.0|


differences are small at all horizons: L2@1s changes from 0.140 to 0.141, L2@2s from 0.290 to 0.293, and L2@3s from 0.537 to 0.544. The average error increases only slightly, from 0.322 to 0.324, which corresponds to a relative degradation of 0.62%. This indicates that the stale visual context introduced by asynchronous execution has only a minor effect on planning quality. 

At the same time, Table 6 shows a clear gain in efficiency. Without the diffusion head in the action expert, AutoMoT-S takes 117.3 ms per step, including 80.3 ms for preparing the KV cache in the understanding expert and 37.0 ms for the action expert, whereas AutoMoT reduces the total latency to 37.0 ms by reusing the cached understanding context, corresponding to a 68.5% reduction. For each asynchronous action step, the latency of the UE is reported as 0.0 ms because its representations are directly reused from the cached KV states. With the diffusion head enabled in the action expert, AutoMoT-S and AutoMoT achieve inference latencies of 143.3 ms and 63.0 ms, respectively. Overall, these results show that the proposed asynchronous inference scheme provides a substantial speedup while keeping planning performance almost unchanged. The inference latency comparison between AutoMoT and other VLA baselines is reported in Appendix A.4. 

## **5. Conclusion** 

We propose AutoMoT, an asynchronous VLA model for end-to-end autonomous driving that unifies reasoning and action generation within a single MoT architecture via layerwise joint attention sharing. AutoMoT preserves the general reasoning capability of the VLM backbone during actionpolicy learning, while enabling efficient asynchronous inference across tasks with different execution frequencies. Extensive evaluations on simulation and real-world benchmarks under both open- and closed-loop settings show that AutoMoT achieves SOTA performance against existing baselines, despite not fine-tuning the VLM backbone on AD-specific datasets. Moreover, experiments on both general-domain and AD-specific VQA benchmarks show that pre-trained VLMs already provide strong multi-task scene understanding through semantic prompting, whereas fine-tuning remains essential for action-level tasks in endto-end autonomous driving. 

9 

**AutoMoT: An Asynchronous VLA Model for E2E Autonomous Driving** 

## **Acknowledgment** 

This work was supported by the Ministry of Education (MOE), Singapore, under Tier 2 Grant (MOE-T2EP502220002). 

## **Impact Statement** 

This work proposes a vision–language–action (VLA) model for end-to-end autonomous driving that unifies scene understanding, decision-making, and planning within a single framework, while enabling asynchronous inference across tasks with different frequencies and thus, better accommodating the real-time requirements of autonomous driving. While deploying VLA-scale models on current onboard computational platforms remains resource-intensive, rapid progress in computational hardware and model acceleration techniques, including quantization, pruning, and efficient caching, may make onboard deployment of AutoMoT increasingly practical. In addition, we investigate the functional boundaries of pre-trained VLMs in autonomous driving, clarifying when and to what extent AD-specific fine-tuning is necessary for different task levels. 

## **References** 

- Acharya, M., Kafle, K., and Kanan, C. Tallyqa: Answering complex counting questions. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 33, pp. 8076– 8084, 2019. 8 

- Caesar, H., Bankiti, V., Lang, A. H., Vora, S., Liong, V. E., Xu, Q., Krishnan, A., Pan, Y., Baldan, G., and Beijbom, O. nuscenes: A multimodal dataset for autonomous driving. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 11621–11631, 2020. 7, 8 

- Chen, K., Li, Y., Zhang, W., Liu, Y., Li, P., Gao, R., Hong, L., Tian, M., Zhao, X., Li, Z., et al. Automated evaluation of large vision-language models on self-driving corner cases. In _2025 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)_ , pp. 7817–7826. IEEE, 2025. 7 

- Chen, S., Jiang, B., Gao, H., Liao, B., Xu, Q., Zhang, Q., Huang, C., Liu, W., and Wang, X. Vadv2: End-to-end vectorized autonomous driving via probabilistic planning. _arXiv preprint arXiv:2402.13243_ , 2024. 2 

- Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., and Song, S. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 2024. 2, 4 

- Deng, C., Zhu, D., Li, K., Gou, C., Li, F., Wang, Z., Zhong, S., Yu, W., Nie, X., Song, Z., et al. Emerging proper- 

ties in unified multimodal pretraining. _arXiv preprint arXiv:2505.14683_ , 2025. 3 

- Fu, H., Zhang, D., Zhao, Z., Cui, J., Liang, D., Zhang, C., Zhang, D., Xie, H., Wang, B., and Bai, X. Orion: A holistic end-to-end autonomous driving framework by vision-language instructed action generation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 24823–24834, 2025a. 2, 3, 6, 7 

- Fu, H., Zhang, D., Zhao, Z., Cui, J., Xie, H., Wang, B., Chen, G., Liang, D., and Bai, X. Minddrive: A visionlanguage-action model for autonomous driving via online reinforcement learning. _arXiv preprint arXiv:2512.13636_ , 2025b. 6 

- Gurari, D., Li, Q., Stangl, A. J., Guo, A., Lin, C., Grauman, K., Luo, J., and Bigham, J. P. Vizwiz grand challenge: Answering visual questions from blind people. In _Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , June 2018. 8 

- Ho, J., Jain, A., and Abbeel, P. Denoising diffusion probabilistic models. In Larochelle, H., Ranzato, M., Hadsell, R., Balcan, M., and Lin, H. (eds.), _Advances in Neural Information Processing Systems_ , volume 33, pp. 6840– 6851. Curran Associates, Inc., 2020. 2 

- Hu, Y., Yang, J., Chen, L., Li, K., Sima, C., Zhu, X., Chai, S., Du, S., Lin, T., Wang, W., et al. Planning-oriented autonomous driving. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 17853–17862, 2023. 1, 2, 6, 7 

- Huang, W., Chen, C., Qi, H., Lv, C., Du, Y., and Yang, H. Motvla: A vision-language-action model with unified fast-slow reasoning. _arXiv preprint arXiv:2510.18337_ , 2025a. 3 

- Huang, W., Zhang, S., Chua, C., Liang, Y., Mao, Z., Yang, H., and Lv, C. Towards safe mobility: A unified transportation foundation model enabled by open-ended vision-language dataset. _arXiv preprint arXiv:2604.22260_ , 2026. 2 

- Huang, Z., Feng, C., Yan, F., Xiao, B., Jie, Z., Zhong, Y., Liang, X., and Ma, L. Robotron-drive: All-in-one large multimodal model for autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 8011–8021, 2025b. 7 

- Hwang, J.-J., Xu, R., Lin, H., Hung, W.-C., Ji, J., Choi, K., Huang, D., He, T., Covington, P., Sapp, B., et al. Emma: End-to-end multimodal model for autonomous driving. _arXiv preprint arXiv:2410.23262_ , 2024. 2, 7 

- Jaeger, B., Chitta, K., and Geiger, A. Hidden biases of endto-end driving models. In _Proc. of the IEEE International Conf. on Computer Vision (ICCV)_ , 2023a. 7 

10 

**AutoMoT: An Asynchronous VLA Model for E2E Autonomous Driving** 

- Jaeger, B., Chitta, K., and Geiger, A. Hidden biases of endto-end driving models. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 8240– 8249, 2023b. 1, 6 

- Jia, X., Gao, Y., Chen, L., Yan, J., Liu, P. L., and Li, H. Driveadapter: Breaking the coupling barrier of perception and planning in end-to-end autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 7953–7963, 2023. 6 

- Jia, X., Yang, Z., Li, Q., Zhang, Z., and Yan, J. Bench2drive: Towards multi-ability benchmarking of closed-loop endto-end autonomous driving. _Advances in Neural Information Processing Systems_ , 37:819–844, 2024. 7 

- Jia, X., You, J., Zhang, Z., and Yan, J. Drivetransformer: Unified transformer for scalable end-to-end autonomous driving. In _International Conference on Learning Representations (ICLR)_ , 2025. 6, 7 

- Jiang, B., Chen, S., Xu, Q., Liao, B., Chen, J., Zhou, H., Zhang, Q., Liu, W., Huang, C., and Wang, X. Vad: Vectorized scene representation for efficient autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 8340–8350, 2023. 1, 2, 7 

- Jiang, B., Chen, S., Liao, B., Zhang, X., Yin, W., Zhang, Q., Huang, C., Liu, W., and Wang, X. Senna: Bridging large vision-language models and end-to-end autonomous driving. _arXiv preprint arXiv:2410.22313_ , 2024. 3, 13 

- Jiang, B., Chen, S., Zhang, Q., Liu, W., and Wang, X. Alphadrive: Unleashing the power of vlms in autonomous driving via reinforcement learning and reasoning. _arXiv preprint arXiv:2503.07608_ , 2025. 2 

- Kahou, S. E., Michalski, V., Atkinson, A., Kad´ ar,´ A.,<sup>´</sup> Trischler, A., and Bengio, Y. Figureqa: An annotated figure dataset for visual reasoning. _arXiv preprint arXiv:1710.07300_ , 2017. 8 

- Li, P., Zhang, Z., Holtz, D., Yu, H., Yang, Y., Lai, Y., Song, R., Geiger, A., and Zell, A. Spacedrive: Infusing spatial awareness into vlm-based autonomous driving. _arXiv preprint arXiv:2512.10719_ , 2, 2025a. 6 

- Li, Y., Tian, M., Lin, Z., Zhu, J., Zhu, D., Liu, H., Wang, Z., Zhang, Y., Xiong, Z., and Zhao, X. Finegrained evaluation of large vision-language models in autonomous driving. _2025 IEEE/CVF International Conference on Computer Vision (ICCV)_ , pp. 9431–9442, 2025b. URL https://api.semanticscholar. org/CorpusID:277349278. 9 

- Li, Y., Xiong, K., Guo, X., Li, F., Yan, S., Xu, G., Zhou, L., Chen, L., Sun, H., Wang, B., et al. Recogdrive: A reinforced cognitive framework for end-to-end autonomous driving. _arXiv preprint arXiv:2506.08052_ , 2025c. 2, 3, 5, 6 

- Li, Y., Tian, M., Zhu, D., Zhu, J., Lin, Z., Xiong, Z., and Zhao, X. Drive-r1: Bridging reasoning and planning in vlms for autonomous driving with reinforcement learning. _Proceedings of the AAAI Conference on Artificial Intelligence_ , 40(8):6708–6716, Mar. 2026. doi: 10.1609/aaai.v40i8.37602. 7 

- Li, Z., Yu, Z., Lan, S., Li, J., Kautz, J., Lu, T., and Alvarez, J. M. Is ego status all you need for open-loop end-to-end autonomous driving? In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 14864–14873, 2024. 7 

- Liao, B., Chen, S., Yin, H., Jiang, B., Wang, C., Yan, S., Zhang, X., Li, X., Zhang, Y., Zhang, Q., et al. Diffusiondrive: Truncated diffusion model for end-to-end autonomous driving. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 12037–12047, 2025. 1, 2, 5, 6 

- Liu, H., Huang, Z., Huang, W., Yang, H., Mo, X., and Lv, C. Hybrid-prediction integrated planning for autonomous driving. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2025a. 1 

- Liu, S., Chen, W., Li, W., Wang, Z., Yang, L., Huang, J., Zhang, Y., Huang, Z., Cheng, Z., and Yang, H. Bridgedrive: Diffusion bridge policy for closed-loop trajectory planning in autonomous driving. _arXiv preprint arXiv:2509.23589_ , 2025b. 2 

- Liu, X., Zhong, Z., Zhang, Q., Guo, Y., Zheng, Y., Wang, J., Zhao, D., Liu, Y.-F., Su, Z., Gao, Y., et al. Reasonplan: Unified scene prediction and decision reasoning for closed-loop autonomous driving. In _Conference on Robot Learning_ , pp. 3051–3068. PMLR, 2025c. 6 

- Lu, P., Mishra, S., Xia, T., Qiu, L., Chang, K.-W., Zhu, S.-C., Tafjord, O., Clark, P., and Kalyan, A. Learn to explain: Multimodal reasoning via thought chains for science question answering. In _The 36th Conference on Neural Information Processing Systems (NeurIPS)_ , 2022. 8 

- Marcu, A.-M., Chen, L., Hunermann, J., Karnsund, A., Han-¨ otte, B., Chidananda, P., Nair, S., Badrinarayanan, V., Kendall, A., Shotton, J., et al. Lingoqa: Visual question answering for autonomous driving. In _European Conference on Computer Vision_ , pp. 252–269. Springer, 2024. 7, 8 

11 

**AutoMoT: An Asynchronous VLA Model for E2E Autonomous Driving** 

- Mathew, M., Bagal, V., Tito, R., Karatzas, D., Valveny, E., and Jawahar, C. Infographicvqa. In _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision_ , pp. 1697–1706, 2022. 8 

- Renz, K., Chen, L., Arani, E., and Sinavski, O. Simlingo: Vision-only closed-loop autonomous driving with language-action alignment. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 11993–12003, 2025. 3, 6, 7 

- Song, J., Meng, C., and Ermon, S. Denoising diffusion implicit models. In _International Conference on Learning Representations_ , 2021. URL https://openreview. net/forum?id=St1giarCHLP. 2 

- Song, Z., Jia, C., Liu, L., Pan, H., Zhang, Y., Wang, J., Zhang, X., Xu, S., Yang, L., and Luo, Y. Don’t shake the wheel: Momentum-aware planning in end-to-end autonomous driving. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 22432–22441, 2025. 6 

- Tian, X., Gu, J., Li, B., Liu, Y., Wang, Y., Zhao, Z., Zhan, K., Jia, P., Lang, X., and Zhao, H. Drivevlm: The convergence of autonomous driving and large vision-language models. In _Conference on Robot Learning_ , pp. 4698– 4726. PMLR, 2025. 2, 3, 7 

- Wang, S., Yu, Z., Jiang, X., Lan, S., Shi, M., Chang, N., Kautz, J., Li, Y., and Alvarez, J. M. Omnidrive: A holistic llm-agent framework for autonomous driving with 3d perception, reasoning and planning. _CoRR_ , 2024. 7, 8 

- Wang, Y., Luo, W., Bai, J., Cao, Y., Che, T., Chen, K., Chen, Y., Diamond, J., Ding, Y., Ding, W., et al. Alpamayo-r1: Bridging reasoning and action prediction for generalizable autonomous driving in the long tail. _arXiv preprint arXiv:2511.00088_ , 2025. 2, 3 

- Weng, X., Ivanovic, B., Wang, Y., Wang, Y., and Pavone, M. Para-drive: Parallelized architecture for real-time autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 15449–15458, 2024. 2 

   - Yang, Z., Chai, Y., Jia, X., Li, Q., Shao, Y., Zhu, X., Su, H., and Yan, J. Drivemoe: Mixture-of-experts for visionlanguage-action model in end-to-end autonomous driving. _arXiv preprint arXiv:2505.16278_ , 2025. 6 

   - Yang, Z., Jia, X., Li, Q., Yang, X., Yao, M., and Yan, J. Raw2drive: Reinforcement learning with aligned world models for end-to-end autonomous driving (in carla v2). _Advances in Neural Information Processing Systems_ , 38: 134122–134147, 2026. 6 

   - Zhang, S., Huang, W., Gao, Z., Chen, H., and Lv, C. Wisead: Knowledge augmented end-to-end autonomous driving with vision-language model. _arXiv preprint arXiv:2412.09951_ , 2024. 2 

   - Zhang, S., Huang, W., Chen, Z., Collister, C. J., Huang, Q., and Lv, C. Openread: Reinforced open-ended reasoning for end-to-end autonomous driving with llm-as-critic. _arXiv preprint arXiv:2512.01830_ , 2025. 7 

   - Zhou, X., Chen, X., and Yang, J. Diff-refiner: Enhancing multi-agent trajectory prediction with a plug-and-play diffusion refiner. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 10779–10785. IEEE, 2025a. 2 

   - Zhou, X., Han, X., Yang, F., Ma, Y., Tresp, V., and Knoll, A. Opendrivevla: Towards end-to-end autonomous driving with large vision language action model. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 40, pp. 13782–13790, 2026. 2, 7 

   - Zhou, Z., Cai, T., Zhao, S. Z., Zhang, Y., Huang, Z., Zhou, B., and Ma, J. Autovla: A vision-language-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. _arXiv preprint arXiv:2506.13757_ , 2025b. 3, 6, 7 

   - Zou, J., Chen, S., Liao, B., Zheng, Z., Song, Y., Zhang, L., Zhang, Q., Liu, W., and Wang, X. Diffusiondrivev2: Reinforcement learning-constrained truncated diffusion modeling in end-to-end autonomous driving. _arXiv preprint arXiv:2512.07745_ , 2025. 4 

- Wu, P., Jia, X., Chen, L., Yan, J., Li, H., and Qiao, Y. Trajectory-guided control prediction for end-to-end autonomous driving: A simple yet strong baseline. _Advances in Neural Information Processing Systems_ , 35: 6119–6132, 2022. 6 

- Xing, S., Qian, C., Wang, Y., Hua, H., Tian, K., Zhou, Y., and Tu, Z. Openemma: Open-source multimodal model for end-to-end autonomous driving. In _Proceedings of the Winter Conference on Applications of Computer Vision_ , pp. 1001–1009, 2025. 7 

12 

**AutoMoT: An Asynchronous VLA Model for E2E Autonomous Driving** 

## **A. Appendix for AutoMoT.** 

### **A.1. Data Flow of AutoMoT** 


_Figure 5._ The detailed data flow of AutoMoT. 

### **A.2. Decision-Making Benchmark Results** 

**Decision Benchmark on NuSync Dataset.** In this section, we report the quantitative results of decision-making over the dataset constructed by ourselves, as mentioned in Section 3.2. The decision space consists of lateral actions, including _turn left_ , _slight left_ , _go straight_ , _slight right_ , _turn right_ , and longitudinal actions, including _accelerate_ , _slow_ , _keep_ , and _stop_ , which contains consecutive meta-actions for three future time frames: 1s, 2s, 3s. Moreover, on top of this multi-frame decision-making dataset, we additionally construct an asynchronous version by decoupling the temporal alignment between semantic reasoning and action prediction. Specifically, the decoupled set contains asynchronous samples with one-step asynchrony (0.5 s) and two-step asynchrony (1.0 s). We then evaluate both AutoMoT (default asynchronous setup) and a coupled variant (AutoMoT-S) that disables the KV cache and runs UE and AE at the same frequency, recomputing all outputs at every step, and the results are shown in Table 7. We observe that although temporal asynchrony introduces additional uncertainty, the accuracy drop remains marginal, suggesting that KV-cache reuse effectively preserves semantic and temporal coherence across timesteps. 

_Table 7._ Decision-making accuracy under synchronized and asynchronous settings at different time horizons. 

||**L**|**ateral Acc.**|_↑_|**Long**|**itudinal A**|**cc.** _↑_|**J**|**oint Acc.**|_↑_|
|---|---|---|---|---|---|---|---|---|---|
|**Method**|1s|2s|Avg|1s|2s|Avg|1s|2s|Avg|
|AutoMoT-S|95.00%|83.20%|84.50%|77.38%|56.81%|62.28%|73.84%|46.77%|53.49%|
|AutoMoT|94.06%|82.69%|83.79%|77.57%|56.85%|62.38%|73.40%|46.36%|53.10%|


**Decision Benchmark on Senna Dataset.** In order to confirm the superiority of AutoMoT, we further evaluate decisionmaking performance on the Senna meta-action benchmark constructed on nuScenes by following Senna (Jiang et al., 

13 

**AutoMoT: An Asynchronous VLA Model for E2E Autonomous Driving** 

2024). According to the original setting, Senna defines discrete meta-action labels by analyzing future trajectories, where longitudinal actions are categorized into _stop_ , _accelerate_ , _decelerate_ , and _constant-speed_ based on velocity variations, while lateral actions are categorized into _left/right turn_ , _left/right lane change_ , and _straight_ based on lateral displacement and heading changes. These meta-action labels provide a structured abstraction of driving behaviors and enable systematic evaluation of high-level decision policies. 

As shown in Table 8, AutoMoT achieves superior decision accuracy over the Senna baseline, demonstrating the superiority of our action expert in terms of action policy learning. 

_Table 8._ Decision-making performance comparison on the Senna nuScenes benchmark. 

|**Model**|Fine-tuned|**Accuracy (%)**|
|---|---|---|
|Senna|✓|88.47|
|AutoMoT (Ours)|✓|**90.92**|


### **A.3. Impact of Individual Component** 

In this section, we conduct additional ablation studies to systematically analyze the contributions of individual components in AutoMoT, including the understanding expert, decision-making module (meta-action planning), and the asynchronous inference mechanism, with respect to overall driving performance. For consistency, all experiments are performed on the nuScenes benchmark, using the official trajectory planning metrics and average accuracy for decision-making evaluation. 

_Table 9._ Ablation study on the understanding and decision-making components of AutoMoT. AutoMoT-R denotes the variant with a randomly initialized VLM backbone. AutoMoT-P denotes the planning-only variant, where the action expert is trained without the decision-making (meta-action planning) objective. 

|Method|L2@1s_↓_|L2@2s_↓_|L2@3s_↓_|L2_avg ↓_|
|---|---|---|---|---|
|AutoMoT (Ours)|0.14|0.29|0.54|0.32|
|AutoMoT-R (w/o Pre-trained UE)|0.16|0.33|0.60|0.36|
|AutoMoT-P (w/o decision-making)|0.14|0.30|0.58|0.34|


**Impact of the Understanding Expert.** To assess the importance of preserving the general intelligence of the VLM backbone, we replace the pre-trained Qwen3-VL-4B in the understanding expert with a randomly initialized counterpart and train it E2E on the trajectory planning task. As shown in Table 9, this from-scratch variant exhibits substantial performance drops across all planning horizons, indicating that the general-purpose knowledge and reasoning capabilities provided by the pre-trained understanding expert are crucial for stable and accurate planning. Notably, the degradation becomes more pronounced at longer horizons, suggesting that long-horizon trajectory planning relies heavily on high-quality scene understanding. 

**Impact of the Decision-Making.** In this ablation study, we keep all components unchanged but remove the decisionmaking objective from the action expert (AE), training it solely on trajectory planning to quantify the contribution of decision-making to overall driving performance. Quantitative results are reported in Table 9. Removing decision-making consistently degrades performance across all prediction horizons, with the average L2 displacement increasing to 0.34. 

### **A.4. Inference Latency Comparisons** 

In this section, we compare AutoMoT against existing VLA baselines (Table 10) to further confirm the superiority of our method in terms of inference latency. Prior VLA-based systems operate at substantially lower frequencies, with reported inference latencies of 7683 ms for OpenEMMA, 1072 ms / 10518 ms for AutoVLA in fast / slow modes, and 430 ms for SimLingo. In contrast, AutoMoT achieves 117 ms under synchronous inference and 37 ms under asynchronous inference, corresponding to 8.5 Hz and 27 Hz, respectively. This yields an order-of-magnitude improvement in inference efficiency over existing VLA-based approaches. The gain is enabled by decoupling reasoning and action generation through asynchronous execution with KV-cache reuse: reasoning is updated at a lower frequency, while action generation runs at a higher frequency, avoiding redundant full-model inference. Compared with synchronized VLA formulations, AutoMoT substantially reduces 

14 

**AutoMoT: An Asynchronous VLA Model for E2E Autonomous Driving** 

unnecessary computation and better aligns with the real-time requirements of autonomous driving, making VLA-based end-to-end systems more practical for onboard deployment. 

_Table 10._ Inference latency comparison of VLA-based driving methods.<sup>†</sup> Results are cited from the original paper, as public checkpoints are not available for reproduction. The inference GPU is not specified; training uses 8 _×_ NVIDIA L40S. 

|**Method**|**GPU**|**Latency (ms)**|**Hz**|
|---|---|---|---|
|OpenEMMA|RTX 5090|7,683|0.13|
|AutoVLA<sup>† </sup>(fast)|Unknown|1,072|0.93|
|AutoVLA<sup>† </sup>(slow)|Unknown|10,518|0.10|
|SimLingo|RTX 5090|430|2.3|
|AutoMoT-S (sync)|RTX 5090|117|8.5|
|AutoMoT (async)|RTX 5090|**37**|**27**|


15 

