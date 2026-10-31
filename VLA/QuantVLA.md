---
title: "QuantVLA: Scale-Calibrated Post-Training Quantization for Vision-Language-Action Models"
date: "2026-02-23"
authors: "Jingxuan Zhang; Yunta Hsieh; Zhongwei Wan; Haokun Lin; Xin Wang; Ziqi Wang"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2602.20309
pdf: https://arxiv.org/pdf/2602.20309
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.20309)** / [論文ページ](https://arxiv.org/abs/2602.20309)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。



# **QuantVLA: Scale-Calibrated Post-Training Quantization for Vision-Language-Action Models** 

**Jingxuan Zhang**<sup>1*</sup> , **Yunta Hsieh**<sup>2*</sup> , **Zhongwei Wan**<sup>1</sup> , **Haokun Lin**<sup>3</sup> , **Xin Wang**<sup>1</sup> , **Ziqi Wang**<sup>1</sup> , **Yingtie Lei**<sup>1</sup> , **Mi Zhang**<sup>1†</sup> 1The Ohio State University, 2University of Michigan, 3City University of Hong Kong mizhang.1@osu.edu 

QuantVLA Homepage Research Hub 

## **Abstract** 

## **1. Introduction** 

_Vision-language-action (VLA) models unify perception, language, and control for embodied agents but face significant challenges in practical deployment due to rapidly increasing compute and memory demands, especially as models scale to longer horizons and larger backbones. To address these bottlenecks, we introduce_ **_QuantVLA_** _, a trainingfree post-training quantization (PTQ) framework that, to our knowledge, is the first PTQ approach for VLA systems and the first to successfully quantize a diffusion transformer (DiT) action head._ **_QuantVLA_** _incorporates three scale-calibrated components: (1) a selective quantization layout that integerizes all linear layers in both the language backbone and the DiT while keeping attention projections in floating point to preserve the original operator schedule; (2)_ attention temperature matching _, a lightweight per-head scaling mechanism that stabilizes attention logits and is folded into the dequantization scales at inference; and (3)_ output head balancing _, a per-layer residual interface calibration that mitigates post-projection energy drift. The framework requires no additional training, uses only a small unlabeled calibration buffer, and supports integer kernels for low-bit weights and activations while leaving the architecture unchanged. Across representative VLA models on LIBERO,_ **_QuantVLA exceeds_** _the task success rates of full-precision baselines, achieves about_ **_70%_** _relative memory savings on the quantized components, providing a practical pathway toward scalable low-bit embodied intelligence under strict compute, memory, and power constraints._ 

> *Equal contribution 

> †Corresponding author 

Vision-Language-Action (VLA) models [53] represent an important step toward embodied multimodal intelligence. They allow robots to parse visual observations together with natural language instructions and to output executable actions. Recent progress in large pretrained language models (LLMs) [36, 42], vision-language models (VLMs) [3, 15], and Diffusion Transformer (DiT) architecture [22, 28] has turned VLA systems into a unified interface that connects perception, high-level reasoning, and low-level control. Building on these backbones, systems such as _π_ 0.5 [12], OpenVLA [14], and GR00T N1.5 [4] achieve strong performance in robotic manipulation and reasoning tasks by integrating visual understanding, language understanding, and action generation within a single policy. As embodied models grow toward foundation scale, improving their computational efficiency becomes critical for deployment on robotic platforms with limited compute and memory while operating under strict compute and memory constraints. 

However, the large model size and complex cross-modal dependencies in current VLA architectures introduce significant computational and memory overhead. Profiling studies reveal that a substantial portion of computational overhead arises not from visual perception but from downstream reasoning and control [45], where the hidden states exhibit high-dimensional structure and sequential decoding introduces substantial computational and memory overhead. This efficiency bottleneck hinders the broader adoption of pretrained VLA models in embedded and mobilerobotic environments. 

Existing work on improving the efficiency of VLA systems can be roughly grouped into two families: methods that design more efficient VLA models [33, 38, 48] and methods that build efficiency frameworks around existing policies [41, 45]. However, these optimizations act pri- 

||Lan|guage|Act|ion|Vii|Qii||
|---|---|---|---|---|---|---|---|
|Method|Attention|MLP|Attention|MLP|son|uantzaton|Training-Free|
|TinyVLA<br>|Compact Transformer|Compact Transformer|Compact DP|Compact DP||||
|EfficientVLA|Layer drop/pruning|Layer pruning|Feature cache|Feature cache|Token reuse + feature c|ache||
|VLA-Cache||||KV r|euse for static vision toke|ns||
|MoLe-VLA|Dynamic routing|Dynamic routing||||||
|QuantVLA|Full linear Attn|<br>Full linear MLP|Full linear Attn|Full linear MLP|Keep vision frozen|PTQ||


Figure 1. **Comparison of representative VLA efficiency frameworks.** (1) TinyVLA focuses on compact multimodal transformers and lightweight diffusion-policy heads for architectural efficiency; (2) EfficientVLA accelerates inference by pruning redundant language layers and reusing intermediate representations; (3) VLA-Cache improves throughput through key–value reuse and static caching of vision tokens; (4) MoLe-VLA adopts mixture-of-layers routing to dynamically skip computation in the language module; and (5) **QuantVLA** introduces a training-free PTQ framework that low-bit quantizes both language and action modules without altering the model architecture. 

marily on the vision encoder and do not directly address the efficiency or robustness of the language backbone and the diffusion-based policy head [7, 24]. In practice, the DiT action head is a major contributor to computation and memory and is tightly coupled to the language backbone, so its behavior strongly affects performance. Yet existing efficiency frameworks typically leave this component unchanged, in part because it is tightly coupled to upstream reasoning and difficult to modify without degrading stability, and instead focus on the visual front end, which means that the main opportunities for reducing the cost of reasoning and action generation remain underexploited. Besides, post-training quantization (PTQ) [25] methods such as SmoothQuant [40] and DuQuant [18] demonstrate that careful precision allocation can reduce memory use and improve efficiency, but they are primarily developed for large language or vision language models and do not capture the heterogeneous activation and precision behaviors of downstream reasoning and action modules in VLA systems. To provide a clearer overview of these acceleration paradigms, Fig. 1 summarizes representative VLA frameworks across language, action, and vision components. 

As shown in Fig. 1, most existing efficient VLA models or methods either redesign transformer and diffusion blocks or add routing and caching around an unchanged policy, while almost none operate directly on the DiT action head or treat precision allocation as a primary design choice. In particular, current frameworks keep the policy head in full precision and focus on the visual front end. This leaves an important opportunity unused: if one can apply PTQ to the highly sensitive DiT head without degrading performance, PTQ becomes a powerful tool for VLA models, since it can substantially reduce memory and bandwidth without retraining, which is especially valuable for large VLA policies that couple a language backbone with a diffusion policy head. 

Therefore, to address these gaps, we introduce **QuantVLA** , a scale-calibrated PTQ framework specifically designed for VLA models. We first analyze why the DiTbased action head is fragile under upstream quantization, 

showing that quantization-induced scale drift changes the effective logits temperature and the residual stream energy, which explains its strong sensitivity to activation changes and precision loss. Guided by this analysis, QuantVLA performs selective post-training quantization over the language and action pathways and introduces two lightweight calibration mechanisms that restore the key scales after quantization. The resulting design led QuantVLA to achieve about 70% relative memory savings on the quantized modules, while even exceeding the LIBERO [23] task success rates of the full precision baseline as shown in the middle and right panel of Fig. 1. In conclusion, our main contributions are summarized as follows: 

1. We provide the first systematic analysis of quantization sensitivity in VLA models with DiT action heads, identifying key failure modes that explain the breakdown of PTQ. 

2. We propose **QuantVLA** , the first rotation-based, training-free PTQ framework for VLA models, achieving state-of-the-art performance under low-precision inference while enabling substantial memory savings under low-precision deployment. 

## **2. Related Work** 

### **2.1. Vision-Language-Action Models** 

VLA models unify perception, reasoning, and control within a single multimodal policy. Existing systems can be grouped into several categories described below. Encoder–decoder approaches such as ALOHA and ACT [51], RT-1 [6], and HPT [37] train Transformer networks from scratch to map visual observations and robot states to actions, achieving high accuracy but limited generalization. Pretrained language or vision language models such as RT2 [56] and OpenVLA [14] represent actions as autoregressive tokens, which enables open vocabulary reasoning but weakens temporal smoothness. Diffusion-based policies address this limitation by generating continuous trajectories through multimodal denoising. Diffusion Policy [7] introduced this framework for smooth motion generation, and 

RDT-1B [24] scaled it to large diffusion transformers that transfer across skills. Video-driven and inverse kinematics models such as UniPi [9] and RoboDreamer [55] use predictive imagination to guide control through simulated motion, which improves interpretability and scalability. 

Besides, hybrid architectures that combine language reasoning and diffusion-based control have recently become dominant [13]. OPENPI _π_ 0 [5] and OPENPI _π_ 0.5 [12] unify vision and language inputs within a single diffusion transformer DiT [28], which tightly couples semantic reasoning and low level actuation, while GR00T N1.5 [4] extends this paradigm through a dual system design where a vision–language interpreter grounds semantics and a DiT trained with flow matching [22] objectives generates precise humanoid motion. These hybrid language and diffusionbased architectures point toward scalable and semantically grounded embodied intelligence. As VLA models scale to longer horizons and larger backbones, deployment becomes increasingly constrained by the downstream reasoning and action-generation stack, where the language backbone and diffusion-based policy head often dominate compute and memory. 

### **2.2. Efficient and Compact VLA Models** 

Recent work has explored efficient and compact visionlanguage-action (VLA) models that reduce deployment cost by designing lightweight architectures, smaller backbones, or specialized inference pipelines. TinyVLA [38] builds compact multimodal transformers with lightweight diffusion policy heads to achieve faster inference and improved data efficiency. SmolVLA [33] targets affordable robotics by adopting a small VLA architecture together with an asynchronous inference stack to keep control latency low. FLOWER [30] and X-VLA [52] further explore architectural simplification and alternative action formulations to improve efficiency at reduced model scales. 

These approaches achieve efficiency primarily through new model designs and training pipelines. In contrast, QuantVLA is a post-training quantization framework that preserves the original architecture and training procedure. As a result, it is orthogonal to compact VLA design and, in principle, can be composed with both large foundation VLAs and smaller efficient VLA variants as a post-training deployment step. 

### **2.3. Efficiency Frameworks for Pretrained VLAs** 

Another line of work improves the efficiency of pretrained VLA models by optimizing the inference framework without redesigning the underlying policy. EfficientVLA [45] accelerates inference by pruning redundant language layers, selecting compact visual tokens, and reusing intermediate representations. VLA-Cache [41] reduces computational overhead by detecting unchanged visual observations 

across frames and reusing cached key–value features during rollouts. MoLe-VLA [48] further introduces mixtureof-layers routing to dynamically skip non-essential computation in the language backbone. 

These methods improve runtime efficiency through pruning, routing, or caching mechanisms while keeping numerical precision unchanged. QuantVLA differs by directly operating on numerical precision and post-training deployment efficiency, and by quantizing both the language backbone and the diffusion-based action head without modifying execution order or introducing additional routing logic. Besides, recent work also explores efficient tokenization and action discretization for VLAs, such as FAST [29], BEAST [54], and OmniSAT [2], which reduce sequence length or improve token utilization. These approaches operate at the representation level and are complementary to QuantVLA, which focuses on numerical precision and posttraining deployment efficiency. 

### **2.4. Post-Training Quantization** 

Post-training quantization (PTQ) has been extensively studied as an effective approach to reduce memory usage for pre-trained models [19, 43, 44]. The basic RTN quantization formulation is summarized in Appendix A, from Eq. 18 to Eq. 21. PTQ methods can be broadly categorized into weight-only quantization [8, 10, 21, 46] and weight–activation quantization [20, 31, 39, 50]. Our work focuses on the latter, specifically on exploring ultra low-bit weight–activation quantization. For large language models (LLMs), SmoothQuant [40] performs channel-wise rescaling of activations and weights to smooth out outliers and stabilize low-bit inference in transformer layers. Rotationbased approaches [1, 11, 18, 35] further utilize orthogonal transformations to distribute outliers across activation matrices. DuQuant [18] applies dual-path transformations that combine block-orthogonal rotations with per-channel smoothing, effectively redistributing outliers and improving robustness under low-bit precision. For diffusion transformers (DiTs), SVDQuant [16] protects activation outliers by introducing low-rank residual branches, while ViDiTQ [49] employs fine-grained grouping and dynamic quantization to better adapt to activation statistics. However, directly applying these methods to VLA models remains challenging. VLA pipelines tightly couple multimodal reasoning with diffusion-based action generation within a single policy network. Scale drift across modalities and along the diffusion rollout violates the assumptions underlying existing PTQ techniques. In particular, quantization-induced scale mismatch can distort the effective attention-logits temperature and the residual-stream energy in diffusion-policy heads, which makes stable low-bit control substantially harder than unimodal transformers. A key open problem is how to design quantization schemes that remain stable 

under such tight multimodal–diffusion coupling while still achieving low-bit efficiency for VLA control. 

## **3. Method** 

### **3.1. Preliminaries on Diffusion-based VLA Models** 

We study Vision–Language–Action (VLA) systems whose action head is a Diffusion Transformer (DiT) [28, 32]. At each control step, a short history of RGB frames is embedded via a pretrained vision encoder, such as SigLIP2 [47] or DINOv2 [27], to produce image tokens. Concurrently, the natural language instruction is tokenized and embedded by a pretrained language backbone. The visual and textual tokens are projected into a shared transformer space, where attention merges perception with the instruction context to form a task-conditioned representation _F_ VL. 

The policy head, a Diffusion Transformer, is conditioned on _F_ VL, on robot proprioception, and on a diffusion timestep _t_ . It iteratively updates an action latent according to: 


After _T_ refinement steps, the final latent _x_ 0 is decoded into the action. For tokenized policies, the output is a sequence of discrete action tokens. In this formulation, the diffusion transformer denotes the architecture of the policy head. Flow matching [22] denotes the learning objective used to fit _fθ_ and views the same iterative refinement as a conditional ordinary differential equation (ODE) [34] that trains the network to predict a velocity field transporting _xt_ toward executable actions. 

### **3.2. Post-Training Quantization Setup and Emergent DiT Sensitivity** 

#### **3.2.1. DuQuant Reparameterization.** 

Among PTQ variants, DuQuant [18] is empirically the most stable under aggressive bit widths for transformer stacks. It does so via an invertible reparameterization of each linear layer that (i) applies per-channel smoothing with a diagonal matrix Λ, (ii) performs block-orthogonal rotations _R_<sup>ˆ</sup> (1) _, R_<sup>ˆ</sup> (2), and (iii) inserts a zigzag channel permutation to redistribute outliers, which preserves the original linear map and makes activations and weights more amenable to low-bit quantization. Inspired by these robustness and outlier-redistribution properties, we adopt a similar reparameterization for linear layers in VLA models to improve stability under quantization. Additional implementation details are provided in the Appendix B. 

#### **3.2.2. Challenges in Implementing Quantization for VLA** 

While the reparameterization in the previous subsection improves low-bit robustness at the layer level, deploying it to tightly coupled VLM stacks exposes two issues. First, 

quantizing the upstream language backbone perturbs intermediate representations that condition the DiT action policy, and the perturbation propagates downstream as input drift. Second, the DiT head must emit precise action tokens for real robots, which means small rounding and scale mismatches will translate into control errors. 

As clarified in Appendix C, dequantization scales control two deterministic factors in DiT, which are the effective logits temperature through _sqsk_ and the residual stream energy through _svso_ . It explains how logits and energy transfer from the language backbone to DiT when no perturbation is present. Building on this baseline, we now analyze how quantization errors propagate and accumulate. 

Building on the deterministic transfer in Appendix C, we now develop a first-order analysis of error propagation to show that the distribution reaching attention is perturbed when DuQuant is applied to the upstream language backbone and the DiT feed-forward blocks. Let _XT_ denote the teacher input and let _XQ_ = _XT_ + _ε_ up denote the input under quantization. Even if the attention weights remain in floating point, this perturbation propagates linearly. 


Define the pre-softmax logits _L_ : 


and let ∆ _L_ = _LQ − LT_ . Keeping only first-order terms yields 


where ∆ _L_ local aggregates local rounding and scale mismatch from the quantized activations that feed _Q_ and _K_ from the output projection. Let _A_ = softmax( _L_ ) and let _J_ softmax( _·_ ) denote its Jacobian. The attention update satisfies 


Now include the output head. Write the value path and the quantized output projection as 


The teacher and quantized outputs are 


A first-order expansion around the teacher gives 


Figure 2. Overview of **QuantVLA** for VLAs with a DiT-based action head. The framework is training-free and preserves the original architecture and operator schedule. It combines: (1) a selective quantization layout that integerizes all linear layers in the LLM and all MLP layers in the DiT while keeping the attention projections _Q_ , _K_ , _V_ , _O_ in floating point; (2) _Attention Temperature Matching_ (ATM), a per-head scalar _α_ that aligns teacher–student logits and is folded into dequantization scales; and (3) _Output Head Balancing_ (OHB), a per-layer scalar _β_ that matches post-projection energy at the residual interface. 

According to Eq. 8, quantization in DiT introduces two systematic drifts. First, variance changes in Q and K alter the scale of attention logits, which shifts the effective temperature of the softmax and moves attention entropy away from the teacher distribution. This temperature bias does not vanish within a single layer. It is carried forward by the attention outputs and persists across layers. Second, after multiple head concatenation and the output projection, the amplitude of the attention output exhibits a systematic change. This modifies the residual injection gain and the operating point of layer normalization. In deep DiT stacks, these two drifts accumulate through residual connections and normalization, which degrades stability and overall performance. 

### **3.3. QuantVLA Framework** 

In this section, we present **QuantVLA** , a training-free and deployment-oriented framework that preserves the original model architecture and operator schedule while addressing the two dominant sensitivity factors identified in Sec. 3.2.2. As shown in Fig. 2, QuantVLA integrates a selective quantization layout with two lightweight calibration mechanisms. As noted above, quantizing every linear layer in the LLM and the DiT head causes errors to accumulate along the attention and residual pathways. Guided by this analysis, we integerize all linear layers in the LLM and adopt a selective DiT quantization layout, while keeping the attention projections _Wq_ , _Wk_ , _Wv_ , and _Wo_ in float- 

ing point to avoid amplifying the two drifts identified in Sec. 3.2.2 since they are most sensitive to upstream distribution shifts and directly determine the stability of the softmax distribution and the residual injection. This layout mitigates the dominant sources of drift in DiT under low bit widths. However, integerizing the upstream LLM can still bias the statistics that reach the DiT head. To compensate for this cross-module drift in VLA pipelines, we introduce two lightweight calibrations, **Attention Temperature Matching (ATM)** and **Output Head Balancing (OHB)** , as shown in Fig. 2. Both are estimated from an unlabeled calibration buffer and folded into the dequantization scales, so the operator schedule and integer GEMMs remain unchanged. In QuantVLA, ATM and OHB are instantiated specifically at the language–to–action interface of VLA pipelines, where quantized language features condition the DiT head and induce the strongest scale drift. ATM uses per-head temperature scalars to align the logits distribution through _Q_ and _K_ , preventing attention from becoming overly sharp or overly flat under upstream VLA quantization. OHB uses per-layer output scalars to align the postprojection energy through _Wo_ , restoring the residual injection gain and the operating point of layer normalization in the DiT head. 

Specifically, we calibrate ATM by matching the dispersion of the teacher and quantized logits _L_ defined in Eq. 3. We estimate a scalar _α_ from a small unlabeled calibration buffer and apply it at inference time as follows 


We then confine the correction to a safe range to avoid overcooling or over-heating the attention distribution 


Next, we apply a neutrality band _ε_ to ignore negligible differences and reduce sensitivity to calibration noise 


Therefore, the quantized logits become 


We next match the post-projection energy at the residual interface to stabilize the residual injection gain and the operating point of layer normalization. The activation of the output head at the layer _l_ is 


We measure per-layer energy using RMS for the teacher and the quantized, and directly form a teacher-to-student ratio 


Similarly to ATM, we confine this factor to a safe range and apply a neutrality band 


Finally, we rescale the activation of the output head that enters the residual path 


Building on these techniques, QuantVLA combines a flexible selection of quantized linear layers to counter the sensitivities identified in Sec. 3.2.2. By integerizing all linear layers in the LLM and adopting a selective quantization layout in the DiT while keeping the attention projections in floating point, we avoid compounding errors at the most fragile interfaces. Furthermore, ATM aligns the teacher and student logits statistics to correct attention temperature drift, whereas OHB restores the residual injection gain by matching the output head energy. Crucially, ATM and OHB are realized as tiny per-head and per-layer scalars that are estimated once from an unlabeled calibration buffer 

and folded into existing dequantization scales. They introduce no new operators or activations, require no additional buffers, preserve the original operator schedule and integer GEMMs, and therefore incur no additional GEMM computation during inference. The only overhead is scalar folding performed once during calibration. Based on these steps, we stabilize the DiT action head under low bit widths without retraining. 

## **4. Experiment** 

### **4.1. Experimental Settings** 

**Model and Benchmark.** We evaluate on two state-of-theart VLA policies, OpenPI _π_ 0 _._ 5 [12] and GR00T N1.5 [4], both employing a DiT-based action head that maps fused visual–language features to action sequences. The models span complementary regimes, where _π_ 0 _._ 5 prioritizes efficient inference and GR00T N1.5 offers higher capacity and richer action modeling, and this breadth enables a robust assessment across different coupling strengths between perception and control. Evaluation uses the LIBERO [23] simulator with four task suites that target distinct capabilities: Spatial tests relational reasoning and precise placement, Object focuses on object-centric grasping and manipulation, Goal measures instruction-to-goal alignment and condition satisfaction, and Long examines temporal decomposition and control of accumulated error. We report the success rate under the standard LIBERO protocol to ensure fair comparison and reproducibility. 

**Implementation Details.** We adopt our method with a W4A8 setting. Scales are estimated from a small unlabeled calibration buffer and folded into dequantization at inference. For stability matching, the _α_ of ATM and _β_ of OHB are clipped to a safe range of _±_ 0 _._ 4 before being folded into the scales and using a neutrality band _ε_ of 0 _._ 03. All experiments are conducted on NVIDIA A100 GPUs. More details are shown in Appendix D 

### **4.2. Empirical Validation of the Selective Quantization Layout** 

As established in Sec. 3.2.2, quantization errors introduced by the upstream language backbone perturb the attention temperature and the residual energy in the DiT action head, which renders the attention projections and the residual interface particularly sensitive. To limit this crossmodule drift, we compare several layer selection schemes that quantize the LLM only, the action head only, both modules in full, or the LLM together with the DiT MLP. We evaluate these alternatives on OpenPI _π_ 0 _._ 5 and GR00T N1.5 within LIBERO, and we isolate the effect of layer choice by disabling ATM and OHB in this ablation so that we observe the pure quantization outcome. The results in 

|**Model**|**Precision**|**Layer Selection**|**Layer Nums**|||**LIBERO**<br>|||**Memory (GB)**<br>LLMDiT|
|---|---|---|---|---|---|---|---|---|---|
|||||**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|(+)|
||FP16|No Quantization|0|98.5%|99.0%|97.5%|93.5%|97.1%|4.27|
||W4A8|LLM|126|98.0%|98.5%|97.5%|92.0%|96.5%|1.58|
|_π_0.5|W4A8|DiT|126|81.5%|94.5%|71.5%|39.0%|71.6%|3.85|
||W4A8|LLM+DiT|252|86.0%|97.5%|71.5%|50.0%|76.3%|1.17|
||W4A8|LLM+DiT (MLP)|180|98.0%|97.0%|94.5%|92.0%|95.4%|1.28|
||FP16|No Quantization|0|92.0%|92.0%|86.0%|76.0%|86.5%|2.02|
||W4A8|LLM|84|86.0%|92.0%|80.0%|80.0%|84.5%|1.25|
|GR00T N1.5|W4A8|DiT|96|88.0%|80.0%|86.0%|78.0%|83.0%|1.49|
||W4A8|LLM+DiT|180|66.0%|70.0%|68.0%|76.0%|70.0%|0.74|
||W4A8|LLM+DiT (MLP)|116|90.0%|86.0%|80.0%|74.0%|82.5%|0.91|


Table 1. Selective layer-quantization results under the QuantVLA architecture without ATM/OHB calibration for _π_ 0 _._ 5 and GR00T N1.5 on LIBERO. 


Figure 3. ATM and OHB effects across attention blocks. **(Left)** shows logits standard deviation. **(Right)** shows attention output RMS after the output projection. The figure reports three configurations: the teacher model in floating point without quantization, the quantized baseline with LLM and DiT MLP integerized, and QuantVLA with ATM in the left panel or QuantVLA with OHB in the right panel, which are evaluated on the GR00T N1.5 model. 

Table 1 show a consistent pattern across models and suites, as quantizing the entire action head or the full stack leads to the largest degradation, most notably in the long-horizon task, whereas quantizing the LLM together with the DiT MLP remains closest to the baseline while retaining the memory benefits of integer computation counted over the LLM and DiT components, which aligns with our theoretical analysis in Sec. 3.2.2. Consequently, we fix the layer selection to all linear layers in the LLM and the MLP blocks in the DiT while leaving _Q_ , _K_ , _V_ , and _O_ in floating point for all subsequent experiments. 

### **4.3. Effect of ATM and OHB Calibration** 

In this section, we empirically verify that ATM and OHB restore logits statistics and output energy. Fig. 3 evaluates three configurations on GR00T N1.5: the floating-point teacher, QuantVLA without ATM and OHB calibration, and QuantVLA with ATM in the left panel or with OHB in the right panel. In the left panel, ATM reduces the mismatch in logits Std and moves each attention block toward the teacher, which shows that temperature shifts caused by 

quantization are corrected. In the right panel, OHB aligns the attention output RMS after the output projection with the teacher, which mitigates residual-stream energy drift and stabilizes the downstream residual path. Across blocks, the calibrated curves consistently narrow the gap to the teacher, especially in deeper layers, confirming that ATM corrects logits statistics and OHB corrects output energy. We therefore include both components in all subsequent experiments. 

### **4.4. QuantVLA Results in LIBERO Simulation** 

**Main Results on LIBERO.** Table 2 reports the performance of different quantization techniques on OpenPI _π_ 0 _._ 5 and GR00T N1.5 within the LIBERO simulator. We compare two representative approaches: DuQuant and the proposed QuantVLA framework. DuQuant can be successfully applied to both the LLM and the DiT, but its task accuracy drops significantly under this configuration, for example, on _π_ 0 _._ 5 the average success rate falls to 76.3%, and on GR00T N1.5 it reaches 70%. These outcomes suggest that methods designed for unimodal or loosely coupled set- 

|**Model**|**Precision**|||**LIBERO**|||**Memory (GB)**<br>|**Relative**<br>|
|---|---|---|---|---|---|---|---|---|
|||**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|**(LLM+DiT)**|**Savings**|
|_π_0.5|FP16|98.5%|99.0%|97.5%|93.5%|97.1%|4.27|0.0%|
|+DuQuant(LLM+DiT)|W4A8|86.0%|97.5%|71.5%|50.0%|76.3%|1.17|72.6%|
|+QuantVLA(LLM)|W4A8|98.5%|99.0%|96.5%|96.5%|**97.6%**|1.58|63.0%|
|+QuantVLA|W4A8|98.5%|98.0%|98.0%|96.0%|**97.6%**|1.28|70.0%|
|GR00T N1.5|FP16|92.0%|92.0%|86.0%|76.0%|86.5%|2.02|0.0%|
|+DuQuant(LLM+DiT)|W4A8|66.0%|70.0%|68.0%|76.0%|70.0%|0.74|63.4%|
|+QuantVLA(LLM)|W4A8|96.0%|94.0%|92.0%|66.0%|87.0%|1.25|38.1%|
|+QuantVLA|W4A8|96.0%|92.0%|90.0%|74.0%|**88.0%**|0.91|55.0%|


Table 2. Results on LIBERO for different QuantVLA variants on OpenPI _π_ 0 _._ 5 and GR00T N1.5. The table reports success rates (%) across four LIBERO tasks, memory (GB), and the relative memory savings versus each model’s baseline. 

tings do not transfer to highly coupled VLA systems. In contrast, QuantVLA is the first framework to achieve effective PTQ on VLA models. By combining selective layer quantization with ATM and OHB calibration, QuantVLA not only maintains stable performance but also surpasses the baseline on several task suites. On _π_ 0 _._ 5, QuantVLA attains an average success rate of 97.6%, matching or exceeding the baseline while reducing memory usage from 4.27 GB to 1.28 GB. Similarly, on GR00T N1.5, QuantVLA achieves 88.0% average accuracy with memory reduced from 2.02 GB to 0.91 GB. These results demonstrate that the proposed design effectively mitigates distribution drift caused by quantization in both the language backbone and especially in the DiT action head, which, to our knowledge, has not been quantized in prior VLA work, **thereby delivering state-of-the-art PTQ for VLA models without any retraining.** Additional comparisons with SmoothQuant under different quantization precision settings are provided in Appendix E. Beyond LIBERO, we also further include an extended evaluation on the Simpler [17] manipulation benchmark to assess cross-task robustness. Detailed results are provided in Appendix F. 

**Efficiency of QuantVLA.** QuantVLA achieves substantial memory reduction as shown in Fig. 4. These results confirm that the proposed selective quantization layout and lightweight calibration preserve accuracy while significantly reducing memory consumption. The reduced memory footprint makes QuantVLA particularly suitable for long-horizon policy generation and deployment under tight memory budgets. In practical scenarios, these gains allow the model to process longer temporal contexts, extend input horizons, or run multiple control policies in parallel within the same hardware budget, thereby enabling broader scalability in VLA applications. 

**Robustness and Generalization Analysis.** We further evaluate QuantVLA under two complementary settings to assess robustness and generalization. Table 3 examines the 


Figure 4. Memory saving of QuantVLA over the baseline on OpenPI _π_ 0 _._ 5 and GR00T N1.5. 

|**Model**|**Precision**||**L**|**IBERO**|||
|---|---|---|---|---|---|---|
|||**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
|_π_0.5|FP16|98.5%|99.0%|97.5%|93.5%|97.1%|
|_π_0.5|W4A8|98.5%|98.0%|98.0%|96.0%|**97.6%**|
|+QuantVLA|W4A4|98.5%|98.5%|93.5%|90.5%|95.3%|


Table 3. LIBERO results on OpenPI _π_ 0 _._ 5 comparing FP16, W4A8, and W4A4 precision. 

effect of different quantization precisions on OpenPI _π_ 0 _._ 5, comparing the configurations FP16, W4A8, and W4A4. The results show that QuantVLA maintains strong performance even at lower bit widths, achieving 95.3% average success rate at W4A4, which demonstrates stable behavior under aggressive quantization. Table 4 evaluates GR00T N1.5 with different denoising steps, where QuantVLA consistently matches or exceeds the baseline, reaching 88.0% average success at 8 steps. These results indicate that QuantVLA preserves task accuracy across precision levels and noise conditions, confirming that the proposed calibration and selective quantization design generalizes well to various inference settings. We further evaluate QuantVLA on OpenVLA in Appendix G, which adopts a non-DiT action head, to assess applicability beyond DiT-based VLA models. 

|**Model**|**Denoising**<br>||**L**|**IBERO**|||
|---|---|---|---|---|---|---|
||**Steps**|**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
|GR00T N1.5|8|92.0%|92.0%|86.0%|76.0%|86.5%|
|GR00T N1.5|8|96.0%|92.0%|90.0%|74.0%|**88.0%**|
|+QuantVLA|16|96.0%|94.0%|84.0%|80.0%|88.5%|


Table 4. LIBERO results under different denoising steps on GR00T N1.5. 

## **5. Conclusion** 

We present QuantVLA, the first PTQ framework for VLA models that surpasses full precision baselines without any additional training. Using a selective layout, it integerizes the language backbone and the feedforward blocks of the diffusion transformer while attention projections remain in floating point. Two lightweight calibration scalars align the attention temperature and restore the output energy, thereby stabilizing low-bit inference. As a result, QuantVLA reduces memory usage and improves accuracy. Overall, QuantVLA is training-free, preserves the original architecture, and is robust across modalities, offering a practical path to low-bit deployment and laying the groundwork for future advances, lower power budgets, and reliable long-horizon generation. 

## **References** 

- [1] Saleh Ashkboos, Amirkeivan Mohtashami, Maximilian L Croci, Bo Li, Martin Jaggi, Dan Alistarh, Torsten Hoefler, and James Hensman. Quarot: Outlier-free 4-bit inference in rotated llms. _arXiv preprint arXiv:2404.00456_ , 2024. 3 

- [2] Guillaume Astruc, Nicolas Gonthier, Clement Mallet, and Loic Landrieu. Omnisat: Self-supervised modality fusion for earth observation. In _European Conference on Computer Vision_ , pages 409–427. Springer, 2024. 3 

- [3] Anas Awadalla, Irena Gao, Josh Gardner, Jack Hessel, Yusuf Hanafy, Wanrong Zhu, Kalyani Marathe, Yonatan Bitton, Samir Gadre, Shiori Sagawa, et al. Openflamingo: An opensource framework for training large autoregressive visionlanguage models. _arXiv preprint arXiv:2308.01390_ , 2023. 

   - 1 

- [4] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 1, 3, 6 

- [5] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. pi ~~0~~ : A vision-languageaction flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 3 

- [6] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. 

Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 2 

- [7] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44 (10-11):1684–1704, 2025. 2 

- [8] Peijie Dong, Lujun Li, Yuedong Zhong, Dayou Du, Ruibo Fan, Yuhan Chen, Zhenheng Tang, Qiang Wang, Wei Xue, Yike Guo, et al. Stbllm: Breaking the 1-bit barrier with structured binary llms. _arXiv preprint arXiv:2408.01803_ , 2024. 3 

- [9] Yilun Du, Sherry Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Josh Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning universal policies via text-guided video generation. _Advances in neural information processing systems_ , 36:9156–9172, 2023. 3 

- [10] Elias Frantar, Saleh Ashkboos, Torsten Hoefler, and Dan Alistarh. Gptq: Accurate post-training quantization for generative pre-trained transformers. _arXiv preprint arXiv:2210.17323_ , 2022. 3 

- [11] Xing Hu, Yuan Cheng, Dawei Yang, Zukang Xu, Zhihang Yuan, Jiangyong Yu, Chen Xu, Zhe Jiang, and Sifan Zhou. Ostquant: Refining large language model quantization with orthogonal and scaling transformations for better distribution fitting. _arXiv preprint arXiv:2501.13987_ , 2025. 3 

- [12] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0.5: a vision–language–action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 1, 3, 6 

- [13] Kento Kawaharazuka, Jihoon Oh, Jun Yamada, Ingmar Posner, and Yuke Zhu. Vision-language-action models for robotics: A review towards real-world applications. _IEEE Access_ , 2025. 3 

- [14] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 2 

- [15] Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi. Blip: Bootstrapping language-image pre-training for unified vision-language understanding and generation. In _International conference on machine learning_ , pages 12888–12900. PMLR, 2022. 1 

- [16] Muyang Li, Yujun Lin, Zhekai Zhang, Tianle Cai, Xiuyu Li, Junxian Guo, Enze Xie, Chenlin Meng, Jun-Yan Zhu, and Song Han. Svdquant: Absorbing outliers by lowrank components for 4-bit diffusion models. _arXiv preprint arXiv:2411.05007_ , 2024. 3 

- [17] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, Sergey Levine, Jiajun Wu, Chelsea Finn, Hao Su, Quan Vuong, and Ted Xiao. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 8 

- [18] Haokun Lin, Haobo Xu, Yichen Wu, Jingzhi Cui, Yingtao Zhang, Linzhan Mou, Linqi Song, Zhenan Sun, and Ying 

Wei. Duquant: Distributing outliers via dual transformation makes stronger quantized llms. _Advances in Neural Information Processing Systems_ , 37:87766–87800, 2024. 2, 3, 4 

- [19] Haokun Lin, Haobo Xu, Yichen Wu, Ziyu Guo, Renrui Zhang, Zhichao Lu, Ying Wei, Qingfu Zhang, and Zhenan Sun. Quantization meets dllms: A systematic study of post-training quantization for diffusion llms. _arXiv preprint arXiv:2508.14896_ , 2025. 3 

- [20] Haokun Lin, Xinle Jia, Shaozhen Liu, Shujun Xia, Weitao Huang, Haobo Xu, Junyang Li, Yicheng Xiao, Xingrun Xing, Ziyu Guo, et al. Efficient diffusion language models: A comprehensive survey. _Authorea Preprints_ , 2026. 3 

- [21] Ji Lin, Jiaming Tang, Haotian Tang, Shang Yang, Wei-Ming Chen, Wei-Chen Wang, Guangxuan Xiao, Xingyu Dang, Chuang Gan, and Song Han. Awq: Activation-aware weight quantization for on-device llm compression and acceleration. _Proceedings of machine learning and systems_ , 6:87– 100, 2024. 3 

- [22] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 1, 3, 4 

- [23] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 2, 6 

- [24] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 2, 3 

- [25] Zhenhua Liu, Yunhe Wang, Kai Han, Wei Zhang, Siwei Ma, and Wen Gao. Post-training quantization for vision transformer. _Advances in Neural Information Processing Systems_ , 34:28092–28103, 2021. 2 

- [26] Markus Nagel, Rana Ali Amjad, Mart Van Baalen, Christos Louizos, and Tijmen Blankevoort. Up or down? adaptive rounding for post-training quantization. In _International conference on machine learning_ , pages 7197–7206. PMLR, 2020. 12 

- [27] Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 4 

- [28] William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 4195–4205, 2023. 1, 3, 4 

- [29] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 3 

- [30] Moritz Reuss, Hongyi Zhou, Marcel R¨uhle, Omer<sup>¨</sup> Erdinc¸ Ya˘gmurlu, Fabian Otto, and Rudolf Lioutikov. Flower: Democratizing generalist robot policies with efficient vision-language-action flow policies. _arXiv preprint arXiv:2509.04996_ , 2025. 3 

- [31] Wenqi Shao, Mengzhao Chen, Zhaoyang Zhang, Peng Xu, Lirui Zhao, Zhiqian Li, Kaipeng Zhang, Peng Gao, Yu Qiao, and Ping Luo. Omniquant: Omnidirectionally calibrated quantization for large language models. In _The Twelfth International Conference on Learning Representations_ , 2023. 3 

- [32] Hui Shen, Jingxuan Zhang, Boning Xiong, Rui Hu, Shoufa Chen, Zhongwei Wan, Xin Wang, Yu Zhang, Zixuan Gong, Guangyin Bao, et al. Efficient diffusion models: A survey. _arXiv preprint arXiv:2502.06805_ , 2025. 4 

- [33] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, et al. Smolvla: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 1, 3 

- [34] Yang Song, Jascha Sohl-Dickstein, Diederik P Kingma, Abhishek Kumar, Stefano Ermon, and Ben Poole. Score-based generative modeling through stochastic differential equations. _arXiv preprint arXiv:2011.13456_ , 2020. 4 

- [35] Yuxuan Sun, Ruikang Liu, Haoli Bai, Han Bao, Kang Zhao, Yuening Li, Jiaxin Hu, Xianzhi Yu, Lu Hou, Chun Yuan, et al. Flatquant: Flatness matters for llm quantization. _arXiv preprint arXiv:2410.09426_ , 2024. 3 

- [36] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. 1 

- [37] Lirui Wang, Xinlei Chen, Jialiang Zhao, and Kaiming He. Scaling proprioceptive-visual learning with heterogeneous pre-trained transformers. _Advances in neural information processing systems_ , 37:124420–124450, 2024. 2 

- [38] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Zhibin Tang, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, et al. Tinyvla: Towards fast, data-efficient visionlanguage-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 1, 3 

- [39] Junyi Wu, Haoxuan Wang, Yuzhang Shang, Mubarak Shah, and Yan Yan. Ptq4dit: Post-training quantization for diffusion transformers. _Advances in neural information processing systems_ , 37:62732–62755, 2024. 3, 12 

- [40] Guangxuan Xiao, Ji Lin, Mickael Seznec, Hao Wu, Julien Demouth, and Song Han. Smoothquant: Accurate and efficient post-training quantization for large language models. In _International conference on machine learning_ , pages 38087– 38099. PMLR, 2023. 2, 3 

- [41] Siyu Xu, Yunke Wang, Chenghao Xia, Dihao Zhu, Tao Huang, and Chang Xu. Vla-cache: Towards efficient visionlanguage-action model via adaptive token caching in robotic manipulation. _arXiv preprint arXiv:2502.02175_ , 2025. 1, 3 

- [42] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_ , 2025. 1 

- [43] Lianwei Yang, Haisong Gong, Haokun Lin, Yichen Wu, Zhenan Sun, and Qingyi Gu. Dopq-vit: Towards distribution-friendly and outlier-aware post-training 

quantization for vision transformers. _arXiv preprint arXiv:2408.03291_ , 2024. 3 

- [44] Lianwei Yang, Haokun Lin, Tianchen Zhao, Yichen Wu, Hongyu Zhu, Ruiqi Xie, Zhenan Sun, Yu Wang, and Qingyi Gu. Lrq-dit: Log-rotation post-training quantization of diffusion transformers for text-to-image generation. _arXiv preprint arXiv:2508.03485_ , 2025. 3 

- [45] Yantai Yang, Yuhao Wang, Zichen Wen, Luo Zhongwei, Chang Zou, Zhipeng Zhang, Chuan Wen, and Linfeng Zhang. Efficientvla: Training-free acceleration and compression for vision-language-action models. _arXiv preprint arXiv:2506.10100_ , 2025. 1, 3 

   - [55] Siyuan Zhou, Yilun Du, Jiaben Chen, Yandong Li, Dit-Yan Yeung, and Chuang Gan. Robodreamer: Learning compositional world models for robot imagination. _arXiv preprint arXiv:2404.12377_ , 2024. 3 

   - [56] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 2 

- [46] Zhihang Yuan, Lin Niu, Jiawei Liu, Wenyu Liu, Xinggang Wang, Yuzhang Shang, Guangyu Sun, Qiang Wu, Jiaxiang Wu, and Bingzhe Wu. Rptq: Reorder-based post-training quantization for large language models. _arXiv preprint arXiv:2304.01089_ , 2023. 3 

- [47] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 11975–11986, 2023. 4 

- [48] Rongyu Zhang, Menghang Dong, Yuan Zhang, Liang Heng, Xiaowei Chi, Gaole Dai, Li Du, Yuan Du, and Shanghang Zhang. Mole-vla: Dynamic layer-skipping vision language action model via mixture-of-layers for efficient robot manipulation. _arXiv preprint arXiv:2503.20384_ , 2025. 1, 3 

- [49] Tianchen Zhao, Tongcheng Fang, Haofeng Huang, Enshu Liu, Rui Wan, Widyadewi Soedarmadji, Shiyao Li, Zinan Lin, Guohao Dai, Shengen Yan, et al. Vidit-q: Efficient and accurate quantization of diffusion transformers for image and video generation. _arXiv preprint arXiv:2406.02540_ , 2024. 3 

- [50] Tianchen Zhao, Xuefei Ning, Tongcheng Fang, Enshu Liu, Guyue Huang, Zinan Lin, Shengen Yan, Guohao Dai, and Yu Wang. Mixdq: Memory-efficient few-step text-to-image diffusion models with metric-decoupled mixed precision quantization. In _European Conference on Computer Vision_ , pages 285–302. Springer, 2024. 3, 12 

- [51] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 2 

- [52] Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng, Jiayin Zou, Yilun Chen, Jia Zeng, et al. X-vla: Soft-prompted transformer as scalable cross-embodiment vision-language-action model. _arXiv preprint arXiv:2510.10274_ , 2025. 3 

- [53] Yifan Zhong, Fengshuo Bai, Shaofei Cai, Xuchuan Huang, Zhang Chen, Xiaowei Zhang, Yuanfei Wang, Shaoyang Guo, Tianrui Guan, Ka Nam Lui, et al. A survey on visionlanguage-action models: An action tokenization perspective. _arXiv preprint arXiv:2507.01925_ , 2025. 1 

- [54] Hongyi Zhou, Weiran Liao, Xi Huang, Yucheng Tang, Fabian Otto, Xiaogang Jia, Xinkai Jiang, Simon Hilber, Ge Li, Qian Wang, et al. Beast: Efficient tokenization of b-splines encoded action sequences for imitation learning. _arXiv preprint arXiv:2506.06072_ , 2025. 3 

## **A. General Quantization Formulations** 

Post-training quantization (PTQ) [26, 39, 50] reduces memory footprint and accelerates inference without additional training. This subsection introduces a generic, bitparameterized formulation. Here, we use tildes to denote integer tensors and hats to denote their dequantized floating approximations. 

Consider a linear layer _Y_ = _XW_ without bias. Let _bX_ and _bW_ be the activation and weight bit widths, respectively. Activations are quantized per token using an unsigned grid, and weights are quantized per output channel using a signed grid. Therefore, the integer activations _X_<sup>˜</sup> are obtained as: 


with dequantization 


Integer weights for output channel _o_ are: 


with dequantization 


Following DuQuant, we further factorize the layer with block orthogonal rotations _R_<sup>ˆ</sup> (1) _, R_<sup>ˆ</sup> (2) and a permutation _P_ : 


All three matrices are orthogonal and therefore _P_<sup>_−_1</sup> = _P_<sup>_⊤_</sup> . The left bracket _G_ acts on activations before integerization and the right bracket _G_<sup>_−_1</sup> is folded into the weights to preserve equivalence. After this factorization, we can quantize _G_ on the activation side and _G_<sup>_−_1</sup> on the weight side at the chosen bit widths _bX_ and _bW_ respectively and then execute the integer matrix multiplication with the corresponding dequantization scales. 

## **C. How logits transfer from the language backbone to DiT in a VLA** 

These scales appear in DiT attention only through dequantization. For a head of width _d_ we set 


The logits matrix that drives attention is 


and the attention matrix is 

Here, ∆ _X >_ 0 is the activation scale estimated from a small unlabeled calibration buffer, and _zX ∈{_ 0 _, . . . ,_ 2<sup>_bX_</sup> _−_ 1 _}_ is the integer zero point for the unsigned activation grid. Each output channel _o_ uses a per-channel scale ∆<sup>(</sup> _W_<sup>_o_)</sup> _>_ 0 and a symmetric signed grid _{−_ 2<sup>_bW −_1</sup> _, . . . ,_ 2<sup>_bW −_1</sup> _−_ 1 _}_ . Dequantization multiplies stored integers by their corresponding scales to obtain floating-point approximations. 

## **B. DuQuant Implementation Details** 

With DuQuant design, we then instantiate the transform, beginning with the smoothing step. Specifically, to balance the difficulty of quantizing activations and the relative ease of quantizing weights, we apply per-channel smoothing with a diagonal matrix Λ: 


We then operate on the transformed pair 


The per-head output is 


Let the output projection be dequantized as _W_<sup>ˆ</sup> _o_ = _so W_<sup>˜</sup> _o_ . The block output after concatenating heads and applying the output projection is 


= Therefore, _sqsk_ sets an effective temperature _T_ eff _~~√~~ d/_ ( _sqsk_ ) that controls attention sharpness, and _svso_ primarily determines how much energy is injected into the residual stream. 

## **D. QuantVLA Parameters** 

**Appendix: Quantization and calibration.** GR00T N1.5 and OPENPI _π_ 0.5 use the same DuQuant configuration and the same statistical calibration. We set the weight bit width to 4 and the activation bit width to 8, which reduces memory and bandwidth while keeping accuracy stable. The block 

size is 64 on both the input and the output, so that block orthogonal rotations and collected statistics share the same granularity. For the LLM and DiT backbone, we enable channel permutation to redistribute large channels and reduce outliers. The row rotation modrestoredstore, which applies a rotation before each linear map and the inverse after the map, so that the real-valued function is preserved while improving the suitability of the layer for quantization. During post-training calibration, we set the activation percentile to 99.9 to determine the clipping range, we use 32 batches to estimate scales, and we apply per-channel smoothing with a coefficient of 0.15 to prevent a few channels from dominating a shared scale. 

After integerization, both models use the same statistical matching. Attention temperature matching learns one scalar _α_ for each head and aligns the scale of the student logits with the teacher so that the attention distribution is neither overly sharp nor overly flat. Output head balancing learns one scalar _β_ for each layer and restores the residual stream energy at the module output. In our runs the scope of _β_ is limited to the diffusion transformer head. We fit _α_ and _β_ from a small unlabeled buffer using 128 steps with at most 5 trials for each task, we clamp log _α_ and log _β_ with a limit of 0.30, and we keep a neutrality band _ε_ of 0.03 so that both scalars remain close to 1 when the estimate is uncertain. We fold _α_ into the dequantization scale for inference and apply _β_ at the module output. 

## **E. Comparison with other PTQ Method** 

As shown in Table 5, SmoothQuant, a built-in PTQ method in NVIDIA-OPT, performs reasonably at **W8A8** precision. In contrast, QuantVLA achieves comparable or slightly better results under the more aggressive **W4A8** setting. When SmoothQuant is extended to quantize both the LLM and the DiT MLP, performance remains competitive under W8A8 precision. However, QuantVLA operates at a lower bitwidth while maintaining stable performance across all task suites. In particular, improvements are observed on the long-horizon task, where low-precision inference typically accumulates greater drift over sequential generation. The average success rate under W4A8 is also slightly higher than the floating-point baseline. 

bust in long-sequence scenarios. Therefore, it provides a more favorable accuracy–efficiency trade-off for low-bit inference in VLA models when deployment efficiency is a primary consideration. 

## **F. Extended Benchmark Evaluation** 

As shown in Table 6, we further evaluate QuantVLA on the Pick-and-Can manipulation benchmark. Under **W4A8** precision, SmoothQuant exhibits a noticeable drop in performance compared to the FP16 baseline. In contrast, QuantVLA substantially narrows the gap and maintains a higher success count under the same precision setting. 

|Method|Precision|PickCan|
|---|---|---|
|GR00T|FP16|31 / 50|
|+ SmoothQuant|W4A8|16 / 50|
|+ QuantVLA|W4A8|27 / 50|


Table 6. Quantization results on Pick-and-Can. 

Although performance does not fully match the floatingpoint baseline, the results demonstrate that QuantVLA better preserves task performance under aggressive quantization. This suggests that the proposed design mitigates the sensitivity of the action head to quantization noise in manipulation scenarios. 

## **G. Applicability Beyond DiT-Based VLA Models** 

We evaluated OpenVLA, which uses a deeper 32-layer language backbone than the 18-layer backbones studied here and a non-DiT action head, resulting in different language– action coupling. Thus, the DiT-specific ATM and OHB mechanisms are not directly applicable. Nevertheless, QuantVLA matches OpenVLA performance (Table 7). 

|Model|Precision|Spatial|
|---|---|---|
|OpenVLA|FP16|84.7%|
|**+ QuantVLA**|**W8A16**|**86.0%**|


Table 7. Quantization results on LIBERO-Spatial for OpenVLA. 

|Method|Spatial|Object|Goal|Long|Avg|
|---|---|---|---|---|---|
|_π_0.5|98.5%|99.0%|97.5%|93.5%|97.1%|
|+SmoothQuant (LLM)|97.5%|98.5%|98.0%|92.5%|96.6%|
|+SmoothQuant (LLM + DiT (MLP))|98.0%|99.0%|99.0%|92.0%|97.0%|
|+QuantVLA (LLM)|98.5%|99.0%|96.5%|96.5%|97.6%|
|**+QuantVLA**|**98.5%**|**98.0%**|**98.0%**|**96.0%**|**97.6%**|


Table 5. Additional quantization comparison on the LIBERO benchmark for OpenPI _π_ 0.5. 

These results indicate that QuantVLA sustains task performance under more aggressive quantization and remains ro- 

