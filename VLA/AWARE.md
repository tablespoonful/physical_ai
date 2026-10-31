---
title: "AWARE: Action-Entropy-Weighted and Attention-Guided Retrieval of Observation Evidence for Vision-Language-Action Models"
date: "2026-02-20"
authors: "Jiabing Yang; Yixiang Chen; Yuan Xu; Peiyan Li; Zichen Wen; Bowen Fang"
url: https://arxiv.org/abs/2602.18020
pdf: https://arxiv.org/pdf/2602.18020
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.18020)** / [論文ページ](https://arxiv.org/abs/2602.18020)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **AWARE: Action-Entropy-Weighted and Attention-Guided Retrieval of Observation Evidence for Vision-Language-Action Models** 

Jiabing Yang<sup>1</sup><sup>_,_2</sup><sup>_,_5</sup> , Yixiang Chen<sup>1</sup><sup>_,_2</sup> , Yuan Xu<sup>1</sup><sup>_,_2</sup> , Peiyan Li<sup>1</sup><sup>_,_2</sup> , Zichen Wen<sup>3</sup> , Bowen Fang<sup>1</sup><sup>_,_2</sup> , Chenhang Cui<sup>4</sup> , Tao Yu<sup>1</sup><sup>_,_2</sup> , Qisen Ma<sup>1</sup><sup>_,_2</sup> , Kai Wang<sup>1</sup><sup>_,_2</sup> , Ziheng He<sup>1</sup><sup>_,_2</sup> , Wen Ye<sup>1</sup><sup>_,_2</sup> , Xiangnan Wu<sup>1</sup><sup>_,_2</sup> , Yingda Li<sup>1</sup><sup>_,_2</sup> , Yan Huang<sup>1</sup><sup>_,_2</sup><sup>_,_5</sup><sup>_,†_</sup> , Liang Wang<sup>1</sup><sup>_,_2</sup> 

**_Abstract_ — Vision-Language-Action (VLA) models combine multimodal perception with robotic control, demonstrating remarkable potential for generalizable manipulation. Yet, enhancing their execution typically relies on auxiliary sensory inputs (e.g., depth, 3D point clouds) or costly fine-tuning. Inspired by the insight that Feed-Forward Networks (FFNs) act as key-value memory, we propose Action-Entropy-Weighted and Attention-Guided Retrieval of Observation Evidence (AWARE), an effective, training-free, and plug-and-play module for VLAs. Specifically, AWARE tracks layer-wise uncertainty via an element-wise** **_Action Entropy_ metric, and retrieves observation evidence into the element's FFN through associative memory lookup. Crucially, the retrieved features are weighted by instruction-guided cross-modal attention to isolate task-relevant observation cues, while injection strength is adaptively scaled by the element's entropy and relative network depth. This selectively channels observation evidence to high-entropy action dimensions and deep layers where grounding decays, while leaving converged representations intact. Across LIBERO, SIMPLER, CALVIN, and real-world robot manipulation, AWARE consistently improves diverse VLA architectures with minimal computational overhead, achieving the largest gains on long-horizon tasks without architectural changes or additional training. Project page: https://jiabingyang01.github.io/AWARE/.** 

## I. INTRODUCTION 

Recent advancements in Vision-Language Models (VLMs) [1–3] have catalyzed the development of VisionLanguage-Action (VLA) models [4–6], which map visual observations and language instructions into low-level robot actions. Trained on web-scale pretraining corpora and demonstration data, modern VLAs generalize across diverse manipulation settings. Nonetheless, further boosting policy performance typically incurs prohibitive costs, constrained by the scarcity of physical robot data and non-negligible computational overhead required for fine-tuning. 

To enhance manipulation precision without massive data collection, prevailing approaches frequently augment visual inputs with specialized priors, such as visual trace prompting [7], 3D spatial encodings [8], or depth and point-cloud modalities [9–11]. Although effective, these interventions 

> _†_ Corresponding author. 

> 1School of Artificial Intelligence, University of Chinese Academy of Sciences. 

> 2New Laboratory of Pattern Recognition (NLPR), Institute of Automation, Chinese Academy of Sciences. yangjiabing2025@ia.ac.cn, yhuang@nlpr.ia.ac.cn 

> 3Shanghai Jiao Tong University. 

> 4National University of Singapore. 

> 5FiveAges. 


Fig. 1: **Empirical motivation for AWARE** (OpenVLA-OFT on LIBERO). **(a)** Observation subspace footprint diminishes across network depth, halving by layer 26 across all suites. **(b)** Action Entropy across all 56 action chunk elements: near steps settle early in middle layers while distant steps retain elevated predictive entropy until deep layers, forming a clear decision wavefront (white dashed isocontour) that motivates element-wise observation routing. 

necessitate customized sensor configurations, auxiliary encoders, and extensive task-specific fine-tuning. This motivates an appealing yet challenging question: _can we boost existing VLA policies entirely at inference time, in a training-free manner and without supplementary observation cues, external sensors, or auxiliary network modules?_ 

To address this, we investigate the internal representation dynamics of VLA models during forward inference. Two phenomena stand out. First, as tokens traverse the transformer stack, the proportion of the action representation explained by observation tokens diminishes monotonically, losing half of its subspace footprint by layer 26 across all task suites (Fig. 1a). Second, predictive uncertainty resolves asynchronously across action dimensions: early trajectory steps converge early in the layer stack, whereas as shown in Fig. 1b, distant future steps maintain elevated predictive entropy until deep layers, exhibiting a persistent uncertainty gap of 0 _._ 25 across the prediction horizon. A natural remedy suggests itself: re-inject observation evidence where predictive uncertainty remains high. Because Feed-Forward Networks (FFNs) act as keyvalue associative memories [12, 13], the model's native FFN layers can dynamically retrieve observation cues and reinforce action representations in the middle of the stack. 

Building on these observations, we propose **A** ction-Entropy- **W** eighted and **A** ttention-Guided **R** etrieval of Observation **E** vidence (AWARE), a lightweight, training-free, and plugand-play module that lets each action element autonomously 

regulate its own observation retrieval. AWARE computes the layer-wise **_Action Entropy_** for every individual action dimension, in place of a coarse aggregate scalar. It queries observation tokens using each element's hidden state and blends the retrieved features into the FFN output, modulated by the element's own entropy and normalized network depth. This continuous formulation channels observation evidence specifically to high-entropy action dimensions and deep layers where perception has faded, while preserving converged representations intact, with the retrieval conditioned by the instruction's cross-modal attention. In summary, our key contributions are: 

- We formulate an element-wise **_Action Entropy_** metric to track layer-wise predictive uncertainty, revealing pronounced divergence across temporal horizons. 

- We present **AWARE** , a training-free framework that uses native FFN memory to re-inject observation evidence into individual action elements proportionally to their uncertainty and depth, guided by instruction-relevant visual attention. 

- We validate AWARE across standard simulation benchmarks (LIBERO, SIMPLER, CALVIN) and real-world robots. The gains hold across diverse policy architectures, and ablations trace them to element-wise allocation rather than arbitrary perturbation. 

## II. RELATED WORK 

**Vision-Language-Action Models.** VLA models fine-tune pretrained VLMs on robot data to map observations and language onto low-level control [4, 5, 14–17], a recipe that scales with the cross-embodiment corpora behind it [18, 19]. They differ in how the action is represented, and that is what decides where an inference-time rule can attach: OpenVLA [4] decodes discrete action tokens through its language head, OpenVLA-OFT [6] decodes a whole chunk of placeholder tokens in parallel, CogACT [16] conditions a diffusion expert on a single cognition token, and _π_ 0 [5] attaches a flow-matching expert to a PaliGemma prefix [1]. Another line pretrains action representations from video data [20–23]. AWARE is defined on the positions each family reads its action from, so one rule covers all of them. 

**Uncertainty in Robot Learning.** Output entropy has guided dynamic decoding and token pruning in language models [24], and internal confidence has guided test-time visual retrieval to mitigate perceptual fading [25, 26]. In robotic control, Valle et al. [27] read token entropy as a VLA confidence score, and Karli et al. [28] use it to trigger human intervention. These signals gate a whole token, a whole layer, or a whole observation. A chunked VLA emits every step of a trajectory in one pass and its elements are at different stages of being decided within that pass, so the useful signal is not one number per layer but one per element, which is what AWARE acts on. 

**Perceptual Enhancement for Manipulation.** A common remedy for weak visual grounding is to add something to the input, such as visual traces [7], point clouds and depth [9], 

three-dimensional priors from a geometry model [10], or overlaid aiming cues [11]. Others keep the input and change what the policy is trained to attend to, through gaze reconstruction [29] or attention specialised to task-relevant factors [30]. Each buys accuracy with a sensor, an auxiliary encoder or task-specific fine-tuning. AWARE adds nothing: it re-reads the observation the model has already encoded, through the model’s own FFN, at inference time. 

## III. METHODOLOGY 

## _A. Feed-Forward Networks as Associative Memory_ 

Following the continuous associative memory formalism of Geva et al. [12], a transformer feed-forward network (FFN) with weights **_W_** 1 _∈_ R<sup>_d×D_</sup> , **_W_** 2 _∈_ R<sup>_D×d_</sup> and activation _ϕ_ computes: 


where the parameter columns of **_W_** 1 and **_W_** 2 constitute _D_ key-value pairs _{_ ( **_k_** _i,_ **_v_** _i_ ) _}_<sup>_D_</sup> _i_ =1<sup>(</sup><sup>**_k_**</sup><sup>_i,_</sup><sup>**_v_**</sup><sup>_i∈_R</sup><sup>_d_).Underthiskey-</sup> value view, the FFN executes an unnormalized soft associative retrieval: the hidden state **_h_** acts as a query against stored keys **_k_** _i_ , aggregating matching value vectors **_v_** _i_ weighted by inner-product similarity. Building upon this formulation, recent vision-language studies demonstrate that transformer memory spaces can be dynamically conditioned at inference time with external multimodal tokens to mitigate perceptual fading and attention degradation [13, 25, 26]. In robotic manipulation, where multi-step action execution is vulnerable to cumulative observation fading (Fig. 1a), we exploit this native associative structure to selectively retrieve instructiongrounded observation evidence directly into intermediate action representations, without altering pretrained parameters. 

## _B. Problem Formulation_ 

Vision-Language-Action (VLA) models are designed to jointly process observations and language instructions for the purpose of generating appropriate actions for robots. Formally, given the observation **_o_** _t_ at time _t_ and language instruction **_l_** , a model **_π_** predicts a temporal action sequence ( **_a_** _t,_ **_a_** _t_ +1 _, . . . ,_ **_a_** _t_ + _H−_ 1) (i.e., action chunk size _H_ ) for task execution: 


The observation is the visual input, concatenated with the proprioceptive state if available [5, 6], and each **_a_** _t_ is a 7-DoF end-effector command: three translations, three rotations and one gripper state. A chunked policy such as OpenVLA-OFT represents the _Na_ = _HDa_ action elements ( _H_ =8, _Da_ =7, indexed by _n ∈{_ 1 _, . . . , Na}_ ) as _Na_ placeholder tokens that are decoded in parallel in one bidirectional forward pass. 

## _C. Uncertainty-Aware Observation Retrieval_ 

**Element-Wise Action Entropy Formulation.** Building on prior inference-time interventions that exploit layer-wise predictive uncertainty in language models [24, 31], we tailor 


Fig. 2: **Overall framework of AWARE.** At every layer the language head reads each element of the predicted action representations and gives its Action Entropy. The observation features form a key-value memory that the element queries _<u>ℓ</u>_ through its FFN input, and the retrieved features enter its FFN output at the next layer with weight _wt,n_<sup>(</sup><sup>_ℓ_+1)</sup> = _α L−_ 1<sup>_H_</sup> _t,n_<sup>(</sup><sup>_ℓ_).</sup> Nothing is switched on or off, and the memory is read at every layer. 

an element-wise **_Action Entropy_** metric _Ht,n_<sup>(</sup><sup>_ℓ_)forchunked</sup> VLAs, quantifying decision uncertainty via the entropy of action-related output distributions across the layer hierarchy. The quantity is the entropy of the vocabulary distribution read at the _Na_ positions the action pathway consumes: the action tokens themselves where actions come straight from hidden states [6], the condition token where a second system decodes them [16], or the prefix tokens where a flow-matching expert attends to them. We define the layer-wise action entropy of the _n_ -th action element ( _n ∈{_ 1 _, . . . , Na}_ ) at time step _t_ as 


Here **_p_**<sup>(</sup> _t,n_<sup>_ℓ_)=</sup><sup>_{p_(</sup> _t,n,i_<sup>_ℓ_)</sup><sup>_}_</sup> _i_<sup>_K_</sup> =1<sup>isthecategoricaldistributionover</sup> the candidate tokens for the _n_ -th action or condition token, obtained by projecting the element’s hidden state at the output of layer _ℓ_ through the language modeling head and normalizing with softmax, following the “Logit Lens” formulation [32, 33]. For discrete actions, we set _K_ = 256 to match the number of action bins; for continuous actions, we likewise fix _K_ = 256 for definitional consistency. The normalization ensures _Ht,n_<sup>(</sup><sup>_ℓ_)</sup><sup>_∈_[0</sup><sup>_,_1].AWAREretainsall</sup> _Na_ entropy values, enabling fine-grained, element-specific modulation across the action dimensions. 

**Interpretation of Action Entropy.** In Transformer architectures, representations evolve via iterative refinement along the residual stream. Extensive work in mechanistic interpretability [32, 33] and contrastive decoding [31] establishes that projecting intermediate hidden states through the frozen 

language head reliably elicits latent categorical predictions without auxiliary training, correlating strongly with policy execution uncertainty in robotic manipulation [27, 28]. A potential concern is representation drift: intermediate hidden states are not explicitly trained against the final unembedding head, which could introduce an unaligned coordinate basis. Crucially, as established in [33], any such affine shift is _spatially invariant across tokens at the same layer ℓ_ . Such layer-wide drift manifests solely as an additive scalar offset to the layer’s baseline entropy, which is absorbed by the depth schedule _ℓ/_ ( _L−_ 1) and scaling factor _α_ . AWARE never relies on absolute cross-layer entropy calibration; it operates strictly on the _relative entropy contrast among action elements within the same layer ℓ_ (the decision wavefront in Fig. 1b). Because all _Na_ action elements share the identical coordinate geometry at layer _ℓ_ , their intra-layer relative entropy differences isolate genuine decision uncertainty, a mechanism directly corroborated by our diagnostic experiments in Table V. 

**Cross-Backbone Token Mapping.** The core formulation (Eqs. 3–7) remains identical across all backbones. The only model-dependent adaptation is the token positions where uncertainty is evaluated, aligning with how each architecture structures its action pathway. For chunked policies with bidirectional attention such as OpenVLA-OFT, entropy is evaluated across all _Na_ action placeholder tokens simultaneously ( _Na_ =56). For causal autoregressive models (OpenVLA, SpatialVLA), it is computed at each newly decoded action token ( _Na_ =1). In dual-system architectures like CogACT, it is evaluated at the cognition token that conditions the 

**Algorithm 1 A** ction-Entropy- **W** eighted and **A** ttention-Guided **R** etrieval of Observation **E** vidence <u>(AWARE).</u> 

action decoder. Finally, for flow-matching policies whose continuous expert lacks a vocabulary head ( _π_ 0, _π_ 0 _._ 5), the entropy is evaluated at the instruction positions of the prefix that condition the expert. We restrict this evaluation to the instruction tokens rather than the full prefix because visual patch tokens already constitute the observation memory **_o_** _t_ , and the language head yields meaningful probability distributions only over text tokens. 

**Require:** VLA model **_π_** with _L_ layers; observation **_o_** _t_ =( **_o_**<sup>_v_</sup> _t_<sup>_,_</sup><sup>**_o_**</sup> _t_<sup>_p_);instruction</sup><sup>**_l_**;strength</sup><sup>_α_.</sup> 

**Ensure:** Action chunk **_A_** _t_ =( **_a_** _t, . . . ,_ **_a_** _t_ + _H−_ 1). 

- 1: Form the observation memory **_O_** _t_ from the encoded observation tokens. _▷_ Eq. 4 

- 2: Weight its rows by the instruction’s own read _gt,i_ , once per forward pass. _▷_ Eq. 5 

**Element-Wise FFN Retrieval.** To provide timely perceptual grounding for action dimensions that remain unresolved during execution, AWARE retrieves observation evidence into the subsequent FFN layer, allowing each action element to autonomously regulate its own retrieval. We treat the encoded observation features **_o_** _t_ = ( **_o_** _t,_ 1 _, . . . ,_ **_o_** _t,No_ ) as a key-value memory and use the hidden state **_h_**<sup>(</sup> _t,n_<sup>_ℓ_+1)</sup> entering the FFN of action element _n_ at layer _ℓ_ +1 as the query: 

- 3: **for** _ℓ_ = 0 **to** _L −_ 2 **do** 4: Apply the LM head to the _Na_ action elements at the output of layer _ℓ_ to obtain **_p_**<sup>(</sup> _t,n_<sup>_ℓ_).</sup> 

- 5: Compute Action Entropy _Ht,n_<sup>(</sup><sup>_ℓ_)foreveryelement</sup><sup>_n_.</sup> _▷_ Eq. 3 

- 6: At layer _ℓ_ +1, retrieve INJ<sup>(</sup> _t,n_<sup>_ℓ_+1)</sup> for every action element from **_O_** _t_ . _▷_ Eq. 4 _<u>ℓ</u>_ 

- 7: Blend with weight _wt,n_<sup>(</sup><sup>_ℓ_+1)</sup> = _α L−_ 1<sup>_H_</sup> _t,n_<sup>(</sup><sup>_ℓ_); leave every</sup> other token unchanged. _▷_ Eqs. 6, 7 

- 8: **end for** 9: Decode **_A_** _t_ from the final hidden state through the policy head. 


Here _gt,i_ is the instruction-to-observation attention defined below, and the retrieval operates as a linear associative memory lookup following Eq. 1 with identity activation. In this formulation, observation features act simultaneously as keys and values, and the query **_h_**<sup>(</sup> _t,n_<sup>_ℓ_+1)</sup> retrieves a linear combination of observation tokens weighted by semantic alignment and instruction relevance. In practice, Eq. 4 is vectorized across tokens as _s_ **_O_**<sup>_⊤_</sup> _t_<sup>diag(</sup><sup>**_g_**</sup><sup>_t_)</sup><sup>**_O_**</sup><sup>_t_</sup><sup>**_h_**(</sup> _t,n_<sup>_ℓ_+1)</sup> where **_O_** _t ∈_ R<sup>_No×d_</sup> stacks the observation tokens, requiring only two standard matrix multiplications without iterative looping or matrix inversion. The scaling factor _s_ matches the mean activation magnitude of the native FFN to that of the retrieved features over the action elements, ensuring well-conditioned feature blending. The retrieved evidence is then integrated into the FFN output of element _n_ according to its own uncertainty. **Instruction-Guided Observation Conditioning.** Without task conditioning, an unconstrained associative query _⟨_ **_h_**<sup>(</sup> _t,n_<sup>_ℓ_+1)</sup> _,_ **_o_** _t,i⟩_ can disperse broadly over irrelevant visual background or distractors with high token norms. Because robot manipulation is fundamentally governed by the language instruction specifying target objects and spatial relations, we modulate retrieval weights via cross-modal semantic alignment between instruction tokens and observation patches: 

carries the weight 


read from the entropy of the layer below and applied to the FFN of this one, scaled by the intervention strength _α >_ 0. The normalized depth ratio _ℓ/_ ( _L−_ 1) progressively scales the intervention, mirroring the empirical decay of observation features across depth (Fig. 1a), while the entropy factor _H_<sup>(</sup><sup>_ℓ_)</sup> _t,n_<sup>concentratesretrievalspecificallyonactionelements</sup> with elevated predictive entropy. In practice, because distinct manipulation domains exhibit varying horizon lengths, visual clutter, and precision requirements, policy backbones naturally manifest different baseline action entropy distributions. To achieve optimal performance in practical deployment, _α_ can be configured to match task characteristics, while remaining robust across a broad interior range (Section IV-C). The modified FFN output is then computed as: 


Here, _rt,it,i_ aggregates non-negative semantic alignment across instruction tokens. Comparing against the uniform baseline 1 _/Noo_ yields a normalized importance score: observation tokens receiving at or above uniform attention retain full retrieval weight ( _gt,i_ =1), while task-irrelevant regions are smoothly attenuated. Computing **_g_** _t_ requires only a single matrix multiplication per forward pass with zero learnable parameters, focusing associative retrieval on instructiongrounded visual entities. 

IV. EXPERIMENTS 

## _A. Simulation Experiments_ 

**Simulation Setup and Baselines.** To systematically validate AWARE across diverse robotic manipulation settings, we evaluate on three widely-adopted simulation benchmarks: 

**Continuous Adaptive Blending.** Element _n_ at layer _ℓ_ +1 

TABLE I: Performance comparison on the LIBERO benchmark. All baselines are evaluated under identical checkpoints and evaluation pipelines. Bold denotes the better of a pair. Per-suite intervention strengths _α_ for Spatial, Object, Goal, and Long are: OpenVLA-OFT (0.04, 0.05, 0.10, 0.03), _π_ 0 (0.03, 0.04, 0.05, 0.03), _π_ 0 _._ 5 (0.01, 0.08, 0.01, 0.07), and OpenVLA (0.03, 0.02, 0.01, 0.01). 

|**Method**|**Spatial**|**Object**|**Goal**|**Long**|**Average**|
|---|---|---|---|---|---|
|OpenVLA [4] (_CoRL’24_)|82.8|85.6|78.4|49.6|74.1|
|**_w/_ AWARE** (_Ours_)|**86.4**|**87.0**|**79.0**|**57.2**|**77.4**|
|∆|**+3.6**|**+1.4**|**+0.6**|**+7.6**|**+3.3**|
|_π_0 [5] (_RSS’25_)|96.4|97.2|93.8|81.2|92.2|
|**_w/_ AWARE** (_Ours_)|**98.2**|**98.6**|**94.4**|**84.0**|**93.8**|
|∆|**+1.8**|**+1.4**|**+0.6**|**+2.8**|**+1.6**|
|_π_0_._5 [34] (_CoRL’25_)|98.2|98.6|97.6|92.6|96.8|
|**_w/_ AWARE** (_Ours_)|**99.2**|**99.6**|**98.4**|**94.0**|**97.8**|
|∆|**+1.0**|**+1.0**|**+0.8**|**+1.4**|**+1.0**|
|OpenVLA-OFT [6] (_RSS’25_)|98.0|98.2|97.6|93.8|96.9|
|**_w/_ AWARE** (_Ours_)|**99.2**|**98.6**|**98.6**|**96.0**|**98.1**|
|∆|**+1.2**|**+0.4**|**+1.0**|**+2.2**|**+1.2**|


TABLE II: Performance comparison on the SIMPLER benchmark (Visual Matching). Evaluated with official released checkpoints under identical environments and pipelines. Intervention strengths are _α_ =0 _._ 09 for CogACT and _α_ =0 _._ 08 for SpatialVLA. Bold denotes the better of a pair. 

|**Google Robot**|**Pick**<br>**Coke Can**|**Move**<br>**Near**|**Open/Close**<br>**Drawer**|**Open Top Drawer**<br>**and Place Apple**|**Average**|
|---|---|---|---|---|---|
|CogACT [16] (_arXiv’24_)|90.0|**85.4**|70.4|49.1|73.7|
|**_w/_ AWARE** (_Ours_)|**92.3**|82.9|**75.0**|**57.4**|**76.9**|
|∆|**+2.3**|_−_2.5|**+4.6**|**+8.3**|**+3.2**|
|**WidowX Robot**|**Put Spoon**<br>**on Towel**|**Put Carrot**<br>**on Plate**|**Stack Green Block**<br>**on Yellow Block**|**Put Eggplant**<br>**in Yellow Basket**|**Average**|
|SpatialVLA [8] (_RSS’25_)|16.7|25.0|29.2|**100.0**|42.7|
|**_w/_ AWARE** (_Ours_)|**20.8**|**29.2**|**33.3**|95.8|**44.8**|
|∆|**+4.2**|**+4.2**|**+4.2**|_−_4.2|**+2.1**|


LIBERO [35], SIMPLER [36], and CALVIN [37]. Across these environments, we evaluate seven representative VLA backbones spanning model scales from 0.5B to 7B parameters: single-system models, including LLaVA-VLA (0.5B) [38], SpatialVLA (4B) [8], OpenVLA (7B) [4], and OpenVLA-OFT (7B) [6]; and dual-system architectures, including _π_ 0 (3B) [5], _π_ 0 _._ 5 (3B) [34], and CogACT (7B) [16]. All base policies and AWARE are evaluated on NVIDIA A100 GPUs using official checkpoints under identical environments, initial states, and pipelines. In all experiments, AWARE operates entirely training-free at test time without additional observation cues or learnable parameters. To reflect practical deployment across tasks with diverse horizons and precision demands, the intervention strength _α ∈_ [0 _._ 01 _,_ 0 _._ 10] is calibrated per task suite, with ablation sweeps in Section IV-C confirming that policy gains remain robust across a broad interior range. 

**LIBERO.** Table I reports policy performance across the four suites of the LIBERO benchmark [35] (Spatial, Object, Goal, and Long), each comprising ten manipulation tasks tested over 500 episodes per suite. Across all four heterogeneous VLA backbones, AWARE consistently improves manipulation success over untouched base policies. Because extended temporal horizons exacerbate visual representation fading, the benefits of AWARE are especially pronounced on LIBERO-Long: 

boosting OpenVLA by an absolute 7.6%, _π_ 0 by 2.8%, _π_ 0 _._ 5 by 1.4%, and OpenVLA-OFT to 96.0%. On near-saturated suites such as Spatial, Object, and Goal, the uncertainty-guided weighting naturally scales down intervention on confident tokens, steadily advancing performance toward ceiling (e.g., reaching 99.2% on Spatial) without inducing regressions. These across-the-board gains confirm that associative observation retrieval provides a robust, training-free mechanism benefiting both autoregressive and flow-matching policies. **SIMPLER.** As summarized in Table II, we assess crossembodiment generalization under visual matching on the SIMPLER benchmark [36] across two distinct robot platforms: dual-system CogACT (7B) [16] on Google Robot and SpatialVLA (4B) [8] on WidowX BridgeData. On Google Robot, AWARE raises CogACT’s average success to 76.9%, with the most substantial boost (+8.3%) achieved on the multi-stage task _Open Top Drawer and Place Apple_ , where precise visual relocalization is essential for gripper alignment. On WidowX, AWARE lifts SpatialVLA to 44.8% across 96 paired evaluations, achieving seven wins against five losses across initial configurations. These gains confirm that AWARE generalises seamlessly across diverse robot kinematics, observation viewpoints, and control frequencies without modifying official deployment pipelines. **CALVIN.** Table III evaluates multi-stage sequential manipu- 


Fig. 3: Real-world experimental setup and manipulation results. Top: Franka Research 3 robot workstation (left) and the five evaluated manipulation tasks (right). Bottom: Task success rates across five representative VLA backbones comparing baseline policies with _w/_ AWARE over 40 physical rollouts per task (2,000 trials total). Intervention strengths are _α_ =0 _._ 01 for LLaVA-VLA, _α_ =0 _._ 04 for OpenVLA-OFT, _α_ =0 _._ 05 for CogACT, and _α_ =0 _._ 03 for _π_ 0 and _π_ 0 _._ 5. 

TABLE III: Performance comparison on the CALVIN ABC _→_ D benchmark, in success rate per chain length and average completed length. Evaluated with the released checkpoint; a single strength _α_ =0 _._ 01 is used across the entire benchmark. 

|**Method**|**1/5**|**Succes**<br>**2/5**|**s Rat**<br>**3/5**|**e (%)**<br>**4/5**|**5/5**|**Avg. Len**|
|---|---|---|---|---|---|---|
|LLaVA-VLA [38] (_ICRA’26_)|94.0|82.4|68.2|57.8|47.0|3.49|
|**_w/_ AWARE** (_Ours_)|**94.4 **|**82.8 **|**72.4 **|**62.8 **|**50.4**|**3.63**|
|∆|**+0.4**|**+0.4**|**+4.2**|**+5.0**|**+3.4**|**+0.14**|


lation on the CALVIN ABC _→_ D benchmark [37], testing zero-shot generalization across 500 language-conditioned task chains with the compact LLaVA-VLA backbone [38]. Although base policies achieve high initial success on early subtasks, compounding spatial drift typically causes steep failure cascades at deeper chain stages. Crucially, AWARE provides increasingly pronounced gains as task depth increases, mitigating compounding failure cascades and boosting subtask success by 4.2% at chain length 3, 5.0% at length 4, and 3.4% at length 5. Consequently, the complete five-subtask chain completion rate rises to 50.4%, and the average completed chain length increases to 3.628 subtasks. This confirms that targeted associative retrieval effectively counteracts perceptual fading over extended horizons, even within a compact 0.5B parameter policy. 

## _B. Real-World Experiments_ 

**Real-World Setup.** We perform real-robot experiments to validate the effectiveness of AWARE in the real world. As 

illustrated in Fig. 3 (top), our workstation comprises a Franka Research 3 manipulator with a parallel-jaw gripper, a static overhead ZED 2i camera, and a 3Dconnexion 3D mouse. We evaluate on five diverse tasks: 1) _Put Corn on Pink Plate_ , 2) _Press Yellow Button then Blue_ , 3) _Cover Blue Block with the Box_ , 4) _Lift Corn onto Upper Rack Shelf_ , and 5) _Move Tomato from Turntable to Plate_ , spanning short-horizon placement, sequential button pressing, obstacle occlusion, multi-tier precision lifting, and dynamic moving-target acquisition. For each task, we collect 50 teleoperated demonstrations to finetune in-domain checkpoints. We evaluate five representative policy backbones (LLaVA-VLA, OpenVLA-OFT, CogACT, _π_ 0, and _π_ 0 _._ 5) across 40 physical rollouts per task under randomized layouts and initial poses, totaling 2,000 realworld evaluation trials. 

**Results.** Figure 3 summarizes physical evaluation results across all five policy backbones under a fixed intervention strength per model family. Across all architectures, AWARE consistently enhances physical manipulation, yielding average success gains ranging from +4.0% on high-capacity _π_ 0 _._ 5 to +8.0% on compact LLaVA-VLA. Out of 25 evaluated taskmodel combinations, AWARE achieves positive improvements in 17 settings, reaching an absolute peak of 95.0% on _Put Corn on Pink Plate_ with _π_ 0 _._ 5 and a maximum single-task boost of +17.5% on _Cover Blue Block with the Box_ using OpenVLA-OFT. Lower-capacity policies gain substantial headroom on challenging contact-rich tasks (e.g., a 15.0% improvement on sequential button pressing with LLaVAVLA), while saturated policies maintain steady progress near performance ceilings. Neutral outcomes in four bound- 

TABLE IV: Component analysis on the LIBERO benchmark with OpenVLA-OFT using the baseline strengths from Table I. Ablating individual components isolates the contribution of each design choice while holding the global intervention scale _α_ fixed. 

|**Part **|**of the ru**|**le kept**||**Succ**|**ess rat**|**e (%)**||
|---|---|---|---|---|---|---|---|
|**Per-element**<br>**weight**|**Depth**<br>**factor**|**Instruction**<br>**guidance**|**Spatial**|**Object**|**Goal**|**Long**|**Average**|
|_×_|_×_|_×_|98.0|98.2|97.6|93.8|96.9|
|_×_|✓|✓|98.8|97.0|98.4|95.2|97.4|
|✓|_×_|✓|98.2|97.2|97.8|94.8|97.0|
|✓|✓|_×_|98.6|96.6|98.4|95.2|97.2|
|✓|✓|✓|**99.2**|**98.6**|**98.6**|**96.0**|**98.1**|


TABLE V: Diagnostic variants on OpenVLA-OFT (LIBEROLong) testing alternative explanations across 500 evaluation episodes. 

|**Tested aspect**|**Evaluated variant**|**Succ. (%)**|**∆(%)**|
|---|---|---|---|
|Rf|OpenVLA-OFT (Base)|93.8|–|
|eerence|**AWARE (Ours)**|**96.0**|**+2.2**|
|Uncertainty routing|Linear chunk schedule (_w ∝k/H_)<br>Permuted entropy weights|94.0<br>94.8|+0.2<br>+1.0|
||Unrelated episode memory|94.8|+1.0|
|Injected content|Matched Gaussian noise|94.6|+0.8|
||FFN damping w/o injection|94.0|+0.2|


ary cases and slight trade-offs under high-speed turntable dynamics reflect authentic physical challenges under fixed parameters, confirming that AWARE delivers generalizable, training-free robustness in real-world robotic manipulation. 

## _C. Ablation Studies_ 

Focusing on OpenVLA-OFT, our ablation studies investigate three core aspects of AWARE: component contributions in Table IV, mechanistic validations in Table V, and sensitivity to the intervention strength _α_ in Fig. 4. 

**Component Analysis.** Table IV isolates each core component of AWARE with global scale _α_ fixed. The full method achieves 98.1% average success, with all elements contributing complementarily. Replacing element-specific entropy with uniform weights reduces success to 97.4%, confirming the necessity of fine-grained allocation. Ablating the depth schedule _ℓ/_ ( _L−_ 1) causes the sharpest drop (to 97.0%), demonstrating that intervention is crucial where observation grounding decays. Omitting instruction conditioning reduces success to 97.2%, verifying its distractor filtering role. Across suites, LIBERO-Object is most sensitive (dropping _≥_ 1 _._ 4% under any ablation), reflecting strict reliance on precise perceptual grounding. 

**Mechanistic Analysis.** To isolate the driver of policy gains, Table V benchmarks five diagnostic variants on LIBEROLong. First, replacing Action Entropy with a linear chunk schedule ( _w ∝ k/H_ ) yields only +0.2%, showing dynamic uncertainty cannot be replaced by a fixed schedule. Second, permuting entropy weights across action dimensions halves the gain (+1.0%), confirming features must target genuinely uncertain dimensions. Third, retrieving memory features from 


Fig. 4: **Impact of the strength** _α_ **.** Success rate per suite across the parameter grid; _α_ =0 denotes the untouched baseline policy, and outlined markers denote the optimal operating points for each suite (reported in Table I). 

TABLE VI: Inference latency and throughput on OpenVLAOFT (LIBERO-Long) evaluated on a single NVIDIA A100 GPU. Because the policy predicts action chunks of horizon _H_ = 8, per-step latency reflects the effective wait time per environment interaction step. 

|**Method**|**Throughput** _↑_|**Per call** _↓_|**Per env. step** _↓_|
|---|---|---|---|
|OpenVLA-OFT|82.9 Hz|96.5 ms|29.4 ms|
|w/ AWARE|68.1 Hz|117.5 ms|32.0 ms|
|∆|_−_17_._9%|+21_._8%|+8_._9%|


an unrelated episode recovers only +1.0%, showing generic visual tokens do not suffice. Fourth, injecting norm-matched Gaussian noise yields merely +0.8%, ruling out random perturbation. Finally, retaining native FFN damping ((1 _−w_ ) FFN) without injection gives +0.2%, showing suppression alone is insufficient. Together, these results confirm that AWARE specifically routes authentic visual evidence to high-entropy action dimensions. 

**Sensitivity to Strength** _α_ **.** Sweeping _α ∈_ [0 _._ 01 _,_ 0 _._ 10] for OpenVLA-OFT and _π_ 0 (Fig. 4) reveals a shared optimum at _α_ =0 _._ 03 on LIBERO-Long (+2.2% and +2.8%, respectively). Crucially, adopting a single default _α_ =0 _._ 03 across suites outperforms base policies without per-task tuning, confirming gains do not rely on oracle search. Saturated suites remain stable ( _α ∈_ [0 _._ 01 _,_ 0 _._ 05]), while larger strengths ( _α ≥_ 0 _._ 06) degrade precision. Autoregressive models similarly favor conservative scales ( _α ≤_ 0 _._ 03 for OpenVLA, _α_ =0 _._ 01 for LLaVA-VLA) to avoid over-perturbation. 

## _D. Inference Overhead_ 

AWARE introduces minimal computational overhead by design. Instruction weighting **_g_** _t_ is computed once per policy call, and observation features **_O_** _t_ are pre-cached. At each layer, computing _Ht,n_<sup>(</sup><sup>_ℓ_)andassociativeretrievaloperatestrictlyon</sup> the compact action subset ( _Na ≪ N_ , e.g., 56 action elements vs. _∼_ 1000 multimodal tokens). Rather than evaluating heavy self-attention across all _N_ tokens, AWARE requires only two lightweight matrix multiplications per layer. Benchmarks in Table VI confirm that on OpenVLA-OFT, AWARE adds merely 2.6 ms per environment interaction step (+8 _._ 9%, 29.4 ms to 32.0 ms), sustaining 68.1 Hz throughput and 

preserving real-time control feasibility. 

## V. CONCLUSION 

We have presented AWARE, a lightweight, training-free associative memory retrieval framework for Vision-LanguageAction (VLA) models. Motivated by the observation that action representations lose observation grounding across depth while predictive uncertainty converges asynchronously across dimensions, AWARE employs an element-wise Action Entropy metric to selectively retrieve instruction-guided observation evidence into high-entropy action dimensions via native feed-forward networks. Across seven diverse VLA backbones on LIBERO, SIMPLER, CALVIN, and realworld robots, AWARE consistently improves task execution success on extended-horizon manipulation with negligible computational overhead, offering a practical plug-and-play foundation for robust robot control. 

## REFERENCES 

- [1] L. Beyer, A. Steiner, A. S. Pinto, A. Kolesnikov, X. Wang, D. Salz, M. Neumann, I. Alabdulmohsin, M. Tschannen, E. Bugliarello _et al._ , “Paligemma: A versatile 3b vlm for transfer,” _arXiv preprint arXiv:2407.07726_ , 2024. 

- [2] S. Bai, K. Chen, X. Liu, J. Wang, W. Ge, S. Song, K. Dang, P. Wang, S. Wang, J. Tang _et al._ , “Qwen2. 5-vl technical report,” _arXiv preprint arXiv:2502.13923_ , 2025. 

- [3] S. Karamcheti, S. Nair, A. Balakrishna, P. Liang, T. Kollar, and D. Sadigh, “Prismatic vlms: Investigating the design space of visuallyconditioned language models,” in _Forty-first International Conference on Machine Learning_ , 2024. 

- [4] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong _et al._ , “Openvla: An open-source vision-language-action model,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 2679–2713. 

- [5] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, L. X. Shi, J. Tanner, Q. Vuong, A. Walling, H. Wang, and U. Zhilinsky, “ _π_ 0: A vision-language-action flow model for general robot control,” 2024. [Online]. Available: https://arxiv.org/abs/2410.24164 

- [6] M. J. Kim, C. Finn, and P. Liang, “Fine-tuning vision-languageaction models: Optimizing speed and success,” _arXiv preprint arXiv:2502.19645_ , 2025. 

- [7] R. Zheng, Y. Liang, S. Huang, J. Gao, H. Daumé III, A. Kolobov, F. Huang, and J. Yang, “Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies,” _arXiv preprint arXiv:2412.10345_ , 2024. 

- [8] D. Qu, H. Song, Q. Chen, Y. Yao, X. Ye, Y. Ding, Z. Wang, J. Gu, B. Zhao, D. Wang _et al._ , “Spatialvla: Exploring spatial representations for visual-language-action model,” _arXiv preprint arXiv:2501.15830_ , 2025. 

- [9] V. Bhat, Y.-H. Lan, P. Krishnamurthy, R. Karri, and F. Khorrami, “3d cavla: Leveraging depth and 3d context to generalize vision language action models for unseen tasks,” _arXiv preprint arXiv:2505.05800_ , 2025. 

- [10] T. Lin, G. Li, Y. Zhong, Y. Zou, and B. Zhao, “Evo-0: Vision-languageaction model with implicit spatial understanding,” _arXiv preprint arXiv:2507.00416_ , 2025. 

- [11] Y. Dai, J. Lee, Y. Zhang, Z. Ma, J. Yang, A. Zadeh, C. Li, N. Fazeli, and J. Chai, “Aimbot: A simple auxiliary visual cue to enhance spatial awareness of visuomotor policies,” _arXiv preprint arXiv:2508.08113_ , 2025. 

- [12] M. Geva, R. Schuster, J. Berant, and O. Levy, “Transformer feedforward layers are key-value memories,” in _Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing_ , 2021, pp. 5484–5495. 

- [13] S. Jie, Y. Tang, N. Ding, Z.-H. Deng, K. Han, and Y. Wang, “Memoryspace visual prompting for efficient vision-language fine-tuning,” in _International Conference on Machine Learning_ . PMLR, 2024, pp. 22 062–22 074. 

- [14] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu _et al._ , “Rt-1: Robotics transformer for real-world control at scale,” _arXiv preprint arXiv:2212.06817_ , 2022. 

- [15] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

- [16] Q. Li, Y. Liang, Z. Wang, L. Luo, X. Chen, M. Liao, F. Wei, Y. Deng, S. Xu, Y. Zhang _et al._ , “Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation,” _arXiv preprint arXiv:2411.19650_ , 2024. 

- [17] P. Li, Y. Zhu, Y. Chen, Q. Ma, Y. Xu, J. Yang, H. Guan, Y. Huang, H. Wu, X. Ma _et al._ , “BridgeVLA++: A data-efficient, generalizable, and memory-augmented vision-language-action framework for 3d manipulation,” _arXiv preprint arXiv:2608.05042_ , 2026. 

- [18] Q. Vuong, S. Levine, H. R. Walke, K. Pertsch, A. Singh, R. Doshi, C. Xu, J. Luo, L. Tan, D. Shah _et al._ , “Open x-embodiment: Robotic learning datasets and rt-x models,” in _Towards Generalist Robots: Learning Paradigms for Scalable Skill Acquisition@ CoRL2023_ , 2023. 

- [19] D. Ghosh, H. R. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, J. Luo _et al._ , “Octo: An open-source generalist robot policy,” in _Robotics: Science and Systems_ , 2024. 

- [20] S. Ye, J. Jang, B. Jeon, S. J. Joo, J. Yang, B. Peng, A. Mandlekar, R. Tan, Y.-W. Chao, B. Y. Lin _et al._ , “Latent action pretraining from videos,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [21] Q. Bu, Y. Yang, J. Cai, S. Gao, G. Ren, M. Yao, P. Luo, and H. Li, “Univla: Learning to act anywhere with task-centric latent actions,” _arXiv preprint arXiv:2505.06111_ , 2025. 

- [22] Y. Chen, P. Li, Y. Huang, J. Yang, K. Chen, and L. Wang, “Ec-flow: Enabling versatile robotic manipulation from action-unlabeled videos via embodiment-centric flow,” _arXiv preprint arXiv:2507.06224_ , 2025. 

- [23] Y. Chen, P. Li, J. Yang, K. He, X. Wu, Y. Xu, K. Wang, J. Liu, N. Liu, Y. Huang, and L. Wang, “BridgeV2W: Bridging video generation models to embodied world models via embodiment masks,” _arXiv preprint arXiv:2602.03793_ , 2026. 

- [24] Y. Fang, Z. Yang, Z. Chen, Z. Zhao, and J. Zhou, “From uncertainty to trust: Enhancing reliability in vision-language models with uncertaintyguided dropout decoding,” _arXiv preprint arXiv:2412.06474_ , 2024. 

- [25] X. Zou, Y. Wang, Y. Yan, Y. Lyu, K. Zheng, S. Huang, J. Chen, P. Jiang, J. Liu, C. Tang _et al._ , “Look twice before you answer: Memoryspace visual retracing for hallucination mitigation in multimodal large language models,” _arXiv preprint arXiv:2410.03577_ , 2024. 

- [26] J. Yang, C. Cui, Y. Zhou, Y. Chen, P. Xia, Y. Wei, T. Yu, Y. Huang, and L. Wang, “Ikod: Mitigating visual attention degradation in large vision-language models,” _arXiv preprint arXiv:2508.03469_ , 2025. 

- [27] P. Valle, C. Lu, S. Ali, and A. Arrieta, “Evaluating uncertainty and quality of visual language action-enabled robots,” _arXiv preprint arXiv:2507.17049_ , 2025. 

- [28] U. B. Karli, T. Kurumisawa, and T. Fitzgerald, “Ask before you act: Token-level uncertainty for intervention in vision-language-action models,” in _Second Workshop on Out-of-Distribution Generalization in Robotics at RSS 2025_ , 2025. 

- [29] W. Song, Z. Zhou, H. Zhao, J. Chen, P. Ding, H. Yan, Y. Huang, F. Tang, D. Wang, and H. Li, “Reconvla: Reconstructive vision-language-action model as effective robot perceiver,” _arXiv preprint arXiv:2508.10333_ , 2025. 

- [30] X. Jia, B. Yang, Z. Ge, X. Nie, Y. Zhou, C. Fan, Y. Li, Y. Chai, C. Jing, Z. Liang, Q. Bu, H. Cao, C. Wu, Q. Li, Z. Yang, C. Zhang, H. Li, Z. Wu, J. Yan, and Y.-G. Jiang, “Guidedvla: Specifying task-relevant factors via plug-and-play action attention specialization,” _arXiv preprint arXiv:2605.12369_ , 2026. 

- [31] Y.-S. Chuang, Y. Xie, H. Luo, Y. Kim, J. R. Glass, and P. He, “Dola: Decoding by contrasting layers improves factuality in large language models,” in _International Conference on Learning Representations_ , vol. 2024, 2024, pp. 54 158–54 183. 

- [32] nostalgebraist, “Interpreting GPT: the logit lens,” https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/ interpreting-gpt-the-logit-lens, August 2020, accessed: 2025-02-22. 

- [33] N. Belrose, Z. Furman, L. Smith, D. Halawi, I. Ostrovsky, L. McKinney, S. Biderman, and J. Steinhardt, “Eliciting latent predictions from transformers with the tuned lens,” _arXiv preprint arXiv:2303.08112_ , 2023. 

- [34] K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, 

M. R. Equi, C. Finn, N. Fusai, M. Y. Galliker _et al._ , “ _π_ 0 _._ 5: a visionlanguage-action model with open-world generalization,” in _9th Annual Conference on Robot Learning_ , 2025. 

- [35] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “Libero: Benchmarking knowledge transfer for lifelong robot learning,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 44 776– 44 791, 2023. 

- [36] X. Li, K. Hsu, J. Gu, O. Mees, K. Pertsch, H. R. Walke, C. Fu, I. Lunawat, I. Sieh, S. Kirmani _et al._ , “Evaluating real-world robot manipulation policies in simulation,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 3705–3728. 

- [37] O. Mees, L. Hermann, E. Rosete-Beas, and W. Burgard, “Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 3, pp. 7327–7334, 2022. 

- [38] W. Song, J. Chen, X. Sun, H. Lei, Y. Qin, W. Zhao, P. Ding, H. Zhao, T. Wang, P. Hou, Z. Zhong, H. Yan, D. Wang, J. Ma, and H. Li, “Rethinking the practicality of vision-language-action model: A comprehensive benchmark and an improved baseline,” in _2026 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2026. 

