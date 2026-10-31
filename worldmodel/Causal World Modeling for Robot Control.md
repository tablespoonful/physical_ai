---
title: "Causal World Modeling for Robot Control"
date: "2026-01-29"
authors: "Lin Li; Qihang Zhang; Yiming Luo; Shuai Yang; Ruilin Wang; Fei Han"
url: https://arxiv.org/abs/2601.21998
pdf: https://arxiv.org/pdf/2601.21998
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.21998)** / [論文ページ](https://arxiv.org/abs/2601.21998)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。



# **Causal World Modeling for Robot Control** 

Lin Li<sup>_∗_</sup> Qihang Zhang<sup>_∗†_</sup> Yiming Luo<sup>_∗_</sup> Shuai Yang Ruilin Wang Fei Han Mingrui Yu Zelin Gao Nan Xue Xing Zhu Yujun Shen Yinghao Xu<sup>_‡_</sup> _∗_ Equal Contribution _†_ Project Lead _‡_ Corresponding Author 

This work highlights that video world modeling, alongside vision-language pre-training, establishes a fresh and independent foundation for robot learning. Intuitively, video world models provide the ability to “imagine” the near future by understanding the causality between actions and visual dynamics. Inspired by this, we introduce LingBot-VA, an autoregressive diffusion framework that learns frame prediction and policy execution simultaneously. Our model features three carefully crafted designs: (1) **_a shared latent space_** , integrating vision and action tokens, driven by a Mixture-of-Transformers (MoT) architecture, (2) **_a closed-loop rollout mechanism_** , allowing for ongoing acquisition of environmental feedback with ground-truth observations, (3) **_an asynchronous inference pipeline_** , parallelizing action prediction and motor execution to support efficient control. We evaluate our model on both simulation benchmarks and real-world scenarios, where it shows significant promise in long-horizon manipulation, data efficiency in post-training, and strong generalizability to novel configurations. The code and model are made publicly available to facilitate the community. 

**Website:** https://technology.robbyant.com/lingbot-va **Github:** https://github.com/robbyant/lingbot-va **Checkpoints:** https://huggingface.co/robbyant/lingbot-va 


## **1 Introduction** 

Vision-Language-Action (VLA) models have emerged as a promising paradigm for general-purpose robotic manipulation [7, 11, 12, 34], demonstrating impressive capabilities in grounding linguistic instructions into visual perceptions across diverse objects and unstructured environments. However, beneath their apparent success lies a significant challenge: _representation entanglement_ . Most existing VLAs adopt a feedforward paradigm that maps current observations to action sequences [17, 91], requiring a single neural network to simultaneously learn visual scene understanding, physical dynamics, and motor control from a unified supervision signal. This entanglement can create a bottleneck—the model must compress heterogeneous knowledge, ranging from high-dimensional visual semantics to low-dimensional motor commands, into a shared representation space. This often leads to limited sample efficiency and suboptimal generalization. Without explicit modeling of environmental evolution [25, 26, 82], reactive policies may rely on pattern matching rather than a principled understanding of physical dynamics. 

Recent attempts to bring world modeling into robotic policies span interactive neural simulators (e.g., UniSim [86]), chunk-based video-action diffusion models (e.g., UVA [40] and UWM [97]), and offline video generators for subgoal synthesis (e.g. Gen2Act [4], Act2Goal [95]). While conceptually appealing, these approaches face three primary limitations for effective closed-loop control. First, _the reactivity gap_ : chunk/open-loop generation often rolls out long segments without incorporating real-time feedback, making it hard to adapt to disturbances. Second, _limited long-term memory_ : chunk-wise generation can introduce inconsistencies over long horizons when history is not persistently cached. Third, _causality_ : bidirectional attention within a segment allows future tokens to influence past predictions, which diverges from the causal nature of physical reality where the present depends only on the past. These observations motivate an autoregressive formulation for robust closed-loop reasoning. 

We propose LingBot-VA, an _autoregressive diffusion_ world model that addresses these limitations through a unified 

1 


**Figure 1.** LingBot-VA **: An Autoregressive World Model for Robotic Manipulation.** (1) **Pretraining:** LingBot-VA is pretrained on diverse in-the-wild videos and robot action data, enabling strong generalization across scenes and objects. (2) **Comprehensive Evaluation:** We conduct extensive experiments on real-world tasks (long-horizon, deformable objects, and precision manipulation) and simulation benchmarks, significantly outperforming state-of-the-art methods including _π_ 0 _._ 5. (3) **Versatile Capabilities:** Beyond policy learning, our model supports visual dynamics prediction and inverse dynamics inference from robot videos. (4) **Emergent Properties:** Our causal world modeling approach exhibits long-range temporal memory and strong few-shot adaptation ability. 

video-action framework. Unlike autoregressive language models that predict discrete tokens, our model operates in a continuous latent space via flow matching [46, 50], autoregressively generating chunks of video and action representations through iterative denoising. While our approach conceptually separates visual dynamics prediction and action decoding [22, 27], the key architectural insight is to _interleave_ video and action tokens into a single autoregressive sequence. Both modalities are jointly processed through a Mixture-of-Transformers (MoT) architecture [43] with shared attention. Within this unified autoregressive generation process, latent imagination and action inference occur jointly: at each autoregressive step, the model generates predicted future visual states through iterative denoising while simultaneously decoding the corresponding actions, allowing both streams to mutually condition on one another. This integration, built upon a large-scale pretrained video diffusion backbone [79], offers several advantages: _(i) Reactive AR loop_ : because video and action tokens form a unified sequence, each autoregressive step allows the system to recalibrate based on the latest real-world observation, enabling timely adjustments to both the predicted future and motor commands; _(ii) Persistent context through KV-cache_ : the cached key-value pairs preserve the interleaved video-action trajectory, providing a rich context that helps mitigate temporal drift; _(iii) Causal consistency_ : causal attention masking over the unified sequence ensures that both predicted visual states and action commands are governed by preceding states, respecting the temporal arrow of physical dynamics. By incorporating real-world observations at each step, this formulation helps mitigate the _distribution drift_ that often affects open-loop methods in long-horizon tasks. 

A primary challenge in deploying large-scale autoregressive video-action models is inference latency; generating high-fidelity video tokens through iterative denoising is computationally intensive. We address this through two complementary strategies. First, we introduce _Noisy History Augmentation_ , a training scheme that enables _partial denoising_ at inference time. The key insight is that action decoding does not always require pixel-perfect reconstruction; instead, it can rely on robust semantic structures. By training the action decoder to predict from partially noisy latent representations, we significantly reduce the computational overhead while maintaining precise action prediction. Second, we design an _asynchronous coordination_ pipeline that overlaps computation with execution: while the 

2 

robot executes current actions, the world model predicts future visual states and plans subsequent sequences. This parallelized architecture, combined with variable chunk-size training, facilitates high-frequency closed-loop control without compromising prediction quality. 

We evaluate LingBot-VA across diverse manipulation tasks in both simulation and real-world environments. Our method demonstrates competitive performance compared to state-of-the-art VLA policies, particularly in long-horizon tasks requiring temporal consistency. Our contributions are summarized as follows: 

- **Autoregressive Video-Action World Modeling:** We introduce an autoregressive diffusion framework that _architecturally unifies_ visual dynamics prediction and action inference within a single interleaved sequence while maintaining their _conceptual distinction_ . This formulation supports persistent memory through KV cache and causal consistency via attention masking. 

- **Mixture-of-Transformers Architecture with Asynchronous Execution:** We design a dual-stream MoT architecture with asymmetric capacity and introduce a partial denoising strategy combined with asynchronous coordination to enable efficient robotic control. 

- **Superior Long-Horizon and Precision Performance:** Extensive real-world and simulation experiments demonstrate consistent state-of-the-art performance, with particularly strong improvements on long-horizon and high-precision manipulation tasks. Our method also achieves significantly improved sample efficiency and strong generalization to novel scenes and object configurations. 

## **2 Preliminary** 

### **2.1 Flow Matching** 

Flow matching [46, 50, 75] is a continuous-time generative modeling framework that learns to transform a simple source distribution (e.g., Gaussian noise) to a target data distribution through a continuous flow. Given a data sample _x_ 1 and a noise sample _ϵ ∼N_ (0 _, I_ ), flow matching defines a time-dependent vector field _vs_ : R<sup>_d_</sup> _×_ [0 _,_ 1] _→_ R<sup>_d_</sup> that describes the instantaneous velocity of particles flowing from _ϵ_ to _x_ 1. The trajectory _x_<sup>(</sup><sup>_s_)</sup> evolves according to the ordinary differential equation (ODE): 


where _s ∈_ [0 _,_ 1] denotes the flow time. 

The model is trained to predict this vector field by minimizing: 


where _x_ ˙<sup>(</sup><sup>_s_)</sup> is the true velocity along the interpolation path, typically defined as _x_<sup>(</sup><sup>_s_)</sup> = (1 _− s_ ) _ϵ_ + _sx_ 1, giving _x_ ˙<sup>(</sup><sup>_s_)</sup> = _x_ 1 _− ϵ_ . 

At inference, samples are generated by solving the learned ODE from _s_ = 0 to _s_ = 1: 


### **2.2 Video Generation with Conditional Flow Matching** 

Recent video generation models [23, 35, 54, 79] leverage flow matching to generate videos conditioned on text or images. These models operate in the latent space of pretrained video autoencoders, where visual observations are encoded as latent representations _zt_ = _E_ ( _ot_ ) using encoder _E_ (e.g., from video diffusion models). 

Given a conditioning signal _c_ (text prompt or initial image), the flow matching model learns to generate a sequence of latent video frames **z** = _{z_ 1 _, . . . , zT }_ by predicting the vector field: 


3 


**Figure 2. Framework overview** : LingBot-VA is conditioned by _autoregressive diffusion_ for unified _video-action world modeling_ . We leverage a dual-stream _Mixture-of-Transformers (MoT)_ architecture that interleaves video and action tokens within a single sequence. At each autoregressive step, the video stream (initialized from Wan2.2-5B) first predicts future latent visual states via _flow matching_ . Then the action stream decodes corresponding actions through _inverse dynamics_ conditioning on the predicted visual transitions. 

where _s ∈_ [0 _,_ 1] is the flow time and **z**<sup>(</sup><sup>_s_)</sup> represents the latent video at flow step _s_ . The generation process starts from noise **z**<sup>(0)</sup> = _ϵ ∼N_ (0 _, I_ ) and integrates the learned vector field to obtain the final latent video **z**<sup>(1)</sup> , which is then decoded to pixel space. This bidirectional generation framework enables flexible synthesis from text descriptions or seed images. 

## **3 Method** 

### **3.1 Problem Statement & Approach Overview** 

We study robotic manipulation as a sequential decision-making problem under partial observability. At each timestep _t_ , the agent receives a visual observation _ot ∈O_ and executes an action _at ∈A_ , which induces a transition in the underlying physical world and produces the next observation _ot_ +1. 

**Vision-Language-Action (VLA) Policies.** Most existing VLA policies learn a direct, reactive mapping from observation history to actions: 


through imitation learning on robot demonstration data. While this end-to-end approach has shown impressive results, it suffers from a fundamental coupling problem: the model must simultaneously learn visual scene understanding, physical dynamics, and motor control from a single supervision signal of paired observations and actions. This entanglement leads to poor sample efficiency and limited generalization, as the model struggles to disentangle visual reasoning from action prediction without explicit dynamics modeling. 

**Our Approach.** Unlike VLA policies that directly learn action distributions, we adopt a world modeling perspective: instead of learning _π_ ( _at | ot_ ), we predict how the visual world will evolve, then infer actions based on these predictions.· Our approach operates in two stages: 


Stage 1 learns to predict future visual observations given observation history. Stage 2 uses an inverse dynamics model to decode actions from desired visual transitions. This decomposition enables Stage 1 to leverage large-scale video data for learning physical priors, while Stage 2 only requires robot demonstrations to ground visual predictions in executable actions. 

4 

_Method Overview._ Figure 2 illustrates the details of our framework. Our method consists of three key components, detailed in the following subsections: _(§3.2) Autoregressive Video-Action World Modeling_ describes how we model visual dynamics in latent space and decode actions from predicted state transitions—this is the _core formulation_ of our approach; _(§3.3) LingBot-VA: Unified Architecture & Training_ presents our unified model for video-action pretraining, including the architecture design and training objective—this is the _instantiation_ of our formulation; _(§3.4) Real-time Deployment & Asynchronous Inference_ introduces our deployment strategy that enables real-time control through parallelized prediction and execution—this is the _practical realization_ for robotic control. 

### **3.2 Autoregressive Video-Action World Modeling** 

Previous video world models either focus on open-ended video prediction [54] or learn action-conditioned interactive environments [13, 56] primarily for game or simulation domains, which may not directly transfer to precise robotic manipulation. To leverage rich visual dynamics priors from video data for robot manipulation, we propose a unified video-action world modeling framework that jointly models visual observations and robot actions within a single autoregressive process. Unlike prior approaches that either decouple video prediction from action inference [16, 27] or rely on bidirectional diffusion within segments [97], our method unifies video and action within a single _causal autoregressive_ framework, enabling persistent memory through KV cache and seamless integration of real-time observations. 

**World Dynamics with Autoregressive Modeling.** Recent world models for robotics often adopt bidirectional video generation approaches [4, 20, 24, 42] or learn interactive simulators [86], which face fundamental limitations for closed-loop control. Open-loop methods that generate entire long sequences in one shot incur prohibitive computational cost and cannot incorporate real-time feedback for error correction. Chunk-based diffusion methods that generate video segments sequentially [22, 97] suffer from two critical issues: (1) they lack persistent memory across chunks, as each chunk is generated independently without access to the full history, leading to temporal inconsistencies and drift over long horizons; (2) the bidirectional attention within each chunk violates causality, preventing seamless integration with real-time observations during execution. 

The physical world, however, is inherently causal and autoregressive: the present state depends only on the past, and we cannot observe the future before it occurs. This fundamental property motivates our autoregressive world modeling approach, which offers three critical advantages over chunk-based diffusion for robotic control: _(1) Persistent Memory_ : by explicitly conditioning on the complete observation history through causal attention and KV cache, the model maintains long-term context and temporal coherence across the entire trajectory, avoiding the “amnesia” problem of chunk-based methods; _(2) Causal Consistency_ : the unidirectional dependency structure naturally aligns with closed-loop execution, where new observations can be seamlessly incorporated as they arrive; _(3) Efficiency_ : chunk-wise prediction with parallel generation within each chunk balances computational efficiency with autoregressive flexibility, enabling high-frequency control with real-time error correction. 

We formalize this as an autoregressive process: at each step, the world model predicts the next chunk of _K_ video frames using conditional flow matching: 


where tokens within each chunk are generated in parallel via bidirectional attention, while maintaining causal structure across chunks. This chunk-wise formulation balances generation efficiency with autoregressive flexibility for closed-loop correction. 

**Video-Action State Encoding.** Operating directly on pixel-level video observations is computationally prohibitive due to the high dimensionality and redundancy of raw visual data. We leverage a causal video VAE [79] to compress visual observations into compact latent tokens _zt_ = _E_ ( _ot | o<t_ ) _∈_ R<sup>_N×C_</sup> , where _N_ is the number of spatial tokens after passing into video VAE, and _C_ is the channel number. By conditioning on previous latent states, the encoder maintains temporal coherence while processing observations sequentially, naturally aligning with our autoregressive world modeling framework. To align robot actions with visual tokens, we project action vectors to token embeddings _at ∈_ R<sup>_D_</sup> via a lightweight MLP _ϕ_ ( _·_ ) where _D_ is the dimension of the video token after patchfication, enabling unified interleaving of visual and action tokens as in prior approaches [5, 22]. 

**Latent Video State Transition.** While standard video generation models predict future frames based solely on visual history, robotic manipulation requires accounting for the embodiment’s physical state and interaction with the 

5 

environment. During deployment, the robot’s state evolves through continuous interaction: each action modifies the embodiment’s configuration (e.g., gripper position, joint angles), which in turn influences how the scene evolves. 

In many manipulation settings, actions encode absolute pose information (e.g., end-effector poses in world coordinates), so the action history _a<t_ effectively captures the trajectory of the embodiment’s configuration. Conditioning on action history thus provides knowledge of how the robot has moved and interacted with objects, consistent with prior action-conditioned video/world models [22, 86, 97]. We extend our autoregressive formulation to condition on both observation and action histories: 


where _zt_ is the latent visual state and _at_ is the action token. This enables the world model to ground predictions in the embodiment’s state, ensuring that predicted observations reflect the robot’s physical interaction with the scene. 

**Inverse Dynamics for Action Decoding.** Once the world model predicts future visual states, we leverage these predictions to plan actions. Rather than directly predicting actions from current observations, we employ an inverse dynamics model that infers actions by conditioning on desired future observations, enabling the policy to reason about _what action leads to a desired visual outcome_ . 

However, simply conditioning on the current and next states ( _zt, zt_ +1) is insufficient for accurate action prediction. The action history _a<t_ encodes the embodiment’s state trajectory for determining feasible actions, while the observation history _z<t_ provides temporal context for multi-step interactions (e.g., whether an object was previously grasped). We therefore formulate inverse dynamics as: 


where the inverse dynamics model _gψ_ takes as input the predicted chunk of visual states _z_ ˆ _t_ +1: _t_ + _K_ inferred by Eq. 8, observation history _z≤t_ , and action history _a<t_ . This mirrors recent IDM-based policies [1, 20, 22, 55, 73] that leverage future targets to infer feasible actions while maintaining consistency with embodiment dynamics. 

### **3.3 LingBot-VA: Unified Architecture & Training** 

**Architecture.** To jointly model video and action generation, we leverage a dual-stream diffusion transformer architecture that performs conditional flow matching for autoregressive prediction. Our model consists of two parallel transformer backbones: a video stream initialized from Wan2.2-5B (a large-scale pretrained video generation model with dimension _dv_ [79]), and an action stream with same depth but significantly smaller width _da ≪ dv_ . This asymmetric design is motivated by the observation that action distributions are inherently simpler than visual data requiring fewer parameters to model effectively while maintaining expressive capacity for visual dynamics. 

_Video Sparsification._ Video frames exhibit significant temporal redundancy, especially in robotic manipulation where scenes evolve gradually. We sparsify the video sequence by temporally downsampling frames by a factor of _τ_ = 4, reducing visual tokens while improving efficiency [5]. Since actions evolve at higher frequency than visual changes, we interleave the downsampled video tokens with action tokens in temporal order: for each video frame _ot_ , we associate _τ_ consecutive actions _{at,_ 1 _, at,_ 2 _, . . . , at,τ }_ , forming a unified sequence [ _zt, at,_ 1 _, at,_ 2 _, . . . , at,τ , zt_ +1 _, . . ._ ] for joint modeling. This design means that predicting _K_ video frames corresponds to generating _τK_ actions, enabling high-frequency control while maintaining efficient video generation. 

_Mixture-of-Transformer Block._ To enable interaction while preserving modality-specific feature spaces, we employ a Mixture-of-Transformers (MOT) architecture [5, 19, 43], where video and action tokens are processed by separate transformer blocks at each layer, then fused via cross-modal attention [5]. At each layer, the video and action streams independently compute their query, key, and value matrices using separate QKV projection matrices, maintaining distinct feature spaces for each modality. To align dimensions for cross-modal fusion, action tokens are first projected to the video dimension via a linear layer, participate in joint self-attention, then projected back to their original dimension via a residual connection that preserves the action-specific representations. This MOT design allows video and action to mutually influence each other through attention while maintaining separate parameterizations, preventing interference between modality-specific feature representations. For action decoding, the final action stream outputs are mapped to low-dimensional action vectors via a linear projection head. 

_Action Network Initialization._ Proper initialization of the action stream is critical for training stability and convergence. We find that training the action network from scratch leads to unstable optimization and slow convergence, as the action 

6 

tokens’ output distribution initially diverges significantly from the video distribution, disrupting the joint attention mechanism. To address this, we initialize the action network weights by interpolating the pretrained video weights according to the action dimension, then apply a scaling factor _α_ = ~~�~~ _dv/da_ to preserve output variance, where _dv_ and _da_ are the video and action dimensions. This initialization strategy ensures that action tokens start with output distributions comparable to video tokens, stabilizing early-stage training and accelerating convergence. 

_Variable Chunk Size Training._ To enable flexible deployment, we randomly sample the chunk size _K_ from a predefined range during training. By training with variable chunk sizes (e.g., _K ∈_ [1 _,_ 8]), the model learns to generate coherent predictions across different temporal horizons. At inference time, this allows freely selecting the chunk size to balance computational efficiency and planning horizon—larger chunks reduce the number of autoregressive steps but require longer per-step computation, while smaller chunks enable more frequent closed-loop correction. In our experiments, we use _K_ = 4 for deployment as a practical trade-off. 

**Teacher Forcing for Unified Video-Action Training.** In §3.2, we formulated both visual dynamics prediction (Eq. 7) and inverse dynamics (Eq. 8) as autoregressive modeling problems, where each prediction conditions on the history of observations and actions. This unified autoregressive formulation enables a natural training strategy: we can treat the interleaved video-action sequence as a single unified sequence and train the model using standard next-token prediction, analogous to language modeling in NLP [76]. 

Specifically, given an episode with interleaved tokens, we train the model to predict each token conditioned on all preceding tokens in the sequence. This is implemented via teacher forcing: during training, we use ground-truth tokens from the dataset as context for predicting subsequent tokens, rather than model-generated predictions. The causal dependency structure is enforced through attention masking (Figure 3)—each token can only attend to tokens that appear earlier in the temporal sequence. 


Importantly, teacher forcing is particularly well-suited for robotic manipulation: unlike pure generative modeling where it leads to train-test distribution mismatch, robot policies naturally retrieve real-world observations during deployment, directly matching the training regime. This formulation offers two key benefits: (1) unifying video and action prediction under a single training objective enables end-to-end learning of world dynamics and action inference; (2) by processing episodes in parallel with causal attention masking, we efficiently optimize both components across all timesteps in a single forward pass. 

**Figure 3. Teacher Forcing Attention Mask** : Causal attention mask for unified video-action pretraining. Each token can only attend to preceding tokens in the temporal sequence. 

_Noisy History Augmentation._ The primary bottleneck during attention mask for unified video-action pretraining. Each token can only attend to preceding tokens in the temporal inference remains video token generation—the number of video tokens are much larger than action tokens, and each sequence. requires multiple denoising steps through the flow matching process. To address this, we introduce a noise augmentation strategy during training that enables _partial denoising_ at test time. The key insight is that action prediction does not require fully denoised video representations; the inverse dynamics model can learn to extract action-relevant information from partially noisy video states. Specifically, during training, we randomly augment the video history _z≤t_ with noise following the same interpolation scheme as flow matching: 


This augmentation trains the action decoder to predict actions from partially noisy video representations. 

At inference time, this enables a significant speedup: instead of fully denoising video tokens from _s_ = 0 to _s_ = 1, we only need to denoise to _s_ = 0 _._ 5, halving the number of denoising steps for video generation while maintaining action prediction quality. 

7 

**Algorithm 1** KV Cache Inference 

**Require:** Initial observation _o_ 0, chunk size _K_ , KV cache _C_ 1: _z_ 0 _← E_ ( _o_ 0), _C ←{z_ 0 _}_ 2: _t ←_ 0 3: **loop** 4: Sample _ϵ ∼N_ (0 _, I_ ) _▷_ Generate video chunk (integrate to _s_ = 0 _._ 5) 5: _z_ ˜ _t_ +1: _t_ + _K ← ϵ_ + �00 _._ 5 _vθ_ ( _zt_<sup>(</sup> +1:<sup>_s_)</sup> _t_ + _K_<sup>_, s | C_)</sup><sup>_ds_</sup> 6: Sample _ϵ ∼N_ (0 _, I_ ) _▷_ Generate action chunk (integrate to _s_ = 1) 7: _at_ : _t_ + _K−_ 1 _← ϵ_ + �01<sup>_vψ_(</sup><sup>_a_(</sup> _t_ :<sup>_s_</sup> _t_<sup>)</sup> + _K−_ 1<sup>_, s |z_˜</sup><sup>_t_:</sup><sup>_t_+</sup><sup>_K, C_)</sup><sup>_ds_</sup> 8: **for** _i_ = _t_ **to** _t_ + _K −_ 1 **do** 9: Execute _ai_ , receive _oi_ +1 _▷_ Execute and collect observations 10: _zi_ +1 _← E_ ( _oi_ +1) 11: **end for** 12: _C ←C ∪{zt_ +1: _t_ + _K, at_ : _t_ + _K−_ 1 _} ▷_ Update KV cache 13: _t ← t_ + _K_ 14: **end loop** 

**Training Objective.** We jointly optimize both video and action using flow matching with the noisy history augmentation described above. For video tokens _zt_ , the dynamics loss supervises velocity field prediction conditioned on (potentially noisy) history: 


where _s ∈_ [0 _,_ 1] is flow time, _zt_<sup>(</sup> +1<sup>_s_)= (1</sup><sup>_−s_)</sup><sup>_ϵ_+</sup><sup>_szt_+1 with</sup><sup>_ϵ ∼N_(0</sup><sup>_, I_),</sup><sup>_z_˙</sup> _t_<sup>(</sup> +1<sup>_s_)=</sup><sup>_zt_+1</sup><sup>_−ϵ_, ˜</sup><sup>_z≤t_is the augmented history</sup> (Eq. 10), and _c_ is the language instruction. For action tokens _at_ , the inverse dynamics loss conditions on current and next observations: 


where _a_<sup>(</sup> _t_<sup>_s_)</sup> = (1 _− s_ ) _ϵ_ + _sat_ with _ϵ ∼N_ (0 _, I_ ), _z_ ˜ _t,_ ˜ _zt_ +1 are the (potentially noisy) current and next video tokens, and _c_ is the language instruction. The complete objective is _L_ = _L_ dyn + _λL_ inv. 

### **3.4 Real-time Deployment & Asynchronous Inference** 

**KV Cache for Efficient Autoregressive Inference.** Our autoregressive formulation naturally enables KV cache acceleration during inference. Since each prediction step conditions on the history of observations and actions, we cache the key-value pairs from previous tokens to avoid redundant computation. At each autoregressive step, only the new tokens (current observation and predicted actions) require full attention computation, while cached history tokens are reused. Algorithm 1 describes the complete inference procedure with KV cache. 

**Asynchronous Prediction and Execution.** Despite the efficiency gains from KV cache and partial denoising, autoregressive prediction still incurs non-negligible latency that can violate real-time control requirements. To address this, we introduce an asynchronous inference strategy that pipelines action prediction with execution, effectively hiding prediction latency. We illustrate the difference between synchronous and asynchronous inference in Fig. 4. 

The key insight is to overlap computation with execution (Fig. 4B): While the robot executes the current action chunk _at_ , the model simultaneously predicts the subsequent action chunk _at_ +1 conditioned on the most recent real observation _zt−_ 1 (received after the execution of _at−_ 1). For simplicity, we use _zt_ to denote latent observations (ignoring the video VAE compression) instead of _ot_ in this section. We discard all history data before timestamp _t −_ 1 and use the hat notation ˆ to mark predicted visual content. Consequently, the model’s active context is limited to the executed action chunk _at−_ 1, the recent ground-truth observation _zt−_ 1, the currently executing action _at_ , and its corresponding visual forecast _z_ ˆ _t_ . A naive auto-regressive implementation (Fig. 4B-1) is to store these tokens into the KV cache and predict _z_ ˆ _t_ +1. However, we observed that such a design frequently leads to open-loop degradation and trajectory drift. Because the video generative model inherently favors temporal smoothness, it tends to "continue" the hallucinated video _z_ ˆ _t_ while ignoring the critical physical feedback provided by the real observation _zt−_ 1, eventually causing the model to lose its capacity to react to the environment. 

8 


**Figure 4. Asynchronous pipeline design overview** : The traditional synchronous pipeline (A) suffers from delays caused by blocked computations, while the asynchronous pipeline (B) addresses this issue by enabling parallel computation and execution. However, a naive asynchronous implementation (B-1) relies on outdated visual predictions. In contrast, we improve and refine asynchronous prediction through forward dynamic prediction (B-2), which updates stale predictions with recent real-world observations. 

**Algorithm 2** Asynchronous Inference and Execution **Require:** Initial observation _o_ 0, chunk size _K_ , KV cache _C_ 1: _z_ 0 _← E_ ( _o_ 0); _C ←{z_ 0 _}_ 2: _z_ ˜1: _K, a_ 0: _K−_ 1 _←_ PREDICT( _C_ ) _▷_ Cold Start 3: ObsQueue _←∅ ▷_ Thread-safe queue for incoming real observations 

4: _t ←_ 0 

5: **loop** 

6: **parallel** : **Branch A: Robot Execution** 7: **async** EXECUTOR( _at_ : _t_ + _K−_ 1 _,_ ObsQueue) _▷_ Execute pre-computed actions **Branch B: Inference with FDM Grounding** 8: **if** _t >_ 0 **then** _ot−K_ +1: _t ←_ ObsQueue.dequeue() _▷_ Get real observation _zt−K_ +1: _t ← E_ ( _ot−K_ +1: _t_ ) _C ←C ∪{zt−K_ +1 _,t, at−K_ : _t−_ 1 _} ▷_ Cache feedback **end if** _C_ tmp _←C ∪{at_ : _t_ + _K−_ 1 _} ▷_ Cache action being executed _zt_ +1: _t_ + _K ←_ FDM( _C_ tmp) _▷_ Imagine visual outcome _C_ tmp _←C_ tmp _∪{zt_ +1: _t_ + _K} ▷_ Update cache _z_ ˜ _t_ + _K_ +1: _t_ +2 _K, at_ + _K_ : _t_ +2 _K−_ 1 _←_ PREDICT( _C_ tmp) _t ← t_ + _K_ 9: **end loop** 

To mitigate this, we introduce a Forward Dynamics Model (FDM) grounded step into our inference pipeline (Fig. 4B2). Instead of relying on stale forecasts, we replace it by executing a forward dynamics pass: the model uses the recent feedback _zt−_ 1 and "imagines" the resulting visual state _zt_ after applying action _at_ . By caching this feedback-grounded prediction instead of a stale forecast, we force the model to re-align with environmental feedback before predicting _zt_ +1. This design enhances our asynchronous algorithm into a robust closed-loop system, enabling the robot to effectively perceive and react to real-world changes. 

Algorithm 2 formalizes this asynchronous pipeline. During post training, we additionally incorporate a forward dynamics prediction loss: 


9 

## **4 Experiments** 

### **4.1 Dataset Curation and Preprocessing** 

We curate a large-scale training corpus by aggregating existing public robot manipulation datasets. All datasets undergo preprocessing to ensure consistency in data format and annotation quality, and are split into 90% training and 10% validation per dataset to monitor training dynamics. 

_Unified Action Representation._ To achieve cross-embodiment generalization, we define a universal action interface to adapt to different datasets. We use a dual-arm representation where each robotic arm is characterized by both end-effector pose (EEF) and joint angles. The end-effector pose consists of XYZ coordinates and a rotation quaternion (7 dimensions). For joint angles, we support a maximum of 7 degrees of freedom for single-arm embodiments; if a robot has fewer than 7 joint dimensions, we pad the missing dimensions with zeros to maintain a unified 7-dimensional representation. Each arm also has one gripper action dimension. Therefore, the total action dimensionality for dual-arm systems is: 7EEF + 7joints + 1gripper per arm, resulting in (7 + 7 + 1) _×_ 2 = 30 dimensions. 

_Training Data Composition._ We aggregate data from six sources spanning diverse embodiments, environments, and task categories: 

- **Agibot** [2]: Large-scale dataset with diverse manipulation tasks from mobile manipulators. 

- **RoboMind** [81]: Multi-embodiment manipulation demonstrations. 

- **InternData-A1** [74]: Large-scale simulation dataset for sim-to-real transfer. 

- **OXE** [53]: Multi-embodiment dataset; we use the OpenVLA subset. 

- **UMI Data** [18, 45, 48, 51, 60, 92]: Human demonstration dataset collected via universal manipulation interface<sup>1</sup> , excluding DexUMI. 

- **RoboCOIN** [84]: Cross-embodiment bimanual robotics data. 

In total, our training corpus comprises approximately **16K** hours of robot manipulation data across diverse tasks and environments, including internally collected demonstrations. 

### **4.2 Implementation & Training Details** 

_Implementation Details._ We use Wan2.2-5B as the backbone for the video stream, with hidden dimension _dv_ = 3072 and 30 transformer layers. The action stream shares the same depth but uses a reduced hidden dimension _da_ = 768 (4 _×_ smaller), resulting in approximately 350M additional parameters and a total model size of 5.3B parameters. Both streams employ RoPE positional encoding and are connected via the MoT architecture described in §3.3. We adopt the Wan2.2 causal VAE for tokenization with a 4 _×_ 16 _×_ 16 (temporal _×_ height _×_ width) compression ratio, combined with a patchify operation that further reduces spatial dimensions by 2. The encoded views are concatenated along the width dimension, resulting in a total of _N_ = 192 spatial tokens per frame. The action encoder _ϕ_ and decoder are implemented as single-layer MLPs with hidden dimension 256. We normalize actions using per-dimension quantile normalization statistics computed from the training set. Task instructions are encoded using a frozen T5 text encoder [59] and injected via cross-attention. During training, chunk size _K_ is randomly sampled from [1 _,_ 4]. 

For inference, we use Euler solver with 3 steps for video tokens (integrating to _s_ = 0 _._ 6) and 10 steps for action tokens (integrating to _s_ = 1 _._ 0). Video CFG scale is set to 5.0, while action CFG scale is set to 1.0. During training, noise augmentation is applied with probability _p_ = 0 _._ 5 and _s_ aug _∼_ Uniform[0 _._ 5 _,_ 1 _._ 0]. Following LLM practices, we pack multiple episodes into long sequences (up to 10K tokens) with attention masks. 

> 1https://umi-data.github.io/ 

10 


**Figure 5. Real-world deployment results.** We evaluate LingBot-VA on six manipulation tasks across three categories: longhorizon tasks (Make Breakfast, Pick Screws), precision tasks (Insert Tubes, Unpack Delivery), and deformable & articulated object manipulation (Fold Clothes, Fold Pants). Our method achieves state-of-the-art performance on both metrics. 

_Pre-Training Details._ We pretrain LingBot-VA on the curated dataset for 1.4T tokens. We use the AdamW optimizer with peak learning rate 1 _×_ 10<sup>_−_4</sup> , weight decay 0.01, and cosine annealing schedule with linear warmup. Training is conducted in bfloat16 mixed precision with gradient clipping at 2.0. We apply classifier-free guidance with text dropout rate 0.1. The loss weight _λ_ for inverse dynamics is set to 1. The dataset is sampled uniformly across all sources to ensure balanced learning. We monitor convergence using flow matching loss on the validation set. We use uniform SNR sampler for video model. For both video and action model, we use a uniform SNR sampler. 

_Post-Training Details._ While the pretrained model exhibits zero-shot generalization to seen embodiments, adapting to novel robot platforms requires a small amount of task-specific data. We find that post-training with as few as 50 demonstrations is sufficient for effective deployment. We use a reduced learning rate of 1 _×_ 10<sup>_−_5</sup> and train for 3K steps, which yields robust performance. Alternatively, a higher learning rate of 1 _×_ 10<sup>_−_4</sup> with 1K steps also produces reasonable results, though slightly inferior, offering a faster adaptation option when computational resources are limited. 

### **4.3 Main Results** 

#### **4.3.1 Real-world Deployment** 

_Experimental Setup._ To validate the real-world effectiveness of LingBot-VA, we deploy our model on a physical robot platform and evaluate across six diverse manipulation tasks spanning three challenging categories. (1) **_Long-horizon Tasks:_** We evaluate on _Make Breakfast_ and _Unpack Delivery_ , which require sequential multi-step reasoning and sustained 

11 


**Figure 6. Detailed task progressions and key execution steps of the six real-world tasks.** Each task involves a sequence of manipulation primitives, with scoring criteria detailed in Tables S2 through S4. 

12 

task execution over extended time horizons. (2) **_Precision Tasks:_** We test on _Insert Tubes_ and _Pick Screws_ , demanding accurate positioning and fine-grained motor control for successful completion. (3) **_Deformable Objects:_** We include _Fold Clothes_ and _Fold Pants_ , which involve manipulating non-rigid materials that present unique control challenges. The detailed task procedures are summarized in Fig. 6. These tasks are only collected with **50 real-world demos** for model training. We finetune the model for 500 steps with a learning rate of 1 _×_ 10<sup>_−_4</sup> and a sequence length of 150,000. 

_Results._ As shown in Fig. 5, LingBot-VA consistently achieves state-of-the-art performance across all six tasks and both evaluation metrics (success rate and progress score), substantially outperforming strong baseline _π_ 0 _._ 5. We highlight several key observations that validate our design choices: (1) The superior performance on _longhorizon tasks_ demonstrates that our video-action world model possesses strong temporal memory capabilities. By jointly modeling video and action sequences, the model effectively maintains task context over extended horizons, enabling coherent multi-step reasoning without losing track of intermediate goals. (2) The strong results on _precision tasks_ validate the effectiveness of our unified latent space design. By aligning video and action representations within a shared embedding space, our model achieves tighter coupling between visual perception and motor control, resulting in more accurate and fine-grained action predictions. (3) The robust performance on _deformable objects_ highlights the value of video generation as implicit guidance. The generated video futures provide rich predictive signals about object dynamics and state transitions, which inform the action model to produce more physically plausible manipulation trajectories for challenging non-rigid materials. 

These results collectively demonstrate that our video-action world model effectively transfers to real-world deployment, exhibiting robust performance across diverse manipulation scenarios. 

#### **4.3.2 Simulation Evaluation** 

_Experimental Setup._ We evaluate LingBot-VA on two widely-used simulation benchmarks: RoboTwin 2.0 [15] and LIBERO [47], covering diverse manipulation tasks across different robot embodiments. 

(1) In RoboTwin 2.0, we adopt a multi-task training setup [5] where all models are trained on 2,500 demonstrations collected in clean scenes (50 per task) plus 25,000 demonstrations from heavily randomized scenes (500 per task). We downsample the original 50 Hz video to 12.5 Hz while maintaining the action frequency at 50Hz. The model is trained for 50K steps with a learning rate of 1 _×_ 10<sup>_−_5</sup> . To facilitate a clearer comparison of performance, we categorize the 50 RoboTwin tasks according to their horizons (e.g., _Place Dual Shoes_ has two steps, and _Stack Blocks Three_ has three steps). The detailed horizons are listed in Tab. S1. 

(2) In LIBERO, we train our model on four LIBERO suites: LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and LIBERO-Long. Each suite contains 10 tasks with 50 demonstrations per task (500 total). Following OpenVLA [34], we filter unsuccessful demonstrations before training. The model is finetuned for 4K steps with a learning rate of 1 _×_ 10<sup>_−_5</sup> and a sequence length of 1 _×_ 10<sup>5</sup> . Specifically, we report the average success rate over three random seeds, with each seed comprising 500 evaluation trials (totally 3 _×_ 500 = 1500) for every task suite. 

_Results_ RoboTwin 2.0 is a challenging bimanual manipulation benchmark featuring over 50 tasks that require coordinated dual-arm control. Unlike single-arm benchmarks, RoboTwin tasks demand precise synchronization between 

**Table 1. Evaluation on RoboTwin 2.0 Simulation (Easy vs Hard, 50 tasks)** . RoboTwin 2.0 is a challenging bimanual manipulation benchmark requiring coordinated dual-arm control. Easy uses fixed initial configurations while Hard involves randomized object poses and scene layouts.<sup>_∗_</sup> Results for X-VLA are adopted from Motus [5]. Improvements in parentheses indicate gains over the second-best method (underlined). 

||X-VL|A<sup>_∗_</sup>[93]|_π_0|[7]|_π_0_._5|[29]|Motu|s [5]|LingBot-|VA(Ours)|
|---|---|---|---|---|---|---|---|---|---|---|
|**Metric**|Easy|Hard|Easy|Hard|Easy|Hard|Easy|Hard|Easy|Hard|
|AverageHorizon = 1|81.6|82.5|66.5|61.6|85.1|80.2|91.0|90.6|**94.18** (+3.2)|**93.56** (+3.0)|
|AverageHorizon = 2|59.3|55.9|66.1|54.7|79.3|73.0|85.2|80.9|**90.35** (+5.2)|**86.95** (+6.1)|
|AverageHorizon = 3|61.2|66.0|61.6|50.2|78.6|67.4|85.0|84.2|**93.22** (+8.2)|**93.28** (+9.1)|
|Average50 Tasks|72.9|72.8|65.9|58.4|82.7|76.8|88.7|87.0|**92.93** (+4.2)|**91.55** (+4.6)|


13 

**Table 2. Evaluation on LIBERO benchmarks** . LIBERO tests manipulation across four task suites: Spatial, Object, Goal, and Long-horizon. Our method achieves new state-of-the-art on LIBERO-Object (99.6%), LIBERO-Long (98.5%), LIBERO-Spatial (98.5%), and overall average (98.5%). Baseline results are adopted from [93]. 

|**Methods**|Spatial|**L**<br>Object|**IBERO**<br>Goal|Long|Avg|
|---|---|---|---|---|---|
|Octo [72]|78.9|85.7|84.6|51.1|75.1|
|Seer [73]|-|-|-|87.7|-|
|MoDE [61]|-|-|-|94.0|-|
|SuSIE [9]|-|-|-|76.3|-|
|SpatialVLA [58]|88.2|89.9|78.6|55.5|78.1|
|TraceVLA [94]|84.6|85.2|75.1|54.1|74.8|
|CoT-VLA [90]|87.5|91.6|87.6|69.0|81.1|
|ThinkAct [28]|88.3|91.4|87.1|70.9|84.4|
|SmolVLA [67]|93.0|94.0|91.0|77.0|88.8|
|CronusVLA [37]|97.3|99.6|96.9|94.0|97.0|
|FLOWER [62]|97.1|96.7|95.6|93.5|95.7|
|GR00T-N1 [6]|94.4|97.6|93.0|90.6|93.9|
|_π_0 [7]|96.8|98.8|95.8|85.2|94.1|
|_π_0+FAST [57]|96.4|96.8|88.6|60.2|85.5|
|OpenVLA [34]|84.7|88.4|79.2|53.7|76.5|
|OpenVLA-OFT [32]|97.6|98.4|**97.9**|94.5|97.1|
|DD-VLA [44]|97.2|98.6|97.4|92.0|96.3|
|UniVLA [78]|95.4|98.8|93.6|94.0|95.4|
|X-VLA [93]|98.2|98.6|97.8|97.6|98.1|
|LingBot-VA(Ours)|**98**_._**5**_±_**0**_._**3**|**99**_._**6**_±_**0**_._**3**|97_._2_±_0_._2|**98**_._**5**_±_**0**_._**5**|**98**_._**5**|


two manipulators, making it significantly more difficult for policy learning. We evaluate under both _Easy_ (fixed initial configurations) and _Hard_ (varied object poses and scene layouts) settings. As shown in Tab. 1, LingBot-VA achieves an average success rate of 92.9% (Easy) and 91.6% (Hard), substantially outperforming prior methods including _π_ 0, _π_ 0 _._ 5, X-VLA, and Motus. Notably, the improvement becomes more pronounced for longer-horizon tasks: at Horizon = 3, our method achieves gains of +8.2% (Easy) and +9.1% (Hard) over the second-best approach. This suggests that our autoregressive mechanism effectively maintains long-range temporal memory, enabling more robust performance as task complexity increases. 

We further evaluate on LIBERO benchmark (Tab. 2). On LIBERO, we obtain an average success rate of 98.5%, with particularly strong performance on LIBERO-Long (98.5%). These results establish new state-of-the-art performance in average success rates among foundational VLAs, demonstrating the effectiveness of our video-action world model for generalist robot control. 

### **4.4 Ablation** 

**Asynchronous v.s. synchronous** . We compare our asynchronous video-action generation with a synchronous baseline on RoboTwin tasks. As shown in Tab. 3, both approaches achieve comparable success rates, but our asynchronous method completes tasks **2** _×_ **faster** by predicting future video and action sequences while executing current actions. This validates that asynchronous generation maintains task performance while significantly improving inference efficiency. 

**Pretrained** LingBot-VA **v.s. WAN** . To validate the design choices in our video-action architecture, we conduct a controlled ablation study comparing our pretrained LingBot-VA model with WAN (Wan2.2-5B) as the initialization baseline for fine-tuning on RoboTwin tasks. Both models are fine-tuned on the same RoboTwin dataset using identical post-training procedures (50 task-specific demonstrations, learning rate 1 _×_ 10<sup>_−_5</sup> , 3K steps). 

As shown in Tab. 3, our pretrained LingBot-VA model substantially outperforms WAN fine-tuning across both Easy and Hard settings. Specifically, LingBot-VA achieves an average success rate of 92.10% (Easy) and 91.12% (Hard), while WAN fine-tuning yields significantly lower performance. This performance gap highlights the effectiveness of our joint video-action pretraining strategy, which endows the model with rich visual-motor priors that facilitate fast 

14 

**Table 3. Ablation studies on RoboTwin 2.0 (Easy).** We ablate three design choices: world modeling (AR vs. bidirectional), deployment mode (async vs. sync), and pretraining (Ours vs. WAN). 


**Figure 7. Training dynamic comparison between different action network initialization streategy** : Random initialization leads to unstable optimization (high gradient norms) and slow convergence. Although re-using video network weights stabilizes training, the resulting performance is not optimal. Our approach, which initializes by copying pretrained video weights with proper scaling, proves to be the most effective, ensuring smooth training dynamics and faster convergence. 

adaptation to complex bimanual manipulation tasks. 

**Action Network Initialization** . Proper initialization of the action stream is critical for training stability and convergence. We compare our curated initialization strategy (Section 3.3) with naive random initialization. 

As shown in Fig. 7, random initialization from scratch exhibits volatile training dynamics with significantly slower convergence. This instability arises because action tokens’ output distribution initially diverges dramatically from the video distribution, disrupting the joint attention mechanism in our unified architecture. In contrast, our curated initialization strategy—where action network weights are initialized by interpolating pretrained video weights with a scaling factor _α_ = ~~�~~ _dv/da_ —produces smooth convergence and substantially lower loss. 

### **4.5 Analysis** 

#### **4.5.1 Sample Efficiency** 

We investigate the data efficiency by exploring how LingBot-VA performs with limited post-training data compared to _π_ 0 _._ 5. We conduct this evaluation on both real-world and simulation settings: the “Make Breakfast” long-horizon task and RoboTwin 2.0 Easy benchmarks, allowing us to assess data efficiency across diverse manipulation scenarios. 

As shown in Fig. 8, our method consistently outperforms _π_ 0 _._ 5 across all data regimes on both real-world and simulation tasks. In the low-data regime (10 demonstrations), LingBot-VA achieves 15.6% higher progress score than _π_ 0 _._ 5 on the “Make Breakfast” task and 10.3% higher on RoboTwin 2.0 Easy, demonstrating superior sample efficiency. These results demonstrate that our method learns more effectively from limited data across diverse manipulation scenarios. 

We attribute this superior data efficiency to our video-action world model design. The jointly pretrained video generation backbone provides rich visual priors about physical dynamics and object interactions, which serve as implicit regularization during post-training. This allows the action model to leverage the world knowledge encoded in the video stream, effectively reducing the sample complexity required for adapting to new tasks. In contrast, VLA models like _π_ 0 _._ 5 lack explicit modeling of visual dynamics and thus have no structured dynamics priors to guide learning, requiring 

15 


**Figure 8. Sample efficiency comparison** . LingBot-VA consistently outperforms _π_ 0 _._ 5 across various data regimes on the “Make Breakfast” task, demonstrating superior data efficiency in the post-training stage. 


**Figure 9. Temporal memory evaluation.** Left: Success rates on two memory tasks (Wipe Plate and Search Box). LingBot-VA significantly outperforms _π_ 0 _._ 5 on both tasks, demonstrating superior temporal state tracking ability. Right: Visualization of evaluation environments. 

more demonstrations to learn task-specific behaviors from scratch. 

#### **4.5.2 Temporal Memory** 

We design the following tasks that explicitly require maintaining state information across time to evaluate our model’s temporal memory capabilities, as shown in Figure 9. 

1. **_Wipe Plate_** —the robot must wipe a plate exactly six times, requiring it to count and remember repeated actions. 

2. **_Search Box_** —Two boxes (left and right) are in the scene, with only one containing a block. The robot opens them sequentially from right to left. In data collection, the block is equally likely to be in either box; at test time, it is always in the left box. Without memory, after finding the right box empty, the model has a 50% chance of re-opening it. With memory, it proceeds to search the left box. 

As shown in Fig. 9(a), LingBot-VA substantially outperforms _π_ 0 _._ 5 on both memory tasks. We attribute this to the autoregressive nature of our world model: during training, teacher forcing conditions predictions on full history; during inference, KV-cache naturally preserves all historical information for persistent memory. 

16 


**Figure 10. Novel object and spatial generalization.** LingBot-VA successfully generalizes to objects with varying shapes, textures, and positions. 

#### **4.5.3 Generalization** 

We evaluate generalization along two axes: 

1. **_Novel Object Generalization_** —trained on pick-and-place with a single object, tested on different objects with varying shapes and textures; 

2. **_Spatial Generalization_** —trained with fixed object positions in a localized region(denoted as in-distribution (ID)), tested on random placements especially in out-of-distribution (OOD) regions. 

As shown in Fig. 10, our method demonstrates a stronger generalization in both both novel object and the out-ofdistribution position. The world model learns transferable visual representations through video prediction, capturing object-agnostic physical priors that transfer to novel scenarios. 

## **5 Related Work** 

**Vision-Language-Action Policies** . Recent advancements in Embodied AI have witnessed a paradigm shift toward largescale Vision-Language-Action (VLA) policies. By leveraging web-scale knowledge and diverse robot demonstrations, models such as _π_ 0 _._ 5 [29], GR-3 [39], and GR00T-N1 [6] achieve remarkable generalizability across various manipulation tasks without relying on hand-crafted rules, modular priors, or restricted action abstractions, enabling a more direct and expressive end-to-end mapping from perception to control. These policies typically employ pre-trained VisionLanguage Models (VLMs) as foundational backbones [6, 7, 11, 29, 34, 39, 87, 93], which provide superior cross-modal understanding and more generalizable action distributions compared to task-specific imitation policies like ACT [91] or Diffusion Policy [17]. Efforts have been further devoted to improving the deployability through lightweight backbones [49, 62, 67], efficient tokenization [57], real-time inference [8, 10, 70], or fine-tuning schemes [30, 32, 38]. However, despite their prowess in semantic reasoning, a fundamental limitation persists: the pre-training objectives and data distributions of standard VLMs largely overlook the fine-grained system dynamics and low-level trajectories essential for precision manipulation. While supervised fine-tuning on expensively collected large-scale robot datasets allows these models to approximate the marginal action distribution [3, 31, 53], they remain deficient in capturing the underlying transition dynamics—specifically, how the physical state of the environment should evolve and will evolve. Furthermore, most current VLA methods formulate control as a purely reactive mapping from instantaneous observations to actions. This approach inherently fails to account for the historical context necessary to resolve ambiguities in non-Markovian environments. Additionally, the static image-text pre-training inherent in VLMs fails to instill essential temporal priors. Even when augmented with memory modules [37, 65, 68], such models remain unable to reason about the causal and sequential nature of physical interactions. To address these shortcomings, recent research has pivoted towards generalist robot policies grounded in world models and generative video modeling [1, 5, 40, 64, 97]. However, these methods typically generate predictions with bidirectional attention, which violates the causal structure of physical dynamics and lacks persistent long-term memory across the full execution history. Our LingBot-VA unifies autoregressive video 

17 

prediction with action decoding under a strict causal temporal structure, where each prediction conditions exclusively on past observations and actions. By maintaining a persistent KV cache over the complete interaction history, LingBot-VA ensures long-range temporal consistency and allows the policy to synchronize physical execution with the predicted visual evolution of the environment. 

**World Models for Robotic Control** . Inspired by human reliance on intuitive physics to anticipate environmental changes, world models aim to facilitate effective planning by predicting future dynamics. Existing approaches are generally categorized into three groups based on their state representations. The first category operates in latent space [36, 41, 63, 80], encoding task-relevant features into compact vectors to predict evolution via probabilistic [36, 52, 83] or deterministic methods [63, 85]. The second category utilizes 3D point clouds [66, 69, 77], leveraging Graph Neural Networks (GNNs) to predict geometric evolution [88, 89], which is particularly effective for manipulating deformable objects [77, 89]. The third category focuses on 2D pixel space, directly predicting future keyframes or video sequences [21, 33, 95, 96]. Our work aligns with this third category. Within this domain, approaches range from co-training with video generation for representation learning [14, 40, 97] to serving as simulators for policy learning or evaluation [71]. Our research specifically targets methods that predict future frames during execution to condition action generation. However, prior video-conditioned methods predominantly rely on open-loop generation [21, 95], presenting two significant challenges. First, the misalignment between generated videos and real-world dynamics, coupled with cumulative drift from execution errors, often leads to suboptimal performance. Second, the computational intensity of video generation imposes high latency, severely hindering real-time inference. Our method leverages KV Cache and causal masking to continuously update the model’s memory with real-world observations. This effectively transitions the system to a closed-loop control mechanism, mitigating error accumulation in long-horizon tasks. Furthermore, we introduce a partial denoising strategy, enabling action generation from intermediate representations without waiting for fully denoised frames. 

## **6 Conclusion** 

We present LingBot-VA, an autoregressive diffusion framework that unifies video dynamics prediction and action inference for robotic manipulation. By interleaving video and action tokens within a Mixture-of-Transformers architecture, our model captures the causal structure of physical interactions while enabling closed-loop control through continuous integration of real-world observations. Extensive evaluation demonstrates strong performance across simulation benchmarks (92.0% on RoboTwin 2.0, 98.5% on LIBERO) and real-world deployment, achieving over 20% improvement on challenging tasks compared to _π_ 0 _._ 5 with only 50 demonstrations for adaptation. These results suggest that autoregressive video-action world modeling provides a principled foundation for learning generalizable manipulation policies, offering a compelling alternative to reactive VLA paradigms. 

**Future Work.** Future directions include developing more efficient video compression schemes to reduce computational overhead, and incorporating multi-modal sensory inputs (tactile, force, audio) for more robust manipulation in tasks with complex contact dynamics. 

**Acknowledgment.** We thank Kecheng Zheng for insightful discussions and Wei Wu for valuable assistance with dataset preparation. We also thank Fangyi Xu and Yishu Shen for their help with the post-training data collection. 

## **References** 

- [1] 1X Technologies. 1x world model: From video to action. https://www.1x.tech/discover/world-model-self-learning, 2025. Accessed 2026-01-18. 

- [2] AgiBot-World-Contributors, Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, Shu Jiang, Yuxin Jiang, Cheng Jing, Hongyang Li, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025. 

- [3] Jose Barreiros, Andrew Beaulieu, Aditya Bhat, Rick Cory, Eric Cousineau, Hongkai Dai, Ching-Hsin Fang, Kunimatsu Hashimoto, Muhammad Zubair Irshad, Masha Itkina, et al. A careful examination of large behavior models for multitask dexterous manipulation. _arXiv preprint arXiv:2507.05331_ , 2025. 

- [4] Homanga Bharadhwaj, Debidatta Dwibedi, Abhinav Gupta, Shubham Tulsiani, Carl Doersch, Ted Xiao, Dhruv Shah, Fei 

18 

Xia, Dorsa Sadigh, and Sean Kirmani. Gen2act: Human video generation in novel scenarios enables generalizable robot manipulation. In _Conference on Robot Learning (CoRL)_ , 2024. 

- [5] Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Yao Feng, Chendong Xiang, Yinze Rong, Hongyan Zhao, Hanyu Liu, Zhizhong Su, Lei Ma, Hang Su, et al. Motus: A unified latent action world model. _arXiv preprint arXiv:2512.13030_ , 2025. 

- [6] Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Jim Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil Kundalia, Lawrence Lao, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [7] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, et al. _π_ 0: A visionlanguage-action flow model for general robot control. In _Robotics: Science and Systems_ , 2025. 

- [8] Kevin Black, Manuel Y. Galliker, and Sergey Levine. Real-time execution of action chunking flow policies. _arXiv preprint arXiv:2506.07339_ , 2025. 

- [9] Kevin Black, Mitsuhiko Nakamoto, Pranav Atreya, Homer Walke, Chelsea Finn, Aviral Kumar, and Sergey Levine. Zero-shot robotic manipulation with pretrained image-editing diffusion models. In _Int. Conf. Learn. Represent._ , 2024. 

- [10] Kevin Black, Allen Z Ren, Michael Equi, and Sergey Levine. Training-time action conditioning for efficient real-time chunking. _arXiv preprint arXiv:2512.05964_ , 2025. 

- [11] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, Pete Florence, Chuyuan Fu, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Kehang Han, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning (CoRL)_ , 2023. 

- [12] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Tomas Jackson, Sally Jesmonth, et al. Rt-1: Robotics transformer for real-world control at scale. In _Robotics: Science and Systems_ , 2023. 

- [13] Jake Bruce, Michael Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, Yusuf Aytar, Sarah Bechtle, Feryal Behbahani, Stephanie Chan, Nicolas Heess, et al. Genie: Generative interactive environments. In _Int. Conf. Mach. Learn._ , 2024. 

- [14] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2502.14420_ , 2025. 

- [15] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, Weiliang Deng, Yubin Guo, Tian Nian, Xuanbing Xie, Qiangyu Chen, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 

- [16] Yi Chen, Yuying Ge, Weiliang Tang, Yizhuo Li, Yixiao Ge, Mingyu Ding, Ying Shan, and Xihui Liu. Moto: Latent motion token as the bridging language for robot manipulation. In _Int. Conf. Comput. Vis._ , 2025. 

- [17] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. In _Robotics: Science and Systems_ , 2023. 

- [18] Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Benjamin Burchfiel, Siyuan Feng, Russ Tedrake, and Shuran Song. Universal manipulation interface: In-the-wild robot teaching without in-the-wild robots. In _Robotics: Science and Systems_ , 2024. 

- [19] Chaorui Deng, Deyao Zhu, Kunchang Li, Chenhui Gou, Feng Li, Zeyu Wang, Shu Zhong, Weihao Yu, Xiaonan Nie, Ziang Song, Guang Shi, and Haoqi Fan. Emerging properties in unified multimodal pretraining. _arXiv preprint arXiv:2505.14683_ , 2025. 

- [20] Yilun Du, Mengjiao Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Joshua B. Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning universal policies via text-guided video generation. In _Adv. Neural Inform. Process. Syst._ , 2023. 

- [21] Yilun Du, Sherry Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Josh Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning universal policies via text-guided video generation. _Advances in neural information processing systems_ , 36:9156–9172, 2023. 

- [22] Yao Feng, Hengkai Tan, Xinyi Mao, Guodong Liu, Shuhe Huang, Chendong Xiang, Hang Su, and Jun Zhu. Vidar: Embodied video diffusion model for generalist bimanual manipulation. _arXiv preprint arXiv:2507.12898_ , 2025. 

19 

- [23] Google DeepMind. Veo: A text-to-video generation system. _Google DeepMind Technical Report_ , 2025. 

- [24] Yanjiang Guo, Yucheng Hu, Jianke Zhang, Yen-Jen Wang, Xiaoyu Chen, Chaochao Lu, and Jianyu Chen. Prediction with action: Visual policy learning via joint denoising process. In _Adv. Neural Inform. Process. Syst._ , 2024. 

- [25] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse control tasks through world models. _Nature_ , 2025. 

- [26] Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control. In _Int. Conf. Learn. Represent._ , 2024. 

- [27] Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with predictive visual representations. In _Int. Conf. Mach. Learn._ , 2025. 

- [28] Chi-Pin Huang, Yueh-Hua Wu, Min-Hung Chen, Yu-Chiang Frank Wang, and Fu-En Yang. Thinkact: Vision-language-action reasoning via reinforced visual latent planning. In _Adv. Neural Inform. Process. Syst._ , 2025. 

- [29] Physical Intelligence et al. _π_ 0 _._ 5: A generalist robot policy with flow matching and world models. In _Conference on Robot Learning (CoRL)_ , 2025. 

- [30] Dong Jing, Gang Wang, Jiaqi Liu, Weiliang Tang, Zelong Sun, Yunchao Yao, Zhenyu Wei, Yunhui Liu, Zhiwu Lu, and Mingyu Ding. Mixture of horizons in action chunking. _arXiv preprint arXiv:2511.19433_ , 2025. 

- [31] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, Peter David Fagan, Joey Hejna, Masha Itkina, Marion Lepert, Yecheng Jason Ma, et al. Droid: A large-scale in-the-wild robot manipulation dataset. In _Robotics: Science and Systems_ , 2024. 

- [32] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- [33] Moo Jin Kim, Yihuai Gao, Tsung-Yi Lin, Yen-Chen Lin, Yunhao Ge, Grace Lam, Percy Liang, Shuran Song, Ming-Yu Liu, Chelsea Finn, et al. Cosmos policy: Fine-tuning video models for visuomotor control and planning. _arXiv preprint arXiv:2601.16163_ , 2026. 

- [34] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, et al. Openvla: An open-source vision-language-action model. In _Conference on Robot Learning (CoRL)_ , 2024. 

- [35] Kuaishou. Kling ai. https://klingai.kuaishou.com/, 2024. 

- [36] Chenchang Li, Zihao Ai, Tong Wu, Xiaosa Li, Wenbo Ding, and Huazhe Xu. Deformnet: Latent space modeling and dynamics prediction for deformable object manipulation. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 14770–14776. IEEE, 2024. 

- [37] Hao Li, Shuai Yang, Yilun Chen, Yang Tian, Xiaoda Yang, Xinyi Chen, Hanqing Wang, Tai Wang, Feng Zhao, Dahua Lin, et al. Cronusvla: Transferring latent motion across time for multi-frame prediction in manipulation. _arXiv preprint arXiv:2506.19816_ , 2025. 

- [38] Haozhan Li, Yuxin Zuo, Jiale Yu, Yuhao Zhang, Zhaohui Yang, Kaiyan Zhang, Xuekai Zhu, Yuchen Zhang, Tianxing Chen, Ganqu Cui, et al. Simplevla-rl: Scaling vla training via reinforcement learning. _arXiv preprint arXiv:2509.09674_ , 2025. 

- [39] Jiacheng Li, Mengzhou Sun, Bowen Zhang, Zhe Zhao, Xiu Liu, et al. Gr-3 technical report. _arXiv preprint arXiv:2507.15493_ , 2025. 

- [40] Shuang Li, Yihuai Gao, Dorsa Sadigh, and Shuran Song. Unified video action model. In _Robotics: Science and Systems_ , 2025. 

- [41] Yunzhu Li, Jiajun Wu, Jun-Yan Zhu, Joshua B Tenenbaum, Antonio Torralba, and Russ Tedrake. Propagation networks for model-based control under partial observation. In _2019 International Conference on Robotics and Automation (ICRA)_ , pages 1205–1211. IEEE, 2019. 

- [42] Junbang Liang, Ruoshi Liu, Ege Ozguroglu, Sruthi Sudhakar, Achal Dave, Pavel Tokmakov, Shuran Song, and Carl Vondrick. Dreamitate: Real-world visuomotor policy learning via video generation. In _Conference on Robot Learning (CoRL)_ , 2024. 

- [43] Weixin Liang, LILI YU, Liang Luo, Srini Iyer, Ning Dong, Chunting Zhou, Gargi Ghosh, Mike Lewis, Wen tau Yih, Luke Zettlemoyer, and Xi Victoria Lin. Mixture-of-transformers: A sparse and scalable architecture for multi-modal foundation models. _Transactions on Machine Learning Research_ , 2025. 

20 

- [44] Zhixuan Liang, Yizhuo Li, Tianshuo Yang, Chengyue Wu, Sitong Mao, Tian Nian, Liuao Pei, Shunbo Zhou, Xiaokang Yang, Jiangmiao Pang, Yao Mu, and Ping Luo. Discrete diffusion vla: Bringing discrete diffusion to action decoding in vision-language-action policies. _arXiv preprint arXiv:2508.20072_ , 2025. 

- [45] Fanqi Lin, Yingdong Hu, Pingyue Sheng, Chuan Wen, Jiacheng You, and Yang Gao. Data scaling laws in imitation learning for robotic manipulation. In _Int. Conf. Learn. Represent._ , 2025. 

- [46] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. In _Int. Conf. Learn. Represent._ , 2023. 

- [47] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. In _Adv. Neural Inform. Process. Syst._ , 2023. 

- [48] Fangchen Liu, Chuanyu Li, Yihua Qin, Austin Shaw, Jing Xu, Pieter Abbeel, and Rui Chen. Vitamin: Learning contact-rich tasks through robot-free visuo-tactile manipulation interface. _arXiv preprint arXiv:2504.06156_ , 2025. 

- [49] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: A diffusion foundation model for bimanual manipulation. In _Int. Conf. Learn. Represent._ , 2025. 

- [50] Xingchao Liu, Chengyue Gong, and Qiang Liu. Flow straight and fast: Learning to generate and transfer data with rectified flow. In _Int. Conf. Learn. Represent._ , 2023. 

- [51] Zeyi Liu, Cheng Chi, Eric Cousineau, Naveen Kuppuswamy, Benjamin Burchfiel, and Shuran Song. Maniwav: Learning robot manipulation from in-the-wild audio-visual data. _arXiv preprint arXiv:2406.19464_ , 2024. 

- [52] Bethany Lusch, J Nathan Kutz, and Steven L Brunton. Deep learning for universal linear embeddings of nonlinear dynamics. _Nature communications_ , 9(1):4950, 2018. 

- [53] Open X-Embodiment Collaboration. Open x-embodiment: Robotic learning datasets and rt-x models. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2024. 

- [54] OpenAI. Video generation models as world simulators. _OpenAI Technical Report_ , 2024. 

- [55] Jonas Pai, Liam Achenbach, Victoriano Montesinos, Benedek Forrai, Oier Mees, and Elvis Nava. mimic-video: Video-action models for generalizable robot control beyond vlas. _arXiv preprint 2512.15692_ , 2025. 

- [56] Jack Parker-Holder, Philip Ball, Jake Bruce, Vibhavari Dasagi, Kristian Holsheimer, Christos Kaplanis, Alexandre Moufarek, Guy Scully, Jeremy Shar, Jimmy Shi, Stephen Spencer, Jessica Yung, Michael Dennis, Sultan Kenjeyev, Shangbang Long, et al. Genie 2: A large-scale foundation world model. https://deepmind.google/discover/blog/ genie-2-a-large-scale-foundation-world-model/, 2024. 

- [57] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models. In _Robotics: Science and Systems_ , 2025. 

- [58] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, and Xuelong Li. Spatialvla: Exploring spatial representations for visual-language-action model. In _Robotics: Science and Systems_ , 2025. 

- [59] Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J. Liu. Exploring the limits of transfer learning with a unified text-to-text transformer. _Journal of Machine Learning Research_ , 21(140):1–67, 2020. 

- [60] Omar Rayyan, John Abanes, Mahmoud Hafez, Anthony Tzes, and Fares Abu-Dakka. Mv-umi: A scalable multi-view interface for cross-embodiment learning. _arXiv preprint arXiv:2509.18757_ , 2025. 

- [61] Moritz Reuss, Jyothish Pari, Pulkit Agrawal, and Rudolf Lioutikov. Efficient diffusion transformer policies with mixture of expert denoisers for multitask learning. In _Int. Conf. Learn. Represent._ , 2025. 

- [62] Moritz Reuss, Hongyi Zhou, Marcel Rühle, Ömer Erdinç Ya˘gmurlu, Fabian Otto, and Rudolf Lioutikov. Flower: Democratizing generalist robot policies with efficient vision-language-action flow policies. In _Conference on Robot Learning (CoRL)_ , 2025. 

- [63] Bokui Shen, Zhenyu Jiang, Christopher Choy, Silvio Savarese, Leonidas J Guibas, Anima Anandkumar, and Yuke Zhu. Actionconditional implicit visual dynamics for deformable object manipulation. _The International Journal of Robotics Research_ , 43(4):437–455, 2024. 

- [64] Yichao Shen, Fangyun Wei, Zhiying Du, Yaobo Liang, Yan Lu, Jiaolong Yang, Nanning Zheng, and Baining Guo. Videovla: Video generators can be generalizable robot manipulators. _arXiv preprint arXiv:2512.06963_ , 2025. 

21 

- [65] Hao Shi, Bin Xie, Yingfei Liu, Lin Sun, Fengrong Liu, Tiancai Wang, Erjin Zhou, Haoqiang Fan, Xiangyu Zhang, and Gao Huang. Memoryvla: Perceptual-cognitive memory in vision-language-action models for robotic manipulation. _arXiv preprint arXiv:2508.19236_ , 2025. 

- [66] Haochen Shi, Huazhe Xu, Zhiao Huang, Yunzhu Li, and Jiajun Wu. Robocraft: Learning to see, simulate, and shape elastoplastic objects in 3d with graph networks. _The International Journal of Robotics Research_ , 43(4):533–549, 2024. 

- [67] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, Simon Alibert, Matthieu Cord, Thomas Wolf, and Remi Cadene. Smolvla: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

- [68] Ajay Sridhar, Jennifer Pan, Satvik Sharma, and Chelsea Finn. Memer: Scaling up memory for robot control via experience retrieval. _arXiv preprint arXiv:2510.20328_ , 2025. 

- [69] Deborah Sulsky, Shi-Jian Zhou, and Howard L Schreyer. Application of a particle-in-cell method to solid mechanics. _Computer physics communications_ , 87(1-2):236–252, 1995. 

- [70] Jiaming Tang, Yufei Sun, Yilong Zhao, Shang Yang, Yujun Lin, Zhuoyang Zhang, James Hou, Yao Lu, Zhijian Liu, and Song Han. Vlash: Real-time vlas via future-state-aware asynchronous inference. _arXiv preprint arXiv:2512.01031_ , 2025. 

- [71] Gemini Robotics Team, Coline Devin, Yilun Du, Debidatta Dwibedi, Ruiqi Gao, Abhishek Jindal, Thomas Kipf, Sean Kirmani, Fangchen Liu, Anirudha Majumdar, et al. Evaluating gemini robotics policies in a veo world simulator. _arXiv preprint arXiv:2512.10675_ , 2025. 

- [72] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, et al. Octo: An open-source generalist robot policy. In _Robotics: Science and Systems_ , 2024. 

- [73] Yang Tian, Sizhe Yang, Jia Zeng, Ping Wang, Dahua Lin, Hao Dong, and Jiangmiao Pang. Seer: Predictive inverse dynamics models are scalable learners for robotic manipulation. In _Int. Conf. Learn. Represent._ , 2025. 

- [74] Yang Tian, Yuyin Yang, Yiman Xie, Zetao Cai, Xu Shi, Ning Gao, Hangxu Liu, Xuekun Jiang, Zherui Qiu, Feng Yuan, Yaping Li, Ping Wang, Junhao Cai, Jia Zeng, Hao Dong, et al. Interndata-a1: Pioneering high-fidelity synthetic data for pre-training generalist policy. _arXiv preprint arXiv:2511.16651_ , 2025. 

- [75] Alexander Tong, Kilian Fatras, Nikolay Malkin, Guillaume Huguet, Yanlei Zhang, Jarrid Rector-Brooks, Guy Wolf, and Yoshua Bengio. Improving and generalizing flow-based generative models with minibatch optimal transport. _Transactions on Machine Learning Research_ , 2024. 

- [76] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. In _Adv. Neural Inform. Process. Syst._ , 2017. 

- [77] Yixuan Wang, Yunzhu Li, Katherine Driggs-Campbell, Li Fei-Fei, and Jiajun Wu. Dynamic-resolution model learning for object pile manipulation. _arXiv preprint arXiv:2306.16700_ , 2023. 

- [78] Yuqi Wang, Xinghang Li, Wenxuan Wang, Junbo Zhang, Yingyan Li, Yuntao Chen, Xinlong Wang, and Zhaoxiang Zhang. Unified vision-language-action model. _arXiv preprint arXiv:2506.19850_ , 2025. 

- [79] WanTeam. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_ , 2025. 

- [80] Manuel Watter, Jost Springenberg, Joschka Boedecker, and Martin Riedmiller. Embed to control: A locally linear latent dynamics model for control from raw images. _Advances in neural information processing systems_ , 28, 2015. 

- [81] Kun Wu, Chengkai Hou, Jiaming Liu, Zhengping Che, Xiaozhu Ju, Zhuqin Yang, Meng Li, Yinuo Zhao, Zhiyuan Xu, Guang Yang, Shichao Fan, Xinhua Wang, Fei Liao, Zhen Zhao, Guangyu Li, et al. Robomind: Benchmark on multi-embodiment intelligence normative data for robot manipulation. In _Robotics: Science and Systems_ , 2025. 

- [82] Philipp Wu, Alejandro Escontrela, Danijar Hafner, Pieter Abbeel, and Ken Goldberg. Daydreamer: World models for physical robot learning. In _Conference on Robot Learning (CoRL)_ , 2022. 

- [83] Philipp Wu, Alejandro Escontrela, Danijar Hafner, Pieter Abbeel, and Ken Goldberg. Daydreamer: World models for physical robot learning. In _Conference on robot learning_ , pages 2226–2240. PMLR, 2023. 

- [84] Shihan Wu, Xuecheng Liu, Shaoxuan Xie, Pengwei Wang, Xinghang Li, Bowen Yang, Zhe Li, Kai Zhu, Hongyu Wu, Yiheng Liu, Zhaoye Long, Yue Wang, Chong Liu, Dihan Wang, Ziqiang Ni, et al. Robocoin: An open-sourced bimanual robotic data collection for integrated manipulation. _arXiv preprint arXiv:2511.17441_ , 2025. 

22 

- [85] Zhenjia Xu, Jiajun Wu, Andy Zeng, Joshua B Tenenbaum, and Shuran Song. Densephysnet: Learning dense physical object representations via multi-step dynamic interactions. _arXiv preprint arXiv:1906.03853_ , 2019. 

- [86] Mengjiao Yang, Yilun Du, Kamyar Ghasemipour, Jonathan Tompson, Leslie Pack Kaelbling, Dale Schuurmans, and Pieter Abbeel. Unisim: Learning interactive real-world simulators. In _Int. Conf. Learn. Represent._ , 2024. 

- [87] Shuai Yang, Hao Li, Yilun Chen, Bin Wang, Yang Tian, Tai Wang, Hanqing Wang, Feng Zhao, Yiyi Liao, and Jiangmiao Pang. Instructvla: Vision-language-action instruction tuning from understanding to manipulation. _arXiv preprint arXiv:2507.17520_ , 2025. 

- [88] Kaifeng Zhang, Baoyu Li, Kris Hauser, and Yunzhu Li. Adaptigraph: Material-adaptive graph-based neural dynamics for robotic manipulation. _arXiv preprint arXiv:2407.07889_ , 2024. 

- [89] Kaifeng Zhang, Baoyu Li, Kris Hauser, and Yunzhu Li. Particle-grid neural dynamics for learning deformable object models from rgb-d videos. _arXiv preprint arXiv:2506.15680_ , 2025. 

- [90] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1702–1713, 2025. 

- [91] Tony Z. Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. In _Robotics: Science and Systems_ , 2023. 

- [92] Zhaxizhuoma, Kehui Liu, Chuyue Guan, Zhongjie Jia, Ziniu Wu, Xin Liu, Tianyu Wang, Shuai Liang, Pengan Chen, Pingrui Zhang, Haoming Song, Delin Qu, Dong Wang, Zhigang Wang, Nieqing Cao, et al. Fastumi: A scalable and hardwareindependent universal manipulation interface. _arXiv preprint arXiv:2409.19499_ , 2024. 

- [93] Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng, Jiayin Zou, Yilun Chen, Jia Zeng, Ya-Qin Zhang, Jiangmiao Pang, Jingjing Liu, Tai Wang, and Xianyuan Zhan. X-vla: Soft-prompted transformer as scalable cross-embodiment vision-language-action model. _arXiv preprint arXiv:2510.10274_ , 2025. 

- [94] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daumé III, Andrey Kolobov, Furong Huang, and Jianwei Yang. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv preprint arXiv:2412.10345_ , 2024. 

- [95] Pengfei Zhou, Liliang Chen, Shengcong Chen, Di Chen, Wenzhi Zhao, Rongjun Jin, Guanghui Ren, and Jianlan Luo. Act2goal: From world model to general goal-conditioned policy. _arXiv preprint arXiv:2512.23541_ , 2025. 

- [96] Siyuan Zhou, Yilun Du, Jiaben Chen, Yandong Li, Dit-Yan Yeung, and Chuang Gan. Robodreamer: Learning compositional world models for robot imagination. _arXiv preprint arXiv:2404.12377_ , 2024. 

- [97] Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin Burchfiel, Paarth Shah, and Abhishek Gupta. Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. In _Robotics: Science and Systems_ , 2025. 

## **Appendix** 

## **A Real-world Evaluation Details** 

We present detailed evaluation results for all real-world manipulation tasks. Each task is evaluated with 20 trials for both our method and the baseline ( _π_ 0 _._ 5). To ensure fair comparison, we adopt an alternating evaluation protocol: one trial with _π_ 0 _._ 5, followed by one trial with our method, and so on. 

For each trial, we record the success status of every intermediate step. If a step requires a retry to succeed, we assign a score of 0.5; if it fails, the score is 0; if it succeeds on the first attempt, the score is 1. A trial is marked as successful only if all steps are completed (i.e., the total score equals the maximum possible score). 

We report two metrics: 

- **Progress Score (PS)** : The average score across all trials divided by the maximum possible score, expressed as a percentage: PS =<sup>Avera</sup> Max Steps<sup><u>ge Progress</u></sup> _×_ 100%. 

- **Success Rate (SR)** : The number of successful trials divided by the total number of trials, expressed as a percentage: SR =<sup><u># Successful Trials</u></sup> _N ×_ 100%. 

23 

We evaluate on six diverse real-world tasks: **Make Breakfast** (10 steps: preparing a complete breakfast including toasting bread, pouring water, and plating), **Pick Screws** (5 steps: picking up paper, pouring screws, and inserting three screws), **Fold Clothes** (6 steps: folding a shirt including sleeves and smoothing), **Unpack Delivery** (5 steps: opening a package using a utility knife), **Insert Tubes** (2 categories: grasping and inserting 3 tubes), and **Fold Pants** (3 steps: folding pants and placing them). These tasks span long-horizon sequential manipulation, precision control, and deformable object handling. The following tables present per-trial results for each task. 

24 

**Table S1.** _Evaluation on RoboTwin 2.0 Simulation (Easy vs Hard, 50 tasks)_ . RoboTwin 2.0 is a challenging bimanual manipulation benchmark requiring coordinated dual-arm control. Easy uses fixed initial configurations while Hard involves randomized object poses and scene layouts. 

|**Simulation Task**|**Horizon**|**O**|**urs**|_π_0|[7]|_π_0_._|5 [7]|X-VL|A [93]|Mot|us [5]|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||Easy|Hard|Easy|Hard|Easy|Hard|Easy|Hard|Easy|Hard|
|_Adjust Bottle_|1|90%|94%|99%|95%|**100%**|**99%**|**100%**|**99%**|89%|93%|
|<br>_Beat Block Hammer_|1|**96%**|98%|79%|84%|**96%**|93%|92%|88%|95%|88%|
|_Blocks Ranking RGB_|3|**99%**|98%|80%|63%|92%|85%|83%|83%|**99%**|97%|
|_Blocks Ranking Size_|3|**94%**|96%|14%|5%|49%|26%|67%|74%|75%|63%|
|_Click Alarmclock_|1|99%|**100%**|77%|68%|98%|89%|99%|99%|**100% **|**100%**|
|_Click Bell_|1|**100% **|**100%**|71%|48%|**99%**|66%|**100% **|**100% **|**100% **|**100%**|
|_Dump Bin Bigbin_|1|89%|96%|88%|83%|92%|**97%**|79%|77%|**95%**|91%|
|<br>_Grab Roller_|1|**100% **|**100%**|98%|94%|**100% **|**100% **|**100% **|**100% **|**100% **|**100%**|
|_Handover Block_|2|99%|78%|47%|31%|66%|57%|73%|37%|86%|73%|
|_Handover Mic_|2|94%|96%|**97%**|**97%**|**98%**|**97%**|0%|0%|78%|63%|
|_Hanging Mug_|2|**40%**|28%|14%|11%|18%|17%|23%|27%|**38%**|**38%**|
|_Lift Pot_|1|**100%**|99%|80%|72%|96%|85%|**99%**|**100%**|96%|**99%**|
|<br>_Move Can Pot_|1|94%|97%|**68%**|48%|51%|55%|89%|86%|34%|74%|
|_Move Pillbottle Pad_|1|**99%**|99%|67%|46%|84%|61%|73%|71%|93%|**96%**|
|_Move Playingcard Away_|1|**100%**|99%|74%|65%|96%|84%|93%|**98%**|**100%**|96%|
|_Move Stapler Pad_|1|91%|79%|41%|24%|56%|42%|78%|73%|**83%**|**85%**|
|_Open Laptop_|1|92%|94%|71%|81%|90%|96%|93%|**100%**|95%|91%|
|_Open Microwave_|1|82%|86%|4%|32%|34%|**77%**|**79%**|71%|**95%**|**91%**|
|_Pick Diverse Bottles_|2|89%|82%|69%|31%|81%|71%|58%|36%|90%|**91%**|
|_Pick Dual Bottles_|2|**100%**|99%|59%|37%|93%|63%|47%|36%|96%|90%|
|_Place A2B Left_|1|**97%**|93%|43%|47%|87%|82%|48%|49%|82%|79%|
|_Place A2B Right_|1|**97%**|95%|39%|34%|87%|84%|36%|36%|90%|**87%**|
|_Place Bread Basket_|1|**97%**|95%|62%|46%|77%|64%|81%|71%|91%|**94%**|
|_Place Bread Skillet_|2|95%|90%|66%|49%|**85%**|66%|77%|67%|86%|**83%**|
|_Place Burger Fries_|2|97%|95%|81%|76%|**94%**|87%|**94%**|**94%**|**98%**|**98%**|
|<br>_Place Can Basket_|2|81%|84%|55%|46%|**62%**|**62%**|49%|52%|**81%**|76%|
|_Place Cans Plasticbox_|2|**100%**|99%|63%|45%|94%|84%|**97%**|**98%**|**98%**|94%|
|_Place Container Plate_|1|99%|97%|**97%**|92%|**99%**|95%|**97%**|95%|98%|**99%**|
|_Place Dual Shoes_|2|94%|89%|59%|51%|75%|75%|79%|**88%**|93%|87%|
|_Place Empty Cup_|1|**100% **|**100%**|91%|85%|**100%**|99%|**100%**|98%|99%|98%|
|_Place Fan_|1|99%|93%|66%|71%|**87%**|85%|80%|75%|**91%**|87%|
|_Place Mouse Pad_|1|93%|96%|20%|20%|**60%**|39%|**70%**|**70%**|66%|68%|
|_Place Object Basket_|2|91%|88%|67%|70%|80%|76%|44%|39%|81%|**87%**|
|_Place Object Scale_|1|96%|95%|57%|52%|**86%**|80%|52%|74%|88%|85%|
|_Place Object Stand_|1|**99%**|96%|82%|68%|91%|85%|86%|88%|**98%**|**97%**|
|_Place Phone Stand_|1|**97%**|97%|49%|53%|81%|81%|**88%**|87%|87%|86%|
|_Place Shoe_|1|98%|98%|76%|76%|92%|93%|**96%**|95%|**99%**|**97%**|
|_Press Stapler_|1|85%|82%|44%|37%|87%|83%|**92%**|**98%**|93%|**98%**|
|_Put Bottles Dustbin_|3|87%|91%|65%|56%|**84%**|79%|74%|77%|81%|79%|
|_Put Object Cabinet_|2|85%|87%|73%|60%|**80%**|**79%**|46%|48%|**88%**|71%|
|_Rotate QRcode_|1|**96%**|91%|74%|70%|89%|87%|34%|33%|**89%**|73%|
|<br>_Scan Object_|2|96%|91%|55%|42%|72%|65%|14%|36%|67%|66%|
|<br>_Shake Bottle Horizontally_|1|**100%**|99%|98%|92%|**99%**|**99%**|**100% **|**100% **|**100%**|98%|
|<br>_Shake Bottle_|1|**100%**|97%|94%|91%|**99%**|97%|**99%**|**100% **|**100%**|**97%**|
|_Stack Blocks Three_|3|99%|98%|72%|52%|91%|76%|6%|10%|91%|**95%**|
|_Stack Blocks Two_|2|**100%**|98%|93%|79%|97%|**100%**|92%|87%|**100%**|98%|
|_Stack Bowls Three_|3|86%|83%|**77%**|75%|**77%**|71%|76%|**86%**|79%|**87%**|
|_Stack Bowls Two_|2|94%|98%|94%|95%|95%|96%|96%|93%|**98%**|**98%**|
|_Stamp Seal_|1|96%|97%|46%|33%|79%|55%|76%|82%|93%|92%|
|_Turn Switch_|1|44%|45%|41%|42%|**62%**|54%|40%|61%|**84%**|**78%**|
|**Average (%)**|–|**92.93**|**91.55**|65.92|58.40|82.74|76.76|72.80|72.84|88.66|87.02|


25 

**Table S2.** Detailed evaluation results for Make Breakfast task (10 steps, max score 10). 

|**Trial**|**Succ.**|**Grasp**<br>**Plate**|**Grasp**<br>**Bread**|**Grasp**<br>**Fork**|**Place**<br>**Bread**|**Press**<br>**Toaster**|**Grasp**<br>**Cup**|**Grasp**<br>**Kettle**|**Pour**|**Grasp**<br>**Apple**|**Serve**|**Prog.**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||**Ours**|||||||
|1|0|1|1|1|1|1|1|1|0|1|1|9|
|2|1|1|1|1|1|1|1|1|1|1|1|10|
|3|1|1|1|1|1|1|1|1|1|1|1|10|
|4|1|1|1|1|1|1|1|1|1|1|1|10|
|5|1|1|1|1|1|1|1|1|1|1|1|10|
|6|1|1|1|1|1|1|1|1|1|1|1|10|
|7|0|1|1|1|1|1|1|1|1|1|0|9|
|8|1|1|1|1|1|1|1|1|1|0.5|1|9.5|
|9|0|1|1|1|0|1|1|1|1|1|1|9|
|10|1|1|1|1|1|1|1|1|1|1|1|10|
|11|0|1|1|1|1|1|1|1|0|1|1|9|
|12|1|1|1|1|1|1|1|1|1|1|1|10|
|13|0|1|1|1|0|1|1|1|1|1|1|9|
|14|1|1|1|1|1|1|1|1|1|1|1|10|
|15|1|1|1|1|1|1|1|1|1|1|1|10|
|16|1|1|1|1|1|1|1|1|1|1|1|10|
|17|1|1|1|1|1|1|1|1|1|0.5|1|9.5|
|18|1|1|1|1|1|1|1|1|1|1|1|10|
|19|1|1|1|1|1|1|1|1|1|1|1|10|
|20|1|1|1|1|1|1|1|1|1|1|1|10|
|**Avg**|**0.75**|**1.00**|**1.00**|**1.00**|**0.90**|**1.00**|**1.00**|**1.00**|**0.90**|**0.95**|**0.95**|**9.70**|
|**Progress Score**|||||**9**|**7.0%**(= 9.70/1|0_×_100%)||||||
|<br>**Success Rate**|||||**7**|<br>**5.0%**(= 15/2|<br>0_×_100%)||||||
|||||||**_π_0****_._5**|||||||
|1|0|1|1|1|1|0|0|0|0|0|0|4|
|2|1|1|1|1|1|1|1|1|0|1|1|9|
|3|1|1|1|1|1|1|1|1|0|1|1|9|
|4|1|1|1|1|1|0|0|1|1|1|1|8|
|5|0|1|1|1|0|1|0|1|1|0|1|7|
|6|1|1|1|1|1|1|1|1|0|1|1|9|
|7|1|1|1|0|1|1|1|1|0|1|1|8|
|8|0|1|1|1|1|1|1|1|1|1|0|9|
|9|0|1|1|0|1|0|1|1|0|0|0|5|
|10|0|1|1|1|1|0|0|0|0|0|0|4|
|11|1|1|1|1|1|0|0|1|1|1|1|8|
|12|1|1|1|1|0|0|0|1|1|1|1|7|
|13|1|1|1|0|1|0|0|1|1|1|1|7|
|14|1|1|1|1|0|1|0|1|1|1|1|8|
|15|1|1|1|1|1|0|0|1|1|1|1|8|
|16|1|1|1|1|0|1|0|1|1|1|1|8|
|17|1|1|1|1|1|1|0|1|1|1|1|9|
|18|1|1|1|1|1|1|1|0|0|1|1|8|
|19|1|1|1|0|1|0|0|1|0|1|1|6|
|20|0|1|1|1|0|1|0|0|0|1|0|5|
|**Avg**|**0.70**|**1.00**|**1.00**|**0.80**|**0.75**|**0.55**|**0.35**|**0.80**|**0.50**|**0.80**|**0.75**|**7.30**|
|**Progress Score**<br>**Success Rate**|||||**7**<br>**7**|**3.0%**(= 7.30/1<br>**0.0%**(= 14/2|0_×_100%)<br>0_×_100%)||||||


26 

**Table S3.** Detailed evaluation results for Pick Screws task (5 steps, max score 5). 

|**Trial**|**Success**|**Grab Paper**|**Pour Screws**|**Screw 1**|**Screw 2**|**Screw 3**|**Progress**|
|---|---|---|---|---|---|---|---|
||||**Ours**|||||
|1|1|1|1|0.5|0.5|1|4|
|2|0|1|0|1|1|0.5|3.5|
|3|1|1|1|1|0.5|0.5|4|
|4|1|1|1|1|1|1|5|
|5<br>|1<br>|1<br>|1<br>|1<br>|1<br>|0.5<br>|4.5<br>|
|6|1|1|1|0.5|1|0.5|4|
|7|1|1|1|1|1|1|5|
|8|1|1|1|1|1|1|5|
|9|0|1|0|0|0|0|1|
|10|1|1|1|1|1|1|5|
|11|1|1|1|1|1|1|5|
|12|0|1|0|1|1|1|4|
|13|0|1|0|1|1|1|4|
|14|1|1|1|1|0.5|0.5|4|
|15|0|1|0|0|0.5|1|2.5|
|16|1|1|1|1|1|1|5|
|17|1|1|1|1|1|0.5|4.5|
|18|1|1|1|0.5|0.5|1|4|
|19|0|1|1|0|1|0.5|3.5|
|20|1|1|1|1|1|1|5|
|**Avg**|**0.70**|**1.00**|**0.75**|**0.78**|**0.83**|**0.78**|**4.13**|
|**Progress Score**|||**82.5%**(=|4.13/5_×_100|%)|||
|**Success Rate**|||**70.0%**(=|14/20_×_100|%)|||
||||**_π_0****_._5**|||||
|1|0|1|0|1|1|1|4|
|2|0|0.5|0|1|1|0.5|3|
|3|1|1|1|1|1|1|5|
|4|0|1|0|1|0.5|0.5|3|
|5|1|1|1|0.5|1|0.5|4|
|6|1|1|1|1|0.5|1|4.5|
|7|1|1|1|1|1|1|5|
|8|1|1|1|0.5|0.5|1|4|
|9|0|1|0|0.5|0.5|0|2|
|10|1|1|1|1|1|1|5|
|11|1|1|1|0.5|1|1|4.5|
|12|0|1|0|1|1|0.5|3.5|
|13|0|1|1|1|0|0.5|3.5|
|14|1|1|1|0.5|1|1|4.5|
|15|0|1|1|1|1|0|4|
|16|1|1|1|1|1|1|5|
|17|0|0|0|1|0.5|0.5|2|
|18|0|0|0|0|0|0|0|
|19|0|1|0|1|0.5|0.5|3|
|20|1|1|1|1|1|0.5|4.5|
|**Avg**<br>|**0.50**|**0.88**|**0.60**<br>|**0.83**<br>|**0.75**<br>|**0.65**|**3.70**|
|**Progress Score**|||**74.0%**(=|3.70/5_×_100|%)|||
|**Success Rate**|||**50.0%**(=|10/20_×_100|%)|||


27 

**Table S4.** Detailed evaluation results for Fold Clothes task (6 steps, max score 6). 

|**Trial**|**Success**|**Fold Half**|**Left Sleeve**|**Right Sleeve**|**Fold Again**|**Flatten**|**Place**|**Progress**|
|---|---|---|---|---|---|---|---|---|
|||||**Ours**|||||
|1|1|1|1|1|1|1|1|6|
|2|0|1|1|0|0|0|0|2|
|3|1|1|1|1|1|0.5|0.5|5|
|4|1|1|1|1|1|1|1|6|
|5|0|0.5|0|0|0|0|0|0.5|
|6|0|0|0|0|0|0|0|0|
|7|0|0.5|0|0|0|0|0|0.5|
|8|1|1|1|1|1|0.5|0.5|5|
|9|1|1|1|1|1|1|1|6|
|10|1|1|1|1|1|1|1|6|
|11|0|0.5|0|0|0|0|0|0.5|
|12|0|0.5|0|0|0|0|0|0.5|
|13|0|0.5|0|0|0|0|0|0.5|
|14|0|1|1|1|1|1|0|5|
|15|0|0.5|0|0|0|0|0|0.5|
|16|0|1|1|1|1|0.5|0|4.5|
|17|0|0|0|0|0|0|0|0|
|18|0|1|1|1|0.5|0|0|3.5|
|19|0|0.5|0|0|0|0|0|0.5|
|20|1|1|1|1|1|1|1|6|
|**Avg**|**0.35**|**0.73**|**0.55**|**0.50**|**0.48**|**0.38**|**0.30**|**2.93**|
|**Progress Score**||||**48.8%**(= 2.93/6|_×_100%)||||
|<br>**Success Rate**||||<br>**35.0%**(= 7/20_×_|<br> 100%)||||
|||||**_π_0****_._5**|||||
|1|1|1|1|1|1|1|1|6|
|2|1|1|1|1|1|1|1|6|
|3|1|1|1|1|0.5|1|0.5|5|
|4|0|1|1|1|0.5|1|0|4.5|
|5|0|0.5|1|1|0.5|1|0|4|
|6|0|1|1|0.5|1|1|0|4.5|
|7|0|0.5|0|0|0|0|0|0.5|
|8|0|0.5|0|0|0|0|0|0.5|
|9|0|1|1|1|1|1|0|5|
|10|0|0.5|1|1|0.5|0|0|3|
|11|0|0.5|0|0|0|0|0|0.5|
|12|0|1|1|1|1|1|0|5|
|13|0|1|1|0.5|0|0|0|2.5|
|14|1|1|1|1|1|1|1|6|
|15|1|1|1|1|0.5|1|1|5.5|
|16|0|1|1|1|0.5|0|0|3.5|
|17|1|1|1|1|1|1|1|6|
|18|0|1|1|1|0.5|1|0|4.5|
|19|0|0|0|0|0|0|0|0|
|20|0|1|1|1|0|0|0|3|
|**Avg**<br>|**0.30**|**0.83**|**0.80**|**0.75**<br>|**0.53**<br>|**0.60**|**0.28**|**3.78**|
|**Progress Score**||||**62.9%**(= 3.78/6|_×_100%)||||
|<br>**Success Rate**||||<br>**30.0%**(= 6/20_×_|<br> 100%)||||


28 

**Table S5.** Detailed evaluation results for Unpack Delivery task (5 steps, max score 5). 

|**Trial**|**Success**|**Grab Knife**|**Push Blade**|**Handove**|**r**<br>**Cut Seal**|**Open Lid**|**Progress**|
|---|---|---|---|---|---|---|---|
||||**Ours**|||||
|1|1|1|1|1|1|1|5|
|2<br>|1<br>|1<br>|1<br>|1<br>|1<br>|1<br>|5<br>|
|3|1|1|1|1|1|1|5|
|4|0|1|0|0|0|0|1|
|5<br>|0<br>|1<br>|1<br>|1<br>|0.5<br>|0<br>|3.5<br>|
|6|0|1|1|1|0|0|3|
|7|1|1|1|1|1|1|5|
|8|0|1|1|1|0|0|3|
|9|1|1|1|1|1|1|5|
|10|1|1|1|1|1|1|5|
|11|1|1|1|1|1|1|5|
|12|1|1|1|1|1|1|5|
|13|0|1|1|1|0|0|3|
|14|1|1|1|1|1|1|5|
|15|1|1|1|1|1|1|5|
|16|0|1|1|1|0|0|3|
|17|1|1|1|1|0.5|1|4.5|
|18|1|1|1|1|1|1|5|
|19|0|1|1|1|0.5|0|3.5|
|20|1|1|1|1|1|1|5|
|**Avg**|**0.65**|**1.00**|**0.95**|**0.95**|**0.68**|**0.65**|**4.23**|
|**Progress Score**<br>|||**84.5%**(<br>|= 4.23/5_×_ <br>|100%)<br>|||
|**Success Rate**|||**65.0%**(|= 13/20_×_|100%)|||
||||**_π_0****_._5**|||||
|1|0|1|1|0.5|0.5|0|3|
|2|0|1|1|1|0|0|3|
|3|0|1|1|1|0.5|0|3.5|
|4|0|1|1|1|0.5|0|3.5|
|5|0|1|1|1|0.5|0|3.5|
|6|0|1|1|1|0|0|3|
|7|0|1|1|1|0|0|3|
|8|1|1|1|1|0.5|1|4.5|
|9|0|1|1|1|0.5|0|3.5|
|10|1|1|1|1|1|1|5|
|11|0|1|1|1|0.5|0|3.5|
|12|0|1|1|1|0.5|0|3.5|
|13|1|1|1|1|1|1|5|
|14|0|1|1|1|0.5|0|3.5|
|15|1|1|1|1|0.5|1|4.5|
|16|0|1|1|1|0|0|3|
|17|0|1|1|1|0|0|3|
|18|0|1|1|1|0|0|3|
|19|0|1|1|1|0.5|0|3.5|
|20|1|1|1|1|1|1|5|
|**Avg**<br>|**0.25**|**1.00**|**1.00**<br>|**0.98**<br>|**0.43**<br>|**0.25**|**3.65**|
|**Progress Score**|||**73.0%**(|= 3.65/5_×_|100%)|||
|<br>**Success Rate**|||**25.0%**|(= 5/20_×_|100%)|||


29 

**Table S6.** Detailed evaluation results for Insert Tubes task (2 categories: Grasp and Insert, max score 6). 

|**Trial**|**Success**|**Grasp (3)**<br>**Insert (3)**|**Progress**|
|---|---|---|---|
|||**Ours**||
|1|0|3<br>2|5|
|2<br>|1<br>|3<br>3<br><br>|6<br>|
|3<br>|0<br>|3<br>2<br><br>|5<br>|
|4|0|2<br>2|4|
|5|1|3<br>3|6|
|6|1|3<br>3|6|
|7|0|3<br>2|5|
|8|1|3<br>3|6|
|9|0|3<br>2|5|
|10|0|3<br>2|5|
|11|1|3<br>3|6|
|12|0|3<br>2|5|
|13|1|3<br>3|6<br>|
|14|0|3<br>2|5|
|15|0|3<br>1|4|
|16|1|3<br>3|6|
|17|0|2<br>2|4|
|18<br>|0<br>|2<br>2<br><br>|4<br>|
|19|1|3<br>3|6|
|20|0|2<br>2|4|
|**Avg**|**0.40**|**2.80**<br>**2.35**|**5.15**|
|**Progress Score**||**85.8%**(= 5.15/6_×_100%)||
|<br>**Success Rate**||<br>**40.0%**(= 8/20_×_100%)||
|||**_π_0****_._5**||
|1|0|3<br>1|4|
|2|0|3<br>1|4|
|3|0|3<br>1|4|
|4|0|3<br>1|4|
|5|0|3<br>1|4|
|6|0|3<br>1|4|
|7|0|3<br>1|4|
|8|0|3<br>2|5|
|9|1|3<br>3|6|
|10|1|3<br>3|6|
|11|1|3<br>3|6|
|12|0|2<br>1|3|
|13|0|3<br>2|5|
|14|0|2<br>2|4|
|15|1|3<br>3|6|
|16|1|3<br>3|6|
|17|0|3<br>2|5|
|18|0|2<br>2|4|
|19|1|3<br>3|6|
|20|0|3<br>2|5|
|**Avg**<br>|**0.30**|**2.85**<br>**1.90**<br>|**4.75**|
|**Progress Score**||**79.2%**(= 4.75/6_×_100%)||
|<br>**Success Rate**||**30.0%**(= 6/20_×_100%)||


30 

**Table S7.** Detailed evaluation results for Fold Pants task (3 steps, max score 3). 

|**Trial**|**Success**|**Fold 1**|**Fold 2**|**Place**|**Progress**|
|---|---|---|---|---|---|
|||**Ours**||||
|1|1|1|1|1|3|
|2<br>|1<br>|1<br>|1<br>|1<br>|3<br>|
|3<br>|1<br>|1<br>|1<br>|1<br>|3<br>|
|4|0|0|0|0|0|
|5|0|1|0|0|1|
|6|0|1|0|0|1|
|7|1|1|1|1|3|
|8|1|1|1|1|3|
|9|1|1|1|1|3|
|10|1|1|1|1|3|
|11|1|1|1|1|3|
|12|1|1|1|1|3|
|13|1|1|1|1|3|
|14|1|1|1|1|3|
|15|1|1|1|1|3|
|16|1|1|1|1|3|
|17|1|1|1|1|3|
|18|0|1|0|0|1|
|19|0|1|0|0|1|
|20|0|0|0|0|0|
|**Avg**|**0.70**|**0.90**|**0.70**|**0.70**|**2.30**|
|**Progress Score**||**76.7%**|(= 2.30/3_×_|100%)||
|**Success Rate**||**70.0%**|(= 14/20_×_|100%)||
|||**_π_0****_._5**||||
|1|1|1|1|1|3|
|2|1|1|1|1|3|
|3|1|1|1|1|3|
|4|0|0|0|0|0|
|5|0|0|0|0|0|
|6|0|0|0|0|0|
|7|0|0|0|0|0|
|8|0|0|0|0|0|
|9|0|0|0|0|0|
|10|0|0|0|0|0|
|11|1|1|1|1|3|
|12|1|1|1|1|3|
|13|1|1|1|1|3|
|14|0|0|0|0|0|
|15|0|0|0|0|0|
|16|0|0|0|0|0|
|17|0|0|0|0|0|
|18|0|0|0|0|0|
|19|0|0|0|0|0|
|20|0|0|0|0|0|
|**Avg**|**0.30**|**0.30**|**0.30**|**0.30**|**0.90**|
|**Progress Score**||**30.0%**|(= 0.90/3_×_|100%)||
|<br>**Success Rate**||<br>**30.0%**|<br>(= 6/20_×_|<br>100%)||


31 

