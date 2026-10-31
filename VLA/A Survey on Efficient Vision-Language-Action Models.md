---
title: "A Survey on Efficient Vision-Language-Action Models"
date: "2025-10-27"
authors: "Zhaoshu Yu; Bo Wang; Pengpeng Zeng; Haonan Zhang; Ji Zhang; Zheng Wang"
url: https://arxiv.org/abs/2510.24795
pdf: https://arxiv.org/pdf/2510.24795
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2510.24795)** / [論文ページ](https://arxiv.org/abs/2510.24795)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

1 

# A Survey on Efficient Vision-Language-Action Models 

Zhaoshu Yu, Bo Wang, Pengpeng Zeng, Haonan Zhang, Ji Zhang, Zheng Wang, Lianli Gao, Jingkuan Song, Nicu Sebe, and Heng Tao Shen, _IEEE Fellow_ 

**Abstract** —Vision-Language-Action models (VLAs) represent a significant frontier in embodied intelligence, aiming to bridge digital knowledge with physical-world interaction. Despite their remarkable performance, foundational VLAs are hindered by the prohibitive computational and data demands inherent to their large-scale architectures. To this end, recent studies improve VLA efficiency from different views, _e.g.,_ real-time inference, training computation, and scalable data collection. However, these efforts are mostly studied separately. A unified view is still missing for understanding how efficiency should be optimized across the full VLA lifecycle. To bridge this gap, this survey presents the first comprehensive review of Efficient Vision-Language-Action models ( **Efficient VLAs** ) across the entire model-training-data pipeline. Specifically, we introduce a unified taxonomy to systematically organize the disparate efforts in this domain, categorizing current techniques into three core pillars: _(1) Efficient Model Design_ , focusing on efficient architectures and model compression; _(2) Efficient Training_ , which reduces computational burdens during model learning; and _(3) Efficient Data Collection_ , which addresses the bottlenecks in acquiring and utilizing robotic data. Through a critical review of state-of-the-art methods within this framework, this survey provides an organized reference for the community and summarizes representative applications, delineates key challenges, and charts a roadmap for future research. We maintain a continuously updated project page to track our latest developments: https://evla-survey.github.io/. 

**Index Terms** —Vision-Language-Action Models, Efficient VLAs, Embodied AI, Robotic Manipulation 

✦ 

## **1 INTRODUCTION** 

V [ISION4]4]] signify-LANGUAGEaa breakthrough-ACTIONin Models (VLAs) [thein Models (VLAs) [thethe evolution of1], [artificial2], [3],artificial2], [3], 

[ISION4]4]] signify-LANGUAGEaa breakthrough-ACTIONin Models (VLAs) [thein Models (VLAs) [thethe evolution of1], [artificial2], [3],artificial2], [3], intelligence, endowing interactive physical entities with the capacity for perception and decision-making. These models ground the semantic reasoning of Large Language Models (LLMs) and the cross-modal perception of Vision-Language Models (VLMs) into action spaces and show strong dexterity and generalization in complex environments. The potential of this paradigm is already manifest across diverse highstakes domains, ranging from the real-time interaction in autonomous driving [5], [6] and industrial manufacturing [7] to the high-precision requirements of medical robotics [8] and laboratory automation [9]. 

Recent VLA research is organized around three technical axes: architecture design, training procedures, and data curation. Architectural research focuses on coupling multimodal backbones [10], [11] with diverse action decoders to facilitate end-to-end mapping from perception to execution, spanning autoregressive policies [1] for se- 


Fig. 1: **The transition from foundational VLAs to efficient VLAs.** Foundational VLAs are bottlenecked by real-time incompatibility, excessive computational costs, and inefficient data collection. To enable deployment on edge devices, Efficient VLAs navigate a design space characterized by diverse trade-offs across three core pillars. By strategically balancing these competing objectives, different methods achieve low latency, rapid adaptation, and high reliability across diverse edge device implementations. 

_This study is supported by grant from the Fundamental and Interdisciplinary Disciplines Breakthrough Plan of the Ministry of Education of China (Grant No. JYB2025XDXM116)._ 

- _Zhaoshu Yu, Bo Wang, Pengpeng Zeng, Haonan Zhang, Zheng Wang, and Heng Tao Shen are with the School of Computer Science and Technology, Tongji University, China._ 

- _Ji Zhang is with the School of Computing and Artificial Intelligence, Southwest Jiaotong University, China._ 

- _Lianli Gao is with the School of Computer Science and Engineering, University of Electronic Science and Technology of China, China._ 

- _Jingkuan Song is with the School of Computer Science and Technology, Tongji University, China, and Shanghai Innovation Institute, China._ 

- _• Nicu Sebe is with the Department of Information Engineering and Computer Science, University of Trento, Italy._ 

- _Corresponding author: Pengpeng Zeng. (is.pengpengzeng@gmail.com)_ 

quential prediction to diffusion-based generators [2] for trajectory synthesis. Training methodologies have evolved toward large-scale cross-embodiment pre-training on heterogeneous datasets [12], progressively integrating reinforcement learning [13] and supervised fine-tuning [14] to improve downstream adaptation. Meanwhile, data-centric strategies prioritize high-fidelity trajectories through expert demonstrations [15], realistic simulation [16], and generative augmentation [17] to improve transfer across diverse tasks. These multi-dimensional advancements constitute a cohesive research ecosystem that continually pushes the frontiers 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

2 


Fig. 2: **The organization of our survey.** We systematically categorize efficient VLAs into three core pillars: (1) **Efficient Model Design** , encompassing efficient architectures and model compression techniques, (2) **Efficient Training** , covering efficient pre-training and post-training strategies, and (3) **Efficient Data Collection** , including efficient data collection and augmentation methods. The framework also reviews VLA foundations and key applications. 

### of autonomous agency in the physical world. 

Although these models show strong generalist behavior, foundational VLAs inherit large computational and data footprints from scaling-centric LLM and VLM backbones, which often conflict with latency and power budgets on physical platforms. This mismatch complicates realtime edge deployment on robotic manipulators and mobile agents, and appears through three bottlenecks: (1) **RealTime Incompatibility** : current VLAs suffer from high inference latency and insufficient control frequency [1], making them incompatible with the sub-second control cycles required for responsive and adaptive robotic manipulation; (2) **Excessive Computational Cost** : the pre-training requirements are prohibitively large, as exemplified by OpenVLA [1] consuming 21,500 A100-GPU hours on a 64-GPU cluster, posing significant barriers to reproducibility and scalability; and (3) **Inefficient Data Collection** : The reliance on large-scale datasets, with examples like _π_ 0 [2] requiring over 10,000 hours of robotic trajectories, results in a timeconsuming and labor-intensive data collection pipeline that severely limits the applicability of such approaches. 

To address these challenges, we introduce the **Efficient VLA** paradigm. An efficient VLA is not merely a compact model, but a resource-aware embodied system jointly optimized across model design, training, and data collection. It aims to reduce resource cost and inference latency while preserving real-world embodied capability. As illustrated in Fig. 1, rather than isolated optimizations, these designs [14], [18], [19], [20], [21], [22] navigate a co-dependent space of trade-offs across the three pillars. By forming a synergistic, closed-loop ecosystem, they narrow the gap between heavyweight foundations and edge deployment, targeting high-frequency control under constrained robotic 

### platforms. 

The overarching goal of this survey is to provide a comprehensive view of the technological advances in efficient VLAs. As illustrated in Fig. 2, we organize the literature in a taxonomy comprising three main categories: (1) **Efficient Model Design** : encompassing innovative strategies to optimize the architectural and inference efficiency of VLAs. This includes _Efficient Architectures_ , which offers innovative structural optimizations alongside scalable frameworks, and _Model Compression_ , which involves techniques to compress model parameters and refine token handling. (2) **Efficient Training** : incorporating advanced approaches to reduce the computational and data burdens during VLAs training, containing _Efficient Pre-training/Post-training_ . The former improves efficiency through optimized data and action modeling, while the latter enhances adaptability and performance via customized learning strategies, _e.g.,_ supervised finetuning and reinforcement learning. (3) **Efficient Data Collection** : focusing on cutting-edge methods to improve data collection and enrichment for VLAs development, using interactive, simulated, reusable, and self-driven strategies to make dataset acquisition more scalable and efficient. Through this exploration, we provide a comprehensive understanding of the current state of efficient VLAs, thereby highlighting key challenges and advancements in embodied intelligence and robotic learning. 

While existing literature provides extensive reviews of the general VLA landscape, ranging from architectural overviews [23], [24], [25] and VLM-driven advancements [26] to specific mechanisms such as action tokenization [27] and motor learning [28], these surveys primarily focus on conventional, performance-oriented paradigms. To address their fragmented treatment of efficiency and the 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

3 

lack of a unified taxonomy, this paper presents the first systematic review of efficient VLAs, synthesizing model design, training, and data collection strategies to advance scalable embodied AI. Through this comprehensive synthesis, we bridge the gap between theoretical development and real-world deployment in resource-constrained scenarios. Accompanied by a dedicated GitHub repository, this survey is designed to serve as both a valuable reference for navigating the literature and a foundation for inspiring future innovations. 

The primary contributions of this survey are summarized as follows: 

- **Pioneering Survey:** To the best of our knowledge, this work presents the first comprehensive survey specifically dedicated to the realm of efficient VLAs that covers the entire “model-training-data” process. It fills a critical gap in the literature and aims to establish an organized reference for the research community. 

- **Novel Taxonomy:** We introduce a novel and systematically structured taxonomy that organizes the core technical landscape for building efficient VLAs into three interconnected pillars: Efficient Model Design, Efficient Training, and Efficient Data Collection. 

- **Future Roadmap:** We critically distill the key challenges and current limitations plaguing the field, thereby outlining promising and forward-looking research directions to inspire and guide future endeavors in scalable embodied intelligence. 

The remaining sections of this survey are organized as illustrated in Fig. 2. We begin in Sec. 2 by introducing the foundational concepts of VLAs, delineating the computational challenges that necessitate the pursuit of efficiency. Sec. 3 delves into efficient model design, systematically categorizing techniques that span efficient architectural innovations and model compression. Sec. 4 investigates efficient training paradigms, encompassing strategies to reduce the computational overhead and dataset demands during both pre-training and post-training stages. Sec. 5 examines the crucial role of efficient data collection, exploring methodologies for scalable data collection and effective augmentation to maximize data utility. We then survey key applications in Sec. 6 where efficient VLAs have demonstrated significant potential, highlighting their practical utility in real-world scenarios. Finally, Sec. 7 summarizes the survey. 

## **2 VISION-LANGUAGE-ACTION MODELS** 

In this section, we first review the basic VLA pipeline and identify the key efficiency bottlenecks behind resourceaware VLA design. We then present the taxonomy principle and highlight the unique positioning of this survey as the first systematic review of efficient VLAs in embodied AI. 

### **2.1 An Overview of VLAs** 

### _2.1.1 Foundational Pipeline_ 

As depicted in Fig. 3, VLAs’ foundational pipeline divides multimodal inference into three synergistic modules: a vision encoder that processes scene images into patch embeddings, a LLM backbone augmented for vision-language 


Fig. 3: **An overview of VLAs.** VLAs integrate vision encoders to extract visual features, LLM backbones to fuse multimodal inputs, and action decoders (autoregressive or generative) to produce robotic control signals, enabling endto-end vision-language-action reasoning for embodied manipulation tasks. 

fusion that orchestrates high-level reasoning, and an action decoder that yields precise control trajectories. Pre-trained components allow these pipelines to inherit visual-language priors before adaptation to embodied action generation. **Vision Encoder.** At the ingress, the vision encoder _Eimg_ ( _·_ ) ingests RGB observations and extracts their hierarchical features. Prevailing choices include vision transformers like ViT [29], SigLIP [30], DINOv2 [31], and CLIP [32], whose contrastive or self-supervised pre-training on vast corpora imparts zero-shot versatility. Abstractly, this module maps raw imagery to semantic tokens: 


where _I ∈_ R<sup>_H×W ×_3</sup> denotes the input images, **v** _∈_ R<sup>_Nv×Dv_</sup> represents the vision tokens, and _θimg_ indicates the encoder parameters. 

**LLM Backbone.** After a projector _P_ ( _·_ ) that ensures seamless alignment and mitigates modality gaps, the multimodal sequence then feeds into the LLM backbone _LLM_ ( _·_ )—the center for semantic reasoning. Spanning Qwen [33], PaLM [34], Gemma [35], Llama [36], and Mamba [37], pre-trained LLMs process the fused embeddings for task planning, which can be formulated as follows: 


where **l** _∈_ R<sup>_Nl×Dl_</sup> is language tokens, **h** _∈_ R<sup>_Nh×D_</sup> denotes the hidden states and _θLLM_ represents the LLM parameters. **Action Decoder.** Culminating the flow, the action decoder transmutes latents into robot-ready outputs, such as endeffector poses and gripper commands. Common instantiations include diffusion/flow matching [38], [39], [40] for stochastic refinement of trajectories and autoregressive decoding for sequential action prediction. They all generate action sequences conditioned on reasoning: 


where **a** 1: _T ∈_ R<sup>_T ×Da_</sup> denotes the action chunk over _T_ timesteps and _θact_ indicates the decoder parameters. 

Overall, this tripartite architecture couples perception, language-conditioned reasoning, and action prediction within an end-to-end policy pipeline. 

### _2.1.2 Training Recipes_ 

Following the practice of LLMs and VLMs, VLAs are typically trained in two stages: pre-training and post-training. In 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

4 

|**Efficient VLAs**|**SARA-RT**|**RoboMamba**<br>**TinyVLA**<br>**RoboDual**<br>**LAPA**<br>**DP-VLA**<br>**DeeR-VLA**<br>**QAIL**<br>**MiniVLA**|**LLaRA**<br>**CLIP-RT**<br>**DiVLA**<br>**HiRT**|**FlashVLA**<br>**Spec-VLA**<br>**FLOWER**<br>**SpecPrune-VL**|**OpenVLA-OFT**<br>**MoLe-VLA**<br>**LightDP**<br>**A**<br>**VLA-Adapter**<br>**Evo-1**|**FAST**<br>**VLA-Cache**<br>**PD-VLA**<br>**NORA**<br>**SimpleVLA-RL**<br>**TwinVLA**|**SmolVLA**<br>**BitVLA**<br>**EfficientVLA**<br>**SP-VLA**<br>**CEED-VLA**<br>**CO-RFT**<br>|**DynamicVLA**<br>**DySL-VLA**<br>**RL Token**<br>**QVLA**<br>**DySta**<br>**QuantVLA**<br>**UniFS**<br>**Reflex**<br>**LoRA-SP**<br>**HiFi-UMI**|
|---|---|---|---|---|---|---|---|---|
|**TimeLine**|**-2023**|**2024**||𝝅𝟎|**202**<br>𝝅𝟎𝟔|**5**||**2026-**|
|**Foundational VLAs**|**RT-2**<br>**GR-1**<br>**PaLM-E**|**RT-H**<br>**OpenVLA**<br>**GR-2**<br>**CogACT**<br>𝝅𝝅𝟎𝟎<br>**3D**|**RDT-1B**<br>**-VLA**|𝝅𝝅𝟎𝟎.5<br>**GraspVLA**|**Hi Robot**<br>𝝅𝝅𝟎𝟎.𝟔𝟔<br>∗|**GR-3**<br>**RDT2**|**GR00T N1**<br>**WALL-OSS**|**Lingbot-VLA**<br>**Qwen-VLA**<br>𝝅𝝅𝟎𝟎.7<br>**Xiaomi-Robotics-1**|


Fig. 4: **Timeline of foundational and efficient VLAs.** This timeline charts the progression toward resource-conscious embodied intelligence. Inclusion in the “Efficient VLA” trajectory strictly requires explicit contributions addressing foundational bottlenecks via at least one of our core taxonomy pillars: mitigating computational footprint and inference latency (Efficient Model Design), minimizing adaptation overhead (Efficient Training), or reducing data acquisition costs (Efficient Data Collection). 

this survey, we distinguish these stages by their functions, since they are often mixed in existing literature. We define **Pre-training** as the stage that gives a VLM the basic capacity to act. It moves a general-purpose vision-language model into the embodied domain by aligning visual-language understanding with robot-executable actions. **Post-training** , in contrast, starts from this generalist policy and adapts it to specific tasks, environments, or resource budgets. For instance, RT-2 [3] integrates web-scale vision-language data with robotic trajectories, while OpenVLA [1] and _π_ 0 [2] leverage the massive Open X-Embodiment dataset [41] to establish generalized behavioral priors, which are subsequently specialized through task-specific post-training to align these foundations with environmental constraints for manipulative dexterity. 

Beyond these data-intensive pre-training paradigms, certain emerging works explore data-efficient [42], [43] adaptation or parameter-efficient fine-tuning [44], [45] to swiftly bridge the gap between frozen VLM backbones and robotic agency. Consequently, this survey encompasses a diverse methodological spectrum within the pre-training stage in Sec. 4.1, including techniques traditionally regarded as “post-training” in other domains [46], [47], [48], [49], [50], [51]. The key distinction is not the method itself, but its objective: _if the goal is to create the first version of the actioncapable model from a VLM, we classify it as pre-training._ This approach offers a more fundamental and logically consistent framework that aligns with the practical development lifecycle of VLAs. 

### _2.1.3 Data Collection Paradigms_ 

VLA data mainly comes from two sources: **real-world data** and **simulation data** . Real-world data is collected on physical robots through teleoperation. Representative datasets such as Open X-Embodiment [41], BridgeData V2 [52], and DROID [53] further standardize heterogeneous embodiments, tasks, and camera setups. In parallel, simulation data is generated in virtual environments by instantiating tasks, objects, and robot embodiments in physics engines. Benchmarks such as RLBench [54], RoboCasa [55], RoboGen [56], and LIBERO [57] are simulation data. Together, these two 

TABLE 1: **Efficiency-related metrics of representative VLAs.** The table reports the number of parameters ( **Params.** ), inference latency ( **I.L.** ), operating frequency ( **Freq.** ), and accelerator ( **Accelerator** ) of representative VLAs to contextualize cross-paper efficiency comparisons. “ _↓_ ” indicates that lower values are better, and “ _↑_ ” indicates that higher values are better. “/” denotes that the model can operate at two different frequencies. 

|**Models**|**Params.(**_↓_**)**|**I.L.(ms) (**_↓_**)**|**Freq.(Hz) (**_↑_**)**|**Accelerator**|
|---|---|---|---|---|
|RT-2-PaLI-X [3]|55B|330-1000|1-3|Multi-TPU cloud|
|RT-2-PaLI-X [3]|5B|200|5|Multi-TPU cloud|
|OpenVLA [1]|7B|166|6|RTX 4090|
|_π_0 [2]|3.3B|73|20/50|RTX 4090|
|Hi Robot [58]|3B|73|10/50|1–2 RTX 4090|
|GR00T N1 [12]|2.2B|63.9|-|L40 GPU|


sources constitute the basic training substrate for modern VLAs. 

### **2.2 The Need for Efficient VLAs** 

Despite the formidable capabilities demonstrated by VLA foundational models, their adoption beyond research prototypes faces significant barriers due to profound inefficiencies. These challenges stem from the "triple-bottleneck" across the model-training-data lifecycle. 

**Architectural Incompatibility.** From an architectural perspective, the primary impediment resides in the massive computational footprint of transformer-based VLM backbones. Characterized by billions of parameters [10], [11], [59], [60], these models incur prohibitive inference latency, resulting in control frequencies that fail to meet the stringent real-time requirements of dynamic robotic actuation, as evidenced in Tab. 1. This inefficiency is further amplified by visual signals [61], [62], which produce dense token sequences that must be processed through deep layers. 

**Training Overhead.** The current training paradigm is burdened by the exorbitant computational budgets and energy consumption required for large-scale pre-training. Recent works [63], [64] illustrate that foundational VLA pretraining is becoming a thousand-GPU-hours effort, requiring large accelerator clusters, distributed optimization, and 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

5 

TABLE 2: **Glossary of VLA efficiency metrics.** Standardized definitions of core efficiency dimensions across the modeltraining-data lifecycle. 

|**Terms**|**Definition**|
|---|---|
|Inference Latency<br>Control Frequency<br>Memory Footprint|End-to-end time from input query to model output.<br>The frequency at which a controller outputs control<br>commands or action signals, typically measured in Hz.<br>Runtime or storage memory required by parameters,<br>activations, and cached states.|
|Training Compute<br>Data Efficiency|Total computation consumed during training,<br>typically measured by FLOPs or GPU-hours.<br>The data requirement for achieving target<br>performance level; greater data efficiency corresponds<br>to lower data requirements for comparable<br>performance.|
|Deployment|Practical efficiency under real deployment constraints,|
|Efficiency|including latency, memory, and energy.|


high-throughput infrastructure. Achieving robust generalization across heterogeneous embodiments demands massive compute resources, creating a significant barrier to entry. 

**Data Scarcity.** VLA performance is strongly constrained by the quality and diversity of embodied datasets. Whether through labor-intensive real-world demonstrations [41], [52], [65] or expert-intensive simulation design [56], [66], curating diverse datasets remains time-consuming and difficult to scale, which slows embodied-policy scaling relative to data-rich vision-language domains. 

These profound inefficiencies collectively culminate in a critical deployment bottleneck for applications, particularly in resource-constrained settings such as autonomous vehicles and affordable consumer robotics. Therefore, the pursuit of efficiency is not merely an optional optimization but a fundamental prerequisite for unlocking the transformative potential of VLAs across the broader robotics landscape. Among the three, real-time inference is the most direct requirement for physical interaction. Training and data efficiency are less visible at deployment time, but they decide whether such systems can be built and scaled. Addressing this imperative, the field of **Efficient VLAs** has emerged. As illustrated in Fig. 4, the developmental trajectories of foundational VLAs and efficient VLAs are progressing in parallel. Notably, the timeline reveals a distinct acceleration in the emergence of efficient VLAs, particularly from late 2024 onwards. This proliferation underscores a rapidly intensifying research focus on resource-efficient models, likely driven by the demands of real-world robotic deployment. **Glossary of Efficiency Metrics.** Tab. 2 outlines a comprehensive glossary of VLA efficiency terms in this survey, grounding theoretical computational metrics into operational physical constraints within the embodied lifecycle. 

### **2.3 Taxonomy Principle** 

As discussed above, current VLAs are constrained by a "triple-bottleneck" across the model-training-data lifecycle. Accordingly, this survey reviews the efficiency of VLAs through the lens of three foundational pillars: model architecture, training paradigm, and data acquisition. It should be emphasized that these pillars do not represent isolated dimensions. Instead, they are closely connected and jointly define the efficiency landscape of VLAs: 

TABLE 3: **Comparison of related VLA surveys.** Prior works predominantly focus on general taxonomies or specific mechanisms, leaving a noticeable gap in systematic efficiency analysis. 

|**Survey**|**Year**|**Main Topic**|**Limitations**|
|---|---|---|---|
|Ma et al. [23]|2024|General VLA taxonomy for<br>embodied AI|Efficient VLAs scarcely<br>discussed|
|Shao et al. [26]|2025|Large VLM-driven robotic<br>manipulation VLAs|Only a few efficient<br>fine-tuning methods<br>mentioned|
|Xiang et al. [28]|2025|Human motor learning<br>inspired VLA post-training|No efficient solution listed|
|Zhong et al. [27]|2025|Action tokenization<br>methods in VLAs|Efficiency limited to<br>tokenization dimension|
|Din et al. [24]|2025|Robotic manipulation<br>oriented VLA review|Rarely discuss efficient<br>solutions|
|Zhang et al. [25]|2025|Pure end-to-end VLA<br>architectures|Only discuss part of<br>efficient inference|


(1) **Model** _↔_ **Training** : Efficient architectures ( _e.g.,_ Mamba backbones [19], [37] or MoE [67]) can reduce per-token or activated computation, lowering training and inference cost. Conversely, efficient training strategies (like PEFT [1], [14], [50]) allow massive foundational models to be adapted without retraining the entire parameter set. 

(2) **Training** _↔_ **Data** : Data-efficient pre-training focuses on maximizing the information gain per trajectory, reducing the total volume of data required [43]. In parallel, efficient data collection ( _e.g.,_ simulation synthesis) provides the high-throughput fuel necessary for large-scale training regimes [56], [66]. 

(3) **Data** _↔_ **Model** : Compact model designs often require higher-quality, task-specific data to maintain performance [1], whereas scalable data pipelines enable models to tolerate architectural sparsity through robust exposure to diverse scenarios [41], [53], [56]. 

This tripartite synergy binds model, training, and data into a co-dependent ecosystem. Based on this foundation, we provide an in-depth survey of these three pillars in Sec. 3-5, examining how they jointly shape the efficiency and practicality of VLAs. 

### **2.4 Relevant Surveys** 

The rapid growth of VLA research has made it a central paradigm in embodied AI. Several recent surveys have reviewed this field from different perspectives [23], [24], [25], [26], [27], [28]. As summarized in Tab. 3, existing surveys mostly present VLAs from a general or capability-centric perspective. For instance, Ma et al. [23] provide a holistic overview of VLAs in embodied AI, spanning low-level control, high-level task planning, and diverse datasets and benchmarks. Other surveys delve into specific paradigms: Shao et al. [26] elucidate VLA evolution through a VLMcentric lens, Xiang et al. [28] frame VLA post-training around human motor learning mechanisms, and Zhong et al. [27] isolate action tokenization as the architectural core, providing a systematic taxonomy of mainstream designs. Although [23] and [26] briefly touch upon works related to efficient VLAs in certain fields, none of them specifically address the efficiency problems from both model, training, and data view. To the best of our knowledge, this survey is the first to specifically focus on the VLA efficiency across the full lifecycle. We hope this survey will help establish 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

6 


Fig. 5: Key strategies for **Efficient Architectures** (Sec. 3.1), including Efficient Attention, Transformer Alternatives, Efficient Action Decoding, Lightweight Components, Mixture-of-Experts, and Hierarchical Systems. 

efficiency as a central principle of VLA research, guiding the development of scalable and deployable embodied intelligence. 

## **3 EFFICIENT MODEL DESIGN** 

This section studies efficient model design for VLAs under resource constraints. A central goal is to improve training and inference efficiency by reducing runtime latency, memory usage, and computational overhead while preserving model capability. We organize this section into two complementary directions: (1) **Efficient Architectures** , which improve model structures through modular design, accelerated execution, and sparse computation; and (2) **Model Compression** , which removes redundancy through pruning, quantization, and token optimization. Representative works on efficient model design are summarized in Tab. 4. 

### **3.1 Efficient Architectures** 

As illustrated in Fig. 5, this subsection reviews representative methods, including efficient attention, transformer alternatives, parallel and generative decoding, lightweight components, mixture-of-experts, and hierarchical processing. 

### _3.1.1 Efficient Attention_ 

Despite providing cross-modal synergy, the _O_ ( _L_<sup>2</sup> ) complexity of attention mechanisms [68] hinders real-time, longhorizon robotic control. Recent innovations tackle this via structural linearization, strategic sparsification, and memory optimization. SARA-RT [69] utilizes up-training to convert standard Transformers into linear-attention counterparts while preserving model quality. Moving from architecture to interaction, Long-VLA [70] reduces redundant attention via phase-aware masking, while dVLA [71] enables partial KV caching with prefix masking. To further alleviate inference bottlenecks, RetoVLA [72] repurposes register tokens for global context, while KV-Efficient VLA [73] leverages recurrent gating to compress historical KV caches into compact representations. Subsequently, BLURR [74] amortizes repeated attention computation through instructionprefix KV caching and FlashAttention. More recently, Reflex [75] extends cache reuse to flow-matching VLAs by partitioning attention context into static, sliding, and dynamic regions, enabling _O_ (1) incremental cache updates. Together, these methods enable scalable, low-latency VLA reasoning. 

### _3.1.2 Transformer Alternatives_ 

To circumvent the quadratic bottlenecks of Transformers, State-Space Models (SSMs) like Mamba [37] have emerged as high-efficiency alternatives with linear scaling. RoboMamba [19] pioneers this transition by adopting a Mamba backbone for streamlined embodied reasoning, while FlowRAM [76] further integrates it with conditional flow matching to enhance manipulative precision. These structural pivots catalyze a shift toward leaner yet potent VLA foundations. 

### _3.1.3 Efficient Action Decoding_ 

Standard autoregressive (AR) decoding in VLAs [1] treats actions as discrete tokens, which incurs _O_ ( _N_ ) latency and hinders real-time control. Efficiency is enhanced by either parallelizing the AR stream or replacing it with holistic generative decoders. 

**Parallel Decoding.** To mitigate AR bottlenecks, OpenVLAOFT [14], EdgeVLA [91], and SemanticVLA [114] exploit bidirectional decoding for single-pass action chunk prediction. PD-VLA [77] and its early-exit refinement CEED-VLA [80] recast decoding as nonlinear fixed-point equations solvable via parallel Jacobi iterations. Complementarily, SpecVLA [83] accelerates speculative decoding via relaxed acceptance, while SV-VLA [115] extends speculation to closedloop verification with deviation-triggered replanning. **Generative Decoding.** Generative paradigms supplant token-by-token chains with trajectory synthesis. TinyVLA [45] and HybridVLA [78] integrate diffusion decoders for continuous actions, while FlowRAM [76], NinA [85], and FreqPolicy [79] leverage Flow Matching or Normalizing Flows to bypass iterative denoising for one-shot or fewstep sampling. Further optimizations include MinD’s [81] world-model latents, AMS’s [84] computation reuse, and VQ-VLA’s [82] high-fidelity discretization. Finally, Discrete Diffusion VLA [86] unifies these by combining discretetoken interfaces with adaptive re-masking for efficient error correction. 

### _3.1.4 Lightweight Components_ 

Lightweight components offer a direct path to efficient VLAs by balancing parametric parsimony with operational efficacy. RoboMamba [19] exemplifies this with a 3.7Mparameter MLP head for 6-DoF pose prediction. Scaling this 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

7 

TABLE 4: **Representative works on Efficient Model Design.** "Categories" markers denote subcategories in Sec. 3: (A) Efficient Attention, (B) Transformer Alternatives, (C) Efficient Action Decoding, (D) Lightweight Component, (E) Mixtureof-Experts, (F) Hierarchical Systems, (G) Layer Pruning, (H) Quantization, and (I) Token Optimization. For general methods, the smallest experimental parameter scale is reported, with unavailable data denoted by “ _−_ ”. 

|**Method/Model**|**Categories**|**Architecture(V/L/A)**|**Param. Scale**|**Key Innovations in Efficient Model Design**|
|---|---|---|---|---|
|SARA-RT [69]|(A)|_−_/_−_/_−_|~5B(PaLI-X)|Quadratic-to-linear transformer up-training.|
|Long-VLA [70]|(A)|ResNet-18/CLIP/Diffusion Model(DDIM)|_−_|Phase-aware input masking, long-horizon attention optimization.|
|RetoVLA [72]|(A)|SigLIP/SmolLM2/Flow MatchingModel|_−_|Discarded register token reuse for spatial reasoning.|
|KV-Efficient VLA [73]|(A) (I)|DINOv2+SigLIP/LLaMA-2/_−_|~7B|RNN-gated chunked KV caching, selective contextpruning.|
|dVLA [71]|(A)|MAGViT-v2/MMaDA/FAST|_−_|Prefix attention masking, KV cachingfor diffusion speedup.|
|RoboMamba [19]|(B) (D)|CLIP/Mamba/MLP|~3.2B|Linear-complexityMamba reasoning, lightweight action decoding.|
|FlowRAM [76]|(B) (C)|CLIP/Mamba/MLP|_−_|Region-aware Mamba fusion, flow matching.|
|TinyVLA [45]|(C) (D)|ViT/Pythia/Diffusion Policy|1.3B|Compact VLM with a DP decoder for data-efficient adaptation.|
|PD-VLA [77]<br>|(C)<br>|CLIP/Vicuna/_−_<br>|~7B|Parallel fixed-point iteration for action chunking.<br>|
|OpenVLA-OFT [14]|(C)|DINOv2+SigLIP/LLaMA-2/MLP|~7B|Bidirectional attention forparallel continuous action decoding.|
|<br>HybridVLA [78]|(C) (I)|DINOv2+SigLIP/LLaMA-2/MLP|~7B|Diffusion-autoregression merger,pre-diffusion token KV caching.|
|FreqPolicy[79]|(C)|ResNet-18+MLP/LLaMA-2/U-Net|~7B|Frequencyconsistencyoptimization for flow-basedpolicies.|
|CEED-VLA [80]|(C)|_−_/_−_/_−_|~7B|Consistencydistillation, early-exitparallelJacobi decoding.|
|MinD [81]|(C) (F)|CLIP/_−_/DiT|_−_|Dual-system world models, asynchronous diffusion.|
|VQ-VLA [82]|(C)|DINOv2+SigLIP/LLaMA-2/VQ Decoder(VQ-VAE)|_−_|Scaledquantized tokenizers for discrete action smoothing.|
|Spec-VLA [83]|(C)|DINOv2+SigLIP/LLaMA-2/_−_|~7B|Relaxed speculative decoding,parallel token verification.|
|AMS [84]|(C) (I)|_−_/_−_/_−_|_−_|OS-level management with two-phase hashingfor action reuse.|
|NinA [85]|(C)|_−_/_−_/_−_|_−_|Normalizingflows for continuous action decoding.|
|Discrete Diffusion VLA [86]|(C)|DINOv2+SigLIP/LLaMA-2/_−_|~7B|Discrete diffusion embedding, unified action decoding.|
|CLIP-RT [87]|(D)|CLIP-ViT/CLIP/_−_|~1B|Pre-trained CLIP adaptation, 7xparameter reduction.|
|SVLR [88]|(D)|Mini-InternVL/Phi-3-mini/_−_|_−_|Modular small model integration, consumer GPU deployment.|
|NORA [89]|(D)|Qwen-2.5-VL(VLM)/FAST+|~3B|Compact Qwen2.5-VL-3B backbone with FAST+ tokenization.|
|SmolVLA [20]|(D) (G) (I)|SigLIP/SmolLM2/Flow MatchingTransformer|450M|_N_ = _L/_2layerpruning,pixel-shuffle compression.|
|SP-VLA [90]|(D) (I)|DINOv2+SigLIP/LLaMA-2/_−_|_−_|Action-aware schedulingand spatio-semantic tokenpruning.|
|EdgeVLA [91]|(D)|DINOv2+SigLIP/Qwen2-0.5B/_−_|~1B|Non-autoregressive small language models for edge devices.|
|MiniVLA [92]|(D)|DINOv2+SigLIP/Qwen2.5-0.5B/_−_|~1B|Small LLM integration, 7xparameter reduction.|
|GeRM [93]|(E)|_−_/_−_/_−_|_−_|MoE integration for fast inference, higher capacity.|
|FedVLA [94]|(E)|_−_/_−_/_−_|_−_|Dual-gatingMoE, federated adaptive expert activation.|
|TVVE [95]|(E)|_−_/_−_/_−_|_−_|MoE visual encoder, task-disentangled feature extraction.|
|HiRT [44]|(F)|EfficientNet/InstructBLIP/MAP|_−_|Hierarchical transformers, low-to-high frequency policy guidance.|
|RoboDual [96]|(F)|DINOv2+SigLIP/LLaMA-2/DiT|~7B|Generalist VLA, high frequencydiffusion specialist.|
|DP-VLA [97]|(F)|DINOv2+SigLIP/LLaMA-2/BC-Transformer|_−_|Dual-process framework, reasoning-executor co-design.|
|HAMSTER [98]|(F)|SigLIP/Vicuna-13B-v1.5/3D-DA|_−_|High-level VLM 2Dpaths, low-levelpolicy guidance.|
|FiS [99]|(F)|DINOv2+SigLIP/LLaMA-2/_−_|_−_|Execution-in-reasoning parameter sharingwith dual-system.|
|MoLe-VLA [18]|(G)|DINOv2+SigLIP/LLaMA-2/DiT|_−_|Spatio-temporal routing, selective LLM layer skipping.|
|EfficientVLA [22]|(G) (I)|DINOv2+SigLIP/LLaMA-2/DiT|~5B|Training-free layerpruning, task-relevant token compression.|
|RLRC [100]|(G) (H)|_−_/_−_/_−_|_−_|Structured layerpruning, RL recovery, 4-bitquantization.|
|FLOWER [101]|(G)|Florence-2 ViT/Florence-2 LLM/Flow Transformer|950M|Intermediate modalityfusion, 50% LLM layerpruning.|
|OpenVLA [1]|(H)|DINOv2+SigLIP/LLaMA-2/_−_|~7B|7B VLAquantization framework, zero success-rate degradation.|
|QAIL [102]|(H)|_−_/_−_/_−_|_−_|Quantization-aware fine-tuning, low-bit error mitigation.|
|FAST [21]|(H) (I)|_−_/_−_/_−_|_−_|DCT/BPE action tokenization for action sequences.|
|SQIL [103]|(H)|_−_/_−_/_−_|_−_|Saliency-based loss weighting,quantization-aware training.|
|BitVLA [104]<br>|(H)<br>|SigLIP-L/BitNet b1.58 2B4T/_−_<br>|~3B|1-bit ternary quantization, vision encoder distillation alignment.<br>|
|SQAP-VLA [105]|(H) (I)|Prism-DinoSigLIP/Llama-2/DiT|_−_|Quantization-aware tokenpruningwithquantizer enhancement.|
|VLA-Cache [61]|(I)|_−_/_−_/_−_|_−_|Inter-frame change-aware token selection and KV-cache reuse.|
|FlashVLA [106]|(I)|_−_/_−_/_−_|_−_|Visual tokenpruningvia ICS, stability-based action reuse.|
|Fast ECoT [107]|(I)|DINOv2+SigLIP/LLaMA-2/_−_|_−_|High-level reasoningtoken caching, ECoT cross-timestepreuse.|
|CronusVLA [108]|(I)|DINOv2+SigLIP/LLaMA-2/DiT|~7B|FIFO-queued motion feature caching, multi-frame inference.|
|VOTE [109]|(I)|DINOv2+SigLIP/LLaMA-2/MLP|~7B|Action chunk compression into single <ACT> tokens.|
|CogVLA [110]|(I)|DINOv2+SigLIP/LLaMA-2/_−_|~7B|Instruction-driven token aggregation, FiLM routing, thresholds.|
|SpecPrune-VLA [62]|(I)|_−_/_−_/_−_|_−_|Dynamic tokenpruning,global-local attention, velocitycontrol.|
|LightVLA [111]|(I)|DINOv2+SigLIP/LLaMA-2/MLP|~7B|Gumbel-Softmax differentiable tokenpruning.|
|ADP [112]|(I)|DINOv2+SigLIP/LLaMA-2/MLP|~7B|Trajectory-gated, text-guided vision tokenpruning.|
|<br>Oat-VLA [113]|(I)|DINOv2+SigLIP/LLaMA-2/_−_|~7B|<br>Gripper-guided object/agent-centric token compression.|


philosophy to the backbone, TinyVLA [45], EdgeVLA [91], and MiniVLA [92] leverage sub-2B SLMs, while NORA [89] adopts a compact 3B backbone and Evo-1 [116] preserves semantic alignment at 0.77B. DynamicVLA [117] further pairs a 0.4B VLA with convolutional vision encoding for dynamic manipulation. 

CLIP-RT [87] and DiVLA-2B [118] further show that 1– 2B models can outperform 7B counterparts in throughput and task success. For edge deployment, SVLR [88] combines retraining-free lightweight modules, while LiteVLA [119] enables 4-bit CPU-only deployment on Raspberry Pi 4. Finally, SP-VLA [90] introduces an action-aware scheduler that dynamically alternates between heavy and light generators, achieving frequency-adaptive acceleration with 

negligible performance loss. Together, these designs reduce VLA size and inference cost for edge deployment. 

### _3.1.5 Mixture-of-Experts_ 

Mixture-of-Experts (MoE) architectures decouple model capacity from computational cost by routing tokens to specialized subnetworks. GeRM [93] pioneers sparse MoE in quadruped reinforcement learning, demonstrating that selective activation scales multi-task expressiveness while maintaining inference thrift. Extending this paradigm, FedVLA [94] proposes Dual Gating MoE (DGMoE), utilizing bidirectional token selection to dynamically sparsify computational graphs beyond standard top- _K_ mechanisms. Similarly, TVVE [95] introduces Task-Aware MoE (TaskMoE) to conditionally engage experts based on linguistic-visual 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

8 


Fig. 6: Key strategies for **Model Compression** (Sec. 3.2), including Layer Pruning, Quantization, and Token Optimization through compression, pruning, and caching. 

signals, enabling cross-task interference mitigation through semantic routing. Collectively, these frameworks catalyze modular, adaptive VLAs that harmonize expansive generalization with pragmatic deployment. 

### _3.1.6 Hierarchical Systems_ 

Inspired by dual-process theories [120], [121], hierarchical VLAs bifurcate cognition into deliberate "System 2" reasoning and intuitive "System 1" execution. This decoupling lets compute-intensive VLMs guide latency-sensitive control asynchronously, reconciling semantic depth with realtime responsiveness. 

HiRT [44] and DP-VLA [97] establish low-frequency VLM guidance for high-frequency control, while SmolVLA [20] decouples inference from action execution. RoboDual [96] and HAMSTER [98] condition low-level policies on generalist outputs or 2D paths. FiS [99] partially shares parameters across systems, Fast ECoT [107] asynchronously decouples reasoning from action decoding, and MinD [81] couples low-frequency foresight with high-frequency diffusion control. Recent variants refine the temporal interface: DuoCore-FS [122] buffers slow-path latents for whole-body control, Yan et al. [123] caches semantics within existing VLAs, and UniFS [124] stratifies VLM layers by update frequency. Collectively, these hierarchical architectures scale cognitive depth without compromising operational alacrity. 

### **3.2 Model Compression** 

As illustrated in Fig. 6, this subsection systematically surveys pivotal techniques, from layer pruning and quantization to token optimization, elucidating their general schemes and how they benefit efficiency to cultivate robust, edge-compatible architectures. 

### _3.2.1 Layer Pruning_ 

Layer pruning strategically removes or bypasses redundant layers to reduce model size and latency, exploiting the high interlayer similarity of large-scale VLMs [18], [22]. These methods span fixed structural pruning and adaptive layer skipping. 

Fixed schemes impose predetermined sparsity for efficient inference. SmolVLA [20] truncates the VLM at half depth, EfficientVLA [22] performs training-free importanceguided layer pruning, and RLRC [100] couples structured 

pruning with SFT/RL recovery. LightDP [125] learns SVDinitialized DiT block pruning with consistency distillation, while FLOWER [101] prunes architecture-specific VLM layers via intermediate fusion. 

Adaptive schemes instead allocate depth online. DeeRVLA [126] employs action-consistency-based early exits, while MoLe-VLA [18] dynamically routes layers via STAR. DySL-VLA [127] further retains informative layers statically while skipping incremental layers dynamically according to action importance. 

### _3.2.2 Quantization_ 

Quantization discretizes weights and activations into lowbit representations, drastically curtailing memory footprints while preserving the fidelity of multimodal action synthesis. OpenVLA [1] shows that 4-bit PTQ can halve GPU memory with negligible performance loss. QAIL [102] introduces quantization-aware imitation learning, while SQIL [103] further emphasizes mission-critical states via saliencyweighted training. BitVLA [104] pushes VLAs to ternary 1-bit precision with distillation-aware vision compression, while RLRC [100] applies 4-bit quantization after SFT/RL recovery. 

Beyond model weights, FAST [21] compresses actions through DCT/BPE tokenization, while SQAP-VLA [105] codesigns quantization and token pruning with Hadamard stabilization. More recently, QVLA [128] allocates channelwise bits by action sensitivity, while QuantVLA [129] performs scale-calibrated PTQ across language and DiT action modules. Collectively, these advancements sculpt VLAs for resource-frugal, ubiquitous embodiment. 

### _3.2.3 Token Optimization_ 

Token optimization strategically refines representational sequences in VLAs to mitigate the quadratic escalation of Transformer-based computations. By orchestrating compression, pruning, and caching, these paradigms curtail redundancy and expedite embodied reasoning on resourceconstrained platforms. 

**Token Compression.** Token compression aggregates voluminous streams into succinct representations to bolster inference velocity. For visual inputs, SmolVLA [20] employs pixel shuffling to limit tokens per frame, while CogVLA 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

9 

[110], Oat-VLA [113], and Compressor-VLA [130] compress task-relevant content via instruction-driven aggregation, object-agent-centric tokenization, and instructionguided semantic-spatial compression, respectively. Action tokens are similarly condensed: FAST [21] combines DCT with BPE for action sequence compression, whereas VOTE [109] represents each action chunk with a single <ACT> token decoded by an action head. 

**Token Pruning.** Pruning excises redundant tokens based on saliency metrics to streamline computational demands. FlashVLA [106] and EfficientVLA [22] prune visual tokens by information contribution and task-aware diversity, respectively, while SP-VLA [90] adds spatio-semantic importance. SpecPrune-VLA [62] exploits cross-step attention and action granularity; SQAP-VLA [105] stabilizes pruning under quantization; and LightVLA [111] learns differentiable selection via Gumbel-softmax. KV-Efficient VLA [73] recurrently gates compressed historical KV chunks, whereas ADP [112] adapts token retention to recent action dynamics. More recently, VLA-Pruner [131] jointly scores semantic and action relevance via prefill and temporally smoothed decode attention, while TEAM-VLA [132] combines current-frame foreground expansion with action-guided token merging. **Token Caching.** Token caching exploits temporal invariances to eliminate redundant computations across iterative steps. VLA-Cache [61] reuses static visual KV entries across frames, while HybridVLA [78] extends KV caching to diffusion-based action generation. FlashVLA [106] reuses stable actions, whereas Fast ECoT [107] caches high-level reasoning. Beyond KV reuse, EfficientVLA [22] caches intermediate diffusion features, while CronusVLA [108] reuses compact motion features across frames. AMS [84] generalizes reuse through a hardware-aware context pool spanning KV states, diffusion latents, and action outputs. More recently, DySta [133] disentangles multi-level static and dynamic visual tokens and learns when to refresh static KV caches, enabling efficient long-horizon multi-frame inference. 

### **3.3 Discussion** 

### _3.3.1 Innovations_ 

Current designs for efficient VLAs have shifted from a purely scaling-centric paradigm toward adaptive, lightweight architectures. Linear sequence alternatives, such as the Mamba backbone [19], [76], alleviate the quadratic computational bottleneck of traditional Transformer architectures. Concurrently, parallel decoding strategies, such as bidirectional masked prediction [14], [91] and parallel Jacobi iteration [77], [80], together with generative trajectory prediction [45], [78], [79], reduce token-by-token autoregressive action decoding overhead. Furthermore, hierarchical system designs [44], [97] decouple high-level semantic planning from low-level real-time control, while dynamic token pruning [22], [90], compression [21], [110], and caching [61], [106] techniques reduce redundant computation with limited performance loss in reported settings. 

### _3.3.2 Limitations, Challenges and Future Works_ 

A fundamental trade-off exists between structural sparsification and high-fidelity behavioral representations. Exten- 

sive model pruning and low-bit quantization can compromise latent planning depth [102], [126], degrading finegrained manipulation precision in complex, long-horizon tasks. Furthermore, asynchronous hierarchical systems and parallel decoding frameworks often suffer from spatiotemporal misalignment in dynamic environments [44], which induces control oscillations and jeopardizes hardware safety. 

To address these bottlenecks, future architectures must prioritize intrinsic adaptability by coupling algorithmic design with hardware deployment. Through hardwaresoftware co-design and system-level optimization [84], models can be aligned with specific execution profiles, effectively mitigating computational constraints across heterogeneous edge devices. Ultimately, this co-optimization paradigm enables scalable deployment from consumer devices to industrial manipulators without compromising cross-modal reasoning capabilities. 

## **4 EFFICIENT TRAINING** 

While foundational VLAs leverage pre-trained VLM backbones for robust multimodal reasoning, they inherit prohibitive computational and data overheads, necessitating the advancement of **Efficient Training** methodologies to minimize resource footprint while maintaining competitive performance. As illustrated in Fig. 7, this chapter systematically explores the spectrum of these techniques, focusing on two pivotal stages: (1) **Efficient Pre-training** , instilling foundational action capabilities into pre-trained VLMs or training the entire VLA from scratch with minimal overhead, and (2) **Efficient Post-training** , enabling the swift and effective deployment of VLAs to specific downstream tasks. We list representative works in Tab. 5. 

### **4.1 Efficient Pre-Training** 

As illustrated in Fig. 7 left, this section systematically examines advancements categorized into data-efficient pretraining, efficient action representation, and other efficient pre-training strategies. By highlighting these innovations, we outline the critical pathways for developing robust, general VLA policies without incurring the traditional burden of extensive, resource-intensive pre-training cycles. 

### _4.1.1 Data-Efficient Pre-training_ 

To mitigate the data scarcity inherent in embodied learning, data-efficient pre-training prioritizes the strategic utilization of scarce robotic trajectories alongside abundant non-robotic sources, such as ego-centric videos. This paradigm primarily evolves through two axes: (1) self-supervised objectives that extract intrinsic signals from unlabeled data, and (2) mixeddata co-training frameworks designed to bridge domain gaps. 

**Self-Supervised Training.** Self-supervised training synthesizes supervisory signals from unlabeled or passive datasets to alleviate the prohibitive cost of expert demonstrations. Current research focuses on two frontiers. 

First, to maximize the utility of existing robotic data, DTP [42] employs a diffusion-based trajectory prediction objective. By modeling future end-effector trajectories in the RGB domain, it bridges the vision-action modality gap and improves long-horizon generalization. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

10 


Fig. 7: Key strategies for **Efficient Training** (Sec. 4), comprising Efficient Pre-Training and Efficient Post-Training with their corresponding strategies. 

Second, a more prevalent direction leverages internetscale ego-centric videos to bypass the need for explicit action labels. While LAPA [43] pioneered learning discrete latent action spaces from action-less videos, subsequent works have addressed its susceptibility to task-irrelevant noise ( _e.g.,_ camera shake). For instance, Bu et al. [134] introduced a task-centric VQ-VAE to decouple essential actions from environmental dynamics, while LAWM [135] extended this principle to compact world-model architectures. Expanding beyond latent spaces, EgoVLA [136] and Being-H0 [137] utilize human anatomical priors ( _e.g.,_ MANO parameters) to map human hand movements to robotic manipulation. Complementarily, RynnVLA-001 [138] and Wang et al. [139] demonstrate that pre-training on environment dynamics via generative world models provides a robust foundation for sample-efficient policy fine-tuning. 

**Mixed Data Co-training.** Mixed-data co-training enhances VLA efficiency and transferability by unifying heterogeneous datasets of varying quality and modality. GeRM [93] utilizes a Conservative Q-Learning (CQL) framework to robustly ingest both expert and suboptimal data, mitigating overestimation on out-of-distribution actions. To manage cross-domain complexity, HAMSTER [98] adopts a hierarchical decoupling strategy—predicting 2D trajectories to condition 3D control—thereby efficiently assimilating massive non-robotic data. Similarly, GraspVLA [140] integrates autoregressive perception with flow-matching action generation via Chain-of-Thought (CoT) reasoning. Furthermore, AnyPos [141] uses arm-decoupled estimation to extract transferable motion primitives from task-agnostic data, while TwinVLA [142] composes pretrained single-arm policies for bimanual control without bimanual pre-training. Similarly, WSA1 [143] combines heterogeneous data with 3D world-action joint modeling for data-efficient generalization. 

### _4.1.2 Efficient Action Representation_ 

The high dimensionality and inherent noise of robot action spaces frequently impede VLA training efficiency and generalization. To address this, current research transitions from modeling raw control signals to learning compact, 

semantic motion primitives, primarily through action space compression and innovative structural modeling. 

**Action Space Compression.** A dominant strategy involves projecting continuous actions into distilled latent spaces to truncate the policy search space. While LAPA [43] and Bu et al. [134] utilize VQ-VAE [144] for its robust quantization benefits, RynnVLA-001 [138] and LAWM [135] leverage standard VAE architectures or world-model priors to learn these embeddings. Moving beyond per-step encoding, FAST [21] achieves significant pre-training speedups by applying sequence-level compression, such as DCT and BPE, thereby reducing dimensionality in the temporal domain. More recently, INN Adapter [145] constrains one-step flow matching within an invertible latent action manifold, preserving information while avoiding iterative denoising. 

**Modality Alignment.** Complementarily, efficiency is enhanced by aligning action spaces with visual or anatomical priors. EgoVLA [136] bridges the human-robot domain gap through MANO-based shared action spaces, while VLAAdapter [146] employs a Bridge Attention module to facilitate cross-modal fusion. Furthermore, structural optimizations, such as cVLA’s [147] adoption of image-coordinatebased encoding or ReSET’s [148] restructuring states, simplify the complex mapping from vision to actuation. Ultimately, these advancements enable VLA models to bypass low-level control noise and focus on mastering transferable motion primitives. 

### _4.1.3 Other Pre-training Strategies_ 

Complementing data and action-centric optimizations, several specialized paradigms further bolster VLA pre-training efficiency. **Multi-stage training** [19], [42], [138], [140], [149], [162] in the pre-training phase partitions the learning pipeline into sequential phases, such as modality alignment, cognitive reasoning, and action fine-tuning. MotionWAM [163] stages egocentric dynamics pre-training, crossembodiment grounding, and whole-body adaptation. This staged decoupling enables progressive representation transfer, allowing the model to consolidate foundational perception before mastering complex physical interactions, thereby reducing aggregate computational overhead. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

11 

TABLE 5: **Representative works on Efficient Training.** The “Training Phase” column denotes the specific learning stage where efficient optimizations are targeted. The “Strategies” markers “IL”, “On-RL”, and “Off-RL” correspond to efficiencyfocused Imitation Learning, Online Reinforcement Learning, and Offline Reinforcement Learning paradigms, respectively. “Trainable modules” column outlines the specific architectural components updated during training. 

|**Method/Model**|**Training Phase**|**Strategies**|**Trainable modules**|**Key Innovations in Efficient Training**|
|---|---|---|---|---|
|GeRM [93]|Pre-training|Off-RL|decoder-only Transformer + sparse MoE experts|Sparse MoE routing, offline RL over demonstration and sub-optimal data.|
|LAPA [43]|Pre-training|IL|VLM backbone + action quantization model|Unsupervised VQ-VAE quantization, label-free latent action extraction from video.|
|HAMSTER [98]|Pre-training|IL|vision encoder + LLM backbone + action module|Hierarchical action modeling, embodiment-agnostic 2D path representation.|
|DTP [42]|Multi-stage training|IL|diffusion trajectory model + action module<br>|Diffusion-based trajectory synthesis, long-horizon task training configuration.|
|Humanoid-VLA [149]|Multi-stage training|IL|vision encoder + cross-attention module + LLM<br>backbone + codebook|Language–motion pre-alignment, parameter-efficient egocentric visual adaptation.|
|GraspVLA [140]|Multi-stage training|IL|LLM backbone + projector + flow action expert|Synthetic data scaling, dual-stage grasping pre-training pipeline.|
|UniVLA (Bu et al. ) [134]|Multi-stage training|IL|VLM backbone + action expert|Language-conditioned task-centric video latents for cross-embodiment policy learning.|
|UniVLA (Wang et al.) [139]|Pre-training|IL|multimodal transformer|Multimodal tokenization, sparse data stream unification.|
|EgoVLA [136]|Pre-training|IL|VLM backbone + action head|MANO-shared action space for egocentric transfer, human-to-robot retargeting.|
|AnyPos [141]|Pre-training|IL|DINOv2-Reg + DAD + MLP|Inverse dynamics modeling, task-agnostic data utilization pipeline.|
|Being-H0 [137]|Pre-training|IL|LMM backbone + motion tokenizer + action expert|Video-derived hand motion priors, physical instruction tuning implementation.|
|RynnVLA-001 [138]|Multi-stage training|IL|AR Transformer + ActionVAE + action head|ActionVAE chunk compression and continuous mapping for multi-stage transfer.|
|LAWM [135]|Pre-training|IL|imitation learning model + world model|Self-supervised imitation-world models for latent forecasts and action extraction.|
|FAST [21]|Pre-training|IL|autoregressive VLA with FAST action tokenizer|DCT and BPE integration, action sequence compression via quantization.|
|cVLA [147]|Pre-training|IL|PaliGemma2 self-attention layers|Image-space discrete keypose prediction, simulation-based training structure.|
|VLA-Adapter [146]|Pre-training|IL|ActionQuery + Bridge-Attention + action module|Bridge Attention mechanism, vision-language feature injection into actions.|
|ReSET [148]|Pre-training|IL|scoring network + flow generator + action policy|Human-video-guided initial-state restructuring with a flow-based reduction policy.|
|RoboMamba [19]|Multi-stage training|IL|vision encoder + LLM backbone + action head|Mamba-based efficient alignment, followed by compact policy head adaptation.|
|TinyVLA [45]|Pre-training|IL|vision encoder + LLM backbone + policy head|LoRA-based compact VLM initialization, direct policy transfer bypassing data.|
|TVVE [95]|Multi-stage training|IL + Off-RL|TaskMoE + MVEP + action module|Pseudo-environment deployment, proactive informational perspective capturing.|
|OpenVLA [1]|Post-training|IL|VLM backbone|Systematic PEFT evaluation, comparative analysis.|
|Atomic Skill Library [150]|Post-training|IL|skill-specific VLA policies|Few-shot supervised fine-tuning, atomic skill VLA adaptation architecture.|
|OpenVLA-OFT [14]|Post-training|IL|VLM backbone + action head|Parallel decoding implementation, action chunking integration, LoRA fine-tuning.|
|MoManipVLA [151]|Post-training|IL|VLM backbone|Waypoint-guided supervised fine-tuning, mobile manipulation adaptation.|
|OpenHelix [152]|Post-training|IL|LLM backbone +<ACT>token + action expert|Target-specific <ACT> token refinement, selective parameter updating.|
|ControlVLA [153]|Post-training|IL|additional cross-attention layers|Object-centric representation injection, ControlNet-style adaptation architecture.|
|CronusVLA [108]|Post-training|IL|VLM backbone + cross-frame decoder|Historical frame aggregation, single-to-multi-frame decoding transition design.|
|InstructVLA [64]|Post-training|IL|MoE adapter|LoRA fine-tuning, MoE-adaptation module integration.|
|RICL [154]|Post-training|IL|LLM backbone|Distance-weighted action interpolation, in-context training mechanism.|
|ATE [155]|Post-training|IL|ActionVAE + guidance module|Latent space fine-tuning, unified latent guidance mechanism.|
|RPD [156]|Post-training|On-RL|action module|MSE-guided on-policy exploration, VLA distillation into compact structures.|
|RIPT-VLA [157]|Post-training|On-RL|action head|Dynamic rollout sampling, leave-one-out advantage estimation.|
|VLA-RL [158]|Post-training|On-RL|VLA policy + value model|Trajectory-level RL, auto-regressive modeling, pseudo-labeled segment rewards.|
|CO-RFT [159]|Post-training|Off-RL|action expert + critic network|Action-chunk TD learning extension, offline RL policy fine-tuning.|
|ARFM [160]|Post-training|Off-RL|VLM backbone + action expert|Loss scaling factor introduction, flow matching loss modification.|
|SimpleVLA-RL [13]|Post-training|On-RL|VLM backbone + action head|VLA-specific trajectory sampling, parallelized training execution.|
|RehearseVLA [161]|Post-training|On-RL|world model + VLA Policy + reflector|Video-based world model deployment, resettable virtual environment.|


Strategic integration of **reinforcement learning** (RL) and **modular adaptation** further catalyzes this efficiency. To maximize data utility, GeRM [93] employs Conservative Q-Learning to ingest suboptimal trajectories, while TVVE [95] utilize pseudo-environments to accelerate convergence by bypassing real-world trial-and-error. Parallelly, parameter-efficient fine-tuning (PEFT) via Low-Rank Adaptation (LoRA [46]) is adopted in [44], [45] to inject lightweight adapters into frozen VLM backbones. This approach preserves the potent multimodal priors of large-scale models while minimizing the gradient updates required for action integration, yielding resource-aware VLAs without compromising performance. 

### **4.2 Efficient Post-Training** 

As illustrated in Fig. 7 right, these methods encompass supervised fine-tuning for targeted parameter updates and reinforcement learning-based approaches for policy optimization. Notably, efficient post-training adapts pretrained VLAs to downstream embodiments and tasks while reducing parameter, data, interaction, or optimization costs. 

### _4.2.1 Supervised Fine-tuning_ 

Supervised Fine-Tuning (SFT) specializes pre-trained VLAs for downstream tasks, balancing task-specific proficiency with the preservation of multimodal priors. Systematic benchmarking in OpenVLA PEFT [1] identifies LoRA as the optimal performance-compute trade-off. OpenVLAOFT [14] couples LoRA with parallel chunk decoding, InstructVLA [64] with MoE adapters, and Omaisan et al. [164] 

with 4-bit quantization for 8GB consumer GPUs; LoRASP [165] further replaces fixed ranks with input- and layeradaptive capacity. 

To overcome the dependency on extensive labeled data, recent research emphasizes **sample-efficient adaptation** through structural and contextual priors. Methods such as ControlVLA [153] and MoManipVLA [151] utilize zeroinitialized layers or bi-level trajectory optimization to enable successful transfer with as few as 10–50 samples. Complementarily, OpenHelix [152] updates a learnable <ACT> token atop a frozen MLLM, while CronusVLA [108] introduces lightweight cross-frame decoding for multi-frame adaptation. Beyond gradient-based tuning, RICL [154] adopts In-Context Learning (ICL) to retrieve task-relevant prompts, while ATE [155] employs energy-guided latent alignment to steer policy distributions. Together, these strategies facilitate a transition from broad digital knowledge to specialized physical expertise with minimal overhead. 

### _4.2.2 RL-Based Methods_ 

While SFT relies heavily on demonstration quality, reinforcement learning (RL)-based post-training provides a robust mechanism to overcome data scarcity and environmental variability. These methodologies span online paradigms that refine policies through interactive rollouts and offline frameworks that optimize policies and value functions from fixed trajectory datasets. 

**Online Adaptation and Exploration.** Online RL enhances VLA proficiency through real-time environment feedback 

12 

#### JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

and sophisticated reward engineering. To achieve extreme sample efficiency, RIPT-VLA [157] combines leave-one-out advantage estimation with PPO and sparse binary rewards, improving an SFT policy from 4% to 97% with only one demonstration. VLA-RL [158] instead employs PPO with a VLM-based process reward model and a curriculum selection strategy, while SimpleVLA-RL [13] adopts GRPO with binary outcome rewards and exploration-enhancing rollout strategies. To reduce RL overhead, RehearseVLA [161] shifts exploration to virtual simulators, RPD [156] distills VLA guidance into compact RL experts, and RL Token [166] freezes the VLA while training lightweight actor–critic heads on its learned RL token. Furthermore, human-in-theloop paradigms, such as the "Talk-and-Tweak" scheme [167], incorporate linguistic corrections into diffusion-based models, enabling rapid error recovery and multi-robot coordination. 

**Offline Value Regularization.** In contrast, offline RL focuses on maximizing the utility of archived trajectories while mitigating the distribution shift inherent in out-of-distribution (OOD) actions. Central to this axis, the offline stage of ConRFT [168] and CO-RFT [159] employ Cal-QL [169] to penalize overestimation of OOD actions, integrating consistency objectives or transformer-based critics to stabilize valuebased learning. Building on these foundations, ARFM [160] introduces adaptive scaling in flow-matching losses to curb variance and bolster perturbation robustness. Collectively, these RL-driven pipelines empower VLAs to transcend the limits of passive imitation, fostering autonomous prowess and data-thrifty adaptation. 

### **4.3 Discussion** 

### _4.3.1 Innovations_ 

The core of efficient training paradigms lies in establishing an embodied learning mechanism that balances trainingresource efficiency with robust generalization performance across the model training lifecycle. During the pre-training stage, efficiency is primarily driven by mitigating the embodied data-silo effect through the extraction of latent skills from unannotated internet videos [43], [139], [149] or anatomical priors [136], combined with multi-dimensional action-space compression to shrink the policy search space and accelerate convergence. In the subsequent post-training phase, downstream adaptation is highly optimized through parameter- and sample-efficient supervised fine-tuning that drastically reduces training overhead via structural or contextual priors [14], [64], seamlessly coupled with interactive online exploration [167] and conservative offline reinforcement learning [159], [168] to achieve rapid task specialization while robustly safeguarding against out-of-distribution policy collapse. 

### _4.3.2 Limitations, Challenges and Future Works_ 

Despite these advances, kinematic and dynamic discrepancies between human egocentric data and robotic platforms introduce significant domain noise, degrading the transferability of cross-embodied action priors [136]. Furthermore, while PEFT methods ( _e.g.,_ LoRA) can limit adaptation capacity under restrictive trainable-parameter budgets, particularly when substantial policy reconfiguration 


Fig. 8: **Taxonomy of Efficient Data Collection strategies in VLAs.** This figure illustrates the primary approaches under Sec. 5, encompassing human-in-the-loop, simulated, reusability-oriented, self-driven, and augmentative techniques aimed at scaling dataset acquisition and improving data collection efficiency. 

is required [170]. During post-training, RL-based online methods often suffer from sample inefficiency and high gradient variance under sparse rewards [171]. Conversely, offline RL is susceptible to action-distribution shift and Q- value overestimation on OOD actions [159], [168]. 

Future research should prioritize physics-informed, closed-loop training paradigms. To better assimilate human egocentric data, these paradigms could explore explicitly incorporating geometric, kinematic, or physical consistency constraints into training objectives, such as a kinematic consistency loss _L_ kinematics. Furthermore, to reduce reliance on task-specific reward engineering, future RL post-training may exploit learned progress signals, adaptive multi-teacher guidance [172], and hierarchical RL frameworks to systematically address the challenge of reward sparsity. 

## **5 EFFICIENT DATA COLLECTION** 

VLA performance depends on diverse, high-quality demonstrations, but data collection via human teleoperation is costly and hard to scale. **Efficient Data Collection** strives to scale up high-quality datasets at significantly reduced time and resource expenditure. As illustrated in Fig. 8, Recent efforts to overcome these challenges have pursued several strategies, including human-in-the-loop data collection (Sec. 5.1), simulation data collection (Sec. 5.2), Internet-scale and cross-domain data utilization (Sec. 5.3), self-exploration data collection (Sec. 5.4), and data augmentation (Sec. 5.5). We systematically review these strategies, analyzing their core principles and representative methods, with a concise summary provided in Tab. 6. 

### **5.1 Human-in-the-Loop Data Collection** 

Human-in-the-loop data collection is limited by expertdependent, one-to-one demonstrations, leading to data 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

13 

TABLE 6: **Representative works on Efficient Data Collection.** Categories follow Sec. 5: (A) Human-in-the-loop Data Collection, (B) Simulation Data Collection, (C) Internet-Scale and Cross-Domain Data Utilization, (D) Self-Exploration Data Collection, and (E) Data Augmentation. “Dataset Composition” reports quantity only, and “ _−_ ” means not specified. “Quality Control” summarizes data validation or correction. “Collection” Acceleration summarizes reductions in real-robot data collection. 

|**Method/Dataset**|**Categor**|**y Dataset Composition**|**Quality Control**|**Collection Acceleration**|
|---|---|---|---|---|
|CLIP-RT [87]|(A)|18.1M transitions,21K in-domain transitions|STA checks; heuristic labels.|Low-skill teleop+ STA expansion.|
|GCENT [173]|(A)|48K–62K real frames.|HDF5 validation; mode labels; Task Sentinel.|Failure rewind/refine; one-to-manysupervision.|
|GeRM [93]|(B)|257K simulation trajectories.|Success/failure labels; CQLpenalty.|Automatic Isaac Gym rollouts.|
|GraspVLA [140]|(B)|1Bgraspframes.|CuRobo success; ray-traced randomization.|Parallel syntheticgrasp generation.|
|cVLA [147]|(B)|150k synthetic trainingsamples.|Execution success; visibility/manual filters.|Randomized simulationpre-training.|
|RoboTwin 2.0 [16]|(B)|100K+ expert trajectories.|10 trials; log/VLM diagnosis;_≤_5 repairs.|Code synthesis + simulation feedback.|
|ReBot [174]|(B)|220 real episodes.|Replayvalidation; VBench check.|Simulation replay+ background inpainting.|
|R2R2R [175]|(B)|1 scan + 1 demo_→_50–1000 renders/task.|3DGS tracking; interpolation; real eval.|Single scan/demo to manyrenders.|
|RealMirror [176]|(B)|5 scenarios; 1K+ trajectories.|Jump/jitter filter; temporal ensembling.|VR/Isaac reusable simulation demos.|
|SmolVLA [20]|(C)|481 sets; 22.9K episodes.|VLM labels; camera-view normalization.|Community-data reuse.|
|EgoVLA [136]|(C)|_∼_500K image-actionpairs.|Wrist/MANO retargeting; downsampling.|Ego-videopre-training; few robot demos.|
|RynnVLA-001 [138]|(C)|12M egocentric + 244K robot videos; 798 demonstrations.|Keypoint filtering; Qwen2-VL captions.|Web ego-videopre-training; small teleopset.|
|EgoScaler [177]|(C)|45,157 egocentric episodes; 800 robot episodes.|GPT-4oparsing; BGTS/distance filters.|Annotation-free ego-video extraction.|
|Being-H0 [137]|(C)|150M+ samples; 1,000+ hours.|MANO alignment; GRQ tokens.|Hand-videophysical tuning.|
|EMMA [178]|(C)|3 tasks; 20–50 seed demos.|Depth/view/text filters; AdaMix.|Text-guided video variant synthesis.|
|Humanoid-VLA [149]|(C)|0.929M clips; 557.3M frames; 7,790 hours.|Mocap quality; self-supervision.|Self-supervised motion expansion.|
|AnyPos [141]|(D)|610Kpairs / 638 trajectories.|Uniform coverage; PPO feasibility.|10h autonomous exploration.|
|SimpleVLA-RL [13]|(D)|1–1000 demonstrations/task; simulation rollouts.|Binaryreward; dynamic sampling.|Simulation RL rolloutgeneration.|
|DiffusionRLVLA [179]|(D)|130 tasks; 50 trajectories/task.|Efficiency, smoothness, variance checks.|BC-warmed diffusion RL demos.|
|World-Env [180]|(D)|5 demonstrations/task + self-explored rollouts.|VLM reflector;|World-model virtual exploration.|
|VLA-RFT [181]|(D)|- 16 rollouts/update.|L1+LPIPS reward verification.|World-model reward rollouts.|
|LLaRA [17]|(E)|0.8K/8K/80K demonstrations + six auxiliarytasks.|Rules; GPT-4 rephrasing; oracle boxes.|Conversational/auxiliaryrelabeling.|
|InstructVLA [64]|(E)|650K annotated interactions.|GPT-4o/GT instruction; 95.4% success.|Automatic instruction annotation.|
|ReconVLA [182]|(E)|100K+ trajectories; 2M samples.|GroundingDINOgaze; recon/action loss.|Gaze reconstruction on open data.|
|ERMV [183]|(E)|_−_.|EMA-Attn/SST; expert mask correction.|4D sequence editing; selective masks.|


scarcity. Recent work shifts humans to high-level supervision to improve scalability. CLIP-RT [87] facilitates collection via natural language interfaces, yet still requires constant human presence. HiFi-UMI [184] improves robot-free UMI capture fidelity for deployable demonstrations. Moving toward greater autonomy, GCENT [173] employs a "guardian" strategy, where humans intervene only via rewind-andcorrection during failures. This selective intervention allows a single operator to manage multiple robots, significantly enhancing collection throughput. 

Further fidelity is achieved via real-anchored paradigms: ReBot [174] replays authentic trajectories in simulated scenes with real-background inpainting, while R2R2R [175] converts human videos into 3D assets to track complex trajectories. Alternatively, RealMirror [176] bridges the gap online by integrating WebXR teleoperation with physicsfiltered simulation. Together, these methods transition from pure synthesis to reality-grounded pipelines, enabling the scale required for robust VLA training. 

### **5.3 Internet-Scale and Cross-Domain Data Utilization** 

### **5.2 Simulation Data Collection** 

Human-in-the-loop optimizations improve efficiency but still yield limited, homogeneous data. In contrast, simulation enables automated, parallel generation of diverse largescale datasets across varied settings and embodiments at far lower cost. 

To bypass the constraints of physical collection, recent research leverages massively parallel simulation for data synthesis. GraspVLA [140], GeRM [93], and cVLA [147] utilize modular experts, pre-trained policies, or privileged analytical models to generate billion-frame or multi-modal datasets autonomously. InternData-A1 [66] extends this idea to generalist pre-training with high-fidelity synthetic trajectories across skills, scenes, and embodiments. Advancing this, RoboTwin 2.0 [16] employs a code-generation agent for closed-loop task synthesis and robot-specific motion planning. DynamicVLA [117] further targets dynamic-object manipulation through automatic synthetic collection plus a small non-teleoperated real set. To mitigate the sim-toreal gap, these works employ domain randomization and photorealistic rendering. 

Recent work leverages internet-scale robot and egocentric video data to reduce sim-to-real gaps and dataset costs. SmolVLA [20] shows that standardizing noisy multi-source robot data with VLM-generated descriptions and viewpoint normalization enables state-of-the-art performance using much less data. 

Beyond robotic data, leveraging human egocentric videos offers a more abundant resource. EgoVLA [136] treats humans as a specific "embodiment," while RynnVLA001 [138] automates this acquisition through poseestimation-based curation. To bridge the embodiment gap, EgoScaler [177] and Being-H0 [137] extract 6-DoF trajectories and fine-grained hand poses to convert passive observations into actionable signals. RoboWheel [185] adds contactrich reconstruction and cross-embodiment retargeting to turn human videos into robotic supervision. Further, MimicDreamer [186] and DreamTransfer [178] employ diffusion models to synthesize photorealistic robot demonstrations from human videos, aiming to improve visual and kinematic alignment. Finally, HumanoidVLA [149] extends this scope to third-person videos by decomposing poses into 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

14 

structured tokens, further mitigating data scarcity through self-supervision. 

### **5.4 Self-Exploration Data Collection** 

Beyond passive data acquisition, autonomous exploration transforms data collection into a self-improving process. Initially, AnyPos [141] use RL to autonomously map the robot’s reachable workspace before task-specific learning. Building on this, SimpleVLA-RL [13] utilizes online RL to turn the VLA into a trajectory generator. To enhance exploration quality, Yang et al. [179] replace standard policies with diffusion models, generating synthetic data that improves over original demonstrations. To further reduce interaction costs, exploration is migrating toward virtual environments.RehearseVLA [161] leverages high-fidelity simulators for economic data augmentation; its generalizability is limited by predefined environments. Addressing this, VLA-RFT [181] learns a data-driven world model from offline data. This evolution shifts VLA training from passive accumulation to fully active, scalable generation. 

### **5.5 Data Augmentation** 

Data augmentation enhances VLA efficiency by maximizing the utility of existing trajectories through semantic, temporal, and visual transformations. Semantic enrichment methods, such as LLaRA [17] and InstructVLA [64], use LLMs ( _e.g.,_ GPT-4o) to automate hierarchical annotations and auxiliary tasks, preventing the degradation of pre-trained VLM capabilities. Similarly, RoboChemist [9] diversifies instructions and visual prompts, while ReconVLA [182] generates reconstruction objectives via automated region segmentation. 

Beyond semantics, augmentation targets state-space diversity and visual appearance. Seeing Realism from Simulation [187] narrows the visual gap of simulated trajectories via realistic video transfer while preserving task and action information. Finally, ERMV [183] manipulates the visual modality by propagating targeted frame edits across 4D sequences using motion-aware attention, synthesizing new training views without requiring new physical demonstrations. 

### **5.6 Discussion** 

### _5.6.1 Innovations_ 

Efficient data collection for VLAs is moving from one-toone teleoperation toward reusable data engines that combine human supervision, simulation, cross-domain videos, autonomous exploration, and augmentation. Human-in-theloop systems reduce expert burden by replacing continuous teleoperation with language-conditioned interaction or selective rewind-and-refine correction [87], [173]. Simulationbased pipelines then scale collection through parallel expert generation, code-driven task synthesis, and robot-specific motion planning [16], [93], [140], [147], while real-anchored pipelines use real trajectories, human videos, or online teleoperation to improve visual and physical fidelity [174], [175], [176]. A complementary line standardizes heterogeneous robot data or converts human and egocentric videos into action-relevant supervision [20], [136], [137], [138], 

[149], [177], [186]. Finally, self-exploration and augmentation close the loop by collecting new trajectories from policy interaction and enriching existing data with semantic, spatial, temporal, or visual transformations [17], [64], [141], [179], [183]. 

### _5.6.2 Limitations, Challenges and Future Works_ 

Despite these advances, data acquisition remains constrained by a fundamental fidelity-scalability trade-off. Realworld demonstrations offer high-fidelity physical grounding at prohibitive costs, whereas scalable synthetic and video datasets suffer from domain shifts across embodiments, contact dynamics, and viewpoints [16], [41], [52], [65], [187], [188]. While internet and egocentric videos mitigate data scarcity, their absence of force, proprioception, and actionable annotations introduces kinematic ambiguities that generative datasets cannot fully resolve [136], [137], [149], [177], [186]. Additionally, autonomous exploration introduces a safety-efficiency dilemma: maximizing state coverage risks hardware collisions and noisy reward signals, which degrade policy optimization [13], [141], [179]. 

Therefore, future research must prioritize robust data infrastructures integrating standardized multimodal schemas, uncertainty-aware filtering, physics-grounded sim-to-real validation, and closed-loop engines that co-optimize collection efficiency, safety, and downstream policy performance [16], [173], [176], [187], [188]. 

## **6 APPLICATIONS** 

Efficiency bridges VLA intelligence and physical-world deployment. In latency-critical applications such as autonomous driving and mobile manipulation, **Efficient Model Design** reduces perception–reasoning–action overhead through compact architectures, token reduction, and fast decoding [5], [20], [91], [189], [190]. In data-scarce applications such as household and industrial robotics, **Efficient Training** adapts pretrained VLAs to new tasks and embodiments with lower tuning cost [151], [153], [170]. When openworld deployment must cover diverse tasks, embodiments, and environments, **Efficient Data Collection** reduces costly teleoperation by expanding reusable supervision through standardized datasets, simulation, egocentric videos, selfexploration, and generative augmentation [16], [41], [136], [140], [141]. We therefore select several representative application directions for more detailed discussion. 

### **6.1 Intelligent Vehicles and Autonomous Driving** 

Autonomous driving uses VLAs to map multimodal traffic observations and high-level intent into trajectories or control actions. The central efficiency constraint is real-time reasoning under onboard compute limits, where dense scenes and long-tail hazards leave little tolerance for slow deliberation or unstable action decoding [5], [189], [190]. Recent methods address this through adaptive reasoning and reinforcement fine-tuning [189], [191], diffusion-based planning [192], token pruning [5], and masked VLA diffusion for efficient and explainable planning [190]. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

15 

### **6.2 Mobile Manipulation and Smart Home** 

Mobile manipulation and smart-home robotics require VLAs to navigate indoor spaces, manipulate objects, and follow open-vocabulary instructions. Efficiency is limited by edge deployment, privacy-preserving inference, longhorizon base-arm coordination, and sparse household demonstrations [94]. Recent work responds with compact VLA backbones and asynchronous inference [20], faster edge-oriented action decoding [91], transfer to mobile manipulation [151], and spatially grounded training with depth, multi-view, and temporal supervision [193]. 

### **6.3 Industrial Manufacturing and Logistics** 

Industrial manufacturing and logistics involve VLA-based manipulation, inspection, assembly, disassembly, process control, and warehouse operation. The efficiency challenge shifts from single-task success to throughput, continuousrun reliability, precision placement, and contact-rich control [194], [195], [196]. Recent studies evaluate VLA transfer under industrial constraints [194], use hybrid reasoning for adaptive manufacturing perception and process control [7], add explicit skills for contact-rich disassembly [195], and report on-device humanoid logistics with productivity and reliability metrics [196]. 

### **6.4 Human-Robot Collaboration in Medical Assistance** 

Human-robot collaboration and medical assistance require VLAs to infer intent, support context-aware multimodal interaction [197], and execute assistive actions such as tool handover or surgical support. Their efficiency bottlenecks include real-time interaction, limited user-specific data, and safety-critical recovery [8], [198]. Recent work studies realtime surgical instrument handover [8] and reflective collaboration with mixture-of-experts action generation [198]. 

## **7 CONCLUSION** 

This survey systematically charts the emergent field of **Efficient VLAs** , providing the first unified taxonomy focusing on the model-training-data loop to consolidate the fragmented efforts addressing their prohibitive computational and data bottlenecks. We demonstrate that current solutions converge upon three interdependent pillars, including **Efficient Model Design** , **Efficient Training** , and **Efficient Data Collection** . Our synthesis uncovers the intrinsic trade-offs between model compactness and multimodal expressivity, providing a structured perspective for understanding the design tensions that characterize this space. The challenges and future directions delineated are a direct consequence of this synthesis, charting a necessary roadmap that moves beyond isolated optimizations toward adaptive, co-designed systems. This work thus serves to support this transition, contributing to the development from resource-bound prototypes toward deployable physical-world intelligence. 

## **REFERENCES** 

- [1] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong _et al._ , “Openvla: An open-source vision-language-action model,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 2679–2713. 

- [2] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A visionlanguage-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [3] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

- [4] Q. Li, Y. Liang, Z. Wang, L. Luo, X. Chen, M. Liao, F. Wei, Y. Deng, S. Xu, Y. Zhang _et al._ , “Cogact: A foundational visionlanguage-action model for synergizing cognition and action in robotic manipulation,” _arXiv preprint arXiv:2411.19650_ , 2024. 

- [5] J. Cao, Q. Zhang, P. Jia, X. Zhao, B. Lan, X. Zhang, X. Wei, S. Chen, L. Li, X. Liu _et al._ , “Fastdrivevla: Efficient end-to-end driving via plug-and-play reconstruction-based token pruning,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 40, no. 4, 2026, pp. 2571–2579. 

- [6] X. Zhou, X. Han, F. Yang, Y. Ma, V. Tresp, and A. Knoll, “Opendrivevla: Towards end-to-end autonomous driving with large vision language action model,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 40, no. 16, 2026, pp. 13 782– 13 790. 

- [7] C. Margadji and S. W. Pattinson, “Hybrid reasoning for perception, explanation, and autonomous action in manufacturing,” _Nature Communications_ , 2026. 

- [8] S. Li, J. Wang, R. Dai, W. Ma, W. Y. Ng, Y. Hu, and Z. Li, “Robonurse-vla: Robotic scrub nurse system based on visionlanguage-action model,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2025, pp. 3986– 3993. 

- [9] Z. Zhang, C. Yue, H. Xu, M. Liao, X. Qi, H.-a. Gao, Z. Wang, and H. Zhao, “Robochemist: Long-horizon and safety-compliant robotic chemical experimentation,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 3537–3568. 

- [10] L. Beyer, A. Steiner, A. S. Pinto, A. Kolesnikov, X. Wang, D. Salz, M. Neumann, I. Alabdulmohsin, M. Tschannen, E. Bugliarello _et al._ , “Paligemma: A versatile 3b vlm for transfer,” _arXiv preprint arXiv:2407.07726_ , 2024. 

- [11] S. Karamcheti, S. Nair, A. Balakrishna, P. Liang, T. Kollar, and D. Sadigh, “Prismatic vlms: investigating the design space of visually-conditioned language models,” in _Proceedings of the 41st International Conference on Machine Learning_ , 2024, pp. 23 123– 23 144. 

- [12] J. Bjorck, F. Castañeda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang _et al._ , “Gr00t n1: An open foundation model for generalist humanoid robots,” _arXiv preprint arXiv:2503.14734_ , 2025. 

- [13] H. Li, Y. Zuo, J. Yu, Y. Zhang, Y. Zhaohui, K. Zhang, X. Zhu, Y. Zhang, T. Chen, G. Cui _et al._ , “Simplevla-rl: Scaling vla training via reinforcement learning,” in _International Conference on Learning Representations_ , vol. 2026, 2026, pp. 125 846–125 869. 

- [14] M. J. Kim, C. Finn, and P. Liang, “Fine-tuning vision-languageaction models: Optimizing speed and success,” _arXiv preprint arXiv:2502.19645_ , 2025. 

- [15] Q. Bu, J. Cai, L. Chen, X. Cui, Y. Ding, S. Feng, S. Gao, X. He, X. Hu, X. Huang _et al._ , “Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems,” _arXiv preprint arXiv:2503.06669_ , 2025. 

- [16] T. Chen, Z. Chen, B. Chen, Z. Cai, Y. Liu, Z. Li, Q. Liang, X. Lin, Y. Ge, Z. Gu _et al._ , “Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation,” _arXiv preprint arXiv:2506.18088_ , 2025. 

- [17] X. Li, C. Mata, J. Park, K. Kahatapitiya, Y. S. Jang, J. Shang, K. Ranasinghe, R. D. Burgert, M. Cai, Y. J. Lee _et al._ , “Llara: Supercharging robot learning data for vision-language policy,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [18] R. Zhang, M. Dong, Y. Zhang, L. Heng, X. Chi, G. Dai, L. Du, D. Wang, Y. Du, and S. Zhang, “Mole-vla: Dynamic layerskipping vision language action model via mixture-of-layers for efficient robot manipulation,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 40, no. 22, 2026, pp. 18 764– 18 772. 

- [19] J. Liu, M. Liu, Z. Wang, P. An, X. Li, K. Zhou, S. Yang, R. Zhang, Y. Guo, and S. Zhang, “Robomamba: Efficient vision-languageaction model for robotic reasoning and manipulation,” _Advances_ 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

16 

- _in Neural Information Processing Systems_ , vol. 37, pp. 40 085–40 110, 2024. 

- [20] M. Shukor, D. Aubakirova, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, C. Pascal, M. Russi, A. Marafioti _et al._ , “Smolvla: A vision-language-action model for affordable and efficient robotics,” _arXiv preprint arXiv:2506.01844_ , 2025. 

- [21] K. Pertsch, K. Stachowicz, B. Ichter, D. Driess, S. Nair, Q. Vuong, O. Mees, C. Finn, and S. Levine, “Fast: Efficient action tokenization for vision-language-action models,” _arXiv preprint arXiv:2501.09747_ , 2025. 

- [22] Y. Yang, Y. Wang, Z. Wen, L. Zhongwei, C. Zou, Z. Zhang, C. Wen, and L. Zhang, “Efficientvla: Training-free acceleration and compression for vision-language-action models,” _Advances in Neural Information Processing Systems_ , vol. 38, pp. 40 891–40 914, 2026. 

- [23] Y. Ma, Z. Song, Y. Zhuang, J. Hao, and I. King, “A survey on vision–language–action models for embodied ai,” _IEEE Transactions on Neural Networks and Learning Systems_ , 2026. 

- [24] M. U. Din, W. Akram, L. S. Saoud, J. Rosell, and I. Hussain, “Vision language action models in robotic manipulation: A systematic review,” _arXiv preprint arXiv:2507.10672_ , 2025. 

- [25] D. Zhang, J. Sun, C. Hu, X. Wu, Z. Yuan, R. Zhou, F. Shen, and Q. Zhou, “Pure vision language action (vla) models: A comprehensive survey,” _arXiv preprint arXiv:2509.19012_ , 2025. 

- [26] R. Shao, W. Li, L. Zhang, R. Zhang, Z. Liu, R. Chen, and L. Nie, “Large vlm-based vision-language-action models for robotic manipulation: A survey,” _arXiv preprint arXiv:2508.13073_ , 2025. 

- [27] Y. Zhong, F. Bai, S. Cai, X. Huang, Z. Chen, X. Zhang, Y. Wang, S. Guo, T. Guan, K. N. Lui _et al._ , “A survey on vision-languageaction models: An action tokenization perspective,” _arXiv preprint arXiv:2507.01925_ , 2025. 

- [28] T.-Y. Xiang, A.-Q. Jin, X.-H. Zhou, M.-J. Gui, X.-L. Xie, S.-Q. Liu, S.-Y. Wang, S.-B. Duan, F.-C. Xie, W.-K. Wang _et al._ , “Parallels between vla model post-training and human motor learning: Progress, challenges, and trends,” _arXiv preprint arXiv:2506.20966_ , 2025. 

- [29] A. Dosovitskiy, L. Beyer, A. Kolesnikov, D. Weissenborn, X. Zhai, T. Unterthiner, M. Dehghani, M. Minderer, G. Heigold, S. Gelly _et al._ , “An image is worth 16x16 words: Transformers for image recognition at scale,” in _International Conference on Learning Representations_ , 2020. 

- [30] X. Zhai, B. Mustafa, A. Kolesnikov, and L. Beyer, “Sigmoid loss for language image pre-training,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2023, pp. 11 975–11 986. 

- [31] M. Oquab, T. Darcet, T. Moutakanni, H. Vo, M. Szafraniec, V. Khalidov, P. Fernandez, D. Haziza, F. Massa, A. El-Nouby _et al._ , “Dinov2: Learning robust visual features without supervision,” _Transactions on Machine Learning Research Journal_ , 2024. 

- [32] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark _et al._ , “Learning transferable visual models from natural language supervision,” in _International conference on machine learning_ . PmLR, 2021, pp. 8748–8763. 

- [33] J. Bai, S. Bai, Y. Chu, Z. Cui, K. Dang, X. Deng, Y. Fan, W. Ge, Y. Han, F. Huang _et al._ , “Qwen technical report,” _arXiv preprint arXiv:2309.16609_ , 2023. 

- [34] A. Chowdhery, S. Narang, J. Devlin, M. Bosma, G. Mishra, A. Roberts, P. Barham, H. W. Chung, C. Sutton, S. Gehrmann _et al._ , “Palm: Scaling language modeling with pathways,” _Journal of Machine Learning Research_ , vol. 24, no. 240, pp. 1–113, 2023. 

- [35] G. Team, T. Mesnard, C. Hardin, R. Dadashi, S. Bhupatiraju, S. Pathak, L. Sifre, M. Rivière, M. S. Kale, J. Love _et al._ , “Gemma: Open models based on gemini research and technology,” _arXiv preprint arXiv:2403.08295_ , 2024. 

- [36] H. Touvron, L. Martin, K. Stone, P. Albert, A. Almahairi, Y. Babaei, N. Bashlykov, S. Batra, P. Bhargava, S. Bhosale _et al._ , “Llama 2: Open foundation and fine-tuned chat models,” _arXiv preprint arXiv:2307.09288_ , 2023. 

- [37] A. Gu and T. Dao, “Mamba: Linear-time sequence modeling with selective state spaces,” in _First Conference on Language Modeling_ , 2024. 

- [38] J. Ho, A. Jain, and P. Abbeel, “Denoising diffusion probabilistic models,” _Advances in neural information processing systems_ , vol. 33, pp. 6840–6851, 2020. 

- [39] W. Peebles and S. Xie, “Scalable diffusion models with transformers,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2023, pp. 4195–4205. 

- [40] Y. Lipman, R. T. Chen, H. Ben-Hamu, M. Nickel, and M. Le, “Flow matching for generative modeling,” in _The Eleventh International Conference on Learning Representations_ , 2023. 

- [41] A. O’Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain _et al._ , “Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 6892– 6903. 

- [42] S. Fan, Q. Yang, Y. Liu, K. Wu, Z. Che, Q. Liu, and M. Wan, “Diffusion trajectory-guided policy for long-horizon robot manipulation,” _IEEE Robotics and Automation Letters_ , 2025. 

- [43] S. Ye, J. Jang, B. Jeon, S. J. Joo, J. Yang, B. Peng, A. Mandlekar, R. Tan, Y.-W. Chao, B. Y. Lin _et al._ , “Latent action pretraining from videos,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [44] J. Zhang, Y. Guo, X. Chen, Y.-J. Wang, Y. Hu, C. Shi, and J. Chen, “Hirt: Enhancing robotic control with hierarchical robot transformers,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 933–946. 

- [45] J. Wen, Y. Zhu, J. Li, M. Zhu, Z. Tang, K. Wu, Z. Xu, N. Liu, R. Cheng, C. Shen _et al._ , “Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation,” _IEEE Robotics and Automation Letters_ , 2025. 

- [46] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, W. Chen _et al._ , “Lora: Low-rank adaptation of large language models.” _ICLR_ , vol. 1, no. 2, p. 3, 2022. 

- [47] G. Luo, Y. Zhou, M. Huang, T. Ren, X. Sun, and R. Ji, “Moil: Momentum imitation learning for efficient vision-language adaptation,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2024. 

- [48] J. Yu, Z. Huang, Y. Zhuge, L. Zhang, P. Hu, D. Wang, H. Lu, and Y. He, “Moe-adapters++: Towards more efficient continual learning of vision-language models via dynamic mixtureof-experts adapters,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2025. 

- [49] J. Zhang, J. Huang, S. Jin, and S. Lu, “Vision-language models for vision tasks: A survey,” _IEEE transactions on pattern analysis and machine intelligence_ , vol. 46, no. 8, pp. 5625–5644, 2024. 

- [50] L. Xu, H. Xie, S. J. Qin, X. Tao, and F. L. Wang, “Parameterefficient fine-tuning methods for pretrained language models: A critical review and assessment,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2026. 

- [51] H. Zhang, P. Zeng, L. Cao, W. Lai, J. Li, D. Peng, Y. Bin, X. Wang, J. Zhang, J. Song _et al._ , “A survey on post-training of multimodal large language models,” 2026. 

- [52] H. R. Walke, K. Black, T. Z. Zhao, Q. Vuong, C. Zheng, P. HansenEstruch, A. W. He, V. Myers, M. J. Kim, M. Du _et al._ , “Bridgedata v2: A dataset for robot learning at scale,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 1723–1736. 

- [53] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis _et al._ , “Droid: A large-scale in-the-wild robot manipulation dataset,” in _RSS 2024 Workshop: Data Generation for Robotics_ , 2024. 

- [54] S. James, Z. Ma, D. R. Arrojo, and A. J. Davison, “Rlbench: The robot learning benchmark & learning environment,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 2, pp. 3019–3026, 2020. 

- [55] S. Nasiriany, A. Maddukuri, L. Zhang, A. Parikh, A. Lo, A. Joshi, A. Mandlekar, and Y. Zhu, “Robocasa: Large-scale simulation of everyday tasks for generalist robots,” in _RSS 2024 Workshop: Data Generation for Robotics_ , 2024. 

- [56] Y. Wang, Z. Xian, F. Chen, T.-H. Wang, Y. Wang, K. Fragkiadaki, Z. Erickson, D. Held, and C. Gan, “Robogen: towards unleashing infinite data for automated robot learning via generative simulation,” in _Proceedings of the 41st International Conference on Machine Learning_ , 2024, pp. 51 936–51 983. 

- [57] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “Libero: Benchmarking knowledge transfer for lifelong robot learning,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 44 776–44 791, 2023. 

- [58] L. X. Shi, M. R. Equi, L. Ke, K. Pertsch, Q. Vuong, J. Tanner, A. Walling, H. Wang, N. Fusai, A. Li-Bell _et al._ , “Hi robot: Openended instruction following with hierarchical vision-languageaction models,” in _Forty-second International Conference on Machine Learning_ , 2025. 

- [59] D. Driess, F. Xia, M. S. Sajjadi, C. Lynch, A. Chowdhery, B. Ichter, A. Wahid, J. Tompson, Q. Vuong, T. Yu _et al._ , “Palm-e: An em- 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

17 

- bodied multimodal language model,” in _International Conference on Machine Learning_ . PMLR, 2023, pp. 8469–8488. 

- [60] X. Chen, J. Djolonga, P. Padlewski, B. Mustafa, S. Changpinyo, J. Wu, C. R. Ruiz, S. Goodman, X. Wang, Y. Tay _et al._ , “Pali-x: On scaling up a multilingual vision and language model,” _arXiv preprint arXiv:2305.18565_ , 2023. 

- [61] S. Xu, Y. Wang, C. Xia, D. Zhu, T. Huang, and C. Xu, “Vla-cache: Efficient vision-language-action manipulation via adaptive token caching,” _Advances in Neural Information Processing Systems_ , vol. 38, pp. 164 448–164 473, 2026. 

- [62] H. Wang, J. Xu, J. Pan, Y. Zhou, and G. Dai, “Specprune-vla: Accelerating vision-language-action models via action-aware selfspeculative pruning,” _arXiv preprint arXiv:2509.05614_ , 2025. 

- [63] Y. Guo, Y. Ma, H. Sun, Z. Guan, S. Di, J. Long, W. Xu, X. Bai, W. Huang, Y. Guo _et al._ , “Thousand-gpu large-scale training and optimization recipe for ai-native cloud embodied intelligence infrastructure,” _arXiv preprint arXiv:2603.11101_ , 2026. 

- [64] S. Yang, H. Li, B. Wang, Y. Chen, Y. Tian, T. Wang, H. Wang, F. Zhao, Y. Liao, and J. Pang, “Vision-language-action instruction tuning: From understanding to manipulation,” in _International Conference on Learning Representations_ , vol. 2026, 2026, pp. 152 896–152 943. 

- [65] W. Wu, F. Lu, Y. Wang, S. Yang, S. Liu, F. Wang, Q. Zhu, H. Sun, Y. Wang, S. Ma _et al._ , “A pragmatic vla foundation model,” _arXiv preprint arXiv:2601.18692_ , 2026. 

- [66] Y. Tian, Y. Yang, Y. Xie, Z. Cai, X. Shi, N. Gao, H. Liu, X. Jiang, Z. Qiu, F. Yuan _et al._ , “Interndata-a1: Pioneering high-fidelity synthetic data for pre-training generalist policy,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2026, pp. 976–985. 

- [67] R. A. Jacobs, M. I. Jordan, S. J. Nowlan, and G. E. Hinton, “Adaptive mixtures of local experts,” _Neural computation_ , vol. 3, no. 1, pp. 79–87, 1991. 

- [68] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin, “Attention is all you need,” _Advances in neural information processing systems_ , vol. 30, 2017. 

- [69] I. Leal, K. Choromanski, D. Jain, A. Dubey, J. Varley, M. Ryoo, Y. Lu, F. Liu, V. Sindhwani, Q. Vuong _et al._ , “Sara-rt: Scaling up robotics transformers with self-adaptive robust attention,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 6920–6927. 

- [70] Y. Fan, S. Bai, X. Tong, P. Ding, Y. Zhu, H. Lu, F. Dai, W. Zhao, Y. Liu, S. Huang _et al._ , “Long-vla: Unleashing long-horizon capability of vision language action model for robot manipulation,” in _9th Annual Conference on Robot Learning_ , 2025. 

- [71] J. Wen, M. Zhu, J. Liu, Z. Liu, Y. Yang, L. Zhang, S. Zhang, Y. Zhu, and Y. Xu, “dvla: Diffusion vision-language-action model with multimodal chain-of-thought,” _arXiv preprint arXiv:2509.25681_ , 2025. 

- [72] J. Koo, T. Cho, H. Kang, E. Pyo, T. G. Oh, T. Kim, and A. J. Choi, “Retovla: Reusing register tokens for spatial reasoning in visionlanguage-action models,” _arXiv preprint arXiv:2509.21243_ , 2025. 

- [73] W. Xu and L. Zhuang, “Kv-efficient vla: A method of speed up vision language model with rnn-gated chunked kv cache,” _arXiv preprint arXiv:2509.21354_ , 2025. 

- [74] X. Ma, Z. Yuan, Z. Zhang, K. Shi, L. Sun, and Y. Ye, “Blurr: A boosted low-resource inference for vision-language-action model,” in _Companion Proceedings of the ACM Web Conference 2026_ , 2026, pp. 225–228. 

- [75] Y. Guo and B. Liu, “Reflex: Real-time vla control through streaming inference,” _arXiv preprint arXiv:2607.14695_ , 2026. 

- [76] S. Wang, L. Wang, S. Zhou, J. Tian, J. Li, H. Sun, and W. Tang, “Flowram: Grounding flow matching policy with region-aware mamba framework for robotic manipulation,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 12 176–12 186. 

- [77] W. Song, J. Chen, P. Ding, H. Zhao, W. Zhao, Z. Zhong, Z. Ge, Z. Li, D. Wang, L. Wang _et al._ , “Pd-vla: Accelerating visionlanguage-action model integrated with action chunking via parallel decoding,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2025, pp. 13 162–13 169. 

- [78] J. Liu, H. Chen, P. An, Z. Liu, R. Zhang, C. Gu, X. Li, Z. Guo, S. Chen, M. Liu _et al._ , “Hybridvla: Collaborative diffusion and autoregression in a unified vision-language-action model,” _arXiv preprint arXiv:2503.10631_ , 2025. 

- [79] Y. Su, N. Liu, D. Chen, Z. Zhao, K. Wu, M. Li, Z. Xu, Z. Che, and J. Tang, “Freqpolicy: Efficient flow-based visuomotor policy via 

frequency consistency,” _Advances in Neural Information Processing Systems_ , vol. 38, pp. 27 769–27 797, 2026. 

- [80] W. Song, J. Chen, P. Ding, Y. Huang, H. Zhao, D. Wang, and H. Li, “Ceed-vla: Consistency vision-language-action model with earlyexit decoding,” _arXiv preprint arXiv:2506.13725_ , 2025. 

- [81] X. Chi, K. Ge, J. Liu, S. Zhou, P. Jia, Z. He, Y. Liu, T. Li, L. Han, S. Han _et al._ , “Mind: Learning a dual-system world model for real-time planning and implicit risk analysis,” _arXiv preprint arXiv:2506.18897_ , 2025. 

- [82] Y. Wang, H. Zhu, M. Liu, J. Yang, H.-S. Fang, and T. He, “Vqvla: Improving vision-language-action models via scaling vectorquantized action tokenizers,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2025, pp. 11 089–11 099. 

- [83] S. Wang, R. Yu, Z. Yuan, C. Yu, F. Gao, Y. Wang, and D. F. Wong, “Spec-vla: speculative decoding for vision-language-action models with relaxed acceptance,” in _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , 2025, pp. 26 916–26 928. 

- [84] W. Zheng, B. Li, B. Xu, E. Feng, J. Gu, and H. Chen, “Leveraging os-level primitives for robotic action management,” _arXiv preprint arXiv:2508.10259_ , 2025. 

- [85] D. Tarasov, A. Nikulin, I. Zisman, A. Klepach, L. Nikita, A. Polubarov, A. Derevyagin, and V. Kurenkov, “Nina: Normalizing flows in action. training vla models with normalizing flows,” in _NeurIPS 2025 Workshop on Embodied World Models for Decision Making_ , 2025. 

- [86] Z. Liang, Y. Li, T. Yang, C. Wu, S. Mao, L. Pei, X. Yang, J. Pang, Y. Mu, and P. Luo, “Discrete diffusion vla: Bringing discrete diffusion to action decoding in vision-language-action policies,” _arXiv preprint arXiv:2508.20072_ , 2025. 

- [87] G.-C. Kang, J. Kim, K. Shim, J. K. Lee, and B.-T. Zhang, “Cliprt: Learning language-conditioned robotic policies from natural language supervision,” _arXiv preprint arXiv:2411.00508_ , 2024. 

- [88] M. Samson, B. Muraccioli, and F. Kanehiro, “Scalable, trainingfree visual language robotics: a modular multi-model framework for consumer-grade gpus,” in _2025 IEEE/SICE International Symposium on System Integration (SII)_ . IEEE, 2025, pp. 193–198. 

- [89] C.-Y. Hung, Q. Sun, P. Hong, A. Zadeh, C. Li, U. Tan, N. Majumder, S. Poria _et al._ , “Nora: A small open-sourced generalist vision language action model for embodied tasks,” _arXiv preprint arXiv:2504.19854_ , 2025. 

- [90] Y. Li, Y. Meng, Z. Sun, K. Ji, C. Tang, J. Fan, X. Ma, S.-T. Xia, Z. Wang, and W. Zhu, “Sp-vla: A joint model scheduling and token pruning approach for vla model acceleration,” in _The Fourteenth International Conference on Learning Representations_ , 2025. 

- [91] P. Budzianowski, W. Maa, M. Freed, J. Mo, W. Hsiao, A. Xie, T. Młoduchowski, V. Tipnis, and B. Bolte, “Edgevla: Efficient vision-language-action models,” _arXiv preprint arXiv:2507.14049_ , 2025. 

- [92] S. Belkhale and D. Sadigh, “Minivla: A better vla with a smaller footprint,” 2024. [Online]. Available: https://github. com/Stanford-ILIAD/openvla-mini 

- [93] W. Song, H. Zhao, P. Ding, C. Cui, S. Lyu, Y. Fan, and D. Wang, “Germ: A generalist robotic model with mixture-of-experts for quadruped robot,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 11 879– 11 886. 

- [94] C. Miao, T. Chang, M. Wu, H. Xu, C. Li, M. Li, and X. Wang, “Fedvla: Federated vision-language-action learning with dual gating mixture-of-experts for robotic manipulation,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2025, pp. 6904–6913. 

- [95] Y. Bai, Z. Wang, Y. Liu, K. Luo, Y. Wen, M. Dai, W. Chen, Z. Chen, L. Liu, G. Li _et al._ , “Learning to see and act: Task-aware virtual view exploration for robotic manipulation,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2026, pp. 13 386–13 396. 

- [96] Q. Bu, H. Li, L. Chen, J. Cai, J. Zeng, H. Cui, M. Yao, and Y. Qiao, “Towards synergistic, generalized, and efficient dual-system for robotic manipulation,” _arXiv preprint arXiv:2410.08001_ , 2024. 

- [97] B. Han, J. Kim, and J. Jang, “A dual process vla: Efficient robotic manipulation leveraging vlm,” _arXiv preprint arXiv:2410.15549_ , 2024. 

- [98] Y. Li, Y. Deng, J. Zhang, J. Jang, M. Memmel, C. R. Garrett, F. Ramos, D. Fox, A. Li, A. Gupta _et al._ , “Hamster: Hierarchical action models for open-world robot manipulation,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

18 

- [99] H. Chen, J. Liu, C. Gu, Z. Liu, R. Zhang, X. Li, X. He, Y. Guo, C.-W. Fu, S. Zhang _et al._ , “Fast-in-slow: a dual-system vla model unifying fast manipulation within slow reasoning,” _Advances in Neural Information Processing Systems_ , vol. 38, pp. 98 049–98 083, 2026. 

- [100] Y. Chen, Y. Han, Y. Huang, and X. Li, “Rlrc: Reinforcement learning-based recovery for compressed vision-language-action models,” _IEEE Robotics and Automation Letters_ , 2026. 

- [101] M. Reuss, H. Zhou, M. Rühle, Ö. E. Ya˘gmurlu, F. Otto, and R. Lioutikov, “Flower: Democratizing generalist robot policies with efficient vision-language-flow models,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 3736–3761. 

- [102] S. Park, H. Kim, W. Jeon, J. Yang, B. Jeon, Y. Oh, and J. Choi, “Quantization-aware imitation-learning for resourceefficient robotic control,” _arXiv preprint arXiv:2412.01034_ , 2024. 

- [103] S. Park, H. Kim, S. Kim, W. Jeon, J. Yang, B. Jeon, Y. Oh, and J. Choi, “Saliency-aware quantized imitation learning for efficient robotic control,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2025, pp. 13 140–13 150. 

- [104] H. Wang, C. Xiong, R. Wang, and X. Chen, “Bitvla: 1-bit vision-language-action models for robotics manipulation,” _arXiv preprint arXiv:2506.07530_ , 2025. 

- [105] H. Fang, Y. Liu, Y. Du, L. Du, and H. Yang, “Sqap-vla: A synergistic quantization-aware pruning framework for high-performance vision-language-action models,” _arXiv preprint arXiv:2509.09090_ , 2025. 

- [106] X. Tan, Y. Yang, P. Ye, J. Zheng, B. Bai, X. Wang, J. Hao, and T. Chen, “Think twice, act once: Token-aware compression and action reuse for efficient inference in vision-language-action models,” _arXiv preprint arXiv:2505.21200_ , 2025. 

- [107] Z. Duan, Y. Zhang, S. Geng, G. Liu, J. Boedecker, and C. X. Lu, “Fast ecot: Efficient embodied chain-of-thought via thoughts reuse,” _arXiv preprint arXiv:2506.07639_ , 2025. 

- [108] H. Li, S. Yang, Y. Chen, X. Chen, X. Yang, Y. Tian, H. Wang, T. Wang, D. Lin, F. Zhao _et al._ , “Towards efficient and robust manipulation via multi-frame vision-language-action modeling,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 40, no. 22, 2026, pp. 18 388–18 396. 

- [109] J. Lin, A. Taherin, A. Akbari, A. Akbari, L. Lu, G. Chen, T. Padir, X. Yang, W. Chen, Y. Li _et al._ , “Vote: Vision-language-action optimization with trajectory ensemble voting,” _arXiv preprint arXiv:2507.05116_ , 2025. 

- [110] W. Li, R. Zhang, R. Shao, J. He, and L. Nie, “Cogvla: Cognitionaligned vision-language-action models via instruction-driven routing & sparsification,” _Advances in neural information processing systems_ , vol. 38, pp. 137 646–137 675, 2026. 

- [111] T. Jiang, X. Jiang, Y. Ma, X. Wen, B. Li, K. Zhan, P. Jia, Y. Liu, S. Sun, and X. Lang, “The better you learn, the smarter you prune: Towards efficient vision-language-action models via differentiable token pruning,” _arXiv preprint arXiv:2509.12594_ , 2025. 

- [112] X. Pei, Y. Chen, S. Xu, Y. Wang, Y. Shi, and C. Xu, “Action-aware dynamic pruning for efficient vision-language-action manipulation,” in _International Conference on Learning Representations_ , vol. 2026, 2026, pp. 10 832–10 851. 

- [113] R. Bendikas, D. Dijkman, M. Peschl, S. Haresh, and P. Mazzaglia, “Focusing on what matters: Object-agent-centric tokenization for vision language action models,” in _9th Annual Conference on Robot Learning_ , 2025. 

- [114] W. Li, R. Zhang, R. Shao, Z. Fang, K. Zhou, Z. Tian, and L. Nie, “Semanticvla: Semantic-aligned sparsification and enhancement for efficient robotic manipulation,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 40, no. 22, 2026, pp. 18 397– 18 405. 

- [115] Z. Wang, Z. Lin, R. Li, Y. Zhang, X. Yang, S. Mi, and X.-S. Wei, “Open-loop planning, closed-loop verification: Speculative verification for vla,” _arXiv preprint arXiv:2604.02965_ , 2026. 

- [116] T. Lin, Y. Zhong, Y. Du, J. Zhang, J. Liu, Y. Chen, E. Gu, Z. Liu, H. Cai, Y. Zou _et al._ , “Evo-1: Lightweight vision-language-action model with preserved semantic alignment,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2026, pp. 13 397–13 406. 

- [117] H. Xie, B. Wen, J. Zheng, Z. Chen, F. Hong, H. Diao, and Z. Liu, “Dynamicvla: A vision-language-action model for dynamic object manipulation,” _arXiv preprint arXiv:2601.22153_ , 2026. 

- [118] J. Wen, M. Zhu, Y. Zhu, Z. Tang, J. Li, Z. Zhou, C. Li, X. Liu, Y. Peng, C. Shen _et al._ , “Diffusion-vla: Generalizable and inter- 

   - pretable robot foundation model via self-generated reasoning,” _arXiv preprint arXiv:2412.03293_ , 2024. 

- [119] J. Williams, K. D. Gupta, R. George, and M. Sarkar, “Lite vla: Efficient vision-language-action control on cpu-bound edge robots,” in _2026 IEEE International Conference on Pervasive Computing and Communications Workshops and other Affiliated Events (PerCom Workshops)_ . IEEE, 2026, pp. 530–533. 

- [120] P. C. Wason and J. S. B. Evans, “Dual processes in reasoning?” _Cognition_ , vol. 3, no. 2, pp. 141–154, 1974. 

- [121] D. Kahneman, _Thinking, fast and slow_ . macmillan, 2011. 

- [122] T. Zou, H. Zeng, Y. Nong, Y. Li, K. Liu, H. Yang, X. Ling, X. Li, and L. Ma, “Asynchronous fast-slow vision-languageaction policies for whole-body robotic manipulation,” _arXiv preprint arXiv:2512.20188_ , 2025. 

- [123] S. Yan, G. Wang, Q. Liu, W. Meng, J. Yang, C. Yao, F. Feng, X. Ma, Y. Zhao, and Y. Han, “Acting while understanding: Asynchronous semantic-action decoupling for real-time visionlanguage-action models,” _arXiv preprint arXiv:2606.15285_ , 2026. 

- [124] L. Sun, Z. Guan, C. Wang, Z. Chen, J. Yu, Z. Li, B. He, T. Sun, J. Cao, and L. Liu, “Unifs: Unified fast-to-slow hierarchical architecture for vision-language-action models,” _arXiv preprint arXiv:2606.22794_ , 2026. 

- [125] Y. Wu, H. Wang, Z. Chen, J. Pang, and D. Xu, “On-device diffusion transformer policy for efficient robot manipulation,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2025, pp. 14 073–14 083. 

- [126] Y. Yue, Y. Wang, B. Kang, Y. Han, S. Wang, S. Song, J. Feng, and G. Huang, “Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 56 619–56 643, 2024. 

- [127] Z. Yang, Y. Qi, T. Xie, B. Yu, S. Liu, and M. Li, “Dysl-vla: Efficient vision-language-action model inference via dynamicstatic layer-skipping for robot manipulation,” _arXiv preprint arXiv:2602.22896_ , 2026. 

- [128] Y. Xu, Y. Yang, Z. Fan, Y. Liu, Y. Li, B. Li, and Z. Zhang, “Qvla: Not all channels are equal in vision-language-action model’s quantization,” _arXiv preprint arXiv:2602.03782_ , 2026. 

- [129] J. Zhang, Y. Hsieh, Z. Wan, H. Lin, X. Wang, Z. Wang, Y. Lei, and M. Zhang, “Quantvla: Scale-calibrated post-training quantization for vision-language-action models,” _arXiv preprint arXiv:2602.20309_ , 2026. 

- [130] J. Gao, F. Ye, J. Zhang, and W. Qian, “Compressor-vla: Instructionguided visual token compression for efficient robotic manipulation,” _arXiv preprint arXiv:2511.18950_ , 2025. 

- [131] Z. Liu, Y. Chen, H. Cai, T. Lin, S. Yang, Z. Liu, and B. Zhao, “Bridging the semantic-action gap in visual token pruning for efficient vla inference,” _arXiv preprint arXiv:2511.16449_ , 2025. 

- [132] Y. Ye, J. Ma, J. Cen, and Z. Lu, “Token expand-merge: Trainingfree token compression for vision-language-action models,” _IEEE Robotics and Automation Letters_ , 2026. 

- [133] W. Qiu, H. Lei, T. Huang, and R. Ying, “Efficient long-horizon vision-language-action models via static-dynamic disentanglement,” _arXiv preprint arXiv:2602.03983_ , 2026. 

- [134] Q. Bu, Y. Yang, J. Cai, S. Gao, G. Ren, M. Yao, P. Luo, and H. Li, “Univla: Learning to act anywhere with task-centric latent actions,” _arXiv preprint arXiv:2505.06111_ , 2025. 

- [135] B. Tharwat, Y. Nasser, A. Abouzeid, and I. Reid, “Latent action pretraining through world modeling,” _arXiv preprint arXiv:2509.18428_ , 2025. 

- [136] R. Yang, Q. Yu, Y. Wu, R. Yan, B. Li, A.-C. Cheng, X. Zou, Y. Fang, X. Cheng, R.-Z. Qiu _et al._ , “Egovla: Learning vision-languageaction models from egocentric human videos,” _arXiv preprint arXiv:2507.12440_ , 2025. 

- [137] H. Luo, Y. Feng, W. Zhang, S. Zheng, Y. Wang, H. Yuan, J. Liu, C. Xu, Q. Jin, and Z. Lu, “Being-h0: vision-languageaction pretraining from large-scale human videos,” _arXiv preprint arXiv:2507.15597_ , 2025. 

- [138] Y. Jiang, S. Huang, S. Xue, Y. Zhao, J. Cen, S. Leng, K. Li, J. Guo, K. Wang, M. Chen _et al._ , “Rynnvla-001: Using human demonstrations to improve robot manipulation,” _arXiv preprint arXiv:2509.15212_ , 2025. 

- [139] Y. Wang, X. Li, W. Wang, J. Zhang, Y. Li, Y. Chen, X. Wang, and Z. Zhang, “Unified vision-language-action model,” in _International Conference on Learning Representations_ , vol. 2026, 2026, pp. 80 929–80 944. 

- [140] S. Deng, M. Yan, S. Wei, H. Ma, Y. Yang, J. Chen, Z. Zhang, T. Yang, X. Zhang, H. Cui _et al._ , “Graspvla: a grasping founda- 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

19 

   - tion model pre-trained on billion-scale synthetic action data,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 1004–1029. 

- [141] H. Tan, Y. Feng, X. Mao, S. Huang, G. Liu, Z. Hao, H. Su, and J. Zhu, “Anypos: Automated task-agnostic actions for bimanual manipulation,” _arXiv preprint arXiv:2507.12768_ , 2025. 

- [142] H. Im, E. Jeong, A. Kolobov, J. Fu, and Y. Lee, “Twinvla: Dataefficient bimanual manipulation with twin single-arm visionlanguage-action models,” in _International Conference on Learning Representations_ , vol. 2026, 2026, pp. 61 969–61 995. 

- [143] J. Jiang, J. Zhang, Z. Yin, R. Chen, S. Wang, Z. Yu, P. Zeng, X. Cao, X. Wang, J. Song _et al._ , “Wsa _1: a 3d-centric world-spatialaction model for generalizable robot control,” _arXiv preprint arXiv:2607.03941_ , 2026. 

- [144] A. Van Den Oord, O. Vinyals _et al._ , “Neural discrete representation learning,” _Advances in neural information processing systems_ , vol. 30, 2017. 

- [145] Y. Zhang, K. Ji, Y. Zou, R. Xu, F. Zheng, and L. Cheng, “Invertible neural network adapter for one-step flow matching in robot manipulation,” _arXiv preprint arXiv:2606.19194_ , 2026. 

- [146] Y. Wang, P. Ding, L. Li, C. Cui, Z. Ge, X. Tong, W. Song, H. Zhao, W. Zhao, P. Hou _et al._ , “Vla-adapter: An effective paradigm for tiny-scale vision-language-action model,” in _Proceedings of the AAAI conference on artificial intelligence_ , vol. 40, no. 22, 2026, pp. 18 638–18 646. 

- [147] M. Argus, J. Bratuli´c, H. Masnavi, M. Velikanov, N. Heppert, A. Valada, and T. Brox, “cvla: Towards efficient camera-space vlas,” in _CoRL 2025 Workshop RemembeRL_ , 2025. 

- [148] Y. Dai, A. Keyser, and D. P. Losey, “Prepare before you act: Learning from humans to rearrange initial states,” _arXiv preprint arXiv:2509.18043_ , 2025. 

- [149] P. Ding, J. Ma, X. Tong, B. Zou, X. Luo, Y. Fan, T. Wang, H. Lu, P. Mo, J. Liu _et al._ , “Humanoid-vla: Towards universal humanoid control with visual integration,” _arXiv preprint arXiv:2502.14795_ , 2025. 

- [150] D. Li, B. Peng, C. Li, N. Qiao, Q. Zheng, L. Sun, Y. Qin, B. Li, Y. Luan, B. Wu _et al._ , “An atomic skill library construction method for data-efficient embodied manipulation,” _arXiv preprint arXiv:2501.15068_ , 2025. 

- [151] Z. Wu, Y. Zhou, X. Xu, Z. Wang, and H. Yan, “Momanipvla: Transferring vision-language-action models for general mobile manipulation,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 1714–1723. 

- [152] C. Cui, P. Ding, W. Song, S. Bai, X. Tong, Z. Ge, R. Suo, W. Zhou, Y. Liu, B. Jia _et al._ , “Openhelix: A short survey, empirical analysis, and open-source dual-system vla model for robotic manipulation,” _arXiv preprint arXiv:2505.03912_ , 2025. 

- [153] P. Li, Y. Wu, Z. Xi, W. Li, Y. Huang, Z. Zhang, Y. Chen, J. Wang, S.C. Zhu, T. Liu _et al._ , “Controlvla: Few-shot object-centric adaptation for pre-trained vision-language-action models,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 1898–1913. 

- [154] K. Sridhar, S. Dutta, D. Jayaraman, and I. Lee, “Ricl: Adding incontext adaptability to pre-trained vision-language-action models,” in _9th Annual Conference on Robot Learning_ , 2025. 

- [155] Y. Zhang, C. Wang, Y. Zhao, Y. Ge, Z. Sun, X. Li, C. Zhang, C. Bai, X. Li _et al._ , “Align-then-steer: Adapting the vision-language action models through unified latent guidance,” in _International Conference on Learning Representations_ , vol. 2026, 2026, pp. 14 717– 14 749. 

- [156] T. Jülg, W. Burgard, and F. Walter, “Refined policy distillation: From vla generalists to rl experts,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2025, pp. 11 677–11 684. 

- [157] S. Tan, K. Dou, Y. Zhao, and P. Kraehenbuehl, “Interactive posttraining for vision-language-action models,” in _Workshop on Foundation Models Meet Embodied Agents at CVPR 2025_ , 2025. 

- [158] G. Lu, W. Guo, C. Zhang, Y. Zhou, H. Jiang, Z. Gao, Y. Tang, and Z. Wang, “Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning,” _arXiv preprint arXiv:2505.18719_ , 2025. 

- [159] D. Huang, Z. Fang, T. Zhang, Y. Li, L. Zhao, and C. Xia, “Co-rft: Efficient fine-tuning of vision-language-action models through chunked offline reinforcement learning,” _arXiv preprint arXiv:2508.02219_ , 2025. 

- [160] H. Zhang, S. Zhang, J. Jin, Q. Zeng, Y. Qiao, H. Lu, and D. Wang, “Balancing signal and variance: Adaptive offline rl post-training for vla flow models,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 40, no. 22, 2026, pp. 18 755–18 763. 

- [161] J. Xiao, Y. Yang, X. Chang, R. Chen, F. Xiong, M. Xu, W.-S. Zheng, and Q. Zhang, “Rehearsevla: Simulated post-training for vlas with physically-consistent world model,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2026, pp. 20 867–20 877. 

- [162] J. Wen, Y. Zhu, J. Li, Z. Tang, C. Shen, and F. Feng, “Dexvla: Vision-language model with plug-in diffusion expert for general robot control,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 3094–3114. 

- [163] J. Zheng, T. Ma, Y. Fan, Z. Wang, S. Yang, and J. Liang, “Motionwam: Towards foundation world action models for real-time humanoid loco-manipulation,” _arXiv preprint arXiv:2606.09215_ , 2026. 

- [164] A. Y. A. Omaisan and I. S. Mohamed, “Towards accessible physical ai: Lora-based fine-tuning of vla models for real-world robot control,” _arXiv preprint arXiv:2512.11921_ , 2025. 

- [165] D. Kim, M. Bae, U. Nam, G. Kim, S. Lee, K. Shim, and B. Shim, “Adaptive capacity allocation for vision language action finetuning,” _arXiv preprint arXiv:2603.07404_ , 2026. 

- [166] C. Xu, J. T. Springenberg, M. Equi, A. Amin, A. Esmail, S. Levine, and L. Ke, “Rl token: Bootstrapping online rl with visionlanguage-action models,” _arXiv preprint arXiv:2604.23073_ , 2026. 

- [167] P. Jin, Q. Wang, G. Sun, Z. Cai, P. He, and Y. You, “Dual-actor fine-tuning of vla models: A talk-and-tweak human-in-the-loop approach,” _arXiv preprint arXiv:2509.13774_ , 2025. 

- [168] Y. Chen, S. Tian, S. Liu, Y. Zhou, H. Li, and D. Zhao, “Conrft: A reinforced fine-tuning method for vla models via consistency policy,” _arXiv preprint arXiv:2502.05450_ , 2025. 

- [169] M. Nakamoto, S. Zhai, A. Singh, M. Sobol Mark, Y. Ma, C. Finn, A. Kumar, and S. Levine, “Cal-ql: Calibrated offline rl pretraining for efficient online fine-tuning,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 62 244–62 269, 2023. 

- [170] Y. Jiang, J. Lu, X. Qin, X. Chen, K. Wang, F. Gao, and L. Zhao, “Vla-gse: Boosting parameter-efficient fine-tuning in vla with generalized and specialized experts,” _arXiv preprint arXiv:2605.06175_ , 2026. 

- [171] Z. Zhong, H. Yan, J. Li, J. He, T. Zhang, and H. Li, “Vla-opd: Bridging offline sft and online rl for vision-language-action models via on-policy distillation,” _arXiv preprint arXiv:2603.26666_ , 2026. 

- [172] X. Yuan, Y. Ding, Y. Bin, W. Shao, J. Cai, J. Song, Y. Yang, and H. T. Shen, “More than one teacher: Adaptive multiguidance policy optimization for diverse exploration,” _arXiv preprint arXiv:2510.02227_ , 2025. 

- [173] W. Wang, J. Song, C. Liu, J. Ma, S. Feng, J. Wang, Y. Jiang, K. Chen, S. Zhan, Y. Wang _et al._ , “Genie centurion: Accelerating scalable real-world robot training with human rewind-and-refine guidance,” _arXiv preprint arXiv:2505.18793_ , 2025. 

- [174] Y. Fang, Y. Yang, X. Zhu, K. Zheng, G. Bertasius, D. Szafir, and M. Ding, “Rebot: Scaling robot learning with real-to-sim-to-real robotic video synthesis,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2025, pp. 11 351– 11 358. 

- [175] J. Yu, L. Fu, H. Huang, K. El-Refai, R. A. Ambrus, R. Cheng, M. Z. Irshad, and K. Goldberg, “Real2render2real: Scaling robot data without dynamics simulation or robot hardware,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 547–577. 

- [176] C. Tai, Z. Zheng, H. Long, H. Wu, H. Xiang, Z. Long, J. Xiong, R. Shi, S. Zhang, G. Qiu _et al._ , “Realmirror: A comprehensive, open-source vision-language-action platform for embodied ai,” _arXiv preprint arXiv:2509.14687_ , 2025. 

- [177] T. Yoshida, S. Kurita, T. Nishimura, and S. Mori, “Developing vision-language-action model from egocentric videos,” _arXiv preprint arXiv:2509.21986_ , 2025. 

- [178] Z. Dong, X. Wang, Z. Zhu, Y. Wang, Y. Wang, Y. Zhou, B. Wang, C. Ni, R. Ouyang, W. Qin _et al._ , “Emma: Generalizing real-world robot manipulation via generative visual transfer,” _arXiv preprint arXiv:2509.22407_ , 2025. 

- [179] R. Yang, H. Wei, R. Zhang, Z. Feng, X. Chen, T. Li, C. Zhang, L. Zhao, J. Bian, X. Su _et al._ , “Beyond human demonstrations: Diffusion-based reinforcement learning to generate data for vla training,” _arXiv preprint arXiv:2509.19752_ , 2025. 

- [180] J. Xiao, Y. Yang, X. Chang, R. Chen, F. Xiong, M. Xu, W.-S. Zheng, and Q. Zhang, “World-env: Leveraging world model as a virtual environment for vla post-training,” _arXiv preprint arXiv:2509.24948_ , 2025. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

20 

- [181] H. Li, P. Ding, R. Suo, Y. Wang, Z. Ge, D. Zang, K. Yu, M. Sun, H. Zhang, D. Wang _et al._ , “Vla-rft: Vision-language-action reinforcement fine-tuning with verified rewards in world simulators,” _arXiv preprint arXiv:2510.00406_ , 2025. 

- [182] W. Song, Z. Zhou, H. Zhao, J. Chen, P. Ding, H. Yan, Y. Huang, F. Tang, D. Wang, and H. Li, “Reconvla: Reconstructive visionlanguage-action model as effective robot perceiver,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 40, no. 22, 2026, pp. 18 549–18 557. 

- [183] C. Nie, G. Wang, Z. Lie, and H. Wang, “Ermv: Editing 4d robotic multi-view images to enhance embodied agents,” _arXiv preprint arXiv:2507.17462_ , 2025. 

- [184] Simple AI, Y. Wei, J. Ma, J. Wang, W. Zhou, Y. Zuo, K. Rui, M. Li, J. Zhang, Z. Pan, X. Wang _et al._ , “Hifi-umi: Learning deployable manipulation policies from high-fidelity umi data alone,” _arXiv preprint arXiv:2607.25895_ , 2026. 

- [185] Y. Zhang, Z. Gao, S. Li, L.-H. Chen, K. Liu, R. Cheng, X. Lin, J. Liu, Z. Li, J. Feng _et al._ , “Robowheel: A data engine from real-world human demonstrations for cross-embodiment robotic learning,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2026, pp. 6664–6674. 

- [186] H. Li, I. Zhang, R. Ouyang, X. Wang, Z. Zhu, Z. Yang, Z. Zhang, B. Wang, C. Ni, W. Qin _et al._ , “Mimicdreamer: Aligning human and robot demonstrations for scalable vla training,” _arXiv preprint arXiv:2509.22199_ , 2025. 

- [187] C. Hui, X. Huang, S. Xu, Y. Wang, S. You, F. Wang, T. Huang, and C. Xu, “Seeing realism from simulation: Efficient video transfer for vision-language-action data augmentation,” _arXiv preprint arXiv:2605.02757_ , 2026. 

- [188] Z. Wang, B. Wang, H. Zhang, T. Du, T. Chen, G. Sun, Y. He, Z. Shen, W. Ye, and A. Li, “Vision-language-action in robotics: A survey of datasets, benchmarks, and data engines,” _Transactions on Machine Learning Research_ , 2026. 

- [189] Z. Zhou, T. Cai, S. Zhao, Y. Zhang, Z. Huang, B. Zhou, and J. Ma, “Autovla: A vision-language-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning,” _Advances in Neural Information Processing Systems_ , vol. 38, pp. 27 920–27 956, 2026. 

- [190] J. Zhang, M. Gagvani, C. Cui, J. Peng, R. Zhang, and Z. Wang, “Efficient and explainable end-to-end autonomous driving via masked vision-language-action diffusion,” _arXiv preprint arXiv:2602.20577_ , 2026. 

- [191] Y. Luo, F. Li, S. Xu, Z. Lai, L. Yang, Q. Chen, Z. Luo, Z. Xie, S. Jiang, J. Liu _et al._ , “Adathinkdrive: Adaptive thinking via reinforcement learning for autonomous driving,” _arXiv preprint arXiv:2509.13769_ , 2025. 

- [192] A. Jiang, Y. Gao, Z. Sun, Y. Wang, J. Wang, J. Chai, Q. Cao, Y. Heng, H. Jiang, Y. Dong _et al._ , “Diffvla: Vision-language guided diffusion planning for autonomous driving,” _arXiv preprint arXiv:2505.19381_ , 2025. 

- [193] R. Tu, A. Shukla, S. Yoo, X. Li, J. Li, J. Xie, H. Su, and Z. Tu, “Sgvla: Learning spatially-grounded vision-language-action models for mobile manipulation,” _arXiv preprint arXiv:2603.22760_ , 2026. 

- [194] S. Li, Y. Chen, D. Li, S. Liu, D. Lan, Y. Liu, and Z. Pang, “Transferring vision-language-action models to industry applications: Architectures, performance, and challenges,” in _2025 7th International Conference on Industrial Artificial Intelligence (IAI)_ . IEEE, 2025, pp. 1–6. 

- [195] C. Liu, S. Tian, X. Liang, and M. Zheng, “Self-vla: A skill enhanced agentic vision-language-action framework for contactrich disassembly,” _arXiv preprint arXiv:2603.11080_ , 2026. 

- [196] T. Robotics, J. Kang, T. Park, J. An, S. M. Kimm, J. Kim, J. Pahk, B. Kim, J. Lee, N. Baek _et al._ , “Habilis- _β_ : A fast-motion and longlasting on-device vision-language-action model,” _arXiv preprint arXiv:2602.18813_ , 2026. 

- [197] H. Zhang, P. Zeng, J. Zhang, J. Song, N. Sebe, H. T. Shen, and L. Gao, “Omnicharacter++: Towards comprehensive benchmark for realistic role-playing agents,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2026. 

- [198] N. Sun, Y. Li, C. Wang, H. Li, and H. Liu, “Collabvla: Selfreflective vision-language-action model dreaming together with human,” _arXiv preprint arXiv:2509.14889_ , 2025. 

## **8 BIOGRAPHY SECTION** 

**Zhaoshu Yu** is currently pursuing the Ph.D. degree in Computer Science and Technology at Tongji University, Shanghai, China. His research 

interests include vision-language-action models, embodied intelligence, and reinforcement learning. 

**Bo Wang** is currently a junior undergraduate student majoring in Computer Science and Technology at Tongji University, Shanghai, China. His research interests include vision-language-action models, embodied intelligence, and multimodal learning. 

**Pengpeng Zeng** received the B.E. degree from Xi’an University of Technology in 2016, and the M.E. and Ph.D. degrees from University of Electronic Science and Technology of China in 2019 and 2023, respectively. He is now a Researcher in Tongji University, China. His current research interests include visual understanding, machine learning, and reinforcement learning. 

**Haonan Zhang** is currently a Postdoctoral Researcher with the School of Computer Science and Technology, Tongji University, China. He obtained his Ph.D. degree from the University of Electronic Science and Technology of China in 2026. His research interests include multimodal learning, intelligent dialogue, and agent-based systems. 

**Ji Zhang** is an Assistant Professor with the School of Computing and Artificial Intelligence, Southwest Jiaotong University, China. He obtained his PhD degree from University of Electronic Science and Technology of China in 2024. His research interests include few-shot learning, transfer learning and robotics. 

**Zheng Wang** received the B.E. and Ph.D. degrees from Zhejiang University, Hangzhou, China, in 2011 and 2017, respectively. He is currently with the School of Computer Science and Technology, Tongji University, Shanghai, China. His current research interests mainly focus on visionlanguage action, multimedia understanding, and computer vision. 

**Lianli Gao** is a professor with the School of Computer Science and Engineering, University of Electronic Science and Technology of China. She obtained her PhD degree in Information Technology from The University of Queensland (UQ), Australia, under the supervision of Prof. Jane Hunter and Prof. Michael Bruenig. Her research ranges from Semantic Web, Machine Learning, Deep Learning, Computer Vision (Images and Videos), NLP, Knowledge Reasoning, Knowledge and the related practical applications etc. Specifically, she is mainly focusing on integrating Natural Language for Visual Content Understanding. She has the winner of the IEEE Transactions on Multimedia 2020 Prize Paper Award, Best Student Paper Award in Australian Database Conference (2017, Australia), IEEE TCMC Rising Star Award 2020 and ALIBABA Academic Young Fellow. She is an Associate Editor of IEEE TMM. 

**Jingkuan Song** is a professor with the School of Computer Science and Technology, Tongji University, China. He joined Columbia University as a Postdoc Research Scientist (2016-2017), and University of Trento as a Research Fellow (2014-2016). He obtained his PhD degree in 2014 from The University of Queensland (UQ), Australia. His research interest includes large-scale multimedia retrieval, LLMs and deep learning techniques. He was the winner of the Best Paper Award in ICPR (2016, Mexico), Best Student Paper Award in Australian Database Conference (2017, Australia), and Best Paper Honorable Mention Award (2017, Japan). He is an Associate Editor of IEEE TMM and ACM TOMM. 

**Nicu Sebe** is a professor with the Department of Information Engineering and Computer Science, University of Trento, leading the research in the areas of multimedia information retrieval and human behavior understanding. He was the General CoChair of ACM Multimedia 2013 and 2022, and the Program Chair of ACM Multimedia 2007 and 2011, ECCV 2016, ICCV 2017 and ICPR 2020. He is a fellow of the International Association for Pattern Recognition (IAPr) and of the European Laboratory for Learning and Intelligent Systems (ELLIS). 

**Heng Tao Shen** is a professor with the School of Computer Science and Technology, Tongji University, China. He obtained his BSc with 1st class Honours and PhD from Department of Computer Science, National University of Singapore in 2000 and 2004 respectively. His current research interests include multimedia search, computer vision, artificial intelligence, and big data management. He has published 300+ peerreviewed papers and received 7 best paper awards from international conferences, including the Best Paper Award from ACM Multimedia 2017 and Best Paper Award-Honourable Mention from ACM SIGIR 2017. He has served as General Co-chair for ACM Multimedia 2021 and TPC Co-Chair for ACM Multimedia 2015, and is an Associate Editor of ACM Trans. of Data Science (TDS), IEEE Trans. on Image Processing (TIP), IEEE Trans. on Multimedia (TMM), and IEEE Trans. on Knowledge and Data Engineering (TKDE). He is a Fellow of ACM/IEEE/OSA. 

