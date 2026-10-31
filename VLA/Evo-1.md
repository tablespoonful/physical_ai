---
title: "Evo-1: Lightweight Vision-Language-Action Model with Preserved Semantic Alignment"
date: "2025-11-06"
authors: "Tao Lin; Yilei Zhong; Yuxin Du; Jingjing Zhang; Jiting Liu; Yinxinyu Chen"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2511.04555
pdf: https://arxiv.org/pdf/2511.04555
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.04555)** / [論文ページ](https://arxiv.org/abs/2511.04555)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **Evo-1: Lightweight Vision-Language-Action Model with Preserved Semantic Alignment** 

Tao Lin<sup>1</sup><sup>_,_2</sup><sup>_,_3</sup> Yilei Zhong<sup>1</sup> Yuxin Du<sup>1</sup><sup>_,_2</sup><sup>_,_3</sup> Jingjing Zhang<sup>1</sup> Jiting Liu<sup>1</sup> Yinxinyu Chen<sup>5</sup> Encheng Gu<sup>6</sup> Ziyan Liu<sup>1</sup> Hongyi Cai<sup>1</sup> Yanwen Zou<sup>1</sup><sup>_,_3</sup><sup>_,_4</sup> Lixing Zou<sup>1</sup> Zhaoye Zhou<sup>1</sup> Gen Li<sup>1</sup><sup>_,_3</sup><sup>_,_7</sup><sup>_†_</sup> Bo Zhao<sup>1</sup><sup>_,_2</sup><sup>_,_3</sup><sup>_†_</sup> 

1School of AI, Shanghai Jiao Tong University 2EvoMind Tech 3IAAR-Shanghai 4SII 5Carnegie Mellon University 6University of Cambridge 7Nanyang Technological University taolin200108@gmail.com, bo.zhao@sjtu.edu.cn https://github.com/MINT-SJTU/Evo-1 

## **1. Introduction** 

## **Abstract** 

_Vision-Language-Action (VLA) models have emerged as a powerful framework that unifies perception, language, and control, enabling robots to perform diverse tasks through multimodal understanding. However, current VLA models typically contain massive parameters and rely heavily on large-scale robot data pretraining, leading to high computational costs during training, as well as limited deployability for real-time inference. Moreover, most training paradigms often degrade the perceptual representations of the vision-language backbone, resulting in overfitting and poor generalization to downstream tasks. In this work, we present_ **_Evo-1_** _, a lightweight VLA model that reduces computation and improves deployment efficiency, while maintaining strong performance without pretraining on robot data. Evo-1 builds on a native multimodal Vision-Language model (VLM), incorporating a novel cross-modulated diffusion transformer along with an optimized integration module, together forming an effective architecture. We further introduce a two-stage training paradigm that progressively aligns action with perception, preserving the representations of the VLM. Notably, with only_ **_0.77 billion_** _parameters, Evo-1 achieves_ **_state-of-the-art_** _results on the MetaWorld and RoboTwin suite, surpassing the previous best models by 12.4% and 6.9%, respectively, and also attains a competitive result of 94.8% on LIBERO. In real-world evaluations, Evo-1 attains a 78% success rate with high inference frequency and low memory overhead, outperforming all baseline methods. We release code, data, and model weights to facilitate future research on lightweight and efficient VLA models._ 

In recent years, Vision-Language models (VLMs) [1, 2, 29, 37] have achieved remarkable progress in multimodal understanding and reasoning. Inspired by these advances, researchers have extended multimodal learning to robotic control, leading to the development of Vision-LanguageAction (VLA) models [6, 7, 12, 38]. VLA models integrate perception, language, and control, enabling robots to follow natural language instructions grounded in visual observations and perform diverse manipulation tasks with strong generalization across environments and embodiments. 

Despite their promising capabilities, existing VLA models face several critical limitations. First, their massive number of parameters, often reaching several billions, leads to substantial GPU memory usage and high computational costs during both training and inference. Second, their large computational overhead leads to a low control frequency, limiting the model’s real-time responsiveness in interactive robotic tasks. Third, the widely adopted end-to-end training paradigm often degrades the representation space of the vision-language backbone, leading to poor generalization and overfitting in downstream tasks. Fourth, the majority of these models strongly rely on long-duration training over large-scale robot datasets (e.g., OXE [24], DROID [11]), whose collection is labor-intensive and costly. 

In this work, we introduce Evo-1, a lightweight VLA model designed for low-cost training and real-time deployment. Evo-1 adopts a unified vision-language backbone [37] pretrained under a single-stage multimodal paradigm, where perceptual and linguistic representations are learned jointly without post-hoc alignment, enabling strong multimodal perception and understanding. This compact VLM design substantially reduces overall model scale, reducing GPU memory requirements and computational demands in both training and inference. On top of 

_†_ Corresponding authors. 

13397 

this backbone, we design a cross-modulated diffusion transformer that models continuous action trajectories, allowing efficient temporal reasoning for consistent motion generation. This design also contributes to the model’s compactness and greatly increases inference frequency, supporting responsive behavior in real-time interactive robotic scenarios. We further introduce an optimized integration module that aligns the fused vision-language representations with the proprioceptive information of robot, thereby enabling seamless incorporation of multimodal features into the subsequent control. To strike a balance between preserving the inherent multimodal representational capacity and enabling effective adaptation to downstream action generation, we propose a two-stage training paradigm that gradually aligns the perception and control modules while substantially mitigating distortion of the VLM’s semantic space. By preserving the inherited semantic space, the model demonstrates strong generalization and competitive results without robot data pretraining. 

Evo-1 achieves strong results across three challenging simulation benchmarks: it sets a new state-of-the-art on Meta-World (80.6%) and RoboTwin suite (37.8%), surpassing previous bests of 68.2% and 30.9%, respectively, and reaches 94.8% on LIBERO, demonstrating its adaptability in both single-arm and dual-arm manipulation tasks. In realworld evaluations on four representative robotic tasks, Evo1 achieves an overall success rate of 78%, consistently outperforming other baselines. It also delivers high inference frequency with a compact GPU memory utilization, demonstrating both computational efficiency and stable control in physical deployments. Our contributions are summarized as follows: 

1. **Lightweight and efficient architecture.** We propose Evo-1, a lightweight VLA architecture with only 0.77B parameters that reduces training cost and improves inference speed for real-time deployment on consumer-grade GPUs. 

2. **Semantic preservation for improved generalization.** We introduce a two-stage training paradigm that strikes a balance between preserving inherent multimodal understanding of the VLM and adapting it to downstream action generation, effectively enhancing generalization across diverse manipulation tasks. 

3. **Strong performance without robot data pretraining.** Extensive experiments in both simulation and real-world tasks demonstrate that Evo-1 achieves state-of-the-art performance without relying on large-scale robot data pretraining, substantially reducing the need for costly and labor-intensive data collection. 

## **2. Related Work** 

**Large-Scale Vision-Language-Action Models.** Recent research has advanced Vision-Language-Action (VLA) mod- 

els [6, 7, 12, 14, 17, 20, 21, 28, 31–33] that integrate perception, language, and control within a unified multimodal framework. These models extend pre-trained visionlanguage backbones [2, 4, 5, 22, 37] to predict robot actions, enabling impressive few-shot generalization across diverse manipulation tasks [13, 23]. Representative works such as OpenVLA [12] utilize large-scale demonstration data from the Open-X Embodiment dataset [24], achieving cross-embodiment transfer through discrete action modeling. _π_ 0 [7] adapts the PaliGemma [4] architecture with a flow-matching-based action expert for continuous control, while Hi-Robot [27] introduces hierarchical reasoning and dual-expert architectures for long-horizon planning. 

Although these models demonstrate remarkable performance and generalization, they commonly rely on large pretrained backbones with billions of parameters, leading to significant computational demands and limited feasibility for real-time robotic deployment. 

**Lightweight and Efficient Vision-Language-Action Models.** While large-scale VLA models achieve strong generalization, their substantial computational costs hinder practical deployment. To improve efficiency, recent studies [28, 30, 31] have explored compact architectures that retain multimodal reasoning with significantly fewer parameters. TinyVLA [31] proposes a sub-billion-parameter VLA framework that combines lightweight vision-language backbone with a diffusion-based policy decoder. SmolVLA [28] further emphasizes accessibility by employing a SmolVLM-2 [22] backbone and a compact flow-matching action expert, together with layer skipping, token reduction, and asynchronous inference. Although both models significantly improve efficiency and accessibility, their overall task performance and robustness remain less satisfactory in complex manipulation settings. 

Sharing the same goal of advancing efficient VLA modeling, our proposed Evo-1 further contributes to the development of lightweight yet effective architectures that eliminate large-scale pretraining while substantially reducing training cost, inference resource consumption, and deployment complexity, achieving strong and reliable performance across diverse robotic tasks. 

## **3. Method** 

### **3.1. Overview of Evo-1 Architecture** 

Evo-1 adopts a modular Vision-Language-Action (VLA) architecture that integrates perception, reasoning, and control within a unified yet computationally efficient framework. As illustrated in Figure 1, the architecture comprises three core components: (1) a **vision-language backbone** that encodes multimodal representations from visual observations and textual instructions; (2) a **cross-modulated diffusion transformer** that generates continuous control actions; and 

13398 


Figure 1. **Architecture of Evo-1.** The input RGB observations and language instructions are first encoded by a compact vision-language backbone. Their fused representations are aligned with the robot state through an optimized integration module and then processed by a cross-modulated diffusion transformer to generate actions. The right side shows results across three simulation benchmarks. 

(3) an **integration module** that bridges perception and control through efficient alignment of multimodal and proprioceptive representations. 

Together, these components form a unified perceptionlanguage-action pipeline. Given a set of multi-view visual inputs _{It_<sup>_i}N_</sup> _i_ =1<sup>,alanguageinstruction</sup><sup>_Lt_,andthe</sup> robot state **s** _t_ , the vision-language backbone produces multimodal representations that are propagated through the integration module and interact with the cross-modulated diffusion transformer to produce the final control output. The overall mapping can be expressed as: 


where **a** _t ∈_ R<sup>_da_</sup> denotes the continuous action vector executed at time _t_ , and _θ_ represents the learnable parameters of the entire model. This formulation summarizes the endto-end process of Evo-1, effectively bridging high-level semantic understanding and low-level motor control within a lightweight and computationally efficient framework. 

### **3.2. Model Design** 

#### **3.2.1. Vision-Language Backbone** 

Evo-1 employs the InternVL3-1B model [37] as its visionlanguage backbone, which was pretrained under a native multimodal paradigm. Unlike post-hoc alignment pipelines that retrofit text-only LLMs to handle images, InternVL3 jointly learns linguistic and visual understanding from large-scale multimodal and textual corpora, enabling tight cross-modal alignment and efficient feature fusion. 

The visual encoder adopts InternViT-300M [10], a lightweight transformer distilled from InternViT-6B through layer-wise negative cosine similarity loss. Each RGB observation _{It_<sup>_i}N_</sup> _i_ =1<sup>is resized to 448</sup><sup>_×_448 and passed</sup> through a pixel-unshuffle downsampling operation, reducing the number of visual tokens by 4 _×_ . This yields compact yet expressive patch embeddings that preserve spatial granularity and maintain generalization across diverse visual domains. 

The language branch leverages Qwen2.5-0.5B [3], a transformer-based decoder with 0.5B parameters. Despite its small size, it demonstrates strong capability in capturing diverse task semantics, including spatial, logical, and temporal relations from the instruction _Lt_ . 

For vision-language fusion, InternVL3-1B inserts patchlevel image embeddings into the token sequence by replacing a designated <img> placeholder token. The resulting fused sequence is processed by the shared transformer decoder, enabling joint reasoning over visual and linguistic context in a unified embedding space. 

The fused representation produced by the backbone is denoted as 


where **z** _t ∈_ R<sup>_dz_</sup> denotes the fused multimodal representation that jointly encodes visual and linguistic information, serving as the input to the integration module. To better adapt the pretrained VLM to embodied visuomotor tasks, we retain only the first 14 layers of the language branch, as intermediate layers have been empirically found to exhibit 

13399 

stronger cross-modal alignment between visual and linguistic features [28], making them more effective for visuomotor control. 

#### **3.2.2. Cross-modulated Diffusion Transformer** 

Evo-1 adopts a conditional denoising module as action expert to predict continuous control actions from the fused multimodal embedding produced by the vision-language backbone. Following the flow-matching paradigm [15, 18], it learns a time-dependent vector field that progressively transforms an initial noisy action into the ground-truth target. 

Specifically, the action expert is implemented as a Diffusion Transformer (DiT) [25] that solely relies on stacked cross-attention layers, in contrast to the alternating selfattention and cross-attention structure adopted by prior VLA models [7, 28]. Each noisy action sequence **A**<sup>_τ_</sup> _t_<sup>is gen-</sup> erated by linearly interpolating between the ground-truth action **A** _t_ and a randomly sampled noise vector **_ϵ_** : 


Figure 2. **Comparison of vision-language attention maps after training.** (a) Evo-1 (InternVL3-1B) yields spatially consistent and semantically aligned activations. (b) OpenVLA (Prismatic7B) shows degraded coherence in attention maps. 


The interpolation weight _τ_ is sampled from a Beta distribution and clamped to the range [0 _._ 02 _,_ 0 _._ 98] to ensure numerical stability during training. 

During training, the action expert is optimized to learn a time-conditioned velocity field **v** _θ_ that drives the interpolated action **A**<sup>_τ_</sup> _t_<sup>towardtheground-truthaction</sup><sup>**A**</sup><sup>_t_under</sup> the multimodal context **z** _t_ and robot state **s** _t_ . The objective follows the flow-matching formulation [15, 18], defined as: 

both the perceptual embedding and the robot’s proprioceptive state, we concatenate **z** _t_ with the robot state **s** _t_ instead of projecting them into a shared embedding space. This concatenated feature serves as the key-value input for the transformer blocks of the action expert, providing a global and information-preserving context for action generation. Additional integration variants and their comparative results are detailed in the ablation studies (Sec. 4.4). 

### **3.3. Two-Stage Training Procedure** 

_L_<sup>_τ_</sup> ( _θ_ ) = E _p_ ( **A** _t|_ **z** _t,_ **s** _t_ ) _, q_ ( **A**<sup>_τ_</sup> _t_<sup>_|_</sup><sup>**A**</sup><sup>_t_)</sup> � _∥_ **v** _θ_ ( **A**<sup>_τ_</sup> _t_<sup>_,_</sup><sup>**z**</sup><sup>_t,_</sup><sup>**s**</sup><sup>_t_)</sup><sup>_−_</sup><sup>**u**(</sup><sup>**A**</sup><sup>_τ_</sup> _t_<sup>_|_</sup><sup>**A**</sup><sup>_t_)</sup><sup>_∥_2�</sup> _,_ (4) where **u** ( **A**<sup>_τ_</sup> _t_<sup>_|_</sup><sup>**A**</sup><sup>_t_)denotesthetargetflowdirectionthat</sup> guides **A**<sup>_τ_</sup> _t_<sup>toward</sup><sup>**A**</sup><sup>_t_.</sup> 

At inference time, the final action chunk **A** ˆ _t_ = [ˆ **a** _t,_ ˆ **a** _t_ +1 _, . . . ,_ ˆ **a** _t_ + _H−_ 1] is predicted by the action expert, conditioned on the fused representation **z** _t_ , the current robot state **s** _t_ , and the interpolated action **A**<sup>_τ_</sup> _t_<sup>.</sup> 


where _f_ AE denotes the conditioned action expert network that generates a sequence of _H_ future actions aiming to approximate the ground-truth action sequence **A** _t_ . 

#### **3.2.3. Integration Module** 

Evo-1 adopts a cross-attention-based integration module to effectively fuse multimodal and proprioceptive information before conditioning the Cross-modulated Diffusion Transformer. The fused multimodal representation **z** _t_ is extracted from the 14<sup>th</sup> layer of the vision-language backbone, capturing intermediate-level semantics that balance visual and linguistic features. To preserve the complete information from 

To strike a balance between preserving the inherent multimodal understanding of the vision-language backbone and adapting it to downstream action generation, we adopt a two-stage training paradigm. Preserving the pretrained multimodal semantics is essential for maintaining the generalization ability of the model across diverse visual-linguistic contexts, preventing overfitting to specific manipulation tasks. At the same time, effective adaptation to action generation is necessary to ensure that the fused perceptual representations can accurately guide the diffusion-based action expert, thereby improving task success rates in downstream control. Direct end-to-end training would risk disrupting the pretrained representations, reducing the model’s inherent multimodal understanding and leading to overfitting on specific downstream tasks, which ultimately compromises its generalization ability. 

**Stage 1: Action Expert Alignment.** In the first stage, we freeze the entire vision-language backbone and exclusively train the action expert along with the integration module. This setup allows the randomly initialized weights in action expert to gradually align with the multimodal embedding space without back-propagating noisy gradients into 

13400 

|**Benchmark**|**Models**|**Params**|**Robo-Pretrain**||**Suc**|**cess Rate (%)**|||
|---|---|---|---|---|---|---|---|---|
|**Meta-World**||||**Easy**|**Medium**|**Hard**|**Very Hard**|**Avg.**|
||Diffusion Policy [9]|-|No|23.1|10.7|1.9|6.1|10.5|
||<br>TinyVLA-H [31]|1.3B<br>|No|77.6|21.5|11.4|15.8|31.6|
||_π_0[7]|3.5B|Yes|71.8|48.2|41.7|30.0|47.9|
||SmolVLA [28]|2.25B|No|87.1|51.8|70.0|64.0|68.2|
||**Evo-1 (Ours)**|0.77B|No|**89.2**|**76.8**|**77.2**|**79.2**|**80.6**|
|**LIBERO**||||**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
||OpenVLA [12]|7B|Yes|84.7|88.4|79.2|53.7|76.5|
||CoT-VLA [35]|7B|Yes|87.5|91.6|87.6|69.0|81.1|
||_π_0-FAST [26]|3.5B|Yes|96.4|96.8|88.6|60.2|85.5|
||SmolVLA [28]|2.25B|No|93.0|94.0|91.0|77.0|88.8|
||GR00T N1 [6]|2B|Yes|94.4|97.6|93.0|90.6|93.9|
||_π_0[7]|3.5B|Yes|**96.8**|**98.8**|95.8|85.2|94.2|
||**Evo-1 (Ours)**|0.77B|No|92.7|97.7|**96.3**|**92.3**|**94.8**|
|**RoboTwin**||||**Click Alarmclock**|**Dump Bin Bigbin**|**Place Bread Basket**|**Place Can Basket**|**Avg.**|
|||||easy_|_hard<br>|easy_|_hard<br>|easy_|_hard<br>|easy_|_hard<br>||
||ACT [36]|-|No|32.0_|_ 4.0|68.0_|_ 1.0|6.0_|_0.0|1.0_|_0.0|14.0|
||Diffusion Policy [9]|-|No|<br>61.0_|_ 5.0|<br>49.0_|_ 0.0|<br>14.0_|_0.0|<br>18.0_|_0.0|18.4|
||RDT [19]|1.2B|Yes|61.0_|_12.0|64.0_|_32.0|10.0_|_2.0|19.0_|_**6.0**|25.8|
||_π_0[7]|3.5B|Yes|63.0<br>_|_11.0|**82.0**_|_24.0|**17.0**_|_**4.0**|**41.0**_|_5.0|30.9|
||**Evo-1 (Ours)**|0.77B|No|**77.0**_|_**58.0**|74.0<br>_|_**37.0**|15.0<br>_|_3.0|37.0<br>_|_1.0|**37.8**|


Table 1. **Simulation benchmark results on Meta-World, LIBERO, and RoboTwin.** We evaluate Evo-1 against representative baselines on three widely used simulation benchmarks. Params denotes model size (in billions); Robo-Pretrain shows whether the model is pretrained on robot data; **Bold** marks the best result, and underline denotes the second best. 

the pretrained backbone. As a result, the model can establish a coherent alignment between the VLM features and the action expert before full fine-tuning. 

**Stage 2: Full-scale Fine-Tuning.** Once the integration and action module are sufficiently aligned, we unfreeze the VLM backbone and perform full-scale fine-tuning across the entire architecture. This stage enables joint refinement of both the pretrained vision-language backbone and the action expert, ensuring deeper integration and better adaptation to diverse manipulation tasks. 

**Preserving Multimodal Semantics.** To further validate the benefit of our training strategy, we compare the imagetext attention maps produced by InternVL3-1B (from Evo1 after two-stage training) and Prismatic-7B VLM (used in OpenVLA). As illustrated in Figure 2, the embeddings from InternVL3-1B retain clearer structure and semantically consistent attention regions after training on robot manipulation data, whereas those from Prismatic-7B exhibit notable semantic drift and degraded alignment. This result shows that our training procedure effectively preserves the original semantic space, allowing the model to maintain strong visuallanguage understanding while adapting to downstream control tasks. 

## **4. Experiments** 

### **4.1. Simulation Experiments** 

#### **4.1.1. Meta-World Benchmark** 

**Setup.** To evaluate the manipulation capabilities of Evo1, we conduct experiments on the Meta-World bench- 

mark [34]. For our experiments, we generate 50 demonstrations per task, evaluate each task over ten trials, and report the average performance across five independent runs. Following prior work [28, 31], all tasks are divided into four difficulty levels (easy, medium, hard, and very hard). Under this standardized evaluation setup, we compare Evo1 with several representative baselines on the Meta-World benchmark (1) Diffusion Policy [9] (2) TinyVLA [31] (3) _π_ 0 [7] (4) SmolVLA [28]. All baseline performances are reported from their original papers or reproduction of other published works. 

**Results.** As shown in Table 1, Evo-1 achieves the best overall performance on the Meta-World benchmark, establishing a new state-of-the-art result among existing Vision-Language-Action models. Despite having only 0.77B parameters, Evo-1 attains an average success rate of 80.6%, significantly surpassing much larger models such as SmolVLA (2.25B, 68.2%) and _π_ 0 (3.5B, 47.9%). Moreover, Evo-1 consistently outperforms all baselines across the four difficulty levels (easy, medium, hard, and very hard), demonstrating both superior efficiency and strong capability in diverse manipulation scenarios. 

#### **4.1.2. LIBERO Benchmark** 

**Setup.** To further evaluate the manipulation capabilities of Evo-1, we conduct experiments on the LIBERO benchmark [16]. The evaluation set consists of 40 tasks, which are grouped into four categories (spatial, object, goal, and long), each targeting a distinct aspect of manipulation and reasoning capability. We evaluate each task over ten trials and report the average performance across five independent 

13401 

runs. Under this task setup, we compare Evo-1 against several representative VLA baselines. All baseline results are obtained from their original papers or official reproductions to ensure a fair and reliable comparison. 

**Results.** As illustrated in Table 1, Evo-1 attains an average success rate of 94.8%, exceeding strong baselines such as _π_ 0 (94.2%) and SmolVLA (88.8%). Across the four task categories (spatial, object, goal, long), Evo-1 maintains consistently strong results, with particularly high robustness on long tasks (92.3%), where many existing VLAs exhibit notable degradation. 

#### **4.1.3. RoboTwin Benchmark** 

**Setup.** To evaluate the ability in dual-arm manipulation, we conduct experiments on the RoboTwin Benchmark. Among them, we select four representative tasks: _Click Alarmclock_ , _Dump Bin Bigbin_ , _Place Bread Basket_ , and _Place Can Basket_ . Each task includes 50 demonstrations for training and 100 evaluation trials under two difficulty levels. Under this evaluation setup, we compare Evo-1 against several representative VLA baselines. For fairness and consistency, all baseline results are reported as provided in the official RoboTwin publication [8]. 

**Results.** As shown in Table 1, Evo-1 achieves the highest overall performance on the RoboTwin suite, attaining an average success rate of 37.8%, surpassing the previous SOTA model _π_ 0 (30.9%). Notably, Evo-1 performs exceptionally well on the _Click Alarmclock_ task, demonstrating precise bimanual coordination and effective action consistency even without large-scale pretraining. These results suggest that Evo-1, with its compact design, can still handle challenging dual-arm manipulation tasks with stable and coherent behavior. 

### **4.2. Real-World Experiments** 

**Setup.** To evaluate the model’s performance in diverse realworld scenarios, we conduct experiments using a 6-DoF xArm6 robotic arm equipped with a parallel gripper, and design four manipulation tasks involving diverse object manipulation and real-time interaction, as shown in Figure 3. 

1. **Pick and Place Can.** This task requires grasping a beverage can from varying initial positions and placing it into a white box on the table. 

2. **Pour Foam from Cup.** This task requires lifting a foamfilled cup from varying initial positions and rotating it to pour the foam into a white box. 

3. **Hand Delivery.** This task requires grasping a beverage can from varying positions and gently placing it into a human hand held at different locations. 

4. **Can Stacking.** This task requires grasping a beverage can and stacking it onto another with sufficient stability. The two cans are identical and randomly placed on the table. 


Figure 3. **Task progress of Real-World Experiments.** Step-bystep sequences for the real-world tasks. Each row shows the detailed progression of a task from start to completion. 


Figure 4. **Results of Real-World experiments.** Success rates of four real-world evaluation tasks (left four subplots) and the overall average success rate across tasks (rightmost subplot). 

For each task, we collect 100 teleoperation demonstrations to build the training dataset. Evo-1 is trained from scratch using the two-stage training process without any prior robot-data pretraining. During evaluation, each task is tested for 20 trials under varied object configurations to evaluate the stability and reliability. 

**Results.** As shown in Figure 4, Evo-1 achieves an average success rate of 78% across the four real-world tasks, substantially outperforming SmolVLA (50%) and OpenVLAOFT (55%). With only 0.77 billion parameters (roughly one-fourth the size of 3.5-billion _π_ 0 model), it still exceeds the performance of _π_ 0 (73%), highlighting its efficiency and real-world applicability. 

**Inference Efficiency Analysis.** To investigate the relationship between inference efficiency and model performance, we analyze the parameter scale, GPU memory consumption, inference frequency, and task success rate of represen- 

13402 

|**Model**|**Params(B) **|**GPU**|**Mem. (GB) Infer. **|**Freq. (Hz) **|**Success(%)**|
|---|---|---|---|---|---|
|SmolVLA [28]|0.45||2.0|12.7|50.0|
|OpenVLA [12]|7.0||15.1|7.9|55.0|
|_π_0[7]|3.5||17.9|11.5|73.0|
|Evo-1 (Ours)|0.77||2.3|16.4|78.0|


Table 2. **Inference efficiency comparison.** Comparison of model size, inference efficiency, and real-world performance on an RTX 4090d GPU. Params (B): number of parameters (in billions); GPU Mem.(GB): average memory usage during inference; Infer. Freq.(Hz): average inference frequency; Success (%): overall success rate on real-world tasks. 


Figure 5. **Disturbance settings of generalization experiments.** We evaluate model generalization under four variations: (1) unseen distractor object, (2) background color variation, (3) target position variation, and (4) target height variation. 

tative VLA models in Table 2. The comparison reveals a clear efficiency-performance relationship: large-scale models such as OpenVLA (7 B) and _π_ 0 (3.5 B) require over 15 GB of GPU memory and achieve only 7-11 Hz inference frequency, while smaller models like SmolVLA (0.45 B) have lower computational demands but limited success (50 %). Evo-1, in contrast, strikes the best balance between efficiency and performance. It maintains a low memory consumption of 2.3 GB, achieves the highest inference frequency of 16.4 Hz, and attains the top real-world success rate of 78%. 

### **4.3. Generalization Experiments** 

**Setup.** The generalization experiments are conducted using the real-world _Pick and Place Can_ task as the base scenario. In each trial, the robot is required to grasp a beverage can on the table and place it into a white box. To evaluate generalization in a systematic way, we define four types of disturbance conditions, shown in Figure 5: (i) adding an unseen distractor object, (ii) changing the background color, (iii) shifting the target position, and (iv) varying the target height. All of these changes are beyond the training distribution. We conducted 20 trials for each disturbance condition to ensure the statistical reliability of the evaluation. **Results.** As shown in Table 3, Evo-1 consistently outperforms SmolVLA across all disturbance settings. It achieves 95% in the base case and remains robust under unseen distractors (80%) and background shifts (75%), surpassing SmolVLA (65%, 60%). For position variations, Evo1 maintains high score (95%, 85%, 80%) under increasing displacement, while SmolVLA degrades notably. Likewise, 

|**Condition**|**SmolVLA**|**Ours**|
|---|---|---|
|**Base**|75%|**95%**|
|**Unseen distractor object**<br>Add unseen bottle|65%|**80%**|
|**Background color variation**|||
|Addyellow tablecloth|60%|**75%**|
|**Target position variation**|||
|10 mm backward|75%|**95%**|
|20 mm backward|60%|**85%**|
|30 mm backward|60%|**80%**|
|**Target height variation**|||
|10 mm higher|75%|**100%**|
|20 mm higher|65%|**90%**|
|30 mm higher|60%|**70%**|


Table 3. **Success rates for generalization experiments.** Comparison of success rates between SmolVLA and Ours under different disturbance conditions in real-world task generalization experiments. 

under height variations, Evo-1 retains strong performance (100%, 90%, 70%), showing superior generalization. 

### **4.4. Ablation Study** 

#### **4.4.1. Integration Module Analysis** 

We conduct experiments to investigate how different integration strategies between the Vision-Language model (VLM) and the action expert affect overall performance. As illustrated in Figure 6, we evaluate four representative designs (Module A-D), each offering a unique approach to fusing visual, linguistic, and state information for action generation. 

**Module A: Mid-Layer Cross-Attention.** This design extracts the fused multimodal feature _zt_ from the 14<sup>th</sup> VLM layer, concatenates it with the robot state _st_ , and uses them as key-value inputs for all DiT layers, where the noiseinjected action _A_<sup>_τ_</sup> _t_<sup>serves as the query in cross-attention.</sup> **Module B: Mid-Layer Interleaved Cross-Self Attention.** This design interleaves cross-attention and self-attention layers within the DiT. Each cross-attention block attends to the concatenated VLM feature and state _st_ , followed by a self-attention block that refines internal interactions. 

**Module C: Layer-wise Cross-Attention.** This design injects features from selected mid-to-deep VLM layers into the DiT, where each corresponding layer uses its paired VLM feature and state _st_ as key-value inputs, and _A_<sup>_τ_</sup> _t_<sup>as the</sup> query to enable hierarchical perception-action alignment. **Module D: Joint Key-Value Cross-Attention.** This design concatenates the VLM feature, robot state, and noiseinjected action to form joint key-value inputs for each DiT layer, while _A_<sup>_τ_</sup> _t_<sup>alsoservesasthequerytoachieveunified</sup> multimodal conditioning. 

13403 


Figure 6. **Integration Module Designs.** Architectures of four different modules (A-D) for connecting the VLM and the action expert. 

**Results.** As shown in Figure 8 (a), Module A outperforms other variants by maintaining a consistent propagation of multimodal information, resulting in more coherent multimodal conditioning. In comparison, Modules B-D introduce interruptions in this interaction process, either by inserting self-attention blocks between cross-attention layers or by using different conditioning features across layers, which breaks the continuity and consistency of information propagation. This comparison highlights the effectiveness of Module A’s integration design, which is accordingly adopted in the final Evo-1 architecture. 

#### **4.4.2. Training Paradigm Comparison** 

We compare our proposed two-stage training paradigm with a single-stage baseline that jointly trains all modules from scratch. In the two-stage setup, we first freeze the VLM and train only the integration module and action expert. Once aligned, we unfreeze the VLM and perform full finetuning. In contrast, the single-stage baseline directly trains the VLM, integration module, and action expert together without any freezing schedule. 

**Attention Visualization.** To analyze their difference, we visualize the attention maps of both models. As shown in Figure 7, the two-stage paradigm preserves the semantic attention patterns of VLM, maintaining clear focus on object regions and task-relevant entities. In comparison, the single-stage training disrupts these patterns, causing the model to lose clear semantic focus and attend to irrelevant areas. 

**Results.** As shown in Figure 8 (b), the two-stage training paradigm consistently outperforms the single-stage baseline across all difficulty levels by better preserving the per- 


(b) Attention maps using two-stage training paradigm (ours) 

Figure 7. **Comparison of vision-language attention maps after training.** (a) The single-stage paradigm shows disrupted attention with reduced semantic coherence. (b) Our two-stage paradigm preserves clear and semantically consistent focus regions. 


Figure 8. **Comparison results of integration modules and training paradigms.** (a) Success rates of four integration modules on the LIBERO-Long benchmark. (b) Performance comparison on Meta-World between a single-stage and our two-stage training paradigm. 

ceptual representations of the vision-language backbone, thereby enhancing generalization and reducing overfitting to downstream tasks. 

## **5. Conclusion** 

In this work, we introduce Evo-1, a lightweight and efficient Vision-Language-Action (VLA) model that enables lowcost training and high-efficiency inference on consumergrade GPUs, while achieving state-of-the-art performance without any robot data pretraining. This achievement is attributed to our efficient architectural design and the proposed two-stage training strategy, which together ensure stable perception-action alignment while preserving the semantic understanding of vision-language backbone. To advance future research, we release the code, data, and model weights to encourage further research and practical development of lightweight and high performance VLA models. 

13404 

## **Acknowledgement** 

This work is funded by NSFC-62306046. 

## **References** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 1 

- [2] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katherine Millican, Malcolm Reynolds, et al. Flamingo: a visual language model for few-shot learning. _Advances in neural information processing systems_ , 35:23716–23736, 2022. 1, 2 

- [3] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, et al. Qwen2. 5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 3 

- [4] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 2 

- [5] Stella Biderman, Hailey Schoelkopf, Quentin Gregory Anthony, Herbie Bradley, Kyle O’Brien, Eric Hallahan, Mohammad Aflah Khan, Shivanshu Purohit, USVSN Sai Prashanth, Edward Raff, et al. Pythia: A suite for analyzing large language models across training and scaling. In _International Conference on Machine Learning_ , pages 2397– 2430. PMLR, 2023. 2 

- [6] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 1, 2, 5 

- [7] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. corr, abs/2410.24164, 2024. doi: 10.48550. _arXiv preprint ARXIV.2410.24164_ . 1, 2, 4, 5, 7 

- [8] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 6 

- [9] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , page 02783649241273668, 2023. 5 

- [10] Zhangwei Gao, Zhe Chen, Erfei Cui, Yiming Ren, Weiyun Wang, Jinguo Zhu, Hao Tian, Shenglong Ye, Junjun He, Xizhou Zhu, et al. Mini-internvl: a flexible-transfer pocket 

multi-modal model with 5% parameters and 90% performance. _Visual Intelligence_ , 2(1):32, 2024. 3 

- [11] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 1 

- [12] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 2, 5, 7 

- [13] Gen Li, Nikolaos Tsagkas, Jifei Song, Ruaridh MonWilliams, Sethu Vijayakumar, Kun Shao, and Laura SevillaLara. Learning precise affordances from egocentric videos for robotic manipulation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 10581– 10591, 2025. 2 

- [14] Tao Lin, Gen Li, Yilei Zhong, Yanwen Zou, Yuxin Du, Jiting Liu, Encheng Gu, and Bo Zhao. Evo-0: Vision-languageaction model with implicit spatial understanding. _arXiv preprint arXiv:2507.00416_ , 2025. 2 

- [15] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 4 

- [16] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 5 

- [17] Jiaming Liu, Hao Chen, Pengju An, Zhuoyang Liu, Renrui Zhang, Chenyang Gu, Xiaoqi Li, Ziyu Guo, Sixiang Chen, Mengzhen Liu, et al. Hybridvla: Collaborative diffusion and autoregression in a unified vision-language-action model. _arXiv preprint arXiv:2503.10631_ , 2025. 2 

- [18] Qiang Liu. Rectified flow: A marginal preserving approach to optimal transport. _arXiv preprint arXiv:2209.14577_ , 2022. 4 

- [19] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 5 

- [20] Yuanzhe Liu, Jingyuan Zhu, Yuchen Mo, Gen Li, Xu Cao, Jin Jin, Yifan Shen, Zhengyuan Li, Tianjiao Yu, Wenzhen Yuan, et al. Palm: Progress-aware policy learning via affordance reasoning for long-horizon robotic manipulation. _arXiv preprint arXiv:2601.07060_ , 2026. 2 

- [21] Ziyan Liu, Yeqiu Chen, Hongyi Cai, Tao Lin, Shuo Yang, Zheng Liu, and Bo Zhao. Vla-pruner: Temporal-aware dual-level visual token pruning for efficient vision-languageaction inference. _arXiv preprint arXiv:2511.16449_ , 2025. 2 

- [22] Andr´es Marafioti, Orr Zohar, Miquel Farr´e, Merve Noyan, Elie Bakouch, Pedro Cuenca, Cyril Zakka, Loubna Ben Allal, Anton Lozhkov, Nouamane Tazi, et al. Smolvlm: Redefining small and efficient multimodal models. _arXiv preprint arXiv:2504.05299_ , 2025. 2 

13405 

- [23] Ruaridh Mon-Williams, Gen Li, Ran Long, Wenqian Du, and Christopher G Lucas. Embodied large language models enable robots to complete complex tasks in unpredictable environments. _Nature Machine Intelligence_ , pages 1–10, 2025. 2 

- [24] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903. IEEE, 2024. 1, 2 

- [25] William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 4195–4205, 2023. 4 

- [26] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 5 

- [27] Lucy Xiaoyang Shi, Brian Ichter, Michael Equi, Liyiming Ke, Karl Pertsch, Quan Vuong, James Tanner, Anna Walling, Haohuan Wang, Niccolo Fusai, et al. Hi robot: Open-ended instruction following with hierarchical visionlanguage-action models. _arXiv preprint arXiv:2502.19417_ , 2025. 2 

   - [34] Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Karol Hausman, Chelsea Finn, and Sergey Levine. Metaworld: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on robot learning_ , pages 1094–1100. PMLR, 2020. 5 

   - [35] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1702–1713, 2025. 5 

   - [36] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 5 

   - [37] Jinguo Zhu, Weiyun Wang, Zhe Chen, Zhaoyang Liu, Shenglong Ye, Lixin Gu, Hao Tian, Yuchen Duan, Weijie Su, Jie Shao, et al. Internvl3: Exploring advanced training and test-time recipes for open-source multimodal models. _arXiv preprint arXiv:2504.10479_ , 2025. 1, 2, 3 

   - [38] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 1 

- [28] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, et al. Smolvla: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 2, 4, 5, 7 

- [29] Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, et al. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. _arXiv preprint arXiv:2409.12191_ , 2024. 1 

- [30] Yihao Wang, Pengxiang Ding, Lingxiao Li, Can Cui, Zirui Ge, Xinyang Tong, Wenxuan Song, Han Zhao, Wei Zhao, Pengxu Hou, et al. Vla-adapter: An effective paradigm for tiny-scale vision-language-action model. _arXiv preprint arXiv:2509.09372_ , 2025. 2 

- [31] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Zhibin Tang, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, et al. Tinyvla: Towards fast, data-efficient visionlanguage-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 2, 5 

- [32] Feng Xu, Guangyao Zhai, Xin Kong, Tingzhong Fu, Daniel FN Gordon, Xueli An, and Benjamin Busam. Stare-vla: Progressive stage-aware reinforcement for finetuning vision-language-action models. _arXiv preprint arXiv:2512.05107_ , 2025. 

- [33] Kai Ye, Yuhang Wu, Shuyuan Hu, Junliang Li, Meng Liu, Yongquan Chen, and Rui Huang. _\_ textsc _{_ Gen2Real _}_ : Towards demo-free dexterous manipulation by harnessing generated video. _arXiv preprint arXiv:2509.14178_ , 2025. 2 

13406 

