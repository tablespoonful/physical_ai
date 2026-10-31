---
title: "EcoVLA: Environment-Aware Adaptive Pruning with Interleaved Inference Orchestration for Vision-Language-Action Models"
date: "2026"
venue: "ICML 2026"
url: https://proceedings.mlr.press/v306/huang26h.html
pdf: https://raw.githubusercontent.com/mlresearch/v306/main/assets/huang26h/huang26h.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://raw.githubusercontent.com/mlresearch/v306/main/assets/huang26h/huang26h.pdf)** / [論文ページ](https://proceedings.mlr.press/v306/huang26h.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**EcoVLA: Environment-Aware Adaptive Pruning with Interleaved Inference Orchestration for Vision-Language-Action Models** 

**Yuting Huang**<sup>* 1</sup> **Leilei Ding**<sup>* 1</sup> **Zhipeng Tang**<sup>* 1</sup> **Zenghuan Zhu**<sup>1</sup> **Jiajun Deng**<sup>1</sup> **Xinrui Lin**<sup>1</sup> **Shuo Liu**<sup>1</sup> **Haojie Ren**<sup>1</sup> **Jianmin Ji**<sup>1</sup> **Yanyong Zhang**<sup>1</sup> 

# **Abstract** 

# **1. Introduction** 

While Vision-Language-Action (VLA) models hold promise in embodied intelligence, their large parameter counts lead to substantial inference latency that hinders real-time manipulation, motivating parameter sparsification. However, as the environment evolves during VLA execution, the optimal sparsity patterns change accordingly. Static pruning lacks the adaptability required for environment dynamics, whereas fixed-interval dynamic layer pruning suffers from coarse granularity and high retraining overheads. To bridge this gap, we propose **EcoVLA** , a training-free, plug-and-play adaptive pruning framework that supports orthogonal combination with existing VLA acceleration methods. EcoVLA comprises two components: **E** nvironment-aware **A** daptive **P** runing ( **EAP** ) and **I** nterleaved **I** nference **O** rchestration ( **I**<sup>**2**</sup> **O** ). EAP is a lightweight adaptive channel pruning method that incorporates the temporal consistency of the physical environment to update sparsity patterns. I<sup>2</sup> O leverages the FLOPs bubbles inherent in VLA inference to schedule the pruning method in parallel, ensuring negligible impact on latency. Evaluated on diverse VLA models and benchmarks, EcoVLA delivers state-of-the-art performance, achieving up to 1.60 _×_ speedup with only a 0.4% drop in success rate, and further reaches 2.18 _×_ speedup with only a 0.5% degradation when combined with token pruning. We further validate the effectiveness of EcoVLA on real-world robots. Our code is available here. 

> *Equal contribution 1University of Science and Technology of China, Hefei, China. Correspondence to: Jianmin Ji _<_ jianmin@ustc.edu.cn _>_ , Yanyong Zhang _<_ yanyongz@ustc.edu.cn _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

Vision-Language-Action (VLA) models enhance the generalization of embodied intelligence by injecting semantic understanding into robot control (Black et al., 2024; Li et al., 2024a; Kim et al., 2024). Despite promising real-world results from recent VLA models such as OpenVLA (Kim et al., 2024) and _π_ 0 _._ 5 (Intelligence et al., 2025), inference latency remains the primary bottleneck for real-time control (Yang et al., 2025). In this context, token pruning (Wang et al., 2025; Liu et al., 2025) has been extensively researched as a method to reduce input size, which decreases latency by discarding redundant visual tokens at the risk of losing critical semantics with high pruning ratio. While token-level optimization has been thoroughly studied (Shinde et al., 2025), comparatively little attention has been paid to VLA model pruning. In this work, we focus on VLA model pruning, an area with less research, to further accelerate inference by reducing redundant model parameters. Typically, a VLA architecture comprises a lightweight action expert and a heavy VLM backbone, which dominates the parameter count and shows high sparsity, making it a prime target for pruning (Chen & Li, 2025; Jabbour et al., 2025). 

Existing research on VLA model sparsification primarily bifurcates into two directions, static and dynamic pruning. Static pruning methods, such as RLRC (Chen & Li, 2025) and GLUESTICK (Jabbour et al., 2025), perform pruning or recovery offline. However, they fail to adapt to the dynamically evolving task environment (e.g., transitioning from large-scale navigation to fine-grained local manipulation), where optimal sparsity patterns vary dynamically (Liu et al., 2023b), as shown in Figure 1. Consequently, these static approaches often suffer performance degradation under dynamic sparsity shifts. Moreover, they are heavily shackled by the requirement for massive retraining cycles or a reconstruction process that incurs unsustainable computational costs. To address the inflexibility of static approaches, dynamic pruning methods like MoLe-VLA (Zhang et al., 2026) and DeeR-VLA (Yue et al., 2024) select layers at fixed intervals based on runtime inputs but suffer from critical drawbacks: the dependency on auxiliary routers incurs extra training and runtime inference overheads, while their 

1 

**Environment-Aware Adaptive Pruning with Interleaved Inference Orchestration for Vision-Language-Action Models** 


_Figure 1._ During VLA execution, channel importance scores vary dynamically as the environment evolves, causing the optimal sparsity pattern to shift accordingly. 

coarse layer-level granularity overlooks fine-grained intralayer redundancy. 

To bridge these gaps, a training-free, fine-grained, and environment-aware adaptive model pruning method is urgently needed. However, two major challenges remain. First, VLA models’ sparsity patterns evolve with the environment, making real-time computation difficult. Additionally, relying only on instantaneous observations fails to capture the continuous nature of VLA execution. Second, adaptive pruning introduces real-time overhead. While existing methods for LLMs use large-batch inference to amortize overhead across multiple samples (Le et al., 2025), VLA models constrained by single-sample streaming bear the pruning overhead individually, directly adding it to the end-to-end inference latency. For frequency-sensitive VLA models, such delays limit the effective policy update rate, inducing robotic stuttering and jittering (Black et al., 2026). 

To address these challenges, we propose **EcoVLA** , a training-free, plug-and-play pruning framework capable of adapting sparsity patterns via real-time environmental perception while minimizing pruning overhead through nonblocking parallel inference. EcoVLA comprises two core components: **E** nvironment-aware **A** daptive **P** runing ( **EAP** ) and **I** nterleaved **I** nference **O** rchestration ( **I**<sup>**2**</sup> **O** ). 

EAP is a lightweight, environment-aware adaptive structured channel pruning method. First, leveraging visual observations, EAP perceives environmental dynamics to identify variations in sparsity patterns. Crucially, to maintain the temporal consistency essential for stable VLA execution, we incorporate a temporal feature aggregation strategy. By strategically integrating the instantaneous features with historical features, EAP precisely identifies redundant channels for pruning. The continuous update of historical features with the latest features further guarantees the temporal consistency of the sparsity patterns. 

I<sup>2</sup> O replaces the conventional sequential paradigm with a non-blocking parallel paradigm, strategically exploiting FLOPs Bubbles within VLA inference. Specifically, I<sup>2</sup> O orchestrates two parallel streams, comprising an Inference Stream for real-time action generations and a Prun- 

ing Stream for pruning execution. By interleaving pruning computations into the FLOPs bubbles, we maximize overall hardware utilization, effectively masking the pruning overhead to ensure robust real-time streaming control. We evaluate EcoVLA on robotic manipulation across two simulators (LIBERO (Liu et al., 2023a) and SIMPLER (Li et al., 2024b)) and three VLA models (OpenVLA-OFT (Kim et al., 2025), _π_ 0 _._ 5 (Intelligence et al., 2025) and CogACT (Li et al., 2024a)). EcoVLA achieves 1 _._ 6 _×_ speedup with only a 0 _._ 4% reduction in success rate. Furthermore, by integrating with token pruning methods, EcoVLA boosts the speedup from 1 _._ 21 _×_ (achieved by FastV with a 50% pruning ratio) to 2 _._ 18 _×_ . Crucially, it recovers the accuracy drop caused by FastV, narrowing the performance gap with the vanilla baseline to just 0 _._ 5%. To validate our approach beyond simulation, we deploy EcoVLA on a 7-DoF Kinova Gen3 and a 19-DoF Franka equipped with XHand, demonstrating its practical acceleration capabilities in real-world scenarios. 

# **2. Related Work** 

**Vision-Language-Action Models.** With the rapid development of embodied intelligence, research attention has increasingly expanded beyond high-level task planning toward embodied task execution (Huang et al., 2025; Lin et al., 2025; Kim et al., 2024). In this context, VLAs extend VLMs by incorporating action modalities for embodied control, while also integrating certain planning capabilities to bridge perception, reasoning, and action (Brohan et al., 2022; Black et al., 2024; Kim et al., 2025; Tang et al., 2025b). Despite their efficacy, deployment is constrained by high computational costs (Yang et al., 2025; Jiang et al., 2026). As action heads (e.g., MLPs, diffusion) are lightweight, the VLM backbone remains the dominant computational bottleneck (Zhang et al., 2026; Ma et al., 2025). 

**Efficient Vision-Language-Action Models.** VLA acceleration typically employs token pruning (Wang et al., 2025; Liu et al., 2025) or KV caching (Xu et al., 2026) to exploit input redundancy. For model sparsification, static methods (Chen & Li, 2025; Jabbour et al., 2025) prune parameters offline but lack environmental adaptability and require retraining or reconstruction. Conversely, fixed-interval dynamic methods (Yue et al., 2024; Zhang et al., 2026) offer task-dependence but suffer from high retraining costs and limited transferability. While other techniques such as action chunking (Zhao et al., 2023), which predicts multiple steps of actions at once, and asynchronous inference (Tang et al., 2025a; Black et al., 2026), which overlaps model inference with action execution, can also yield speedup benefits, they are not designed to address these limitations. Consequently, a training-free, fine-grained, and plug-and-play adaptive pruning framework is needed, which can be readily integrated with existing acceleration methods. 

2 

**Environment-Aware Adaptive Pruning with Interleaved Inference Orchestration for Vision-Language-Action Models** 


_Figure 2._ Overall pipeline of EcoVLA. (a) **E** nvironment-aware **A** daptive **P** runing ( **EAP** ): EAP is a lightweight, environment-aware method that identifies sparsity variations by perceiving real-time dynamics. Considering the temporal consistency of VLA execution in physical environments, EAP integrates instantaneous features with historical features to jointly compute the sparsity pattern. (b) **I** nterleaved **I** nference **O** rchestration ( **I**<sup>**2**</sup> **O** ): I<sup>2</sup> O interleaves sparsity pattern computation into the inherent FLOPs bubbles within the VLA inference using a non-blocking parallel paradigm. 

# **3. Preliminaries** 

## **3.1. Vision-Language-Action Models** 

Vision-Language-Action (VLA) models unify visual and linguistic inputs to generate robotic actions, typically consisting of a Vision-Language Model (VLM) backbone and an Action Expert (Kim et al., 2025; Wen et al., 2025). While Action Expert architectures vary (e.g., Diffusion-based or Parallel Decoding) (Black et al., 2024; Kim et al., 2025; Intelligence et al., 2025), they are lightweight compared to the VLM backbone. Thus, the VLM constitutes the primary bottleneck, rendering its standardized architecture the ideal candidate for pruning. 

## **3.2. Formulation of VLA Structured Pruning** 

Let _π_ Θ be a VLA model with Large Language Model (LLM) backbone Θ. We target Θ for pruning due to its dominant model size. We optimize a structural binary mask **m** _∈{_ 0 _,_ 1 _}_<sup>_|_Θ</sup><sup>_|_</sup> (where grouped elements share values) to minimize the divergence between dense and pruned policies: 


where _⊙_ denotes the element-wise product, _κ_ is sparsity constraint, and _D_ represents the calibration dataset. The objective _L_ measures the divergence between models. 

To efficiently solve the global optimization problem defined in (1), we decompose the LLM into layer-wise reconstruction paradigm (An et al., 2024; Le et al., 2025). The LLM consists of _L_ blocks. Each block _l_ transforms the input hidden state **X**<sup>_l_</sup> _∈_ R<sup>_B×S×D_</sup> via a residual mapping: 


We decompose the block function _F_<sup>_l_</sup> into an intermediate transformation and a final linear projection: 


Here, _T_<sup>_l_</sup> is intermediate transformation (e.g., **W**<sup>_K_</sup> or **W**<sup>up</sup> ), while **W**<sup>_l,_final</sup> represents the final weight matrix (e.g., **W**<sup>_O_</sup> or **W**<sup>down</sup> ). Since these intermediate representations encode rich contextual features (Ding et al., 2024; Yan et al., 2026), they can be effectively utilized to guide the computation of the structured sparsity patterns. For hardware acceleration, structured pruning aligns output channels with input 

3 

**Environment-Aware Adaptive Pruning with Interleaved Inference Orchestration for Vision-Language-Action Models** 


where **W**<sup>�</sup><sup>_l,_gate</sup> _,_ **W**<sup>�</sup><sup>_l,_up</sup> _∈_ R<sup>_|_C</sup><sup>_l|×C_out</sup> and **W**<sup>�</sup><sup>_l,_down</sup> _∈_ R<sup>_C_out</sup><sup>_×|_C</sup><sup>_l|_</sup> . The notation _|_ C<sup>_l_</sup> _|_ is the cardinality of C<sup>_l_</sup> . Similarly, in attention blocks, pruning heads removes coupled output channels of **W**<sup>_Q,K,V_</sup> and input channels of **W**<sup>_O_</sup> . 

# **4. Methodology** 

In this section, we introduce EcoVLA, the first training-free, plug-and-play adaptive pruning framework for VLA models, as illustrated in Figure 2. We first detail Environment-aware Adaptive Pruning (EAP) in Section 4.1, which begins with a lightweight predictor to identify real-time sparsity variations and subsequently employs a pruning method based on temporal consistency. Next, we introduce Interleaved Inference Orchestration (I<sup>2</sup> O) in Section 4.2, a parallel execution paradigm that exploits inference FLOPs bubbles to schedule pruning operations, thereby reducing additional overhead. 

## **4.1. Environment-aware Adaptive Pruning** 

## 4.1.1. LIGHTWEIGHT ENVIRONMENT-AWARE SPARSITY VARIATIONS PREDICTOR 

The optimal sparsity patterns of VLA models evolve dynamically during execution. To capture these changes efficiently, we introduce a lightweight environment-aware sparsity-pattern variation predictor. This module leverages visual feature similarities alongside a temporal contextconditioned trigger, enabling rapid and robust identification of changes. 

**Lightweight Visual Similarity Metric.** To avoid introducing substantial computational overhead, we discard the popular attention-based semantic similarity (Xu et al., 2026), opting instead to leverage the visual features extracted by the VLA visual encoder to compute the similarity between step _t_ and _t −_ 1. Let _ft, ft−_ 1 _∈_ R<sup>_N×D_</sup> denote the image token features, where _N_ is the number of visual tokens and _D_ is the feature dimension. We define the similarity score as the average token-wise cosine similarity: 


We posit that if the visual features _ft_ and _ft−_ 1 exhibit high similarity, the sparsity pattern remains stable between frames. Conversely, significant deviation in visual features implies considerable variation in the sparsity pattern. 

**Temporal Context–Conditioned Sparsity Trigger.** In open-world robotic manipulation, the environment is dynamic, causing the distribution of visual feature similarities 

to evolve over time. Since we rely on these similarities to update sparsity patterns, a static decision criterion becomes brittle under distribution shifts. Therefore, we introduce a lightweight Temporal Context-Conditioned Sparsity Trigger, which leverages temporal context to adapt to such shifts. Specifically, we maintain a fixed-size sliding window _Ht_ storing the similarities of the recent _T_ frames: 


Based on this temporal context, we adopt a dynamic decision criterion where the sparsity update is triggered if the current similarity drops below the _p_ -th quantile of the _Ht_ . The sparsity pattern update policy is formally defined as: 


Here, _p_ serves as a sensitivity hyperparameter, where a higher _p_ enhances responsiveness to subtle changes, whereas lower _p_ prioritizes stability. This mechanism yields self-regulative behavior. During rapid motion, the quantile naturally decreases, suppressing excessive updates to ensure stability. Conversely, in stable phases, the quantile increases, facilitating the sensitive detection of fine-grained variations. 

## 4.1.2. TEMPORAL CONSISTENCY PRUNING 

This section details the sparsity pattern computation. Upon triggering a sparsity update at frame _t_ , we execute a dense inference to perform the pruning calculation. We first compute the instantaneous features from the current input at frame _t_ , which are subsequently aggregated with historical features. The newly computed sparsity pattern is then applied starting from the frame _t_ + 1 for sparse inference. 

To formalize this computation, we denote the update triggered at frame _t_ as the _τ_ -th sparsity update step. Specifically, as the current input reaches block _l_ , following the formulation in Section 3.2, we can compute the current intermediate hidden states **X**<sup>_l,int,τ_</sup> = _T_<sup>_l_</sup> (LN( **X**<sup>_l,τ_</sup> )). Given that VLA models operate on single-sample streaming inputs, the dimensionality of **X**<sup>_l,_int</sup><sup>_,τ_</sup> is defined as (1 _, S, Cin_ ). For notational simplicity, we omit the batch dimension in the subsequent formulation. To quantify the activation of the current input across structured channels, we compress the activation along the sequence dimension to obtain the instantaneous feature. Formally, for the _k_ -th structured channel, the calculation is performed as follows: 


where _ϵ_<sup>_l,τ_</sup> _k_ represents the instantaneous feature of the _k_ -th structured channel given the current input. However, relying solely on instantaneous features is suboptimal, as the physical execution of VLA models exhibits 

4 

**Environment-Aware Adaptive Pruning with Interleaved Inference Orchestration for Vision-Language-Action Models** 

inherent temporal consistency. This temporal consistency is characterized by smooth, continuous transitions in both physical environments and proprioceptive states across adjacent frames, rather than discrete, abrupt jumps. In light of this, we aggregate the instantaneous feature with the historical feature. Specifically, we initialize the historical feature _E_<sup>_l,_(0)</sup> _∈_ R<sup>_Cin_</sup> for each block _l_ by averaging the instantaneous features computed by Equation 8 over the calibration dataset. For each subsequent update step _τ_ , we can compute the fused feature by leveraging the previous historical feature _E_<sup>_l,_(</sup><sup>_τ−_1)</sup> as a temporal prior: 


where _α ∈_ [0 _,_ 1] is the temporal inertia parameter. A larger _α_ leads to a more conservative update. We update the historical feature on full channels using an exponential moving average. Here, the momentum _λ_ ensures temporal consistency, providing a stable prior for subsequent steps: 


Finally, we can compute the sparsity pattern. Following PPsp (Le et al., 2025), we evaluate the significance of the _k_ - th channel in the _l_ -th layer based on both weight magnitude and fused feature. Let **W**<sup>_l,_final</sup> _∈_ R<sup>_Cout×Cin_</sup> denote the final weight matrix in block _l_ . The importance score _Sk_<sup>_l,τ_</sup> is formulated as: 


where _{·}_ denotes the set of elements, and _S_<sup>_l,τ_</sup> _∈_ R<sup>_Cin_</sup> . Crucially, identifying and pruning the _k_ -th input channel of **W**<sup>_l,_final</sup> (associated with low _Sk_<sup>_l,τ_) necessitates the simulta-</sup> neous removal of the corresponding _k_ -th output channel of the intermediate transformations _T_<sup>_l_</sup> . 

## 4.1.3. ANALYSIS OF COMPUTATIONAL COST 

The computational overhead of EAP is primarily divided into visual feature similarity and sparsity pattern computation. For an image represented by _N_ visual tokens with feature dimension _D_ and a block with _Cin_ hidden dimensions and _Cout_ output channels, the sparsity pattern overhead includes instantaneous feature computation, feature fusion, historical feature updates, and importance score computation. Although the computational cost can be reduced through pre-computation, the worst-case complexity occurs when weight magnitudes are computed online, leading to the following FLOPs formulation: 


The computational overhead of EAP is marginal, as it primarily consists of element-wise operations that exhibit a negligible footprint compared to the VLA. 

## **4.2. Interleaved Inference Orchestration** 

In this section, we first analyze the computational characteristics of VLA inference, revealing FLOPs bubbles arising from resource under-utilization. We then introduce **I** nterleaved **I** nference **O** rchestration ( **I**<sup>**2**</sup> **O** ), which exploits the complementary resource profiles between the VLM Backbone and Action Expert stages to absorb sparsity pattern computation into these bubbles with minimal overhead (Figure 2). Finally, we present hardware-efficient implementations to further accelerate both dense and sparse execution. 

## 4.2.1. FLOPS BUBBLES OF VLA INFERENCE 

In this section, our profiling reveals temporal FLOPs bubbles during VLA inference due to a mismatch between model workload and hardware capacity, providing an opportunity to absorb sparsity pattern computation overhead. 

**The VLM Backbone Stage.** This stage is dominated by large-scale General Matrix Multiplications (GEMMs) in transformer layers, rendering it inherently computebound (Williams et al., 2009). Given the massive model dimensions ( _N, K_ ) and the extensive sequence length ( _M_ ), the arithmetic intensity ( _I_ ) of these operations significantly exceeds the hardware’s compute-to-memory ratio: FLOPs 2 _· M · N · K_ (13) Bytes<sup>=</sup> 2 _·_ ( _NK_ + _MK_ + _MN_ )<sup>_≫_</sup> _T_<sup>_T_</sup> bandwidth<sup>compute</sup> 

where _T_ compute and _T_ bandwidth compute throughput and memory bandwidth, respectively. Consequently, the GPU Tensor Cores operate at near-peak saturation, while the memory bandwidth remains largely under-saturated, providing the necessary headroom for concurrent auxiliary tasks. 

**The Action Expert Stage.** In stark contrast, this stage consists of lightweight MLPs or diffusion-based denoising steps (Ma et al., 2025). Operating under the real-time, robotic control streaming (batch size = 1), computational demand falls orders of magnitude below the GPU’s peak parallel processing capacity (Markidis et al., 2018). In this state, the powerful Tensor Cores remain largely under-utilized, leaving a substantial computational reservoir that can be reclaimed to execute auxiliary tasks. 

## 4.2.2. HIDING PRUNING OVERHEADS VIA I<sup>2</sup> O 

The conventional synchronous pruning stream is serially scheduled either preceding or succeeding the main inference stream, thereby linearly increasing the total latency. To circumvent this bottleneck, EcoVLA introduces **I** nterleaved **I** nference **O** rchestration ( **I**<sup>**2**</sup> **O** ) as illustrated in Figure 2, whose core philosophy is to interleave sparsity pattern computation into the FLOPs bubbles of the VLA pipelines. 

Specifically, we decouple the sparsity pattern computation for step _t_ + 1 from the main dense inference of the current 

5 

**Environment-Aware Adaptive Pruning with Interleaved Inference Orchestration for Vision-Language-Action Models** 

step _t_ by dispatching it to a parallel pruning stream. During the VLM Backbone stage, where the GPU is computesaturated but memory bandwidth remains undersaturated, the pruning stream concurrently buffers the requisite intermediate activations. Subsequently, as the inference transitions to the Action Expert stage, I<sup>2</sup> O interleaves the sparsity pattern computation into FLOPs bubbles, effectively utilizing the idle Tensor Cores. As a result, I<sup>2</sup> O fully taps into the GPU’s untapped computational potential, achieving a balanced workload distribution across the inference pipeline. By interleaving the sparsity pattern computation into the FLOPs bubbles, our approach avoids intense GPU resource contention, enabling low-latency sparsity-pattern computation with minimal overhead. 

Building on this efficient orchestration, we now turn our attention to the latency analysis of I<sup>2</sup> O. Let _Tinfer_ denote the VLA inference latency and _Tprune_ the overhead. In conventional synchronous approaches, the total latency is additive: _Lsynch_ = _Tinfer_ + _Tprune_ . In I<sup>2</sup> O, the latency becomes _LI_ 2 _O_ = _Tinfer_ + _δ_ , where _δ_ accounts for the overhead induced by concurrent execution, such as Streaming Multiprocessor (SM) scheduling costs, memory bandwidth contention and minor GPU resource competition. Owing to the lightweight design of the adaptive pruning module and its execution within FLOPs bubbles, _δ_ is minimal. Consequently, this orchestration ensures that adaptive pruning is integrated seamlessly without impacting the latency-sensitive VLA control loop, thus maintaining the high-frequency reactivity essential for smooth robotic manipulation. 

## **4.3. Hardware-efficient Implementation** 

In this section, we detail the hardware-level optimizations implemented for both dense and sparse VLA inference to achieve practical inference acceleration. 

ciency (Yang et al., 2018). We simply store these matrices in column-major format to enhance memory access locality. Similarly, we also store the output projection weights _WO_ in the self-attention module in a column-major format. 

**High-Performance Fused Kernels.** During sparse VLA inference, the MLP computes gate projection, up projection, SiLU activation, and element-wise multiplication. We fuse these four operations into a single Triton kernel that reads the input once and keeps intermediate results in registers, eliminating redundant memory traffic and reducing kernel launches from 4 to 1, yielding nearly 2 _×_ speedup in practice. 

## 4.3.2. DENSE METRIC ACCELERATION 

In addition to I<sup>2</sup> O, we apply two memory-level optimizations to accelerate sparsity pattern computation. 

**Allocation-Free Caching.** As noted in Equation 11, computing the sparsity pattern involves L2 norms of squared weights and activation norms, where standard implementations suffer from repeated weight loading and dynamic memory allocation. We address this by pre-computing L2 norms of squared weights as compact vectors (a 99.97% reduction) and pre-allocating static activation buffers, transforming memory-bound operations into lightweight lookups while eliminating runtime allocations. 

**Batched Metric Computation.** Per-layer sparsity computation incurs many separate kernel launches. We instead stack L2 norms of squared weights and activation buffers across layers into contiguous tensors, enabling kernel fusion that amortizes launch overhead and exposes layer-level parallelism. 

# **5. Experiments** 

## **5.1. Experimental Settings** 

## 4.3.1. SPARSE EFFICIENT KERNELS 

We apply three kernel-level optimizations targeting memory efficiency and computation throughput in sparse inference. 

**Sparse Linear Transformation Kernel.** In the standard PyTorch implementation, the retained weights are indexed before performing the linear transformation, which incurs additional memory I/O overhead. In contrast, we have implemented a sparse linear transformation Triton kernel (Tillet et al., 2019; Liu et al., 2023b) that directly loads only the retained weights during computation, avoiding this overhead and improving efficiency. 

**Memory coalescing.** As described in Section 3.2, when performing pruning on the _W_ down weights of the MLP, we actually prune the columns of the weights. In the sparse implementation, this results in indices pointing to non-contiguous memory regions, leading to reduced memory access effi- 

**Baselines.** To validate the generalizability of EcoVLA, we evaluate it across diverse VLA architectures. In simulation, we conduct experiments on open-source VLA models, including OpenVLA-OFT (Kim et al., 2025), _π_ 0 _._ 5 (Intelligence et al., 2025), and CogACT (Li et al., 2024a). For fair comparison, we benchmark EcoVLA against Wanda (Sun et al., 2023), a mainstream static pruning method. Beyond standalone improvements, we demonstrate that EcoVLA is broadly compatible and can be stacked with other acceleration techniques. Experiments combining EcoVLA with FastV (Chen et al., 2024) and VLA-Cache (Xu et al., 2026) yield substantial additional speedups with negligible performance degradation. For real-world evaluation, we fine-tune _π_ 0 _._ 5 for deployment on a 7-DoF Kinova Gen3 robotic arm and a 19-DoF Franka equipped with XHand. See Appendix A for further details. 

**Evaluation Protocol.** To ensure a comprehensive compar- 

6 

**Environment-Aware Adaptive Pruning with Interleaved Inference Orchestration for Vision-Language-Action Models** 

_Table 1._ Performance of EcoVLA on OpenVLA-OFT in LIBERO at 25% and 40% pruning ratios. For VLA-Cache-based methods, speedup is computed using the eager LlamaAttention latency reported in parentheses. 

|||Succe|ss Rate(%) _↑_||||||
|---|---|---|---|---|---|---|---|---|
|Method|LIBERO-Spatial|LIBERO-Object|LIBERO-Goal|LIBERO-Long|Average|FLOPs (T)_↓_|Latency (ms)_↓_|Speedup_↑_|
|Vanilla|97_._6|98_._4|96_._2|94_._6|96_._7|4_._05(100_._0%)|143_._56(162_._78)|1_._00_×_|
|FastV|96_._4|97_._2|89_._0|94_._8|94_._4|2_._49(61_._48%)|118_._57|1_._21_×_|
|VLA-Cache|96_._6|98_._6|96_._4|94_._8|96_._6|3_._03(74_._81%)|148_._51|1_._10_×_|
||||_Pruning  _|_Ratio 25%_|||||
|Wanda|95_._8|98_._8|87_._2|93_._2|93_._8|3_._14(77_._53%)|124_._32|1_._15_×_|
|**Ours**|97_._4|98_._8|94_._6|96_._4|96_._8|3_._23(79_._75%)|113_._98|1_._26_×_|
|**FastV + Ours**|96_._6|98_._2|94_._0|96_._0|96_._2|1_._96(48_._39%)|65_._85|2_._18_×_|
|**VLA-Cache + Ours**|96_._8|98_._4|92_._4|94_._2|95_._5|2_._43(60_._00%)|121_._24|1_._34_×_|
||||_Pruning  _|_Ratio 40%_|||||
|Wanda|89_._2|98_._4|77_._0|90_._6|88_._8|2_._57(63_._46%)|106_._47|1_._35_×_|
|**Ours**|95_._6|97_._8|89_._4|93_._2|94_._0|2_._74(67_._65%)|101_._58|1_._41_×_|
|**FastV + Ours**|94_._4|97_._8|85_._8|93_._4|92_._9|1_._64(40_._49%)|61_._16|2_._35_×_|
|**VLA-Cache + Ours**|93_._0|98_._2|89_._6|93_._4|93_._6|2_._03(50_._12%)|108_._48|1_._50_×_|


_Table 2._ Performance of EcoVLA on _π_ 0 _._ 5 in LIBERO at 25% and 37 _._ 5% pruning ratios. 

|Method|Sparsity|LIBERO-Spatial|Success<br> LIBERO-Object|Rate(%) _↑_<br>LIBERO-Goal|LIBERO-Long|Average|FLOPs (T)_↓_|Latency (ms)_↓_|Speedup_↑_|
|---|---|---|---|---|---|---|---|---|---|
|Vanilla|0%|98_._8|98_._2|98_._0|92_._4|96_._9|1_._99(100_._0%)|81_._94|1_._00_×_|
||25_._0%|98_._2|98_._6|98_._4|91_._6|96_._7|1_._64(82_._41%)|62_._66|1_._31_×_|
|**Ours**|37_._5%|97_._8|98_._4|96_._8|87_._0|95_._0|1_._47(73_._87%)|55_._98|1_._46_×_|
||_Tab_|_le 3._ Performa|nce of EcoVLA|on CogACT|in SIMPLE|R at25|%and40%pr|uning ratios.||


|SIMPLER|Method|Sparsity<br>|Pick Cok|Succ<br>e Move Near|ess Rate(%)<br> Open/Close|_↑_<br> Open Top|Average|FLOPs (T)_↓_|Latency (m|s)_↓_Speedup_↑_|
|---|---|---|---|---|---|---|---|---|---|---|
|Visual Matching|Vanilla<br>**Ours**<br>**Ours**|0<br>25%<br>40%|93_._3<br>95_._0<br>93_._0|83_._8<br>82_._1<br>85_._4|74_._5<br>70_._8<br>73_._5|41_._7<br>38_._9<br>42_._6|73_._3<br>71_._7<br>73_._6|1_._81 (100_._0%)<br>1_._45 (80_._11%)<br>1_._25(69_._06%)|104_._16<br>72_._65<br>66_._43|1_._00_×_<br>1_._43_×_<br>1_._57_×_|
||Vanilla|0|88_._7|76_._8|26_._7|51_._9|61_._0|1_._81 (100_._0%)|105_._87|1_._00_×_|
|Variant Aggregation|**Ours**<br>**Ours**|25%<br>40%|85_._9<br>86_._1|75_._3<br>74_._3|27_._2<br>33_._1|46_._0<br>48_._7|58_._6<br>60_._6|1_._47 (81_._22%)<br>1_._28 (70_._72%)|73_._98<br>66_._25|1_._43_×_<br>1_._60_×_|
|erformance of E<br>od<br>Task1<br>ine<br>12_/_20<br><br>s<br>12_/_20<br>|coVLA<br>Task2<br>18_/_20<br>16_/_20|on_π_0_._5 <br>Task3<br>16_/_20<br>15_/_20|on a re<br><br>Lat<br><br>|al-world rob<br>ency (ms)<br>86_._08<br>68_._40|ot.|**P**|**lace the ap**|**ple**<br>**Put the**|**pill bottle**|**Place the banana**|
|||||||**i**|**n the bask**|**et.**<br>**in the**|**cabinet.**|**in the basket.**|


_Table 4._ Performance of EcoVLA on _π_ 0 _._ 5 on a real-world robot. 

|Method|Task1|Task2<br>Ta|sk3|Latency (ms)|
|---|---|---|---|---|
|Baseline|12_/_20|18_/_20<br>16|_/_20|86_._08|
|Ours|12_/_20|16_/_20<br>15|_/_20|68_._40|


_Table 5._ Overhead of Pruning Stream. 

_Figure 3._ Robot Manipulation on Kinova Gen3 Platform. 

|Execution Method|Latency (ms)|
|---|---|
|Normal VLA Inference|143.56|
|I<sup>2</sup>O|148.06|


on an NVIDIA Jetson Orin. Latency is measured following VLA-Cache. For VLA-Cache-based experiments, we use eager LlamaAttention (Touvron et al., 2023a;b) instead of FlashAttention (Dao et al., 2022); otherwise, FlashAttention is enabled by default. Hyperparameter details are provided in the Appendix A.3. 

ison, we adopt different pruning ratios. Specifically, for OpenVLA-OFT (Kim et al., 2025) and CogACT (Li et al., 2024a), we perform evaluations at pruning ratios of 25% and 40%, while for _π_ 0 _._ 5 (Intelligence et al., 2025), we evaluate at 25% and 37 _._ 5% to accommodate the architecture. The evaluation metrics primarily include task success rate(%), inference latency( _ms_ ), and FLOPs( _T_ ). 

**Benchmarks.** We evaluate EcoVLA on two simulators and real-robot tasks. The LIBERO (Liu et al., 2023a) benchmark is designed to evaluate robotic manipulation capabilities across four task suites: LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and LIBERO-Long. Each task suite examines different capabilities of VLA. The SIMPLER (Li et al., 2024b) simulation environment provides two evaluation settings, including Visual Matching and Variant Aggregation. We evaluate four tasks on the Google Robot arm: 1) 

**Implementation Details.** We follow the original settings of FastV (Chen et al., 2024) and VLA-Cache (Xu et al., 2026). Unless otherwise specified, experiments run on an NVIDIA RTX 3090 GPU, while edge-device results are obtained 

7 

**Environment-Aware Adaptive Pruning with Interleaved Inference Orchestration for Vision-Language-Action Models** 


_Figure 4._ Acceleration breakdown for dense and sparse inference. 


_Figure 5._ Trade-off between Success Rate and Latency. 

_Pick Coke Can (PickCan)_ , 2) _Move Near (MoveNear)_ , 3) _Open/Close Drawer (Drawer)_ , and 4) _Open Top Drawer and Place Apple (DrawerApple)_ . To assess EcoVLA in realworld settings, we evaluate it on two real-robot platforms, each covering three tasks, as shown in Figure 3 and Figure 7. More details are provided in the Appendix B.1. 

## **5.2. Main Results** 

**Results on OpenVLA-OFT.** Using the LIBERO benchmark, we evaluate EcoVLA on OpenVLA-OFT and show its compatibility by combining it orthogonally with acceleration techniques like FastV and VLA-Cache. Table 1 shows that EcoVLA achieves 1 _._ 26 _×_ and 1 _._ 41 _×_ speedups at 25% and 40% pruning ratios, with comparable performance at 25% sparsity and only a 2 _._ 7% drop at 40% sparsity. The robustness of EcoVLA is particularly pronounced on the pruning-sensitive LIBERO-Goal benchmark, significantly outperforming the mainstream method Wanda. Specifically, EcoVLA establishes a commanding lead of 7 _._ 4% and 12 _._ 4% over Wanda at the respective pruning ratios. Beyond this robustness, EcoVLA achieves lower latency than Wanda despite an additional pruning overhead, as I<sup>2</sup> O conceals the pruning cost within FLOPs bubbles. Combined with our hardware-efficient design, this enables EcoVLA to deliver distinctly higher wall-clock speedups over Wanda. 

Our results empirically validate the broad compatibility of EcoVLA. When combined with FastV (50% token pruning), 


_Figure 7._ Experiments on Franka Research 3 robot with XHand. 

it achieves a 2 _._ 18 _×_ speedup with a negligible 0 _._ 5% loss at 25% sparsity, and reaches a 2 _._ 35 _×_ speedup at 40%. When combined with VLA-Cache, it achieves a 1 _._ 34 _×_ speedup with a negligible 1 _._ 2% loss at 25% sparsity, and reaches a 1 _._ 5 _×_ speedup at 40%. Notably, these combinations deliver significantly higher speedups compared to the standalone baselines. While generally incurring only a slight decline in success rate, intriguingly, we observe a performance improvement in the FastV combination. We attribute this phenomenon to the regularization effect induced by our precise, adaptive model sparsification (Jin et al., 2022). 

**Results on** _π_ 0 _._ 5 **.** To demonstrate the cross-model generalizability of EcoVLA, we conduct experiments on the state-ofthe-art VLA model, _π_ 0 _._ 5, as shown in Table 2. At 25% and 37 _._ 5% pruning ratios, EcoVLA achieves 1 _._ 31 _×_ and 1 _._ 46 _×_ speedups with marginal accuracy drops of 0 _._ 2% and 1 _._ 9%, respectively. Notably, for the LIBERO-Object, we observe a 0 _._ 2% accuracy improvement at the 37 _._ 5% pruning ratio. This observation corroborates the regularization benefit discussed earlier, suggesting that selective pruning effectively filters out noise from redundant parameters. Most significantly, despite _π_ 0 _._ 5’s inherently efficient structure and low latency (81 _._ 94 ms), EcoVLA still manages to extract a substantial 1 _._ 46 _×_ acceleration. This capability to further accelerate an already fast model redefines the standards for efficient real-time deployment. 

**Results on CogACT.** We evaluate EcoVLA’s generalization on CogACT within SIMPLER, as summarized in Table 3. In the Visual Matching setting, EcoVLA achieves a 1 _._ 57 _×_ speedup at a 40% pruning ratio with a 0 _._ 3% improvement in success rate. Similarly, in the Variant Aggregation setting, it reaches a 1 _._ 6 _×_ speedup at 40% pruning while incurring a marginal accuracy reduction of 0 _._ 4%. 

8 

**Environment-Aware Adaptive Pruning with Interleaved Inference Orchestration for Vision-Language-Action Models** 

_Table 6._ Additional results on a Franka Research 3 robot with XHand. 

_Table 7._ Performance of EcoVLA under noise. 

|Method|pickup reagent<br>bottle|Success Rate _↑_<br>stack white block<br>on green|put block<br>in the basket|Latency<br>(ms)_↓_|Noise<br>Ours<br>25%|Clean<br>26_/_50|Visual<br>Noise<br>25_/_50|Lighting<br>Variation<br>24_/_50|Jitter<br>27_/_50|Occlu-<br>sion<br>21_/_50|
|---|---|---|---|---|---|---|---|---|---|---|
|_π_0_._5|27_/_50|23_/_50|25_/_50|81_._81|()||||||
|Ours (25%)|26_/_50|22_/_50|25_/_50|62_._53|||||||


_Table 8._ Activation shift between the first and middle frames under different pruning ratios. 

|Sparsity|Attention Overlap|Average Replaced|Important Heads<br>MLP Overlap<br>Average Replaced I|mportant Channels|
|---|---|---|---|---|
|25%|0_._95|1_._3_/_|24<br>0_._86<br>1159|_/_8256|
|40%|0_._92|1_._6_/_|20<br>0_._78<br>1427|_/_6605|


_Table 9._ Results on the Orin under different pruning ratios. 

|Hardware|Sparsity|Latency (ms)_↓_|Speedup_↑_|
|---|---|---|---|
|Orin|0%|702_._26|1_._00_×_|
|Orin|25%|548_._67|1_._28_×_|
|Orin|40%|491_._23|1_._43_×_|


**Results on Real Robot.** We evaluate real-world performance on a physical 7-DoF Kinova Gen3 arm controlled by _π_ 0 _._ 5. Figure 3 illustrates robot manipulation tasks performed during the experiments. As shown in Table 4, our approach delivers a 1 _._ 26 _×_ wall-clock speedup at the cost of minor performance loss, underscoring its viability for real-robot deployment. Further analysis is provided in Appendix B.2. 

## **5.3. More Results** 

**Ablation Study of Acceleration on OpenVLA-OFT.** Figure 4 details the acceleration breakdown. For dense inference, bubble scheduling, buffer optimization, and batched metrics reduce latency by 36 _._ 04 ms, 10 _._ 00 ms, and 21 _._ 14 ms respectively, yielding 148 _._ 06 ms. For sparse inference, utilizing sparse kernels, memory coalescing, and kernel fusion cuts latency by 32 _._ 63 ms, 13 _._ 49 ms, and 1 _._ 76 ms, resulting in 108 _._ 24 ms. 

**Trade-off between Performance and Latency.** As shown in Figure 5, we analyze the trade-off between success rate and latency on LIBERO-Long. While the success rate remains robust below 40% pruning, it deteriorates rapidly beyond this threshold. We observe an optimal trade-off between performance and latency at a 40% pruning ratio. 

**Overhead of Pruning Stream on OpenVLA-OFT.** The parallel pruning stream introduces overhead _δ_ , detailed in Table 5. As analyzed in Section 4.2.2, owing to the lightweight design of the EAP and its execution within FLOPs bubbles, this overhead is minimal, limited to 4.5 ms. 

**Hyperparameter Studies.** Figure 6 analyzes the impact of _α_ and _p_ on LIBERO-Long. High _α_ over-relies on historical features, causing sparsity lag, while low _α_ leads to instability. Performance peaks at _α_ = 0 _._ 7, validating our 

design. Similarly, low _p_ overlooks subtle cues, whereas high _p_ causes hypersensitivity to noise. The peak success rate at _p_ = 80% confirms EcoVLA effectively filters noise while maintaining the sensitivity required for robust operation. Additional analysis is provided in Appendix C. 

**Additional Real-Robot Results and Noise Robustness.** To assess EcoVLA’s robustness under noise, we conduct additional real-robot experiments. As shown in Figure 7, we evaluate real-world performance on a Franka Research 3 robot with an XHand, across three tasks. Table 6 shows that EcoVLA achieves a 1 _._ 31 _×_ speedup with minimal reduction in success rate. We further introduce four perturbation types to the pickup reagent bottle task to simulate visual noise. Table 7 shows that EcoVLA remains relatively robust under visual noise, lighting variation, and jitter, while occlusion introduces a more visible degradation. 

**Activation Shift Analysis.** Figure 1 shows that channel importance varies with environmental changes during VLA execution. To further quantify this observation, Table 8 reports the activation shift between important channels selected from different visual frames on LIBERO. The results show that important attention heads and MLP channels change over time, especially at higher sparsity levels, supporting the need for environment-aware adaptive pruning. The metric definition is provided in Appendix D. 

**Results on Edge Device.** To evaluate the edge-device applicability of EcoVLA, we further conduct experiments on the NVIDIA Jetson Orin platform. Table 9 shows that EcoVLA still achieves substantial speedup, demonstrating its effectiveness for resource-constrained edge deployment. Detailed hardware specifications are provided in Appendix E. 

# **6. Conclusion** 

We present EcoVLA, a training-free, plug-and-play adaptive pruning framework for VLA models that combines Environment-aware Adaptive Pruning (EAP) with Interleaved Inference Orchestration (I<sup>2</sup> O) to update sparsity online with negligible overhead. We validate EcoVLA on both real robots and high-fidelity simulators. 

9 

**Environment-Aware Adaptive Pruning with Interleaved Inference Orchestration for Vision-Language-Action Models** 

# **Acknowledgements** 

This work was supported by the Fundamental and Interdisciplinary Disciplines Breakthrough Plan of the Ministry of Education of China (No. JYB2025XDXM113) and the National Natural Science Foundation of China (No. 62332016). 

# **Impact Statement** 

This paper presents work whose goal is to advance the field of machine learning. There are many potential societal consequences of our work, none of which we feel must be specifically highlighted here. 

- Huang, Y., Ding, L., Tang, Z., Wang, T., Lin, X., Zhang, W., Ma, M., and Zhang, Y. A framework for benchmarking and aligning task-planning safety in llm-based embodied agents. _arXiv preprint arXiv:2504.14650_ , 2025. 

- Intelligence, P., Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., et al. _π_ 0 _._ 5: a vision-language-action model with openworld generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- Jabbour, J., Kim, D.-K., Smith, M., Patrikar, J., Ghosal, R., Wang, Y., Agha, A., Reddi, V. J., and Omidshafiei, S. Don’t run with scissors: Pruning breaks vla models but they can be recovered. _arXiv preprint arXiv:2510.08464_ , 2025. 

# **References** 

- An, Y., Zhao, X., Yu, T., Tang, M., and Wang, J. Fluctuationbased adaptive structured pruning for large language models. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 38, pp. 10865–10873, 2024. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Black, K., Galliker, M., and Levine, S. Real-time execution of action chunking flow policies. _Advances in Neural Information Processing Systems_ , 38:33383–33407, 2026. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al. RT-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- Chen, L., Zhao, H., Liu, T., Bai, S., Lin, J., Zhou, C., and Chang, B. An image is worth 1/2 tokens after layer 2: Plug-and-play inference acceleration for large visionlanguage models. In _European Conference on Computer Vision_ , pp. 19–35. Springer, 2024. 

- Chen, Y. and Li, X. Rlrc: Reinforcement learning-based recovery for compressed vision-language-action models. _arXiv preprint arXiv:2506.17639_ , 2025. 

- Dao, T., Fu, D., Ermon, S., Rudra, A., and Re, C.´ Flashattention: Fast and memory-efficient exact attention with io-awareness. _Advances in neural information processing systems_ , 35:16344–16359, 2022. 

- Ding, L., Shen, D., Wang, C., Wang, T., Zhang, L., and Zhang, Y. Dgr: A general graph desmoothing framework for recommendation via global and local perspectives. _arXiv preprint arXiv:2403.04287_ , 2024. 

- Jiang, W., Clemons, J., Sankaralingam, K., and Kozyrakis, C. How fast can i run my vla? demystifying vla inference performance with vla-perf. _arXiv preprint arXiv:2602.18397_ , 2026. 

- Jin, T., Carbin, M., Roy, D., Frankle, J., and Dziugaite, G. K. Pruning’s effect on generalization through the lens of training and regularization. _Advances in Neural Information Processing Systems_ , 35:37947–37961, 2022. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. OpenVLA: An open-source visionlanguage-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- Le, Q., Diao, E., Wang, Z., Wang, X., Ding, J., Yang, L., and Anwar, A. Probe pruning: Accelerating llms through dynamic pruning via model-probing. _arXiv preprint arXiv:2502.15618_ , 2025. 

- Li, Q., Liang, Y., Wang, Z., Luo, L., Chen, X., Liao, M., Wei, F., Deng, Y., Xu, S., Zhang, Y., et al. CogACT: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024a. 

- Li, X., Hsu, K., Gu, J., Pertsch, K., Mees, O., Walke, H. R., Fu, C., Lunawat, I., Sieh, I., Kirmani, S., et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024b. 

- Lin, X., Wu, Y., Yang, H., Huang, Y., Zhang, Y., Ji, J., and Zhang, Y. Improving efficiency of answer set planning with rough solutions from large language models for robotic task planning. In _Proceedings of the Thirty-Fourth International Joint Conference on Artificial Intelligence_ , pp. 4570–4578, 2025. 

10 

**Environment-Aware Adaptive Pruning with Interleaved Inference Orchestration for Vision-Language-Action Models** 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. LIBERO: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023a. 

- Liu, Z., Wang, J., Dao, T., Zhou, T., Yuan, B., Song, Z., Shrivastava, A., Zhang, C., Tian, Y., Re, C., et al. Deja Vu: Contextual sparsity for efficient llms at inference time. In _International Conference on Machine Learning_ , pp. 22137–22176. PMLR, 2023b. 

- Liu, Z., Chen, Y., Cai, H., Lin, T., Yang, S., Liu, Z., and Zhao, B. Vla-pruner: Temporal-aware dual-level visual token pruning for efficient vision-language-action inference. _arXiv preprint arXiv:2511.16449_ , 2025. 

- Ma, Y., Zhou, Y., Yang, Y., Wang, T., and Fan, H. Running vlas at real-time speed. _arXiv preprint arXiv:2510.26742_ , 2025. 

- Markidis, S., Der Chien, S. W., Laure, E., Peng, I. B., and Vetter, J. S. Nvidia tensor core programmability, performance & precision. In _2018 IEEE international parallel and distributed processing symposium workshops (IPDPSW)_ , pp. 522–531. IEEE, 2018. 

- Shinde, G., Ravi, A., Dey, E., Sakib, S., Rampure, M., and Roy, N. A survey on efficient vision-language models. _Wiley Interdisciplinary Reviews: Data Mining and Knowledge Discovery_ , 15(3):e70036, 2025. 

- Sun, M., Liu, Z., Bair, A., and Kolter, J. Z. A simple and effective pruning approach for large language models. _arXiv preprint arXiv:2306.11695_ , 2023. 

- Tang, J., Sun, Y., Zhao, Y., Yang, S., Lin, Y., Zhang, Z., Hou, J., Lu, Y., Liu, Z., and Han, S. VLASH: Real-time vlas via future-state-aware asynchronous inference. _arXiv preprint arXiv:2512.01031_ , 2025a. 

- Tang, Z., Zhang, S., Deng, J., Wang, C., You, G., Huang, Y., Lin, X., and Zhang, Y. VLMPlanner: Integrating visual language models with motion planning. In _Proceedings of the 33rd ACM International Conference on Multimedia_ , pp. 5040–5049, 2025b. 

- Tillet, P., Kung, H.-T., and Cox, D. Triton: an intermediate language and compiler for tiled neural network computations. In _Proceedings of the 3rd ACM SIGPLAN International Workshop on Machine Learning and Programming Languages_ , pp. 10–19, 2019. 

- Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M.-A., Lacroix, T., Roziere, B., Goyal, N., Hambro, E.,` Azhar, F., et al. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_ , 2023a. 

- Touvron, H., Martin, L., Stone, K., Albert, P., Almahairi, A., Babaei, Y., Bashlykov, N., Batra, S., Bhargava, P., Bhosale, S., et al. Llama 2: Open foundation and finetuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023b. 

- Wang, H., Xu, J., Pan, J., Zhou, Y., and Dai, G. Specprunevla: Accelerating vision-language-action models via action-aware self-speculative pruning. _arXiv preprint arXiv:2509.05614_ , 2025. 

- Wen, J., Zhu, Y., Li, J., Zhu, M., Tang, Z., Wu, K., Xu, Z., Liu, N., Cheng, R., Shen, C., et al. Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 

- Williams, S., Waterman, A., and Patterson, D. Roofline: an insightful visual performance model for multicore architectures. _Communications of the ACM_ , 52(4):65–76, 2009. 

- Xu, S., Wang, Y., Xia, C., Zhu, D., Huang, T., and Xu, C. Vla-cache: Efficient vision-language-action manipulation via adaptive token caching. _Advances in Neural Information Processing Systems_ , 38:164448–164473, 2026. 

- Yan, C., Zhang, W., Ning, Z., Xu, F., Tao, Z., Zhang, L., Yin, B., and Zhang, Y. Breaking model lock-in: Cost-efficient zero-shot llm routing via a universal latent space. _arXiv preprint arXiv:2601.06220_ , 2026. 

- Yang, C., Buluc¸, A., and Owens, J. D. Design principles for sparse matrix multiplication on the gpu. In _European Conference on Parallel Processing_ , pp. 672–687. Springer, 2018. 

- Yang, Y., Wang, Y., Wen, Z., Zhongwei, L., Zou, C., Zhang, Z., Wen, C., and Zhang, L. EfficientVLA: Training-free acceleration and compression for vision-language-action models. _arXiv preprint arXiv:2506.10100_ , 2025. 

- Yue, Y., Wang, Y., Kang, B., Han, Y., Wang, S., Song, S., Feng, J., and Huang, G. Deer-VLA: Dynamic inference of multimodal large language models for efficient robot execution. _Advances in Neural Information Processing Systems_ , 37:56619–56643, 2024. 

- Zhang, R., Dong, M., Zhang, Y., Heng, L., Chi, X., Dai, G., Du, L., Wang, D., Du, Y., and Zhang, S. Mole-vla: Dynamic layer-skipping vision language action model via mixture-of-layers for efficient robot manipulation. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 40, pp. 18764–18772, 2026. 

- Zhao, T. Z., Kumar, V., Levine, S., and Finn, C. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 

11 

**Environment-Aware Adaptive Pruning with Interleaved Inference Orchestration for Vision-Language-Action Models** 

# **A. Experimental Settings** 

## **A.1. VLA Model Details** 

**OpenVLA-OFT.** Derived from the OpenVLA architecture, OpenVLA-OFT incorporates an Optimized Fine-Tuning strategy that simultaneously enhances manipulation precision and computational efficiency. By adopting a continuous action space optimized via _L_ 1 regression alongside parallel decoding and action chunking mechanisms, it achieves superior throughput and success rates on the LIBERO benchmark. A key characteristic of this variant is the deployment of bidirectional attention during inference. 

_π_ 0 _._ 5 **.** _π_ 0 _._ 5 is a generalist Vision-Language-Action (VLA) model designed to achieve broad open-world generalization in mobile manipulation by leveraging a heterogeneous co-training recipe. Building upon the _π_ 0 architecture and the PaliGemma VLM backbone, _π_ 0 _._ 5 integrates diverse data sources—including cross-embodiment robot data, multimodal web data, and high-level semantic predictions—to bridge the generalization gap. The model employs a hierarchical inference mechanism where it first predicts a high-level semantic subtask (e.g., ”pick up the pillow”) based on the visual observation and global instruction, which then conditions a specialized ”action expert” to generate continuous low-level control actions via flow matching. This capability is developed through a two-stage training process that transitions from scalable discrete token pre-training to precise continuous flow-matching post-training, enabling the execution of complex, long-horizon tasks in environments completely unseen during training. 

**CogACT.** This architecture synthesizes perception and reasoning by employing DINOv2 and SigLIP for visual encoding alongside a LLaMA2-7B language backbone. To bridge the gap between high-level cognition and low-level action, CogACT utilizes a specialized Diffusion Transformer (DiT). By conditioning this diffusion-based action module on the features extracted by the VLM, the model effectively addresses the challenges of generating precise, continuous, and temporally correlated robotic trajectories. 

## **A.2. Acceleration Method Details** 

**FastV.** FastV addresses inference latency in Large Vision-Language Models (LVLMs) by mitigating visual token redundancy. The method is grounded in the observation that deep layers often exhibit an attention sink phenomenon, where visual tokens consume substantial computational resources despite receiving minimal attention weights. To counter this, FastV introduces a plug-and-play mechanism that monitors attention scores to dynamically discard low-utility visual tokens after a certain depth, thereby reducing FLOPs while preserving model accuracy. 

**VLA-Cache.** VLA-Cache is a training-free inference accelerator tailored for robotic VLA models. It exploits the observation that visual scenes in robotic tasks remain largely stable between consecutive frames, particularly in background areas. By distinguishing between static and dynamic elements, the method recycles KV-cache states for unchanged tokens while enforcing full computation for critical, task-relevant features to ensure precision. Furthermore, it incorporates an adaptive strategy that modulates the caching ratio according to layer-specific attention patterns. 

## **A.3. Implementation Details** 

For OpenVLA-OFT, we set the sensitivity parameter _p_ = 5%. Regarding temporal inertia parameter, we set _α_ = 0 _._ 7 for LIBERO-Spatial and LIBERO-Long to reduce historical reliance in dynamic spatial layouts. Conversely, for LIBERO-Object and LIBERO-Goal, we use a higher _α_ = 0 _._ 9 as these manipulation tasks feature relatively stable environments. For _π_ 0 _._ 5, given its enhanced execution stability, we set the sensitivity parameter to 80%. The temporal inertia parameter is kept fixed at 0.7. For CogACT, we set the sensitivity parameter _p_ = 5%, _α_ = 0 _._ 7. We set _λ_ to 0 _._ 99 in all experiments, following prior work (Le et al., 2025) and engineering-oriented empirical screening. 

# **B. Real-robot Setup and Analysis** 

## **B.1. Real-robot Setup** 

We conduct real-robot experiments on two platforms: a Kinova Gen3 robotic arm and a Franka robot equipped with XHand. The corresponding experimental setups are shown in Figure 8 and Figure 9. 

**Kinova Gen3** . We use two Intel RealSense D435i cameras: one providing a third-person view and the other mounted on the robot wrist. For each task, we collect 50 demonstrations. When fine-tuning the _π_ 0 _._ 5 model, we freeze the VLM backbone 

12 

**Environment-Aware Adaptive Pruning with Interleaved Inference Orchestration for Vision-Language-Action Models** 


_Figure 8._ Kinova Gen3 robot setup. 

_Figure 9._ Franka equipped with XHand robot setup. 

and apply LoRA-based adaptation, while fully fine-tuning the action expert. We use a global batch size of 32 and train the model for 10 _k_ steps on a single GPU. 

**Franka equipped with XHand** . We use three Intel RealSense D435i cameras, including a front-left view, a rear-left view, and a wrist-mounted view. For each task, we collect 100 demonstrations. The fine-tuning configuration follows the same setting as described above. 

## **B.2. Analysis on Kinova Gen3** 

During evaluation, to more thoroughly assess the model’s capability, we test on 20 randomly sampled object placements within the training range, re-randomizing the object position in every trial to probe the model’s spatial reasoning and generalization across object locations. On real-robot tasks, while achieving a 1 _._ 26 _×_ speedup, EcoVLA exhibits a minor performance drop compared to _π_ 0 _._ 5. We further observe that most failures occur when the object is placed near the boundary of the workspace. We conjecture that such edge-case placements require finer-grained spatial cues and stricter geometric constraints, making the pruned model more susceptible to representation loss and thus less robust in spatial generalization. 

# **C. Hyperparameter Analysis** 

We evaluate the influence of sensitivity parameter _p_ and temporal inertia parameter, _α_ on success rates using _π_ 0 _._ 5. 

**Impact of Sensitivity Parameter.** As shown in Figure 6 (b), we evaluate the impact of the sensitivity parameter _p_ , as it directly dictates EcoVLA’s responsiveness to environmental dynamics. At low _p_ values, EcoVLA adopts a conservative strategy, updating sparsity patterns only during drastic environmental changes, thereby overlooking subtle cues. Conversely, an excessively high _p_ induces hypersensitivity, where sensor noise or lighting fluctuations are misidentified as dynamics. This triggers redundant updates that disrupt temporal continuity. Performance peaks at _p_ = 80%, a setting that effectively filters noise while retaining sufficient sensitivity to capture physical transitions, ensuring robust operation in complex environments. 

**Impact of Temporal Inertia Parameter.** We investigate the properties of _α_ on LIBERO-Long (Figure 6 (a)), as this parameter is critical for long-horizon tasks with varying spatial layouts. High _α_ excessively weights history, causing the model to miss new critical features, whereas extremely low _α_ relies on single-frame inputs, disrupting inference stability. Performance peaks at 87 _._ 0% with an intermediate _α_ , validating our Temporal Consistency Pruning strategy. This confirms that EcoVLA effectively filters high-frequency noise while maintaining sensitivity to environmental dynamics. 

# **D. Details of Activation Shift Analysis** 

We quantify activation shift by measuring the overlap between important channels selected from different visual frames. Let _Ct_<sup>(</sup><sup>_K_)</sup> denote the set of top- _K_ important components at frame _t_ , where the components can be either attention heads or MLP 

13 

**Environment-Aware Adaptive Pruning with Interleaved Inference Orchestration for Vision-Language-Action Models** 

channels. Given two frames _t_ 1 and _t_ 2, we define their overlap as 


A higher overlap indicates that the same components remain important across frames, while a lower overlap suggests stronger temporal activation shift. We additionally report the number of replaced important components, computed as 


In our analysis, we compare the important components identified from the first frame and the middle frame across different tasks, and report the average overlap rate. This provides a direct measurement of whether the important attention heads and MLP channels remain temporally stable during VLA inference. 

# **E. Detailed hardware specifications** 

We conduct edge-device experiments on an NVIDIA Jetson AGX Orin Developer Kit. The device runs Ubuntu 22.04.5 LTS with Linux kernel 5.15.148-tegra on an aarch64 platform. The L4T release is R36.4.3. The device is configured under the 50W power mode, and CUDA compilation tools are version 12.1. 

_Table 10._ Hardware and software specifications of the edge device. 

|Item|Specification|
|---|---|
|Device|NVIDIA Jetson AGX Orin Developer Kit|
|Architecture|aarch64|
|Operating system|Ubuntu 22.04.5 LTS|
|Kernel|Linux 5.15.148-tegra|
|L4T version|R36.4.3|
|Memory|61 GiB|
|Power mode|50W mode|
|CUDA version|12.1, V12.1.66|


14 

