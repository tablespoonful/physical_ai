---
title: "SCRIPT: Scalable Diffusion Policy with Multi-stage Training for Language-driven Physics-Based Humanoid Control"
date: "2026-05-21"
authors: "Jingyan Zhang; Han Liang; Ruichi Zhang; Bin Li; Juze Zhang; Xin Chen"
url: https://arxiv.org/abs/2605.22894
pdf: https://arxiv.org/pdf/2605.22894
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.22894)** / [論文ページ](https://arxiv.org/abs/2605.22894)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# SCRIPT: Scalable Diffusion Policy with Multi-stage Training for Language-driven Physics-Based Humanoid Control 

JINGYAN ZHANG, ShanghaiTech University, China HAN LIANG<sup>†</sup> , ByteDance Seed, China RUICHI ZHANG, University of Pennsylvania, USA BIN LI, ShanghaiTech University, China JUZE ZHANG, Stanford University, USA XIN CHEN, ByteDance Seed, USA JINGYA WANG, ShanghaiTech University, China LAN XU, ShanghaiTech University, China JINGYI YU<sup>‡</sup> , ShanghaiTech University, China 


Fig. 1. SCRIPT translates natural-language motion descriptions (left) into physically simulated humanoid behavior (right) under closed-loop dynamics. 

†Project leader. 

‡Corresponding author. 

Authors’ Contact Information: Jingyan Zhang, ShanghaiTech University, Shanghai, China, zhangjy7@shanghaitech.edu.cn; Han Liang, ByteDance Seed, Shanghai, China, lianghan@shanghaitech.edu.cn; Ruichi Zhang, University of Pennsylvania, Philadelphia, USA, rczhang@seas.upenn.edu; Bin Li, ShanghaiTech University, Shanghai, China, libin3@shanghaitech.edu.cn; Juze Zhang, Stanford University, Stanford, USA, juze@stanford.edu; Xin Chen, ByteDance Seed, San Jose, USA, chenxin2@shanghaitech.edu.cn; Jingya Wang, ShanghaiTech University, Shanghai, China, wangjingya@shanghaitech.edu.cn; Lan Xu, ShanghaiTech University, Shanghai, China, xulan1@shanghaitech.edu.cn; Jingyi Yu, ShanghaiTech University, Shanghai, China, yujingyi@shanghaitech.edu.cn. 

Controlling physics-based humanoids from natural-language instructions is a critical step toward general-purpose embodied agents. However, existing methods remain constrained by a tension between semantic expressiveness and physical feasibility, often failing to jointly achieve faithful instruction following, high-quality motion, and stable long-horizon control. We propose SCRIPT, a scalable diffusion policy with a multi-stage training framework for language-driven physics-based humanoid control. The core of SCRIPT 

_SA Conference Papers ’26, Kuala Lumpur, Malaysia_ © 2026 Copyright held by the owner/author(s). ACM ISBN 979-8-4007-2842-6/2026/12 https://doi.org/10.1145/3829340.3842344 

This work is licensed under a Creative Commons Attribution 4.0 International License. 

SA Conference Papers ’26, December 01–04, 2026, Kuala Lumpur, Malaysia. 

2 • Zhang et al. 

is a Joint Action-State-Text Diffusion Transformer (JAST-DiT), which represents actions, physical states, and text as dedicated token streams and couples them through joint attention, enabling direct interaction between language semantics and control dynamics. To stabilize autoregressive control, we introduce a nonlinear history conditioning mechanism, which preserves the dense recent context and samples increasingly sparse cues from long-term history. Beyond supervised imitation pre-training, we propose a post-training stage, further improving the performance using Reinforcement Learning with Hybrid Rewards (RLHR). By injecting learnable noise into the flow-sampling process, RLHR effectively improves motion quality and instruction following within closed-loop simulations using hybrid physical feedback and text rewards. Quantitative evaluations demonstrate that SCRIPT outperforms prior state-of-the-art methods, with gains across text alignment, motion quality, and physical realism metrics. Furthermore, scaling studies on the 1200-hour MotionMillion dataset demonstrate consistent performance gains with model scaling, highlighting SCRIPT’s robust scalability for large-scale pre-training. Code and data for this paper are available at https://zhanglele12138.github.io/SCRIPT/. 

CCS Concepts: • **Computing methodologies** → **Physical simulation** . 

Additional Key Words and Phrases: Physics-based humanoid control, diffusion models, reinforcement learning 

### **ACM Reference Format:** 

Jingyan Zhang, Han Liang, Ruichi Zhang, Bin Li, Juze Zhang, Xin Chen, Jingya Wang, Lan Xu, and Jingyi Yu. 2026. SCRIPT: Scalable Diffusion Policy with Multi-stage Training for Language-driven Physics-Based Humanoid Control. In _SIGGRAPH Asia 2026 Conference Papers (SA Conference Papers ’26), December 01–04, 2026, Kuala Lumpur, Malaysia._ ACM, New York, NY, USA, 18 pages. https://doi.org/10.1145/3829340.3842344 

## 1 Introduction 

Endowing humanoid agents with the ability to comprehend human intent and interact naturally with their environments is pivotal to bridging the digital and physical worlds. Toward this vision, enabling physics-based humanoids to synthesize expressive and physically plausible motions from language instructions has emerged as a key frontier in computer graphics and embodied artificial intelligence [Fung et al. 2025]. Achieving such capability at scale fundamentally hinges on massive paired text-motion data [Guo et al. 2022; Mahmood et al. 2019; Plappert et al. 2016]. Recent advances in large language models (LLMs) [Brown et al. 2020; Guo et al. 2025; Touvron et al. 2023] and vision-language models (VLMs) [Bai et al. 2025; Liu et al. 2023; Radford et al. 2021] have made it feasible to construct richly annotated, large-scale motion datasets from diverse web sources [Fan et al. 2025; Lin et al. 2023; McLean et al. 2025; Zhang et al. 2025b]. The expansion of data scale and semantic coverage has fueled rapid progress in text-conditioned kinematic motion generation, enabling models to synthesize diverse human motion sequences from open-vocabulary instructions [Fan et al. 2025; Jiang et al. 2023; Liang et al. 2024; Lu et al. 2025; Tevet et al. 2022; Wen et al. 2025]. In parallel, deep reinforcement learning (RL) has become a powerful paradigm for physics-based character control, where policies are optimized through interaction with simulated environments. By training policies directly under rigid-body dynamics in contact-rich simulations, these methods can produce controllers for highly dynamic skills such as running, agile traversal, and acrobatic maneuvers [Peng et al. 2022, 2021; Rempe et al. 2023; Xu et al. 2025; 

Zhang et al. 2025a]. Despite these advances, combining the scalability of data-driven kinematic motion generation with the physical feasibility and closed-loop robustness of humanoid control remains challenging. 

Recent studies [Ren et al. 2023; Serifi et al. 2024; Tevet et al. 2024; Wu et al. 2025b] adopt a hierarchical framework, where diffusionbased planners generate kinematic references and a tracking policy executes them under physical constraints. However, since the references are not guaranteed to be dynamically feasible, the tracker must trade off reference fidelity against actuation limits, and subtle reference artifacts can be amplified into visible failures during closed-loop execution. Other approaches build unified controllers by distilling specialized expert policies [Juravsky et al. 2024] or leveraging pretrained motion priors [Mu et al. 2025]. Despite advancing policy coverage and instruction following, compressing diverse motions into a single policy incurs information loss and mode averaging, compromising stylistic diversity [Peng et al. 2022; Zhu et al. 2023]. Recent large-scale tracking policies show that RL-based humanoid control can benefit from scaling, but they remain focused on reference-motion tracking rather than language-conditioned control [Luo et al. 2025]. Diffusion policies have also been explored for physics-based humanoid control, offering expressive action distributions for closed-loop execution [Huang et al. 2025; Ren et al. 2024; Truong et al. 2024; Wu et al. 2025a]. However, by treating text merely as a coarse condition, these methods weakly couple language with states and actions, limiting joint improvements in text-motion alignment and physical plausibility. 

Building on these insights, we propose SCRIPT, a scalable endto-end diffusion policy with a multi-stage training paradigm for language-driven physics-based humanoid control. Conditioned on language instructions and state histories, SCRIPT generates executable actions to drive humanoid motion within a physics simulator. SCRIPT is built upon the Joint Action-State-Text Diffusion Transformer (JAST-DiT), which maintains separate token streams for actions, physical states, and text while enabling dense cross-modal interaction through joint attention. To support stable autoregressive execution, we further introduce a nonlinear long-term history conditioning mechanism that preserves recent control dynamics and sparsely samples distant context during rollouts. Beyond imitation pre-training with supervised flow matching loss, SCRIPT incorporates an RL post-training stage that directly optimizes tasklevel rewards to further improve semantic alignment and physical stability. Experiments show that SCRIPT achieves state-of-the-art performance on HumanML3D and exhibits consistent scaling gains on MotionMillion as the model size increases from 0.2B to 1.2B parameters. Our contributions are summarized as follows: 

- We introduce SCRIPT, a scalable diffusion policy framework for language-driven physics-based humanoid control, achieving state-of-the-art performance. 

- We propose JAST-DiT and a tailored nonlinear long-term history conditioning mechanism for stable autoregressive modeling, demonstrating favorable scaling performance on the large-scale 1200-hour MotionMillion dataset. 

SA Conference Papers ’26, December 01–04, 2026, Kuala Lumpur, Malaysia. 

SCRIPT: Scalable Diffusion Policy with Multi-stage Training for Language-driven Physics-Based Humanoid Control • 3 

- We propose a hybrid-reward RL post-training stage that optimizes physics-based and text-alignment rewards, further improving physical stability and instruction following. 

## 2 Related Work 

_Large-Scale Kinematic Motion Generation._ Human motion datasets have rapidly expanded in both scale and modality coverage, spanning text [Fan et al. 2025; Guo et al. 2022; Zhang et al. 2025b], audio [Li et al. 2021; Liu et al. 2024b, 2022b], inertial signals [Huang et al. 2018; Trumble et al. 2017], and objects [Bhatnagar et al. 2022; Li et al. 2023; Zhang et al. 2024]. Advances in LLM- and VLM-assisted annotation have made it increasingly feasible to construct largescale paired text-motion datasets. Driven by the steady growth of text-motion data, recent models have increasingly adopted scalable generative architectures [He et al. 2025a; Jiang et al. 2023; Peebles and Xie 2023; Wang et al. 2024a; Zhu et al. 2025]. By scaling up model capacity, recent works have advanced motion generation from closed-set to open-vocabulary generation, achieving substantially improved text-motion alignment for complex textual prompts [Fan et al. 2025; Li et al. 2026; Liang et al. 2024; Lu et al. 2025; Rempe et al. 2026; Wen et al. 2025]. However, these methods generate offline kinematic trajectories rather than closed-loop control policies executable in physics simulation. Without modeling of contact dynamics, balance control, actuation limits, and environmental feedback, the resulting motions often exhibit physical artifacts such as foot skating, floating, and ground penetration, limiting their direct applicability to physics-based control. 

_Physics-Based Humanoid Control._ Early methods in physics-based humanoid control largely followed a tracking paradigm [Peng et al. 2018]. Subsequent work introduced motion priors [Luo et al. 2024b; Peng et al. 2021] and latent skill spaces [Peng et al. 2022; Tessler et al. 2023; Yao et al. 2022, 2024] to support reusable motor skills, while more recent language-conditioned controllers [Juravsky et al. 2022, 2024; Mu et al. 2025; Tessler et al. 2024] further enable text-driven control. Although effective in scaling, distilling diverse motions into compact policies or latent skill spaces often introduces mode averaging. Another line of work follows a cascaded planner-tracker paradigm, where kinematic references are tracked by a physicsbased controller [Lim et al. 2026; Ren et al. 2023; Tevet et al. 2024]. However, artifacts and infeasible contacts in the generated kinematic references can be amplified during tracking, degrading the physical stability and instruction fidelity. Recent works apply diffusion policies to humanoid control [Huang et al. 2025; Truong et al. 2024; Wu et al. 2025a], locomotion for real robots [Huang et al. 2024], and motion tracking [Liao et al. 2025], training end-to-end controllers via behavior cloning on expert demonstrations. These methods typically rely on basic commands or reference trajectories, and even approaches incorporating language suffer from limited data scale and coarse conditioning that hinder precise alignment with physical control. Building scalable language-driven diffusion policies from large-scale motion data while preserving physical plausibility and instruction fidelity remains an open challenge. 

_Reinforcement Learning for Diffusion Policies._ Supervised diffusion training learns policies through denoising or flow matching 

regression, whereas RL fine-tunes policies through reward-driven environmental interaction. To bridge this gap, recent methods formulate the denoising process as a Markov decision process (MDP) to optimize specific rewards [Black et al. 2023; Fan et al. 2023; Hiranaka et al. 2024; Hu et al. 2025; Xue et al. 2025; Yang et al. 2024]. This paradigm naturally extends to continuous control, where online RL is used to improve diffusion models initialized through behavioral cloning [Ren et al. 2024; Zhang et al. 2025c]. Policy gradients tailored to flow-based policies have also been applied to robot control [Yi et al. 2026]. Parallel efforts in human motion generation apply RL or preference optimization to align diffusion models with physical constraints, text prompts, and human aesthetics [Girolamo et al. 2026; Han et al. 2024; Liu et al. 2024a; Pappa et al. 2024]. However, these methods primarily focus on offline kinematic generation, where rewards are evaluated on completed trajectories rather than through closed-loop physical interaction. By contrast, physical humanoid control requires continuous execution, where each action shapes future states, causing minor deviations to compound into physical instability. Therefore, RL post-training of diffusion-based policies that achieves both high-level text-motion alignment and stable closedloop physical execution remains largely underexplored. Our RLHR complements these efforts by coupling a hybrid semantic-physical reward with closed-loop humanoid control. 

## 3 Preliminaries 

## 3.1 Problem Formulation 

Given a text instruction _𝑐_ , we train a language-driven diffusion policy _𝜋𝜃_ to control a physics-based humanoid in a simulated environment. Let s _𝑡_ ∈ R<sup>_𝑑𝑠_</sup> and a _𝑡_ ∈ R<sup>_𝑑𝑎_</sup> denote the proprioceptive state and the control action at time step _𝑡_ . Let _𝐿_ and _𝐻_ denote the sampled state history length and the prediction horizon, respectively. We define the sampled state history at time _𝑡_ as H _𝑡_ = {s _𝑡_ − _ℓ𝑖_ } _𝑖_<sup>_𝐿_</sup> =1<sup>, where</sup> _ℓ𝑖_ is the temporal offset selected from a raw history window by our history sampler. The state s _𝑡_ includes the root height, along with the local position, 6D rotation [Zhou et al. 2019], linear velocity, and angular velocity of each joint. The action a _𝑡_ specifies target joint angles for a proportional-derivative (PD) controller. We encode the text instruction _𝑐_ using the CLIP [Radford et al. 2021] text encoder, yielding a pooled embedding cpool and penultimate-layer token features ctxt. Inspired by [Esser et al. 2024], we utilize penultimate-layer features to prevent the loss of token-level semantics caused by final projections. At each rollout step, _𝜋𝜃_ jointly generates the next _𝐻_ state-action pairs conditioned on the sampled state history H _𝑡_ and the text embeddings: 


During inference, the policy operates in a receding-horizon manner, predicting an _𝐻_ -step trajectory, executing only the first action, and updating the history for the next prediction. 

## 3.2 Flow Matching 

Flow Matching (FM) is a generalized formulation of diffusion models that replaces complex stochastic differential equations with simpler, deterministic probability paths. Accordingly, we formulate _𝜋𝜃_ as a 

SA Conference Papers ’26, December 01–04, 2026, Kuala Lumpur, Malaysia. 

4 • Zhang et al. 


Fig. 2. Overview of the SCRIPT framework. Left: Stage I pre-trains a flow matching diffusion policy via behavior cloning, and Stage II applies RL post-training via PPO with hybrid rewards. JAST-DiT jointly models action, state, and text tokens through separate streams with joint attention. 

conditional generative policy based on FM [Albergo and VandenEijnden 2022; Lipman et al. 2022; Liu et al. 2022a]. Let x0 ∼N (0 _,_ I) denote a Gaussian noise sample and x1 ∼ _𝑝_ data denote a clean data sample. FM defines a linear probability path 


where _𝜏_ is the flow time. The target velocity along this path is obtained by differentiating x _𝜏_ with respect to _𝜏_ : 


FM trains a vector field _𝑣𝜃_ (x _𝜏,𝜏,_ y) to match this target velocity, where y = {H _𝑡,_ ctxt _,_ cpool} denotes the conditioning information. The training objective is to minimize the mean squared error between the predicted and target velocities: 


In our setting, the clean data sample x1 corresponds to the future state-action trajectory chunk [a _𝑡_ +1: _𝑡_ + _𝐻_ ; s _𝑡_ +1: _𝑡_ + _𝐻_ ]. 

## 4.1 Large-Scale Data Curation 

Large-scale physically executable data are essential for languagedriven humanoid control. Existing text-motion datasets, such as HumanML3D [Guo et al. 2022] and MotionMillion [Fan et al. 2025], provide rich semantic coverage but consist of kinematic SMPL trajectories that often contain artifacts such as ground penetration and floating. Directly tracking these unconstrained motions in simulation can conflict with rigid-body dynamics, resulting in invalid stateaction demonstrations. To mitigate this issue, we curate the raw motions through pre-tracking artifact filtering and post-tracking rollout filtering with PHC [Luo et al. 2023]. We filter out motion clips with severe artifacts, such as ground penetration or body floating. Subsequently, we train multiple expert policies to track the remaining motions in parallel, collecting per-frame proprioceptive state s _𝑡_ ∈ R<sup>358</sup> and target PD control action a _𝑡_ ∈ R<sup>69</sup> . Sequences with excessive tracking error or humanoid falls are discarded to avoid physically invalid demonstrations. After curation, we retain 550K physical trajectories covering nearly 1200 hours of motion data, which are partitioned into training, validation, and test sets without motion overlap. We use sliding windows to extract fixed-length segments from variable-length trajectories, with details provided in Sec. A of the supplementary material. 

## 4 Methodology 

Fig. 2 illustrates SCRIPT, our multi-stage framework for languagedriven physics-based humanoid control. SCRIPT consists of three key components: (1) processing large-scale text-motion datasets to construct state-action demonstrations (Sec. 4.1); (2) JAST-DiT, a diffusion transformer that jointly models actions, states, and text to predict future chunks, with nonlinear history-conditioned crossattention (Sec. 4.2); and (3) an RLHR post-training stage that optimizes semantic alignment and physical stability via PPO [Schulman et al. 2017] on stochastic flow-sampling trajectories (Sec. 4.3). 

## 4.2 JAST-DiT Architecture 

_Joint Action-State-Text Self-Attention._ To model the coupled dependencies among low-level actions, physical states, and language semantics, we introduce JAST-DiT, a Joint Action-State-Text Diffusion Transformer. Rather than using text solely as a global condition, our architecture maintains independent token streams for each modality, enabling modality-specific representation and tokenlevel cross-modal interaction within each Transformer block. As 

SA Conference Papers ’26, December 01–04, 2026, Kuala Lumpur, Malaysia. 

SCRIPT: Scalable Diffusion Policy with Multi-stage Training for Language-driven Physics-Based Humanoid Control • 5 


Fig. 3. Nonlinear history sampling. Our strategy keeps recent states densely sampled and distant states sparsely sampled, balancing short-term control dynamics with long-range temporal context. 

illustrated in the right panel of Fig. 2, the inputs to JAST-DiT consist of the action and state tokens from the noisy trajectory chunk, alongside the penultimate-layer CLIP text tokens ctxt. These tokens are mapped to a shared hidden dimension via stream-specific projections and subsequently augmented with positional embeddings. We denote the resulting streams at the _ℓ_ -th Transformer block as A<sup>(</sup><sup>_ℓ_)</sup> , S<sup>(</sup><sup>_ℓ_)</sup> , and C<sup>(</sup><sup>_ℓ_)</sup> . In parallel, the flow time _𝜏_ and the pooled text embedding cpool are encoded into a global condition vector e = Cond( _𝜏,_ cpool). Within each block, this vector is injected via AdaLN-Zero modulation [Peebles and Xie 2023] to independently modulate each stream before projecting them into stream-specific queries, keys, and values (e.g., Q _𝑎,_ K _𝑎,_ V _𝑎_ for the action stream). To enhance numerical stability, we apply QK-Norm [Dehghani et al. 2023; Henry et al. 2020] to the query and key features. These streamspecific projections are subsequently concatenated along the token dimension to form Q = [Q _𝑎_ ; Q _𝑠_ ; Q _𝑐_ ], with K and V constructed analogously. Since the diffusion policy denoises the entire trajectory chunk jointly, the action and state tokens attend bidirectionally without causal masking, while the text padding mask is retained. Finally, we compute joint attention over the concatenated sequence and partition the output back into the three distinct feature streams: 


_Nonlinear History-Conditioned Cross-Attention._ In the physical control of embodied agents, explicit memory mechanisms are crucial for maintaining long-term action coherence [Fung et al. 2025; Guhur et al. 2023; Radosavovic et al. 2024]. Conditioning solely on the current state provides limited temporal context, making it difficult to infer evolving dynamics such as momentum trends and contact transitions, which may lead to action drift or physical instability during long-horizon autoregressive rollouts. Inspired by working memory [Baddeley 2020] and forgetting curves [Murre and Dros 2015] in cognitive science, we incorporate short- and long-term state history into the action and state streams through cross-attention. During rollouts, we maintain a dense history buffer B _𝑡_ = {(s _𝑡_ − _𝑖_ )} _𝑖_<sup>_𝐿_</sup> =<sup>max</sup> 1<sup>. While the updated action and state streams from</sup> 

Table 1. SCRIPT model variants. 

|Model|_𝑛_layers|_𝑑_model|_𝑛_heads|_𝑑_head|Params|
|---|---|---|---|---|---|
|SCRIPT-Base|8|512|4|128|206_._31M|
|SCRIPT-Large|10|768|6|128|577_._97M|
|SCRIPT-Huge|12|1024|8|128|1231_._39M|


the joint attention layer could intuitively query this entire buffer, attending to all _𝐿_ max historical states is computationally prohibitive and introduces redundant information. To address this, we construct the sampled state history H _𝑡_ using a nonlinear downsampling strategy, as illustrated in Fig. 3. Specifically, we keep the latest _𝑁𝑠_ states as dense recent history and sparsely sample _𝑁𝑙_ frames from the remaining distant history of length _𝐿_ distant = _𝐿_ max − _𝑁𝑠_ . To sample the distant history, we draw uniformly distributed variables _𝑢𝑖_ ∈[0 _,_ 1] for _𝑖_ = 1 _, . . . , 𝑁𝑙_ and compute the frame indices as: 


Here, _𝛼_ controls the decay rate, with larger values biasing the sampling probability toward more recent frames. Rather than concatenating the distant and recent frames into a single sequence, we inject them hierarchically via sequential cross-attention. The action and state streams attend to the sparse distant history Hdist<sup>(</sup><sup>_ℓ_)to retrieve</sup> long-range context, before attending to the dense recent history Hrec<sup>(</sup><sup>_ℓ_)to capture fine-grained local dynamics:</sup> 


After all JAST-DiT blocks, the refined token streams are projected to predict the flow velocity field _𝑣𝜃_ for the future state-action trajectory chunk. The entire model is trained with the conditional FM objective in Eq. 4, where the clean sample corresponds to the future stateaction chunk [a _𝑡_ +1: _𝑡_ + _𝐻_ ; s _𝑡_ +1: _𝑡_ + _𝐻_ ]. 

_Scalable Model Variants._ To study the impact of model scaling on policy performance in physics-based humanoid control, we follow the scaling principles of Diffusion Transformers (DiT) [Peebles and Xie 2023] and instantiate the SCRIPT model across three distinct capacities: Base, Large, and Huge. As summarized in Table 1, we systematically scale the number of network layers _𝑛_ layers, the hidden dimension _𝑑_ model, and the number of attention heads _𝑛_ heads, while keeping the per-head dimension _𝑑_ head fixed at 128. Consequently, the total parameter count ranges from 206.31M to 1231.39M. By instantiating these variants, we provide an empirical exploration of scaling behaviors for physics-based humanoid control. 

## 4.3 Online Reinforcement Learning Post-Training 

_Stochastic Exploration via Noise Injection._ Although the pretrained diffusion policy can successfully follow language instructions, supervised flow matching primarily fits the training distribution rather than directly optimizing task rewards under closed-loop physics simulation. This limitation motivates RLHR, our online reinforcement learning post-training stage, which directly optimizes task 

SA Conference Papers ’26, December 01–04, 2026, Kuala Lumpur, Malaysia. 

6 • Zhang et al. 

Table 2. Comparison with physics-based humanoid control baselines on HumanML3D. We comprehensively evaluate the methods across text-motion alignment, motion quality, and physical stability. The best results are in **bold** . 

|Method||R-precision|||Motion Qual|ity|Ph|ysics-bas|ed Metrics|
|---|---|---|---|---|---|---|---|---|---|
||Top-1↑|Top-2↑|Top-3↑|FID↓|MM Dist.↓|Diversity→|Floating↓|Jerk↓|Duration time↑|
|Phys-GT|0_._651±_._002|0_._815±_._001|0_._882±_._001|0_._000±_._000|1_._700±_._001|1_._494±_._008|17_._49|2_._941|100_._00%|
|PDP [Truong et al. 2024]|0_._206±_._002|0_._324±_._001|0_._416±_._002|1_._536±_._004|2_._666±_._003|1_._335±_._011|27_._19|3_._047|89_._54%|
|UniPhys [Wu et al. 2025a]|0_._143±_._004|0_._242±_._003|0_._326±_._003|0_._487±_._001|2_._750±_._001|1_._447±_._008|19_._67|2_._036|92_._55%|
|CLoSD [Tevet et al. 2024]|0_._370±_._002|0_._537±_._002|0_._641±_._001|0_._728±_._002|2_._291±_._001|1_._444±_._008|20_._71|2_._767|94_._81%|
|SCRIPT Stage I|0_._429±_._003|0_._595±_._003|0_._689±_._001|0_._203±_._001|2_._112±_._001|1_._462±_._007|17_._85|1_._723|97_._67%|
|SCRIPT Stage II|0_._435±_._002|0_._599±_._002|0_._693±_._001|0_._164±_._001|2_._123±_._001|1_._486±_._009|17_._61|1_._706|98_._08%|


rewards in physics simulation to improve semantic alignment and physical stability. Following ReinFlow [Zhang et al. 2025c], we transform the deterministic flow sampling process into a stochastic one by injecting Gaussian noise exclusively into the action subspace at each Euler integration step: 


where x _𝑘_ denotes the intermediate noisy state-action trajectory chunk at the _𝑘_ -th Euler step. Here, _𝝐𝑘_ ∼N (0 _,_ I) represents the injected noise, _𝜎𝜙_ ( _𝜏𝑘,_ H _𝑡_ ) denotes a dynamic exploration scale predicted by a lightweight network conditioned on the flow time and state history, and M _𝑎_ is a binary mask that restricts the perturbation to the action dimensions. This stochastic update turns the deterministic flow sampler into a Markov chain over Euler steps, thereby enabling tractable action-space transition likelihoods for policy-gradient optimization. 

_Reward Design._ Our reward design combines dense physical regularization with trajectory-level semantic alignment. The physical term is a positive tracking bonus that stabilizes closed-loop execution by rewarding agreement with the reference motion distribution, while the semantic term encourages consistency with the language instruction. We optimize the composite reward _𝑟𝑡_ = _𝑤_ phys _𝑟_ phys ( _𝑡_ ) + _𝑤_ text _𝑟_ text ( _𝑡_ ), where _𝑤_ phys and _𝑤_ text are weighting coefficients for the physical and semantic components, respectively. The physical reward _𝑟_ phys ( _𝑡_ ) rewards agreement between the simulated humanoid state and the reference motion: 


where _𝑑𝑚_ ( _𝑡_ ) denotes the discrepancy between the simulated rollout and the reference kinematic data in terms of keypoint positions _𝑝_ , orientations _𝑞_ , linear velocities _𝑣_ , and angular velocities _𝜔_ . To encourage semantic alignment, we introduce a sparse trajectorylevel state-text contrastive reward _𝑟_ text, which is evaluated exclusively at episode termination. To achieve this, we leverage a frozen state-text contrastive model consisting of a state trajectory encoder _𝑓𝑚_ and a text encoder _𝑓𝑡_ , which was pre-trained to align physical state sequences with language descriptions. For each environment _𝑖_ within a training batch B, we encode its full episodic state sequence S _𝑖_<sup>full</sup> and compute the cosine similarity to the text prompt _𝑐 𝑗_ as _𝑆𝑖𝑗_ = ⟨ _𝑓𝑚_ (S _𝑖_<sup>full</sup> ) _, 𝑓𝑡_ ( _𝑐 𝑗_ )⟩. The semantic reward is then defined as 

the log-normalized probability of the corresponding text prompt: 


_Optimization Objective._ We optimize the stochastic flow sampler with PPO using the rewards defined above from physics rollouts. To mitigate catastrophic forgetting and prevent excessive deviation from the pretrained flow matching policy, we augment the standard RL objective with a behavior cloning anchor loss: 


where Lvalue represents the MSE between the critic predictions and the estimated returns, Hentropy is the analytical action noise entropy. To remain consistent with the first-stage flow matching objective, the BC anchor is evaluated on resampled flow matching pairs: 


where _𝜃_ 0 denotes the frozen pretrained policy, and x is a clean stateaction trajectory chunk sampled from the rollout buffer. This term anchors the fine-tuned velocity field to the pretrained one while allowing PPO to improve task rewards in simulation. Further details are provided in Sec. B of the supplementary material. 

## 5 Experiments 

## 5.1 Experiment Setup 

_Physics simulation setup._ Following [Luo et al. 2023], we control a SMPL-like [Loper et al. 2023] physics humanoid in Isaac Gym simulator [Makoviychuk et al. 2021]. The humanoid consists of 24 body parts, with 23 actuated rotational joints and an unactuated pelvis. Given the current state s _𝑡_ and action a _𝑡_ , the simulator advances the system as s _𝑡_ +1 = SIM(s _𝑡 ,_ a _𝑡_ ). 

_Evaluation Metrics and Training Details._ We evaluate SCRIPT along two axes: text-motion alignment and physical plausibility. Following the text-to-motion evaluation protocol [Guo et al. 2022; Liang et al. 2024], we report R-Precision (Top-1/2/3), FID, and MM-Dist using the text-motion evaluator. For physical plausibility, following physics-based motion benchmarks [Yuan et al. 2023], we report Floating, Jerk, and Duration time, where Floating and Jerk are computed from global joint positions. SCRIPT is trained in two stages. In Stage I, we train SCRIPT-Large on HumanML3D for benchmark 

SA Conference Papers ’26, December 01–04, 2026, Kuala Lumpur, Malaysia. 

SCRIPT: Scalable Diffusion Policy with Multi-stage Training for Language-driven Physics-Based Humanoid Control • 7 


Fig. 4. Qualitative comparison on HumanML3D. We compare SCRIPT against PDP [Truong et al. 2024], UniPhys [Wu et al. 2025a], and CLoSD [Tevet et al. 2024]. Each row shows a generated motion as a temporally stacked pose sequence, with the key prompt phrase highlighted. SCRIPT follows the prompt more faithfully while maintaining physical plausibility. 

SA Conference Papers ’26, December 01–04, 2026, Kuala Lumpur, Malaysia. 

8 • Zhang et al. 


Fig. 5. Qualitative results of SCRIPT-Huge trained on MotionMillion. Large-scale training enables diverse language-conditioned humanoid motions in physics simulation, covering locomotion, sports, dance, and daily actions. 

Table 3. Model scaling on MotionMillion. 

Table 4. Ablation studies on the HumanML3D test set. 

|Method||R-precision|||Motion Quali|ty|
|---|---|---|---|---|---|---|
||Top-1↑|Top-2↑|Top-3↑|FID↓|MM Dist.↓|Diversity→|
|GT|0_._707±_._001|0_._834±_._001|0_._886±_._001|0_._000±_._000|2_._864±_._000|2_._335±_._018|
|Base|0_._396±_._001|0_._544±_._001|0_._633±_._001|1_._057±_._000|3_._738±_._000|2_._251±_._016|
|Large|0_._437±_._001|0_._591±_._001|0_._680±_._001|0_._776±_._000|3_._625±_._000|2_._262±_._012|
|Huge|0_._464±_._001|0_._616±_._001|0_._701±_._001|0_._645±_._000|3_._554±_._000|2_._287±_._020|


comparisons and scaled model variants on MotionMillion for scaling studies. The HumanML3D model uses _𝐻_ = 4 and _𝐿_ max = 154, while the MotionMillion scaling models use a longer history of _𝐿_ max = 604. All models use 10% text-condition dropout for classifier-free guidance [Ho and Salimans 2022]. In Stage II, we initialize the actor from the pretrained model and perform RL post-training in 128 parallel Isaac Gym environments. We use a BC anchor weight of 1.0 and constrain the learnable exploration noise to _𝜎_ ∈[0 _._ 03 _,_ 0 _._ 08]. Additional details are provided in the supplemental material. 

## 5.2 Benchmark Evaluation on HumanML3D 

We compare SCRIPT against three representative baselines for physicsbased humanoid control. Table 2 reports the quantitative results. SCRIPT outperforms all baselines in semantic alignment and overall motion quality, while also achieving stronger physical plausibility. PDP and UniPhys condition their policies on a single CLIP pooled embedding, which compresses sentence-level semantics into one global vector. This design can obscure token-level cues such as 

|Method||R-precision|||Motion Qualit|y|Duration|
|---|---|---|---|---|---|---|---|
||Top-1↑|Top-2↑|Top-3↑|FID↓|MM Dist.↓|Div.→|Time↑|
|Phys-GT|0_._651±_._002|0_._815±_._001|0_._882±_._001|0_._000±_._000|1_._700±_._001|1_._494±_._008|100_._00%|
|Ours-Stage I|0_._429±_._003|0_._595±_._003|0_._689±_._001|0_._203±_._001|2_._112±_._001|1_._462±_._007|97_._67%|
|_Stream Ablation_||||||||
|Action stream only|0_._357±_._002|0_._524±_._002|0_._630±_._002|0_._485±_._000|2_._268±_._000|1_._433±_._009|97_._52%|
|w/o Text stream|0_._307±_._001|0_._461±_._001|0_._563±_._002|0_._967±_._000|2_._390±_._000|1_._357±_._009|98_._47%|
|w/o State stream|0_._384±_._002|0_._540±_._002|0_._633±_._001|0_._307±_._000|2_._243±_._000|1_._461±_._006|94_._57%|
|_History Ablation_||||||||
|w/ Uniform sampling|0_._419±_._002|0_._583±_._001|0_._679±_._002|0_._302±_._000|2_._169±_._000|1_._446±_._007|96_._29%|
|w/ Longer history|0_._395±_._002|0_._556±_._002|0_._654±_._001|0_._166±_._000|2_._192±_._000|1_._468±_._010|98_._14%|
|w/o History|0_._117±_._001|0_._203±_._001|0_._278±_._001|4_._063±_._001|2_._910±_._000|0_._946±_._009|76_._68%|


action verbs, body-part references, and modifiers, making it difficult for the policy to associate specific linguistic details with the corresponding control decisions. As shown in Fig. 4 E,G, the generated behaviors often collapse to generic motion patterns, capturing only the coarse action category while ignoring directional or manner-specific constraints, such as the specified clockwise walking direction. In contrast, SCRIPT augments the global CLIP text condition with token-level features from the penultimate layer of the CLIP text encoder, and introduces them as an explicit text stream in JAST-DiT. Through joint attention, these fine-grained text tokens interact directly with the action and state streams, allowing the policy to associate specific linguistic cues with the corresponding physical context. Although CLoSD improves text alignment over action-space baselines, its planner-tracker design remains vulnerable to tracking mismatch. When the generated reference motion exceeds the tracker’s capability, such as physically implausible or abrupt motions, accumulated tracking errors can lead to falls, as 

SA Conference Papers ’26, December 01–04, 2026, Kuala Lumpur, Malaysia. 

SCRIPT: Scalable Diffusion Policy with Multi-stage Training for Language-driven Physics-Based Humanoid Control • 9 


Fig. 6. Qualitative ablation results. The full model preserves stable and prompt-faithful motion, while ablated variants exhibit failures in stability, promptfollowing, or motion quality. 

Table 5. Reward ablation studies on the HumanML3D test set. 

|Method|R-prec.||Motion Qualit|y|Physi|cs-based|Metrics|
|---|---|---|---|---|---|---|---|
||Top-3↑|FID↓|MM Dist.↓|Div.→|Floating↓|Jerk↓|Duration↑|
|Phys-GT|0_._882±_._001|0_._000±_._000|1_._700±_._001|1_._494±_._008|17_._49|2_._941|100%|
|Ours-Stage II|0_._693±_._001|0_._164±_._001|2_._123±_._001|1_._486±_._009|17_._61|1_._706|98_._08%|
|_Hybrid Rewar_|_ds Ablation_|||||||
|w/o_𝑟_phys|0_._680±_._001|0_._220±_._001|2_._155±_._002|1_._471±_._008|20_._793|2_._254|93_._62%|
|w/o_𝑟_text|0_._649±_._003|0_._430±_._002|2_._219±_._003|1_._425±_._011|15_._399|1_._169|98_._74%|


shown in Fig. 4A,G. SCRIPT instead predicts actions directly in simulation, reducing the mismatch between high-level motion intent and physical execution. Stage I trains SCRIPT by imitating expert data, but closed-loop execution can still accumulate errors and shift the policy away from the expert distribution. Stage II mitigates this issue through on-policy rollouts in simulation, optimizing text-alignment and physical-plausibility rewards on the policy’s own trajectories. This explains the consistent gains in FID, Diversity, and physics metrics, while stable R-precision shows no semantic degradation. 

## 5.3 Scaling on MotionMillion 

To study how SCRIPT benefits from increased model capacity, we train three variants, ranging from 0.2B to 1.2B parameters, on the MotionMillion dataset. Table 3 reports the quantitative model-size scaling results. Within the evaluated range, all metrics improve consistently as model capacity increases, suggesting that SCRIPT can effectively exploit additional capacity when trained on large-scale text-motion data. Figure 5 further shows qualitative results from 

our Huge model trained on MotionMillion, illustrating the diverse and physically plausible motions enabled by large-scale training. With increased model capacity, SCRIPT learns a broader motion repertoire, covering a wide range of instructions while maintaining physically plausible control. 

## 5.4 Ablation Studies 

_Effect of JAST-DiT._ Table 4 reports the stream ablation results, validating the necessity of each modality in JAST-DiT. The Actiononly variant performs poorly across all metrics, indicating that a single stream cannot capture the coupled dependencies among control, physical state, and language. Removing the Text stream causes severe degradation in semantic alignment, as the policy loses token-level linguistic cues and tends to produce state-driven motions regardless of the prompt. Removing the State stream preserves semantic alignment relatively well but degrades motion quality and physical stability, confirming that explicit state tokens are essential for closed-loop control. As visualized in Figure 6A, these failures lead to either poor instruction following or unstable physical rollouts. The ablation results demonstrate that the three streams play complementary roles: text carries semantic intent, state anchors physical context, and action represents executable control, while joint attention enables JAST-DiT to align language with closed-loop control. 

_Effect of Nonlinear History Conditioning._ Table 4 reports the history ablation results, validating the role of temporal context and the design of our nonlinear sampler. Removing history entirely causes 

SA Conference Papers ’26, December 01–04, 2026, Kuala Lumpur, Malaysia. 

10 • Zhang et al. 

Table 6. Robustness under external pushes on HumanML3D. 

|Push|Fall@|2s (%)↓|Durati|on time↑|F|ID↓|To|p-1↑|
|---|---|---|---|---|---|---|---|---|
||Stage I|Stage II|Stage I|Stage II|Stage I|Stage II|Stage I|Stage II|
|0 N|1_._48|1_._38|97_._67%|98_._08%|0_._203|0_._164|0_._429|0_._435|
|400 N|4_._04|3_._40|96_._78%|97_._24%|0_._504|0_._420|0_._359|0_._366|
|600 N|10_._42|9_._48|93_._49%|94_._40%|0_._858|0_._727|0_._295|0_._305|
|800 N|27_._36|25_._15|84_._84%|86_._95%|1_._338|1_._206|0_._237|0_._244|


severe degradation, confirming that stable long-horizon closed-loop control requires sufficient temporal context. At the same window length, replacing nonlinear sampling with uniform sampling weakens both semantic alignment and motion quality, as uniform sampling under-represents recent dynamics that are critical for immediate control. Extending the history window further marginally improves motion quality but reduces semantic alignment, suggesting that excessive distant context can make the policy over-rely on past dynamics and respond less precisely to the input prompt. As shown in Fig. 6B, these trends appear as unstable motion or weaker instruction following. 

_Effect of Hybrid Reward._ Table 5 reports the reward ablation results, evaluating the contribution of each component in RLHR. Without the physical reward, the policy preserves semantic alignment but loses physical plausibility, producing text-relevant motions that suffer from drift, jerky movement, or early termination in simulation. Without the text reward, the policy improves physical metrics and may even outperform the full model on some stability-related measures, but semantic alignment and motion quality degrade. This apparent improvement reflects a survival bias where the policy favors conservative motions to avoid early termination and maximize _𝑟_ phys. The trajectory-level text reward mitigates this, preserving semantic alignment. As shown in Fig. 6C, these ablations produce complementary failure modes: unstable rollouts without the physical reward, and conservative motions with weak instruction following without the text reward. The full hybrid reward avoids both extremes, enabling motions that are both faithful to language and physically plausible. 

_Robustness under External Perturbations._ To quantify the robustness gains from the post-training stage, we evaluate the models under external perturbations on the HumanML3D test split. Specifically, during each rollout, a constant horizontal force pulse is applied to the pelvis of the humanoid for 0.2 s. The force magnitude ranges from zero for the unperturbed baseline up to 800 N. For a strict paired comparison, we evaluate Stage I and Stage II using identical randomly sampled perturbation directions and onset times across all test sequences and force levels. As shown in Table 6, the performance advantage of Stage II becomes more pronounced as the perturbation magnitude increases. Notably, at every nonzero force level, Stage II consistently achieves higher Duration time and a lower Fall@2s metric, which we define as the fall rate within 2 s after the push begins. Stage II also maintains better alignment with language instructions under external force. It consistently yields lower FID and higher R-precision under stronger impacts. These results demonstrate that the RL optimization stage does not merely 


Fig. 7. Qualitative comparison under an identical 600 N pelvis push. Stage I loses balance and falls, whereas Stage II absorbs the disturbance and resumes the instructed motion. 

induce conservative behavior. Rather, Stage II successfully improves physical robustness while preserving the intended motion semantics. Qualitative comparisons under identical pushes are shown in Fig. 7. 

## 6 Conclusion 

In this paper we present SCRIPT, a scalable diffusion policy framework for language-driven physics-based humanoid control. By jointly modeling actions, physical states, and language with JAST-DiT, and further incorporating history conditioning and reinforcement learning post-training, SCRIPT learns closed-loop control policies from large-scale physically executable trajectories. Experiments show that SCRIPT outperforms prior motion-generation and planner– tracker methods in instruction following, motion quality, and physical plausibility, while exhibiting consistent gains with data and model scaling. Future work will extend SCRIPT to more complex human-object interactions, multi-agent collaboration, and openenvironment tasks. We discuss limitations and failure modes in the supplementary material. 

## Acknowledgments 

This work was supported in part by the National Natural Science Foundation of China under Grant No. W2431046; the Central Guidance on Local Science and Technology Development Fund of China under Grant No. YDZX20253100001001; the Key Laboratory of Intelligent Perception and Human-Machine Collaboration (ShanghaiTech University), Ministry of Education; and the Shanghai Frontiers Science Center of Human-Centered Artificial Intelligence. Also supported by HPC Platform of ShanghaiTech University. 

SA Conference Papers ’26, December 01–04, 2026, Kuala Lumpur, Malaysia. 

SCRIPT: Scalable Diffusion Policy with Multi-stage Training for Language-driven Physics-Based Humanoid Control • 11 

## References 

- References Xiaoyu Huang, Yufeng Chi, Ruofeng Wang, Zhongyu Li, Xue Bin Peng, Sophia Shao, Michael S Albergo and Eric Vanden-Eijnden. 2022. Building normalizing flows with Borivoje Nikolic, and Koushil Sreenath. 2024. Diffuseloco: Real-time legged locostochastic interpolants. _arXiv preprint arXiv:2209.15571_ (2022). motion control with diffusion from offline datasets. _arXiv preprint arXiv:2404.19264_ 

- Alan Baddeley. 2020. Working memory. _Memory_ (2020), 71–111. (2024). Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui Chen, Zesen Cheng, LiangXiaoyu Huang, Takara Truong, Yunbo Zhang, Fangzhou Yu, Jean Pierre Sleiman, Jessica hao Deng, Wei Ding, Chang Gao, Chunjiang Ge, et al. 2025. Qwen3-vl technical Hodgins, Koushil Sreenath, and Farbod Farshidian. 2025. Diffuse-cloc: Guided report. _arXiv preprint arXiv:2511.21631_ (2025). diffusion for physics-based character look-ahead control. _ACM Transactions on_ 

- Bharat Lal Bhatnagar, Xianghui Xie, Ilya A Petrov, Cristian Sminchisescu, Christian _Graphics (TOG)_ 44, 4 (2025), 1–12. Theobalt, and Gerard Pons-Moll. 2022. Behave: Dataset and method for tracking Yinghao Huang, Manuel Kaufmann, Emre Aksan, Michael J. Black, Otmar Hilliges, and human object interactions. In _Proceedings of the IEEE/CVF conference on computer_ Gerard Pons-Moll. 2018. Deep Inertial Poser Learning to Reconstruct Human Pose _vision and pattern recognition_ . 15935–15946. from SparseInertial Measurements in Real Time. _ACM Transactions on Graphics,_ 

- Kevin Black, Michael Janner, Yilun Du, Ilya Kostrikov, and Sergey Levine. 2023. Training _(Proc. SIGGRAPH Asia)_ 37, 6 (Nov. 2018), 185:1–185:15. diffusion models with reinforcement learning. _arXiv preprint arXiv:2305.13301_ (2023). Biao Jiang, Xin Chen, Wen Liu, Jingyi Yu, Gang Yu, and Tao Chen. 2023. MotionGPT: 

- Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Human motion as a foreign language. _Advances in Neural Information Processing_ Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. _Systems_ 36 (2023), 20067–20079. 2020. Language models are few-shot learners. _Advances in neural information_ Jordan Juravsky, Yunrong Guo, Sanja Fidler, and Xue Bin Peng. 2022. PADL: Language- _processing systems_ 33 (2020), 1877–1901. directed physics-based character control. In _SIGGRAPH Asia 2022 Conference Papers_ . 

- Mostafa Dehghani, Josip Djolonga, Basil Mustafa, Piotr Padlewski, Jonathan Heek, 1–9. Justin Gilmer, Andreas Peter Steiner, Mathilde Caron, Robert Geirhos, Ibrahim Jordan Juravsky, Yunrong Guo, Sanja Fidler, and Xue Bin Peng. 2024. Superpadl: Scaling Alabdulmohsin, et al. 2023. Scaling vision transformers to 22 billion parameters. In language-directed physics-based control with progressive supervised distillation. In _International conference on machine learning_ . PMLR, 7480–7512. _ACM SIGGRAPH 2024 Conference Papers_ . 1–11. 

- Patrick Esser, Sumith Kulal, Andreas Blattmann, Rahim Entezari, Jonas Müller, Harry Jiaman Li, Jiajun Wu, and C Karen Liu. 2023. Object motion guided human motion Saini, Yam Levi, Dominik Lorenz, Axel Sauer, Frederic Boesel, et al. 2024. Scalsynthesis. _ACM Transactions on Graphics (TOG)_ 42, 6 (2023), 1–11. ing rectified flow transformers for high-resolution image synthesis. In _Forty-first_ Ruilong Li, Shan Yang, David A. Ross, and Angjoo Kanazawa. 2021. Learn to Dance _international conference on machine learning_ . with AIST++: Music Conditioned 3D Dance Generation. arXiv:2101.08779 [cs.CV] 

- Ke Fan, Shunlin Lu, Minyue Dai, Runyi Yu, Lixing Xiao, Zhiyang Dou, Junting Dong, Zekun Li, Sizhe An, Chengcheng Tang, Chuan Guo, Ivan Shugurov, Linguang Zhang, Lizhuang Ma, and Jingbo Wang. 2025. Go to zero: Towards zero-shot motion Amy Zhao, Srinath Sridhar, Lingling Tao, and Abhay Mittal. 2026. LLaMo: Scaling generation with million-scale data. In _Proceedings of the IEEE/CVF International_ Pretrained Language Models for Unified Motion Understanding and Generation _Conference on Computer Vision_ . 13336–13348. with Continuous Autoregressive Tokens. _arXiv preprint arXiv:2602.12370_ (2026). 

- Ying Fan, Olivia Watkins, Yuqing Du, Hao Liu, Moonkyung Ryu, Craig Boutilier, Pieter Han Liang, Jiacheng Bao, Ruichi Zhang, Sihan Ren, Yuecheng Xu, Sibei Yang, Xin Chen, Abbeel, Mohammad Ghavamzadeh, Kangwook Lee, and Kimin Lee. 2023. DPOK: Jingyi Yu, and Lan Xu. 2024. Omg: Towards open-vocabulary motion generation Reinforcement learning for fine-tuning text-to-image diffusion models. _Advances in_ via mixture of controllers. In _Proceedings of the IEEE/CVF Conference on Computer Neural Information Processing Systems_ 36 (2023), 79858–79885. _Vision and Pattern Recognition_ . 482–493. 

- Pascale Fung, Yoram Bachrach, Asli Celikyilmaz, Kamalika Chaudhuri, Delong Chen, Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Willy Chung, Emmanuel Dupoux, Hongyu Gong, Hervé Jégou, Alessandro Lazaric, Sreenath, and C Karen Liu. 2025. Beyondmimic: From motion tracking to versatile et al. 2025. Embodied ai agents: Modeling the world. _arXiv preprint arXiv:2506.22355_ humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ (2025). (2025). Dohun Lim, Minji Kim, Jaewoon Lim, and Sungchan Kim. 2026. BRIC: Bridging Kine- 

- Macaluso Girolamo, Mandelli Lorenzo, Mirko Bicchierai, Stefano Berretti, and Andrew D matic Plans and Physical Control at Test Time. In _Proceedings of the AAAI Conference_ Bagdanov. 2026. No MoCap Needed: Post-Training Motion Diffusion Models with _on Artificial Intelligence_ , Vol. 40. 23505–23513. Reinforcement Learning using Only Textual Prompts. In _Proceedings of the IEEE/CVF_ Jing Lin, Ailing Zeng, Shunlin Lu, Yuanhao Cai, Ruimao Zhang, Haoqian Wang, and _Winter Conference on Applications of Computer Vision_ . 967–976. Lei Zhang. 2023. Motion-x: A large-scale 3d expressive whole-body human motion 

- Pierre-Louis Guhur, Shizhe Chen, Ricardo Garcia Pinel, Makarand Tapaswi, Ivan Laptev, dataset. _Advances in Neural Information Processing Systems_ 36 (2023), 25268–25280. and Cordelia Schmid. 2023. Instruction-driven history-aware policies for robotic Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. 2022. manipulations. In _Conference on Robot Learning_ . PMLR, 175–187. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ (2022). 

- Chuan Guo, Shihao Zou, Xinxin Zuo, Sen Wang, Wei Ji, Xingyu Li, and Li Cheng. 2022. Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. 2023. Visual instruction Generating diverse and natural 3d human motions from text. In _2022 IEEE/CVF_ tuning. _Advances in neural information processing systems_ 36 (2023), 34892–34916. _Conference on Computer Vision and Pattern Recognition (CVPR)_ . IEEE, 5142–5151. Haiyang Liu, Zihao Zhu, Giorgio Becherini, Yichen Peng, Mingyang Su, You Zhou, 

- Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xuefei Zhe, Naoya Iwamoto, Bo Zheng, and Michael J Black. 2024b. Emage: Towards Xu, Ruoyu Zhang, Shirong Ma, Xiao Bi, et al. 2025. Deepseek-r1: Incentivizing reaunified holistic co-speech gesture generation via expressive masked audio gesture soning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_ modeling. In _Proceedings of the IEEE/CVF conference on computer vision and pattern_ (2025). _recognition_ . 1144–1154. 

- Gaoge Han, Mingjiang Liang, Jinglei Tang, Yongkang Cheng, Wei Liu, and Shaoli Huang. Haiyang Liu, Zihao Zhu, Naoya Iwamoto, Yichen Peng, Zhengqing Li, You Zhou, Elif 2024. Reindiffuse: Crafting physically plausible motions with reinforced diffusion Bozkurt, and Bo Zheng. 2022b. BEAT: A Large-Scale Semantic and Emotional model. _arXiv preprint arXiv:2410.07296_ (2024). Multi-Modal Dataset for Conversational Gestures Synthesis. _European Conference_ 

- Tairan He, Zi Wang, Haoru Xue, Qingwei Ben, Zhengyi Luo, Wenli Xiao, Ye Yuan, _on Computer Vision_ (2022). Xingye Da, Fernando Castañeda, Shankar Sastry, et al. 2025b. VIRAL: Visual SimXingchao Liu, Chengyue Gong, and Qiang Liu. 2022a. Flow straight and fast: Learning to-Real at Scale for Humanoid Loco-Manipulation. _arXiv preprint arXiv:2511.15200_ to generate and transfer data with rectified flow. _arXiv preprint arXiv:2209.03003_ (2025). (2022). 

- Yannan He, Garvita Tiwari, Xiaohan Zhang, Pankaj Bora, Tolga Birdal, Jan Eric Lenssen, Xiaoyang Liu, Yunyao Mao, Wengang Zhou, and Houqiang Li. 2024a. Motionrl: Align and Gerard Pons-Moll. 2025a. MoLingo: Motion-Language Alignment for Text-totext-to-motion generation to human preferences with multi-reward reinforcement Motion Generation. _arXiv preprint arXiv:2512.13840_ (2025). learning. _arXiv preprint arXiv:2410.06513_ (2024). 

- Alex Henry, Prudhvi Raj Dachapally, Shubham Shantaram Pawar, and Yuxuan Chen. Matthew Loper, Naureen Mahmood, Javier Romero, Gerard Pons-Moll, and Michael J 2020. Query-key normalization for transformers. In _Findings of the Association for_ Black. 2023. SMPL: A skinned multi-person linear model. In _Seminal Graphics Computational Linguistics: EMNLP 2020_ . 4246–4253. _Papers: Pushing the Boundaries, Volume 2_ . 851–866. 

- Ayano Hiranaka, Shang-Fu Chen, Chieh-Hsin Lai, Dongjun Kim, Naoki Murata, Takashi Shunlin Lu, Jingbo Wang, Zeyu Lu, Ling-Hao Chen, Wenxun Dai, Junting Dong, Zhiyang Shibuya, Wei-Hsiang Liao, Shao-Hua Sun, and Yuki Mitsufuji. 2024. Hero: HumanDou, Bo Dai, and Ruimao Zhang. 2025. Scamo: Exploring the scaling law in autorefeedback efficient reinforcement learning for online diffusion model finetuning. gressive motion generation model. In _Proceedings of the Computer Vision and Pattern arXiv preprint arXiv:2410.05116_ (2024). _Recognition Conference_ . 27872–27882. 

- Jonathan Ho and Tim Salimans. 2022. Classifier-free diffusion guidance. _arXiv preprint_ Zhengyi Luo, Jinkun Cao, Sammy Christen, Alexander Winkler, Kris Kitani, and _arXiv:2207.12598_ (2022). Weipeng Xu. 2024a. Omnigrasp: Grasping diverse objects with simulated humanoids. 

- Zijing Hu, Fengda Zhang, Long Chen, Kun Kuang, Jiahui Li, Kaifeng Gao, Jun Xiao, _Advances in Neural Information Processing Systems_ 37 (2024), 2161–2184. Xin Wang, and Wenwu Zhu. 2025. Towards better alignment: Training diffusion Zhengyi Luo, Jinkun Cao, Kris Kitani, Weipeng Xu, et al. 2023.. 2023. 2023. Perpetual humanoid models with reinforcement learning against sparse rewards. In _Proceedings of the_ control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Computer Vision and Pattern Recognition Conference_ . 23604–23614. _Conference on Computer Vision_ . 10895–10904. 

   - Xiaoyang Liu, Yunyao Mao, Wengang Zhou, and Houqiang Li. 2024a. Motionrl: Align text-to-motion generation to human preferences with multi-reward reinforcement learning. _arXiv preprint arXiv:2410.06513_ (2024). 

   - Matthew Loper, Naureen Mahmood, Javier Romero, Gerard Pons-Moll, and Michael J Black. 2023. SMPL: A skinned multi-person linear model. In _Seminal Graphics Papers: Pushing the Boundaries, Volume 2_ . 851–866. 

   - Shunlin Lu, Jingbo Wang, Zeyu Lu, Ling-Hao Chen, Wenxun Dai, Junting Dong, Zhiyang Dou, Bo Dai, and Ruimao Zhang. 2025. Scamo: Exploring the scaling law in autoregressive motion generation model. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ . 27872–27882. 

   - Zhengyi Luo, Jinkun Cao, Sammy Christen, Alexander Winkler, Kris Kitani, and Weipeng Xu. 2024a. Omnigrasp: Grasping diverse objects with simulated humanoids. _Advances in Neural Information Processing Systems_ 37 (2024), 2161–2184. 

   - Zhengyi Luo, Jinkun Cao, Kris Kitani, Weipeng Xu, et al. 2023.. 2023. 2023. Perpetual humanoid control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . 10895–10904. 

   - Zhengyi Luo, Jinkun Cao, Josh Merel, Alexander Winkler, Jing Huang, Kris Kitani, and Weipeng Xu. 2024b. Universal Humanoid Motion Representations for Physics-Based 

SA Conference Papers ’26, December 01–04, 2026, Kuala Lumpur, Malaysia. 

12 • Zhang et al. 

Control. In _International Conference on Learning Representations_ . 

- Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Castañeda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, Xingye Da, Runyu Ding, Cyrus Hogg, Lina Song, Edy Lim, Eugene Jeong, Tairan He, Haoru Xue, Wenli Xiao, Zi Wang, Simon Yuen, Jan Kautz, Yan Chang, Umar Iqbal, Linxi Fan, and Yuke Zhu. 2025. SONIC: Supersizing Motion Tracking for Natural Humanoid Whole-Body Control. _arXiv preprint arXiv:2511.07820_ (2025). 

- Naureen Mahmood, Nima Ghorbani, Nikolaus F Troje, Gerard Pons-Moll, and Michael J Black. 2019. AMASS: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ . 5442–5451. 

- Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, et al. 2021. Isaac Gym: High performance GPU-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ (2021). 

- Claire McLean, Makenzie Meendering, Tristan Swartz, Orri Gabbay, Alexandra Olsen, Rachel Jacobs, Nicholas Rosen, Philippe de Bree, Tony Garcia, Gadsden Merrill, et al. 2025. Embody 3d: A large-scale multimodal motion and behavior dataset. _arXiv preprint arXiv:2510.16258_ (2025). 

- Yuxuan Mu, Ziyu Zhang, Yi Shi, Minami Matsumoto, Kotaro Imamura, Guy Tevet, Chuan Guo, Michael Taylor, Chang Shu, Pengcheng Xi, et al. 2025. SMP: Reusable Score-Matching Motion Priors for Physics-Based Character Control. _arXiv preprint arXiv:2512.03028_ (2025). 

- Jaap MJ Murre and Joeri Dros. 2015. Replication and analysis of Ebbinghaus’ forgetting curve. _PloS one_ 10, 7 (2015), e0120644. 

- Aaron van den Oord, Yazhe Li, and Oriol Vinyals. 2018. Representation learning with contrastive predictive coding. _arXiv preprint arXiv:1807.03748_ (2018). 

- Liang Pan, Zeshi Yang, Zhiyang Dou, Wenjia Wang, Buzhen Huang, Bo Dai, Taku Komura, and Jingbo Wang. 2025. Tokenhsi: Unified synthesis of physical humanscene interactions through task tokenization. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ . 5379–5391. 

- Massimiliano Pappa, Luca Collorone, Giovanni Ficarra, Indro Spinelli, and Fabio Galasso. 2024. Modipo: text-to-motion alignment via ai-feedback-driven direct preference optimization. _arXiv preprint arXiv:2405.03803_ (2024). 

- William Peebles and Saining Xie. 2023. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ . 4195–4205. 

- Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. 2018. DeepMimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ 37, 4 (2018), 1–14. 

- Xue Bin Peng, Yunrong Guo, Lina Halper, Sergey Levine, and Sanja Fidler. 2022. ASE: Large-scale reusable adversarial skill embeddings for physically simulated characters. _ACM Transactions On Graphics (TOG)_ 41, 4 (2022), 1–17. 

- Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. 2021. AMP: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ 40, 4 (2021), 1–20. 

- Matthias Plappert, Christian Mandery, and Tamim Asfour. 2016. The KIT MotionLanguage Dataset. _Big Data_ 4, 4 (dec 2016), 236–252. doi:10.1089/big.2016.0028 

- Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. 2021. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ . PmLR, 8748–8763. 

- Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, and Koushil Sreenath. 2024. Real-world humanoid locomotion with reinforcement learning. _Science Robotics_ 9, 89 (2024), eadi9579. 

- Davis Rempe, Zhengyi Luo, Xue Bin Peng, Ye Yuan, Kris Kitani, Karsten Kreis, Sanja Fidler, and Or Litany. 2023. Trace and pace: Controllable pedestrian animation via guided trajectory diffusion. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . 13756–13766. 

- Davis Rempe, Mathis Petrovich, Ye Yuan, Haotian Zhang, Xue Bin Peng, Yifeng Jiang, Tingwu Wang, Umar Iqbal, David Minor, Michael de Ruyter, et al. 2026. Kimodo: Scaling Controllable Human Motion Generation. _arXiv preprint arXiv:2603.15546_ (2026). 

- Allen Z Ren, Justin Lidard, Lars L Ankile, Anthony Simeonov, Pulkit Agrawal, Anirudha Majumdar, Benjamin Burchfiel, Hongkai Dai, and Max Simchowitz. 2024. Diffusion policy policy optimization. _arXiv preprint arXiv:2409.00588_ (2024). 

- Jiawei Ren, Mingyuan Zhang, Cunjun Yu, Xiao Ma, Liang Pan, and Ziwei Liu. 2023. Insactor: Instruction-driven physics-based characters. _Advances in Neural Information Processing Systems_ 36 (2023), 59911–59923. 

- Tim Salimans and Jonathan Ho. 2022. Progressive distillation for fast sampling of diffusion models. _arXiv preprint arXiv:2202.00512_ (2022). 

- John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. 2017. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ (2017). 

- Agon Serifi, Ruben Grandia, Espen Knoop, Markus Gross, and Moritz Bächer. 2024. Robot motion diffusion model: Motion generation for robotic characters. In _SIGGRAPH asia 2024 conference papers_ . 1–9. 

- Yang Song, Prafulla Dhariwal, Mark Chen, and Ilya Sutskever. 2023. Consistency models. (2023). 

Chen Tessler, Yunrong Guo, Ofir Nabati, Gal Chechik, and Xue Bin Peng. 2024. Maskedmimic: Unified physics-based character control through masked motion inpainting. _ACM Transactions On Graphics (TOG)_ 43, 6 (2024), 1–21. 

- Chen Tessler, Yoni Kasten, Yunrong Guo, Shie Mannor, Gal Chechik, and Xue Bin Peng. 2023. Calm: Conditional adversarial latent models for directable virtual characters. In _ACM SIGGRAPH 2023 conference proceedings_ . 1–9. 

- Guy Tevet, Sigal Raab, Setareh Cohan, Daniele Reda, Zhengyi Luo, Xue Bin Peng, Amit H Bermano, and Michiel van de Panne. 2024. Closd: Closing the loop between simulation and diffusion for multi-task character control. _arXiv preprint arXiv:2410.03441_ (2024). 

- Guy Tevet, Sigal Raab, Brian Gordon, Yonatan Shafir, Daniel Cohen-Or, and Amit H Bermano. 2022. Human motion diffusion model. _arXiv preprint arXiv:2209.14916_ (2022). 

- Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. 2023. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ (2023). 

- Matt Trumble, Andrew Gilbert, Charles Malleson, Adrian Hilton, and John Collomosse. 2017. Total Capture: 3D Human Pose Estimation Fusing Video and Inertial Sensors. In _2017 British Machine Vision Conference (BMVC)_ . 

- Takara Everest Truong, Michael Piseno, Zhaoming Xie, and Karen Liu. 2024. Pdp: Physics-based character animation via diffusion policy. In _SIGGRAPH Asia 2024 Conference Papers_ . 1–10. 

- Laurens Van der Maaten and Geoffrey Hinton. 2008. Visualizing data using t-SNE. _Journal of machine learning research_ 9, 11 (2008). 

- Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. Attention is all you need. _Advances in neural information processing systems_ 30 (2017). 

- Yuan Wang, Di Huang, Yaqi Zhang, Wanli Ouyang, Jile Jiao, Xuetao Feng, Yan Zhou, Pengfei Wan, Shixiang Tang, and Dan Xu. 2024a. MotionGPT-2: A general-purpose motion-language model for motion generation and understanding. _arXiv preprint arXiv:2410.21747_ (2024). 

- Zhendong Wang, Zhaoshuo Li, Ajay Mandlekar, Zhenjia Xu, Jiaojiao Fan, Yashraj Narang, Linxi Fan, Yuke Zhu, Yogesh Balaji, Mingyuan Zhou, et al. 2024b. One-step diffusion policy: Fast visuomotor policies via diffusion distillation. _arXiv preprint arXiv:2410.21257_ (2024). 

- Yuxin Wen, Qing Shuai, Di Kang, Jing Li, Cheng Wen, Yue Qian, Ningxin Jiao, Changhai Chen, Weijie Chen, Yiran Wang, et al. 2025. HY-Motion 1.0: Scaling Flow Matching Models for Text-To-Motion Generation. _arXiv preprint arXiv:2512.23464_ (2025). 

- Yan Wu, Korrawe Karunratanakul, Zhengyi Luo, and Siyu Tang. 2025a. Uniphys: Unified planner and controller with diffusion for flexible physics-based character control. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . 13214–13224. 

- Zhen Wu, Jiaman Li, Pei Xu, and C Karen Liu. 2025b. Human-object interaction from human-level instructions. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . 11176–11186. 

- Michael Xu, Yi Shi, KangKang Yin, and Xue Bin Peng. 2025. PARC: Physics-based augmentation with reinforcement learning for character controllers. In _Proceedings of the Special Interest Group on Computer Graphics and Interactive Techniques Conference Papers_ . 1–11. 

- Zeyue Xue, Jie Wu, Yu Gao, Fangyuan Kong, Lingting Zhu, Mengzhao Chen, Zhiheng Liu, Wei Liu, Qiushan Guo, Weilin Huang, et al. 2025. Dancegrpo: Unleashing grpo on visual generation. _arXiv preprint arXiv:2505.07818_ (2025). 

- Kai Yang, Jian Tao, Jiafei Lyu, Chunjiang Ge, Jiaxin Chen, Weihan Shen, Xiaolong Zhu, and Xiu Li. 2024. Using human feedback to fine-tune diffusion models without any reward model. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . 8941–8951. 

- Heyuan Yao, Zhenhua Song, Baoquan Chen, and Libin Liu. 2022. Controlvae: Modelbased learning of generative controllers for physics-based characters. _ACM Transactions on Graphics (TOG)_ 41, 6 (2022), 1–16. 

- Heyuan Yao, Zhenhua Song, Yuyang Zhou, Tenglong Ao, Baoquan Chen, and Libin Liu. 2024. Moconvq: Unified physics-based motion control via scalable discrete representations. _ACM Transactions on Graphics (TOG)_ 43, 4 (2024), 1–21. 

- Seonghyeon Ye, Yunhao Ge, Kaiyuan Zheng, Shenyuan Gao, Sihyun Yu, George Kurian, Suneel Indupuru, You Liang Tan, Chuning Zhu, Jiannan Xiang, et al. 2026. World action models are zero-shot policies. _arXiv preprint arXiv:2602.15922_ (2026). 

- Brent Yi, Hongsuk Choi, Himanshu Gaurav Singh, Xiaoyu Huang, Takara E Truong, Carmelo Sferrazza, Yi Ma, et al. 2026. Flow Policy Gradients for Robot Control. _arXiv preprint arXiv:2602.02481_ (2026). 

- Ye Yuan, Jiaming Song, Umar Iqbal, Arash Vahdat, and Jan Kautz. 2023. Physdiff: Physicsguided human motion diffusion model. In _Proceedings of the IEEE/CVF international conference on computer vision_ . 16010–16021. 

- Juze Zhang, Jingyan Zhang, Zining Song, Zhanhe Shi, Chengfeng Zhao, Ye Shi, Jingyi Yu, Lan Xu, and Jingya Wang. 2024. HOI-M<sup>3</sup> : Capture multiple humans and objects interaction within contextual environment. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . 516–526. 

SA Conference Papers ’26, December 01–04, 2026, Kuala Lumpur, Malaysia. 

SCRIPT: Scalable Diffusion Policy with Multi-stage Training for Language-driven Physics-Based Humanoid Control • 13 

- Tonghe Zhang, Chao Yu, Sichang Su, and Yu Wang. 2025c. ReinFlow: Fine-tuning flow matching policy with online reinforcement learning. _arXiv preprint arXiv:2505.22094_ (2025). 

- Yuhong Zhang, Jing Lin, Ailing Zeng, Guanlin Wu, Shunlin Lu, Yurong Fu, Yuanhao Cai, Ruimao Zhang, Haoqian Wang, and Lei Zhang. 2025b. Motion-x++: A large-scale multimodal 3d whole-body human motion dataset. _arXiv preprint arXiv:2501.05098_ (2025). 

- Ziyu Zhang, Sergey Bashkirov, Dun Yang, Yi Shi, Michael Taylor, and Xue Bin Peng. 2025a. Physics-Based Motion Imitation with Adversarial Differential Discriminators. In _Proceedings of the SIGGRAPH Asia 2025 Conference Papers_ . 1–12. 

- Yi Zhou, Connelly Barnes, Jingwan Lu, Jimei Yang, and Hao Li. 2019. On the continuity of rotation representations in neural networks. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . 5745–5753. 

- Bingfan Zhu, Biao Jiang, Sunyi Wang, Shixiang Tang, Tao Chen, Linjie Luo, Youyi Zheng, and Xin Chen. 2025. MotionGPT3: Human motion as a second modality. _arXiv preprint arXiv:2506.24086_ (2025). 

- Qingxu Zhu, He Zhang, Mengting Lan, and Lei Han. 2023. Neural categorical priors for physics-based character control. _ACM Transactions on Graphics (TOG)_ 42, 6 (2023), 1–16. 

SA Conference Papers ’26, December 01–04, 2026, Kuala Lumpur, Malaysia. 

14 • Zhang et al. 

## A Data Curation and Processing Details 

This section provides implementation details of our data curation procedure, including artifact filtering, perturbed rollouts for robustness checking, and padding and window slicing of the tracked trajectories. 

## A.1 Preprocessing and Filtering 

We organize all motion clips following the MotionMillion data format [Fan et al. 2025]. For each SMPL sequence, we compute the 3D positions of 24 joints at each frame via forward kinematics, denoted as _𝑝𝑡_<sup>(</sup><sup>_𝑗_)</sup> ∈ R<sup>3</sup> . We use these joint positions for geometric filtering and rollout quality assessment, filtering both the original kinematic motions and simulated rollouts to obtain high-quality references and tracking data. For kinematic motions, we filter clips using four criteria: sequence length, motion magnitude, ground penetration, and floating artifacts. 

- (1) **Short clips.** We remove clips with _𝑇 <_ 30 frames, since their temporal span is insufficient to form valid history and prediction windows. 

- (2) **Near-static clips.** We compute the mean joint-angle difference within a 1-second sliding window. If the mean difference remains below 2 × 10<sup>−3</sup> for all windows, the clip is considered to contain insufficient motion and is discarded. 

- (3) **Ground penetration.** We define _𝑧𝑡_ = min _𝑗 𝑝𝑡,𝑧_<sup>(</sup><sup>_𝑗_)as the lowest</sup> joint height at frame _𝑡_ . A clip is marked as penetrating if the median value of _𝑧𝑡_ over the final 1 second is more than 0 _._ 05 m lower than that over the first 1 second, and the minimum value of _𝑧𝑡_ over the full sequence is below −0 _._ 03 m. 

- (4) **Floating artifacts.** If the minimum foot-joint height remains above 0 _._ 30 m throughout the sequence and its variance is below 0 _._ 08, we treat the clip as lacking valid ground contact and remove it. 

After raw-motion filtering, some kinematic references may still violate rigid-body constraints when tracked in simulation, leading to tracking failures or jerk artifacts. We therefore further filter simulated rollouts using root-aligned MPJPE to measure tracking accuracy and jerk to measure rollout smoothness. Let _𝑝𝑡_<sup>(</sup><sup>_𝑗_)</sup> and _𝑝_ ˆ _𝑡_<sup>(</sup><sup>_𝑗_)</sup> denote the reference and rollout joint positions, respectively, with the pelvis joint indexed by _𝑗_ = 0. We compute root-aligned MPJPE as 


For rollout smoothness, we compute jerk using the third-order finite difference of joint positions with Δ _𝑡_ = 1/fps: 


We discard rollouts with MPJPE ≥ 0 _._ 15 m or jerk ≥ 600 m/s<sup>3</sup> to remove severe tracking failures and high-frequency artifacts. 


Fig. 8. t-SNE visualization of the retained data. 

## A.2 Perturbed Rollout 

To efficiently process large-scale motion data, we divide the prefiltered motion clips into multiple subsets and train a separate tracking policy [Luo et al. 2023] for each subset. After training, each policy tracks the reference motions from its corresponding subset in parallel, accelerating simulation tracking and state-action data collection. For each rollout, we record the proprioceptive state s _𝑡_ from the simulator and the target PD control action a _𝑡_ predicted by the tracking policy. Specifically, we partition the pre-filtered clips into 160 subsets of approximately 7.2K clips each. Each subset is tracked by a dedicated expert policy trained in 512 parallel environments, following the default PHC configuration. Training concludes when the success rate exceeds 90% for five consecutive evaluations, where success is defined as completing rollouts without falling or large tracking deviations. Following PDP [Truong et al. 2024], we inject small Gaussian perturbations into the executed tracking actions during rollout to broaden the collected state distribution. Behavior cloning on clean expert trajectories mainly covers states near the expert distribution, whereas closed-loop execution may drift away from this distribution due to accumulated prediction errors. Action perturbations expose the tracking policy to off-reference states, while the unperturbed policy output provides corrective supervision for recovery. This produces perturbed-state/clean-action pairs that improve robustness to state deviations. 

Specifically, at simulation step _𝑡_ , the tracking policy outputs an unperturbed action a _𝑡_ . We add isotropic Gaussian noise to obtain the executed action: 


The perturbed action a˜ _𝑡_ is sent to the PD controller, while the unperturbed action a _𝑡_ is saved as supervision. Thus, each training pair consists of the perturbed rollout state s _𝑡_<sup>pert</sup> and the corresponding unperturbed action a _𝑡_ . This encourages the downstream diffusion policy to recover from off-reference states during closed-loop execution. 

## A.3 Data Distribution Visualization 

To examine the coverage of the retained data, we visualize both the language and motion distributions using t-SNE [Van der Maaten and Hinton 2008], as shown in Fig. 8. We represent motion with rollout proprioceptive states s _𝑡_ and language with CLIP pooled text 

SA Conference Papers ’26, December 01–04, 2026, Kuala Lumpur, Malaysia. 

SCRIPT: Scalable Diffusion Policy with Multi-stage Training for Language-driven Physics-Based Humanoid Control • 15 

embeddings cpool, and apply t-SNE to visualize motion diversity and semantic coverage. The state and text visualizations provide complementary views of the collected data. State-space embeddings reveal the diversity of tracked physical motion patterns, while text embeddings reflect the semantic coverage of the language conditions. Together, they suggest that the retained physically executable data preserve both motion diversity and semantic richness. 

scale bounded, we map z _𝑘_ to the log-variance space: 


The final exploration scale is _𝝈𝑘_ = _𝜎𝜙_ ( _𝜏𝑘,_ H _𝑡_ ) = exp( 2<sup><u>1</u>log</sup><sup>_𝝈_</sup> _𝑘_<sup>2). This</sup> parameterization constrains each action-dimension standard deviation to [ _𝜎_ min _, 𝜎_ max], preventing the exploration scale from collapsing to zero or growing unbounded during PPO updates. 

## A.4 Windowed Sample Construction 

To construct fixed-length training samples, we apply first-frame padding and sliding-window slicing to each tracked trajectory. Since nonlinear history sampling requires sufficient past context, we prepend _𝑁_ pad copies of the first frame to support boundary samples near the beginning of a sequence. We then slice the padded trajectory into fixed-length windows according to the history range and prediction horizon _𝐻_ . Each window contains the historical states for constructing H _𝑡_ , the subsequent _𝐻_ -frame state-action supervision targets, and the corresponding text condition _𝑐_ . 

## B Online Reinforcement Learning Post-Training 

## B.1 Stochastic Flow Sampling 

Following ReinFlow [Zhang et al. 2025c], we compute policy likelihoods by treating the stochastic flow sampling process as a Markov chain over Euler steps. Let x _𝑘_ denote the intermediate noisy stateaction trajectory chunk at the _𝑘_ -th Euler step. The deterministic part of the Euler update defines the transition mean 


where y = {H _𝑡,_ ctxt _,_ cpool} denotes the combined policy condition. Let _𝑃𝑎_ (·) denote the projection operator that extracts the action dimensions from the full state-action chunk. We define x _𝑘_<sup>_𝑎_=</sup><sup>_𝑃𝑎_(x</sup><sup>_𝑘_),</sup> _𝝁𝑘_<sup>_𝑎_=</sup><sup>_𝑃𝑎_(</sup><sup>_𝝁𝑘_),and</sup><sup>_𝝈𝑘_=</sup><sup>_𝜎𝜙_(</sup><sup>_𝜏𝑘,_H</sup><sup>_𝑡_),where</sup><sup>_𝝈𝑘_∈R|a|istheper-</sup> dimension exploration scale restricted to the action subspace. Since stochasticity is injected exclusively into the action dimensions, the chain log-likelihood is evaluated as: 


The initial noise term log N (x0; 0 _,_ I) is independent of the policy parameters and safely cancels out in the PPO likelihood ratio calculations. Computing likelihoods only in the action subspace avoids treating deterministic future-state predictions as policy entropy, while retaining tractable transition likelihoods for policy-gradient optimization. 

## B.2 Exploration Noise Network 

We further detail the lightweight network used to predict the exploration scale _𝜎𝜙_ ( _𝜏𝑘,_ H _𝑡_ ) in Eq.9. Consistent with the main text, the network takes the flow time _𝜏𝑘_ and the sampled state history H _𝑡_ as inputs, rather than the AdaLN-Zero condition used by JAST-DiT. Specifically, we first compute a raw output 


where emb( _𝜏𝑘_ ) is a sinusoidal time embedding, _ℎ_ (H _𝑡_ ) is a history projection, and _𝑔𝜙_ is a lightweight MLP. To keep the exploration 

## B.3 Optimization Details 

In this section, we elaborate on the three core components of the RLHR objective: the chain-level PPO ratio, the closed-form entropy bonus, and the velocity-field BC anchor. Based on the chain loglikelihood derived in Eq. 18, the PPO importance ratio is evaluated over the entire stochastic Euler denoising chain. 

_Chain-level PPO Ratio._ Let the per-step action-space transition log-density be 


where x _𝑘_<sup>_𝑎_</sup> +1<sup>and</sup><sup>_𝝁_</sup> _𝑘_<sup>_𝑎_denote the action-dimension sample and tran-</sup> sition mean, respectively, and _𝝈𝑘_ is the corresponding exploration scale. Because the initial noise term in Eq. 18 is independent of the policy parameters, it safely cancels out when computing the importance sampling ratio _𝜌_ ( _𝜃,𝜙_ ) between the current and old policies: 


The clipped PPO surrogate objective is thus formulated as: 


where the advantage estimate _𝐴_<sup>ˆ</sup> is computed using GAE from the physics rollouts. In practice, we clamp the accumulated logprobability differences before exponentiation to prevent numerical overflow, which can otherwise easily occur when summing over high-dimensional action spaces across multiple Euler integration steps. 

_Closed-form Gaussian Entropy._ Because each stochastic Euler transition is modeled as an independent diagonal Gaussian within the action subspace, its step-wise entropy admits a closed-form expression: 


where _𝝈𝑘,𝑖_ denotes the predicted standard deviation for the _𝑖_ -th action dimension at step _𝑘_ . The overall policy entropy bonus is then computed as the average over the entire integration chain: 


Crucially, this formulation is exactly differentiable with respect to the noise network parameters _𝜙_ via _𝝈𝑘_ = _𝜎𝜙_ ( _𝜏𝑘,_ H _𝑡_ ). This property allows us to systematically regularize the exploration scale without relying on high-variance, sampling-based entropy estimators. 

SA Conference Papers ’26, December 01–04, 2026, Kuala Lumpur, Malaysia. 

16 • Zhang et al. 

_Velocity-field BC Anchor._ The BC anchor introduced in Eq.13 is designed as a velocity-field regularizer rather than a direct actionspace constraint. By anchoring the fine-tuned velocity field _𝑣𝜃_ to the frozen pretrained model _𝑣𝜃_ 0 , this term preserves the foundational geometric prior established during Stage-I flow matching, while allowing PPO to optimize the induced action distribution for specific task rewards. To maintain strict consistency with the original flow-matching objective, the BC triplets (x _,𝜏, 𝝐_ ) are independently resampled for each update rather than reusing the integration chains from physics rollouts. This decoupled sampling ensures that the anchor remains a robust regularizer, preventing the policy from collapsing toward sub-optimal local modes during reinforcement learning. 

frozen and used to extract state and text features, as well as to score the semantic consistency between generated state sequences and language conditions. 

## D Evaluation Metrics 

_Text-following Metrics._ We compute text-following metrics in the shared embedding space of the frozen text-state aligner described in Sec. C. Given _𝐵_ paired generated state sequences and text conditions, let z _𝑠_<sup>(</sup><sup>_𝑖_)</sup> and z _𝑡_<sup>(</sup><sup>_𝑖_)</sup> denote their normalized state and text embeddings. For R-Precision, we retrieve the paired text for each generated state sequence within the batch: 


## C Text-State Aligner 

We report _𝑘_ = 1 _,_ 2 _,_ 3, where higher values indicate better text– motion alignment. 

To establish a shared representation space between physical state trajectories and language instructions, we train a text-state contrastive aligner. This aligner remains frozen during the RLHR stage and is utilized for both semantic reward computation and evaluation. The model follows a symmetric two-tower architecture comprising a state trajectory encoder and a text encoder, which map their respective modalities into a shared 512-dimensional latent space. Each training sample contains a state sequence S = {s _𝑡_ }<sup>_𝑇_</sup> _𝑡_ =1<sup>, where</sup> s _𝑡_ ∈ R<sup>358</sup> , and the CLIP pooled embedding of the corresponding text, cpool ∈ R<sup>1280</sup> [Radford et al. 2021]. The CLIP embeddings are extracted offline with a frozen text encoder and cached before training. The state inputs are normalized to [−1 _,_ 1] with a min–max normalizer before encoding. 

MM-Dist measures the average distance between paired state and text embeddings: 


Lower values indicate closer semantic alignment. 

For FID, we fit Gaussian distributions to the generated and reference state embeddings, denoted by ( _𝝁_ gen _,_ **𝚺** gen) and ( _𝝁_ ref _,_ **𝚺** ref ), respectively: 


The state encoder first projects each 358-dimensional state vector to a 1024-dimensional latent space with a linear layer. We prepend a learnable query token to the sequence, add sinusoidal positional encodings, and feed the resulting tokens into an 8-layer Transformer encoder [Vaswani et al. 2017] with hidden dimension 1024, FFN dimension 2048, 8 attention heads, and dropout 0.1. The output corresponding to the query token is then projected to 512 dimensions and L2-normalized to obtain the state embedding z _𝑠_ . The text encoder consists of a linear projection that maps the precomputed CLIP pooled embedding cpool to the same 512-dimensional space, followed by L2 normalization to obtain the text embedding z _𝑡_ . 

_Physical-plausibility Metrics._ We compute physical-plausibility metrics directly from the global SMPL joint positions p _𝑡_<sup>(</sup><sup>_𝑗_)</sup> ∈ R<sup>3</sup> , where _𝑗_ = 1 _, . . . , 𝐽_ and the _𝑧_ axis points upward. Floating measures the average positive clearance between the lowest body joint and the ground, with a tolerance _𝜏_ tol = 0 _._ 005 m: 


We train the two-tower model with a symmetric InfoNCE loss [Oord et al. 2018]. For a batch of _𝐵_ paired state sequences and text conditions, let z _𝑠_<sup>(</sup><sup>_𝑖_)</sup> and z _𝑡_<sup>(</sup><sup>_𝑗_)</sup> denote the normalized embeddings of the _𝑖_ -th state sequence and the _𝑗_ -th text condition, respectively. The similarity matrix is defined as 

Jerk measures trajectory smoothness using the same third-order finite-difference form as Eq. (15), but for evaluation we report the frame-based value in mm/frame<sup>3</sup> . Specifically, we omit the Δ _𝑡_<sup>3</sup> normalization and multiply by 10<sup>3</sup> to convert meters to millimeters. Lower values indicate smoother motions with fewer high-frequency artifacts. 


_𝑠 𝑡 ,_ Duration Time measures how long the agent remains valid during _𝛾_ is a learnable temperature parameter. The training objective simulation before falling. Following the early-termination criterion averages the state-to-text and text-to-state cross-entropy losses: used in PHC, we terminate a rollout when the pelvis height falls below a threshold, i.e., _𝑝𝑡,𝑧_<sup>(root)</sup> _< 𝜏_ fall. If no fall is detected, the rollout Lalign =<sup>1</sup> 2 �CE( _𝑆,_ y) + CE( _𝑆_<sup>⊤</sup> _,_ y)� _,_ y = (1 _, . . . , 𝐵_ ) _._ (26) is considered successfully tracked to the end. We define Duration Time as the ratio between the total number of valid simulated frames We train the aligner with AdamW for 300 epochs, using an initial before termination and the total number of reference frames across rate of 1 × 10 × 10 10<sup>−44</sup> , weight decay 1 × 10 × 10 10<sup>−44</sup> , and batch size all rollouts: 

where _𝛾_ is a learnable temperature parameter. The training objective averages the state-to-text and text-to-state cross-entropy losses: 

We train the aligner with AdamW for 300 epochs, using an initial learning rate of 1 × 10 × 10 10<sup>−44</sup> , weight decay 1 × 10 × 10 10<sup>−44</sup> , and batch size 96. The learning rate is decayed to 1 × 10<sup>−7</sup> with cosine annealing. The maximum state sequence length is set to 400, matching the pre-sliced training window size. After training, the aligner is 


SA Conference Papers ’26, December 01–04, 2026, Kuala Lumpur, Malaysia. 

SCRIPT: Scalable Diffusion Policy with Multi-stage Training for Language-driven Physics-Based Humanoid Control • 17 

We set _𝜏_ fall = 0 _._ 15 m, consistent with the default termination height in PHC, and use the same threshold for all methods. 

## E Training Details 

_HumanML3D Pretraining._ We train SCRIPT-Large, a 0.5B-scale model with 577.97M parameters, on HumanML3D as the main pretrained model for benchmark comparison. The model uses a 10-layer JAST-DiT with hidden dimension 768, 6 attention heads, and head dimension 128. We set the prediction horizon to _𝐻_ = 4 and the history length to _𝐿_ max = 154, resulting in a training window of 158 frames with stride 2. 

Training is performed on a single node with 8 A100 GPUs using PyTorch DDP. We use bf16 mixed precision and enable TF32 acceleration. The optimizer is AdamW with learning rate 1×10<sup>−4</sup> , a 1K-step linear warmup, _𝛽_ = (0 _._ 9 _,_ 0 _._ 999), and weight decay 1 × 10<sup>−4</sup> . We use an EMA decay of 0.9999, enabled after the first 1K warmup steps. The per-GPU batch size is 1024, giving an effective global batch size of 8192. The model is trained for 110K steps. For classifier-free guidance, the text condition is replaced with an empty string with probability 10%. We use the EMA weights of the pretrained model as the behavior-cloning checkpoint for downstream RL initialization. 

_MotionMillion Scaling Pretraining._ For scaling experiments on MotionMillion, we increase the history length to _𝐿_ max = 604 and use a training window of 608 frames with stride 2. We train three model variants that differ only in network depth and width: Base, Large, and Huge. Base uses 8 layers, hidden dimension 512, and 4 attention heads; Large uses 10 layers, hidden dimension 768, and 6 attention heads; Huge uses 12 layers, hidden dimension 1024, and 8 attention heads. The head dimension is fixed to 128 for all variants. These models have approximately 0.2B, 0.5B, and 1.2B parameters, respectively. 

All variants are trained on a single node with 8 A100 GPUs using PyTorch DDP and bf16 mixed precision. We use AdamW with learning rate 1 × 10<sup>−4</sup> and a 1K-step warmup, together with EMA decay 0.9999. All models are trained for 560K steps, with checkpoints saved every 20K steps. The classifier-free guidance setting follows the HumanML3D pretraining stage, using 10% text-condition dropout. 

_RLHR Post-Training._ We initialize the actor from the EMA weights of the HumanML3D pretrained checkpoint and use a lightweight MLP critic with approximately 1.4M parameters. RL post-training is performed on a single A100 GPU with 128 parallel Isaac Gym environments. The simulation uses the PHC humanoid with 24 SMPL body parts and PD control over 23 actuated joints. 

Each PPO iteration collects 300 frames per environment. We optimize for 5 epochs with mini-batch size 1280 and train for up to 300 iterations. Both actor and critic use cosine learning-rate schedules, with peak learning rates of 1 × 10<sup>−5</sup> and 1 × 10<sup>−3</sup> , respectively, and a first cycle length of 1500 optimization steps. We use PPO clipping threshold _𝜖_ = 0 _._ 10, discount factor _𝛾_ = 0 _._ 99, maximum gradient norm 1.0, and running reward scaling. 

During Euler sampling, we inject learnable Gaussian exploration noise only into the action dimensions. The noise scale is predicted by a lightweight network and constrained to _𝜎_ ∈[0 _._ 03 _,_ 0 _._ 08]. The 

training objective combines the PPO loss, value loss, entropy regularization, and a velocity-form behavior-cloning anchor with coefficient 1.0. The hybrid reward consists of a dense physical reward with weight 1.0 and a sequence-level episodic contrastive text reward with coefficient 20. 

_Training and Inference Cost._ For the main HumanML3D benchmark, Stage-I pretraining of SCRIPT-Large on HumanML3D takes approximately 30 hours on a single node with eight A100 GPUs, with a measured throughput of 1.04 steps/s. Stage-II RLHR post-training is performed on a single A100 GPU with 128 parallel simulation environments. The checkpoint used for the reported Stage-II results was obtained after 160 PPO iterations, requiring approximately four days of training. At inference time, SCRIPT-Large generates an action chunk of _𝐻_ = 4 frames in approximately 333 ms on a single A100 GPU. Each prediction uses 10 denoising steps, where each step requires one conditional and one unconditional network evaluation for classifier-free guidance, resulting in 20 network evaluations in total. Thus, the inference latency is approximately 2 _._ 5× the duration of the generated action chunk. 

## F Limitations and Future Work 

Although SCRIPT jointly integrates action, state, and language representations, several limitations remain. SCRIPT currently focuses on whole-body humanoid control on flat terrain. Therefore, SCRIPT does not support fine-grained hand articulation and grasping [Luo et al. 2024a], humanoid loco-manipulation [He et al. 2025b], or scene-aware interaction in cluttered environments [Pan et al. 2025]. Furthermore, during data curation, we use multiple expert tracking policies in parallel to extract state-action demonstrations and retain only reference motions and simulated rollouts that pass our predefined motion-quality, tracking-error, and smoothness filters. Although this filtering improves the physical validity of the retained data, it may underrepresent challenging yet physically feasible motions and bias the learned policy toward the curated training distribution. Consequently, prompts describing underrepresented or out-of-distribution motions may lead to loss of balance or visible artifacts, whereas physically infeasible requests, such as sustained unsupported flight (e.g., “flying like an airplane”), cannot be reliably realized by the current embodiment. Finally, the current implementation is not yet optimized for high-frequency, real-time closed-loop humanoid control. Benefiting from the flow-matching formulation, our policy is able to generate an action chunk with only 10 denoising steps. However, further optimization is still required to achieve high-frequency real-time interactive control. Future work will focus on improving inference efficiency through acceleration techniques, such as policy distillation [Wang et al. 2024b], reduced sampling steps [Salimans and Ho 2022; Song et al. 2023], and optimized noise schedules [Ye et al. 2026], while extending SCRIPT toward richer human-object interactions and real-world humanoid deployment. 

## G Discussion 

The JAST-DiT architecture achieves excellent performance during the initial imitation learning stage. Ablation experiments reveal that the history conditioning mechanism dictates generation quality and 

SA Conference Papers ’26, December 01–04, 2026, Kuala Lumpur, Malaysia. 

18 • Zhang et al. 

stability, while the independent text and state streams anchor semantics and physical feasibility. This confirms that coupling dedicated token streams through joint attention ensures accurate instruction execution and prevents motion homogenization. Beyond the architecture, large-scale curated data underpins these gains, and all metrics improve monotonically with model capacity without saturation. RLHR builds upon this imitation anchor to mitigate state drift through interactive exploration in physics simulation. This optimization grants the policy robust recovery capabilities against 

sudden external forces, enabling steady execution when facing perturbations. During RL exploration, policies tend to converge toward conservative survival behaviors to avoid falling, generating degenerate motions that deviate from textual instructions. The hybrid reward mechanism counteracts this tendency via mandatory semantic alignment, suggesting that closed-loop control systems must establish strict cross-modal constraints to balance physical stability and instruction fidelity. 

SA Conference Papers ’26, December 01–04, 2026, Kuala Lumpur, Malaysia. 

