---
title: "Learning to Accelerate Vision-Language-Action Models through Adaptive Visual Token Caching"
date: "2026-01-31"
authors: "Yujie Wei; Jiahan Fan; Jiyu Guo; Ruichen Zhen; Rui Shao; Xiu Su"
url: https://arxiv.org/abs/2602.00686
pdf: https://arxiv.org/pdf/2602.00686
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.00686)** / [論文ページ](https://arxiv.org/abs/2602.00686)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Learning to Accelerate Vision-Language-Action Models through Adaptive Visual Token Caching** 

Yujie Wei<sup>1*</sup> Jiahan Fan<sup>2*</sup> Jiyu Guo<sup>2</sup> Ruichen Zhen<sup>3</sup> Rui Shao<sup>2</sup> Xiu Su<sup>4</sup> Zeke Xie<sup>5</sup> Hongxun Yao<sup>1</sup> Shuo Yang<sup>2�</sup> 

1Harbin Institute of Technology 2Harbin Institute of Technology, Shenzhen 3Meituan Academy of Robotics Shenzhen, Meituan 

2Harbin Institute of Technology, Shenzhen 

4Central South University 5HKUST(GZ) 

## **Abstract** 

_Vision-Language-Action (VLA) models have demonstrated remarkable generalization capabilities in robotic manipulation tasks, yet their substantial computational overhead remains a critical obstacle to real-world deployment. Improving inference efficiency is therefore essential for practical robotic applications. Existing acceleration methods often rely on heuristic or static strategies—such as rulebased token caching or pruning—that are decoupled from task objectives and fail to adapt to dynamic scene changes. In this work, we reformulate inference acceleration as a learnable policy optimization problem and propose a novel framework that integrates a dynamic, task-aware decisionmaking process directly into the VLA model. At its core are two lightweight, cooperative modules: a Cached Token Selector, which determines which tokens should be reused, and a Cache Ratio Predictor, which controls how many tokens to reuse. Training these modules is non-trivial due to their discrete decisions. We address this by adopting a differentiable relaxation that allows gradient-based end-to-end optimization. Extensive experiments on the LIBERO and SIMPLER benchmarks, as well as real-robot evaluations, show that our method achieves a 1.76× wall-clock inference speedup while simultaneously improving the average success rate by 1.9 percentage points (from 75.0% to 76.9%) on LIBERO and by 5.0 percentage points on real-world tasks, significantly outperforming existing baselines. This work highlights the potential of learning task-aware computational allocation policies, paving the way for VLA models that are both powerful and efficient.Code is available at GitHub._ 

## **1. Introduction** 

Large Vision-Language-Action (VLA) models have recently shown remarkable progress in unifying perception, 

> * Equal Contribution 

> � Corresponding Author: shuoyang@hit.edu.cn 


Figure 1. Our learnable caching (LAC) outperforms rule-based baselines in both efficiency and performance. **(a)** Rule-based selectors are decoupled from the task objective. They often rely on proxies, but _where the model attends is not necessarily what the task requires_ . This leads to suboptimal, task-agnostic caching (20% cache ratio). **(b)** Our selector is optimized with direct task gradients ( _∇L_ VLA), ensuring its decisions align with actual task requirements. This enables a more aggressive adaptive caching strategy, leading to a much higher cache ratio (40%) and greater efficiency, while simultaneously improving the success rate. 

reasoning, and control for embodied intelligence [4, 9, 15, 17, 20, 53, 55–57]. By coupling large-scale multimodal pretraining with autoregressive action decoding, models such as RT-2 [57], PaLM-E [9], and OpenVLA [17] enable robots to interpret open-ended language commands and perform complex manipulation tasks. However, deploying such models in real-world robotic systems remains challenging due to their high computational overhead, which conflicts with the low-latency requirements of real-time 

1 

control, hindering widespread adoption. 

A major inefficiency arises from redundant computation across consecutive frames, as VLA models reprocess the entire visual input at every step, even when most background regions remain static. Existing acceleration methods attempt to mitigate this by caching or pruning visual tokens, but they typically rely on fixed, rule-based heuristics [7, 48, 52]. As illustrated in Figure 1 (a), these rule-based selectors are fundamentally decoupled from the downstream task objective. This means their decisions are based on proxies, such as attention scores or visual saliency, which often fail to capture true task-relevance. A policy might waste computation on visually distracting but functionally irrelevant regions, or erroneously discard subtle but critical cues for the task. In essence, **_where the model attends is not necessarily what the task requires_** . This fundamental misalignment leads to a suboptimal trade-off between speed and accuracy, limiting both the potential efficiency gains and the overall reliability of the system. 

We argue that the key to efficient VLA inference lies not in manually designing better heuristics, but in learning a dynamic computation policy that is directly optimized for task success. We hypothesize that an optimal policy should learn to allocate computational resources based on scene motion and task requirements, reusing redundant information while recomputing only the most salient parts. 

Based on this insight, we propose **LAC** ( **L** earnable **A** daptive **C** aching for Vision-Language-Action models), a lightweight framework that transforms heuristic acceleration into a learnable, task-driven policy. As shown in Figure 1 (b), LAC introduces a _learnable token selector_ that receives direct feedback from the final task loss ( _∇Lvla_ ) which measures the ability of VLA models. This end-toend optimization enables the selector to make more intelligent, task-aware decisions. As a result, LAC can adopt a more aggressive caching strategy (40% cache ratio) that not only improves efficiency but also enhances task performance, achieving a higher success rate. At its core, LAC features two cooperative modules: the _Cached Token Selector_ , which learns token-level dynamic saliency, and the _Cache Ratio Predictor_ , which determines the overall reuse budget. To effectively assess scene dynamics, these modules leverage computationally lightweight optical flow. This approach provides a direct, pixel-level signal of motion, which is crucial for identifying which visual tokens correspond to moving objects like the robot’s gripper or manipulated items. Crucially, we opt for this direct motion signal over language-based guidance, as the latter would likely necessitate a larger model and incur additional computational overhead, running counter to our goal of efficiency. Both are trained jointly through a task-driven policy learning framework, ensuring that every computation decision contributes directly to the final goal. 

Before delving into the details, we summarize our contributions as follows: 

- We propose **LAC** , the first learnable adaptive caching framework that transforms heuristic acceleration into an end-to-end trainable policy for VLA models. 

- We design two lightweight and cooperative decision modules—the _Cached Token Selector_ , which identifies which visual tokens should be recomputed or reused, and the _Cache Ratio Predictor_ , which determines how many tokens to reuse based on scene-level motion entropy. Together, they enable fine-grained and adaptive token reuse for efficient VLA inference. 

- Extensive experiments on LIBERO, SIMPLER, and realworld robotic platforms demonstrate that LAC achieves up to a 1.76× wall-clock acceleration while simultaneously improving task performance, outperforming existing rule-based pruning and caching baselines. 

## **2. Related Work** 

**Vision-Language-Action Models.** Vision-LanguageAction (VLA) models represent a significant advancement in robotics, building upon the multimodal reasoning capabilities of large-scale vision-language models (VLMs) [1, 2, 8, 10, 19, 28, 36, 41]. By introducing an action modality, these models [17, 20, 23, 25, 30, 31, 37, 38, 42, 43, 56, 57] are able to perform end-to-end visuomotor control. The common paradigm involves adapting powerful VLM backbones, such as Llama [11, 40], through fine-tuning on extensive robotics datasets like Open X-Embodiment [32]. To generate actions, these models employ diverse strategies, from discretizing robot movements into languagelike tokens [17, 57] to integrating specialized decoders like diffusion action transformers [20, 44, 46] or flow models [4, 15]. This has led to successes in complex manipulation tasks [14, 54], but the substantial computational demands of VLA models remain a critical hurdle for practical, real-time deployment in resource-constrained settings. **Acceleration of VLA Models.** Prior work on accelerating VLMs often falls short for robotic applications. Strategies like token pruning [5, 7, 26, 47, 52] and merging [6, 12, 24, 35] are ill-suited for robotics. They fail to exploit critical temporal redundancy across video frames. Moreover, their pruning logic can harm the spatial fidelity required for manipulation and introduces computational overhead that often outweighs the benefits for short robotic action sequences. VLA-specific approaches, including architectural optimizations [29, 45], dynamic scheduling [21, 49, 51], and quantization [33], demand costly retraining or rely on heuristic-based rules. High-frequency control methods [18, 34, 50] also leave the vision processing bottleneck largely unaddressed. The most related approach, VLACache [48], introduces key-value caching across timesteps but employs a static, rule-based policy that cannot effec- 

2 


Figure 2. **Overview of the two-stage training framework for LAC. Stage I: Initialization.** The Cached Token Selector is initially pretrained to align with the VLA’s internal attention map, providing a stable and informative initialization. **Stage II: Joint Optimization.** Following this, the Cached Token Selector and Cache Ratio Predictor are jointly optimized with the VLA backbone held frozen. The selector learns token-level saliency for dynamic reuse, while the predictor estimates the optimal cache ratio from a discrete set. Gradients from the task loss _L_ VLA are backpropagated through both modules via the differentiable selection mechanism, enabling end-to-end policy learning for adaptive computation. 

tively adapt to changing scene dynamics. 

In contrast, our proposed LAC transforms acceleration into a learnable, task-oriented policy, using jointly optimized modules to create a fine-grained, adaptive caching strategy that dynamically and effectively balances computation and accuracy. 

## **3. Method** 

To address the high computational cost faced by VisionLanguage-Action (VLA) models in real-time decisionmaking, we propose a dynamic computation optimization framework that enables adaptive efficiency within the perception–action loop. For embodied agents, efficient perception is the foundation of low-latency and responsive control. Our approach accelerates inference by intelligently reusing redundant visual information rather than performing uniform, dense computation for every incoming frame. The core of the method lies in two lightweight, cooperative modules that dynamically determine token-wise processing strategies based on scene content. The following sections detail the overall framework, key components, and the twostage training procedure. 

### **3.1. Overall Framework** 

To enhance the inference efficiency of VLA models, we propose a learnable adaptive caching framework that dynamically decides which visual tokens to recompute and which to reuse from a cache. This adaptive computation strategy aims to reduce computational overhead while simultaneously improving task performance. A high-level overview of our proposed method is illustrated in Figure 2. 

At the heart of our framework are two lightweight, cooperative modules: the _Cached Token Selector_ and the _Cache Ratio Predictor_ . The Cached Token Selector is responsible for generating token-level saliency scores to identify which visual information is critical and requires recomputation. Concurrently, the Cache Ratio Predictor assesses the overall scene dynamics to determine an appropriate proportion of tokens to cache. These two modules operate as a plug-and-play addition, guiding the computational flow for a pre-trained and frozen VLA backbone, thereby preserving its powerful learned representations. 

To train these decision-making modules effectively, we devise a two-stage training procedure. In the first stage, _Initialization_ , we train the Cached Token Selector to mimic the attention distribution of the expert VLA model. This provides the selector with a strong initial policy for identifying salient regions. In the second stage, _Joint Optimization_ , we 

3 

fine-tune the selector and train the Cache Ratio Predictor end-to-end. The optimization objective in this stage is the final task performance, ensuring that the learned caching policy is directly aligned with the ultimate goal. 

### **3.2. Preliminaries: KV Caching for Efficiency** 

In autoregressive Transformer models, Key-Value (KV) caching is a standard technique to accelerate inference by reusing key ( **K** ) and value ( **V** ) representations across decoding steps. Given an input sequence **X** = [ _x_ 1 _, x_ 2 _, . . . , xT_ ], the self-attention mechanism computes 


During inference, only the new token’s **k** new and **v** new are computed and appended to the cache as follows: 


This incremental update avoids recomputation of historical states, significantly improving decoding efficiency. 

While KV caching works well for language decoding within a single context window, it remains limited for Vision-Language-Action (VLA) models. In robotic control, consecutive frames are highly redundant, yet current VLA models typically re-encode full visual inputs at every step, wasting computation and increasing latency. 

This inefficiency motivates our work: most static regions need not be recomputed each timestep. By selectively updating only salient visual tokens and reusing cached representations for redundant ones, the model can achieve efficiency gains without sacrificing perception or control accuracy. Building on this intuition, our method learns an adaptive caching policy that dynamically decides _which_ and _how many_ to recompute, as detailed in the following sections. 

### **3.3. Dynamic Token Caching Modules** 

At the core of our framework are two lightweight, cooperative modules: the _Cached Token Selector_ and the _Cache Ratio Predictor_ . To capture scene dynamics, they leverage a motion-aware representation _Vt_ = [ _It_ ; _Ot_ ], formed by concatenating the visual frame _It_ and the optical flow _Ot_ . We compute _Ot_ with a lightweight RAFT-small [39] model, as it provides a direct and efficient motion signal, avoiding the higher computational overhead associated with using language for guidance. These modules jointly decide _which_ visual tokens to recompute and _how many_ to reuse from the cache. For an input token sequence _Xt_ = _{x_<sup>(1)</sup> _t_<sup>_, . . . , x_(</sup> _t_<sup>_N_)</sup> _}_ , they operate on _Vt_ to produce a binary mask _Mt ∈{_ 0 _,_ 1 _}_<sup>_N_</sup> that guides the per-token computation. 

#### **3.3.1. Cached Token Selector** 

The Cached Token Selector is a function _f_ sel with parameters _θ_ sel, responsible for assessing token-level importance. Given the motion-aware input _Vt_ , it generates a vector of saliency scores _St_ : 


where _St_ = _{s_<sup>(1)</sup> _t_<sup>_, . . . , s_(</sup> _t_<sup>_N_)</sup> _}_ and _s_<sup>(</sup> _t_<sup>_i_)</sup> is a continuous value in the range [0 _,_ 1]. A higher score _s_<sup>(</sup> _t_<sup>_i_)</sup> indicates that token _x_<sup>(</sup> _t_<sup>_i_)’sinformationiscriticalforthecurrent</sup> timestep—perhaps due to manipulator movement or object interaction—and should accordingly be recomputed. Conversely, tokens with lower scores are identified as candidates for caching. To ensure minimal computational overhead, _f_ sel is implemented as a small and efficient convolutional neural network (CNN). 

#### **3.3.2. Cache Ratio Predictor** 

While the selector provides a relative ranking, the Cache Ratio Predictor determines the overall computational budget. This module, _f_ pred( _·_ ; _θ_ pred), also assesses global scene dynamics using the input _Vt_ to select an appropriate cache ratio from a discrete set _R_ = _{r_ 1 _, . . . , rC}_ by outputing a vector of logits _Lt_ over the set _R_ : 


where _Lt_ = _{lt_<sup>(1)</sup><sup>_, . . . , l_</sup> _t_<sup>(</sup><sup>_C_)</sup> _}_ . Each logit _lt_<sup>(</sup><sup>_j_)</sup> corresponds to the model’s confidence in applying cache ratio _rj_ . During inference, the ratio with the highest logit is selected. In a static scene, the predictor is trained to select a high ratio to maximize efficiency, while in a dynamic scene, it learns to select a lower ratio to maintain high task performance. 

### **3.4. Two-Stage Training Procedure** 

Learning a discrete caching policy from scratch is unstable under sparse supervision. We address this cold-start problem with a two-stage training paradigm: we first initialize the policy by distilling expert knowledge, then fine-tune it on task objectives while keeping the pretrained VLA frozen. **Stage I: Initialization via Attention Alignment.** This stage provides the _Cached Token Selector_ with an initialization by distilling knowledge from the expert VLA. Although the VLA’s attention scores are not optimal policies, they offer a useful proxy for general visual saliency. As shown in Figure 2, the selector _f_ sel is trained to mimic the VLA’s attention map _S_ VLA by minimizing a MSE loss: 


This warm-up provides the selector with a sensible initial policy, which is crucial for stabilizing the subsequent endto-end optimization process. 

4 

**Stage II: Joint Optimization for Task Performance.** After initialization, both modules are jointly optimized to balance task accuracy and computational efficiency. To make discrete selections differentiable, we employ the Gumbel-Softmax trick with straight-through estimation (see Sec. 3.5). The total loss combines the task loss _L_ VLA with a regularization term encouraging higher cache ratios: 


where 


Here, _p_ ˜ _t_ denotes the soft probabilities from GumbelSoftmax and _rj_ the candidate cache ratios. The weight _λ_ controls the efficiency–performance trade-off. Gradients are backpropagated to update both modules. This end-toend training aligns the learned caching policy directly with the downstream control objective. 

### **3.5. Differentiable Discrete Decision Learning** 

A key challenge is that the decisions made by our modules are inherently discrete. The _Cache Ratio Predictor_ uses an arg max operation to select a ratio from a discrete set _R_ , while the _Cached Token Selector_ relies on a non-differentiable top-k operation to identify tokens for caching. These operations obstruct gradient flow from the final task loss, preventing end-to-end optimization. 

To overcome this obstacle, we introduce a differentiable policy optimization framework based on the GumbelSoftmax trick [16] combined with the Straight-Through Estimator (STE) [3]. This creates a hybrid “hard forward, soft backward” strategy: it uses deterministic discrete selections in the forward pass for efficiency, while simultaneously enabling effective gradient flow through a continuous, “soft” approximation during backpropagation. 

For the _Cache Ratio Predictor_ , we use the GumbelSoftmax trick. Given the module’s output logits _lt_ , we then generate “soft” probability vector _p_ ˜ _t_ by adding Gumbel noise with a temperature _τ_ : 


where _gj ∼_ Gumbel(0 _,_ 1). Then, in the forward pass, we perform a hard arg max to get a one-hot vector _pt_ for deterministic ratio selection: 


During backpropagation, the Straight-Through Estimator (STE) passes gradients directly to the soft probabilities _p_ ˜ _t_ . 

For the _Cached Token Selector_ , we apply a similar principle. While the forward pass uses a hard mask **M** _t_ from the ‘top-k’ operation, the backward pass constructs a differentiable “soft” mask **M**<sup>˜</sup> _t_ using a steep sigmoid function: 


where _θk_ is the score threshold for the _kt_ -th token and _τs_ is a temperature parameter. Gradients are computed with respect to this soft mask. This hybrid strategy enables our decision modules to learn _what_ and _how much_ to cache in a unified, task-oriented framework. 

### **3.6. Inference Procedure** 

Once the training process is complete, our decision modules are integrated with the frozen VLA backbone to create a highly efficient and stable inference pipeline. 

**Deterministic Decision-Making.** For stable and consistent inference, we replace the stochastic sampling from training with deterministic arg max operations. The _Cache Ratio Predictor_ selects the cache ratio _rt_ corresponding to the highest logit. Subsequently, the _Cached Token Selector_ generates a binary mask **M** _t_ by selecting the _kt_ = _N · rt_ tokens with the lowest importance scores. 

**Efficient Forward Pass.** The generated mask **M** _t_ partitions visual tokens to enable an efficient forward pass. _Active tokens_ are re-encoded to compute new Key (K) and Value (V) states, while the KV states of _cached tokens_ are directly reused from the previous timestep. This merged set of KV states is then fed to the action decoder, significantly reducing redundant computation. 

**Stochastic Recovery Mechanism.** To enhance longhorizon robustness and mitigate error accumulation from persistent caching, we employ a stochastic recovery mechanism. At each step, with a small probability _p_ recover, a fraction of “cached” tokens are randomly selected and forced to be recomputed. This low-cost refresh improves model stability without significantly impacting efficiency. 

## **4. Experiments** 

To comprehensively assess the performance and efficiency of LAC, we conduct a rigorous evaluation across both diverse simulated environments and a physical robotic platform. Our framework is flexibly integrated with two prominent open-source Vision-Language-Action (VLA) models: OpenVLA [17] and CogAct [20]. These models are subsequently benchmarked on the LIBERO [27] and SIMPLER [22] environments, respectively. 

### **4.1. Experimental Setup** 

**Compared Methods.** Given the shared architectural foundations of VLAs and Vision-Language Models (VLMs), 

5 

Table 1. **Results on the LIBERO benchmark.** Our method (LAC) simultaneously improves both performance and efficiency over all baselines. Compared to the strong OpenVLA baseline, LAC increases the average success rate by 1.9 percentage points (from 75.0% to 76.9%) while achieving a 1.76 _×_ wall-clock speedup and reducing FLOPs by 25.3%. 

|**Method**|**LIBERO**<br>**Spatial**|**LIBERO**<br>**Object**|**LIBERO**<br>**Goal**|**LIBERO**<br>**Long**|**Average**|**FLOPs(T)**_↓_|**CUDA**<br>**Time (ms)**_↓_|
|---|---|---|---|---|---|---|---|
|Baseline (OpenVLA)|84.4%|**86.6%**|75.6%|53.2%|75.0%|1.864|51.91|
|SparseVLM [52]|79.8%|67.0%|72.6%|39.4%|64.7%|1.407|83.39|
|FastV [7]|83.4%|84.0%|74.2%|51.6%|73.3%|1.864|53.28|
|VLA-Cache [48]|83.8%|85.8%|76.4%|52.8%|74.7%|**1.355**|31.83|
|**Ours (LAC)**|**85.6%**|86.2%|**76.6%**|**59.2%**|**76.9%**|1.392|**29.51**|


acceleration techniques developed for VLMs can often be adapted for VLA inference. Consequently, we apply two leading token-level acceleration techniques, SparseVLM [52] and FastV [7], to OpenVLA to serve as strong baseline comparisons on the LIBERO benchmark. 

**Evaluation Metrics.** We quantify the performance of our method using three key metrics: success rate, FLOPs, and CUDA time. Success rate measures the efficacy of task completion. On the efficiency front, FLOPs represent the theoretical computational cost, whereas CUDA time provides a practical measure of wall-clock runtime on the GPU. This combination of metrics is standard in the evaluation of VLM/VLA acceleration frameworks. 

### **4.2. Evaluation Benchmarks** 

**LIBERO.** The LIBERO benchmark [27] is structured into four specialized suites: Spatial, Object, Goal, and Long, each specifically designed to probe a distinct dimension of manipulation generalization. To maintain consistency and ensure reproducibility, we adopt the standard setup of OpenVLA [17], employing its officially provided model weights. Each suite consists of ten subtasks, and final performance is averaged over multiple trials. 

**SIMPLER.** The SIMPLER simulator [22] features two primary configurations: Visual Matching and Variant Aggregation. In line with the methodology of CogAct [20], we evaluate our method on a Google robot arm across four distinct manipulation tasks within both settings. By using CogAct as our base model, we test the generalizability of LAC to VLA models with diverse action decoding heads and under varied simulation conditions. 

**Real-world Robot Setting** We extend our evaluation to a physical Franka manipulator to assess performance under real-world conditions, including perception noise and actuation latency. For these experiments, we fine-tune the OpenVLA base model with LoRA [13]. The evaluation is conducted on four manipulation tasks: KnockCrisp, PickMango, CoverBanana, and KnockBottle. 

### **4.3. Results on Simulation Environments** 

**Main Results on LIBERO.** Table 1 summarizes our main results on the LIBERO benchmark. Our method achieves a 1.76× wall-clock speedup and improves the average success rate by 1.9 percentage points. Notably, baselines such as SparseVLM show increased latency despite lower theoretical FLOPs. Their pruning logic introduces overhead that outweighs the benefits for the short action sequences in robotics, and can also harm the spatial fidelity required for manipulation tasks. These results confirm that LAC delivers substantial acceleration for VLA models while simultaneously enhancing task performance and generalization. 

**Qualitative Results on LIBERO.** Figure 3 highlights the superiority of LAC’s learned computational policy. LAC’s saliency map (middle row) correctly identifies the moving gripper as the most critical region, ensuring it is always recomputed while the static background is efficiently cached (orange). Conversely, the rule-based method (top row) makes a critical error: its task-agnostic heuristic caches the target basket simply because it is initially static. This decision deprives the model of essential visual updates for the upcoming interaction, causing the policy to fail as the robot arm gets stuck at the basket’s rim, unable to find the correct placement. LAC’s policy, guided by the task objective, avoids this failure, and its stability is further enhanced by stochastic recovered tokens (green). The figure clearly illustrates that a learned policy is essential for selectively recomputing salient information, unlike rigid heuristics that can discard vital context. 

**Effect of Token Reusing Ratio.** Figure 4 compares methods under different token reusing or pruning rates. As the reuse ratio increases, LAC maintains stable performance, whereas pruning-based methods (e.g., SparseVLM) exhibit steep drops in success rate. Moreover, our CUDA inference time remains consistently lower, indicating genuine wallclock efficiency rather than theoretical FLOPs reduction. 

**Ablation Studies.** We ablate LAC by progressively enabling its three core components (Table 2). Starting with the Token Selector alone achieves a 82 _._ 2% success rate, showing that learning token-level saliency already 

6 


Figure 3. **Qualitative visualization of learned vs. rule-based caching.** LAC’s policy (bottom) uses a learned saliency map to focus computation on the moving gripper while caching the static background (orange). In contrast, the rule-based method (top) detrimentally caches the static target basket, a task-agnostic error that could lead to task failure. This demonstrates the superiority of LAC’s learned approach, which is further stabilized by recovered tokens (green). 


Figure 4. **Effect of Token Reusing/Pruning Ratio on LIBEROSpatial.** Comparison of different methods under varying token reusing (or pruning) ratios. **Left:** Task success rate. **Right:** CUDA inference time. Our LAC maintains consistently high performance as the reuse ratio increases, while pruning-based methods such as SparseVLM degrade rapidly. In addition, LAC achieves the lowest CUDA latency across all settings, confirming its genuine wall-clock acceleration. 

Table 2. Ablation on key components. Each row incrementally adds one module. 

|**Method**|**Success (%)**|**FLOPs(T)**_↓_|**Time (ms)**_↓_|
|---|---|---|---|
|Selector only|82.20|1.283|28.48|
|+ Reuse Predictor|83.40|1.325|29.04|
|+ Recovery (Full)|**85.60**|1.377|29.32|


captures essential visuomotor cues for efficient reason- 

ing. Adding the Reuse Predictor improves performance to 83.4%(+1.2points). The slight increase in FLOPs and time reflects its learned strategy: it adaptively reduces the cache ratio during critical moments to ensure task success. This demonstrates a successful trade-off, sacrificing a small amount of speed for a notable gain in robustness. This indicates that adaptive, scene-level reuse budgeting is effective. Finally, introducing the stochastic recovery mechanism yields the full model performance of 85 _._ 6% (+2 _._ 2 points over the previous variant), which enhances robustness and consistency across diverse task settings. These results verify that each component contributes progressively to efficiency–accuracy balance, forming a cohesive and complementary acceleration framework. 

**Main Results on SIMPLER.** As shown in Table 3, our method achieves comparable or even better success rates than CogAct while significantly reducing computational cost. Specifically, our approach achieves an average success rate of 75.5% in the _Visual Matching_ setting (CogAct: 74.8%) and 63.0% in the more challenging _Variant Aggregation_ setting (CogAct: 61.3%). Furthermore, the efficiency improvements are substantial: our method reduces FLOPs by 17.4% (1.827 _→_ 1.509) and achieves a 1.42 _×_ speedup in inference time (53.92 ms _→_ 37.86 ms). These results highlight the strong portability of our approach, demonstrating its ability to serve as a general and architecture-agnostic acceleration strategy for VLA models with different action decoders (e.g., diffusion-based). 

7 

Table 3. Results on the SIMPLER benchmark [22] using CogAct [20] as the base model. Best results in each block are **bolded** . 

|**SIMPLER**|**Method**|**PickCan**|**MoveNear**|**Drawer**|**DrawerApple**|**Average**|**FLOPs(T)**_↓_|**CUDA**<br>**Time (ms)**_↓_|
|---|---|---|---|---|---|---|---|---|
|**Visual**|Baseline (CogAct)|91.3%|**85.0%**|71.8%|50.9%|74.8%|1.847|54.29|
|**Matching**|VLA-Cache<br>**Ours (LAC)**|92.0%<br>**92.3%**|83.3%<br>84.2%|70.5%<br>**72.7%**|51.6%<br>**52.8%**|74.4%<br>**75.5%**|**1.496**<br>1.511|39.63<br>**37.82**|
|**Variant**|Baseline (CogAct)|89.6%|80.8%|28.3%|46.6%|61.3%|1.807|53.54|
|**Areation**|VLA-Cache|91.7%|79.3%|**32.5%**|45.8%|62.3%|**1.493**|39.11|
|**ggg**|**Ours (LAC)**|**92.1%**|**81.5%**|31.2%|**47.1%**|**63.0%**|1.506|**37.90**|


Table 4. Real-world robotic manipulation results on four tasks. 

|**Method**|**KnockCrisp**|**PickMango**|**CoverBanana**|**KnockBottle**|**Average**|**FLOPs(T)**_↓_|**CUDA**<br>**Time (ms)**_↓_|
|---|---|---|---|---|---|---|---|
|Baseline (OpenVLA)|48.0%|**16.0%**|**24.0%**|44.0%|33.0%|1.893|37.38|
|VLA-Cache|48.0%|12.0%|20.0%|40.0%|30.0%|**1.534**|33.36|
|**Ours (LAC)**|**52.0%**|12.0%|**24.0%**|**64.0%**|**38.0%**|1.569|**32.47**|


Figure 5. Qualitative visualization of our learned policy (LAC) on a real-world manipulation task. The Token Saliency map (middle row) demonstrates that the model correctly identifies the moving end-effector and its immediate interaction space as the most critical regions. Consequently, the Cache Mask (bottom row) shows an efficient policy where static background elements are cached, focusing computation only on task-relevant dynamics. Visualizations for two other tasks can be found in the Appendix. 

### **4.4. Results on Real Robot** 

We validate our approach on a physical robot across four manipulation tasks, with quantitative results detailed in Table 4. Our method demonstrates superior performance, improving the average success rate by 5.0% over the baseline while reducing FLOPs and inference latency. 

To provide qualitative insight into these results, Figure 5 visualizes the behavior of our learned policy. The Token Saliency map (middle row) confirms that our model learns to dynamically focus computation on critical, task-relevant regions—namely the robot’s end-effector and its immediate interaction space. Consequently, as shown in the Cache 

Mask (bottom row), this learned saliency translates directly into an efficient caching strategy: static background elements are reused, while only the salient, moving regions are recomputed. This ability to intelligently ignore visual distractions not only explains the computational gains but also contributes to greater policy robustness and higher task success rates in cluttered, real-world environments. 

## **5. Conclusion** 

This paper addresses the computational inefficiency of Vision-Language-Action (VLA) models for real-world robotics. We introduce a novel framework that transforms 

8 

inference acceleration from a heuristic-driven process into a learnable, task-oriented policy. At its core, our method, LAC, uses two lightweight, jointly optimized modules to dynamically decide which visual tokens to recompute and which to reuse from a cache. 

Extensive experiments on simulation benchmarks and a physical robot demonstrate our approach’s effectiveness. Our method, LAC, achieves up to a 1.76× inference speedup while improving task success rates, outperforming static caching and pruning methods. These results validate our core hypothesis: by learning to adaptively reuse visual information, a learnable, task-driven policy can enhance the efficiency, robustness, and overall performance of robotic control. 

## **References** 

- [1] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katherine Millican, Malcolm Reynolds, et al. Flamingo: a visual language model for few-shot learning. In _NeurIPS_ , pages 23716–23736, 2022. 2 

- [2] Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei Huang, et al. Qwen technical report. _arXiv preprint arXiv:2309.16609_ , 2023. 2 

- [3] Yoshua Bengio, Nicholas L´eonard, and Aaron Courville. Estimating or propagating gradients through stochastic neurons for conditional computation. _arXiv preprint arXiv:1308.3432_ , 2013. 5 

- [4] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Chelsea Finn, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 1, 2 

- [5] Jianjian Cao, Peng Ye, Shengze Li, Chong Yu, Yansong Tang, Jiwen Lu, and Tao Chen. MADTP: multimodal alignment-guided dynamic token pruning for accelerating vision-language transformer. In _CVPR_ , pages 15710–15719. IEEE, 2024. 2 

- [6] Qingqing Cao, Bhargavi Paranjape, and Hannaneh Hajishirzi. Pumer: Pruning and merging tokens for efficient vision language models. In _ACL_ , pages 12890–12903, 2023. 2 

- [7] Liang Chen, Haozhe Zhao, Tianyu Liu, Shuai Bai, Junyang Lin, Chang Zhou, and Baobao Chang. An image is worth 1/2 tokens after layer 2: Plug-and-play inference acceleration for large vision-language models. In _ECCV_ , pages 19–35. Springer, 2024. 2, 6 

- [8] Wenliang Dai, Junnan Li, Dongxu Li, Anthony Tiong, Junqi Zhao, Weisheng Wang, Boyang Li, Pascale N Fung, and Steven Hoi. Instructblip: Towards general-purpose visionlanguage models with instruction tuning. In _NeurIPS_ , pages 49250–49267, 2023. 2 

- [9] Danny Driess, Fei Xia, Apoorva Anand, Aakanksha Chowdhery, Wenlong Huang, et al. Palm-e: An embodied multimodal language model. In _ICML_ , pages 8469–8488. PMLR, 2023. 1 

- [10] Zhengxiao Du, Yujie Qian, Xiao Liu, Ming Ding, Jiezhong Qiu, Zhilin Yang, and Jie Tang. Glm: General language model pretraining with autoregressive blank infilling. In _ACL_ , pages 320–335, 2022. 2 

- [11] Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. The llama 3 herd of models. _arXiv preprint arXiv:2407.21783_ , 2024. 2 

- [12] Anwen Hu, Haiyang Xu, Liang Zhang, Jiabo Ye, Ming Yan, Ji Zhang, Qin Jin, Fei Huang, and Jingren Zhou. mplugdocowl2: High-resolution compressing for ocr-free multipage document understanding. In _ACL_ , pages 5817–5834, 2025. 2 

- [13] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models. In _ICLR_ , page 3, 2022. 6 

- [14] Wenlong Huang, Chen Wang, Yunzhu Li, Ruohan Zhang, and Li Fei-Fei. Rekep: Spatio-temporal reasoning of relational keypoint constraints for robotic manipulation. In _CoRL_ , pages 4573–4602. PMLR, 2024. 2 

- [15] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 1, 2 

- [16] Eric Jang, Shixiang Gu, and Ben Poole. Categorical reparameterization with gumbel-softmax. In _ICLR_ , 2017. 5 

- [17] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An opensource vision-language-action model. In _CoRL_ , pages 2679– 2713. PMLR, 2024. 1, 2, 5, 6 

- [18] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 2 

- [19] Junnan Li, Dongxu Li, Silvio Savarese, and Steven C. H. Hoi. BLIP-2: bootstrapping language-image pre-training with frozen image encoders and large language models. In _ICML_ , pages 19730–19742. PMLR, 2023. 2 

- [20] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, et al. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 1, 2, 5, 6, 8 

- [21] Wei Li, Renshan Zhang, Rui Shao, Jie He, and Liqiang Nie. Cogvla: Cognition-aligned vision-language-action model via instruction-driven routing & sparsification. _arXiv preprint arXiv:2508.21046_ , 2025. 2 

- [22] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. In _CoRL_ , pages 3705– 3728. PMLR, 2024. 5, 6, 8 

- [23] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, et al. Vision-language foundation models as effective robot imitators. In _ICLR_ . OpenReview.net, 2024. 2 

9 

- [24] Yanwei Li, Chengyao Wang, and Jiaya Jia. Llama-vid: An image is worth 2 tokens in large language models. In _ECCV_ , pages 323–340. Springer, 2024. 2 

- [25] Yi Li, Yuquan Deng, Jesse Zhang, Joel Jang, Marius Memmel, Caelan Reed Garrett, Fabio Ramos, Dieter Fox, Anqi Li, Abhishek Gupta, and Ankit Goyal. HAMSTER: hierarchical action models for open-world robot manipulation. In _ICLR_ . OpenReview.net, 2025. 2 

- [26] Haokun Lin, Haoli Bai, Zhili Liu, Lu Hou, Muyi Sun, Linqi Song, Ying Wei, and Zhenan Sun. Mope-clip: Structured pruning for efficient vision-language models with modulewise pruning error metric. In _CVPR_ , pages 27360–27370. IEEE, 2024. 2 

- [27] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. In _NeurIPS_ , pages 44776–44791, 2023. 5, 6 

- [28] Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Improved baselines with visual instruction tuning. In _CVPR_ , pages 26286–26296. IEEE, 2024. 2 

- [29] Jiaming Liu, Mengzhen Liu, Zhenyu Wang, Pengju An, et al. Robomamba: Efficient vision-language-action model for robotic reasoning and manipulation. In _NeurIPS_ , pages 40085–40110, 2024. 2 

- [30] Jiaming Liu, Hao Chen, Pengju An, Zhuoyang Liu, Renrui Zhang, Chenyang Gu, Xiaoqi Li, Ziyu Guo, Sixiang Chen, Mengzhen Liu, et al. Hybridvla: Collaborative diffusion and autoregression in a unified vision-language-action model. _arXiv preprint arXiv:2503.10631_ , 2025. 2 

- [31] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. RDT-1B: a diffusion foundation model for bimanual manipulation. In _ICLR_ . OpenReview.net, 2025. 2 

- [32] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and RT-X models : Open x-embodiment collaboration. In _ICRA_ , pages 6892– 6903. IEEE, 2024. 2 

- [33] Seongmin Park, Hyungmin Kim, Wonseok Jeon, Juyoung Yang, Byeongwook Jeon, Yoonseon Oh, and Jungwook Choi. Quantization-aware imitation-learning for resourceefficient robotic control. _arXiv preprint arXiv:2412.01034_ , 2024. 2 

- [34] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 2 

- [35] Yuzhang Shang, Mu Cai, Bingxin Xu, Yong Jae Lee, and Yan Yan. Llava-prumerge: Adaptive token reduction for efficient large multimodal models. In _ICCV_ , pages 22857–22867, 2025. 2 

- [36] Leyang Shen, Gongwei Chen, Rui Shao, Weili Guan, and Liqiang Nie. Mome: Mixture of multimodal experts for generalist multimodal large language models. In _NeurIPS_ , pages 42048–42070, 2024. 2 

- [37] Lucy Xiaoyang Shi, Brian Ichter, Michael Equi, Liyiming Ke, Karl Pertsch, Quan Vuong, James Tanner, Anna Walling, Haohuan Wang, Niccolo Fusai, et al. Hi robot: Open-ended instruction following with hierarchical visionlanguage-action models. _arXiv preprint arXiv:2502.19417_ , 2025. 2 

- [38] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An opensource generalist robot policy. In _RSS_ , 2024. 2 

- [39] Zachary Teed and Jia Deng. RAFT: recurrent all-pairs field transforms for optical flow. In _ECCV_ , pages 402–419. Springer, 2020. 4 

- [40] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. 2 

- [41] Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, et al. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. _arXiv preprint arXiv:2409.12191_ , 2024. 2 

- [42] Sicheng Wang, Sheng Liu, Weiheng Wang, Jianhua Shan, and Bin Fang. Robobert: An end-to-end multimodal robotic manipulation model. _arXiv preprint arXiv:2502.07837_ , 2025. 2 

- [43] Junjie Wen, Jinqiang Cui, Zhenjun Zhao, Ruixin Yan, Zhi Gao, Lihua Dou, and Ben M. Chen. Syreanet: A physically guided underwater image enhancement framework integrating synthetic and real images. In _ICRA_ , pages 5177–5183. IEEE, 2023. 2 

- [44] Junjie Wen, Yichen Zhu, Jinming Li, Zhibin Tang, Chaomin Shen, and Feifei Feng. Dexvla: Vision-language model with plug-in diffusion expert for general robot control. _arXiv preprint arXiv:2502.05855_ , 2025. 2 

- [45] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, et al. Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation. _IEEE RA-L_ , 2025. 2 

- [46] Junjie Wen, Yichen Zhu, Minjie Zhu, Zhibin Tang, Jinming Li, Zhongyi Zhou, Xiaoyu Liu, Chaomin Shen, Yaxin Peng, and Feifei Feng. Diffusionvla: Scaling robot foundation models via unified diffusion and autoregression. In _ICML_ , 2025. 2 

- [47] Long Xing, Qidong Huang, Xiaoyi Dong, Jiajie Lu, Pan Zhang, Yuhang Zang, Yuhang Cao, Conghui He, Jiaqi Wang, Feng Wu, et al. Pyramiddrop: Accelerating your large vision-language models via pyramid visual redundancy reduction. _arXiv preprint arXiv:2410.17247_ , 2024. 2 

- [48] Siyu Xu, Yunke Wang, Chenghao Xia, Dihao Zhu, et al. Vla-cache: Towards efficient vision-language-action model via adaptive token caching in robotic manipulation. _arXiv preprint arXiv:2502.02175_ , 2025. 2, 6 

- [49] Yang Yue, Yulin Wang, Bingyi Kang, Yizeng Han, Shenzhi Wang, Shiji Song, Jiashi Feng, and Gao Huang. Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution. In _NeurIPS_ , pages 56619–56643, 2024. 2 

10 

- [50] Jianke Zhang, Yanjiang Guo, Xiaoyu Chen, Yen-Jen Wang, Yucheng Hu, Chengming Shi, and Jianyu Chen. Hirt: Enhancing robotic control with hierarchical robot transformers. In _CoRL_ , pages 933–946. PMLR, 2024. 2 

- [51] Rongyu Zhang, Menghang Dong, Yuan Zhang, Liang Heng, et al. Mole-vla: Dynamic layer-skipping vision language action model via mixture-of-layers for efficient robot manipulation. _arXiv preprint arXiv:2503.20384_ , 2025. 2 

- [52] Yuan Zhang, Chun-Kai Fan, Junpeng Ma, Wenzhao Zheng, Tao Huang, Kuan Cheng, Denis Gudovskiy, Tomoyuki Okuno, Yohei Nakata, Kurt Keutzer, et al. Sparsevlm: Visual token sparsification for efficient vision-language model inference. _arXiv preprint arXiv:2410.04417_ , 2024. 2, 6 

- [53] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _CVPR_ , pages 1702–1713, 2025. 1 

- [54] Tony Z. Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. In _RSS_ , 2023. 2 

- [55] Yifan Zhong, Xuchuan Huang, Ruochong Li, Ceyao Zhang, Zhang Chen, Tianrui Guan, Fanlian Zeng, Ka Num Lui, Yuyao Ye, Yitao Liang, et al. Dexgraspvla: A vision-language-action framework towards general dexterous grasping. _arXiv preprint arXiv:2502.20900_ , 2025. 1 

- [56] Zhongyi Zhou, Yichen Zhu, Minjie Zhu, Junjie Wen, Ning Liu, Zhiyuan Xu, Weibin Meng, Yaxin Peng, Chaomin Shen, Feifei Feng, et al. Chatvla: Unified multimodal understanding and robot control with vision-language-action model. In _EMNLP_ , pages 5377–5395, 2025. 2 

- [57] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. RT-2: vision-language-action models transfer web knowledge to robotic control. In _CoRL_ , pages 2165–2183. PMLR, 2023. 1, 2 

11 

## **Appendix** 

## **A. Limitations** 

While LAC enables efficient adaptive inference, it presents two main limitations. First, our reliance on optical flow as a motion prior means that extreme visual conditions may affect the precision of the token selector. Second, in scenarios with rapid global visual changes or high-speed camera ego-motion, the policy will intelligently opt to recompute most tokens to preserve accuracy; consequently, the efficiency gains in such highly dynamic settings will naturally diminish compared to more stable environments. 

## **B. Implementation Details** 

This section further details the technical implementation of our Learnable Adaptive Caching (LAC) framework within the Transformer’s forward pass. At each inference step _t_ , the binary mask **M** _t_ generated by our policy dictates the selective computation process. This is realized through the following modifications to the VLA decoder’s forward pass: 

- **Position Management and Attention Masking.** An internal state array tracks which tokens, as specified by **M** _t_ , require recomputation. Tokens designated for caching preserve their positional encodings from the previous step. This is crucial as it allows the attention masks to be dynamically pruned, restricting the scope of the selfattention mechanism to the reduced set of active tokens and thus saving computation. 

- **Conditional Rotary Embedding.** To introduce fresh positional information for the current timestep, rotary embeddings are applied exclusively to the recomputed tokens. Cached tokens bypass this operation, retaining their previously encoded states and avoiding redundant processing. 

- **Dynamic Key-Value (KV) Cache Updates.** The KV cache at each Transformer layer _l_ is updated dynamically. Newly computed tokens update their respective entries with _{_ **K**<sup>_l_</sup> _t_<sup>_,_</sup><sup>**V**</sup> _t_<sup>_l}_,whilereusedtokensinherittheirvalues</sup> from the prior frame’s cache, _{_ **K**<sup>_l_</sup> _t−_ 1<sup>_,_</sup><sup>**V**</sup> _t_<sup>_l_</sup> _−_ 1<sup>_}_.Thispar-</sup> tial update strategy, which mixes new and old KV entries, yields valid attention outputs. This is enabled by the permutation-invariant nature of the Transformer architecture, which allows attention to be computed over any valid set of key-value pairs. 

This entire mechanism is fully compatible with the standard KV caching used for autoregressive decoding. The most significant computational gain is realized during the generation of the initial action token at each timestep; subsequent tokens are then decoded autoregressively without incurring additional cost. 

## **C. Formal Efficiency Analysis** 

We provide a theoretical complexity analysis to quantify the computational benefits of LAC. Let _N_ denote the number of visual tokens per frame, _D_ the embedding dimension, _L_ the number of Transformer layers, and _M_ the intermediate dimension of the Feed-Forward Network (FFN). **Policy Overhead.** The overhead of our method stems from the fixed-cost optical flow estimation (RAFT) and the lightweight CNN selector. This cost scales linearly with the input image resolution ( _H, W_ ) and is independent of the Transformer depth or sequence length: 


Since this overhead is computed only once per frame and does not scale with the model depth _L_ , it remains negligible compared to the backbone computation. 

**Baseline Computational Cost.** In a standard VLA Transformer layer, the computational cost consists of Multi-Head Self-Attention (MSA) and Feed-Forward Networks (FFN). For a sequence of _N_ tokens, the FLOPs per layer are: 


Here, 4 _ND_<sup>2</sup> accounts for QKV and output projections, 2 _N_<sup>2</sup> _D_ represents the attention score computation and aggregation, and 2 _NDM_ accounts for the two linear transformations in the FFN (projection _D → M_ and _M → D_ ). **LAC Computational Cost.** Our method processes only a subset of active tokens _N_ act = (1 _− ρ_ ) _N_ , where _ρ_ is the cache ratio. 

- **Projections & FFN:** We compute linear projections and FFNs strictly for active tokens. 

- **Attention:** Active queries ( _N_ act) attend to the full context (active + cached tokens, total _N_ ). 

- The reduced cost per layer is: 


**Theoretical FLOPs Reduction.** The reduction in FLOPs per layer is derived by subtracting the LAC cost from the baseline: 


Integrating the overhead, the total efficiency gain for the model is: 


This analysis demonstrates that LAC significantly reduces the theoretical computational complexity, at the cost of a minimal, constant policy overhead. 

12 


What action should the robot take to pick up the apple and place it in the box? 


What action should the robot take to knock down the crisp? 


Figure 6. **Qualitative visualizations of the learned policy (LAC) on real-world tasks.** The examples show the policy correctly identifying task-relevant regions for recomputation. (Top) Input image sequence. (Middle) Learned Token Saliency map. (Bottom) Resulting Cache Mask, with orange for cached tokens and green for stochastically recovered tokens. 

## **D. Additional Experiment Results** 

### **D.1. Real-World Robot Tasks** 

Figure 6 visualizes our policy’s behavior on two real-world tasks: _”pick up the apple and place it in the box”_ (left) and _”knock down the crisp”_ (right). The learned Token Saliency (middle row) demonstrates the model’s ability to effectively distinguish between important and unimportant visual regions. High saliency scores are concentrated on the robot’s end-effector and the interaction targets, while the static background is assigned low importance. Consequently, the Cache Mask (bottom row) reveals an efficient strategy: unimportant visual regions are cached (marked in orange), while the critical, high-saliency regions remain unmasked for active recomputation. Additionally, green tiles appear within the cached regions, illustrating the stochastic recovery mechanism that randomly updates a fraction of tokens to ensure robustness. 

### **D.2. LIBERO Benchmark** 

Figures 7 and 8 present additional qualitative visualizations across four diverse tasks from the LIBERO benchmark. Consistent with our real-world observations, the learned policy accurately identifies task-relevant dynamics: high saliency scores are assigned to the robot gripper and target objects, while the static environment is cached for reuse. The resulting Cache Masks in both figures confirm that LAC efficiently allocates computation by re-computing critical regions (unmasked) and retrieving the static background from the cache (orange), with occasional updates provided by stochastic recovery (green) to prevent error accumulation. 

### **D.3. Additional Ablations and Comparisons** 

To further justify our architectural decisions and training paradigm, we conduct additional ablation studies on the LIBERO benchmark. Specifically, we investigate the necessity of the Two-Stage Training strategy and the choice of input modality for the decision modules. The quantitative results are summarized in Table 5. 

|**Method Variant**|**Success Rate (%)**|
|---|---|
|w/o Stage I Initialization|79.2|
|Language-guided Policy|83.0|
|**Ours (LAC)**|**85.6**|


Table 5. **Additional Ablation Studies on LIBERO.** We compare our full method against a variant without Stage I initialization and a variant replacing optical flow with language guidance. 

**Impact of Initialization Strategy (Stage I).** Our framework employs a two-stage training pipeline where the _Cached Token Selector_ is first initialized by distilling attention scores from the frozen VLA (Stage I) before endto-end optimization. As shown in Table 5, skipping this initialization step (“w/o Stage I Initialization”) results in a performance drop to 79.2%. This confirms that learning a discrete selection policy from scratch under sparse supervision is unstable. The initialization phase provides a critical ”visual saliency prior,” ensuring the selector begins the joint optimization (Stage II) from a reasonable state rather than converging to suboptimal local minima. 

**Motion vs. Language for Adaptive Caching.** We also evaluated an alternative design where the LAC framework is conditioned on language instructions rather than optical 

13 


Figure 7. **Qualitative Results on LIBERO Benchmark (Part 1).** We visualize the behavior of LAC on the first set of manipulation tasks. (Top) Input image sequence; (Middle) Learned Token Saliency map; (Bottom) Generated Cache Mask (orange for cached, green for stochastically recovered, and unmasked regions for active). High saliency is consistently assigned to task-relevant regions like the gripper and target object, which are actively recomputed. 

flow. This variant achieves a success rate of 83.0%, underperforming our motion-based approach. Consistent with the discussion in our main text, relying on language guidance presents a dilemma between accuracy and efficiency. Effective vision-language alignment typically requires large, computationally expensive encoders. In this ablation, to maintain an inference speed comparable to LAC, we employed a lightweight language conditioning module. However, this restricted capacity limits the model’s ability to precisely align textual instructions with visual features. In contrast, optical flow provides a direct, pixel-level signal of motion that naturally captures task-relevant dynamics without the heavy computational overhead required for deep semantic processing. 

14 


Figure 8. **Qualitative Results on LIBERO Benchmark (Part 2).** Visualization on additional tasks. Similar to Part 1, the policy successfully caches the unimportant visual regions (orange) while actively re-computing the moving agents and interaction targets (shown as unmasked). Green tiles indicate tokens updated via the stochastic recovery mechanism, demonstrating the robustness of our adaptive caching strategy. 

15 

