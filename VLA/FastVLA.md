---
title: "FastVLA: Task-Conditioned and Temporally Adaptive Visual Token Compression for Efficient Vision-Language-Action Models"
date: "2026-10-15"
authors: "Jiuyi Xu; Chengyuan Qian; Zhengzhong Tu; Yang Sui; Yangming Shi"
url: https://arxiv.org/abs/2610.22146
pdf: https://arxiv.org/pdf/2610.22146
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2610.22146)** / [論文ページ](https://arxiv.org/abs/2610.22146)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **FastVLA: Task-Conditioned and Temporally Adaptive Visual Token Compression for Efficient Vision-Language-Action Models** 

Jiuyi Xu Chengyuan Qian Zhengzhong Tu Colorado School of Mines Texas A&M University Texas A&M University 

Yang Sui Yangming Shi Microsoft AI Colorado School of Mines 

## **Abstract** 

_Vision-Language-Action (VLA) models present a promising paradigm for general-purpose robot manipulation, but closed-loop deployment is often limited by inference efficiency: at each timestep, high-resolution, often multi-view images are encoded into hundreds of visual tokens that dominate transformer computation and latency. Token compression via attention is a natural solution but is challenging for VLA control because (1) decision-critical tokens are determined by the task, not generic visual saliency, and (2) the token budget varies substantially across steps, so static metrics and budgets waste computation or discard control-critical tokens. We introduce FastVLA, a trainingfree, task-aware, and temporally adaptive visual token compression framework. At each step, FastVLA scores token importance via task-to-vision attention and adaptively sets the compression rate from the importance-distribution uniformity, measured by an inverse-Simpson metric with online sliding-window calibration. We evaluate FastVLA on OpenVLA, OpenVLA-OFT, and CogACT across LIBERO and SIMPLER, and on a physical Franka Research 3 robot. In simulation, it reduces LLM-backbone FLOPs by 35-59% and action latency by 9-32% (a 1.09×-1.46× speedup) while maintaining task success, achieving a comparable or better efficiency-performance trade-off than existing plugand-play token compression/pruning/reuse baselines. On the real robot, it cuts action-prediction latency by 20% (1.25× speedup) at comparable success. Code is available at https://github.com/jiuyixu25/FastVLA._ 

## **1. Introduction** 

Vision-Language-Action (VLA) models have recently emerged as a compelling paradigm for general-purpose 

robot manipulation, enabling policies to predict low-level actions conditioned on natural-language tasks and visual observations [4, 7, 11, 15, 30]. By leveraging large-scale pretraining and large vision-language backbones, VLAs demonstrate strong generalization across objects, scenes, and task specifications, making them increasingly attractive for deployment in versatile manipulation systems. Despite their impressive capabilities, deploying these models in closed-loop control is often limited by inference efficiency [9]. At every control step, high-resolution (e.g., 224 _×_ 224) and frequently multi-view observations are encoded into hundreds of visual tokens [3, 16] that dominate the compute and latency of the vision-language-model (VLM) backbone during action prediction, far outweighing the few text tokens of a short task. 

Yet not all visual tokens contribute equally to action prediction. In a typical manipulation step, only a small subset of tokens carries decision-critical information (e.g., the target object/place or the gripper–object contact region), while the rest are redundant or even distracting [12, 26, 27]. Reducing the number of visual tokens processed by the largelanguage-model (LLM) backbone, without sacrificing task performance, has therefore become a key direction for accelerating VLA inference [22, 23, 25]. 

However, directly applying VLM-specific token compression methods [5, 8, 29] to robotic control is often suboptimal, because these methods are designed for single-shot vision-language understanding, where the objective is to preserve global semantic content for perception tasks such as detection, captioning, or generation. Unlike image-based VLMs that process a single image, or video-based VLMs that encode a fixed sequence of frames, a VLA interacts with the environment through actions that directly shape its subsequent observations: at each step the agent receives a new observation conditioned on its previous action and predicts the next one. Visual tokens are thus not repre- 

1 

sentations of a static scene but components of a _sequential decision process_ , which sets token compression for VLA apart from its VLM counterpart in two respects. The first is that token relevance is governed by the task rather than by generic visual saliency (now standard practice in languageguided pruning), which we adopt as our importance signal rather than claim as a contribution. The second, and the focus of this work, is that the _amount_ of decision-critical visual information varies drastically across control steps: some steps (e.g., target localization) rely on broad scene context, whereas others (e.g., grasping or contact) depend on a small, localized region. A single fixed compression rate is therefore inherently mismatched, wasting computation when the useful information is concentrated, and discarding necessary context when broader information is required. 

Motivated by this, we propose **FastVLA, a trainingfree visual token compression framework for efficient VLA inference whose core is a temporally adaptive, perstep compression rate** . At each step, FastVLA scores visual-token importance with task-to-vision attention which is a training-free signal that a controlled comparison shows is more reliable for action prediction than vision-to-vision or all-to-vision attention and then, crucially, decides _how many_ tokens to keep from the shape of the resulting importance distribution. Specifically, it estimates the effective number of tokens the decision depends on via an inverse-Simpson uniformity measure, and maps this quantity through an online sliding-window calibration to a timestep-dependent compression rate: when the current step concentrates on few tokens relative to its recent history it prunes aggressively, and when the decision draws on broader context it prunes conservatively. By allocating the token budget where each decision needs it, FastVLA reduces LLM-backbone computation, speeds up action prediction, and improves closed-loop responsiveness, without caches or training. 

We evaluate FastVLA on three open-source VLA models including OpenVLA [15], OpenVLA-OFT [16], and CogACT [17], across the widely used LIBERO [19] and SIMPLER [18] benchmarks, and on a physical Franka Research 3 robot. In simulation, FastVLA reduces LLM-backbone FLOPs by 35-59% and action latency by 9-32% (up to a 1 _._ 46 _×_ speedup) while maintaining task success, yielding a comparable or even better efficiency-performance trade-off than existing training-free compression, pruning, and reuse baselines. On the real robot, it cuts action-prediction latency by 20% (1 _._ 25 _×_ speedup) and raises the control frequency by up to 25% at comparable success. In summary, our contributions are: 

- We propose FastVLA, a training-free, plug-and-play visual token compression framework that accelerates closed-loop VLA inference. 

- We design a step-adaptive compression policy that sets a timestep-dependent token budget from the inverseSimpson uniformity of the importance distribution under online sliding-window calibration. 

- We validate FastVLA on OpenVLA/OpenVLA-OFT (LIBERO), CogACT (SIMPLER), and a physical Franka Research 3 robot, achieving substantial compute and latency reductions in simulation and a 1 _._ 25 _×_ real-robot speedup with comparable task success. 

## **2. Related Work** 

### **2.1. Vision-Language-Action Models for Robot Manipulation** 

VLA models predict robot actions directly from naturallanguage tasks and visual observations. Early work such as SayCan [1] combines language-conditioned planning with learned low-level skills, while RT-1 [6] and RT-2 [30] scale language-conditioned visuomotor learning with large robot datasets and web-scale vision-language pretraining. In parallel, PaLM-E [10] and Octo [21] highlight the benefits of large pretrained representations across tasks and embodiments. More recently, foundation VLA models including OpenVLA [15] and OpenVLA-OFT [16], CogACT [17], and _π_ 0 [4] / _π_ 0 _._ 5 [3] demonstrate strong robustness and open-world generalization via heterogeneous multi-robot data and transformer backbones. These billion-scale models encode high-resolution, often multi-view observations into long visual-token sequences at every control step, which motivates inference-time methods that remove redundant visual tokens while preserving task-critical information. 

### **2.2. Visual Token Compression for Efficient VLA Inference** 

Because most VLA models [3, 4, 15–17] adopt VLMstyle architectures, training-free token compressors built for VLMs are broadly applicable: they prune or merge visual tokens by token similarity (ToMe [5]), shallow-layer or cross-modal attention (FastV [8], SparseVLM [29], VisPruner [28]), or token diversity (DivPrune [2]). However, these methods are designed for single-image inference and apply a static pruning policy, so transferring them directly to VLA often degrades control performance. 

Recent work therefore targets VLA inference along three lines: reuse- and cache-based methods that exploit cross-step temporal redundancy (VLA-Cache [26], FlashVLA [23]); importance-estimation methods that add task-, phase-, or motion-aware cues (SpecPrune-VLA [25], ADP [22], VLA-Pruner [20]); and hybrid or learned schemes that go beyond pruning (EfficientVLA [27], LightVLA [12]). 

These methods still share limitations that FastVLA overcomes. Reuse and caching introduce cross-step state and 

2 


Figure 1. Overview of FastVLA. At each action-prediction step, FastVLA scores visual tokens with task-conditioned attention, measures the uniformity of the top-scoring importance distribution, and sets the step’s compression rate through an online sliding-window calibration, reducing LLM-backbone computation while preserving action performance. 

cache-management overhead, so wall-clock gains can lag FLOP reductions; learned schemes such as LightVLA require training and are tied to a specific backbone, although at equal success they can reach a better compute–latency point than training-free methods. In addition, some VLM/VLA compression algorithms commit to a fixed compression ratio, adapting (if at all) only through auxiliary external signals such as end-effector motion. FastVLA differs on three axes: it is training-free, pruning independently at each step without caches; it conditions token importance on the language task; and, crucially, it makes the compression rate itself adaptive, reading the per-step concentration of task-relevant evidence via an inverse-Simpson uniformity signal calibrated against a short temporal window, spending tokens where the decision needs them and pruning harder where it does not. 

## **3. Method** 

We propose FastVLA, a temporally adaptive and trainingfree visual token compression method that reduces the number of visual tokens processed by the VLA model’s LLM backbone (Fig. 1). FastVLA proceeds in two stages: it first scores visual-token importance with a task-conditioned attention signal, and then, as our core contribution, sets _how many_ tokens to keep adaptively at each step from the concentration of that importance distribution. We present both stages below. 

### **3.1. Preliminary: Visual Token Compression in VLA Models** 

Methods that reduce the visual-token cost of a VLA backbone fall into three largely orthogonal families: _token pruning_ discards a subset of visual tokens, shortening the sequence seen by later layers; _token merging_ pools similar tokens into fewer representatives; and _reuse/caching_ 

recomputes only the tokens that changed across control steps, reusing cached token or key-value states for the rest. FastVLA belongs to the pruning family: at every action step it performs a hard, task-conditioned top- _K_ selection of visual tokens, with the retained budget set adaptively per step. 

### **3.2. Task-conditioned visual token importance** 

A VLA policy is explicitly conditioned on the language task, so visual-token usage is driven by the task prompt rather than by generic visual saliency: the tokens that matter are those covering the target object/place and the interaction region named by the task. The design question is therefore _which_ attention signal best captures this task-driven importance. Since selecting tokens by attention is already standard in VLM compression, we do not propose it as new but instead re-evaluate three candidate signals for VLA control: _all-to-vision_ (naive cross-modal attention from the fused representation to visual tokens), _task-to-vision_ (task tokens attending to visual tokens), and _vision-to-vision_ (visual selfattention capturing perceptual saliency). 

We progressively pruned visual tokens by each score and measured policy performance on LIBERO with OpenVLAOFT (Fig. 2). Task-to-vision scoring was clearly the most robust: it retained near-saturated success under lightto-moderate compression (10%–50%) and preserved nontrivial performance even under aggressive compression ( _≥_ 70%), whereas vision-to-vision and all-to-vision degraded much faster and approached failure at 90%. We therefore adopt task-to-vision attention as the importance signal in the remainder of the method. 

Formally, let **T** _∈_ R<sup>_M×d_</sup> and **V** _∈_ R<sup>_N×d_</sup> denote the task- and visual-token representations. Following scaled dot-product attention [24], we apply RMSNorm to obtain **T** ˜ and **V** ˜ , compute affinities **S** = **T** ˜ **V** ˜<sup>T</sup> _/_ _~~√~~ d ∈_ R<sup>_M×N_</sup> , and apply a _softmax_ over visual tokens to obtain attention weights **A** . Averaging over a subset of task tokens _Q_ gives 

3 


Figure 2. Average success rate on LIBERO under increasing visual token pruning rates for the three attention-based importance signals. 


Figure 3. Visual token importance distributions across action steps in a single trial on the LIBERO-Long benchmark. 

a per-token importance score: 


so that visual tokens consistently attended by the task context receive higher importance. 

### **3.3. Adaptive Step-aware Compression Rate** 

Having fixed _which_ tokens matter, the central question of our method is _how many_ to keep at each step. In a closedloop rollout, successive steps rely on visual information to very different extents. For example, approaching or grasping an object depends on a small localized region, whereas locating a target or verifying the scene requires broad context. Fig. 3 makes this concrete: within a single trial, the per-step importance distribution swings between nearly uniform (many tokens contribute comparably) and highly concentrated (a few tokens dominate). A fixed compression rate therefore wastes computation on concentrated steps and discards needed context on broad ones; the rate should instead adapt to this per-step concentration. 

We implement this in two steps: measure how concentrated the importance distribution is, then map that concen- 


Figure 4. Shannon entropy and inverse Simpson over the action steps of a single LIBERO-Long trial. 

tration to a per-step rate. To measure it, a natural choice is Shannon entropy, but with hundreds of visual tokens and a long tail of near-zero scores, normalized entropy varies only within a narrow band and is insensitive to concentration among the dominant tokens (Fig. 4), making it hard to map to distinct compression rates. 

**Inverse Simpson uniformity.** We instead adopt the second-order effective-number measure (inverse Simpson) [13, 14], which emphasizes squared weights and thus down-weights the long tail while reporting the _effective number_ of dominant tokens which is a better fit for the sparse, heavy-tailed importance distributions of VLA models, and one with a substantially larger dynamic range across steps. Over the top- _K_ tokens we compute: 


where _U_<sup>(</sup><sup>_t_)</sup> _∈_ (0 _,_ 1]: small values indicate concentrated attention (few tokens dominate), large values a more uniform distribution. Here _K_ = _⌈_ (1 _−_ ( _ρ_ + _τ_ )) _N ⌉_ is the smallest budget the band can request; since _K_ is fixed within a run and _U_<sup>(</sup><sup>_t_)</sup> enters the decision only through the calibration below, which is invariant to constant rescaling, this normalization cannot conflate concentration with budget. 

**Online step-adaptive rate.** Thresholding _U_<sup>(</sup><sup>_t_)</sup> against an absolute scale would require anchors that do not transfer: the range of _U_<sup>(</sup><sup>_t_)</sup> drifts across suites and backbones, so anchors fit on one setting misallocate the budget on another. We therefore calibrate _U_<sup>(</sup><sup>_t_)</sup> against its own recent temporal context through a sliding window _W_<sup>(</sup><sup>_t_)</sup> = _{U_<sup>(</sup><sup>_t−T_)</sup> _, . . . , U_<sup>(</sup><sup>_t−_1)</sup> _}_ of length _T_ . Letting _U_ min<sup>(</sup><sup>_t_)and</sup><sup>_U_</sup> max<sup>(</sup><sup>_t_)</sup> be the window extremes, the relative position 


locates the current step within the ongoing execution: a 

4 

#### **Algorithm 1** FastVLA 

**Input:** Current timestep _t_ , task tokens **T**<sup>(</sup><sup>_t_)</sup> _∈_ R<sup>_M×d_</sup> , visual tokens **V**<sup>(</sup><sup>_t_)</sup> _∈_ R<sup>_N×d_</sup> , sliding window (queue) _W_ with max length _T_ **Hyperparameters:** Target compression rate _ρ_ , deviation factor _τ_ 

1: _// Step 1: Attention-based Token Importance Score_ 2: **T**<sup>˜</sup> _←_ RMSNORM( **T**<sup>(</sup><sup>_t_)</sup> ), **V**<sup>˜</sup> _←_ RMSNORM( **V**<sup>(</sup><sup>_t_)</sup> ) 3: **s** _←_ MEAN SOFTMAX <u>1</u> � � _~~√~~ d_<sup>**T**˜</sup><sup>**V**˜</sup><sup>_⊤_��</sup> 4: _// Step 2: Inverse Simpson-based Uniformity_ 5: **v** _←_ TOPK( **s** _, ⌈_ (1 _−_ ( _ρ_ + _τ_ )) _N ⌉_ ) 6: **q** _←_ **v** _/_<sup>�</sup> _j_<sup>_vj_;</sup><sup>_U_(</sup><sup>_t_)</sup><sup>_←_</sup> _⌈_ (1 _−_ ( _ρ_ + _τ_ ))1 _N ⌉_<sup><u>�</u></sup> _j_<sup>_q_</sup> _j_<sup>2</sup> 7: _// Step 3: Online Mapping based on Sliding Window_ 8: **if** _t <_ 2 **then** // _Initialize U_ min _and U_ max 9: _ρ_<sup>(</sup><sup>_t_)</sup> _← ρ − τ_ 10: **else** 11: _U_ min _←_ MIN( _W_ ), _U_ max _←_ MAX( _W_ ) _<u>U</u>_<sup>(</sup><sup>_t_)</sup> _−U_ <u>min</u> 12: _α_<sup>(</sup><sup>_t_)</sup> _←_ CLIP� _U_ max _−U_ min<sup>_,_0</sup><sup>_,_1</sup> � 13: _ρ_<sup>(</sup><sup>_t_)</sup> _←_ PROJECT( _α_<sup>(</sup><sup>_t_)</sup> ; [ _ρ − τ, ρ_ + _τ_ ]) 14: **end if** 15: _W ←_ PUSHPOP( _W, U_<sup>(</sup><sup>_t_)</sup> _, T_ ) 16: **Return:** _ρ_<sup>(</sup><sup>_t_)</sup> 

small _α_<sup>(</sup><sup>_t_)</sup> (more concentrated than the recent past) warrants aggressive pruning, a large _α_<sup>(</sup><sup>_t_)</sup> (more uniform) warrants caution. We then map it to a per-step rate via a bounded linear projection centered at a target rate _ρ_ : 


so the rate adapts within [ _ρ − τ, ρ_ + _τ_ ], where _ρ_ sets the average compression (e.g., 50%) and the deviation factor _τ_ bounds the per-step deviation (e.g., _±_ 10%). Algorithm 1 summarizes the full per-step procedure. 

**Implementation details.** Scores are computed on the LLM backbone’s input embeddings with a parameter-free RMSNorm. _Q_ contains every token after the visual span (the prompt with the task), skipping all-zero placeholder embeddings such as OpenVLA-OFT’s action slots. _W_ is cleared at the start of every episode. The first two steps use the conservative rate _ρ − τ_ because _W_ cannot yet provide a range, and a degenerate window ( _U_ max = _U_ min) falls back to _ρ_ . Since _α_<sup>(</sup><sup>_t_)</sup> is clipped, a step more concentrated (more uniform) than every step in _W_ saturates at _ρ_ + _τ_ ( _ρ − τ_ ). Each step keeps the round((1 _−ρ_<sup>(</sup><sup>_t_)</sup> ) _N_ ) top-scoring visual tokens in their original order. 

## **4. Experiments** 

To evaluate the effectiveness of FastVLA, we conduct experiments in both simulation and real-world environments. We implement FastVLA on three open-source 

VLA models: OpenVLA [15], OpenVLA-OFT [16], and CogACT-base [17]. Specifically, we evaluate OpenVLA and OpenVLA-OFT on the LIBERO benchmark [19] and CogACT-base on the SIMPLER benchmark [18], and additionally validate FastVLA on a physical Franka Research 3 robot, together covering a diverse set of manipulation tasks. All experiments are conducted on a single NVIDIA RTX 4090 GPU. 

### **4.1. Experiment Setup** 

**Compared Methods.** We compare FastVLA against a broad range of recent acceleration methods spanning three categories: (i) general VLM token-pruning methods, including FastV [8], SparseVLM [29], and DivPrune [2]; (ii) VLA-specific token compression, caching, and reuse methods, including VLA-Cache [26], EfficientVLA [27], FlashVLA [23], SpecPrune-VLA [25], and ADP [22]; and (iii) the learned token-pruning method LightVLA [12]. Among these, VLA-Cache and LightVLA provide published, open-source, and reproducible implementations, which we re-evaluate under our unified setup. For the remaining methods (marked with<sup>_∗_</sup> in Tab. 1), we are unable to reproduce them in our environment and therefore quote their published results for reference only. 

**Evaluation Metrics.** We report success rate, FLOPs, latency, control frequency, and CUDA latency, together with the resulting speedup. FLOPs provides a hardware-agnostic estimate of the theoretical computation of the LLM backbone. Latency denotes the total per-step action-prediction time. Control frequency is the number of environment actions executed per second, _H/_ latency, where _H_ is the number of actions produced by one prediction call ( _H_ =8 for OpenVLA-OFT, which predicts an action chunk per forward pass, and _H_ =1 for OpenVLA and CogACT); it quantifies the real-time responsiveness of closed-loop control and makes chunked and single-step policies comparable on one axis. For chunked policies this is an action throughput computed from latency, not a measured rate: OpenVLAOFT receives a new observation once per chunk, i.e., at most 1 _/_ latency (8 _._ 4 _→_ 12 _._ 3 Hz in Tab. 1). CUDA latency reports the LLM-backbone inference time on the GPU, and speedup is computed as the ratio of the per-backbone baseline latency to that of each method. 

**Choice of** _ρ_ **.** _ρ_ sets FastVLA’s average compute budget and is the only setting chosen per benchmark and backbone; _τ_ =0 _._ 1 and _T_ =10 are shared by all experiments. For each suite (each task on SIMPLER) we report the most aggressive _ρ_ on a 0.05 grid whose success stayed within 2 points of the uncompressed model. 

### **4.2. Evaluation Environments** 

**Simulation Benchmarks.** We evaluate on two large-scale simulation benchmarks for language-conditioned robot ma- 

5 

Table 1. Comparison of different VLA acceleration methods on the LIBERO benchmark. FastVLA uses _ρ_ =0 _._ 8 _/_ 0 _._ 7 _/_ 0 _._ 75 _/_ 0 _._ 6 on OpenVLA-OFT and 0 _._ 35 _/_ 0 _._ 5 _/_ 0 _._ 4 _/_ 0 _._ 3 on OpenVLA (Spatial/Object/Goal/10). FastVLA SR results are averaged over three random seeds and reported as mean _±_ standard error. Methods marked with<sup>_∗_</sup> could not be reproduced in our setup; their success rates and speedups are quoted from SpecPrune-VLA [25] (FastV, DivPrune, SparseVLM, EfficientVLA, SpecPrune-VLA) or the original papers (FlashVLA [23], ADP [22]), with speedups measured on the authors’ hardware, and their FLOPs apply the reported FLOPs ratios to our baseline. 

|Method||Succ|ess Rate (%|)_↑_||FLOPs|Latency|Control Freq.|CUDA Lat.|Speedup|
|---|---|---|---|---|---|---|---|---|---|---|
|||||||(T)_↓_|(ms)_↓_|(Hz)_↑_|(ms)_↓_|_↑_|
||Spatial|Object|Goal|10|Average||||||
|OpenVLA|85.8|88.8|77.4|53.4|76.4|1.86|186.64|5.36|42.28|1.00_×_|
|+ VLA-Cache|86.0|88.0|75.4|54.4|76.0|1.36|203.37|4.92|31.83|0.92_×_|
|+ FlashVLA<sup>_∗_</sup>|82.6|86.6|78.8|46.8|73.7|0.82|-|-|-|1.56_×_|
|**+ FastVLA**|**85.3**_±_**0.1 **|**87.2**_±_**0.2 **|**77.6**_±_**0.2 **|**53.2**_±_**0.4 **|**75.8**_±_**0.2**|**1.20**|**161.53**|**6.19**|**26.91**|**1.16**_×_|
|OpenVLA-OFT|98.2|98.2|97.6|94.0|97.0|3.98|118.52|67.50|65.99|1.00_×_|
|+ FastV<sup>_∗_</sup>|94.6|95.8|94.0|88.8|93.3|2.27|-|-|-|1.44_×_|
|+ DivPrune<sup>_∗_</sup>|92.4|91.2|89.0|84.8|89.4|2.15|-|-|-|1.46_×_|
|+ SparseVLM<sup>_∗_</sup>|96.8|94.2|97.6|93.6|95.6|3.06|-|-|-|1.28_×_|
|+ VLA-Cache|98.2|98.0|97.2|94.8|97.1|3.05|99.83|80.12|62.44|1.19_×_|
|+ EfficientVLA<sup>_∗_</sup>|96.5|91.1|96.0|72.1|88.9|1.39|-|-|-|1.52_×_|
|+ SpecPrune-VLA<sup>_∗_</sup>|97.4|95.8|97.7|93.4|96.1|1.71|-|-|-|1.46_×_|
|+ ADP<sup>_∗_</sup>|99.4|98.0|96.4|91.2|96.3|3.24|-|-|-|1.23_×_|
|+ LightVLA|97.6|98.0|97.4|93.0|96.5|1.21|72.41|110.48|32.67|1.64_×_|
|**+ FastVLA**|**97.8**_±_**0.1 **|**98.0**_±_**0.1 **|**97.0**_±_**0.5 **|**93.1**_±_**0.5 **|**96.5**_±_**0.3**|**1.65**|**81.17**|**98.56**|**40.39**|**1.46**_×_|


nipulation. **LIBERO** comprises four suites (Spatial, Object, Goal, and Long) that test generalization across scene layouts, objects, language-specified goals, and long horizons; we follow the standard protocols of OpenVLA<sup>1</sup> and OpenVLA-OFT<sup>2</sup> . **SIMPLER** , designed to reduce the simto-real gap, provides visual matching and variant aggregation settings; we evaluate on Pick Coke Can, Move Near, Open/Close Drawer, and Put Apple in Drawer, following the protocol of CogACT<sup>3</sup> with CogACT-base as the baseline. 

**Real-World Environment.** We further validate FastVLA on a physical Franka Research 3 robot to examine whether the efficiency gains observed in simulation transfer to real deployment. We consider two tabletop manipulation tasks, _pick_ and _pick and place_ . The policy is OpenVLA-OFT finetuned with LoRA on teleoperated demonstrations and deployed in closed-loop control using the same RTX 4090 inference setup as in simulation. For each task and condition, we run 50 rollouts, alternating between the unmodified baseline and FastVLA. 

### **4.3. Experiment Results** 

**LIBERO.** Tab. 1 reports results on the four LIBERO suites. On OpenVLA, FastVLA cuts LLM FLOPs from 1.86 to 1.20 T ( _−_ 35 _._ 5%) and latency from 186.64 to 161.53 ms 

> 1https://github.com/openvla/openvla 

> 2https://github.com/moojink/openvla-oft 

> 3https://github.com/microsoft/CogACT 

(1 _._ 16 _×_ ) at a cost of 0.6 points of success (76.4 _→_ 75.8%); on OpenVLA-OFT, from 3.98 to 1.65 T ( _−_ 58 _._ 5%) and 118.52 to 81.17 ms (1 _._ 46 _×_ , 67.50 _→_ 98.56 Hz) at a cost of 0.5 points (97.0 _→_ 96.5%). Against prior accelerators the picture is a trade-off rather than dominance. VLA-Cache preserves success best on OpenVLA-OFT (97.1%) but converts far less computation into speed (FastVLA needs 45 _._ 9% fewer FLOPs and 18 _._ 7% lower latency), and its gains are backbone-dependent (0 _._ 92 _×_ on OpenVLA vs. 1 _._ 19 _×_ on OpenVLA-OFT). Against general VLM pruners (FastV, DivPrune, SparseVLM), FastVLA attains the highest success (96.5% vs. 89–96%) at lower FLOPs. LightVLA defines the better efficiency frontier: at equal success it uses 26.7% fewer FLOPs and is 10.8% faster (1.21 vs. 1.65 T; 72.41 vs. 81.17 ms), but must be re-trained per backbone, whereas FastVLA drops into three backbones and a real robot at inference time with a directly controllable budget _ρ_ . 

**SIMPLER.** Tab. 2 reports results with CogACT-base as the baseline. Under Visual Matching, FastVLA cuts LLM FLOPs by 37 _._ 3% and latency by 8 _._ 5% (1 _._ 09 _×_ ; 5 _._ 73 _→_ 6 _._ 27 Hz) with average success essentially unchanged ( _−_ 0 _._ 4 points). Under the more challenging Variant Aggregation setting, it cuts FLOPs by 37 _._ 6%, latency by 10 _._ 2% (1 _._ 11 _×_ ; 5 _._ 72 _→_ 6 _._ 37 Hz) and CUDA latency by 21 _._ 0%, while improving average success by 1 _._ 0 points, indicating that adaptive compression does not compromise robustness under distribution shift and task variation. 

**Real-World.** Tab. 3 reports the real-robot results. On the 

6 


Figure 5. **Qualitative rollouts.** _Top:_ a LIBERO-Long task (simulation); _bottom:_ a real-world pick-and-place task. Each strip shows eight frames sampled uniformly over time from the third-person camera, with the full observation alongside its _FastVLA_ -pruned counterpart. Full rollout videos are in the supplementary material. 

Table 2. Comparison of different VLA acceleration methods on the SIMPLER benchmark. FastVLA SR results are averaged over three random seeds and reported as mean _±_ standard error. For FastVLA we set _ρ_ =0 _._ 7 (PickCan), 0 _._ 5 (MoveNear), and 0 _._ 3 (Drawer, DrawerApple). 

|SIMPLER|Method||Su|ccess Rate (|%)_↑_||FLOPs|Latency|Control Freq.|CUDA Lat.|Speedup|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||PickCan|MoveNear|Drawer|DrawerApple|Average|(T)_↓_|(ms)_↓_|(Hz)_↑_|(ms)_↓_|_↑_|
|Vil Mthi|CogACT-base|93.7|86.7|75.9|53.7|77.5|1.85|174.48|5.73|82.53|1.00_×_|
|sua acng|**+ FastVLA**|**93.7**_±_**2.0**|**85.4**_±_**0.7**|**75.5**_±_**0.9**|**53.6**_±_**0.2**|**77.1**_±_**0.8**|**1.16**|**159.59**|**6.27**|**66.10**|**1.09**_×_|
|Vi Ai|CogACT-base|89.1|76.7|50.8|27.0|60.9|1.81|174.94|5.72|82.74|1.00_×_|
|arant ggregaton|**+ FastVLA**|**89.5**_±_**1.3**|**77.2**_±_**1.0**|**52.4**_±_**0.3**|**28.3**_±_**0.4**|**61.9**_±_**0.6**|**1.13**|**157.06**|**6.37**|**65.34**|**1.11**_×_|


Table 3. Real-world evaluation on a Franka Research 3 robot. 

|Task|Method|Success Rate<br>_↑_|Latency<br>(ms)_↓_|Control Freq.<br>(Hz)_↑_|Speedup<br>_↑_|
|---|---|---|---|---|---|
||OpenVLA-OFT|84.0%|121.13|66.04|1.0_×_|
|Pick|**+ FastVLA**|**80.0%**|**96.90**|**82.56**|**1.25**_×_|
||OpenVLA-OFT|68.0%|120.01|66.67|1.0_×_|
|Pick and place|**+ FastVLA**|**66.0%**|**97.77**|**81.82**|**1.23**_×_|


firm that FastVLA’s efficiency gains transfer to real-world closed-loop manipulation. Fig. 5 visualizes the pruning in simulation and on the real robot: the retained tokens concentrate on task-relevant regions such as the robotic arm and the target objects. 

### **4.4. Ablation Studies** 

_pick_ task, FastVLA reduces action latency from 121.13 to 96.90 ms ( _−_ 20 _._ 0%) and raises the effective control frequency from 66.04 to 82.56 Hz (+25 _._ 0%), while retaining a comparable success rate (84.0% vs. 80.0%). On the more demanding _pick and place_ task, latency drops from 120.01 to 97.77 ms ( _−_ 18 _._ 5%) and control frequency increases from 66.67 to 81.82 Hz (+22 _._ 7%), with the success rate again largely preserved (68.0% vs. 66.0%). These results con- 

**Adaptivity vs. the budget it spends.** Since the step-wise rate lives in a band around _ρ_ , an adaptive run may realize a budget slightly different from its nominal target, and a gain could then reflect lighter compression rather than adaptivity. We therefore log the _realized_ retained-token count and add a compute-matched control: a fixed-rate policy set to the budget the adaptive run actually consumed, _ρ_ fix=1 _− k/N_<sup>¯</sup> (Tab. 4). Realized budgets exceed the nominal target by 

7 

Table 4. Compute-matched comparison of fixed and adaptive token selection across four LIBERO suites. Tokens (and target compression rate) are reported separately for each suite. Results are averaged over three random seeds and reported as mean _±_ standard error. 

|Method|Spa|tial|Obj|ect|Go|al|1|0|
|---|---|---|---|---|---|---|---|---|
||Tokens|SR (%)_↑_|Tokens|SR (%)_↑_|Tokens|SR (%)_↑_|Tokens|SR (%)_↑_|
|Fixed @ nominal|102 (80%)|96.7_±_0.1|154 (70%)|97.0_±_0.2|128 (75%)|95.1_±_0.5|205 (60%)|91.9_±_0.4|
|Fixed, budget-matched|105|96.5_±_0.1|157|97.1_±_0.1|132|95.7_±_0.3|207|92.0_±_0.3|
|Adaptive|104.3|**97.8**_±_**0.1**|156.3|**98.0**_±_**0.1**|131.9|**97.0**_±_**0.5**|206.8|**93.1**_±_**0.5**|


0 _._ 9–3 _._ 0%, which is precisely why the control is needed. Handing the _fixed_ policy that same extra budget is worth at most +0 _._ 6 points (+0 _._ 15 on average), whereas the adaptive policy turns it into +0 _._ 9 to +1 _._ 3 points on every suite (95 _._ 3 _→_ 96 _._ 5 on average) while never consuming more tokens than its control. The gain thus comes from _when_ the budget is spent, not how much of it is spent. 

**Choice of calibration.** A rank-based map, _α_<sup>(</sup><sup>_t_)</sup> = rank( _U_<sup>(</sup><sup>_t_)</sup> ) _/T_ , is more robust by construction: an anomalous step shifts _α_<sup>(</sup><sup>_t_)</sup> by at most 1 _/T_ instead of resetting the min–max range. On closed-loop rollouts the two are indistinguishable (Tab. 5), differing by at most 0 _._ 6 points (0 _._ 2 on average) at budgets within 2 _._ 5%, because _U_<sup>(</sup><sup>_t_)</sup> drifts smoothly rather than spiking, so min–max’s outlier sensitivity is never exercised. We keep min–max, which is continuous and preserves the magnitude of a deviation, and note that rank calibration is a drop-in substitute for noisy observations. 

**Choice of diversity metric.** Under identical scoring, budgets and calibration, we compare the inverse-Simpson effective number against a Shannon-based one ( _e_<sup>_H_</sup> _/K_ ) and 1 _−_ Gini, entropic and order-statistic families, respectively. Inverse-Simpson is strongest on both suites (Tab. 6), by +2 _._ 3 to +3 _._ 0 points over Shannon and +1 _._ 7 to +2 _._ 0 over Gini. This is not a budget artifact: it retains only 0 _._ 6–1 _._ 8% more tokens, worth a few tenths of a point by Tab. 4. We attribute the advantage to dynamic range: the Shannon logarithm and the saturation of 1 _−_ Gini near uniform distributions both compress the variation of _U_<sup>(</sup><sup>_t_)</sup> , leaving the calibration less contrast to resolve. 

## **5. Conclusion** 

We present FastVLA, a training-free, task-conditioned, and temporally adaptive visual-token compression framework for efficient VLA inference. Beyond scoring token importance with task-to-vision attention, its core idea is to reformulate per-step token budgeting as an online decision, setting the compression rate from the inverse-Simpson concentration of the importance distribution under slidingwindow calibration. Across three backbones and two simulation benchmarks, FastVLA cuts LLM-backbone FLOPs by 35-59% and action latency by 9-32% while maintaining task success, and on a physical Franka robot it reduces la- 

Table 5. Comparison of min–max and rank-based calibration across four LIBERO suites. Success rates and token usage are reported separately for each suite. 

|Calibration|Spat|ial|Obje|ct|
|---|---|---|---|---|
||SR (%)_↑_|Tokens|SR (%)_↑_|Tokens|
|Min–Max|97.8|104.3|98.0|156.3|
|Rank|97.6|103.0|98.0|159.5|
|Calibration|Go|al|10||
||SR (%)_↑_|Tokens|SR (%)_↑_|Tokens|
|Min–Max|97.0|131.9|93.1|206.8|
|Rank|96.9|132.1|92.5|205.5|


Table 6. Ablation of diversity metrics across the LIBERO-Goal and LIBERO-10 suites. Success rates and token usage are reported separately for each suite. 

|Diversity Metric|Go|al|10|
|---|---|---|---|
||SR (%)_↑_|Tokens|SR (%)_↑_<br>Tokens|
|Shannon|94.0|129.6|90.8<br>205.5|
|Gini|95.3|130.3|91.1<br>205.2|
|**Inverse-Simpson**|**97.0**|**131.9**|**93.1**<br>**206.8**|


tency by 20% and raises control frequency by up to 25% at comparable success, staying within 0.6 points of the uncompressed models on LIBERO while remaining entirely training-free. Incorporating robot-specific structure such as 3D geometry or proprioception into the importance estimate, and combining adaptive pruning with complementary reuse or early-exit strategies, are promising directions for further accelerating real-time VLA control. 

**Limitations.** _ρ_ is chosen per benchmark and backbone, and the budget-matched control covers only OpenVLAOFT on LIBERO. The connection between concentration and safe pruning is supported indirectly by that control rather than by a per-step analysis of pruning-induced action errors. The real-robot study covers two tasks with one backbone, and several baselines are quoted rather than rerun. 

8 

## **References** 

- [1] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, et al. Do as I can, not as I say: Grounding language in robotic affordances. In _Conference on Robot Learning_ , 2022. 2 

- [2] Saeed Ranjbar Alvar, Gursimran Singh, Mohammad Akbari, and Yong Zhang. DivPrune: Diversity-based visual token pruning for large multimodal models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 9392–9401, 2025. 2, 5 

- [3] Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, et al. _π_ 0 _._ 5: A vision-language-action model with open-world generalization. In _Conference on Robot Learning_ , 2025. 1, 2 

- [4] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-languageaction flow model for general robot control. In _Robotics: Science and Systems_ , 2025. 1, 2 

- [5] Daniel Bolya, Cheng-Yang Fu, Xiaoliang Dai, Peizhao Zhang, Christoph Feichtenhofer, and Judy Hoffman. Token merging: Your ViT but faster. In _International Conference on Learning Representations_ , 2023. 1, 2 

- [6] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. RT-1: Robotics transformer for real-world control at scale. In _Robotics: Science and Systems_ , 2023. 2 

- [7] Rui Cai, Jun Guo, Xinze He, Piaopiao Jin, Jie Li, Bingxuan Lin, Futeng Liu, Wei Liu, Fei Ma, Kun Ma, et al. XiaomiRobotics-0: An open-sourced vision-language-action model with real-time execution. _arXiv preprint arXiv:2602.12684_ , 2026. 1 

- [8] Liang Chen, Haozhe Zhao, Tianyu Liu, Shuai Bai, Junyang Lin, Chang Zhou, and Baobao Chang. An image is worth 1/2 tokens after layer 2: Plug-and-play inference acceleration for large vision-language models. In _European Conference on Computer Vision_ , pages 19–35. Springer, 2024. 1, 2, 5 

- [9] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44 (10-11):1684–1704, 2025. 1 

- [10] Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, et al. PaLM-E: An embodied multimodal language model. In _International Conference on Machine Learning_ , 2023. 2 

- [11] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, et al. Gemini Robotics: Bringing AI into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025. 1 

- [12] Titong Jiang, Xuefeng Jiang, Yuan Ma, Xin Wen, Bailin Li, Kun Zhan, Peng Jia, Yahui Liu, Sheng Sun, and Xianpeng Lang. The better you learn, the smarter you prune: Towards efficient vision-language-action models via differentiable token pruning. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2026. 1, 2, 5 

- [13] Lou Jost. Entropy and diversity. _Oikos_ , 113(2):363–375, 2006. 4 

- [14] C. J. Keylock. Simpson diversity and the Shannon–Wiener index as special cases of a generalized entropy. _Oikos_ , 109 (1):203–207, 2005. 4 

- [15] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P. Foster, Pannag R. Sanketi, Quan Vuong, et al. OpenVLA: An open-source vision-language-action model. In _Conference on Robot Learning_ , 2024. 1, 2, 5 

- [16] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. In _Robotics: Science and Systems_ , 2025. 1, 2, 5 

- [17] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. CogACT: A foundational visionlanguage-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 2, 5 

- [18] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, Sergey Levine, Jiajun Wu, Chelsea Finn, Hao Su, Quan Vuong, and Ted Xiao. Evaluating realworld robot manipulation policies in simulation. In _Conference on Robot Learning_ , 2024. 2, 5 

- [19] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. LIBERO: Benchmarking knowledge transfer for lifelong robot learning. In _Advances in Neural Information Processing Systems (Datasets and Benchmarks Track)_ , 2023. 2, 5 

- [20] Ziyan Liu, Yeqiu Chen, Hongyi Cai, Tao Lin, Shuo Yang, Zheng Liu, and Bo Zhao. VLA-Pruner: Temporal-aware dual-level visual token pruning for efficient vision-languageaction inference. _arXiv preprint arXiv:2511.16449v1_ , 2025. 

   - 2 

- [21] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An opensource generalist robot policy. In _Robotics: Science and Systems_ , 2024. 2 

- [22] Xiaohuan Pei, Yuxing Chen, Siyu Xu, Yunke Wang, Yuheng Shi, and Chang Xu. Action-aware dynamic pruning for efficient vision-language-action manipulation. In _International Conference on Learning Representations_ , 2026. 1, 2, 5, 6 

- [23] Xudong Tan, Yaoxin Yang, Peng Ye, Jialin Zheng, Bizhe Bai, Xinyi Wang, Jia Hao, and Tao Chen. Think twice, act once: Token-aware compression and action reuse for efficient inference in vision-language-action models. _arXiv preprint arXiv:2505.21200_ , 2025. 1, 2, 5, 6 

- [24] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia 

9 

   - Polosukhin. Attention is all you need. In _Advances in Neural Information Processing Systems_ , pages 5998–6008, 2017. 3 

- [25] Hanzhen Wang, Jiaming Xu, Yushun Xiang, Jiayi Pan, Yongkang Zhou, Yong-Lu Li, and Guohao Dai. SpecPruneVLA: Accelerating vision-language-action models via action-aware self-speculative pruning. In _International Conference on Machine Learning_ , 2026. 1, 2, 5, 6 

- [26] Siyu Xu, Yunke Wang, Chenghao Xia, Dihao Zhu, Tao Huang, and Chang Xu. VLA-Cache: Efficient visionlanguage-action manipulation via adaptive token caching. In _Advances in Neural Information Processing Systems_ , 2025. 1, 2, 5 

- [27] Yantai Yang, Yuhao Wang, Zichen Wen, Zhongwei Luo, Chang Zou, Zhipeng Zhang, Chuan Wen, and Linfeng Zhang. EfficientVLA: Training-free acceleration and compression for vision-language-action models. In _Advances in Neural Information Processing Systems_ , 2025. 1, 2, 5 

- [28] Qizhe Zhang, Aosong Cheng, Ming Lu, Renrui Zhang, Zhiyong Zhuo, Jiajun Cao, Shaobo Guo, Qi She, and Shanghang Zhang. Beyond text-visual attention: Exploiting visual cues for effective token pruning in VLMs. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 20857–20867, 2025. 2 

- [29] Yuan Zhang, Chun-Kai Fan, Junpeng Ma, Wenzhao Zheng, Tao Huang, Kuan Cheng, Denis Gudovskiy, Tomoyuki Okuno, Yohei Nakata, Kurt Keutzer, et al. SparseVLM: Visual token sparsification for efficient vision-language model inference. In _International Conference on Machine Learning_ , 2025. 1, 2, 5 

- [30] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. RT-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 1, 2 

10 

# **FastVLA: Task-Conditioned and Temporally Adaptive Visual Token Compression for Efficient Vision-Language-Action Models** Supplementary Material 

## **A. Discussion on FLOPs vs. latency.** 

We isolated every stage with CUDA-event timing, for FastVLA and for both re-run baselines (OpenVLA-OFT, 4-suite average; Tab. 7). Token scoring and selection add negligible cost: FastVLA’s scoring takes 1 _._ 5 ms, 1 _._ 8% of a step. The gap has three causes. (i) FLOPs counts only the LLM backbone, which is 55 _._ 7% of the baseline step. (ii) Within the LLM stage, time falls sub-linearly in FLOPs because at batch size 1 the backbone is bandwidth- rather than compute-bound at these sequence lengths. (iii) The vision encoder runs before compression and is unchanged by it; the residual 5–7% spread across methods is run-to-run variation, consistent with clock throttling under the heavier baseline step. The last row is computed as the actionprediction latency minus the measured stages, so it absorbs host–device synchronisation in addition to CPU pre/postprocessing; it shrinks with the token count because the host spends less time waiting on the backbone and because part of the input preparation scales with sequence length. Crucially, this is a property of the deployment regime and not of FastVLA: all three methods show the same sub-linear behaviour: FLOPs _−_ 58 _._ 5% vs. LLM time _−_ 38 _._ 8% (FastVLA), _−_ 69 _._ 6% vs. _−_ 50 _._ 5% (LightVLA), and _−_ 23 _._ 4% vs. _−_ 5 _._ 5% (VLA-Cache, whose reuse leaves attention spanning the full KV). Overall, FastVLA still delivers 118 _._ 5 _→_ 81 _._ 2 ms (1 _._ 46 _×_ ) and 67 _._ 5 _→_ 98 _._ 6 Hz. 

## **B. Signal transfer to CogACT** 

Tab. 8 supports the transferability of our main finding. Across all 16 configurations, vision-to-vision scoring consistently performs worst, and its gap from task-conditioned scoring grows with pruning: from 2 _._ 7 points at 30% to 32 _._ 2 points at 90% on average. From 30% to 90% pruning, taskconditioned scoring retains 22–57% of its success, compared with only 4–15% for vision-only scoring. This is consistent with our hypothesis: visual saliency captures visual distinctiveness, which need not align with task relevance, whereas task-conditioned scoring can prioritize decisioncritical regions as the token budget becomes scarce. 

The comparison between task-to-vision and all-to-vision is less consistent. On SIMPLER, they are nearly tied, with task-to-vision leading in 11 of 16 configurations by only 0 _._ 8 points on average. This may reflect SIMPLER’s short, template-generated tasks, for which the task tokens provide limited additional information over the full task-aware sequence. Thus, the robust distinction is task-aware versus 


Figure 6. Ablation on the deviation factor _τ_ in FastVLA on LIBERO-Object using OpenVLA-OFT. 

task-agnostic scoring. We use task-to-vision as the default because it performs best on average while using a smaller query set, making scoring cheaper. 

## **C. Ablations on the deviation factor** _τ_ **and window length** _T_ 

We ablate two key hyperparameters of FastVLA on OpenVLA-OFT: the deviation factor _τ_ and the window length _T_ . 

For the deviation factor _τ_ (LIBERO-Object, Fig. 6), which controls how aggressively the rate varies across steps, compute is nearly unaffected because it is governed by the target budget while success is highly sensitive: a small _τ_ (0 or 0 _._ 05) reduces to a near fixed-rate strategy and underperforms, an overly large _τ_ ( _≥_ 0 _._ 4) destabilizes budget allocation and over-compresses at critical moments, and a moderate _τ_ (0 _._ 1 _−_ 0 _._ 2) recovers near-baseline success; crucially, the gap between _τ_ = 0 and a moderate _τ_ shows that the temporal adaptivity itself, not merely the average token budget, preserves success, empirically validating the step-adaptive design at the core of FastVLA. 

For the window length _T_ (LIBERO-Long, Fig. 7), compute is again negligibly affected while success peaks at a moderate window ( _T_ = 10), outperforming both smaller ( _T_ = 5) and larger ( _T_ = 20 or + _∞_ ) windows: too small a window yields unstable temporal statistics, whereas too large a window introduces stale importance signals from earlier manipulation phases that no longer match the current decision. 

11 

|ms/step (4-suite avg.)|Baseline|+FastVLA|+LightVLA|+VLA-Cache|
|---|---|---|---|---|
|LLM FLOPs (T)_↓_|3.98|1.65|1.21|3.05|
|Vision encoder|34.6|32.9|32.0|32.8|
|Token scoring / selection|–|1.5|1.3|CPU<sup>_†_</sup>|
|LLM backbone (FLOPs scope)|66.0|**40.4**|32.7|62.4|
|Action head|0.5|0.5|0.6|0.5|
|Other (CPU + sync)|17.4|5.9|5.8|4.1|
|Action-prediction latency|118.5|**81.2**|72.4|99.8|


Table 7. Stage-wise latency decomposition (CUDA events, RTX 4090). All stages are measured from 500-episode runs. VLA-Cache selects reusable tokens on the CPU, overlapping the GPU stages. 

|Setting / Task|Scoring signal||Prunin|g rate||
|---|---|---|---|---|---|
|||30%|50%|70%|90%|
|_Visual Matchin_|_g_|||||
||Task-to-vision|92.7|89.3|71.7|53.0|
|PickCan|All-to-vision|93.7|88.7|75.0|56.7|
||Vision-to-vision|88.7|78.0|58.3|11.3|
||Task-to-vision|88.8|79.6|60.0|30.4|
|MoveNear|All-to-vision|86.3|75.8|54.6|35.4|
||Vision-to-vision|85.4|73.8|46.7|12.5|
|_Variant Aggreg_|_ation_|||||
||Task-to-vision|88.0|82.7|74.7|46.7|
|PickCan|All-to-vision|89.3|80.0|72.0|45.3|
||Vision-to-vision|86.7|74.7|56.0|5.3|
||Task-to-vision|76.7|75.8|49.2|22.5|
|MoveNear|All-to-vision|75.8|73.3|46.7|20.0|
||Vision-to-vision|75.0|67.5|42.5|3.3|


Table 8. Transfer of the importance signal to CogACT on SIMPLER. Success rate (%) under progressive visual-token pruning for the three candidate scoring signals of Sec. 3.2, on both SIMPLER settings. 


Figure 7. Ablation on the window length _T_ in FastVLA on LIBERO-Long using OpenVLA-OFT. 

12 

