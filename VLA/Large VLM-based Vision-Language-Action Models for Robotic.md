---
title: "Large VLM-based Vision-Language-Action Models for Robotic Manipulation: A Survey"
date: "2025-08-18"
authors: "Rui Shao; Wei Li; Lingsen Zhang; Renshan Zhang; Zhiyang Liu; Ran Chen"
url: https://arxiv.org/abs/2508.13073
pdf: https://arxiv.org/pdf/2508.13073
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2508.13073)** / [論文ページ](https://arxiv.org/abs/2508.13073)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

1 

# Large VLM-based Vision-Language-Action Models for Robotic Manipulation: A Survey 

Rui Shao, Wei Li, Lingsen Zhang, Renshan Zhang, Zhiyang Liu, Ran Chen, Liqiang Nie 

**Abstract** —Robotic manipulation, as a critical frontier in robotics and embodied AI, demands precise motor control and integrated understanding of visual and semantic cues in dynamic environments. Traditional approaches, grounded in predefined task specifications and rigid control policies, often struggle to scale or generalize in unstructured, novel scenarios. In recent years, Vision-Language-Action (VLA) models, built upon Large Vision-Language Models (VLMs) pretrained on vast image-text datasets, have become an increasingly studied paradigm. By leveraging large VLMs’ capabilities in open-world generalization, hierarchical task planning, knowledge-augmented reasoning, and rich multimodal fusion, these models empower robots to interpret high-level instructions, recognize unseen environments and execute complex manipulation tasks. This survey provides the first systematic, taxonomy-oriented review of large VLM-based VLA models for robotic manipulation. We begin by clearly defining large VLM-based VLA models and delineating two principal architectural paradigms: **(1) monolithic models** , encompassing single-system and dual-system designs with differing levels of integration; and **(2) hierarchical models** , which explicitly decouple planning from execution via interpretable intermediate representations. Building on this foundation, we present an in-depth examination of large VLM-based VLA models: **(1)** integration with advanced domains, including reinforcement learning, training-free optimization, learning from human videos, and world model integration; **(2)** synthesis of distinctive characteristics, consolidating architectural traits, operational strengths, and the datasets and benchmarks that support their development; **(3)** identification of promising directions, including memory mechanisms, 4D perception, efficient adaptation, multi-agent cooperation, and other emerging capabilities. This survey consolidates recent advances to resolve inconsistencies in existing taxonomies, mitigate research fragmentation, and fill a critical gap through the systematic integration of studies at the intersection of large VLMs and robotic manipulation. We provide a regularly updated project page to document ongoing progress: https://github.com/JiuTian-VL/Large VLM-based VLA for Robotic Manipulation. 

**Index Terms** —Vision-Language-Action Models, Robotic Manipulation, Embodied AI, Large Vision-Language Models 

✦ 

## **1 INTRODUCTION** 

R theOBOTICconfluencemanipulationof roboticsstandsandasembodieda pivotal challengeartificial in-at telligence [1]–[5]. Its realization necessitates not only precise motor control but also a profound comprehension of diverse visual and semantic cues within complex, dynamic environments. The widespread utility of robotic manipulation is evident across numerous domains, including advanced manufacturing, efficient logistics, precision healthcare, and versatile domestic service [6]–[8]. Traditional manipulation methods [9]–[15] have been predominantly anchored in meticulously engineered control policies and rigidly predefined task specifications. However, these approaches demonstrably falter in unstructured, real-world settings—particularly when confronted with novel objects [16], [17], ambiguous natural language instructions [18], [19], or previously unseen environmental configurations [9], [20]–[22]—thereby exposing inherent limitations in their scalability and generalization capabilities. 

Recently, large Vision-Language Models (VLMs) [23]– [28] have emerged as a transformative paradigm. Pretrained on vast web-scale image-text datasets, large VLMs provide capabilities for aligning visual information with natural 

_Rui Shao, Wei Li, Lingsen Zhang, Renshan Zhang, Zhiyang Liu, Ran Chen and Liqiang Nie are with the School of Computer Science and Technology, Harbin Institute of Technology (Shenzhen), China, 518055 (email: shaorui@hit.edu.cn, {liwei2024, zls030726, zhangrenshan, 25s151095, 220310324}@stu.hit.edu.cn, nieliqiang@gmail.com). Wei Li is corresponding author._ 


Fig. 1: Illustration of core advantages of large VLMbased Vision-Language-Action (VLA) models for robotic manipulation. Large VLM-based VLA models leverages the strengths of large Vision-Language Models (VLMs), including **(1)** open-world generalization, **(2)** hierarchical task planning, **(3)** knowledge-augmented reasoning, and **(4)** rich multimodal fusion. These capabilities empower diverse robotic arms and significantly enhance robotic intelligence. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

2 


Fig. 2: Outline of the organization of our comprehensive survey (top) and a chronological timeline of notable developments in large VLM-based Vision-Language-Action models for robotic manipulation (bottom). The timeline highlights representative milestones for both monolithic models and hierarchical models, providing a perspective on the field’s recent progress. 

language. This innovative capacity enables large VLMs to interpret complex visual scenes in conjunction with textual descriptions, moving beyond mere object recognition to encompass a holistic contextual understanding. The subsequent integration of large VLMs into robotic systems has catalyzed the development of a novel class of models: large VLM-based Vision-Language-Action (VLA) models [29]– [35]. As illustrated in Fig. 1, this emerging paradigm offers great potential to overcome the fundamental limitations of conventional robotic pipelines. It enables robots to interpret high-level human instructions, generalize to unseen objects and scenarios, reason about complex spatial relationships, and perform sophisticated manipulation tasks in dynamic, unstructured environments. For instance, a VLA model could execute commands such as “place the red mug next to the laptop onto the top shelf,” a task demanding a sophisticated fusion of visual grounding, spatial reasoning, and sequential motion planning. 

In this work, based on an extensive review of recent research [29]–[40] and a refined understanding of the field [41]–[46], we propose a coherent definition of large VLM-based VLA models: the model (1) leverages a large VLM to understand visual observations and natural language instructions, and (2) performs reasoning processes that directly or indirectly serve robotic action generation. We further distinguish two principal categories of large VLMbased VLA models, as shown in Fig. 2 and Fig. 3: 

- **Monolithic Models** (Fig. 3, left) comprise single-system and dual-system implementations. (1) Single-system models [29], [30], [47], [48] integrate both environmental comprehension (including visual perception, linguistic understanding, and robot state awareness) and action generation within a unified architecture. In contrast, (2) dual-system models [32]–[35] employ a VLM backbone for scene interpretation and an action expert for action determination, exchanging information via 

the propagation of latent representations. 

- **Hierarchical Models** (Fig. 3, right) [49]–[53] explicitly decouple planning from policy execution. These differ from dual-system end-to-end approaches through two defining characteristics: (1) Structured intermediate outputs where planner modules generate interpretable representations such as keypoint detections, affordance maps, or trajectory proposals, which are then processed by policy modules to formulate executable actions; and (2) Decoupled training paradigms that enable independent optimization of hierarchical modules through specialized loss functions or API-mediated interactions. 

This taxonomy emphasizes critical design dimensions in VLA development, particularly regarding system integration granularity and the explicitness of cognitive decomposition, while maintaining essential connections to modern representation learning paradigms. 

Operating under the above definitions and taxonomy, our comprehensive survey across the broad spectrum of related work reveals several critical gaps within the nascent VLA field, with the organization of this survey illustrated in Fig. 2. First, the terminology and modeling assumptions in this field remain inconsistent, and the research landscape is fragmented across disciplines (robotics, computer vision, natural language processing, etc.). Second, existing reviews tend to focus either on VLMs [54]–[58] or on robotic manipulation in isolation [2], [59]–[62], lacking a comprehensive synthesis of the unique challenges and advances that arise at their intersection. Therefore, there is a pressing need for a systematic and principled survey that elucidates the foundations of large VLM-based VLA models, organizes the space of relevant methods, and outlines future directions for this integrated paradigm. This survey aims to address this gap. We present a structured and in-depth overview of advances in large VLM-based VLA models research, aiming to provide a panoramic perspective of the field to foster a 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

3 


Fig. 3: Comparison of the two principal categories of large VLM-based VLA models. Monolithic models (Sec. 3) integrate perception, language understanding, and action generation within single- or dual-system architectures, with the latter incorporating an additional action expert. In contrast, hierarchical models (Sec. 4) decouple planning from policy execution through interpretable intermediate outputs (e.g., subtasks, keypoints, programs, affordances). 

deeper understanding and support future research. Our key contributions are summarized as follows: 

## **2 BACKGROUND** 

### **2.1 Evolution of Vision-Language Models** 

- **A Longitudinal Synthesis of large VLM-based VLA Models Development:** We systematically review the evolutionary trajectory of VLMs, the technical advancements in manipulation learning, and the subsequent emergence of the large VLM-based VLA paradigm. Furthermore, we examine the development of monolithic models and hierarchical models, identifying key challenges and outlining future directions. 

- **A Cross-Cutting Synthesis of large VLM-based VLA Modeling Practices:** We provide a more fine-grained comparative taxonomy of monolithic models and hierarchical models, examining them in detail from both structural and functional perspectives. We further explore advanced research frontiers of large VLM-based VLA models, highlighting their distinctive characteristics and the datasets that underpin their development. 

This synthesis provides a high-level summary and a conceptual roadmap for understanding the field’s development and structural organization. 

The remainder of this survey is organized as follows. As illustrated in Fig. 2, Sec. 2 presents essential background on the evolution of VLMs and the foundations of robotic manipulation. Sec. 3 examines monolithic models, detailing single-system and dual-system architectures, their respective advantages, and design trade-offs. Sec. 4 explores hierarchical models, categorizing them into planner-only and planner–policy frameworks, and further sub-classifying by intermediate representations such as subtasks, keypoints, and programs. Sec. 5 discusses other advanced fields, including RL-based optimization, training-free methods, learning from human videos, and world model-based approaches. Sec. 6 analyzes key characteristics of large VLMbased VLA models, covering multimodal fusion, instruction following, and multi-dimensional generalization. Sec. 7 concludes the survey. Appx. A provides a comparative experimental analysis of state-of-the-art large VLM-based VLA models, evaluating generalization across benchmarks and real-world deployments, and discussing trade-offs between monolithic and hierarchical paradigms. Appx. B categorizes and analyzes the diverse datasets and benchmarks employed in large VLM-based VLA models research, spanning simulated, real-world, and human interaction data. Finally, Appx. C explores critical open challenges and promising future research directions. 

Recently, the emergence of large VLMss [23]–[28], [63]–[65] has been marked by a shift from task-specific architectures to unified frameworks capable of handling diverse multimodal tasks [66]–[70]. Modern VLMs, such as LLaVA1.5 [23] and Qwen-VL [25], typically adopt a three-component architecture: a vision encoder to encode visual input, a projector to align visual features with textual embeddings, and a large language model to mediate multimodal reasoning. This design unifies multimodal tasks as textual outputs. It enables VLMs to perform not only traditional tasks like visual question answering or object detection [71], [72], but also more advanced capabilities, including compositional reasoning and spatial navigation [73]–[76], which are critical for real-world applications. Building on this foundation, DriveVLM [77] demonstrates the integration of VLMs into autonomous driving systems, while CogAgent [78] shows VLMs’ ability to interact with graphical user interfaces. These advancements highlight the growing sophistication of large VLMs in bridging vision and language, while also revealing the emerging potential of using large VLMs to build broad real-world applications. 

Crucially, the potential of large VLMs in real-world applications [79]–[88] rests on their generalization capabilities afforded by visual instruction tuning. By training on large-scale, carefully curated visual instruction–following datasets, VLMs acquire the flexibility to comprehend abstract or open-ended instructions and to generalize to unseen multimodal scenarios. LLaVA [26] pioneers this paradigm by leveraging GPT-4 to convert raw image–text pairs into 150K conversational samples, significantly enhancing its ability to address open-ended queries. InternVL2 [27] advances by introducing an LLM-guided automated filtering pipeline. It helps clean noisy annotations, reducing anomalous behaviors of the model. Collectively, these advances demonstrate how visual instruction tuning prepares large VLMs to follow high-level commands. This capability forms the foundation for extending large VLMs to VLA for robotic manipulation, which requires robust reasoning across vision, language, and action in the real world with ambiguous instructions. 

Recent advancements in VLMs further emphasize scalability for enhanced multimodal perception and reasoning. Models like LLaVA-OneVision [89] unify image and video processing within a single framework. Qwen-2VL [90] intro- 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

4 

duces dynamic resolution support for arbitrary input sizes, while Vision-R1 [91] leverages reinforcement learning to improve chain-of-thought reasoning. Collectively, these innovations empower VLMs with stronger real-world perception and decision-making capabilities, laying the groundwork for VLMs to further integrate action generation. 

Building on these breakthroughs, the next frontier for large VLMs is to transition from passive observation to active interaction with physical environments. While models like DriveVLM [77] and CogAgent [78] already demonstrate VLMs’ ability to process real-world inputs and generate high-level plans, they remain unable to engage directly with the real world in an embodied, physical manner. Equipping VLMs with robotic manipulation capabilities thus emerges as a particularly promising avenue for future research. 

### **2.2 Advancements in Robotic Manipulation** 

Early language-conditioned robotic systems typically relied on modular designs, pairing separate vision encoders with language modules or planners rather than using unified multimodal models. For instance, CLIPort [16] combines the CLIP vision-language encoder [92] for semantic grounding with a Transporter network [17] for spatial reasoning, while RT-1 [20] uses a CNN-based visual encoder [93] conditioned on separate language embeddings to map observations and instructions to actions. Beyond such pipelines, early vision-language manipulation methods like PerAct [94] and VIMA [95] introduced transformer-based policies that jointly process visual inputs and language prompts for action prediction, while VLMBench [96] provided a standardized benchmark for evaluating language-grounded manipulation. Although these approaches enable a degree of multi-task generalization by integrating pretrained visual and language components, they remain limited by taskspecific supervision and lack strong generalization to novel concepts and long-horizon tasks. They also struggle with complex or ambiguous instructions, highlighting the need for unified large-scale VLM-based VLA architectures [29], [32], [33], [35], [97]–[103]. 

In contrast, the latest VLA models tightly integrate vision, language, and action control in a unified system. The RT-2 [30] model exemplifies this shift. RT-2 [30] begins with a pretrained large VLM backbone (e.g., PaLM-E [21] or PaLI-X [104]) and co-trains it on both internet-scale visionlanguage tasks and real robot trajectories. Crucially, robot actions are cast as text tokens and included in the same training corpus as normal language outputs. This simple scheme allows the model to “absorb” robot control as another language task, resulting in a unified VLA model. Empirically, RT-2 demonstrates improved semantic understanding. Compared to RT-1 [20], RT-2 [30] generalizes to novel objects and unseen instructions (e.g., placing an object on a particular number) and can perform basic reasoning (choosing the smallest or closest object). In other words, the large-scale vision-language pretraining imbues the robotic policy with real-world knowledge and stronger language grounding that earlier models lack. 

Following RT-2’s demonstration of how Internet-scale VLM pretraining can boost robotic control, more VLA models have emerged. For example, _π_ 0 [32] adopts a flowmatching architecture on top of a pretrained VLM, trained 

on diverse dexterous robot datasets, which yields strong zero-shot generalization and easy adaptation to new tasks via fine-tuning. In addition, OpenVLA [29] has been released as a 7B open-source VLA model pretrained on approximately 970k real-world robot demonstrations. It achieves superior generalist manipulation performance and supports efficient fine-tuning on consumer hardware via techniques like LoRA [105]. Together, these advancements underscore a trend toward greater generality and open accessibility in VLA-driven robotic manipulation. 

### **2.3 Relevant Surveys and Taxonomies** 

The growing interest in VLA models for embodied AI has inspired several surveys [1]–[6], [8], [106], [107], yet most focus on broader architectural paradigms or diverse application domains, leaving a gap in the systematic exploration of large VLM-based VLA systems specifically tailored for robotic manipulation. Crucially, the taxonomies in existing surveys fail to highlight the fundamental impact of pretrained large models as core backbones on architectural design. 

For example, Wang et al. [106] offers an early overview of the integration of text-only LLMs into robotic task planning. It emphasizes their capability to generate precise action plans from natural language instructions. However, the study primarily focuses on high-level reasoning and does not address the challenge of grounding VLMs in robotic visual perception and action determination, which is a gap that recent VLA models are designed to fill. To bridge this gap, our taxonomy introduces both monolithic and hierarchical paradigms to systematically analyze how highlevel semantic plans are translated into actuator commands and how VLMs are securely grounded in low-level control mechanisms. Ma et al. [2] conduct a comprehensive survey of VLA architectures, reviewing modular, end-to-end, and hybrid approaches for integrating vision, language, and action modalities. However, this survey lacks a focused analysis of recent trends that leverage pre-trained VLMs as foundational components. To address this limitation, our Monolithic and Hierarchical classifications categorize models based on how the VLM backbone is structurally integrated into the control loop. Specifically, we detail whether the VLM acts as a unified action generator or a decoupled high-level planner, as shown in Fig. 3. Sapkota et al. [8] provide an extensive investigation into a broader range of VLA applications, such as autonomous driving, augmented reality navigation, and precision agriculture. However, its breadth dilutes the depth required for robotics-specific challenges such as real-time actuation constraints, sensor noise robustness, and long-term decision-making. Yao et al. [108] categorize language-conditioned manipulation tasks based on the functional roles of language, such as serving as policy conditioning or enabling cognitive planning. Li et al. [109] examine how various foundation models are incorporated into the high-level functional modules of robot learning. While these surveys provide task-oriented or modular perspectives, they typically treat foundation models as auxiliary cognitive tools rather than unified action generators. In contrast, this survey specifically investigates how large VLMs are structurally coupled with low-level control mechanisms. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

5 

To address the lack of a comprehensive and in-depth survey in this emerging field, we provide a structured overview of recent VLA research. Building on the definition of VLA models described in Sec. 1, we trace the evolution of VLAs in robotics and analyze key learning paradigms. Meanwhile, we provide comparative introductions and insights into advanced architectures leveraging reinforcement learning, world models, and related techniques. Our aim is to offer a comprehensive perspective that supports deeper understanding and drives future advances. 

## **3 MONOLITHIC MODELS** 

Monolithic VLA models are mainly implemented in two ways: single-system and dual-system architectures, as illustrated in Fig. 3 left. In the single-system design (Sec. 3.1), visual perception, language instructions, and robot states are jointly fed into a unified model that processes all modalities and decodes executable actions via autoregressive or parallel decoding. In contrast, dual-system architectures (Sec. 3.2) divide functionality into two cooperating modules: System 2 (VLM backbone) performs slower but more generalized reflective reasoning, while System 1 (action expert) focuses on fast processing to support reactive behaviors. Singlesystem VLAs offer streamlined development and avoid complex inter-module communication. In contrast, dualsystem VLAs are highly inclusive and cover a broad range of action expert integration strategies, including hybrid variants subsumed under this category, leveraging a division of labor to combine reactive speed with reasoning accuracy. 

### **3.1 Single-system Models** 

Single-system VLA models embody the monolithic design philosophy. They aim to transfer the semantic knowledge of large VLMs to robotic manipulation tasks through a unified model. This section reviews the paradigms of single-system models and explores two main research directions: enhancing the model’s capabilities to solve complex tasks and improving inference efficiency for practical deployment. All models are summarized in Tab. 1. 

### _3.1.1_ **_Classic Paradigm: Autoregressive Decoding_** 

The autoregressive decoding paradigm draws directly from the sequence generation capability of LLMs. By discretizing the robot’s continuous action space into a token sequence, the model can sequentially predict action tokens. As shown in “Autoregressive Decoding” of Fig. 4, the VLM receives the visual observation, natural language instruction, and optionally the robot state as input. Then it autoregressively generates action tokens, which can be converted into executable actions through a downstream de-tokenizer. 

The RT series [20], [30], [110] and OpenVLA [29] are typical examples of this paradigm. RT-1 [20] introduces Transformer [136] into the VLA domain and encodes continuous robot actions as discrete tokens. RT-2 [30] inherits this token-based action representation and applies it to a larger-scale VLM. It co-fine-tunes on internet-scale visionlanguage and robot trajectory data, successfully transferring rich visual–semantic knowledge from web data to robotic manipulation tasks. RT-2-X [110] further improves crossrobot skill transfer by applying co-fine-tuning on the Open 

X-Embodiment (OXE) dataset [110]. Going a step further, OpenVLA [29] replaces the large-parameter vision encoder in RT series with a combination of SigLIP [137] and DINOv2 [138]. Through fine-tuning on large-scale real-world robotic manipulation data, it achieves superior performance with fewer model parameters. Its fully open-sourced nature positions it as a widely used baseline in subsequent research. 

These models demonstrate that large-scale visionlanguage pretraining knowledge can be transferred directly to robot control. However, the classic paradigm relies heavily on a single 2D visual input and reactive decision-making. As a result, they often perform poorly in complex real-world environments due to limited capabilities and low efficiency, setting the stage for subsequent research on performance enhancement and inference efficiency optimization. 

### _3.1.2_ **_Model Performance Enhancement_** 

To address these performance bottlenecks in complex environments, recent studies have systematically enhanced VLA models from three perspectives. They expand perception modalities to capture richer physical surroundings, strengthen reasoning capabilities to transition from reactive control to deliberate decision-making, and improve generalization capabilities to ensure robust execution. 

**Enhancing Perception Modalities** . As shown in Fig. 4, these models improve real-world information acquisition by expanding input modalities. **(1) 3D perception.** Since the real world is three-dimensional and continuous, large VLMbased VLA models cannot fully understand it by relying solely on 2D images. Accordingly, Leo Agent [111] directly obtains object-centric 3D point clouds from simulation environments and encodes them using PointNet++ [139]; the encoded features are then fed into a spatial transformer [140] to generate “Space” information. In real-world settings, SpatialVLA [117] proposes Ego3D position encoding, which estimates depth from 2D images and back-projects it into egocentric 3D coordinates, fusing pixel-wise 3D positions with 2D features to produce egocentric “Space” information. Similarly, BridgeVLA [38] reconstructs 3D point clouds from RGB-D images and generates three orthographic projection views, enabling “Space” information to be represented in a 2D format compatible with large VLMs. 

**(2) 4D perception.** To better capture spatial structure and temporal dynamics in robotic manipulation, 4D perception is required for more comprehensive scene understanding. TraceVLA [114] overlays sampled motion-point trajectories on the current image to create the “Trace” information in Fig. 4. Combined with the original observation, it equips the large VLM with spatiotemporal understanding. Furthermore, 4D-VLA [125] integrates 3D coordinates into visual features to resolve spatial coordinate inconsistency, and leverages memory bank sampling of historical keyframes to mitigate temporal state ambiguity, thereby improving spatiotemporal reasoning. ST-VLA [127] introduces the “Spatial Traces” approach, which combines historical temporal “Trace” information with spatial depth information of the scene, surpassing prior SpatialVLA [117] and TraceVLA [114] models in certain robotic manipulation tasks. 

**(3) Additional modality perception.** Purely vision-based models often fail in contact-rich operations. To reduce the perceptual gap with the real world during manipulation, 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

6 

TABLE 1: Single-system VLA models. In the LLM / VLM column, omission of the V-Encoder indicates a VLM; otherwise, it represents an LLM. In the Learning column, “AD” denotes Autoregressive Decoding and “PD” denotes Parallel Decoding. “SFT” denotes fine-tuning distinct from action-prediction imitation learning, where tasks like captioning, VQA, reasoning and others all qualify as SFT. “A” and “B” in parentheses represent the learning methods used by Action head or Backbone. 

|**Model**|**V-Encoder**|**LLM / VLM**|**Learning**|**Contribution**|
|---|---|---|---|---|
|||**Classic Par**|**adigm: Autoregressiv**|**e Decoding**|
|RT-2 [30]|-|PaLI-X / PaLM-E|AD (A), SFT (B)|Represent actions as VLM tokens to enable generalization.|
|RT-2-X [110]|ViT-22B|UL2|AD (A), SFT (B)|Fine-tune on cross-robot data for positive skill transfer.|
|OpenVLA [29]|DINOv2 + SigLIP|LLaMA2-7B|AD (A)|Open-source 7B-parameter VLA model for generalist robot control.|
|||**Paradigm Derivat**|**ions: Model Performa**|**nce Enhancement**|
|LEO agent [111]|ConvNext|Vicuna-7B|AD (A), SFT (B)|Combine object-centric 3D features with LLM for action.|
|<br>ECoT [112]|DINOv2 + SigLIP|LLaMA2-7B|AD (A), SFT (B)|<br>Incorporate chain-of-thought to enhance policy explainability.|
|ReVLA [113]|DINOv2 + SigLIP|LLaMA2-7B|AD (A)|Reverse backbone gradually to preserve visual generalization.|
|TraceVLA [114]|DINOv2 + SigLIP|LLaMA2-7B|AD (A)|Propose visual trace prompting for spatiotemporal awareness.|
|FuSe [115]|-|PaliGemma-3B|AD (A), SFT (B)|Leverage natural language for cross-modal fine-tuning.|
|UniAct [116]|-|LLaVA-0.5B|PD (A)|Propose universal action space for versatile and adaptive control.|
|SpatialVLA [117]|SigLIP|Gemma2|AD (A)|Improve generalization via 3D encoding and action grid.|
|<br>UP-VLA [118]|ViT + VQ-GAN|Phi1.5-1.3B|AD (A), SFT (B)|<br>Propose unified training for semantic-spatial understanding.|
|VLAS [119]|CLIP|Vicuna-7B|AD (A), SFT (B)|Introduce voice modality to VLA and construct a paired dataset.|
|HybridVLA [37]|DINOv2 + SigLIP|LLaMA2-7B|Diff., AD (A)|Integrate diffusion and autoregressive policies to improve success.|
|<br>CoT-VLA [36]|<br>-|VILA-U|AD+PD(A), SFT(B)|<br>Propose a visual chain-of-thought to improve planning.|
|VTLA [120]|-|Qwen2-VL-7B|AD (A)|Integrate visual and tactile inputs to improve task success.|
|OE-VLA [121]|SigLIP|Qwen1.5-7B|AD (A), SFT (B)|Introduce four open-ended tasks to expand interaction modalities.|
|ReFineVLA [122]|SigLIP|Gemma2|AD (A), SFT (B)|<br>Propose reasoning-aware framework to fine-tune VLAs effectively.|
|LoHoVLA [123]|SigLIP|Gemma-2B|AD (A), SFT (B)|i <br>Address long-horizon tasks via hierarchical closed-loop control.|
|BridgeVLA [38]|SigLIP|Gemma|PD (A), SFT (B)|Project 3D data into 2D space for efficient action prediction|
|UnifiedVLA [124]|-|Emu3|AD (A), SFT (B)|Convert all input signals into tokens to build a unified model.|
|i<br>WorldVLA [41]|-|Chameleon|AD (A), SFT (B)|i<br>Combine world and action models for bidirectional improvement.|
|4D-VLA [125]|-|InternVL-4B|PD (A)|Integrate 4D spatiotemporal cues for efficient VLA pretraining.|
|VOTE [126]|DINOv2 + SigLIP|LLaMA2-7B|PD (A)|Introduce voting strategy to increase action prediction accuracy.|
|ST-VLA [127]|-|PaliGemma2|AD (A), SFT (B)|Project visual traces onto depth maps for better understanding.|
|||**Paradigm Derivat**|**ions: Inference Efficie**|**ncy Optimization**|
|RoboFlamingo<br>[128]|ViT|MPT-1B|PD (A), SFT (B)|Decouple design to adapt open-sourced VLM for robotic control.|
|RoboMamba [129]|CLIP / SigLIP ViT-L|Mamba-2.8B/1.4B|PD (A), SFT (B)|Introduce the Mamba architecture to the VLA field.|
|DeeR-VLA [39]|CLIP ViT-L/14|MPT-1B / 7B|PD (A)|Propose dynamic early-exit to reduce inference overhead.|
|OpenVLA-OFT [47]|DINOv2 + SigLIP|LLaMA2-7B|<br>PD (A)|<br>Boost performance via OpenVLA-based fine-tuning.|
|<br>PD-VLA [130]|<br>CLIP ViT-L|Vicuna1.5-7B|<br>PD (A)|i<br>Introduce parallel decoding manner for faster robot control.|
|MoLe-VLA [131]|DINOv2 + SigLIP|LLaMA2-7B|PD (A)|<br>Reduce computation via dynamic LLM layer activation.|
|NORA [48]|-|Qwen2.5-VL-3B|AD (A)|Build efficient low-parameter model to boost performance.|
|FLashVLA [132]|DINOv2 + SigLIP|LLaMA|<br>AD (A)|i<br>Propose retraining-free acceleration to improve VLA inference.|
|BitVLA [133]|SigLIP b1.58|BitNet b1.58 2B4T|PD (A), SFT (B)|Build ternary weight model to reduce deployment memory cost.|
|Spec-VLA [134]|DINOv2 + SigLIP|LLaMA2-7B|PD (A)|Propose speculative decoding to speed up without success drop.|
|CogVLA [135]|DINOv2 + SigLIP|LLaMA2-7B|PD (A)|Propose a cognition-aligned framework for efficient manipulation.|


VTLA [120] encodes tactile information with a vision encoder to align it with visual sequences, and then feeds it into the LLM together with visual and textual tokens, thereby constructing a “Vision-Tactile-Language-Action model”. Beyond tactile information, auditory cues in the real world also deserve attention. VLAS [119] employs the “Whisper Encoder” to extract speech features and projects them into the LLM embedding space through an MLP, thereby introducing the audio information shown in Fig. 4. Moreover, Fuse [115] learns to align “Touch” and “Audio” modalities with language concepts during fine-tuning, enabling multimodal fusion with limited modality specific annotations. Beyond touch and audio, OE-VLA [121] incorporates multimodal instructions by leveraging diverse multimodal data and a two-stage curriculum learning strategy, thereby extending instructions beyond text to images and videos. 

**Enhancing Reasoning Capabilities** . To move VLA models from simple reactive control toward more advanced 

deliberative decision-making, enhancing reasoning ability is essential. As shown in “Enhancing Reasoning Capabilities” of Fig. 4, the LLM generates a chain-of-thought “Reasoning” process, which is then used as contextual information to produce the final “Action”. ECoT [141] generates a reasoning chain that sequentially combines high-level task planning with visually grounded features before outputting the final action. CoT-VLA [36] further introduces a visual chain-ofthought reasoning by predicting a subgoal observation that represents a planned state in pixel space. In contrast to reasoning-oriented perspectives, LoHoVLA [123] employs a “Hierarchical Closed-Loop Control” mechanism to address planning errors, action failures, and external disturbances, thereby handling long-horizon tasks. ReFineVLA [122] adopts a “Selective Transfer Fine-Tuning” strategy with dual learning objectives to fine-tune only the upper layers, enabling the model to enhance multimodal understanding. These studies collectively underscore the central 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

7 


Fig. 4: Comparison of representative paradigms in single-system models. Sec. 3.1.1 illustrates the model schematic of classical autoregressive decoding, where arrows denote information flow. Sec. 3.1.2 presents approaches to enhance model capabilities through additional modalities, chain-of-thought reasoning, and improved generalization. Sec. 3.1.3 discusses methods for improving inference efficiency through architectural refinement, parameter design, and decoding strategies. 

role of reasoning in enabling VLA models to achieve more reliable and generalizable action prediction. 

**Enhancing Generalization Capabilities** . The generalization capability of a model refers to its ability to perform diverse tasks across different platforms and scenarios. As illustrated in “Enhancing Generalization Capabilities” of Fig. 4, UniAct [116] defines a “Universal Action Codebook” that abstracts heterogeneous robot actions into a unified representation. This unified encoding eliminates actionspace heterogeneity and enables cross-embodiment learning and reasoning, thereby enhancing generalization. ReVLA [113] employs a reversible training strategy that gradually restores the vision encoder to its original pre-trained state, mitigating catastrophic forgetting during fine-tuning and improving out-of-distribution visual generalization. 

Another approach to enhancing generalization is to generate more robust and reliable actions, as depicted in Fig. 4. HybridVLA [37] integrates diffusion and autoregressive decoding within a unified model, and employs a Collaborative Action Ensemble mechanism to adaptively fuse them, selecting the most suitable generation strategy for different tasks, thereby improving control robustness. Similarly, VOTE [126] introduces an adaptive “Ensemble Voting” strategy that groups past action predictions by similarity to the current one. It averages the majority set to produce more robust actions, balancing responsiveness and stability. 

Enabling the model to better understand physical dynamics can promote the generation of more reliable actions. WorldVLA [41] integrates an action model and a world model within a unified autoregressive framework for capturing physical dynamics. Likewise, UnifiedVLA [124] introduces a world model as a post-training task, enabling it to learn causal dynamics of the physical world from largescale unlabeled videos. UP-VLA [118] proposes a training framework that implicitly learns the physical dynamics of the world by predicting the next-frame image during pretraining. Consequently, these models generate more reliable actions that better adhere to physical laws. 

Overall, the core strategies for improving the performance of single-system models include introducing new modalities and incorporating techniques such as chain-ofthought reasoning. The former injects diverse prior knowledge about the physical world into the model and com- 

pensates for the blind spots of 2D vision, whereas the latter endows the model with more human-like complex reasoning. Together with other advances, these strategies ultimately lead to broader generalization capabilities. However, although these methods substantially improve model capability, incorporating new modalities still relies on taskspecific fine-tuning data and has not yet developed general pre-trained representations comparable to those for 2D image-text data. Nevertheless, integrating these capabilities inevitably exacerbates the computational burden, highlighting a critical trade-off between performance enhancement and the real-time constraints of robotic control. 

### _3.1.3_ **_Inference Efficiency Optimization_** 

To resolve the slow inference speeds that conflict with highfrequency robotic control requirements, recent studies have systematically optimized VLA efficiency from three perspectives. They refine model architectures to enable dynamic and lightweight computation, reduce overall parameter sizes to lower deployment barriers, and accelerate decoding strategies to generate actions more rapidly. 

**Architectural Optimization** . These works aim to improve efficiency by adjusting the VLM architecture in VLA. As illustrated in “Architectural Optimization” of Fig. 4, dynamic inference can be achieved through layer skipping or early exiting, avoiding redundant computation. MoLe-VLA [131] introduces a “Spatio-Temporal Aware Router (STAR)” over the joint projection space of visual and language inputs, dynamically computing routing weights to select the most relevant LLM layers. This mechanism efficiently activates critical layers while skipping redundant ones, enabling fast and semantically sensitive inference. DeeR-VLA [39] enables dynamic inference by adding multiple early exits within the LLM. Adjacent exits compare output consistency to determine whether inference can be terminated early, avoiding unnecessary deep-layer computation. Unlike dynamic inference, RoboMamba [129] uses a linear-complexity Mamba backbone [142] and pose head, reporting 9.0 Hz on A100 versus 3.4 Hz for OpenVLA-7B [29]. However, this _∼_ 3 _×_ gain over OpenVLA is based on an SE(3) pose-prediction interface and does not imply universal superiority over generalist autoregressive VLAs. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

8 

**Parameter Optimization** . Reducing model size directly lowers deployment difficulty. As shown in Fig. 4 under “Parameter Optimization”, model compression directly reduces the parameter count. BitVLA [133] introduces the first “1bit” weight VLA model, using distillation-aware training to quantize the vision encoder and adopting the “1-bit” weight BitNet b1.58 [143] as its LLM. On the other hand, NORA [48] pairs a compact, high-quality VLM with a FAST+ [144] tokenizer that compresses high-dimensional actions into short token sequences. It demonstrates that a well-designed small model can outperform larger models. 

**Inference Acceleration** . This line of work seeks to enhance inference efficiency by accelerating the process of action decoding during inference. The most notable aspect is that most models replace autoregressive decoding with parallel decoding. Fig. 4 under “Inference Acceleration” shows that decoding speed can be improved by modifying the LLM decoding process or using a specialized action head. In this way, a complete action sequence can be generated in a single forward pass. RoboFlamingo [128] separates perception and policy, using an independent MLP action head to convert VLM outputs into actions. This enables the generation of stacked actions in one pass. OpenVLA-OFT [47] replaces the causal attention mask with a bidirectional one, enabling empty action embeddings to be filled in one pass and converted to continuous actions via an MLP. PDVLA [130] reformulates autoregressive decoding as a nonlinear equation system solved via fixed-point iteration. Bidirectional attention updates action tokens until convergence, thereby enabling parallel decoding. 

Different from parallel decoding, Spec-VLA [134] explores speculative decoding in VLA models. With Relaxed Acceptance to increase the verification model’s acceptance rate for draft model predictions, it achieves a 1.42 _×_ speedup over the baseline. Beyond decoding, FlashVLA [132] addresses redundancy by using FlashTrigger to evaluate the stability of actions and the environment and decide whether to skip the current inference, significantly reducing latency. 

In summary, current optimization methods significantly improve the efficiency of model inference and deployment by compressing parameter sizes, pruning redundant computations, and parallelizing the decoding process. While they successfully bridge the gap between heavy foundation models and real-time robotic constraints, these efficiency gains often come at the expense of reasoning depth and task accuracy. Aggressive quantization and pruning strategies can degrade the model’s capability to handle complex tasks. Furthermore, most approaches merely adapt standard LLM optimization techniques rather than addressing the unique spatial-temporal nature of embodied control. Moving forward, true efficiency will require a shift from simple structural compression to embodiment-native designs. Developing dual-system paradigms that decouple high-level deliberate reasoning from high-frequency instinctive motor control offers a promising solution to these challenges. Ultimately, the field must seek an optimal equilibrium that preserves the emergent intelligence of massive models within the ultra-low latency required by the physical world. 


Fig. 5: Comparison of representative paradigms in monolithic dual-system models. Sec. 3.2.1 introduces cascadebased methods, where the VLM backbone is cascaded with the action expert to forward its output features in a single pass to the action expert. Sec. 3.2.2 introduces parallel-based methods, where the VLM backbone and the action expert operate in parallel and interact in various ways. 

### **3.2 Dual-system Models** 

The need to simultaneously handle the demands of deep reasoning and real-time action generation has prompted the development of monolithic dual-system VLA architectures. These models adopt two distinct systems: a larger and slower System 2 for high-level reasoning and planning, and a smaller and faster System 1 for low-level action generation. This separation enables a faster response time and smoother real-world deployment. It delivers both solid strategic planning and high-speed control for robotic manipulation. The separated low-level control module is also more adaptable to task-specific optimization. The key distinction between this approach and single-system models lies in the introduction of an action expert to explicitly decouple action generation. In contrast to hierarchical models, its major difference is that it does not produce an interpretable intermediate output. Tab. 2 summarizes representative dual-system methods. Fig. 5 illustrates two representative architectures: cascade-based methods and parallel-based methods. This categorization is grounded in how System 2 interacts with System 1. Cascade-based designs follow a sequential interaction pattern, where high-level planning precedes lowlevel execution, while parallel-based designs adopt a tightly coupled paradigm with continuous interaction between the two systems during inference. This distinction leads to different trade-offs in information flow, system coupling, and real-time responsiveness. 

### _3.2.1_ **_Cascade-based Methods_** 

Following the above categorization, we first examine cascade-based methods, which adopt a sequential interaction pattern between the two systems. In this paradigm, high-level reasoning is performed prior to low-level action execution, resulting in a clear temporal separation between planning and control. 

As shown in the upper part of Fig. 5, cascade-based dualsystem VLA models separate high-level semantic reasoning from low-level real-time control in a serial manner. The high-level system (System 2) typically employs VLMs to process multimodal input, perform semantic grounding, 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

9 

TABLE 2: Dual-system VLA models. The “System 2 Backbone” column lists the VLM backbone used as the System 2 component in dual-system methods. The “System 1 Learning” column lists the learning methods used by the action experts as System 1. “Diff.” denotes diffusion-based learning, “FM” denotes flow-matching, “MSE” denotes mean squared error, “BCE” denotes binary cross-entropy, and “AR” denotes autoregressive learning. 

|**Model**|**System 2**<br>**Backbone**|**System 1**<br>**Learning**|**Contribution**|
|---|---|---|---|
||||**Cascade-based**|
|DP-VLA [145]|OpenVLA|Regression|Propose a dual-system architecture for robot manipulation with efficiency and performance.|
|RoboDual [146]|OpenVLA|Diff.|Combine a VLA-based generalist for reasoning and a DIT specialist for control.|
|LCB [147]|LLaVA|Diff.|Leverage an added special token to encode VLM reasoning and act as conditions for policy.|
|GR00T N1 [35]|Eagle-2|FM|Combine a VLM and DiT for humanoid robots manipulation.|
|CogACT [148]|OpenVLA|Diff.|Propose an action ensemble algorithm to integrate the action diffusion process into VLA.|
|HiRT [149]|InstructBLIP|Regression|Propose a dual-system model with System 2 running at a lower frequency.|
|Fast-in-Slow [43]|Prismatic|Diff., AR|Propose a unified dual-system model that embeds fast execution within a VLM-based reasoner.|
|OpenHelix [61]|LLaVA|Diff.|Conduct auxiliary training on the token bridging VLM and policy.|
|ChatVLA [150]|Qwen2-VL|Diff.|Unifie vision-language-action via MoE-shared attention with separate perception/control FFNs.|
|ChatVLA-2 [151]|Qwen2-VL|Diff.|Enable open-world robotic reasoning via dynamic MoE routing and Reasoning-Following MLP.|
|Diffusion-VLA [152]|Qwen2-VL|Diff.|Merge Qwen2-VL reasoning with diffusion actions via FiLM-modulated reasoning injection.|
|TriVLA [153]|Eagle-2|Diff.|Introduce a world-dynamics perception module as system 3 to complement static perception.|
|GF-VLA [154]|LLaMA 2|Regression|Enable interpretable bimanual manipulation via information-theoretic graphs from human videos.|
|RationalVLA [155]|LLaVA-v1.5|Diff.|<br>Introduce a learnable latent interface to enable instruction rejection for robust manipulation.|
|VQ-VLA [156]|OpenVLA|VQ-VAE|Develop a vector quantization-based action tokenizer for efficient and smoother control.|
|TinyVLA [157]|LLaVA|Diff.|Demonstrate that high-performance VLAs require no large-scale robotic pretraining.|
||||**Parallel-based**|
|_π_0 [32]|PaliGemma|FM|Combine a pre-trained Vision-Language Model with a Flow Matching-based Action Expert.|
|_π_0-FAST [144]|_π_0|AR|Propose a DCT-based action tokenization enabling efficient autoregressive VLA training.|
|_π_0_._5 [33]|PaliGemma|FM|Convert high-level prompts into more fine-grained subtask predictions before feeding into_π_0|
|_π_0_._5-KI [40]|PaliGemma|FM|Prevent gradients from the action expert from flowing into the VLM backbone during training.|
|ForceVLA [158]|_π_0|Diff.|Treat force sensing as a first-class modality via MoE, improving contact-rich manipulation.|
|SmolVLA [34]|SmolVLM-2|FM|Propose a lightweight VLA with frozen SmolVLM-2 and flow-matching transformer.|
|OneTwoVLA [159]|_π_0|FM|Integrate acting/reasoning in shared VLA backbone processing multi-view inputs.|
|Tactile-VLA [160]|_π_0|FM|Integrate tactile sensing to enable force-aware, generalizable contact-rich manipulation.|
|GR-3 [161]|Qwen2.5-VL|FM|Combine VL data and few-shot trajectories for robust manipulation in long-horizon or unseen tasks.|
|villa-X [162]|PaliGemma|FM|Integrate proprioceptively grounded latent actions and robot actions in a joint diffusion process.|
|GraspVLA [163]|InternLM2|FM|Enable sim-to-real and open-vocabulary grasping with synthetic data.|


and generate action plans. These plans are encoded as latent cognitive representations rather than being executed directly. The low-level system (System 1) then decodes these representations into executable robot actions at a higher frequency, significantly improving run-time efficiency and facilitating real-world deployment. Fig. 5 shows two architectures, differing in how the action expert is designed. 

To decouple the capabilities of “cognition” and “action” of the model, many methods select a separate model to serve as the action expert. As shown in the “Separate Action Expert” part at the top-left of Fig. 5, the VLM backbone transmits features to the action expert to convey information derived from visual, textual, and robot-specific state inputs. For example, CogACT [148] introduces the diffusion transformer (DiT) [164] as an action model. In particular, it also proposes an adaptive action ensemble algorithm for smoother and more efficient movement trajectories. GR00T N1 [35] also adopts a dual-system architecture in which DiT is introduced as the low-level action model. Both systems are tightly coupled and jointly trained end-to-end, enabling much faster policy steps. Some models adopt a similar architecture, but do not employ a DiT. For example, DP-VLA [145] uses a Behavioral Cloning transformer [165] instead. 

Many models have made variations based on this. The HiRT model [149] uses VLM to operate at a lower frequency. This process extracts features for long-term understanding 

of the scene. Then a lightweight visual action strategy is deployed at a higher frequency. This design enables more efficient robotic manipulation and allows the system to keep up with changes in the real-world environment during deployment. TriVLA [153] is a three-module system incorporating a video generation model to predict future frames, a VLM to interpret instructions, and a diffusion action expert. GF-VLA [154] extracts information–based hand–object and object–object scene graphs from human demonstrations, then fuses them with an LLM to generate interpretable behavior trees and low-level Cartesian actions for dual-arm control. RationalVLA [155] couples a VLM with a diffusion policy through a learnable latent interface. The VLM emits a token serving as the condition of the controller for action generation or a token to refuse infeasible commands. VQVLA [156] adopts a convolutional residual VQ-VAE [166], which is pretrained with action sequence, to take the place of the binning method of OpenVLA [29]. The model shows linear performance gains from more simulated data and has less sim-to-real gap. Some models integrate the action expert into the VLA backbone, Fast-in-Slow [43] is a typical example. As shown in the “Unified Action Expert” part at the top-right of Fig. 5, the action expert utilizes the final transformer blocks of the VLM backbone. They run at different frequencies, enabling seamless coordination between the two systems within a single pretrained model. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

10 

In cascaded VLA models, the action expert serves as the core component. Based on the underlying learning paradigm, they can be broadly categorized into four classes: regression, discretization, diffusion, and flow matching. Each class adopts distinct architectures: **(1)** regressionbased methods typically employ a Transformer encoder with an MLP head to directly predict continuous actions; **(2)** discretization-based methods leverage VQ-VAE [166] to compress continuous actions into discrete codebooks; **(3)** diffusion-based methods utilize 1D U-Net [167] or DiT [164] to model complex action distributions via iterative denoising; and **(4)** flow matching methods generally build vector field networks upon DiT, enabling efficient generation through ordinary differential equation trajectories. These paradigms reflect fundamental trade-offs among architectural simplicity, expressive power for complex action distributions, computational efficiency, and quantization error. 

Overall, cascade-based designs emphasize modular decomposition between cognition and action, while differing primarily in the implementation of the action expert, setting the stage for more tightly coupled interaction paradigms explored in parallel-based methods. However, this explicit separation also introduces inherent limitations: the lack of real-time feedback from the action system can reduce adaptability in dynamic environments, and errors in highlevel planning may propagate to execution without timely correction. As a result, although cascade-based methods offer strong interpretability and stable optimization, they often face challenges in responsiveness and robustness under rapidly changing conditions. 

### _3.2.2_ **_Parallel-based Methods_** 

In contrast to cascade-based designs, parallel-based methods adopt a tightly coupled interaction pattern between high-level reasoning and low-level control. Instead of enforcing a strict temporal separation, the two systems operate simultaneously and continuously exchange information during inference. 

As shown in the lower part of Fig. 5, parallel-based dualsystem VLA designs an action expert operating in parallel with the VLM backbone. The two components interact to exchange information during inference. Based on the choice of action expert and the interaction mechanism, two categories in Fig. 5 are defined. 

As shown in the “Shared-attention Architecture” part at the bottom-left of Fig. 5, this architecture draws inspiration from the mix-of-experts (MoE) framework [168]. They leverage token interactions within self-attention layers, which are shared by the VLM backbone and the action expert to separate high-level reasoning from low-level execution. Information derived from visual and textual inputs interacts with noise and robot-specific inputs within the shared self-attention layers. This design facilitates taskspecific optimization. For example, this design allows for the incorporation of a true MoE or other specially designed architectures within the action expert. A typical example is _π_ 0 [32]. Its backbone weights are initialized from a pretrained VLM. To handle robot-specific inputs and action generation, a second set of independent weights, the flowmatching-based action expert, is introduced and trained from scratch. ForceVLA [158] uses _π_ 0 [32] as the base model, 

the FVLMoE module with MoE is used to introduce the force modality into VLA. OneTwoVLA [159] is based on _π_ 0 [32] and can switch between two modes: explicitly reasoning and generating actions based on the most recent reasoning. This architecture makes it easier for the two systems to operate asynchronously and further improves efficiency. 

Many innovations are built upon this. _π_ 0 _._ 5 [33] builds on _π_ 0 [32] by introducing an additional step. The VLA module integrates visual information to convert high-level prompts into more fine-grained subtask predictions, which are then processed by the dual-system architecture of _π_ 0 [32]. _π_ 0 _._ 5-KI [40] builds on _π_ 0 _._ 5 [33]. During training, it prevents gradients from the action expert from flowing into the VLM backbone during training to preserve the VLM’s knowledge advantage. _π_ 0-FAST [144] introduces a DCTdriven action tokenization approach that facilitates efficient autoregressive training of VLA models. GraspVLA [163] proposes a dual-system model via Progressive Action Generation (PAG), which unifies autoregressive perception tasks and flow-matching-based action generation into a Chain-ofThought process. This design enables joint training on synthetic and Internet data, achieving direct sim-to-real transfer and open-vocabulary grasping. villa-X [162] grounds latent actions in robot states and jointly models latent and robot actions via joint diffusion for structured vision-action integration. Tactile-VLA [160] integrates tactile sensing into VLA models with hybrid position–force control. As shown in the “Cross-attention Architecture” part at the bottomright of Fig. 5, this architecture feeds the visual, textual, and state inputs into the VLM, where the self-attention layers generate key–value and pass key–value to the action expert’s cross-attention layers. For instance, SmolVLA [34] adopts this architecture. It improves efficiency by leveraging a lightweight and frozen VLM backbone and training only a downstream Flow Matching Transformer as the action expert. Another example is GR-3 [161], which unifies visionlanguage understanding with robot trajectory learning. 

Overall, parallel-based designs emphasize tight coupling and continuous interaction between cognition and action, enabling real-time adaptability and responsive behavior in dynamic environments. By allowing bidirectional information flow during inference, these methods can better adjust actions based on evolving observations and intermediate reasoning states. However, this strong interdependence also introduces challenges: the increased system coupling complicates optimization and training stability, and the lack of clear modular boundaries can reduce interpretability and flexibility for component-level improvements. As a result, while parallel-based methods excel in responsiveness and adaptability, they often face difficulties in scalability and maintainability compared to cascade-based designs. 

## **4 HIERARCHICAL MODELS** 

Hierarchical modelling serves as a foundational paradigm in large VLM-based VLA models, particularly in scenarios where long-horizon reasoning, spatial abstraction, or action decomposition is required. These models are typically composed of a high-level planner and a low-level policy, as illustrated in Fig. 3 right. The planner receives instructions 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

11 


Fig. 6: A diagram showing the hierarchical models in this survey. These models are divided into two categories according to their constitutions, i.e., Planner-Only (Sec. 4.1) and Planner+Policy (Sec. 4.2). Based on the intermediate representation type, one category can be further divided into subtask-based (S), keypoint-based (K), and program-based (P). “(A)” denotes methods combining affordance for auxiliary purposes. 

and observations, transforming them into interpretable intermediate representations. The policy then accepts these representations and generates action sequences or codes that robots can directly execute. A summary of hierarchical models is provided in Tab. 3. 

Importantly, the planner and policy in hierarchical models can operate independently, without either module being strictly dependent on the other. This modularity enables flexible combinations: many works focus solely on designing the planner component, leveraging existing off-the-shelf policies for execution. Therefore, we divide hierarchical models into two categories: Planner-Only (Sec. 4.1) and Planner+Policy (Sec. 4.2). Unlike dual-system VLA models, which also involve multiple modules, the intermediate representations in hierarchical models are explicitly interpretable to humans. Based on their nature, each category can be further divided into subtask-, keypoint-, and programbased methods. A comparative analysis of monolithic and hierarchical models is presented in Sec. 4.3. 

### **4.1 Planner-Only** 

### _4.1.1_ **_Program-based Methods_** 

Among the intermediate representations, programs are uniquely characterized by their capacity to encapsulate complex logic, conditional control flows, and precise parameterizations into highly structured text. By leveraging the inherent code-generation proficiencies of large foundational models, this category focuses on translating high-level task goals into strict algorithmic sequences. In this approach, planners generate intermediate programs for robotic manipulation, which fall into two categories: robot-executable programs and auxiliary programs. Robotexecutable programs are built on robot libraries and can be 

directly executed to control the robot. For instance, Chainof-Modality [172] employs a multimodal prompting strategy, where the VLM is engaged in a multi-turn conversation across different modalities and ultimately generates a robotexecutable Python program to reproduce the task. Similarly, Instruct2Act [180] produces Python code that invokes APIs to control robot actions. In contrast, auxiliary programs support the policy in task understanding but cannot be executed directly. ROVI [173] exemplifies this category by generating auxiliary programs to describe the potential action and resolve the actual execution through translational and rotational costs. Likewise, ReLEP [174] uses a VLM with a memory bank to decompose tasks into basic skills from a skill library. It produces plans in the form of auxiliary programs that enable strong long-horizon performance. 

In summary, program-based methods excel in orchestrating complex, multi-step tasks by abstracting manipulation into semantic logic and API calls. While this algorithmic abstraction is highly effective for tasks with clear procedural structures, other scenarios demand precise, continuous geometric reasoning directly within the visual observation. This alternate focus on spatial grounding characterizes keypointbased methods, as discussed next. 

### _4.1.2_ **_Keypoint-based Methods_** 

While program-based methods emphasize logical control flow, keypoint-based planners shift the focus toward precise spatial reasoning directly within the visual observation. More broadly, we use “keypoint” as a general term for grounded intermediate subgoals that specify where or how to interact. These representations extend beyond sparse points to include continuous waypoints, visual sketches, and even non-visual coordinate sequences. Low-level con- 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

12 

TABLE 3: Hierarchical VLA models. The “Type” column denotes the output type of the planner, where “K” represents Keypoint, “S” represents Subtask, and “P” represents Program. The “Learning” column specifies the learning method adopted by the model, where “SFT” refers to Supervised Fine-Tuning, “RL” denotes Reinforcement Learning, “IM” indicates Imitation Learning, and “API” is a special case referring to the invocation of pre-existing models. 

|**Model**|**Type**|**Backbone**|**Learning**|**Contribution**|
|---|---|---|---|---|
|||||**Planner-Only**|
|MoManipVLA [169]|K|OpenVLA-7B|IM|Leverage VLA models to predict waypoints and optimize full-body trajectories.|
|ManipLVM-R1 [49]|K|Qwen2.5-VL-3B|RL|GRPO tuning for affordance and trajectory, robust performance in OOD situations.|
|PaLM-E [21]|S|PaLM|SFT|Train a VLM capable of general VQA and robot manipulation instruction generation.|
|Emb-Reas [50]|S|Qwen2-VL-7B|SFT|Construct a VLM and open-sourced dataset with planning, reasoning, and reflection.|
|RoboPoint [170]|K|Vicuna-v1.5-13B|SFT|Finetune VLM for spatial affordance prediction in the form of keypoints.|
|Reinforced [171]|S|Qwen2.5-VL-7B|SFT, RL|Conduct GRPO on a finetuned model, bringing better generalization to unseen.|
|CoM [172]|P|Gemini 1.5 Pro|API|Sequential multimodal prompting to extract force-aware manipulation from demos.|
|RoVI [173]|K, P|GPT-4o / LLaVA-13B|SFT|Visual sketch-based instruction and hierarchical pipeline for precise manipulation.|
|ReLEP [174]|P|LLaVA-1.6-7B|SFT|A planning framework with implicit logical inference and hallucination mitigation.|
|ViLa [175]|S|GPT-4V|API|A VLM planner integrating perception and reasoning without affordance models.|
|RoboBrain [176]|K, S|LLaVA|SFT|Provide a hierarchical VLA focus on planning, affordance, and trajectory.|
||||**P**|**lanner+Policy**|
|HAMSTER [51]|K|VILA-1.5-13B|SFT, IM|Propose an out-of-the-box way for trajectory prediction to assist the low-level policy.|
|HiRobot [177]|S|PaliGemma-3B,_π_0|SFT, IM|A hierarchical VLA with high explainability and capacity for complex tasks.|
|Agentic Robot [178]|S|GPT-4o|SFT|A closed-loop hierarchical pipeline where a VLM is attached to a completion judge.|
|DexVLA [179]|S|Qwen2-VL|SFT, IM|Combine a VLM with a large diffusion head up to 1B and a 3-stage training recipe.|
|Instruct2Act [180]|P|ChatGPT|API|Generate programs that call APIs for mapping from instructions to actions.|
|RoboMatrix [181]|S|Vicuna 1.5|SFT|VLA with modular scheduling layer, skill layer, and hardware layer.|
|PointVLA [182]|S|Qwen2-VL|SFT|Attach VLA with a point cloud encoder and injector to equip spatial perception.|
|_A_0 [52]|K|Qwen2.5-7B|SFT, API|Hierarchical affordance-aware diffusion with embody-agnostic keypoint prediction.|
|FSD [183]|S|CLIP, Vicuna|SFT|Propose the generation of visual aids via SrCoT for zero-shot manipulation.|
|RoBridge [184]|S|GPT-4o|IM, RL|Bridge VLM cognition with RL execution via invariant operable representation.|
|Robocerebra [185]|S|GPT-4o, Qwen2.5-VL|SFT|A novel benchmark and hierarchical framework for long-horizontal evaluation.|
|DexGraspVLA [186]|S|Qwen-VL|API, IM|Combine a VLM as a high-level planner with a low-level diffusion-based policy.|
|RT-H [31]|S|PaLI-X 55B|SFT, IM|An action hierarchy architecture using language motion as a middle representation.|
|ReKep [53]|K, P|GPT-4o|API|Training-free trajectory generation by keypoint constraints for manipulation.|
|VoxPoser [187]|P|GPT-4|API|Propose language-guided 3D value maps with zero-shot generalization capabilities.|
|SkillDiffuser [188]|S|Transformer|IM|A hierarchical VLA with high-level model and low-level model.|
|RT-Affordance [189]|K|PaLM-E 2|SFT, IM|<br>Use visual affordances as intermediate features for web-robot knowledge transfer.|
|HiBerNAC [190]|S|PaLM2|SFT|Propose an asynchronous model that mimics the hierarchical structure of the brain|
|LLARVA [191]|K|Llama 2 7B|SFT, IM|A vision-action instruction tuning paradigm and a large instruction tuning dataset.|
|MALMM [192]|S, P|GPT-4-Turbo|API|Three-agent system combining planner, supervisor, and coder without post-training.|
|VLA-Touch [193]|S|GPT-4o|IM|Integrate tactile sensing into VLA control via diffusion-based imitation learning.|


trollers then consume these spatial descriptors to generate continuous actions. Under this broad definition, we categorize existing methods by the complexity of their spatial representations, ranging from discrete waypoints to rich visual sketches. At the foundational level, several methods tackle robotic manipulation by predicting explicit waypoints. MoManipVLA [169] generates a key waypoint at each step through a VLA model, which is subsequently refined into executable actions via a bi-level trajectory optimization framework. Other approaches emphasize affordance-driven keypoints to capture task-relevant semantics. RoboPoint [170] interprets natural language instructions to generate visual keypoints that specify precise manipulation targets. Building on this, recent models often form hybrid representations. ManipLVM-R1 [49] trains a VLM with Group Relative Policy Optimization (GRPO) [194] to predict both the affordance area for grasping and the trajectory of the target object, thereby yielding a more generalizable planner. Similarly, RoboBrain [176] integrates task planning, affordance perception, and trajectory estimation by combining LLaVA [26] for high-level planning with an A-LoRA module to identify interactable regions and a T-LoRA module to predict trajectory waypoints. Moreover, some works explore 

richer forms of spatial guidance, such as trajectories and visual sketches. RoVI [173], for instance, employs a sketchbased interface, extracting starting points, waypoints, and endpoints from hand-drawn annotations using YOLOv8, which are then applied as trajectory constraints. 

Collectively, these keypoint-based methods highlight the advantage of bridging high-level VLM reasoning and lowlevel control through interpretable, spatially grounded intermediate representations. 

### _4.1.3_ **_Subtask-based Methods_** 

Distinct from the rigid logic of programs and the geometric constraints of keypoints, subtask-based methods leverage natural language instructions to maximize semantic flexibility and open-world generalization.In this approach, the planner is typically a large VLM that receives high-level implicit instructions (e.g., clean up the table) along with observations, and decomposes them into step-by-step textual commands. Since these models produce interpretable intermediate instructions rather than executable actions, a low-level control policy is still required in practical deployment. Early efforts such as PaLM-E [21], a LLaVA-style VLM trained with robotic manipula- 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

13 

tion data, demonstrate the feasibility of unifying general VQA capabilities with robot command generation. Building upon this direction, Embodied-Reasoner [50] introduces Observation–Thought–Action trajectories to support spatial analysis, reflection, and verification during step-wise planning. Reinforced Planning [171] retains this subtaskdecomposition setup but boosts generalization through a two-stage pipeline of SFT followed by GRPO-based reinforcement fine-tuning. Meanwhile, some systems decouple perception from reasoning: Embodied-R [195] combines a large VLM for perception with a small LM for reasoning for embodied spatial reasoning on video, and its reasoning traces can be leveraged to derive stepwise subtask proposals for manipulation. In contrast, ViLA [175] leverages GPT-4V as an external planner, prompting it to generate candidate task plans from textual and visual inputs and then executing only the first command, discarding the remainder. 

Overall, subtask-based planners translate complex instructions and visual observations into interpretable textual commands to guide execution policies. They excel in generating step-by-step text plans and performing complex tasks, yet their real-world performance remain limited by the capability of low-level control policies. 

### **4.2 Planner+Policy** 

### _4.2.1_ **_Keypoint-based Methods_** 

Within the integrated Planner+Policy architecture, keypointbased methods leverage spatial primitives as a direct geometric bridge between high-level reasoning and low-level execution. By explicitly pairing a VLM planner with a downstream policy designed to consume these visual anchors, these models ensure that the planner’s spatial intent is rigorously adhered to during continuous control. This type of model generally uses a large VLM to ground subgoals as spatial primitives, spanning from discrete keypoints and continuous 2D trajectories to affordance representations and visual sketches. The low-level policy then consumes these primitives to predict continuous trajectories and control. For instance, HAMSTER [51] first predicts trajectory keypoints from instructions and observations. Then it links these keypoints into an ordered path with a gradient color, and overlays this guidance for policy execution. Besides, ReKep [53] utilizes DINOv2 [138] and SAM [196] to produce keypoint proposals, then uses GPT-4o [197] to turn those keypoints into cost functions. These functions are subsequently solved into waypoints and actions by an optimizer. Moreover, _A_ 0 [52] adopts an affordance-aware hierarchy: the planner predicts contact points and post-contact motion as an embodiment-agnostic affordance representation, which the action policy then converts into control. To further enrich the spatial context, some works leverage visualized images—such as 2D trajectories or sketches overlaid on visual observations—to represent subsequent subtasks. Complementary to sparse point outputs, these trajectory- and sketch-conditioned formulations provide a lightweight yet expressive interface for downstream control. For example, RT-Trajectory [198] enables the policy to follow coarse motion guidance while grounding it in the current visual scene. Similarly, RT-Sketch [199] interprets user-provided sketches 

as subtask goals, effectively guiding the robot even under ambiguous language instructions or visual distractors. 

In summary, coupling a keypoint-generating planner with a dedicated action policy provides robust spatial grounding, making these architectures highly adept at precision-demanding tasks. 

### _4.2.2_ **_Subtask-based Methods_** 

Shifting from the geometric focus of spatial primitives to semantic abstraction, subtask-based hierarchical models utilize natural language as the universal interface between cognition and control. Subtask-based hierarchical models bridge the planner and policy with instructions. The planner plays the same role as a subtask-based planner-only hierarchical model, and a low-level policy is appended to generate action sequences. This explicit pairing allows the high-level VLM to handle complex, open-ended reasoning, while delegating the intricacies of high-frequency physical execution to a specialized downstream policy. A representative example is HiRobot [177], the planner of which accepts open-ended user instructions and then decomposes them into atomic commands for the policy. Similarly, DexVLA [179] features a VLM planner and a diffusion-based action policy. The policy is conditioned on the subtask tokens given by the VLM planner, excelling in complex and long-horizon robotic manipulation tasks. Built on DexVLA, PointVLA [182] enhances spatial perception by incorporating a point cloud encoder and injector into the policy, enabling the model to follow the planner’s instructions in geometrically complex scenes. RoBridge [184] prompts the planner to generate text instructions of primitive actions and form an invariant operable representation for the policy to execute. Besides, SkillDiffuser [188] decomposes complex tasks into subtasks through a high-level model that predicts a set of skills, while a low-level diffusion policy realizes concrete actions. Analogously, RoboMatrix [181] organizes execution into a three-layer hierarchy: a modular scheduling layer generates subtask sequences, the skill layer encodes and selects reusable behaviors, and the hardware layer implements robot control. HiBerNAC [190] proposes an asynchronous, hierarchical framework. In this framework, the multi-agent neural structure first decomposes high-level instructions into structured subtasks. Then, an asynchronous pipeline manages these subtasks and coordinates the reactive VLA to execute the final low-level actions. Moreover, MALMM [192] includes a planner, a supervisor, and a coder. The planner generates subtasks for the coder, and the supervisor coordinates transitions between modules. The coder serves as the policy and converts plans into executable robot code, including actions and positions. 

Ultimately, subtask-based Planner+Policy frameworks demonstrate how natural language can effectively decouple abstract reasoning from motor control. By converting openended goals into structured skill sequences, these models offer a highly interpretable and scalable approach to longhorizon manipulation, complementing the spatial precision of keypoint-based architectures. 

### **4.3 Comparison: Monolithic vs. Hierarchical** 

**Architectural comparison.** The difference between monolithic and hierarchical architectures in large VLM-based 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

14 

VLA models for robotic manipulation lies primarily in how they map visual inputs and linguistic instructions into actions, either through a unified or modular approach. Monolithic models emphasize a single, integrated pipeline that jointly optimizes perception, reasoning, and control to directly translate high-level multimodal semantics into low-level actions. This design enables holistic and tightly coupled learning in robotic manipulation. Conversely, hierarchical architectures adopt a multi-stage design that explicitly separates high-level planning from low-level policy execution, promoting modularity and interpretability. This system decomposition allows components to be independently designed, trained, or replaced, enhancing flexibility and easing the integration of domain knowledge or adaptation to new robotic manipulation tasks. 

Another core distinction lies in the inherent nature of the intermediate processing. Monolithic models, while potentially embedding intricate internal reasoning, do so within latent spaces that are often opaque to external inspection. This implicit strategy allows them to fully exploit the representational capacity of large models, potentially discovering efficient task decompositions not explicitly designed by humans. Hierarchical systems, on the other hand, explicitly commit to generating explicit, human-understandable intermediate outputs. This makes them particularly advantageous in robotic manipulation scenarios that demand explainability, detailed task monitoring, or compatibility with traditional robotics pipelines, where high-level plans can be independently validated or modified. 

Despite these differences, both approaches contribute unique strengths to the evolving landscape of VLA for robotic manipulation. Monolithic models highlight the power of unified learning and minimal manual decomposition, offering a streamlined route to generalization across diverse tasks. Hierarchical frameworks, by explicitly layering cognition and control, provide greater transparency and enhanced modular flexibility, which can be critical for complex multi-stage tasks or safety-critical deployments. Together, these paradigms illustrate complementary strategies for bridging vision-language understanding and embodied action, each offering valuable insights into the design of next-generation intelligent robotic manipulation systems. To further quantify and empirically analyze the performance and inherent trade-offs of these two architectures across practical simulation benchmarks and physical deployments, we present a comprehensive comparative experimental evaluation in **Appx. A** . 

**Practical model selection.** In practice, the architectural choice should be determined by deployment requirements, including control frequency and action precision, reasoning horizon and interpretability, computational and data budgets, and task-specific sensing requirements. To keep the main taxonomy concise, we provide a detailed baselinecentered model-selection guideline in **Appx. D** . The accompanying tables summarize representative single-system, dual-system, and hierarchical methods in terms of their corresponding baselines, addressed limitations, associated trade-offs, and recommended application scenarios. 

TABLE 4: Representative VLA methods grouped into four advanced categories: Reinforcement Learning-based, Training-Free, Learning from Human Videos, and World Model-based approaches. The grouping follows the methodological analysis in Sec. 5. 

|**Description**|**Method**|
|---|---|
|**Reinforcement **|**Learning-based Methods**|
|Use RL to optimize robotic poli-<br>cies through interaction or pre-<br>collected trajectories.|VLA-RL [204], ReWiND [42], Grape [200],<br>TGRPO [205], HIL-SERL [207], ConRFT<br>[208], RLDG [209], iRe-VLA [210]|
|**Trainin**|**g-Free Methods**|
|Improve VLA models via archi-<br>tectural or computational opti-<br>mizations without retraining.|FlashVLA [132], EfficientVLA [211], VLA-<br>Cache [212], PD-VLA [130], SP-VLA [213],<br>BAC [214], FAST [144], RTC [44]|
|**Learning fr**|**om Human Videos**|
|Leverage<br>human<br>videos<br>to<br>adapt robot policies, enabling<br>cross-domain transfer.|Human-Robot Semantic Alignment [45],<br>UniVLA [215], LAPA [216], VPDD [217],<br>3D-VLA [218], Humanoid-VLA [219]|
|**World M**|**odel-based VLA**|
|Integrate predictive world mod-<br>els into VLA to model environ-<br>ment dynamics.|World-VLA [41], World4Omni [46], 3D-<br>VLA [218], RIGVid [220], FoundationPose<br>[221], V-JEPA 2-AC [222]|


## **5 OTHER ADVANCED FIELD** 

Beyond core VLA architectures, we highlight four directions for robustness, efficiency, and long-horizon planning: RLbased optimization, training-free improvements, learning from human videos, and world model-based VLA. Tab. 4 summarizes representative methods. 

### **5.1 Reinforcement Learning-based Methods** 

Reinforcement learning (RL) plays an important role in enhancing VLA’s generalization ability [200] and task completion rate [201]. It can be broadly categorized as online, which optimizes policies through real-time interaction, and offline, which learns from pre-collected trajectories. Most VLA methods are built upon traditional RL algorithms. We list several approaches in Tab. 5. 

Unlike RL in LLMs or VLMs [91], [202], [203] that usually finish generation in a few turns, VLA models typically involve long-horizon tasks with hundreds of steps in one trajectory, making rule-based reward functions prone to sparsity and instability [200], [204]. To address this, many works incorporate learned dense reward signals. VLA-RL [204] trains a Robotic Process Reward Model (RPRM) to predict the success likelihood of action sequences. ReWiND [42] models reward as progress toward the final goal state, assigning higher rewards to states visually closer to task completion. In addition to training a reward model, Grape [200] and TGRPO [205] leverage powerful VLMs [197], [206] via prompting to generate feedback-based reward signals. 

Besides reward sparsity, online learning is sampleinefficient due to slow simulation. To address this, several methods adopt hybrid offline-online training. ReWiND integrates offline Implicit Q-Learning [223] with online Soft Actor-Critic [224], accelerating learning and enhancing safety in real-world deployment. HIL-SERL [207] is based on RLPD and introduces human-in-the-loop intervention in the training process. ConRFT [208] employs a two-phase 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

15 

training scheme: an offline phase using Cal-ConRFT (combining behavior cloning and Q-learning) to initialize policy, followed by online HIL-ConRFT, which balances supervised and RL losses with human-in-the-loop intervention. 

Furthermore, some methods leverage RL as a data engine to enhance generalist robotic models. RLDG [209] is a prime example, which trains expert policies via HIL-SERL [207] to 100% task success, then distills them into foundation models via sft. Similarly, iRe-VLA [210] alternates between online RL (to collect new successful trajectories) and sft on the expanded dataset, progressively improving the model through iterative imitation and exploration. 

### **5.2 Training-Free Methods** 

Training-free methods typically leverage modular and extensible designs to improve existing VLA architectures without training. This enables rapid prototyping, ablation studies, and targeted enhancements while preserving the model’s original capabilities and avoiding additional costs. 

A range of training-free methods has been proposed to improve the efficiency of large VLM-based VLA models efficiency without retraining or architectural changes. A compelling example is FlashVLA [132], which employs a trigger mechanism that skips full decoding when action and visual cues remain stable, selectively reusing or pruning visual tokens. Similarly, EfficientVLA [211] prunes redundant language layers, filters task-relevant visual tokens, and caches intermediate features, while VLA-Cache [212] reuses cached key–value representations [136] of static tokens with task-relevance filtering and layer-adaptive reuse. Beyond these, SP-VLA [213] combines spatio–semantic token pruning with an action-aware scheduler that routes intuitive steps to a lightweight generator and complex ones to the full VLA. Likewise, PD-VLA [130] reformulates autoregressive decoding under action chunking as a parallel fixedpoint iteration, enabling simultaneous token prediction. FAST [144] compresses action sequences via discrete cosine transform and byte-pair encoding to reduce redundancy in high-frequency control, achieving up to 5× faster training. Furthermore, RTC [44] optimizes control-time scheduling by monitoring task progress and adjusting control frequency, reducing unnecessary computation during inference. 

### **5.3 Learning from Human Videos** 

Recent advancements in VLA models have introduced several novel learning paradigms that surpass conventional policy learning strategies. Among them, a notable trend emerges: leveraging human video data to guide robot policy learning, using structural similarities in human-object and robot-object interactions to align visual and temporal cues. 

This method aims to narrow the embodiment gap by transferring task-relevant knowledge from rich human video data. It uses human videos to pre-train perception or adapt policies. For instance, Human-Robot Semantic Alignment [45] aligns vision encoders across domains using paired human-robot videos, while UniVLA [215] learns task-centric latent actions from unlabeled human and robot videos to unify policy planning. Similarly, LAPA [216] leverages VQ-VAE [166] quantized latent actions to pre-train on large-scale video-language pairs, enabling transfer from 

TABLE 5: Representative RL approaches for VLA. ✓ stands for online and ✗ stands for offline. “S” stands for sparse reward, “D” for dense reward, “RM” denotes a pre-trained reward model, “GPT” denotes a reward given by GPT, and “TC” denotes a reward function based on task completion. 

|**Method**|**RL Algo.**|**Online**|**Reward Formulation**|
|---|---|---|---|
|VLA-RL [204]|PPO|✓|TC (S) + RM (D)|
|RIPT-VLA [225]|LOOP|✓|TC (S)|
|RLVLA [201]|PPO|✓|TC (S) + Object Grasp (S)|
|TPO [200]|DPO|✓|TC (S) + GPT (S)|
|ConRFT [208]|-|✗+✓|TC (S)|
|TGRPO [205]|GRPO|✓|TC (S) + GPT (D)|
|iRe-VLA [210]|PPO|✓|TC (S)|
|RLDG [209]|HIL-SERL|✓|TC (S)|
|ReWiND [42]|IQL SAC|✗+✓|TC (S) + RM (D)|
|HIL-SERL [207]|RLPD|✗+✓|TC (S)|


actionless human videos. Besides, VPDD [217] applies discrete diffusion over unified video tokens, facilitating crossdomain knowledge transfer through future dynamics prediction. 3D-VLA [218] integrates human-object interaction videos with robot demonstrations for richer 3D reasoning, and Humanoid-VLA [219] exploits pose-recovered motion trajectories from online videos to enhance motion diversity. Collectively, these methods demonstrate that human video data can substantially enrich robot policy learning, yielding robustness and versatility even with limited robot data. 

### **5.4 World Model-based VLA** 

World models, characterized by their ability to learn compact latent representations of environment dynamics, have emerged as powerful tools for enabling predictive reasoning and long-horizon planning. Recently, the integration of world models into VLA systems has gained traction as a promising strategy to enhance action planning through explicit modeling of environment dynamics. 

Rather than directly generating actions from current observations, these approaches simulate future states, enabling agents to anticipate the consequences of their actions and refine decision-making accordingly. For instance, WorldVLA [41] introduces an autoregressive action world model that jointly learns to predict visual outcomes and generate actions within a unified token-based architecture. This mutual reinforcement between the world model and the action model improves both visual imagination and action fidelity, supporting more robust long-horizon planning. World4Omni [46] employs a large-scale world model to produce subgoal images that depict intermediate task states. These generated visual cues are then used to guide a modular low-level policy, enabling zero-shot manipulation across diverse environments and robot embodiments. 3DVLA [218] employs a generative world model to predict future goal images and point clouds conditioned on instructions, effectively simulating scene dynamics. RIGVid [220] uses a diffusion-based world model to generate candidate task videos, which are then filtered by a VLM for feasibility, with FoundationPose [221] extracting gripper poses for execution. V-JEPA 2-AC [222] builds a latent action-conditioned world model on top of a massive self-supervised video encoder trained on internet-scale data. During inference, it performs model-based planning by simulating future latent 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

16 

states conditioned on goal images, bridging dense video understanding with zero-shot robotic manipulation. 

## **6 CHARACTERISTICS OF VLA MODELS** 

### **6.1 Multimodal Fusion** 

**Shared Embedding Space.** A defining characteristic of large VLM-based VLA models is the use of a shared, semantically aligned representation space for visual observations and linguistic instructions. Such alignment establishes direct semantic correspondence between perception and commands, providing a unified representation basis for subsequent action generation [8]. 

**Multimodal Token-Level Integration.** Beyond representation alignment, many VLA models integrate vision, language, proprioception, and actions at the token level within a unified model [43], [124], [226]. This fine-grained interaction enables information from different modalities to dynamically condition one another throughout the perception– action cycle. 

**Comprehensive Modal Compatibility.** Another characteristic is the extensibility of VLA models to richer sensory modalities beyond conventional vision and language. As discussed in Sec. 3.1.2 recent VLA models have incorporated information such as 3D perception, tactile sensing, and audio to complement visual observations. From a multimodal-fusion perspective, these developments demonstrate the flexibility of VLA frameworks in integrating heterogeneous sensory information while maintaining a unified perception–language–action paradigm. 

### **6.2 Instruction Following** 

**Semantic Instruction Grounding.** Instruction following in large VLM-based VLA models goes beyond the brittle pipelines of traditional robotic systems. These models leverage the world knowledge of pre-trained VLMs to ground natural language instructions into actions dynamically, enabling context-sensitive understanding rather than fixed templates. For instance, ChatVLA-2 [151] can interpret math problems written on whiteboards. Despite lacking explicit training in mathematics, it demonstrates an ability to generalize from visual-linguistic priors. 

**Task Decomposition and Collaboration.** Beyond direct instruction-to-action translation, instruction following often involves hierarchical task decomposition, especially for long-horizon tasks. Specifically, high-level commands are broken down into sub-goals, which are then executed by low-level controllers [177]. LoHoVLA [123] exemplifies this paradigm by generating intermediate subtasks from visual and language inputs, which guide action generation and maintain semantic alignment throughout execution. By continuously synchronizing subtask intentions with actions, the model maintains coherence in long-horizon tasks, supporting reliable goal completion. 

**Explicit Reasoning via Chain-of-Thought.** A key fact of the instruction following capability of VLA models is the integration of chain-of-thought reasoning into the decisionmaking loop. In CoT-VLA [36], for instance, the model interposes latent visual goals—predicting future images—before generating corresponding action sequences, effectively embedding a sub-goal generation mechanism. This explicit 

reasoning ties instructions to anticipated visual outcomes. It helps mitigate shortsighted hallucinations frequently observed in monolithic systems. In addition, it allows iterative refinement of plans, thereby facilitating more reliable execution of complex, multi-step tasks. 

### **6.3 Multi-Dimensional Generalization** 

**Cross-Task Generalization.** Most VLA models exhibit zeroshot and few-shot generalizations, representing a leap beyond the brittle performance of traditional robotic manipulation models that often require extensive retraining. A prime example is DexVLA [179], which couples a large VLM with a billion-parameter diffusion action expert and an embodied curriculum to transfer skills across embodiments and rapidly adapt to unseen tasks. Without taskspecific tuning, it attains consistently high success on diverse manipulations and generalizes to novel objects and scenes. Under direct language prompting, it also completes complex long-horizon workflows and outperforms state-ofthe-art baselines such as OpenVLA [29] and _π_ 0 [32]. 

**Cross-Domain Data Generalization.** This capacity extends further: _π_ 0 _._ 5 and similar “foundation VLA” models are co-trained on heterogeneous data—web text, simulation videos, and cross-robot embodiments—to acquire broad contextual and semantic understanding. As a result, they successfully deploy “out-of-the-box” in new home environments, executing multi-stage tasks like dishwashing with OOD success rates exceeding 90% [32]. This wide compatibility starkly contrasts with traditional pipelines, which typically collapse outside their training distribution. 

**Cross-Embodiment and Sim-to-Real Generalization.** Cross-embodiment and sim-to-real transfer represent another dimension of generalization. Hierarchical VLA architectures, which learn high-level planners in VLM space and delegate low-level control to domain-specific decoders, enable leveraging off-domain data (e.g., hand-drawn sketches or simulations in diverse setups) to generalize across varying dynamics and robot morphologies. One such model, HAMSTER [51], achieves a 20% success boost over OpenVLA across seven axes of generalization. 

## **7 CONCLUSION** 

In conclusion, this survey presents a comprehensive synthesis of large VLM-based VLA models in robotic manipulation. By proposing a taxonomy of Monolithic and Hierarchical architectures, alongside a unified framework of datasets, benchmarks, and advanced learning paradigms, we structure the current landscape and its defining characteristics. Looking forward, future priorities must address cross-embodiment adaptation, scalable real-world deployment, and tighter coupling of reasoning and execution using internet-scale data. We aim for this survey to serve as a foundational step toward embodied AI that unifies perception, language, and action. 

## **REFERENCES** 

> [1] Z. Xu, K. Wu, J. Wen _et al._ , “A survey on robotics with foundation models: toward embodied ai,” _arXiv:2402.02385_ , 2024. 

> [2] Y. Ma, Z. Song, Y. Zhuang _et al._ , “A survey on vision-languageaction models for embodied ai,” _arXiv:2405.14093_ , 2024. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

17 

- [3] W. Wu, H. He, Y. Wang _et al._ , “Metaurban: a simulation platform for embodied ai in urban spaces,” in _ICLR_ , 2025. 

- [4] K. Zhang, P. Yun, J. Cen _et al._ , “Generative artificial intelligence in robotic manipulation: a survey,” _arXiv:2503.03464_ , 2025. 

- [5] Y. Liu, W. Chen, Y. Bai _et al._ , “Aligning cyber space with physical world: a comprehensive survey on embodied ai,” _arXiv:2407.06886_ , 2024. 

- [6] Y. Liu, X. Cao, T. Chen _et al._ , “A survey of embodied ai in healthcare: techniques, applications, and opportunities,” _INFORM FUSION_ , vol. 119, p. 103033, 2025. 

- [7] S. Nahavandi, R. Alizadehsani, D. Nahavandi _et al._ , “Machine learning meets advanced robotic manipulation,” _INFORM FUSION_ , vol. 105, p. 102221, 2024. 

- [8] R. Sapkota, Y. Cao, K. I. Roumeliotis _et al._ , “Vision-languageaction models: concepts, progress, applications and challenges,” _arXiv:2505.04769_ , 2025. 

- [9] A. Billard and D. Kragic, “Trends and challenges in robot manipulation,” _Science_ , vol. 364, p. eaat8414, 2019. 

- [10] C. Wen, X. Lin, J. So _et al._ , “Any-point trajectory modeling for policy learning,” in _RSS_ , 2024, p. 92. 

- [11] P.-L. Guhur, S. Chen, R. G. Pinel _et al._ , “Instruction-driven historyaware policies for robotic manipulations,” in _CoRL_ , 2023, pp. 175– 187. 

- [12] M. Xu, Z. Xu, Y. Xu _et al._ , “Flow as the cross-domain manipulation interface,” in _CoRL_ , 2024. 

- [13] J. Gu, S. Kirmani, P. Wohlhart _et al._ , “Rt-trajectory: Robotic task generalization via hindsight trajectory sketches,” in _ICLR_ , 2024, pp. 2475–2499. 

- [14] J. Zhao, N. Kuppuswamy, S. Feng _et al._ , “Polytouch: A robust multi-modal tactile sensor for contact-rich manipulation using tactile-diffusion policies,” in _ICRA_ , 2025. 

- [15] V. Mengers and O. Brock, “No plan but everything under control: Robustly solving sequential tasks with dynamically composed gradient descent,” in _ICRA_ , 2025. 

- [16] M. Shridhar, L. Manuelli, and D. Fox, “Cliport: what and where pathways for robotic manipulation,” in _CoRL_ , 2022, pp. 894–906. 

- [17] A. Zeng, P. Florence, J. Tompson _et al._ , “Transporter networks: rearranging the visual world for robotic manipulation,” in _CoRL_ , 2021, pp. 726–747. 

- [18] M. Ahn, A. Brohan, N. Brown _et al._ , “Do as i can, not as i say: grounding language in robotic affordances,” _arXiv:2204.01691_ , 2022. 

- [19] W. Huang, F. Xia, T. Xiao _et al._ , “Inner monologue: Embodied reasoning through planning with language models,” _arXiv:2207.05608_ , 2022. 

- [20] A. Brohan, N. Brown, J. Carbajal _et al._ , “Rt-1: robotics transformer for real-world control at scale,” in _RSS_ , 2023. 

- [21] D. Driess, F. Xia, M. S. M. Sajjadi _et al._ , “Palm-e: an embodied multimodal language model,” in _ICML_ , 2023, pp. 8469–8488. 

- [22] O. Kroemer, S. Niekum, and G. Konidaris, “A review of robot learning for manipulation: Challenges, representations, and algorithms,” _Journal of machine learning research_ , vol. 22, no. 30, pp. 1–82, 2021. 

- [23] H. Liu, C. Li, Y. Li _et al._ , “Improved baselines with visual instruction tuning,” in _CVPR_ , 2024, pp. 26296–26306. 

- [24] W. Dai, J. Li, D. Li _et al._ , “Instructblip: towards general-purpose vision-language models with instruction tuning,” in _NeurIPS_ , 2023, pp. 49250–49267. 

- [25] J. Bai, S. Bai, S. Yang _et al._ , “Qwen-vl: a versatile vision-language model for understanding, localization, text reading, and beyond,” _arXiv:2308.12966_ , 2023. 

- [26] H. Liu, C. Li, Q. Wu _et al._ , “Visual instruction tuning,” in _NeurIPS_ , 2023, pp. 34892–34916. 

- [27] Z. Chen, W. Wang, Y. Cao _et al._ , “Expanding performance boundaries of open-source multimodal models with model, data, and test-time scaling,” _arXiv:2412.05271_ , 2024. 

- [28] Z. Li, B. Yang, Q. Liu _et al._ , “Monkey: image resolution and text label are important things for large multi-modal models,” in _CVPR_ , 2024, pp. 26763–26773. 

- [29] M. J. Kim, K. Pertsch, S. Karamcheti _et al._ , “Openvla: an opensource vision-language-action model,” in _CoRL_ , 2024, pp. 2679– 2713. 

- [30] B. Zitkovich, T. Yu, S. Xu _et al._ , “Rt-2: vision-language-action models transfer web knowledge to robotic control,” in _CoRL_ , 2023, pp. 2165–2183. 

- [31] S. Belkhale, T. Ding, T. Xiao _et al._ , “Rt-h: action hierarchies using language,” in _RSS_ , 2024. 

- [32] K. Black, N. Brown, D. Driess _et al._ , “ _π_ 0: A vision-language-action flow model for general robot control,” in _RSS_ , 2025. 

- [33] P. Intelligence, N. B. Kevin Black, K. D. James Darpinian _et al._ , “ _π_ 0 _._ 5: a vision language-action model with open-world generalization,” _arXiv:2504.16054_ , 2025. 

- [34] M. Shukor, D. Aubakirova, F. Capuano _et al._ , “Smolvla: a visionlanguage-action model for affordable and efficient robotics,” _arXiv:2506.01844_ , 2025. 

- [35] J. Bjorck, F. Casta˜neda, N. Cherniadev _et al._ , “Gr00t n1: an open foundation model for generalist humanoid robots,” _arXiv:2503.14734_ , 2025. 

- [36] Q. Zhao, Y. Lu, M. J. Kim _et al._ , “Cot-vla: visual chain-of-thought reasoning for vision-language-action models,” in _CVPR_ , 2025, pp. 1702–1713. 

- [37] J. Liu, H. Chen, P. An _et al._ , “Hybridvla: collaborative diffusion and autoregression in a unified vision-language-action model,” _arXiv:2503.10631_ , 2025. 

- [38] P. Li, Y. Chen, H. Wu _et al._ , “Bridgevla: input-output alignment for efficient 3d manipulation learning with vision-language models,” _arXiv:2506.07961_ , 2025. 

- [39] Y. Yue, Y. Wang, B. Kang _et al._ , “Deer-vla: dynamic inference of multimodal large language models for efficient robot execution,” in _NeurIPS_ , 2024, pp. 56619–56643. 

- [40] J. T. S. Danny Driess, L. Y. Brian Ichter, K. P. Adrian Li-Bell _et al._ , “Knowledge insulating vision-language-action models: train fast, run fast, generalize better,” _arXiv:2505.23705_ , 2025. 

- [41] J. Cen, C. Yu, H. Yuan _et al._ , “Worldvla: towards autoregressive action world model,” _arXiv:2506.21539_ , 2025. 

- [42] J. Zhang, Y. Luo, A. Anwar _et al._ , “Rewind: language-guided rewards teach robot policies without new demonstrations,” _arXiv:2505.10911_ , 2025. 

- [43] H. Chen, J. Liu, C. Gu _et al._ , “Fast-in-slow: a dual-system foundation model unifying fast manipulation within slow reasoning,” _arXiv:2506.01953_ , 2025. 

- [44] K. Black, M. Y. Galliker, and S. Levine, “Real-time execution of action chunking flow policies,” _arXiv:2506.07339_ , 2025. 

- [45] J. Zhou, T. Ma, K. Y. Lin _et al._ , “Mitigating the human-robot domain discrepancy in visual pre-training for robotic manipulation,” in _CVPR_ , 2025, pp. 22551–22561. 

- [46] H. Chen, B. Wang, J. Guo _et al._ , “World4omni: a zero-shot framework from image generation world model to robotic manipulation,” _arXiv:2506.23919_ , 2025. 

- [47] M. J. Kim, C. Finn, and P. Liang, “Fine-tuning vision-languageaction models: optimizing speed and success,” in _RSS_ , 2025. 

- [48] C.-Y. Hung, Q. Sun, P. Hong _et al._ , “Nora: a small open-sourced generalist vision language action model for embodied tasks,” _arXiv:2504.19854_ , 2025. 

- [49] Z. Song, G. Ouyang, M. Li _et al._ , “Maniplvm-r1: reinforcement learning for reasoning in embodied manipulation with large vision-language models,” _arXiv:2505.16517_ , 2025. 

- [50] W. Zhang, M. Wang, G. Liu _et al._ , “Embodied-reasoner: synergizing visual search, reasoning, and action for embodied interactive tasks,” _arXiv:2503.21696_ , 2025. 

- [51] Y. Li, Y. Deng, J. Zhang _et al._ , “Hamster: hierarchical action models for open-world robot manipulation,” in _ICLR_ , 2025. 

- [52] R. Xu, J. Zhang, M. Guo _et al._ , “A0: an affordance-aware hierarchical model for general robotic manipulation,” _arXiv:2504.12636_ , 2025. 

- [53] W. Huang, C. Wang, Y. Li _et al._ , “Rekep: spatio-temporal reasoning of relational keypoint constraints for robotic manipulation,” in _CoRL_ , 2024. 

- [54] Y. Du, Z. Liu, J. Li _et al._ , “A survey of vision-language pre-trained models,” in _IJCAI_ , 2022. 

- [55] J. Zhang, J. Huang, S. Jin _et al._ , “Vision-language models for vision tasks: A survey,” _TPAMI_ , vol. 46, pp. 5625–5644, 2024. 

- [56] J. Wu, W. Gan, Z. Chen _et al._ , “Multimodal large language models: A survey,” in _BigData_ , 2023, pp. 2247–2256. 

- [57] Z. Li, X. Wu, H. Du _et al._ , “A survey of state of the art large vision language models: Alignment, benchmark, evaluations and challenges,” _arXiv:2501.02189_ , 2025. 

- [58] D. Shu, H. Zhao, J. Hu _et al._ , “Large vision-language model alignment and misalignment: A survey through the lens of explainability,” _arXiv:2501.01346_ , 2025. 

- [59] M. Song, X. Deng, Z. Zhou _et al._ , “A survey on diffusion policy for robotic manipulation: Taxonomy, analysis, and future directions,” _Authorea Preprints_ , 2025. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

18 

- [60] R. Wolf, Y. Shi, S. Liu _et al._ , “Diffusion models for robotic manipulation: A survey,” _arXiv:2504.08438_ , 2025. 

- [61] C. Cui, P. Ding, W. Song _et al._ , “Openhelix: A short survey, empirical analysis, and open-source dual-system vla model for robotic manipulation,” _arXiv:2505.03912_ , 2025. 

- [62] Y. Zheng, L. Yao, Y. Su _et al._ , “A survey of embodied learning for object-centric robotic manipulation,” _MIR_ , vol. 22, pp. 588–626, 2025. 

- [63] G. Chen, L. Shen, R. Shao _et al._ , “Lion: empowering multimodal large language model with dual-level visual knowledge,” in _CVPR_ , 2024, pp. 26540–26550. 

- [64] R. Zhang, R. Shao, G. Chen _et al._ , “Falcon: Resolving visual redundancy and fragmentation in high-resolution multimodal large language models via visual registers,” in _ICCV_ , 2025. 

- [65] L. Shen, G. Chen, R. Shao _et al._ , “Mome: Mixture of multimodal experts for generalist multimodal large language models,” in _NeurIPS_ , 2024. 

- [66] W. Li, B. Hu, R. Shao _et al._ , “Lion-fs: Fast & slow video-language thinker as online video assistant,” in _CVPR_ , 2025. 

- [67] Z. Li, Y. Xie, R. Shao _et al._ , “Optimus-1: Hybrid multimodal memory empowered agents excel in long-horizon tasks,” in _NeurIPS_ , 2024. 

- [68] ——, “Optimus-2: Multimodal minecraft agent with goalobservation-action conditioned policy,” in _CVPR_ , 2025. 

- [69] Q. Ye, Z. Yu, R. Shao _et al._ , “Cat: Enhancing multimodal large language model to answer questions in dynamic audio-visual scenarios,” in _ECCV_ , 2024. 

- [70] ——, “Cat+: investigating and enhancing audio-visual understanding in large language models,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2025. 

- [71] J.-B. Alayrac, J. Donahue, P. Luc _et al._ , “Flamingo: a visual language model for few-shot learning,” _NeurIPS_ , vol. 35, pp. 23716–23736, 2022. 

- [72] Z. Peng, W. Wang, L. Dong _et al._ , “Kosmos-2: Grounding multimodal large language models to the world,” _arXiv:2306.14824_ , 2023. 

- [73] Z. Ma, J. Hong, M. O. Gul _et al._ , “Crepe: Can vision-language foundation models reason compositionally?” in _CVPR_ , 2023, pp. 10910–10921. 

- [74] C.-Y. Hsieh, J. Zhang, Z. Ma _et al._ , “Sugarcrepe: Fixing hackable benchmarks for vision-language compositionality,” _NeurIPS_ , vol. 36, pp. 31096–31116, 2023. 

- [75] D. Shah, B. Osi´nski, S. Levine _et al._ , “Lm-nav: Robotic navigation with large pre-trained models of language, vision, and action,” in _CoRL_ . pmlr, 2023, pp. 492–504. 

- [76] C. Liu, Z. Zhou, J. Zhang _et al._ , “Msnav: Zero-shot visionand-language navigation with dynamic memory and llm spatial reasoning,” _arXiv:2508.16654_ , 2025. 

- [77] X. Tian, J. Gu, B. Li _et al._ , “Drivevlm: the convergence of autonomous driving and large vision-language models,” in _CoRL_ , 2025, pp. 4698–4726. 

- [78] W. Hong, W. Wang, Q. Lv _et al._ , “Cogagent: a visual language model for gui agents,” in _CVPR_ , 2024, pp. 14281–14290. 

- [79] G. Chen, X. Zhou, R. Shao _et al._ , “Less is more: Empowering gui agent with context-aware simplification,” in _ICCV_ , 2025. 

- [80] Y. Lyu, R. Shao, G. Chen _et al._ , “Puma: Layer-pruned language model for efficient unified multimodal retrieval with modalityadaptive learning,” in _ACM MM_ , 2025. 

- [81] Y. Zhu, Y. Lyu, Z. Yu _et al._ , “Emosym: A symbiotic framework for unified emotional understanding and generation via latent reasoning,” in _ACM MM_ , 2025. 

- [82] B. Xie, R. Shao, G. Chen _et al._ , “Gui-explorer: Autonomous exploration and mining of transition-aware knowledge for gui agent,” in _ACL_ , 2025. 

- [83] R. Shao, T. Wu, and Z. Liu, “Robust sequential deepfake detection,” _International Journal of Computer Vision_ , vol. 133, pp. 3278– 3295, 2025. 

- [84] R. Shao, T. Wu, J. Wu _et al._ , “Detecting and grounding multimodal media manipulation and beyond,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 46, pp. 5556–5574, 2024. 

- [85] R. Shao, T. Wu, and Z. Liu, “Detecting and grounding multimodal media manipulation,” in _CVPR_ , 2023. 

- [86] R. Shao, X. Lan, J. Li _et al._ , “Multi-adversarial discriminative deep domain generalization for face presentation attack detection,” in _CVPR_ , 2019. 

- [87] R. Shao, T. Wu, L. Nie _et al._ , “Deepfake-adapter: Dual-level adapter for deepfake detection,” _International Journal of Computer Vision_ , vol. 133, pp. 3613–3628, 2025. 

- [88] J. Chen, D. Yuen, B. Xie _et al._ , “Spa-bench: A comprehensive benchmark for smartphone agent evaluation,” in _ICLR_ , 2025. 

- [89] B. Li, Y. Zhang, D. Guo _et al._ , “Llava-onevision: easy visual task transfer,” _TMLR_ , 2025. 

- [90] S. Bai, K. Chen, X. Liu _et al._ , “Qwen2.5-vl technical report,” _arXiv:2502.13923_ , 2025. 

- [91] W. Huang, B. Jia, Z. Zhai _et al._ , “Vision-r1: incentivizing reasoning capability in multimodal large language models,” _arXiv:2503.06749_ , 2025. 

- [92] A. Radford, J. W. Kim, C. Hallacy _et al._ , “Learning transferable visual models from natural language supervision,” in _ICML_ , 2021, pp. 8748–8763. 

- [93] M. Tan and Q. Le, “Efficientnet: rethinking model scaling for convolutional neural networks,” in _ICML_ , 2019, pp. 6105–6114. 

- [94] M. Shridhar, L. Manuelli, and D. Fox, “Perceiver-actor: A multitask transformer for robotic manipulation,” in _CoRL_ , 2022. 

- [95] Y. Jiang, A. Gupta, Z. Zhang _et al._ , “Vima: general robot manipulation with multimodal prompts,” in _NeurIPS_ , 2022. 

- [96] K. Zheng, X. Chen, O. Jenkins _et al._ , “VLMbench: A compositional benchmark for vision-and-language manipulation,” in _NeurIPS_ , 2022. 

- [97] W. Li, R. Zhang, R. Shao _et al._ , “Semanticvla: Semantic-aligned sparsification and enhancement for efficient robotic manipulation,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 40, no. 22, 2026, pp. 18397–18405. 

- [98] W. Li, J. Liu, L. Yixing _et al._ , “Consisvla-4d: Advancing spatiotemporal consistency in efficient 3d-perception and 4d-reasoning for robotic manipulation,” _arXiv preprint arXiv:2605.05126_ , 2026. 

- [99] Z. Li, B. Hu, R. Shao _et al._ , “Global prior meets local consistency: Dual-memory augmented vision-language-action model for efficient robotic manipulation,” _arXiv preprint arXiv:2602.20200_ , 2026. 

- [100] B. Hu, Z. Li, R. Shao _et al._ , “From abstraction to instantiation: Learning behavioral representation for vision-language-action model,” _arXiv preprint arXiv:2605.22671_ , 2026. 

- [101] Y. Zhu, R. Shao, Z. Liu _et al._ , “H-gar: A hierarchical interaction framework via goal-driven observation-action refinement for robotic manipulation,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 40, no. 22, 2026, pp. 18882–18890. 

- [102] Q. Lv, H. Li, X. Deng _et al._ , “Spatial-temporal graph diffusion policy with kinematic modeling for bimanual robotic manipulation,” in _2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . IEEE, 2025, pp. 17394–17404. 

- [103] Q. Lv, W. Kong, H. Li _et al._ , “F1: A vision-language-action model bridging understanding and generation to actions,” _arXiv preprint arXiv:2509.06951_ , 2025. 

- [104] X. Chen, J. Djolonga, P. Padlewski _et al._ , “Pali-x: on scaling up a multilingual vision and language model,” in _CVPR_ , 2024, pp. 14432–14444. 

- [105] E. J. Hu, Y. Shen, P. Wallis _et al._ , “Lora: low-rank adaptation of large language models,” in _ICLR_ , 2022. 

- [106] J. Wang, E. Shi, H. Hu _et al._ , “Large language models for robotics: opportunities, challenges, and perspectives,” _JAI_ , vol. 4, pp. 52– 64, 2025. 

- [107] J. Sun, P. Mao, L. Kong _et al._ , “A review of embodied grasping,” _Sensors_ , vol. 25, p. 852, 2025. 

- [108] X. Yao, H. Zhou, O. Mees _et al._ , “Bridging language and action: A survey of language-conditioned robot manipulation,” _arXiv:2312.10807_ , 2023. 

- [109] D. Li, Y. Jin, Y. Sun _et al._ , “What foundation models can bring for robot learning in manipulation: A survey,” _The International Journal of Robotics Research_ , p. 02783649251390579, 2024. 

- [110] A. O’Neill, A. Rehman, A. Maddukuri _et al._ , “Open x- embodiment: robotic learning datasets and rt-x models: open x- embodiment collaboration 0,” in _ICRA_ , 2024, pp. 6892–6903. 

- [111] J. Huang, S. Yong, X. Ma _et al._ , “An embodied generalist agent in 3d world,” in _ICML_ , 2024, pp. 20413–20451. 

- [112] W. Chen, S. Belkhale, S. Mirchandani _et al._ , “Training strategies for efficient embodied reasoning,” _arXiv:2505.08243_ , 2025. 

- [113] S. Dey, J.-N. Zaech, N. Nikolov _et al._ , “Revla: reverting visual domain limitation of robotic foundation models,” in _ICRA_ , 2025. 

- [114] R. Zheng, Y. Liang, S. Huang _et al._ , “Tracevla: visual trace prompting enhances spatial-temporal awareness for generalist robotic policies,” in _ICLR_ , 2025. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

19 

- [115] J. Jones, O. Mees, C. Sferrazza _et al._ , “Beyond sight: finetuning generalist robot policies with heterogeneous sensors via language grounding,” in _ICRA_ , 2025. 

- [116] J. Zheng, J. Li, D. Liu _et al._ , “Universal actions for enhanced embodied foundation models,” in _CVPR_ , 2025, pp. 22508–22519. 

- [117] D. Qu, H. Song, Q. Chen _et al._ , “Spatialvla: exploring spatial representations for visual-language-action model,” in _RSS_ , 2025. 

- [118] J. Zhang, Y. Guo, Y. Hu _et al._ , “Up-vla: a unified understanding and prediction model for embodied agent,” in _ICML_ , 2025. 

- [119] W. Zhao, P. Ding, Z. Min _et al._ , “Vlas: vision-language-action model with speech instructions for customized robot manipulation,” in _ICLR_ , 2025. 

- [120] C. Zhang, P. Hao, X. Cao _et al._ , “Vtla: vision-tactile-languageaction model with preference learning for insertion manipulation,” _arXiv:2505.09577_ , 2025. 

- [121] W. Zhao, G. Li, Z. Gong _et al._ , “Unveiling the potential of visionlanguage-action models with open-ended multimodal instructions,” _arXiv:2505.11214_ , 2025. 

- [122] T. Van Vo, T. Q. Nguyen, K. M. Nguyen _et al._ , “Refinevla: reasoning-aware teacher-guided transfer fine-tuning,” _arXiv:2505.19080_ , 2025. 

- [123] Y. Yang, J. Sun, S. Kou _et al._ , “Lohovla: a unified visionlanguage-action model for long-horizon embodied tasks,” _arXiv:2506.00411_ , 2025. 

- [124] Y. Wang, X. Li, W. Wang _et al._ , “Unified vision-language-action model,” _arXiv:2506.19850_ , 2025. 

- [125] J. Zhang, Y. Chen, Y. Xu _et al._ , “4d-vla: spatiotemporal vision-language-action pretraining with cross-scene calibration,” _arXiv:2506.22242_ , 2025. 

- [126] J. Lin, A. Taherin, A. Akbari _et al._ , “Vote: vision-language-action optimization with trajectory ensemble voting,” _arXiv:2507.05116_ , 2025. 

- [127] M. A. Patratskiy, A. K. Kovalev, and A. I. Panov, “Spatial traces: Enhancing vla models with spatial-temporal understanding,” _arXiv:2508.09032_ , 2025. 

- [128] X. Li, M. Liu, H. Zhang _et al._ , “Vision-language foundation models as effective robot imitators,” in _ICLR_ , 2024, pp. 1–19. 

- [129] J. Liu, M. Liu, Z. Wang _et al._ , “Robomamba: efficient visionlanguage-action model for robotic reasoning and manipulation,” in _NeurIPS_ , vol. 37, 2024, pp. 40085–40110. 

- [130] W. Song, J. Chen, P. Ding _et al._ , “Accelerating vision-languageaction model integrated with action chunking via parallel decoding,” _arXiv:2503.02310_ , 2025. 

- [131] R. Zhang, M. Dong, Y. Zhang _et al._ , “Mole-vla: dynamic layerskipping vision language action model via mixture-of-layers for efficient robot manipulation,” _arXiv:2503.20384_ , 2025. 

- [132] X. Tan, Y. Yang, P. Ye _et al._ , “Think twice, act once: token-aware compression and action reuse for efficient inference in visionlanguage-action models,” _arXiv:2505.21200_ , 2025. 

- [133] H. Wang, C. Xiong, R. Wang _et al._ , “Bitvla: 1-bit vision-languageaction models for robotics manipulation,” _arXiv:2506.07530_ , 2025. 

- [134] S. Wang, R. Yu, Z. Yuan _et al._ , “Spec-vla: speculative decoding for vision-language-action models with relaxed acceptance,” _arXiv:2507.22424_ , 2025. 

- [135] W. Li, R. Zhang, R. Shao _et al._ , “Cogvla: Cognition-aligned vision-language-action model via instruction-driven routing & sparsification,” _arXiv:2508.21046_ , 2025. 

- [136] A. Vaswani, N. Shazeer, N. Parmar _et al._ , “Attention is all you need,” in _NeurIPS_ , 2017. 

- [137] X. Zhai, B. Mustafa, A. Kolesnikov _et al._ , “Sigmoid loss for language image pre-training,” in _ICCV_ , 2023, pp. 11975–11986. 

- [138] M. Oquab, T. Darcet, T. Moutakanni _et al._ , “Dinov2: learning robust visual features without supervision,” _TMLR_ , 2024. 

- [139] C. R. Qi, L. Yi, H. Su _et al._ , “Pointnet++: deep hierarchical feature learning on point sets in a metric space,” in _NeurIPS_ , vol. 30, 2017. 

- [140] S. Chen, P.-L. Guhur, M. Tapaswi _et al._ , “Language conditioned spatial relation reasoning for 3d object grounding,” _NeurIPS_ , vol. 35, pp. 20522–20535, 2022. 

- [141] M. Zawalski, W. Chen, K. Pertsch _et al._ , “Robotic control via embodied chain-of-thought reasoning,” in _CoRL_ , 2025, pp. 3157– 3181. 

- [142] A. Gu and T. Dao, “Mamba: linear-time sequence modeling with selective state spaces,” _arXiv:2312.00752_ , 2023. 

- [143] J. Nielsen and P. Schneider-Kamp, “Bitnet b1. 58 reloaded: stateof-the-art performance also on smaller networks,” in _DeLTA_ , 2024, pp. 301–315. 

- [144] K. Pertsch, K. Stachowicz, B. Ichter _et al._ , “Fast: efficient action tokenization for vision-language-action models,” in _RSS_ , 2025. 

- [145] B. Han, J. Kim, and J. Jang, “A dual process vla: efficient robotic manipulation leveraging vlm,” _arXiv:2410.15549_ , 2024. 

- [146] Q. Bu, H. Li, L. Chen _et al._ , “Towards synergistic, generalized, and efficient dual-system for robotic manipulation,” _arXiv:2410.08001_ , 2024. 

- [147] Y. Shentu, P. Wu, A. Rajeswaran _et al._ , “From llms to actions: latent codes as bridges in hierarchical robot control,” in _IROS_ , 2024, pp. 8539–8546. 

- [148] Q. Li, Y. Liang, Z. Wang _et al._ , “Cogact: a foundational visionlanguage-action model for synergizing cognition and action in robotic manipulation,” _arXiv:2411.19650_ , 2024. 

- [149] J. Zhang, Y. Guo, X. Chen _et al._ , “Hirt: enhancing robotic control with hierarchical robot transformers,” in _CoRL_ , 2025, pp. 933–946. 

- [150] Z. Zhou, Y. Zhu, M. Zhu _et al._ , “Chatvla: unified multimodal understanding and robot control with vision-language-action model,” _arXiv:2502.14420_ , 2025. 

- [151] Z. Zhou, Y. Zhu, J. Wen _et al._ , “Chatvla-2: vision-language-action model with open-world embodied reasoning from pretrained knowledge,” _arXiv:2505.21906_ , 2025. 

- [152] J. Wen, Y. Zhu, M. Zhu _et al._ , “Diffusionvla: scaling robot foundation models via unified diffusion and autoregression,” in _ICML_ , 2025. 

- [153] Z. Liu, Y. Gu, S. Zheng _et al._ , “Trivla: a unified triple-system-based unified vision-language-action model for general robot control,” _arXiv:2507.01424_ , 2025. 

- [154] S. Li, L. Gao, J. Wang _et al._ , “Information-theoretic graph fusion with vision-language-action model for policy reasoning and dual robotic control,” _arXiv:2508.05342_ , 2025. 

- [155] W. Song, J. Chen, W. Li _et al._ , “Rationalvla: a rational visionlanguage-action model with dual system,” _arXiv:2506.10826_ , 2025. 

- [156] J. Jones, O. Mees, C. Sferrazza _et al._ , “Vq-vla: improving visionlanguage-action models via scaling vector-quantized action tokenizers,” in _ICCV_ , 2025. 

- [157] J. Wen, Y. Zhu, J. Li _et al._ , “Tinyvla: towards fast, data-efficient vision-language-action models for robotic manipulation,” _RA-L_ , 2025. 

- [158] J. Yu, H. Liu, Q. Yu _et al._ , “Forcevla: enhancing vla models with a force-aware moe for contact-rich manipulation,” _arXiv:2505.22159_ , 2025. 

- [159] F. Lin, R. Nai, Y. Hu _et al._ , “Onetwovla: a unified vision-languageaction model with adaptive reasoning,” _arXiv:2505.11917_ , 2025. 

- [160] J. Huang, S. Wang, F. Lin _et al._ , “Tactile-vla: unlocking visionlanguage-action model’s physical knowledge for tactile generalization,” _arXiv:2507.09160_ , 2025. 

- [161] C. Cheang, S. Chen, Z. Cui _et al._ , “Gr-3 technical report,” _arXiv:2507.15493_ , 2025. 

- [162] X. Chen, H. Wei, P. Zhang _et al._ , “Villa-x: enhancing latent action modeling in vision-language-action models,” _arXiv:2507.23682_ , 2025. 

- [163] S. Deng, M. Yan, S. Wei _et al._ , “Graspvla: a grasping foundation model pre-trained on billion-scale synthetic action data,” _arXiv:2505.03233_ , 2025. 

- [164] W. Peebles and S. Xie, “Scalable diffusion models with transformers,” in _ICCV_ , 2023, pp. 4195–4205. 

- [165] A. Mandlekar, D. Xu, J. Wong _et al._ , “What matters in learning from offline human demonstrations for robot manipulation,” in _CoRL_ , 2022, pp. 1678–1690. 

- [166] A. van den Oord, O. Vinyals, and k. kavukcuoglu, “Neural discrete representation learning,” in _NeurIPS_ , 2017, pp. 1–10. 

- [167] O. Ronneberger, P. Fischer, and T. Brox, “U-net: Convolutional networks for biomedical image segmentation,” in _MICCAI_ , 2015. 

- [168] A. M. Noam Shazeer, A. D. Krzysztof Maziarz, G. H. Quoc Le _et al._ , “Outrageously large neural networks: the sparsely-gated mixture-of-experts layer,” in _ICLR_ , 2017. 

- [169] Z. Wu, Y. Zhou, X. Xu _et al._ , “Momanipvla: transferring visionlanguage-action models for general mobile manipulation,” in _CVPR_ , 2025, pp. 1714–1723. 

- [170] W. Yuan, J. Duan, V. Blukis _et al._ , “Robopoint: a vision-language model for spatial affordance prediction in robotics,” in _CoRL_ , 2024. 

- [171] D. Wu, J. Fan, J. Zang _et al._ , “Reinforced reasoning for embodied planning,” _arXiv:2505.22050_ , 2025. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

20 

- [172] C. Wang, F. Xia, W. Yu _et al._ , “Chain-of-modality: learning manipulation programs from multimodal human videos with visionlanguage-models,” in _ICRA_ , 2025. 

- [173] Y. Li, Z. Gong, H. Li _et al._ , “Robotic visual instruction,” in _CVPR_ , 2025, pp. 12155–12165. 

- [174] S. Liu, J. Du, S. Xiang _et al._ , “Long-horizon embodied planning with implicit logical inference and hallucination mitigation,” _arXiv:2409.15658_ , 2025. 

- [175] Y. Hu, F. Lin, T. Zhang _et al._ , “Look before you leap: unveiling the power of gpt-4v in robotic vision-language planning,” _arXiv:2311.17842_ , 2023. 

- [176] Y. Ji, H. Tan, J. Shi _et al._ , “Robobrain: a unified brain model for robotic manipulation from abstract to concrete,” in _CVPR_ , 2025, pp. 1724–1734. 

- [177] L. X. Shi, B. Ichter, M. Equi _et al._ , “Hi robot: open-ended instruction following with hierarchical vision-language-action models,” in _ICML_ , 2025. 

- [178] Z. Yang, Y. Chen, X. Zhou _et al._ , “Agentic robot: a braininspired framework for vision-language-action models in embodied agents,” _arXiv:2505.23450_ , 2025. 

- [179] J. Wen, Y. Zhu, J. Li _et al._ , “Dexvla: vision-language model with plug-in diffusion expert for general robot control,” in _CoRL_ , 2025. 

- [180] S. Huang, Z. Jiang, H. Dong _et al._ , “Instruct2act: mapping multimodality instructions to robotic actions with large language model,” _arXiv:2305.11176_ , 2023. 

- [181] W. Mao, W. Zhong, Z. Jiang _et al._ , “Robomatrix: a skill-centric hierarchical framework for scalable robot task planning and execution in open-world,” _arXiv:2412.00171_ , 2024. 

- [182] C. Li, J. Wen, Y. Peng _et al._ , “Pointvla: injecting the 3d world into vision-language-action models,” _arXiv:2503.07511_ , 2025. 

- [183] Y. Yuan, H. Cui, Y. Chen _et al._ , “From seeing to doing: bridging reasoning and decision for robotic manipulation,” _arXiv:2505.08548_ , 2025. 

- [184] K. Zhang, R. Xu, P. Ren _et al._ , “Robridge: a hierarchical architecture bridging cognition and execution for general robotic manipulation,” in _ICCV_ , 2025. 

- [185] S. Han, B. Qiu, Y. Liao _et al._ , “Robocerebra: a large-scale benchmark for long-horizon robotic manipulation evaluation,” _arXiv:2506.06677_ , 2025. 

- [186] Y. Zhong, X. Huang, R. Li _et al._ , “Dexgraspvla: a visionlanguage-action framework towards general dexterous grasping,” _arXiv:2502.20900_ , 2025. 

- [187] W. Huang, C. Wang, R. Zhang _et al._ , “Voxposer: composable 3d value maps for robotic manipulation with language models,” in _CoRL_ , 2023. 

- [188] Z. Liang, Y. Mu, H. Ma _et al._ , “Skilldiffuser: interpretable hierarchical planning via skill abstractions in diffusion-based task execution,” in _CVPR_ , 2024, pp. 16467–16476. 

- [189] S. Nasiriany, S. Kirmani, T. Ding _et al._ , “RT-affordance: reasoning about robotic manipulation with affordances,” in _CoRL_ , 2024. 

- [190] H. Wu, H. Zhang, P. Zhang _et al._ , “Hibernac: hierarchical brainemulated robotic neural agent collective for disentangling complex manipulation,” _arXiv:2506.08296_ , 2025. 

- [191] D. Niu, Y. Sharma, G. Biamby _et al._ , “Llarva: vision-action instruction tuning enhances robot learning,” in _CoRL_ , 2024. 

- [192] H. Singh, R. J. Das, M. Han _et al._ , “Malmm: multi-agent large language models for zero-shot robotics manipulation,” in _CVPR_ , 2024. 

- [193] J. Bi, K. Y. Ma, C. Hao _et al._ , “Vla-touch: Enhancing vision-language-action models with dual-level tactile feedback,” _arXiv:2507.17294_ , 2025. 

- [194] D. Guo, D. Yang, H. Zhang _et al._ , “Deepseek-r1: incentivizing reasoning capability in llms via reinforcement learning,” _arXiv:2501.12948_ , 2025. 

- [195] B. Zhao, Z. Wang, J. Fang _et al._ , “Embodied-r: collaborative framework for activating embodied spatial reasoning in foundation models via reinforcement learning,” _arXiv:2504.12680_ , 2025. 

- [196] A. Kirillov, E. Mintun, N. Ravi _et al._ , “Segment anything,” in _ICCV_ , 2023, pp. 4015–4026. 

- [197] A. Hurst, A. Lerer, A. P. Goucher _et al._ , “Gpt-4o system card,” _arXiv:2410.21276_ , 2024. 

- [198] J. Gu, S. Kirmani, P. Wohlhart _et al._ , “Rt-trajectory: Robotic task generalization via hindsight trajectory sketches,” _arXiv:2311.01977_ , 2023. 

- [199] P. Sundaresan, Q. Vuong, J. Gu _et al._ , “Rt-sketch: Goalconditioned imitation learning from hand-drawn sketches,” in _CoRL_ , vol. 270. pmlr, 2025, pp. 70–96. 

- [200] Z. Zhang, K. Zheng, Z. Chen _et al._ , “Grape: generalizing robot policy via preference alignment,” _arXiv:2411.19309_ , 2024. 

- [201] J. Liu, F. Gao, B. Wei _et al._ , “What can rl bring to vla generalization? an empirical study,” _arXiv:2505.19789_ , 2025. 

- [202] L. Ouyang, J. Wu, X. Jiang _et al._ , “Training language models to follow instructions with human feedback,” in _NeurIPS_ , 2022, pp. 27730–27744. 

- [203] A. Jaech, A. Kalai, A. Lerer _et al._ , “Openai o1 system card,” _arXiv:2412.16720_ , 2024. 

- [204] G. Lu, W. Guo, C. Zhang _et al._ , “Vla-rl: towards masterful and general robotic manipulation with scalable reinforcement learning,” _arXiv:2505.18719_ , 2025. 

- [205] Z. Chen, R. Niu, H. Kong _et al._ , “Tgrpo: fine-tuning visionlanguage-action model via trajectory-wise group relative policy optimization,” _arXiv:2506.08440_ , 2025. 

- [206] J. Achiam, S. Adler, S. Agarwal _et al._ , “Gpt-4 technical report,” _arXiv:2303.08774_ , 2023. 

- [207] J. Luo, C. Xu, J. Wu _et al._ , “Precise and dexterous robotic manipulation via human-in-the-loop reinforcement learning,” _arXiv:2410.21845_ , 2024. 

- [208] Y. Chen, S. Tian, S. Liu _et al._ , “Conrft: a reinforced fine-tuning method for vla models via consistency policy,” _arXiv:2502.05450_ , 2025. 

- [209] C. Xu, Q. Li, J. Luo _et al._ , “Rldg: robotic generalist policy distillation via reinforcement learning,” in _RSS_ , 2025. 

- [210] Y. Guo, J. Zhang, X. Chen _et al._ , “Improving vision-languageaction model with online reinforcement learning,” in _ICRA_ , 2025. 

- [211] Y. Yang, Y. Wang, Z. Wen _et al._ , “Efficientvla: training-free acceleration and compression for vision-language-action models,” _arXiv:2506.10100_ , 2025. 

- [212] S. Xu, Y. Wang, C. Xia _et al._ , “Vla-cache: towards efficient visionlanguage-action model via adaptive token caching in robotic manipulation,” _arXiv:2502.02175_ , 2025. 

- [213] Y. Li, Y. Meng, Z. Sun _et al._ , “Sp-vla: a joint model scheduling and token pruning approach for vla model acceleration,” _arXiv:2506.12723_ , 2025. 

- [214] K. Ji, Y. Meng, H. Cui _et al._ , “Block-wise adaptive caching for accelerating diffusion policy,” _arXiv:2506.13456_ , 2025. 

- [215] Q. Bu, Y. Yang, J. Cai _et al._ , “Univla: learning to act anywhere with task-centric latent actions,” _arXiv:2505.06111_ , 2025. 

- [216] S. Ye, J. Jang, B. Jeon _et al._ , “Latent action pretraining from videos,” in _ICLR_ , 2025. 

- [217] H. He, C. Bai, L. Pan _et al._ , “Learning an actionable discrete diffusion policy via large-scale actionless video pre-training,” in _NeurIPS_ , 2024, pp. 31124–31153. 

- [218] H. Zhen, X. Qiu, P. Chen _et al._ , “3d-vla: a 3d vision-languageaction generative world model,” in _ICML_ , 2024, pp. 61229–61245. 

- [219] P. Ding, J. Ma, X. Tong _et al._ , “Humanoid-vla: towards universal humanoid control with visual integration,” _arXiv:2502.14795_ , 2025. 

- [220] S. Patel, S. Mohan, H. Mai _et al._ , “Robotic manipulation by imitating generated videos without physical demonstrations,” _arXiv:2507.00990_ , 2025. 

- [221] B. Wen, W. Yang, J. Kautz _et al._ , “Foundationpose: unified 6d pose estimation and tracking of novel objects,” in _CVPR_ , 2024, pp. 17868–17879. 

- [222] M. Assran, A. Bardes, D. Fan _et al._ , “V-jepa 2: self-supervised video models enable understanding, prediction and planning,” _arXiv:2506.09985_ , 2025. 

- [223] I. Kostrikov, A. Nair, and S. Levine, “Offline reinforcement learning with implicit q-learning,” in _ICLR_ , 2022. 

- [224] T. Haarnoja, A. Zhou, P. Abbeel _et al._ , “Soft actor-critic: off-policy maximum entropy deep reinforcement learning with a stochastic actor,” in _ICML_ , 2018, pp. 1861–1870. 

- [225] S. Tan, K. Dou, Y. Zhao _et al._ , “Interactive post-training for visionlanguage-action models,” _arXiv:2505.17016_ , 2025. 

- [226] Z. Wang, S. Cai, Z. Mu _et al._ , “Omnijarvis: unified visionlanguage-action tokenization enables open-world instruction following agents,” in _NeurIPS_ , 2024. 

- [227] B. Liu, Y. Zhu, C. Gao _et al._ , “Libero: benchmarking knowledge transfer for lifelong robot learning,” in _NeurIPS_ , vol. 36, 2023, pp. 44776–44791. 

- [228] S. Fei, S. Wang, J. Shi _et al._ , “Libero-plus: In-depth robustness analysis of vision-language-action models,” _arXiv:2510.13626_ , 2025. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

21 

- [229] O. Mees, L. Hermann, E. Rosete-Beas _et al._ , “Calvin: a benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks,” _RA-L_ , vol. 7, pp. 7327–7334, 2022. 

- [230] H. Ha, H. Ha, P. Florence _et al._ , “Scaling up and distilling down: Language-guided robot skill acquisition,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 3766–3777. 

- [231] C. Wen, X. Lin, J. So _et al._ , “Any-point trajectory modeling for policy learning,” _arXiv:2401.00025_ , 2023. 

- [232] T. Z. Zhao, V. Kumar, S. Levine _et al._ , “Learning finegrained bimanual manipulation with low-cost hardware,” _arXiv:2304.13705_ , 2023. 

- [233] C. Chi, Z. Xu, S. Feng _et al._ , “Diffusion policy: visuomotor policy learning via action diffusion,” _IJRR_ , 2023. 

- [234] S. Lee, Y. Wang, H. Etukuru _et al._ , “Behavior generation with latent actions,” in _ICML_ , 2024, pp. 26991–27008. 

- [235] O. M. Team, D. Ghosh, H. Walke _et al._ , “Octo: an open-source generalist robot policy,” _arXiv:2405.12213_ , 2024. 

- [236] K. Black, N. Brown, J. Darpinian _et al._ , “ _π_ 0. 5: a vision-languageaction model with open-world generalization,” _arXiv:2504.16054_ , 2025. 

- [237] E. Jang, A. Irpan, M. Khansari _et al._ , “Bc-z: zero-shot task generalization with robotic imitation learning,” in _CoRL_ , 2022, pp. 991–1002. 

- [238] F. Ebert, Y. Yang, K. Schmeckpeper _et al._ , “Bridge data: boosting generalization of robotic skills with cross-domain datasets,” in _RSS_ , 2022, pp. 1–7. 

- [239] H.-S. Fang, H. Fang, Z. Tang _et al._ , “Rh20t: a comprehensive robotic dataset for learning diverse skills in one-shot,” in _ICRA_ , 2024, pp. 653–660. 

- [240] A. Khazatsky, K. Pertsch, S. Nair _et al._ , “Droid: a large-scale inthe-wild robot manipulation dataset,” in _RSS_ , 2024, pp. 1–26. 

- [241] C. Li, R. Zhang, J. Wong _et al._ , “Behavior-1k: a human-centered, embodied ai benchmark with 1,000 everyday activities and realistic simulation,” in _CoRL_ , 2022. 

- [242] M. Shridhar, J. Thomason, D. Gordon _et al._ , “Alfred: a benchmark for interpreting grounded instructions for everyday tasks,” in _CVPR_ , 2020, pp. 10740–10749. 

- [243] S. James, Z. Ma, D. R. Arrojo _et al._ , “Rlbench: the robot learning benchmark & learning environment,” _RA-L_ , vol. 5, pp. 3019–3026, 2020. 

- [244] M. Grotz, M. Shridhar, T. Asfour _et al._ , “Peract2: benchmarking and learning for robotic bimanual manipulation tasks,” _arXiv:2407.00278_ , 2024. 

- [245] T. Yu, D. Quillen, Z. He _et al._ , “Meta-world: a benchmark and evaluation for multi-task and meta reinforcement learning,” in _CoRL_ , 2020, pp. 1094–1100. 

- [246] A. Gupta, V. Kumar, C. Lynch _et al._ , “Relay policy learning: solving long-horizon tasks via imitation and reinforcement learning,” in _CoRL_ , 2019. 

- [247] E. Cherepanov, N. Kachaev, A. K. Kovalev _et al._ , “Memory, benchmark & robots: a benchmark for solving complex tasks with reinforcement learning,” _arXiv:2502.10550_ , 2025. 

- [248] X. Li, K. Hsu, J. Gu _et al._ , “Evaluating real-world robot manipulation policies in simulation,” in _CoRL_ , 2024. 

- [249] M. Savva, A. Kadian, O. Maksymets _et al._ , “Habitat: a platform for embodied ai research,” in _ICCV_ , 2019, pp. 9339–9347. 

- [250] A. Szot, A. Clegg, E. Undersander _et al._ , “Habitat 2.0: training home assistants to rearrange their habitat,” in _NeurIPS_ , vol. 34, 2021, pp. 251–266. 

- [251] X. Puig, E. Undersander, A. Szot _et al._ , “Habitat 3.0: a co-habitat for humans, avatars and robots,” _ICLR_ , 2024. 

- [252] F. Xiang, Y. Qin, K. Mo _et al._ , “Sapien: a simulated part-based interactive environment,” in _CVPR_ , 2020, pp. 11097–11107. 

- [253] W. Pumacay, I. Singh, J. Duan _et al._ , “The colosseum: a benchmark for evaluating generalization for robotic manipulation,” in _RSS_ , 2024. 

- [254] S. Zhang, Z. Xu, P. Liu _et al._ , “Vlabench: a large-scale benchmark for language-conditioned robotics manipulation with longhorizon reasoning tasks,” in _ICCV_ , 2025. 

- [255] K. Grauman, A. Westbury, E. Byrne _et al._ , “Ego4d: around the world in 3,000 hours of egocentric video,” in _CVPR_ , 2022. 

- [256] K. Grauman, A. Westbury, L. Torresani _et al._ , “Ego-exo4d: understanding skilled human activity from first-and third-person perspectives,” in _CVPR_ , 2024, pp. 19383–19400. 

- [257] Y. Chen, Y. Ge, Y. Ge _et al._ , “Egoplan-bench: benchmarking egocentric embodied planning with multimodal large language models,” _arxiv:2312.06722_ , 2024. 

- [258] X. Wang, K. Zhao, F. Liu _et al._ , “Egovid-5m: a large-scale videoaction dataset for egocentric video generation,” _arXiv:2411.08380_ , 2024. 

- [259] D. Damen, H. Doughty, G. M. Farinella _et al._ , “Scaling egocentric vision: the epic-kitchens dataset,” in _ECCV_ , 2018. 

- [260] K. Maeda, T. Hirasawa, A. Hashimoto _et al._ , “Com kitchens: an unedited overhead-view video dataset as a vision-language benchmark,” in _ECCV_ , 2024, pp. 123–140. 

- [261] C. Fan, “Egovqa-an egocentric video question answering benchmark dataset,” in _ICCV_ , 2019. 

- [262] B. Jia, T. Lei, S.-C. Zhu _et al._ , “Egotaskqa: understanding human tasks in egocentric videos,” in _NeurIPS_ , vol. 35, 2022, pp. 3343– 3360. 

- [263] R. Hoque, P. Huang, D. J. Yoon _et al._ , “Egodex: learning dexterous manipulation from large-scale egocentric video,” _arXiv:2505.11709_ , 2025. 

- [264] C. Wang, H. Shi, W. Wang _et al._ , “Dexcap: scalable and portable mocap data collection system for dexterous manipulation,” in _RSS_ , 2024. 

- [265] S. Kareer, D. Patel, R. Punamiya _et al._ , “Egomimic: scaling imitation learning via egocentric video,” _arXiv:2410.24221_ , 2024. 

- [266] R.-Z. Qiu, S. Yang, X. Cheng _et al._ , “Humanoid policy˜ human policy,” _arXiv:2503.13441_ , 2025. 

- [267] J. Yu, L. Fu, H. Huang _et al._ , “Real2render2real: scaling robot data without dynamics simulation or robot hardware,” _arXiv:2505.09601_ , 2025. 

- [268] A. Das, S. Datta, G. Gkioxari _et al._ , “Embodied question answering,” in _CVPR_ , 2018, pp. 1–10. 

- [269] D. Gordon, A. Kembhavi, M. Rastegari _et al._ , “Iqa: visual question answering in interactive environments,” in _CVPR_ , 2018, pp. 4089– 4098. 

- [270] L. Yu, X. Chen, G. Gkioxari _et al._ , “Multi-target embodied question answering,” in _CVPR_ , 2019, pp. 6309–6318. 

- [271] E. Wijmans, S. Datta, O. Maksymets _et al._ , “Embodied question answering in photorealistic environments with point cloud perception,” in _CVPR_ , 2019, pp. 6659–6668. 

- [272] M. M. Islam, A. Gladstone, R. Islam _et al._ , “Eqa-mx: embodied question answering using multimodal expression,” in _ICLR_ , 2023. 

- [273] A. Majumdar, A. Ajay, X. Zhang _et al._ , “Openeqa: embodied question answering in the era of foundation models,” in _CVPR_ , 2024, pp. 16488–16498. 

- [274] J.-W. Choi, Y. Yoon, H. Ong _et al._ , “Lota-bench: benchmarking language-oriented task planners for embodied agents,” in _ICLR_ , 2024. 

## **APPENDIX A** 

## **EXPERIMENTAL EVALUATION** 

In this section, we present a rigorous comparative analysis of state of the art large VLM based vision language action (VLA) models. To comprehensively assess these architectures, we synthesize quantitative results from three primary simulation benchmarks alongside diverse real world deployments. Specifically, we utilize LIBERO [227] to evaluate lifelong learning and long horizon capabilities. We then employ LIBERO-Plus [228] and CALVIN [229] to deeply explore model generalization under severe visual and kinematic distribution shifts. Beyond simulations, we systematically investigate model performance on real world custom tasks to examine practical capabilities across varied robotic hardware. Finally, drawing on these empirical findings, we discuss the inherent tradeoffs between monolithic and hierarchical paradigms in physical applications. 

### **A.1 Benchmark Performance Analysis** 

To ensure a standardized comparison, we employ Success Rate (SR) as our primary Evaluation Metric. SR is defined as the percentage of episodes in which the robot successfully completes the target task within a predefined maximum step limit following a natural language instruction. For 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

22 

multi-task evaluations, we calculate the average SR across all tasks within a given suite to quantify the model’s overall robustness and generalization proficiency. 

### _A.1.1 Evaluation on Diverse Tasks_ 

TABLE 6: Comprehensive LIBERO Benchmark Results. 

|**Method**<br>**Early Languag**|**Spatial**<br>**e-Condi**|**Object**<br>**tioned R**|**Goal**<br>**obotic **|**Long**<br>**System**|**Overall**|
|---|---|---|---|---|---|
|Distill-D [230]|46.8|72.0|63.8|47.3|57.5|
|Transformer-BC [227]|71.8|71.0|76.3|24.2|60.8|
|ResNet-T [227]|75.7|78.9|52.7|45.0|63.1|
|ATM [231]|68.5|68.0|77.8|39.3|63.4|
|ACT [232]|82.0|78.8|66.1|44.0|67.7|
|Diffusion Policy [233]<br>|78.3|92.5|68.3|50.5|72.4|
|VQ-BeT [234]|88.7|90.3|61.3|59.7|75.0|
|**Monolithic VL**|**A model**|**s: Single**|**-system**|**Mode**|**l**|
|FlashVLA [132]|84.2|86.4|75.4|51.4|74.4|
|TraceVLA [114]|84.6|85.2|75.1|54.1|74.8|
|Octo [235]|78.9|85.7|84.6|51.1|75.1|
|Spec-VLA [134]|85.8|85.0|74.7|55.0|75.1|
|<br>OpenVLA [29]|84.7|88.4|79.2|53.7|76.5|
|<br>UniAct [116]|77.0|87.0|77.0|70.0|77.8|
|SpatialVLA [117]|88.2|89.9|78.6|55.5|78.1|
|<br>WorldVLA [41]|87.6|96.2|83.4|60.0|81.8|
|CoT-VLA [36]|87.5|91.6|87.6|69.0|83.9|
|NORA [48]|92.2|95.4|89.4|74.6|87.9|
|4D-VLA [125]|88.9|95.2|90.9|79.1|88.6|
|PD-VLA [130]|95.5|96.7|94.9|91.7|94.7|
|VOTE [126]|96.0|98.5|94.0|91.0|94.9|
|UnifiedVLA [124]|95.4|98.8|93.6|94.0|95.5|
|i<br>BitVLA [133]|96.6|99.0|95.4|92.8|96.0|
|OpenVLA-OFT [47]|97.6|98.4|97.9|94.5|97.1|
|<br>**Monolithic V**|**LA mode**|**ls: Dual-**|**system**|**Model**||
|GraspVLA [163]|-|94.1|91.2|82.0|-|
|_π_0 + FAST [144]<br>|96.4|96.8|88.6|60.2|85.5|
|TriVLA [153]|91.2|93.8|89.8|73.2|87.0|
|SmolVLA [34]|93.0|94.0|91.0|77.0|88.8|
|_π_0 [32]<br>|96.8|98.8|95.8|85.2|94.2|
|villa-X [162]|97.5|97.0|91.5|74.5|90.1|
|<br>**Hier**|**archical **|**VLA mo**|**dels**|||
|DexVLA [179]|97.2|99.1|95.6|-|-|
|Agentic Robot [178]|85.8|89.0|81.8|61.6|79.6|
|<br>**Ot**|**her Adv**|**anced Fie**|**ld**|||
|LAPA [216]|73.8|74.6|58.8|55.4|65.7|
|<br>VLA-Cache [212]|83.8|85.8|76.4|52.8|74.7|
|<br>VLA-RL [204]|90.2|91.8|82.2|59.8|81.0|
|WorldVLA [41]|87.6|96.2|83.4|60.0|81.8|
|UniVLA [215]|96.5|96.8|95.6|92.0|95.2|


**The Capability Leap of Monolithic Scaling.** Table 6 presents the evaluation of various paradigms on the LIBERO benchmark [227], spanning Spatial, Object, Goal, and Long-horizon tasks. A prominent phenomenon is the massive capability leap from Early Language-Conditioned Systems to Monolithic VLA models. Early models, relying on smaller backbones or decoupled feature extractors (e.g., ACT [232], Diffusion Policy [233]), plateau around a 65% to 75% overall success rate. In stark contrast, Monolithic Single-system models powered by large VLMs demonstrate exceptional scalability, with state-of-the-art models like OpenVLA-OFT [47], UniVLA [215], and UnifiedVLA [124] achieving overall success rates exceeding 95%. This clearly indicates that leveraging massive pretrained VLMs as unified backbones fundamentally shatters the performance ceil- 

ing of early decoupled systems, establishing monolithic scaling as the primary driver for broad tasks. 

**Overcoming Long Horizon Bottlenecks.** Crucially, the “Long” task category highlights a significant bottleneck for earlier architectures. While models like TransformerBC [227] and ACT [232] achieve high performance on spatial and object tasks, their performance drops to roughly 20% to 35% on long-horizon reasoning. This exposes a fundamental limitation in naive autoregressive decoding over long temporal windows, where context saturation and error accumulation rapidly degrade performance. Conversely, recent single-system advancements (e.g., PD-VLA [130], VOTE [126]) and dual-system models (e.g., _π_ 0 [32]) explicitly address this through parallel decoding mechanisms, flow-matching, or continuous latent feature propagation, effectively pushing long-horizon success rates above 90%. This provides a deep insight: while simply scaling VLM parameters effectively solves basic spatial semantic grounding, sustained long horizon execution strictly requires architectural innovations that capture temporal dynamics and tightly integrate high level cognitive reasoning with robust continuous control. 

### _A.1.2 Evaluation on Generalization Performance_ 

### **Visual Kinematic Overfitting and Perceptual Brittleness.** 

The LIBERO-Plus [228] results in Table 7 detail performance under a comprehensive suite of perturbations. A detailed analysis of these results exposes a multifaceted overfitting phenomenon. For instance, OpenVLA [29] suffers a catastrophic overall performance drop to 16.1%. The near total collapse under camera viewpoint shifts (1.1%) and robot initial state perturbations (4.1%) confirms a severe visual kinematic entanglement. These models heavily memorize specific 2D pixel to joint mappings rather than acquiring an embodiment agnostic understanding of physical mechanics or invariant spatial geometry. Even the state of the art OpenVLA-OFT [47] experiences a massive performance drop when facing unseen camera angles. Furthermore, substantial degradation under varying light conditions, background textures, and sensor noise indicates a critical overreliance on pristine high frequency visual features. Instead of learning robust geometric object affordances, current architectures overfit to the specific rendering pipelines and photometric properties of their training environments. 

**Cognitive Limitations and Semantic Fragility.** Beyond perceptual brittleness, the performance drops associated with language instruction rewriting and object layout alterations reveal profound cognitive limitations. When task instructions are infused with conversational distractors, commonsense synonyms, or complex reasoning chains, models exhibit significant capability regression. This demonstrates that the integrated VLMs often function as shallow linguistic pattern matchers rather than exhibiting true deep semantic reasoning or robust multimodal information filtering. Additionally, the introduction of confounding distractor objects or shifted target poses severely disrupts visual attention, proving that current architectures struggle to maintain stable object permanence and relational focus in cluttered scenes. Dual system models like _π_ 0 [32] and _π_ 0 + FAST [43] exhibit similar vulnerabilities across these dimensions, proving that merely decoupling the action expert does not in- 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

23 

TABLE 7: Comprehensive LIBERO-Plus Benchmark Results under Various Perturbations. _↓_ denotes the relative decrease from the original success rate. 

|**Method**|**Original**|**Camera**|**Robot**|**Language**|**Light**|**Background**|**Noise**|**Layout**|**Overall**|
|---|---|---|---|---|---|---|---|---|---|
|OpenVLA [29]|76.5|1.1 (75.4_↓_)|4.1 (72.4_↓_)|26.8 (49.7_↓_)|4.4 (72.1_↓_)|25.3 (51.2_↓_)|19.3 (57.2_↓_)|31.6 (44.9_↓_)|16.1 (60.4_↓_)|
|<br>OpenVLA-OFT [47]|97.1|59.7 (37.4_↓_)|37.2 (59.9_↓_)|81.5 (15.6_↓_)|85.8 (11.3_↓_)|92.4 (4.7_↓_)|76.7 (20.4_↓_)|77.1 (20.0_↓_)|72.9 (24.2_↓_)|
|<br>_π_0 [32]|94.2|15.8 (78.4_↓_)|6.6 (87.6_↓_)|61.0 (33.2_↓_)|79.6 (14.6_↓_)|78.5 (15.7_↓_)|79.4 (14.8_↓_)|70.4 (23.8_↓_)|55.9 (38.3_↓_)|
|_π_0 + FAST [144]|85.5|66.4 (19.1_↓_)|24.8 (60.7_↓_)|63.3 (22.2_↓_)|73.0 (12.5_↓_)|67.7 (17.8_↓_)|75.8 (9.7_↓_)|70.3 (15.2_↓_)|63.0 (22.5_↓_)|
|NORA [48]|87.9|4.0 (83.9_↓_)|41.1 (46.8_↓_)|67.0 (20.9_↓_)|31.0 (56.9_↓_)|50.5 (37.4_↓_)|17.6 (70.3_↓_)|63.9 (24.0_↓_)|39.3 (48.6_↓_)|
|WorldVLA [41]|79.1|0.3 (78.8_↓_)|30.2 (48.9_↓_)|44.2 (34.9_↓_)|29.4 (49.7_↓_)|14.5 (64.6_↓_)|12.2 (66.9_↓_)|39.4 (39.7_↓_)|24.3 (54.8_↓_)|
|UniVLA [215]|95.2|4.3 (90.9_↓_)|50.3 (44.9_↓_)|71.8 (23.4_↓_)|59.1 (36.1_↓_)|80.0 (15.2_↓_)|25.3 (69.9_↓_)|34.3 (60.9_↓_)|46.4 (48.8_↓_)|


herently resolve these foundational geometric and semantic flaws. 

**Cross Domain Resilience and Robust Action Generation.** As shown in Table 8, the ABC _→_ D split represents the most difficult evaluation setting within CALVIN benchmark [229], forcing methods to generalize to unseen scene (Environment D) after training exclusively on three distinct environments (A, B, and C). In this rigorous cross domain and long horizon setting, the sequential nature of the 1/5 to 5/5 tasks severely tests a model’s resistance to compounding covariate shift. Early architectures like RT-1 [20] suffer immediate collapse, dropping from a 53.3% success rate at the first step to a mere 1.3% at the fifth step. However, advanced monolithic and dual system architectures, such as TriVLA [153], UnifiedVLA [124], and _π_ 0 [32], demonstrate remarkable resilience by maintaining high success rates even at the final 5/5 stage. We attribute this success to the integration of robust action generation paradigms, specifically diffusion and flow matching mechanisms, which provide dynamic action correction capabilities. This strongly implies that tightly coupling the deep semantic planning of a VLM with an expressive and noise resistant low level action expert is currently the most viable path toward achieving generalized long horizon robotic autonomy in unseen environments. 

TABLE 8: Comprehensive CALVIN Benchmark Results under ABC _→_ D Setting. 

|**Method**|**1/5**|**2/5**|**3/5**|**4/5**|**5/5**|**Avg. Len.**|
|---|---|---|---|---|---|---|
|RT-1 [20]|53.3|22.2|9.4|3.8|1.3|0.90|
|LCB [147]|73.6|50.2|28.5|16.0|9.9|1.78|
|RationalVLA [155]|74.3|58.3|42.3|30.0|20.7|2.26|
|VLAS [119]|87.2|64.2|40.9|28.1|19.6|2.40|
|RoboFlamingo [128]|82.4|61.9|46.6|33.1|23.5|2.47|
|DeeR-VLA [39]|84.8|72.3|54.9|44.6|33.5|2.90|
|OE-VLA [121]|91.8|73.8|56.2|44.2|33.4|2.99|
|OpenVLA [29]|91.3|77.8|62.0|52.1|43.5|3.27|
|RoboDual [146]|94.4|82.7|72.1|62.4|54.4|3.66|
|UniVLA [215]|95.5|85.8|75.4|66.9|56.5|3.80|
|_π_0 [32]|93.8|85.0|76.7|68.1|59.9|3.92|
|UP-VLA [118]|92.8|86.5|81.5|76.9|69.9|4.08|
|TriVLA [153]|96.8|92.4|86.8|83.2|81.8|4.37|
|UnifiedVLA [124]|98.9|94.8|89.0|82.8|75.1|4.41|


### _A.1.3 Evaluation on Real-World Custom Tasks_ 

Evaluating VLA models in the real world presents a unique set of challenges. As summarized in Table 9, real-world experimental setups are highly customized, varying significantly in robotic hardware (e.g., Franka, WidowX, Unitree), baseline comparisons, and task complexity. Consequently, 

directly comparing absolute Success Rates (SR) across different methods is often infeasible. Instead, a more rigorous analytical approach involves examining the relative performance gains over established baselines (such as OpenVLA [29], RT-1 [20], or Diffusion Policy [233]) and identifying the specific task characteristics that highlight the structural advantages of either monolithic or hierarchical paradigms. 

**Capabilities and Strengths of Monolithic Architectures.** Monolithic models, encompassing both singlesystem and tightly coupled dual-system designs, consistently demonstrate strong performance in dynamic, contactrich, and multi-modal environments. By mapping observations directly to actions within a unified latent space, these models excel at tasks requiring high-frequency reactive control and seamless sensory integration. For instance, as shown in Table 9, VILA [120] achieves a remarkable 97.5% SR in contact-rich peg-in-hole assemblies, highlighting the efficacy of an end-to-end architecture in preserving subtle physical and tactile nuances that might be lost during intermediate feature extraction. Furthermore, monolithic models exhibit robust local generalization against visual distractors and out-of-distribution objects. Models like OpenVLA [29] and TraceVLA [114] show significant SR improvements (16.8% and 57.5%, respectively) over standard baselines when confronted with unseen backgrounds and randomized initial positions. Moreover, unified architectures naturally facilitate multi-modal fusion; methods like FuSe [115] successfully integrate visual, auditory, and tactile reasoning, yielding a 22.7% performance boost in custom multimodal tasks. 

**Capabilities and Strengths of Hierarchical Architectures.** Conversely, hierarchical architectures demonstrate profound advantages in extreme zero-shot generalization, long-horizon multi-stage planning, and cross-embodiment transfer. By explicitly decoupling high-level semantic reasoning from low-level continuous control, these models can leverage the immense cognitive capabilities of foundational VLMs without being bottlenecked by the strict real-time constraints of actuator control. Table 9 reveals that hierarchical frameworks often achieve massive relative improvements in structurally complex scenarios. For example, RoboMatrix [181] demonstrates up to a 100% relative improvement in zero-shot skill recombination, while DexGrasp [186] yields a 61.4% gain in dexterous generalization across extreme domain shifts. Because the intermediate representations (such as 3D keypoints, affordance maps, or visual traces) are highly structured, hierarchical models like PointVLA [182] and _A_ 0 [52] excel in 3D-aware spatial reasoning and affordance-guided manipulation. This 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

24 

TABLE 9: Analysis of Real-world Experiments. _↑_ denotes the improvement in success rate compared to the baseline method under the same task settings. 

|**Model**|**Robot**|**Baseline**|**SR**(%)|**Real-World Task Characteristics**|
|---|---|---|---|---|
|||||**MONOLITHIC**|
|RT-2 [30]|-|RT-1|71_._3(24_._3 _↑_)|Custom zero-shot tasks assessing generalization and emergent capabilities.|
|RT-2-X [110]|WidowX|RT-1|40(5 _↑_)|Using diverse test environments and robot arms to assess cross-entity transfer.|
|OpenVLA [29]<br>|Panda<br>|DP<br>|61_._1(16_._8 _↑_)<br>|Custom tasks with out-of-distribution target objects and distractors.<br>|
|ECoT [112]|WidowX|OpenVLA|65(28 _↑_)|Custom spatial-relation and out-of-distribution tasks assessing generalization.|
|TraceVLA [114]|WidowX|OpenVLA|75(57_._5 _↑_)|Custom tasks with randomized initial positions, unseen tasks, and distractor objects.|
|FuSe [115]|WidowX|Octo|68_._7(22_._7 _↑_)|Custom tasks assessing joint visual, auditory, and tactile reasoning.|
|UniAct [116]|UnitreeG1|LangWBC|83_._1(24_._9 _↑_)|Custom tasks assessing heterogeneous instruction understanding.|
|SpatialVLA [117]|WidowX|OpenVLA|74_._0(9 _↑_)|Custom unseen-background and pose tasks assessing semantic and motor robustness.|
|UP-VLA [118]|Panda|DP|65(51_._7 _↑_)|Custom unseen and precision tasks assessing generalization and perception.|
|HybridVLA [37]|FR3|CogACT|83(22 _↑_)|Custom tasks assessing spatial understanding and long-horizon capabilities.|
|CoT-VLA [36]|Panda|OpenVLA|78_._8(11_._5 _↑_)|Custom long-horizon tasks assessing out-of-distribution generalization.|
|VTLA [120]<br>|UR3<br>|Qwen2-VL<br>|97_._5(2_._5 _↑_)<br>|Custom peg-in-hole assembly tasks assessing contact-rich manipulation.<br>|
|BridgeVLA [38]|FR3|RVT-2|96_._9(6_._9 _↑_)|Custom basic and generalization evaluation settings.|
|4D-VLA [125]|Franka|OpenVLA|85_._6(57_._9 _↑_)|Custom out-of-distribution and novel-view generalization tasks.|
|ST-VLA [127]<br>OFT [47]<br>PD-VLA [130]|Panda<br>ViperX<br>UnitreeZ1|OpenVLA<br>RDT-1B<br>LLaVA-VLA|72_._5(32_._5 _↑_)<br>87_._8(9_._4 _↑_)<br>70(33_._3 _↑_)|Custom tasks assessing generalization, robustness, and long-horizon capabilities.<br>Custom unseen dexterous bimanual manipulation tasks.<br>Custom distractor-augmented tasks assessing action coherence.|
|<br>MoLe-VLA [131]|FR3|CogAct|70(3_._3 _↑_)|<br>Custom tasks assessing precise 3D spatial understanding and continuous control.|
|NORA [48]|WidowX|OpenVLA|56_._7(16_._7 _↑_)|Custom tasks assessing out-of-distribution generalization and multi-target grasping.|
|BitVLA [133]<br>|Franka|_π_0|65(12_._5 _↑_)<br>|Custom basic and OOD tasks with unseen objects and background substitutions.<br>|
|Tactile-VLA [160]<br>GR-3 [161]|-<br>ByteMini|_π_0<br>_π_0|90(50 _↑_)<br>57_._8(17_._8 _↑_)|Custom contact-rich manipulation tasks assessing language-driven force reasoning.<br>Custom tabletop tasks assessing generalization across unseen scenarios.|
|TinyVLA [157]|Franka|OpenVLA|94_._0(25_._7 _↑_)|Custom single-arm and bimanual tasks with diverse action spaces.|
|RoboDual [146]|ALOHA|OpenVLA|82_._7(26_._7 _↑_)|Custom tasks comparing specialist, generalist and hybrid VLA approaches.|
|GR00T N1 [35]|GR-1|DP|76_._8(30_._4 _↑_)|Custom tasks assessing data efficiency across varying scales of human teleoperation data.|
|<br>CogACT [148]<br>HiRT [149]|Realman<br>Franka|OpenVLA<br>Vanilla-VLA|71_._2(51_._9 _↑_)<br>75_._0(27_._0 _↑_)|i<br>Custom tasks with object-color compositional reasoning.<br>Custom tasks assessing semantic grounding with unseen objects, distractors and target motion.|
|Fast-in-Slow [43]|Agilex|_π_0|74(13 _↑_)|Custom multi-condition tasks assessing generalization, robustness and distraction resilience.|
|ChatVLA [150]|Franka|OpenVLA|51_._4(32_._7 _↑_)<br>|Custom long-horizon and multi-task tasks assessing compositional skills.|
|ChatVLA-2 [151]|ARX|_π_0|81_._4(65_._4 _↑_)|Custom mathematical and spatial reasoning tasks.|
|DiVLA [152]|Agilex|OpenVLA|71_._0(44_._3 _↑_)|Custom multi-task and sorting tasks assessing generalization and robustness to visual changes.|
|RationalVLA [155]|AgileX|3DDA|85_._0(68_._3 _↑_)|Custom tasks with unseen instructions assessing language generalization.|
|ForceVLA [158]<br>|Franka<br>|_π_0|60_._5(20_._3 _↑_)<br>|Custom contact-rich tasks assessing force control and multimodal manipulation.<br>|
|SmolVLA [34]|Franka|_π_0|78_._3(16_._6 _↑_)|Custom tasks assessing generalization and OOD robustness.|
|OneTwoVLA [159]|Franka|_π_0|87(30 _↑_)|Custom long-horizon tasks assessing planning and generalization.|
|||||**HIERARCHICAL**|
|Hamster [51]|Panda|OpenVLA|69(32 _↑_)|Custom tabletop tasks assessing cross-domain visual and semantic generalization.|
|DexVLA [179]|DJI’RM|_π_0|55(13_._5 _↑_)|Custom long-horizon tasks assessing implicit reasoning and cross-embodiment dexterity.|
|RoboMatrix [181]|DJI’RM|OpenVLA|100(100 _↑_)|Custom long-horizon tasks assessing zero-shot skill recombination and generalization.|
|PointVLA [182]|AgileX|DexVLA|57(53 _↑_)|Custom 3D-aware tasks assessing spatial reasoning, height adaptability, and anti-hallucination.|
|_A_0 [52]<br>|Gen3<br>|ReKep<br>|53_._75(20 _↑_)<br>|Custom zero-shot tasks assessing affordance points and continuous visual traces.<br>|
|FSD [183]|xArm6|RoboPoint|72(30 _↑_)|Custom zero-shot tasks evaluating affordance- and visual trace-guided manipulation.|
|Robridge [184]|Gen3|ReKep|83_._3(34_._1 _↑_)|<br>Custom multi-stage tasks assessing zero-shot generalization and cognition-execution bridging.|
|<br>DG186|RMGO||917614|<br>Ct ht tk lti dt liti  t di hift|
|exrasp []<br>RT-H [31]<br>|+<br>EDR<br>|_π_0<br>RT-2<br>|_._(_. ↑_)<br>40(15 _↑_)<br>|usom zero-so ass evauang exerous generazaon across exreme oman ss.<br>High-Precision tasks assessing contextual sequential execution and language interventions.<br>|
|ReKep [53]|Franka|VoxPoser|61(51 _↑_)|Custom tasks assessing zero-shot spatio-temporal reasoning and reactive coordination.|
|<br>VoxPoser [187]|Panda|LLM+Prim|88(64 _↑_)|<br>Custom tabletop tasks assessing zero-shot spatial composition and dynamic robustness.|
|RT-Affo [189]|EDR|RT-2|68(40 _↑_)|<br>Custom manipulation tasks testing fine-grained part-level and precise spatial reasoning.|
|HiBerNAC [190]|Franka|Octo/RDT|60(39_/_5_._6 _↑_)|Custom dynamic tasks for neuro-inspired long-horizon adaptation and error-correction.|
|LLARVA [191]|Panda|RPT/Octo|83(13_/_37 _↑_)<br>|Randomized cube tasks assessing fine-grained 2D-to-3D visual-action alignment.|
|MALMM [192]|Panda|SA|56(30 _↑_)|Custom zero-shot tabletop tasks assessing semantic reasoning and visual grounding.|
|VLA-Touch [193]|Panda|RDT-1B|53_._3(23_._3 _↑_)|<br>Custom contact-rich tasks assessing tactile grasping, pressure, and sustained contact.|


JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

25 

modularity allows the high-level planner to adapt to novel tasks and instructions intuitively, bridging the cognitionexecution gap with highly interpretable sub-goals. 

**Analytical Trade-offs: Monolithic vs. Hierarchical Designs.** A direct comparison between the two paradigms emerges when analyzing hierarchical models that explicitly benchmark against established monolithic systems (e.g., OpenVLA [29], _π_ 0 [236], and RT-2 [30]). The empirical data indicates that while monolithic models provide a robust foundation for generalist control, hierarchical models significantly outperform them in long-horizon planning and structurally complex reasoning. For example, in zero-shot skill recombination and long-horizon tasks, RoboMatrix [181] achieves a 100% relative SR improvement over OpenVLA, while DexVLA [179] outperforms _π_ 0 by 13.5% in tasks evaluating implicit reasoning and cross-embodiment dexterity. Furthermore, when tasks require contextual sequential execution or spatial composition, hierarchical models like RT-H [31] and VoxPoser [187] surpass RT-2 by 15% and 64%, respectively, highlighting the benefits of decoupling dynamic robustness from language interventions. Ultimately, this comparative data suggests a clear trade-off: monolithic models are highly capable standalone generalists optimized for reactive, visually diverse, and contact-rich environments, whereas hierarchical models are structurally necessary for overcoming the performance ceilings of endto-end systems in long-horizon, multi-stage, and zero-shot skill transfer scenarios. 

## **APPENDIX B** 

## **DATASETS AND BENCHMARKS** 

### **B.1 Real-world Robot Datasets** 

Real-world data, capturing environmental complexity such as dynamic lighting, background motion, and varied object properties, is vital for training and evaluating VLA models. Effective language grounding and semantic generalization rely on aligning natural language instructions, perceptual inputs, and precise action responses. To support this, a series of large-scale real-world datasets have emerged. BC-Z [237] provides expert demonstrations with language commands across 100 tasks; RT-1 [20] and its kitchen variant extend this to over 700 daily activities, while RT-2 [30] incorporates web-scale vision-language data for broader vocabulary and instruction generalization. RoboFlamingo [128] exemplifies the transfer of pretrained multimodal priors into realworld control. BridgeData V2 [238] and RH20T [239] further enhance cross-domain generalization through extensive, language-annotated demonstrations, with RH20T enabling one-shot learning across 147 tasks. DROID [240] expands this landscape with teleoperated demonstrations “in the wild,” offering diverse visual contexts over 564 tasks. Most notably, the OXE dataset [110] unifies over 1 million multimodal demonstrations across 22 robot platforms and 500+ skills, marking a significant step toward web-scale, crossembodiment generalization. Although these efforts improve real-world applicability, the long-tail distribution of openworld objects, scenes, and skills remains underrepresented, underscoring the need for broader and more diverse realworld data to scale large VLM-based VLA models further. 


Fig. 7: Illustration of four dataset types that underpin large VLM-based VLA models for robotic manipulation. 

### **B.2 Simulation Datasets and Benchmarks** 

To overcome real-world data limitations, physics-based simulators and virtual environments offer scalable, safe, and reproducible interaction data, aligning with the multimodal, large-scale training needs of large VLM-based VLA models. They enable complex instruction following, multistage planning, and consistent language grounding with automatic evaluation. BEHAVIOR [241] supports multistep semantic control in cluttered household settings; ALFRED [242] focuses on long-horizon tasks specified by egocentric language instructions; RLBench [243] allows finegrained policy learning through RGB-D tabletop manipulation, and RLBench2 [244] extends it to bimanual manipulation with language-conditioned action prediction. Benchmarks such as Meta-World [245], Franka Kitchen [246], and LIBERO [227] further advance this direction by incorporating multi-skill scenarios, often enriched with language annotations and vision-language rewards to encourage generalization. CALVIN [229] enables multi-stage manipulation under unconstrained language instructions to support long-horizon behaviors. MIKASA-Robo [247] addresses memory-centric challenges by evaluating agents under partial observability in tabletop tasks. SIMPLER [248] bridges the sim-to-real gap through calibrated simulated environments aligned with common real-world robot configurations, reducing discrepancies in perception and control. High-fidelity platforms such as Habitat [249]–[251] and SAPIEN [252] support spatial reasoning and manipulation learning in realistic 3D environments, enabling scalable embodied VLA research. Beyond traditional simulation benchmarks, THE COLOSSEUM [253] and VLABench [254] extend simulation benchmarks by assessing robustness under distribution shifts and supporting universal languageconditioned manipulation, respectively. Despite limitations such as imperfect physics and visual artifacts, simulation remains crucial for efficient training, systematic evaluation, and robust real-world generalization. 

### **B.3 Human Behavior Datasets** 

Large-scale human behavior datasets offer semantically rich and contextually diverse demonstrations that are wellsuited for pretraining VLA models. Egocentric video cor- 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

26 

pora such as Ego4D [255], Ego-Exo4D [256], EgoPlanBench [257], and EgoVid-5 [258] capture diverse daily activities from a first-person perspective. In contrast, domainspecific datasets like EPIC-Kitchens [259] and COMKitchens [260] focus on fine-grained, temporally structured cooking tasks. These resources support learning of object recognition, action sequencing, and task decomposition. Reasoning-oriented datasets such as EgoVQA [261] and EgoTaskQA [262] further enhance cognitive grounding by introducing spatial, temporal, and causal reasoning over egocentric video. To address the lack of precise manipulation signals in general-purpose corpora like Ego4D, EgoDex [263] extends this line of work with 829 hours of egocentric video paired with dense 3D hand and finger tracking. Similarly, smaller manipulation-focused datasets such as DexCap [264], EgoMimic [265], and PH<sup>2</sup> D [266] offer fine-grained supervision for hand-object coordination and embodiment-aware policy learning. Complementing these human-centric datasets, R2R2R [267] offers a scalable pipeline that replaces teleoperation with smartphone scans and human videos to generate high-fidelity demonstrations. Together, these resources provide a rich spectrum of semantic grounding, embodiment alignment, and data scalability essential for training generalist VLA models. 

### **B.4 Embodied Datasets and Benchmarks** 

As robots advance toward greater autonomy, understanding and planning tasks become essential. Leveraging strong language and world knowledge, VLMs empower VLA systems to plan over long horizons, parse complex instructions, and build cross-modal reasoning for semantic decision-making. In response, a growing set of benchmarks has emerged to evaluate embodied agents’ planning and reasoning abilities. Early efforts such as EmbodiedQA [268] and IQUAD [269] established the integration of vision, language, and spatial navigation through question-answering in 3D environments. These have since evolved into more cognitively demanding tasks. MT-EQA [270] incorporates multi-target reasoning, MP3D-EQA [271] introduces 3D point cloud inputs for enhanced spatial grounding, EQA-MX [272] adds non-verbal cues for naturalistic multimodal interaction, and OpenEQA [273] expands the scope to open-ended questions involving functional and commonsense reasoning. Complementarily, LoTa-Bench [274] directly evaluates plan executability by deploying LLM-generated plans in simulation. Collectively, these benchmarks emphasize active perception, reasoning, and execution, offering rigorous protocols to assess high-level semantic planning in general-purpose VLA. 

## **APPENDIX C OUTLOOK** 

### **C.1 Future Directions** 

**Datasets and Benchmarking.** As VLA models advance, the reliance on simulated datasets reveals a significant reality gap. Synthetic scenes lack the visual complexity of real environments. By contrast, collecting real-world data is costly, limiting both diversity and scale. Meanwhile, existing benchmarks typically focus on short-horizon pick-and-place 

tasks and report simple success rates. These settings offer little insight into practical challenges such as long-term planning, mobile manipulation and multi-agent collaboration. Future datasets may combine large-scale real-world data acquisition with task suites that capture practical challenges. Evaluations should include richer metrics, such as subtask success, time efficiency, and robustness to disturbances. Such datasets and benchmarks would enable systematic progress on the broader capabilities of VLA systems. 

**Memory Mechanisms and Long-Term Planning.** Effective real-world manipulation often requires planning over extended horizons and recalling past observations. However, most current VLAs rely on frame-by-frame reasoning, resulting in short-sighted behavior and a limited ability to leverage historical context. To address this, a promising direction is to design architectures that incorporate forwardlooking planning and memory mechanisms with episodic awareness. By grounding high-level decisions in contextual memory, agents may move beyond reactive responses toward coherent, goal-driven action sequences, enabling more consistent and effective manipulation in complex scenarios. 

**3D and 4D Perception.** Robotic manipulation inherently involves interacting with objects in a three-dimensional and temporally dynamic environment. However, existing VLA models operate primarily on static 2D visual inputs. This limits the agent’s ability to reason about complex spatial and temporal information, including depth, affordances, object movement, and human actions. Moving beyond static 2D snapshots, 4D perception demands a model to understand how 3D scenes evolve over time. The progression from 2D to 4D perception requires integrating depth or point cloud observations, as well as fusing multi-modal inputs into unified representations. It also involves embedding perception that is grounded in temporal context and replanning actions on the fly. Together, these 4D-aware abilities would enable more robust and adaptive manipulation in the real world. 

**Mobile Manipulation.** Real-world tasks often demand the simultaneous execution of locomotion and manipulation, giving rise to the specialized domain of mobile manipulation. This task requires a synergistic integration of navigation capabilities and interactive skills with the environment, introducing tightly coupled demands on perception and control. Rather than treating locomotion and grasping as separate stages, future VLA models may benefit from learning integrated policies that adaptively prioritize locomotion and arm coordination, ultimately leading to more robust and flexible mobile manipulation. 

**Multi-Agent Cooperation.** Many real-world collaborative tasks, such as bulky objects moving or joint tool use, require agents to negotiate intentions, adapt to teammates’ actions, and jointly reason over multi-step goals. However, single-agent VLAs often falter when communication and role assignment become critical, highlighting the need for interaction-aware representations. Integrating emergent dialogue protocols with shared world models may enable agents to synchronize plans and flexibly allocate subtasks. Such cooperative capabilities promise to elevate robotic teams from loosely coordinated individuals to cohesive collaborators capable of addressing complex group objectives. 

**Lifelong Learning in Open-World.** Robotic autonomy demands continual skill acquisition without catastrophic 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

27 

forgetting. However, most VLA models trained on static datasets struggle to handle unfamiliar objects and novel interaction modes. They also have difficulty incorporating new experiences. This reveals the limits of static training paradigms. Future VLA systems may benefit from mechanisms that incrementally accumulate knowledge through exploration and feedback in open-world. Incorporating memory structures that grow over time and enabling agents to self-organize experiences into reusable abstractions may also provide a foundation for long-term competence. 

**Model Efficiency.** Though VLA models excel at understanding vision-language instructions and planning actions, they often suffer from prohibitive computational and memory costs. Deploying these models on resource-constrained robotic platforms raises concerns about latency, memory usage, and sustained operation. The key challenges lie in balancing model capacity with real-time inference requirements and preserving multimodal alignment to maintain accuracy during compression. Promising directions include task-aware dynamic token pruning, asynchronous inference for seamless transitions between action chunks, and hardware-friendly quantization schemes. 

### **C.2 Discussion** 

As the field of vision language action modeling rapidly matures, several core agreements, emerging paradigms, and theoretical disputes have surfaced. By synthesizing the recent advancements reviewed in this survey, we provide a critical subjective analysis of the current research trajectory. 

**Established and Emerging Consensus.** A firm consensus has emerged within the community regarding the efficacy of transferring internet-scale visual-semantic priors to physical embodiments. Researchers uniformly agree that initializing robotic policies with massive pre-trained large vision-language models fundamentally addresses the semantic grounding bottleneck, enabling models to demonstrate zero-shot generalization potential when encountering novel objects and unconstrained linguistic instructions. Furthermore, an emerging consensus is shifting the perspective on low-level action generation. While early models relied heavily on pure discrete autoregressive token prediction for control, the community increasingly recognizes that representing continuous, high-precision physical movements via discrete text tokens suffers from compounding spatial errors and temporal instability in long-horizon tasks. Consequently, integrating continuous action generation paradigms (such as diffusion policies or flow-matching networks) as the execution engine is rapidly becoming the accepted standard for achieving smooth and reliable control. 

**Key Controversies and Opposing Views.** Despite these agreements, significant theoretical divides remain. The most prominent controversy centers on the integration of explicit world models versus purely implicit end to end architectures. One camp argues that large monolithic VLA models can implicitly internalize the laws of physics and environmental dynamics simply by scaling up model parameters and robot interaction data, rendering separate simulation modules redundant. Conversely, opposing researchers argue that without explicit predictive world models to simulate future states and enforce geometric constraints, VLAs 

will always remain vulnerable to severe hallucinations and visual kinematic overfitting in out of distribution scenarios. Critics of the explicit world model approach counter this by pointing out that simulating high fidelity video or 3D environments adds prohibitive computational overhead, creating unacceptable latency for real time reactive control. 

**Critical Insights: Successes and Persistent Bottlenecks.** Although current VLA architectures excel at interpreting complex human intents and achieving broad semantic generalization, a critical examination reveals profound structural limitations in physical grounding, data scaling, temporal control, and explicit environmental modeling that severely bottleneck true real world autonomy. 

- **Illusory Physical Reasoning and Statistical Shortcuts.** Large vision-language models fundamentally operate as statistical pattern learners over 2D data, lacking true causal grounding in 3D physical dynamics. Apparent task success (e.g., object placement) largely stems from exploiting language priors and visual co-occurrence, rather than understanding underlying physics, revealing a reliance on trajectory imitation instead of genuine embodied cognition. 

- **Embodiment Heterogeneity and the Breakdown of Scaling.** Robot data is intrinsically heterogeneous, entangled with kinematics, sensing configurations, and embodiment-specific constraints. Na¨ıve data aggregation induces distributional conflicts and performance collapse, in contrast to the scaling benefits observed in language models. Coupled with the high cost of teleoperation data, this limits scalability unless new paradigms beyond imitation learning (such as largescale autonomous reinforcement learning) are realized. 

- **Pseudo Closed-Loop Control and Missing Temporal Dynamics.** Despite end-to-end claims, most VLAs generate open-loop action sequences delegated to low-level controllers. This induces temporal misalignment and weak responsiveness in dynamic, contact-rich settings, leading to error accumulation over long horizons due to the absence of continuous-time dynamics modeling. 

- **Implicit Memorization vs. Explicit World Modeling.** Monolithic VLAs rely on implicit parameterized memorization of physical regularities, lacking explicit geometric and causal constraints, and thus are prone to hallucination under distribution shift. Explicit world models provide principled physical simulation but incur prohibitive computational costs for real-time control. This trade-off between scalability and physical fidelity remains a core barrier to safe deployment. 

Ultimately, overcoming these foundational barriers requires the robotics community to move beyond simply scaling static two dimensional pattern matchers. Future breakthroughs will depend on developing native multimodal architectures that seamlessly integrate explicit causal physical reasoning, scalable autonomous exploration, and high frequency continuous control. 

## **APPENDIX D** 

## **PRACTICAL MODEL-SELECTION GUIDELINES** 

This appendix complements the architecture-oriented taxonomy in the main manuscript with a model-selection per- 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

28 

TABLE 10: Practical model-selection guide for representative single-system VLA methods. A baseline denotes the architectural predecessor or principal comparator used by the cited paper. Numeric gains are paper-specific and are not comparable across rows because datasets, robots, metrics, and protocols differ. 

|Method|Primary baseline(s)|Limitation addressed and evidence|Trade-off|Recommended scenario|
|---|---|---|---|---|
|RT-2 [30]|RT-1; VC-1|Co-fines-tunes web vision-language and<br>robot data; PaLI-X-55B reports about<br>59% average on emergent-skill tests<br>versus about 17% for RT-1.|The strongest version is very large and<br>closed; autoregressive action tokens<br>raise compute, latency, and<br>reproducibility barriers.|Semantic OOD commands and web-<br>knowledge transfer when datacenter-<br>scale inference is acceptable.|
|OpenVLA [29]|RT-2-X; Diffusion<br>Policy for adaptation|Open 7B generalist trained on 970k<br>demonstrations; reports+16_._5points<br>over RT-2-X across 29 tasks and+20_._4<br>points over Diffusion Policy.|Still a 7B autoregressive policy; new<br>embodiments or high-frequency tasks<br>generally require task-specific<br>fine-tuning and serving optimization.|Default open, reproducible baseline for<br>generalist manipulation, ablations, and<br>downstream fine-tuning.|
|ECoT [112]|OpenVLA|Adds grounded reasoning over plans,<br>subtasks, motions, boxes, and<br>end-effector states; reports a 28-point<br>gain on generalization tasks.|Requires synthetic reasoning<br>annotations and extra autoregressive<br>reasoning tokens, increasing pre-action<br>latency.|Semantic ambiguity, OOD generaliza-<br>tion, failure diagnosis, and human cor-<br>rection rather than tight control loops.|
|ReVLA [113]|OpenVLA|Merges the vision backbone toward its<br>pretrained state to reduce forgetting;<br>reports 77% and 66% relative gains for<br>visual-OOD grasping and lifting.|Targets visual domain shift, not control<br>frequency or dynamics; performance<br>depends on the merging schedule.|Stable action spaces with large shifts<br>in lighting, textures, backgrounds, or<br>object appearance.|
|TraceVLA [114]|OpenVLA|Encodes state-action history as traces;<br>reports+10% on SimplerEnv and3_._5_×_<br>success on its physical-robot tasks.|Needs trace construction and 150k<br>additional trajectories; benefits depend<br>on tracking quality.|Motion sensitive or progress dependent<br>tasks where a single frame is insuffi-<br>cient.|
|SpatialVLA [117|]<br>OpenVLA;<br>RT-1-X/RT-2-X; Octo|Adds depth-derived egocentric 3D<br>encoding and action grids; reports<br>20.1 Hz versus 5.0 Hz for OpenVLA,<br>with stronger spatial transfer.|Depends on depth estimation and<br>camera intrinsics, uses 1.1M episodes,<br>and re-discretizes action grids for a new<br>robot.|3D layout changes, cross-robot spa-<br>tial transfer, and geometry-dominated<br>tasks.|
|RoboMamba<br>[129]|OpenVLA-7B;<br>ManipLLM-7B|A 2.8B Mamba plus 3.7M pose head<br>runs at 9.0 Hz on A100 versus<br>3.4/1.1 Hz; the OpenVLA comparison is<br>about2_._6_×_.|Speed is reported for a narrower SE(3)<br>pose interface, not a matched<br>cross-embodiment generalist-policy<br>comparison.|Efficient pose-level reasoning/control<br>within the supported setup.|
|OpenVLA-<br>OFT [47]|OpenVLA; adapted<br>_π_0/RDT-1B|Parallel decoding, chunks, continuous<br>actions, and L1 training raise LIBERO<br>average success from 76.5% to 97.1%<br>and throughput by26_×_.|An adaptation recipe, not a zero-shot<br>replacement; needs robot/task<br>demonstrations and changes the base<br>action interface.|High-frequency, dexterous, or bimanual<br>deployment starting from OpenVLA.|


spective. For each representative method, we identify: (1) the principal baseline or architectural predecessor; (2) the limitation addressed by the proposed innovation; (3) the corresponding trade-off; and (4) the task or deployment scenario for which the method is most appropriate. Because the reported results are obtained using different platforms, datasets, and evaluation protocols, numerical values should not be compared directly across rows and should not be interpreted as a global ranking. 

**Single-System Models.** As summarized in Table 10, OpenVLA [29] is a strong default when openness, reproducibility, and a mature fine-tuning ecosystem are priorities. When the main bottleneck is semantic or visual generalization, ECoT [112], ReVLA [113], TraceVLA [114], and SpatialVLA [117] target reasoning, visual-domain shift, temporal motion cues, and 3D spatial structure, respectively, but introduce additional annotations, sensing assumptions, or computation. For deployment speed, RoboMamba [129] reduces backbone and head cost, whereas OpenVLA-OFT [47] preserves the OpenVLA starting point and obtains high-rate continuous action chunks through task-specific adaptation. Therefore, single-system efficiency claims should always be read together with the action interface and evaluation scope. 

**Dual-System Models.** As summarized in Table 11, dualsystem designs are preferable when continuous or highfrequency action generation is the primary requirement. _π_ 0 [32] provides a strong generalist flow-matching foundation, while _π_ 0 _._ 5 [33] adds semantic co-training for open-world long-horizon tasks. CogACT [148] and RoboDual [146] are suitable when a specialized action expert can be trained for higher precision or control rate. SmolVLA [34] targets 

resource-constrained deployment, GR00T N1 [35] targets humanoid and bimanual systems, and ForceVLA [158] targets contact-rich tasks with force-torque sensing. These benefits come at the cost of an additional action module, or a more complex training/data recipe. 

**Hierarchical Models.** As summarized in Table 12, hierarchical models are preferable when a task requires longhorizon decomposition, explicit intermediate representations, human intervention, or verifiable geometric constraints. PaLM-E [21] and HiRobot [177] are suitable for high-level semantic planning when a reliable library of low-level skills is already available. RoboPoint [170] and HAMSTER [51] use keypoints or paths to bridge highlevel visual reasoning and low-level control, making them attractive for geometry-intensive manipulation and crossdomain transfer. VoxPoser [187] and ReKep [53] are preferable when training-free deployment, explicit 3D constraints, and inspectable planning are priorities, whereas RT-H [31] supports interpretable language-level intervention during execution. These advantages come at the cost of additional planner–policy interfaces, possible error propagation between levels, increased inference latency, or dependence on low-level controllers. The choice of a hierarchical method should be based on the desired intermediate representation and the available downstream control components. 

Single-system models provide a simple and reproducible starting point, dual-system models are generally better suited to high-frequency and precise continuous control, and hierarchical models are preferable for long-horizon, interpretable, or constraint-driven tasks. Model selection should balance task requirements against control latency, 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

29 

TABLE 11: Practical model-selection guide for representative dual-system VLA methods. 

|Method|Primary baseline(s)|Limitation addressed and evidence|Trade-off|Recommended scenario|
|---|---|---|---|---|
|_π_0 [32]|Autoregressive VLAs<br>such as<br>RT-2/OpenVLA|Adds a flow-matching action expert<br>for continuous chunks and reports<br>control up to 50 Hz across dexterous,<br>cross-embodiment tasks.|Relies on more than 10,000 hours of<br>robot data, substantial compute, and<br>iterative flow generation; the latent<br>interface is not human-interpretable.|High-frequency continuous control and<br>dexterity when large-scale data and com-<br>pute are available.|
|_π_0_._5 [33]|_π_0|Adds heterogeneous co-training and<br>semantic/subtask prediction, enabling<br>long-horizon manipulation in entirely<br>unseen homes.|Broader capability comes from a more<br>complex data mixture and<br>annotation/training recipe; the system<br>remains resource intensive.|Open-world household tasks with long<br>horizons, semantic decisions, and novel<br>environments.|
|CogACT [148]|OpenVLA; RT-2-X|Replaces action quantization with a<br>diffusion action transformer; reports<br>over 35% gains over OpenVLA in<br>simulation and 55% in real-world.|Adds a separately parameterized<br>denoising module and tighter<br>VLM-policy coupling, increasing<br>training and serving complexity.|Precise, multimodal action distributions<br>when minimal architecture and explicit<br>plans are secondary.|
|RoboDual [146]|OpenVLA|Adds a 20M specialist; reports+26_._7<br>points in real-world tests,+12points<br>on CALVIN, and3_._8_×_control<br>frequency.|The specialist needs in-domain<br>demonstrations and another maintained<br>module; gains may not transfer<br>unchanged across embodiments.|Known deployment domains with lim-<br>ited demonstrations and strict control-<br>rate requirements.|
|SmolVLA [34]|_π_0; ACT;<br>OpenVLA/Octo<br>comparisons|A 0.45B model reaches 87.3% LIBERO<br>average versus 86.0% for robotics<br>pretrained_π_0, while training about<br>40% faster with6_×_less memory.|Pretraining uses about 23k trajectories<br>and one robot family; longer action<br>execution improves speed but reduces<br>responsiveness.|Consumer GPUs/CPUs, low-cost arms,<br>teaching labs, and rapid iteration.|
|GR00T N1 [35]|BC-Transformer;<br>Diffusion Policy|Combines an Eagle VLM, diffusion<br>transformer, and<br>real/human-video/synthetic data;<br>reports strong multi-embodiment<br>humanoid results.|Humanoid-oriented post-training,<br>simulation assets, and<br>embodiment-specific data remain<br>substantial integration requirements.|Humanoid or bimanual industrial ma-<br>nipulation with synthetic-data and post-<br>training infrastructure.|
|TinyVLA [157]|OpenVLA|Uses a compact backbone and<br>diffusion decoder without robot<br>pretraining; reports faster, more<br>data-efficient learning with<br>comparable evaluated success.|Savings come from target-domain<br>fine-tuning, so broad zero-shot and<br>cross-embodiment capability is less<br>established.|Fast prototyping or new tasks with few<br>demonstrations and no large pretraining<br>stage.|
|ForceVLA [158]|_π_0-based baselines|Fuses 6-axis force through a<br>force-aware MoE; reports+23_._2%<br>average success and up to 80% on<br>plug insertion.|Requires synchronized force-torque<br>sensing, calibration, and specialized<br>data; the modality does not help<br>ordinary free-space tasks by default.|Insertion, assembly, wiping, and other<br>contact-rich tasks with occlusion or un-<br>certain contact.|


data budgets, sensing assumptions, interpretability, and integration complexity. Tables 10–12 instantiate these rules with named baselines and explicit trade-offs. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 

30 

TABLE 12: Practical model-selection guide for representative hierarchical VLA methods. 

|Method|Primary baseline(s)|Limitation addressed and evidence|Trade-off|Recommended scenario|
|---|---|---|---|---|
|PaLM-E [21]|PaLM plus<br>task-specific<br>multimodal/robot<br>planners|Injects continuous sensor observations<br>into an LLM and jointly trains robotics,<br>VQA, and captioning, demonstrating<br>positive transfer across embodiments.|Planner outputs need a downstream<br>controller; the largest 562B model is<br>costly and does not directly provide<br>high-frequency actions.|High-level multimodal planning when<br>broad reasoning is primary and reliable<br>skills/controllers already exist.|
|RoboPoint [170]|GPT-4o; PIVOT|Trains a VLM to emit 2D affordance<br>keypoints from synthetic data; reports<br>+21_._8% affordance accuracy and<br>+30_._5% downstream success.|Produces points rather than control;<br>accuracy can inherit synthetic-data and<br>projection biases and needs a motion<br>planner/policy.|Scalable spatial grounding, pick/place<br>targets, navigation points, and AR assis-<br>tance.|
|VoxPoser [187]|Code as Policies;<br>language-<br>conditioned<br>manipulation<br>baselines|Composes 3D value maps and<br>model-based planning for zero-shot<br>closed-loop trajectories over open-set<br>instructions and objects.|Depends on RGB-D, open-vocabulary<br>models, code generation, and<br>optimization; component errors<br>compound and contact-rich dynamics<br>need extra modeling.|Training-free open-vocabulary tabletop<br>tasks with calibrated 3D sensing and ac-<br>cessible model APIs.|
|ReKep [53]|VoxPoser-style<br>value-map planning|Uses executable relational<br>keypoint-cost functions and<br>hierarchical optimization for bimanual<br>and reactive tasks without task data.|Sensitive to segmentation/tracking and<br>constraint-generation errors; nonlinear<br>optimization can be slow or locally<br>infeasible.|Relational geometry, reactivity, and in-<br>spectable<br>constraints<br>over<br>end-to-end<br>simplicity.|
|RT-H [31]|RT-2-style flat<br>task-to-action<br>prediction|Inserts language motions between task<br>and action, improving sharing across<br>diverse tasks and enabling language<br>intervention/correction.|Requires language-motion supervision<br>or intervention data; language can<br>mis-specify fine geometry and still relies<br>on the low-level policy.|Multitask policies that must accept inter-<br>pretable human-in-the-loop corrections.|
|HAMSTER [51]|OpenVLA|Uses VLM-generated 2D paths to<br>condition a 3D policy; reports+20<br>points average across seven<br>generalization axes over OpenVLA.|A 2D path discards depth/contact detail<br>and needs path data plus a trained 3D<br>policy; high-level errors propagate.|Cross-domain<br>transfer<br>from<br>videos,<br>sketches, or simulation to precise real-<br>robot control.|
|HiRobot [177]|Direct-instruction<br>_π_0-style control|Converts open-ended prompts and<br>feedback into atomic commands for a<br>low-level VLA, supporting complex<br>household workflows.|Two-stage inference adds latency and<br>error propagation; success is bounded<br>by the low-level policy’s atomic skill<br>coverage.|Long-horizon household tasks with user<br>feedback, semantic preferences, and reli-<br>able skills.|
|DexVLA [179]|Octo; OpenVLA;<br>Diffusion Policy|l<br>Scales a plug-in diffusion expert to 1B<br>parameters with an embodiment<br>curriculum for complex long-horizon<br>and cross-embodiment control.|The large expert and three-stage recipe<br>raise compute and engineering cost; the<br>latent/subtask interface is less<br>inspectable than keypoint/program<br>hierarchies.|Dexterous<br>long-horizon<br>tasks<br>across<br>single-arm, bimanual, or dexterous-hand<br>platforms.|


