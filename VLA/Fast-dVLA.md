---
title: "Fast-dVLA: Accelerating Discrete Diffusion VLA to Real-Time Performance"
date: "2026-03-26"
authors: "Wenxuan Song; Jiayi Chen; Shuai Chen; Jingbo Wang; Pengxiang Ding; Han Zhao"
url: https://arxiv.org/abs/2603.25661
pdf: https://arxiv.org/pdf/2603.25661
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.25661)** / [論文ページ](https://arxiv.org/abs/2603.25661)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Fast-dVLA: Accelerating Discrete Diffusion VLA to Real-Time Performance** 

**Wenxuan Song**<sup>1</sup><sup>_∗_</sup> , **Jiayi Chen**<sup>1</sup><sup>_∗_</sup> , **Shuai Chen**<sup>2,3</sup><sup>_∗_</sup> , **Jingbo Wang**<sup>1</sup> , **Pengxiang Ding**<sup>5,6</sup> , **Han Zhao**<sup>5,6</sup> , **Yikai Qin**<sup>1</sup> , **Xinhu Zheng**<sup>1</sup> , **Donglin Wang**<sup>2</sup> , **Yan Wang**<sup>4†</sup> , **Haoang Li**<sup>1†</sup> 

1The Hong Kong University of Science and Technology (Guangzhou), 2ShanghaiTech University, 3Shanghai Institute of Technical Physics, CAS, 4AIR, Tsinghua University, 5Westlake University, 6Zhejiang University 

_∗_ Equal Contribution, †Corresponding Author 

This paper proposes a novel approach to address the challenge that pretrained VLA models often fail to effectively improve performance and reduce adaptation costs during standard supervised finetuning (SFT). Some advanced finetuning methods with auxiliary training objectives can improve performance and reduce the number of convergence steps. However, they typically incur significant computational overhead due to the additional losses from auxiliary tasks. To simultaneously achieve the enhanced capabilities of auxiliary training with the simplicity of standard SFT, we decouple the two objectives of auxiliary task training within the parameter space, namely, enhancing general capabilities and fitting task-specific action distributions. To deliver this goal, we only need to train the model to converge on a small-scale task set using two distinct training strategies. The difference between the resulting model parameters can then be interpreted as _capability vectors_ provided by auxiliary tasks. These vectors are then merged with pretrained parameters to form a capability-enhanced meta model. Moreover, when standard SFT is augmented with a lightweight orthogonal regularization loss, the merged model attains performance comparable to auxiliary finetuned baselines with reduced computational overhead. Experimental results demonstrate that this approach is highly effective across diverse robot tasks. Project page: `https://chris1220313648.github.io/Fast-dVLA/` 

**Correspondence:** Wenxuan Song at `songwenxuan0115@gmail.com` 


## **1 Introduction** 

Vision–Language–Action (VLA) (Yan et al., 2026; Cui et al., 2025; Intelligence et al., 2025; Song et al., 2025b; Kim et al., 2025b) models are typically trained on large-scale robotic datasets to map multimodal perception into executable robotic control, exhibiting language following and visual generalization capabilities, and have become a dominant paradigm in current research on robotic foundation models. Representative VLAs (Black et al., 2024; Bjorck et al., 2025; Liu et al., 2025b; Zhong et al., 2026) adopt a flow-matching architecture, where the VLM performs multimodal understanding and the FM action head takes the processed representations as input and outputs continuous control signals. Recently, discrete diffusion VLAs (dVLAs) based on the diffusion Large Language Models (dLLMs) (Liang et al., 2025b; Wen et al., 2025a,c; Chen et al., 2025; Ye et al., 2025b) have emerged as a promising challenger to existing VLA architectures. These models output actions in a parallel, iterative denoising manner, while not relying on the flow-matching head. Therefore, compared with flow-matching architectures, they demonstrate inherent advantages in unified multimodal alignment and understanding (Chen et al., 2025; Wen et al., 2025a), while better preserving the pretrained knowledge of VLMs (Liang et al., 2025b). 

However, current dVLAs still suffer from a fundamental limitation. Their inference speed is slow, with an execution frequency that is far below the real-time requirements of physical robotic systems (typically around 30 Hz). This large gap substantially limits their practical applicability in real-world settings. As illustrated in Figure 2, although dVLA significantly reduces the number of forward passes required to generate a complete action sequence compared to discrete autoregressive (AR) VLA (Figure 2 (a)) by enabling parallel decoding, 

1 


**Figure 1 Speed/Success Rate trade-off. Left (Intra-comparison):** Compared to other acceleration strategies for discrete diffusion VLAs (dVLAs), DD-VLA (Liang et al., 2025b) and Dream-VLA (Ye et al., 2025a), our `Fast-dVLA` achieves a favorable success rate and speed. Here, BlockDiff denotes block diffusion (Arriola et al., 2025). **Right (Inter-comparison):** Our `Fast-dVLA` surpasses autoregressive methods, _i.e._ , _π_ 0-FAST (Pertsch et al., 2025). It also reaches parallel performance and inference frequency with state-of-the-art (SOTA) continuous flow-matching methods, _i.e._ , _π_ 0.5 (Intelligence et al., 2025), while maintaining several inherent advantages of dVLAs. We report metrics on LIBERO (Liu et al., 2023). 

its bidirectional attention mechanism prevents the reuse of key–value (KV) caches from previously generated tokens, resulting in a very low per-pass forward efficiency (Figure 2 (b)). 

To explore the feasibility of leveraging KV cache, we investigate the action decoding order in dVLAs (Figure 3). We observe that, although with bidirectional attention, dVLAs still follow a left-to-right decoding pattern. This block-wise decoding behavior suggests that a promising direction is to apply block diffusion (Arriola et al., 2025) (Figure 2 (c)), which natively trains dVLAs with block-wise attention, decodes a block of action tokens in parallel, caches the corresponding KV states after completing the block, and then proceeds to the next block in an AR manner. This design achieves a moderate inference speed by balancing partial KV cache reuse with intra-block parallel decoding. However, it inherently precludes inter-block parallelism, which is a crucial factor for achieving high-throughput and low-latency inference. 

This paper proposes `Fast-dVLA` , a novel block-wise diffusion strategy that achieves the first breakthrough in accelerating dVLAs to a real-time regime. Conceptually, we exploit block-wise sequential generation for KV cache utilization, while removing the requirement that later blocks wait for earlier ones to finish denoising. Concretely, we treat the full action token sequence at each timestep ( _i.e._ , the dimensionality of the actions) and its multiples as an action block. Then, `Fast-dVLA` learns to denoise a sequence of blocks with monotonically increasing mask ratios in parallel. Naturally, preceding blocks can finish before subsequent ones, allowing their KV states to be cached for subsequent computations. Note that we constrain the attention to be block-wise causal to ensure the KV cache remains unchanged. For training efficiency, inspired by (Wang et al., 2026), we distill `Fast-dVLA` from finetuned dVLAs with bidirectional attention using an asymmetric distillation loss. During inference, we design a pipelined parallel decoding algorithm that enables inter-block parallelism with varying noise levels across blocks. 

We conduct extensive experiments on representative dVLA models, including Dream-VLA (Ye et al., 2025a), Discrete Diffusion VLA (DD-VLA) (Liang et al., 2025b), and UD-VLA (Chen et al., 2025) across CALVIN (Mees et al., 2022), LIBERO (Liu et al., 2023), and SIMPLER (Li et al., 2024) benchmarks. Figure 1 shows that our method consistently achieves 2.8 _×_ –4.1 _×_ speedup while preserving action performance, which is superior to other dVLA paradigms. Lastly, diverse real-world tasks demonstrate the dynamic capability and working efficiency in the application. 

Our contributions are summarized as follows: 

- We reveal an implicit block-wise AR decoding tendency in the fully bidirectional dVLA, motivating an AR–diffusion hybrid denoising process. 

- We propose `Fast-dVLA` , which leverages block-wise diffusion with a corresponding attention pattern to 

2 

|Sequential|Parallel||Sequenti|al + Parallel|
|---|---|---|---|---|
|(a) Autoregressive<br>VLA|(b) Discrete<br>Diffusion VLA|(c) Block Dif<br>VLA|fusion|(d) Ours|
||Noisy Action<br>(Block)|Clean Action<br>(Block)|Clean Actio<br>at Current|<sup>Partially Clean</sup><br>Action Block<br>n (Block)<br>Forward|
|Model|(a) Autoregressive VLA|(b) Discrete<br>Diffusion VLA|(c) Block<br>VL|Diffusion<br>A<br>(d) Ours|
|Forwards per<br>Sequence|High|Low|Mod|erate<br>Low|
|Forward Speed|Fast|Low|Fa|st<br>Fast|
|Speed per Sequence<br>(Inference Speed)|Slow|Slow|Mod|erate<br>Fast|


**Figure 2 Comparison among discrete decoding paradigms.** Here, _Forward per Sequence_ denotes the needed forward numbers for a full sequence output, _Forward Speed_ denotes the decoding speed for each forward, and _Speed per Sequence (i.e., Inference Speed)_ denotes the decoding speed for the full sequence output. **Our** **`Fast-dVLA` requires significantly fewer forward passes and executes each pass efficiently, resulting in substantially faster inference.** 

allow KV cache reuse, while allowing inter-block parallelism through diffusion forcing. 

- Following the observation, we apply an asymmetric distillation for efficient training, and a pipelined parallel decoding for real-time inference. 

- Extensive experiments on CALVIN, LIBERO, and SIMPLER demonstrate up to 4.1 _×_ acceleration over existing dVLA models, while maintaining SOTA-level success rates. Moreover, the results in diverse real-world tasks demonstrate the dynamic capability and working efficiency in the application. 

## **2 Preliminary: Discrete Diffusion VLA (dVLA)** 

Discrete Diffusion VLA ( _e.g._ , **Dream-VLA** (Ye et al., 2025a) and **DD-VLA** (Liang et al., 2025b)) output discrete action tokens, obtained either by uniform bins (Kim et al., 2025b) or by quantized tokenizers (Pertsch et al., 2025), instead of operating directly on continuous controls. Actions are represented as a length- _L_ discrete token sequence **a** 0 = ( _a_ 0<sup>_i_, . . . ,</sup><sup>_a_</sup> 0<sup>_L_), where each token</sup><sup>_a_</sup> 0<sup>_i_corresponds to discrete low-level robot actions and a</sup> special mask token M is added to the vocabulary to enable diffusion-style corruption. The forward diffusion process randomly replaces a subset of action tokens with M according to a time-dependent mask ratio, independently across positions. The reverse process learns to recover masked tokens conditioned on the unmasked context and multimodal inputs **c** ( _e.g._ , language and visual observations). At each denoising step, unmasked tokens are copied unchanged, while masked positions are predicted from a categorical distribution parameterized by the model. 

During training, a mask ratio _γt ∈_ (0, 1] is sampled, and the corresponding action tokens are replaced by M to obtain a corrupted sequence **a** ˜ _t_ . The model is then trained to reconstruct the original tokens using cross-entropy 

3 


**Figure 3** Visualization of the decoding tendency of action tokens at different positions in Dream-VLA (Ye et al., 2025a). Brighter regions indicate higher decoding probability. Despite using bidirectional attention, the model exhibits a clear left-to-right decoding tendency such that action tokens at earlier temporal positions are typically decoded in earlier diffusion iterations. Overall, the decoding process reveals an implicit block-wise AR pattern. 

loss computed only on masked positions: 


where _Mγt_ denotes the set of masked positions. This objective preserves the core corruption–denoising principle of discrete diffusion while enabling efficient training with standard discrete VLA architectures. 

**UD-VLA** (Chen et al., 2025) extends this framework to unified VLA models(Wang et al., 2025b) by incorporating future visual prediction. Specifically, future image observations are encoded into a discrete token sequence **v** 0 = ( _v_<sup>1</sup> 0<sup>, . . . ,</sup><sup>_v_</sup> 0<sup>_L_) using a VQ-VAE (Zheng et al., 2022) encoder, and concatenated with the action tokens to</sup> form a unified sequence. The diffusion process is then applied jointly over visual and action tokens, allowing future visual reasoning and action generation to be learned in a unified manner. 

## **3 Method** 

In this section, we first introduce an intriguing observation (see Section 3.1). Then, we propose `Fast-dVLA` to accelerate dVLA in a block-wise decoding manner. Our method is built to support two key features: (1) a block-wise attention mechanism that enables the reuse of KV cache across denoising iterations (see Section 3.2) and (2) a diffusion forcing denoising process that supports simultaneous decoding of blocks with different noising levels. To efficiently train such models, we design an asymmetric distillation that starts from a pretrained bidirectional dVLA (see Section 3.3). During inference, we design an inter-block parallel decoding schedule that balances inference speed and decoding reliability (see Section 3.4). 

### **3.1 Motivation** 

As shown in Figure 3, we record and visualize the decoding frequency at different positions during the denoising process of a representative dVLA ( _i.e.,_ Dream-VLA). Interestingly, even though the dVLA employs bidirectional attention, the model still exhibits a strong left-to-right decoding pattern at a global level. In particular, action blocks that occur earlier in the temporal dimension tend to be decoded in earlier denoising iterations. This can be attributed to: 1) The backbone (Ye et al., 2025b) of existing dVLAs is typically initialized from an AR VLM and trained in a discrete diffusion manner, thereby retaining certain autoregressive characteristics. 2) Actions at different timesteps exhibit inherent temporal dependencies. This block-wise AR decoding behavior suggests that _a finetuned bidirectional dVLA can be directly forced to follow a block-diffusion decoding manner_ . 

### **3.2 Critical Designs of Target Models** 

**Block-Wise Attention for Inter-block KV Cache Reusing.** As shown in Figure 4a, current dVLA (Chen et al., 2025; Liang et al., 2025b; Ye et al., 2025a) models generate either partial or full sequences using bidirectional attention, which causes the Key-Value (KV) representations to vary at every denoising iteration. As a result, the conventional KV cache mechanism used in AR models cannot be directly reused to accelerate inference. To address this limitation, we adopt a block diffusion decoding strategy (see Figure 2d) with block-wise 

4 


**Figure 4 KV cache similarity across diffusion iterations under block-diffusion decoding.** We visualize the similarity of attention key–value (KV) states for the first action block across different denoising steps. **(a):** In native dVLA with bidirectional attention, the KV representations evolve across iterations, preventing effective reuse of cached states. **(b):** In contrast, after adapting dVLA to a block-wise attention architecture via asymmetric distillation, once all tokens in the first block are unmasked, the corresponding KV states remain fixed, enabling efficient KV cache reuse and substantially reducing the computational overhead in subsequent iterations. 

attention (see Figure 5), which bridges autoregressive decoding and discrete diffusion by interpolating between sequential dependency and parallel generation. 

Within each block, the KV representations are influenced only by the prefix tokens and the tokens inside the current block. As shown in Figure 4b, once the decoding of a block is completed, the KV values of that block remain unchanged in subsequent steps, enabling effective cache reuse for the following decoding process. 

**Diffusion Forcing for Inter-block Parallel Decoding.** Motivated by observations in mimic-video (Pai et al., 2025) that action tokens need not attend to the clean tokens from previous timesteps, we construct a progressively decaying noise sequence similar to diffusion forcing (Chen et al., 2024; Yin et al., 2025; Li et al., 2026). Let the index set of the _i_ -th block be defined as _Bi_ = _{_ ( _i −_ 1) _k_ , . . . , _ik −_ 1 _}_ , and denote by _YBi_ the corresponding token subsequence. 

During the forward diffusion process, we assign progressively increasing noise levels to different blocks according to a monotonic schedule _t_ 1 _< t_ 2 _< · · · < tN_ . Formally, the noise sequence can be represented as _Y_<sup>_t_1:</sup><sup>_N_</sup> = _{YB_<sup>_t_1</sup> 1<sup>, . . . ,</sup><sup>_Y_</sup> _B_<sup>_tN_</sup> _N_<sup>_}_.Underthisdesign,earlierblocksareexposed</sup> to lower corruption levels and thus retain more complete information, whereas later blocks remain more heavily masked and uncertain. 


**Figure 5 Block-wise Attention.** 

For the reverse process, we learn a _θ_ -parameterized model that factorizes the conditional distribution in a block-wise autoregressive manner: 


This formulation allows the model to progressively refine earlier blocks while concurrently denoising later ones, naturally enabling parallel decoding across blocks without sacrificing temporal consistency. 

5 


**Figure 6** Overview of the pipelined parallel decoding in `Fast-dVLA` . Blocks are processed concurrently in a dynamically growing pipeline. A new block is introduced when the tail block exceeds the addition threshold _τ_ add =<sup><u>2</u></sup> 7<sup>, and becomes</sup> fully activated after its predecessor surpasses the activation threshold _τ_ act =<sup><u>4</u></sup> 7<sup>.</sup> 

### **3.3 Training: Asymmetric Distillation for Efficient Post-Training** 

To train our `Fast-dVLA` , a straightforward approach is to train it from scratch while maintaining block-wise attention and diffusion-forcing objective. The loss function is defined as: 


However, motivated by Section 3.1, directly inheriting the decoding nature from open-source bidirectional dVLAs (Chen et al., 2025; Zhang et al., 2025c; Liang et al., 2025b) (serving as teacher models) can be a more efficient and lower-cost way. Specifically, inspired by (Wang et al., 2026), we design an asymmetric distillation in which the `Fast-dVLA` (serving as student models) with block-wise attention is forced to align with the output of the teacher model with bidirectional attention, while they share the same architecture and both condition on the blocks with a monotonic noise schedule. Thus, the distillation loss is formulated as: 


where _D_ KL represents the KL divergence aggregated over the mask tokens. The distillation is asymmetric in that the teacher _pϕ−_ predicts for each block _YB_<sup>0</sup> _i_<sup>with a global view of all blocks, while the student</sup><sup>_pθ_learns to</sup> approximate using only a causally restricted view. 

Taking the training budget required for training a dVLA from scratch as the reference, Figure 8 shows that asymmetric distillation from finetuned weight ( _L_ AD in Equation (4)) achieves convergence with only 1/10 steps, which is much more efficient than training with _L_ BD on the base of finetuned weight or from scratch. Thus, we adopt asymmetric distillation as the default training objective. 

### **3.4 Inference: Pipelined Parallel Decoding** 

As shown in Figure 6, in contrast to traditional block diffusion (Arriola et al., 2025), which performs parallel decoding only within each block while strictly decoding different blocks in sequence, our method enables parallel prediction across multiple blocks. 

Specifically, we distinguish activated blocks (i.e., the block currently being decoded) into two states: _semiactivated_ and _fully-activated_ . The transition between these states is governed by the completion ratio of the preceding block with respect to the thresholds _τ_ add and _τ_ act. When the completion ratio of the previous block exceeds _τ_ add, the subsequent block is introduced as a semi-activated block. We adopt the confidence-aware decoding strategy (Wu et al., 2025) to selectively decode tokens whose prediction confidence exceeds the threshold _τ_ conf. Once the completion ratio surpasses _τ_ act, the block transitions to a fully-activated state, in 

6 

which at least 1/ _n_ of the remaining tokens are guaranteed to be decoded at each step according to confidence ranking. 

This multi-state block-parallel decoding mechanism achieves a favorable trade-off between efficiency and performance. At the same time, it ensures that earlier action tokens are decoded in early iterations, thereby preserving the temporal causality inherent in action execution. A pseudocode summary of our inference is available in the supplementary material. 

## **4 Experiments** 

We conduct comprehensive experiments to evaluate the effectiveness of `Fast-dVLA` in both simulated and real-world robot manipulation tasks. The experiments are designed to answer five core questions: 

**(RQ1)** Does our `Fast-dVLA` achieve a favorable performance/speed trade-off among all dVLA acceleration paradigms? Furthermore, is `Fast-dVLA` consistently effective across diverse dVLA architectures (see Section 4.2)? 

**(RQ2)** How does the performance of existing dVLA methods accelerated by `Fast-dVLA` compare to SOTA methods ( _i.e._ , flow-matching VLAs) on diverse benchmarks and tasks (see Section 4.3)? 

**(RQ3)** Could `Fast-dVLA` facilitate the real-world tasks (see Section 4.4)? 

**(RQ4)** Is the training of `Fast-dVLA` efficient (see Section 4.5)? 

**(RQ5)** What empirical insights can guide the selection of hyperparameters for `Fast-dVLA` to ensure optimal performance (see Section 4.6) ? 

### **4.1 Setup** 

**Models.** We select Dream-VLA and DD-VLA as representatives of dVLA models, and UD-VLA as the representative of unified dVLA models. For Dream-VLA, we perform distillation for 4k steps, corresponding to approximately 1/5 of the original fine-tuning budget. For DD-VLA, we set the distillation steps to 4k, which is approximately 1/8 of the original fine-tuning steps. We set the block size to be 7, as analyzed in Section 4.6. For UD-VLA, we perform distillation for 3k steps, corresponding to approximately 1/8 of the original UD-VLA fine-tuning steps, with a batch size of 12. Due to the relatively long output sequences (625 tokens) in UD-VLA, we set the block size to be a multiple of 32. All remaining training hyperparameters follow the original model configurations. 

**Benchmarks.** We conduct extensive simulated experiments on three popular benchmarks (CALVIN (Mees et al., 2022), LIBERO (Liu et al., 2023), and SimplerEnv (Li et al., 2024)) to provide comprehensive results. Detailed introduction of these benchmarks is available in the supplementary material. 

### **4.2 Paradigm Comparison (RQ1)** 

**`Fast-dVLA` achieves obvious acceleration with competitive performance.** Table 1 shows that Fast-dLLM (Wu et al., 2025) realizes 2 _×_ speedup with an obvious performance drop. This proves that directly reusing the KV cache under fully bidirectional attention introduces biased keys and values in the attention states that lead to performance degradation (see Figure 4a). Block Diffusion (Arriola et al., 2025) decodes blocks strictly in sequence, thus also obtaining a limited acceleration. In contrast, our `Fast-dVLA` built on Dream-VLA and DD-VLA both achieve speedups up to 4.1 _×_ , while slightly improving performance compared to their base models. We attribute the efficiency gain to the discrete diffusion forcing denoising, which effectively reuses the KV cache and offers inter-block parallelism, increasing throughput per iteration step. Meanwhile, our block-wise attention preserves temporal causality in action prediction, leading to more stable optimization during training. In addition, the results further demonstrate the effectiveness of our acceleration strategy across different methods on the same dataset. 

**`Fast-dVLA` naturally generalizes to unified dVLA architectures.** As shown in Table 2, `Fast-dVLA` achieves a 2.8 _×_ inference speedup over UD-VLA on the long-horizon CALVIN ABCD-D benchmark, while maintaining superior performance. This result demonstrates that our method can be seamlessly extended to unified dVLA 

7 

**Table 1** Comparison between various acceleration strategies on two base models in terms of task-wise success rates (SR) and inference speed on LIBERO. 

|Decoding Method||Suc|cess Rate|_↑_||Speed_↑_|
|---|---|---|---|---|---|---|
||Spatial|Goal|Object|Long|Avg.|(Tokens/s)|
|Dream-VLA (Ye et al.,2025a)|0.902|0.920|0.880|0.720|0.856|98.8 (_×1.0_)|
|+ Fast-dLLM|0.884|0.894|0.834|0.702|0.828|183.2 (_×1.9_)|
|+ Block Diffusion|0.918|0.904|0.886|0.722|0.858|181.7 (_×1.8_)|
|+`Fast-dVLA`(ours)|0.912|0.920|0.902|0.746|0.870|**313.1** (_×3.2_)|
|Discrete Diffusion VLA (Liang et al.,2025b)|0.972|0.986|0.974|0.920|0.963|152.1 (_×1.5_)|
|+ Fast-dLLM|0.940|0.952|0.948|0.898|0.935|312.5 (_×3.2_)|
|+ Block Diffusion|0.976|0.986|0.972|0.932|0.967|322.1 (_×3.3_)|
|+`Fast-dVLA`(ours)|0.970|0.988|0.976|0.928|0.966|**402.7** (_×4.1_)|


**Table 2** Comparison between various acceleration strategies on UD-VLA in terms of tasks completed in a row, average sentence length, and inference speed on CALVIN. 

|Decoding Method|Task|T|asks Com|pleted i|n a Row|_↑_|Avg.|Speed_↑_|
|---|---|---|---|---|---|---|---|---|
|||1/5|2/5|3/5|4/5|5/5|Len. _↑_|(Tokens/s)|
|UD-VLA|ABCD_→_D|0.992|0.968|0.936|0.904|0.840|**4.64**|67.3 (_×1.0_)|
|+ Fast-dLLM|ABCD_→_D|0.972|0.920|0.858|0.808|0.762|4.32|132.5 (_×2.0_)|
|+ Block Diffusion|ABCD_→_D|0.988|0.944|0.894|0.862|0.804|4.50|129.5 (_×1.9_)|
|+`Fast-dVLA`(ours)|ABCD_→_D|0.984|0.952|0.922|0.870|0.812|4.54|**186.7** (_×2.8_)|


frameworks that generate visual foresights together with actions to serve as a process of chain of thought, highlighting its adaptability in accelerating multimodal generation and action prediction. 

### **4.3 Comparison with SOTA (RQ2)** 

**Accelerating UD-VLA on CALVIN.** Table 3 shows that compared with world-modeling VLA (Zhang et al., 2025a) that jointly generate future images and actions, our `Fast-dVLA` applied on UD-VLA inherits the strong representational capacity and the advantages of a unified multimodal latent space, while mitigating the long decoding latency induced by future image tokens through our acceleration technique. These results demonstrate that the unified dVLA paradigm can serve as a practical and viable solution for VLAs with a world-modeling process. 

**Accelerating Dream-VLA on SimplerEnv.** On the SimplerEnv, which more closely reflects real-world robotic evaluation settings with high visual fidelity, our results are consistent with those observed on CALVIN. Table 4 shows that our `Fast-dVLA` achieves the highest decoding speeds among all VLAs with discrete outputs, including AR paradigms (OpenVLA and _π_ 0-FAST), vanilla dVLA paradigms (DD-VLA and LLaDA-VLA), and block diffusion paradigms (Dream-VLA with Fast-dLLM or Block Diffusion). This improvement stems from the effective combination of KV caching and inner/inter-block parallelism. 

In terms of task success rates, benefiting from the superior cross-modal alignment of dVLAs, our `Fast-dVLA` outperforms continuous flow-matching approaches such as GR00T-N1 and _π_ 0. Furthermore, leveraging the sequential action representation induced by our method and the large-scale robot pretraining of Dream-VLA, our `Fast-dVLA` also surpasses existing dVLA methods. 

For the comprehensive comparison on LIBERO, please refer to the supplementary materials. 

8 

**Table 3** Comprehensive evaluation of long-horizon manipulation on the CALVIN benchmark. UniVLA<sup>_∗_</sup> denotes the variant without historical frames for fair comparison. 

|**Method**|**Task**|**T**|**asks Co**|**mpleted**|**in a Ro**|**w**|**Avg. Len.** _↑_|
|---|---|---|---|---|---|---|---|
|||1/5|2/5|3/5|4/5|5/5||
|RT-1 (Brohan et al.,2023)|ABCD_→_D|0.844|0.617|0.438|0.323|0.227|2.45|
|LLaDA-VLA (Wen et al.,2025c)|ABCD_→_D|0.956|0.878|0.795|0.739|0.645|4.01|
|Deer (Yue et al.,2024b)|ABCD_→_D|0.982|0.902|0.821|0.759|0.670|4.13|
|GR-1 (Wu et al.,2024)|ABCD_→_D|0.949|0.896|0.844|0.789|0.731|4.21|
|ReconVLA (Song et al.,2025c)|ABCD_→_D|0.980|0.900|0.845|0.785|0.705|4.23|
|UniVLA<sup>_∗_</sup>(Wang et al.,2025b)|ABCD_→_D|0.948|0.906|0.862|0.834|0.690|4.26|
|MODE (Reuss et al.,2025a)|ABCD_→_D|0.971|0.925|0.879|0.835|0.779|4.39|
|UP-VLA (Zhang et al.,2025a)|ABCD_→_D|0.962|0.921|0.879|0.842|0.812|4.42|
|MDT (Reuss et al.,2024)|ABCD_→_D|0.986|0.958|0.916|0.862|0.801|4.52|
|**UD-VLA +****`Fast-dVLA` (ours)**|ABCD_→_D|0.984|0.952|0.922|0.870|0.812|**4.54**|


**Table 4** Evaluation on WidowX Robot tasks in SimplerEnv. We report the Grasping Success Rate (Grasp) and Task Success Rate (Success) in percentages (%). Besides, we further report the decode speed (Speed) of all VLAs with discrete output, which is calculated in tokens per second. 

|**Method**|**Spoon**|**on Towel**|**Carrot**|**on Plate**|**Stack G**|**reen Block**|**Eggplan**|**t in Basket**|**Aver**|**age**|
|---|---|---|---|---|---|---|---|---|---|---|
||Grasp|Success|Grasp|Success|Grasp|Success|Grasp|Success|Success|Speed|
|RoboVLM (Liu et al.,2025a)|37.5|20.8|33.3|25.0|8.3|8.3|0.0|0.0|13.5|-|
|SpatialVLA (Qu et al.,2025)|20.8|16.7|29.2|25.0|62.5|29.2|**100.0**|**100.0**|42.7|-|
|OpenVLA-OFT (Kim et al.,2025a)|50.0|12.5|41.7|4.2|70.8|20.8|91.7|37.5|18.8|-|
|_π_0 (Black et al.,2024)|45.8|29.1|25.0|0.0|50.0|16.6|91.6|62.5|27.1|-|
|_π_0-FAST (Pertsch et al.,2025)|62.5|29.1|58.5|21.9|54.0|10.8|83.3|66.6|32.1|107.5|
|GR00T-N1 (Bjorck et al.,2025)|**83.3**|**62.5**|54.2|45.8|70.8|16.7|41.7|20.8|36.5|-|
|DDVLA (Liang et al.,2025b)|70.8|29.2|58.3|29.2|62.5|20.8|91.7|70.8|37.5|152.8|
|LLaDA-VLA (Wen et al.,2025c)|-|56.9|-|**76.3**|-|30.6|-|58.3|55.5|160.0|
|Dream-VLA (Ye et al.,2025a)|79.2|45.8|62.5|45.8|**83.3**|25.0|**100.0**|87.5|51.0|100.1|
|+ Fast-dLLM (Wu et al.,2025)|70.8|41.7|54.2|37.5|70.8|20.8|83.3|66.6|41.7|214.2|
|+ Block Diffusion (Arriola et al.,2025)|**83.3**|54.1|**66.7**|45.8|**83.3**|29.1|95.8|91.6|55.2|226.4|
|+`Fast-dVLA`(ours)|**83.3**|54.1|62.5|54.1|**83.3**|**37.5**|**100.0**|91.6|**59.3**|**366.4**|


### **4.4 Real-world Experiments (RQ3)** 

**Setup.** Real-world experiments were conducted on a bimanual AgileX platform, where each 6-DOF arm is equipped with a gripper. The sensory suite includes a high-mounted overhead camera providing a global perspective and two wrist-mounted cameras for localized views. 

**Task setting.** We designed three distinct tasks, as illustrated in Figure 7: (1) _Conveyor Picking_ , which involves picking blocks from a moving conveyor belt and placing them into a tray. (2) _Vegetables Stowing_ , which requires sorting vegetables based on their text labels in a container. (3) _Vegetables Retrieving_ , which involves grasping a target vegetable and placing it into a pot according to specific language instructions. For each task, we collected 100 expert demonstrations for training. For evaluation, we conducted 40 trials per task, recording the success rate and the average completion time. Specifically, for the conveyor belt task, we utilized the number of successful grasps per minute as the primary evaluation metric to quantify performance. In addition, we recorded the execution frequency on the real-world robot platform to quantify the real-time performance. 

**Results.** We evaluate our method against two representative models: _π_ 0-FAST (Pertsch et al., 2025) (the SOTA AR VLA) and Dream-VLA (Ye et al., 2025a), a representative dVLA that acts as our base model. Figure 7 shows our model demonstrates robust performance across all three tasks. Notably, the conveyor belt picking task requires both precise grasping and real-time responsiveness. Our method achieves nearly double the efficiency of previous approaches, closely aligned with the practical demands of industrial sorting systems. In the remaining two tasks that require semantic understanding, our model maintains competitive performance with only a marginal reduction in success rate relative to the baseline, while further shortening the required completion time. Crucially, our system maintains a consistent execution frequency of 30 Hz across all tasks, satisfying the practical demand of real-time control that other approaches fail to meet. These results underscore 

9 


**Figure 7** Real-world experiment results. We report (a) successful grasps per minute ( _↑_ ); (b) success rates ( _↑_ ) and completion times ( _↓_ ); (c) execution frequency ( _↑_ ). 

our model’s efficient execution and precise instruction-following capabilities. 

### **4.5 Training Efficiency (RQ4)** 


To evaluate the training efficiency of our `Fast-dVLA` , we compare four training strategies based on Dream-VLA on LIBERO: (1) _Asymmetric Distillation from Finetuned Weight (L_ AD _)._ This approach distills our `Fast-dVLA` from the task-specific finetuned weight using _L_ AD. (2) _Training from Finetuned Weight (L_ BD _)._ This approach trains `Fast-dVLA` from the finetuned weight with _L_ BD. (3) _Training From Scratch (L_ BD _)._ This approach trains our `Fast-dVLA` from the pretrained dVLA. (4) _Training From Scratch (L_ act _)._ This approach finetunes a normal dVLA on the specific tasks to serve as the baseline for comparison. 

**Figure 8** Action Mean Squared Error (MSE) of the dVLA at varying training steps on LIBERO. The MSE of our asymmetric distillation exhibits the fastest decline, indicating the most rapid convergence speed. 

distillation exhibits the fastest decline, indicating the most Figure 8 shows that our asymmetric distillation rapid convergence speed. demonstrates significantly superior training efficiency. Notably, the distillation strategy (blue line) requires only 2,000 training steps to converge, which is 5 _×_ faster than continuing to train from the finetuned weight (orange line) and approximately 1/10 of the steps needed for training from scratch (green line). From another perspective, our asymmetric distillation offers a cost-efficient pathway to accelerate existing dVLA models to real-time performance required for practical applications. Besides, all strategies for training our `Fast-dVLA` converge faster than finetuning a normal dVLA (red line), denoting that our architecture is more efficient. 

### **4.6 Ablation Studies (RQ5)** 

**Block size aligned with action dimensionality brings better performance.** We validate the importance of choosing the multiples of the action dimensionality as the block size. To ensure fairness, the results are averaged from several values between the sizes of 7 (action token numbers in one step) and 14. Specifically, we find that this choice better maintains success rates and speedup, demonstrating its coherence with the action architecture that better keeps the intrinsic temporal dependencies of the action tokens (see Table 5). 

**Ablation of** _τ_ **conf.** For the confidence threshold _τ_ conf in the semi-activated block, lowering the threshold yields an approximately linear drop in performance while improving inference speed. As shown in Figure 9, we set the confidence threshold to 0.5 to balance these two factors, achieving a 2.8 _×_ acceleration while incurring a marginal performance drop of 2%. 

10 


**Figure 9** Ablation study on the confidence threshold _τ_ conf of `Fast-dVLA` based on UD-VLA. 

## **5 Related Works** 

_Discrete Diffusion VLA (dVLA)._ In this paper, we extend the notion of dLLM (Yu et al., 2025) to the embodied domain and define dVLA, a VLA model that enables parallel decoding of multiple action tokens (and optionally tokens from other modalities) through an iterative denoising-based inference procedure. PD-VLA (Song et al., 2025b) first adopts Jacobi decoding to enable AR VLA to predict in parallel action tokens without training. Then, DD-VLA (Liang et al., 2025b) and LLADA-VLA (Wen et al., 2025c) follow the BERT-style (Devlin et al., 2019) masked prediction strategy, where selected action 

**Table 5** Choice of block size on LIBERO-Long based on Dream-VLA. Here, multiples denotes that the value is the multiples of the dimensionality of action, while random denotes random numbers for the block size. 

|Block|Success Rate|Speedup|
|---|---|---|
|Multiples|74.7%|4.01_×_|
|Ramdom|73.3%|3.95_×_|


tokens are replaced with a special mask token, and the model directly learns to predict the original tokens at these masked positions. Dream-VLA (Ye et al., 2025a) performs a large-scale robotic pretraining on a diffusion vision-language model to inject embodied capabilities. UD-VLA (Chen et al., 2025), MM-ACT (Liang et al., 2025a) and dVLA (Wen et al., 2025a) integrate visual CoT or textual CoT into discrete diffusion–based VLA models and jointly diffuse future frames, textual reasoning traces, and actions within a single unified framework. However, they overlook the bottleneck in inference speed, thereby leaving a gap in real-world applications. 

_Acceleration of VLA._ Recent efforts of efficient VLA focus on pruning for redundancy reduction. MoLeVLA (Zhang et al., 2025b) dynamically activates layers via a Mixture-of-Layers design. EfficientVLA (Yang et al., 2025) proposes a training-free acceleration framework combining layer pruning, token selection, and diffusion caching. ADP (Pei et al., 2025) and LightVLA (Jiang et al., 2025) introduce action-aware and differentiable token pruning strategies, respectively, to reduce visual redundancy while maintaining performance. Beyond pruning, early-exit strategies have also been explored to reduce cost. DeeR-VLA (Yue et al., 2024a) adaptively adjusts the effective model depth, while CEED-VLA (Song et al., 2025a) enables early termination over iterative steps during inference. Another effective method is caching. VLA-Cache (Xu et al., 2025), for example, improves efficiency by caching static tokens and recomputing only task-dependent components. Similarly, CronusVLA (Li et al., 2025) proposes feature-level token caching via a FIFO queue, decoupling expensive single-frame perception from lightweight multi-frame reasoning. Researchers are also exploring novel architectures and optimization techniques. RoboMamba (Liu et al., 2024) integrates Mamba state-space modeling into the VLA 

11 

framework to achieve efficient robotic reasoning. In parallel, quantization techniques, such as those proposed by BitVLA (Wang et al., 2025a) and QVLA (Xu et al., 2026), enable the deployment of VLA models on hardware with limited resources by using low-bit representations. Finally, the development of lightweight backbones from the ground up offers a direct path to efficiency. TinyVLA (Wen et al., 2025b) pursues this by designing compact architectures from scratch. Flower (Reuss et al., 2025b) proposes an efficient 950M-parameter diffusion-based VLA that uses intermediate-modality fusion and action-specific conditioning. Meanwhile, SmolVLA (Shukor et al., 2025) combines application-level pruning with spatial compaction through pixel rearrangement. However, these works do not specifically address the acceleration of dVLA. In contrast, our work systematically investigates acceleration strategies tailored to the unique characteristics of dVLA, thereby filling this gap. 

## **6 Conclusion** 

In this paper, we tackle key limitations in the inference speed of dVLAs. Specifically, we reveal an implicit blockwise AR decoding tendency in the fully bidirectional dVLA. Thus, we propose `Fast-dVLA` , which leverages block-wise diffusion with a corresponding attention pattern to allow KV cache reuse, while allowing inter-block parallelism through diffusion forcing. We also curate an efficient training process and a pipelined inference for real-time inference. Extensive experiments on simulated benchmarks and real-world tasks demonstrate up to 4.1 _×_ acceleration over existing dVLA models, while maintaining SOTA-level success rates. These findings offer a practical solution for deploying dVLAs as competitive alternatives to continuous flow-matching VLAs in real-world applications. 

## **References** 

- Marianne Arriola, Aaron Gokaslan, Justin T Chiu, Zhihan Yang, Zhixuan Qi, Jiaqi Han, Subham Sekhar Sahoo, and Volodymyr Kuleshov. Block diffusion: Interpolating between autoregressive and diffusion language models. _arXiv preprint arXiv:2503.09573_ , 2025. 

- Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alexander Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. Robotics: Science and Systems Foundation, 2023. 

- Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 

- Boyuan Chen, Diego Martí Monsó, Yilun Du, Max Simchowitz, Russ Tedrake, and Vincent Sitzmann. Diffusion forcing: Next-token prediction meets full-sequence diffusion. _Advances in Neural Information Processing Systems_ , 37:24081–24125, 2024. 

- Jiayi Chen, Wenxuan Song, Pengxiang Ding, Ziyang Zhou, Han Zhao, Feilong Tang, Donglin Wang, and Haoang Li. Unified diffusion vla: Vision-language-action model via joint discrete denoising diffusion process. _arXiv preprint arXiv:2511.01718_ , 2025. 

- Can Cui, Pengxiang Ding, Wenxuan Song, Shuanghao Bai, Xinyang Tong, Zirui Ge, Runze Suo, Wanqi Zhou, Yang Liu, Bofang Jia, et al. Openhelix: A short survey, empirical analysis, and open-source dual-system vla model for robotic manipulation. _arXiv preprint arXiv:2505.03912_ , 2025. 

- Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deep bidirectional transformers for language understanding. In _Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, volume 1 (long and short papers)_ , pages 4171–4186, 2019. 

- Chi-Pin Huang, Yueh-Hua Wu, Min-Hung Chen, Yu-Chiang Frank Wang, and Fu-En Yang. Thinkact: Vision-language-action reasoning via reinforced visual latent planning. _arXiv preprint arXiv:2507.16815_ , 2025. 

12 

- Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. pi0.5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- Titong Jiang, Xuefeng Jiang, Yuan Ma, Xin Wen, Bailin Li, Kun Zhan, Peng Jia, Yahui Liu, Sheng Sun, and Xianpeng Lang. The better you learn, the smarter you prune: Towards efficient vision-language-action models via differentiable token pruning. _arXiv preprint arXiv:2509.12594_ , 2025. 

- Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025a. 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P Foster, Pannag R Sanketi, Quan Vuong, et al. Openvla: An open-source vision-language-action model. In _Conference on Robot Learning_ , pages 2679–2713. PMLR, 2025b. 

- Jason Lee, Jiafei Duan, Haoquan Fang, Yuquan Deng, Shuo Liu, Boyang Li, Bohan Fang, Jieyu Zhang, Yi Ru Wang, Sangho Lee, et al. Molmoact: Action reasoning models that can reason in space. _arXiv preprint arXiv:2508.07917_ , 2025. 

- Hao Li, Shuai Yang, Yilun Chen, Yang Tian, Xiaoda Yang, Xinyi Chen, Hanqing Wang, Tai Wang, Feng Zhao, Dahua Lin, et al. Cronusvla: Transferring latent motion across time for multi-frame prediction in manipulation. _arXiv preprint arXiv:2506.19816_ , 2025. 

- Lin Li, Qihang Zhang, Yiming Luo, Shuai Yang, Ruilin Wang, Fei Han, Mingrui Yu, Zelin Gao, Nan Xue, Xing Zhu, et al. Causal world modeling for robot control. _arXiv preprint arXiv:2601.21998_ , 2026. 

- Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, Sergey Levine, Jiajun Wu, Chelsea Finn, Hao Su, Quan Vuong, and Ted Xiao. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 

- Haotian Liang, Xinyi Chen, Bin Wang, Mingkang Chen, Yitian Liu, Yuhao Zhang, Zanxin Chen, Tianshuo Yang, Yilun Chen, Jiangmiao Pang, et al. Mm-act: Learn from multimodal parallel generation to act. _arXiv preprint arXiv:2512.00975_ , 2025a. 

- Zhixuan Liang, Yizhuo Li, Tianshuo Yang, Chengyue Wu, Sitong Mao, Tian Nian, Liuao Pei, Shunbo Zhou, Xiaokang Yang, Jiangmiao Pang, et al. Discrete diffusion vla: Bringing discrete diffusion to action decoding in vision-language-action policies. _arXiv preprint arXiv:2508.20072_ , 2025b. 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _arXiv preprint arXiv:2306.03310_ , 2023. 

- Huaping Liu, Xinghang Li, Peiyan Li, Minghuan Liu, Dong Wang, Jirong Liu, Bingyi Kang, Xiao Ma, Tao Kong, and Hanbo Zhang. Towards generalist robot policies: What matters in building vision-language-action models. 2025a. 

- Jiaming Liu, Mengzhen Liu, Zhenyu Wang, Lily Lee, Kaichen Zhou, Pengju An, Senqiao Yang, Renrui Zhang, Yandong Guo, and Shanghang Zhang. Robomamba: Multimodal state space model for efficient robot reasoning and manipulation. _arXiv e-prints_ , pages arXiv–2406, 2024. 

- Jiaming Liu, Hao Chen, Pengju An, Zhuoyang Liu, Renrui Zhang, Chenyang Gu, Xiaoqi Li, Ziyu Guo, Sixiang Chen, Mengzhen Liu, et al. Hybridvla: Collaborative diffusion and autoregression in a unified vision-language-action model. _arXiv preprint arXiv:2503.10631_ , 2025b. 

- Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters (RA-L)_ , 7(3):7327–7334, 2022. 

- Octo Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 

- Jonas Pai, Liam Achenbach, Victoriano Montesinos, Benedek Forrai, Oier Mees, and Elvis Nava. mimic-video: Video-action models for generalizable robot control beyond vlas. _arXiv preprint arXiv:2512.15692_ , 2025. 

- Xiaohuan Pei, Yuxing Chen, Siyu Xu, Yunke Wang, Yuheng Shi, and Chang Xu. Action-aware dynamic pruning for efficient vision-language-action manipulation. _arXiv preprint arXiv:2509.22093_ , 2025. 

- Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

13 

- Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- Moritz Reuss, Ömer Erdinç Yağmurlu, Fabian Wenzel, and Rudolf Lioutikov. Multimodal diffusion transformer: Learning versatile behavior from multimodal goals. _Robotics: Science and Systems XX. Ed.: D. Kulic_ , 2024. 

- Moritz Reuss, Jyothish Pari, Pulkit Agrawal, and Rudolf Lioutikov. Efficient diffusion transformer policies with mixture of expert denoisers for multitask learning. In _The Thirteenth International Conference on Learning Representations_ , 2025a. 

- Moritz Reuss, Hongyi Zhou, Marcel Rühle, Ömer Erdinç Yağmurlu, Fabian Otto, and Rudolf Lioutikov. Flower: Democratizing generalist robot policies with efficient vision-language-action flow policies. _arXiv preprint arXiv:2509.04996_ , 2025b. 

- Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, et al. Smolvla: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

- Wenxuan Song, Jiayi Chen, Pengxiang Ding, Yuxin Huang, Han Zhao, Donglin Wang, and Haoang Li. Ceed-vla: Consistency vision-language-action model with early-exit decoding. _arXiv preprint arXiv:2506.13725_ , 2025a. 

- Wenxuan Song, Jiayi Chen, Pengxiang Ding, Han Zhao, Wei Zhao, Zhide Zhong, Zongyuan Ge, Jun Ma, and Haoang Li. Accelerating vision-language-action model integrated with action chunking via parallel decoding. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2025b. 

- Wenxuan Song, Ziyang Zhou, Han Zhao, Jiayi Chen, Pengxiang Ding, Haodong Yan, Yuxin Huang, Feilong Tang, Donglin Wang, and Haoang Li. Reconvla: Reconstructive vision-language-action model as effective robot perceiver. _arXiv preprint arXiv:2508.10333_ , 2025c. 

- Hongyu Wang, Chuyan Xiong, Ruiping Wang, and Xilin Chen. Bitvla: 1-bit vision-language-action models for robotics manipulation. _arXiv preprint arXiv:2506.07530_ , 2025a. 

- Xu Wang, Chenkai Xu, Yijie Jin, Jiachun Jin, Hao Zhang, Kai Yu, and Zhijie Deng. Diffusion LLMs can do faster-than-AR inference via discrete diffusion forcing. In _The Fourteenth International Conference on Learning Representations_ , 2026. `https://openreview.net/forum?id=t5uLZSRjhF` . 

- Yuqi Wang, Xinghang Li, Wenxuan Wang, Junbo Zhang, Yingyan Li, Yuntao Chen, Xinlong Wang, and Zhaoxiang Zhang. Unified vision-language-action model. _arXiv preprint arXiv:2506.19850_ , 2025b. 

- Junjie Wen, Minjie Zhu, Jiaming Liu, Zhiyuan Liu, Yicun Yang, Linfeng Zhang, Shanghang Zhang, Yichen Zhu, and Yi Xu. dvla: Diffusion vision-language-action model with multimodal chain-of-thought. _arXiv preprint arXiv:2509.25681_ , 2025a. 

- Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Zhibin Tang, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, Yaxin Peng, Feifei Feng, and Jian Tang. Tinyvla: Toward fast, data-efficient vision-language-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 10(4):3988–3995, 2025b. doi: 10.1109/LRA.2025.3544909. 

- Yuqing Wen, Hebei Li, Kefan Gu, Yucheng Zhao, Tiancai Wang, and Xiaoyan Sun. Llada-vla: Vision language diffusion action models. _arXiv preprint arXiv:2509.06932_ , 2025c. 

- Chengyue Wu, Hao Zhang, Shuchen Xue, Zhijian Liu, Shizhe Diao, Ligeng Zhu, Ping Luo, Song Han, and Enze Xie. Fast-dllm: Training-free acceleration of diffusion llm by enabling kv cache and parallel decoding. _arXiv preprint arXiv:2505.22618_ , 2025. 

- Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. Unleashing large-scale video generative pre-training for visual robot manipulation. In _International Conference on Learning Representations_ , 2024. 

- Siyu Xu, Yunke Wang, Chenghao Xia, Dihao Zhu, Tao Huang, and Chang Xu. Vla-cache: Towards efficient vision-languageaction model via adaptive token caching in robotic manipulation, 2025. 

- Yuhao Xu, Yantai Yang, Zhenyang Fan, Yufan Liu, Yuming Li, Bing Li, and Zhipeng Zhang. Qvla: Not all channels are equal in vision-language-action model’s quantization. _arXiv preprint arXiv:2602.03782_ , 2026. 

- Haodong Yan, Zhide Zhong, Jiaguan Zhu, Junjie He, Weilin Yuan, Wenxuan Song, Xin Gong, Yingjie Cai, Guanyi Zhao, Xu Yan, et al. S-vam: Shortcut video-action model by self-distilling geometric and semantic foresight. _arXiv preprint arXiv:2603.16195_ , 2026. 

14 

- Yantai Yang, Yuhao Wang, Zichen Wen, Luo Zhongwei, Chang Zou, Zhipeng Zhang, Chuan Wen, and Linfeng Zhang. Efficientvla: Training-free acceleration and compression for vision-language-action models. _arXiv preprint arXiv:2506.10100_ , 2025. 

- Jiacheng Ye, Shansan Gong, Jiahui Gao, Junming Fan, Shuang Wu, Wei Bi, Haoli Bai, Lifeng Shang, and Lingpeng Kong. Dream-vl & dream-vla: Open vision-language and vision-language-action models with diffusion language model backbone. _arXiv preprint arXiv:2512.22615_ , 2025a. 

- Jiacheng Ye, Zhihui Xie, Lin Zheng, Jiahui Gao, Zirui Wu, Xin Jiang, Zhenguo Li, and Lingpeng Kong. Dream 7b: Diffusion large language models. _arXiv preprint arXiv:2508.15487_ , 2025b. 

- Tianwei Yin, Qiang Zhang, Richard Zhang, William T Freeman, Fredo Durand, Eli Shechtman, and Xun Huang. From slow bidirectional to fast autoregressive video diffusion models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 22963–22974, 2025. 

- Runpeng Yu, Qi Li, and Xinchao Wang. Discrete diffusion in large language and multimodal models: A survey. _arXiv preprint arXiv:2506.13759_ , 2025. 

- Yang Yue, Yulin Wang, Bingyi Kang, Yizeng Han, Shenzhi Wang, Shiji Song, Jiashi Feng, and Gao Huang. Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution. In _The Thirty-eighth Annual Conference on Neural Information Processing Systems_ , 2024a. 

- Yang Yue, Yulin Wang, Bingyi Kang, Yizeng Han, Shenzhi Wang, Shiji Song, Jiashi Feng, and Gao Huang. Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution. _Advances in Neural Information Processing Systems_ , 37:56619–56643, 2024b. 

- Jianke Zhang, Yanjiang Guo, Yucheng Hu, Xiaoyu Chen, Xiang Zhu, and Jianyu Chen. Up-vla: A unified understanding and prediction model for embodied agent. _arXiv preprint arXiv:2501.18867_ , 2025a. 

- Rongyu Zhang, Menghang Dong, Yuan Zhang, Liang Heng, Xiaowei Chi, Gaole Dai, Li Du, Yuan Du, and Shanghang Zhang. Mole-vla: Dynamic layer-skipping vision language action model via mixture-of-layers for efficient robot manipulation. _arXiv preprint arXiv:2503.20384_ , 2025b. 

- Wenyao Zhang, Hongsi Liu, Zekun Qi, Yunnan Wang, Xinqiang Yu, Jiazhao Zhang, Runpei Dong, Jiawei He, He Wang, Zhizheng Zhang, et al. Dreamvla: a vision-language-action model dreamed with comprehensive world knowledge. _arXiv preprint arXiv:2507.04447_ , 2025c. 

- Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. pages 1702–1713, 2025. 

- Chuanxia Zheng, Tung-Long Vuong, Jianfei Cai, and Dinh Phung. Movq: Modulating quantized vectors for high-fidelity image generation. _Advances in Neural Information Processing Systems_ , 35:23412–23425, 2022. 

- Zhide Zhong, Haodong Yan, Junfeng Li, Xiangchen Liu, Xin Gong, Wenxuan Song, Jiayi Chen, and Haoang Li. Flowvla: Thinking in motion with a visual chain of thought. _arXiv preprint arXiv:2508.18269_ , 2025. 

- Zhide Zhong, Junfeng Li, Junjie He, Haodong Yan, Xin Gong, Guanyi Zhao, Yingjie Cai, Jiantao Gao, Xu Yan, Bingbing Liu, et al. Dualcot-vla: Visual-linguistic chain of thought via parallel reasoning for vision-language-action models. _arXiv preprint arXiv:2603.22280_ , 2026. 

15 

**Table S1** Ablation study on block expansion threshold _τ_ add and block activation threshold _τ_ act on UD-VLA. 

|_τ_add|_τ_act|avg. len. _↑_|Speed_↑_|
|---|---|---|---|
|0.4|0.4|4.42|**253.1**|
|0.4|0.6|4.46|248.3|
|0.5|0.5|4.44|204.8|
|0.5|0.7|4.54|186.7|
|0.6|0.6|4.52|182.3|
|0.6|0.8|**4.57**|160.7|


**Table S2** Comparison with various base models in terms of inference speed, average length, and execution frequency. 

|Radical Decoding|Speed (Tokens/s)|Avg. Len.|
|---|---|---|
|log2|186.67|4.54|
|log3|164.42|4.57|
|log4|144.71|4.58|


# Appendix 

This supplementary material provides additional analyses and implementation details for `Fast-dVLA` . We first present ablation studies on the decoding hyperparameters, including the block expansion and activation thresholds in Section A and the radical decoding strategy in fully activated blocks in Section B. We then describe the implementation details in Section C and provide the detailed inference procedure in Section D. Next, we summarize the evaluation benchmarks in Section E, followed by the comparison with state-of-the-art methods on LIBERO in Section F. 

## **A Ablation of** _τ_ **add and** _τ_ **act.** 

We conduct an ablation study on _τ_ add and _τ_ act based on UD-VLA (see Table S1). When _τ_ add = _τ_ act, a newly added block immediately becomes fully activated, causing the dual-state decoding scheme to degenerate into a single-state regime. The results show that our `Fast-dVLA` is not sensitive to these hyperparameters. _τ_ add and _τ_ act exhibit a positive correlation with task performance and a negative correlation with decoding speed. Importantly, the proposed dual-state decoding mechanism incurs significantly performance degradation while maintaining decoding speed comparable to the single-state variant. For scenarios that demand high action accuracy, we adopt a more conservative dual-state configuration (i.e., _τ_ add _< τ_ act) to better preserve performance. 

## **B Ablation Study of Radical Decoding in Fully Activated Blocks** 

We further conduct an ablation study on the radical decoding strategy used in fully activated blocks. Specifically, we vary the radical decoding factor among `log2` , `log3` , and `log4` . Here, `log2` corresponds to the most aggressive setting, where a fully activated block decodes at least half of its remaining tokens in one iteration. 

As shown in Table S2, our `Fast-dVLA` is fairly robust to different radical decoding factors. Although more conservative settings such as `log3` and `log4` slightly reduce the decoding speed, the average success length remains largely stable across all configurations. In particular, `log2` achieves the highest decoding speed of 186.67 tokens/s, while maintaining a comparable average success length of 4.54. These results suggest that our `Fast-dVLA` is not highly sensitive to the choice of the radical decoding factor, and that the aggressive `log2` setting provides the best efficiency-performance trade-off. 

## **C Implementation Details.** 

We employ LoRA-based asymmetric distillation throughout. The LoRA rank is set to 32. During distillation, LoRA branches are disabled when computing teacher output logits. In contrast, LoRA branches are activated 

16 

**Algorithm 1** Confidence-Guided Block Decoding with Logarithmic Scheduling 

**Require:** Fast-dVLA model _pθ_ ; block expansion threshold _τ_ add; block activation threshold _τ_ act; confidence threshold _τ_ conf; logarithmic scheduling factor _n_ . 1: Initialize _Y_ = _{YB_ 1 _}_ as a single block filled with `[MASK]` tokens. 2: **while** generation is not complete **do** 3: **if** the decoded ratio in _YBi−_ 1 exceeds _τ_ add **and** `<|EOA|>` not in _Y_ **then** 4: Append a new block _YBi_ with all tokens masked and mark it as _semi-activated_ . 5: **end if** 6: Perform a forward pass on _Y_ using Fast-dVLA _pθ_ with cached KV. 7: **for** each active block _YBi_ in _Y_ **do** 8: Let _Ri_ denote the set of remaining masked token positions in _Bi_ . 9: Compute confidence scores **c** _i_ for all positions in _Ri_ . 10: **if** _YBi_ is _fully activated_ **then** 11: Set _k ←⌊|Ri|_ / _n⌋_ . 12: Compute the block-specific decoding threshold: _τi ←_ min� _τ_ conf, min(TopK( **c** _i_ , _k_ ))�. 13: **else** 14: Set _τi ← τ_ conf. 15: **end if** 16: Construct the decoding candidate set _Si ←{ p ∈Ri | ci_ ( _p_ ) _≥ τi }_ . 17: Decode tokens at positions in _Si_ and remain others as mask token in _Bi_ . 18: **if** the decoded ratio in _YBi−_ 1 exceeds _τ_ act **then** 19: Mark _YBi_ as _fully activated_ . 20: **end if** 21: **end for** 22: Update the KV cache for completed blocks. 23: **end while** 

when computing student model output logits. This design maximally preserves the pretrained dVLA backbone’s visual–language understanding and action-reasoning priors, while allowing the LoRA modules to focus solely on learning the transfer of attention pattern. 

For both Dream-VLA and DD-VLA, we set the action chunk size to 8, and to 5 for the SIMPLER tasks. For UD-VLA, the action chunk size is set to 10. All other training hyperparameters follow the official settings. 

## **D Inference Details.** 

The detailed inference pseudocode is provided in Algorithm 1. 

## **E Benchmarks** 

**CALVIN.** The CALVIN benchmark (Mees et al., 2022) is a simulated suite for evaluating long-horizon, languageconditioned robotic manipulation. It spans four environments (A, B, C, and D) with 34 tasks and 1,000 language instructions. We evaluate 500 rollouts per model, where each rollout involves a sequence of 5 consecutive sub-tasks. We report the average length (avg. len.) of successful sub-task completions of all rollouts with a maximum value of 5. 

**LIBERO.** LIBERO (Liu et al., 2023) is a simulated manipulation benchmark with 4 suites (Spatial, Object, Goal, Long). Spatial probes layout reasoning, Object tests object generalization, Goal evaluates goal-conditioned control, and Long targets long-horizon compositional skills. We report success rates per suite and overall average, each suite containing 10 tasks and 50 rollouts per task. 

**SimplerEnv.** SimplerEnv (Li et al., 2024) is a real-to-sim suite for assessing transfer and generalization of robot policies trained on real-world video data. We evaluate on WidowX robots under varied lighting, textures, colors, and viewpoints. Tasks include _Put Spoon on Towel_ , _Put Carrot on Plate_ , _Stack Green on Yellow Block_ , and _Put Eggplant in Yellow Basket_ . We report per-task success rates and the overall average. 

17 

**Table S3 Evaluation and comparison on the LIBERO benchmark.** 

|**Method**|**Spatial**|**Object**|**Goal**|**Long**|**Average**|
|---|---|---|---|---|---|
|Octo (Octo Team et al.,2024)|78.9%|85.7%|84.6%|51.1%|75.1%|
|SpatialVLA (Qu et al.,2025)|88.2%|89.9%|78.6%|55.5%|78.1%|
|CoT-VLA (Zhao et al.,2025)|87.5%|91.6%|87.6%|69.0%|81.1%|
|WorldVLA (Cen et al.,2025)|87.6%|96.2%|83.4%|60.0%|81.8%|
|ThinkAct (Huang et al.,2025)|88.3%|91.4%|87.1%|70.9%|84.4%|
|_π_0-FAST (Pertsch et al.,2025)|96.4%|96.8%|88.6%|60.2%|85.5%|
|MolmoAct (Lee et al.,2025)|87.0%|95.4%|87.6%|77.2%|86.6%|
|FlowVLA (Zhong et al.,2025)|93.2%|95.0%|91.6%|72.6%|88.1%|
|DreamVLA (Zhang et al.,2025c)|97.5%|94.0%|89.5%|89.5%|92.6%|
|_π_0 (Black et al.,2024)|96.8%|**98.8%**|95.8%|85.2%|94.2%|
|_π_0.5 (Intelligence et al.,2025)|**98.8%**|98.2%|**98.0%**|92.4%|**96.8%**|
|DDVLA (Liang et al.,2025b)|97.2%|98.6%|97.4%|92.0%|96.3%|
|+ ours|97.0%|**98.8%**|97.6%|**92.8%**|96.6%|


## **F Comparison with SOTA on LIBERO** 

Table S3 presents the comparison with state-of-the-art methods on the LIBERO benchmark. Overall, our method achieves competitive performance against recent strong VLA baselines, demonstrating that accelerating discrete diffusion VLAs does not compromise policy quality. Built upon DDVLA (Liang et al., 2025b), our method improves the average success rate from 96.3% to 96.6%, while further boosting performance on the most challenging _Long_ suite from 92.0% to 92.8%. The gains on long-horizon tasks suggest that our acceleration strategy preserves, and even slightly enhances, the sequential decision-making capability required for extended manipulation. 

Compared with previous autoregressive and continuous-flow paradigms, our method remains highly competitive across all four suites. In particular, it matches or surpasses strong baselines such as _π_ 0-FAST, MolmoAct, and FlowVLA by a clear margin, and performs comparably to the most recent frontier models, including _π_ 0, _π_ 0.5, and DDVLA. Notably, while _π_ 0.5 achieves the best average success rate, our `Fast-dVLA` delivers stronger performance than DDVLA on _Object_ , _Goal_ , and especially _Long_ , highlighting the effectiveness of our design in improving both robustness and long-horizon execution. 

These results indicate that our method inherits the strong representational capacity of discrete diffusion VLAs, while making them more practical without sacrificing task success. 

18 

