---
title: "HBVLA: Pushing 1-Bit Post-Training Quantization for Vision-Language-Action Models"
date: "2026-02-14"
authors: "Xin Yan; Zhenglin Wan; Feiyang Ye; Xingrui Yu; Hangyu Du; Yang You"
url: https://arxiv.org/abs/2602.13710
pdf: https://arxiv.org/pdf/2602.13710
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.13710)** / [論文ページ](https://arxiv.org/abs/2602.13710)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **HB-VLA: Pushing 1-Bit Post-Training Quantization for Vision-Language-Action Models** 

## **Xin Yan**<sup>1</sup> **, Zhenglin Wan**<sup>2</sup> **, Feiyang Ye, Xingrui Yu**<sup>3∗</sup> **, Hangyu Du**<sup>4</sup> **, Yang You**<sup>2</sup> **, Ivor Tsang**<sup>3</sup> 

1School of Artificial Intelligence, Beijing Normal University, Beijing, China 

2Department of Computer Science, National University of Singapore, Singapore 

3Centre for Frontier AI Research, Agency for Science, Technology and Research (A*STAR), Singapore 

4College of Design and Engineering, National University of Singapore, Singapore yu_xingrui@a-star.edu.sg 

#### **Abstract** 

Vision-Language-Action (VLA) models enable instructionfollowing embodied control, but their large compute and memory footprints hinder deployment on resource-constrained robots and edge platforms. While reducing weights to 1- bit precision through binarization can greatly improve efficiency, existing methods fail to preserve action-critical information under extreme compression, causing quantization errors to accumulate during long-horizon closed-loop execution and severely degrade control performance. To address this challenge, we propose HB-VLA, a VLA-tailored binarization framework. First, we introduce an action-aware rectified Hessian that identifies weights truly critical for stable action generation, where token importance is derived from a drift-weighted action loss. Then, we employ a sparse orthogonal transform for non-salient weights to induce a low-entropy intermediate state. Finally, we quantize both salient and non-salient weights in the Haar domain with group-wise 1-bit quantization. Extensive experiments on LIBERO, SIMPLER, and real-world robotic tasks show that HB-VLA reduces weight memory by about 82.0%, while outperforming the strongest binary PTQ baseline by 11.0 percentage points on average across eight evaluation settings and by up to 17.8 points. These results demonstrate that HB-VLA enables efficient and stable deployment of VLA models on resource-limited robotic platforms. 

## **Introduction** 

In recent years, Vision-Language-Action (VLA) models have emerged as a powerful paradigm for instruction-following embodied control by integrating visual perception, language understanding, and action generation within a single policy. Representative VLAs, such as RT-2 (Zitkovich et al. 2023), OpenVLA (Kim et al. 2024), and CogACT (Li et al. 2024a), have demonstrated strong performance on a wide range of manipulation tasks, including long-horizon instruction execution and generalization across diverse objects and scenes. These advances are largely enabled by large-scale model parameters and extensive robot datasets, which together provide high representation capacity and robust instruction grounding. However, these capabilities come with substantial computational demands and high memory usage, posing significant challenges for deployment on resource-constrained 

robotic platforms and edge devices where real-time, closedloop control is required. 

Post-Training Quantization (PTQ) (Nagel et al. 2019, 2020; Krishnamoorthi 2018) has gained significant traction due to its efficiency and practicality. Unlike quantizationaware training (QAT) (Jacob et al. 2018), which requires access to training data and retraining the network, PTQ operates on frozen parameters and uses a small calibration set to determine quantization parameters and rounding decisions. Recent PTQ methods have shown promising results in reducing weight and activation bitwidths for large models (Lin et al. 2024). Despite progress in 8-bit and 4-bit quantization for VLAs (Fang et al. 2025), the scale and deployment constraints of modern VLAs still call for more aggressive compression. Neural network binarization, which reduces weight precision to a single bit, is a promising direction toward ultra-low-bit quantization ( _≤_ 2 bits). However, directly transferring binary PTQ methods from large language models (LLMs) and vision-language models (VLMs) to VLAs is often ineffective. The central challenge in VLA binarization is not merely preserving feature reconstruction or language-model perplexity, but maintaining stable action behavior under closed-loop execution. Unlike LLMs or VLMs, whose errors are typically measured in token, logit, or feature space, VLA policies output continuous actions that are executed by a physical system. Consequently, even small quantization-induced action deviations can be amplified by contact dynamics and accumulated over long-horizon rollouts, leading to unstable grasps, oscillatory motions, or large trajectory drift. This fundamental mismatch suggests that ultra-low-bit VLA quantization should be formulated as an action-preserving problem, rather than a direct extension of reconstruction-oriented LLM/VLM binarization. 

Motivated by this perspective, we revisit 1-bit PTQ for VLAs from the viewpoint of policy preservation and identify a fundamental mismatch between existing quantization criteria and embodied control requirements. Unlike conventional models where quantization sensitivity can be approximated by representation reconstruction, VLA policies require preserving the parameters that are most influential to downstream action generation. This mismatch manifests in three aspects. First, quantization sensitivity is inherently policydependent and varies significantly across VLA components: 

∗Corresponding author. 


Figure 1: **Left:** An extreme background activation (Val=106.5). **Middle:** The activation heatmap is dominated by statistical outliers. **Right:** The overlay reveals misalignment: distractors such as the water bottle and background clutter dominate over the task-relevant apple, illustrating the dual-dominance problem. 

while the vision encoder is relatively robust, the projector and action generation modules are substantially more sensitive due to their direct influence on control outputs. Therefore, binary representation capacity should be allocated according to action relevance rather than uniformly across the network. Second, commonly used Hessian-based saliency estimation, e.g., **H** = **XX**<sup>_⊤_</sup> , captures activation statistics but does not account for the physical consequence of quantization errors. As shown in Figure 1, high-magnitude visual activations caused by background distractors can dominate the curvature estimation, leading to saliency scores that are misaligned with action-critical regions. Third, the parameter geometry of multimodal VLA policies introduces additional challenges for extreme quantization. Existing transform-based binarization methods rely on local structural assumptions in weight space, which may not hold when parameters from different modalities are interleaved, resulting in inefficient binary representations. 

Based on these observations, we propose **HB-VLA** , an action-preserving 1-bit post-training quantization framework that explicitly optimizes binary representation allocation according to policy sensitivity. Rather than extending reconstruction-oriented binarization methods to VLAs, HB-VLA establishes a policy-aware quantization pipeline consisting of three interconnected components. First, we introduce an action-aware rectified Hessian to estimate the sensitivity of model parameters with respect to closed-loop action deviation, enabling the identification of parameters whose preservation is essential for stable control. Second, we develop a structure-aware binary projection strategy that adapts the weight geometry of multimodal policies before quantization, reducing the interference caused by heterogeneous parameter distributions. Third, we employ a saliencyadaptive Haar-domain quantization scheme that assigns different binary encoding strategies to action-critical and redundant parameters while reducing storage overhead. Through this unified design, HB-VLA transforms binary quantization from a representation reconstruction problem into a policy preservation problem, enabling efficient extreme compression while maintaining stable embodied control. 

## **Related Work** 

### **Vision-Language-Action Models.** 

Vision-Language-Action (VLA) models have advanced embodied AI by enabling end-to-end policies that map multimodal observations to robotic actions. Representative models, including RT-2 (Zitkovich et al. 2023), OpenVLA (Kim et al. 2024), and UniVLA (Bu et al. 2025), extend pretrained VLMs (Karamcheti et al. 2024) by tokenizing actions for sequence generation. In contrast, another line of work models continuous actions with generative decoders, such as diffusion policies in Octo (Team et al. 2024) and CogACT (Li et al. 2024a), and flow matching in _π_ 0 (Black et al. 2026), achieving smooth and precise control. However, their large memory footprint limits deployment. Existing quantization methods, such as BitVLA (Wang et al. 2025a) and SQIP (Park et al. 2025), mainly rely on QAT, which requires costly training and large-scale robotic data. Therefore, low-bit PTQ for VLA models remains largely unexplored. This work addresses this gap by demonstrating that extreme quantization is essential for practical deployment of generalist VLA models. 

### **Network Binarization** 

Network binarization compresses neural networks by constraining weights and activations to binary values, enabling efficient bitwise computation. Most existing approaches rely on QAT with Straight-Through Estimators (STE) (Bengio, Leonard, and Courville 2013) to optimize the nondifferentiable sign function. BinaryConnect (Courbariaux, Bengio, and David 2015) and BWN introduced weight binarization, while XNOR-Net (Rastegari et al. 2016) extended it to both weights and activations. For transformers (Vaswani et al. 2017), BiT (Liu et al. 2022b) introduced elastic binarization with learnable scaling, and EcoFormer (Liu et al. 2022a) explored binary attention through hashing. Recent LLM binarization methods, including PBLLM (Yuan, Shang, and Dong 2024), BiLLM (Huang et al. 2024), ARB-LLM (Li et al. 2025), and HBLLM (Chen, Ye, and Jiang 2025), improve binary representation capacity through various strategies, such as frequency decomposition. 


Figure 2: (i) We establish a block-wise gradient probe to derive token importance scores ( _St_ ) and construct a **Corrected Hessian** proxy to identify _functionally salient_ weights grounded in the policy. (ii) We apply a hybrid quantization strategy: salient weights undergo residual quantization, while non-salient weights are processed via sparse orthogonal transform ( _P_ ) and Haar wavelet transform ( _H_ ) prior to group-wise 1-bit quantization. 

Bi-VLM (Wang et al. 2025b) further extends binarization to multimodal models but overlooks important activation structures. Inspired by these advances, we propose HB-VLA, an action-preserving 1-bit PTQ framework tailored for embodied control. 

## **Methodology** 

### **Method Overview** 

We define the objective of HB-VLA under the policypreserving binary quantization setting. From a global perspective, we frame the quantization as an optimization problem to identify the optimal binary parameter configuration _θ_<sup>ˆ</sup><sup>_⋆_</sup> such that the induced policy _fθ_ ˆ minimizes the KL divergence to the full-precision policy _fθ_ : 


For the quantization of a matrix layer **W** , the objective expressed in the Frobenius norm is formulated as: 


where **X** is the input of the matrix layer. 

We emphasize that our approach does not aim to solve these objective functions via explicit end-to-end optimization. Instead, this formulation serves as a conceptual framework that guides our method design. The actual quantization 

process is based on a set of heuristics and structure-aware strategies that approximate these objectives in a computationally efficient manner. To this end, our method HB-VLA adapts the efficient Haar transform into a unified pipeline tailored for VLAs. As shown in Figure 2, we begin by computing a policy-aware Hessian to identify salient weights critical for action. For the remaining non-salient weights, we apply a structured sparse orthogonal transform prior to the Haar transform. This aligns weight columns into a low-entropy state to suppress high-frequency noise. Subsequently, we perform **residual-aware refinement** , where salient columns are quantized via a column Haar transform to compensate for non-salient approximation errors. 

### **Policy-Aware Weight Partitioning** 

For each quantized linear layer, let **X** = [ **x** 1 _, . . . ,_ **x** _N_ ] _∈_ R<sup>_d×N_</sup> denote the calibration activations, where _N_ is the number of input tokens. Given a weight matrix **W** , our goal is to identify a compact set of salient columns whose binarization errors have the largest impact on action generation. Instead of using the standard Hessian proxy **H** = **XX**<sup>_⊤_</sup> , we introduce a rectified Hessian that assigns different importance to different tokens: 


where **S** = Diag( _s_ 1 _, . . . , sN_ ) and _st_ is the unique tokenimportance score defined in Eq. (7) from the drift-weighted action loss. This formulation preserves the efficiency of Hessian-based saliency estimation while aligning the weighting term with action-space sensitivity. 

**Forward.** We consider a local residual attention block in the action pathway, Φ( **X** ) ≜ **X** + MHSA( **X** ), and its binarized counterpart Φ(<sup>ˆ</sup> _·_ ). Given the same input **X** _∈_ R<sup>_d×N_</sup> , we obtain 


The two block outputs are then passed through the remaining frozen layers to produce the full-precision action _a_ and the binarized action ˆ _a_ , respectively. 

**Drift-Weighted Action Loss.** Instead of measuring only local block reconstruction error, we measure the action deviation induced by binarization. For a _da_ -dimensional action vector, we define a drift-weighted action loss: 


where _ρ_ ¯ _j_ denotes the drift sensitivity of the _j_ -th action dimension. Following the idea of structural kinematic propagation, we estimate this sensitivity using a structural or embodiment-specific Jacobian that maps action perturbations to end-effector deviations: 


Here, **J**<sup>(</sup><sup>_t_)</sup> describes how an error in each action dimension affects the end-effector at timestep _t_ . Thus, action dimensions whose perturbations are more likely to be amplified into trajectory drift receive larger weights in _L_ act. 

**Backward.** We perform a locally isolated backpropagation on _L_ act and collect gradients at the attention projections ( _Q, K, V, O_ ). Let _P_ = _{Q, K, V, O}_ denote the set of projection outputs **Y**<sup>(</sup><sup>_p_)</sup> _∈_ R<sup>_dp×N_</sup> . The projection gradients and the resulting token-importance score are defined jointly as 


Here, _a_<sup>(</sup> _t_<sup>_p_)</sup> is the channel-normalized sensitivity of token _t_ at projection _p_ , and _st_ averages this sensitivity over _Q_ , _K_ , _V_ , and _O_ . A larger _st_ therefore indicates that perturbing token _t_ causes a larger drift-weighted action deviation across the attention pathways.Equation (7) is thesole definition oftoken importance used in both the main text and the appendix; no separate residual-feature gradient is used as an alternative score. 

**Saliency Partition.** Finally, we compute column saliency from the rectified Hessian **H**<sup>˜</sup> in Eq. (3) and partition each layer into salient and non-salient column sets _I_ sal and 

_I_ non _−_ sal. We first derive element-wise importance scores normalized by the Hessian diagonal and aggregate them into per-column scores via an _ℓ_ 2 reduction. The number of salient columns is then determined by minimizing a local binarization reconstruction objective, with the remaining columns assigned to _I_ non _−_ sal. 

### **Saliency-Aware Hybrid Binarization With Haar Transform** 

We use a hybrid binarization method that treats salient and non-salient weights differently, but both parts share the same two-step quantization primitive. We first map weights to the Haar domain and split them into low-pass and high-pass subbands. Concretely, for an even length _m_ , we define a one-level, orthonormally normalized Haar transform matrix **H** _m ∈_ R<sup>_m×m_</sup> and map _w ∈_ R<sup>1</sup><sup>_×m_</sup> to the Haar domain by 


Here _k_ = 1 _, . . . , m/_ 2, and _w_<sup>lo</sup> _, w_<sup>hi</sup> _∈_ R<sup>1</sup><sup>_×_(</sup><sup>_m/_2)</sup> are the lowpass and high-pass subbands. Thus, **H** _m_ is constructed from the normalized filters [1 _/_ _~~√~~_ 2 _,_ 1 _/_ _~~√~~_ 2] and [1 _/_ _~~√~~_ 2 _, −_ 1 _/_ _~~√~~_ 2] (with a coefficient-ordering permutation), so that **H**<sup>_⊤_</sup> _m_<sup>**H**</sup><sup>_m_=</sup> **H** _m_ **H**<sup>_⊤_</sup> _m_<sup>=</sup><sup>**I**and</sup><sup>**H**</sup><sup>_−_</sup> _m_<sup>1=</sup><sup>**H**</sup><sup>_⊤_</sup> _m_<sup>. More details are provided in</sup> Appendix **??** . 

After the transform, we employ a row-wise grouping strategy. Instead of global partitioning, we adaptively split coefficients within each frequency band into groups (e.g., dense/sparse) to capture the local structural pattern. Then we apply binarization to every group: 


where _µg_ and _αg_ are computed per group. Notably, for nonsalient weights, we optimize storage efficiency by enforcing a single shared mean _µ_ across groups within the same row and frequency band. This approach effectively reduces the average bit-width and metadata overhead while preserving model performance. 

**Non-salient Weights Binarization.** Since salient columns are excluded from the Haar transform of the non-salient part, we first fill the missing values in salient columns using adjacent averages, obtaining **W** _l,_ filled. We binarize **W** _l,_ filled in the Haar domain by applying a row-wise Haar transform along the column axis: 


In VLAs, non-salient columns often exhibit strong modalitydependent structures. However, these columns are typically interleaved in the weight matrix space rather than forming contiguous, modality-specific blocks. This lack of structural locality poses a significant challenge for the Haar transform, which operates on fixed local windows by calculating differences between adjacent columns. When the Haar operator pairs columns from disparate modalities, the resulting crossmodality offsets manifest as sharp step-change outliers in the Haar domain. 

To resolve this, we employ a **sparse orthogonal transform** , implemented via a permutation matrix **P** _∈ {_ 0 _,_ 1 _}_<sup>_m×m_</sup> , prior to the Haar transform. This mechanism allows us to maintain the _O_ ( _d_ ) convolutional efficiency of Haar while making it adaptive to the underlying weight geometry. After permutation, we follow the quantization primitive: 


where **_µ_** and **_α_** are computed group-wise in Eq. (9). Since both the permutation **P** and the normalized Haar basis **H** _m_ are orthogonal, the transform preserves the Frobenius norm. In particular, 


We construct this sparse orthogonal transform by minimizing the high-frequency energy generated during decomposition. Specifically, for a one-level Haar transform, the energy in the high-pass subband is proportional to the sum of discrepancies between paired columns. Let _π_ be the ordering induced by **P** and let **H** hi denote the first-level high-pass basis. Then the high-pass energy admits the following identity: 


and we provide a proof in Appendix **??** . Therefore, determining the optimal **P** is equivalent to solving a discrete optimization problem that maximizes local column similarity. Since the exact global optimum is intractable, we adopt a greedy pairing-and-chaining heuristic to efficiently generate the permutation _π_ that defines **P** . _Due to the page limitation, the detailed pseudocode of the proposed algorithm is provided in the Appendix._ 

**Salient Weights Binarization.** � After obtaining the nonsalient approximation **W** _l,_ non _−_ sal, we quantize salient columns on the residual to avoid interference from the nonsalient reconstruction. We define the residual 


By defining _I_ sal as the index set of salient columns, we extract the salient residual **R** _l_ (: _, I_ sal) and apply a _column-wise_ Haar transform (more details are provided in Appendix **??** ): 


## **Experiment** 

We validate our approach through a series of experiments across simulated benchmarks and physical robot manipulation tasks. All experiments are conducted on NVIDIA A800 GPUs. More details are provided in Appendix. 

### **Experimental Setup** 

We conduct experiments on three settings: the LIBERO (Liu et al. 2023) and SIMPLER (Li et al. 2024b), two widely recognized robotic manipulation benchmarks for evaluation in simulation environments, and the real-world Mobile ALOHA platform with three test tasks, to validate the practical applicability of HB-VLA. We use the widely used performance evaluation metrics “Success Rate (SR)” to evaluate the results in these challenging settings. During inference, all activations remain in BF16 precision, while only weights are binarized. 

**LIBERO** (Liu et al. 2023): LIBERO evaluates knowledge transfer and policy generalization across four suites: Spatial, Object, Goal, and Long. It contains 100 MuJoCo tasks and 5,000 demonstrations using a Franka Panda arm with RGB, proprioceptive, and delta-action observations. 

**SIMPLER** (Li et al. 2024b): SIMPLER evaluates VLA policies in high-fidelity simulations under Visual Matching and Variant Aggregation. We use the Google robot arm on four tasks: Pick Coke Can, Move Near, Open/Close Drawer, and Place Apple into Top Drawer. 

**Real-world Evaluation Suite.** We evaluate real-world adaptability on Mobile ALOHA using Pick and Place, Sequenced Instruction, and Flexible Folding benchmarks (Bu et al. 2025; Zhao et al. 2025). These tasks assess generalization from 30– 450 demonstrations per task to novel environments. Further details are provided in the Appendix. 

**Baselines.** We selected recently published 1-bit PTQ methods as baselines, including HBLLM (Chen, Ye, and Jiang 2025), BiLLM (Huang et al. 2024), and BiVLM (Wang et al. 2025b). BiLLM and HBLLM all utilize the PTQ approach for model calibration through OBQ based method of GPTQ. 

### **Main Results** 

**Quantization on Different Components.** As shown in Tables 1, 2, and 3, the vision encoder is generally the most robust to quantization. The adaptor/projector and language model show moderate sensitivity, while quantizing the action head causes the largest performance drop. 

**Comparison with SOTA Methods.** As shown in Table 4, HB-VLA consistently outperforms all binary PTQ baselines on both LIBERO and SIMPLER. Existing LLM/VLM binarization methods degrade substantially when directly applied to VLAs, whereas HB-VLA retains a much smaller gap to full precision. On LIBERO, HB-VLA reaches 92.7% with LM+ViT quantization, only 4.4 percentage points below FP. On SIMPLER Visual Matching, it improves the strongest baseline from 62.3% to 70.0% for LM+ViT quantization and from 55.8% to 67.2% for full-model quantization. Similar gains under Variant Aggregation indicate better preservation of action-relevant representations under visual shifts and closed-loop execution. 

|SIMPLER|Task|FP|Vis|Adp|Lm|Act|Vis+Lm|Vis+Adp+Lm|Vis+Adp+Lm+Act|
|---|---|---|---|---|---|---|---|---|---|
||Pick Coke|91.3|90.8|84.7|88.2|85.4|86.7|87.2|86.4|
|il|Move Near|85.0|84.6|82.7|83.5|82.5|81.7|80.3|79.7|
|Vsua<br>Matching|O/C Drawer|71.8|72.0|70.6|71.5|70.0|71.8|69.9|68.3|
||Place Apple|50.9|47.4|46.9|44.8|41.7|38.4|36.2|34.5|
||Avg|74.8|73.7|71.2|72.0|69.9|70.0|68.4|67.2|
||Pick Coke|89.6|89.3|86.9|87.4|82.7|85.1|84.9|82.5|
|i|Move Near|80.8|80.8|75.8|76.3|74.4|72.5|73.2|71.7|
|Varant<br>Aggregation|O/C Drawer|28.3|26.7|25.9|25.7|24.3|21.4|20.6|20.3|
||Place Apple|46.6|45.4|30.4|32.7|29.5|24.9|25.3|22.6|
||Avg|61.3|60.6|54.8|55.5|52.7|51.0|51.0|49.2|


Table 1: Component-wise quantization results of CogACT model on SIMPLER environment, with average weight precision ranging from 1.02 to 1.13 bits. FP denotes full precision; Vis denotes the vision encoder; Adp denotes the adaptation layer; Lm denotes the language model; and Act denotes the action head. “O/C Drawer” refers to the Open/Close Drawer task. All results are reported as success rates (%). 

|LIBERO|FP|Vis|Adp|Lm|Act|Vis+Lm|Vis+Adp+Lm|Vis+Adp+Lm+Act|
|---|---|---|---|---|---|---|---|---|
|Spatial|98.5|98.5|97.6|97.9|96.5|95.8|94.2|92.8|
|Object|99.0|98.6|98.0|98.2|97.8|97.2|96.5|95.6|
|Goal|97.5|97.3|96.2|95.7|91.3|93.5|89.8|86.5|
|Long|93.5|92.7|87.3|89.5|86.5|84.4|79.2|76.7|
|Avg|97.1|96.8|94.8|95.3|93.0|92.7|89.9|87.9|


Table 2: Quantization on different components of _π_ 0 _._ 5 on LIBERO with weights from 1.02 to 1.13 bits. All results are reported as success rates (%). FP: Full precision. Vis: Vision encoder. Adp: Adapt layer. Lm: Language model. Act: Action Head. 

**Mobile ALOHA.** Pick and Place is evaluated over 30 trials, while the other tasks use 24 trials each. As shown in Figure 3, OpenVLA-OFT performs strongly across all three tasks, whereas BiLLM performs worst and exhibits persistent arm oscillations during execution. Compared with FP, HB-VLA drops by 23.4, 12.5, and 16.6 percentage points on Pick and Place, Sequenced Instruction, and Flexible Folding, respectively. Despite these gaps, it consistently outperforms all binary PTQ baselines, demonstrating better retention of real-world control performance under 1-bit weight quantization. 

### **Time and Memory Analysis** 

As shown in Table 5, HB-VLA substantially reduces the weight memory footprint across different VLA models. Using the metadata-aware storage estimate, HB-VLA compresses _π_ 0 _._ 5 from 4.6GB to 0.83GB, OpenVLA-OFT from 15.2GB to 2.74GB, and CogACT from 30.5GB to 5.50GB, corresponding to an average memory reduction of about 82.0%. This demonstrates that HB-VLA remains storageefficient even when quantization metadata is considered. In addition, HB-VLA achieves a 2 _._ 93 _×_ inference speedup over the full-precision baseline, reducing latency by approximately 65.9%. These results show that HB-VLA provides both substantial memory savings and practical acceleration for closed-loop robotic control. 


Figure 3: Comparison of baseline methods on the Mobile ALOHA experiments. Evaluation across three real-world tasks, including (a) Pick and Place, (b) Sequenced Instruction, (c) Flexible Folding. **Top:** Middle state image for each task. **Bottom:** Task-specific success rates for OpenVLA-OFT (FP Model), our HBVLA method, and baselines, including BiLLM and HBLLM. 

|LIBERO|FP|Vis|Adp|Lm|Vis+Adp|Vis+Lm|Lm+Adp|Vis+Adp+Lm|
|---|---|---|---|---|---|---|---|---|
|Spatial|97.6|97.2|94.5|94.7|90.8|89.3|90.2|83.4|
|Object|98.4|97.6|96.8|97.2|97.2|97.8|94.2|88.6|
|Goal|94.5|93.9|93.4|92.8|91.9|91.3|92.0|85.8|
|Long|97.9|95.4|86.9|87.5|85.5|82.7|86.2|76.0|
|Avg|97.1|96.0|92.9|93.0|91.4|90.3|90.7|83.5|


Table 3: Quantization on different components of OpenVLA-OFT on LIBERO with weights from 1.02 to 1.13 bits. All results are reported as success rates (%). FP: Full precision. Vis: Vision encoder. Adp: Adapt layer. Lm: Language model. 

|Model|Benchmark|FP|BiLLM|BiVLM|HBLLM|**HB-VLA (Ours)**|
|---|---|---|---|---|---|---|
|_π_0_._5(LM+ViT)|LIBERO|97.1|54.3|63.2|74.9|**92.7**|
|_π_0_._5(All)|LIBERO|97.1|47.2|55.8|70.7|**87.9**|
|CogACT (LM+ViT)|SIMPLER (VM)|74.8|28.8|57.1|62.3|**70.0**|
|CogACT (All)|SIMPLER (VM)|74.8|23.2|50.7|55.8|**67.2**|
|CogACT (LM+ViT)|SIMPLER (VA)|61.3|14.9|47.4|47.9|**51.0**|
|CogACT (All)|SIMPLER (VA)|61.3|8.8|40.9|43.2|**49.2**|
|OpenVLA-OFT (LM+ViT)|LIBERO|97.1|57.7|64.0|79.2|**90.3**|
|OpenVLA-OFT (All)|LIBERO|97.1|49.3|52.5|70.1|**83.5**|


Table 4: SOTA comparison on _π_ 0 _._ 5, CogACT, and OpenVLA-OFT with weights ranging from 1.02 to 1.13 bits. FP: Full precision. LM: Language model. ViT: Vision backbone. All: The whole VLA model. All results are reported as success rates (%). **Bold** values indicate the best results among the quantized models, excluding the full-precision model. 

|**Model**|**FP Memory**|**Quantization Memory**|
|---|---|---|
|_π_0_._5|4.6GB|0.83GB|
|OpenVLA-OFT|15.2GB|2.74GB|
|CogACT|30.5GB|5.50GB|


|Hessian|Visual|Variant|
|---|---|---|
|Formulation|Matching (Avg.)_↓_|Aggregation (Avg.)_↓_|
|Standard|12.5%|13.4%|
|Action-Aware|**10.3%**|**12.1%**|


Table 5: Weight-only memory comparison before and after HB-VLA quantization. 

|Selection|Visual|Variant|
|---|---|---|
|criterion|Matching_↓_|Aggregation_↓_|
|_ℓ_1|11.6%|15.6%|
|_ℓ_2|**8.8%**|**12.8%**|


Table 6: Study of column permutation criterion. 

### **Further Analysis** 

**Column-Norm Criterion for Permutation.** To evaluate the impact of the permutation criterion for non-salient columns on quantization effectiveness, we compare two strategies: the column _ℓ_ 1-norm and the column _ℓ_ 2-norm with CogACT on Simpler. The results are shown in Table 6. Using the _ℓ_ 2-norm yields lower quantization error and superior downstream performance compared to _ℓ_ 1, as the _ℓ_ 2-norm more effectively captures energy distribution across columns, thereby improving quantization quality. 

**Effectiveness of Action-Aware Hessian.** To investigate the impact of the proposed rectified Hessian on saliency estimation, we compare it against the standard Hessian formulation with CogACT on Simpler. As shown in Table 7, our action-aware Hessian effectively filters out quantization noise 

Table 7: Impact of Hessian formulation on quantization. 

and accurately identifies task-critical weights essential for instruction-following control, resulting in significant gains in success rate. 

_Due to the page limitation, additional ablation studies on saliency partition candidates and sparse orthogonal reordering are provided in the Appendix._ 

## **Conclusion** 

In this paper, we introduce HB-VLA, a 1-bit post-training quantization framework tailored to VLA models. HB-VLA combines policy-aware weight partitioning with a sparse orthogonal transform in the Haar domain to alleviate the severe performance degradation caused by extreme quantization while preserving action-relevant representations. Experiments on LIBERO, SIMPLER, and real-world Mobile ALOHA demonstrate that HB-VLA consistently outperforms existing binary PTQ baselines across different VLA architectures, visual variations, and manipulation tasks. These results show that HB-VLA achieves substantial model compression while retaining strong closed-loop control performance, highlighting the practical potential of low-bit PTQ for deploying capable VLA policies on resource-constrained robotic platforms. 

## **References** 

Bengio, Y.; Leonard, N.; and Courville, A. 2013. Estimating or propagating gradients through stochastic neurons for conditional computation. ArXiv preprint arXiv:1308.3432. 

Black, K.; Brown, N.; Driess, D.; Esmail, A.; Equi, M.; Finn, C.; Fusai, N.; Groom, L.; Hausman, K.; Ichter, B.; Jakubczak, S.; Jones, T.; Ke, L.; Levine, S.; Li-Bell, A.; Mothukuri, M.; Nair, S.; Pertsch, K.; Shi, L. X.; Tanner, J.; Vuong, Q.; Walling, A.; Wang, H.; and Zhilinsky, U. 2026. _π_ 0: A VisionLanguage-Action Flow Model for General Robot Control. arXiv:2410.24164. 

Bu, Q.; Yang, Y.; Cai, J.; Gao, S.; Ren, G.; Yao, M.; Luo, P.; and Li, H. 2025. Univla: Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2505.06111_ . 

Chen, N.; Ye, W.; and Jiang, Y. 2025. HBLLM: WaveletEnhanced High-Fidelity 1-Bit Quantization for LLMs. arXiv:2512.00862. 

Courbariaux, M.; Bengio, Y.; and David, J.-P. 2015. Binaryconnect: Training deep neural networks with binary weights during propagations. In Cortes, C.; and Lawrence, N., eds., _Proceedings of Advances in Neural Information Processing Systems (NeurIPS 2015)_ , volume 28. Montreal, Canada: Curran Associates. 

Fang, H.; Liu, Y.; Du, Y.; Du, L.; and Yang, H. 2025. Sqapvla: A synergistic quantization-aware pruning framework for high-performance vision-language-action models. _arXiv preprint arXiv:2509.09090_ . 

Huang, W.; Liu, Y.; Qin, H.; Li, Y.; Zhang, S.; Liu, X.; Magno, M.; and Qi, X. 2024. BiLLM: Pushing the Limit of Post-Training Quantization for LLMs. In Krause, A.; and Brunskill, E., eds., _Proceedings of the International Conference on Machine Learning (ICML 2024)_ . Vienna, Austria: OpenReview.net. 

Jacob, B.; Kligys, S.; Chen, B.; Zhu, M.; Tang, M.; Howard, A.; Adam, H.; and Kalenichenko, D. 2018. Quantization and training of neural networks for efficient integer-arithmeticonly inference. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , 2704–2713. 

Karamcheti, S.; Nair, S.; Balakrishna, A.; Liang, P.; Kollar, T.; and Sadigh, D. 2024. Prismatic vlms: Investigating the design space of visually-conditioned language models. In _Forty-first International Conference on Machine Learning_ . 

Kim, M. J.; Pertsch, K.; Karamcheti, S.; Xiao, T.; Balakrishna, A.; Nair, S.; Rafailov, R.; Foster, E.; Lam, G.; Sanketi, P.; et al. 2024. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ . 

Krishnamoorthi, R. 2018. Quantizing deep convolutional networks for efficient inference: A whitepaper. _arXiv preprint arXiv:1806.08342_ . 

Li, Q.; Liang, Y.; Wang, Z.; Luo, L.; Chen, X.; Liao, M.; Wei, F.; Deng, Y.; Xu, S.; Zhang, Y.; et al. 2024a. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ . 

Li, X.; Hsu, K.; Gu, J.; Pertsch, K.; Mees, O.; Walke, H. R.; Fu, C.; Lunawat, I.; Sieh, I.; Kirmani, S.; et al. 2024b. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ . 

Li, Z.; Yan, X.; Zhang, T.; Qin, H.; Xie, D.; Tian, J.; Shi, Z.; Kong, L.; Zhang, Y.; and Yang, X. 2025. ARB-LLM: Alternating Refined Binarizations for Large Language Models. In Cho, K.; and Lamb, A., eds., _Proceedings of the Thirteenth International Conference on Learning Representations (ICLR 2025)_ . Singapore: OpenReview.net. 

Lin, J.; Tang, J.; Tang, H.; Yang, S.; Chen, W.-M.; Wang, W.-C.; Xiao, G.; Dang, X.; Gan, C.; and Han, S. 2024. Awq: Activation-aware weight quantization for on-device llm compression and acceleration. _Proceedings of machine learning and systems_ , 6: 87–100. 

Liu, B.; Zhu, Y.; Gao, C.; Feng, Y.; Liu, Q.; Zhu, Y.; and Stone, P. 2023. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36: 44776–44791. 

Liu, J.; Pan, Z.; He, H.; Cai, J.; and Zhuang, B. 2022a. Ecoformer: Energy-saving attention with linear complexity. In Koyejo, S.; and Mohamed, S., eds., _Proceedings of Advances in Neural Information Processing Systems (NeurIPS 2022)_ , volume 35, 10295–10308. New Orleans, LA, USA: Curran Associates. 

Liu, Z.; Oguz, B.; Pappu, A.; Xiao, L.; Yih, S.; Li, M.; Krishnamoorthi, R.; and Mehdad, Y. 2022b. Bit: Robustly binarized multi-distilled transformer. In Koyejo, S.; and Mohamed, S., eds., _Proceedings of Advances in Neural Information Processing Systems (NeurIPS 2022)_ , volume 35, 14303–14316. New Orleans, LA, USA: Curran Associates. Nagel, M.; Amjad, R. A.; Van Baalen, M.; Louizos, C.; and Blankevoort, T. 2020. Up or down? adaptive rounding for post-training quantization. In _International conference on machine learning_ , 7197–7206. PMLR. 

Nagel, M.; Baalen, M. v.; Blankevoort, T.; and Welling, M. 2019. Data-free quantization through weight equalization and bias correction. In _Proceedings of the IEEE/CVF international conference on computer vision_ , 1325–1334. 

Park, S.; Kim, H.; Kim, S.; Jeon, W.; Yang, J.; Jeon, B.; Oh, Y.; and Choi, J. 2025. Saliency-aware quantized imitation learning for efficient robotic control. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 13140–13150. 

Rastegari, M.; Ordonez, V.; Redmon, J.; and Farhadi, A. 2016. XNOR-Net: ImageNet Classification Using Binary Convolutional Neural Networks. In Leibe, B.; Matas, J.; Sebe, N.; and Welling, M., eds., _Proceedings of the 14th European Conference on Computer Vision (ECCV 2016)_ , volume 9908, 525–542. Amsterdam, The Netherlands: Springer. Team, O. M.; Ghosh, D.; Walke, H.; Pertsch, K.; Black, K.; Mees, O.; Dasari, S.; Hejna, J.; Kreiman, T.; Xu, C.; et al. 2024. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ . Vaswani, A.; Shazeer, N.; Parmar, N.; Uszkoreit, J.; Jones, L.; Gomez, A. N.; Kaiser, L.; and Polosukhin, I. 2017. Attention is all you need. In Guyon, I.; and Luxburg, U. V., eds., 

_Proceedings of Advances in Neural Information Processing Systems (NeurIPS 2017)_ , volume 30. Long Beach, CA, USA: Curran Associates. 

Wang, H.; Xiong, C.; Wang, R.; and Chen, X. 2025a. BitVLA: 1-bit Vision-Language-Action Models for Robotics Manipulation. _arXiv preprint arXiv:2506.07530_ . 

Wang, X.; Huang, J.; Abdalla, R.; Zhang, C.; Xian, R.; and Manocha, D. 2025b. Bi-VLM: Pushing Ultra-Low Precision Post-Training Quantization Boundaries in Vision-Language Models. _arXiv preprint arXiv:2509.18763_ . 

Yuan, Z.; Shang, Y.; and Dong, Z. 2024. PB-LLM: Partially Binarized Large Language Models. In Gupta, A.; and Guyon, I. M., eds., _Proceedings of the Twelfth International Conference on Learning Representations (ICLR 2024)_ . Vienna, Austria: OpenReview.net. 

Zhao, Q.; Lu, Y.; Kim, M. J.; Fu, Z.; Zhang, Z.; Wu, Y.; Li, Z.; Ma, Q.; Han, S.; Finn, C.; et al. 2025. Cot-vla: Visual chainof-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 1702–1713. 

Zitkovich, B.; Yu, T.; Xu, S.; Xu, P.; Xiao, T.; Xia, F.; Wu, J.; Wohlhart, P.; Welker, S.; Wahid, A.; et al. 2023. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , 2165– 2183. PMLR. 

