---
title: "Pure Vision Language Action (VLA) Models: A Comprehensive Survey"
date: "2025-09-23"
authors: "Dapeng Zhang; Jing Sun; Chenghui Hu; Xiaoyan Wu; Zhenlong Yuan; Rui Zhou"
url: https://arxiv.org/abs/2509.19012
pdf: https://arxiv.org/pdf/2509.19012
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2509.19012)** / [論文ページ](https://arxiv.org/abs/2509.19012)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# Pure Vision-Language-Action (VLA) Models: A Comprehensive Survey 

Dapeng Zhang*<sup>1,2</sup> , Jing Sun*<sup>1</sup> , Chenghui Hu*<sup>1</sup> , Xiaoyan Wu<sup>1</sup> , Zhenlong Yuan<sup>3</sup> , Rui Zhou<sup>1</sup> , Fei Shen<sup>†2</sup> , and Qingguo Zhou<sup>†1</sup> 

**Abstract** —The emergence of Vision-Language-Action (VLA) models marks a paradigm shift from traditional policy-based control to generalized robotics, reframing Vision-Language Models (VLMs) from passive sequence generators into active agents for manipulation and decision-making in complex, dynamic environments. This survey delves into advanced VLA methods, aiming to provide a clear taxonomy and a systematic, comprehensive review of existing research. It presents a comprehensive analysis of VLA applications across different scenarios and classifies VLA approaches into several paradigms: autoregression-based, diffusion-based, reinforcement-based, hybrid, and specialized methods; while examining their motivations, core strategies, and implementations in detail. In addition, foundational datasets, benchmarks, and simulation platforms are introduced. Building on the current VLA landscape, the review further proposes perspectives on key challenges and future directions to advance research in VLA models and generalizable robotics. By synthesizing insights from over three hundred recent studies, this survey maps the contours of this rapidly evolving field and highlights the opportunities and challenges that will shape the development of scalable, general-purpose VLA methods. 

and highlights the opportunities and challenges that will shape the development of scalable, general-purpose VLA methods. **Index Terms** —Vision-Language-Action, Vision-Language Model, Robotics, Embodied AI **1 INTRODUCTIONS** Robotics has long been a prominent area of scientific research. Historically, robots primarily relied on preprogrammed instructions and engineered control policies to perform task decomposition and execution. These methods were commonly applied to simple, repetitive tasks, such as factory assembly lines and logistics sorting. In recent years, the rapid advancement of artificial intelligence has enabled researchers to exploit the feature extraction and trajectory prediction capabilities of deep learning across diverse modalities, including images, text, and point clouds. By integrating techniques such as perception, detection, tracking, and localization, researchers have decomposed robotic tasks into multiple stages to meet execution requirements, thereby advancing the development of embodied intelligence and autonomous driving. However, most of these robots still operate as isolated agents, designed for specific tasks and lacking effective interaction with humans and external environment. To address these limitations, researchers have begun ex- 

**Index Terms** —Vision-Language-Action, Vision-Language Model, Robotics, Embodied AI 

✦ 


To address these limitations, researchers have begun exploring the incorporation of large language models (LLMs) and vision-language models (VLMs) to enable more accurate and flexible robotic manipulation. Modern robotic 

Fig. 1: Organization and Structure of the VLA Survey. 

manipulation methods [1], [2] typically leverage vision language generative paradigms (e.g., autoregressive models [3], [4], [5], [6] or diffusion models [7]), combined with large-scale datasets [8] and advanced fine-tuning strategies. We refer to these as VLA foundation models, which have substantially improved the quality of robotic manipulations. Fine-grained action control over generated content provides users with greater flexibility, unlocking the practical potential of VLA for task execution. 

- 1 _Lanzhou University, China_ 2 _National University of Singapore, Singapore_ 

   - 3 _Institute of Computing Technology, Chinese Academy of Sciences, China_ 

- _* Equal contributions_ 

- _† Fei Shen and Qingguo Zhou are the corresponding authors_ 

- _• D. Zhang, J. Sun, C. Hu, X. Wu, R. Zhou and Q. Zhou are with School of Information Science and Engineering, Lanzhou University, China. E-mail: {zhangdp22, sjing2023,huchh2024,wuxiaoyan2024,zr,zhouqg}@lzu.edu.cn_ 

Despite their promise, reviews of pure VLA methods remain scarce. Existing surveys either focus on taxonomy over VLM foundational models or provide broad overviews 

- _Z. Yuan is with the Institute of Computing Technology, Chinese Academy of Sciences, China. E-mail: yuanzhenlong21b@ict.ac.cn_ 

- _D. Zhang and F. Shen are with the NExT++ Research Centre, National University of Singapore, Singapore. E-mail: shenfei29@nus.edu.sg_ 

2 


Fig. 2: Illustration of various VLA skeleton. 

of robotic manipulation as a whole. Firstly, VLA methods represent a nascent field in robotics, with no established methodological landscape or consensus taxonomy, making it challenging to systematically summarize these approaches. Secondly, current reviews either classify VLA approaches based on differences in foundational models or present a comprehensive analysis of robotic applications across the entire history of the field, often emphasizing traditional methods at the expense of emerging techniques. While these reviews offer valuable insights, they provide only cursory examinations of robotic models or concentrate primarily on foundational models, leaving a significant gap in the literature regarding pure VLA methods. 

In this paper, we investigate VLA methods and associated resources, providing a focused and comprehensive review of existing approaches. Our goal is to present a clear taxonomy, systematically summarize VLA research, and elucidate the development trajectory of this rapidly evolving field. After a brief overview of LLMs and VLMs, we focus on the policy strategies of VLA models, highlighting the unique contributions and distinctive features of previous studies. We classify VLA approaches into 4 categories: autoregression-based, diffusion-based, reinforcement-based, hybrid, and specialized methods, and provide a detailed analysis of their motivations, core strategies, and mechanisms. As shown in Fig. 2, we present a VLA skeleton of these methods. We examine application domains, including robotic arms, quadruped robots, humanoids, and wheeled robots (autonomous vehicles), offering a comprehensive assessment of VLA deployment across diverse scenarios. Given the strong dependence of VLA models on datasets and simulation platforms, we provide a concise overview of these resources. Finally, based on the current VLA landscape, we identify key challenges and outline future research directions—including data limitations, inference speed, and safety—to accelerate the advancement 

of VLA models and generalizable robotics. 

The overall structure of this survey is illustrated in Fig. 1. First, Section 2 provides an overview of the background for VLA research. Section 3 presents the existing VLA approaches in the robotics field. Section 4 introduces the datasets and benchmarks employed by VLA approaches. Sections 5 and 6 discuss simulation platforms and robotic hardware. Section 7 further discusses the challenges and future directions for VLA-based robotic methods. Finally, we summarize the paper and provide our perspective on future developments. 

In summary, our contributions are as follows: 

- We present the well-structured taxonomy of pure VLA methods, classifying approaches based on their action-generation strategies. This facilitates understanding of existing methods and highlights core challenges in the field. 

- The survey emphasizes the defining characteristics and methodological innovations of each category and technique, providing a clear perspective on current approaches. 

- We provide a comprehensive overview of associated resources (datasets, benchmarks and simulation platforms) for training and evaluating VLA models. 

- We investigate the practical impact of VLA in robotics, identify key limitations of existing techniques, and propose potential avenues for further exploration. 

## **2 BACKGROUNDS** 

The emergence of Vision-Language-Action (VLA) models represents a significant advance toward general-purpose embodied intelligence. Traditional robotic systems typically rely on isolated perception pipelines, hand-engineered control strategies, or task-specific reinforcement learning. Although these approaches perform effectively in constrained environments, such as factory floors or laboratories, they generalize poorly to dynamic and unstructured settings. Modern robots can “see” using computer vision models, “understand” language through large language models, and “act” via controllers or learned policies; however, integrating these capabilities into a coherent and unified system remains a key challenge. VLA models address this challenge by providing a unified framework that grounds language in perception and maps it to executable actions. 

### **2.1 Early: LLM/VLM fundamental Models** 

Breakthroughs in unimodal modeling have laid the methodological and engineering foundation for multimodal integration. In computer vision, convolutional neural networks (e.g., AlexNet [9], ResNet [10]) established a representational paradigm transitioning from local convolutions to deep residual learning, which was further advanced by the Vision Transformer (ViT) [11]. ViT introduced self-attention to the image domain, markedly improving transferability and generalization. In natural language processing, the Transformer architecture enabled large-scale pretraining and alignment techniques, giving rise to models such as BERT [12], GPT [13], T5 [14], and GPT-4 [15], which exhibit 

3 


Fig. 3: Vision-Language-Action Taxonomy: From Autoregression-based, Diffusion-based, to Reinforcement-based and Hybrid/Specialized methods, multi-paradigm advances and practical adaptations in VLA. The taxonomy is organized along a chronological timeline. 

strong reasoning capabilities, instruction-following, and incontext learning. In parallel, reinforcement learning advanced policy optimization and sequential decision-making, progressing from DQN and PPO to Decision Transformer, which highlights a unifying perspective of control through sequence modeling. 

Against this backdrop, vision-language models (VLMs) emerged as a crucial bridge between unimodal learning and embodied intelligence. Early approaches (e.g., ViLBERT [16], VisualBERT [17]) aligned and fused images and text using dual-stream or single-stream Transformers, while contrastive learning methods (e.g., CLIP) mapped large-scale image–text pairs into a shared embedding space, enabling zero-shot and few-shot recognition and retrieval. More recently, instruction-tuned, dialogue-centric multimodal models (e.g., BLIP-2 [18], Flamingo [19], LLaVA [20]) have substantially strengthened open-ended cross-modal understanding, fine-grained grounding, and multi-turn reasoning, setting the stage for Vision-Language-Action (VLA) systems. 

### **2.2 Present: Development of VLA Models** 

### _2.2.1 From LLM/VLM to VLA Models_ 

Following this trajectory, research has naturally advanced toward VLA integration, which unifies visual perception, language understanding, and executable control within a single sequence modeling framework [1], [2], [21], [22], [23]. Typical designs encode images and instructions as prefix or context tokens, inject robot states and sensory feedback as state tokens, and autoregressively generate action tokens to produce control sequences, thereby closing 

the perception-language-action loop. Compared with traditional perception, planning, and control pipelines, VLA provides end-to-end cross-modal alignment and a unified treatment of goals, constraints, and intent. It inherits the semantic and instruction generalization of VLMs, while explicit state coupling and action generation confer robustness to environmental disturbances and long-horizon tasks. This progression—from unimodal to multimodal, and then to multimodal plus executable control—establishes the methodological foundation for systems that can not only see and understand, but also act. 

### _2.2.2 The Supporting Role of Data and Simulation_ 

The development of Vision-Language-Action (VLA) models in robotics relies heavily on high-quality datasets and realistic simulators capable of capturing the complexity of real-world scenarios. Recent robotic methods are typically deep learning–based and data-driven; consequently, dataset collection and annotation play a critical role in driving advancements in the field. Some datasets are collected in real-world settings, which requires substantial human effort and financial resources. To address these challenges, researchers also leverage large-scale human manipulation videos from the Internet as generalization datasets to provide auxiliary supervision for VLA model training. Despite these efforts, data collection remains costly, annotations are labor-intensive, and long-tail corner cases are often underrepresented. Other datasets are generated through robot simulators, which facilitate the collection of large-scale labeled data. Simulators provide diverse and controllable environments, flexible sensor configurations, realistic kinematic models, and interactive static and dynamic scenes, 

4 

supporting both data collection and model evaluation. Representative datasets include Open X-Embodiment (OXE) [8], which integrates 22 robot datasets from 21 institutions, encompassing 527 skills and 160,266 tasks, and BridgeData [24], comprising 71 tasks across 10 environments in multiple domains. These resources standardize data formats, thereby promoting rapid development and reproducibility in VLA research. Simulators such as THOR [25], Habitat [26], MuJoCo [27], Isaac Gym [28], and CARLA [29] offer extensible virtual environments capable of generating multimodal annotations, including action trajectories, object states, and natural language instructions. Collectively, these datasets and simulation platforms mitigate the scarcity of real-world robot data and accelerate the training and evaluation of VLA models. 

### **2.3 Future: Towards General Embodied Intelligence** 

VLA models occupy the forefront of research where vision, language, and action converge. They build upon breakthroughs in foundational models for perception and reasoning, emphasizing capabilities in human interaction and task execution, and extend these abilities to the physical world. By integrating the representational power of visual encoders, the reasoning capabilities of large language models, and the decision-making abilities of reinforcement learning and control frameworks, VLA models hold significant potential to bridge the “perception–understanding–action” gap. Despite facing challenges related to scalability, generalization, safety, and real-world deployment, VLA is widely recognized as a key frontier in embodied artificial intelligence. Although VLA has achieved notable success in Vision-Language-Action interactions, and benefits from advances in large-scale language models, it has not yet attained full generality in the domain of embodied intelligence. General embodied intelligence posits that humanlike intelligent behavior relies not only on cognitive processing but also on the physical body, environmental perception, and feedback mechanisms, enabling interaction with the external world. To accommodate the demands of diverse tasks, general embodied intelligence can manifest through various types of robots, including humanoid robots for household applications, assembly robots with dexterous manipulators, and bionic robots with specialized capabilities. Clearly, general embodied intelligence has the potential to enable artificial systems to perform a wider array of tasks across diverse environments. VLA is currently evolving toward this vision of general embodied intelligence and holds considerable promise for realizing it. 

## **3 VISION-LANGUAGE-ACTION MODELS** 

In recent years, Vision-Language-Action (VLA) models have undergone rapid and systematic development, driven by advances in multimodal representation learning, generative modeling, and reinforcement learning. To trace this evolution, this section reviews the major methodological paradigms in VLA, including autoregressive-based modeling, diffusion-based approaches, reinforcement learning strategies, and hybrid or specialized designs. Fig. 3 presents a tree diagram illustrating the progression of these 

paradigms, with each branch highlighting representative works within the respective taxonomy. The taxonomy is organized chronologically, emphasizing how methodological innovations have progressively expanded the capabilities of VLA models. 

### **3.1 Autoregression-Based Models in Vision-LanguageAction Research** 

Autoregression-based models constitute a classical yet effective paradigm for sequence generation in Vision-LanguageAction (VLA) tasks. By treating action sequences as temporally dependent processes, these models generate actions step by step, conditioned on prior context, perceptual inputs, and task prompts. With the rapid advancement of Transformer architectures, recent VLA systems [21], [30], [31] have demonstrated the scalability and robustness of this approach. Representative works in these directions are summarized in Table 1, collectively highlighting the versatility and generality of the autoregression-based modeling paradigm in VLA research. 

### _3.1.1 Autoregressive Generalist VLA Methodologies_ 

Research on generalist VLA agents unifies perception, task instructions, and action generation within autoregressive sequence modeling. By tokenizing multimodal inputs, these models enable step-by-step action generation across heterogeneous tasks. 

Early work like Gato [32] demonstrated tokenizing heterogeneous modalities for joint training. Subsequent scaling efforts, notably RT-1/RT-2 [30], [34] leveraged massive realworld datasets and web-scale pretraining, while PaLM-E [33] integrated pretrained language knowledge into embodied control, establishing autoregressive Transformers as practical unifying models. 

To address embodiment fragmentation, frameworks like Octo [36], LEO [35], and UniAct [40] aligned visuallinguistic modalities with universal action abstractions for cross-platform compatibility. Recent advances focus on reasoning integration and efficiency. Models now combine action generation with language reasoning and adaptive prompting for long-horizon planning [21], [39], [43]. Lightweight designs like NORA [42] and RoboMM [38] address deployment constraints. 

Overall, research on generalist VLA agents has progressed from early unified tokenization to large-scale realworld training and semantic grounding, advancing toward cross-platform universality, reasoning integration, and efficiency-oriented designs. This trajectory reflects a shift from proof-of-concept demonstrations to systems emphasizing scalability, semantic reasoning, and deployability. Table 1 (A) summarizes representative autoregressive generalist agents and their key contributions. However, issues of safety, interpretability, and alignment with human values remain largely unresolved, leaving ample room for future research. 

### _3.1.2 Autoregressive Reasoning and Semantic Planning with LLMs_ 

The integration of LLMs has transformed them from passive input parsers into semantic mediators within VLA 

5 

TABLE 1: Representative works on Autoregression-Based Models. 

|**Method / Model**|**Year**|**Key Innovation in Autoregression-Based Models**|
|---|---|---|
|**(A) Autoregressive Gener**|**alist VLA M**|**ethodologies**|
|Gato [32]|2022|Unified multimodal Transformer with tokenized vision language states and actions.|
|<br>RT-1 [30]|2022|i     , , ,<br>Real-world robotic Transformer trained on 130k demos with FiLM-based multimodal fusion|
|<br>PaLM-E [33]|2023|.<br>Embodied multimodal LLM combining PaLM and ViT for VQA, navigation, and manipulation.|
|RT-2 [34]<br>LEO [35]<br>|2023<br>2024<br>|Extended PaLM-E with action tokens and web-scale VLM knowledge for open-vocabulary grasping.<br>Two-stage training for 3D vision–language alignment and VLA fine-tuning.<br>|
|Octo [36]<br>|2024|Open-source cross-robot policy trained on 1.5M video instances with reward-free imitation.<br>|
|RUM [37]|2024|Utility-based scoring enabling robust zero-shot deployment and new benchmarks.|
|<br>RoboMM [38]<br>|2024<br>|<br>Multimodal fusion with modality masking achieving SOTA on RoboData.<br>i|
|UP-VLA [39]<br>|2025<br>|Unified prompting framework merging tasks, visuals, and actions for better few-shot performance.<br>i|
|UniAct [40]<br>Humanoid-VLA [41]|2025<br>2025|Defined universal atomic actions to solve cross-embodiment heterogeneity.<br>Applied VLA to humanoid control with multi-view RGB and language prompts|
|<br>NORA [42]<br>|2025<br>|.<br>Lightweight open-source VLA using FAST+ tokenizer and 970k demonstrations.<br>|
|OneTwoVLA [43]|2025|Adaptive System 1 & 2 reasoning for long-horizon planning and error recovery.|
|VOTE [44]<br>UiVLA45|2025<br>2025|<br>Voting-based ensemble reduces action tokens for faster inference and training.<br>Ld tkti ltt ti tti f di id|
|n []<br>OE-VLA [46]|2025|earne as-cenrc aen acon represenaons rom verse veos.<br>Extended VLAs for open-ended multimodal instruction following.|
|**(B) Autoregressive Reaso**|**ning and Se**|**mantic Planning with LLMs**|
|Inner Monologue [47]|2022|Introduced inner language-driven reasoning loop, improving embodied task success.|
|<br>Instruct2Act [48]<br>RoboFlamingo [49]<br>|2023<br>2023<br>|<br>Proposed vision–language–task script–action pipeline with semantic intermediaries.<br>Adapted OpenFlamingo to robotics, enabling efficient VLM-to-VLA transfer.<br>|
|LLaRA [50]<br>ECoT [51]|2024<br>2024|Augmented trajectories with dialogue tasks to enhance data and transfer.<br>Formalized embodied chain-of-thought reasoning to boost OpenVLA.|
|<br>Mobility VLA [52]<br>|2024<br>|<br>Integrated long-context VLM with navigation for multimodal instruction-following.<br>|
|UAV-VLA [53]|2025|Generated UAV missions from satellite imagery using VLM-based planning.|
|Tactile-VLA [54]|2025|Combined tactile feedback with reasoning for precise, adaptive control.|
|<br>Shake-VLA [55]<br>|2025<br>|<br>Introduced multimodal bimanual system with speech, vision, and haptics.<br>i|
|Hi Robot [56]|2025|Adopted hierarchical coarse-to-fine planning for long-instruction following.|
|DexGraspVLA [57]|2025|Combined VLM planning with diffusion for robust dexterous grasping.|
|<br>HAMSTER [58]<br>|2025<br>|<br>Hierarchical VLA leveraging out-of-domain data for broad generalization.<br>|
|CoT-VLA [59]<br>|2025|Implemented visual chain-of-thought reasoning with predictive goals.<br>|
|Gemini Robotics [60]|2025|Built Gemini 2.0-based platform for robust multi-task embodied reasoning.|
|<br>CognitiveDrone [61]<br>|2025<br>|<br>Developed cognitive UAV VLA achieving high success on aerial benchmark.<br>|
|_π_0.5 [62]<br>InSpire [63]|2025<br>2025|Trained on heterogeneous robots for open-world generalization.<br>Introduced spatial reasoning prompts to reduce spurious correlations.|
|<br>**(C) Autoregressive Trajec**|**tory Generat**|<br>**ion and Visual Alignment Modeling**|
|LATTE [64]<br>VIMA [65]|2022<br>2023|Mapped natural language to motion trajectories with a Transformer decoder.<br>Unified multimodal tokens for lanuae vision and actions with stron zero-shot eneralization|
|<br>InstructRL [66]<br>|2023|i    gg, ,    g  g.<br>Used joint vision–language encoders with policy Transformer for better alignment.<br>|
|CrossFormer [67]|2024|Scalable Transformer policy handling multi-embodiment data for generalization.|
|<br>GR-1 [68]<br>|2024<br>|<br>Unified video and action tokens for temporal modeling via video pretraining transfer.<br>|
|GR-2 [69]<br>|2024<br>|Extended GR-1 with web-scale video–language supervision for zero-shot manipulation.<br>|
|OpenVLA [21]|2024|Released 7B open-source VLA trained on 970k trajectories, surpassing RT-2-X.|
|<br>Bi-VLA [70]<br>RbNVLA71|2024<br>2024|<br>Employed dual-arm predictors for coordinated bimanual manipulation.<br>Ahid hihii il i ih VLA lii i dil i|
|oourse- []<br>Moto [72]|2025|ceve g-precson surgca graspng wt  poces n meca settngs.<br>Bridged video pretraining and execution with motion language tokens.|
|OpenDriveVLA [73]|2025|<br>Aligned 2D/3D perception into a unified semantic space for driving trajectories.|
|<br>GraspVLA [74]<br>RaceVLA [75]|2025<br>2025|i<br>Pretrained GPT-style decoder with GraspVerse for real-world grasp transfer.<br>Generated vision–language trajectories for dynamic drone racing control.|
|VTLA [76]|2025|Fused vision–tactile input with preference optimization for_>_90% unseen success.|
|<br>PointVLA [77]<br>|2025<br>|<br>Injected point clouds into pretrained VLAs for lightweight 3D reasoning.<br>|
|WorldVLA [31]<br>TraceVLA [78]|2025<br>2025|Mitigated autoregressive error propagation with joint vision–action modeling.<br>Used visual trace prompting to capture cues in long-horizon tasks.|
|<br>Interleave-VLA [79]|2025|<br>Suorted interleaved imae–text inuts to boost zero-shot maniulation|
|<br>MoManipVLA [80]|2025|pp  g p    p.<br>Unified base–arm trajectory alignment for mobile manipulation transfer.|
|**(D) Structural Optimizati**|**on and Effic**|**iient Inference Mechanisms in Autoregressive VLA**|
|HiP [81]|2023|Introduced hierarchical planning with token prediction for long-horizon manipulation.|
|Actra [82]<br>DR-VLA [83]|2024<br>2024|Optimized Transformer with trajectory attention and learnable queries to cut overhead.<br>Mlti-xit rhittr nblin rl xit t rd ltn|
|ee<br>FAST [22]|2025|ue acecue eag eay es o euce aecy.<br>Generated variable-length action tokens for efficient long-horizon execution.|
|SpatialVLA [84]<br>VLA-Cache [85]|2025<br>2025|Enhanced geometric perception using voxel grids and spatial attention.<br>Reused Transformer ke–value states with adative cachin for efficienc|
|<br>Beyond Sight [86]<br>|2025|y   p g  iy.<br>Language-guided perception adaptation improved multimodal sensor fusion.<br>|
|MoLe-VLA [87]|2025|Mixture-of-experts router enabled dynamic layer skipping, reducing cost 40%.|
|<br>PD-VLA [88]<br>|2025<br>|<br>Applied parallel fixed-point decoding to accelerate inference without retraining.<br>|
|BitVLA [89]<br>GR-MG [90]|2025<br>2025|Used 1-bit quantization, cutting memory to 30% while preserving performance.<br>Leveraged diffusion-generated goals for semi-supervised autoregressive learning.|
|<br>LoHoVLA [91]<br>|2025<br>|<br>Unified hierarchical control for ultra-long-horizon closed-loop tasks.<br>|
|OTTER [92]<br>ChatVLA [93]|2025<br>2025|Injected language into vision encoding with TAVE for stronger alignment.<br>Unified architecture with expert routing and phased alignment for scalability.|


6 

systems, enabling reasoning-driven control for long-horizon and compositional tasks. This section reviews LLM-based reasoning evolution from semantic intermediaries to hierarchical planners and platform-level orchestration. 

To inject reasoning into VLA models, Inner Monologue [47], [48] introduced self-talk-style reasoning with preaction planning and post-action reflection. Extensions like Prompt-to-Walk, RoboFlamingo, and RoboMM [38], [49], [94] demonstrated linguistic representations across locomotion and manipulation tasks. 

Subsequent approaches enhanced adaptability through feedback and hierarchical planning. Interactive Language [95] enabled real-time correction, Open-Ended Instructable Agents [96] utilized episodic memory, and Hi Robot [56] adopted hierarchical planning for long instructions. MissionGPT, Mobility VLA, and NORA [42], [52], [97] emphasized lightweight deployment and dialogue-driven adaptability. 

Hierarchical frameworks combined semantic planning with controllers for dexterous manipulation [98], [99], [100], [101]. InSpire, From Foresight to Forethought, and CoT-VLA [59], [63], [102] emphasized runtime stability and chain-ofthought mechanisms. 

Autoregression-based reasoning architecture commonly patches the input to the sequence and utilizes those tokens for further reasoning. These models can process input of various lengths,and the strong ability of in-context learning enables them to process different modalities under aunified structure [103]. UAV-specific systems, such as CognitiveDrone and UAV-VLA [53], [61], highlighted aerial navigation and satellite-informed planning. Additional contributions, including OneTwoVLA [43], addressed adaptive reasoning–action switching and abstraction of heterogeneous control spaces. 

In contrast to the aforementioned methods, efforts toward systematization and platformization have begun to consolidate these advances. Gemini Robotics [60] and Agentic Robot [104] positioned LLMs as central orchestrators of embodied pipelines, while _π_ 0.5 and fast [22], [62] targeted open-world scalability and efficient tokenization. Supporting works, including VLA Model–Expert Collaboration and LLaRA [50], [105], explored collaborative mechanisms and auxiliary tasks for improved VLM-to-VLA transfer. LLMbased reasoning in VLA has progressed from semantic intermediaries to interactive and hierarchical planning, crossmodal extensions, and integrated platforms. 

Although LLM-based reasoning in VLA has evolved from semantic intermediaries to interactive and hierarchical planners, cross-modal extensions, and integrated platforms. Nonetheless, persistent challenges remain, including hallucination control, multimodal alignment, reasoning stability, and real-time safety. Table 1(B) summarizes representative studies and their contributions. 

### _3.1.3 Autoregressive Trajectory Generation and Visual Alignment Modeling_ 

Autoregressive trajectory modeling strengthens perceptionaction mapping while ensuring vision-language semantic alignment. These models decode motion trajectories or control tokens conditioned on multimodal observations, offer- 

ing unified mechanisms for grounded instruction following and action execution [106], [107], [108]. 

Early work such as LATTE [64] showed the feasibility of mapping language directly to trajectories, inspiring multimodal extensions. With large-scale pretraining, VIMA [65] and InstructRL [66] demonstrated that joint tokenization of language, vision, and action supports strong cross-task generalization, though often only in simulation. Meanwhile, MOO [109] and GPT-based approaches [110] leveraged pretrained vision–language backbones for open-world generalization and lightweight trajectory generation, suggesting semantic priors can reduce reliance on robot-specific pretraining. 

A second line of work explores video prediction and world modeling. GR-1/2 [68], [69] transferred video generation pretraining to robotics, while CronusVLA [111] and WorldVLA [31] improved temporal consistency. TraceVLA [78] and Uni-NaVid [112] further introduced long-horizon prompting, collectively shifting from shorthorizon decoding to predictive environment modeling. 

Autoregression-based methods have been adapted to diverse robot embodiments, from quadruped locomotion to bimanual manipulation, demonstrating the flexibility of Vision-Language-Action frameworks [70], [113], [114]. Large-scale efforts such as OpenVLA [21], [115] further highlight cross-platform generalization and efficient adaptation, while latent motion token approaches [72], [116] point toward lightweight pretraining strategies. 

Beyond manipulation, autoregressive trajectory generation has extended to autonomous driving, where recent models achieve closed-loop control by aligning vision and language with trajectory prediction, often without HD maps or LiDAR [117], [118], [119]. Similar principles have been applied to mobile manipulation and UAV planning [75], [80], underscoring the versatility of these methods across robotic platforms. 

Researchers have also extended autoregressive frameworks toward fine-grained sensing and richer modalities. Recent models emphasize precise manipulation with robust pretraining pipelines [74], [120], [121], [122], [123], while tactile–language–action integration [76], [124] enables contactrich interaction. Parallel efforts exploit 3D/4D perception to embed spatial structure into autoregressive decoding [77], [125], [126], further broadening the multimodal landscape. 

Autoregression-based trajectory generation has progressed from direct language-to-trajectory mapping toward a broad ecosystem that spans multimodal pretraining, video-driven world modeling, embodiment-specific architectures, and cross-modal sensing (see Table 1 (C)). These advances showcase the scalability and versatility of autoregression as a unifying mechanism for VLA. Nonetheless, challenges remain in long-horizon stability, semantic grounding under noisy inputs, and efficient deployment on physical robots. Future work should prioritize robust closed-loop integration between predictive modeling and low-level control, and explore synergies between autoregressive policies and higher-level reasoning modules such as LLM planners, moving closer to reliable, general-purpose embodied intelligence. 

7 

### _3.1.4 Structural Optimization and Efficient Inference Mechanisms in Autoregressive VLA_ 

In autoregressive VLA research, structural optimization and efficient inference are critical for enabling scalable deployment and real-time control. Beyond accuracy, the central challenge is how to reduce computational redundancy, shorten inference latency, and maintain robustness across diverse robotic settings. 

One important direction is hierarchical and modular optimization. Early work such as HiP [81] demonstrated that decomposing tasks into symbolic planning, video prediction, and action execution enables long-horizon reasoning with autoregressive models. Follow-up designs—ranging from efficient observation backbones and action chunking to trajectory-aware attention and frequency separation [82], [127], [128]—further showed that modular structures can significantly reduce computation while preserving generalization. 

Another line of work emphasizes dynamic and adaptive inference. Frameworks like DeeR-VLA [83] enable early termination of decoding based on task complexity, while token-efficient designs such as FAST [22] compress long action sequences into variable-length tokens. Together, these approaches show how adaptive computation can improve real-time responsiveness with minimal loss in accuracy. 

A third category emphasizes lightweight compression and parallelization. Quantization and layer-skipping methods [87], [89] cut precision and dynamically activate only subsets of layers, significantly reducing computation. In parallel, decoding and redundancy-reduction strategies [88], [129] accelerate inference without retraining, highlighting how architectural compression complements adaptive inference. 

Compression and parallelization methods span quantization and layer-skipping [87], [89], which substantially reduce computation, as well as parallel decoding and redundancy-reduction strategies [88], [129], which accelerate inference without retraining. 

Efficiency has also been pursued through sensor fusion and temporal reuse. Domain-specific optimizations such as voxelized spatial modeling [84], adaptive key–value caching [85], and perception adaptation [86] reduce redundant computation while improving robustness. 

Notably, several works integrate efficiency with multimodal reasoning. OTTER [92] injects language-awareness into vision encoding, while ChatVLA [93] employs staged coupling with mixture-of-experts routing. Other advances—ranging from diffusion-based goal generation [90], quantization [89], to hierarchical feedback for ultra-long horizons [91]—illustrate how architectural refinements can balance efficiency and scalability. 

In summary, structural optimization and efficient inference in autoregressive VLA models have evolved from early hierarchical decomposition strategies to adaptive computation, lightweight compression, caching, and multimodalaware integration (see Table 1(D)). These methods address long-sequence dependency and computational redundancy, delivering notable gains in both benchmarks and real-world deployment. Looking forward, future research should pursue hardware-aware co-optimization, intelligent scheduling, 

and robust safety mechanisms to ensure scalable and reliable progress toward general-purpose embodied intelligence. 

### _3.1.5 Discussion_ 

**Innovations** Autoregression-based models have driven major innovations in Vision-Language-Action research by unifying multimodal perception, language reasoning, and sequential action generation within scalable Transformer architectures. They support generalist agents capable of cross-task generalization, enable semantic planning through LLM integration, and extend trajectory generation to longhorizon and multimodal settings, structural optimizations such as token compression, parallel decoding, and quantization improve efficiency for real-world deployment. 

**Limitations** Autoregressive decoding introduces error accumulation and latency, multimodal alignment can be brittle under noisy or incomplete inputs, and scaling large models requires prohibitive computational resources and data. Moreover, reasoning-driven approaches still face challenges of hallucination, stability, and interpretability, while efficiency mechanisms often trade off accuracy or generality. Addressing these issues will require tighter coupling between reasoning and control, robustness under real-world uncertainty, and hardware-aware optimization strategies to balance scalability with practical deployment. 

### **3.2 Diffusion-based Models in Vision-Language-Action Research** 

Diffusion (including flow matching, VAE, etc.) models have emerged as a transformative paradigm in generative artificial intelligence, showing remarkable potential within Vision-Language-Action (VLA) frameworks for embodied intelligence. In this subsection, we review the evolution of diffusion models in VLA systems, focusing on three critical dimensions. Representative works are summarized in Table 2. 

### _3.2.1 Diffusion Generalist VLA Methodologies_ 

Diffusion models integration into VLA systems shifts robotic action generation from deterministic regression to probabilistic generative policies. By formulating action generation as conditional denoising, diffusion-based methods naturally model diverse action distributions, enabling multiple valid trajectories from identical observations [7], [136]. 

A key trajectory has been the incorporation of richer representational structures. Geometry-aware methods embed SE(3) constraints into diffusion, extending beyond Euclidean spaces to jointly optimize grasping and motion in 3D environments [130], [133], thereby ensuring physically consistent actions. In parallel, reinterpreting policy learning as video generation [131], [134] leverages the temporal richness of video for long-horizon planning and cross-modal grounding. 

Scaling efforts like RDT-1B [135] demonstrate trajectorylevel diffusion with temporal and environmental conditioning for zero-shot generalization in bimanual manipulation. Temporal coherence is addressed through unified velocity fields across timesteps [136] or historical conditioning with efficient caching for real-time deployment [137]. 

8 

TABLE 2: Representative works on Diffusion-based Models. 

|**Method / Model**|**Year**|**Key Innovation in Diffusion-based Models**|
|---|---|---|
|**(A) Diffusion Generalist VL**|**A Method**|**ologies**|
|SE(3)-DiffusionFields [130]<br>UPDP [131]<br>StructDiffusion [132]<br>Diffusion Policy [7]<br>3D Diffuser Actor [133]<br>AVDC [134]<br>RDT-1B [135]<br>TUDP [136]|2023<br>2023<br>2023<br>2024<br>2024<br>2024<br>2025<br>2025|Extended diffusion to SE(3) poses, learning smooth costs for grasp and motion planning.<br>Framed decision-making as video generation with images as interfaces and language guidance.<br>Combined diffusion and object-centric transformers for language-guided 3D structure creation.<br>Modeled actions as conditional diffusion, outperforming behavioral cloning.<br>Embedded 3D scenes with conditional diffusion for trajectory generation.<br>Learned visuomotor policies from video via optical flow and motion reconstruction.<br>Large-scale diffusion model for bimanual manipulation with temporal conditioning.<br>Unified diffusion across time with velocity fields and action discrimination.|
|CDP [137]|2025|i      i<br>Improved coherence via historical action conditioning and caching mechanisms.|
|DD VLA [138]<br>TRETL [139]|2025<br>2025|Modeled discretized action chunks with discrete diffusion and cross-entropy training.<br>Recombined task behaviors by averaging hidden states across demonstrated trajectories.|
|**(B) Diffusion-based Multim**|**odal Arch**|**itectural Fusion**|
|SuSIE [140]<br>M-DiT [141]|2023<br>2024|Pre-trained image-edit diffusion models for zero-shot robot manipulation via goal image generation.<br>Unified multimodal tokens enabling flexible language–image–position goal conditioning.|
|CogACT [142]|2024|i    l<br>Introduced cognition modules with semantic graphs linking perception and behavior.|
|PERIA [143]<br>|2024|Jointly fine-tuned MLLMs and image editing models for reasoning and sub-goal planning.<br>|
|Chain-of-Affordance [144]|2024|Parsed tasks into sequential affordance sub-goals with explicit perception–action pairs.|
|<br>_π_0 [2]<br>|2024<br>|<br>Encoded video and language as latent tokens in observe–understand–execute loops.<br>|
|Track2Act [145]|2024|Leveraged web videos to predict point tracks and map them to robot actions.|
|<br>Dita [146]|2025|<br>Scalable diffusion Transformer denoising continuous actions directly.|
|Diffusion-VLA [1]|2025|Integrated self-generated reasoning with diffusion policies via symbolic intermediates.|
|ForceVLA [147]|2025|Incorporated 6-axis force sensing with force-aware MoE fusion for real-time control.|
|**(C) Application Optimizati**|**on and De**|**ployment in Diffusion-Based VLA**|
|NoMaD [148]|2023|Unifies goal-directed navigation and oal-agnostic exploration in diffusion policy.|
|<br>TinyVLA [149]|2025|i<br>Uses LoRA fine-tuning with only 5% trainable parameters, effectively reducing training costs.|
|<br>SmolVLA [150]|2025|i<br>Deploys compact VLAs on consumer hardware with async inference.|
|VQ-VLA [151]|2025|<br>Employs vector-quantized tokenizers to reduce sim-to-real gaps.|
|DexVLG [152]<br>|2025<br>|Trains large-scale grasp model for dexterous hand grasping on DexGraspNet for zero-shot dexterity.<br>|
|AC-DiT [153]|2025|Adapts diffusion Transformer with multimodal mobility conditioning.|
|<br>DexVLA [154]|2025|<br>Applies morphology curriculum learning for cross-robot adaptation.|
|<br>MinD [155]|2025|<br>Combines video imagination with high-frequency diffusion policies.|
|Hume [156]|2025|<br>Integrates dual-system value-guided reasoning and fast denoising.|
|TriVLA [157]|2025|<br>Operates triple-system VLA with 36Hz dynamics and reasoning layers.|
|BYOVLA [158]|2025|Adds runtime interventions to enhance robustness without retraining.|
|DreamVLA [159]|2025|Employs dynamic self-reflective loops with CoT, error tokens, and expert layers.|
|GEVRM [160]|2025|l<br>Uses IMC principles with text-guided video generation for robustness.|
|DriveMoE [161]|2025|<br>Deploys scene/action-specialized Mixture-of-experts architectures for autonomous driving.|
|DreamGen [162]|2025|<br>Generates neural trajectories enabling humanoids to learn novel tasks.|
|EnerVerse [163]|2025|Predicts embodied futures with multi-view autoreressive video diffusion|
|<br>VidBot [164]|2025|g  .<br>Reconstructs 3D affordances from monocular videos with depth priors.|
|<br>OFT [115]|2025|<br>Optimizes fine-tuning via parallel decoding and chunked actions.|
|<br>TrackVLA [165]|2025|i<br>Uses shared LLM heads and diffusion for embodied visual tracking.|
|<br>FP3 [166]|2025|<br>Builds large-scale 3D foundation diffusion policy for manipulation.|
|GR00T N1 [167]|2025|<br>Provides humanoid foundation model with multimodal Transformer control.|
|ObjectVLA [168]|2025|Enables open-world object manipulation without human demos|
|<br>SwitchVLA [169]|2025|.<br>Models execution-aware task switching from state–context signals.|
|<br>A0 [170]|2025|<br>An Affordance-aware model decomposes tasks into spatial affordances and low-level execution.|
|LangToMo [171]|2025|<br>Forecasts pixel motion as intermediate reasoning for actions.|
|<br>Evo-0 [172]|2025|<br>Injects 3D geometry features via visual geometry foundation modules.|


These advances mark three transitions: deterministic to probabilistic generation, Euclidean to geometry-aware representations, and supervised to self-supervised paradigms. This reframing as generative modeling enables multi-task generalization, few-shot adaptation, and natural language interfaces. Table 2(A) summarizes architectural choices and training strategies. However, temporal coherence remains fragile under dynamic environmental shifts. 

### _3.2.2 Diffusion-Based Multimodal Architectural Fusion_ 

The integration of Transformers in VLA systems drives unified modeling of vision, language, and action within single frameworks, moving beyond modular pipelines to capture intricate interdependencies in embodied intelligence. 

Within this shift, combining Transformers with diffusion models has proven especially transformative, as attention mechanisms naturally complement generative modeling. Large-scale frameworks such as Dita [146] and Diffusion Transformer Policy [173] show that scaling attention-based architectures beyond small action heads substantially improves continuous action modeling, with self-attention inductive biases aligning well with the compositionality of robotic behaviors. 

The central challenge lies not in scaling architectures but in fusing heterogeneous modalities while preserving their distinct properties. Vision, language, and proprioception differ in temporal granularity, semantics, and processing needs—creating opportunities for richer context but also 

9 

risks of diluting modality-specific strengths. To address this, token-space alignment strategies such as M-DiT [141] map diverse signals into unified representations, enabling conditional diffusion Transformers to flexibly support arbitrary combinations of goals and observations, a key step toward general-purpose robotics. 

Domain-specific designs like ForceVLA [147] treat force sensing as a first-class modality, using force-aware mixtureof-experts to integrate tactile feedback with visual-language embeddings, significantly improving contact-rich manipulation. 

Recent advances integrate explicit reasoning within diffusion policies. Diffusion-VLA [1] introduces Self-Generated Reasoning modules producing symbolic representations, while CogACT [142] leverages semantic scene graphs, unifying perception, reasoning, and control. 

Pre-trained model leveraging includes repurposing image editing models for zero-shot manipulation [140] and joint fine-tuning strategies like PERIA [143]. Structured decomposition through Chain-of-Affordance [144] and flowgraph approaches like _π_ 0 [2] outperform end-to-end methods in complex environments. 

Taken together, these developments (Table 2(B)) reveal a field in transition—from monolithic architectural adaptations toward cognitively inspired frameworks that integrate structured reasoning, multi-sensory inputs, and explicit knowledge representation. This shift signals a move beyond purely data-driven end-to-end learning toward more interpretable and generalizable designs, though progress remains constrained by high computational demands and limited dataset diversity. 

### _3.2.3 Application Optimization and Deployment in Diffusion-Based VLA_ 

The transition from laboratory prototypes to real-world deployment remains one of the most formidable challenges for diffusion-based Vision-Language-Action (VLA) systems. Meeting this challenge requires advances across three interconnected fronts: efficiency, adaptability, and robustness. Recent work demonstrates that rather than scaling model size indiscriminately, progress now hinges on principled optimization strategies, cognitive-inspired architectures, and practical deployment mechanisms. 

Efficiency optimization has become a central theme. While diffusion models are resource-intensive, lightweight designs such as TinyVLA and SmolVLA [149], [150] show that pre-trained backbones with parameter-efficient tuning (e.g., LoRA) can cut training costs to single-GPU scales without sacrificing performance. Complementary strategies like VQ-VLA [151], which employs vector-quantized action tokenizers to narrow the sim-to-real gap, illustrate how efficiency gains can align with robustness. Collectively, these works reflect a paradigm shift toward “intelligent sparsity,” prioritizing performance-per-computation over brute-force scaling. 

At the same time, task adaptability has become a defining feature of advanced VLA systems. In dexterous manipulation, large-scale curated datasets such as DexVLG [152] enable strong zero-shot performance, while in mobile manipulation, frameworks like AC-DiT [153] unify perception and actuation through mobility-to-body conditioning. Overall, 

the trend is toward balancing general-purpose architectures with deep domain specialization, embedding task-specific inductive biases while retaining broad multimodal capabilities. 

Architectural innovation represents the next frontier. Dualand triple-system designs, such as MinD and TriVLA [155], [157], demonstrate how cognitive principles can be operationalized in robotics. MinD integrates low-frequency video prediction for strategic planning with high-frequency diffusion policies for reactive control, while TriVLA explicitly separates vision language reasoning, dynamics perception, and policy learning into coordinated modules. Operating at interactive frequencies (e.g., 36Hz), these cognitively inspired architectures not only improve task performance but also enhance system interpretability and maintainability—key requirements for industrial deployment. 

Beyond efficiency and design, runtime robustness has emerged as a decisive factor for real-world adoption. Lightweight intervention strategies like BYOVLA [158] dynamically edit irrelevant visual regions at inference time without fine-tuning, mitigating robustness failures in unpredictable environments. Meanwhile, self-reflective architectures such as DreamVLA [159] introduce hierarchical error handling with reasoning-enhanced modules, error-aware layers, and expert adapters. Together, these strategies illustrate a shift toward “defensive AI,” emphasizing resilience and reliability as much as raw task performance. 

The application landscape of diffusion-based VLA systems has rapidly expanded. In autonomous driving, DriveMoE [161] employs scene- and skill-specialized mixtures of experts to achieve state-of-the-art closed-loop control, while in humanoid robotics, DreamGen [162] leverages video world models to generalize from single-task teleoperation to dozens of novel behaviors. EnerVerse [163] and VidBot [164] extend this paradigm by predicting embodied futures through autoregressive video diffusion and affordance learning, underscoring the potential of video-centric world models for planning. These advances highlight a transition from task-specific prototypes to versatile, domain-spanning systems. 

Ambitious efforts toward foundation models further underscore the field’s trajectory. FP3 [166] introduces a largescale 3D policy model pre-trained on 60,000 trajectories, while GR00T N1 [167] integrates multimodal Transformer architectures into a humanoid foundation system. Like large language models in NLP, these approaches aim to provide general-purpose priors for robotics, though they must also address safety, real-time control, and physical reliability—challenges less pronounced in text-based domains. 

Generalization and fine-tuning strategies remain critical for advancing diffusion-based VLA systems toward real-world deployment. Recent research highlights multiple complementary directions: ObjectVLA and SwitchVLA [168], [169] demonstrate the feasibility of open-world object manipulation and execution-aware task switching, emphasizing flexibility in dynamic environments. In parallel, approaches such as LangToMo and Evo0 [171], [172] introduce novel intermediate representations and geometry-aware plug-in modules, showing that structured perceptual priors can significantly enhance adaptabil- 

10 

ity across tasks. On the optimization front, systematic finetuning frameworks like OFT [115] integrate techniques including parallel decoding, action chunking, and continuous representation learning, moving the field from exploratory proofs-of-concept toward an engineering discipline. 

Collectively, these strategies illustrate that achieving robust generalization requires architectural innovation, efficient model design, adaptive task specialization, cognitively inspired architectures, and robust runtime strategies, as summarized in Table 2 (C). Nonetheless, challenges persist: safety-critical scenarios is still underdeveloped. Bridging these gaps is essential to transition from experimental prototypes to reliable, general-purpose robotic systems. 

The application of diffusion models in VLA systems is evolving toward greater efficiency, robustness, and universality. From foundational action generation modeling to complex multimodal fusion and practical deployment optimization, a comprehensive technological framework has emerged. There are still issues need to be solved, future development trends will continue to address key challenges including model efficiency enhancement, generalization capability improvement, and practical deployment performance optimization. 

### _3.2.4 Discussion_ 

**Innovations** Diffusion-based models fundamentally reframing robotic control as a generative modeling problem. They enable probabilistic action generation, multimodal architectural fusion, and cognitively inspired deployment strategies, advancing beyond deterministic and modular pipelines. These approaches improve trajectory diversity, geometric grounding, and reasoning integration. Besides, efficiencyfocused designs such as TinyVLA and SmolVLA make realworld deployment increasingly feasible. 

**Limitations** However, due to the fact that temporal coherence in dynamic environments is still fragile, largescale diffusion models demand prohibitive computational resources and datasets, and safety-critical reliability under adversarial or uncertain conditions is underexplored. Furthermore, while multimodal fusion enriches representation, it risks diluting modality-specific strengths, and domain-specialized adaptations may reduce transferability. Addressing these challenges will require more efficient and robust training paradigms, richer safety-aware evaluation standards, and closer alignment between foundation-scale modeling and practical deployment constraints. 

### **3.3 Reinforcement-based Fine-Tune Models in VisionLanguage-Action Research** 

### _3.3.1 Reinforcement-based Fine-Tune Strategies in VLA Research_ 

Reinforcement-based Vision-Language-Action (VLA) methods integrate vision–language foundation models with reinforcement learning to enhance perception, reasoning, and decision-making. By leveraging visual and linguistic inputs, these methods generate context-aware actions within interactive and dynamic environments. They have emerged as a critical research direction for advancing autonomous driving, robotics, and broader embodied AI systems. Recent advances demonstrate that reinforcement-based VLA 

approaches can incorporate human feedback, adapt to novel tasks, and outperform purely supervised paradigms. The progression of these efforts is summarized in Table 3. 

Earlier methods improved robot manipulation skills using large-scale human video datasets or robot manipulation datasets by introducing reinforcement reward strategies [174], [175], [176], [183]. These methods aimed to investigate the promptability of pre-trained Vision-Language Models (VLMs) in reinforcement learning, showing that even frozen models can support efficient downstream policy training through prompt embedding learning. VIP [174] derives a self-supervised goal-conditioned value function independent of actions, generating smooth embeddings that implicitly evaluate value via embedding distance. 

Similar to other reinforcement fine-tuning approaches, some methods use language and images to jointly generate reward proxies and obtain cross-modal state language representations through self-supervised contrastive training. These methods emphasize the transferability of rewardaware representations, enabling applications in robot learning under sparse rewards or complex language instructions [175], [183], [192]. 

Furthermore, some approaches primarily optimize reward functions or loss functions to improve policy learning [177], [180]. These methods use language models as intermediaries for reward function design, learning reward proxies through human demonstrations and VLM semantic mapping. This approach simplifies reward engineering, while generalization and interpretability can be further optimized with reinforcement learning from human feedback (RLHF). For example, Elemental demonstrates the ability to rapidly customize task requirements and efficiently learn from limited samples in complex manipulation tasks. SafeVLA [182] explores VLA from a safety perspective, addressing the risks of deploying VLAs in open environments. It proposes a constrained-learning alignment mechanism to prevent highrisk behaviors while maintaining task performance. The method incorporates a safety critic network into the VLA architecture to estimate risk levels and employs the Constrained Policy Optimization (CPO) framework to maximize policy rewards while ensuring that security loss remains below a predefined threshold. SafeVLA significantly reduces risk events in multitask testing—including manipulation, navigation, and handling—particularly in scenarios where ambiguous natural language instructions increase policy uncertainty, thereby demonstrating superior safety and stability. This work provides an essential safety mechanism for deploying VLA models in real-world applications. 

Unlike the aforementioned robot arm VLA models, researchers have also investigated VLA frameworks for quadruped and humanoid robots. Using natural language navigation instructions, these robots emphasize trajectory prediction, target description, obstacle avoidance, and related tasks. For example, NaVILA [181] fine-tunes a VLA model with a single-stage reinforcement learning (RL) policy to output continuous control commands, enabling adaptation to complex terrain and dynamically changing language instructions. In contrast, MoRE [186] integrates multiple low-rank adaptive modules as distinct experts into a dense multimodal large language model (MLLM), forming a sparsely activated hybrid expert model that is subsequently 

11 

TABLE 3: Evolution of Reinforcement-based Models in VLA Research and Key Innovations. 

|**Method**|**Year**|**VLA Innovation with Reinforcement Learning**|
|---|---|---|
|VIP [174]<br>|2023<br>|Generates dense reward functions from visual pretraining for unseen tasks.<br>|
|LIV [175]<br>|2023<br>|Learns joint vision–language rewards from action-free videos with text.<br>|
|PR2L [176]<br>|2024<br>|Leverages VLM world knowledge with RL for robot manipulation.<br>|
|ALGAE [177]<br>|2024|Introduces language-guided abstractions to explain RL-driven behavior.<br>|
|GRAPE [178]<br>|2024|Aligns VLAs at trajectory level, modeling rewards from successes and failures.<br>i|
|RLDG [179]<br>|2024<br>|Uses RL to generate training data for generalist policy finetuning.<br>|
|ELEMENTAL [180]<br>|2025<br>|Learns reward proxies from demonstrations via VLM-based semantic mapping.<br>|
|NaVILA [181]<br>|2025<br>|Integrates multimodal VLA with RL for quadruped navigation on complex terrain.<br>|
|SafeVLA [182]<br>|2025|Constrains RL alignment to prevent risky actions while maintaining performance.<br>|
|iRe-VLA [183]<br>|2025|Combines SFT stability with RL exploration to boost VLA capability.<br>|
|ReinboT [184]|2025|Enhances Robot GPT with RL to maximize rewards and data quality use.|
|ConRFT [185]|2025|Blends offline BC, Q-learning, and online consistency for safe efficient RL.<br>i|
|MoRE [186]<br>|2025|Scales quadruped VLAs with RL and mixed-quality dataset finetuning.<br>|
|SimpleVLA-RL [187]<br>|2025<br>|Trains from one trajectory using binary (0/1) rewards in online RL.<br>|
|LeVERB [188]<br>|2025|Couples VLA reasoning with RL dynamics for humanoid whole-body control.<br>|
|AutoVLA [189]<br>|2025<br>|Employs CoT reasoning with RL optimization for autonomous driving.<br>i|
|RPD [190]<br>|2025<br>|Distills student from VLA teacher using RL-based refinement.<br>|
|RLRC [191]<br>|2025|Compresses VLA via pruning, SFT+RL recovery, and quantization.<br>|
|VLA-RL [192]<br>|2025|Improves robustness with online RL and VLM-based reward modeling.|
|AutoDrive-R<sup>2 </sup>[193]|2025|Enhances autonomous driving with CoT reasoning and RL self-reflection.|
|ReWiND [194]|2025|Uses language-conditioned rewards for offline RL from small demos.|
|Embodied-R1 [195]|2025|Trains with reinforced fine-tuning and multi-task reward curriculum.|
|IRL-VLA [196]<br>|2025|Applies inverse RL in a reward world model within a VLA framework.<br>|
|ThinkAct [197]|2025|Bridges reasoning and execution with reinforced visual latent planning.|


trained as a Q-function using reinforcement learning objectives. LeVERB [188] extends this line of research by proposing a hierarchical VLA framework for whole-body control (WBC) of humanoid robots. Similar to NaVILA, LeVERB couples vision–language processing with dynamicslevel action processing, where reinforcement learning strategies translate potential vocabularies into high-frequency dynamic control commands, enabling complex whole-body task execution. 

Offline reinforcement learning has proven effective for deriving robust policy models from mixed-quality datasets. ReinboT [184] exemplifies this approach by applying the principle of maximizing cumulative rewards via RL. It enhances understanding of data quality distribution by predicting dense rewards that capture subtle differences in operational tasks, thereby enabling robots to generate more robust decision actions guided by long-term benefits. Online reinforcement learning methods have also been extensively explored in the VLA domain. For instance, SimpleVLA-RL [187] employs only a single trajectory and a binary outcomelevel reward (0/1) to train a VLA model. This method avoids reliance on dense supervision or large-scale behavior cloning datasets, but achieves performance comparable to full trajectory supervised fine-tuning (SFT) with simulating rule-based reward signals in the environment. Recognizing the limitations of using only offline or online strategies, ConRFT [185] introduces a hybrid strategy that combines both. Its offline policy incorporates behavior cloning with Q- learning to extract policies from limited demonstrations and stabilize value estimation, while its online policy introduces consistency goals and artificial intervention mechanisms to steadily improve policy performance, ensuring safe exploration and sample efficiency throughout training. 

In the autonomous driving domain, VLA models also leverage reinforcement learning to enhance driving performance in previously unseen scenarios [193]. AutoVLA [189] exemplifies this direction by introducing an autore- 

gressive generation model equipped with reasoning and action capabilities. It first processes visual inputs and language instructions, then applies reasoning fine-tuning to produce discrete, feasible actions that can be reconstructed into continuous trajectories. This model employs two finetuning steps—Chain-of-Thought Reasoning and Group Relative Policy Optimization—achieving state-of-the-art performance. 

Notably, different from existing models that require enormous numbers of parameters, resulting in high computational and memory demands, some researchers have investigated efficiency strategies such as quantization, pruning, and knowledge distillation within reinforcement learning–based VLAs, often combined with algorithms such as Proximal Policy Optimization (PPO) [198]. For instance, RPD [190] distills a student model from a VLA teacher model to increase inference speed, while RLRC [191] introduces a novel compression framework composed of structured pruning, SFT- and RL-based performance recovery, and quantization. These approaches reduce memory usage and improve inference throughput while preserving the task success rate of the original VLA. 

### _3.3.2 Discussion_ 

**Innovations** Reinforcement-based VLA fine-tune strategies using visual and language signals to generate dense, transferable reward proxies, and combining offline behavior cloning with online reinforcement learning stabilizes policy optimization and enhances generalization. Safety-focused approaches also represent an important advancement by integrating constrained optimization to reduce high-risk actions in open-world deployment. Furthermore, extensions to quadruped, humanoid, and autonomous driving tasks highlight the versatility of reinforcement-driven VLA across diverse robotic embodiments. 

**Limitations** Despite these advances, reward of reinforcement-based VLA engineering often remains 

12 

indirect or noisy, leading to suboptimal learning; training stability can be hindered by the interplay between supervised fine-tuning and exploration; and scaling to highdimensional, real-world environments is computationally expensive, requiring substantial hardware and data resources. Additionally, while safety-aware strategies have been proposed, ensuring reliable generalization under ambiguous or adversarial instructions remains an open challenge. Addressing these issues will require more efficient reward representation, robust sample-efficient training paradigms, and richer evaluation benchmarks that capture both safety and reasoning capabilities. 

### **3.4 Other Advanced Researches** 

While autoregressive, diffusion, and reinforcement learning remain the foundational paradigms of VLA model design, the growing complexity and diversity of embodied tasks have spurred the development of approaches that transcend these boundaries. Current research progress can be organized into five key directions: hybrid architectures that integrate multiple generation paradigms, advanced multi-modal fusion for enhanced cross-modal and spatial understanding, specialized domain adaptations addressing task-specific challenges, foundation models and large-scale training paradigms that unify perception–reasoning–control at scale, and practical deployment strategies emphasizing efficiency, safety, and human–robot collaboration. The representative works are summarized in Table 4. 

### _3.4.1 Hybrid Architectures and Multi-Paradigm Integration_ 

As embodied manipulation tasks continue to grow in diversity and complexity, relying on a single generation paradigm (whether autoregressive, diffusion, or reinforcement learning) often proves inadequate. Hybrid architectures have thus emerged as a promising solution, strategically combining multiple paradigms to exploit their complementary strengths. The central objective of this approach is to integrate the smoothness and physical consistency of continuous action generation, the precision of discrete reasoning, and the adaptability needed for dynamic, real-world environments. In doing so, hybrid systems lay the groundwork for more capable and versatile VLA models. 

A representative example is HybridVLA [201], which unifies diffusion-based continuous trajectory generation with autoregressive token-level reasoning in a single 7Bparameter framework. This design leverages diffusion processes to produce smooth and physically coherent motion, while retaining the contextual inference capacity inherent in autoregressive models. The dual-system philosophy, inspired by cognitive science, has also been embraced in recent works. Fast-in-Slow [243] operationalizes Kahneman’s dual-process theory by embedding a low-latency execution module within a slower yet cognitively richer VLM backbone. This enables real-time responsiveness while preserving high-level reasoning. Similarly, RationalVLA [202] integrates vision–language reasoning with low-level manipulation policies through learnable latent embeddings, allowing the model to filter out infeasible commands and plan executable actions. 

Scaling hybrid designs has also shown considerable promise. Transformer-based Diffusion Policy [244] demonstrates that billion-parameter architectures can effectively combine diffusion processes with attention mechanisms, surpassing conventional U-Net designs by capturing richer contextual dependencies for trajectory modeling. This trend points toward the next generation of VLA systems that embed autoregressive Transformers within diffusion-based planners, achieving greater context-awareness alongside higher-quality motion generation. 

Beyond individual innovations, initiatives such as OpenHelix [203] are moving toward the systematization of hybrid VLA design. Through large-scale empirical evaluation, OpenHelix benchmarks alternative reasoning–execution integration strategies and provides open-source implementations alongside design guidelines. This shift signals a maturation of the field, fostering reproducibility and standardization in hybrid VLA development. The progression of these efforts is summarized in Table 4 (A), which outlines the key innovations driving hybrid VLA architectures. 

### _3.4.2 Advanced Multi-Modal Fusion and Spatial Understanding_ 

Achieving robust manipulation in complex environments requires more than straightforward cross-modal alignment; it calls for structured, task-aware fusion mechanisms capable of capturing fine-grained semantics and spatial relationships. Recent progress reflects a decisive shift away from early feature concatenation toward architectures that explicitly model geometry, affordances, and spatial constraints. These advances are propelling VLA models toward richer spatial grounding and more reliable action generation in unstructured, 3D-aware settings. 

Early efforts such as CLIPort [206] laid the foundation by disentangling visual processing into a “what” pathway for object identification and a “where” pathway for action localization. Leveraging CLIP-based representations, CLIPort generates pick-and-place heatmaps from paired image–language inputs, demonstrating the advantages of structured visual reasoning in language-conditioned manipulation. Building upon this foundation, subsequent research has emphasized 3D spatial understanding as a core competency. VoxPoser [245] introduces composable 3D value maps guided by large language models, dividing instruction interpretation into target understanding and action planning over voxelized scene representations. This modular design enhances generalization by cleanly separating semantic parsing from spatial reasoning. Similarly, 3D-VLA [207] integrates autoregressive language modeling with diffusionbased action prediction in a generative 3D world model, achieving coherent unification of perception, language, and action modalities. 

The challenge of multi-view perception has been tackled through unified representation learning. RoboUniView [246] employs multi-view Transformer modules to fuse temporal and spatial cues, substantially improving 3D scene geometry understanding compared to single-view baselines. In contrast, BridgeVLA [211] projects 3D observations into multiple 2D views and predicts actions within a unified 2D heatmap space, to highlight the efficiency of compact yet spatially grounded representations. To handle more 

13 

TABLE 4: Evolution of Hybrid Architectures and Specialized Approacher in Vision-Language-Action Research. 

|**Method**|**Year**|**Key Innovation in Hybrid and Specialized Architecture**|
|---|---|---|
|**(A) Hybrid Architectures a**|**nd Multi-P**|**aradigm Integration in VLA**|
|VRB [199]|2023|Learns affordances from human videos to enable complex robot interactions.|
|YAY Robot [200]<br>|2024<br>|Incorporates real-time natural language corrections into robot training.<br>|
|HybridVLA [201]|2025|Combines diffusion-based trajectories with autoregressive reasoning in one framework.|
|<br>RationalVLA [202]|2025|<br>Links high-level reasoning with low-level policies via latent embeddings.|
|OpenHelix [203]<br>|2025|<br>Provides standardized hybrid VLA designs through large-scale empirical studies.<br>|
|EgoVLA [204]<br>|2025<br>|Transfers human wrist/hand actions from video into robot actions.<br>|
|ACTLLM [205]|2025|Enforces action consistency to align perception with executable actions.|
|<br>TUDP [136]|2025|<br>Builds a time-unified diffusion policy with velocity and discrimination signals.|
|**(B) Advances in Multi-Mo**|**dal Fusion **|**and Spatial Understanding in VLA**|
|CLIPort [206]|2021|Separates “what” and “where” pathways with CLIP to generate action heatmaps.|
|3D-VLA [207]|2024|<br>Integrates perception, language, and action via generative 3D world modeling.|
|ReKep [208]<br>RoboPoint [209]<br>GMLLMA [210]|2024<br>2024<br>2024|Leverages relational keypoint graphs for precise spatio-temporal reasoning.<br>Predicts affordance maps as priors for downstream robotic planning.<br>Adapts MLLMs across embodiments and action spaces for grounded reasoning.|
|<br>BridgeVLA [211]|2025|<br>Aligns 3D observations to 2D heatmaps for sample-efficient action prediction.|
|GeoManip [212]<br>|2025<br>|Embeds geometric constraints to generalize actions without retraining.<br>|
|TTF-VLA [213]<br>|2025<br>|Fuses past and current visual tokens for training-free inference improvement.<br>|
|MemoryVLA [214]|2025|Builds working memory with perceptual and cognitive tokens plus a memory bank.|
|<br>**(C) Specialized Domain A**|**daptations **|<br>**and Applications in VLA**|
|GenAug [215]|2023|Uses semantic data augmentation to retarget behaviors with minimal real data.|
|<br>ROSIE [216]|2023|<br>Applies diffusion-based augmentation to enrich manipulation datasets.|
|CoVLA [217]|2024|<br>Builds a large VLA dataset for AD with paired instructions and trajectories.|
|LeVERB [188]<br>|2025<br>|Designs hierarchical policies for humanoid body control with robust sim-to-real transfer.<br>i|
|Helix [218]|2024|Unifies humanoid control for manipulation, locomotion, and collaboration.|
|<br>AutoRT [219]|2024|i<br>Orchestrates robot fleets via observe–reason–execute with foundation models.|
|MMiVLA [220]|2025|l<br>Adt fid-b VLA t bil bt thh it d ti tiiti|
|oanp<br>CubeRobot [221]<br>|2025<br>|aps ixease s o moe roos roug waypon an moon opmzaon.<br>Solves Rubik’s Cube with dual-loop VisionCoT and memory stream for high success.<br>|
|EAV-VLA [222]|2025|Develops adversarial patch attacks to destabilize or redirect robot actions.|
|<br>**(D) Foundation Models an**|**d Large-Sca**|<br>**le Training in VLA**|
|R3M [223]<br>|2022<br>|Learns compact visual representations via time-contrastive, video-language alignment.<br>|
|CACTI [224]|2023|Establishes a scalable four-stage pipeline for multi-task robot learning in simulation and real-world.|
|VC-1 [225]<br>DROID [226]<br>|2024<br>2025|<br>Studies pre-training data scale using 4,000+ hours of video with MAE-trained transformers.<br>Provides a large multimodal dataset of 150k+ trajectories across 1k+ objects and tasks.<br>l|
|ViSA-Flow [227]<br>|2025<br>|Pre-trains generative models on action flows from large-scale human–object interaction videos.<br>i|
|Fine-tuned GMPs [228]|2024|Benchmarks fine-tuning strategies for generalist policies across action spaces and signals.|
|<br>Rbt CT229|2025|i<br>Itd lihtiht hifthht i f bdid lii ith 3 ft if|
|oo o []||nrouces gweg can-o-oug reasonng or emoe poces w × aser nerence.|
|CAST [230]<br>|2025<br>|Enhances dataset diversity via counterfactual language and action generation.<br>i|
|RoboBrain [231]|2025|Proposes a unified embodied foundation model for perception, reasoning, and planning.|
|**(E) Deployment of VLA M**|**odels: Effic**|**iiency, Safety, and Human–Robot Collaboration**|
|EdgeVLA [232]|2024|Achieves 6× faster inference by removing dependencies and using compact LLMs.|
|DeeR-VLA [233]|2024|Cuts control cost with confidence-based early exit.|
|<br>Dual Process VLA [234]|2024|i<br>Splits reasoning and motor control across dual models for efficiency.|
|CEEDVLA235|2025|i<br>Sd  if 4 ith it ditillti d l it|
|- []||pees up nerence × w conssency saon an eary ex.|
|RoboMamba [236]|2024|Uses lightweight fusion for resource-limited deployment|
|<br>ReVLA [237]|2025|.<br>Adapts across visual domains to improve robustness.|
|<br>SAFE [238]|2025|<br>Proactively detects failures from internal VLA signals.|
|DyWA [239]|2025|<br>Models dynamics for adaptive control in uncertain environments.|
|CrayonRobo [240]<br>|2025<br>|Provides interpretable grounding via object-centric prompts.<br>|
|cVLA [241]|2025|Enhances sim-to-real transfer with 2D waypoint prediction.|
|RTC [242]|2025|<br>Supports smooth asynchronous execution of chunked policies.|


demanding scenarios, specialized spatial reasoning methods have emerged. ReKep [208] models spatio-temporal dependencies via relational keypoint graphs, excelling in precision-critical tasks. RoboPoint [209] predicts affordance maps that highlight feasible interaction regions, providing essential perception priors for downstream planning. GeoManip [212] integrates symbolic geometric constraints to guide action generation without requiring task-specific retraining, thereby achieving strong out-of-distribution generalization. 

Taken together, these works trace a clear trajectory: from early pathway-based 2D fusion to modular, 3D-aware archi- 

tectures that unify spatial grounding, semantic reasoning, and action generation. As VLA systems increasingly operate in unconstrained, real-world environments, the capacity to reason explicitly about geometry and affordances will remain a decisive factor for achieving robust and generalizable manipulation. Table 4 (B) summarizes this progression. 

### _3.4.3 Specialized Domain Adaptations and Applications_ 

The versatility of the VLA framework has enabled its expansion into specialized embodied domains that pose unique perceptual, reasoning, and control challenges. Such adaptations not only validate the generality of VLA principles 

14 

but also reveal the architectural and algorithmic modifications necessary for domain-specific success. From safetycritical robotics to fully digital interaction, these innovations demonstrate the adaptability of VLA pipelines to varied operational contexts. 

In safety-critical contexts such as autonomous driving, CoVLA [217] presents the first large-scale VLA dataset tailored for this domain, comprising approximately 50,000 paired language instructions and driving trajectory videos across diverse urban scenarios. This work illustrates how vision–language reasoning can be coupled with continuous control policies for navigation and hazard avoidance. 

The VLA paradigm has also been extended to graphical user interface (GUI) interaction, where perception-action loops operate in fully digital spaces. ShowUI [247] adopts a Vision-Language-Action pipeline for processing on-screen elements and generating control sequences for actions such as clicking, dragging, and form filling. Its strong performance on GUI-Bench underscores the applicability of VLA principles to non-physical manipulation tasks. 

Humanoid whole-body control has emerged as another challenging domain. LeVERB [188] proposes a hierarchical architecture in which a vision–language policy learns latent action vocabularies from kinematic demonstrations, while a reinforcement-learned control layer produces low-level dynamics commands. This two-level design bridges the semantic–control gap, enabling robust sim-to-real transfer across more than 150 tasks. Similarly, Helix [218] demonstrates that a single unified policy network can acquire diverse humanoid behaviors, from object manipulation to cross-robot collaboration, without task-specific retraining. 

Specialized adaptations also target large-scale robot orchestration and mobile manipulation. AutoRT [219] coordinates heterogeneous robot fleets via an observe–reason–execute framework that delegates strategic planning to VLMs such as PaLM-E and RT-2, while MoManipVLA [220] transfers fixed-base VLA models to mobile manipulation settings through waypoint-based trajectory generation and dual-layer motion optimization. 

Other domain-specific innovations incorporate physical reasoning or task-specialized cognitive structures. Physically grounded VLA [248] embed modules for estimating stability and contact points, improving manipulation under complex physical constraints. CubeRobot [221] applies a dual-loop VisionCoT and Memory Stream design to Rubik’s Cube solving, achieving near-perfect success rates in lowand medium-complexity tasks, and strong performance in high-difficulty scenarios. 

Overall, these domain-driven adaptations demonstrate the versatility of VLA architectures, as well as the importance of tailoring perception–reasoning–control pipelines to meet the specific demands of different operational contexts. They also reinforce the potential of VLA models as a unifying embodied intelligence framework spanning physical, digital, and hybrid environments. These specialized adaptations are summarized in Table 4 (C), which highlights the architectural and algorithmic innovations enabling VLA systems to succeed across diverse embodied domains. 

_3.4.4 Foundation Models and Large-Scale Training_ The rise of foundation models and large-scale training has reshaped the trajectory of VLA research, enabling unified perception–reasoning–control frameworks that generalize across tasks, embodiments, and environments. By leveraging massive multi-modal datasets and scalable architectures, this direction seeks to build generalist embodied agents with broad capabilities and efficient adaptation. Large-scale pretraining is increasingly becoming the backbone for nextgeneration VLA systems. Recent foundation models provide systematic researches in robotics, covering vision–language models, policy models, and cross-modal alignment techniques for manipulation, navigation, and planning, specifically focus on VLA architectures, organizing them into perception-aligned, policy-generative, and world-modelbased categories, while identifying a unifying trend toward tightly integrated multi-modal interfaces [249]. 

Large-scale datasets have been pivotal in enabling foundation-scale training. DROID [226] contributes over 150,000 trajectories spanning more than 1,000 objects and task scenarios, with multimodal annotations including RGBD, language, low-dimensional states, and environment labels. The General Flow framework [250] uses 3D point trajectories as transferable affordance representations, enabling cross-domain skill transfer from humans to robots. Similarly, ViSA-Flow [227] pre-trains generative models on semantic action flows extracted from large-scale human–object interaction videos, requiring minimal adaptation for downstream robot learning. 

Training strategies have also been extensively studied to improve efficiency and adaptability. Zhang et al. [228] analyze fine-tuning factors—including action space, policy head design, and supervision signals—through 2,500 rollout experiments, offering practical guidelines for adapting foundation-scale VLA models. Chen et al. [229] investigate the integration of chain-of-thought reasoning into embodied policy learning, demonstrating that lightweight reasoning mechanisms can yield significant performance gains with a 3× inference speedup compared to standard approaches. 

Together, these efforts indicate a converging trajectory toward generalist embodied agents trained on massive, diverse datasets and equipped with modular reasoning capabilities. The combination of large-scale pre-training, efficient adaptation, and transferable affordance representations is positioning foundation-scale VLA models as the backbone for next-generation robotic intelligence. The representative works in this direction are summarized in Table 4(D), highlighting both data-centric and algorithmic advances driving foundation-scale VLA research. 

### _3.4.5 Practical Deployment over Efficiency, Safety, and Human–Robot Collaboration_ 

As VLA models transition from research to real-world applications, practical deployment demands a holistic focus on efficiency, robustness, and human–robot interaction. Realtime inference, resilience to adversarial conditions, and seamless collaborative workflows are critical for reliable operation in dynamic, unpredictable environments. This direction integrates system optimization with safety and adaptability, ensuring that high-capacity models remain both effective and trustworthy in practice. 

15 


Fig. 4: Sample data of various datasets. 

Efficiency-Oriented Designs have focused on reducing inference latency, lowering computational demands, and improving adaptability to resource-constrained platforms. For real-time execution, RTC (Real-Time Chunking) [242] predicts upcoming action segments while executing current ones, enabling continuous high-frequency control. EdgeVLA [232] eliminates autoregressive dependencies in end-effector prediction and incorporates compact language models, achieving a 6× speedup with minimal performance degradation. Similarly, DeeR-VLA [233] employs dynamic early-exit mechanisms to terminate inference once confidence thresholds are met, reducing online control costs. 

Maintaining knowledge integrity during adaptation has become another priority. Knowledge-insulating VLA models [251] address semantic degradation when integrating specialized modules into pretrained VLMs, using insulation strategies to retain cross-task generalization. Consistency-based acceleration strategies, such as CEEDVLA [235], apply consistency distillation and early-exit decoding to achieve over 4× inference acceleration while mitigating error accumulation through mixed-label supervision. Lightweight multi-modal fusion approaches like RoboMamba [236] and cross-domain adaptation methods such as ReVLA [237] further contribute to deployable efficiency. 

Safety and Robustness have emerged as equally critical pillars for deployment readiness. SAFE [238] leverages internal VLA feature representations to detect failures across multiple tasks, generalizing to unseen scenarios and enabling proactive intervention. Security assessments by Cheng et al. [252] via the Physical Vulnerability Evaluation Procedures (PVEP) reveal vulnerabilities to adversarial patches, typography-based prompts, and distributional shifts, motivating the development of adversarially robust perception–control pipelines. Interpretability-focused work, such as Lu et al. [253], uncovers symbolic encodings of objects, relations, and actions in VLA hidden layers, laying the groundwork for more transparent decision-making. Adaptive control frameworks like DyWA [239] further enhance robustness by jointly modeling geometry, state, physics, and action to respond to dynamic, partially observable conditions. 

Human–Robot Collaboration research has explored interactive learning loops where humans and VLA models refine each other’s performance. Xiang et al. [254] propose collaborative frameworks that integrate limited expert interventions into VLA decision-making, reducing 

operator workload while enriching model training data. Closed-loop strategies like those in Zhi et al. [255] combine GPT-4V perception with real-time feedback control to adapt to environmental changes on the fly. History-aware policy learning [256] and object-centric visual prompting approaches such as CrayonRobo [240] enhance task grounding and transparency, while skill library construction [257] and grounding mask methods [258] enable scalable, reusable task decomposition. Camera-space policy designs like cVLA [241] improve sim-to-real transfer by predicting trajectory waypoints directly in 2D image coordinates, making policies more embodiment-agnostic. The representative methods for practical deployment are summarized in Table 4(E), highlighting key innovations across efficiency, safety, and human–robot collaboration. 

In summary, practical deployment of VLA systems demands a multi-faceted design philosophy that simultaneously addresses efficiency, safety, and collaborative adaptability. The integration of real-time inference optimization, robustness against failures and adversarial conditions, and human-in-the-loop refinement strategies is paving the way for persistent, reliable, and interactive robotic systems in real-world environments. 

### _3.4.6 Discussion_ 

**Innovations** The surveyed other advanced VLA highlight several innovations that collectively extend VLA research beyond the confines of previous section. Hybrid architectures that combine complementary paradigms for both reasoning and action generation, advanced multimodal fusion for 3D-aware spatial grounding, and domain adaptations that extend VLA principles to areas such as autonomous driving, humanoid control, and GUI interaction. Foundation-scale models leverage massive multimodal datasets to build increasingly generalist agents, while deployment-oriented methods emphasize efficiency, safety, and human–robot collaboration for real-world applicability. 

**Limitations** However, these hybrid systems remain computationally costly and complex to scale, and multi-modal fusion still struggles with noisy or incomplete real-world inputs. Domain-specific adaptations risk overfitting to narrow contexts, while foundation models demand prohibitive data and resource investments. Deployment efforts, though promising, continue to face challenges in robustness, interpretability, and reliability under adversarial or dynamic conditions. Addressing these limitations will require more 

16 

efficient training strategies, broader evaluation standards, and tighter integration between research design and practical deployment. 

## **4 DATASETS AND BENCHMARKS** 

TABLE 5: Representative Datasets and Benchmarks for Robots. 

|**Dataset Name**|**Year**|**Sensors**|**Episodes**|**Tasks**|
|---|---|---|---|---|
|**(A) Real-world Datasets **|**and B**|**enchmarks**|||
|MIME [259]|2018|RGBD|8300|20|
|EPIC-KITCHENS|2018|RGB|10000|32|
|[260]|||||
|RoboNet [261]|2019|RGB|162000|–|
|MT-Opt [262]|2021|RGB|800000|12|
|<br>BridgeData [24]|2021|RGBD|60100|24|
|<br>Bc-z [263]|2022|RGB|25877|100|
|RT-1 [264]|2022|RGB|13000|700|
|MOO [265]|2023|RGB|59100|–|
|RoboHive [266]|2023|RGBD|98500|38|
|OBRH [267]|2023|RGBD|5600|109|
|RH20T [268]|2024|RGBD|110000|147|
|DROID [269]|2024|RGBD|76000|–|
|AutoRT [270]|2024|RGB|77000|–|
|UMI [271]|2024|RGB|1400|7|
|OXE [8]|2025|RGBD|_>_1000000|160266|
|**(B) Simulation Datasets **|**and B**|**enchmarks**|||
|ROBOTURK [272]|2018|RGB|_>_7868|2200|
|Meta-World [273]|2019|RGB|–|50|
|ALFRED [274]|2019|RGBD|8055|120|
|RLBench [275]|2019|RGBD|–|100|
|<br>VIMA 0.5 [276]|2022|RGB|_>_600000|_>_1000|
|<br>CALVIN 0.5 [277]|2022|RGBD|–|34|
|<br>LIBERO [278]|2023|RGB|5000|100|
|<br>Lota-Bench [279]|2024|RGB|611|12|
|<br>Mobile ALOHA [280]|2024|RGB|825|7|
|RoboCasa [281]|2024|RGBD|_>_100000|100|
|RoboGen [282]|2024|RGB|–|106|


Like other imitation learning approaches, Visual Language Action (VLA) models rely on high-quality labeled datasets. These datasets are either collected from real-world scenarios or generated using simulation environments, the dataset samples are illustrated in Fig. 4. Typically, they contain multimodal observations—such as images, LiDAR point clouds, and inertial measurement unit (IMU) readings—along with corresponding ground-truth labels and language instructions. To facilitate a systematic understanding, we analyze existing datasets and benchmarks, and propose a taxonomy that organizes datasets according to their complexity, modality, and task diversity. This taxonomy provides a clear framework for evaluating the suitability of different datasets for VLA research and highlights potential gaps in existing resources, the representative works are summarized in Table 5. 

### **4.1 Real-World Datasets and Benchmarks** 

High-quality real-world datasets are fundamental for the development of reliable VLA algorithms. In recent years, numerous high-quality and diverse real-world robotics datasets have been collected. Researchers have gathered datasets using different sensor modalities, across a variety of tasks and environmental settings. 

### _4.1.1 Real-World Datasets and Benchmarks for Embodied Robotics_ 

A real-world embodied robotics dataset refers to a collection of multimodal data acquired from robots that interact with their environments through perception and action. Embodied robotics datasets are specifically designed to capture the complex interactions between visual, auditory, proprioceptive, and tactile sensory inputs and the corresponding motor actions, intentions, and environmental contexts. They are essential for training and evaluating models in embodied AI, where the objective is to enable robots to perform tasks through closed-loop, adaptive behaviors in dynamic environments. By providing rich, temporally aligned observations and actions, these datasets serve as foundational resources for developing and benchmarking algorithms in imitation learning, reinforcement learning, visual-language action, and robotic planning. 

Current embodied robot datasets faces significant data costs issues because real-world robot data is not largely collected. Collecting real-world robot datasets poses many challenges. It not only requires hardware equipments, but also requires precise manipulation. Among them, MIME [259], RoboNet [261], and MT-Opt [262] have collected largescale robot demonstration datasets spanning a range of tasks, from simple object pushing to complex household object stacking. Different from prior datasets that often assume a single optimal trajectory per task, these datasets include multiple demonstrations for the same task, using the minimum distance among test trajectories as an evaluation metric. This approach has significantly advanced research in manipulation and VLA tasks. BridgeData [24] offers a large-scale, multi-domain robot dataset comprising 71 tasks across 10 environments. Experiments demonstrate that jointly training on this dataset along with a small subset (e.g., 50 tasks) of unseen tasks in a new domain can double success rates compared to using target domain data alone. As a result, many contemporary VLA methods adopt BridgeData for model training. In the embodied AI field, model generalization is often limited by the difficulty of collecting diverse real-world robotic data. RT-1 [264] provides a broad dataset of real-world robotic tasks to improve both task performance and generalization to novel scenarios. Similarly, Bc-z [263] includes previously unseen manipulation tasks involving novel combinations of objects within the same scene, supporting research in generalizable policy learning. Several datasets also provide comprehensive software platforms and ecosystems for Embodied AI, covering environments such as hand manipulation, locomotion, multi-tasking, multi-agent scenarios, and musclebased control [265]. Compared to earlier works, RoboHive [266] bridges the gap between current robot learning capabilities and potential growth, supporting diverse learning paradigms including reinforcement, imitation, and transfer learning. Distinctively, RH20T [268] offers 147 tasks encompassing 110K manipulation episodes, including multimodal visual, force, audio, and action data. Each episode is accompanied by a human demonstration and language description, making this dataset particularly suitable for one-shot imitation learning and policy transfer to new tasks based on previously trained episodes. 

17 

To advance the development of more generalizable manipulation policies, the robotics community must prioritize the collection of large-scale, diverse datasets spanning a wide range of tasks and environmental settings. Several datasets have been collaboratively gathered by multiple robots across different regions, making them among the most geographically and contextually diverse embodied robot datasets to date [269], [270], [271], [283]. In addition, Open X-Embodiment (OXE) [8] consolidates 22 robot datasets collected through collaboration among 21 institutions, covering 527 skills and 160,266 tasks. OXE provides standardized data formats to facilitate easy use by researchers. An overview of these datasets is provided in Table 5 (A). 

For benchmark evaluation, researchers typically use Success Rate—the proportion of tasks successfully completed relative to the total number of tasks. Some studies additionally employ Language Following Rate to assess the model’s ability to interpret and execute language instructions. Furthermore, recent VLA models are often evaluated by transferring trained policies to previously unseen environments to measure robustness and generalization performance [2], [21]. 

### _4.1.2 Real-World Datasets and Benchmarks for Autonomous Driving_ 

Autonomous driving dataset is different from embodied robot dataset. It has emerged as one of the most transformative applications of artificial intelligence, relying heavily on large-scale datasets to train and evaluate perception, planning, and control algorithms. High-quality datasets are foundational for the development of robust and generalizable autonomous driving systems, as they enable supervised learning, benchmarking, and simulation of rare or safety-critical scenarios. Over the past decade, numerous datasets such as, [284], [285], [286], [287], [288], [289], [290], [291], [292], [293], have been introduced, offering multi-modal sensor data including camera images, LiDAR point clouds, radar signals, and high-definition maps. These datasets vary significantly in geographic coverage, sensor configuration, driving behavior diversity, and annotation richness, making them complementary resources for research and development. 

However, most public datasets are collected in open-loop settings and primarily represent normal driving behavior, which limits their ability to cover long-tail corner cases. To address this gap, recent efforts have focused on generating synthetic data, simulating closed-loop interactions, and curating datasets tailored to rare or safety-critical events. Continued innovation in dataset design remains vital for advancing safe, scalable, and generalizable autonomous driving systems. 

For evaluation, autonomous driving VLA models commonly rely on metrics such as L2 distance, which measures deviation from reference trajectories—and completion rate, which quantifies the proportion of successfully completed driving tasks. 

### **4.2 Simulation Datasets and Benchmarks** 

Collecting large-scale real-world data for continuous control tasks poses significant challenges, as these tasks require 

real-time interaction and continuous feedback from human annotators. Moreover, acquiring such data is often costly and time-consuming, limiting its scalability. This enables a scalable mechanism for diverse human supervision on an extensive set of problem instances. To investigate the performance of embodied robot or autonomous driving models in large-scale and high-quality data, researchers utilize the simulated data from virtualization engines for training and evaluation. 

### _4.2.1 Simulation Datasets and Benchmarks for Embodied Robotics_ 

Simulation datasets for embodied AI typically include synthetic scenes, physics-based interactions, annotations for navigation, object manipulation, task execution, and agentenvironment dynamics. These datasets allow for benchmarking and training across a wide range of tasks, from visual navigation and semantic exploration to complex multistep object manipulation. Prominent examples include [273], [275], [282], [294], [295], each offering different trade-offs in realism, task diversity, and control fidelity. By enabling safe experimentation and massive-scale data collection, simulation datasets are foundational to the development of robust, generalizable embodied agents. As the field matures, the design of richer, more realistic simulation datasets, covering diverse embodiments, tasks, and environments, continues to drive progress toward real-world deployment. 

ROBOTURK [272] is a simulated dataset for high quality 6-DoF manipulation states and actions, collected through teleoperation using mobile devices. Unlike traditional approaches that rely on remote users to demonstrate actions within a virtual engine, ROBOTURK leverages policy learning to generate multi-step robot tasks with varying rewards. By aggregating large quantities of demonstrations, the dataset provides precise and reliable data for both training and evaluation. iGibson0.5 [296] introduces a benchmark for training and evaluating interactive navigation solutions. This work not only provides a novel experimental simulation environment but also proposes a dedicated metric to assess the interplay between navigation and physical interaction along navigation paths. The benchmark introduces the Interactive Navigation Score, composed of two submetrics: Path Efficiency and Effort Efficiency. Path Efficiency is defined as the ratio between the length of the shortest successful path and the actual path length traversed by the robot, weighted by a success indicator function. Effort Efficiency captures the excess kinematic and dynamic effort required during navigation, reflecting the cost of physical interactions. VIMA [276] introduces a new benchmark, VIMABENCH, which establishes a four-level evaluation protocol to assess progressively stronger generalization capabilities, ranging from randomized object placement to entirely novel tasks. Similarly, CALVIN and LOTA-Bench [277], [279] focus on learning long-horizon, language-conditioned tasks across diverse manipulation environments using multimodal robot sensor data. These benchmarks are particularly suited for evaluating methods that aim to generalize to unseen entities by training on large-scale interaction datasets and testing on novel scenes. Performance in these benchmarks is typically measured using task success rates. An overview of these simulation datasets is provided in Table 5(B). 

18 

### _4.2.2 Simulation Datasets and Benchmarks for Autonomous Driving_ 

Closed-loop simulation plays a critical role in ensuring the safety of autonomous driving systems, as it enables the generation of safety-critical scenarios that are difficult or dangerous to capture in the real world. While previously recorded driving logs provide valuable resources for constructing new scenarios, closed-loop evaluation demands modifications to the original sensor data in order to reflect updated scene configurations. For example, actors may need to be added or removed, and the trajectories of both existing actors and the ego vehicle may differ from those in the original recordings [297], [298]. UniSim [299] is a neural sensor simulator that extends single recorded trajectories into multi-sensor closed-loop simulations. It constructs neural feature grids to reconstruct both static backgrounds and dynamic actors, compositing them to simulate LiDAR and camera data from novel viewpoints. This allows for the addition, removal, or repositioning of actors. To better accommodate unseen viewpoints, UniSim further employs a convolutional network to complete regions not visible in the original data. 

Unlike real-world autonomous driving datasets, closedloop simulation benchmarks require specialized evaluation metrics tailored to interactive driving tasks. Commonly used metrics include Driving Route (measuring adherence to planned trajectories), Infraction Score (penalizing traffic rule violations), and Completion Score (assessing task completion). Together, these metrics provide a more comprehensive assessment of VLA model performance in realistic, safety-critical driving scenarios. 

### **4.3 Discussion** 

**Innovations** This paper introduce systematic taxonomies, standardized evaluation metrics, and large-scale collaborative efforts such as Open X-Embodiment (OXE), which unifies datasets from multiple institutions to promote reproducibility and generalization. These contributions enable broader coverage of tasks, richer modality combinations, and improved policy transfer across domains, advancing the scalability of embodied AI research. 

**Limitations** However, real-world datasets are expensive and logistically challenging to collect, often restricted to controlled laboratory environments with limited scene diversity; simulation datasets, while scalable and safe, still struggle to fully capture the complexity, noise, and unpredictability of real-world interactions. Moreover, benchmark metrics such as success rate and trajectory deviation may insufficiently reflect nuanced capabilities like language grounding, long-horizon reasoning, or safe deployment in unstructured environments. Addressing these limitations requires not only expanding dataset diversity and realism but also designing richer evaluation protocols that better capture the demands of real-world autonomy. 

## **5 SIMULATORS** 

Robot simulators have become indispensable tools for developing and evaluating intelligent robotic systems in diverse and interactive environments. These platforms typically integrate physics engines, sensor models (e.g., RGB-D, 

IMU, LiDAR), and task logic to support a wide range of tasks such as navigation, manipulation, and multimodal instruction following. State-of-the-art simulators provide scalable, photorealistic, and physically plausible environments for training embodied agents using reinforcement learning, imitation learning, or large pre-trained models. By offering safe, controllable, and reproducible settings, embodied simulators accelerate the development of generalizable robotic intelligence while significantly reducing the cost and risks associated with real-world experimentation [294], [300]. 

THOR [25] is a simulator featuring near photo-realistic 3D indoor scenes, where AI agents can navigate environments and interact with objects to complete tasks. It supports a variety of research areas, including imitation learning, reinforcement learning, manipulation planning, visual question answering, unsupervised representation learning, object detection, and semantic segmentation. In contrast, some simulators are based on virtualized real spaces rather than artificially designed environments, encompassing thousands of full-scale buildings equipped with embodied agents that are subject to realistic physical and spatial constraints [301], [302]. Habitat [26] and Habitat 2.0 [303] further extend this paradigm by offering scalable simulation platforms for training embodied agents in complex 3D environments with interactive, physics-enabled scenarios. ALFRED [274] introduces a benchmark consisting of long-horizon, compositional tasks with non-reversible state changes, aiming to bridge the gap between simulation benchmarks and real-world applications. ALFRED includes both high-level goals and low-level language instructions, making tasks significantly more complex in terms of sequence length, action space, and linguistic variability compared to existing vision-and-language datasets. 

Earlier simulation environments that combined physics and robotic tasks often focused on a narrow set of scenarios and featured only small-scale, simplified scenes. In contrast, iGibson 1.0 [304] and iGibson 2.0 [305] are open-source simulation platforms that support a more diverse set of household tasks within large-scale, realistic environments. Their scenes are replicas of real-world homes, with object distributions and layouts closely aligned with physical spaces, thereby enhancing ecological validity and bridging the gap between simulated and real-world robotic learning. 

Advanced simulators not only allow multiple agents to interact within the same environment but also provide a wide range of sensor and physics outputs. Ideally, such simulators should combine a universal physics engine, a flexible robotics simulation platform, and a high-fidelity rendering system. These features make them powerful tools for both robotic simulation and generative model evaluation [306], [307], [308], [309], [310], [311]. 

MuJoCo [27] is a widely adopted, open-source physics engine designed to facilitate research and development in robotics and related domains that require accurate simulation. More recently, GPU-based simulation engines have gained popularity. Notably, NVIDIA Isaac Gym [28], built on the Omniverse platform, enables large-scale development, simulation, and testing of AI-driven robots in physically realistic virtual environments. Isaac Gym has become increasingly popular in both academia and industry for accelerating the creation of new robotics tools and enhancing 

19 

### existing systems. 

Similar challenges exist in autonomous driving, where large-scale real-world data collection and annotation are both costly and time-consuming. Collecting sufficient data to cover the multitude of rare corner cases is particularly difficult. To address this, researchers have developed simulators that include both static road elements (e.g., intersections, traffic lights, and buildings) and dynamic agents (e.g., vehicles and pedestrians). CARLA [29] and LGSVL [312] leverage game engines to render realistic driving scenarios, supporting flexible sensor configurations and generating signals suitable for training and evaluating driving strategies. These platforms have become critical for advancing autonomous driving research by providing controllable, reproducible, and cost-effective testing environments. 

## **6 ROBOT HARDWARE** 

The physical structure of a robot provides the foundation for perception, locomotion, manipulation, and interaction with its environment. Its core components typically include sensors, actuators, power systems, and a control unit. Sensors—such as cameras, LiDAR, inertial measurement units, and tactile arrays—supply essential information about both the external environment and the robot’s internal state. Actuators, including motors, servos, or hydraulic systems, convert control signals into physical actions, enabling tasks such as locomotion and object manipulation. The control unit, generally based on embedded processors or microcontrollers, functions as the computational core by integrating sensor inputs and issuing commands to actuators. Power systems, typically in the form of batteries or external energy sources, sustain continuous operation. Hardware design must balance performance, energy efficiency, weight, and durability to satisfy task-specific requirements across diverse application domains, including industrial automation, service robotics, and autonomous vehicles [313], [314], [315]. 

## **7 CHALLENGES AND FUTURE DIRECTIONS** 

### **7.1 Challenges of Vision-Language-Action Models** 

This section summarizes the open challenges and future directions in advancing Vision-Language-Action (VLA) models. Despite remarkable progress in recent years, the development of VLA models has gradually revealed critical bottlenecks. The most fundamental issue lies in the fact that current VLA systems are largely built upon the transfer of large-scale LLMs or VLMs. Although these models excel in semantic understanding and cross-modal alignment, they lack direct training and experience in interacting with the physical world. As a result, VLA systems often demonstrate the gap of “understanding the instruction but failing to execute the task” in real environments. This reflects a fundamental contradiction: the disconnection between semanticlevel generalization and embodied capabilities in the physical world. How to achieve the transformation from nonembodied knowledge to embodied intelligence, and to truly bridge the gap between semantic reasoning and physical execution, remains the central challenge. Specifically, this contradiction is manifested in the following aspects. 

### _7.1.1 Scarcity of Robotic Data_ 

Robotic interaction data is a critical resource that determines the performance of VLA models; however, existing datasets remain insufficient in both scale and diversity. Collecting large-scale demonstrations across a wide range of tasks and environments in the real world is constrained by hardware costs, experimental efficiency, and safety concerns. Existing open-source datasets, such as Open X-Embodiment, have advanced robot learning but are primarily focused on tabletop manipulation and object grasping. This lack of task and environmental diversity significantly limits generalization to novel contexts and complex tasks. Simulation platforms, such as RLBench, offer a cost-effective means of generating large-scale trajectories but are constrained by rendering fidelity, physics engine accuracy, and task modeling limitations. Even with techniques such as domain randomization or style transfer, the sim-to-real gap persists, with many models performing well in simulation yet failing when deployed on physical robots. Therefore, enhancing both the diversity and realism of robotic data at scale remains a primary challenge in mitigating generalization deficits. 

### _7.1.2 Architectural Heterogeneity_ 

Most VLA models attempt end-to-end modeling across vision, language, and action, but their implementations reveal strong heterogeneity. On one hand, different works adopt different backbone networks: vision encoders may rely on ViT, DINOv2, or SigLIP; language backbones on PaLM, LLaMA, or Qwen; and action heads on discrete tokenization, continuous control vectors, or even diffusion-based generation. Such architectural diversity hinders comparison and reuse across models, slowing the emergence of unified standards. On the other hand, perception, reasoning, and control are often loosely coupled internally, leading to fragmented feature spaces and weak portability across platforms or task domains. Some models excel at crosstask language understanding but require heavy adaptation when interfacing with low-level controllers. This architectural heterogeneity increases integration complexity and significantly constrains generalization and scalability. 

### _7.1.3 Real-Time Inference Constraints and Cost_ 

Current VLA models are heavily dependent on large-scale Transformer architectures with autoregressive decoding, which severely limits inference speed and execution efficiency on real robots. Since each action token depends on the previous one, latency accumulates, while highfrequency tasks such as dynamic grasping or mobile navigation demand millisecond-level responses. Moreover, highdimensional visual inputs and massive parameter counts impose prohibitive computation and memory costs. Many state-of-the-art VLAs require GPU memory far beyond the capacity of typical embedded platforms. Even with quantization, compression, or edge–cloud co-inference, it remains difficult to balance accuracy, real-time performance, and low cost. This combination of inference constraints and hardware bottlenecks leaves VLA deployment trapped between being too slow and too expensive. 

20 

### _7.1.4 Pseudo-Interaction in Human–Robot Interaction_ 

Systems generate actions based on prior knowledge or static training patterns rather than engaging in genuine interaction grounded in environmental dynamics and causal reasoning. When encountering unfamiliar settings or state changes, models often rely on statistical co-occurrence learned from data, rather than probing the environment or using sensor feedback to refine actions. This lack of causal reasoning means that VLAs may appear to follow instructions but fail to establish genuine causal chains between environment states and action outcomes. As a result, robots often fail to adapt in dynamic environments. This pseudointeraction highlights VLA’s deficiency in causal modeling and feedback utilization, and remains a key obstacle to embodied intelligence. 

### _7.1.5 Evaluation and Benchmarking Limitations_ 

The evaluation of VLA models is also limited. Current benchmarks are mainly set in laboratory or highly structured simulated environments, focusing on tabletop manipulation or object grasping. While such tasks measure performance on narrow distributions, they do not capture generalization or robustness in open-world scenarios. Once deployed in outdoor, industrial, or complex home settings, performance often degrades drastically, exposing the gap between evaluation and real-world applicability. This narrow evaluation scope hinders comprehensive assessment of VLA feasibility and limits horizontal comparisons across models. The lack of unified, authoritative, and diverse benchmarks is becoming a major bottleneck for real-world progress. 

While these five aspects highlight key shortcomings in data, architecture, interaction, and evaluation, they do not exhaust the challenges faced by VLA research. More fundamentally, the long-term question is whether VLA systems can truly achieve controllability, trustworthiness, and safety. In other words, the future of VLA requires not only solving performance and generalization issues but also addressing the deeper concerns of deploying intelligent agents responsibly. This transition implies that researchers must move beyond model optimization toward systemic paradigm shifts in order to meet long-term challenges. 

to close the loop from semantic understanding to physical execution. Beyond a technical advance, this would mark a crucial step toward artificial general intelligence. 

### _7.2.2 Breakthroughs in Causal Reasoning and Genuine Interaction_ 

Most existing VLAs rely on static data distributions and surface-level correlations, lacking the ability to interact based on causal laws. They simulate interaction by guessing from prior patterns, rather than probing the environment and updating strategies with feedback. If future VLAs can incorporate causal modeling and interactive reasoning, robots will learn to probe, validate, and adapt—enabling genuine dialogue with dynamic environments. Such a breakthrough would overcome pseudointeraction and mark the transition from data-driven intelligence to deeply interactive intelligence. 

### _7.2.3 Virtual–Real Integration and Large-Scale Data Generation_ 

While data scarcity is a critical limitation, it also represents a massive opportunity. If virtual and real data ecosystems can be integrated—through high-fidelity simulation, synthetic data generation, and multi-robot sharing—it will be possible to construct datasets containing trillions of trajectories across diverse tasks. Just as GPT leveraged internet-scale corpora to trigger a leap in language intelligence, such data ecosystems could trigger a leap in embodied generalization, enabling VLAs to operate robustly in open-world scenarios. 

### _7.2.4 Societal Embedding and Trustworthy Ecosystems_ 

The ultimate value of VLA lies not only in technical capability but also in societal integration. As VLA enters public and domestic spaces, safety, trustworthiness, and ethical alignment will determine its adoption. Establishing standardized frameworks for risk assessment, explainability, and accountability would transform VLAs from laboratory artifacts into trusted partners. Once embedded in society, VLAs could serve as the next-generation human–AI interface, reshaping domains such as healthcare, industry, education, and services. This societal embedding marks a milestone opportunity for translating frontier research into real-world transformation. 

### **7.2 Opportunities of Vision-Language-Action Models** 

Despite formidable challenges, the future of VLA is also full of opportunities. As the crucial bridge connecting language, perception, and action, VLA has the potential to transcend the semantic–physical gap and become a central pathway for embodied intelligence. Overcoming current bottlenecks could reshape the paradigm of robotics research and position VLA at the forefront of real-world deployment. 

### _7.2.1 World Modeling and Cross-Modal Unification_ 

At present, language, vision, and action remain loosely coupled in VLA systems, confining them to instruction “generation” rather than holistic world understanding. Achieving true cross-modal unification would enable VLA to model environments, reasoning, and interaction jointly within a single token stream. This unified structure would allow VLA to evolve into a proto–world model, enabling robots 

## **8 CONCLUSION** 

Recent advances in Vision-Language-Action (VLA) models have extended the generalizable capabilities of visionlanguage models to robotic applications, including embodied AI, autonomous driving, and diverse manipulation tasks. This survey systematically charts the emergence of VLA approaches by examining their motivations, methodologies, and applications. It provides a unified taxonomy of architectural structures and analyzes over 300 articles, along with supporting materials. We first categorize VLA architectural innovations based on autoregression-based models, diffusion-based models, reinforcement-based learning, hybrid structures, and efficiency optimization techniques. Subsequently, we explore the datasets, benchmarks, and simulation platforms that facilitate VLA training and evaluation. Building on this comprehensive review, we analyze the 

21 

strengths and limitations of current approaches and highlight potential directions for future research. Collectively, these insights offer a consolidated reference and a forwardlooking roadmap for developing trustworthy, continually evolving VLAs capable of advancing general artificial intelligence in robotic systems. 

## **REFERENCES** 

- [1] J. Wen, M. Zhu, Y. Zhu, Z. Tang, J. Li, Z. Zhou, C. Li, X. Liu, Y. Peng, C. Shen, and F. Feng, “Diffusion-vla: Generalizable and interpretable robot foundation model via self-generated reasoning,” 2025. [Online]. Available: https: //arxiv.org/abs/2412.03293 

- [2] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, L. X. Shi, J. Tanner, Q. Vuong, A. Walling, H. Wang, and U. Zhilinsky, “ _π_ 0: A vision-language-action flow model for general robot control,” 2024. [Online]. Available: https://arxiv.org/abs/2410.24164 

- [3] Y. Liu, X. Li, Z. Wang, B. Zhao, and C. Xie, “Clips: An enhanced clip framework for learning with synthetic captions,” 2024. [Online]. Available: https://arxiv.org/abs/2411.16828 

- [4] J. Li, D. Li, C. Xiong, and S. Hoi, “Blip: Bootstrapping languageimage pre-training for unified vision-language understanding and generation,” 2022. [Online]. Available: https://arxiv.org/ abs/2201.12086 

- [5] L. Xue, M. Shu, A. Awadalla, J. Wang, A. Yan, S. Purushwalkam, H. Zhou, V. Prabhu, Y. Dai, M. S. Ryoo, S. Kendre, J. Zhang, S. Tseng, G. A. Lujan-Moreno, M. L. Olson, M. Hinck, D. Cobbley, V. Lal, C. Qin, S. Zhang, C.-C. Chen, N. Yu, J. Tan, T. M. Awalgaonkar, S. Heinecke, H. Wang, Y. Choi, L. Schmidt, Z. Chen, S. Savarese, J. C. Niebles, C. Xiong, and R. Xu, “xgen-mm (blip-3): A family of open large multimodal models,” 2025. [Online]. Available: https://arxiv.org/abs/2408.08872 

- [6] S. Bai, K. Chen, X. Liu, J. Wang, W. Ge, S. Song, K. Dang, P. Wang, S. Wang, J. Tang, H. Zhong, Y. Zhu, M. Yang, Z. Li, J. Wan, P. Wang, W. Ding, Z. Fu, Y. Xu, J. Ye, X. Zhang, T. Xie, Z. Cheng, H. Zhang, Z. Yang, H. Xu, and J. Lin, “Qwen2.5-vl technical report,” 2025. [Online]. Available: https://arxiv.org/abs/2502.13923 

- [7] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” 2024. [Online]. Available: https://arxiv.org/abs/2303.04137 

- [8] A. O’Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain _et al._ , “Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 6892– 6903. 

- [9] A. Krizhevsky, I. Sutskever, and G. E. Hinton, “Imagenet classification with deep convolutional neural networks,” _Advances in neural information processing systems_ , vol. 25, 2012. 

- [10] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in _Proceedings of the IEEE conference on computer vision and pattern recognition_ , 2016, pp. 770–778. 

- [11] A. Dosovitskiy, L. Beyer, A. Kolesnikov, D. Weissenborn, X. Zhai, T. Unterthiner, M. Dehghani, M. Minderer, G. Heigold, S. Gelly _et al._ , “An image is worth 16x16 words: Transformers for image recognition at scale,” _arXiv preprint arXiv:2010.11929_ , 2020. 

- [12] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “Bert: Pretraining of deep bidirectional transformers for language understanding,” in _Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, volume 1 (long and short papers)_ , 2019, pp. 4171–4186. 

- [13] A. Radford, K. Narasimhan, T. Salimans, I. Sutskever _et al._ , “Improving language understanding by generative pre-training,” 2018. 

- [14] C. Raffel, N. Shazeer, A. Roberts, K. Lee, S. Narang, M. Matena, Y. Zhou, W. Li, and P. J. Liu, “Exploring the limits of transfer learning with a unified text-to-text transformer,” _Journal of machine learning research_ , vol. 21, no. 140, pp. 1–67, 2020. 

- [15] J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat _et al._ , “Gpt-4 technical report,” _arXiv preprint arXiv:2303.08774_ , 2023. 

- [16] J. Lu, D. Batra, D. Parikh, and S. Lee, “Vilbert: Pretraining taskagnostic visiolinguistic representations for vision-and-language tasks,” _Advances in neural information processing systems_ , vol. 32, 2019. 

- [17] L. H. Li, M. Yatskar, D. Yin, C.-J. Hsieh, and K.-W. Chang, “Visualbert: A simple and performant baseline for vision and language,” _arXiv preprint arXiv:1908.03557_ , 2019. 

- [18] J. Li, D. Li, S. Savarese, and S. Hoi, “Blip-2: Bootstrapping language-image pre-training with frozen image encoders and large language models,” in _International conference on machine learning_ . PMLR, 2023, pp. 19 730–19 742. 

- [19] J.-B. Alayrac, J. Donahue, P. Luc, A. Miech, I. Barr, Y. Hasson, K. Lenc, A. Mensch, K. Millican, M. Reynolds _et al._ , “Flamingo: a visual language model for few-shot learning,” _Advances in neural information processing systems_ , vol. 35, pp. 23 716–23 736, 2022. 

- [20] H. Liu, C. Li, Q. Wu, and Y. J. Lee, “Visual instruction tuning,” _Advances in neural information processing systems_ , vol. 36, pp. 34 892–34 916, 2023. 

- [21] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn, “Openvla: An open-source visionlanguage-action model,” 2024. [Online]. Available: https: //arxiv.org/abs/2406.09246 

- [22] K. Pertsch, K. Stachowicz, B. Ichter, D. Driess, S. Nair, Q. Vuong, O. Mees, C. Finn, and S. Levine, “Fast: Efficient action tokenization for vision-language-action models,” 2025. [Online]. Available: https://arxiv.org/abs/2501.09747 

- [23] S. Yang, H. Li, Y. Chen, B. Wang, Y. Tian, T. Wang, H. Wang, F. Zhao, Y. Liao, and J. Pang, “Instructvla: Vision-language-action instruction tuning from understanding to manipulation,” _arXiv preprint arXiv:2507.17520_ , 2025. 

- [24] F. Ebert, Y. Yang, K. Schmeckpeper, B. Bucher, G. Georgakis, K. Daniilidis, C. Finn, and S. Levine, “Bridge data: Boosting generalization of robotic skills with cross-domain datasets,” _arXiv e-prints_ , pp. arXiv–2109, 2021. 

- [25] E. Kolve, R. Mottaghi, W. Han, E. VanderBilt, L. Weihs, A. Herrasti, M. Deitke, K. Ehsani, D. Gordon, Y. Zhu _et al._ , “Ai2thor: An interactive 3d environment for visual ai,” _arXiv preprint arXiv:1712.05474_ , 2017. 

- [26] M. Savva, A. Kadian, O. Maksymets, Y. Zhao, E. Wijmans, B. Jain, J. Straub, J. Liu, V. Koltun, J. Malik _et al._ , “Habitat: A platform for embodied ai research,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2019, pp. 9339–9347. 

- [27] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for model-based control,” in _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ . IEEE, 2012, pp. 5026–5033. 

- [28] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa, and G. State, “Isaac gym: High performance gpu-based physics simulation for robot learning,” 2021. [Online]. Available: https://arxiv.org/abs/2108.10470 

- [29] A. Dosovitskiy, G. Ros, F. Codevilla, A. Lopez, and V. Koltun, “Carla: An open urban driving simulator,” 2017. [Online]. Available: https://arxiv.org/abs/1711.03938 

- [30] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan _et al._ , “Rt-1: Robotics transformer for real-world control at scale,” 2023. [Online]. Available: https://arxiv.org/abs/2212.06817 

- [31] J. Cen, C. Yu, H. Yuan, Y. Jiang, S. Huang, J. Guo, X. Li, Y. Song, H. Luo, F. Wang _et al._ , “Worldvla: Towards autoregressive action world model,” _arXiv preprint arXiv:2506.21539_ , 2025. 

- [32] S. Reed, K. Zolna, E. Parisotto, S. G. Colmenarejo, A. Novikov, G. Barth-Maron, M. Gimenez, Y. Sulsky, J. Kay, J. T. Springenberg, T. Eccles, J. Bruce, A. Razavi, A. Edwards, N. Heess, Y. Chen, R. Hadsell, O. Vinyals, M. Bordbar, and N. de Freitas, “A generalist agent,” 2022. [Online]. Available: https://arxiv.org/abs/2205.06175 

- [33] D. Driess, F. Xia, M. S. M. Sajjadi, C. Lynch, A. Chowdhery, B. Ichter, A. Wahid, J. Tompson, Q. Vuong, T. Yu, W. Huang, Y. Chebotar, P. Sermanet, D. Duckworth, S. Levine, V. Vanhoucke, K. Hausman, M. Toussaint, K. Greff, A. Zeng, I. Mordatch, and 

22 

P. Florence, “Palm-e: An embodied multimodal language model,” 2023. [Online]. Available: https://arxiv.org/abs/2303.03378 

- [34] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, X. Chen, K. Choromanski, T. Ding, D. Driess, A. Dubey, C. Finn, P. Florence, C. Fu, M. G. Arenas, K. Gopalakrishnan, K. Han, K. Hausman, A. Herzog, J. Hsu, B. Ichter, A. Irpan, N. Joshi, R. Julian, D. Kalashnikov, Y. Kuang, I. Leal, L. Lee, T.-W. E. Lee, S. Levine, Y. Lu, H. Michalewski, I. Mordatch, K. Pertsch, K. Rao, K. Reymann, M. Ryoo, G. Salazar, P. Sanketi, P. Sermanet, J. Singh, A. Singh, R. Soricut, H. Tran, V. Vanhoucke, Q. Vuong, A. Wahid, S. Welker, P. Wohlhart, J. Wu, F. Xia, T. Xiao, P. Xu, S. Xu, T. Yu, and B. Zitkovich, “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” 2023. [Online]. Available: https://arxiv.org/abs/2307.15818 

- [35] J. Huang, S. Yong, X. Ma, X. Linghu, P. Li, Y. Wang, Q. Li, S.-C. Zhu, B. Jia, and S. Huang, “An embodied generalist agent in 3d world,” 2024. [Online]. Available: https://arxiv.org/abs/2311.12871 

- [36] O. M. Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, J. Luo, Y. L. Tan, L. Y. Chen, P. Sanketi, Q. Vuong, T. Xiao, D. Sadigh, C. Finn, and S. Levine, “Octo: An open-source generalist robot policy,” 2024. [Online]. Available: https://arxiv.org/abs/2405.12213 

- [37] H. Etukuru, N. Naka, Z. Hu, S. Lee, J. Mehu, A. Edsinger, C. Paxton, S. Chintala, L. Pinto, and N. M. M. Shafiullah, “Robot utility models: General policies for zero-shot deployment in new environments,” 2024. [Online]. Available: https: //arxiv.org/abs/2409.05865 

- [38] F. Yan, F. Liu, L. Zheng, Y. Zhong, Y. Huang, Z. Guan, C. Feng, and L. Ma, “Robomm: All-in-one multimodal large model for robotic manipulation,” 2024. [Online]. Available: https://arxiv.org/abs/2412.07215 

- [39] J. Zhang, Y. Guo, Y. Hu, X. Chen, X. Zhu, and J. Chen, “Up-vla: A unified understanding and prediction model for embodied agent,” 2025. [Online]. Available: https://arxiv.org/abs/2501. 18867 

- [40] J. Zheng, J. Li, D. Liu, Y. Zheng, Z. Wang, Z. Ou, Y. Liu, J. Liu, Y.-Q. Zhang, and X. Zhan, “Universal actions for enhanced embodied foundation models,” 2025. [Online]. Available: https://arxiv.org/abs/2501.10105 

- [41] P. Ding, J. Ma, X. Tong, B. Zou, X. Luo, Y. Fan, T. Wang, H. Lu, P. Mo, J. Liu, Y. Wang, H. Zhou, W. Feng, J. Liu, S. Huang, and D. Wang, “Humanoid-vla: Towards universal humanoid control with visual integration,” 2025. [Online]. Available: https://arxiv.org/abs/2502.14795 

- [42] C.-Y. Hung, Q. Sun, P. Hong, A. Zadeh, C. Li, U.-X. Tan, N. Majumder, and S. Poria, “Nora: A small open-sourced generalist vision language action model for embodied tasks,” 2025. [Online]. Available: https://arxiv.org/abs/2504.19854 

- [43] F. Lin, R. Nai, Y. Hu, J. You, J. Zhao, and Y. Gao, “Onetwovla: A unified vision-language-action model with adaptive reasoning,” 2025. [Online]. Available: https://arxiv.org/abs/2505.11917 

- [44] J. Lin, A. Taherin, A. Akbari, A. Akbari, L. Lu, G. Chen, T. Padir, X. Yang, W. Chen, Y. Li, X. Lin, D. Kaeli, P. Zhao, and Y. Wang, “Vote: Vision-language-action optimization with trajectory ensemble voting,” 2025. [Online]. Available: https://arxiv.org/abs/2507.05116 

- [45] Q. Bu, Y. Yang, J. Cai, S. Gao, G. Ren, M. Yao, P. Luo, and H. Li, “Univla: Learning to act anywhere with task-centric latent actions,” 2025. [Online]. Available: https://arxiv.org/abs/2505. 06111 

- [46] W. Zhao, G. Li, Z. Gong, P. Ding, H. Zhao, and D. Wang, “Unveiling the potential of vision-language-action models with open-ended multimodal instructions,” 2025. [Online]. Available: https://arxiv.org/abs/2505.11214 

- [47] W. Huang, F. Xia, T. Xiao, H. Chan, J. Liang, P. Florence, A. Zeng, J. Tompson, I. Mordatch, Y. Chebotar, P. Sermanet, N. Brown, T. Jackson, L. Luu, S. Levine, K. Hausman, and B. Ichter, “Inner monologue: Embodied reasoning through planning with language models,” 2022. [Online]. Available: https://arxiv.org/abs/2207.05608 

- [48] S. Huang, Z. Jiang, H. Dong, Y. Qiao, P. Gao, and H. Li, “Instruct2act: Mapping multi-modality instructions to robotic actions with large language model,” 2023. [Online]. Available: https://arxiv.org/abs/2305.11176 

- [49] X. Li, M. Liu, H. Zhang, C. Yu, J. Xu, H. Wu, C. Cheang, Y. Jing, W. Zhang, H. Liu, H. Li, and T. Kong, “Vision-language 

- foundation models as effective robot imitators,” in _The Twelfth International Conference on Learning Representations_ , 2024. [Online]. Available: https://openreview.net/forum?id=lFYj0oibGR 

- [50] X. Li, C. Mata, J. Park, K. Kahatapitiya, Y. S. Jang, J. Shang, K. Ranasinghe, R. Burgert, M. Cai, Y. J. Lee, and M. S. Ryoo, “Llara: Supercharging robot learning data for vision-language policy,” in _International Conference on Learning Representations_ , 2025. 

- [51] M. Zawalski, W. Chen, K. Pertsch, O. Mees, C. Finn, and S. Levine, “Robotic control via embodied chain-of-thought reasoning,” 2025. [Online]. Available: https://arxiv.org/abs/ 2407.08693 

- [52] Z. Xu, H.-T. L. Chiang, Z. Fu, M. G. Jacob, T. Zhang, T.-W. E. Lee, W. Yu, C. Schenck, D. Rendleman, D. Shah, F. Xia, J. Hsu, J. Hoech, P. Florence, S. Kirmani, S. Singh, V. Sindhwani, C. Parada, C. Finn, P. Xu, S. Levine, and J. Tan, “Mobility VLA: Multimodal instruction navigation with long-context VLMs and topological graphs,” in _8th Annual Conference on Robot Learning_ , 2024. [Online]. Available: https://openreview.net/forum?id=JScswMfEQ0 

- [53] O. Sautenkov, Y. Yaqoot, A. Lykov, M. A. Mustafa, G. Tadevosyan, A. Akhmetkazy, M. Altamirano Cabrera, M. Martynov, S. Karaf, and D. Tsetserukou, “Uav-vla: Vision-language-action system for large scale aerial mission generation,” in _Proceedings of the 2025 ACM/IEEE International Conference on Human-Robot Interaction_ , ser. HRI ’25. IEEE Press, 2025, p. 1588–1592. 

- [54] J. Huang, S. Wang, F. Lin, Y. Hu, C. Wen, and Y. Gao, “Tactile-vla: Unlocking vision-language-action model’s physical knowledge for tactile generalization,” 2025. [Online]. Available: https://arxiv.org/abs/2507.09160 

- [55] M. H. Khan, S. Asfaw, D. Iarchuk, M. A. Cabrera, L. Moreno, I. Tokmurziyev, and D. Tsetserukou, “Shake-vla: Visionlanguage-action model-based system for bimanual robotic manipulations and liquid mixing,” 2025. [Online]. Available: https://arxiv.org/abs/2501.06919 

- [56] L. X. Shi, B. Ichter, M. Equi, L. Ke, K. Pertsch, Q. Vuong, J. Tanner, A. Walling, H. Wang, N. Fusai, A. Li-Bell, D. Driess, L. Groom, S. Levine, and C. Finn, “Hi robot: Open-ended instruction following with hierarchical vision-language-action models,” 2025. [Online]. Available: https://arxiv.org/abs/2502.19417 

- [57] Y. Zhong, X. Huang, R. Li, C. Zhang, Y. Liang, Y. Yang, and Y. Chen, “Dexgraspvla: A vision-language-action framework towards general dexterous grasping,” 2025. [Online]. Available: https://arxiv.org/abs/2502.20900 

- [58] Y. Li, Y. Deng, J. Zhang, J. Jang, M. Memmel, R. Yu, C. R. Garrett, F. Ramos, D. Fox, A. Li, A. Gupta, and A. Goyal, “Hamster: Hierarchical action models for open-world robot manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2502.05485 

- [59] Q. Zhao, Y. Lu, M. J. Kim, Z. Fu, Z. Zhang, Y. Wu, Z. Li, Q. Ma, S. Han, C. Finn, A. Handa, M.-Y. Liu, D. Xiang, G. Wetzstein, and T.-Y. Lin, “Cot-vla: Visual chain-of-thought reasoning for vision-language-action models,” 2025. [Online]. Available: https://arxiv.org/abs/2503.22020 

- [60] G. R. Team, S. Abeyruwan, J. Ainslie, J.-B. Alayrac, M. G. Arenas, T. Armstrong _et al._ , “Gemini robotics: Bringing ai into the physical world,” 2025. [Online]. Available: https://arxiv.org/abs/2503.20020 

- [61] A. Lykov, V. Serpiva, M. H. Khan, O. Sautenkov, A. Myshlyaev, G. Tadevosyan, Y. Yaqoot, and D. Tsetserukou, “Cognitivedrone: A vla model and evaluation benchmark for real-time cognitive task solving and reasoning in uavs,” _arXiv preprint arXiv:2503.01378_ , 2025. 

- [62] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, M. Y. Galliker, D. Ghosh, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, D. LeBlanc, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, A. Z. Ren, L. X. Shi, L. Smith, J. T. Springenberg, K. Stachowicz, J. Tanner, Q. Vuong, H. Walke, A. Walling, H. Wang, L. Yu, and U. Zhilinsky, “ _π_ 0 _._ 5: a vision-language-action model with open-world generalization,” 2025. [Online]. Available: https://arxiv.org/abs/2504.16054 

- [63] J. Zhang, S. Wu, X. Luo, H. Wu, L. Gao, H. T. Shen, and J. Song, “Inspire: Vision-language-action models with intrinsic spatial reasoning,” _arXiv preprint arXiv:2505.13888_ , 2025. 

- [64] A. Bucker, L. Figueredo, S. Haddadin, A. Kapoor, S. Ma, S. Vemprala, and R. Bonatti, “Latte: Language trajectory 

23 

transformer,” 2022. [Online]. Available: https://arxiv.org/abs/ 2208.02918 

- [65] Y. Jiang, A. Gupta, Z. Zhang, G. Wang, Y. Dou, Y. Chen, L. Fei-Fei, A. Anandkumar, Y. Zhu, and L. Fan, “Vima: General robot manipulation with multimodal prompts,” 2023. [Online]. Available: https://arxiv.org/abs/2210.03094 

- [66] H. Liu, L. Lee, K. Lee, and P. Abbeel, “Instruction-following agents with multimodal transformer,” 2023. [Online]. Available: https://arxiv.org/abs/2210.13431 

- [67] R. Doshi, H. Walke, O. Mees, S. Dasari, and S. Levine, “Scaling cross-embodied learning: One policy for manipulation, navigation, locomotion and aviation,” 2024. [Online]. Available: https://arxiv.org/abs/2408.11812 

- [68] H. Wu, Y. Jing, C. Cheang, G. Chen, J. Xu, X. Li, M. Liu, H. Li, and T. Kong, “Unleashing large-scale video generative pre-training for visual robot manipulation,” in _The Twelfth International Conference on Learning Representations_ , 2024. [Online]. Available: https://openreview.net/forum?id=NxoFmGgWC9 

- [69] C.-L. Cheang, G. Chen, Y. Jing, T. Kong, H. Li, Y. Li, Y. Liu, H. Wu, J. Xu, Y. Yang, H. Zhang, and M. Zhu, “Gr-2: A generative videolanguage-action model with web-scale knowledge for robot manipulation,” _arXiv preprint arXiv:2410.06158_ , 2024. 

- [70] K. F. Gbagbe, M. A. Cabrera, A. Alabbas, O. Alyunes, A. Lykov, and D. Tsetserukou, “Bi-vla: Vision-language-action model-based system for bimanual robotic dexterous manipulations,” 2024. [Online]. Available: https://arxiv.org/abs/2405.06039 

- [71] S. Li, J. Wang, R. Dai, W. Ma, W. Y. Ng, Y. Hu, and Z. Li, “Robonurse-vla: Robotic scrub nurse system based on vision-language-action model,” 2024. [Online]. Available: https://arxiv.org/abs/2409.19590 

- [72] Y. Chen, Y. Ge, W. Tang, Y. Li, Y. Ge, M. Ding, Y. Shan, and X. Liu, “Moto: Latent motion token as the bridging language for learning robot manipulation from videos,” 2025. [Online]. Available: https://arxiv.org/abs/2412.04445 

- [73] X. Zhou, X. Han, F. Yang, Y. Ma, and A. C. Knoll, “Opendrivevla: Towards end-to-end autonomous driving with large vision language action model,” 2025. [Online]. Available: https://arxiv.org/abs/2503.23463 

- [74] S. Deng, M. Yan, S. Wei, H. Ma, Y. Yang, J. Chen, Z. Zhang, T. Yang, X. Zhang, H. Cui, Z. Zhang, and H. Wang, “Graspvla: a grasping foundation model pre-trained on billion-scale synthetic action data,” 2025. [Online]. Available: https://arxiv.org/abs/2505.03233 

- [75] V. Serpiva, A. Lykov, A. Myshlyaev, M. H. Khan, A. A. Abdulkarim, O. Sautenkov, and D. Tsetserukou, “Racevla: Vla-based racing drone navigation with human-like behaviour,” 2025. [Online]. Available: https://arxiv.org/abs/2503.02572 

- [76] C. Zhang, P. Hao, X. Cao, X. Hao, S. Cui, and S. Wang, “Vtla: Vision-tactile-language-action model with preference learning for insertion manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2505.09577 

- [77] C. Li, J. Wen, Y. Peng, Y. Peng, F. Feng, and Y. Zhu, “Pointvla: Injecting the 3d world into vision-language-action models,” 2025. [Online]. Available: https://arxiv.org/abs/2503.07511 

- [78] R. Zheng, Y. Liang, S. Huang, J. Gao, H. D. III, A. Kolobov, F. Huang, and J. Yang, “Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies,” 2025. [Online]. Available: https://arxiv.org/abs/2412. 10345 

- [79] C. Fan, X. Jia, Y. Sun, Y. Wang, J. Wei, Z. Gong, X. Zhao, M. Tomizuka, X. Yang, J. Yan, and M. Ding, “Interleave-vla: Enhancing robot manipulation with interleaved image-text instructions,” 2025. [Online]. Available: https: //arxiv.org/abs/2505.02152 

- [80] Z. Wu, Y. Zhou, X. Xu, Z. Wang, and H. Yan, “Momanipvla: Transferring vision-language-action models for general mobile manipulation,” in _Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)_ , June 2025, pp. 1714–1723. 

- [81] A. Ajay, S. Han, Y. Du, S. Li, A. Gupta, T. Jaakkola, J. Tenenbaum, L. Kaelbling, A. Srivastava, and P. Agrawal, “Compositional foundation models for hierarchical planning,” 2023. [Online]. Available: https://arxiv.org/abs/2309.08587 

- [82] Y. Ma, D. Chi, S. Wu, Y. Liu, Y. Zhuang, J. Hao, and I. King, “Actra: Optimized transformer architecture for vision-languageaction models in robot learning,” 2024. [Online]. Available: https://arxiv.org/abs/2408.01147 

- [83] Y. Yue, Y. Wang, B. Kang, Y. Han, S. Wang, S. Song, J. Feng, and G. Huang, “Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution,” in _Advances in Neural Information Processing Systems_ , A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, Eds., vol. 37. Curran Associates, Inc., 2024, pp. 56 619–56 643. [Online]. Available: https://proceedings.neurips.cc/paper <u>files/paper/2024/</u> file/67b0e7c7c2a5780aeefe3b79caac106e-Paper-Conference.pdf 

- [84] D. Qu, H. Song, Q. Chen, Y. Yao, X. Ye, Y. Ding, Z. Wang, J. Gu, B. Zhao, D. Wang, and X. Li, “Spatialvla: Exploring spatial representations for visual-language-action model,” 2025. [Online]. Available: https://arxiv.org/abs/2501.15830 

- [85] S. Xu, Y. Wang, C. Xia, D. Zhu, T. Huang, and C. Xu, “Vla-cache: Towards efficient vision-language-action model via adaptive token caching in robotic manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2502.02175 

- [86] J. Jones, O. Mees, C. Sferrazza, K. Stachowicz, P. Abbeel, and S. Levine, “Beyond sight: Finetuning generalist robot policies with heterogeneous sensors via language grounding,” 2025. [Online]. Available: https://arxiv.org/abs/2501.04693 

- [87] R. Zhang, M. Dong, Y. Zhang, L. Heng, X. Chi, G. Dai, L. Du, Y. Du, and S. Zhang, “Mole-vla: Dynamic layerskipping vision language action model via mixture-of-layers for efficient robot manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2503.20384 

- [88] W. Song, J. Chen, P. Ding, H. Zhao, W. Zhao, Z. Zhong, Z. Ge, J. Ma, and H. Li, “Accelerating vision-language-action model integrated with action chunking via parallel decoding,” 2025. [Online]. Available: https://arxiv.org/abs/2503.02310 

- [89] H. Wang, C. Xiong, R. Wang, and X. Chen, “Bitvla: 1-bit vision-language-action models for robotics manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2506.07530 

- [90] P. Li, H. Wu, Y. Huang, C. Cheang, L. Wang, and T. Kong, “Grmg: Leveraging partially-annotated data via multi-modal goalconditioned policy,” _IEEE Robotics and Automation Letters_ , 2025. 

- [91] Y. Yang, J. Sun, S. Kou, Y. Wang, and Z. Deng, “Lohovla: A unified vision-language-action model for long-horizon embodied tasks,” 2025. [Online]. Available: https://arxiv.org/abs/2506.00411 

- [92] H. Huang, F. Liu, L. Fu, T. Wu, M. Mukadam, J. Malik, K. Goldberg, and P. Abbeel, “Otter: A vision-language-action model with text-aware visual feature extraction,” 2025. [Online]. Available: https://arxiv.org/abs/2503.03734 

- [93] Z. Zhou, Y. Zhu, M. Zhu, J. Wen, N. Liu, Z. Xu, W. Meng, R. Cheng, Y. Peng, C. Shen, and F. Feng, “Chatvla: Unified multimodal understanding and robot control with vision-language-action model,” 2025. [Online]. Available: https://arxiv.org/abs/2502.14420 

- [94] Y.-J. Wang, B. Zhang, J. Chen, and K. Sreenath, “Prompt a robot to walk with large language models,” 2024. [Online]. Available: https://arxiv.org/abs/2309.09969 

- [95] C. Lynch, A. Wahid, J. Tompson, T. Ding, J. Betker, R. Baruch, T. Armstrong, and P. Florence, “Interactive language: Talking to robots in real time,” 2022. [Online]. Available: https://arxiv.org/abs/2210.06407 

- [96] G. Sarch, Y. Wu, M. J. Tarr, and K. Fragkiadaki, “Openended instructable embodied agents with memory-augmented large language models,” 2023. [Online]. Available: https: //arxiv.org/abs/2310.15127 

- [97] V. Berman, A. Bazhenov, S. Satsevich, and D. Tsetserukou, “Missiongpt: Mission planner for mobile robot based on robotics transformer model,” in _2024 2nd International Conference on Foundation and Large Language Models (FLLM)_ , 2024, pp. 201–206. 

- [98] H. Bharadhwaj, J. Vakil, M. Sharma, A. Gupta, S. Tulsiani, and V. Kumar, “Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking,” 2023. 

- [99] Y. Hu, F. Lin, T. Zhang, L. Yi, and Y. Gao, “Look before you leap: Unveiling the power of gpt-4v in robotic vision-language planning,” 2023. [Online]. Available: https: //arxiv.org/abs/2311.17842 

- [100] L. Fan, K. Chen, Z. Xu, M. Yuan, P. Huang, and W. Huang, “Language reasoning in vision-language-action model for robotic grasping,” in _2024 China Automation Congress (CAC)_ , 2024, pp. 6656–6661. 

- [101] S. Nasiriany, S. Kirmani, T. Ding, L. Smith, Y. Zhu, D. Driess, D. Sadigh, and T. Xiao, “Rt-affordance: Affordances are versatile 

24 

   - intermediate representations for robot manipulation,” 2024. [Online]. Available: https://arxiv.org/abs/2411.02704 

- [102] Y. Wu, R. Tian, G. Swamy, and A. Bajcsy, “From foresight to forethought: Vlm-in-the-loop policy steering via latent alignment,” 2025. [Online]. Available: https://arxiv.org/abs/ 2502.01828 

- [103] W. Zhao, P. Ding, M. Zhang, Z. Gong, S. Bai, H. Zhao, and D. Wang, “Vlas: Vision-language-action model with speech instructions for customized robot manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2502.13508 

- [104] Z. Yang, Y. Chen, X. Zhou, J. Yan, D. Song, Y. Liu, Y. Li, Y. Zhang, P. Zhou, H. Chen, and L. Sun, “Agentic robot: A brain-inspired framework for vision-language-action models in embodied agents,” 2025. [Online]. Available: https://arxiv.org/abs/2505.23450 

- [105] T.-Y. Xiang, A.-Q. Jin, X.-H. Zhou, M.-J. Gui, X.-L. Xie, S.-Q. Liu, S.-Y. Wang, S.-B. Duang, S.-C. Wang, Z. Lei, and Z.-G. Hou, “Vla model-expert collaboration for bidirectional manipulation learning,” 2025. [Online]. Available: https://arxiv.org/abs/2503.04163 

- [106] J. Wei, S. Yuan, P. Li, Q. Hu, Z. Gan, and W. Ding, “Occllama: An occupancy-language-action generative world model for autonomous driving,” 2024. [Online]. Available: https://arxiv.org/abs/2409.03272 

- [107] P. Chen, P. Bu, Y. Wang, X. Wang, Z. Wang, J. Guo, Y. Zhao, Q. Zhu, J. Song, S. Yang, J. Wang, and B. Zheng, “Combatvla: An efficient vision-language-action model for combat tasks in 3d action role-playing games,” 2025. [Online]. Available: https://arxiv.org/abs/2503.09527 

- [108] M. Li, Z. Wang, K. He, X. Ma, and Y. Liang, “Jarvis-vla: Post-training large-scale vision language models to play visual games with keyboards and mouse,” 2025. [Online]. Available: https://arxiv.org/abs/2503.16365 

- [109] A. Stone, T. Xiao, Y. Lu, K. Gopalakrishnan, K.-H. Lee, Q. Vuong, P. Wohlhart, S. Kirmani, B. Zitkovich, F. Xia, C. Finn, and K. Hausman, “Open-world object manipulation using pre-trained vision-language models,” 2023. [Online]. Available: https://arxiv.org/abs/2303.00905 

- [110] T. Kwon, N. D. Palo, and E. Johns, “Language models as zero-shot trajectory generators,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 7, p. 6728–6735, Jul. 2024. [Online]. Available: http://dx.doi.org/10.1109/LRA.2024.3410155 

- [111] H. Li, S. Yang, Y. Chen, Y. Tian, X. Yang, X. Chen, H. Wang, T. Wang, F. Zhao, D. Lin, and J. Pang, “Cronusvla: Transferring latent motion across time for multi-frame prediction in manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/ 2506.19816 

- [112] J. Zhang, K. Wang, S. Wang, M. Li, H. Liu, S. Wei, Z. Wang, Z. Zhang, and H. Wang, “Uni-navid: A video-based visionlanguage-action model for unifying embodied navigation tasks,” 2025. [Online]. Available: https://arxiv.org/abs/2412.06224 

- [113] P. Ding, H. Zhao, W. Zhang, W. Song, M. Zhang, S. Huang, N. Yang, and D. Wang, “Quar-vla: Vision-language-action model for quadruped robots,” in _Computer Vision – ECCV 2024: 18th European Conference, Milan, Italy, September 29–October 4, 2024, Proceedings, Part V_ . Berlin, Heidelberg: Springer-Verlag, 2024, p. 352–367. [Online]. Available: https://doi.org/10.1007/ 978-3-031-72652-1 <u>21</u> 

- [114] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” 2023. [Online]. Available: https://arxiv.org/abs/2304.13705 

- [115] M. J. Kim, C. Finn, and P. Liang, “Fine-tuning vision-languageaction models: Optimizing speed and success,” 2025. [Online]. Available: https://arxiv.org/abs/2502.19645 

- [116] S. Ye, J. Jang, B. Jeon, S. J. Joo, J. Yang, B. Peng, A. Mandlekar, R. Tan, Y.-W. Chao, B. Y. Lin, L. Liden, K. Lee, J. Gao, L. Zettlemoyer, D. Fox, and M. Seo, “Latent action pretraining from videos,” in _The Thirteenth International Conference on Learning Representations_ , 2025. [Online]. Available: https://openreview.net/forum?id=VYOe2eBQeh 

- [117] F. Bartoccioni, E. Ramzi, V. Besnier, S. Venkataramanan, T.-H. Vu, Y. Xu, L. Chambon, S. Gidaris, S. Odabas, D. Hurych, R. Marlet, A. Boulch, M. Chen, ´Eloi Zablocki, A. Bursuc, E. Valle, and M. Cord, “Vavim and vavam: Autonomous driving through video generative modeling,” 2025. [Online]. Available: https://arxiv.org/abs/2502.15672 

- [118] K. Renz, L. Chen, E. Arani, and O. Sinavski, “Simlingo: Visiononly closed-loop autonomous driving with language-action alignment,” 2025. [Online]. Available: https://arxiv.org/abs/ 2503.09594 

- [119] H. Fu, D. Zhang, Z. Zhao, J. Cui, D. Liang, C. Zhang, D. Zhang, H. Xie, B. Wang, and X. Bai, “Orion: A holistic end-to-end autonomous driving framework by visionlanguage instructed action generation,” 2025. [Online]. Available: https://arxiv.org/abs/2503.19755 

- [120] A. Goyal, V. Blukis, J. Xu, Y. Guo, Y.-W. Chao, and D. Fox, “Rvt-2: Learning precise manipulation from few demonstrations,” 2024. [Online]. Available: https://arxiv.org/abs/2406.08545 

- [121] J. Lu, C. Clark, S. Lee, Z. Zhang, S. Khosla, R. Marten, D. Hoiem, and A. Kembhavi, “Unified-io 2: Scaling autoregressive multimodal models with vision, language, audio, and action,” 2023. [Online]. Available: https://arxiv.org/abs/2312.17172 

- [122] L. Fu, H. Huang, G. Datta, L. Y. Chen, W. C.-H. Panitch, F. Liu, H. Li, and K. Goldberg, “In-context imitation learning via next-token prediction,” 2024. [Online]. Available: https://arxiv.org/abs/2408.15980 

- [123] D. Niu, Y. Sharma, H. Xue, G. Biamby, J. Zhang, Z. Ji, T. Darrell, and R. Herzig, “Pre-training auto-regressive robotic models with 4d representations,” 2025. [Online]. Available: https://arxiv.org/abs/2502.13142 

- [124] P. Hao, C. Zhang, D. Li, X. Cao, X. Hao, S. Cui, and S. Wang, “Tla: Tactile-language-action model for contact-rich manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2503.08548 

- [125] I. Singh, A. Goyal, S. Birchfield, D. Fox, A. Garg, and V. Blukis, “Og-vla: 3d-aware vision language action model via orthographic image generation,” 2025. [Online]. Available: https://arxiv.org/abs/2506.01196 

- [126] J. Zhang, Y. Chen, Y. Xu, Z. Huang, Y. Zhou, Y. Yuan, X. Cai, G. Huang, X. Quan, H. Xu, and L. Zhang, “4d-vla: Spatiotemporal vision-language-action pretraining with cross-scene calibration,” _arXiv preprint arXiv:2506.22242_ , 2025. 

- [127] S. Haldar, Z. Peng, and L. Pinto, “Baku: An efficient transformer for multi-task policy learning,” 2024. [Online]. Available: https://arxiv.org/abs/2406.07539 

- [128] J. Zhang, Y. Guo, X. Chen, Y.-J. Wang, Y. Hu, C. Shi, and J. Chen, “HiRT: Enhancing robotic control with hierarchical robot transformers,” in _8th Annual Conference on Robot Learning_ , 2024. [Online]. Available: https://openreview.net/forum?id= wTKJge0PTq 

- [129] Z. Duan, Y. Zhang, S. Geng, G. Liu, J. Boedecker, and C. X. Lu, “Fast ecot: Efficient embodied chain-of-thought via thoughts reuse,” 2025. [Online]. Available: https://arxiv.org/abs/2506. 07639 

- [130] J. Urain, N. Funk, J. Peters, and G. Chalvatzaki, “Se(3)diffusionfields: Learning smooth cost functions for joint grasp and motion optimization through diffusion,” 2023. [Online]. Available: https://arxiv.org/abs/2209.03855 

- [131] Y. Du, M. Yang, B. Dai, H. Dai, O. Nachum, J. B. Tenenbaum, D. Schuurmans, and P. Abbeel, “Learning universal policies via text-guided video generation,” 2023. [Online]. Available: https://arxiv.org/abs/2302.00111 

- [132] W. Liu, Y. Du, T. Hermans, S. Chernova, and C. Paxton, “Structdiffusion: Language-guided creation of physically-valid structures using unseen objects,” 2023. [Online]. Available: https://arxiv.org/abs/2211.04604 

- [133] T.-W. Ke, N. Gkanatsios, and K. Fragkiadaki, “3d diffuser actor: Policy diffusion with 3d scene representations,” 2024. [Online]. Available: https://arxiv.org/abs/2402.10885 

- [134] P.-C. Ko, J. Mao, Y. Du, S.-H. Sun, and J. B. Tenenbaum, “Learning to act from actionless videos through dense correspondences,” in _The Twelfth International Conference on Learning Representations_ , 2024. [Online]. Available: https://openreview.net/forum?id= Mhb5fpA1T0 

- [135] S. Liu, L. Wu, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, and J. Zhu, “Rdt-1b: a diffusion foundation model for bimanual manipulation,” in _International Conference on Representation Learning_ , Y. Yue, A. Garg, N. Peng, F. Sha, and R. Yu, Eds., vol. 2025, 2025, pp. 29 982–30 009. [Online]. Available: https://proceedings.iclr.cc/paper <u>files/paper/2025/</u> file/49f80e4d2471ad4f2edf4f5f1ab62339-Paper-Conference.pdf 

- [136] Y. Niu, S. Zhou, Y. Li, Y. Den, and L. Wang, “Timeunified diffusion policy with action discrimination for robotic 

25 

manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/ 2506.09422 

- [137] J. Ma, Y. Qin, Y. Li, X. Liao, Y. Guo, and R. Zhang, “Cdp: Towards robust autoregressive visuomotor policy learning via causal diffusion,” 2025. [Online]. Available: https://arxiv.org/abs/2506.14769 

- [138] Z. Liang, Y. Li, T. Yang, C. Wu, S. Mao, L. Pei, X. Yang, J. Pang, Y. Mu, and P. Luo, “Discrete diffusion vla: Bringing discrete diffusion to action decoding in vision-language-action policies,” 2025. [Online]. Available: https://arxiv.org/abs/2508.20072 

- [139] Q. Li, “Task reconstruction and extrapolation for _π_ 0 using text latent,” 2025. [Online]. Available: https://arxiv.org/abs/2505. 03500 

- [140] K. Black, M. Nakamoto, P. Atreya, H. Walke, C. Finn, A. Kumar, and S. Levine, “Zero-shot robotic manipulation with pretrained image-editing diffusion models,” 2023. [Online]. Available: https://arxiv.org/abs/2310.10639 

- [141] M. Reuss, Omer<sup>¨</sup> Erdinc¸ Ya˘gmurlu, F. Wenzel, and R. Lioutikov, “Multimodal diffusion transformer: Learning versatile behavior from multimodal goals,” 2024. [Online]. Available: https: //arxiv.org/abs/2407.05996 

- [142] Q. Li, Y. Liang, Z. Wang, L. Luo, X. Chen, M. Liao, F. Wei, Y. Deng, S. Xu, Y. Zhang, X. Wang, B. Liu, J. Fu, J. Bao, D. Chen, Y. Shi, J. Yang, and B. Guo, “Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation,” 2024. [Online]. Available: https://arxiv.org/abs/2411.19650 

- [143] F. Ni, J. Hao, S. Wu, L. Kou, Y. Yuan, Z. Dong, J. Liu, M. Li, Y. Zhuang, and Y. Zheng, “Peria: Perceive, reason, imagine, act via holistic language and vision planning for manipulation,” in _Advances in Neural Information Processing Systems_ , A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, Eds., vol. 37. Curran Associates, Inc., 2024, pp. 17 541–17 571. [Online]. Available: https://proceedings.neurips.cc/paper <u>files/paper/2024/</u> file/1f6af963e891e7efa229c24a1607fa7f-Paper-Conference.pdf 

- [144] J. Li, Y. Zhu, Z. Tang, J. Wen, M. Zhu, X. Liu, C. Li, R. Cheng, Y. Peng, and F. Feng, “Improving vision-languageaction models via chain-of-affordance,” 2024. [Online]. Available: https://arxiv.org/abs/2412.20451 

- [145] H. Bharadhwaj, R. Mottaghi, A. Gupta, and S. Tulsiani, “Track2act: Predicting point tracks from internet videos enables generalizable robot manipulation,” 2024. [Online]. Available: https://arxiv.org/abs/2405.01527 

- [146] Z. Hou, T. Zhang, Y. Xiong, H. Duan, H. Pu, R. Tong, C. Zhao, X. Zhu, Y. Qiao, J. Dai _et al._ , “Dita: Scaling diffusion transformer for generalist vision-language-action policy,” _arXiv preprint arXiv:2503.19757_ , 2025. 

- [147] J. Yu, H. Liu, Q. Yu, J. Ren, C. Hao, H. Ding, G. Huang, G. Huang, Y. Song, P. Cai _et al._ , “Forcevla: Enhancing vla models with a force-aware moe for contact-rich manipulation,” _arXiv preprint arXiv:2505.22159_ , 2025. 

- [148] A. Sridhar, D. Shah, C. Glossop, and S. Levine, “Nomad: Goal masked diffusion policies for navigation and exploration,” 2023. [Online]. Available: https://arxiv.org/abs/2310.07896 

- [149] J. Wen, Y. Zhu, J. Li, M. Zhu, K. Wu, Z. Xu, N. Liu, R. Cheng, C. Shen, Y. Peng, F. Feng, and J. Tang, “Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2409.12514 

- [150] M. Shukor, D. Aubakirova, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, C. Pascal, M. Russi, A. Marafioti, S. Alibert, M. Cord, T. Wolf, and R. Cadene, “Smolvla: A visionlanguage-action model for affordable and efficient robotics,” 2025. [Online]. Available: https://arxiv.org/abs/2506.01844 

- [151] Y. Wang, H. Zhu, M. Liu, J. Yang, H.-S. Fang, and T. He, “Vq-vla: Improving vision-language-action models via scaling vector-quantized action tokenizers,” 2025. [Online]. Available: https://arxiv.org/abs/2507.01016 

- [152] J. He, D. Li, X. Yu, Z. Qi, W. Zhang, J. Chen, Z. Zhang, Z. Zhang, L. Yi, and H. Wang, “Dexvlg: Dexterous visionlanguage-grasp model at scale,” 2025. [Online]. Available: https://arxiv.org/abs/2507.02747 

- [153] S. Chen, J. Liu, S. Qian, H. Jiang, L. Li, R. Zhang, Z. Liu, C. Gu, C. Hou, P. Wang _et al._ , “Ac-dit: Adaptive coordination diffusion transformer for mobile manipulation,” _arXiv preprint arXiv:2507.01961_ , 2025. 

- [154] J. Wen, Y. Zhu, J. Li, Z. Tang, C. Shen, and F. Feng, “Dexvla: Vision-language model with plug-in diffusion expert for general robot control,” 2025. [Online]. Available: https: //arxiv.org/abs/2502.05855 

- [155] X. Chi, K. Ge, J. Liu, S. Zhou, P. Jia, Z. He, Y. Liu, T. Li, L. Han, S. Han, S. Zhang, and Y. Guo, “Mind: Unified visual imagination and control via hierarchical world models,” 2025. [Online]. Available: https://arxiv.org/abs/2506.18897 

- [156] H. Song, D. Qu, Y. Yao, Q. Chen, Q. Lv, Y. Tang, M. Shi, G. Ren, M. Yao, B. Zhao, D. Wang, and X. Li, “Hume: Introducing system-2 thinking in visual-language-action model,” 2025. [Online]. Available: https://arxiv.org/abs/2505.21432 

- [157] Z. Liu, Y. Gu, S. Zheng, X. Xue, and Y. Fu, “Trivla: A triple-system-based unified vision-language-action model for general robot control,” 2025. [Online]. Available: https: //arxiv.org/abs/2507.01424 

- [158] A. J. Hancock, A. Z. Ren, and A. Majumdar, “Run-time observation interventions make vision-language-action models more visually robust,” in _1st Workshop on Safely Leveraging Vision-Language Foundation Models in Robotics: Challenges and Opportunities_ , 2025. [Online]. Available: https://openreview.net/ forum?id=PAX7FjvyYf 

- [159] W. Zhang, H. Liu, Z. Qi, Y. Wang, X. Yu, J. Zhang, R. Dong, J. He, H. Wang, Z. Zhang, L. Yi, W. Zeng, and X. Jin, “Dreamvla: A vision-language-action model dreamed with comprehensive world knowledge,” _CoRR_ , vol. abs/2507.04447, 2025. [Online]. Available: https://doi.org/10.48550/arXiv.2507.04447 

- [160] H. Zhang, P. Ding, S. Lyu, Y. Peng, and D. Wang, “Gevrm: Goal-expressive video generation model for robust visual manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/ 2502.09268 

- [161] Z. Yang, Y. Chai, X. Jia, Q. Li, Y. Shao, X. Zhu, H. Su, and J. Yan, “Drivemoe: Mixture-of-experts for vision-language-action model in end-to-end autonomous driving,” 2025. [Online]. Available: https://arxiv.org/abs/2505.16278 

- [162] J. Jang, S. Ye, Z. Lin, J. Xiang, J. Bjorck, Y. Fang, F. Hu, S. Huang, K. Kundalia, Y.-C. Lin, L. Magne, A. Mandlekar, A. Narayan, Y. L. Tan, G. Wang, J. Wang, Q. Wang, Y. Xu, X. Zeng, K. Zheng, R. Zheng, M.-Y. Liu, L. Zettlemoyer, D. Fox, J. Kautz, S. Reed, Y. Zhu, and L. Fan, “Dreamgen: Unlocking generalization in robot learning through video world models,” 2025. [Online]. Available: https://arxiv.org/abs/2505.12705 

- [163] S. Huang, L. Chen, P. Zhou, S. Chen, Z. Jiang, Y. Hu, Y. Liao, P. Gao, H. Li, M. Yao _et al._ , “Enerverse: Envisioning embodied future space for robotics manipulation,” _arXiv preprint arXiv:2501.01895_ , 2025. 

- [164] H. Chen, B. Sun, A. Zhang, M. Pollefeys, and S. Leutenegger, “Vidbot: Learning generalizable 3d actions from in-the-wild 2d human videos for zero-shot robotic manipulation,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 27 661–27 672. 

- [165] S. Wang, J. Zhang, M. Li, J. Liu, A. Li, K. Wu, F. Zhong, J. Yu, Z. Zhang, and H. Wang, “Trackvla: Embodied visual tracking in the wild,” 2025. [Online]. Available: https://arxiv.org/abs/2505.23189 

- [166] R. Yang, G. Chen, C. Wen, and Y. Gao, “Fp3: A 3d foundation policy for robotic manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2503.08950 

- [167] NVIDIA, :, J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. J. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, J. Jang, Z. Jiang, J. Kautz, K. Kundalia, L. Lao, Z. Li, Z. Lin, K. Lin, G. Liu, E. Llontop, L. Magne, A. Mandlekar, A. Narayan, S. Nasiriany, S. Reed, Y. L. Tan, G. Wang, Z. Wang, J. Wang, Q. Wang, J. Xiang, Y. Xie, Y. Xu, Z. Xu, S. Ye, Z. Yu, A. Zhang, H. Zhang, Y. Zhao, R. Zheng, and Y. Zhu, “Gr00t n1: An open foundation model for generalist humanoid robots,” 2025. [Online]. Available: https://arxiv.org/abs/2503.14734 

- [168] M. Zhu, Y. Zhu, J. Li, Z. Zhou, J. Wen, X. Liu, C. Shen, Y. Peng, and F. Feng, “Objectvla: End-to-end open-world object manipulation without demonstration,” 2025. [Online]. Available: https://arxiv.org/abs/2502.19250 

- [169] M. Li, Z. Zhao, Z. Che, F. Liao, K. Wu, Z. Xu, P. Ren, Z. Jin, N. Liu, and J. Tang, “Switchvla: Execution-aware task switching for vision-language-action models,” 2025. [Online]. Available: https://arxiv.org/abs/2506.03574 

- [170] R. Xu, J. Zhang, M. Guo, Y. Wen, H. Yang, M. Lin, J. Huang, Z. Li, K. Zhang, L. Wang _et al._ , “A0: An affordance-aware hier- 

26 

archical model for general robotic manipulation,” _arXiv preprint arXiv:2504.12636_ , 2025. 

- [171] K. Ranasinghe, X. Li, C. Mata, J. Park, and M. S. Ryoo, “Pixel motion as universal representation for robot control,” 2025. [Online]. Available: https://arxiv.org/abs/2505.07817 

- [172] T. Lin, G. Li, Y. Zhong, Y. Zou, and B. Zhao, “Evo-0: Visionlanguage-action model with implicit spatial understanding,” _arXiv preprint arXiv:2507.00416_ , 2025. 

- [173] Z. Hou, T. Zhang, Y. Xiong, H. Pu, C. Zhao, R. Tong, Y. Qiao, J. Dai, and Y. Chen, “Diffusion transformer policy,” 2025. [Online]. Available: https://arxiv.org/abs/2410.15959 

- [174] Y. J. Ma, S. Sodhani, D. Jayaraman, O. Bastani, V. Kumar, and A. Zhang, “Vip: Towards universal visual reward and representation via value-implicit pre-training,” 2023. [Online]. Available: https://arxiv.org/abs/2210.00030 

- [175] Y. J. Ma, W. Liang, V. Som, V. Kumar, A. Zhang, O. Bastani, and D. Jayaraman, “Liv: Language-image representations and rewards for robotic control,” 2023. [Online]. Available: https://arxiv.org/abs/2306.00958 

- [176] W. Chen, O. Mees, A. Kumar, and S. Levine, “Visionlanguage models provide promptable representations for reinforcement learning,” 2024. [Online]. Available: https: //arxiv.org/abs/2402.02651 

- [177] A. Peng, B. Z. Li, I. Sucholutsky, N. Kumar, J. A. Shah, J. Andreas, and A. Bobu, “Adaptive language-guided abstraction from contrastive explanations,” 2024. [Online]. Available: https://arxiv.org/abs/2409.08212 

- [178] Z. Zhang, K. Zheng, Z. Chen, J. Jang, Y. Li, C. Wang, M. Ding, D. Fox, and H. Yao, “Grape: Generalizing robot policy via preference alignment,” 2024. [Online]. Available: https://arxiv.org/abs/2411.19309 

- [179] C. Xu, Q. Li, J. Luo, and S. Levine, “Rldg: Robotic generalist policy distillation via reinforcement learning,” 2024. [Online]. Available: https://arxiv.org/abs/2412.09858 

- [180] L. Chen, N. Moorman, and M. Gombolay, “Elemental: Interactive learning from demonstrations and vision-language models for reward design in robotics,” 2025. [Online]. Available: https://arxiv.org/abs/2411.18825 

- [181] A.-C. Cheng, Y. Ji, Z. Yang, Z. Gongye, X. Zou, J. Kautz, E. Bıyık, H. Yin, S. Liu, and X. Wang, “Navila: Legged robot vision-language-action model for navigation,” 2025. [Online]. Available: https://arxiv.org/abs/2412.04453 

- [182] B. Zhang, Y. Zhang, J. Ji, Y. Lei, J. Dai, Y. Chen, and Y. Yang, “Safevla: Towards safety alignment of vision-language-action model via constrained learning,” 2025. [Online]. Available: https://arxiv.org/abs/2503.03480 

- [183] Y. Guo, J. Zhang, X. Chen, X. Ji, Y.-J. Wang, Y. Hu, and J. Chen, “Improving vision-language-action model with online reinforcement learning,” 2025. [Online]. Available: https://arxiv.org/abs/2501.16664 

- [184] H. Zhang, Z. Zhuang, H. Zhao, P. Ding, H. Lu, and D. Wang, “Reinbot: Amplifying robot visual-language manipulation with reinforcement learning,” 2025. [Online]. Available: https: //arxiv.org/abs/2505.07395 

- [185] Y. Chen, S. Tian, S. Liu, Y. Zhou, H. Li, and D. Zhao, “Conrft: A reinforced fine-tuning method for vla models via consistency policy,” _arXiv preprint arXiv:2502.05450_ , 2025. 

- [186] H. Zhao, W. Song, D. Wang, X. Tong, P. Ding, X. Cheng, and Z. Ge, “More: Unlocking scalability in reinforcement learning for quadruped vision-language-action models,” 2025. [Online]. Available: https://arxiv.org/abs/2503.08007 

- [187] SimpleVLA-RL Team, “Simplevla-rl: Online rl with simple reward enables training vla models with only one trajectory,” https: //github.com/PRIME-RL/SimpleVLA-RL, 2025, gitHub repository. 

- [188] H. Xue, X. Huang, D. Niu, Q. Liao, T. Kragerud, J. T. Gravdahl, X. B. Peng, G. Shi, T. Darrell, K. Screenath, and S. Sastry, “Leverb: Humanoid whole-body control with latent vision-language instruction,” 2025. [Online]. Available: https://arxiv.org/abs/2506.13751 

- [189] Z. Zhou, T. Cai, Y. Zhao, Seth Z.and Zhang, Z. Huang, B. Zhou, and J. Ma, “Autovla: A vision-language-action model for end-toend autonomous driving with adaptive reasoning and reinforcement fine-tuning,” _arXiv preprint arXiv:2506.13757_ , 2025. 

- [190] T. J¨ulg, W. Burgard, and F. Walter, “Refined policy distillation: From vla generalists to rl experts,” _arXiv preprint arXiv:2503.05833_ , 2025. 

- [191] Y. Chen and X. Li, “Rlrc: Reinforcement learning-based recovery for compressed vision-language-action models,” 2025. [Online]. Available: https://arxiv.org/abs/2506.17639 

- [192] G. Lu, W. Guo, C. Zhang, Y. Zhou, H. Jiang, Z. Gao, Y. Tang, and Z. Wang, “Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning,” 2025. [Online]. Available: https://arxiv.org/abs/2505.18719 

- [193] Z. Yuan, J. Tang, J. Luo, R. Chen, C. Qian, L. Sun, X. Chu, Y. Cai, D. Zhang, and S. Li, “Autodrive-r<sup>2</sup> : Incentivizing reasoning and self-reflection capacity for vla model in autonomous driving,” 2025. [Online]. Available: https://arxiv.org/abs/2509.01944 

- [194] J. Zhang, Y. Luo, A. Anwar, S. A. Sontakke, J. J. Lim, J. Thomason, E. Biyik, and J. Zhang, “Rewind: Language-guided rewards teach robot policies without new demonstrations,” 2025. [Online]. Available: https://arxiv.org/abs/2505.10911 

- [195] Y. Yuan, H. Cui, Y. Huang, Y. Chen, F. Ni, Z. Dong, P. Li, Y. Zheng, and J. Hao, “Embodied-r1: Reinforced embodied reasoning for general robotic manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2508.13998 

- [196] A. Jiang, Y. Gao, Y. Wang, Z. Sun, S. Wang, Y. Heng, H. Sun, S. Tang, L. Zhu, J. Chai, J. Wang, Z. Gu, H. Jiang, and L. Sun, “Irl-vla: Training an vision-language-action policy via reward world model,” 2025. [Online]. Available: https://arxiv.org/abs/2508.06571 

- [197] C.-P. Huang, Y.-H. Wu, M.-H. Chen, Y.-C. F. Wang, and F.-E. Yang, “Thinkact: Vision-language-action reasoning via reinforced visual latent planning,” 2025. [Online]. Available: https://arxiv.org/abs/2507.16815 

- [198] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” 2017. [Online]. Available: https://arxiv.org/abs/1707.06347 

- [199] S. Bahl, R. Mendonca, L. Chen, U. Jain, and D. Pathak, “Affordances from human videos as a versatile representation for robotics,” 2023. [Online]. Available: https://arxiv.org/abs/ 2304.08488 

- [200] L. X. Shi, Z. Hu, T. Z. Zhao, A. Sharma, K. Pertsch, J. Luo, S. Levine, and C. Finn, “Yell at your robot: Improving on-the-fly from language corrections,” 2024. [Online]. Available: https://arxiv.org/abs/2403.12910 

- [201] J. Liu, H. Chen, P. An, Z. Liu, R. Zhang, C. Gu, X. Li, Z. Guo, S. Chen, M. Liu, C. Hou, M. Zhao, K. alex Zhou, P.-A. Heng, and S. Zhang, “Hybridvla: Collaborative diffusion and autoregression in a unified vision-language-action model,” 2025. [Online]. Available: https://arxiv.org/abs/2503.10631 

- [202] W. Song, J. Chen, W. Li, X. He, H. Zhao, C. Cui, P. D. S. Su, F. Tang, X. Cheng, D. Wang, Z. Ge, X. Zheng, Z. Liu, H. Wang, and H. Li, “Rationalvla: A rational vision-languageaction model with dual system,” 2025. [Online]. Available: https://arxiv.org/abs/2506.10826 

- [203] C. Cui, P. Ding, W. Song, S. Bai, X. Tong, Z. Ge, R. Suo, W. Zhou, Y. Liu, B. Jia _et al._ , “Openhelix: A short survey, empirical analysis, and open-source dual-system vla model for robotic manipulation,” _arXiv preprint arXiv:2505.03912_ , 2025. 

- [204] R. Yang, Q. Yu, Y. Wu, R. Yan, B. Li, A.-C. Cheng, X. Zou, Y. Fang, X. Cheng, R.-Z. Qiu, H. Yin, S. Liu, S. Han, Y. Lu, and X. Wang, “Egovla: Learning vision-language-action models from egocentric human videos,” 2025. [Online]. Available: https://arxiv.org/abs/2507.12440 

- [205] J. Bi, L. B. Wen, Z. Liu, and C. Xu, “Actllm: Action consistency tuned large language model,” 2025. [Online]. Available: https://arxiv.org/abs/2506.21250 

- [206] M. Shridhar, L. Manuelli, and D. Fox, “Cliport: What and where pathways for robotic manipulation,” 2021. [Online]. Available: https://arxiv.org/abs/2109.12098 

- [207] H. Zhen, X. Qiu, P. Chen, J. Yang, X. Yan, Y. Du, Y. Hong, and C. Gan, “3d-vla: A 3d vision-languageaction generative world model,” 2024. [Online]. Available: https://arxiv.org/abs/2403.09631 

- [208] W. Huang, C. Wang, Y. Li, R. Zhang, and L. Fei-Fei, “Rekep: Spatio-temporal reasoning of relational keypoint constraints for robotic manipulation,” 2024. [Online]. Available: https://arxiv.org/abs/2409.01652 

- [209] W. Yuan, J. Duan, V. Blukis, W. Pumacay, R. Krishna, A. Murali, A. Mousavian, and D. Fox, “Robopoint: A vision-language model for spatial affordance prediction for robotics,” 2024. [Online]. Available: https://arxiv.org/abs/2406.10721 

27 

- [210] A. Szot, B. Mazoure, H. Agrawal, D. Hjelm, Z. Kira, and A. Toshev, “Grounding multimodal large language models in actions,” 2024. [Online]. Available: https://arxiv.org/abs/2406. 07904 

- [211] P. Li, Y. Chen, H. Wu, X. Ma, X. Wu, Y. Huang, L. Wang, T. Kong, and T. Tan, “Bridgevla: Input-output alignment for efficient 3d manipulation learning with vision-language models,” 2025. [Online]. Available: https://arxiv.org/abs/2506.07961 

- [212] W. Tang, J.-H. Pan, Y.-H. Liu, M. Tomizuka, L. E. Li, C.-W. Fu, and M. Ding, “Geomanip: Geometric constraints as general interfaces for robot manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2501.09783 

- [213] C. Liu, J. Zhang, C. Li, Z. Zhou, S. Wu, S. Huang, and H. Duan, “Ttf-vla: Temporal token fusion via pixel-attention integration for vision-language-action models,” 2025. [Online]. Available: https://arxiv.org/abs/2508.19257 

- [214] H. Shi, B. Xie, Y. Liu, L. Sun, F. Liu, T. Wang, E. Zhou, H. Fan, X. Zhang, and G. Huang, “Memoryvla: Perceptualcognitive memory in vision-language-action models for robotic manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/ 2508.19236 

- [215] Z. Chen, S. Kiami, A. Gupta, and V. Kumar, “Genaug: Retargeting behaviors to unseen situations via generative augmentation,” 2023. [Online]. Available: https://arxiv.org/abs/2302.06671 

- [216] T. Yu, T. Xiao, A. Stone, J. Tompson, A. Brohan, S. Wang, J. Singh, C. Tan, D. M, J. Peralta, B. Ichter, K. Hausman, and F. Xia, “Scaling robot learning with semantically imagined experience,” 2023. [Online]. Available: https://arxiv.org/abs/2302.11550 

- [217] H. Arai, K. Miwa, K. Sasaki, Y. Yamaguchi, K. Watanabe, S. Aoki, and I. Yamamoto, “Covla: Comprehensive vision-languageaction dataset for autonomous driving,” 2024. [Online]. Available: https://arxiv.org/abs/2408.10845 

- [218] A. Figure, “Helix: A vision-language-action model for generalist humanoid control,” _Figure AI News_ , 2024. 

- [219] M. Ahn, D. Dwibedi, C. Finn, M. G. Arenas, K. Gopalakrishnan, K. Hausman, B. Ichter, A. Irpan, N. Joshi, R. Julian, S. Kirmani, I. Leal, E. Lee, S. Levine, Y. Lu, I. Leal, S. Maddineni, K. Rao, D. Sadigh, P. Sanketi, P. Sermanet, Q. Vuong, S. Welker, F. Xia, T. Xiao, P. Xu, S. Xu, and Z. Xu, “Autort: Embodied foundation models for large scale orchestration of robotic agents,” 2024. [Online]. Available: https://arxiv.org/abs/2401.12963 

- [220] Z. Wu, Y. Zhou, X. Xu, Z. Wang, and H. Yan, “Momanipvla: Transferring vision-language-action models for general mobile manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/ 2503.13446 

- [221] F. Wang, X. Yu, and W. Wu, “Cuberobot: Grounding language in rubik’s cube manipulation via vision-language model,” in _Companion Proceedings of the ACM on Web Conference 2025_ , 2025, pp. 2181–2186. 

- [222] T. Wang, C. Han, J. C. Liang, W. Yang, D. Liu, L. X. Zhang, Q. Wang, J. Luo, and R. Tang, “Exploring the adversarial vulnerabilities of vision-language-action models in robotics,” 2025. [Online]. Available: https://arxiv.org/abs/2411.13587 

- [223] S. Nair, A. Rajeswaran, V. Kumar, C. Finn, and A. Gupta, “R3m: A universal visual representation for robot manipulation,” 2022. [Online]. Available: https://arxiv.org/abs/2203.12601 

- [224] Z. Mandi, H. Bharadhwaj, V. Moens, S. Song, A. Rajeswaran, and V. Kumar, “Cacti: A framework for scalable multi-task multi-scene visual imitation learning,” 2023. [Online]. Available: https://arxiv.org/abs/2212.05711 

- [225] A. Majumdar, K. Yadav, S. Arnaud, Y. J. Ma, C. Chen, S. Silwal, A. Jain, V.-P. Berges, P. Abbeel, J. Malik, D. Batra, Y. Lin, O. Maksymets, A. Rajeswaran, and F. Meier, “Where are we in the search for an artificial visual cortex for embodied intelligence?” 2024. [Online]. Available: https://arxiv.org/abs/2303.18240 

- [226] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis, P. D. Fagan, J. Hejna, M. Itkina, M. Lepert, Y. J. Ma, P. T. Miller, J. Wu, S. Belkhale, S. Dass, H. Ha, A. Jain, A. Lee, Y. Lee, M. Memmel, S. Park, I. Radosavovic, K. Wang, A. Zhan, K. Black, C. Chi, K. B. Hatch, S. Lin, J. Lu, J. Mercat, A. Rehman, P. R. Sanketi, A. Sharma, C. Simpson, Q. Vuong, H. R. Walke, B. Wulfe, T. Xiao, J. H. Yang, A. Yavary, T. Z. Zhao, C. Agia, R. Baijal, M. G. Castro, D. Chen, Q. Chen, T. Chung, J. Drake, E. P. Foster, J. Gao, V. Guizilini, D. A. Herrera, M. Heo, K. Hsu, J. Hu, M. Z. Irshad, D. Jackson, C. Le, Y. Li, K. Lin, R. Lin, Z. Ma, A. Maddukuri, S. Mirchandani, D. Morton, T. Nguyen, A. O’Neill, R. Scalise, 

   - D. Seale, V. Son, S. Tian, E. Tran, A. E. Wang, Y. Wu, A. Xie, J. Yang, P. Yin, Y. Zhang, O. Bastani, G. Berseth, J. Bohg, K. Goldberg, A. Gupta, A. Gupta, D. Jayaraman, J. J. Lim, J. Malik, R. Mart´ın-Mart´ın, S. Ramamoorthy, D. Sadigh, S. Song, J. Wu, M. C. Yip, Y. Zhu, T. Kollar, S. Levine, and C. Finn, “Droid: A large-scale in-the-wild robot manipulation dataset,” 2025. [Online]. Available: https://arxiv.org/abs/2403.12945 

- [227] C. Chen, Q. Yang, X. Xu, N. Fazeli, and O. Andersson, “Visa-flow: Accelerating robot skill learning via large-scale video semantic action flow,” _arXiv preprint arXiv:2505.01288_ , 2025. 

- [228] W. Zhang, Y. Li, Y. Qiao, S. Huang, J. Liu, F. Dayoub, X. Ma, and L. Liu, “Effective tuning strategies for generalist robot manipulation policies,” 2024. [Online]. Available: https: //arxiv.org/abs/2410.01220 

- [229] W. Chen, S. Belkhale, S. Mirchandani, O. Mees, D. Driess, K. Pertsch, and S. Levine, “Training strategies for efficient embodied reasoning,” _arXiv preprint arXiv:2505.08243_ , 2025. 

- [230] C. Glossop, W. Chen, A. Bhorkar, D. Shah, and S. Levine, “Cast: Counterfactual labels improve instruction following in vision-language-action models,” 2025. [Online]. Available: https://arxiv.org/abs/2508.13446 

- [231] Y. Ji, H. Tan, J. Shi, X. Hao, Y. Zhang, H. Zhang, P. Wang, M. Zhao, Y. Mu, P. An, X. Xue, Q. Su, H. Lyu, X. Zheng, J. Liu, Z. Wang, and S. Zhang, “Robobrain: A unified brain model for robotic manipulation from abstract to concrete,” 2025. [Online]. Available: https://arxiv.org/abs/2502.21257 

- [232] P. Budzianowski, W. Maa, M. Freed, J. Mo, W. Hsiao, A. Xie, T. Młoduchowski, V. Tipnis, and B. Bolte, “Edgevla: Efficient vision-language-action models,” _arXiv preprint arXiv:2507.14049_ , 2025. 

- [233] Y. Yue, Y. Wang, B. Kang, Y. Han, S. Wang, S. Song, J. Feng, and G. Huang, “Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution,” 2024. [Online]. Available: https://arxiv.org/abs/2411.02359 

- [234] B. Han, J. Kim, and J. Jang, “A dual process vla: Efficient robotic manipulation leveraging vlm,” 2024. [Online]. Available: https://arxiv.org/abs/2410.15549 

- [235] W. Song, J. Chen, P. Ding, Y. Huang, H. Zhao, D. Wang, and H. Li, “Ceed-vla: Consistency vision-language-action model with early-exit decoding,” 2025. [Online]. Available: https://arxiv.org/abs/2506.13725 

- [236] J. Liu, M. Liu, Z. Wang, P. An, X. Li, K. Zhou, S. Yang, R. Zhang, Y. Guo, and S. Zhang, “Robomamba: Efficient vision-languageaction model for robotic reasoning and manipulation,” 2024. [Online]. Available: https://arxiv.org/abs/2406.04339 

- [237] S. Dey, J.-N. Zaech, N. Nikolov, L. V. Gool, and D. P. Paudel, “Revla: Reverting visual domain limitation of robotic foundation models,” 2025. [Online]. Available: https://arxiv.org/abs/2409. 15250 

- [238] Q. Gu, Y. Ju, S. Sun, I. Gilitschenski, H. Nishimura, M. Itkina, and F. Shkurti, “Safe: Multitask failure detection for vision-language-action models,” 2025. [Online]. Available: https://arxiv.org/abs/2506.09937 

- [239] J. Lyu, Z. Li, X. Shi, C. Xu, Y. Wang, and H. Wang, “Dywa: Dynamics-adaptive world action model for generalizable nonprehensile manipulation,” 2025. [Online]. Available: https: //arxiv.org/abs/2503.16806 

- [240] X. Li, L. Xu, M. Zhang, J. Liu, Y. Shen, I. Ponomarenko, J. Xu, L. Heng, S. Huang, S. Zhang, and H. Dong, “Crayonrobo: Object-centric prompt-driven vision-languageaction model for robotic manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2505.02166 

- [241] M. Argus, J. Bratulic, H. Masnavi, M. Velikanov, N. Heppert, A. Valada, and T. Brox, “cvla: Towards efficient camera-space vlas,” _arXiv preprint arXiv:2507.02190_ , 2025. 

- [242] K. Black, M. Y. Galliker, and S. Levine, “Real-time execution of action chunking flow policies,” 2025. [Online]. Available: https://arxiv.org/abs/2506.07339 

- [243] H. Chen, J. Liu, C. Gu, Z. Liu, R. Zhang, X. Li, X. He, Y. Guo, C.-W. Fu, S. Zhang, and P.-A. Heng, “Fast-in-slow: A dual-system foundation model unifying fast manipulation within slow reasoning,” 2025. [Online]. Available: https://arxiv.org/abs/2506.01953 

- [244] M. Zhu, Y. Zhu, J. Li, J. Wen, Z. Xu, N. Liu, R. Cheng, C. Shen, Y. Peng, F. Feng, and J. Tang, “Scaling diffusion policy in transformer to 1 billion parameters for robotic manipulation,” 2024. [Online]. Available: https://arxiv.org/abs/2409.14411 

28 

- [245] W. Huang, C. Wang, R. Zhang, Y. Li, J. Wu, and L. FeiFei, “Voxposer: Composable 3d value maps for robotic manipulation with language models,” 2023. [Online]. Available: https://arxiv.org/abs/2307.05973 

- [246] F. Liu, F. Yan, L. Zheng, C. Feng, Y. Huang, and L. Ma, “Robouniview: Visual-language model with unified view representation for robotic manipulation,” 2024. [Online]. Available: https://arxiv.org/abs/2406.18977 

- [247] K. Q. Lin, L. Li, D. Gao, Z. Yang, S. Wu, Z. Bai, W. Lei, L. Wang, and M. Z. Shou, “Showui: One vision-languageaction model for gui visual agent,” 2024. [Online]. Available: https://arxiv.org/abs/2411.17465 

- [248] J. Gao, B. Sarkar, F. Xia, T. Xiao, J. Wu, B. Ichter, A. Majumdar, and D. Sadigh, “Physically grounded visionlanguage models for robotic manipulation,” 2024. [Online]. Available: https://arxiv.org/abs/2309.02561 

- [249] Z. Xu, K. Wu, J. Wen, J. Li, N. Liu, Z. Che, and J. Tang, “A survey on robotics with foundation models: toward embodied ai,” 2024. [Online]. Available: https://arxiv.org/abs/2402.02385 

- [250] C. Yuan, C. Wen, T. Zhang, and Y. Gao, “General flow as foundation affordance for scalable robot learning,” in _8th Annual Conference on Robot Learning_ , 2024. [Online]. Available: https://openreview.net/forum?id=nmEt0ci8hi 

- [251] D. Driess, J. T. Springenberg, B. Ichter, L. Yu, A. Li-Bell, K. Pertsch, A. Z. Ren, H. Walke, Q. Vuong, L. X. Shi, and S. Levine, “Knowledge insulating vision-language-action models: Train fast, run fast, generalize better,” 2025. [Online]. Available: https://arxiv.org/abs/2505.23705 

- [252] H. Cheng, E. Xiao, C. Yu, Z. Yao, J. Cao, Q. Zhang, J. Wang, M. Sun, K. Xu, J. Gu, and R. Xu, “Manipulation facing threats: Evaluating physical vulnerabilities in end-to-end vision language action models,” 2024. [Online]. Available: https://arxiv.org/abs/2409.13174 

- [253] H. Lu, H. Li, P. S. Shahani, S. Herbers, and M. Scheutz, “Probing a vision-language-action model for symbolic states and integration into a cognitive architecture,” 2025. [Online]. Available: https://arxiv.org/abs/2502.04558 

- [254] T.-Y. Xiang, A.-Q. Jin, X.-H. Zhou, M.-J. Gui, X.-L. Xie, S.-Q. Liu, S.-Y. Wang, S.-B. Duang, S.-C. Wang, Z. Lei _et al._ , “Vla modelexpert collaboration for bi-directional manipulation learning,” _arXiv preprint arXiv:2503.04163_ , 2025. 

- [255] P. Zhi, Z. Zhang, Y. Zhao, M. Han, Z. Zhang, Z. Li, Z. Jiao, B. Jia, and S. Huang, “Closed-loop open-vocabulary mobile manipulation with gpt-4v,” 2025. [Online]. Available: https://arxiv.org/abs/2404.10220 

- [256] P.-L. Guhur, S. Chen, R. Garcia, M. Tapaswi, I. Laptev, and C. Schmid, “Instruction-driven history-aware policies for robotic manipulations,” 2022. [Online]. Available: https: //arxiv.org/abs/2209.04899 

- [257] D. Li, B. Peng, C. Li, N. Qiao, Q. Zheng, L. Sun, Y. Qin, B. Li, Y. Luan, B. Wu, Y. Zhan, M. Sun, T. Xu, L. Li, H. Shen, and X. He, “An atomic skill library construction method for data-efficient embodied manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2501.15068 

- [258] H. Huang, X. Chen, Y. Chen, H. Li, X. Han, Z. Wang, T. Wang, J. Pang, and Z. Zhao, “Roboground: Robotic manipulation with grounded vision-language priors,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 22 540–22 550. 

- [259] P. Sharma, L. Mohan, L. Pinto, and A. Gupta, “Multiple interactions made easy (mime): Large scale demonstrations data for imitation,” _Proceedings of Machine Learning Research_ , vol. 87, pp. 906– 915, 2018, publisher Copyright: © CoRL 2018. All rights reserved.; 2nd Conference on Robot Learning, CoRL 2018 ; Conference date: 29-10-2018 Through 31-10-2018. 

- [260] D. Damen, H. Doughty, G. M. Farinella, S. Fidler, A. Furnari, E. Kazakos, D. Moltisanti, J. Munro, T. Perrett, W. Price, and M. Wray, “Scaling egocentric vision: The epic-kitchens dataset,” 2018. [Online]. Available: https://arxiv.org/abs/1804.02748 

- [261] S. Dasari, F. Ebert, S. Tian, S. Nair, B. Bucher, K. Schmeckpeper, S. Singh, S. Levine, and C. Finn, “Robonet: Large-scale multirobot learning,” in _CoRL 2019: Volume 100 Proceedings of Machine Learning Research_ , 2019. 

- [262] D. Kalashnikov, J. Varley, Y. Chebotar, B. Swanson, R. Jonschkowski, C. Finn, S. Levine, and K. Hausman, “Mt-opt: Continuous multi-task robotic reinforcement learning at scale,” _arXiv preprint arXiv:2104.08212_ , 2021. 

- [263] E. Jang, A. Irpan, M. Khansari, D. Kappler, F. Ebert, C. Lynch, S. Levine, and C. Finn, “Bc-z: Zero-shot task generalization with robotic imitation learning,” in _Conference on Robot Learning_ . PMLR, 2022, pp. 991–1002. 

- [264] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu _et al._ , “Rt1: Robotics transformer for real-world control at scale,” _arXiv preprint arXiv:2212.06817_ , 2022. 

- [265] A. Stone, T. Xiao, Y. Lu, K. Gopalakrishnan, K.-H. Lee, Q. Vuong, P. Wohlhart, S. Kirmani, B. Zitkovich, F. Xia _et al._ , “Open-world object manipulation using pre-trained vision-language models,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 3397–3417. 

- [266] V. Kumar, R. Shah, G. Zhou, V. Moens, V. Caggiano, A. Gupta, and A. Rajeswaran, “Robohive: A unified framework for robot learning,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 44 323–44 340, 2023. 

- [267] N. M. M. Shafiullah, A. Rai, H. Etukuru, Y. Liu, I. Misra, S. Chintala, and L. Pinto, “On bringing robots home,” 2023. [Online]. Available: https://arxiv.org/abs/2311.16098 

- [268] H.-S. Fang, H. Fang, Z. Tang, J. Liu, C. Wang, J. Wang, H. Zhu, and C. Lu, “Rh20t: A comprehensive robotic dataset for learning diverse skills in one-shot,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 653–660. 

- [269] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis _et al._ , “Droid: A large-scale in-the-wild robot manipulation dataset,” _CoRR_ , 2024. 

- [270] M. Ahn, D. Dwibedi, C. Finn, M. G. Arenas, K. Gopalakrishnan, K. Hausman, B. Ichter, A. Irpan, N. Joshi, R. Julian _et al._ , “Autort: Embodied foundation models for large scale orchestration of robotic agents,” _arXiv preprint arXiv:2401.12963_ , 2024. 

- [271] C. Chi, Z. Xu, C. Pan, E. Cousineau, B. Burchfiel, S. Feng, R. Tedrake, and S. Song, “Universal manipulation interface: Inthe-wild robot teaching without in-the-wild robots,” _CoRR_ , 2024. 

- [272] A. Mandlekar, Y. Zhu, A. Garg, J. Booher, M. Spero, A. Tung, J. Gao, J. Emmons, A. Gupta, E. Orbay, S. Savarese, and L. Fei-Fei, “Roboturk: A crowdsourcing platform for robotic skill learning through imitation,” in _Proceedings of The 2nd Conference on Robot Learning_ , ser. Proceedings of Machine Learning Research, A. Billard, A. Dragan, J. Peters, and J. Morimoto, Eds., vol. 87. PMLR, 29–31 Oct 2018, pp. 879–893. [Online]. Available: https://proceedings.mlr.press/v87/mandlekar18a.html 

- [273] T. Yu, D. Quillen, Z. He, R. Julian, K. Hausman, C. Finn, and S. Levine, “Meta-world: A benchmark and evaluation for multitask and meta reinforcement learning,” in _Conference on robot learning_ . PMLR, 2020, pp. 1094–1100. 

- [274] M. Shridhar, J. Thomason, D. Gordon, Y. Bisk, W. Han, R. Mottaghi, L. Zettlemoyer, and D. Fox, “Alfred: A benchmark for interpreting grounded instructions for everyday tasks,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2020, pp. 10 740–10 749. 

- [275] S. James, Z. Ma, D. R. Arrojo, and A. J. Davison, “Rlbench: The robot learning benchmark & learning environment,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 2, pp. 3019–3026, 2020. 

- [276] Y. Jiang, A. Gupta, Z. Zhang, G. Wang, Y. Dou, Y. Chen, L. Fei-Fei, A. Anandkumar, Y. Zhu, and L. Fan, “Vima: General robot manipulation with multimodal prompts,” _arXiv preprint arXiv:2210.03094_ , vol. 2, no. 3, p. 6, 2022. 

- [277] O. Mees, L. Hermann, E. Rosete-Beas, and W. Burgard, “Calvin: A benchmark for language-conditioned policy learning for longhorizon robot manipulation tasks,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 3, pp. 7327–7334, 2022. 

- [278] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “Libero: Benchmarking knowledge transfer for lifelong robot learning,” 2023. [Online]. Available: https: //arxiv.org/abs/2306.03310 

- [279] J.-W. Choi, Y. Yoon, H. Ong, J. Kim, and M. Jang, “Lota-bench: Benchmarking language-oriented task planners for embodied agents,” 2024. [Online]. Available: https://arxiv.org/abs/2402. 08178 

- [280] Z. Fu, T. Z. Zhao, and C. Finn, “Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation,” 2024. [Online]. Available: https://arxiv.org/abs/2401.02117 

- [281] S. Nasiriany, A. Maddukuri, L. Zhang, A. Parikh, A. Lo, A. Joshi, A. Mandlekar, and Y. Zhu, “Robocasa: Large-scale simulation of everyday tasks for generalist robots,” 2024. [Online]. Available: https://arxiv.org/abs/2406.02523 

29 

- [282] Y. Wang, Z. Xian, F. Chen, T.-H. Wang, Y. Wang, K. Fragkiadaki, Z. Erickson, D. Held, and C. Gan, “Robogen: Towards unleashing infinite data for automated robot learning via generative simulation,” in _International Conference on Machine Learning_ . PMLR, 2024, pp. 51 936–51 983. 

- [283] P. Guruprasad, H. Sikka, J. Song, Y. Wang, and P. P. Liang, “Benchmarking vision, language, & action models on robotic learning tasks,” 2024. [Online]. Available: https: //arxiv.org/abs/2411.05821 

- [284] L. Chen, C. Sima, Y. Li, Z. Zheng, J. Xu, X. Geng, H. Li, C. He, J. Shi, Y. Qiao, and J. Yan, “Persformer: 3d lane detection via perspective transformer and the openlane benchmark,” 2022. [Online]. Available: https://arxiv.org/abs/2203.11089 

- [285] M. Cordts, M. Omran, S. Ramos, T. Rehfeld, M. Enzweiler, R. Benenson, U. Franke, S. Roth, and B. Schiele, “The cityscapes dataset for semantic urban scene understanding,” 2016. [Online]. Available: https://arxiv.org/abs/1604.01685 

- [286] F. Yu, H. Chen, X. Wang, W. Xian, Y. Chen, F. Liu, V. Madhavan, and T. Darrell, “Bdd100k: A diverse driving dataset for heterogeneous multitask learning,” 2020. [Online]. Available: https://arxiv.org/abs/1805.04687 

- [287] X. Huang, P. Wang, X. Cheng, D. Zhou, Q. Geng, and R. Yang, “The apolloscape open dataset for autonomous driving and its application,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 42, no. 10, p. 2702–2719, Oct. 2020. [Online]. Available: http://dx.doi.org/10.1109/TPAMI.2019.2926463 

- [288] M.-F. Chang, J. Lambert, P. Sangkloy, J. Singh, S. Bak, A. Hartnett, D. Wang, P. Carr, S. Lucey, D. Ramanan, and J. Hays, “Argoverse: 3d tracking and forecasting with rich maps,” 2019. [Online]. Available: https://arxiv.org/abs/1911.02620 

- [289] D. Dauner, M. Hallgarten, T. Li, X. Weng, Z. Huang, Z. Yang, H. Li, I. Gilitschenski, B. Ivanovic, M. Pavone, A. Geiger, and K. Chitta, “Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking,” 2024. [Online]. Available: https://arxiv.org/abs/2406.15349 

- [290] J. Mao, M. Niu, C. Jiang, H. Liang, J. Chen, X. Liang, Y. Li, C. Ye, W. Zhang, Z. Li, J. Yu, H. Xu, and C. Xu, “One million scenes for autonomous driving: Once dataset,” 2021. [Online]. Available: https://arxiv.org/abs/2106.11037 

- [291] P. Sun, H. Kretzschmar, X. Dotiwalla, A. Chouard, V. Patnaik, P. Tsui, J. Guo, Y. Zhou, Y. Chai, B. Caine, V. Vasudevan, W. Han, J. Ngiam, H. Zhao, A. Timofeev, S. Ettinger, M. Krivokon, A. Gao, A. Joshi, S. Zhao, S. Cheng, Y. Zhang, J. Shlens, Z. Chen, and D. Anguelov, “Scalability in perception for autonomous driving: Waymo open dataset,” 2020. [Online]. Available: https://arxiv.org/abs/1912.04838 

- [292] H. Caesar, V. Bankiti, A. H. Lang, S. Vora, V. E. Liong, Q. Xu, A. Krishnan, Y. Pan, G. Baldan, and O. Beijbom, “nuscenes: A multimodal dataset for autonomous driving,” 2020. [Online]. Available: https://arxiv.org/abs/1903.11027 

- [293] A. Geiger, P. Lenz, and R. Urtasun, “Are we ready for autonomous driving? the kitti vision benchmark suite,” in _2012 IEEE Conference on Computer Vision and Pattern Recognition_ , 2012, pp. 3354–3361. 

- [294] X. Puig, K. Ra, M. Boben, J. Li, T. Wang, S. Fidler, and A. Torralba, “Virtualhome: Simulating household activities via programs,” in _Proceedings of the IEEE conference on computer vision and pattern recognition_ , 2018, pp. 8494–8502. 

- [295] A. Gupta, V. Kumar, C. Lynch, S. Levine, and K. Hausman, “Relay policy learning: Solving long-horizon tasks via imitation and reinforcement learning,” in _Conference on Robot Learning_ . PMLR, 2020, pp. 1025–1037. 

- [296] F. Xia, W. B. Shen, C. Li, P. Kasimbeg, M. E. Tchapmi, A. Toshev, R. Mart´ın-Mart´ın, and S. Savarese, “Interactive gibson benchmark: A benchmark for interactive navigation in cluttered environments,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 2, pp. 713–720, 2020. 

- [297] X. Jia, Z. Yang, Q. Li, Z. Zhang, and J. Yan, “Bench2drive: Towards multi-ability benchmarking of closed-loop end-to-end autonomous driving,” in _Advances in Neural Information Processing Systems_ , A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, Eds., vol. 37. Curran Associates, Inc., 2024, pp. 819–844. [Online]. Available: https://proceedings.neurips.cc/paper <u>files/paper/</u> 2024/file/017761f94a1cd66d01c041aff85492c4-Paper-Datasets and <u>Benchmarks Track.pdf</u> 

- [298] H. Shao, Y. Hu, L. Wang, G. Song, S. L. Waslander, Y. Liu, and H. Li, “Lmdrive: Closed-loop end-to-end driving with large language models,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , June 2024, pp. 15 120–15 130. 

- [299] Z. Yang, Y. Chen, J. Wang, S. Manivasagam, W.-C. Ma, A. J. Yang, and R. Urtasun, “Unisim: A neural closed-loop sensor simulator,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , June 2023, pp. 1389–1399. 

- [300] Y. Tassa, Y. Doron, A. Muldal, T. Erez, Y. Li, D. d. L. Casas, D. Budden, A. Abdolmaleki, J. Merel, A. Lefrancq _et al._ , “Deepmind control suite,” _arXiv preprint arXiv:1801.00690_ , 2018. 

- [301] F. Xia, A. R. Zamir, Z. He, A. Sax, J. Malik, and S. Savarese, “Gibson env: Real-world perception for embodied agents,” in _Proceedings of the IEEE conference on computer vision and pattern recognition_ , 2018, pp. 9068–9079. 

- [302] F. Xiang, Y. Qin, K. Mo, Y. Xia, H. Zhu, F. Liu, M. Liu, H. Jiang, Y. Yuan, H. Wang _et al._ , “Sapien: A simulated part-based interactive environment,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2020, pp. 11 097–11 107. 

- [303] A. Szot, A. Clegg, E. Undersander, E. Wijmans, Y. Zhao, J. Turner, N. Maestre, M. Mukadam, D. S. Chaplot, O. Maksymets _et al._ , “Habitat 2.0: Training home assistants to rearrange their habitat,” _Advances in neural information processing systems_ , vol. 34, pp. 251– 266, 2021. 

- [304] B. Shen, F. Xia, C. Li, R. Mart´ın-Mart´ın, L. Fan, G. Wang, C. P´erezD’Arpino, S. Buch, S. Srivastava, L. Tchapmi _et al._ , “igibson 1.0: A simulation environment for interactive tasks in large realistic scenes,” in _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2021, pp. 7520–7527. 

- [305] C. Li, F. Xia, R. Mart´ın-Mart´ın, M. Lingelbach, S. Srivastava, B. Shen, K. E. Vainio, C. Gokmen, G. Dharan, T. Jain _et al._ , “igibson 2.0: Object-centric simulation for robot learning of everyday household tasks,” in _Conference on Robot Learning_ . PMLR, 2022, pp. 455–465. 

- [306] C. Gan, J. Schwartz, S. Alter, M. Schrimpf, J. Traer, J. De Freitas, J. Kubilius, A. Bhandwaldar, N. Haber, M. Sano _et al._ , “Threedworld: A platform for interactive multi-modal physical simulation,” _Advances in Neural Information Processing Systems (NeurIPS)_ , 2021. 

- [307] X. Zhang, R. Chen, A. Li, F. Xiang, Y. Qin, J. Gu, Z. Ling, M. Liu, P. Zeng, S. Han, Z. Huang, T. Mu, J. Xu, and H. Su, “Close the optical sensing domain gap by physics-grounded active stereo sensor simulation,” _IEEE Transactions on Robotics_ , pp. 1–19, 2023. 

- [308] “Bullet physics sdk,” [Online], https://github.com/ bulletphysics/bullet3. 

- [309] G. Authors, “Genesis: A universal and generative physics engine for robotics and beyond, december 2024,” _URL https://github. com/Genesis-Embodied-AI/Genesis_ . 

- [310] Q. Bu, J. Cai, L. Chen, X. Cui, Y. Ding, S. Feng, S. Gao, X. He, X. Huang, S. Jiang _et al._ , “Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems,” _arXiv preprint arXiv:2503.06669_ , 2025. 

- [311] S. Tao, F. Xiang, A. Shukla, Y. Qin, X. Hinrichsen, X. Yuan, C. Bao, X. Lin, Y. Liu, T. kai Chan, Y. Gao, X. Li, T. Mu, N. Xiao, A. Gurha, V. N. Rajesh, Y. W. Choi, Y.-R. Chen, Z. Huang, R. Calandra, R. Chen, S. Luo, and H. Su, “Maniskill3: Gpu parallelized robotics simulation and rendering for generalizable embodied ai,” 2025. [Online]. Available: https://arxiv.org/abs/2410.00425 

- [312] G. Rong, B. H. Shin, H. Tabatabaee, Q. Lu, S. Lemke, M. Moˇzeiko, E. Boise, G. Uhm, M. Gerow, S. Mehta, E. Agafonov, T. H. Kim, E. Sterner, K. Ushiroda, M. Reyes, D. Zelenkovsky, and S. Kim, “Lgsvl simulator: A high fidelity simulator for autonomous driving,” in _2020 IEEE 23rd International Conference on Intelligent Transportation Systems (ITSC)_ , 2020, pp. 1–6. 

- [313] “Franka robotics,” [Online], https://franka.de/. 

- [314] “A1 robot arm,” [Online], https://userguide-galaxea.github. io/Product <u>User Guide/Introducing Galaxea Robot/product</u> info/A1/. 

- [315] R. Cadene, S. Alibert, A. Soare, Q. Gallouedec, A. Zouitine, S. Palma, P. Kooijmans, M. Aractingi, M. Shukor, D. Aubakirova, M. Russi, F. Capuano, C. Pascale, J. Choghari, J. Moss, and T. Wolf, “Lerobot: State-of-the-art machine learning for realworld robotics in pytorch,” https://github.com/huggingface/ lerobot, 2024. 

