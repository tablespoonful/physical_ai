---
title: "DriveFine: Refining-Augmented Masked Diffusion VLA for Precise and Robust Driving"
date: "2026-02-16"
authors: "Chenxu Dang; Sining Ang; Yongkang Li; Haochen Tian; Jie Wang; Guang Li"
url: https://arxiv.org/abs/2602.14577
pdf: https://arxiv.org/pdf/2602.14577
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.14577)** / [論文ページ](https://arxiv.org/abs/2602.14577)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **DriveFine: Refining-Augmented Masked Diffusion VLA for Precise and Robust Driving** 

Chenxu Dang<sup>1</sup><sup>_,_2</sup><sup>_,_3</sup><sup>_⋆_</sup> , Sining Ang<sup>3</sup> , Yongkang Li<sup>1</sup> , Haochen Tian<sup>2</sup> , Jie Wang<sup>2</sup> , 

Guang Li<sup>2</sup> , Hangjun Ye<sup>2</sup> , Jie Ma<sup>1</sup> , Long Chen<sup>2</sup><sup>_†_</sup> , and Yan Wang<sup>3</sup><sup>_†_</sup> 

> 1 Huazhong University of Science and Technology 

> 2 Xiaomi EV 

> 3 Institute for AI Industry Research (AIR), Tsinghua University 

**Abstract.** Vision-Language-Action (VLA) models for autonomous driving increasingly adopt generative planners trained with imitation learning followed by reinforcement learning. Diffusion-based planners suffer from modality alignment difficulties, low training efficiency, and limited generalization. Token-based planners are plagued by cumulative causal errors and irreversible decoding. In summary, the two dominant paradigms exhibit complementary strengths and weaknesses. In this paper, we propose **DriveFine** , a masked diffusion VLA model that combines flexible decoding with self-correction capabilities. In particular, we design a novel plug-and-play block-MoE, which seamlessly injects a refinement expert on top of the generation expert. By enabling explicit expert selection during inference and gradient blocking during training, the two experts are fully decoupled, preserving the foundational capabilities and generic patterns of the pretrained weights, which highlights the flexibility and extensibility of the block-MoE design. Furthermore, we design a hybrid reinforcement learning strategy that encourages effective exploration of refinement expert while maintaining training stability. Extensive experiments on NAVSIM v1, v2, and Navhard benchmarks demonstrate that DriveFine exhibits strong efficacy and robustness. The code will be released at `https://github.com/MSunDYY/DriveFine` . 

**Keywords:** Masked Diffusion LLM · Reinforcement Learning · Block MoE · Autonomous Driving 

## **1 Introduction** 

Vision-Language-Action (VLA) systems for autonomous driving (AD) integrate sensor observations and textual instructions, with a planner responsible for generating driving actions or trajectories. Early deterministic planners (e.g., MLPbased [12, 15, 50] or anchor-based classifiers [3, 25]) tended to imitate a single expert trajectory, which struggle with distribution shift and cannot capture the inherently multi-modal nature of driving. 

> _⋆_ Completed during the internship at Xiaomi EV and AIR. _†_ Corresponding authors. 


**Fig. 1:** Comparison of decoding mechanisms for Action Tokens in Generative VLA Models. (a) Parallel refinement with multi-step denoising. (b) Token-by-token decoding. (c) Generate first in parallel, then refine. 

Recently, non-deterministic generative planners have emerged as the dominant paradigms in AD VLAs. They predict actions as probability distributions, effectively capturing the multimodal nature of driving behavior. Moreover, their inherent sampling capability encourages active exploration and enables seamless integration with rule-driven reinforcement learning strategies, such as GRPO, to guide policy learning. Current state-of-the-art generative VLAs can be categorized into diffusion-based models [18, 24, 28, 51] with continuous action modeling and token-based planners [29, 48, 49] with discrete action representations. 

(1) **Diffusion-based VLAs** , as shown in Fig. 1(a) construct a Markov chain and iteratively refine noisy trajectories by predicting their mean and variance. 


Despite the efficiency enabled by parallel decoding, the additional diffusion Transformer hinders cross-modal alignment, leading to inefficient training that typically requires hundreds of epochs. 

Moreover, diffusion-based planners are EPDMS inherently conditional generators, which limits their robustness and generalization **Fig. 2:** PDMS-oriented RFT. ability, as evidenced empirically in Fig. 2: when optimized with PDMS-oriented reinforcement fine-tuning, diffusion-based planners [24,28] suffer a significant drop in EPDMS. Here, both PDMS and EPDMS are metrics provided by NAVSIM [9], see 4.1 for details. We attribute this degradation to the weak coupling between diffusion planners and the VLM, which induces reward hacking and the loss of pretrained knowledge, substantially limiting their practical applicability. 

DriveFine: Refining-Augmented ... 3 


**Fig. 3:** Failure cases caused by irreversible decoding in token-based VLAs. 

(2) **Token-based VLAs** , as illustrated in Fig. 1(b), decode actions into tokens autoregressively within a predefined vocabulary, achieving a unified representation across vision, language, and action. As shown in Fig. 2, the PDMSoriented RFT for InternVL [5] leads to simultaneous improvements in both PDMS and EPDMS, exhibiting its stronger generalization and extensibility. 

However, token-based VLAs [29,49] generally lag behind diffusion-based counterparts [24, 51] in both performance and efficiency. This is mainly due to their causal attention and fixed token-by-token decoding, which is computationally costly and prone to error accumulation during inference. More critically, they inherit the irreversible decoding property of LLMs: decoded tokens cannot be modified once committed. Planning, however, is highly sensitive to noise: even point-level deviations can cause the entire trajectory failure, such as collision or off-road driving (Fig. 3). 

Very recent works [19, 43] explored masked diffusion LLMs [20, 32] (dLLMs) featuring more flexible decoding orders for driving. However, this flexibility aggravates the irreversible decoding problems: as shown in Fig. 3, tokens decoded early lack global consistency constraints, are more likely to become outliers, and cannot be revised afterward, leading to trajectory-level failure. In contrast, diffusion-based planners iteratively refine the trajectory, enabling successive refinement and thereby ensuring high-quality trajectory generation. 

Clearly, both VLA planners exhibit complementary strengths and weaknesses, motivating the exploration of a model harnessing the advantages of both. 

In this paper, we propose **DriveFine** , pioneering the explicit injection of token-VLA’s refining capability for more precise and robust driving. We adopt a pretrained multi-modal masked Diffusion LLM (LaViDa [20] with LLaDA [32] as LLM) as our base planner, considering its several benefits compared with AR LLMs: parallel decoding for efficiency, bidirectional attention for richer context modeling, and a flexible decoding strategy that facilitates adaptive learning. 

The refining of token-VLAs is far from trivial and must adhere to several principles: preserving the base VLM’s original training and inference paradigms to prevent collapse of foundational capabilities; minimizing extra overhead in computation and parameters; remaining decoupled from trajectory generation to avoid interference. Evidently, this presents substantial challenges. 

- 4 C. Dang et al. 

To this end, we design a block-wise Mixture-of-Experts (MoE) architecture. Specifically, the majority of LLaDA blocks serve as shared experts for common contexts, while the remaining blocks are explicitly partitioned into generation experts and refinement experts. During inference, task-specific experts are proactively selected. During training, gradient flow from the refining branch is strictly confined to the refinement experts, decoupling from the generation experts. This explicit isolation preserves the foundational capabilities of the generation experts, effectively preventing mode collapse and cross-task interference. 

To align with the dominant pipeline, we further introduce an online-offline hybrid reinforcement learning paradigm. The generation expert samples a group of trajectories, which are reinforced via GRPO. Simultaneously, these trajectories are paired into offline anchor-target trajectory tuples. In parallel, the refinement expert actively refines the above trajectories, computing the associated rewards and generating online trajectory pairs, which, together with offline pairs, jointly supervise the refinement expert. Experimental results demonstrate that the block-wise MOE significantly enhances trajectory quality with limited parameter increase and slight inference overhead, raising the performance ceiling of token-based VLAs. We summarize our core contributions as follows: 

- We provide a thorough analysis of the strengths and weaknesses of mainstream diffusion-based and token-based VLAs. 

- We propose DriveFine, featuring a plug-and-play block-wise Mixture-ofExperts (block-MoE) that injects refining capability into token-based VLAs at minimal cost. 

- We design a targeted hybrid reinforcement learning strategy to further elevate DriveFine’s performance ceiling. 

- Extensive experiments demonstrate that DriveFine consistently achieves stateof-the-art performance on NavSim v1, v2, and Navhard benchmarks. 

## **2 Related Work** 

### **2.1 End to end Autonomous Driving** 

Early end-to-end planners predominantly relied on deterministic modeling, such as MLP-based regression [6, 12, 15, 34] and anchor-based classification [3], imitating a single expert trajectory. GenAD [46] imposes a GRU-based generator. To align the trajectory diversity, diffusion policies were introduced to recover trajectories from random noise, thereby better aligning with the inherent uncertainty of autonomous driving. Diffusion planners [35, 47] leverage diffusion policies to jointly perform trajectory prediction and planning. GoalFlow [42] adopts goal-conditioned flow matching to generate trajectories, while DiffusionDrive [28] applies truncated diffusion over multiple anchor modes. 

### **2.2 VLAs for Autonomous Driving** 

Conventional end-to-end driving models are often regarded as black boxes. To enhance interpretability, understanding, and reasoning, vision–language models 

DriveFine: Refining-Augmented ... 5 

(VLMs) [1, 5] have been increasingly incorporated into autonomous driving systems in recent years. Early explorations primarily focused on high-level scene understanding [39] and reasoning [13, 31, 40], while the demand for action generation gave rise to a large body of Vision–Language–Action (VLA) models. Early two-stage VLAs [4, 14, 30, 37] generate meta-actions or low-frequency actions from a VLM, followed by an e2e planner for refinement. However, gradient isolation in such pipelines contradicts the principle of end-to-end learning. In contrast, recent one-stage VLAs directly output the final trajectory. For example, OpenDriveVLA [48] autoregressively decodes trajectories, while AutoVLA [49] augments the action vocabulary with clustered anchors. These approaches feature token-based decoding and are thus referred to as token-based VLAs. Other approaches incorporate a planner on top of the VLM to facilitate cross-modal alignment. Orion [11] employs a GRU-based decoder, while recent works [8,18,24] increasingly adopt diffusion policies as planners, achieving stronger performance. 

### **2.3 Reinforcement Learning for Autonomous Driving** 

Imitation learning lacks negative supervision from counterexamples, which leads to poor performance in out-of-distribution (OOD) scenarios. To address this limitation, many studies introduce reinforcement learning to improve the generalization of planners. Early works adopt DPO, while AlphaDrive [16] is the first to introduce GRPO [33]. AdaThinkDrive [29] and AutoVLA [49] directly apply GRPO to token-based VLAs, whereas ReCogDrive [24] designs a diffGRPO. DiffusionDrivev2 [51] further proposes intra- and inter-anchor truncated GRPO strategies. More recently, another scoring-based reinforcement learning models [17, 25, 26] performs stage-wise reasoning under direct reward guidance, leading to stronger performance. 

## **3 Method** 

In this section, we present a detailed introduction of DriveFine with the overview in Fig. 4. Sec. 3.1 describes the formulation of trajectory planning with the pretrained dLLM. Sec 3.2 details the proposed Block-MoE for refinement. Sec 3.3 illustrates the hybrid reinforcement learning strategy. 

### **3.1 Diffusion LLM for Planning** 

**Modatily Tokenization.** As shown in Fig. 4, a single front-view image is processed by a pretrained vision tower (SigLIP [38]) to produce continuous visual tokens, while a text tokenizer converts textual prompts info discrete tokens. 

To preserve the continuity of trajectory and enable token-level refinement, we discretize the action space following prior works [19, 43]. The spatial range [ _−_ 100 _m,_ +100 _m_ ] is uniformly divided into 4,000 bins with a resolution of 0.05 m, shared across longitudinal and lateral axes. The heading angle range [ _−_ 90 _,_ +90] is discretized into 1800 bins with a resolution of 0 _._ 1. These bins are appended to the 

6 C. Dang et al. 


**Fig. 4:** Architecture Overview of DriveFine. Visual and textual inputs are jointly aligned into a unified language space. A set of masked tokens undergoes _s_ steps of parallel denoising followed by a single refinement step. The key difference between the generation expert and the refinement expert lies in their input tokens: the former decodes only the masked tokens, whereas the latter operates on unmasked tokens. 

LLM vocabulary, enabling direct decoding of trajectory tokens and facilitating unified cross-modal alignment between language and actions. 

**Training and Inference.** The generating expert follows the standard dLLM training and inference paradigm. During training, clean sequences are corrupted by random masking, where tokens are replaced by a special mask token [M] with probability _t_ , and supervised via masked cross-entropy loss: 


Here, _L_ , _p_ 0, _r_ 0 and _rt_ denote the sequence length, contextual token, original sequence, and the noised sequence, respectively. 

During the inference stage, the policy model is encouraged to condition on the given inputs (visions and instructions) and progressively reconstruct a feasible trajectory from fully masked trajectory via several iterative unmasking steps. Specifically, at denoising step _t_ , all masked tokens of noised trajectory _rt_ are predicted in parallel by a mask predictor (generation expert). A subset of mask tokens is then decoded to sequence _rt−_ 1 for the next iteration. 

### **3.2 Block-level MoE for Refinement** 

As our previous analysis indicates, the flexible token decoding exacerbates the hazards of irreversible decoding, highlighting the necessity of refinement. 

The most straightforward approach is to introduce additional MoE layers to enable adaptive learning, and apply a loss directly on the unmasked tokens for 

DriveFine: Refining-Augmented ... 7 

supervision. However, this departs from the standard pre-training and inference paradigm of dLLMs, lossing their foundational capabilities, as they learn only to decode the mask tokens. Moreover, the deep coupling between generation and refinement introduces mutual interference and hinders task-specific tuning and optimization. Yet, fully decoupling the components would inevitably result in a dramatic increase in parameters. 

However, despite their different objectives, generation and refinement share a high similarity in contextual representation. Motivated by this insight, we propose our block-level Mixture-of-Experts (block-MoE) together with a carefully designed training–inference pipeline. 

As illustrated in Fig. 4, a diffusion language model (LLaDA) consists of several stacked blocks. We treat the pretrained dLLM as a generation expert in its entirety, and just replicate its last _n_ blocks as refinement blocks, while the preceding blocks and visual tower are shared between both generation and refinement experts. 

**Training and Inference.** During inference, the model is explicitly prompted to perform specific task. The shared blocks extract common contextual representations, following which the corresponding expert blocks are manually activated to execute either generation or refinement. 

During training, the generating branch computes the loss only on masked tokens as in Eq. 1, while the refinement branch computes the loss over all tokens, with gradient flow confined to the refinement expert. Here, the refinement expert undergoes simply warm-started for basic decoding. 

Clearly, our block-MoE achieves complete decoupling between generation and refinement during training and inference. This preserves the foundational knowledge of the pretrained model, preventing catastrophic forgetting. Moreover, the refinement expert is plug-and-play and can be trained synchronously with the generation experts, emphasizing its flexibility and transferability. 

### **3.3 Reinforcement Finetuning** 

Recent studies have demonstrated the critical role of reinforcement learning in autonomous driving both theoretically and empirically. In the following, we detail how reinforcement fine-tuning (RFT) is leveraged to explore and enhance the full potential of DriveFine. 

**GRPO for Generation Expert.** For the generation expert, we employ a rulebased online reinforcement learning strategy, Group Relative Policy Optimization (GRPO). Specifically, given an arbitrary scenario _p_ , the generation expert parallelly samples a group of _G_ candidate trajectories _{xi}_<sup>_G_</sup> _i_ =1<sup>.Following[41],</sup> we progressively sample for _s_ steps to ensure consistency between training and inference, and aggregate every _τ_ neighboring steps to balance alignment and efficiency. For each trajectory _xi_ , we retain � _τs_ � sampled paths _{x_<sup>_j_</sup> _i_<sup>_}⌊_</sup> _j_<sup>_s/τ_</sup> =1<sup>_⌋_.The</sup> 

8 C. Dang et al. 


**Fig. 5:** Reinforcement Fine-tuning Pipeline. The offline advantage and online advantage are jointly combined to form the hybrid advantage to supervise the training of the refinement expert. 

associated rewards _{ri}_<sup>_G_</sup> _i_ =1<sup>are then evaluated in a simulator. Subsequently, with-</sup> out normalization as in [45], the group-relative rewards are computed as follows: 


_x_<sup>_⌊_</sup> 1<sup>_s/τ⌋_</sup> Subsequently, the sampled tokens are processed sequentially, and their losses are computed using the standard GRPO objective: 


where _oi_ denotes the length of the sequence, _ϵ_ controls the clipping range, _β_ balances the KL divergence penalty, and: 


**Hybrid RL for Refining Expert.** The purpose of the optimization expert is to fine-tune the generated trajectories to improve their quality. Compared to the anchor trajectories, corrective actions that lead to score improvements should be encouraged, while those that degrade the score should be penalized, regardless of the anchor itself. Therefore, the generated trajectories naturally serve as a reference for advantage computation, eliminating the need for traditional baseline estimation in reinforcement learning (e.g., the value network in PPO or the 

DriveFine: Refining-Augmented ... 9 

group-average reward in GRPO). Notably, the sampling of trajectories ensures diversity, allowing them to be directly used for training the optimization expert without further modification. Specifically,for sampled trajectories _{xi}_<sup>_G_</sup> _i_ =1<sup>,</sup> we compute pairwise reward differences to obtain a relative advantage matrix. Since the sampled trajectories are produced by the generation expert, they constitute offline data for the refining expert; hence, we define this as an offline reward matrix **A**<sup>ˆ</sup> of _∈_ R _G×G_ : 


The offline advantage matrix offers several benefits: (1) it has zero mean, simultaneously encouraging improvements and penalizing degradations; (2) the squared advantages provide denser reward signals compared to GRPO, enhancing training stability; and (3) it requires no additional sampling, making the computation simple and efficient. 

Despite its many advantages, the optimizer is inherently limited by an upper bound. To encourage the optimizer to explore autonomously, for each generated trajectory _xi_ , we allow it to sample a number of _K_ refined trajectories _{x_ ˆ _ik}_<sup>_K_</sup> _k_ =1 online and compute their corresponding rewards _{r_ ˆ _ik}_<sup>_K_</sup> _k_ =1<sup>simultaneously.The</sup> online reward matrix **A**<sup>ˆ</sup><sup>_on_</sup> _∈_ R<sup>_G×K_</sup> is then calculated as follows: 


Finally, a hybrid loss is computed to optimize the refining expert: 


In our implementation, the generator and refiner are trained synchronously: trajectories are sampled online by the generator and then fed to the refiner for training, thereby enabling their collaborative learning and improvement. 

## **4 Experiments** 

### **4.1 Experimental Settings** 

**Dataset.** We evaluate DriveFine on the NAVSIM [9] dataset, which is built upon nuPlan [2] (a subset of OpenScene [7]) and provides surround-view images from 8 cameras along with high-quality LiDAR point clouds. The dataset is split into 1,192 (navtrain) scenes for training and 136 scenes (navtest) for testing. NAVSIM also offers a simulation environment for closed-loop evaluation. 

NAVSIM v1 adopts the Predictive Driver Model Score (PDMS) as the evaluation metric, which is a weighted aggregation of multiple driving-related criteria, 

10 C. Dang et al. 

**Table 1:** PDMS results on the **NAVSIM-v1** benchmark.<sup>_†_</sup> denotes best-of-6 sampling, and * indicates the appliance of score-based reinforcement training as [17, 26]. 

|Method|Sensors|NC_↑_<br>|DAC_↑_|TTC_↑_|C._↑_|EP_↑_|PDMS_↑_|
|---|---|---|---|---|---|---|---|
|Human|–|100|100|100|99.9|87.5|94.8|
||_En_|_d-to-En_|_d Metho_|_ds_||||
|UniAD [12]|6xC|97.8|91.9|92.9|**100.0**|78.8|83.4|
|TransFuser [6]|3xC+L|97.7|92.8|92.8|**100.0**|79.2|84.0|
|LAW [21]|1xC|96.4|95.4|88.7|99.9|81.7|84.6|
|Hydra-MDP [25]|3xC+L|98.3|96.0|94.6|**100.0**|78.7|86.5|
|DiffusionDrive [28]|3xC+L|98.2|96.2|94.7|**100.0**|82.2|88.1|
|WoTE [23]|3xC+L|98.5|96.8|94.4|99.9|81.9|88.3|
||_Vision L_|_anguage _|_Action _|_Method_|_s_|||
|AutoVLA [49]|3xC|98.4|95.6|**98.0**|99.9|81.9|89.1|
|DriveVLA-W0 [22]|1xC|98.7|**99.1**|95.3|99.3|83.3|90.2|
|AdaThinkDrive [29]|1xC|98.4|97.8|95.2|**100**|84.4|90.3|
|ReCogDrive [24]|1xC|98.2|97.8|95.2|99.8|83.5|89.6|
|DriveFine|1xC|98.6|97.9|95.2|99.9|85.5|90.7|
|DriveFine*|1xC|**98.8**|98.6|96.2|**100**|**86.9**|**91.8**|
|AutoVLA<sup>_†_ </sup>[49]|3xC|99.1|97.1|97.1|**100.0**|87.6|92.1|
|DriveVLA-W0<sup>_†_</sup>|1xC|**99.3**|97.4|97.0|99.9|88.3|93.0|
|AdaThinkDrive<sup>_†_ </sup>[29]|1xC|99.1|98.8|97.2|**100**|87.9|93.0|
|DriveFine<sup>_†_</sup>|1xC|**99.3**|**99.2**|**97.9**|**100**|**89.1**|**94.2**|


including collision avoidance, drivable area compliance, progress–risk trade-off, and comfort. Building upon this metric, NAVSIM v2 introduces the extended PDM Score (EPDMS), which incorporates additional weighted factors such as traffic light compliance, lane boundary adherence, driving direction following, and extended comfort. 

**Implementation Details.** We adopt Siglip-384 [38] as the visual tower, which partitions a single front-view image into 8 patches of size 384 _×_ 384. Pretrained weights from LLaDA-8B [32] are loaded directly, with the first 28 transformer blocks serving as shared blocks and the last 4 blocks designated as expert ones. DriveFine is trained in two stages. In the first stage, it performs supervised fine-tuning (SFT) using the QA pairs and textualized trajectories provided by ReCogDrive [24], without any additional pretraining. In the second stage, it undergoes reinforcement fine-tuning (RFT) in the NAVSIM simulation environment. 

During the SFT stage, the model is trained for 12 epochs with a batch size of 64, optimized using AdamW with a learning rate of 4 _×_ 10<sup>_−_5</sup> and cosine learning rate decay. 

DriveFine: Refining-Augmented ... 11 

**Table 2:** EPDMS results on the `NAVSIM-v2` benchmark.<sup>_†_</sup> indicates results evaluated on the bug-fixed version of NAVSIM. 

|Method|NC_↑_|DAC_↑_|DDC_↑_|TLC_↑_|EP_↑_|TTC_↑_|LK_↑_|C._↑_|EC_↑_|EPDMS_↑_|
|---|---|---|---|---|---|---|---|---|---|---|
|Ego-MLP [27]|93.1|77.9|92.7|99.6|86.0|91.5|89.4|98.3|85.4|64.0|
|TransFuser [6]|96.9|89.9|97.8|99.7|87.1|95.4|92.7|98.3|87.2|76.7|
|DriveSuprim [44]|97.5|96.5|99.4|99.6|88.4|96.6|95.5|98.3|77.0|83.1|
|ARTEMIS [10]|98.3|95.1|98.6|99.8|81.5|97.4|96.5|98.3|–|83.1|
|ReCogDrive [24]|98.3|95.2|**99.5**|99.8|87.1|97.5|96.6|98.3|86.5|83.6|
|DiffusionDrive [28]|98.2|95.9|99.4|99.8|87.5|97.3|96.8|98.3|**87.7**|84.5|
|DriveVLA-W0 [22]|**99.0 **|**98.4**|99.3|99.9|87.0|**98.1**|93.2|97.9|58.9|86.5|
|DriveFine|**98.7**|97.3|98.8|99.8|88.2|97.8|**97.7**|**98.4**|84.7|87.1|
|DriveFine<sup>_†_</sup>|**98.7**|97.3|**99.5**|99.8|**88.7**|97.8|**97.7**|**98.4**|83.8|**89.7**|


**Table 3:** EPDMS results on the Navhard benchmark. * indicates values are copied from [36]; all other results are obtained from our own evaluations. 

|Method|Stage|NC_↑_|DAC_↑_|DDC_↑_|TLC_↑_|EP_↑_|TTC_↑_|LK_↑_HC_↑_EC_↑_|EPDMS_↑_|
|---|---|---|---|---|---|---|---|---|---|
|ReCogDrive [24]|S1<br>S2|97.1<br>78.2|80.2<br>69.3|98.4<br>83.9|**100**<br>98.2|83.6<br>86.6|95.3<br>73.9|93.6 97.6 76.0<br>44.1 96.4 72.0|68.9<br>37.8|
|DiffusionDrive* [28]|<sup>S1</sup><br>S2|96.8<br>80.1|86.0<br> **72.8**|98.8<br>84.4|99.3<br>**98.4**|84.0<br> 85.9|95.8<br> **76.6**|96.7 97.6 79.6<br> 46.4 96.3 **72.8**|66.7<br>40.5|
|DriveFine(Ours)|S1<br>S2|**97.6**<br>**82.1**|**90.0**<br>71.3|**99.1**<br>**84.8**|99.3<br>**98.4**|**84.9**<br>**88.1**|**96.7**<br>74.3|**97.3**<br>**97.6**<br>72.0<br>**47.2**<br>**96.8**<br>**72.8**|**74.4**<br>**41.0**|


In the RFT stage, The group size for generating expert rollouts is set to 10, each of trajectory is further optimized online by the optimizer 6 times. The model is trained for 1 epoch with a batch size of 16 and a learning rate of 1 _×_ 10<sup>_−_6</sup> . 

At inference, DriveFine executes 12 sampling steps followed by a single refining step, adhering to a confidence-prioritized and cosine schedule for decoding. 

### **4.2 Main Results** 

**Results of Navtest.** We first report the NAVSIM v1 results, evaluating PDMS on the navtest split, as shown in Tab. 1. DriveFine achieves state-of-the-art (SOTA) performance. In particular, compared with autoregressive token-based VLA models [29, 49], DriveFine achieves a 0.5% improvement, while being on par with diffusion-based planners [24]. When score-based reinforcement finetuning is applied (an additional scorer is trained), DriveFine further improves its performance to 91.9 PDMS, surpassing all existing VLA planners. 

We report the comparison results on NAVSIM-v2 in Tab. 2, which provides a more comprehensive evaluation of the overall model performance. For a fair comparison with prior works, we evaluate DriveFine using an earlier NAVSIM version, which contains a score computation bug that leads to systematically 

12 C. Dang et al. 

**Table 4:** Ablation results of core components of DriveFine. 

|ID|SFT|GRPO|Offline-RFT|Online-RFT|NC|DAC|TTC|Conf.|EP|**PDMS**|
|---|---|---|---|---|---|---|---|---|---|---|
|1|✓|✗|✗|✗|98.0|95.2|94.9|99.4|81.6|86.7|
|2|✓|✓|✗|✗|98.3|96.9|95.1|99.2|85.1|89.6+2.9|
|3|✓|✓|✓|✗|98.5|97.3|95.2|99.9|85.4|90.3+0.7|
|4|✓|✓|✓|✓|98.6|97.9|95.2|99.9|85.5|90.8+0.5|


underestimated overall scores. Despite this issue, DriveFine still achieves 86.7 EPDMS, outperforming DriveVLA-W0 [22] by 0.5 points. When evaluated with the bug-fixed NAVSIM version, DriveFine further reaches 89.7 EPDMS, thereby establishing a new state of the art. 

**Results of Navhard.** We further conduct experiments on the more challenging Navhard benchmark, which employs Gaussian splatting to generate scenarios beyond the training data distribution and adopts a two-stage evaluation protocol. The results are reported in Tab. 3. Notably, no additional training is applied in this setting. Under this fair evaluation protocol, DriveFine outperforms the diffusion-based methods [28, 31] on both stage metrics, with a particularly notable improvement of 5.5 points in Stage 1 EPDMS over ReCogDrive, further demonstrating its strong performance as well as the superior generalization capability of token-based VLAs. 

### **4.3 Ablation Studies** 

**Ablations of the core components.** Tab. 4 presents an ablation study on the core components of DriveFine. With LLaDA mimicking expert trajectories (SFT), the model achieves a PDMS of 86.7. GRPO reinforcement training increases PDMS to 89.6. Incorporating the refinement expert with offline reinforcement training further improves performance by 0.7 point, while online reinforcement training raises the model’s performance ceiling to 90.8. 

We observe that the refinement mechanism improves nearly all metrics, particularly DAC and Conf. Further visualization of trajectories before and after refinement (as shown in the Fig. 6) clearly demonstrates that the refinement expert can effectively correct anomalies when individual tokens lead to collisions or off-road events, which would otherwise result in complete trajectory failure. Additionally, it significantly mitigates fluctuations caused by noncausal decoding, enhancing overall trajectory smoothness. 

**Ablation study on the robustness of DriveFine.** We further evaluated the robustness of DriveFine. As shown in Tab. 5, after PDMS-oriented RFT, extended metrics such as LK, EC, and DDC remain stable or show slight improvements. Consequently, the increase in PDMS is accompanied by a synchronous 

DriveFine: Refining-Augmented ... 13 


**Fig. 6:** Qualitative visualization comparison between DriveFine and other SOTA methods. In the rightmost figure, the red and green lines denote the trajectories before and after refinement, respectively. 

**Table 5:** Performance comparison of differ- **Table 6:** Sensitivity the number of refineent models. ment blocks _n_ . 

|Model|EP_↑_LK_↑_EC_↑_<br>PDMS_↑_|EPMDS_↑_|n|0|1|2|4|6|8|
|---|---|---|---|---|---|---|---|---|---|
|DriveFine-SFT|86.8 97.9 83.3<br>86.7|86.8|Param(B)|8|8.25|8.5|9|9.5|10|
|+RFT(PDMS)|88.7 97.7 83.8<br>90.5+3.8|89.1+2.3|PDMS|89.6|90.0|90.4|90.8|90.8|90.7|


improvement in EPMDS. Compared with diffusion-based models in 7, DriveFine demonstrates a clear robustness advantage, further confirming the potential of token-based models. 

**Sensitivity analysis of the number of refinement blocks.** We evaluated the sensitivity of DriveFine to the number of refinement blocks, as summarized in Tab. 6. When _n_ = 0, i.e., without any refinement capability, the trajectories are derived from the generative expert. Remarkably, introducing just one refinement block (250M parameters) already improves trajectory quality (+0.4 PDMS). As the number of blocks increases, performance gradually improves, reaching the optimal level when 4 refinement blocks are injected. 

**Efficiency-Performance Trade-off Analysis.** We evaluate the impact of the number of diffusion steps _s_ on the efficiency–performance trade-off, comparing 

14 C. Dang et al. 

DriveFine with VLA models of similar scale, as shown in Fig. 7. As expected, inference latency increases roughly proportionally with _s_ . In general, a larger number of diffusion steps allows the model to “think” more thoroughly, resulting in better performance. 

However, we observe that with only 4 steps, DriveFine already achieves a PDMS of 90.47, comparable to ReCogDrive-8B [24], with an average latency of merely 207 ms, representing an optimal efficiency–performance balance. This further demonstrates the robustness of masked diffusion LLMs. In contrast, the InternVL model relies on token-by-token decoding, incurring much higher inference latency. Overall, these results indicate that the flexible decoding of diffusion-based lan- 


**Fig. 7:** PDMS-Latency trade-off 

guage models enables an effective balance between efficiency and performance, paving the way for more efficient planning paradigms. 

**Effect of Group Size.** As shown in Tab. 7, DriveFine is moderately sensitive to the GRPO group size. Even with a small group size _G_ = 2, it outperforms the SFT baseline by 1.7 PDMS. Increasing _G_ leads to a monotonic performance gain, with the best performance achieved at _G_ = 8. 

**Table 7:** Sensitivity of group size _G_ . 

|Group size _G_|0|2|4|6|8|10|
|---|---|---|---|---|---|---|
|EP_↑_|81.6|83.7|84.4|84.7|85.1|85.2|
|DAC_↑_|95.2|95.8|96.3|96.5|96.9|96.8|
|PDMS_↑_|86.7|88.4|89.1|89.4|89.6|89.6|


## **5 Conclusion** 

In this paper, we conduct a comprehensive analysis of the two dominant VLA planners for autonomous driving: diffusion-based and token-based paradigms, highlighting their respective strengths and limitations. We further explore leveraging masked diffusion LLMs as a potential solution to mitigate their shortcomings. Building on these insights, we propose DriveFine, which features a plugand-play block-MoE architecture combined with a hybrid reinforcement training strategy to inject refinement capabilities into token-based VLAs. We evaluate DriveFine on NAVSIMv1, NAVSIMv2, and the more challenging Navhard 

DriveFine: Refining-Augmented ... 15 

benchmarks, and demonstrate its effectiveness and robustness through extensive ablation studies and comparative analyses. We hope our findings and contributions will provide valuable insights for the community. 

## **References** 

1. Bai, S., Chen, K., Liu, X., Wang, J., Ge, W., Song, S., Dang, K., Wang, P., Wang, S., Tang, J., et al.: Qwen2. 5-vl technical report. arXiv preprint arXiv:2502.13923 (2025) 5 

2. Caesar, H., Kabzan, J., Tan, K.S., Fong, W.K., Wolff, E., Lang, A., Fletcher, L., Beijbom, O., Omari, S.: nuplan: A closed-loop ml-based planning benchmark for autonomous vehicles. arXiv preprint arXiv:2106.11810 (2021) 9 

3. Chen, S., Jiang, B., Gao, H., Liao, B., Xu, Q., Zhang, Q., Huang, C., Liu, W., Wang, X.: Vadv2: End-to-end vectorized autonomous driving via probabilistic planning. arXiv preprint arXiv:2402.13243 (2024) 1, 4 

4. Chen, X., Huang, L., Ma, T., Fang, R., Shi, S., Li, H.: Solve: Synergy of languagevision and end-to-end networks for autonomous driving. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 12068–12077 (2025) 5 

5. Chen, Z., Wu, J., Wang, W., Su, W., Chen, G., Xing, S., Zhong, M., Zhang, Q., Zhu, X., Lu, L., et al.: Internvl: Scaling up vision foundation models and aligning for generic visual-linguistic tasks. In: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. pp. 24185–24198 (2024) 3, 5 

6. Chitta, K., Prakash, A., Jaeger, B., Yu, Z., Renz, K., Geiger, A.: Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. IEEE transactions on pattern analysis and machine intelligence **45** (11), 12878–12895 (2022) 4, 10, 11 

7. Contributors, O.: Openscene: The largest up-to-date 3d occupancy prediction benchmark in autonomous driving. In: Proceedings of the Conference on Computer Vision and Pattern Recognition, Vancouver, Canada. pp. 18–22 (2023) 9 

8. Dang, C., Wang, J., Li, G., Hou, Z., You, Z., Ye, H., Ma, J., Chen, L., Wang, Y.: Sparseoccvla: Bridging occupancy and vision-language models via sparse queries for unified 4d scene understanding and planning. arXiv preprint arXiv:2601.06474 (2026) 5 

9. Dauner, D., Hallgarten, M., Li, T., Weng, X., Huang, Z., Yang, Z., Li, H., Gilitschenski, I., Ivanovic, B., Pavone, M., et al.: Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking. Advances in Neural Information Processing Systems **37** , 28706–28719 (2024) 2, 9 

10. Feng, R., Xi, N., Chu, D., Wang, R., Deng, Z., Wang, A., Lu, L., Wang, J., Huang, Y.: Artemis: Autoregressive end-to-end trajectory planning with mixture of experts for autonomous driving. arXiv preprint arXiv:2504.19580 (2025) 11 

11. Fu, H., Zhang, D., Zhao, Z., Cui, J., Liang, D., Zhang, C., Zhang, D., Xie, H., Wang, B., Bai, X.: Orion: A holistic end-to-end autonomous driving framework by vision-language instructed action generation. arXiv preprint arXiv:2503.19755 (2025) 5 

12. Hu, Y., Yang, J., Chen, L., Li, K., Sima, C., Zhu, X., Chai, S., Du, S., Lin, T., Wang, W., et al.: Planning-oriented autonomous driving. In: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. pp. 17853– 17862 (2023) 1, 4, 10 

- 16 C. Dang et al. 

13. Huang, Z., Tang, T., Chen, S., Lin, S., Jie, Z., Ma, L., Wang, G., Liang, X.: Making large language models better planners with reasoning-decision alignment. In: European Conference on Computer Vision. pp. 73–90. Springer (2024) 5 

14. Hwang, J.J., Xu, R., Lin, H., Hung, W.C., Ji, J., Choi, K., Huang, D., He, T., Covington, P., Sapp, B., et al.: Emma: End-to-end multimodal model for autonomous driving. arXiv preprint arXiv:2410.23262 (2024) 5 

15. Jiang, B., Chen, S., Xu, Q., Liao, B., Chen, J., Zhou, H., Zhang, Q., Liu, W., Huang, C., Wang, X.: Vad: Vectorized scene representation for efficient autonomous driving. In: Proceedings of the IEEE/CVF International Conference on Computer Vision. pp. 8340–8350 (2023) 1, 4 

16. Jiang, B., Chen, S., Zhang, Q., Liu, W., Wang, X.: Alphadrive: Unleashing the power of vlms in autonomous driving via reinforcement learning and reasoning. arXiv preprint arXiv:2503.07608 (2025) 5 

17. Kirby, E., Boulch, A., Xu, Y., Yin, Y., Puy, G., Zablocki, É., Bursuc, A., Gidaris, S., Marlet, R., Bartoccioni, F., et al.: Driving on registers. arXiv preprint arXiv:2601.05083 (2026) 5, 10 

18. Li, J., Wu, J., Hu, D., Huang, X., Sun, B., Hao, Z., Lang, X., Zhu, X., Zhang, L.: Sgdrive: Scene-to-goal hierarchical world cognition for autonomous driving. arXiv preprint arXiv:2601.05640 (2026) 2, 5 

19. Li, P., Zheng, Y., Wang, Y., Wang, H., Zhao, H., Liu, J., Zhan, X., Zhan, K., Lang, X.: Discrete diffusion for reflective vision-language-action models in autonomous driving. arXiv preprint arXiv:2509.20109 (2025) 3, 5 

20. Li, S., Kallidromitis, K., Bansal, H., Gokul, A., Kato, Y., Kozuka, K., Kuen, J., Lin, Z., Chang, K.W., Grover, A.: Lavida: A large diffusion language model for multimodal understanding. arXiv preprint arXiv:2505.16839 (2025) 3 

21. Li, Y., Fan, L., He, J., Wang, Y., Chen, Y., Zhang, Z., Tan, T.: Enhancing end-toend autonomous driving with latent world model. arXiv preprint arXiv:2406.08481 (2024) 10 

22. Li, Y., Shang, S., Liu, W., Zhan, B., Wang, H., Wang, Y., Chen, Y., Wang, X., An, Y., Tang, C., et al.: Drivevla-w0: World models amplify data scaling law in autonomous driving. arXiv preprint arXiv:2510.12796 (2025) 10, 11, 12 

23. Li, Y., Wang, Y., Liu, Y., He, J., Fan, L., Zhang, Z.: End-to-end driving with online trajectory evaluation via bev world model. arXiv preprint arXiv:2504.01941 (2025) 10 

24. Li, Y., Xiong, K., Guo, X., Li, F., Yan, S., Xu, G., Zhou, L., Chen, L., Sun, H., Wang, B., et al.: Recogdrive: A reinforced cognitive framework for end-to-end autonomous driving. arXiv preprint arXiv:2506.08052 (2025) 2, 3, 5, 10, 11, 14 

25. Li, Z., Li, K., Wang, S., Lan, S., Yu, Z., Ji, Y., Li, Z., Zhu, Z., Kautz, J., Wu, Z., et al.: Hydra-mdp: End-to-end multimodal planning with multi-target hydradistillation. arXiv preprint arXiv:2406.06978 (2024) 1, 5, 10 

26. Li, Z., Yao, W., Wang, Z., Sun, X., Chen, J., Chang, N., Shen, M., Wu, Z., Lan, S., Alvarez, J.M.: Generalized trajectory scoring for end-to-end multimodal planning. arXiv preprint arXiv:2506.06664 (2025) 5, 10 

27. Li, Z., Yu, Z., Lan, S., Li, J., Kautz, J., Lu, T., Alvarez, J.M.: Is ego status all you need for open-loop end-to-end autonomous driving? In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 14864– 14873 (2024) 11 

28. Liao, B., Chen, S., Yin, H., Jiang, B., Wang, C., Yan, S., Zhang, X., Li, X., Zhang, Y., Zhang, Q., et al.: Diffusiondrive: Truncated diffusion model for end-to-end autonomous driving. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 12037–12047 (2025) 2, 4, 10, 11, 12 

DriveFine: Refining-Augmented ... 17 

29. Luo, Y., Li, F., Xu, S., Lai, Z., Yang, L., Chen, Q., Luo, Z., Xie, Z., Jiang, S., Liu, J., et al.: Adathinkdrive: Adaptive thinking via reinforcement learning for autonomous driving. arXiv preprint arXiv:2509.13769 (2025) 2, 3, 5, 10, 11 

30. Mao, J., Qian, Y., Ye, J., Zhao, H., Wang, Y.: Gpt-driver: Learning to drive with gpt. arXiv preprint arXiv:2310.01415 (2023) 5 

31. Nie, M., Peng, R., Wang, C., Cai, X., Han, J., Xu, H., Zhang, L.: Reason2drive: Towards interpretable and chain-based reasoning for autonomous driving. In: European Conference on Computer Vision. pp. 292–308. Springer (2024) 5, 12 

32. Nie, S., Zhu, F., You, Z., Zhang, X., Ou, J., Hu, J., Zhou, J., Lin, Y., Wen, J.R., Li, C.: Large language diffusion models. arXiv preprint arXiv:2502.09992 (2025) 3, 10 

33. Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang, H., Zhang, M., Li, Y., Wu, Y., et al.: Deepseekmath: Pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300 (2024) 5 

34. Sun, W., Lin, X., Shi, Y., Zhang, C., Wu, H., Zheng, S.: Sparsedrive: End-to-end autonomous driving via sparse scene representation. In: 2025 IEEE International Conference on Robotics and Automation (ICRA). pp. 8795–8801. IEEE (2025) 4 

35. Tan, T., Zheng, Y., Liang, R., Wang, Z., Zheng, K., Zheng, J., Li, J., Zhan, X., Liu, J.: Flow matching-based autonomous driving planning with advanced interactive behavior modeling. arXiv preprint arXiv:2510.11083 (2025) 4 

36. Tian, H., Li, T., Liu, H., Yang, J., Qiu, Y., Li, G., Wang, J., Gao, Y., Zhang, Z., Wang, L., et al.: Simscale: Learning to drive via real-world simulation at scale. arXiv preprint arXiv:2511.23369 (2025) 11 

37. Tian, X., Gu, J., Li, B., Liu, Y., Wang, Y., Zhao, Z., Zhan, K., Jia, P., Lang, X., Zhao, H.: Drivevlm: The convergence of autonomous driving and large visionlanguage models. arXiv preprint arXiv:2402.12289 (2024) 5 

38. Tschannen, M., Gritsenko, A., Wang, X., Naeem, M.F., Alabdulmohsin, I., Parthasarathy, N., Evans, T., Beyer, L., Xia, Y., Mustafa, B., et al.: Siglip 2: Multilingual vision-language encoders with improved semantic understanding, localization, and dense features. arXiv preprint arXiv:2502.14786 (2025) 5, 10 

39. Wang, S., Yu, Z., Jiang, X., Lan, S., Shi, M., Chang, N., Kautz, J., Li, Y., Alvarez, J.M.: Omnidrive: A holistic vision-language dataset for autonomous driving with counterfactual reasoning. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 22442–22452 (2025) 5 

40. Wang, T., Xie, E., Chu, R., Li, Z., Luo, P.: Drivecot: Integrating chain-of-thought reasoning with end-to-end driving. arXiv preprint arXiv:2403.16996 (2024) 5 

41. Wang, Y., Yang, L., Li, B., Tian, Y., Shen, K., Wang, M.: Revolutionizing reinforcement learning framework for diffusion large language models. arXiv preprint arXiv:2509.06949 (2025) 7 

42. Xing, Z., Zhang, X., Hu, Y., Jiang, B., He, T., Zhang, Q., Long, X., Yin, W.: Goalflow: Goal-driven flow matching for multimodal trajectories generation in endto-end autonomous driving. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 1602–1611 (2025) 4 

43. Xu, M., Cui, J., Cai, F., Shang, H., Zhu, Z., Luan, S., Xu, Y., Zhang, N., Li, Y., Cai, J., et al.: Wam-diff: A masked diffusion vla framework with moe and online reinforcement learning for autonomous driving. arXiv preprint arXiv:2512.11872 (2025) 3, 5 

44. Yao, W., Li, Z., Lan, S., Wang, Z., Sun, X., Alvarez, J.M., Wu, Z.: Drivesuprim: Towards precise trajectory selection for end-to-end planning. arXiv preprint arXiv:2506.06659 (2025) 11 

18 C. Dang et al. 

45. Zhao, S., Gupta, D., Zheng, Q., Grover, A.: d1: Scaling reasoning in diffusion large language models via reinforcement learning. arXiv preprint arXiv:2504.12216 (2025) 8 

46. Zheng, W., Song, R., Guo, X., Zhang, C., Chen, L.: Genad: Generative end-to-end autonomous driving. In: European Conference on Computer Vision. pp. 87–104. Springer (2024) 4 

47. Zheng, Y., Liang, R., Zheng, K., Zheng, J., Mao, L., Li, J., Gu, W., Ai, R., Li, S.E., Zhan, X., et al.: Diffusion-based planning for autonomous driving with flexible guidance. arXiv preprint arXiv:2501.15564 (2025) 4 

48. Zhou, X., Han, X., Yang, F., Ma, Y., Tresp, V., Knoll, A.: Opendrivevla: Towards end-to-end autonomous driving with large vision language action model. arXiv preprint arXiv:2503.23463 (2025) 2, 5 

49. Zhou, Z., Cai, T., Zhao, S.Z., Zhang, Y., Huang, Z., Zhou, B., Ma, J.: Autovla: A vision-language-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. arXiv preprint arXiv:2506.13757 (2025) 2, 3, 5, 10, 11 

50. Zhu, R., Zhao, J., Zhang, D., Wang, G., Chen, X., Zhang, S., Gong, J., Zhou, Q., Zhang, W., Wang, N., et al.: Sparsead: Sparse query-centric paradigm for efficient end-to-end autonomous driving. IEEE Transactions on Artificial Intelligence (2025) 1 

51. Zou, J., Chen, S., Liao, B., Zheng, Z., Song, Y., Zhang, L., Zhang, Q., Liu, W., Wang, X.: Diffusiondrivev2: Reinforcement learning-constrained truncated diffusion modeling in end-to-end autonomous driving. arXiv preprint arXiv:2512.07745 (2025) 2, 3, 5 

