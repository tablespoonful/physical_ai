---
title: "AC^2-VLA: Action-Context-Aware Adaptive Computation in Vision-Language-Action Models for Efficient Robotic Manipulation"
date: "2026-01-27"
authors: "Wenda Yu; Tianshi Wang; Fengling Li; Jingjing Li; Lei Zhu"
url: https://arxiv.org/abs/2601.19634
pdf: https://arxiv.org/pdf/2601.19634
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.19634)** / [論文ページ](https://arxiv.org/abs/2601.19634)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **AC**<sup>2</sup> **-VLA: Action-Context-Aware Adaptive Computation in Vision-Language-Action Models for Efficient Robotic Manipulation Wenda Yu**<sup>1</sup> , **Tianshi Wang**<sup>1</sup><sup>_∗_</sup> , **Fengling Li**<sup>2</sup> , **Jingjing Li**<sup>3</sup> , **Lei Zhu**<sup>1</sup> 

1Tongji University 

2University of Technology Sydney 

3University of Electronic Science and Technology of China 

yu ~~w~~ enda@126.com, tswang0116@163.com, fenglingli2023@gmail.com, lijin117@yeah.net, leizhu0608@gmail.com 

## **Abstract** 

Vision-Language-Action (VLA) models have demonstrated strong performance in robotic manipulation, yet their closed-loop deployment is hindered by the high latency and compute cost of repeatedly running large vision-language backbones at every timestep. We observe that VLA inference exhibits structured redundancies across temporal, spatial, and depth dimensions, and that most existing efficiency methods ignore action context, despite its central role in embodied tasks. To address this gap, we propose ActionContext-aware Adaptive Computation for VLA models (AC<sup>2</sup> -VLA), a unified framework that conditions computation on current visual observations, language instructions, and previous action states. Based on this action-centric context, AC<sup>2</sup> - VLA adaptively performs cognition reuse across timesteps, token pruning, and selective execution of model components within a unified mechanism. To train the adaptive policy, we introduce an actionguided self-distillation scheme that preserves the behavior of the dense VLA policy while enabling structured sparsification that transfers across tasks and settings. Extensive experiments on robotic manipulation benchmarks show that AC<sup>2</sup> -VLA achieves up to a 1.79 _×_ speedup while reducing FLOPs to 29.4% of the dense baseline, with comparable task success. Source codes can be found at https://github.com/SunnyYWD/AC-2-VLA. 

## **1 Introduction** 

Recent progress in vision-language foundation models and large-scale robot datasets such as Open X-Embodiment [O’Neill _et al._ , 2023] have accelerated the development of generalist Vision-Language-Action (VLA) models. In closed-loop embodied tasks, these models must deliver lowlatency decisions with stable closed-loop control over longhorizon tasks. Representative methods such as RT-2 [Brohan _et al._ , 2023] and OpenVLA [Kim _et al._ , 2024] demonstrate that large multimodal backbones can follow language 

> _∗_ Corresponding author. 


Figure 1: Comparison of efficient VLA computation strategies. Existing methods typically apply cache reuse, token pruning, or layer skipping based on visual or heuristic cues in an uncoordinated manner, resulting in action-context-agnostic efficiency. In contrast, AC<sup>2</sup> - VLA leverages action context to jointly gate cache reuse, token pruning, and layer skipping for action-context-aware efficiency. 

instructions and generalize to diverse tasks. More recent policies such as CogACT [Li _et al._ , 2024a] further improve control by generating expressive action trajectories via diffusionbased modeling. However, deploying these models remains challenging because inference repeatedly executes a computationally expensive vision-language backbone at every control step, resulting in high latency and compute cost, reducing control frequency, and compromising real-time responsiveness in dynamic environments. 

To mitigate these deployment challenges, recent work has explored various efficiency mechanisms for VLA models. _Static compression methods_ such as pruning [Yang _et al._ , 2025] and quantization [Fang _et al._ , 2025] reduce model size but cannot adapt to changing task complexity. _Dynamic computation techniques_ , including token pruning [Tan _et al._ , 2025] and layer skipping [Zhang _et al._ , 2025], adjust compute online, while caching approaches such as VLA-Cache [Xu _et al._ , 2025] exploit temporal redundancy by reusing features across adjacent timesteps. Despite these advances, most existing methods make compute allocation decisions primarily based on visual cues, which can be suboptimal for robot manipulation. In embodied tasks, visual complexity does 

not necessarily correlate with control difficulty: visually simple scenes may require full-capacity reasoning for precise interactions, while visually complex transit phases may allow more aggressive pruning. 

Based on this insight, we present Action-Context-aware Adaptive Computation for VLA models (AC<sup>2</sup> -VLA), as illustrated in Fig. 1. AC<sup>2</sup> -VLA dynamically allocates computation along the temporal, spatial, and depth dimensions, guided by the action-centric context that is directly relevant to embodied tasks. Specifically, we introduce a lightweight action-prior router that conditions on the previous action state together with multimodal embeddings, and predicts a unified sparsity strategy for the current timestep. The router orchestrates three complementary mechanisms: _(i) cognition caching_ , which reuses backbone features across adjacent timesteps when the action context suggests stable state transitions; _(ii) action-context-aware token pruning_ , which removes visual tokens that are irrelevant to the current manipulation stage; and _(iii) conditional layer skipping_ , which bypasses redundant transformer blocks when the action context indicates lower reasoning demand. To preserve the robustness of the original dense policy under structured sparsification, we train the router using an action-guided self-distillation scheme that encourages consistent action predictions while enabling adaptive computation. Results show that AC<sup>2</sup> -VLA significantly reduces inference cost while maintaining strong manipulation success rates, highlighting the effectiveness of action-guided adaptive computation for efficient closed-loop control. In summary, our contributions are as follows: 

- We identify that computation redundancy in VLA models aligns more with action context than visual cues, and propose action-context-aware adaptive computation for efficient robotic manipulation. 

- We propose AC<sup>2</sup> -VLA with an action-prior router that adaptively coordinates cognition caching, token pruning, and layer skipping, supported by action-guided selfdistillation for robust sparsification. 

- Experiments on robotic manipulation benchmarks show substantial latency and FLOPs reductions with minimal performance degradation, and confirm consistent gains over baselines with extensive ablations. 

## **2 Related Work** 

### **2.1 Vision-Language-Action Models** 

The rapid progress of VLMs, together with large-scale robot data collections such as Open X-Embodiment [O’Neill _et al._ , 2023], has accelerated the emergence of generalist embodied policies that unify perception, instruction following, and action prediction. Among modern VLA systems, the RT series, such as RT-1 and RT-2, demonstrates that tokenbased autoregressive decoding can scale to broad task sets via large multimodal backbones [Brohan _et al._ , 2022; Brohan _et al._ , 2023]. Building on similar foundations, OpenVLA [Kim _et al._ , 2024] further systematizes training and evaluation for vision-language-action modeling at scale. In parallel, diffusion- and flow-based policies have become a compelling alternative for continuous control, where action gen- 

eration is formulated as conditional denoising or flow matching and sampled as coherent trajectories, such as CogACT [Li _et al._ , 2024a] and the _π_ 0 _/π_ 0 _._ 5 line [Black _et al._ , 2024; Black _et al._ , 2025]. Despite their strong generalization and stable closed-loop behaviors, these models share a common deployment bottleneck: regardless of paradigm, VLA inference is dominated by repeatedly executing a large multimodal backbone, leading to high latency in real-time control. 

### **2.2 Efficient VLA Strategies** 

Prior work on efficient VLA strategies broadly falls into four categories: lightweight model design, dynamic routing and conditional execution, compression via pruning and quantization, and temporal reuse through caching or compute switching. Lightweight designs reduce per-step cost by scaling down backbones or streamlining training and inference, such as TinyVLA [Wen _et al._ , 2024], SmolVLA [Shukor _et al._ , 2025], and FLOWER [Reuss _et al._ , 2025]. Dynamic routing methods reduce computation by activating only a subset of the model, such as MoLe-VLA [Zhang _et al._ , 2025] and instruction-driven routing with structured sparsification in CogVLA [Li _et al._ , 2025a]. Compression-oriented approaches aim to remove redundant tokens and layers or codesign pruning with quantization, such as LightVLA [Jiang _et al._ , 2025], FlashVLA [Tan _et al._ , 2025], and SQAPVLA [Fang _et al._ , 2025]. Temporal reuse exploits redundancy across adjacent control steps by reusing cognition or switching computation modes, such as VLA-Cache [Xu _et al._ , 2025], SP-VLA [Li _et al._ , 2025b], and VOTE [Lin _et al._ , 2025]. However, existing methods often target only one redundancy axis or rely on static heuristics without modeling action context, limiting robustness in closed-loop control. In contrast, AC<sup>2</sup> -VLA uses action context for routing and unifies temporal reuse, spatial sparsification, and depthwise conditional execution within an action-prior router. 

## **3 Method** 

### **3.1 Overview** 

Given a visual observation _xt_ and a language instruction _u_ , a VLA model predicts an action chunk **a** _t_ : _t_ + _H_ with horizon _H_ . We consider a generic VLA pipeline that factorizes action generation into a multimodal backbone and an action head: 


Here, _pϕ_ can be instantiated as an autoregressive decoder or a diffusion/flow-based trajectory generator, depending on the underlying VLA policy. 

In real-time deployment, inference is bottlenecked by repeatedly executing the VLM backbone at every control step. We observe structured computation redundancies along three complementary axes: 

- ( _i) Temporal redundancy_ : backbone representations can be reused across adjacent timesteps; 

- ( _ii) Spatial redundancy_ : only a subset of vision tokens is necessary for action prediction; 

- ( _iii) Depth redundancy_ : executing fewer backbone layers often suffices with minimal performance loss. 


Figure 2: Overview of the proposed AC<sup>2</sup> -VLA. At each timestep, the model builds an action-prior condition **c** _t_ from the current observation, instruction, and action context, and uses a unified router to generate token pruning, layer skipping, and cache reuse gates, enabling efficient computation and low-latency control. 

To exploit these redundancies within a unified mechanism, AC<sup>2</sup> -VLA introduces an action-prior router, as shown in Fig. 2. At each timestep, conditioned on the action-centric context **c** _t_ , an action-prior router generates a set of computation gates for temporal reuse, spatial token selection, and depth-wise conditional execution: 


where _Nv_ and _L_ denote the numbers of vision tokens and transformer layers, respectively. The cache gate _p_<sup>cache</sup> _t_ determines whether to reuse cached backbone representations, while **p**<sup>topk</sup> _t_ and **p**<sup>lay</sup> _t_ control token pruning and conditional layer execution. We train the router via teacher-student distillation with lightweight regularization to preserve densepolicy behavior under structured sparsification. 

Overall, AC<sup>2</sup> -VLA jointly optimizes temporal reuse, token selection, and conditional layer execution, enabling efficient inference for closed-loop robotic manipulation. 

### **3.2 Action-Context-aware Unified Routing** 

AC<sup>2</sup> -VLA is driven by an action-prior condition vector **c** _t_ that explicitly encodes the robot’s action context. In closed-loop control, the next action distribution is strongly shaped by the ongoing motion state, making the previous action **a** _t−_ 1 a natural and inexpensive prior for allocating computation. We therefore use **a** _t−_ 1, parameterized consistently with the action head, as the primary routing signal. When no previous action is available at the first step, we set **a** _t−_ 1 = **0** and rely on lightweight visual and instruction summaries to generate initial gates. 

Let **V** _t ∈_ R<sup>_Nv×dv_</sup> denote per-token vision features, and we summarize them with a mean-max mixture: 


For language, we avoid an additional full forward by pooling embedded instruction tokens **E** _t ∈_ R<sup>_T ×d_</sup> : 


where _ℓt_ denotes the last valid token index under the attention mask when available, otherwise we use mean pooling. 

We embed the action-head step index _τt_ with a sinusoidal encoder **e** ( _τt_ ), which captures the internal generation progress of the action head. When reuse is enabled, we additionally include a cache-state cue **s**<sup>_c_</sup> _t_<sup>encodingthequantized</sup> action-delta proxy used for cache keying, together with compact cache statistics and an availability probe. All inputs are projected to a shared hidden size and fused by an MLP: **c** _t_ = _f_ fuse( _ψa_ ( **a** _t−_ 1) _, ψv_ ( **s**<sup>_v_</sup> _t_<sup>)</sup><sup>_,ψu_(</sup><sup>**s**</sup> _t_<sup>_u_)</sup><sup>_,_</sup> (5) _ψτ_ ( **e** ( _τt_ )) _, ψc_ ( **s**<sup>_c_</sup> _t_<sup>))</sup><sup>_._</sup> 

In implementation, vision tokens and pooled summaries are detached before entering the router to prevent gradients from flowing into heavyweight backbone components through the routing pathway. 

Given **c** _t_ , the router predicts three gate families: a reuse probability _p_<sup>cache</sup> _t_ , token keep scores **p**<sup>topk</sup> _t_ , and layer execution gates **p**<sup>lay</sup> _t_<sup>.We detail each gate in the following.</sup> **Cache reuse gate.** We predict a scalar reuse probability: 


where _T_ cache controls gate sharpness. A high _p_<sup>cache</sup> _t_ indicates a reuse request, while an actual reuse occurs only when the cache lookup succeeds. 

**Token pruning gate.** For each vision token **v** _t,i_ , we predict its keep score via action-conditioned matching: 


where _gt,i_ is an optional lightweight bias such as a geometric prior derived from the current observation. During inference, 

tokens are compacted by keeping the top-ranked ones according to _p_<sup>topk</sup> _t,i_ . 

**Layer skipping gate.** We predict per-layer execution probabilities: 


with bias initialization that favors near-dense execution early in training. At runtime, transformer blocks with low _p_<sup>lay</sup> _t,ℓ_<sup>are</sup> conditionally bypassed to reduce depth-wise computation. 

### **3.3 From Unified Gating to Practical Speedups** 

We next describe how the unified gates translate into practical inference speedups in AC<sup>2</sup> -VLA, through feature reuse across timesteps, spatial token pruning with compaction, and depth-wise conditional execution. Algorithm 1 summarizes the resulting inference-time procedure. 

**Cache reuse.** When the router predicts a high reuse probability _p_<sup>cache</sup> _t_ , we attempt to bypass the expensive multimodal backbone forward by querying a cognition cache. Specifically, we build a compact and robust cache key that captures both motion continuity and visual consistency. We first pool the vision tokens: 


and form the cache key as 

**Algorithm 1** AC<sup>2</sup> -VLA inference for a single control step _t_ 

**Input** : visual observation _xt_ , instruction _u_ , previous action **a** _t−_ 1, step index _τt_ , cache _C_ **Output** : action chunk **a** _t_ : _t_ + _H_ 1: **V** _t ← f_ vis( _xt_ ); **v** ¯ _t ←_ MeanPool( **V** _t_ ) 2: **s**<sup>_v_</sup> _t_<sup>_←_</sup><sup><u>1</u></sup> 2<sup>(MeanPool(</sup><sup>**V**</sup><sup>_t_) + MaxPool(</sup><sup>**V**</sup><sup>_t_))</sup> 3: **s**<sup>_u_</sup> _t_<sup>_←_EmbedPool(</sup><sup>_u_)</sup> 4: **c** _t ← f_ fuse( _ψa_ ( **a** _t−_ 1) _, ψv_ ( **s**<sup>_v_</sup> _t_<sup>)</sup><sup>_, ψu_(</sup><sup>**s**</sup><sup>_u_</sup> _t_<sup>)</sup><sup>_, ψτ_(</sup><sup>**e**(</sup><sup>_τt_))</sup><sup>_, ψc_(</sup><sup>**s**</sup><sup>_c_</sup> _t_<sup>))</sup> 5: ( _p_<sup>cache</sup> _t ,_ **p**<sup>topk</sup> _t ,_ **p**<sup>lay</sup> _t_<sup>)</sup><sup>_←R_(</sup><sup>**c**</sup><sup>_t_)</sup> 6: _ht ←_ 0 7: **if** REUSEREQ( _p_<sup>cache</sup> _t_ ) **then** 8: ∆ **a** _t ←_ DeltaProxy( **a** _t−_ 1) 9: _kt ←_ (Quant( _∥_ ∆ **a** _t∥_ ) _,_ Hash(¯ **v** _t_ )) 10: ( _ht,_ **z** _t_ ) _←C._ Get( _kt_ ) 11: **end if** 12: **if** _ht_ = 0 **then** 13: **m** _t ←_ TopKMask( **p**<sup>topk</sup> _t_ ); **g** _t ←_ BinGate( **p**<sup>lay</sup> _t_<sup>)</sup> 14: ( **V**<sup>˜</sup> _t,_ **_π_** _t, Nv_<sup>orig</sup> ) _←_ Compact( **V** _t,_ **m** _t_ ) 15: pos _t ←_ RoPEAlign( **_π_** _t, Nv_<sup>orig</sup> ) 16: **z** _t ← f_ VLM( _xt, u_ ; **V**<sup>˜</sup> _t,_ pos _t,_ **g** _t_ ) 17: **if** REUSEREQ( _p_<sup>cache</sup> _t_ ) **then** 18: _C._ Put( _kt,_ **z** _t_ ) _{_ write back only on request & miss _}_ 19: **end if** 

20: **end if** 21: **a** _t_ : _t_ + _H ← pϕ_ ( **a** _|_ **z** _t_ ; _τt_ ) 22: **return a** _t_ : _t_ + _H_ 


where Quant( _∥_ ∆ **a** _t∥_ ) is an action-delta norm proxy, and Hash(¯ **v** _t_ ) is a lightweight vision hash for state matching. The robust hash normalizes ¯ **v** _t_ , applies a fixed random projection, and quantizes before hashing. 

We distinguish a reuse request from an actual cache hit _ht ∈{_ 0 _,_ 1 _}_ . When a hit occurs, we directly reuse the cached multimodal representation **z** _t_ and skip the VLM backbone forward, otherwise we compute **z** _t_ = _f_ VLM( _xt, u_ ) as usual. To keep cache population consistent with the router’s intent, we only write back the newly computed **z** _t_ when reuse was requested but the lookup missed. 

**Token Pruning.** Token gating determines which vision tokens should be retained. To obtain real wall-clock speedups beyond attention masking, we perform token pruning by physically removing pruned tokens and shortening the transformer sequence. Let **m** _t ∈{_ 0 _,_ 1 _}_<sup>_Nv_</sup> denote the keep mask. Compaction produces 


where **_π_** _t_ maps each kept token to its original patch index. We always keep at least one token to prevent degenerate empty sequences. 

For Rotary Position Embedding (RoPE)-based backbones, naive reindexing after compaction would distort the original patch coordinates. We therefore preserve RoPE-consistent patch positions using **_π_** _t_ : 


and assign text positions to start after the original patch span _Nv_<sup>orig</sup> recorded during compaction: 


During training, to stabilize optimization and maintain differentiability, we adopt a soft relaxation by scaling projected patch embeddings with token keep scores: 


Hard compaction is applied only at inference time for maximum speedup. 

**Layer Skipping.** We implement conditional depth execution by wrapping each transformer block with a lightweight gating mechanism. Given the hidden state **h**<sup>(</sup><sup>_ℓ_)</sup> at layer _ℓ_ , the gated residual update is defined as 


where _Fℓ_ ( _·_ ) denotes the _ℓ_ -th transformer block and _αt,ℓ ∈_ [0 _,_ 1] is the layer gate derived from _p_<sup>lay</sup> _t,ℓ_<sup>.Duringtraining,</sup> _αt,ℓ_ remains soft; at inference, it is binarized so that inactive samples bypass the layer entirely. 

For efficient execution, active samples are dynamically grouped into a sub-batch to run _Fℓ_ ( _·_ ), and the results are scattered back to the full batch. 

### **3.4 Optimization** 

We train the router to preserve dense-policy behavior under sparse execution with: 


|**Google Robot**|**Method**|||**Success Rate (**|_↑_**)**||
|---|---|---|---|---|---|---|
|||**PickCan**|**MoveNear**|**Drawer**|**DrawerApple**|**Average**|
||RT-1|85.7%|44.2%|73.0%|6.5%|52.4%|
||RT-1-X|56.7%|31.7%|59.7%|21.3%|42.4%|
||RT-2-X|78.7%|77.9%|25.0%|3.7%|46.3%|
|Visual Matching|Octo-Base|17.0%|4.2%|22.7%|0.0%|11.0%|
||OpenVLA|18.0%|56.3%|63.0%|0.0%|34.3%|
||CogACT|91.3%|85.0%|71.8%|50.9%|74.8%|
||**AC**<sup>2</sup>**-VLA**|**97.2%**|**82.7%**|**80.6%**|**46.8%**|**76.8%**|
||RT-1|89.8%|50.0%|32.3%|2.6%|43.7%|
||RT-1-X|49.0%|32.3%|29.4%|10.1%|30.2%|
||RT-2-X|82.3%|79.2%|35.3%|20.6%|54.4%|
|Variant Aggregation|Octo-Base|0.6%|3.1%|1.1%|0.0%|1.2%|
||OpenVLA|60.8%|67.7%|28.8%|0.0%|39.3%|
||CogACT|89.6%|80.8%|28.3%|46.6%|61.3%|
||**AC**<sup>2</sup>**-VLA**|**88.7%**|**84.4%**|**28.2%**|**45.1%**|**61.6%**|


Table 1: Google Robot success rates on SIMPLER under two evaluation settings. Most baseline results are reported by CogACT, and we add the AC<sup>2</sup> -VLA row by evaluating our method under the same protocol. 

**Action-guided self-distillation.** We use a teacher-student scheme, where the teacher runs the dense policy and the student executes routed sparse inference, including cache reuse, token pruning, and layer skipping. We distill both action outputs and cognition features: 

that aims to narrow the real-to-sim gap. We report results on two robot embodiments under three protocols: 

- **Google Robot Visual Matching:** Tests generalization in visually matched real-world conditions on tasks including Pick Coke Can, Move Near, Open/Close Drawer, and Place Apple. 


- **Google Robot Variant Aggregation:** Introduces variations in background, lighting, and distractors, providing a more challenging robustness setting. 

where ˆ **_ϵ_** denotes the action prediction, and **z** _t_ is the backbone representation. _λϵ_ and _λz_ control the relative weights, and _D_ ( _·, ·_ ) is a feature-matching distance. 

- **WidowX Visual Matching:** Evaluates fine-grained manipulation on WidowX with tasks including Put Spoon on Towel, Put Carrot on Plate, Stack Cube, and Put Eggplant in Basket. 

**Regularization and temporal smoothing.** We add _Lreg_ to enforce target token/layer budgets and supervise the reuse gate, and _Ltemp_ to penalize abrupt changes in gating decisions across timesteps for stable closed-loop control. 

Following standard SIMPLER protocols, we use 3 Hz control **4 Experiment** with 513 Hz simulation for Google Robot and 5 Hz control **4.1 Experimental Setup** with 500 Hz simulation for WidowX. Episodes are capped at 80 steps for Google Robot and 120 steps for WidowX to **Backbones.** We build AC<sup>2</sup> -VLA on CogACT [Li _et al._ , penalize inefficient or stalled behaviors. 

**Backbones.** We build AC<sup>2</sup> -VLA on CogACT [Li _et al._ , 2024a], a diffusion-based VLA model with a Prismatic-7B vision-language backbone and a DiT-Base action head. To isolate routing effects, we freeze the pre-trained vision and language backbones and optimize only the lightweight routing modules, while keeping the action head unchanged with 8 denoising steps. 

**Baselines.** We compare AC<sup>2</sup> -VLA with two groups of baselines: generalist dense VLA policies and efficiency-oriented methods. 

**Generalist VLA Models:** We report results for RT-1 [Brohan _et al._ , 2022], RT-2-X [Brohan _et al._ , 2023], Octo [Octo Model Team _et al._ , 2024], OpenVLA [Kim _et al._ , 2024], and our backbone CogACT [Li _et al._ , 2024a] in full precision, which serve as dense upper bounds on task success. 

**Implementation Details.** All experiments are conducted on a node with NVIDIA RTX 5090 GPUs. We initialize from the CogACT-Base checkpoint [Li _et al._ , 2024a] and train on the Bridge subset of Open X-Embodiment [O’Neill _et al._ , 2023] for 3,000 steps using AdamW with batch size 48 and learning rate 1 _×_ 10<sup>_−_6</sup> . We use an action horizon of _H_ = 15 with 8 diffusion steps. Unless noted otherwise, AC<sup>2</sup> -VLA enables action distillation, sets the maximum token pruning ratio to 0.6, and uses a cache reuse threshold of 0.2. 

**Efficiency-Oriented Methods:** We include representative acceleration approaches, including VLA-Cache [Xu _et al._ , 2025] for temporal reuse, EfficientVLA [Yang _et al._ , 2025] for static pruning, MoLe-VLA [Zhang _et al._ , 2025] for conditional layer skipping via mixture-of-layers routing, and FastV [Chen _et al._ , 2024] as a lightweight pruning baseline. These comparisons characterize the trade-off between compute efficiency, measured by FLOPs and latency, and manipulation success across diverse tasks. 

**Benchmarks.** We evaluate on SIMPLER [Li _et al._ , 2024b], a high-fidelity simulation benchmark for robotic manipulation 

|**WidowX Robot**|**Method**||**Succ**|**ess Rate (**_↑_**)**|||
|---|---|---|---|---|---|---|
|||**Put Spoon on Towel**|**Put Carrot on Plate**|**Stack Cube**|**Put Eggplant in Basket**|**Average**|
||RT-1-X|0.0%|4.2%|0.0%|0.0%|1.1%|
||Octo-Base|15.8%|12.5%|0.0%|41.7%|17.5%|
|SIMPLER|Octo-Small|41.7%|8.2%|0.0%|56.7%|26.7%|
|Visual Matching|OpenVLA|4.2%|0.0%|0.0%|12.5%|4.2%|
||CogACT|71.7%|50.8%|15.0%|67.5%|51.3%|
||**AC**<sup>2</sup>**-VLA**|**71.2%**|**58.0%**|**14.8%**|**74.0%**|**54.5%**|


Table 2: WidowX Visual Matching success rates on SIMPLER. Most baseline results are reported by CogACT, and we add the AC<sup>2</sup> -VLA row by evaluating our method under the same protocol. 

|**Setting**|**Method**||**S**|**uccess Rate**|**(**_↑_**)**||**Speed-up (**_↑_**)**|**FLOPs (**_↓_**)**|
|---|---|---|---|---|---|---|---|---|
|||**PickCan**|**MoveNear**|**Drawer**|**DrawerApple**|**Average**|||
||CogACT|91.3%|85.0%|71.8%|50.9%|74.8%|1.00_×_|100.0%|
||VLA-Cache|92.0%|83.3%|70.5%|51.6%|74.4%|1.36_×_|80.1%|
|Visual|EfficientVLA|95.3%|83.3%|70.3%|56.5%|76.4%|1.59_×_|45.1%|
|Matching|FastV|92.6%|81.4%|69.8%|52.4%|74.1%|1.21_×_|42.0%|
||MoLe-VLA|86.4%|80.2%|70.6%|50.4%|71.9%|1.53_×_|47.4%|
||**AC**<sup>2</sup>**-VLA**|**97.2%**|**82.7%**|**80.6%**|**46.8%**|**76.8%**|**1.79**_×_|**29.4%**|
||CogACT|89.6%|80.8%|28.3%|46.6%|61.3%|1.00_×_|100.0%|
||VLA-Cache|91.7%|79.3%|32.5%|45.8%|62.3%|1.37_×_|82.6%|
|Variant|EfficientVLA|94.8%|77.6%|28.4%|51.9%|63.2%|1.57_×_|45.1%|
|Aggregation|FastV|91.4%|78.6%|27.6%|50.6%|62.1%|1.19_×_|42.0%|
||MoLe-VLA|89.2%|79.5%|29.9%|46.2%|61.2%|1.49_×_|46.3%|
||**AC**<sup>2</sup>**-VLA**|**88.7%**|**84.4%**|**28.2%**|**45.1%**|**61.6%**|**1.67**_×_|**34.7%**|


Table 3: Comparison with efficiency-oriented VLA methods on SIMPLER across two settings. 

### **4.2 Comparison with State-of-the-Art** 

We compare AC<sup>2</sup> -VLA on SIMPLER, reporting task success in Tables 1 and 2 and the speed–accuracy trade-off in Table 3. **Task Performance.** AC<sup>2</sup> -VLA achieves strong control performance across evaluation protocols. On Google Robot Visual Matching, it reaches 76.8% average success, outperforming the dense CogACT baseline at 74.8% and larger models such as RT-2-X at 46.3%. Gains are most pronounced on precision-critical tasks, e.g., Drawer Opening improves from 71.8% to 80.6%, suggesting that action-prior-guided sparsification helps suppress distractors and stabilizes decision making. On Variant Aggregation, AC<sup>2</sup> -VLA matches the fullprecision baseline with 61.6% versus 61.3%, while consistently surpassing RT-1 and OpenVLA. 

**Efficiency and Computational Cost.** AC<sup>2</sup> -VLA substantially reduces the inference cost of CogACT. As shown in Table 3, it uses 29.4% of the original FLOPs, yielding a 1.79 _×_ wall-clock speedup. Notably, this acceleration does not compromise performance and even improves success over dense CogACT, indicating that the removed computation largely corresponds to redundant or distracting features for closedloop control. 

### **4.3 Ablation Study** 

We ablate AC<sup>2</sup> -VLA on SIMPLER Google Robot Visual Matching to validate key design choices. We focus on the three efficiency axes controlled by the router, namely token 


Figure 3: Adaptive layer execution and cache reuse over time. 

pruning, layer skipping, and cognition reuse, and analyze their interaction under comparable budgets. Ablation results are summarized in Table 4. We observe that each component provides complementary benefits, and the full model achieves the best speed-accuracy trade-off when all three axes are jointly enabled: 

- **Cache reuse.** Without cognition reuse, success drops to 70.5% and speedup decreases to 1.66 _×_ , suggesting that temporal reuse improves both efficiency and closed-loop stability. Fig. 3 illustrates adaptive layer execution and cache hit behavior over time. 

- **Token pruning.** Removing token pruning reduces speedup to 1.52 _×_ , showing that spatial sparsification contributes most to acceleration. Fig. 4 visualizes the token-level routing patterns. 


Figure 4: Left: input observation. Right: visualization of token-level importance predicted by the action-conditioned router, highlighting regions relevant to the current manipulation stage while suppressing distractors. The highlighted regions adapt with the action context, focusing computation on interaction-critical areas. 


Figure 5: Pareto frontier for token pruning and layer skipping on the SIMPLER benchmark. 

- **Layer routing.** Disabling layer routing drops the success rate to 67.4% under similar FLOPs, indicating that conditional depth execution helps retain high-level reasoning while reducing compute. 

- **Full model.** AC<sup>2</sup> -VLA attains 76.8% success while delivering a 1.79 _×_ speedup, demonstrating the effectiveness of jointly leveraging spatial, depth-wise, and temporal redundancies. 

### **4.4 More Exploration** 

Beyond component ablations, we further analyze the hyperparameter space and emergent behaviors of AC<sup>2</sup> -VLA, focusing on the joint sparsity trade-off and the effect of cognition caching on closed-loop stability. 

**Token-layer sparsity and the efficiency-accuracy tradeoff.** We perform a grid search over the token keep ratio _rtopk_ and the executed layer count _Nlay_ , as shown in Fig. 5. The results exhibit a clear Pareto frontier, where _rtopk_ = 0 _._ 4 and _Nlay_ = 28 achieves the best trade-off, reaching 1.79 _×_ speedup with 76.8% success. This suggests that many visual tokens are dispensable, while sufficient depth remains important for reasoning over the retained tokens. 

**When cache reuse improves robustness beyond speed.** Interestingly, cache reuse can improve robustness in addition to reducing compute. As shown in Table 5, setting the cache threshold to _τcache_ = 0 _._ 2 yields 87.1% success, outperform- 

|**Configuration**|**Success Rate (**_↑_|**) Speed-up (**_↑_**)**|**FLOPs (**_↓_**)**|
|---|---|---|---|
|Dense baseline<br>|74.8%|1.00_×_|100.0%|
|Full AC<sup>2</sup>-VLA|76.8%|1.79_×_|29.4%|
|No cache reuse,_τcache_ = 1_._0|70.5%|1.66_×_|38.6%|
|Without layer routing|67.4%|1.68_×_|29.4%|
|Without token pruning|72.7%|1.52_×_|66.8%|


Table 4: Component ablation on SIMPLER Google Robot Visual Matching. Speed-up is measured relative to the dense baseline. 

|**Sweep**|**Value Success Rate (**_↑_**) **|**Speed-up (**_↑_**)**|**FLOPs (**_↓_**)**|
|---|---|---|---|
||0.2<br>33.3%|1.69_×_|25.8%|
||0.3<br>56.1%|1.66_×_|34.7%|
|Tk k ti|0.4<br>68.9%|1.63_×_|44.1%|
|oen eep rao_rtopk_|0.6<br>78.8%|1.47_×_|62.5%|
||0.8<br>81.1%|1.26_×_|81.0%|
||22<br>69.7%|1.51_×_|68.8%|
||24<br>73.5%|1.46_×_|75.0%|
|Kt l_N_|26<br>78.0%|1.41_×_|81.2%|
|ep ayers _lay_|28<br>77.3%|1.37_×_|87.5%|
||30<br>80.3%|1.33_×_|93.8%|
||0.00<br>82.6%|1.53_×_|64.8%|
||0.05<br>81.1%|1.52_×_|65.8%|
|Ch thhld|0.10<br>77.3%|1.54_×_|63.4%|
|ace reso_τcache_|0.20<br>87.1%|1.53_×_|63.4%|
||0.30<br>78.8%|1.51_×_|66.3%|
||0.40<br>79.5%|1.52_×_|64.9%|


Table 5: Sensitivity sweeps on SIMPLER Google Robot Visual Matching, varying one efficiency component at a time with the other two disabled. 

ing the dense baseline by +12.3%. We attribute this gain to improved temporal consistency: standard per-frame inference can amplify high-frequency visual noise and induce action jitter, whereas reusing **z** _t_ when the action context is stable effectively smooths decision making and stabilizes control. 

**Sensitivity to key hyper-parameters.** We next vary the token keep ratio and the maximum executed depth to examine how accuracy degrades under more aggressive sparsification. 

- **Token sparsity.** Performance remains stable down to _rtopk_ = 0 _._ 4, but collapses at _rtopk_ = 0 _._ 2 with 33.3% success, indicating a minimum visual information requirement for manipulation. 

- **Depth.** The policy remains competitive with _Nlay_ = 28 at 77.3% success, while reducing below 24 layers causes a sharp drop, suggesting that sufficient depth is critical for complex tasks. 

## **5 Conclusion** 

We present AC<sup>2</sup> -VLA, an action-context-aware framework for efficient Vision-Language-Action inference. By introducing a unified router that allocates computation across spatial, depth, and temporal dimensions based on the robot’s manipulation state, AC<sup>2</sup> -VLA addresses the limitations of efficiency methods driven solely by visual complexity and enables adaptive closed-loop control. Experiments on the SIMPLER benchmark demonstrate a superior efficiency–accuracy trade-off, achieving a 1.79 _×_ speedup and reducing FLOPs to 29.4% of the dense baseline while improving task success. 

These results indicate that action-guided sparsification acts as both an efficiency mechanism and a regularizer, suppressing visual distractors and promoting temporal consistency. Overall, AC<sup>2</sup> -VLA suggests that aligning computation with action is a more effective paradigm for embodied intelligence than static compression, and points toward adaptive inference as a key ingredient for scalable generalist robot policies. 

## **References** 

- [Black _et al._ , 2024] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [Black _et al._ , 2025] Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian LiBell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. In Joseph Lim, Shuran Song, and Hae-Won Park, editors, _Proceedings of The 9th Conference on Robot Learning_ , volume 305 of _Proceedings of Machine Learning Research_ , pages 17–40. PMLR, 27–30 Sep 2025. 

- [Brohan _et al._ , 2022] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Tomas Jackson, Sally Jesmonth, Nikhil J. Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, KuangHuei Lee, Sergey Levine, Yao Lu, Utsav Malla, Deeksha Manjunath, Igor Mordatch, Ofir Nachum, Carolina Parada, Jodilyn Peralta, Emily Perez, Karl Pertsch, Jornell Quiambao, Kanishka Rao, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Kevin Sayed, Jaspiar Singh, Sumedh Sontakke, Austin Stone, Clayton Tan, Huong Tran, Vincent Vanhoucke, Steve Vega, Quan Vuong, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- [Brohan _et al._ , 2023] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, Pete Florence, Chuyuan Fu, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Kehang Han, Karol Hausman, Alexander Herzog, Jasmine Hsu, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Dmitry 

Kalashnikov, Yuheng Kuang, Isabel Leal, Lisa Lee, Tsang-Wei Edward Lee, Sergey Levine, Yao Lu, Henryk Michalewski, Igor Mordatch, Karl Pertsch, Kanishka Rao, Krista Reymann, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Pierre Sermanet, Jaspiar Singh, Anikait Singh, Radu Soricut, Huong Tran, Vincent Vanhoucke, Quan Vuong, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Jialin Wu, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 

- [Chen _et al._ , 2024] Liang Chen, Haozhe Zhao, Tianyu Liu, Shuai Bai, Junyang Lin, Chang Zhou, and Baobao Chang. An image is worth 1/2 tokens after layer 2: Plug-and-play inference acceleration for large vision-language models. _arXiv preprint arXiv:2403.06764_ , 2024. 

- [Fang _et al._ , 2025] Hengyu Fang, Yijiang Liu, Yuan Du, Li Du, and Huanrui Yang. Sqap-vla: A synergistic quantization-aware pruning framework for highperformance vision-language-action models. _arXiv preprint arXiv:2509.09090_ , 2025. 

- [Jiang _et al._ , 2025] Titong Jiang, Xuefeng Jiang, Yuan Ma, Xin Wen, Bailin Li, Kun Zhan, Peng Jia, Yahui Liu, Sheng Sun, and Xianpeng Lang. The better you learn, the smarter you prune: Towards efficient vision-languageaction models via differentiable token pruning. _arXiv preprint arXiv:2509.12594_ , 2025. 

- [Kim _et al._ , 2024] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source visionlanguage-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [Li _et al._ , 2024a] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, Xiaofan Wang, Bei Liu, Jianlong Fu, Jianmin Bao, Dong Chen, Yuanchun Shi, Jiaolong Yang, and Baining Guo. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 

- [Li _et al._ , 2024b] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, Sergey Levine, Jiajun Wu, Chelsea Finn, Hao Su, Quan Vuong, and Ted Xiao. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 

- [Li _et al._ , 2025a] Wei Li, Renshan Zhang, Rui Shao, Jie He, and Liqiang Nie. CogVLA: Cognition-aligned visionlanguage-action model via instruction-driven routing & sparsification. _arXiv preprint arXiv:2508.21046_ , 2025. 

- [Li _et al._ , 2025b] Ye Li, Yuan Meng, Zewen Sun, Kangye Ji, Chen Tang, Jiajun Fan, Xinzhu Ma, Shutao Xia, Zhi 

Wang, and Wenwu Zhu. SP-VLA: A joint model scheduling and token pruning approach for VLA model acceleration. _arXiv preprint arXiv:2506.12723_ , 2025. 

- [Lin _et al._ , 2025] Juyi Lin, Amir Taherin, Arash Akbari, Arman Akbari, Lei Lu, Guangyu Chen, Taskin Padir, Xiaomeng Yang, Weiwei Chen, Yiqian Li, Xue Lin, David Kaeli, Pu Zhao, and Yanzhi Wang. VOTE: Visionlanguage-action optimization with trajectory ensemble voting. _arXiv preprint arXiv:2507.05116_ , 2025. 

   - [Zhang _et al._ , 2025] Rongyu Zhang, Menghang Dong, Yuan Zhang, Liang Heng, Xiaowei Chi, Gaole Dai, Li Du, Yuan Du, and Shanghang Zhang. Mole-vla: Dynamic layer-skipping vision language action model via mixtureof-layers for efficient robot manipulation. _arXiv preprint arXiv:2503.20384_ , 2025. 

- [Octo Model Team _et al._ , 2024] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- [O’Neill _et al._ , 2023] Abby O’Neill, Abdul Rehman, Abhinav Gupta, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, and et al. Open x-embodiment: Robotic learning datasets and RT-X models. _arXiv preprint arXiv:2310.08864_ , 2023. 

- [Reuss _et al._ , 2025] Moritz Reuss, Hongyi Zhou, Marcel R¨uhle, Omer<sup>¨</sup> Erdinc¸ Ya˘gmurlu, Fabian Otto, and Rudolf Lioutikov. FLOWER: Democratizing generalist robot policies with efficient vision-language-action flow policies. _arXiv preprint arXiv:2509.04996_ , 2025. 

- [Shukor _et al._ , 2025] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, Simon Alibert, Matthieu Cord, Thomas Wolf, and R´emi Cad`ene. SmolVLA: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

- [Tan _et al._ , 2025] Xudong Tan, Yaoxin Yang, Peng Ye, Jialin Zheng, Bizhe Bai, Xinyi Wang, Jia Hao, and Tao Chen. Think twice, act once: Token-aware compression and action reuse for efficient inference in Vision-LanguageAction models. _arXiv preprint arXiv:2505.21200_ , 2025. 

- [Wen _et al._ , 2024] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, Yaxin Peng, Feifei Feng, and Jian Tang. TinyVLA: Towards fast, data-efficient Vision-LanguageAction models for robotic manipulation. _arXiv preprint arXiv:2409.12514_ , 2024. 

- [Xu _et al._ , 2025] Siyu Xu, Yunke Wang, Chenghao Xia, Dihao Zhu, Tao Huang, and Chang Xu. Vla-cache: Efficient vision-language-action manipulation via adaptive token caching. _arXiv preprint arXiv:2502.02175_ , 2025. 

- [Yang _et al._ , 2025] Yantai Yang, Yuhao Wang, Zichen Wen, Luo Zhongwei, Chang Zou, Zhipeng Zhang, Chuan Wen, and Linfeng Zhang. Efficientvla: Training-free acceleration and compression for vision-language-action models. _arXiv preprint arXiv:2506.10100_ , 2025. 

