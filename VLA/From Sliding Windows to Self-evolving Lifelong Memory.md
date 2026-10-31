---
title: "From Sliding Windows to Self-evolving Lifelong Memory: A Dual-perspective Survey of Memory Paradigms for Long-Horizon Robotics VLA Models"
date: "2026-10-16"
authors: "Yong Wang; Boyu Shen; Xinwei Zhang; Yizheng Li; Keyuan Luo"
url: https://arxiv.org/abs/2610.23319
pdf: https://arxiv.org/pdf/2610.23319
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2610.23319)** / [論文ページ](https://arxiv.org/abs/2610.23319)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **From Sliding Windows to Self-evolving Lifelong Memory: A Dual-perspective Survey of Memory Paradigms for Long-Horizon Robotics VLA Models** 

Yong Wang<sup>[0009-0003-2943-4670]</sup> , Boyu Shen<sup>[0009-0002-4801-0892]</sup> , Xinwei Zhang<sup>[0009-0004-3582-</sup> 3901], Yizheng Li [0009-0006-7475-8457] and Keyuan Luo *[0009-0006-5265-784X] 

Department of Computer Science and Technology, Hainan Bielefeld University of Applied Sciences, Hainan 571700, China `keyuan.luo@hibiuh.edu.cn` 

**Abstract.** Long-horizon robotic tasks expose a fundamental limitation of current Vision-Language-Action (VLA) models because their restricted temporal context prevents effective accumulation and reuse of past experiences. As a result, memory has become a fundamental component for enabling embodied agents to perform long-horizon reasoning and adaptive decision-making. This survey presents a systematic taxonomy of VLA memory mechanisms based on memory scope and persistence, categorizing existing approaches into five representative paradigms and one emerging frontier. Based on this taxonomy, we compare representative VLA memory systems in terms of memory characteristics, architectural complexity, and open-source maturity, revealing a clear tradeoff in which increasing architectural complexity is generally accompanied by decreasing open-source maturity. Finally, we discuss the key challenges in building full-lifecycle memory systems, including efficient memory management and lifelong knowledge evolution. Overall, this survey provides a unified perspective on memory architectures for VLA agents and offers insights into the development of lifelong embodied intelligence. 

**Keywords:** Vision-Language-Action Models, Long-horizon Robotics, Memory Paradigms, Lifelong Embodied Intelligence, Survey 

## **1 Introduction** 

Vision-Language-Action (VLA) models have demonstrated strong capabilities in mapping visual and linguistic inputs to robotic actions [1]. However, long-horizon manipulation remains challenging due to limited temporal context and insufficient mechanisms for storing and reusing task-relevant experiences [5, 8, 26]. 

Existing studies mainly investigate individual memory mechanisms, while a unified framework for characterizing memory evolution in VLA systems remains lacking [1, 8]. Unlike previous surveys that categorize VLA systems according to architectures or learning strategies [1], this survey adopts memory as the organizing principle and introduces a Scope–Persistence perspective to characterize the evolution from 

#### 2 

short-context interaction toward lifelong self-evolving memory. Existing memory mechanisms are further analyzed from the perspectives of memory evolution, architectural complexity, and practical accessibility. The analysis reveals a trade-off between increasing memory capability and decreasing accessibility. Persistent deployment-time memory and self-evolving memory remain open challenges due to the limited availability of full-stack implementations [10]. 

The main contributions of this survey are summarized as follows: 

- We introduce a unified Scope–Persistence taxonomy to characterize the evolution of memory architectures in VLA systems, providing a memory-centric perspective beyond existing architecture- or learning-based categorizations. 

- We systematically review existing VLA memory mechanisms and organize them into five established paradigms and one emerging frontier, covering their memory representations, retrieval strategies, and update mechanisms. 

- We establish a unified comparison framework considering memory scope, memory form, persistence, speed, forgetting behavior, and open-source maturity, revealing the trade-off between memory capability and system accessibility. 

- We identify self-evolving lifelong memory as an emerging direction and discuss key challenges toward developing persistent and continuously adaptive embodied agents. 

## **2 Background and Taxonomy** 

### **2.1 VLA Models and Long-horizon Tasks** 

Vision-Language-Action (VLA) models integrate visual perception, language understanding, and robotic control to generate actions from multimodal inputs [1, 30]. Related multimodal learning strategies have also been explored in other embodied intelligent systems, where transformer-based architectures exploit cross-modal interactions between visual and contextual information for perception and decision-making [31–33]. However, existing VLA policies often rely on limited temporal context, restricting their ability to perform long-horizon tasks requiring progress tracking, failure recovery, and experience reuse [1, 2]. 

### **2.2 Dimensions of Comparison** 

We adopt six dimensions to compare memory paradigms, including Scope, Memory Form, Persistence, Speed, Forgetting, and Open-source Maturity (OSS). Scope describes the temporal and contextual span of accessible experience, while Memory Form characterizes its representation, including implicit parameter-based memory and explicit external memory [3,7]. Persistence indicates whether experience can be retained beyond the current episode [3]. Speed, Forgetting, and OSS evaluate deployment efficiency, knowledge retention, and implementation accessibility, respectively. 

3 

Beyond these dimensions, memory systems are analyzed through four lifecycle mechanisms, including representation, retrieval, updating, and consolidation [3, 5, 7]. To improve the consistency of qualitative comparison, each dimension is evaluated according to predefined criteria. Scope evaluates the range of available experience from recent observations to lifelong knowledge. Speed considers retrieval latency and computational overhead during deployment. Forgetting reflects the ability to preserve previously acquired knowledge during future tasks. OSS maturity considers the availability of source code, pretrained models, documentation, and reproducible implementations. 

The qualitative ratings in Table 1 are determined based on relative comparisons among representative systems rather than absolute measurements. For example, speed reflects additional computational overhead introduced by memory retrieval and management, while OSS maturity considers the availability of public implementations, pretrained models, and reproducible experimental settings. 

### **2.3 The Memory Paradigms** 

We propose a taxonomy of VLA memory mechanisms based on two complementary dimensions, namely memory scope and cross-episode persistence. Memory scope characterizes the temporal and contextual extent of information available to the agent, whereas cross-episode persistence reflects whether acquired knowledge persists beyond a single episode [3]. These two dimensions provide a model-independent perspective for analyzing the evolution of VLA memory mechanisms. 


**Fig. 1.** Scope–Persistence taxonomy illustrating the evolution of representative VLA memory paradigms across different memory scopes and persistence levels. 

Existing memory paradigms can be organized according to memory scope and persistence, as shown in Fig. 1. Rather than representing a strictly linear progression, different paradigms emerge to address distinct memory requirements. Based on their defining characteristics, existing approaches are categorized into six representative types: sliding window memory, implicit fusion memory, explicit retrieval memory, trainingperiod memory, persistent memory, and self-evolving memory. 

4 

**Table 1.** Qualitative comparison of representative VLA memory paradigms. 

|Paradigm|Scope|Memory<br>Form|Persistence|Speed|Forgetting|OSS|Examples|
|---|---|---|---|---|---|---|---|
|Sliding<br>Window|1-6 frames|Implicit|None|Highest|Excellent|High|OpenVLA|
|Implicit<br>Fusion|Episode|Implicit|None|High|Medium|High|OpenPI,𝜋0|
|Explicit<br>Retrieval|Episode|Explicit|None|Moderate|Medium|Medium|MemoryVLA|
|Training<br>Period|Training|Weights|Train only|High|Poor|Medium|MAP-VLA|
|Persistent|Deployment|Explicit|Full|Moderate|Excellent|Low|ELLMER|
|Self-<br>evolving|Lifecycle|Unified|Full|N/A|N/A|Concept|No mature<br>implementation|


**Table 2.** Engineering Mechanisms Underlying Different Memory Paradigms. 

|Paradigm|MemoryRepresentation|Retrieval Strategy|Update and Consolidation|
|---|---|---|---|
|Sliding Window|Observation sequence|Context attention|None|
|Implicit Fusion|Latent state|Implicit aggregation|Learned update|
|Explicit Retrieval|Episodic memory bank|Similarity-based retrieval|Manual writing|
|Training Period|Model parameters|Parameter inference|Offline optimization|
|Persistent|Persistent memory store|Cross-episode retrieval|Memory management|
|Self-evolving|Prospective unified<br>memory|Prospective autonomous<br>retrieval|Prospective autonomous<br>evolution|


The first three paradigms focus on within-episode reasoning and differ mainly in how historical information is retained, ranging from temporary context windows to latent representations and explicit memory retrieval. The remaining paradigms extend memory across episodes by enabling knowledge reuse over time. This evolution reflects a gradual transition from short-term context utilization to persistent and adaptive memory systems. 

Representative systems are compared using the framework introduced in Section 2.2. Table 1 summarizes their memory characteristics and practical accessibility, while Table 2 further analyzes the underlying engineering mechanisms. These comparisons reveal a trade-off between memory capability and implementation complexity. More advanced memory mechanisms generally provide broader temporal coverage and stronger knowledge retention, but often introduce higher computational requirements and lower reproducibility. 

## **3 Within-episode Memory** 

Within a single task execution, memory mechanisms enable the agent to make shortterm decisions by leveraging recent observations, latent representations, or retrieved experiences [2]. The policy parameters are kept unchanged during deployment, and memory is instead maintained through temporary context, latent states, or external retrieval mechanisms. 

5 

### **3.1 Sliding Window** 

In sliding-window policies, the model only uses a limited number of recent observations with task instructions for action prediction rather than maintaining complete episode history. This approach follows sequence modeling paradigms such as Decision Transformer [29] and is adopted by VLA policies including OpenVLA [16], Octo [18], and RoboFlamingo [11], as well as visuomotor policies such as Diffusion Policy [24]. Since earlier observations are discarded after leaving the input window, these methods cannot reuse past experiences across episodes. This design reduces computational overhead and avoids additional memory management during deployment, but prevents the policy from revisiting potentially important historical information. Because model parameters remain fixed after training, new experiences cannot be integrated during execution. Therefore, sliding-window memory achieves efficient short-term reasoning at the cost of limited temporal coverage and poor longhorizon adaptability. Extending the context window can partially alleviate this limitation but introduces higher inference cost and memory consumption [3, 5, 8]. This creates a practical trade-off between short-term efficiency and long-horizon information retention, making sliding-window approaches less suitable for tasks requiring delayed reasoning or recovery from earlier failures. 

### **3.2 Single-episode Implicit Fusion** 

Recent VLA models, including π0 [13] and OpenPI [14], typically do not maintain an independent persistent memory module during deployment. Instead, historical information is temporarily retained through latent representations or extended context windows, enabling the policy to incorporate previous observations when generating actions. Since inference does not update model parameters, such information cannot be preserved as reusable memory beyond the current interaction [3]. Although implicit fusion improves within-episode temporal reasoning, it suffers from limited interpretability because the model cannot explicitly identify or modify retained experiences. Moreover, extending context length increases computational costs, creating a transparency–efficiency trade-off that limits its applicability to long-horizon experience reuse [1, 3, 8]. 

### **3.3 Single-episode Explicit Retrieval** 

Explicit retrieval-based memory stores previous task experiences in external memory and retrieves relevant information during execution. MemoryVLA [10], MemER [9], KEMO [27], and Embodied-RAG [28] follow this strategy by separating memory storage from policy inference, enabling experience reuse without updating policy parameters. Compared with implicit fusion, retrieval-based memory provides more interpretable and accessible stored information [1]. However, growing memory banks increase retrieval latency and storage costs, while irrelevant or outdated experiences may introduce retrieval noise [3,8–10]. Moreover, retrieval alone cannot update the underlying policy or consolidate new knowledge, limiting continuous adaptation. 

#### 6 

Therefore, retrieval-based approaches trade flexible experience access for increased memory management complexity. 

## **4 Cross-episode Memory** 

### **4.1 Training-period Cross-episode Enhancement** 

Paradigm 4 integrates accumulated experience during training or fine-tuning, consolidating task-relevant knowledge into model parameters through optimization. Representative systems include MAP-VLA [19] and GR-2 [4], which leverage trainingstage experience to improve generalization. After training, the acquired knowledge is retained in fixed parameters, distinguishing this paradigm from deployment-time persistent memory. However, new experiences cannot be incorporated without additional optimization, requiring retraining or fine-tuning that increases computational cost and may cause catastrophic forgetting of previously acquired skills. 

### **4.2 Deployment-time Persistent Memory** 

Deployment-time persistent memory architectures maintain task-relevant information beyond individual episodes through external memory structures, separating memory from policy parameters and enabling retrieval during deployment. Recent embodied AI systems, including ELLMER [15], RoboMemory [17], KARMA [25], and ECHO [21], explore persistent memory through external storage, hierarchical organization, and consolidation mechanisms. However, current approaches mainly focus on memory storage and retrieval, while autonomous organization, knowledge consolidation, and adaptive updating remain open challenges. Persistent memory also introduces a stability–plasticity trade-off: frequent updates improve adaptation but risk overwriting valuable knowledge, whereas conservative updates limit flexibility. In addition, large-scale memory stores increase storage and retrieval costs, hindering longterm robot deployment. 

### **4.3 Full-lifecycle Multimodal Self-evolving Memory** 

Paradigm 6 represents an emerging direction toward self-evolving lifelong memory for VLA agents. Unlike persistent memory mechanisms that mainly store and retrieve experiences, this paradigm aims to enable autonomous memory updating, knowledge consolidation, and capability refinement through continuous interaction [1]. However, fully autonomous self-evolving memory has not yet been demonstrated in current VLA systems [1]. Achieving this capability requires balancing adaptation and knowledge stability while addressing challenges in memory reliability, scalability, and autonomous memory management [3]. 

7 

## **5 Benchmarks and Evaluation** 

Recent benchmarks evaluate different aspects of embodied intelligence, including manipulation generalization through SimplerEnv [20], continual skill learning through LIBERO and LIBERO-Long [8], long-horizon execution through CALVIN [2], compositional reasoning through LoHoRavens [22], and memory-intensive manipulation in non-Markovian environments through LIBERO-Mem [23]. However, existing evaluations still mainly focus on task-level metrics, such as success rate, execution duration, and continual learning performance, while providing limited assessment of memory quality and effectiveness [8]. In particular, current continual learning benchmarks mainly measure forgetting through performance degradation after sequential training, but rarely evaluate whether agents can retain semantic knowledge, manipulation skills, and previous experiences [3, 5, 6, 8, 12]. Future benchmarks should therefore incorporate quantitative metrics for memory retention, forgetting resistance, retrieval effectiveness, and memory efficiency, considering the relationship between stored information, retrieval cost, and task performance. 

Quantitative evaluation of memory capabilities should consider both task performance and memory-specific metrics. Memory retention can be measured by evaluating whether previously acquired skills remain accessible after long intervals or intervening tasks. Retrieval effectiveness can be evaluated through retrieval accuracy or recall of relevant experiences, while memory efficiency can consider storage consumption and inference latency. Such metrics would enable more direct comparison between different memory architectures beyond task success rates. 

## **6 Open Challenges and Future Directions** 

VLA memory research has gradually expanded from using short observation contexts to storing and reusing information across longer interactions. However, current memory designs still lack a complete mechanism for continuous adaptation during robot deployment. Key challenges remain in memory organization, experience incorporation, knowledge maintenance, and efficient retrieval. Most existing methods separate memory storage from usage, leaving memory selection, modification, and forgetting strategies underexplored. For long-term operation, adaptive memory management based on task relevance, usage frequency, and future utility is needed to maintain compact and effective memory structures [12]. Moreover, persistent memory updating remains limited, as many approaches rely on training-time knowledge or temporary task records. Modular memory structures that enable deployment-time updates without retraining remain an important direction [10]. 

Beyond experience storage, lifelong VLA learning also requires transforming accumulated information into reusable skills. Memory consolidation and automatic skill discovery may help extract transferable behaviors from previous interactions [8, 15]. Meanwhile, efficient retrieval becomes increasingly important as multimodal memory grows, where hierarchical retrieval mechanisms can reduce search costs and improve access to relevant experiences in long-horizon tasks [9]. 

8 

## **7 Conclusion** 

Memory in VLA models has been reviewed in this survey from the perspective of scope and persistence, providing a taxonomy that connects different memory architectures within a common framework. Based on representative systems covering slidingwindow policies, implicit fusion, retrieval-based memory, and persistent memory designs, we discuss how memory mechanisms have developed to support longhorizon embodied intelligence. These approaches have improved the reuse of previous experiences and temporal reasoning ability, but persistent memory during deployment remains limited in current open-source VLA systems. The gap between algorithmic progress and practical deployment indicates the need for memory mechanisms that can retain, retrieve, consolidate, and update knowledge over long-term operation while satisfying computational constraints. The discussion in this survey is also subject to several limitations. The taxonomy and qualitative comparison are derived from the representative systems considered in this work, and the lack of standardized benchmarks still makes it difficult to evaluate different memory mechanisms in a unified manner. Broader evaluations covering more emerging VLA systems, together with quantitative protocols for memory retention, retrieval, and lifelong adaptation, will be important for future studies. 

## **References** 

1. Ma, Y., Song, Z., Zhuang, Y., Hao, J., King, I.: A Survey on Vision-Language-Action Models for Embodied AI. IEEE Transactions on Neural Networks and Learning Systems 37, 3031–3051 (2026). https://doi.org/10.1109/TNNLS.2025.3650584 

2. Mees, O., Hermann, L., Rosete-Beas, E., Burgard, W.: CALVIN: A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation Tasks. IEEE Robotics and Automation Letters 7, 7327–7334 (2022). https://doi.org/10.1109/LRA.2022.3180108 

3. Parisi, G.I., Kemker, R., Part, J.L., Kanan, C., Wermter, S.: Continual lifelong learning with neural networks: A review. Neural Networks 113, 54–71 (2019). https://doi.org/10.1016/j.neunet.2019.01.012 

4. Cheang, C.-L., Chen, G., Jing, Y., Kong, T., Li, H., Li, Y., Liu, Y., Wu, H., Xu, J., Yang, Y., Zhang, H., Zhu, M.: GR-2: A Generative Video-Language-Action Model with WebScale Knowledge for Robot Manipulation. In: Proceedings of the IEEE International Conference on Robotics and Automation (ICRA), pp. 1–8 (2025) 

5. Rolnick, D., Ahuja, A., Schwarz, J., Lillicrap, T., Wayne, G.: Experience Replay for Continual Learning. In: Advances in Neural Information Processing Systems, vol. 32. Curran Associates, Inc. (2019) 

6. Lopez-Paz, D., Ranzato, M.A.: Gradient Episodic Memory for Continual Learning. In: Advances in Neural Information Processing Systems, vol. 30. Curran Associates, Inc. (2017) 

7. Graves, A., Wayne, G., Reynolds, M., Harley, T., Danihelka, I., Grabska-Barwińska, A., Colmenarejo, S.G., Grefenstette, E., Ramalho, T., Agapiou, J., Badia, A.P., Hermann, K.M., Zwols, Y., Ostrovski, G., Cain, A., King, H., Summerfield, C., Blunsom, P., Kavuk- 

9 

   - cuoglu, K., Hassabis, D.: Hybrid computing using a neural network with dynamic external memory. Nature 538, 471–476 (2016). https://doi.org/10.1038/nature20101 

8. Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., Stone, P.: LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning. In: Advances in Neural Information Processing Systems, vol. 36, pp. 44776–44791. Curran Associates, Inc. (2023) 

9. Sridhar, A., Pan, J., Sharma, S., Finn, C.: MemER: Scaling Up Memory for Robot Control via Experience Retrieval. In: International Conference on Learning Representations (ICLR) (2026) 

10. Shi, H., Xie, B., Liu, Y., Sun, L., Liu, F., Wang, T., Zhou, E., Fan, H., Zhang, X., Huang, G.: MemoryVLA: Perceptual-Cognitive Memory in Vision-Language-Action Models for Robotic Manipulation. In: International Conference on Learning Representations (ICLR) (2026) 

11. Li, X., Liu, M., Zhang, H., Yu, C., Xu, J., Wu, H., Cheang, C., Jing, Y., Zhang, W., Liu, H.: Vision-language foundation models as effective robot imitators. In: International Conference on Learning Representations. pp. 26703–26721 (2024) 

12. Kirkpatrick, J., Pascanu, R., Rabinowitz, N., Veness, J., Desjardins, G., Rusu, A.A., Milan, K., Quan, J., Ramalho, T., Grabska-Barwinska, A., Hassabis, D., Clopath, C., Kumaran, D., Hadsell, R.: Overcoming catastrophic forgetting in neural networks. Proceedings of the National Academy of Sciences 114, 3521–3526 (2017). https://doi.org/10.1073/pnas.1611835114 

13. Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Shi, L.X., Tanner, J., Vuong, Q., Walling, A., Wang, H., Zhilinsky, U.: π0: A Vision-Language-Action Flow Model for General Robot Control. In: Robotics: Science and Systems XXI (2025) 

14. Physical Intelligence: OpenPI: Open-Source Vision-Language-Action Models for Robotics, https://github.com/Physical-Intelligence/openpi, (2025) 

15. Mon-Williams, R., Li, G., Long, R., Du, W., Lucas, C.G.: Embodied large language models enable robots to complete complex tasks in unpredictable environments. Nature Machine Intelligence 7, 592–601 (2025). https://doi.org/10.1038/s42256-025-01005-x 

16. Kim, M.J., Pertsch, K., Karamcheti, S., et al.: OpenVLA: An Open-Source VisionLanguage-Action Model. In: Proceedings of The 8th Conference on Robot Learning, pp. 2679–2713. PMLR (2025) 

17. Lei, M., Cai, H., Cui, Z., et al.: RoboMemory: A Brain-inspired Multi-memory Agentic Framework for Lifelong Learning in Physical Embodied Systems. In: NeurIPS 2025 Workshop on Space in Vision, Language, and Embodied AI (2025) 

18. Open X-Embodiment Team, Ghosh, D., Walke, H., et al.: Octo: An Open-Source Generalist Robot Policy. In: Proceedings of Robotics: Science and Systems (RSS) (2024) 

19. Li, R., Guo, W., Wu, Z., Wang, C., Deng, H., Weng, Z., Tan, Y.-P., Wang, Z.: MAP-VLA: Memory-Augmented Prompting for Vision-Language-Action Model in Robotic Manipulation. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) (2026) 

20. Li, X., Hsu, K., Gu, J., Pertsch, K., Mees, O., Walke, H.R., Fu, C., Lunawat, I., Sieh, I., Kirmani, S., Levine, S., Wu, J., Finn, C., Su, H., Vuong, Q., Xiao, T.: Evaluating RealWorld Robot Manipulation Policies in Simulation. In: Proceedings of the 8th Conference on Robot Learning (CoRL), pp. 2640–2678. PMLR (2024) 

21. Hu, Y., Cui, J., Lu, J., Yang, R., Ye, J., Zhao, B., Chen, X., Lan, X., Ren, P.: ECHO: Continuous Hierarchical Memory for Vision-Language-Action Models. arXiv preprint arXiv:2605.10993 (2026) 

10 

22. Zhang, S., Wicke, P., Şenel, L.K., Figueredo, L., Naceri, A., Haddadin, S., Plank, B., Schütze, H.: LoHoRavens: A Long-Horizon Language-Conditioned Benchmark for Robotic Tabletop Manipulation. In: 6th Robot Learning Workshop at NeurIPS (2023) 

23. Chung, N., Hanyu, T., Nguyen, T., Le, H., Bumgarner, F., Nguyen, D.M.H., Vo, K., Yamazaki, K., Rainwater, C., Kieu, T., Nguyen, A., Le, N.: Rethinking Progression of Memory State in Robotic Manipulation: An Object-Centric Perspective. In: Proceedings of the AAAI Conference on Artificial Intelligence, vol. 40, pp. 3407–3415 (2026) 

24. Chi, C., Feng, S., Du, Y., Xu, Z., Cousineau, E., Burchfiel, B., Song, S.: Diffusion Policy: Visuomotor Policy Learning via Action Diffusion. In: Proceedings of Robotics: Science and Systems XIX (2023) 

25. Wang, Z., Yu, B., Zhao, J., Sun, W., Hou, S., Liang, S., Hu, X., Han, Y., Gan, Y.: KARMA: Augmenting Embodied AI Agents with Long-and-short Term Memory Systems. In: Proceedings of the IEEE International Conference on Robotics and Automation (ICRA), pp. 1–8 (2025) 

26. Huang, W., Xia, F., Xiao, T., Chan, H., Liang, J., Florence, P., Zeng, A., Tompson, J., Mordatch, I., Chebotar, Y., Sermanet, P., Jackson, T., Brown, N., Luu, L., Levine, S., Hausman, K., Ichter, B.: Inner Monologue: Embodied Reasoning through Planning with Language Models. In: Proceedings of The 6th Conference on Robot Learning, pp. 1769– 1782. PMLR (2023) 

27. Zeng, Y., Ye, M., Chen, Y., Shentu, Y., Wu, P., Yan, Z., Li, Z.: KEMO: Event-Driven Keyframe Memory for Long-Horizon Robot Manipulation with VLA Policies. arXiv preprint arXiv:2606.23589 (2026) 

28. Xie, Q., Min, S.Y., Ji, P., Yang, Y., Zhang, T., Xu, K., Bajaj, A., Salakhutdinov, R., Johnson-Roberson, M., Bisk, Y.: Embodied-RAG: General Non-parametric Embodied Memory for Retrieval and Generation. In: Advances in Neural Information Processing Systems, vol. 37, pp. 2409–2421 (2024) 

29. Chen, L., Lu, K., Rajeswaran, A., Lee, K., Grover, A., Laskin, M., Abbeel, P., Srinivas, A., Mordatch, I.: Decision Transformer: Reinforcement Learning via Sequence Modeling. In: Advances in Neural Information Processing Systems, vol. 34, pp. 15084–15097. Curran Associates, Inc. (2021) 

30. Shridhar, M., Manuelli, L., Fox, D.: CLIPort: What and Where Pathways for Robotic Manipulation. In: Proceedings of the 5th Conference on Robot Learning, pp. 894–906. PMLR (2022) 

31. Li, Y., Zhong, H., Müller, S.: Multi-context fusion transformer for pedestrian crossing intention prediction in urban environments. arXiv preprint arXiv:2511.20011 (2025) 

32. Li, Y., Müller, S.: ACIT: Attention-guided cross-modal interaction transformer for pedestrian crossing intention prediction. In: Proceedings of the 2025 IEEE 28th International Conference on Intelligent Transportation Systems (ITSC), pp. 2018–2024 (2025) 

33. Li, Y., Müller, S.: MTC: Multimodal transformer with cross-modality guided attention for pedestrian crossing intention prediction. IEEE Sensors Journal 25(24), 44929–44939 (2025) 

