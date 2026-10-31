---
title: "Vision-Language-Action Models for Autonomous Driving: Past, Present, and Future"
date: "2025-12-18"
authors: "Tianshuai Hu; Xiaolu Liu; Song Wang; Yiyao Zhu; Ao Liang; Lingdong Kong"
url: https://arxiv.org/abs/2512.16760
pdf: https://arxiv.org/pdf/2512.16760
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.16760)** / [論文ページ](https://arxiv.org/abs/2512.16760)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。



# **Vision-Language-Action Models for Autonomous Driving: Past, Present, and Future** 

**Tianshuai Hu**<sup>1</sup><sup>_,_</sup> , **Xiaolu Liu**<sup>2</sup><sup>_,_</sup> , **Song Wang**<sup>2</sup><sup>_,_</sup> , **Yiyao Zhu**<sup>1</sup><sup>_,_</sup> , **Ao Liang**<sup>3</sup><sup>_,_</sup> , **Lingdong Kong**<sup>3</sup><sup>_,_</sup> , **Guoyang Zhao**<sup>4</sup> , **Zeying Gong**<sup>4</sup> , **Jun Cen**<sup>5</sup> , **Zhiyu Huang**<sup>6</sup> , **Xiaoshuai Hao**<sup>7</sup> , **Linfeng Li**<sup>3</sup> , **Hang Song**<sup>8</sup> , **Xiangtai Li**<sup>9</sup> , **Jun Ma**<sup>1</sup><sup>_,_4</sup> , **Shaojie Shen**<sup>1</sup> , **Jianke Zhu**<sup>2</sup> , **Dacheng Tao**<sup>9</sup> , **Ziwei Liu**<sup>9</sup><sup>_,_</sup> , **Junwei Liang**<sup>1</sup><sup>_,_4</sup><sup>_,_</sup> 

1HKUST 2Zhejiang University 3National University of Singapore 4HKUST(GZ) 5DAMO Academy, Alibaba 6University of California, Los Angeles 7Xiaomi EV 8Xi’an Jiaotong University 9Nanyang Technological University, Singapore 


WorldBench Team 

###### **Equal Contributions Project Lead Corresponding Authors** 

Autonomous driving has long relied on modular “Perception-Decision-Action” pipelines, where handcrafted interfaces and rule-based components often break down in complex or long-tailed scenarios. Their cascaded design further propagates perception errors, degrading downstream planning and control. **Vision-Action (VA)** models address some limitations by learning direct mappings from visual inputs to actions, but they remain opaque, sensitive to distribution shifts, and lack structured reasoning or instruction-following capabilities. Recent progress in Large Language Models (LLMs) and multimodal learning has motivated the emergence of **Vision-Language-Action (VLA)** frameworks, which integrate perception with language-grounded decision making. By unifying visual understanding, linguistic reasoning, and actionable outputs, VLAs offer a more interpretable, generalizable, and human-aligned paradigm for driving policies. This work provides a structured characterization of the emerging VLA landscape for autonomous driving. We trace the evolution from early VA approaches to modern VLA frameworks and organize existing methods into two principal paradigms: _End-to-End VLA_ , which integrates perception, reasoning, and planning within a single model, and _Dual-System VLA_ , which separates slow deliberation (via VLMs) from fast, safety-critical execution (via planners). Within these paradigms, we further distinguish subclasses such as textual _vs._ numerical action generators and explicit _vs._ implicit guidance mechanisms. We also summarize representative datasets and benchmarks for evaluating VLA-based driving systems and highlight key challenges and open directions, including robustness, interpretability, and instruction fidelity. Overall, this work aims to establish a coherent foundation for advancing human-compatible autonomous driving systems. 


**Project Page:** https://worldbench.github.io/vla4ad 

**GitHub Repo:** https://github.com/worldbench/awesome-vla-for-ad 

**HuggingFace Leaderboard:** https://huggingface.co/spaces/worldbench/vla4ad 

## **1 Introduction** 

The pursuit of fully autonomous driving (AD) has long been a central goal in AI and robotics [37, 72, 122]. Conventional AD systems typically adopt a modular “Perception-Decision-Action” pipeline, where mapping [82, 83], object detection [121, 148, 152, 199], motion prediction [55, 116, 307], and trajectory planning [150, 308] are developed and optimized as separate components. While this design has achieved strong performance in structured environments, its reliance on hand-crafted interfaces and rules limits 

1 


**Figure 1 Outline.** This work aims to provide a structured roadmap of the VLA paradigm for autonomous driving. We begin with **Preliminary Foundations** (Section 2), which formalize the general formulation of VLA models and detail their three core components: the multi-modal input modalities, the VLM backbone, and the action prediction head. It then traces the evolution from **VA Models** (Section 3), which directly map perception to control, towards **VLA Models** (Section 4), which incorporate language-grounded reasoning and interpretable decision-making. We further categorize VLA architectures into two major paradigms – **End-to-End VLA** (Section 4.1) and **Dual-System VLA** (Section 4.2) – that differ in their integration of vision, language, and action modules. Next, we review **Datasets & Benchmarks** (Section 5) that enable both open-loop and closed-loop evaluation of driving intelligence. Finally, we discuss **Challenges & Future Directions** (Section 6), highlighting interpretability, reasoning, and human-AI interaction as central themes driving the next generation of VLA-based autonomous driving research. 

adaptability in complex [84, 85, 220], dynamic [120, 274, 275], and long-tailed scenarios [73, 197, 302]. Moreover, the sequential cascade is prone to cross-stage error propagation, where perception noise is amplified by downstream reasoning and control, compromising stability and safety. 

To mitigate these issues, research has increasingly moved toward end-to-end autonomous driving, where **Vision-Action (VA)** models directly map raw sensory inputs to control commands or trajectory waypoints using imitation [42, 198, 204] and reinforcement learning [67, 150, 281]. Early systems such as ALVINN [203] and ChauffeurNet [9] demonstrated the viability of behavior cloning at scale. Subsequent advances introduced more expressive architectures: TransFuser [39] exploited transformer-based multimodal fusion, UniAD [93] unified perception and planning, VAD [107] leveraged vectorized scene representations, DriveTransformer [104] explored scalable transformer backbones, and DiffusionDrive [155] applied generative modeling to multi-modal trajectory prediction. Collectively, these VA models show that complex driving policies can be learned directly from data, laying the foundation for modern end-to-end AD systems. 

Despite these successes, VA models exhibit fundamental limitations. They largely behave as “black boxes”, offering limited interpretability in safety-critical settings [27, 112, 123, 124, 189, 309]. Their generalization remains fragile under rare or long-tail scenarios that are underrepresented in training [2, 27, 68, 110, 145, 309]. By directly mapping perception to low-level actions, they lack chain-of-thought (CoT) reasoning and contextual 

2 

deliberation [27, 69, 110, 286], limiting their ability to resolve ambiguous or multi-stage interactions. Moreover, their focus on visual inputs prevents them from incorporating high-level plans or human instructions in natural language, leaving a gap in human-vehicle interaction [110, 197, 222, 320]. 

The emergence of Large Language Models (LLMs) and Large Multimodal Models (LMMs) has catalyzed a new paradigm: **Vision-Language-Action (VLA)** models [180, 217, 336]. VLA models couple a Vision-Language Model (VLM) backbone with an action-prediction head, enabling direct mapping from multimodal inputs (vision + language) to executable driving actions. By jointly modeling perception, language understanding, and decision-making, VLA frameworks aspire to provide human-like reasoning, interpretability, and instructionfollowing [66, 71, 340]. Initial explorations such as DriveMLM [46] and GPT-Driver [184] introduced language modules into driving pipelines for high-level decision understanding, paving the way for more integrated designs. Later systems advanced toward closed-loop and reasoning-centric VLA models: LMDrive [222] achieved language-guided closed-loop driving, DriveLM [225] enabled structured reasoning via visual question answering, and DriveGPT4 [287] provided natural-language rationales for decisions. Recent works further investigate tightly coupled reasoning and control, including AutoVLA [340] with fast/slow thinking and GRPO-based optimization [224], and SimLingo [213], which explicitly studies language-action alignment. 

End-to-End VLA models, however, must simultaneously _reason_ and _act_ in real time, creating challenges for latency and safety. This has led to _Dual-System_ VLA designs, where high-level decision making is separated from low-level trajectory execution. DriveVLM [249] generates textual rationales or decisions with a VLM while relying on a classical planner for trajectories. VLP [197] tokenizes waypoints and value maps to produce planning-aware latent actions, and Diff-VLA [106] synthesizes language-guided trajectories refined by rule- or optimization-based controllers. InsightDrive [227] integrates causal language reasoning with MPC, assigning _why_ to the VLM and _how_ to the planner. 

Together, these developments signal a paradigm shift from perception-driven pipelines toward systems that jointly reason, understand, and act. Given the rapid evolution of this field, there is a need to consolidate its conceptual foundations, clarify architectural trends, and provide a structured analysis of emerging directions. 

**Contributions.** This work provides a comprehensive characterization of VLA models for autonomous driving. Specifically: 

- We chart the evolution from precursor VA models (Section 3) to modern VLA frameworks (Section 4), providing historical context and clarifying the motivations behind this paradigm shift. 

- We propose a taxonomy that categorizes VLA architectures into End-to-End (Section 4.1) and DualSystem (Section 4.2) designs, and compare their principles, advantages, and limitations. 

- We present an organized synthesis of datasets and evaluation benchmarks relevant to VLA-based driving (Section 5), facilitating consistent and meaningful comparisons. 

- We identify key challenges in real-world VLA deployment and outline future research directions (Section 6) to guide progress toward safer and more reliable autonomous systems. 

**Scope.** This work differs from prior studies on VLA models [110, 180, 217, 336] through its domain-specific focus, historical framing, and architectural depth.<sup>1</sup> **Domain-specific focus.** Unlike broader analyses that span robotics or embodied AI [179, 223], our work _focuses exclusively on autonomous driving_ , allowing a finegrained analysis of driving-specific challenges, dataset characteristics, and safety requirements.<sup>2</sup> **Historical and conceptual continuity.** We adopt a “Past-Present-Future” narrative that traces the path from early VA models to modern VLA frameworks, emphasizing the motivations and technical lineage underlying the integration of language grounding into perception and control.<sup>3</sup> **Fine-grained architectural taxonomy.** Unlike prior highlevel overviews [44, 110, 301, 338], we propose a hierarchical taxonomy that differentiates End-to-End and Dual-System VLA models and analyzes how they organize perception, reasoning, and control. 

Through this combination of domain specificity, historical depth, and structured architectural analysis, we aim to provide a comprehensive and insightful reference for VLA research in autonomous driving. 

**Organization.** The remainder of this paper is organized as follows. Section 2 introduces the preliminary foundations of VLA frameworks. Section 3 outlines the evolution of VA models. Section 4 presents our 

3 


**Figure 2** Summary of representative **VA** and **VLA** models from existing literature, spanning _End-to-End Models_ , _World Models_ , _Dual-Systems_ , etc. For the complete list of related approaches and the discussions on their specifications, configurations, and technical details, kindly refer to Section 3 and Section 4, respectively. 

taxonomy and analysis of VLA architectures. Section 5 summarizes datasets and benchmarks. Section 6 discusses remaining challenges and future directions. Section 7 concludes this work. 

## **2 Preliminary Foundations** 

Vision-Language-Action (VLA) frameworks [2, 179, 339, 340] leverage large Vision-Language Models (VLMs) [34, 40, 129, 258] to interpret complex driving scenes and produce executable actions. A typical formulation can be expressed as: 


where **x** denotes multimodal inputs at timestamp _t_ , _F_ ( _·_ ) is a VLM backbone parameterized by _θ_ , and _H_ ( _·_ ) is an action-generation head. This section introduces these three components: the input modalities ( **x** ), the VLM backbone ( _F_ ), and the action prediction head ( _H_ ). 

#### **2.1 Input Modalities** 

The input **x** aggregates heterogeneous signals that describe the external environment and the ego-vehicle state [16, 234, 269]. These inputs can be grouped into four categories: sensor observations, latent scene representations, language instructions, and proprioceptive states. 

##### **2.1.1 Sensor Inputs** 

Sensor inputs include raw or preprocessed data directly obtained from vehicle-mounted sensors [23, 24, 140]. 

- **Visual Images.** Surround-view RGB images that offer dense semantic information: **x** img _∈_ R<sup>_Nc×H×W ×_3</sup> , where _Nc_ is the number of cameras ( _e.g._ , 6 to 8), and _H_ , _W_ are the height and width of each image. 

4 

- **LiDAR Point Clouds.** A sparse or dense set of 3D points representing the environment geometry: **x** lidar _∈_ R<sup>_Np×D_</sup> _, D ≥_ 4, where _Np_ is the number of points, and _D_ includes dimensions such as _x, y, z_ , velocity, and intensity. 

##### **2.1.2 Latent Representations** 

Multiple VLA systems operate on intermediate spatial representations that fuse multimodal sensor inputs. 

- **Bird’s-Eye View (BEV) Features.** Top-down view representation, often generated by fusing camera or LiDAR data [148, 154, 167]: **x** bev _∈_ R<sup>_C×H_bev</sup><sup>_×W_bev</sup> , where _C_ is the number of feature channels, and _H_ bev _, W_ bev are the spatial dimensions of the BEV grid. 

- **Occupancy Grids.** 3D volumetric representation predicting occupancy and semantics for each spatial location [166, 260, 267, 284]: **x** occ _∈_ R<sup>_C_occ</sup><sup>_×X×Y ×Z_</sup> , where _X, Y, Z_ are the spatial resolution of the 3D grid, and _C_ occ denotes the number of occupancy feature channels ( _e.g._ , occupancy, flow and semantics). 

##### **2.1.3 Language Inputs** 

To enable VLA capabilities, the model also receives high-level textual instructions or task descriptions [65, 76, 287]. It is composed of a sequence of tokens representing the driving task or goal ( _e.g._ , _“turn left at the next intersection”_ ): **x** lang _∈_ Z<sup>_T_</sup> or **x** lang _∈_ R<sup>_T ×D_emb</sup> , where _T_ is the sequence length, and _D_ emb is the embedding dimension (if token embeddings are used). 

##### **2.1.4 Vehicle State Information** 

There is also proprioceptive information describing the current dynamic state of the ego-vehicle [16, 149]: **x** state _∈_ R<sup>_D_state</sup> , where _D_ state is the dimension of the state vector, including speed, acceleration, steering angle, yaw rate, turn indicator status, etc. 

### **2.2 VLM Backbone (** _F_ **)** 

The VLM backbone _F_ ( _·_ ) is the core reasoning engine of the system. It is typically a large vision language model [5, 8, 34, 159, 258, 343]. Its primary role is to fuse the diverse input modalities into a single, powerful latent representation. It consists of a vision encoder ( _e.g._ , a Vision Transformer, ViT) [210] to process visual inputs and an LLM decoder that conditions its generation on the visual features. A bridge network [34, 159] or unified multimodal token modelling mechanism [5, 258] is used to align the vision features with the language embeddings. VLM can directly generate the actions or provide the guidance for another action expert to develop more robust results. 

##### **2.2.1 VLM for Direct Action Generation (Single-System)** 

In this paradigm, the VLM directly emits actions through its language head [46, 98, 184, 225] or a small attached head [213, 222, 288]. This fully end-to-end design exploits the VLM’s reasoning capabilities to map from visual/language inputs to executable controls. 

##### **2.2.2 VLM for Guidance Generation (Dual-System)** 

Alternatively, the VLM functions as a high-level reasoning module that produces intermediate guidance—textual rationales [80, 207, 249] or structured latent intents [145, 197], which a downstream planner converts into low-level actions [257]. This “slow thinking + fast execution” architecture improves interpretability and enables planners to enforce physical feasibility and safety constraints. 

### **2.3 Action Prediction Head (** _H_ **)** 

The head _H_ ( _·_ ) converts the VLM latent representation into action outputs. Consistent with the taxonomy used in existing literature, we categorize action heads into four types based on their output formulation and generation mechanism: Language Head (LH), Regression (REG), Trajectory Selection (SEL), and Trajectory Generation (GEN). 

5 

- **Language Head (LH).** This design directly utilizes the VLM’s inherent text-generation capabilities to produce actions in the language space. The head is typically the language modeling head of the VLM, trained to output either free-form textual commands ( _e.g._ , _“turn left”_ ) [287] or a sequence of discretized action tokens [340]. The model autoregressively predicts these tokens, which are subsequently parsed into executable signals. This approach is widely adopted in textual action generators like DriveMLM [46] and DriveGPT4 [287]. 

- **Regression (REG).** This formulation employs a decoder structure followed by a regressor (typically a Multi-Layer Perceptron) to directly predict continuous values. Unlike language heads, it avoids discretization by mapping the latent features aggregated via Transformers or GRUs to specific numerical outputs such as steering angles, throttle/brake values, or trajectory waypoints. Representative methods using this deterministic approach include LMDrive [222] and DriveGPT4-V2 [288]. 

- **Trajectory Selection (SEL).** Instead of directly regressing a single path, this head evaluates a set of candidate trajectories and selects the optimal one based on a learned cost function or scoring mechanism. The model typically generates or samples a diverse set of dynamically feasible trajectories and uses the latent representation to predict the cost or probability for each candidate. This approach, utilized by methods like WoTE [144] and SeerDrive [315], ensures that the final output adheres to kinematic constraints by selecting from pre-defined candidates. 

- **Trajectory Generation (GEN).** This generative formulation synthesizes actions through probabilistic modeling, most notably using diffusion models or variational autoencoder [106, 155, 332]. Starting from noise, the head iteratively refines the trajectory sample conditioned on the VLM latent state and optionally language instructions. This allows the model to capture the multi-modality and uncertainty of future distributions. Prominent examples include ORION [66] and DiffVLA [106]. 

#### **2.4 Action in Driving** 

In the context of autonomous driving, particularly for models like VLAs, the action space defines the set of possible outputs the model can generate to control the vehicle. The choice of action representation is a fundamental design decision that dictates how the model’s reasoning is translated into physical motion. We outline three primary paradigms for action space representation below. 

##### **2.4.1 Discrete Trajectory Representations** 

This paradigm represents the vehicle’s intended future path as a finite sequence of spatial waypoints [167]. Each waypoint is a spatial coordinate that the vehicle is expected to reach at a specific future time step. This representation allows for explicit geometric path planning and trajectory optimization. The action, **a** _t_ , formulated at the current time _t_ , is a set of Φ future waypoints: 


Here, Φ is the prediction horizon (the total number of future steps), and each ( _xi, yi_ ) is a coordinate in a 2D Cartesian plane representing the target position at step _i_ . 

##### **2.4.2 Continuous Trajectory Representations** 

Instead of discrete points, this approach parameterizes the vehicle’s motion as a continuous function over a future time horizon [163]. The trajectory is typically defined by functions that govern the vehicle’s longitudinal and lateral motion, such as speed and turning radius. The action, _at_ , is defined by these continuous functions over a time interval [0 _, T_ ]: 


In this formulation, _v_ ( _t_ ) represents the vehicle’s speed profile, and _κ_ ( _t_ ) represents its curvature profile over the future time horizon _T_ . This inherently captures the continuous nature of vehicle dynamics. 

6 

##### **2.4.3 Direct Control Representations** 

This paradigm involves the direct output of low-level vehicle control commands that are immediately sent to the vehicle’s actuators [288]. These outputs typically consist of continuous signals for steering, acceleration, and braking control. The values are often normalized and constrained to lie within the vehicle’s physical operational ranges. The action vector, _at_ , represents control signals for a specific time step _t_ : 


where _δt_ is the steering angle, _τt_ is the throttle input, and _βt_ is the brake input at time step _t_ . Each component is bound by the vehicle’s hardware limits, _e.g._ , _δt ∈_ [ _δ_ min _, δ_ max]. 

##### **2.4.4 Language Representations** 

This paradigm leverages the natural language capabilities of VLMs to express driving actions through textual descriptions [18]. The action is represented as a sequence of discrete tokens from a predefined vocabulary: 


Here, _V_ represents the model’s vocabulary, _T_ is the sequence length, and each token _wi_ corresponds to an element in the vocabulary. The language-based action can range from high-level commands ( _e.g._ , _“turn left at the intersection”_ ) to specific numerical trajectory representations encoded as text tokens. 

## **3 Vision-Action Models** 

Vision-Action (VA) models represent one of the earliest and most influential lines of research in autonomous driving. Their core idea is to directly map sensory observations – typically camera inputs – to driving actions, thereby avoiding explicit modular decomposition into perception, prediction, and planning. Enabled by deep neural networks, VA models have been explored through **two major training paradigms** :<sup>1</sup> _imitation learning_ , which distills policies from expert demonstrations, and<sup>2</sup> _reinforcement learning_ , which optimizes behavior through trial-and-error interaction. More recently, _world models_ have expanded this paradigm by enabling agents to simulate scene dynamics and reason about action consequences, improving robustness and scalability. Table 1 provides an overview of representative efforts. 

From an architectural perspective, VA methodologies for autonomous driving can be broadly grouped into: 

- **End-to-End Models** , which directly predict control commands or planned trajectories from sensory inputs. 

- **World Models** , which explicitly model action-conditioned future dynamics to support policy learning and decision-making. 

#### **3.1 End-to-End Models for Autonomous Driving** 

End-to-end (E2E) models learn a single neural network that maps raw or intermediate sensor observations to actions or planned trajectories [15, 27, 37, 144]. Unlike modular stacks, which isolate perception, prediction, and planning, E2E approaches implicitly couple these tasks within a unified representation [91, 108, 236]. Depending on whether perception supervision is employed, existing methods fall into two main categories: _action-only models_ and _perception-action models_ , as illustrated in Figure 3. 

##### **3.1.1 Action-Only Model** 

Action-only models adopt a streamlined one-stage formulation: sensory inputs are fed directly into a network that outputs low-level actions. These methods primarily differ in whether policies are learned from **demonstrations** or through **exploration** . 

**Imitation Learning (IL)** , especially behavior cloning [6], learns a policy by matching expert actions, as visualized in the IL branch of Figure 3. Early works [15, 42, 198, 203] demonstrated that actions can be predicted directly from monocular or multi-view inputs, and subsequent designs refined backbone architectures [23, 39, 206]. 

7 

NEAT [38] highlights behaviorally relevant image regions via intermediate attention maps, while TCP [272] fuses a trajectory branch and control branch for complementary supervision. To better leverage scene geometry, BEV-Planner [149] predicts trajectories from BEV features enriched with ego states. Urban-Driver [218] moves beyond open-loop evaluation by training policies in a differentiable, datadriven simulator. 

IL-based methods are simple, efficient, and require no reward engineering; however, they remain sensitive to distribution shift [56, 205, 215] and causal confusion [49, 190, 200], which can impair reliability in long-tailed or rare-event scenarios. 

**Reinforcement Learning (RL)** optimizes actions through interaction, offering greater flexibility than imitation-based approaches [118, 237]. Several works address the sample inefficiency of RL by combining it with supervised pretraining: Latent-DRL [251] and Gri [22] pre-train visual encoders using semantic segmentation, while LSD [194] initializes policies via IL before performing RL fine-tuning. Privileged-information distillation has also proven effective: LBC [24], WoR [25], and Roach [326] use simulator-only states to guide sensor-based agents. 

Combined with the world model, Think2Drive [136] trains the agent with the Model-Based RL (MBRL) method, paired with a compact latent world model learning the transitions of the environment. Raw2Drive [300] is a dual-stream MBRL approach, where the raw sensor world model is aligned with the privileged world model for camerabased action prediction. In contrast to studies in non-photorealistic CARLA [56], recent efforts have 

**Table 1** Summary of **Vision-Action** models in autonomous driving. _•_ **Inputs** : Camera, : LiDAR, and : Ego-Status. 

- **Action Types** : <u>RL:</u> Policy w/ Reinforcement Learning, <u>REG:</u> Decoder + 

- MLP, <u>SEL:</u> Traj. Selection w/ Cost, and <u>GEN:</u> Traj. Generation w/ Generative Model. 

- **Outputs** : <u>Ctrl.:</u> Control Signal, Traj.: Numerical Trajectory. 

|_•_ **Datasets:**<br>**C**<br>CARL|A [56],<br>**N**|NoCr|ash [43],|**P**<br>ProcGen [|41],<br>**L**|Lyft [89],|
|---|---|---|---|---|---|---|
|**N**<br>nuScenes[16]<br>**B**<br>B|ench2D|rive[10|3]<br>**N**<br>N|AVSIM[47]|||
|,<br><br><br>**O**<br>OpenOcc [250],<br>**O**|OpenD|<br>V [296],|,<br><br><br>**N**<br>nuP|,<br>lan [17],<br>**O**<br>O|cc3D|[248],|
|**C**<br>Cam4DOcc [177],|and<br>**P**<br>|Private|Data.||||
|**#**<br>**Model**|**Venue**|**Input**|**Dataset**|**Vision**|**Action**|**Output**|
|_•_ **Sec. 3.1.1 Action-only Models**|||||||
|<br>1<br>LBC [24]|CoRL’20||**C**<br>**N**|ResNet [87]|RL|Ctrl.+Traj.|
|2<br>Latent-DRL [251]|CVPR’20||**C**|ResNet [87]|RL|Ctrl.|
|3<br>NEAT [38]<br><br>|ICCV’21||**C**|ResNet [87]<br>|REG<br>|Traj.<br>|
|4<br>Roach [326]|ICCV’21||**C**<br>**N**|ResNet [87]|RL|Ctrl.|
|5<br>WoR [25]|ICCV’21||**C**<br>**N**<br>**P**|ResNet [87]|REG|Ctrl.|
|6<br>TCP [272]<br><br>|NeurIPS’22||**C**|ResNet [87]<br>|REG<br>|Ctrl.+Traj.<br>|
|7<br>Urban-Driver [218]<br>8<br>LAV[23]|CoRL’22<br>CVPR’22||**L**<br>**C**|ResNet [87]<br>ResNet[87]|REG<br>REG|Traj.<br>Ctrl.+Traj.|
|<br>9<br>TransFuser [39]|TPAMI’23||**C**|<br>ResNet [87]|REG|Traj.|
|10<br>GRI [22]|Robotics’23||**C**|EfficientNet [238]|RL|Ctrl.|
|11<br>BEVPlanner [149]<br><br>|CVPR’24||**N**|ResNet [87]<br>|REG<br>|Traj.<br>|
|12<br>Raw2Drive [300]|NeurIPS’25||**C**<br>**B**|ResNet [87]|RL|Ctrl.|
|13<br>RAD [67]|NeurIPS’25||**P**|ResNet [87]|RL|Traj.|
|14<br>TrajDiff [75]|arXiv’25||**N**|ResNet [87]|GEN|Traj.|
|_•_ **Sec. 3.1.2 Perception-Action**|**Models**|||fi|||
|15<br>ST-P3 [91]|ECCV’22||**N**<br>**C**|EfficientNet [238]|SEL|Traj.|
|16<br>UniAD[93]|CVPR’23||**N**|ResNet[87]|REG|Traj|
|<br>17<br>VAD [107]|ICCV’23||**N**|<br>ResNet [87]|REG|.<br>Traj.|
|18<br>OccNet [250]<br>19<br>GAD332|ICCV’23<br>’||**N**<br>**O**<br>|ResNet [87]<br>RNt87|SEL<br>GEN|Traj.<br>T|
|en []<br><br>|ECCV24||**N**|ese []<br>||raj.<br>|
|20<br>PARA-Drive [268]|CVPR’24||**N**|ResNet [87]|REG|Traj.|
|21<br>Hydra-MDP [147]<br><br>|CVPRW’24<br>||**N**<br>|ResNet [87]<br>|SEL<br>|Traj.<br>|
|22<br>SparseAD [317]<br>|arXiv’24||**N**|ResNet [87]<br>|REG|Traj.|
|23<br>GaussianAD [333]|arXiv’24||**N**|ResNet [87]|REG|Traj.|
|24<br>DiFSD [231]<br><br>|arXiv’24||**N**|ResNet [87]<br>|GEN<br>|Traj.<br>|
|25<br>DriveTransformer [104]|ICLR’25||**N**<br>**B**|ResNet [87]|REG|Traj.|
|26<br>SparseDrive [236]|ICRA’25||**N**|ResNet [87]|REG|Traj.|
|27<br>DiffusionDrive [155]<br><br>|CVPR’25||**N**<br>**N**|ResNet [87]<br>|GEN<br>|Traj.<br>|
|28<br>GoalFlow [279]|CVPR’25||**N**|VoVNet [128]|GEN|Traj.|
|29<br>GuideFlow [161]<br><br>|arXiv’25<br>||**N**<br>**N**<br>**B**<br>|ResNet [87]<br>|GEN<br>|Traj.<br>|
|30<br>ETA [78]<br>31<br>Geo [105]|arXiv’25<br>arXiv’25||**B**<br>**N**|CLIP-ViT [210]<br>ResNet [87]|REG<br>REG|Traj.<br>Traj.|
|32<br>DiffusionDriveV2[345]|Xi’25||**N**|ResNet[87]|GEN|Traj|
|f <br>33<br>NaviHydra [271]|arv<br>arXiv’25||**N**|<br>ResNet [87]|SEL|.<br>Traj.|
|34<br>Mimir [280]|arXiv’25||**N**|ResNet [87]|GEN|Traj.|
|_•_ **Sec. 3.2.1 Image-Based World**|**Models**||||||
|<br>35<br>DrieDreamer[264]|<br>ECCV’24||**N**|SD[214]|REG|Traj|
|v <br>36<br>GenAD [296]|CVPR’24||**O**|<br>SDXL [202]|REG|.<br>Traj.|
|37<br>Drive-WM [266]<br><br>|CVPR’24<br>||**N**<br>|ConvNeXt [172]<br>|SEL<br>|Traj.<br>|
|38<br>DrivingWorld [92]<br>|arXiv’24||**N**|VQ-VAE [254]<br>|REG|Traj.|
|39<br>Imagine-2-Drive [70]|IROS’25||**C**|SVD [13]|SEL|Traj.|
|40<br>DrivingGPT [33]<br><br>|ICCV’25||**N**<br>**N**|VQ-VAE [254]<br>|REG<br>|Traj.<br>|
|41<br>Epona [321]|ICCV’25||**N**<br>**N**<br>**N**|DC-AE [26]|REG|Traj.|
|42<br>VaViM [10]|arXiv’25||**O**<br>**N**<br>**N**|LLaMAGen [235]|GEN|Traj.|
|_•_ **Sec. 3.2.2 Occupancy-Based**|**World Model**|**s**|||||
|<br>43<br>OccWorld [331]<br>|<br>ECCV’24||**N**<br>**O**|ResNet [87]<br>|REG|Traj.|
|44<br>NeMo [96]|ECCV’24||**N**|ResNet [87]|REG|Traj.|
|45<br>OccVAR [111]<br><br>|-<br>||**N**<br>**O**<br><br>|ResNet [87]<br>|REG<br>|Traj.<br>|
|46<br>RenderWorld [292]<br>47<br>DFIT-OccWorld [318]|arXiv’24<br>arXiv’24||**N**<br>**O**<br>**N**<br>**O**|Swin-T [171]<br>ResNet [87]|REG<br>REG|Traj.<br>Traj.|
|48<br>Drive-OccWorld[297]|AAAI’25||**N**<br>**C**|ResNet[87]|REG|Traj|
|<br>49<br>T<sup>3</sup>Former [282]|arXiv’25||**N**<br>**O**|<br>ResNet [87]|REG|.<br>Traj.|
|50<br>AD-R1 [289]|arXiv’25||**N**<br>**N**|-|RL|Traj.|
|_•_ **Sec. 3.2.3 Latent-Based Worl**|**d Models**||||||
|<br>51<br>Covariate-Shift [204]<br>|<br>arXiv’24||**C**|DINOv2 [196]<br>|REG|Traj.|
|52<br>World4Drive [335]<br>53<br>WoTE[144]|ICCV’25<br>ICCV’25||**N**<br>**N**<br>**N**<br>**B**|ResNet [87]<br>ResNet[87]|REG<br>SEL|Traj.<br>Traj|
|<br>54<br>LAW [142]|ICLR’25||**N**<br>**N**<br>**C**|<br>Swin-T [171]|REG|.<br>Traj.|
|55<br>SSR [133]<br>56<br>EhPli233|ICLR’25<br>’||**N**<br>**C**<br>|ResNet [87]<br>RNt87|REG<br>REG|Traj.<br>T|
|co-annng []<br><br>|arXiv25||**N**|ese []<br>||raj.<br>|
|57<br>SeerDrive [315]|NeurIPS’25||**N**<br>**N**|VoVNet [128]|SEL|Traj.|


shifted toward photorealistic world modeling. RAD [67] establishes a 3DGS-based [115] closed-loop RL training paradigm regulated by IL in a realistic 3DGS environment. The key challenges in RL-based models include sample inefficiency [150], reward function design [119], and sim-to-real transfer [37]. 

8 

##### **3.1.2 Perception-Action Model** 

Perception-action models follow a two-stage paradigm in which perception tasks ( _e.g._ , mapping, tracking) supervise and constrain trajectory prediction. These methods generally adopt either dense BEV-based representations or sparse query-based representations, as shown in Figure 3. 

**Dense BEV-Based Models** construct uni- 

fied top-down features from multi-view cameras. ST-P3 [91] jointly learns spatial-temporal features for perception and planning; UniAD [93] integrates sequential task dependencies to support goal-directed planning. VAD [107] employs a vectorized scene representation to improve both planning safety and efficiency. OccNet [250] incorporates occupancy embeddings to capture 3D scene geometry. Para-Drive [268] proposes a fully parallel E2E architecture for real-time deployment. 

Generative and sampling-based approaches have recently emerged: GenAD [332] frames planning as sampling from learned distributions; DiffusionDrive [155] introduces a truncated diffusion policy guided by multi-modal anchors; GuideFlow [161] incorporates explicit 


**Figure 3** The categorization of **End-to-End VA models** based on model structures and outputs, including _Action-Only Models_ (Sec. 3.1.1), and _Perception-Action Models_ (Sec. 3.1.2). 

physical constraints into the generation process. While BEV representations naturally align with 2D trajectory planning, they require substantial computation due to their dense spatial structure. 

**Sparse Query-Based Models** avoid explicit BEV grids by using latent queries to aggregate image features. SparseAD [317] and SparseDrive [236] represent the entire scene using sparse perception queries and a parallel planner, achieving strong efficiency-accuracy trade-offs. DiFSD [231] introduces an ego-centric sparse formulation and models uncertainty through trajectory denoising. DriveTransformer [104] incorporates task parallelism, sparse attention, and streaming updates for improved stability. GaussianAD [333] adopts 3D semantic Gaussians for fine-grained yet compact scene representation. 

Sparse query methods significantly reduce inference latency, but the absence of a dense future-world representation can restrict long-horizon reasoning and planning safety. 

#### **3.2 World Models for Autonomous Driving** 

World models aim to predict how driving scenes evolve under different ego actions [77, 125, 291]. By jointly modeling scene dynamics and ego motion, they provide a powerful mechanism for learning safe, long-horizon driving policies [53]. Their applications span immersive simulation [12, 90, 174, 212, 290, 342], end-to-end planning [68, 92, 264, 266], and feature learning for downstream tasks [28, 29, 137, 169, 188, 298, 319]. Here, we focus on world models designed for trajectory planning and categorize them by prediction modality and representation granularity into three groups: **image-based** , **occupancy-based** , and **latent-based** models (Figure 4). 

##### **3.2.1 Image-Based World Model** 

Image-based world models generate future frames conditioned on ego actions, enabling agents to “dream” scene evolution and evaluate the consequences of different trajectories. These methods leverage modern generative models to synthesize realistic, temporally coherent videos and are typically classified into diffusion-based and autoregressive architectures. 

9 

**Diffusion-Based World Models** use latent video diffusion [14, 214] to produce multi-step rollouts. For front-view forecasting, GenAD [296] and Vista [68] incorporate temporal reasoning modules to handle complex motion patterns. Imagine-2-Drive [70] integrates diffusion generation into a reinforcement-learning framework, training a policy actor inside the world model. To support multi-view predictions, DriveDreamer [264] employs a twostage pipeline for video synthesis and policy learning. Drive-WM [266] factors views within a spatiotemporal model and generates multiple plausible futures, selecting trajectories using image-based rewards. 

**Autoregressive (AR) Models** tokenize images using VQ-VAE [254] and model scene evolution via next-token prediction [58, 127, 305]. DrivingWorld [92] builds a GPT-style architecture for highfidelity long-horizon video generation. DrivingGPT [33] interleaves image and action tokens, unifying simulation and trajectory planning. Epona [321] combines AR modeling with diffusion to produce high-resolution, long-duration rollouts. 

Image-based world models provide photorealistic simulations crucial for training and evaluation. However, their reliance on 2D appearance limits explicit 3D reasoning, which can hinder safetycritical long-horizon planning. 

##### **3.2.2 Occupancy-Based World Models** 

Occupancy-based world models represent the driving scene as spatiotemporal occupancy grids and predict their evolution under different actions. Instead 


**Figure 4** The categorization of **World Models** based on prediction modalities, including _Image-Based Models_ (Sec. 3.2.1), _Occupancy-Based Models_ (Sec. 3.2.2), and _Latent-Based Models_ (Sec. 3.2.3). 

of synthesizing raw pixels, these models focus on the geometry and semantics of free space, obstacles, and agents [153, 170, 342]. As shown in the middle of Figure 4, AR prediction is commonly used in occupancy world models. 

OccWorld [331] first introduces occupancy forecasting for planning, using a scene tokenizer to discretize 3D occupancy before applying a GPT-style transformer to synthesize future scenes and ego trajectories. RenderWorld [292] produces 3D occupancy through a self-supervised Gaussian module, while OccVAR [111] performs coarse-to-fine 4D occupancy forecasting. T<sup>3</sup> Former [282] encodes occupancy using compact triplanes and predicts future triplane updates from multi-scale history. 

An alternative line employs single-stage feedforward prediction. Drive-OccWorld [297] uses predicted future BEV features for action-conditioned 3D forecasting. DFIT-OccWorld [318] introduces a decoupled dynamic flow strategy to support efficient non-autoregressive prediction. NeMo [96] improves vision-based occupancy forecasting by combining it with self-supervised image reconstruction signals. 

Occupancy-based models offer strong geometric fidelity and explicit free-space reasoning but rely on costly 3D annotations, which can limit scalability across diverse environments. 

##### **3.2.3 Latent-Based World Models** 

Latent-based world models bypass explicit image or occupancy forecasting and instead predict future dynamics directly in a compressed latent space. By operating on high-level features, these models capture behavioral patterns and long-horizon dependencies while avoiding the computational overhead of pixel-level generation. Regarding the forecasting strategy, the latent world model utilizes single-frame or AR prediction presented at the bottom of Figure 4. 

10 

**Table 2** Categories of **natural language prompts** for Vision-Language-Action (VLA) models in autonomous driving. 

|**Prompt Type**|**Explanations**|
|---|---|
|**System Prompt**|Text templates or query formulations designed to interact with LLMs,<br>guiding them to perform specific driving-related reasoning or trajectory<br>prediction tasks.<br>System prompts often define the task structure,<br>provide role definitions, and shape the model’s reasoning behavior.|
|**Instructions**|Commands or instructions provided by humans or systems, typically<br>describing the driving goal or required maneuver (_e.g._, “turn left at<br>the next intersection”).|
|**Scene Description**|Textual descriptions of surroundings, including perceived objects, road<br>layout, and contextual factors (_e.g._, _“a pedestrian is crossing on the_<br>_right”_, or _“a vehicle is 5 meters ahead on the left”_).|
|**Traffic Rules**|Prompts encoding regulatory constraints or domain knowledge, such as<br>traffic laws, traffic light status, right-of-way rules, or safety guidelines.|
|**Ego Status**|Information about the ego vehicle’s internal state, including speed,<br>position, heading, or navigation intent.|
|**Context Information**|Demonstrations presented as paired examples of driving scenarios and<br>corresponding actions, used to guide the model via in-context learning.|


Early latent models [7, 337] learn feature-level dynamics for planning without generating visual frames. LAW [142] leverages self-supervised learning to predict future scene features from current features and planned ego trajectories, enabling end-to-end driving without perception labels. World4Drive [335] employs vision foundation models to create latent representations from which diverse planning trajectories can be generated and evaluated. Echo-Planning [233] introduces a bidirectional Current→Future→Current (CFC) cycle to enforce temporal consistency in latent BEV features. For robustness in imitation learning, Covariate-Shift [204] addresses distribution mismatch using latent rollouts. By injecting predicted BEV features, SeerDrive [315] refines both latent prediction and trajectory generation in a closed-loop manner. 

Latent world models offer efficient and semantically informed forecasting. However, achieving high-quality planning still requires auxiliary supervision from 2D/3D annotations, such as bounding boxes or HD maps. 

#### **3.3 Limitations of VA Compared to VLA** 

While VA models remain widely deployed, they face structural limitations that hinder performance in complex, ambiguous, or long-tailed scenarios: areas where VLA models excel. 

- **Limited Interpretability.** VA models provide little insight into their decision-making process. In contrast, VLA models can articulate reasoning steps or explanations through language. 

- **Weak Generalization.** VA policies lack broad world knowledge and often require environment-specific retraining. VLA models leverage large-scale pretraining to generalize better under distribution shifts and long-tailed events. 

- **No Chain-of-Thought Reasoning.** VA models directly map pixels to actions, making it difficult to perform explicit reasoning or contextual analysis. VLAs natively support step-wise reasoning. 

- **No Language Understanding.** VA systems cannot incorporate human instructions or high-level goals expressed in texts. VLA models naturally integrate such inputs to guide planning and decision-making. 

## **4 Vision-Language-Action Models** 

VLA models extend the Vision-Action paradigm by coupling visual perception with the multimodal reasoning capabilities of large vision-language models. Equipped with chain-of-thought style inference and broad world knowledge, these models are particularly promising for rare, ambiguous, and long-tailed driving scenarios. Table 2 summarizes typical prompting strategies, and Table 3 overviews representative VLA-based approaches. 

11 

**Table 3** Summary of **Vision-Language-Action** models in autonomous driving. _•_ **Input** : :Camera, : Sys. Prompt, : Instruct., : Scene Descrip., : Status, : Traffic Rule, : Context Info. _•_ **Action** : <u>LH:</u> Lang. Head, <u>REG:</u> Decoder+MLP, <u>GEN:</u> Traj. GEN with Generative Model. _•_ **Output** : <u>Desc.:</u> Linguistic Descriptions, Traj.: Numerical Trajectory, <u>Ctrl.:</u> Control Signal. <u>Meta.:</u> Meta Action. _•_ **Datasets:** **<mark>N</mark>** <u>:</u> nuScenes [16], **<mark>B</mark>** <u>:</u> BDD-X [117], **<mark>D</mark>** <u>:</u> DriveLM [225], **S** <u>:</u> SDN [183], **<mark>V</mark>** <u>:</u> VLAAD [201], **<mark>B</mark>** <u>:</u> Bench2Drive [103], **<mark>W</mark>** : Waymo [59], **<mark>M</mark>** : MetaAD [109], **C** : Carla [56], **<mark>I</mark>** : ImpromptuVLA [35], **<mark>N</mark>** : NAVSIM [47], **O** : OpenDV [296], **<mark>N</mark>** : nuPlan [17], **<mark>T</mark>** : Talk2Car [50], **C** : CoVLA [2], **<mark>P</mark>** : PhysicalAI-AV [193] and **<mark>P</mark>** : Private Data. 

|**#**<br>**Model**<br>|**Venue**<br>|**Input Modality**|**Dataset**|**Vision**|**Language**|**Action**|**Output**|
|---|---|---|---|---|---|---|---|
|_•_ **Sec. 4.1.1: Textural Action Gen**<br>1<br>DriveMLM [46]|**erator**<br>arXiv’23||**C**|EVA-CLIP [61]|LLaMA [252]|LH|Desc.+Meta.|
|2<br>RAG-Driver [309]|RSS’24||**B**|CLIP [210]|Vicuna-1.5 [36]|LH|Desc.+Ctrl.|
|3<br>RDA-Driver [97]<br>4<br>DLM|ECCV’24<br>’||**D**<br>**N**<br>|BEVFusion [154]<br>BLIP|LLaMA [252]<br>LLMA|LH<br>LH|Desc.+Traj.<br>MT|
|rive [225]<br>5<br>DriveGPT4 [287]<br>|ECCV24<br>RA-L’24||**D**<br>**B**|-2 [132]<br>CLIP [210]<br>|a [252]<br>LLaMA-2 [252]<br>|LH|eta.+raj.<br>Desc.+Ctrl.<br>|
|6<br>DriVLMe [95]<br>7<br>LLaDA [130]<br>8<br>VLAAD[201]|IROS’24<br>CVPR’24<br>WACVW’24||**B**<br>**S**<br>**C**<br>**N**<br>**N**<br>**V**|CLIP [210]<br>-<br>BLIP-2[132]|Vicuna [36]<br>GPT-4 [1]<br>LLaMA-2[252]|LH<br>LH<br>LH|Desc.+Ctrl.<br>Ctrl.+Traj.<br>Ctrl|
|<br>9<br>OccLLaMA[267]|Xi’24||**N**|<br>Sin-T[171]PointPillar[126]|<br>LLaMA-3[74]|LH|.<br>Ctrl+Traj|
|<br>10<br>Doe-1 [334]<br><br>|arv<br>arXiv’24||**N**|w ,  <br>Lumina-mGPT [157]<br>|<br>BPE tokenizer [241]<br>|LH<br>|..<br>Ctrl.+Traj.<br>|
|11<br>LINGO-2 [245]|-||**P**|Wayve Vision Model [246]|Wayve VLA Model [246]|LH|Desc.+Traj.|
|12<br>SafeAuto [320]|ICML’25||**B**<br>**D**|LanguageBind [341]|Video-LLaVA [156]|LH|Desc.+Ctrl.|
|13<br>OpenEMMA [278]<br>14<br>ReasonPlan[168]|WACV’25<br>CRL’25||**N**<br>**B**|Qwen2-VL [258]<br>SiLIP[314]|Qwen2-VL [258]<br>Qwen[4]|LH<br>LH|Desc.+Traj.<br>Desc+Traj+Meta|
|<br>15<br>FutureSightDrive [312]<br>16<br>ImpromptuVLA [35]<br>|o<br>NeurIPS’25<br>NeurIPS’25||**N**<br>**D**<br>**I**|g <br>ViT [57]<br>Qwen2.5-VL [5]<br>|<br>Qwen2-VL [258]<br>Qwen2.5-VL [5]<br>|LH<br>LH|...<br>Desc.+Traj.<br>Traj.|
|17<br>WKER [313]|AAAI’25||**N**|EVA-02 [62]|LLaMA3 [74]|LH|Desc.+Traj.|
|18<br>OmniDrive [259]<br>19<br>S4-Driver[276]|CVPR’25<br>CVPR’25||**N**<br>**D**<br>**W**<br>**N**|EVA-02 [62]<br>PaLI3[31]|LLaMA2 [252]<br>PaLI3[31]|LH<br>LH|Desc.+Traj<br>Meta+Traj|
|<br>20<br>EMMA [98]<br><br>|TMLR’25<br>||**W**<br>**N**<br>|<br>Gemini-VLM [243]|<br>Gemini [242]<br>|LH<br>|..<br>Desc.+Traj.<br>|
|21<br>Occ-LLM [284]<br><br>|ICRA’25||**N**|-<br>|LLaMA2 [252]<br>|LH<br>|Traj.<br>|
|22<br>Sce2DriveX [327]|RA-L’25||**N**<br>**B**|OpenCLIP [99]|Vicuna-1.5 [36]|LH|Ctrl.+Traj.|
|23<br>DriveAgent-R1 [330]<br>24<br>Drive-R1 [146]|arXiv’25<br>arXiv’25||**N**<br>**P**<br>**N**<br>**D**|Qwen2.5-VL [5]<br>InternVL2 [263]|Qwen2.5-VL [5]<br>InternVL2 [263]|LH<br>LH|Desc.+Meta.<br>Desc.+Traj.+Meta.|
|25<br>FastDriveVLA[18]|arXiv’25||**N**|Qwen25-VL[5]|Qwen25-VL[5]|LH|Desc+Traj|
|<br>26<br>WiAD323|’|||. <br>CLIP210|. <br>MbilVLM40|LH|..<br>TCl|
|se []<br><br>²|arXiv25||**B**<br>**C**<br>**D**|[]<br>|oe []<br>||raj.+tr.<br>|
|27<br>AutoDrive-R [310]<br>|arXiv’25||**N**<br>**W**|Qwen2.5-VL [5]<br>|Qwen2.5-VL [5]<br>|LH|Traj.|
|28<br>OmniReason [165]<br>29<br>OpenREAD [324]|arXiv’25<br>arXiv’25||**N**<br>**B**<br>**N**|EVA-02 [62]<br>Qwen3 [293]|LLaVA-1.5 [160]<br>Qwen3 [293]|LH<br>LH|Meta.+Traj.<br>Desc.+Meta.+Traj.|
|30<br>dVLM-AD[178]|arxiv’25||**W**<br>**N**|SigLIP2[253]|LLaDA-V[303]|LH|Desc+Traj|
|<br>31<br>PLA325|’|||<br>SEd|<br>GPT411|LH|..<br>DT|
|[]<br><br>|arXiv25<br>||**N**|ensor ncoer<br>|-. []<br>||esc.+raj.<br>|
|32<br>AlphaDrive [109]<br>33<br>CoReVLA [60]|arXiv’25<br>arXiv’25||**M**<br>**B**|Qwen2-VL [258]<br>Qwen2.5-VL [5]|Qwen2-VL [258]<br>Qwen2.5-VL [5]|LH<br>LH|Desc.+Meta.<br>Ctrl.+Traj.|
|_•_ **Sec. 4.1.2: Numerical Action G**<br>34<br>LMDrive [222]|**enerator**<br>CVPR’24||**C**|ResNet [87]|LLaMA [252] Vicuna [36]|REG|Ctrl.|
|35<br>BEVDriver [270]<br>36<br>CoVLA-Agent [2]|IROS’25<br>WACV’25||**C**<br>**C**|InterFuser [221]<br>CLIP [210]|LLaMA-3.1 [74]<br>LLaMA2 [252]|REG<br>REG|Ctrl.+Traj.<br>Desc.+Traj.|
|37<br>ORION[66]|ICCV’25||**N**<br>**B**|EVA-02[62]|Vicuna-15[36]|GEN|Desc+Traj|
|<br>38<br>SimLingo [213]<br>39<br>DriveGPT4-V2 [288]<br><br>|CVPR’25<br>CVPR’25||**C**<br>**B**<br>**C**|<br>InternViT [34]<br>CLIP [210] SigLIP [314]<br>|. <br>Qwen2 [258]<br>Qwen [4] Tinyllama [322]<br>|REG<br>REG<br>|..<br>Ctrl.+Traj.<br>Ctrl.+Traj.<br>|
|40<br>AutoVLA [340]|NeurIPS’25||**N**<br>**B**<br>**N**<br>**W**|Qwen2.5-VL [5]|Qwen2.5-VL [5]|LH|Traj.|
|41<br>DriveMoE [299]|arXiv’25||**B**|PaliGemma [11]|PaliGemma [11]|GEN|Ctrl.|
|42<br>DSDrive [167]|arXiv’25||**C**|ResNet [87]|LLaMA [252]|REG|Desc.+Traj.|
|43<br>OccVLA[166]|rXi’25||**N**|VQ-VAE[254]|PaliGemma-2[230]|REG|Traj|
|<br>44<br>D|av<br>’|||<br>LC|<br>IL4|GEN|.<br>DT|
|VRive [76]<br>45<br>ReflectDrive [135]|arXiv25<br>arXiv’25||**N**<br>**B**<br>**N**|Qwen2.5-V [5], VQ [329]<br>LLaDA-V [303]|nternV3 [33]<br>LLaDA-V [303]|GEN|esc.+raj.<br>Traj.|
|46<br>E3AD [240]<br>47<br>LCDrive [239]|arXiv’25<br>arXiv’25||**T**<br>**P**|Qwen2.5-VL [5]<br>DINOv2 [196]|Qwen2.5-VL [5]<br>Qwen3 [293]|REG<br>LH|Traj.<br>Traj.|
|48<br>Alpamayo-R1 [265]<br><br>|arXiv’25<br>’||**P**<br><br><br>|Cosmos-Reason1 [3]<br>|Cosmos-Reason1 [3]<br>|REG<br>|Desc.+Ctrl.+Traj.<br>|
|49<br>UniUGP [173]<br>50<br>MindDrive [232]<br>|arXiv25<br>arXiv’25||**W**<br>**N**<br>**N**<br>**N**|Qwen2.5-VL [5]<br>ResNet-34 [87]<br>|Qwen2.5-VL [5]<br>LLaVA-1B [129]<br>|GEN<br>GEN|Desc.+Traj.<br>Traj.|
|51<br>AdaThinkDrive [176]|arXiv’25||**N**|InternVL3 [343]|InternVL3 [343]|REG|Desc.+Traj.+Meta.|
|52<br>Percept-WAM [79]|arXiv’25||**N**<br>**N**|InternViT [34]|InternVL2 [263]|REG|Traj.|
|53<br>Reasoning-VLA[316]|arXiv’25||**N**<br>**N**<br>**W**<br>**A**|Qwen2.5-VL[5]|Qwen2.5-VL[5]|REG|Traj.|
|<br>54<br>SDi[134]|Xi’25||**N**<br>**B**|<br>Q25VL[5]|<br>Q25VL[5]|REG|D+Tj|
|pacerve <br>55<br>OpenDriveVLA [339]|arv<br>AAAI’26||**N**|wen.- <br>BEVFormer [148]|wen.- <br>Qwen2.5 [294]|LH|esc.ra.<br>Ctrl.+Traj.|
|_•_ **Sec. 4.2.1: Dual-System: Expl**<br>56<br>DiVLM249|**icit Action G**<br>’|**uidance**|||VL4|REG|DT|
|rve []<br><br>|CoRL24<br>||**N**<br>**S**<br>|-<br>|Qwen []<br><br>||esc.+raj.<br>|
|57<br>LeapAD [187]<br>58<br>FasionAD [207]|NeurIPS’24<br>arXiv’24||**C**<br>**N**<br>**C**|QwenVL [4]<br>GenAD [332]|GPT-4 [1],<br>Qwen1.5 [244]<br>CLIP [210],<br>QwenVL [4]|LH<br>GEN|Ctrl.+Traj.<br>Ctrl.+Traj.|
|59<br>Senna [108]<br>61<br>DME-Driver [80]|arXiv’24<br>AAAI’25||**N**<br>**H**|VADv2 [30], ViT [57]<br>UniAD [93]|Vicuna [36]<br>LLaVA [159]|REG<br>REG|Desc.+Traj.<br>Desc.+Traj.|
|62<br>SOLVE [32]<br><br>AA|CVPR’25<br>’||**N**<br><br>|EVA-02 [62]<br>AA|LLaVA-1.5 [160]<br>|REG<br>|Ctrl.+Traj.<br>l|
|63<br>ReL-D [175]<br><br>|ICCV25||**N**<br>**B**|UniD [93], VD [107]<br><br>|MiniCPM-2.5 [306]<br>|REG<br>|Ctr.+Traj.<br>|
|64<br>LeapVAD [181]<br>f|TNNLS’25||**D**<br>**C**|QwenVL [4]<br>InternVL2 [263]<br>|GPT-4o [195]<br>|LH<br>|Ctrl.+Traj.|
|65<br>DiffVLA [106]<br>66<br>FasionAD++ [208]|arXiv’25<br>arXiv’25||**N**<br>**N**<br>**C**|CLIP [210]<br>BEVFormer [148]|Vicuna-1.5 [36]<br>Vicuna-1.5 [36],<br>QwenVL [4]|GEN<br>GEN|Traj.<br>Ctrl.+Traj.|
|_•_ **Sec. 4.2.2: Dual-System: Imp**<br>67<br>VLP [197]|**licit Represe**<br>CVPR’24|**ntations Transfer**|**N**|UniAD [93], VAD [107]|CLIP [210]|REG|Traj.|
|68<br>VLM-AD [286]|CoRL’25||**N**|UniAD [93], VAD [107]|CLIP [210]|REG|Traj.|
|69<br>DiMA [88]<br>70<br>ALNP3182|CVPR’25<br>’||**N**<br>|UniAD [93], VAD [107]<br>VAD107|LLaVA-1.5 [160]<br>LLMA2252|REG<br>REG|Ctrl.+Traj.<br>DT|
|- []<br><br>|arXiv25<br>||**N**<br>|[]<br>|a- []<br>||esc.+raj.<br>|
|71<br>VERDI [63]<br><br>|arXiv’25||**N**|VAD [107]<br>fi|Qwen2.5-VL [5]<br>|REG<br>|Ctrl.+Traj.<br>|
|72<br>VLM-E2E [163]|arXiv’25||**N**|EfficientNet [238]|CLIP [210]|REG|Traj.|
|73<br>ReCogDrive [145]|arXiv’25||**N**|InternViT [34]|Qwen2.5 [294]|GEN|Desc.+Traj.|
|74<br>InsightDrive [227]<br>75<br>NetRoller[277]|arXiv’25<br>arXiv’25||**N**<br>**N**<br>**D**|ResNet [87]<br>CLIP[210]|BERT [52]<br>LLaMA-2[252]|REG<br>REG|Traj.<br>Traj|
|<br>76<br>ViLaD [45]<br>77<br>OmniScene [164]|arXiv’25<br>arXiv’25||**N**<br>**N**|<br>SigLIP-2 [253]<br>ResNet [87]|<br>LLaDA-V [303]<br>Qwen2.5-VL [5]|GEN<br>REG|.<br>Ctrl.+Traj.<br>Traj.|
|78<br>LMAD [226]|arXiv’25||**N**<br>**D**|VAD [107]|LLaVA-1.5 [160]|LH|Desc.+Meta.|


12 

From an architectural standpoint, current VLA methodologies for autonomous driving can be grouped into: 

- **End-to-End VLA** : a single model directly maps multimodal sensory inputs and language to actions. 

- **Dual-System VLA** : a VLM provides high-level reasoning or guidance, while a specialized driving module executes fast, low-level action. 

#### **4.1 End-to-End VLA for Autonomous Driving** 

End-to-end VLA frameworks aim to unify perception, reasoning, and planning within a single architecture. By leveraging the generalization ability of multimodal large language models (MLLMs), they directly transform multimodal observations into actions, reducing reliance on hand-crafted modules and task-specific heuristics. According to the form of their outputs, existing approaches can be broadly divided into two families, as illustrated in Figure 5: **textual action generators** , which operate primarily in the language space, and **numerical action generators** , which predict trajectories or controls in a continuous or discretized numeric space. 

##### **4.1.1 Textual Action Generator** 

Textual action generators formulate driving as a reasoning problem in the language space. The model produces human-readable symbolic decisions, allowing it to “think” and justify its outputs in words. Depending on the abstraction level of these outputs, existing methods can be grouped into _meta-actions_ and _trajectory waypoints_ . 

**Meta-Actions** are discrete, semantic driving decisions, such as “accelerate”, “stop”, or “change lane”. They form an interpretable interface between high-level reasoning in VLMs and downstream controllers. Early works mainly used language models to output free-form text or conceptual descriptions, which are not directly executable. DriveMLM [46] narrows this gap by aligning LLM outputs with behavioral planning states in a modular stack, enabling language models to act as intermediate planners whose symbolic decisions can be converted into control commands. 

Subsequent methods strengthen robustness and reasoning-planning alignment 


**Figure 5** The categorization of **End-to-End VLA models** based on the form of model outputs, including _Textual Action Models_ (Sec. 4.1.1), and _Numerical Action Models_ (Sec. 4.1.2). 

with reinforcement learning and chain-of-thought supervision [109, 146, 224]. AlphaDrive [109] introduces Group Relative Policy Optimization (GRPO) [224] to refine meta-actions using rewards that jointly consider trajectory quality, decision correctness, and format consistency. DriveAgent-R1 [330] first fine-tunes on a curated CoT dataset to encourage step-wise visual reasoning, then applies RL with trajectory- and meta-action-based rewards to bias reasoning paths toward decisions that are practically useful for driving. Recognizing that single-frame front-view inputs limit temporal and spatial understanding, Sce2DriveX [327] further incorporates multi-view video streams and BEV representations, enabling context-aware meta-decisions that are consistent with road topology and spatiotemporal dynamics. 

**Trajectory Waypoints** –based textual generators frame motion planning as the prediction of future coordinates expressed in natural language, thereby unifying reasoning and trajectory forecasting within a single linguistic sequence. DriveLM [225] is an early representative of this paradigm, modeling autonomous driving as graph-structured visual question answering and generating textualized trajectory waypoints conditioned on multi-stage perception, prediction, and planning. Building on this idea, subsequent works adopt end-to-end multimodal formulations. EMMA [98] integrates camera observations and navigation commands into a unified language-driven pipeline for joint perception, road-graph understanding, and trajectory prediction. To enhance robustness in challenging scenarios, ImpromptuVLA [35] introduces an 80K-clip corner-case dataset, 

13 

demonstrating that pretraining on diverse edge cases significantly improves trajectory accuracy and closed-loop stability. LightEMMA [209] further benchmarks 12 vision–language models, revealing clear trade-offs between interpretability and numerical precision. 

A complementary research direction focuses on better aligning reasoning with decision-making. RDADriver [97] enforces consistency between chain-of-thought explanations and trajectory outputs through tailored constraints, while Drive-R1 [146] leverages reinforcement learning to improve alignment between textual reasoning and waypoint prediction. Beyond alignment, efficiency and knowledge integration are explored by FastDriveVLA [18] via token pruning, WiseAD [323] through explicit driving priors, and OmniDrive [259] using counterfactual reasoning. WKER [313] further enhances robustness under occlusion by combining instruction-guided token selection with external knowledge sources. 

Overall, textual action generators offer strong interpretability and rich reasoning but must bridge a fundamental gap between discrete language tokens and continuous control spaces. This mismatch can introduce precision limits and, in extreme cases, unstable or collapsed trajectories. 

##### **4.1.2 Numerical Action Generator** 

Numerical action generators augment VLM backbones with mechanisms that produce directly usable numeric outputs. The model still leverages language-driven reasoning internally, but its final predictions are expressed as trajectories, waypoints, or control values that can be consumed by classical planners or low-level controllers. Two main realizations exist: _additional action heads_ attached to the backbone, and _additional action tokens_ that discretize continuous actions into a token space. 

**Additional Action Head.** A common strategy is to attach specialized prediction heads to vision-language models. BEVDriver [270] couples a multimodal encoder with a GRU-based head over BEV features, linking language-grounded reasoning with spatial waypoint prediction. CoVLA-Agent [2] uses a lightweight MLP head trained on the CoVLA dataset, demonstrating that joint supervision from trajectories and captions can simultaneously improve interpretability and numeric accuracy. DriveGPT4-V2 [288] augments token-based planning with an MLP that maps multimodal embeddings to continuous trajectories, enhancing sample efficiency while retaining GPT-style reasoning. 

To specialize behaviors, DriveMoE [299] employs a Mixture-of-Experts design whose action head dynamically activates experts for skills such as lane following or overtaking. DSDrive [167] proposes a dual-head coordination module, with one head predicting waypoints and another generating reasoning outputs; distillation from larger VLMs keeps the model compact yet interpretable. LMDrive [222] integrates multimodal encoders with an MLP that directly outputs control signals in a closed loop, marking one of the first instruction-following, language-guided end-to-end systems. 

Beyond simple MLPs, ORION [66] replaces deterministic heads with a diffusion-based predictor, modeling multi-modal trajectory distributions under uncertainty. SimLingo [213] decouples temporal speed waypoints from geometric path waypoints via a disentangled MLP head, enabling finer-grained control. 

**Additional Action Tokens.** Instead of explicit heads, some works reuse the language token space to represent actions. AutoVLA [340] discretizes continuous trajectories into a codebook of action tokens, which are autoregressively generated alongside reasoning tokens, thereby unifying semantic reasoning and planning within a single sequence. Reinforcement fine-tuning penalizes redundant reasoning and improves token efficiency. OpenDriveVLA [339] follows a similar token-based paradigm but grounds token generation in a hierarchical alignment between 2D/3D perception and the language model. Structured features are embedded into a unified semantic space, and interaction tokens for the ego vehicle, environment, and other agents are autoregressively decoded into driving actions. 

Numerical action generators are well-suited for downstream control, as their outputs are natively compatible with planners and actuators. However, they typically sacrifice some interpretability and often require substantial supervised data for stable training. When discretized action tokens are used, quantization artifacts can further limit fine-grained control accuracy. 

14 

#### **4.2 Dual-System VLA** 

Dual-system VLA frameworks draw inspiration from the dual-process theory popularized by _Thinking, Fast and Slow_ [113]. In this paradigm, a VLM serves as the _slow_ , deliberative system that performs high-level reasoning, situational assessment, and linguistic inference, while a specialized autonomous driving module acts as the _fast_ system responsible for real-time, low-latency trajectory generation and control. By combining these complementary strengths, dual-system frameworks aim to achieve both interpretability and safety-critical reactivity. 


Depending on how VLM outputs interact with the specialized planner, existing methods can be categorized into two families: **explicit action guidance** and **implicit representation transfer** , as illustrated in Figure 6. 

##### **4.2.1 Explicit Action Guidance** 

Explicit action guidance frameworks use VLMs as structured action generators, whose high-level outputs are subsequently transformed or refined by the fast driving module. These approaches differ in their abstraction level and are mainly grouped into **meta-action guidance** and **waypoint supervision** . 

**Figure 6** The categorization of **Dual-System VLA Models** based on how VLM interacts with E2E module, including explicit action guidance (Sec. 4.2.1),), and implicit representations transfer models (Sec. 4.2.2).). 

**Meta-Action Guidance** resorts to VLMs VLM interacts with E2E module, including explicit action guidance to output symbolic driving intentions, (Sec. 4.2.1),), and implicit representations transfer models (Sec. 4.2.2).). such as “slow down”, “change lane”, or “turn left”, which act as semantic priors for downstream planners. This design leverages the interpretability of linguistic actions while avoiding the precision challenges of directly generating continuous trajectories. Early work such as FasionAD [207] embodies the dual-process design by pairing a fast, data-driven planner with a slow VLM that issues meta-actions; a learned switching mechanism selects the appropriate pathway based on confidence and scene context. LeapVAD [181] refines this structure by combining an analytic branch that builds a memory bank with a heuristic branch that retrieves prior meta-actions for familiar situations. 

More recent systems integrate high-level reasoning more tightly with planning. Senna [108] couples a commonsense VLM with an end-to-end planner: Senna-VLM produces natural-language decisions, which Senna-E2E converts into executable trajectories. DiffVLA [106] injects VLM-generated lateral and longitudinal decisions as one-hot priors into a diffusion-based planner, guiding multi-modal trajectory denoising. 

Hierarchical frameworks such as DME-Driver [80] further separate decision and execution: a VLM-based Decision-Maker supplies meta-decisions or visual attention priors, and a dedicated Executor translates them into fine-grained control. ReAL-AD [175] extends this to a full three-layer hierarchy: strategy, decision, and operation, where VLM-derived situational insights shape progressively refined planning commands. 

**Waypoint Supervision** is an explicit guidance that uses VLMs to generate coarse trajectory waypoints, which the fast planning module refines into dense, executable trajectories. DriveVLM [249] adopts a hierarchical reasoning-to-planning pipeline: the VLM produces meta-actions and coarse waypoints through chain-of-thought reasoning, and conventional planners transform them into detailed trajectories. 

SOLVE [32] strengthens VLM-planner coordination through a shared vision encoder and a Trajectory Chainof-Thought module that iteratively refines candidate waypoints before final selection by the E2E planner. These designs provide a tighter numerical interface between reasoning and control, enabling VLMs to influence planning while retaining stability through classical refinement. 

15 

Overall, explicit guidance approaches maintain strong interpretability and grant VLM a direct role in decisionmaking. However, they remain sensitive to the accuracy and consistency of VLM outputs; misaligned or ambiguous commands can propagate downstream and degrade planning safety. 

##### **4.2.2 Implicit Representations Transfer** 

Implicit feature constraint refers to methods where the VLM acts as a teacher or auxiliary module during training, transferring reasoning ability or cognitive priors as latent features to the compact E2E network. These approaches fall into two main groups: **knowledge distillation** and **multimodal feature fusion** . 

**Knowledge Distillation** -based approaches transfer VLM-generated explanations, reasoning traces, or structured action semantics into the latent space of the E2E driving model. VLP [197] aligns BEV features and planning queries with pretrained language embeddings using contrastive and supervisory objectives, enabling planners to inherit commonsense scene understanding. VLM-AD [286] generates free-form textual justifications and structured behavior labels using a VLM, distilling them into the planner through an alignment head and an action classification head. This dual-supervision design helps the E2E module acquire richer semantic representations while remaining computationally light during deployment. 

More comprehensive alignment is seen in VERDI [63], which aligns perception, prediction, and planning outputs with VLM-generated chain-of-thought explanations, injecting structured reasoning across all stages of the pipeline. ALN-P3 [182] extends this principle with full-stack co-distillation: perception tokens, predicted motions, and planned trajectories are jointly aligned with VLM reasoning to unify cognition and execution. 

**Multimodal Feature Fusion** -based approaches directly integrate VLM-derived features into the fast planner. InsightDrive [227] introduces language-guided scene representations, where VLM-generated descriptions highlight critical regions and modulate BEV features via cross-attention. VLM-E2E [163] explicitly models driver attention by fusing textual attention cues with BEV features through a learnable gating mechanism. Beyond attention cues, NetRoller [277] extracts latent reasoning variables from VLMs and adapts them into compact features suitable for real-time planners. ReCogDrive [145] aligns linguistic priors with a diffusionbased planner, refining trajectories through reinforcement learning to promote safety and human-like behavior. ETA [78] focuses on efficiency: VLM reasoning is computed asynchronously in earlier frames and fused into current features using an action-mask mechanism, ensuring guidance without incurring high real-time costs. 

Implicit transfer methods reduce inference cost and avoid dependence on large VLMs at runtime, but they may sacrifice interpretability, and excessive distillation can oversimplify reasoning signals. Their effectiveness also depends strongly on how well the distilled or fused features align with the capacity of the fast driving module. 

## **5 Datasets & Benchmark** 

Standardized datasets and benchmarks form the empirical foundation of VLA research, supporting model development, training, and evaluation. Since VLA driving systems integrate perception, language, and action, VLA datasets exhibit substantial diversity in modality composition, annotation granularity, and task definitions. Accordingly, evaluation protocols vary substantially, encompassing conventional trajectory-based metrics, language-centric assessments, and interactive closed-loop evaluations. 

#### **5.1 Datasets for VLA in Autonomous Driving** 

Traditionally, VA datasets provide rich sensory observations (cameras, LiDAR, RADAR) paired with control actions, enabling end-to-end mapping from images to trajectories [16, 17, 304]. These datasets underpin the development of early IL/RL-based VA models. 

As language becomes an increasingly important modality for reasoning, instruction following, and explainability, VLA datasets have emerged [46, 225, 249, 262]. These datasets extend traditional driving logs with textual instructions, question-answer pairs, or rationales aligned with visual observations and expert actions [2, 35]. In general, a dataset is considered VLA-compatible when it provides temporally or semantically aligned language 

16 

- **Table 4** Summary of existing **Datasets & Benchmarks** for training and evaluating the VA and VLA models. _•_ **Vision Sensor Inputs** : Camera, LiDAR point cloud, RADAR point cloud, and Map. 

- **Vision Types** : <u>Real:</u> Data collected from real driving scenes, and <u>Sim:</u> Data collected from simulator. 

- **Language Annotation Types** : <u>A:</u> Automatic labeling process, and <u>M:</u> Manual labeling process. 

- **Action Types** : Traj.: Numerical trajectory output, and <u>Ctrl:</u> Control signal output. 

- **Action Metrics** : Open: Open-loop Evaluation, <u>CL:</u> Closed-loop Evaluation, and Lang.: Language-based Evaluation. 

||||**Vision**||**Languag**|**e**||**Act**|**ion**|**h k**|
|---|---|---|---|---|---|---|---|---|---|---|
|**Dataset**|**Year**|**Sensor**|**Type**|**Scale**|**Category**|**Label**|**Scale**|**Type**|**Metric**|**Oter Tass**|
|_•_ **Vision-Action Datasets**|||||||||||
|**B**<br>BDD100K [304]<br>|2020<br>||Real<br>|120M<br>|-|-|-|Traj.<br>|-<br>|Percept.<br>|
|**N**<br>nuScenes [16]|2020||Real|1.4M|-|-|-|Traj.|Open|Percept.|
|**W**<br>Waymo[234]|2020||Real|200M|-|-|-|Traj.|Open|Percept., Forecast.|
|**N**<br>nuPlan [17]|2021||Real|4.6M|-|-|-|Ctrl, Traj.|CL|Forecast.|
|**A**<br>Argoverse 2 [269]|2021||Real|300K|-|-|-|Traj.|Open|Percept., Forecast.|
|**B**<br>Bench2Drive [103]|2024||Sim|2M|-|-|-|Traj.|CL|-|
|**R**<br>RoboBEV [275]<br>|2025||Real|866K|-|-|-|Traj.|Open|Percept.|
|**W**<br>WOD-E2E [283]|2025||Real|800K|-|-|-|Traj.|Open|-|
|_•_ **Vision-Language-Action D**|**atasets**||||||||||
|**B**<br>BDD-X [117]<br>|2018||Real|8.4M|Caption|M|26K|Ctrl|Open|Reason.|
|**T**<br>Talk2Car [51]|2022||Real|400K|Caption|M|12K|Ctrl, Traj.|Open|Ground.|
|**S**<br>SDN [183]|2022||Sim|-|Instruction, QA|A+M|8.4K|Ctrl, Traj.|CL|QA|
|**D**<br>DriveMLM [46]|2023||Sim|-|Reason., Deci.|A+M|-|Ctrl, Traj.|CL, Lang.|Reason., QA|
|**L**<br>LMDrive [222]|2024||Sim|3M|Instruction|A+M|64K|Traj.|CL|-|
|**B**<br>DriveLM-N [225]|2024||Real|4.8K|QA|M|445K|Ctrl, Traj.|Open|Reason., QA|
|**B**<br>DriveLM-C [225]<br>|2024||Sim|64K|QA|A|3.76M|Ctrl, Traj.|Open|Reason., QA|
|**H**<br>HBD [80]|2024||Real,Sim|-|Deci., Descrip., QA|A+M|-|Traj.|Open|Descrip., QA|
|**V**<br>VLAAD [201]|2024||Real|-|Reason., QA|A+M|64K|Ctrl.|Lang.|Caption, QA|
|**S**<br>SUP-AD [249]<br>|2024||Real|-|Action, Reason., QA|A+M|-|Ctrl, Traj.|Open, Lang.|Reason, QA|
|**N**<br>NuInstruct [54]|2024||Real|11.8K|Instruction|A|91K|Ctrl|Lang.|Reason.|
|**W**<br>WOMD-Reason [141]|2024||Real|63K|QA|A|2940K|Plan.|Lang.|Reason., QA|
|**D**<br>DriveCoT [262]<br>|2024||Sim|-|CoT, Deci.|A|36K|Ctrl|Open|Reason.|
|**R**<br>Reason2Drive [192]|2024||Real|-|Reason., QA|A|632K|Ctrl, Traj.|Open|Reason., QA|
|**D**<br>DriveBench [274]|2025||Real|19.2K|QA|A+M|20.5K|Ctrl|Lang.|QA|
|**M**<br>MetaAD [109]|2025||Real|120K|Reason., Plan, QA|-|30K|Ctrl|Lang.|Reason.|
|**O**<br>OmniDrive [259]|2025||Real|-|Reason., QA|A|-|Ctrl, Traj.|Open|Reason.|
|**N**<br>NuInteract [328]|2025||Real|34K|Caption, QA|A|1.5M|Ctrl|Lang.|Percept., Ground.|
|**D**<br>DriveAction [86]|2025||Real|2.6K|QA|A|16.18K|Ctrl|Lang.|-|
|**I**<br>ImpromptuVLA [35]|2025||Real,Sim|2M|Instruction, QA|A+M|80K|Ctrl, Traj.|Open, CL|QA|
|**C**<br>CoVLA [2]|2025||Real|6M|Caption|A|6M|Traj.|Open|-|
|**O**<br>OmniReason-N [165]|2025||Real|-|QA|A|-|Ctrl, Traj.|Open|Reason., QA|
|**O**<br>OmniReason-B2D [165]|2025||Sim|-|QA|A|-|Ctrl, Traj.|Open|Reason., QA|


annotations that connect visual observations with actions or trajectories, enabling tri-modal learning. The summarized collections are provided in Table 4. 

##### **5.1.1 Vision-Action Datasets** 

Originally, BDD100K [304] provides 100K diverse driving videos from across the United States, covering a wide spectrum of weather, lighting, and traffic conditions, making it a foundational dataset for behavioral cloning and end-to-end driving. Later, nuScenes [16] offers 1,000 multi-sensor driving scenes with synchronized 6- camera surround views, LiDAR sweeps, radar, 3D boxes, and motion trajectories, supporting both perception tasks and multi-agent motion forecasting. Larger-scale datasets such as the Waymo Open Dataset [59] and Argoverse 2 [269] further extend this paradigm with higher-resolution sensors, longer trajectories, and detailed HD maps, enabling robust training of perception-to-prediction pipelines in diverse urban settings. Complementing these efforts, nuPlan [17] incorporates long-horizon ego trajectories, dense map context, and simulation interfaces for closed-loop testing, providing comprehensive supervision for evaluating decisionmaking and planning under complex, real-world conditions. While lacking explicit language supervision, these VA datasets establish the visual–action foundation for VLA development by providing structured supervision that links visual perception, temporal dynamics, and expert decision-making. 

##### **5.1.2 Vision-Language-Action Datasets** 

Building upon the visual–action foundation established by VA datasets, VLA datasets enrich driving logs with structured or free-form natural language to support joint perception-language-action learning. 

17 

**Table 5** Comparisons of state-of-the-art models for **Open-Loop Planning** on the nuScenes [16] benchmark. _•_ **Input** : :Camera, :LiDAR, : Prompt, : Instruct., : Scene Descrip., : Status, : Rule, : Context. _•_ **Action** : <u>LH:</u> Language Head, <u>RL:</u> Policy w/ Reinforcement Learning, <u>REG:</u> Decoder + MLP, <u>SEL:</u> Trajectory Selection w/ Cost, and <u>GEN:</u> Trajectory Generation w/ Generative Model. _•_ **Evaluation Metrics** : L2 <u>(</u> _<u>↓</u>_ <u>):</u> L2 Error in meters, and CR <u>(</u> _<u>↓</u>_ <u>):</u> Collision Rate. 

|**Model**|**Year**|**Input**|**Vision**|**Language**|**Action**|**1s**|**L**<br>**2s**|**2**_↓_<br>**3s**|**Avg.**|**1s**|**C**<br>**2s**|**R**_↓_<br>**3s**|**Avg.**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|_•_ **Vision-Action Models**||||||||||||||
|ST-P3 [91]|2022||EfficientNet|-|REG|1.33|2.11|2.90|2.11|0.23|0.62|1.27|0.71|
|UniAD [93]|2022||ResNet|-|REG|0.44|0.67|0.96|0.69|0.04|0.08|0.23|0.12|
|VAD [107]<br>|2023||ResNet|-|REG|0.17|0.34|0.60|0.37|0.07|0.10|0.24|0.14|
|OccNet [250]|2023||ResNet|-|SEL|1.29|2.13|2.99|2.14|0.21|0.59|1.37|0.72|
|BEV-Planner[149]|2024||ResNet|-|REG|030|052|083|055|010|037|130|059|
|<br>Drive-WM [266]|2024||ConvNeXt|-|SEL|.<br>0.43|.<br>0.77|.<br>1.20|.<br>0.80|.<br><br>0.10|.<br>0.21|.<br>0.48|.<br>0.26|
|GenAD [332]|2024||ResNet|-|GEN|0.36|0.83|1.55|0.91|0.06|0.23|1.00|0.43|
|OccWorld [331]|2024||ResNet|-|REG|0.43|1.08|1.99|1.17|0.07|0.38|1.35|0.60|
|DriveDreamer [264]|2024||SD|-|REG|-|-|-|0.29|-|-|-|0.15|
|SparseAD[317]|2024||ResNet|-|REG|0.15|0.31|0.56|0.34|0.00|0.04|0.15|0.06|
|<br>GaussianAD [333]|2024||ResNet|-|REG|0.40|0.64|0.88|0.64|0.09|0.38|0.81|0.42|
|LAW [142]|2024||Swin-T|-|REG|0.24|0.46|0.76|0.49|0.08|0.10|0.39|0.19|
|SSR [133]|2024||ResNet|-|REG|0.18|0.36|0.63|0.39|0.01|0.04|0.12|0.06|
|Drive-OccWorld [297]|2025||ResNet|-|REG|0.25|0.44|0.72|0.47|0.03|0.08|0.22|0.11|
|DriveTransformer [104]|2025||ResNet|-|REG|0.19|0.34|0.66|0.40|0.03|0.10|0.21|0.11|
|DiffusionDrive [155]|2025||ResNet|-|GEN|0.27|0.54|0.90|0.57|0.03|0.05|0.16|0.08|
|World4Drive [335]|2025||ResNet|-|REG|0.23|0.47|0.81|0.50|0.02|0.12|0.33|0.16|
|Epona [321]|2025||DC-AE|-|REG|0.61|1.17|1.98|1.25|0.01|0.22|0.85|0.36|
|SeerDrive [315]|2025||ResNet|-|SEL|0.20|0.39|0.69|0.43|0.00|0.05|0.14|0.06|
|GuideFlow [161]|2025||ResNet|-|GEN|-|-|-|-|0.00|0.02|0.18|0.07|
|_•_ **Vision-Language-Action**|**Models**|||||||||||||
|Agent-Driver [185]|2023||-|GPT-3.5|LH|0.16|0.34|0.61|0.37|0.02|0.07|0.18|0.09|
|DriveVLM [249]|2024||ViT|QwenVL|GEN|0.18|0.34|0.68|0.40|0.10|0.22|0.45|0.27|
|DriveVLM-Dual [249]|2024||ViT|QwenVL|REG|0.15|0.29|0.48|0.31|0.05|0.08|0.17|0.10|
|RAG-Driver [309]|2024||CLIP|Vicuna-1.5|LH|0.34|0.37|0.69|0.40|0.01|0.05|0.26|0.10|
|Senna [108]|2024||ViT|Vicuna-1.5|REG|0.37|0.54|0.86|0.59|0.09|0.12|0.33|0.18|
|Doe-1 [334]|2024||Lumina-mGPT|BPE Tokenizer|LH|0.37|0.67|1.07|0.70|0.02|0.14|0.47|0.21|
|VLP [197]|2024||UniAD, VAD|CLIP|REG|0.30|0.53|0.84|0.55|0.01|0.07|0.38|0.15|
|VLM-AD [286]|2024||UniAD, VAD|CLIP-ViT|REG|0.24|0.46|0.75|0.48|0.12|0.17|0.41|0.23|
|OpenDriveVLA [339]|2025||ResNet|Qwen2.5-VL|LH|0.14|0.30|0.55|0.33|0.02|0.07|0.22|0.10|
|OmniDrive [259]|2025||EVA-02|LLaMA2|LH|0.40|0.80|1.32|0.84|0.04|0.46|2.32|0.94|
|ORION [66]|2025||EVA-02|Vicuna-1.5|GEN|0.17|0.31|0.55|0.34|0.05|0.25|0.80|0.37|
|EMMA98|2025||GiiVLM|Gii|LH|014|029|054|03|||||
|[]<br>WKER [313]|2025||emn-<br>EVA-02|emn<br>LLaMA3|LH|.<br>0.14|.<br>0.30|.<br>0.55|.<br>0.33|-<br><br>0.07|-<br>0.14|-<br>0.32|-<br>0.18|
|Drive-R1 [146]|2025||InternVL2|InternVL2|LH|0.14|0.28|0.50|0.31|0.02|0.06|0.19|0.09|
|ReAL-AD [175]|2025||ResNet|MiniCPM|REG|0.30|0.48|0.67|0.48|0.07|0.10|0.28|0.15|
|ReAL-AD [175]|2025||ResNet|QwenVL|REG|0.35|0.53|0.71|0.53|0.09|0.12|0.31|0.17|
|DiMA [88]|2025||VAD|LLaVA-1.5|REG|0.18|0.50|1.03|0.57|0.00|0.05|0.16|0.08|
|FasionAD [207]|2025||BEVFormer|VLM+Thinking|GEN|0.19|0.62|1.25|0.69|0.02|0.09|0.44|0.18|
|InsightDrive[227]|2025||ResNet|VLMs|REG|023|041|068|044|009|010|027|015|
|<br>S4-Driver [276]|2025||ViT-G|PaLI3|LH|.<br>0.13|.<br>0.28|.<br>0.51|.<br>0.31|.<br><br>-|.<br>-|.<br>-|.<br>-|
|SOLVE [32]|2025||EVA-02|LLaVA-1.5|REG|0.13|0.25|0.47|0.28|0.00|0.16|0.43|0.20|
|VERDI [63]|2025||VAD|Qwen2.5-VL|REG|0.36|0.62|0.96|0.65|-|-|-|-|
|OmniReason [165]|2025||EVA-02|LLaVA-1.5|LH|0.15|0.31|0.57|0.34|0.04|0.18|0.98|0.40|
|FutureSightDrive [312]|2025||ViT|Qwen2-VL|LH|0.14|0.25|0.46|0.28|0.03|0.06|0.21|0.10|
|Occ-LLM [284]|2025||-|LLaMA2|LH|0.12|0.24|0.49|0.28|-|-|-|-|
|FastDriveVLA [18]|2025||Qwen2.5-VL|Qwen2.5-VL|LH|0.14|0.29|0.54|0.33|0.00|0.18|0.70|0.29|
|AutoDrive-R² [310]|2025||Qwen2.5-VL|Qwen2.5-VL|LH|0.13|0.19|0.25|0.19|-|-|-|-|
|VDrive[76]|2025||Qwen25-VLCVQ|InternVL3|GEN|012|026|050|029|003|016|036|018|
|<br>OccVLA [166]|2025||., <br>VQ-VAE|PaliGemma-2|REG|.<br>0.18|.<br>0.26|.<br>0.40|.<br>0.28|.<br><br>-|.<br>-|.<br>-|.<br>-|
|FasionAD++[207]|2024||GenAD|CLIP<br>QwenVL|GEN|013|026|045|028|005|008|015|009|
|<br>ALN-P3 [182]|2025||VAD|,<br><br>CLIP,<br>LLaMA-2|REG|.<br>-|.<br>-|.<br>-|.<br>-|.<br>0.05|.<br>0.09|.<br>0.35|.<br>0.16|
|VLM-E2E [163]|2025||EfficientNet|CLIP|REG|0.28|0.50|0.80|0.53|0.01|0.06|0.20|0.09|
|NetRoller[277]|2025||CLIP|LLaMA-2|REG|0.38|0.66|1.01|0.68|0.06|0.13|0.30|0.16|
|OmniScene [164]|2025||ResNet|Qwen2.5-VL|REG|0.28|0.53|0.91|0.57|0.00|0.04|0.19|0.08|
|Sce2DriveX[327]|2025||OpenCLIP|Vicuna-1.5|LH|0.15|0.33|0.59|0.36|-|-|-|-|
|<br>dVLM-AD [178]<br>PtWAM79|2025<br>2025||SigLIP2<br>ItViT|LLaDA-V<br>ItVL2|LH<br>REG|0.15<br>016|0.40<br>033|0.68<br>060|0.41<br>036|-<br>|-|-|-|
|ercep- []<br>Reasoning-VLA [316]|2025||nern<br>Qwen2.5-VL|nern<br>Qwen2.5-VL|REG|.<br>0.05|.<br>0.19|.<br>0.41|.<br>0.22|-<br><br>0.02|-<br>0.06|-<br>0.13|-<br>0.07|


18 

Representative examples include BDD-X [117], which extends BDD100K with time-aligned human rationales, where annotators describe why the driver performed a specific action. This dataset provides early grounding for language-based explanations. DriveLM [225] constructs graph-structured question-answer pairs based on nuScenes and CARLA scenarios. These QA pairs target conditional reasoning, enabling models to infer high-level intent, spatial relations, and driving decisions. Impromptu VLA [35] aggregates data from eight public driving datasets and supplements them with captions, instructions, and QA pairs aligned with expert trajectories. The focus is on corner cases and long-tailed events. Other datasets, such as LingoQA [186] and CoVLA [2], collect real-world driving videos paired with natural language QA or behavior descriptions, emphasizing spatiotemporal reasoning and human-understandable driving motivations. 

Notably, QA-style annotations have emerged as a dominant paradigm for extending driving datasets, serving as a common foundation for training and evaluating reasoning and planning capabilities [86, 225]. However, the scope and assumptions embedded in such annotations naturally influence model behavior, motivating further exploration of more diverse perspectives, planning horizons, and evaluation protocols for real-world deployment. 

#### **5.2 Evaluation Metrics** 

Evaluation metrics differ according to the model’s output modality: **trajectory-based** metrics for continuous action prediction and **text-based** metrics for models producing linguistic commands or rationales. 

##### **5.2.1 Trajectory-Based Action Evaluation** 

Trajectory-based outputs are typically evaluated in open-loop and closed-loop settings. 

**Open-Loop Evaluation.** The predicted trajectory is directly compared against expert trajectories without executing in a simulator. Metrics such as L2 error and collision rate [91], along with trajectory-based indicators including Average Displacement Error (ADE), Final Displacement Error (FDE), and Miss Rate (MR) [93], are widely used. These metrics regard human driving demonstrations as the ground truth and formulate planning essentially as an imitation learning task. By measuring the deviation between predicted and expert trajectories, they provide a straightforward way to assess the accuracy of motion prediction. 

**Closed-Loop Evaluation.** Instead, it measures the model’s performance when interacting with a simulation environment ( _e.g._ , CARLA [56]). Representative metrics include route completion (RC), driving score (DS), and infraction distance (ID). Bench2Drive [103] further considers success rate, efficiency, and comfort. NAVSIM [47], built on nuPlan [17], introduces the Predictive Driver Model Score (PDMS), which aggregates subscores for ego progress (EP), time-to-collision (TTC), and comfort (C), while applying penalties on collisions (NC) and driving admissibility (DAC). These metrics provide a holistic view of the safety, feasibility, and deployability of planning actions. 

##### **5.2.2 Text-Based Action Evaluation** 

For low-level vehicle control expressed in natural language, evaluation covers both linguistic quality and control effectiveness. Standard text metrics, such as BLEU, ROUGE, and CIDEr, are commonly used to assess the quality of generated language [225, 328], which measures n-gram overlap with human-annotated reference commands. Beyond command accuracy, reasoning quality is assessed through rationale consistency [192] and human preference ratings of language explanations, particularly in datasets following the BDD-X [117] format. To assess driving applications, execution-based metrics are introduced for behavior assessment. SimLingo [213] introduces an action-dreaming benchmark. The corresponding actions are mapped from the input instruction, which is open-loop evaluated using the success rate. 

Regardless of output modality, these benchmarks emphasize key aspects of action quality, including accuracy, executability, safety, and intention alignment. 

#### **5.3 Quantitative Experiments & Analyses** 

This section reviews quantitative benchmarks for evaluating VLA models across action prediction, planning accuracy, and closed-loop driving performance. Among them, nuScenes [16], NAVSIM [47], and Bench2Drive [103] 

19 

**Table 6** Comparisons of state-of-the-art models on the WOD-E2E [283] test split. 

_•_ **Input** : :Camera, : Sys. Prompt, : Instruct., : Scene Descrip., : Status, : Traffic Rule, : Context Info. _•_ **Action** : <u>LH:</u> Language Head, <u>RL:</u> Policy with Reinforcement Learning, <u>REG:</u> Decoder + MLP, and <u>GEN:</u> Trajectory Generation w/ Generative Model. _•_ **Evaluation Metrics** : RFS <u>(Overall/Spotlight)</u> ( _↓_ ): Rater Feedback Score, ADE 5s/3s ( _↓_ ): Average Displacement Error. 

|**Model**|**Year**|**Input**|**Vision**|**Language**|**Action**|**RFS(Overall)(**_↑_**)**|**RFS(Spotlight)(**_↑_**)**|**ADE 5s(**_↓_**)**|**ADE 3s(**_↓_**)**|
|---|---|---|---|---|---|---|---|---|---|
|_•_ **Vision-Action Models**||||||||||
|Waymo Baseline|2025||-|-|-|7.53|6.60|3.02|1.32|
|Swin-Trajectory [283]|2025||SwinT|-|REG|7.54|6.68|2.81|1.21|
|DiffusionDrive [155]|2025||ResNet|-|GEN|7.69|6.65|2.99|1.31|
|RAP-DINO [64]|2025||DINO|-|REG|8.04|7.20|2.65|1.17|
|_•_ **Vision-Language-Acti**|**on Mode**|**ls**||||||||
|OpenEMMA [278]|2025||Qwen2-VL|Qwen2-VL|LH|5.16|4.71|12.74|6.68|
|HMVLM [256]|2025||ViT|Qwen2.5-VL|LH|7.74|6.73|3.07|1.33|
|AutoVLA [340]|2025||Qwen2.5-VL|Qwen2.5-VL|LH|7.56|6.94|2.96|1.35|
|Poutine [216]|2025||ViT|Qwen2.5-VL|LH|7.99|6.89|2.74|1.21|
|LightEMMA [209]|2025||Qwen2.5-VL|Qwen2.5-VL|LH|6.52|5.71|3.73|1.71|
|dVLM-AD [178]|2025||SigLIP2|LLaDA-V|LH|7.63|-|3.02|1.29|


are the most widely used. More recently, WOD-E2E [283] introduces long-tail, safety-critical scenes with human-preference annotations, enabling more robust assessment of modern E2E and VLA systems. 

##### **5.3.1 nuScenes Benchmark** 

The nuScenes open-loop benchmark evaluates planning quality using trajectory-based metrics, including L2 displacement error and Collision Rate, as summarized in Table 5. Basically, vision-action models such as UniAD [93] reports 0.69m L2 and 0.12 collision rate. Incorporating language generally improves performance by providing semantic cues for safer planning. For instance, Drive-R1 [146] combines supervised CoT alignment with RL finetuning to reach 0.31m L2 and 0.09 collision rate. 

Beyond accuracy, recent studies explore the role of language in handling complex and long-tailed driving scenarios. While improvements are most evident in common cases, rare and highly complex situations remain an active area of investigation, motivating the integration of richer reasoning signals and data sources. 

From a systems perspective, computational efficiency is an important consideration for practical deployment. Lightweight and efficiency-oriented designs, such as InsightDrive [227] (16.3 FPS) and token-pruned architectures like FastDriveVLA [18], illustrate ongoing efforts to balance model capacity with real-time feasibility. For cross-domain evaluation, nuScenes highlights generalization to unseen cities and distribution shifts as a key benchmark dimension. Works such as VLP [197] and DiMA [88] examine this setting and motivate complementary strategies including domain adaptation, distillation, and data augmentation. 

##### **5.3.2 WOD-E2E Benchmark** 

The Waymo Open Dataset for End-to-End Driving (WOD-E2E) [283] is a large-scale benchmark designed to evaluate end-to-end driving systems under long-tail, safety-critical scenarios that rarely appear in conventional datasets. It contains 4K segments with high-level routing commands, ego-status signals, and multi-camera views, enabling rigorous assessment of perception-planning coupling. A key contribution of WOD-E2E is the Rater Feedback Score (RFS), which measures trajectory quality based on alignment with human preference annotations rather than logged expert trajectories. As shown in Table 6, RFS (Overall and Spotlight) complements conventional ADE metrics by providing a more human-aligned assessment of driving behavior. 

Overall results indicate that while vision–action models achieve stable displacement accuracy, VLA models exhibit more diverse performance. Approaches such as Poutine [216], and dVLM-AD [178] achieve balanced RFS and ADE performance, highlighting the importance of effectively aligning language reasoning with trajectory generation. Figure 7 presents the visualized performance of AutoVLA [340] in the WOD-E2E dataset. 

20 

**Table 7** Comparisons of state-of-the-art models for **Open-Loop Planning** on the NAVSIM [47] _navtest_ benchmark. _•_ **Input** : :Camera, : LiDAR, : Prompt, : Instruct., : Scene Descrip., : Status, : Rule, : Context. _•_ **Action** : <u>LH:</u> Language Head, <u>RL:</u> Policy with Reinforcement Learning, <u>REG:</u> Decoder + MLP, <u>SEL:</u> Trajectory Selection w/ Cost, and <u>GEN:</u> Trajectory Generation w/ Generative Model. _•_ **Evaluation Metrics** : <u>NC:</u> Navigation Completion, <u>DAC</u> ( _↑_ ): Driving Accuracy, <u>TTC</u> ( _↑_ ): Time-To-Collision, <u>Comf.</u> ( _↑_ ): Comfort, <u>EP</u> ( _↑_ ): Ego Progress, and <u>PDMS</u> ( _↑_ ): Perception Driving Metric Score. 

|**Model**|**Year**|**Input**|**Vision**|**Language**|**Action**|**NC(**_↑_**)**|**DAC(**_↑_**)**|**TTC(**_↑_**)**|**Comf(**_↑_**)**|**EP(**_↑_**)**|**PDMS(**_↑_**)**|
|---|---|---|---|---|---|---|---|---|---|---|---|
|_•_ **Vision-Action Models**||||||||||||
|TransFuser [39]|2022||ResNet|-|REG|97.7|92.8|92.8|100|79.2|84.0|
|UniAD [93]|2023||ResNet|-|REG|97.8|91.9|92.9|100|78.8|83.4|
|VADv2 [30]|2024||ResNet|-|REG|97.2|89.1|91.6|100|76.0|80.9|
|PARA-Drive [268]|2024||ResNet|-|REG|97.9|92.4|93.0|99.8|79.3|84.0|
|LAW [142]|2024||Swin-T|-|REG|96.4|95.4|88.7|99.9|81.7|84.6|
|DRAMA [308]|2024||ResNet|-|REG|98.0|93.1|94.8|100|80.1|85.5|
|DiffusionDrive [155]|2024||ResNet|-|GEN|98.2|96.2|94.7|100|82.2|88.1|
|WoTE [144]|2025||ResNet|-|SEL|98.5|96.8|94.9|99.9|81.9|88.3|
|World4Drive [335]|2025||ResNet|-|REG|97.4|94.3|92.8|100|79.9|85.1|
|DrivingGPT [33]|2025||VQ-VAE|-|REG|98.9|90.7|94.9|95.6|79.7|82.4|
|AD-R1 [289]|2025||-|-|RL|98.7|97.8|94.8|100|87.5|91.9|
|SeerDrive [315]|2025||VoVNet|-|SEL|98.8|98.6|95.8|100|84.2|90.7|
|Epona [321]|2025||DC-AE|-|REG|97.9|95.1|93.8|99.9|80.4|86.2|
|GoalFlow [279]<br>f|2025||VoVNet|-|GEN|98.4|98.3|94.6|100|85.0|90.3|
|TrajDiff [75]|2025||ResNet|-|GEN|98.1|97.0|94.3|100.0|82.7|88.5|
|DiffusionDriveV2 [345]|2025||ResNet|-|GEN|98.3|97.9|94.8|99.9|87.5|91.2|
|NaviHydra [271]|2025||ResNet|-|SEL|98.7|98.6|88.7|96.2|100.0|92.7|
|Mimir [280]|2025||ResNet|-|GEN|98.2|97.5|94.6|100|83.6|89.3|
|_•_ **Vision-Language-Actio**|**n Model**|**s**||||||||||
|ReCogDrive [145]|2025||InternViT|Qwen2.5-VL|GEN|98.2|97.8|95.2|99.8|83.5|89.6|
|AutoVLA [340]|2025||Qwen2.5-VL|Qwen2.5-VL|LH|99.1|97.1|97.1|99.9|87.6|92.1|
|ReflectDrive [135]|2025||LLaDA-V|LLaDA-V|GEN|99.7|99.5|99.1|99.9|88.9|94.7|
|AdaThinkDrive [176]|2025||InternVL3|InternVL3|REG|99.1|98.8|97.2|100.0|87.9|93.0|
|Percept-WAM [79]|2025||InternViT|InternVL2|REG|98.8|98.6|94.4|99.5|84.8|90.2|
|Reasoning-VLA [316]|2025||Qwen2.5-VL|Qwen2.5-VL|REG|97.8|93.2|98.1|99.8|80.7|91.7|


##### **5.3.3 NAVSIM Benchmark** 

NAVSIM [47] is built on OpenScene (a redistribution of nuPlan [17]), provides a closed-loop simulation environment designed to evaluate planning quality under realistic urban driving conditions. It adopts the PDMS metric, which aggregates multiple driving aspects, including No-Collision (NC), Driving Admissibility (DAC), Time-to-Collision (TTC), Ego Progress (EP), and Comfort (C), offering a holistic assessment of safety, efficiency, and driving smoothness. As shown in Table 7, most methods achieve strong performance on safety-related metrics such as NC and DAC, while TTC and EP serve as more discriminative indicators of planning foresight and long-horizon decision quality. These metrics highlight differences in how models balance safety and progress when interacting with dynamic environments. 

Representative vision–action approaches, such as WoTE [144], achieve 88.3 PDMS by integrating a BEV-based world model with reward-guided trajectory selection, demonstrating the effectiveness of structured world modeling for closed-loop planning. Building upon this foundation, language-conditioned methods further enhance decision-making. For instance, AutoVLA [340] improves performance to 99.1 NC and 87.6 EP by leveraging language-driven decision priors and a Best-of-N oracle scoring strategy, illustrating how language supervision can guide trajectory selection and improve long-horizon planning behavior. 

##### **5.3.4 Bench2Drive Benchmark** 

Bench2Drive [103] provides a closed-loop evaluation protocol built on CARLA V2, focusing on success rate and composite driving scores to assess goal-directed driving behavior under interactive settings. Unlike open-loop benchmarks, Bench2Drive explicitly evaluates an agent’s ability to execute long-horizon tasks and respond to dynamic environmental feedback. 

Recent VLA approaches demonstrate clear benefits from language grounding in this benchmark. For example, SimLingo [213] introduces an action dreaming mechanism that aligns natural language instructions with control sequences, achieving a leading driving score of 85.94, as reported in Table 8. These results indicate 

21 

**Table 8** Closed-loop and Open-loop performance comparison of E2E-AD Methods on the **Bench2Drive** benchmark. _•_ **Input** : : Camera, : LiDAR, : Prompt, : Instruct., : Scene Descrip., : Status, : Rule, : Context. _•_ **Action** : <u>LH:</u> Language Head, <u>RL:</u> Policy with Reinforcement Learning, <u>REG:</u> Decoder + MLP, <u>SEL:</u> Trajectory Selection w/ Cost, and <u>GEN:</u> Trajectory Generation w/ Generative Model. _•_ **Evaluation Metrics** : DS <u>(</u> _<u>↑</u>_ <u>):</u> Driving Score, SR <u>(</u> _<u>↑</u>_ <u>):</u> Success Rate. Avg. L2 <u>(</u> _<u>↓</u>_ <u>):</u> Averaged L2 distance of trajectory. 

|**Method**|**Year**|**Input**|**Vision**|**Language**|**Action**||**Cl**|**osed-Loop**||**Open-Loop**|
|---|---|---|---|---|---|---|---|---|---|---|
|||||||DS_↑_|SR(%)_↑_|Efficiency_↑_|Comfort_↑_|Avg. L2 _↓_|
|_•_ **Vision-Action Models**|||||||||||
|TCP [272]|2022||ResNet|-|REG|40.70|15.00|54.26|47.80|1.70|
|ThinkTwice [102]|2023||ResNet|-|REG|62.44|31.23|69.33|16.22|0.95|
|DriveAdapter [101]|2023||ResNet|-|REG|64.22|33.08|70.22|16.01|1.01|
|UniAD-Base [93]|2023||ResNet|-|REG|45.81|16.36|129.21|43.58|0.73|
|VAD [107]|2023||ResNet|-|REG|42.35|15.00|157.94|46.01|0.91|
|GenAD [332]|2024||ResNet|-|GEN|44.81|15.90|-|-|-|
|DriveTransformer [104]|2025||ResNet|-|REG|63.46|35.01|100.64|20.78|0.62|
|ETA [78]|2025||CLIP|-|REG|69.53|38.64|184.51|28.43|-|
|WoTE [144]|2025||ResNet|-|SEL|61.71|31.36|-|-|-|
|GuideFlow [161]|2025||ResNet|-|GEN|75.21|51.36|-|-|-|
|Raw2Drive [300]|2025||ResNet|-|RL|71.36|50.24|214.17|22.42|-|
|_•_ **Vision-Language-Action**|**Models**||||||||||
|ORION [66]|2025||EVA-02|Vicuna-1.5|GEN|77.74|54.62|151.48|17.38|0.68|
|AutoVLA [340]|2025||SigLIP|Qwen2.5-VL|LH|78.84|57.73|146.93|39.33|-|
|SimLingo-Base [213]|2025||InternViT|Qwen2|REG|85.94|66.82|244.18|25.49|-|
|SimLingo [213]|2025||InternViT|Qwen2|REG|85.07|67.27|259.23|33.67|-|
|ReAL-AD [175]|2025||ResNet|QwenVL|REG|40.76|10.93|-|-|0.87|
|ReasonPlan [168]|2025||SigLIP|Qwen|LH|64.01|34.55|180.64|25.63|0.61|
|DriveMoE [299]|2025||BEV Encoder|LLaMA|REG|74.22|48.64|175.96|15.31|0.31|
|VDRive[76]|2025||Qwen2.5-VL, CVQ|InternVL3|GEN|66.15|50.51|110.23|22.90|0.55|
|CoReVLA [60]|2025||Qwen2.5-VL|Qwen2.5-VL|LH|72.18|50.00|145.41|34.35|-|


that language-guided reasoning can effectively influence closed-loop decision-making and improve planning performance in interactive driving scenarios. 

Taken together with open-loop benchmarks, Bench2Drive highlights the growing importance of language–action alignment in VLA systems, particularly for interpreting high-level goals, guiding long-horizon behavior, and adapting actions under complex, human-centered instructions. 

## **6 Challenges & Future Directions** 

VLA models mark a shift from modular stacks toward holistic, reasoning-driven driving agents. By leveraging large multimodal backbones, they promise richer environmental understanding, stronger generalization, and more interpretable decision-making. Yet, realizing their full potential in safety-critical autonomous driving requires addressing several fundamental challenges. In parallel, emerging research directions point toward next-generation systems that are more efficient, trustworthy, and capable of long-horizon reasoning. 

#### **6.1 Current Challenges** 

##### **6.1.1 Model Architecture and System Efficiency** 

**Real-Time Processing and Latency.** VLA models inherit the substantial computational footprint of modern vision-language backbones. High-resolution, high-frame-rate camera inputs generate long visual-token sequences, and multi-view fusion amplifies memory and latency costs. Meeting the strict real-time constraints of autonomous vehicles, therefore, remains difficult [268, 273]. Recent advances in streaming token compression and adaptive visual encoders [18, 138] offer promising directions, but achieving sub-50ms inference remains an unmet requirement for safety-critical deployment. 

**Lack of Domain-Specific Foundation Models.** General-purpose VLMs [5, 34, 343] provide strong priors but are not optimized for driving-specific perception, physics, or multi-sensor fusion. Autonomous driving requires precise spatial reasoning, adherence to traffic rules, and an understanding of rare, high-stakes edge cases – abilities not fully captured by generic models. As highlighted in Section 3, dedicated driving foundation models [151] remain a missing cornerstone for scalable and dependable VLA systems. 

22 


**Figure 7** Visualization examples of the AutoVLA [340] reasoning/planning results on WOD-E2E [283] dataset. 

23 

##### **6.1.2 Data and Generalization** 

**Generalizing to Rare and Novel Scenarios.** One motivation for VLAs is their ability to leverage strong visual-language priors to interpret complex scenes. However, while VLM components may generalize well perceptually, aligning this understanding to the action space introduces new uncertainties. As noted in Section 4, reasoning-rich representations do not automatically translate to robust action generation. Longtailed scenarios – misbehaving traffic agents, unusual road layouts, unpredictable weather – remain failure points [48, 73, 247, 302, 311]. 

**Cost of High-Quality Data.** VLAs rely on diverse, high-quality multimodal datasets [131, 162], yet collecting paired vision-action-language triplets at scale is expensive. Synthetic environments [21, 191, 228] help, but face substantial sim-to-real gaps, with discrepancies in noise characteristics, lighting, and behavior of other agents [121, 275]. Improving data efficiency and mitigating distribution shifts remain long-standing challenges. 

##### **6.1.3 Core Capabilities and Trustworthiness** 

**Interpretability & Hallucination.** While VLA models produce natural-language rationales via chain-of-thought prompting [66, 261, 340], these explanations are generated artifacts – not faithful reflections of the underlying causal reasoning. Language hallucination [94, 158, 211] presents new risks: the model may justify an incorrect decision with a confident but spurious narrative. Ensuring consistent grounding between perceptions, actions, and explanations is an open challenge. 

**Long-Horizon Temporal Coherence.** Driving depends on anticipating multi-stage interactions and maintaining situational awareness across extended time horizons [199, 229, 285]. Current transformer-based VLA architectures remain constrained by limited context windows and short-term conditioning, inherited from standard VLM designs. Temporal fragmentation leads to inconsistent decisions, especially in multi-agent or highly dynamic traffic scenes. 

#### **6.2 Future Directions** 

##### **6.2.1 Next-Generation Model Paradigms** 

**Unified Vision-Language-World Models.** A promising evolution integrates VLA with predictive world models [8, 20, 142, 143], extending the VA-based models in Section 3.2. Rather than reacting frame by frame, such systems simulate future scene evolution conditioned on candidate actions, enabling proactive planning and more reliable behavior under uncertainty. Building unified, end-to-end world models that jointly reason about perception, language, and dynamics may form the backbone of next-generation autonomous agents. 

**Richer Multimodal Fusion.** As sensor suites diversify, future architectures will incorporate early and tight fusion of LiDAR, Radar, event cameras, and high-definition maps [121, 222, 275]. Language enhances semantic grounding, but robust 3D geometry is indispensable for safe decision-making [166, 248]. Holistic multimodal fusion can combine the interpretability of VLMs with the spatial precision of geometric sensors. 

##### **6.2.2 Advancing Intelligence and Adaptation** 

**Socially Aware, Knowledge-Grounded Driving.** VLA models must acquire deeper commonsense reasoning – understanding intent, conventions, and causal relationships beyond explicit annotations [139, 313]. Future efforts will draw from large-scale video-language corpora, leveraging external knowledge bases and structured reasoning modules to support socially compliant and anticipatory driving. 

**Continual & Onboard Learning.** Static, offline-trained models cannot capture evolving road infrastructures or regional driving customs [19, 255, 344]. Enabling safe, incremental learning from everyday driving, while avoiding catastrophic forgetting and ensuring safety guarantees, is essential for long-term deployment. This relates closely to addressing long-tail generalization gaps. 

24 

**Table 9** Summary of the evaluation metrics used for evaluating the **trajectory-based** and **text-based** action outputs. 

|**Abbr.**|**-**|**Full Name**|**Description**|**Ref.**|
|---|---|---|---|---|
|**Action-Planni**|**ng Op**|**en-Loop Evaluation**|||
|<br>L2|<br>_↓_|<br>L2 Error|L2 distance error between the planned trajectory and the human<br>driving trajectory in 3 seconds.|[91]|
|CR|_↓_|Collision Rate|How often the self-driving vehicle would collide with other agents<br>on the road.|[91]|
|ADE|_↓_|Average<br>Displacement Error|Mean displacement error between predicted trajectories and ex-<br>pert waypoints across the horizon, reflecting overall trajectory<br>accuracy.|[93]|
|FDE|_↓_|Final Displacement<br>Error|Displacement error at the final predicted waypoint compared<br>with expert trajectories, emphasizing long-term accuracy.|[93]|
|MR|_↓_|Miss Rate|Fraction of prediction time steps where displacement error ex-<br>ceeds horizon-specific thresholds, reflecting failure in trajectory<br>coverage.|[93]|
|AHE|_↓_|Average Heading<br>Error|Mean absolute angular deviation between predicted and expert<br>heading over the trajectory horizon, measuring orientation accu-<br>racy.|[114]|
|FHE|_↓_|Final Heading<br>Error|Absolute angular deviation of predicted heading from expert at<br>the final timestep, reflecting terminal orientation accuracy.|[114]|
|SLE|_↓_|Speed L1 Error|Mean absolute error of predicted speed control signals.|[100]|
|SALE|_↓_|Steer Angle L1<br>Error|Mean absolute error of predicted steering angle control signals.|[100]|
|RFS|_↑_|Rater Feedback<br>|Measure how well the predicted trajectory aligns with human<br>driving preferences by checking whether it falls within trust|[283]|
|||Score|regions.||
|**Trajectory-Ba**|**sed C**|**losed-Loop Evaluation**|||
|RC|_↑_|Route Completion|The percentage of route distance completed.|[206]|
|DS|_↑_|Driving Score|RC weighted by a penalty factor that accounts for collisions with<br>pedestrians, vehicles, etc.|[206]|
|NC|_↑_|No Collision|Fraction of scenarios without ego-fault collisions, focusing exclu-<br>sively on responsibility-aware collision evaluation.|[47]|
|DAC|_↑_|Driving<br>Admissibility Check|Boolean evaluation that checks whether the ego vehicle remains<br>inside drivable polygons throughout the rollout.|[47]|
|TTC|_↑_|Time To Collision|Boolean verification that the time-to-collision value exceeds safety<br>thresholds, preventing imminent crashes.|[47]|
|C|_↑_|Driving Comfort|The comfort of driving.|[47]|
|EP|_↑_|Ego Progress|Penalization of excessive jerk, acceleration, or yaw-rate, reflecting<br>ride quality and passenger comfort.|[47]|
|PDMS|_↑_|Predictive Driver<br>Model Score|A flexible weighted evaluation score in autonomous driving that<br>aggregates multiple safety, progress, and comfort subscores into<br>a single metric.|[47]|
|SR|_↑_|Success Rate|Percentage of navigation episodes that successfully reach the goal<br>within a fixed time budget, indicating overall task completion.|[56]|
|ID|_↑_|Infraction Distance|Average driving distance between two infractions, with longer<br>distances reflecting safer and more reliable policy behavior.|[56]|
|**Text-Based A**|**ction**|**Evaluation**<br>Cbd|||
|CIDEr|_↑_|onsensus-ase<br>Image Description<br>Evaluation|Measures similarity of generated captions to multiple human<br>references using TF-IDF weighted n-grams.|[182]|
|BLEU|_↑_|Bilingual<br>Evaluation<br>Understudy|Precision-based metric that compares n-grams of the generated<br>text against reference texts.|[182]|
|METEOR|_↑_|Metric for<br>Evaluation of<br>Translation with<br>Explicit Ordering|Considers unigram precision and recall with stemming, synonym<br>matching, and fragmentation penalty.|[182]|
|Rouge|_↑_|Recall-Oriented<br>Understudy for<br>Gisting Evaluation|Recall-focused metric using overlapping n-grams, word sequences,<br>or word pairs between generated and reference texts.|[182]|
|Top-1<br>Acc|_↑_|Visual Question<br>Answering Top-1<br>Accuracy|Percentage of predictions where the most confident output<br>matches the ground truth label.|[182]|


25 

##### **6.2.3 Ecosystem for Safe Deployment** 

**Standardized Evaluation & Safety Guarantees.** Evaluation metrics from current benchmarks, _e.g._ , NAVSIM [47] and Bench2Drive [103], assess safety and comfort but do not capture key VLA-specific risks such as reasoning failures, instruction-following errors, or cross-modal inconsistencies [158, 211]. Future benchmarks should evaluate multi-step instruction execution, robustness to ambiguous language, and resistance to hallucination. Beyond empirical testing, formal verification tools are needed to provide theoretical guarantees for safety-critical behaviors. 

**Human-Centric Interaction & Personalization.** VLA systems open the door to richer in-car interaction [219, 295]. Natural language enables drivers to specify goals, constraints, and preferences (“ _drive cautiously_ ”, “ _avoid unprotected left turns_ ”). Personalization modules [81] can adapt driving styles to different users, enhancing comfort and trust. The challenge lies in balancing personalization with strict safety and regulatory requirements. 

## **7 Conclusion** 

Vision-Language-Action models are reshaping autonomous driving by coupling perception with high-level reasoning and natural language understanding. This work formalizes the VLA problem setting, outlines the progression from traditional VA pipelines, and organizes existing methods into coherent architectural families together with the datasets and benchmarks that support their development. VLA systems offer clear advantages in interpretability, generalization, and human interaction, but core challenges remain: aligning symbolic reasoning with continuous control, ensuring robustness in long-tail scenarios, and establishing evaluation protocols that faithfully measure instruction following and safety. Progress will depend on advances in efficient architectures, deeper multimodal fusion, world-model-driven planning, and more rigorous humancentered testing. Overall, VLA represents a promising direction for building autonomous agents that are not only competent drivers but also communicative, transparent, and responsive to human intent. 

## **References** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, Red Avila, Igor Babuschkin, Suchir Balaji, Valerie Balcom, Paul Baltescu, Haiming Bao, Mohammad Bavarian, Jeff Belgum, Irwan Bello, Jake Berdine, Gabriel Bernadett-Shapiro, Christopher Berner, Lenny Bogdonoff, Oleg Boiko, Madelaine Boyd, Anna-Luisa Brakman, Greg Brockman, Tim Brooks, Miles Brundage, Kevin Button, Trevor Cai, Rosie Campbell, Andrew Cann, Brittany Carey, Chelsea Carlson, Rory Carmichael, Brooke Chan, Che Chang, Fotis Chantzis, Derek Chen, Sully Chen, Ruby Chen, Jason Chen, Mark Chen, Ben Chess, Chester Cho, Casey Chu, Hyung Won Chung, Dave Cummings, Jeremiah Currier, Yunxing Dai, Cory Decareaux, Thomas Degry, Noah Deutsch, Damien Deville, Arka Dhar, David Dohan, Steve Dowling, Sheila Dunning, Adrien Ecoffet, Atty Eleti, Tyna Eloundou, David Farhi, Liam Fedus, Niko Felix, Simón Posada Fishman, Juston Forte, Isabella Fulford, Leo Gao, Elie Georges, Christian Gibson, Vik Goel, Tarun Gogineni, Gabriel Goh, Rapha Gontijo-Lopes, Jonathan Gordon, Morgan Grafstein, Scott Gray, Ryan Greene, Joshua Gross, Shixiang Shane Gu, Yufei Guo, Chris Hallacy, Jesse Han, Jeff Harris, Yuchen He, Mike Heaton, Johannes Heidecke, Chris Hesse, Alan Hickey, Wade Hickey, Peter Hoeschele, Brandon Houghton, Kenny Hsu, Shengli Hu, Xin Hu, Joost Huizinga, Shantanu Jain, Shawn Jain, et al. GPT-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- [2] Hidehisa Arai, Keita Miwa, Kento Sasaki, Kohei Watanabe, Yu Yamaguchi, Shunsuke Aoki, and Issei Yamamoto. CoVLA: Comprehensive vision-language-action dataset for autonomous driving. In _IEEE/CVF Winter Conf. Appl. Comput. Vis._ , pages 1933–1943, 2025. 

- [3] Alisson Azzolini, Junjie Bai, Hannah Brandon, Jiaxin Cao, Prithvijit Chattopadhyay, Huayu Chen, Jinju Chu, Yin Cui, Jenna Diamond, Yifan Ding, Liang Feng, Francesco Ferroni, Rama Govindaraju, Jinwei Gu, Siddharth Gururani, Imad El Hanafi, Zekun Hao, Jacob Huffman, Jingyi Jin, Brendan Johnson, Rizwan Khan, George Kurian, Elena Lantz, Nayeon Lee, Zhaoshuo Li, Xuan Li, Maosheng Liao, Tsung-Yi Lin, Yen-Chen Lin, Ming-Yu Liu, Xiangyu Lu, Alice Luo, Andrew Mathau, Yun Ni, Lindsey Pavao, Wei Ping, David W. Romero, Misha Smelyanskiy, Shuran Song, Lyne Tchapmi, Andrew Z. Wang, Boxin Wang, Haoxiang Wang, Fangyin Wei, Jiashu 

26 

Xu, Yao Xu, Dinghao Yang, Xiaodong Yang, Zhuolin Yang, Jingxu Zhang, Xiaohui Zeng, and Zhe Zhang. Cosmos-Reason1: From physical common sense to embodied reasoning. _arXiv preprint arXiv:2503.15558_ , 2025. 

- [4] Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei Huang, Binyuan Hui, Luo Ji, Mei Li, Junyang Lin, Runji Lin, Dayiheng Liu, Gao Liu, Chengqiang Lu, Keming Lu, Jianxin Ma, Rui Men, Xingzhang Ren, Xuancheng Ren, Chuanqi Tan, Sinan Tan, Jianhong Tu, Peng Wang, Shijie Wang, Wei Wang, Shengguang Wu, Benfeng Xu, Jin Xu, An Yang, Hao Yang, Jian Yang, Shusheng Yang, Yang Yao, Bowen Yu, Hongyi Yuan, Zheng Yuan, Jianwei Zhang, Xingxuan Zhang, Yichang Zhang, Zhenru Zhang, Chang Zhou, Jingren Zhou, Xiaohuan Zhou, and Tianhang Zhu. Qwen technical report. _arXiv preprint arXiv:2309.16609_ , 2023. 

- [5] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhaohai Li, Jianqiang Wan, Pengfei Wang, Wei Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng, Hang Zhang, Zhibo Yang, Haiyang Xu, Junyang Lin, et al. Qwen2.5-VL technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 

- [6] Michael Bain and Claude Sammut. A framework for behavioural cloning. In _Mach. intell._ , volume 15, pages 103–129, 1995. 

- [7] Federico Baldassarre, Marc Szafraniec, Basile Terver, Vasil Khalidov, Francisco Massa, Yann LeCun, Patrick Labatut, Maximilian Seitzer, and Piotr Bojanowski. Back to the features: DINO as a foundation for video world models. _arXiv preprint arXiv:2507.19468_ , 2025. 

- [8] Philip J. Ball, Jakob Bauer, Frank Belletti, Bethanie Brownfield, Ariel Ephrat, Shlomi Fruchter, Agrim Gupta, Kristian Holsheimer, Aleksander Holynski, Jiri Hron, Christos Kaplanis, Marjorie Limont, Matt McGill, Yanko Oliveira, Jack Parker-Holder, Frank Perbet, Guy Scully, Jeremy Shar, Stephen Spencer, Omer Tov, Ruben Villegas, Emma Wang, Jessica Yung, Cip Baetu, Jordi Berbel, David Bridson, Jake Bruce, Gavin Buttimore, Sarah Chakera, Bilva Chandra, Paul Collins, Alex Cullum, Bogdan Damoc, Vibha Dasagi, Maxime Gazeau, Charles Gbadamosi, Woohyun Han, Ed Hirst, Ashyana Kachra, Lucie Kerley, Kristian Kjems, Eva Knoepfel, Vika Koriakin, Jessica Lo, Cong Lu, Zeb Mehring, Alex Moufarek, Henna Nandwani, Valeria Oliveira, Fabio Pardo, Jane Park, Andrew Pierson, Ben Poole, Helen Ran, Tim Salimans, Manuel Sanchez, Igor Saprykin, Amy Shen, Sailesh Sidhwani, Duncan Smith, Joe Stanton, Hamish Tomlinson, Dimple Vijaykumar, Luyu Wang, Piers Wingfield, Nat Wong, Keyang Xu, Christopher Yew, Nick Young, Vadim Zubov, Douglas Eck, Dumitru Erhan, Koray Kavukcuoglu, Demis Hassabis, Zoubin Gharamani, Raia Hadsell, Aäron van den Oord, Inbar Mosseri, Adrian Bolton, Satinder Singh, and Tim Rocktäschel. Genie 3: A new frontier for world models, 2025. URL https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/. 

- [9] Mayank Bansal, Alex Krizhevsky, and Abhijit Ogale. ChauffeurNet: Learning to drive by imitating the best and synthesizing the worst. _arXiv preprint arXiv:1812.03079_ , 2018. 

- [10] Florent Bartoccioni, Elias Ramzi, Victor Besnier, Shashanka Venkataramanan, Tuan-Hung Vu, Yihong Xu, Loick Chambon, Spyros Gidaris, Serkan Odabas, David Hurych, Renaud Marlet, Alexandre Boulch, Mickael Chen, Éloi Zablocki, Andrei Bursuc, Eduardo Valle, and Matthieu Cord. VaViM and VaVAM: Autonomous driving through video generative modeling. _arXiv preprint arXiv:2502.15672_ , 2025. 

- [11] Lucas Beyer, Andreas Steiner, André Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, Thomas Unterthiner, Daniel Keysers, Skanda Koppula, Fangyu Liu, Adam Grycner, Alexey Gritsenko, Neil Houlsby, Manoj Kumar, Keran Rong, Julian Eisenschlos, Rishabh Kabra, Matthias Bauer, Matko Bošnjak, Xi Chen, Matthias Minderer, Paul Voigtlaender, Ioana Bica, Ivana Balazevic, Joan Puigcerver, Pinelopi Papalampidi, Olivier Henaff, Xi Xiong, Radu Soricut, Jeremiah Harmsen, and Xiaohua Zhai. PaliGemma: A versatile 3B VLM for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- [12] Hengwei Bian, Lingdong Kong, Haozhe Xie, Liang Pan, Yu Qiao, and Ziwei Liu. DynamicCity: Large-scale 4D occupancy generation from dynamic scenes. In _Int. Conf. Learn. Represent._ , 2025. 

- [13] Andreas Blattmann, Tim Dockhorn, Sumith Kulal, Daniel Mendelevitch, Maciej Kilian, Dominik Lorenz, Yam Levi, Zion English, Vikram Voleti, Adam Letts, Varun Jampani, and Robin Rombach. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_ , 2023. 

- [14] Andreas Blattmann, Robin Rombach, Huan Ling, Tim Dockhorn, Seung Wook Kim, Sanja Fidler, and Karsten Kreis. Align your latents: High-resolution video synthesis with latent diffusion models. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 22563–22575, 2023. 

27 

- [15] Mariusz Bojarski, Davide Del Testa, Daniel Dworakowski, Bernhard Firner, Beat Flepp, Prasoon Goyal, Lawrence D. Jackel, Mathew Monfort, Urs Muller, Jiakai Zhang, Xin Zhang, Jake Zhao, and Karol Zieba. End-to-end learning for self-driving cars. _arXiv preprint arXiv:1604.07316_ , 2016. 

- [16] Holger Caesar, Varun Bankiti, Alex H. Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuScenes: A multimodal dataset for autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 11621–11631, 2020. 

- [17] Holger Caesar, Juraj Kabzan, Kok Seang Tan, Whye Kit Fong, Eric Wolff, Alex Lang, Luke Fletcher, Oscar Beijbom, and Sammy Omari. nuPlan: A closed-loop ML-based planning benchmark for autonomous vehicles. _arXiv preprint arXiv:2106.11810_ , 2021. 

- [18] Jiajun Cao, Qizhe Zhang, Peidong Jia, Xuhui Zhao, Bo Lan, Xiaoan Zhang, Zhuo Li, Xiaobao Wei, Sixiang Chen, Liyun Li, Xianming Liu, Ming Lu, Yang Wang, and Shanghang Zhang. FastDriveVLA: Efficient end-to-end driving via plug-and-play reconstruction-based token pruning. _arXiv preprint arXiv:2507.23318_ , 2025. 

- [19] Zhong Cao, Xiang Li, Kun Jiang, Weitao Zhou, Xiaoyu Liu, Nanshan Deng, and Diange Yang. Autonomous driving policy continual learning with one-shot disengagement case. _IEEE Trans. Intell. Veh._ , 8(2):1380–1391, 2022. 

- [20] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, Deli Zhao, and Hao Chen. WorldVLA: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 

- [21] Qianwen Chao, Huikun Bi, Weizi Li, Tianlu Mao, Zhaoqi Wang, Ming C. Lin, and Zhigang Deng. A survey on visual traffic simulation: Models, evaluations, and applications in autonomous driving. In _Computer Graphics Forum_ , volume 39, pages 287–308. Wiley Online Library, 2020. 

- [22] Raphael Chekroun, Marin Toromanoff, Sascha Hornauer, and Fabien Moutarde. GRI: General reinforced imitation and its application to vision-based autonomous driving. _Robotics_ , 12(5):127, 2023. 

- [23] Dian Chen and Philipp Krähenbühl. Learning from all vehicles. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 17222–17231, 2022. 

- [24] Dian Chen, Brady Zhou, Vladlen Koltun, and Philipp Krähenbühl. Learning by cheating. In _Conf. Robot Learn._ , pages 66–75. PMLR, 2020. 

- [25] Dian Chen, Vladlen Koltun, and Philipp Krähenbühl. Learning to drive from a world on rails. In _IEEE/CVF Int. Conf. Comput. Vis._ , pages 15590–15599, 2021. 

- [26] Junyu Chen, Dongyun Zou, Wenkun He, Junsong Chen, Enze Xie, Song Han, and Han Cai. DC-AE 1.5: Accelerating diffusion model convergence with structured latent space. In _IEEE/CVF Int. Conf. Comput. Vis._ , pages 19628–19637, 2025. 

- [27] Li Chen, Penghao Wu, Kashyap Chitta, Bernhard Jaeger, Andreas Geiger, and Hongyang Li. End-to-end autonomous driving: Challenges and frontiers. _IEEE Trans. Pattern Anal. Mach. Intell._ , 46(12):10164–10183, 2024. 

- [28] Runnan Chen, Youquan Liu, Lingdong Kong, Nenglun Chen, Xinge Zhu, Yuexin Ma, Tongliang Liu, and Wenping Wang. Towards label-free scene understanding by vision foundation models. In _Adv. Neural Inf. Process. Syst._ , volume 36, pages 75896–75910, 2023. 

- [29] Runnan Chen, Youquan Liu, Lingdong Kong, Xinge Zhu, Yuexin Ma, Yikang Li, Yuenan Hou, Yu Qiao, and Wenping Wang. CLIP2Scene: Towards label-efficient 3D scene understanding by CLIP. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 7020–7030, 2023. 

- [30] Shaoyu Chen, Bo Jiang, Hao Gao, Bencheng Liao, Qing Xu, Qian Zhang, Chang Huang, Wenyu Liu, and Xinggang Wang. VADv2: End-to-end vectorized autonomous driving via probabilistic planning. _arXiv preprint arXiv:2402.13243_ , 2024. 

- [31] Xi Chen, Xiao Wang, Lucas Beyer, Alexander Kolesnikov, Jialin Wu, Paul Voigtlaender, Basil Mustafa, Sebastian Goodman, Ibrahim Alabdulmohsin, Piotr Padlewski, Daniel Salz, Xi Xiong, Daniel Vlasic, Filip Pavetic, Keran Rong, Tianli Yu, Daniel Keysers, Xiaohua Zhai, and Radu Soricut. PaLI-3 vision language models: Smaller, faster, stronger. _arXiv preprint arXiv:2310.09199_ , 2023. 

28 

- [32] Xuesong Chen, Linjiang Huang, Tao Ma, Rongyao Fang, Shaoshuai Shi, and Hongsheng Li. SOLVE: Synergy of language-vision and end-to-end networks for autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 12068–12077, 2025. 

- [33] Yuntao Chen, Yuqi Wang, and Zhaoxiang Zhang. DrivingGPT: Unifying driving world modeling and planning with multi-modal autoregressive transformers. _arXiv preprint arXiv:2412.18607_ , 2024. 

- [34] Zhe Chen, Jiannan Wu, Wenhai Wang, Weijie Su, Guo Chen, Sen Xing, Muyan Zhong, Qinglong Zhang, Xizhou Zhu, Lewei Lu, Bin Li, Ping Luo, Tong Lu, Yu Qiao, and Jifeng Dai. InternVL: Scaling up vision foundation models and aligning for generic visual-linguistic tasks. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 24185–24198, 2024. 

- [35] Haohan Chi, Huan ang Gao, Ziming Liu, Jianing Liu, Chenyu Liu, Jinwei Li, Kaisen Yang, Yangcheng Yu, Zeda Wang, Wenyi Li, Leichen Wang, Xingtao Hu, Hao Sun, Hang Zhao, and Hao Zhao. Impromptu VLA: Open weights and open data for driving vision-language-action models. _arXiv preprint arXiv:2505.23757_ , 2025. 

- [36] Wei-Lin Chiang et al. Vicuna: An open-source chatbot impressing GPT-4 with 90%* ChatGPT quality, 2023. URL https://vicuna.lmsys.org. 

- [37] Pranav Singh Chib and Pravendra Singh. Recent advancements in end-to-end autonomous driving using deep learning: A survey. _IEEE Trans. Intell. Veh._ , 9(1):103–118, 2023. 

- [38] Kashyap Chitta, Aditya Prakash, and Andreas Geiger. NEAT: Neural attention fields for end-to-end autonomous driving. In _IEEE/CVF Int. Conf. Comput. Vis._ , pages 15793–15803, 2021. 

- [39] Kashyap Chitta, Aditya Prakash, Bernhard Jaeger, Zehao Yu, Katrin Renz, and Andreas Geiger. TransFuser: Imitation with transformer-based sensor fusion for autonomous driving. _IEEE Trans. Pattern Anal. Mach. Intell._ , 45(11):12878–12895, 2022. 

- [40] Xiangxiang Chu, Limeng Qiao, Xinyu Zhang, Shuang Xu, Fei Wei, Yang Yang, Xiaofei Sun, Yiming Hu, Xinyang Lin, Bo Zhang, and Chunhua Shen. MobileVLM v2: Faster and stronger baseline for vision language model. _arXiv preprint arXiv:2402.03766_ , 2024. 

- [41] Karl Cobbe, Chris Hesse, Jacob Hilton, and John Schulman. Leveraging procedural generation to benchmark reinforcement learning. In _Int. Conf. Mach. Learn._ , pages 2048–2056. PMLR, 2020. 

- [42] Felipe Codevilla, Matthias Müller, Antonio López, Vladlen Koltun, and Alexey Dosovitskiy. End-to-end driving via conditional imitation learning. In _IEEE Int. Conf. Robot. Autom._ , pages 4693–4700, 2018. 

- [43] Felipe Codevilla, Eder Santana, Antonio M. Lopez, and Adrien Gaidon. Exploring the limitations of behavior cloning for autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 9329–9338, 2019. 

- [44] Can Cui, Yunsheng Ma, Xu Cao, Wenqian Ye, Yang Zhou, Kaizhao Liang, Jintai Chen, Juanwu Lu, Zichong Yang, Kuei-Da Liao, Tianren Gao, Erlong Li, Kun Tang, Zhipeng Cao, Tong Zhou, Ao Liu, Xinrui Yan, Shuqi Mei, Jianguo Cao, Ziran Wang, and Chao Zheng. A survey on multimodal large language models for autonomous driving. In _IEEE/CVF Winter Conf. Appl. Comput. Vis._ , pages 958–979, 2024. 

- [45] Can Cui, Yupeng Zhou, Juntong Peng, Sung-Yeon Park, Zichong Yang, Prashanth Sankaranarayanan, Jiaru Zhang, Ruqi Zhang, and Ziran Wang. ViLaD: A large vision language diffusion framework for end-to-end autonomous driving. _arXiv preprint arXiv:2508.12603_ , 2025. 

- [46] Erfei Cui, Wenhai Wang, Zhiqi Li, Jiangwei Xie, Haoming Zou, Hanming Deng, Gen Luo, Lewei Lu, Xizhou Zhu, and Jifeng Dai. DriveMLM: Aligning multi-modal large language models with behavioral planning states for autonomous driving. _arXiv preprint arXiv:2312.09245_ , 2023. 

- [47] Daniel Dauner, Marcel Hallgarten, Tianyu Li, Xinshuo Weng, Zhiyu Huang, Zetong Yang, Hongyang Li, Igor Gilitschenski, Boris Ivanovic, Marco Pavone, Andreas Geiger, and Kashyap Chitta. NAVSIM: Data-driven non-reactive autonomous vehicle simulation and benchmarking. In _Adv. Neural Inf. Process. Syst._ , volume 37, pages 28706–28719, 2024. 

- [48] Cainan Davidson, Deva Ramanan, and Neehar Peri. RefAV: Towards planning-centric scenario mining. _arXiv preprint arXiv:2505.20981_ , 2025. 

- [49] Pim De Haan, Dinesh Jayaraman, and Sergey Levine. Causal confusion in imitation learning. In _Adv. Neural Inf. Process. Syst._ , volume 32, pages 11698–11709, 2019. 

29 

- [50] Thierry Deruyttere, Simon Vandenhende, Dusan Grujicic, Luc Van Gool, and Marie-Francine Moens. Talk2Car: Taking control of your self-driving car. In _Conf. Empirical Methods Natural Lang. Process._ , pages 2088–2098, 2019. 

- [51] Thierry Deruyttere, Dusan Grujicic, Matthew B. Blaschko, and Marie-Francine Moens. Talk2Car: Predicting physical trajectories for natural language commands. _IEEE Access_ , 10:123809–123834, 2022. 

- [52] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. BERT: Pre-training of deep bidirectional transformers for language understanding. _arXiv preprint arXiv:1810.04805_ , 2018. 

- [53] Jingtao Ding, Yunke Zhang, Yu Shang, Jie Feng, Yuheng Zhang, Zefang Zong, Yuan Yuan, Hongyuan Su, Nian Li, Jinghua Piao, Yucheng Deng, Nicholas Sukiennik, Chen Gao, Fengli Xu, and Yong Li. Understanding world or predicting future? a comprehensive survey of world models. _ACM Comput. Surveys_ , 2024. 

- [54] Xinpeng Ding, Jianhua Han, Hang Xu, Xiaodan Liang, Wei Zhang, and Xiaomeng Li. Holistic autonomous driving understanding by bird’s-eye-view injected multi-modal large models. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 13668–13677, 2024. 

- [55] Nemanja Djuric, Vladan Radosavljevic, Henggang Cui, Thi Nguyen, Fang-Chieh Chou, Tsung-Han Lin, NITIN SINGH, and Jeff Schneider. Uncertainty-aware short-term motion prediction of traffic actors for autonomous driving. In _IEEE/CVF Winter Conf. Appl. Comput. Vis._ , pages 2095–2104, 2020. 

- [56] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. CARLA: An open urban driving simulator. In _Conf. Robot Learn._ , pages 1–16. PMLR, 2017. 

- [57] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, and Neil Houlsby. An image is worth 16x16 words: Transformers for image recognition at scale. In _Int. Conf. Learn. Represent._ , 2021. 

- [58] Patrick Esser, Robin Rombach, and Bjorn Ommer. Taming transformers for high-resolution image synthesis. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 12873–12883, 2021. 

- [59] Scott Ettinger, Shuyang Cheng, Benjamin Caine, Chenxi Liu, Hang Zhao, Sabeek Pradhan, Yuning Chai, Ben Sapp, Charles R. Qi, Yin Zhou, Zoey Yang, Aurélien Chouard, Pei Sun, Jiquan Ngiam, Vijay Vasudevan, Alexander McCauley, Jonathon Shlens, and Dragomir Anguelov. Large scale interactive motion forecasting for autonomous driving: The Waymo Open Motion dataset. In _IEEE/CVF Int. Conf. Comput. Vis._ , pages 9710–9719, 2021. 

- [60] Shiyu Fang, Yiming Cui, Haoyang Liang, Chen Lv, Peng Hang, and Jian Sun. CoReVLA: A dual-stage end-to-end autonomous driving framework for long-tail scenarios via collect-and-refine. _arXiv preprint arXiv:2509.15968_ , 2025. 

- [61] Yuxin Fang, Wen Wang, Binhui Xie, Quan Sun, Ledell Wu, Xinggang Wang, Tiejun Huang, Xinlong Wang, and Yue Cao. EVA: Exploring the limits of masked visual representation learning at scale. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 19358–19369, 2023. 

- [62] Yuxin Fang, Quan Sun, Xinggang Wang, Tiejun Huang, Xinlong Wang, and Yue Cao. EVA-02: A visual representation for neon genesis. _Image and Vision Computing_ , 149:105171, 2024. 

- [63] Bowen Feng, Zhiting Mei, Baiang Li, Julian Ost, Filippo Ghilotti, Roger Girgis, Anirudha Majumdar, and Felix Heide. VERDI: VLM-embedded reasoning for autonomous driving. _arXiv preprint arXiv:2505.15925_ , 2025. 

- [64] Lan Feng, Yang Gao, Eloi Zablocki, Quanyi Li, Wuyang Li, Sichao Liu, Matthieu Cord, and Alexandre Alahi. RAP: 3D rasterization augmented end-to-end planning. _arXiv preprint arXiv:2510.04333_ , 2025. 

- [65] Daocheng Fu, Xin Li, Licheng Wen, Min Dou, Pinlong Cai, Botian Shi, and Yu Qiao. Drive like a human: Rethinking autonomous driving with large language models. In _IEEE/CVF Winter Conf. Appl. Comput. Vis. Worksh._ , pages 910–919, 2024. 

- [66] Haoyu Fu, Diankun Zhang, Zongchuang Zhao, Jianfeng Cui, Dingkang Liang, Chong Zhang, Dingyuan Zhang, Hongwei Xie, Bing Wang, and Xiang Bai. ORION: A holistic end-to-end autonomous driving framework by vision-language instructed action generation. _arXiv preprint arXiv:2503.19755_ , 2025. 

- [67] Hao Gao, Shaoyu Chen, Bo Jiang, Bencheng Liao, Yiang Shi, Xiaoyang Guo, Yuechuan Pu, Haoran Yin, Xiangyu Li, Xinbang Zhang, Ying Zhang, Wenyu Liu, Qian Zhang, and Xinggang Wang. RAD: Training an end-to-end driving policy via large-scale 3DGS-based reinforcement learning. _arXiv preprint arXiv:2502.13144_ , 2025. 

30 

- [68] Shenyuan Gao, Jiazhi Yang, Li Chen, Kashyap Chitta, Yihang Qiu, Andreas Geiger, Jun Zhang, and Hongyang Li. Vista: A generalizable driving world model with high fidelity and versatile controllability. _Adv. Neural Inf. Process. Syst._ , 37:91560–91596, 2024. 

- [69] Xiangbo Gao, Yuheng Wu, Rujia Wang, Chenxi Liu, Yang Zhou, and Zhengzhong Tu. LangCoop: Collaborative driving with language. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 4226–4237, 2025. 

- [70] Anant Garg and K Madhava Krishna. Imagine-2-Drive: Leveraging high-fidelity world models via multi-modal diffusion policies. _arXiv preprint arXiv:2411.10171_ , 2024. 

- [71] Maoning Ge, Kento Ohtani, Yingjie Niu, Yuxiao Zhang, and Kazuya Takeda. VLA-MP: A vision-language-action framework for multimodal perception and physics-constrained action generation in autonomous driving. _Sensors_ , 25(19):6163, 2025. 

- [72] Andreas Geiger, Philip Lenz, and Raquel Urtasun. Are we ready for autonomous driving? the KITTI vision benchmark suite. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 3354–3361, 2012. 

- [73] Anurag Ghosh, Shen Zheng, Robert Tamburo, Khiem Vuong, Juan Alvarez-Padilla, Hailiang Zhu, Michael Cardei, Nicholas Dunn, Christoph Mertz, and Srinivasa G. Narasimhan. ROADWork dataset: Learning to recognize, observe, analyze and drive through work zones. _arXiv preprint arXiv:2406.07661_ , 2024. 

- [74] Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, Amy Yang, Angela Fan, Anirudh Goyal, Anthony Hartshorn, Aobo Yang, Archi Mitra, Archie Sravankumar, Artem Korenev, Arthur Hinsvark, Arun Rao, Aston Zhang, Aurelien Rodriguez, Austen Gregerson, Ava Spataru, Baptiste Roziere, Bethany Biron, Binh Tang, Bobbie Chern, Charlotte Caucheteux, Chaya Nayak, Chloe Bi, Chris Marra, Chris McConnell, Christian Keller, Christophe Touret, Chunyang Wu, Corinne Wong, Cristian Canton Ferrer, Cyrus Nikolaidis, Damien Allonsius, Daniel Song, Danielle Pintz, Danny Livshits, Danny Wyatt, David Esiobu, Dhruv Choudhary, Dhruv Mahajan, Diego Garcia-Olano, Diego Perino, Dieuwke Hupkes, Egor Lakomkin, Ehab AlBadawy, Elina Lobanova, Emily Dinan, Eric Michael Smith, Filip Radenovic, Francisco Guzmán, Frank Zhang, Gabriel Synnaeve, Gabrielle Lee, Georgia Lewis Anderson, Govind Thattai, Graeme Nail, Gregoire Mialon, Guan Pang, Guillem Cucurell, Hailey Nguyen, Hannah Korevaar, Hu Xu, Hugo Touvron, Iliyan Zarov, Imanol Arrieta Ibarra, Isabel Kloumann, Ishan Misra, Ivan Evtimov, Jack Zhang, Jade Copet, Jaewon Lee, Jan Geffert, Jana Vranes, Jason Park, Jay Mahadeokar, Jeet Shah, Jelmer van der Linde, Jennifer Billock, Jenny Hong, Jenya Lee, Jeremy Fu, Jianfeng Chi, Jianyu Huang, Jiawen Liu, Jie Wang, Jiecao Yu, Joanna Bitton, Joe Spisak, Jongsoo Park, Joseph Rocca, et al. The LLaMA 3 herd of models. _arXiv preprint arXiv:2407.21783_ , 2024. 

- [75] Xingtai Gui, Jianbo Zhao, Wencheng Han, Jikai Wang, Jiahao Gong, Feiyang Tan, Cheng zhong Xu, and Jianbing Shen. TrajDiff: End-to-end autonomous driving without perception annotation. _arXiv preprint arXiv:2512.00723_ , 2025. 

- [76] Ziang Guo and Zufeng Zhang. VDRive: Leveraging reinforced VLA and diffusion policy for end-to-end autonomous driving. _arXiv preprint arXiv:2510.15446_ , 2025. 

- [77] David Ha and Jürgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2018. 

- [78] Shadi Hamdan, Chonghao Sima, Zetong Yang, Hongyang Li, and Fatma Guney. ETA: Efficiency through thinking ahead, a dual approach to self-driving with large models. In _IEEE/CVF Int. Conf. Comput. Vis._ , pages 26529–26538, 2025. 

- [79] Jianhua Han, Meng Tian, Jiangtong Zhu, Fan He, Huixin Zhang, Sitong Guo, Dechang Zhu, Hao Tang, Pei Xu, Yuze Guo, Minzhe Niu, Haojie Zhu, Qichao Dong, Xuechao Yan, Siyuan Dong, Lu Hou, Qingqiu Huang, Xiaosong Jia, and Hang Xu. Percept-WAM: Perception-enhanced world-awareness-action model for robust end-to-end autonomous driving. _arXiv preprint arXiv:2511.19221_ , 2025. 

- [80] Wencheng Han, Dongqian Guo, Cheng-Zhong Xu, and Jianbing Shen. DME-Driver: Integrating human decision logic and 3D scene perception in autonomous driving. In _AAAI Conf. Artifi. Intell._ , volume 39, pages 3347–3355, 2025. 

- [81] Ruiyang Hao, Bowen Jing, Haibao Yu, and Zaiqing Nie. StyleDrive: Towards driving-style aware benchmarking of end-to-end autonomous driving. _arXiv preprint arXiv:2506.23982_ , 2025. 

- [82] Xiaoshuai Hao, Mengchuan Wei, Yifan Yang, Haimei Zhao, Hui Zhang, Yi Zhou, Qiang Wang, Weiming Li, Lingdong Kong, and Jing Zhang. Is your HD map constructor reliable under sensor corruptions? _Adv. Neural Inf. Process. Syst._ , 37:22441–22482, 2024. 

31 

- [83] Xiaoshuai Hao, Yunfeng Diao, Mengchuan Wei, Yifan Yang, Peng Hao, Rong Yin, Hui Zhang, Weiming Li, Shu Zhao, and Yu Liu. MapFusion: A novel BEV feature fusion network for multi-modal map construction. _Information Fusion_ , 119:103018, 2025. 

- [84] Xiaoshuai Hao, Lingdong Kong, Rong Yin, Pengwei Wang, Jing Zhang, Yunfeng Diao, and Shu Zhao. SafeMap: Robust HD map construction from incomplete observations. In _Int. Conf. Mach. Learn._ , pages 22091–22102. PMLR, 2025. 

- [85] Xiaoshuai Hao, Guanqun Liu, Yuting Zhao, Yuheng Ji, Mengchuan Wei, Haimei Zhao, Lingdong Kong, Rong Yin, and Yu Liu. MSC-Bench: Benchmarking and analyzing multi-sensor corruption for driving perception. _arXiv preprint arXiv:2501.01037_ , 2025. 

- [86] Yuhan Hao, Zhengning Li, Lei Sun, Weilong Wang, Naixin Yi, Sheng Song, Caihong Qin, Mofan Zhou, Yifei Zhan, and Xianpeng Lang. DriveAction: A benchmark for exploring human-like driving decisions in VLA models. _arXiv preprint arXiv:2506.05667_ , 2025. 

- [87] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 770–778, 2016. 

- [88] Deepti Hegde, Rajeev Yasarla, Hong Cai, Shizhong Han, Apratim Bhattacharyya, Shweta Mahajan, Litian Liu, Risheek Garrepalli, Vishal M. Patel, and Fatih Porikli. Distilling multi-modal large language models for autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 27575–27585, 2025. 

- [89] John Houston, Guido Zuidhof, Luca Bergamini, Yawei Ye, Long Chen, Ashesh Jain, Sammy Omari, Vladimir Iglovikov, and Peter Ondruska. One thousand and one hours: Self-driving motion prediction dataset. In _Conf. Robot Learn._ , pages 409–418. PMLR, 2021. 

- [90] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. GAIA-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 

- [91] Shengchao Hu, Li Chen, Penghao Wu, Hongyang Li, Junchi Yan, and Dacheng Tao. ST-P3: End-to-end vision-based autonomous driving via spatial-temporal feature learning. In _Eur. Conf. Comput. Vis._ , pages 533–549. Springer, 2022. 

- [92] Xiaotao Hu, Wei Yin, Mingkai Jia, Junyuan Deng, Xiaoyang Guo, Qian Zhang, Xiaoxiao Long, and Ping Tan. DrivingWorld: Constructing world model for autonomous driving via video GPT. _arXiv preprint arXiv:2412.19505_ , 2024. 

- [93] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, Lewei Lu, Xiaosong Jia, Qiang Liu, Jifeng Dai, Yu Qiao, and Hongyang Li. Planning-oriented autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 17853–17862, 2023. 

- [94] Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian Wang, Qianglong Chen, Weihua Peng, Xiaocheng Feng, Bing Qin, and Ting Liu. A survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions. _ACM Trans. Info. Syst._ , 43(2):1–55, 2025. 

- [95] Yidong Huang, Jacob Sansom, Ziqiao Ma, Felix Gervits, and Joyce Chai. DriVLMe: Enhancing llm-based autonomous driving agents with embodied and social experiences. In _IEEE/RSJ Int. Conf. Intell. Robots Syst._ , pages 3153–3160, 2024. 

- [96] Zanming Huang, Jimuyang Zhang, and Eshed Ohn-Bar. Neural volumetric world models for autonomous driving. In _Eur. Conf. Comput. Vis._ , pages 195–213. Springer, 2024. 

- [97] Zhijian Huang, Tao Tang, Shaoxiang Chen, Sihao Lin, Zequn Jie, Lin Ma, Guangrun Wang, , and Xiaodan Liang. Making large language models better planners with reasoning-decision alignment. In _Eur. Conf. Comput. Vis._ , pages 73–90. Springer, 2024. 

- [98] Jyh-Jing Hwang, Runsheng Xu, Hubert Lin, Wei-Chih Hung, Jingwei Ji, Kristy Choi, Di Huang, Tong He, Paul Covington, Benjamin Sapp, Yin Zhou, James Guo, Dragomir Anguelov, and Mingxing Tan. EMMA: End-to-end multimodal model for autonomous driving. _arXiv preprint arXiv:2410.23262_ , 2024. 

- [99] Gabriel Ilharco, Mitchell Wortsman, Nicholas Carlini, Rohan Taori, Achal Dave, Vaishaal Shankar, Hongseok Namkoong, et al. OpenCLIP. _Zenodo_ , 2021. 

- [100] Fan Jia, Weixin Mao, Yingfei Liu, Yucheng Zhao, Yuqing Wen, Chi Zhang, Xiangyu Zhang, and Tiancai Wang. ADriver-I: A general world model for autonomous driving. _arXiv preprint arXiv:2311.13549_ , 2023. 

32 

- [101] Xiaosong Jia, Yulu Gao, Li Chen, Junchi Yan, Patrick Langechuan Liu, and Hongyang Li. DriveAdapter: Breaking the coupling barrier of perception and planning in end-to-end autonomous driving. In _IEEE/CVF Int. Conf. Comput. Vis._ , pages 7953–7963, 2023. 

- [102] Xiaosong Jia, Penghao Wu, Li Chen, Jiangwei Xie, Conghui He, Junchi Yan, and Hongyang Li. Think twice before driving: Towards scalable decoders for end-to-end autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , 2023. 

- [103] Xiaosong Jia, Zhenjie Yang, Qifeng Li, Zhiyuan Zhang, and Junchi Yan. Bench2Drive: Towards multi-ability benchmarking of closed-loop end-to-end autonomous driving. In _Adv. Neural Inf. Process. Syst._ , volume 37, pages 819–844, 2024. 

- [104] Xiaosong Jia, Junqi You, Zhiyuan Zhang, and Junchi Yan. DriveTransformer: Unified transformer for scalable end-to-end autonomous driving. In _Int. Conf. Learn. Represent._ , 2025. 

- [105] Xiaosong Jia, Chenhe Zhang, Yule Jiang, Songbur Wong, Zhiyuan Zhang, Chen Chen, Shaofeng Zhang, Xuanhe Zhou, Xue Yang, Junchi Yan, and Yu-Gang Jiang. Spatial retrieval augmented autonomous driving. _arXiv preprint arXiv:2512.06865_ , 2025. 

- [106] Anqing Jiang, Yu Gao, Zhigang Sun, Yiru Wang, Jijun Wang, Jinghao Chai, Qian Cao, Yuweng Heng, Hao Jiang, Yunda Dong, Zongzheng Zhang, Xianda Guo, Hao Sun, and Hao Zhao. DiffVLA: Vision-language guided diffusion planning for autonomous driving. _arXiv preprint arXiv:2505.19381_ , 2025. 

- [107] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. VAD: Vectorized scene representation for efficient autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 8340–8350, 2023. 

- [108] Bo Jiang, Shaoyu Chen, Bencheng Liao, Xingyu Zhang, Wei Yin, Qian Zhang, Chang Huang, Wenyu Liu, and Xinggang Wang. Senna: Bridging large vision-language models and end-to-end autonomous driving. _arXiv preprint arXiv:2410.22313_ , 2024. 

- [109] Bo Jiang, Shaoyu Chen, Qian Zhang, Wenyu Liu, and Xinggang Wang. AlphaDrive: Unleashing the power of VLMs in autonomous driving via reinforcement learning and reasoning. _arXiv preprint arXiv:2503.07608_ , 2025. 

- [110] Sicong Jiang, Zilin Huang, Kangan Qian, Ziang Luo, Tianze Zhu, Yang Zhong, Yihong Tang, Menglin Kong, Yunlong Wang, Siwen Jiao, Hao Ye, Zihao Sheng, Xin Zhao, Tuopu Wen, Zheng Fu, Sikai Chen, Kun Jiang, Diange Yang, Seongjin Choi, and Lijun Sun. A survey on vision-language-action models for autonomous driving. _arXiv preprint arXiv:2506.24044_ , 2025. 

- [111] Bu Jin, Xiaotao Hu, Songen Gu, Yupeng Zheng, Xiaoyang Guo, et al. OccVAR: Scalable 4D occupancy prediction via next-scale prediction. https://openreview.net/forum?id=X2HnTFsFm8, 2025. 

- [112] Taotao Jing, Haifeng Xia, Renran Tian, Haoran Ding, Xiao Luo, Joshua Domeyer, Rini Sherony, and Zhengming Ding. Inaction: Interpretable action decision making for autonomous driving. In _European Conference on Computer Vision_ , pages 370–387. Springer, 2022. 

- [113] Daniel Kahneman. Thinking, fast and slow. _Farrar, Straus and Giroux_ , 2011. 

- [114] Napat Karnchanachari, Dimitris Geromichalos, Kok Seang Tan, Nanxiang Li, Christopher Eriksen, Shakiba Yaghoubi, Noushin Mehdipour, Gianmarco Bernasconi, Whye Kit Fong, Yiluan Guo, and Holger Caesar. Towards learning-based planning: The nuPlan benchmark for real-world autonomous driving. In _IEEE Int. Conf. Robot. Autom._ , pages 629–636, 2024. 

- [115] Bernhard Kerbl, Georgios Kopanas, Thomas Leimkühler, and George Drettakis. 3D gaussian splatting for real-time radiance field rendering. _ACM Trans. Graph._ , 42(4):139–1, 2023. 

- [116] Siddhesh Khandelwal, William Qi, Jagjeet Singh, Andrew Hartnett, and Deva Ramanan. What-if motion prediction for autonomous driving. _arXiv preprint arXiv:2008.10587_ , 2020. 

- [117] Jinkyu Kim, Anna Rohrbach, Trevor Darrell, John Canny, and Zeynep Akata. Textual explanations for self-driving vehicles. In _Eur. Conf. Comput. Vis._ , pages 563–578. Springer, 2018. 

- [118] B Ravi Kiran, Ibrahim Sobh, Victor Talpaert, Patrick Mannion, Ahmad A. Al Sallab, Senthil Yogamani, and Patrick Pérez. Deep reinforcement learning for autonomous driving: A survey. _IEEE Int. Conf. Intell. Transport. Syst._ , 23(6):4909–4926, 2021. 

- [119] W Bradley Knox, Alessandro Allievi, Holger Banzhaf, Felix Schmitt, and Peter Stone. Reward (mis)design for autonomous driving. _Artifi. Intell._ , 316:103829, 2023. 

33 

- [120] Lingdong Kong, Youquan Liu, Runnan Chen, Yuexin Ma, Xinge Zhu, Yikang Li, Yuenan Hou, Yu Qiao, and Ziwei Liu. Rethinking range view representation for LiDAR segmentation. In _IEEE/CVF Int. Conf. Comput. Vis._ , pages 228–240, 2023. 

- [121] Lingdong Kong, Youquan Liu, Xin Li, Runnan Chen, Wenwei Zhang, Jiawei Ren, Liang Pan, Kai Chen, and Ziwei Liu. Robo3D: Towards robust and reliable 3D perception against corruptions. In _IEEE/CVF Int. Conf. Comput. Vis._ , pages 19994–20006, 2023. 

- [122] Lingdong Kong, Shaoyuan Xie, Hanjiang Hu, Yaru Niu, Wei Tsang Ooi, Benoit R. Cottereau, Lai Xing Ng, Yuexin Ma, Wenwei Zhang, Liang Pan, Kai Chen, Ziwei Liu, Weichao Qiu, Wei Zhang, Xu Cao, Hao Lu, Ying-Cong Chen, Caixin Kang, Xinning Zhou, Chengyang Ying, Wentao Shang, Xingxing Wei, Yinpeng Dong, Bo Yang, Shengyin Jiang, Zeliang Ma, Dengyi Ji, Haiwen Li, Xingliang Huang, Yu Tian, Genghua Kou, Fan Jia, Yingfei Liu, Tiancai Wang, Ying Li, Xiaoshuai Hao, Yifan Yang, Hui Zhang, Mengchuan Wei, Yi Zhou, Haimei Zhao, Jing Zhang, Jinke Li, Xiao He, Xiaoqiang Cheng, Bingyang Zhang, Lirong Zhao, Dianlei Ding, Fangsheng Liu, Yixiang Yan, Hongming Wang, Nanfei Ye, Lun Luo, Yubo Tian, Yiwei Zuo, Zhe Cao, Yi Ren, Yunfan Li, Wenjie Liu, Xun Wu, Yifan Mao, Ming Li, Jian Liu, Jiayang Liu, Zihan Qin, Cunxi Chu, Jialei Xu, Wenbo Zhao, Junjun Jiang, Xianming Liu, Ziyan Wang, Chiwei Li, Shilong Li, Chendong Yuan, Songyue Yang, Wentao Liu, Peng Chen, Bin Zhou, Yubo Wang, Chi Zhang, Jianhang Sun, Hai Chen, Xiao Yang, Lizhong Wang, Dongyi Fu, Yongchun Lin, Huitong Yang, Haoang Li, Yadan Luo, Xianjing Cheng, and Yong Xu. The RoboDrive challenge: Drive anytime anywhere in any condition. _arXiv preprint arXiv:2405.08816_ , 2024. 

- [123] Lingdong Kong, Xiang Xu, Youquan Liu, Jun Cen, Runnan Chen, Wenwei Zhang, Liang Pan, Kai Chen, and Ziwei Liu. LargeAD: Large-scale cross-sensor data pretraining for autonomous driving. _IEEE Trans. Pattern Anal. Mach. Intell._ , 2025. 

- [124] Lingdong Kong, Xiang Xu, Jiawei Ren, Wenwei Zhang, Liang Pan, Kai Chen, Wei Tsang Ooi, and Ziwei Liu. Multi-modal data-efficient 3D scene understanding for autonomous driving. _IEEE Trans. Pattern Anal. Mach. Intell._ , 47(5):3748–3765, 2025. 

- [125] Lingdong Kong, Wesley Yang, Jianbiao Mei, Youquan Liu, Ao Liang, Dekai Zhu, Dongyue Lu, Wei Yin, Xiaotao Hu, Mingkai Jia, Junyuan Deng, Kaiwen Zhang, Yang Wu, Tianyi Yan, Shenyuan Gao, Song Wang, Linfeng Li, Liang Pan, Yong Liu, Jianke Zhu, Wei Tsang Ooi, Steven C. H. Hoi, and Ziwei Liu. 3D and 4D world modeling: A survey. _arXiv preprint arXiv:2509.07996_ , 2025. 

- [126] Alex H. Lang, Sourabh Vora, Holger Caesar, Lubing Zhou, Jiong Yang, and Oscar Beijbom. PointPillars: Fast encoders for object detection from point clouds. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 12697–12705, 2019. 

- [127] Doyup Lee, Chiheon Kim, Saehoon Kim, Minsu Cho, and Wook-Shin Han. Autoregressive image generation using residual quantization. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 11523–11532, 2022. 

- [128] Youngwan Lee, Joong-won Hwang, Sangrok Lee, Yuseok Bae, and Jongyoul Park. An energy and GPUcomputation efficient backbone network for real-time object detection. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog. Worksh._ , pages 1–9, 2019. 

- [129] Bo Li, Yuanhan Zhang, Dong Guo, Renrui Zhang, Feng Li, Hao Zhang, Kaichen Zhang, Peiyuan Zhang, Yanwei Li, Ziwei Liu, and Chunyuan Li. LlaVA-OneVision: Easy visual task transfer. _arXiv preprint arXiv:2408.03326_ , 2024. 

- [130] Boyi Li, Yue Wang, Jiageng Mao, Boris Ivanovic, Sushant Veer, Karen Leung, and Marco Pavone. Driving everywhere with large language model policy adaptation. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 14948–14957, 2024. 

- [131] Hongyang Li, Yang Li, Huijie Wang, Jia Zeng, Huilin Xu, Pinlong Cai, Li Chen, Junchi Yan, Feng Xu, Lu Xiong, Jingdong Wang, Futang Zhu, Chunjing Xu, Tiancai Wang, Fei Xia, Beipeng Mu, Zhihui Peng, Dahua Lin, and Yu Qiao. Open-sourced data ecosystem in autonomous driving: The present and future. _arXiv preprint arXiv:2312.03408_ , 2023. 

- [132] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. BLIP-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In _Int. Conf. Mach. Learn._ , pages 19730–19742. PMLR, 2023. 

- [133] Peidong Li and Dixiao Cui. Navigation-guided sparse scene representation for end-to-end autonomous driving. _arXiv preprint arXiv:2409.18341_ , 2024. 

34 

- [134] Peizheng Li, Zhenghao Zhang, David Holtz, Hang Yu, Yutong Yang, Yuzhi Lai, Rui Song, Andreas Geiger, and Andreas Zell. SpaceDrive: Infusing spatial awareness into VLM-based autonomous driving. _arXiv preprint arXiv:2512.10719_ , 2025. 

- [135] Pengxiang Li, Yinan Zheng, Yue Wang, Huimin Wang, Hang Zhao, Jingjing Liu, Xianyuan Zhan, Kun Zhan, and Xianpeng Lang. Discrete diffusion for reflective vision-language-action models in autonomous driving. _arXiv preprint arXiv:2509.20109_ , 2025. 

- [136] Qifeng Li, Xiaosong Jia, Shaobo Wang, and Junchi Yan. Think2Drive: Efficient reinforcement learning by thinking with latent world model for autonomous driving (in CARLA-V2). In _Eur. Conf. Comput. Vis._ , pages 142–158. Springer, 2024. 

- [137] Rong Li, Yuhao Dong, Tianshuai Hu, Ao Liang, Youquan Liu, Dongyue Lu, Liang Pan, Lingdong Kong, Junwei Liang, and Ziwei Liu. 3EED: Ground everything everywhere in 3D. In _Adv. Neural Inf. Process. Syst._ , volume 38, 2025. 

- [138] Wentong Li, Yuqian Yuan, Jian Liu, Dongqi Tang, Song Wang, Jie Qin, Jianke Zhu, and Lei Zhang. TokenPacker: Efficient visual projector for multimodal LLM. _Int. J. Comput. Vis._ , 133:6794–6812, 2025. 

- [139] Xin Li, Yeqi Bai, Pinlong Cai, Licheng Wen, Daocheng Fu, Bo Zhang, Xuemeng Yang, Xinyu Cai, Tao Ma, Jianfei Guo, Xing Gao, Min Dou, Yikang Li, Botian Shi, Yong Liu, Liang He, and Yu Qiao. Towards knowledge-driven autonomous driving. _arXiv preprint arXiv:2312.04316_ , 2023. 

- [140] Ye Li, Lingdong Kong, Hanjiang Hu, Xiaohao Xu, and Xiaonan Huang. Is your LiDAR placement optimized for 3D scene understanding? In _Adv. Neural Inf. Process. Syst._ , volume 37, pages 34980–35017, 2024. 

- [141] Yiheng Li, Cunxin Fan, Chongjian Ge, Zhihao Zhao, Chenran Li, Chenfeng Xu, Huaxiu Yao, Masayoshi Tomizuka, Bolei Zhou, Chen Tang, Mingyu Ding, and Wei Zhan. WOMD-Reasoning: A large-scale dataset for interaction reasoning in driving. _arXiv preprint arXiv:2407.04281_ , 2024. 

- [142] Yingyan Li, Lue Fan, Jiawei He, Yuqi Wang, Yuntao Chen, Zhaoxiang Zhang, and Tieniu Tan. Enhancing end-to-end autonomous driving with latent world model. _arXiv preprint arXiv:2406.08481_ , 2024. 

- [143] Yingyan Li, Shuyao Shang, Weisong Liu, Bing Zhan, Haochen Wang, Yuqi Wang, Yuntao Chen, Xiaoman Wang, Yasong An, Chufeng Tang, Lu Hou, Lue Fan, and Zhaoxiang Zhang. DriveVLA-W0: World models amplify data scaling law in autonomous driving. _arXiv preprint arXiv:2510.12796_ , 2025. 

- [144] Yingyan Li, Yuqi Wang, Yang Liu, Jiawei He, Lue Fan, and Zhaoxiang Zhang. End-to-end driving with online trajectory evaluation via bev world model. _arXiv preprint arXiv:2504.01941_ , 2025. 

- [145] Yongkang Li, Kaixin Xiong, Xiangyu Guo, Fang Li, Sixu Yan, Gangwei Xu, Lijun Zhou, Long Chen, Haiyang Sun, Bing Wang, Kun Ma, Guang Chen, Hangjun Ye, Wenyu Liu, and Xinggang Wang. ReCogDrive: A reinforced cognitive framework for end-to-end autonomous driving. _arXiv preprint arXiv:2506.08052_ , 2025. 

- [146] Yue Li, Meng Tian, Dechang Zhu, Jiangtong Zhu, Zhenyu Lin, Zhiwei Xiong, and Xinhai Zhao. Drive-R1: Bridging reasoning and planning in VLMs for autonomous driving with reinforcement learning. _arXiv preprint arXiv:2506.18234_ , 2025. 

- [147] Zhenxin Li, Kailin Li, Shihao Wang, Shiyi Lan, Zhiding Yu, Yishen Ji, Zhiqi Li, Ziyue Zhu, Jan Kautz, Zuxuan Wu, Yu-Gang Jiang, and Jose M. Alvarez. Hydra-MDP: End-to-end multimodal planning with multi-target hydra-distillation. _arXiv preprint arXiv:2406.06978_ , 2024. 

- [148] Zhiqi Li, Wenhai Wang, Hongyang Li, Enze Xie, Chonghao Sima, Tong Lu, Qiao Yu, and Jifeng Dai. BEVFormer: learning bird’s-eye-view representation from LiDAR-camera via spatiotemporal transformers. _IEEE Trans. Pattern Anal. Mach. Intell._ , 47(3):2020–2036, 2024. 

- [149] Zhiqi Li, Zhiding Yu, Shiyi Lan, Jiahan Li, Jan Kautz, Tong Lu, and Jose M Alvarez. Is ego status all you need for open-loop end-to-end autonomous driving? In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 14864–14873, 2024. 

- [150] Zhuoren Li, Guizhe Jin, Ran Yu, Zhiwen Chen, Nan Li, Wei Han, Lu Xiong, Bo Leng, Jia Hu, Ilya Kolmanovsky, and Dimitar Filev. A survey of reinforcement learning-based motion planning for autonomous driving: Lessons learned from a driving task perspective. _arXiv preprint arXiv:2503.23650_ , 2025. 

- [151] Li Auto Inc. MindVLA, 2025. URL https://ir.lixiang.com/news-releases/news-release-details/ li-auto-inc-march-2025-delivery-update. 

35 

- [152] Ao Liang, Lingdong Kong, Dongyue Lu, Youquan Liu, Jian Fang, Huaici Zhao, and Wei Tsang Ooi. Perspectiveinvariant 3D object detection. In _IEEE/CVF Int. Conf. Comput. Vis._ , pages 27725–27738, 2025. 

- [153] Ao Liang, Youquan Liu, Yu Yang, Dongyue Lu, Linfeng Li, Lingdong Kong, Huaici Zhao, and Wei Tsang Ooi. LiDARCrafter: Dynamic 4D world modeling from LiDAR sequences. In _AAAI Conf. Artifi. Intell._ , volume 40, 2026. 

- [154] Tingting Liang, Hongwei Xie, Kaicheng Yu, Zhongyu Xia, Zhiwei Lin, Yongtao Wang, Tao Tang, Bing Wang, and Zhi Tang. BEVFusion: A simple and robust LiDAR-camera fusion framework. _Adv. Neural Inf. Process. Syst._ , 35:10421–10434, 2022. 

- [155] Bencheng Liao, Shaoyu Chen, Haoran Yin, Bo Jiang, Cheng Wang, Sixu Yan, Xinbang Zhang, Xiangyu Li, Ying Zhang, Qian Zhang, and Xinggang Wang. DiffusionDrive: Truncated diffusion model for end-to-end autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 12037–12047, 2025. 

- [156] Bin Lin, Yang Ye, Bin Zhu, Jiaxi Cui, Munan Ning, Peng Jin, and Li Yuan. Video-LLaVA: Learning united visual representation by alignment before projection. _arXiv preprint arXiv:2311.10122_ , 2023. 

- [157] Dongyang Liu, Shitian Zhao, Le Zhuo, Weifeng Lin, Yi Xin, Xinyue Li, Qi Qin, Yu Qiao, Hongsheng Li, and Peng Gao. Lumina-MGPT: Illuminate flexible photorealistic text-to-image generation with multimodal generative pretraining. _arXiv preprint arXiv:2408.02657_ , 2024. 

- [158] Hanchao Liu, Wenyuan Xue, Yifei Chen, Dapeng Chen, Xiutian Zhao, Ke Wang, Liping Hou, Rongjun Li, and Wei Peng. A survey on hallucination in large vision-language models. _arXiv preprint arXiv:2402.00253_ , 2024. 

- [159] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. In _Adv. Neural Inf. Process. Syst._ , volume 36, pages 34892–34916, 2023. 

- [160] Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Improved baselines with visual instruction tuning. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 26296–26306, 2024. 

- [161] Lin Liu, Caiyan Jia, Guanyi Yu, Ziying Song, JunQiao Li, Feiyang Jia, Peiliang Wu, Xiaoshuai Hao, and Yandan Luo. GuideFlow: Constraint-guided flow matching for planning in end-to-end autonomous driving. _arXiv preprint arXiv:2511.18729_ , 2025. 

- [162] Mingyu Liu, Ekim Yurtsever, Jonathan Fossaert, Xingcheng Zhou, Walter Zimmer, Yuning Cui, Bare Luka Zagar, and Alois C. Knoll. A survey on autonomous driving datasets: Statistics, annotation quality, and a future outlook. _IEEE Trans. Intell. Veh._ , 9(11):7138–7164, 2024. 

- [163] Pei Liu, Haipeng Liu, Haichao Liu, Xin Liu, Jinxin Ni, and Jun Ma. VLM-E2E: Enhancing end-to-end autonomous driving with multimodal driver attention fusion. _arXiv preprint arXiv:2502.18042_ , 2025. 

- [164] Pei Liu, Hongliang Lu, Haichao Liu, Haipeng Liu, Xin Liu, Ruoyu Yao, Shengbo Eben Li, and Jun Ma. OmniScene: Attention-augmented multimodal 4D scene understanding for autonomous driving. _arXiv preprint arXiv:2509.19973_ , 2025. 

- [165] Pei Liu, Qingtian Ning, Xinyan Lu, Haipeng Liu, Weiliang Ma, Dangen She, Peng Jia, Xianpeng Lang, and Jun Ma. OmniReason: A temporal-guided vision-language-action framework for autonomous driving. _arXiv preprint arXiv:2509.00789_ , 2025. 

- [166] Ruixun Liu, Lingyu Kong, Derun Li, and Hang Zhao. OccVLA: Vision-language-action model with implicit 3D occupancy supervision. _arXiv preprint arXiv:2509.05578_ , 2025. 

- [167] Wenru Liu, Pei Liu, and Jun Ma. DSDrive: Distilling large language model for lightweight end-to-end autonomous driving with unified reasoning and planning. _arXiv preprint arXiv:2505.05360_ , 2025. 

- [168] Xueyi Liu, Zuodong Zhong, Yuxin Guo, Yun-Fu Liu, Zhiguo Su, Qichao Zhang, Junli Wang, Yinfeng Gao, Yupeng Zheng, Qiao Lin, Huiyong Chen, and Dongbin Zhao. ReasonPlan: Unified scene prediction and decision reasoning for closed-loop autonomous driving. _arXiv preprint arXiv:2505.20024_ , 2025. 

- [169] Youquan Liu, Lingdong Kong, Jun Cen, Runnan Chen, Wenwei Zhang, Liang Pan, Kai Chen, and Ziwei Liu. Segment any point cloud sequences by distilling vision foundation models. In _Adv. Neural Inf. Process. Syst._ , volume 36, pages 37193–37229, 2023. 

- [170] Youquan Liu, Lingdong Kong, Weidong Yang, Xin Li, Ao Liang, Runnan Chen, Ben Fei, and Tongliang Liu. La La LiDAR: Large-scale layout generation from LiDAR data. In _AAAI Conf. Artifi. Intell._ , volume 40, 2026. 

36 

- [171] Ze Liu, Yutong Lin, Yue Cao, Han Hu, Yixuan Wei, Zheng Zhang, Stephen Lin, and Baining Guo. Swin transformer: Hierarchical vision transformer using shifted windows. In _IEEE/CVF Int. Conf. Comput. Vis._ , pages 10012–10022, 2021. 

- [172] Zhuang Liu, Hanzi Mao, Chao-Yuan Wu, Christoph Feichtenhofer, Trevor Darrell, and Saining Xie. A ConvNet for the 2020s. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 11976–11986, 2022. 

- [173] Hao Lu, Ziyang Liu, Guangfeng Jiang, Yuanfei Luo, Sheng Chen, Yangang Zhang, and Ying-Cong Chen. UniUGP: Unifying understanding, generation, and planing for end-to-end autonomous driving. _arXiv preprint arXiv:2512.09864_ , 2025. 

- [174] Jiachen Lu, Ze Huang, Zeyu Yang, Jiahui Zhang, and Li Zhang. WoVoGen: World volume-aware diffusion for controllable multi-camera driving scene generation. In _Eur. Conf. Comput. Vis._ , pages 329–345. Springer, 2024. 

- [175] Yuhang Lu, Jiadong Tu, Yuexin Ma, and Xinge Zhu. ReAL-AD: Towards human-like reasoning in end-to-end autonomous driving. In _IEEE/CVF Int. Conf. Comput. Vis._ , pages 27783–27793, 2025. 

- [176] Yuechen Luo, Fang Li, Shaoqing Xu, Zhiyi Lai, Lei Yang, Qimao Chen, Ziang Luo, Zixun Xie, Shengyin Jiang, Jiaxin Liu, Long Chen, Bing Wang, and Zhi xin Yang. AdaThinkDrive: Adaptive thinking via reinforcement learning for autonomous driving. _arXiv preprint arXiv:2509.13769_ , 2025. 

- [177] Junyi Ma, Xieyuanli Chen, Jiawei Huang, Jingyi Xu, Zhen Luo, Jintao Xu, Weihao Gu, Rui Ai, and Hesheng Wang. Cam4DOcc: Benchmark for camera-only 4D occupancy forecasting in autonomous driving applications. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 21486–21495, 2024. 

- [178] Yingzi Ma, Yulong Cao, Wenhao Ding, Shuibai Zhang, Yan Wang, Boris Ivanovic, Ming Jiang, Marco Pavone, and Chaowei Xiao. dVLM-AD: Enhance diffusion vision-language-model for driving via controllable reasoning. _arXiv preprint arXiv:2512.04459_ , 2025. 

- [179] Yueen Ma, Zixing Song, Yuzheng Zhuang, Jianye Hao, and Irwin King. A survey on vision-language-action models for embodied AI. _arXiv preprint arXiv:2405.14093_ , 2024. 

- [180] Yueen Ma, Zixing Song, Yuzheng Zhuang, Jianye Hao, and Irwin King. Survey on vision-language-action models. _arXiv preprint arXiv:2502.06851_ , 2025. 

- [181] Yukai Ma, Tiantian Wei, Naiting Zhong, Jianbiao Mei, Tao Hu, Licheng Wen, Xuemeng Yang, Botian Shi, and Yong Liu. LeapVAD: A leap in autonomous driving via cognitive perception and dual-process thinking. _arXiv preprint arXiv:2501.08168_ , 2025. 

- [182] Yunsheng Ma, Burhaneddin Yaman, Xin Ye, Mahmut Yurt, Jingru Luo, Abhirup Mallik, Ziran Wang, and Liu Ren. ALN-P3: Unified language alignment for perception, prediction, and planning in autonomous driving. _arXiv preprint arXiv:2505.15158_ , 2025. 

- [183] Ziqiao Ma, Benjamin VanDerPloeg, Cristian-Paul Bara, Yidong Huang, Eui-In Kim, Felix Gervits, Matthew Marge, and Joyce Chai. DOROTHIE: Spoken dialogue for handling unexpected situations in interactive autonomous driving agents. _arXiv preprint arXiv:2210.12511_ , 2022. 

- [184] Jiageng Mao, Yuxi Qian, Junjie Ye, Hang Zhao, and Yue Wang. GPT-Driver: Learning to drive with GPT. _arXiv preprint arXiv:2310.01415_ , 2023. 

- [185] Jiageng Mao, Junjie Ye, Yuxi Qian, Marco Pavone, and Yue Wang. A language agent for autonomous driving. In _Conf. Lang. Model._ , 2025. 

- [186] Ana-Maria Marcu, Long Chen, Jan Hünermann, Alice Karnsund, Benoit Hanotte, Prajwal Chidananda, Saurabh Nair, Vijay Badrinarayanan, Alex Kendall, Jamie Shotton, Elahe Arani, and Oleg Sinavski. LingoQA: Visual question answering for autonomous driving. In _Eur. Conf. Comput. Vis._ , pages 252–269. Springer, 2024. 

- [187] Jianbiao Mei, Yukai Ma, Xuemeng Yang, Licheng Wen, Xinyu Cai, Xin Li, Daocheng Fu, Bo Zhang, Pinlong Cai, Min Dou, Botian Shi, Liang He, Yong Liu, and Yu Qiao. Continuously learning, adapting, and improving: A dual-process approach to autonomous driving. In _Adv. Neural Inf. Process. Syst._ , volume 37, pages 123261–123290, 2024. 

- [188] Chen Min, Dawei Zhao, Liang Xiao, Jian Zhao, Xinli Xu, Zheng Zhu, Lei Jin, Jianshu Li, Yulan Guo, Junliang Xing, Liping Jing, Yiming Nie, and Bin Dai. DriveWorld: 4D pre-trained scene understanding via world models for autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 15522–15533, 2024. 

- [189] Mona Mirzaie and Bodo Rosenhahn. Interpretable decision-making for end-to-end autonomous driving. _arXiv preprint arXiv:2508.18898_ , 2025. 

37 

- [190] Urs Muller, Jan Ben, Eric Cosatto, Beat Flepp, and Yann Cun. Off-road obstacle avoidance through end-to-end learning. In _Adv. Neural Inf. Process. Syst._ , volume 18, pages 739–746, 2005. 

- [191] Ferdinand Mütsch, Helen Gremmelmaier, Nicolas Becker, Daniel Bogdoll, Marc René Zofka, and J. Marius Zöllner. From model-based to data-driven simulation: Challenges and trends in autonomous driving. _arXiv preprint arXiv:2305.13960_ , 2023. 

- [192] Ming Nie, Renyuan Peng, Chunwei Wang, Xinyue Cai, Jianhua Han, Hang Xu, and Li Zhang. Reason2Drive: Towards interpretable and chain-based reasoning for autonomous driving. In _Eur. Conf. Comput. Vis._ , pages 292–308. Springer, 2024. 

- [193] NVIDIA. Physical AI autonomous vehicles dataset. https://huggingface.co/datasets/nvidia/ PhysicalAI-Autonomous-Vehicles, October 2025. 

- [194] Eshed Ohn-Bar, Aditya Prakash, Aseem Behl, Kashyap Chitta, and Andreas Geiger. Learning situational driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 11296–11305, 2020. 

- [195] OpenAI. Hello GPT4-o. https://openai.com/index/hello-gpt-4o, 2024. 

- [196] Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, Mahmoud Assran, Nicolas Ballas, Wojciech Galuba, Russell Howes, Po-Yao Huang, Shang-Wen Li, Ishan Misra, Michael Rabbat, Vasu Sharma, Gabriel Synnaeve, Hu Xu, Hervé Jegou, Julien Mairal, Patrick Labatut, Armand Joulin, and Piotr Bojanowski. DINOv2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 

- [197] Chenbin Pan, Burhaneddin Yaman, Tommaso Nesti, Abhirup Mallik, Alessandro G. Allievi, Senem Velipasalar, and Liu Ren. VLP: Vision language planning for autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 14760–14769, 2024. 

- [198] Yunpeng Pan, Ching-An Cheng, Kamil Saigol, Keuntaek Lee, Xinyan Yan, Evangelos Theodorou, and Byron Boots. Agile autonomous driving using end-to-end deep imitation learning. In _Robot. Sci. Syst._ , 2018. 

- [199] Jinhyung Park, Chenfeng Xu, Shijia Yang, Kurt Keutzer, Kris Kitani, Masayoshi Tomizuka, and Wei Zhan. Time Will Tell: New outlooks and a baseline for temporal multi-view 3D object detection. In _Int. Conf. Learn. Represent._ , 2023. 

- [200] Jongjin Park, Younggyo Seo, Chang Liu, Li Zhao, Tao Qin, Jinwoo Shin, and Tie-Yan Liu. Object-aware regularization for addressing causal confusion in imitation learning. In _Adv. Neural Inf. Process. Syst._ , volume 34, pages 3029–3042, 2021. 

- [201] SungYeon Park, MinJae Lee, JiHyuk Kang, Hahyeon Choi, Yoonah Park, Juhwan Cho, Adam Lee, and DongKyu Kim. VLAAD: Vision and language assistant for autonomous driving. In _IEEE/CVF Winter Conf. Appl. Comput. Vis. Worksh._ , pages 980–987, 2024. 

- [202] Dustin Podell, Zion English, Kyle Lacey, Andreas Blattmann, Tim Dockhorn, Jonas Müller, Joe Penna, and Robin Rombach. SDXL: Improving latent diffusion models for high-resolution image synthesis. In _Int. Conf. Learn. Represent._ , 2023. 

- [203] Dean A Pomerleau. ALVINN: An autonomous land vehicle in a neural network. In _Adv. Neural Inf. Process. Syst._ , volume 1, pages 305–313, 1988. 

- [204] Alexander Popov, Alperen Degirmenci, David Wehr, Shashank Hegde, Ryan Oldja, Alexey Kamenev, Bertrand Douillard, David Nistér, Urs Muller, Ruchi Bhargava, Stan Birchfield, and Nikolai Smolyanskiy. Mitigating covariate shift in imitation learning for autonomous vehicles using latent space generative world models. _arXiv preprint arXiv:2409.16663_ , 2024. 

- [205] Aditya Prakash, Aseem Behl, Eshed Ohn-Bar, Kashyap Chitta, and Andreas Geiger. Exploring data aggregation in policy learning for vision-based urban autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 11763–11773, 2020. 

- [206] Aditya Prakash, Kashyap Chitta, and Andreas Geiger. Multi-modal fusion transformer for end-to-end autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 7077–7087, 2021. 

- [207] Kangan Qian, Zhikun Ma, Yangfan He, Ziang Luo, Tianyu Shi, Tianze Zhu, Jiayin Li, Jianhui Wang, Ziyu Chen, Xiao He, Yining Shi, Zheng Fu, Xinyu Jiao, Kun Jiang, Diange Yang, and Takafumi Matsumaru. FasionAD: Fast and slow fusion thinking systems for human-like autonomous driving with adaptive feedback. _arXiv preprint arXiv:2411.18013_ , 2024. 

38 

- [208] Kangan Qian, Ziang Luo, Sicong Jiang, Zilin Huang, Jinyu Miao, Zhikun Ma, Tianze Zhu, Jiayin Li, Yangfan He, Zheng Fu, Yining Shi, Boyue Wang, Hezhe Lin, Ziyu Chen, Jiangbo Yu, Xinyu Jiao, Mengmeng Yang, Kun Jiang, and Diange Yang. FasionAD++: Integrating high-level instruction and information bottleneck in fat-slow fusion systems for enhanced safety in autonomous driving with adaptive feedback. _arXiv preprint arXiv:2503.08162_ , 2025. 

- [209] Zhijie Qiao, Haowei Li, Zhong Cao, and Henry X. Liu. LightEMMA: Lightweight end-to-end multimodal model for autonomous driving. _arXiv preprint arXiv:2505.00284_ , 2025. 

- [210] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and Ilya Sutskever. Learning transferable visual models from natural language supervision. In _Int. Conf. Mach. Learn._ , pages 8748–8763. PMLR, 2021. 

- [211] Vipula Rawte, Amit Sheth, and Amitava Das. A survey of hallucination in large foundation models. _arXiv preprint arXiv:2309.05922_ , 2023. 

- [212] Xuanchi Ren, Yifan Lu, Tianshi Cao, Ruiyuan Gao, Shengyu Huang, Amirmojtaba Sabour, Tianchang Shen, Tobias Pfaff, Jay Zhangjie Wu, Runjian Chen, Seung Wook Kim, Jun Gao, Laura Leal-Taixe, Mike Chen, Sanja Fidler, and Huan Ling. Cosmos-Drive-Dreams: Scalable synthetic driving data generation with world foundation models. _arXiv preprint arXiv:2506.09042_ , 2025. 

- [213] Katrin Renz, Long Chen, Elahe Arani, and Oleg Sinavski. SimLingo: Vision-only closed-loop autonomous driving with language-action alignment. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 11993–12003, 2025. 

- [214] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Björn Ommer. High-resolution image synthesis with latent diffusion models. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 10684–10695, 2022. 

- [215] Stéphane Ross, Geoffrey Gordon, and Drew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _Int. Conf. Artifi. Intell. Stat._ , pages 627–635, 2011. 

- [216] Luke Rowe, Rodrigue de Schaetzen, Roger Girgis, Christopher Pal, and Liam Paull. Poutine: Vision-languagetrajectory pre-training and reinforcement learning post-training enable robust end-to-end autonomous driving. _arXiv preprint arXiv:2506.11234_ , 2025. 

- [217] Ranjan Sapkota, Yang Cao, Konstantinos I. Roumeliotis, and Manoj Karkee. Vision-language-action models: Concepts, progress, applications and challenges. _arXiv preprint arXiv:2505.04769_ , 2025. 

- [218] Oliver Scheel, Luca Bergamini, Maciej Wołczyk, Błażej Osiński, and Peter Ondruska. Urban driver: Learning to drive from real-world demonstrations using policy gradients. In _Conf. Robot Learn._ , pages 718–728. PMLR, 2022. 

- [219] Mariah L Schrum, Emily Sumner, Matthew C Gombolay, and Andrew Best. Maveric: A data-driven approach to personalized autonomous driving. _IEEE Trans. Robot._ , 40:1952–1965, 2024. 

- [220] Hao Shan, Ruikai Li, Han Jiang, Yizhe Fan, Ziyang Yan, Bohan Li, Xiaoshuai Hao, Hao Zhao, Zhiyong Cui, Yilong Ren, and Haiyang Yu. Stability under scrutiny: Benchmarking representation paradigms for online HD mapping. _arXiv preprint arXiv:2510.10660_ , 2025. 

- [221] Hao Shao, Letian Wang, Ruobing Chen, Hongsheng Li, and Yu Liu. Safety-enhanced autonomous driving using interpretable sensor fusion transformer. In _Conf. Robot Learn._ , pages 726–737. PMLR, 2023. 

- [222] Hao Shao, Yuxuan Hu, Letian Wang, Guanglu Song, Steven L. Waslander, Yu Liu, and Hongsheng Li. LMDrive: Closed-loop end-to-end driving with large language models. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 15120–15130, 2024. 

- [223] Rui Shao, Wei Li, Lingsen Zhang, Renshan Zhang, Zhiyang Liu, Ran Chen, and Liqiang Nie. Large VLM-based vision-language-action models for robotic manipulation: A survey. _arXiv preprint arXiv:2508.13073_ , 2025. 

- [224] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, Y.K. Li, Y. Wu, and Daya Guo. DeepSeekMath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 

- [225] Chonghao Sima, Katrin Renz, Kashyap Chitta, Li Chen, Hanxue Zhang, Chengen Xie, Jens Beißwenger, Ping Luo, Andreas Geiger, , and Hongyang Li. DriveLM: Driving with graph visual question answering. In _Eur. Conf. Comput. Vis._ , pages 256–274. Springer, 2024. 

- [226] Nan Song, Bozhou Zhang, Xiatian Zhu, Jiankang Deng, and Li Zhang. LMAD: Integrated end-to-end visionlanguage model for explainable autonomous driving. _arXiv preprint arXiv:2508.12404_ , 2025. 

39 

- [227] Ruiqi Song, Xianda Guo, Yanlun Peng, Qinggong Wei, Hangbin Wu, and Long Chen. InsightDrive: Insight scene representation for end-to-end autonomous driving. _arXiv preprint arXiv:2503.13047_ , 2025. 

- [228] Zhihang Song, Zimin He, Xingyu Li, Qiming Ma, Ruibo Ming, Zhiqi Mao, Huaxin Pei, Lihui Peng, Jianming Hu, Danya Yao, and Yi Zhang. Synthetic datasets for autonomous driving: A survey. _IEEE Trans. Intell. Veh._ , 9(1): 1847–1864, 2023. 

- [229] Ziying Song, Caiyan Jia, Lin Liu, Hongyu Pan, Yongchang Zhang, Junming Wang, Xingyu Zhang, Shaoqing Xu, Lei Yang, and Yadan Luo. Don’t shake the wheel: Momentum-aware planning in end-to-end autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 22432–22441, 2025. 

- [230] Andreas Steiner, André Susano Pinto, Michael Tschannen, Daniel Keysers, Xiao Wang, Yonatan Bitton, Alexey Gritsenko, Matthias Minderer, Anthony Sherbondy, Shangbang Long, Siyang Qin, Reeve Ingle, Emanuele Bugliarello, Sahar Kazemzadeh, Thomas Mesnard, Ibrahim Alabdulmohsin, Lucas Beyer, and Xiaohua Zhai. PaliGemma 2: A family of versatile VLMs for transfer. _arXiv preprint arXiv:2412.03555_ , 2024. 

- [231] Haisheng Su, Wei Wu, and Junchi Yan. DiFSD: Ego-centric fully sparse paradigm with uncertainty denoising and iterative refinement for efficient end-to-end self-driving. _arXiv preprint arXiv:2409.09777_ , 2024. 

- [232] Bin Sun, Yaoguang Cao, Yan Wang, Rui Wang, Jiachen Shang, Xiejie Feng, Jiayi Lu, Jia Shi, Shichun Yang, Xiaoyu Yan, and Ziying Song. MindDrive: An all-in-one framework bridging world models and vision-language model for end-to-end autonomous driving. _arXiv preprint arXiv:2512.04441_ , 2025. 

- [233] Jintao Sun, Hu Zhang, Gangyi Ding, and Zhedong Zheng. Echo planning for autonomous driving: From current observations to future trajectories and back. _arXiv preprint arXiv:2505.18945_ , 2025. 

- [234] Pei Sun, Henrik Kretzschmar, Xerxes Dotiwalla, Aurelien Chouard, Vijaysai Patnaik, Paul Tsui, James Guo, Yin Zhou, Yuning Chai, Benjamin Caine, Vijay Vasudevan, Wei Han, Jiquan Ngiam, Hang Zhao, Aleksei Timofeev, Scott Ettinger, Maxim Krivokon, Amy Gao, Aditya Joshi, Yu Zhang, Jonathon Shlens, Zhifeng Chen, and Dragomir Anguelov. Scalability in perception for autonomous driving: Waymo open dataset. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 2446–2454, 2020. 

- [235] Peize Sun, Yi Jiang, Shoufa Chen, Shilong Zhang, Bingyue Peng, Ping Luo, and Zehuan Yuan. Autoregressive model beats diffusion: Llama for scalable image generation. _arXiv preprint arXiv:2406.06525_ , 2024. 

- [236] Wenchao Sun, Xuewu Lin, Yining Shi, Chuang Zhang, Haoran Wu, and Sifa Zheng. SparseDrive: End-to-end autonomous driving via sparse scene representation. In _IEEE Int. Conf. Robot. Autom._ , pages 8795–8801, 2025. 

- [237] Richard S Sutton, Andrew G Barto, et al. _Reinforcement Learning: An Introduction_ , volume 1. MIT Press, Cambridge, 1998. 

- [238] Mingxing Tan and Quoc Le. EfficientNet: Rethinking model scaling for convolutional neural networks. In _Int. Conf. Mach. Learn._ , pages 6105–6114. PMLR, 2019. 

- [239] Shuhan Tan, Kashyap Chitta, Yuxiao Chen, Ran Tian, Yurong You, Yan Wang, Wenjie Luo, Yulong Cao, Philipp Krahenbuhl, Marco Pavone, and Boris Ivanovic. Latent chain-of-thought world modeling for end-to-end driving. _arXiv preprint arXiv:2512.10226_ , 2025. 

- [240] Yihong Tang, Haicheng Liao, Tong Nie, Junlin He, Ao Qu, Kehua Chen, Wei Ma, Zhenning Li, Lijun Sun, and Chengzhong Xu. E3AD: An emotion-aware vision-language-action model for human-centric end-to-end autonomous driving. _arXiv preprint arXiv:2512.04733_ , 2025. 

- [241] Chameleon Team. Chameleon: Mixed-modal early-fusion foundation models. _arXiv preprint arXiv:2405.09818_ , 2024. 

- [242] Gemini Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M. Dai, Anja Hauth, Katie Millican, David Silver, Melvin Johnson, Ioannis Antonoglou, Julian Schrittwieser, Amelia Glaese, Jilin Chen, Emily Pitler, Timothy Lillicrap, Angeliki Lazaridou, Orhan Firat, James Molloy, Michael Isard, Paul R. Barham, Tom Hennigan, Benjamin Lee, Fabio Viola, Malcolm Reynolds, Yuanzhong Xu, Ryan Doherty, Eli Collins, Clemens Meyer, Eliza Rutherford, Erica Moreira, Kareem Ayoub, Megha Goel, Jack Krawczyk, Cosmo Du, Ed Chi, Heng-Tze Cheng, Eric Ni, Purvi Shah, Patrick Kane, Betty Chan, Manaal Faruqui, Aliaksei Severyn, Hanzhao Lin, YaGuang Li, Yong Cheng, Abe Ittycheriah, Mahdis Mahdieh, Mia Chen, Pei Sun, Dustin Tran, Sumit Bagri, Balaji Lakshminarayanan, Jeremiah Liu, Andras Orban, Fabian Güra, Hao Zhou, Xinying Song, Aurelien Boffy, Harish Ganapathy, Steven Zheng, HyunJeong Choe, Ágoston Weisz, Tao Zhu, Yifeng Lu, Siddharth Gopal, Jarrod Kahn, Maciej Kula, Jeff Pitman, Rushin Shah, Emanuel Taropa, Majd Al Merey, Martin Baeuml, Zhifeng Chen, Laurent El Shafey, Yujing Zhang, 

40 

Olcan Sercinoglu, George Tucker, Enrique Piqueras, Maxim Krikun, Iain Barr, Nikolay Savinov, Ivo Danihelka, Becca Roelofs, Anaïs White, Anders Andreassen, Tamara von Glehn, Lakshman Yagati, Mehran Kazemi, Lucas Gonzalez, Misha Khalman, Jakub Sygnowski, Alexandre Frechette, Charlotte Smith, Laura Culp, et al. Gemini: A family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ , 2023. 

- [243] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, Steven Bohez, Konstantinos Bousmalis, Anthony Brohan, Thomas Buschmann, Arunkumar Byravan, Serkan Cabi, Ken Caluwaerts, Federico Casarini, Oscar Chang, Jose Enrique Chen, Xi Chen, Hao-Tien Lewis Chiang, Krzysztof Choromanski, David D’Ambrosio, Sudeep Dasari, Todor Davchev, Coline Devin, Norman Di Palo, Tianli Ding, Adil Dostmohamed, Danny Driess, Yilun Du, Debidatta Dwibedi, Michael Elabd, Claudio Fantacci, Cody Fong, Erik Frey, Chuyuan Fu, Marissa Giustina, Keerthana Gopalakrishnan, Laura Graesser, Leonard Hasenclever, Nicolas Heess, Brandon Hernaez, Alexander Herzog, R. Alex Hofer, Jan Humplik, Atil Iscen, Mithun George Jacob, Deepali Jain, Ryan Julian, Dmitry Kalashnikov, M. Emre Karagozler, Stefani Karp, Chase Kew, Jerad Kirkland, Sean Kirmani, Yuheng Kuang, Thomas Lampe, Antoine Laurens, Isabel Leal, Alex X. Lee, TsangWei Edward Lee, Jacky Liang, Yixin Lin, Sharath Maddineni, Anirudha Majumdar, Assaf Hurwitz Michaely, Robert Moreno, Michael Neunert, Francesco Nori, Carolina Parada, Emilio Parisotto, Peter Pastor, Acorn Pooley, Kanishka Rao, Krista Reymann, Dorsa Sadigh, Stefano Saliceti, Pannag Sanketi, Pierre Sermanet, Dhruv Shah, Mohit Sharma, Kathryn Shea, Charles Shu, Vikas Sindhwani, Sumeet Singh, Radu Soricut, Jost Tobias Springenberg, Rachel Sterneck, Razvan Surdulescu, Jie Tan, Jonathan Tompson, Vincent Vanhoucke, Jake Varley, Grace Vesom, Giulia Vezzani, Oriol Vinyals, Ayzaan Wahid, Stefan Welker, et al. Gemini robotics: Bringing AI into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025. 

- [244] Qwen Team. Introducing Qwen1.5, February 2024. URL https://qwenlm.github.io/blog/qwen1.5. 

- [245] Wayve Team. LINGO-2: Driving with natural language, 2024. URL https://wayve.ai/thinking/ lingo-2-driving-with-language. 

- [246] Waywe Research Team et al. LINGO-2: Driving with natural language, 2024. 

- [247] Ran Tian, Boyi Li, Xinshuo Weng, Yuxiao Chen, Edward Schmerling, Yue Wang, Boris Ivanovic, and Marco Pavone. Tokenize the world into object-level knowledge to address long-tail events in autonomous driving. In _Conf. Robot Learn._ , pages 3656–3673. PMLR, 2025. 

- [248] Xiaoyu Tian, Tao Jiang, Longfei Yun, Yucheng Mao, Huitong Yang, Yue Wang, Yilun Wang, and Hang Zhao. Occ3D: A large-scale 3D occupancy prediction benchmark for autonomous driving. In _Adv. Neural Inf. Process. Syst._ , volume 36, pages 64318–64330, 2023. 

- [249] Xiaoyu Tian, Junru Gu, Bailin Li, Yicheng Liu, Yang Wang, Zhiyong Zhao, Kun Zhan, Peng Jia, Xianpeng Lang, and Hang Zhao. DriveVLM: The convergence of autonomous driving and large vision-language models. In _Conf. Robot Learn._ , pages 4698–4726. PMLR, 2025. 

- [250] Wenwen Tong, Chonghao Sima, Tai Wang, Li Chen, Silei Wu, Hanming Deng, Yi Gu, Lewei Lu, Ping Luo, Dahua Lin, and Hongyang Li. Scene as occupancy. In _IEEE/CVF Int. Conf. Comput. Vis._ , pages 8406–8415, 2023. 

- [251] Marin Toromanoff, Emilie Wirbel, and Fabien Moutarde. End-to-end model-free reinforcement learning for urban driving using implicit affordances. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 7153–7162, 2020. 

- [252] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, Dan Bikel, Lukas Blecher, Cristian Canton Ferrer, Moya Chen, Guillem Cucurull, David Esiobu, Jude Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller, Cynthia Gao, Vedanuj Goswami, Naman Goyal, Anthony Hartshorn, Saghar Hosseini, Rui Hou, Hakan Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa, Isabel Kloumann, Artem Korenev, Punit Singh Koura, Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee, Diana Liskovich, Yinghai Lu, Yuning Mao, Xavier Martinet, Todor Mihaylov, Pushkar Mishra, Igor Molybog, Yixin Nie, Andrew Poulton, Jeremy Reizenstein, Rashi Rungta, Kalyan Saladi, Alan Schelten, Ruan Silva, Eric Michael Smith, Ranjan Subramanian, Xiaoqing Ellen Tan, Binh Tang, Ross Taylor, Adina Williams, Jian Xiang Kuan, Puxin Xu, Zheng Yan, Iliyan Zarov, Yuchen Zhang, Angela Fan, Melanie Kambadur, Sharan Narang, Aurelien Rodriguez, Robert Stojnic, Sergey Edunov, and Thomas Scialom. LLaMA 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. 

- [253] Michael Tschannen, Alexey Gritsenko, Xiao Wang, Muhammad Ferjad Naeem, Ibrahim Alabdulmohsin, Nikhil Parthasarathy, Talfan Evans, Lucas Beyer, Ye Xia, Basil Mustafa, Olivier Hénaff, Jeremiah Harmsen, Andreas Steiner, and Xiaohua Zhai. SigLIP 2: Multilingual vision-language encoders with improved semantic understanding, localization, and dense features. _arXiv preprint arXiv:2502.14786_ , 2025. 

41 

- [254] Aaron Van Den Oord, Oriol Vinyals, et al. Neural discrete representation learning. In _Adv. Neural Inf. Process. Syst._ , volume 30, pages 6309–6318, 2017. 

- [255] Eli Verwimp, Kuo Yang, Sarah Parisot, Lanqing Hong, Steven McDonagh, Eduardo Pérez-Pellitero, Matthias De Lange, and Tinne Tuytelaars. CLAD: A realistic continual learning benchmark for autonomous driving. _Neural Net._ , 161:659–669, 2023. 

- [256] Daming Wang, Yuhao Song, Zijian He, Kangliang Chen, Xing Pan, Lu Deng, and Weihao Gu. HMVLM: Multistage reasoning-enhanced vision-language model for long-tailed driving scenarios. _arXiv preprint arXiv:2506.05883_ , 2025. 

- [257] Dingrui Wang, Marc Kaufeld, and Johannes Betz. DualAD: Dual-layer planning for reasoning in autonomous driving. In _IEEE/RSJ Int. Conf. Intell. Robots Syst._ , 2025. 

- [258] Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Yang Fan, Kai Dang, Mengfei Du, Xuancheng Ren, Rui Men, Dayiheng Liu, Chang Zhou, Jingren Zhou, and Junyang Lin. Qwen2-VL: Enhancing vision-language model’s perception of the world at any resolution. _arXiv preprint arXiv:2409.12191_ , 2024. 

- [259] Shihao Wang, Zhiding Yu, Xiaohui Jiang, Shiyi Lan, Min Shi, Nadine Chang, Jan Kautz, Ying Li, and Jose M. Alvarez. OmniDrive: A holistic vision-language dataset for autonomous driving with counterfactual reasoning. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 22442–22452, 2025. 

- [260] Song Wang, Jiawei Yu, Wentong Li, Wenyu Liu, Xiaolu Liu, Junbo Chen, and Jianke Zhu. Not all voxels are equal: Hardness-aware semantic scene completion with self-distillation. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 14792–14801, 2024. 

- [261] Song Wang, Gongfan Fang, Lingdong Kong, Xiangtai Li, Jianyun Xu, Sheng Yang, Qiang Li, Jianke Zhu, and Xinchao Wang. PixelThink: Towards efficient chain-of-pixel reasoning. _arXiv preprint arXiv:2505.23727_ , 2025. 

- [262] Tianqi Wang, Enze Xie, Ruihang Chu, Zhenguo Li, and Ping Luo. DriveCoT: Integrating chain-of-thought reasoning with end-to-end driving. _arXiv preprint arXiv:2403.16996_ , 2024. 

- [263] Weiyun Wang, Zhe Chen, Wenhai Wang, Yue Cao, Yangzhou Liu, Zhangwei Gao, Jinguo Zhu, Xizhou Zhu, Lewei Lu, Yu Qiao, and Jifeng Dai. Enhancing the reasoning ability of multimodal large language models via mixed preference optimization. _arXiv preprint arXiv:2411.10442_ , 2024. 

- [264] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Jiagang Zhu, and Jiwen Lu. DriveDreamer: Towards real-world-drive world models for autonomous driving. In _Eur. Conf. Comput. Vis._ , pages 55–72. Springer, 2024. 

- [265] Yan Wang, Wenjie Luo, Junjie Bai, Yulong Cao, Tong Che, Ke Chen, Yuxiao Chen, Jenna Diamond, Yifan Ding, Wenhao Ding, Liang Feng, Greg Heinrich, Jack Huang, Peter Karkus, Boyi Li, Pinyi Li, Tsung-Yi Lin, Dongran Liu, Ming-Yu Liu, Langechuan Liu, Zhijian Liu, Jason Lu, Yunxiang Mao, Pavlo Molchanov, Lindsey Pavao, Zhenghao Peng, Mike Ranzinger, Ed Schmerling, Shida Shen, Yunfei Shi, Sarah Tariq, Ran Tian, Tilman Wekel, Xinshuo Weng, Tianjun Xiao, Eric Yang, Xiaodong Yang, Yurong You, Xiaohui Zeng, Wenyuan Zhang, Boris Ivanovic, and Marco Pavone. Alpamayo-R1: Bridging reasoning and action prediction for generalizable autonomous driving in the long tail. _arXiv preprint arXiv:2511.00088_ , 2025. 

- [266] Yuqi Wang, Jiawei He, Lue Fan, Hongxin Li, Yuntao Chen, and Zhaoxiang Zhang. Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 14749–14759, 2024. 

- [267] Julong Wei, Shanshuai Yuan, Pengfei Li, et al. OccLLaMA: An occupancy-language-action generative world model for autonomous driving. _arXiv preprint arXiv:2409.03272_ , 2024. 

- [268] Xinshuo Weng, Boris Ivanovic, Yan Wang, Yue Wang, and Marco Pavone. PARA-Drive: Parallelized architecture for real-time autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 15449–15458, 2024. 

- [269] Benjamin Wilson, William Qi, Tanmay Agarwal, John Lambert, Jagjeet Singh, Siddhesh Khandelwal, Bowen Pan, Ratnesh Kumar, Andrew Hartnett, Jhony Kaesemodel Pontes, Deva Ramanan, Peter Carr, and James Hays. Argoverse 2: Next generation datasets for self-driving perception and forecasting. _arXiv preprint arXiv:2301.00493_ , 2023. 

- [270] Katharina Winter, Mark Azer, and Fabian B. Flohr. BEVDriver: Leveraging BEV maps in LLMs for robust closed-loop driving. _arXiv preprint arXiv:2503.03074_ , 2025. 

42 

- [271] Hanfeng Wu, Marlon Steiner, Michael Schmidt, Alvaro Marcos-Ramiro, and Christoph Stiller. NaviHydra: Controllable navigation-guided end-to-end autonomous driving with hydra-distillation. _arXiv preprint arXiv:2512.10660_ , 2025. 

- [272] Penghao Wu, Xiaosong Jia, Li Chen, Junchi Yan, Hongyang Li, and Yu Qiao. Trajectory-guided control prediction for end-to-end autonomous driving: A simple yet strong baseline. In _Adv. Neural Inf. Process. Syst._ , volume 35, pages 6119–6132, 2022. 

- [273] Jihong Xie, Xiang Zhou, and Lu Cheng. Edge computing for real-time decision making in autonomous driving: Review of challenges, solutions, and future trends. _Int. J. Adv. Comput. Sci. & Appl._ , 15(7), 2024. 

- [274] Shaoyuan Xie, Lingdong Kong, Yuhao Dong, Chonghao Sima, Wenwei Zhang, Qi Alfred Chen, Ziwei Liu, and Liang Pan. Are VLMs ready for autonomous driving? an empirical study from the reliability, data, and metric perspectives. In _IEEE/CVF Int. Conf. Comput. Vis._ , pages 6585–6597, 2025. 

- [275] Shaoyuan Xie, Lingdong Kong, Wenwei Zhang, Jiawei Ren, Liang Pan, Kai Chen, and Ziwei Liu. Benchmarking and improving bird’s eye view perception robustness in autonomous driving. _IEEE Trans. Pattern Anal. Mach. Intell._ , 47(5):3878–3894, 2025. 

- [276] Yichen Xie, Runsheng Xu, Tong He, Jyh-Jing Hwang, Katie Luo, Jingwei Ji, Hubert Lin, Letian Chen, Yiren Lu, Zhaoqi Leng, Dragomir Anguelov, and Mingxing Tan. S4-Driver: Scalable self-supervised driving multimodal large language model with spatio-temporal visual representation. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 1622–1632, 2025. 

- [277] Ren Xin, Hongji Liu, Xiaodong Mei, Wenru Liu, Maosheng Ye, Zhili Chen, and Jun Ma. NetRoller: Interfacing general and specialized models for end-to-end autonomous driving. _arXiv preprint arXiv:2506.14589_ , 2025. 

- [278] Shuo Xing, Chengyuan Qian, Yuping Wang, Hongyuan Hua, Kexin Tian, Yang Zhou, and Zhengzhong Tu. OpenEMMA: Open-source multimodal model for end-to-end autonomous driving. In _IEEE/CVF Winter Conf. Appl. Comput. Vis._ , pages 1001–1009, 2025. 

- [279] Zebin Xing, Xingyu Zhang, Yang Hu, Bo Jiang, Tong He, Qian Zhang, Xiaoxiao Long, and Wei Yin. GoalFlow: Goal-driven flow matching for multimodal trajectories generation in end-to-end autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 1602–1611, 2025. 

- [280] Zebin Xing, Yupeng Zheng, Qichao Zhang, Zhixing Ding, Pengxuan Yang, Songen Gu, Zhongpu Xia, and Dongbin Zhao. Mimir: Hierarchical goal-driven diffusion with uncertainty propagation for end-to-end autonomous driving. _arXiv preprint arXiv:2512.07130_ , 2025. 

- [281] Chengkai Xu, Jiaqi Liu, Yicheng Guo, Yuhang Zhang, Peng Hang, and Jian Sun. Towards human-centric autonomous driving: A fast-slow architecture integrating large language model guidance with reinforcement learning. _arXiv preprint arXiv:2505.06875_ , 2025. 

- [282] Haoran Xu, Peixi Peng, Guang Tan, Yiqian Chang, Yisen Zhao, and Yonghong Tian. Temporal triplane transformers as occupancy world models. _arXiv preprint arXiv:2503.07338_ , 2025. 

- [283] Runsheng Xu, Hubert Lin, Wonseok Jeon, Hao Feng, Yuliang Zou, Liting Sun, John Gorman, Ekaterina Tolstaya, Sarah Tang, Brandyn White, Ben Sapp, Mingxing Tan, Jyh-Jing Hwang, and Dragomir Anguelov. WOD-E2E: Waymo open dataset for end-to-end driving in challenging long-tail scenarios. _arXiv preprint arXiv:2510.26125_ , 2025. 

- [284] Tianshuo Xu, Hao Lu, Xu Yan, Yingjie Cai, Bingbing Liu, and Yingcong Chen. Occ-LLM: Enhancing autonomous driving with occupancy-based large language models. In _IEEE Int. Conf. Robot. Autom._ , 2025. 

- [285] Xiang Xu, Lingdong Kong, Song Wang, Chuanwei Zhou, and Qingshan Liu. Beyond one shot, beyond one perspective: Cross-view and long-horizon distillation for better LiDAR representations. In _IEEE/CVF Int. Conf. Comput. Vis._ , pages 25506–25518, 2025. 

- [286] Yi Xu, Yuxin Hu, Zaiwei Zhang, Gregory P. Meyer, Siva Karthik Mustikovela, Siddhartha Srinivasa, Eric M. Wolff, and Xin Huang. VLM-AD: End-to-end autonomous driving through vision-language model supervision. _arXiv preprint arXiv:2412.14446_ , 2024. 

- [287] Zhenhua Xu, Yujia Zhang, Enze Xie, Zhen Zhao, Yong Guo, Kwan-Yee K. Wong, Zhenguo Li, and Hengshuang Zhao. DriveGPT4: Interpretable end-to-end autonomous driving via large language model. _IEEE Robot. Autom. Lett._ , 9(10):8186–8193, 2024. 

43 

- [288] Zhenhua Xu, Yan Bai, Yujia Zhang, Zhuoling Li, Fei Xia, Kwan-Yee K. Wong, Jianqiang Wang, and Hengshuang Zhao. DriveGPT4-V2: Harnessing large language model capabilities for enhanced closed-loop autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 17261–17270, 2025. 

- [289] Tianyi Yan, Tao Tang, Xingtai Gui, Yongkang Li, Jiasen Zhesng, Weiyao Huang, Lingdong Kong, Wencheng Han, Xia Zhou, Xueyang Zhang, Yifei Zhan, Kun Zhan, Cheng zhong Xu, and Jianbing Shen. AD-R1: Closedloop reinforcement learning for end-to-end autonomous driving with impartial world models. _arXiv preprint arXiv:2511.20325_ , 2025. 

- [290] Tianyi Yan, Dongming Wu, Wencheng Han, Junpeng Jiang, Xia Zhou, Kun Zhan, Cheng-zhong Xu, and Jianbing Shen. DrivingSphere: Building a high-fidelity 4D world for closed-loop simulation. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 27531–27541, 2025. 

- [291] Xu Yan, Haiming Zhang, Yingjie Cai, Jingming Guo, Weichao Qiu, Bin Gao, Kaiqiang Zhou, Yue Zhao, Huan Jin, Jiantao Gao, Zhen Li, Lihui Jiang, Wei Zhang, Hongbo Zhang, Dengxin Dai, and Bingbing Liu. Forging vision foundation models for autonomous driving: Challenges, methodologies, and opportunities. _arXiv preprint arXiv:2401.08045_ , 2024. 

- [292] Ziyang Yan, Wenzhen Dong, Yihua Shao, Yuhang Lu, Haiyang Liu, Jingwen Liu, Haozhe Wang, Zhe Wang, Yan Wang, Fabio Remondino, and Yuexin Ma. RenderWorld: World model with self-supervised 3D label. In _IEEE Int. Conf. Robot. Autom._ , pages 6063–6070, 2025. 

- [293] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, Chujie Zheng, Dayiheng Liu, Fan Zhou, Fei Huang, Feng Hu, Hao Ge, Haoran Wei, Huan Lin, Jialong Tang, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jing Zhou, Jingren Zhou, Junyang Lin, Kai Dang, Keqin Bao, Kexin Yang, Le Yu, Lianghao Deng, Mei Li, Mingfeng Xue, Mingze Li, Pei Zhang, Peng Wang, Qin Zhu, Rui Men, Ruize Gao, Shixuan Liu, Shuang Luo, Tianhao Li, Tianyi Tang, Wenbiao Yin, Xingzhang Ren, Xinyu Wang, Xinyu Zhang, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yinger Zhang, Yu Wan, Yuqiong Liu, Zekun Wang, Zeyu Cui, Zhenru Zhang, Zhipeng Zhou, and Zihan Qiu. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_ , 2025. 

- [294] An Yang et al. Qwen2.5 technical report. _arXiv preprint arXiv:2412.15115_ , 2024. 

- [295] Haohan Yang, Yanxin Zhou, Jingda Wu, Haochen Liu, Lie Yang, and Chen Lv. Human-guided continual learning for personalized decision-making of autonomous driving. _IEEE Int. Conf. Intell. Transport. Syst._ , 26(4): 5435–5447, 2025. 

- [296] Jiazhi Yang, Shenyuan Gao, Yihang Qiu, Li Chen, Tianyu Li, Bo Dai, Kashyap Chitta, Penghao Wu, Jia Zeng, Ping Luo, Jun Zhang, Andreas Geiger, Yu Qiao, and Hongyang Li. Generalized predictive model for autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 14662–14672, 2024. 

- [297] Yu Yang, Jianbiao Mei, Yukai Ma, Siliang Du, Wenqing Chen, Yijie Qian, Yuxiang Feng, and Yong Liu. Driving in the occupancy world: Vision-centric 4D occupancy forecasting and planning via world models for autonomous driving. In _AAAI Conf. Artifi. Intell._ , volume 39, pages 9327–9335, 2025. 

- [298] Zetong Yang, Li Chen, Yanan Sun, and Hongyang Li. Visual point cloud forecasting enables scalable autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 14673–14684, 2024. 

- [299] Zhenjie Yang, Yilin Chai, Xiaosong Jia, Qifeng Li, Yuqian Shao, Xuekai Zhu, Haisheng Su, and Junchi Yan. DriveMoE: Mixture-of-experts for vision-language-action model in end-to-end autonomous driving. _arXiv preprint arXiv:2505.16278_ , 2025. 

- [300] Zhenjie Yang, Xiaosong Jia, Qifeng Li, Xue Yang, Maoqing Yao, and Junchi Yan. Raw2Drive: Reinforcement learning with aligned world models for end-to-end autonomous driving (in CARLA-V2). _arXiv preprint arXiv:2505.16394_ , 2025. 

- [301] Zhenjie Yang et al. LLM4Drive: A survey of large language models for autonomous driving. In _Adv. Neural Inf. Process. Syst. Worksh._ , 2024. 

- [302] Huaiyuan Yao, Pengfei Li, Bu Jin, Yupeng Zheng, An Liu, Lisen Mu, Qing Su, Qian Zhang, Yilun Chen, and Peng Li. LiloDriver: A lifelong learning framework for closed-loop motion planning in long-tail autonomous driving scenarios. _arXiv preprint arXiv:2505.17209_ , 2025. 

- [303] Zebin You, Shen Nie, Xiaolu Zhang, Jun Hu, Jun Zhou, Zhiwu Lu, Ji-Rong Wen, and Chongxuan Li. LLaDA-V: Large language diffusion models with visual instruction tuning. _arXiv preprint arXiv:2505.16933_ , 2025. 

44 

- [304] Fisher Yu, Haofeng Chen, Xin Wang, Wenqi Xian, Yingying Chen, Fangchen Liu, Vashisht Madhavan, and Trevor Darrell. BDD100K: A diverse driving dataset for heterogeneous multitask learning. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 2636–2645, 2020. 

- [305] Lijun Yu, José Lezama, Nitesh B. Gundavarapu, Luca Versari, Kihyuk Sohn, David Minnen, Yong Cheng, Vighnesh Birodkar, Agrim Gupta, Xiuye Gu, Alexander G. Hauptmann, Boqing Gong, Ming-Hsuan Yang, Irfan Essa, David A. Ross, and Lu Jiang. Language model beats diffusion-tokenizer is key to visual generation. _arXiv preprint arXiv:2310.05737_ , 2023. 

- [306] Tianyu Yu, Haoye Zhang, Qiming Li, Qixin Xu, Yuan Yao, Da Chen, Xiaoman Lu, Ganqu Cui, Yunkai Dang, Taiwen He, Xiaocheng Feng, Jun Song, Bo Zheng, Zhiyuan Liu, Tat-Seng Chua, and Maosong Sun. RLAIF-V: Open-source AI feedback leads to super GPT-4V trustworthiness. _arXiv preprint arXiv:2405.17220_ , 2024. 

- [307] Ze Yu, Jun Li, Yuzhen Wei, Yuandong Lyu, and Xiaojun Tan. Combining camera-LiDAR fusion and motion planning using bird’s-eye view representation for end-to-end autonomous driving. _Drones_ , 9(4):281, 2025. 

- [308] Chengran Yuan, Zhanqi Zhang, Jiawei Sun, Shuo Sun, Zefan Huang, Christina Dao Wen Lee, Dongen Li, Yuhang Han, Anthony Wong, Keng Peng Tee, and Marcelo H. Ang Jr. DRAMA: An efficient end-to-end motion planner for autonomous driving with mamba. _arXiv preprint arXiv:2408.03601_ , 2024. 

- [309] Jianhao Yuan, Shuyang Sun, Daniel Omeiza, Bo Zhao, Paul Newman, Lars Kunze, and Matthew Gadd. RAGDriver: Generalisable driving explanations with retrieval-augmented in-context learning in multi-modal large language model. _arXiv preprint arXiv:2402.10828_ , 2024. 

- [310] Zhenlong Yuan, Chengxuan Qian, Jing Tang, Rui Chen, Zijian Song, Lei Sun, Xiangxiang Chu, Yujun Cai, Dapeng Zhang, and Shuo Li. AutoDrive-R2: Incentivizing reasoning and self-reflection capacity for VLA model in autonomous driving. _arXiv preprint arXiv:2509.01944_ , 2025. 

- [311] Mahmut Yurt, Xin Ye, Yunsheng Ma, Jingru Luo, Abhirup Mallik, John Pauly, Burhaneddin Yaman, and Liu Ren. LTDA-Drive: LLMs-guided generative models based long-tail data augmentation for autonomous driving. _arXiv preprint arXiv:2505.18198_ , 2025. 

- [312] Shuang Zeng, Xinyuan Chang, Mengwei Xie, Xinran Liu, Yifan Bai, Zheng Pan, Mu Xu, Xing Wei, and Ning Guo. FutureSightDrive: Thinking visually with spatio-temporal CoT for autonomous driving. _arXiv preprint arXiv:2505.17685_ , 2025. 

- [313] Mingliang Zhai, Cheng Li, Zengyuan Guo, Ningrui Yang, Xiameng Qin, Sanyuan Zhao, Junyu Han, Ji Tao, Yuwei Wu, , and Yunde Jia. World knowledge-enhanced reasoning using instruction-guided interactor in autonomous driving. In _AAAI Conf. Artifi. Intell._ , volume 39, pages 9842–9850, 2025. 

- [314] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. In _IEEE/CVF Int. Conf. Comput. Vis._ , pages 11975–11986, 2023. 

- [315] Bozhou Zhang, Nan Song, Jingyu Li, Xiatian Zhu, Jiankang Deng, and Li Zhang. Future-aware end-to-end driving: Bidirectional modeling of trajectory planning and scene evolution. _arXiv preprint arXiv:2510.11092_ , 2025. 

- [316] Dapeng Zhang, Zhenlong Yuan, Zhangquan Chen, Chih-Ting Liao, Yinda Chen, Fei Shen, Qingguo Zhou, and Tat-Seng Chua. Reasoning-VLA: A fast and general vision-language-action reasoning model for autonomous driving. _arXiv preprint arXiv:2511.19912_ , 2025. 

- [317] Diankun Zhang, Guoan Wang, Runwen Zhu, Jianbo Zhao, Xiwu Chen, Siyu Zhang, Jiahao Gong, Qibin Zhou, Wenyuan Zhang, Ningzi Wang, Feiyang Tan, Hangning Zhou, Ziyao Xu, Haotian Yao, Chi Zhang, Xiaojun Liu, Xiaoguang Di, and Bin Li. SparseAD: Sparse query-centric paradigm for efficient end-to-end autonomous driving. _arXiv preprint arXiv:2404.06892_ , 2024. 

- [318] Haiming Zhang, Ying Xue, Xu Yan, Jiacheng Zhang, Weichao Qiu, Dongfeng Bai, Bingbing Liu, Shuguang Cui, and Zhen Li. An efficient occupancy world model via decoupled dynamic flow and image-assisted training. _arXiv preprint arXiv:2412.13772_ , 2024. 

- [319] Haiming Zhang, Wending Zhou, Yiyao Zhu, Xu Yan, Jiantao Gao, Dongfeng Bai, Yingjie Cai, Bingbing Liu, Shuguang Cui, and Zhen Li. VisionPAD: A vision-centric pre-training paradigm for autonomous driving. In _IEEE/CVF Conf. Comput. Vis. Pattern Recog._ , pages 17165–17175, 2025. 

- [320] Jiawei Zhang, Xuan Yang, Taiqi Wang, Yu Yao, Aleksandr Petiushko, and Bo Li. SafeAuto: Knowledge-enhanced safe autonomous driving with multimodal foundation models. _arXiv preprint arXiv:2503.00211_ , 2025. 

45 

- [321] Kaiwen Zhang, Zhenyu Tang, Xiaotao Hu, Xingang Pan, Xiaoyang Guo, Yuan Liu, Jingwei Huang, Li Yuan, Qian Zhang, Xiao-Xiao Long, Xun Cao, and Wei Yin. Epona: Autoregressive diffusion world model for autonomous driving. _arXiv preprint arXiv:2506.24113_ , 2025. 

- [322] Peiyuan Zhang, Guangtao Zeng, Tianduo Wang, and Wei Lu. TinyLLaMA: An open-source small language model. _arXiv preprint arXiv:2401.02385_ , 2024. 

- [323] Songyan Zhang, Wenhui Huang, Zihui Gao, Hao Chen, and Chen Lv. WiseAD: Knowledge augmented end-to-end autonomous driving with vision-language model. _arXiv preprint arXiv:2412.09951_ , 2024. 

- [324] Songyan Zhang, Wenhui Huang, Zhan Chen, Chua Jiahao Collister, Qihang Huang, and Chen Lv. OpenREAD: Reinforced open-ended reasoing for end-to-end autonomous driving with LLM-as-Critic. _arXiv preprint arXiv:2512.01830_ , 2025. 

- [325] Yi Zhang, Erik Leo Haß, Kuo-Yi Chao, Nenad Petrovic, Yinglei Song, Chengdong Wu, and Alois Knoll. A unified perception-language-action framework for adaptive autonomous driving. _arXiv preprint arXiv:2507.23540_ , 2025. 

- [326] Zhejun Zhang, Alexander Liniger, Dengxin Dai, Fisher Yu, and Luc Van Gool. End-to-end urban driving by imitating a reinforcement learning coach. In _IEEE/CVF Int. Conf. Comput. Vis._ , pages 15222–15232, 2021. 

- [327] Rui Zhao, Qirui Yuan, Jinyu Li, Haofeng Hu, Yun Li, Zhenhai Gao, and Fei Gao. Sce2DriveX: A generalized MLLM framework for scene-to-drive learning. _IEEE Robot. Autom. Lett._ , 10(12):12580–12587, 2025. 

- [328] Zongchuang Zhao, Haoyu Fu, Dingkang Liang, Xin Zhou, Dingyuan Zhang, Hongwei Xie, Bing Wang, and Xiang Bai. Extending large vision-language model for diverse interactive tasks in autonomous driving. _arXiv preprint arXiv:2505.08725_ , 2025. 

- [329] Chuanxia Zheng and Andrea Vedaldi. Online clustered codebook. In _IEEE/CVF Int. Conf. Comput. Vis._ , pages 22798–22807, 2023. 

- [330] Weicheng Zheng, Xiaofei Mao, Nanfei Ye, Pengxiang Li, Kun Zhan, Xianpeng Lang, and Hang Zhao. DriveAgentR1: Advancing VLM-based autonomous driving with hybrid thinking and active perception. _arXiv preprint arXiv:2507.20879_ , 2025. 

- [331] Wenzhao Zheng, Weiliang Chen, Yuanhui Huang, Borui Zhang, Yueqi Duan, and Jiwen Lu. OccWorld: Learning a 3D occupancy world model for autonomous driving. In _Eur. Conf. Comput. Vis._ , pages 55–72. Springer, 2024. 

- [332] Wenzhao Zheng, Ruiqi Song, Xianda Guo, Chenming Zhang, and Long Chen. GenAD: Generative end-to-end autonomous driving. In _Eur. Conf. Comput. Vis._ , pages 87–104. Springer, 2024. 

- [333] Wenzhao Zheng, Junjie Wu, Yao Zheng, Sicheng Zuo, Zixun Xie, Longchao Yang, Yong Pan, Zhihui Hao, Peng Jia, Xianpeng Lang, and Shanghang Zhang. GaussianAD: Gaussian-centric end-to-end autonomous driving. _arXiv preprint arXiv:2412.10371_ , 2024. 

- [334] Wenzhao Zheng, Zetian Xia, Yuanhui Huang, Sicheng Zuo, Jie Zhou, and Jiwen Lu. Doe-1: Closed-loop autonomous driving with large world model. _arXiv preprint arXiv:2412.09627_ , 2024. 

- [335] Yupeng Zheng, Pengxuan Yang, Zebin Xing, Qichao Zhang, Yuhang Zheng, Yinfeng Gao, Pengfei Li, Teng Zhang, Zhongpu Xia, Peng Jia, XianPeng Lang, and Dongbin Zhao. World4Drive: End-to-end autonomous driving via intention-aware physical latent world model. In _IEEE/CVF Int. Conf. Comput. Vis._ , pages 28632–28642, 2025. 

- [336] Yifan Zhong et al. Yifan zhong and fengshuo bai and shaofei cai and xuchuan huang and zhang chen and xiaowei zhang and yuanfei wang and shaoyang guo and tianrui guan and ka nam lui and zhiquan qi and yitao liang and yuanpei chen and yaodong yang. _arXiv preprint arXiv:2507.01925_ , 2025. 

- [337] Gaoyue Zhou, Hengkai Pan, Yann LeCun, and Lerrel Pinto. DINO-WM: World models on pre-trained visual features enable zero-shot planning. In _Int. Conf. Mach. Learn._ PMLR, 2025. 

- [338] Xingcheng Zhou, Mingyu Liu, Ekim Yurtsever, Bare Luka Zagar, Walter Zimmer, Hu Cao, and Alois C. Knoll. Vision language models in autonomous driving: A survey and outlook. _IEEE Trans. Intell. Veh._ , pages 1–20, 2024. 

- [339] Xingcheng Zhou, Xuyuan Han, Feng Yang, Yunpu Ma, Volker Tresp, and Alois Knoll. OpenDriveVLA: Towards end-to-end autonomous driving with large vision language action model. _arXiv preprint arXiv:2503.23463_ , 2025. 

- [340] Zewei Zhou, Tianhui Cai, Seth Z. Zhao, Yun Zhang, Zhiyu Huang, Bolei Zhou, and Jiaqi Ma. AutoVLA: A vision-language-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. _arXiv preprint arXiv:2506.13757_ , 2025. 

46 

- [341] Bin Zhu, Bin Lin, Munan Ning, Yang Yan, Jiaxi Cui, HongFa Wang, Yatian Pang, Wenhao Jiang, Junwu Zhang, Zongwei Li, Wancai Zhang, Zhifeng Li, Wei Liu, and Li Yuan. LanguageBind: Extending video-language pretraining to N-modality by language-based semantic alignment. In _Int. Conf. Learn. Represent._ , 2024. 

- [342] Dekai Zhu, Yixuan Hu, Youquan Liu, Dongyue Lu, Lingdong Kong, and Slobodan Ilic. SPIRAL: Semantic-aware progressive LiDAR scene generation and understanding. In _Adv. Neural Inf. Process. Syst._ , volume 38, 2025. 

- [343] Jinguo Zhu, Weiyun Wang, Zhe Chen, Zhaoyang Liu, Shenglong Ye, Lixin Gu, Hao Tian, Yuchen Duan, Weijie Su, Jie Shao, Zhangwei Gao, Erfei Cui, Xuehui Wang, Yue Cao, Yangzhou Liu, Xingguang Wei, Hongjie Zhang, Haomin Wang, Weiye Xu, Hao Li, Jiahao Wang, Nianchen Deng, Songze Li, Yinan He, Tan Jiang, Jiapeng Luo, Yi Wang, Conghui He, Botian Shi, Xingcheng Zhang, Wenqi Shao, Junjun He, Yingtong Xiong, Wenwen Qu, Peng Sun, Penglong Jiao, Han Lv, Lijun Wu, Kaipeng Zhang, Huipeng Deng, Jiaye Ge, Kai Chen, Limin Wang, Min Dou, Lewei Lu, Xizhou Zhu, Tong Lu, Dahua Lin, Yu Qiao, Jifeng Dai, and Wenhai Wang. InternVL3: Exploring advanced training and test-time recipes for open-source multimodal models. _arXiv preprint arXiv:2504.10479_ , 2025. 

- [344] Huiping Zhuang, Di Fang, Kai Tong, Yuchen Liu, Ziqian Zeng, Xu Zhou, and Cen Chen. Online analytic exemplar-free continual learning with large models for imbalanced autonomous driving task. _IEEE Trans. Veh. Tech._ , 74(2):1949–1958, 2024. 

- [345] Jialv Zou, Shaoyu Chen, Bencheng Liao, Zhiyu Zheng, Yuehao Song, Lefei Zhang, Qian Zhang, Wenyu Liu, and Xinggang Wang. DiffusionDriveV2: Reinforcement learning-constrained truncated diffusion modeling in end-to-end autonomous driving. _arXiv preprint arXiv:2512.07745_ , 2025. 

47 

