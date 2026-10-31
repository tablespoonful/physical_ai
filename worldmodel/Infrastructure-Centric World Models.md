---
title: "Infrastructure-Centric World Models: Bridging Temporal Depth and Spatial Breadth for Roadside Perception"
date: "2026-04-19"
authors: "Siyuan Meng; Chengbo Ai"
url: https://arxiv.org/abs/2604.17651
pdf: https://arxiv.org/pdf/2604.17651
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.17651)** / [論文ページ](https://arxiv.org/abs/2604.17651)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Infrastructure-Centric World Models: Bridging Temporal Depth and Spatial Breadth for Roadside Perception** 

Siyuan Meng<sup>∗1</sup> and Chengbo Ai<sup>1</sup> 

> 1Department of Civil and Environmental Engineering, University of Massachusetts Amherst 

##### **Abstract** 

World models,generative AI systems that learn to simulate how environments evolve,have emerged as a cornerstone of next-generation autonomous driving, exemplified by the Waymo World Model, NVIDIA Cosmos, and a rapidly growing body of academic work (HERMES, ResWorld, DriveVLA-W0). However, all existing driving world models adopt an _ego-vehicle_ perspective, leaving the infrastructure viewpoint entirely unexplored. We argue that infrastructurecentric world models offer a fundamentally different and complementary capability: the bird’seye, multi-sensor, persistent viewpoint that roadside systems uniquely possess. Central to our thesis is a _fundamental spatio-temporal complementarity_ : fixed roadside sensors excel at **temporal depth** ,accumulating long-term behavioral distributions including rare safety-critical events at specific locations,while vehicle-borne sensors excel at **spatial breadth** ,sampling diverse scenes across large road networks. Neither platform alone can learn a complete model of traffic dynamics. This paper presents a research vision for developing Infrastructure-centric World Models (I-WM) organized in three phases: (I) generative scene understanding with qualityaware uncertainty propagation, (II) physics-informed predictive dynamics with multi-agent counterfactual reasoning, and (III) collaborative world models for vehicle-to-everything (V2X) communication via latent space alignment. We propose a dual-layer architecture,modular, annotation-free perception as a multi-modal data engine feeding end-to-end generative world models,accompanied by a phased multi-modal sensor strategy that progresses from LiDARcentric core sensing through 4D radar and signal phase data to forward-looking modalities including event cameras and environmental sensors. We establish a taxonomy of driving world model paradigms, position I-WM relative to LeCun’s JEPA framework, Li Fei-Fei’s spatial intelligence vision, and Vision-Language-Action architectures, and introduce the concept of **Infrastructure VLA (I-VLA)** as a novel unification of roadside perception, natural language commands, and traffic control actions. Our vision builds upon existing multi-LiDAR perception pipelines (FRGB3D, MulDet3D, MulTrack3D) and identifies concrete open-source foundations (DynamicCity, OccWorld, CarDreamer) for each phase, providing an actionable path toward intelligent infrastructure that does not merely observe traffic but understands and anticipates it. 

**Keywords:** World Models, Infrastructure-Centric Perception, Roadside LiDAR, Multi-Modal Sensing, V2X Cooperative Perception, Spatial Intelligence, 4D Occupancy Forecasting 

## **1 Introduction** 

Current roadside perception systems primarily focus on instantaneous object detection and tracking. However, they lack a deep understanding of the “rules of the world”,such as physical constraints, 

> ∗Corresponding author. Email: `siyuanmeng@umass.edu` 

1 

causal relationships, and intent prediction. Meanwhile, industry leaders such as Waymo have recently introduced vehicle-centric world models built upon foundation models like Google DeepMind’s Genie 3, demonstrating the power of generative simulation for autonomous driving safety validation [38]. Concurrently, NVIDIA’s Cosmos platform [26] has established open-weight world foundation models for physical AI, while a rapidly growing body of work,including HERMES [51], ResWorld [45], and DriveVLA-W0 [22],continues to push the frontier of vehicle-centric driving world models. 

This paper proposes a 5-year research trajectory to develop **Infrastructure-centric World Models (I-WM)** that offer a fundamentally different and complementary perspective: the _bird’seye, multi-sensor, persistent_ viewpoint that roadside systems uniquely possess. Unlike ego-vehicle world models that reason about the immediate surroundings of a single agent, I-WM reasons about the _entire traffic ecosystem_ ,enabling predictive analytics, proactive safety interventions, and cognitive V2X collaboration. Central to our thesis is a **fundamental spatio-temporal complementarity** : roadside systems excel at _temporal depth_ ,accumulating long-term behavioral distributions at fixed locations,while vehicle-based systems excel at _spatial breadth_ ,sampling diverse scenes across large road networks. The I-WM framework is designed to harness this complementarity as a firstclass design principle. 

Architecturally, we advocate a **dual-layer design** that separates concerns between perception and world modeling. The _perception layer_ employs modular, unsupervised methods,background modeling (FRGB3D), multi-objective detection (MulDet3D), and consensus-based tracking (MulTrack3D),that operate without manual annotation and can be rapidly deployed at new sites. These serve as a structured _data engine_ , providing the world model with high-quality, uncertainty-annotated observations (3D detections, trajectories, static scene priors). The _world model layer_ then builds upon these structured inputs using end-to-end generative architectures,diffusion-based 4D scene generation, autoregressive occupancy forecasting, and self-supervised latent dynamics,to learn scene evolution, counterfactual reasoning, and future prediction. This separation is deliberate: roadside deployment demands annotation-free perception (since each new intersection lacks labeled data), while world models benefit from end-to-end learning over the structured representations that the perception layer produces. In the longer term, we envision a fully end-to-end roadside foundation model that unifies both layers, but the dual-layer approach provides an actionable near-term path that leverages existing validated components. 

## **2 Industry Context: Why Infrastructure-Centric?** 

The recent release of the Waymo World Model (February 2026) marks a milestone for vehicle-centric generative simulation. Built on Genie 3, it generates photorealistic camera and LiDAR data for rare edge-case scenarios, supports counterfactual reasoning via driving action control, and enables language-conditioned scene editing. However, Waymo’s approach is fundamentally _ego-centric_ ,it models the world from a single vehicle’s perspective. 

**Infrastructure-centric and vehicle-centric world models are complementary, not competing.** The roadside “God’s-eye view” resolves occlusions invisible to any single vehicle, provides persistent monitoring across all traffic participants, and enables system-level optimization (e.g., signal control) that ego-centric models cannot achieve. Table 1 summarizes these differences. 

### **2.1 Temporal Depth vs. Spatial Breadth: The Fundamental Complementarity** 

Beyond the functional differences outlined in Table 1, roadside and vehicle-based sensing exhibit a deeper **epistemological complementarity** rooted in their deployment geometry,one that deter- 

2 

Table 1: Positioning: Vehicle-Centric vs. Infrastructure-Centric World Models. 

|**Dimension**|**Waymo World Model**<br>**(Vehicle-Centric)**|**I-WM (Infrastructure-Centric)**|
|---|---|---|
|Viewpoint|Ego-vehicle perspective|Bird’s-eye / multi-sensor panoramic|
|Core Strength|Fine-grained ego-surroundings<br>modeling|Global traffic situational awareness|
|Data Foundation|_∼_200M miles of fleet driving data|Long-term fixed-site deployment<br>data|
|Occlusion Handling|Limited by ego viewpoint|Multi-angle occlusion completion|
|Control<br>Dimensions|Ego driving actions|Traffic signals + multi-agent<br>control|
|Uncertainty<br>Modeling|No explicit reliability propagation|Quality-aware framework<br>throughout|
|Counterfactual<br>Scope|Single ego-vehicle “what-if”|Multi-agent, system-level “what-if”|
|Downstream Users|Single-vehicle autonomy|Traffic management, V2X, urban<br>planning|
|Foundation Model|Genie 3 post-training|Open foundation models +<br>roadside post-training|


mines what each platform can _learn_ about traffic dynamics. 

**Roadside LiDAR: Temporal Deep Wells.** A fixed roadside sensor continuously observes the _same_ spatial region over days, weeks, or months. This produces a **temporal deep well** ,a dense time-series at a single location that captures the complete probability distribution of traffic behaviors, including the critical long tail of rare events (near-misses, wrong-way entries, jaywalking). Such temporal depth enables: (1) _scene normality modeling_ ,learning what “normal” looks like at a specific intersection (cf. FRGB3D background models), so that deviations can be detected and quantified; (2) _rare-event statistics_ ,accumulating sufficient samples of near-crash scenarios that a single passing vehicle would never encounter at the same location; and (3) _counterfactual baselines_ ,when a near-miss occurs, the model can compare against the site’s empirical behavioral distribution to ask “what if the driver had not braked?”,a form of infrastructure-enabled counterfactual reasoning that is infeasible from a transient vehicle perspective. 

**Vehicle-Borne LiDAR: Spatial Wide Nets.** A vehicle-mounted sensor traverses _many_ locations but observes each only briefly. This produces a **spatial wide net** ,a broad but shallow sampling of the road network that captures geometric diversity (road types, lane configurations, urban vs. rural), but offers only a snapshot of behavioral dynamics at any single point. 

**Implications for World Model Design.** This complementarity has concrete architectural consequences. Roadside I-WM learns _deep temporal priors_ ,how traffic evolves over time at a specific location, including diurnal patterns, weather-induced behavioral changes, and conflict precursors. These priors are location-specific but temporally rich. Vehicle-centric WM learns _broad spatial priors_ ,what different road geometries look like, how lane configurations affect behavior, and how scenes vary across a city. These priors are spatially diverse but temporally shallow. Fused world models 

3 

(Phase III of our roadmap) can inherit temporal depth from roadside and spatial breadth from vehicles, achieving a level of environmental understanding that neither platform can reach alone. 

**Data Efficiency Argument.** A single roadside deployment operating for one week at a busy intersection can observe thousands of unique vehicle-vehicle interactions, including dozens of conflict events. Achieving comparable behavioral diversity from a vehicle platform would require driving hundreds of kilometers through similar intersections,and even then, the vehicle would lack the repeated-observation advantage needed to estimate behavioral distributions. This **data efficiency** is a key practical motivation for infrastructure-centric world models, particularly for safety-critical applications where rare events matter most. 

## **3 Related Work** 

The proposed I-WM research vision draws on and extends several active lines of research. This section reviews the most relevant prior work across seven pillars and establishes a taxonomy of existing driving world models. 

### **3.1 World Models for Autonomous Driving** 

The concept of _world models_ ,internal simulators that predict how the environment evolves,has gained significant traction in autonomous driving. Recent surveys provide comprehensive overviews of the field [6, 8, 11, 33], while a dedicated review on connected automated vehicle scenarios highlights the potential of world models for cooperative perception and V2X applications [35]. Representative vehicle-centric world models include GAIA-1 [14], which generates realistic driving videos conditioned on actions and text; Vista [10], a generalizable driving world model with versatile controllability; DriveDreamer [36], which leverages structured traffic constraints; and Epona [49], an autoregressive diffusion model supporting minute-long horizon generation. 

More recently, several works have pushed the frontier of unified scene understanding and generation. HERMES [51] (ICCV 2025) presents a unified driving world model that simultaneously handles 3D scene understanding and future scene generation through BEV representations and LLM-based world queries, achieving state-of-the-art results on nuScenes. ResWorld [45] (ICLR 2026) introduces temporal residual modeling that separates dynamic objects from static backgrounds,an idea conceptually related to our FRGB3D background subtraction but applied in latent BEV space for end-to-end planning. DriveVLA-W0 [22] (ICLR 2026) demonstrates that world models can amplify data scaling laws for autonomous driving by combining vision-language-action architectures with latent world modeling. 

At the industry level, NVIDIA’s Cosmos platform [26] has established open-weight world foundation models trained on 9,000 trillion tokens from 20 million hours of real-world data, providing a general-purpose WFM that can be fine-tuned for domain-specific applications. However, **all existing driving world models,both academic and industrial,adopt an ego-vehicle perspective** , leaving infrastructure-centric world modeling as a significant and timely gap. 

### **3.2 4D Occupancy Forecasting** 

Predicting volumetric occupancy over time is a core capability for any world model. OccWorld [50] pioneered GPT-style autoregressive forecasting in 3D occupancy space, while Drive-OccWorld [42] extended this paradigm to end-to-end planning by integrating action-conditioned generation with an occupancy-based planner. DriveWorld [24] proposed 4D pre-training for scene understanding 

4 

via world models. These methods demonstrate that dense occupancy representations can serve as a powerful “canvas” for world model rollouts. Our I-WM adapts this idea to the roadside setting, where the fixed, elevated viewpoint enables more complete occupancy estimation with fewer occlusions. 

### **3.3 Neural Scene Reconstruction and LiDAR Generation** 

Generating realistic sensor data is essential for simulation-based training. NeRF-LiDAR [46] demonstrated that Neural Radiance Fields can produce LiDAR point clouds nearly indistinguishable from real data. In the diffusion model family, LiDAR Diffusion Models [28] introduced scene-level conditional generation on KITTI, LidarDM [54] achieved layout-aware 4D LiDAR video generation, and RangeLDM [15] proposed fast range-view generation with structural fidelity. The Waymo World Model [38] extends this line by jointly generating camera and LiDAR data from Genie 3 posttraining. An emerging trend is _multi-modal sensor generation_ : as world models move toward richer sensory outputs, 4D millimeter-wave radar is gaining attention as a complementary modality. Recent surveys [7] document rapid progress in 4D radar perception, while learning-based radar data generation methods are beginning to close the sim-to-real gap for radar point clouds. Our roadmap builds on these advances but targets generation from the _roadside_ perspective, with multi-modal outputs (LiDAR + camera + radar) and the additional requirement of quality-aware (uncertaintyannotated) synthetic data. 

### **3.4 Physics-Informed Deep Learning and RL-Based Traffic Control** 

Integrating traffic flow theory into neural networks has emerged as a promising paradigm. Raissi et al. [27] established the foundational Physics-Informed Neural Networks (PINNs) framework. In transportation, Di et al. [5] surveyed PIDL architectures for traffic state estimation, proposing hybrid computational graphs that combine physics-based and data-driven components. STDEN [18] embeds differential equation-based traffic dynamics into neural ODE solvers for flow prediction, while Zhang et al. [47] developed computational graph methods that encode LWR and ARZ traffic models into deep learning pipelines. These physics-informed approaches directly inform our Phase II design (Section 5.2) of latent dynamics with physical constraints ( _L_ physics) and counterfactual reasoning capabilities. 

Complementarily, reinforcement learning (RL) for traffic signal control has matured into a rich field, with recent surveys [25] documenting the evolution from single-agent DQN approaches to multi-agent architectures using graph neural networks and hierarchical RL for large-scale network coordination [31]. These RL-based signal control methods are directly relevant to our Phase II closed-loop infrastructure simulation, where the world model serves as a “mental simulator” for the signal controller. Integrating a learned world model with RL-based signal optimization,replacing the traditional traffic simulator with a generative world model,represents a key innovation of the I-WM framework, enabling model-predictive control that anticipates traffic dynamics informed by Signal Phase and Timing (SPaT) data. 

### **3.5 Cooperative Perception and V2X Communication** 

Vehicle-to-Everything (V2X) cooperative perception has become a rapidly growing field. Huang et al. [17] provide a comprehensive survey covering agent selection, data alignment, and fusion strategies. Key datasets include DAIR-V2X [43], V2X-Seq [44], V2X-Real [40], and V2XScenes [34] (ICCV 2025). V2X-ViT [41] introduced vision transformers for cooperative perception, and UniV2X [20] demonstrated end-to-end autonomous driving through V2X cooperation. Recent ICCV 2025 workshop challenges [13] further highlight the community’s growing interest. Notably, V2X-R [16] 

5 

(CVPR 2025) introduced cooperative LiDAR-4D radar fusion for 3D object detection using denoising diffusion, demonstrating that 4D radar can enhance cooperative perception robustness in adverse conditions,directly supporting our multi-modal sensor strategy (Section 4.3). While these works focus on _perception-level_ fusion, our Phase III proposes a deeper form of collaboration, _world model alignment_ ,where infrastructure and vehicles share compressed latent representations of their respective world models. 

### **3.6 Taxonomy: Three Paradigms of Driving World Models** 

Despite the rapid proliferation of driving world models, existing literature lacks a clear taxonomy that relates their architectural choices to their downstream purposes. We identify three distinct paradigms, summarized in Table 2. 

**Paradigm A: Video Generation World Models.** This paradigm treats world modeling as a conditional video prediction problem. Representative methods include LingBot-World [29], GAIA1 [14], Vista [10], Epona [49], and NVIDIA Cosmos [26]. These models excel at visual fidelity and long-horizon generation, but operate in 2D pixel space and lack explicit 3D geometric understanding, limiting their utility for safety-critical spatial reasoning tasks. 

**Paradigm B: 3D/4D Scene Generation World Models.** This paradigm generates or predicts directly in 3D volumetric space. DynamicCity [4] (ICLR 2025 Spotlight) introduced HexPlanebased 4D occupancy generation with DiT-based diffusion. OccWorld [50] pioneered autoregressive 3D occupancy forecasting, Copilot4D [48] demonstrated unsupervised LiDAR world models, and HERMES [51] (ICCV 2025) unifies 3D scene understanding and generation through BEV representations. HunyuanWorld [32] and UrbanWorld [30] generate explorable 3D environments. These models preserve true 3D geometry, enabling physically meaningful downstream applications. 

**Paradigm C: Decision/Planning-Oriented World Models.** This paradigm treats the world model as an internal simulator for RL agents. CarDreamer [9] provides an open-source platform integrating DreamerV2/V3 with CARLA. Drive-WM [37] (CVPR 2024) pioneered multiview forecasting with planning. DreamerV3 [12] (Nature 2025) demonstrated mastery of diverse control tasks. ResWorld [45] (ICLR 2026) bridges Paradigms B and C via temporal residuals, and DriveVLAW0 [22] (ICLR 2026) unifies world modeling with VLA architectures. 

### **3.7 Broader AI Landscape: JEPA, Spatial Intelligence, and VLA** 

Beyond driving-specific world models, three broader research threads shape the conceptual foundations of our I-WM. 

**LeCun’s JEPA Framework.** Yann LeCun’s Joint-Embedding Predictive Architecture (JEPA) [19] proposes that world models should predict in _abstract representation spaces_ rather than in pixel or token spaces. This vision has materialized through I-JEPA [1] for images, V-JEPA 2 [2] for video understanding and action anticipation, and LeWorldModel (LeWM) [23], the first JEPA that trains stably end-to-end from raw pixels using only two loss terms (a prediction loss and a Gaussian regularizer based on SIGReg [3]), achieving 48 _×_ faster planning than foundation-model-based alternatives. 

JEPA’s core principle,predicting in latent space rather than reconstructing observations,directly aligns with our Phase II latent dynamics formulation ( _zt_ +1 = _T_ ( _zt, at, η_ )). However, JEPA methods 

6 

Table 2: Taxonomy of Driving World Model Paradigms. 

||**A: Video**<br>**Generation**|**B: 3D/4D Scene**<br>**Gen.**|**C: Decision/Planning**|
|---|---|---|---|
|Output Space|2D video frames|3D occupancy /<br>point clouds|Latent states + actions|
|Core Strength|Visual fidelity, long<br>horizon|Geometric accuracy,<br>physics|Sample-efficient RL|
|3D Geometry|Implicit only|Explicit|Abstract (latent)|
|Open-Source|LingBot-World,|DynamicCity,|CarDreamer, DreamerV3,|
|Rep.|Vista, Cosmos|OccWorld,<br>HERMES,<br>UrbanWorld|ResWorld, DriveVLA-W0|
|Limitations|No true 3D<br>reasoning|Computationally<br>expensive|Not visually interpretable|
|**I-WM**|Reference for|**Primary**|Phase II control|
|**Relevance**|generation|**foundation**||


currently operate in modality-agnostic latent spaces without explicit 3D geometry, which is insufficient for distance-based safety metrics (TTC, PET). Our I-WM bridges this gap by adopting JEPA’s latent prediction philosophy within a _geometrically explicit_ 3D/4D representation (Paradigm B). LeWM’s SIGReg regularizer can be directly applied to stabilize training of our HexPlane latent representations, and V-JEPA 2’s self-supervised video encoder offers a promising initialization strategy for the camera branch of our multi-modal roadside encoder. 

**Li Fei-Fei’s Spatial Intelligence.** Fei-Fei Li’s concept of _spatial intelligence_ [21] argues that AI must move beyond language to develop a grounded understanding of 3D physical environments,encompassing geometry, semantics, physics, and dynamics. World Labs’ Marble model [39] operationalizes this vision by generating persistent, editable 3D environments from text, images, or video, with hybrid editing tools that decouple spatial structure from visual style. 

We argue that **roadside infrastructure is the ideal platform for spatial intelligence in transportation** : the fixed bird’s-eye viewpoint, multi-sensor coverage, and persistent observation provide the most complete and least occluded 3D understanding of traffic scenes. While World Labs targets general-purpose spatial AI, our I-WM represents a _domain-specific spatial intelligence_ optimized for transportation safety,where the temporal-depth advantage (Section 2.1) provides behaviorally rich training data that general-purpose models cannot match. 

**Vision-Language-Action (VLA) Models and Infrastructure VLA.** The VLA paradigm [22] unifies visual perception, language understanding, and action generation. Current VLA models define “action” as ego-vehicle driving commands. We propose reconceptualizing this for the infrastructure domain as **Infrastructure VLA (I-VLA)** , where: _Vision_ = multi-LiDAR + camera roadside perception; _Language_ = natural language scene descriptions and traffic management commands; and _Action_ = infrastructure control decisions (signal phase optimization, dynamic speed limits, variable message signs, incident alerts). This I-VLA formulation emerges naturally from our phased roadmap and represents a novel contribution entirely absent from the current literature, where all VLA models assume an ego-vehicle agent. 

7 

Table 3: Open-Source Foundations for I-WM Development. 

|**Open-Source**<br>**Model**|**Venue / Year**|**Target Phase**|**Components to Adapt**|
|---|---|---|---|
|DynamicCity [4]|ICLR 2025<br>Spotlight|Phase I (core)|HexPlane 4D repr.; DiT<br>diffusion; trajectory<br>conditioning|
|OccWorld [50]|ECCV 2024|Phase I|GPT-style autoregressive<br>occupancy forecasting|
|Copilot4D [48]|ICLR 2024|Phase I|Unsupervised discrete<br>diffusion for LiDAR|
|LidarDM [54]|ICRA 2025|Phase I|Layout-aware 4D LiDAR<br>generation|
|HERMES [51]|ICCV 2025|Phase I–II|BEV tokenizer; LLM world<br>queries|
|NVIDIA<br>Cosmos [26]|CES 2025|Phase I (ref.)|Open-weight WFM;<br>fine-tuning framework|
|CarDreamer [9]|IEEE IoT 2024|Phase II–III|Gym interface;<br>DreamerV2/V3; V2X<br>sharing|
|ResWorld [45]|ICLR 2026|Phase II|Temporal residual BEV<br>modeling|


**Summary of Gaps.** Despite significant progress across vehicle-centric world models, physicsinformed traffic modeling, V2X cooperative perception, and broader AI paradigms including JEPA, spatial intelligence, and VLA, no existing work has combined these threads into an infrastructurecentric world model with quality-aware uncertainty propagation and V2X latent sharing. The fundamental temporal-depth advantage of fixed roadside deployment remains entirely unexploited. This paper aims to fill precisely this gap. 

## **4 Technical Positioning and Data Strategy** 

### **4.1 I-WM Technical Positioning** 

Our Infrastructure-centric World Model is positioned as **Paradigm B (3D/4D Scene Generation) as the primary foundation, augmented with elements from Paradigm C (Decision/Planning)** for closed-loop infrastructure control. This choice is driven by three requirements: (1) roadside safety metrics (TTC, PET) require accurate 3D positions and velocities; (2) our core data modality is multi-LiDAR point clouds, for which Paradigm B models provide the most natural representation; and (3) propagating spatially-varying uncertainty requires explicit 3D representations where confidence can be associated with each voxel or point. 

Table 3 identifies the open-source models most relevant to each phase of our research roadmap. 

**Core Technical Strategy.** Our I-WM adopts a dual-layer architecture (Figure 1) that cleanly separates _perception_ from _world modeling_ . The perception layer,comprising FRGB3D (background modeling), MulDet3D (unsupervised detection), and MulTrack3D (consensus tracking),operates without manual annotation and produces structured, uncertainty-annotated representations: 3D 

8 

##### **Dual-Layer I-WM Architecture (Conceptual Overview)** 

**Layer 1: Modular Perception (Data Engine)** , _Unsupervised, annotation-free, site-adaptive_ FRGB3D Multi-Modal Inputs (LiDAR + Camera + 4D Radar + SPaT) _−−−−−−→_ Static Scene Prior + ForeMulDet3D MulTrack3D ground Segments _−−−−−−→_ 3D Detections with Uncertainty _−−−−−−−−→_ Trajectories with Quality Scores �� _Structured, uncertainty-annotated, multi-modal observations_ **Layer 2: Generative World Model (End-to-End, Self-Supervised)** Phase I Phase II Structured Observations _−−−−−→_ 4D Occupancy Forecasting + Scene Generation _−−−−−→_ PhysicsPhase III Informed Latent Dynamics + Counterfactual Reasoning + Language Control _−−−−−−→_ V2X World Model Alignment + I-VLA 

Figure 1: Conceptual overview of the dual-layer I-WM architecture. Layer 1 provides annotationfree, multi-modal perception as a data engine; Layer 2 builds end-to-end generative world models on top of the structured representations. 

bounding boxes, trajectories, static scene priors, and per-point reliability scores. These serve as the _observation model_ and _data engine_ for the world model layer, which employs end-to-end generative architectures trained via self-supervised objectives (predicting future occupancy from past observations,no human labels required). This separation is strategically motivated: roadside perception must be annotation-free for scalable deployment across diverse intersections, while world models benefit from end-to-end learning over the rich structured representations that the perception layer provides. 

Concretely, Phase I adapts DynamicCity’s HexPlane VAE + DiT generation framework from the ego-vehicle to the roadside multi-LiDAR domain, adding quality-aware uncertainty channels, informed by HERMES’s unified understanding-generation paradigm. Phase II integrates CarDreamer’s RL-based planning loop with physics-informed latent dynamics, leveraging ResWorld’s temporal residual approach and LeWM’s SIGReg regularizer. Phase III develops cross-domain world model alignment protocols for V2X latent sharing, enabling roadside temporal priors to complement vehicle spatial priors. 

### **4.2 Data Acquisition Strategy** 

Training an infrastructure-centric world model requires large-scale, multi-modal data from the roadside perspective. We adopt a **three-tier data strategy** : 

**Tier 1: Proprietary Multi-LiDAR Roadside Data.** Our existing deployments provide multiLiDAR synchronized point clouds with overlapping fields of view, quality-aware annotations with per-point reliability scores, 3D bounding boxes and trajectories from MulDet3D and MulTrack3D, background models from FRGB3D, and continuous multi-day recordings providing the complete behavioral distribution needed to train temporal priors. 

**Tier 2: Public Roadside and V2X Datasets.** Key public datasets include DAIR-V2X [43] (71K frames, 28 intersections), V2X-Seq [44] (15K frames, sequential perception), TUMTraf-V2X [53] and TUMTraf-I [52] (multi-sensor roadside benchmarks), V2X-Real [40] (33K LiDAR frames, multimode cooperation), and V2XScenes [34] (challenging multi-condition traffic). 

9 

**Tier 3: Simulation-Generated Synthetic Data.** CARLA-based roadside simulation provides data with perfect ground truth labels, controllable conditions, and programmable rare events. World model self-play (bootstrap) enables the trained I-WM to generate additional synthetic training data. 

### **4.3 Multi-Modal Sensor Strategy** 

A world model’s ability to understand and predict the physical world depends critically on the richness of its sensory input. We adopt a **phased multi-modal strategy** organized into three tiers of sensor modalities, reflecting both deployment readiness and value to the world model. 

**Core Modalities: Multi-LiDAR + RGB Camera.** Multi-LiDAR point clouds form the geometric backbone of I-WM, providing precise 3D structure essential for safety metrics (TTC, PET). RGB cameras complement LiDAR with dense appearance and semantic information (lane markings, traffic signs, pedestrian intent cues). Phase I begins as _LiDAR-centric_ , leveraging our existing perception pipeline, and progressively incorporates synchronized cameras for joint LiDAR-camera world model training as deployment sites are augmented. 

**Extended Modalities: 4D Radar + Signal Phase and Timing (SPaT).** Two additional modalities offer high value with low deployment barrier: 

- **4D millimeter-wave radar** provides Doppler velocity measurements that neither LiDAR nor camera directly offer,critical for the world model’s dynamic prediction. Equally important, radar maintains performance in adverse weather (rain, fog, snow) where LiDAR degrades significantly, providing a natural reliability complement within our quality-aware framework. Recent work on cooperative LiDAR-4D radar fusion [16] (CVPR 2025) demonstrates the feasibility of this combination in V2X settings. 

- **Signal Phase and Timing (SPaT) data** from traffic signal controllers provides the single most important _causal variable_ governing intersection behavior. Without SPaT, the world model must implicitly infer signal state from vehicle behavior,an unnecessary ambiguity. With SPaT, Phase II counterfactual reasoning can directly explore signal-conditioned scenarios (“what if the signal had turned red 5 seconds earlier?”), and Phase II closed-loop simulation can jointly optimize signal timing and safety. SPaT data is typically available at zero marginal cost from existing signal controller infrastructure. 

**Forward-Looking Modalities: Event Cameras + Environmental Sensors.** For longerterm exploration: (1) _event cameras_ offer microsecond-level temporal resolution for capturing fast dynamics (sudden braking, collision instants) that conventional cameras miss at standard frame rates; and (2) _environmental sensors_ (temperature, precipitation, visibility, road surface condition) provide conditioning variables for weather-aware world modeling,the same intersection exhibits fundamentally different behavioral distributions on dry versus icy pavement. These modalities are included in the Phase II–III timeline as deployment infrastructure matures. 

Table 4 summarizes the multi-modal strategy and its relationship to the I-WM development phases. 

10 

Table 4: Phased Multi-Modal Sensor Strategy for I-WM. 

|**Tier**|**Modalities**|**Key Contribution**<br>**to WM**|**Deployment Phase**|
|---|---|---|---|
|Core|Multi-LiDAR,<br>RGB Camera|3D geometry,<br>appearance, semantics|Phase I (LiDAR first,<br>camera added<br>progressively)|
|Extended|4D Radar, SPaT|Doppler velocity,<br>weather robustness,<br>causal signal state|Phase I–II|
|Forward-<br>Looking|Event Camera,<br>Environmental<br>Sensors|Microsecond<br>dynamics,<br>weather-conditioned<br>behavioral priors|Phase II–III|


## **5 Research Vision** 

### **5.1 Phase I: Generative Scene Understanding (Years 1–2)** 

_Goal: Solving data scarcity through high-fidelity reconstruction and generation, with built-in reliability quantification. The world model layer is trained end-to-end via self-supervised objectives,predicting future scene states from past observations,without requiring manual annotation beyond what the perception layer already provides._ 

**Foundation Model Adaptation.** Following the paradigm demonstrated by Waymo (Genie 3 _→_ driving domain) and NVIDIA Cosmos (general WFM _→_ domain-specific fine-tuning), we adopt a two-stage strategy: leverage open-source 3D/4D foundation models,specifically DynamicCity’s HexPlane VAE and DiT diffusion framework [4],then perform domain adaptation using our multiLiDAR roadside datasets. The perception layer (FRGB3D, MulDet3D, MulTrack3D) automatically generates structured training data,occupancy grids, 3D bounding boxes, and trajectories,at each deployment site without human annotation, enabling the world model to be trained in a fully selfsupervised manner: the ground truth for future prediction is simply the perception layer’s output at future time steps. HERMES’s [51] approach of unifying understanding and generation through BEV representations provides a complementary paradigm for multi-task roadside scene reasoning. 

**4D Occupancy Forecasting.** Building on OccWorld’s [50] autoregressive prediction paradigm, we develop algorithms to predict the volumetric occupancy of intersections in temporal sequences. The roadside viewpoint offers a key advantage: a more complete and less occluded occupancy field compared to ego-vehicle perspectives. 

**Multi-Modal Generative Synthesis.** We employ Diffusion Models to jointly synthesize LiDAR point clouds and camera imagery from the roadside perspective, utilize Neural Radiance Fields for digital twin creation, and synthesize rare edge-case scenarios for generative data augmentation. 

**Quality-Aware Synthetic Data (Unique Contribution).** Unlike existing world models that generate data without uncertainty information, our quality-aware framework propagates sensor-level reliability through the generation pipeline. We extend DynamicCity’s HexPlane representation with 

11 

additional uncertainty channels, encoding per-voxel reliability alongside semantic and geometric features. 

### **5.2 Phase II: Physics-Informed Predictive Dynamics (Years 2–3)** 

_Goal: Teaching the model “common sense,” causality, and controllability._ 

#### **Latent Space Dynamics with Physical Constraints.** 


We learn the transition function _T_ that governs how a traffic scene evolves in a compressed latent space, with traffic flow theory and vehicle dynamics embedded as physics-informed loss functions _L_ physics. Inspired by ResWorld’s [45] temporal residual approach, we develop a roadside-specific variant that leverages FRGB3D’s static scene priors as an explicit background model. 

**Multi-Agent Counterfactual Reasoning.** While Waymo’s counterfactual reasoning modifies the ego-vehicle’s actions, our infrastructure viewpoint enables _multi-agent_ counterfactual analysis. The temporal-depth advantage uniquely enables a form of counterfactual reasoning unavailable to vehicle-centric models: because the roadside sensor has observed thousands of similar scenarios, the world model can compare any specific event against the site’s empirical behavioral distribution,providing a data-driven counterfactual baseline. 

**Language-Conditioned Scene Editing.** We enable engineers and traffic planners to describe scenario modifications in natural language, generating corresponding multi-modal simulations. Beyond Waymo’s control axes, we introduce infrastructure-specific axes: signal phase control, traffic volume scaling, and weather/lighting modulation. 

### **5.3 Phase III: Collaborative World Models for V2X (Years 3–5)** 

_Goal: Achieving “cognitive alignment” between infrastructure and vehicles, merging temporal depth with spatial breadth._ 

**World Model Alignment Across Domains.** A critical research question is how to _align_ infrastructure and vehicle world models in a shared latent space: 


where _qI_ and _qV_ are the latent encoders of the infrastructure and vehicle world models, respectively. 

**Complementary World Views: Temporal Depth Meets Spatial Breadth.** The roadside world model provides _temporal priors_ : learned behavioral distributions at the current location that encode cumulative knowledge from months of observation. Connected vehicles contribute _spatial context_ : knowledge of road network conditions beyond the infrastructure sensor’s field of view. V2I latent sharing compresses complex world states into bandwidth-efficient representations for real-time communication. 

**Multi-Agent Game Theory.** We model competitive and cooperative behaviors of human drivers and AVs, leveraging the infrastructure’s complete observability to serve as an impartial referee and information broker. 

12 

Table 5: Mapping Current Research to I-WM Components. 

|**Existing Work**|**I-WM Role**|**Description**|
|---|---|---|
|FRGB3D|Static Scene Prior /|Provides the static world “canvas” and|
|(Background<br>Modeling)|Temporal Normality<br>Baseline|enables temporal-depth-based<br>counterfactual reasoning.|
|MulDet3D|Object Initialization|Supplies detected objects as initial|
|(Multi-LiDAR<br>Detection)||conditions for world model rollouts.|
|MulTrack3D /<br>ClusterTrack3D|Dynamic Agent<br>Modeling|Provides trajectory histories as training<br>data for agent behavior prediction.|
|Multi-LiDAR<br>Registration|Spatial Anchor|Ground-aligned registration ensures a<br>consistent global frame.|
|Quality-Aware<br>Pipeline|Uncertainty Propagation|Propagates sensor-level reliability<br>through the entire<br>perception-to-prediction chain.|


## **6 Leveraging Current Research Strengths** 

This research vision builds directly upon our existing technical foundations, which constitute the _perception layer_ (Layer 1) of the dual-layer I-WM architecture. Table 5 maps each component to its role as a data engine for the generative world model layer. 

## **7 Broader Impact** 

A key differentiator of infrastructure-centric world models is their applicability _beyond_ autonomous vehicle testing. Unlike Waymo’s vehicle-centric model, which primarily serves AV development, I- WM enables: (1) _proactive safety analysis_ ,generating counterfactual near-miss scenarios to compute Surrogate Safety Measures at scale; (2) _adaptive signal control optimization_ ,using the world model as a “mental simulator” for model-predictive control; (3) _urban planning and design_ ,simulating infrastructure changes before physical construction; (4) _training data generation for agencies_ ,providing synthetic datasets for detection system calibration; and (5) _extreme event preparedness_ ,simulating infrastructure responses to rare events for emergency planning. 

## **8 Conclusion** 

The emergence of vehicle-centric world models, alongside open platforms such as NVIDIA Cosmos, LeCun’s JEPA-based latent predictive architectures, and Li Fei-Fei’s spatial intelligence vision, demonstrates that world modeling is becoming a cornerstone of next-generation AI. However, the infrastructure perspective remains an untapped frontier. 

Central to our approach is the recognition that roadside and vehicle-based sensing are **epistemologically complementary** : roadside systems offer _temporal depth_ ,dense, long-term behavioral observations at fixed locations,while vehicle systems offer _spatial breadth_ ,diverse sampling across large road networks. By designing the I-WM architecture to explicitly exploit this complementarity, we enable environmental understanding that neither platform can achieve alone. 

13 

Our approach,grounded in Paradigm B foundations (DynamicCity, OccWorld, HERMES), enriched with Paradigm C elements (CarDreamer, ResWorld), informed by JEPA’s latent prediction philosophy and spatial intelligence principles, and trained on a three-tier data strategy,provides a concrete and actionable path forward. The dual-layer architecture we propose,modular, annotationfree perception as a data engine feeding end-to-end generative world models,balances the practical realities of roadside deployment (where labeled data is scarce and each site is unique) with the representational power of modern generative AI (where self-supervised learning over structured observations can capture complex traffic dynamics). 

Looking further ahead, two long-term visions emerge. First, as data and compute scale, the duallayer architecture may converge into a **fully end-to-end roadside foundation model** that jointly learns perception and world modeling from raw sensor streams,analogous to how vehicle-centric systems have evolved from modular pipelines to end-to-end architectures. Second, the natural extension of I-WM toward an **Infrastructure Vision-Language-Action (I-VLA)** framework,where roadside perception, natural language commands, and traffic control actions are unified,represents a novel research direction that could fundamentally reshape how intelligent infrastructure interacts with the transportation ecosystem. The integration of I-WM with existing vehicle-centric models through latent space alignment will unlock capabilities that neither perspective can achieve alone,moving toward a future where infrastructure does not merely observe traffic, but _understands and anticipates_ it. 

## **References** 

- [1] Mahmoud Assran, Quentin Duval, Ishan Misra, Piotr Bojanowski, Pascal Vincent, Michael Rabbat, Yann LeCun, and Nicolas Ballas. Self-supervised learning from images with a jointembedding predictive architecture. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2023. 

- [2] Mahmoud Assran, Adrien Bardes, David Fan, Quentin Garrido, Russell Howes, Mojtaba Komeili, Matthew Muckley, Ammar Rizvi, Claire Roberts, Koustuv Sinha, Artem Zholus, et al. V-JEPA 2: Self-supervised video models enable understanding, prediction, and planning. _Meta AI Research_ , 2025. V-JEPA 2.1 released March 2026. 

- [3] Randall Balestriero and Yann LeCun. LeJEPA: Provable and scalable self-supervised learning without the heuristics. _arXiv preprint arXiv:2511.08544_ , 2025. 

- [4] Hengwei Bian, Lingdong Kong, Haozhe Xie, Liang Pan, Yu Qiao, and Ziwei Liu. DynamicCity: Large-scale 4D occupancy generation from dynamic scenes. In _International Conference on Learning Representations (ICLR)_ , 2025. Spotlight paper. 

- [5] Xuan Di, Rongye Shi, Zhaobin Mo, and Yongjie Fu. Physics-informed deep learning for traffic state estimation: A survey and the outlook. _Algorithms_ , 16(6):305, 2023. 

- [6] Jingtao Ding, Yunke Zhang, Yu Shang, Yuheng Zhang, Zefang Zong, Jie Feng, Yuan Yuan, Hongyuan Su, Nian Li, Nicholas Sukiennik, et al. Understanding world or predicting future? A comprehensive survey of world models. _ACM Computing Surveys_ , 58(3):1–38, 2025. 

- [7] Lili Fan, Jianming Wang, Yuxue Chang, Yang Li, Yue Wang, and Dong Cao. 4D mmwave radar for autonomous driving perception: A comprehensive survey. _IEEE Transactions on Intelligent Vehicles_ , 9:4606–4620, 2024. 

14 

- [8] Tuo Feng, Wenguan Wang, and Yi Yang. A survey of world models for autonomous driving. _ACM Computing Surveys_ , 2025. arXiv:2501.11260. 

- [9] Dechen Gao, Shuangyu Cai, Hanchu Zhou, Hang Wang, Iman Soltani, and Junshan Zhang. CarDreamer: Open-source learning platform for world model based autonomous driving. _IEEE Internet of Things Journal_ , 12:2866–2875, 2024. arXiv:2405.09111. 

- [10] Shenyuan Gao, Jiazhi Yang, Li Chen, Kashyap Chitta, Yihang Qiu, Andreas Geiger, Jun Zhang, and Hongyang Li. Vista: A generalizable driving world model with high fidelity and versatile controllability. In _Advances in Neural Information Processing Systems_ , volume 37, pages 91560–91596, 2024. 

- [11] Yanchen Guan, Haicheng Liao, Zhenning Li, Jia Hu, Chengzhong Xu, Yunjian Zhang, Guofa Li, and Changjun Jiang. World models for autonomous driving: An initial survey. _IEEE Transactions on Intelligent Vehicles_ , 2024. arXiv:2403.02622. 

- [12] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _Nature_ , 2025. 

- [13] Ruiyang Hao, Haibao Yu, Jiaru Zhong, Chuanye Wang, Jiahao Wang, Yiming Kan, Wenxian Yang, Siqi Fan, Huilin Yin, Jianing Qiu, et al. Research challenges and progress in the endto-end V2X cooperative autonomous driving competition. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV) Workshops_ , pages 1828–1839, 2025. 

- [14] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. GAIA-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 

- [15] Qianjiang Hu, Zhimin Zhang, and Wei Hu. RangeLDM: Fast realistic LiDAR point cloud generation. In _European Conference on Computer Vision (ECCV)_ , 2024. 

- [16] Hao Huang et al. V2X-R: Cooperative LiDAR-4D radar fusion for 3D object detection with denoising diffusion. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2025. 

- [17] Tao Huang, Jiaxing Chen, Shan Zhang, Jianming Hu, Yi Zhang, and Shengbo Eben Li. Vehicleto-everything cooperative perception for autonomous driving. _IEEE Transactions on Intelligent Transportation Systems_ , 2025. arXiv:2310.03525. 

- [18] Jiahao Ji, Jingyuan Wang, Zhe Jiang, Jiawei Jiang, and Hu Zhang. STDEN: Towards physicsguided neural networks for traffic flow prediction. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 36, pages 4048–4056, 2022. 

- [19] Yann LeCun. A path towards autonomous machine intelligence. _OpenReview preprint_ , 2022. 

- [20] Boyi Li et al. End-to-end autonomous driving through V2X cooperation. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , 2024. 

- [21] Fei-Fei Li. From words to worlds: Spatial intelligence is AI’s next frontier. Substack, November 2025. URL `https://drfeifei.substack.com/p/ from-words-to-worlds-spatial-intelligence` . 

15 

- [22] Yingyan Li, Shuyao Shang, Weisong Liu, Bing Zhan, Haochen Wang, Yuqi Wang, Yuntao Chen, Xiaoman Wang, Yasong An, Chufeng Tang, et al. DriveVLA-W0: World models amplify data scaling law in autonomous driving. In _International Conference on Learning Representations (ICLR)_ , 2026. arXiv:2510.12796. 

- [23] Lucas Maes, Quentin Le Lidec, Damien Scieur, Yann LeCun, and Randall Balestriero. LeWorldModel: Stable end-to-end joint-embedding predictive architecture from pixels. _arXiv preprint_ , 2026. 

- [24] Chen Min, Dawei Zhao, Liang Xiao, Jian Zhao, Xinli Xu, Zheng Zhu, Lei Jin, Jianshu Li, Yulan Guo, Junliang Xing, et al. DriveWorld: 4D pre-trained scene understanding via world models for autonomous driving. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 15522–15533, 2024. 

- [25] Mohammad Noaeen et al. Traffic signal control via reinforcement learning: A review on applications and innovations. _Infrastructures_ , 10(5):114, 2025. 

- [26] NVIDIA. Cosmos world foundation model platform for physical AI. _arXiv preprint arXiv:2501.03575_ , 2025. 

- [27] Maziar Raissi, Paris Perdikaris, and George Em Karniadakis. Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations. _Journal of Computational Physics_ , 378:686–707, 2019. 

- [28] Haoxi Ran, Vitor Guizilini, and Yue Wang. Towards realistic scene generation with LiDAR diffusion models. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 

- [29] Robbyant Team, Ant Group. Advancing open-source world models: LingBot-World. _arXiv preprint arXiv:2601.20540_ , 2025. 

- [30] Yu Shang, Yuming Lin, Yu Zheng, Hangyu Fan, Jingtao Ding, Jie Feng, Jiansheng Chen, Li Tian, and Yong Li. UrbanWorld: An urban world model for 3D city generation. _arXiv preprint arXiv:2407.11965_ , 2024. 

- [31] Jiahao Shen. Hierarchical reinforcement learning-based traffic signal control. _Scientific Reports_ , 15:32862, 2025. 

- [32] Tencent Hunyuan3D Team. HunyuanWorld 1.0: Generating immersive, explorable, and interactive 3D worlds from words or pixels. _arXiv preprint_ , 2025. 

- [33] Sifan Tu, Xin Zhou, Dingkang Liang, Xingyu Jiang, Yumeng Zhang, Xiaofan Li, and Xiang Bai. The role of world models in shaping autonomous driving: A comprehensive survey. _arXiv preprint arXiv:2502.10498_ , 2025. 

- [34] Chuanye Wang et al. V2XScenes: A multiple challenging traffic conditions dataset for largerange vehicle-infrastructure cooperative perception. In _IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2025. 

- [35] Haoran Wang et al. Research on world models for connected automated driving: Advances, challenges, and outlook. _Applied Sciences_ , 15(16):8986, 2025. 

16 

- [36] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Jiagang Zhu, and Jiwen Lu. DriveDreamer: Towards real-world-driven world models for autonomous driving. In _European Conference on Computer Vision (ECCV)_ , 2024. 

- [37] Yuqi Wang, Jiawei He, Lue Fan, Hongxin Li, Yuntao Chen, and Zhaoxiang Zhang. Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 

- [38] Waymo Team. The Waymo world model: A new frontier for autonomous driving simulation. Waymo Blog, February 2026. URL `https://waymo.com/blog/2026/02/ the-waymo-world-model-a-new-frontier-for-autonomous-driving-simulation` . 

- [39] World Labs. Marble: A multimodal world model for spatial intelligence. World Labs, 2025. URL `https://www.worldlabs.ai/blog` . 

- [40] Hao Xiang, Zhaoliang Zheng, Xin Xia, Runsheng Xu, Letian Gao, Zewei Zhou, et al. V2X-Real: A large-scale dataset for vehicle-to-everything cooperative perception. In _European Conference on Computer Vision (ECCV)_ , 2024. 

- [41] Runsheng Xu, Hao Xiang, Zhengzhong Tu, Xin Xia, Ming-Hsuan Yang, and Jiaqi Ma. V2XViT: Vehicle-to-everything cooperative perception with vision transformer. In _European Conference on Computer Vision (ECCV)_ , 2022. 

- [42] Yu Yang, Jianbiao Mei, Yukai Ma, Siliang Du, Wenqing Chen, Yijie Qian, Yuxiang Feng, and Yong Liu. Driving in the occupancy world: Vision-centric 4D occupancy forecasting and planning via world models for autonomous driving. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, pages 9327–9335, 2025. 

- [43] Haibao Yu, Yizhen Luo, Mao Shu, Yiyi Huo, Zebang Yang, Yifeng Shi, Zhenglong Guo, Hanyu Li, Xing Hu, Jirui Yuan, et al. DAIR-V2X: A large-scale dataset for vehicle-infrastructure cooperative 3D object detection. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 21361–21370, 2022. 

- [44] Haibao Yu, Wenxian Yang, Hongzhi Ruan, Zhenwei Yang, Yingjuan Tang, Xu Gao, Xin Hao, Yifeng Shi, Yifeng Pan, Ning Sun, et al. V2X-Seq: A large-scale sequential dataset for vehicleinfrastructure cooperative perception and forecasting. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 5486–5495, 2023. 

- [45] Jinqing Zhang, Zehua Fu, Zelin Xu, Wenying Dai, Qingjie Liu, and Yunhong Wang. ResWorld: Temporal residual world model for end-to-end autonomous driving. In _International Conference on Learning Representations (ICLR)_ , 2026. arXiv:2602.10884. 

- [46] Junge Zhang, Feihu Zhang, Shaochen Kuang, and Li Zhang. NeRF-LiDAR: Generating realistic LiDAR point clouds with neural radiance fields. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 38, pages 7178–7186, 2024. 

- [47] Junyi Zhang, Shuai Mao, Lufeng Yang, Wei Ma, Shukai Li, and Ziyou Gao. Physics-informed deep learning for traffic state estimation based on the traffic flow model and computational graph method. _Information Fusion_ , 101:101971, 2024. 

17 

- [48] Lunjun Zhang, Yuwen Xiong, Ze Yang, Sergio Casas, Rui Hu, and Raquel Urtasun. Copilot4D: Learning unsupervised world models for autonomous driving via discrete diffusion. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- [49] Shuyang Zhang et al. Epona: Autoregressive diffusion world model for autonomous driving. In _IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2025. 

- [50] Wenzhao Zheng, Weiliang Chen, Yuanhui Huang, Borui Zhang, Yueqi Duan, and Jiwen Lu. OccWorld: Learning a 3D occupancy world model for autonomous driving. In _European Conference on Computer Vision (ECCV)_ , pages 55–72, 2024. 

- [51] Xin Zhou, Dingkang Liang, Sifan Tu, Xiwu Chen, Yikang Ding, Dingyuan Zhang, Feiyang Tan, Hengshuang Zhao, and Xiang Bai. HERMES: A unified self-driving world model for simultaneous 3D scene understanding and generation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 27817–27827, 2025. 

- [52] Walter Zimmer, Christian Creß, Huu Tung Nguyen, and Alois C. Knoll. TUMTraf intersection dataset: All you need for urban 3D camera-LiDAR roadside perception. In _IEEE International Conference on Intelligent Transportation Systems (ITSC)_ , 2023. IEEE Best Student Paper Award. 

- [53] Walter Zimmer, Gerhard Arya Wardana, Suren Sritharan, Xingcheng Zhou, Rui Song, and Alois C. Knoll. TUMTraf V2X cooperative perception dataset. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 

- [54] Vlas Zyrianov, Henry Che, Zhijian Liu, and Shenlong Wang. LidarDM: Generative LiDAR simulation in a generated world. _arXiv preprint arXiv:2404.02903_ , 2024. 

18 

