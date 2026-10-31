---
title: "ST-$π$: Structured SpatioTemporal VLA for Robotic Manipulation"
date: "2026-04-20"
authors: "Chuanhao Ma; Hanyu Zhou; Shihan Peng; Yan Li; Tao Gu; Luxin Yan"
url: https://arxiv.org/abs/2604.17880
pdf: https://arxiv.org/pdf/2604.17880
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.17880)** / [論文ページ](https://arxiv.org/abs/2604.17880)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **ST-** _𝜋_ **: Structured SpatioTemporal VLA for Robotic Manipulation** 

Chuanhao Ma<sup>1</sup> , Hanyu Zhou<sup>2∗</sup> , Shihan Peng<sup>1</sup> , Yan Li<sup>2</sup> , Tao Gu<sup>3</sup> , Luxin Yan<sup>1</sup> 

1 School of Artificial Intelligence and Automation, Huazhong University of Science and Technology 

- 2 School of Computing, National University of Singapore 

   - 3 School of Computing, Macquarie University 

{machuanhao, yanluxin}@hust.edu.cn, hy.zhou@nus.edu.sg 


**Figure 1: Illustration of typical VLA paradigms for spatiotemporal robotic manipulation. (a) OpenVLA operates on single-frame observations, leading to spatiotemporal chaos in long-horizon trajectories. (b) VLA-4D incorporates temporal information into visual and action representations, achieving consistent trajectories over short horizons but exhibiting instability in later stages. (c) Our ST-** _𝜋_ **explicitly models structured task decomposition and employs a spatiotemporal action expert, enabling coherent and stable trajectories for long-horizon manipulation.** 

## **Abstract** 

Vision-language-action (VLA) models have achieved great success on general robotic tasks, but still face challenges in fine-grained spatiotemporal manipulation. Typically, existing methods mainly embed spatiotemporal knowledge into visual and action representations, and directly perform a cross-modal mapping for step-level action prediction. However, such spatiotemporal reasoning remains largely implicit, making it difficult to handle multiple sequential behaviors with explicit spatiotemporal boundaries. In this work, we propose **ST-** _𝜋_ , a structured spatiotemporal VLA model for robotic manipulation. Our model is guided by two key designs: **1) Spatiotemporal VLM.** We encode 4D observations and task instructions into latent spaces, and feed them into the LLM to generate a sequence of causally ordered chunk-level action prompts consisting of sub-tasks, spatial grounding and temporal grounding. **2) Spatiotemporal action expert.** Conditioned on chunk-level action prompts, we design a structured dual-generator guidance to jointly model spatial dependencies and temporal causality, thus predicting step-level action parameters. Within this structured framework, the VLM explicitly plans global spatiotemporal behavior, and the action expert further refines local spatiotemporal control. In addition, we propose a real-world robotic dataset with structured spatiotemporal annotations for fine-tuning. Extensive experiments have been conducted to demonstrate the effectiveness of our model. Our code link: https://github.com/chuanhaoma/ST-pi. 

## **1 Introduction** 

Vision-language-action (VLA) models [4, 15, 17, 18, 30] have emerged as a promising paradigm for robotic manipulation that integrates perception, language reasoning, and action generation in a unified framework. Despite their strong performance on a wide range of robotic tasks, they still face significant challenges in fine-grained spatiotemporal manipulation tasks. Such tasks are typically longhorizon and composed of multiple sub-tasks with explicit spatial and temporal boundaries, such as complex assembly and household activities. Conventional VLA models [28, 39] embed geometric information but lack explicit spatiotemporal representations, making it difficult to capture and reason about the structured boundaries in complex tasks. Therefore, our goal is to develop spatiotemporal models for fine-grained manipulation. 

Existing 4D VLA approaches enhance spatiotemporal reasoning by extending spatial representations with temporal dimensions in both visual inputs and action representations. For instance, Zhang _et al._ [37] introduce a memory-bank-based historical framesampling strategy to construct 4D observation inputs; Zhou _et al._ [42] further extend action representations with temporal control to promote coherent action execution. However, since the spatiotemporal reasoning remains largely implicit, these methods are primarily limited to short-horizon behavior planning. While implicit representations are sufficient for short-horizon coherence, they fail to properly model the causal dependencies and transitions between 

> ∗Corresponding author. 

1 


**Figure 2: Overview of ST-** _𝜋_ **. Our model consists of two key components: (1) ST-VLM, which constructs 4D observation representations and performs structured task decomposition; and (2) ST-AE, which generates executable action chunks conditioned on chunk-level action prompts for each sub-task, ensuring stable and coherent trajectories.** 

sub-tasks in long-horizon scenarios. Therefore, it is essential to explicitly model spatiotemporal structure, enabling the representation of sub-task boundaries and reasoning about causal dependencies across long-horizon manipulation. 

To address these issues, we argue that fine-grained manipulation requires explicit and structured spatiotemporal modeling at both chunk-level planning and step-level execution. For chunklevel planning, we suggest that complex tasks are composed of a sequence of sub-tasks with distinct spatial and temporal boundaries, where temporal causal dependencies exist across sub-tasks. This motivates us to explicitly model such dependencies and capture spatiotemporal boundaries for structured task decomposition. For step-level execution, we observe that action steps within the same sub-task exhibit inherent spatial coherence and temporal causality. This indicates the need to explicitly guide action generation along both spatial and temporal dimensions, ensuring spatial coherence and temporal stability. Consequently, a unified framework that explicitly models both chunk-level planning and step-level execution is essential for fine-grained spatiotemporal manipulation. 

In this work, we propose **ST-** _𝜋_ , a structured spatiotemporal VLA framework for fine-grained robotic manipulation. As illustrated in Fig. 2, our ST- _𝜋_ consists of a spatiotemporal vision-language model and a spatiotemporal action expert. For the spatiotemporal vision-language model, we construct 4D observations from image sequences and predict chunk-level action prompts containing semantic intent with spatial and temporal attributes. For the spatiotemporal action expert, we construct spatial and temporal motion generators to refine the actions and enforce spatiotemporal coherence and causality. In addition, we construct a real-world dataset, 

termed STAR, to support training, where manipulation trajectories are segmented into sub-tasks with semantic, spatial, and temporal annotations. The contributions of this work are as follows: 

- We propose **ST-** _𝜋_ , a unified framework that explicitly structures both chunk-level task decomposition and step-level action generation, enabling fine-grained manipulation. 

- We design ST-VLM, a spatiotemporal VLM for behavior planning. The ST-VLM predicts causally ordered sub-tasks as chunk-level action prompts with semantic, spatial, and temporal attributes. 

- We introduce ST-AE, a structured action expert with complementary spatial and temporal generators, enabling spatially coherent and temporally consistent action generation. 

- We construct STAR, a real-world long-horizon robotic manipulation dataset with structured sub-task annotations. Extensive experiments demonstrate consistent improvements. 

## **2 Related Works** 

**Vision-Language-Action Models.** The success of vision-language models (VLM) [2, 3, 23] in scene reasoning promotes the adoption in robotics, giving rise to vision-language-action (VLA) models. Early VLA models [8, 15, 30, 43] adopt end-to-end architectures that encode images, texts, and actions into a shared representation, directly mapping multimodal inputs to control parameters via cross-modal attention. These approaches benefit from large-scale multimodal pretraining [5, 11, 23, 44] and demonstrate strong generalization across diverse tasks. More recently, hierarchical VLA 

2 


**Figure 3: Architecture of ST-VLM. The ST-VLM takes 4D representations, language instructions, and query tokens as inputs to construct unified spatiotemporal representations. It performs structured task decomposition to generate chunk-level action prompts, including semantic intent and spatiotemporal information of sub-tasks.** 

models [1, 4, 13, 18, 35] have been introduced, combining highlevel reasoning with low-level control. However, most VLA frameworks [16, 28, 38, 39] primarily encode geometric cues while underutilizing temporal information. This motivates the exploration of 4D VLA frameworks integrating geometric knowledge with temporal information for stable and precise manipulation. 

**4D Vision-Language-Action Models.** Recent works [11, 26, 37, 42] have explored 4D VLA models to integrate temporal information with perception and control modeling. For example, Zhang _et al._ [37] augment visual inputs by performing geometric alignment and historical frame sampling to construct 4D observations, enhancing spatiotemporal perception from image sequences. However, temporal modeling is primarily applied at the perception level, while action dynamics remain implicitly modeled. Zhou _et al._ [42] further extend temporal modeling to the action space by embedding temporal information into both visual and action representations. Despite these advances, their spatiotemporal reasoning remains largely implicit. While effective for single-stage manipulation, the implicit formulation limits fine-grained spatiotemporal execution in multi-stage tasks. This inspires us to develop the spatiotemporal VLA model with explicit structured reasoning. 

**4D Reasoning Models.** Recent advances in large multimodal models (LMMs) [2, 23, 32, 34, 40, 41] significantly enhance the capability of spatiotemporal reasoning over dynamic scenes. These 4D LMMs extend visual-language modeling beyond static images with geometry cues and temporal dynamics, enabling temporally consistent grounding, cross-frame reasoning, and query-based understanding. For example, Yang _et al._ [34] extend language models with temporally aligned region-level visual representations, enabling crossframe grounding over dynamic scenes. Similarly, Zhou _et al._ [40] embed dynamic-aware 4D coordinate prompts into disentangled 

spatial and temporal visual features, aligning spatiotemporal embeddings with language representations to enhance 4D scene understanding. While these methods demonstrate strong capability, their spatiotemporal reasoning remains primarily perception-oriented rather than structured for embodied manipulation. This highlights the need for a structured spatiotemporal VLA framework explicitly decomposing high-level instructions into executable sub-tasks with spatiotemporally coherent actions. 

## **3 Our ST-** _𝜋_ 

**Overview.** As illustrated in Fig. 2, our ST- _𝜋_ consists of two key components: **1) SpatioTemporal Vision-Language Model** (STVLM) for chunk-level task decomposition, and **2) SpatioTemporal Action Expert** (ST-AE) for step-level action generation. 

**Our Framework.** Given a sequence of multi-view observations I _𝑡_ = { _𝐼𝑡_ − _𝑊_ +1 _, . . . , 𝐼𝑡_ } with _𝑊_ frames, and the high-level language instruction _𝐿_ , we employ ST-VLM to decompose the task into a sequence of chunk-level action prompts, and then use ST-AE to generate executable action parameters conditioned on these prompts. **1) SpatioTemporal Vision-Language Model (** **_cf. Sec. 3.1_ ).** The ST-VLM constructs the 4D observation and decomposes high-level instructions. We first extract visual features _𝑓𝑣_ and geometric features _𝑓𝑔_ using a vision encoder and a geometry encoder, respectively. These features, together with timestamps t, are then fused into unified 4D representations _𝑓_ 4 _𝐷_ via a spatiotemporal fusion module: 


where STE(·) denotes the spatiotemporal fusion module. Conditioned on the 4D representations and the language instruction, the ST-VLM autoregressively predicts a sequence of chunk-level action prompts { _𝑝𝑘_ } _𝑘_<sup>_𝐾_</sup> =1<sup>to represent sub-tasks, where</sup><sup>_𝐾_denotes the</sup> maximum number of sub-tasks for task decomposition. 

3 


**Figure 4: Overview of structured task decomposition with chunk-level action prompt. A long-horizon task (a) is decomposed into a sequence of sub-tasks (b). Each sub-task is represented as a chunk-level action prompt (c) with semantic, spatial, and temporal components, capturing what to do, where to act, and how to execute.** 

**2) SpatioTemporal Action Expert (** **_cf. Sec. 3.2_ ).** The ST-AE generates action parameters conditioned on the current sub-task _𝑝𝑘_ via a flow-matching [21] process. We construct two complementary motion generators: a spatial generator and a temporal generator. Conditioned on the action prompt _𝑝𝑘_ and 4D representations, the two motion generators separately produce update flows _𝑣𝑠_ and _𝑣𝑡_ , which are then fused via a flow fusion mechanism: 


where _𝑣_ denotes the fused flow; SG(·) and TG(·) denote the spatial and the temporal generators; FF(·) denotes the flow fusion module. Then the fused flow guides the generation of action chunk _𝐴𝑘_ . 

## **3.1 SpatioTemporal Vision-Language Model** 

As illustrated in Fig. 3, the ST-VLM performs structured chunklevel task decomposition conditioned on 4D representations and language instructions. Instead of implicitly encoding sub-tasks into latent features, ST-VLM represents them as chunk-level action prompts with semantic intent and spatiotemporal information, and explicitly models inter-chunk dependencies. In this section, we describe how ST-VLM constructs structured 4D representations and performs causal task decomposition. 

**Structured 4D Representation Construction.** In robotic manipulation, conventional approaches typically rely on static 2D observations to predict action parameters in 3D space, leading to an inherent mismatch between perception and action. Extending observations to 4D representations improves the understanding of dynamic scenes. Therefore, we construct 4D representations by integrating visual features, geometric cues, and temporal contexts. We extract visual features using a SigLIP-based vision encoder [36] and geometric features using a geometry encoder adapted from VGGT [32]. While visual features capture appearance semantics, geometric features encode spatial structure in latent space. To incorporate temporal contexts, we encode the timestamps t into temporal 

embeddings using Fourier positional encoding [20] _𝜙_ (·). The temporal embedding _𝜙_ (t) is fused with visual and geometric features as structured spatiotemporal embeddings via a linear layer: 


where VE(·) and GE(·) denote the vision and geometry encoders. This structured 4D representation provides explicit spatiotemporal grounding for the causal task decomposition in ST-VLM. 

**Structured Planning with Action Prompts.** As illustrated in Fig. 4, complex robotic manipulation tasks are typically composed of multiple sub-tasks, each with its own execution objective, operational region, and expected duration, while causal dependencies exist across sub-tasks. Our ST-VLM explicitly models such sub-task structures using chunk-level action prompts to capture the spatiotemporal information, and further enforces explicit constraints on the causal dependencies. Given the 4D representation _𝑓_ 4 _𝐷_ and the high-level instruction _𝐿_ , the ST-VLM autoregressively predicts a sequence of action prompts within a short planning horizon _𝐾_ . Each prompt _𝑝𝑘_ is composed of semantic tokens _𝑠𝑘_ , spatial tokens x _𝑘_ , and temporal tokens _𝜏𝑘_ : 


where _𝑝<𝑘_ denotes the preceding action prompts before step _𝑘_ . The ST-VLM follows a rolling-horizon scheme: ST-VLM predicts the next _𝐾_ sub-tasks and re-plans after each sub-task is completed. 

In each chunk-level action prompt, semantic tokens consist of _𝑀_ learnable query tokens that capture the semantic intent and are supervised by the textual description of each sub-task, while the spatial and temporal tokens respectively encode the target execution region and the expected duration. Separate train-only regression heads are attached to tokens for supervision. During modeling, all tokens attend to the 4D representations to extract spatiotemporal context, while the spatial and temporal tokens further attend to the semantic tokens to explicitly model execution constraints. Across action prompts, we model causal dependencies using a block-wise 

4 


**Figure 5: Architecture of ST-AE. The ST-AE takes chunk-level action prompts to generate actions through a dual-generator mechanism. A shared backbone with different attention constraints is applied to produce spatial and temporal flows, which are fused to guide action generation.** 

causal attention structure [13, 31]. The semantic tokens of prompt _𝑝𝑘_ attend to all preceding prompts _𝑝<𝑘_ , while future prompts _𝑝>𝑘_ are masked, enforcing causally ordered task decomposition. 

biases, enabling the model to jointly capture spatial coordination and temporal causality for coherent action generation. 

**Dual-Generator Action Generation.** In the early phase of action generation, spatial shaping plays a dominant role, establishing the coarse trajectory structure. In the later phase, temporal refinement becomes dominant, capturing causal dependencies and fine-tuning individual action steps. We adopt a time-dependent fusion strategy to gradually shift the guidance from spatial shaping to temporal refinement over the generation process: 


where _𝜏_ denotes the current step; _𝑇_ denotes the total number of denoising steps; _𝛼_<sup>_𝜏_</sup> denotes the time-dependent fusion weight. Following the flow-matching formulation, the action chunk _𝐴𝑘_ is refined by integrating the fused update flow: 


where Δ _𝜏_ denotes the denoising step size. Starting from an initial Gaussian noise sample, the action chunk is iteratively refined, resulting in spatially coherent and temporally consistent trajectories. 

## **3.3 Optimization** 

## **3.2 SpatioTemporal Action Expert** 

Conditioned on chunk-level action prompts, the ST-AE generates action chunks for each sub-task via a flow-matching process, illustrated in Fig. 5. Each action chunk _𝐴𝑘_ consists of _𝐻_ action steps: 


where Δx and Δ _𝜃_ denote translational and rotational motions of the robot; _𝑔_ denotes the gripper motion; Δ _𝑡_ denotes the step duration. **Dual-Generator Spatiotemporal Guidance.** Action generation involves two complementary stages: spatial shaping and temporal refinement. Spatial shaping transforms the initial noise into trajectory structures, while temporal refinement further adjusts the trajectory by enforcing causal dependencies across actions. We introduce a spatiotemporal dual-generator guidance: a spatial motion generator and a temporal motion generator, producing spatial update flows _𝑣𝑠_ and temporal update flows _𝑣𝑡_ , respectively: 


where Φ _𝑠_ (·) and Φ _𝑡_ (·) denote the spatial and temporal generators, and _𝜃_ denotes their shared parameters. 

The two generators differ in architectural constraints and conditioning features. The spatial motion generator conditions on the semantic and spatial tokens with a bidirectional attention constraint to action tokens. With all action steps in the chunk attending to each other, the spatial generator captures global spatial structures and encourages coordinated updates across steps to generate smooth trajectories. In contrast, the temporal motion generator conditions on the semantic and temporal tokens with a causal attention constraint to capture step-wise temporal dependencies and enforce sequential consistency. Each step is generated conditioned only on its preceding steps, ensuring temporally consistent action generation within the action chunk. Both motion generators are implemented using a shared backbone network to learn a unified action representation. This complementary design introduces distinct inductive 

Our ST- _𝜋_ involves two learning objectives: structured task planning for ST-VLM and dual-generator action generation for ST-AE. 

**Structured Task Planning.** Given the 4D observation representation _𝑓_ 4 _𝐷_ and the high-level instruction _𝐿_ , we optimize the ST-VLM to predict a sequence of structured action prompts { _𝑝𝑘_ } _𝑘_<sup>_𝐾_</sup> =1<sup>. The train-</sup> ing objective consists of three components: 1) Language modeling loss, which supervises the semantic tokens to predict the sub-task textual description. 2) Spatial regression loss, which supervises the spatial token to localize the target region. 3) Temporal regression loss, which supervises the temporal token to estimate the execution duration. The overall objective is formulated as: 

LVLM = − _𝜆𝐿_ E[log _𝑃_ ( _𝐿𝑘_ | _𝑓_ 4 _𝐷, 𝐿,𝑠𝑘_ )]+ _𝜆𝑠_ |x _𝑘_ −x _𝑘_<sup>∗|1+</sup><sup>_𝜆𝜏_|</sup><sup>_𝜏𝑘_−</sup><sup>_𝜏_</sup> _𝑘_<sup>∗|1</sup><sup>_,_(9)</sup> where _𝐿𝑘_ , x _𝑘_<sup>∗and</sup><sup>_𝜏_</sup> _𝑘_<sup>∗denote the ground-truth description, spatial</sup> target, and duration of sub-task; _𝜆𝐿_ , _𝜆𝑠_ and _𝜆𝜏_ denote loss weights. **Dual-generator Action Generation.** To train the ST-AE, we adopt a flow-matching objective for action generation. Given a ground-truth action chunk _𝐴𝑘_<sup>∗, the ST-AE learns to transport the</sup> noisy action toward the target trajectory. Following the flow-matching formulation [10, 21, 24], we construct the noisy action by interpolating between the ground-truth action and Gaussian noise. For denoising timestep _𝜏_ ∈[0 _,_ 1] and noise _𝜔_ ∼N (0 _, 𝐼_ ), we construct the noisy action chunk _𝐴_<sup>_𝜏,𝜔_</sup> _𝑘_ and the target update flow _𝑢𝑘_<sup>_𝜔_:</sup> 


The fused flow _𝑣_ in the ST-AE is trained to match the target update flow with the following objective: 


**Total Loss.** The entire framework is optimized end-to-end with a weighted sum of two objectives, which is formulated as: 


5 


**Figure 6: Illustration of our real-world robotic platform and STAR dataset. Each task in the STAR dataset is segmented into multiple sub-tasks, with annotations including language instructions, target locations, and execution durations. The dataset includes three suites: Object Recognition, Sequential Goal, and Long-Horizon.** 

## **4 Training Datasets and Pipeline** 

## **4.1 Dataset** 

To train and evaluate our ST- _𝜋_ , we leverage three complementary datasets to provide supervision at different levels. 

**ScanNet series.** We utilize the ScanNet [9], ScanRefer [6], and Scan2Cap [7], which provide richly annotated 3D reconstructions of indoor scenes. We extract RGB observations, descriptions, and corresponding 3D bounding boxes to provide spatial grounding supervision. These datasets are primarily used to train spatial representations and align geometric features with visual representations. 

**DROID-ST.** We construct DROID-ST, a structured task decomposition dataset derived from DROID [14] demonstrations. Each trajectory is decomposed into a variable-length sequence of subtasks, annotated with sub-task descriptions, target object bounding boxes, durations, and corresponding action segments. 

**STAR.** As shown in Fig. 6, we construct **STAR** (Spatiotemporal Task Annotation for Robotics), a real-world dataset including 30 manipulation tasks on the Franka Research 3 platform. The dataset is collected via a Gello [33] teleoperation system with multi-view observations, where each task contains 50 demonstrations, resulting in around 300k interaction steps in total. The dataset consists of three suites: _Object Recognition_ , _Sequential Goal_ , and _Long-Horizon_ , covering a diverse set of tasks with increasing complexity. Each subtask is annotated with descriptions, target locations, and execution durations. In terms of modalities, the inputs include multi-view images with depth observations, language instructions, and robot proprioceptive states. The outputs include end-effector motions and joint angles. To enhance temporal generalization, we collect demonstrations with varying speeds and encode the speed into the instruction using descriptors _fast_ , _medium_ , and _slow_ . 

## **4.2 Training Recipe** 

Our ST- _𝜋_ is trained through a three-stage training procedure that progressively enhances the capability of spatiotemporal perception, structured task planning, and robotic manipulation policy. **Stage 1: Representation Alignment.** We first align geometric features with visual representations using ScanNet datasets. To 

preserve the pretrained knowledge of large backbones, we freeze the VLM backbone, the vision encoder and the geometry encoder, and train the geometry-aware adapters, the 4D fusion module and the spatial token with 3D bounding box supervision. In this stage, we only apply the spatial regression loss. 

**Stage 2: Behavior Planning Learning.** In the second stage, we train the model to perform structured task decomposition using the DROID-ST dataset. First, we freeze the time encoder and temporal token, and train the ST-VLM along with semantic tokens. Conditioned on the 4D representation and the language instruction, the model is supervised to predict the textual description of each sub-task, with the language modeling loss and LoRA [12] applied for efficient adaptation. Next, we unfreeze and train the temporal components. The temporal token is supervised to predict the duration of each sub-task with the temporal regression loss, enabling the ST-VLM to capture temporal dynamics in task decomposition. 

**Stage 3: Robotic Task Fine-tuning.** In the third stage, we perform end-to-end fine-tuning using the DROID-ST dataset to learn a unified manipulation policy. We freeze the vision encoder, the geometry encoder, the 4D fusion module and the action prompt tokens to preserve the decomposition capability learned previously. The model is then fine-tuned to generate executable action chunks conditioned on the 4D representation and the chunk-level action prompt, supervised by the flow-matching loss in Sec. 3.3. 

## **5 Experiments** 

## **5.1 Experiment Setup** 

**Implementation Details.** Our model adopts the pretrained weights of PaliGemma [3] from _𝜋_ 0 _._ 5 [13] as the VLM backbone, DINOv2 [27] from VGGT [32] as the geometry encoder, and Gemma-300M [29] equipped with a structured spatiotemporal attention mechanism as the action expert. The model is trained on 8 NVIDIA RTX PRO 6000 GPUs, using the AdamW [25] optimizer. In training stage 1, we set _𝜆𝑠_ = 1, _𝜆𝐿_ = _𝜆𝜏_ = 0, and the learning rate to 2 _𝑒_ − 5 with a batch size of 64. In stage 2 and stage 3, we set _𝜆𝐿_ = _𝜆_ 1 = 1, _𝜆𝑠_ = _𝜆𝜏_ = 5, _𝜆_ 2 = 10, and the learning rate to 1 _𝑒_ − 5 with a batch size of 32. 

6 

**Table 1: Evaluation on the LIBERO benchmark.** 

|Model|Sp|atial|Ob|ject|G|oal|Lo|ng|Av|erage|
|---|---|---|---|---|---|---|---|---|---|---|
||SR ↑|CT(s) ↓|SR ↑|CT(s) ↓|SR ↑|CT(s) ↓|SR ↑|CT(s) ↓|SR ↑|CT(s) ↓|
|OpenVLA [15]|84.7%|5.5|88.4%|7.5|79.2%|6.1|53.7%|13.1|76.5%|8.0|
|Octo [30]|78.9%|5.7|85.7%|6.9|84.6%|6.3|51.1%|9.3|75.1%|7.0|
|SpatialVLA [28]|88.2%|5.3|89.9%|7.4|79.0%|6.0|55.5%|8.9|78.1%|6.6|
|TraceVLA [39]|84.6%|-|85.2%|-|76.3%|-|54.1%|-|74.8%|-|
|4D-VLA [37]|88.9%|-|95.2%|-|90.9%|-|79.1%|-|88.6%|-|
|CogACT [18]|87.5%|5.4|90.2%|7.1|80.2%|6.0|53.2%|10.7|77.8%|7.2|
|_𝜋_0_._5 [13]|**98.8%**|**5.2**|98.2%|6.3|96.8%|5.8|92.4%|7.8|96.9%|6.3|
|ST-_𝜋_(Ours)|98.4%|5.4|**98.3%**|**6.0**|**96.9%**|**5.3**|**94.3%**|**6.9**|**97.3%**|**5.9**|


**Table 2: Evaluation on the SIMPLER benchmark.** 

|Protocol|Model|#Pick C<br>|oke Can<br>|#Mov<br>|e Near<br>|#Open/C<br>|lose Drawer<br>|Ave<br>|rage<br>|
|---|---|---|---|---|---|---|---|---|---|
|||SR ↑|CT(s) ↓|SR ↑|CT(s) ↓|SR ↑|CT(s) ↓|SR ↑|CT(s) ↓|
||OpenVLA [15]|14.7%|15.2|49.2%|11.8|39.8%|15.5|34.6%|14.2|
||Octo [30]|14.7%|11.8|4.2%|10.3|24.1%|18.4|14.3%|13.5|
|Vil Mthin|CogACT [18]|**91.0%**|6.1|78.0%|6.4|75.9%|13.7|**81.6%**|8.7|
|sua acg|SpatialVLA [28]|81.7%|6.2|83.3%|6.7|57.4%|14.8|74.1%|9.2|
||_𝜋_0_._5 [13]|83.1%|6.1|81.4%|6.2|60.9%|14.4|75.1%|8.9|
||ST-_𝜋_(Ours)|85.5%|**6.0**|**84.1%**|**6.0**|**68.2%**|**13.7**|79.3%|**8.6**|
||OpenVLA [15]|48.2%|12.6|43.5%|11.7|15.1%|17.6|35.6%|14.0|
||Octo [30]|0.2%|15.8|2.8%|13.6|0.8%|25.8|1.3%|18.4|
|Variant Areation|CogACT [18]|**89.2%**|6.3|80.8%|6.6|25.8%|**13.1**|65.3%|8.7|
|ggg|SpatialVLA [28]|85.7%|7.0|76.1%|7.5|25.9%|15.2|62.6%|9.9|
||_𝜋_0_._5 [13]|84.6%|6.1|78.3%|6.8|31.2%|13.5|64.7%|8.8|
||ST-_𝜋_(Ours)|86.7%|**5.8**|**81.4%**|**6.2**|**33.6%**|13.3|**67.2%**|**8.4**|


**Comparison Methods.** We compare our model with several representative VLA approaches, including OpenVLA [15], Octo [30], Diffusion Policy [8], SpatialVLA [28], TraceVLA [39], 4D-VLA [37], _𝜋_ 0 _._ 5 [13], and CogACT [18]. The first three methods are 2D VLA models operating on single-frame images. The next two methods are 3D VLA models incorporating 3D positions. 4D-VLA is the 4D method with spatiotemporal visual observations. The last two methods adopt dual-system architectures within the VLA framework. 

**Evaluation Metrics.** We evaluate all models on three benchmarks: LIBERO [22], SIMPLER [19] and our **STAR** . For LIBERO and SIMPLER, models are trained on the corresponding dataset and evaluated within the same environment. For real-world experiments, we fine-tune models on the **STAR** dataset. We report task success rate and completion time as the primary evaluation metrics. 

The results highlight the importance of structured spatiotemporal modeling in long-horizon manipulation tasks. 

**Evaluation on SIMPLER.** We adopt SIMPLER [19] as an additional simulation benchmark for scalable evaluation. SIMPLER provides a suite of simulation environments that replicate common real-world robotic setups and supports real-to-sim evaluation. The benchmark consists of two evaluation protocols, _Visual Matching_ and _Variant Aggregation_ , which assess generalization under visual distribution shifts and environment variations. We compare our ST- _𝜋_ with several representative baselines, including OpenVLA [15], Octo [30], CogACT [18], SpatialVLA [28], and _𝜋_ 0 _._ 5 [13]. As shown in Tab. 2, our method achieves competitive performance across evaluation protocols, demonstrating efficient execution in simulations. 

## **5.2 Comparison on Simulation Benchmarks** 

**Evaluation on LIBERO.** We fine-tune and evaluate all competing models in four suites of LIBERO. From the results in Tab. 1, we derive three main observations. First, performance improves as observations become more expressive, evolving from 2D single-frame inputs to 3D spatial representations and further to 4D spatiotemporal observations. Second, VLA models adopting dual-system architectures with high-level behavior planning and low-level action generation consistently outperform single-system counterparts. Third, our model achieves the highest success rates and the shortest completion time on most tasks. This advantage is primarily attributed to the explicit modeling of spatiotemporal sub-task dependencies. 

## **5.3 Comparison on Real-World STAR** 

To validate the practical applicability of our framework, we conduct real-world experiments on a Franka Research 3 platform. All competing methods are fine-tuned on the **STAR** dataset in Sec. 4.1 and evaluated on three evaluation suites. As shown in Fig. 7 and Tab. 3, our model achieves the highest average success rate across all evaluation suites. The performance gap becomes more pronounced in long-horizon manipulation scenarios, where precise behavior transitions and task decomposition are critical for planning. This result indicates that explicit structured spatiotemporal modeling of task decomposition enhances execution stability and robustness in real-world robotic manipulation environments. 

7 


**Figure 7: Real-world performance comparison. We evaluate different VLA methods on real-world tasks with increasing complexity. Our ST-** _𝜋_ **consistently outperforms all baselines, demonstrating robustness in long-horizon manipulation.** 

## **5.4 Ablation Study** 

**Effect of the Structured Spatiotemporal Framework.** To evaluate the effect of the structured spatiotemporal framework, we conduct an ablation study isolating the contributions of the ST-VLM and the ST-AE. We compare four variants by enabling or disabling (i) structured task decomposition in ST-VLM and (ii) spatiotemporal motion generators in ST-AE. When decomposition is disabled, the model directly generates actions for the entire task without predicting intermediate sub-tasks; when the structured ST-AE is removed, motion generators are replaced with a standard full-attention policy. As shown in Tab. 4, both components contribute to performance. ST-VLM improves long-horizon manipulation stability by modeling chunk-level dependencies, while the ST-AE enhances action consistency by enforcing spatial coherence and temporal causality. The combination yields the best performance, demonstrating that structured planning and action generation are complementary and critical for fine-grained spatiotemporal manipulation. 

### **Ablation on High-Level Spatiotemporal Attention Structure.** 

We further analyze the effect of the spatiotemporal attention structure in ST-VLM for sub-task decomposition. In our ST- _𝜋_ , the predicted sub-tasks follow a causal attention constraint enforcing temporal ordering during decomposition. We compare three attention configurations in Tab. 5. Results show that the causal attention structure consistently yields the best performance across different task suites and evaluation metrics. Bidirectional attention weakens the 

temporal structure in decomposition, while removing inter-chunk attention entirely drops the dependencies between sub-tasks. This suggests that explicitly modeling causal dependencies is necessary for stable planning and coherent long-horizon execution. 

**Ablation on the Observation Modality.** We further study the impact of the observation modality. Our full model leverages multiframe observations with geometric features, forming structured 4D representations. We progressively simplify the observations and compare three settings: 4D observations (multi-frame images + geometric features), 3D observations (single-frame image + geometric features), and 2D observations (single-frame image only). Results in Tab. 6 show that performance consistently degrades as observations are simplified. Using multi-frame observations leads to more stable long-horizon execution, while geometric features provide spatial cues for precise manipulation. The full 4D representation achieves the best performance, demonstrating the importance of jointly modeling appearance, geometry, and temporal context. 

## **5.5 Discussion** 

**Role of Spatiotemporal Generators.** We analyze how the spatiotemporal motion generators in ST-AE influence action generation behavior. In Fig. 8, we visualize the trajectories under three configurations, each isolating the spatial and temporal generators. The spatial-only variant produces coherent trajectories, but exhibits irregular step sizes, leading to unstable temporal progression. In 

8 


**Figure 8: Trajectory comparison of different motion generator variants. (a) Task illustration. (b) Only the spatial motion generator produces smooth but irregular-velocity trajectories. (c) Only the temporal motion generator produces nearly constantvelocity but non-smooth trajectories. (d) Combining both yields smooth and temporally consistent trajectories.** 

**Table 4: Effect of Structured Spatiotemporal Framework.** 

|SpatioTemporal|SpatioTemporal|LIBERO|Avg.|STA|R|
|---|---|---|---|---|---|
|VLM|Action Expert|SR↑|CT↓|SR↑|CT↓|
|✗|✗|96.9%|6.3|76.8%|16.2|
|✓|✗|97.2%|6.2|78.4%|15.4|
|✗|✓|97.1%|6.0|77.2%|14.6|
|✓|✓|**97.4%**|**5.9**|**80.1% **|**13.5**|


**Table 6: Ablation on Observation Modality.** 

|Modalit|LIBERO|Avg.|STA|R|
|---|---|---|---|---|
|y|SR↑|CT↓|SR↑|CT↓|
|2D|94.6%|6.4|74.2%|16.3|
|3D|96.0%|6.2|77.1%|15.2|
|4D(Ours)|**97.4%**|**5.9**|**80.1%**|**13.5**|


**Table 5: Ablation on High-Level Spatiotemporal Attention.** 

|Mask|LIBERO<br>SR↑|Avg.<br>CT↓|STA<br>SR↑|R<br>CT↓|
|---|---|---|---|---|
|None|92.5%|6.1|73.8%|15.8|
|Bidirectional|96.5%|6.0|78.4%|14.5|
|Causal(Ours)|**97.4**%|**5.9**|**80.1**%|**13.5**|


**Table 7: Effect of Behavioral Decomposition Granularity.** 

|Subtask Number_𝐾_|LIBERO<br>SR↑|Avg.<br>CT↓|STA<br>SR↑|R<br>CT↓|
|---|---|---|---|---|
|_𝐾_=1|96.5%|6.7|76.2%|16.6|
|_𝐾_=2|97.1%|6.1|79.3%|14.3|
|_𝐾_=3|**97.4**%|**5.9**|**80.1**%|13.5|
|_𝐾_=4|97.2%|6.1|79.9%|**13.4**|


contrast, the temporal-only variant generates trajectories with consistent velocities, but lacks spatial smoothness, resulting in jagged motion. Our full model, which integrates both generators, produces trajectories that are both spatially smooth and temporally stable. This demonstrates that the spatial and temporal generators provide complementary inductive biases, and their joint modeling enables coherent and stable action generation. 

**Effect of Task Decomposition Granularity.** We analyze how the granularity of task decomposition influences performance by varying the number of predicted sub-tasks _𝐾_ . We evaluate _𝐾_ ∈{1 _,_ 2 _,_ 3 _,_ 4} while keeping other settings fixed. Results in Tab. 7 show that performance improves as the decomposition becomes more refined, indicating that moderate task decomposition promotes better structure of long-horizon behaviors. When _𝐾_ increases to 4, performance slightly decreases compared to _𝐾_ = 3, suggesting that overly finegrained decomposition may introduce additional prediction noise or reflect insufficient training for deeper decomposition levels. These results indicate that a moderate decomposition granularity provides a trade-off between planning flexibility and stability. 

**Limitation.** Despite its effectiveness, our framework assumes that robotic manipulation tasks can be decomposed into a sequential chain of sub-tasks. While this assumption holds for many robotic 

manipulation scenarios, more complex behaviors may involve parallel or branching structures that cannot be fully captured by a strictly causal decomposition. Extending the framework to support more flexible task structures and richer dependency modeling across sub-tasks remains a valuable direction for future work. 

## **6 Conclusion** 

In this paper, we present ST- _𝜋_ , a structured spatiotemporal VLA framework for fine-grained robotic manipulation. The proposed framework introduces a spatiotemporal vision-language model that explicitly decomposes high-level instructions into structured chunklevel action prompts with semantic, spatial, and temporal representations. We further design a spatiotemporal action expert that generates step-level action parameters through a dual-generator guidance, ensuring spatial coherence and temporal causality during motion generation. To support structured supervision, we construct a real-world dataset termed STAR, with structured annotations for fine-grained spatiotemporal manipulation training. Extensive experiments on simulation benchmarks and real-world robotic platforms demonstrate that our framework achieves consistent improvements over representative VLA baselines. 

9 

## **References** 

- [1] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, et al. 2022. Do as i can, not as i say: Grounding language in robotic affordances. _arXiv preprint arXiv:2204.01691_ (2022). 

- [2] Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui Chen, Zesen Cheng, Lianghao Deng, Wei Ding, Chang Gao, Chunjiang Ge, et al. 2025. Qwen3-vl technical report. _arXiv preprint arXiv:2511.21631_ (2025). 

- [3] Lucas Beyer, Andreas Steiner, André Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. 2024. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ (2024). 

- [4] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. 2024. _𝜋_ 0: A Vision-Language-Action Flow Model for General Robot Control. _arXiv preprint arXiv:2410.24164_ (2024). 

- [5] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. 2022. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ (2022). 

- [6] Dave Zhenyu Chen, Angel X Chang, and Matthias Nießner. 2020. Scanrefer: 3d object localization in rgb-d scans using natural language. In _European conference on computer vision_ . Springer, 202–221. 

- [7] Zhenyu Chen, Ali Gholami, Matthias Nießner, and Angel X Chang. 2021. Scan2cap: Context-aware dense captioning in rgb-d scans. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . 3193–3203. 

- [8] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. 2025. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ 44, 10-11 (2025), 1684–1704. 

- [9] Angela Dai, Angel X. Chang, Manolis Savva, Maciej Halber, Thomas Funkhouser, and Matthias Nießner. 2017. ScanNet: Richly-annotated 3D Reconstructions of Indoor Scenes. In _Proc. Computer Vision and Pattern Recognition (CVPR), IEEE_ . 

- [10] Patrick Esser, Sumith Kulal, Andreas Blattmann, Rahim Entezari, Jonas Müller, Harry Saini, Yam Levi, Dominik Lorenz, Axel Sauer, Frederic Boesel, et al. 2024. Scaling rectified flow transformers for high-resolution image synthesis. In _Fortyfirst international conference on machine learning_ . 

- [11] Chengkai Hou, Yanjie Ze, Yankai Fu, Zeyu Gao, Songbo Hu, Yue Yu, Shanghang Zhang, and Huazhe Xu. 2025. 4D Visual Pre-training for Robot Learning. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . 8451– 8461. 

- [12] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Liang Wang, Weizhu Chen, et al. 2022. Lora: Low-rank adaptation of large language models. _Iclr_ 1, 2 (2022), 3. 

- [13] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. 2025. _𝜋_ 0 _._ 5: a Vision-Language-Action Model with Open-World Generalization. _arXiv preprint arXiv:2504.16054_ (2025). 

- [14] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. 2024. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ (2024). 

- [15] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. 2024. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ (2024). 

- [16] Chengmeng Li, Junjie Wen, Yan Peng, Yaxin Peng, Feifei Feng, and Yichen Zhu. 2025. PointVLA: Injecting the 3D World into Vision-Language-Action Models. _arXiv preprint arXiv:2503.07511_ (2025). 

- [17] Haozhan Li, Yuxin Zuo, Jiale Yu, Yuhao Zhang, Zhaohui Yang, Kaiyan Zhang, Xuekai Zhu, Yuchen Zhang, Tianxing Chen, Ganqu Cui, et al. 2025. Simplevla-rl: Scaling vla training via reinforcement learning. _arXiv preprint arXiv:2509.09674_ (2025). 

- [18] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. 2024. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ (2024). 

- [19] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, Sergey Levine, Jiajun Wu, Chelsea Finn, Hao Su, Quan Vuong, and Ted Xiao. 2024. Evaluating RealWorld Robot Manipulation Policies in Simulation. _arXiv preprint arXiv:2405.05941_ (2024). 

- [20] Yang Li, Si Si, Gang Li, Cho-Jui Hsieh, and Samy Bengio. 2021. Learnable fourier features for multi-dimensional spatial positional encoding. _Advances in Neural Information Processing Systems_ 34 (2021), 15816–15829. 

- [21] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. 2022. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ 

(2022). 

- [22] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. 2023. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ 36 (2023), 44776–44791. 

- [23] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. 2023. Visual instruction tuning. _Advances in neural information processing systems_ 36 (2023), 34892–34916. 

- [24] Xingchao Liu, Chengyue Gong, and Qiang Liu. 2022. Flow straight and fast: Learning to generate and transfer data with rectified flow. _arXiv preprint arXiv:2209.03003_ (2022). 

- [25] Ilya Loshchilov and Frank Hutter. 2017. Decoupled weight decay regularization. _arXiv preprint arXiv:1711.05101_ (2017). 

- [26] Dantong Niu, Yuvan Sharma, Haoru Xue, Giscard Biamby, Junyi Zhang, Ziteng Ji, Trevor Darrell, and Roei Herzig. 2025. Pre-training auto-regressive robotic models with 4d representations. _arXiv preprint arXiv:2502.13142_ (2025). 

- [27] Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin ElNouby, et al. 2023. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ (2023). 

- [28] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. 2025. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ (2025). 

- [29] Gemma Team, Thomas Mesnard, Cassidy Hardin, Robert Dadashi, Surya Bhupatiraju, Shreya Pathak, Laurent Sifre, Morgane Rivière, Mihir Sanjay Kale, Juliette Love, et al. 2024. Gemma: Open models based on gemini research and technology. _arXiv preprint arXiv:2403.08295_ (2024). 

- [30] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. 2024. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ (2024). 

- [31] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. Attention is all you need. _Advances in neural information processing systems_ 30 (2017). 

- [32] Jianyuan Wang, Minghao Chen, Nikita Karaev, Andrea Vedaldi, Christian Rupprecht, and David Novotny. 2025. Vggt: Visual geometry grounded transformer. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ . 5294– 5306. 

- [33] Philipp Wu, Yide Shentu, Zhongke Yi, Xingyu Lin, and Pieter Abbeel. 2023. GELLO: A General, Low-Cost, and Intuitive Teleoperation Framework for Robot Manipulators. 

- [34] Chiao-An Yang, Ryo Hachiuma, Sifei Liu, Subhashree Radhakrishnan, Raymond A Yeh, Yu-Chiang Frank Wang, and Min-Hung Chen. 2025. 4D-RGPT: Toward Region-level 4D Understanding via Perceptual Distillation. _arXiv preprint arXiv:2512.17012_ (2025). 

- [35] Yi Yang, Jiaxuan Sun, Siqi Kou, Yihan Wang, and Zhijie Deng. 2025. Lohovla: A unified vision-language-action model for long-horizon embodied tasks. _arXiv preprint arXiv:2506.00411_ (2025). 

- [36] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. 2023. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF international conference on computer vision_ . 11975–11986. 

- [37] Jiahui Zhang, Yurui Chen, Yueming Xu, Ze Huang, Yanpeng Zhou, Yu-Jie Yuan, Xinyue Cai, Guowei Huang, Xingyue Quan, Hang Xu, et al. 2025. 4d-vla: Spatiotemporal vision-language-action pretraining with cross-scene calibration. _arXiv preprint arXiv:2506.22242_ (2025). 

- [38] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 2024. 3d-vla: A 3d vision-language-action generative world model. _arXiv preprint arXiv:2403.09631_ (2024). 

- [39] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daumé III, Andrey Kolobov, Furong Huang, and Jianwei Yang. 2024. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv preprint arXiv:2412.10345_ (2024). 

- [40] Hanyu Zhou and Gim Hee Lee. 2025. Llava-4d: Embedding spatiotemporal prompt into lmms for 4d scene understanding. _arXiv preprint arXiv:2505.12253_ (2025). 

- [41] Hanyu Zhou and Gim Hee Lee. 2025. Uni4d-llm: A unified spatiotemporal-aware vlm for 4d understanding and generation. _arXiv preprint arXiv:2509.23828_ (2025). 

- [42] Hanyu Zhou, Chuanhao Ma, and Gim Hee Lee. 2025. VLA-4D: Embedding 4D Awareness into Vision-Language-Action Models for SpatioTemporally Coherent Robotic Manipulation. _arXiv preprint arXiv:2511.17199_ (2025). 

- [43] Zewei Zhou, Tianhui Cai, Seth Z Zhao, Yun Zhang, Zhiyu Huang, Bolei Zhou, and Jiaqi Ma. 2025. Autovla: A vision-language-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. _arXiv preprint arXiv:2506.13757_ (2025). 

- [44] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. 2023. Rt-2: Vision-languageaction models transfer web knowledge to robotic control. In _Conference on Robot Learning_ . PMLR, 2165–2183. 

10 

