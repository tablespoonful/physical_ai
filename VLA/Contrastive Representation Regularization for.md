---
title: "Contrastive Representation Regularization for Vision-Language-Action Models"
date: "2025-10-02"
authors: "Taeyoung Kim; Jimin Lee; Myungkyu Koo; Dongyoung Kim; Kyungmin Lee; Changyeon Kim"
venue: "Submitted to ICLR 2026 / ICML 2026"
url: https://arxiv.org/abs/2510.01711
pdf: https://arxiv.org/pdf/2510.01711
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2510.01711)** / [論文ページ](https://arxiv.org/abs/2510.01711)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Contrastive Representation Regularization for Vision-Language-Action Models** 

**Taeyoung Kim**<sup>1 2</sup> **Jimin Lee**<sup>1</sup> **Myungkyu Koo**<sup>1 2</sup> **Dongyoung Kim**<sup>1 2</sup> **Kyungmin Lee**<sup>1</sup> **Changyeon Kim**<sup>1</sup> **Younggyo Seo**<sup>3</sup><sup>_†_</sup> **Jinwoo Shin**<sup>1 2</sup><sup>_†_</sup> 

# **Abstract** 

Vision-Language-Action (VLA) models have shown strong capabilities in robot manipulation by leveraging rich representations from pretrained Vision-Language Models (VLMs). However, their representations arguably remain suboptimal, lacking sensitivity to robotic signals such as control actions and proprioceptive information. To address the issue, we introduce _Robot Stateaware Contrastive Loss (RS-CL)_ , a simple and effective representation regularization for VLA models, designed to bridge the gap between VLM representations and robotic signals. In particular, RS-CL aligns the representations more closely with the robot’s proprioceptive states by using relative distances between the states as soft supervision. Complementing the original action prediction objective, RS-CL enhances control-relevant representation learning, while being lightweight and fully compatible with standard VLA training pipelines. Our empirical results demonstrate that RS-CL substantially improves the performance of state-of-the-art VLA models; it pushes the prior art to 69.7%, achieving the state-of-the-art performance on the RoboCasa-Kitchen benchmark, and boosts success rates from 45.0% to 58.3% on challenging real-robot manipulation tasks. 

# **1. Introduction** 

Vision-Language-Action (VLA; Zitkovich et al. 2023) models have emerged as a powerful framework for robot manipulation, leveraging pre-trained Vision-Language Models (VLM; Liu et al. 2023b) to provide rich visual and semantic grounding for control policies. Among the state-of-the-art VLA models, the common design is to employ a generative action decoder conditioned on VLM-derived representa- 

_†_ Equal advising.<sup>1</sup> KAIST<sup>2</sup> RLWRLD<sup>3</sup> UC Berkeley. Correspondence to: Taeyoung Kim <taeyoungkim85@kaist.ac.kr>. 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

tions (Black et al., 2025b; Bjorck et al., 2025). These decoders are trained with an action prediction loss, supervised by the ground-truth sequence of actions. 

Prior studies have shown that training the backbone VLM alongside the action decoder is essential to the action prediction performance of VLA models. This is because VLMs are typically trained on large-scale visual instruction datasets, but have not been explicitly exposed to robotic modalities, such as low-level control actions and proprioceptive information. Consequently, training VLA models conditioned on frozen VLM representations leads to suboptimal performance, as the VLM lacks the capability to capture robotic signals (Driess et al., 2025). 

Many recent works have proposed methods to train the VLM backbone in VLA models to tackle this issue. A widely adopted strategy is to directly update the VLM via gradients from the action prediction objective (Black et al., 2025b; Bjorck et al., 2025). Beyond this, several works introduce auxiliary objectives, such as jointly training the VLM backbone with curated instruction datasets (Yang et al., 2025), or blocking gradients from the action decoder, and instead learning to generate intermediate subtasks and discretized actions (Driess et al., 2025). Another line of work further trains the VLM on embodied reasoning or spatial grounding tasks using robotics datasets (Cao et al., 2025; Luo et al., 2025; Azzolini et al., 2025; NVIDIA GEAR, 2025), or autoregressively predicts discretized actions (Kim et al., 2025; Black et al., 2025a) before fine-tuning them for continuous action prediction. While these approaches help bridge the gap between general-purpose VLM representations and the demands of action prediction, they often require additional training stages or carefully curated datasets. 

In contrast, we aim to directly refine VLM representations to better serve action prediction, while remaining efficient and seamlessly compatible with the existing VLA training pipelines. In particular, we focus on contrastive learning, as it provides a principled way to refine representations by defining similar and dissimilar pairs, effectively structuring the embedding space. The specific choice of pair construction determines what the embeddings should capture, ranging from semantic relations between modalities (Radford et al., 2021) to temporal dynamics and policy-relevant 

1 

**Contrastive Representation Regularization for Vision-Language-Action Models** 


_Figure 1._ **Overview.** We extend the standard VLA model training framework with a contrastive regularization path. Embeddings from the pre-trained VLM are augmented by the _view cutoff_ operation applied on the feature slice corresponding to a randomly selected observation view, and are optimized with our _Robot State-aware Contrastive Loss_ to attract samples with similar proprioceptive states. 

representations (Sermanet et al., 2018; Nair et al., 2022; Ma et al., 2023). Inspired by this perspective, we introduce a contrastive objective that explicitly guides the representations to capture robotic signals, in particular the robot’s proprioceptive states. By jointly optimizing the VLM representation with the standard action prediction loss, we learn representations that are not only semantically rich but also deeply grounded in the robot’s physical state, leading to accurate action prediction. 

**Contribution.** We propose _Robot State-aware Contrastive Loss (RS-CL)_ , a representation regularization that leverages continuous proprioceptive distances as soft contrastive supervision to reshape VLM representations for accurate action prediction. Unlike conventional contrastive losses, RSCL assigns pairwise weights based on proprioceptive state distances, guiding representations to better reflect controlrelevant structure. In addition, we propose a representationlevel augmentation for VLA models, termed _view cutoff_ . This augmentation constructs alternative embeddings by masking out the feature corresponding to a randomly selected observation view. By operating at the representation level and minimizing additional forward passes through the pre-trained VLM, RS-CL enables single-stage, end-to-end representation learning for VLA models, remaining fully compatible with existing training pipelines. 

We extensively evaluate the effectiveness of RS-CL under multitask manipulation benchmarks such as RoboCasaKitchen (Nasiriany et al., 2024) and LIBERO (Liu et al., 2023a). RS-CL achieves state-of-the-art performance on the RoboCasa-Kitchen benchmark with a success rate of 

69.7%, surpassing all strong baselines. Notably, RS-CL yields larger gains on pick-and-place tasks, improving success rates from 30.3% to 41.5% (+11.2%), which require precise positioning during grasping and placing. Finally, we show that RS-CL is applicable to real-robot hardware experiments, showing improvement from 45.0% to 58.3% (+13.3%) on challenging manipulation tasks. 

In summary, our contributions are as follows: 

- We introduce _Robot State-aware Contrastive Loss (RS-CL)_ , a novel objective for VLA models that explicitly aligns VLM representations with proprioceptive states. 

- We design RS-CL to operate directly at the representation alongside the original action prediction objective. Therefore, RS-CL remains lightweight and compatible with the existing training pipeline. 

- We validate RS-CL across diverse training scenarios on simulation benchmarks and real-world experiments, yielding improvements over the state-of-the-art VLA models. 

# **2. Method** 

In this section, we introduce _Robot State-aware Contrastive Loss (RS-CL)_ , which enhances the action prediction capability of VLA models by guiding the representation to capture low-level robotic signals, particularly the proprioceptive states. We describe the VLA training framework in Sec. 2.1 and present our proposed method, RS-CL, in Sec. 2.2. An overview of our method is shown in Fig. 1. 

2 

**Contrastive Representation Regularization for Vision-Language-Action Models** 


_Figure 2._ **Training VLM representations towards action prediction. (a)** We visualize VLM embeddings of robot episodes performing the same task “Open the microwave / cabinet door” across different scenes in RoboCasa-Kitchen. **(b)** Pre-trained VLM representations are dominated by the visual appearance ( _e.g._ , scene layout, large surrounding objects). **(c)** RS-CL guides embeddings to align with the robot’s proprioceptive states, yielding representations that capture common robotic signals ( _e.g._ , the robot’s current pose, next control action) across environments, therefore aligning all episodes by the task progress. 

## **2.1. Vision-Language-Action model** 

VLA models are trained to predict the next action chunk **A** _t_ = [ **a** _t,_ **a** _t_ +1 _, . . . ,_ **a** _t_ + _H_ ] of horizon _H_ at current timestep _t_ , from a set of observation images from _V_ different views **O**<sup>_V_</sup> _t_<sup>=</sup><sup>_{_</sup><sup>**o**1</sup> _t_<sup>_,_</sup><sup>**o**2</sup> _t_<sup>_, . . . ,_</sup><sup>**o**</sup><sup>_V_</sup> _t_<sup>_}_, a task instruction</sup><sup>**c**, and the robot’s</sup> proprioceptive state **q** . A standard framework for VLA models (Black et al., 2025b; Bjorck et al., 2025) encodes multimodal inputs [ **O**<sup>_V_</sup> _t_<sup>_,_</sup><sup>**c**] using a pre-trained VLM into a</sup> hidden representation, and pass it to the action decoder. In practice, we train a lightweight adapter module _fϕ_ upon the VLM and freeze the VLM, following NVIDIA GEAR (2025). _fϕ_ processes the output of the VLM as **h** = _fϕ_ �VLM( **O**<sup>_V_</sup> _t_<sup>_,_</sup><sup>**c**)</sup> � _∈_ R<sup>_N×d_model</sup> , where _N_ is the number of input tokens for the VLM and _d_ model is the size of the hidden dimension. 

An action decoder _Dθ_ generates **A** _t_ conditioned on **h** with the current robot state **q** . Similar to prior works (Black et al., 2025b; Bjorck et al., 2025), we adopt the DiT (Peebles & Xie, 2023) architecture for the _Dθ_ and train with the flowmatching objective (Lipman et al., 2023; Liu, 2022): 


where **A**<sup>_s_</sup> _t_<sup>=</sup><sup>_s_</sup><sup>**A**</sup><sup>_t_+ (1</sup><sup>_−s_)</sup><sup>_ϵ_is an interpolated action chunk</sup> at the flow-matching timestep _s ∈_ [0 _,_ 1] sampled from a prior distribution _p_ ( _s_ ). After training, _Dθ_ generates **A** _t_ through an iterative denoising process starting from a random Gaussian noise _ϵ ∼N_ ( **0** _,_ **I** ). 

## **2.2. Robot State-aware Contrastive Loss** 

While VLMs acquire rich semantic representations from Internet-scale vision–language data, they lack exposure to 

robotic modalities such as low-level control actions and proprioceptive states. As a result, their embeddings are often dominated by the visual appearance and fail to capture signals relevant to robot control. This misalignment is evident when visualizing VLM embeddings of robot trajectories for the same manipulation task ( _e.g._ , Open the microwave / cabinet door) across different environments in RoboCasa-Kitchen (see Fig. 2a). We observe that the embeddings cluster primarily by visual cues, such as large objects or background textures (see Fig. 2b), rather than control-relevant factors like the robot’s current pose or the next action needed to complete the task. A more detailed visualization and analysis are provided in Appendix E.1. 

This misalignment motivates our central hypothesis: explicitly aligning VLM representations with the robot’s physical state will improve the action prediction performance of VLA models. Based on this hypothesis, we introduce _Robot Stateaware Contrastive Loss (RS-CL)_ , an auxiliary objective for VLA models that regularizes the VLM representation space using supervision from the robot’s proprioceptive states. Our key idea is a contrastive loss that leverages the distances between proprioceptive states to assign soft weights to similarity scores, which effectively guides the representation space toward alignment with control-relevant robotic signals. As an auxiliary objective, RS-CL complements the action prediction loss, enabling the entire model to be trained endto-end in a single stage. Concretely, RS-CL consists of three key components: (i) a _learnable summarization token_ that amortizes long VLM output embeddings, (ii) a _weighting scheme_ for robot state supervision via contrastive learning, and (iii) a _representation-level augmentation_ strategy that enables lightweight and stable representation learning. 

3 

**Contrastive Representation Regularization for Vision-Language-Action Models** 

**Amortizing VLM embeddings for representation learning.** Applying contrastive learning on the full sequence of VLM embeddings **h** _∈_ R<sup>_N×d_model</sup> is impractical as the sequence length _N_ is typically large, leading to high computational cost and diluted learning signals. To address this, we introduce a _learnable summarization token_ **u** _∈_ R<sup>1</sup><sup>_×d_model</sup> to produce a compact representative embedding of the sequence. Specifically, **u** is appended to the VLM output and processed by the adapter _fϕ_ : 


where **w** denotes the output of the summarization token and _⊕_ denotes concatenation along the sequence dimension. Finally, **w** is projected by a lightweight projector _gψ_ into **z** = _gψ_ ( **w** ), providing a compact summary for contrastive learning (Chen et al., 2020), while the original embedding **h** serves as the conditioning input to the action decoder. 

**Incorporating robot states into contrastive learning.** To effectively restructure the VLM representation space to capture robotic signals, we introduce a supervised contrastive learning objective assigned with _soft weights_ (Khosla et al., 2020; Suresh & Ong, 2021), that incorporate the distance between proprioceptive states. Conceptually, embeddings associated with similar proprioceptive states receive higher weights, are pulled closer in the representation space. We consider InfoNCE (Oord et al., 2018) for the contrastive loss, which is widely used in practice (Laskin et al., 2020; Nair et al., 2022; Ma et al., 2023). Formally, our _Robot Stateaware Contrastive Loss (RS-CL)_ is defined as a weighted variant of the InfoNCE loss: 


where _{_ **z** ˜ _}_<sup>_B_</sup> _j_ =1<sup>denotes the augmented batch corresponding</sup> to _{_ **z** _}_<sup>_B_</sup> _i_ =1<sup>, sim denotes the cosine similarity, and</sup><sup>_τ>_0 is</sup> a temperature that controls the sharpness of similarity. The soft weights _wij_ are computed from the relative distance between proprioceptive states **q** _i,_ **q** _j_ . In practice, we use the Euclidean distance and formulate _wij_ as follows: 


where _β >_ 0 is a temperature that controls the sharpness of the mapping from distance to weight. The complete training objective integrates the proposed RS-CL with the action prediction objective, implemented as the flow-matching loss in Eq. 1: 


where _λ >_ 0 is a weighting coefficient that balances the contribution of RS-CL, and we jointly optimize _θ_ , _ϕ_ , and _ψ_ . 


_Figure 3._ **Representation-level augmentation for contrastive learning.** _View cutoff_ randomly masks the embedding slice associated with one observation viewpoint, forming contrastive pairs at the representation level. 

**Representation augmentation for contrastive pairs.** The primary goal of our augmentation strategy is to generate diverse contrastive pairs while preserving the semantics tied to the robot’s proprioceptive states. In line with this goal, we exploit the property that VLA models commonly process observations of the same scene from multiple views, and propose _view cutoff_ (see Fig. 3), a simple representation-level augmentation inspired by cutoff (Shen et al., 2020). View cutoff randomly selects a single view index _i ∈{_ 1 _, . . . , V }_ and masks out the corresponding feature slice from the VLM output VLM( **O**<sup>_V_</sup> _t_<sup>_,_</sup><sup>**c**).Unlike data-level augmentations re-</sup> quiring additional forward passes through the VLM for each augmented batch, view cutoff operates at the representation level, obtaining alternative representations with minimal overhead. As a result, only the lightweight adapter _fϕ_ and projector _gψ_ are required to process the augmented variants, making the method substantially more efficient, yet still providing diverse pairs for contrastive learning. 

# **3. Experiments** 

In this section, we evaluate the effectiveness of RS-CL across diverse training scenarios. In Section 3.1, we examine its impact on a pre-trained state-of-the-art VLA model across multitask manipulation benchmarks: RoboCasaKitchen (Nasiriany et al., 2024) and LIBERO (Liu et al., 2023a), and further demonstrate its applicability to realworld tasks using a 7-DoF manipulator. In Section 3.2, we further validate RS-CL when training VLAs from scratch on top of various pre-trained VLM backbones. 

**Implementation and training details.** We adopt GR00T N1.5 (NVIDIA GEAR, 2025) as our baseline VLA framework and unless otherwise specified, we follow the training and inference settings of the original implementation. For the regularization path, a projection head _gψ_ is implemented as a 2-layer MLP with hidden dimension 2048 and projection dimension 128. The weighting coefficient _λ_ for _L_ RS-CL is initialized to 1.0 and decayed to 0 using a cosine schedule, such that representation refinement is emphasized in 

4 

**Contrastive Representation Regularization for Vision-Language-Action Models** 

_Table 1._ **RoboCasa-Kitchen benchmark success rate (%).** Results include the performance of representative VLA methods trained with 300 demonstrations. Results of _π_ 0, _π_ 0-FAST, and GR00T N1.5 are reproduced while others are from the original work. Best results are highlighted in **bold** . 


_Figure 4._ **RoboCasa-Kitchen benchmark success rate (%) by number of training demonstrations.** We compare RS-CL (blue) with the baseline GR00T N1.5 (gray) across varying training dataset sizes. RS-CL consistently outperforms across all settings, and notably demonstrates significant performance gains in the lowdata regime (30 demos) for pick-and-place tasks. 

early training while accurate action prediction becomes the main focus later. For proprioceptive states, we primarily use the end-effector position ( _x_ , _y_ , _z_ , 6D rotation, and gripper state), min-max normalized to [ _−_ 1 _,_ 1] per dimension. In the real-robot experiments, we additionally explore the use of absolute joint positions of the manipulator to examine variations in proprioceptive configurations. 

## **3.1. Fine-tuning Experiments** 

We first evaluate RS-CL in a fine-tuning scenario, where it is integrated into a state-of-the-art pre-trained VLA model. This setup tests whether RS-CL can yield additional gains on model weights that are already optimized for action prediction in large-scale, demonstrating the ability to further enhance strong pre-trained policies at a target environment. 

**Simulation experiment setup.** We evaluate RS-CL on two widely used multitask simulation benchmarks, RoboCasaKitchen and LIBERO, comparing against representative VLA baselines. RoboCasa-Kitchen consists of 24 atomic manipulation tasks in a simulated kitchen environment with three camera views (2 exterior, 1 wrist camera). We evaluate RS-CL under varying numbers of training demonstrations 

_Table 2._ **LIBERO benchmark success rate (%).** Results include the performance of representative VLA methods. Results of GR00T N1 and GR00T N1.5 are reproduced, where the performance of _π_ 0-FAST, _π_ 0 are from the original work. Best results are highlighted in **bold** . 

|Method|Spatial|Object|Goal|Long|Avg.|
|---|---|---|---|---|---|
|_π_0-FAST|96.4|96.8|88.6|60.2|85.5|
|_π_0|96.4|98.8|95.8|85.2|94.1|
|GR00T N1|95.6|97.6|94.2|89.6|94.3|
|GR00T N1.5|98.2|**99.4**|97.2|87.8|95.7|
|**+ RS-CL (ours)**|**98.4**|98.6|**98.2**|**90.4**|**96.4**|


_Table 3._ **Comparison to time-contrastive networks (TCN; Sermanet et al. 2018).** Results report the average success rate (%) and FLOPs per sample for a single forward pass during training on RoboCasa-Kitchen with 30 demonstrations. Best results are highlighted in **bold** , and _↑_ ( _↓_ ) indicates higher (lower) are better. 

|Method|SR (%,_↑_)|FLOPs (_×_10<sup>12</sup>,_↓_)|
|---|---|---|
|Baseline|48.2|2.58|
|Multi-view TCN|50.0|7.53|
|Single-view TCN|50.3|7.53|
|<br>**RS-CL**|**53.0**|**2.91**|


(30, 100, and 300) using the publicly available dataset generated by MimicGen (Mandlekar et al., 2023). LIBERO comprises four multitask suites with two camera views (1 exterior, 1 wrist camera). For LIBERO, we use the filtered dataset released by Kim et al. (2024) and jointly train all four task suites (see Appendix B for details). 

**Simulation experiment results.** Table 1 and Fig. 4 summarize the performance of RS-CL on the RoboCasa-Kitchen benchmark. RS-CL achieves state-of-the-art performance among all VLA baselines and consistently outperforms the original GR00T N1.5 fine-tuning framework across all dataset sizes. In particular, RS-CL yields substantial gains on pick-and-place tasks, with success rates increasing from 30.3% to 41.5% (+11.2%). We attribute these gains to RS-CL’s ability to produce more accurate actions during execution, which is especially important for pick-and-place tasks that require precise positioning during both grasping and placing. RS-CL also improves performance on LIBERO (Table 2), confirming its robustness across benchmarks. 

To evaluate the effectiveness and efficiency of our specific design choice, we compare RS-CL with time-contrastive networks (TCN; Sermanet et al. 2018), a representative representation learning method in robotics that learns from explicitly comparing representations across neighboring timesteps. We implement TCN as an auxiliary objective on top of GR00T N1.5, considering both multi-view and single-view variants (see Appendix B.3 for details). Table 3 shows that both TCN variants provide only modest improvements over the baseline, while incurring a substantial increase in computational cost. This overhead arises 

5 

**Contrastive Representation Regularization for Vision-Language-Action Models** 


_Figure 5._ **Real-robot experiment task examples.** We validate RS-CL on a Franka Research 3 arm with a Robotiq 2F-85 gripper, utilizing two camera views. **(a)** We conduct pick-and-place tasks across diverse objects and environments, and a close lid task. **(b)** We evaluate generalization abilities under variations in visual appearance, physical properties, language following, and lighting conditions. 


_Figure 6._ **Real-robot experiment success rate (%).** Results on **(a)** in-domain tasks (4 pick-and-place and 1 close-lid task), and **(b)** generalization tasks (visual, physical, lighting variation and language following). For the in-domain close lid and language following tasks, we report both partial success ( _e.g._ , successful pickup, language following; transparent bars) and full success (solid bars). 

from the need for temporally structured data mining and additional VLM forward passes to construct positive and negative pairs. In contrast, RS-CL achieves a higher success rate with only a modest increase in FLOPs. This efficiency is enabled by the proposed _view-cutoff_ augmentation, which operates entirely at the representation level after a single VLM forward pass. Overall, RS-CL serves as an effective yet lightweight regularizer for single-stage, end-to-end VLA training, strengthening conditioning representations without significant additional computational overhead. 

**Real-robot experiment setup.** To further assess whether RS-CL leads to more precise actions in task execution, we design our real-robot experiments primarily around pickand-place tasks, which require accurate positioning during grasping and placing. We also introduce a challenging close lid task; the lid has a small handle that is more difficult to grasp than other objects, and once grasped, the wrist camera view becomes partially occluded, making placement harder (see Fig. 5a). We evaluate each method on both in-domain tasks and generalization tasks in Fig. 5. We collect and train each method with teleoperated expert demonstrations 

of 4 pick-and-place tasks across diverse objects (teddy bear, sponge, cup, cube) and environments (box, bowl, plate, basket), as well as the close lid task, utilizing two camera views (exterior and wrist). For pick-and-place tasks, we use end-effector position as the proprioceptive state, while for the close lid task, we use absolute joint positions of the manipulator; see Appendix C for details. 

**Real-robot experiment results.** RS-CL consistently improves performance across real-robot tasks (see Fig. 6a). In particular, for the close-lid task, RS-CL brings improvements not only in partial success ( _i.e._ , lifting the lid) but also larger gains in complete success ( _i.e._ , accurately closing the pot) even under occluded viewpoints (see Fig. 5a, bottomright). We attribute this effect to two factors: (i) proprioceptive supervision enables more accurate positioning, and (ii) the proposed _view cutoff_ augmentation promotes viewinvariant representations, thereby improving robustness to partial occlusion. Finally, our generalization experiments show that RS-CL not only maintains but leads to stronger generalization performance of VLAs across visual, physical, lighting shifts, and language grounding (see Fig. 6b). 

6 

**Contrastive Representation Regularization for Vision-Language-Action Models** 


_Figure 7._ **From-scratch experiments across multiple backbone VLMs.** Success rates (%) on RoboCasa-Kitchen for VLA models trained from various backbones, where Vanilla denotes Qwen2.5-VL. Results show the effects of RS-CL on backbones further trained with robotics data, based on **(a)** Qwen2.5-VL-3B, **(b)** 7B, and **(c)** SigLIP2 and GR00T N1.5, covering diverse backbone and training capacities. 

## **3.2. From-Scratch Experiments** 

In this section, we evaluate the impact of RS-CL in a from-scratch training scenario, where we train a VLA model directly on top of general-purpose pre-trained VLM backbones of Qwen2.5-VL (Bai et al., 2025) and SigLIP2 (Tschannen et al., 2025). This setup directly reflects our motivation that pre-trained VLM representations lack sensitivity to robotic signals, and enables us to validate whether explicitly aligning them to proprioceptive information yields performance gains. Furthermore, we compare RS-CL against baselines obtained by further training general-purpose VLMs on robotics datasets. 

**Setup.** We adopt RoboCasa-Kitchen as our primary benchmark, using 300 demonstrations for training. We attach a randomly initialized action decoder to pre-trained VLMs with a lightweight adapter module _fϕ_ . The VLM backbone is frozen and only the adapter is trained to refine conditioning representations, except for SigLIP2, where we additionally try unfreezing the backbone to study the effect of RS-CL with varying numbers of trainable backbone parameters. The action decoder is implemented as a 16-layer DiT with 0.5B parameters. For further-trained VLM baselines, we include RoboBrain (Cao et al., 2025), VeBrain (Luo et al., 2025), and Cosmos-Reason1 (Azzolini et al., 2025), which are high-performing models further trained from Qwen2.5VL on embodied reasoning and robotics datasets, as well as NORA (Hung et al., 2025), which is trained to predict FAST (Pertsch et al., 2025) tokenized actions (see Appendix B.4 for details). 

**Results on different pre-trained VLM backbones.** Fig. 7 summarizes the effect of RS-CL when training VLA models from different pre-trained VLMs. RS-CL consistently improves the success rate across all backbones, demonstrating that our representation regularization generalizes beyond a particular backbone VLM. On SigLIP2, RS-CL yields larger improvements when the backbone is unfrozen, indicating that RS-CL can benefit from increased trainable capacity. 

_Table 4._ **Ablation study on design choices.** Results report the average success rate (%) on RoboCasa-Kitchen with 300 demonstrations, analyzing the effect of different **(a)** distance definitions for soft-label supervision and **(b)** augmentation methods. 

|Soft-label target|Avg.|Augmentation method|Avg.|
|---|---|---|---|
|Baseline (_i.e._, no regularization)|65.7|No augmentation|65.3|
|No soft label (_i.e._, InfoNCE)|67.3|Token cutoff|66.3|
|Next action sequence distance|66.7|Feature cutoff|67.5|
|Next single action distance|66.8|Span cutoff|67.3|
|Current state distance|**69.7**|View cutoff|**69.7**|


(a) Soft-label target. 

(b) Augmentation method. 

**Comparison to VLM training strategies.** Fig. 7 compares RS-CL with VLMs further trained on robotics datasets, for tasks such as visual grounding, embodied reasoning, and discretized action prediction. While such further-trained VLMs, when used as conditioning models, provide only limited and often inconsistent gains across backbone families, RS-CL consistently delivers larger improvements. It achieves higher success rates than any of these adapted models on both Qwen2.5-VL-3B and 7B, and further enhances their benefits when combined with them. Even for GR00T N1.5 VLM (NVIDIA GEAR, 2025), which is derived from Eagle 2.5 VLM (Chen et al., 2025) with enhanced grounding and reasoning capabilities, RS-CL provides additional gains. These results suggest that robotics-specific training alone may not fully close the gap between general-purpose VLM representations and the demands for action prediction, while RS-CL effectively bridges much of the gap. 

## **3.3. Ablation Studies and Analyses** 

**Effect of soft-label supervision target.** In Table 4a, we observe that standard InfoNCE improves over the baseline without contrastive learning, demonstrating the effectiveness of our training framework, namely contrastive representation regularization for VLA models. However, alternative supervision signals (see Appendix B.3 for distance definitions) such as next action distances fall below vanilla InfoNCE. A plausible reason is that next actions have multimodal characteristics, and they themselves serves as the 

7 

**Contrastive Representation Regularization for Vision-Language-Action Models** 

_Table 5._ **KNN task-phase classification accuracy (%) on identical task trajectories across diverse scenes.** RS-CL enhances representation quality for task progress recognition under visual variations, narrowing the gap to ground-truth state performance. 


_Figure 8._ **Alignment to proprioceptive states.** We measure the alignment of conditioning representations inside trained VLA models, to the robot’s proprioceptive states using CKNNA (Huh et al., 2024). RS-CL successfully improves the representation alignment to robot states of VLA models, compared to the model solely trained with action prediction loss. 

prediction target, making it difficult to use as a reliable alignment signal. In contrast, the robot proprioceptive state provides a stable cue for representation alignment. 

**Effect of representation augmentation strategy.** In Table 4b, we observe limited improvements from similar representation-level cutoff operations (Shen et al., 2020), while our proposed _view cutoff_ achieves the highest success rate. This shows that simulating viewpoint variation is particularly beneficial for robust representation learning in multi-view robotic manipulation settings. This is in line with prior works, addressing the effects of utilizing multiview data for representation learning (Weinzaepfel et al., 2022; Seo et al., 2023). 

**Quantitative analysis of representation alignment.** We further analyze how RS-CL improves the alignment of VLM representations with robotic signals using KNN classification and CKNNA (Huh et al., 2024). As shown in Table 5, RS-CL improves task-phase classification, suggesting that the conditioning representation encodes state observations more reliably and is robust to visual background changes, thereby providing a more stable signal for the action decoder. Consistently, RS-CL increases representation similarity between learned embeddings and proprioceptive features (see Fig. 8), indicating that it reshapes the embedding space toward capturing control-relevant signals. Additional details for the experiments are provided in Appendix B.3. 

# **4. Related Works** 

**Leveraging VLM representations for robot manipulation.** Vision-Language-Action (VLA) models have shown strong capabilities in robotic control by leveraging semantically enriched features from pre-trained Vision-Language Models (VLMs) (Zitkovich et al., 2023; Driess et al., 2023; Kim et al., 2024; Black et al., 2025b; Pertsch et al., 2025; Bjorck et al., 2025). A widely used architecture for VLA models consists of a pre-trained VLM and an action decoder with dedicated parameters (Black et al., 2025b; Bjorck et al., 2025; Shukor et al., 2025; Li et al., 2024; Zhou et al., 2025; Wen et al., 2025), training the VLM backbone with action prediction loss. Prior works have sought to further train VLMs for core knowledge of robot manipulation such as embodied reasoning and physical grounding (Cao et al., 2025; Luo et al., 2025; Azzolini et al., 2025; NVIDIA GEAR, 2025), or by discretized action prediction (Kim et al., 2025; Black et al., 2025a). Other methods jointly train the VLM with the action decoder on the aforementioned objectives. (Driess et al., 2025; Yang et al., 2025). Distinct from these approaches, our method does not rely on largescale curated robotics datasets but instead improves VLM representations via a self-supervised objective. 

**Contrastive representation learning.** Contrastive learning has been widely adopted to acquire transferable representations from high-dimensional inputs (Oord et al., 2018; Chen et al., 2020; He et al., 2020; Laskin et al., 2020; Radford et al., 2021). In robotics, contrastive objectives enable robust transfer of visuomotor policies, leveraging temporal consistency (Sermanet et al., 2018; Nair et al., 2022; Ma et al., 2023) or multi-view data (Seo et al., 2023). Recent works extend this idea to multimodal alignment (Rana et al., 2023; Myers et al., 2023; Lee et al., 2025), producing behaviorally grounded embeddings for control. Unlike prior approaches that apply contrastive learning as a separate representation learning stage, we integrate it directly into VLA training, enabling single-stage end-to-end optimization with the action prediction objective. 

# **5. Conclusion** 

In this work, we present _Robot State-aware Contrastive Loss (RS-CL)_ , a simple and effective regularization method that explicitly aligns representations with robot proprioceptive states. Our experiments demonstrate that RS-CL consistently improves VLA performances, particularly on tasks requiring reliable and precise positioning. These findings highlight the importance of shaping conditioning representations with physically grounded signals for accurate action prediction. We hope this work encourages further exploration of incorporating robot state and sensor signals, such as object pose or tactile feedback, to advance VLA models toward more precise and versatile robot control. 

8 

**Contrastive Representation Regularization for Vision-Language-Action Models** 

# **Impact Statement** 

This paper presents a work to advance robot manipulation with vision-language-action models. The societal implications of this work are consistent with those commonly associated with research on robotic learning systems, including safe deployment and appropriate use in real-world environments. We do not foresee any unique ethical concerns arising from this work beyond those commonly encountered in research on robotic learning. 

# **Acknowledgments** 

This work was partly supported by Institute for Information & Communications Technology Planning & Evaluation (IITP) grant funded by the Korea government (MSIT) (RS-2019-II190075, Artificial Intelligence Graduate School Program (KAIST); RS-2024-00509279, Global AI Frontier Lab; RS-2025-02653113, High-Performance Research AI Computing Infrastructure Support at the 2 PFLOPS Scale), and RLWRLD Inc. We also thank Sihyun Yu for his valuable comments and suggestions in preparing an earlier version of the manuscript, and Suhyeok Jang for helpful support in conducting real-world experiments. 

- Chen, G., Li, Z., Wang, S., Jiang, J., Liu, Y., Lu, L., Huang, D.-A., Byeon, W., Le, M., Rintamaki, T., et al. Eagle 2.5: Boosting long-context post-training for frontier visionlanguage models. In _Advances in Neural Information Processing Systems_ , 2025. 

- Chen, T., Kornblith, S., Norouzi, M., and Hinton, G. A simple framework for contrastive learning of visual representations. In _International Conference on Machine Learning_ , 2020. 

- Driess, D., Xia, F., Sajjadi, M. S., Lynch, C., Chowdhery, A., Wahid, A., Tompson, J., Vuong, Q., Yu, T., Huang, W., et al. PaLM-E: An embodied multimodal language model. In _International Conference on Machine Learning_ , 2023. 

- Driess, D., Springenberg, J. T., Ichter, B., Yu, L., Li-Bell, A., Pertsch, K., Ren, A. Z., Walke, H., Vuong, Q., Shi, L. X., et al. Knowledge insulating vision-language-action models: Train fast, run fast, generalize better. In _Advances in Neural Information Processing Systems_ , 2025. 

- He, K., Fan, H., Wu, Y., Xie, S., and Girshick, R. Momentum contrast for unsupervised visual representation learning. In _IEEE Conference on Computer Vision and Pattern Recognition_ , 2020. 

# **References** 

- Azzolini, A., Bai, J., Brandon, H., Cao, J., Chattopadhyay, P., Chen, H., Chu, J., Cui, Y., Diamond, J., Ding, Y., et al. Cosmos-Reason1: From physical common sense to embodied reasoning. _arXiv preprint arXiv:2503.15558_ , 2025. 

- Bai, S., Chen, K., Liu, X., Wang, J., Ge, W., Song, S., Dang, K., Wang, P., Wang, S., Tang, J., et al. Qwen2.5-VL technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 

- Bjorck, J., Castañeda, F., Cherniadev, N., Da, X., Ding, R., Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al. GR00TN1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., et al. _π_ 0 _._ 5: A vision-language-action model with open-world generalization. In _Conference on Robot Learning_ , 2025a. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for general robot control. In _Robotics: Science and Systems_ , 2025b. 

- Cao, M., Tan, H., Ji, Y., Lin, M., Li, Z., Cao, Z., Wang, P., Zhou, E., Han, Y., et al. Robobrain 2.0 technical report. _arXiv preprint arXiv:2507.02029_ , 2025. 

- Huh, M., Cheung, B., Wang, T., and Isola, P. The platonic representation hypothesis. In _International Conference on Machine Learning_ , 2024. 

- Hung, C.-Y., Sun, Q., Hong, P., Zadeh, A., Li, C., Tan, U., Majumder, N., Poria, S., et al. Nora: A small opensourced generalist vision language action model for embodied tasks. _arXiv preprint arXiv:2504.19854_ , 2025. 

- Jang, J., Ye, S., Lin, Z., Xiang, J., Bjorck, J., Fang, Y., Hu, F., Huang, S., Kundalia, K., Lin, Y.-C., et al. Dreamgen: Unlocking generalization in robot learning through video world models. In _Conference on Robot Learning_ , 2025. 

- Jiang, Z., Xie, Y., Lin, K., Xu, Z., Wan, W., Mandlekar, A., Fan, L. J., and Zhu, Y. Dexmimicgen: Automated data generation for bimanual dexterous manipulation via imitation learning. In _IEEE International Conference on Robotics and Automation_ , 2025. 

- Khazatsky, A., Pertsch, K., Nair, S., Balakrishna, A., Dasari, S., Karamcheti, S., Nasiriany, S., Srirama, M. K., Chen, L. Y., Ellis, K., et al. DROID: A large-scale in-the-wild robot manipulation dataset. In _Robotics: Science and Systems_ , 2024. 

- Khosla, P., Teterwak, P., Wang, C., Sarna, A., Tian, Y., Isola, P., Maschinot, A., Liu, C., and Krishnan, D. Supervised contrastive learning. In _Advances in Neural Information Processing Systems_ , 2020. 

9 

**Contrastive Representation Regularization for Vision-Language-Action Models** 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. OpenVLA: An open-source visionlanguage-action model. In _Conference on Robot Learning_ , 2024. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. In _Robotics: Science and Systems_ , 2025. 

- Koo, M., Choi, D., Kim, T., Lee, K., Kim, C., Seo, Y., and Shin, J. HAMLET: Switch your vision-languageaction model into a history-aware policy. In _International Conference on Learning Representations_ , 2026. 

- Kornblith, S., Norouzi, M., Lee, H., and Hinton, G. Similarity of neural network representations revisited. In _International Conference on Machine Learning_ , 2019. 

- Laskin, M., Srinivas, A., and Abbeel, P. Curl: Contrastive unsupervised representations for reinforcement learning. In _International Conference on Machine Learning_ , 2020. 

- Lee, S.-W., Kang, X., Yang, B., and Kuo, Y.-L. Class: Contrastive learning via action sequence supervision for robot manipulation. In _Conference on Robot Learning_ , 2025. 

- Li, Q., Liang, Y., Wang, Z., Luo, L., Chen, X., Liao, M., Wei, F., Deng, Y., Xu, S., Zhang, Y., et al. CogACT: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 

- Liang, J., Tokmakov, P., Liu, R., Sudhakar, S., Shah, P., Ambrus, R., and Vondrick, C. Video generators are robot policies. _arXiv preprint arXiv:2508.00795_ , 2025. 

- Lipman, Y., Chen, R. T., Ben-Hamu, H., Nickel, M., and Le, M. Flow matching for generative modeling. In _International Conference on Learning Representations_ , 2023. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. LIBERO: Benchmarking knowledge transfer for lifelong robot learning. In _Advances in Neural Information Processing Systems_ , 2023a. 

- Liu, H., Li, C., Wu, Q., and Lee, Y. J. Visual instruction tuning. In _Advances in Neural Information Processing Systems_ , 2023b. 

- Liu, Q. Rectified flow: A marginal preserving approach to optimal transport. _arXiv preprint arXiv:2209.14577_ , 2022. 

- Luo, G., Yang, G., Gong, Z., Chen, G., Duan, H., Cui, E., Tong, R., Hou, Z., Zhang, T., Chen, Z., et al. Visual embodied brain: Let multimodal large language models see, think, and control in spaces. _arXiv preprint arXiv:2506.00123_ , 2025. 

- Ma, Y. J., Sodhani, S., Jayaraman, D., Bastani, O., Kumar, V., and Zhang, A. VIP: Towards universal visual reward and representation via value-implicit pre-training. In _International Conference on Learning Representations_ , 2023. 

- Mandlekar, A., Nasiriany, S., Wen, B., Akinola, I., Narang, Y., Fan, L., Zhu, Y., and Fox, D. Mimicgen: A data generation system for scalable robot learning using human demonstrations. In _Conference on Robot Learning_ , 2023. 

- Myers, V., He, A. W., Fang, K., Walke, H. R., HansenEstruch, P., Cheng, C.-A., Jalobeanu, M., Kolobov, A., Dragan, A., and Levine, S. Goal representations for instruction following: A semi-supervised language interface to control. In _Conference on Robot Learning_ , 2023. 

- Nair, S., Rajeswaran, A., Kumar, V., Finn, C., and Gupta, A. R3M: A universal visual representation for robot manipulation. In _Conference on Robot Learning_ , 2022. 

- Nasiriany, S., Maddukuri, A., Zhang, L., Parikh, A., Lo, A., Joshi, A., Mandlekar, A., and Zhu, Y. RoboCasa: Large-scale simulation of everyday tasks for generalist robots. In _Robotics: Science and Systems_ , 2024. 

- NVIDIA GEAR. GR00T N1.5: An improved open foundation model for generalist humanoid robots. https://research.nvidia.com/labs/ gear/gr00t-n1_5, 2025. 

- Oord, A. v. d., Li, Y., and Vinyals, O. Representation learning with contrastive predictive coding. _arXiv preprint arXiv:1807.03748_ , 2018. 

- Peebles, W. and Xie, S. Scalable diffusion models with transformers. In _IEEE International Conference on Computer Vision_ , 2023. 

- Pertsch, K., Stachowicz, K., Ichter, B., Driess, D., Nair, S., Vuong, Q., Mees, O., Finn, C., and Levine, S. FAST: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., et al. Learning transferable visual models from natural language supervision. In _International Conference on Machine Learning_ , 2021. 

- Rana, K., Melnik, A., and Sünderhauf, N. Contrastive language, action, and state pre-training for robot learning. _arXiv preprint arXiv:2304.10782_ , 2023. 

- Seo, Y., Kim, J., James, S., Lee, K., Shin, J., and Abbeel, P. Multi-view masked world models for visual robotic manipulation. In _International Conference on Machine Learning_ , 2023. 

10 

**Contrastive Representation Regularization for Vision-Language-Action Models** 

- Sermanet, P., Lynch, C., Chebotar, Y., Hsu, J., Jang, E., Schaal, S., and Levine, S. Time-contrastive networks: Self-supervised learning from video. In _IEEE International Conference on Robotics and Automation_ , 2018. 

- Shen, D., Zheng, M., Shen, Y., Qu, Y., and Chen, W. A simple but tough-to-beat data augmentation approach for natural language understanding and generation. _arXiv preprint arXiv:2009.13818_ , 2020. 

multimodal understanding and robot control with visionlanguage-action model. _arXiv preprint arXiv:2502.14420_ , 2025. 

   - Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , 2023. 

- Shukor, M., Aubakirova, D., Capuano, F., Kooijmans, P., Palma, S., Zouitine, A., Aractingi, M., Pascal, C., Russi, M., Marafioti, A., et al. SmolVLA: A vision-languageaction model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

- Suresh, V. and Ong, D. C. Not all negatives are equal: Label-aware contrastive loss for fine-grained text classification. In _Conference on Empirical Methods in Natural Language Processing_ , 2021. 

- Tschannen, M., Gritsenko, A., Wang, X., Naeem, M. F., Alabdulmohsin, I., Parthasarathy, N., Evans, T., Beyer, L., Xia, Y., Mustafa, B., et al. SigLIP 2: Multilingual vision-language encoders with improved semantic understanding, localization, and dense features. _arXiv preprint arXiv:2502.14786_ , 2025. 

- Weinzaepfel, P., Leroy, V., Lucas, T., Brégier, R., Cabon, Y., Arora, V., Antsfeld, L., Chidlovskii, B., Csurka, G., and Revaud, J. CroCo: Self-supervised pre-training for 3d vision tasks by cross-view completion. In _Advances in Neural Information Processing Systems_ , 2022. 

- Wen, J., Zhu, M., Zhu, Y., Tang, Z., Li, J., Zhou, Z., Li, C., Liu, X., Peng, Y., Shen, C., et al. Diffusion-vla: Generalizable and interpretable robot foundation model via self-generated reasoning. In _International Conference on Machine Learning_ , 2025. 

- Won, J., Lee, K., Jang, H., Kim, D., and Shin, J. Dual-stream diffusion for world-model augmented vision-languageaction model. _arXiv preprint arXiv:2510.27607_ , 2025. 

- Yang, S., Li, H., Chen, Y., Wang, B., Tian, Y., Wang, T., Wang, H., Zhao, F., Liao, Y., and Pang, J. Instructvla: Vision-language-action instruction tuning from understanding to manipulation. _arXiv preprint arXiv:2507.17520_ , 2025. 

- Zheng, R., Wang, J., Reed, S., Bjorck, J., Fang, Y., Hu, F., Jang, J., Kundalia, K., Lin, Z., Magne, L., et al. Flare: Robot learning with implicit world modeling. In _Conference on Robot Learning_ , 2025. 

- Zhou, Z., Zhu, Y., Zhu, M., Wen, J., Liu, N., Xu, Z., Meng, W., Cheng, R., Peng, Y., Shen, C., et al. Chatvla: Unified 

11 

**Contrastive Representation Regularization for Vision-Language-Action Models** 

# **A. Hardware Details and Computation Overhead** 

All experiments are conducted on a single node equipped with 2 _×_ NVIDIA A100-SXM4-80GB GPUs and 64 CPU cores. Unless otherwise noted, we use a global batch size of 64 and train for 60K optimization steps. 

To quantify the additional cost introduced by RS-CL, we measure both floating point operations (FLOPs) and wall-clock training time for our fine-tuning experiment in RoboCasa-Kitchen. Using a FLOPs profiler, we measure the forward FLOPs per sample during training. Table 6 summarizes the compute characteristics for a single training run. 

_Table 6._ Compute overhead of RS-CL. We report estimated forward FLOPs per sample and total training time for 60K steps with global batch size 64. 

|Method|FLOPs / sample (forward)|Training time (hrs)|
|---|---|---|
|Baseline|2_._576_×_10<sup>12</sup>|23.06|
|RS-CL|2_._909_×_10<sup>12</sup>|23.49|


The additional wall-clock cost introduced by RS-CL is negligible (+1 _._ 25%), because the _view-cutoff_ augmentation operates directly on the VLM embeddings and RS-CL only adds a lightweight projection head and soft contrastive loss on top of the backbone forward pass. In particular, it does not require extra forward passes through the VLM backbone or longer token sequences, so the dominant compute costs of training remain essentially unchanged. 

# **B. Simulation Experiment Details** 

## **B.1. Dataset** 

For RoboCasa-Kitchen, we use the publicly available dataset<sup>1</sup> containing 3000 demonstrations generated with MimicGen (Mandlekar et al., 2023). For LIBERO, we use the publicly available dataset<sup>2</sup> , consisting of all 270K samples from LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and LIBERO-Long, re-rendered by Kim et al. (2024). 

## **B.2. Training and Evaluation Details** 

For fine-tuning experiments on GR00T N1.5 (NVIDIA GEAR, 2025), we employ the publicly available pre-trained checkpoint<sup>3</sup> . We follow the original training and inference recipe of NVIDIA GEAR (2025), including the prior distribution _p_ ( _s_ ) = Beta(<sup>_<u>a−</u>_</sup> _a_<sup>_<u>s</u>_; 1</sup><sup>_._5</sup><sup>_,_1)</sup><sup>_, a_= 0</sup><sup>_._999 for sampling the flow-matching timestep</sup><sup>_s_in equation 1.All models are trained with</sup> the _new_embodiment_ tag. We omit the use of future tokens (Zheng et al., 2025), as they are beyond the scope of this work. 

For RoboCasa-Kitchen, we train for 60K gradient steps with a global batch size of 64, using AdamW with a learning rate of 1e-4 under a cosine decay schedule and 3K warmup steps. For LIBERO, we adopt a smaller global batch size of 32, as this setting yields better performance in practice. 

For _π_ 0 and _π_ 0-FAST, we use the pre-trained checkpoints<sup>45</sup> to reproduce fine-tuned performance on RoboCasa-Kitchen. We train _π_ 0 for 60K steps and _π_ 0-FAST for 30K steps, both with a global batch size of 64. We set the learning rate to 2.5e-5 with cosine decay to 2.5e-6 and 1K warmup steps. At inference, we use an action horizon _H_ = 16 and execute all actions without re-planning. 

For RoboCasa-Kitchen, we evaluate all models with 1200 trials. For LIBERO, we evaluate 50 trials for each task, following Kim et al. (2024). 

> 1https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-GR00T-X-Embodiment-Sim 

> 2https://huggingface.co/datasets/physical-intelligence/libero 

> 3https://huggingface.co/nvidia/GR00T-N1.5-3B 

> 4gs://openpi-assets/checkpoints/pi0_base 

> 5gs://openpi-assets/checkpoints/pi0_fast_base 

12 

**Contrastive Representation Regularization for Vision-Language-Action Models** 

## **B.3. Analysis Details** 

**TCN implementation details.** TCN learns embeddings by pulling temporally adjacent observations together while pushing apart observations from distant timesteps. Since recent VLA models consume multi-view observations (NVIDIA GEAR, 2025; Black et al., 2025b) in a single forward pass, the multi-view TCN variant samples negatives from timesteps outside a temporal margin range, while positives are generated by zeroing out a randomly selected camera view. The single-view TCN variant follows the original formulation, drawing positives from a nearby temporal window and negatives from a distant temporal window. Following the original work (Sermanet et al., 2018), we set the temporal margin for defining positive/negative pairs to 0.2s. 

**Soft label target distance definition.** For the ablation study on soft label targets in Sec. 3.3, we define distances as follows. For next single action and current state, we use Euclidean distance. For next action sequence, we use Dynamic Time Warping (DTW), which measures similarity between temporal sequences that may vary in speed. DTW requires an additional temperature hyperparameter _γ_ , which we set to 10.0. The soft weight temperature _β_ and similarity temperature _τ_ are fixed at 1.0 and 0.2, respectively. 

**CKNNA measurement.** CKNNA (Huh et al., 2024) is a nearest-neighbor variant of kernel alignment (Kornblith et al., 2019). We randomly sample 10 trajectories per task in RoboCasa-Kitchen, totaling 240 trajectories. Each trajectory is processed with a window size of 16, yielding 4415 transitions. We extract the embeddings from the adapter module _fϕ_ (used as conditioning inputs to the action decoder) along with the corresponding proprioceptive states. We follow the implementation of Huh et al. (2024) and report results with _k_ = 10, measuring the alignment between proprioceptive states and conditional representations in the VLA model. 

**KNN task-phase classification.** We perform a cross-scene KNN task-phase classification experiment on identical manipulation trajectories replayed in different visual environments. For each trajectory, we first align the executions across scenes using Dynamic Time Warping (DTW), and discretize the aligned time axis into 32 shared task-progress classes. Each timestep is assigned a scene-invariant phase label describing where it lies in the overall execution of the task. Given a trained model, we extract the conditioning representation at each timestep and evaluate how well it encodes task progress under visual changes by training a KNN classifier in this representation space to predict the phase labels. We compare four feature choices: (i) the pre-trained VLM representation without any robot-action training, (ii) the representation from a model trained only with the action prediction loss (baseline), (iii) the representation from a model trained with RS-CL, and (iv) the ground-truth proprioceptive state, which serves as an upper-bound reference for phase information. We use a KNN classifier with k = 5. 

## **B.4. Implementation Details for From-Scratch VLA Training** 

We attach a randomly initialized action decoder to various pre-trained VLMs, with a lightweight adapter module _fϕ_ in between. Following NVIDIA GEAR (2025), we define VLM( **O**<sup>_V_</sup> _t_<sup>_,_</sup><sup>**c**) as the hidden representation from layer 12 out of 36</sup> layers for Qwen2.5-VL-3B variants and the GR00T N1.5 backbone. For Qwen2.5-VL-7B, we extract VLM( **O**<sup>_V_</sup> _t_<sup>_,_</sup><sup>**c**) from</sup> layer 18 out of 28, which yields higher performance in our layer ablation study on LIBERO (see Table 7). For SigLIP, we instead use the final hidden representation as the condition embedding. 

As the action decoder, we adopt a 16-layer DiT with 0.5B parameters. Empirically, we find that omitting a projection layer to reduce embedding dimensionality before conditioning improves performance (see Table 7). Accordingly, we do not apply such a layer. Instead, for Qwen2.5-VL-7B variants, we use a larger attention dimension that matches its hidden size _d_ model = 3584, while Qwen2.5-VL-3B uses _d_ model = 2048. 

_Table 7._ **Hidden layer ablations on Qwen2.5-VL-7B backbone.** We report success rates (%) on the LIBERO benchmark, varying the hidden layer index used as the conditioning representation for VLA models trained from scratch. 

|Layer|Spatial|Object|Goal|Long|Avg.|
|---|---|---|---|---|---|
|12 (with projection)|87.4|94.2|41.8|40.4|66.0|
|18 (with projection)|86.8|83.4|61.6|44.0|69.0|
|**18 (no projection)**|85.2|89.4|73.2|36.2|**71.0**|
|24 (with projection)|85.2|89.4|73.2|36.2|57.0|


13 

**Contrastive Representation Regularization for Vision-Language-Action Models** 

# **C. Real-Robot Experiment Details** 

## **C.1. Hardware Platform** 

We use Franka Research 3, a 7-DoF robotic arm equipped with a Robotiq 2F-85 gripper, following the setup of Khazatsky et al. (2024). For visual perception, we utilize the dual camera setup: a movable Stereolabs ZED 2 provides a global view, and a wrist-mounted ZED Mini captures a close-range view. Teleoperated demonstrations are collected using an Oculus Quest 2, and we log time-synchronized RGB images, joint states, and gripper width for training and evaluation. Demonstrations are recorded at 10 Hz. 

## **C.2. Real-Robot Tasks** 

The in-domain and generalization tasks (visual, physical generalization, and language grounding) along with their corresponding prompts and representative key frames from the real-world evaluation, are shown in Fig. 9– 13. 

**In-domain tasks.** We introduce four pick-and-place tasks (Box to Bowl, Box to Plate, Basket to Bowl, Plate to Basket), with varied objects (teddy bear, blue cube, blue cup, yellow sponge) for each task (see Fig. 9). 

**Visual generalization.** We use in-domain objects differing in color ( _e.g._ , changing a blue cube to a green cube, or a yellow sponge to a blue sponge), and introduce background variations by changing the tabletop covering or the target container (see Fig. 10). 

**Physical generalization.** We evaluate with unseen objects not used in training, including a yellow banana, purple grapes, red strawberry, and a yellow cup. The yellow cup has a different shape and texture from the blue cup used in training. (see Fig. 11). 

**Language grounding.** We place two objects that are seen at training at the pick-up location, and specify which one to pick and place at target location (see Fig. 12). 

**Lighting generalization.** We evaluate on in-domain tasks under significantly darker lighting conditions than those used in training (see Fig. 13). 

## **C.3. Real-World Training and Evaluation Details** 

**Dataset.** We collect 60 demonstrations for each pick-and-place task and close lid task, resulting in 300 expert demonstrations. 

**Training.** We jointly train a model with the 4 pick-and-place tasks, and another model for the close-lid task. For pick-andplace, we employ a cartesian action space with proprioceptive states, and for the close-lid task we use a joint action space to cover various configurations in manipulation. 

**Evaluation.** For real-robot evaluation, we report the average success rate over 24 trials for each pick-and-place task, with varied objects. In the close-lid task, outcomes are classified as full success (lid fully closed), partial success (partially closed), or failure (not closed). For physical generalization, we evaluate with unseen objects (yellow banana, purple grapes, red strawberry, yellow cup), with success defined as the accurate completion of the pick-and-place. We define language following as whether the gripper approaches the correct object, and task success as completing the instructed pick-and-place. 

14 

**Contrastive Representation Regularization for Vision-Language-Action Models** 


_Figure 9._ Real-world in-domain tasks. 


_Figure 10._ Real-world visual generalization tasks. 

15 

### **Contrastive Representation Regularization for Vision-Language-Action Models** 


_Figure 13._ Real-world lighting variation tasks. 

16 

**Contrastive Representation Regularization for Vision-Language-Action Models** 

# **D. Hyperparameters** 

We detail the hyperparameter choices used for RS-CL and analyze the sensitivity of the method to its main components. Unless otherwise specified, we initialize the weighting coefficient _λ_ for _L_ RS-CL to 1.0 and decay it to 0 following a cosine schedule over the total training steps. This design emphasizes representation refinement in the early stages of training, while gradually shifting the focus toward accurate action prediction in later stages. 

We set the similarity temperature _τ_ to 0.2 and the distance-based soft weighting temperature _β_ to 1.0 across all experiments. As summarized in Table 8, RS-CL exhibits stable performance over a wide range of hyperparameter values, including different _λ_ schedules, temperature settings, projection dimensions, batch sizes, and random seeds. These results indicate that the proposed method is robust and does not rely on precise hyperparameter tuning to achieve strong performance. 

_Table 8._ **Hyperparameter ablations.** Average success rate (%) on RoboCasa-Kitchen with 30 demonstrations. Baseline performance without RS-CL is 48.2. The selected settings in the main experiments are highlighted in **bold** . 

|**Hyperparameter**|**Setting**|**Avg. SR**|
|---|---|---|
|Baseline|-|48.2|
|_λ_schedule|1_._0_→_0(cosine)|**53.0**|
||Fixed (_λ_= 1_._0/0_._5)|50.7 / 51.0|
|Similarity temp. _τ_|0.01 / 0.02 / 0.05 / 0.1 / 1.0|51.6 / 53.0 / 52.0 /**53.3**/ 51.1|
|Distance temp. _β_|0.1 / 1.0 / 10.0|51.2 /**53.0**/ 49.8|
|Projection dim|64 / 128 / 256|50.9 /**53.0**/ 51.2|
|Batch size|Baseline (32 / 64)|48.4 / 48.2|
||RS-CL (32 / 64)|51.5 /**53.0**|
|Training Seeds|Baseline (0 / 7 / 42)<br>RS-CL (0 / 7 / 42)|49.2 / 48.8 / 48.2<br>54.7 / 51.3 /**53.0**|


17 

**Contrastive Representation Regularization for Vision-Language-Action Models** 

# **E. Further Analysis** 

## **E.1. Detailed Visualizations of VLM Representations** 


_Figure 14._ **Detailed visualizations of VLM representations. (a)** We visualize VLM embeddings of robot episodes performing the same task “Open the microwave / cabinet door” across different scenes in RoboCasa-Kitchen. Pre-trained VLM representations form distinct clusters primarily based on visual appearance, and the task/timestep progress trajectories ( _i.e._ , gray lines starting from blue to yellow dots) are not consistently aligned across these clusters. **(b)** With RS-CL, the representations still preserve scene-dependent grouping, but the task progress becomes geometrically aligned across groups ( _i.e._ , from bottom toward the top-left region), indicating that episodes from different environments share a common progression direction in the embedding space. 

We provide a more detailed explanation of Fig. 2 using the additional visualizations in Fig. 14. In the pre-trained VLM representation (Fig. 14a, we observe four prominent clusters ( _i.e._ , G1–G4) that are clearly grouped by scene layout. Specifically, G1 corresponds to scenes where a flat, wide tabletop occupies most of the space in front of the robot; G2 to scenes with a tabletop in front and a stove or burner at the front right; G3 to scenes dominated by a stove or burner directly in front of the robot; and G4 to scenes where an oven is positioned in front of the robot. These clusters are thus primarily induced by the most visually dominant objects in the scene. However, the underlying task, “Open the microwave / cabinet door,” mainly requires the robot arm to move upward and reach an overhead door in front of the robot, which is largely independent of these dominant background objects. Consistent with this mismatch, the timestep-indexed task progress trajectories ( _i.e._ , gray lines from blue to yellow) do not align across clusters, indicating that the pre-trained VLM embeddings are organized by visual appearance rather than by control-relevant task progress. 

In contrast, Fig. 14b shows the condition representations of the VLA model trained with RS-CL. While episode embeddings from different scenes still form partially separated groups, the common task progress becomes geometrically aligned across these groups. Trajectories consistently evolve from the bottom toward the top-left region of the embedding space. This suggests that RS-CL reshapes the conditioning representation to be more robot-state centric, so that episodes at similar task phases are aligned even when they come from visually distinct environments, while still preserving the semantic grouping from the pre-trained VLM. 

## **E.2. Quantitative Analysis of Representation Structure** 

To complement the qualitative visualizations in Fig. 14, we quantify how the representations are organized by measuring KNN classification accuracy ( _k_ = 5) on the embeddings. We report (i) _scene classification accuracy_ , predicting the scene cluster (G1–G4 in Fig. 14a), and (ii) _task-progress classification accuracy_ , predicting the discretized task phase. We additionally report results on the raw proprioceptive state as a natural reference for task-progress structure. 

As shown in Table 9, pre-trained VLM embeddings achieve near-perfect scene accuracy (99.6%) but near-chance taskprogress accuracy (1.2%), confirming that they are organized by visual appearance rather than control-relevant task progress. RS-CL substantially improves task-progress structure (1.2% _→_ 22.9%), approaching the proprioceptive-state reference (25.6%), while largely preserving scene information (93.6%). This shows that RS-CL effectively transfers the task-progress structure implicit in proprioceptive states into the VLM representation, consistent with the trajectory alignment in Fig. 14b. 

18 

**Contrastive Representation Regularization for Vision-Language-Action Models** 

_Table 9._ **KNN classification accuracy (%) on the representation space.** Pre-trained VLM representations are dominated by scenedependent visual appearance and carry almost no task-progress information. RS-CL substantially improves task-progress structure, nearly matching the proprioceptive-state reference, while preserving most of the scene information from the pre-trained VLM. 

|Representation|Scene Acc.(%)|Task progress Acc.(%)|
|---|---|---|
|Pre-trained VLM embeddings|99.6|1.2|
|Embeddings trained with RS-CL|93.6|22.9|
|Ground-truth proprioceptive states|53.1|25.6|


## **E.3. Adaptation to another VLA Architecture** 

To verify that RS-CL remains effective regardless of the underlying action modeling paradigm of the baseline VLA model, we apply it to _π_ 0-FAST (Pertsch et al., 2025), an autoregressive VLA model that predicts action tokens via next-token prediction instead of flow matching. Under the RoboCasa-Kitchen fine-tuning setting, _π_ 0-FAST with RS-CL improves performance across all demonstration counts (see Table 10). These results suggest that, as long as the VLA model conditions its policy on a large-scale pre-trained VLM backbone, RS-CL is a broadly applicable and beneficial regularization strategy, independent of the specific action modeling design. 

_Table 10._ **RoboCasa-Kitchen benchmark success rate (%).** Results include fine-tuned performance of _π_ 0-FAST (Pertsch et al., 2025), an autoregressive VLA model and GR00T N1.5 (NVIDIA GEAR, 2025), an flow-matching VLA model, with RS-CL. Best results within the same backbone indicated in **bold** . 

|Method|30 demos|100 demos|300 demos|
|---|---|---|---|
|_π_0-FAST (Autoregressive)|29.8|60.2|63.6|
|**+ RS-CL (Ours)**|**33.2**|**61.1**|**65.2**|
|GR00T N1.5 (Flow-Matching)|48.2|63.9|65.7|
|**+ RS-CL (Ours)**|**53.0**|**67.2**|**69.7**|


## **E.4. Applicability across Proprioceptive State Configurations** 

Different robots naturally provide different proprioceptive state representations. To examine the applicability of RS-CL across such variations, we evaluate it under different state configurations on RoboCasa-Kitchen (Nasiriany et al., 2024) and on more complex embodiments in DexMimicGen (Jiang et al., 2025), while keeping the rest of the framework unchanged. 

**State definition on RoboCasa-Kitchen.** We compare two natural choices for the proprioceptive state: end-effector pose (the default in the baseline VLA framework) and joint position. As shown in Table 11(a), RS-CL consistently improves over the baseline under both choices, with joint position yielding slightly stronger gains. This indicates that the benefit does not depend on a particular state parameterization. 

**Higher-dimensional state spaces on DexMimicGen.** We further evaluate RS-CL on more complex embodiments in DexMimicGen: bimanual Panda arms with two Inspire Hands (38-dim state) and the GR-1 humanoid platform performing upper-body manipulation (36-dim state). As shown in Table 11(b), RS-CL provides consistent improvements in both settings, showing that its benefit extends to higher-dimensional and more complex proprioceptive configurations. 

_Table 11._ **RS-CL across diverse proprioceptive state configurations.** RS-CL consistently improves over the baseline across (a) different state definitions on RoboCasa-Kitchen and (b) more complex embodiments with higher-dimensional state spaces on DexMimicGen. 

|_(a)_Success rate (%) on RoboCasa-|Kitchen (30 demos).|_(b)_Success|rate (%) on DexMimicG|en.|
|---|---|---|---|---|
|Method|Success rate|Method<br>Bi|manual Panda + Hands|GR-1 Humanoid|
|Baseline|48.2|Baseline|52.7|68.9|
|**+ RS-CL (EEF pose)**|53.0|**+ RS-CL (Ours)**|**57.3**|**73.1**|
|**+ RS-CL (Joint position)**|**53.4**||||


19 

**Contrastive Representation Regularization for Vision-Language-Action Models** 

## **E.5. Task-wise Analysis** 

To better understand where RS-CL contributes most, we break down the RoboCasa-Kitchen success rates by task group: pick-and-place, open-and-close, and others ( _e.g._ , twisting knobs or insertion). As shown in Table 12, RS-CL provides the largest gains on pick-and-place tasks (+4 _._ 2 to +11 _._ 4%) and on twisting/insertion tasks (+3 _._ 8 to +5 _._ 4%), with relatively smaller improvements on open-and-close tasks ( _−_ 1 _._ 3 to +1 _._ 0%). 

_Table 12._ **RoboCasa-Kitchen success rate (%) by task group.** Main numbers are results for 30 demonstrations, with 300-demonstration results in parentheses. Full per-task results are provided in Table 13. 

|Method|Pick and Place|Open and Close|Others (_e.g._, twisting, insertion)|
|---|---|---|---|
|Baseline|30.1 (55.6)|**71.3**(84.7)|48.2 (62.6)|
|**+ RS-CL (Ours)**|**41.5**(**59.8**)|70.0 (**85.7**)|**52.0**(**68.0**)|


We attribute this pattern to structural differences across task groups. Open-and-close tasks involve a constrained action space ( _e.g._ , swinging a door or drawer along a fixed axis), where the baseline representation already performs strongly and leaves limited room for improvement. In contrast, pick-and-place tasks involve diverse state-to-action mappings due to varying initial and goal placements, and twisting/insertion tasks require precise state-dependent control near contact points. RS-CL’s state-aware representation provides more informative supervision in these cases, translating into larger performance gains. 

## **E.6. Discussion** 

**Limitations.** While RS-CL explicitly leverages proprioceptive states to align the representation space, it does not incorporate further signals in robotic manipulation, such as object poses or contact forces. These modalities often provide complementary information that is captured by robot’s proprioception state. Extending RS-CL to integrate such modalities into the representations, represents a promising direction for future research. **Future directions.** One promising extension is to apply RS-CL to settings with more complex proprioceptive spaces, such as humanoid robots or dexterous hand manipulation tasks. These domains involve high-dimensional and complex state representations, where aligning VLM embeddings with proprioceptive signals may be even more beneficial for accurate action prediction. 

20 

**Contrastive Representation Regularization for Vision-Language-Action Models** 

# **F. More Quantitative Results** 

In this section, we report detailed task-wise results of our main experiments. Table 13 reports RoboCasa-Kitchen success rates of GR00T N1.5 trained with and without RS-CL, Table 14 reports our reproduced results of _π_ 0 and _π_ 0-FAST on the same benchmark, and Table 15 reports task-wise results of the from-scratch experiments across various VLM backbones. 

_Table 13._ **Detailed results on RoboCasa-Kitchen.** Task-wise success rates of GR00T N1.5 (NVIDIA GEAR, 2025) trained with, and without RS-CL, by different number of demonstrations. 

|Task|G|R00T N1.5 (_L_|FM)|GR00T|N1.5 (_L_FM+|_λL_RS-CL)|
|---|---|---|---|---|---|---|
||30 demos|100 demos|300 demos|30 demos|100 demos|300 demos|
|RoboCasa Kitchen (24 tasks, PnP|= Pick-and-P|lace)|||||
|Close Double Door|44.0|86.0|80.0|54.0|78.0|86.0|
|Close Drawer|96.0|96.0|96.0|96.0|96.0|96.0|
|Close Single Door|98.0|94.0|98.0|88.0|98.0|98.0|
|Coffee Press Button|70.0|82.0|90.0|86.0|94.0|92.0|
|Coffee Serve Mug|64.0|72.0|58.0|74.0|66.0|70.0|
|Coffee Setup Mug|28.0|34.0|24.0|30.0|54.0|46.0|
|Open Double Door|80.0|92.0|82.0|72.0|80.0|84.0|
|Open Drawer<br>|46.0<br>|58.0<br>|74.0<br>|44.0<br>|54.0<br>|76.0<br>|
|Open Single Door|64.0|58.0|78.0|66.0|60.0|74.0|
|PnP from Cab_→_Counter|28.0|42.0|54.0|38.0|54.0|60.0|
|PnP from Counter_→_Cab|36.0|54.0|54.0|40.0|58.0|68.0|
|PnP from Counter_→_Microwave|30.0|36.0|32.0|34.0|40.0|40.0|
|PnP from Counter_→_Sink|28.0|66.0|58.0|40.0|60.0|68.0|
|PnP from Counter_→_Stove|38.0|60.0|66.0|38.0|74.0|72.0|
|PnP from Microwave_→_Counter|24.0|44.0|50.0|46.0|50.0|48.0|
|PnP from Sink_→_Counter|40.0|52.0|60.0|54.0|62.0|68.0|
|PnP from Stove_→_Counter|22.0|60.0|68.0|42.0|66.0|54.0|
|Turn Off Microwave|62.0|86.0|94.0|62.0|84.0|94.0|
|Turn Off Sink Faucet|72.0|86.0|92.0|70.0|94.0|88.0|
|Turn Off Stove|10.0|14.0|28.0|10.0|8.0|28.0|
|Turn On Microwave|44.0|58.0|44.0|48.0|72.0|66.0|
|Turn On Sink Faucet|60.0|90.0|86.0|72.0|90.0|90.0|
|Turn On Stove|34.0|56.0|32.0|36.0|58.0|36.0|
|Turn Sink Spout|38.0|58.0|78.0|32.0|62.0|70.0|
|**Average**|**48.2**|**63.9**|**65.7**|**53.0**|**67.2**|**69.7**|


21 

**Contrastive Representation Regularization for Vision-Language-Action Models** 

_Table 14._ **Detailed results on RoboCasa-Kitchen.** Task-wise success rates (%) of reproduced _π_ 0 (Black et al., 2025b) and _π_ 0- FAST (Pertsch et al., 2025), by different number of demonstrations. 

|Task||_π_0|||_π_0-FAST||
|---|---|---|---|---|---|---|
||30 demos|100 demos|300 demos|30 demos|100 demos|300 demos|
|RoboCasa Kitchen (24 tasks,|PnP = Pick-a|nd-Place)|||||
|Close Double Door|68.0|86.0|86.0|44.0|84.0|78.0|
|Close Drawer|94.0|94.0|96.0|84.0|96.0|94.0|
|Close Single Door|94.0|98.0|96.0|84.0|90.0|72.0|
|Coffee Press Button|66.0|80.0|88.0|20.0|82.0|90.0|
|Coffee Serve Mug|80.0|66.0|64.0|44.0|66.0|68.0|
|Coffee Setup Mug|20.0|32.0|38.0|2.0|34.0|38.0|
|Open Double Door|92.0|90.0|84.0|26.0|68.0|78.0|
|Open Drawer|44.0|56.0|62.0|36.0|58.0|68.0|
|Open Single Door|58.0|64.0|70.0|44.0|70.0|66.0|
|PnP Cab_→_Counter|14.0|22.0|18.0|12.0|22.0|30.0|
|PnP Counter_→_Cab|32.0|44.0|46.0|8.0|58.0|48.0|
|PnP Counter_→_Microwave|26.0|30.0|18.0|10.0|32.0|20.0|
|PnP Counter_→_Sink|32.0|44.0|58.0|2.0|46.0|56.0|
|PnP Counter_→_Stove|14.0|32.0|60.0|10.0|50.0|64.0|
|PnP Microwave_→_Counter|16.0|20.0|24.0|4.0|38.0|46.0|
|PnP Sink_→_Counter|22.0|24.0|66.0|12.0|56.0|62.0|
|PnP Stove_→_Counter|10.0|46.0|44.0|18.0|62.0|60.0|
|Turn Off Microwave|64.0|84.0|96.0|68.0|98.0|96.0|
|Turn Off Sink Faucet|72.0|86.0|94.0|48.0|76.0|94.0|
|Turn Off Stove|14.0|10.0|22.0|0.0|18.0|22.0|
|Turn On Microwave|58.0|82.0|70.0|52.0|68.0|88.0|
|Turn On Sink Faucet|80.0|82.0|86.0|40.0|66.0|74.0|
|Turn On Stove|26.0|68.0|42.0|12.0|52.0|38.0|
|Turn Sink Spout|50.0|68.0|72.0|36.0|54.0|76.0|
|**Average**|**47.8**|**58.7**|**62.5**|**29.8**|**60.2**|**63.6**|


_Table 15._ **Detailed results of from-scratch experiments.** Task success rate (%) on the RoboCasa-Kitchen benchmark trained with 300 demonstrations. All models train a VLA from scratch, starting from each pre-trained VLM backbone. Best results within the same backbone indicated in **bold** . 

|Backbone Model|S|uccess Ra|te|
|---|---|---|---|
||PnP|Others|Avg.|
|Qwen2.5-VL-3B (Bai et al.,2025)|2.5|8.6|6.6|
|**+ RS-CL (Ours)**|**3.5**|**16.0**|**11.8**|
|NORA (Hung et al.,2025)|1.5|11.4|8.1|
|**+ RS-CL (Ours)**|**3.5**|**23.3**|**16.7**|
|RoboBrain2.0-3B (Cao et al.,2025)|2.8|13.9|10.2|
|**+ RS-CL (Ours)**|**5.8**|**19.6**|**15.0**|
|Qwen2.5-VL-7B (Bai et al.,2025)|2.5|12.4|9.1|
|**+ RS-CL (Ours)**|**9.8**|**21.1**|**17.3**|
|RoboBrain2.0-7B (Cao et al.,2025)|2.3|12.8|9.3|
|**+ RS-CL (Ours)**|**12.0**|**25.9**|**21.3**|
|VeBrain-7B (Luo et al.,2025)|3.0|10.9|8.3|
|**+ RS-CL (Ours)**|**7.8**|**20.3**|**17.6**|
|Cosmos-Reason-7B (Azzolini et al.,2025)|1.0|5.5|4.0|
|**+ RS-CL (Ours)**|**7.3**|**15.9**|**13.0**|
|SigLIP2 (Tschannen et al.,2025)|0.3|2.9|2.0|
|<br>**+ RS-CL (Ours)**|**0.8**|**3.5**|**2.6**|
|<br>SigLIP2, unfrozen backbone|3.3|4.4|4.0|
|<br>**+ RS-CL (Ours)**|**17.3**|**12.5**|**14.1**|
|GR00T N1.5 VLM (NVIDIA GEAR,2025)|37.5|62.0|53.8|
|**+ RS-CL (Ours)**|**37.8**|**66.3**|**56.8**|


22 

