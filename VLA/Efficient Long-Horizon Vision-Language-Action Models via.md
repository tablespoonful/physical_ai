---
title: "Efficient Long-Horizon Vision-Language-Action Models via Static-Dynamic Disentanglement"
date: "2026-02-03"
authors: "Weikang Qiu; Huashuo Lei; Tinglin Huang; Rex Ying"
url: https://arxiv.org/abs/2602.03983
pdf: https://arxiv.org/pdf/2602.03983
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.03983)** / [論文ページ](https://arxiv.org/abs/2602.03983)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Static-Dynamic Disentanglement for Efficient Multi-Frame Vision-Language-Action Models** 

**Weikang Qiu**<sup>_∗_</sup> **Huashuo Lei**<sup>_∗_</sup> Yale University The Hong Kong University of Science and Technology (Guangzhou) 

**Tinglin Huang** Yale University 

**Rex Ying** 

Yale University 

## **Abstract** 

Vision-Language-Action (VLA) models have recently emerged as a promising paradigm for generalist robotic control. Built upon vision–language model (VLM) architectures, VLAs predict actions conditioned on visual observations and language instructions, achieving strong performance and generalization across tasks. However, VLAs face two major challenges: a limited context window for input frames and inefficient inference due to the quadratic attention complexity and large parameter counts. To this end, we propose DySta, a framework that disentangles visual inputs into multi-level static and dynamic tokens, which enables (1) retaining a single copy of static tokens across frames to significantly reduce context length, and (2) reusing the key–value (KV) cache of static tokens through a lightweight recache gate that updates only when necessary. This design enables efficient multi-frame integration and efficient inference. In addition, we introduce a new benchmark that more effectively evaluates the multi-frame integration ability of VLAs. Experiments show that DySta improves multi-frame integration by 24.5% across metrics on our benchmark and 23.3% in absolute success rate on real-world memory-dependent tasks, while accelerating inference by 2.0× (with +2.3% success rate) on simulation benchmarks and 2.2× (with +10.6% success rate) on real-world general tasks. 

## **1 Introduction** 

Vision-Language-Action (VLA) models [19, 17, 36, 18, 65, 62, 3, 11] have recently emerged as a powerful paradigm for generalist robotic control. Trained on large-scale heterogeneous datasets such as Open-X-Embodiment [53], which aggregate expert demonstrations across diverse robotic tasks, state-of-the-art VLA models exhibit impressive task performance. However, they are typically built on top of large vision–language models [23, 16, 2, 47], whose large parameter counts and quadratic-complexity contextual processing [52] translate into two central deployment bottlenecks: (1) a constrained context budget that limits how many past observations can be ingested, and (2) high per-step inference latency that hinders real-time control. These manifest as the two challenges of _multi-frame integration_ and _efficient inference_ elaborated below and illustrated in Figure 1. 

**Multi-frame Integration** . Most current VLAs operate in a memoryless manner [17, 19, 36], taking only the current observation as input. As a result, they struggle with tasks that require temporal dependency or memory tracking. For instance, when instructed to press a button, a VLA must remember whether the button has already been pressed; otherwise, it may repeat the same action 

> _∗_ Equal contribution. 

Preprint. 

indefinitely. A straightforward solution is to include previous observations in the model input. However, VLA’s vision backbones typically produce hundreds of visual tokens per image, leading to prohibitively long contexts when multiple frames are concatenated for the transformer-based architecture with quadratic complexity in sequence length. Existing methods often rely on indirect or compressed representations [14, 50], or expose multiple frames to the decoder head only [44], which either risks significant information loss or bypasses the language model’s ability to jointly reason over multiple frames. 

**Efficient Inference** . Due to their large model sizes, VLAs incur long latency for each forward pass. In real-world settings, however, robotic systems are often expected to respond promptly—for example, a household assistant should complete tasks as quickly as possible, while safety-critical scenarios such as spill containment or fire response may require near-instantaneous reactions. Moreover, recent post-training approaches for VLAs [46, 26], rely on reinforcement learning [48, 41, 43] and require extensive rollouts during training, making inference speed a key bottleneck. While existing work has explored improving VLA efficiency through generic techniques for general machine learning models, such as quantization, token pruning, or layer pruning [56, 59, 58, 17], these approaches do not leverage the intrinsic characteristics of VLA tasks. Recent works [56, 22, 49] exploit temporal redundancy by reusing computations across consecutive frames, via KV-cache reuse or action reuse. Nonetheless, these techniques rely on heuristic, non-learnable criteria and often assume that visual similarity in pixel space indicates the temporal-consistency of their latent representations—an assumption that is invalid in transformer-based vision and language backbones, as illustrated in Figure 2. 

To address these challenges, we propose DySta. We focus on a broad and practically important class of robotic scenarios—such as tabletop manipulation, household chores, and warehouse picking—where the agent operates within relatively stable scenes or undergoes discrete, infrequent scene transitions. In this regime, much of the visual information in a scene remains static or changes slowly over time: the background, objects remaining still, and even moved objects whose visual appearances stay largely invariant. Building on this observation, we explicitly disentangle visual tokens into dynamic tokens and multi-level static tokens with different temporal persistence. This design yields two 


Figure 1: Our model solves two main challenges in existing VLAs with the proposed static-dynamic disentanglement. 1) By keeping one copy of static tokens across all timesteps, our model is able to squash observations of multiple steps to the model’s context; 2) By moving static tokens in front of all dynamic tokens, our model could reuse the KV-cache of previous timesteps during rollouts. 

key benefits. First, instead of conditioning on a single image as in prior work, our model can ingest multi-step observations while maintaining a compact context: static tokens are included only once in the input sequence across timesteps, while only dynamic tokens from multiple steps are concatenated over time. This substantially reduces the effective context length and enables multi-frame integration. Second, our method improves the inference efficiency by reusing key–value (KV) caches associated with static tokens from previous steps. We also introduce a recache gate module that determines whether previously cached static tokens should be reused or recomputed, which further improves performance while minimizing the inference latency. 

In addition, we observe that existing simulation benchmarks largely fail to assess a VLA’s multi-frame integration capabilities. For example, temporally dependent tasks such as placing objects into a basket do not require remembering past trajectories. To address this gap, we design a new simulation benchmark inspired by principles of human episodic memory, which provides a more effective evaluation of temporal reasoning and memory usage than prior benchmarks [21, 20]. 

To evaluate multi-frame integration, we assess our model on the proposed benchmark. Our method achieves a 24 _._ 5% improvement across all metrics and 23 _._ 3% in absolute success rate on real-world 

2 

experiments. To evaluate inference efficiency, we benchmark our approach on public simulation benchmarks [21, 20] and real-world experiments. On SimplerEnv [20], DySta improves the success rate by 3 _._ 9% over the strongest baseline while achieving a 2 _._ 26 _×_ inference speedup. In real-world experiments, DySta improves the average success rate by 10 _._ 6% over the base model and achieves a 2 _._ 21 _×_ speedup. These results demonstrate that DySta not only enhances multi-frame integration, but also substantially reduces inference latency. In summary, our contributions are as follows: 

- We propose DySta, which enables multi-frame integration and efficient inference by disentangling image tokens to dynamic tokens and multi-level static tokens with different temporal persistence. 

- We introduce a trainable recache gate that adaptively determines when to refresh the cache or reuse previously cached representations, further improving the performance while minimizing the inference latency. 

- We introduce LIBERO-Memory, a new benchmark that more effectively evaluates a VLA’s multiframe integration ability by temporally dependent tasks. 

## **2 Related Works** 

**Vision-Language-Action Models** Vision-language models (VLMs) [23, 55] have demonstrated strong performance in image-related and cross-modal tasks. Leveraging these capabilities, visionlanguage-action (VLA) models further finetune VLMs on large-scale robotic datasets [53, 21], which usually consist of extensive human demonstrations. At each timestep, VLAs [3, 11, 17, 19, 36] usually take the current environment observation (image) and a language instruction as inputs, and are trained to output actions of the next step. Although they have demonstrated high performance on certain benchmarks, due to the large parameters, they are 1) inefficient in rollout and 2) unable to incorporate historical frames in the context. In contrast, our model, by disentangling the static and dynamic components, is efficient in inference by leveraging the KV-cache of static components, and is able to incorporate a long history for temporally dependent tasks. 


**_Not_** static anymore **VLA Acceleration** Methods to improve VLA’s after attentions **_Always_** static efficiency usually focus on general quantization or pruning methods.explores quantizationFor example, [techniques 17applied, 38, 35to] Layer N LLM Layer N LLM VLAs. [45, 58, 60, 59] explored pruning unimLayer 1 Layer 1 portant tokens and layers according to some heuristics. Although reducing the computational Vision Encoder Vision Encoder complexity of VLAs, these methods just migrate acceleration methods from existing general machine learning models, thus totally ignoring the unique characteristics of VLAs. Different from **Existing Methods Ours** these methods, recent works [56, 22, 49] explore **(e.g., VLA-cache)** temporal redundancy in decision making: conFigure 2: Some of the existing methods [56, 22] secutive frames share temporal correlation, enthat exploit to reuse information in previous frames abling avoiding recomputation of some compoignore the problem that the static patches will be nents by, for example, leveraging the KV-cache affected by attentions even if they are identical in of previous steps. However, these methods rely the original pixel space. on non-learnable heuristics to recache or simply reuse the previous action, which may suffer from suboptimal performance. Notably, some of these methods [56, 22] implicitly assume that visual similarity in pixel space implies invariance in the latent representations produced by the vision encoder and LLM—an assumption that does not generally hold in transformer-based architectures, as illustrated in Figure 2 and elaborated in Appendix G. 

**Multi-Frame VLAs** Existing approaches to incorporating historical frames in VLAs typically provide the model with only indirect or compressed access to temporal information. For example, Jang et al. [14] uses a non-learnable pooling operation to condense historical frames into a fixed number of tokens. Liu et al. [22], Torne et al. [50] incorporate historical frames into the current input via patch-wise mixing. TraceVLA [61] overlays visual traces of keypoints onto the current observation to indicate object trajectories. In addition, MemoryVLA [44] exposes the LLM backbone to only a single frame at each timestep and delegates multi-frame reasoning to a lightweight decoding module, which limits the model’s capacity for joint temporal decision-making. In contrast to these methods, 

3 

our approach allows the LLM backbone to directly reason over multiple frames without information loss, by explicitly disentangling static and dynamic components and avoiding redundant involvement of temporally persistent visual information. 

## **3 Method** 

In this section, we first present the problem formulation. We then introduce the architecture of our model, followed by the training objectives that enable static–dynamic disentanglement and the recaching mechanism. Next, we provide a computational complexity analysis and derive the theoretical acceleration and context-length improvements. Finally, we introduce the benchmark for evaluating multi-frame integration. 

**Problem Formulation** Given a timestep _t_ , the corresponding observation of the environment is denoted by **_X_** _t_ . A VLA _π_ predicts actions of the following steps based on previous _T_ observations and a language instruction _I_ . 


where **_a_** _t_ is the action at the _t_ step. Most existing VLAs usually consider _T_ = 0 due to the limited due to the limited context length of large language models. 

### **3.1 Model Architecture** 

**Static-dynamic disentanglement** Standard Recache VLA vision backbones typically encode the <mark>L2 static</mark> Gate image **_X_** _t_ into _N_ image tokens **_Z_** _t_ = Cached Static **_z_** _t,_ 1 _,_ **_z_** _t,_ 2 _, · · · ,_ **_z_** _t,N_ as inputs of the VLA’s Tokens <mark>L1 static L2 static</mark> LLM backbone _π_ LLM. Such a design implicitly <mark>static</mark> assumes that all visual tokens must be recomDisentanglement puted and reprocessed at every timestep. However, real-world environments exhibit strong temporal redundancy: many visual attributes remain unchanged across time, while only a subFigure 3: Model architecture overview. We illusset varies dynamically. Moreover, static infortrate the design using two levels of static cache. mation exists at different temporal scales. For each level, a recache gate determines whether the example, global scene layout or background cached static tokens should be reused or refreshed. structure may persist for long horizons, whereas If the L1 cache is refreshed, the L2 cache is also object-level appearance may change more freforcibly refreshed. quently due to occlusion or interaction. To reflect this structure, we disentangle visual tokens into multi-level static tokens and dynamic tokens. 

Figure 3: Model architecture overview. We illustrate the design using two levels of static cache. At each level, a recache gate determines whether the cached static tokens should be reused or refreshed. If the L1 cache is refreshed, the L2 cache is also forcibly refreshed. 


where **_Z_**<sup>_s_</sup> _t_<sup>_l_denotes static tokens at level</sup><sup>_l_, and</sup><sup>**_Z_**</sup><sup>_d_</sup> _t_<sup>are dynamic tokens.The ratio between static and</sup> dynamic tokens is set as a predefined hyperparameter. Under this design, dynamic tokens capture timestep-specific information and are recomputed at every timestep, whereas static tokens at each level are selectively reused through a learned caching mechanism, described later. 

**Temporal dependency modeling** Most VLAs [17, 19, 36] are only able to process the current observation ( _T_ = 0), 


where _π_ LLM is the LLM backbone of the VLA. With successful static-dynamic disentanglement, we only need to keep _one copy_ of the static tokens within a period and construct the input from multiple observations as 


4 

This formulation enables the model to leverage longer temporal context without duplicating static information, effectively alleviating context window bottlenecks while preserving relevant visual cues. 

**Learning when to recache** A key challenge is deciding when cached static tokens should be refreshed. Naively recomputing static tokens at every timestep negates any computational benefit, while overly aggressive reuse of static tokens risks stale representations. To address this, we introduce a learned recache gate at each static level _l_ , 


which predicts the probability that static tokens should be recomputed given the current observation and a cached reference from ∆ timesteps earlier. During training, we use the Gumbel-softmax trick [12, 29] to allow end-to-end differentiable binary decisions. At inference time, static tokens are refreshed if the probability is greater than a threshold, i.e., _gl > δl_ ; otherwise, the previous cache is reused. It is also worth noting that if the higher-level cache (e.g., L1) should be refreshed, the lower-level cache (e.g., L2) should also be refreshed during both training and inference. Additional details of the architecture of the recache gate could be found in Appendix B. 

**Computational and Acceleration Analysis** Let _N_ be the total number of tokens per observation, _r_ the fraction of cached static tokens, and _T_ the number of observations in the context. Our staticdynamic disentanglement reduces the effective context length from _NT_ to _NT − rN_ ( _T −_ 1), and reduces the FLOPs of the LLM backbone by a factor of 1 _− r_ . The recache gate adds only negligible overhead ( _≈_ 1 _._ 27%). A full derivation and wall-clock latency breakdown are provided in Appendix F. 

### **3.2 Training Objective** 


Besides the standard task loss of the underlying VLA base model _L_ task, we introduce two additional training objectives. The first promotes temporally persistent static tokens, and the second trains the cache gate that adaptively determines when cached representations should be refreshed. 

**Learning static tokens** As illustrated in Figure 4, to ensure that static tokens can be safely and effectively reused across time, they must remain stable over a temporal window while still encoding task-relevant information. To encourage this property, we apply a contrastive term to the static tokens. Specifically, observations from different timesteps within the same trajectory are treated as positive pairs, while observations from different trajectories are treated as negative pairs. We employ InfoNCE loss [34]34]] _L_<sup>_l_</sup> InfoNCE<sup>to perform contrastive learning for static tokens at level</sup><sup>_l_.</sup> 

trajectory are treated as positive pairs, while observations from different Figure 4: Contrastive We employ InfoNCE loss [34]34]] loss used to train static<sup>to perform contrastive learning for static tokens at level</sup><sup>_l_.</sup> tokens to be temporally persistent. ObserIf the recache gate is trained only through vations from the same recompute static tokens at every timestep, trajectory form positive computational benefit. To discourage this trivial pairs, while observasolution, we add a regularization term that biases the gate toward reuse tions from different trajectories form negative pairs. _L_ gate = _−p_ ∆ log _g −_ (1 _− p_ ∆) log(1 _− g_ ) _,_ (6) 

**Training the recache gate** If the recache gate is trained only through task supervision, it tends to recompute static tokens at every timestep, which eliminates any computational benefit. To discourage this trivial solution, we add a regularization term that biases the gate toward reuse when observations are close in time. 

where _p_ ∆ = 1 _− e_<sup>_−λ_∆</sup> is a predefined prior which allows the use of current observation only when ∆ is large. The recache gate learns to adaptively refresh static tokens only when necessary, balancing computational efficiency and model performance. Note that since _λ_ and the recache threshold _δl_ jointly determine the recaching frequency, we fix _λ_ and expose only _δl_ as the operating-point knob. The full training objective is 


where _αl_ and _β_ weight the auxiliary regularization terms. A sensitivity analysis for these coefficients is provided in Appendix I.1. 

5 


Figure 5: An example of the procedure of the proposed benchmark. 

### **3.3 LIBERO-Memory Benchmark** 

Existing VLA simulation benchmarks [21, 20] are designed for memoryless tasks, which do not require multi-frame integration, and the current observation alone is theoretically sufficient to predict the next action. For example, in a task with the goal “put X in the basket”, [21] the agent can act optimally without retaining information from previous frames. As a result, it is unclear whether the reported performance of existing models for modeling temporal dependency [14, 44] truly stems from improved temporal modeling or from other artifacts. This highlights the absence of a strong and fair benchmark for temporal dependency modeling and multi-frame integration. 

To address this gap, we introduce a new simulation benchmark designed to test multi-frame integration explicitly. Our benchmark includes tasks that require a robot to retain and utilize information from past observations, thereby directly evaluating a model’s temporal dependency modeling ability. 

Following the setup of LIBERO, the robot operates in a tabletop environment containing three objects: two visually distinct cans and a stove. As illustrated in Figure 5, each episode consists of three tasks which reflects the structure of episodic memory [51, 6]. 

**Tasks** Each trial consists of three subtasks, each intentionally designed to require the model to retain and reason over information from previous observations at different aspects: 1) Grasp one of the cans, as specified by the instruction, and place it on the stove to heat. 2) After a period of time (given in the instructions), remove the can from the stove and return it to its original location. 3) Once the position of the first can has been restored, grasp the remaining can and place it on the stove. 

This task design requires the model to retain _episodic memory_ , integrating information about what happened, where it occurred, and when it took place [51, 6]. First, the robot must remember the initial spatial layout in order to return the first can to its original position (where). Second, it must track the elapsed time since the can was placed on the stove to determine when to remove it (when). Third, it must remember which can has already been heated in order to correctly select the remaining one for the final step (what). 

These requirements prevent the task from being solved using only the current observation or a short observation history. We use Robosuite [68] as the simulation framework to produce the dataset. The layout and the oracle demonstrations are programmatically generated. More details can be found in Appendix C. 

## **4 Experiments** 

In this section, we evaluate the model’s inference efficiency as well as its multi-frame integration ability. We further present ablation studies of the key components of our method and analyze the model’s behavior through attention-map visualizations. 

### **4.1 Acceleration** 

In this study, we validate our method’s performance under acceleration by enabling KV caching of static components. 

**Baselines** For baselines, we compare to those that also adopt temporal information reuse. _FlashVLA_ [49] simply reuses the previous action based on a heuristic criterion. _TTF-VLA_ [22] and _VLA-cache_ [56] identify reusable visual patches using hand-designed heuristics and cache the corresponding embeddings from previous steps; however, these cached patches are not guaranteed to remain static 

6 

Table 1: Results on the SimplerEnv benchmark. Task suites follow the setting of Qu et al. [36]. All baselines and our method are applied to the same VLA base model (i.e., CogACT [19]). 

||Vi|sual Mat|ching|Varia|nt Aggr|egation||Acceleratio|n|
|---|---|---|---|---|---|---|---|---|---|
|Method|Pick<br>Can|Move<br>Near|Drawer|Pick<br>Can|Move<br>Near|Drawer|FLOPs|Latency<br>(ms)|Speedup|
|CogACT [19]|91_._3|85_._0|71_._8|89_._6|80_._8|28_._3|100%|1360|1_._00_×_|
|+ FlashVLA [49]|80_._0|57_._1|73_._6|82_._5|60_._8|28_._6|83_._4%|1024|1_._33_×_|
|+ TTF [22]|89_._3|71_._3|58_._4|88_._0|62_._7|34_._0|86_._5%|1051|1_._29_×_|
|+ VLA-Cache [56]|92_._0|83_._3|70_._5|91_._7|79_._3|32_._5|80_._1%|985|1_._38_×_|
|+ DySta (Ours)|**92**_._**7**|**88**_._**8**|**75**_._**0**|**92**_._**4**|**81**_._**0**|**38**_._**9**|**43**_._**4**%|**601**|**2**_._**26**_×_|


Table 2: Results on the LIBERO benchmark. Policy inputs: third-person image, language instruction. All baselines and our method are applied to the same VLA base model (i.e., OpenVLA-OFT [18]). 

|Models|Spatial|Object|Goal|Long|Average|FLOPs|Latency (ms)|Speedup|
|---|---|---|---|---|---|---|---|---|
|OpenVLA-OFT [18]|96_._2|**98**_._**3**|**96**_._**2**|90_._7|95_._4|100_._0%|741|1_._00_×_|
|+ FlashVLA [49]|71_._8|90_._0|79_._2|78_._8|80_._0|88_._7%|657|1_._13_×_|
|+ TTF [22]|95_._8|94_._2|93_._6|86_._0|92_._4|75_._0%|575|1_._29_×_|
|+ VLA-Cache [56]|95_._6|92_._8|94_._0|89_._6|93_._0|85_._5%|652|1_._14_×_|
|+ DySta (Ours)|**97**_._**8**|97_._6|**96**_._**2**|**92**_._**4**|**96**_._**0**|**63**_._**4**%|**437**|**1**_._**70**_×_|


in the hidden representation space. All methods are based on the same VLA base model (i.e., CogACT [19]), with all other necessary variables controlled consistently. 

**Simulation benchmark** We use SimplerEnv [20] and LIBERO [21] task suite to evaluate the performance and acceleration. Kim et al. [18] offers two settings for LIBERO, one using only a thirdperson image and a language instruction as inputs, and another that additionally includes an extra camera view and proprioceptive state. We adopt the former setting, as it offers broader applicability and aligns more closely with standard VLA deployment scenarios. For the LIBERO benchmark, we finetune the model to the corresponding downstream datasets. For the SimplerEnv benchmark, we use Open X-Embodiment (OXE) [53] as the training dataset. All settings are consistent with the corresponding original base model. Dataset statistics could be found in Appendix A. 

**Real-World benchmark** We evaluate DySta with Cobot Magic robots on 7 tasks across 3 categories, each with 20 trials. This evaluation scale is consistent with prior work [44, 19]. Models are finetuned on each task. More details could be found in Appendix A.2. 

**Evaluation** The performance is measured by success rate, and acceleration is measured by the FLOPs reduction rate and the inference latency. 

**Implementation details** We use two levels of static cache. L1 static cache consists of 133 (52%) tokens and L2 static cache consists of 107 (42%) tokens, resulting in 16 dynamic tokens. The sensitivity analysis of the static ratio is in Appendix I.2. FLOPs are measured by open-source tools<sup>2</sup> . Additional details, including the recaching threshold _δl_ , the resulting average recaching intervals and the latency distribution when rollout, can be found in Appendix D and Appendix H. 

**Results** Table 1 and Table 2 summarize the performance and the acceleration results. Table 3 summarizes the results on the real-world benchmark. Across tables, we show that our method achieves improved or comparable performance across benchmarks with substantial speedup. Notably, on the SimplerEnv benchmark, our method improves the base model by 4 _._ 9%, and outperforms the best baseline by 3 _._ 9% and achieves 2 _._ 26 _×_ acceleration. On the real-world benchmark, our model improves the base model by 10 _._ 6% and achieves 2 _._ 21 _×_ acceleration. 

### **4.2 Multi-Frame Integration for Temporal-dependency Modeling** 

**Baselines** We consider the following baselines: _OpenVLA-OFT_<sup>_†_</sup> incorporates full image tokens from historical observations. Since this baseline incurs a prohibitively large context length compared with standard models, we allocate the maximum available resources and tune it for the best achievable 

> 2 `https://github.com/MrYxJ/calculate-flops.pytorch` 

7 

Table 3: Success rate (%) on real-world experiments with the Cobot Magic robot. All baselines and our method are applied to the same VLA base model (i.e., OpenVLA-OFT [18]). 

|Method||Pick-an<br>|d-Place<br>||Pou<br>|ring<br>|Container<br>|Acce|leration M<br>|etrics|
|---|---|---|---|---|---|---|---|---|---|---|
||Corn<br>_→_Pot|Corn<br>_→_Plate|Bread<br>_→_Pan|Carrot<br>Transfer|Pour<br>Coke|Pour<br>Bottle|Open<br>Drawer|FLOPs|Latency<br>(ms)|Speedup|
|OpenVLA-OFT|55|70|**55**|65|60|35|**35**|100_._0%|1089|1_._00_×_|
|+ FlashVLA|35|55|30|50|55|30|15|62_._5%|791|1_._30_×_|
|+ TTF|35|70|30|55|55|40|15|98_._6%|1077|1_._01_×_|
|+ VLA-Cache|60|65|35|50|45|40|30|74_._0%|836|1_._27_×_|
|+ DySta (Ours)|**65**|**80**|50|**70**|**60**|**50**|**35**|**30**_._**5**%|**493**|**2**_._**21**_×_|


performance. _TTF-VLA_ [22] mixes the current observation with past observations in a patch-wise manner. _TraceVLA_ [61] visualizes the trajectories of active points by overlaying them onto the image using distinct colors, referred to as visual traces. _MemoryVLA_ [44] feeds the LLM backbone with images from each timestep independently and extracts a representation for each; only the multitimestep representations are provided to the decoder. _ContextVLA_ [14] pools historical observations into a fixed number of tokens and prepends them to the image tokens of the current observation. All methods are applied to the same VLA base model (i.e., OpenVLA-OFT [18]), with all other necessary variables controlled consistently. 

**Simulation benchmark and evaluation** We adopt the proposed LIBERO-memory benchmark to evaluate multi-frame integration by memory-dependent tasks, whose designs are inspired by the notion of episodic memory. The benchmark comprises three objectives. (1) _(where) Position Reset._ After heating the first can, the robot is required to remember its original position and return it to the position. Performance is measured by success rate, where an episode is considered successful if the positional error is below a threshold. (2) _(when) Doneness._ The model must track the elapsed heating time and remove the can at the appropriate moment. Given a target heating duration specified in the instruction, we measure the absolute difference (in seconds) between the actual and desired heating times, capturing overcooking or undercooking. (3) _(what) On-Stove._ After heating and resetting the first can, the robot is required to remember which can has been cooked and place the second can on the stove for heating. We report the success rate of placing the second can on the stove. 

**Real-world benchmark** We evaluate DySta with Cobot Magic robots on 3 tasks, each with 20 trials. Models are finetuned on each task. Performance is measured by success rate. More details could be found in Appendix A.2. 

**Implementation details** We use one static level. The ratio of static tokens is set to 0 _._ 9, corresponding to 230 static tokens and 

Table 4: Results on the temporal-dependent tasks for multi-frame integration. All models use OpenVLA-OFT [18] as the base model. OpenVLA-OFT<sup>_†_</sup> denotes a naive baseline that packs as many frames as possible into the context. 

|Models|On Stove_↑_|Position Reset_↑_|Doneness (seconds)_↓_|
|---|---|---|---|
|OpenVLA-OFT<sup>_†_</sup>|39_._0%|78_._0%|0_._44|
|TTF-VLA [22]|7_._8%|1_._5%|1_._51|
|TraceVLA [61]|2_._0%|3_._0%|1_._41|
|MemoryVLA [44]|23_._0%|2_._0%|1_._49|
|ContextVLA [14]|50_._8%|22_._3%|0_._37|
|DySta (Ours)|**69**_._**8**%|**83**_._**0**%|**0**_._**26**|


26 dynamic tokens. The number of observations is set to 20, with a sampling interval of 20 frames (1 frame per second), resulting in 750 context tokens. More details could be found in Appendix D. 

**Results** As shown in Table 4, our method significantly and consistently outperforms all baselines on all objectives, with an average improvement of 24 _._ 5%. On the real-world experiments in Appendix E, we achieve 23 _._ 3% absolute in absolute success rate. Single-image methods such as TraceVLA almost always fail, since the task cannot be solved from the current observation alone, and visual traces provide only marginal additional benefit. ContextVLA underperforms due to non-learnable pooling observations, which may discard critical temporal and spatial details. MemoryVLA presents the LLM backbone with only a single frame at each timestep, leaving multi-frame reasoning to a lightweight decoder; as a result, the LLM itself does not reason over multiple frames, which limits the model’s capacity. While these baselines have their own ways to reduce context length, they do so at the cost of information or model capacity. In contrast, our approach preserves all relevant visual information by reusing temporally persistent static tokens, enabling effective multi-frame integration within a limited context window. 

8 

### **4.3 Ablation Studies** 

To validate the effectiveness of the proposed components, we conduct ablation studies on each of them, with results summarized in Table 5. From the second row, removing the contrastive learning objective leads to a noticeable performance degradation, as there is no longer an explicit mechanism to enforce temporal consistency in the static tokens. Performance also declines when the L2 static cache is removed and only a single-level static cache is used, as shown in the third row, highlighting the importance of the proposed multi-level caching design. Finally, replacing the learnable recache gate results in a further drop in performance, demonstrating the necessity of adaptive cache refreshing. 

### **4.4 Visualizations** 

We visualize the attention between the image and static/dynamic tokens across timesteps in Figure 6. 

Dynamic tokens consistently attend to movable objects, most notably the gripper (including its shadow) and the apple on the tabletop. This behavior aligns with their intended role of capturing temporally varying, actionrelevant elements in the scene. 

Table 5: Ablation studies. _w/o Contrast_ removes the contrastive learning objective during training. _w/o L2 cache_ ablates the multilevel design by retaining only a single static cache level. _Fixed step_ replaces the learnable recache gate by forcing the refresh of the cache at fixed intervals. The refresh interval is set to match the average recaching interval of DySta (first row). 

||visual|matching|variant a|ggregation|
|---|---|---|---|---|
||PickCan|MoveNear|PickCan|MoveNear|
|DySta|**92**_._**7**|**88**_._**8**|**92**_._**4**|81_._0|
|w/o Contrast|91_._3|84_._6|91_._6|**82**_._**7**|
|w/o L2 cache|92_._0|85_._0|91_._5|81_._5|
|fixed step|87_._7|81_._7|85_._3|74_._8|


L1 static tokens, which are designed to represent the most persistent visual information, primarily focus on background and ambient regions. Their attention heatmaps are often strongest in areas without salient foreground objects. We interpret this behavior as L1 static tokens of shallow layers functioning as sink tokens, capturing coarse, global scene context rather than object-specific details. Importantly, their attention patterns remain highly consistent across timesteps, reflecting strong temporal invariance. 

L2 static tokens exhibit intermediate behavior between L1 static and dynamic tokens. They attend more strongly to semi-static objects, such as the drawer, which typically remains stationary most of the time. At _t_ = 0 both drawer handles are highlighted, as either could potentially be moved. After the drawer is opened ( _t >_ 100), the attention maps stabilize and remain focused on the drawer structure, indicating that these tokens capture object-level static information with moderate temporal persistence. The robotic arm is also highlighted at certain frames, which we attribute to its importance in the task and the need to preserve its appearance across timesteps. 

We further illustrate how static-dynamic assignments evolve along a trajectory in Appendix J. 

## **5 Conclusion** 

We introduced DySta, a method that improves efficiency and multi-frame integration in VLA models via static–dynamic disentanglement. By reusing temporally persistent static tokens and selectively refreshing them through a learnable 


Figure 6: Attention map visualization across time. For each token, we compute its last-layer attention to image patches and upsample the result to the full image resolution to produce a heatmap. Heatmaps are averaged over tokens of the same type and displayed by row (e.g., the Dynamic row shows the average attention heatmap of all dynamic tokens). 

recache gate, DySta enables compact multi-frame contexts and efficient inference. Experiments show that our approach substantially improves performance on temporally dependent tasks while providing meaningful speedups over strong baselines. These results suggest that explicitly modeling temporal 

9 

persistence is a promising direction for scalable and practical VLA systems. **Limitations** . We realize our approach based on pretrained VLAs. Such a strategy may not fully unleash the performance of the model. Future work could focus on pretraining VLAs with our architecture from scratch. 

10 

## **References** 

- [1] Suneel Belkhale, Yuchen Cui, and Dorsa Sadigh. Hydra: Hybrid robot actions for imitation learning. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2023. 

- [2] Lucas Beyer, Andreas Steiner, André Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- [3] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control, 2024. URL `https://arxiv. org/abs/2410.24164` . 

- [4] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- [5] Lawrence Yunliang Chen, Simeon Adebola, and Ken Goldberg. Berkeley UR5 demonstration dataset. `https://sites.google.com/view/berkeley-ur5/home` . 

- [6] Nicola S Clayton and Anthony Dickinson. Episodic-like memory during cache recovery by scrub jays. _Nature_ , 395(6699):272–274, 1998. 

- [7] Zichen Jeff Cui, Yibin Wang, Nur Muhammad Mahi Shafiullah, and Lerrel Pinto. From play to policy: Conditional behavior generation from uncurated robot data. In _Proceedings of International Conference on Learning Representations (ICLR)_ , 2023. 

- [8] Shivin Dass, Jullian Yapeter, Jesse Zhang, Jiahui Zhang, Karl Pertsch, Stefanos Nikolaidis, and Joseph J. Lim. Clvr jaco play dataset, 2023. URL `https://github.com/clvrai/clvr_ jaco_play_dataset` . 

- [9] Frederik Ebert, Yanlai Yang, Karl Schmeckpeper, Bernadette Bucher, Georgios Georgakis, Kostas Daniilidis, Chelsea Finn, and Sergey Levine. Bridge data: Boosting generalization of robotic skills with cross-domain datasets. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2022. 

- [10] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models, 2021. URL `https://arxiv.org/abs/2106.09685` . 

- [11] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization, 2025. URL `https://arxiv.org/abs/2504.16054` . 

- [12] Eric Jang, Shixiang Gu, and Ben Poole. Categorical reparameterization with gumbel-softmax. _arXiv preprint arXiv:1611.01144_ , 2016. 

- [13] Eric Jang, Alex Irpan, Mohi Khansari, Daniel Kappler, Frederik Ebert, Corey Lynch, Sergey Levine, and Chelsea Finn. Bc-z: Zero-shot task generalization with robotic imitation learning. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2022. 

- [14] Huiwon Jang, Sihyun Yu, Heeseung Kwon, Hojin Jeon, Younggyo Seo, and Jinwoo Shin. Contextvla: Vision-language-action model with amortized multi-frame context. _arXiv preprint arXiv:2510.04246_ , 2025. 

11 

- [15] Dmitry Kalashnikov, Alex Irpan, Peter Pastor, Julian Ibarz, Alexander Herzog, Eric Jang, Deirdre Quillen, Ethan Holly, Mrinal Kalakrishnan, Vincent Vanhoucke, et al. Qt-opt: Scalable deep reinforcement learning for vision-based robotic manipulation. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2018. 

- [16] Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic vlms: Investigating the design space of visually-conditioned language models. In _Forty-first International Conference on Machine Learning_ , 2024. 

- [17] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [18] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. 2025. URL `https://arxiv.org/abs/2502.19645` . 

- [19] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 

- [20] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 

- [21] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

- [22] Chenghao Liu, Jiachen Zhang, Chengxuan Li, Zhimu Zhou, Shixin Wu, Songfang Huang, and Huiling Duan. Ttf-vla: Temporal token fusion via pixel-attention integration for visionlanguage-action models. _arXiv preprint arXiv:2508.19257_ , 2025. 

- [23] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _Advances in neural information processing systems_ , 36:34892–34916, 2023. 

- [24] Huihan Liu, Soroush Nasiriany, Lance Zhang, Zhiyao Bao, and Yuke Zhu. Robot learning on the job: Human-in-the-loop autonomy and learning during deployment. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

- [25] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization, 2019. URL `https: //arxiv.org/abs/1711.05101` . 

- [26] Guanxing Lu, Wenkai Guo, Chubin Zhang, Yuheng Zhou, Haonan Jiang, Zifeng Gao, Yansong Tang, and Ziwei Wang. Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning. _arXiv preprint arXiv:2505.18719_ , 2025. 

- [27] Jianlan Luo, Charles Xu, Xinyang Geng, Gilbert Feng, Kuan Fang, Liam Tan, Stefan Schaal, and Sergey Levine. Multi-stage cable routing through hierarchical imitation learning. _IEEE Transactions on Robotics_ , 40:1476–1491, 2024. 

- [28] Jianlan Luo, Charles Xu, Fangchen Liu, Liam Tan, Zipeng Lin, Jeffrey Wu, Pieter Abbeel, and Sergey Levine. Fmb: a functional manipulation benchmark for generalizable robotic learning. _The International Journal of Robotics Research_ , 2024. 

- [29] Chris J Maddison, Andriy Mnih, and Yee Whye Teh. The concrete distribution: A continuous relaxation of discrete random variables. _arXiv preprint arXiv:1611.00712_ , 2016. 

- [30] Ajay Mandlekar, Yuke Zhu, Animesh Garg, Jonathan Booher, Max Spero, Albert Tung, Julian Gao, John Emmons, Anchit Gupta, Emre Orbay, et al. Roboturk: A crowdsourcing platform for robotic skill learning through imitation. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2018. 

12 

- [31] Oier Mees, Jessica Borja-Diaz, and Wolfram Burgard. Grounding language with visual affordances over unstructured data. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , 2023. 

- [32] Russell Mendonca, Shikhar Bahl, and Deepak Pathak. Structured world models from human videos. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2023. 

- [33] Soroush Nasiriany, Tian Gao, Ajay Mandlekar, and Yuke Zhu. Learning and retrieval from prior data for skill-based imitation learning. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2023. 

- [34] Aaron van den Oord, Yazhe Li, and Oriol Vinyals. Representation learning with contrastive predictive coding. _arXiv preprint arXiv:1807.03748_ , 2018. 

- [35] Seongmin Park, Hyungmin Kim, Wonseok Jeon, Juyoung Yang, Byeongwook Jeon, Yoonseon Oh, and Jungwook Choi. Quantization-aware imitation-learning for resource-efficient robotic control, 2024. URL `https://arxiv.org/abs/2412.01034` . 

- [36] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- [37] Gabriel Quere, Annette Hagengruber, Maged Iskandar, Samuel Bustamante, Daniel Leidner, Freek Stulp, and Jörn Vogel. Shared control templates for assistive robotics. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , 2020. 

- [38] Siddharth Reddy, Anca D. Dragan, and Sergey Levine. Sqil: Imitation learning via reinforcement learning with sparse rewards, 2019. URL `https://arxiv.org/abs/1905.11108` . 

- [39] Erick Rosete-Beas, Oier Mees, Gabriel Kalweit, Joschka Boedecker, and Wolfram Burgard. Latent plans for task-agnostic offline reinforcement learning. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2022. 

- [40] Saumya Saxena, Mohit Sharma, and Oliver Kroemer. Multi-resolution sensing for real-time control with vision-language models. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2023. 

- [41] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [42] Rutav Shah, Roberto Martín-Martín, and Yuke Zhu. Mutex: Learning unified policies from multimodal task specifications. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2023. 

- [43] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 

- [44] Hao Shi, Bin Xie, Yingfei Liu, Lin Sun, Fengrong Liu, Tiancai Wang, Erjin Zhou, Haoqiang Fan, Xiangyu Zhang, and Gao Huang. Memoryvla: Perceptual-cognitive memory in vision-languageaction models for robotic manipulation, 2025. URL `https://arxiv.org/abs/2508.19236` . 

- [45] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, Simon Alibert, Matthieu Cord, Thomas Wolf, and Remi Cadene. Smolvla: A vision-language-action model for affordable and efficient robotics, 2025. URL `https://arxiv.org/abs/2506.01844` . 

- [46] SimpleVLA-RL Team. Simplevla-rl: Online rl with simple reward enables training vla models with only one trajectory. `https://github.com/PRIME-RL/SimpleVLA-RL` , 2025. GitHub repository. 

- [47] Andreas Steiner, André Susano Pinto, Michael Tschannen, Daniel Keysers, Xiao Wang, Yonatan Bitton, Alexey Gritsenko, Matthias Minderer, Anthony Sherbondy, Shangbang Long, et al. Paligemma 2: A family of versatile vlms for transfer. _arXiv preprint arXiv:2412.03555_ , 2024. 

13 

- [48] Richard S Sutton, David McAllester, Satinder Singh, and Yishay Mansour. Policy gradient methods for reinforcement learning with function approximation. _Advances in neural information processing systems_ , 12, 1999. 

- [49] Xudong Tan, Yaoxin Yang, Peng Ye, Jialin Zheng, Bizhe Bai, Xinyi Wang, Jia Hao, and Tao Chen. Think twice, act once: Token-aware compression and action reuse for efficient inference in vision-language-action models. _arXiv preprint arXiv:2505.21200_ , 2025. 

- [50] Marcel Torne, Karl Pertsch, Homer Walke, Kyle Vedder, Suraj Nair, Brian Ichter, Allen Z. Ren, Haohuan Wang, Jiaming Tang, Kyle Stachowicz, Karan Dhabalia, Michael Equi, Quan Vuong, Jost Tobias Springenberg, Sergey Levine, Chelsea Finn, and Danny Driess. Mem: Multi-scale embodied memory for vision language action models, 2026. URL `https://www. pi.website/download/Mem.pdf` . 

- [51] Endel Tulving et al. Episodic and semantic memory. _Organization of memory_ , 1(381-403):1, 1972. 

- [52] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. _Advances in neural information processing systems_ , 30, 2017. 

- [53] Quan Vuong, Sergey Levine, Homer Rich Walke, Karl Pertsch, Anikait Singh, Ria Doshi, Charles Xu, Jianlan Luo, Liam Tan, Dhruv Shah, et al. Open x-embodiment: Robotic learning datasets and rt-x models. In _Towards Generalist Robots: Learning Paradigms for Scalable Skill Acquisition@ CoRL2023_ , 2023. 

- [54] Homer Walke, Kevin Black, Abraham Lee, Moo Jin Kim, Max Du, Chongyi Zheng, Tony Zhao, Philippe Hansen-Estruch, Quan Vuong, Andre He, Vivek Myers, Kuan Fang, Chelsea Finn, and Sergey Levine. Bridgedata v2: A dataset for robot learning at scale. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2023. 

- [55] Weihan Wang, Qingsong Lv, Wenmeng Yu, Wenyi Hong, Ji Qi, Yan Wang, Junhui Ji, Zhuoyi Yang, Lei Zhao, Song XiXuan, et al. Cogvlm: Visual expert for pretrained language models. _Advances in Neural Information Processing Systems_ , 37:121475–121499, 2024. 

- [56] Siyu Xu, Yunke Wang, Chenghao Xia, Dihao Zhu, Tao Huang, and Chang Xu. Vla-cache: Towards efficient vision-language-action model via adaptive token caching in robotic manipulation. _arXiv preprint arXiv:2502.02175_ , 2025. 

- [57] Ge Yan, Kris Wu, and Xiaolong Wang. ucsd kitchens dataset. `https://github.com/ geyan21/rlds_dataset_builder/tree/main/ucsd_kitchens` , 2023. 

- [58] Yantai Yang, Yuhao Wang, Zichen Wen, Luo Zhongwei, Chang Zou, Zhipeng Zhang, Chuan Wen, and Linfeng Zhang. Efficientvla: Training-free acceleration and compression for visionlanguage-action models. _arXiv preprint arXiv:2506.10100_ , 2025. 

- [59] Yang Yue, Yulin Wang, Bingyi Kang, Yizeng Han, Shenzhi Wang, Shiji Song, Jiashi Feng, and Gao Huang. Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution. _Advances in Neural Information Processing Systems_ , 37:56619–56643, 2024. 

- [60] Rongyu Zhang, Menghang Dong, Yuan Zhang, Liang Heng, Xiaowei Chi, Gaole Dai, Li Du, Yuan Du, and Shanghang Zhang. Mole-vla: Dynamic layer-skipping vision language action model via mixture-of-layers for efficient robot manipulation. _arXiv preprint arXiv:2503.20384_ , 2025. 

- [61] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daumé III, Andrey Kolobov, Furong Huang, and Jianwei Yang. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv preprint arXiv:2412.10345_ , 2024. 

- [62] Yifan Zhong, Fengshuo Bai, Shaofei Cai, Xuchuan Huang, Zhang Chen, Xiaowei Zhang, Yuanfei Wang, Shaoyang Guo, Tianrui Guan, Ka Nam Lui, Zhiquan Qi, Yitao Liang, Yuanpei Chen, and Yaodong Yang. A survey on vision-language-action models: An action tokenization perspective, 2025. URL `https://arxiv.org/abs/2507.01925` . 

14 

- [63] Gaoyue Zhou, Victoria Dean, Mohan Kumar Srirama, Aravind Rajeswaran, Jyothish Pari, Kyle Hatch, Aryan Jain, Tianhe Yu, Pieter Abbeel, Lerrel Pinto, et al. Train offline, test online: A real robot learning benchmark. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , 2023. 

- [64] Xinghao Zhu, Ran Tian, Chenfeng Xu, Mingxiao Huo, Wei Zhan, Masayoshi Tomizuka, and Mingyu Ding. Fanuc manipulation: A dataset for learning-based manipulation with fanuc mate 200id robot. `https://sites.google.com/berkeley.edu/fanuc-manipulation` , 2023. 

- [65] Xunyu Zhu, Jian Li, Yong Liu, Can Ma, and Weiping Wang. A survey on model compression for large language models, 2024. URL `https://arxiv.org/abs/2308.07633` . 

- [66] Yifeng Zhu, Peter Stone, and Yuke Zhu. Bottom-up skill discovery from unsegmented demonstrations for long-horizon robot manipulation. _IEEE Robotics and Automation Letters_ , 7(2): 4126–4133, 2022. 

- [67] Yifeng Zhu, Abhishek Joshi, Peter Stone, and Yuke Zhu. Viola: Imitation learning for visionbased manipulation with object proposal priors. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2023. 

- [68] Yuke Zhu, Josiah Wong, Ajay Mandlekar, Roberto Martín-Martín, Abhishek Joshi, Kevin Lin, Abhiram Maddukuri, Soroush Nasiriany, and Yifeng Zhu. robosuite: A modular simulation framework and benchmark for robot learning, 2025. URL `https://arxiv.org/abs/2009. 12293` . 

15 

## **A Dataset and Benchmark Details** 

### **A.1 Simulation** 

**Training** Table 6 summarizes the Open-X-Embodiment dataset we use for the base model CogACT [19]. Table 7 summarizes the LIBERO dataset we use for the base model OpenVLA-OFT [18]. 

Table 6: Open-X-Embodiment dataset composition we use for CogACT training. 

|Dataset|Ratio|
|---|---|
|Fractal [4]|27.1%|
|Kuka [15]|14.7%|
|Bridge [54, 9]|15.3%|
|Taco Play [39, 31]|3.4%|
|Jaco Play [8]|0.6%|
|Berkeley Cable Routing [27]|0.3%|
|Roboturk [30]|2.7%|
|Viola [67]|1.1%|
|Berkeley Autolab UR5 [5]|1.4%|
|Toto [63]|2.3%|
|Stanford Hydra Dataset [1]<br>|5.1%|
|Austin Buds Dataset [66]|0.2%|
|NYU Franka Play Dataset [7]|1.0%|
|UCSD Kitchen Dataset [57]|_<_0.1%|
|Austin Sailor Dataset [33]|2.5%|
|Austin Sirius Dataset [24]|2.0%|
|DLR EDAN Shared Control [37]|_<_0.1%|
|IAMLab CMU Pickup Insert [40]|1.0%|
|UTAustin Mutex [42]|2.6%|
|Berkeley Fanuc Manipulation [64]|0.9%|
|CMU Stretch [32]|0.2%|
|BC-Z [13]|8.6%|
|FMB Dataset [28]|2.4%|


Table 7: LIBERO dataset 

|Dataset|Libero-Spatial|Libero-Object|Libero-Goal|Libero-Long|
|---|---|---|---|---|
|#(trajectories)|432|454|428|379|


**SimplerEnv** SimplerEnv [20] is a simulation-based benchmark designed for tabletop robotic manipulation. It is explicitly constructed to minimize the sim-to-real gap, demonstrating strong alignment between simulation performance and real-world execution across multiple robot platforms. The benchmark supports two complementary evaluation configurations: Visual Matching, which emphasizes high visual fidelity to real-world environments, and Variant Aggregations, which systematically introduce visual perturbations such as changes in background, lighting, distractors, and surface textures to assess robustness. SIMPLER includes tasks instantiated on both the Google Robot and the WidowX robot, covering a diverse set of manipulation primitives such as picking, placing, navigation, and articulated object interaction. In all tasks, agents receive RGB visual observations and natural language instructions. SIMPLER offers two evaluation settings: 

- _Visual Matching:_ Real-world images are overlaid onto simulated environments, with foreground objects and robots adjusted to closely match real-world appearances. 

- _Variant Aggregation:_ Multiple environmental variations are generated—such as different backgrounds, lighting conditions, and surface textures. 

**LIBERO** LIBERO is built around a simulated Franka Emika Panda arm and provides high-quality human-teleoperated demonstration data paired with language-conditioned tasks to support sample- 

16 


Figure 7: In real-world evaluations with the Cobot Magic robot, each task is evaluated over 20 episodes. 

efficient learning and generalization. The benchmark comprises four distinct task suites—LIBEROSpatial, LIBERO-Object, LIBERO-Goal, and LIBERO-Long, each providing 10 distinct tasks. 

### **A.2 Real-World** 

For the acceleration experiments, we include 7 tasks across 3 categories in the acceleration experiment, with 20 episodes used for training and 20 trials used for evaluating each task. The task designs are detailed below: 

- **Pick-and-Place.** The robot is instructed to move an object from its original location to a specified destination (e.g., a pan or pot). We report the success rate for each object. 

- **Pouring.** The robot is instructed to pour the contents of a bottle or can into a container. We report the success rate for each target container. 

- **Drawer Opening.** The robot is instructed to open a specified drawer. We report the success rate of successfully opening the drawer. 

For the multi-frame integration experiments, we evaluate three tasks that require memory or temporal reasoning: 

17 


Figure 8: In real-world evaluations with the Cobot Magic robot for multi-frame integration, each task is evaluated over 20 episodes. 


Figure 9: Architecture of the recache gate. 

- **Sequential Heat.** The robot is instructed to heat the vegetables one at a time. The model must remember which vegetables have already been heated. 

- **Pour Twice.** The robot is instructed to pour from the bottle twice. The model must keep track of whether the first pour has already been completed. 

- **Press Buttons.** The robot is instructed to press a sequence of buttons. The model must remember which buttons have already been pressed and determine the next button to press. 

For each task, we vary both the object’s location and the robotic arm’s starting position. The demonstrations of tasks are illustrated in Figure 8 and Figure 10. 

## **B Architecture Details** 

**Recache gate** The recache gate is designed to predict the probability of refreshing cached representations based on images (or their latent representations) observed at different timesteps. To minimize additional inference latency in the VLA, the recache gate must remain lightweight. Accordingly, we adopt a simple MLP-based architecture. 

As illustrated in Figure 9, the gate takes as input latent embeddings **_Z_** _t_ 1 and **_Z_** _t_ 2 produced by the VLA’s vision backbone at two different timesteps. We first apply a position-wise feedforward network to each embedding. The embeddings are then transposed to enable a channel-wise feedforward operation. After these transformations and dimensionality reduction, the resulting features are flattened and passed through a final MLP to predict the recache probability. For different static levels, we share all parameters except for the final prediction head. 

18 

## **C LIBERO-Memory Benchmark** 

Following the LIBERO benchmark [21], the layout initialization is specified by the BDDL scene description file, which is a file format that specifies the initial layout’s sampling strategy and other meta information. 

1 <mark>`( define ( problem LIBERO_Kitchen_Tabletop_Manipulation )`</mark> 2 <mark>`( :domain robosuite)`</mark> 3 <mark>`( :language Heat the tomato sauce on the stove for 1.4 second and then heat the alphabet soup)`</mark> 4 <mark>`( :regions`</mark> 5 <mark>`( operation_region`</mark> 6 <mark>`( :target kitchen_table )`</mark> 7 <mark>`( :ranges (`</mark> 8 <mark>`(-0.2 0.09999999999999999 0.0 0.2)`</mark> 9 <mark>`)`</mark> 10 <mark>`)`</mark> 11 <mark>`( :yaw_rotation (`</mark> 12 <mark>`(0.0 0.0)`</mark> 13 <mark>`)`</mark> 14 <mark>`)`</mark> 15 <mark>`)`</mark> 16 <mark>`( stove_region`</mark> 17 <mark>`( :target kitchen_table )`</mark> 18 <mark>`( :ranges (`</mark> 19 <mark>`(-0 .30000000000000004 -0.2 -0.1 -0 .09999999999999999)`</mark> 20 <mark>`)`</mark> 21 <mark>`)`</mark> 22 <mark>`( :yaw_rotation (`</mark> 23 <mark>`(0.0 0.0)`</mark> 24 <mark>`)`</mark> 25 <mark>`)`</mark> 26 <mark>`)`</mark> 27 <mark>`( cook_region`</mark> 28 <mark>`( :target flat_stove_1 )`</mark> 29 <mark>`)`</mark> 30 <mark>`)`</mark> 31 32 <mark>`( :fixtures`</mark> 33 <mark>`kitchen_table - kitchen_table`</mark> 34 <mark>`flat_stove_1 - flat_stove`</mark> 35 <mark>`)`</mark> 36 37 <mark>`( :objects`</mark> 38 <mark>`alphabet_soup_1 - alphabet_soup`</mark> 39 <mark>`tomato_sauce_1 - tomato_sauce`</mark> 40 <mark>`)`</mark> 41 42 <mark>`( :obj_of_interest`</mark> 43 <mark>`tomato_sauce_1`</mark> 44 <mark>`alphabet_soup_1`</mark> 45 <mark>`)`</mark> 46 47 <mark>`( :init`</mark> 48 <mark>`( On tomato_sauce_1 kitchen_table_operation_region )`</mark> 49 <mark>`( On alphabet_soup_1 kitchen_table_operation_region )`</mark> 50 <mark>`( On flat_stove_1 kitchen_table_stove_region )`</mark> 51 <mark>`( Turnon flat_stove_1 )`</mark> 52 <mark>`)`</mark> 53 54 <mark>`( :goal`</mark> 55 <mark>`( And ( CloseXY tomato_sauce_1 ) ( On alphabet_soup_1 flat_stove_1_cook_region ))`</mark> 56 <mark>`)`</mark> 57 58 <mark>`)`</mark> 

Listing 1: An example of the PDDL scene description file used in LIBERO-Memory. 

19 


Figure 10: Examples of our proposed LIBERO Memory Benchmark. 


Figure 11: Distribution of the trajectory length of the LIBERO-Memory benchmark 

**Oracle demonstrations** We generate expert trajectories programmatically because the correct behavior in LIBERO-Memory is fully specified and unambiguous. For example, for a sub-task such as “place the tomato sauce can on the stove”, an oracle with access to the simulator state can deterministically execute the correct sequence. The oracle knows the target object and its current location, and issues movement commands that drive the end-effector toward that location. After each movement, it compares the updated end-effector position with the desired target and decides the next control direction. Once the end-effector is sufficiently close, the oracle closes the gripper to grasp the object and subsequently moves it to the specified target location. 

Figure 10 shows more detailed example trajectories of the benchmark. Figure 11 shows the distribution of the trajectory length of the benchmark. 

To better contextualize the absolute performance of our model, we include a human baseline for the benchmark in Table 8. Specifically, we recruited two human participants familiar with the task setup, who performed the tasks using standard keyboard controls. Each human participant completed 50 rollout episodes. The performance varies across subtasks: _On Stove_ is largely semantic and can be solved reliably by humans, while _Position Reset_ and _Doneness_ require precise tracking of spatial locations and elapsed time over long horizons, making them more challenging for humans and highlighting greater potential for machine learning models to excel. 

Table 8: Human Performance on LIBERO-Memory. 

|Models|On Stove_↑_|Position Reset_↑_|Doneness_↓_|
|---|---|---|---|
|Human 1|98_._0%|74_._0%|1_._58|
|Human 2|96_._0%|68_._0%|1_._44|
|DySta (Ours)|69_._8%|83_._0%|0_._26|


20 

## **D Implementation Details and Hyperparameter Choices** 

For the recache gate in Figure 9, the first FFN is a 3-layer MLP that reduce the embedding dimension from 2 _×_ 4096 to 128. The second FFN is a 3-layer MLP that reduce the number of embeddings from 256 to 128. The head after the flatten operation is a linear layer with input dimension 128 _×_ 64. 

**CogACT** We use LoRA [10] to train the model, with the rank of 32. We use AdamW [25] with a learning rate of 2 _×_ 10<sup>_−_5</sup> . Training is conducted on 2 _×_ H100 for 6000 steps, with a global batch size of 32. 

**OpenVLA-OFT** We use LoRA [10] to train the model, with the rank of 32. We use AdamW [25] with a learning rate of 5 _×_ 10<sup>_−_4</sup> . Training is conducted on 2 _×_ H100 for 15000 steps, with a global batch size of 64. 

For both base models, the coefficients of the training objectives are set as _α_ 1 = 0 _._ 2 _, α_ 2 = 0 _._ 1 _, β_ = 0 _._ 1. For their corresponding benchmarks, the evaluation and the acceleration measurements are all conducted on 1 _×_ L40S for each task. 

Table 9 summarizes the recaching threshold settings and the resulting average recaching intervals. 

Table 9: Recaching threshold settings and the resulting average recaching intervals 

||Pick Can|Move Near|Drawer|
|---|---|---|---|
|_δ_1|0_._8|0_._4|0_._7|
|_δ_2|0_._4|0_._3|0_._4|
|avg interval of L1|9_._14|2_._23|7_._47|
|avg interval of L2|2_._15|2_._05|4_._16|


## **E Real-World Experiments on Multi-Frame Integration** 

We summarize the results of real-world experiments on multi-frame integration in Table 10. We found that our method outperforms baselines, with an average absolute improvement of 23 _._ 3%. 

## **F Computational and Acceleration Analysis** 

In this section, we provide the full computational analysis of the context length reduction and the acceleration enabled by our approach. 

**Context length** Let _N_ be the number of total tokens (including image tokens and text tokens). Let _r_ be the fraction of tokens that are cached, and _N_<sup>_′_</sup> = (1 _− r_ ) _N_ be the number of recomputed tokens. 

Let _T_ be the number of observations that should be incorporated in the context. The context length with our method reduces from _NT_ to _rN_ + (1 _− r_ ) _NT_ = _NT − rN_ ( _T −_ 1). 

**Static token reuse** The complexity of the language model backbone in the VLA model mainly comes from two types of modules: the multi-head attention (MHA) layers and the feedforward neural networks. Let _d_ be the dimension of embedding. The FLOPs of the MHA layer are estimated by 4 _Nd_<sup>2</sup> + 2 _N_<sup>2</sup> _d_ , and the FLOPs of the feedforward neural network are estimated by 2 _Ndm_ , where _m_ is the hidden dimension of the MLP. Therefore, the total FLOPs can be written as _F_ = 4 _Nd_<sup>2</sup> + 2 _N_<sup>2</sup> _d_ + 2 _Ndm_ . 

With our method, given that the static tokens are cached, only the dynamic parts (including the dynamic image tokens and the language instructions), the projection layers in the MHA layer will reduce to 4 _N_<sup>_′_</sup> _d_<sup>2</sup> , the attention matrix calculation will reduce to 2 _N_<sup>_′_</sup> _Nd_ , and the FLOPs of the feedforward network will reduce to 2 _N_<sup>_′_</sup> _dm_ . The final FLOPs are _F_<sup>_′_</sup> = 4 _N_<sup>_′_</sup> _d_<sup>2</sup> + 2 _NN_<sup>_′_</sup> _d_ + 2 _N_<sup>_′_</sup> _dm_ . 

21 

Table 10: Real-world task accuracy (%) on temporally dependent tasks for multi-frame integration. Each task is evaluated over 20 trials. 

|Method|Heat<br>Vegetables|Pour<br>Twice|Press<br>Buttons|Average|
|---|---|---|---|---|
|MemoryVLA|10_._0|25_._0|45_._0|26_._7|
|ContextVLA|25_._0|40_._0|40_._0|35_._0|
|DySta (Ours)|**35**_._**0**|**75**_._**0**|**65**_._**0**|**58**_._**3**|


Table 11: Breakdown of the CUDA latency of each component. 

|Component|CUDA Latency (ms)|ratio|
|---|---|---|
|Vision Backbone|246_._9|41_._1%|
|Recache Gate|18_._7|3_._1%|
|LLM Backbone|335_._7|55_._8%|
|Total|601_._2|100_._0%|


Therefore, the theoretical FLOPs reduction of the LLM backbone _under an idealized setting_ could be estimated as 


The overall reduction will be diluted by the involvement of the vision backbone, the decoding module, and the cache refresh step. However, these components are significantly less computationally intensive than the LLM backbone. Moreover, the introduction of the recache gate incurs only negligible overhead ( _≈_ 1 _._ 27%) and has minimal impact on the overall computational complexity. The latency breakdown of each component is summarized in Table 11. 

## **G Latent Representation Drift** 

Methods such as [56] implicitly assume similarity in the pixel space lead to similarity in the latent space. In this section, we analyze the latent representations during VLA rollouts to show that this assumption is fundamentally flawed. 

As illustrated in Figure 12, we measure cosine similarity between tokens at each timestep and their initial tokens in both pixel and latent space. Visually static tokens still exhibit substantial latent drift — e.g., in layer 0, a pixel-constant token (orange) drops to 0.5 in latent space after just one timestep, while the blue token with minor pixel changes (steps 15–20) drops from 0.5 to 0.2. These results confirm that pixel-level similarity does not imply latent invariance, thus invalidating existing methods and motivating our learned recache mechanism operating in representation space. 

## **H Latency Distribution** 

We provide the latency distribution during rollout across tasks in Figure 13. On the *Pick Can* task, 86.0% of steps fully reuse static tokens across all levels, resulting in low latency ( 250 ms). A smaller fraction ( 7.4%) triggers an L2 refresh ( 500 ms), while only 6.6% of steps require an L1 refresh, leading to higher latency ( 900 ms). 

These results show that high-latency events are infrequent, with the vast majority of steps operating in the efficient reuse regime. Since our goal is to optimize overall rollout efficiency (in addition to enabling multi-frame integration), occasional latency spikes have a negligible impact on end-to-end performance. 

## **I Hyperparameter Sensitivity** 

In this section, we analyze the sensitivity of crucial hyperparameters. 

22 


Figure 13: The latency distribution for each step in rollouts. _Reuse_ means no refresh needed. _Ln Refresh_ means the need to refresh the n-th level static cache. 


Figure 14: Sensitivity analysis on the coefficients for each loss term. Experiments are conducted on Pick Can (Visual Matching). 

23 


Figure 15: Sensitivity analysis of the static ratio. Experiments are conducted on Pick Can (Visual Matching). 


Figure 16: An illustration that the model misclassifies objects and later corrects such errors. 

### **I.1 Objective Coefficients** 

We conduct sensitivity analysis of important hyperparameters in our training objective, i.e., _α_ and _β_ in our loss term. The results are plotted in Figure 14. 

For the coefficient _α_ of _L_ infoNCE, we find the performance to be stable across a broad range of values. 

For the coefficient _β_ of _L_ gate, we observe that performance is stable once _β ≥_ 0 _._ 1. When _β_ = 0, the recache gate is not effectively trained and degenerates to random refresh/reuse decisions, leading to significantly degraded performance. 

### **I.2 Static Ratio** 

We consider the static ratio as a tunable hyperparameter that can be adapted to different environments. For more dynamic settings, it can be adjusted by (1) reducing the ratio during training to allocate more capacity to dynamic tokens, or (2) lowering the recache threshold for more frequent cache refreshing at test time. 

Our sensitivity analysis in Figure 15 shows stable performance across a broad range of ratios, with degradation only at extreme values. 

## **J Temporal Evolution of Static-Dynamic Assignments** 

Below, we show a representative trajectory illustrating how DySta adapts its static-dynamic assignments over time. As shown in Figure 16, the Pepsi can is initially treated as static because it is not intended to be manipulated. However, when unexpected contact occurs, the model detects the resulting change and reclassifies the can as dynamic, thereby triggering a cache refresh. In some cases, objects such as the orange may be treated as dynamic even though they remain unchanged. This does not affect task correctness, but only introduces a small amount of additional computational overhead. 

24 

## **K Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none of which we feel must be specifically highlighted here. 

## **L Declaration of LLM Usage** 

We used large language models solely for editing and polishing the manuscript (e.g., grammar, phrasing, and typo correction). LLMs were not involved in the research ideation, methodology, experiments, or analysis, and do not constitute any original or non-standard component of this work. 

25 

## **NeurIPS Paper Checklist** 

1. **Claims** 

Question: Do the main claims made in the abstract and introduction accurately reflect the paper’s contributions and scope? 

Answer: [Yes] 

Justification: The three contributions stated in the introduction are each developed in the Method section and validated in the Experiments section, with scope explicitly stated. Guidelines: 

   - The answer [N/A] means that the abstract and introduction do not include the claims made in the paper. 

   - The abstract and/or introduction should clearly state the claims made, including the contributions made in the paper and important assumptions and limitations. A [No] or [N/A] answer to this question will not be perceived well by the reviewers. 

   - The claims made should match theoretical and experimental results, and reflect how much the results can be expected to generalize to other settings. 

   - It is fine to include aspirational goals as motivation as long as it is clear that these goals are not attained by the paper. 

2. **Limitations** 

Question: Does the paper discuss the limitations of the work performed by the authors? Answer: [Yes] 

Justification: The paper has included a limitation paragraph in the last section. 

Guidelines: 

   - The answer [N/A] means that the paper has no limitation while the answer [No] means that the paper has limitations, but those are not discussed in the paper. 

   - The authors are encouraged to create a separate “Limitations” section in their paper. 

   - The paper should point out any strong assumptions and how robust the results are to violations of these assumptions (e.g., independence assumptions, noiseless settings, model well-specification, asymptotic approximations only holding locally). The authors should reflect on how these assumptions might be violated in practice and what the implications would be. 

   - The authors should reflect on the scope of the claims made, e.g., if the approach was only tested on a few datasets or with a few runs. In general, empirical results often depend on implicit assumptions, which should be articulated. 

   - The authors should reflect on the factors that influence the performance of the approach. For example, a facial recognition algorithm may perform poorly when image resolution is low or images are taken in low lighting. Or a speech-to-text system might not be used reliably to provide closed captions for online lectures because it fails to handle technical jargon. 

   - The authors should discuss the computational efficiency of the proposed algorithms and how they scale with dataset size. 

   - If applicable, the authors should discuss possible limitations of their approach to address problems of privacy and fairness. 

   - While the authors might fear that complete honesty about limitations might be used by reviewers as grounds for rejection, a worse outcome might be that reviewers discover limitations that aren’t acknowledged in the paper. The authors should use their best judgment and recognize that individual actions in favor of transparency play an important role in developing norms that preserve the integrity of the community. Reviewers will be specifically instructed to not penalize honesty concerning limitations. 

3. **Theory assumptions and proofs** 

Question: For each theoretical result, does the paper provide the full set of assumptions and a complete (and correct) proof? 

Answer: [Yes] 

26 

Justification: The paper provides computational analysis in the main text and its derivation in the appendix. 

Guidelines: 

- The answer [N/A] means that the paper does not include theoretical results. 

- All the theorems, formulas, and proofs in the paper should be numbered and crossreferenced. 

- All assumptions should be clearly stated or referenced in the statement of any theorems. 

- The proofs can either appear in the main paper or the supplemental material, but if they appear in the supplemental material, the authors are encouraged to provide a short proof sketch to provide intuition. 

- Inversely, any informal proof provided in the core of the paper should be complemented by formal proofs provided in appendix or supplemental material. 

- Theorems and Lemmas that the proof relies upon should be properly referenced. 

### 4. **Experimental result reproducibility** 

Question: Does the paper fully disclose all the information needed to reproduce the main experimental results of the paper to the extent that it affects the main claims and/or conclusions of the paper (regardless of whether the code and data are provided or not)? 

Answer: [Yes] 

Justification: The paper describes the experimental setting in the main text and provides the details in the appendix. The code has also been provided in the supplemental material. 

Guidelines: 

- The answer [N/A] means that the paper does not include experiments. 

- If the paper includes experiments, a [No] answer to this question will not be perceived well by the reviewers: Making the paper reproducible is important, regardless of whether the code and data are provided or not. 

- If the contribution is a dataset and/or model, the authors should describe the steps taken to make their results reproducible or verifiable. 

- Depending on the contribution, reproducibility can be accomplished in various ways. For example, if the contribution is a novel architecture, describing the architecture fully might suffice, or if the contribution is a specific model and empirical evaluation, it may be necessary to either make it possible for others to replicate the model with the same dataset, or provide access to the model. In general. releasing code and data is often one good way to accomplish this, but reproducibility can also be provided via detailed instructions for how to replicate the results, access to a hosted model (e.g., in the case of a large language model), releasing of a model checkpoint, or other means that are appropriate to the research performed. 

- While NeurIPS does not require releasing code, the conference does require all submissions to provide some reasonable avenue for reproducibility, which may depend on the nature of the contribution. For example 

- (a) If the contribution is primarily a new algorithm, the paper should make it clear how to reproduce that algorithm. 

- (b) If the contribution is primarily a new model architecture, the paper should describe the architecture clearly and fully. 

- (c) If the contribution is a new model (e.g., a large language model), then there should either be a way to access this model for reproducing the results or a way to reproduce the model (e.g., with an open-source dataset or instructions for how to construct the dataset). 

- (d) We recognize that reproducibility may be tricky in some cases, in which case authors are welcome to describe the particular way they provide for reproducibility. In the case of closed-source models, it may be that access to the model is limited in some way (e.g., to registered users), but it should be possible for other researchers to have some path to reproducing or verifying the results. 

### 5. **Open access to data and code** 

27 

Question: Does the paper provide open access to the data and code, with sufficient instructions to faithfully reproduce the main experimental results, as described in supplemental material? 

Answer: [Yes] 

Justification: The code and the instructions have been provided in the supplemental material, and the data is publicly available for the simulation experiments. Guidelines: 

   - The answer [N/A] means that paper does not include experiments requiring code. 

   - Please see the NeurIPS code and data submission guidelines ( `https://neurips.cc/ public/guides/CodeSubmissionPolicy` ) for more details. 

   - While we encourage the release of code and data, we understand that this might not be possible, so [No] is an acceptable answer. Papers cannot be rejected simply for not including code, unless this is central to the contribution (e.g., for a new open-source benchmark). 

   - The instructions should contain the exact command and environment needed to run to reproduce the results. See the NeurIPS code and data submission guidelines ( `https: //neurips.cc/public/guides/CodeSubmissionPolicy` ) for more details. 

   - The authors should provide instructions on data access and preparation, including how to access the raw data, preprocessed data, intermediate data, and generated data, etc. 

   - The authors should provide scripts to reproduce all experimental results for the new proposed method and baselines. If only a subset of experiments are reproducible, they should state which ones are omitted from the script and why. 

   - At submission time, to preserve anonymity, the authors should release anonymized versions (if applicable). 

   - Providing as much information as possible in supplemental material (appended to the paper) is recommended, but including URLs to data and code is permitted. 

6. **Experimental setting/details** 

Question: Does the paper specify all the training and test details (e.g., data splits, hyperparameters, how they were chosen, type of optimizer) necessary to understand the results? 

Answer: [Yes] 

Justification: The paper describes the experimental setting in the main text and provides the details in the appendix. 

Guidelines: 

   - The answer [N/A] means that the paper does not include experiments. 

   - The experimental setting should be presented in the core of the paper to a level of detail that is necessary to appreciate the results and make sense of them. 

   - The full details can be provided either with the code, in appendix, or as supplemental material. 

7. **Experiment statistical significance** 

Question: Does the paper report error bars suitably and correctly defined or other appropriate information about the statistical significance of the experiments? 

Answer: [No] 

Justification: We do not report error bars across training runs due to the prohibitive computational cost of training VLA models—each reported number can require multiple days on H100-class GPUs—which makes multi-seed training infeasible within the resource budget of this work. This is consistent with standard practice in prior VLA literature. Each result is instead aggregated over multiple evaluation episodes per task to mitigate evaluation variance. Guidelines: 

- The answer [N/A] means that the paper does not include experiments. 

- The authors should answer [Yes] if the results are accompanied by error bars, confidence intervals, or statistical significance tests, at least for the experiments that support the main claims of the paper. 

28 

- The factors of variability that the error bars are capturing should be clearly stated (for example, train/test split, initialization, random drawing of some parameter, or overall run with given experimental conditions). 

- The method for calculating the error bars should be explained (closed form formula, call to a library function, bootstrap, etc.) 

- The assumptions made should be given (e.g., Normally distributed errors). 

- It should be clear whether the error bar is the standard deviation or the standard error of the mean. 

- It is OK to report 1-sigma error bars, but one should state it. The authors should preferably report a 2-sigma error bar than state that they have a 96% CI, if the hypothesis of Normality of errors is not verified. 

- For asymmetric distributions, the authors should be careful not to show in tables or figures symmetric error bars that would yield results that are out of range (e.g., negative error rates). 

- If error bars are reported in tables or plots, the authors should explain in the text how they were calculated and reference the corresponding figures or tables in the text. 

### 8. **Experiments compute resources** 

Question: For each experiment, does the paper provide sufficient information on the computer resources (type of compute workers, memory, time of execution) needed to reproduce the experiments? 

Answer: [Yes] 

Justification: The paper describes the compute resources used for the experiments in in the appendix. 

Guidelines: 

   - The answer [N/A] means that the paper does not include experiments. 

   - The paper should indicate the type of compute workers CPU or GPU, internal cluster, or cloud provider, including relevant memory and storage. 

   - The paper should provide the amount of compute required for each of the individual experimental runs as well as estimate the total compute. 

   - The paper should disclose whether the full research project required more compute than the experiments reported in the paper (e.g., preliminary or failed experiments that didn’t make it into the paper). 

9. **Code of ethics** 

Question: Does the research conducted in the paper conform, in every respect, with the NeurIPS Code of Ethics `https://neurips.cc/public/EthicsGuidelines` ? 

Answer: [Yes] 

Justification: The paper advances general machine learning research and does not raise any ethical concerns. The authors have reviewed the NeurIPS Code of Ethics and confirm that their research conforms to it. 

Guidelines: 

   - The answer [N/A] means that the authors have not reviewed the NeurIPS Code of Ethics. 

   - If the authors answer [No], they should explain the special circumstances that require a deviation from the Code of Ethics. 

   - The authors should make sure to preserve anonymity (e.g., if there is a special consideration due to laws or regulations in their jurisdiction). 

10. **Broader impacts** 

Question: Does the paper discuss both potential positive societal impacts and negative societal impacts of the work performed? 

Answer: [Yes] 

Justification: The author has included an impact statement section in the appendix. 

29 

Guidelines: 

- The answer [N/A] means that there is no societal impact of the work performed. 

- If the authors answer [N/A] or [No], they should explain why their work has no societal impact or why the paper does not address societal impact. 

- Examples of negative societal impacts include potential malicious or unintended uses (e.g., disinformation, generating fake profiles, surveillance), fairness considerations (e.g., deployment of technologies that could make decisions that unfairly impact specific groups), privacy considerations, and security considerations. 

- The conference expects that many papers will be foundational research and not tied to particular applications, let alone deployments. However, if there is a direct path to any negative applications, the authors should point it out. For example, it is legitimate to point out that an improvement in the quality of generative models could be used to generate Deepfakes for disinformation. On the other hand, it is not needed to point out that a generic algorithm for optimizing neural networks could enable people to train models that generate Deepfakes faster. 

- The authors should consider possible harms that could arise when the technology is being used as intended and functioning correctly, harms that could arise when the technology is being used as intended but gives incorrect results, and harms following from (intentional or unintentional) misuse of the technology. 

- If there are negative societal impacts, the authors could also discuss possible mitigation strategies (e.g., gated release of models, providing defenses in addition to attacks, mechanisms for monitoring misuse, mechanisms to monitor how a system learns from feedback over time, improving the efficiency and accessibility of ML). 

### 11. **Safeguards** 

Question: Does the paper describe safeguards that have been put in place for responsible release of data or models that have a high risk for misuse (e.g., pre-trained language models, image generators, or scraped datasets)? 

Answer: [N/A] 

Justification: The released assets are a robot manipulation model and a simulation benchmark (LIBERO-Memory), which do not generate harmful content nor involve scraped or sensitive data, and therefore pose no high risk of misuse. 

Guidelines: 

   - The answer [N/A] means that the paper poses no such risks. 

   - Released models that have a high risk for misuse or dual-use should be released with necessary safeguards to allow for controlled use of the model, for example by requiring that users adhere to usage guidelines or restrictions to access the model or implementing safety filters. 

   - Datasets that have been scraped from the Internet could pose safety risks. The authors should describe how they avoided releasing unsafe images. 

   - We recognize that providing effective safeguards is challenging, and many papers do not require this, but we encourage authors to take this into account and make a best faith effort. 

12. **Licenses for existing assets** 

Question: Are the creators or original owners of assets (e.g., code, data, models), used in the paper, properly credited and are the license and terms of use explicitly mentioned and properly respected? 

Answer: [Yes] 

Justification: All pre-trained base models, datasets, and simulation frameworks are properly cited and used in accordance with their original licenses. 

Guidelines: 

- The answer [N/A] means that the paper does not use existing assets. 

- The authors should cite the original paper that produced the code package or dataset. 

30 

- The authors should state which version of the asset is used and, if possible, include a URL. 

- The name of the license (e.g., CC-BY 4.0) should be included for each asset. 

- For scraped data from a particular source (e.g., website), the copyright and terms of service of that source should be provided. 

- If assets are released, the license, copyright information, and terms of use in the package should be provided. For popular datasets, `paperswithcode.com/datasets` has curated licenses for some datasets. Their licensing guide can help determine the license of a dataset. 

- For existing datasets that are re-packaged, both the original license and the license of the derived asset (if it has changed) should be provided. 

- If this information is not available online, the authors are encouraged to reach out to the asset’s creators. 

### 13. **New assets** 

Question: Are new assets introduced in the paper well documented and is the documentation provided alongside the assets? 

Answer: [Yes] 

Justification: We introduce the benchmark and the codebase. Both are documented in the appendix (dataset construction, BDDL scene description, oracle demonstrations, and implementation details) and provided in the supplemental material. 

Guidelines: 

   - The answer [N/A] means that the paper does not release new assets. 

   - Researchers should communicate the details of the dataset/code/model as part of their submissions via structured templates. This includes details about training, license, limitations, etc. 

   - The paper should discuss whether and how consent was obtained from people whose asset is used. 

   - At submission time, remember to anonymize your assets (if applicable). You can either create an anonymized URL or include an anonymized zip file. 

14. **Crowdsourcing and research with human subjects** 

Question: For crowdsourcing experiments and research with human subjects, does the paper include the full text of instructions given to participants and screenshots, if applicable, as well as details about compensation (if any)? 

Answer: [N/A] 

Justification: The paper does not involve crowdsourcing. The human-performance reference in the appendix was conducted by two trained volunteers, which only offers as an additional context for understanding the experiments. 

Guidelines: 

- The answer [N/A] means that the paper does not involve crowdsourcing nor research with human subjects. 

- Including this information in the supplemental material is fine, but if the main contribution of the paper involves human subjects, then as much detail as possible should be included in the main paper. 

- According to the NeurIPS Code of Ethics, workers involved in data collection, curation, or other labor should be paid at least the minimum wage in the country of the data collector. 

### 15. **Institutional review board (IRB) approvals or equivalent for research with human subjects** 

Question: Does the paper describe potential risks incurred by study participants, whether such risks were disclosed to the subjects, and whether Institutional Review Board (IRB) approvals (or an equivalent approval/review based on the requirements of your country or institution) were obtained? 

31 

### Answer: [N/A] 

Justification: The paper does not involve study on human subjects. 

Guidelines: 

- The answer [N/A] means that the paper does not involve crowdsourcing nor research with human subjects. 

- Depending on the country in which research is conducted, IRB approval (or equivalent) may be required for any human subjects research. If you obtained IRB approval, you should clearly state this in the paper. 

- We recognize that the procedures for this may vary significantly between institutions and locations, and we expect authors to adhere to the NeurIPS Code of Ethics and the guidelines for their institution. 

- For initial submissions, do not include any information that would break anonymity (if applicable), such as the institution conducting the review. 

### 16. **Declaration of LLM usage** 

Question: Does the paper describe the usage of LLMs if it is an important, original, or non-standard component of the core methods in this research? Note that if the LLM is used only for writing, editing, or formatting purposes and does _not_ impact the core methodology, scientific rigor, or originality of the research, declaration is not required. 

Answer: [Yes] 

Justification: The paper includes a declaration in the appendix stating that LLMs were used only for editing and polishing the manuscript, with no involvement in the core methodology. Guidelines: 

- The answer [N/A] means that the core method development in this research does not involve LLMs as any important, original, or non-standard components. 

- Please refer to our LLM policy in the NeurIPS handbook for what should or should not be described. 

32 

