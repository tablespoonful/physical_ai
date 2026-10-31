---
title: "Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning"
date: "2025-08-14"
authors: "Wenlong Liang; Rui Zhou; Yang Ma; Bing Zhang; Songlin Li; Yijia Liao"
url: https://arxiv.org/abs/2508.10399
pdf: https://arxiv.org/pdf/2508.10399
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2508.10399)** / [論文ページ](https://arxiv.org/abs/2508.10399)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning** 

WENLONG LIANG, University of Electronic Science and Technology of China, China RUI ZHOU<sup>∗</sup> , University of Electronic Science and Technology of China, China YANG MA, University of Electronic Science and Technology of China, China BING ZHANG, University of Electronic Science and Technology of China, China SONGLIN LI, University of Electronic Science and Technology of China, China YIJIA LIAO, University of Electronic Science and Technology of China, China 

PING KUANG, University of Electronic Science and Technology of China, China 

Embodied AI aims to develop intelligent systems with physical forms capable of perceiving, decision-making, acting, and learning in real-world environments, providing a promising way to Artificial General Intelligence (AGI). Despite decades of explorations, it remains challenging for embodied agents to achieve human-level intelligence for general-purpose tasks in open dynamic environments. Recent breakthroughs in large models have revolutionized embodied AI by enhancing perception, interaction, planning and learning. In this article, we provide a comprehensive survey on large model empowered embodied AI, focusing on autonomous decision-making and embodied learning. We investigate both hierarchical and end-to-end decision-making paradigms, detailing how large models enhance high-level planning, low-level execution, and feedback for hierarchical decision-making, and how large models enhance Vision-Language-Action (VLA) models for endto-end decision making. For embodied learning, we introduce mainstream learning methodologies, elaborating on how large models enhance imitation learning and reinforcement learning in-depth. For the first time, we integrate world models into the survey of embodied AI, presenting their design methods and critical roles in enhancing decision-making and learning. Though solid advances have been achieved, challenges still exist, which are discussed at the end of this survey, potentially as the further research directions. 

Additional Key Words and Phrases: Embodied AI, Large Model, Hierarchical Decision-Making, End-to-end, Imitation Learning, Reinforcement Learning, World Model 

# **1 INTRODUCTION** 

Embodied AI[209] aims to develop intelligent systems with physical forms capable of perceiving, decision-making, acting, and learning in real-world environments. It believes that true intelligence emerges from the interactions of an agent with its environment, providing a promising path to Artificial General Intelligence (AGI)[184]. Although the exploration for embodied AI has spanned multiple decades, it remains a challenge to endow agents with human-level intelligence, so that they can perform general-purpose tasks in open, unstructured, and dynamic environments. Early embodied AI systems[21, 200], grounded in symbolic reasoning and behaviorism, relied on rigid preprogrammed rules, resulting in limited adaptability and superficial intelligence. Although robots are widely used in manufacturing, logistics, and specialized operations, their functionality is limited to controlled environments. Advances in machine learning[133], particularly deep learning[99], have 

∗Corresponding author. 

> Authors’ addresses: Wenlong Liang, University of Electronic Science and Technology of China, Chengdu, China, 202421090221@std.uestc.edu.cn; Rui Zhou, University of Electronic Science and Technology of China, Chengdu, China, ruizhou@uestc.edu.cn; Yang Ma, University of Electronic Science and Technology of China, Chengdu, China, 202422090505@std.uestc.edu.cn; Bing Zhang, University of Electronic Science and Technology of China, Chengdu, China, 202521090224@std.uestc.edu.cn; Songlin Li, University of Electronic Science and Technology of China, Chengdu, China, 202422090530@std.uestc.edu.cn; Yijia Liao, University of Electronic Science and Technology of China, Chengdu, China, 202422090531@std.uestc.edu.cn; Ping Kuang, University of Electronic Science and Technology of China, Chengdu, China, kuangping@uestc.edu.cn. 

Liang et al. 

2 

marked a turning point for embodied AI. Vision-guided planning and reinforcement learning-based control[173] have significantly reduced the dependence of agents on precise environment modeling. Despite the advances, these models are usually trained on task-specific datasets and still face challenges in generalization and transferability, which restricts their adaptation to diverse scenarios for general-purpose applications. Recent breakthroughs in large models[149, 150, 182, 183], have significantly improved the capabilities of embodied AI. With accurate perception, interaction, and planning abilities, these models have laid the foundations for general-purpose embodied agents[137]. However, the field of embodied AI empowered by large models is still in its nascent stage, struggling with challenges in generalization, scalability, and seamless environmental interaction[177]. There is a great need to have a comprehensive and systematic review of recent advances in large model empowered embodied AI to address the gaps, challenges, and opportunities in the pursuit of AGI. 

Through comprehensive investigation in these fields, we find that current studies are scattered, with complex topics but lack of systematic categorization. Existing reviews primarily focus on large models themselves, such as Large Language Models (LLM)[29, 151, 225] and Vision Language Models (VLM)[104, 113, 191], with little attention to the synergy of large models and embodied agents. Although some reviews involve this integration, they tend to focus on the components, such as planning[188], learning[7, 26, 204], simulators[201], and applications[157, 201, 209], without systematic analysis of the overall paradigm and how these components interact to improve intelligence. Furthermore, some comprehensive surveys miss the recent advances, particularly Vision-Language-Action (VLA)[117] models and end-to-end decision-making, which have gained prominence since 2024. The review [119] provides a detailed introduction to VLA models, but lacks comparison with the hierarchical paradigm and detailed exploration of learning methods. In addition, due to the rapid development of this field, earlier surveys[48, 220] cannot catch up with the latest progress. In this survey, we focus on the decision-making and learning aspects of large model empowered embodied AI, analyze and categorize the studies, figure out the latest progress, point out the remaining challenges and the future directions, providing researchers with a clear theoretical framework and practical guidance. A comparison between our survey and the related ones are listed in Table1. 

Table 1. Comparisons between our survey and the related surveys wrt. surveying scopes. 

|Survey|Related|Publication|Large|Decision|-making|Em|bodied le|arning|World|
|---|---|---|---|---|---|---|---|---|---|
|te|surves|time|models||||||model|
|yp|y|||Hierarchic|alEnd2end|IL|RL|Other||
||[29, 104,|||||||||
||113, 151,|2024|√|×|×|×|×|×|×|
||191, 225]|||||||||
||[210]|2024|×|√|×|√|√|√|×|
||[26]|2024|√|×|×|×|×|×|×|
|Sifi|[7, 227]|2025|×|×|×|√|√|√|×|
|pecic|[188]|2024|×|√|×|×|×|×|×|
||[204]|2024|×|√|×|×|×|√|×|
||[165]|2025|×|×|×|×|√|×|×|
||[43, 122]|2024|×|×|×|×|×|×|√|
||[119]|2024|~~√~~|~~√~~|~~√~~|~~√~~|~~√~~|×|×|
||[190]|2024|×|√|√|√|×|×|×|
|Compre<br>h|[95]|2024|×|√|√|√|×|×|×|
|ensive|[117]|2024|√|√|√|√|×|√|×|
||**Ours**|–|√|√|√|√|√|√|√|


Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

3 

The main contributions of our survey are summarized as follows: 

- (1) **Focus on the empowerment of large models from the view of embodied AI.** For hierarchical decision-making, embodied AI involves high-level planning, low-level execution, and feedback enhancement, so we review and classify the related works according to this hierarchy. For end-to-end decision making, embodied AI relies on VLA models, so we review VLA models and the enhancements. As the main embodied learning methods are imitation learning (IL) and reinforcement learning (RL), we review how large models empower policy and strategy network construction in imitation learning, and how large models empower reward function design and policy network construction in reinforcement learning. 

- (2) **Comprehensive review on embodied decision-making and embodied learning.** In this survey, we provide a comprehensive review of large model empowered decision-making and learning of embodied AI. For decision-making, we review both hierarchical and end-to-end paradigms empowered by large models and compare them in detail. For embodied learning, we review not only imitation learning and reinforcement learning, but also transfer learning and meta-learning. In addition, we review the world models and how they boost decision-making and learning. 

- (3) **Dual analytical approach for in-depth insights.** We adopt a dual analytical methodology that integrates both horizontal and vertical perspectives. Horizontal analysis reviews and compares diverse approaches, such as diverse large models, hierarchical versus end-to-end decision-making, imitation learning versus reinforcement learning, and diverse strategies for embodied learning. Vertical analysis traces the evolution of core models or methods, detailing their origins, subsequent advances, and open challenges. This dual methodology enables both macro-level overview and in-depth insights of mainstream methods of embodied AI. 

The organization of our survey is shown in Fig. 1. Section 2 introduces the concept of embodied AI, provides an overview of large models, and discusses general capability enhancement on them. Then it presents the synergy of large models on embodied AI, setting the stage for subsequent sections. Section 3 delves into the hierarchical decision-making paradigm, elaborating on how large models empower dynamic high-level planning, low-level execution, and iterative optimization through feedback. Section 4 focuses on end-to-end decision making. It begins with an introduction and decomposition of VLA models, and then explores the latest enhancements in perception, action generation, and deployment efficiency. At the end of this section, it provides a comprehensive comparison between hierarchical and end-to-end decision-making. Section 5 presents embodied learning methodologies, in particular, large model-enhanced imitation learning and reinforcement learning. Section 6 introduces world models and discusses their role in decision-making and embodied learning of embodied intelligence. Section 7 discusses the open challenges and points out the future prospects. Section 8 concludes the survey. 

# **2 PRELIMINARIES** 

Large models[29, 151, 225] have demonstrated impressive capabilities and gained immense popularity in recent years. Researchers have started to take advantage of these models to build AI agents[4, 85, 137, 234]. In this section, we provide preliminary knowledge about embodied AI and large models. We first introduce the basic concepts and the overall process of embodied AI. Subsequently, we present the mainstream large models and the techniques to enhance their general capabilities. Finally, we discuss the application of large models in embodied AI systems. 

# **2.1 Embodied AI** 

An embodied AI system typically comprises two primary components: physical entities and intelligent agents[209]. Physical entities, such as humanoid robots[124], quadruped robots[13], and 

Liang et al. 

4 


Fig. 1. Organization of this survey. 

intelligent vehicles[160], execute actions and receive feedback, serving as the interface between the physical and the digital worlds. Intelligent agents form the cognitive core, enabling autonomous decision-making and learning. To perform embodied tasks, embodied AI systems interpret human intentions from language instructions, actively explore their surroundings, perceive multimodal elements from environments, and execute actions for tasks. This process imitates human learning and problem-solving paradigm. As illustrated in Fig. 2(a), humans learn skills from various resources, 

5 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 


Fig. 2. Embodied AI: from prospect of capabilities required during the whole process. 

for example, books, instructional materials, and online content. When encountering unfamiliar scenarios, they assess the environment, plan necessary actions, mentally simulate strategies, and adapt themselves based on results and external feedback. Embodied agents mimic this human-like learning and problem-solving paradigm, as illustrated in Fig. 2(b). Through imitation learning, agents acquire skills from human demonstrations or video data. When confronting complex tasks or novel environments, they analyze the surroundings, decompose tasks according to objectives, autonomously make execution strategies, and refine plans through simulators or world models. After execution, reinforcement learning optimizes strategies and actions by integrating external feedback, improving overall performance. 

The core of embodied intelligence is to enable agents to make decisions and learn new knowledge autonomously in open dynamic environments[227]. Autonomous decision-making can be realized by two approaches: (1) the hierarchical paradigm[4], which separates perception, planning, and execution into different modules, and (2) the end-to-end paradigm[234], which integrates these functionalities into a unified framework for seamless operation. Embodied learning enables agents to refine their behavioral strategies and cognitive models autonomously through long-term environmental interactions, achieving continual improvement. It can be achieved by imitation learning[20] to acquire skills from demonstrations and by reinforcement learning[11] to optimize skills through iterative refinement during task execution. Besides, world models[233] also play a critical role in providing agents with opportunities to make trials and accumulate experiences, by simulating real-world reasoning spaces. These components work synergistically to enhance the capabilities of embodied agents, advancing toward AGI. 

# **2.2 Large Models** 

Large models, including large language model (LLM), large vision model (LVM), large visionlanguage model (LVLM), multimodal large model (MLM), and vision-language-action (VLA) model, have achieved remarkable breakthroughs in architecture, data scale, and task complexity, showcasing robust perception, reasoning, and interaction capabilities. Fig. 3 shows the timeline of major large models and general capacity enhancement (GCE) to them. 

_2.2.1 Large Language Model._ In 2018, Google released BERT[42], a bidirectional Transformer model pretrained with self-supervised tasks, markedly improving performance on natural language tasks. 

Liang et al. 

6 


Fig. 3. Timeline of major large models. 

Subsequently, OpenAI released GPT[149], a generative model based on Transformer architecture, which used autoregressive training on large-scale unsupervised corpora to produce coherent text, marking a breakthrough in generative models. GPT-2[150] further scaled up model size and training data, enhancing text coherence and naturalness. In 2020, GPT-3[54] set a milestone with its vast model capacity and diverse training data, excelling in text generation, question answering, and translation. It showcased zero- and few-shot learning capabilities for the first time, paving the way for future research. Later, Codex[32], pretrained on code datasets, advanced code generation and understanding. ChatGPT[1] (based on GPT-3.5) enabled natural and fluid interactions with users while supporting a wide range of knowledge domains. Google’s PaLM[8, 39] excelled in language understanding, generation, and reasoning through large-scale training and optimized computation. InstructGPT[138], built on GPT-3[149], leveraged reinforcement learning with human feedback (RLHF) to align with human preferences. Meta’s Vicuna[38], an open-source dialogue model, delivered high-quality interactions with low computational cost, ideal for resource-constrained systems. Meta’s Llama series[182, 183] (7B, 13B, 30B, 65B parameters) significantly contributed to open-source research and development. 

_2.2.2 Large Vision Model._ LVM[96] is to process visual information. The Vision Transformer (ViT)[45] adapted the Transformer architecture for computer vision, dividing images into fixedsized patches and using self-attention to capture global dependencies. Based on it, Facebook AI released DINO[27] and DINOv2[136], leveraging self-supervised learning with ViT. DINO employed a self-distillation approach with a student-teacher network to generate high-quality image representations, capturing semantic structures without labeled data through self-attention and contrastive learning. DINOv2 enhanced DINO with improved contrastive learning and a larger training set, boosting the representation quality. The Masked Autoencoder (MAE)[78] exploited self-supervised learning to reconstruct masked visual inputs, enabling pretraining on vast unlabeled image datasets. The Segment Anything Model (SAM)[97, 156], pretrained on 11 million images, 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

7 

supported diverse segmentation tasks, including semantic, instance, and object segmentation, with strong adaptability through user feedback-based fine-tuning. 

_2.2.3 Large Vision Language Model._ LVLM[107] integrates pretrained visual encoders with visionlanguage fusion modules, allowing to process visual inputs and respond to vision-related queries via language prompts. CLIP[148], developed by OpenAI, trained image and text encoders via contrastive learning[35] on large-scale image-text pairs, aligning paired sample features while minimizing unpaired ones to create visual representations that match textual semantics. BLIP[108] employed bidirectional self-supervised learning to fuse visual and linguistic data, using a “guided” strategy to enhance pretraining efficiency and improve performance in visual question answering and image captioning. BLIP-2[107] further introduced the QFormer structure, extracting visual features from a frozen image encoder and aligning them with language instructions via multimodal pretraining for efficient cross-modal fusion. Flamingo[6] excelled in few-shot learning, processing multimodal data with minimal samples to support cross-modal reasoning in data-scarce scenarios. GPT-4V[223] extended traditional GPT to handle joint image-text inputs, generating image descriptions and answering visual questions with robust multimodal reasoning. DeepSeek-V3[115] further expanded the boundaries of multimodal reasoning by adopting a dynamic sparse activation architecture. It introduced a hybrid routing mechanism that combined task-specific experts with dynamic parameter allocation, achieving high computational efficiency in cross-modal fusion tasks. 

_2.2.4 Multimodal Large Model._ MLM can process diverse modalities, including text, vision, audio, etc. According to the input-output paradigm, MLM can be categorized to multimodal-input textoutput models and multimodal-input multimodal-output models. 

Multimodal-input text-output models integrate diverse data modalities for comprehensive content understanding. For instance, Video-Chat[109] enhanced video analysis through conversational modeling, excelling in dynamic visual content understanding. Building on Llama architecture, VideoLLaMA[218] incorporated visual and audio inputs to enable robust video content analysis. Google’s Gemini[179], designed for multimodality, efficiently processed text, image, and audio for image description and multimodal question answering. PaLM-E[46] converted multimodal inputs to unified vectors and fed them to the PaLM model for end-to-end training, achieving strong multimodal understanding. 

Multimodal-input multimodal-output models generate diverse data modalities, such as text, image and video, by learning complex data distributions. For instance, DALL·E[155], extending GPT-3 with a Vector Quantized Variational Autoencoder (VQ-VAE) and a 1.2-billion-parameter Transformer, generated creative, prompt-aligned images, supporting zero-shot tasks. DALL·E2[154] enhanced DALL·E by integrating CLIP to it, employing a two-stage process: first generating lowresolution images then followed by super-resolution enhancement, which improved image quality and diversity greatly. DALL·E3[16] further refined image-prompt alignment by enhancing text encoder and training data quality. In 2024, OpenAI released Sora[22], a video generative model that could create high-quality coherent videos up to 60 seconds from text prompts. Sora utilized a coding network to convert inputs into discrete tokens, exploited a large-scale diffusion model to optimize sequences, and projected denoised tokens back to video space. 

_2.2.5 Vision-Language-Action Model._ VLA models have gained enormous attention recently. Their core objective is to map multimodal inputs to action outputs directly, instead of the intermediate steps of hierarchical decision-making, thereby improving the perception-action integration capabilities of robots. The concept of VLA was first proposed by RT-2[234], which utilized pretrained vision-language models to discretize action space into action tokens and achieved generalization through joint fine-tuning of Internet data and robot data. However, its discrete action design and 

Liang et al. 

8 

closed-source nature limit its flexibility and further research. To overcome the limitations, VLA models based on continuous action generation[111] and open-source VLA models[93] emerged. Recent studies on VLA models further addressed the challenges. BYO-VLA[74], 3D-VLA[226], PointVLA[105] coped with visual input processing. Octo[180] and Diffusion-VLA[196] addressed action generation accuracy. TinyVLA[198] and _𝜋_ 0[18] improved computational efficiency. 

# **2.3 General Capability Enhancement of Large Models** 

Large models still suffer from limitations in reasoning ability, hallucination, computational cost, and task specificity. Researchers proposed a series of techniques to enhance their general capabilities, which are illustrated in Fig. 4. 

_In-Context Learning (ICL)_ [23] enables large models to achieve zero-shot generalization through carefully designed prompts, allowing them to tackle new tasks without additional training and tuning. Leveraging the context in input prompts, large models can understand task requirements and generate relevant outputs, making themselves a versatile tool for applications ranging from natural language processing to task-specific problem-solving. Recent advances focus on optimizing prompting techniques, such as automated prompt generation and dynamic example selection, to enhance the robustness of ICL across diverse domains. 

_X of Thoughts (XoT)_ is a family of reasoning frameworks to improve capabilities of large models in solving mathematical, logical and open-ended problems. Chain of Thoughts (CoT)[195] incorporates intermediate reasoning steps into prompts, guiding large models to break down complex problems into manageable parts. Tree of Thoughts (ToT)[213] extends CoT by exploring multiple reasoning 


Fig. 4. General capability enhancement of large models. 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

9 

paths in a tree-like structure, allowing large models to evaluate alternative solutions and backtrack when necessary. Graph of Thoughts (GoT)[15] further advances ToT by adopting a graph structure where nodes represent intermediate states and edges capture relationships and dependencies, enabling flexible non-linear reasoning. 

_Retrieval Augmented Generation (RAG)_ [103] retrieves relevant information from external knowledge bases, such as databases and web sources, and feeds it to large models for accurate responses. RAG alleviates the problem of outdated or incomplete knowledge of large models, ensuring access to up-to-date and domain-specific information. Recent advances include hybrid retrieval mechanisms that combine dense and sparse retrieval methods to balance precision and efficiency, and fine-tuning strategies to align retrieved content with generative outputs effectively. 

_Reasoning and Acting (ReAct)_ [214] integrates reasoning with action execution, enabling to produce explicit reasoning traces during performing tasks. By requiring large models to articulate their thinking processes before acting, ReAct enhances decision transparency and improves performance in dynamic interactive settings. 

_Reinforcement Learning from Human Feedback (RLHF)_ [138] integrates human preferences into training of large models, aligning large models with human values and intentions. Using human feedback as a reward signal, RLHF improves the model’s ability to generate helpful, harmless, and honest outputs in dynamic, interactive settings. By prompting the model to generate multiple responses, RLHF allows humans to rank or rate them based on quality and safety, and uses this feedback to refine the model’s future generation, ensuring coherence and ethical considerations. 

_Model Context Protocol (MCP)_ [81], an open-source standard introduced by Anthropic, provides a standardized interface for large models to interact with external data sources, tools, and services. MCP enhances the interoperability and adaptability of large models, enabling seamless integration with diverse external systems. Recent developments in MCP focus on extending its compatibility with multimodal inputs and optimizing its performance in real-time applications. 

# **2.4 Embodied Large Models** 

Large models empower embodied intelligence by enhancing the capabilities of intelligent agents. Through seamless integration of multiple modalities, including text, vision, audio, and tactile, Embodied Large Models (ELM), also known as Embodied Multimodal Large Models (EMLM), can empower agents to construct sophisticated systems capable of perceiving, reasoning, and acting in complex environments, playing a vital role in autonomous decision-making and embodied learning. 

Different large models empower embodied intelligent agents with varying capabilities. LLM usually serves as cognitive backbone[4, 85, 116], processing natural language inputs, grasping contextual nuances, and generating actionable responses. LVM is typically used in perception tasks or as callable APIs during task execution[172, 192], leveraging pretrained vision encoders to predict object class, pose, and geometry. LVLM and MLM can further enhance the capabilities of intelligent agents by integrating LLMs with multiple modalities[83, 171, 211], enabling agents to understand human instructions across text, vision, and audio, generating contextually relevant responses or actions. Recent advances in complex navigation and manipulation tasks have highlighted the advantages of MLM[201, 209]. Different from previous models that handle functionalities separately, VLA models learn end-to-end mappings from visual and linguistic inputs to executable actions[18, 94, 234]. This streamlined pipeline enables agents to interpret complex instructions, perceive dynamic environments, and execute precise physical movements, resulting in more robust and versatile embodied AI systems. Beyond enhancing planning intelligence, researchers are increasingly exploring their generative capabilities to advance embodied learning[36, 120, 204] and assist in constructing world models[47, 146, 212], further supporting the path to AGI. 

Liang et al. 

10 


Fig. 5. Hierarchical decision-making paradigm, consisting of perception and interaction, high-level planning, low-level execution, feedback and enhancement. 

# **3 HIERARCHICAL AUTONOMOUS DECISION-MAKING** 

Autonomous decision-making of agents aims to turn environmental perception and task understanding into executable decisions and physical actions. Conventional decision-making takes a hierarchical paradigm, consisting of perception and interaction, high-level planning, low-level execution, and feedback and enhancement. The perception and interaction layer relies on vision models, the high-level planning layer relies on predefined logical rules[55], and the low-level execution layer relies on classic control algorithms[56]. These methods excel in structured environments, but struggle in unstructured or dynamic settings, due to limited holistic optimization and high-level decision-making. 

Advances in large models, with their robust learning, reasoning, and generalization capabilities, have shown promises in complex task processing. By integrating the reasoning capabilities of large models with the execution capabilities of physical entities, it provides a new paradigm for autonomous decision-making. As shown in Fig. 5, environmental perception firstly interprets the agent’s surrounding environment, LLM-empowered high-level planning subsequently decomposes complex tasks into sub-tasks in consideration of perception information and task instructions, LLM-empowered low-level execution then translates sub-tasks into precise physical actions, and finally LLM-empowered feedback enhancement introduces closed-loop feedback to enhance the intelligence. 

# **3.1 High-Level Planning** 

High-level planning produces reasonable plans according to task instructions and perceived information. Traditional high-level planning relies on rule-based methods[59, 75, 126]. Given initial states and goals specified in Planning Domain Definition Language (PDDL), heuristic search planner verifies action preconditions for feasibility and employs search trees to select optimal action sequences, thereby generating an efficient and cost-effective plan[90]. Although effective in structured environments, rule-based methods struggle with adaptability in unstructured or dynamic scenarios. Large models, leveraging their zero-shot and few-shot generalization capabilities, have driven breakthroughs in addressing these challenges. According to the form of planning, LLMempowered high-level planning can be categorized into structured language planning, natural language planning, and programming language planning, as illustrated in Fig. 6. 

11 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 


Fig. 6. High-level planning empowered by large models. 

_3.1.1 Structured Language Planning with LLM._ LLM can enhance structured language planning through two key strategies, as shown in Fig. 6(a). (1) The first strategy employs LLM as the planner, utilizing its zero/few-shot generalization capability to produce plans. However, Valmeekam et al.[185] demonstrated that LLM often generated infeasible plans due to strict PDDL syntax and semantics, leading to logical errors. To mitigate this problem, LLV[9] introduced an external validator, a PDDL parser or an environment simulator, to check and iteratively refine LLM-generated plans through error feedback. FSP-LLM[175] optimized prompt engineering to align plans with logical constraints, ensuring feasibility of tasks. (2) The second strategy leverages LLM to automate PDDL generation, reducing manual effort in domain modeling. In LLM+P[116], LLM created PDDL domain files and problem descriptions, which were then solved by traditional planners, combining linguistic understanding with symbolic reasoning. PDDL-WM[64] used LLM to iteratively construct and refine PDDL domain models, which were validated by parsers and user feedback to ensure correctness and executability. By leveraging LLM as direct planner or PDDL generator, these strategies enhance automation and reduce user involvement, thus improve planning efficiency, adaptability, and scalability significantly. 

_3.1.2 Natural Language Planning with LLM._ Natural language offers greater expression flexibility than structured language, enabling full harness of LLM to decompose complex plans into subplans[110, 167], as illustrated in Fig. 6(b). However, natural language planning often produces infeasible plans, as its outputs are often based on experiences rather than actual environments. For instance, when instructed to “clean the room”, an LLM may propose “retrieve the vacuum cleaner”, without verifying the availability of it. Zero-shot[85] explored the feasibility of using LLM to decompose high-level tasks into a series of executable language planning steps. Their experiments showed that LLM could generate preliminary plans based on common sense reasoning, but lacked constraints on physical environments and action feasibility. 

To address this problem, SayCAN[4] integrates LLM with reinforcement learning, combining LLM-generated plans with a predefined skill repository and value functions to evaluate action feasibility. By scoring actions with expected cumulative rewards, SayCAN filters out impractical steps (e.g., “jump onto the table to grab a cup”), in favor of safer high-value actions (e.g., “move to the table and reach out”). Text2Motion[114] further enhances planning for tasks involving spatial interactions by incorporating geometric feasibility. It uses LLM to propose candidate action sequences, which are then evaluated by a checker for physical viability, to avoid actions like “stacking a large box on a small ball”. However, both approaches rely on fixed skill sets, lacking adaptability to open-ended tasks. Grounded Decoding[87] addresses this limitation by introducing a 

Liang et al. 

12 

flexible decoding strategy. It dynamically integrates LLM outputs with a real-time grounded model, which assesses action feasibility according to current environmental states and agent capabilities, guiding LLM to produce contextually viable plans. 

_3.1.3 Programming Language Planning with LLM._ Programming language planning transforms natural language instructions to executable programs, leveraging the precision of code to define spatial relationships, function calls, and control APIs for dynamic high-level planning in embodied tasks, as shown in Fig. 6(c). CaP[112] converts task planning to code generation, producing Pythonstyle programs with recursively defined functions to create a dynamic function library. For instance, in robot navigation, CaP firstly defines a “move” function, then extends it to “avoid obstacle move” or “approach target” based on task requirements. This self-extending library enhances adaptability to new tasks without predefined templates. However, CaP’s reliance on perception APIs and unconstrained code generation limit its handling of complex instructions. To overcome these limitations, Instruct2Act[84] offers a more integrated solution by leveraging multimodal foundation models to unify perception, planning, and control. It uses vision-language models for accurate object identification and understanding of spatial relationships, providing precise environmental awareness. The perception data is then fed to LLM, which generates code-based action sequences from a predefined robot skill repository. This method substantially increases planning accuracy and allows agents to adapt to new environments effectively, especially in tasks with significant visual components. ProgPrompt[176] employs structured prompts with environmental operations, object descriptions, and example programs to guide LLM in generating tailored, code-based plans. By incorporating predefined constraints, ProgPrompt minimizes invalid code generation and enhances cross-environment adaptability. 

# **3.2 Low-Level Execution** 

Following high-level task planning, low-level actions are executed using predefined skill lists[85]. Skill lists represent a series of basic capabilities or action modules required by embodied agents to perform specific tasks. They serve as a bridge between task planning and physical execution. For example, perception-related skills include object recognition and obstacle detection, while motionrelated skills include object grasping and moving. Implementation of low-level skills involves control theory, machine learning, and robotics engineering. The approaches evolve from traditional control algorithms to learning-driven control and to modular control, as shown in Fig. 7. 


Fig. 7. Low-level execution. 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

13 

_3.2.1 Traditional Control Algorithms._ Foundational skills are typically designed using traditional control algorithms, which mainly make use of classic model-based techniques with clear mathematical derivations and physical principles. Proportional-integral-derivative (PID) control[81] adjusts parameters to minimize errors in robotic arm joint control. State feedback control[178], often paired with linear quadratic regulators (LQR)[125], optimizes performance using system state data. Model predictive control (MPC)[2] forecasts states and generates control sequences via rolling optimization, ideal for tasks like drone path tracking. Traditional control algorithms provide mathematical interpretability, low computational complexity and real-time performance, enabling reliable task execution. However, when faced with dynamic environments, traditional control algorithms lack adaptability and struggle to handle high-dimensional uncertain system dynamics. They need to integrate with data-driven techniques, such as deep learning and reinforcement learning, to enhance generalization capabilities. For example, when a quadruped robot navigates uneven terrain, traditional PID control collaborates with learning algorithms to dynamically adjust its gait. 

_3.2.2 Learning-Driven Control with LLM._ Robot learning lies at the junction of machine learning and robotics. It enables intelligent agents to develop control strategies and low-level skills from extensive data, including human demonstrations, simulations, and environmental interactions. Imitation learning and reinforcement learning represent two important learning methods for this purpose. Imitation learning trains strategies from expert demonstrations, enabling rapid policy development with reduced exploration time. Embodied-GPT[131] leverages a 7B language model for high-level planning and converts plans to low-level strategies via imitation learning. Reinforcement learning optimizes strategies through iterative trials and environmental rewards, suitable in highdimensional dynamic environments. Hi-Core[140] employs a two-layer framework where LLM sets high-level strategies and sub-goals, while reinforcement learning generates specific actions at low levels. These learning-driven control methods empowered by LLM offer strong adaptability and generalization. However, their training typically requires a large amount of data and computational resources, and the convergence and stability of the strategies are difficult to guarantee. 

_3.2.3 Modular Control with LLM and Pretrained Models._ Modular control integrates LLM with pretrained strategy models, such as CLIP[148] for visual recognition and SAM[96] for segmentation. By equipping LLM with descriptions of these tools, they can be invoked dynamically during task execution. DEPS[192] combines multiple different modules to complete detection and actions based on task requirements and natural language descriptions of the pretrained models. PaLM-E[46] merges LLM with visual modules for segmentation and recognition. CLIPort[172] leverages CLIP for open-vocabulary detection. [112] leveraged LLM to generate codes to create libraries of callable functions for navigation and operations. This modular approach ensures scalability and reusability across diverse tasks by leveraging shared pretrained models. 

However, challenges exist. Firstly, calling external strategy models may introduce additional computational and communication delays, especially in real-time tasks (e.g., autonomous driving[216]), where such delays may affect the response efficiency significantly. Secondly, the overall performance of intelligent agents is highly dependent on the quality of the pretrained strategy models. If the strategy models have defects (such as insufficient generalization ability or training data bias), even with strong planning capabilities of LLM, the execution results may still be unsatisfactory. Therefore, it is important to optimize the communication efficiency between modules, improve the robustness of the strategy models, and design more intelligent invocation decision mechanisms. 

Liang et al. 

14 

# **3.3 Feedback and Enhancement** 

Hierarchical decision-making architecture guides task planning through task descriptions and example prompts. To ensure the quality of task planning, a closed-loop feedback mechanism should be introduced. The feedback may come from the large model itself, humans, and external environments, as shown in Fig. 8. 


Fig. 8. Feedback and enhancement. 

_3.3.1 Self-Reflection of Large Models._ The large models can act as task planners, evaluators and optimizers, thus iteratively refine decision-making processes without external interventions. The agents get feedback of actions, autonomously detect and analyze failed executions, and continuously learn from previous tasks. By this self-reflection and optimization mechanism, the large models can generate robust strategies, offering advantages in long-sequence planning, multimodal tasks, and real-time scenarios. Self-reflection can implemented in two ways, as depicted in Fig. 8(a). 

(1) The first approach triggers plan regeneration by Re-Prompting[153] based on detected execution failures or precondition errors. Re-Prompting integrates error context (e.g., failing to unlock a door before opening it) as feedback to dynamically adjust prompts and thereby correct LLM-generated plans. DEPS[153] adopts a “describe, explain, plan, select” framework, where LLM describes execution process, explains failure causes, and re-prompts to correct plan deficiencies, enhancing interactive planning. 

(2) The second approach takes introspection mechanism, enabling LLM to evaluate and refine its output independently. Self-Refine[121] uses a single LLM for planning and optimization, iteratively improving plan rationality through multiple self-feedback cycles. Reflexion[170] extends it by incorporating a long-term memory to store evaluation results, combining multiple feedback mechanisms to enhance plan feasibility. ISR-LLM[231] applies iterative self-optimization in PDDLbased planning, generating initial plans, performing rationality checks, and refining outcomes via self-feedback. Voyager[189], tailored for programming language planning, builds a dynamic code skill library by extracting feedback from execution failures, enabling agents to adapt to complex tasks. 

_3.3.2 Human Feedback._ Human feedback enhances planning accuracy and efficiency by establishing an interactive closed-loop mechanism with humans, as illustrated in Fig. 8(b). This approach enables agents to dynamically adjust behaviors based on human feedback. KNOWNO[161] introduces an uncertainty measurement framework, allowing LLM to identify knowledge gaps and 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

15 

seek human assistance in high-risk or uncertain scenarios. EmbodiedGPT[132] takes a planningexecution-feedback loop, where agents request human inputs when low-level controls fail. This human feedback, combined with reinforcement learning and self-supervised optimization, enables the agent to iteratively refine its planning strategies, ensuring better alignment with dynamic environmental conditions. YAY Robot[168] allows users to pause robots with commands and provide guidance, facilitating real-time language-based corrections. The feedback is recorded for strategy fine-tuning and periodic queries, enabling real-time and long-term improvements. IRAP[80] allows interactive question-answering with humans to acquire task-specific knowledge, enabling precise robot instructions. 

_3.3.3 Environment Feedback._ Environment feedback enhances LLM-based planning via dynamic interactions with environments, as depicted in Fig. 8(c). Inner Monologue[88] transforms multimodal inputs to linguistic descriptions for an “inner monologue” reasoning, allowing LLM to adjust plans based on environmental feedback. TaPA[203] integrates open-vocabulary object detection and tailors plans for navigation and operations. DoReMi[65] detects discrepancies between planned and actual outcomes and takes multimodal feedback to adjust tasks dynamically. In multi-agent settings, RoCo[123] leverages environmental feedback and inter-agent communications to correct robotic arm path plannings in real time. 

LLM-based planning often requires to convert feedback to natural language. VLM simplifies this by integrating visual inputs and language reasoning, avoiding feedback conversions. ViLaIn[171] integrates LLM with VLM to generate machine-readable PDDL from language instructions and scene observations, driving symbolic planners with high precision. ViLA[83] and Octopus[211] achieve robot vision language planning by making advantage of GPT4-V MLM to generate plans, integrating perception data for robust zero-shot reasoning. Voxposer[86] further exploits MLM to extract spatial geometric information, generate 3D coordinates and constraint maps from robot observations to populate code parameters, thereby enhancing spatial accuracy in planning. 

# **4 END-TO-END AUTONOMOUS DECISION-MAKING** 

Hierarchical paradigm relies on separate task-planning, action-execution and feedback modules, hence it suffers from error accumulation and struggles to generalize across diverse tasks. Moreover, high-level semantic knowledge derived from large models is difficult to apply to robotic action execution directly, resulting in integration gaps. To mitigate these challenges, end-to-end autonomous decision-making gains significant attention recently, which maps multimodal inputs (i.e. visual observations and linguistic instructions) to actions directly. It is typically implemented by VLA, as illustrated in Fig. 9. 


Fig. 9. End-to-end decision-making by VLA. 

Liang et al. 

16 

# **4.1 Vision-Language-Action Models** 

VLA models represent a breakthrough in embodied AI by integrating perception, language understanding, planning, action execution and feedback optimizing into a unified framework. By leveraging rich prior knowledge of large models, VLA models can achieve precise and adaptable task execution in dynamic, open environments. A typical VLA model comprises three key components: tokenization and representation, multimodal information fusion, and action detokenization, as illustrated in the Fig. 10. 


Fig. 10. Vision-Language-Action Models. 

(1) _Tokenization and Representation._ VLA models use four token types: vision, language, state, and action, to encode multimodal inputs for context-aware action generation. Vision tokens and language tokens encode environmental scenes and instructions into embeddings, forming the foundation of task and context. State tokens capture the agent’s physical configuration, including joint positions, force-torque, gripper status, end-effector pose, and object locations. Action tokens, generated autoregressively based on prior tokens, represent low-level control signals (e.g., joint angles, torque, wheel velocities) or high-level movement primitives (e.g., “move to grasp pose,” “rotate wrist”), enabling VLA models to act as language-driven policy generators. 

(2) _Multimodal Information Fusion._ Visual tokens, language tokens, and state tokens are fused into a unified embedding for decision-making through a cross-modal attention mechanism, typically implemented within a transformer architecture. This mechanism dynamically weighs the contributions of each modality, enabling the VLA model to jointly reason over object semantics, spatial layouts, and physical constraints based on the task context. 

(3) _Action Detokenization._ The fused embedding is then passed to an autoregressive decoder, typically implemented within the transformer architecture, to generate a series of action tokens corresponding to low-level control signals or high-level movement primitives. Action generation can be discrete or continuous. In discrete action generation, the model selects from a predefined set of actions, such as specific movement primitives or discretized control signals, which are mapped to executable commands. In continuous action generation, the model outputs fine-grained control signals, often sampled from a continuous distribution using a final MLP layer, enabling precise 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

17 

manipulation or navigation. These action tokens are detokenized by mapping them to executable control commands, which are passed to the execution loop. The loop feeds back updated state information, enabling the VLA model to dynamically adapt to perturbations, object shifts, or occlusions in real time. 

Robotics Transformer 2 (RT-2)[234] is a renowned VLA model. It leverages Vision Transformer (ViT)[45] for visual processing and leverages PaLM to integrates vision, language, and robot state information. Specially, RT-2 discretizes the action space into eight dimensions (including 6-DoF end-effector displacement, gripper status, and termination commands). Each dimension is divided into 256 discrete intervals except for the termination command and embedded into the VLM vocabulary as action tokens. During training, RT-2 employs a two-stage strategy: first pretraining with Internet-scale vision-language data to enhance semantic generalization; then fine-tuning to map inputs (i.e., robot camera images and text task descriptions) to outputs (i.e., action word token sequences, e.g., “1 128 91 241 5 101 127 255”). The trained VLA model can generate action word in an autoregressive manner based on vision-language inputs, and decode them into specific action sequences via a predefined mapping table. By modeling actions as “language”, RT-2 leverages large models’ capabilities to enhance low-level action commands with rich semantic knowledge. 

# **4.2 Enhancements on VLA** 

Although the VLA end-to-end decision-making architecture is powerful, it exhibits notable limitations that constrain its performance in complex embodied tasks. Firstly, the real-time closed-loop mechanism causes VLA models highly sensitive to perturbations in visual and language inputs, where visual noise (e.g., occlusions or cluttered backgrounds) can destabilize action outputs, compromising task reliability. In addition, the reliance on 2D perception limits the model’s ability to interpret intricate 3D spatial relationships. Secondly, the action generation process often depends on simplistic policy networks at the output layer, which have difficulties in meeting the requirements of high-precision and dynamically evolving tasks, resulting in sub-optimal trajectories. Thirdly, training VLA models demands high computation resources, leading to high deployment costs and scalability challenges. To address these issues and advance the applicability of VLA in complex scenarios, researchers have proposed some enhancements. We categorize them as: perception capability enhancement (to solve the first problem), trajectory action optimization (to solve the second problem), and training cost reduction (to solve the third problem), as illustrated in the Fig. 11. 

_4.2.1 Perception Capability Enhancement._ To improve the perception capability, BYO-VLA[74] optimizes the tokenization and representation component by implementing a runtime observation intervention mechanism, which leverages automated image preprocessing to filter out visual noise originating from occluding objects and cluttered backgrounds. TraceVLA[229] focuses on the multimodal information fusion component, introducing visual trajectory prompts to the crossmodal attention mechanism. By incorporating trajectory-related data with vision, language, and state tokens, TraceVLA enhances spatio-temporal awareness, enabling precise action trajectory predictions. BYO-VLA improves input quality, while TraceVLA refines integration of dynamic information during fusion. For 3D perception, 3D-VLA[226] combines a 3D large model with a diffusion-based world model to process point clouds and language instructions. It generates semantic scene representations and predicts future point cloud sequences, improving 3D object relationship understanding, thereby surpassing 2D VLA models in complex 3D settings. SpatialVLA[147] further emphasizes the problem of spatial understanding in robot sorting tasks. It proposes Ego3D position encoding to inject 3D information directly into input observations and adopts adaptive action schemes to improve robots’ adaptability in different environments. 

Liang et al. 

18 


Fig. 11. Enhancements on Vision-Language-Action Models. 

_4.2.2 Trajectory Action Optimization._ Discrete action space limits the expression of undefined or high-precision actions. Diffusion-enhanced methods can provide smoother and more controllable actions by modeling complex robot behaviors through diffusion models. Octo[180] combines Transformer and diffusion models to generate robot actions. It processes multimodal inputs through Transformer, extracts visual-language features, and uses conditional diffusion decoders to iteratively optimize action sequences based on these features, so as to generate smooth and precise trajectories. By modular design and efficient fine-tuning, Octo achieves cross-task generalization with only a small amount of task-specific data. Diffusion-VLA[196] combines a language model with a diffusion policy decoder into a unified framework. It uses an autoregressive language model to parse language instructions and generate preliminary task representations, which are fed into the diffusion policy decoder, optimizing the action sequence through a gradual denoising process. Diffusion-VLA employs end-to-end training across the entire framework, jointly optimizing language understanding and action generation. The diffusion process corrects the discontinuities in the autoregressive outputs at each step, ensuring the smoothness and robustness of action trajectories. Compared to Octo, Diffusion-VLA has higher computational cost but is more suitable for complex tasks requiring deep semantic-action fusion. 

_4.2.3 Training Cost Reduction._ VLA models in complex tasks require high computational cost, which is limited on resource-constrained embodied platforms. To reduce the training cost, researchers have proposed optimization methods to improve inference speed, data efficiency, and real-time performance while maintaining task performance. _𝜋_ 0[18] exploits flow matching to represent complex continuous action distributions. Compared to multi-step sampling used in diffusion models, flow matching optimizes action generation process through continuous flow field modeling, consequently reducing computational overhead and improving real-time performance. Compared to Diffusion-VLA[196] and Octo[180], the improvements in computational efficiency and control accuracy make _𝜋_ 0 more suitable for resource-constrained embodied applications, especially tasks requiring high-precision continuous control. In addition, TinyVLA[234] achieves significant improvement in inference speed and data efficiency by designing a lightweight multimodal model and a diffusion strategy decoder. OpenVLA-OFT[92] uses parallel decoding instead of traditional 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

19 

autoregressive generation to generate complete action sequences in a single forward pass rather than one by one, thereby reducing the inference time significantly. 

# **4.3 Mainstream VLA Models** 

A large number of VLA models have emerged recently, with various architectures and capabilities. For better understanding and deployment, we summarize and compare them in Table 2 with respect to architecture, contributions and capability enhancements. 

Table 2. Mainstream VLA models (P: perception, A: trajectory action, C: training cost). 

|Model|Architecture|Contributions|Enh<br>P|ancem<br>A|ents<br>C|
|---|---|---|---|---|---|
|RT-2 [234]<br>(2023)|• Vision Encoder: ViT22B/ViT-4B<br>• Language Encoder: PaLIX/PaLM-E<br>• Action Decoder: Symbol-tuning|Pioneering large-scale VLA, jointly<br>fine-tuned on web-based VQA and<br>robotic datasets, unlocking<br>advanced emergent functionalities.|×|√|√|
|Seer [63]<br>(2023)|• Vision Encoder: Visual backbone<br>• Language Encoder: Transformer-based<br>• Action Decoder: Autoregressive action<br>prediction head|Efficiently predict future video<br>frames from language instructions<br>by extending a pretrained<br>text-to-image diffusion model.|√|×|√|
|Octo [180]<br>(2024)|• Vision Encoder: CNN<br>• Language Encoder: T5-base<br>• Action Decoder: Diffusion Transformer|First generalist policy trained on a<br>massive multi-robot dataset (800k+<br>trajectories). A powerful<br>open-source foundation model.|×|√|×|
|Open-<br>VLA [94]<br>(2024)|• Vision Encoder: DINOv2 + SigLIP<br>• Language Encoder: Prismatic-7B<br>• Action Decoder: Symbol-tuning|An open-source alternative to RT-2,<br>superior parameter efficiency and<br>strong generalization with efficient<br>LoRA fine-tuning.|×|×|√|
|Mobility-<br>VLA [37]<br>(2024)|• Vision Encoder: Long-context ViT + goal<br>image encoder<br>• Language Encoder: T5-based instruction<br>encoder<br>• Action Decoder: Hybrid diffusion + au-<br>toregressive ensemble|Leverages demonstration tour<br>videos as an environmental prior,<br>using a long-context VLM and<br>topological graphs for navigating<br>based on complex multimodal<br>instructions.|√|√|×|
|Tiny-VLA<br>[198]<br>(2025)|• Vision Encoder: FastViT with low-latency<br>encoding<br>• Language Encoder: Compact language en-<br>coder (128-d)<br>• Action Decoder: Diffusion policy decoder<br>(50M parameters)|Outpaces OpenVLA in speed and<br>precision; eliminates pretraining<br>needs; achieves 5x faster inference<br>for real-time applications.|×|×|√|


Liang et al. 

20 

Table 2. Mainstream VLA models (P: perception, A: trajectory action, C: training cost) (continued). 

|Model|Architecture|Contributions|Enh<br>P|ancem<br>A|ents<br>C|
|---|---|---|---|---|---|
|Diffusion-<br>VLA [196]<br>(2024)|• Transformer-based visual encoder for con-<br>textual perception<br>• Language Encoder: Autoregressive rea-<br>soning module with next-token prediction<br>• Diffusion policy head for robust action<br>sequence generation|Leverage diffusion-based action<br>modeling for precise control;<br>superior contextual awareness and<br>reliable sequence planning.|×|√|×|
|Point-<br>VLA [105]<br>(2025)|• Vision Encoder: CLIP + 3D Point Cloud<br>• Language Encoder: Llama-2<br>• Action Decoder: Transformer with spatial<br>token fusion|Excel at long-horizon and spatial<br>reasoning tasks; avoid retraining<br>by preserving pretrained 2D<br>knowledge|√|×|×|
|VLA-<br>Cache<br>[208]<br>(2025)|• Vision Encoder: SigLIP with token mem-<br>ory buffer<br>• Language Encoder: Prismatic-7B<br>• Action Decoder: Transformer with dy-<br>namic token reuse|Faster inference with near-zero<br>loss; dynamically reuse static<br>features for real-time robotics|×|×|√|
|_𝜋_0 [18]<br>(2024)|• Vision Encoder: PaliGemma VLM back-<br>bone<br>• Language Encoder: PaliGemma (multi-<br>modal)<br>• Action Decoder: Flow Matching|Employ flow matching to produce<br>smooth, high-frequency (50Hz)<br>action trajectories for real-time<br>control.|×|√|√|
|_𝜋_0 Fast<br>[143]<br>(2025)|• Vision Encoder: PaliGemma VLM back-<br>bone<br>• Language Encoder: PaliGemma (multi-<br>modal)<br>• Action Decoder: Autoregressive Trans-<br>former with FAST|Introduces an efficient action<br>tokenization scheme based on the<br>Discrete Cosine Transform (DCT),<br>enabling autoregressive models to<br>handle high-frequency tasks and<br>significantly speeding up training.|×|√|√|
|Edge-VLA<br>[25] (2025)|• Vision Encoder: SigLIP + DINOv2<br>• Language Encoder: Qwen2 (0.5B parame-<br>ters)<br>• Action Decoder: Joint control prediction<br>(non-autoregressive)|Streamlined VLA tailored for edge<br>devices, delivering 30–50Hz<br>inference speed with<br>OpenVLA-comparable<br>performance, optimized for<br>low-power, real-time deployment.|×|×|√|


Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

21 

Table 2. Mainstream VLA models (P: perception, A: trajectory action, C: training cost) (continued). 

|Model|Architecture|Contributions|Enh<br>P|ancem<br>A|ents<br>C|
|---|---|---|---|---|---|
|OpenVLA-<br>OFT [92]<br>(2025)|• Vision Encoder: SigLIP + DINOv2 (multi-<br>view)<br>• Language Encoder: Llama-2 7B<br>• Action Decoder: Parallel decoding with<br>action chunking and L1 regression|An optimized fine-tuning recipe for<br>VLAs that integrates parallel<br>decoding and a continuous action<br>representation to improve<br>inference speed and task success.|×|√|√|
|Spatial-<br>VLA [147]<br>(2025)|• Vision Encoder: SigLIP from PaLiGemma2<br>4B<br>• Language Encoder: PaLiGemma2<br>• Action Decoder: Adaptive Action Grids<br>and autoregressive transformer|Enhance spatial intelligence by<br>injecting 3D information via<br>‘Ego3D Position Encoding’ and<br>representing actions with<br>‘Adaptive Action Grids’.|√|√|×|
|MoLe-<br>VLA [219]<br>(2025)|• Vision Encoder: Multi-stage ViT with<br>STAR router<br>• Language Encoder: CogKD-enhanced<br>Transformer<br>• Action Decoder: Sparse Transformer with<br>dynamic routing|A brain-inspired architecture that<br>uses dynamic layer-skipping<br>(Mixture-of-Layers) and knowledge<br>distillation to improve efficiency.|×|×|√|
|DexGrasp-<br>VLA [230]<br>(2025)|• Vision Encoder: Object-centric spatial ViT<br>• Language Encoder: Transformer with<br>grasp sequence reasoning<br>• Action Decoder: Diffusion controller for<br>grasp pose generation|A hierarchical framework for<br>general dexterous grasping, using a<br>VLM for high-level planning and a<br>diffusion policy for low-level<br>control.|×|√|×|
|Dex-VLA<br>[197]<br>(2025)||A large plug-in diffusion-based<br>action expert and an embodiment<br>curriculum learning strategy for<br>efficient cross-robot training and<br>adaptation.|×|√|×|


# **4.4 Hierarchical versus End-to-End Decision-Making** 

Hierarchical and end-to-end represent two distinct paradigms to achieve autonomous decisionmaking for embodied intelligence, each with unique design philosophies, implementation strategies, performance characteristics, and application domains. Herewith we make a comparison between them, as listed in Table 3, which outlines the key differences with respect to architecture, performance, interpretability, generalization, etc. 

Hierarchical architectures decompose the decision-making process into multiple modules, each addressing the specific aspects of perception, planning, execution and feedback. The core idea is to break down complex tasks into manageable sub-tasks, to enhance debuggability, optimization, and maintenance. Hierarchical architectures excel in integrating domain knowledge (e.g., physical constraints, rules), offering high interpretability and reliability for embodied tasks. But their 

Liang et al. 

22 

limitations are obvious. The separation of modules may lead to sub-optimal solutions due to improper coordination, particularly in dynamic complex environments. Manual task decomposition may hinder the adaptability to unseen scenarios and tasks. 

End-to-end architectures employ a large-scale neural network, i.e., VLA, to map multimodal inputs to actions directly, without modular decomposition. VLAs are usually built on large multimodal models and trained on extensive datasets, achieving visual perception, language understanding, and action generation simultaneously. Due to highly integrated architecture, VLA minimizes error accumulation across modules and enables efficient learning via end-to-end optimization. As training on large-scale multimodal dataset, VLA possesses strong generalization to complex tasks in unstructured environments. However, the black-box nature of VLAs reduces interpretability, making it difficult to analyze the decision-making process. VLAs’s performance relies heavily on the quality and diversity of training data. The computational cost of end-to-end training is also high. 

Table 3. Comparison of hierarchical and end-to-end decision-making paradigms. 

|Aspect|Hierarchical|End-to-End|
|---|---|---|
|Architecture|• Perception: dedicated modules (e.g., SLAM,<br>CLIP)<br>• High-level planning: structured, language, pro-<br>gram<br>• Low-level execution: predefined skill lists<br>• Feedback: LLM self-reflection, human, environ-<br>ment|• Perception: integrated in tokenization<br>• Planning: implicit via VLA pretraining<br>• Action generation: Autoregressive generation<br>with diffusion-based decoders<br>• Feedback: inherent in closed-loop cycle|
|Performance|• Reliable in structured tasks<br>• Limited in dynamic settings|• Superior in complex, open-ended tasks with<br>strong generalization<br>• Dependent on training data|
|Interpretability|• High, with clear modular design|• Low, due to black-box nature of neural net-<br>works|
|Generalization|• Limited, due to reliance on human-designed<br>structures|• Strong, driven by large-scale pretraining<br>• Sensitive to data gaps|
|Real-time|• Low, inter-module communications may intro-<br>duce delays in complex scenarios|• High, direct perception-to-action mapping min-<br>imizes processing overhead|
|Computational<br>Cost|• Moderate, with independent module optimiza-<br>tion but coordination overhead|• High, requiring significant resources for train-<br>ing|


Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

23 

Table 3. Comparison of hierarchical and end-to-end decision-making (continued). 

|Aspect|Hierarchical|End-to-End|
|---|---|---|
|Application|• Suitable for industrial automation, drone navi-<br>gation, autonomous driving|• Suitable for domestic robots, virtual assistants,<br>human-robot collaboration|
|Advantages|• High interpretability<br>• High reliability<br>• Easy to integrate domain knowledge|• Seamless multimodal integration<br>• Efficient in complex tasks<br>• Minimal error accumulation|
|Limitations|• Sub-optimal, due to module coordination issues<br>• Low adaptability to unstructured settings|• Low interpretability<br>• High dependency on training data<br>• High computational costs<br>• Low generalization in out-of-distribution sce-<br>narios|


# **5 EMBODIED LEARNING** 

Embodied learning aims to enable agents to acquire complex skills and refine their capabilities during interactions with environments[227]. Through learning and optimizing skills continuously, agents can achieve precise decision-making and real-time adaptation. This ability can be achieved through coordination of multiple learning strategies, as depicted in Fig. 12. Imitation learning allows agents to quickly acquire initial policies, transfer learning[152] facilitates knowledge transfer across diverse tasks, meta-learning[51] enables agents to learn how to learn, and reinforcement learning[11] optimizes policies through continuous interactions with environments. However, these learning methods still face significant technical challenges in embodied AI. Imitation learning struggles to capture complex behaviors, while reinforcement learning is often hindered by intricacies of designing effective reward functions. In recent years, the advent of Transformer and large models has motivated researchers to explore integration of large models with learning methods to overcome the limitations. In this section, we first describe the process of embodied learning and common learning methods, we then elaborate on imitation learning and reinforcement learning in more details and investigate how large models enhance these methods in embodied AI. 

# **5.1 Embodied Learning Methods** 

Embodied agents should be able to acquire new knowledge and learn new tasks along their entire life, instead of relying on initial training datasets[227]. This ability is essential for the complexity and variability of the real world, where new tasks and challenges arise frequently. Embodied learning can be modeled as a goal-conditional partially observable Markov decision process, defined as an 8-tuple ( _𝑆,𝐴,𝐺,𝑇, 𝑅,_ Ω _,𝑂,𝛾_ ), where 

- _𝑆_ is the set of states of the environment. Each state encodes multimodal information, such as textual descriptions, images, or structured data. 

- _𝐴_ is the set of actions. Each action represents an instruction or command, often expressed in natural language. 

- _𝐺_ is the set of possible goals. _𝑔_ ∈ _𝐺_ specifies a particular objective, e.g., purchase a laptop. 

Liang et al. 

24 


Fig. 12. Embodied learning: process and methodologies. 

- _𝑇_ ( _𝑠_<sup>′</sup> | _𝑠,𝑎_ ) is the state transition probability function. For each state-action pair ( _𝑠,𝑎_ ), _𝑇_ (·) defines the probability distribution over next states _𝑠_<sup>′</sup> ∈ _𝑆_ . 

- _𝑅_ : _𝑆_ × _𝐴_ × _𝐺_ → _𝑅_ is the goal-conditional reward function, evaluating how well an action _𝑎_ in state _𝑠_ advances the goal . For each triplet ( _𝑠,𝑎,𝑔_ ) , the reward can be numeric (e.g., a score) or textual (e.g., good job), providing an interactive feedback for the goal. 

- Ω is the set of observations, which may include textual, visual, or multimodal data, representing the agent’s partial view of the state. 

- _𝑂_ ( _𝑜_<sup>′</sup> | _𝑠_<sup>′</sup> _,𝑎_ ) is the observation probability function, defining the probability of observing _𝑜_<sup>′</sup> ∈ Ω after transitioning to state _𝑠_<sup>′</sup> via action _𝑎_ . 

- _𝛾_ ∈[0 _,_ 1) is the discount factor, balancing the immediate and the long-term rewards. It applies only when rewards are numeric. 

This formulation captures the complexities of real-world scenarios, where an agent operates under partially observable stochastic dynamics. At time _𝑡_ , the agent receives an observation _𝑜𝑡_ ∈ Ω and a goal _𝑔_ ∈ _𝐺_ . It selects an action _𝑎𝑡_ ∈ _𝐴_ according to the policy _𝜋_ ( _𝑎𝑡_ | _𝑜𝑡,𝑔_ ). After action execution, the environment state transitions to _𝑠𝑡_ +1 ∼ _𝑇_ ( _𝑠_<sup>′</sup> | _𝑠𝑡,𝑎𝑡_ ), yielding an observation _𝑜𝑡_ +1 ∼ _𝑂_ ( _𝑜_<sup>′</sup> | _𝑠𝑡_ +1 _,𝑎𝑡_ ) and a reward _𝑅_ ( _𝑠𝑡_ +1 _,𝑎𝑡,𝑔_ ). For end-to-end decision-making, the VLA model directly encodes the policy _𝜋_ ( _𝑎_ | _𝑜,𝑔_ ), processing multimodal observation _𝑜_ ∈ Ω and producing action _𝑎_ ∈ _𝐴_ . For hierarchical decision-making, the high-level agent generates context-aware subgoal _𝑔𝑠𝑢𝑏_ via an LLM-enhanced policy _𝜋ℎ𝑖𝑔ℎ_ ( _𝑔𝑠𝑢𝑏_ | _𝑜,𝑔_ ), then the low-level policy _𝜋𝑙𝑜𝑤_ ( _𝑎_ | _𝑜,𝑔𝑠𝑢𝑏_ ) maps the subgoal to an action _𝑎_ ∈ _𝐴_ . The low-level policy _𝜋𝑙𝑜𝑤_ ( _𝑎_ | _𝑜,𝑔𝑠𝑢𝑏_ ) can be learned through imitation learning or reinforcement learning. The learned policy is embedded in the model’s hierarchical architecture, and fine-tuned during training to handle specific tasks, e.g., navigation, manipulation, human-robot interaction. 

For embodied intelligence, imitation learning, reinforcement learning, transfer learning, and meta-learning all play important roles in enabling agents to act in complex real-world environments. Each learning method addresses unique challenges. Imitation learning[204] allows agents to learn effective policies by emulating expert or video demonstrations, highly efficient for tasks like robotic manipulation, where high-quality data is available. But its dependence on diverse demonstrations limits adaptability to new scenarios. Reinforcement learning[139] excels in dynamic settings through 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

25 

trial-and-error interactions guided by reward functions. However, it is a challenge to design proper reward functions and reinforcement learning requires high computational resources. Transfer learning[152] enhances learning effect by transferring knowledge between related tasks, ideal for reusing skills. Yet it risks negative transfer when tasks differ significantly[181]. Meta-learning[66] focuses on learning how to learn, enabling rapid adaptation to new tasks with minimal data. But it requires extensive pretraining across diverse tasks. Table 4 summaries and compares these methods in brief with respect to embodied AI. 

Table 4. Comparison of learning methods wrt. embodied AI. 

|Methods|Strengths|Limitations|Applications|
|---|---|---|---|
|Imitation<br>Learning|• Rapid policy learning by<br>mimicking expert demon-<br>strations<br>• Efficient for tasks with high-<br>quality data|• Dependent on diverse, high-<br>quality demonstrations<br>• Limited adaptability to new<br>tasks or sparse data scenar-<br>ios|• Robotic manipulation<br>• Structured navigation<br>• Human-robot<br>interaction<br>with expert guidance|
|Reinforcement<br>Learning|• Optimizes policies in dy-<br>namic uncertain environ-<br>ments via trial-and-errors<br>• Excels in tasks with clear re-<br>ward signals|• Requires large samples and<br>computational resources<br>• Sensitive to reward function<br>and discount factor|• Autonomous navigation<br>• Adaptive human-robot in-<br>teraction<br>• Dynamic task optimization|
|Transfer Learning|• Accelerates<br>learning<br>by<br>transferring<br>knowledge<br>between related tasks<br>• Enhances generalization in<br>related tasks|• Risks<br>negative<br>transfer<br>when tasks differ signifi-<br>cantly<br>• Requires task similarity for<br>effective learning|• Navigation across diverse<br>environments<br>• Manipulation with shared<br>structures<br>• Cross-task skill reuse|
|Meta-Learning|• Rapid adaptation to new<br>tasks with minimal data<br>• Ideal for diverse embodied<br>tasks|• Demands<br>extensive<br>pre-<br>training and large datasets<br>• Establishing<br>a<br>universal<br>meta-policy<br>is<br>resource-<br>intensive|• Rapid adaptation in naviga-<br>tion, manipulation, or inter-<br>action across diverse tasks<br>and environments|


_5.1.1 Imitation Learning._ Imitation learning is a key method in embodied learning. It enables agents to learn policies by mimicking expert demonstrations, allowing rapid acquisition of decisionmaking strategies for goal-oriented tasks[204]. The training is supervised using datasets of expert state-action pairs ( _𝑠,𝑎_ ). The goal is to learn a policy _𝜋_ ( _𝑎_ | _𝑠_ ) that closely replicates the expert’s behavior by minimizing the negative log-likelihood of the expert’s actions. Therefore, its objective function can be defined as: 

L( _𝜋_ ) = − E _𝜏_ ∼PD [log _𝜋_ (a| _𝑠_ )] (1) 

Liang et al. 

26 

where _𝐷_ is the set of expert demonstrations. Each demonstration _𝜏𝑖_ consists of a sequence of state-action pairs ( _𝑠𝑡,𝑎𝑡_ ) of length _𝐿_ : 


In continuous action spaces, the policy _𝜋_ (·) is often modeled as a Gaussian distribution, and the objective function is approximated using mean squared error (MSE) between the predicted and the expert actions. Imitation learning is highly sample-efficient, as it avoids extensive trial-and-error, but it is highly dependent on the quality and coverage of the demonstration data, having difficulties in unseen scenarios. A hybrid approach combining imitation learning with reinforcement learning can address this limitation by initializing the policy with imitation learning and refining it with reinforcement learning, enhancing robustness to unseen situations. 

_5.1.2 Reinforcement Learning._ Reinforcement learning is currently a dominating method in embodied learning. It enables agents to learn policies by interacting with environments through trial-and-error, making it well-suited for dynamic and uncertain settings[139]. At each time step _𝑡_ , the agent observes a state _𝑠_ and selects an action _𝑎_ according to its policy _𝜋_ ( _𝑎_ | _𝑠_ ). After action execution, the agent receives a reward _𝑟_ from the reward function _𝑅_ ( _𝑠,𝑎,𝑔_ ), the environment transitions to a new state _𝑠_<sup>′</sup> according to the state transition probability _𝑇_ ( _𝑠_<sup>′</sup> | _𝑠,𝑎_ ), yielding an observation _𝑜_<sup>′</sup> ∼ _𝑂_ ( _𝑜_<sup>′</sup> | _𝑠_<sup>′</sup> _,𝑎_ ). The objective function of reinforcement learning is to maximize the expected cumulative reward: 


where _𝛾_ ∈[0 _,_ 1) is a discount factor balancing immediate and long-term rewards. Reinforcement learning excels in optimizing policies for complex tasks, but requires extensive explorations, which is computationally costly. A hybrid approach combining imitation learning and reinforcement learning can improve the issue, where imitation learning provides initial policies to reduce explorations, and reinforcement learning refines them through interactions with environments. 

_5.1.3 Transfer Learning._ In scenarios where training from scratch requires extensive samples and time, transfer learning can be applied to alleviate the effort[152]. It allows agents to accelerate learning on related target tasks using the knowledge from source tasks. By transferring learned policies, features, or representations from source tasks, the agents enhance efficiency and generalization on target tasks. Given a source task with a state-action space defined by state _𝑠_ ∈ _𝑆_ , action _𝑎_ ∈ _𝐴_ , and the policy _𝜋_ ( _𝑎_ | _𝑠_ ), transfer learning adapts the source policy _𝜋𝑠_ to a target task with different dynamics or goals. The objective is to minimize the divergence between the source policy _𝜋𝑠_ and the target policy _𝜋𝑡_ , by fine-tuning the policy using a small number of target task data. The process is guided by the task-specific loss of the target task, constrained by the Kullback-Leibler (KL) divergence for policy alignment: 


where _𝜃𝑡_<sup>∗represents the optimal policy parameters for the target task,</sup><sup>_𝜃𝑠_and</sup><sup>_𝜃𝑡_are the parameters</sup> of the source and the target policies, respectively, _𝐷𝐾𝐿_ measures the divergence between the source policy _𝜋𝑠_ and the target policy _𝜋𝑡_ , L _𝑡_ is the task-specific loss of the target task, and _𝜆_ is a regularization parameter balancing policy alignment and task performance. This process ensures that the transferred knowledge aligns with the target task’s state transition probability _𝑇_ ( _𝑠_<sup>′</sup> | _𝑠,𝑎_ ) and reward function _𝑅_ ( _𝑠,𝑎,𝑔_ ). In embodied settings, transfer learning enables agents to reuse learned behaviors across different environments and goals, reducing training time. However, significant 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

27 

disparities between source and target tasks may lead to negative transfer, where performance degrades due to mismatched knowledge. 

_5.1.4 Meta-Learning._ Meta-learning can also be used in embodied AI, enabling agents to learn how to learn[51, 66], so that they can swiftly infer optimal policies for new tasks from a small number of samples. At each time step _𝑡_ , the agent receives an observation _𝑜_ ∈ Ω and a goal _𝑔_ , and selects an action _𝑎_ according to the meta-policy that adapts to task-specific dynamics defined by the state transition probability _𝑇_ ( _𝑠_<sup>′</sup> | _𝑠,𝑎_ ) and the reward function _𝑅_ ( _𝑠,𝑎,𝑔_ ). The objective is to optimize the expected performance across tasks by minimizing the loss on task-specific data. In the context of Model-Agnostic Meta-Learning (MAML)[52], this is achieved by learning an initial set of model parameters _𝜃_ that can be adapted quickly to new tasks with minimal updates. Specifically, for a set of tasks T _𝑖_ , MAML optimizes the meta-objective as: 


where _𝜃_<sup>∗</sup> represents the optimal meta-policy parameters, L T _𝑖_ is the task-specific loss, _𝑓𝜃_ is the model parameterized by _𝜃_ , _𝜃𝑖_ is the task-specific parameters after gradient updates with the learning rate _𝛼_ , and the outer optimization minimizes the expected loss across tasks after adaptation. Meta-learning can enable agents to quickly adapt to new tasks by fine-tuning a pretrained model using a small number of demonstrations or interactions. The meta-policy can be embedded in a large model and refined during training to handle diverse tasks. Despite the strengths, meta-learning requires substantial pretraining and large samples across tasks, posing challenges in establishing a universal learning policy, particularly when tasks vary significantly in state spaces or dynamics. 

# **5.2 Imitation Learning Empowered by Large Models** 

The primary objective of imitation learning is to enable agents to achieve expert-level performance by mimicking their actions from demonstrators. Imitation learning can be realized by different approaches, including behavior cloning[53], inverse reinforcement learning[135], generative adversarial imitation learning[79], and hierarchical imitation learning[12], each contributing to the construction of policy networks. Among these approaches, behavior cloning stands out as the most important one, which formulates imitation learning as a supervised regression task. Given observations _𝑜_ ∈ Ω and goals _𝑔_ ∈ _𝐺_ , the policy network _𝜋_ predicts the expected actions _𝑎_ ∈ _𝐴_ . 

The policy network _𝜋_ needs to accurately map observations _𝑜_ and goals _𝑔_ to actions _𝑎_ , so as to ensure high imitation fidelity, even in complex, dynamic, partially observable environments. Beyond replication, imitation learning seeks to endow agents with the ability to generalize to unseen states, goals, or environments. The generalization ability is essential for real-world applications, such as robotic manipulation, autonomous navigation, and human-robot interaction, where environmental dynamics and task requirements often deviate from training scenarios. Additionally, imitation learning aims to ensure robustness against distribution shifts, where small errors in action predictions do not accumulate to cause significant deviations from the expert’s trajectories, particularly in stochastic or dynamic settings. Finally, imitation learning strives for sample efficiency, trying to enable agents to learn effective policies from a limited number of expert demonstrations, reducing the dependency on extensive, high-quality datasets. 

Behavior cloning still have difficulties in meeting these requirements to build a robust policy[204]. Its dependence on high-quality expert demonstrations hampers generalization to unseen states or goals. Expert demonstrations often exhibit randomness, multimodality and complexity, which are difficult for policy networks to capture, leading to compromised imitation fidelity and degraded 

Liang et al. 

28 


Fig. 13. Imitation learning empowered by diffusion models or Transformers. 

performance. Recent advances in large models have significantly enhanced behavior cloning, addressing its inherent limitations. As illustrated in Fig. 13, **large models empower imitation learning in the following aspects: (1) use diffusion models to construct policy networks; (2) use Transformer to construct policy networks.** 

_5.2.1 Diffusion-based Policy Network._ Diffusion models are excellent in handling complex multimodal distributions[40]. They can be used to generate diverse action trajectories, so as to enhance robustness and expressiveness of policies. Recent researches have started to integrate diffusion models into policy networks to overcome the limitations of traditional imitation learning. Pearce[142] proposes a diffusion model-based imitation learning framework, which incorporates diffusion models into policy networks. By optimizing expert demonstrations iteratively through noise addition and removal, the framework can capture the diversity of action distributions and generate diverse action sequences. DABC[34] adopts a two-stage process to train the policy network with the empowerment of a diffusion model. It first pretrains a base policy network through behavior cloning, then refines the modeling of action distributions via a diffusion model. Diffusion Policy[36] proposes a policy network that takes the diffusion model as the decision model for vision-driven robot tasks. It uses visual input and robot’s current state as conditions, employs U-Net as denoising network, predicts denoising steps based on visual features and state vectors, thereby generating continuous action sequences. To enhance the spatial perception capabilities of the policy network, 3D-Diffusion[217] proposes a diffusion policy framework based on 3D inputs. It uses simple 3D representations as inputs, leverages a diffusion model to generate action sequences, thus improving the generalization of visual motion policies by capturing spatial information. Compared to 2D policy networks, 3D-Diffusion can better understand geometric relationships and spatial constraints in 3D environments. 

_5.2.2 Transformer-based Policy Network._ Transformer architectures can empower imitation learning by treating expert trajectories as sequential data and utilizing self-attention mechanisms to model dependencies between actions, states and goals. This end-to-end approach minimizes error accumulation in intermediate steps, enhancing consistency and accuracy of policies. Google’s RT-1[20] is the first to demonstrate the potential of Transformers in robot control. By combining a large-scale, diverse dataset (130k+ trajectories, 700+ tasks) with a pretrained vision-language 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

29 

model, it significantly improves task generalization for unseen tasks and scenes. Subsequent work RT-Trajectory[62] introduces the “trajectory sketch” method, incorporating low-level visual cues to enhance the task generalization capabilities of end-to-end Transformers. Stanford University’s ALOHA[224] utilizes the encoding-decoding structure of Transformers to generate robotic arm action sequences from multi-view images, achieving precise double-arm operations with low-cost hardware. Its follow-up research uses an action chunking strategy to predict multistep action sequences, significantly improving the stability and consistency of long-term tasks. Mobile ALOHA[58] extends the original task to whole-body coordinated mobile operation tasks, introducing a mobile platform and a teleoperation interface to handle more complex dual-arm tasks. For 3D spatial operations, HiveFormer[224] and RVT[60] utilize multi-view data and CLIP for visual-language feature fusion and directly predict 6D grasp poses, achieving state-of-the-art performance on RLBench and real-world robotic arm tasks, highlighting the advantages of Transformers in complex spatial modeling. To grasp deformable objects (e.g., fabric or soft materials), Man proposes a Transformer framework combining visual and tactile feedback, optimizing grasp parameters through exploratory actions. Google’s RoboCat[19] employs cross-task, cross-entity embodied imitation learning, integrating VQ-GAN[50] to tokenize visual inputs, utilizing Decision Transformer to predict actions and observations, achieving rapid policy generalization with only a few samples. RoboAgent[17] adopts a similar encoding-decoding structure, fusing vision, task descriptions, and robot states to minimize action sequence prediction errors. CrossFormer[44] proposes a Transformer-based imitation learning architecture for cross-embodied tasks, trained on large-scale expert data to unify the processing of manipulation, navigation, mobility, and aerial tasks, demonstrating the potential of multi-task learning. 

# **5.3 Reinforcement Learning Empowered by Large Models** 

Through interactions with environments, reinforcement learning[11] allows agents to develop optimal control strategies, adapt to diverse unseen scenarios, maintain robustness in dynamic environments, and learn from limited data, thereby enabling sophisticated tasks in the real world. Initially reinforcement learning is based on fundamental techniques, such as policy search and value function optimization, exemplified by Q-learning[194] and State Action Reward State Action (SARSA)[164]. With the dominance of deep learning, reinforcement learning is integrated with deep neural networks, known as Deep Reinforcement Learning (DRL). DRL allows agents to learn intricate policies from high-dimensional inputs, leading to significant accomplishments, e.g., AlphaGo[174] and Deep Q-Network (DQN)[130]. DRL enables agents to learn autonomously in new environments, without explicit human interventions, thus allowing for wide applications ranging from gaming to robot control and beyond. Subsequent advances further improve the learning effects. Proximal Policy Optimization (PPO)[166] improves stability and efficiency of policy optimization through a clipped probability ratio. Soft Actor-Critic (SAC)[68] improves exploration and robustness by incorporating a maximum entropy framework. 

Despite these progresses, reinforcement learning still faces limitations in constructing policy networks _𝜋_ and designing reward functions _𝑅_ ( _𝑠,𝑎,𝑔_ ). **Recent advances in large models empower reinforcement learning in the following aspects: (1) improve reward function design; (2) optimize policy network construction by modeling complex action distributions.** They are as illustrated in Fig. 14. 

_5.3.1 Reward Function Design._ Designing reward function has been a challenge for reinforcement learning[49], due to its complexity and task-specific nature. Traditional reward functions are designed manually by domain experts, requiring comprehensive consideration of factors and expertise, such as task completion, energy consumption, safety, and weigh of each factor, which is 

Liang et al. 

30 


Fig. 14. Reinforcement learning empowered by large models. 

quite difficult. Manual design often leads to sparse or poorly scaled rewards, causing issues like reward hacking, where the agent exploits unintended signals to maximize the reward without achieving the intended goal. 

Large models offer a promising solution by generating **(1) reward signals** _𝑟_ or **(2) reward function** _𝑅_ ( _𝑠,𝑎,𝑔_ ), reducing reliance on manual design and capturing complex multimodal feedback. Kwon et al. and Language to Rewards (L2R)[215] introduce zero-shot and few-shot approaches respectively, utilizing GPT-3 to produce reward signals directly from textual behavior prompts, translating high-level goals to hardware-specific control policies. However, their sparse rewards restrict the usage in complex tasks and successful generation depends heavily on precise prompts or specific templates. Text2Reward[205] improves this by generating dense interpretable Python reward functions from environment descriptions and examples, iteratively refining them via human feedback, achieving high success rates across robotic manipulation and locomotion tasks. Eureka[120] leverages GPT-4 to create dense rewards from task and environment prompts. It mitigates Text2Reward’s reliance on human feedback by employing an automated iterative strategy for reward function optimization, surpassing human-crafted rewards. Further, Auto MC-Reward[106] implements full automation with a multi-stage pipeline for Minecraft, where a reward designer generates reward signals, a validator ensures quality, and a trajectory analyzer refines rewards through failure-driven iterations. Auto MC-Reward boosts the efficiency significantly, but its domain-specific focus constrains its generalization compared to Eureka and Text2Reward. 

_5.3.2 Policy Network Construction._ Offline reinforcement learning learns[101] optimal policies from pre-collected datasets without online interactions. But the reliance on static datasets may result in errors for actions absent from the datasets. Policy regularization may mitigate this problem by constraining deviations from behavior policy. But limitations in policy expressiveness and sub-optimal regularization methods may cause under-performance. To enhance expressiveness and adaptability of offline reinforcement learning, researchers propose to **exploit (1) diffusion models, (2) Transformer-based architectures, and (3) LLMs to empower the construction of policy networks** , as illustrated in Fig. 15. 

_Policy network construction with diffusion models._ Diffusion models[40] enhance policy expressiveness by modeling complex action distributions through iterative noising and denoising. DiffusionQL[193] employs diffusion models as foundation policy, modeling action distributions and training to maximize value function objectives within the Q-learning framework. This approach generates high-reward policies that fit multimodal or non-standard action distributions in offline datasets. 

31 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 


Fig. 15. Policy network construction empowered by large models. 

However, diffusion models require a large number of denoising steps to produce actions from fully noised states. To alleviate the effort, EDP[91] introduces an efficient sampling method that reconstructs actions from intermediate noised states in a single step, significantly reducing the computational overhead. EDP can integrate with various offline reinforcement learning frameworks, enhancing sampling efficiency while maintaining policy expressiveness. 

_Policy network construction with Transformer-based architectures._ Transformer-based architectures leverage the self-attention mechanism to capture long-term dependencies in trajectories, thereby improving policy flexibility and accuracy. Decision Transformer[31] re-frames offline reinforcement learning as a conditional sequence modeling problem, treating state-action-reward trajectories as sequential inputs, and applies supervised learning to generate optimal actions from offline datasets. Based on it, Prompt-DT[207] enhances generalization in few-shot scenarios by incorporating prompt engineering, using trajectory prompts with task-specific encoding to guide action generation for new tasks. To improve adaptability in dynamic environments, Online Decision Transformer (ODT)[228] pretrains Transformer via offline reinforcement learning to learn sequence generation, then fine-tunes it through online reinforcement learning interactions. Q-Transformer[30] integrates Transformer’s sequence modeling with Q-function estimation, learning Q-values autoregressively to generate optimal actions. In multi-task offline reinforcement learning, Gato[158] adopts a Transformer-based sequence modeling approach, but it relies heavily on dataset optimality and incurs high training cost due to large parameters. 

_Policy network construction with LLM._ Built upon the sequence modeling capabilities of Transformers, LLM introduces a new paradigm by leveraging pretrained knowledge to streamline offline reinforcement learning tasks. GLAM[28] uses LLM as policy agents, generating executable action sequences for language-defined tasks, which are optimized online via PPO with contextual memory for improved sequence consistency in long-horizon planning. LaMo[169] employs GPT-2 as base policy, which is fine-tuned with LoRA to preserve prior knowledge, converting state-action-reward sequences into language prompts for task-aligned policy generation. Reid[159] explores LLM’s transferability using pretrained BERT, which is fine-tuned for specific tasks and augmented by external knowledge bases. Evaluations on D4RL benchmarks[57] show that Reid outperforms Decision Transformer meanwhile reducing training time, demonstrating LLM’s efficiency in offline reinforcement learning. 

Liang et al. 

32 


Fig. 16. World models and applications in decision-making and embodied learning. 

# **6 WORLD MODELS** 

World models serve as internal simulations or representations of environments. With world models, intelligent systems can anticipate future states, comprehend cause-and-effect relationships, and make reasonable decisions, without solely relying on real-world interactions, which is expensive and often infeasible. Providing a rich cognitive framework, world models facilitate more efficient learning, decision-making, and adaptation in complex dynamic environments, thereby enhancing agents’ capacities to execute sophisticated tasks. In this section, we investigate the design of world models and examine how they contribute to decision-making and embodied learning. 

# **6.1 Design of World Models** 

The concept of world model can be traced back to reinforcement learning[233]. Traditional RL relies on repeated agent-environment interactions, incurring high computational costs, hence impractical in data-scarce or complex scenarios. Instead of learning behaviors solely through repeated interactions, world models enable agents to learn in a simulated environment. This approach is especially valuable in data-scarce or complex scenarios. In terms of design, current world models can be categorized into four types: latent space world model, Transformer-based world model, diffusion-based world model, and joint embedding predictive architecture, as shown in the upper part of Fig. 16. 

_6.1.1 Latent Space World Model._ The latent space world model is represented by Recurrent State Space Model (RSSM)[67, 69], which facilitates predictions in latent spaces. RSSM learns dynamic environment models from pixel observations and plans actions in encoded latent spaces. By decomposing the latent state into stochastic and deterministic parts, RSSM considers both deterministic 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

33 

and stochastic factors of the environment. Due to RSSM’s exceptional performance in continuous control tasks of robots, many works based on RSSM emerged. PlaNet[71] employs RSSM with a Gated Recurrent Unit (GRU) and a Convolutional Variational AutoEncoder (CVAE), leveraging CNN for latent dynamics and model predictive control. Dreamer[70] advances it by learning the actor and the value networks from latent representations. Dreamer V2[72] further uses the actor-critic algorithm to learn the behaviors purely from the imagined sequences generated by the world model, achieving performance comparable to human players on the Atari 200M benchmark. Dreamer V3[73] enhances stability with symlog predictions, layer normalization, and normalized returns via exponential moving average, outperforming specialized algorithms in continuous control tasks. 

_6.1.2 Transformer-based World Model._ Latent space world models usually rely on CNN or Recurrent Neural Networks (RNN), hence they face challenges when operating in high-dimensional, continuous, or multimodal environments. Transformer-based world models offer a powerful alternative. They leverage the attention mechanism to model multimodal inputs, overcoming the limitations of CNN and RNN, exhibiting superior performance, particularly in complex memoryinteraction tasks. IRIS[129] is one of the first to apply Transformer in world models, where agents learn skills within an autoregressive Transformer-based world model. IRIS tokenizes images using a Vector Quantized Variational Autoencoder (VQ-VAE) and employs an autoregressive Transformer to predict future tokens, showing exceptional performance in low-data Atari 100k settings. Google’s Genie[24], built on spatial-temporal Transformer[206] and trained on vast unlabeled Internet video datasets via self-supervised learning, outperforms traditional RSSM. Genie provides a new paradigm for manipulable, generative, interactive environments, highlighting the transformative potential of Transformer. TWM[162] proposes a Transformer-XL-based world model. It migrates Transformer-XL’s segment-level recurrence mechanism to world model, enabling the capture of long-term dependencies between the states of the environment. To further enhance efficiency, TWM trains a model-free agent within the latent imagination, avoiding full inference during runtime. STORM[222] utilizes a stochastic Transformer, thus not relying on look-ahead search on Atari 100k benchmark. It fuses state and action into a single token, which improves training efficiency and matches the performance of Dreamer V3 on Atari 100k benchmark. These Transformer-based world models discretize states, actions, and observations into sequences, leveraging self-attention to capture long-term dependencies, significantly improving prediction accuracy, sample efficiency, and adaptability across tasks. 

_6.1.3 Diffusion-based World Model._ Diffusion-based world models, exemplified by OpenAI’s Sora[22], represent a significant advance in generating predictive video sequences in the original image space. Distinct from latent space world models and Transformer-based world models, Sora leverages an encoding network to convert videos and images into tokens, followed by a large-scale diffusion model that applies noising and denoising processes to these tokens, subsequently mapping them back to the original image space to produce multi-step image predictions based on language descriptions. This capability makes Sora highly applicable to embodied tasks. For example, Sora can generate trajectory videos for agents across future time steps using robot task descriptions and trajectory priors, enhancing model-based reinforcement learning. UniPi[47] employs diffusion models to model agent trajectories in image space, generating future key video frames from language inputs and initial images, followed by super-resolution in time series to create consistent, high-quality image sequences. UniSim[212] further improves trajectory prediction by jointly training diffusion models on Internet data and robot interaction videos, enabling prediction of long-sequence video trajectories for both high-level and low-level task instructions. 

Liang et al. 

34 

_6.1.4 Joint Embedding Predictive Architecture._ The above data-driven world models excel in natural language processing tasks, but lack real-world common sense due to their reliance on training data. The Joint Embedding Predictive Architecture (JEPA)[102], proposed by Yann LeCun at Meta, is a groundbreaking approach to overcome the limitations regarding common sense. Inspired by human brains’ efficient learning, JEPA introduces hierarchical planning and self-supervised learning in a high-level representation space. Hierarchical planning breaks complex tasks into multiple abstraction levels, each addressing specific sub-tasks to simplify decision-making and control, focusing on semantic features rather than pixel-level outputs as traditional generative models do. Through self-supervised learning, JEPA trains networks to predict missing or hidden input data, enabling pretraining on large unlabeled datasets and fine-tuning for diverse tasks. JEPA’s architecture comprises a perception module and a cognitive module, forming a world model using latent variables to capture essential information while filtering redundancies, supporting efficient decision-making and future scenario planning. By incorporating a dual-system concept, JEPA balances “fast” intuitive reactions with “slow” deliberate reasoning. This combination of hierarchical planning, self-supervised learning, and a robust world model makes JEPA a scalable, cognition-inspired framework for complex, real-world environments. 

# **6.2 World Model in Decision-Making** 

World models can provide agents with powerful internal representations, enabling them to predict environmental dynamics and potential outcomes before taking actual actions. For decision-making, it plays two main roles: **(1) simulated validation** and **(2) knowledge augmentation** , as shown in the left of Fig. 16. Through these mechanisms, world models can improve agents’ ability to plan and execute tasks in complex dynamic environments significantly. 

_6.2.1 World Model for Simulated Validation._ In robotics, testing decisions can be incredibly expensive and time-consuming, especially the sequential and long-term tasks, where current decisions profoundly affect future performances. World models can mitigate this issue by enabling simulated validation, allowing agents to “try out” actions and observe the likely consequences without realworld commitments. This simulated validation dramatically shortens iteration time and facilitates safe testing of corner cases or high-risk scenarios that would be impractical otherwise. The ability to predict how actions affect future environmental states helps agents to identify and avoid potential mistakes, ultimately optimizing performance. NeBula[3] constructs probabilistic belief spaces using Bayesian filtering, which allows robots to reason effectively across diverse structural configurations, including unknown environments, offering a sophisticated way to predict outcomes under uncertainty. UniSim[212] is a generative simulator for real-world interactions, which can simulate the visual outcomes of both high-level instructions and low-level controls. It contains a unified generative framework that takes actions as input, integrating diverse datasets across different modulations. 

_6.2.2 World Model for Knowledge Augmentation._ To successfully accomplish real-world tasks, agents often require rich knowledge and environmental common sense. World models can augment agents with predictive and contextual knowledge essential for strategy planning. By predicting future environmental states or enriching agents’ understanding of the world, world models enable agents to anticipate outcomes, avoid mistakes, and optimize performance over time. The World Knowledge Model (WKM)[146] imitates humans’ mental world knowledge by providing global prior knowledge before a task and maintaining local dynamic knowledge during the task. It synthesizes global task knowledge and local state knowledge from experts and sampled trajectories, achieving superior planning performance when integrated with LLM. Agent-Pro[221] transforms an agent’s interactions with its environment (especially with other agents in interactive tasks) into “beliefs”. 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

35 

These beliefs represent the agent’s social understanding of the environment and inform subsequent decisions and behavioral strategy updates. GovSim[144] explores the emergence of cooperative behaviors within societies of LLM agents. These agents gather information about the external world and other agents’ strategies through multi-agent conversations, implicitly forming their own high-level insights and representations of the world model. 

# **6.3 World Model in Embodied Learning** 

Apart from decision making, world models can enable agents to learn new skills and new behaviors efficiently. Different from model-free reinforcement learning, which often incurs high computational costs and data inefficiency from direct agent-environment interactions, model-based reinforcement learning leverages world models to streamline the learning process by **(1) simulating state transitions** and **(2) generating data** , as shown in the right of Fig. 16. 

_6.3.1 World Model for State Transitions._ Traditional reinforcement learning is model-free and learns directly from agent-environment interactions, which is computationally intensive and impractical in data-scarce or complex scenarios. Model-based reinforcement learning alleviates these limitations by leveraging a world model that explicitly captures state transitions and dynamics, allowing agents to enhance their learning process from simulated environments for safe, cost-effective and data-efficient training. The world model creates virtual representations of the real world, so that the agents can explore hypothetical actions and refine policies without inherent risks or costs associated with real-world interactions. RobotDreamPolicy[145] learns a world model and develops the policy within it, drastically reducing interactions with the real environment. DayDreamer[202] leverages Dreamer V2, an RSSM-based world model, to encode observations into latent states and predict future states, achieving rapid skill learning in real robots with high sample efficiency. SWIM[128] takes a step further by utilizing Internet-scale human video data to understand rich human interactions and gain meaningful affordances. It is initially trained on a large dataset of egocentric videos and then fine-tuned with robot data to adapt to robot domains. Subsequently, behaviors for specified tasks can be learned efficiently with this world model. 

_6.3.2 World Model for Data Generation._ Beyond empowering learning and optimizing policies, world models, especially diffusion-based world models, can be used to synthesize data, which is particularly valuable for embodied AI as collecting diverse and extensive real-world data is challenging. Diffusion-based World models can synthesize realistic trajectory data, state representations, and dynamics, thereby augmenting existing datasets or creating entirely new datasets to enhance learning processes. SynthER[118] utilizes diffusion-based world models to generate low-dimensional offline RL trajectory data to augment the original datasets. Their evaluations demonstrate that the diffusion models can effectively learn state representations and dynamical equations from trajectory data. MTDiff[77] applies diffusion-based world models to generate multi-task trajectories, using expert trajectories as prompts to guide the generation of agent trajectories that align with specific task objectives and dynamics. VPDD[76] trains the trajectory prediction world models using a large-scale human operation dataset, and then fine-tunes the action generation module with only a small amount of labeled action data, significantly reducing the need of extensive robot interaction data for policy learning. 

# **7 CHALLENGE AND FUTURE PROSPECTS** 

Embodied intelligence presents unprecedented opportunities far beyond virtual confines. However, challenges still exist. In this section, we discuss the major open issues of scarcity of high-quality embodied data, continual learning for long-term adaptability, computational and deployment 

Liang et al. 

36 

efficiency, and sim-to-real gap. By investigating the core challenges, we point out the potential research directions towards robust, adaptable, and truly intelligent embodied systems. 

# **7.1 Scarcity of Embodied Data** 

Training embodied intelligent agents requires vast and diverse datasets. RT-X[186] collected robot arm data from over 60 laboratories and built the open X-Embodiment dataset. AutoRT[5] proposed systems for automatic data collection in new environments. However, real-world robotic data is still insufficient. The reasons lie in the immense diversity in robot designs, the intricate nature of real-world interactions, and the specific requirements of various tasks, etc. The state-of-theart embodied datasets, e.g., VIMA[89] (with 650,000 demonstrations) and RT-1[28] (with 130,000 demonstrations), are still dwarfed by their vision-language counterparts, such as LAION-5B (with 5.75 billion text-image pairs). To address the issue of embodied data scarcity, researchers have tried various solutions. 

- (1) Leverage world models, particularly diffusion-based world models, to synthesize new data from existing agent experiences. SynthER[118] utilizes a diffusion-based world model to synthesize data and augment offline RL trajectory datasets, significantly enhancing performance in both offline and online settings. 

- (2) Integrate large human datasets. Ego4D[61] provides rich real-world dynamics and observations gleaned from Internet-sourced videos. This approach helps improve the contextual understanding for robotic tasks by leveraging common human behaviors and interactions. However, due to the morphological differences between humans and robots, directly transferring human actions to robots often results in misalignment and reduced transferability. 

Data generation via world models emphasizes data quality and diversity, while human data integration leverages real-world context. They still face the challenges of reality gap, computational costs, and alignment issues. 

# **7.2 Continual Learning** 

Embodied intelligent systems should be able to autonomously update knowledge and optimize strategies through ongoing interactions with open dynamic environments, meanwhile maintaining previously acquired capabilities across evolving tasks and conditions. This ability can be achieved by continual learning[127]. Without continual learning, an intelligent agent needs to be retrained for every new scenario or slight environmental change, severely limiting its real-world utility. However, significant obstacles exist for continual learning. 

- (1) Catastrophic forgetting[141] remains a core issue, where learning new tasks degrades prior knowledge. For instance, a robot perfectly trained for navigation on flat surfaces may lose its proficiency when subsequently tasked with rugged terrain, limiting the robot’s accumulation of experiences. 

- (2) Efficient autonomous exploration is difficult, as current methods still struggle to balance exploring new experiences and exploiting existing knowledge effectively, especially in highdimensional state spaces or scenarios with sparse rewards. 

- (3) Inherent unpredictability of the real world, including sensor degradation or mechanical wear, further complicates continual learning, necessitating robust self-diagnostic and self-repair capabilities of agents. 

To address these challenges, researchers are exploring various approaches. **Experience replay** [10] can mitigate catastrophic forgetting by periodically revisiting historical data. **Regularization techniques** [98] preserve prior task knowledge by constraining weight updates during new task learning. **Data mixing strategies** [100] integrate varying proportions of prior data distributions 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

37 

with new data to reduce feature distortion. Frameworks such as CycleResearcher[199] facilitate embodied learning in complex processes by **optimizing policy and reward models** . Future advances may include **enhance self-supervised learning** to drive active exploration via intrinsic motivation, and **incorporate multi-agent collaboration mechanisms** to accelerate individual learning through collective interactions. 

# **7.3 Computation and Deployment Efficiency** 

The increasingly sophisticated models of embodied intelligence demand substantial computational resources for training and deployment. For instance, DiffusionVLA[22] requires hundreds of highend GPUs and weeks of training on million-scale trajectory datasets, with computations reaching petaflops (PFLOPs). Its iterative sampling during inference results in a latency of several seconds, which is an impediment for real-time control applications in robotics. The Transformer-based VLA RT-2[234] maintains a complex architecture that demands approximately 20GB of video memory. Although RT-2 has reduced training costs through pretraining, this high memory requirement complicates the deployment on resource-constrained edge devices, such as actual robots. Cloudbased deployment as an alternative is often impractical due to the concerns regarding data privacy, security, and real-time operational constraints inherent in physical robot interactions. To mitigate these challenges, several strategies are being explored. 

- (1) Parameter-Efficient Fine-Tuning (PEFT) methods, such as LoRA[82], significantly reduce finetuning costs. By updating only low-rank matrices, they can achieve the training costs approximately 1/10 of full fine-tuning. However, this efficiency may compromise the performance on highly complex tasks. 

- (2) Model compression techniques, including knowledge distillation ad quantization, can be leveraged to deploy large models on limited hardware. TinyVLA employs knowledge distillation to compress the large model to approximately 10 million parameters. Combined with fast sampling algorithms and 4-bit quantization, TinyVLA[234] achieves an impressive 30ms inference latency and a 2GB memory footprint, making it viable for edge devices. 

- (3) Hardware acceleration offers another solution for efficiency, as MiniGPT-4[232] does. Although providing immediate performance gains, hardware-specific optimizations often lack generalization across different platforms. 

Optimizing large-scale models through compression techniques and designing inherently lightweight architectures are the most feasible approaches to achieve effective and widespread deployment of embodied AI on edge devices. 

# **7.4 Sim-to-Real Gap** 

Embodied AI requires a huge amount of data to train the agents. However, it is prohibitively expensive or impractical to collect such real-world data for diverse embodiments. Simulators alleviate this problem by enabling the agents to train on large and diverse simulated datasets[163], which proves to be a cost-effective and scalable solution. After training in simulators, the agents are deployed in real-world settings through sim-to-real transfer. 

However, sim-to-real transfer suffers from the “sim-to-real gap”[187], due to fundamental discrepancies between simulated and real-world environments. These discrepancies manifest in various forms, such as inaccurate physical dynamics[33] and differences in visual rendering[14]. For example, friction, collision, and fluid behaviors are difficult to model accurately; lighting, camera exposure, and material properties are difficult to simulate. An agent trained in a simulated environment often fails unexpectedly when confronted with the subtle imperfections and complexities of the real world, as simulation cannot fully replicate reality. Therefore, well-trained policies may fail 

Liang et al. 

38 

in out-of-distribution scenarios in the real world. Furthermore, modeling real-world environments accurately is inherently challenging[41]. Slight differences between the simulated and the real world tend to accumulate in long-term decision-making, resulting in policies that are not robust or adaptable to environmental changes. 

Advanced simulators, such as the differentiable and highly realistic Genesis[134], are working actively to narrow this gap through precise physics modeling and photorealistic rendering, thereby increasing the transferability of agents from simulators to the real world. Nonetheless, bridging the sim-to-real gap remains a major challenge for robust embodied AI. 

# **8 CONCLUSIONS** 

Advent of large models endows embodied agents with great intelligent capabilities. In this article, we conduct a comprehensive survey on techniques and recent advances in embodied AI, focusing on autonomous decision-making and embodied learning empowered by large models. We begin the survey by introducing the preliminary knowledge of embodied AI and various major large models, reviewing their recent developments and applications on embodied intelligence. We then elaborate on the decision-making methodologies of embodied AI, detailing both hierarchical and end-to-end paradigms, their underlying mechanisms, and the latest advances. Afterwards, we review the embodied learning mechanisms, focusing on imitation learning and reinforcement learning, particularly how the large models empower them. Subsequently, we introduce the world models, presenting their design methods and their vital roles in decision-making and embodied learning. Finally, we discuss the open challenges in embodied intelligence, including embodied data scarcity, continual learning, computation and deployment efficiency, and sim-to-real gap, along with the potential solutions. Through this systematic investigation, we provide researchers and engineers with an in-depth summarization and analysis of status-quo and open challenges in the field of embodied AI, meanwhile figuring out the potential directions to the path towards artificial general intelligence. 

# **REFERENCES** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. 2023. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ (2023). 

- [2] Abdul Afram and Farrokh Janabi-Sharifi. 2014. Theory and applications of HVAC control systems–A review of model predictive control (MPC). _Building and environment_ 72 (2014), 343–355. 

- [3] Ali Agha, Kyohei Otsu, Benjamin Morrell, David D Fan, Rohan Thakker, Angel Santamaria-Navarro, Sung-Kyun Kim, Amanda Bouman, Xianmei Lei, Jeffrey Edlund, et al. 2021. Nebula: Quest for robotic autonomy in challenging environments; team costar at the darpa subterranean challenge. _arXiv preprint arXiv:2103.11470_ (2021). 

- [4] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, et al. 2022. Do as i can, not as i say: Grounding language in robotic affordances. _arXiv preprint arXiv:2204.01691_ (2022). 

- [5] Michael Ahn, Debidatta Dwibedi, Chelsea Finn, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Karol Hausman, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, et al. 2024. Autort: Embodied foundation models for large scale orchestration of robotic agents. _arXiv preprint arXiv:2401.12963_ (2024). 

- [6] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katherine Millican, Malcolm Reynolds, et al. 2022. Flamingo: a visual language model for few-shot learning. _Advances in neural information processing systems_ 35 (2022), 23716–23736. 

- [7] Shan An, Ziyu Meng, Chao Tang, Yuning Zhou, Tengyu Liu, Fangqiang Ding, Shufang Zhang, Yao Mu, Ran Song, Wei Zhang, et al. 2025. Dexterous manipulation through imitation learning: A survey. _arXiv preprint arXiv:2504.03515_ (2025). 

- [8] Rohan Anil, Andrew M Dai, Orhan Firat, Melvin Johnson, Dmitry Lepikhin, Alexandre Passos, Siamak Shakeri, Emanuel Taropa, Paige Bailey, Zhifeng Chen, et al. 2023. Palm 2 technical report. _arXiv preprint arXiv:2305.10403_ (2023). 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

39 

- [9] Daman Arora and Subbarao Kambhampati. 2023. Learning and leveraging verifiers to improve planning capabilities of pre-trained language models. _arXiv preprint arXiv:2305.17077_ (2023). 

- [10] Benedikt Bagus and Alexander Gepperth. 2021. An investigation of replay-based approaches for continual learning. In _2021 International Joint Conference on Neural Networks (IJCNN)_ . IEEE, 1–9. 

- [11] Andrew G Barto. 2021. Reinforcement learning: An introduction. by richard’s sutton. _SIAM Rev_ 6, 2 (2021), 423. 

- [12] Suneel Belkhale, Yuchen Cui, and Dorsa Sadigh. 2023. Hydra: Hybrid robot actions for imitation learning. In _Conference on Robot Learning_ . PMLR, 2113–2133. 

- [13] Guillaume Bellegarda, Yiyu Chen, Zhuochen Liu, and Quan Nguyen. 2022. Robust high-speed running for quadruped robots via deep reinforcement learning. In _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 10364–10370. 

- [14] Amanda Bertsch, Uri Alon, Graham Neubig, and Matthew Gormley. 2023. Unlimiformer: Long-range transformers with unlimited length input. _Advances in Neural Information Processing Systems_ 36 (2023), 35522–35543. 

- [15] Maciej Besta, Nils Blach, Ales Kubicek, Robert Gerstenberger, Michal Podstawski, Lukas Gianinazzi, Joanna Gajda, Tomasz Lehmann, Hubert Niewiadomski, Piotr Nyczyk, et al. 2024. Graph of thoughts: Solving elaborate problems with large language models. In _Proceedings of the AAAI conference on artificial intelligence_ , Vol. 38. 17682–17690. 

- [16] James Betker, Gabriel Goh, Li Jing, Tim Brooks, Jianfeng Wang, Linjie Li, Long Ouyang, Juntang Zhuang, Joyce Lee, Yufei Guo, et al. 2023. Improving image generation with better captions. _Computer Science. https://cdn. openai. com/papers/dall-e-3. pdf_ 2, 3 (2023), 8. 

- [17] Homanga Bharadhwaj, Jay Vakil, Mohit Sharma, Abhinav Gupta, Shubham Tulsiani, and Vikash Kumar. 2024. Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 4788–4795. 

- [18] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. 2024. _𝜋_ 0: A Vision-Language-Action Flow Model for General Robot Control. _arXiv preprint arXiv:2410.24164_ (2024). 

- [19] Konstantinos Bousmalis, Giulia Vezzani, Dushyant Rao, Coline Devin, Alex X Lee, Maria Bauzá, Todor Davchev, Yuxiang Zhou, Agrim Gupta, Akhil Raju, et al. 2023. Robocat: A self-improving generalist agent for robotic manipulation. _arXiv preprint arXiv:2306.11706_ (2023). 

- [20] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. 2022. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ (2022). 

- [21] Rodney Brooks. 2003. A robust layered control system for a mobile robot. _IEEE journal on robotics and automation_ 2, 1 (2003), 14–23. 

- [22] Tim Brooks, Bill Peebles, Connor Holmes, Will DePue, Yufei Guo, Li Jing, David Schnurr, Joe Taylor, Troy Luhman, Eric Luhman, et al. 2024. Video generation models as world simulators. _OpenAI Blog_ 1, 8 (2024), 1. 

- [23] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. 2020. Language models are few-shot learners. _Advances in neural information processing systems_ 33 (2020), 1877–1901. 

- [24] Jake Bruce, Michael D Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, et al. 2024. Genie: Generative interactive environments. In _Forty-first International Conference on Machine Learning_ . 

- [25] Paweł Budzianowski, Wesley Maa, Matthew Freed, Jingxiang Mo, Winston Hsiao, Aaron Xie, Tomasz Młoduchowski, Viraj Tipnis, and Benjamin Bolte. 2025. EdgeVLA: Efficient Vision-Language-Action Models. _arXiv preprint arXiv:2507.14049_ (2025). 

- [26] Yuji Cao, Huan Zhao, Yuheng Cheng, Ting Shu, Yue Chen, Guolong Liu, Gaoqi Liang, Junhua Zhao, Jinyue Yan, and Yun Li. 2024. Survey on large language model-enhanced reinforcement learning: Concept, taxonomy, and methods. _IEEE Transactions on Neural Networks and Learning Systems_ (2024). 

- [27] Mathilde Caron, Hugo Touvron, Ishan Misra, Hervé Jégou, Julien Mairal, Piotr Bojanowski, and Armand Joulin. 2021. Emerging properties in self-supervised vision transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ . 9650–9660. 

- [28] Thomas Carta, Clément Romac, Thomas Wolf, Sylvain Lamprier, Olivier Sigaud, and Pierre-Yves Oudeyer. 2023. Grounding large language models in interactive environments with online reinforcement learning. In _International Conference on Machine Learning_ . PMLR, 3676–3713. 

- [29] Yupeng Chang, Xu Wang, Jindong Wang, Yuan Wu, Linyi Yang, Kaijie Zhu, Hao Chen, Xiaoyuan Yi, Cunxiang Wang, Yidong Wang, et al. 2024. A survey on evaluation of large language models. _ACM transactions on intelligent systems and technology_ 15, 3 (2024), 1–45. 

- [30] Yevgen Chebotar, Quan Vuong, Karol Hausman, Fei Xia, Yao Lu, Alex Irpan, Aviral Kumar, Tianhe Yu, Alexander Herzog, Karl Pertsch, et al. 2023. Q-transformer: Scalable offline reinforcement learning via autoregressive q-functions. 

Liang et al. 

40 

In _Conference on Robot Learning_ . PMLR, 3909–3928. 

- [31] Lili Chen, Kevin Lu, Aravind Rajeswaran, Kimin Lee, Aditya Grover, Misha Laskin, Pieter Abbeel, Aravind Srinivas, and Igor Mordatch. 2021. Decision transformer: Reinforcement learning via sequence modeling. _Advances in neural information processing systems_ 34 (2021), 15084–15097. 

- [32] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. 2021. Evaluating large language models trained on code. _arXiv preprint arXiv:2107.03374_ (2021). 

- [33] Po-Lin Chen and Cheng-Shang Chang. 2023. Interact: Exploring the potentials of chatgpt as a cooperative agent. _arXiv preprint arXiv:2308.01552_ (2023). 

- [34] Shang-Fu Chen, Hsiang-Chun Wang, Ming-Hao Hsu, Chun-Mao Lai, and Shao-Hua Sun. 2023. Diffusion modelaugmented behavioral cloning. _arXiv preprint arXiv:2302.13335_ (2023). 

- [35] Ting Chen, Simon Kornblith, Mohammad Norouzi, and Geoffrey Hinton. 2020. A simple framework for contrastive learning of visual representations. In _International conference on machine learning_ . PmLR, 1597–1607. 

- [36] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. 2023. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ (2023), 02783649241273668. 

- [37] Hao-Tien Lewis Chiang, Zhuo Xu, Zipeng Fu, Mithun George Jacob, Tingnan Zhang, Tsang-Wei Edward Lee, Wenhao Yu, Connor Schenck, David Rendleman, Dhruv Shah, et al. 2024. Mobility vla: Multimodal instruction navigation with long-context vlms and topological graphs. _arXiv preprint arXiv:2407.07775_ (2024). 

- [38] WL Chiang et al. 2023. Vicuna: An Open-Source Chatbot Impressing GPT-4 With 90% ChatGPT Quality. Accessed: Apr. 14, 2023. 

- [39] Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, et al. 2023. Palm: Scaling language modeling with pathways. _Journal of Machine Learning Research_ 24, 240 (2023), 1–113. 

- [40] Florinel-Alin Croitoru, Vlad Hondru, Radu Tudor Ionescu, and Mubarak Shah. 2023. Diffusion models in vision: A survey. _IEEE transactions on pattern analysis and machine intelligence_ 45, 9 (2023), 10850–10869. 

- [41] Sahith Dambekodi, Spencer Frazier, Prithviraj Ammanabrolu, and Mark O Riedl. 2020. Playing text-based games with common sense. _arXiv preprint arXiv:2012.02757_ (2020). 

- [42] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2019. Bert: Pre-training of deep bidirectional transformers for language understanding. In _Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, volume 1 (long and short papers)_ . 4171–4186. 

- [43] Jingtao Ding, Yunke Zhang, Yu Shang, Yuheng Zhang, Zefang Zong, Jie Feng, Yuan Yuan, Hongyuan Su, Nian Li, Nicholas Sukiennik, et al. 2024. Understanding world or predicting future? a comprehensive survey of world models. _Comput. Surveys_ (2024). 

- [44] Ria Doshi, Homer Walke, Oier Mees, Sudeep Dasari, and Sergey Levine. 2024. Scaling cross-embodied learning: One policy for manipulation, navigation, locomotion and aviation. _arXiv preprint arXiv:2408.11812_ (2024). 

- [45] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, et al. 2020. An image is worth 16x16 words: Transformers for image recognition at scale. _arXiv preprint arXiv:2010.11929_ (2020). 

- [46] Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, et al. 2023. Palm-e: An embodied multimodal language model. (2023). 

- [47] Yilun Du, Sherry Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Josh Tenenbaum, Dale Schuurmans, and Pieter Abbeel. 2023. Learning universal policies via text-guided video generation. _Advances in neural information processing systems_ 36 (2023), 9156–9172. 

- [48] Jiafei Duan, Samson Yu, Hui Li Tan, Hongyuan Zhu, and Cheston Tan. 2022. A survey of embodied ai: From simulators to research tasks. _IEEE Transactions on Emerging Topics in Computational Intelligence_ 6, 2 (2022), 230–244. 

- [49] Jonas Eschmann. 2021. Reward function design in reinforcement learning. _Reinforcement learning algorithms: Analysis and Applications_ (2021), 25–33. 

- [50] Patrick Esser, Robin Rombach, and Bjorn Ommer. 2021. Taming transformers for high-resolution image synthesis. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . 12873–12883. 

- [51] Rasool Fakoor, Pratik Chaudhari, Stefano Soatto, and Alexander J Smola. 2019. Meta-q-learning. _arXiv preprint arXiv:1910.00125_ (2019). 

- [52] Chelsea Finn, Pieter Abbeel, and Sergey Levine. 2017. Model-agnostic meta-learning for fast adaptation of deep networks. In _International conference on machine learning_ . PMLR, 1126–1135. 

- [53] Pete Florence, Corey Lynch, Andy Zeng, Oscar A Ramirez, Ayzaan Wahid, Laura Downs, Adrian Wong, Johnny Lee, Igor Mordatch, and Jonathan Tompson. 2022. Implicit behavioral cloning. In _Conference on robot learning_ . PMLR, 158–168. 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

41 

- [54] Luciano Floridi and Massimo Chiriatti. 2020. GPT-3: Its nature, scope, limits, and consequences. _Minds and machines_ 30, 4 (2020), 681–694. 

- [55] Maria Fox and Derek Long. 2003. PDDL2. 1: An extension to PDDL for expressing temporal planning domains. _Journal of artificial intelligence research_ 20 (2003), 61–124. 

- [56] Gene F Franklin, J David Powell, Abbas Emami-Naeini, and J David Powell. 2002. _Feedback control of dynamic systems_ . Vol. 4. Prentice hall Upper Saddle River. 

- [57] Justin Fu, Aviral Kumar, Ofir Nachum, George Tucker, and Sergey Levine. 2020. D4rl: Datasets for deep data-driven reinforcement learning. _arXiv preprint arXiv:2004.07219_ (2020). 

- [58] Zipeng Fu, Tony Z Zhao, and Chelsea Finn. 2024. Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation. _arXiv preprint arXiv:2401.02117_ (2024). 

- [59] Michael Gelfond and Yulia Kahl. 2014. _Knowledge representation, reasoning, and the design of intelligent agents: The answer-set programming approach_ . Cambridge University Press. 

- [60] Ankit Goyal, Jie Xu, Yijie Guo, Valts Blukis, Yu-Wei Chao, and Dieter Fox. 2023. Rvt: Robotic view transformer for 3d object manipulation. In _Conference on Robot Learning_ . PMLR, 694–710. 

- [61] Kristen Grauman, Andrew Westbury, Eugene Byrne, Zachary Chavis, Antonino Furnari, Rohit Girdhar, Jackson Hamburger, Hao Jiang, Miao Liu, Xingyu Liu, et al. 2022. Ego4d: Around the world in 3,000 hours of egocentric video. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . 18995–19012. 

- [62] Jiayuan Gu, Sean Kirmani, Paul Wohlhart, Yao Lu, Montserrat Gonzalez Arenas, Kanishka Rao, Wenhao Yu, Chuyuan Fu, Keerthana Gopalakrishnan, Zhuo Xu, et al. 2023. Rt-trajectory: Robotic task generalization via hindsight trajectory sketches. _arXiv preprint arXiv:2311.01977_ (2023). 

- [63] Xianfan Gu, Chuan Wen, Weirui Ye, Jiaming Song, and Yang Gao. 2023. Seer: Language instructed video prediction with latent diffusion models. _arXiv preprint arXiv:2303.14897_ (2023). 

- [64] Lin Guan, Karthik Valmeekam, Sarath Sreedharan, and Subbarao Kambhampati. 2023. Leveraging pre-trained large language models to construct and utilize world models for model-based task planning. _Advances in Neural Information Processing Systems_ 36 (2023), 79081–79094. 

- [65] Yanjiang Guo, Yen-Jen Wang, Lihan Zha, and Jianyu Chen. 2024. Doremi: Grounding language model by detecting and recovering from plan-execution misalignment. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 12124–12131. 

- [66] Abhishek Gupta, Russell Mendonca, YuXuan Liu, Pieter Abbeel, and Sergey Levine. 2018. Meta-reinforcement learning of structured exploration strategies. _Advances in neural information processing systems_ 31 (2018). 

- [67] David Ha and Jürgen Schmidhuber. 2018. Recurrent world models facilitate policy evolution. _Advances in neural information processing systems_ 31 (2018). 

- [68] Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. 2018. Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor. In _International conference on machine learning_ . Pmlr, 1861–1870. 

- [69] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. 2019. Dream to control: Learning behaviors by latent imagination. _arXiv preprint arXiv:1912.01603_ (2019). 

- [70] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. 2019. Dream to control: Learning behaviors by latent imagination. _arXiv preprint arXiv:1912.01603_ (2019). 

- [71] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. 2019. Learning latent dynamics for planning from pixels. In _International conference on machine learning_ . PMLR, 2555–2565. 

- [72] Danijar Hafner, Timothy Lillicrap, Mohammad Norouzi, and Jimmy Ba. 2020. Mastering atari with discrete world models. _arXiv preprint arXiv:2010.02193_ (2020). 

- [73] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. 2023. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ (2023). 

- [74] Asher J Hancock, Allen Z Ren, and Anirudha Majumdar. 2024. Run-time observation interventions make visionlanguage-action models more visually robust. _arXiv preprint arXiv:2410.01971_ (2024). 

- [75] Patrik Haslum, Nir Lipovetzky, Daniele Magazzeni, Christian Muise, Ronald Brachman, Francesca Rossi, and Peter Stone. 2019. _An introduction to the planning domain definition language_ . Vol. 13. Springer. 

- [76] Haoran He, Chenjia Bai, Ling Pan, Weinan Zhang, Bin Zhao, and Xuelong Li. 2024. Large-scale actionless video pre-training via discrete diffusion for efficient policy learning. _CoRR_ (2024). 

- [77] Haoran He, Chenjia Bai, Kang Xu, Zhuoran Yang, Weinan Zhang, Dong Wang, Bin Zhao, and Xuelong Li. 2023. Diffusion model is an effective planner and data synthesizer for multi-task reinforcement learning. _Advances in neural information processing systems_ 36 (2023), 64896–64917. 

- [78] Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Dollár, and Ross Girshick. 2022. Masked autoencoders are scalable vision learners. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . 16000–16009. 

Liang et al. 

42 

- [79] Jonathan Ho and Stefano Ermon. 2016. Generative adversarial imitation learning. _Advances in neural information processing systems_ 29 (2016). 

- [80] Kazuki Hori, Kanata Suzuki, and Tetsuya Ogata. 2024. Interactively robot action planning with uncertainty analysis and active questioning by large language model. In _2024 IEEE/SICE International Symposium on System Integration (SII)_ . IEEE, 85–91. 

- [81] Xinyi Hou, Yanjie Zhao, Shenao Wang, and Haoyu Wang. 2025. Model context protocol (mcp): Landscape, security threats, and future research directions. _arXiv preprint arXiv:2503.23278_ (2025). 

- [82] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. 2022. Lora: Low-rank adaptation of large language models. _ICLR_ 1, 2 (2022), 3. 

- [83] Yingdong Hu, Fanqi Lin, Tong Zhang, Li Yi, and Yang Gao. 2023. Look before you leap: Unveiling the power of gpt-4v in robotic vision-language planning. _arXiv preprint arXiv:2311.17842_ (2023). 

- [84] Siyuan Huang, Zhengkai Jiang, Hao Dong, Yu Qiao, Peng Gao, and Hongsheng Li. 2023. Instruct2act: Mapping multi-modality instructions to robotic actions with large language model. _arXiv preprint arXiv:2305.11176_ (2023). 

- [85] Wenlong Huang, Pieter Abbeel, Deepak Pathak, and Igor Mordatch. 2022. Language models as zero-shot planners: Extracting actionable knowledge for embodied agents. In _International conference on machine learning_ . PMLR, 9118–9147. 

- [86] Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, and Li Fei-Fei. 2023. Voxposer: Composable 3d value maps for robotic manipulation with language models. _arXiv preprint arXiv:2307.05973_ (2023). 

- [87] Wenlong Huang, Fei Xia, Dhruv Shah, Danny Driess, Andy Zeng, Yao Lu, Pete Florence, Igor Mordatch, Sergey Levine, Karol Hausman, et al. 2023. Grounded decoding: Guiding text generation with grounded models for embodied agents. _Advances in Neural Information Processing Systems_ 36 (2023), 59636–59661. 

- [88] Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, et al. 2022. Inner monologue: Embodied reasoning through planning with language models. _arXiv preprint arXiv:2207.05608_ (2022). 

- [89] Yunfan Jiang, Agrim Gupta, Zichen Zhang, Guanzhi Wang, Yongqiang Dou, Yanjun Chen, Li Fei-Fei, Anima Anandkumar, Yuke Zhu, and Linxi Fan. 2022. Vima: General robot manipulation with multimodal prompts. _arXiv preprint arXiv:2210.03094_ 2, 3 (2022), 6. 

- [90] Yuqian Jiang, Harel Yedidsion, Shiqi Zhang, Guni Sharon, and Peter Stone. 2019. Multi-robot planning with conflicts and synergies. _Autonomous Robots_ 43, 8 (2019), 2011–2032. 

- [91] Bingyi Kang, Xiao Ma, Chao Du, Tianyu Pang, and Shuicheng Yan. 2023. Efficient diffusion policies for offline reinforcement learning. _Advances in Neural Information Processing Systems_ 36 (2023), 67195–67212. 

- [92] Moo Jin Kim, Chelsea Finn, and Percy Liang. 2025. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ (2025). 

- [93] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. 2024. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ (2024). 

- [94] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. 2024. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ (2024). 

- [95] Yeseung Kim, Dohyun Kim, Jieun Choi, Jisang Park, Nayoung Oh, and Daehyung Park. 2024. A survey on integration of large language models with intelligent robots. _Intelligent Service Robotics_ 17, 5 (2024), 1091–1107. 

- [96] Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C Berg, Wan-Yen Lo, et al. 2023. Segment anything. In _Proceedings of the IEEE/CVF international conference on computer vision_ . 4015–4026. 

- [97] Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C Berg, Wan-Yen Lo, et al. 2023. Segment anything. In _Proceedings of the IEEE/CVF international conference on computer vision_ . 4015–4026. 

- [98] James Kirkpatrick, Razvan Pascanu, Neil Rabinowitz, Joel Veness, Guillaume Desjardins, Andrei A Rusu, Kieran Milan, John Quan, Tiago Ramalho, Agnieszka Grabska-Barwinska, et al. 2017. Overcoming catastrophic forgetting in neural networks. _Proceedings of the national academy of sciences_ 114, 13 (2017), 3521–3526. 

- [99] Alex Krizhevsky, Ilya Sutskever, and Geoffrey E Hinton. 2012. Imagenet classification with deep convolutional neural networks. _Advances in neural information processing systems_ 25 (2012). 

- [100] Ananya Kumar, Aditi Raghunathan, Robbie Jones, Tengyu Ma, and Percy Liang. 2022. Fine-tuning can distort pretrained features and underperform out-of-distribution. _arXiv preprint arXiv:2202.10054_ (2022). 

- [101] Sascha Lange, Thomas Gabel, and Martin Riedmiller. 2012. Batch reinforcement learning. In _Reinforcement learning: State-of-the-art_ . Springer, 45–73. 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

43 

|[102]|Yann LeCun. 2022. A path towards autonomous machine intelligence version 0.9. 2, 2022-06-27. _Open Review_62, 1<br>(2022) 1–62.|
|---|---|
|[103]|,<br> Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler,<br>Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al.2020. Retrieval-augmented generation for knowledge-intensive nlp<br>tasks. _Advances in neural information processing systems_33 (2020), 9459–9474.|
|[104]|<br> Chunyuan Li, Zhe Gan, Zhengyuan Yang, Jianwei Yang, Linjie Li, Lijuan Wang, Jianfeng Gao, et al.2024. Multimodal<br>foundation models: From specialists to general-purpose assistants. _Foundations and Trends® in Computer Graphics_<br>_and Vision_16, 1-2 (2024), 1–214.|
|[105]|Chengmeng Li, Junjie Wen, Yan Peng, Yaxin Peng, Feifei Feng, and Yichen Zhu. 2025. Pointvla: Injecting the 3d world<br>into vision-language-action models. _arXiv preprint arXiv:2503.07511_(2025).|
|[106]|Hao Li, Xue Yang, Zhaokai Wang, Xizhou Zhu, Jie Zhou, Yu Qiao, Xiaogang Wang, Hongsheng Li, Lewei Lu, and<br>Jifeng Dai. 2024. Auto mc-reward: Automated dense reward design with large language models for minecraft. In<br>_Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_. 16426–16435.|
|[107]|<br> Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. 2023. Blip-2: Bootstrapping language-image pre-training<br>with frozen image encoders and large language models. In _International conference on machine learning_. PMLR,<br>19730–19742.|
|[108]|Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi. 2022. Blip: Bootstrapping language-image pre-training<br>for unified vision-language understanding and generation. In_International conference on machine learning_. PMLR,<br>12888–12900.|
|[109]|KunChang Li, Yinan He, Yi Wang, Yizhuo Li, Wenhai Wang, Ping Luo, Yali Wang, Limin Wang, and Yu Qiao. 2023.<br>Videochat: Chat-centric video understanding. _arXiv preprint arXiv:2305.06355_(2023).|
|[110]|<br> Shuang Li, Xavier Puig, Chris Paxton, Yilun Du, Clinton Wang, Linxi Fan, Tao Chen, De-An Huang, Ekin Akyürek,<br>Anima Anandkumar, et al.2022. Pre-trained language models for interactive decision-making. _Advances in Neural_<br>_Information Processing Systems_35 (2022), 31199–31212.|
|[111]|<br> Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan<br>Zhang, Huaping Liu, et al.2023. Vision-language foundation models as effective robot imitators. _arXiv preprint_<br>_arXiv:2311.01378_(2023).|
|[112]|Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete Florence, and Andy Zeng. 2022.<br>Code as policies: Language model programs for embodied control. _arXiv preprint arXiv:2209.07753_(2022).|
|[113]|<br> Zijing Liang, Yanjie Xu, Yifan Hong, Penghui Shang, Qi Wang, Qiang Fu, and Ke Liu. 2024. A survey of multimodel<br>large language models. In_Proceedings of the 3rd International Conference on Computer, Artificial Intelligence and_<br>_Control Engineering_. 405–409.|
|[114]|<br> Kevin Lin, Christopher Agia, Toki Migimatsu, Marco Pavone, and Jeannette Bohg. 2023. Text2motion: From natural<br>language instructions to feasible plans. _Autonomous Robots_47, 8 (2023), 1345–1365.|
|[115]|Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu<br>Zhang, Chong Ruan, et al. 2024. Deepseek-v3 technical report. _arXiv preprint arXiv:2412.19437_ (2024).|
|[116]|<br> Bo Liu, Yuqian Jiang, Xiaohan Zhang, Qiang Liu, Shiqi Zhang, Joydeep Biswas, and Peter Stone. 2023. Llm+ p:<br>i|
|[117]|Empowering large language models with optimal planning proficiency. _arXiv preprint arXiv:2304.11477_ (2023).<br> Yang Liu, Weixing Chen, Yongjie Bai, Xiaodan Liang, Guanbin Li, Wen Gao, and Liang Lin. 2025. Aligning cyber<br>space with physical world: A comprehensive survey on embodied ai. _IEEE/ASME Transactions on Mechatronics_(2025).|
|[118]|<br> Cong Lu, Philip Ball, Yee Whye Teh, and Jack Parker-Holder. 2023. Synthetic experience replay. _Advances in Neural_<br>_Information Processing Systems_36 (2023), 46323–46344.|
|[119]|<br> Yueen Ma, Zixing Song, Yuzheng Zhuang, Jianye Hao, and Irwin King. 2024. A survey on vision-language-action<br>models for embodied ai. _arXiv preprint arXiv:2405.14093_(2024).|
|[120]|<br> Yecheng Jason Ma, William Liang, Guanzhi Wang, De-An Huang, Osbert Bastani, Dinesh Jayaraman, Yuke Zhu, Linxi<br>Fan, and Anima Anandkumar. 2023. Eureka: Human-level reward design via coding large language models. _arXiv_<br>_preprint arXiv:2310.12931_(2023).|
|[121]|Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri,<br>Shrimai Prabhumoye, Yiming Yang, et al.2023. Self-refine: Iterative refinement with self-feedback. _Advances in_<br>_Neural Information Processing Systems_36 (2023), 46534–46594.|
|[122]|<br> Xinji Mai, Zeng Tao, Junxiong Lin, Haoran Wang, Yang Chang, Yanlan Kang, Yan Wang, and Wenqiang Zhang. 2024.<br>From efficient multimodal models to world models: A survey. _arXiv preprint arXiv:2407.00118_(2024).|
|[123]|fi  <br> Zhao Mandi, Shreeya Jain, and Shuran Song. 2024. Roco: Dialectic multi-robot collaboration with large language<br>models. In_2024 IEEE International Conference on Robotics and Automation (ICRA)_. IEEE, 286–299.|
|[124]|Spyros Maniatopoulos, Philipp Schillinger, Vitchyr Pong, David C Conner, and Hadas Kress-Gazit. 2016. Reactive<br>high-level behavior synthesis for an atlas humanoid robot. In_2016 IEEE international conference on robotics and_<br>_automation (ICRA)_. IEEE, 4192–4199.|


Liang et al. 

44 

- [125] David Q Mayne, James B Rawlings, Christopher V Rao, and Pierre OM Scokaert. 2000. Constrained model predictive control: Stability and optimality. _Automatica_ 36, 6 (2000), 789–814. 

- [126] Drew McDermott, Malik Ghallab, Adele E. Howe, Craig A. Knoblock, Ashwin Ram, Manuela M. Veloso, Daniel S. Weld, and David E. Wilkins. 1998. PDDL-the planning domain definition language. https://api.semanticscholar.org/ CorpusID:59656859 

- [127] Sanket Vaibhav Mehta, Darshan Patil, Sarath Chandar, and Emma Strubell. 2023. An empirical investigation of the role of pre-training in lifelong learning. _Journal of Machine Learning Research_ 24, 214 (2023), 1–50. 

- [128] Russell Mendonca, Shikhar Bahl, and Deepak Pathak. 2023. Structured world models from human videos. _arXiv preprint arXiv:2308.10901_ (2023). 

- [129] Vincent Micheli, Eloi Alonso, and François Fleuret. 2022. Transformers are sample-efficient world models. _arXiv preprint arXiv:2209.00588_ (2022). 

- [130] Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Andrei A Rusu, Joel Veness, Marc G Bellemare, Alex Graves, Martin Riedmiller, Andreas K Fidjeland, Georg Ostrovski, et al. 2015. Human-level control through deep reinforcement learning. _nature_ 518, 7540 (2015), 529–533. 

- [131] Yao Mu, Qinglong Zhang, Mengkang Hu, Wenhai Wang, Mingyu Ding, Jun Jin, Bin Wang, Jifeng Dai, Yu Qiao, and Ping Luo. 2023. Embodiedgpt: Vision-language pre-training via embodied chain of thought. _Advances in Neural Information Processing Systems_ 36 (2023), 25081–25094. 

- [132] Yao Mu, Qinglong Zhang, Mengkang Hu, Wenhai Wang, Mingyu Ding, Jun Jin, Bin Wang, Jifeng Dai, Yu Qiao, and Ping Luo. 2023. Embodiedgpt: Vision-language pre-training via embodied chain of thought. _Advances in Neural Information Processing Systems_ 36 (2023), 25081–25094. 

- [133] Kevin P Murphy. 2012. _Machine learning: a probabilistic perspective_ . MIT press. [134] Rhys Newbury, Jack Collins, Kerry He, Jiahe Pan, Ingmar Posner, David Howard, and Akansel Cosgun. 2024. A review of differentiable simulators. _IEEE Access_ (2024). 

- [135] Andrew Y Ng, Stuart Russell, et al. 2000. Algorithms for inverse reinforcement learning.. In _Icml_ , Vol. 1. 2. [136] Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. 2023. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ (2023). 

- [137] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. 2022. Training language models to follow instructions with human feedback. _Advances in neural information processing systems_ 35 (2022), 27730–27744. 

- [138] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. 2022. Training language models to follow instructions with human feedback. _Advances in neural information processing systems_ 35 (2022), 27730–27744. 

- [139] Chaofan Pan, Xin Yang, Yanhua Li, Wei Wei, Tianrui Li, Bo An, and Jiye Liang. 2025. A Survey of Continual Reinforcement Learning. _arXiv preprint arXiv:2506.21872_ (2025). 

- [140] Cheng Pan, Xi Yang, Haoran Wang, Jiaming Zhang, Jushun Li, and Jie Xu. 2024. Hierarchical Continual Reinforcement Learning via Large Language Model. _arXiv preprint arXiv:2401.15098_ (2024). 

- [141] German I Parisi, Ronald Kemker, Jose L Part, Christopher Kanan, and Stefan Wermter. 2019. Continual lifelong learning with neural networks: A review. _Neural networks_ 113 (2019), 54–71. 

- [142] Tim Pearce, Tabish Rashid, Anssi Kanervisto, Dave Bignell, Mingfei Sun, Raluca Georgescu, Sergio Valcarcel Macua, Shan Zheng Tan, Ida Momennejad, Katja Hofmann, et al. 2023. Imitating human behaviour with diffusion models. _arXiv preprint arXiv:2301.10677_ (2023). 

- [143] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. 2025. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ (2025). 

- [144] Giorgio Piatti, Zhijing Jin, Max Kleiman-Weiner, Bernhard Schölkopf, Mrinmaya Sachan, and Rada Mihalcea. 2024. Cooperate or collapse: Emergence of sustainable cooperation in a society of llm agents. _Advances in Neural Information Processing Systems_ 37 (2024), 111715–111759. 

- [145] AJ Piergiovanni, Alan Wu, and Michael S Ryoo. 2019. Learning real-world robot policies by dreaming. In _2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 7680–7687. 

- [146] Shuofei Qiao, Runnan Fang, Ningyu Zhang, Yuqi Zhu, Xiang Chen, Shumin Deng, Yong Jiang, Pengjun Xie, Fei Huang, and Huajun Chen. 2024. Agent planning with world knowledge model. _Advances in Neural Information Processing Systems_ 37 (2024), 114843–114871. 

- [147] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. 2025. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ (2025). 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

45 

- [148] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. 2021. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ . PmLR, 8748–8763. 

- [149] Alec Radford, Karthik Narasimhan, Tim Salimans, Ilya Sutskever, et al. 2018. Improving language understanding by generative pre-training. (2018). 

- [150] Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, et al. 2019. Language models are unsupervised multitask learners. _OpenAI blog_ 1, 8 (2019), 9. 

- [151] Mohaimenul Azam Khan Raiaan, Md Saddam Hossain Mukta, Kaniz Fatema, Nur Mohammad Fahad, Sadman Sakib, Most Marufatul Jannat Mim, Jubaer Ahmad, Mohammed Eunus Ali, and Sami Azam. 2024. A review on large language models: Architectures, applications, taxonomies, open issues and challenges. _IEEE access_ 12 (2024), 26839–26874. 

- [152] Kate Rakelly, Aurick Zhou, Chelsea Finn, Sergey Levine, and Deirdre Quillen. 2019. Efficient off-policy metareinforcement learning via probabilistic context variables. In _International conference on machine learning_ . PMLR, 5331–5340. 

- [153] Sarthak S Raman, Vashisht Cohen, Erez Rosen, Shreyas Mirchandani, Benjamin Arkin, David Hedges, Alex Sorokin, Brent Gold, Tsung-Yen Fu, David Salac, et al. 2022. Planning with large language models via corrective re-prompting. _arXiv preprint arXiv:2210.03952_ (2022). 

- [154] Aditya Ramesh, Prafulla Dhariwal, Alex Nichol, Casey Chu, and Mark Chen. 2022. Hierarchical text-conditional image generation with clip latents. _arXiv preprint arXiv:2204.06125_ 1, 2 (2022), 3. 

- [155] Aditya Ramesh, Mikhail Pavlov, Gabriel Goh, Scott Gray, Chelsea Voss, Alec Radford, Mark Chen, and Ilya Sutskever. 2021. Zero-shot text-to-image generation. In _International conference on machine learning_ . Pmlr, 8821–8831. 

- [156] Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman Rädle, Chloe Rolland, Laura Gustafson, et al. 2024. Sam 2: Segment anything in images and videos. _arXiv preprint arXiv:2408.00714_ (2024). 

- [157] Sonia Raychaudhuri and Angel X Chang. 2025. Semantic Mapping in Indoor Embodied AI–A Comprehensive Survey and Future Directions. _arXiv preprint arXiv:2501.05750_ (2025). 

- [158] Scott Reed, Konrad Zolna, Emilio Parisotto, Sergio Gomez Colmenarejo, Alexander Novikov, Gabriel Barth-Maron, Mai Gimenez, Yury Sulsky, Jackie Kay, Jost Tobias Springenberg, et al. 2022. A generalist agent. _arXiv preprint arXiv:2205.06175_ (2022). 

- [159] Machel Reid, Yutaro Yamada, and Shixiang Shane Gu. 2022. Can wikipedia help offline reinforcement learning? _arXiv preprint arXiv:2201.12122_ (2022). 

- [160] Brian Reily, Peng Gao, Fei Han, Hua Wang, and Hao Zhang. 2022. Real-time recognition of team behaviors by multisensory graph-embedded robot learning. _The International Journal of Robotics Research_ 41, 8 (2022), 798–811. 

- [161] Allen Z Ren, Anushri Dixit, Alexandra Bodrova, Sumeet Singh, Stephen Tu, Noah Brown, Peng Xu, Leila Takayama, Fei Xia, Jake Varley, et al. 2023. Robots that ask for help: Uncertainty alignment for large language model planners. _arXiv preprint arXiv:2307.01928_ (2023). 

- [162] Jan Robine, Marc Höftmann, Tobias Uelwer, and Stefan Harmeling. 2023. Transformer-based world models are happy with 100k interactions. _arXiv preprint arXiv:2303.07109_ (2023). 

- [163] Nikita Rudin, David Hoeller, Philipp Reist, and Marco Hutter. 2022. Learning to walk in minutes using massively parallel deep reinforcement learning. In _Conference on robot learning_ . PMLR, 91–100. 

- [164] Gavin A Rummery and Mahesan Niranjan. 1994. _On-line Q-learning using connectionist systems_ . Vol. 37. University of Cambridge, Department of Engineering Cambridge, UK. 

- [165] Ranjan Sapkota, Yang Cao, Konstantinos I Roumeliotis, and Manoj Karkee. 2025. Vision-language-action models: Concepts, progress, applications and challenges. _arXiv preprint arXiv:2505.04769_ (2025). 

- [166] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. 2017. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ (2017). 

- [167] Pratyusha Sharma, Antonio Torralba, and Jacob Andreas. 2021. Skill induction and planning with latent language. _arXiv preprint arXiv:2110.01517_ (2021). 

- [168] Lucy Xiaoyang Shi, Zheyuan Hu, Tony Z Zhao, Archit Sharma, Karl Pertsch, Jianlan Luo, Sergey Levine, and Chelsea Finn. 2024. Yell at your robot: Improving on-the-fly from language corrections. _arXiv preprint arXiv:2403.12910_ (2024). 

- [169] Ruizhe Shi, Yuyao Liu, Yanjie Ze, Simon S Du, and Huazhe Xu. 2023. Unleashing the power of pre-trained language models for offline reinforcement learning. _arXiv preprint arXiv:2310.20587_ (2023). 

- [170] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. 2023. Reflexion: Language agents with verbal reinforcement learning. _Advances in Neural Information Processing Systems_ 36 (2023), 8634–8652. 

- [171] Keisuke Shirai, Cristian C Beltran-Hernandez, Masashi Hamaya, Atsushi Hashimoto, Shohei Tanaka, Kento Kawaharazuka, Kazutoshi Tanaka, Yoshitaka Ushiku, and Shinsuke Mori. 2024. Vision-language interpreter for robot task planning. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2051–2058. 

Liang et al. 

46 

- [172] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. 2022. Cliport: What and where pathways for robotic manipulation. In _Conference on Robot Learning_ . PMLR, 894–906. 

- [173] David Silver, Aja Huang, Chris J Maddison, Arthur Guez, Laurent Sifre, George Van Den Driessche, Julian Schrittwieser, Ioannis Antonoglou, Veda Panneershelvam, Marc Lanctot, et al. 2016. Mastering the game of Go with deep neural networks and tree search. _nature_ 529, 7587 (2016), 484–489. 

- [174] David Silver, Aja Huang, Chris J Maddison, Arthur Guez, Laurent Sifre, George Van Den Driessche, Julian Schrittwieser, Ioannis Antonoglou, Veda Panneershelvam, Marc Lanctot, et al. 2016. Mastering the game of Go with deep neural networks and tree search. _nature_ 529, 7587 (2016), 484–489. 

- [175] Tom Silver, Varun Hariprasad, Reece S Shuttleworth, Nishanth Kumar, Tomás Lozano-Pérez, and Leslie Pack Kaelbling. 2022. PDDL planning with pretrained large language models. In _NeurIPS 2022 foundation models for decision making workshop_ . 

- [176] Ishika Singh, Valts Blukis, Arsalan Mousavian, Ankit Goyal, Danfei Xu, Jonathan Tremblay, Dieter Fox, Jesse Thomason, and Animesh Garg. 2022. Progprompt: Generating situated robot task plans using large language models. _arXiv preprint arXiv:2209.11302_ (2022). 

- [177] Fuchun Sun, Runfa Chen, Tianying Ji, Yu Luo, Huaidong Zhou, and Huaping Liu. 2024. A comprehensive survey on embodied intelligence: Advancements, challenges, and future perspectives. _CAAI Artificial Intelligence Research_ 3 (2024). 

- [178] Ed D Tate, Jessy W Grizzle, and Huei Peng. 2009. SP-SDP for fuel consumption and tailpipe emissions minimization in an EVT hybrid. _IEEE Transactions on Control Systems Technology_ 18, 3 (2009), 673–687. 

- [179] Gemini Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. 2023. Gemini: a family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ (2023). 

- [180] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. 2024. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ (2024). 

- [181] Andrea Tirinzoni, Andrea Sessa, Matteo Pirotta, and Marcello Restelli. 2018. Importance weighted transfer of samples in reinforcement learning. In _International Conference on Machine Learning_ . PMLR, 4936–4945. 

- [182] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. 2023. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_ (2023). 

- [183] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. 2023. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ (2023). 

- [184] A. M. Turing. 1950. Computing machinery and intelligence. _Mind_ LIX, 236 (1950), 433–460. [185] Karthik Valmeekam, Alberto Olmo, Sarath Sreedharan, and Subbarao Kambhampati. 2022. Large language models still can’t plan (a benchmark for LLMs on planning and reasoning about change). In _NeurIPS 2022 Foundation Models for Decision Making Workshop_ . 

- [186] Quan Vuong, Sergey Levine, Homer Rich Walke, Karl Pertsch, Anikait Singh, Ria Doshi, Charles Xu, Jianlan Luo, Liam Tan, Dhruv Shah, et al. 2023. Open x-embodiment: Robotic learning datasets and rt-x models. In _Towards Generalist Robots: Learning Paradigms for Scalable Skill Acquisition@ CoRL2023_ . 

- [187] Andrew Wagenmaker, Kevin Huang, Liyiming Ke, Kevin Jamieson, and Abhishek Gupta. 2024. Overcoming the Sim-to-Real Gap: Leveraging Simulation to Learn to Explore for Real-World RL. _Advances in Neural Information Processing Systems_ 37 (2024), 78715–78765. 

- [188] Zishen Wan, Yuhang Du, Mohamed Ibrahim, Yang Zhao, Tushar Krishna, and Arijit Raychowdhury. 2024. Thinking and moving: An efficient computing approach for integrated task and motion planning in cooperative embodied ai systems. In _Proceedings of the 43rd IEEE/ACM International Conference on Computer-Aided Design_ . 1–7. 

- [189] Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. 2023. Voyager: An open-ended embodied agent with large language models. _arXiv preprint arXiv:2305.16291_ (2023). 

- [190] Jiaqi Wang, Enze Shi, Huawen Hu, Chong Ma, Yiheng Liu, Xuhui Wang, Yincheng Yao, Xuan Liu, Bao Ge, and Shu Zhang. 2025. Large language models for robotics: Opportunities, challenges, and perspectives. _Journal of Automation and Intelligence_ 4, 1 (2025), 52–64. 

- [191] Yiqi Wang, Wentao Chen, Xiaotian Han, Xudong Lin, Haiteng Zhao, Yongfei Liu, Bohan Zhai, Jianbo Yuan, Quanzeng You, and Hongxia Yang. 2024. Exploring the reasoning abilities of multimodal large language models (mllms): A comprehensive survey on emerging trends in multimodal reasoning. _arXiv preprint arXiv:2401.06805_ (2024). 

- [192] Ziyi Wang, Sheng Cai, Guandao Chen, Si-Yuan Chen, Hong-Xin Yang, Shuyuan Liu, Zihao Zhao, Yuxiang Wang, Chen Chen, Leo J Li, et al. 2023. Describe, explain, plan and select: Interactive planning with large language models enables open-world multi-task agents. _arXiv preprint arXiv:2302.01560_ (2023). 

47 

Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning 

- [193] Zhendong Wang, Jonathan J Hunt, and Mingyuan Zhou. 2022. Diffusion policies as an expressive policy class for offline reinforcement learning. _arXiv preprint arXiv:2208.06193_ (2022). 

- [194] Christopher John Cornish Hellaby Watkins et al. 1989. Learning from delayed rewards. (1989). [195] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. 2022. Chain-of-thought prompting elicits reasoning in large language models. _Advances in neural information processing systems_ 35 (2022), 24824–24837. 

- [196] Junjie Wen, Minjie Zhu, Yichen Zhu, Zhibin Tang, Jinming Li, Zhongyi Zhou, Chengmeng Li, Xiaoyu Liu, Yaxin Peng, Chaomin Shen, et al. 2024. Diffusion-VLA: Generalizable and Interpretable Robot Foundation Model via Self-Generated Reasoning. _arXiv preprint arXiv:2412.03293_ (2024). 

- [197] Junjie Wen, Yichen Zhu, Jinming Li, Zhibin Tang, Chaomin Shen, and Feifei Feng. 2025. Dexvla: Vision-language model with plug-in diffusion expert for general robot control. _arXiv preprint arXiv:2502.05855_ (2025). 

- [198] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Zhibin Tang, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, et al. 2025. Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ (2025). 

- [199] Yixuan Weng, Minjun Zhu, Guangsheng Bao, Hongbo Zhang, Jindong Wang, Yue Zhang, and Linyi Yang. 2024. Cycleresearcher: Improving automated research via automated review. _arXiv preprint arXiv:2411.00816_ (2024). 

- [200] David E Wilkins. 2014. _Practical planning: extending the classical AI planning paradigm_ . Elsevier. [201] Lik Hang Kenny Wong, Xueyang Kang, Kaixin Bai, and Jianwei Zhang. 2025. A Survey of Robotic Navigation and Manipulation with Physics Simulators in the Era of Embodied AI. _arXiv preprint arXiv:2505.01458_ (2025). 

- [202] Philipp Wu, Alejandro Escontrela, Danijar Hafner, Pieter Abbeel, and Ken Goldberg. 2023. Daydreamer: World models for physical robot learning. In _Conference on robot learning_ . PMLR, 2226–2240. 

- [203] Zhenyu Wu, Ziwei Wang, Xiuwei Xu, Jiwen Lu, and Haibin Yan. 2023. Embodied task planning with large language models. _arXiv preprint arXiv:2307.01848_ (2023). 

- [204] Xuan Xiao, Jiahang Liu, Zhipeng Wang, Yanmin Zhou, Yong Qi, Shuo Jiang, Bin He, and Qian Cheng. 2025. Robot learning in the era of foundation models: A survey. _Neurocomputing_ (2025), 129963. 

- [205] Tianbao Xie, Siheng Zhao, Chen Henry Wu, Yitao Liu, Qian Luo, Victor Zhong, Yanchao Yang, and Tao Yu. 2024. Text2reward: Automated dense reward function generation for reinforcement learning. In _International Conference on Learning Representations (ICLR), 2024 (07/05/2024-11/05/2024, Vienna, Austria)_ . 

- [206] Mingxing Xu, Wenrui Dai, Chunmiao Liu, Xing Gao, Weiyao Lin, Guo-Jun Qi, and Hongkai Xiong. 2020. Spatialtemporal transformer networks for traffic flow forecasting. _arXiv preprint arXiv:2001.02908_ (2020). 

- [207] Mengdi Xu, Yikang Shen, Shun Zhang, Yuchen Lu, Ding Zhao, Joshua Tenenbaum, and Chuang Gan. 2022. Prompting decision transformer for few-shot policy generalization. In _international conference on machine learning_ . PMLR, 24631–24645. 

- [208] Siyu Xu, Yunke Wang, Chenghao Xia, Dihao Zhu, Tao Huang, and Chang Xu. 2025. Vla-cache: Towards efficient vision-language-action model via adaptive token caching in robotic manipulation. _arXiv preprint arXiv:2502.02175_ (2025). 

- [209] Zhiyuan Xu, Kun Wu, Junjie Wen, Jinming Li, Ning Liu, Zhengping Che, and Jian Tang. 2024. A survey on robotics with foundation models: toward embodied ai. _arXiv preprint arXiv:2402.02385_ (2024). 

- [210] Zhiyuan Xu, Kun Wu, Junjie Wen, Jinming Li, Ning Liu, Zhengping Che, and Jian Tang. 2024. A survey on robotics with foundation models: toward embodied ai. _arXiv preprint arXiv:2402.02385_ (2024). 

- [211] Jingkang Yang, Yuhao Dong, Shuai Liu, Bo Li, Ziyue Wang, Haoran Tan, Chencheng Jiang, Jiamu Kang, Yuanhan Zhang, Kaiyang Zhou, et al. 2024. Octopus: Embodied vision-language programmer from environmental feedback. In _European conference on computer vision_ . Springer, 20–38. 

- [212] Mengjiao Yang, Yilun Du, Kamyar Ghasemipour, Jonathan Tompson, Dale Schuurmans, and Pieter Abbeel. 2023. Learning interactive real-world simulators. _arXiv preprint arXiv:2310.06114_ 1, 2 (2023), 6. 

- [213] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik Narasimhan. 2023. Tree of thoughts: Deliberate problem solving with large language models. _Advances in neural information processing systems_ 36 (2023), 11809–11822. 

- [214] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. 2023. React: Synergizing reasoning and acting in language models. In _International Conference on Learning Representations (ICLR)_ . 

- [215] Wenhao Yu, Nimrod Gileadi, Chuyuan Fu, Sean Kirmani, Kuang-Huei Lee, Montse Gonzalez Arenas, Hao-Tien Lewis Chiang, Tom Erez, Leonard Hasenclever, Jan Humplik, et al. 2023. Language to rewards for robotic skill synthesis. _arXiv preprint arXiv:2306.08647_ (2023). 

- [216] Ekim Yurtsever, Jacob Lambert, Alexander Carballo, and Kazuya Takeda. 2020. A survey of autonomous driving: Common practices and emerging technologies. _IEEE access_ 8 (2020), 58443–58469. 

- [217] Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 2024. 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations. _arXiv preprint arXiv:2403.03954_ (2024). 

Liang et al. 

48 

- [218] Hang Zhang, Xin Li, and Lidong Bing. 2023. Video-llama: An instruction-tuned audio-visual language model for video understanding. _arXiv preprint arXiv:2306.02858_ (2023). 

- [219] Rongyu Zhang, Menghang Dong, Yuan Zhang, Liang Heng, Xiaowei Chi, Gaole Dai, Li Du, Yuan Du, and Shanghang Zhang. 2025. Mole-vla: Dynamic layer-skipping vision language action model via mixture-of-layers for efficient robot manipulation. _arXiv preprint arXiv:2503.20384_ (2025). 

- [220] Tianyao Zhang, Xiaoguang Hu, Jin Xiao, and Guofeng Zhang. 2022. A survey of visual navigation: From geometry to embodied AI. _Engineering Applications of Artificial Intelligence_ 114 (2022), 105036. 

- [221] Wenqi Zhang, Ke Tang, Hai Wu, Mengna Wang, Yongliang Shen, Guiyang Hou, Zeqi Tan, Peng Li, Yueting Zhuang, and Weiming Lu. 2024. Agent-pro: Learning to evolve via policy-level reflection and optimization. _arXiv preprint arXiv:2402.17574_ (2024). 

- [222] Weipu Zhang, Gang Wang, Jian Sun, Yetian Yuan, and Gao Huang. 2023. Storm: Efficient stochastic transformer based world models for reinforcement learning. _Advances in Neural Information Processing Systems_ 36 (2023), 27147–27166. 

- [223] Xinlu Zhang, Yujie Lu, Weizhi Wang, An Yan, Jun Yan, Lianke Qin, Heng Wang, Xifeng Yan, William Yang Wang, and Linda Ruth Petzold. 2023. Gpt-4v (ision) as a generalist evaluator for vision-language tasks. _arXiv preprint arXiv:2311.01361_ (2023). 

- [224] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. 2023. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ (2023). 

- [225] Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, et al. 2023. A survey of large language models. _arXiv preprint arXiv:2303.18223_ 1, 2 (2023). 

- [226] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 2024. 3d-vla: A 3d vision-language-action generative world model. _arXiv preprint arXiv:2403.09631_ (2024). 

- [227] Junhao Zheng, Chengming Shi, Xidi Cai, Qiuke Li, Duzhen Zhang, Chenxing Li, Dong Yu, and Qianli Ma. 2025. Lifelong learning of large language model based agents: A roadmap. _arXiv preprint arXiv:2501.07278_ (2025). 

- [228] Qinqing Zheng, Amy Zhang, and Aditya Grover. 2022. Online decision transformer. In _international conference on machine learning_ . PMLR, 27042–27059. 

- [229] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daumé III, Andrey Kolobov, Furong Huang, and Jianwei Yang. 2024. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv preprint arXiv:2412.10345_ (2024). 

- [230] Yifan Zhong, Xuchuan Huang, Ruochong Li, Ceyao Zhang, Yitao Liang, Yaodong Yang, and Yuanpei Chen. 2025. Dexgraspvla: A vision-language-action framework towards general dexterous grasping. _arXiv preprint arXiv:2502.20900_ (2025). 

- [231] Zhehua Zhou, Jiayang Song, Kunpeng Yao, Zhan Shu, and Lei Ma. 2024. Isr-llm: Iterative self-refined large language model for long-horizon sequential task planning. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2081–2088. 

- [232] Deyao Zhu, Jun Chen, Xiaoqian Shen, Xiang Li, and Mohamed Elhoseiny. 2023. Minigpt-4: Enhancing vision-language understanding with advanced large language models. _arXiv preprint arXiv:2304.10592_ (2023). 

- [233] Zheng Zhu, Xiaofeng Wang, Wangbo Zhao, Chen Min, Nianchen Deng, Min Dou, Yuqi Wang, Botian Shi, Kai Wang, Chi Zhang, et al. 2024. Is sora a world simulator? a comprehensive survey on general world models and beyond. _arXiv preprint arXiv:2405.03520_ (2024). 

- [234] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. 2023. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ . PMLR, 2165–2183. 

