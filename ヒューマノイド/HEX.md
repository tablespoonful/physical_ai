---
title: "HEX: Humanoid-Aligned Experts for Cross-Embodiment Whole-Body Manipulation"
date: "2026-04-09"
authors: "Shuanghao Bai; Meng Li; Xinyuan Lv; Jiawei Wang; Xinhua Wang; Fei Liao"
url: https://arxiv.org/abs/2604.07993
pdf: https://arxiv.org/pdf/2604.07993
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.07993)** / [論文ページ](https://arxiv.org/abs/2604.07993)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。



# **HEX: Humanoid-Aligned Experts for Cross-Embodiment Whole-Body Manipulation** 

Shuanghao Bai<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> Meng Li<sup>1</sup><sup>_∗†_</sup> Xinyuan Lv<sup>1</sup><sup>_,_3</sup> Jiawei Wang<sup>1</sup><sup>_,_3</sup> Xinhua Wang<sup>1</sup> Fei Liao<sup>1</sup> Chengkai Hou<sup>1</sup><sup>_,_4</sup> Langzhe Gu<sup>1</sup><sup>_,_4</sup> Bowei Zhang<sup>1</sup><sup>_,_3</sup> Wanqi Zhou<sup>2</sup> Kun Wu<sup>1</sup> Ziluo Ding<sup>1</sup> Zhiyuan Xu<sup>1</sup> Lei Sun<sup>3</sup> Shanghang Zhang<sup>4</sup> Zhengping Che<sup>1</sup><sup>_‡_</sup> Jian Tang<sup>1</sup><sup>_‡_</sup> Badong Chen<sup>2</sup><sup>_‡_</sup> 

1Beijing Innovation Center of Humanoid Robotics 2Xi’an Jiaotong University 3Nankai University 4Peking University 

> _∗_ Equal Contribution _†_ Project Lead _‡_ Corresponding Author 

Humans achieve complex manipulation through coordinated whole-body control, whereas most VisionLanguage-Action (VLA) models treat robot body parts largely independently, making high-DoF humanoid control challenging and often unstable. We present HEX, a state-centric framework for coordinated manipulation on full-sized bipedal humanoid robots. HEX introduces a humanoid-aligned universal state representation for scalable learning across heterogeneous embodiments, and incorporates a Mixture-of-Experts Unified Proprioceptive Predictor to model whole-body coordination and temporal motion dynamics from large-scale multi-embodiment trajectory data. To efficiently capture temporal visual context, HEX uses lightweight history tokens to summarize past observations, avoiding repeated encoding of historical images during inference. It further employs a residual-gated fusion mechanism with a flow-matching action head to adaptively integrate visual-language cues with proprioceptive dynamics for action generation. Experiments on real-world humanoid manipulation tasks show that HEX achieves state-of-the-art performance in task success rate and generalization, particularly in fast-reaction and long-horizon scenarios. 

**Website:** https://hex-humanoid.github.io/ 

**Github:** https://github.com/Open-X-Humanoid/HEX 


## **1 Introduction** 

Humanoid robots hold the promise of bringing embodied intelligence into complex human environments such as homes and schools. Existing research, however, has largely focused on either locomotion, which enables robots to navigate unstructured environments [38, 40, 44], or hand-centric manipulation, where the lower body remains fixed and control is limited to the arms and hands [25, 61]. In contrast, humans routinely perform tasks that require simultaneous locomotion and manipulation, leveraging coordinated motion of the entire body. Enabling such whole-body manipulation in humanoids remains significantly underexplored. The challenge is fundamental: the robot must maintain dynamic balance while producing high-dimensional, tightly coupled motions across multiple limbs during object interaction. 

Existing approaches to humanoid whole-body manipulation mainly follow two paradigms. The first adopts an explicitly decomposed design, in which locomotion or navigation and manipulation are controlled by separate policies [55]. While such decomposition simplifies learning and control, it relies heavily on manual task priors and interface design, and becomes increasingly brittle as task complexity grows. Errors can also accumulate across modules, making tightly coupled behaviors, such as manipulation during locomotion, difficult to achieve robustly. A more recent trend is to adopt a hierarchical design, where the high-level module produces task-relevant commands, such as arm and hand actions [23, 33] or corresponding hand-eye targets [8], while a low-level whole-body controller refines them into high-frequency, balance-preserving motions. 

In parallel, recent Vision-Language-Action (VLA) models have introduced stronger visual-semantic understanding 

1 


**Figure 1. Overview of HEX.** (a) HEX is, to the best of our knowledge, the first whole-body VLA framework for full-sized bipedal humanoid robots, pretrained on diverse cross-embodiment humanoid trajectory data. (b) HEX combines a high-level VLA module with a low-level whole-body controller for coordinated action generation and balance-preserving execution. (c) We evaluate HEX on TianGong 2.0 and TianGong 3.0 across whole-body, long-horizon, and fast-reaction tasks, demonstrating strong performance across diverse manipulation scenarios. 

and reasoning through large vision-language models, showing promising scalability and generalization [10, 14, 22, 24]. As a result, recent humanoid systems increasingly adopt VLA-style high-level planners together with low-level wholebody controllers for stable execution [5, 23, 33, 50]. Despite these advances, most existing VLA-based approaches remain insufficiently structured for humanoid whole-body manipulation. In many cases, actions are predicted over high-dimensional joints or latent commands without explicitly modeling how body parts interact through shared balance and posture. As a result, the policy may capture task intent semantically, yet still fail to produce coordinated wholebody behavior, especially in fast-reaction and long-horizon scenarios where temporal consistency and whole-body coordination are essential. 

To address this limitation, we propose **HEX** , a framework built on the key insight that effective humanoid whole-body manipulation requires both embodiment-aware predictive dynamics and temporally grounded scene understanding, as shown in Figure 1. Specifically, HEX introduces a humanoid-aligned universal state representation that provides a structured basis for modeling whole-body proprioceptive dynamics across different body parts and embodiments. 

2 

Built upon this representation, HEX captures temporal motion evolution and whole-body coordination in proprioceptive space, enabling scalable predictive modeling for heterogeneous humanoid trajectories. Whole-body manipulation also depends on temporal visual context, especially when object motion, scene evolution, or partial observability makes the current observation insufficient. To this end, HEX summarizes past visual-language context into compact representations while leveraging predictive proprioceptive dynamics to provide state foresight. Together, these designs form a _review-and-forecast_ paradigm, where past visual context supports scene understanding and future state prediction supports coordinated whole-body control. The resulting visual-language and predictive state representations are then adaptively fused for action generation, producing smooth and coordinated whole-body behaviors. 

We evaluate HEX on a diverse set of real-world humanoid manipulation tasks against strong VLA and imitation learning baselines, including ACT [66], SwitchVLA [26], GR00T N1.5 [5], Π0 _._ 5 [22], and _ψ_ 0 [50]. Across a wide range of task settings, HEX consistently achieves higher task success rates and stronger generalization. The improvements are particularly pronounced in fast-reaction and long-horizon scenarios, where coordinated whole-body dynamics and temporal consistency are critical. In summary, our contributions are fourfold. First, to the best of our knowledge, we present the first whole-body VLA framework for full-sized bipedal humanoid robots. Second, we propose a crossembodiment humanoid-aligned state representation with predictive proprioceptive modeling for scalable whole-body pretraining. Third, we introduce a review-and-forecast paradigm that combines visual history summarization, future state prediction, and adaptive multimodal fusion for action generation. Finally, extensive experiments on real-world humanoid manipulation benchmarks demonstrate state-of-the-art performance and validate HEX as an effective framework for coordinated whole-body manipulation. 

## **2 Related Work** 

### **2.1 Learning-based Humanoid Whole-body Control** 

Learning-based humanoid whole-body control has been primarily advanced through reinforcement learning (RL) and imitation learning (IL) [4, 27, 29, 62]. Early RL-based methods such as DeepMimic [40] and AMP [41] established motion-tracking and motion-prior-based policy learning as effective paradigms for acquiring robust and natural humanoid skills. More recent work has extended this line toward real-world, contact-rich, and visually grounded whole-body control, including simulation-pretrained latent action learning for real-world RL [20], force-adaptive loco-manipulation [65], highly dynamic full-body skill learning [54], large-scale motion-tracking controllers with strong generalization [36], and visual sim-to-real humanoid loco-manipulation via privileged RL and teacher–student policy distillation [18]. In parallel, imitation learning has emerged as an efficient alternative by leveraging human demonstrations, teleoperation trajectories, and motion priors. Recent approaches explore human-to-humanoid imitation from teleoperation or egocentric demonstrations [15, 17, 43], unified motion-tracking and predictive motion priors [9, 34], as well as generative imitation with diffusion-based policies [31, 63]. Despite their success, these methods are primarily designed for skill imitation or task-specific control, and generally provide limited semantic understanding of instructions, goals, and visual context. 

More recently, vision-language-action (VLA) models, empowered by the strong visual-semantic understanding and reasoning capabilities of large vision–language models and their potential to scale to more general scenarios [2, 3, 7, 46, 49], have begun to extend from fixed-base manipulation to humanoid whole-body control. Humanoid-VLA [11] introduces visual integration for humanoid control, while GR00T N1 [5] and Ψ0 [50] move toward generalist humanoid foundation models trained on large-scale heterogeneous data. To better handle whole-body behaviors, LeVERB [57] proposes hierarchical latent vision-language instructions, WholeBodyVLA [23] explores unified latent VLA control for loco-manipulation, and TrajBooster [33] improves downstream adaptation through trajectory-centric retargeting. More recent approaches explore complementary strategies: OpenHLM [21] investigates whole-body teleoperation and heterogeneous co-training, VLK [48] leverages synthetic interactions in reconstructed scenes, HALOMI [67] incorporates active perception and human demonstrations, and HAF [16] combines hierarchical action flow with latent reinforcement learning. In parallel, world-action models (WAMs) have emerged as an alternative paradigm for coupling predictive dynamics with whole-body action generation. MotionWAM [69] exploits video-model features and unified motion representations for real-time loco-manipulation, while _ω_ -0 [28] integrates latent future-observation prediction with whole-body action generation. Two recent WholeBodyWAM approaches further investigate scalable motion priors [64] and pretrained world-action priors with whole-body-controller-grounded coordination [30], respectively. 

3 

Complementary to these advances in data-driven adaptation, action generation, and predictive modeling, our work focuses on explicitly capturing structured proprioceptive dependencies through humanoid-aligned state representations and joint past-future temporal modeling, coupling visual-language reasoning with embodiment-aware representations for coordinated whole-body control. 

### **2.2 Cross-Embodiment Learning for Humanoid Robots** 

Cross-embodiment learning seeks to transfer knowledge across agents with different morphologies by learning shared behavior representations, aligned control spaces, or generalizable pretrained policies [12, 47, 60]. One line of work focuses on _human-to-humanoid learning_ , where human videos or egocentric demonstrations are used as scalable supervision for humanoid control [37, 43, 45, 50, 51, 59]. Representative examples include Mao et al. [37], which leverage large-scale human videos for humanoid pose control, Humanoid Policy _∼_ Human Policy [43], which aligns egocentric human demonstrations with humanoid behaviors in a unified policy space, and Ψ0 [50], which incorporates human egocentric videos into a staged humanoid foundation-model training recipe. Another line studies _robot-tohumanoid_ or _cross-humanoid learning_ , where policies or representations are transferred across heterogeneous robotic embodiments [5, 32, 35, 39, 42, 58, 61]. Representative works include H-Zero [32], which enables few-shot transfer to novel humanoids through cross-humanoid pretraining, EAGLE [39], which learns a unified controller across diverse humanoid embodiments, and GR00T N1 [5], which scales humanoid foundation modeling with heterogeneous robot trajectories, human videos, and synthetic data. 

Similar in spirit, HEX also targets cross-embodiment humanoid learning, but differs from prior works by introducing a compositional and humanoid-aligned proprioceptive modeling framework. Its Unified Proprioceptive Predictor with Mixture-of-Experts (MoE) operates on canonical body-part abstractions, allowing heterogeneous trajectories from the same embodiment or different humanoids to be encoded in a shared latent space without retraining a monolithic state encoder for every new joint configuration or missing-part setting. By combining reusable part-level encoders with dynamic expert routing, HEX more efficiently exploits both intra- and cross-embodiment data, while capturing structured whole-body and temporal dependencies for coordinated whole-body control. 

## **3 Method** 

### **3.1 Overview** 

HEX adopts a hierarchical architecture for humanoid whole-body manipulation, consisting of a high-level VLA policy and a low-level RL-based whole-body controller. The high-level policy takes visual-language context together with humanoid-aligned proprioceptive states as input and produces task-conditioned outputs. Specifically, it directly predicts upper-body manipulation actions for the arms and hands, while simultaneously generating lower-body commands for the whole-body controller. These commands specify both the motion mode, such as standing, walking, or kneeling, and the desired motion within each mode. The low-level controller operates at a higher control frequency and translates these commands into dynamically stable joint-level motions while maintaining balance through state feedback. 

The high-level VLA policy in HEX consists of three main components. First, a Visual-Language Model (VLM) module encodes current visual-language context together with lightweight temporal review cues. Second, a Unified Proprioceptive Predictor (UPP) models humanoid-aligned state dynamics and captures whole-body interactions through predictive proprioceptive modeling. Third, an action expert integrates visual-language and proprioceptive features through adaptive fusion to generate the final high-level action. Figure 2 provides an overview of the full framework. For the low-level controller, we instantiate skill-specific RL policies trained with motion-guided objectives. These policies share a unified command interface, allowing the high-level VLA to select the appropriate motion regime and specify the desired lower-body motion through the same control interface. In particular, the standing and walking controllers are trained with a DeepMimic-style reference-tracking formulation [40], which is well suited to stable periodic or quasi-static motions with clear target kinematics. In contrast, the half-kneeling controller is trained with an AMP-style objective [41], where an adversarial motion prior encourages natural contact-rich posture transitions without requiring strict frame-wise tracking to a single reference trajectory. In the following, we present the core components of the high-level VLA policy in HEX. 

4 


**Figure 2. Overview of the proposed high-level VLA policy in HEX.** Given a language instruction _L_ , the current visual observation _Vt_ , and a history query token _Qt_ , the VLM encodes visual-language context together with lightweight temporal review cues summarized in a history cache. In parallel, humanoid-aligned proprioceptive states are organized into structured part-aware tokens and processed by a MoE-based Unified Proprioceptive Predictor, which captures whole-body interactions and forecasts future state dynamics. The resulting visual-language and predictive proprioceptive features are then integrated by the HEX Action Expert through adaptive fusion for action generation, producing task-relevant high-level actions over the prediction horizon. 

### **3.2 VLM with History Query Feature Cache** 

To incorporate temporal visual-language context without repeatedly encoding long image histories, we introduce a lightweight history query feature cache. At each timestep _t_ , we encode the language instruction, the current visual observation, and a query token using a single vision–language model (VLM). Specifically, we concatenate the language tokens **L** , visual tokens **V** _t_ extracted from observation **o** _t_ , and a query token **Q** _t_ , and feed them into the VLM: 


The resulting query feature **Q**<sup>_′_</sup> _t_<sup>servesasacompactsummaryofthecurrentvisual-languagecontext.Ratherthan</sup> propagating the query token itself across time, we generate a fresh query feature at every timestep and store it in a fixed-length cache: 


where _τv_ denotes the visual history window, set to 2 in all experiments. This cache stores only compact query features, rather than the original images or full VLM activations. Together with the current-step visual-language features **L**<sup>_′_</sup> _t_<sup>and</sup> **V** _t_<sup>_′_,</sup><sup>_M_vl</sup> _t_<sup>provides recent semantic context for the subsequent proprioceptive modeling and action generation modules.</sup> 

This design provides an efficient form of visual review: temporal scene information is preserved through a compact feature memory, while the VLM itself remains a single-step feed-forward encoder applied only to the current frame. As a result, HEX can exploit temporal visual context without incurring the substantial cost of repeatedly encoding long visual histories. 

### **3.3 UPP with Morphology-based MoE** 

Humanoid proprioceptive states comprise heterogeneous signals, including whole-body joint positions, velocities, accelerations, and tactile feedback. As sensing capabilities expand, policies must capture both these signals and their interactions across body parts to support coordinated whole-body control. 

To enable cross-embodiment learning, we organize proprioceptive states into canonical body-part slots, including left/right arms, left/right hands, left/right legs, head, waist, and an auxiliary others slot. This decomposition follows two considerations. First, it preserves body-part-specific motion characteristics before cross-part interactions are modeled by UPP. Second, the fine-grained partition facilitates cross-embodiment adaptation by localizing embodiment-specific variations. For example, humanoid platforms may share similar arm structures while employing substantially different end-effectors, such as dexterous hands or parallel grippers. Separating arms from hands therefore allows transferable arm representations to be preserved when only the end-effector changes, whereas merging them would entangle these variations within a single representation. Although we use this set of canonical slots in the current work, the formulation is readily extensible to richer or more fine-grained body-part decompositions. 

5 


**Figure 3. Left and middle: Unified Proprioceptive Predictor (UPP).** Morphology-based proprioceptive states are first mapped into canonical body-part tokens and augmented with learnable future query tokens. These spatio-temporal tokens are processed by a shared transformer backbone sandwiched by morphology-aware MoE adaptation modules, yielding future proprioceptive latents **H**<sup>_p_</sup> . The middle panel details the morphology-aware MoE, where flattened part-time tokens are routed by a learned top- _k_ gate to a set of routed experts, while a shared expert provides a common transformation across all tokens. This design enables token-wise specialization for embodiment- and part-dependent variations while preserving reusable dynamics across embodiments. **Right: Action Expert.** Noisy action tokens are encoded and conditioned on both visual-language features **H**<sup>_V L_</sup> and predicted proprioceptive features **H**<sup>_p_</sup> through dual cross-attention. A learned gate adaptively injects the state branch on top of the visual-language branch, followed by self-attention and feed-forward refinement. The resulting denoised features are decoded into high-level actions for arm and hand control and for downstream whole-body execution. 

For an embodiment _e_ , the raw proprioceptive state **s**<sup>(</sup> _t_<sup>_e_)</sup> may vary in dimensionality and composition. We first partition **s**<sup>(</sup> _t_<sup>_e_)</sup> into the available body-part observations. Each body part is then processed by a lightweight proprioceptive encoder and projected into the same _d_ -dimensional latent space. For unavailable body parts, the latent is replaced by a learned missing-part token. The resulting body-part latent tokens are concatenated to form the structured representation 


where _P_ denotes the number of canonical part slots and _d_ is the latent dimension. This enables prediction in a shared latent space rather than the raw embodiment-specific state space. 

While part-aligned representations accommodate heterogeneous states, whole-body prediction also requires modeling temporal evolution and cross-part interactions. HEX therefore employs a Unified Proprioceptive Predictor (UPP), illustrated in Figure 3(a), to capture these dependencies. We concatenate the current part tokens with learnable future query tokens **N** _t_ +1: _t_ + _τp_ , where _τp_ denotes the prediction horizon, and add temporal and part positional embeddings to form a spatio-temporal token sequence. 

To better accommodate embodiment- and token-specific variations while preserving a shared predictive backbone, UPP incorporates two lightweight morphology-aware MoE modules: an input-side MoE before the shared transformer predictor and an output-side MoE after it. As shown in Figure 3(a), each flattened spatio-temporal token is routed by a learned top- _k_ gate to selected experts, alongside a shared expert branch. The routed expert outputs are weighted and combined with the shared expert output. This enables specialization in embodiment- and part-specific dynamics while preserving reusable knowledge across embodiments. The MoE modules thus provide lightweight token-level adaptation around the shared transformer backbone. 

Between the input-side and output-side MoE adaptation modules, a shared transformer backbone models embodimentagnostic temporal dynamics in the latent space. The backbone processes the part-time tokens using interleaved selfattention and visual-language-conditioned attention to capture cross-part dependencies and task-relevant dynamics. Conditioned on the current proprioceptive latent **P** _t_ , language and visual features **L**<sup>_′_</sup> _t_<sup>and</sup><sup>**V**</sup> _t_<sup>_′_,andvisual-language</sup> 

6 

history cache _M_<sup>vl</sup> _t_<sup>, UPP predicts future proprioceptive latents over a horizon</sup><sup>_τp_:</sup> 


The predicted latents capture short-horizon whole-body evolution and provide future-oriented proprioceptive cues for downstream action generation. 

### **3.4 Action Expert with Adaptive Fusion** 

As shown in Figure 3 (b), the action expert generates high-level actions by iteratively denoising action tokens with noise under dual conditioning from visual-language and proprioceptive features. Unlike direct fusion between the two modalities, our action expert uses the evolving action representation itself as the query, and conditions it on both the VLM outputs and the UPP outputs through two parallel cross-attention branches. This design allows action generation to be guided jointly by motion-level vision-semantic context and future-oriented proprioceptive dynamics. 

Let **X** _t_ denote the current action hidden states at diffusion step _t_ , let **H**<sup>_vl_</sup> _t_<sup>= [</sup><sup>**L**</sup><sup>_′_</sup> _t_<sup>_,_</sup><sup>**V**</sup> _t_<sup>_′, Mt_] denote the full set of VLM</sup> features from the last layer, and let **H**<sup>_p_</sup> _t_<sup>=</sup><sup>**P**</sup><sup>_t_:</sup><sup>_t_+</sup><sup>_τ_</sup> _p_<sup>denote the proprioceptive features produced by UPP. Action Expert</sup> first normalizes the current action states, 


and then applies two cross-attention operations in parallel: 


where the action states serve as queries, while the visual-language and proprioceptive features serve as two conditioning memories. To combine the two conditioning branches, Action Expert uses a gated fusion mechanism conditioned on both cross-attended features and the current normalized action states: 


where _σ_ ( _·_ ) is the sigmoid function. The fused conditioning signal is then computed as 


and injected into the action states through a residual update: 


After this dual-conditioning stage, Action Expert further applies self-attention and a feed-forward block to refine the action representation. In this way, the visual-language branch provides semantic and motion-relevant guidance for task execution, while the proprioceptive branch injects future-oriented whole-body dynamics and whole-body coordination cues. The gate adaptively modulates the contribution of the state branch during denoising, enabling the model to generate high-level actions that directly control the arms and hands while remaining consistent with downstream whole-body execution. 

### **3.5 Cross-Embodiment Training** 

We pretrain HEX on trajectory datasets collected from multiple humanoid embodiments, covering diverse kinematics, dynamics, and embodiment-specific state-action spaces. Training jointly optimizes an action-generation objective for the action expert and an auxiliary future-state prediction objective for the Unified Proprioceptive Predictor. 

For action generation, we adopt a flow-matching objective. Given a clean future action trajectory **A** _t_ : _t_ + _τa_ and Gaussian noise **N** of the same shape, we construct a noisy action trajectory 


7 

and define the corresponding velocity target as 


Let **Z**<sup>_a_</sup> _t_<sup>denotethefinalhiddenrepresentationproducedbytheActionExpert,andlet</sup><sup>**P**</sup><sup>_t_+1:</sup><sup>_t_+</sup><sup>_τ_</sup> _p_<sup>denotethefuture</sup> proprioceptive latents predicted by UPP. The action decoder _Da_ ( _·_ ) maps **Z**<sup>_a_</sup> _t_<sup>to velocity predictions, while the state</sup> decoder _Ds_ ( _·_ ) maps **P** _t_ +1: _t_ + _τp_ to future proprioceptive states. Let **s** _t_ +1: _t_ + _τp_ denote the corresponding ground-truth future proprioceptive trajectory. We then define the training objectives as 


where _La_ supervises high-level action denoising under dual conditioning from visual-language and proprioceptive features, while _Ls_ encourages UPP to model short-horizon proprioceptive evolution in the shared latent space. Because both objectives are defined over the shared body-part-aligned representation, the same training formulation naturally extends across heterogeneous humanoid embodiments. In practice, we optionally adopt a staged schedule for optimization stability: we first warm up UPP using _Ls_ , and then jointly optimize UPP and the Action Expert under the combined objective. 

## **4 Experiments** 

We conduct extensive experiments on real-world humanoid whole-body manipulation to evaluate the effectiveness, generalization ability, and practical behavior of HEX. In particular, we aim to answer the following four questions: 

- **RQ1:** To what extent does HEX improve performance over strong state-of-the-art baselines on real-world humanoid whole-body manipulation, particularly in seen and long-horizon settings? (Section 4.2) 

- **RQ2:** How effectively does HEX generalize under unseen scene variations? (Section 4.3) 

- **RQ3:** What is the effect of each major component in HEX on the overall performance? (Section 4.4) 

- **RQ4:** What insights can be drawn from HEX regarding expert routing behavior, inference efficiency, and failure modes? (Section 4.5) 

### **4.1 Experiment Setup** 

**Hardware and data collection.** As shown in Figure 4, we adopt a modular teleoperation pipeline for data collection. Head motion is controlled by computer-issued commands that regulate upward and downward pitch under a fixed data collection protocol. Arm _Data Collection Setup Arm & Hand_ and hand motions are teleoperated through an isomorphic arm–hand interface [56], while waist and leg motions are controlled using a handheld joystick. To evaluate cross-embodiment capability, we use two humanoid platforms, TianGong 2.0 and TianGong 3.0. Our data collection procedure follows RoboMIND [19, 52]. Kinematically Matched 


**Baselines.** To ensure a fair comparison of high-level VLA policies, we use the same RL-based low-level controller for balance control across all methods, thereby isolating the contribution of the high-level policy. All models receive the same visual observations, robot proprioceptive information, and language instructions, while preserving their original input encoding and fusion mechanisms. We compare HEX with the following IL and VLA baselines. Unless otherwise specified, all remaining hyperparameters follow the original implementations. 

**Figure 4.** Hardware setup for real-robot teleoperation data collection. 

ACT [66] is a small-scale vision–action model that combines a Transformer encoder–decoder with action chunking. We set the action horizon to 200 and train it for 35k steps on 8 NVIDIA A100 GPUs with a per-GPU batch size of 64. 

8 

SwitchVLA [26] is a medium-scale VLA framework for execution-aware task switching under changing instructions. We set the action horizon to 200 and train it for 100 epochs on 8 NVIDIA A100 GPUs with a per-GPU batch size of 200. 

GR00T N1.5 [5] is a large-scale humanoid VLA model trained on both real-world teleoperation and large-scale simulated data. It predicts action sequences from the final-layer VLM features. We set the action horizon to 100 and train it for 50k steps on a single NVIDIA A100 GPU with a batch size of 64. 

_π_ 0 _._ 5 [22] is a large-scale general-purpose robot foundation model in which the VLM and action expert share the same attention backbone. We set the action horizon to 100 and train it for 50k steps on 8 NVIDIA A100 GPUs with a per-GPU batch size of 8. 

_ψ_ 0 [50] freezes a pretrained vision-language model and trains a separate flow-matching action expert. We set the action horizon to 30 and train it for 50k steps on 8 NVIDIA A100 GPUs with a batch size of 8. 

**Pretraining Datasets.** As shown in Figure 1 (a), our training corpus comprises over 12M frames collected from seven humanoid embodiments across four data sources. First, our in-house HEX dataset contains approximately 4M frames from three embodiments: the legged humanoids TianGong 2.0 and TianGong 3.0, and the wheeled humanoid TianYi. Owing to differences in data collection protocols and system versions, the state and action definitions are not fully consistent across embodiments. For example, the state of TianGong 2.0 includes upper- and lower-body proprioceptive signals, while TianGong 3.0 may additionally incorporate IMU measurements and hand tactile signals. Second, the Humanoid Everyday dataset [68] provides approximately 3.4M frames from the legged humanoids Unitree G1 and H1. Its state representation includes both upper- and lower-body information, whereas the action space contains only upper-body actions. Third, AgiBot World Colosseo [6] contributes 3.8M frames from a wheeled AgiBot humanoid platform. We use its G1-retargeted version [33], in which the original actions are transformed into a format executable by legged humanoids. Finally, we include 2.3M frames from the Leju legged humanoid subset of RoboCOIN [53]. Although these datasets differ substantially in embodiment, state composition, and action parameterization, they can all be leveraged for pretraining within our cross-embodiment architecture. 

**Implementation Details.** HEX is built on the vision-language model Qwen3-VL-2B-Instruct [1]. The UPP is a 4-layer transformer with hidden size 768, forecasting a 50-step future state horizon. To model embodiment-specific dynamics, we employ a MoE module [13] with 16 routed experts and 2 shared experts, using top-1 softmax routing and an auxiliary load-balancing loss with weight 0.01. The action head is a 16-layer DiT-B with hidden size 1024, which predicts 100-step action chunks conditioned on visual–language features and predicted future states. During pretraining, HEX is trained for 200k steps with a per-device batch size of 16 and an action chunk size of 100, requiring approximately 1K A100 GPU hours. Optimization is performed using AdamW, with learning rates of 1 _._ 0 _×_ 10<sup>_−_5</sup> for the VLM and 2 _._ 0 _×_ 10<sup>_−_5</sup> for both the UPP and action modules. We adopt a cosine learning rate schedule with a minimum learning rate of 10<sup>_−_6</sup> , using 5k warmup steps for the main model and 2k warmup steps for the UPP model. For fine-tuning, each task is trained for 20k steps using AdamW. The learning rate is set to 1 _._ 0 _×_ 10<sup>_−_5</sup> for the Qwen-VL interface and 4 _._ 0 _×_ 10<sup>_−_5</sup> for both the UPP and action modules. The warmup steps for the UPP model are reduced to 1k. 

During inference, linear interpolation is applied only to the directly predicted arm and hand actions to improve motion smoothness. Lower-body outputs instead serve as commands to the RL-based whole-body controller, which performs closed-loop control and dynamic stabilization at a higher control frequency. We therefore do not additionally interpolate these commands, avoiding unnecessary latency that could reduce responsiveness during balance and locomotion. 

**Metric.** For real-world evaluation, task success rate (SR) is used to measure strict end-to-end task completion. However, for long-horizon tasks, binary SR cannot distinguish failures occurring at different intermediate stages. To provide a more fine-grained evaluation, a Stage-wise Progress Score (SPS) is additionally introduced to quantify partial task completion. Specifically, each long-horizon task is decomposed into _K_ ordered semantic stages, with a predefined weight _wk_ assigned to stage _k_ . Let _Ii,k_ = 1 if evaluation episode _i_ successfully completes stage _k_ , and 0 otherwise. SPS is defined as 


where _N_ denotes the number of evaluation episodes. SPS ranges from 0 to 100, assigning partial credit to completed intermediate stages, while SR measures strict end-to-end success. The stage definitions and weights are fixed for each task and applied identically to all evaluated methods. 

9 

**Table 1.** Task success rates (%) of different methods on TianGong 3.0 and TianGong 2.0 tasks. The icons denote the main body parts involved in control for each task: arm ( ), hand ( ), waist ( ), and leg ( ). 

||||TianGong 3.0 (<br>)|TianGong 3.0 (<br>)|TianGong 3.0 (<br>)|
|---|---|---|---|---|---|
|Method|Para.|Avg (%)|Kneel and manipulate<br>the objects|Tidy Table|Bring box and<br>pack all objects|
|ACT [66]|80M|57.1|83.3|8.3|8.3|
|SwitchVLA [26]|0.3B|40.5|0.0|8.3|0.0|
|GR00T N1.5 [5]|3B|70.2|100.0|41.7|33.3|
|_π_0_._5 [22]|3.3B|71.8|100.0|35.7|25.0|
|_ψ_0 [50]|–|77.4|100.0|41.7|33.3|
|HEX|2.4B|**79.8**|100.0|41.7|41.7|
|Method|Para.|TianGong 2.0 (<br>)|TianGong 2.0 (<br>)|TianGong 2.0 (<br>)|TianGong 2.0 (<br>)|
|||Mirror the human’s pose|Pour liquor while<br>following the human order|Human assistant|Walking while<br>avoiding obstacles|
|ACT [66]|80M|83.3|83.3|66.7|66.7|
|SwitchVLA [26]|0.3B|100.0|41.7|58.3|75.0|
|GR00T N1.5 [5]|3B|83.3|66.7|66.7|100.0|
|_π_0_._5 [22]|3.3B|83.3|91.7|75.0|91.7|
|_ψ_0 [50]|2.5B|100.0|91.7|75.0|100.0|
|HEX|2.4B|100.0|91.7|83.3|100.0|


The stage definitions and weights are fixed for each task and applied identically to all methods. Specifically, _Basket transfer from bed to table_ , _Toy transfer to cart basket_ , and _Long-horizon box convey_ each comprise four stages: grasping, turning, locomotion, and placement, with weights (3 _,_ 2 _,_ 3 _,_ 2), (3 _,_ 2 _,_ 4 _,_ 3), and (3 _,_ 2 _,_ 4 _,_ 3), respectively. _Pouring_ comprises five stages: grasping, pouring into three cups, and returning the arm, with weights (3 _,_ 3 _,_ 3 _,_ 3 _,_ 2). 

### **4.2 Comparing with SoTA** 

#### **4.2.1 Seen Scenarios** 

Seen scenarios refer to evaluation settings where the test environments closely match those in the training data. This setting primarily assesses the ability of VLA models to reproduce demonstrated trajectories from observations. All methods are evaluated over 12 trials. 

**Post-training Datasets.** We collect seven real-robot tasks in total, including four on Tiangong 2.0 and three on Tiangong 3.0. These tasks cover whole-body control involving the arms and hands, waist, and legs, as well as multiple scenarios requiring timely human-robot interaction, enabling evaluation of both task success rate and response speed across different VLA models. The seven tasks are as follows. 

Task 1: Mirror the human’s pose. The robot observes a person standing in front of it and imitates the posed gestures, including “V,” “L,” and “A,” in real time. We collect 108 trajectories for training. 

Task 2: Pour liquor while following human order. A liquor bottle and three cups are placed on the table in front of the robot. The robot pours liquid into the cup indicated by the human’s pointing. We collect 100 trajectories for training. 

Task 3: Human assistant. The robot carries a box and follows a human collaborator to assist with organizing objects across two tables. We collect 98 trajectories for training. 

Task 4: Walking while avoiding obstacles. As the robot walks forward, it must stop promptly when a person or cart passes through its path, and then resume walking once the path is clear. We collect 100 trajectories for training. 

Task 5: Kneel and manipulate the objects. The robot kneels down to pick up blocks and place them into a box. We collect 300 trajectories for training. 

Task 6: Tidy table. The robot clears the tabletop by sorting scattered objects into a box and disposing of paper scraps into a trash bin. We collect 100 trajectories for training. 

10 

**Table 2.** Task success rate (SR, %) and stage-wise progress score (SPS) of different methods on three long-horizon whole-body manipulation tasks. 

|Method|Para.|TianGong 2<br>Long-horiz|.0 (<br>)<br>on box convey|Basket transf|TianGong 3.0 (<br>er from bed to table|)<br>Toy transfer|to cart basket|
|---|---|---|---|---|---|---|---|
|||SR (%)|SPS|SR (%)|SPS|SR (%)|SPS|
|ACT [66]|80M|26.7|55.6|6.7|18.9|0.0|18.0|
|SwitchVLA [26]|0.3B|13.3|42.8|0.0|5.0|0.0|16.0|
|GR00T N1.5 [5]|3B|20.0|47.8|60.0|70.0|33.3|56.7|
|_π_0_._5 [22]|3.3B|40.0|76.1|46.7|62.2|60.0|77.3|
|_ψ_0 [50]|2.5B|46.7|75.6|46.7|67.2|60.0|74.0|
|HEX|2.4B|**53.3**|**79.4**|**73.3**|**83.9**|**86.7**|**92.0**|


Task 7: Bring box and pack all objects. The robot first retrieves a box and then packs all target objects into it. We collect 100 trajectories for training. 

**Results.** As shown in Table 1, in in-distribution settings, despite their much smaller parameter scales, ACT and SwitchVLA remain competitive with several-billion-parameter models, indicating that relatively compact policies can already achieve strong performance on seen tasks. In particular, ACT exhibits strong trajectory-following behavior and produces remarkably smooth hand motions on several reactive tasks with almost no observable latency. Among the large-scale models, _π_ 0 _._ 5 slightly outperforms GR00T N1.5 in average success rate, while _ψ_ 0 further improves overall performance and HEX achieves the best average success rate of 79.8%. Qualitatively, large-scale models may exhibit mild lag or stuttering in highly reactive tasks, whereas smaller policies such as ACT often produce smoother motions. Overall, HEX provides the strongest balance between task success and motion quality among the evaluated large-scale models, which may benefit from its explicit future-state conditioning and predictive proprioceptive modeling. 

#### **4.2.2 Long-Horizon Scenarios** 

Long-horizon tasks are composed of multiple subtasks, where different stages require different body parts, such as the waist and hands in some stages and the legs in others. This heterogeneous composition increases task complexity and gives rise to more pronounced cascading errors across stages. 

**Post-training Datasets.** We collect a long-horizon box conveyance task consisting of four stages: squatting down to grasp the box, turning toward the table, moving to the table and stopping in front of it, and squatting down again to place the box. In total, we collect 56 trajectories for training. We further introduce two household long-horizon tasks, _Basket transfer from bed to table_ and _Toy transfer to cart basket_ , each with 100 post-training trajectories. Both tasks require coordinated manipulation and locomotion over multiple stages, including object grasping, body turning, object transport, and final placement. Each task is evaluated over 15 trials. 

**Results.** As shown in Table 2, HEX consistently achieves the best SR and SPS across all three long-horizon tasks. On the original box convey task, HEX reaches 53.3% SR and 79.4 SPS. The advantage becomes more pronounced on the two additional tasks, achieving 73.3% SR and 83.9 SPS on basket transfer, and 86.7% SR and 92.0 SPS on toy transfer. Compared with the strongest baseline on each task, HEX improves SR by 6.6, 13.3, and 26.7 percentage points, respectively. These results demonstrate that HEX more reliably maintains task progress across multiple manipulation and locomotion stages, reducing performance degradation over long-horizon whole-body execution. 

### **4.3 Generalization Study** 

**Evalation Tasks.** As shown in Figure 5, we evaluate generalization on four tasks from the seen-scenario setting, including three standard tasks (Tasks 1, 2, and 5) and one long-horizon task. For _Pose Mimic_ , we consider Pose Mimic Fast, which increases the speed of human pose switching, and Pose Mimic Intervention, where an additional person in the background continuously performs distracting poses. A total of 18 trials are conducted, including 5 trials each for the V-, L-, and A-shaped poses, and 3 trials for the return-hand pose. For _Pouring_ , we evaluate Pouring Distractors by adding irrelevant objects, and Pouring Position by changing the bottle location. In the distractor setting, three cups are tested with 5 trials each. In the position-variation setting, the bottle is placed at 9 different locations, with one trial for each cup at each location. For _Kneel Pick_ , we evaluate Kneel Pick Dynamic, where object positions are changed during 

11 


**Figure 5.** Generalization tasks. Two distribution-shift variants for each of four seen tasks: _Pose Mimic_ , _Pouring_ , _Box Carry_ , and _Kneel Pick_ . 

execution, and Kneel Pick Objects, where the original blocks are replaced with unseen balls. Each variant is evaluated with 15 grasp-and-place trials. For _Box Carry_ , we evaluate Box Carry Distractors by introducing additional surrounding objects, and Box Carry Lights by changing the lighting condition. Each variant is evaluated over 15 trials. 

**Results.** Figure 6 summarizes the results on eight generalization variants across four seen tasks. HEX achieves the best overall average success rate of 61.8%, substantially outperforming _π_ 0 _._ 5 (44.3%), GR00T N1.5 (41.0%), and SwitchVLA (22.4%). Overall, HEX performs best on nearly all variants. In _Pose Mimic_ , HEX matches the best result under fast switching (100%) and achieves the highest success rate under human intervention (85.7%). Notably, under human intervention, all methods except HEX fail to maintain the “L” hand gesture after being distracted by a background person. In addition, GR00T N1.5 and _π_ 0 _._ 5 often produce inaccurate L-shaped poses. In contrast, HEX remains substantially more robust to such interference. In _Pouring_ , HEX shows the clearest advantage, improving from 0% for all baselines to 53.3% under visual distractors, and reaching 55.5% under bottle-position changes. After distractor objects are introduced, all baselines tend to start pouring before 


**Figure 6.** Generalization results across unseen task variants. 

receiving a human instruction and then remain fixed at one location. We conjecture that these models mistakenly treat the red plate as the human hand, whereas HEX does not exhibit this failure mode. In _Box Carry_ , HEX also achieves the best results under both unseen lighting (26.7%) and unseen surrounding objects (40.0%). For _Kneel Pick_ , HEX attains 33.0% under dynamic position changes and 100% under unseen objects. These results indicate that HEX generalizes more robustly under diverse distribution shifts, including faster human motion, human interference, visual distractors, object-position changes, lighting variation, and dynamic scene changes. 

12 

### **4.4 Ablation Study** 

#### **4.4.1 Ablation on Pretraining** 

We evaluate the impact of pretraining from two perspectives: in-distribution optimization efficiency and out-ofdistribution generalization. 

**In-distribution Performance.** Figure 7(a) shows that pretraining mainly improves optimization w/ pretrain w/o pretrain SR w/o pretrain SR w/ pretrain efficiency rather than final converged perfor10<sup>0</sup> 100 10<sup>0</sup> mance in the single-task setting. Specifically, 75 the pretrained model exhibits lower state and 10<sup>−1</sup> 10<sup>−1</sup> action losses during early training, indicating 50 10<sup>−2</sup> better initialization and faster convergence. As 10<sup>−2</sup> 25 training proceeds, the state loss gap becomes 10<sup>−3</sup> 0 marginal after approximately 10k steps, while 0 10k 20k 30k 0 10k 20k 30k the pretrained model generally maintains a lower Step Step action loss. This advantage is also reflected in **Figure 7.** Effect of pretraining. Left: state loss. Right: action loss early-stage task success: at 5k/10k/15k/20k steps, together with success-rate comparisons at different training stages. the pretrained model achieves 2/12, 4/12, 8/12, and 10/12 successes, compared with 0/12, 0/12, 2/12, and 7/12 without pretraining. However, both models eventually achieve comparable success rates (11/12 vs. 10/12). These results suggest that the primary benefit of pretraining under in-distribution conditions lies in faster optimization and improved training efficiency, rather than substantially higher final performance. 

**Out-of-distribution Generalization.** To further examine whether pretraining improves generalization beyond faster downstream optimization, we evaluate HEX on the long-horizon _Toy transfer to cart basket_ task under two distribution shifts: unseen target cart positions and unseen manipulated objects, as illustrated in Figure 8. Both models are evaluated under the same downstream training and testing settings, differing only in whether pretraining is applied. As shown in Table 3, pretraining substantially improves performance under both shifts. For unseen target positions, SR increases from 40.0% to 73.3%, while SPS 


**Figure 8.** Real-world generalization settings with and without pretraining. (a) Spatial generalization to unseen cart positions. (b) Object generalization to unseen plush toys. 

improves from 61.7 to 83.9. Without pretraining, the policy often completes initial manipulation but struggles with target-directed locomotion and accurate placement, particularly for distant targets. In contrast, the pretrained model exhibits more consistent navigation and placement across target positions. For unseen objects, the improvement is more pronounced, with SR increasing from 0.0% to 66.7% and SPS from 10.6 to 77.2. The non-pretrained model frequently fails to establish stable grasps or execute locomotion, whereas the pretrained model achieves reliable whole-body task execution. These results show that pretraining not only accelerates downstream optimization but also improves robustness to unseen objects and spatial configurations. 

**Table 3.** Effect of pretraining on OOD generalization for the _Toy transfer to cart basket_ task. We evaluate two distribution shifts: unseen target positions and an unseen object. 

|OOD Setting|Pretraining|SR (%)_↑_|SPS_↑_|
|---|---|---|---|
|Three target positions|w/o Pretrain<br>w/ Pretrain|40.0<br>**73.3**|61.7<br>**83.9**|
|Unseen object|w/o Pretrain<br>w/ Pretrain|0.0<br>**66.7**|10.6<br>**77.2**|


13 

#### **4.4.2 Data Scaling** 

We investigate the effects of data scaling at both the pretraining and fine-tuning stages, examining how pretraining data composition and downstream supervision influence task performance. 

**Ablation on Pretraining Data Composition.** We investigate how different pretraining data sources and their combinations affect downstream performance on the long-horizon _Basket transfer from bed to table_ task under the same fine-tuning protocol. As shown in Table 4, HEX and HE-G1 achieve the strongest single-source transfer, both reaching 80.0% SR, with SPS values of 88.7 and 86.7, respectively. Notably, HE-G1 transfers effectively despite substantial embodiment differences from Tiangong, demonstrating the potential of cross-embodiment knowledge transfer. In contrast, Agibot, HE-H1, and RoboCOIN-Leju yield weaker performance. Uniformly mixing multiple sources does not always help: adding Agibot to HEX reduces SR from 80.0% to 46.7%, whereas combining HEX with HE-G1 preserves strong performance. These results suggest that data quality and transferability may matter more than embodiment similarity alone. Accordingly, the final all-source configuration adopts quality-aware sampling, prioritizing stronger sources while retaining weaker ones for diversity. This strategy achieves the best overall performance (86.7% SR and 90.0 SPS), highlighting the importance of balancing data quality and diversity in cross-embodiment pretraining. 

**Table 4.** Ablation on pretraining data composition for the _Basket transfer from bed to table_ task. All models use the same downstream fine-tuning and evaluation setting. 

|Setting|Pretraining Data|SR (%)_↑_|SPS_↑_|
|---|---|---|---|
||Agibot|0.0|46.7|
||HE-G1|**80.0**|86.7|
|Single-source|HE-H1|0.0|26.0|
||RoboCOIN-Leju|0.0|6.7|
||HEX data|**80.0**|**88.7**|
||HEX + Agibot|46.7|58.7|
|Mlti-sorce|HEX + HE-G1|80.0|88.7|
|uu|HEX + HE-H1|0.0|33.3|
||All sources|**86.7**|**90.0**|


To better understand these performance differences, we further examine three characteristics of the pretraining datasets: task diversity, visual diversity, and whole-body motion coverage. First, Agibot, Unitree G1, Unitree H1, Leju, and Tiangong contain 175, 247, 247, 5, and 34 task categories, respectively. However, task count alone does not determine transferability, as Unitree G1 and H1 exhibit different downstream performance despite having identical task counts. Second, we sample 2K frames from each dataset and measure visual diversity using the mean pairwise cosine distance between extracted features. Figure 9(a) shows that Tiangong exhibits relatively high intra-source and inter-source visual distances, whereas Agibot and Unitree H1 show lower visual variation. Third, Figure 9(b) shows that Tiangong, Unitree G1, and Leju contain higher proportions of coordinated arm-leg motion, while Agibot and Unitree H1 exhibit more limited coverage. This may partly explain their weaker transfer to tasks requiring coordinated locomotion and manipulation. Notably, Leju exhibits relatively high motion coverage but limited task diversity, suggesting that no single data characteristic fully explains downstream transferability. Together, these findings highlight that effective cross-embodiment pretraining requires diverse and task-relevant visual and motion experiences, rather than merely increasing the number of tasks or robot embodiments. 

**Ablation on Pretraining Data Scaling.** To investigate the impact of pretraining data scale, we evaluate HEX using different fractions of the pretraining dataset while keeping the downstream fine-tuning data and protocol unchanged. As shown in Figure 10(a), pretraining exhibits a non-monotonic effect on downstream performance. Surprisingly, using only 10-20% of the pretraining data reduces SR from 53.3% (training from scratch) to 0.0%, indicating that insufficient pretraining can introduce negative transfer rather than improve performance. One possible explanation is that limited pretraining data fails to capture sufficiently diverse embodiment-specific dynamics, resulting in biased representations that hinder downstream adaptation. As the pretraining scale increases to 50%, SPS improves to 71.1, although SR remains below the scratch baseline at 40.0%. With the full pretraining dataset, HEX achieves 86.7% SR and 91.7 SPS, substantially outperforming training from scratch. These findings suggest that effective cross-embodiment pretraining requires sufficient data coverage to learn transferable motion representations, as limited heterogeneous data may introduce harmful inductive biases rather than beneficial prior knowledge. 

14 


**Figure 9.** Analysis of visual and motion diversity across pretraining datasets. (a) Mean pairwise cosine distances between visual features, where diagonal and off-diagonal entries represent intra-source diversity and inter-source differences, respectively. (b) Proportions of samples exhibiting leg motion, arm motion, and simultaneous arm-leg motion across different datasets. 


**Figure 10.** Effect of pretraining and fine-tuning data ratio on the long-horizon _Basket transfer from bed to table_ task. 

**Ablation on Fine-tuning Data Scaling.** To further investigate the data efficiency of downstream adaptation, we evaluate HEX on the long-horizon _Basket transfer from bed to table_ task using different fractions of task-specific training data. As shown in Figure 10(b), increasing the fine-tuning data ratio progressively improves task performance. Although no complete task success is achieved with 10-50% of the training data, the stage-wise progress score (SPS) increases from 0.0 at 10% to 3.3 at 20% and 19.4 at 50%, indicating improved partial task completion. With the full training dataset, HEX achieves a success rate (SR) of 86.6% and an SPS of 91.7. These results characterize the adaptation behavior of the cross-embodiment pretrained model under varying amounts of downstream supervision, while also highlighting the importance of sufficient task-specific data for successful long-horizon whole-body manipulation. 

#### **4.4.3 Ablation on Model Components** 

Figure 11 evaluates the contributions of the VLM history cache, UPP, and morphology-aware MoE design. Performance consistently improves as these components are progressively introduced, highlighting their complementary roles in complex whole-body manipulation. In particular, UPP contributes substantially to overall performance, underscoring the importance of accurate proprioceptive dynamics modeling for coordinated control. On _Pour_ and _Box Conveying_ , the morphology-agnostic MoE achieves SPS values of 91.7 and 65.0, outperforming the “w/o MoE” variant (88.7 and 60.0). Incorporating morphology-aware routing further improves SPS to 97.0 and 79.4, respectively, under the same model capacity and expert architecture. These results suggest that effective whole-body control benefits not only from specialized expert representations but also from explicitly accounting for embodiment-specific structural differences, enabling more effective modeling of heterogeneous whole-body motion dynamics. 

15 


**Figure 11.** Effect of key model components. Performance improves consistently as the history cache, UPP, and MoE design are progressively introduced, and the full HEX achieves the best SPS on both _Pouring_ and _Box Conveying_ . 

**Table 5.** Parameter sensitivity analysis of the visual history window, number of experts in UPP, and loss weight _α_ . 

|**(a) Vi**|**sual History**|**Window**|**(b) Numbe**|**r of Experts**|**in UPP**|**(c**|**) Loss Wei**|**ght**_α_|
|---|---|---|---|---|---|---|---|---|
|_H_|SR (%)_↑_|SPS_↑_|# Experts|SR (%)_↑_|SPS_↑_|_α_|SR (%)_↑_|SPS_↑_|
|0|0.0|43.3|1|13.3|40.0|0.0|0.0|30.7|
|2|**80.0**|**85.3**|8|33.3|58.7|0.5|73.3|**89.3**|
|4|46.6|52.0|16|**53.3**|68.7|1.0|**80.0**|85.3|
|8|0.0|28.7|32|**53.3**|**72.0**|2.0|0.0|18.7|


### **4.5 Other Anayses** 

#### **4.5.1 Parameter Sensitivity Analysis** 

Table 5 provides a sensitivity analysis of HEX for three key hyperparameters: the visual history window _H_ , the number of experts in UPP, and the loss weight _α_ used to balance action and state prediction objectives. 

**Visual history window.** Using only the current observation ( _H_ = 0) leads to a substantial performance drop, indicating that temporal visual context is important for long-horizon whole-body execution. A short history window of _H_ = 2 achieves the best performance, with 80.0% SR and 85.3 SPS. Increasing the window to _H_ = 4 or _H_ = 8 does not yield further improvements. In particular, with _H_ = 8, the policy tends to over-rotate during the turning stage, which subsequently affects locomotion. This suggests that a compact visual history provides sufficient temporal cues while avoiding excessive reliance on outdated observations. We therefore use _H_ = 2 by default. 

**Number of experts.** Increasing the number of UPP experts from 1 to 16 consistently improves both SR and SPS, demonstrating the benefit of additional expert capacity for modeling heterogeneous whole-body dynamics. Increasing the number further from 16 to 32 yields the same SR (53.3%) and only a modest SPS improvement from 68.7 to 72.0, while introducing additional computational and memory overhead. We therefore adopt 16 experts as a practical trade-off between performance and efficiency. 

**Loss weight** _α_ **.** The loss weight _α_ controls the balance between action generation and proprioceptive prediction. Removing the state-prediction objective ( _α_ = 0) substantially degrades performance, confirming the importance of predictive proprioceptive modeling. In contrast, an excessively large weight ( _α_ = 2) also leads to severe degradation, suggesting that over-emphasizing state prediction can interfere with task-oriented action learning through the shared representation. Although _α_ = 0 _._ 5 achieves a slightly higher SPS, _α_ = 1 yields the highest end-to-end success rate (80.0%), and is therefore selected as the default setting. 

#### **4.5.2 MoE Routing Pattern** 

Figures 12 and 13 analyze the routing behavior of the input-side and output-side MoE modules from complementary perspectives. Figure 12 shows that the input-side MoE exhibits relatively sparse and persistent body-part preferences, indicating specialization toward different local proprioceptive components, while its activations can still vary with the 

16 


**Figure 12.** Expert-wise routing patterns of the input-side and output-side MoE modules during a whole-body manipulation rollout. 

evolving motion pattern. In contrast, the output-side MoE shows stronger task-dependent coordination across multiple body parts, suggesting that contextualized features after the transformer backbone enable experts to capture coordinated whole-body dynamics rather than only isolated body-part characteristics. 

Figure 13 further shows how these patterns evolve during long-horizon execution. Before the transformer blocks, expert assignments remain largely stable across subtask transitions, whereas after the transformer blocks, routing becomes markedly more phase-dependent, with major expert switches aligning with semantic task boundaries such as turning and locomotion. Together, these results suggest that the input-side MoE primarily captures persistent body-partspecific dynamics, while the output-side MoE further adapts expert selection to task phase and cross-part coordination. 

17 


**Figure 13.** Comparison of MoE routing patterns before and after the transformer blocks during a long-horizon box conveyance task. Left: MoE before the transformer blocks. Right: MoE after the transformer blocks. The heatmaps show the selected expert ID for each body part over time, together with representative frames and annotated subtask boundaries. Compared with the largely static routing before the transformer blocks, the routing after the transformer blocks shows clearer phase-dependent switching, suggesting stronger state-dependent control specialization. 

**Figure 14.** Failure analysis across different methods and tasks. Each Sankey diagram shows how failed trials are distributed across task stages and fine-grained error types, with flow width proportional to the number of failures. 

**Latency.** Figure 15 compares the latency-accuracy trade-off of different methods on an RTX 4090. ACT achieves the lowest latency, but with a substantial drop in success rate. Among the large-scale baselines, GR00T N1.5 attains a relatively favorable latency-accuracy trade-off, achieving competitive performance at lower latency than both _π_ 0 _._ 5 and HEX. HEX nevertheless achieves the highest success rate overall (79.8%) with 73.34 ms latency, outperforming all baselines in task success while remaining faster than _π_ 0 _._ 5. Overall, these results show that HEX provides the strongest effectiveness under a practical inference budget. 

**Failure Analysis.** Figure 14 shows that different methods fail not only at different rates, but also in different stages. In the two seen-scenario tasks, failures are relatively concentrated in a small number of key sub-stages, mainly related to object grasping, placement, and multi-object handling. In contrast, the long-horizon box conveyance task exhibits more distributed failures across grasping, turning, locomotion, and final placement, indicating that longer action chains amplify error accumulation and cross-stage dependency. Across tasks, HEX generally yields fewer failures and a more concentrated failure distribution than the baselines. This suggests that its advantage is not only higher overall success, but also improved robustness to error propagation across sequential stages, especially in long-horizon execution. 

**UPP Prediction Analysis.** To directly examine whether UPP learns meaningful future proprioceptive dynamics, we evaluate its prediction accuracy on a held-out validation set throughout training. As shown in Fig. 16, the prediction losses of all body components steadily decrease and converge to low values, indicating that UPP can predict future 

18 


**Figure 15.** Latency–accuracy comparison on a single NVIDIA RTX 4090 GPU, where bubble size indicates the number of model parameters. 


**Figure 16.** Body-part-wise future proprioceptive prediction loss of UPP on the validation set throughout training. 

proprioceptive states on unseen trajectories rather than merely fitting the training data. The body-part-wise results further reveal different prediction difficulties across components, with the waist exhibiting relatively higher residual error than most other parts, reflecting the more complex dynamics involved in whole-body coordination. 

## **5 Conclusion** 

We presented **HEX** , a framework for humanoid whole-body manipulation that addresses a key limitation of existing VLA-style approaches: they often do not explicitly model how different body parts interact under shared balance and posture. HEX tackles this problem through a humanoid-aligned universal state representation, predictive modeling of whole-body proprioceptive dynamics, and adaptive fusion of visual-language context with future state evolution. This leads to more coherent and stable whole-body action generation. Extensive experiments on real-world humanoid manipulation tasks show that HEX achieves superior performance over strong baselines, particularly in fast-reaction and long-horizon settings where coordinated whole-body behavior is essential. Overall, our results highlight the importance of explicitly modeling structured body-part interaction for general and scalable humanoid manipulation. 

## **References** 

- [1] Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui Chen, Zesen Cheng, Lianghao Deng, Wei Ding, Chang Gao, Chunjiang Ge, et al. Qwen3-vl technical report. _arXiv preprint arXiv:2511.21631_ , 2025. 

- [2] Shuanghao Bai, Jing Lyu, Wanqi Zhou, Zhe Li, Dakai Wang, Lei Xing, Xiaoguang Zhao, Pengwei Wang, Zhongyuan Wang, Cheng Chi, Badong Chen, and Shanghang Zhang. Latent reasoning VLA: Latent thinking and prediction for vision-languageaction models. In _Proceedings of the 43rd International Conference on Machine Learning_ , volume 306, pages 5409–5426. PMLR, 2026. 

- [3] Shuanghao Bai, Wenxuan Song, Jiayi Chen, Yuheng Ji, Zhide Zhong, Jin Yang, Han Zhao, Wanqi Zhou, Zhe Li, Pengxiang Ding, et al. Embodied robot manipulation in the era of foundation models: Planning and learning perspectives. _IEEE Transactions on Robotics_ , 2026. 

- [4] Shuanghao Bai, Wenxuan Song, Jiayi Chen, Yuheng Ji, Zhide Zhong, Jin Yang, Han Zhao, Wanqi Zhou, Wei Zhao, Zhe Li, et al. Towards a unified understanding of robot manipulation: A comprehensive survey. _arXiv preprint arXiv:2510.10903_ , 2025. 

- [5] Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [6] Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 3549–3556, 2025. 

19 

- [7] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. In _Robotics: Science and Systems_ , 2025. 

- [8] Sirui Chen, Yufei Ye, Zi-ang Cao, Pei Xu, Jennifer Lew, and Karen Liu. Hand-eye autonomous delivery: Learning humanoid navigation, locomotion and reaching. In _Conference on Robot Learning_ , pages 4058–4073. PMLR, 2025. 

- [9] Zixuan Chen, Mazeyu Ji, Xuxin Cheng, Xuanbin Peng, Xue Bin Peng, and Xiaolong Wang. Gmt: General motion tracking for humanoid whole-body control. _arXiv preprint arXiv:2506.14770_ , 2025. 

- [10] Can Cui, Pengxiang Ding, Wenxuan Song, Shuanghao Bai, Xinyang Tong, Zirui Ge, Runze Suo, Wanqi Zhou, Yang Liu, Bofang Jia, et al. Openhelix: A short survey, empirical analysis, and open-source dual-system vla model for robotic manipulation. _arXiv preprint arXiv:2505.03912_ , 2025. 

- [11] Pengxiang Ding, Jianfei Ma, Xinyang Tong, Binghong Zou, Xinxin Luo, Yiguo Fan, Ting Wang, Hongchao Lu, Panzhong Mo, Jinxin Liu, et al. Humanoid-vla: Towards universal humanoid control with visual integration. _arXiv preprint arXiv:2502.14795_ , 2025. 

- [12] Ria Doshi, Homer Rich Walke, Oier Mees, Sudeep Dasari, and Sergey Levine. Scaling cross-embodied learning: One policy for manipulation, navigation, locomotion and aviation. In _Conference on Robot Learning_ , pages 496–512. PMLR, 2025. 

- [13] Zhiying Du, Bei Liu, Yaobo Liang, Yichao Shen, Haidong Cao, Xiangyu Zheng, Zhiyuan Feng, Zuxuan Wu, Jiaolong Yang, and Yu-Gang Jiang. Himoe-vla: Hierarchical mixture-of-experts for generalist vision-language-action policies. _arXiv preprint arXiv:2512.05693_ , 2025. 

- [14] Yiguo Fan, Shuanghao Bai, Xinyang Tong, Pengxiang Ding, Yuyang Zhu, Hongchao Lu, Fengqi Dai, Wei Zhao, Yang Liu, Siteng Huang, et al. Long-vla: Unleashing long-horizon capability of vision language action model for robot manipulation. In _Conference on Robot Learning_ , pages 2018–2037. PMLR, 2025. 

- [15] Zipeng Fu, Qingqing Zhao, Qi Wu, Gordon Wetzstein, and Chelsea Finn. Humanplus: Humanoid shadowing and imitation from humans. In _Conference on Robot Learning_ , pages 2828–2844. PMLR, 2025. 

- [16] Langzhe Gu, Chengkai Hou, Meng Li, Xinhua Wang, Jiaming Liu, Xinyuan Lv, Bowei Zhang, Shuanghao Bai, Guangrun Li, Jingyang He, et al. Haf: Adapting generalist vlas to humanoid whole-body loco-manipulation via hierarchical action flow and spectral latent rl. In _Conference on Robot Learning_ , 2026. 

- [17] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris M Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. In _Conference on Robot Learning_ , pages 1516–1540. PMLR, 2025. 

- [18] Tairan He, Zi Wang, Haoru Xue, Qingwei Ben, Zhengyi Luo, Wenli Xiao, Ye Yuan, Xingye Da, Fernando Castañeda, Shankar Sastry, et al. Viral: Visual sim-to-real at scale for humanoid loco-manipulation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 13430–13441, 2026. 

- [19] Chengkai Hou, Kun Wu, Jiaming Liu, Zhengping Che, Di Wu, Fei Liao, Guangrun Li, Jingyang He, Qiuxuan Feng, Zhao Jin, et al. Robomind 2.0: A multimodal, bimanual mobile manipulation dataset for generalizable embodied intelligence. _arXiv preprint arXiv:2512.24653_ , 2025. 

- [20] Jiaheng Hu, Peter Stone, and Roberto Martín-Martín. Slac: Simulation-pretrained latent action space for whole-body real-world rl. In _Conference on Robot Learning_ , pages 2966–2982. PMLR, 2025. 

- [21] Yingdong Hu, Haodong Zhu, Boyuan Zheng, Yihang Hu, Tong Zhang, Zunhao Chen, Junming Zhao, Ruiqian Nai, and Yang Gao. Openhlm: An empirical recipe for whole-body humanoid loco-manipulation. _arXiv preprint arXiv:2606.22174_ , 2026. 

- [22] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: A vision-language-action model with open-world generalization. In _Conference on Robot Learning_ , volume 305, pages 17–40. PMLR, 2025. 

- [23] Haoran Jiang, Jin Chen, Qingwen Bu, Li Chen, Modi Shi, Yanjie Zhang, Delong Li, Chuanzhe Suo, Hongyang Li, et al. Wholebodyvla: Towards unified latent vla for whole-body loco-manipulation control. In _International Conference on Learning Representations_ , volume 2026, pages 157438–157461, 2026. 

- [24] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P Foster, Pannag R Sanketi, Quan Vuong, et al. Openvla: An open-source vision-language-action model. In _Conference on Robot Learning_ , pages 2679–2713. PMLR, 2025. 

- [25] Jinhan Li, Yifeng Zhu, Yuqi Xie, Zhenyu Jiang, Mingyo Seo, Georgios Pavlakos, and Yuke Zhu. Okami: Teaching humanoid robots manipulation skills through single video imitation. In _Conference on Robot Learning_ , pages 299–317. PMLR, 2025. 

20 

- [26] Meng Li, Zhen Zhao, Zhengping Che, Fei Liao, Kun Wu, Zhiyuan Xu, Pei Ren, Zhao Jin, Ning Liu, and Jian Tang. Switchvla: Execution-aware task switching for vision-language-action models. _arXiv preprint arXiv:2506.03574_ , 2025. 

- [27] Zhe Li, Yangyang Wei, Boan Zhu, Yibo Peng, Tao Huang, Pengwei Wang, Zhongyuan Wang, Cheng Chi, Chang Xu, and Shanghang Zhang. From language to locomotion: Retargeting-free humanoid control via motion latent guidance. In _International Conference on Learning Representations_ , volume 2026, pages 129292–129319, 2026. 

- [28] Zhe Li, Zhenzhe Zhang, Yangyang Wei, Wenjie Zhang, Xichen Yuan, Peiyuan Zhi, Gen Li, Xinying Guo, Fengjie Gao, Jianfei Yang, et al. _ω_ -0: A latent predictive world action model for concurrent humanoid loco-manipulation. _arXiv preprint arXiv:2608.06375_ , 2026. 

- [29] Zhe Li, Boan Zhu, Yangyang Wei, Shuanghao Bai, Yuheng Ji, Yibo Peng, Tao Huang, Pengwei Wang, Zhongyuan Wang, S-H Gary Chan, et al. Robomirror: Understand before you imitate for video to humanoid locomotion. In _European Conference on Computer Vision_ , pages 482–499. Springer, 2026. 

- [30] Zhuo Li, Yiming Yao, Jim Tan, Mengjie Jing, Zhipeng Dong, and Fei Chen. Wholebodywam: Generalizing pre-trained world-action priors to humanoid loco-manipulation via wbc-grounded coordination. _arXiv preprint arXiv:2609.16644_ , 2026. 

- [31] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _Science Robotics_ , 11(117):eadx8924, 2026. 

- [32] Yunfeng Lin, Minghuan Liu, Yufei Xue, Ming Zhou, Yong Yu, Jiangmiao Pang, and Weinan Zhang. H-zero: Cross-humanoid locomotion pretraining enables few-shot novel embodiment transfer. In _2026 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9306–9313. IEEE, 2026. 

- [33] Jiacheng Liu, Pengxiang Ding, Qihang Zhou, Yuxuan Wu, Da Huang, Zimian Peng, Wei Xiao, Weinan Zhang, Lixin Yang, Cewu Lu, et al. Trajbooster: Boosting humanoid whole-body manipulation via trajectory-centric learning. In _2026 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 17257–17264. IEEE, 2026. 

- [34] Chenhao Lu, Xuxin Cheng, Jialong Li, Shiqi Yang, Mazeyu Ji, Chengjing Yuan, Ge Yang, Sha Yi, and Xiaolong Wang. Mobile-television: Predictive motion priors for humanoid whole-body control. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5364–5371. IEEE, 2025. 

- [35] Hao Luo, Ye Wang, Wanpeng Zhang, Sipeng Zheng, Ziheng Xi, Chaoyi Xu, Haiweng Xu, Haoqi Yuan, Chi Zhang, Yiqing Wang, et al. Being-h0.5: Scaling human-centric robot learning for cross-embodiment generalization. _arXiv preprint arXiv:2601.12993_ , 2026. 

- [36] Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Fernando Castañeda, Sirui Chen, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _Science Robotics_ , 11(117):eaed4592, 2026. 

- [37] Jiageng Mao, Siheng Zhao, Siqi Song, Chuye Hong, Tianheng Shi, Junjie Ye, Mingtong Zhang, Haoran Geng, Jitendra Malik, Vitor Guizilini, et al. Universal humanoid robot pose learning from internet human videos. In _2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids)_ , pages 1–8. IEEE, 2025. 

- [38] Jun Nakanishi, Jun Morimoto, Gen Endo, Gordon Cheng, Stefan Schaal, and Mitsuo Kawato. Learning from demonstration and adaptation of biped locomotion. _Robotics and autonomous systems_ , 47(2-3):79–91, 2004. 

- [39] Quanquan Peng, Yunfeng Lin, Yufei Xue, Jiangmiao Pang, and Weinan Zhang. Embodiment-aware generalist specialist distillation for unified humanoid whole-body control. In _2026 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 16996–17003, 2026. 

- [40] Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- [41] Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ , 40(4):1–20, 2021. 

- [42] Ryan Punamiya, Dhruv Patel, Patcharapong Aphiwetsa, Pranav Kuppili, Lawrence Zhu, Simar Kareer, Judy Hoffman, and Danfei Xu. Egobridge: Domain adaptation for generalizable imitation from egocentric human data. In _Advances in Neural Information Processing Systems_ , volume 38, pages 47092–47122, 2025. 

- [43] Ri-Zhao Qiu, Shiqi Yang, Xuxin Cheng, Chaitanya Chawla, Jialong Li, Tairan He, Ge Yan, David J Yoon, Ryan Hoque, Lars Paulsen, et al. Humanoid policy human policy. In _Conference on Robot Learning_ , pages 2888–2906. PMLR, 2025. 

- [44] Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, and Koushil Sreenath. Real-world humanoid locomotion with reinforcement learning. _Science Robotics_ , 9(89):eadi9579, 2024. 

21 

- [45] Modi Shi, Shijia Peng, Jin Chen, Haoran Jiang, Yinghui Li, Di Huang, Ping Luo, Hongyang Li, and Li Chen. Egohumanoid: Unlocking in-the-wild loco-manipulation with robot-free egocentric demonstration. In _Robotics: Science and Systems_ , 2026. 

- [46] Wenxuan Song, Ziyang Zhou, Han Zhao, Jiayi Chen, Pengxiang Ding, Haodong Yan, Yuxin Huang, Feilong Tang, Donglin Wang, and Haoang Li. Reconvla: Reconstructive vision-language-action model as effective robot perceiver. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 40, pages 18549–18557, 2026. 

- [47] Lirui Wang, Xinlei Chen, Jialiang Zhao, and Kaiming He. Scaling proprioceptive-visual learning with heterogeneous pre-trained transformers. In _Advances in neural information processing systems_ , volume 37, pages 124420–124450, 2024. 

- [48] Yen-Jen Wang, Jiaman Li, Sirui Chen, Takara E Truong, Pei Xu, Pieter Abbeel, Rocky Duan, Koushil Sreenath, Angjoo Kanazawa, Carmelo Sferrazza, et al. Vlk: Learning humanoid loco-manipulation from synthetic interactions in reconstructed scenes. _arXiv preprint arXiv:2606.30645_ , 2026. 

- [49] Yihao Wang, Pengxiang Ding, Lingxiao Li, Can Cui, Zirui Ge, Xinyang Tong, Wenxuan Song, Han Zhao, Wei Zhao, Pengxu Hou, et al. Vla-adapter: An effective paradigm for tiny-scale vision-language-action model. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 40, pages 18638–18646, 2026. 

- [50] Songlin Wei, Hongyi Jing, Boqian Li, Zhenyu Zhao, Jiageng Mao, Zhenhao Ni, Sicheng He, Jie Liu, Xiawei Liu, Kaidi Kang, et al. Ψ0: An open foundation model towards universal humanoid loco-manipulation. In _Robotics: Science and Systems_ , 2026. 

- [51] Haoyang Weng, Yitang Li, Nikhil Sobanbabu, Zihan Wang, Zhengyi Luo, Tairan He, Deva Ramanan, and Guanya Shi. Hdmi: Learning interactive humanoid whole-body control from human videos. _arXiv preprint arXiv:2509.16757_ , 2025. 

- [52] Kun Wu, Chengkai Hou, Jiaming Liu, Zhengping Che, Xiaozhu Ju, Zhuqin Yang, Meng Li, Yinuo Zhao, Zhiyuan Xu, Guang Yang, et al. Robomind: Benchmark on multi-embodiment intelligence normative data for robot manipulation. In _Robotics: Science and Systems_ , 2025. 

- [53] Shihan Wu, Xuecheng Liu, Shaoxuan Xie, Pengwei Wang, Xinghang Li, Bowen Yang, Zhe Li, Kai Zhu, Hongyu Wu, Yiheng Liu, et al. Robocoin: An open-sourced bimanual robotic data collection for integrated manipulation. _arXiv preprint arXiv:2511.17441_ , 2025. 

- [54] Weiji Xie, Jinrui Han, Jiakun Zheng, Huanyu Li, Xinzhe Liu, Jiyuan Shi, Weinan Zhang, Chenjia Bai, and Xuelong Li. Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills. In _Advances in Neural Information Processing Systems_ , volume 38, pages 62406–62433, 2026. 

- [55] Zhaoming Xie, Jonathan Tseng, Sebastian Starke, Michiel Van De Panne, and C Karen Liu. Hierarchical planning and control for box loco-manipulation. _Proceedings of the ACM on Computer Graphics and Interactive Techniques_ , 6(3):1–18, 2023. 

- [56] Zhiyuan Xu, Yinuo Zhao, Kun Wu, Ning Liu, Junjie Ji, Zhengping Che, Chi Harold Liu, and Jian Tang. Hacts: a human-ascopilot teleoperation system for robot learning. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 15475–15481. IEEE, 2025. 

- [57] Haoru Xue, Xiaoyu Huang, Dantong Niu, Qiayuan Liao, Thomas Kragerud, Jan Tommy Gravdahl, Xue Bin Peng, Guanya Shi, Trevor Darrell, Koushil Sreenath, et al. Leverb: Humanoid whole-body control with latent vision-language instruction. _arXiv preprint arXiv:2506.13751_ , 2025. 

- [58] Yufei Xue, Yunfeng Lin, Wentao Dong, Yang Tang, Jingbo Wang, Jiangmiao Pang, Ming Zhou, Minghuan Liu, and Weinan Zhang. Scalable and general whole-body control for cross-humanoid locomotion. In _Proceedings of the 43rd International Conference on Machine Learning_ , volume 306, pages 143236–143254. PMLR, 2026. 

- [59] Haoran Yang, Jiacheng Bao, Yucheng Xin, Haoming Song, Yuyang Tian, Bin Zhao, Dong Wang, and Xuelong Li. Zerowbc: Learning natural visuomotor humanoid control directly from human egocentric video. _arXiv preprint arXiv:2603.09170_ , 2026. 

- [60] Jonathan Yang, Catherine Glossop, Arjun Bhorkar, Dhruv Shah, Quan Vuong, Chelsea Finn, Dorsa Sadigh, and Sergey Levine. Pushing the limits of cross-embodiment learning for manipulation and navigation. In _Robotics: Science and Systems_ , 2024. 

- [61] Ruihan Yang, Qinxi Yu, Yecheng Wu, Rui Yan, Borui Li, An-Chieh Cheng, Xueyan Zou, Yunhao Fang, Xuxin Cheng, Ri-Zhao Qiu, et al. Egovla: Learning vision-language-action models from egocentric human videos. _arXiv preprint arXiv:2507.12440_ , 2025. 

- [62] Yanjie Ze, Zixuan Chen, Joao Pedro Araujo, Zi-ang Cao, Xue Bin Peng, Jiajun Wu, and Karen Liu. Twist: Teleoperated whole-body imitation system. In _Conference on Robot Learning_ , pages 2143–2154. PMLR, 2025. 

- [63] Yanjie Ze, Zixuan Chen, Wenhao Wang, Tianyi Chen, Xialin He, Ying Yuan, Xue Bin Peng, and Jiajun Wu. Generalizable humanoid manipulation with 3d diffusion policies. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 2873–2880. IEEE, 2025. 

22 

- [64] Bowei Zhang, Qiyao Zhang, Shuanghao Bai, Xinhua Wang, Meng Li, Yilei Wang, Leiwang Zhang, Jian Tang, Lu Zhou, Lei Sun, et al. Wholebodywam: Learning whole-body world action models with scalable motion priors. _arXiv preprint arXiv:2609.18197_ , 2026. 

- [65] Yuanhang Zhang, Yifu Yuan, Prajwal Gurunath, Ishita Gupta, Shayegan Omidshafiei, Ali-akbar Agha-mohammadi, Marcell Vazquez-Chanlatte, Liam Pedersen, Tairan He, and Guanya Shi. Falcon: Learning force-adaptive humanoid loco-manipulation. In _Proceedings of the 8th Annual Learning for Dynamics and Control Conference_ , volume 331, pages 265–281. PMLR, 2026. 

- [66] Tony Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. In _Robotics: Science and Systems_ , 2023. 

- [67] Zehui Zhao, Yuxuan Zhao, Gaojing Zhang, Chenxi Liu, Maolin Zheng, and Wenzhao Lian. Halomi: Learning humanoid loco-manipulation with active perception from human demonstrations. _arXiv preprint arXiv:2606.18772_ , 2026. 

- [68] Zhenyu Zhao, Hongyi Jing, Xiawei Liu, Jiageng Mao, Abha Jha, Hanwen Yang, Rong Xue, Sergey Zakharov, Vitor Guizilini, and Yue Wang. Humanoid everyday: A comprehensive robotic dataset for open-world humanoid manipulation. In _2026 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6415–6422. IEEE, 2026. 

- [69] Jia Zheng, Teli Ma, Yudong Fan, Zifan Wang, Shuo Yang, and Junwei Liang. Motionwam: Towards foundation world action models for real-time humanoid loco-manipulation. _arXiv preprint arXiv:2606.09215_ , 2026. 

23 

