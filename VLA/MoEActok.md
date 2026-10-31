---
title: "MoEActok: A MoE-based Action Tokenizer for Vision-Language-Action Models"
date: "2026"
venue: "CVPR 2026"
url: https://openaccess.thecvf.com/content/CVPR2026/html/Xu_MoEActok_A_MoE-based_Action_Tokenizer_for_Vision-Language-Action_Models_CVPR_2026_paper.html
pdf: https://openaccess.thecvf.com/content/CVPR2026/papers/Xu_MoEActok_A_MoE-based_Action_Tokenizer_for_Vision-Language-Action_Models_CVPR_2026_paper.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://openaccess.thecvf.com/content/CVPR2026/papers/Xu_MoEActok_A_MoE-based_Action_Tokenizer_for_Vision-Language-Action_Models_CVPR_2026_paper.pdf)** / [論文ページ](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_MoEActok_A_MoE-based_Action_Tokenizer_for_Vision-Language-Action_Models_CVPR_2026_paper.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **MoEActok: A MoE-based Action Tokenizer for Vision-Language-Action Models** 

Chunpu Xu<sup>1</sup><sup>_,_3</sup> Zhixuan Liang<sup>4</sup> Tianshuo Yang<sup>4</sup> Chi-Min Chan<sup>5</sup> Yang Xiao<sup>1</sup> Jessie Wang<sup>1</sup> Xiaokang Yang<sup>2</sup> Yao Mu<sup>2</sup><sup>_,_3</sup><sup>_,_*</sup> 1PolyU 2SJTU 3Shanghai AI Laboratory 4HKU 5HKUST 

chun-pu.xu@connect.polyu.hk, muyao@sjtu.edu.cn 

## **Abstract** 

_Recent works on vision-language-action (VLA) models have made great progress in exploring action tokenizers that convert continuous control signals into discrete tokens to align with LLM/VLM training paradigms. These approaches typically train a single tokenizer over entire manipulation trajectories, which often comprise multiple distinct skills and thus pose a challenging optimization trade-off. To address this issue, we introduce_ **_MoEActok_** _, a novel_ **_act_** _ion_ **_tok_** _enizer that employs a mixture-of-experts (_ **_MoE_** _) quantizer to produce skill-aware discrete representations for VLA models. MoEActok utilizes a clustering-driven MoE VQ-VAE mechanism in which each expert specializes in a particular skill. The key components are: (a) an action-skill decoupling strategy that uses k-means clustering to group action chunks, aligning clusters having similar skills; (b) a skill-aware training paradigm that augments VLA models with skill-conditioned context, improving skill grounding; and (c) an adapter that projects shared encoder representations into skill-specific latent spaces for specialized quantization, and subsequently harmonize the heterogeneous quantized representations back into a unified space for coherent reconstruction by the shared decoder. We evaluate MoEActok-based VLA models against multiple prior action tokenizer baselines in the RoboTwin and Simpler-Env simulators, and further assess zero-shot transfer on three real-world tasks. Across both simulated and real-world settings, MoEActok-based VLA substantially outperforms existing discrete tokenization methods. Code is available at https://github.com/cpaaax/MoEActok._ 

## **1. Introduction** 

Vision-language-action (VLA) models [2, 3, 5, 11, 12, 17, 23, 26, 30, 32, 35] have revolutionized robotic manipulation by integrating multimodal inputs to generate executable action sequences, drawing on the success of large-scale pre- 

> *Corresponding author. 


Figure 1. Clustering results of actions on BridgeData V2. The seven dimensions (0-6) represent the robot end-effector actions: x, y, z coordinates for position, roll, pitch, yaw for orientation, and gripper action. 

training in language and vision domains [1, 9]. These models typically leverage autoregressive architectures [28] to predict latent discrete tokens, with or without a separate action decoder, that represent continuous robot actions, enabling efficient training and inference similar to those in large-language-models (LLMs) and large vision-languagemodels (VLMs). However, the effectiveness of such models relies on quality of action tokenization process, which distills high-dimensional, temporally coherent control signals into compact, semantically rich discrete representations. 

Early VLA approaches [3, 11, 35] rely on straightforward discretization techniques, such as uniform binning of individual action dimensions, which often struggle with the nuances of dexterous tasks due to their inability to capture inter-step dependencies. Recently, more advanced methods have introduced structured tokenization paradigms to mitigate the issue. For instance, FAST tokenizer [23] proposes frequency-domain transformations followed by byte-pair encoding to facilitate autoregressive prediction in challenging manipulation scenarios. Complementing this, residual 

28042 

VQ-VAE frameworks ( _i.e._ , VQ-BET [12], VQ-VLA [31]) employ multiple residual vector quantization layers to hierarchically transform action sequences into discrete tokens. 

Despite these notable advances in tokenization design for VLAs, a fundamental challenge persists that these tokenizers are trained holistically across full trajectories that integrate diverse and heterogeneous skills, such as coordinated movement and precise grasping. These approaches, while intuitively appealing for capturing end-to-end behaviors, inadvertently introduce representation conflicts as they require the model to learn from conflated signals. For example, in robotic manipulation tasks, a single trajectory might seamlessly blend translational locomotion with finegrained end-effector adjustments, imposing competing demands on the tokenizer’s capacity to process actions of different skills. As reflected by the clustering phenomenon in Figure 1 for action chunks from BridgeData V2 [29], this heterogeneity shows in distinct yet intermixed specialization patterns: clusters 0 and 1 predominantly capture movement primitives, with cluster 0 and cluster 1 corresponding to opposite rotations around the z-axis; in contrast, clusters 2 and 3 focus on grasping actions, where cluster 2 aligns with gripper-closing motions and cluster 3 with gripperopening motions. This mixed-signal optimization necessitates a compromise in representation fidelity, as a unified quantizer struggles to specialize in the distinct kinematic patterns and temporal scales of individual skills, resulting in suboptimal generalization. Moreover, without explicit mechanisms to disentangle skill-specific structures, downstream VLAs may underperform in grounding observations to precise action primitives. 

To address these challenges, we propose **MoEActok** , a mixture-of-experts (MoE) [7] action tokenizer that generates skill-specialized discrete tokens tailored for VLAs. Individual experts are specialized via k-means partitioning of action chunks into semantically coherent clusters. This ensures high intra-cluster similarity aligned with distinct skills, such as rotational movements or grasping primitives, while enabling dynamic routing to maintain representational compactness and fidelity. Complementing the model design, we propose an adapter that bridges shared and skill-specific latent spaces before and after quantization, enabling effective cross-skill representation learning. To further enhance skill grounding, we incorporate a skillaware training paradigm that conditions VLA models on skill clusters, enabling hierarchical prediction from coarsegrained skill categories to fine-grained action tokens. This strategy mitigates optimization conflicts, promotes modular generalization, and improves the alignment of observations with precise action primitives. 

To validate the effectiveness of the proposed method, we conduct experiments on two widely used simulators, including RoboTwin [6] and Simpler-Env [14]. Moreover, we 

perform zero-shot experiments with real robots to evaluate the effectiveness of using VLAs trained with collected data from RoboTwin, directly on tasks in the real world. In summary, our work makes the following key contributions: 

- We introduce MoEActok, a novel mixture-of-experts tokenizer that decomposes action discretization into skillspecific quantization, where each expert specializes in encoding actions from different behavioral clusters identified through unsupervised learning clustering. 

- We propose a skill-aware training paradigm that can augment VLAs with coarse-to-fine action prediction. 

- We develop an adapter that aligns representations between the unified encoder-decoder architecture and specialized expert quantizers, facilitating coherent action reconstruction. 

- We carried out comprehensive experiments in both simulated and zero-shot real-world settings to showcase the effectiveness of the proposed approach. 

## **2. Related Work** 

### **2.1. Vision-Language-Action Models** 

Vision-language-action (VLA) models have rapidly evolved into a cornerstone for endowing robots with versatile manipulation capabilities, bridging the gap between highlevel semantic understanding and low-level physical execution [2, 3, 5, 21, 25, 32, 35]. By leveraging the pre-trained representations from large language models (LLMs) and vision-language models (VLMs), these architectures enable robots to interpret natural language instructions alongside visual inputs, generating coherent action sequences for complex tasks. Pioneering efforts like CLIPort [25] and PerAct [21] laid the groundwork by fusing CLIP-encoded vision with modular policy networks to handle languageguided object interactions. Subsequent advancements in the RT family [2, 3, 35] scaled this paradigm through massive internet-scale pre-training, introducing discrete action representations that facilitate efficient fine-tuning on robotspecific data. Building on these foundations, contemporary VLA systems emphasize broad generalization and multitask proficiency. For instance, Octo [26] introduced an expansive dataset spanning diverse robot embodiments, fostering policies that adapt across varied hardware setups. Similarly, OpenVLA [11] demonstrated robust zero-shot transfer to real-world household scenarios by distilling VLMs into compact action predictors. 

### **2.2. Action Tokenization** 

Central to the success of these autoregressive VLAs is the design of action tokenization schemes, which transform raw, multidimensional trajectories into discrete sequences amenable to next-token prediction [24]. Traditional approaches often rely on uniform binning, discretizing each 

28043 

action dimension independently at every timestep [3, 11, 35]. While computationally lightweight, this method struggles with temporal correlations in high-dimensional spaces, leading to redundant tokens and suboptimal learning, particularly for smooth, predictive motion patterns. To address these limitations, researchers have turned to more sophisticated compression techniques that exploit the inherent structure of action signals. Vector quantization (VQ) emerges as a promising direction, enabling latent space clustering for compact representations [12, 31]. For example, VQ-VLA [31] advances this by training convolutional residual VQ-VAEs on scaled datasets, blending realworld noisy trajectories with vast synthetic simulations to yield tokenizers that enhance long-horizon planning. Complementing this, FAST [23] draws from signal processing roots, applying discrete cosine transforms (DCT) to shift actions into a frequency domain before employing bytepair encoding (BPE) for iterative merging of correlated coefficients. However, none of these works take into consideration decoupling heterogeneous action skills, such as precise grasping versus broad movement, into specialized representations, often resulting in entangled latent spaces that hinder fine-grained control. In this work, we address this gap by introducing a novel tokenizer that leverages multiple experts to modularly learn and disentangle diverse skill distributions, enabling more adaptive action generation for diverse robotic tasks. Several recent works bypass action tokenization entirely by generating continuous actions through alternative decoding strategies, such as diffusion heads [4, 8, 10, 13, 15, 16, 18, 19, 22]. While effective, the majority of these approaches require architectural modifications incompatible with standard autoregressive transformers. In contrast, our tokenization-based method seamlessly integrates with existing LLMs, preserving their architectural benefits without structural changes. 

## **3. Method** 

### **3.1. Problem Formulation** 

In this work, we explore a comprehensive robotic manipulation dataset denoted as _D_ = _{{_ ( _o_ 1 _, s_ 1 _, a_ 1) _, ...,_ ( _oTi, sTi, aTi_ ) _, Lm,i}_<sup>_N_</sup> _i_ =1<sup>_m}_</sup> _m_<sup>_M_</sup> =1<sup>,</sup> which consists of _M_ distinct manipulation scenarios. In the _m_<sup>th</sup> scenario, there are _Nm_ demonstration trajectories. The _i_<sup>th</sup> trajectory spans _Ti_ timesteps, where at each timestep _t_ , we record: an RGB frame _ot_ capturing the environmental view, the robot’s proprioceptive state _st_ , and the executed control action _at_ . To elaborate on the details of _at_ , we take the actions in BridgeDataV2 [29] as an example. The robot arm operates with 7 Degrees of Freedom (DoF), and _at ∈_ R<sup>7</sup> is represented by a 7-dimensional vector. In this vector, the first six dimensions correspond to the positional coordinates (x, y, z) and the rotational angles (roll, pitch, 

yaw). The final dimension pertains to the gripper’s action, where a value of 1 indicates an open action and a value of 0 means a closed action. Accompanying each sequence is a concise natural language sentence _Lm,i_ that describes the objective of the scenario. The overarching aim is to derive an end-to-end policy _πϕ_ ( _at_ : _t_ + _k−_ 1 _|ot, st, l_ ) capable of generating _k_ -step action chunks directly from visual observation, proprioceptive states, and instruction text. 

### **3.2. Action-Skill Decoupling** 

MoEActok training relies on a mixture-of-experts architecture, where each expert focuses on one group of actions. Therefore, partitioning action chunks across trajectories into semantically distinct groups is necessary. As supported by the action clustering results shown in Figure 1, actions exhibit clear clustering patterns based on the seven dimensions of actions, demonstrating that actions naturally form distinct groups. Importantly, such kinematic-based grouping is more conducive to model learning and generalization, as it reflects the underlying structure of manipulation primitives. Therefore, we propose an efficient, unsupervised clustering procedure that automatically categorizes action chunks based on their inherent features. 

For an input action chunk _at_ : _t_ + _k−_ 1 _∈_ R<sup>_k×_7</sup> , we derive a compact global representation ¯ _a ∈_ R<sup>7</sup> that encapsulates the chunk’s aggregate dynamics. The initial 6 dimensions aggregate the cumulative arm motion via element-wise summation: _a_ ¯1:6 =<sup>�</sup><sup>_t_</sup> _j_<sup>+</sup> =<sup>_k_</sup> _t_<sup>_−_1</sup> _aj,_ 1:6. Meanwhile, the seventh dimension quantifies net gripper displacement as the endpoint difference: _a_ ¯7 = _at_ + _k−_ 1 _,_ 7 _− at,_ 7. This design ensures that the first six dimensions of _a_ ¯ encapsulate the aggregate arm kinematics across the chunk. In contrast, the seventh dimension isolates the gripper action, thereby disentangling translational and end-effector primitives. We then apply the _k_ -means clustering algorithm to these derived global chunk representations, yielding _K_ distinct cluster centroids. Each cluster is interpreted as a specialized skill category. 

### **3.3. MoEActok Tokenizer** 

Building upon the action-skill decoupling framework established above, we introduce MoEActok, a novel mixtureof-experts tokenizer that leverages the identified skill clusters to achieve more effective action representation learning. Our tokenization architecture is fundamentally grounded in vector quantization principles, extending variational autoencoder methodologies [27] with a multi-expert paradigm tailored for heterogeneous skill distributions. The core architecture consists of three interconnected components: a shared encoding module, a mixture-of-experts quantization layer, and a unified decoding module. The encoder and decoder employ a hybrid architectural design that synergistically combines convolutional neural networks with multi-head transformer layers, enabling both local tempo- 

28044 


Figure 2. Overview of MoEActok action tokenizer (top) and the MoEActok-based VLA model (bottom). 

ral pattern extraction and long-range dependency modeling. Specifically, the encoder transforms input action chunks _at_ : _t_ + _k−_ 1 into compressed latent representations _z_ that capture essential behavioral patterns. 

The key innovation lies in our mixture-of-experts quantization module, which addresses the fundamental limitation that a single quantizer struggles to optimally represent the diverse distributional characteristics inherent across different skill categories. Motivated by our _K_ -cluster action-skill decomposition, we deploy _K_ specialized vector quantizers _{V Q_ 1 _, V Q_ 2 _, ..., V QK}_ where each quantizer _V Qi_ maintains its own codebooks. During quantization, the skill category _h_ derived from the clustering procedure directs the latent representation _z_ to the related expert quantizer, ensuring that each skill-specific quantizer can specialize in capturing the nuanced patterns within its designated action category. Formally, given a latent representation _z_ and its associated skill category _h ∈{_ 1 _,_ 2 _, ..., K}_ , _z_ is transformed into discrete tokens through the quantization process as follows: 


where _q_ is the quantized index, _zq_ is the corresponding embedding vector from the related codebook of _V Qh_ . 

_zq_ is subsequently processed by the decoder to reconstruct the original action chunk _at_ : _t_ + _k−_ 1. This design ensures that each quantizer can develop specialized representations optimized for its respective skill domain. 

Furthermore, given that each quantizer specializes in distinct action skill clusters with potentially disparate latent 

distributions, we introduce a skill-adaptive mapping mechanism to ensure optimal feature alignment across the heterogeneous expert domains. This mechanism comprises two complementary components: a pre-quantization adapter **_A_**<sup>_pre_</sup> _h_ and a post-quantization adapter **_A_**<sup>_post_</sup> _h_ . The prequantization adapter **_A_**<sup>_pre_</sup> _h_ transforms the shared encoder representation _z_ into a skill-specific latent space tailored for quantizer _V Qh_ : 


where _W_ 1, _W_ 2, _W_ 3, _W_ 4 denote trainable linear transformation matrices, _σ_ 1 and _σ_ 2 are the ReLU activation function. 

This transformation enables each expert quantizer to operate within its specialized representational subspace, where the codebook embeddings are optimally positioned to capture skill-specific behavioral patterns. The skillspecific latent representation _z_<sup>_′_</sup> is then quantized using the corresponding expert quantizer to obtain the discrete index _q_ and the retrieved quantized embedding _zq_ . 

Conversely, the post-quantization adapter **_A_**<sup>_post_</sup> _h_ , which employs an identical architectural structure as its prequantization adapter, maps the _zq_ back to a unified latent space compatible with the shared decoder: 


where _zq_<sup>_′_is sent to the decoder for reconstruction.</sup> 

To optimize our MoEActok tokenizer, we follow VQVAE [27] and adopt a multi-objective training paradigm that combines three complementary loss components. The 

28045 

primary objective is the reconstruction fidelity loss _Lrec_ , which enforces semantic consistency between the original input action chunks _at_ : _t_ + _k−_ 1 and their decoded action _a_ ˆ _t_ : _t_ + _k−_ 1: 


This loss ensures that the entire encode-quantize-decode pipeline preserves the essential kinematic information necessary for faithful action reproduction. 

The second component is the codebook optimization loss _Lemb_ , which facilitates the learning of meaningful discrete representations within each expert’s codebook. This loss minimizes the distance between the skill-adapted encoder output _z_<sup>_′_</sup> and its nearest quantized embedding _zq_ : 


where _sg_ [ _·_ ] denotes the stop-gradient operator, ensuring that gradients flow only to the codebook parameters and not back through the encoder during this optimization step. 

The third component is the encoder commitment loss _Lcom_ , which stabilizes the training dynamics by encouraging the encoder to produce representations that align closely with the selected codebook vectors, thereby mitigating erratic switching between different discrete codes: 


The overall training objective combines these three components with the weighting factors: 


where _α_ and _β_ are hyperparameters that balance the relative importance of codebook learning and encoder stability, respectively. 

### **3.4. Skill-Aware VLA Training** 

Our objective is to develop a unified vision-language-action policy _πϕ_ ( _at_ : _t_ + _k−_ 1 _|ot, st, l_ ) that can seamlessly integrate multimodal inputs to generate coherent action sequences for different manipulation tasks. 

To enable effective cross-modal learning within a single transformer architecture, we establish a comprehensive tokenization pipeline that converts each input modality into discrete token sequences while preserving semantic integrity. For linguistic instruction _l_ , we leverage the LLM’s native tokenization scheme to obtain textual tokens. Proprioceptive state _st_ is discretized into 256 bins per state dimension following FAST [23]. Visual observation _ot_ is processed through SigLIP-SO400M [34], yielding 256 continuous visual tokens that encode spatial-semantic information. Action sequences are tokenized to discrete tokens _{qr}_<sup>_R_</sup> _r_ =1<sup>using our proposed MoEActok, transforming</sup> 

continuous action chunks into discrete action tokens. To maintain clear modality boundaries, we introduce special delimiter tokens, where t ~~b~~ os/t ~~e~~ os for textual segments, s ~~b~~ os/s ~~e~~ os for proprioceptive state information, i ~~b~~ os/i ~~e~~ os for image content, and a ~~b~~ os/a ~~e~~ os for action sequences. 

Given the multimodal tokenized inputs, the standard VLA training follows an autoregressive objective using cross-entropy loss: 


where _qr_ represents the _r_ -th action token, _q<r_ denotes the preceding action token sequence. 

However, this conventional training approach presents a fundamental challenge. The action tokens originate from distinct skill clusters identified during our action-skill decoupling procedure, yet the model needs to implicitly infer the appropriate skill category and generate corresponding tokens during inference without explicit skill guidance. This implicit skill reasoning significantly complicates the learning process, as the model must simultaneously solve skill classification and action prediction tasks within a single objective. To address this limitation, we propose a skillaware VLA training paradigm that explicitly incorporates the skill clusters _h ∈{_ 1 _,_ 2 _, ..., K}_ obtained from our unsupervised clustering procedure. This approach decomposes the action generation process into two interpretable stages, i.e., skill identification followed by skill-conditioned action prediction. 

The enhanced training objective is reformulated as: 


The first term enforces explicit skill classification capability, requiring the model to predict the appropriate skill cluster _h_ based on the current context. The second term conditions action token generation on both the contextual inputs and the predicted skill category, enabling the model to leverage skill-specific behavioral patterns learned by the corresponding expert quantizer. 

## **4. Experiments** 

We evaluate our method on two simulation environments, RoboTwin [6] and Simpler-Env [14], as well as on a realworld AgileX Cobot Magic robot. 

### **4.1. Simulation Benchmarks** 

**RoboTwin.** RoboTwin is a comprehensive bimanual manipulation benchmark designed to facilitate scalable dataset 

28046 

Table 1. Success rates of different VLAs across RoboTwin simulation 12 tasks. 

|**Tokenizer**|**Beat Block**<br>**Hammer**|**Move Playingcard**<br>**Away**|**Pick Diverse**<br>**Bottles**|**Move Can**<br>**Pot**|**Move Pillbottle**<br>**Pad**|**Click Bell**|**Handover Mic**|
|---|---|---|---|---|---|---|---|
|**Binning**|0.11|0.01|**0.27**|0.02|0.00|0.67|0.85|
|**FAST**|0.00|0.18|0.06|0.08|0.01|0.68|0.17|
|**VQ-BET**|0.10|0.27|0.12|0.13|0.06|0.64|0.59|
|**VQ-VLA**|0.14|0.46|0.24|0.30|0.20|0.59|0.93|
|**MoEActok**|**0.26**|**0.65**|0.15|**0.50**|**0.29**|**0.85**|**0.95**|
|**Tokenizer**|**Place Mouse**<br>**Pad**|**Place Container**<br>**Plate**|**Place Phone**<br>**Stand**|**Place Burger**<br>**Fries**|**Shake Bottle**|**Average**|**Success Rate**|
|**Binning**|0.00|0.00|0.02|0.01|0.92||0.24|
|**FAST**|0.01|0.07|0.01|0.00|0.76||0.17|
|**VQ-BET**|0.00|0.54|0.04|0.15|0.87||0.29|
|**VQ-VLA**|0.08|0.79|0.23|0.52|0.96||0.45|
|**MoEActok**|**0.23**|**0.88**|**0.38**|**0.59**|**0.98**||**0.56**|


Table 2. Success rates of different VLAs across Simpler-Env simulation 4 tasks. 

|**Tokenizer**|**Put Spoon**<br>**on Towel**|**Put Carrot**<br>**on Plate**|**Stack Green**<br>**on Yellow**|**Put Eggplant**<br>**in Basket**|**Avg.**|
|---|---|---|---|---|---|
|**Bining**|0.08|0.00|0.00|0.04|0.03|
|**FAST**|0.21|0.17|0.00|0.08|0.12|
|**VQ-BET**|0.04|0.04|0.00|0.00|0.02|
|**VQ-VLA**|0.29|0.33|**0.21**|0.00|0.21|
|**MoEActok**|**0.38**|**0.38**|0.13|**0.63**|**0.38**|


**ning** [11] uniformly discretizes each action dimension into 256 bins per timestep; (2) **FAST** [23] applies Discrete Cosine Transform (DCT) to convert actions to the frequency domain, then uses Byte-Pair Encoding (BPE); (3) **VQBET** [12] employs MLPs for feature encoding followed by two-layer Residual Vector Quantization (RVQ); (4) **VQVLA** [31] leverages a convolutional residual VQ-VAE architecture to discretize continuous actions. 

generation with high-fidelity demonstrations and standardized evaluation protocols. The benchmark encompasses diverse manipulation tasks spanning various skill categories, including Click Bell, Place Container Plate, Pick Diverse Bottles, Move Pillbottle Pad, etc. We collect 1,600 expert demonstrations for each task, yielding a total corpus of 19,200 trajectories across 12 task categories. To enhance dataset diversity and model robustness against environmental variations, we employ domain randomization techniques during data collection following the RoboTwin [6]. We adopt the task success rate as the evaluation metric. 

**Simpler-Env.** SimplerEnv mitigates the real-to-sim control and visual gaps inherent in simulated manipulation environments, enabling more accurate evaluation of robotic policies that closely mirror their real-world performance and behavior. We focus on four WidowX robot tasks, and they are Put Carrot on Plate, Put Spoon on Towel, Stack Green on Yellow, and Put Eggplant in Basket. Training data is sourced from the BridgeV2 dataset [29]. Following prior works, we report the trajectory success rate. 

### **4.2. Baselines and Training Details** 

**Baselines.** We compare our MoEActok tokenizer against four representative action tokenization methods: (1) **Bin-** 

**Training Details.** To ensure controlled comparison, all tokenizers are integrated into an identical VLA architecture (Figure 2) with Qwen2.5-0.5B [33] as the LLM backbone. Our MoEActok uses 4 expert quantizers with codebook dimension 2048. Action chunks are configured with temporal horizons of 8 steps for RoboTwin and 4 steps for BridgeV2. Given 7-dimensional per-arm control vectors, this results in 14-dimensional inputs for bimanual RoboTwin tasks and 7- dimensional inputs for single-arm BridgeV2 tasks. Training proceeds in two stages: First, MoEActok is pre-trained using AdamW [20] with learning rate 5 _×_ 10<sup>_−_5</sup> . Second, for VLA policy learning, we freeze both MoEActok and SigLIP parameters while fine-tuning the LLM and MLP projectors using AdamW with initial learning rate 1 _×_ 10<sup>_−_4</sup> and cosine annealing. VLAs train for 10 epochs on RoboTwin and 20 epochs on BridgeV2 data. 

### **4.3. Evaluation results on Simulation Benchmarks** 

**RoboTwin Results.** Our MoEActok-based VLA achieves the highest overall success rate of 0.56, representing a substantial improvement over competing tokenization approaches. Specifically, we observe significant performance gains compared to the binning-based VLA (0.24), FASTbased VLA (0.17), and existing VQ-VAE variants, including VQ-BET (0.29) and VQ-VLA (0.45). Our method attains superior results across the majority of evaluated tasks, 

28047 


Figure 3. Real-world manipulation visualizations for “Click Bell” and “Place Container Plate” tasks. Table 3. Results of ablation study on RoboTwin benchmark. 

|**Tokenizer**|**Beat Block**<br>**Hammer**|**Move Playingcard**<br>**Away**|**Pick Diverse**<br>**Bottles**|**Move Can**<br>**Pot**|**Move Pillbottle**<br>**Pad**|**Click Bell**|<br>**Handover Mic**|
|---|---|---|---|---|---|---|---|
|**MoEActok**|0.26|0.65|0.15|0.50|0.29|0.85|0.95|
|**w/o Adapter**|0.13|0.58|0.16|0.41|0.19|0.58|0.92|
|**w/o Skill-aware**|0.16|0.51|0.13|0.53|0.26|0.52|0.99|
|**Tokenizer**|**Place Mouse**<br>**Pad**|**Place Container**<br>**Plate**|**Place Phone**<br>**Stand**|**Place Burger**<br>**Fries**|**Shake Bottle**|**Avera**|**ge Success**|
|**MoEActok**|0.23|0.88|0.38|0.59|0.98||0.56|
|**w/o Adapter**|0.19|0.77|0.17|0.47|0.89||0.45|
|**w/o Skill-aware**|0.07|0.85|0.29|0.44|0.88||0.47|


Table 4. Results of ablation study on Simpler-Env benchmark. 

|**Tokenizer**|**Put Spoon**<br>**on Towel**|**Put Carrot**<br>**on Plate**|**Stack Green**<br>**on Yellow**|**Put Eggplant**<br>**in Basket**|**Avg.**|
|---|---|---|---|---|---|
|**MoEActok**|0.38|0.38|0.13|0.63|0.38|
|**w/o Adapter**|0.33|0.21|0.04|0.08|0.17|
|**w/o Skill-aware**|0.25|0.33|0.29|0.33|0.30|


demonstrating its robustness to diverse manipulation scenarios with varying skill requirements. 

**Simpler-Env Results.** Table 2 presents the evaluation results on the SimplerEnv WidowX robot suite. Our MoEActok-based VLA achieves the highest average success rate of 0.38, with task-specific performance of 0.38 for Put Spoon on Towel, 0.38 for Put Carrot on Plate, 0.13 for Stack Green on Yellow, and 0.63 for Put Eggplant in Basket. Among baseline methods, VQ-VLA represents the most competitive approach, as it also employs vector quantization but within a convolutional residual architecture. The performance comparison reveals a substantial improvement: MoEActok achieves 0.38 average success rate compared to VQ-VLA’s 0.21, representing an absolute gain of 17 percentage points. This significant margin demonstrates the effectiveness of our MoE quantization strategy over conventional VQ-VAE architectures. During inference, MoEActok achieves a throughput of approximately 10 Hz on a single NVIDIA RTX 4090 GPU. When integrated with the 

vLLM inference engine, this throughput scales to 54Hz. 

### **4.4. Ablation Study** 

To systematically evaluate the contribution of each component in our MoEActok architecture, we conduct ablation studies on two critical design choices: (1) remove the adapters for latent space harmonization ( **w/o Adapter** ), and (2) remove the skill-aware training paradigm with explicit skill prediction ( **w/o Skill-aware** ). Results on RoboTwin and SimplerEnv benchmarks are presented in Tables 3 and 4, respectively. From the results, removing the adapters leads to substantial performance degradation across both benchmarks. On RoboTwin, the success rate drops from 0.56 to 0.45, while on SimplerEnv, it plummets from 0.38 to 0.17. This significant decline demonstrates that adapters play a crucial role in reconciling the representational mismatch between skill-specific quantization spaces and the shared encoder-decoder architecture. Without these harmonization modules, the model struggles to effectively leverage the specialized representations learned by each expert quantizer. The ablation of skill-aware training also yields notable performance reductions: from 0.56 to 0.47 on RoboTwin and from 0.38 to 0.30 on SimplerEnv. These results validate our hypothesis that explicit skill prediction facilitates more structured learning. By decomposing the action generation process into skill identification followed by skill-conditioned token prediction, the model can better 

28048 


Figure 4. The influence of the number of experts on the performance of RoboTwin. 


Figure 5. The influence of the number of experts on the performance of Simper-Env. 

exploit the underlying skill structure in manipulation tasks, leading to more robust and generalizable policies. 

### **4.5. In-depth Analysis** 

We investigate the influence of the number of expert quantizers _K_ on performance by evaluating _K ∈{_ 1 _,_ 2 _,_ 4 _}_ on both RoboTwin and SimplerEnv benchmarks (Figures 4 and 5). The results demonstrate consistent performance gains with increasing _K_ . On RoboTwin, the average success rate improves from 0.50 ( _K_ =1) to 0.56 ( _K_ =4). On SimplerEnv, performance increases from 0.26 ( _K_ =1) to 0.38 ( _K_ =4). These findings validate that manipulation tasks comprise diverse skill primitives requiring specialized representation. 

### **4.6. Evaluation Results on Real Robot** 

To validate the practical applicability of our approach, we conduct real-world experiments on the AgileX Cobot Magic platform, equipped with four 6-DoF AgileX Piper arms 

Table 5. Real-world results. 

|**Tokenizer**|**Click Bell**|**Place Container**<br>**on Plate**|**Pick Diverse**<br>**Bottles**|**Avg.**|
|---|---|---|---|---|
|**Binning**|6/20|0/20|0/20|0.10|
|**FAST**|4/20|1/20|0/20|0.08|
|**VQ-BET**|7/20|2/20|0/20|0.15|
|**VQ-VLA**|10/20|7/20|0/20|0.28|
|**MoEActok**|12/20|9/20|1/20|0.37|


with parallel grippers. Visual observations are captured via a RealSense D435 RGB camera at 640×480 resolution and 30 Hz. To evaluate sim-to-real transfer, we directly deploy VLA policies trained exclusively on RoboTwin simulation data to three real-world tasks without any fine-tuning: Click Bell, Place Container on Plate, and Pick Diverse Bottles. Each task is evaluated over 20 trials. As shown in Tab. 5, our MoEActok-based VLA significantly outperforms all baselines across all three tasks, consistent with simulation results. Fig. 3 visualizes successful execution sequences for Click Bell (top) and Place Container on Plate (bottom). 

## **5. Conclusion** 

This work introduces MoEActok, a novel skill-aware action tokenizer that addresses the challenge of representing heterogeneous manipulation behaviors in VLAs. This method is motivated by the key observation that robotic manipulation tasks can be naturally decomposed into distinct skill primitives, each requiring specialized representation strategies. Based on this insight, we propose a MoE architecture that employs skill-specific quantizers within a clustering framework. This design enables MoEActok to allocate experts for learning different manipulation skills, thereby capturing the inherent diversity of action patterns more effectively. Comprehensive experiments across multiple benchmarks and real-world robotic settings validate our method. 

28049 

## **References** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 1 

- [2] Suneel Belkhale, Tianli Ding, Ted Xiao, Pierre Sermanet, Quon Vuong, Jonathan Tompson, Yevgen Chebotar, Debidatta Dwibedi, and Dorsa Sadigh. Rt-h: Action hierarchies using language. _ArXiv_ , abs/2403.01823, 2024. 1, 2 

- [3] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 1, 2, 3 

- [4] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. _ArXiv_ , abs/2505.06111, 2025. 3 

- [5] Chi-Lam Cheang, Guangzeng Chen, Ya Jing, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Hongtao Wu, Jiafeng Xu, Yichu Yang, Hanbo Zhang, and Minzhao Zhu. Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation. _ArXiv_ , abs/2410.06158, 2024. 1, 2 

- [6] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Qiwei Liang, Zixuan Li, Xianliang Lin, Yiheng Ge, Zhenyu Gu, Weiliang Deng, Yubin Guo, Tian Nian, Xuanbing Xie, Qiangyu Chen, Kailun Su, Tianling Xu, Guodong Liu, Mengkang Hu, Huan ang Gao, Kaixuan Wang, Zhixuan Liang, Yusen Qin, Xiaokang Yang, Ping Luo, and Yao Mu. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _ArXiv_ , abs/2506.18088, 2025. 2, 5, 6 

- [7] William Fedus, Barret Zoph, and Noam Shazeer. Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity. _Journal of Machine Learning Research_ , 23(120):1–39, 2022. 2 

- [8] Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with predictive visual representations. _ArXiv_ , abs/2412.14803, 2024. 3 

- [9] Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, Alec Radford, et al. Gpt-4o system card. _arXiv preprint arXiv:2410.21276_ , 2024. 1 

- [10] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Rich Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0.5: 

a vision-language-action model with open-world generalization. _ArXiv_ , abs/2504.16054, 2025. 3 

- [11] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag R. Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. _ArXiv_ , abs/2406.09246, 2024. 1, 2, 3, 6 

- [12] Seungjae Lee, Yibin Wang, Haritheja Etukuru, H. Jin Kim, Nur Muhammad Mahi Shafiullah, and Lerrel Pinto. Behavior generation with latent actions. In _ICML_ , 2024. 1, 2, 3, 6 

- [13] Shuang Li, Yihuai Gao, Dorsa Sadigh, and Shuran Song. Unified video action model. _ArXiv_ , abs/2503.00200, 2025. 3 

- [14] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 2, 5 

- [15] Zhixuan Liang, Yao Mu, Mingyu Ding, Fei Ni, Masayoshi Tomizuka, and Ping Luo. Adaptdiffuser: diffusion models as adaptive self-evolving planners. In _Proceedings of the 40th International Conference on Machine Learning_ , pages 20725–20745, 2023. 3 

- [16] Zhixuan Liang, Yao Mu, Hengbo Ma, Masayoshi Tomizuka, Mingyu Ding, and Ping Luo. Skilldiffuser: Interpretable hierarchical planning via skill abstractions in diffusion-based task execution. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 16467– 16476, 2024. 3 

- [17] Zhixuan Liang, Yizhuo Li, Tianshuo Yang, Chengyue Wu, Sitong Mao, Liuao Pei, Xiaokang Yang, Jiangmiao Pang, Yao Mu, and Ping Luo. Discrete diffusion vla: Bringing discrete diffusion to action decoding in vision-language-action policies. _arXiv preprint arXiv:2508.20072_ , 2025. 1 

- [18] Jiaming Liu, Hao Chen, Pengju An, Zhuoyang Liu, Renrui Zhang, Chenyang Gu, Xiaoqi Li, Ziyu Guo, Sixiang Chen, Mengzhen Liu, Chengkai Hou, Mengdi Zhao, KC alex Zhou, Pheng-Ann Heng, and Shanghang Zhang. Hybridvla: Collaborative diffusion and autoregression in a unified visionlanguage-action model. _ArXiv_ , abs/2503.10631, 2025. 3 

- [19] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _ArXiv_ , abs/2410.07864, 2024. 3 

- [20] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. In _International Conference on Learning Representations_ , 2017. 6 

- [21] Shridhar Mohit, Manuelli Lucas, and Fox Dieter. Perceiveractor: A multi-task transformer for robotic manipulation. _ArXiv_ , abs/2209.05451, 2022. 2 

- [22] Nvidia, Johan Bjorck, Fernando Castaneda, Nikita Cherniadev, Xingye Da, Runyu Ding, LinxiJimFan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyuan Jiang, Jan Kautz, Kaushil Kundalia, Lawrence Lao, Zhiqi Li, Zongyu Lin, Kevin Lin, Guilin Liu, Edith Llontop, Loic 

28050 

Magne, Ajay Mandlekar, Avnish Narayan, Soroush Nasiriany, Scott Reed, You Liang Tan, Guanzhi Wang, Zu Wang, Jing Wang, Qi Wang, Jiannan Xiang, Yuqi Xie, Yinzhen Xu, Zhen-Teng Xu, Seonghyeon Ye, Zhiding Yu, Ao Zhang, Hao Zhang, Yizhou Zhao, Ruijie Zheng, and Yuke Zhu. Gr00t n1: An open foundation model for generalist humanoid robots. _ArXiv_ , abs/2503.14734, 2025. 3 

- [23] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 1, 3, 5, 6 

- [24] Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, et al. Language models are unsupervised multitask learners. _OpenAI blog_ , 1(8):9, 2019. 2 

- [25] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Cliport: What and where pathways for robotic manipulation. _ArXiv_ , abs/2109.12098, 2021. 2 

- [26] Octo Model Team, Dibya Ghosh, Homer Rich Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, You Liang Tan, Pannag R. Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An opensource generalist robot policy. _ArXiv_ , abs/2405.12213, 2024. 1, 2 

- [27] Aaron Van Den Oord, Oriol Vinyals, et al. Neural discrete representation learning. _Advances in neural information processing systems_ , 30, 2017. 3, 4 

- [28] Ashish Vaswani, Noam M. Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and Illia Polosukhin. Attention is all you need. In _Neural Information Processing Systems_ , 2017. 1 

- [29] Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, An- 

dre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pages 1723–1736. PMLR, 2023. 2, 3, 6 

- [30] Lirui Wang, Xinlei Chen, Jialiang Zhao, and Kaiming He. Scaling proprioceptive-visual learning with heterogeneous pre-trained transformers. _ArXiv_ , abs/2409.20537, 2024. 1 

- [31] Yating Wang, Haoyi Zhu, Mingyu Liu, Jiange Yang, HaoShu Fang, and Tong He. Vq-vla: Improving visionlanguage-action models via scaling vector-quantized action tokenizers. _ArXiv_ , abs/2507.01016, 2025. 2, 3, 6 

- [32] Hongtao Wu, Ya Jing, Chi-Hou Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. Unleashing large-scale video generative pre-training for visual robot manipulation. _ArXiv_ , abs/2312.13139, 2023. 1, 2 

- [33] Qwen An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Guanting Dong, Haoran Wei, Huan Lin, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxin Yang, Jingren Zhou, Junyang Lin, Yang Su, Yi-Chao Zhang, Yunyang Wan, Yuqi Liu, Zeyu Cui, Zhenru Zhang, Zihan Qiu, Shanghaoran Quan, and Zekun Wang. Qwen2.5 technical report. _ArXiv_ , abs/2412.15115, 2024. 6 

- [34] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. _2023 IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 11941–11952, 2023. 5 

- [35] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 1, 2, 3 

28051 

