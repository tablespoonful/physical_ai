---
title: "DM0: An Embodied-Native Vision-Language-Action Model towards Physical AI"
date: "2026-02-16"
authors: "En Yu; Haoran Lv; Jianjian Sun; Kangheng Lin; Ruitao Zhang; Yukang Shi"
url: https://arxiv.org/abs/2602.14974
pdf: https://arxiv.org/pdf/2602.14974
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.14974)** / [論文ページ](https://arxiv.org/abs/2602.14974)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。



# **DM0: An Embodied-Native Vision-Language-Action Model towards Physical AI** 

**DM0 Team, Dexmal & StepFun** 

**Github:** **`https://github.com/Dexmal/dexbotic` Huggingface:** **`https://huggingface.co/collections/Dexmal/dm0`** 

## **Abstract** 

Moving beyond the traditional paradigm of adapting internet-pretrained models to physical tasks, we present **DM0** , an Embodied-Native Vision-Language-Action (VLA) framework designed for Physical AI. Unlike approaches that treat physical grounding as a fine-tuning afterthought, **DM0** unifies embodied manipulation and navigation by learning from heterogeneous data sources from the onset. Our methodology follows a comprehensive three-stage pipeline: Pretraining, Mid-Training, and Post-Training. First, we conduct large-scale unified pretraining on the Vision-Language Model (VLM) using diverse corpora—seamlessly integrating web text, autonomous driving scenarios, and embodied interaction logs—to jointly acquire semantic knowledge and physical priors. Subsequently, we build a flow-matching action expert atop the VLM. To reconcile high-level reasoning with low-level control, **DM0** employs a hybrid training strategy: for embodied data, gradients from the action expert are not backpropagated to the VLM to preserve generalized representations, while the VLM remains trainable on non-embodied data. Furthermore, we introduce an Embodied Spatial Scaffolding strategy to construct spatial Chain-of-Thought (CoT) reasoning, effectively constraining the action solution space. Experiments on the RoboChallenge benchmark demonstrate that **DM0** achieves state-of-the-art performance in both Specialist and Generalist settings on Table30. 


Figure 1 | **DM0** is pretrained on diverse corpora—seamlessly integrating web, autonomous driving and embodied data. It jointly acquire semantic knowledge and physical priors. 

### **Contents** 

|**1**|**Intr**|**oduction**|**3**|
|---|---|---|---|
|**2**|**Mo**|**del Description**|**4**|
||2.1|Model Architecture . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . .<br>4|
||2.2|Multi-Source Hybrid Training . . . . . . . . . . . . . . .|. . . . . . . . . . . . . .<br>5|
||2.3|Embodied Spatial Scaffolding . . . . . . . . . . . . . . .|. . . . . . . . . . . . . .<br>5|
|**3**|**Tra**|**ining Recipe**|**6**|
||3.1|Pretraining<br>. . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . .<br>6|
||3.2|Mid-Training . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . .<br>7|
||3.3|Post-Training . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . .<br>10|
|**4**|**Exp**|**erimental Evaluations**|**10**|
||4.1|Experimental Setup<br>. . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . .<br>10|
||4.2|RoboChallenge Results . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . .<br>11|
||4.3|Multimodal Understanding<br>. . . . . . . . . . . . . . . .|. . . . . . . . . . . . . .<br>11|
|**5**|**Dis**|**cussion**|**14**|
||5.1|Conclusion<br>. . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . .<br>14|
||5.2|Future Work<br>. . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . .<br>14|
|**6**|**Aut**|**hor List**|**20**|


2 

### **1. Introduction** 

The pursuit of Physical AI—artificial intelligence capable of perceiving, reasoning, and acting in the physical world—is a central goal of robotics and computer vision. Recent breakthroughs in Large Language Models (LLMs) (DeepSeek-AI, 2024; Touvron et al., 2023; Yang et al., 2025a) and Vision-Language Models (VLMs) (Bai et al., 2025; Huang et al., 2026; Team et al., 2025) have endowed agents with impressive semantic understanding and reasoning capabilities. Building upon these foundations, Vision-Language-Action (VLA) (Black et al., 2024, 2025; Li et al., 2024; Shi et al., 2025; Sun et al., 2025; Zitkovich et al., 2023) models have emerged as a promising paradigm to bridge the gap between high-level cognition and low-level motor control, driving progress towards generalist robots that can operate in unstructured human environments. 

However, current VLA research predominantly follows a ”Pretrain-then-Adapt” paradigm (Black et al., 2025; NVIDIA et al., 2025; Wen et al., 2025; Xie et al., 2025). Typically, models are first pretrained solely on massive static internet datasets (e.g., image-text pairs) and subsequently fine-tuned on limited embodied data. While effective for semantic alignment, this approach suffers from a critical limitation: the model lacks intrinsic physical grounding (Kim et al., 2024; Li et al., 2024). Internet data provides semantic knowledge but fails to capture the dynamic, continuous, and spatial nature of physical interactions. Consequently, adapting these ”Internet-Native” models often leads to distinct module fragmentation (separating navigation from manipulation) or catastrophic forgetting, where the pursuit of motor skills degrades the model’s general reasoning capacity. 

We argue that true generalist robots require an Embodied-Native framework. This entails training the model from scratch (or from very early stages) with a unified perspective that treats embodied sensorimotor data as a first-class citizen alongside linguistic and visual data. Such a framework must harmonize heterogeneous data sources—spanning web corpus, autonomous driving logs, and robot manipulation trajectories—to learn representations that are simultaneously semantically rich and physically actionable. 

To realize this vision, we introduce **DM0** , an Embodied-Native VLA framework designed to unify manipulation and navigation. Unlike conventional adaptation methods, **DM0** is built upon a multi-source, three-stage training pipeline: Pretraining, Mid-Training, and Post-Training. Our framework is anchored by three key components. 

- **Unified Pre-training on Vision-Language, Driving and Embodied Corpus:** In the initial stage, we perform large-scale unified pretraining on the VLM using diverse corpora—integrating vision-language data, driving scenes data, and embodied action data. This ensures the model acquires physical priors (e.g., spatial relations, physics dynamics) concurrently with semantic knowledge. 

- **Hybrid Training Architecture:** To translate this understanding into precise actions, we construct a flow-matching action expert upon the VLM. During Mid- and Post-Training, we employ a hybrid gradient strategy: gradients from the action expert are decoupled from the VLM for embodied tasks to prevent the erosion of general knowledge, while the VLM continues to learn from non-embodied data. 

- **Embodied Spatial Scaffolding Strategy:** To further bridge the reasoning-action gap, we propose an Embodied Spatial Scaffolding strategy. This mechanism generates spatial Chain-of-Thought (CoT) reasoning to decompose complex instructions, effectively constraining the action solution space for the policy. 

Extensive experiments on the RoboChallenge benchmark show that **DM0** outperforms ex- 

3 

isting policies, including GigaBrain-0.1 (GigaAI, 2025), Spirit-v1.5 (Team, 2026) and _𝜋_ 0.5 (Black et al., 2025), achieving state-of-the-art results on Table30 in both Specialist and Generalist settings. Specifically, **DM0** -Specialist achieves an average 62.0% success rate for thirty Table30 tasks, surpassing previous SoTA GigaBrain-0.1 by more than 10% margins. **DM0** -Generalist produces an average 37.3% success rate, surpassing _𝜋_ 0.5-Generalist by a large margin, showing superior generalization ability. 

### **2. Model Description** 

#### **2.1. Model Architecture** 


Figure 2 | Model Architecture. **DM0** consists of a vision-language model (VLM) backbone and a Flow Matching (Lipman et al., 2022) based action expert. The VLM processes multi-modal inputs and generates embodied reasoning representations, which are subsequently consumed by the action expert to produce continuous robot actions. 

The **DM0** model, illustrated in Figure 2, is an end-to-end Vision-Language-Action (VLA) model that supports joint training on large-scale datasets spanning diverse tasks and data distributions, including web-scale multi-modal data, driving-scene data, and embodied data. 

The proposed architecture is composed of two core components: (i) a VLM built on the Qwen3-1.7B large language model (LLM) (Yang et al., 2025a), augmented with a perception encoder (PE) (Bolya et al., 2025) to enable multi-modal perception, semantic understanding, and embodied reasoning in robotic environments; and (ii) an action expert based on Flow Matching (Lipman et al., 2022), which generates continuous control actions conditioned on the key-value (KV) cache extracted from the VLM backbone. The multi-view images are resized to 728 × 728 and input to the PE, after which the image embeddings are downsampled by 4× using two 3 × 3 convolutional layers with stride 2. 

At inference time, **DM0** supports two alternative inference modes. In the first mode, the model directly predicts continuous action sequences from multi-modal observations and language instructions. In the second mode, the model first generates textual outputs for embodied reasoning, and subsequently conditions the action expert on these outputs to produce continuous actions. Formally, the distribution of the joint model is factorized as follows. 


Here, **a** _𝑡_ : _𝑡_ + _𝐻_ denotes the continuous action sequence over a horizon of _𝐻_ time steps. The 

4 

multi-modal observation at time step _𝑡_ is indicated by **o** _𝑡_ = [ **I** _𝑡_ , **s** _𝑡_ ], where **I** _𝑡_ represents visual inputs and **s** _𝑡_ corresponds to the proprioceptive state of the robot. The variable _𝑙_ denotes the language instruction and _𝑙_<sup>ˆ</sup> denotes the predicted textual output. 

#### **2.2. Multi-Source Hybrid Training** 

Several previous works (Driess et al., 2025) (Zhang et al., 2026) have investigated unified training paradigms that integrate VLM with an action expert for end-to-end learning. Although such approaches offer architectural simplicity, the jointly optimization of language and continuous control objectives has been observed to adversely affect the semantic representations preserved in pretrained VLM, potentially undermining their language understanding and reasoning capabilities. 

We adopt a hybrid gradient strategy inspired by Knowledge Insulation (KI) (Driess et al., 2025) that decouples gradients from the action expert when training on embodied data, thereby preventing the erosion of semantic knowledge in the pretrained VLM. At the same time, the VLM continues to be updated using non-embodied data, allowing the model to further refine its general language and visual understanding capabilities. In addition, the VLM is supervised to predict discrete action tokens, encouraging it to encode action-relevant semantics that are beneficial for downstream action prediction. We provide a detailed description of the training procedure in the following. 

The VLM is trained to predict embodied reasoning text and discrete action tokens by minimizing the auto-regressive cross-entropy loss: 


The action expert is trained to predict continuous action sequences by minimizing the Flow Matching loss: 


Where, **A** _𝑡_ : _𝑡_ + _𝐻_ denotes the ground-truth continuous action sequence, and **a** ˜ _𝑡_ : _𝑡_ + _𝐻_ = _𝜏_ **A** _𝑡_ : _𝑡_ + _𝐻_ + (1 − _𝜏_ ) _𝜀_ is the noisy action obtained by injecting Gaussian noise _𝜀_ ∼N ( **0** , **I** ). The variable _𝜏_ ∈[0, 1] represents the flow time step. 

The overall training objective is defined as a weighted combination of the two losses: 


where _𝜆_ is a scalar weighting coefficient. During joint training, we set _𝜆_ = 1. 

#### **2.3. Embodied Spatial Scaffolding** 

During the joint training stage, we introduce a set of auxiliary objectives organized as a hierarchical prediction framework to provide structured supervision. Specifically, the model is trained to sequentially perform the following tasks: 

- (i) **Subtask prediction** : Predict a fine-grained task description that decomposes the overall task into a sequence of interpretable and manageable steps. 

5 

- (ii) **Goal bounding box prediction** : Predict the bounding box of the target object or goal-relevant region within the visual observation. 

- (iii) **End-effector trajectory prediction** : Predict the future trajectory of the robot end effector in the primary camera view over a specified horizon. 

- (iv) **Discrete action prediction** : Predict discrete action tokens that represent the robot control commands. 

This design induces a natural curriculum over levels of abstraction, guiding the model to progressively transition from high-level semantic reasoning to spatial grounding and ultimately to low-level control. From a theoretical perspective, this hierarchical supervision introduces a sequence of task-aligned inductive biases that progressively constrain the model’s hypothesis space. Each intermediate objective functions as a structured information bottleneck, suppressing task-irrelevant variation while preserving semantically and geometrically meaningful structure. In particular, subtask prediction encourages the model to encode high-level intent, goal bounding box prediction enforces object-centric spatial grounding, and trajectory prediction further aligns the learned representations with action-relevant geometry. Together, these objectives encourage representations that become increasingly structured and causally aligned with the underlying visuomotor decision-making process. 

### **3. Training Recipe** 

**DM0** is trained in three sequential stages that progress from general vision-language ability to embodied control and finally to deployment-ready policies. We accordingly design three training recipes, each tailored to the objective of its stage. **Pretraining** establishes a strong multimodal foundation on large-scale web, driving, and embodied data. **Mid-training** adds action prediction and grounds the model in cross-embodiment robot data while retaining general dialogue ability. **Post-training** narrows the embodiment and data scope to stabilize visuomotor alignment on a small set of target platforms. We describe each stage below. 

#### **3.1. Pretraining** 

The goal of pretraining is to learn a general vision-language model with strong multimodal alignment, fine-grained perception, and broad reasoning over web, document, driving, and embodied data. By jointly training on these heterogeneous sources, the model acquires both semantic knowledge and physical priors (e.g., spatial relations and grounding in real-world scenes). The resulting VLM then serves as the backbone that we extend in mid-training with action prediction and embodiment-specific supervision. 

**Data construction.** To support both fine-grained perception and broad reasoning, we build a multimodal pretraining corpus spanning the following domains. 

**Knowledge.** Web-sourced interleaved data come from Common Crawl, StepCrawl, and keyword-based searches; we filter out pages with an image download failure rate exceeding 90%, QR-code images, and extreme aspect ratios. Image–text pairs are drawn from open collections (LAION (Schuhmann et al., 2022), COYO (Byeon et al., 2022), BLIP-CCS (Li et al., 2022), Zero (Xie et al., 2023)) and curated via CLIP-based balanced resampling, keyword retrieval, and caption mining from interleaved context based on CLIP similarity and aesthetic scores. We also construct mosaic inputs by concatenating four images into a single training sample. 

**Education.** Samples cover K-12 (math, physics, chemistry, geometry, chemical formulas; open and synthetic sources including CoSyn (Yang et al., 2025b)), university (STEM, medicine, 

6 

arts, finance), and adult learning (e.g., driving license, CPA, legal exams). Questions are sourced from licensed examination materials and open problem sets (Ben Abacha et al., 2019; He et al., 2020; Sujet AI, 2024); supporting content from textbooks, workbooks, and educational sites. 

**OCR.** Image-to-text uses real and synthetic images (PaddleOCR (Cui et al., 2025), SynthDog (Kim et al., 2022)). Image-to-code covers Markdown, L<sup>A</sup> TEX, Matplotlib (open and rule-based synthetic charts), and TikZ/Graphviz. Document-to-text uses document pages (PaddleOCR or MinerU 2.0 (Wang et al., 2024)); document-to-code spans HTML, Markdown, and LaTeX (web/GitHub/arXiv) and open datasets (Chai et al., 2025; Laurençon et al., 2024; Liu et al., 2024; Yuan et al., 2022). An OCR-VQA subset combines open data with QA pairs generated from other OCR tasks. 

**Grounding & Counting.** Bounding-box and point-level grounding are derived from open detection datasets (OpenImages (Kuznetsova et al., 2020), COCO (Lin et al., 2014), Merlin (Yu et al., 2024, 2025), PixMo (Deitke et al., 2024)) and in-house document paragraph detection. Counting data are obtained from public benchmarks (Kaggle; SakiRinn) and by converting detection annotations into counting supervision. 

**VQA.** General VQA draws on open benchmarks (Liu et al., 2025; Zellers et al., 2019) and QA pairs generated from captions. 

**GUI.** The GUI subset (Yan et al., 2025) includes interface captions, knowledge VQA, trajectories (across atomic actions), grounding, and web OCR with element coordinates. 

**Driving.** Driving-scene samples include depth-aware detection and grounding annotations (category labels, metric depth, bounding boxes in normalized [0, 1000] coordinates). License plates are masked where required for privacy compliance. 

**Embodied.** We include embodied data formulated as grounding and caption QA tasks (e.g., object and region localization, scene and spatial-relation descriptions over robot observations), so the model acquires physical and spatial priors alongside semantic knowledge. 

Together, these domains establish the perceptual and reasoning foundation that mid-training subsequently integrates with action supervision. 

**Training settings.** Pretraining is conducted in a single stage with all parameters jointly optimized. We optimize with AdamW (Loshchilov and Hutter, 2017) ( _𝛽_ 1 = 0.9, _𝛽_ 2 = 0.95, _𝜀_ = 10<sup>−8</sup> , weight decay 0.01), for 1.2T tokens in 370K steps (global batch 8,192, length 4,096). The learning rate is scheduled in two phases: 900B tokens with linear decay from 5 × 10<sup>−5</sup> to 1 × 10<sup>−5</sup> for general representation learning; then 300B tokens with linear decay from 1 × 10<sup>−5</sup> to 6 × 10<sup>−6</sup> on a higher-quality mix to strengthen OCR, grounding, and reasoning capabilities. The resulting model serves as the backbone for the next stage, where we add action prediction and cross-embodiment control. 

#### **3.2. Mid-Training** 

Building on the pretrained backbone, mid-training introduces action prediction and grounds the model in physical control. This stage uses a single training loop that jointly supervises text tokens, discrete action tokens, and continuous actions via the action expert. As a result, the model learns to couple language reasoning with executable physical actions. 

**Goal and supervision.** Mid-training optimizes three aligned supervision targets: (i) multimodal dialogue tokens, (ii) discretized action trajectories (action tokens), and (iii) continuous action trajectories from the action expert. The latter two correspond to the same underlying 

7 


Figure 3 | **Overview of Curated Vision-Language Data.** The curated dataset is designed to enhance core embodied reasoning abilities while preserving the general multimodal understanding and reasoning capabilities of the pretrained VLM. 

sequence, represented in quantized and continuous forms, respectively. Cross-embodiment robot data are mixed with vision-language and reasoning data; we also retain a portion of high-quality vision-language data from pretraining to preserve general multimodal capability. 

**Data mixture.** The data mixture (overview in Figure 3, proportions in Figure 4) balances retention of general VLM ability with embodiment-specific learning. It is organized into five categories: 

- **Vision–language data.** To preserve general multimodal understanding and instructionfollowing ability, we include: (1) `Cambrian-737k` (Tong et al., 2024); (2) `Cambrian-10M (filtered)` (Tong et al., 2024), from which we remove low-quality samples and content less relevant to embodied learning (e.g., mathematics-heavy problems, non-English data, purely writing-centric content); (3) `LLaVA OneVision (OV) 1.5` (An et al., 2025); and (4) `Self-collected multimodal data` , which includes caption-reannotated embodied data from the pretraining stage (embodied-scene grounding and spatial-relation VQA) as well as other self-collected multimodal data (e.g., GUI grounding and OCR). 

- **Embodied reasoning (ER) data.** We construct ER datasets to strengthen high-level planning and temporal reasoning: (1) **Task Decomposition** , generating the full sequence of steps required to accomplish a task; (2) **Subtask Prediction** , predicting the next subtask to execute; (3) **Action QA** , predicting the action that transitions between two frames; (4) **Temporal reasoning** , recognizing the task being performed and identifying the next subtask; and (5) **Task Progress Estimation** , estimating the current progress toward task completion. 

- **Simulation data.** We include trajectories from (1) four LIBERO (Liu et al., 2023) tasks (Spatial, Goal, Object, and Long); (2) RoboTwin2.0 (Chen et al., 2025) with 50 tasks; and 

8 


Figure 4 | Data mixture ratios for pretraining, midtraining and post-training. After weighted sampling, the total data volumes for the three stages are 1.13T tokens (pretraining), 200M samples (mid-training), and 50M samples (post-training). 

(3) self-collected navigation trajectories in Habitat. 

- **Single-arm robotic data.** Trajectories from single-arm manipulation, including (1) selfcollected data spanning multiple embodiments (e.g., Franka, UR5, ARX-5, and UMI), and (2) open-source data (OXE (Vuong et al., 2023) and Fuse (Jones et al., 2025)). 

- **Dual-arm robotic data.** Bi-manual manipulation trajectories, including (1) self-collected data on ALOHA, and (2) open-source data (RoboMind (Wu et al., 2025), Agibot Alpha (Bu et al., 2025), and Galaxea Open World (Team, 2025a)). 

**Data representation and processing.** To support the mixed supervision above, we use two representation styles. Robotic data are stored as episodic JSONL records, where each line corresponds to a timestep with (a) multi-view visual observations (images or video frame references), (b) language instruction, (c) proprioceptive state (used to derive the next-step action by temporal shifting), and optionally **subtask** , **goal box** , and **2D gripper waypoint traces** . Vision–language data are either stored in a ready-to-train conversation format or as minimal keys. In the latter case, full conversations are constructed on-the-fly using a conversation template. From these representations we build (i) multimodal multi-turn dialogues and (ii) continuous trajectory data. The multi-turn dialogue is assembled into a chain-of-thought (CoT) sequence, while the model ultimately predicts the corresponding action trajectory. 

- **Trajectory representation.** For robotic data, we train on per-timestep trajectory samples; for vision–language and ER data, we train with multi-turn conversations. Multi-view images are deterministically ordered and truncated or padded to a fixed number of views (three in our setting). If available, 2D waypoint traces and goal boxes are attached as auxiliary supervision. 

- **Duplicate data removal.** To reduce redundancy in embodiment data, particularly for end-effector (EEF) trajectories, we apply keyframe sampling. This process involves selecting critical frames that capture significant state changes, thereby filtering out repetitive or static segments before training. 

**Conversation augmentation.** All data are expressed as template-based conversations so that the same supervision (text, actions, waypoints, etc.) can be presented in varied natural language. 

- **Templates and supervision fields.** For robot trajectories, the dialogue is constructed from a task instruction and may optionally include additional supervision fields: **Subtask** 

9 

(natural language description), **2D waypoint trace** (projected gripper waypoints), **Goal box** (target bounding box), and **Action** (both discretized action tokens for the VLM and continuous action targets for the action expert). If a supervision field is absent, we automatically select a compatible template that omits that field. For ER and navigation data, we use specialized template families tailored to the supervision type (e.g., QA, reasoning, progress estimation). 

- **Template augmentation.** To improve generalization, we design 500 distinct conversation templates for each specific data combination scenario, which are manually polished for quality. During training, we randomly select one of these templates for each sample, introducing linguistic diversity and preventing overfitting to specific prompt structures. 

**Action formulation.** Actions are supervised in two aligned views over the same sequence: discrete tokens for the VLM and continuous values for the action expert. Per-timestep next actions are constructed via temporal state shifting. We construct short-horizon windows of length 50, normalize them, and quantize them into a 255-bin vocabulary as special action tokens. The VLM predicts tokenized trajectories, while the action expert regresses continuous trajectories. 

**Training settings.** Mid-training runs for one epoch on 64× NVIDIA H20 GPUs with AdamW (learning rate decaying from 2.5 × 10<sup>−5</sup> to 1 × 10<sup>−5</sup> ), a maximum sequence length of 4,096, and AMP enabled. Each sample uses three images with ColorJitter augmentation; per-device batch size is 6. The resulting model supports multimodal conversation and action trajectory prediction across diverse embodiments. Post-training then narrows the embodiment and data scope for deployment. 

#### **3.3. Post-Training** 

Post-training starts from the mid-trained model and specializes it for deployment by concentrating robot data on a small set of target embodiments. Narrowing embodiment diversity reduces distributional variance and stabilizes cross-modal alignment, enabling the model to learn finegrained visuomotor correspondences and action semantics where they matter most for the chosen manipulators. 

**Data strategy and mixture.** The data mixture consists of (1) a resampled subset of midtraining vision–language data to preserve general dialogue ability, and (2) single-arm and dualarm robotic data limited to the target embodiments. Data representation, conversation templates, and action formulation remain identical to those used in mid-training. 

**Training settings.** Training continues under the same joint supervision (text, discrete action tokens and continuous action expert targets) and the same optimization configuration as midtraining. Only the data sampling and the set of target embodiments are modified. The resulting model specializes to the target platforms while retaining general multimodal ability. 

### **4. Experimental Evaluations** 

#### **4.1. Experimental Setup** 

**Benchmark Protocols.** Given DM0’s focus on physical-world interaction, we evaluate it on the real-world **RoboChallenge** benchmark [(Team, 2025b)], which features a comprehensive suite of over 30 long-horizon tabletop manipulation tasks (see **Table 30** ). These tasks require multi-step reasoning, spatial understanding, and precise continuous control, covering domains 

10 

such as object picking, placement, rearrangement, tool usage, and compositional instruction following. 

**Training Setup.** During the supervised fine-tuning (SFT) phase, we employ two distinct training configurations, differentiated by their data sources and evaluation scopes. 

- **SFT (Specialist):** This configuration is trained exclusively on data from the target task. The model was fine-tuned on 8×H20 GPUs with a batch size of 4 per GPU for 40K to 150K iterations, contingent upon task complexity. We set the action horizon to 50 steps. For tasks involving repetitive sub-goals, progress supervision was applied to enhance learning efficacy and performance. 

- **SFT (Generalist):** This configuration is trained on data aggregated from all available tasks for the target robot platform and is consequently evaluated on the full suite of tasks for that robot. Training was conducted on 16×H20 GPUs with a batch size of 4 per GPU for 200K iterations, with an action horizon of 50 steps. 

**Comparison Models.** We benchmark DM0 against several leading open-source models, including GigaBrain-0.1 (GigaAI, 2025), Spirit-V1.5 (Team, 2026), _𝜋_ 0.5 (Black et al., 2025), and _𝜋_ 0 (Black et al., 2024). 

The benchmark evaluates performance using both success rate and a composite task score. In our analysis, we report the success rate for the specialist setting, but provide both metrics for the generalist setting due to the low success rate for all models. 

#### **4.2. RoboChallenge Results** 

In Table 1, we benchmark the DM0 specialist model against strong open-source baselines within the 3B–5B parameter range. The results demonstrate that DM0, despite having only 2B parameters, consistently outperforms all compared models across multiple robot platforms (UR5, Franka, ARX5, ALOHA) and achieves a superior overall success rate of 62.00%. The performance advantage is particularly pronounced in complex, long-horizon tasks such as arrange fruits in basket, plug in network cable and sweep rubbish, where DM0 achieves perfect or near-perfect success while other models frequently fail. This indicates that DM0’s design offers significantly more efficient and effective task-specific manipulation capabilities. In Table 2, we compare the DM0-generalist model against the _𝜋_ 0-generalist and _𝜋_ 0.5-generalist models. The DM0-generalist achieves a combined average success rate and task score of 37.3/49.08, substantially outperforming both _𝜋_ 0.5-generalist (17.67/31.27) and _𝜋_ 0-generalist (9.0/20.22). This performance edge is consistent across nearly all robot platforms and task categories. Notably, DM0-generalist excels in tasks requiring precise manipulation and long-horizon reasoning, such as stack color blocks(100/100.0), place shoes on rack(100/98.5), put cup on coaster (100/100.0), and search green boxes(100/100.5), where it often achieves perfect scores while competing models achieve low scores. The results indicate that DM0’s generalist formulation provides superior cross-task adaptability and robust performance. 

All evaluated checkpoints of specialist and generalist models and inference code are published in **https://github.com/dexmal/Dexbotic-RoboChallengeInference** . 

#### **4.3. Multimodal Understanding** 

We further evaluate the multimodal capabilities of DM0 (mid-training checkpoint) on a suite of visual question-answering (VQA) samples. The results indicate that DM0 retains core 

11 

Table 1 | Comparison with state-of-the-art open-source VLA models on Table30 benchmark in RoboChallenge. List in success rate. Tasks with * use the progress supervision. **100** for highest and <u>90</u> for second highest. The data is reported before 20260210. 

||||**M**|**odel**||
|---|---|---|---|---|---|
||**Benchmark**|DM0|Spirit-v1.5|GigaBrain-0.1|_𝜋_0.5|
|||2B|4B|3B|3B|
||arrange fruits in basket|**100**|80|60|40|
|**UR5**|hang toothbrush cup|**80**|**80**|40|50|
||set the plates|**100**|80|90|80|
||shred scrap paper|**30**|20|0|0|
||sort books|**20**|0|0|0|
||stack color blocks|**100**|80|**100**|**100**|
||move objects into box|**100**|80|90|50|
|**Franka**|press three buttons|**90**<sup>∗</sup>|**90**|40|0|
||arrange flowers|**70**|50|40|50|
||arrange paper cups|30|0|**80**|0|
||fold dishcloth|**20**|**20**|10|**20**|
||open the drawer|**100**|70|**100**|40|
||place shoes on rack|**100**|90|50|90|
|**ARX5**|put cup on coaster|**100**|90|**100**|90|
||search green boxes|**100**|90|80|80|
||sort electronic products|0|30|0|**50**|
||turn on light switch|**80**|**80**|60|40|
||water potted plant|**80**<sup>∗</sup>|0|60|0|
||wipe the table|0|0|0|0|
||clean dining table|0|30|**40**|10|
||make vegetarian sandwich|0|0|0|0|
||plug in network cable|**80**|0|0|20|
||pour fries into plate|40|**50**|**50**|30|
||put opener in drawer|30|**80**|40|**80**|
|**ALOHA**|put pen into pencil case|90|90|**100**|80|
||scan QR code|0|0|10|**50**|
||stack bowls|**100**|**100**|**100**|**100**|
||stick tape to box|40|20|**60**|10|
||sweep the rubbish|**80**|60|50|20|
||turn on faucet|**100**|70|**100**|**100**|
||**Overall**|**62.00**|51.00|51.67|42.67|


12 

Table 2 | Comparison with state-of-the-art open-source VLA generalist models on Table30 benchmark in RoboChallenge. List in success rate / score. **100/100** for highest score. The data is reported before 20260210. 

||||**Model**||
|---|---|---|---|---|
||**Benchmark**|DM0<br>2B|_𝜋_0.5<br>3B|_𝜋_0<br>3B|
|**UR5**|arrange fruits in basket<br>hang toothbrush cup<br>set the plates|**70/87.0**<br>**90/95.0**<br>60/62|0/9.0<br>50/71.0<br>40/49.5|0/11.5<br>20/62.0<br>**50/69.5**|
||shred scrap paper|**30/45.0**|20/36.0|20/27.0|
||sort books|0/8.5|0/24.0|**10/26.5**|
||stack color blocks|**100/100.0**|10/30.0|30/39.0|
|**Franka**|move objects into box<br>press three buttons|**50/64.5**<br>0/0.0|20/40.0<br>**0/4.0**|20/44.5<br>0/0.0|
||arrange flowers|**20/49.0**|0/30.5|0/13.5|
||arrange paper cups|**10/54.0**|0/31.0|0/15.0|
||fold dishcloth|**10/10.5**<br>|0/0.0<br>|0/0.0<br>|
||open the drawer|**90/95.0**|50/80.0|0/20.0|
||place shoes on rack|**100/98.5**|0/20.0|0/16.5|
|**ARX5**|put cup on coaster|**100/100.0**|70/63.0|0/0.0|
||search green boxes|**100/95.5**|0/3.0|0/0.0|
||sort electronic products|0/18.4|**0/22.5**|**0/22.5**|
||turn on light switch|**70/70.5**|10/25.0|20/29.0|
||water potted plant|**0/33.5**|0/0.0|0/0.0|
||wipe the table|**0/47.5**|10/28.0|0/29.0|
||clean dining table|0/12|**30/62.0**|0/25.5|
||make vegetarian sandwich|**0/15.0**|0/0.0|0/0.0|
||plug in network cable|**20/45.5**|0/0.0|0/0.0|
||pour fries into plate|**0/6.0**|0/0.0|0/0.0|
||put opener in drawer|10/10.0|**20/38.0**|0/0.0|
|**ALOHA**|put pen into pencil case<br>scan QR code|20/40.0<br>0/0|**50/63.5**<br>**0/7.0**|0/14.5<br>0/3.0|
||stack bowls|70/71|**80/83.0**|40/53.5|
||stick tape to box|0/14|**0/16.0**|0/0.0|
||sweep the rubbish|**30/40.0**|10/46.0|0/17.0|
||turn on faucet|**70/84.5**|60/56.0|60/67.5|
||**Overall**|**37.3/49.08**|17.67/31.27|9.0/20.22|


13 

VQA functionalities, including scene understanding, visual grounding, attribute recognition, and optical character recognition (OCR), as demonstrated in both embodied (Table 3) and lifestyle (Table 4) domains. As intended, the model is capable of predicting subtasks, detecting target objects, and forecasting trajectories and actions. Its chain-of-thought (CoT) reasoning performance is detailed in Table 5. Moreover, we observe that DM0 generalizes effectively to mobile contexts, indicating promising potential for deployment in mobile agent applications (Table 6). 

### **5. Discussion** 

#### **5.1. Conclusion** 

In this work, we presented DM0, a pioneering Embodied-Native Vision-Language-Action (VLA) framework that fundamentally rethinks the development of generalist robot policies. Deviating from the conventional paradigm of adapting internet-pretrained models via post-hoc finetuning, DM0 integrates physical grounding from the onset through a unified pretraining strategy on heterogeneous data sources—spanning web corpora, autonomous driving logs, and embodied trajectories.We introduced a comprehensive three-stage training pipeline (Pre-, Mid-, and Post-Training) underpinned by two key technical innovations: a hybrid gradient strategy that decouples action expert learning from VLM semantic preservation, and an Embodied Spatial Scaffolding mechanism that leverages spatial Chain-of-Thought (CoT) to rationalize complex physical tasks. Empirical results on the Table30 benchmark demonstrate that DM0 achieves state-of-the-art performance, surpassing strong baselines such as Spirit-v1.5 and _𝜋_ 0.5 in both Specialist and Generalist settings. These findings validate our core hypothesis: constructing VLA models with intrinsic, multi-source physical priors is a more effective path towards robust Physical AI than adapting purely semantic models. 

#### **5.2. Future Work** 

While DM0 establishes a strong baseline for Embodied-Native VLAs, several promising directions remain for future exploration: 

- **Scaling the Embodied-Native Paradigm:** Currently, DM0 operates as a lightweight model. We plan to investigate the scaling laws of the Embodied-Native framework by training on significantly larger datasets (e.g., combining simulation data with real-world logs) and increasing model parameter size (e.g., to 7B or 30B scales) to observe emergent physical reasoning capabilities. 

- **Expanding Multi-Modal Perception:** Physical interaction often requires cues beyond vision and text. Future iterations of DM0 will incorporate additional modalities such as tactile feedback, audio, and depth information directly into the unified pretraining stage, further enhancing the model’s fine-grained manipulation skills in occluded or dynamic environments. 

- **Long-Horizon Reasoning & World Models:** Although our Spatial Scaffolding improves reasoning, extremely long-horizon tasks remain a challenge. We aim to integrate World Model capabilities into the DM0 framework, allowing the agent to mentally simulate action consequences and plan over longer temporal horizons before execution. 

14 

### **References** 

- X. An, Y. Xie, K. Yang, W. Zhang, X. Zhao, Z. Cheng, Y. Wang, S. Xu, C. Chen, C. Wu, H. Tan, C. Li, J. Yang, J. Yu, X. Wang, B. Qin, Y. Wang, Z. Yan, Z. Feng, Z. Liu, B. Li, and J. Deng. Llava-onevision-1.5: Fully open framework for democratized multimodal training. In arXiv, 2025. 

- S. Bai, Y. Cai, R. Chen, K. Chen, X. Chen, Z. Cheng, L. Deng, W. Ding, C. Gao, C. Ge, W. Ge, Z. Guo, Q. Huang, J. Huang, F. Huang, B. Hui, S. Jiang, Z. Li, M. Li, M. Li, K. Li, Z. Lin, J. Lin, X. Liu, J. Liu, C. Liu, Y. Liu, D. Liu, S. Liu, D. Lu, R. Luo, C. Lv, R. Men, L. Meng, X. Ren, X. Ren, S. Song, Y. Sun, J. Tang, J. Tu, J. Wan, P. Wang, P. Wang, Q. Wang, Y. Wang, T. Xie, Y. Xu, H. Xu, J. Xu, Z. Yang, M. Yang, J. Yang, A. Yang, B. Yu, F. Zhang, H. Zhang, X. Zhang, B. Zheng, H. Zhong, J. Zhou, F. Zhou, J. Zhou, Y. Zhu, and K. Zhu. Qwen3-vl technical report. arXiv <u>preprint</u> arXiv:2511.21631, 2025. 

- A. Ben Abacha, S. A. Hasan, V. V. Datla, J. Liu, D. Demner-Fushman, and H. Müller. Vqa-med: Overview of the medical visual question answering task at imageclef 2019. In <u>Working</u> Notes of <u>CLEF</u> 2019, volume 2380 of <u>CEUR Workshop</u> Proceedings, Lugano, Switzerland, 2019. 

- K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, L. X. Shi, J. Tanner, Q. Vuong, A. Walling, H. Wang, and U. Zhilinsky. _𝜋_ 0: A vision-language-action flow model for general robot control. arXiv <u>preprint</u> arXiv:2410.24164, 2024. 

- K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. R. Equi, C. Finn, N. Fusai, M. Y. Galliker, et al. _𝜋_ 0.5: a vision-language-action model with open-world generalization. In <u>9th</u> Annual <u>Conference</u> on <u>Robot</u> Learning, 2025. 

- D. Bolya, P.-Y. Huang, P. Sun, J. H. Cho, A. Madotto, C. Wei, T. Ma, J. Zhi, J. Rajasegaran, H. Rasheed, J. Wang, M. Monteiro, H. Xu, S. Dong, N. Ravi, D. Li, P. Dollár, and C. Feichtenhofer. Perception encoder: The best visual embeddings are not at the output of the network. arXiv <u>preprint</u> arXiv:2504.13181, 2025. URL `https://arxiv.org/abs/2504.13181` . 

- Q. Bu, J. Cai, L. Chen, X. Cui, Y. Ding, S. Feng, S. Gao, X. He, X. Huang, S. Jiang, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. arXiv <u>preprint</u> arXiv:2503.06669, 2025. 

- M. Byeon, B. Park, H. Kim, S. Lee, W. Baek, and S. Kim. Coyo-700m: Image-text pair dataset. `https://github.com/kakaobrain/coyo-dataset` , 2022. 

- M. Chai, Z. Shen, C. Zhang, Y. Zhang, X. Wang, S. Dou, J. Kang, J. Zhang, and Q. Zhang. Docfusion: A unified framework for document parsing tasks. arXiv <u>preprint</u> arXiv:2412.12505, 2025. 

- T. Chen, Z. Chen, B. Chen, Z. Cai, Y. Liu, Z. Li, Q. Liang, X. Lin, Y. Ge, Z. Gu, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. arXiv <u>preprint</u> arXiv:2506.18088, 2025. 

- C. Cui, T. Sun, M. Lin, T. Gao, Y. Zhang, J. Liu, X. Wang, Z. Zhang, C. Zhou, H. Liu, et al. Paddleocr 3.0 technical report. arXiv <u>preprint</u> arXiv:2507.05595, 2025. 

DeepSeek-AI. Deepseek-v3 technical report, 2024. URL `https://arxiv.org/abs/2412.19437` . 

15 

- M. Deitke, C. Clark, S. Lee, A. Tripathi, Y. Yang, J. Park, M. Salehi, N. Muennighoff, K. Lo, L. Soldaini, et al. Molmo and pixmo: Open weights and open data for state-of-the-art visionlanguage models. arXiv <u>preprint</u> arXiv:2409.17146, 2024. 

- D. Driess, J. T. Springenberg, B. Ichter, L. Yu, A. Li-Bell, K. Pertsch, A. Z. Ren, H. Walke, Q. Vuong, L. X. Shi, and S. Levine. Knowledge insulating vision-language-action models: Train fast, run fast, generalize better. arXiv <u>preprint</u> arXiv:2505.23705, 2025. 

- GigaAI. Gigabrain-0: A world model-powered vision-language-action model. 2025. URL `https: //arxiv.org/abs/2510.19430` . 

- X. He, Y. Zhang, L. Mou, E. Xing, and P. Xie. Pathvqa: 30000+ questions for medical visual question answering. arXiv <u>preprint</u> arXiv:2003.10286, 2020. 

- A. Huang, C. Yao, C. Han, F. Wan, H. Guo, H. Lv, H. Zhou, J. Wang, J. Zhou, J. Sun, J. Hu, K. Lin, L. Zhao, M. Huang, S. Yuan, W. Qu, X. Wang, Y. Lai, Y. Zhao, Y. Zhang, Y. Shi, Y. Chen, Z. Weng, Z. Meng, A. Li, A. Kong, B. Dong, C. Wan, D. Wang, D. Qi, D. Li, E. Yu, G. Li, H. Yin, H. Zhou, H. Zhang, H. Yan, H. Zhou, H. Peng, J. Zhang, J. Lv, J. Fu, J. Cheng, J. Zhou, J. Yin, J. Xie, J. Wu, J. Zhang, J. Liu, K. Tan, K. Yan, L. Chen, L. Chen, M. Li, Q. Zhao, Q. Sun, S. Pang, S. Fan, S. Shang, S. Zhang, T. You, W. Ji, W. Xie, X. Yang, X. Hou, X. Jiao, X. Ren, X. Kong, X. Huang, X. Wu, X. Chen, X. Wang, X. Zhang, Y. Wei, Y. Li, Y. Xu, Y. Shen, Y. Peng, Y. Peng, Y. Zhou, Y. Li, Y. Yang, Y. Zhang, Z. Xie, Z. Huang, Z. Lu, Z. Fan, Z. Cheng, D. Jiang, Q. Han, X. Zhang, Y. Zhu, and Z. Ge. Step3-vl-10b technical report, 2026. URL `https://arxiv.org/abs/2601.09668` . 

- J. Jones, O. Mees, C. Sferrazza, K. Stachowicz, P. Abbeel, and S. Levine. Beyond sight: Finetuning generalist robot policies with heterogeneous sensors via language grounding. arXiv <u>preprint</u> arXiv:2501.04693, 2025. 

Kaggle. Fsc dataset. URL `https://www.kaggle.com/datasets/xuncngng/fsc147-0` . 

- G. Kim, T. Hong, M. Yim, J. Nam, J. Park, W. Yim, S. Hwang, S. Yun, D. Han, and S. Park. Ocr-free document understanding transformer. In European <u>Conference</u> on <u>Computer Vision (ECCV),</u> 2022. 

- M. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn. Openvla: An open-source vision-language-action model. arXiv <u>preprint</u> arXiv:2406.09246, 2024. 

- A. Kuznetsova, H. Rom, N. Alldrin, J. Uijlings, I. Krasin, J. Pont-Tuset, S. Kamali, S. Popov, M. Malloci, A. Kolesnikov, et al. The open images dataset v4: Unified image classification, object detection, and visual relationship detection at scale. International <u>journal</u> of computer vision, 128(7):1956–1981, 2020. 

- H. Laurençon, L. Tronchon, and V. Sanh. Unlocking the conversion of web screenshots into html code with the websight dataset. arXiv <u>preprint,</u> 2024. 

- J. Li, D. Li, C. Xiong, and S. Hoi. Blip: Bootstrapping language-image pre-training for unified vision-language understanding and generation. In International conference on machine learning, pages 12888–12900. PMLR, 2022. 

- Q. Li, Y. Liang, Z. Wang, L. Luo, X. Chen, M. Liao, F. Wei, Y. Deng, S. Xu, Y. Zhang, et al. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. arXiv <u>preprint</u> arXiv:2411.19650, 2024. 

16 

- T.-Y. Lin, M. Maire, S. Belongie, J. Hays, P. Perona, D. Ramanan, P. Dollár, and C. L. Zitnick. Microsoft coco: Common objects in context. In European conference on computer vision, pages 740–755. Springer, 2014. 

- Y. Lipman, R. T. Q. Chen, H. Ben-Hamu, M. Nickel, and M. Le. Flow matching for generative modeling. arXiv <u>preprint</u> arXiv:2210.02747, 2022. URL `https://arxiv.org/abs/2210.027 47` . 

- B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. arXiv <u>preprint</u> arXiv:2306.03310, 2023. 

- C. Liu, H. Wei, J. Chen, L. Kong, Z. Ge, Z. Zhu, L. Zhao, J. Sun, C. Han, and X. Zhang. Focus anywhere for fine-grained multi-page document understanding. arXiv <u>preprint</u> arXiv:2405.14295, 2024. 

- X. Liu, W. Wang, Y. Yuan, J. Huang, Q. Liu, P. He, and Z. Tu. Insight over sight: Exploring the vision-knowledge conflicts in multimodal llms. arXiv <u>preprint</u> arXiv:2410.08145, 2025. 

- I. Loshchilov and F. Hutter. Decoupled weight decay regularization. arXiv <u>preprint</u> arXiv:1711.05101, 2017. 

- NVIDIA, J. Bjorck, N. C. Fernando Castañeda, X. Da, R. Ding, L. J. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, J. Jang, Z. Jiang, J. Kautz, K. Kundalia, L. Lao, Z. Li, Z. Lin, K. Lin, G. Liu, E. Llontop, L. Magne, A. Mandlekar, A. Narayan, S. Nasiriany, S. Reed, Y. L. Tan, G. Wang, Z. Wang, J. Wang, Q. Wang, J. Xiang, Y. Xie, Y. Xu, Z. Xu, S. Ye, Z. Yu, A. Zhang, H. Zhang, Y. Zhao, R. Zheng, and Y. Zhu. GR00T N1: An open foundation model for generalist humanoid robots. In ArXiv Preprint, March 2025. 

SakiRinn. Locount. URL `https://github.com/SakiRinn/mmdetection-locount` . 

- C. Schuhmann, R. Beaumont, R. Vencu, C. Gordon, R. Wightman, M. Cherti, T. Coombes, A. Katta, C. Mullis, M. Wortsman, et al. Laion-5b: An open large-scale dataset for training next generation image-text models. Advances in neural information <u>processing</u> systems, 35: 25278–25294, 2022. 

- H. Shi, B. Xie, Y. Liu, L. Sun, F. Liu, T. Wang, E. Zhou, H. Fan, X. Zhang, and G. Huang. Memoryvla: Perceptual-cognitive memory in vision-language-action models for robotic manipulation. arXiv <u>preprint</u> arXiv:2508.19236, 2025. 

- Sujet AI. Sujet-finance-qa-vision-100k: A large-scale dataset for financial document vqa, 2024. URL `https://huggingface.co/datasets/sujet-ai/Sujet-Finance-QA-Vision-100k` . 

- L. Sun, B. Xie, Y. Liu, H. Shi, T. Wang, and J. Cao. Geovla: Empowering 3d representations in vision-language-action models. arXiv <u>preprint</u> arXiv:2508.09071, 2025. 

- G. Team. Galaxea g0: Open-world dataset and dual-system vla model. arXiv <u>preprint</u> arXiv:2509.00576v1, 2025a. 

- G. Team, A. Kamath, J. Ferret, S. Pathak, N. Vieillard, R. Merhej, S. Perrin, T. Matejovicova, A. Ramé, M. Rivière, L. Rouillard, T. Mesnard, G. Cideron, J. bastien Grill, S. Ramos, E. Yvinec, M. Casbon, E. Pot, I. Penchev, G. Liu, F. Visin, K. Kenealy, L. Beyer, X. Zhai, A. Tsitsulin, R. Busa-Fekete, A. Feng, N. Sachdeva, B. Coleman, Y. Gao, B. Mustafa, I. Barr, E. Parisotto, D. Tian, M. Eyal, C. Cherry, J.-T. Peter, D. Sinopalnikov, S. Bhupatiraju, R. Agarwal, M. Kazemi, D. Malkin, R. Kumar, D. Vilar, I. Brusilovsky, J. Luo, A. Steiner, 

17 

   - A. Friesen, A. Sharma, A. Sharma, A. M. Gilady, A. Goedeckemeyer, A. Saade, A. Feng, A. Kolesnikov, A. Bendebury, A. Abdagic, A. Vadi, A. György, A. S. Pinto, A. Das, A. Bapna, A. Miech, A. Yang, A. Paterson, A. Shenoy, A. Chakrabarti, B. Piot, B. Wu, B. Shahriari, B. Petrini, C. Chen, C. L. Lan, C. A. Choquette-Choo, C. Carey, C. Brick, D. Deutsch, D. Eisenbud, D. Cattle, D. Cheng, D. Paparas, D. S. Sreepathihalli, D. Reid, D. Tran, D. Zelle, E. Noland, E. Huizenga, E. Kharitonov, F. Liu, G. Amirkhanyan, G. Cameron, H. Hashemi, H. Klimczak-Plucińska, H. Singh, H. Mehta, H. T. Lehri, H. Hazimeh, I. Ballantyne, I. Szpektor, I. Nardini, J. Pouget-Abadie, J. Chan, J. Stanton, J. Wieting, J. Lai, J. Orbay, J. Fernandez, J. Newlan, J. yeong Ji, J. Singh, K. Black, K. Yu, K. Hui, K. Vodrahalli, K. Greff, L. Qiu, M. Valentine, M. Coelho, M. Ritter, M. Hoffman, M. Watson, M. Chaturvedi, M. Moynihan, M. Ma, N. Babar, N. Noy, N. Byrd, N. Roy, N. Momchev, N. Chauhan, N. Sachdeva, O. Bunyan, P. Botarda, P. Caron, P. K. Rubenstein, P. Culliton, P. Schmid, P. G. Sessa, P. Xu, P. Stanczyk, P. Tafti, R. Shivanna, R. Wu, R. Pan, R. Rokni, R. Willoughby, R. Vallu, R. Mullins, S. Jerome, S. Smoot, S. Girgin, S. Iqbal, S. Reddy, S. Sheth, S. Põder, S. Bhatnagar, S. R. Panyam, S. Eiger, S. Zhang, T. Liu, T. Yacovone, T. Liechty, U. Kalra, U. Evci, V. Misra, V. Roseberry, V. Feinberg, V. Kolesnikov, W. Han, W. Kwon, X. Chen, Y. Chow, Y. Zhu, Z. Wei, Z. Egyed, V. Cotruta, M. Giang, P. Kirk, A. Rao, K. Black, N. Babar, J. Lo, E. Moreira, L. G. Martins, O. Sanseviero, L. Gonzalez, Z. Gleicher, T. Warkentin, V. Mirrokni, E. Senter, E. Collins, J. Barral, Z. Ghahramani, R. Hadsell, Y. Matias, D. Sculley, S. Petrov, N. Fiedel, N. Shazeer, O. Vinyals, J. Dean, D. Hassabis, K. Kavukcuoglu, C. Farabet, E. Buchatskaya, J.-B. Alayrac, R. Anil, Dmitry, Lepikhin, S. Borgeaud, O. Bachem, A. Joulin, A. Andreev, C. Hardin, R. Dadashi, and L. Hussenot. Gemma 3 technical report, 2025. 

- R. Team. Robochallenge: Large-scale real-robot evaluation of embodied policies, 2025b. URL `https://robochallenge.cn/robochallenge_techreport.pdf` . 

- S. A. Team. Spirit-v1.5: Clean data is the enemy of great robot foundation models. <u>Spirit</u> AI Blog, 2026. https://www.spirit-ai.com/en/blog/spirit-v1-5. 

- S. Tong, E. Brown, P. Wu, S. Woo, M. Middepogu, S. C. Akula, J. Yang, S. Yang, A. Iyer, X. Pan, A. Wang, R. Fergus, Y. LeCun, and S. Xie. Cambrian-1: A fully open, vision-centric exploration of multimodal llms, 2024. 

- H. Touvron, T. Lavril, G. Izacard, X. Martinet, M.-A. Lachaux, T. Lacroix, B. Rozière, N. Goyal, E. Hambro, F. Azhar, et al. Llama: Open and efficient foundation language models. arXiv <u>preprint</u> arXiv:2302.13971, 2023. 

- Q. Vuong, S. Levine, H. R. Walke, K. Pertsch, A. Singh, R. Doshi, C. Xu, J. Luo, L. Tan, D. Shah, et al. Open x-embodiment: Robotic learning datasets and rt-x models. In Towards <u>Generalist Robots:</u> Learning Paradigms for <u>Scalable Skill</u> Acquisition@ <u>CoRL2023,</u> 2023. 

- B. Wang, C. Xu, X. Zhao, L. Ouyang, F. Wu, Z. Zhao, R. Xu, K. Liu, Y. Qu, F. Shang, et al. Mineru: An open-source solution for precise document content extraction. arXiv <u>preprint</u> arXiv:2409.18839, 2024. 

- Y. Wen, H. Li, K. Gu, Y. Zhao, T. Wang, and X. Sun. Llada-vla: Vision language diffusion action models. arXiv <u>preprint</u> arXiv:2509.06932, 2025. 

- K. Wu, C. Hou, J. Liu, Z. Che, X. Ju, Z. Yang, M. Li, Y. Zhao, Z. Xu, G. Yang, et al. Robomind: Benchmark on multi-embodiment intelligence normative data for robot manipulation. In <u>Robotics: Science</u> and <u>Systems (RSS)</u> 2025. Robotics: Science and Systems Foundation, 2025. URL `https://www.roboticsproceedings.org/rss21/p152.pdf` . 

18 

- B. Xie, E. Zhou, F. Jia, H. Shi, H. Fan, H. Zhang, H. Li, J. Sun, J. Bin, J. Huang, et al. Dexbotic: Open-source vision-language-action toolbox. arXiv <u>preprint</u> arXiv:2510.23511, 2025. 

- C. Xie, H. Cai, J. Li, F. Kong, X. Wu, J. Song, H. Morimitsu, L. Yao, D. Wang, X. Zhang, et al. Ccmb: A large-scale chinese cross-modal benchmark. In Proceedings of the <u>31st</u> ACM International <u>Conference</u> on Multimedia, pages 4219–4227, 2023. 

- H. Yan, J. Wang, X. Huang, Y. Shen, Z. Meng, Z. Fan, K. Tan, J. Gao, L. Shi, M. Yang, et al. Step-gui technical report. arXiv <u>preprint</u> arXiv:2512.15431, 2025. 

- A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv, C. Zheng, D. Liu, F. Zhou, F. Huang, F. Hu, H. Ge, H. Wei, H. Lin, J. Tang, J. Zhang, J. Tu, J. Zhang, J. Yang, J. Yang, J. Zhou, J. Zhou, J. Lin, K. Dang, K. Bao, K. Yang, L. Yu, L. Deng, M. Li, M. Xue, M. Li, P. Zhang, P. Wang, Q. Zhu, R. Men, R. Gao, S. Liu, S. Luo, T. Li, T. Tang, W. Yin, X. Ren, X. Wang, X. Zhang, X. Ren, Y. Fan, Y. Su, Y. Zhang, Y. Zhang, Y. Wan, Y. Liu, Z. Wang, Z. Cui, Z. Zhang, Z. Zhou, and Z. Qiu. Qwen3 technical report. arXiv <u>preprint</u> arXiv:2505.09388, 2025a. URL `https://arxiv.org/abs/2505.09388` . 

- Y. Yang, A. Patel, M. Deitke, T. Gupta, L. Weihs, A. Head, M. Yatskar, C. Callison-Burch, R. Krishna, A. Kembhavi, and C. Clark. Scaling text-rich image understanding via codeguided synthetic multimodal data generation. arXiv <u>preprint</u> arXiv:2502.14846, 2025b. 

- E. Yu, L. Zhao, Y. Wei, J. Yang, D. Wu, L. Kong, H. Wei, T. Wang, Z. Ge, X. Zhang, et al. Merlin: Empowering multimodal llms with foresight minds. In European <u>Conference</u> on <u>Computer Vision,</u> pages 425–443. Springer, 2024. 

- E. Yu, K. Lin, L. Zhao, Y. Wei, Z. Zhu, H. Wei, J. Sun, Z. Ge, X. Zhang, T. Wang, et al. Unhackable temporal rewarding for scalable video mllms. arXiv <u>preprint</u> arXiv:2502.12081, 2025. 

- Y. Yuan, X. Liu, W. Dikubab, H. Liu, Z. Ji, Z. Wu, and X. Bai. Syntax-aware network for handwritten mathematical expression recognition. arXiv <u>preprint</u> arXiv:2203.01601, 2022. 

- R. Zellers, Y. Bisk, A. Farhadi, and Y. Choi. From recognition to cognition: Visual commonsense reasoning. arXiv <u>preprint</u> arXiv:1811.10830, 2019. 

- C. Zhang, J. Wang, Z. Gao, Y. Su, T. Dai, C. Zhou, J. Lu, and Y. Tang. Clap: Contrastive latent action pretraining for learning vision-language-action models from human videos. arXiv <u>preprint</u> arXiv:2601.04061, 2026. URL `https://arxiv.org/abs/2601.04061` . 

- B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In <u>Conference</u> on <u>Robot</u> Learning, pages 2165–2183. PMLR, 2023. 

19 

### **6. Author List** 

All authors are listed alphabetically by their first names. 

**Pretraining & Mid-training & Post-training:** En Yu, Haoran Lv, Jianjian Sun, Kangheng Lin, Ruitao Zhang, Yukang Shi, Yuyang Chen, Ze Chen, Ziheng Zhang 

**Supervised Fine-tuning:** Fan Jia, Kaixin Liu, Meng Zhang, Ruitao Hao, Saike Huang, Songhan Xie, Yu Liu, Zhao Wu 

**Reinforcement Learning:** Bin Xie, Pengwei Zhang, Qi Yang, Xianchi Deng, Yunfei Wei 

**Data Collection & Process:** Enwen Zhang, Hongyang Peng, Jie Zhao, Kai Liu, Wei Sun, Yajun Wei, Yi Yang, Yunqiao Zhang, Ziwei Yan 

**Evaluation:** Enwen Zhang, Haitao Yang, Hao Liu, Haoqiang Fan, Haowei Zhang, Junwen Huang, Kai Liu, Yang Chen, Yunchao Ma, Yunhuan Yang, Zhengyuan Du, Ziming Liu 

**Infrastructure:** Jiahui Niu, Yucheng Zhao 

**Sponsors:** Daxin Jiang, Wenbin Tang, Xiangyu Zhang, Zheng Ge 

**Project Lead:** Erjin Zhou, Tiancai Wang 

20 

#### **Image** 


#### **QAs** 

**Q:** What type is the rack? **A:** wooden rack. 

**Q:** How many bowls in the image? **A:** 4. 

**Q:** What is the object that the robot arm is grasping? **A:** Cup. 

**Q:** Describe the image. **A:** The scene depicts a white table with various items scattered across its surface. The items include a red toothpaste tube, a red box, a black trash can, a clear plastic container, a white box, a black marker, a blue marker, a pink cup, a yellow marker, a red marker, a white marker, a black eraser, and a small white box. 

**Q:** Describe the content of image. **A:** The image shows a pair of robotic arms positioned on a white table, gripping the handles of a blue fabric. To the left, a gray bag contains red fabric. An orange folded item rests on the table to the right. 

**Q:** What is the color of clothes in the right box? **A:** clothes in the right box are blue. 

**Q:** What is the color of clothes in the middle box? 

**A:** clothes in the middle box are black. 

Table 3 | DM0 retains fundamental VQA capabilities such as scene description, object detection, and attribute recognition in embodied scenarios. 

21 

#### **Image** 


#### **QAs** 

#### **Q:** Describe the image. 

**A:** The image shows a dog with a light brown coat, sitting and smiling at the camera. The dog’s eyes are open and its mouth is slightly open, revealing a pink tongue. The background is blurred, but it appears to be a indoor setting with a white wall and a white floor. The dog’s ears are slightly pointed, and its face is clean and wellgroomed. The overall mood of the image is cheerful and friendly. 

**Q:** What is the name of this book? 

**A:** The name of the book is ”Algebra” by Serge Lang. 

**Q:** What color is the word ”Algebra”? 

**A:** The word ”Algebra” is black. 

#### **Q:** Descibe the image. 


**A:** The image captures a bustling city street, teeming with life and activity. The street, marked with a crosswalk, serves as the main focus of the image. It’s lined with tall buildings, their glass facades reflecting the overcast sky above. The buildings vary in height and design, creating a dynamic skyline that adds depth to the scene. A few cars are visible on the street, their presence adding a sense of movement and life to the image. People can be seen walking on the sidewalk, going about their day, their figures small against the backdrop of the cityscape. The sky above is filled with clouds, casting a soft light over the scene. Despite the overcast conditions, the image exudes a sense of energy and vibrancy, characteristic of a busy city street. 

Table 4 | DM0 retains fundamental VQA capabilities such as scene description, OCR in general scenarios. 

22 

#### **Image** 


#### **QAs** 

**Q:** Please decompose the specified high-level goal ’organize toys’ into its constituent subtasks. **A:** Pick up the toy car from the ground with your right hand and place it into the storage box. 

**Q:** Please identify the initial subtask required to achieve the following objective: open and close microwave oven. **A:** Place the plate from the microwave back on the right side of the table with your right hand. 

**Q:** Please identify the specific subtask required to achieve the following goal: lift the steamer lid. **A:** Pick up the second steamer lid from the right with your left hand and place it on the third steamer from the right. 

**Q:** In order to complete the instruction ’fold clothes’, please identify the necessary subtask plan. **A:** The current subtask is determined to be: Fold the red T-shirt on the bed neatly with both hands. 

Table 5 | DM0 possesses Chain-of-Thought (CoT) capability for predicting subtasks within embodied scenarios. 

23 


**Q:** I want to order my dinner, which **QAs** button should I press? 

**A:** Press the 外卖 button. 


**Q:** I want to check which games are in discounts, which button should I press? 

**A:** To check which games are in discounts, press the ”More” button located at the top right corner of the ”Discounts & Events” section. 

Table 6 | DM0 also demonstrates potential for supporting mobile agents. 

24 

