---
title: "World Models: A Comprehensive Survey of Architectures, Methodologies, Reasoning Paradigms, and Applications"
date: "2026-05-28"
authors: "Arif Hassan Zidan; Yi Pan; Hanqi Jiang; Ruiyu Yan; Wei Ruan; Zihao Wu"
url: https://arxiv.org/abs/2606.00133
pdf: https://arxiv.org/pdf/2606.00133
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.00133)** / [論文ページ](https://arxiv.org/abs/2606.00133)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# World Models: A Comprehensive Survey of Architectures, Methodologies, Reasoning Paradigms, and Applications 

Arif Hassan Zidan<sup>1</sup> , Yi Pan<sup>2</sup> , Hanqi Jiang<sup>2</sup> , Ruiyu Yan<sup>9</sup> , Wei Ruan<sup>2</sup> , Zihao Wu<sup>2</sup> , Lifeng Chen<sup>2</sup> , Weihang You<sup>2</sup> , Xinliang Li<sup>2</sup> , Bowen Chen<sup>3</sup> , Huawen Hu<sup>2</sup> , Peilong Wang<sup>10</sup> , Sizhuang Liu<sup>12</sup> , Jing Zhang<sup>5</sup> , Siyuan Li<sup>2</sup> , Zhengliang Liu<sup>2</sup> , Yu Bao<sup>6</sup> , Lin Zhao<sup>3</sup> , Lichao Sun<sup>7</sup> , Dajiang Zhu<sup>5</sup> , Xiang Li<sup>4</sup> , Jinglei Lv<sup>8</sup> , Quanzheng Li<sup>4</sup> , Wei Liu<sup>11</sup> , Tianming Liu<sup>*2</sup> , and Wei Zhang<sup>*1</sup> 

> 1School of Computer and Cyber Sciences, Augusta University, Augusta, GA, USA 

> 2School of Computing, University of Georgia, Athens, GA, USA 

> 3Department of Biomedical Engineering, New Jersey Institute of Technology, Newark, NJ, USA 

> 4Department of Radiology, Massachusetts General Hospital, Harvard Medical School, Boston, MA, USA 

> 5Department of Computer Science and Engineering, University of Texas at Arlington, Arlington, TX, USA 

> 6Department of Graduate Psychology, James Madison University, Harrisonburg, VA, USA 

> 7Computer Science and Engineering, Lehigh University, Bethlehem, PA, USA 

> 8School of Biomedical Engineering, The University of Sydney, Sydney, Australia 

> 9Tandon School of Engineering, New York University, Brooklyn, NY, USA 

> 10Department of Radiation Oncology, City of Hope National Medical Center, Duarte, CA, 

USA 

> 11Department of Mayo Clinic Comprehensive Cancer Center, Mayo Clinics, Phoenix, AZ, USA 

> 12Savannah River Ecology Laboratory (SREL), University of Georgia, Aiken, SC, USA 

> * **Corresponding author(s).** E-mail(s): tliu@uga.edu; wzhang2@augusta.edu 

##### **Abstract** 

World models, internal simulators that learn the structure and dynamics of an environment, have emerged as a central paradigm in the pursuit of artificial general intelligence, enabling agents to predict, plan, and reason within learned representations. Despite rapid progress across reinforcement learning, robotics, autonomous driving, and video generation, the field still lacks a unified framework capable of integrating its diverse architectural choices, training methodologies, reasoning mechanisms, and application settings. This survey addresses that gap by introducing a comprehensive multi-axis taxonomy organized along four complementary dimensions: (i) architecture, encompassing representation format, dynamics formulation, input modality, learning paradigm, and downstream application; (ii) methodological family, including state-space and recurrent approaches, transformer-based models, diffusion-based generators, physics-informed networks, and language-augmented multimodal systems; (iii) reasoning strategy, covering imagination-based planning, latent policy learning, counterfactual reasoning, and planning under uncertainty; and (iv) application domain, spanning robotics, autonomous driving, video prediction, multimodal agents, reinforcement learning, scientific modeling, medical 

1 

imaging, educational measurement, and business and finance. Tracing the historical development of the field from early cognitive-science foundations to milestone systems such as PlaNet, the Dreamer family, MuZero, Sora, Cosmos, and Genie, we examine how these dimensions interact and highlight the recent convergence of chain-of-thought reasoning with world-model imagination. Across these axes, we review evaluation protocols and benchmarks, identify persistent challenges—including compounding prediction errors, sim-to-real transfer, and fragmented evaluation practices—and outline future directions toward unified multimodal world models, foundation-scale interactive simulators, and safe deployment in safety-critical domains. By synthesizing these developments within a single cross-disciplinary framework, this survey provides a structured roadmap for advancing world-model research toward more general, robust, and capable autonomous systems. 

## **Contents** 

|**1**<br>**Intr**|**oduct**|**ion**|**5**|
|---|---|---|---|
|**2**<br>**Bac**|**kgrou**|**nd and Conceptual Foundations of World Model**|**7**|
|2.1|Defini|ition and Basic Concepts . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. .<br>8|
|2.2|Key c|omponents of a world model<br>. . . . . . . . . . . . . . . . . . . . . . . . . .|. .<br>11|
|2.3|Funda|mental distinctions between World models and model-free RL<br>. . . . . . .|. .<br>13|
|2.4|Role o|f latent spaces in world models . . . . . . . . . . . . . . . . . . . . . . . . .|. .<br>15|
|**3**<br>**Cat**|**egoriz**|**ation of World Models by Architecture**|**16**|
|3.1|Classii|fication by representation . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. .<br>16|
||3.1.1|Observation-space (pixel-level) representations. . . . . . . . . . . . . . . .|. .<br>17|
||3.1.2|Continuous latent representations. . . . . . . . . . . . . . . . . . . . . . .|. .<br>17|
||3.1.3|Discrete token representations. . . . . . . . . . . . . . . . . . . . . . . . .|. .<br>17|
||3.1.4|Joint-embedding (representation-space) predictions.<br>. . . . . . . . . . . .|. .<br>17|
||3.1.5|Structured and object-centric representations. . . . . . . . . . . . . . . . .|. .<br>18|
||3.1.6|3D and occupancy-based representations.<br>. . . . . . . . . . . . . . . . . .|. .<br>18|
|3.2|Classii|fication by dynamics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. .<br>18|
||3.2.1|Deterministic Dynamics . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. .<br>19|
||3.2.2|Stochastic Dynamics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. .<br>19|
||3.2.3|Implicit Generative Dynamics . . . . . . . . . . . . . . . . . . . . . . . . .|. .<br>19|
||3.2.4|Representation-space Predictive Dynamics . . . . . . . . . . . . . . . . . .|. .<br>19|
||3.2.5|Memory-Augmented Dynamics . . . . . . . . . . . . . . . . . . . . . . . .|. .<br>20|
||3.2.6|Discussion and Open Challenges<br>. . . . . . . . . . . . . . . . . . . . . . .|. .<br>20|
|3.3|Classii|fication by Modality . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. .<br>20|
||3.3.1|Visual-Only World Models<br>. . . . . . . . . . . . . . . . . . . . . . . . . .|. .<br>21|
||3.3.2|Language-Only World Models . . . . . . . . . . . . . . . . . . . . . . . . .|. .<br>22|
||3.3.3|3D Geometric World Models<br>. . . . . . . . . . . . . . . . . . . . . . . . .|. .<br>23|
||3.3.4|Proprioceptive and Tactile World Models<br>. . . . . . . . . . . . . . . . . .|. .<br>23|
||3.3.5|Multimodal Fusion World Models . . . . . . . . . . . . . . . . . . . . . . .|. .<br>24|
||3.3.6|Discussion and Open Challenges<br>. . . . . . . . . . . . . . . . . . . . . . .|. .<br>25|
|3.4|Classii|fication by learning paradigms<br>. . . . . . . . . . . . . . . . . . . . . . . . .|. .<br>25|
||3.4.1|Self-Supervised and Unsupervised Learning . . . . . . . . . . . . . . . . .|. .<br>25|
||3.4.2|Online Model-Based Reinforcement Learning . . . . . . . . . . . . . . . .|. .<br>27|
||3.4.3|Offline and Batch Learning . . . . . . . . . . . . . . . . . . . . . . . . . .|. .<br>28|
||3.4.4|Foundation Model Paradigm: Large-Scale Pretraining and Adaptation . .|. .<br>28|


2 

||3.4.5|Supervised and Imitation Learning . . . . . . . . . . . . . . . . . . . .|. . . .<br>29|
|---|---|---|---|
||3.4.6|Hybrid and Multi-Stage Learning Paradigms<br>. . . . . . . . . . . . . .|. . . .<br>30|
||3.4.7|Discussion and Open Challenges<br>. . . . . . . . . . . . . . . . . . . . .|. . . .<br>31|
|3.5|Classii|fication by downstream use . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>33|
||3.5.1|Reinforcement Learning and Planning . . . . . . . . . . . . . . . . . .|. . . .<br>33|
||3.5.2|Autonomous Driving . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>33|
||3.5.3|Robotics and Embodied AI . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>34|
||3.5.4|Healthcare and Medical Imaging . . . . . . . . . . . . . . . . . . . . .|. . . .<br>34|
||3.5.5|Video Generation and Creative Simulation<br>. . . . . . . . . . . . . . .|. . . .<br>35|
||3.5.6|Language Reasoning and Decision-Making . . . . . . . . . . . . . . . .|. . . .<br>35|
||357|DiscussionandOenChallenes|36|
||..|p g<br>. . . . . . . . . . . . . . . . . . . . .|. . . .<br>|
|**4**<br>**Cat**|**egoriz**|**ation of World Models by Methodological Families**|**36**|
|4.1|State-|space and recurrent latent world models . . . . . . . . . . . . . . . . . .|. . . .<br>36|
|4.2|Transf|ormer-based world models<br>. . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>37|
|4.3|Diffus|fion-Based World Models . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>40|
|4.4|Physic|s-informed and structured world model . . . . . . . . . . . . . . . . . .|. . . .<br>43|
|4.5|Langu|age-augmented and multi-modal world models . . . . . . . . . . . . . .|. . . .<br>47|
|**5**<br>**Cat**|**egoriz**|**ation of World Models by Reasoning Strategy**|**52**|
|5.1|Imagi|nation-based planning . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>53|
||5.1.1|Imagination during learning: background planning. . . . . . . . . . . .|. . . .<br>54|
||5.1.2|Imagination at decision time: forward search. . . . . . . . . . . . . . .|. . . .<br>54|
||5.1.3|Cross-domain advantages of latent imagination. . . . . . . . . . . . . .|. . . .<br>55|
||5.1.4|Open challenges: compounding errors and objective mismatch. . . . .|. . . .<br>55|
|5.2|Policy|learning with a world model . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>56|
|5.3|Count|erfactual reasoning . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>58|
||5.3.1|The abduction–action–prediction pipeline. . . . . . . . . . . . . . . . .|. . . .<br>59|
||5.3.2|Why counterfactuals matter: isolating decision effects. . . . . . . . . .|. . . .<br>59|
||5.3.3|Toward causally structured world models. . . . . . . . . . . . . . . . .|. . . .<br>60|
||5.3.4|Fundamental limits: non-identifiability and counterfactual validity. . .|. . . .<br>61|
|5.4|Plann|ing under uncertainty . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>61|
|**6**<br>**Cat**|**egoriz**|**ation of World Models by Application Domains**|**63**|
|6.1|Robot|ics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>63|
|6.2|Auton|omous driving and control systems . . . . . . . . . . . . . . . . . . . . .|. . . .<br>67|
|6.3|Video|prediction and scene understanding . . . . . . . . . . . . . . . . . . . .|. . . .<br>69|
|6.4|Multi|modal agents and language-grounded systems . . . . . . . . . . . . . . .|. . . .<br>75|
|6.5|Reinfo|rcement learning and Games . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>78|
|6.6|Scienti|ific and Domain-specific Modeling . . . . . . . . . . . . . . . . . . . . .|. . . .<br>82|
|6.7|i<br>Medic|ii<br>al Images and Video Recordings . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>85|
||6.7.1|Medical Imaging Analysis and Progressive Disease Prediction . . . . .|. . . .<br>85|
||6.7.2|Tumor Evolution and Treatment Planning . . . . . . . . . . . . . . . .|. . . .<br>87|
||6.7.3|Surgical Video and Robotic Surgery<br>. . . . . . . . . . . . . . . . . . .|. . . .<br>88|
||6.7.4|Disease Progression Modeling from Electronic Health Records . . . . .|. . . .<br>89|
||6.7.5|Capability Assessment and Open Challenges<br>. . . . . . . . . . . . . .|. . . .<br>89|
|6.8|Educa|tional Measurement . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>90|
|6.9|Busin|ess and Finance<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . .<br>94|


3 

||6.9.1|Beyond physical laws: the belief-modeling paradigm. . . . . . . . . . . . . . .<br>94|
|---|---|---|
||6.9.2|Methodological trajectories. . . . . . . . . . . . . . . . . . . . . . . . . . . . .<br>94|
||6.9.3|The imperative of counterfactual reasoning in corporate and financial strategy. 95|
||6.9.4|Fundamental bottlenecks: non-stationarity, identifiability, and reflexivity.<br>. .<br>95|
|**7**<br>**Ev**|**aluatio**|**n Protocols and Benchmarks**<br>**96**|
|7.1|Comm|on Evaluation Metrics<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .<br>96|
|7.2|Bench|mark Environments and Datasets<br>. . . . . . . . . . . . . . . . . . . . . . . . .<br>97|
|**8**<br>**Ma**|**jor Ch**|**allenges and Limitations**<br>**99**|
|**9**<br>**Dis**|**cussion**|**and Future Directions**<br>**106**|


4 

## **1 Introduction** 

The pursuit of artificial general intelligence (AGI) has long motivated researchers to develop intelligent systems that not only recognize meaningful patterns from multimodal data but also acquire a coherent and causal understanding of the environments in which they operate. Central to this ambition is the concept of the World Model (WM)—an internal simulator that captures environmental dynamics and enables both forward and counterfactual rollouts for perception, prediction, and decision-making [1]. The intellectual foundations of this idea extend far beyond contemporary machine learning. In cognitive science, it has long been recognized that humans interpret the external world by abstracting it into simplified elements and relational structures. This perspective is articulated in Johnson-Laird’s theory of mental models [2] and resonates with early developments in artificial intelligence, such as Minsky’s frame representations proposed in the 1970s [3]. In brief, these perspectives highlight the longstanding interdisciplinary interest in constructing internal representations that enable reasoning about complex environments. 

While these early frameworks were largely symbolic, the advent of deep learning ushered in a new era for operationalizing the world model concept. In reinforcement learning (RL), Ha and Schmidhuber [4] revitalized this idea by demonstrating that generative neural networks can learn compact spatial and temporal representations of an environment in an unsupervised manner. Notably, their work showed that agents could even be trained entirely within internally generated simulations derived from these learned representations. More recently, LeCun [5] identified the world model as a central architectural component for autonomous intelligence, proposing that it should infer missing information about the current state of the world and predict plausible future states resulting from imagined sequences of actions. 

Since these seminal contributions, the field has expanded rapidly in both scope and ambition. In model-based reinforcement learning (MBRL), the Dreamer series [6–8] demonstrated that agents can learn complex behaviors entirely through latent imagination, scaling from simple control tasks to diverse domains using a unified algorithmic framework. In parallel, DeepMind’s MuZero [9] achieved superhuman performance in several challenging domains without access to explicit environment rules by learning an implicit model that predicts only planning-relevant quantities. 

Beyond MBRL, OpenAI’s Sora [10] introduced large-scale video generation as a form of world simulation, sparking debate about whether such models constitute genuine world models [11]. Foundation model approaches from Meta (V-JEPA 2 [12]), DeepMind (Genie [13]), and NVIDIA (Cosmos [14]) have further demonstrated that large-scale self-supervised pretraining can yield actionable world simulators for robotic planning, interactive environment generation, and physical AI, respectively. These efforts align with LeCun’s broader vision [5] of a modular cognitive architecture centered on a configurable predictive world model trained via his proposed Joint-Embedding Predictive Architecture (JEPA), offering a theoretically grounded alternative to purely generative approaches. Collectively, these developments have transformed world models from a niche MBRL topic into a central pillar of the broader pursuit of AGI. 

Within this expanding landscape, a particularly promising development is the integration of chain-of-thought (CoT) reasoning [15] with world models. Traditional CoT represents reasoning as explicit sequences of natural language tokens, a process that can be computationally expensive and limited by the relatively low information density of discrete textual representations [16]. Recent research has begun to shift this reasoning process into latent spaces, where world models provide the underlying substrate for multi-step deliberation. For instance, Coconut [17] introduces continuous thought representations that enable breadth-first reasoning directly in latent space. Similarly, LCDrive [18] integrates CoT-style reasoning with action planning by interleaving action-proposal tokens with latent world model predictions, allowing agents to simulate counterfactual futures 

5 

before committing to a trajectory. Building on this direction, FutureX [19] proposes an auto-think mechanism that dynamically activates a latent world model only when scene complexity warrants deliberative reasoning. Collectively, these approaches suggest that world models may function not merely as predictive simulators but also as reasoning engines in their own right—potentially replacing linguistic chains of thought with grounded, spatiotemporal chains of imagination (CoI). 

Notably, the growing prominence of world models is also driven by increasing recognition of the fundamental limitations of large language models (LLMs) built on transformer architectures [20, 21]. Despite the remarkable success of models such as GPT-4 [22] and reasoning-augmented systems like o1 [23] in tasks involving language understanding and code generation, these systems operate primarily within the discrete and relatively low-dimensional space of text tokens. As a result, they lack a grounded understanding of the continuous and high-dimensional physical world [5]. Meanwhile, LLMs generally lack persistent world-state representations, have limited capacity for causal reasoning, and struggle with long-horizon planning—capabilities that are routinely exhibited by biological organisms. This gap reflects Moravec’s paradox [24]: while high-level cognitive tasks such as language processing and chess playing appear tractable for machines, sensorimotor competencies that have been refined through billions of years of biological evolution remain far more difficult to replicate. 

In contrast, world models aim to address these limitations by learning to predict the consequences of actions within physical or simulated environments, thereby constructing internal representations of object dynamics and temporal evolution. By enabling agents to simulate possible futures and evaluate alternative action sequences, world models provide a foundation for planning, reasoning, and adaptive decision-making in complex environments. The growing institutional investment in this direction—exemplified by the establishment of Advanced Machine Intelligence (AMI) [25], DeepMind’s continued development of the Genie family of models, and NVIDIA’s Cosmos platform—signals an emerging consensus that the next frontier of artificial intelligence lies in building systems capable of modeling and interacting with the world itself. 

Yet, as research activity accelerates and world models attract attention from increasingly diverse communities, a fundamental question remains: what exactly constitutes a world model? In model-based reinforcement learning (MBRL), the concept is often defined narrowly as a learned transition function _T_<sup>�</sup> ( _st_ +1 _| st, at_ ) coupled with a reward predictor _R_<sup>�</sup> ( _rt | st, at_ ) [26]. In the broader AI literature, however, world models are increasingly viewed as general-purpose simulators capable of supporting counterfactual reasoning, causal inference, and hierarchical planning [1, 5]. This diversity of perspectives has led to a fragmented research landscape, in which communities working on latent dynamics models, generative video prediction, object-centric representations, and language-grounded planning often develop their approaches in relative isolation. 

Importantly, various recent surveys have begun to organize this rapidly evolving field. For example, Ding et al. [11] examine world models from the perspective of understanding versus prediction, while Li et al. [1] propose a three-axis taxonomy for embodied AI. Additional domainspecific surveys have explored applications in autonomous driving [27], robotic manipulation [28], and 3D/4D scene modeling [29]. Nevertheless, existing reviews typically focus on specific methodological perspectives or application domains and do not simultaneously address the full spectrum of architectural paradigms, methodological families, reasoning mechanisms, and application contexts within a unified framework. The world models are opening up an underexplored domains, including medical imaging and educational measurement—further highlighting the need for a comprehensive, cross-disciplinary survey. 

To address this gap, this survey provides a structured and comprehensive review organized along several complementary axes: 

6 

1. **Architecture** (Section 3): key architectural design choices, including representation type, dynamics modeling approach, input modality, learning paradigm, and downstream use cases. 

2. **Methodological Families** (Section 4): major modeling paradigms such as state-space and recurrent latent models, variational and generative approaches, transformer-based architectures, object-centric and compositional models, physics-informed models, and languageaugmented multimodal systems. 

3. **Reasoning Strategies** (Section 5): mechanisms for decision-making and planning, including imagination-based planning, policy learning within learned models, counterfactual reasoning, long-horizon and hierarchical planning, and planning under uncertainty. 

4. **Application Domains** (Section 6): representative application areas, including robotics, autonomous driving, video prediction and scene understanding, multimodal agents, reinforcement learning and games, scientific modeling, medical imaging and video analysis, and educational measurement. 

Figure 1 summarizes this landscape visually, organized in three layers. _Top:_ The conceptual taxonomy divides world models into two complementary perspectives—implicit representations of the external world, encompassing decision-making (Section 5) and world knowledge learning (Section 4), and future predictions of the physical world, covering video generation (Section 6) and embodied environments (Section 3). _Middle:_ A historical timeline of milestone contributions, from Minsky’s frame system theory (1974) through Ha and Schmidhuber’s neural world models (2018), LeCun’s JEPA (2022), world knowledge in LLMs (2023), to recent large-scale simulators including Sora and UniSim (2024). _Bottom:_ Representative application-domain deployments—DayDreamer for robotics (Section 6.1), Smallville for social simulacra (Section 6.4), and Vista for autonomous driving (Section 6.2)—illustrating the breadth of deployment contexts that world models now support. Additionally, we further examine evaluation protocols and benchmarks (Section 7), identify key challenges facing current approaches (Section 8), and outline promising directions for future research (Section 9). By providing a unified, multi-axis perspective, this survey aims to serve both as a comprehensive reference for researchers entering the field and as a roadmap for advancing world models toward robust, general-purpose autonomous intelligence. 

## **2 Background and Conceptual Foundations of World Model** 

World models are state-of-the-art intelligent models that enable an intelligent agent to form compact representations of its environment and predict how that environment may evolve over time. In artificial intelligence, the modern idea is closely associated with model-based reinforcement learning and generative latent-dynamics modeling, where an agent learns not only how to act but also how the world changes in response to actions. 

Conceptually, world models are rooted in a broader predictive view of intelligence. Rather than reacting only to current inputs, intelligent systems benefit from anticipating future states, estimating consequences of actions, and using internal simulation to guide behavior. This idea has strong connections to earlier traditions in cognitive science, neuroscience, and reinforcement learning, including predictive processing, predictive coding, and predictive representations. The following sections present the vital background, conceptual architecture, and foundations of World Model. 

7 


Figure 1: Overview of the world model landscape, organized into a conceptual taxonomy of implicit representations and future predictions, a historical timeline of milestone contributions from 1974 to 2024, and representative application-domain deployments spanning robotics, social simulation, and autonomous driving. 

### **2.1 Definition and Basic Concepts** 

In artificial intelligence, a world model is an internal predictive model that captures how an environment evolves over time and how that evolution depends on an agent’s actions. An early formulation by Schmidhuber described a model-building control system in which the controller was equipped with an additional module, the _world model_ , trained to predict future inputs from prior input–action pairs [30]. In contemporary machine learning, the term has broadened while retaining this core idea: a world model is a learned representation of environment dynamics that supports prediction, simulation, and decision-making. Ha and Schmidhuber’s neural world-model framework made this formulation especially influential in modern deep learning by demonstrating that an agent can learn compressed spatial and temporal representations of an environment and then use them to support downstream control [4]. 

To make this definition precise, let _ot_ denote the observation at time _t_ , _at_ the action, _rt_ the reward, and _st_ a latent state intended to summarize the information necessary for predicting the future. A world model can then be written as a parameterized predictive system with parameters _θ_ that approximates the environment dynamics 

To formalize this definition, let _ot_ denote the observation at time _t_ , _at_ the action, _rt_ the reward, and _st_ a latent state, intended to summarize the information necessary for predicting the future. A world model can then be expressed as a parameterized predictive system with parameters _θ_ that approximates the environment dynamics: 


In fully observed settings, one may identify _st_ with the true environment state. In partially observed 

8 

settings, however, the model must infer a latent belief-like state from the history _ht_ = ( _o≤t, a<t_ ), for example through an encoder of the form 

In fully observed settings, _st_ may coincide with the true environment state. In partially observed settings, however, the model must infer a latent, belief-like state from the interaction history _ht_ = ( _o≤t, a<t_ ), for example through an encoder of the form 


This notation highlights an essential point: a world model need not reproduce the external world in full detail; rather, it must represent those aspects of experience that are sufficient for useful prediction and control. 

The objective of a world model is therefore not merely to reconstruct observations, but to learn state representations that make future outcomes predictable. In simple settings, this may involve forecasting the next observation directly. In more realistic settings, particularly under partial observability, the model must maintain a latent state that summarizes past observations and actions sufficiently well to predict future observations, rewards, and other task-relevant signals. This perspective helps explain why later work shifted from raw observation prediction to latent dynamics modeling. PlaNet, for instance, learns environment dynamics from images in a compact latent space and explicitly combines deterministic and stochastic transition components, reflecting the insight that useful world models must track both persistent structure and uncertainty over multiple possible futures [31]. Dreamer extends this line of work by treating learned latent dynamics not only as a predictive model but also as a substrate for behavior learning through imagined rollouts [32]. 

Most world models therefore contain several recurring components. First, they include a perception or representation module that compresses high-dimensional sensory inputs into a tractable state representation, such as a latent vector or token sequence. Second, they include an actionconditioned dynamics model that predicts how this latent state evolves over time. Third, many systems incorporate task-level heads, such as reward or continuation predictors, because control requires estimating not only what the world will look like, but also whether imagined trajectories are desirable or terminal. Ha and Schmidhuber instantiated this decomposition using a variational autoencoder for visual compression and a recurrent dynamics model for temporal prediction [33]. PlaNet and Dreamer refined the same blueprint into latent state-space models suitable for planning and policy optimization [31, 32], while Genie scaled the idea into a generative interactive environment built from a spatiotemporal video tokenizer, an autoregressive dynamics model, and a learned latent action interface [13]. 

From a functional perspective, the central promise of world models is imagination. Once a model can simulate likely future trajectories under candidate actions, an agent can use those imagined trajectories to evaluate plans, improve a policy, or train partly or entirely within a learned environment rather than the real one. This is why world models are so closely connected to model-based reinforcement learning. Ha and Schmidhuber showed that policies could be trained inside a modelgenerated environment and then transferred back to the actual task [33]. Dreamer advanced this idea by learning behaviors purely through latent imagination, propagating value gradients through imagined trajectories in compact latent space [32]. Genie broadens the same concept beyond narrow task simulators by introducing action-controllable virtual worlds learned from unlabeled internet video, which the authors describe as a “foundation world model” [13]. Across these variants, the unifying principle is that the model serves as an internal sandbox for counterfactual interaction. 

Formally, if a policy _π_ ( _at | st_ ) acts inside the learned dynamics, the model can generate an imagined rollout 


9 

for horizon _H_ , with actions sampled from _π_ and transitions sampled from _pθ_ ( _st_ +1 _| st, at_ ). Planning or policy learning can then optimize an expected return inside the model, 


where _γ ∈_ [0 _,_ 1) is the discount factor. This equation captures the operational role of a world model: it turns future interaction into a differentiable or at least simulatable object that can be searched, optimized, or evaluated before executing behavior in the real environment. 

Several conceptual distinctions are useful when defining world models. One is the distinction between observation-space and latent-space models. Observation-space models attempt to predict future pixels, frames, or sensor readings directly, whereas latent-space models predict compressed hidden states that are typically more computationally efficient and more useful for planning. A second distinction is between deterministic and stochastic world models. Deterministic models are often simpler, but they may blur over genuinely uncertain futures; stochastic models are better suited to capturing ambiguity and multimodality. A third distinction concerns task-specific versus general-purpose world models. Earlier systems were usually trained on a single environment for planning or control, whereas newer systems such as Genie seek to learn broadly reusable, actioncontrollable generative environments from large-scale, weakly supervised data. These distinctions matter because they shape what the model can represent, how it is trained, and how its predictions can be used. 

Meanwhile, a world model is not equivalent to a perfect simulator or a complete ontology of reality. Its value depends on whether it captures the aspects of the environment that matter for prediction and control. Ha and Schmidhuber explicitly noted that an unsupervised visual model may reproduce visually detailed but task-irrelevant structure while failing to capture features critical for successful behavior [33]. PlaNet likewise framed learned dynamics as a long-standing challenge because errors compound across multi-step prediction horizons, especially in image-based domains [31]. For this reason, the practical quality of a world model is typically judged not only by reconstruction fidelity, but also by whether it yields stable imagined rollouts, supports useful planning, improves sample efficiency, and generalizes beyond the exact trajectories observed during training. In this sense, the core idea of a world model is predictive abstraction: the model should compress experience into a form that is simple enough to simulate yet rich enough to support effective action. 

A world model can also be described more compactly as a learned function _fθ_ that approximates the transition dynamics of an environment: 


where _st_ denotes the state (or observation) at time _t_ , _at_ the action taken, _s_ � _t_ +1 the predicted next state, and _r_ � _t_ +1 the predicted reward. In practice, world models often operate in a learned latent space _zt_ = enc( _ot_ ) rather than directly over raw observations _ot_ , enabling compact representations and tractable long-horizon prediction. 

Moreover, three properties distinguish a world model from a generic predictive model: 

1. **Action-conditioning** : The model predicts how the environment evolves _in response to_ specific actions, enabling counterfactual reasoning (“What would happen if I turned left instead of right?”). 

2. **Multi-step rollout** : The model can be applied autoregressively to generate trajectories of arbitrary length, supporting planning and simulation. 

10 

3. **Utility for decision-making** : The model’s predictions are used downstream—for policy optimization, planning, data augmentation, or safety verification—rather than serving as an end in themselves. 

### **2.2 Key components of a world model** 

Most modern world models operate within a partially observable Markov decision process (POMDP) framework ( _S, A, T, R,_ Ω _, O, γ_ ), where _S_ is the state space, _A_ the action space, _T_ the transition function, _R_ the reward function, Ωthe observation space, _O_ the emission function, and _γ ∈_ [0 _,_ 1) a discount factor. A world model approximates _T_ and optionally _R_ and _O_ . We will summarize multiple key components of World Model in the following four functional modules: 

**Encoder.** The encoder maps raw, high-dimensional observations _ot_ (images, point clouds, sensor readings) into a compact latent representation: 


Notably, this compression step is essential, as raw observations are often too high-dimensional to support tractable multi-step prediction. The encoder can be either deterministic, such as a convolutional neural network, or stochastic, such as the posterior network in a variational autoencoder (VAE). For example, Ha and Schmidhuber [4] used a VAE-based encoder to compress 64 _×_ 64 image frames into 32-dimensional latent vectors. Similarly, the Dreamer family of models [32, 34] employs a posterior encoder conditioned on observation history to infer both deterministic and stochastic components of the latent state. 

**Dynamics model (transition predictor).** The dynamics model predicts the next latent state given the current state and action: 


Importantly, the dynamics model constitutes the core of a world model. In RNN-based architectures [31], it is typically implemented as a Recurrent State-Space Model (RSSM), which factorizes the latent state into a deterministic recurrent component _ht_ that preserves long-range temporal dependencies, and a stochastic component _ht_ that captures uncertainty in the environment. In transformer-based architectures [35, 36], the dynamics model is commonly formulated as an autoregressive transformer that predicts subsequent token(s) in a discrete latent sequence. In diffusion-based approaches [37], future states are generated through an iterative denoising process. 

Besides, at a high level, current world models can be understood as a system composed of three tightly coupled components: a visual model, a memorial model, and a control model. Together, these components enable an agent to perceive its environment, retain and organize past information, and select actions on the basis of predicted future outcomes. This decomposition is especially useful because it clarifies how world models transform raw sensory inputs into structured internal representations that support reasoning, planning, and decision-making. 

The visual model is responsible for perception and representation learning. Its primary role is to transform high-dimensional sensory observations, such as images, video frames, or other raw inputs, into a compact and informative latent representation. In many modern world models, this component is implemented using convolutional neural networks, variational autoencoders, vision transformers, or tokenizers that compress observations into latent vectors or discrete tokens. The importance of the visual model lies in its ability to filter out irrelevant perceptual details while preserving the features that are most critical for downstream prediction and control. Without such compression, directly modeling future trajectories in raw observation space would often be computationally prohibitive and statistically inefficient. 

11 

The memorial model serves as the temporal and predictive core of the architecture. Its function is to maintain a representation of past experience and to model how the latent state of the environment evolves over time. This component is called “memorial” because it provides the system with memory: it integrates current observations with historical context, allowing the agent to infer hidden structure, track temporal dependencies, and represent uncertainty about future states. In recurrent world models, the memorial model is often implemented using recurrent neural networks or recurrent state-space models, which combine deterministic memory states with stochastic latent variables. In more recent architectures, transformers and diffusion-based sequence models have also been used to capture long-range temporal dependencies and generate future latent trajectories. The memorial model is what allows a world model to go beyond static perception and function as a predictive simulator of environment dynamics. 

The control model is the decision-making component. Given the latent state produced by the visual model and updated through the memorial model, the control model determines which action should be taken in order to maximize expected reward, achieve a specified goal, or satisfy a task constraint. In reinforcement learning settings, this component may take the form of a policy network, a value function, or a planning module that evaluates imagined future rollouts generated by the world model. More broadly, the control model translates predictive knowledge into purposeful behavior. Its effectiveness depends not only on the quality of the learned policy, but also on the fidelity of the perceptual and temporal representations provided by the other two components. 

These three modules are not independent; rather, they operate as an integrated system. The visual model encodes the current observation into a latent state, the memorial model updates this latent state in light of prior context and predicts future states, and the control model uses these representations to evaluate alternatives and select actions. Their interaction enables the central capability of a world model: the ability to imagine possible futures before acting in the real environment. In this sense, the visual model answers the question of what is being observed, the memorial model addresses how the world changes over time, and the control model determines what should be done next. 

This tripartite view also provides a useful conceptual framework for comparing different world model architectures. Some systems emphasize stronger visual encoding through powerful tokenization or representation learning, whereas others focus on more expressive memorial mechanisms for long-horizon prediction. Still others devote greater modeling capacity to the control component, especially in tasks that require sophisticated planning or policy optimization. Despite these differences, the visual–memorial–control decomposition captures a common structural logic underlying many world-model-based systems across reinforcement learning, robotics, autonomous systems, and scientific applications. 

**Reward predictor.** The reward predictor estimates the scalar reward from the current latent state: 


Accurate reward prediction is essential for model-based RL, as policy optimization in imagination depends on the quality of predicted returns. MuZero [38] demonstrated that a world model whose dynamics operate entirely in a learned abstract space—predicting reward, value, and policy without ever reconstructing observations—suffices for superhuman performance in Go, chess, shogi, and Atari. 

**Decoder (optional).** The decoder reconstructs observations from latent states: 


12 

Decoders serve two roles: (1) providing a reconstruction loss signal for training the encoder and dynamics model, and (2) enabling visualization of imagined trajectories. However, the decoder is architecturally optional. MuZero dispenses with it entirely, and JEPA-based models [5, 39] predict in representation space rather than pixel space, sidestepping the computational burden and the blurriness associated with pixel-level reconstruction. 

Beyond these four modules, several world models incorporate additional components. _Continuation predictors_ estimate episode termination probabilities. _Discount predictors_ model time-varying discount factors. DreamerV3 [40] uses symlog-transformed predictions and categorical value representations to achieve cross-domain generality. 

### **2.3 Fundamental distinctions between World models and model-free RL** 

A foundational distinction in reinforcement learning lies in whether the agent learns an explicit model of environmental dynamics or learns behavior directly from reward-driven interaction. This divide separates world-model-based approaches from model-free reinforcement learning (RL) and has important consequences for planning, sample efficiency, transfer, uncertainty handling, and interpretability [33, 41]. 

At the most basic level, the two paradigms differ in _what is being learned_ . World-model methods learn predictive structure—for example, transition, observation, and reward dynamics in observation space or in a latent state space—so that future trajectories can be imagined or evaluated internally [31–33]. By contrast, model-free RL typically learns a policy, value function, or both directly from interaction data, without requiring an explicit predictive model of the environment [42–44]. In this sense, world models emphasize learning how the environment evolves, whereas model-free methods emphasize learning which action maximizes return. 

This difference naturally induces a second distinction: _planning versus direct policy execution_ . Learned world models can be rolled forward to support online planning or latent imagination. PlaNet performs online planning in latent space, PETS uses learned dynamics for model-predictive control, Dreamer improves behavior by imagining trajectories in a learned latent model, and TDMPC combines a latent dynamics model with trajectory optimization at decision time [31, 32, 45, 46]. In contrast, canonical model-free methods such as DQN, PPO, and SAC typically act through a direct forward pass of a learned policy or value-based decision rule rather than explicit search through hypothetical futures [42–44]. 

A third distinction concerns _sample efficiency_ . A recurrent motivation for world-model approaches is that a learned dynamics model allows the agent to reuse real experience more effectively through prediction, imagination, or planning. PILCO is a classic example of extreme data efficiency in model-based control, while PETS, MBPO, and Dreamer show that learned models can substantially improve performance per real environment step in modern continuous-control and visual-control settings [32, 45, 47, 48]. Model-free methods, by construction, do not exploit an explicit learned simulator in this way; instead, they improve policies or value functions from real or replayed transitions alone [42–44]. 

However, the advantages of world models come with a characteristic liability: _model bias_ . If the learned dynamics are inaccurate, long imagined rollouts can drift away from the true environment and induce the policy to exploit modeling errors. PILCO explicitly frames model bias as a central problem and addresses it with probabilistic dynamics and uncertainty-aware planning, while MBPO shows that short branched rollouts can reduce the harmful effects of model exploitation in practice [47, 48]. Model-free RL avoids this particular failure mode because it does not rely on explicit multistep predictions of environment dynamics, although it sacrifices some of the structural leverage available to model-based systems [42, 44]. 

13 

The two paradigms also differ in _representation learning_ . In modern world-model architectures, latent states are trained not only to support action selection but also to summarize the hidden dynamics of the environment over time. World Models, PlaNet, and Dreamer all rely on compact latent representations that support prediction and imagination, rather than purely reactive control [31–33]. By contrast, in standard model-free RL, learned representations are typically optimized only insofar as they improve policy or value estimation for the current task [42–44]. This difference often makes world-model representations more naturally reusable for downstream planning or adaptation. 

This distinction becomes especially important for _generalization and transfer_ . DARLA showed that disentangled representations can improve zero-shot transfer in RL, while Schema Networks demonstrated that a generative, causal model of environment dynamics can enable stronger transfer and combinatorial generalization than reactive baselines on structured tasks [49, 50]. More broadly, a learned world model can in principle be paired with new rewards, goals, or planners without discarding all previously acquired knowledge of environment dynamics. Model-free policies, in contrast, are typically more tightly coupled to the reward structure under which they were trained [42, 43]. 

Another key difference is support for _counterfactual and hypothetical reasoning_ . Because world models specify how the world would evolve under alternative actions, they naturally support “what if” analysis. Woulda, Coulda, Shoulda formalized this idea by using structural causal models for counterfactual policy search from logged experience, and Schema Networks likewise emphasized generative causal structure for reasoning about unseen situations [50, 51]. Standard model-free RL does not natively provide an explicit simulator for evaluating alternate futures; any such reasoning must be added externally or approximated indirectly through value estimation [42, 43]. 

World models can also offer greater _transparency of internal predictions_ . In World Models and Dreamer, researchers can inspect reconstructions, latent rollouts, or imagined trajectories, while Schema Networks exposes an explicitly structured generative model of object interactions and consequences [32, 33, 50]. Model-free policies such as DQN or SAC, by contrast, usually encode their knowledge more implicitly in policy and value parameters, which can make post hoc interpretation harder [42, 44]. 

A further distinction concerns _uncertainty_ . PETS uses probabilistic ensembles to capture uncertainty in learned dynamics, and PILCO models uncertainty directly through Gaussian process dynamics; more generally, approximate Bayesian techniques such as Monte Carlo dropout provide a practical route for predictive uncertainty estimation in deep models [45, 47, 52]. Model-free RL can also reason about uncertainty, but typically through uncertainty in value estimation rather than explicit uncertainty over future world trajectories; examples include Bootstrapped DQN for deep exploration and distributional RL for learning return distributions [53, 54]. Thus, uncertainty in world models is often tied more directly to forecasting and planning. 

Despite these contrasts, the boundary between world models and model-free RL is not absolute. Many strong modern agents are hybrid. Dreamer combines a learned world model with actor-critic learning in latent imagination, MBPO uses a learned model to supply synthetic data to an off-policy learner, TD-MPC combines latent dynamics with value learning for control, and SPR shows how predictive latent objectives can substantially improve otherwise model-free agents [32, 46, 48, 55]. The modern landscape is therefore better viewed as a continuum: world-model approaches place prediction and internal simulation at the center of control, whereas model-free methods place direct return optimization at the center. 

In summary, the fundamental distinction is that world models learn an internal predictive account of the environment and use it for imagination, planning, or reasoning, whereas model-free RL learns to act effectively without requiring explicit environmental simulation. This difference 

14 

propagates into downstream properties including planning ability, sample efficiency, vulnerability to model bias, transfer potential, counterfactual reasoning, and uncertainty handling [32, 33, 41, 42]. 

### **2.4 Role of latent spaces in world models** 

A defining design choice in modern world models is whether future predictions are made in the _observation space_ (e.g., raw pixels) or in a learned _latent space_ . Most successful world models operate in latent space, and this design choice has major implications for predictive accuracy, computational efficiency, and downstream task performance. 

**Motivation for latent prediction.** Raw observations in real-world are high-dimensional and contain substantial task-irrelevant information. A 64 _×_ 64 RGB image has 12,288 dimensions; a 256 _×_ 256 image has 196,608. Predicting every pixel of every future frame is computationally expensive and forces the model to allocate capacity to visually complex but decision-irrelevant details (e.g., exact textures, lighting variations). Latent space prediction compresses observations into a compact representation _zt_ that retains decision-relevant information while discarding perceptual noise, reducing the dimensionality by orders of magnitude (e.g., from 12,288 to 32–256 dimensions in typical implementations). 

**Motivation for latent prediction.** Real-world observations are typically high-dimensional and contain substantial information that is irrelevant to decision-making. For example, a 64 _×_ 64 RGB image contains 12,288 dimensions, whereas a 256 _×_ 256 RGB image contains 196,608. Predicting every pixel of future frames is therefore computationally expensive and forces the model to devote representational capacity to visually complex but task-irrelevant details, such as textures or lighting variations. By contrast, latent-space prediction compresses observations into a compact representation, _zt_ that preserves decision-relevant information while filtering out perceptual noise, often reducing dimensionality by several orders of magnitude (e.g., from 12,288 dimensions to 32– 256 in typical implementations). 

**Deterministic vs. stochastic latent spaces.** Early world models used deterministic encoders, but stochastic environments demand stochastic latent representations that capture aleatoric uncertainty. Ha and Schmidhuber [4] used a VAE with a Gaussian latent space, where the stochasticity of the latent code captures the inherent unpredictability of the environment. The RSSM [31] introduced a hybrid design: a deterministic recurrent state _ht_ that preserves temporal memory, combined with a stochastic component _zt_ sampled from a learned prior or posterior distribution. This dual structure has been adopted by the entire Dreamer line and many subsequent models. DreamerV2 [34] further demonstrated that _discrete_ categorical latent variables (32 categorical distributions with 32 classes each, yielding a 32<sup>32</sup> representational capacity) outperform continuous Gaussian latents on Atari games, likely because discrete representations better capture the discrete nature of game state transitions. 

**Deterministic versus stochastic latent spaces.** Early world models often relied on deterministic encoders, but stochastic environments require representations that can capture aleatoric uncertainty. Ha and Schmidhuber [4], for example, used a VAE with a Gaussian latent space, in which the stochastic latent code reflects the inherent unpredictability of the environment. The RSSM [31] introduced a hybrid formulation consisting of a deterministic recurrent state, _ht_ that preserves temporal memory, together with a stochastic component, _zt_ sampled from a learned prior or posterior distribution. This dual-state design has since become standard in the Dreamer family and many subsequent world models. DreamerV2 [34] further showed that _discrete_ categorical latent variables can outperform continuous Gaussian latents on Atari benchmarks, likely because discrete representations better align with the discrete transition structure of many game environments. 

**Continuous versus discrete tokenization.** An alternative to continuous latent spaces is 

15 

discrete tokenization, in which observations are mapped to a finite vocabulary of learned codes. IRIS [35], for instance, uses a VQ-VAE [56] tokenizer to transform image frames into discrete tokens and then models dynamics through next-token prediction with a transformer. This formulation creates a close parallel to language modeling and allows training with categorical cross-entropy objectives. STORM [36] adopts a hybrid strategy by combining stochastic continuous latents with transformer-based dynamics, thereby occupying an intermediate position between continuous and fully discrete approaches. 

**Prediction in representation space (JEPA).** LeCun [5] proposed the Joint-Embedding Predictive Architecture (JEPA) as a principled alternative to both pixel-space prediction and reconstruction-based latent modeling. In JEPA, the model predicts the representation of a future observation directly in embedding space rather than reconstructing the observation itself, and no decoder is required. This formulation avoids the bottleneck of pixel reconstruction, which often penalizes errors in task-irrelevant details, as well as the mode-averaging effects associated with pixel-wise losses. I-JEPA [39] validated this approach for image representation learning, while V- JEPA [57] and V-JEPA 2 [58] extended it to video, demonstrating strong performance in large-scale video understanding and zero-shot robotic planning. 

**Latent-space structure and downstream performance.** The structure of the latent space directly influences the quality of imagined rollouts and, consequently, the effectiveness of policies trained on imagined trajectories. If the latent space fails to encode decision-relevant factors, such as object positions, velocities, or contact dynamics, then even an accurate dynamics model will generate uninformative predictions. Conversely, an overly detailed latent space that attempts to preserve every perceptual feature may waste capacity on irrelevant variation. The success of MuZero [38], which learns a latent representation optimized solely for reward and value prediction without any reconstruction objective, illustrates that task-aligned latent spaces can outperform reconstructionbased alternatives. DreamerV3 [40] further highlights the importance of carefully structured latent representations by using symlog transformations and categorical value distributions to maintain calibration across domains with highly variable reward scales. 

Despite the success of latent world models, several open challenges remain, including: (1) _latentspace collapse_ , where distinct observations are mapped to identical codes and critical information is lost; (2) _representation drift_ , where the latent space shifts within training and undermines the consistency of imagined data; (3) _disentanglement_ , namely, learning latent dimensions that correspond to interpretable physical factors; and (4) _scalability_ , that is, designing latent spaces that remain both compact and expressive as environmental complexity increases. 

## **3 Categorization of World Models by Architecture** 

World model architectures can be analyzed along several complementary axes, each reflecting a key design dimension of how the model encodes observations, represents dynamics, handles uncertainty, and supports downstream decision-making. In brief, these axes provide a structured framework for comparing existing approaches and understanding the trade-offs among different architectural choices. World model architectures can be categorized along several complementary axes described below: 

### **3.1 Classification by representation** 

The choice of how to represent environment states is a fundamental design decision that determines what information the world model retains, how tractable multi-step prediction is, and what downstream tasks the model can support. We identify six principal representation families. 

16 

#### **3.1.1 Observation-space (pixel-level) representations.** 

The most direct approach predicts future observations in raw observation space—typically RGB pixels or LiDAR point clouds. Early video prediction models [59, 60] operated in pixel space, as do recent diffusion-based world models such as DIAMOND [37] and GameNGen [61]. The advantage is that no information is discarded: every visual detail is available for downstream use. The disadvantages are high dimensionality (a 256 _×_ 256 RGB frame has 196,608 dimensions), allocation of model capacity to decision-irrelevant details (textures, lighting), and the computational cost of multi-step prediction. Pixel-space models are most appropriate when visual fidelity is itself the objective, as in video generation or game simulation. 

#### **3.1.2 Continuous latent representations.** 

Most successful world models compress observations into continuous latent vectors via a learned encoder, then predict dynamics in this compact space. Ha and Schmidhuber [4] used a VAE to compress 64 _×_ 64 frames into 32-dimensional Gaussian latent codes. The RSSM [31] introduced a hybrid continuous latent state comprising a deterministic recurrent component _ht_ (preserving temporal memory through GRU updates) and a stochastic component _zt_ (sampled from a learned Gaussian distribution to capture environmental uncertainty): 


This deterministic-stochastic split has been adopted across the entire Dreamer line [32, 40] and many subsequent models (STORM [36]). Continuous latent spaces offer principled uncertainty quantification through the stochastic component and are well-suited for continuous control domains where smooth interpolation between states is meaningful. Their limitation is the tendency toward blurry reconstructions when a pixel-wise decoder is used, due to the Gaussian likelihood assumption. 

#### **3.1.3 Discrete token representations.** 

An alternative is to quantize observations into a finite vocabulary of discrete codes, typically via a VQ-VAE [56] tokenizer. IRIS [35] converts each image frame into a sequence of discrete tokens, then treats dynamics as next-token prediction—drawing a direct parallel with language modeling. DreamerV2 [34] demonstrated that discrete categorical latent variables (32 categorical distributions with 32 classes each) outperform continuous Gaussian latents on Atari games, likely because discrete representations better capture the discrete nature of game state transitions. GAIA-1 [62] extends this approach to driving, tokenizing video frames and predicting future tokens autoregressively with a 9-billion-parameter transformer. Discrete representations enable the use of powerful autoregressive transformer architectures with categorical cross-entropy training, but sacrifice fine-grained spatial detail due to the quantization bottleneck. 

#### **3.1.4 Joint-embedding (representation-space) predictions.** 

LeCun [5] proposed the Joint-Embedding Predictive Architecture (JEPA) as a principled alternative that avoids both pixel-space reconstruction and explicit tokenization. In JEPA, a predictor network maps the embedding of the current observation to the embedding of the next observation, with the target embeddings produced by an exponential moving average (EMA) encoder: 


17 

No decoder is used; the loss operates entirely in representation space. This avoids the pixelreconstruction bottleneck (which penalizes models for failing to predict decision-irrelevant details) and the mode-averaging inherent in pixel-wise losses. I-JEPA [39] validated this for images. V- JEPA [57] extended it to video, and V-JEPA 2 [58]—pretrained on over one million hours of internet video—achieved state-of-the-art video understanding and enabled zero-shot robot planning. MuZero [38] can also be viewed as operating in a task-aligned representation space, since its latent dynamics are optimized solely for reward and value prediction without any reconstruction objective. 

#### **3.1.5 Structured and object-centric representations.** 

Rather than treating the world state as a monolithic vector or token sequence, object-centric models decompose it into a set of _slots_ , each representing a distinct entity with its own properties: 


Kipf et al. [63] introduced the Contrastive Structured World Model (C-SWM), which learns objectcentric representations via contrastive learning and models dynamics through a graph neural network over object slots. RoboDreamer [64] decomposes language instructions into primitive components and uses compositional diffusion models conditioned on each. DreMa [65] integrates Gaussian Splatting with physics simulators for object-level scene manipulation. Object-centric representations support combinatorial generalization to novel object configurations and are more interpretable, but they scale poorly with the number of objects ( _O_ ( _N_<sup>2</sup> ) for pairwise interaction modeling) and assume that the environment can be cleanly decomposed into discrete entities. 

#### **3.1.6 3D and occupancy-based representations.** 

For domains with rich spatial structure, world models can represent the environment as 3D occupancy grids, voxels, or point clouds. OccWorld [66] uses a GPT-like model to autoregressively predict future 3D occupancy tokens for autonomous driving, enabling spatially consistent scene forecasting. Copilot4D [67] learns to forecast LiDAR point clouds via discrete diffusion, achieving over 65% reduction in Chamfer distance for 1-second prediction. Kong et al. [68] surveyed 3D and 4D world modeling approaches, establishing taxonomies across video-based, occupancy-based, and LiDAR-based generation. These representations are particularly valuable for autonomous driving and robotics, where 3D spatial reasoning is essential for safe planning, but they incur substantial memory and compute costs that scale cubically with spatial resolution. 

### **3.2 Classification by dynamics** 

A fundamental dimension for understanding world models lies in how they represent and learn _dynamics_ , i.e., the temporal evolution of latent states. Rather than focusing on architectural components, this perspective categorizes models based on the form of the transition mechanism, typically expressed as _p_ ( _st_ +1 _| st, at_ ). This viewpoint is particularly relevant for domains such as healthcare, where dynamics correspond to disease progression, treatment response, and longitudinal physiological changes. 

In the following, we categorize world models according to their formulation of dynamics, ranging from explicit parametric transitions to implicit generative processes and adaptive memory-based mechanisms. 

18 

#### **3.2.1 Deterministic Dynamics** 

Deterministic dynamics models assume that the next state is a single-valued function of the current state, i.e., _st_ +1 = _fθ_ ( _st, at_ ). This formulation simplifies learning and enables efficient multi-step rollout in latent space. Early world models such as World Models [33] and PlaNet [31] adopt this paradigm, using recurrent networks to propagate latent states. Subsequent works such as Dreamer [32] further demonstrate that deterministic latent dynamics can support long-horizon imagination and policy optimization. 

However, deterministic formulations inherently struggle to capture multi-modal futures and uncertainty, often leading to averaged or overconfident predictions. This limitation is particularly problematic in medical applications, where disease trajectories exhibit significant inter-patient variability. 

#### **3.2.2 Stochastic Dynamics** 

To address the limitations of deterministic transitions, stochastic dynamics models introduce latent variables to represent uncertainty, modeling transitions as distributions rather than point estimates. 

In practice, this is often implemented through variational state-space models, where latent stochastic variables capture unobserved factors influencing temporal evolution. Modern latent world models, including extensions of PlaNet and Dreamer, incorporate stochastic components to improve expressivity while retaining stable temporal structure. 

Stochastic dynamics are especially important in medical settings, where uncertainty arises from both measurement noise and intrinsic biological variability. Such models enable the representation of multiple plausible disease trajectories and support probabilistic reasoning in downstream tasks. 

#### **3.2.3 Implicit Generative Dynamics** 

An alternative formulation models dynamics implicitly through generative processes, without explicitly parameterizing transition functions. Diffusion-based models represent a prominent example, where temporal evolution is captured through iterative denoising processes over entire trajectories. 

This paradigm has recently been extended to medical world modeling. MRI Contrast Enhancement Kinetics World Model (CEKWorld) [69] formulates contrast-agent dynamics as a continuoustime generative process conditioned on non-contrast MRI. By leveraging latent diffusion, it synthesizes temporally dense sequences from sparsely sampled clinical data. To address the challenges of low temporal resolution, the model introduces spatiotemporal consistency constraints in latent space, mitigating content distortion and temporal discontinuity observed in sparse training regimes [69]. 

Implicit generative dynamics provide strong flexibility and expressivity, making them well-suited for modeling complex biological processes. However, their lack of explicit transition structure can limit interpretability and complicate integration with decision-making frameworks. 

#### **3.2.4 Representation-space Predictive Dynamics** 

Recent work explores modeling dynamics directly in representation space, focusing on predicting future latent embeddings rather than reconstructing observations. This paradigm is closely related to joint-embedding predictive architectures (JEPA), where the objective is to learn invariant and predictive representations. 

LeWorldModel [70] adopts this approach by learning end-to-end predictive embeddings from pixel inputs, improving stability and scalability by avoiding explicit reconstruction. Similarly, 

19 

Brain-JEPA [71] extends this paradigm to neural data, modeling brain dynamics from fMRI signals using spatiotemporal masking and gradient-based target positioning. 

In this formulation, dynamics are defined as transformations in representation space, capturing essential temporal structure while discarding irrelevant details. This abstraction is particularly advantageous for high-dimensional data such as brain imaging, where direct pixel-level modeling is both inefficient and unnecessary. 

#### **3.2.5 Memory-Augmented Dynamics** 

A more recent direction extends dynamics modeling with external memory, allowing transitions to be conditioned on retrieved past experiences. In this formulation, dynamics are no longer purely parametric but depend on both learned representations and an external memory module. 

CLARITY [72] exemplifies this paradigm by modeling context-aware disease trajectories in latent space. By incorporating patient-specific information and historical cases, the model dynamically adapts its predictions, enabling personalized forecasting of disease progression and treatment outcomes. 

More broadly, medical world model frameworks [73] emphasize the importance of incorporating domain knowledge and patient-specific context into dynamics modeling. Such approaches are particularly effective under distribution shift, where purely parametric models may fail to generalize across populations or institutions. 

Memory-augmented dynamics thus provide a mechanism for bridging global knowledge and local adaptation, a property that is essential for real-world deployment in healthcare settings. 

#### **3.2.6 Discussion and Open Challenges** 

The classification above highlights a spectrum of dynamics formulations, ranging from explicit deterministic transitions to implicit generative processes and adaptive memory-based systems. These approaches reflect different trade-offs between efficiency, expressivity, interpretability, and adaptability. 

Despite significant progress, several open challenges remain. First, accurately modeling longterm dynamics under sparse and irregular observations remains difficult, particularly in medical domains where data acquisition is constrained. Second, balancing expressivity and interpretability is an ongoing challenge, as highly flexible generative models often lack clear physical or clinical meaning. Third, robustness under distribution shift continues to be a major concern, motivating the integration of memory and test-time adaptation mechanisms. 

Finally, a promising direction lies in hybrid models that combine stochastic dynamics, implicit generative modeling, and memory augmentation. Such systems may offer a unified framework capable of capturing complex temporal processes while remaining adaptable to real-world variability. 

### **3.3 Classification by Modality** 

The modality of input data constitutes a fundamental axis along which world models diverge in design, capability, and applicability. Since world models must internalize the dynamics of the environments they represent, the sensory channels through which environmental information is perceived directly shape both the learned representations and the downstream utility of the model. We organize existing world models into five broad modality categories: _visual-only_ , _language-only_ , _3D geometric_ , _proprioceptive and tactile_ , and _multimodal fusion_ . Table 1 summarizes representative works along this taxonomy. 

20 

Table 1: Representative world models classified by input modality. 

|**Model**|**Visual**|**Language**|**LiDAR/3D**|**Proprioceptive**|**Tactile**|**Audio**|
|---|---|---|---|---|---|---|
|**_Visual-only_**|||||||
|Dreamer (v1–v3) [6–8]|✓||||||
|IRIS [74]|✓||||||
|DIAMOND [75]|✓||||||
|GameNGen [76]|✓||||||
|Sora [10]|✓||||||
|Genie / Genie 2 [13]|✓||||||
|**_Language-only_**|||||||
|RAP [77]||✓|||||
|WebDreamer [78]||✓|||||
|WorldLLM [79]||✓|||||
|**_3D Geometric (LiDAR /_**|**_Point _**|**_Cloud / Oc_**|**_cupancy)_**||||
|LiDARGen [80]|||✓||||
|LidarDM [81]|||✓||||
|OccWorld [82]|||✓||||
|**_Proprioceptive and Tacti_**|**_le_**||||||
|DayDreamer [83]|✓|||✓|||
|MLA [84]|✓|✓|✓||✓||
|Tactile-VLA [85]|✓|✓|||✓||
|**_Multimodal Fusion_**|||||||
|GAIA-1 / GAIA-2 [86, 87]|✓|✓|||||
|Cosmos [14]|✓|✓|||||
|V-JEPA 2 [12]|✓|||✓|||
|UniSim [88]|✓||✓||||
|VLWM [89]|✓|✓|||||


#### **3.3.1 Visual-Only World Models** 

The most extensively studied category of world models operates on visual observations, typically in the form of RGB images or video frames. This design choice is natural: vision provides a highbandwidth, information-rich channel that captures spatial layout, object appearance, and temporal dynamics simultaneously. Pioneering work in model-based reinforcement learning established this paradigm. Ha and Schmidhuber [4] trained a variational autoencoder (VAE) and a recurrent neural network (RNN) on image observations to learn compact latent representations of visual environments, enabling agents to act within internally generated “dreams.” The Dreamer series [6–8] extended this approach through the Recurrent State-Space Model (RSSM), learning visual dynamics in a compact latent space and training policies entirely through imagined rollouts. More recently, DreamerV3 [8] demonstrated that a single, fixed configuration can master over 150 diverse tasks spanning continuous control, Atari games, and even Minecraft, establishing visual world models as general-purpose decision-making substrates. 

An important architectural shift has been the adoption of transformer-based and diffusion-based 

21 

dynamics models operating on visual tokens. IRIS [74] discretizes visual observations using a VQVAE and models dynamics with an autoregressive transformer, achieving competitive performance on the Atari 100k benchmark. DIAMOND [75] replaces the autoregressive transition model with a diffusion process, generating the next observation conditioned on past frames and actions. This diffusion-based paradigm has been pushed further by GameNGen [76], which demonstrated realtime interactive simulation of the classic game DOOM at over 20 frames per second using a finetuned Stable Diffusion model, achieving visual fidelity nearly indistinguishable from the actual game by human raters. 

At the foundation model scale, video generation has been reframed as a form of world simulation. OpenAI’s Sora [10] demonstrated that scaling video diffusion transformers trained on diverse internet video can produce temporally coherent visual sequences that appear to respect physical constraints such as object permanence and rigid-body dynamics, although the extent to which such models constitute genuine world models remains debated [11]. DeepMind’s Genie [13] took a complementary approach, learning a latent action space from unlabeled video in a self-supervised manner, enabling the generation of interactive and controllable 2D environments from single image prompts. 

Despite their success, visual-only world models face inherent limitations. Raw pixel reconstruction is computationally expensive and may force models to allocate representational capacity to task-irrelevant visual details such as textures and lighting variations. Moreover, purely visual representations lack the semantic abstraction needed for high-level reasoning and struggle to capture aspects of the world state that are not directly observable in the image, such as object masses, material properties, or off-screen entities. 

#### **3.3.2 Language-Only World Models** 

A distinct but increasingly influential line of research employs natural language as the primary representational medium for world modeling. Rather than predicting future pixel values, languageonly world models predict future _states_ expressed as textual descriptions, leveraging the semantic abstraction and compositional structure inherent in natural language. This paradigm capitalizes on the extensive world knowledge already encoded in large language models (LLMs) through pretraining on internet-scale text corpora. 

Hao et al. [77] proposed the Reasoning via Planning (RAP) framework, which repurposes an LLM to serve simultaneously as a world model—predicting state transitions—and as a reasoning agent, combined with Monte Carlo Tree Search for strategic exploration of the reasoning space. Notably, RAP on LLaMA-33B surpassed chain-of-thought prompting on GPT-4 in plan generation tasks, demonstrating that LLMs can serve as effective approximate world models when coupled with principled planning algorithms. In a similar spirit, WebDreamer [78] treats LLMs as world models for web-based environments, simulating the outcomes of candidate browser actions in natural language before committing to one, achieving substantial improvements over reactive baselines on benchmarks such as VisualWebArena. 

Language-based world models offer several attractive properties. Natural language provides a semantically rich and human-interpretable interface, enabling straightforward inspection of predicted world states and facilitating human-in-the-loop correction. Furthermore, language-based predictions are computationally far less expensive to generate than pixel-level reconstructions, making them particularly suitable for high-level task planning over long horizons. Recent work on WorldLLM [79] induces explicit natural-language hypotheses about transition regularities via Bayesian inference over agent experience, yielding an interpretable and low-dimensional world model that guides both forward prediction and curiosity-driven exploration. 

22 

However, language-only world models suffer from significant limitations. Textual descriptions are inherently lossy: they cannot capture fine-grained spatial relationships, continuous dynamics, or precise metric information. LLM-based world models also exhibit compounding prediction errors over long horizons, with accuracy degrading substantially as rollout length increases [78]. Additionally, these models inherit the well-documented limitations of LLMs, including hallucination, difficulty with precise numerical reasoning, and fragile performance on tasks requiring grounded physical understanding. 

#### **3.3.3 3D Geometric World Models** 

A third category of world models operates on three-dimensional geometric representations, including LiDAR point clouds, occupancy grids, and depth maps. These representations provide explicit 3D structural information that is complementary to the appearance-centric nature of RGB imagery and is especially critical for applications in autonomous driving and outdoor robotics where precise spatial reasoning is required. 

LiDAR-based world modeling has advanced rapidly in recent years. LiDARGen [80] formulated point cloud generation as a denoising diffusion process in an equirectangular projection, producing physically plausible LiDAR scans that can be conditionally sampled for tasks such as point cloud densification without retraining. Subsequent diffusion-based approaches, including R2DM [90] and RangeLDM [91], improved fidelity and scalability by operating in latent range-view spaces. LidarDM [81] further demonstrated compositional scene generation, synthesizing LiDAR data within realistic driving environments. Beyond generation, occupancy-based world models such as OccWorld [82] predict future 3D occupancy states of a scene, providing a structured volumetric representation that unifies spatial prediction across both static and dynamic elements. 

3D geometric world models are particularly valuable for autonomous driving, where a comprehensive survey of driving-specific approaches can be found in [27, 29]. These models can faithfully represent the geometry of roads, buildings, and vehicles, capturing information that is absent from monocular camera images. However, they typically lack semantic richness—a LiDAR point cloud encodes _where_ objects are but not necessarily _what_ they are or how they will behave—motivating the integration of 3D geometric data with other modalities. 

#### **3.3.4 Proprioceptive and Tactile World Models** 

Embodied agents, particularly robots, interact with their environments through sensory channels that extend well beyond vision. Proprioceptive signals—such as joint positions, velocities, and torques—provide direct information about the agent’s own body state, while tactile sensors convey contact forces and surface properties during physical interaction. Incorporating these modalities into world models is essential for contact-rich manipulation tasks where visual observation alone is insufficient. 

DayDreamer [83] demonstrated that Dreamer-style world models can be applied to physical robots by learning dynamics from a combination of visual observations and proprioceptive inputs, enabling a quadruped robot to learn locomotion gaits entirely from real-world interaction without simulation. Several recent works have further expanded the sensory repertoire. The Multisensory Language-Action (MLA) model [84] proposes an encoder-free multimodal alignment scheme that repurposes the LLM backbone itself as a perception module, directly interpreting 2D images, 3D point clouds, and tactile tokens through positional correspondence. Similarly, Tactile-VLA [85] and BiTLA [92] integrate tactile feedback with vision-language-action architectures, demonstrating improvements on contact-rich manipulation benchmarks. 

23 

The inclusion of proprioceptive and tactile modalities addresses a fundamental blind spot of vision-only approaches: the physics of contact. A robot grasping a fragile object must sense grip force in real time; a hand manipulating a deformable object must feel how the material yields. These signals are inherently low-dimensional compared to vision but carry information that is impossible to obtain from cameras alone. The challenge lies in the heterogeneity of these sensor modalities—tactile readings, joint encoders, and force-torque sensors each operate at different frequencies, dimensionalities, and noise characteristics—requiring careful architectural design for effective fusion. 

#### **3.3.5 Multimodal Fusion World Models** 

Perhaps the most ambitious and rapidly growing category encompasses world models that jointly process multiple input modalities, seeking to construct richer and more robust internal representations of the world by leveraging the complementary strengths of different sensory channels. The intuition is straightforward: the physical world is inherently multimodal, and an agent that can simultaneously process visual appearance, linguistic context, geometric structure, and physical feedback should develop a more complete understanding of environmental dynamics than one relying on any single channel. 

In autonomous driving, GAIA-1 [86] demonstrated a multimodal world model that conditions video generation on text descriptions and structured control inputs, enabling controllable synthesis of driving scenarios. Its successor, GAIA-2 [87], further advanced controllability through multi-view latent diffusion with fine-grained scene-level conditioning. UniSim [88] takes a different approach, constructing neural feature grids from recorded driving logs to simultaneously simulate both camera and LiDAR data in a closed-loop fashion, enabling the first closed-loop evaluation of autonomy systems on counterfactual safety-critical scenarios. 

At the foundation model scale, NVIDIA’s Cosmos [14] provides a platform for training world foundation models that ingest video and text to produce generative simulators for physical AI applications. Meta’s V-JEPA 2 [12], a 1.2 billion-parameter model trained via self-supervised video prediction using the Joint-Embedding Predictive Architecture (JEPA), achieves state-ofthe-art performance on visual understanding benchmarks while simultaneously enabling zero-shot robot planning by integrating visual predictions with proprioceptive inputs. This model exemplifies LeCun’s [5] vision of a non-generative world model that predicts in abstract representation space rather than reconstructing raw pixels, avoiding the computational burden and representational waste of pixel-level generation. 

A particularly notable recent development is the Vision-Language World Model (VLWM) [89], which perceives the environment through visual observations but predicts world evolution using language-based abstraction. By compressing video inputs into hierarchical text descriptions (termed “Tree of Captions”) and training a language model to predict action-state trajectories, VLWM achieves strong performance on high-level task planning benchmarks while maintaining full interpretability of the predicted world states. This approach bridges the visual and language modalities in a complementary fashion: vision handles low-level perception while language carries the representational burden of dynamics prediction. 

The key architectural challenge in multimodal world models lies in the fusion mechanism. Early approaches typically employ modality-specific encoders followed by concatenation or cross-attention in a shared latent space [93]. More recent designs explore tighter integration strategies, such as the Global Workspace approach [94], which draws inspiration from cognitive neuroscience’s Global Workspace Theory to learn a shared bottleneck representation across modalities, allowing each sensory channel to inform the world model while maintaining modality-specific processing pathways. 

24 

#### **3.3.6 Discussion and Open Challenges** 

The modality landscape of world models reveals several important trends and unresolved tensions. First, there is a clear trajectory toward _modality convergence_ : state-of-the-art systems increasingly combine multiple sensory inputs, mirroring the multimodal nature of biological perception. Second, the choice of _prediction target modality_ is decoupling from the input modality—models may ingest video but predict in language space (VLWM) or ingest images but predict in abstract latent space (V-JEPA 2), suggesting that the optimal representation for world dynamics may not coincide with any raw sensory modality. 

Several open challenges remain. _Scalable multimodal alignment_ across more than two or three modalities remains technically difficult, as the number of pairwise alignment objectives grows quadratically. _Temporal synchronization_ poses practical challenges when fusing modalities that operate at vastly different sampling rates (e.g., 30 Hz cameras, 1 kHz tactile sensors, and 10 Hz LiDAR). _Missing modality robustness_ —the ability of a world model to degrade gracefully when one or more sensory channels are unavailable—has received little attention but is critical for realworld deployment. Finally, the question of _optimal prediction modality_ remains open: it is not yet clear whether world models should predict in pixel space, language space, latent embedding space, or some hybrid thereof, as each choice entails distinct trade-offs among fidelity, interpretability, computational cost, and downstream task utility. 

### **3.4 Classification by learning paradigms** 

The learning paradigm— _how_ a world model acquires knowledge of environmental dynamics constitutes a fundamental classification axis that is orthogonal to representation type (Section 3.1), dynamics architecture (Section 3.2), and input modality (Section 3.3). The same architectural backbone, such as the RSSM underlying the Dreamer family, can be trained through online reinforcement learning [6], offline batch learning, or large-scale self-supervised pretraining, yielding models with markedly different data requirements, generalization capabilities, and deployment characteristics. This section organizes existing world models into six broad learning-paradigm categories—selfsupervised and unsupervised learning, online model-based reinforcement learning, offline and batch learning, foundation model pretraining and adaptation, supervised and imitation learning, and hybrid multi-stage paradigms—and analyzes the trade-offs each entails. Table 2 provides a summary of representative models classified along this axis. 

#### **3.4.1 Self-Supervised and Unsupervised Learning** 

The dominant learning paradigm for modern world models is self-supervised learning (SSL), in which models learn compact spatiotemporal representations from raw, unlabeled observations by optimizing pretext objectives that exploit the inherent structure of sensory data. This paradigm eliminates the need for reward signals or ground-truth labels, enabling training on large-scale datasets collected without task-specific annotation. 

**Reconstruction-based self-supervision.** The earliest and most widely adopted SSL strategy for world models is learning through observation reconstruction. Ha and Schmidhuber [4] pioneered this approach by training a VAE in an unsupervised manner to compress image observations into compact latent vectors, paired with an RNN that predicted future latent distributions. The entire world model was learned without any task reward, relying solely on the reconstruction objective of the VAE and the predictive loss of the RNN. The Dreamer series [6–8] extended this paradigm through the RSSM, where the world model is trained to reconstruct observations, predict rewards, 

25 

and predict episode terminations from latent states. A critical finding from DreamerV3 [8] is that the world model’s representations are predominantly shaped by its _task-agnostic reconstruction objective_ rather than by task-specific reward gradients, suggesting that unsupervised dynamics learning provides the primary representational substrate upon which task-specific signals merely fine-tune behavior. 

Reconstruction-based self-supervision also underlies video prediction approaches. Stochastic video prediction models such as SV2P [59] and SVG [60] learn to predict future video frames by introducing variational latent variables to capture the inherent uncertainty of future outcomes. More recently, diffusion-based world models—including DIAMOND [37] and GameNGen [61]—reformulate next-observation prediction as a denoising process, where the model learns to reverse a gradual noise-corruption procedure. The denoising score-matching objective is itself a form of self-supervision: no labels are required beyond the observations themselves. 

While reconstruction-based approaches have proven remarkably effective, they carry a fundamental limitation: pixel-level reconstruction forces models to allocate representational capacity to task-irrelevant visual details such as textures, lighting variations, and background clutter, potentially at the expense of capturing decision-relevant dynamics. 

**Contrastive and non-contrastive representation learning.** An alternative SSL strategy avoids pixel-level reconstruction entirely, instead learning structured representations through contrastive or non-contrastive objectives. Contrastive Structured World Models (C-SWM) [63] learn object-centric state representations by contrasting temporally adjacent state-transition pairs against randomly sampled negatives, yielding physically meaningful latent spaces that support accurate multi-step prediction without any reconstruction decoder. Self-Predictive Representations (SPR) [95] encourage task-relevant latent consistency by training representations to predict their own future latent states under a learned transition model, achieving substantial improvements in data efficiency on the Atari 100k benchmark. 

Non-contrastive methods, which avoid the need for explicit negative samples, have also gained traction. Approaches inspired by BYOL [96] and VICReg [97] learn representations by enforcing agreement between different augmented views of the same observation while using regularization mechanisms—such as exponential moving average targets, variance-invariance-covariance constraints, or stop-gradient operations—to prevent representational collapse. DINO-WM [98] builds world dynamics models on compact DINOv2 patch embeddings rather than raw pixels, predicting future patch features from offline behavioral trajectories and enabling zero-shot planning across diverse environments without reward models or expert demonstrations. This demonstrates that pre-trained visual representations encoding rich semantic structure can serve as powerful inductive biases for dynamics learning. 

**Joint-Embedding Predictive Architectures (JEPA).** Perhaps the most theoretically principled SSL paradigm for world modeling is the Joint-Embedding Predictive Architecture (JEPA) proposed by LeCun [5]. Unlike generative approaches that predict raw observations, JEPA learns to predict future _representations_ in a learned latent space, deliberately discarding unpredictable and task-irrelevant perceptual details. This design choice reflects a fundamental insight: the optimal representation for world dynamics may not coincide with any raw sensory modality, and forcing pixel-level prediction wastes model capacity on information that is irrelevant for downstream decision-making. 

I-JEPA [39] instantiated this principle for static images, predicting the representations of masked image regions from visible context entirely in latent space, and achieving competitive performance 

26 

with substantially higher computational efficiency than both masked autoencoder and contrastive baselines. V-JEPA [57] extended this to the temporal domain by predicting masked spatiotemporal regions in video, learning motion-sensitive representations without pixel reconstruction. V-JEPA 2 [12], pretrained on over one million hours of internet video, demonstrated that scaling JEPA pretraining yields video representations with state-of-the-art understanding and prediction capabilities—achieving 77.3% top-1 accuracy on Something-Something v2 for motion understanding and 39.7 recall-at-5 on Epic-Kitchens-100 for action anticipation. Critically, V-JEPA 2 can be post-trained into an action-conditioned world model (V-JEPA 2-AC) using fewer than 62 hours of unlabeled robot video, enabling zero-shot robotic planning on physical Franka arms without any task-specific training or reward. The JEPA paradigm thus represents a shift from “generative” to “predictive” self-supervised learning, where the model learns what aspects of the future are predictable and relevant rather than attempting to reconstruct every detail. 

#### **3.4.2 Online Model-Based Reinforcement Learning** 

In online model-based reinforcement learning (MBRL), the world model is learned concurrently with the agent’s policy through iterative interaction with the environment. The agent alternates between collecting real experience, updating its internal model of the environment, and using that model to improve its behavior—either through synthetic data generation or direct planning. 

**Interleaved model learning and data augmentation.** The conceptual roots of this paradigm trace back to Sutton’s Dyna architecture [99], which interleaved real environment interaction with model-based updates by using the learned dynamics to generate synthetic transitions for value function training. In modern MBRL, this strategy has been refined to balance the benefits of modelgenerated data against the risks of compounding model errors. MBPO [48] limits model rollouts to short horizons initiated from real states sampled from a replay buffer, providing a theoretical monotonic improvement guarantee while substantially improving data efficiency. STEVE [100] further explored how uncertainty-aware model rollouts can be incorporated into value estimation, using ensembles to quantify epistemic uncertainty and avoid exploitation of poorly modeled regions. 

**Imagination-based policy learning.** A more ambitious use of online world models places imagined latent trajectories at the center of policy optimization. PlaNet [31] demonstrated that compact latent dynamics models can support planning directly from image observations, achieving 50 _×_ data efficiency improvements over model-free methods using the Cross-Entropy Method for online trajectory optimization. The Dreamer family [6–8] extended this by combining learned latent dynamics with actor-critic learning entirely within imagined rollouts: after fitting a world model from real experience, the agent rolls forward imagined latent trajectories and uses them to train value and policy networks via backpropagation through the differentiable dynamics. Because the transition dynamics are implemented as differentiable neural networks, gradients of long-term value estimates can be propagated through imagined trajectories, effectively transforming imagination into a differentiable computation graph. DayDreamer [83] validated this paradigm on physical robots, demonstrating that a quadruped could learn locomotion gaits entirely from real-world interaction without any simulation. 

**Search-based online reasoning.** An alternative online paradigm performs explicit planning at inference time through search procedures. MuZero [9] learns a latent dynamics model sufficient for predicting only planning-relevant quantities—rewards, values, and policy logits—and combines it with Monte Carlo Tree Search to achieve superhuman performance across Go, chess, shogi, 

27 

and Atari without access to environment rules. This approach embodies the principle of _value equivalence_ [101]: the latent space is shaped to preserve decision-relevant structure rather than to faithfully reconstruct observations. EfficientZero [102] improved data efficiency by incorporating self-supervised consistency objectives, while TD-MPC [46] integrated learned latent dynamics with trajectory optimization for continuous control. Unlike amortized approaches that encode planning into a parametric policy, search-based methods explicitly recompute optimal actions for each state, trading increased computational cost at inference time for improved flexibility and robustness to out-of-distribution states. 

#### **3.4.3 Offline and Batch Learning** 

In safety-critical domains such as healthcare, autonomous driving, and industrial control, online exploration may be prohibitively expensive, dangerous, or ethically impermissible. Offline world model learning addresses this constraint by training entirely from pre-collected, static datasets without any further environment interaction. 

The core challenge in this setting is _distribution shift_ : when the learned world model is used to simulate trajectories beyond the support of the training data, prediction errors can compound rapidly, potentially leading to “model exploitation”—where the policy discovers unrealistically highreward trajectories that exist only as artifacts of model inaccuracies. MOPO [103] addresses this by learning an ensemble of dynamics models and penalizing the policy’s return estimates by the ensemble’s disagreement, providing a conservative lower bound on the true expected return. The Diffusion World Model (DWM) [104] departs from the standard one-step autoregressive paradigm by predicting multi-step future states and rewards concurrently via diffusion, achieving a 44% performance gain over one-step models on D4RL benchmarks. More recently, RLVR-World [105] proposed using reinforcement learning with verifiable rewards as a post-training paradigm for world models, directly optimizing transition prediction metrics rather than maximum likelihood, demonstrating substantial gains across text games, web navigation, and robotic manipulation. 

A critical insight from the offline learning literature is the tension between _predictive accuracy_ and _decision utility_ : a world model that achieves low reconstruction error does not necessarily provide the most useful representation for policy optimization [106]. Models may preserve visually rich but task-irrelevant details while failing to represent reward-critical structure, helping explain why policy performance does not always correlate with prediction quality. This observation has motivated growing interest in _decision-oriented_ world models that are explicitly optimized for downstream control utility. 

#### **3.4.4 Foundation Model Paradigm: Large-Scale Pretraining and Adaptation** 

Inspired by the transformative success of the “pretrain then fine-tune” paradigm in natural language processing and computer vision, an emerging class of world models is trained at industrial scale on massive, heterogeneous datasets before being adapted to specific downstream tasks through lightweight fine-tuning or zero-shot transfer. 

**World foundation models.** At the largest scale, World Foundation Models (WFMs) are pretrained on diverse, internet-scale data to learn general-purpose dynamics priors. OpenAI’s Sora [10] demonstrated that training a diffusion transformer on large-scale internet video yields temporally coherent visual sequences that appear to respect certain physical constraints, though subsequent analysis revealed these properties to be inconsistent [11, 107]. NVIDIA’s Cosmos [14] released openweight WFMs at 7B and 14B parameters trained on over 20 million hours of real-world video, with 

28 

its successor Cosmos-Predict2.5 [108] transitioning to flow-matching with RL-based post-training on 200 million clips. DeepMind’s Genie series [13, 109, 110] progressively scaled interactive world model generation from 2D environments to 3D navigable worlds generated from text prompts at 720p and 24 fps. The Large World Model (LWM) [111] pursued an orthogonal scaling axis by extending context length to one million tokens via RingAttention, enabling joint modeling of long video and text sequences. These efforts represent the convergence of video generation and world simulation at industrial scale, though whether scale alone can yield genuine physical understanding—as opposed to sophisticated pattern matching—remains actively debated. 

**Pretrain-then-fine-tune for world models.** Below the scale of foundation models, the pretrainthen-fine-tune paradigm has been adopted to improve the data efficiency of task-specific world model training. WPT [112] pretrains a generalist world model on reward-free, non-expert offline data from diverse tasks, then fine-tunes it online for specific downstream tasks, demonstrating clear improvements in sample efficiency—particularly on hard exploration tasks where learning from scratch fails entirely. MOTO [113] explores offline pretraining followed by online fine-tuning for model-based robot learning, while Vid2Act [114] uses a mixture world model pretrained on multi-task offline trajectories and adaptively transfers dynamics knowledge to novel tasks through domain-selective distillation. 

**Cross-domain transfer and adaptation.** A key promise of pretrained world models is their ability to transfer knowledge across domains, embodiments, and environments. SimDist [115] pretrains world model components in simulation and finetunes only the dynamics model for real-world deployment, exploiting the modular structure of world models to directly target the sim-to-real dynamics gap. V-JEPA 2-AC [12] achieves zero-shot robotic planning on physical robots using a world model post-trained on fewer than 62 hours of unlabeled robot video—without collecting any data from the target environment or performing any task-specific training. The Open X-Embodiment initiative [116] demonstrated that policies trained on a mixture of over one million trajectories from 22 robot embodiments achieve 50% higher success rates than single-domain policies, establishing that cross-embodiment transfer is viable at scale. 

#### **3.4.5 Supervised and Imitation Learning** 

While self-supervised and reinforcement learning paradigms dominate the world model literature, supervised and imitation learning remain important in settings where ground-truth labels, expert demonstrations, or structured prior knowledge are available. 

**Learning from demonstrations.** In robotic manipulation, world models are frequently trained on large-scale teleoperated demonstrations. RT-1 [117] trained a scalable transformer on over 130,000 real-robot episodes covering more than 700 tasks, achieving 97% success rate on trained tasks. While RT-1 and its successors (RT-2 [118], OpenVLA [119]) are primarily framed as VisionLanguage-Action policies rather than explicit world models, their training paradigm—supervised next-action prediction from observation-action pairs—is structurally analogous to world model training, and the implicit dynamics knowledge they acquire through large-scale demonstration learning increasingly overlaps with the capabilities of explicit world models. 

**Language and structured supervision.** Language provides a rich form of weak supervision for world model learning. GAIA-1 [62] jointly conditions video generation on text descriptions and 

29 

structured control inputs, where the text serves as a supervisory signal specifying scene composition and ego-vehicle behavior. WorldLLM [79] induces explicit natural-language hypotheses about transition regularities via Bayesian inference over agent experience, yielding an interpretable world model guided by linguistic structure. Language-conditioned latent dynamics models such as Dynalang [120] treat language understanding itself as emergent from the dynamics learning objective: the model learns to associate diverse language types—descriptions, instructions, corrections—with their environmental consequences through supervised prediction. 

**Physics-supervised learning.** A distinct form of supervision arises when world models are trained on data generated by physics simulators with known ground-truth dynamics. Physicsinformed model-based RL [121] incorporates known physics equations as soft or hard constraints within the world model training loop. Machine learning interatomic potentials such as SchNet [122] and NequIP [123] are trained on quantum-mechanical calculations to approximate potential energy surfaces, functioning as supervised world models of molecular dynamics. These approaches trade generality for physical accuracy and are discussed further in Section 4.5. 

#### **3.4.6 Hybrid and Multi-Stage Learning Paradigms** 

In practice, the most effective world model systems increasingly combine multiple learning paradigms in staged or interleaved training pipelines, leveraging the complementary strengths of each approach. 

**Self-supervised pretraining followed by RL fine-tuning.** The most prominent hybrid paradigm combines large-scale self-supervised pretraining with task-specific reinforcement learning. V-JEPA 2 [12] exemplifies this two-stage approach: a 1.2-billion-parameter video encoder is first pretrained via self-supervised masked prediction on over one million hours of internet video, then post-trained as an action-conditioned world model (V-JEPA 2-AC) using a small amount of robot interaction data, with planning performed via the Cross-Entropy Method at deployment. CosmosPredict2.5 [108] follows a similar trajectory: self-supervised pretraining via flow-matching is followed by RL-based post-training to improve physical plausibility. The finding from DreamerV3 [8] that world model representations are predominantly shaped by unsupervised reconstruction objectives further motivates this paradigm, suggesting that task-agnostic pretraining on large unlabeled datasets could substantially reduce the online interaction budget required for downstream task learning. 

**Simulation pretraining with real-world adaptation.** A complementary hybrid approach leverages the abundant data available in simulation to pretrain world models that are subsequently adapted to the real world. DayDreamer [83] demonstrated that world models can bridge this gap by learning directly on physical robots, while SimDist [115] takes a modular approach—pretraining the full world model stack in simulation and finetuning only the dynamics component using a small number of real-world trajectories. Domain randomization and curriculum learning strategies further support this paradigm by training world models across distributions of simulated environments to improve robustness to real-world variation. 

**Multi-task and multi-modal joint training.** The Unified World Model (UWM) [124] couples video prediction and action generation through a shared diffusion process during pretraining on large-scale robotic datasets, enabling a single model to serve simultaneously as a simulator and a policy. Motus [125] introduces a Mixture-of-Transformer architecture integrating three specialized experts—for understanding, video generation, and action prediction—with flexible mode-switching 

30 

within a single framework, achieving a 45% absolute improvement over prior vision-language-action baselines by pretraining on unlabeled video with optical flow as an embodiment-agnostic action proxy. 

#### **3.4.7 Discussion and Open Challenges** 

Table 2 presents representative world models classified by learning paradigms, where Data req.” indicates the typical scale of training data, Labels” specifies whether task-specific supervision is required, and “Generalization” characterizes the breadth of transfer capability. 

The six learning paradigms surveyed above reveal several important cross-cutting trends and unresolved tensions. 

First, there is a clear trajectory toward _paradigm convergence_ : the most capable world models increasingly combine self-supervised pretraining with task-specific reinforcement learning or supervised fine-tuning, mirroring the “pretrain then adapt” recipe that has proven transformative in NLP and computer vision. The finding that DreamerV3’s representations are dominated by unsupervised objectives [8] provides theoretical motivation for this trajectory, suggesting that the bulk of world knowledge can be acquired from unlabeled data. 

Second, the question of _objective alignment_ remains largely unresolved. Self-supervised objectives such as pixel reconstruction and denoising are not necessarily aligned with downstream decision-making requirements [106]. Decision-oriented approaches—exemplified by MuZero’s valueequivalence principle [101] and JEPA’s selective prediction in representation space [5]—offer principled alternatives, but a unified framework that systematically balances predictive accuracy with decision utility is still lacking. 

Third, the emergence of _scaling laws for world models_ represents a critical open question. Foundation models such as Cosmos and Sora demonstrate that larger models trained on more data yield improved generation quality, but whether this improvement translates to genuine physical understanding—rather than more sophisticated pattern matching—remains contested. Controlled experiments by Kang et al. [107] suggest that video generation models exhibit case-based generalization rather than abstract physical reasoning, highlighting the need for evaluation protocols that distinguish statistical regularity from causal understanding. 

Fourth, _data efficiency and data scale_ present a fundamental tension. JEPA and foundation model paradigms achieve strong cross-domain generalization but require millions of hours of video data for pretraining. Online MBRL methods achieve remarkable data efficiency—PlaNet demonstrated 50 _×_ improvements over model-free methods—but generalize poorly beyond their training distribution. Bridging this gap through sample-efficient transfer from pretrained representations to novel environments is among the most important open problems. 

Fifth, _continual and lifelong learning_ of world models has received comparatively little attention. Deployed world models must adapt to evolving environments, new objects, and shifting dynamics without catastrophically forgetting previously acquired knowledge. Current systems are almost universally trained in a single phase and frozen at deployment, a limitation that fundamentally constrains their real-world applicability. 

Finally, the interplay between learning paradigm and _causal understanding_ warrants deeper investigation. Most self-supervised world models learn correlational rather than causal models of dynamics, as demonstrated by the failure modes identified in LLM-based world simulators [126] and video generation models [107]. Whether architectural innovations, training objectives, or data curation strategies can enable world models to acquire genuine causal understanding through any learning paradigm remains one of the field’s most fundamental open questions. 

31 

Table 2: Representative world models classified by learning <u>paradigm.</u> 

|**Learning Paradigm**|**Representative**<br>**Models**|**Data Req.**|**Labels**|**Generalization**|**Compute**|
|---|---|---|---|---|---|
|**_Self-Supervised / Unsu_**|**_pervised_**|||||
|Reconstruction-based|Dreamer<br>v1–v3 [6–8],<br>DIAMOND [37],<br>GameNGen [61]|Med–High|None|Moderate|Moderate|
|Contrastive /<br>Non-contrastive|C-SWM [63],<br>SPR [95],<br>DINO-WM [98]|Med|None|Moderate|Low–Med|
|JEPA|I-JEPA [39],<br>V-JEPA [57],<br>V-JEPA 2 [12]|Very High|None|High|High|
|**_Online Model-Based RL_**||||||
|Data augmentation<br>(Dyna-style)|Dyna-Q [99],<br>MBPO [48],<br>STEVE [100]|Low|Reward|In-domain|Moderate|
|Imagination-based|PlaNet [31],<br>Dreamer [6],<br>DayDreamer [83]|Low–Med|Reward|In-domain|Moderate|
|Search-based|MuZero [9], Effi-<br>cientZero [102],<br>TD-MPC [46]|Low–Med|Reward|In-domain|Med–High|
|**_Offline / Batch Learnin_**|**_g_**|||||
||MOPO [103],<br>DWM [104],<br>RLVR-<br>World [105]|Medium|Reward|Data-limited|Low–Med|
|**_Foundation Model Pret_**|**_raining_**|||||
||Sora [10],<br>Cosmos [14],<br>Genie [13],<br>LWM [111]|Very High|None/Weak|Cross-domain|Very High|
|**_Supervised / Imitation_**||||||
||RT-1 [117],<br>GAIA-1 [86],<br>Dynalang [120],<br>WorldLLM [79]|Med–High|Required|In-domain|Moderate|
|**_Hybrid / Multi-Stage_**||||||
||V-JEPA<br>2-AC [12],<br>Cosmos-<br>Predict2.5 [108],<br>UWM [124],<br>Motus [125]|Flexible|Partial|High|High|


32 

### **3.5 Classification by downstream use** 

While prior subsections have organized world models by their architectural backbone and learning paradigm, an equally revealing lens is their _downstream application_ . The same foundational idea-learning an internal model of environment dynamics and using it to anticipate future statesmanifests very differently depending on whether the end goal is mastering a board game, navigating an urban intersection, folding laundry, diagnosing tumors, generating cinematic video, or reasoning over natural language. Examining world models through the lens of downstream use exposes not only domain-specific design constraints (observation modality, action space, safety requirements, real-time latency budgets) but also recurring architectural motifs that transcend individual fields. In what follows, we survey six major application families, highlight representative systems in each, and close with a cross-cutting discussion of open challenges. 

#### **3.5.1 Reinforcement Learning and Planning** 

Reinforcement learning (RL) and game-playing remain the original and most mature proving ground for world models. PlaNet [31] demonstrated that a recurrent state-space model trained entirely from image observations could support effective planning via the cross-entropy method, eliminating the need for a model-free policy altogether. The Dreamer line of work extended this idea to actorcritic learning entirely within imagined trajectories: Dreamer [32] introduced latent imagination for continuous-action tasks, DreamerV2 [34] replaced Gaussian latents with discrete representations and matched model-free performance on the Atari benchmark, and DreamerV3 [40] introduced a suite of robustness techniques-symlog predictions, layer normalization, and free-bits KL balancing-that allowed a single set of hyperparameters to master domains ranging from Minecraft to continuous locomotion. 

In parallel, the MuZero family [38] demonstrated that a learned dynamics model, combined with Monte Carlo tree search (MCTS), could achieve superhuman performance in Go, chess, shogi, and Atari without access to ground-truth game rules. EfficientZero [102] augmented MuZero with self-supervised temporal consistency losses and achieved human-level Atari performance with only two hours of real-time experience, dramatically improving sample efficiency. For continuous control, TD-MPC [46] proposed learning an implicit latent dynamics model jointly optimized with temporaldifference objectives and local trajectory optimization, and its successor TD-MPC2 [127] scaled this paradigm to a single 317M-parameter world model capable of solving 80 diverse continuous-control tasks, establishing a new benchmark for generalist model-based control. A persistent limitation across RL world models is compounding prediction error over long horizons, which degrades both planning and policy optimization quality. 

#### **3.5.2 Autonomous Driving** 

Autonomous driving presents world models with a distinctive set of challenges: multi-agent interaction, long-tail safety scenarios, multi-sensor fusion, and the need to generate physically plausible future states at both the geometric and photometric level. GAIA-1 [86] was among the first largescale generative world models for driving, using a video diffusion architecture conditioned on text, action, and map inputs to produce realistic multi-second driving rollouts. Its successor, GAIA2 [128], extended the framework to controllable multi-view generation with improved geometric consistency. DriveDreamer [129] adopted a two-stage approach-first learning structured traffic dynamics, then generating video conditioned on predicted layouts-and DriveDreamer-2 [130] further incorporated large language models for diverse scenario description and generation. WoVoGen [131] 

33 

advanced multi-camera consistency through world-volume-aware diffusion, explicitly lifting generation into 3D to enforce cross-view coherence. 

Beyond video-centric formulations, several works have explored geometric world models for driving. OccWorld [132] learns a 3D occupancy-based world model that jointly predicts future scene occupancy and ego-vehicle motion, enabling downstream planning in a structured volumetric representation. Vista [133] demonstrated that a single autoregressive video world model can generalize across diverse driving conditions while offering versatile controllability over viewpoint, dynamics, and weather. UniSim [88] pushed the boundary further by learning a universal real-world simulator that can render novel viewpoints and simulate the visual consequences of arbitrary agent actions, bridging the gap between world modeling and closed-loop simulation. A key open question in driving world models is the extent to which photorealistic generation translates into improved downstream planning performance versus merely serving as a data-augmentation tool. 

#### **3.5.3 Robotics and Embodied AI** 

Transferring world models from simulation to physical hardware introduces challenges of partial observability, noisy actuators, and the prohibitive cost of real-world data collection. DayDreamer [83] provided the first demonstration that the Dreamer framework could learn locomotion and manipulation behaviors entirely on physical robots, achieving quadruped walking in one hour and robotic arm pick-and-place in ten minutes of real interaction-without any simulation pre-training. RoboDreamer [64] extended world models to compositional multi-step manipulation by learning compositional world dynamics that decompose complex instructions into sequenced sub-goals, enabling robot imagination over long task horizons. 

A complementary line of research focuses on learning general-purpose visual representations that implicitly encode world dynamics. V-JEPA 2 [12] pre-trained a joint-embedding predictive architecture on over one million hours of internet video, then post-trained an action-conditioned predictor (V-JEPA 2-AC) with fewer than 62 hours of unlabeled robot trajectories. The resulting model enabled zero-shot prehensile manipulation on Franka arms in new lab environments via model-predictive control-without any task-specific reward or additional data collection. While not world models per se, the Robotics Transformer series-RT-1 [117] and RT-2 [118]-demonstrated that large-scale transformer policies trained on diverse robot data can exhibit emergent generalization, and RT-2 in particular showed that vision-language pre-training allows robot policies to inherit semantic reasoning from web-scale data. The interplay between explicit world-model planning (DayDreamer, RoboDreamer) and implicit world knowledge encoded in large foundation models (V-JEPA 2, RT-2) remains an active frontier, with hybrid architectures increasingly favored. 

#### **3.5.4 Healthcare and Medical Imaging** 

Healthcare represents a nascent yet high-impact frontier for world models, where the ability to simulate disease progression or physiological dynamics can directly inform clinical decision-making. CEKWorld [69] introduced the first world model for MRI contrast enhancement kinetics, learning to simulate the spatiotemporal dynamics of contrast agent distribution from a single non-contrast scan. By modeling pharmacokinetic evolution through spatiotemporal consistency learning, CEKWorld eliminates the need for exogenous contrast injection, reducing patient risk and cost while enabling continuous temporal-resolution imaging. CLARITY [134] proposed a latent-space world model for disease trajectory forecasting, conditioning predictions on treatment decisions to support treatment planning in oncology. Similarly, MeWM [135] demonstrated generative simulation of tumor evolution conditioned on clinical interventions, improving optimal treatment protocol selection 

34 

#### by 13% in F1 score. 

Beyond treatment planning, self-supervised world models have entered neuroscience. BrainJEPA [136] applied a JEPA framework with gradient positioning and spatiotemporal masking to fMRI data, learning brain dynamics representations that transfer to diverse downstream tasks. A recent survey by Qazi et al. [137] provides the first systematic review of world models in healthcare, organizing the field into four capability levels: temporal prediction, action-conditioned prediction, counterfactual rollouts, and planning or control. The survey highlights that most medical world models remain at level one or two, with counterfactual reasoning and closed-loop planning representing largely unrealized opportunities. Critical challenges include the extreme scarcity of longitudinal paired data, the need for rigorous uncertainty quantification in clinical deployment, and regulatory barriers to using generative models in diagnostic pipelines. 

#### **3.5.5 Video Generation and Creative Simulation** 

The convergence of world modeling and video generation has produced some of the most publicly visible systems in AI. OpenAI’s Sora [138] framed video generation explicitly as _world simulation_ , using a diffusion-transformer architecture to produce photorealistic videos with emergent physical behaviors such as object persistence and fluid dynamics, though it notably struggles with finegrained physical consistency. Genie [13] from DeepMind approached interactive world modeling by learning a latent action space entirely from unlabeled internet video, enabling playable 2D environments generated from a single image. Genie 2 [109] scaled this concept to photorealistic 3D environments with persistent geometry and object interactions, positioning foundation world models as a potential replacement for hand-authored game engines. 

In the domain of interactive simulation, GameNGen [76] demonstrated that a diffusion model conditioned on action sequences could simulate the DOOM game engine in real time at over 20 frames per second, with visual quality nearly indistinguishable from the original engine according to human evaluators. DIAMOND [37] showed that diffusion-based world models preserve visual details critical for downstream RL performance in Atari, outperforming prior discrete-token world models. NVIDIA’s Cosmos [14] introduced a world foundation model platform explicitly designed for physical AI applications, providing pre-trained video generation backbones that downstream systems can fine-tune for robotics, driving, or creative tasks. A fundamental tension in this space is whether video-generation world models truly learn physical laws or merely produce visually plausible hallucinations-a distinction with profound implications for safety-critical downstream uses. 

#### **3.5.6 Language Reasoning and Decision-Making** 

An emerging research direction reinterprets large language models (LLMs) themselves as world models, leveraging their latent knowledge for planning and reasoning. RAP [139] formalized this perspective by treating an LLM as a world model within a Monte Carlo tree search framework: the LLM simulates the consequences of candidate reasoning steps, a reward function scores partial solutions, and MCTS guides search toward high-quality completions. This approach achieved substantial improvements on mathematical reasoning, plan generation, and logical inference benchmarks. WebDreamer [78] applied a similar model-based planning paradigm to web agents, using an LLM to simulate the outcomes of candidate browser actions (clicking, typing, navigating) and selecting actions via tree search over imagined web page states, outperforming reactive baselines on WebArena benchmarks. 

Dynalang [120] explored a different integration point, using language as an additional observation modality within a DreamerV3-based world model. By grounding language tokens in the same 

35 

latent dynamics as visual observations, Dynalang enables agents to benefit from language hints, instructions, and contextual descriptions during both world model learning and policy optimization. WorldLLM [79] introduced curiosity-driven theory-making, where an LLM iteratively builds and refines explicit world theories to improve its predictive accuracy and downstream decision-making. These language-centric world models highlight a fundamental question: whether the implicit world knowledge captured during language pre-training is sufficient for reliable planning, or whether explicit dynamics learning remains necessary for robust decision-making in complex environments. 

#### **3.5.7 Discussion and Open Challenges** 

Several cross-cutting themes emerge from this survey of downstream applications. First, there is a clear progression from _task-specific_ world models (e.g., MuZero for board games, OccWorld for driving) toward _foundation world models_ (e.g., Cosmos, Genie 2, V-JEPA 2) that aim to serve as general-purpose backbones across domains. Whether such generalist models can match specialist performance in safety-critical settings remains unresolved. Second, the evaluation gap is widening: video-generation world models are often assessed on perceptual quality metrics (FID, FVD), whereas RL world models are measured on task reward, and medical world models on clinical endpoints-making cross-domain comparison and progress tracking difficult. Third, the question of whether world models learn genuine _causal_ structure or merely correlational shortcuts is increasingly urgent, particularly as these models enter healthcare and autonomous driving where counterfactual reasoning is essential. Finally, the computational cost of training and deploying large-scale world models remains a bottleneck, with real-time inference posing particular challenges for embodied applications. Addressing these challenges will require not only architectural advances but also new evaluation frameworks, safety guarantees, and interdisciplinary collaboration. 

## **4 Categorization of World Models by Methodological Families** 

This section focuses on the main _methodological families_ used to build and train the World Models. Each family reflects different assumptions about how environmental dynamics should be modeled, which inductive biases are most effective, and how learned representations should relate to underlying physical processes. We begin with state-space and recurrent latent models (Section 4.1), which have long been central to model-based reinforcement learning, and then examine transformer-based world models (Section 4.2), which replace recurrence with self-attention and tokenized representations. We next consider diffusion-based world models (Section 4.3), followed by physics-informed and structured approaches (Section 4.4) that embed domain knowledge directly into the architecture. We conclude with language-augmented and multi-modal world models, which combine natural language with diverse sensory inputs to support richer grounding and broader generalization. 

### **4.1 State-space and recurrent latent world models** 

Structured State Space Models (SSMs) such as S4 [140] and Mamba [141] offer _O_ ( _n_ ) sequence processing with strong long-range dependency modeling, presenting an alternative to both recurrent and attention-based architectures. S4 introduced structured parameterizations that efficiently capture long-range dependencies through the HiPPO framework. Mamba extended this with inputdependent (selective) state transitions, achieving transformer-competitive performance on language and other modalities at 5 _×_ higher throughput. Recent work has begun to explore SSMs explicitly as world-model backbones: Po et al. [142] proposed long-context state-space video world models 

36 

(ICCV 2025), demonstrating that linear RNNs can capture long-range temporal dependencies without increasing per-frame generation cost. Their linear complexity and strong temporal modeling make SSMs promising candidates for long-horizon environment simulation. 

Whereas, recurrent neural networks, particularly LSTMs [143] and GRUs [144], were the first deep architectures used for world modeling. Ha and Schmidhuber [4] combined a VAE (the “vision” model V) with a Mixture Density Network-RNN (MDN-RNN, the “memory” model M) to learn a compact generative model of RL environments. The VAE compressed each image frame into a latent vector _zt_ , while the MDN-RNN predicted the distribution of the next latent _p_ ( _zt_ +1 _|zt, at_ ), capturing stochastic dynamics. A minimal linear controller (only 867 parameters) trained via CMA-ES could solve Car Racing and VizDoom tasks by planning entirely in the model’s imagination. 

Hafner et al. [31] introduced the Recurrent State-Space Model (RSSM) in PlaNet, which splits the latent state into a deterministic recurrent component _ht_ and a stochastic component _zt_ . This dual-path design was critical: the deterministic path preserves long-range memory, while the stochastic path captures environmental uncertainty. PlaNet used the Cross-Entropy Method (CEM) for online planning and demonstrated 50 _×_ data efficiency improvements over model-free methods on continuous control tasks from pixels. 

The Dreamer series [32, 34, 40] extended the RSSM with actor-critic learning in imagined trajectories. DreamerV1 learned value functions and policies by backpropagating analytic gradients through the world model’s predictions. DreamerV2 introduced discrete categorical latent representations, enabling mastery of Atari games. DreamerV3 achieved robustness across 150+ tasks with a fixed set of hyperparameters through normalization and transformation techniques, and was the first algorithm to collect diamonds in Minecraft from scratch without human demonstrations. 

GAN-based world models exploit adversarial training for sharper outputs. GameGAN [145] learned to simulate Pac-Man by ingesting gameplay screenshots and keyboard actions, using a dynamics engine, memory module, and rendering engine—all implemented as neural networks trained end-to-end. While producing visually crisp frames, GAN-based approaches suffer from training instability and mode collapse, limiting their adoption for complex environments. 

### **4.2 Transformer-based world models** 

The transformer architecture [146], originally developed for natural language processing, has emerged as a dominant paradigm for world modeling owing to its capacity for long-range dependency modeling, parallelizable training, and favorable scaling properties. This section surveys the evolution of transformer-based world models, from early sequence-modeling formulations of reinforcement learning to large-scale interactive environment generators. 

**Foundational formulations.** The application of transformers to sequential decision-making was catalyzed by two concurrent works. The first one is _Decision Transformer_ [147] recast offline reinforcement learning as conditional sequence modeling: a causally masked GPT architecture autoregressively generates actions conditioned on desired returns-to-go, past states, and actions, entirely bypassing temporal-difference learning and value function estimation. The Second one is _Trajectory Transformer_ [148] adopted a complementary model-based perspective, discretizing continuous state-action-reward trajectories into tokens and modeling their joint distribution with a transformer, thereby enabling beam-search-based planning over long horizons. Together, these works established that the sequence prediction capabilities of transformers could subsume both policy learning and dynamics modeling within a unified framework. 

Concurrent developments in video generation provided key architectural ingredients. For exapmle, VideoGPT [149] demonstrated that a VQ-VAE tokenizer paired with an autoregressive transformer could generate temporally coherent video sequences, foreshadowing the _tokenize-then-predict_ 

37 

paradigm that would become standard in visual world models. Scaling these ideas to multi-task settings, Gato [150] serialized data from over 600 diverse tasks-spanning Atari games, robotic manipulation, image captioning, and dialogue-into a single token sequence consumed by a 1.2Bparameter decoder-only transformer, demonstrating the feasibility of a universal generalist agent. The Multi-Game Decision Transformer [151] investigated scaling properties by training a single transformer policy across multiple Atari games simultaneously, while Algorithm Distillation [152] showed that entire RL learning histories could be distilled into a causal transformer, enabling _in-context_ reinforcement learning-improvement across episodes without any parameter updates. 

**RL agents trained in transformer world models.** A pivotal advance came with IRIS [35], which demonstrated that transformers are sample-efficient world models for imagination-based reinforcement learning. IRIS employs a discrete autoencoder to tokenize visual observations into a sequence of codes _zt_ = ( _zt_<sup>1</sup><sup>_, . . . , z_</sup> _t_<sup>_K_)andtrainsanautoregressivetransformertopredictfuture</sup> token sequences conditioned on past observations and actions: 


where _rt_ and _γt_ denote the predicted reward and termination signal, respectively. On the Atari 100k benchmark, IRIS achieved a mean human-normalized score of 1.046, surpassing human performance on 10 of 26 games and establishing a new state of the art for methods without lookahead search. 

Several works rapidly built upon this paradigm. TransDreamer [153] proposed the Transformer State-Space Model (TSSM), directly replacing the GRU-based Recurrent State-Space Model (RSSM) in the Dreamer framework [40] with a transformer backbone while retaining stochastic latent variables, and demonstrated improved performance on tasks requiring long-range memory. TWM [154] applied a Transformer-XL architecture over compact latent representations of states, actions, and rewards, efficiently capturing long-term dependencies through segment-level recurrence. STORM [36] combined a GPT-like transformer with a categorical VAE encoder, introducing stochastic latent variables that improved robustness over IRIS’s deterministic tokenization; it achieved 126.7% mean human performance on Atari 100k with only 4.3 hours of training on a single GPU. 

More recent efforts have targeted efficiency and expressiveness. ∆-IRIS [155] introduced a context-aware tokenizer that encodes stochastic frame-to-frame deltas rather than full observations, dramatically reducing the token count per timestep and achieving state-of-the-art performance on Crafter while training an order of magnitude faster than IRIS. DART [156] paired a transformer decoder for world modeling with a transformer encoder for policy learning, incorporating explicit memory tokens to handle partial observability. Dedieu et al. [157] proposed three complementary improvements-Dyna-style warmup training, nearest-neighbor patch tokenization, and block teacher forcing-that together enabled a transformer world model to surpass both DreamerV3 and humanlevel performance on Craftax-classic for the first time, reaching 69.7% reward versus 53.2% for DreamerV3. 

**Transformer models as real-world and game simulators.** Beyond closed-loop RL training, transformers have been scaled to serve as general-purpose interactive simulators. Genie [13], an 11-billion-parameter model from Google DeepMind, represents the first generative interactive environment trained from unlabeled Internet video. Its architecture comprises three components: a spatiotemporal video tokenizer (ST-ViViT), a latent action model that infers discrete action codes from video without ground-truth action labels, and an ST-Transformer dynamics model that autoregressively predicts future latent frames conditioned on inferred actions. Genie enables controllable generation of diverse 2D platformer environments from text, sketch, or image prompts. 

38 

Its successor, Genie 2 [109], extends this paradigm to rich 3D environments using an autoregressive latent diffusion architecture, generating consistent interactive worlds for up to one minute from a single image prompt with emergent object interactions, NPC behavior, and persistent world memory. 

GAIA-1 [62], a 9-billion-parameter model from Wayve, applies the transformer world model paradigm to autonomous driving simulation. Its 6.5B-parameter autoregressive transformer predicts future discrete image tokens conditioned on video, text, and action inputs, while a 2.6Bparameter video diffusion decoder renders predictions back to pixel space, exhibiting emergent understanding of 3D geometry and traffic dynamics. UniSim [158] learns an interactive real-world simulator by orchestrating diverse training data-internet images, robotics trajectories, and navigation sequences-to simulate visual outcomes of both high-level language instructions and low-level motor commands; policies trained entirely within UniSim transfer zero-shot to real robotic manipulation. Oasis [159] demonstrated real-time open-world generation using a Diffusion Transformer (DiT) backbone, producing Minecraft-like interactive environments at 20 FPS. Pandora [160] coupled a pretrained large language model with a video diffusion model for world simulation controlled by free-form natural language. OpenAI’s Sora [161] further established the paradigm of large-scale video generation models as implicit world simulators, demonstrating emergent physical reasoning in a diffusion transformer trained on internet-scale video. 

**Domain-specific adaptations.** Transformer-based world models have seen extensive adoption in _autonomous driving_ . UniAD [162], a unified detection, tracking, mapping, motion forecasting, occupancy prediction, and planning within a single transformer framework where all perception modules serve the downstream planning objective through unified query interfaces. OccWorld [132] formulates the driving world model in 3D semantic occupancy space: a VQ-VAE scene tokenizer produces discrete volumetric tokens, and a GPT-like spatial-temporal transformer autoregressively forecasts future occupancy grids and ego trajectories. Copilot4D [67] applies discrete diffusion on VQ-VAE-tokenized LiDAR point clouds using a spatial-temporal transformer, reducing prior stateof-the-art Chamfer distance by over 65% for one-second predictions on nuScenes. MILE [163] jointly learns a world model and driving policy through model-based imitation learning, executing complex maneuvers from plans generated entirely in imagination. ViDAR [164] introduced visual point cloud forecasting as a scalable self-supervised pretraining objective that jointly learns semantics, 3D structure, and temporal dynamics, while Vista [133] developed a generalizable driving world model with high-fidelity, action-conditioned, long-horizon prediction trained on large-scale websourced driving video. 

In _robotics_ , the Robotics Transformer series has demonstrated the efficacy of transformer-based models for real-world manipulation at scale. RT-1 [117] trained a 35-million-parameter transformer on over 130,000 real robot episodes spanning 700+ tasks, establishing robust multi-task generalization. RT-2 [165] co-fine-tuned large vision-language models (PaLI-X 55B and PaLM-E 12B) on both web-scale data and robotic trajectories, representing robot actions as text tokens. This enabled significant transfer of web knowledge to robotic control-improving success rates on novel objects from 32% to 62%-and emergent semantic reasoning capabilities including chain-of-thought planning for multi-step manipulation tasks. 

**Comparative analysis and key challenges.** Transformer-based world models offer several structural advantages over recurrent and diffusion-based alternatives. Unlike GRU-based models such as the RSSM in the Dreamer line [40], transformers attend directly to any past timestep, circumventing the information bottleneck of fixed-size hidden states and enabling superior longrange dependency modeling. Compared to diffusion-based world models such as DIAMOND [37], autoregressive transformers generate predictions in a single forward pass rather than requiring iterative denoising steps, yielding substantial inference-time efficiency-a critical advantage for online 

39 

#### planning within imagination. 

However, transformers introduce distinct challenges. The _quadratic computational complexity O_ ( _T_<sup>2</sup> ) with respect to context length _T_ remains a fundamental bottleneck, particularly for highresolution visual world models where each observation may comprise hundreds of tokens. Mitigation strategies have included delta encoding to reduce per-frame token counts [155], Transformer-XL segment-level recurrence [154], and fused single-token-per-timestep representations [36]. The _discrete tokenization bottleneck_ poses another limitation: VQ-VAE-based approaches necessarily discard fine-grained visual information during quantization, a weakness that diffusion-based world models [37] explicitly address by operating in continuous pixel space. Furthermore, _autoregressive error accumulation_ over extended prediction horizons can degrade imagined trajectory quality, a problem partially mitigated by stochastic latent variables in STORM [36] and TransDreamer [153]. As transformer world models scale from game benchmarks toward open-ended real-world simulation, addressing these challenges while preserving the architecture’s strengths in expressiveness, parallelism, and scalability constitutes an active and rapidly evolving research frontier. 

### **4.3 Diffusion-Based World Models** 

Diffusion models [166] have emerged as a powerful paradigm for world modeling, offering a compelling alternative to discrete-token and recurrent approaches. Rooted in denoising score matching, these models learn to reverse a gradual noise-corruption process, generating high-fidelity samples through iterative denoising. When adapted for world modeling, diffusion-based approaches inherit several attractive properties: capturing complex, multi-modal distributions over future states, preserving fine-grained visual details that discrete tokenization may discard, and naturally representing environmental stochasticity through the sampling process itself. 

**Foundational formulations.** The core idea is to recast image generation as a conditional next-observation prediction problem. Given past observations _o<t_ and an action _at_ , the diffusion world model learns _p_ ( _ot_ +1 _| o<t, at_ ) by training a denoising network _ϵθ_ to remove noise from a corrupted target observation. The training objective follows the standard denoising score matching loss: 


where _o_<sup>(</sup><sup>_k_)</sup> _t_ +1<sup>denotestheobservationcorruptedatnoiselevel</sup><sup>_k_and</sup><sup>_ϵ∼N_(0</sup><sup>_, I_).Atinferencetime,</sup> predictions are generated by starting from pure noise and applying the learned denoising process for _K_ steps. A key architectural distinction is whether the diffusion process operates in pixel space or a learned latent space. Pixel-space approaches such as DIAMOND [37] operate directly on raw observations, preserving all visual details at higher computational cost. Latent diffusion approaches [167] first compress observations through a pretrained VAE, then apply diffusion in the lower-dimensional latent space. This strategy, adopted by GameNGen [61], Sora [168], NVIDIA Cosmos [14], and many autonomous driving world models, significantly reduces computational costs while maintaining high perceptual quality. 

An important early contribution bridging diffusion models and sequential decision-making was Diffuser [169], which directly modeled the joint distribution over state-action trajectories _p_ ( _τ_ ) = _p_ ( _s_ 1 _, a_ 1 _, . . . , sT , aT_ ) using a temporal U-Net. Planning was accomplished by sampling from this trajectory distribution, with classifier-guided sampling and inpainting techniques steering trajectories toward high-reward regions or goal constraints. Decision Diffuser [170] extended this framework with classifier-free guidance, conditioning trajectory generation directly on target returns, constraints, or skills without a separately trained reward function. A further development, the Diffusion World Model (DWM) [104], departs from the one-step autoregressive paradigm by 

40 

predicting multi-step future states and rewards concurrently in a single forward pass, achieving a 44% performance gain over one-step dynamics models on D4RL benchmarks. 

**RL agents trained in diffusion world models.** A defining application of diffusion-based world models is their use as imagination environments for RL agent training, analogous to the Dreamer series [34, 171, 172] but with the world model replaced by a diffusion process. DIAMOND [37] (NeurIPS 2024 Spotlight) represents the most rigorous exploration of this paradigm, replacing discrete-token world models (e.g., IRIS [35]) with a pixel-space diffusion model conditioned on a short history of past frames and actions. Several design choices proved critical. First, DIAMOND adopted the EDM framework [173] rather than DDPM [166], which becomes unstable under autoregressive generation with few denoising steps due to compounding errors. Second, EDM enabled stable long-horizon rollouts with as few as three denoising steps per frame. Third, for transitions with multiple plausible outcomes (e.g., opponent movement in Boxing), more denoising steps enabled better mode selection, whereas single-step denoising averaged across modes, producing blurry predictions. On Atari 100k, DIAMOND achieved a mean human-normalized score of 1.46, a new state of the art for agents trained entirely within a world model. Qualitative analysis revealed that improved performance in certain games was directly attributable to better modeling of critical visual details (e.g., small ball positions, score digits) that discrete-token approaches failed to preserve. DIAMOND was further demonstrated as an interactive neural game engine on 87 hours of Counter-Strike: Global Offensive gameplay, scaling from 4.4M to 381M parameters via a two-stage low-resolution dynamics prediction and diffusion-based upsampling pipeline. A subsequent extension, StateSpaceDiffuser [174], addresses DIAMOND’s limited temporal context by integrating a state-space model (Mamba), enabling long-context diffusion world modeling with linear per-frame complexity. 

In robotics, diffusion world models have recently been adopted to refine pre-trained manipulation policies. World4RL [175] uses a diffusion-based world model pre-trained on multi-task robotic datasets as a high-fidelity simulator for end-to-end RL fine-tuning, entirely avoiding real-world interaction. Similarly, DiWA [176] leverages a latent world model to adapt diffusion-based robotic skills offline, achieving effective fine-tuning on the CALVIN benchmark with orders of magnitude fewer physical interactions than model-free baselines. These works demonstrate that the trainin-imagination paradigm, initially validated on Atari, is now maturing toward real-world robotic deployment. 

**Diffusion models as real-world and game simulators.** Diffusion-based world models have also been deployed as standalone interactive simulators. GameNGen [61] demonstrated that a diffusion model built upon Stable Diffusion v1.4 could simulate classic DOOM at over 20 FPS on a single TPU, trained in two phases: an RL agent first played DOOM and its sessions were recorded, then a diffusion model learned next-frame prediction conditioned on past frames and actions. A key contribution was conditioning noise augmentation, which stabilized autoregressive generation over multi-minute sessions (next-frame PSNR 29.4, near-chance human distinguishability). GameGenX [177] extended this to interactive open-world environments with controllable actions and dynamic scenes. 

UniSim [88] proposed a universal real-world simulator trained on diverse data spanning internet images, robotics, navigation, and human activity. It predicts future frames conditioned on multimodal actions—from language instructions to low-level motor controls—unified via T5 embeddings with discretized control signals. UniSim enabled training vision-language planners and RL policies that transferred zero-shot to real robots, demonstrating diffusion world models’ potential for bridging the sim-to-real gap. 

OpenAI’s Sora [168] introduced large-scale video generation as world simulation via a DiT [178] architecture on spacetime latent patches, claiming emergent world-simulator properties. However, 

41 

subsequent work revealed these to be inconsistent [11], and Kang et al. [107] showed through controlled experiments that such models exhibit case-based generalization—mimicking nearest training examples rather than abstracting physical rules—fueling debate about whether visual-only training can yield true world models. 

The scaling of diffusion world models has entered the foundation model era. NVIDIA Cosmos [14] released open-weight WFMs in diffusion (7B/14B) and autoregressive variants, trained on 20 million hours of real-world video. Its successor Cosmos-Predict2.5 [108] transitioned to flowmatching with RL-based post-training on 200 million clips. Together with CogVideoX [179], which scales diffusion transformers via expert adaptive normalization, these efforts mark the convergence of video generation and world simulation at industrial scale. 

**Domain-specific adaptations.** Autonomous driving has been particularly fertile ground for diffusion-based world models, driven by the need for photorealistic simulation, action-controllable prediction, and scalable data augmentation. GAIA-1 [62] pioneered this direction with a 6.5Bparameter transformer world model paired with a 2.6B-parameter video diffusion decoder for controllable driving scenario generation conditioned on video, text, and action inputs. DriveDreamer [129] introduced a two-stage pipeline: the first stage learns structured traffic constraints via diffusion, while the second enables future state prediction conditioned on past trajectories. DriveDreamer-2 [130] leveraged LLMs to convert user queries into agent trajectories for corner-case generation, and DriveDreamer4D [180] extended this line to 4D driving scene representation by combining video generation with 4D Gaussian Splatting. GenAD [181] developed the generalized predictive model framework with action controllability and trajectory conditioning. Vista [133] pushed resolution to 576 _×_ 1024 pixels while supporting multiple action control modes (steering angle/speed, trajectory commands, goal points) through dynamic conditioning priors. GAIA-2 [182] scaled to multi-view generation with agent-level semantic control, trained on approximately 25 million video sequences across three countries. OccSora [183] proposed 4D occupancy generation as an alternative representation, generating geometry-aware voxel predictions that offer richer 3D structural information than image-based approaches. A common pattern across these models is latent diffusion with structured conditioning: BEV representations, 3D bounding boxes, HD map layouts, or ego-vehicle trajectories inject geometric and semantic structure into the diffusion process. Discrete diffusion has also been explored: Copilot4D [67] discretized LiDAR observations via VQ-VAE and employed discrete diffusion for unsupervised future point-cloud prediction, demonstrating that diffusion-based world modeling extends beyond the image domain. 

In robotic manipulation and control, Diffusion Policy [184] adapted trajectory diffusion to visuomotor control, generating action sequences conditioned on visual observations using a temporal U-Net or Transformer denoiser with receding-horizon execution. While not a world model per se, it demonstrates the broader utility of diffusion for action generation in embodied settings. Several works have since combined diffusion-based action generation with explicit world models: RoboDreamer [185] used language-guided imagination for long-horizon robotic planning, DreMa [186] integrated diffusion-based visual generation with model-based RL for dexterous manipulation, and IRASim [187] proposed a fine-grained interaction-aware world model for robot manipulation. A particularly promising direction is the unification of video prediction and action generation: the Unified World Model (UWM) [124] couples video and action diffusion during pre-training on largescale robotic datasets, enabling a single model to serve simultaneously as simulator and policy, while TesserAct [188] extends world modeling to 4D embodied representations for physically grounded robotic planning. 

**Comparative analysis and key challenges.** Compared to alternative generative paradigms, diffusion models offer several distinctive advantages for world modeling. First, they consistently produce sharper predictions than VAE-based approaches (which suffer from Gaussian-likelihood 

42 

blurriness) and discrete-token models (which may lose fine-grained details during quantization); DIAMOND’s Atari results demonstrate that this visual superiority translates directly to improved downstream RL performance. Second, the stochastic sampling process naturally represents environmental uncertainty, with multiple denoising trajectories yielding diverse plausible futures. Third, diffusion models support rich conditioning mechanisms (classifier-free guidance, cross-attention, inpainting) that incorporate diverse information sources without fundamental architectural changes. 

However, several key challenges remain. Inference speed is a fundamental bottleneck: iterative denoising is inherently slower than single-pass generation, and while few-step sampling, distillation, and consistency models [189] can reduce the gap, real-time generation remains challenging for high-resolution observations; flow-matching formulations as adopted by Cosmos-Predict2.5 [108] offer a promising direction. Autoregressive error accumulation persists: noise augmentation [61] and EDM-based formulations [37] provide effective but incomplete mitigation, while StateSpaceDiffuser [174] and the multi-step parallel prediction of DWM [104] represent two recent complementary approaches. Computational cost at scale remains prohibitive for many research groups, with Cosmos training on 200 million video clips at up to 14B parameters. Finally, as the debate around Sora illustrates and the controlled experiments of Kang et al. [107] confirm, diffusion models trained purely on visual data may learn statistical regularities that mimic physical behavior without acquiring genuine physical understanding; ensuring that predictions respect conservation laws, object permanence, and causal relationships remains an open challenge connecting to the physics-informed approaches discussed in Section 4.4. 

### **4.4 Physics-informed and structured world model** 

The preceding sections have examined world models grounded in recurrent latent dynamics, variational and adversarial generation, transformer-based sequence prediction, and diffusion-based denoising. A common thread across these approaches is their reliance on general-purpose function approximation: the network architecture imposes minimal assumptions about the structure of the environment, and physical plausibility must emerge entirely from data. While this flexibility enables broad applicability, it comes at a cost. Models that lack structural priors tend to violate conservation laws over long rollouts, struggle to generalize across object counts or physical parameters, and require large datasets to learn regularities that are already well-characterized by classical mechanics. This section surveys an alternative family of world models that embed physical laws, relational structure, or compositional object representations directly into the architecture or training objective. We organize the discussion into five sub-families: physics-conserving neural dynamics models, graph neural network-based dynamics simulators, object-centric world models, equivariant and symmetry-preserving models, and neuro-symbolic and compositional approaches. 

**Physics-conserving neural dynamics.** Classical mechanics provides two equivalent formalisms for describing conservative systems. In the Hamiltonian formulation, the state of a system is described by generalized coordinates **q** and conjugate momenta **p** , and the dynamics are governed by Hamilton’s equations: 


where _H_ ( **q** _,_ **p** ) denotes the Hamiltonian, which typically corresponds to the total energy of the system. **Hamiltonian Neural Networks** (HNNs) [190] were the first to exploit this structure by parameterizing _H_ with a multilayer perceptron and computing the time derivatives of **q** and **p** via automatic differentiation through Eq. (15). Because the architecture enforces Hamilton’s equations exactly, the resulting dynamics conserve energy by construction, produce perfectly time-reversible 

43 

trajectories, and generalize to longer horizons than standard neural network baselines that directly regress state derivatives. 

An alternative formulation is provided by Lagrangian mechanics, where the dynamics follow from the Euler–Lagrange equation: 


with the Lagrangian _L_ ( **q** _,_ **q** ˙ ) = _T − V_ defined as the difference between kinetic energy _T_ and potential energy _V_ . **Lagrangian Neural Networks** (LNNs) [191] parameterize the Lagrangian directly with a neural network and derive the equations of motion through Eq. (16). A key advantage over HNNs is that the Lagrangian formulation does not require canonical coordinates, making it applicable to systems where the transformation to phase-space variables is nontrivial. **Deep Lagrangian Networks** (DeLaN) [192] pursued a complementary approach by decomposing the Lagrangian into separate neural networks for kinetic and potential energy, parameterizing the mass matrix **M** ( **q** ) as a positive-definite neural network output to ensure physical consistency, and demonstrating strong results on robot dynamics identification. 

Subsequent work extended these foundational ideas along several axes. **Symplectic ODE-Net** (SymODEN) [193] combined the Hamiltonian formulation with neural ordinary differential equations [194], learning dynamics from observed state trajectories while enforcing symplectic structure and incorporating control inputs. **Constrained Hamiltonian and Lagrangian Neural Networks** (CHNN/CLNN) [195] showed that embedding systems into Cartesian coordinates and enforcing holonomic constraints explicitly via Lagrange multipliers dramatically simplifies the learning problem, yielding approximately 100 _×_ improvements in accuracy and data efficiency over prior HNN and LNN methods. **Hamiltonian Generative Networks** (HGNs) [196] bridged the gap between physics-conserving dynamics and high-dimensional observations by combining a VAE-like inference network with a Hamiltonian dynamics module, enabling the consistent learning of Hamiltonian dynamics directly from image sequences without restrictive domain assumptions. 

Underpinning many of these models is the **Neural ODE** framework [194], which parameterizes continuous-time dynamics _d_ **h** _/dt_ = _fθ_ ( **h** ( _t_ ) _, t_ ) with a neural network and computes forward trajectories using black-box ODE solvers. Neural ODEs provide memory-efficient training through the adjoint method, constant memory cost regardless of integration depth, and adaptive computation that allocates more solver steps to regions of complex dynamics. When combined with Hamiltonian or Lagrangian structure, Neural ODEs ensure that the learned dynamics respect both the continuous nature of physical time and the conservation laws encoded in the energy function. 

A complementary line of work draws on Koopman operator theory, which seeks a (possibly infinite-dimensional) linear operator that governs the evolution of observables of a nonlinear dynamical system. Li et al. [197] proposed learning **compositional Koopman operators** by integrating Koopman theory with graph neural networks, enabling linear prediction in a learned embedding space while preserving the compositional structure of multi-body systems. This approach achieves efficient long-horizon prediction through simple matrix exponentiation in the lifted space, at the cost of requiring the learned embedding to faithfully linearize the dynamics. 

**Graph neural network-based dynamics simulators.** While physics-conserving models encode conservation laws into the dynamics, a parallel line of research encodes relational structure through graph neural networks (GNNs). The central insight is that many physical systems— collections of particles, rigid bodies, deformable meshes—are naturally described as graphs, where nodes represent entities and edges represent interactions. **Interaction Networks** (INs) [198] introduced the first general-purpose learnable physics engine based on this principle. An IN decomposes a physical scene into objects and pairwise relations, computes interaction effects through learned 

44 

neural network modules, and aggregates these effects to predict per-object state updates. The original work demonstrated accurate prediction of gravitational dynamics, rigid-body collisions, and mass-spring systems, establishing the template for all subsequent GNN-based simulators. 

Battaglia et al. [199] subsequently provided a unified theoretical framework for relational inductive biases in deep learning, formalizing the graph network as a general computational primitive that subsumes INs, message-passing neural networks, and related architectures. This framework clarified how different choices of graph structure, message functions, and aggregation operators encode different physical assumptions, and motivated a series of increasingly powerful simulators. 

**Graph Network-based Simulators** (GNS) [200] scaled the IN paradigm to complex, multimaterial physical domains. By representing the simulation state as a particle graph and applying learned message-passing updates, GNS achieved accurate simulation of fluids, rigid solids, and deformable materials within a single framework, generalizing to particle counts and domain configurations not seen during training. **MeshGraphNets** [201] extended this approach to mesh-based simulation domains such as computational fluid dynamics and structural mechanics, operating on adaptive triangular or tetrahedral meshes rather than particle graphs. By processing the mesh as a graph with learned message-passing, MeshGraphNets achieved one to two orders of magnitude speedup over traditional numerical solvers while maintaining physical accuracy, and received the ICLR 2021 Outstanding Paper Award. 

**Neural Relational Inference** (NRI) [202] addressed the complementary problem of simultaneously inferring interaction structure and dynamics from observational data. Using a variational autoencoder framework where the encoder infers a latent interaction graph and the decoder predicts dynamics conditioned on this graph, NRI learns to discover which entities interact and how, without supervision on the graph structure. **DPI-Net** [203] extended particle-based GNN simulators to manipulation tasks involving rigid bodies, deformable objects, and fluids, demonstrating that learned particle dynamics can support downstream planning for robotic control. Li et al. [204] further showed that such learned physical models can be grounded in visual observations, enabling prediction of physical dynamics directly from images through a perception-to-simulation pipeline. 

**Object-centric world models.** A closely related but distinct research direction decomposes visual scenes into discrete object representations, enabling compositional reasoning about dynamics. The key enabler for this line of work is **Slot Attention** [205], an iterative competitive attention mechanism that decomposes perceptual inputs into a fixed set of exchangeable representation vectors called “slots,” each corresponding to an object or entity in the scene. Slot Attention requires no supervision on object identity or segmentation, instead relying on reconstruction objectives to discover object structure. Its success has established slot-based representations as the de facto standard for unsupervised object discovery in visual world models. 

**SAVi** (Slot Attention for Video) [206] extended Slot Attention to the temporal domain, conditioning slot initialization on the first frame to enable consistent object tracking across video sequences. **Contrastive Structured World Models** (C-SWM) [63] took a different approach, learning object-centric state representations through contrastive learning rather than reconstruction. C-SWM encodes each object as a vector in a structured latent space and models transitions via a GNN operating on these object representations, demonstrating that contrastive objectives can yield physically meaningful latent spaces that support accurate multi-step prediction in environments with multiple interacting objects. 

**SlotFormer** [207] combined slot-based object representations with Transformer-based dynamics prediction, autoregressively predicting future slot states and decoding them into video frames. By operating on object-level tokens rather than pixel patches, SlotFormer achieves strong performance on unsupervised visual dynamics simulation while maintaining compositional generalization to novel object configurations. More recent work has further integrated object-centric representa- 

45 

tions with model-based reinforcement learning. **Object-Centric Dreamer** [208] combines Slot Attention with the RSSM architecture via a GNN-based per-object dynamics model, enabling model-based RL agents to reason about individual objects. **SOLD** (Slot Object-Centric Latent Dynamics) [209] extends this to relational manipulation learning from pixels, using slot representations with learned relational dynamics for robotic control tasks. 

Several additional contributions have expanded the scope of object-centric world models such as **OP3** [210] introduced entity abstraction for model-based planning, learning to decompose scenes into interactable entities. **GENESIS** [211] proposed a generative model that jointly performs scene decomposition and generation, producing spatially disentangled object representations. **DreamWeaver** [212] demonstrated compositional world model learning directly from pixels at scale, while recent work on **STICA** [213] and **FIOC-WM** [214] has explored causality-aware and factored interactive object-centric world models, respectively, incorporating causal reasoning into the object-centric dynamics. 

**Equivariant and symmetry-preserving models.** Physical laws are characterized by symmetries: the laws of motion are invariant to translations, rotations, and reflections of the coordinate system. Standard neural networks do not respect these symmetries, requiring them to learn invariances from data augmentation or large datasets. Equivariant architectures address this by building symmetry directly into the network structure. **E(n) Equivariant Graph Neural Networks** (EGNNs) [215] introduced a GNN architecture that is equivariant to rotations, translations, and reflections in _n_ -dimensional Euclidean space, achieving up to 1000 _×_ improvements in data efficiency on molecular dynamics tasks compared to non-equivariant baselines. EGNNs operate by updating both node features and coordinate positions through message-passing, with the coordinate updates constructed to preserve equivariance by design. 

However, strict equivariance can be counterproductive when external fields break the symmetry of the system. **Subequivariant Graph Neural Networks** (SGNNs) [216] formalized this observation by introducing the concept of subequivariance—a relaxation of full _E_ (3) equivariance to the subgroup of symmetries that are actually preserved by the physical system. For example, a system under gravity is invariant to rotations about the vertical axis and horizontal translations but not to arbitrary 3D rotations. SGNNs demonstrated superior performance over both non-equivariant and fully equivariant models on dynamics prediction tasks involving gravity and other external fields. 

**SEGNO** [217] (Second-order Equivariant Graph Neural ODE) further advanced this line by combining equivariant GNNs with neural ODE integration, enforcing second-order continuity in the learned dynamics. By operating on both positions and velocities and preserving equivariance through the ODE integration, SEGNO achieves more accurate long-horizon prediction for systems governed by second-order differential equations. Recent work on **flow-equivariant world models** [218] has begun to explore how equivariance constraints can be incorporated into broader world model architectures beyond particle systems, extending these principles to latent dynamics models for reinforcement learning. 

**Neuro-symbolic and compositional approaches.** The approaches discussed thus far embed physical structure implicitly through architectural choices. An alternative strategy is to combine neural learning with explicit symbolic reasoning, seeking to recover interpretable physical laws from data. Cranmer et al. [219] demonstrated **symbolic distillation from graph neural networks** , training a GNN-based simulator and then extracting symbolic expressions for the learned interaction functions using symbolic regression. This approach successfully recovered known force laws (e.g., Newtonian gravity, Coulomb’s law) and Hamiltonians from simulation data, and even discovered a novel analytical formula relevant to dark matter dynamics in astrophysics, demonstrating that neural network-based world models can serve as stepping stones toward interpretable scientific discovery. 

46 

**Cosmos** [220] (not to be confused with NVIDIA’s Cosmos platform) proposed neurosymbolic grounding for compositional world models, learning to ground visual observations in symbolic object descriptions and compose dynamics rules from these symbols. This approach achieves strong compositional generalization—the ability to predict dynamics for combinations of objects and interactions not seen during training—by factoring the world model into perception (neural) and dynamics (symbolic) components. **Physics-informed model-based reinforcement learning** (PiMBRL) [121] took a more direct approach, incorporating known physics equations as soft or hard constraints within the world model training loop for model-based RL, demonstrating improved sample efficiency and physical plausibility on control tasks where partial physics knowledge is available. 

The neuro-symbolic direction also intersects with the growing literature on **semantic world models** , which ground dynamics prediction in natural language or symbolic scene descriptions rather than raw pixels. While these approaches are discussed more fully in Section 3.6, they share with physics-informed methods the core insight that structured, interpretable representations can improve generalization and data efficiency relative to monolithic neural dynamics models. 

**Comparative analysis and open challenges.** The five sub-families surveyed in this section share a common thesis: encoding known structural properties of the physical world into world model architectures yields improvements in data efficiency, generalization, and long-horizon stability relative to unstructured approaches. Physics-conserving models (HNN, LNN, and their extensions) excel at eliminating energy drift in long rollouts but require knowledge of the appropriate coordinate system and energy decomposition. GNN-based simulators (IN, GNS, MeshGraphNets) provide a natural framework for relational reasoning over multi-body systems and achieve remarkable speedups over numerical simulation, but their accuracy degrades for contact-rich dynamics involving friction and collision. Object-centric models (Slot Attention, C-SWM, SlotFormer) enable compositional reasoning and generalization to novel object configurations, but unsupervised object discovery remains fragile in visually complex real-world scenes. Equivariant architectures (EGNN, SGNN, SEGNO) offer dramatic data efficiency gains by encoding symmetries, but require careful analysis of which symmetries actually hold in the target domain. Neuro-symbolic approaches achieve the strongest compositional generalization and interpretability but struggle to scale to high-dimensional, continuous-valued observations. 

Several important open challenges cut across all sub-families. First, no existing architecture seamlessly unifies physics conservation, object-centricity, and equivariance within a single framework; combining these complementary inductive biases remains an active research frontier. Second, contact-rich dynamics—involving friction, collision, and deformation—remain difficult for all approaches, as these phenomena introduce discontinuities that violate the smoothness assumptions underlying many physics-informed models. Third, while these methods demonstrate strong results on synthetic benchmarks such as Physion [221] and controlled simulation environments, bridging the gap to real-world deployment with noisy, partial observations remains a significant challenge. Fourth, integrating the structural inductive biases surveyed here with the representational power of foundation-scale models (Section 3.4) represents a promising but largely unexplored direction. Finally, whether physical behavior should be explicitly encoded through architectural constraints or can emerge from sufficient data and scale—the tension between physics-informed and physicsemergent approaches—remains a fundamental open question in the field. 

### **4.5 Language-augmented and multi-modal world models** 

The world model architectures surveyed in the preceding sections—state-space and recurrent latent models, variational and generative approaches, transformer-based systems, diffusion models, and 

47 

physics-informed designs—operate predominantly within visual or low-dimensional state spaces, learning dynamics from pixels, point clouds, or structured physical representations. While these paradigms have proven remarkably effective for environment simulation and policy learning, they share a fundamental limitation: they lack the ability to incorporate the rich semantic and compositional structure that natural language provides. Human cognition, by contrast, routinely integrates linguistic knowledge with perceptual experience to form predictive models of the world—we can imagine what will happen when we “push the red cup off the table” precisely because language supplies abstract relational and causal structure that complements raw sensory prediction [5]. This observation has motivated a rapidly growing body of work that augments world models with language and multimodal inputs, fundamentally altering how these systems represent states, predict transitions, and generalize across tasks. Crucially, the integration of language is not merely an interface convenience; it changes the model architecture, the learning objective, and the nature of the predicted quantities. This section surveys six methodological families that embody different strategies for this integration, focusing throughout on _how_ language and multimodality reshape world model design rather than on specific downstream applications, which are discussed in Section 6. 

**Language-conditioned latent dynamics models.** The most direct approach to incorporating language into world models is to augment existing latent dynamics architectures—particularly the RSSM framework underlying the Dreamer family [40]—with language as an additional conditioning signal. **Dynalang** [120] introduced the foundational insight that language understanding can be unified with future prediction as a single self-supervised objective. Built upon the DreamerV3 RSSM, Dynalang extends the model to accept both image observations and text tokens as input, learning to predict future text and image representations jointly. The key methodological contribution is that language grounding emerges naturally from the dynamics learning objective: the model learns to associate diverse language types—descriptions, instructions, corrections—with their environmental consequences, without requiring explicit language-grounding supervision. This approach demonstrates that the transition function _pθ_ ( _zt_ +1 _| zt, at, lt_ ), where _lt_ denotes a language embedding, can serve as a universal grounding mechanism. 

Subsequent work has explored variations of this language-conditioned dynamics paradigm. **LIMT** [222] leverages pre-trained language models such as Sentence-BERT to extract semantically meaningful task embeddings that condition both the dynamics model and the actor-critic networks, achieving approximately 30% higher success rates than model-free baselines under equivalent sample budgets and enabling zero-shot generalization to novel task descriptions. **LUMOS** [223] extends the paradigm to real-world robotic manipulation by learning a language-conditioned visuomotor policy within the latent space of an offline world model, demonstrating that language-steerable skills learned from fewer than 1% hindsight language annotations can transfer zero-shot to physical robots on the CALVIN benchmark. **LED-WM** [224] takes a complementary approach by conditioning the world model on _environmental descriptions_ rather than task instructions, using an attention mechanism to explicitly ground textual descriptions of dynamics rules to entities in the observation space, thereby improving policy generalization to environments with novel dynamics. Collectively, these methods establish that language conditioning at the latent dynamics level improves sample efficiency, enables compositional task specification, and facilitates transfer across environments—all without fundamentally departing from the RSSM architectural paradigm. 

**Large language models as world models.** A conceptually distinct approach repurposes large language models themselves as world models, leveraging their pre-trained knowledge to simulate state transitions and predict action consequences in text space. The **Reasoning via Planning** 

48 

**(RAP)** framework [139] exemplifies this paradigm by casting the LLM in a dual role: as both a world model that predicts state transitions and a reasoning agent that proposes actions. RAP integrates Monte Carlo Tree Search (MCTS) with the LLM’s predictions, using the world model component to evaluate state transitions while task-specific rewards guide the search. This formulation enabled LLaMA-33B to surpass chain-of-thought prompting on GPT-4 by 33% in plan generation tasks, establishing that the structured exploration afforded by treating an LLM as an explicit world model can substantially outperform sequential reasoning. 

The viability of LLMs as world models has been investigated along multiple axes. Xie et al. [225] demonstrated that LLMs can be fine-tuned to learn PDDL-style precondition and effect knowledge—determining action applicability based on world state and predicting resulting states after action execution—from synthetic data, with human-participant studies confirming alignment with human understanding of world dynamics. In a complementary direction, **GLAM** [226] showed that LLMs can achieve functional grounding through online reinforcement learning in text-based environments, using PPO to progressively update an LLM policy for improved sample efficiency and generalization. 

However, systematic evaluation has revealed fundamental limitations of current LLMs as world simulators. Wang et al. [126] introduced the ByteSized32-State-Prediction benchmark comprising 76,369 state transitions and found that even GPT-4 achieves only 59.9% accuracy on non-trivial transitions, with cumulative accuracy dropping below 1% after ten sequential steps. The identified failure modes—environment-driven transitions, arithmetic reasoning, common-sense physics, and scientific knowledge—suggest that LLMs learn correlational rather than causal models of world dynamics. More recent work by Gkountouras et al. [227] addresses this limitation directly by integrating causal representation learning with LLMs, constructing a framework in which a causal world model with variables linked to natural language expressions serves as a simulator that the LLM can query. This causally-aware approach outperforms pure LLM-based reasoners, particularly for longer planning horizons, pointing toward a productive synthesis between statistical language models and structured causal reasoning. 

**Text-conditioned video generation as world simulation.** A third methodological family transforms video generation architectures into world simulators through language conditioning, raising fundamental questions about whether text-to-video models can constitute genuine world models. **GAIA-1** [62] pioneered this direction with a 9-billion-parameter architecture that casts world modeling as unsupervised sequence modeling over jointly tokenized video, text, and action inputs. The architecture pairs a 6.5-billion-parameter autoregressive transformer with a 2.6billion-parameter video diffusion decoder, demonstrating emergent properties including contextual awareness and geometry understanding in driving scenarios. Text conditioning enables fine-grained control over ego-vehicle behavior and scene composition, establishing the viability of language as a control interface for large-scale generative world models. 

**UniSim** [88] generalized this approach by training a video diffusion model on diverse data spanning internet images, robotics, navigation, and human activity, unifying multiple action modalities— from language instructions to low-level motor controls—through T5 language model embeddings concatenated with discretized control signals. The resulting model supports temporally extended actions in various modalities and enables training vision-language planners and reinforcement learning policies that transfer zero-shot to real robots. **Pandora** [160] introduced a hybrid autoregressivediffusion architecture that uses free-form text as the action space and video as the state space, integrating a pre-trained 7-billion-parameter LLM with a pre-trained video generation model through lightweight fine-tuning. This design enables real-time, language-controllable world simulation across 

49 

diverse domains while generating videos of unlimited duration through autoregressive chaining. 

At industrial scale, NVIDIA’s **Cosmos** [14] released open-weight World Foundation Models at 7B and 14B parameters trained on over 20 million hours of real-world video, integrating text, image, and video conditioning within unified diffusion and autoregressive variants. The subsequent Cosmos-Predict2.5 [108] transitioned to flow-matching with reinforcement learning-based post-training on 200 million clips, while the companion Cosmos-Reason model provides richer text grounding through chain-of-thought reasoning about physical dynamics. The **Large World Model (LWM)** [111] pursued an orthogonal scaling axis by extending context length to one million tokens via RingAttention, enabling joint modeling of long video and text sequences in a unified autoregressive framework. DeepMind’s **Genie** [13] and its successors demonstrated that interactive world models can be built from unlabeled video alone by learning latent action models, with Genie 3 accepting text prompts to generate navigable 3D environments at 24 frames per second. Despite these impressive capabilities, the debate over whether text-conditioned video generation constitutes genuine world modeling remains active: controlled experiments by Kang et al. [107] have shown that such models exhibit case-based generalization—mimicking nearest training examples rather than abstracting physical rules—suggesting that visual fidelity alone does not guarantee causal understanding. 

**Vision-language joint embedding approaches.** In contrast to generative approaches that predict future observations in pixel space, joint embedding predictive architectures learn to predict future _representations_ rather than raw sensory data. LeCun’s **JEPA** framework [5] provides the theoretical foundation for this paradigm, arguing that generative pixel-space prediction wastes model capacity on perceptually irrelevant details and proposing instead that world models should operate by aligning representations of compatible inputs in a shared embedding space. This principle has been operationalized through a series of increasingly capable models. 

**V-JEPA 2** [12], pre-trained on over one million hours of video through self-supervised spatiotemporal representation learning, predicts masked spatio-temporal regions entirely in a learned latent space without any pixel reconstruction. The resulting representations achieve 77.3% top-1 accuracy on Something-Something v2 and, critically for world modeling, can be post-trained for robotic action-conditioned planning on Franka robot arms using fewer than 62 hours of unlabeled robot video. **VL-JEPA** [228] extends the joint embedding principle to the vision-language domain by predicting continuous text embeddings rather than autoregressively generating tokens, achieving competitive performance with 50% fewer trainable parameters (1.6 billion) than classical visionlanguage models while natively supporting open-vocabulary classification, text-to-video retrieval, and visual question answering. This approach demonstrates that JEPA principles extend naturally to multimodal settings, providing an alternative to the cross-attention mechanisms used in generative approaches. 

A related line of work investigates how pre-trained visual foundation models can serve as representation backbones for world modeling. **DINO-WM** [98] builds world dynamics models on compact DINOv2 patch embeddings rather than raw pixels, predicting future patch features from offline behavioral trajectories and achieving zero-shot planning across six environments including mazes, push manipulation, and multi-particle scenarios without requiring reward models or expert demonstrations. While DINO-WM is language-free, its success illustrates a broader methodological point: pre-trained visual representations that encode semantic structure—whether acquired through implicit language alignment during pre-training or through self-supervised objectives— provide a powerful inductive bias for dynamics learning, complementing the explicit language conditioning approaches described above. 

50 

**Semantic world models.** Perhaps the most radical departure from conventional world modeling is the proposal that world models need not predict future observations or latent states at all, but can instead reason directly in language and semantic space. **Semantic World Models (SWM)** [229] reformulate world modeling as visual question answering about the future: given current observations and candidate actions, the model—built upon the PaliGemma 3B vision-language model—directly answers questions about the semantic effects of those actions without generating any pixel-level predictions. A new projection matrix conditions the VLM on actions, enabling both sampling-based planning and gradient-based policy improvement through the model’s differentiable predictions. The results are striking: on the LangTable benchmark, SWM improves success rates from 14.4% to 81.6% through gradient-based optimization, dramatically outperforming pixel-based world models by reasoning in a space that is both lower-dimensional and more directly aligned with task-relevant information. 

**VLWM** [89] extends this paradigm by using natural language as the abstract world state representation for planning. Given visual observations, VLWM first infers overall goal achievements, then predicts a trajectory composed of interleaved actions and world state changes expressed as structured text. The model supports both System-1 reactive planning through a learned action policy and System-2 reflective planning through cost minimization over predicted textual trajectories, with the latter improving Elo scores by 27% over the former. These semantic approaches suggest a provocative thesis: for tasks where the relevant state can be expressed linguistically, bypassing pixel-space prediction entirely may yield both more efficient and more capable world models. The open question is whether this advantage holds for domains requiring fine-grained spatial reasoning, where semantic abstraction may discard information critical for precise manipulation. 

**Unified multimodal architectures.** The approaches described above augment existing architectures with language or replace visual prediction with linguistic reasoning. A final methodological family pursues a more ambitious goal: building end-to-end architectures that natively integrate vision, language, and action within a single world model framework. **WorldGPT** [230] constructs a generalist world model upon a multimodal large language model backbone, acquiring understanding of world dynamics through analyzing millions of videos and incorporating a cognitive architecture combining memory offloading, knowledge retrieval, and context reflection to enhance performance on long-term tasks. **Motus** [125] introduces a Mixture-of-Transformer (MoT) architecture integrating three specialized experts—for understanding, video generation, and action prediction—with a UniDiffuser-style scheduler that enables flexible switching between world model, vision-language-action model, inverse dynamics model, and video generation modes within a single architecture. The use of optical flow as an embodiment-agnostic proxy for actions, compressed into low-dimensional latent codes, enables large-scale action pre-training from unlabeled video, achieving a 45% absolute improvement over prior vision-language-action baselines on the RoboTwin 2.0 benchmark. 

Language compositionality has also been leveraged to improve world model generalization. **RoboDreamer** [185] factorizes video generation through the natural compositionality of language, parsing instructions into lower-level primitives that condition separate models to generate videos compositionally, enabling generalization to unseen combinations of objects and actions. **SuSIE** [231] takes a lightweight approach by using a language-conditioned image editing diffusion model—fine-tuned from InstructPix2Pix on video data—as a world model for subgoal prediction, alternating between high-level image editing and low-level goal-reaching to achieve state-of-the-art performance on the zero-shot CALVIN benchmark. These unified architectures illustrate a broader trend toward treating vision, language, and action as co-equal modalities within a single predictive 

51 

framework, rather than treating language as an auxiliary input to a primarily visual system. 

**Comparative analysis and open challenges.** The six methodological families surveyed above represent fundamentally different answers to the question of how language should participate in world modeling. Language-conditioned latent dynamics models preserve the well-understood RSSM framework while gaining compositional task specification and improved generalization. LLMbased world models offer rich prior knowledge and flexible text-based reasoning but currently lack the causal fidelity required for reliable multi-step simulation. Text-conditioned video generation achieves photorealistic world simulation at scale but faces unresolved questions about whether visual generation implies genuine physical understanding. Joint embedding approaches avoid the computational burden and information-theoretic inefficiency of pixel-space prediction, operating instead in compact representation spaces that may be more suitable for decision-making. Semantic world models bypass visual prediction entirely, reasoning in language space with dramatic efficiency gains for tasks where semantic abstraction suffices. Unified multimodal architectures seek to subsume all modalities within a single framework, though the architectural complexity required to support flexible mode-switching remains a practical challenge. 

Several cross-cutting open problems emerge from this analysis. First, the question of _causal grounding_ remains largely unresolved: most language-conditioned world models learn correlational rather than causal relationships between language and dynamics, and establishing whether a model has truly grounded language to physical consequences—rather than exploiting surface-level statistical regularities—requires new evaluation protocols that go beyond task success metrics [227]. Second, _compositional generalization_ is frequently claimed but rarely demonstrated rigorously; while language provides compositional structure, it remains unclear whether current models achieve systematic generalization to novel combinations of concepts or merely interpolate within training distributions. Third, _long-horizon consistency_ poses a fundamental challenge across all families: maintaining coherent world state predictions over extended text-conditioned rollouts is difficult whether the model operates in pixel space, latent space, or language space. Fourth, the optimal _level of abstraction_ for world model prediction—pixels, latent representations, or semantic descriptions—likely depends on the downstream task, but principled methods for selecting or adapting this abstraction level are lacking. Finally, the _computational cost_ of large-scale language-augmented world models, from Cosmos at 14 billion parameters to LWM at one million token context, presents significant barriers to accessibility and reproducibility, motivating research into efficient architectures that preserve the benefits of multimodal integration at reduced scale. 

## **5 Categorization of World Models by Reasoning Strategy** 

A world model is only as useful as the reasoning it enables. Whereas the previous sections examined how world models are structured (Section 3) and trained (Section 4), this section focuses on how their predictions are used for decision-making. We organize these reasoning strategies into four categories. Imagination-based planning (Section 5.1) uses the model to simulate candidate action sequences and choose promising trajectories through search or optimization. Policy learning with a world model trains a reactive policy within imagined rollouts, reducing reliance on online environment interaction. Counterfactual reasoning (Section 5.3) asks what would have happened under an alternative action, supporting causal analysis and credit assignment. Finally, planning under uncertainty (Section 5.4) addresses imperfect predictions and partial observability, emphasizing robust decision-making under model uncertainty. 

52 

### **5.1 Imagination-based planning** 

A fundamental challenge in intelligent systems is how to reason about future outcomes without relying exclusively on costly interaction with the physical world. Humans routinely address this problem through mental simulation, imagining possible consequences before acting [232]. Inspired by this capability, modern world models increasingly incorporate imagination-based planning, in which agents evaluate hypothetical futures using internal models of environmental dynamics [233]. In world models, imagination can be formalized as trajectory optimization in learned latent dy- 


Figure 2: Imagination-based planning in latent world models. Starting from the current latent state _Zt_ , a learned dynamics model is used to simulate future states in latent space. Multiple candidate actions are evaluated through imagined rollouts, which are scored using a reward predictor and a value function. The selected action is then executed and the process repeats. For clarity, the figure illustrates a simplified branching over actions; in practice, planning is performed over action sequences and rollouts are conditioned on actions at each step. 

namics. Rather than interacting with the environment to evaluate actions, an agent internally constructs and evaluates possible future trajectories, effectively decoupling decision-making from physical experience. This perspective reframes planning as a computational problem: optimizing actions over simulated latent trajectories under a learned transition model. 

Formally, let _zt_ denote the latent representation of the system at time _t_ . Given a candidate sequence of actions _at_ : _t_ + _H_ , the model simulates future latent states over a planning horizon _H_ [31]: 


where _pθ_ is a learned probabilistic transition model. These simulated states are evaluated through task-relevant predictors: 


allowing the agent to estimate long-term consequences entirely within latent space [171]. Crucially, operating in latent space abstracts away high-dimensional perceptual detail while preserving decision-relevant structure, enabling planning to scale beyond raw observation space. 

Despite differences in implementation, existing approaches can be unified under a single principle: decision-making is achieved by optimizing over imagined trajectories. The primary distinction lies in when this optimization is performed. One class of methods amortizes imagination into a parametric policy during training, while another performs explicit optimization at decision time 

53 

through online reasoning. This distinction reflects a fundamental trade-off between amortized computation and on-demand deliberation in intelligent systems [233]. 

#### **5.1.1 Imagination during learning: background planning.** 

In the first paradigm, imagination is primarily used to improve policies during training by generating synthetic experience. Instead of relying solely on real environment interaction, the world model produces large numbers of hypothetical trajectories, which are treated as additional training data for updating policy and value functions [99]. 

Crucially, because the transition dynamics are implemented as differentiable neural networks, gradients of long-term value estimates can be propagated through imagined trajectories via backpropagation through time. This effectively turns imagination into a differentiable computation graph, enabling end-to-end optimization of long-horizon behavior and alleviating the need for explicit multi-step credit assignment from real trajectories. 

Representative methods include **PlaNet** [31] and the **Dreamer family** [40, 171], which learn latent dynamics models and optimize policies entirely within imagined rollouts. These approaches demonstrate that a substantial portion of policy learning can be driven by internally generated experience, leading to significant improvements in sample efficiency compared to model-free reinforcement learning. 

From a broader perspective, this paradigm can be interpreted as amortizing the cost of planning into the training phase: the agent learns a parametric policy that implicitly encodes the outcome of many imagined trajectories, thereby enabling fast decision-making at inference time without explicit search. 

#### **5.1.2 Imagination at decision time: forward search.** 

In the second paradigm, imagination is performed at inference time to guide action selection through online reasoning. Rather than relying solely on a pre-trained policy, the agent expands possible futures from the current state and evaluates their long-term consequences under a learned dynamics model, effectively performing planning on demand [46]. 

This process is typically implemented via search procedures such as **Monte Carlo Tree Search (MCTS)** , where candidate action sequences are iteratively explored and refined based on predicted rewards and value estimates. Representative approaches include **MuZero** [9], **EfficientZero** [102], and **TD-MPC** [46], which integrate learned latent dynamics with search or trajectory optimization to achieve strong performance across a range of decision-making tasks. 

A central concept in this setting is value equivalence [101], which shifts the objective of representation learning from reconstructing observations to preserving decision-relevant quantities such as rewards, values, and policies. As a result, the latent space is shaped to support accurate planning rather than faithful reconstruction, aligning model learning with downstream control objectives. 

Unlike amortized approaches, this paradigm explicitly recomputes optimal actions for each state, trading increased computational cost for improved flexibility and robustness. In particular, online search enables the agent to adapt to out-of-distribution states and recover from model or policy errors by re-evaluating alternative futures at decision time. 

From a broader perspective, this paradigm can be viewed as allocating computational resources to real-time deliberation rather than pre-computation: planning is performed explicitly when needed, allowing the agent to dynamically refine its decisions based on the current context and predicted outcomes. 

54 

#### **5.1.3 Cross-domain advantages of latent imagination.** 

The advantages of imagination-based planning stem from a single underlying property: the decoupling of decision evaluation from physical interaction. By shifting computation from the external environment to an internal latent simulation, physical experience is effectively transformed into an infinitely reusable computational resource. 

First, this decoupling unlocks substantial gains in sample efficiency through data amplification. Because internal rollouts are generated without the temporal and physical bottlenecks of real-world interaction, a single observed trajectory can be expanded into a multitude of imagined futures. This computational parallelization enables significantly faster policy improvement compared to purely model-free approaches. Second, imagination enables safe and risk-free exploration. Since hypothetical trajectories are evaluated entirely within the latent space, agents can safely simulate high-risk, rare, or irreversible outcomes. This eliminates physical consequences during the trialand-error process, which is particularly crucial for safety-critical domains such as robotics and autonomous systems [233]. Third, imagination provides a natural computational substrate for counterfactual and causal reasoning. By fixing the initial latent state and intervening on candidate action sequences, agents can evaluate alternative futures under identical environmental conditions. This elevates the model beyond simple predictive modeling, allowing for causal analysis of decision outcomes through explicit "what-if" queries. 

Ultimately, these advantages are not restricted to classical control settings, but extend broadly to sequential decision-making under uncertainty. From a broader perspective, latent imagination serves as a general-purpose mechanism for transforming observational data into structured predictions over possible futures, thereby seamlessly unifying prediction, planning, and reasoning within a single computational framework. 

#### **5.1.4 Open challenges: compounding errors and objective mismatch.** 

Despite its advantages, imagination-based planning remains fundamentally constrained by imperfections in learned world models. A primary limitation arises from compounding errors, where small inaccuracies in one-step predictions accumulate over successive rollout steps, leading to a progressive divergence between imagined and real trajectories. This phenomenon can be understood as a form of distribution shift: as rollouts extend further into the future, the model is increasingly queried on states that lie outside the support of its training data, resulting in internally consistent yet physically implausible imagined futures. 

A second challenge lies in objective mismatch [106]. Many world models are trained using generative or reconstruction-based objectives, such as predicting observations or short-term signals, which are not necessarily aligned with the requirements of downstream decision-making. Consequently, improvements in predictive accuracy do not always translate into better control performance, revealing a fundamental misalignment between representation learning and decision objectives. Recent approaches such as **SPR** [95] partially address this issue by encouraging task-relevant latent consistency, but a general solution remains elusive. 

Importantly, these two challenges are deeply intertwined: compounding errors are exacerbated when the learned representation fails to preserve decision-relevant structure, while objective mismatch can amplify long-horizon prediction errors by prioritizing perceptual fidelity over controllability. From a broader perspective, this suggests that imagination-based planning is not merely a problem of improving predictive accuracy, but a joint problem of representation learning, dynamics modeling, and decision alignment. 

Addressing these limitations requires advances along multiple axes, including improving long- 

55 

horizon consistency, learning task-aligned latent representations, and developing objectives that explicitly couple model learning with decision-making. More fundamentally, it calls for a shift from viewing world models as passive predictors toward treating them as decision-oriented abstractions optimized for planning and control. 

### **5.2 Policy learning with a world model** 

Reinforcement learning (RL) has achieved impressive results in a wide range of sequential decisionmaking problems. However, its heavy reliance on large-scale environment interaction remains a major limitation, especially in domains where data collection is expensive, slow, or unsafe [234, 235]. This challenge has led to growing interest in model-based reinforcement learning, where an agent learns an internal model of the environment and uses it to support decision-making. Within this broader paradigm, world models have emerged as an important framework for improving sample efficiency and enabling policy learning through internal simulation rather than direct interaction alone [236, 237]. 

A world model generally consists of two closely related components: a representation model and a dynamics model [11, 238]. The representation model maps high-dimensional observations into a compact latent state, while the dynamics model predicts how this latent state evolves under the effect of actions. In many formulations, the model may also predict rewards and termination signals, so that imagined trajectories can be used not only for forecasting future states but also for evaluating candidate decisions. The role of this design is not limited to dimensionality reduction. More importantly, it defines a predictive latent space in which policy learning or planning can be carried out more efficiently than in the original observation space. 

Once such a model is learned, the main question becomes how it should be used for control. In other words, the key issue is not only whether the model can represent the environment accurately, but also how imagined trajectories contribute to policy optimization. Existing methods differ mainly in this respect. Broadly speaking, policy learning in world model-based RL can be organized into three major approaches: model-generated data augmentation, latent imagination for actor-critic learning, and gradient-based optimization through differentiable dynamics [239, 240]. 

The first approach uses the learned model to generate synthetic transitions that supplement real experience. This idea can be traced back to early work such as Dyna-Q [241], where real interaction and model-based updates are interleaved during learning. In modern model-based RL, this strategy often appears in a more controlled form: the agent performs short imagined rollouts from states sampled from a replay buffer and then uses the resulting transitions for value or policy updates. Methods such as MBPO [103] are representative of this line of work. Rather than relying on longhorizon simulations, MBPO limits model rollouts to short segments in order to reduce the effect of compounding errors while still improving data efficiency. Related methods such as STEVE [100] further explore how uncertainty-aware model rollouts can be incorporated into target estimation. The strength of this family of methods lies in its relative conservatism: the model is used to expand training data, but policy learning is not placed entirely at the mercy of long imagined trajectories. 

A second line of work performs policy learning directly in latent imagination. In this setting, the world model is not merely a source of additional synthetic transitions; instead, imagined latent trajectories become the main medium through which policy evaluation and improvement are carried out. PlaNet [242] is an important early example of this direction, showing that compact latent dynamics can support planning directly from image observations. The Dreamer family [243, 244] extends this idea further by combining learned latent dynamics with actor-critic learning. After fitting a latent world model from real experience, Dreamer rolls forward imagined latent trajectories and uses them to train value and policy networks entirely in latent space. This approach offers 

56 

two advantages. First, policy optimization becomes computationally efficient because it avoids repeatedly reconstructing high-dimensional observations. Second, the representation and control components become more tightly connected, since the latent state must preserve information that is useful not only for prediction, but also for reward estimation and long-horizon decision-making. For this reason, latent imagination methods place particularly strong demands on representation quality. 

A third approach takes advantage of differentiability in the learned dynamics and performs policy optimization through analytic gradients. In model-free RL, policy gradients are typically estimated through likelihood-ratio methods or actor-critic approximations, both of which may suffer from high variance. By contrast, if the learned transition model is differentiable, one can backpropagate reward-related signals through imagined trajectories and directly update policy parameters. This general idea is reflected in work on Stochastic Value Gradients (SVG) [245], which showed that a learned stochastic dynamics model can be used to propagate gradients through trajectories for policy learning. Such methods are especially attractive in continuous control, where actions and latent transitions are naturally amenable to end-to-end differentiation. At the same time, they are highly sensitive to model fidelity. If the learned dynamics become inaccurate in regions visited by the policy, then the resulting gradients may guide the policy toward behaviors that are effective only inside the model rather than in the true environment. 

Although these three approaches are closely related, they make different assumptions about how the model should support control. Data augmentation methods use the model mainly as a provider of additional experience and therefore tend to be more conservative. Latent imagination methods rely more directly on imagined trajectories during policy optimization and thus require stronger latent representations. Gradient-based methods go even further by allowing the internal structure of the model itself to shape policy updates, which can be highly efficient but also more vulnerable to model errors. As a result, the value of a world model cannot be judged independently of the policy learning mechanism built upon it. 

An important point, however, is that not all world models are designed around observation reconstruction. Much of the literature on latent imagination, including PlaNet and Dreamer, learns latent states that remain closely tied to reconstructive or predictive modeling of the environment. By contrast, decision-oriented models such as MuZero [246] take a different route. MuZero does not aim to reconstruct raw observations; instead, it learns a latent dynamics model sufficient for predicting task-relevant quantities such as reward, value, and policy-related transitions. This distinction is conceptually important for a survey of policy learning. It suggests that, from the perspective of control, a useful world model need not reproduce every detail of the external world. In some cases, it may be more effective to model only the aspects of dynamics that matter for decision-making. 

Despite the promise of these methods, policy learning with world models faces several persistent challenges. One of the most important is compounding error. Even if one-step prediction error appears small, small inaccuracies may accumulate over multiple imagined steps and distort long-horizon return estimates. This becomes especially problematic when the policy is trained on imagined trajectories, because the policy may adapt to flaws in the learned model rather than to the true environment. In extreme cases, the agent discovers trajectories that achieve unrealistically high reward under the model but fail when executed in the real environment. This phenomenon is often described as model exploitation and remains a central concern in world model-based RL. 

A related challenge is the mismatch between the objective used to train the world model and the requirements of downstream control. A model that performs well under reconstruction or prediction metrics does not necessarily provide the most useful representation for policy learning. For example, it may preserve visually rich but task-irrelevant details while failing to represent 

57 

reward-critical structure. This problem helps explain why policy learning performance does not always correlate with prediction quality in a straightforward way. It also motivates the growing interest in task-aware latent representations and decision-oriented world modeling, as illustrated by the contrast between reconstructive latent models and approaches such as MuZero. 

To mitigate these problems, several practical strategies have been proposed. One common approach is to use short-horizon rollouts so that model-generated errors do not have time to accumulate excessively [247]. Another is uncertainty-aware modeling, often implemented through ensembles or probabilistic dynamics models, which helps identify when imagined trajectories are less trustworthy [248]. Multi-step consistency objectives, such as latent overshooting, have also been introduced to improve long-horizon prediction quality. In addition, some work explores discrete or otherwise structured latent spaces in order to reduce the tendency of policies to exploit unrealistic details of continuous latent representations. Although these methods differ in form, they are all motivated by the same core requirement: policy learning must remain robust even when the learned model is imperfect. 

The relevance of this problem becomes even clearer in the setting of Offline RL. Because the agent can no longer interact with the environment to correct its mistakes, it must rely entirely on a fixed dataset and whatever inductive support is provided by the learned model. In this context, world models can offer an important mechanism for policy evaluation, imagined rollout, or constrained policy improvement. At the same time, offline settings also make model bias more dangerous, since erroneous imagined trajectories cannot be corrected through further exploration. For this reason, the relationship between world models and offline RL has become an active area of recent research. 

Recent work has also explored more expressive sequence models for world modeling, especially transformer-based architectures [249]. Compared with recurrent dynamics models, transformers are often better at capturing long-range temporal dependencies and complex sequential structure, which may improve latent prediction and imagined rollout quality. This trend has broadened the design space of world model-based RL, particularly in domains that require longer memory or richer sequence understanding. More generally, the field is moving toward increasingly reusable predictive models that can support policy learning across multiple tasks instead of being trained from scratch for a single environment. From the perspective of policy learning, this shift is significant because it points toward a future in which control policies are learned on top of more general latent dynamics models rather than task-specific simulators alone. 

In summary, world models provide a promising framework for reinforcement learning by shifting part of the learning process from direct environment interaction to internal simulation. Their role in policy learning is not limited to improving sample efficiency. They also introduce new mechanisms for control, including model-generated updates, latent imagination, and gradient-based optimization through differentiable dynamics. At the same time, the success of these methods depends critically on whether the learned model captures the aspects of the environment that are relevant for decision-making, and whether policy optimization can remain robust to model bias. For this reason, policy learning in world model-based RL is best understood not simply as an extension of model-free RL, but as a distinct framework in which representation learning, dynamics modeling, and control are deeply intertwined. 

### **5.3 Counterfactual reasoning** 

Counterfactual reasoning represents a fundamental shift in the role of world models, transforming them from predictive simulators into causal reasoning systems. While conventional world models estimate future trajectories conditioned on observed states and actions [4, 31], counterfactual rea- 

58 

soning addresses a qualitatively different question: given an observed trajectory, what would have occurred under an alternative decision at some past time step? This formulation aligns with the highest level of Pearl’s ladder of causation, moving beyond association and intervention toward reasoning about alternative histories [250]. 

In the context of world models, counterfactual reasoning can be formalized as latent-conditioned re-simulation under intervention. Unlike standard forward rollouts, which propagate dynamics from arbitrary states, counterfactual queries must remain anchored to the specific latent conditions that generated the observed trajectory. As a result, counterfactual reasoning requires not only forward prediction, but also reconstruction of the latent causal factors underlying past observations. 

#### **5.3.1 The abduction–action–prediction pipeline.** 

The computation of counterfactuals follows the classical abduction–action–prediction paradigm in causal inference [251], which can be formalized as: 


The first term corresponds to abduction, where the model infers not only the latent state but also the underlying exogenous noise (unobserved environmental randomness) that generated the specific observed trajectory. This step is inherently underdetermined: multiple latent configurations may explain the same observations, introducing ambiguity into the inferred causal state. In world models, this ambiguity is particularly pronounced, as the representation must simultaneously support accurate forward prediction and encode the precise causal context required for valid interventions.The second term represents the intervention, replacing the factual action with a counterfactual alternative while preserving the inferred latent context. Unlike standard policy evaluation, this operation explicitly enforces a _do_ -operator semantics, ensuring that only the specific causal mechanism associated with the action is modified, while all other environmental factors remain rigidly fixed.The third term performs prediction, rolling the system forward under the modified dynamics [171]. Notably, this rollout must remain strictly consistent with both the inferred latent state and the intervened action, placing strong requirements on the stability and causal fidelity of the learned transition model. 

Crucially, both factual and counterfactual trajectories share the exact same inferred latent state at time _t_ , differing only in the intervened action. Counterfactual reasoning is therefore not a naive re-simulation from arbitrary states, but a causally conditioned rollout that strictly isolates the effect of decision changes under identical latent circumstances. 

Ultimately, the abduction–action–prediction pipeline reveals that counterfactual reasoning is fundamentally a problem of disentangling inference, intervention, and prediction within a shared latent space. The reliability of counterfactual conclusions therefore depends not only on predictive accuracy, but critically on the identifiability and causal structure of the learned representation. 

#### **5.3.2 Why counterfactuals matter: isolating decision effects.** 

The core value of counterfactual reasoning lies in its unique capacity to isolate the causal contribution of decisions. While standard predictive models can forecast outcomes conditioned on observed trajectories, they inherently fail to attribute responsibility to specific actions. Counterfactual reasoning overcomes this by enabling the direct comparison of alternative decisions under strictly identical latent conditions, thereby definitively disentangling the true effects of an action from the underlying environmental dynamics. 

59 

In the context of offline reinforcement learning—where online interaction is typically limited or unsafe [233]—counterfactual world models empower agents to reinterpret historical trajectories. By estimating how different actions would have altered long-term returns [252], this approach effectively transforms static observational datasets into a rich substrate for causal evaluation, facilitating robust policy improvement without requiring further environment interaction. 

Beyond policy optimization, this capability is paramount in safety-critical domains such as autonomous driving and medical decision-making [253]. In these environments, determining whether an adverse outcome could have been prevented is just as critical as predicting its occurrence. Here, counterfactual reasoning underpins accountability, risk analysis, and decision auditing, fundamentally elevating the role of world models from mere prediction to causal explanation. 

Ultimately, counterfactual reasoning serves as a critical complement to imagination-based planning by introducing a causal interpretation layer over simulated trajectories. While imagination proactively explores potential futures, counterfactuals retroactively explain realized outcomes by identifying how alternative interventions would have reshaped them. Together, they establish a dual perspective on decision-making, seamlessly unifying forward-looking prediction with backwardlooking causal attribution within a cohesive world modeling framework. 

#### **5.3.3 Toward causally structured world models.** 

Reliable counterfactual reasoning imposes stringent requirements on representation structure. A latent state that is strictly sufficient for forward prediction is not necessarily suitable for counterfactual analysis unless it admits a modular causal decomposition. In conventional latent-variable models with entangled representations, intervening on a single action can inadvertently induce widespread and unstructured changes across the latent space. This violates a core tenet of causal inference: interventions should remain strictly localized, affecting only their specific downstream mechanisms. 

This limitation exposes a fundamental gap between predictive sufficiency and causal adequacy. Representations optimized purely for reconstructing observations or minimizing prediction error frequently fail to preserve the modular structure necessary for valid interventions [254, 255]. Consequently, true counterfactual reasoning demands more than just an accurate dynamics model; it necessitates a representation space inherently designed to support the localized and interpretable manipulation of isolated causal factors. 

To bridge this gap, recent approaches increasingly integrate structural causal models (SCMs) into the design of world models, actively enforcing representations that respect causal modularity [256]. A central objective in this pursuit is causal disentanglement—specifically, the separation of variables directly influenced by agent actions from those governing the broader, autonomous environment [257, 258]. This directly operationalizes the independent causal mechanisms (ICM) principle [259], which posits that the generative process of an environment should be factorized into independent, composable components that do not mutually interfere upon local intervention. 

Under such causally structured representations, counterfactual interventions manifest as precise, localized modifications of specific mechanisms, rather than arbitrary and unpredictable perturbations of a monolithic latent space. Ultimately, this paradigm shift dictates that future world models must evolve beyond serving merely as compact predictive encodings. Instead, they must function as causally structured representations, where the very geometry of the latent space faithfully reflects the true underlying factorization of the environment’s dynamics. 

60 

#### **5.3.4 Fundamental limits: non-identifiability and counterfactual validity.** 

Despite its profound conceptual appeal, counterfactual reasoning in world models faces formidable foundational challenges. From a theoretical perspective, the core bottleneck lies in non identifiability the well-documented phenomenon where multiple distinct latent dynamics models can perfectly explain the observed factual data while yielding entirely divergent counterfactual predictions [260]. Consequently, achieving mere observational accuracy is fundamentally insufficient to guarantee counterfactual validity. 

From a practical standpoint, counterfactual queries inherently risk pushing models into outof-distribution (OOD) regimes. This vulnerability is particularly acute when the proposed counterfactual action deviates significantly from the data-collecting behavioral policy [48]. In such extrapolation scenarios, model rollouts may remain internally coherent yet causally fallacious—a critical failure mode termed counterfactual hallucination [106]. More fundamentally, this exposes a severe vulnerability under distribution shift: predictive accuracy and counterfactual correctness can easily become uncoupled, laying bare the inherent limitations of relying solely on standard generative training objectives. 

Addressing these formidable bottlenecks requires advancing far beyond merely scaling up predictive models. It necessitates the integration of stronger causal structural priors, the development of uncertainty-aware inference mechanisms capable of flagging OOD interventions, and the creation of rigorous evaluation protocols explicitly designed to assess causal reliability rather than just reconstruction loss. Ultimately, the realization of trustworthy counterfactual world models demands representations that do more than passively reproduce observed histories; they must reliably and consistently support grounded reasoning about alternative realities. 

### **5.4 Planning under uncertainty** 

A world model is only as useful as the decisions it enables. Because learned dynamics models are inevitably imperfect—trained on finite data and approximating complex physical processes—every plan derived from such a model is subject to uncertainty. Two distinct sources contribute. _Aleatoric_ (environmental) uncertainty arises from inherently stochastic transitions: the same action applied in the same state may produce different outcomes due to sensor noise, unobserved variables, or genuine randomness in the environment. _Epistemic_ (model) uncertainty stems from the learner’s incomplete knowledge: regions of the state–action space that are poorly covered by training data yield unreliable predictions. Effective planning must account for both. 

**Stochastic dynamics and distributional rollouts.** The most direct approach encodes aleatoric uncertainty into the world model itself. The RSSM [31] maintains a stochastic latent variable _zt_ sampled from a learned prior at each step, so that multi-step rollouts naturally produce a _distribution_ over future trajectories rather than a single deterministic path. DreamerV2 [34] replaced Gaussian latents with discrete categorical distributions, improving the model’s ability to represent multi-modal outcomes (e.g., a pedestrian turning left or right). DreamerV3 [40] extended this with symlog-transformed predictions and categorical value heads, ensuring that the actor– critic trained on imagined rollouts remains calibrated across domains with vastly different reward magnitudes. In these systems, the policy is optimized with respect to the _expected_ return under the model’s stochastic dynamics, implicitly averaging over aleatoric uncertainty. 

**Ensemble-based epistemic uncertainty.** Epistemic uncertainty is harder to capture because a single neural network tends to be overconfident on out-of-distribution inputs. Ensembles of world models offer a practical remedy. PETS [45] trains an ensemble of probabilistic neural networks, each predicting a Gaussian distribution over next states, and plans using trajectory sampling across 

61 

ensemble members. The _disagreement_ among ensemble predictions serves as a proxy for epistemic uncertainty: high disagreement signals that the model is extrapolating beyond its training data. Plan2Explore [261] exploited this signal directly, using ensemble disagreement as an intrinsic reward to drive exploration toward states where the world model is most uncertain—a strategy that learns task-agnostic world models which can be rapidly adapted to new objectives. MBPO [48] used an ensemble to determine a trust horizon: the policy trains on imagined rollouts only up to the horizon beyond which model predictions become unreliable, then falls back to real data. This adaptive truncation prevents the policy from exploiting inaccurate long-horizon predictions. 

**Pessimistic and conservative planning.** In offline settings—where the agent must learn entirely from a fixed dataset without further environment interaction—optimistic exploitation of model inaccuracies is particularly dangerous, because the agent cannot collect corrective data. MOPO [103] penalizes the reward of imagined transitions by a term proportional to the ensemble’s predictive uncertainty, encouraging the policy to avoid state–action regions where the model is unreliable: 


where _u_ ( _s, a_ ) quantifies uncertainty (typically the maximum standard deviation across ensemble members) and _λ_ controls the degree of conservatism. MOReL [262] takes a more aggressive approach, terminating imagined rollouts entirely when the model detects that the agent has left the support of the offline data. RAMBO-RL [263] formulates the problem as a two-player game between the policy and an adversarial dynamics model, training the model to minimize policy performance within a constrained set of plausible dynamics. This adversarial framing provides worst-case robustness without requiring explicit uncertainty quantification. 

**Safe planning under learned dynamics.** Safety-critical applications impose hard constraints that the agent must satisfy even when the world model is wrong. García and Fernández [264] surveyed the landscape of safe RL, distinguishing between methods that modify the optimization criterion (risk-sensitive objectives) and those that constrain the policy’s admissible set. In the world-model setting, As et al. [265] proposed Bayesian world models for constrained policy optimization: a Gaussian process dynamics model provides calibrated uncertainty bounds, and the policy is optimized to maximize return while satisfying probabilistic safety constraints derived from these bounds. In autonomous driving, world models are used to simulate rare but dangerous scenarios (collisions, sudden braking, adverse weather) that are underrepresented in training data, enabling stress-testing of planning systems against tail events that would be impractical or unethical to reproduce in the real world [62, 133]. In medical decision-making, the consequences of model error can be severe; MeWM [135] incorporates an inverse dynamics model that evaluates the predicted outcomes of treatment plans, providing a feedback loop that mitigates the risk of acting on inaccurate simulations. 

**Disentangling controllable and uncontrollable dynamics.** Not all uncertainty is equal from a planning perspective. Some variation in future states is a direct consequence of the agent’s actions (controllable), while other variation is driven by exogenous factors beyond the agent’s influence (uncontrollable)—the behavior of other vehicles, stochastic weather, or unseen patient physiology. Iso-Dream [266] explicitly separates controllable and noncontrollable visual dynamics within the world model’s latent space, enabling the planner to focus on aspects of the future it can influence while treating the rest as noise to be robust against. This decomposition is particularly relevant for multi-agent environments such as urban driving, where the ego agent’s plan must be robust to the unpredictable actions of surrounding actors. 

Despite the progress outlined above, several challenges remain. First, calibration—ensuring that model uncertainty estimates are neither overconfident nor excessively conservative—remains 

62 

difficult for deep neural networks, and miscalibrated uncertainty directly translates into suboptimal or unsafe plans. Second, the computational cost of ensemble-based methods scales linearly with ensemble size, making them expensive for large-scale world models with billions of parameters. Third, there is no unified framework that jointly addresses aleatoric uncertainty, epistemic uncertainty, and hard safety constraints within a single planning algorithm; current methods typically handle one or two of these concerns in isolation. Finally, the interaction between long-horizon compounding error and uncertainty quantification is poorly understood: as rollout horizons increase, the distinction between model error and genuine stochasticity blurs, and current uncertainty estimators struggle to decompose the two. 

## **6 Categorization of World Models by Application Domains** 

This section surveys nine major application areas, moving roughly from the most established to the most emerging. Robotics (Section 6.1) and autonomous driving (Section 6.2) remain core settings for world model research, where latent dynamics models have shown strong gains in sample efficiency and sim-to-real transfer. Video prediction and scene understanding extend these models to forecasting visual futures, while multimodal and language-grounded agents use foundation models as implicit world simulators for embodied decision-making. Reinforcement learning and games (Section 6.5) continue to serve as key testbeds for new architectures. We then examine newer applications in scientific and domain-specific modeling (Section 6.6), medical imaging and clinical decision-making (Section 6.7), educational measurement (Section 6.8), and business and finance (Section 6.9), where world models are being adapted beyond the physical environments in which they first emerged. 

### **6.1 Robotics** 

Robotics is one of the most demanding application domains for world models because prediction quality is ultimately judged by physical execution rather than simulator return alone. Unlike agents acting in relatively clean discrete environments, robotic systems must cope with continuous kinematics, contact discontinuities, partial observability caused by occlusion and sensor noise, and the potentially irreversible consequences of a bad prediction. In this setting, world models are attractive for at least three reasons: they can reduce the cost of real-world data collection by supporting synthetic rollouts in latent or pixel space, enable counterfactual evaluation of candidate action sequences before physical commitment, and learn transferable representations of object and scene dynamics that generalize across tasks and embodiments. Recent surveys frame this landscape from complementary perspectives. Li et al. [28] review robotic manipulation through the joint lenses of perception, prediction, and control, while Li et al. [1] propose a broader taxonomy based on functionality, temporal modeling, and spatial representation. Consistent with those reviews, this subsection keeps robotics as the application focus while organizing the discussion using several recurring technical families: latent dynamics models, self-supervised predictive architectures, generative world simulators, and structured or object-centric models. Table 3 summarizes representative examples. 

**Latent Imagination for Robot Learning.** The most direct application of world model principles to physical robotics is the use of latent dynamics models: learned simulators that compress sensory observations into compact state representations and roll out imagined futures for policy improvement. This paradigm, rooted in the Recurrent State-Space Model (RSSM) used by 

63 

Table 3: Representative world models in robotics, organized by paradigm. Real Robot indicates evaluation on <u>physical</u> hardware beyond simulation. 

|**Model**|**Year**|**Paradigm**|**Key Contribution**|**Real**|
|---|---|---|---|---|
|DayDreamer [83]|2022|Latent dynamics|RSSM on 4 physical platforms|✓|
|I-JEPA [39]|2023|Predictive/JEPA|Masked image representation||
|UniSim [88]|2023|Generative sim.|Universal generative simulator|✓|
|TD-MPC2 [267]|2023|Latent dynamics|Latent MPC + value learning||
|V-JEPA [268]|2024|Predictive/JEPA|Masked video representation||
|DreMa [269]|2024|Structured / 3D|Compositional digital twin||
|RoboDreamer [64]|2024|Latent dynamics|Compositional language goals||
|DINO-WM [270]|2025|Predictive/JEPA|Frozen DINOv2 + zero-shot MPC||
|RWM [237]|2025|Latent dynamics|Dual-autoregressive offline MBRL||
|V-JEPA 2 [12]|2025|Predictive/JEPA|1.2B param. action-conditioned MPC||
|COSMOS [14]|2025|Generative sim.|720p video diffusion, 20M hrs||
|UWM [271]|2025|Generative sim.|Unified video + action diffusion||
|Cosmos Policy [272]|2026|Generative sim.|Video model adapted into policy|✓|
|PointWorld [273]|2026|Structured / 3D|3D point-flow world modeling|✓|


the Dreamer family [6, 7], factorizes the latent state into a deterministic recurrent component _ht_ = _fθ_ ( _ht−_ 1 _, zt−_ 1 _, at−_ 1) and a stochastic component _zt ∼ qϕ_ ( _zt | ht, xt_ ). In robotics, that factorization is attractive because it offers a tractable way to model both predictable motion and harder-to-predict contact events while training policies largely through imagined rollouts rather than repeated physical trials. For example, DayDreamer [83] demonstrated latent imagination on real robots—wheeled, quadruped, arm, and dexterous platforms—showing that it remains effective despite noise, delays, and irreversibility, not just in simulators. RoboDreamer [64] builds on this by factorizing language instructions into reusable primitive skills with latent goal embeddings, enabling novel task compositions at test time. 

A second important direction is offline deployment, where policies must be trained from precollected datasets rather than through repeated online interaction. **RWM** [237] models this setting with a dual-autoregressive design and a self-supervised consistency objective aimed at improving long-horizon rollouts under dataset bias and partial observability. Its uncertainty-aware extension, **RWM-U** [274], further propagates epistemic uncertainty during rollout and couples the world model to uncertainty-penalized policy optimization, making the method substantially more robust on offline real-robot settings than earlier offline MBRL baselines. A complementary design is represented by **TD-MPC2** [267], which couples a latent dynamics model to short-horizon planning and value learning. Rather than using the model only for imagination-based policy training, TDMPC2 uses it directly at decision time, illustrating how latent world models in robotics now span both imagination-heavy RL and tightly integrated planning-and-control pipelines. 

**Self-Supervised Predictive Architectures.** A parallel and increasingly influential line of work develops predictive models in representation space rather than by reconstructing pixels, following LeCun’s Joint-Embedding Predictive Architecture (JEPA) framework [5]. Strictly speaking, some members of this family originated as general visual representation learners rather than robotspecific world models. They are nevertheless relevant here because later robotic planning systems directly build on their predictive abstractions, and because they make explicit a key design claim for robotics: prediction in an abstract latent space may be a better use of model capacity than reconstructing every texture, shadow, and background detail in the scene. 

Building on this principle, I-JEPA [39] showed that predicting latent representations of masked 

64 

image regions produces semantically meaningful features without pixel reconstruction, providing a foundation for action-conditioned planning. V-JEPA [268] extended latent prediction to video, masking and predicting spatiotemporal regions to bridge passive visual pretraining with active control. DINO-WM [270] made this bridge explicit for robotics, combining a frozen DINOv2 encoder with an action-conditioned transition model, enabling offline training and planning entirely in latent space. Finally, V-JEPA 2 [12] scaled these ideas to a 1.2B-parameter video model with action conditioning, demonstrating that large-scale latent video pretraining can support robotic manipulation planning without pixel-level generation. Collectively, these works highlight that effective robotic world models need not be photorealistic, as long as latent predictions preserve task-relevant structure. 

Table 4: Comparison of self-supervised predictive world model architectures (JEPA family) for robotics. Offline indicates the model can be trained on pre-collected trajectories without environment interaction. Zero-shot indicates test-time <u>generalization</u> without <u>per-task</u> fine-tuning. 

|**Model**|**Input**|**Encoder**|**Action-Cond.**|**Offline**|**Zero-shot**|
|---|---|---|---|---|---|
|I-JEPA [39]|Image|ViT (learned)|×|✓|×|
|V-JEPA [268]|Video|ViT (learned)|×|✓|×|
|DINO-WM [98]|Image|DINOv2 (frozen)|✓|✓|✓|
|V-JEPA 2 [12]|Video|ViT-H (learned)|✓|✓|✓|


**Generative World Simulators for Robotics.** A third paradigm treats the world model as a generative simulator that produces action-conditioned video rollouts for planning, policy learning, or synthetic data generation. The core appeal is straightforward: a visually faithful, actionconditioned simulator can partially bridge the gap between abundant unlabeled video and scarce robot demonstrations, while providing a controllable testbed for counterfactual evaluation prior to real deployment. 

Early work in this direction, exemplified by UniSim [88], demonstrated that a single generative model trained on heterogeneous sources—robot demonstrations, human videos, and simulated trajectories—can serve as more than a passive predictor. It can act as a substrate for training planners and policies that subsequently transfer to physical robots. This insight motivates a key architectural question: how should video generation and action modeling be coupled? Unified World Models (UWM) [271] address this by jointly diffusing over video and actions within one backbone, allowing action-free video to contribute to the same pretrained representation as actionlabeled robot data—a practically important property given the relative scarcity of high-quality demonstrations. 

Scale and generality push this line further. COSMOS [14] pretrains on massive video corpora as a broad prior over physical dynamics, treating task-level adaptation as a lightweight downstream step. Its companion Cosmos-Transfer1 [275] targets sim-to-real transfer specifically, translating simulated trajectories into more photorealistic videos while preserving scene structure and motion. Cosmos Policy [272] goes a step further by collapsing the classical separation between world model and policy: future observations, values, and actions become jointly learnable outputs of one pretrained video backbone, blurring the boundary between prediction and control. 

A complementary axis of variation concerns what the simulator predicts. Rather than generating 2D video, PointWorld [273] operates in 3D point-flow space, predicting scene motion directly from RGB-D observations and candidate actions. This is especially appealing for manipulation, where interactions are more naturally described by spatial displacement than by image synthesis, 

65 

and where tying the model to geometry facilitates embodiment transfer. At a different level of abstraction, GenSim2 [276] and RoboGen [277] leverage large language models to automatically generate diverse task curricula, reward functions, and training environments, using generative rollouts for policy evaluation without real data collection. Together, these approaches illustrate that the value of a world simulator need not be confined to policy execution: it can also substantially reduce the human engineering effort required to construct generalizable training pipelines. 

**Structured and Object-Centric World Models.** Manipulation problems typically depend on a small number of entities whose identities, poses, affordances, and pairwise relations determine success or failure. Representing the entire scene as a monolithic latent vector obscures precisely this relational structure, motivating a class of models that instead maintain explicit decomposition over objects and their interactions. 

One influential route combines slot-based perceptual decomposition [278] with graph-style relational reasoning over object tokens. The robotics motivation is practical: preserving object-level state and pairwise geometry yields better extrapolation in contact-rich settings and supports combinatorial generalization to unseen configurations—both failure modes that flat scene representations handle poorly. 

DreMa [269] frames this idea as a learnable digital twin, coupling explicit world structure to imagination and planning so that predicted states remain geometrically consistent with what the robot can physically execute. This matters especially in contact-rich manipulation, where small errors in relative geometry accumulate rapidly and tend to dominate failure modes. 3D-VLA [279] pursues a complementary angle by grounding reasoning and action generation in point clouds rather than 2D observations, gaining a more direct handle on occlusion, viewpoint change, and spatial arrangement. Together, these works converge on a shared lesson: robotic world models tend to benefit from inductive biases about objects, geometry, and interaction structure rather than from undifferentiated scene-level latents alone. 

**World Models for Sim-to-Real Transfer.** The sim-to-real gap remains one of the most practically significant obstacles in robot learning. Its sources are multiple and interacting: contact dynamics differ from reality in stiffness, friction, and damping; visual appearance diverges in lighting, material reflectance, and sensor noise; and subtle mismatches in interactive dynamics accumulate into large trajectory deviations at deployment. World models address this challenge from two complementary directions—generating realistic training data that narrows the domain gap at the input level, and learning representations that abstract away distributional variation irrelevant to task execution. 

The more direct route is appearance transfer: a generative model translates simulated trajectories into visually realistic videos while preserving scene geometry and motion, as in COSMOSTransfer1 [275]. A related strategy expands task diversity rather than visual realism alone— GenSim2 [276] uses LLM-generated tasks, assets, and scenarios to increase coverage over the variation that most often breaks sim-trained policies at deployment. 

The second direction operates at the representation level. Models such as V-JEPA [268] and DINO-WM [270] predict in latent space rather than reconstructing pixels, naturally deemphasizing low-level texture and lighting while preserving geometric and semantic structure more relevant to control. This helps explain why latent predictive models often transfer better than their visual fidelity alone would suggest. 

66 

**Benchmarks and Evaluation.** Evaluation in this area spans standardized simulation benchmarks and increasingly common physical hardware trials, reflecting growing emphasis on real-world validation. A persistent challenge is the evaluation validity gap: high simulation performance often fails to predict real-robot success, motivating benchmarks specifically designed to measure sim-toreal correlation. 

On the simulation side, the DeepMind Control Suite [280] remains standard for continuouscontrol sample efficiency, while RLBench [281] provides 100 manipulation tasks with demonstrations for evaluating world-model-based planning and imitation learning, and Meta-World [282] stresses multi-task transfer across 50 tasks. For real-robot evaluation, the Open X-Embodiment dataset [116]—over one million trajectories across 22 embodiments—has become central for measuring representation and policy transfer across morphologies. SimplerEnv [283] occupies a distinct niche: designed explicitly to improve correspondence between simulation scores and real-robot outcomes, it is particularly useful for testing whether simulated progress is likely to survive deployment. 

### **6.2 Autonomous driving and control systems** 

Autonomous driving represents one of the most mature and commercially motivated application domains for world models, driven by the need to ensure safe navigation in open-world environments that are inherently unpredictable, high-dimensional, and safety-critical. Unlike laboratory-scale robotic manipulation, autonomous driving operates at the intersection of real-time perception, multi-agent interaction, regulatory compliance, and physical dynamics—making predictive simulation and counterfactual reasoning not merely convenient but operationally essential. A survey dedicated to this intersection is provided by Guan et al. [27], who document the rapid proliferation of learned environment models across the full perception, prediction, and planning stack of modern autonomous driving pipelines. Collectively, the models surveyed in this section span three complementary capabilities: generating photorealistic driving scenarios for training data augmentation, predicting action-conditioned future observations for planning, and learning compact 4D scene representations that preserve geometric structure over long horizons. 

**Scene generation and data augmentation.** A primary motivation for deploying world models in autonomous driving is the scarcity of safety-critical edge cases—unusual weather, atypical road configurations, or near-miss events—that are difficult to collect at scale from real-world fleet operations. World models address this by generating photorealistic, action-controllable driving scenarios that supplement real data for downstream perception and planning training. **GAIA-1** [62] pioneered large-scale generative world modeling for this domain with a 9-billion-parameter architecture that jointly tokenizes video, text, and action inputs, enabling controllable generation of diverse scenarios conditioned on ego-vehicle behavior and textual scene descriptions. Its successor **GAIA2** [182] scaled this paradigm to multi-camera, multi-agent generation with fine-grained semantic control over individual traffic participants, trained on approximately 25 million video sequences across three countries —demonstrating that generative world models can function as scalable data engines for rare scenario synthesis. **MagicDrive** [284] extended this line to spatially consistent multi-view generation across six camera angles simultaneously, introducing explicit 3D geometric control through BEV map and bounding box conditioning that ensures cross-view consistency absent from purely image-level generation approaches. 

**Action-conditioned video prediction.** Beyond data augmentation, world models serve as closed-loop simulators that predict future observations given planned ego-vehicle actions, enabling planners to evaluate action consequences without physical execution. **DriveDreamer** [129] established a two-stage paradigm: a first stage learning structured traffic constraints via diffusion from historical data, and a second enabling action-conditioned future frame prediction. **DriveDreamer-** 

67 

**2** [130] advanced this by integrating large language model guidance for corner-case generation, converting user-specified natural language queries into agent trajectory specifications that condition the world model to synthesize challenging rare scenarios on demand. **DriveDreamer4D** [180] further extended this line to explicit 4D scene representation by combining video generation with 4D Gaussian Splatting, producing spatially consistent multi-view predictions with geometric supervision that support novel viewpoint synthesis. **Vista** [133] pushed the resolution frontier to 576×1024 pixels while introducing flexible action control modes—encompassing steering angle and speed commands, waypoint trajectory conditioning, and goal-point specification—unified through a dynamic conditioning prior within a single architecture. **GenAD** [181] proposed a generalized predictive model framework emphasizing action controllability and trajectory conditioning across diverse driving environments, establishing that a unified world model architecture can capture dynamics across multiple geographic regions and sensor configurations. 

**4D occupancy and geometric world models.** Image-based world models represent the environment as sequences of 2D projections, discarding explicit 3D geometric structure. A parallel line of work embeds 4D scene representations—combining spatial 3D structure with temporal evolution—directly into the world model architecture. **OccSora** [183] proposed generating future 4D occupancy voxel grids as an alternative world representation, producing geometry-aware predictions that explicitly encode volumetric scene structure and support reasoning about occluded regions invisible in camera images. **OccWorld** [132] introduced a joint world model that simultaneously predicts future ego motion and 3D occupancy evolution in a unified latent space, demonstrating that occupancy-based world modeling enables more accurate long-horizon trajectory planning than camera-only counterparts by preserving geometric structure across the prediction horizon. These occupancy-based approaches are complementary to image-based methods: while they sacrifice photorealistic fidelity, they offer structured 3D representations that are more directly amenable to geometric planning and safety verification. 

**LiDAR and multimodal world modeling.** Production autonomous driving systems routinely fuse camera, LiDAR, and radar inputs; however, most generative world models operate primarily in the image domain. **Copilot4D** [67] demonstrated that world model principles extend naturally to LiDAR point-cloud modalities by discretizing 3D point clouds via VQ-VAE and applying discrete diffusion for unsupervised future point-cloud prediction, achieving accurate occupancy forecasting without any labeled supervision. **UniWorld** [285] proposed a unified multimodal world model that learns joint representations over camera images and LiDAR inputs, enabling consistent future prediction across both sensor modalities through a shared latent dynamics model and demonstrating improved downstream 3D detection and motion forecasting through world-modelbased pre-training. 

**World models for end-to-end planning.** Beyond perception-level simulation, world models have been directly integrated into end-to-end driving planners. **LCDrive** [18] integrates chain-ofthought style reasoning with latent world model predictions, interleaving action-proposal tokens with world model rollouts to evaluate candidate trajectories counterfactually before committing to an action. **FutureX** [19] introduces an auto-think mechanism that dynamically activates a latent world model only when scene complexity warrants deliberative reasoning, reducing computational overhead during routine driving while maintaining full predictive capacity in complex scenarios. Think Twice Before Driving [286] formalizes this deliberative planning paradigm by decoupling state estimation from policy optimization through an explicit world model, showing that agents that simulate before acting achieve substantially lower collision rates on closed-loop evaluation. 

**Benchmarks and evaluation.** The field has converged on a set of standard benchmarks that evaluate different aspects of world model performance in the autonomous driving context, summarized in Table 2. The nuScenes dataset [287] provides 1,000 driving scenes with synchronized 

68 

multi-camera and LiDAR data, and is widely used for evaluating future prediction quality through video FID, Fréchet Video Distance (FVD), and trajectory-conditioned PSNR. The Waymo Open Dataset [288] provides larger-scale coverage at higher sensor resolution, enabling evaluation of long-horizon scene prediction fidelity. **CARLA** [289] an open-source urban driving simulator, serves as the primary closed-loop evaluation environment, where world model-based planners are assessed on route completion rate, infraction rate, and driving score across diverse weather and traffic scenarios. The recently introduced **nuPlan** [290] provides reactive multi-agent closed-loop simulation, enabling evaluation of world models under interactive traffic participant behavior rather than pre-recorded scenario replay—an increasingly important capability as the field transitions from open-loop to closed-loop evaluation regimes. 

Table 5: Representative benchmarks for autonomous driving world model evaluation. 

|**Benchmark**|**Year **|**Modality**|**Scale**|**Key Metric**|
|---|---|---|---|---|
|nuScenes|2020|Camera + LiDAR|1,000 scenes|FVD, traj. PSNR|
|Waymo Open|2020|Camera + LiDAR|1,950 segments|Prediction ADE/FDE|
|CARLA|2017|Simulation|Unlimited|Driving score, infraction rate|
|nuPlan|2024|Camera + LiDAR|1,500 hours|Closed-loop reactive score|


**Challenges and future directions.** Autonomous driving has proven to be one of the most fertile application domains for world model research, with large-scale fleet data availability, clear evaluation metrics, and direct commercial impact jointly motivating rapid progress. The field is currently transitioning from open-loop video prediction—where models are evaluated on single-step or short-horizon frame quality—toward closed-loop planning evaluation, where the world model must support reliable action selection over extended horizons under interactive traffic dynamics. Several key challenges remain. First, long-horizon consistency continues to limit deployed systems: current world models struggle to maintain geometrically and semantically coherent predictions beyond a few seconds, with compounding errors degrading scene structure over extended horizons. Second, multi-agent modeling—accurately predicting the joint future behavior of all traffic participants conditioned on the ego-vehicle’s planned actions—requires capturing complex inter-agent dependencies that current architectures model only approximately. Third, the sim-to-real gap persists: models trained on recorded fleet data may not faithfully represent the interactive dynamics that emerge in closed-loop deployment, where the ego-vehicle’s actions influence the behavior of surrounding agents. Fourth, safety verification of world model-based planners demands formal guarantees that remain elusive for high-capacity learned models, limiting their adoption in certified safety-critical deployments. Finally, the computational cost of diffusion-based and transformer-based world models at driving-relevant resolutions poses deployment challenges, motivating research into efficient architectures that preserve predictive quality under strict real-time latency constraints. 

### **6.3 Video prediction and scene understanding** 

Video prediction—forecasting future frames given past observations and optional conditioning signals—is one of the oldest and most natural formulations of world modeling. Scene understanding extends this beyond raw pixel forecasting to extracting structured representations of the depicted world: object identities, spatial relations, physical properties, and causal interactions. Together, these capabilities form a foundation for numerous downstream applications, from autonomous navigation to embodied agent training and creative content generation. 

69 

Unlike the methodological treatment of diffusion-based world models in Section 4.3, which examines _how_ generative architectures learn environment dynamics, this section surveys video prediction and scene understanding as an _application domain_ . The focus is on what tasks are being solved, how models are evaluated, and what fundamental limitations persist—spanning multiple methodological families rather than detailing any single architecture. We refer readers to Section 4.3 for architectural specifics of the diffusion-based systems mentioned here. We also distinguish this discussion from domain-specific video prediction in autonomous driving (Section 6.2), which addresses sensor-specific and safety-critical requirements unique to that setting, and from multimodal agent systems (Section 6.4), which discuss some of the same models from the perspective of agent training environments. Table 6 summarizes representative models organized by paradigm. 

Table 6: Representative world models for video prediction and scene understanding, organized by paradigm. 

|**Model**|**Year**|**Paradigm**|**Key Contribution**|**Interactive**|
|---|---|---|---|---|
|SV2P [59]|2018|Stochastic VAE|Variational latent for<br>multi-future prediction||
|SVG [60]|2018|Stochastic VAE|Learned prior for stochastic<br>video generation||
|SAVP [291]|2018|VAE + GAN|Combined variational and<br>adversarial training||
|VideoGPT [149]|2021|Autoregressive|VQ-VAE + GPT for video<br>token prediction||
|Sora [168]|2024|Diffusion<br>transformer|Minute-long high-fidelity video<br>generation||
|SVD [292]|2023|Latent diffusion|Scalable image-to-video<br>diffusion model||
|CogVideoX [179]|2024|Diffusion<br>transformer|Expert adaptive normalization<br>for text-to-video||
|Open-Sora [293]|2024|Diffusion<br>transformer|Open-source efficient video<br>generation||
|Genie [13]|2024|Latent action<br>model|Interactive 2D worlds from<br>unlabeled video|✓|
|Genie 2 [109]|2024|Latent action<br>model|Persistent interactive 3D<br>environments|✓|
|DIAMOND [37]|2024|Pixel diffusion|Pixel-space diffusion world<br>model, Atari 100k SOTA|✓|
|GameNGen [61]|2024|Latent diffusion|Neural DOOM engine at 20+<br>FPS|✓|
|Oasis [159]|2024|Autoregressive|Transformer-based interactive<br>game simulator|✓|
|Pandora [160]|2024|Hybrid|Language-action conditioned<br>video world model|✓|
|Diffusion<br>Forcing [294]|2024|Causal diffusion|Next-token meets full-sequence<br>diffusion||
|GaussianWorld [238]|2025|3D Gaussian|Streaming 3D occupancy<br>prediction||


**From Deterministic to Stochastic Video Prediction.** Early deep learning approaches to video prediction employed deterministic convolutional architectures that directly regressed future frames from past observations. While conceptually straightforward, these models produced characteristically blurry predictions because they averaged over the inherently multi-modal distribution of possible futures—a pixel in an occluded region, for instance, could plausibly take many different 

70 

values, and a mean-squared-error loss encourages the model to hedge by outputting the mean. Stochastic video prediction models addressed this fundamental limitation by introducing latent random variables that capture the uncertainty over future outcomes. **SV2P** [59] augmented an action-conditioned video prediction network with a time-varying latent variable sampled from a learned posterior, enabling the generation of multiple plausible futures from a single past sequence. **SVG** [60] introduced a learned prior network that generates latent codes autoregressively, conditioning each step on the previous frame’s representation to produce temporally coherent stochastic predictions. **SAVP** [291] combined variational and adversarial training objectives, using a VAE for diversity and a GAN discriminator for sharpness, demonstrating that the two approaches are complementary rather than competing. Oprea et al. [295] provided a comprehensive review documenting the evolution from deterministic to stochastic to adversarial approaches, establishing video prediction as a well-defined research area within computer vision. 

These early stochastic models operated primarily on low-resolution, short-horizon sequences— typically predicting 10–30 frames at resolutions below 256 _×_ 256. Their contributions were nevertheless foundational: they established the principle that video prediction is fundamentally a distribution estimation problem, introduced the variational and adversarial toolkits that subsequent work would scale, and identified the core tension between sample diversity and temporal consistency that continues to shape the field. 

**Autoregressive and Token-Based Video Prediction.** A parallel line of work reformulated video prediction as a sequence modeling problem over discrete tokens, drawing on the success of autoregressive language models. **VideoGPT** [149] pioneered this approach by training a VQVAE to discretize video frames into spatial-temporal token sequences, then modeling their joint distribution with a GPT-style transformer. This formulation naturally handles variable-length generation and benefits from the well-understood scaling properties of transformer architectures. **Phenaki** [296] extended autoregressive video generation to variable-length sequences conditioned on time-varying text prompts, enabling the generation of multi-minute videos that follow evolving narrative descriptions—a significant step toward open-domain video synthesis. **VideoPoet** [297] further unified multiple video generation tasks (text-to-video, image-to-video, video-to-audio, stylization) within a single large language model framework, demonstrating that a unified token vocabulary can subsume diverse modalities. 

The autoregressive paradigm was subsequently applied to interactive world simulation. **Oasis** [159] demonstrated that a transformer operating on discrete video tokens can serve as an interactive game simulator, generating real-time game frames conditioned on player actions—representing an autoregressive counterpart to the diffusion-based game engines discussed below. The key advantage of autoregressive approaches is their natural compatibility with scaling laws established in language modeling; the key limitation is that discrete tokenization may discard fine-grained visual details, and sequential token generation can be slow for high-resolution video. 

**Large-Scale Diffusion Models as World Simulators.** The most significant recent development in video prediction has been the scaling of diffusion-based video generation models to internet-scale training data, producing systems whose outputs exhibit high visual fidelity and apparent physical consistency. This paradigm shift was crystallized by OpenAI’s **Sora** [168] (see Section 4.3 for architectural details), whose technical report [138] argued that the system exhibits emergent properties of a world simulator—including consistent 3D geometry, object permanence, and camera-aware scene generation—motivating systematic investigation into whether large-scale video generators constitute genuine world models. Concurrently, **Make-A-Video** [298] 

71 

and **Imagen Video** [299] demonstrated that pretrained text-to-image models could be extended to video through learned temporal dynamics, establishing cascaded diffusion architectures as a viable paradigm for high-definition video synthesis. 

This debate has been informed by several concurrent large-scale systems. While some of the following were developed primarily as video generators rather than world models, they are included here because their scaling insights, architectural innovations, and emergent behaviors are directly informing the design of next-generation world simulators—and several are being actively studied for latent world-modeling properties. **Stable Video Diffusion** (SVD) [292] demonstrated that carefully curated pretraining data enables high-quality image-to-video generation, establishing an influential open-weight baseline whose data curation methodology has been widely adopted. Google’s **Lumiere** [300] introduced a space-time U-Net that generates entire video durations in a single pass, improving global temporal consistency—a property critical for world simulation. **W.A.L.T.** [301] proposed a unified transformer for both image and video generation using a shared latent space. Meta’s **Movie Gen** [302] scaled to 30 billion parameters with synchronized audio generation, demonstrating the feasibility of multimodal world-scale generation. **CogVideoX** [179] introduced expert adaptive normalization for scalable text-to-video generation, while **Open-Sora** [293] democratized access to the DiT-based paradigm through an open-source implementation. NVIDIA’s **Cosmos** [14] and its successor **Cosmos-Predict2.5** [108], pretrained on 20 million hours of video, explicitly position video generation as a foundation for physical AI and world simulation. 

Despite their visual impressiveness, the status of these systems as world models remains contested. Ding et al. [11] examined the boundary between understanding and prediction in video generation, arguing that perceptual fidelity does not imply causal understanding. More pointedly, Kang et al. [107] conducted controlled experiments demonstrating that current video generation models exhibit _case-based generalization_ —reproducing visual patterns similar to training examples rather than abstracting underlying physical laws—and fail systematically on scenarios requiring genuine physical reasoning such as novel object interactions and out-of-distribution forces. These findings suggest that scaling visual-only training may be necessary but not sufficient for building world models that truly understand physical dynamics, a theme we revisit in the challenges discussion below. 

**Interactive World Models and Neural Game Engines.** A stringent test of whether a video generation model constitutes a world model is its capacity for _interactive_ deployment: can it maintain a coherent, responsive environment conditioned on a continuous stream of user actions? The architectural details of the systems discussed below are covered in Section 4.3; here we focus on their application-level capabilities and what they reveal about the boundary between video generation and environment simulation. Section 6.4 further discusses how some of these systems serve as training environments for embodied agents. 

DeepMind’s **Genie** family [13, 109, 110] progressively demonstrated interactive world generation from unlabeled video: Genie learned latent action models for 2D environments, Genie 2 scaled to persistent 3D worlds from single image prompts, and Genie 3 extended to text-prompted 3D worlds at 720p and 24 FPS. On the game simulation front, **DIAMOND** [37] and **GameNGen** [61] showed that diffusion models can function as real-time game engines at interactive rates, while **GameGenX** [177] extended this to open-world environments with richer action spaces. **Pandora** [160] bridged text-based interaction with visual world simulation by supporting both natural language actions and video state representations. **Diffusion Forcing** [294] provided a theoretical bridge between autoregressive and diffusion paradigms by applying variable noise levels across tokens, enabling causal generation with planning capabilities. 

72 

These interactive systems collectively suggest that the boundary between video generation and environment simulation is dissolving. However, they also reveal a persistent challenge: maintaining long-horizon consistency under interactive control, where the model must generate coherent responses to arbitrary action sequences rather than following a fixed trajectory, substantially amplifies the compounding error problem. Moreover, all of the systems discussed above operate on 2D image projections, discarding the 3D geometric structure that underpins physical reasoning about occlusion, depth, and spatial interaction—limitations that motivate the next direction. 

**3D and 4D Scene Understanding from Video.** A complementary research direction extends video world models to explicit 3D and 4D (3D + time) scene representations, bridging video prediction with spatial scene understanding. Kong et al. [68] provided the first comprehensive survey dedicated to 3D and 4D world modeling, establishing taxonomies spanning three complementary approaches: _video-based_ (VideoGen) methods that generate future 2D frames and optionally lift them to 3D, _occupancy-based_ (OccGen) methods that directly predict volumetric scene structure, and _LiDAR-based_ (LiDARGen) methods that forecast future point clouds. 

Within the occupancy prediction paradigm, **GaussianWorld** [238] introduced streaming 3D occupancy prediction using Gaussian splatting, representing scene elements as 3D Gaussians that evolve over time and enable efficient rendering from novel viewpoints. This approach preserves geometric structure that purely 2D video prediction discards, supporting downstream applications such as view synthesis, spatial planning, and collision detection. 

A key challenge for temporal coherence in both 2D and 3D video world models is the compounding error inherent in autoregressive generation: small prediction errors accumulate over time, leading to degraded scene structure and visual artifacts in long sequences. Po et al. [142] addressed this with _state-space video world models_ for long-context generation, replacing attention-based temporal modeling with linear recurrent architectures (structured state-space models) that offer constant per-frame memory and computation costs. This enables generation over substantially longer horizons than transformer-based approaches, whose quadratic attention cost limits practical sequence lengths. The 3D and 4D world modeling direction is particularly promising for embodied AI applications, where agents must reason about spatial layout, occlusion, and object persistence in three dimensions rather than through 2D projections. 

It is worth noting that “scene understanding” encompasses not only geometric reconstruction but also semantic and relational comprehension: recognizing objects, inferring their physical properties, understanding inter-object relations, and reasoning about causal structure from video. Objectcentric approaches that decompose visual scenes into discrete entity representations—via slot-based mechanisms (Slot Attention, SAVi, SlotFormer) and relational dynamics via graph neural networks (C-SWM, Object-Centric Dreamer)—are surveyed in detail in Section 4.4. Those models provide compositional generalization and physical reasoning capabilities that complement the generationfocused approaches discussed here. A promising but largely unexplored frontier lies in integrating object-centric scene understanding with large-scale video generation models, which would combine the visual fidelity of diffusion-based generators with the structured reasoning afforded by explicit entity representations. 

**Physical Plausibility and the World Model Debate.** The rapid advancement of large-scale video generation has precipitated a fundamental question: do these models _understand_ the physical world, or do they merely produce visually plausible simulations that mimic physical behavior without internalizing its underlying principles? This question has significant implications for whether video generation models can serve as reliable world models for downstream decision-making. 

73 

Several recent works have developed benchmarks and analyses specifically targeting this question. **PhysDreamer** [303] explored physics-based interaction with 3D objects via video generation, demonstrating that coupling generative models with explicit physical simulation can improve the physical plausibility of generated interactions. **WorldSimBench** [304] proposed a comprehensive evaluation framework that assesses video generation models specifically as world simulators, introducing metrics beyond visual quality to measure action controllability, physical consistency, and long-horizon coherence. 

These investigations converge on a nuanced conclusion: current video generation models capture statistical regularities that correlate with physical behavior—objects generally fall downward, liquids flow, and rigid bodies collide—but they do not enforce physical laws as hard constraints. Consequently, they can produce physically implausible outputs for scenarios underrepresented in training data. Bridging this gap may require integrating explicit physical priors (as discussed in Section 4.4), grounding video generation in 3D scene representations, or developing hybrid architectures that combine the visual fidelity of diffusion models with the physical guarantees of simulation engines. 

Despite remarkable progress, several fundamental challenges continue to limit the deployment of video prediction and scene understanding models as reliable world models. 

_Temporal consistency and long-horizon coherence._ Maintaining coherent object identities, physical properties, and geometric relationships across long generated sequences remains the single most significant limitation. Autoregressive models suffer from compounding prediction errors, while diffusion models struggle with global temporal planning across extended sequences. State-space architectures [142] and hierarchical generation strategies offer promising directions but have not yet fully resolved this challenge. 

_Physical understanding versus pattern matching._ As discussed above, current models capture visual correlations with physical behavior but do not enforce physical laws [107]. Closing this gap likely requires architectural innovations that integrate explicit physical reasoning—such as the physics-informed approaches reviewed in Section 4.4—with the visual generation capabilities of large-scale diffusion and autoregressive models. 

_Controllability and interactivity._ Enabling precise, fine-grained user control over generated content—from camera trajectories and object manipulations to semantic scene editing—remains challenging. Interactive world models (Genie, DIAMOND, GameNGen) have demonstrated realtime responsiveness within constrained domains, but extending this to open-world settings with diverse action spaces requires substantially richer conditioning mechanisms. 

_Evaluation methodology._ Standard perceptual metrics (FID, FVD, SSIM) capture visual quality but fail to assess physical plausibility, causal consistency, or interactive fidelity [305]. The field urgently needs evaluation protocols that measure whether generated videos respect physical laws, maintain causal coherence, and support reliable downstream decision-making—properties that are essential if video world models are to serve as substrates for planning and control. 

_Computational cost and real-time deployment._ Diffusion-based models require multiple denoising steps per frame, and transformer-based models face quadratic scaling with sequence length, both limiting real-time applicability. Distillation, consistency models, and linear-complexity architectures represent active research directions, but achieving real-time generation at high resolution with full physical fidelity remains an open challenge. 

_From video generation to genuine world modeling._ Perhaps the most consequential open question is whether the video prediction paradigm—training on large corpora of passively observed video— can yield systems that truly model environment dynamics, or whether genuine world modeling requires active interaction, causal intervention, or explicit physical grounding. The resolution of this question will determine whether video generation models remain powerful content creation 

74 

tools or evolve into foundational components of autonomous intelligent systems. 

### **6.4 Multimodal agents and language-grounded systems** 

The convergence of large language models, vision-language models, and learned world models has given rise to a new generation of multimodal agents capable of perceiving, reasoning about, and acting in complex environments. Unlike the methodological discussion in Section 3.6, which examines how language and multimodal inputs reshape world model architectures and training paradigms, this section surveys the _application systems_ that deploy these capabilities across diverse domains— from robotic manipulation and open-world game playing to graphical user interface navigation and interactive world simulation. A unifying theme across these systems is the use of foundation models as implicit or explicit world models: large pretrained networks that encode rich knowledge about environment dynamics, physical affordances, and semantic relationships, thereby grounding agent behavior in multimodal understanding of the world [306, 307]. The rapid maturation of this application domain since 2022 has been accompanied by the development of standardized benchmarks and open-source model releases that are accelerating progress toward generalist embodied agents. 

**Language-grounded robotic manipulation and planning.** A foundational challenge in deploying language-conditioned robots is bridging the gap between the abstract semantic knowledge encoded in large language models and the physical affordances of a particular robot in a particular environment. **SayCan** [306] addressed this by combining the semantic scoring of an LLM—which rates how _useful_ each primitive skill is for a given instruction—with a learned value function that rates how _feasible_ that skill is in the current state. The product of these two scores selects executable, contextually relevant actions, enabling a mobile manipulator to complete long-horizon kitchen tasks specified in natural language with a 74% planning success rate across 101 real-world trials. **Inner Monologue** [308] extended this paradigm to closed-loop execution by incorporating environment feedback—success detection, scene descriptions, and human corrections—into an ongoing “inner monologue” that allows the LLM planner to retry and replan upon failure, substantially improving robustness over open-loop approaches. Building on this compositional philosophy, **Socratic Models** [309] demonstrated that multiple pretrained foundation models (vision-language models, LLMs, audio models) can be composed through language as an intermediate representation without any additional training, establishing a zero-shot framework for embodied task completion. 

A parallel line of work reframes robot policy generation as code synthesis. **Code as Policies** [310] showed that LLMs can generate executable Python programs that compose perception APIs, control primitives, and spatial reasoning functions, achieving zero-shot generalization to novel tasks across multiple robot embodiments without additional training. **VoxPoser** [311] advanced this idea into three dimensions by using LLMs and VLMs to compose 3D affordance and constraint maps from RGB-D observations and language instructions; these volumetric value maps then serve as objective functions for motion planners, achieving a 76.7% success rate on unseen manipulation instructions. In the domain of reward design, **Eureka** [312] demonstrated that GPT-4 can generate reward functions via evolutionary optimization of reward code, outperforming human expert reward designs on 83% of 29 reinforcement learning environments spanning 10 robot morphologies— including the first successful demonstration of pen spinning with a simulated dexterous hand. 

**Open-world game agents.** Open-world games—particularly Minecraft—have emerged as a primary testbed for multimodal agents that must perceive, plan, and act over long horizons in complex, procedurally generated environments. **MineDojo** [313] established the foundational benchmark for this domain, providing 1,581 programmatic tasks with natural language goal specifications alongside an internet-scale knowledge base comprising 730K YouTube videos, 7K wiki pages, and 340K Reddit posts, and receiving the NeurIPS 2022 Outstanding Datasets and Bench- 

75 

marks Award. Building on this infrastructure, **Voyager** [314] introduced the first LLM-powered lifelong learning agent, combining an automatic curriculum for open-ended exploration, an evergrowing skill library of executable code, and an iterative prompting mechanism with environment feedback and self-verification. Voyager discovered 3.3 times more unique items, traveled 2.3 times longer distances, and reached technology tree milestones 15.3 times faster than prior methods. 

Subsequent systems addressed complementary challenges. **DEPS** [315] (Describe, Explain, Plan, and Select) introduced interactive planning with LLMs that incorporates error explanation and plan refinement, becoming the first zero-shot agent to robustly accomplish over 70 distinct Minecraft tasks. **JARVIS-1** [316] combined multimodal language models with a multimodal memory system that stores and retrieves relevant past experiences, enabling completion of over 200 different tasks and achieving a 12.5% completion rate on the notoriously difficult diamond pickaxe challenge—a five-fold improvement over prior records. **STEVE-1** [317] took a more data-efficient approach by instruction-tuning the Video Pretraining (VPT) model for text and visual instruction following, producing a capable Minecraft agent trained for only $60 of compute. Collectively, these systems demonstrate that combining foundation model reasoning with structured memory, code generation, and curriculum learning can yield agents with increasingly open-ended capabilities. 

**Vision-Language-Action models for generalist robot control.** Vision-Language-Action (VLA) models represent an end-to-end paradigm in which a single model maps multimodal inputs— images and language instructions—directly to executable robot actions. This approach was foreshadowed by **Gato** [150], DeepMind’s 1.2B-parameter generalist agent that performed 604 tasks spanning Atari games, image captioning, dialogue, and real robot block stacking within a single set of weights. **PaLM-E** [307] scaled this vision substantially by injecting continuous embodied observations directly into the embedding space of the 562B-parameter PaLM language model, demonstrating positive transfer across internet-scale language, vision, and robotics domains. 

The Robotics Transformer family established the VLA paradigm for real-world deployment. **RT-1** [117] trained a scalable transformer on 130K real-robot episodes covering over 700 tasks collected from 13 robots over 17 months, achieving a 97% success rate on trained tasks. **RT-2** [118] was the first model to explicitly formalize the VLA concept, adapting large vision-language models to output robot actions represented as text tokens and exhibiting emergent capabilities such as chain-of-thought reasoning for multi-stage semantic manipulation. The **Open X-Embodiment** initiative [116] assembled the largest open-source real robot dataset—over one million trajectories from 22 embodiments across 60 datasets contributed by 34 research laboratories worldwide—and showed that RT-1-X and RT-2-X models trained on this mixture achieved 50% higher success rates than policies trained on single-domain data alone. 

Recent open-source efforts have democratized access to VLA models. **Octo** [318], a 93Mparameter transformer-based diffusion policy pretrained on 800K episodes from Open X-Embodiment, achieved performance comparable to the 55B-parameter RT-2-X while being nearly 600 times smaller. **OpenVLA** [119], a 7B-parameter open-source VLA trained on 970K real-world demonstrations, outperformed the closed RT-2-X by 16.5% in absolute success rate across 29 tasks with seven times fewer parameters. _π_ 0 [319], developed by Physical Intelligence, introduced flow matching for action generation within a VLA framework built on the PaliGemma VLM backbone, enabling complex dexterous manipulation across seven robot platforms and 68 tasks. **VIMA** [320] demonstrated that diverse manipulation tasks can be expressed through multimodal prompts interleaving text and visual tokens, achieving 2.9 times higher success rates than alternatives in the most challenging generalization setting of its benchmark. These developments mark a clear trajectory from closed, proprietary systems toward open, reproducible generalist robot policies. 

**GUI and web navigation agents.** Multimodal agents have also been deployed for interacting with digital interfaces, where the environment consists of graphical user interfaces rather than 

76 

physical spaces. **CogAgent** [321], an 18B-parameter vision-language model specializing in GUI understanding, operates using only screenshots as input and outperformed LLM-based methods that consume extracted HTML on both the Mind2Web benchmark for PC navigation and the AITW benchmark for Android navigation, earning a CVPR 2024 Highlight distinction. **CRADLE** [322] proposed a modular framework for General Computer Control that restricts agents to interact with arbitrary software exclusively through screenshots and keyboard/mouse actions, becoming the first agent to follow main storylines in the complex open-world game Red Dead Redemption 2. **WebArena** [323] and **VisualWebArena** [324] established realistic benchmarks with self-hosted websites and visually grounded tasks, revealing that even the most capable multimodal models achieve only approximately 16% task success—underscoring the substantial gap between current agent capabilities and human-level web navigation performance. 

**Interactive world simulators as training environments.** A complementary application paradigm uses generative world models not as agents themselves but as interactive environments for training and evaluating embodied agents. **UniSim** [88] learned a universal simulator from diverse data sources and demonstrated that both vision-language planners and reinforcement learning policies trained purely within UniSim-generated simulations transferred successfully to physical robots, earning the ICLR 2024 Outstanding Paper Award. The **Genie** family from Google DeepMind has progressively expanded the scope of generative interactive environments: the original **Genie** [13] learned to generate interactive 2D environments from unlabeled internet video using a latent action model, **Genie 2** [109] scaled this to persistent, action-controllable 3D worlds generated from a single image prompt, and **Genie 3** [110] extended generation to dynamic 3D worlds from text prompts at 720p resolution and 24 frames per second with real-time navigation. In a distinct but related direction, **RAP** [139] formalized the repurposing of an LLM as both a world model and a reasoning agent, incorporating Monte Carlo Tree Search for strategic planning and demonstrating that RAP on LLaMA-33B surpassed chain-of-thought prompting on GPT-4 with a 33% relative improvement. These results collectively suggest that learned world simulators—whether pixel-based or language-based—can serve as effective training substrates that reduce reliance on costly real-world data collection. 

**Benchmarks and evaluation.** The evaluation of multimodal agent systems relies on a growing ecosystem of standardized benchmarks spanning diverse domains and capability levels. Table 7 summarizes the principal evaluation suites. In household robotics, **ALFRED** [325] provides 25K natural language instructions paired with 8K demonstrations in the AI2-THOR simulator, while **CALVIN** [326] evaluates language-conditioned policy learning across 34 tasks in four environments. For tabletop manipulation, **VIMA-Bench** [320] defines 17 task types with fourlevel generalization evaluation across over 600K trajectories, and **Language-Table** [327] offers 600K trajectories with 87K language instructions, achieving 93.5% success on a real robot. The **Open X-Embodiment** [116] dataset provides the largest cross-embodiment evaluation at over one million trajectories from 22 robot platforms. For digital agents, **WebArena** [323] and **VisualWebArena** [324] benchmark web navigation with 812 and 910 tasks respectively, while **AgentBench** [328] evaluates LLMs as agents across eight distinct environments. A persistent finding across these benchmarks is that even state-of-the-art systems exhibit substantial performance gaps relative to human baselines, particularly on long-horizon tasks requiring sustained reasoning, recovery from errors, and compositional generalization. 

**Challenges and future directions.** Despite rapid progress, several fundamental challenges remain. First, long-horizon consistency continues to limit deployed systems: current agents struggle to maintain coherent plans over hundreds of sequential decisions, with errors compounding as task horizons grow. Second, the question of whether foundation-model-based agents possess genuine causal understanding—as opposed to sophisticated pattern matching—remains unresolved, with 

77 

Table 7: Representative benchmarks for multimodal agent evaluation. 

|**Benchmark**|**Year**|**Domain**|**Scale**|**Key Metr**|**ic**|
|---|---|---|---|---|---|
|ALFRED|2020|Household (AI2-THOR)|25K instructions|Task succes|s rate|
|MineDojo|2022|Minecraft|1,581 tasks|Task compl|etion rate|
|CALVIN|2022|Language-cond. manip.|34 tasks, 4 envs|Multi-step<br>tion|comple-|
|VIMA-Bench|2023|Tabletop manipulation|17 task types|4-level gene|ralization|
|Language-Table|2023|Tabletop manipulation|600K trajectories|Real-robot<br>rate|success|
|Open X-Embodiment|2024|Cross-embodiment|1M+ trajectories|Cross-embo<br>transfer|diment|
|WebArena|2024|Web navigation|812 tasks|Task succes|s rate|
|VisualWebArena|2024|Visual web navigation|910 tasks|Functional<br>tion|evalua-|
|AgentBench|2024|Multi-domain agents|8 environments|Multi-turn<br>rate|success|


implications for robustness and out-of-distribution generalization. Third, safety and reliability requirements for real-world deployment far exceed what current systems can guarantee, particularly in domains involving physical interaction with humans. Fourth, no single benchmark currently spans the full spectrum of multimodal agent capabilities, creating a need for unified evaluation frameworks that assess perception, reasoning, planning, and action in an integrated manner. Fifth, while VLA models have demonstrated impressive generalization, most still require massive training datasets; leveraging world models for data augmentation and sample-efficient learning represents a promising direction for reducing data requirements. Finally, nearly all current systems operate as single agents, leaving multi-agent coordination in shared physical or digital environments as a largely unexplored frontier. Addressing these challenges will require not only advances in individual model capabilities but also deeper integration of explicit world models with the implicit world knowledge encoded in foundation models. 

### **6.5 Reinforcement learning and Games** 

Reinforcement learning (RL) formalizes sequential decision-making as finding a policy _π_ : _S →_ ∆( _A_ ) that maximizes the expected cumulative discounted return _J_ ( _π_ ) = E _π_ [<sup>�</sup><sup>_∞_</sup> _t_ =0<sup>_γtrt_]withinan</sup> MDP _M_ = ( _S, A, T, R, γ_ ), where the transition dynamics _T_ ( _s_<sup>_′_</sup> _| s, a_ ) and reward function _R_ ( _r | s, a_ ) are both unknown [26]. The central difficulty is that the agent must simultaneously discover what the environment does and optimize against it—a coupling that drives the prohibitive sample complexity of model-free methods, which require tens of millions of interactions before converging. World models address this at its root by learning approximate dynamics _T_<sup>�</sup> and _R_<sup>�</sup> from observed transitions, thereby decoupling environment discovery from policy optimization: once the model is learned, the agent can generate unlimited synthetic experience, plan multi-step action sequences, and assign credit for long-horizon returns—all without additional real environment steps. From the perspective of how the learned model is used, world model RL methods fall into three non-exclusive strategies [233]: (i) **Dyna-style data augmentation** [329], which adds imagined transitions to the replay buffer to increase training data for model-free policy optimization; (ii) **imagination-based policy gradient** , which backpropagates policy gradients directly through differentiable multi-step rollouts in the world model; and (iii) **model-based planning** , which performs explicit look-ahead search (via Monte Carlo Tree Search, MCTS; model predictive control, MPC; or related algorithms) 

78 

to select actions with superior long-term consequences at decision time. Game environments serve as the canonical testbed for this research because they provide well-defined ground-truth dynamics, reproducible evaluation, and a carefully calibrated spectrum of difficulty that isolates specific RL challenges: from low-dimensional continuous control that tests pure dynamics learning, through pixel-based Atari that demands simultaneous representation learning and planning, to board games and open-world environments that require combinatorial search and hierarchical credit assignment. 

**Sample Efficiency: World Models as Data Multipliers.** The most direct motivation for world models in RL is the theoretical and empirical sample complexity gap between model-based and model-free methods. A learned dynamics model transforms each real transition ( _st, at, rt, st_ +1) into a generator of arbitrarily many synthetic transitions, enabling the agent to amortize the cost of environment interaction across a much larger effective training dataset. **SimPLe** [330] was the first to demonstrate this at scale in pixel-based settings, iterating between collecting 6,400 real Atari frames, training a stochastic convolutional world model, and optimizing a PPO policy on 16,000 imagined rollouts per cycle—achieving a 2.1 _×_ improvement over Rainbow DQN at 100K steps and establishing the **Atari 100K benchmark** as the canonical evaluation regime for sample-efficient model-based RL. This iterative real-imagined loop, which Sutton originally termed the Dyna architecture [329], was subsequently refined by **IRIS** [74] and **DIAMOND** [75]: IRIS discretizes frames via VQ-VAE into token sequences and models dynamics with a GPT-style transformer, using imagined rollouts for actor-critic training and achieving 1.046 human-normalized score (HNS) on Atari 100K; DIAMOND replaces autoregressive token prediction with denoising diffusion for holistic next-frame generation, producing sharper and more temporally consistent predictions that yield 1.463 HNS. The progression from SimPLe through IRIS and DIAMOND to **DreamerV3** [8] over five years — all using exactly the same 100K real environment steps — quantifies the compounding gains from better world model representations, more stable training objectives, and tighter integration of model learning with policy optimization. 

**Credit Assignment: Imagination-Based Policy Gradient.** Sparse reward environments pose the credit assignment problem in its sharpest form: the agent must identify which actions, among a long sequence, were causally responsible for an eventual reward—a problem whose difficulty grows with horizon length and reward sparsity. Model-free TD methods address this through bootstrapped value targets and eligibility traces, but remain limited by the variance of bootstrapped estimates and the difficulty of propagating sparse signals backward over long horizons. World models offer a fundamentally different solution: the agent can simulate the future consequences of actions forward through the learned dynamics, directly evaluating long-horizon returns without relying on sparse reward signals to propagate credit backward through time. The Dreamer series [6– 8] operationalizes this through the _RSSM_ (Recurrent State-Space Model), which factorizes the latent state into a deterministic recurrent component _ht_ = _fθ_ ( _ht−_ 1 _, zt−_ 1 _, at−_ 1) and a stochastic component _zt ∼ qϕ_ ( _zt | ht, xt_ ), trained via the ELBO objective combining reconstruction, reward prediction, and KL regularization (Eq. 21). The actor and critic are then optimized entirely within imagined _H_ -step rollouts using the _λ_ -return _G_<sup>_λ_</sup> _t_<sup>=</sup><sup>_rt_+</sup><sup>_γ_[(1</sup><sup>_−λ_)</sup><sup>_v_�</sup><sup>_t_+1+</sup><sup>_λGλ_</sup> _t_ +1<sup>], which blends one-step</sup> TD targets (low variance) with Monte Carlo returns (low bias) to efficiently propagate credit over extended horizons. 


The effectiveness of this approach in long-horizon credit assignment is best illustrated by the Minecraft diamond challenge: DreamerV3 [8] is the first algorithm to collect diamonds from scratch 

79 

without human demonstrations, requiring sequential discovery of a 12-item technology tree (wood _→_ planks _→_ sticks _→_ crafting table _→_ . . . _→_ iron pickaxe _→_ diamonds) under sparse binary rewards. Transformer-based world models further strengthen credit assignment by replacing GRU recurrence with attention over the full history of latent states. **TransDreamer** [153] introduces the Transformer State-Space Model (TSSM) and demonstrates substantial improvements over DreamerV2 on Memory Maze and POMDPSuite, where rewards depend on observations hundreds of steps in the past. Its successor **TransDreamerV3** [331] integrates TSSM into the DreamerV3 framework, combining transformer-based long-range memory with DreamerV3’s robustness techniques for stable multi-domain learning. **STORM** [36] takes a complementary approach by introducing stochastic uncertainty into transformer dynamics through prior-posterior Gaussian pairs, enabling explicit uncertainty quantification that both improves prediction calibration and provides a principled KL-based intrinsic reward for exploration; the result is a mean HNS of 1.311 on Atari 100K, with particularly large gains on partially observable games where uncertainty modeling is most valuable. 

**Planning and Look-Ahead Reasoning: From MCTS to Latent MPC.** Beyond improving data efficiency and credit assignment, world models enable deliberate planning: the ability to mentally simulate action sequences and evaluate their long-term consequences before execution—a capability fundamentally unavailable to reactive model-free policies. Two planning paradigms have proven most effective. The first uses MCTS within the learned model at decision time, constructing a partial game tree whose nodes are latent states and whose edges are candidate actions, guided by value and policy network heuristics. **AlphaZero** [332] established this paradigm using known game rules, achieving superhuman performance in Go, chess, and shogi through self-play. **MuZero** [9] generalized it to unknown environments by learning a value-equivalent model (three functions _hθ_ for representation, _gθ_ for dynamics, and _fθ_ for prediction of value, policy, and reward), trained end-toend to minimize prediction error on planning-relevant targets without any reconstruction objective. MCTS then operates entirely within this learned latent space, achieving superhuman performance across 57 Atari games, Go, chess, and shogi simultaneously. **MuZero Reanalyze** [333] improved its sample efficiency by replaying stored trajectories through the current world model to relabel value and policy targets. **EfficientZero** [102] addressed MuZero’s limitations in the low-data regime by augmenting it with three modifications that jointly solve the credit assignment and data efficiency problems simultaneously: a self-supervised consistency loss _L_ cons = _∥gθ_ ( _st, at_ ) _−_ sg[ _hθ_ ( _ot_ +1)] _∥_<sup>2</sup> 2<sup>that provides dense dynamics supervision independent of reward sparsity, end-to-end</sup> value prefix learning to reduce compounding temporal error, and off-policy correction for replayed data. Together these achieve 194.3% mean human performance on Atari 100K with two hours of real gameplay—500 _×_ fewer frames than DQN. **EfficientZero V2** [334] extends this framework to continuous action spaces via Gumbel-based sampling search, outperforming DreamerV3 in 50 of 66 tasks across Atari and DMControl without per-domain tuning. **Student of Games** [335] unifies MCTS with counterfactual regret minimization for imperfect-information settings, achieving near-human performance in both chess and poker within a single model-based architecture. 

The second planning paradigm uses MPC in continuous action spaces, sampling action sequences, evaluating them by rolling out through the world model, and executing the highest-value sequence in receding-horizon fashion. **TD-MPC2** [267] combines a latent dynamics model with temporal difference learning and MPPI-based MPC, where the world model evaluates candidate trajectories and the value function bootstraps terminal returns. On HumanoidBench [336]—17 whole-body control tasks for a 56-DOF humanoid—TD-MPC2 outperforms DreamerV3 by over 40% on average, demonstrating that tight integration of model-based look-ahead with value esti- 

80 

mation is particularly powerful in high-dimensional continuous action spaces where exhaustive tree search is infeasible. 

**Partial Observability: Belief State Estimation Through World Models.** A central challenge in many RL environments is partial observability: the agent’s observation _ot_ does not fully determine the underlying state _st_ , so optimal decision-making requires integrating evidence across the full observation history _o_ 1: _t_ . Model-free methods address this heuristically through frame stacking or recurrent networks, but lack a principled mechanism for maintaining calibrated uncertainty over hidden states. World models provide a natural solution via Bayesian filtering: the RSSM posterior _q_ ( _zt | ht, ot_ ) represents the agent’s belief about the current latent state given all past observations compressed into the deterministic state _ht_ , enabling principled uncertainty-aware planning. The advantage of this belief state formulation is most apparent in environments requiring long-range memory. On Memory Maze [337] (where the agent must navigate a 3D labyrinth and retrieve goal locations visited hundreds of steps earlier), **TransDreamer** [153] substantially outperforms DreamerV2 by replacing GRU recurrence with full-history attention in the TSSM, allowing the agent to selectively retrieve episodically relevant observations. **STORM** [36] similarly exploits transformer attention for partial observability, with its stochastic formulation additionally capturing residual state uncertainty through explicit prior-posterior pairs conditioned on hidden states. On the NetHack Learning Environment [338] (a roguelike with thousands of item types, stochastic events, and partial map visibility requiring persistent long-term memory), recurrent world model approaches demonstrate the capacity to maintain coherent beliefs over episodes of thousands of steps, far exceeding the horizon where standard frame-stacking policies degrade. The practical implication is that the choice of dynamics model architecture (GRU vs. transformer vs. state-space model) has the largest impact in partially observable settings, and this dimension should guide architecture selection for real-world RL deployments where full observability is rarely available. 

**Exploration: World Models Under Sparse and Deceptive Rewards.** Effective exploration is among the most practically important and theoretically difficult aspects of RL: the agent must visit sufficiently diverse states to discover high-reward trajectories without a guiding signal. Standard entropy-based exploration (maximizing action distribution entropy) proves insufficient for hard exploration benchmarks with long reward chains or deceptive local optima. World models enable two principled approaches to this problem. The first exploits epistemic uncertainty: states where the world model has high prediction error are states that have been visited infrequently, and thus contain the most information to be gained from exploration. This motivates using world model prediction error as an intrinsic reward that augments the extrinsic task reward—a direction pursued by several curiosity-driven exploration methods that integrate naturally with RSSM-based world models. The second approach, embodied by **Optimistic World Models (OWM)** [339], draws on the reward-biased maximum likelihood estimation (RBMLE) principle from adaptive control theory to implement the “optimism in the face of uncertainty” (OFU) principle directly within the dynamics model. OWM augments the standard world model training objective with an optimistic dynamics loss: 


which gently steers the learned transition distribution toward higher-reward outcomes, training the world model to generate optimistic imaginations without requiring explicit uncertainty estimates or constrained optimization. This plug-and-play modification is architecturally agnostic—instantiated as Optimistic DreamerV3 and Optimistic STORM, it achieves significant gains on sparse-reward Atari games that defeat standard entropy-based exploration, while adding minimal computational 

81 

overhead. A complementary perspective is offered by **EfficientZero** ’s [102] self-supervised consistency loss, which densifies the dynamics training signal independent of reward sparsity: by supervising the world model with the encoder’s next-observation representation rather than relying solely on the sparse reward signal, EfficientZero ensures the dynamics model remains accurate even in regions where rewards are absent—enabling MCTS to plan reliably through extended reward-free passages that confound approaches relying on reward-supervised dynamics alone. 

**Generative Game Engines: From Simulators to Policy Training Substrates.** A distinct but increasingly prominent paradigm treats environment simulation as a generative modeling problem, training high-capacity generative models to produce photorealistic action-conditioned frame sequences that can serve as both evaluation environments and policy training substrates. This approach prioritizes visual fidelity over latent compactness, and planning interpretability over computational efficiency. **GameGAN** [145] was an early demonstration, training a GAN to simulate DOOM and Pac-Man from gameplay trajectories; while visually coherent, GAN training instability limited its utility as an RL training environment. **DIAMOND** [75] resolved this by replacing the adversarial objective with denoising diffusion: given a window of _k_ past frames and an action, the DDPM iteratively denoises a random noise tensor into the predicted next frame through a sequence of reverse diffusion steps conditioned via cross-attention, producing holistic per-frame predictions with 1.463 HNS on Atari 100K. **GameNGen** [76] scaled this paradigm dramatically—adapting Stable Diffusion to simulate DOOM at 20 fps with visual quality indistinguishable from the real game by human evaluators (PSNR 29.4 dB), trained on 900 hours of automated gameplay. The key insight of GameNGen is that consistent enemy AI behavior, ammo bookkeeping, and physically plausible projectile dynamics all emerge from a single diffusion model trained purely on gameplay video, without any explicit game rule supervision—suggesting that photorealistic game simulation may be an emergent property of large-scale generative models at sufficient training scale. 

### **6.6 Scientific and Domain-specific Modeling** 

Scientific disciplines have long relied on numerical simulation to model complex physical systems: from atmospheric dynamics to molecular interactions to cosmic structure formation. These simulations, grounded in first-principles physics, provide high-fidelity predictions but incur enormous computational costs. A single high-resolution climate projection can require millions of CPU-hours, and atomistic molecular dynamics simulations of biologically relevant timescales remain intractable even on modern supercomputers. World models offer a compelling alternative by learning surrogate dynamics models directly from simulation data or observations, enabling orders-of-magnitude speedups while preserving physically meaningful predictions. Unlike the physics-informed architectures discussed in Section 4.4, which embed conservation laws and symmetries as architectural priors, this section surveys how world-model concepts are applied as _domain-level tools_ across specific scientific fields: weather and climate prediction, molecular and materials simulation, and cosmological modeling, where learned dynamics surrogates are transforming the practice of computational science. 

**Weather and climate prediction.** Numerical weather prediction (NWP) has been the operational backbone of meteorology for decades, evolving the atmospheric state forward through discretized partial differential equations at enormous computational expense. The emergence of data-driven weather models represents a paradigm shift in this field. **Pangu-Weather** [340] introduced a 3D Earth-Specific Transformer architecture trained on 39 years of global reanalysis data 

82 

from ERA5, becoming the first AI-based system to outperform the European Centre for MediumRange Weather Forecasts (ECMWF) Integrated Forecasting System across all variables and lead times up to one week, at 0.25<sup>_◦_</sup> spatial resolution. **GraphCast** [341], developed by DeepMind, adopted graph neural networks on an icosahedral mesh to model atmospheric dynamics, achieving superior accuracy to ECMWF’s deterministic forecasts on over 90% of 1,380 verification targets while producing 10-day forecasts in under one minute on a single GPU. These models can be interpreted as learned world models of the atmosphere: given the current and previous atmospheric states ( _Xt, Xt−_ 1), they predict the next state _X_ � _t_ +1 through a learned transition function that implicitly captures the governing fluid dynamics. 

A critical limitation of these early models was their deterministic nature; they produced singlepoint forecasts that could not represent the inherent uncertainty of chaotic atmospheric dynamics. **GenCast** [342], also from DeepMind, addressed this by formulating weather prediction as a conditional diffusion process: starting from noise, a denoiser network iteratively refines candidate atmospheric states conditioned on recent observations, producing an ensemble of plausible future trajectories. GenCast outperformed ECMWF’s operational ensemble forecast (ENS) on 97.2% of 1,320 evaluation targets and demonstrated superior skill in predicting extreme weather events, tropical cyclone tracks, and wind power generation, while requiring only 8 minutes on a single TPU to generate a full 15-day ensemble. **NeuralGCM** [343] pursued a complementary hybrid approach, embedding learned parameterizations within a differentiable general circulation model to combine the physical guarantees of NWP with the flexibility of neural networks, achieving competitive accuracy from weather to climate timescales. 

Beyond medium-range forecasting, foundation-model approaches are extending the temporal scope of learned atmospheric world models. **ClimaX** [344] introduced a vision-transformer backbone pretrained on heterogeneous climate datasets including CMIP6 simulations, demonstrating that a single architecture can be fine-tuned for weather forecasting, seasonal prediction, regional downscaling, and climate projection. **Aurora** [345], pretrained on over one million hours of diverse Earth system data, achieved state-of-the-art accuracy using a 1.3-billion-parameter 3D Swin Transformer and has been integrated into ECMWF’s operational evaluation suite alongside physics-based models. 

**Molecular simulation and computational chemistry.** At the atomic scale, world models address a different but structurally analogous challenge: predicting the temporal evolution of molecular systems governed by quantum-mechanical interactions. Classical molecular dynamics (MD) numerically integrates Newton’s equations of motion using empirical force fields, but the accuracycost tradeoff limits both the system sizes and timescales that can be practically explored. Machine learning interatomic potentials (MLIPs) have emerged as learned transition models that approximate the potential energy surface _U_ ( **r** ) and its gradients from quantum-mechanical training data, enabling MD simulations with near ab initio accuracy at a fraction of the cost. 

Architecturally, these models parallel the state-space world models discussed in Section 4.4: the molecular configuration **r** _t_ serves as the state, the force field provides the transition dynamics, and the trajectory constitutes a rollout. **SchNet** [122] introduced continuous-filter convolutional networks for learning molecular representations that respect rotational invariance. Subsequent equivariant architectures, including **NequIP** [123] and **MACE** [346], incorporated E(3)-equivariant message passing to achieve superior data efficiency and accuracy. The recent **GEMS** framework [347] demonstrated that pretrained neural network potentials can simulate biomolecular dynamics across chemically diverse fragments, representing a step toward general-purpose molecular world models. 

Beyond force-field surrogates, generative approaches directly tackle the sampling bottleneck that 

83 

limits conventional MD. **Boltzmann generators** [348] introduced normalizing flows that learn invertible transformations between a simple Gaussian prior and the target Boltzmann distribution of a molecular system, enabling one-shot generation of equilibrium configurations without sequential simulation. This approach has been extended to transferable architectures that generalize across chemical space [349], and to diffusion-based methods for modeling protein conformational dynamics [350]. In the drug discovery context, **AlphaFold 3** [351] extended structure prediction from proteins to general biomolecular complexes including DNA, RNA, and small-molecule ligands, using a diffusion-based architecture that assembles predictions from an initial cloud of atoms. While primarily a structure prediction model rather than a dynamics simulator, AlphaFold 3 demonstrates that learned models can capture the physical constraints governing molecular interactions at scale, laying groundwork for future dynamics-capable molecular world models. 

**Cosmological simulation and astrophysics.** At the largest physical scales, cosmological N- body simulations model the gravitational evolution of dark matter and baryonic matter over billions of years to predict the large-scale structure of the universe. These simulations are indispensable for interpreting observational data from galaxy surveys but are computationally prohibitive at the resolutions required for precision cosmology. Learned surrogate models have emerged as efficient alternatives that approximate the mapping from initial conditions to evolved cosmic structure. 

The **Deep Density Displacement Model** (D<sup>3</sup> M) [352] demonstrated that a deep neural network can learn to transform first-order perturbation theory approximations into accurate nonlinear structure predictions, achieving results comparable to full N-body simulations at a small fraction of the computational cost. Super-resolution approaches [353] have further shown that generative adversarial networks can enhance low-resolution dark matter simulations to high-resolution counterparts containing up to 512 times more particles while preserving statistical properties of the matter distribution. The **CAMELS** project [354] created thousands of cosmological hydrodynamic simulations with systematic parameter variations, providing large-scale training data for machine learning models that can marginalize over uncertainties in baryonic physics while extracting cosmological information, an approach that parallels the use of diverse training environments in reinforcement-learning-based world models. 

These cosmological surrogates face a domain-specific variant of the long-horizon consistency challenge: small errors in predicted density fields compound over cosmic time, leading to incorrect predictions of halo formation and galaxy clustering. Addressing this requires incorporating physical priors such as mass conservation, momentum conservation, and the correct power spectrum of initial fluctuations, constraints that connect directly to the physics-informed methods discussed in Section 4.4. 

Across these domains, scientific world models share common frontiers that distinguish them from perception-oriented counterparts. _Physical consistency_ is non-negotiable: unlike video prediction, where minor artifacts may be tolerable, scientific surrogates must respect conservation laws, symmetries, and thermodynamic constraints over extended rollouts, whether that means energy conservation in molecular trajectories, mass conservation in atmospheric models, or the correct matter power spectrum in cosmological rollouts. _Uncertainty quantification_ is equally essential, as demonstrated by GenCast’s ensemble diffusion approach; deterministic point predictions are insufficient when the goal is to characterize full probability distributions over possible outcomes. Perhaps most acutely, _out-of-distribution generalization_ remains an open problem, since scientific models are routinely used to extrapolate beyond training conditions: novel greenhouse gas concentrations, untested thermodynamic regimes, or alternative cosmological parameters, where data-driven models may fail silently. Addressing these demands points toward hybrid architectures that couple learned 

84 

components with physics-based constraints, and the convergence of foundation-model pretraining with domain-specific fine-tuning suggests that the next generation of scientific world models will achieve broader generalization across conditions, scales, and physical regimes, potentially enabling a paradigm of “simulation-free” scientific discovery in which learned surrogates serve as the primary engine for hypothesis generation, experimental design, and physical prediction. 

### **6.7 Medical Images and Video Recordings** 

The application of world models to healthcare and medical imaging is an emerging frontier with unique requirements: patient safety demands extreme reliability, data is scarce and privacy constrained, and the stakes of inaccurate predictions are high. Unlike game or driving environments where errors result in low scores or simulated collisions, prediction failures in clinical settings can directly impact patient well-being. Yet, the core world-model paradigm—learning environment dynamics, predicting future states conditioned on actions, and using those predictions for planning—maps naturally onto the clinical workflow: a patient’s physiological state evolves over time, clinical interventions (treatments, surgeries, medications) constitute actions, and the goal is to select the intervention that optimizes long-term patient outcomes. 

Qazi et al. [253] provided the first focused review of world models for clinical applications, proposing a four-level capability rubric that classifies medical world models by functional maturity: **L1** (temporal prediction)—forecasting the natural evolution of a patient’s state without conditioning on interventions; **L2** (action-conditioned prediction)—predicting outcomes given specific treatment choices; **L3** (counterfactual rollouts)—simulating “what-if” scenarios for decision support, enabling comparison of multiple candidate interventions; and **L4** (planning and control)—closing the loop by using the learned dynamics model to autonomously recommend or optimize treatment strategies. This rubric provides a useful framework for assessing the maturity of medical world models across application domains. Figure 3 maps the principal medical world models onto this rubric, revealing that most systems cluster at L1–L2 with a clear gap at L4. 

#### **6.7.1 Medical Imaging Analysis and Progressive Disease Prediction** 

World models for medical imaging aim to capture the temporal dynamics of anatomical structures, enabling the prediction of how pathology evolves over time, such as tumor growth, neurodegenerative atrophy, or treatment-induced changes. In this context, these models typically operate across longitudinal time points or patient cohorts rather than in real-time interactive environments. 

**Brain disease progression.** Latent diffusion models have recently emerged as a powerful paradigm for individual-level disease progression modeling using 3D brain MRI. Brain Latent Progression (BrLP) [355], for example, operates in a compact latent space and incorporates subjectlevel metadata, including age, sex, diagnosis, and APOE genotype, to predict Alzheimer’s disease (AD) progression from 3D T1-weighted MRI. Trained on 11,730 scans from 2,805 subjects across three longitudinal AD datasets, BrLP achieved a 22% improvement in volumetric accuracy across AD-relevant brain regions and a 43% improvement in image similarity relative to prior approaches. An extended version [355] further scaled to more than 14,000 MRIs and demonstrated potential clinical utility in identifying fast progressors in a simulated retrospective study. 

**Brain tumor growth prediction.** Treatment-aware diffusion probabilistic models [356] have been developed to predict future tumor morphology from multi-parametric MRI while conditioning on treatment plans, such as surgery type, chemotherapy regimen, and radiation dose. By incorporating treatment information as a conditioning signal to guide the diffusion process, these models can generate both future MRI volumes and corresponding tumor segmentation masks. Report- 

85 


Figure 3: Capability landscape of medical world models. Models are placed according to their clinical domain (columns) and the highest capability level they achieve on the L1–L4 rubric of Qazi et al. [253] (rows). L1 = temporal prediction; L2 = action-conditioned prediction; L3 = counterfactual rollouts; L4 = autonomous planning and control. The dashed red boundary at L4 indicates that no medical world model currently operates at the planning-and-control level, highlighting the principal open frontier. 

edly, they improve future tumor prediction accuracy by more than 16% compared with treatmentagnostic baselines. This represents an L2-level capability, namely, action-conditioned prediction in which the “action” corresponds to the clinical treatment plan. 

**Retinal disease progression.** In ophthalmology, AI systems have been developed to predict the progression of diabetic retinopathy (DR) and age-related macular degeneration (AMD) from fundus photographs and optical coherence tomography (OCT) scans. Although these approaches are not always explicitly framed as world models, they implement the core L1 capability of temporal prediction. The MICCAI 2024 DIAMOND and MARIO challenges [357] benchmarked 21 deep learning methods for patient-specific prediction of DR and AMD progression. In addition, foundation models such as RETFound [358], which was pretrained using self-supervised masked autoencoding on 1.6 million unlabeled retinal images, have demonstrated strong transfer performance for disease detection and progression prediction, outperforming ImageNet-pretrained baselines across multiple ophthalmic and systemic disease tasks. 

**General-purpose medical representations.** JEPA-style predictive representation learn- 

86 

ing [39] offers a promising route toward general-purpose medical image representations without requiring large labeled datasets. By predicting masked image regions in representation space rather than reconstructing them in pixel space, these models can learn features that capture anatomically meaningful structure. Such representations may serve as effective encoders for downstream clinical world models. 

**functional Magnetic Resonance Imaging.** An emerging direction within world models is the prediction of future brain activity from functional Magnetic Resonance Imaging (fMRI), where the goal is to model not only static representations but also the temporal evolution of brain states. Early work demonstrated that auto-regressive models can forecast resting-state dynamics from prior fMRI time series, showing that future brain states can be predicted while preserving functional connectivity structure [359]. This line of research has progressed to voxel-level prediction by Sun et al., which introduced a Swin Transformer–based framework for 4D fMRI forecasting [360]. By jointly modeling spatial and temporal dependencies, this approach predicts several seconds of future brain activity from prior scans while preserving BOLD contrast and dynamics, demonstrating that fine-grained whole-brain evolution is learnable at high spatial resolution. 

More recently, the field has shifted toward foundation models for fMRI, moving beyond taskspecific predictors to large-scale, generalizable representations. For example, NeuroSTORM was pretrained on tens of millions of fMRI frames across large cohorts, enabling transferable representations for prediction, diagnosis, and downstream analysis [361]. Similarly, BrainLM and related models adopt self-supervised learning (e.g., masked modeling) to learn latent brain dynamics from thousands of hours of fMRI data, supporting both forecasting and cross-task generalization [362]. These models mark a transition from narrow predictive models to scalable, reusable representations of brain activity. In parallel, multimodal foundation models are beginning to predict brain activity from external stimuli. Meta’s TRIBE and its recent extension TRIBE v2 demonstrate that largescale models can predict whole-brain fMRI responses from video, audio, and language inputs in a zero-shot manner [363]. Although primarily framed as encoding models, these approaches align with world-model perspectives by learning mappings between external environments and internal brain states. 

Building on these advances, our recent work on fMRI foundation modelling [361] further emphasizes learning unified, temporally consistent representations of brain dynamics that can support prediction, imputation, and downstream clinical tasks. This direction aligns closely with the concept of world models, where latent representations capture the evolving state of a complex system—in this case, the human brain. 

Overall, the field is rapidly evolving from regional forecasting _→_ voxel _→_ level prediction _→_ foundation models _→_ multimodal brain simulators. This progression suggests that fMRI-based brainstate models are becoming increasingly capable of supporting in silico simulation of brain dynamics, with potential applications in scan acceleration, digital brain twins, disease monitoring, and counterfactual prediction of brain trajectories under different conditions. 

#### **6.7.2 Tumor Evolution and Treatment Planning** 

Treatment planning represents the transition from L1 (temporal prediction) to L2–L3 (actionconditioned prediction and counterfactual reasoning), where the world model explicitly simulates how a patient’s disease state evolves _in response to_ specific therapeutic interventions. 

**MeWM (Medical World Model).** Yang et al. [135] introduced MeWM, the first world model in medicine that visually predicts future disease states based on clinical decisions. MeWM comprises three components mirroring the canonical world-model architecture: (1) a _policy model_ implemented as a vision-language model that generates candidate treatment action combos (e.g., 

87 

TACE protocol selection for hepatocellular carcinoma) from the patient’s current CT scan and clinical context; (2) a _dynamics model_ implemented as an action-driven 3D diffusion model trained on longitudinal paired pre- and post-treatment CT volumes that simulates tumor progression or regression under the proposed treatment; and (3) an _inverse dynamics model_ that applies survival risk analysis to the simulated post-treatment tumor, quantitatively evaluating treatment efficacy and feeding back to refine the policy. In Turing tests evaluated by board-certified radiologists, MeWM’s synthesized post-treatment tumors achieved state-of-the-art specificity. Its inverse dynamics model outperformed medical-specialized GPTs (including GPT-4o) in optimizing individualized TACE protocols, with F1-scores of 52.4% (in-house) and 64.1% (public dataset) versus GPT-4o’s 42.0% and 44.3%. Critically, MeWM improved clinical decision-making for interventional physicians by 13% F1-score in selecting optimal TACE protocols, demonstrating the practical value of L2–L3 world models in oncology. 

**CLARITY.** Ding et al. [134] addressed limitations of MeWM—particularly its reliance on stochastic diffusion for visual reconstruction rather than causal physiological transitions, and its lack of patient-specific temporal context. CLARITY models the pre-to-post-treatment transformation as a smooth, interpretable trajectory within a structured latent space rather than reconstructing clinical images pixel-by-pixel. It integrates temporal context (time intervals between scans), clinical context (genomic alterations, demographics, therapeutic history), and an inverse survival evaluation that creates an adaptive feedback loop: predicted outcomes are fed back to the therapy policy agent, enabling iterative refinement of treatment recommendations. On the MU-Glioma-Post dataset for glioma treatment planning, CLARITY outperformed MeWM by 12% and surpassed all medicalspecialized large language models, representing an advance toward L3–L4 capability. 

#### **6.7.3 Surgical Video and Robotic Surgery** 

Surgical world models learn the dynamics of surgical scenes—tool-tissue interactions, anatomical deformations, bleeding, and instrument movements—to enable simulation, training, and autonomous assistance. These models operate at L2–L3, with L4 (autonomous surgical planning) as an aspirational frontier. 

**SurgWM (Surgical Vision World Model).** Koju et al. [364] presented the first actioncontrollable surgical visual world model. Inspired by Genie’s [13] approach of learning latent actions from unlabeled video, SurgWM infers latent surgical actions from raw surgical video without requiring action annotations—a critical advantage given that obtaining action labels for surgical data is prohibitively expensive. The architecture comprises a video tokenizer, a surgical latent action model, and a surgical dynamics model, all using spatio-temporal transformers with causal temporal attention for autoregressive prediction. Trained on the SurgToolLoc-2022 dataset (24,695 clips from da Vinci robotic surgery), SurgWM generates action-controllable surgical video predictions, enabling applications in medical professional training and autonomous surgical agent development. Evaluation on FVD and SSIM confirmed both generation quality and controllability, with conditioning on ground-truth-derived actions yielding consistently better metrics. 

**UniSWM (Unified Surgical World Model).** The UniSWM [365] proposes a mixture-oftransformers (MoT) architecture that unifies three capabilities within a single model: structured understanding (hierarchical recognition of surgical phases, steps, atomic actions, and movements), long-horizon prediction (multi-step surgical trajectory forecasting), and fine-grained generation (action-conditioned video synthesis). UniSWM introduces UniSWM-DB, a diverse multimodal dataset containing 1.81 million samples for surgical training, and UniSWM-Bench, a comprehensive benchmark covering five understanding tasks, two prediction tasks, and three generation tasks across both in-body and operating room settings. 

88 

**Cardiac Copilot and EchoWorld.** Jiang et al. [366] introduced Cardiac Copilot, an AI system for real-time ultrasound probe guidance in echocardiography—addressing the severe global shortage of experienced cardiac sonographers. The core innovation is “Cardiac Dreamer,” a datadriven world model that represents cardiac spatial structure: given the current probe position, Cardiac Dreamer provides structure features of nearby cardiac planes in latent space, serving as a navigation map for autonomous plane localization. Trained on expert operation data from 125 clinical scans (188K sample pairs collected via a robotic arm with 6-DOF pose sensing), Cardiac Dreamer reduced navigation errors by up to 33% across three standard echocardiographic planes (PLAX, PSAX-AV, PSAX-MV). Yue et al. [367] (CVPR 2025) extended this with EchoWorld, a motion-aware world modeling framework pretrained on over one million ultrasound images from 200+ routine scans. EchoWorld employs masked anatomical prediction and motion-conditioned visual simulation during pretraining, then applies a motion-aware attention mechanism during fine-tuning to integrate historical visual-motion sequences, achieving further reductions in guidance error over Cardiac Copilot and existing visual backbones. 

#### **6.7.4 Disease Progression Modeling from Electronic Health Records** 

Applied to electronic health records (EHRs), world models learn to forecast clinical event sequences— lab results, medication changes, deterioration events—from structured temporal patient data, enabling proactive intervention planning. The irregular sampling, sparsity, and noise inherent in EHR data pose challenges absent in visual world modeling. 

**MedDreamer.** Xu et al. [368] introduced MedDreamer, the first model-based RL framework that applies latent imagination to irregular healthcare data. MedDreamer uses a world model with an Adaptive Feature Integration (AFI) module that captures patient and treatment dynamics by modeling their interactions in higher-order latent spaces, addressing the challenges of irregular sampling, sparsity, and missing values in EHR data. Through a two-phase training pipeline, the model first grounds its policy in real clinical time progression, then refines it using horizon-based imagination mixed with real data. Evaluated on sepsis treatment and mechanical ventilation management using two large-scale EHR datasets, MedDreamer achieved relative mortality rate reductions of 20.9% (sepsis) and 16.0% (mechanical ventilation) compared to clinician baselines, outperforming both model-free (DDQN, EZ-Vent, DeepVent) and model-based (MBRL-BNN, DreamerV3) baselines. This represents L2–L3 capability on EHR data: action-conditioned prediction with imagination-based policy optimization. 

**Broader EHR-based approaches.** The intersection of deep reinforcement learning and EHR data is an active area with multiple complementary approaches: Deep Q-Networks for disease prediction from EHR sequences, dynamic treatment regime optimization using offline RL, and personalized diagnostic decision pathways that formulate diagnosis as a sequential decisionmaking problem. However, most existing EHR-based systems operate at L1–L2 (temporal and action-conditioned prediction), with L3 (counterfactual validation of treatment alternatives) and L4 (autonomous closed-loop treatment optimization) remaining largely unrealized due to the absence of interventional ground truth and the ethical constraints of deploying autonomous clinical agents. 

#### **6.7.5 Capability Assessment and Open Challenges** 

As illustrated in Figure 3, the majority of current medical world models operate at L1–L2; advancing to L3–L4 requires addressing several domain-specific challenges: 

1. _Data scarcity and privacy:_ Medical datasets are orders of magnitude smaller than those 

89 

available for games or driving. A typical longitudinal oncology dataset contains hundreds to low thousands of patients, compared to millions of frames in Atari or thousands of hours of driving video. Strict privacy regulations (HIPAA, GDPR) further constrain data sharing and centralized model training. Federated learning and synthetic data generation via world models themselves offer partial solutions, but have not been validated at scale for clinical applications. 

2. _Clinical validation and interventional ground truth:_ Advancing from L2 to L3 requires validation of counterfactual predictions—“What would have happened under an alternative treatment?”—against outcomes that are inherently unobservable (the counterfactual was not administered). Qazi et al. [253] recommend multi-site holdout validation, matched cohort studies, and clinician adjudication, but prospective randomized evaluation of world-model recommendations remains ethically complex and logistically challenging. 

3. _Safety, interpretability, and regulatory approval:_ Deploying L4-level autonomous clinical world models requires not only accuracy but also calibrated uncertainty estimates (the model must know when it does not know), interpretability (clinicians must understand the basis for recommendations), and formal regulatory pathways (FDA 510(k) or De Novo for AI-asmedical-device). Overconfident predictions in oncology or surgery can be life-threatening; abstention policies and human-in-the-loop safeguards are essential. 

4. _Heterogeneity across patient populations:_ Patient populations vary across demographics, comorbidities, genetic backgrounds, and treatment histories. A world model trained on one institution’s cohort may not generalize to another’s. Domain adaptation, multi-site pretraining, and personalization through patient-specific conditioning (as in CLARITY [134] and BrLP [355]) are active areas of research. 

5. _Multimodal state construction:_ Clinical “observations” span imaging (CT, MRI, ultrasound, pathology slides), structured data (labs, vitals, medications), unstructured text (clinical notes, radiology reports), and genomic data. Constructing a complete patient state representation that integrates these heterogeneous modalities remains an open challenge, yet is necessary for world models that aspire to comprehensive clinical reasoning. 

### **6.8 Educational Measurement** 

Educational measurement studies how learners’ knowledge, abilities, and reasoning processes can be inferred from observable educational data. The field spans a broad range of tasks, including ability estimation, student modeling, automated assessment, and learning analytics. Across these settings, the common objective is to recover latent cognitive constructs from partial observations and to characterize how these constructs evolve under instructional interactions. 

From the perspective of world models, educational measurement can be reinterpreted as learning a dynamical model of a learner’s cognitive environment. In this formulation, the learner is treated as a partially observable environment, instructional interventions (e.g., exercises, hints, feedback, or curriculum choices) play the role of actions, and student behaviors (e.g., answers, explanations, or scores) are treated as observations. This interpretation is consistent with the central goal of world models: learning latent state representations together with transition and observation mechanisms that support prediction, simulation, and downstream decision making. For clarity, in this survey we use the term _educational world model_ to denote a world-model formulation of educational measurement, in which the learner is treated as a partially observable dynamical system whose latent cognitive state evolves under instructional actions. 

90 


Figure 4: Educational measurement viewed as a world model of learning dynamics. The figure combines the standard knowledge-tracing pipeline (interaction history _→_ latent knowledge estimation _→_ response prediction) with the latent-state formulation used in world models (state inference _→_ dynamics _→_ observation). This design is motivated by classical student modeling and knowledge tracing on the one hand, and by latent world-model architectures used in model-based reinforcement learning on the other. 

Formally, let _st_ denote the learner’s latent cognitive state at time step _t_ , where _st_ may encode knowledge mastery, misconceptions, strategy use, or other unobserved cognitive variables. Let _at_ denote an instructional action applied at time _t_ , such as assigning an exercise, providing feedback, or selecting the next learning activity. Let _ot_ denote the observable outcome at time _t_ , such as a correctness label, a score, a textual explanation, or another behavioral trace. Educational measurement under a world-model view can then be written as 


In Eq. 23, the transition model describes how the latent cognitive state evolves after the learner interacts with an instructional action and produces an observation. In Eq. 24, the observation model maps the updated latent state to the next observable behavior. This decomposition closely parallels the structure of latent world models in model-based reinforcement learning, where hidden state, dynamics, and observation are modeled jointly. 

As illustrated in Fig. 4, this perspective provides a unified way to connect traditional educational measurement with modern world-model architectures. Student interaction histories are first encoded into a latent knowledge state; a learning-dynamics module then models how this state changes under instructional actions; finally, an observation module predicts externally visible outcomes such as correctness, scores, or explanations. This view is useful because it not only covers response prediction, but also naturally suggests simulation of future learning trajectories and planning of instructional strategies. 

91 

**Structural correspondence between education and world models.** The mapping in Eqs. 23– 24 clarifies why educational measurement is a natural application domain for world-model thinking. The latent state _st_ plays the role of the learner’s hidden knowledge space; the transition model captures learning, forgetting, and other state changes caused by instruction; and the observation model explains how latent cognition gives rise to visible behavior. Under this view, student modeling methods can be interpreted as domain-specific latent-dynamics models, even when they were not originally introduced using the vocabulary of world models. 

**Classical student models as early latent-dynamics models.** Classical educational measurement already contains important ingredients of this formulation. Bayesian Knowledge Tracing (BKT) models each skill as a binary latent variable _Lt ∈{_ 0 _,_ 1 _}_ indicating whether the skill is unmastered or mastered. The transition from one latent state to the next is governed by a learning probability 


where _p_ learn denotes the probability that the learner acquires the skill between two interaction steps. The observation model then accounts for stochastic response noise through slip and guess parameters: 


where _ot_ = 1 means that the learner answers correctly, _p_ slip is the probability of making an error despite mastery, and _p_ guess is the probability of answering correctly without mastery. Although BKT is simple and skill-local, it is already an explicit latent-state transition model. [369] 

Item Response Theory (IRT) emphasizes the observation side of educational measurement. In the basic one-parameter logistic form, the probability that learner _i_ answers item _j_ correctly is 


where _θi_ denotes the learner’s latent ability and _βj_ denotes the difficulty of the item. IRT is highly interpretable and foundational in psychometrics, but by itself it is primarily static: it measures latent ability from observations rather than modeling rich temporal state evolution. [370] 

**Neural latent-dynamics models for student state tracking.** The shift from classical psychometrics to modern knowledge tracing reflects a shift from low-dimensional parametric state models to more expressive latent simulators. Deep Knowledge Tracing (DKT) uses recurrent neural networks to summarize interaction history into a continuous hidden state: 


where _xt_ encodes the current interaction (typically the question-response pair), _ht_ is the latent representation of the learner’s state, _W_ and _b_ are learnable parameters, and _yt_ is the predicted probability vector for future responses. Compared with BKT, DKT replaces hand-designed parametric transitions with a learned continuous-state dynamics model that can capture more complex dependencies in learning sequences. [371] 

Subsequent work increasingly enriched this latent-dynamics view. DKVMN separates concept memory from mastery memory, allowing the model to represent which concepts exist and how well each concept is mastered over time. [372] SAKT uses self-attention to select relevant prior interactions for the current prediction, thereby improving modeling under sparse histories. [373] SAINT introduces a deeper encoder-decoder Transformer formulation for knowledge tracing, while 

92 

AKT integrates attentive sequence modeling with interpretable components inspired by cognitive and psychometric considerations. [374, 375] More recent models continue this trend: DTransformer emphasizes diagnostic and stable state estimation, HiTSKT models hierarchical/session-aware sequence structure, and LKT brings pretrained language-model representations into knowledge tracing when question and concept text are available. [376–378] Together, these methods can be interpreted as increasingly expressive latent world models of learning processes. 

**Structured observation and generative assessment.** A central challenge for educational world models is that the observation space is often far richer than a binary correct/incorrect label. Many authentic assessments involve open-ended text, explanations, short answers, essays, or multicriteria rubrics. This makes the observation model in Eq. 24 substantially harder: the system must map latent cognitive states to semantically rich outputs and, in many cases, also infer structured evidence from those outputs. 

Recent LLM-based assessment studies show that large language models can achieve competitive performance in automated essay scoring and broader automated assessment settings, though validity, robustness, and rubric alignment remain central concerns. [379–381] Within this context, AutoSCORE provides a particularly natural example for this survey because it can be interpreted as a structured observation model. Instead of directly mapping a student response to a final score, AutoSCORE first extracts rubric-aligned scoring components from the response and then aggregates them into a final assessment: 


where _o_<sup>text</sup> _t_ is the raw open-ended student response and _o_<sup>struct</sup> _t_ is its structured rubric-aligned representation. A second scoring stage then maps this structured representation to the final score. From a world-model perspective, this is appealing because it turns unstructured observations into diagnostically meaningful components that can more directly support latent-state updating. [382] 

**Critical synthesis: from response prediction to imaginative instructional planning.** A key insight from the literature is that educational measurement has become increasingly strong at _predicting_ immediate student performance, but it has not yet fully exploited the _simulation and planning_ capabilities that define modern world models. If the transition model _T_<sup>�</sup> in Eq. 23 were learned with sufficient fidelity, one could simulate future latent trajectories under counterfactual instructional choices: 


where _s_ � _t_ +1: _t_ + _H_ denotes the simulated future latent states over a horizon of length _H_ , _T_<sup>�</sup> is the learned transition model, _st_ is the current latent learner state, and _{a_<sup>_′_</sup> _k_<sup>_}t_</sup> _k_<sup>+</sup> =<sup>_H_</sup> _t_<sup>_−_1</sup> is a candidate sequence of future instructional actions. Such simulation would support counterfactual questions of direct pedagogical interest: which curriculum path is likely to maximize long-term retention, reduce cognitive overload, or accelerate mastery for a particular learner? 

This research gap should be framed carefully. It does not mean that educational AI lacks student models; on the contrary, the field has developed a rich ecosystem of psychometric, sequential, and assessment models. Rather, the opportunity is that these methods have only partially been integrated into full simulation-based world-model pipelines. In this sense, educational measurement is already close to world modeling in spirit, but still early in its use of explicit imaginative rollouts, long-horizon planning, and adaptive counterfactual reasoning. That gap makes the domain especially promising for future work on intelligent tutoring systems, assessment-aware planning, and learner-specific adaptive world models. 

93 

### **6.9 Business and Finance** 

Business and financial systems represent a fundamentally different regime for world modeling, where the objective shifts from simulating deterministic physical dynamics to reasoning under severe uncertainty, hidden states, and strategic human interactions. Unlike classical environments governed by stable transition laws, corporate and financial ecosystems are shaped by latent socioeconomic factors and the adaptive behavior of competing agents. Consequently, world models in this domain must operate not as rigid physical engines, but as highly adaptable inferential and decision-support systems. 

Table 8: World modeling in business and finance: core dimensions and methodologies. 

|**Dimension**|**Financial Context**|**Modeling Approach**|**Strategic Value**|
|---|---|---|---|
|Latent State|Unobservable drivers|Belief POMDPs, latent<br>variable models|Asset allocation under<br>uncertainty|
|Market Dynamics|Non-stationary regime<br>shifts|Adaptive state-space<br>models|Long-horizon risk<br>management|
|Financial Signals|Noisy, delayed, or<br>alternative data|Bayesian filtering,<br>representation learning|Real-time market<br>inference|
|Interactions|Algorithmic &<br>competitor behaviors|Game-theoretic MARL|Anticipating strategic<br>responses|
|Evaluation|Counterfactual strategy<br>outcomes|Causal inference, offline<br>RL|Risk-free policy<br>backtesting|
|Reflexivity|Market self-impact and<br>price impact|Policy-conditioned<br>dynamics|Handling self-referential<br>markets|


#### **6.9.1 Beyond physical laws: the belief-modeling paradigm.** 

Financial markets and corporate architectures are defined by severe partial observability, multiagent strategic interactions, and structural non-stationarity. The underlying true state of the system—comprising institutional order flow, market sentiment, shifting consumer demand, and competitor strategies—is only indirectly observable through noisy or delayed signals. 

Because of this, world models in business and finance cannot function as deterministic simulators; rather, they must operate strictly as belief models. The latent state does not correspond to a concrete spatial configuration, but instead represents a probability distribution over hidden economic drivers. This reframes the fundamental modeling objective: moving from predicting observable trajectories to continuously maintaining and updating coherent beliefs about latent factors, an approach that naturally aligns with the principles of partially observable Markov decision processes (POMDPs) [383]. 

#### **6.9.2 Methodological trajectories.** 

Existing applications of world models in this domain can be broadly categorized into three methodological trajectories. The first encompasses time-series predictive models, leveraging architectures such as recurrent neural networks and Temporal Fusion Transformers [384] to map historical observations directly to future asset prices or operational metrics. While highly effective for pure forecasting, these approaches typically lack an explicit, manipulable latent structure, thereby providing limited support for counterfactual intervention or causal decision analysis. 

94 

To address this limitation, a second class of methods employs latent dynamics models, predominantly inspired by state-space formulations. By introducing hidden variables that capture macroeconomic regimes (e.g., bull vs. bear markets), liquidity conditions, or latent risk factors, these models explicitly separate observable signals from their underlying generative drivers. This enables more robust reasoning over sudden regime shifts and long-horizon dependencies, bringing them significantly closer to the core principles of world modeling. 

A third, increasingly critical direction formulates financial systems as multi-agent environments [385]. In this paradigm, market dynamics are viewed as emergent phenomena arising from the interactions of heterogeneous agents—such as algorithmic traders, institutions, and retail consumers—each pursuing distinct, often competing objectives. As a result, the evolution of the system depends not only on exogenous economic conditions but also on the strategic adaptations of other participants, intrinsically introducing a game-theoretic dimension into the world model. 

#### **6.9.3 The imperative of counterfactual reasoning in corporate and financial strategy.** 

In business and finance, strategic decision-making fundamentally revolves around evaluating alternatives: comparing different algorithmic trading strategies, portfolio allocations, dynamic pricing policies, or supply chain interventions. This operational reality necessitates rigorous counterfactual reasoning—estimating what would have transpired under a different decision while holding the underlying latent market conditions constant. 

Formally, this is expressed by comparing expected outcomes under alternative interventions via the _do_ -calculus framework [251]: 


which precisely quantifies the causal impact of a chosen action. In offline settings, causally grounded world models transform historical transaction logs and market data into a dynamic substrate for policy evaluation [386], enabling institutions to stress-test strategies without incurring real-world financial risk. 

#### **6.9.4 Fundamental bottlenecks: non-stationarity, identifiability, and reflexivity.** 

Despite these conceptual advances, the deployment of world models in finance faces formidable bottlenecks. First, non-stationarity is pervasive: macroeconomic conditions, regulatory frameworks, and collective agent behaviors evolve continuously, leading to severe distribution shifts that rapidly degrade learned dynamics. Second, non-identifiability poses a critical theoretical challenge; multiple latent configurations may explain the observed historical data equally well while yielding drastically divergent counterfactual predictions. 

Third, and perhaps most uniquely, financial systems exhibit reflexivity [387]—a phenomenon where the deployment of a model and its subsequent actions directly alter the environment it is attempting to model. This creates self-referential feedback loops where the environment is no longer independent of the agent’s policy _π_ : 


Such endogenous effects violate the standard reinforcement learning assumption of a fixed, exogenous environment, fundamentally complicating long-horizon prediction and robust control. 

Ultimately, these characteristics dictate that world models for business and finance must transcend the role of passive environmental simulators. Instead, they must be rigorously engineered as belief-driven, strategically aware, and causally grounded systems, uniquely capable of operating amid deep uncertainty, adversarial interaction, and continuous structural evolution. 

95 

## **7 Evaluation Protocols and Benchmarks** 

Evaluating world models is fundamentally more complex than evaluating standard generative models or policies in isolation. A world model must simultaneously satisfy multiple requirement— perceptual fidelity, temporal consistency, physical plausibility, action-conditioned accuracy, and downstream task utility–yet no single metric or benchmark captures all of these dimensions. This section surveys the evaluation landscape along three axes: the metrics used to quantify model quality (Section 7.1), the benchmark environments and datasets against which models are tested (Section 7.2). 

### **7.1 Common Evaluation Metrics** 

Evaluation metrics for world models can be organized into four families, each measuring a distinct facet of model quality. 

**Perceptual quality metrics.** These metrics assess the visual fidelity of generated observations. The _Fréchet Inception Distance_ (FID) [388] computes the Fréchet distance between the feature distributions (extracted from an Inception-v3 network trained on ImageNet) of generated and real image sets. Lower FID indicates higher distributional similarity. The _Fréchet Video Distance_ (FVD) [389] extends this to video by using features from an Inflated 3D ConvNet (I3D) trained on the Kinetics dataset, capturing both spatial quality and coarse temporal coherence. FVD has become the de facto standard for video generation evaluation, though it has known limitations: it prioritizes per-frame quality over temporal consistency (a phenomenon termed “content bias” [390]), and it is sensitive to sample size, yielding non-zero values even for identical distributions due to finite-sample estimation noise [389]. 

Frame-level metrics complement distributional measures. The Structural Similarity Index (SSIM) [391] evaluates luminance, contrast, and structural information between pairs of images, correlating better with human perception than pixel-wise MSE. The _Peak Signal-to-Noise Ratio_ (PSNR) measures pixel-level reconstruction accuracy. The _Learned Perceptual Image Patch Similarity_ (LPIPS) [392] computes distances in deep feature space (typically VGGNet), achieving strong alignment with human perceptual judgments. However, all frame-level metrics are computed perframe without access to temporal context, making them blind to inter-frame consistency—a critical property for world models that must generate coherent trajectories. 

**Task-performance metrics.** In model-based RL, the primary evaluation metric is _cumulative episodic return_ , often normalized against human performance. The _Human-Normalized Score_ (HNS) is defined as HNS = ( _R_ agent _− R_ random) _/_ ( _R_ human _− R_ random), where _R_ denotes cumulative reward. Mean and median HNS across games are the standard aggregate statistics for the Atari 100k benchmark [393]. Agarwal et al. [394] advocated replacing mean/median with the _interquartile mean_ (IQM) and stratified bootstrap confidence intervals, demonstrating that mean HNS is dominated by outlier games and median HNS discards too much information. For continuous control (DeepMind Control Suite), raw episodic returns—averaged over seeds and normalized by an expert policy—are standard. 

In autonomous driving, task metrics include _driving score_ (a composite of route completion and infraction penalties), _success rate_ , _collision rate_ , and planning-specific measures such as _L2 trajectory error_ and _displacement error_ . The CARLA Leaderboard [289] reports a driving score from 0 to 100. Bench2Drive [395] introduced multi-ability evaluation with fine-grained driving competency scores. In robotics, _success rate_ on manipulation or locomotion tasks is standard, evaluated over multiple trials with randomized initial conditions. 

**Temporal consistency and dynamics metrics.** VBench [396] decomposed video generation 

96 

quality into 16 disentangled dimensions, including subject consistency, background consistency, temporal flickering, motion smoothness, and dynamic degree. VBench 2.0 [397] extended this to intrinsic faithfulness, adding physics plausibility, commonsense reasoning, and human anatomy consistency. WorldBench [398] proposed concept-specific physical evaluation using segmentationbased foreground mIoU against ground-truth physics simulations (generated via Kubric/PyBullet), revealing that state-of-the-art video world models achieve only 45% mIoU on physical reasoning tasks. These emerging benchmarks represent a shift from distributional perceptual metrics toward diagnostic evaluation of specific physical and causal properties. 

**Prediction accuracy metrics.** For 3D world models, _Chamfer distance_ measures the geometric fidelity of predicted point clouds against ground truth. Copilot4D [67] reported a 65% reduction in Chamfer distance for 1-second LiDAR prediction. Occupancy-based models (OccWorld [66]) use _Intersection-over-Union_ (IoU) on predicted voxel grids. For offline RL world models, _one-step prediction error_ (MSE in latent or observation space) and _multi-step rollout divergence_ quantify dynamics model accuracy independently of downstream policy quality. 

### **7.2 Benchmark Environments and Datasets** 

Benchmark environments for world models span four primary application domains, each with distinct evaluation protocols and data characteristics. 

**Reinforcement learning benchmarks.** The _Atari 100k_ benchmark [393] restricts agents to 100,000 environment steps (approximately 2 hours of real-time gameplay) across 26 games from the Arcade Learning Environment (ALE) [399]. This data-efficiency constraint makes it the primary testbed for model-based RL methods. EfficientZero [102] achieved 194% mean HNS; DIAMOND [37] set the current record for agents trained entirely within a world model at 1.46 mean HNS. The _DeepMind Control Suite_ (DMC) [400] provides 20+ continuous control tasks from pixels with a standard budget of 10<sup>6</sup> environment steps, evaluating locomotion and manipulation under diverse physics. DreamerV3 [40] demonstrated cross-domain generality on DMC with fixed hyperparameters. Additional RL benchmarks include _Crafter_ [401] (a procedurally generated survival game testing 22 achievements), _Minecraft_ (open-ended exploration with sparse rewards), and _Memory Maze_ [402] (testing long-term memory in world models). 

_D4RL_ [403] provides standardized offline RL datasets across locomotion, navigation, and manipulation tasks, enabling evaluation of world models that must learn dynamics from fixed datasets without online interaction. Recent work has shown that diffusion-based world models achieve 44% improvement over one-step models on D4RL locomotion tasks. However, D4RL’s tasks are increasingly saturated; D5RL [404] has been proposed with more realistic robotic tasks where current methods struggle to outperform behavioral cloning. 

**Autonomous driving benchmarks.** _nuScenes_ [287] provides 1,000 driving scenes (5.5 hours) with 360° sensor coverage and 3D annotations, serving as the dominant evaluation dataset for driving world models. However, growing consensus holds that nuScenes was designed for perception rather than planning, and open-loop L2 trajectory error on nuScenes correlates poorly with closedloop driving performance [395]. The _CARLA simulator_ [289] provides closed-loop evaluation via the CARLA Leaderboard, where agents drive through predefined routes and receive composite driving scores. _Bench2Drive_ [395] (NeurIPS 2024) introduced 10,000 clips with multi-ability closed-loop evaluation, explicitly arguing that L2 error is not a meaningful indicator and that the community should move beyond open-loop nuScenes planning results. _NAVSIM_ [405] (NeurIPS 2024) provided the first direct comparison between model families previously benchmarked exclusively on either CARLA or nuScenes, revealing that simple methods can match large-scale architectures on challenging scenarios. _nuPlan_ [406] extends nuScenes with a closed-loop simulator for planning 

97 

#### evaluation. 

**Video generation and scene understanding benchmarks.** Measuring the gap between visual fidelity and physical understanding requires evaluation protocols that go beyond traditional perceptual metrics. The evaluation of video prediction and generation models has evolved substantially alongside model capabilities, progressing from simple pixel-level metrics to multidimensional assessment frameworks. Table 9 summarizes the principal evaluation protocols of video prediction and scene understanding. 

Traditional metrics assess low-level visual quality: **Fréchet Video Distance** (FVD) [389] extends the image-level FID to video by comparing distributions of features extracted from a pretrained video classifier, and remains the most widely reported metric for unconditional and conditional video generation. **SSIM** and **LPIPS** measure structural similarity and perceptual distance at the frame level. However, Luo et al. [305] demonstrated that FVD correlates poorly with human judgments for modern high-fidelity generators, motivating the development of more discriminative metrics. 

Recent benchmarks take a multidimensional approach. **VBench** [396] introduced a comprehensive evaluation suite decomposing video generation quality into 16 fine-grained dimensions— including subject consistency, background consistency, temporal flickering, motion smoothness, aesthetic quality, and text-video alignment—enabling diagnosis of specific failure modes rather than relying on a single aggregate score. **VBench 2.0** [397] extended this framework to assess _intrinsic faithfulness_ , evaluating whether generated videos obey real-world physical and commonsense constraints. **EvalCrafter** [407] provided an evaluation framework spanning visual quality, text-video alignment, motion quality, and temporal coherence, benchmarking a broad range of video generation models. **WorldSimBench** [304] focused specifically on evaluating video generation models as world simulators, introducing metrics for action controllability, physical consistency, and interactive fidelity that standard visual quality metrics fail to capture. 

A persistent challenge across all evaluation approaches is the gap between perceptual quality and physical fidelity: a video can be visually stunning yet physically implausible, and no current metric reliably captures this distinction at scale. The development of evaluation protocols that assess physical understanding, causal consistency, and interactive reliability—beyond mere visual appeal—remains a critical open problem for the field. 

Table 9: Representative evaluation benchmarks and metrics for video prediction and scene understanding. 

|**Benchmark / Metric**|**Year**|**Type**||**Key Focus**|
|---|---|---|---|---|
|FVD [389]|2019|Distribution|metric|Video-level<br>distributional<br>quality|
|VBench [396]|2024|Multi-dim.<br>mark|bench-|16<br>fine-grained<br>quality<br>di-<br>mensions|
|VBench 2.0 [397]|2025|Multi-dim.<br>mark|bench-|Intrinsic<br>faithfulness<br>and<br>physics|
|EvalCrafter [407]|2024|Multi-dim.<br>mark|bench-|Visual,<br>motion,<br>and align-<br>ment quality|
|WorldSimBench [304]|2025|Simulator<br>mark|bench-|Action<br>controllability<br>and<br>physical consistency|
|Beyond FVD [305]|2025|Metric anal|ysis|Enhanced<br>metrics<br>beyond<br>FVD limitations|


**Robotics benchmarks.** Robot world models are evaluated through downstream task suc- 

98 

cess rates on manipulation benchmarks such as _RLBench_ [281] (100 hand-designed tasks with proprioceptive and visual observations), _CALVIN_ [326] (language-conditioned long-horizon manipulation), and _Meta-World_ [282] (50 robotic manipulation tasks for multi-task and meta-learning). DayDreamer [83] evaluated on real robot hardware, measuring locomotion distance and manipulation success rate from limited real-world interactions. DreMa [65] reported one-shot policy learning accuracy on a Franka Emika Panda robot. Table 10 provides an overview of the principal benchmarks. 

Table 10: Principal benchmark environments for world model evaluation. 

|**Benchmark **|**Domain**|**Eval.**<br>**Type**|**Budget /**<br>**Scale**|**Primary**<br>**Metrics**|**Top Methods**|
|---|---|---|---|---|---|
|Atari<br>100k [393]|RL /<br>Games|Online,<br>closed|100k steps (_∼_2<br>hrs)|Mean/Median<br>HNS, IQM|DIAMOND,<br>EfficientZero|
|DMC [400]|Cont. ctrl|Online,<br>closed|1M steps|Episodic return|DreamerV3,<br>TD-MPC2|
|D4RL [403]|Offline RL|Offline|Fixed datasets|Normalized<br>score|DWM, LEQ|
|nuScenes [287]|Driving|Open-loop|5.5 hrs, 1k<br>scenes|L2 error, FID,<br>FVD|GAIA-1, Vista|
|CARLA [289]|Driving|Closed-<br>loop|Predefined<br>routes|Driving score,<br>SR|Bench2Drive<br>entries|
|VBench [396]|Video gen.|Automated|16 dimensions|Composite<br>quality|Sora, Kling|
|RLBench [281]|Robotics|Task<br>success|100 tasks|Success rate|PerAct,<br>RoboMM|


## **8 Major Challenges and Limitations** 

Despite rapid progress, world models still face several fundamental challenges that span architectures, methodological families, and application domains. These are not simply engineering limitations, but often reflect deeper tensions between learned dynamics models and the complexity of real-world environments. This section examines seven major challenges: long-horizon consistency and error compounding, scalability and computational cost, the sim-to-real transfer gap, fragmented evaluation and benchmarking, data efficiency and representation learning, safety and robustness in high-stakes settings, and the still unresolved problem of multi-modal grounding. 

### **Long-Horizon Consistency and Error Compounding** 

Autoregressive world models generate future states by recursively feeding their own predictions as inputs, a process that causes small per-step inaccuracies to accumulate multiplicatively over the rollout horizon. Janner et al. [48] formalized this risk by deriving monotonic improvement bounds showing that the return discrepancy between the learned model and the true environment grows linearly with both the rollout length _k_ and the single-step model error _εm_ . In practice, this means that a world model with only 1% per-step prediction error can diverge dramatically from 

99 

reality after just tens of imagined steps, producing physically implausible or semantically incoherent trajectories. Ding et al. [104] demonstrated this empirically for offline RL, showing that predicted returns “quickly collapse as rollout length increases” when using standard one-step autoregressive dynamics. 

**Controlled rollout horizons.** The most widely adopted mitigation strategy is to limit the temporal extent of imagined rollouts. MBPO [48] initiates short model-based rollouts (starting at _k_ =1 and gradually extending to _k_ =25) from real states stored in a replay buffer, then mixes these imagined transitions with real data for off-policy training. This _branched rollout_ design prevents long-horizon error accumulation while still gaining substantial sample efficiency—achieving the theoretical monotonic improvement guarantee within the trust region of the learned dynamics. DreamerV3 [8] employs a complementary approach: rather than limiting rollout length, it stabilizes long-horizon imagination through a suite of robustness techniques including symlog-transformed predictions that compress large value ranges, percentile-based return normalization, and KL balancing with free bits that prevents posterior collapse. Together, these enable stable actor-critic training across 150+ diverse tasks with rollout horizons of 15 steps using a single fixed hyperparameter set. 

**Multi-step and parallel prediction.** An alternative to sequential one-step rollouts is to predict multiple future steps simultaneously. The Diffusion World Model (DWM) [104] replaces the autoregressive paradigm with a diffusion process that generates multi-step future states and rewards concurrently in a single forward pass, bypassing the recursive error chain entirely and achieving a 44% performance improvement over one-step models on D4RL locomotion benchmarks. Diffusion Forcing [294] offers a theoretically motivated hybrid: it assigns independent noise levels to each token in a sequence during training, unifying the variable-length generation of autoregressive models with the holistic coherence of full-sequence diffusion. This enables stable rollouts well past the training horizon where standard autoregressive baselines diverge, because the model learns to denoise partial trajectories at multiple corruption levels simultaneously. 

**Latent overshooting and consistency objectives.** PlaNet [31] introduced _latent overshooting_ , a multi-step variational inference objective that regularizes the world model’s latent predictions over extended horizons by comparing multi-step prior predictions with posterior-inferred states. While subsequent work in the Dreamer family found that latent overshooting may be unnecessary when actor-critic optimization is performed in imagination [408], the underlying principle— providing dense supervision beyond one-step prediction—has proven influential. EfficientZero [102] implements a related idea through a self-supervised temporal consistency loss that aligns multistep model predictions with encoder representations of actual future observations, providing rich dynamics supervision independent of reward sparsity. 

**Long-context architectures.** The limited temporal memory of recurrent world models (RSSM, GRU) exacerbates compounding error, since information from distant past observations is progressively lost. Transformer-based world models [36, 74] address this through full-history attention but incur quadratic computational cost. State-space models offer a scalable alternative: Po et al. [142] demonstrated that linear RNN architectures with structured state-space parameterizations can capture long-range temporal dependencies at constant per-frame cost, outperforming transformer baselines on spatial retrieval tasks in Memory Maze and Minecraft. StateSpaceDiffuser [409] integrates a Mamba-based state-space model into a diffusion world model, where the SSM branch provides persistent temporal memory while the diffusion branch generates high-fidelity frames, maintaining coherent visual context for an order of magnitude more steps than diffusiononly baselines. EDELINE [410] similarly couples Mamba SSMs with diffusion dynamics, introducing dynamic loss harmonization to balance multi-task learning of reward and termination prediction over extended horizons. 

100 

**Hierarchical temporal abstraction.** Hierarchical world models reduce compounding error by operating at multiple temporal resolutions, so that high-level predictions span longer horizons with fewer recursive steps. Director [411] decomposes planning into a high-level “manager” that selects latent subgoals and a low-level “worker” that executes short-horizon motor commands, enabling successful navigation in 3D mazes that flat world models cannot solve. THICK [412] learns a hierarchy of world models with adaptive temporal abstractions from discrete latent dynamics, where lower levels update sparsely in time and higher levels predict only at context-change boundaries. Schiewer et al. [408] provide a systematic evaluation of hierarchical MBRL, documenting both the benefits (reduced effective rollout depth) and the challenges (difficulty of learning appropriate abstraction boundaries, risk of model exploitation at each level). 

Despite these advances, long-horizon consistency remains the single most significant technical bottleneck for world models. The fundamental tension is that extending the imagination horizon increases the planning capacity of the agent but simultaneously amplifies the risk of exploiting model inaccuracies. No current approach fully resolves this trade-off: controlled rollout horizons sacrifice long-term planning, multi-step prediction methods struggle with complex visual observations, and hierarchical models introduce additional learning challenges at each level. Developing world models that maintain calibrated predictions over hundreds or thousands of steps—matching the temporal horizons required for real-world planning in domains such as autonomous driving and medical treatment—remains a critical open problem. 

### **Scalability and Computational Cost** 

State-of-the-art world models span a computational spectrum that ranges from lightweight latent dynamics models trainable on a single GPU to foundation-scale systems requiring thousands of accelerators and millions of GPU-hours. GAIA-1 [62], a 9-billion-parameter generative world model for autonomous driving, pairs a 6.5B autoregressive transformer with a 2.6B video diffusion decoder trained on 4,700 hours of real-world driving data. NVIDIA’s Cosmos [14] released open-weight world foundation models at 4B, 7B, 12B, and 14B parameters trained on over 20 million hours of video. DeepMind’s Genie [13] scales to 11 billion parameters with a spatiotemporal video tokenizer and autoregressive dynamics model trained on unlabeled internet video. These scales make training prohibitively expensive for most research groups: the Open-Sora project [293] estimated that reproducing a commercial-quality video generation model costs approximately $200K in compute, and even this represents a substantial reduction from the estimated costs of proprietary systems like Sora [10]. 

**Inference-time bottlenecks.** For interactive applications—robotics, game simulation, autonomous driving—inference latency is as critical as training cost. Diffusion-based world models are particularly affected because each predicted frame requires multiple denoising iterations. DIAMOND [37] demonstrated that the EDM framework [173] enables stable autoregressive generation with as few as three denoising steps, but this still limits throughput compared to single-pass autoregressive models. GameNGen [413] achieved real-time DOOM simulation at 20 FPS on a single TPU by fine-tuning Stable Diffusion with four denoising steps, and further distillation reduced this to a single step at 50 FPS. However, scaling such approaches to higher-resolution, more complex environments remains challenging. Oasis [159] demonstrated real-time Minecraft-like world generation at 360p and 20 FPS using a Diffusion Transformer architecture on NVIDIA H100 GPUs, but resolution and visual fidelity remain limited compared to offline generation systems. 

**Consistency and distillation approaches.** Consistency models [189] offer a principled framework for reducing the sampling cost of diffusion models by training networks that map any noise level directly to the clean data manifold in a single step. Latent consistency models [414] 

101 

extended this to latent diffusion, achieving high-quality image generation in 2–4 steps with only 32 A100 GPU-hours of training. For video, DOLLAR [415] combines variational score distillation with consistency distillation for few-step video generation, achieving up to 278 _×_ acceleration over the teacher model’s sampling procedure. Applying these distillation techniques specifically to world model inference—where the quality of each predicted frame directly affects downstream planning— is an active research direction, though the interaction between distillation-induced approximation errors and compounding rollout errors remains poorly understood. 

**Token reduction and efficient architectures.** A complementary strategy reduces computational cost by minimizing the number of tokens processed per timestep. ∆-IRIS [155] encodes stochastic frame-to-frame deltas rather than full observations, dramatically reducing per-timestep token count while achieving state-of-the-art performance on Crafter with an order-of-magnitude training speedup over the original IRIS. STORM [36] fuses each observation into a single continuous latent token (versus IRIS’s 16 discrete tokens per frame), enabling transformer-based world modeling with substantially lower attention cost and achieving 126.7% mean human performance on Atari 100k with only 4.3 hours of training on a single GPU. These results suggest that architectural efficiency innovations can deliver disproportionate cost reductions without sacrificing downstream task performance, potentially democratizing world model research beyond well-resourced industrial laboratories. 

**Architecture-level trade-offs.** The choice among RSSM, transformer, diffusion, and statespace architectures involves fundamental trade-offs between computational cost, memory, and predictive capacity. RSSM-based models (Dreamer family) are the most computationally efficient, with _O_ (1) per-step cost independent of history length, but compress all temporal information into a fixed-size hidden state that limits long-range memory. Transformer-based models (IRIS, STORM) offer superior long-range dependency modeling but incur _O_ ( _T_<sup>2</sup> ) attention cost in context length _T_ , which becomes prohibitive for long episodes with high-resolution observations. State-space models [142] provide _O_ ( _T_ ) complexity with strong long-range modeling, but their application to world modeling is still nascent. Diffusion models (DIAMOND, GameNGen) achieve the highest visual fidelity but require multiple sequential denoising steps per frame, making them the slowest at inference unless distillation is applied. No single architecture currently dominates across all evaluation dimensions, and the optimal choice depends critically on the deployment constraints of the target application. 

### **Sim-to-Real Transfer and Domain Gap** 

World models trained in simulation benefit from unlimited data, perfect state access, and safe exploration, but the resulting models often fail when deployed in the real world due to systematic discrepancies between simulated and physical environments. This _sim-to-real gap_ manifests along two largely orthogonal axes: the _visual domain gap_ , arising from differences in rendering quality, lighting, textures, and sensor characteristics; and the _dynamics domain gap_ , arising from inaccurate contact models, simplified friction and deformation physics, and unmodeled latencies and noise in real actuators and sensors. 

**Domain randomization.** The most established approach to bridging the visual domain gap is domain randomization, which trains models on a distribution of simulated environments with randomly varied visual and physical parameters, encouraging representations that are invariant to superficial variation. Tobin et al. [416] demonstrated that object detectors trained on randomized simulated images transfer to real-world perception without any real training data. Chen et al. [417] subsequently provided a theoretical framework establishing sharp bounds on the sim-to-real gap under domain randomization, proving that transfer can succeed under mild distributional coverage 

102 

conditions without requiring real-world samples. In the world model setting, domain randomization has been applied to train both visual encoders and dynamics models, with the expectation that randomization forces the model to capture invariant physical structure rather than simulationspecific artifacts. However, domain randomization alone is often insufficient for the dynamics gap, as it randomizes parameters within a fixed physics engine whose structural assumptions (e.g., rigidbody contact models) may not match reality. 

**Direct real-world learning.** DayDreamer [83] demonstrated an alternative paradigm: training Dreamer-style world models directly on real-world interaction data without any simulation. A quadruped robot learned to walk in approximately one hour, and a robotic arm learned pick-andplace in ten minutes, using only real sensor data for both world model training and imaginationbased policy optimization. This approach completely avoids the sim-to-real gap but is constrained by the cost and risk of real-world data collection, limiting its applicability to domains where hardware is accessible and failure consequences are manageable. Data augmentation techniques such as DrQ [418], which applies random image shifts to improve sample efficiency in pixel-based RL, can partially compensate for the limited visual diversity of real-world datasets. 

**Modular sim-to-real adaptation.** A promising middle ground exploits the modular structure of world models to selectively adapt only the components most affected by domain shift. SimDist [419] pretrains the full world model stack (encoder, dynamics, reward, and value models) in simulation using privileged state information, then freezes all components except the dynamics model, which is fine-tuned on a small amount of real-world data via supervised learning. This _simulation distillation_ approach leverages the insight that the encoder and value representations learned in simulation are largely transferable, while the dynamics model—which must capture real contact physics, friction, and latency—requires adaptation. Notably, SimDist documented that naive end-to-end RL fine-tuning frequently causes catastrophic forgetting of simulation-acquired knowledge, motivating the modular freezing strategy. ReDRAW [420] takes a complementary approach by learning latent-state dynamics residuals: a base world model pretrained in simulation is augmented with a lightweight residual correction network that captures the sim-to-real dynamics gap without modifying the base model’s representations, demonstrated on both MuJoCo domains and a physical Duckiebot lane-following task. 

**Teacher-student distillation.** TWIST [421] introduces a teacher-student framework in which a teacher world model is trained with full state information in simulation, then supervises a student world model that receives only domain-randomized image observations. The student inherits the teacher’s dynamics understanding while learning visual representations robust to domain shift. Simulation-Guided Fine-Tuning (SGFT) [422] uses simulation-learned value functions for reward shaping during real-world exploration, achieving at least 2 _×_ improvement in sample efficiency on real robot manipulation tasks compared to baselines that do not exploit simulation priors. 

**Conditional world generation for domain transfer.** At the foundation model scale, Cosmos-Transfer1 [275] reframes the domain gap as a conditional generation problem: given simulated trajectories with semantic segmentation, depth maps, and edge inputs, a diffusion-based world model generates photorealistic video that preserves the scene structure and motion of the simulation while adopting realistic visual appearance. This approach has been demonstrated for both robotics and autonomous driving sim-to-real transfer, producing training data that narrows the visual domain gap without requiring real-world data collection for each new task. GenSim2 [276] complements this by using large language models to automatically generate diverse simulated tasks, assets, and scenarios, expanding coverage over the task variation that most often breaks sim-trained policies at deployment. 

**Remaining challenges.** Despite these advances, the sim-to-real gap remains one of the most practically significant obstacles in deploying world models. Contact-rich manipulation—involving 

103 

friction, deformation, and multi-point contact—is particularly challenging because the physics engines underlying most simulators make simplifying assumptions (rigid-body contacts, Coulomb friction) that diverge significantly from real-world mechanics. Multi-modal sensory integration compounds the problem: world models that fuse vision with proprioception and tactile sensing must bridge domain gaps in each modality simultaneously. Furthermore, the real world is nonstationary in ways that simulation is not: lighting changes, object wear, and environmental drift mean that even a well-adapted world model may degrade over time without continual adaptation mechanisms. 

### **Evaluation and Benchmarking** 

No consensus exists on how to evaluate world models comprehensively, and the fragmentation of evaluation protocols across application domains—RL, autonomous driving, video generation, robotics—impedes systematic comparison of architectural innovations and obscures fundamental limitations of current approaches. 

**The perceptual quality trap.** The most widely adopted metrics—Fréchet Inception Distance (FID), Fréchet Video Distance (FVD), SSIM, PSNR, and LPIPS—measure visual fidelity but not decision-relevant properties. Ge et al. [423] demonstrated that FVD is strongly biased toward perframe appearance quality over temporal realism: one can halve FVD scores simply by selecting static, motion-free videos, exposing a fundamental disconnect between the metric and the temporal dynamics that world models are designed to capture. Luo et al. [305] identified three additional critical FVD limitations—non-Gaussianity of I3D feature distributions, insensitivity to temporal distortions, and impractical sample-size requirements—and proposed JEDi (JEPA Embedding Distance), which requires only 16% of the samples needed for reliable FVD estimation while better correlating with human temporal quality judgments. Liu et al. [424] introduced Fréchet Video Motion Distance (FVMD), which evaluates motion consistency separately from appearance and reveals cases where FVD and VBench give inconsistent assessments compared to human judgment, particularly for videos with intensive motion. These critiques collectively suggest that the field’s reliance on FVD as a primary evaluation metric may be systematically misdirecting research toward perceptual quality at the expense of temporal and physical consistency. 

**Physics and causal reasoning benchmarks.** A growing family of benchmarks specifically targets the physical understanding of world models. WorldBench [398] provides concept-specific, disentangled physics evaluation using physically simulated ground-truth videos, testing intuitive physics properties (object permanence, scale consistency) and physical parameter estimation (friction, viscosity) in isolation. Its central finding is sobering: all tested state-of-the-art world models lack robust physical consistency, with foreground mIoU degrading sharply after 5–9 frames of autoregressive prediction. Physion [221] evaluates physical prediction using realistic 3D simulations across eight physical scenarios, comparing model predictions against human performance and finding that object-centric representations are necessary but insufficient for human-level physical reasoning. Physion++ [425] extends this by requiring online inference of latent physical properties (mass, friction, elasticity), revealing that all current models fail to reach human-level prediction when property inference is required. IntPhys [426] adapts the violation-of-expectation paradigm from developmental psychology, testing whether models can distinguish physically possible from impossible events involving object permanence and spatio-temporal continuity—with current models performing near chance. PhysBench [427] evaluates 75 vision-language models across over 10,000 entries and finds that even models excelling at commonsense reasoning struggle with physical world understanding. 

**World model-specific benchmarks.** Several recent benchmarks target world models specif- 

104 

ically rather than video generation in general. WorldModelBench [428] evaluates world modeling capabilities across 7 application domains and 56 subdomains with 67K human labels, assessing both instruction-following and physics-adherence dimensions. WorldSimBench [304] introduces a dual evaluation framework with explicit perceptual evaluation and implicit manipulative evaluation (measuring video-action consistency) across open-ended environments, autonomous driving, and robot manipulation. WorldScore [429] provides the first unified benchmark for world generation, evaluating 19+ models on controllability, quality, and dynamics through a decomposition into next-scene generation with camera trajectories. VBench [396] decomposes video generation quality into 16 hierarchical dimensions (subject consistency, motion smoothness, temporal flickering, spatial relationships, etc.), and VBench 2.0 [397] extends this to intrinsic faithfulness, evaluating physics plausibility, commonsense reasoning, and human anatomy consistency—arguing that prior benchmarks focus on visual convincingness rather than real-world adherence. 

**The open-loop vs. closed-loop evaluation gap.** In autonomous driving, the disconnect between open-loop evaluation (predicting future trajectories given recorded past) and closed-loop performance (executing in an interactive simulator) has been documented as a critical limitation. Li et al. [430] exposed that models achieve strong open-loop results on nuScenes by primarily relying on ego-vehicle status (velocity, heading) rather than perception, fundamentally undermining the validity of open-loop planning metrics. Bench2Drive [395] explicitly argues that open-loop L2 trajectory error does not reliably predict closed-loop driving ability, providing 2 million annotated frames across 44 interactive scenarios for proper closed-loop evaluation. NAVSIM [405] bridges this gap using non-reactive simulation on real-world nuPlan data, hosting a CVPR 2024 competition that attracted 143 teams and 463 submissions. These findings have broader implications: any world model evaluated solely in open-loop mode may appear far more capable than it is in deployment, where each prediction influences future observations through the agent’s actions. 

**Statistical rigor.** Agarwal et al. [394] demonstrated that standard RL evaluation practices— reporting mean or median scores across a small number of games and seeds—produce unreliable conclusions. Mean human-normalized scores are dominated by outlier games, while median scores discard too much information. They proposed performance profiles, stratified bootstrap confidence intervals, and the interquartile mean as robust aggregate metrics, releasing the `rliable` library for standardized statistical analysis. Despite receiving the NeurIPS 2021 Outstanding Paper Award and widespread citation, many world model papers continue to report only mean/median scores without confidence intervals, making published comparisons difficult to interpret and potentially misleading. 

**Toward unified evaluation.** The field would benefit from a unified evaluation protocol that measures a world model’s core capabilities—dynamics prediction accuracy, temporal consistency, physical plausibility, action-conditioned controllability, and downstream task utility—in a domainagnostic manner. Currently, an RL world model measured by HNS on Atari cannot be meaningfully compared with a driving world model measured by FVD on nuScenes or a robotics world model measured by manipulation success rate. Developing such a unified framework, potentially combining diagnostic physics probes [398], perceptual quality decomposition [396], and task-performance normalization [394], represents one of the most impactful methodological contributions the field could pursue. 

### **Data Efficiency and Representation Learning** 

While world models improve data efficiency relative to model-free methods, they still require substantial data—especially in high-dimensional observation spaces. Self-supervised and foundationmodel approaches (JEPA [5], V-JEPA [57]) address this by pretraining on large unlabeled datasets, 

105 

but effectively transferring these representations to downstream tasks with limited fine-tuning data remains challenging. 

### **Safety, Robustness, and Interpretability** 

Deploying world models in safety-critical applications (autonomous driving, medical decision-making, robotics) requires that the model’s predictions be reliable, calibrated, and interpretable. Overconfident predictions can lead to dangerous actions; underconfident predictions can lead to overly conservative behavior. Formal verification of learned world models and methods for quantifying and communicating predictive uncertainty to downstream decision-makers are essential for realworld deployment. 

### **Multimodality and Grounding** 

Real-world environments are inherently multimodal: visual, auditory, tactile, proprioceptive, and linguistic information are all relevant for building accurate world models. Current approaches predominantly focus on visual inputs, with limited integration of other modalities. Grounding world models in physical reality—ensuring that predictions respect physical laws, object permanence, and causal relationships—remains an open challenge. 

## **9 Discussion and Future Directions** 

The preceding sections have traced the evolution of world models from early symbolic frame-based representations to the current generation of billion-parameter neural simulators, highlighting advances in architectures, methodological paradigms, reasoning strategies, and an increasingly diverse range of application domains. In this final section, we step back from the technical details to consider a broader set of questions that, in our view, are likely to shape the future trajectory of the field. Rather than revisiting the specific challenges summarized in Section 8, we focus instead on crosscutting themes, unresolved tensions, and emerging research directions that transcend individual application areas. 

### **Toward a Unified Definition of World Models** 

One of the most striking observations emerging from this survey is that there is still no universally accepted definition of what constitutes a world model. In model-based reinforcement learning, the term retains a relatively precise meaning, typically referring to a learned transition model coupled with a reward predictor that enables planning through imagination. Yet, the same label is now applied to video generation systems that produce photorealistic footage without any explicit notion of action or reward, to language models whose internal representations may or may not encode causal structure, and to domain-specific simulators in areas such as medicine and climate science, where design constraints differ substantially from those of game-playing agents. 

This ambiguity is not merely terminological; it has important practical consequences for how research is organized, how models are evaluated, and how progress is assessed. A video generation model that performs well on FVD, for example, may be described as a “world model” despite lacking action-conditioned prediction, whereas a lightweight RSSM that supports effective planning in a low-dimensional latent space may be regarded as insufficiently general. In our view, the field would benefit from a clearer distinction between _predictive world models_ , which forecast future states conditioned on actions and support downstream decision-making, and _generative world simulators_ , 

106 

which generate realistic sensory data without necessarily enabling interactive control. Both classes of systems are valuable, but conflating them obscures the distinct technical challenges they entail and makes meaningful cross-domain comparison more difficult. 

### **The Convergence of World Models and Foundation Models** 

Perhaps the most consequential trend identified in this survey is the ongoing convergence of world models and foundation models. Systems such as Cosmos [14], Genie [13], and V-JEPA 2 [58] are trained on internet-scale video corpora and are intended to function as general-purpose simulators that can be adapted to downstream tasks through fine-tuning or prompting. This trajectory closely parallels the evolution of language models from task-specific systems to general-purpose reasoning engines, and it raises a comparable set of conceptual and practical questions. 

The potential advantages of this shift are substantial. In principle, a single pretrained world model could provide a shared representational substrate for robotics, autonomous driving, scientific modeling, and medical simulation, thereby reducing the need for domain-specific data collection and extensive task-specific engineering. At the same time, this promise must be interpreted with caution. Foundation world models are trained predominantly on internet video, which is heavily biased toward particular visual domains, such as indoor scenes, driving footage, and gaming content, while underrepresenting the physical interactions and contact dynamics that are especially critical for robotic manipulation. Whether broad visual pretraining can yield representations that transfer effectively to domains governed by fundamentally different physical principles, such as molecular dynamics, fluid simulation, or surgical planning, remains an open empirical question. 

Moreover, the sheer scale of these models raises important concerns about accessibility. When training a competitive world model requires tens of thousands of GPU-hours and access to proprietary datasets, meaningful progress becomes concentrated within a small number of industrial laboratories. The open-source efforts reviewed in this paper, including Open-Sora, Oasis, and related projects, are encouraging developments, but the gap between open and closed systems remains substantial. Ensuring that world model research remains accessible to the broader academic community is therefore not only a matter of equity, but also a scientific imperative, since diversity of approaches, assumptions, and perspectives has historically been central to progress in machine learning. 

### **Grounding, Causality, and the Limits of Prediction** 

A recurring theme across the application domains reviewed in this survey is the tension between perceptual fidelity and physical grounding. Contemporary video-based world models can generate strikingly realistic imagery, yet they often violate basic physical principles: objects may interpenetrate, gravity may behave inconsistently, and conservation laws may be ignored. The evaluation literature reinforces this concern. For example, WorldBench [398] reports that state-of-the-art models achieve only 45 

This limitation is consequential because the most impactful applications of world models, including robotics, autonomous driving, and medical decision-making, require predictions that are not only visually plausible but also physically reliable. A driving world model that occasionally generates phantom obstacles or fails to preserve vehicle momentum is of little value for safetycritical planning, regardless of how strong its FVD performance may be. Bridging this gap will likely require moving beyond purely data-driven approaches toward architectures that incorporate stronger physical inductive biases, whether through equivariant network designs, physics-informed loss functions, or hybrid neuro-symbolic systems that combine learned components with known 

107 

#### governing equations. 

A related and deeper question is whether world models can, or should, learn causal structure. The distinction between correlation and causation is foundational to scientific reasoning, because it determines whether a model can support genuine counterfactual inference, asking not only “what will happen next?” but also “what would have happened if a different action had been taken?” Current world models are typically trained on observational data and optimized for next-step prediction, which, in general, is insufficient for identifying causal relationships [251]. The extent to which causal structure can be recovered from sufficiently rich and diverse training data, and the architectural innovations required to support such reasoning, therefore remains an important open question with implications that extend far beyond any single application domain. 

### **Multimodal Integration and Embodied Intelligence** 

The world models surveyed in this paper operate primarily on visual inputs, occasionally augmented with language descriptions or proprioceptive signals. By contrast, biological organisms construct their internal models of the world from a far richer sensory repertoire, including touch, hearing, proprioception, vestibular feedback, and olfaction. The relative neglect of non-visual modalities in current research is partly a practical consequence of the fact that vision is the modality for which large-scale datasets and pretrained encoders are most readily available. However, it also points to a deeper conceptual limitation in how current world models are formulated. 

For embodied agents acting in the physical world, tactile and proprioceptive feedback is often more informative than vision for contact-rich tasks such as grasping, insertion, and tool use. The limited number of systems that incorporate tactile sensing into world models [88] already illustrates the value of multimodal dynamics modeling. Nevertheless, systematic methods for integrating heterogeneous sensory streams—each characterized by different sampling rates, noise profiles, and information content—into a unified predictive framework remain at an early stage of development. Advancing this line of research will likely require not only architectural innovations, but also new datasets and evaluation benchmarks capable of capturing the richness of multimodal embodied interaction. 

Language occupies a distinctive position within this landscape. As discussed in Section 4, language-augmented world models can ground abstract instructions in physical dynamics while also providing a natural interface for specifying goals, constraints, and task structure. The rapid development of vision-language-action models, such as RT-2, OpenVLA, and _π_ 0, suggests that language may increasingly function as a universal task-specification layer for embodied world models. At the same time, current systems of this kind rely heavily on the implicit world knowledge encoded in pretrained language models, and it remains unclear whether such implicit knowledge can substitute for an explicit learned dynamics model when precise physical reasoning is required. 

### **Safety, Reliability, and Deployment Considerations** 

The deployment of world models in safety-critical domains—such as autonomous driving, surgical planning, and drug dosing—raises concerns that extend well beyond predictive accuracy. In these settings, the consequences of model failure can be severe and irreversible, rendering the standard machine learning workflow of training a model, evaluating it on a held-out test set, and then deploying it insufficient for real-world use. 

Three issues warrant particular attention. First, _calibration_ : the uncertainty estimates produced by a world model must accurately reflect the true likelihood of error. Overconfident predictions may cause an autonomous vehicle to accelerate into a situation the model has mischaracterized, whereas 

108 

underconfident predictions may render a surgical planning system so conservative that it becomes practically unusable. Achieving well-calibrated uncertainty quantification in high-dimensional, autoregressive prediction settings remains largely unsolved, and the interaction between calibration and compounding errors over long rollout horizons is still poorly understood. 

Second, _distributional robustness_ : real-world environments are inherently non-stationary, and any world model trained on one distribution will inevitably encounter situations that differ from those seen during training. The long tail of rare events—such as unusual weather conditions, atypical patient presentations, or novel road geometries—is precisely where accurate prediction is most critical, yet it is also where data-driven models are most vulnerable to failure. Domain randomization, sim-to-real transfer, and continual learning offer partial remedies, but none yet provides the level of formal safety assurance required in high-stakes applications. 

Third, _interpretability_ : when world model predictions inform consequential decisions, practitioners must be able to understand the basis of those predictions. The latent representations learned by current world models are often opaque, and although object-centric and structured representations offer some advantages for interpretability, they have not yet been demonstrated at the scale and complexity required for practical deployment. Developing methods that provide meaningful and trustworthy explanations of world model predictions—without substantially sacrificing predictive performance—therefore remains an important direction for future research. 

### **Expanding the Application Frontier** 

This survey has documented the application of world models to domains that, only a few years ago, would have seemed unlikely candidates, including educational measurement, clinical decisionmaking, cosmological simulation, and financial markets. These emerging applications are important not only because of their practical relevance, but also because of the theoretical questions they bring to the forefront. 

Medical world models, for example, must operate under conditions of extreme data scarcity, strict privacy constraints, and demanding safety requirements. The four-level capability framework proposed by Qazi et al. [253], which ranges from temporal prediction to counterfactual rollouts and ultimately autonomous planning, provides a useful lens for assessing progress. At present, however, most systems remain concentrated at the lower levels of this hierarchy. Reaching Level 4, in which a world model can autonomously recommend treatment strategies, will require advances not only in calibration, interpretability, and reliability, but also in regulatory acceptance and clinical trust, challenges that are not purely technical. 

Educational world models present a different set of difficulties. In this context, the “environment” is a human learner whose internal state—including knowledge, misconceptions, and motivation—is only indirectly observable and whose dynamics are shaped by cognitive, social, and developmental processes that differ fundamentally from those of physical systems. Whether the architectural assumptions that work well in physical environments, such as Markovian state transitions, stationary dynamics, and dense reward signals, can be meaningfully transferred to educational settings remains an open question. 

Financial world models face yet another class of challenges, including reflexivity, non-stationarity, and strategic interaction, all of which depart substantially from the physical settings in which world models were originally developed. The fact that deploying a model can alter the very environment it seeks to model [387] introduces a fundamental complication for standard reinforcement learning formulations. This suggests that world models for strategic environments may require game-theoretic or multi-agent formulations that move beyond the traditional single-agent POMDP framework. 

To summarize, these diverse applications point to a common lesson: the world model paradigm 

109 

is sufficiently flexible to extend across a wide range of domains, but each domain imposes its own constraints that challenge the limits of existing methods. The most productive directions for future research will likely emerge from sustained interaction between these domain-specific demands and the general-purpose architectural innovations being developed across the broader world model community. 

### **The Road Ahead** 

We conclude with several speculative observations regarding the future direction of the field. The integration of latent reasoning with world models—as exemplified by Coconut [17], LCDrive [18], and FutureX [19]—suggests that world models may evolve from passive simulators into active reasoning engines capable of supporting multi-step deliberation in latent space. If this trajectory continues, the distinction between “thinking” and “simulating” may become increasingly blurred, with world models serving as a shared substrate for both perception and cognition. 

The development of hierarchical and compositional world models—systems that decompose complex environments into reusable components and reason across multiple levels of temporal and spatial abstraction—remains an important but still largely unrealized objective. Existing hierarchical approaches [411, 412] have demonstrated promising results in structured environments, but extending these ideas to open-ended real-world settings characterized by heterogeneous objects, uncertain interactions, and long-horizon task structure remains a major challenge. 

Finally, the question of what it would mean for a world model to “understand” the world, rather than merely predict it, remains both philosophically significant and practically consequential. The gap between current systems and the robust, flexible, and causal world understanding exhibited even by relatively simple biological organisms remains substantial. Narrowing this gap will require not only larger models and more data, but also conceptual advances in how intelligence represents, learns, and reasons about the structure of physical and social reality. This survey has sought to map the current state of the field; its most important chapters are still to be explored. 

110 

## **References** 

- [1] Xinqing Li et al. A comprehensive survey on world models for embodied AI. _arXiv preprint arXiv:2510.16732_ , 2025. 

- [2] Philip N. Johnson-Laird. _Mental Models: Towards a Cognitive Science of Language, Inference, and Consciousness_ . Harvard University Press, 1983. 

- [3] Marvin Minsky. A framework for representing knowledge. Technical Report Memo 306, MIT AI Laboratory, 1974. 

- [4] David Ha and Jürgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2018. Also published as: Recurrent World Models Facilitate Policy Evolution, NeurIPS 2018. 

- [5] Yann LeCun. A path towards autonomous machine intelligence. _OpenReview preprint_ , 2022. Version 0.9.2, 2022-06-27. 

- [6] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. _arXiv preprint arXiv:1912.01603_ , 2019. 

- [7] Danijar Hafner, Timothy Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models. In _International Conference on Learning Representations_ , 2021. 

- [8] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _Nature_ , 2025. 

- [9] Julian Schrittwieser, Ioannis Antonoglou, Thomas Hubert, Karen Simonyan, Laurent Sifre, Simon Schmitt, Arthur Guez, Edward Lockhart, Demis Hassabis, Thore Graepel, Timothy Lillicrap, and David Silver. Mastering atari, go, chess and shogi by planning with a learned model. _Nature_ , 588(7839):604–609, 2020. 

- [10] Yixin Liu, Kai Zhang, Yuan Li, Zhiling Yan, Chujie Gao, Ruoxi Chen, Zhengqing Yuan, Yue Huang, Hanchi Sun, Jianfeng Gao, Lifang He, and Lichao Sun. Sora: A review on background, technology, limitations, and opportunities of large vision models. _arXiv preprint arXiv:2402.17177_ , 2024. 

- [11] Jingtao Ding, Yunke Zhang, Yu Shang, Yuheng Zhang, Zefang Zong, Jie Feng, Yuan Yuan, Hongyuan Su, Nian Li, Jinghua Piao, Yucheng Deng, Nicholas Sukiennik, Chen Gao, Fengli Xu, and Yong Li. Understanding world or predicting future? a comprehensive survey of world models. _ACM Computing Surveys_ , 58(3):1–38, 2025. doi: 10.1145/3746449. 

- [12] Mahmoud Assran et al. V-JEPA 2: Self-supervised video models enable understanding, prediction and planning. _arXiv preprint_ , 2025. 

- [13] Jake Bruce, Michael Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steiber, Chris Apps, et al. Genie: Generative interactive environments. _arXiv preprint arXiv:2402.15391_ , 2024. 

- [14] NVIDIA. Cosmos: World foundation model platform for physical AI. _arXiv preprint_ , 2025. 

- [15] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language models. In _Advances in Neural Information Processing Systems_ , volume 35, 2022. 

111 

- [16] Xinghao Chen et al. Reasoning beyond language: A comprehensive survey on latent chainof-thought reasoning. _arXiv preprint arXiv:2505.16782_ , 2025. 

- [17] Shibo Hao et al. Training large language models to reason in a continuous latent space. _arXiv preprint arXiv:2412.06769_ , 2024. 

- [18] Shuhan Tan, Kashyap Chitta, Yuxiao Chen, Ran Tian, Yurong You, Yan Wang, Wenjie Luo, Yulong Cao, Philipp Krähenbühl, Marco Pavone, and Boris Ivanovic. Latent chain-of-thought world modeling for end-to-end driving. _arXiv preprint arXiv:2512.10226_ , 2025. 

- [19] Zhiyu Xiang et al. Futurex: Enhance end-to-end autonomous driving with chain-of-thought reasoning in latent world model. _arXiv preprint arXiv:2512.11226_ , 2025. 

- [20] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and Illia Polosukhin. Attention is all you need, 2023. URL `https://arxiv. org/abs/1706.03762` . 

- [21] Tianyang Lin, Yuxin Wang, Xiangyang Liu, and Xipeng Qiu. A survey of transformers. _AI Open_ , 3:111–132, 2022. 

- [22] OpenAI. GPT-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- [23] Tianyang Zhong, Zhengliang Liu, Yi Pan, Yutong Zhang, Zeyu Zhang, Yifan Zhou, Shizhe Liang, Zihao Wu, Yanjun Lyu, Peng Shu, et al. Evaluation of OpenAI o1: Opportunities and challenges of AGI. _arXiv preprint arXiv:2409.18486_ , 2025. 

- [24] Hans Moravec. _Mind Children: The Future of Robot and Human Intelligence_ . Harvard University Press, 1988. 

- [25] Yann LeCun. Advanced machine intelligence (AMI): Building AI systems that understand the physical world, 2025. Announced November 2025. `https://www. advancedmachineintelligence.com` . 

- [26] Richard S. Sutton and Andrew G. Barto. _Reinforcement Learning: An Introduction_ . MIT Press, 2nd edition, 2018. 

- [27] Yanchen Guan, Haicheng Cui, et al. World models for autonomous driving: An initial survey. _arXiv preprint arXiv:2403.02622_ , 2024. 

- [28] Xuan Li et al. A step toward world models: A survey on robotic manipulation. _arXiv preprint arXiv:2511.02097_ , 2025. 

- [29] Steven C. H. Chen et al. 3d and 4d world modeling: A survey. `https://worldbench.github. io/survey` , 2025. 

- [30] Jürgen Schmidhuber. Curious model-building control systems. In _Proc. International Joint Conference on Neural Networks (IJCNN)_ , volume 2, pages 1458–1463. IEEE, 1991. doi: 10.1109/IJCNN.1991.170605. 

- [31] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels. In _Proceedings of the 36th International Conference on Machine Learning_ , pages 2555–2565. PMLR, 2019. 

112 

- [32] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. In _International Conference on Learning Representations_ , 2020. 

- [33] David Ha and Jürgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2018. 

- [34] Danijar Hafner, Timothy Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models. In _International Conference on Learning Representations (ICLR)_ , 2021. 

- [35] Vincent Micheli, Eloi Alonso, and François Fleuret. Transformers are sample-efficient world learners. In _The Eleventh International Conference on Learning Representations (ICLR)_ , 2023. 

- [36] Weipu Zhang et al. STORM: Efficient stochastic transformer based world models for reinforcement learning. In _Advances in Neural Information Processing Systems_ , 2023. 

- [37] Eloi Alonso, Adam Jelley, Vincent Micheli, Anssi Kanervisto, Amos Storber, Oriol Vinyals, and François Fleuret. Diffusion for world modeling: Visual details matter in Atari. In _Advances in Neural Information Processing Systems_ , 2024. NeurIPS 2024 Spotlight. 

- [38] Julian Schrittwieser, Ioannis Antonoglou, Thomas Hubert, Karen Simonyan, Laurent Sifre, Simon Schmitt, Arthur Guez, Edward Lockhart, Demis Hassabis, Thore Graepel, Timothy Lillicrap, and David Silver. Mastering Atari, Go, chess and shogi by planning with a learned model. _Nature_ , 588(7839):604–609, 2020. 

- [39] Mahmoud Assran, Quentin Duval, Ishan Misra, Piotr Bojanowski, Pascal Vincent, Michael Rabbat, Yann LeCun, and Nicolas Ballas. Self-supervised learning from images with a jointembedding predictive architecture. _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 15619–15629, 2023. 

- [40] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _Nature_ , 2025. arXiv preprint arXiv:2301.04104, 2023. 

- [41] Thomas M. Moerland, Joost Broekens, Aske Plaat, and Catholijn M. Jonker. Model-based reinforcement learning: A survey. _Foundations and Trends in Machine Learning_ , 16(1):1–118, 2023. 

- [42] Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Andrei A. Rusu, Joel Veness, Marc G. Bellemare, Alex Graves, Martin Riedmiller, Andreas K. Fidjeland, Georg Ostrovski, Stig Petersen, Charles Beattie, Amir Sadik, Ioannis Antonoglou, Helen King, Dharshan Kumaran, Daan Wierstra, Shane Legg, and Demis Hassabis. Human-level control through deep reinforcement learning. _Nature_ , 518(7540):529–533, 2015. 

- [43] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [44] Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. Soft actor-critic: Offpolicy maximum entropy deep reinforcement learning with a stochastic actor. In _Proceedings of the 35th International Conference on Machine Learning (ICML)_ , pages 1861–1870, 2018. 

113 

- [45] Kurtland Chua, Roberto Calandra, Rowan McAllister, and Sergey Levine. Deep reinforcement learning in a handful of trials using probabilistic dynamics models. _Advances in Neural Information Processing Systems_ , 31, 2018. 

- [46] Nicklas Hansen, Xiaolong Wang, and Hao Su. Temporal difference learning for model predictive control. In _International Conference on Machine Learning_ , pages 8487–8506. PMLR, 2022. 

- [47] Marc Peter Deisenroth and Carl Edward Rasmussen. Pilco: A model-based and data-efficient approach to policy search. In _Proceedings of the 28th International Conference on Machine Learning (ICML)_ , pages 465–472, 2011. 

- [48] Michael Janner, Justin Fu, Marvin Zhang, and Sergey Levine. When to trust your model: Model-based policy optimization. In _Advances in Neural Information Processing Systems_ , volume 32, 2019. 

- [49] Irina Higgins, Arka Pal, Andrei A. Rusu, Loic Matthey, Christopher P. Burgess, Alexander Pritzel, Matthew Botvinick, Charles Blundell, and Alexander Lerchner. Darla: Improving zero-shot transfer in reinforcement learning. In _Proceedings of the 34th International Conference on Machine Learning (ICML)_ , pages 1480–1490, 2017. 

- [50] Ken Kansky, Tom Silver, David A. Mély, Mohamed Eldawy, Miguel Lázaro-Gredilla, Xinghua Lou, Nimrod Dorfman, Szymon Sidor, Scott Phoenix, and Dileep George. Schema networks: Zero-shot transfer with a generative causal model of intuitive physics. _arXiv preprint arXiv:1706.04317_ , 2017. 

- [51] Lars Buesing, Theophane Weber, Yori Zwols, Nicolas Heess, Sébastien Racanière, Arthur Guez, and Jean-Baptiste Lespiau. Woulda, coulda, shoulda: Counterfactually-guided policy search. In _International Conference on Learning Representations (ICLR)_ , 2019. 

- [52] Yarin Gal and Zoubin Ghahramani. Dropout as a bayesian approximation: Representing model uncertainty in deep learning. In _Proceedings of the 33rd International Conference on Machine Learning (ICML)_ , pages 1050–1059, 2016. 

- [53] Ian Osband, Charles Blundell, Alexander Pritzel, and Benjamin Van Roy. Deep exploration via bootstrapped dqn. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 29, 2016. 

- [54] Marc G. Bellemare, Will Dabney, and Rémi Munos. A distributional perspective on reinforcement learning. In _Proceedings of the 34th International Conference on Machine Learning (ICML)_ , pages 449–458, 2017. 

- [55] Max Schwarzer, Ankesh Anand, Rishab Goel, R. Devon Hjelm, Aaron Courville, and Philip Bachman. Data-efficient reinforcement learning with self-predictive representations. In _International Conference on Learning Representations (ICLR)_ , 2021. 

- [56] Diederik P. Kingma and Max Welling. Auto-encoding variational Bayes. _International Conference on Learning Representations_ , 2014. 

- [57] Adrien Bardes, Quentin Garrido, Jean Ponce, Xinlei Chen, Michael Rabbat, Yann LeCun, Mahmoud Assran, and Nicolas Ballas. Revisiting feature prediction for learning visual representations from video. _arXiv preprint arXiv:2404.08471_ , 2024. 

114 

- [58] Meta AI. V-JEPA 2: Self-supervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. 

- [59] Mohammad Babaeizadeh, Chelsea Finn, Dumitru Erhan, Roy H. Campbell, and Sergey Levine. Stochastic variational video prediction. _International Conference on Learning Representations_ , 2018. 

- [60] Emily Denton and Rob Fergus. Stochastic video generation with a learned prior. _International Conference on Machine Learning_ , pages 1174–1183, 2018. 

- [61] Dani Valevski, Yaniv Leviathan, Moab Arar, and Shlomi Fruchter. Diffusion models are realtime game engines. In _The Thirteenth International Conference on Learning Representations (ICLR)_ , 2025. arXiv:2408.14837. 

- [62] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Sherwin, and Pedro Corrado. GAIA-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 

- [63] Thomas Kipf, Elise van der Pol, and Max Welling. Contrastive learning of structured world models. In _International Conference on Learning Representations_ , 2020. URL `https:// openreview.net/forum?id=H1gax6VtDB` . 

- [64] Siyuan Zhou, Yilun Du, Jiaben Chen, Yandong Li, Dit-Yan Yeung, and Chuang Gan. Robodreamer: learning compositional world models for robot imagination. In _Proceedings of the 41st International Conference on Machine Learning_ , pages 61885–61896, 2024. 

- [65] Leonardo Barcellona et al. Dream to manipulate: Compositional world models empowering robot imitation learning with imagination. In _International Conference on Learning Representations_ , 2025. 

- [66] Wenzhao Wang et al. OccWorld: Learning a 3D occupancy world model for autonomous driving. _arXiv preprint arXiv:2311.16038_ , 2024. 

- [67] Yunpeng Zhang et al. Copilot4D: Learning unsupervised world models for autonomous driving via discrete diffusion. In _The Twelfth International Conference on Learning Representations (ICLR)_ , 2024. 

- [68] Lingdong Kong et al. 3D and 4D world modeling: A survey. _arXiv preprint arXiv:2509.07996_ , 2025. 

- [69] Jindi Kong, Yuting He, Cong Xia, Rongjun Ge, and Shuo Li. Mri contrast enhancement kinetics world model. _arXiv preprint arXiv:2602.19285_ , 2026. 

- [70] Anonymous. Leworldmodel: Stable end-to-end joint-embedding predictive architecture from pixels. _arXiv preprint_ , 2024. 

- [71] Anonymous. Brain-jepa: Brain dynamics foundation model with gradient positioning and spatiotemporal masking. _arXiv preprint_ , 2024. 

- [72] Anonymous. Clarity: Medical world model for guiding treatment decisions by modeling context-aware disease trajectories in latent space. _arXiv preprint_ , 2025. 

- [73] Anonymous. Medical world model. _arXiv preprint_ , 2024. 

115 

- [74] Vincent Micheli, Eloi Alonso, and François Fleuret. Transformers are sample-efficient world models. In _International Conference on Learning Representations (ICLR)_ , 2023. 

- [75] Eloi Alonso, Adam Jelley, Vincent Micheli, Anssi Kanervisto, Amos Storkey, Tim Pearce, and François Fleuret. Diffusion for world modeling: Visual details matter in atari. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 37, 2024. 

- [76] Dani Valevski, Yaniv Leviathan, Moab Arar, and Shlomi Fruchter. Diffusion models are real-time game engines. _arXiv preprint arXiv:2408.14837_ , 2024. Published at ICLR 2025. 

- [77] Shibo Hao, Yi Gu, Haodi Ma, Joshua Hong, Zhen Wang, Daisy Wang, and Zhiting Hu. Reasoning with language model is planning with world model. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP)_ , pages 8154– 8173, Singapore, 2023. Association for Computational Linguistics. 

- [78] Yu Gu, Boyuan Deng, Chen Zhu, Yi Dong, Mingyue Li, Jianwei Xie, Shuyan Lu, Tianbao Shi, Yu Su, and Wen-tau Yih. Is your LLM secretly a world model of the internet? model-based planning for web agents. _arXiv preprint arXiv:2411.06559_ , 2024. 

- [79] Raz Levy, Ronen I. Brafman, and Moshe Tennenholtz. WorldLLM: Learning world models via large language models. _arXiv preprint arXiv:2506.05270_ , 2025. 

- [80] Vlas Zyrianov, Xiyue Zhu, and Shenlong Wang. Learning to generate realistic LiDAR point clouds. _arXiv preprint arXiv:2209.03954_ , 2022. ECCV 2022. 

- [81] Vlas Zyrianov, Boris Ivanovic, Vince Zhao, and Marco Pavone. LidarDM: Generative LiDAR simulation in a generated world. _arXiv preprint arXiv:2404.02903_ , 2024. 

- [82] Wenzhao Zheng, Weiliang Chen, Yuanhui Huang, Borui Zhang, Yueqi Duan, and Jiwen Lu. OccWorld: Learning a 3D occupancy world model for autonomous driving. In _European Conference on Computer Vision (ECCV)_ , 2024. arXiv preprint arXiv:2311.16038, 2023. 

- [83] Philipp Wu, Alejandro Escontrela, Danijar Hafner, Pieter Abbeel, and Ken Goldberg. Daydreamer: World models for physical robot learning. In _Conference on robot learning_ , pages 2226–2240. PMLR, 2023. 

- [84] MLA Team. MLA: A multisensory language-action model for multimodal understanding and forecasting in robotic manipulation. _arXiv preprint arXiv:2509.26642_ , 2025. 

- [85] Tactile-VLA Team. Tactile-VLA: Unlocking vision-language-action model’s physical knowledge for tactile generalization. _arXiv preprint_ , 2025. 

- [86] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. GAIA-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 

- [87] Kashyap Chitta, Daniel Dauner, Harshit S. Behl, Liliang Peng, Walter Zimmer, Mike Koehler, Adrien Gaidon, Andreas Geiger, Dragomir Anguelov, and Wayve Team. GAIA2: A controllable multi-view generative world model for autonomous driving. _arXiv preprint arXiv:2503.20523_ , 2025. 

- [88] Mengjiao Yang, Yilun Du, Kamyar Ghasemipour, Jonathan Tompson, Dale Schuurmans, and Pieter Abbeel. Learning interactive real-world simulators. In _The Twelfth International Conference on Learning Representations (ICLR)_ , 2024. Outstanding Paper Award. 

116 

- [89] Delong Chen, Theo Moutakanni, Willy Chung, Yejin Bang, Ziwei Ji, Allen Bolourchi, and Pascale Fung. Planning with reasoning using vision language world model. _arXiv preprint arXiv:2509.02722_ , 2025. 

- [90] Kazuto Nakashima and Ryo Kurazume. LiDAR data synthesis with denoising diffusion probabilistic models. _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , pages 14724–14731, 2024. 

- [91] Qianjiang Hu, Zhimin Zhang, and Wei Hu. RangeLDM: Fast realistic LiDAR point cloud generation. _arXiv preprint arXiv:2403.10094_ , 2024. 

- [92] BiTLA Team. BiTLA: A bimanual tactile-language-action model for contact-rich robotic manipulation. _arXiv preprint_ , 2025. 

- [93] Xinji Mai, Zeng Zeng, Yizhao Wei, Jiahong Pei, Guowen Liu, Jieming Dong, Haiwen Fan, Yingchen Li, Ruihua Zhou, and Shuai Xie. From efficient multimodal models to world models: A survey. _arXiv preprint arXiv:2407.00118_ , 2024. 

- [94] Benjamin Devillers, Lucas Maytié, and Rufin VanRullen. Multimodal dreaming: A global workspace approach to world model-based reinforcement learning. _arXiv preprint arXiv:2502.21142_ , 2025. 

- [95] Max Schwarzer, Ankesh Anand, Rishab Goel, R Devon Hjelm, Aaron Courville, and Philip Bachman. Data-efficient reinforcement learning with self-predictive representations. In _International Conference on Learning Representations_ , 2021. 

- [96] Jean-Bastien Grill, Florian Strub, Florent Altché, Corentin Tallec, Pierre Richemond, Elena Buchatskaya, Carl Doersch, Bernardo Avila Pires, Zhaohan Guo, Mohammad Gheshlaghi Azar, et al. Bootstrap your own latent-a new approach to self-supervised learning. _Advances in neural information processing systems_ , 2020. 

- [97] Adrien Bardes, Jean Ponce, and Yann LeCun. Vicreg: Variance-invariance-covariance regularization for self-supervised learning. _arXiv preprint arXiv:2105.04906_ , 2021. 

- [98] Gaoyue Zhou, Hengkai Pan, Yann Lecun, and Lerrel Pinto. DINO-WM: World models on pre-trained visual features enable zero-shot planning. In Aarti Singh, Maryam Fazel, Daniel Hsu, Simon Lacoste-Julien, Felix Berkenkamp, Tegan Maharaj, Kiri Wagstaff, and Jerry Zhu, editors, _Proceedings of the 42nd International Conference on Machine Learning_ , volume 267 of _Proceedings of Machine Learning Research_ , pages 79115–79135. PMLR, 13–19 Jul 2025. URL `https://proceedings.mlr.press/v267/zhou25t.html` . 

- [99] Richard S Sutton. Integrated architectures for learning, planning, and reacting based on approximating dynamic programming. In _Proceedings of the seventh international conference on machine learning_ , pages 216–224, 1990. 

- [100] Jacob Buckman, Danijar Hafner, George Tucker, Eugene Brevdo, and Honglak Lee. Sampleefficient reinforcement learning with stochastic ensemble value expansion. _Advances in neural information processing systems_ , 31, 2018. 

- [101] Christopher Grimm, André Barreto, Satinder Singh, and David Silver. The value equivalence principle for model-based reinforcement learning. In _Advances in Neural Information Processing Systems_ , volume 33, pages 5541–5552, 2020. 

117 

- [102] Weirui Ye, Shaohuai Liu, Thanard Kurutach, Pieter Abbeel, and Yang Gao. Mastering atari games with limited data. In _Advances in Neural Information Processing Systems_ , volume 34, pages 25476–25488, 2021. 

- [103] Tianhe Yu, Garrett Thomas, Lantao Yu, Stefano Ermon, James Y Zou, Sergey Levine, Chelsea Finn, and Tengyu Ma. Mopo: Model-based offline policy optimization. _Advances in neural information processing systems_ , 33:14129–14142, 2020. 

- [104] Zihan Ding, Amy Zhang, Yuandong Tian, and Qinqing Zheng. Diffusion world model: Future modeling beyond step-by-step rollout for offline reinforcement learning, 2024. URL `https: //arxiv.org/abs/2402.03570` . 

- [105] Jialong Wu, Shaofeng Yin, Ningya Feng, and Mingsheng Long. Rlvr-world: Training world models with reinforcement learning. _arXiv preprint arXiv:2505.13934_ , 2025. 

- [106] Nathan Lambert, Brandon Amos, Omry Yadan, and Roberto Calandra. Objective mismatch in model-based reinforcement learning. In _Learning for Dynamics and Control_ , pages 761–770. PMLR, 2020. 

- [107] Bingyi Kang, Yang Yue, Rui Lu, Zhijie Lin, Yang Zhao, Kaixin Wang, Gao Huang, and Jiashi Feng. How far is video generation from world model: A physical law perspective. In _Proceedings of the 42nd International Conference on Machine Learning (ICML)_ , 2025. 

- [108] NVIDIA, Arslan Ali, et al. World simulation with video foundation models for physical AI. _arXiv preprint arXiv:2511.00062_ , 2025. 

- [109] Jack Parker-Holder et al. Genie 2: A large-scale foundation world model. _Google DeepMind Technical Report_ , 2024. 

- [110] Google DeepMind. Genie 3 — google deepmind, 2025. URL `https://deepmind.google/ models/genie/` . 

- [111] Hao Liu, Wilson Yan, Matei Zaharia, and Pieter Abbeel. World model on million-length video and language with blockwise ringattention, 2025. URL `https://arxiv.org/abs/2402. 08268` . 

- [112] Yi Zhao, Aidan Scannell, Yuxin Hou, Tianyu Cui, Le Chen, Dieter Büchler, Arno Solin, Juho Kannala, and Joni Pajarinen. Generalist world model pre-training for efficient reinforcement learning. In _ICLR 2025 Workshop on World Models: Understanding, Modelling and Scaling_ , 2025. 

- [113] Rafael Rafailov, Kyle Beltran Hatch, Victor Kolev, John D Martin, Mariano Phielipp, and Chelsea Finn. Moto: Offline pre-training to online fine-tuning for model-based robot learning. In _Conference on Robot Learning_ , pages 3654–3671. PMLR, 2023. 

- [114] Minting Pan, Yitao Zheng, Yunbo Wang, and Xiaokang Yang. Model-based reinforcement learning with multi-task offline pretraining. In _Joint European Conference on Machine Learning and Knowledge Discovery in Databases_ , 2024. 

- [115] Jacob Levy, Tyler Westenbroek, Kevin Huang, Fernando Palafox, Patrick Yin, Shayegan Omidshafiei, Dong-Ki Kim, Abhishek Gupta, and David Fridovich-Keil. Simulation distillation: Pretraining world models in simulation for rapid real-world adaptation. _arXiv preprint arXiv:2603.15759_ , 2026. 

118 

- [116] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, Albert Tung, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, Anant Rai, Anchit Gupta, Andrew Wang, Anikait Singh, Animesh Garg, Aniruddha Kembhavi, Annie Xie, Anthony Brohan, Antonin Raffin, Archit Sharma, Arefeh Yavary, Arhan Jain, Ashwin Balakrishna, Ayzaan Wahid, Ben Burgess-Limerick, Beomjoon Kim, Bernhard Schölkopf, Blake Wulfe, Brian Ichter, Cewu Lu, Charles Xu, Charlotte Le, Chelsea Finn, Chen Wang, Chenfeng Xu, Cheng Chi, Chenguang Huang, Christine Chan, Christopher Agia, Chuer Pan, Chuyuan Fu, Coline Devin, Danfei Xu, Daniel Morton, Danny Driess, Daphne Chen, Deepak Pathak, Dhruv Shah, Dieter Büchler, Dinesh Jayaraman, Dmitry Kalashnikov, Dorsa Sadigh, Edward Johns, Ethan Foster, Fangchen Liu, Federico Ceola, Fei Xia, Feiyu Zhao, Freek Stulp, Gaoyue Zhou, Gaurav S. Sukhatme, Gautam Salhotra, Ge Yan, Gilbert Feng, Giulio Schiavi, Glen Berseth, Gregory Kahn, Guanzhi Wang, Hao Su, Hao-Shu Fang, Haochen Shi, Henghui Bao, Heni Ben Amor, Henrik I Christensen, Hiroki Furuta, Homer Walke, Hongjie Fang, Huy Ha, Igor Mordatch, Ilija Radosavovic, Isabel Leal, Jacky Liang, Jad Abou-Chakra, Jaehyung Kim, Jaimyn Drake, Jan Peters, Jan Schneider, Jasmine Hsu, Jeannette Bohg, Jeffrey Bingham, Jeffrey Wu, Jensen Gao, Jiaheng Hu, Jiajun Wu, Jialin Wu, Jiankai Sun, Jianlan Luo, Jiayuan Gu, Jie Tan, Jihoon Oh, Jimmy Wu, Jingpei Lu, Jingyun Yang, Jitendra Malik, João Silvério, Joey Hejna, Jonathan Booher, Jonathan Tompson, Jonathan Yang, Jordi Salvador, Joseph J. Lim, Junhyek Han, Kaiyuan Wang, Kanishka Rao, Karl Pertsch, Karol Hausman, Keegan Go, Keerthana Gopalakrishnan, Ken Goldberg, Kendra Byrne, Kenneth Oslund, Kento Kawaharazuka, Kevin Black, Kevin Lin, Kevin Zhang, Kiana Ehsani, Kiran Lekkala, Kirsty Ellis, Krishan Rana, Krishnan Srinivasan, Kuan Fang, Kunal Pratap Singh, Kuo-Hao Zeng, Kyle Hatch, Kyle Hsu, Laurent Itti, Lawrence Yunliang Chen, Lerrel Pinto, Li Fei-Fei, Liam Tan, Linxi Jim Fan, Lionel Ott, Lisa Lee, Luca Weihs, Magnum Chen, Marion Lepert, Marius Memmel, Masayoshi Tomizuka, Masha Itkina, Mateo Guaman Castro, Max Spero, Maximilian Du, Michael Ahn, Michael C. Yip, Mingtong Zhang, Mingyu Ding, Minho Heo, Mohan Kumar Srirama, Mohit Sharma, Moo Jin Kim, Naoaki Kanazawa, Nicklas Hansen, Nicolas Heess, Nikhil J Joshi, Niko Suenderhauf, Ning Liu, Norman Di Palo, Nur Muhammad Mahi Shafiullah, Oier Mees, Oliver Kroemer, Osbert Bastani, Pannag R Sanketi, Patrick Tree Miller, Patrick Yin, Paul Wohlhart, Peng Xu, Peter David Fagan, Peter Mitrano, Pierre Sermanet, Pieter Abbeel, Priya Sundaresan, Qiuyu Chen, Quan Vuong, Rafael Rafailov, Ran Tian, Ria Doshi, Roberto Martín-Martín, Rohan Baijal, Rosario Scalise, Rose Hendrix, Roy Lin, Runjia Qian, Ruohan Zhang, Russell Mendonca, Rutav Shah, Ryan Hoque, Ryan Julian, Samuel Bustamante, Sean Kirmani, Sergey Levine, Shan Lin, Sherry Moore, Shikhar Bahl, Shivin Dass, Shubham Sonawani, Shuran Song, Sichun Xu, Siddhant Haldar, Siddharth Karamcheti, Simeon Adebola, Simon Guist, Soroush Nasiriany, Stefan Schaal, Stefan Welker, Stephen Tian, Subramanian Ramamoorthy, Sudeep Dasari, Suneel Belkhale, Sungjae Park, Suraj Nair, Suvir Mirchandani, Takayuki Osa, Tanmay Gupta, Tatsuya Harada, Tatsuya Matsushima, Ted Xiao, Thomas Kollar, Tianhe Yu, Tianli Ding, Todor Davchev, Tony Z. Zhao, Travis Armstrong, Trevor Darrell, Trinity Chung, Vidhi Jain, Vincent Vanhoucke, Wei Zhan, Wenxuan Zhou, Wolfram Burgard, Xi Chen, Xiaolong Wang, Xinghao Zhu, Xinyang Geng, Xiyuan Liu, Xu Liangwei, Xuanlin Li, Yao Lu, Yecheng Jason Ma, Yejin Kim, Yevgen Chebotar, Yifan Zhou, Yifeng Zhu, Yilin Wu, Ying Xu, Yixuan Wang, Yonatan Bisk, Yoonyoung Cho, Youngwoon Lee, Yuchen Cui, Yue Cao, Yueh-Hua Wu, Yujin Tang, Yuke Zhu, Yunchu Zhang, Yunfan Jiang, Yunshuang Li, Yunzhu Li, Yusuke Iwasawa, Yutaka Matsuo, Zehan Ma, Zhuo Xu, Zichen Jeff Cui, Zichen Zhang, and Zipeng Lin. Open x-embodiment: Robotic learning datasets and rt-x models : Open x-embodiment 

119 

collaboration0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903, 2024. doi: 10.1109/ICRA57147.2024.10611477. 

- [117] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- [118] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, Quan Vuong, Vincent Vanhoucke, Huong Tran, Radu Soricut, Anikait Singh, Jaspiar Singh, Pierre Sermanet, Pannag R. Sanketi, Grecia Salazar, Michael S. Ryoo, Krista Reymann, Kanishka Rao, Karl Pertsch, Igor Mordatch, Henryk Michalewski, Yao Lu, Sergey Levine, Lisa Lee, Tsang-Wei Edward Lee, Isabel Leal, Yuheng Kuang, Dmitry Kalashnikov, Ryan Julian, Nikhil J. Joshi, Alex Irpan, Brian Ichter, Jasmine Hsu, Alexander Herzog, Karol Hausman, Keerthana Gopalakrishnan, Chuyuan Fu, Pete Florence, Chelsea Finn, Kumar Avinava Dubey, Danny Driess, Tianli Ding, Krzysztof Marcin Choromanski, Xi Chen, Yevgen Chebotar, Justice Carbajal, Noah Brown, Anthony Brohan, Montserrat Gonzalez Arenas, and Kehang Han. Rt-2: Vision-languageaction models transfer web knowledge to robotic control. In Jie Tan, Marc Toussaint, and Kourosh Darvish, editors, _Proceedings of The 7th Conference on Robot Learning_ , volume 229 of _Proceedings of Machine Learning Research_ , pages 2165–2183. PMLR, 06–09 Nov 2023. URL `https://proceedings.mlr.press/v229/zitkovich23a.html` . 

- [119] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P Foster, Pannag R Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. In Pulkit Agrawal, Oliver Kroemer, and Wolfram Burgard, editors, _Proceedings of The 8th Conference on Robot Learning_ , volume 270 of _Proceedings of Machine Learning Research_ , pages 2679–2713. PMLR, 06–09 Nov 2025. URL `https://proceedings.mlr.press/v270/kim25c.html` . 

- [120] Jessy Lin, Yuqing Du, Olivia Watkins, Danijar Hafner, Pieter Abbeel, Dan Klein, and Anca Dragan. Learning to model the world with language. In Ruslan Salakhutdinov, Zico Kolter, Katherine Heller, Adrian Weller, Nuria Oliver, Jonathan Scarlett, and Felix Berkenkamp, editors, _Proceedings of the 41st International Conference on Machine Learning_ , volume 235 of _Proceedings of Machine Learning Research_ , pages 29992–30017. PMLR, 21–27 Jul 2024. URL `https://proceedings.mlr.press/v235/lin24g.html` . 

- [121] Adithya Ramesh and Balaraman Ravindran. Physics-informed model-based reinforcement learning. In Nikolai Matni, Manfred Morari, and George J. Pappas, editors, _Proceedings of The 5th Annual Learning for Dynamics and Control Conference_ , volume 211 of _Proceedings of Machine Learning Research_ , pages 26–37. PMLR, 15–16 Jun 2023. URL `https://proceedings.mlr.press/v211/ramesh23a.html` . 

- [122] Kristof T Schütt, Pieter-Jan Kindermans, Huziel Enoc Sauceda, Stefan Chmiela, Alexandre Tkatchenko, and Klaus-Robert Müller. SchNet: A continuous-filter convolutional neural network for modeling quantum interactions. In _Advances in Neural Information Processing Systems_ , volume 30, pages 992–1002, 2017. 

- [123] Simon Batzner, Albert Musaelian, Lixin Sun, Mario Geiger, Jonathan P Mailoa, Mordechai Kornbluth, Nicola Molinari, Tess E Smidt, and Boris Kozinsky. E(3)-equivariant graph neural 

120 

networks for data-efficient and accurate interatomic potentials. _Nature Communications_ , 13: 2453, 2022. 

- [124] Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin Burchfiel, Paarth Shah, and Abhishek Gupta. Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. In _Robotics: Science and Systems (RSS)_ , 2025. arXiv:2504.02792. 

- [125] Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Yao Feng, Chendong Xiang, Yinze Rong, et al. Motus: A unified latent action world model. _arXiv preprint arXiv:2512.13030_ , 2025. 

- [126] Ruoyao Wang, Graham Todd, Ziang Xiao, Xingdi Yuan, Marc-Alexandre Côté, Peter Clark, and Peter Jansen. Can language models serve as text-based world simulators? In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)_ , pages 1–17, 2024. 

- [127] Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control. _arXiv preprint arXiv:2310.16828_ , 2023. 

- [128] Lloyd Russell, Anthony Hu, Lorenzo Bertoni, George Fedoseev, Jamie Shotton, Elahe Arani, and Gianluca Corrado. Gaia-2: A controllable multi-view generative world model for autonomous driving. _arXiv preprint arXiv:2503.20523_ , 2025. 

- [129] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Jiagang Zhu, and Jiwen Lu. DriveDreamer: Towards real-world-driven world models for autonomous driving. In _European Conference on Computer Vision (ECCV)_ , 2024. 

- [130] Guosheng Zhao, Xiaofeng Wang, Zheng Zhu, Xinze Chen, Guan Huang, Xiaoyi Bao, and Xingang Wang. DriveDreamer-2: LLM-enhanced world models for diverse driving video generation. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , 2025. 

- [131] Jiachen Lu, Ze Huang, Zeyu Yang, Jiahui Zhang, and Li Zhang. Wovogen: World volumeaware diffusion for controllable multi-camera driving scene generation. In _European conference on computer vision_ , pages 329–345. Springer, 2024. 

- [132] Wenzhao Zheng, Weiliang Chen, Yuanhui Huang, Borui Zhang, Yueqi Duan, and Jiwen Lu. OccWorld: Learning a 3D occupancy world model for autonomous driving. In _European Conference on Computer Vision (ECCV)_ , 2024. 

- [133] Shenyuan Gao et al. Vista: A generalizable driving world model with high fidelity and versatile controllability. In _Advances in Neural Information Processing Systems_ , volume 37, 2024. 

- [134] Tianxingjian Ding et al. CLARITY: Medical world model for guiding treatment decisions by modeling context-aware disease trajectories in latent space. _arXiv preprint arXiv:2512.08029_ , 2025. 

- [135] Zuoyu Yang et al. Medical world model: Generative simulation of tumor evolution for treatment planning. _arXiv preprint arXiv:2506.02327_ , 2025. 

- [136] Zijian Dong, Ruilin Li, Yilei Wu, Thuan T Nguyen, Joanna S Chong, Fang Ji, Nathanael R Tong, Christopher L Chen, and Juan H Zhou. Brain-jepa: Brain dynamics foundation model 

121 

with gradient positioning and spatiotemporal masking. _Advances in Neural Information Processing Systems_ , 37:86048–86073, 2024. 

- [137] Mohammad Areeb Qazi, Maryam Nadeem, and Mohammad Yaqub. Beyond generative ai: World models for clinical prediction, counterfactuals, and planning. _arXiv preprint arXiv:2511.16333_ , 2025. 

- [138] Tim Brooks, Bill Peebles, Connor Holmes, Will DePue, Yufei Guo, Leo Jing, David Schnurr, Joe Taylor, Troy Luhman, Eric Luhman, et al. Video generation models as world simulators. _OpenAI Blog_ , 1(8):1, 2024. 

- [139] Shibo Hao, Yi Gu, Haodi Ma, Joshua Hong, Zhen Wang, Daisy Wang, and Zhiting Hu. Reasoning with language model is planning with world model. In Houda Bouamor, Juan Pino, and Kalika Bali, editors, _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ , pages 8154–8173, Singapore, December 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.emnlp-main.507. URL `https://aclanthology.org/2023.emnlp-main.507/` . 

- [140] Albert Gu, Karan Goel, and Christopher Ré. Efficiently modeling long sequences with structured state spaces. In _International Conference on Learning Representations_ , 2022. 

- [141] Albert Gu and Tri Dao. Mamba: Linear-time sequence modeling with selective state spaces. _arXiv preprint arXiv:2312.00752_ , 2023. 

- [142] Ryan Po, Yoni Nitzan, Zhengfei Zhang, Desai Chen, Tri Dao, Eli Shechtman, Gordon Wetzstein, and Xin Huang. Long-context state-space video world models. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 8733–8744, 2025. arXiv:2505.20171. 

- [143] Sepp Hochreiter and Jürgen Schmidhuber. Long short-term memory. _Neural Computation_ , 9(8):1735–1780, 1997. 

- [144] Kyunghyun Cho, Bart van Merriënboer, Caglar Gulcehre, Dzmitry Bahdanau, Fethi Bougares, Holger Schwenk, and Yoshua Bengio. Learning phrase representations using RNN encoder-decoder for statistical machine translation. _Proceedings of the Conference on Empirical Methods in Natural Language Processing_ , pages 1724–1734, 2014. 

- [145] Seung Wook Kim, Yuhao Zhou, Jonah Philion, Antonio Torralba, and Sanja Fidler. Learning to simulate dynamic environments with GameGAN. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 1231–1240, 2020. 

- [146] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. _Advances in Neural Information Processing Systems_ , 30, 2017. 

- [147] Lili Chen, Kevin Lu, Aravind Rajeswaran, Kimin Lee, Aditya Grover, Michael Laskin, Pieter Abbeel, Aravind Srinivas, and Igor Mordatch. Decision transformer: Reinforcement learning via sequence modeling. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 34, pages 15084–15097, 2021. 

- [148] Michael Janner, Qiyang Li, and Sergey Levine. Offline reinforcement learning as one big sequence modeling problem. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 34, pages 1273–1286, 2021. 

122 

- [149] Wilson Yan, Yunzhi Zhang, Pieter Abbeel, and Aravind Srinivas. VideoGPT: Video generation using VQ-VAE and transformers. _arXiv preprint arXiv:2104.10157_ , 2021. 

- [150] Scott Reed, Konrad Żołna, Emilio Parisotto, Sergio Gómez Colmenarejo, Alexander Novikov, Gabriel Barth-Maron, Mai Giménez, Yury Sulsky, Jackie Kay, Jost Tobias Springenberg, Tom Eccles, Jake Bruce, Ali Razavi, Ashley Edwards, Nicolas Heess, Yutian Chen, Raia Hadsell, Oriol Vinyals, Mahyar Bordbar, and Nando de Freitas. A generalist agent. _Transactions on Machine Learning Research (TMLR)_ , 2022. 

- [151] Kuang-Huei Lee, Ofir Nachum, Mengjiao Yang, Lisa Lee, Daniel Freeman, Winnie Xu, Sergio Guadarrama, Ian Fischer, Eric Jang, Henryk Michalewski, and Igor Mordatch. Multi-game decision transformers. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 35, pages 27921–27936, 2022. 

- [152] Michael Laskin, Luyu Wang, Junhyuk Oh, Emilio Parisotto, Stephen Spencer, Richie Steigerwald, DJ Strouse, Steven Hansen, Angelos Filos, Ethan Brooks, Maxime Gazeau, Himanshu Sahni, Satinder Singh, and Volodymyr Mnih. In-context reinforcement learning with algorithm distillation. In _International Conference on Learning Representations (ICLR)_ , 2023. 

- [153] Chang Chen, Yi-Fu Wu, Jaesik Yoon, and Sungjin Ahn. Transdreamer: Reinforcement learning with transformer world models. _arXiv preprint arXiv:2202.09481_ , 2022. 

- [154] Jan Robine, Marc Höftmann, Tobias Uelwer, and Stefan Harmeling. Transformer-based world models are happy with 100k interactions. In _International Conference on Learning Representations (ICLR)_ , 2023. 

- [155] Vincent Micheli, Eloi Alonso, and François Fleuret. Efficient world models with contextaware tokenization. In _International Conference on Machine Learning (ICML)_ , 2024. arXiv:2406.19320. 

- [156] Pranav Agarwal, Sheldon Andrews, and Samira Ebrahimi Kahou. DART: Learning to play atari in a world of tokens. In _International Conference on Machine Learning (ICML)_ , volume 235, pages 313–328. PMLR, 2024. 

- [157] Antoine Dedieu, Joseph Ortiz, Xinghua Lou, Carter Wendelken, Wolfgang Lehrach, J. Swaroop Guntupalli, Miguel Lazaro-Gredilla, and Kevin Murphy. Improving transformer world models for data-efficient RL. In _International Conference on Machine Learning (ICML)_ , volume 267. PMLR, 2025. 

- [158] Sherry Yang, Yilun Du, Kamyar Ghasemipour, Jonathan Tompson, Leslie Kaelbling, Dale Schuurmans, and Pieter Abbeel. Learning interactive real-world simulators. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- [159] Decart Quevedo, Ethan McIntyre, Jack Campbell, Brendan Chen, and Dash Wachen. Oasis: A universe in a transformer. _Technical Report_ , 2024. URL: `https://oasis-model.github. io/` . 

- [160] Jiannan Xiang, Guangyi Liu, Yi Gu, Qiyue Gao, Yuting Ning, Yuheng Zha, Zeyu Feng, Tianhua Tao, Shibo Hao, Yemin Shi, Zhengzhong Liu, Eric P. Xing, and Zhiting Hu. Pandora: Towards general world model with natural language actions and video states. _arXiv preprint arXiv:2406.09455_ , 2024. 

123 

- [161] Tim Brooks, Bill Peebles, Connor Holmes, Will DePue, Yufei Guo, Li Jing, David Schnurr, Joe Taylor, Troy Luhman, Eric Luhman, Clarence Ng, Ricky Wang, and Aditya Ramesh. Video generation models as world simulators. Technical report, OpenAI, 2024. Technical Report, February 2024. 

- [162] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, Lewei Lu, Xiaosong Jia, Qiang Liu, Jifeng Dai, Yu Qiao, and Hongyang Li. Planning-oriented autonomous driving. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2023. Best Paper Award. 

- [163] Anthony Hu, Gianluca Corrado, Nicolas Griffiths, Zak Murez, Corina Gurau, Hudson Yeo, Alex Kendall, Roberto Cipolla, and Jamie Shotton. Model-based imitation learning for urban driving. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 35, 2022. 

- [164] Zetong Yang, Li Chen, Yanan Sun, and Hongyang Li. Visual point cloud forecasting enables scalable autonomous driving. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. Highlight. 

- [165] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, Pete Florence, Chuyuan Fu, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Kehang Han, Karol Hausman, Alexander Herzog, Jasmine Hsu, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Lisa Lee, Tsang-Wei Edward Lee, Sergey Levine, Yao Lu, Henryk Michalewski, Igor Mordatch, Karl Pertsch, Kanishka Rao, Krista Reymann, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Pierre Sermanet, Jaspiar Singh, Anikait Singh, Radu Soricut, Huong Tran, Vincent Vanhoucke, Quan Vuong, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Jialin Wu, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. RT-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 

- [166] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. In _Advances in Neural Information Processing Systems_ , volume 33, pages 6840–6851, 2020. 

- [167] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Björn Ommer. High-resolution image synthesis with latent diffusion models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 10684–10695, 2022. 

- [168] OpenAI. Video generation models as world simulators. _OpenAI Technical Report_ , 2024. 

- [169] Michael Janner, Yilun Du, Joshua B. Tenenbaum, and Sergey Levine. Planning with diffusion for flexible behavior synthesis. In _Proceedings of the 39th International Conference on Machine Learning (ICML)_ , volume 162 of _Proceedings of Machine Learning Research_ , pages 9902–9915. PMLR, 2022. 

- [170] Anurag Ajay, Yilun Du, Abhi Gupta, Joshua B. Tenenbaum, Tommi S. Jaakkola, and Pulkit Agrawal. Is conditional generative modeling all you need for decision-making? In _The Eleventh International Conference on Learning Representations (ICLR)_ , 2023. 

- [171] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. In _International Conference on Learning Representations (ICLR)_ , 2020. 

124 

- [172] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse control tasks through world models. _Nature_ , 2025. 

- [173] Tero Karras, Miika Aittala, Timo Aila, and Samuli Laine. Elucidating the design space of diffusion-based generative models. In _Advances in Neural Information Processing Systems_ , volume 35, pages 26565–26577, 2022. 

- [174] Nedko Savov, Naser Kazemi, Deheng Zhang, Danda Pani Paudel, Xi Wang, and Luc Van Gool. StateSpaceDiffuser: Bringing long context to diffusion world models. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. arXiv:2505.22246. 

- [175] Zhennan Jiang, Kai Liu, Yuxin Qin, Shuai Tian, Yupeng Zheng, Mingcai Zhou, Chao Yu, Haoran Li, and Dongbin Zhao. World4RL: Diffusion world models for policy refinement with reinforcement learning for robotic manipulation. _arXiv preprint arXiv:2509.19080_ , 2025. 

- [176] Akshay L Chandra, Iman Nematollahi, Chenguang Huang, Tim Welschehold, Wolfram Burgard, and Abhinav Valada. DiWA: Diffusion policy adaptation with world models. _arXiv preprint arXiv:2508.03645_ , 2025. 

- [177] Haoxuan Che, Xuanhua He, Quande Liu, Cheng Jin, and Hao Chen. GameGen-X: Interactive open-world game video generation. In _The Thirteenth International Conference on Learning Representations (ICLR)_ , 2025. 

- [178] William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 4195–4205, 2023. 

- [179] Zhuoyi Yang, Jiayan Teng, Wendi Zheng, Ming Ding, Shiyu Huang, Jiazheng Xu, Yuanming Yang, Wenyi Hong, Xiaohan Zhang, Guanyu Feng, et al. CogVideoX: Text-to-video diffusion models with an expert transformer. In _The Thirteenth International Conference on Learning Representations (ICLR)_ , 2025. 

- [180] Guosheng Zhao, Chaojun Ni, Xiaofeng Wang, Zheng Zhu, Xingle Zhang, Yida Wang, Guan Huang, Xinze Chen, Boyuan Wang, Youyi Zhang, et al. DriveDreamer4D: World models are effective data machines for 4d driving scene representation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2025. 

- [181] Lanqing Zheng, Xinqing Li, et al. GenAD: Generalized predictive model for autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 

- [182] Wayve. GAIA-2: A controllable multi-view generative world model for autonomous driving. _arXiv preprint arXiv:2503.20523_ , 2025. 

- [183] Lening Wang, Wenzhao Zheng, et al. OccSora: 4d occupancy generation models as world simulators for autonomous driving. In _The Thirteenth International Conference on Learning Representations (ICLR)_ , 2025. 

- [184] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. In _Robotics: Science and Systems (RSS)_ , 2023. 

125 

- [185] Siyuan Zhou, Yilun Du, Jiaben Chen, Yandong Li, Dit-Yan Yeung, and Chuang Gan. RoboDreamer: Learning compositional world models for robot imagination. In _Proceedings of the 41st International Conference on Machine Learning (ICML)_ , volume 235 of _Proceedings of Machine Learning Research_ , pages 61885–61896. PMLR, 2024. 

- [186] Leonardo Barcellona, Matteo Borselli, Francesco Sclafani, Vedant Kambhampati, et al. Dream to manipulate: Compositional world models empowering robot imitation learning with imagination. _arXiv preprint arXiv:2412.14957_ , 2024. 

- [187] Fangqi Zhu et al. IRASim: Learning interactive real-robot action simulators. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2025. arXiv:2406.14540. 

- [188] Haoyu Zhen, Qiao Sun, Hongxin Zhang, Junyan Li, Siyuan Zhou, Yilun Du, and Chuang Gan. TesserAct: Learning 4d embodied world models. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2025. arXiv:2504.20995. 

- [189] Yang Song, Prafulla Dhariwal, Mark Chen, and Ilya Sutskever. Consistency models. In _International Conference on Machine Learning (ICML)_ , 2023. arXiv:2303.01469. 

- [190] Samuel Greydanus, Misko Dzamba, and Jason Yosinski. Hamiltonian neural networks. In H. Wallach, H. Larochelle, A. Beygelzimer, F. d'Alché-Buc, E. Fox, and R. Garnett, editors, _Advances in Neural Information Processing Systems_ , volume 32. Curran Associates, Inc., 2019. URL `https://proceedings.neurips.cc/paper_files/paper/2019/ file/26cd8ecadce0d4efd6cc8a8725cbd1f8-Paper.pdf` . 

- [191] Miles Cranmer, Sam Greydanus, Stephan Hoyer, Peter Battaglia, David Spergel, and Shirley Ho. Lagrangian neural networks, 2020. URL `https://arxiv.org/abs/2003.04630` . 

- [192] Michael Lutter, Christian Ritter, and Jan Peters. Deep lagrangian networks: Using physics as model prior for deep learning, 2019. URL `https://arxiv.org/abs/1907.04490` . 

- [193] Yaofeng Desmond Zhong, Biswadip Dey, and Amit Chakraborty. Symplectic ode-net: Learning hamiltonian dynamics with control. In _International Conference on Learning Representations_ , 2020. URL `https://openreview.net/forum?id=ryxmb1rKDS` . 

- [194] Ricky T. Q. Chen, Yulia Rubanova, Jesse Bettencourt, and David K Duvenaud. Neural ordinary differential equations. In S. Bengio, H. Wallach, H. Larochelle, K. Grauman, N. CesaBianchi, and R. Garnett, editors, _Advances in Neural Information Processing Systems_ , volume 31. Curran Associates, Inc., 2018. URL `https://proceedings.neurips.cc/paper_ files/paper/2018/file/69386f6bb1dfed68692a24c8686939b9-Paper.pdf` . 

- [195] Marc Finzi, Ke Alexander Wang, and Andrew G Wilson. Simplifying hamiltonian and lagrangian neural networks via explicit constraints. In H. Larochelle, M. Ranzato, R. Hadsell, M.F. Balcan, and H. Lin, editors, _Advances in Neural Information Processing Systems_ , volume 33, pages 13880–13889. Curran Associates, Inc., 2020. URL `https://proceedings.neurips.cc/paper_files/paper/2020/file/ 9f655cc8884fda7ad6d8a6fb15cc001e-Paper.pdf` . 

- [196] Peter Toth, Danilo J. Rezende, Andrew Jaegle, Sébastien Racanière, Aleksandar Botev, and Irina Higgins. Hamiltonian generative networks. In _International Conference on Learning Representations_ , 2020. URL `https://openreview.net/forum?id=HJenn6VFvB` . 

126 

- [197] Yunzhu Li, Hao He, Jiajun Wu, Dina Katabi, and Antonio Torralba. Learning compositional koopman operators for model-based control. In _International Conference on Learning Representations_ , 2020. URL `https://openreview.net/forum?id=H1ldzA4tPr` . 

- [198] Peter Battaglia, Razvan Pascanu, Matthew Lai, Danilo Jimenez Rezende, and koray kavukcuoglu. Interaction networks for learning about objects, relations and physics. In D. Lee, M. Sugiyama, U. Luxburg, I. Guyon, and R. Garnett, editors, _Advances in Neural Information Processing Systems_ , volume 29. Curran Associates, Inc., 2016. URL `https://proceedings.neurips.cc/paper_files/paper/2016/file/ 3147da8ab4a0437c15ef51a5cc7f2dc4-Paper.pdf` . 

- [199] Peter W. Battaglia, Jessica B. Hamrick, Victor Bapst, Alvaro Sanchez-Gonzalez, Vinicius Zambaldi, Mateusz Malinowski, Andrea Tacchetti, David Raposo, Adam Santoro, Ryan Faulkner, Caglar Gulcehre, Francis Song, Andrew Ballard, Justin Gilmer, George Dahl, Ashish Vaswani, Kelsey Allen, Charles Nash, Victoria Langston, Chris Dyer, Nicolas Heess, Daan Wierstra, Pushmeet Kohli, Matt Botvinick, Oriol Vinyals, Yujia Li, and Razvan Pascanu. Relational inductive biases, deep learning, and graph networks, 2018. URL `https://arxiv.org/abs/1806.01261` . 

- [200] Alvaro Sanchez-Gonzalez, Jonathan Godwin, Tobias Pfaff, Rex Ying, Jure Leskovec, and Peter Battaglia. Learning to simulate complex physics with graph networks. In Hal Daumé III and Aarti Singh, editors, _Proceedings of the 37th International Conference on Machine Learning_ , volume 119 of _Proceedings of Machine Learning Research_ , pages 8459–8468. PMLR, 13–18 Jul 2020. URL `https://proceedings.mlr.press/v119/sanchez-gonzalez20a.html` . 

- [201] Tobias Pfaff, Meire Fortunato, Alvaro Sanchez-Gonzalez, and Peter Battaglia. Learning mesh-based simulation with graph networks. In _International Conference on Learning Representations_ , 2021. URL `https://openreview.net/forum?id=roNqYL0_XP` . 

- [202] Thomas Kipf, Ethan Fetaya, Kuan-Chieh Wang, Max Welling, and Richard Zemel. Neural relational inference for interacting systems. In Jennifer Dy and Andreas Krause, editors, _Proceedings of the 35th International Conference on Machine Learning_ , volume 80 of _Proceedings of Machine Learning Research_ , pages 2688–2697. PMLR, 10–15 Jul 2018. URL `https://proceedings.mlr.press/v80/kipf18a.html` . 

- [203] Yunzhu Li, Jiajun Wu, Russ Tedrake, Joshua B. Tenenbaum, and Antonio Torralba. Learning particle dynamics for manipulating rigid bodies, deformable objects, and fluids, 2019. URL `https://arxiv.org/abs/1810.01566` . 

- [204] Yunzhu Li, Toru Lin, Kexin Yi, Daniel Bear, Daniel Yamins, Jiajun Wu, Joshua Tenenbaum, and Antonio Torralba. Visual grounding of learned physical models. In Hal Daumé III and Aarti Singh, editors, _Proceedings of the 37th International Conference on Machine Learning_ , volume 119 of _Proceedings of Machine Learning Research_ , pages 5927–5936. PMLR, 13–18 Jul 2020. URL `https://proceedings.mlr.press/v119/li20j.html` . 

- [205] Francesco Locatello, Dirk Weissenborn, Thomas Unterthiner, Aravindh Mahendran, Georg Heigold, Jakob Uszkoreit, Alexey Dosovitskiy, and Thomas Kipf. Object-centric learning with slot attention. In H. Larochelle, M. Ranzato, R. Hadsell, M.F. Balcan, and H. Lin, editors, _Advances in Neural Information Processing Systems_ , volume 33, pages 11525–11538. Curran Associates, Inc., 2020. URL `https://proceedings.neurips.cc/paper_files/paper/ 2020/file/8511df98c02ab60aea1b2356c013bc0f-Paper.pdf` . 

127 

- [206] Thomas Kipf, Gamaleldin Fathy Elsayed, Aravindh Mahendran, Austin Stone, Sara Sabour, Georg Heigold, Rico Jonschkowski, Alexey Dosovitskiy, and Klaus Greff. Conditional objectcentric learning from video. In _International Conference on Learning Representations_ , 2022. URL `https://openreview.net/forum?id=aD7uesX1GF_` . 

- [207] Ziyi Wu, Nikita Dvornik, Klaus Greff, Thomas Kipf, and Animesh Garg. Slotformer: Unsupervised visual dynamics simulation with object-centric models. In _The Eleventh International Conference on Learning Representations_ , 2023. URL `https://openreview.net/forum?id= TFbwV6I0VLg` . 

- [208] Whie Jung, Jaehoon Yoo, Sungjin Ahn, and Seunghoon Hong. Learning to compose: Improving object centric learning by injecting compositionality. In _The Twelfth International Conference on Learning Representations_ , 2024. URL `https://openreview.net/forum?id= HT2dAhh4uV` . 

- [209] Malte Mosbach, Jan Niklas Ewertz, Angel Villar-Corrales, and Sven Behnke. SOLD: Slot object-centric latent dynamics models for relational manipulation learning from pixels. In Aarti Singh, Maryam Fazel, Daniel Hsu, Simon Lacoste-Julien, Felix Berkenkamp, Tegan Maharaj, Kiri Wagstaff, and Jerry Zhu, editors, _Proceedings of the 42nd International Conference on Machine Learning_ , volume 267 of _Proceedings of Machine Learning Research_ , pages 44911– 44935. PMLR, 13–19 Jul 2025. URL `https://proceedings.mlr.press/v267/mosbach25a. html` . 

- [210] Rishi Veerapaneni, John D. Co-Reyes, Michael Chang, Michael Janner, Chelsea Finn, Jiajun Wu, Joshua Tenenbaum, and Sergey Levine. Entity abstraction in visual modelbased reinforcement learning. In Leslie Pack Kaelbling, Danica Kragic, and Komei Sugiura, editors, _Proceedings of the Conference on Robot Learning_ , volume 100 of _Proceedings of Machine Learning Research_ , pages 1439–1456. PMLR, 30 Oct–01 Nov 2020. URL `https://proceedings.mlr.press/v100/veerapaneni20a.html` . 

- [211] Martin Engelcke, Adam R. Kosiorek, Oiwi Parker Jones, and Ingmar Posner. Genesis: Generative scene inference and sampling with object-centric latent representations. In _International Conference on Learning Representations_ , 2020. URL `https://openreview.net/forum?id= BkxfaTVFwH` . 

- [212] Junyeob Baek, Yi-Fu Wu, Gautam Singh, and Sungjin Ahn. Dreamweaver: Learning compositional world models from pixels. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL `https://openreview.net/forum?id=e5mTvjXG9u` . 

- [213] Yosuke Nishimoto and Takashi Matsubara. Object-centric world models for causality-aware reinforcement learning. _Proceedings of the AAAI Conference on Artificial Intelligence_ , 40 (29):24585–24593, Mar. 2026. doi: 10.1609/aaai.v40i29.39642. URL `https://ojs.aaai. org/index.php/AAAI/article/view/39642` . 

- [214] Fan Feng, Phillip Lippe, and Sara Magliacane. Learning interactive world model for objectcentric reinforcement learning. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. URL `https://openreview.net/forum?id=E0cjqfM55C` . 

- [215] Víctor Garcia Satorras, Emiel Hoogeboom, and Max Welling. E(n) equivariant graph neural networks. In Marina Meila and Tong Zhang, editors, _Proceedings of the 38th International Conference on Machine Learning_ , volume 139 of _Proceedings of Machine Learning Research_ , 

128 

pages 9323–9332. PMLR, 18–24 Jul 2021. URL `https://proceedings.mlr.press/v139/ satorras21a.html` . 

- [216] Jiaqi Han, Wenbing Huang, Hengbo Ma, Jiachen Li, Josh Tenenbaum, and Chuang Gan. Learning physical dynamics with subequivariant graph neural networks. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, editors, _Advances in Neural Information Processing Systems_ , volume 35, pages 26256–26268. Curran Associates, Inc., 2022. URL `https://proceedings.neurips.cc/paper_files/paper/2022/file/ a845fdc3f87751710218718adb634fe7-Paper-Conference.pdf` . 

- [217] Yang Liu, Jiashun Cheng, Haihong Zhao, Tingyang Xu, Peilin Zhao, Fugee Tsung, Jia Li, and Yu Rong. SEGNO: Generalizing equivariant graph neural networks with physical inductive biases. In _The Twelfth International Conference on Learning Representations_ , 2024. URL `https://openreview.net/forum?id=3oTPsORaDH` . 

- [218] Hansen Lillemark, Benhao Huang, Fangneng Zhan, Yilun Du, and T. Anderson Keller. Flow equivariant world models: Structured dynamics outside the field of view. In _NeurIPS 2025 Workshop on Space in Vision, Language, and Embodied AI_ , 2025. URL `https://openreview. net/forum?id=hq2nQ1K7E5` . 

- [219] Miles Cranmer, Alvaro Sanchez Gonzalez, Peter Battaglia, Rui Xu, Kyle Cranmer, David Spergel, and Shirley Ho. Discovering symbolic models from deep learning with inductive biases. In H. Larochelle, M. Ranzato, R. Hadsell, M.F. Balcan, and H. Lin, editors, _Advances in Neural Information Processing Systems_ , volume 33, pages 17429–17442. Curran Associates, Inc., 2020. URL `https://proceedings.neurips.cc/paper_files/paper/2020/ file/c9f2f917078bd2db12f23c3b413d9cba-Paper.pdf` . 

- [220] Atharva Sehgal, Arya Grayeli, Jennifer J. Sun, and Swarat Chaudhuri. Neurosymbolic grounding for compositional world models. In _The Twelfth International Conference on Learning Representations_ , 2024. URL `https://openreview.net/forum?id=4KZpDGD4Nh` . 

- [221] Daniel Bear, Elias Wang, Damian Mrowca, Felix Jedidja Binder, Hsiao-Yu Tung, RT Pramod, Cameron Holdaway, Sirui Tao, Kevin A. Smith, Fan-Yun Sun, Li Fei-Fei, Nancy Kanwisher, Joshua B. Tenenbaum, Daniel LK Yamins, and Judith E Fan. Physion: Evaluating physical prediction from vision in humans and machines. In _Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 1)_ , 2021. URL `https://openreview.net/forum?id=CXyZrKPz4CU` . 

- [222] Elie Aljalbout, Nikolaos Sotirakis, Patrick van der Smagt, Maximilian Karl, and Nutan Chen. Limt: Language-informed multi-task visual world models. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 8226–8233, 2025. doi: 10.1109/ICRA55743.2025.11128817. 

- [223] Iman Nematollahi, Branton DeMoss, Akshay L Chandra, Nick Hawes, Wolfram Burgard, and Ingmar Posner. Lumos: Language-conditioned imitation learning with world models. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 8219–8225, 2025. doi: 10.1109/ICRA55743.2025.11127988. 

- [224] Joe Nguyen and Stefan Lee. Language-conditioned world model improves policy generalization by reading environmental descriptions. In _NeurIPS 2025 Workshop on Bridging Language, Agent, and World Models for Reasoning and Planning_ , 2025. URL `https: //openreview.net/forum?id=ClrjcLTKBt` . 

129 

- [225] Kaige Xie, Ian Yang, John Gunerli, and Mark Riedl. Making large language models into world models with precondition and effect knowledge. In Owen Rambow, Leo Wanner, Marianna Apidianaki, Hend Al-Khalifa, Barbara Di Eugenio, and Steven Schockaert, editors, _Proceedings of the 31st International Conference on Computational Linguistics_ , pages 7532– 7545, Abu Dhabi, UAE, January 2025. Association for Computational Linguistics. URL `https://aclanthology.org/2025.coling-main.503/` . 

- [226] Thomas Carta, Clément Romac, Thomas Wolf, Sylvain Lamprier, Olivier Sigaud, and PierreYves Oudeyer. Grounding large language models in interactive environments with online reinforcement learning. In Andreas Krause, Emma Brunskill, Kyunghyun Cho, Barbara Engelhardt, Sivan Sabato, and Jonathan Scarlett, editors, _Proceedings of the 40th International Conference on Machine Learning_ , volume 202 of _Proceedings of Machine Learning Research_ , pages 3676–3713. PMLR, 23–29 Jul 2023. URL `https://proceedings.mlr.press/v202/ carta23a.html` . 

- [227] John Gkountouras, Matthias Lindemann, Phillip Lippe, Efstratios Gavves, and Ivan Titov. Language agents meet causality – bridging LLMs and causal world models. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL `https://openreview. net/forum?id=y9A2TpaGsE` . 

- [228] Delong Chen, Mustafa Shukor, Theo Moutakanni, Willy Chung, Jade Yu, Tejaswi Kasarla, Yejin Bang, Allen Bolourchi, Yann LeCun, and Pascale Fung. Vl-jepa: Joint embedding predictive architecture for vision-language, 2026. URL `https://arxiv.org/abs/2512.10942` . 

- [229] Jacob Berg, Chuning Zhu, Yanda Bao, Ishan Durugkar, and Abhishek Gupta. Semantic world models. _arXiv preprint arXiv:2510.19818_ , 2025. 

- [230] Zhiqi Ge, Hongzhe Huang, Mingze Zhou, Juncheng Li, Guoming Wang, Siliang Tang, and Yueting Zhuang. Worldgpt: Empowering llm as multimodal world model. In _Proceedings of the 32nd ACM International Conference on Multimedia_ , MM ’24, page 7346–7355, New York, NY, USA, 2024. Association for Computing Machinery. ISBN 9798400706868. doi: 10.1145/3664647.3681488. URL `https://doi.org/10.1145/3664647.3681488` . 

- [231] Kevin Black, Mitsuhiko Nakamoto, Pranav Atreya, Homer Walke, Chelsea Finn, Aviral Kumar, and Sergey Levine. Zero-shot robotic manipulation with pretrained image-editing diffusion models, 2023. URL `https://arxiv.org/abs/2310.10639` . 

- [232] Jessica B Hamrick. Analogues of mental simulation and imagination in deep learning. _Current Opinion in Behavioral Sciences_ , 29:8–16, 2019. 

- [233] Thomas M Moerland, Joost Broekens, Aske Plaat, and Catholijn M Jonker. Model-based reinforcement learning: A survey. _Foundations and Trends® in Machine Learning_ , 16(1): 1–118, 2023. 

- [234] Shangding Gu, Long Yang, Yali Du, Guang Chen, Florian Walter, Jun Wang, and Alois Knoll. A review of safe reinforcement learning: Methods, theories, and applications. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 46(12):11216–11235, 2024. 

- [235] Yuxiang Zheng, Dayuan Fu, Xiangkun Hu, Xiaojie Cai, Lyumanshan Ye, Pengrui Lu, and Pengfei Liu. Deepresearcher: Scaling deep research via reinforcement learning in real-world environments. In _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , pages 414–431, 2025. 

130 

- [236] Qi Lyu, Jiahua Dong, Baichen Liu, Xudong Wang, Wenqi Liang, Duzhen Zhang, Jiahang Tu, Hongliu Li, Hanbin Zhao, Henghui Ding, Yulun Zhang, Zhi Han, Nicu Sebe, Fahad Shahbaz Khan, Salman Khan, Mubarak Shah, Philip Torr, Ming-Hsuan Yang, and Dacheng Tao. Learning to model the world: A survey of world models in artificial intelligence. _TechRxiv_ , 2026(0305), 2026. doi: 10.36227/techrxiv.177274570.09578608/v1. URL `https://www.techrxiv.org/doi/abs/10.36227/techrxiv.177274570.09578608/v1` . 

- [237] Chenhao Li, Andreas Krause, and Marco Hutter. Robotic world model: A neural network simulator for robust policy optimization in robotics. _arXiv preprint arXiv:2501.10100_ , 2025. 

- [238] Sicheng Zuo, Wenzhao Zheng, Yuanhui Huang, Jie Zhou, and Jiwen Lu. Gaussianworld: Gaussian world model for streaming 3d occupancy prediction. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 6772–6781, 2025. 

- [239] Kai Xu, Hang Zhao, Ruizhen Hu, Yuhang Huang, Ziqiao Zhou, Wancheng Feng, Yi Li, Sida Peng, Xing Liu, Zihao Liu, et al. From specialist to generalist: A comprehensive survey on world models. _Authorea Preprints_ , 2026. 

- [240] Arif Hassan Zidan, Afrar Jahin, Yu Bao, Tianming Liu, and Wei Zhang. A theoretical and experimental exploration in permutation randomization on nonsmooth nonconvex optimization. _Contemporary Mathematics_ , page 2382–2403, April 2026. ISSN 2705-1064. doi: 10.37256/cm.7220268464. URL `http://dx.doi.org/10.37256/cm.7220268464` . 

- [241] Kao-Shing Hwang, Wei-Cheng Jiang, and Yu-Jen Chen. Model learning and knowledge sharing for a multiagent system with dyna-q learning. _IEEE transactions on cybernetics_ , 45(5): 978–990, 2014. 

- [242] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels. In _International conference on machine learning_ , pages 2555–2565. PMLR, 2019. 

- [243] Masashi Okada and Tadahiro Taniguchi. Dreaming: Model-based reinforcement learning by latent imagination without reconstruction. In _2021 ieee international conference on robotics and automation (icra)_ , pages 4209–4215. IEEE, 2021. 

- [244] Fei Deng, Ingook Jang, and Sungjin Ahn. Dreamerpro: Reconstruction-free model-based reinforcement learning with prototypical representations. In _International conference on machine learning_ , pages 4956–4975. PMLR, 2022. 

- [245] Nicolas Heess, Gregory Wayne, David Silver, Timothy Lillicrap, Tom Erez, and Yuval Tassa. Learning continuous control policies by stochastic value gradients. _Advances in neural information processing systems_ , 28, 2015. 

- [246] Jinke He, Thomas M Moerland, Joery A de Vries, and Frans A Oliehoek. What model does muzero learn? _arXiv preprint arXiv:2306.00840_ , 2023. 

- [247] Xiaodong Lu, Xiaohan Wang, Jiajun Chai, Guojun Yin, Wei Lin, Zhijun Chen, Yu Luo, Fuzhen Zhuang, Yikun Ban, and Deqing Wang. Contextual rollout bandits for reinforcement learning with verifiable rewards. _arXiv preprint arXiv:2602.08499_ , 2026. 

- [248] Xingzhou Lou, Dong Yan, Wei Shen, Yuzi Yan, Jian Xie, and Junge Zhang. Uncertaintyaware reward model: Teaching reward models to know what is unknown. _arXiv preprint arXiv:2410.00847_ , 2024. 

131 

- [249] Maxime Burchi and Radu Timofte. Learning transformer-based world models with contrastive predictive coding. _arXiv preprint arXiv:2503.04416_ , 2025. 

- [250] Judea Pearl and Dana Mackenzie. _The Book of Why: The New Science of Cause and Effect_ . Basic Books, 2018. 

- [251] Judea Pearl. _Causality: Models, Reasoning, and Inference_ . Cambridge University Press, 2nd edition, 2009. 

- [252] Lars Buesing, Theophane Weber, Yori Zwols, Sebastien Racaniere, Arthur Guez, JeanBaptiste Lespiau, and Nicolas Heess. Woulda, coulda, shoulda: Counterfactually-guided policy search. In _International Conference on Learning Representations_ , 2019. 

- [253] Irene Y. Chen et al. Beyond generative AI: World models for clinical prediction, counterfactuals, and planning. _arXiv preprint arXiv:2511.16333_ , 2025. 

- [254] Pim de Haan, Dinesh Dinesh, and Sergey Levine. Causal confusion in imitation learning. In _Advances in Neural Information Processing Systems_ , volume 32, 2019. 

- [255] Martin Arjovsky, Léon Bottou, Ishaan Gulrajani, and David Lopez-Paz. Invariant risk minimization. _arXiv preprint arXiv:1907.02893_ , 2019. 

- [256] Bernhard Schölkopf, Francesco Locatello, Stefan Bauer, Nan Rosemary Ke, Nal Kalchbrenner, Anirudh Goyal, and Yoshua Bengio. Toward causal representation learning. _Proceedings of the IEEE_ , 109(5):812–834, 2021. 

- [257] Maximilian Seitzer, Bernhard Schölkopf, and Georg Martius. Causal influence detection for improving efficiency in reinforcement learning. In _Advances in Neural Information Processing Systems_ , volume 34, pages 22905–22918, 2021. 

- [258] Valentin Thomas, Emmanuel Bengio, William Fedus, Jules Pondard, Philippe Beaudoin, Hugo Larochelle, Joelle Pineau, Doina Precup, and Yoshua Bengio. Independently controllable factors. In _Advances in Neural Information Processing Systems_ , volume 30, 2017. 

- [259] Jonas Peters, Dominik Janzing, and Bernhard Schölkopf. _Elements of Causal Inference: Foundations and Learning Algorithms_ . The MIT Press, 2017. 

- [260] Francesco Locatello, Stefan Bauer, Mario Lucic, Gunnar Raetsch, Sylvain Gelly, and Bernhard Schölkopf. Challenging common assumptions in the unsupervised learning of disentangled representations. In _International Conference on Machine Learning_ , pages 4114–4124. PMLR, 2019. 

- [261] Ramanan Sekar, Oleh Rybkin, Kostas Daniilidis, Pieter Abbeel, Danijar Hafner, and Deepak Pathak. Planning to explore via self-supervised world models. _International Conference on Machine Learning_ , pages 8583–8592, 2020. 

- [262] Rahul Kidambi, Aravind Rajeswaran, Praneeth Netrapalli, and Thorsten Joachims. MOReL: Model-based offline reinforcement learning. In _Advances in Neural Information Processing Systems_ , volume 33, 2020. 

- [263] Marc Rigter, Bruno Lacerda, and Nick Hawes. RAMBO-RL: Robust adversarial model-based offline reinforcement learning. In _Advances in Neural Information Processing Systems_ , 2022. 

132 

- [264] Javier García and Fernando Fernández. A comprehensive survey on safe reinforcement learning. _Journal of Machine Learning Research_ , 16(1):1437–1480, 2015. 

- [265] Yarden As, Ilnura Usmanova, Sebastian Curi, and Andreas Krause. Constrained policy optimization via Bayesian world models. In _International Conference on Learning Representations_ , 2022. 

- [266] Minting Pan, Xiangming Zhu, Yunbo Wang, and Xiaokang Yang. Iso-Dream: Isolating noncontrollable visual dynamics in world models. In _Advances in Neural Information Processing Systems_ , 2022. 

- [267] Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control. In _The Twelfth International Conference on Learning Representations_ , 2024. 

- [268] Adrien Bardes, Quentin Garrido, Jean Ponce, Xinlei Chen, Michael Rabbat, Yann LeCun, Mido Assran, and Nicolas Ballas. V-JEPA: Latent video prediction for visual representation learning, 2024. URL `https://openreview.net/forum?id=WFYbBOEOtv` . 

- [269] Leonardo Barcellona, Andrii Zadaianchuk, Davide Allegro, Samuele Papa, Stefano Ghidoni, and Efstratios Gavves. Dream to manipulate: Compositional world models empowering robot imitation learning with imagination. _arXiv preprint arXiv:2412.14957_ , 2024. 

- [270] Gaoyue Zhou, Hengkai Pan, Yann LeCun, and Lerrel Pinto. Dino-wm: World models on pretrained visual features enable zero-shot planning. _arXiv preprint arXiv:2411.04983_ , 2024. 

- [271] Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin Burchfiel, Paarth Shah, and Abhishek Gupta. Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. _arXiv preprint arXiv:2504.02792_ , 2025. 

- [272] Moo Jin Kim, Yihuai Gao, Tsung-Yi Lin, Yen-Chen Lin, Yunhao Ge, Grace Lam, Percy Liang, Shuran Song, Ming-Yu Liu, Chelsea Finn, et al. Cosmos policy: Fine-tuning video models for visuomotor control and planning. _arXiv preprint arXiv:2601.16163_ , 2026. 

- [273] Wenlong Huang, Yu-Wei Chao, Arsalan Mousavian, Ming-Yu Liu, Dieter Fox, Kaichun Mo, and Li Fei-Fei. Pointworld: Scaling 3d world models for in-the-wild robotic manipulation. _arXiv preprint arXiv:2601.03782_ , 2026. 

- [274] Chenhao Li, Andreas Krause, and Marco Hutter. Uncertainty-aware robotic world model makes offline model-based reinforcement learning work on real robots. _arXiv preprint arXiv:2504.16680_ , 2025. 

- [275] Hassan Abu Alhaija, Jose Alvarez, Maciej Bala, Tiffany Cai, Tianshi Cao, Liz Cha, Joshua Chen, Mike Chen, Francesco Ferroni, Sanja Fidler, et al. Cosmos-transfer1: Conditional world generation with adaptive multimodal control. _arXiv preprint arXiv:2503.14492_ , 2025. 

- [276] Pu Hua, Minghuan Liu, Annabella Macaluso, Yunfeng Lin, Weinan Zhang, Huazhe Xu, and Lirui Wang. Gensim2: Scaling robot data generation with multi-modal and reasoning llms. _arXiv preprint arXiv:2410.03645_ , 2024. 

- [277] Yufei Wang, Zhou Xian, Feng Chen, Tsun-Hsuan Wang, Yian Wang, Katerina Fragkiadaki, Zackory Erickson, David Held, and Chuang Gan. Robogen: Towards unleashing infinite data 

133 

for automated robot learning via generative simulation. _arXiv preprint arXiv:2311.01455_ , 2023. 

- [278] Francesco Locatello, Dirk Weissenborn, Thomas Unterthiner, Aravindh Mahendran, Georg Heigold, Jakob Uszkoreit, Alexey Dosovitskiy, and Thomas Kipf. Object-centric learning with slot attention. _Advances in neural information processing systems_ , 33:11525–11538, 2020. 

- [279] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3d-vla: A 3d vision-language-action generative world model. In _International Conference on Machine Learning_ , pages 61229–61245. PMLR, 2024. 

- [280] Saran Tunyasuvunakool, Alistair Muldal, Yotam Doron, Siqi Liu, Steven Bohez, Josh Merel, Tom Erez, Timothy Lillicrap, Nicolas Heess, and Yuval Tassa. dm_control: Software and tasks for continuous control. _Software Impacts_ , 6:100022, 2020. 

- [281] Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J Davison. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ , 5(2):3019–3026, 2020. 

- [282] Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Karol Hausman, Chelsea Finn, and Sergey Levine. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on robot learning_ , pages 1094–1100. PMLR, 2020. 

- [283] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 

- [284] Ruiyuan Gao, Kai Chen, Enze Xie, Lanqing Hong, Zhenguo Li, Dit-Yan Yeung, and Qiang Xu. Magicdrive: Street view generation with diverse 3d geometry control. _arXiv preprint arXiv:2310.02601_ , 2023. 

- [285] Chen Min, Dawei Zhao, Liang Xiao, Yiming Nie, and Bin Dai. Uniworld: Autonomous driving pre-training via world models. _arXiv preprint arXiv:2308.07234_ , 2023. 

- [286] Xiaosong Jia, Penghao Wu, Li Chen, Jiangwei Xie, Conghui He, Junchi Yan, and Hongyang Li. Think twice before driving: Towards scalable decoders for end-to-end autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 21983–21994, 2023. 

- [287] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 11621–11631, 2020. 

- [288] Pei Sun, Henrik Kretzschmar, Xerxes Dotiwalla, Aurelien Chouard, Vijaysai Patnaik, Paul Tsui, James Guo, Yin Zhou, Yuning Chai, Benjamin Caine, et al. Scalability in perception for autonomous driving: Waymo open dataset. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 2446–2454, 2020. 

- [289] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. CARLA: An open urban driving simulator. In _Conference on Robot Learning_ , pages 1–16, 2017. 

134 

- [290] Napat Karnchanachari, Dimitris Geromichalos, Kok Seang Tan, Nanxiang Li, Christopher Eriksen, Shakiba Yaghoubi, Noushin Mehdipour, Gianmarco Bernasconi, Whye Kit Fong, Yiluan Guo, et al. Towards learning-based planning: The nuplan benchmark for real-world autonomous driving. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 629–636. IEEE, 2024. 

- [291] Alex X Lee, Richard Zhang, Frederik Ebert, Pieter Abbeel, Chelsea Finn, and Sergey Levine. Stochastic adversarial video prediction. _arXiv preprint arXiv:1804.01523_ , 2018. 

- [292] Andreas Blattmann, Tim Dockhorn, Sumith Kulal, Daniel Mendelevitch, Maciej Kilian, Dominik Lorenz, Yam Levi, Zion English, Vikram Voleti, Adam Letts, et al. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_ , 2023. 

- [293] Zangwei Li, Xiangyu Li, Chenhui You, et al. Open-Sora: Democratizing efficient video production for all. _arXiv preprint arXiv:2412.20404_ , 2024. 

- [294] Boyuan Chen, Diego Martí Monsó, Yilun Du, Max Simchowitz, Russ Tedrake, and Vincent Sitzmann. Diffusion forcing: Next-token prediction meets full-sequence diffusion. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 37, 2024. arXiv:2407.01392. 

- [295] Sergiu Oprea, Pablo Martinez-Gonzalez, Alberto Garcia-Garcia, John Alejandro CastroVargas, Sergio Orts-Escolano, Jose Garcia-Rodriguez, and Antonis Argyros. A review on deep learning techniques for video prediction. In _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , volume 44, pages 2806–2826, 2022. 

- [296] Ruben Villegas, Mohammad Babaeizadeh, Pieter-Jan Kindermans, Hernan Moraldo, Han Zhang, Mohammad Taghi Saffar, Santiago Castro, Julius Kunze, and Dumitru Erhan. Phenaki: Variable length video generation from open domain textual descriptions. In _International Conference on Learning Representations_ , 2023. URL `https://openreview.net/ forum?id=vOEXS39nOF` . 

- [297] Dan Kondratyuk, Lijun Yu, Xiuye Gu, José Lezama, Jonathan Huang, Grant Schindler, Rachel Hornung, Vighnesh Birodkar, Jimmy Yan, Ming-Chang Chiu, Krishna Somandepalli, Hassan Akbari, Yair Alon, Yong Cheng, Josh Dillon, Agrim Gupta, Meera Hahn, Anja Hauth, David Hendon, Alonso Martinez, David Minnen, Mikhail Sirotenko, Kihyuk Sohn, Xuan Yang, Hartwig Adam, Ming-Hsuan Yang, Irfan Essa, Huisheng Wang, David A. Ross, Bryan Seybold, and Lu Jiang. Videopoet: a large language model for zero-shot video generation. In _Proceedings of the 41st International Conference on Machine Learning_ , ICML’24. JMLR.org, 2024. 

- [298] Uriel Singer, Adam Polyak, Thomas Hayes, Xi Yin, Jie An, Songyang Zhang, Qiyuan Hu, Harry Yang, Oron Ashual, Oran Gafni, et al. Make-a-video: Text-to-video generation without text-video data. _arXiv preprint arXiv:2209.14792_ , 2022. 

- [299] Jonathan Ho, William Chan, Chitwan Saharia, Jay Whang, Ruiqi Gao, Alexey Gritsenko, Diederik P Kingma, Ben Poole, Mohammad Norouzi, David J Fleet, et al. Imagen video: High definition video generation with diffusion models. _arXiv preprint arXiv:2210.02303_ , 2022. 

135 

- [300] Omer Bar-Tal, Hila Chefer, Omer Tov, Charles Herrmann, Roni Paiss, Shiran Zada, Ariel Ephrat, Junhwa Hur, Guanghui Liu, Amit Raj, Yuanzhen Li, Michael Rubinstein, Tomer Michaeli, Oliver Wang, Deqing Sun, Tali Dekel, and Inbar Mosseri. Lumiere: A space-time diffusion model for video generation. In _SIGGRAPH Asia 2024 Conference Papers_ , SA ’24, New York, NY, USA, 2024. Association for Computing Machinery. ISBN 9798400711312. doi: 10.1145/3680528.3687614. URL `https://doi.org/10.1145/3680528.3687614` . 

- [301] Agrim Gupta, Lijun Yu, Kihyuk Sohn, Xiuye Gu, Meera Hahn, Fei-Fei Li, Irfan Essa, Lu Jiang, and José Lezama. Photorealistic video generation with diffusion models. In _Computer Vision – ECCV 2024: 18th European Conference, Milan, Italy, September 29–October 4, 2024, Proceedings, Part LXXIX_ , page 393–411, Berlin, Heidelberg, 2024. Springer-Verlag. ISBN 978-3-031-72985-0. doi: 10.1007/978-3-031-72986-7_23. URL `https://doi.org/10. 1007/978-3-031-72986-7_23` . 

- [302] Adam Polyak, Amit Zohar, Andrew Brown, Andros Tjandra, Animesh Sinha, Ann Lee, Apoorv Vyas, Bowen Shi, Chih-Yao Ma, Ching-Yao Chuang, et al. Movie gen: A cast of media foundation models. _arXiv preprint arXiv:2410.13720_ , 2024. 

- [303] Tianyuan Zhang, Hong-Xing Yu, Rundi Wu, Brandon Y. Feng, Changxi Zheng, Noah Snavely, Jiajun Wu, and William T. Freeman. Physdreamer: Physics-based interaction with 3d objects via video generation. In _Computer Vision – ECCV 2024: 18th European Conference, Milan, Italy, September 29–October 4, 2024, Proceedings, Part II_ , page 388–406, Berlin, Heidelberg, 2024. Springer-Verlag. ISBN 978-3-031-72626-2. doi: 10.1007/978-3-031-72627-9_22. URL `https://doi.org/10.1007/978-3-031-72627-9_22` . 

- [304] Yiran Qin, Hao Shi, Zhen Yu, Lei Wang, Yang Zhou, Ziwei Li, Xi Yin, Shuai Liu, Lu Sheng, Jing Shao, Lei Bai, Wanli Ouyang, and Yingcong Zhang. WorldSimBench: Towards video generation models as world simulators. In _International Conference on Learning Representations (ICLR)_ , 2025. arXiv:2410.18072. 

- [305] Ge Luo, Tommaso Favero, Zhiwei Luo, Alexia Jolicoeur-Martineau, and Christopher Pal. Beyond FVD: Enhanced evaluation metrics for video generation quality. In _International Conference on Learning Representations (ICLR)_ , 2025. arXiv:2410.05203. 

- [306] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, et al. Do as i can, not as i say: Grounding language in robotic affordances. _arXiv preprint arXiv:2204.01691_ , 2022. 

- [307] Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, Yevgen Chebotar, Pierre Sermanet, Daniel Duckworth, Sergey Levine, Vincent Vanhoucke, Karol Hausman, Marc Toussaint, Klaus Greff, Andy Zeng, Igor Mordatch, and Pete Florence. PaLM-e: An embodied multimodal language model. In Andreas Krause, Emma Brunskill, Kyunghyun Cho, Barbara Engelhardt, Sivan Sabato, and Jonathan Scarlett, editors, _Proceedings of the 40th International Conference on Machine Learning_ , volume 202 of _Proceedings of Machine Learning Research_ , pages 8469–8488. PMLR, 23–29 Jul 2023. URL `https://proceedings.mlr.press/v202/driess23a.html` . 

- [308] Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, Pierre Sermanet, Tomas Jackson, Noah 

136 

Brown, Linda Luu, Sergey Levine, Karol Hausman, and brian ichter. Inner monologue: Embodied reasoning through planning with language models. In Karen Liu, Dana Kulic, and Jeff Ichnowski, editors, _Proceedings of The 6th Conference on Robot Learning_ , volume 205 of _Proceedings of Machine Learning Research_ , pages 1769–1782. PMLR, 14–18 Dec 2023. URL `https://proceedings.mlr.press/v205/huang23c.html` . 

- [309] Andy Zeng, Maria Attarian, brian ichter, Krzysztof Marcin Choromanski, Adrian Wong, Stefan Welker, Federico Tombari, Aveek Purohit, Michael S Ryoo, Vikas Sindhwani, Johnny Lee, Vincent Vanhoucke, and Pete Florence. Socratic models: Composing zero-shot multimodal reasoning with language. In _The Eleventh International Conference on Learning Representations_ , 2023. URL `https://openreview.net/forum?id=G2Q2Mh3avow` . 

- [310] Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete Florence, and Andy Zeng. Code as policies: Language model programs for embodied control. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9493–9500, 2023. doi: 10.1109/ICRA48891.2023.10160591. 

- [311] Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, and Li Fei-Fei. Voxposer: Composable 3d value maps for robotic manipulation with language models. In Jie Tan, Marc Toussaint, and Kourosh Darvish, editors, _Proceedings of The 7th Conference on Robot Learning_ , volume 229 of _Proceedings of Machine Learning Research_ , pages 540–562. PMLR, 06–09 Nov 2023. URL `https://proceedings.mlr.press/v229/huang23b.html` . 

- [312] Yecheng Jason Ma, William Liang, Guanzhi Wang, De-An Huang, Osbert Bastani, Dinesh Jayaraman, Yuke Zhu, Linxi Fan, and Anima Anandkumar. Eureka: Human-level reward design via coding large language models. In _The Twelfth International Conference on Learning Representations_ , 2024. URL `https://openreview.net/forum?id=IEduRUO55F` . 

- [313] Linxi Fan, Guanzhi Wang, Yunfan Jiang, Ajay Mandlekar, Yuncong Yang, Haoyi Zhu, Andrew Tang, De-An Huang, Yuke Zhu, and Anima Anandkumar. Minedojo: Building open-ended embodied agents with internet-scale knowledge. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, editors, _Advances in Neural Information Processing Systems_ , volume 35, pages 18343–18362. Curran Associates, Inc., 2022. URL `https://proceedings.neurips.cc/paper_files/paper/2022/file/ 74a67268c5cc5910f64938cac4526a90-Paper-Datasets_and_Benchmarks.pdf` . 

- [314] Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. Voyager: An open-ended embodied agent with large language models. _Transactions on Machine Learning Research_ , 2024. ISSN 2835-8856. URL `https: //openreview.net/forum?id=ehfRiF0R3a` . 

- [315] Zihao Wang, Shaofei Cai, Guanzhou Chen, Anji Liu, Xiaojian Ma, Yitao Liang, and Team CraftJarvis. Describe, explain, plan and select: interactive planning with large language models enables open-world multi-task agents. In _Proceedings of the 37th International Conference on Neural Information Processing Systems_ , NIPS ’23, Red Hook, NY, USA, 2023. Curran Associates Inc. 

- [316] Zihao Wang, Shaofei Cai, Anji Liu, Yonggang Jin, Jinbing Hou, Bowei Zhang, Haowei Lin, Zhaofeng He, Zilong Zheng, Yaodong Yang, Xiaojian Ma, and Yitao Liang. Jarvis-1: Open-world multi-task agents with memory-augmented multimodal language models. _IEEE_ 

137 

_Transactions on Pattern Analysis and Machine Intelligence_ , 47(3):1894–1907, 2025. doi: 10.1109/TPAMI.2024.3511593. 

- [317] Shalev Lifshitz, Keiran Paster, Harris Chan, Jimmy Ba, and Sheila McIlraith. Steve1: A generative model for text-to-behavior in minecraft. In A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, and S. Levine, editors, _Advances in Neural Information Processing Systems_ , volume 36, pages 69900–69929. Curran Associates, Inc., 2023. URL `https://proceedings.neurips.cc/paper_files/paper/2023/file/ dd03f856fc7f2efeec8b1c796284561d-Paper-Conference.pdf` . 

- [318] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- [319] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [320] Yunfan Jiang, Agrim Gupta, Zichen Zhang, Guanzhi Wang, Yongqiang Dou, Yanjun Chen, Li Fei-Fei, Anima Anandkumar, Yuke Zhu, and Linxi Fan. VIMA: General robot manipulation with multimodal prompts, 2023. URL `https://openreview.net/forum?id=hzjQWjPC04A` . 

- [321] Wenyi Hong, Weihan Wang, Qingsong Lv, Jiazheng Xu, Wenmeng Yu, Junhui Ji, Yan Wang, Zihan Wang, Yuxiao Dong, Ming Ding, and Jie Tang. Cogagent: A visual language model for gui agents. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 14281–14290, June 2024. 

- [322] Weihao Tan, Wentao Zhang, Xinrun Xu, Haochong Xia, Ziluo Ding, Boyu Li, Bohan Zhou, Junpeng Yue, Jiechuan Jiang, Yewen Li, Ruyi An, Molei Qin, Chuqiao Zong, Longtao Zheng, Yujie Wu, Xiaoqiang Chai, Yifei Bi, Tianbao Xie, Pengjie Gu, Xiyun Li, Ceyao Zhang, Long Tian, Chaojie Wang, Xinrun Wang, Börje F. Karlsson, Bo An, Shuicheng Yan, and Zongqing Lu. Cradle: Empowering foundation agents towards general computer control. In Aarti Singh, Maryam Fazel, Daniel Hsu, Simon Lacoste-Julien, Felix Berkenkamp, Tegan Maharaj, Kiri Wagstaff, and Jerry Zhu, editors, _Proceedings of the 42nd International Conference on Machine Learning_ , volume 267 of _Proceedings of Machine Learning Research_ , pages 58658– 58725. PMLR, 13–19 Jul 2025. URL `https://proceedings.mlr.press/v267/tan25h.html` . 

- [323] Shuyan Zhou, Frank F. Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue Ou, Yonatan Bisk, Daniel Fried, Uri Alon, and Graham Neubig. Webarena: A realistic web environment for building autonomous agents. In _The Twelfth International Conference on Learning Representations_ , 2024. URL `https://openreview.net/forum?id= oKn9c6ytLx` . 

- [324] Jing Yu Koh, Robert Lo, Lawrence Jang, Vikram Duvvur, Ming Lim, Po-Yu Huang, Graham Neubig, Shuyan Zhou, Russ Salakhutdinov, and Daniel Fried. VisualWebArena: Evaluating multimodal agents on realistic visual web tasks. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors, _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 881–905, Bangkok, Thailand, August 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.acl-long.50. URL `https://aclanthology.org/2024.acl-long.50/` . 

138 

- [325] Mohit Shridhar, Jesse Thomason, Daniel Gordon, Yonatan Bisk, Winson Han, Roozbeh Mottaghi, Luke Zettlemoyer, and Dieter Fox. Alfred: A benchmark for interpreting grounded instructions for everyday tasks. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , June 2020. 

- [326] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7(3):7327–7334, 2022. doi: 10.1109/LRA.2022.3180108. 

- [327] Corey Lynch, Ayzaan Wahid, Jonathan Tompson, Tianli Ding, James Betker, Robert Baruch, Travis Armstrong, and Pete Florence. Interactive language: Talking to robots in real time. _IEEE Robotics and Automation Letters_ , pages 1–8, 2023. doi: 10.1109/LRA.2023.3295255. 

- [328] Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen Men, Kejuan Yang, Shudan Zhang, Xiang Deng, Aohan Zeng, Zhengxiao Du, Chenhui Zhang, Sheng Shen, Tianjun Zhang, Yu Su, Huan Sun, Minlie Huang, Yuxiao Dong, and Jie Tang. Agentbench: Evaluating LLMs as agents. In _The Twelfth International Conference on Learning Representations_ , 2024. URL `https://openreview.net/forum?id= zAdUB0aCTQ` . 

- [329] Richard S Sutton. Dyna, an integrated architecture for learning, planning, and reacting. _ACM Sigart Bulletin_ , 2(4):160–163, 1991. 

- [330] Lukasz Kaiser, Mohammad Babaeizadeh, Piotr Milos, Blazej Osinski, Roy H Campbell, Konrad Czechowski, Dumitru Erhan, Chelsea Finn, Piotr Kozakowski, Sergey Levine, et al. Model-based reinforcement learning for atari. _arXiv preprint arXiv:1903.00374_ , 2019. 

- [331] Shruti Sadanand Dongare, Amun Kharel, Jonathan Samuel, and Xiaona Zhou. Transdreamerv3: Implanting transformer in dreamerv3. _arXiv preprint arXiv:2506.17103_ , 2025. 

- [332] David Silver, Thomas Hubert, Julian Schrittwieser, Ioannis Antonoglou, Matthew Lai, Arthur Guez, Marc Lanctot, Laurent Sifre, Dharshan Kumaran, Thore Graepel, et al. A general reinforcement learning algorithm that masters chess, shogi, and go through self-play. _Science_ , 362(6419):1140–1144, 2018. 

- [333] Julian Schrittwieser, Thomas Hubert, Amol Mandhane, Mohammadamin Barekatain, Ioannis Antonoglou, and David Silver. Online and offline reinforcement learning by planning with a learned model. _Advances in Neural Information Processing Systems_ , 34:27580–27591, 2021. 

- [334] Shengjie Wang, Shaohuai Liu, Weirui Ye, Jiacheng You, and Yang Gao. Efficientzero v2: Mastering discrete and continuous control with limited data. _arXiv preprint arXiv:2403.00564_ , 2024. 

- [335] Martin Schmid, Matej Moravčík, Neil Burch, Rudolf Kadlec, Josh Davidson, Kevin Waugh, Nolan Bard, Finbarr Timbers, Marc Lanctot, G Zacharias Holland, et al. Student of games: A unified learning algorithm for both perfect and imperfect information games. _Science Advances_ , 9(46):eadg3256, 2023. 

- [336] Carmelo Sferrazza, Dun-Ming Huang, Xingyu Lin, Youngwoon Lee, and Pieter Abbeel. Humanoidbench: Simulated humanoid benchmark for whole-body locomotion and manipulation. _arXiv preprint arXiv:2403.10506_ , 2024. 

139 

- [337] Jurgis Pasukonis, Timothy Lillicrap, and Danijar Hafner. Evaluating long-term memory in 3d mazes. _arXiv preprint arXiv:2210.13383_ , 2022. 

- [338] Heinrich Küttler, Nantas Nardelli, Alexander Miller, Roberta Raileanu, Marco Selvatici, Edward Grefenstette, and Tim Rocktäschel. The nethack learning environment. _Advances in Neural Information Processing Systems_ , 33:7671–7684, 2020. 

- [339] Akshay Mete, Shahid Aamir Sheikh, Tzu-Hsiang Lin, Dileep Kalathil, and PR Kumar. Optimistic world models: Efficient exploration in model-based deep reinforcement learning. _arXiv preprint arXiv:2602.10044_ , 2026. 

- [340] Kaifeng Bi, Lingxi Xie, Hengheng Zhang, Xin Chen, Xiaotao Gu, and Qi Tian. Accurate medium-range global weather forecasting with 3D neural networks. _Nature_ , 619(7970):533– 538, 2023. 

- [341] Remi Lam, Alvaro Sanchez-Gonzalez, Matthew Willson, Peter Wirber, Meire Fortunato, Ferran Alet, Suman Ravuri, Timo Ewalds, Zach Eaton-Rosen, Weihua Hu, et al. Learning skillful medium-range global weather forecasting. _Science_ , 382(6677):1416–1421, 2023. 

- [342] Ilan Price, Alvaro Sanchez-Gonzalez, Ferran Alet, Tom R Andersson, Andrew El-Kadi, Dominic Masters, Timo Ewalds, Jacklynn Stott, Shakir Mohamed, Peter Battaglia, Remi Lam, and Matthew Willson. Probabilistic weather forecasting with machine learning. _Nature_ , 637 (8044):84–90, 2025. 

- [343] Dmitrii Kochkov, Janni Yuval, Ian Langmore, Peter Norgaard, Jamie Smith, Griffin Mooers, Milan Klöwer, James Lottes, Stephan Rasp, Peter Düben, Sam Hatfield, Peter Battaglia, Alvaro Sanchez-Gonzalez, Matthew Willson, Michael P Brenner, and Stephan Hoyer. Neural general circulation models for weather and climate. _Nature_ , 632(8027):1060–1066, 2024. 

- [344] Tung Nguyen, Johannes Brandstetter, Ashish Kapoor, Jayesh K Gupta, and Aditya Grover. ClimaX: A foundation model for weather and climate. In _International Conference on Machine Learning_ , pages 25904–25938. PMLR, 2023. 

- [345] Cristian Bodnar, Wessel P Bruinsma, Ana Lucic, Megan Stanley, Anna Allen, Johannes Brandstetter, Patrick Garvan, Maik Riechert, Jonathan A Weyn, Haiyu Dong, Jayesh K Gupta, Kit Thambiratnam, Alexander T Archibald, Chun-Chieh Wu, Elizabeth Heider, Max Welling, Richard E Turner, and Paris Perdikaris. A foundation model for the Earth system. _Nature_ , 641(8065):1180–1187, 2025. 

- [346] Ilyes Batatia, Dávid Péter Kovács, Gregor N C Simm, Christoph Ortner, and Gábor Csányi. MACE: Higher order equivariant message passing neural networks for fast and accurate force fields. In _Advances in Neural Information Processing Systems_ , volume 35, pages 11423–11436, 2022. 

- [347] Oliver T Unke, Martin Stöhr, Stefan Ganscha, Thomas Unterthiner, Hartmut Maennel, Sergii Kashubin, Daniel Ahlin, Michael Gastegger, Leonardo Medrano Sandonás, and Joshua T Berryman. Biomolecular dynamics with machine-learned quantum-mechanical force fields trained on diverse chemical fragments. _Science Advances_ , 10:eadn4397, 2024. 

- [348] Frank Noé, Simon Olsson, Jonas Köhler, and Hao Wu. Boltzmann generators: Sampling equilibrium states of many-body systems with deep learning. _Science_ , 365(6457):eaaw1147, 2019. 

140 

- [349] Leon Klein, Andrew Y K Foong, and Frank Noé. Transferable Boltzmann generators. In _Advances in Neural Information Processing Systems_ , volume 37, 2024. 

- [350] Marloes Arts, Victor Garcia Satorras, Chin-Wei Huang, Daniel Zugner, Marco Federici, Cecilia Clementi, Frank Noé, Robert Pinsler, and Rianne van den Berg. Two for one: Diffusion models and force fields for coarse-grained molecular dynamics. _Journal of Chemical Theory and Computation_ , 19(18):6151–6159, 2023. 

- [351] Josh Abramson, Jonas Adler, Jack Dunger, Richard Evans, Tim Green, Alexander Pritzel, Olaf Ronneberger, Lindsay Willmore, Andrew J Ballard, Joshua Bambrick, et al. Accurate structure prediction of biomolecular interactions with AlphaFold 3. _Nature_ , 630:493–500, 2024. 

- [352] Siyu He, Yin Li, Yu Feng, Shirley Ho, Siamak Ravanbakhsh, Wei Chen, and Barnabás Póczos. Learning to predict the cosmological structure formation. _Proceedings of the National Academy of Sciences_ , 116(28):13825–13832, 2019. 

- [353] Yueying Ni, Yin Li, Patrick Lachance, Rupert A C Croft, Tiziana Di Matteo, Simeon Bird, and Yu Feng. AI-assisted superresolution cosmological simulations. _Proceedings of the National Academy of Sciences_ , 118(19):e2022038118, 2021. 

- [354] Francisco Villaescusa-Navarro, Daniel Anglés-Alcázar, Shy Genel, David N Spergel, Rachel S Somerville, Romeel Dave, Annalisa Pillepich, Lars Hernquist, Dylan Nelson, et al. The CAMELS multifield dataset: Learning the universe’s fundamental parameters with artificial intelligence. _The Astrophysical Journal Supplement Series_ , 259(2):61, 2022. 

- [355] Lemuel Puglisi, Daniel C. Alexander, and Daniele Ravì. Brain latent progression: Individualbased spatiotemporal disease progression on 3D brain MRIs via latent diffusion. _Medical Image Analysis_ , 2025. 

- [356] Quy Duc Durrer et al. Treatment-aware diffusion probabilistic model for longitudinal MRI generation and diffuse glioma growth prediction. _Medical Image Analysis_ , 99:103349, 2025. 

- [357] MICCAI Challenge Organizers. Image-based prediction of retinal disease progression: MICCAI challenges, DIAMOND 2024 and MARIO 2024. In _Lecture Notes in Computer Science_ , volume 15431. Springer, 2025. 

- [358] Yukun Zhou, Mark A. Chia, Siegfried K. Wagner, et al. RETFound: A foundation model for generalizable disease detection from retinal images. _Nature_ , 622:156–163, 2023. 

- [359] Yifei Sun, Mariano Cabezas, Jiah Lee, Chenyu Wang, Wei Zhang, Fernando Calamante, and Jinglei Lv. Predicting human brain states with transformer. In _International Conference on Medical Image Computing and Computer-Assisted Intervention_ , pages 136–146. Springer, 2024. 

- [360] Yifei Sun, Daniel Chahine, Qinghao Wen, Tianming Liu, Xiang Li, Yixuan Yuan, Fernando Calamante, and Jinglei Lv. Voxel-level brain states prediction using swin transformer. _IEEE Journal of Biomedical and Health Informatics_ , 29(12):8719–8726, 2025. 

- [361] Cheng Wang, Yu Jiang, Zhihao Peng, Chenxin Li, Changbae Bang, Lin Zhao, Jinglei Lv, Jorge Sepulcre, Carl Yang, Lifang He, et al. Towards a general-purpose foundation model for fmri analysis. _arXiv preprint arXiv:2506.11167_ , 2025. 

141 

- [362] Josue Ortega Caro, Antonio H de O Fonseca, Christopher Averill, Syed A Rizvi, Matteo Rosati, James L Cross, Prateek Mittal, Emanuele Zappala, Daniel Levine, Rahul M Dhodapkar, et al. Brainlm: A foundation model for brain activity recordings. _BioRxiv_ , pages 2023–09, 2023. 

- [363] Stéphane d’Ascoli, Jérémy Rapin, Yohann Benchetrit, Hubert Banville, and Jean-Rémi King. Tribe: Trimodal brain encoder for whole-brain fmri response prediction. _arXiv preprint arXiv:2507.22229_ , 2025. 

- [364] Yuan Gao et al. Surgical vision world model. _arXiv preprint_ , 2025. 

- [365] UniSWM Authors. Unified surgical world model for structured understanding, long-horizon prediction, and fine-grained generation. _ICLR 2026 Submission_ , 2025. 

- [366] Haojun Jiang, Zhenguo Sun, Ning Jia, Meng Li, Yu Sun, Shaqi Luo, Shiji Song, and Gao Huang. Cardiac copilot: Automatic probe guidance for echocardiography with world model. In _Medical Image Computing and Computer Assisted Intervention – MICCAI 2024_ , pages 190–199. Springer, 2024. 

- [367] Yang Yue, Yulin Wang, Haojun Jiang, Pan Liu, Shiji Song, and Gao Huang. EchoWorld: Learning motion-aware world models for echocardiography probe guidance. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 25993–26003, 2025. 

- [368] Qianyi Xu et al. medDreamer: Model-based reinforcement learning with latent imagination on complex EHRs for clinical decision support. _arXiv preprint arXiv:2505.19785_ , 2025. 

- [369] Albert T Corbett and John R Anderson. Knowledge tracing: Modeling the acquisition of procedural knowledge. _User modeling and user-adapted interaction_ , 4(4):253–278, 1994. 

- [370] Frederic M Lord. _Applications of item response theory to practical testing problems_ . Routledge, 2012. 

- [371] Chris Piech, Jonathan Bassen, Jonathan Huang, Surya Ganguli, Mehran Sahami, Leonidas J Guibas, and Jascha Sohl-Dickstein. Deep knowledge tracing. _Advances in neural information processing systems_ , 28, 2015. 

- [372] Jiani Zhang, Xingjian Shi, Irwin King, and Dit-Yan Yeung. Dynamic key-value memory networks for knowledge tracing. In _Proceedings of the 26th international conference on World Wide Web_ , pages 765–774, 2017. 

- [373] Shalini Pandey and George Karypis. A self-attentive model for knowledge tracing. _arXiv preprint arXiv:1907.06837_ , 2019. 

- [374] Youngduck Choi, Youngnam Lee, Junghyun Cho, Jineon Baek, Byungsoo Kim, Yeongmin Cha, Dongmin Shin, Chan Bae, and Jaewe Heo. Towards an appropriate query, key, and value computation for knowledge tracing. In _Proceedings of the seventh ACM conference on learning@ scale_ , pages 341–344, 2020. 

- [375] Aritra Ghosh, Neil Heffernan, and Andrew S Lan. Context-aware attentive knowledge tracing. In _Proceedings of the 26th ACM SIGKDD international conference on knowledge discovery & data mining_ , pages 2330–2339, 2020. 

142 

- [376] Yu Yin, Le Dai, Zhenya Huang, Shuanghong Shen, Fei Wang, Qi Liu, Enhong Chen, and Xin Li. Tracing knowledge instead of patterns: Stable knowledge tracing with diagnostic transformer. In _Proceedings of the ACM web conference 2023_ , pages 855–864, 2023. 

- [377] Fucai Ke, Weiqing Wang, Weicong Tan, Lan Du, Yuan Jin, Yujin Huang, and Hongzhi Yin. Hitskt: A hierarchical transformer model for session-aware knowledge tracing. _KnowledgeBased Systems_ , 284:111300, 2024. 

- [378] Unggi Lee, Jiyeong Bae, Dohee Kim, Sookbun Lee, Jaekwon Park, Taekyung Ahn, Gunho Lee, Damji Stratton, and Hyeoncheol Kim. Language model can do knowledge tracing: Simple but effective method to integrate language model and knowledge tracing task. _arXiv preprint arXiv:2406.02893_ , 2024. 

- [379] Watheq Ahmad Mansour, Salam Albatarni, Sohaila Eltanbouly, and Tamer Elsayed. Can large language models automatically score proficiency of written essays? In _Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024)_ , pages 2777–2786, 2024. 

- [380] Austin Pack, Alex Barrett, and Juan Escalante. Large language models and automated essay scoring of english language learner writing: Insights into validity and reliability. _Computers and Education: Artificial Intelligence_ , 6:100234, 2024. 

- [381] Emrah Emirtekin. Large language model-powered automated assessment: a systematic review. _Applied Sciences_ , 15(10):5683, 2025. 

- [382] Yun Wang, Zhaojun Ding, Xuansheng Wu, Siyue Sun, Ninghao Liu, and Xiaoming Zhai. Autoscore: Enhancing automated scoring with multi-agent large language models via structured component recognition. _arXiv preprint arXiv:2509.21910_ , 2025. 

- [383] Ben Hambly, Ruihai Xu, and Huining Yang. Recent advances in reinforcement learning in finance. _Mathematical Finance_ , 33(3):437–503, 2023. 

- [384] Bryan Lim, Sercan Ö Arık, Nicolas Loeff, and Tomas Pfister. Temporal fusion transformers for interpretable multi-horizon time series forecasting. _International Journal of Forecasting_ , 37(4):1748–1764, 2021. 

- [385] Xiao-Yang Liu, Jingyang Xia, Hongyang Wang, Ziyi Yang, et al. FinRL-Meta: Market environments and benchmarks for data-driven financial reinforcement learning. In _Thirtysixth Conference on Neural Information Processing Systems Datasets and Benchmarks Track_ , 2022. 

- [386] Sergey Levine, Aviral Kumar, George Tucker, and Justin Fu. Offline reinforcement learning: Tutorial, review, and perspectives on open problems. _arXiv preprint arXiv:2005.01643_ , 2020. 

- [387] George Soros. Fallibility, reflexivity, and the human uncertainty principle. _Journal of Economic Methodology_ , 20(4):309–329, 2013. 

- [388] Martin Heusel, Hubert Ramsauer, Thomas Unterthiner, Bernhard Nessler, and Sepp Hochreiter. GANs trained by a two time-scale update rule converge to a local Nash equilibrium. In _Advances in Neural Information Processing Systems_ , volume 30, 2017. 

143 

- [389] Thomas Unterthiner, Sjoerd van Steenkiste, Karol Kurach, Raphael Marinier, Marcin Michalski, and Sylvain Gelly. Towards accurate generative models of video: A new metric & challenges. _arXiv preprint arXiv:1812.01717_ , 2019. 

- [390] Songwei Ge, Seungjun Nah, Guilin Liu, Tyler Poon, Andrew Tao, Bryan Catanzaro, David Jacobs, Jia-Bin Huang, Ming-Yu Liu, and Yogesh Balaji. Content-debiased FVD metric and a new baseline for text-to-video generation. _arXiv preprint arXiv:2404.12391_ , 2024. 

- [391] Zhou Wang, Alan C. Bovik, Hamid R. Sheikh, and Eero P. Simoncelli. Image quality assessment: From error visibility to structural similarity. _IEEE Transactions on Image Processing_ , 13(4):600–612, 2004. 

- [392] Richard Zhang, Phillip Isola, Alexei A. Efros, Eli Shechtman, and Oliver Wang. The unreasonable effectiveness of deep features as a perceptual metric. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 586–595, 2018. 

- [393] Lukasz Kaiser, Mohammad Babaeizadeh, Piotr Milos, Blazej Osinski, Roy H. Campbell, Konrad Czechowski, Dumitru Erhan, Chelsea Finn, Piotr Kozakowski, Sergey Levine, Afroz Mohiuddin, Ryan Sepassi, George Tucker, and Henryk Zoph. Model-based reinforcement learning for Atari. _International Conference on Learning Representations_ , 2020. 

- [394] Rishabh Agarwal, Max Schwarzer, Pablo Samuel Castro, Aaron Courville, and Marc G. Bellemare. Deep reinforcement learning at the edge of the statistical precipice. In _Advances in Neural Information Processing Systems_ , volume 34, 2021. 

- [395] Xiaosong Jia et al. Bench2Drive: Towards multi-ability benchmarking of closed-loop end-toend autonomous driving. In _Advances in Neural Information Processing Systems (Datasets and Benchmarks Track)_ , 2024. 

- [396] Ziqi Huang, Yinan He, Jiashuo Yu, Fan Zhang, Chenyang Si, Yuming Jiang, Yuanhan Zhang, Tianxing Wu, Qingyang Jin, Nattapol Chanber, et al. VBench: Comprehensive benchmark suite for video generative models. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024. 

- [397] Ziqi Huang, Zhuoyi Fan, Tianxing Wu, Yinan He, Yuanhan Zhang, et al. VBench2.0: Advancing video generation benchmark suite for intrinsic faithfulness. _arXiv preprint arXiv:2503.21755_ , 2025. 

- [398] Rishi Upadhyay et al. WorldBench: Disambiguating physics for diagnostic evaluation of world models. _arXiv preprint arXiv:2601.21282_ , 2026. 

- [399] Marc G. Bellemare, Yavar Naddaf, Joel Veness, and Michael Bowling. The Arcade Learning Environment: An evaluation platform for general agents. _Journal of Artificial Intelligence Research_ , 47:253–279, 2013. 

- [400] Yuval Tassa, Yotam Doron, Alistair Muldal, Tom Erez, Yazhe Li, Diego de Las Casas, David Budden, Abbas Abdolmaleki, Josh Merel, Andrew Lefrancq, Timothy Lillicrap, and Martin Riedmiller. DeepMind Control Suite. In _arXiv preprint arXiv:1801.00690_ , 2018. 

- [401] Danijar Hafner. Benchmarking the spectrum of agent capabilities. _International Conference on Learning Representations_ , 2022. 

144 

- [402] Mohammad Reza Samsami, Danijar Hafner, and Robert Dadashi. Mastering memory tasks with world models. In _International Conference on Learning Representations_ , 2024. Oral, top 1.2%. 

- [403] Justin Fu, Aviral Kumar, Ofir Nachum, George Tucker, and Sergey Levine. D4RL: Datasets for deep data-driven reinforcement learning. _arXiv preprint arXiv:2004.07219_ , 2020. 

- [404] Rafael Rafailov, Tianhe Yu, Aravind Rajeswaran, and Chelsea Finn. D5RL: Diverse datasets for data-driven deep reinforcement learning. _Reinforcement Learning Journal_ , 2024. 

- [405] Daniel Dauner, Marcel Hallgarten, Andreas Geiger, and Kashyap Chitta. NAVSIM: Datadriven non-reactive autonomous vehicle simulation and benchmarking. In _Advances in Neural Information Processing Systems (Datasets and Benchmarks Track)_ , 2024. 

- [406] Holger Caesar, Juraj Kabzan, Kok Seang Tan, Whye Kit Fong, Eric Wolber, Alex Lang, Luke Fletcher, Oscar Beijbom, and Sammy Omari. nuPlan: A closed-loop ML-based planning benchmark for autonomous vehicles. _arXiv preprint arXiv:2106.11810_ , 2021. 

- [407] Yaofang Liu, Xiaodong Cun, Xuebo Liu, Xintao Wang, Yong Zhang, Haoxin Chen, Yang Liu, Tieyong Zeng, Raymond Chan, and Ying Shan. Evalcrafter: Benchmarking and evaluating large video generation models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 22139–22149, June 2024. 

- [408] Robin Schiewer, Anand Subramoney, and Laurenz Wiskott. Exploring the limits of hierarchical world models in reinforcement learning. _Scientific Reports_ , 14:26856, 2024. doi: 10.1038/s41598-024-76719-w. arXiv:2406.00483. 

- [409] Kaloyan Savov, Haleh Kazemi, Yiming Zhang, Danda Pani Paudel, and Luc Van Gool Wang. StateSpaceDiffuser: Bringing long context to diffusion world models. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 38, 2025. arXiv:2505.22246. 

- [410] Sungmin Lee, Xinyu Lin, Jiahui Sun, and Minjune Lee. EDELINE: Enhancing memory in diffusion-based world models via linear-time sequence modeling. _arXiv preprint arXiv:2502.00466_ , 2025. 

- [411] Danijar Hafner, Kuang-Huei Lee, Ian Fischer, and Pieter Abbeel. Deep hierarchical planning from pixels. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 35, 2022. arXiv:2206.04114. 

- [412] Christian Gumbsch, Noor Sajid, Georg Martius, and Martin V. Butz. Learning hierarchical world models with adaptive temporal abstractions from discrete latent dynamics. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- [413] Dani Valevski, Yaniv Leviathan, Moab Arar, and Shlomi Fruchter. Diffusion models are realtime game engines. In _International Conference on Learning Representations (ICLR)_ , 2025. arXiv:2408.14837. 

- [414] Simian Luo, Yiqin Tan, Longbo Huang, Jian Li, and Hang Zhao. Latent consistency models: Synthesizing high-resolution images with few-step inference. _arXiv preprint arXiv:2310.04378_ , 2023. 

145 

- [415] Zihan Ding, Mingyu Jin, Siqian Liu, Haiwen Zheng, Aditya Singh, Zhenting Zhang, Haoxuan Kang, Lichen Lin, Hu Liu, and Zhengliang Ding. DOLLAR: Few-step video generation via distillation and latent reward optimization. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2025. arXiv:2412.15689. 

- [416] Josh Tobin, Rachel Fong, Alex Ray, Jonas Schneider, Wojciech Zaremba, and Pieter Abbeel. Domain randomization for transferring deep neural networks from simulation to the real world. In _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 23–30, 2017. arXiv:1703.06907. 

- [417] Xiaoyu Chen, Jiachen Hu, Chi Jin, Lihong Li, and Liwei Wang. Understanding domain randomization for sim-to-real transfer. In _International Conference on Learning Representations (ICLR)_ , 2022. arXiv:2110.03239. 

- [418] Denis Yarats, Ilya Kostrikov, and Rob Fergus. Image augmentation is all you need: Regularizing deep reinforcement learning from pixels. In _International Conference on Learning Representations (ICLR)_ , 2021. arXiv:2004.13649. 

- [419] Adam Levy, Tyler Westenbroek, Yichao Huang, Eduardo Palafox, Shuangyu Yin, Shayegan Omidshafiei, Edward S. Kim, Abhinav Gupta, and David Fridovich-Keil. Simulation distillation: Pretraining world models in simulation for rapid real-world adaptation. _arXiv preprint arXiv:2603.15759_ , 2026. 

- [420] J. B. Lanier, Jinhyun Kim, Shahriar Karamzade, Michael Luo Liu, Shaurya Sinha, Danijar He, Daniele Corsi, and Dieter Fox. Adapting world models with latent-state dynamics residuals. _arXiv preprint arXiv:2504.02252_ , 2025. 

- [421] Jun Yamada, Marc Rigter, Jack Collins, and Ingmar Posner. TWIST: Teacher-student world model distillation for efficient sim-to-real transfer. _arXiv preprint arXiv:2311.03622_ , 2023. 

- [422] Shuangyu Yin, Tyler Westenbroek, Eduardo Palafox, Yilin Ma, Adam Levy, Abhinav Gupta, and David Fridovich-Keil. Rapidly adapting policies to the real world via simulationguided fine-tuning. In _International Conference on Learning Representations (ICLR)_ , 2025. arXiv:2502.02705. 

- [423] Songwei Ge, Aniruddha Mahapatra, Gaurav Parmar, Jun-Yan Zhu, and Jia-Bin Huang. On the content bias in Fréchet video distance. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 7277–7288, 2024. arXiv:2404.12391. 

- [424] Jiahe Liu, Youran Qu, Qi Yan, Xiaoming Zeng, Lili Wang, and Jing Liao. Fréchet video motion distance: A metric for evaluating motion consistency in videos. _arXiv preprint arXiv:2407.16124_ , 2024. 

- [425] Hsiao-Yu Fish Tung, Mingyu Ding, Zhenfang Chen, Sirui Tao, Vedant Lad, Daniel M. Bear, Chuang Gan, Joshua B. Tenenbaum, Daniel L. K. Yamins, Judith E. Fan, and Kevin A. Smith. Physion++: Evaluating physical scene understanding that requires online inference of different physical properties. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 36, 2023. arXiv:2306.15668. 

- [426] Ronan Riochet, Mario Ynocente Castro, Mathieu Bernard, Adam Lerer, Rob Fergus, Véronique Izard, and Emmanuel Dupoux. IntPhys 2019: A benchmark for visual intuitive 

146 

physics understanding. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 44 (9):5016–5025, 2022. doi: 10.1109/TPAMI.2021.3083839. arXiv:1803.07616. 

- [427] Wei Chow, Jianing Mao, Yongkang Li, Daniel Seita, Vitor Guizilini, and Rui Wang. PhysBench: Benchmarking and enhancing vision-language models for physical world understanding. In _International Conference on Learning Representations (ICLR)_ , 2025. arXiv:2501.16411. 

- [428] Fanqing Li, Jiaxin Fang, Kairui Chen, Tong Yang, Yue Cao, Kelvin C. K. Wong, Zhengqin Luo, Zhongying Wang, Xi Yin, Joseph E. Gonzalez, Ion Stoica, Jianfei Han, and Ming Lu. WorldModelBench: Judging video generation models as world models. _arXiv preprint arXiv:2502.20694_ , 2025. 

- [429] Haoyi Duan, Hong-Xing Yu, Sirui Chen, Li Fei-Fei, and Jiajun Wu. WorldScore: A unified evaluation benchmark for world generation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 27713–27724, 2025. arXiv:2504.00983. 

- [430] Zhiqi Li, Zhiding Yu, Shiyi Lan, Jiahan Li, Jan Kautz, Tong Lu, and Jose M. Alvarez. Is ego status all you need for open-loop end-to-end autonomous driving? In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. arXiv:2312.03031. 

147 

