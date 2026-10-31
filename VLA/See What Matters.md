---
title: "See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model"
date: "2026-05-12"
authors: "Yixu Feng; Zinan Zhao; Yanxiang Ma; Chenghao Xia; Chengbin Du; Yunke Wang"
venue: "ICML 2026"
url: https://arxiv.org/abs/2605.11817
pdf: https://arxiv.org/pdf/2605.11817
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.11817)** / [論文ページ](https://arxiv.org/abs/2605.11817)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

**Yixu Feng**<sup>1</sup> **Zinan Zhao**<sup>2</sup><sup>_†_</sup> **Yanxiang Ma**<sup>1</sup> **Chenghao Xia**<sup>3</sup> **Chengbin Du**<sup>3</sup> **Yunke Wang**<sup>1</sup> **Chang Xu**<sup>1</sup> 

## **Abstract** 

Vision-Language-Action (VLA) models have shown remarkable promise in robotics manipulation, yet their high computational cost hinders real-time deployment. Existing token pruning methods suffer from a fundamental trade-off: aggressive compression using pruning inevitably discards critical geometric details like contact points, leading to severe performance degradation. This forces a compromise, limiting the achievable compression rate and thus the potential speedup. We argue that breaking this trade-off requires rethinking compression as a geometry-aware, continuous token resampling in the vision encoder. To this end, we propose the _Differentiable Grid Sampler (GridS)_ , a plug-and-play module that performs task-aware, continuous resampling of visual tokens in VLA. By adaptively predicting a minimal set of salient coordinates and extracting features via differentiable interpolation, GridS preserves essential spatial information while achieving drastic compression (with fewer than 10% original visual tokens). Experiments on both LIBERO benchmark and a real robotic platform demonstrate that validating the lowest feasible visual token count reported to date, GridS achieves a 76% reduction in FLOPs with no degradation in the success rate. The code is available at Github. 

## **1. Introduction** 

Vision-Language-Action models (VLAs) integrate semantic reasoning and low-level control into unified architectures, showing strong generalization across manipulation tasks (Bai et al., 2025; Black et al., 2024; Kim et al., 2025b; Zitkovich et al., 2023; Zhong et al., 2026; Pertsch et al., 

> _†_ Work done during internship at StellarEdge Robotics. 1The University of Sydney<sup>2</sup> City University of Hong Kong<sup>3</sup> StellarEdge Robotics. Correspondence to: Chang Xu _<_ c.xu@sydney.edu.au _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 


_Figure 1._ Motivation and Performance of GridS. (a) Standard VLAs process images with dense, uniform token representations (2 _×_ 256), leading to high computational redundancy in irrelevant background areas (100% Compute). (b) Our Grid Sample (GridS) prunes non-essential tokens, focusing only on salient regions. This reduces the token count to 2 _×_ 16, requiring only 6.25% of the original compute. (c) Real-world Experiments demonstrate that GridS not only reduces inference latency by 2 _._ 3s but also significantly boosts the out-of-distribution task success rate (SR) by +28 _._ 6% compared to the baseline. 

2025; Liang et al., 2025; Xu et al., 2025a;c; Hui et al., 2026; Li et al., 2026a). However, VLAs incur high computational costs due to the massive token volume of the vision encoder. As shown in Fig. 1(a), an image is projected into 256 tokens in vision encoder (Dosovitskiy et al., 2021). This excessive sequence length creates a severe bottleneck for the subsequent Transformer block, where computational complexity scales quadratically with input sequence length. 

To mitigate this efficiency bottleneck, recent research has investigated visual token pruning. One prevalent approach adopt semantic pruning in VLAs (Li et al., 2026c), yet these methods often prioritize salient object bodies while neglecting geometrically critical but semantically subtle regions, _e.g._ edges or contact points (Qu et al., 2025; Chen et al., 2024a). Another direction is dynamic token pruning, which retains variable token counts per image (Yang et al., 2025; Xu et al., 2025b; Zhang et al., 2025; Xu et al., 2026; Pei et al., 2026). These methods adopt training-free strategies 

1 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

that are inherently non-differentiable, functioning as static heuristics derived from pre-existing policies. Consequently, they fail to align with specific application requirements, leading to varying degrees of degradation in task success rates. 

More fundamentally, both types of methods are constrained by their reliance on discrete selection over a fixed grid (Yuan et al., 2025). However, robotic interaction often requires sub-patch precision (as Fig. 2 (a), a grasp point is located between two patches). Restricting the model to select coarse patches introduces inherent quantization errors and leads to a loss of fine-grained spatial fidelity. 

To break this performance-efficiency trade-off, we propose the Differentiable **Grid S** ampler ( **GridS** ). GridS fundamentally reformulates VLA token compression from a passive discrete patch-dropping task into an active, geometry-aware continuous resampling process. Rather than being confined to the rigid output grid of a vision encoder, GridS dynamically predicts task-driven spatial coordinates and queries the continuous feature map via differentiable bilinear interpolation. As shown in Figs 1 and 2 (b), our method precisely localizes and samples the most discriminative tokens, retaining only 6.25% —(or even lower) of the original count. This allows the model to filter out a few task-related regions from the dense tokens, serving as an effective pruning strategy. 

We evaluate GridS in two flow-matching VLA architectures ( _π_ 0 (Black et al., 2024), _π_ 0 _._ 5 (Intelligence et al., 2025)), and a auto-regressive model (SmolVLA (Shukor et al., 2025)) to demonstrate its superior efficiency. In simulation tasks (LIBERO (Liu et al., 2023) and ALOHA (Zhao et al., 2023)), GridS maintains baseline success rates using fewer than 10% of visual tokens, while increasing task speed by 1.2 _×_ and training speed by 3.4 _×_ . In particular, on the LIBERO task of _π_ 0, we achieved a 1% improvement in accuracy by only using 4 visual tokens. Real-world experiments on a consumer-grade GPU reveal an average 1.23 _×_ inference speedup and a 22.2% success rate gain over baseline (SmolVLA). Counter-intuitively, we observe that reducing the number of tokens leads to a substantial 28.6% accuracy gain in out-of-distribution (OOD) scenarios (see Fig. 1 (c)). By significantly reducing deployment costs, GridS establishes a new pruning paradigm, paving the way for VLAs in highly dynamic and physically interactive environments. Furthermore, guided by constructive reviewers feedback, we have expanded our evaluations to include the LIBERO-PLUS (Fei et al., 2025) and RoboTwin (Mu et al., 2025) benchmarks, detailed in App. E. Crucially, these extended stress tests highlight the ultimate potential of our compression paradigm: GridS can aggressively distill visual information down to a single token ( _K_ = 1) while maintaining on-par performance with the dense baseline (reported in App. G). 


_Figure 2._ Discrete Selection vs. Differentiable Sampling. (a) Traditional approaches operate on a fixed grid. When the target region (yellow cross) falls between patches, the model is forced to perform discrete selection, leading to spatial quantization errors and a loss of fidelity. (b) Our approach predicts continuous coordinates and utilizes differentiable bilinear sampling to interpolate features from the four nearest neighbors. 

**Conflict of Interest Disclosure.** The authors declare that they have no financial conflicts of interest. 

## **2. Related Work** 

### **2.1. Vision-Language-Action Models** 

The paradigm of robotic learning has shifted from specialized, modular pipelines to unified VLA architectures, which integrate pre-trained vision encoders with language decoders to predict robot actions directly from visual observations and textual instructions. Early works like RT-1 (Brohan et al., 2022) demonstrated the efficacy of tokenizing robotic actions, while RT-2 (Zitkovich et al., 2023) and PaLM-E (Driess et al., 2023) scaled this approach by leveraging internet-scale Vision-Language Models (VLMs) to achieve remarkable semantic generalization and reasoning. More recently, open-source initiatives such as OpenVLA (Kim et al., 2025b) and _π_ 0 (Black et al., 2024) have adopted more efficient backbones to democratize VLA research. However, standard VLAs inherit a prohibitive computational burden by indiscriminately processing dense token grids where irrelevant background noise equal priority to critical end-effectors. This redundancy not only incurs prohibitive overhead due to the quadratic complexity of the attention mechanism, but also compromises the model’s accuracy and generalization capabilities. 

### **2.2. Efficient VLA Perception** 

**Visual Token Pruning.** Recent acceleration strategies seek to minimize the visual token budget through importancebased filtering or temporal reuse mechanisms (Kong et al., 2025). SparseVLM (Zhang et al., 2025) leverages trainingfree cross-modal attention to prune tokens, yet this semanticdriven selection inherently biases the model toward salient 

2 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 


_Figure 3._ Overview of the GridS Token Pruning framework. **(a) Standard Dense Representation** : An input image ( _HR_ and _WR_ denote the original image resolution) is processed by a visual encoder with ViT embeddings (Dosovitskiy et al., 2021) to generate dense visual tokens ( _H × W × C_ ), capturing full spatial details. **(b) GridS Token Pruning Module** : This module identifies salient regions to sample a sparse set of visual tokens ( _K × C_ ), which includes two Stage: (1) Global Coordinate Prediction, and (2) Grid Sampling with Geometry Injection. By ensuring the token count is significantly smaller than the dense spatial resolution ( _K ≪ H × W_ ), it achieves efficient representation for the downstream Transformer. 

objects while neglecting geometrically critical but semantically subtle regions. VLA-Cache (Xu et al., 2025b) exploits temporal redundancy by caching visual features across timesteps, but its reliance on discrete update thresholds over a fixed grid often fails to capture fine-grained geometric deformations during dynamic interaction. EfficientVLA (Yang et al., 2025) employs a learnable policy to dynamically drop background patches, but the resulting ragged tensors severely degrade hardware throughput due to inefficient memory coalescing. To sum up, these approaches are collectively constrained by their reliance on discrete selection over a fixed grid, introducing inevitable quantization errors that sacrifice the sub-patch spatial fidelity essential for precision control. 

**Asynchronous Execution.** Alternatively, system-level optimizations leverage asynchronous architectures to decouple the computationally intensive vision encoder from the high-frequency policy head, effectively masking perception latency during real-time deployment (Li et al., 2026b). Representative frameworks such as SmolVLA (Shukor et al., 2025), RTC (Black et al., 2026), and VLASH (Tang et al., 2025), employ multi-threaded pipelines or model compression strategies to parallelize visual processing while maintaining high control frequencies. However, this temporal decoupling inevitably introduces state staleness, where the policy actuates based on outdated observations, resulting in significant performance degradation and instability in highly dynamic manipulation tasks. 

### **2.3. Continuous and Deformable Sampling** 

Traditional Convolution Neural Network and Vision Transformer performs vector embedding on a standard grid (Doso- 

vitskiy et al., 2021). To overcome the limitations of fixed grids, deformable mechanisms (Dai et al., 2017; Zhu et al., 2021) and the Vision Transformer with Deformable Attention (DAT) (Xia et al., 2022) introduced learnable offsets, allowing the model to shift attention to flexible spatial locations. In addition, research in implicit neural representations, such as LIIF (Chen et al., 2021) and NeRF (Mildenhall et al., 2021), has demonstrated that modeling images as continuous functions enables feature recovery at arbitrary sub-pixel coordinates. 

## **3. GridS Pruning** 

In this section, we first analyze the computational bottlenecks inherent in standard VLA representations. We then present the **Differentiable Grid Sampler (GridS)** , detailing its pipeline and provide a mathematical derivation of the continuous sampling mechanism. Finally, we outline the end-to-end training objectives. 

### **3.1. Efficiency Bottleneck in Standard VLAs** 

Standard VLA architectures typically employ a frozen Vision Transformer (e.g., SigLIP (Zhai et al., 2023) or DINOv2 (Oquab et al., 2024)) to encode visual observations. As illustrated in Fig. 3 (a), an input image _I ∈_ R<sup>3</sup><sup>_×HR×WR_</sup> is patchified and encoded into a dense feature grid _Tdense ∈_ R<sup>_H×W ×C_</sup> , where _H × W_ represents the number of patches (for instance, DINOv2 generate 16 _×_ 16 = 256 tokens). 

While comprehensive, this dense representation introduces significant redundancy. Since the computational complexity of the downstream Transformer scales quadratically with sequence length ( _O_ ( _N_<sup>2</sup> )), processing hundreds of visual to- 

3 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

kens, most of which represent non-informative background noise, incurs prohibitive computational costs. This necessitates a pruning mechanism that can effectively discard irrelevant regions while preserving fine-grained details essential for robotic manipulation. 

### **3.2. The GridS Pipeline** 

To address above limitations, we propose GridS, a plugand-play module designed to compress dense features into a compact set of active tokens. As shown in Fig. 1 (b), the pipeline can divided to two stages: (1) Global Coordinate Prediction, and (2) Grid Sampling with Geometry Injection. 

**Global Coordinate Prediction.** Effective active grid sampling requires an understanding of the scene’s global semantic structure. Instead of processing local patches in isolation, we first aggregate the entire feature map _Tdense_ via global average pooling to obtain a context vector _z ∈_ R<sup>_C_</sup> : 


This operation provides a summary of the current observation, enabling the model to make informed decisions about where to attend. 

Furthermore, we employ a lightweight MLP to predict the locations of the most discriminative regions based on the context _z_ (see Fig. 3 (b-1)). Crucially, rather than outputting discrete grid indices, the network predicts _K_ sets of continuous, normalized coordinates _P ∈_ [0 _,_ 1]<sup>_K×_2</sup> as _P_ = _σ_ (MLP( _z_ )), where _σ_ is the Sigmoid function ensuring coordinates remain within the image bounds, and _K ≪_ ( _H × W_ ) represents the target number of active tokens. 

**Grid Sampling with Geometry Injection.** As shown in Fig. 3 (b-2), we sample from the predicted grid points in the dense tokens (detailed in Sec. 3.3) to generate sparse tokens _Fspa ∈_ R<sup>_K×C_</sup> , whereas the spatial structure of the original grid is disrupted. To restore geometric awareness, we use a Coordinate Encoder to map the predicted coordinates _P_ into position embeddings _Epos ∈_ R<sup>_K×C_</sup> . These embeddings are added to the sampled features to form the final Visual Sparse Tokens ( _Tspa_ ), which are then concatenated with language and action tokens for the downstream Transformer. 

### **3.3. Differentiable Bilinear Sampling** 

The core innovation of GridS lies in how it extracts features from the predicted coordinates _P_ . Unlike discrete selection strategies that suffer from quantization errors, we employ Differentiable Bilinear Sampling. 

As illustrated in Fig. 4, let _P_ ( _x, y_ ) be a predicted continuous 


_Figure 4._ **Differentiable Bilinear Sampling.** To extract features at a continuous coordinate _P_ ( _x, y_ ), the module computes a weighted interpolation of the four nearest integer neighbors. This operation enables sub-pixel feature extraction and ensures the sampling process is differentiable. 

coordinate in the feature map space. The sampling point typically does not align with the integer grid centers. To achieve sub-patch level accuracy, we define the value of the sampled token _Fsampled_ ( _x, y_ ) as a weighted interpolation of its four nearest neighbors on the original grid. 

Let the top-left neighbor be _P_ 1 = ( _xi, yi_ ) = ( _⌊x⌋, ⌊y⌋_ ). The offsets to the float coordinate are given by ∆ _x_ = _x − xi_ and ∆ _y_ = _y − yi_ . The interpolation weights _ωi_ for the four neighbors _{P_ 1 _, P_ 2 _, P_ 3 _, P_ 4 _}_ are computed as: 


The final sampled feature is the weighted sum of the neighbor features: 


This mechanism allows the model to extract sub-patch features. For instance, if a grasp point lies exactly on the edge shared by two patches, GridS can sample the exact boundary by assigning balanced weights to neighbors, whereas discrete selection would be forced to choose just one side. 


which implies that the MLP Layer for coordinate generation is not using a heuristic; it is actively trained by the downstream task to move sampling points toward regions that minimize the action prediction error. 

4 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

_Table 1._ Comparison of Model Efficiency and Performance on LIBERO dataset (Liu et al., 2023). We report efficiency metrics (visual tokens, FLOPs, completion time) and success rate across different task categories. We follow VLASH (Tang et al., 2025) to calculate the average duration and steps of task completion. All efficiency calculations are evaluated on a single RTX Pro6000 GPU and in 32 language tokens. The symbol ”<sup>_†_</sup> ” represents the training-free pruning methods, which forced to operate post-training at test time, leading to inherent performance degradation. (We note that VLA-Cache is not strictly a pruning method, but a token-cached speeding-up method. However, since many pruning methods are also compared with it, we also provide the result here.) 

|**Model**|**Ei**|**fficiency**(_↓_)|||**LIB**|**ERO Ac**|**curacy (**|**%)**||
|---|---|---|---|---|---|---|---|---|---|
||**Vis. Tokens**|**FLOPs (G)**|**Time (s)**|**Spatial**|**Object**|**Goal**|**Long**|**Avg. SR**|∆**SR**|
|OpenVLA (Kim et al.,2025b)|256|1956.19|26.08|84.7|88.4|79.2|53.7|76.5|-|
|CogACT (Li et al.,2024)|256|1891.24|13.80|97.2|98.0|90.2|88.8|93.6|-|
|SmolVLA (Shukor et al.,2025)|64|306.78|8.91|81.3|92.9|85.8|55.8|79.0|-|
|OpenVLA-OFT (Kim et al.,2025a)|512|3922.56|17.43|97.6|94.2|95.2|92.0|94.8|-|
|_π_0(Black et al.,2024)|256|216.01|8.17|97.2|98.8|96.0|85.6|94.4|-|
|_π_0+ FastV<sup>_†_ </sup>(Chen et al.,2024b)<br>|100|143.59|7.32|97.0|98.4|93.8|82.4|92.9|-1.5|
|_π_0+ SparseVLM<sup>_†_ </sup>(Zhang et al.,2025)|100|150.30|7.48|93.4|98.0|91.2|76.6|89.8|-4.6|
|_π_0+ VLA-Cache<sup>_†_ </sup>(Xu et al.,2025b)|256|188.12|7.52|95.2|97.6|96.6|85.6|93.8|-0.6|
|_π_0+ GridS16|16|51.65|6.05|98.0|99.2|96.4|90.2|96.0|+1.6|
|_π_0+ GridS4|4|43.61|5.86|96.6|99.4|96.4|89.6|95.5|+1.1|
|_π_0_._5(Intelligence et al.,2025)|256|249.76|8.54|98.4|98.0|97.6|92.8|96.7|-|
|_π_0_._5+ GridS16|16|83.84|6.76|98.6|98.8|98.4|95.2|97.7|+1.0|
|_π_0_._5+ GridS4|4|75.73|6.53|97.4|99.0|97.4|92.8|96.7|0.0|


### **3.4. Training Objectives and Joint Optimization** 

Existing token pruning methods are typically applied posttraining, which is described as a training-free method. Rather than an inherent advantage, this ”training-free” property is a forced compromise due to their non-differentiable designs, which inevitably degrades downstream performance. GridS integrated directly between the vision encoder and transformer, it is jointly optimized with the VLA policy during standard fine-tuning. It trains end-to-end using only the primary task loss—without any auxiliary supervision or ground-truth attention maps—making it seamlessly compatible with diverse paradigms, including auto-regressive and flow-matching models. Since downstream fine-tuning is already a prerequisite for VLAs, GridS introduces no extra pipeline steps. By heavily compressing visual tokens early in the forward pass, it significantly reduces the computational footprint and accelerates training compared to standard implementations. 

## **4. Experiments** 

We design experiments to investigate the following questions of GridS: 

1. **Comparative Advantage.** Does GridS offer a competitive edge over SOTA autoregressive and flow-matching pruning methods (Sec. 4.1 and Sec. 4.2)? 

2. **Generalization Capability.** Does the introduction of GridS perturb the generalization boundaries of the pretrained model (Sec. 4.2)? 

3. **Efficiency.** Does GridS enhance efficiency and mitigate computational overhead (Sec. 4.3)? 

4. **Mechanism of High Compression.** What enables GridS to maintain model capability despite a massive reduction ( _>_ 90%) in visual information (Sec. 4.4)? 

### **4.1. Simulation Experiments** 

### 4.1.1. LIBERO 

**Experiments setup.** We conduct experiments on the Libero simulation benchmark (Liu et al., 2023), specifically utilizing its four distinct suites ( _Spatial_ , _Object_ , _Goal_ , and _Long_ ) that contain 10 tasks each. These suites are designed to evaluate specific robotic capabilities: spatial understanding, object recognition, goal-directed behavior, and long-horizon planning, respectively. We select _π_ 0 (Black et al., 2024) and _π_ 0 _._ 5 (Intelligence et al., 2025), two flowmatching method as our baseline models. Leveraging GridS, we aggressively prune the visual tokens from the baseline count of 256 down to set budgets of 16, and 4. We evaluate the performance across all four suites, reporting the accuracy for the tasks, as well as the computational cost (FLOPs) and inference time associated with each token density. 

**Main Results.** Evaluations on LIBERO (Tab. 1) reveal a critical flaw in traditional post-training pruning: discretely dropping patches (FastV, SparseVLM) destroys spatial continuity, degrading _π_ 0 success rates by 1 _._ 5% and 4 _._ 6%. In contrast, GridS resolves this efficiency-performance tradeoff through joint optimization. Compressing the standard 256 tokens down to 16 reduces FLOPs by _∼_ 76% (to 51.6 G) and execution time by _>_ 2 _._ 1s, while actually yielding a 

5 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

_Table 2._ Evaluation on ALOHA benchmark (Zhao et al., 2023). We report the average success rates and enviroment rewards across 3 random seeds. The performance is evaluated on a RTX Pro6000 GPU. 

|Method|Visual Tokens|Times (s)|Env._↑_|Avg._↑_|Transfe|r Cube|Inser|tion|
|---|---|---|---|---|---|---|---|---|
||||Rewards|Accuracy (%)|Scripted|Human|Scripted|Human|
|_π_0(Black et al.,2024)|256|7.04|**2.44**|86.3|100.0|96.9|91.4|56.7|
|_π_0+ GridS|**16**|**6.32**|2.38|**87.0**|100.0|96.9|86.9|64.2|


_Figure 5._ **Real-world evaluation on the SO100 robot arm.** (a) Execution rollouts of three language-conditioned tasks: _Pick & Place_ , _Stack Cubes_ , and _Transfer Pen_ . (b) The corresponding Out-of-Distribution (OOD) test scenarios, featuring unseen distractor objects and variable spatial arrangements. We schemed 21 different OOD scenarios. (c) Quantitative comparison of Success Rate (%) and Execution Time (s). Our proposed method, **GridS** , consistently outperforms the baseline across all tasks. Notably, in the challenging _Stack Cubes_ task, GridS achieves a **+52.4%** increase in success rate and demonstrates superior generalization in OOD settings where the baseline frequently fails. 

+1 _._ 6% absolute improvement in average success rate. Notably, this gain peaks at +4.6% in the Long-horizon suite. Since long-horizon tasks are highly vulnerable to error accumulation, this confirms that our continuous resampling mechanism effectively filters visual distractors to produce robust state representations. Furthermore, these empirical advantages scale consistently to the stronger _π_ 0 _._ 5 backbone. 

### 4.1.2. ALOHA 

**Experiments setup.** Built upon MuJoCo (Todorov et al., 2012), the ALOHA benchmark (Zhao et al., 2023) targets fine-grained bimanual manipulation through two primary tasks: _Transfer Cube_ and _Bimanual Insertion_ . The dataset comprises 50 demonstrations per task, collected via scripted policies or human teleoperation, with an episode horizon 

of 400 steps (8 seconds). We evaluate each method using three distinct random seeds. For both the baseline and GridS-integrated models, we conducted a total of at least 300 evaluation episodes across the two tasks (covering 100 unique initializations) and reported the average success rate. 

**Main Results.** As shown in Tab. 2, GridS demonstrates exceptional efficiency-performance trade-offs. With only 16 visual tokens (vs. 256 in baseline), our method reduces inference latency by _∼_ 10% while achieving a better average success rate of 87 _._ 0%. Specifically, the success rate of GridS on the Transfer Cube task remains unchanged, which can be attributed to overfitting. In the challenging Insertion (Human) task, GridS significantly outperforms the baseline +7 _._ 5%, indicating improved robustness to the variability 

6 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

inherent in human demonstrations. This phenomenon becomes even more pronounced in real-world settings, a topic that will be elaborated upon in the following subsection. 

### **4.2. Real-world Experiments** 

**Experimental Setup and Dataset.** We conduct our experiments on a standard Linux workstation equipped with an NVIDIA RTX 3090 (24GB) GPU. The policy is based on the SmolVLA architecture (Shukor et al., 2025) and is trained with a batch size of 16 for 50,000 optimization steps. We evaluate the policy on three real-world manipulation tasks executed on a SO100 robot (Cadene et al., 2024), utilizing a dataset collected to cover varying complexities. The dataset is constructed as follows: (1) _Pick & Place_ : 83 episodes where the robot grasps a green cube from two distinct initial positions and places it into a green bowl; (2) _Transfer Pen_ : 74 episodes involving picking up a pen and placing it into a container; (3) _Stack Cubes_ : 75 episodes of stacking a green cube onto a blue cube, comprising 50 trajectories targeting the blue cube on the right side of the SO100 and 25 targeting the left side. While Fig. 5 (a) illustrates the ideal environment used for data collection and routine testing, we rigorously evaluate generalization using a benchmark of 21 distinct OOD scenarios (see Fig. 5 (b)), characterized by severe visual distractors and novel object arrangements to stress-test the policy’s robustness. 

**Main Results.** As reported in Fig. 5 (c), GridS consistently outperforms the baseline across all tasks. This performance gap is particularly pronounced in the most challenging Stack Cubes task, where our method achieves a 60.0% success rate compared to the baseline’s _∼_ 7.6%, yielding a substantial +52.4% improvement. Crucially, GridS exhibits superior robustness in OOD scenarios; while the baseline completely fails in the OOD settings for Transfer Pen and Stack Cubes, GridS maintains capable performance. Furthermore, our sparse tokenization translates to tangible efficiency gains, reducing the average execution time by up to 3.3s (Fig. 5 (c), right). These results confirm that GridS effectively eliminates redundancy to enhance both policy robustness and inference speed. 

### **4.3. Ablation Study** 

### 4.3.1. TOKEN COUNT 

**LIBERO.** We analyze the impact of the sampled token number _K_ on model efficiency and success rates (Tab. 1). While GridS generally improves performance, we observe task-specific sensitivities at extreme sparsity ( _K_ = 4). First, Spatial shows a 1.2% decline on _π_ 0 _._ 5. Although GridS can identify the most suitable location points based on image features, it still suffers from geometric ambiguity; precise spatial relationships require fine-grained boundary infor- 

_Table 3._ Ablation study of success rate of stacking cubes in realworld with different tokens. Results with SO100 robot. 

|Method|Vis. Tokens|Success Rate (%)|OOD SR (%)|
|---|---|---|---|
||4|0.0|0.0|
|GridS|8|28.5|19.1|
||**16**|**61.9**|**38.1**|
||32|19.0|0.0|
|Baseline|64|9.5|0.0|


_Figure 6._ **Performance Analysis.** We compare the inference latency (left) and computational cost (right) of the baseline method versus our proposed GridS pruning (16 tokens) across varying batch sizes. Solid and dashed lines denote the absolute values (left y-axis), while the dotted lines indicate the relative speedup and efficiency ratios (right y-axis). 

mation that may be lost when representing an object with only few tokens. Second, Long performance drops in the sparsest setting ( _K_ = 4). Since long-horizon tasks are vulnerable to error accumulation, transient sampling misses in intermediate frames—more likely under strict token budgets—can disrupt sequential execution. However, Object remains robust (peaking at 99.4% with _K_ = 4), validating that core semantic recognition requires minimal visual data. This can be attributed to the high instruction dependency of the task, where the sequence and position of object placement are relatively static. As a result, the model is more inclined to memorize these tokens during fine-tuning instead of comprehending the underlying logic. 

Given the severe overfitting tendencies associated with the LIBERO dataset, deriving fine-grained insights solely from these experiments is challenging. Consequently, we conducted further ablation studies in real-world settings to validate our method. We have reported more ablation experiments in the appendix. 

**Real-world.** To investigate the impact of token density on fine-grained manipulation, we evaluate the Stacking Cubes task across varying token budgets _K ∈{_ 4 _,_ 8 _,_ 16 _,_ 32 _}_ . 

As shown in Tab. 3, the results exhibit a distinct inverted U-shaped trend, pinpointing _K_ = 16 as the optimal trade- 

7 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

_Table 4._ Average training time per step (batch size equals 128). 

|**Model**|**Time (s/step)**_↓_|**Speedup**_↑_|
|---|---|---|
|_π_0 (Baseline)|14.32|1.0_×_|
|_π_0 +**GridS**|**4.21**|**3.4**_×_|
|_π_0_._5 (Baseline)|12.83|1.0_×_|
|_π_0_._5 +**GridS**|**4.41**|**2.9**_×_|


off between semantic sufficiency and redundancy reduction. At extreme sparsity ( _K_ = 4), the policy fails completely, indicating an information bottleneck where the representation lacks the geometric resolution required for precise alignment. Conversely, increasing _K_ beyond the optimal point leads to a sharp performance degradation (19.0% at _K_ = 32), trending towards the poor performance of baseline. This counter-intuitive drop suggests that excessive tokens introduce irrelevant background noise, which overwhelms the policy in precision-sensitive scenarios. By employing bilinear interpolation to compress the token count by a factor of 4, GridS ( _K_ = 16) functions as an effective feature sampler. This downsampling process significantly filters out redundancy and maximizes the signal-to-noise ratio, thereby facilitating robust manipulation. 

We further evaluated robustness across 21 diverse real-world OOD scenarios, where GridS16 demonstrates superior generalization (38.1%) compared to the complete failure of the baseline and other settings. Reducing the budget to _K_ = 8 causes the policy to suffer from severe positional bias, where successful manipulation is restricted exclusively to objects initialized on the left side due to insufficient spatial coverage. Conversely, increasing to _K_ = 32 introduces excessive visual noise that impairs terminal state recognition; specifically, while it can stack the cubes, the distraction prevents it from deciding to release the gripper, leading to task failure. 

### 4.3.2. COMPUTATIONAL EFFICIENCY ANALYSIS 

We benchmark the per-chunk inference time and computational cost across varying batch sizes from 1 to 128 on both _π_ 0 and _π_ 0 _._ 5 backbones (Fig. 6). Theoretically, GridS reduces the compute load, achieving a consistent FLOPs reduction ratio of approximate 4.2 _×_ for _π_ 0 and 3.0 _×_ for _π_ 0 _._ 5. Practically, we note that the wall-clock speedup is less pronounced at test-time inference (one batch), showing a modest _∼_ 1.2 _×_ gain. This is because the dense baseline is already highly optimized by JAX (Bradbury et al., 2018) compilation, leaving the runtime dominated by fixed kernel overheads rather than computation. Consequently, the benefits of GridS are most substantial in high-throughput settings where GPU compute is saturated, scaling rapidly to a 3.2 _×_ speedup at 128 batch size. The benefits of our method are further magnified throughout the training process. As Tab. 4, our method significantly accelerates the 


_Figure 7._ Visualization of Information Retention and Sampling Efficiency. We evaluate GridS on LIBERO, ALOHA, and RealWorld data. Left: Information Retention Maps demonstrate that our sampling strategy maintains high information retention (green), effectively covering the original feature space. Right: Token SelfSimilarity matrices reveal that while original features suffer from high spatial redundancy. 

optimization process, achieving a substantial 2.9 _×_ and 3.4 _×_ speedup for _π_ 0 _._ 5 and _π_ 0 respectively at a batch size of 128. 

### **4.4. Why GridS Works?** 

GridS adaptively samples global contextual cues using a learnable MLP and bilinear interpolation. Fig. 7 (right) illustrates the resulting reduction in spatial redundancy: while original feature maps display dense off-diagonal correlations, GridS yields a clean, diagonal-dominant structure, confirming that the bilinear sampling transforms redundant inputs into a compact, orthogonal token set. 

We visualize the corresponding semantic coverage via Information Retention maps (Fig. 7 left). A more detailed calculation method for retention map can be found in the appendix I. In visually simple environments like standard ALOHA, the model easily covers the clean scene, achieving near-uniform retention (0.9994). However, retention scores naturally drop in LIBERO (0.9709) and noisy Real-World scenarios (0.8610). While a strictly uniform map represents the theoretical ideal of zero information loss, preserving all visual input actually degrades performance in cluttered domains. To achieve high success rates in complex environments, the policy must discard irrelevant distractors. Therefore, the low-retention areas are not a flaw; they correctly reflect GridS actively filtering out background noise to concentrate its capacity on critical dynamic geometries. This inherent spatial regularization explains why GridS yields massive out-of-distribution (OOD) improvements over full- 

8 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

token baselines. We have analyzed more possible reasons in the Appendix G and K. 

## **5. Conclusion** 

In this work, we presented the Differentiable Grid Sampler (GridS), a plug-and-play module that enhances VLA efficiency by reformulating token compression as continuous, task-aware resampling. Crucially, our extensive experiments validate that complex manipulation tasks can be successfully executed with as few as 16 visual tokens, establishing a new benchmark for the lowest feasible token count reported to date. By replacing fixed-grid redundancy with high-fidelity sparse sampling, GridS not only reduces computational costs by 76% but also achieves significant gains in out-of-distribution robustness (+28 _._ 6%). 

## **Acknowledgement** 

This work was supported in part by the Australian Research Council under Projects DP240101848 and FT230100549. In addition, we express our gratitude to Jackie L. for his helpful discussions on this paper and to Iroha S. for her spiritual support. 

## **Impact Statement** 

The primary goal of this work is to enhance the computational efficiency of Vision-Language-Action models. By significantly reducing inference costs, our approach contributes to ’Green AI’ initiatives by lowering energy consumption and democratizes access to advanced robotic capabilities on consumer-grade hardware. Beyond general considerations regarding robotic automation, we do not foresee any specific negative consequences stemming directly from this work. 

## **References** 

- Bai, S., Song, W., Chen, J., Ji, Y., Zhong, Z., Yang, J., Zhao, H., Zhou, W., Zhao, W., Li, Z., et al. Towards a unified understanding of robot manipulation: A comprehensive survey. _arXiv preprint arXiv:2510.10903_ , 2025. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for general robot control. corr, abs/2410.24164, 2024. doi: 10.48550. _arXiv preprint ARXIV.2410.24164_ , 2024. 

- Black, K., Galliker, M., and Levine, S. Real-time execution of action chunking flow policies. _Advances in Neural Information Processing Systems_ , 38:33383–33407, 2026. 

- Bradbury, J., Frostig, R., Hawkins, P., Johnson, M. J., Leary, C., Maclaurin, D., Necula, G., Paszke, A., VanderPlas, 

J., Wanderman-Milne, S., et al. Jax: Composable transformations of python+ numpy programs, version 0.3. 13, 2018. _Online at http://github.com/jax-ml/jax (accessed on October 31, 2025)_ , 2018. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., Ibarz, J., Ichter, B., Irpan, A., Jackson, T., Jesmonth, S., Joshi, N., Julian, R., Kalashnikov, D., Kuang, Y., Leal, I., Lee, K.-H., Levine, S., Lu, Y., Malla, U., Manjunath, D., Mordatch, I., Nachum, O., Parada, C., Peralta, J., Perez, E., Pertsch, K., Quiambao, J., Rao, K., Ryoo, M., Salazar, G., Sanketi, P., Sayed, K., Singh, J., Sontakke, S., Stone, A., Tan, C., Tran, H., Vanhoucke, V., Vega, S., Vuong, Q., Xia, F., Xiao, T., Xu, P., Xu, S., Yu, T., and Zitkovich, B. Rt-1: Robotics transformer for real-world control at scale. In _arXiv preprint arXiv:2212.06817_ , 2022. 

- Cadene, R., Alibert, S., Soare, A., Gallouedec, Q., Zouitine, A., Palma, S., Kooijmans, P., Aractingi, M., Shukor, M., Aubakirova, D., Russi, M., Capuano, F., Pascal, C., Choghari, J., Moss, J., and Wolf, T. Lerobot: Stateof-the-art machine learning for real-world robotics in pytorch. https://github.com/huggingface/ lerobot, 2024. 

- Chen, B., Xu, Z., Kirmani, S., Ichter, B., Sadigh, D., Guibas, L., and Xia, F. Spatialvlm: Endowing vision-language models with spatial reasoning capabilities. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 14455–14465, 2024a. 

- Chen, L., Zhao, H., Liu, T., Bai, S., Lin, J., Zhou, C., and Chang, B. An image is worth 1/2 tokens after layer 2: Plug-and-play inference acceleration for large visionlanguage models. In _European Conference on Computer Vision_ , pp. 19–35. Springer, 2024b. 

- Chen, T., Chen, Z., Chen, B., Cai, Z., Liu, Y., Li, Z., Liang, Q., Lin, X., Ge, Y., Gu, Z., et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 

- Chen, Y., Liu, S., and Wang, X. Learning continuous image representation with local implicit image function. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 8628–8638, 2021. 

- Conklin, H., Hosking, T., Yi-Chern, T., Cohen, J. D., Leslie, S.-J., Griffiths, T. L., Bartolo, M., and Goldfarb-Tarrant, S. Learning is forgetting; LLM training as lossy compression. In _The Fourteenth International Conference on Learning Representations_ , 2026. 

9 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

- Dai, J., Qi, H., Xiong, Y., Li, Y., Zhang, G., Hu, H., and Wei, Y. Deformable convolutional networks. In _Proceedings of the IEEE international conference on computer vision_ , pp. 764–773, 2017. 

- Dosovitskiy, A., Beyer, L., Kolesnikov, A., Weissenborn, D., Zhai, X., Unterthiner, T., Dehghani, M., Minderer, M., Heigold, G., Gelly, S., Uszkoreit, J., and Houlsby, N. An image is worth 16x16 words: Transformers for image recognition at scale. In _International Conference on Learning Representations_ , 2021. 

- Driess, D., Xia, F., Sajjadi, M. S. M., Lynch, C., Chowdhery, A., Ichter, B., Wahid, A., Tompson, J., Vuong, Q., Yu, T., Huang, W., Chebotar, Y., Sermanet, P., Duckworth, D., Levine, S., Vanhoucke, V., Hausman, K., Toussaint, M., Greff, K., Zeng, A., Mordatch, I., and Florence, P. PaLMe: An embodied multimodal language model. In Krause, A., Brunskill, E., Cho, K., Engelhardt, B., Sabato, S., and Scarlett, J. (eds.), _Proceedings of the 40th International Conference on Machine Learning_ , volume 202 of _Proceedings of Machine Learning Research_ , pp. 8469–8488. PMLR, 23–29 Jul 2023. 

- Fei, S., Wang, S., Shi, J., Dai, Z., Cai, J., Qian, P., Ji, L., He, X., Zhang, S., Fei, Z., et al. Libero-plus: In-depth robustness analysis of vision-language-action models. _arXiv preprint arXiv:2510.13626_ , 2025. 

- Houlsby, N., Giurgiu, A., Jastrzebski, S., Morrone, B., De Laroussilhe, Q., Gesmundo, A., Attariyan, M., and Gelly, S. Parameter-efficient transfer learning for nlp. In _International conference on machine learning_ , pp. 2790– 2799. PMLR, 2019. 

- Hu, E. J., yelong shen, Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., and Chen, W. LoRA: Low-rank adaptation of large language models. In _International Conference on Learning Representations_ , 2022. 

- Hui, C., Huang, X., Xu, S., Wang, Y., You, S., Wang, F., Huang, T., and Xu, C. Seeing realism from simulation: Efficient video transfer for vision-language-action data augmentation. _arXiv preprint arXiv:2605.02757_ , 2026. 

- Intelligence, P., Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., et al. _π_ 0. 5: a vision-language-action model with open-world generalization, 2025. _URL https://arxiv. org/abs/2504.16054_ , 1(2):3, 2025. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025a. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E. P., Sanketi, 

P. R., Vuong, Q., Kollar, T., Burchfiel, B., Tedrake, R., Sadigh, D., Levine, S., Liang, P., and Finn, C. Openvla: An open-source vision-language-action model. In Agrawal, P., Kroemer, O., and Burgard, W. (eds.), _Proceedings of The 8th Conference on Robot Learning_ , volume 270 of _Proceedings of Machine Learning Research_ , pp. 2679–2713. PMLR, 06–09 Nov 2025b. 

- Kirillov, A., Mintun, E., Ravi, N., Mao, H., Rolland, C., Gustafson, L., Xiao, T., Whitehead, S., Berg, A. C., Lo, W.-Y., et al. Segment anything. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 4015–4026, 2023. 

- Kong, Z., Li, Y., et al. Token reduction should go beyond efficiency in generative models–from vision, language to multimodality. _arXiv preprint arXiv:2505.18227_ , 2025. 

- Li, Q., Liang, Y., Wang, Z., Luo, L., Chen, X., Liao, M., Wei, F., Deng, Y., Xu, S., Zhang, Y., et al. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 

- Li, W., Su, X., Cao, Y., Xu, H., Xia, X., You, S., Chen, Y., and Xu, C. Sentinel-vla: A metacognitive vla model with active status monitoring for dynamic reasoning and error recovery, 2026a. 

- Li, W., Su, X., Niu, D., Cao, Y., Xu, H., Qu, Z., Fan, L., You, S., and Xu, C. Vla-attc: Adaptive test-time compute for vla models with relative action critic model, 2026b. 

- Li, W., Zhang, R., Shao, R., Fang, Z., Zhou, K., Tian, Z., and Nie, L. Semanticvla: Semantic-aligned sparsification and enhancement for efficient robotic manipulation. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , 2026c. 

- Liang, W., Zhou, R., Ma, Y., Zhang, B., Li, S., Liao, Y., and Kuang, P. Large model empowered embodied ai: A survey on decision-making and embodied learning. _arXiv preprint arXiv:2508.10399_ , 2025. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

- Mildenhall, B., Srinivasan, P. P., Tancik, M., Barron, J. T., Ramamoorthi, R., and Ng, R. Nerf: Representing scenes as neural radiance fields for view synthesis. _Communications of the ACM_ , 65(1):99–106, 2021. 

- Mu, Y., Chen, T., Chen, Z., Peng, S., Lan, Z., Gao, Z., Liang, Z., Yu, Q., Zou, Y., Xu, M., et al. Robotwin: Dual-arm robot benchmark with generative digital twins. In _Proceedings of the computer vision and pattern recognition conference_ , pp. 27649–27660, 2025. 

10 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

- Oquab, M., Darcet, T., Moutakanni, T., Vo, H. V., Szafraniec, M., Khalidov, V., Fernandez, P., HAZIZA, D., Massa, F., El-Nouby, A., Assran, M., Ballas, N., Galuba, W., Howes, R., Huang, P.-Y., Li, S.-W., Misra, I., Rabbat, M., Sharma, V., Synnaeve, G., Xu, H., Jegou, H., Mairal, J., Labatut, P., Joulin, A., and Bojanowski, P. DINOv2: Learning robust visual features without supervision. _Transactions on Machine Learning Research_ , 2024. ISSN 2835-8856. Featured Certification. 

- Pei, X., Chen, Y., Xu, S., Wang, Y., Shi, Y., and Xu, C. Action-aware dynamic pruning for efficient visionlanguage-action manipulation. In _The Fourteenth International Conference on Learning Representations_ , 2026. 

- Pertsch, K., Stachowicz, K., Ichter, B., Driess, D., Nair, S., Vuong, Q., Mees, O., Finn, C., and Levine, S. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- Qu, D., Song, H., Chen, Q., Yao, Y., Ye, X., Ding, Y., Wang, Z., Gu, J., Zhao, B., Wang, D., et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- Shukor, M., Aubakirova, D., Capuano, F., Kooijmans, P., Palma, S., Zouitine, A., Aractingi, M., Pascal, C., Russi, M., Marafioti, A., et al. Smolvla: A vision-languageaction model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

- Tang, J., Sun, Y., Zhao, Y., Yang, S., Lin, Y., Zhang, Z., Hou, J., Lu, Y., Liu, Z., and Han, S. Vlash: Real-time vlas via future-state-aware asynchronous inference. _arXiv preprint arXiv:2512.01031_ , 2025. 

- Todorov, E., Erez, T., and Tassa, Y. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ international conference on intelligent robots and systems_ , pp. 5026–5033. IEEE, 2012. 

- Xia, Z., Pan, X., Song, S., Li, L. E., and Huang, G. Vision transformer with deformable attention. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 4794–4803, 2022. 

- Xu, H., Ding, J., Xu, J., Wang, R., Chen, J., Mai, J., Fu, Y., Ghanem, B., Xu, F., and Elhoseiny, M. Diffusion-based imaginative coordination for bimanual manipulation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 11469–11479, 2025a. 

- Xu, R., Wang, Y., Luo, Y., and Du, B. Rethinking visual token reduction in lvlms under cross-modal misalignment. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 40, pp. 27323–27331, 2026. 

- Xu, S., Wang, Y., Xia, C., Zhu, D., Huang, T., and Xu, C. Vla-cache: Efficient vision-language-action manipulation via adaptive token caching. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025b. 

- Xu, S., Wang, Z., Wang, Y., Xia, C., Huang, T., and Xu, C. Affordance field intervention: Enabling vlas to escape memory traps in robotic manipulation. _arXiv preprint arXiv:2512.07472_ , 2025c. 

- Yang, Y., Wang, Y., Wen, Z., Zhongwei, L., Zou, C., Zhang, Z., Wen, C., and Zhang, L. Efficientvla: Training-free acceleration and compression for vision-language-action models. In Belgrave, D., Zhang, C., Lin, H., Pascanu, R., Koniusz, P., Ghassemi, M., and Chen, N. (eds.), _Advances in Neural Information Processing Systems_ , volume 38, pp. 40891–40914. Curran Associates, Inc., 2025. 

- Yuan, W., Duan, J., Blukis, V., Pumacay, W., Krishna, R., Murali, A., Mousavian, A., and Fox, D. Robopoint: A vision-language model for spatial affordance prediction in robotics. In Agrawal, P., Kroemer, O., and Burgard, W. (eds.), _Proceedings of The 8th Conference on Robot Learning_ , volume 270 of _Proceedings of Machine Learning Research_ , pp. 4005–4020. PMLR, 06–09 Nov 2025. 

- Zhai, X., Mustafa, B., Kolesnikov, A., and Beyer, L. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 11975–11986, 2023. 

- Zhang, Y., Fan, C.-K., Ma, J., Zheng, W., Huang, T., Cheng, K., Gudovskiy, D. A., Okuno, T., Nakata, Y., Keutzer, K., and Zhang, S. SparseVLM: Visual token sparsification for efficient vision-language model inference. In Singh, A., Fazel, M., Hsu, D., Lacoste-Julien, S., Berkenkamp, F., Maharaj, T., Wagstaff, K., and Zhu, J. (eds.), _Proceedings of the 42nd International Conference on Machine Learning_ , volume 267 of _Proceedings of Machine Learning Research_ , pp. 74840–74857. PMLR, 13–19 Jul 2025. 

- Zhao, T. Z., Kumar, V., Levine, S., and Finn, C. Learning fine-grained bimanual manipulation with low-cost hardware. In _ICML Workshop on New Frontiers in Learning, Control, and Dynamical Systems_ , 2023. 

- Zheng, J., Li, J., Wang, Z., Liu, D., Kang, X., Feng, Y., Zheng, Y., Zou, J., Chen, Y., Zeng, J., et al. X-vla: Soft-prompted transformer as scalable crossembodiment vision-language-action model. _arXiv preprint arXiv:2510.10274_ , 2025. 

- Zhong, Y., Huang, X., Li, R., Zhang, C., Chen, Z., Guan, T., Zeng, F., Lui, K. N., Ye, Y., Liang, Y., et al. Dexgraspvla: A vision-language-action framework towards general dexterous grasping. In _Proceedings of the AAAI Conference_ 

11 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

_on Artificial Intelligence_ , volume 40, pp. 18836–18844, 2026. 

- Zhu, X., Su, W., Lu, L., Li, B., Wang, X., and Dai, J. Deformable _{_ detr _}_ : Deformable transformers for end-to-end object detection. In _International Conference on Learning Representations_ , 2021. 

- Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. 

12 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

# **Appendix** 

## **A. Real-World Experimental Setup** 

We evaluate our method on a real-world teleoperation platform designed for precise manipulation tasks. Figure 8 illustrates the hardware configuration used for policy deployment. 

**Robot Manipulators.** We utilize the **LeRobot SO-100** , a 6-DoF low-cost open-source robotic arm, as the follower robot for execution. For data collection, we employ a leader-follower teleoperation scheme where a second identical SO-100 arm captures precise joint positions. These positions are mapped directly to the follower arm to ensure smooth demonstration recording. 

**Vision System.** Our vision-language-action model processes visual feedback from a multi-view camera setup. **It is important to note that while the hardware supports depth sensing, our policy operates exclusively on RGB images.** 

- **Front(Third-Person) View:** An **Intel RealSense D435** camera is mounted diagonally above the robot at approximately 45 degrees relative to the workspace. This viewpoint provides a holistic understanding of the scene layout and object positions relative to the robot base. 

- **Wrist(Egocentric) View:** An **Intel RealSense D405** camera is mounted directly on the robot’s wrist. This enables close-up observation of the end-effector gripper and the final contact between the gripper and objects. 


_Figure 8._ **Real-World Hardware Setup.** The image displays the LeRobot SO-100 follower arm used for policy execution. Visual inputs come from a fixed Intel RealSense D435 providing global scene context and a wrist-mounted Intel RealSense D405 capturing fine-grained local details. The policy operates using only RGB streams from these sensors. 

**Real World Tasks.** We provide comprehensive video demonstrations comparing our proposed GridS against the unpruned dense baseline SmolVLA and a standard token pruning baseline. All real-world experiments utilize the LeRobot SO-100 setup described above. 

- **Pick & Place (83 episodes):** The robot grasps a green cube from two distinct initial positions and places it into a green bowl. This task serves as a benchmark for motion quality. Thanks to the differentiable nature of GridS, the policy produces smooth trajectories, effectively filtering out high-frequency control noise while maintaining a stable path towards the target. 

- **Transfer Pen (74 episodes):** A high-precision task involving picking up a thin marker pen and placing it into a cup container. This task rigorously tests the model’s fine-grained accuracy and capability for delicate manipulation. Instead of mechanically memorizing training trajectories, GridS demonstrates robust generalization by precisely sampling features from the small target object (the pen). This allows for accurate end-effector alignment even with slight positional variations, ensuring the gripper successfully interacts with the thin geometry. 

13 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

- **Stack Cubes (75 episodes):** A **multi-stage task** requiring the robot to stack a green cube onto a blue cube. The dataset includes 50 trajectories targeting the right side and 25 targeting the left side. This task demands strong **spatial reasoning** and the ability to handle **longer-horizon sequences** (approach _→_ grasp _→_ align _→_ stack). The model must understand the relative 3D relationship between the held object and the target base, maintaining this spatial context over a longer execution timeline than simple pick-and-place tasks. 

**Out-of-Distribution (OOD) Evaluation.** To rigorously evaluate model robustness beyond the training distribution, we established over 20 distinct out-of-distribution (OOD) tests for each task. Although training data was collected under consistent conditions, these evaluation scenarios introduce severe visual and spatial perturbations. We categorized these perturbations into seven key example types to stress-test model generalization capabilities (as shown in Figure 9): 

- **Cluttered Background:** Replace clean tabletops with patterned fabrics and remove backdrops from front-view backgrounds to test visual attention. 

- **Novel Target Instances:** Place standard training cubes on unfamiliar backgrounds to introduce confusion. 

- **Removing Training Priors:** Eliminate auxiliary objects (e.g., standard background cubes) present throughout training to ensure the model relies on targets rather than environmental landmarks. 

- **Unknown Distractions:** Introduce diverse, irrelevant clutter (e.g., tools, snacks) into the workspace to create visual interference. 

- **Spatial extrapolation:** Position target objects in locations not covered by demonstration data. 

- **Adversarial layouts:** Place distractors near target objects or along optimal trajectory paths. 

- **Compound perturbations:** Combine visual clutter, novel objects, and unseen spatial layouts simultaneously to maximize task difficulty. 


_Figure 9._ **Visualization of OOD Scenarios.** We selected seven examples per task to demonstrate how we evaluated the strategy across over 20 scenarios categorized into seven types of perturbations: cluttered backgrounds, novel objects, removed training scenes, and unseen spatial layouts. Across these settings, GridS demonstrated stronger robustness compared to baseline models. 

## **B. Hyperparameter Settings** 

We present the detailed training hyperparameters used for fine-tuning the VLA models in our experiments in Table 5. To ensure rigorous and fair comparisons, we employ a unified set of hyperparameters across all methods—including the unpruned baseline model, the standard token pruning approach, and our proposed GridS model—which are also applied to real-world manipulation tasks. These parameters are empirically optimized to balance training stability and convergence efficiency while effectively preventing overfitting. 

14 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

_Table 5._ Hyperparameters derived from configuration. 

|**Model**|SmolVLA|_π_0(LIBERO/ALOHA)|_π_0_._5(LIBERO)|
|---|---|---|---|
|_Training Configuration_||||
|Batch Size|16|32|128|
|Training Steps|50,000|30,000|30,000|
|Action Chunk Size|50|10|10|
|Input Image Resolution|512_×_512|224_×_224|224_×_224|
|_Optimizer (AdamW)_||||
|Learning Rate (LR)|1e-4|5e-5|5e-5|
|Betas||[0.9, 0.95]||
|Weight Decay||1e-10||
|Grad ClipNorm|10|1.0|1.0|
|_Learning Rate Scheduler_||||
|Type||Cosine Decay with Warm|up|
|Warmup Steps|1,000|10,000/1,000|10,000|
|Peak Learning Rate|1e-4|5e-5|5e-5|
|Decay Learning Rate|2.5e-6|5e-5/2.5e-6|5e-5|
|DecaySteps|50,000|30,000 / 15,000|30,000|


## **C. Video Demonstrations and Qualitative Analysis** 

We provide comprehensive video demonstrations in the supplementary material to qualitatively validate the results reported in the main paper. These videos offer a side-by-side comparison between our proposed **GridS** and the strongest baseline (SmolVLA) across both standard and Out-of-Distribution (OOD) settings. 

**Standard Benchmarks: Efficiency and Smoothness.** In the standard _Pick & Place_ , _Transfer Pen_ , and _Stack Cubes_ tasks, the demonstrations highlight the significant performance gap between the two models. 

- **Completion Speed:** Viewers can observe that the GridS-controlled robot completes tasks noticeably faster than the baseline. The reduced computational overhead results in more fluid and continuous motion, avoiding the ”stop-and-go” pauses often observed in the baseline execution. 

- **Motion Quality:** Despite pruning 90% of the visual tokens, GridS maintains precise end-effector control, effectively eliminating the jitter caused by discrete quantization errors in fixed-grid baselines. 

**OOD Scenarios: True Attention vs. Rote Memorization.** The videos also showcase the deployment of both models in the challenging OOD scenarios described in Appendix. The visual comparison reveals a fundamental difference in policy behavior. 

- **Genuine Attention vs. Mechanical Memorization:** A critical observation is the difference in failure modes. The baseline often behaves as if executing a **mechanically memorized action sequence** , failing blindly when the target object is shifted or the environment changes. In sharp contrast, GridS demonstrates **genuine visual attention** . It can be seen actively ”looking” for the target, dynamically adjusting its trajectory to lock onto the object’s actual position rather than replaying a fixed path. 

- **Robustness in Complex Scenes:** Under high visual load (e.g., cluttered desks), GridS successfully filters out background noise to focus on the target, maintaining **real-time responsiveness** (low latency). The baseline, conversely, often struggles to distinguish the target from the distractors, leading to freezing or incorrect actuation. 

The full video demonstrations can be found in the Github link. 

## **D. Robustness to Camera Viewpoint Loss** 

To evaluate the generalization capability and robustness of GridS under sensor failure scenarios, we conducted a ”Viewpoint Loss” experiment on the LIBERO benchmark. In this setting, models were trained using full visual observations (Third- 

15 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

_Table 6._ **Robustness to Viewpoint Loss (Wrist-Only Inference).** Models are trained with both Base and Wrist cameras but evaluated using _only the Wrist camera_ . We compare two missing-modality strategies: Masking tokens vs. Black Image input. GridS ( _K_ = 16) demonstrates superior robustness compared to the Baseline. 

|**Missing Strategy**|**Task Suite**|**Baseline (Acc)**|**GridS (Acc)**|
|---|---|---|---|
||Spatial|0.66|**0.92**(+0.26)|
|**Token Maskin**|Object|0.88|**0.92**(+0.04)|
|**g**|Goal|0.76|**0.94**(+0.18)|
||Long|0.30|**0.70**(+0.40)|
||Spatial|0.62|**0.82**(+0.20)|
|**Black Imae**|Object|0.84|**0.92**(+0.08)|
|**g**|Goal|0.62|**0.68**(+0.06)|
||Long|0.18|**0.44**(+0.26)|


person Front + Egocentric Wrist cameras) but evaluated using only the Wrist camera during inference. We tested two strategies for simulating the missing base camera: (1) Masking: explicitly masking the visual tokens corresponding to the base view; and (2) Black Image: replacing the base view input with a blank black image. 

As shown in Table 7, the standard Baseline suffers catastrophic performance degradation when the global view is removed, particularly in spatial reasoning (spatial) and long-horizon (10) tasks (e.g., dropping to 18% success rate in LIBERO-10 with black images). This suggests the Baseline over-relies on the static global view and fails to leverage fine-grained cues from the wrist camera. 

In contrast, GridS maintains remarkably high success rates across all tasks despite the missing modality. In the ”Masking” setting, GridS achieves 0.92 on Spatial tasks (vs. Baseline 0.66) and 0.70 on Long-horizon tasks (vs. Baseline 0.30). This demonstrates that GridS’s active sampling mechanism effectively reduces dependency on specific viewpoints by learning to extract task-relevant features (e.g., object geometry and interaction points) directly from the available wrist-view tokens, ensuring robust control even in strictly egocentric environments. 

We further conducted ablation experiments on the wrist-only (black image form) on GridS: 

_Table 7._ Success rates on LIBERO dataset using strictly wrist-camera visual inputs (third-person view masked). Performance exhibits high sensitivity and non-linear fluctuations with respect to the token budget _K_ . 

|**Token Budget**(_K_)|**Spatial**|**Object**|**Goal**|**Long**|
|---|---|---|---|---|
|_K_ = 1|15.2|1.8|9.0|0.8|
|_K_ = 4|79.2|90.2|63.0|53.2|
|_K_ = 6|59.0|67.4|57.2|44.6|
|_K_ = 8|68.0|63.8|48.8|18.6|
|_K_ = 10|59.2|25.0|26.8|18.4|
|_K_ = 12|76.8|83.6|56.4|42.0|
|_K_ = 16|**80.6**|84.8|68.0|50.8|
|_K_ = 32|71.6|**95.0**|**72.2**|**55.4**|


**Empirical Observations:** The results demonstrate a highly non-linear, oscillating trend rather than a smooth scaling curve. At extreme sparsity ( _K_ = 1), the policy predictably fails due to severe information loss. Surprisingly, performance peaks dramatically at _K_ = 4 across all suites. However, as the token budget slightly increases to intermediate values ( _K ∈{_ 6 _,_ 8 _,_ 10 _}_ ), the success rate experiences a catastrophic drop. The performance then robustly recovers at larger token budgets ( _K ≥_ 12). 

**Possible Interpretations:** While the exact underlying mechanics of this fluctuation remain an open question for future investigation, we hypothesize that it stems from the complex interaction between the constrained field of view (FOV) of the wrist camera and the spatial optimization dynamics of GridS: 

- _Geometric Symmetry and Optimization Landscape:_ The high-performing budgets (e.g., _K ∈{_ 4 _,_ 16 _,_ 32 _}_ ) correspond 

16 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

to numbers that easily form symmetric spatial arrangements (such as 2 _×_ 2 or 4 _×_ 4 conceptual grids). The coordinate predictor might inherently favor optimizing symmetric, evenly distributed continuous points. Non-standard budgets ( _K ∈{_ 6 _,_ 8 _,_ 10 _}_ ) may force the network into asymmetric local minima during end-to-end training, thereby disrupting spatial awareness. 

- _Wrist Camera FOV Bottleneck:_ Without the global context from the third-person camera, the wrist camera view is heavily dominated by the gripper and the immediate target object. A minimal budget like _K_ = 4 might perfectly align with the core local geometries (e.g., the two gripper tips and two target keypoints). When given slightly more tokens ( _K ∈{_ 6 _,_ 8 _,_ 10 _}_ ), the model may attempt to track out-of-focus background details to infer global goals, leading to attention distraction. When _K ≥_ 16, the token capacity becomes sufficient to redundantly encode both local structures and background cues without severe feature conflicts. 

## **E. More experiments** 

### **E.1. LIBERO-Plus** 

### E.1.1. OVERVIEW OF THE LIBERO-PLUS BENCHMARK 

Current VLA models exhibit highly saturated performance on standard robotic manipulation benchmarks such as the original LIBERO. However, these aggregate success rates often mask the inherent vulnerability of the models when deployed in dynamic, real-world environments. To rigorously evaluate the robustness and generalization capabilities of these policies, the LIBERO-PLUS benchmark systematically extends the original dataset by introducing controlled, cross-dimensional perturbations designed to stress-test models against realistic distribution shifts (Fei et al., 2025). 

Specifically, LIBERO-PLUS incorporates seven core perturbation dimensions, which are further subdivided into 21 low-level components, to comprehensively assess the robustness of multimodal inputs across vision, state, and language. These dimensions encompass variations in camera viewpoints (e.g., modifying distance, spherical position, and orientation), robot initial states via random joint angle perturbations, and language instructions, which are rewritten using Large Language Models to introduce distracting contexts or alter reasoning complexity. Furthermore, the benchmark rigorously evaluates visual robustness by modifying light conditions (such as diffuse color, direction, and shadows), background textures of scenes and surfaces, sensor noise (simulating motion blur, Gaussian blur, and fog), and object layouts by introducing unseen confounding objects and perturbing target object poses. 

Beyond its extensive coverage of perturbation factors, the benchmark is notably large in scale, comprising 10,030 evaluation tasks. To provide fine-grained insights into when and how VLA models fail, LIBERO-PLUS introduces a dynamic difficulty stratification mechanism. All tasks are pre-evaluated using four representative state-of-the-art models and are categorized into five difficulty levels (Level-1 to Level-5) based on the number of models that successfully complete them. In addition to this comprehensive evaluation suite, the benchmark provides a generalized training dataset containing over 20,000 successful trajectories, enabling researchers to investigate whether mixed fine-tuning on generalized data can substantially mitigate performance degradation and enhance policy robustness. 

### E.1.2. IN-DOMAIN EVALUATION ON THE LIBERO-PLUS BENCHMARK 

We conduct an in-domain evaluation where both the dense baseline ( _π_ 0 _._ 5) and our compressed model ( _π_ 0 _._ 5 + GridS32) are directly co-trained on the augmented LIBERO-PLUS dataset and tested on its corresponding evaluation suite. The quantitative results across the four suites, broken down by perturbation dimension and difficulty level, are presented in Table 8a. 

**1. Remarkable Parameter and Data Efficiency under In-Domain Augmented Training.** When co-trained on the augmented LIBERO-PLUS dataset, the dense baseline ( _π_ 0 _._ 5) recovers from its previously catastrophic OOD failures (e.g., Camera Viewpoints in Spatial jumps from 67.0% to 94.9%). Given this highly saturated in-domain setting, it is remarkable that GridS successfully retains competitive overall performance across all suites (only a marginal degradation of 1.1% to 3.0% on average). Operating on just 32 visual tokens—an 87.5% reduction in visual density compared to the baseline’s 256 tokens—GridS proves that even when the training distribution is highly complex and perturbed, a vast majority of standard visual tokens are mathematically redundant for acquiring dexterous manipulation policies. 

**2. The Persistent Advantage of Information Bottleneck in Visual Perturbations.** The most profound observation from this in-domain evaluation (Panel A) is that despite the baseline being explicitly trained on all perturbation types, GridS _still_ 

17 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

_Table 8._ In-Domain Evaluation on the LIBERO-PLUS Benchmark. Both the dense baseline ( _π_ 0 _._ 5) and the compressed model ( _π_ 0 _._ 5 + GridS32) are co-trained on the augmented dataset. Performance is broken down by perturbation dimension (Panel A) and task difficulty level (Panel B) across four suites. 

#### _(a)_ LIBERO-Spatial 

|**Metric Category**<br>_π_0_._5**Baseline**<br>_π_0_._5**+ GridS**32|∆|
|---|---|
|_Panel A: By Perturbation Dimension_||
|Background Textures<br>98.4<br>98.4|**0.0**|
|Camera Viewpoints<br>94.9<br>97.9|**+3.0**|
|Language Instructions<br>82.8<br>77.9|-4.9|
|Light Conditions<br>92.5<br>96.2|**+3.7**|
|Objects Layout<br>92.2<br>90.1|-2.1|
|Robot Initial States<br>77.1<br>69.1|-8.0|
|Sensor Noise<br>94.6<br>96.3|**+1.7**|
|_Panel B: By Task Difficulty Level_||
|Level 1 (Easiest)<br>91.2<br>92.3|+1.1|
|Level 2<br>92.5<br>93.4|+0.9|
|Level 3<br>91.3<br>90.3|-1.0|
|Level 4<br>89.1<br>85.9|-3.2|
|Level 5 (Hardest)<br>75.4<br>66.0|-9.4|
|**Overall**<br>**90.0**<br>**88.8**|**-1.2**|


#### _(b)_ LIBERO-Object 

|**Metric Category**<br>_π_0_._5**Baseline**|_π_0_._5**+ GridS**32|∆|
|---|---|---|
|_Panel A: By Perturbation_|_Dimension_||
|Background Textures<br>98.4|98.8|**+0.4**|
|Camera Viewpoints<br>98.0|98.5|**+0.5**|
|Language Instructions<br>85.9|87.0|**+1.1**|
|Light Conditions<br>97.0|98.7|**+1.7**|
|Objects Layout<br>90.1|86.4|-3.7|
|Robot Initial States<br>60.1|53.5|-6.6|
|Sensor Noise<br>98.6|98.8|**+0.2**|
|_Panel B: By Task Difficu_|_ilty Level_||
|Level 1 (Easiest)<br>95.1|93.9|-1.2|
|Level 2<br>94.3|95.9|+1.6|
|Level 3<br>91.9|90.7|-1.2|
|Level 4<br>86.7|85.2|-1.5|
|Level 5 (Hardest)<br>80.0|77.0|-3.0|
|**Overall**<br>**89.0**|**87.9**|**-1.1**|


#### _(c)_ LIBERO-Goal 

|**Metric Category**<br>_π_0_._5**Baseline**|_π_0_._5**+ GridS**32|∆|
|---|---|---|
|_Panel A: By Perturbation_|_Dimension_||
|Background Textures<br>95.4|97.2|**+1.8**|
|Camera Viewpoints<br>93.9|96.1|**+2.2**|
|Language Instructions<br>67.8|64.4|-3.4|
|Light Conditions<br>96.4|96.1|-0.3|
|Objects Layout<br>73.2|64.2|-9.0|
|Robot Initial States<br>78.0|75.3|-2.7|
|Sensor Noise<br>94.2|95.3|**+1.1**|
|_Panel B: By Task Diffic_|_iulty Level_||
|Level 1 (Easiest)<br>94.7|95.0|+0.3|
|Level 2<br>91.6|92.8|+1.2|
|Level 3<br>91.3|89.0|-2.3|
|Level 4<br>82.0|80.7|-1.3|
|Level 5 (Hardest)<br>63.5|57.6|-5.9|
|Unknown<br>96.7|94.2|-2.5|
|**Overall**<br>**84.3**|**82.6**|**-1.7**|


#### _(d)_ LIBERO-Long (10) 

|**Metric Category**<br>_π_0_._5**Baseline**|_π_0_._5**+ GridS**32|∆|
|---|---|---|
|_Panel A: By Perturbation_|_Dimension_||
|Background Textures<br>92.7|89.6|-3.1|
|Camera Viewpoints<br>88.5|90.7|**+2.2**|
|Language Instructions<br>82.8|74.2|-8.6|
|Light Conditions<br>92.0|95.6|**+3.6**|
|Objects Layout<br>86.5|81.4|-5.1|
|Robot Initial States<br>65.4|55.7|-9.7|
|Sensor Noise<br>88.4|88.6|**+0.2**|
|_Panel B: By Task Difficu_|_ilty Level_||
|Level 1 (Easiest)<br>90.5|84.3|-6.2|
|Level 2<br>92.2|88.0|-4.2|
|Level 3<br>87.6|83.1|-4.5|
|Level 4<br>83.7|81.5|-2.2|
|Level 5 (Hardest)<br>75.5|75.3|-0.2|
|**Overall**<br>**84.6**|**81.6**|**-3.0**|


18 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

_consistently outperforms_ the dense baseline across dimensions with extreme visual variance: 

- _Camera Viewpoints & Light Conditions:_ GridS achieves strictly superior performance in Camera Viewpoints (+3.0% in Spatial, +2.2% in Goal/10) and Light Conditions (+3.7% in Spatial, +3.6% in LIBERO-10). 

- _Sensor Noise:_ GridS also systematically outperforms the baseline under various sensor noise conditions (e.g., +1.7% in Spatial, +1.1% in Goal). 

This phenomenon corroborates that the Information Bottleneck enforced by GridS is not merely an OOD generalization trick; it actively distills the representation during training. By aggressively pruning dense visual grids, GridS inherently prevents the transformer from assigning attention weights to unpredictable backgrounds, shadow artifacts, or noise pixels. Instead, it compels the model to reliably track robust, invariant causal geometries (such as the end-effector and target object contours) even within the training distribution. 

**3. Analyzing the Resolution Trade-off (Where GridS Degrades).** The slight average performance drop (e.g., -1.2% in Spatial) can be directly attributed to dimensions that necessitate extremely high-resolution, fine-grained visual details: 

- _Robot Initial States:_ GridS exhibits performance drops (-2.7% to -9.7%) when the initial joint configuration is heavily randomized. To plan complex recovery trajectories from awkward initial poses, the model requires full-body kinematic awareness. Compressing the visual input to 32 tokens slightly over-smooths the proprioceptive boundary of the robot arm. 

- _Objects Layout & Language Instructions:_ GridS also experiences slight degradations (-2.1% to -9.0%) when the scene is cluttered with confounding objects or when language instructions require discriminating subtle textural differences. A strict token budget inherently sacrifices the fine-grained semantic resolution needed to perfectly ground highly complex linguistic queries against tiny distractors. 

**Conclusion: Efficiency Meets Distillation.** In summary, the in-domain LIBERO-PLUS results complete the theoretical validation of GridS. While an 87.5% reduction in token density predictably entails a marginal cost in ultra-fine-grained kinematic and semantic resolution, it simultaneously functions as an innate spatial regularizer. By systematically outperforming the fully-augmented dense baseline in Camera, Noise, and Light perturbations, GridS cements its status as a paradigm that bridges massive computational acceleration with superior visual feature distillation. 

### E.1.3. ZERO-SHOT OUT-OF-DISTRIBUTION EVALUATION ON LIBERO-PLUS 

To rigorously evaluate the generalization capabilities of our proposed GridS mechanism, we conduct zero-shot out-ofdistribution (OOD) evaluations on the LIBERO-PLUS benchmark. We test the _π_ 0 _._ 5 models (the dense baseline and the GridS variant with _K_ = 32) across seven perturbation dimensions and five task difficulty levels (Level-1 to Level-5). The quantitative results across the four suites are detailed in Table 9. 

**1. Difficulty Dynamics: The “Learning is Forgetting” Signature.** A granular analysis of the task difficulty levels (Panel B) reveals a profound dynamic. In highly predictable, easy scenarios (Level-1 and Level-2), the dense baseline slightly outperforms GridS because its 256 tokens enable perfect memorization of specific visual layouts. However, as the perturbation intensity reaches extreme limits (Level-5), the baseline’s dense representation becomes a liability, leading to catastrophic degradation (e.g., plunging to 47.9% in LIBERO-Goal and 52.6% in LIBERO-10). In stark contrast, GridS substantially closes the gap and even overtakes the baseline at Level-5 (+0.5% in Goal, +3.4% in LIBERO-10). This confirms that compressing the visual representation acts as a strict information bottleneck: by “forgetting” task-irrelevant environmental noise, GridS prevents spurious overfitting and maintains causal robustness in extreme OOD conditions. 

**2. Where GridS Excels: Visual and Spatial Robustness.** GridS demonstrates overwhelming superiority in perturbation dimensions that heavily distort visual geometry and rendering (Panel A). 

- _Camera Viewpoints:_ The dense baseline completely collapses under camera shifts (dropping to 67.0% in Spatial and 45.8% in LIBERO-10) due to severe _camera overfitting_ —it relies on absolute pixel coordinates and background references. GridS actively discards the background and samples only relative, object-centric geometries, yielding massive inverse gains (+19.4% in Spatial, +10.8% in LIBERO-10). 

19 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

_Table 9._ Zero-shot Out-of-Distribution Evaluation on the LIBERO-PLUS Benchmark. The _π_ 0 _._ 5 baseline and the compressed model ( _π_ 0 _._ 5 + GridS32) are evaluated under various perturbation dimensions (Panel A) and difficulty levels (Panel B). ∆ denotes the absolute performance difference. 

|_(a_|_)_LIBERO-Spat|ial||_(b)_|LIBERO-Obj|ect||
|---|---|---|---|---|---|---|---|
|**Metric Category**|_π_0_._5**Baseline**|_π_0_._5**+ GridS**32|∆|**Metric Category**<br>|_π_0_._5**Baseline**|_π_0_._5**+ GridS**3|2<br>∆|
|_Panel A:_|_By Perturbation D_|_imension_||_Panel A: B_|_y Perturbation_|_Dimension_||
|Background Textures|97.3|95.0|-2.3|Background Textures|99.6|98.0|-1.6|
|Camera Viewpoints|67.0|86.4|**+19.4**|Camera Viewpoints|81.3|82.8|+1.5|
|Language Instructions|92.6|82.6|-10.0|Language Instructions|92.4|80.8|-11.6|
|Light Conditions|96.9|98.6|+1.7|Light Conditions|99.0|97.6|-1.4|
|Objects Layout|96.9|95.1|-1.8|Objects Layout|90.1|87.6|-2.5|
|Robot Initial States|83.4|72.6|-10.8|<br>Robot Initial States|73.6|61.8|-11.8|
|Sensor Noise|90.9|91.5|+0.6|Sensor Noise|95.5|97.9|+2.4|
|_Panel B   i_|_: By Task Difficul_|_ity Level_||_Panel B:   i_|_By Task Difficu_|_ilty Level_||
|Level 1 (Easiest)|93.5|92.5|-1.0|Level 1 (Easiest)|97.3|93.9|-3.4|
|Level 2|90.9|91.0|+0.1|Level 2|96.7|92.8|-3.9|
|Level 3|87.6|89.2|+1.6|Level 3|94.7|90.3|-4.4|
|Level 4<br>|88.7<br>|87.3<br>|-1.4<br>|Level 4|86.1|83.4|-2.7|
|Level 5 (Hardest)|72.8|67.5|-5.3|Level 5 (Hardest)|75.9|72.4|-3.5|
|**Overall**|**88.7**|**88.3**|**-0.4**|**Overall**|**89.3**|**85.7**|**-3.6**|
|_(_|_c)_LIBERO-Goa|l||_(d)_L|IBERO-Long|(10)||
|**Metric Category**|_π_0_._5**Baseline**|_π_0_._5**+ GridS**32|∆|**Metric Category**<br>|_π_0_._5**Baseline**|_π_0_._5**+ GridS**3|2<br>∆|
|_Panel A:_|_By Perturbation D_|_imension_||_Panel A: B_|_y Perturbation_|_Dimension_||
|Background Textures|87.9|95.0|+7.1|Background Textures|93.8|84.1|-9.7|
|Camera Viewpoints|71.3|80.9|**+9.6**|Camera Viewpoints|45.8|56.6|**+10.8**|
|Language Instructions|72.0|60.0|-12.0|Language Instructions|92.2|85.6|-6.6|
|Light Conditions|85.7|97.8|**+12.1**|Light Conditions|91.6|87.6|-4.0|
|<br>Objects Layout|70.1|65.9|-4.2|<br>Objects Layout|92.0|84.0|-8.0|
|<br>Robot Initial States|78.5|69.7|-8.8|<br>Robot Initial States|78.9|64.9|-14.0|
|Sensor Noise|88.7|90.0|+1.3|Sensor Noise|78.4|84.0|+5.6|
|_Panel B   i_|_: By Task Difficul_|_ity Level_||_Panel B:   i_|_By Task Difficu_|_ilty Level_||
|Level 1 (Easiest)|95.5|93.5|-2.0|Level 1 (Easiest)|95.0|91.0|-4.0|
|Level 2|91.1|92.5|+1.4|Level 2|95.6|88.4|-7.2|
|Level 3|87.1|85.6|-1.5|Level 3|91.3|83.7|-7.6|
|Level 4|74.2|70.9|-3.3|Level 4|83.0|80.1|-2.9|
|Level 5 (Hardest)|47.9|48.4|**+0.5**|Level 5 (Hardest)|52.6|56.0|**+3.4**|
|Unknown|86.0|97.5|**+11.5**|**Overall**|**80.0**|**77.1**|**-2.9**|
|**Overall**|**78.2**|**78.0**|**-0.2**|||||


|**Metric Category**<br>_π_0_._5**Baseline**|_π_0_._5**+ GridS**3|2<br>∆|
|---|---|---|
|_Panel A: By Perturbation_|_Dimension_||
|Background Textures<br>93.8|84.1|-9.7|
|Camera Viewpoints<br>45.8|56.6|**+10.8**|
|Language Instructions<br>92.2|85.6|-6.6|
|Light Conditions<br>91.6|87.6|-4.0|
|Objects Layout<br>92.0|84.0|-8.0|
|Robot Initial States<br>78.9|64.9|-14.0|
|Sensor Noise<br>78.4|84.0|+5.6|
|_Panel B: By Task Diffic_|_iulty Level_||
|Level 1 (Easiest)<br>95.0|91.0|-4.0|
|Level 2<br>95.6|88.4|-7.2|
|Level 3<br>91.3|83.7|-7.6|
|Level 4<br>83.0|80.1|-2.9|
|Level 5 (Hardest)<br>52.6|56.0|**+3.4**|
|**Overall**<br>**80.0**|**77.1**|**-2.9**|


20 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

- _Sensor Noise & Light Conditions:_ Under heavy noise (e.g., motion/Gaussian blur) and drastic illumination changes, GridS consistently outperforms the baseline (+5.6% Noise in LIBERO-10; +12.1% Light in Goal). The sparse sampling of 32 keypoints inherently bypasses high-frequency pixel corruption, allowing the policy to focus solely on uncorrupted topological affordances. 

**3. Where GridS Struggles: Fine-Grained Kinematics and Semantics.** While highly resilient to visual variance, extreme compression inevitably introduces specific trade-offs: 

- _Robot Initial States:_ GridS exhibits performance drops (-8.8% to -14.0%) when the robot’s initial joint angles are heavily perturbed. In difficult instances where the arm starts far from the training distribution, complex recovery trajectory planning requires high-resolution visual feedback of the entire kinematic chain. Aggressively compressing the scene down to 32 tokens over-smooths these fine-grained proprioceptive details. 

- _Language Instructions:_ We observe a moderate degradation (-6.6% to -12.0%) under language rewriting. Because GridS operates by aggressively filtering visual clutter, it may inadvertently discard subtle visual cues (e.g., slight textural variations or small contextual objects) that are strictly necessary to ground and decode highly complex, reasoned language instructions. 

**4. Superiority over Discrete Pruning Paradigms and Final Advantage.** To contextualize these results, it is imperative to note that existing discrete token reduction methods, such as FastV and SparseVLM, _suffer catastrophic performance drops exceeding 20% on the LIBERO-PLUS dataset_ . By discretely dropping patches, they fracture the continuous 2D spatial structure; when subjected to viewpoint shifts, these quantization errors are fatally magnified. GridS fundamentally resolves this via Differentiable Bilinear Sampling. 

Ultimately, maintaining near-lossless overall performance (-0.4% in Spatial, -0.2% in Goal) while compressing the visual input by 87 _._ 5% (256 _→_ 32 tokens) is a monumental achievement. GridS proves to be far more than an inference accelerator— it is a powerful representation distillator. Its true advantage over the dense baseline lies in its ability to break the fragility of dense vision, trading negligible absolute fidelity for breakthrough spatial and visual robustness. 

### **E.2. RoboTwin** 

During the rebuttal period, we received a suggestion from Reviewer LrTB to conduct testing on RoboTwin 2.0 (Chen et al., 2025). Therefore, we trained and deployed using the X-VLA method (Zheng et al., 2025) within a limited time. We conducted new experiments on the complex ”Place Bread Skillet” task. This suite is explicitly designed to evaluate long-horizon planning and sequential multi-stage execution. As shown in our new results, GridS effectively maintains geometric attention over extended horizons, vastly outperforming the full-token baseline: while the fine-tuned standard XVLA [1] achieves only a 12% success rate, our XVLA+GridS policy yields a remarkable 76% success rate. We will add more result of RoboTwin 2.0 on the next period of discussion. Furthermore, our existing real-world stacking task is inherently a multi-stage process (approach _→_ grasp _→_ align _→_ stack) requiring sustained spatial reasoning. GridS achieved a massive +52.4% success rate improvement here over the baseline. 

Together, these results clearly demonstrate that GridS does not degrade in challenging settings; rather, it robustly supports rich, long-horizon interactions by preventing spatial error accumulation. We will include these new RoboTwin 2.0 results in the revised manuscript. 

## **F. Evaluation of Alternative Downsampling Baselines** 

To rigorously isolate the contribution of our proposed geometry-aware sampling mechanism from the mere reduction in sequence length, we evaluate GridS against two alternative downsampling baselines: 

- **Random Sampling:** Randomly selecting _K_ tokens from the dense visual feature grid. 

- **Top-** _K_ **Pruning:** Discretely selecting the top _K_ tokens based on visual saliency (e.g., maximum activation norms). 

For a strictly fair comparison, all variants are restricted to an identical token budget ( _K_ = 16) and are trained under the exact same full fine-tuning protocol on the LIBERO dataset. The quantitative comparisons are reported in Table 10. 

21 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

_Table 10._ Performance comparison of different downsampling mechanisms under a matched fine-tuning protocol on the LIBERO dataset. All compressed variants use exactly 16 visual tokens. 

|**Method**|**Tokens**|**Spatial**|**Object**|**Goal**|**Long**|**Avg. SR (%)**|
|---|---|---|---|---|---|---|
|Baseline (_π_0)|256|97.2|98.8|96.0|85.6|94.4|
|Random Sampling|16|93.8|98.4|85.8|73.2|87.8|
|Top-_K_ Pruning|16|96.6|98.8|89.8|77.0|90.5|
|**GridS (Ours)**|**16**|**98.0**|**99.2**|**96.4**|**90.2**|**96.0**|


**Analysis:** As shown in Table 10, naive token reduction strategies fail to maintain the baseline’s capabilities. Random Sampling drastically degrades the average success rate to 87.8%, with a particularly severe collapse in long-horizon tasks (73.2%), as it arbitrarily discards critical interactive geometries. Top- _K_ Pruning performs marginally better (90.5%) by prioritizing salient features, but still falls significantly short of the dense baseline. This performance gap highlights the fundamental flaw of discrete patch dropping: it destroys continuous 2D spatial structures, resulting in geometric quantization errors that severely impair precise motor control. 

In contrast, GridS not only recovers this performance drop but actively outperforms the 256-token baseline. These results conclusively demonstrate that the performance gains of GridS are not simply a byproduct of reducing the token count (which might otherwise prevent overfitting), but are intrinsically derived from its differentiable, geometry-aware resampling mechanism that effectively filters noise while preserving essential physical precision. 

## **G. Extreme Compression: A Novel Information Bottleneck Paradigm** 

To push the limits of our proposed sampling mechanism, we conduct an extreme stress test on the LIBERO dataset by restricting the GridS budget to a single visual token ( _K_ = 1). We employ the fine-tuned _π_ 0 _._ 5 architecture for this ablation to verify if the mechanism holds under a highly capable backbone. The results of this ultra-sparse configuration are reported in Table 11. 

_Table 11._ Performance of GridS under the extreme sparsity constraint ( _K_ = 1) using the _π_ 0 _._ 5 backbone. Counter-intuitively, a single sampled token (a 99.6% reduction in visual input) retains sufficient information to achieve nearly identical performance compared to the dense 256-token baseline. 

|**Model Config**|**Spatial**|**Object**|**Goal**|**Long**|**Avg. SR (%)**|
|---|---|---|---|---|---|
|_π_0_._5Baseline (256 Tokens)|98.4|98.0|97.6|92.8|96.7|
|_π_0_._5**+ GridS (**_K_ = 1**)**|98.0|99.0|97.6|91.8|96.6|


### **Analysis from an Information Retention Perspective:** 

The astonishing capability of a single-token representation (averaging 96.6%, practically on par with the 96.7% of the dense _π_ 0 _._ 5 baseline) provides profound insight into visual redundancy in robotic manipulation. From an information theory perspective, this phenomenon can be explained through the _Information Bottleneck (IB)_ principle. 

In standard dense grid representations, the model is fed all visual information indiscriminately. While this mathematically maximizes ”information retention”, it simultaneously introduces massive amounts of task-irrelevant background noise and domain-specific textures. This overabundance of redundant capacity allows the over-parameterized VLA policy to overfit to spurious spatial correlations—essentially memorizing the dataset layout rather than learning generalizable interaction skills. 

By imposing an extreme constraint ( _K_ = 1), GridS creates a strict information bottleneck. To minimize task loss under this severe limitation, the coordinate predictor is forced to discard all redundant background context and actively map the single sampling coordinate to the absolute semantic center of the interactive scene (e.g., the precise affordance point between the gripper and the target). 

### **A Novel Compression Paradigm:** 

These findings suggest that GridS operates fundamentally differently from traditional token pruning. Traditional methods attempt to passively ”preserve what is important” by selecting multiple discrete patches. In contrast, GridS introduces an 

22 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

active representation distillation paradigm. By drastically reducing the volume of training information (a 99.6% compression rate with negligible performance degradation), the differentiable bottleneck inherently prevents the model from relying on spatial shortcuts. Instead, it compels the downstream Transformer to learn the true causal physical mechanics (the essential geometry and affordances) required to complete the task. This paradigm shifts the focus of VLA perception from ”maximizing input coverage” to ”extracting minimal sufficient statistics”, opening a new pathway for highly generalized and computationally minimal robotic learning. 

## **H. Ablation Studies on GridS Architecture** 

To thoroughly evaluate the architectural design choices of GridS, we conduct a comprehensive ablation study on the LIBERO dataset. We systematically isolate and modify key components, including the pooling mechanism, predictor capacity, coordinate injection, and interpolation strategy. The quantitative results are summarized in Table 12. 

_Table 12._ Ablation study of GridS components on the LIBERO dataset. The default setting serves as the reference baseline. 

|**Component Changed**|**Variant**|∆**Success Rate**|
|---|---|---|
|_Default GridS_|(GAP, Base MLP, w/ Coord, Bilinear)|Reference|
|Pli Stt|Conv-Downsample|-4.4%|
|(a) oong raegy|Global Max Pooling (GMP)|-0.3%|
||10_×_Larger MLP|+0.2%|
|(b) Predictor Capacity|100_×_Larger MLP<br>Segment Anything Model|+0.2%<br>-6.2%|
|(c) Coordinate Injection|w/o Coordinate Injection|-3.6%|
|(d) Interpolation Method|Nearest-Neighbor|-4.1%|


Based on the experimental results, we detail the analysis of each component below: 

- **Pooling Strategy:** The parameter-free Global Average Pooling (GAP) serves as a robust global summarizer. Replacing it with a parameterized convolutional downsampling module leads to a 4.4% performance drop, largely due to overfitting to the spatial biases present in the dataset. Alternatively, Global Max Pooling (GMP) slightly degrades performance (-0.3%) by discarding continuous global spatial context. 

- **Predictor Capacity:** Expanding the MLP predictor size by 10 _×_ or even 100 _×_ yields a negligible +0.2% improvement. This indicates that mapping global visual context to a sparse set of 2D coordinates is an inherently low-complexity task, where scaling up model capacity offers no meaningful benefit. We further experimented with utilizing a frozen, pre-trained Segment Anything Model (SAM) (Kirillov et al., 2023) to guide the coordinate sampling. Surprisingly, this led to a severe **-6.2%** performance drop. This strongly highlights that generic semantic segmentation (identifying *what* an object is) misaligns with task-driven geometric sampling (identifying exactly *where* the gripper should interact). 

- **Coordinate Injection:** Removing explicit coordinate injection results in a 3.6% performance drop. Because the sparse continuous sampling inherently disrupts the original dense 2D grid structure, explicitly injecting spatial coordinates is essential for the downstream Transformer to retain accurate positional awareness of the objects. 

- **Interpolation Method:** Substituting bilinear interpolation with nearest-neighbor sampling significantly degrades performance (-4.1%). The discrete rounding operation in nearest-neighbor sampling breaks the gradient flow. In contrast, bilinear interpolation preserves full differentiability, which is strictly required for end-to-end, task-driven optimization. 

## **I. Calculation of the Information Retention Map** 

To quantitatively evaluate the semantic coverage of the sampled tokens, we introduce the Information Retention map (as visualized in Figure 7). 

23 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

For each original dense token _F_ orig<sup>(</sup><sup>_i,j_)</sup> _∈_ R<sup>_C_</sup> at spatial location ( _i, j_ ), we compute its maximum cosine similarity against all _K_ sampled sparse tokens _F_ samp<sup>(</sup><sup>_k_)</sup><sup>_∈_R</sup><sup>_C_.The retention score</sup><sup>_R_at location (</sup><sup>_i, j_) is mathematically defined as:</sup> 


Intuitively, a high retention score (approaching 1 _._ 0, represented by the green regions in our visualizations) indicates that the semantic information of that specific original patch is successfully preserved by at least one token in the aggressively compressed GridS set. 

## **J. Limitations** 

While GridS demonstrates strong empirical performance and theoretical efficiency, we identify two primary limitations in our current framework. 

First, the practical wall-clock speedup during single-batch inference is relatively modest (approximately 1.2 _×_ ) despite massive FLOPs reductions. Because dense baseline models are already heavily optimized via JAX compilation, the runtime bottleneck during sequential, single-batch execution shifts from active computation to fixed kernel overheads. Consequently, the maximum efficiency benefits of GridS are currently realized primarily in high-throughput, large-batch settings. 

Second, the sampling mechanism relies on a static, predefined token budget (e.g., _K_ = 16) across all tasks. Our ablation studies reveal an inverted U-shaped performance trend regarding token density, indicating that an excessively large _K_ degrades performance by reintroducing irrelevant background noise in precision-sensitive scenarios. Currently, GridS cannot adaptively adjust this token budget based on real-time scene complexity. Extending the architecture to dynamically predict the optimal token count _K_ per frame represents a critical direction for future research. 

Third, GridS currently exhibits sub-optimal compatibility with Parameter-Efficient Fine-Tuning (PEFT) methods (Houlsby et al., 2019). Our experiments indicate that when adapted using LoRA (Hu et al., 2022) rather than full fine-tuning, GridS underperforms the dense baseline by 8.3%. We hypothesize that this stems from a severe representational mismatch: GridS fundamentally alters the spatial distribution of visual tokens (shifting from dense, uniform grids to sparse, continuously interpolated features). While full fine-tuning provides sufficient parameter capacity to realign the VLA’s attention mechanism to this novel input structure, LoRA’s restricted degrees of freedom struggle to overcome the frozen pre-trained dense priors. Addressing this capacity bottleneck to enable highly efficient PEFT deployment is an important next step. 

## **K. Additional Visualizations of Information Retention Maps** 

To further demonstrate the robust and consistent behavior of the GridS sampling mechanism, we provide additional visualizations of the Information Retention maps evaluated on the LIBERO benchmark (Figure 10) and ALOHA (Figure 11). In addition, we provide the full sequence of Information Retention maps for the real-world ”Stacking Cubes” task (Steps 0–47) in Figure 12. 

An important empirical observation is that during successful real-world execution, the average retention score fluctuates consistently between 0 _._ 8 and 0 _._ 9, rather than maintaining near-perfect 1 _._ 0 fidelity. As analyzed below, this ”lossy” compression is a key driver of our model’s superior out-of-distribution (OOD) performance. 

The observation that intermediate retention (0 _._ 8 _∼_ 0 _._ 9) outperforms full retention (1 _._ 0) aligns with the ”Learning is Forgetting” principle (Conklin et al., 2026). In VLA models, perfect information retention (as seen in the dense baseline) often leads to the inclusion of high-frequency noise and task-irrelevant environmental features. This over-abundance of information allows the model to find ”spatial shortcuts” or overfit to spurious correlations within the training distribution. In contrast, GridS introduces a principled Information Bottleneck. By restricting the retention to approximately 85%, the model is forced to ”forget” non-causal background pixels. This compression compels the Transformer backbone to rely exclusively on the invariant, minimal sufficient statistics of the scene, namely the physical affordances and object-effector geometries. Consequently, GridS achieves significantly higher success rates in real-world OOD scenarios where the baseline’s ”perfect memory” of training-specific noise becomes a liability. 

Viewed through the lens of information retention, a score approaching 1.0 indicates high reconstructive fidelity, yielding 

24 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 

performance that closely mirrors the dense baseline. Conversely, an intermediate retention regime of 0 _._ 8 _∼_ 0 _._ 9 acts as a critical information bottleneck. By intentionally discarding 10% _∼_ 20% of the peripheral visual signals, this lossy compression compels the model to ’forget’ spurious background noise and distill the true causal features governing the manipulation task. 


_Figure 10._ Additional Information Retention maps on the LIBERO dataset. 

25 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 


_Figure 11._ Additional Information Retention maps on the ALOHA dataset. 

26 

**See What Matters: Differentiable Grid Sample Pruning for Generalizable Vision-Language-Action Model** 


_Figure 12._ Continuous Information Retention maps for the Real-World Stacking task (Steps 0–47). The visualization demonstrates that the model consistently maintains a retention score of 0 _._ 8 _∼_ 0 _._ 9, effectively filtering background distractors while focusing on the relative geometry between the gripper and cubes. 

27 

