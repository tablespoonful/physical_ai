---
title: "A Survey of World Models for Autonomous Driving"
date: "2025-01-20"
authors: "Tuo Feng; Wenguan Wang; Yi Yang"
url: https://arxiv.org/abs/2501.11260
pdf: https://arxiv.org/pdf/2501.11260
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2501.11260)** / [論文ページ](https://arxiv.org/abs/2501.11260)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **A Survey of World Models for Autonomous Driving** 

TUO FENG, WENGUAN WANG<sup>∗</sup> , and YI YANG, Collaborative Innovation Center of Artificial Intelligence (CCAI), Zhejiang University, China 

Recent breakthroughs in autonomous driving have been propelled by advances in robust world modeling, fundamentally transforming how vehicles interpret dynamic scenes and execute safe decision-making. World models have emerged as a linchpin technology, offering high-fidelity representations of the driving environment that integrate multi-sensor data, semantic cues, and temporal dynamics. This paper systematically reviews recent advances in world models for autonomous driving, proposing a three-tiered taxonomy: (i) Generation of Future Physical World, covering Image-, BEV-, OG-, and PC-based generation methods that enhance scene evolution modeling through diffusion models and 4D occupancy forecasting; (ii) Behavior Planning for Intelligent Agents, combining rule-driven and learning-based paradigms with cost map optimization and reinforcement learning for trajectory generation in complex traffic conditions; (ii) Interaction between Prediction and Planning, achieving multi-agent collaborative decision-making through latent space diffusion and memory-augmented architectures. The study further analyzes training paradigms, including self-supervised learning, multimodal pretraining, and generative data augmentation, while evaluating world models’ performance in scene understanding and motion prediction tasks. Future research must address key challenges in self-supervised representation learning, multimodal fusion, and advanced simulation to advance the practical deployment of world models in complex urban environments. Overall, the comprehensive analysis provides a technical roadmap for harnessing the transformative potential of world models in advancing safe and reliable autonomous driving solutions. 

CCS Concepts: • **General and reference** → **Surveys and overviews** ; • **Computing methodologies** → **Computer vision** ; • **Networks** → **Network design and planning algorithms** . 

Additional Key Words and Phrases: Autonomous Driving, World Models, Self-Supervised Learning, Behavior Planning, Generative Approaches 

### **ACM Reference Format:** 

Tuo Feng, Wenguan Wang, and Yi Yang. 2025. A Survey of World Models for Autonomous Driving. 1, 1 (September 2025), 34 pages. https://doi.org/10.1145/nnnnnnn.nnnnnnn 

## **1 Introduction** 

The quest for autonomous driving has become a focal point in both scientific research and industry endeavors. At its core lies the ambition to reduce traffic accidents, alleviate congestion, and enhance mobility for societal groups [42]. Current statistics underscore that human error remains the principal cause of accidents [157], indicating that reducing reliance on direct human control could lower the incidence of traffic-related fatalities and injuries. Beyond safety, economic factors also propel the development of autonomous driving technologies [133]. 

∗Corresponding author 

Authors’ Contact Information: Tuo Feng, fengtuo2015@outlook.com; Wenguan Wang, wenguanwang.ai@gmail.com; Yi Yang, yangyics@zju.edu.cn, Collaborative Innovation Center of Artificial Intelligence (CCAI), Zhejiang University, Hangzhou, Zhejiang, China. 

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org. © 2025 Copyright held by the owner/author(s). Publication rights licensed to ACM. Manuscript submitted to ACM 

Manuscript submitted to ACM 

1 

T. Feng et al. 

2 


Fig. 1. **Structure of the overall review** (§1). The top row outlines the organization. The second and third rows illustrate the background and key components. The fourth row highlights various methodologies for training models in autonomous driving. The bottom row showcases four application areas for world models in autonomous driving. 

Despite these incentives, achieving high-level autonomy faces major hurdles. Foremost among these is perceiving and understanding dynamic traffic scenarios, which requires fusing heterogeneous sensor streams into an environmental representation [50, 59]. Autonomous vehicles must rapidly assimilate multi-modal data, detect salient objects, and anticipate their motion under adversarial conditions – such as sensor degradation in heavy rain, unpaved roads with poor markings, or aggressive traffic maneuvers [144, 175]. Moreover, real-time decision-making introduces computational constraints, imposing millisecond-level responsiveness to address unexpected obstacles or anomalous behaviors [119]. Equally pivotal is the system’s resilience in extreme or long-tail scenarios ( _e.g_ ., severe weather, construction zones, or erratic driving behaviors), where performance shortfalls can compromise overall safety [9, 195]. 

Within this context, constructing robust _world models_ has emerged as a cornerstone. In essence, a world model is a generative spatio-temporal neural system that compresses multi-sensor physical observations into a compact latent state and rolls it forward under hypothetical actions, letting the vehicle rehearse futures before they occur [36, 68]. This high-fidelity internal map [133] updates online, and feeds downstream tasks such as physical-world prediction [166]. Recent work refines such models with generative sensor fusion [8, 73, 77, 124, 192], unifying heterogeneous inputs into consistent top-down views [193, 221]. 

These robust world models leverage environmental representations to optimize behavior planning, serving as a keystone for safer, efficient autonomous driving. By enabling trajectory optimization, real-time hazard detection, and adaptive route planning, they reduce predictable risks [50] and are compatible with vehicle-to-everything systems [119]. World models facilitate cohesive integration between perception and control subsystems, streamlining the closed-loop autonomy pipeline [149, 242]. 

Manuscript submitted to ACM 

WMAD 

3 

**Differences between Our Survey and Others.** Existing surveys on world models for autonomous driving can be classified into two categories. The mainstream category covers general world models used across many fields [36, 250], with autonomous driving only one area. The second category [47, 62], though relatively scarce, focuses on the application of world models within autonomous driving. They categorize studies coarsely and often focus solely on world simulation or lack discussions on the interaction between planning and prediction, resulting in a lack of a clear taxonomy. In this paper, a comprehensive review of world models for autonomous driving is presented, and their applications are explored, thereby highlighting how these models are shaped by and adapt to the automotive sector. 

**Goals of Our Survey.** Guided by the principle that world models are central to the understanding of dynamic scenes, this survey aims to (i) develop a _comprehensive, structured taxonomy_ of world models for autonomous driving highlighting the core architectures, input/output modalities, and conditioning strategies; (ii) classify the most commonly used datasets and evaluation metrics employed in world-model research for autonomous driving; and (iii) identify future research directions to advance the reliability and safety of world models in complex driving environments. 

Current research falls into three key areas: (i) Generation of Future Physical World: Focusing on the physical world evolution of both dynamic objects and static entities [192, 195, 238]; (ii) Behavior Planning for Intelligent Agents: Examining generative and rule-based planning methods that produce safe, efficient paths under uncertain driving conditions [22, 80, 166]; (iii) Interaction between Behavior Planning and Future Prediction: Highlighting how unified frameworks can capture agent interactions and leverage predictive insights for collaborative optimization [219, 219]. Specifically, the following contributions are presented: 

- Analysis of Future Prediction Models: Image-/BEV-/OG-/PC-based generation methods are examined to show how geometric and semantic fidelity is achieved, including 4D occupancy forecasting and diffusion-based generation. 

- Investigation of Behavior Planning: Behavior planning is explored through both rule-based and learning-based approaches, and notable improvements in robustness and collision avoidance are demonstrated. 

- Proposition of Interactive Model Research: Interactive models that jointly address future prediction and agent behavior are systematically reviewed, indicating how this synergy can vastly enhance real-world adaptability and operational safety. 

Four frontier challenges are highlighted – developing _self-supervised_ world models, constructing _unified multi-modal_ embeddings, building _advanced, physics-aware_ simulators, and designing _lean, latency-aware_ architectures – to chart a clear roadmap for next-generation autonomous driving research. As the research landscape expands and real-world adoption grows more urgent, this survey is intended to serve as a valuable reference for researchers and practitioners, laying the groundwork for safer, more robust autonomous-driving solutions. 

A summary of this paper’s structure is given in Fig. 1: §1 motivates world models for autonomous driving; §2 formalises the core tasks of world models; §3 introduces a taxonomy of existing methods; §4 contrasts prevailing data and training paradigms; §5 outlines key application areas; §6 benchmarks state-of-the-art models; §7 identifies open challenges and research opportunities; and §8 concludes the survey and summarizes key findings. 

## **2 Background** 

§2.1 first defines world models and their autonomous driving variant that fuses multi-modal inputs for long-horizon planning tasks; next, §2.2 states the formal problem, describing future-world generation and agent planning. 

Manuscript submitted to ACM 

T. Feng et al. 

4 

## **2.1 Definition of World Models** 

A world model is a generative spatio-temporal neural system that encodes the external physical environment into a compact latent state, jointly capturing geometry, semantics and causal context [36]. This internal state is learned without labels: the system first employs a self-learning compressor to squeeze raw sensor frames into a handful of key numbers; next, a time-aware prediction module uses the hidden state and the agent’s action to infer what the next hidden state will be, allowing the agent to rehearse an entire trajectory in its “mind” before acting in the real world [67, 68]. Because every part of the pipeline is differentiable [68], the whole model functions as an interpretable virtual sandbox that supplies gradients, data samples, and “what-if” roll-outs, enabling the agent to make decisions more efficiently [36]. 

World Models for Autonomous Driving apply the same idea to road domains by mapping synchronized camera images, LiDAR sweeps, radar echoes and HD-maps into a single latent scene graph, thereby unifying perception and prediction within one representation [62]. Inside this latent space the model rolls forward the joint dynamics of surrounding traffic and the ego vehicle over long horizons [36], enabling realistic scene generation, multi-agent behaviour forecasting, trajectory evaluation and low-latency control – all while respecting the physical constraints and multimodal uncertainties endemic to real-world driving. 

## **2.2 Core Tasks in World Models for Autonomous Driving** 

In autonomous driving, a critical aspect is accurately predicting the future states of both the ego vehicle and its surrounding environment. To address the core tasks, world models _𝒘_ in autonomous driving takes sensor inputs (including a set of multi-view images _𝑰_ and a set of LiDAR points _𝑷_ ) collected from previous frames and infers the scene and trajectory for the next frames. Specifically, the ego trajectory at time _𝑇_ + 1, denoted as _𝜏_<sup>_𝑇_+1</sup> , is predicted alongside the surrounding scene _𝒛_<sup>_𝑇_+1</sup> . _𝒘_ models the coupled dynamics of the ego vehicle’s motion and the environment’s evolution. Formally, the function _𝒘_ is given by: 


The first core task is generation of future physical world [2, 76, 221, 235], which involves forecasting the future states of dynamic entities. This task emphasizes capturing potential interactions, stochastic behaviors, and uncertainties within rapidly changing and complex scenes. The second core task is behavior planning for intelligent agents [75, 80, 164, 242], focusing on generating optimal and feasible trajectories for the ego vehicle. It requires accounting for safety constraints, dynamic obstacles, traffic regulations, and real-time adaptability. 

## **3 Taxonomy** 

## **3.1 Generation of Future Physical World** 

Fig. 2 arranges future-scene generators into four tracks – image, Bird’s-Eye View (BEV), occupancy grid (OG) and point cloud (PC) – that jointly raise realism, from photoreal frames through map-level layouts to 4D voxels and LiDAR sweeps, all enabled by controllable diffusion and long-horizon forecasting. 

_3.1.1 Image-based Generation._ Image-based future-prediction methods for autonomous driving use generative models to tackle limited data and dynamic environments. Synthesizing realistic images enlarges training data and strengthens perception and planning. 

Manuscript submitted to ACM 

WMAD 

5 


Fig. 2. **The paradigms of generation methods for future physical world** (§3.1). (a) Image-based generation synthesizes highfidelity 2D images. (b) BEV-based generation forecasts BEV maps using paired image and BEV cues. (c) OG-based generation predicts 4D occupancy grids. (d) PC-based generation outputs future LiDAR sweeps. Boxes indicate processing modules; solid arrows denote data flow. 

**Dreamer Series.** _Dreamer series_ was first proposed for learning world models to address dynamic scene understanding in gaming and robotics [69–71], later expanded to autonomous driving with DriveDreamer [195]. It enables controllable video generation in high-density urban traffic using real-world driving data, though they remain limited to 2D outputs lacking spatial-temporal coherence. Subsequent research introduces DriveDreamer-2 [239], incorporating LLM-based prompting mechanisms to enhance interactivity and diversity. With further advancements, DriveDreamer4D [238] significantly extends model capabilities by utilizing world model priors to generate spatial-temporally coherent 4D driving videos, marking a transition from traditional 2D to advanced 4D video generation. ReconDreamer [155] explores online restoration techniques to achieve precise video reconstruction of dynamic scenes. WorldDreamer [196] expands the applicability of world models by pioneering masked token prediction for multi-modal generation, bridging text-tovideo and action-to-video tasks, and moving towards general-purpose world model construction. The development of the _Dreamer series_ demonstrates a clear trend: progressing from 2D to multi-dimensional video generation, transitioning from task-specific to general-purpose models, and shifting from closed, structured conditions toward more open and general natural-language-based conditions. 

**Diffusion-based Image Generation.** The evolution of this type in autonomous driving are coalescing around two complementary thrusts: _controllable generation_ ( _e.g_ ., BEVControl [217], DrivingDiffusion [124], and GeoDrive [23]), which use latent diffusion to render geometry-consistent videos from rich cues such as BEV layouts, text prompts and optical flow, and _high-fidelity spatio-temporal modelling_ , where Drive-WM [198], Vista [54], and LongDWM [194] push diffusion roll-outs to longer horizons and higher spatial resolutions, markedly boosting temporal coherence and per-frame detail. The field progresses through breakthroughs in _multi-modal conditions_ : integrating ego trajectory, human-pose, and DINO appearance tokens for behaviour-aware video synthesis [73]; translating simulator layouts into photorealistic scenes through a cascade diffusion pipeline [247] or dual-scale controlNet-stable diffusion [121]; uniting LiDAR and camera streams in a BEV latent grid for geometry-consistent cross-sensor forecasting [235]; aligning ego–other vehicle trajectories in latent space to enable fully controllable, multi-agent video generation [249]; and grounding multi-camera driving video generation in physics by aligning ego-world coordinates, injecting 3D flows, and box-guided occlusion reasoning [223]. Recent methods [90, 96, 123, 130, 141, 171, 189, 191] focus on expanding from simple RGB image generation to more _diverse and enriched paradigms_ , including extending conventional RGB prediction to jointly generate both images and depth [130]; shifting from layout-conditioned synthesis to fine-grained trajectory-conditioned control [123]; moving beyond 2D-only conditioning toward multi-view consistent generation [96]; transitioning from 2D layout cues to full 3D scene conditioned synthesis [90]; broadening single-view synthesis into multi-view, multi-agent interactive scenarios [171]; progressing from short-term clips to long-horizon video generation [189]; and further leveraging failure-case augmentation for robustness [141]; alongside the release of accident-anticipation benchmarks for risk-aware evaluation [63]. Moreover, InfiniCube [139] employs world-guided 

Manuscript submitted to ACM 

T. Feng et al. 

6 

Table 1. **Overview** of summary, methods and core architectures for Image-/BEV-based generation (§3.1.1 and §3.1.2). 

|**Summary**|**Method**|**Pub.**|**Core Architecture**|**Input Modality**&**Control Condition**|**Output Modality**|**Training Dataset**|
|---|---|---|---|---|---|---|
|||||_Image-based Generation_|||
||DriveDreamer[195]|ECCV’24|Diffusion Model|Text + Image + HDMap + Box + Actions|2D Image + Actions|nuScenes[17]|
||DriveDreamer-2[239]|AAAI’25|LLM + Diffusion Model|Text + HDMap + Box|2D Image|nuScenes[17]|
|Image-based Generation<br>|DriveDreamer4D[238]|CVPR’24|Diffusion Model + 4DGS|Text + Image + Trajectory|2D Image|Waymo[179]|
|Dreamer Series|ReconDreamer[155]|CVPR’24|Diffusion Model|Image + HDMap + Box|2D Image|Waymo[179]|
||WorldDreamer[196]|arXiv’24|LLM|Image + Video + Text + Action|2D Image|nuScenes[17]|
||CarDreamer[52]|IOTJ’24|World Model Backbone|Image + BEV + LiDAR + Radar|2D Image + Actions|CARLA[39]|
||BEVControl [217]|arXiv’23|Diffusion Model|BEV + Image + Text|2D Image|nuScenes[17]|
||DrivingDiffusion[124]|ECCV’24|Diffusion Model|Image + Layouts + Text + Optical Flow|2D Image|CARLA[39]|
||Drive-WM[198]<br>|CVPR’24|Diffusion Model|Image + Action + Box + Map + Text|2D Image|nuScenes[17] + Waymo[179]<br>|
||DriVerse [123]|ACMMM’25|Diffusion Model|Image + Trajectory|2D Image|nuScenes[17] + Waymo[179]|
||GEM[73]|CVPR’24|Diffusion Model<br>I|mage + Trajectory + Human pose + DINO features|<br>2D Image + Depth|Self-created dataset[73]|
||Vista[54]|NeurIPS’24|Diffusion Model|Image + Action|2D Image|Self-created dataset[54]|
||SimGen [247]<br>|NeurIPS’24<br>|Diffusion Model<br>f|Image + Depth + Segmentation + Text<br>|2D Image|DIVA [247] + nuScenes[17]<br>|
||Delphi[141]|arXiv’24|Diffusion Model|Image + BEV layout + Failure Case|2D Image|nuScenes[17]|
||BevWorld[235]|arXiv’24|Diffusion Model|Image + Point cloud + Action|2D Image + 3D LiDAR|nuScenes[17] + CARLA[40]|
||DrivePhysica [223]|arXiv’24|Diffusion Model|Image + Poses + Box + Lane + Text|2D Image|nuScenes[17]|
||Imagine-2-Drive [56]|arXiv’24|Diffusion Model|Image|2D Image|CARLA[40]|
|Image-based Generation<br>f|MaskGWM[156]|arXiv’25|Diffusion Model|Image + Text + Action|2D Image|OpenDV-2K[216] + nuScenes[17]|
|Diffusion Models|EOTWM [249]|arXiv’25|Diffusion Model|Image + Text + Trajectory|2D Image|nuScenes[17]|
||UniFuture [130]|arXiv’25|Diffusion Model|Image + Depth|2D Image + Depth|nuScenes[17]|
||DiVE [96]|arXiv’25|Diffusion Model|Image + Text + Box + Road condition|2D Image|nuScenes[17]|
||CoGen [90]|arXiv’25|Diffusion Model|Image + Occupancy|2D Image|nuScenes[17]|
||GAIA-2 [171]|arXiv’25|Diffusion Model|Image + Action + Text|2D Image|Internal dataset[171]|
||MiLA [189]<br>|arXiv’25<br>’|Diffusion Model<br>f|Image + Waypoints + Text + Camera parameters<br>|2D Image<br>|nuScenes[17]<br>|
||DiST-4D [65]|ICCV25|Diffusion Model|Image + Trajectory + BEV + Pose + Box|RGBD image|nuScenes[17] + Waymo[179]|
||SimWorld[121]|arXiv’25|Diffusion Model|Mask + Box + Text|2D Image|AutoMine[126]|
||InfiniCube[139]|ICCV’25|Diffusion Model + 3DGS|HD Map + Bounding boxes + Text|2D Image + 3DGS|Waymo[179]|
||STAGE[191]|arXiv’25|Diffusion Model|Image + HD Map + 3D Box|2D Image + Long-horizon video|nuScenes[17]|
||AoTA[63]<br>|Comm. Eng.’25|Diffusion Model|Image + HD Map + Layouts + Ego pose + Text|2D Image|nuScenes[17]|
||GeoDrive [23]|arXiv’25|Diffusion Model|Image + Trajectory|2D Image|nuScenes[17]|
||LongDWM[194]|arXiv’25|Diffusion Model|Image + Action|2D Image + Long-horizon video|nuScenes[17]|
||GAIA-1[77]|arXiv’23|Transformer|Image + Action + Text|2D Image|Internal dataset[77]|
||HoloDrive[207]|arXiv’24|Transformer|Image + LiDAR + Layouts + Text|2D Image + 3D LiDAR|nuScenes[17]|
||BEVGen[181]|RA-L’24|Transformer|Image + BEV layout|2D Image|nuScenes[17] + Argoverse 2[204]|
|Image-based Generation|DrivingWorld[81]|arXiv’24|Video GPT|Image + Orientation + Location|2D Image|NuPlan[18] Internal data[81]|
|Transformers|DriveSim [178]|arXiv’24|MLLMs|Image + Text|2D Image|Internal dataset[178]|
||TMPE [164]|arXiv’24|Tansformer|Image + Path + Speed|2D Image + BEV|CARLA [39]|
||NeMo[88]|ECCV’24|Transformer|Image|2D Image + LiDAR + Occupancy|nuScenes[17]|
||FUTURIS[102]|arXiv’25|Transformer|Segmentation + Depth|Segmentation + Depth|Cityscapes[32]|
|||||_BEV-based Generation_|||
||FIERY [76]|ICCV’21|Transformer|Image + Ego motion|BEV|nuScenes[17]|
||StretchBEV[6]|ECCV’22|LSTM|Image|BEV|nuScenes[17]|
||MILE[75]|NeurIPS’22|RNN|Image + BEV segmentation + Action|Image + BEV + Action|CARLA[40]|
|BEV-based Generation|UNO[2]|CVPR’24|CNN|LiDAR|Occupancy + LiDAR + BEV|nuScenes[17]|
||PowerBEV [116]|IJCAI’23|CNN|Image|BEV Instance|nuScenes[17]|
||GenAD[242]|ECCV’24|Transformer|Image + BEV|Map + Trajectory|nuScenes[17]|
||CarFormer[72]|ECCV’24|Transformer|BEV + Trajectory+ Destination + Traffic sign|BEV + Action|Longest6[28]|


video diffusion grounded on HD maps, 3D bounding boxes, and text, then lifts the generated long-horizon videos into dynamic 3D Gaussian scenes via a fast feed-forward reconstruction pipeline. This technical evolution reveals a clear trend from isolated scene generation to integrated closed-loop simulation systems, providing high-fidelity, scalable synthetic environments for autonomous driving. 

**Transformer-based Image Generation.** Transformer-based driving imagers are evolving from _narrow, single-view renderers_ into _holistic, action-aware world models_ . _Cross-view_ architectures such as HoloDrive [207] and BEVGen [181] fuse camera and LiDAR or lift BEV layouts to street-level frames, unifying 2D appearance with 3D geometry. A _parallel line_ scales sequence modeling: DrivingWorld [81] and GAIA-1 [77] treat video, text and control as one token stream, enabling minute-long, controllable clips with coherent semantics. These token factories prove that unsupervised prediction alone can encode road rules and actor intent. _Complementary work_ probes limits and remedies: DriveSim [178] exposes causal hallucinations in multimodal LLMs, while a DINOv2-based multi-view encoder [164] compresses synchronized front views into a latent scene grid that decodes to both RGB and BEV semantics, reducing covariate shift. **Summary.** Table 1 shows different modern image-centric generative frameworks, which use diffusion and transformer architectures to produce diverse driving data. Several observations can be drawn: 

Manuscript submitted to ACM 

WMAD 

7 

- These methods synthesize photorealistic images to enrich training sets. They also create rare or safety-critical scenarios that are hard to capture in real data. 

- World models forecast future states conditioned on actions. Fusion of multiple modalities enhances planning and dynamic reasoning. 

_3.1.2 BEV-based Generation._ **BEV Representation.** A BEV representation unifies multi-modal sensor streams into a single top-down map, exposing lane layouts, dynamic actors, and free space in a planner-friendly format [235]. By stripping away perspective distortions, BEV methods provide high-level, spatially coherent context that has become a powerful complement – or even alternative – to image-centric pipelines, supporting tasks such as motion prediction and long-horizon trajectory forecasting. This 2D projection, however, gains simplicity at the expense of depth resolution: BEV maps can struggle to retain fine-grained 3D geometry in scenes with complex vertical structure or steep depth gradients [45]. 

Starting with the probabilistic BEV forecaster FIERY [76], researchers stretch temporal range with StretchBEV [6], learn continuous 4D occupancy fields with UnO [2], and cut computation via the 2DCNN design [116]. _Object-centric_ slots then emerge: CarFormer [72] assigns every actor a latent slot. MILE [75] compresses the whole scene into a single compact latent with the driving policy, enabling _policy-aware, multi-modal_ prediction. Together, these advances unlock _generative planning_ ; GenAD [242] rolls the latent forward to sample ego-conditioned futures, BEVControl [217] lets users overwrite it with editable sketches for safety auditing, and ViDAR [221], although operating in point-cloud space, supplies geometry-aware pre-training that lifts BEV performance across the board. Together these works chart a path from early probabilistic forecasts to _efficient, object-aware, user-controllable_ world models. 

**Summary.** Table 1 summarizes recent BEV-based generative methods, which predict future BEV representations for autonomous driving tasks. Several observations can be drawn: 

- Early works transform monocular images into probabilistic BEV maps, whereas newer models incorporate object-centric slots, 4D occupancy fields, and trajectory-conditioned latents to capture richer semantics and multi-agent interactions. 

- Recent approaches move beyond supervised training by adopting self-supervised occupancy learning, lightweight multi-scale designs, and editable BEV sketches, paving the way toward closed-loop, generative world-model simulation. 

_3.1.3 OG-based Generation._ **OG Representation.** An OG representation divides the driving scene into 3D voxels and assigns each cell a probability of being occupied, producing a single lattice that simultaneously tracks static structure and moving actors. This discretisation yields far richer geometric detail than 2D projections such as BEV, enabling finegrained reasoning about scene evolution and actor interactions – qualities that have made OGs a mainstay of future-state prediction in autonomous driving. The price of this fidelity, however, is steep: dense voxel grids demand considerable memory and computational throughput, which can hinder deployment in large-scale or real-time systems [184]. 

OG-based Generation ( _i.e_ ., occupancy forecasting) originates from forecasting semantic occupancy grids on BEV [22, 106, 143, 172, 174, 185]. It is employed to predict how the surrounding occupancy will evolve in the near future. **CNN-based OG Generation.** Occ4cast starts this type by unifying sparse-to-dense completion and 4D forecasting into a coherent Eulerian grid that reconstructs geometry and predicts its future[135]. Cam4DOcc then ports this paradigm from LiDAR to low-cost multi-view cameras, releasing a benchmark and network that align per-view geometry with motion cues[142]. Finally, PreWorld trims supervision demands by introducing a semi-supervised, two-stage pipeline 

Manuscript submitted to ACM 

T. Feng et al. 

8 

Table 2. **Overview** of summary, methods and core architectures for OG-/PC-based generation (§3.1.3 and §3.1.4). 

|**Summary**|**Method**|**Pub.**|**Core Architecture**|**Input Modality**&**Control Condition**|**Output Modality**|**Training Dataset**|
|---|---|---|---|---|---|---|
|||||_OG-based Generation_|||
|OG-based Generation|Occ4cast[135]|IROS’24|CNNs|LiDAR|Occupancy|OCFBench[135]|
|<br>CNNs|Cam4DOcc[142]<br>|CVPR’24<br>|CNN|Image + Ego motion + GMO + GSO|Occupancy|OpenOccupancy[197]<br>|
||PreWorld[120]<br>|ICLR’25<br>|CNN<br>|Image + Occupancy|Occupancy|Occ3D[184]<br>|
||MUVO[10]|IV’23|Transformer|Image + LiDAR + Action|Image + LiDAR + Occupancy|CARLA[39]|
||OccWorld[241]<br>DFIT-OccWorld[229]|ECCV’24<br>arXiv’24|Transformer<br>Transformer|Occupancy + Trajectory<br>Occupancy + Image + Ego poses|Occupancy + Trajectory<br>Occupancy + Image + Trajectory|Occ3D[184]<br>Occ3D[184] + OpenScene[31]|
||DriveWorld[149]|CVPR’24|Transformer|Image + Action|Occupancy + Action|nuScenes[17] + OpenScene[31]|
|OG-based Generation|Drive-OccWorld[220]|AAAI’25|Transformer|Image + Action|Occupancy + Flow + Trajectory|nuScenes[17] + OpenOccupancy[197]|
|<br>Transformers|OccLLaMA[199]<br>GaussianWorld[252]|arXiv’24<br>CVPR’25|Transformer<br>Transformer + 3DGS|Occupancy + Trajectory + Text<br>Gaussians + Image|Occupancy + Trajectory + Text<br>Occupancy|nuScenes[17] + OpenOccupancy[197]<br>nuScenes[17]|
||RenderWorld[213]|ICRA’24|Transformer + 3DGS|Image|Occupancy + Trajectory|nuScenes[17]|
||OccProphet[24]<br>Occ-LLM[210]<br>T<sup>3</sup>Former [209]|ICLR’25<br>ICRA’25<br>arXiv’25|Transformer<br>LLM<br>Transformer|Image<br>Image + Occupancy<br>Occupancy|Occupancy + Flow<br>Occupancy + Trajectory + Text<br>Occupancy + Trajectory|nuScenes[17] + OpenOccupancy[197]<br>nuScenes[17] + Occ3D[184]<br>nuScenes[17]|
||AFMWM[134]|arXiv’25|Transformer|Occupancy + Trajectory|Occupancy + Video|Occ3D[184] + KITTI360[131]|
||I<sup>2</sup>-World[132]|arXiv’25|Transformer|Occupancy|4D occupancy|Occ3D[184]|
||DOME[60]|arXiv’24|Diffusion Model|Occupancy + Action|Occupancy|nuScenes[17]|
|OG-based Generation|OccSora[192]|arXiv’24|Diffusion Model|Occupancy + Trajectory|Occupancy|Occ3D[184]|
|<br>Diffusion Models|UniScene[114]<br>DynamicCity[8]|arXiv’24<br>ICLR’25|Diffusion Model<br>Diffusion Model|BEV Layouts + Text<br>Occupancy + Command + Trajectory + Layout|Occupancy + LiDAR + Image<br>Occupancy|OpenOccupancy[197] + nuScenes[17]<br>Occ3D[184] + CarlaSC[205]|
||COME[177]|arXiv’25|Diffusion Model|Occupancy+ Pose/BEV layout|Occupancy|Occ3D[184]|
|||||_PC-based Generation_|||
|PC-based Generation<br>|PCP[146]|CoRL’22|CNN|LiDAR + Range map|LiDAR|KITTI[57]|
|CNNs|4DOcc[107]|CVPR’23|CNN|LiDAR|Occupancy+ LiDAR|KITTI[57]+ nuScenes[17]|
||PCPNet[140]|RA-L’23|CNN|LiDAR + Range map|LiDAR|KITTI[57]|
|PC-based Generation|ViDAR[221]|CVPR’24|Transformer|Image + Action|LiDAR|nuScenes[17]|
|Transformers|HERMES[246]|ICCV’25|Transformer|Image + Text + Action|LiDAR + Text|nuScenes[17]|
|PC-bd Gti|LiDARGen[253]|ECCV’22|Diffusion Model|LiDAR + Range map|LiDAR|KITTI-360[131]|
|ase eneraon<br>Diffusion Models|Copilot4D[233]|ICLR’24|Diffusion Model|LiDAR|LiDAR|KITTI[57] + nuScenes[17]|
|f|RangeLDM[79]|arXiv’24|Diffusion Model|LiDAR + Range map|LiDAR|KITTI-360[131]|
||LiDARCrafter[129]|arXiv’25|Diffusion Model|Text + Ego-centric scenegraph + LiDAR + Motion|LiDAR|nuScenes[17]|
||Lidarsim[144]|CVPR’20|Composition|LiDAR|LiDAR|Internal dataset[144]|
||lidarGeneration[16]|IROS’19|VAE + GAN|LiDAR + Point map|LiDAR|KITTI[57]|
|PCbd Gti|UltraLiDAR[208]|CVPR’23|VQ-VAE|LiDAR|LiDAR|KITTI-360[131] + nuScenes[17]|
|-ase eneraon<br>Others|SPFNet[201]|CoRL’21|LSTMs|LiDAR + Range map|LiDAR|KITTI[57] + nuScenes[17]|
||S2net[200]|ECCV’22|LSTMs|LiDAR + Range map|LiDAR|KITTI[57] + nuScenes[17]|
||NFL[83]|ICCV’23|Nerf|LiDAR|LiDAR|KITTI[57]|
||Nerf-lidar[230]|AAAI’24|Nerf|LiDAR + Image + Segmentation|LiDAR|nuScenes[17]|


that distills 2D imagery into 3D occupancy and planning priors[120]. These milestones trace a clear trajectory: from dense LiDAR-based geometry, through camera-centric low-cost sensing, to label-efficient world models. **Transformer-based OG Generation.** Many recent leading methods of this type adopt Transformer-based core architectures. These models act as vision-centric world models for autonomous driving and are designed to learn from pre-collected, open-loop benchmarks; hence they sit outside “Interaction between Planning and Prediction”. 

Transformer-based OG research starts with MUVO [10], which fuses camera + LiDAR features in a voxel-level Transformer to predict 3D occupancy, yet its deterministic rollout and label hunger limit scalability. OccWorld [241] converts these voxels into autoregressive scene tokens, while DFIT-OccWorld [229] decouples dynamic-static warping to cut training cost, collectively launching a generative, token-based line of work. Toward perception-control unity, DriveWorld [149] pre-trains a memory-augmented world model for downstream planning, and Drive-OccWorld [220] adds trajectory-conditioned heads so the same tokens directly score driving costs. _Efficiency_ remains a parallel thread – OccProphet [24] refines compute, and T<sup>3</sup> Former [209] sparsifies temporal attention with triplane features, achieving real-time, camera-only deployment. Meanwhile, AFMWM[134] pairs a high-ratio Swin-VAE compressor with efficient latent forecasting. I<sup>2</sup> -World [132] further pursues efficiency by decoupling tokenization into _intra_ - and _inter_ -scene stages within an encoder–decoder with a transformation-matrix control head. OccLLaMA [199] and Occ-LLM [210] broaden the token vocabulary to _language and action_ , enabling instruction-driven occupancy reasoning across the same generative backbone. Collectively, the field has evolved from deterministic voxel Transformers through autoregressive token worlds and efficiency-focused triplane models to _multimodal, instruction-aware, real-time world models_ . Some studies attempt to introduce _3D Gaussian Splatting (3DGS)_ into this field. GaussianWorld [252] treats occupancy as Manuscript submitted to ACM 

WMAD 

9 

a 4D forecasting task in Gaussian space, explicitly factorising ego motion, local dynamics and scene completion; RenderWorld [213] removes all lidar by pairing a self-supervised Img2Occ labeler with an AM-VAE encoder and the same autoregressive backbone, yielding a compact, vision-only pipeline. Overall, these studies trace a path from heavy deterministic voxel fusion to lightweight stochastic tokenised representations, from perception-only forecasting to memory- and planning-conditioned roll-outs, and from single-modality grids to language-grounded multi-sensor inputs; the overall trend converges on _controllable, efficient, multi-modal_ world models. 

**Diffusion-based OG Generation.** Diffusion-based OG generation methods enable fine-grained control by coupling spatio-temporal diffusion transformers with compact 4D tokens. They further advance toward _controllable, token-efficient, multi-modal_ world models by: introducing trajectory-resampling control to steer future occupancy synthesis [60]; compressing scenes into compact 4D tokens for coherent occupancy videos [192]; projecting 4D voxels onto HexPlanes and rolling them out with DiT for large-scale semantic forecasting [8]; diffusing unified BEV semantic grids into joint video + LiDAR streams [114]; and disentangling ego-motion from scene evolution via a scene-centric forecasting branch whose guidance is injected through a tailored ControlNet into the occupancy world model [177]. 

**Summary.** Table 2 assembles recent OG generative frameworks using CNNs, Transformers, and diffusion models for 4D occupancy forecasting. Several observations emerge: 

- The field migrates from heavy, deterministic voxel fusion to lightweight, stochastic tokenisation and further to Gaussian splats, reducing memory cost. 

- Occupancy world models evolve beyond perception-only roll-outs: memory-augmented and trajectory-conditioned heads embed planning cues, and language-grounded tokens enable instruction-driven reasoning. 

- Efficiency and controllability become central themes: dynamic/static warping, sparse triplane attention, and diffusion-based controllable priors. This pushes OG generation toward real-time, scalable simulation. 

_3.1.4 PC-based Generation._ **PC Representation.** A PC representation encodes the world as the raw 3D points returned by LiDAR, preserving fine-grained 3D details for vehicles, pedestrians, and surrounding infrastructure. This fine spatial fidelity makes PCs indispensable for occupancy forecasting, dynamic-scene modelling, and predictive reconstruction in autonomous driving. However, the sparsity and irregular sampling of LiDAR scans – combined with real-time computational constraints – continue to pose significant algorithmic challenges. In response, LiDAR point cloud generation, a subtask of 3D point cloud generation, has gained increasing attention to address these limitations and enhance downstream perception and planning capabilities. 

Similar to OG-based generation, PC-based generation predicts future 3D point clouds from past LiDAR sweeps. **CNN-based PC Generation.** PCP [146] stacks consecutive range images into a 3D spatio-temporal volume and applies 3D CNNs that fuse geometry with motion cues for consistent temporal modelling. 4DOcc [107] discretizes historical scans into 4D occupancy grids and leverages lightweight CNN temporal modules to forecast future occupancy, lowering annotation demands while preserving scene fidelity. 

**Transformer-based PC Generation.** PCPNet [140] enriches range-image sequences by inserting self-attention layers that capture long-range dependencies, producing temporally consistent point clouds with stronger contextual cues. ViDAR [221] frames vision-LiDAR pre-training as an autoregressive task: it embeds images and actions with a Transformer encoder and decodes future point sequences causally, providing geometry-aware priors that benefit downstream BEV generation. Building on this, HERMES [246] fuses multi-view images and textual prompts into BEV embeddings through causal attention, then employs differentiable voxel rendering, constrained by motion and collision losses, to synthesize high-fidelity point clouds that respect scene dynamics. 

Manuscript submitted to ACM 

T. Feng et al. 

10 

**Diffusion-based PC Generation.** LiDARGen [253] formulates LiDAR synthesis as a score-matching diffusion process on equirectangular range images, producing physically plausible and controllable samples. Copilot4D [233] discretizes LiDAR observations with a VQ-VAE and conducts discrete diffusion to autoregressively sample future sweeps, enabling unsupervised world-model learning. RangeLDM [79] denoises latent representations of range-view images to reconstruct accurate point clouds, combining latent diffusion with Hough-voting projections. LiDARCrafter [129] extends LiDAR generation to dynamic 4D world modeling by parsing free-form text into an ego-centric scene graph, conditioning a tri-branch diffusion network for layout synthesis, and enforcing temporal coherence via an autoregressive warping module with ego/agent motion priors. 

**Other PC Generation Methods.** Early GAN-based frameworks [173] support unconditional point-cloud synthesis, while lidarGeneration [16] specifically mimics real-world LiDAR statistics via adversarial training on range-image projections. SPFNet [201] and S2net [200] employ LSTMs on sequential range maps with explicit compensation for sensor calibration. Lidarsim [144] couples physical raycasting with learned noise models to generate near-realistic scenes. UltraLiDAR [208] uses discrete latent tokens to preserve structural and semantic consistency. Neural-field methods ( _i.e_ ., NFL [83] and Nerf-LiDAR [230]) extend NeRF paradigms to LiDAR, enabling novel-view synthesis under dynamic and partially observed conditions. 

**Summary.** Table 2 shows different modern LiDAR generation frameworks. Several observations can be drawn: 

- PC-based Generation leverages diverse architectures ( _e.g_ ., Diffusion Models, GANs, VQ-VAE, and NeRF) to address LiDAR sparsity and irregularity while preserving geometric fidelity. Methods like LiDARGen and UltraLiDAR explicitly model physical sensor constraints, whereas Nerf-LiDAR and NFL integrate neural rendering to enhance novel-view synthesis under dynamic scenarios. 

- Recent advancements prioritize integrating world models and multi-modal inputs. However, most approaches focus on geometric priors of LiDAR data, with limited exploration of semantic-aware generation or perceptual consistency for downstream tasks. 

## **3.2 Behavior Planning for Intelligent Agents** 

Behavior planning translates a rich, ever-changing scene understanding into a safe, comfortable, goal-directed trajectory. Most methods first sample diverse, kinematically feasible motions and then, guided by semantic predictions and tactical cues, select the most likely candidate [22, 78, 227]. This likelihood-based scoring fuses predicted dynamics, traffic rules, and comfort metrics, yielding a path that adapts smoothly to evolving conditions while meeting stringent safety requirements. 

_3.2.1 Learning-based Planning._ Early autonomous-vehicle planners relied on rule-based heuristics, but these brittle hand-crafted pipelines struggle with the combinatorial variety of urban traffic and become hard to maintain as the rule set expands [101, 158]. Learning-based motion planning gained traction once large-scale driving logs and fast GPUs became available [175]. Modern architectures ingest multimodal sensor streams ( _i.e_ ., LiDAR, RADAR, GPS signals [19] and camera frames [12, 170]) to output lane-change choices [89, 187], future state distributions [153], reference paths [113], or direct control commands such as steering and throttle [137, 162, 165]. 

Offline supervision or reinforcement learning allows these networks to keep online inference fast and to adapt to new scenes when supplied with sufficient diverse data. Compared with rule-based planning, data-driven planners handle uncertainty and interaction richness more gracefully, especially when reinforced by graph neural networks, attention mechanisms, or large language models that encode high-level traffic intent [91–93]. However, three open issues Manuscript submitted to ACM 

WMAD 

11 

remain: (i) generalisation: performance still degrades in out-of-distribution weather, geography, or traffic densities; (ii) interpretability: opaque latent policies impede validation and debugging [30, 162, 165]; and (iii) formal safety guarantees: current learning pipelines lack provable bounds required for certification [138]. Addressing these gaps is central to scaling learning-based behavior planning from research prototypes to trustworthy real-world deployment. **RL & MPC Planners.** _Model-free reinforcement-learning (RL)_ planner [166] employs a twin-delayed deep deterministic policy gradient (TD3) that maps high-level planning features to manoeuvre commands, delegating the final continuous trajectory to a downstream generator. AdaptiveDriver [188] performs planning with _adaptive world models_ by learning a closed-loop social world model and embedding it into an MPC planner. In contrast, AdaWM [190] formulates _adaptive world-model RL_ : under distribution shift it diagnoses world-model/policy mismatch via a divergence measure and triggers alignment-driven finetuning while execution is through a learned RL policy. _Uncertainty-aware_ variants [35] inject stochastic ensembles or adaptive low-rank updates, exposing epistemic and aleatoric risk for more robust out-ofdistribution reasoning, though at the price of heavier sampling and fine-tuning overheads. _Agent-centric and analytic_ approaches [154] model each actor separately – using attention-based latent intents or differentiable physics – to capture nuanced social interactions, but they rely on accurate tracks or hand-coded dynamics. _Latent-space_ accelerators [117] plan entirely in a low-dimensional latent, enabling orders-of-magnitude faster roll-outs on modest hardware, yet abstract states can omit critical geometry such as traffic-light phase and undermine fine manoeuvres. _Model-based RL_ learns a predictive world model and optimizes the policy via imagination roll-outs, improving sample efficiency and closed-loop reliability; recent exemplars include Raw2Drive’s dual-stream alignment between a privileged and a raw-sensor world model [224] and PIWM’s DreamerV3-style individual world model [55] that encodes inter-agent intentions via trajectory prediction, enabling imagination-based RL. Moreover, there has been a growing trend of integrating RL with vision language model (VLM) and vision-language-action (VLA) models in autonomous driving. VL-SAFE employs offline, world-model RL guided by a VLM: it labels logs with VLM safety scores, imagines safety-aware roll-outs, and trains an actor-critic policy [167]. IRL-VLA constructs a reward world model via inverse RL to replace costly simulator-based rewards, and subsequently uses the RWM to guide PPO-based RL training of a VLA policy [95]. 

**LLM-based Planners.** _Autoregressive multimodal transformers_ [7, 26] treat driving as next-token prediction over interleaved image-and-action tokens, coupling perception, world modelling and control, and achieving competitive nuPlan results, but they demand high-end multi-GPU compute and still struggle with long-horizon consistency and safety certification. WoTE adds a lightweight bird’s-eye-view predictor that scores sampled trajectories online, boosting safety with minimal latency, yet its fidelity is capped by BEV grid resolution and the quality of the trajectory sampler [127]. SSR compresses dense BEV features into just 16 navigation-guided tokens, cutting FLOPs while maintaining accuracy, though aggressive sparsification risks missing rare but critical actors or occlusions [115]. DriveSim explores _GPT-4V-style_ models as internal simulators for language-conditioned planning, showing promising affordance reasoning but revealing frame-order errors and inconsistent imagined trajectories that limit closed-loop reliability [178]. FSDrive [225] reframes intermediate reasoning from text CoT to a spatio-temporal visual CoT: a VLM first acts as a world model to imagine a unified future frame overlaying future lanes and 3D boxes (spatial) together with an ordinary future frame (temporal), and then, conditioned on these visual CoT predictions, outputs the trajectory as an inverse-dynamics step; a unified pretraining scheme activates visual generation while preserving understanding. 

**Volume-based Planners.** Hybrid _cost-volume_ methods first sample or generate a diverse set of candidate trajectories and then rank them with a composite cost that fuses hand-crafted comfort or rule-compliance terms with likelihoods predicted from learned occupancy or segmentation maps. To preserve interpretability, such planners explicitly build a cost map, pair it with a trajectory sampler, and execute the candidate with the lowest overall cost. Concretely, _cost-volume_ 

Manuscript submitted to ACM 

T. Feng et al. 

12 

Table 3. **Overview** of representative learning-based planners (§3.2.1). Please note that methods that use VLM/VLA only to assist RL training or safety scoring are listed under _RL & MPC planners_ ; methods where a (V)LLM acts as the planner at inference appear under _LLM-based planners_ . 

|**Summary**|**Method**|**Pub.**|**Core Architecture**|**Input Modality**&**Control Cond.**|**Output Modality**|**Training Dataset**|
|---|---|---|---|---|---|---|
|||||_RL & MPCplanners_|||
|Model-free RL|PFBD[166]<br>|Electronics’19|TD3policynet|Gap+ Speed + Curvature|Manoeuvre cmd.|Internal[166]|
|Adaptive World Model<br>|AdaptiveDriver[188]<br>AdaWM[190]|arXiv’24<br>ICLR’25|BehaviorNet + MPC<br>Low-rank adaptive WM|Agent histories + HD-map<br>State + reward|Trajectory<br>Trajectory|nuPlan[18]<br>nuPlan[18]|
|Uncertainty-aware|UMBRELLA[35]|RA-L’23|Ensemble + Unc.propag.|Vehicle state history|Trajectory|NGSIM[74]+ CARLA[21]|
|Agent-centric/Analytic|Dream2Drive[154]|arXiv’25|Diff.physics WM|State +goal|Trajectory|WOMD[41]|
|Latent accelerator|Think2Drive[117]|ECCV’24|Latent-spaceplanner|Latent WM|Trajectory|CARLA-V2[21]|
|Model-base RL|Raw2Drive[224]<br>PIWM[55]|arXiv’25<br>TIV’25|Neural planner + Policy RL<br>Actor–critic RL|Multi-view cameras + Ego state<br>Agent histories/relations + Ego|Low-level actions<br>Action + Trajectory|CARLA V2[21] + Bench2Drive[94]<br>I-SIM[234]|
|VLM/VLA|VL-SAFE[167]<br>IRL-VLA[95]|arXiv’25<br>arXiv’25|VLM + WM + offline safe RL<br>IRL + PPO RL + VLApolicy|Image + Text + Offline expert logs<br>Multi-view images/video + Ego state|Low-level actions/Policy<br>Trajectory+ Actions|Internal[167]<br>NAVSIM v2[34]|
|||||_LLM-basedplanners_|||
|Autoreg. Transformer|DrivingGPT[26]<br>VaViM[7]|arXiv’24<br>arXiv’25|MM GPT-style decoder<br>Video-Gen. Transformer|Image + ego state<br>Video + ego|Action tokens<br>Action tokens|nuPlan[18] & NAVSIM[34]<br>OpenDV[216]& nuPlan[18]& nuScenes[17]|
|BEV scorer|WoTE[127]|arXiv’25|BEV head + sampler|BEVgrid + cand. traj.|Score vector|NAVSIM[34]&Bench2Drive[94]|
|Sparse-token WM|SSR[115]|ICLR’25|Sparse token WM|BEV features|Action tokens|nuScenes[17]& CARLA[39]|
|Vision-LLM sim.|DriveSim[178]|arXiv’24|GPT-4Vprobe|Lang. cmd. + frames|Sim. trajectory|Internal[178]|
|Visual CoT|FSDrive[225]|arXiv’25|VLM + visual CoT|Surround cameras + Nav/ego|Trajectory+ future frames|nuScenes[17]|
||||_V_|_olume-basedplanners_|||
||DSDNet[227]|ECCV’20|CNN cost-volume|Image + BEV map|Trajectory set|nuScenes[17] & ATG4D[227] & Precog[169]|
|Volume-based<br>Hybrid Cost Volume|ST-P3[80]<br>MP3[22]<br>NEAT[27]|ECCV’22<br>CVPR’21<br>ICCV’21|Spatio-temp. CNN<br>Unified map–predict–plan<br>Attention fields|Image seq.<br>Multi-modal<br>Image + HD-map|Trajectory set<br>Trajectory set<br>Trajectory set|nuScenes[17] & CARLA[39]<br>nuScenes[17]<br>nuScenes[17]|
||NMP[226]|CVPR’19|Neural motion planner|LiDAR + HD-map|Trajectory set|Internal[226]|
||PPP[172]|ECCV’20|Semantic BEVplanner|BEV semantics|Trajectoryset|nuScenes[17]|
|Occupancyvolume|Occ-WM[220]|AAAI’25|4D occ. WM +_𝑄_-net|4D occupancy|Trajectory|nuScenes[17]+ Occ3D[184]|
|||||_Others_|||
|Imitation Learning<br>Ego Status|MILE[75]<br>BEV-Planner[128]|NIPS’22<br>CVPR’24|Latent dynamics + Policy<br>Ego-query cross-attn + MLP|Image + ego actions<br> <br>Images + Ego status|Action + BEV Segmentation<br>Trajectory|<br>CARLA expert logs[39]<br>nuScenes[17]|
|Uncertainty-aware|UncAD[218]|arXiv’25<br>|MUE(Laplace BEV)+ UGPnP + U|CAS<br>Multi-view images + Ego state|Trajectory|nuScenes[17]|


planners [22, 161, 172, 226] compute a confidence score for each sampled trajectory from the cost volume, guiding the choice toward paths that best balance safety, efficiency, and rule compliance. This approach yields interpretable, safety-oriented plans, but its effectiveness diminishes when the sampler cannot cover the dense combinatorial space of urban traffic [22, 27, 80, 172, 226, 227]. By contrast, _occupancy volume_ method replaces heuristic costs with a learnable head applied to 4D occupancy forecasts, providing richer collision cues and enabling end-to-end fine-tuning, albeit at the expense of higher memory footprints and a reliance on dense occupancy supervision [220]. 

**Other Planners.** MILE [75] introduces a model-based imitation learning (IL) framework that leverages 3D geometry as an inductive bias to jointly learn static scenes, surrounding agents, and ego-vehicle states from high-resolution camera data. It acquires a generative world model and driving policy from offline expert logs, and employs action-conditioned rollouts to simulate diverse future scenarios. BEV-Planner [128], a label-free baseline, directly regresses trajectories through cross-attention between ego-vehicle queries and temporal BEV features, with optional integration of ego status. UncAD [218] makes the BEV map itself probabilistic: a Map Uncertainty Estimation (MUE) head predicts BE BEVV map points and their Laplace parameters, then an Uncertainty-Guided Prediction & Planning (UGPnP) stage generates multi-modal trajectories, and an Uncertainty–Collision-Aware Selection (UCAS) ranks them by collision risk and map confidence. 

**Summary.** Table 3 shows compares major learning-based planning paradigms. Several observations can be drawn: 

   - Modern planners fuse LiDAR, RADAR, GPS and vision, sample kinematic motions, and rank them with learned semantic, interaction, and rule cues, yielding adaptable trajectories beyond brittle heuristics. 

- Architectures diverge: RL and MPC planners fuse latent dynamics, uncertainty, safety; LLM transformers cast driving as token prediction; cost-volume planners rank sampled paths via learned occupancy costs. 

- Manuscript submitted to ACM 

WMAD 

13 

- Gaps remain: models falter in novel weather, policies stay opaque, safety proofs are lacking, and heavy compute blocks real-time urban use, urging work on robust, interpretable, certifiable planners. 

_3.2.2 Rule-based Planning._ Rule-based planners endure because they guarantee safety and are easy to audit [58, 245]. They treat motion as a deterministic optimisation over explicit dynamics and hand-crafted costs, yielding transparent behaviour. Four core families dominate: car-following laws ( _e.g_ ., IDM), sampling planners (RRT, state lattice), modelpredictive control, and potential-field navigation. Modern stacks combine these blocks for interpretability and safety, yet modular fusion can lose global optimality and fixed heuristics struggle in dense, fast-changing traffic. **Car-following Models.** Physics-inspired longitudinal models translate the instantaneous gap, speed and closing rate into throttle or brake commands. The Intelligent Driver Model and its calibrated siblings capture free-flow, synchronized and stop-and-go regimes with a single continuous formula [186]. Recent work samples multiple IDM roll-outs and selects the minimum-cost, safety-compliant candidate to improve comfort without losing closed-form guarantees [33]. Because these laws are purely algebraic, production-grade Adaptive Cruise Control (ACC) systems can execute them at tens-tohundreds Hz frequencies. However, their inherently short prediction horizon is a key limitation, so modern planners augment analytic commands with map priors or predictive MPC to anticipate intersections and cut-in maneuvers better. **Sampling-based Planners.** Sampling-based planners probe the vehicle’s configuration space with a sequence of samples, accept only collision-free continuations, and then rank feasible motion sequences with handcrafted costs. They split into two sub-families that trade optimality for speed in different ways. _Random sampling_ methods grow a tree or roadmap toward stochastically chosen states, guaranteeing probabilistic completeness and – when augmented with rewiring – asymptotic optimality. Classic Rapidly-Exploring Random Trees (RRT) [110, 112] realise millisecond-level feasibility checks for single-query problems. Their optimal variants, RRT and RRG, refine paths online by incremental rewiring [99, 100]. Closed-loop extensions embed vehicle dynamics for high-speed manoeuvres, as demonstrated on MIT’s “Talos” car in the DARPA Urban Challenge [15, 111] and in multi-agent settings [163]. _Deterministic sampling_ methods pre-tile the state–time space with kinematically feasible motion primitives, then apply graph search to pick the lowest-cost, collision-free sequence. Spatiotemporal lattices and their conformal highway variant capture curvature and speed limits explicitly [145, 251]. Polynomial libraries (cubic, quintic, B-spline) further reduce run-time by storing analytically smooth segments that satisfy dynamic bounds [29, 122]. Discretised terminal manifolds shrink search depth for time-critical street scenarios [203], and the Stanford “Junior” entry shows how such libraries integrate into a full urban-driving stack [151]. Because the candidate set is finite, deterministic planners sacrifice global optimality for predictable timing, making them popular for production autonomous vehicle stacks. 

**Continuous Optimisation.** Continuous optimisation planners rebuild vehicle paths in continuous space each control cycle, casting curvature and speed as variables in a quadratic or nonlinear program constrained by dynamics and obstacle corridors. Warm-starting with the previous solution yields smooth, near-optimal trajectories without discrete motion libraries. Apollo’s Expectation–Maximisation planner alternates lateral smoothing with longitudinal speed optimisation, whereas Rastelli’s continuous-curvature scheme minimises jerk and curvature variation along Bézier splines. Both show that convex or near-convex formulations can meet real-time demands while overcoming the sub-optimality and roughness of sampling-based schemes, though at the cost of continual optimisation [43, 160]. 

**Artificial Potential-field Navigation.** Attractive and repulsive potentials characterise the goal as an energy well and obstacles as peaks, letting a robot follow the negative gradient in real time [104, 105]. Newton-style updates hasten escape from saddle points [168], and adaptive gain tuning lessens oscillations on public roads [14]. Blending the field with sigmoid curves limits curvature spikes in dense traffic [136], while embedding the gradient in a torque-based 

Manuscript submitted to ACM 

T. Feng et al. 

14 

Table 4. **Overview** of representative rule-based motion-planning algorithms (§3.2.2). 

|**Summary**|**Method**|**Publication**|**Core Architecture**|**Input Modality & Control Condition**|**Output Modality**|
|---|---|---|---|---|---|
||||_Car-following models_|||
|Car-following<br>Models|IDM [186]<br>IDM Roll-out Sampling [33]|Phys. Rev. E’00<br>CoRL’23|Closed-form ordinary-differential law<br>Batched IDM roll-outs + cost ranking|Gap + Speed + Relative speed<br>Gap+ Speed + Relative speed|Longitudinal acceleration<br>Acceleration + Rollout|
||||_Sampling-basedplanners_|||
|Sampling-based<br>Random|RRT [112]<br>RRT-Connect [110]<br>RRT<sup>∗</sup>/RRG[99,100]|Tech. Rep.’98<br>ICRA’00<br>RSS’10/IJRR’11|Tree search with random exploration<br>Bi-directional RRT connection<br>Rewiringoptimal RRT for asymptotic optimality|State + Map + Obstacles<br>State + Map + Obstacles<br>State + Map+ Obstacles|Feasible path<br>Feasible path<br>Near-optimalpath|
|Sampling-based<br>Deterministic|Spatiotemporal Lattice [251]<br>Conformal Lattice [145]<br>Discrete Terminal Manifold[203]|IROS’09<br>ICRA’11<br>IJRR’12|Pre-tiled spatiotemporal lattice search<br>Highway-aligned lattice search<br>Polynomial trajectorylibrary+ Cost ranking|Ego + State + Map<br>Ego + State + Map<br>Ego + State + Map|Trajectory<br>Trajectory<br>Time-critical trajectory|
||||_Continuous optimisation_|||
|Continuous<br>Optimisation|Apollo EM Planner [43]<br>Continuous-Curvature Spline[160]|arXiv’18<br>IV’14<br>|Alternating DP + spline-QP<br>Bézier-spline continuous-curvatureplanning+Jerk-aware cost|Frenet reference line + Feasible tunnel<br>Ego + Map|Smooth trajectory<br>Smooth trajectory|
||||_Artificialpotential-field navigation_|||
|Artificial<br>Potential-Field|Classic APF [104,105]<br>Newton-PF [168]<br>Hybrid Sigmoid-PF [14,136]<br>Torque-PD PF[51]|CISM’78/IJRR’86<br>T-RO’06<br>Sensors’20/IV’17<br>IV’15|Attractive-repulsive potential field<br>Potential-field with Newton-based update<br>Potential field with sigmoid blending<br>Potential field withinproportional–derivative steering|Goal pose + Obstacles<br>Goal pose + Obstacles<br>Goal pose + Obstacles<br>Potential-field value|Steering command<br>Steering command<br>Steering command<br>Steeringtorque|


proportional–derivative steering loop unifies motion planning with low-level control [51]. Although local minima persist, coupling potential-field guidance with higher-level sampling or MPC preserves rapid collision avoidance without forfeiting global optimality [58, 245]. 

**Summary.** Table 4 compares four major rule-based motion-planning paradigms. Several observations follow: 

- Rule-based motion planners span car-following, sampling, continuous optimisation and potential-field families, balancing update rate, smoothness and global optimality while remaining easy to audit. 

- Modern stacks fuse potential-field reflexes, discrete sampling diversity and MPC smoothing, yet modular design can miss global optima and fixed heuristics struggle under dense traffic shifts. 

_3.2.3 Search-based Planning._ Search-based planners discretise the vehicle’s high-dimensional, continuous state-space into a graph whose edges are motion primitives – short, pre-computed, kinematically feasible maneuvers. Classical graph-search techniques such as Dijkstra [11, 61] and the A* family [13, 98] then find the minimum-cost path according to heuristics that balance safety, smoothness, and progress. Vehicle constraints are embedded in the primitive library; Hybrid-State A* extends this idea by blending continuous headings with discrete cells to satisfy non-holonomic bicycle-model dynamics [38]. 

The approach offers strong optimality guarantees and explicit handling of traffic rules and obstacles, but suffers from the resolution-complexity trade-off: finer grids or larger graphs improve path quality and continuity yet raise computational load exponentially, jeopardising real-time performance. Recent work tackles this bottleneck with (i) model-predictive A* that employs relaxed cost-to-go maps for long-horizon searches in milliseconds [4], (ii) adaptive fidelity models that switch between simple longitudinal or drift dynamics to match task urgency [3], (iii) multi-heuristic search that fuses several admissible and inadmissible heuristics to accelerate exploration in cluttered layouts [1], and (iv) Task-and-Motion Planning hybrids that sample primitives from multiple local models while maintaining optimality guarantees in nonlinear, unstable regimes [5]. Together these advances extend search-based planning from structured highway settings to complex urban and off-road scenarios while retaining its interpretable, graph-optimal foundation. 

## **3.3 Interaction between Planning and Prediction** 

Interaction between behaviour planning and future prediction forms a feedback loop: the agent chooses actions while forecasting how all traffic will react. Tight coupling lets it pick manoeuvres that stay both safe and efficient. Research has advanced from passive log replay to fully interactive world models that respond online to ego actions (Fig. 3). Manuscript submitted to ACM 

WMAD 

15 


Fig. 3. **The evolution of interaction** (§3.3). (a) Open-loop regime synthesises scenes from logged data under static conditions; the generator memorises scenarios but never reacts to new actions. (b) Uncontrollable closed-loop regime unifies perception, prediction and planning in an auto-regressive loop, yet latent physics remain fixed, so users cannot inject rules or rare events. (c) Controllable closed-loop regime adds editable 4D worlds, occupancy control and feedback/backward signals, enabling a drive agent to interact safely with a fully testable simulator. 

**Generative Methods and Open-loop Regime.** Recent generative approaches ( _e.g_ ., DriveGAN [108], MagicDrive [53], and DriveDreamer [195]) narrow the sim-to-real gap by focusing on photorealism and synthesizing editable streetscene videos that substantially enrich training corpora; nevertheless, they merely replay pre-sampled futures without responding to online control inputs, thus confining research to a data-centric, open-loop paradigm that breaks the causal link between present actions and subsequent observations. TrafficGen [44] and LCTGen [182] generate traffic scenes from vector logs and natural-language prompts, respectively, while RealGen [37] retrieves and recombines template behaviours to create tag-specific or crash-critical scenarios. All three remain strictly open-loop, replaying fixed futures that ignore online control inputs. NAVSIM [34] shares this non-reactive paradigm, seeking only to refine open-loop metrics; it cannot inject rare events or alter traffic rules, offering merely quasi-closed-loop scores. These limitations draw growing criticism, as open-loop benchmarks can overstate safety and performance when an agent’s actions never influence the futures being evaluated. 

**Auto-regressive World Models and Uncontrollable Closed-loop Regime.** Auto-regressive driving world models [10, 46, 54, 77, 180, 199, 206, 215, 220, 231, 237, 240, 241, 243] have quickly progressed from trajectory-only roll-outs to multi-sensor, long-horizon simulators that generate futures conditioned on ego actions, unifying prediction and planning in a single generative loop. This paradigm supplies cheap, diverse data, exposes planners to their own downstream consequences, and captures uncertainty more richly than fixed-log, open-loop corpora [25, 54, 77]. However, the latent physics are opaque: users cannot freely edit traffic rules, inject rare events, adjust replay speed, or verify safety guarantees, and compounding distribution drift still threatens reliability, leaving current systems in an uncontrollable closed-loop that hampers rigorous safety-critical evaluation [149]. 

Some autoregressive models rely primarily on images [10, 54, 77, 152]. Another line of autoregressive models [199, 241] has integrated 3D occupancy grids into environmental modeling, providing a more detailed and robust representation of spatial dynamics. These grids enable accurate handling of occlusions and spatial relationships in dense urban scenes. However, their use in long-sequence video generation remains limited by the computational complexity of processing and maintaining large-scale 3D data over extended periods. Concurrently, state-space diffusion at the agent/trafficlight level scales to trip-level city simulation[183], complementing image-/occupancy-based rollouts with controllable mid-level semantics. 

**Controllable Closed-loop Regime.** Research has progressed from script-driven traffic engines, through game-engine simulators with sensor realism, to neural and hybrid platforms that merge photoreal rendering with fully editable 

Manuscript submitted to ACM 

T. Feng et al. 

16 

actor control. Early _microscopic engines_ such as SUMO [109] exposed per-vehicle APIs for spawning, deletion and IDM/MOBIL/RL control, enabling fine-grained, reproducible experiments; Waymax [64] later accelerated log replay with JAX for rapid, sensor-free policy iteration, yet neither rendered raw sensor data. To fill this gap, CARLA [40] grafted Unreal-Engine visuals and configurable sensors onto a physics core, while MetaDrive [118] traded photoreal texture for procedural roads and kHz physics to support fast domain randomisation. Both deliver closed-loop images but still cover limited geographies and fall short of real-world visual fidelity, restricting direct transfer to models trained on natural data. _Neural-hybrid_ simulators then appeared. UniSim [222] learns photoreal feature grids from a single drive, and OASim [211] re-poses vehicles with lighting-consistent implicit rendering, yet both remain bounded by their source clips. Dreamland [150] links a physics simulator with a large video generator via a layered world abstraction, mapping simulator states to editable photoreal imagery and boosting controllability and realism for configurable closed-loop world creation. _Fidelity and interactivity_ keeps expanding: Sky-Drive [86] adds socially aware multi-agent interactions; DriveArena [219] converts 2D traffic sketches to photoreal video; DrivingSphere [212] upgrades to 4D occupancy for geometrically accurate stress tests. The _LimSim family_ scales closed-loop control to city networks. LimSim [202] offers distributed, scriptable traffic; LimSim++ [48] adds road-rule scripts and vision hooks; and the latest LIMSIM Series [49] provides modular APIs for covering map topology, human-style bots and area-of-interest acceleration, allowing users to inject hazards, swap policies and tune metrics for rigorous, interactive safety validation. 

Beyond simulator-centric loops, recent works realize controllable closed loops _inside the latent space_ . World4Drive [244] builds an intention-aware latent world model, rolls out intent-conditioned futures and uses a world-model selector to choose the best trajector. LAW [125] learns a plan-conditioned latent world model; future-feature prediction supervises reps and waypoint planning. 

**Summary.** The community has progressed from static, open-loop datasets to fully interactive, high-fidelity simulators. Platforms that fuse controllable closed-loop dynamics with photoreal sensor generation pave the way for the next wave of behaviour-aware, safety-critical autonomous driving research. Several observations can be drawn: 

- Closed-loop scores should complement or replace open-loop metrics to reveal true safety margins. 

- Generative simulators reduce reliance on real-world collection by synthesising corner cases on demand. 

- Tight planning–prediction integration inspires hybrid curricula: models alternate between logged supervision and interactive roll-outs, and share unified losses that couple trajectory forecasting with policy optimisation. 

## **4 Data and Training Paradigms** 

This section focuses on the methodologies for training models in autonomous driving, emphasizing self-supervised learning paradigms, pretraining strategies, and innovative approaches for data generation. 

## **4.1 Self-Supervised Learning for World Models** 

Self-supervised world-model research for autonomous driving uses 2D images [97] or raw LiDAR scans to automatically generate supervision, cutting 3D annotation costs. Rapid progress is now reshaping the field around 3D occupancy grids. Because dense voxel annotation is laborious, many groups pivoted to _cheaper_ 2D supervision. RenderOcc [159], SelfOcc [84], OccNeRF [228], H3O [176], World4Drive [244], and related NeRF-style systems lift multi-view images into volumetric space, back-propagating depth or semantic losses; these image-only routes save annotation cost but lag LiDAR-centric baselines in fidelity and fine geometry. A _complementary branch_ exploits the LiDAR stream itself: UnO [2] and EO [106] derive self-labels by contrasting predicted 4D fields with future scans, while RenderWorld [213], UniPAD [214], and PreWorld [120] couple differentiable rendering with multi-view cameras to fuse 2D texture and 3D Manuscript submitted to ACM 

WMAD 

17 


Fig. 4. (a) **Self-supervised world models** lift multi-view images into 3D volumes, forecast future grids, and learn from 2D renders plus occupancy cues, reducing labels (§4.1). (b) **Large-scale pre-training** on visual point-cloud sequences yields a single backbone that adapts to detection, tracking, mapping, occupancy, and planning (§4.2). 

structure; ViDAR [221] further aligns video patches to point clouds for stronger temporal motion priors. _Tokenisation and diffusion_ bring a third flavour: COPILOT4D [232] and BEVWorld [235] discretise multimodal data into vocabulary codes, then learn discrete diffusion to regenerate future scenes, capturing complex distributions without any human annotation, and AD-L-JEPA [248] eliminates both contrastive and generative heads, directly forecasting bird’s-eye embeddings for faster pre-training. 

These techniques cut labeling costs, unify vision and geometry, and hint at closed-loop plan by letting a policy probe predicted futures. Current self-supervised occupancy models still face three key drawbacks. _Accuracy lags behind fully-supervised 3D/4D baselines_ – NeRF-style pipelines, in particular, lose fine-scale detail. Volumetric rendering and diffusion inference incur _heavy compute and memory costs_ , making long-horizon prediction slow and resource-hungry. Most methods predict only the current voxel grid; _principled, label-free 4D occupancy forecasting_ remains largely unexplored. Looking ahead, key research directions include faster volumetric rendering, and tighter integration with downstream planners to verify that self-supervised grids truly improve safety rather than merely saving labels. 

## **4.2 Large-Scale Pretraining Frameworks** 

A growing body of research argues that large-scale pre-training of world models is becoming the most economical path to robust autonomous driving. _Universal vision/multimodal frameworks_ [54, 87, 120, 148, 149, 214, 221, 235] ingest millions of image-LiDAR sequences, encode them in a unified BEV or voxel space, and learn to forecast future occupancies or videos. Their strengths lie in rich spatio-temporal context, easy transfer to detection, segmentation, trajectory prediction and even planning, and drastic label-cost reduction. Weaknesses include heavy GPU demand, sensitivity to camera calibration, and lingering reliance on heuristic heads ( _e.g_ ., simple occupancy decoders). _LiDAR/occupancy-centric self-supervision_ targets pure 3D geometry. Occupancy-MAE [147] masks voxels, AD-L-JEPA [248] reconstructs masked embeddings, and UnO [2] predicts continuous 4D occupancy fields from future point-cloud pseudo-labels. These methods excel at fine-grained geometry, learn on sparse data, and are sensor-agnostic, but they lack rich semantics and require precise temporal alignment. _Foundation-level generative world models_ ( _e.g_ ., Gaia-1 [77], Gaia-2 [171]) scale to hundreds of millions of frames, synthesize controllable multi-camera scenes, and couple generation with understanding. They promise closed-loop simulation and data augmentation, yet training cost and safety-critical evaluation remain open hurdles. 

Manuscript submitted to ACM 

T. Feng et al. 

18 

Table 5. **Usage of data generation** (§4.3). 

|Method|Usage of datageneration|
|---|---|
||Generation reused for downstream tasks|
|DriveDreamer-2[239]<br>BEVControl[217]<br>SimGen[247]<br>GAIA-2[171]|Generates user-customized videos from text prompts, and the authors discuss adding them to 3D detection training set.<br>BEV sketches are converted to street-view images that fine-tune BEVFormer, boosting NDS by +1.29.<br>Simulator + real-layout images serve as augmentation, improving BEV detection & segmentation on nuScenes.<br>Synthetic multi-camera videos feed Wayve’s offlineperception &planningstack for trainingand safetyvalidation.<br>Generation for self-training|
|GEM[73]<br>Vista[54]<br>GAIA-1[77]|Generates scenes from ego trajectory and DINO cues.<br>High-fidelity video world model evaluated on generation metrics and RL reward.<br>Demonstrates controllable scene synthesis.|
|DrivingWorld[81]|Video-GPT model measured by FID/FVD.|
|MiLA[189]|Targets long-horizon video synthesis for future training.|
|CoGen[90]|Produces controllable multi-view 3D-consistent scenes.|


Research has progressed from early multimodal prediction networks, through _unified 4D pre-training pipelines_ , to the first attempts at foundation generative models; at each stage the emphasis shifts from “perception only” to “perceivepredict-plan” while annotation demand falls. Hybrid systems are anticipated that fuse dense LiDAR self-supervision with the semantic richness and controllability of vision-centric foundation models. These systems are envisioned to provide task-aware, uncertainty-calibrated priors that can be fine-tuned online. Several open challenges remain: scalable temporal memory, principled safety validation, and energy-efficient training. If these hurdles are overcome, world-model pre-training is likely to become the standard backbone for all levels of autonomous-driving software. 

## **4.3 Data Generation for Training** 

Large-scale autonomous–driving datasets are still dominated by natural logs collected with expensive fleets, yet §3.1 shows that modern world-model generators can manufacture much of what a learner needs. Early _image-centric_ systems [108, 195] could only replay low-resolution clips, but the latest diffusion and Transformer models [54, 77, 124, 171] fuse text, HD-map, trajectory and sensor cues to paint photorealistic, action-conditioned street scenes that retain long-range temporal coherence. Their synthetic videos supplement rare night, rain and construction frames and feed directly into perception or closed-loop policy training. _A parallel stream_ converts multi-view imagery or sparse LiDAR into structured representations before generation. BEV pipelines [2, 76, 242] first lift observations into a bird’s-eye lattice, then roll the lattice forward to harvest scene and intention labels at centimetre accuracy while filtering away distracting appearance noise. _Occupancy-grid diffusion_ [8, 192] and _tokenised voxel Transformers_ [220, 241] push this idea further: they stochastically sculpt 4D grids that obey physics, provide dense semantics and can be queried by planners for risk-aware cost volumes. Finally, _LiDAR-native approaches_ [79, 253] learn score-based or latent denoisers on range images, recreating full sweeps with realistic sensor noise and occlusion artefacts; these meshes or point clouds supply geometry-heavy tasks ( _e.g_ ., mapping, motion forecasting) without camera bias. Table 5 summarises representative methods and how their synthetic outputs feed into training. 

Compared with hand-coded simulators, generator-based data pipelines offer three tangible benefits. 

- Coverage: By conditioning on control commands, generators extrapolate to corner cases absent from logs. 

- Fidelity: Multi-modal diffusion preserves cross-view consistency and metre-accurate depth, which classical game engines still struggle to match. 

- Efficiency: Once trained they amortise fleet costs, allowing continuous data refresh through cheap sampling rather than fresh drives. 

However, challenges remain: high-resolution diffusion is GPU-hungry; precise camera calibration is required for viewto-view consistency; and safety assessment of purely synthetic curricula is still an open research problem. Nevertheless, Manuscript submitted to ACM 

WMAD 

19 


Fig. 5. **Application areas and tasks** (§5). (a) Scene understanding fuses multi-camera/LiDAR into a 4D BEV latent that updates every frame, giving precise geometry. (b) Motion prediction rolls latent forward under action cues, outputting collision fields for planners. (c) Simulation turns the generator into an editable 4D world where diffusion seeds rare traffic for safe closed-loop tests. (d) End-to-end driving joins perception, prediction and control in one autoregressive policy. 

data generation has evolved from a niche augmentation trick to a central pillar of autonomous-driving training pipelines, and future hybrids that blend LiDAR-tight geometry with image-level semantics are expected to yield even richer corpora for end-to-end learning. 

## **5 Application Areas and Tasks** 

Through the integration of world models, autonomous driving systems have made progress in tasks such as scene understanding, motion prediction, simulation, and end-to-end driving, demonstrating greater reliability and adaptability. 

## **5.1 Scene Understanding** 

High-fidelity 3D reconstruction is vital, but real sensors are noisy and costly to label. World models answer by compressing multi-camera and LiDAR streams into a unified spatio-temporal latent that continuously refreshes as new frames arrive. _Early 4D pre-training_ shows that one memory state can support detection, mapping and tracking without task-specific heads [149]. Subsequent _BEV-centric tokenisers_ project all modalities into a compact bird’s-eye lattice; decoding that lattice back to pixels or point clouds yields high-resolution semantics and largely removes the need for manual fusion heuristics [235]. _A parallel line_ predicts dense 3D occupancies instead of bounding boxes [252], giving planners free-space priors that remain topologically consistent over seconds rather than frames [192, 241]. _Physical realism_ continues to rise as neural volumetric splats attach radiance and density to each voxel, turning the map into a differentiable oracle for visibility or risk gradients [87, 103]. These advances collapse sensor boundaries, cut annotation budgets, and make scene understanding an anticipatory rather than reactive module; the price is GPU memory and still-uncertain safety certificates for learned geometry. 

## **5.2 Motion Prediction** 

Future-state inference has moved from extrapolating agent boxes to rolling the latent world forward. Diffusion-based generators evolve the entire scene as a 4D occupancy video that enforces basic physical-consistency losses, allowing planners to clamp candidate ego trajectories and query collision risk in milliseconds [192]. Tokenised video models extend horizons beyond a minute while preserving fine intent cues, widening the temporal window for congestion management and logistics scheduling [66]. Vision-centric hybrids link these 4D forecasts to an end-to-end planner, delivering action-controllable occupancy roll-outs that bypass separate mapping stages [220]. Behaviour realism improves when multi-agent personalities are embedded inside the world; latent “traffic bots” yield socially plausible manoeuvres without brittle lane-change heuristics [180, 237]. The unified latent now integrates map topology, social 

Manuscript submitted to ACM 

T. Feng et al. 

20 

norms, and kinematics, delivering probability fields that planners can sample or edit instead of juggling disparate trajectory sets. Remaining challenges lie in compute-heavy diffusion roll-outs and the calibration of epistemic uncertainty when imagined futures drift far from training data. 

## **5.3 Simulation** 

Traditional game-engine simulators cannot keep pace with the diversity and rare traffic cases. Generative world models fill that gap by producing controllable, multi-modal replicas of the road. Latent-diffusion frameworks synthesize multicamera sequences with pixel-level realism and cross-view depth consistency, strong enough for perception-regression tests and data augmentation [54, 77, 171]. Cascade pipelines further blend simulator geometry with real video priors, shrinking the sim-to-real gap and measurably improving BEV detectors when synthetic clips are mixed into training corpora [124, 247]. Geometry-first approaches generate long 4D occupancy volumes, supplying verification tools with dense physical states rather than mere imagery [60, 65, 192]. High-fidelity platforms now close the interaction loop, letting policies influence rendered frames each step and revealing covariate-shift failures before road deployment [212, 219, 222]. However, GPU cost and regulatory acceptance remain hurdles. 

## **5.4 End-to-End Driving** 

End-to-end pipelines once mapped pixels directly to control signals through black-box regression; world models now provide the memory, foresight and language hooks that make such systems transparent and data-efficient. Generative architectures recast driving as next-token prediction in a multimodal language, producing future frames and waypoint plans that lower collision rates compared with deterministic baselines [26, 242]. Large closed-loop models integrate perception, prediction and control inside a single autoregressive policy, evaluating imagined futures every control cycle to boost rule compliance and ride comfort [243]. Language-vision transformers extend controllability: a single sequence model now obeys natural-language directives like “yield at the zebra crossing, then merge” without extra planners [26, 182]. Lightweight augmentations place a predictive head in front of imitation layers; gradients through imagined roll-outs have been reported to reduce real-world data requirements and expose intermediate occupancy maps for audit [125, 127]. Token limits and long-horizon coherence remain open issues. 

## **6 Performance Comparison** 

This section presents an evaluation of world models for autonomous driving across tasks and metrics. Based on discussions in §5, representative algorithms are benchmarked to provide evidence of their strengths and limitations. 

## **6.1 Evaluation Platforms and Benchmarks** 

**CarlaSC.** CarlaSC [205] is a synthetic dataset generated via CARLA, offering 4D occupancy at 128×128×8 resolution within a 25 _._ 6 _𝑚_ ×25 _._ 6 _𝑚_ × 3 _𝑚_ volume around the ego-vehicle. 

**NuScenes.** nuScenes [17] contains 1 _,_ 000 scenes split into 700 train, 150 val, and 150 test. It includes six RGB cameras (360<sup>◦</sup> ) and 32-beam LiDAR with centimeter-level accuracy. 

**Occ3D-nuScenes.** Occ3D-nuScenes [184] is built from nuScenes with 700 training and 150 validation sequences, each with ∼40 frames at 2Hz. 

**Occ3D-Waymo.** Occ3D-Waymo [184] is based on Waymo [179], with 798 training and 202 validation sequences, each ∼200 frames at 10Hz, covering 17 semantic classes. Manuscript submitted to ACM 

WMAD 

21 

Table 6. **4D scene generation comparison** (§6.2). Metrics reported for OccSora [192] _vs_ DynamicCity [8] on CarlaSC [205] and Occ3D-Waymo [184], in both 2D and 3D evaluation spaces. 

|Dataset|Method|#Frames|IS↑|FID↓|2D Metrics<br>KID↓|P↑|R↑|IS↑|FID↓|3D Metrics<br>KID↓|P↑|R↑|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|CarlaSC|OccSora[192]|16|1.030|28.55|0.008|0.224|0.010|2.257|1559|52.72|0.380|0.151|
||DynamicCity[8]||**1.040**|**12.94**|**0.002**|**0.307**|**0.018**|**2.331**|**354.2**|**19.10**|**0.460**|**0.170**|
|O3D-W|OccSora[192]|16|1.005|42.53|0.049|0.654|0.004|3.129|3140|12.20|0.384|0.001|
|ccaymo|DynamicCity[8]||**1.010**|**36.73**|**0.001**|**0.705**|**0.015**|**3.206**|**1806**|**77.71**|**0.494**|**0.026**|


Table 7. **Point cloud forecasting** performance on OpenScene [236] mini val set (§6.3). 

|Method|0.5s|1.0s|Chamfer Distance (m<sup>2</sup>)↓<br>1.5s<br>2.0s|2.5s|3.0s|Avg.|
|---|---|---|---|---|---|---|
|ViDAR [221]|1.34|1.43|1.51<br>1.60|1.71|1.86|1.58|
|DFIT-OccWorld-O [229]|0.38|0.72|0.74<br>0.75|0.79|0.86|0.70|
|DFIT-OccWorld-V[229]|0.40|0.75|0.78<br>0.83|0.89|0.90|0.76|


**OpenScene.** OpenScene [236], from nuPlan [20], spans over 120 hours across four cities with 600 _,_ 000+ frames. It uses eight cameras and five LiDARs. OpenScene-mini has 5 _,_ 392 train and 8 _,_ 729 val frames. 

## **6.2 4D Scene Generation** 

4D Scene Generation refers to the task of synthesizing temporally coherent 3D scene sequences that evolve over time, effectively capturing both spatial and temporal dynamics. 

**Metrics.** For 4D Scene Generation, both 2D and 3D perceptual quality metrics are employed: (i) Inception Score (IS) ↑; (ii) Fréchet Inception Distance (FID) ↓; (iii) Kernel Inception Distance (KID) ↓; (iv) Precision (P) ↑; (v) Recall (R) ↑. **Results.** To evaluate the effectiveness of DynamicCity [8] in 4D scene generation, comparisons are conducted against OccSora [192] on the Occ3D-Waymo [184] and CarlaSC [205] benchmarks. As reported in Table 6, IS, FID, KID, P, and R are measured in both 2D and 3D spaces. Across both benchmarks and evaluation spaces, DynamicCity consistently delivers higher perceptual quality (IS, FID) and stronger fidelity-diversity trade-offs, validating its effectiveness in generating realistic 4D scenes. Looking forward, research is converging on geometry-consistent 4D diffusion with text/trajectory/physics conditioning and unified RGB-depth-occupancy rendering to support interactive simulators. 

## **6.3 Point Cloud Forecasting** 

Point cloud forecasting is a self-supervised task that predicts future point clouds from past observations, traditionally using range-image projections processed by 3D convolutions or LSTMs while explicitly modeling sensor motion. **Metrics.** Chamfer Distance (CD) ↓ are employed as evaluation metric for point cloud forecasting. CD measures the similarity between a predicted point cloud and its ground-truth counterpart. Lower CD values indicate higher fidelity in capturing the true spatial distribution of points. 

**Results.** Table 7 shows that both DFIT-OccWorld variants substantially outperform the ViDAR baseline at every forecast horizon. DFIT-OccWorld-O trims mean CD to 0.70m<sup>2</sup> and stays ahead of ViDAR across all horizons; the V-variant follows at 0.76m<sup>2</sup> , and the gap widens as lead time grows. The field is shifting from range-image CNN/LSTM to token-based diffusion, leveraging image priors and physics constraints to sustain long-horizon precision. 

## **6.4 4D Occupancy Forecasting** 

This subsection examines models’ capabilities to perceive and predict dynamic scenes, focusing on how moving objects and their interactions evolve over time. 

Manuscript submitted to ACM 

T. Feng et al. 

22 

Table 8. **4D occupancy forecasting on the Occ3D-nuScenes [184] dataset** (§6.4). Aux. Sup. denotes auxiliary supervision apart from the ego trajectory. Avg. denotes the average performance of that in 1s, 2s, and 3s. 

|Method|Inut|Aux Su||mIo|U↑|||Io|U↑||
|---|---|---|---|---|---|---|---|---|---|---|
||p|.p.|1s|2s|3s|Avg.|1s|2s|3s|Avg.|
|Copy&Paste|3D-Occ|None|14.91|10.54|8.52|11.33|24.47|19.77|17.31|20.52|
|OccWorld [241]|3D-Occ|None|25.78|15.14|10.51|17.14|34.63|25.07|20.18|26.63|
|RenderWorld [213]|3D-Occ|None|28.69|18.89|14.83|20.80|37.74|28.41|24.08|30.08|
|OccLLaMA-O [199]|3D-Occ|None|25.05|19.49|15.26|19.93|34.56|28.53|24.41|29.17|
|Occ-LLM [210]|3D-Occ|None|24.02|21.65|17.29|20.99|36.65|32.14|28.77|32.52|
|DFIT-OccWorld-O [229]|3D-Occ|None|31.68|21.29|15.18|22.71|40.28|31.24|25.29|32.27|
|DOME-O [60]|3D-Occ|None|35.11|25.89|20.29|27.10|43.99|35.36|29.74|36.36|
|AFMWM[134]|3D-Occ|None|36.42|27.39|21.66|28.49|43.68|36.89|31.98|37.52|
|UniScene [114]<br>|3D-Occ|None|35.37|29.59|25.08|31.76|38.34|32.70|29.09|34.84|
|I<sup>2</sup>-World-O [132]|3D-Occ|None|47.62|38.58|32.98|39.73|54.29|49.43|45.69|49.80|
|T<sup>3</sup>Former-O[209]|3D-Occ|None|46.32|33.23|28.73|36.09|77.00|75.89|76.32|76.40|
|RenderWorld [213]|Camera|Occ|2.83|2.55|2.37|2.58|14.61|13.61|12.98|13.73|
|TPVFormer [85]+Lidar+OccWorld-T [241]|Camera|Semantic LiDAR|4.68|3.36|2.63|3.56|9.32|8.23|7.47|8.34|
|TPVFormer [85]+SelfOcc [84]+OccWorld-S [241]|Camera|None|0.28|0.26|0.24|0.26|5.05|5.01|4.95|5.00|
|OccWorld-F [199]|Camera|Occ|8.03|6.91|3.54|6.16|23.62|18.13|15.22|18.99|
|OccLLaMA-F [199]|Camera|Occ|10.34|8.66|6.98|8.66|25.81|23.19|19.97|22.99|
|GWM [46]|Camera|Occ|11.63|10.07|8.17|10.12|26.22|24.97|22.13|24.60|
|DOME-F [60]|Camera|None|24.12|17.41|13.24|18.25|35.18|27.90|23.435|28.84|
|DFIT-OccWorld [229]|Camera|3D-Occ|13.38|10.16|7.96|10.50|19.18|16.85|15.02|17.02|
|I<sup>2</sup>-World-STC [132]|Camera|None|21.67|18.78|16.47|18.97|30.55|28.76|26.99|28.77|
|T<sup>3</sup>Former-F[209]|Camera|Occ|24.87|18.30|15.63|19.60|38.98|37.45|31.89|36.11|


Table 9. **Motion planning on the nuScenes [17] dataset** (§6.5). Aux.Sup. denotes auxiliary supervision apart from the ego trajectory. We source the results from their respective papers. 

|Mhd|I|A S||L2 (|m)↓|||Collision|Rate (%)↓||
|---|---|---|---|---|---|---|---|---|---|---|
|eto|nput|ux. up.|1s|2s|3s|Avg.|1s|2s|3s|Avg.|
|NMP [226]|LiDAR|Box & Motion|0.53|1.25|2.67|1.48|0.04|0.12|0.87|0.34|
|FF [78]|LiDAR|Freespace|0.55|1.20|2.54|1.43|0.06|0.17|1.07|0.43|
|EO[106]|LiDAR|Freespace|0.67|1.36|2.78|1.60|0.04|0.09|0.88|0.33|
|ST-P3 [80]|Camera|Map & Box & Depth|1.33|2.11|2.90|2.11|0.23|0.62|1.27|0.71|
|UniAD [82]|Camera|Map & Box & Motion & Tracklets & Occ|0.48|0.96|1.65|1.03|0.05|0.17|0.71|0.31|
|UniAD+DriveWorld [149]|Camera|Map & Box & Motion & Tracklets & Occ|0.34|0.67|1.07|0.69|0.04|0.12|0.41|0.19|
|DriveDreamer [195]|Camera|Map & Box & Motion|-|-|-|0.29|-|-|-|0.15|
|GenAD [242]|Camera|Map & Box & Motion|0.36|0.83|1.55|0.91|0.06|0.23|1.00|0.43|
|OccWorld-T [241]|Camera|Semantic LiDAR|0.54|1.36|2.66|1.52|0.12|0.40|1.59|0.70|
|OccWorld-S [241]|Camera|None|0.67|1.69|3.13|1.83|0.19|1.28|4.59|2.02|
|Drive-OccWorld [220]|Camera|None|0.32|0.75|1.49|0.85|0.05|0.17|0.64|0.29|
|ViDAR [221]|Camera|None|-|-|-|0.91|-|-|-|0.23|
|OccWorld-F [199]|Camera|Occ|0.45|1.33|2.25|1.34|0.08|0.42|1.71|0.73|
|OccLLaMA-F [199]|Camera|Occ|0.38|1.07|2.15|1.20|0.06|0.39|1.65|0.70|
|RenderWorld [213]|Camera|Occ|0.48|1.30|2.67|1.48|0.14|0.55|2.23|0.97|
|DFIT-OccWorld-V [229]|Camera|Occ|0.42|1.14|2.19|1.25|0.09|0.19|1.37|0.55|
|GWM [46]|Camera|Occ|0.24|1.01|2.05|1.13|0.07|0.26|1.45|0.59|
|UncAD [218]|Camera|None|0.33|0.59|0.94|0.62|0.10|0.14|0.28|0.17|
|FSDrive[225]|Camera|Ego status|0.14|0.25|0.46|0.28|0.03|0.06|0.21|0.10|
|OccWorld [241]|3D-Occ|None|0.43|1.08|1.99|1.17|0.07|0.38|1.35|0.60|
|RenderWorld [213]|3D-Occ|None|0.35|0.91|1.84|1.03|0.05|0.40|1.39|0.61|
|OccLLaMA-O [199]|3D-Occ|None|0.37|1.02|2.03|1.14|0.04|0.24|1.20|0.49|
|DFIT-OccWorld-O [229]|3D-Occ|None|0.38|0.96|1.73|1.02|0.07|0.39|0.90|0.45|
|T<sup>3</sup>Former-O[209]|3D-Occ|None|0.32|0.91|1.76|1.00|0.08|0.32|0.51|0.30|


**Metrics.** The evaluation of occupancy forecasting relies on mIoU and IoUs to gauge how accurately each future frame’s semantic occupancy is recovered, while placing additional emphasis on temporal accuracy and consistency across multiple time horizons ( _e.g_ ., 1s, 2s, 3s). 

**Results.** Table 8 summarizes the 4D occupancy forecasting performance on Occ3D-nuScenes [184], where predictions for 1s, 2s, and 3s into the future are assessed via mIoU and IoU. Notably, I<sup>2</sup> -World-O [132] and T<sup>3</sup> Former-O [209] attain state-of-the-art results, surpassing baseline methods. Even the purely camera-based T<sup>3</sup> Former-F variant remains highly competitive, reflecting the model’s robustness in scenarios without direct 3D occupancy supervision. Future advances target tokenised or diffusion backbones that accept language or trajectory prompts and camera-only pipelines that cut LiDAR cost while keeping real-time viability. 

Manuscript submitted to ACM 

WMAD 

23 

## **6.5 Motion planning** 

Motion planning rapidly generates collision-free, energy-aware trajectories by considering obstacles, road layout, and surrounding vehicles, promoting safety and efficiency. 

**Metrics.** The evaluation of motion planning centers on key aspects such as L2 error and collision rate. L2 error quantifies how closely a planned trajectory tracks the reference or desired path, while collision rate measures the frequency of unsafe interactions with obstacles. 

**Results.** Table 9 reports motion-planning results on nuScenes [17]. For camera end-to-end planners, adding rich supervision markedly helps: UniAD+DriveWorld reduces the average L2 error for -33% and the average collision rate for -39% compared with UniAD [82]. In the 3D-occupancy input regime, T<sup>3</sup> Former-O achieves the best trade-off with 1.00m average L2 and 0.30 average collision, cutting 3s collisions by ∼62% and halving the average collision rate (0.60%→0.30%) versus OccWorld. The best performance is from FSDrive (0.28m/0.10%), but it relies on privileged ego status supervision, making it less directly comparable to fully perception-driven planners. Overall, the table highlights that richer supervision improves accuracy and safety, while occupancy-centric models can remain competitive. 

## **7 Future Research Directions** 

This section surveys four frontier directions – self-supervised learning, multi-modal fusion, advanced simulation, and efficient architectures – that aim to reduce label dependence, sharpen perception and planning, boost simulation realism, and enable resource-aware deployment. 

## **7.1 Self-Supervised World Models** 

Self-supervision has already proven that large amounts of annotated data are useful but not indispensable. **Reducing Label Dependency.** Upcoming work is expected to couple cross-modal reconstruction (images ↔ LiDAR ↔ occupancy) with strong physics-based consistency losses. By letting each sensor stream synthesize or critique the others, a single model can refine depth, motion, and semantics without ever seeing a hand-drawn box. Generative objectives ( _e.g_ ., long-horizon video rollout, stochastic occupancy completion, or latent LiDAR synthesis) will serve as ‘free’ supervision signals that capture rare weather, lighting, and traffic events. Combined with lightweight on-device distillation and sparse activation routing, these techniques promise to slash annotation budgets while keeping the model small enough for automotive hardware. 

**Exploring Unlabeled Data Potential.** Beyond saving labels, the frontier is to _unlock the structure_ hidden in the ocean of raw fleet logs. Self-supervised world models will (i) maintain a long-term memory that adapts online yet respects safety guarantees, (ii) roll imagined futures to train planners entirely in latent space, and (iii) estimate aleatoric and epistemic uncertainty on-the-fly so that risk grows when the model drifts away from familiar distributions. Coupling these world models with reinforcement learning agents turns every kilometre (real or simulated) into a self-improvement step, gradually building a driving policy that requires fewer interventions and generalises across cities. 

## **7.2 Multi-Modal World Models** 

Packing images, point clouds, and BEV cues into a single latent already lifts perception, prediction, and planning. The next wave seeks universal embeddings that ingest any sensor ( _e.g_ ., camera, LiDAR, radar, event, or thermal) without hand-tuned adapters. Three paths emerge: (i) ultra-compact cross-modal tokenisers that keep geometry and texture yet run on car-grade GPUs; (ii) self-aligning schedulers that weld asynchronous packets into causally consistent world 

Manuscript submitted to ACM 

T. Feng et al. 

24 

states; (iii) curriculum objectives uniting differentiable rendering, language grounding, and physics-aware roll-outs so semantics, intent, and constraints co-evolve. Realising these goals would give vehicles a single, continuously refreshed memory that streamlines control, supports life-long adaptation, and sustains robustness under sensor degradation. 

## **7.3 Advanced Simulation** 

**Physics Engine.** Physics-aware generation steers autonomous-driving simulators. DrivePhysica aligns ego/world frames, injects 3D flows, and applies box-guided occlusion, yielding multi-camera videos [223]. Future platforms fuse diffusion world models with differentiable rigid, soft, fluid, and thermal solvers in one loop. Diffusion priors sketch 4D occupancy while the solver enforces Newtonian laws, ensuring validity and gradients that reveal traction loss, drag, or sensor occlusion before deployment. 

**Cross-Scenario Generalization.** Next-generation simulators will synthesize domain-agnostic worlds spanning cities, seasons, and driving styles. Interaction corpora toughen policies in unseen regions, while text-guided generators inject rare hazards and cultural norms to push controllers beyond sensor priors. Hybrid neural-physics engines let weather, lighting, and dynamics be tuned on the fly, unifying perception tests, policy search, and safety proofs. The goal is a fully differentiable sandbox where traffic rules, multi-agent uncertainty, and physics co-evolve, enabling auto-curricula and online co-training to shorten real-world validation. 

**Real-World Validation.** Modern volumetric rendering, panoramic synthesis, and cross-modal alignment let simulators mirror city traffic with centimetre geometry, photorealism across weather, and agent motion. This fidelity boosts detector pre-training, fortifies long-horizon planners, and exposes corner-case failures before road tests, while physics-based sensors and diffusion controllers keep synthetic trajectories feasible. Continuous loops align simulated outputs with fleet telemetry, producing scalable, balanced scenarios that accelerate research and validation across perception, prediction, and control. 

**Diffusion-based Generation.** Diffusion-based world modelling is converging toward unified generators that synthesise kilometre-long journeys while remaining tractable on embedded hardware. Progress unfolds along four axes. First, spatial coverage widens from single images to volumetric 4D roll-outs, giving planners seconds of geometry and exposing long-horizon corner cases. Second, richer conditioning blends panoramic cameras, text, motion plans, and physics priors so each sample obeys traffic rules, weather, and social etiquette. Third, efficiency improves through tokenised latents, causal masking, and hierarchical caches that cut memory and latency without sacrificing detail. Fourth, interactive editing enables on-the-fly swaps of agents, lanes, or illumination, turning the generator into a reusable testbed. Paired with emerging perception-plus-control benchmarks, these strands point toward self-improving simulators that shorten validation cycles, reduce data costs, and hasten autonomous-driving deployment. 

## **7.4 Efficient World Models** 

Looking forward, efficient world models will rely on lean, latency-aware backbones that fuse sensing, prediction, and control in a single sweep. One shared feature reservoir – drawing jointly on vision, depth, and map cues – will serve every downstream head, eliminating costly re-projection. Lightweight language adapters will weave route guidance and traffic regulations into this common space. Scene motion will be roughed out as coarse flow; only ambiguous regions will be up-sampled into dense volumes, slashing computation. Multi-scale grids will stream context before zooming into high-detail regions around dynamic agents, conserving memory. Capacity-elastic layers will monitor feature entropy and activate deeper blocks only when congestion rises, sustaining real-time performance on modest vehicle GPUs. 

Manuscript submitted to ACM 

WMAD 

25 

Coupled with edge quantisation and federated updates, these systems will learn continually from fleet data while respecting power, bandwidth, and privacy limits – bringing scalable, safety-critical autonomy within tangible reach. 

## **8 Conclusion** 

World models have rapidly become a cornerstone for autonomous driving, enabling deeper integration among perception, prediction, and decision-making. Recent advances in multi-modal fusion unify data from cameras, LiDAR, and other sensors, while self-supervised learning and large-scale pretraining reduce dependence on annotated datasets. Generative methods, particularly diffusion-based approaches, now facilitate diverse synthetic data for long-tail scenarios, enhancing model robustness in rare or extreme conditions. New frameworks tightly couple motion prediction with planning algorithms, moving toward closed-loop paradigms that promise safer, more adaptive navigation. As sensing technologies evolve and cross-domain datasets proliferate, world models are poised to become even more integral to the reliable, large-scale deployment of next-generation autonomous driving systems. 

## **References** 

- [1] Bhargav Adabala and Zlatan Ajanović. 2023. A Multi-Heuristic Search-based Motion Planning for Automated Parking. In _Proc. Int. Conf. Inf., Commun. Automat. Technol._ IEEE, 1–8. 

- [2] Ben Agro, Quinlan Sykora, Sergio Casas, Thomas Gilles, and Raquel Urtasun. 2024. UnO: Unsupervised Occupancy Fields for Perception and Forecasting. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 14487–14496. 

- [3] Zlatan Ajanovic. 2019. Towards SuperHuman autonomous vehicles. (2019). 

- [4] Zlatan Ajanovic, Bakir Lacevic, Barys Shyrokau, Michael Stolz, and Martin Horn. 2018. Search-based optimal motion planning for automated driving. In _Proc. IEEE/RSJ Int. Conf. Intell. Robot. Syst._ IEEE, 4523–4530. 

- [5] Zlatan Ajanović, Enrico Regolin, Barys Shyrokau, Hana Ćatić, Martin Horn, and Antonella Ferrara. 2023. Search-based task and motion planning for hybrid systems: Agile autonomous vehicles. _arXiv preprint arXiv:2301.10384_ (2023). 

- [6] Adil Kaan Akan and Fatma Güney. 2022. Stretchbev: Stretching future instance prediction spatially and temporally. In _Proc. Eur. Conf. Comput. Vis._ Springer, 444–460. 

- [7] Florent Bartoccioni, Elias Ramzi, Victor Besnier, Shashanka Venkataramanan, Tuan-Hung Vu, Yihong Xu, Loick Chambon, Spyros Gidaris, Serkan Odabas, David Hurych, et al. 2025. VaViM and VaVAM: Autonomous Driving through Video Generative Modeling. _arXiv preprint arXiv:2502.15672_ (2025). 

- [8] Hengwei Bian, Lingdong Kong, Haozhe Xie, Liang Pan, Yu Qiao, and Ziwei Liu. 2025. DynamicCity: Large-Scale 4D Occupancy Generation from Dynamic Scenes. In _Proc. Int. Conf. Learn. Represent._ 

- [9] Daniel Bogdoll, Noël Ollick, Tim Joseph, Svetlana Pavlitska, and J Marius Zöllner. 2024. UMAD: Unsupervised Mask-Level Anomaly Detection for Autonomous Driving. _arXiv preprint arXiv:2406.06370_ (2024). 

- [10] Daniel Bogdoll, Yitian Yang, and J Marius Zöllner. 2023. Muvo: A multimodal generative world model for autonomous driving with geometric representations. In _Proc. IEEE Intell. Veh. Symp._ 

- [11] Jon Bohren, Tully Foote, Jim Keller, Alex Kushleyev, Daniel Lee, Alex Stewart, Paul Vernaza, Jason Derenick, John Spletzer, and Brian Satterfield. 2009. Little ben: The ben franklin racing team’s entry in the 2007 darpa urban challenge. In _The DARPA Urban Challenge_ . Springer, 231–255. 

- [12] Mariusz Bojarski, Davide Del Testa, Daniel Dworakowski, Bernhard Firner, Beat Flepp, Prasoon Goyal, Lawrence D Jackel, Mathew Monfort, Urs Muller, Jiakai Zhang, et al. 2016. End to end learning for self-driving cars. _arXiv preprint arXiv:1604.07316_ (2016). 

- [13] Zahra Boroujeni, Daniel Goehring, Fritz Ulbrich, Daniel Neumann, and Raul Rojas. 2017. Flexible unit A-star trajectory planning for autonomous vehicles on structured road maps. In _Proc. IEEE Int. Conf. Veh. Electron. Saf._ IEEE, 7–12. 

- [14] Farid Bounini, Denis Gingras, Herve Pollart, and Dominique Gruyer. 2017. Modified artificial potential field method for online path planning applications. In _Proc. IEEE Intell. Veh. Symp._ IEEE, 180–185. 

- [15] Martin Buehler, Karl Iagnemma, and Sanjiv Singh. 2009. _The DARPA Urban Challenge: Autonomous Vehicles in City Traffic_ (1st ed.). Springer Publishing Company, Incorporated. 

- [16] Lucas Caccia, Herke Van Hoof, Aaron Courville, and Joelle Pineau. 2019. Deep generative modeling of lidar data. In _Proc. IEEE/RSJ Int. Conf. Intell. Robot. Syst._ IEEE, 5034–5040. 

- [17] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. 2020. nuscenes: A multimodal dataset for autonomous driving. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 11621–11631. 

- [18] Holger Caesar, Juraj Kabzan, Kok Seang Tan, Whye Kit Fong, Eric Wolff, Alex Lang, Luke Fletcher, Oscar Beijbom, and Sammy Omari. 2021. nuplan: A closed-loop ml-based planning benchmark for autonomous vehicles. _arXiv preprint arXiv:2106.11810_ (2021). 

Manuscript submitted to ACM 

T. Feng et al. 

26 

- [19] Luca Caltagirone, Mauro Bellone, Lennart Svensson, and Mattias Wahde. 2017. LIDAR-based driving path generation using fully convolutional neural networks. In _Proc. IEEE Int. Conf. Intell. Transp. Syst._ IEEE, 1–6. 

- [20] Anh-Quan Cao and Raoul De Charette. 2022. Monoscene: Monocular 3d semantic scene completion. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 

- [21] CARLA Team. 2022. CARLA: Autonomous Driving Leaderboard. https://leaderboard.carla.org/. 

- [22] Sergio Casas, Abbas Sadat, and Raquel Urtasun. 2021. Mp3: A unified model to map, perceive, predict and plan. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 14403–14412. 

- [23] Anthony Chen, Wenzhao Zheng, Yida Wang, Xueyang Zhang, Kun Zhan, Peng Jia, Kurt Keutzer, and Shanghang Zhang. 2025. Geodrive: 3d geometry-informed driving world model with precise action control. _arXiv preprint arXiv:2505.22421_ (2025). 

- [24] Junliang Chen, Huaiyuan Xu, Yi Wang, and Lap-Pui Chau. 2025. Occprophet: Pushing efficiency frontier of camera-only 4d occupancy forecasting with observer-forecaster-refiner framework. In _Proc. Int. Conf. Learn. Represent._ 

- [25] Keyu Chen, Wenchao Sun, Hao Cheng, and Sifa Zheng. 2025. RIFT: Closed-Loop RL Fine-Tuning for Realistic and Controllable Traffic Simulation. _arXiv preprint arXiv:2505.03344_ (2025). 

- [26] Yuntao Chen, Yuqi Wang, and Zhaoxiang Zhang. 2024. DrivingGPT: Unifying Driving World Modeling and Planning with Multi-modal Autoregressive Transformers. _arXiv preprint arXiv:2412.18607_ (2024). 

- [27] Kashyap Chitta, Aditya Prakash, and Andreas Geiger. 2021. Neat: Neural attention fields for end-to-end autonomous driving. In _Proc. IEEE Int. Conf. Comput. Vis._ 15793–15803. 

- [28] Kashyap Chitta, Aditya Prakash, Bernhard Jaeger, Zehao Yu, Katrin Renz, and Andreas Geiger. 2022. Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. _IEEE Trans. Pattern Anal. Mach. Intell._ 45, 11 (2022), 12878–12895. 

- [29] Keonyup Chu, Minchae Lee, and Myoungho Sunwoo. 2012. Local path planning for off-road autonomous driving with avoidance of static obstacles. _Proc. IEEE Int. Conf. Intell. Transp. Syst._ 13, 4 (2012), 1599–1616. 

- [30] Felipe Codevilla, Eder Santana, Antonio M López, and Adrien Gaidon. 2019. Exploring the limitations of behavior cloning for autonomous driving. In _Proc. IEEE Int. Conf. Comput. Vis._ 9329–9338. 

- [31] OpenScene Contributors. 2023. OpenScene: The Largest Up-to-Date 3D Occupancy Prediction Benchmark in Autonomous Driving. 

- [32] Marius Cordts, Mohamed Omran, Sebastian Ramos, Timo Rehfeld, Markus Enzweiler, Rodrigo Benenson, Uwe Franke, Stefan Roth, and Bernt Schiele. 2016. The cityscapes dataset for semantic urban scene understanding. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 3213–3223. 

- [33] Daniel Dauner, Marcel Hallgarten, Andreas Geiger, and Kashyap Chitta. 2023. Parting with Misconceptions about Learning-based Vehicle Motion Planning. In _Conf. Robot Learn._ 

- [34] Daniel Dauner, Marcel Hallgarten, Tianyu Li, Xinshuo Weng, Zhiyu Huang, Zetong Yang, Hongyang Li, Igor Gilitschenski, Boris Ivanovic, Marco Pavone, et al. 2024. Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking. In _Proc. Adv. Neural Inf. Process. Syst._ , Vol. 37. 28706–28719. 

- [35] Christopher Diehl, Timo Sebastian Sievernich, Martin Krüger, Frank Hoffmann, and Torsten Bertram. 2023. Uncertainty-aware model-based offline reinforcement learning for automated driving. _IEEE Robot. Autom. Lett._ 8, 2 (2023), 1167–1174. 

- [36] Jingtao Ding, Yunke Zhang, Yu Shang, Yuheng Zhang, Zefang Zong, Jie Feng, Yuan Yuan, Hongyuan Su, Nian Li, Nicholas Sukiennik, et al. 2024. Understanding World or Predicting Future? A Comprehensive Survey of World Models. _arXiv preprint arXiv:2411.14499_ (2024). 

- [37] Wenhao Ding, Yulong Cao, Ding Zhao, Chaowei Xiao, and Marco Pavone. 2024. Realgen: Retrieval augmented generation for controllable traffic scenarios. In _Proc. Eur. Conf. Comput. Vis._ Springer, 93–110. 

- [38] Dmitri Dolgov, Sebastian Thrun, Michael Montemerlo, and James Diebel. 2008. Practical search techniques in path planning for autonomous driving. _Ann Arbor_ 1001, 48105 (2008), 18–80. 

- [39] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. 2017. CARLA: An Open Urban Driving Simulator. In _Conf. Robot Learn. (Proceedings of Machine Learning Research, Vol. 78)_ , Sergey Levine, Vincent Vanhoucke, and Ken Goldberg (Eds.). PMLR, Mountain View, CA, USA, 1–16. arXiv:1711.03938 https://proceedings.mlr.press/v78/dosovitskiy17a.html 

- [40] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. 2017. CARLA: An Open Urban Driving Simulator. In _Conf. Robot Learn. (Proc. Mach. Learn. Res., Vol. 78)_ , Sergey Levine, Vincent Vanhoucke, and Ken Goldberg (Eds.). PMLR, Mountain View, CA, USA, 1–16. https://proceedings.mlr.press/v78/dosovitskiy17a.html 

- [41] Scott Ettinger, Shuyang Cheng, Benjamin Caine, Chenxi Liu, Hang Zhao, Sabeek Pradhan, Yuning Chai, Ben Sapp, Charles R Qi, Yin Zhou, et al. 2021. Large scale interactive motion forecasting for autonomous driving: The waymo open motion dataset. In _Proc. IEEE Int. Conf. Comput. Vis._ 9710–9719. 

- [42] Daniel J. Fagnant and Kara Kockelman. 2015. Preparing a Nation for Autonomous Vehicles: Opportunities, Barriers and Policy Recommendations. _Transp. Res. Part A: Policy Pract._ 77 (2015), 167–181. doi:10.1016/j.tra.2015.04.003 

- [43] Haoyang Fan, Fan Zhu, Changchun Liu, Liangliang Zhang, Li Zhuang, Dong Li, Weicheng Zhu, Jiangtao Hu, Hongye Li, and Qi Kong. 2018. Baidu apollo em motion planner. _arXiv preprint arXiv:1807.08048_ (2018). 

- [44] Lan Feng, Quanyi Li, Zhenghao Peng, Shuhan Tan, and Bolei Zhou. 2023. Trafficgen: Learning to generate diverse and realistic traffic scenarios. In _ICRA_ . 

- [45] Tuo Feng, Wenguan Wang, Xiaohan Wang, Yi Yang, and Qinghua Zheng. 2023. Clustering based point cloud representation learning for 3d analysis. In _Proc. IEEE Int. Conf. Comput. Vis._ 8283–8294. 

Manuscript submitted to ACM 

WMAD 

27 

- [46] Tuo Feng, Wenguan Wang, and Yi Yang. 2025. Gaussian-based World Model: Gaussian Priors for Voxel-Based Occupancy Prediction and Future Motion Prediction. In _Proc. IEEE Int. Conf. Comput. Vis._ 

- [47] Ao Fu, Yi Zhou, Tao Zhou, Yi Yang, Bojun Gao, Qun Li, Guobin Wu, and Ling Shao. 2024. Exploring the Interplay Between Video Generation and World Models in Autonomous Driving: A Survey. _arXiv preprint arXiv:2411.02914_ (2024). 

- [48] Daocheng Fu, Wenjie Lei, Licheng Wen, Pinlong Cai, Song Mao, Min Dou, Botian Shi, and Yu Qiao. 2024. Limsim++: A closed-loop platform for deploying multimodal llms in autonomous driving. In _Proc. IEEE Intell. Veh. Symp._ IEEE, 1084–1090. 

- [49] Daocheng Fu, Naiting Zhong, Xu Han, Pinlong Cai, Licheng Wen, Song Mao, Botian Shi, and Yu Qiao. 2025. LimSim Series: An Autonomous Driving Simulation Platform for Validation and Enhancement. _arXiv preprint arXiv:2502.09170_ (2025). 

- [50] Andrei Furda and Ljubo Vlacic. 2011. Enabling Safe Autonomous Driving in Real-World City Traffic Using Multiple Criteria Decision Making. _IEEE Intell. Transp. Syst. Mag._ 3, 3 (2011), 4–17. doi:10.1109/MITS.2011.940472 

- [51] Enric Galceran, Ryan M Eustice, and Edwin Olson. 2015. Toward integrated motion planning and control using potential fields and torque-based steering actuation for autonomous driving. In _Proc. IEEE Intell. Veh. Symp._ IEEE, 304–309. 

- [52] Dechen Gao, Shuangyu Cai, Hanchu Zhou, Hang Wang, Iman Soltani, and Junshan Zhang. 2024. Cardreamer: Open-source learning platform for world model based autonomous driving. _IEEE Internet Things J._ (2024). 

- [53] Ruiyuan Gao, Kai Chen, Enze Xie, Lanqing HONG, Zhenguo Li, Dit-Yan Yeung, and Qiang Xu. 2024. MagicDrive: Street View Generation with Diverse 3D Geometry Control. In _Proc. Int. Conf. Learn. Represent._ 

- [54] Shenyuan Gao, Jiazhi Yang, Li Chen, Kashyap Chitta, Yihang Qiu, Andreas Geiger, Jun Zhang, and Hongyang Li. 2024. Vista: A Generalizable Driving World Model with High Fidelity and Versatile Controllability. In _Proc. Adv. Neural Inf. Process. Syst._ 

- [55] Yinfeng Gao, Qichao Zhang, Da-Wei Ding, and Dongbin Zhao. 2024. Dream to Drive With Predictive Individual World Model. _IEEE Trans. Intell. Veh._ (2024). 

- [56] Anant Garg and K Madhava Krishna. 2024. Imagine-2-Drive: High-Fidelity World Modeling in CARLA for Autonomous Vehicles. _arXiv preprint arXiv:2411.10171_ (2024). 

- [57] Andreas Geiger, Philip Lenz, and Raquel Urtasun. 2012. Are we ready for autonomous driving? the kitti vision benchmark suite. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ IEEE, 3354–3361. 

- [58] David González, Joshué Pérez, Vicente Milanés, and Fawzi Nashashibi. 2015. A review of motion planning techniques for automated vehicles. _IEEE Trans. Intell. Transp. Syst._ 17, 4 (2015), 1135–1145. 

- [59] Sorin Grigorescu, Bogdan Trasnea, Tiberiu T. Cocias, and Gigel Macesanu. 2020. A Survey of Deep Learning Techniques for Autonomous Driving. _J. Field Robot._ 37, 3 (2020), 362–386. doi:10.1002/rob.21918 

- [60] Songen Gu, Wei Yin, Bu Jin, Xiaoyang Guo, Junming Wang, Haodong Li, Qian Zhang, and Xiaoxiao Long. 2024. Dome: Taming diffusion model into high-fidelity controllable occupancy world model. _arXiv preprint arXiv:2410.10429_ (2024). 

- [61] Tianyu Gu, John M Dolan, and Jin-Woo Lee. 2016. Runtime-bounded tunable motion planning for autonomous driving. In _Proc. IEEE Intell. Veh. Symp._ IEEE, 1301–1306. 

- [62] Yanchen Guan, Haicheng Liao, Zhenning Li, Jia Hu, Runze Yuan, Yunjian Li, Guohui Zhang, and Chengzhong Xu. 2024. World Models for Autonomous Driving: An Initial Survey. _IEEE Trans. Intell. Veh._ 9 (2024). doi:10.1109/TIV.2024.3398357 early access. 

- [63] Yanchen Guan, Haicheng Liao, Chengyue Wang, Xingcheng Liu, Jiaxun Zhang, and Zhenning Li. 2025. World model-based end-to-end scene generation for accident anticipation in autonomous driving. _Communications Engineering_ 4, Article 144 (Aug. 2025). doi:10.1038/s44172-025-00474-7 

- [64] Cole Gulino, Justin Fu, Wenjie Luo, George Tucker, Eli Bronstein, Yiren Lu, Jean Harb, Xinlei Pan, Yan Wang, Xiangyu Chen, et al. 2024. Waymax: An accelerated, data-driven simulator for large-scale autonomous driving research. In _Proc. Adv. Neural Inf. Process. Syst._ , Vol. 36. 

- [65] Jiazhe Guo, Yikang Ding, Xiwu Chen, Shuo Chen, Bohan Li, Yingshuang Zou, Xiaoyang Lyu, Feiyang Tan, Xiaojuan Qi, Zhiheng Li, et al. 2025. DiST-4D: Disentangled Spatiotemporal Diffusion with Metric Depth for 4D Driving Scene Generation. In _Proc. IEEE Int. Conf. Comput. Vis._ 

- [66] Xi Guo, Chenjing Ding, Haoxuan Dou, Xin Zhang, Weixuan Tang, and Wei Wu. 2024. InfinityDrive: Breaking Time Limits in Driving World Models. _arXiv preprint arXiv:2412.01522_ (2024). 

- [67] David Ha and Jürgen Schmidhuber. 2018. Recurrent world models facilitate policy evolution. In _Proc. Adv. Neural Inf. Process. Syst._ , Vol. 31. 

- [68] David Ha and Jürgen Schmidhuber. 2018. World models. _arXiv preprint arXiv:1803.10122_ (2018). 

- [69] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. 2020. Dream to Control: Learning Behaviors by Latent Imagination. In _Proc. Int. Conf. Learn. Represent._ 

- [70] Danijar Hafner, Timothy P Lillicrap, Mohammad Norouzi, and Jimmy Ba. 2021. Mastering Atari with Discrete World Models. In _Proc. Int. Conf. Learn. Represent._ 

- [71] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. 2023. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ (2023). 

- [72] Shadi Hamdan and Fatma Güney. 2025. CarFormer: Self-Driving with Learned Object-Centric Representations. In _Proc. Eur. Conf. Comput. Vis._ Springer, 177–193. 

- [73] Mariam Hassan, Sebastian Stapf, Ahmad Rahimi, Pedro Rezende, Yasaman Haghighi, David Brüggemann, Isinsu Katircioglu, Lin Zhang, Xiaoran Chen, Suman Saha, et al. 2024. GEM: A Generalizable Ego-Vision Multimodal World Model for Fine-Grained Ego-Motion, Object Dynamics, and Scene Composition Control. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 

Manuscript submitted to ACM 

T. Feng et al. 

28 

- [74] Mikael Henaff, Alfredo Canziani, and Yann LeCun. 2018. Model-Predictive Policy Learning with Uncertainty Regularization for Driving in Dense Traffic. In _Proc. Int. Conf. Learn. Represent._ 

- [75] Anthony Hu, Gianluca Corrado, Nicolas Griffiths, Zachary Murez, Corina Gurau, Hudson Yeo, Alex Kendall, Roberto Cipolla, and Jamie Shotton. 2022. Model-based imitation learning for urban driving. In _Proc. Adv. Neural Inf. Process. Syst._ , Vol. 35. 20703–20716. 

- [76] Anthony Hu, Zak Murez, Nikhil Mohan, Sofía Dudas, Jeffrey Hawke, Vijay Badrinarayanan, Roberto Cipolla, and Alex Kendall. 2021. Fiery: Future instance prediction in bird’s-eye view from surround monocular cameras. In _Proc. IEEE Int. Conf. Comput. Vis._ 15273–15282. 

- [77] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. 2023. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ (2023). 

- [78] Peiyun Hu, Aaron Huang, John Dolan, David Held, and Deva Ramanan. 2021. Safe local motion planning with self-supervised freespace forecasting. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 12732–12741. 

- [79] Qianjiang Hu, Zhimin Zhang, and Wei Hu. 2024. RangeLDM: Fast Realistic LiDAR Point Cloud Generation. _arXiv preprint arXiv:2403.10094_ (2024). 

- [80] Shengchao Hu, Li Chen, Penghao Wu, Hongyang Li, Junchi Yan, and Dacheng Tao. 2022. St-p3: End-to-end vision-based autonomous driving via spatial-temporal feature learning. In _Proc. Eur. Conf. Comput. Vis._ Springer, 533–549. 

- [81] Xiaotao Hu, Wei Yin, Mingkai Jia, Junyuan Deng, Xiaoyang Guo, Qian Zhang, Xiaoxiao Long, and Ping Tan. 2024. DrivingWorld: ConstructingWorld Model for Autonomous Driving via Video GPT. _arXiv preprint arXiv:2412.19505_ (2024). 

- [82] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. 2023. Planningoriented autonomous driving. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 17853–17862. 

- [83] Shengyu Huang, Zan Gojcic, Zian Wang, Francis Williams, Yoni Kasten, Sanja Fidler, Konrad Schindler, and Or Litany. 2023. Neural lidar fields for novel view synthesis. In _Proc. IEEE Int. Conf. Comput. Vis._ 18236–18246. 

- [84] Yuanhui Huang, Wenzhao Zheng, Borui Zhang, Jie Zhou, and Jiwen Lu. 2024. Selfocc: Self-supervised vision-based 3d occupancy prediction. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 19946–19956. 

- [85] Yuanhui Huang, Wenzhao Zheng, Yunpeng Zhang, Jie Zhou, and Jiwen Lu. 2023. Tri-perspective view for vision-based 3d semantic occupancy prediction. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 9223–9232. 

- [86] Zilin Huang, Zihao Sheng, Zhengyang Wan, Yansong Qu, Yuhao Luo, Boyue Wang, Pei Li, Yen-Jung Chen, Jiancong Chen, Keke Long, et al. 2025. Sky-Drive: A Distributed Multi-Agent Simulation Platform for Socially-Aware and Human-AI Collaborative Future Transportation. _arXiv preprint arXiv:2504.18010_ (2025). 

- [87] Zanming Huang, Jimuyang Zhang, and Eshed Ohn-Bar. 2024. Neural volumetric world models for autonomous driving. In _Proc. Eur. Conf. Comput. Vis._ Springer, 195–213. 

- [88] Zanming Huang, Jimuyang Zhang, and Eshed Ohn-Bar. 2025. Neural Volumetric World Models for Autonomous Driving. In _Proc. Eur. Conf. Comput. Vis._ Springer, 195–213. 

- [89] Quoc Huy, Seiichi Mita, Hossein Tehrani Nik Nejad, and Long Han. 2013. Dynamic and safe path planning based on support vector machine among multi moving obstacles for autonomous vehicles. _IEICE Trans. Inf. Syst._ 96, 2 (2013), 314–328. 

- [90] Yishen Ji, Ziyue Zhu, Zhenxin Zhu, Kaixin Xiong, Ming Lu, Zhiqi Li, Lijun Zhou, Haiyang Sun, Bing Wang, and Tong Lu. 2025. Cogen: 3d consistent video generation via adaptive conditioning for autonomous driving. _arXiv preprint arXiv:2503.22231_ (2025). 

- [91] Xiaosong Jia, Li Chen, Penghao Wu, Jia Zeng, Junchi Yan, Hongyang Li, and Yu Qiao. 2023. Towards Capturing the Temporal Dynamics for Trajectory Prediction: a Coarse-to-Fine Approach. In _Conf. Robot Learn. (Proceedings of Machine Learning Research, Vol. 205)_ , Karen Liu, Dana Kulic, and Jeff Ichnowski (Eds.). PMLR, Atlanta, GA, USA, 910–920. https://proceedings.mlr.press/v205/jia23a.html 

- [92] Xiaosong Jia, Liting Sun, Masayoshi Tomizuka, and Wei Zhan. 2021. IDE-Net: Interactive Driving Event and Pattern Extraction from Human Data. _IEEE Robot. Autom. Lett._ 6, 2 (April 2021), 3065–3072. doi:10.1109/LRA.2021.3062309 

- [93] Xiaosong Jia, Penghao Wu, Li Chen, Yu Liu, Hongyang Li, and Junchi Yan. 2023. Hdgt: Heterogeneous driving graph transformer for multi-agent trajectory prediction via scene encoding. _IEEE Trans. Pattern Anal. Mach. Intell._ (2023). 

- [94] Xiaosong Jia, Zhenjie Yang, Qifeng Li, Zhiyuan Zhang, and Junchi Yan. 2024. Bench2drive: Towards multi-ability benchmarking of closed-loop end-to-end autonomous driving. In _Proc. Adv. Neural Inf. Process. Syst._ , Vol. 37. 819–844. 

- [95] Anqing Jiang, Yu Gao, Yiru Wang, Zhigang Sun, Shuo Wang, Yuwen Heng, Hao Sun, Shichen Tang, Lijuan Zhu, Jinhao Chai, et al. 2025. IRL-VLA: Training an Vision-Language-Action Policy via Reward World Model. _arXiv preprint arXiv:2508.06571_ (2025). 

- [96] Junpeng Jiang, Gangyi Hong, Miao Zhang, Hengtong Hu, Kun Zhan, Rui Shao, and Liqiang Nie. 2025. DiVE: Efficient Multi-View Driving Scenes Generation Based on Video Diffusion Transformer. _arXiv preprint arXiv:2504.19614_ (2025). 

- [97] Bu Jin, Weize Li, Baihan Yang, Zhenxin Zhu, Junpeng Jiang, Huan-ang Gao, Haiyang Sun, Kun Zhan, Hengtong Hu, Xueyang Zhang, et al. 2025. PosePilot: Steering Camera Pose for Generative World Models with Self-supervised Depth. In _Proc. IEEE/RSJ Int. Conf. Intell. Robot. Syst._ 

- [98] Sören Kammel, Julius Ziegler, Benjamin Pitzer, Moritz Werling, Tobias Gindele, Daniel Jagzent, Joachim Schöder, Michael Thuy, Matthias Goebl, Felix von Hundelshausen, et al. 2009. Team AnnieWAY’s autonomous system for the DARPA Urban Challenge 2007. In _The DARPA Urban Challenge_ . Springer, 359–391. 

- [99] Sertac Karaman and Emilio Frazzoli. 2010. Incremental Sampling-Based Algorithms for Optimal Motion Planning. In _Robotics: Science and Systems VI_ . Robotics: Science and Systems Foundation, Zaragoza, Spain. https://www.roboticsproceedings.org/rss06/p34.pdf 

- [100] Sertac Karaman and Emilio Frazzoli. 2011. Sampling-based algorithms for optimal motion planning. _Int. J. Robot. Res._ 30, 7 (2011), 846–894. 

Manuscript submitted to ACM 

WMAD 

29 

- [101] Napat Karnchanachari, Dimitris Geromichalos, Kok Seang Tan, Nanxiang Li, Christopher Eriksen, Shakiba Yaghoubi, Noushin Mehdipour, Gianmarco Bernasconi, Whye Kit Fong, Yiluan Guo, et al. 2024. Towards learning-based planning: The nuPlan benchmark for real-world autonomous driving. _arXiv preprint arXiv:2403.04133_ (2024). 

- [102] Efstathios Karypidis, Ioannis Kakogeorgiou, Spyros Gidaris, and Nikos Komodakis. 2025. Advancing Semantic Future Prediction through Multimodal Visual Sequence Transformers. _arXiv preprint arXiv:2501.08303_ (2025). 

- [103] Bernhard Kerbl, Georgios Kopanas, Thomas Leimkühler, and George Drettakis. 2023. 3d gaussian splatting for real-time radiance field rendering. _ACM Transactions on Graphics_ 42, 4 (2023), 1–14. 

- [104] Oussama Khatib. 1986. Real-time obstacle avoidance for manipulators and mobile robots. In _Autonomous Robot Vehicles_ . Springer, 396–404. [105] O. Khatib and J. Le Maitre. 1978. Dynamic control of manipulators operating in a complex environment. In _Proc. 3rd CISM-IFToMM Symp. Theory Pract. Robots Manip._ , Vol. 267. 

- [106] Tarasha Khurana, Peiyun Hu, Achal Dave, Jason Ziglar, David Held, and Deva Ramanan. 2022. Differentiable raycasting for self-supervised occupancy forecasting. In _Proc. Eur. Conf. Comput. Vis._ Springer, 353–369. 

- [107] Tarasha Khurana, Peiyun Hu, David Held, and Deva Ramanan. 2023. Point cloud forecasting as a proxy for 4d occupancy forecasting. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 1116–1124. 

- [108] Seung Wook Kim, Jonah Philion, Antonio Torralba, and Sanja Fidler. 2021. Drivegan: Towards a controllable high-quality neural simulation. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 5820–5829. 

- [109] Daniel Krajzewicz, Jakob Erdmann, Michael Behrisch, and Laura Bieker. 2012. Recent development and applications of SUMO-Simulation of Urban MObility. _International journal on advances in systems and measurements_ 5, 3&4 (2012). 

- [110] James J Kuffner and Steven M LaValle. 2000. RRT-connect: An efficient approach to single-query path planning. In _Proc. IEEE Int. Conf. Robot. Autom._ , Vol. 2. IEEE, 995–1001. 

- [111] Yoshiaki Kuwata, Justin Teo, Gaston Fiore, Sertac Karaman, Emilio Frazzoli, and Jonathan P How. 2009. Real-time motion planning with applications to autonomous urban driving. _IEEE Trans. Control Syst. Technol._ 17, 5 (2009), 1105–1118. 

- [112] Steven LaValle. 1998. Rapidly-exploring random trees: A new tool for path planning. _Research Report 9811_ (1998). 

- [113] Stéphanie Lefevre, Ashwin Carvalho, and Francesco Borrelli. 2015. A learning-based framework for velocity control in autonomous driving. _IEEE Trans. Autom. Sci. Eng._ 13, 1 (2015), 32–42. 

- [114] Bohan Li, Jiazhe Guo, Hongsi Liu, Yingshuang Zou, Yikang Ding, Xiwu Chen, Hu Zhu, Feiyang Tan, Chi Zhang, Tiancai Wang, et al. 2024. UniScene: Unified Occupancy-centric Driving Scene Generation. _arXiv preprint arXiv:2412.05435_ (2024). 

- [115] Peidong Li and Dixiao Cui. 2025. Navigation-Guided Sparse Scene Representation for End-to-End Autonomous Driving. In _Proc. Int. Conf. Learn. Represent._ 

- [116] Peizheng Li, Shuxiao Ding, Xieyuanli Chen, Niklas Hanselmann, Marius Cordts, and Juergen Gall. 2023. PowerBEV: a powerful yet lightweight framework for instance prediction in bird’s-eye view. _arXiv preprint arXiv:2306.10761_ (2023). 

- [117] Qifeng Li, Xiaosong Jia, Shaobo Wang, and Junchi Yan. 2024. Think2Drive: Efficient Reinforcement Learning by Thinking with Latent World Model for Autonomous Driving (in CARLA-V2). In _Proc. Eur. Conf. Comput. Vis._ Springer, 142–158. 

- [118] Quanyi Li, Zhenghao Peng, Lan Feng, Qihang Zhang, Zhenghai Xue, and Bolei Zhou. 2022. Metadrive: Composing diverse driving scenarios for generalizable reinforcement learning. _IEEE Trans. Pattern Anal. Mach. Intell._ 45, 3 (2022), 3461–3475. 

- [119] Shilong Li. 2023. Research on the Application of Machine Learning in the Real Time Decision System of Autonomous Vehicles. _Front. Comput. Intell. Syst._ 5, 2 (2023). doi:10.54097/fcis.v5i2.12278 

- [120] Xiang Li, Pengfei Li, Yupeng Zheng, Wei Sun, Yan Wang, and Yilun Chen. 2025. Semi-Supervised Vision-Centric 3D Occupancy World Model for Autonomous Driving. In _Proc. Int. Conf. Learn. Represent._ 

- [121] Xinqing Li, Ruiqi Song, Qingyu Xie, Ye Wu, Nanxin Zeng, and Yunfeng Ai. 2025. SimWorld: A Unified Benchmark for Simulator-Conditioned Scene Generation via World Model. _arXiv preprint arXiv:2503.13952_ (2025). 

- [122] Xiaohui Li, Zhenping Sun, Dongpu Cao, Zhen He, and Qi Zhu. 2015. Real-time trajectory planning for autonomous urban driving: Framework, algorithms, and verifications. _IEEE/ASME Trans. Mechatronics_ 21, 2 (2015), 740–753. 

- [123] Xiaofan Li, Chenming Wu, Zhao Yang, Zhihao Xu, Dingkang Liang, Yumeng Zhang, Ji Wan, and Jun Wang. 2025. DriVerse: Navigation World Model for Driving Simulation via Multimodal Trajectory Prompting and Motion Alignment. In _ACM Int. Conf. Multimedia_ . 

- [124] Xiaofan Li, Yifu Zhang, and Xiaoqing Ye. 2024. DrivingDiffusion: Layout-Guided Multi-view Driving Scenarios Video Generation with Latent Diffusion Model. In _Proc. Eur. Conf. Comput. Vis._ Springer, 469–485. 

- [125] Yingyan Li, Lue Fan, Jiawei He, Yuqi Wang, Yuntao Chen, Zhaoxiang Zhang, and Tieniu Tan. 2025. Enhancing End-to-End Autonomous Driving with Latent World Model. In _Proc. Int. Conf. Learn. Represent._ 

- [126] Yuchen Li, Zixuan Li, Siyu Teng, Yu Zhang, Yuhang Zhou, Yuchang Zhu, Dongpu Cao, Bin Tian, Yunfeng Ai, Zhe Xuanyuan, et al. 2022. AutoMine: An unmanned mine dataset. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 21308–21317. 

- [127] Yingyan Li, Yuqi Wang, Yang Liu, Jiawei He, Lue Fan, and Zhaoxiang Zhang. 2025. End-to-End Driving with Online Trajectory Evaluation via BEV World Model. _arXiv preprint arXiv:2504.01941_ (2025). 

- [128] Zhiqi Li, Zhiding Yu, Shiyi Lan, Jiahan Li, Jan Kautz, Tong Lu, and Jose M Alvarez. 2024. Is ego status all you need for open-loop end-to-end autonomous driving?. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 14864–14873. 

Manuscript submitted to ACM 

T. Feng et al. 

30 

- [129] Ao Liang, Youquan Liu, Yu Yang, Dongyue Lu, Linfeng Li, Lingdong Kong, Huaici Zhao, and Wei Tsang Ooi. 2025. LiDARCrafter: Dynamic 4D World Modeling from LiDAR Sequences. _arXiv preprint arXiv:2508.03692_ (2025). 

- [130] Dingkang Liang, Dingyuan Zhang, Xin Zhou, Sifan Tu, Tianrui Feng, Xiaofan Li, Yumeng Zhang, Mingyang Du, Xiao Tan, and Xiang Bai. 2025. Seeing the Future, Perceiving the Future: A Unified Driving World Model for Future Generation and Perception. _arXiv preprint arXiv:2503.13587_ (2025). 

- [131] Yiyi Liao, Jun Xie, and Andreas Geiger. 2022. Kitti-360: A novel dataset and benchmarks for urban scene understanding in 2d and 3d. _IEEE Trans. Pattern Anal. Mach. Intell._ 45, 3 (2022), 3292–3310. 

- [132] Zhimin Liao, Ping Wei, Ruijie Zhang, Shuaijia Chen, Haoxuan Wang, and Ziyang Ren. 2025. I<sup>2</sup> -World: Intra-Inter Tokenization for Efficient Dynamic 4D Scene Forecasting. _arXiv preprint arXiv:2507.09144_ (2025). 

- [133] Liangkai Liu, Sidi Lu, Ren Zhong, Baofu Wu, Yongtao Yao, Qingyang Zhang, and Weisong Shi. 2021. Computing Systems for Autonomous Driving: State of the Art and Challenges. _IEEE Internet Things J._ 8, 8 (2021), 6469–6486. doi:10.1109/JIOT.2020.3043716 

- [134] Tianran Liu, Shengwen Zhao, and Nicholas Rhinehart. 2025. Towards foundational LiDAR world models with efficient latent flow matching. _arXiv preprint arXiv:2506.23434_ (2025). 

- [135] Xinhao Liu, Moonjun Gong, Qi Fang, Haoyu Xie, Yiming Li, Hang Zhao, and Chen Feng. 2024. Lidar-based 4d occupancy completion and forecasting. In _Proc. IEEE/RSJ Int. Conf. Intell. Robot. Syst._ IEEE, 11102–11109. 

- [136] Bing Lu, Hongwen He, Huilong Yu, Hong Wang, Guofa Li, Man Shi, and Dongpu Cao. 2020. Hybrid Path Planning Combining Potential Field with Sigmoid Curve for Autonomous Driving. _Sensors_ 20, 24 (2020), 7197. 

- [137] Chao Lu, Jianwei Gong, Chen Lv, Xin Chen, Dongpu Cao, and Yimin Chen. 2019. A personalized behavior learning system for human-like longitudinal speed control of autonomous vehicles. _Sensors_ 19, 17 (2019), 3672. 

- [138] Han Lu, Xiaosong Jia, Yichen Xie, Wenlong Liao, Xiaokang Yang, and Junchi Yan. 2024. ActiveAD: Planning-Oriented Active Learning for End-to-End Autonomous Driving. _arXiv preprint arXiv:2403.02877_ (2024). 

- [139] Yifan Lu, Xuanchi Ren, Jiawei Yang, Tianchang Shen, Zhangjie Wu, Jun Gao, Yue Wang, Siheng Chen, Mike Chen, Sanja Fidler, et al. 2025. Infinicube: Unbounded and controllable dynamic 3d driving scene generation with world-guided video models. In _Proc. IEEE Int. Conf. Comput. Vis._ 

- [140] Zhen Luo, Junyi Ma, Zijie Zhou, and Guangming Xiong. 2023. Pcpnet: An efficient and semantic-enhanced transformer network for point cloud prediction. _IEEE Robot. Autom. Lett._ 8, 7 (2023), 4267–4274. 

- [141] Enhui Ma, Lijun Zhou, Tao Tang, Zhan Zhang, Dong Han, Junpeng Jiang, Kun Zhan, Peng Jia, Xianpeng Lang, Haiyang Sun, et al. 2024. Unleashing Generalization of End-to-End Autonomous Driving with Controllable Long Video Generation. _arXiv preprint arXiv:2406.01349_ (2024). 

- [142] Junyi Ma, Xieyuanli Chen, Jiawei Huang, Jingyi Xu, Zhen Luo, Jintao Xu, Weihao Gu, Rui Ai, and Hesheng Wang. 2024. Cam4docc: Benchmark for camera-only 4d occupancy forecasting in autonomous driving applications. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 21486–21495. 

- [143] Reza Mahjourian, Jinkyu Kim, Yuning Chai, Mingxing Tan, Ben Sapp, and Dragomir Anguelov. 2022. Occupancy flow fields for motion forecasting in autonomous driving. _IEEE Robot. Autom. Lett._ 7, 2 (2022), 5639–5646. 

- [144] Sivabalan Manivasagam, Shenlong Wang, Kelvin Wong, Wenyuan Zeng, Mikita Sazanovich, Shuhan Tan, Bin Yang, Wei-Chiu Ma, and Raquel Urtasun. 2020. Lidarsim: Realistic lidar simulation by leveraging the real world. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 11167–11176. 

- [145] Matthew McNaughton, Chris Urmson, John M. Dolan, and Jin-Woo Lee. 2011. Motion planning for autonomous driving with a conformal spatiotemporal lattice. In _Proc. IEEE Int. Conf. Robot. Autom._ IEEE, 4889–4895. 

- [146] Benedikt Mersch, Xieyuanli Chen, Jens Behley, and Cyrill Stachniss. 2022. Self-supervised point cloud prediction using 3d spatio-temporal convolutional networks. In _Conf. Robot Learn._ PMLR, 1444–1454. 

- [147] Chen Min, Liang Xiao, Dawei Zhao, Yiming Nie, and Bin Dai. 2024. Occupancy-MAE: Self-supervised Pre-Training Large-Scale LiDAR Point Clouds with Masked Occupancy Autoencoders. _IEEE Trans. Intell. Veh._ 9, 7 (July 2024), 5150–5162. doi:10.1109/TIV.2023.3322409 

- [148] Chen Min, Dawei Zhao, Liang Xiao, Yiming Nie, and Bin Dai. 2023. Uniworld: Autonomous driving pre-training via world models. _arXiv preprint arXiv:2308.07234_ (2023). 

- [149] Chen Min, Dawei Zhao, Liang Xiao, Jian Zhao, Xinli Xu, Zheng Zhu, Lei Jin, Jianshu Li, Yulan Guo, Junliang Xing, et al. 2024. Driveworld: 4d pre-trained scene understanding via world models for autonomous driving. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 15522–15533. 

- [150] Sicheng Mo, Ziyang Leng, Leon Liu, Weizhen Wang, Honglin He, and Bolei Zhou. 2025. Dreamland: Controllable World Creation with Simulator and Generative Models. _arXiv preprint arXiv:2506.08006_ (2025). 

- [151] Michael Montemerlo, Jan Becker, Suhrid Bhat, Hendrik Dahlkamp, Dmitri Dolgov, Scott Ettinger, Dirk Haehnel, Tim Hilden, Gabe Hoffmann, Burkhard Huhnke, Doug Johnston, Stefan Klumpp, Dirk Langer, Anthony Levandowski, Jesse Levinson, Julien Marcil, David Orenstein, Johannes Paefgen, Isaac Penny, Anna Petrovskaya, Mike Pflueger, Ganymed Stanek, David Stavens, Antone Vogt, and Sebastian Thrun. 2008. Junior: The Stanford Entry in the Urban Challenge. _J. Field Robot._ 25, 9 (sep 2008), 569–597. 

- [152] Arian Mousakhan, Sudhanshu Mittal, Silvio Galesso, Karim Farid, and Thomas Brox. 2025. Orbis: Overcoming Challenges of Long-Horizon Prediction in Driving World Models. _arXiv preprint arXiv:2507.13162_ (2025). 

- [153] Sajjad Mozaffari, Omar Y Al-Jarrah, Mehrdad Dianati, Paul Jennings, and Alexandros Mouzakitis. 2020. Deep learning-based vehicle behavior prediction for autonomous driving applications: A review. _IEEE Trans. Intell. Transp. Syst._ (2020). 

- [154] Asen Nachkov, Danda Pani Paudel, Jan-Nico Zaech, Davide Scaramuzza, and Luc Van Gool. 2025. Dream to Drive: Model-Based Vehicle Control Using Analytic World Models. _arXiv preprint arXiv:2502.10012_ (2025). 

Manuscript submitted to ACM 

WMAD 

31 

- [155] Chaojun Ni, Guosheng Zhao, Xiaofeng Wang, Zheng Zhu, Wenkang Qin, Guan Huang, Chen Liu, Yuyin Chen, Yida Wang, Xueyang Zhang, et al. 2024. ReconDreamer: Crafting World Models for Driving Scene Reconstruction via Online Restoration. _arXiv preprint arXiv:2411.19548_ (2024). 

- [156] Jingcheng Ni, Yuxin Guo, Yichen Liu, Rui Chen, Lewei Lu, and Zehuan Wu. 2025. MaskGWM: A Generalizable Driving World Model with Video Mask Reconstruction. _arXiv preprint arXiv:2502.11663_ (2025). 

- [157] World Health Organization. 2019. _Global status report on road safety 2018_ . World Health Organization. 

- [158] Brian Paden, Michal Čáp, Sze Zheng Yong, Dmitry Yershov, and Emilio Frazzoli. 2016. A survey of motion planning and control techniques for self-driving urban vehicles. _IEEE Trans. Intell. Veh._ 1, 1 (2016), 33–55. 

- [159] Mingjie Pan, Jiaming Liu, Renrui Zhang, Peixiang Huang, Xiaoqi Li, Li Liu, and Shanghang Zhang. 2024. RenderOcc: Vision-Centric 3D Occupancy Prediction with 2D Rendering Supervision. In _Proc. IEEE Int. Conf. Robot. Autom._ 

- [160] Joshué Pérez Rastelli, Ray Lattarulo, and Fawzi Nashashibi. 2014. Dynamic Trajectory Generation Using Continuous-Curvature Algorithms for Door to Door Assistance Vehicles. In _Proc. IEEE Intell. Veh. Symp._ IEEE, Dearborn, MI, USA, 510–515. doi:10.1109/IVS.2014.6856526 

- [161] Tung Phan-Minh, Elena Corina Grigore, Freddy A Boulton, Oscar Beijbom, and Eric M Wolff. 2020. Covernet: Multimodal behavior prediction using trajectory sets. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 14074–14083. 

- [162] Dean A Pomerleau. 1989. _Alvinn: An autonomous land vehicle in a neural network_ . Technical Report. CARNEGIE-MELLON UNIV PITTSBURGH PA ARTIFICIAL INTELLIGENCE AND PSYCHOLOGY .... 

- [163] Anawat Pongpunwattana and Rolf Rysdyk. 2004. Real-Time Planning for Multiple Autonomous Vehicles in Dynamic Uncertain Environments. _J. Aerosp. Comput. Inf. Commun._ 1, 12 (Dec. 2004), 580–604. doi:10.2514/1.12919 

- [164] Alexander Popov, Alperen Degirmenci, David Wehr, Shashank Hegde, Ryan Oldja, Alexey Kamenev, Bertrand Douillard, David Nistér, Urs Muller, Ruchi Bhargava, et al. 2024. Mitigating covariate shift in imitation learning for autonomous vehicles using latent space generative world models. _arXiv preprint arXiv:2409.16663_ (2024). 

- [165] Aditya Prakash, Kashyap Chitta, and Andreas Geiger. 2021. Multi-modal fusion transformer for end-to-end autonomous driving. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 

- [166] Lilin Qian, Xin Xu, Yujun Zeng, and J. Huang. 2019. Deep, Consistent Behavioral Decision Making with Planning Features for Autonomous Vehicles. _Electronics_ (2019). doi:10.3390/electronics8121492 

- [167] Yansong Qu, Zilin Huang, Zihao Sheng, Jiancong Chen, Sikai Chen, and Samuel Labi. 2025. VL-SAFE: Vision-Language Guided Safety-Aware Reinforcement Learning with World Models for Autonomous Driving. _arXiv preprint arXiv:2505.16377_ (2025). 

- [168] Jing Ren, Kenneth A. McIsaac, and Rajnikant V. Patel. 2006. Modified Newton’s method applied to potential field-based navigation for mobile robots. _IEEE Trans. Robot._ 22, 2 (2006), 384–391. 

- [169] Nicholas Rhinehart, Rowan McAllister, Kris Kitani, and Sergey Levine. 2019. Precog: Prediction conditioned on goals in visual multi-agent settings. In _Proc. IEEE Int. Conf. Comput. Vis._ 2821–2830. 

- [170] Charles Richter and Nicholas Roy. 2017. Safe visual navigation via deep learning and novelty detection. (2017). 

- [171] Lloyd Russell, Anthony Hu, Lorenzo Bertoni, George Fedoseev, Jamie Shotton, Elahe Arani, and Gianluca Corrado. 2025. Gaia-2: A controllable multi-view generative world model for autonomous driving. _arXiv preprint arXiv:2503.20523_ (2025). 

- [172] Abbas Sadat, Sergio Casas, Mengye Ren, Xinyu Wu, Pranaab Dhawan, and Raquel Urtasun. 2020. Perceive, predict, and plan: Safe motion planning through interpretable semantic representations. In _Proc. Eur. Conf. Comput. Vis._ Springer, 414–430. 

- [173] Ahmad El Sallab, Ibrahim Sobh, Mohamed Zahran, and Nader Essam. 2019. Lidar sensor modeling and data augmentation with gans for autonomous driving. _arXiv preprint arXiv:1905.07290_ (2019). 

- [174] Marcel Schreiber, Stefan Hoermann, and Klaus Dietmayer. 2019. Long-term occupancy grid prediction using recurrent neural networks. In _Proc. IEEE Int. Conf. Robot. Autom._ IEEE, 9299–9305. 

- [175] Wilko Schwarting, Javier Alonso-Mora, and Daniela Rus. 2018. Planning and Decision-Making for Autonomous Vehicles. _Annu. Rev. Control Robot. Auton. Syst._ 1 (2018), 187–210. doi:10.1146/annurev-control-060117-105157 

- [176] Yunxiao Shi, Hong Cai, Amin Ansari, and Fatih Porikli. 2025. H3o: Hyper-efficient 3d occupancy prediction with heterogeneous supervision. _arXiv preprint arXiv:2503.04059_ (2025). 

- [177] Yining Shi, Kun Jiang, Qiang Meng, Ke Wang, Jiabao Wang, Wenchao Sun, Tuopu Wen, Mengmeng Yang, and Diange Yang. 2025. COME: Adding Scene-Centric Forecasting Control to Occupancy World Model. _arXiv preprint arXiv:2506.13260_ (2025). 

- [178] Shiva Sreeram, Tsun-Hsuan Wang, Alaa Maalouf, Guy Rosman, Sertac Karaman, and Daniela Rus. 2024. Probing Multimodal LLMs as World Models for Driving. _arXiv preprint arXiv:2405.05956_ (2024). 

- [179] Pei Sun, Henrik Kretzschmar, Xerxes Dotiwalla, Aurelien Chouard, Vijaysai Patnaik, Paul Tsui, James Guo, Yin Zhou, Yuning Chai, Benjamin Caine, et al. 2020. Scalability in perception for autonomous driving: Waymo open dataset. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 2446–2454. 

- [180] Simon Suo, Sebastian Regalado, Sergio Casas, and Raquel Urtasun. 2021. Trafficsim: Learning to simulate realistic multi-agent behaviors. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 10400–10409. 

- [181] Alexander Swerdlow, Runsheng Xu, and Bolei Zhou. 2024. Street-View Image Generation from a Bird’s-Eye View Layout. _IEEE Robot. Autom. Lett._ (2024), 1–8. doi:10.1109/LRA.2024.3424866 early access. 

- [182] Shuhan Tan, Boris Ivanovic, Xinshuo Weng, Marco Pavone, and Philipp Krähenbühl. 2023. Language Conditioned Traffic Generation. In _Conf. Robot Learn. (Proceedings of Machine Learning Research, Vol. 229)_ , Jie Tan, Marc Toussaint, and Kourosh Darvish (Eds.). PMLR, Atlanta, GA, USA, 2714–2752. arXiv:2307.07947 https://proceedings.mlr.press/v229/tan23a.html 

Manuscript submitted to ACM 

T. Feng et al. 

32 

- [183] Shuhan Tan, John Lambert, Hong Jeon, Sakshum Kulshrestha, Yijing Bai, Jing Luo, Dragomir Anguelov, Mingxing Tan, and Chiyu Max Jiang. 2025. SceneDiffuser++: City-Scale Traffic Simulation via a Generative World Model. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 1570–1580. 

- [184] Xiaoyu Tian, Tao Jiang, Longfei Yun, Yucheng Mao, Huitong Yang, Yue Wang, Yilun Wang, and Hang Zhao. 2024. Occ3d: A large-scale 3d occupancy prediction benchmark for autonomous driving. In _Proc. Adv. Neural Inf. Process. Syst._ , Vol. 36. 

- [185] Maneekwan Toyungyernsub, Esen Yel, Jiachen Li, and Mykel J Kochenderfer. 2022. Dynamics-aware spatiotemporal occupancy prediction in urban environments. In _Proc. IEEE/RSJ Int. Conf. Intell. Robot. Syst._ IEEE, 10836–10841. 

- [186] Martin Treiber, Ansgar Hennecke, and Dirk Helbing. 2000. Congested traffic states in empirical observations and microscopic simulations. _Phys. Rev. E_ 62, 2 (Aug. 2000), 1805–1824. doi:10.1103/PhysRevE.62.1805 

- [187] Charlott Vallon, Ziya Ercan, Ashwin Carvalho, and Francesco Borrelli. 2017. A machine learning approach for personalized autonomous lane change initiation and control. In _Proc. IEEE Intell. Veh. Symp._ IEEE, 1590–1595. 

- [188] Arun Balajee Vasudevan, Neehar Peri, Jeff Schneider, and Deva Ramanan. 2024. Planning with Adaptive World Models for Autonomous Driving. _arXiv preprint arXiv:2406.10714_ (2024). 

- [189] Haiguang Wang, Daqi Liu, Hongwei Xie, Haisong Liu, Enhui Ma, Kaicheng Yu, Limin Wang, and Bing Wang. 2025. MiLA: Multi-view Intensivefidelity Long-term Video Generation World Model for Autonomous Driving. _arXiv preprint arXiv:2503.15875_ (2025). 

- [190] Hang Wang, Xin Ye, Feng Tao, Chenbin Pan, Abhirup Mallik, Burhaneddin Yaman, Liu Ren, and Junshan Zhang. 2025. AdaWM: Adaptive World Model based Planning for Autonomous Driving. In _Proc. Int. Conf. Learn. Represent._ 

- [191] Jiamin Wang, Yichen Yao, Xiang Feng, Hang Wu, Yaming Wang, Qingqiu Huang, Yuexin Ma, and Xinge Zhu. 2025. STAGE: A Stream-Centric Generative World Model for Long-Horizon Driving-Scene Simulation. _arXiv preprint arXiv:2506.13138_ (2025). 

- [192] Lening Wang, Wenzhao Zheng, Yilong Ren, Han Jiang, Zhiyong Cui, Haiyang Yu, and Jiwen Lu. 2024. OccSora: 4D Occupancy Generation Models as World Simulators for Autonomous Driving. _arXiv preprint arXiv:2405.20337_ (2024). 

- [193] Pengwei Wang, Song Gao, Liang Li, Shuo Cheng, and Hai xia Zhao. 2020. Research on driving behavior decision making system of autonomous driving vehicle based on benefit evaluation model. _Arch. Transp._ 53, 1 (2020), 21–36. doi:10.5604/01.3001.0014.1740 

- [194] Xiaodong Wang, Zhirong Wu, and Peixi Peng. 2025. LongDWM: Cross-Granularity Distillation for Building a Long-Term Driving World Model. _arXiv preprint arXiv:2506.01546_ (2025). 

- [195] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Jiagang Zhu, and Jiwen Lu. 2024. DriveDreamer: Towards Real-World-Drive World Models for Autonomous Driving. In _Proc. Eur. Conf. Comput. Vis._ Springer, 55–72. 

- [196] Xiaofeng Wang, Zheng Zhu, Guan Huang, Boyuan Wang, Xinze Chen, and Jiwen Lu. 2024. Worlddreamer: Towards general world models for video generation via predicting masked tokens. _arXiv preprint arXiv:2401.09985_ (2024). 

- [197] Xiaofeng Wang, Zheng Zhu, Wenbo Xu, Yunpeng Zhang, Yi Wei, Xu Chi, Yun Ye, Dalong Du, Jiwen Lu, and Xingang Wang. 2023. Openoccupancy: A large scale benchmark for surrounding semantic occupancy perception. In _Proc. IEEE Int. Conf. Comput. Vis._ 

- [198] Yuqi Wang, Jiawei He, Lue Fan, Hongxin Li, Yuntao Chen, and Zhaoxiang Zhang. 2024. Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 14749–14759. 

- [199] Julong Wei, Shanshuai Yuan, Pengfei Li, Qingda Hu, Zhongxue Gan, and Wenchao Ding. 2024. Occllama: An occupancy-language-action generative world model for autonomous driving. _arXiv preprint arXiv:2409.03272_ (2024). 

- [200] Xinshuo Weng, Junyu Nan, Kuan-Hui Lee, Rowan McAllister, Adrien Gaidon, Nicholas Rhinehart, and Kris M Kitani. 2022. S2net: Stochastic sequential pointcloud forecasting. In _Proc. Eur. Conf. Comput. Vis._ Springer, 549–564. 

- [201] Xinshuo Weng, Jianren Wang, Sergey Levine, Kris Kitani, and Nicholas Rhinehart. 2021. Inverting the pose forecasting pipeline with SPF2: Sequential pointcloud forecasting for sequential pose forecasting. In _Conf. Robot Learn._ PMLR, 11–20. 

- [202] Licheng Wenl, Daocheng Fu, Song Mao, Pinlong Cai, Min Dou, Yikang Li, and Yu Qiao. 2023. LimSim: A long-term interactive multi-scenario traffic simulator. In _Proc. IEEE Int. Conf. Intell. Transp. Syst._ IEEE, 1255–1262. 

- [203] Moritz Werling, Sören Kammel, Julius Ziegler, and Lutz Gröll. 2012. Optimal trajectories for time-critical street scenarios using discretized terminal manifolds. _Int. J. Robot. Res._ 31, 3 (2012), 346–359. 

- [204] Benjamin Wilson, William Qi, Tanmay Agarwal, John Lambert, Jagjeet Singh, Siddhesh Khandelwal, Bowen Pan, Ratnesh Kumar, Andrew Hartnett, Jhony Kaesemodel Pontes, et al. 2023. Argoverse 2: Next generation datasets for self-driving perception and forecasting. _arXiv preprint arXiv:2301.00493_ (2023). 

- [205] Joey Wilson, Jingyu Song, Yuewei Fu, Arthur Zhang, Andrew Capodieci, Paramsothy Jayakumar, Kira Barton, and Maani Ghaffari. 2022. MotionSC: Data set and network for real-time semantic mapping in dynamic environments. _IEEE Robot. Autom. Lett._ 7, 3 (2022), 8439–8446. 

- [206] Wei Wu, Xiaoxin Feng, Ziyan Gao, and Yuheng Kan. 2024. Smart: Scalable multi-agent real-time motion generation via next-token prediction. In _Proc. Adv. Neural Inf. Process. Syst._ , Vol. 37. 114048–114071. 

- [207] Zehuan Wu, Jingcheng Ni, Xiaodong Wang, Yuxin Guo, Rui Chen, Lewei Lu, Jifeng Dai, and Yuwen Xiong. 2024. HoloDrive: Holistic 2D-3D Multi-Modal Street Scene Generation for Autonomous Driving. _arXiv preprint arXiv:2412.01407_ (2024). 

- [208] Yuwen Xiong, Wei-Chiu Ma, Jingkang Wang, and Raquel Urtasun. 2023. Learning compact representations for lidar completion and generation. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 1074–1083. 

- [209] Haoran Xu, Peixi Peng, Guang Tan, Yiqian Chang, Yisen Zhao, and Yonghong Tian. 2025. Temporal Triplane Transformers as Occupancy World Models. _arXiv preprint arXiv:2503.07338_ (2025). 

Manuscript submitted to ACM 

WMAD 

33 

- [210] Tianshuo Xu, Hao Lu, Xu Yan, Yingjie Cai, Bingbing Liu, and Yingcong Chen. 2025. Occ-LLM: Enhancing Autonomous Driving with OccupancyBased Large Language Models. In _Proc. IEEE Int. Conf. Robot. Autom._ 

- [211] Guohang Yan, Jiahao Pi, Jianfei Guo, Zhaotong Luo, Min Dou, Nianchen Deng, Qiusheng Huang, Daocheng Fu, Licheng Wen, Pinlong Cai, et al. 2024. OASim: an Open and Adaptive Simulator based on Neural Rendering for Autonomous Driving. _arXiv preprint arXiv:2402.03830_ (2024). 

- [212] Tianyi Yan, Dongming Wu, Wencheng Han, Junpeng Jiang, Xia Zhou, Kun Zhan, Cheng-zhong Xu, and Jianbing Shen. 2025. DrivingSphere: Building a High-fidelity 4D World for Closed-loop Simulation. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 

- [213] Ziyang Yan, Wenzhen Dong, Yihua Shao, Yuhang Lu, Liu Haiyang, Jingwen Liu, Haozhe Wang, Zhe Wang, Yan Wang, Fabio Remondino, et al. 2025. Renderworld: World model with self-supervised 3d label. In _Proc. IEEE Int. Conf. Robot. Autom._ 

- [214] Honghui Yang, Sha Zhang, Di Huang, Xiaoyang Wu, Haoyi Zhu, Tong He, Shixiang Tang, Hengshuang Zhao, Qibo Qiu, Binbin Lin, et al. 2024. Unipad: A universal pre-training paradigm for autonomous driving. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 15238–15250. 

- [215] Jiazhi Yang, Kashyap Chitta, Shenyuan Gao, Long Chen, Yuqian Shao, Xiaosong Jia, Hongyang Li, Andreas Geiger, Xiangyu Yue, and Li Chen. 2025. ReSim: Reliable World Simulation for Autonomous Driving. _arXiv preprint arXiv:2506.09981_ (2025). 

- [216] Jiazhi Yang, Shenyuan Gao, Yihang Qiu, Li Chen, Tianyu Li, Bo Dai, Kashyap Chitta, Penghao Wu, Jia Zeng, Ping Luo, et al. 2024. Generalized predictive model for autonomous driving. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 14662–14672. 

- [217] Kairui Yang, Enhui Ma, Jibin Peng, Qing Guo, Di Lin, and Kaicheng Yu. 2023. Bevcontrol: Accurately controlling street-view elements with multi-perspective consistency via bev sketch layout. _arXiv preprint arXiv:2308.01661_ (2023). 

- [218] Pengxuan Yang, Yupeng Zheng, Qichao Zhang, Kefei Zhu, Zebin Xing, Qiao Lin, Yun-Fu Liu, Zhiguo Su, and Dongbin Zhao. 2025. UncAD: Towards Safe End-to-end Autonomous Driving via Online Map Uncertainty. In _Proc. IEEE Int. Conf. Robot. Autom._ 

- [219] Xuemeng Yang, Licheng Wen, Yukai Ma, Jianbiao Mei, Xin Li, Tiantian Wei, Wenjie Lei, Daocheng Fu, Pinlong Cai, Min Dou, et al. 2024. Drivearena: A closed-loop generative simulation platform for autonomous driving. _arXiv preprint arXiv:2408.00415_ (2024). 

- [220] Yu Yang, Jianbiao Mei, Yukai Ma, Siliang Du, Wenqing Chen, Yijie Qian, Yuxiang Feng, and Yong Liu. 2025. Driving in the occupancy world: Vision-centric 4d occupancy forecasting and planning via world models for autonomous driving. In _AAAI Conf. Artif. Intell._ 9327–9335. 

- [221] Zetong Yang, Li Chen, Yanan Sun, and Hongyang Li. 2024. Visual point cloud forecasting enables scalable autonomous driving. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 14673–14684. 

- [222] Ze Yang, Yun Chen, Jingkang Wang, Sivabalan Manivasagam, Wei-Chiu Ma, Anqi Joyce Yang, and Raquel Urtasun. 2023. Unisim: A neural closed-loop sensor simulator. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 1389–1399. 

- [223] Zhuoran Yang, Xi Guo, Chenjing Ding, Chiyu Wang, and Wei Wu. 2024. Pysical Informed Driving World Model. _arXiv preprint arXiv:2412.08410_ (2024). 

- [224] Zhenjie Yang, Xiaosong Jia, Qifeng Li, Xue Yang, Maoqing Yao, and Junchi Yan. 2025. Raw2Drive: Reinforcement learning with aligned world models for end-to-end autonomous driving (in carla v2). _arXiv preprint arXiv:2505.16394_ (2025). 

- [225] Shuang Zeng, Xinyuan Chang, Mengwei Xie, Xinran Liu, Yifan Bai, Zheng Pan, Mu Xu, and Xing Wei. 2025. FutureSightDrive: Thinking Visually with Spatio-Temporal CoT for Autonomous Driving. _arXiv preprint arXiv:2505.17685_ (2025). 

- [226] Wenyuan Zeng, Wenjie Luo, Simon Suo, Abbas Sadat, Bin Yang, Sergio Casas, and Raquel Urtasun. 2019. End-to-end interpretable neural motion planner. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 8660–8669. 

- [227] Wenyuan Zeng, Shenlong Wang, Renjie Liao, Yun Chen, Bin Yang, and Raquel Urtasun. 2020. Dsdnet: Deep structured self-driving network. In _Proc. Eur. Conf. Comput. Vis._ 

- [228] Chubin Zhang, Juncheng Yan, Yi Wei, Jiaxin Li, Li Liu, Yansong Tang, Yueqi Duan, and Jiwen Lu. 2023. Occnerf: Self-supervised multi-camera occupancy prediction with neural radiance fields. _arXiv preprint arXiv:2312.09243_ (2023). 

- [229] Haiming Zhang, Ying Xue, Xu Yan, Jiacheng Zhang, Weichao Qiu, Dongfeng Bai, Bingbing Liu, Shuguang Cui, and Zhen Li. 2024. An Efficient Occupancy World Model via Decoupled Dynamic Flow and Image-assisted Training. _arXiv preprint arXiv:2412.13772_ (2024). 

- [230] Junge Zhang, Feihu Zhang, Shaochen Kuang, and Li Zhang. 2024. Nerf-lidar: Generating realistic lidar point clouds with neural radiance fields. In _AAAI Conf. Artif. Intell._ , Vol. 38. 7178–7186. 

- [231] Kaiwen Zhang, Zhenyu Tang, Xiaotao Hu, Xingang Pan, Xiaoyang Guo, Yuan Liu, Jingwei Huang, Li Yuan, Qian Zhang, Xiao-Xiao Long, et al. 2025. Epona: Autoregressive Diffusion World Model for Autonomous Driving. In _Proc. IEEE Int. Conf. Comput. Vis._ 

- [232] Lunjun Zhang, Yuwen Xiong, Ze Yang, Sergio Casas, Rui Hu, and Raquel Urtasun. 2023. Learning unsupervised world models for autonomous driving via discrete diffusion. _arXiv preprint arXiv:2311.01017_ (2023). 

- [233] Lunjun Zhang, Yuwen Xiong, Ze Yang, Sergio Casas, Rui Hu, and Raquel Urtasun. 2024. Copilot4D: Learning Unsupervised World Models for Autonomous Driving via Discrete Diffusion. In _Proc. Int. Conf. Learn. Represent._ 

- [234] Qichao Zhang, Yinfeng Gao, Yikang Zhang, Youtian Guo, Dawei Ding, Yunpeng Wang, Peng Sun, and Dongbin Zhao. 2022. Trajgen: Generating realistic and diverse trajectories with reactive and feasible agent behaviors for autonomous driving. _IEEE Trans. Intell. Transp. Syst._ 23, 12 (2022), 24474–24487. 

- [235] Yumeng Zhang, Shi Gong, Kaixin Xiong, Xiaoqing Ye, Xiao Tan, Fan Wang, Jizhou Huang, Hua Wu, and Haifeng Wang. 2024. Bevworld: A multimodal world model for autonomous driving via unified bev latent space. _arXiv preprint arXiv:2407.05679_ (2024). 

- [236] Yanan Zhang, Jinqing Zhang, Zengran Wang, Junhao Xu, and Di Huang. 2024. Vision-based 3D occupancy prediction in autonomous driving: a review and outlook. _arXiv preprint arXiv:2405.02595_ (2024). 

Manuscript submitted to ACM 

T. Feng et al. 

34 

- [237] Zhejun Zhang, Alexander Liniger, Dengxin Dai, Fisher Yu, and Luc Van Gool. 2023. Trafficbots: Towards world models for autonomous driving simulation and motion prediction. In _Proc. IEEE Int. Conf. Robot. Autom._ IEEE, 1522–1529. 

- [238] Guosheng Zhao, Chaojun Ni, Xiaofeng Wang, Zheng Zhu, Xueyang Zhang, Yida Wang, Guan Huang, Xinze Chen, Boyuan Wang, Youyi Zhang, et al. 2025. Drivedreamer4d: World models are effective data machines for 4d driving scene representation. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 

- [239] Guosheng Zhao, Xiaofeng Wang, Zheng Zhu, Xinze Chen, Guan Huang, Xiaoyi Bao, and Xingang Wang. 2025. Drivedreamer-2: Llm-enhanced world models for diverse driving video generation. In _AAAI Conf. Artif. Intell._ , Vol. 39. 10412–10420. 

- [240] Jianbo Zhao, Jiaheng Zhuang, Qibin Zhou, Taiyu Ban, Ziyao Xu, Hangning Zhou, Junhe Wang, Guoan Wang, Zhiheng Li, and Bin Li. 2024. Kigras: Kinematic-driven generative model for realistic agent simulation. _IEEE Robot. Autom. Lett._ (2024). 

- [241] Wenzhao Zheng, Weiliang Chen, Yuanhui Huang, Borui Zhang, Yueqi Duan, and Jiwen Lu. 2025. Occworld: Learning a 3d occupancy world model for autonomous driving. In _Proc. Eur. Conf. Comput. Vis._ Springer, 55–72. 

- [242] Wenzhao Zheng, Ruiqi Song, Xianda Guo, Chenming Zhang, and Long Chen. 2025. Genad: Generative end-to-end autonomous driving. In _Proc. Eur. Conf. Comput. Vis._ Springer, 87–104. 

- [243] Wenzhao Zheng, Zetian Xia, Yuanhui Huang, Sicheng Zuo, Jie Zhou, and Jiwen Lu. 2024. Doe-1: Closed-loop autonomous driving with large world model. _arXiv preprint arXiv:2412.09627_ (2024). 

- [244] Yupeng Zheng, Pengxuan Yang, Zebin Xing, Qichao Zhang, Yuhang Zheng, Yinfeng Gao, Pengfei Li, Teng Zhang, Zhongpu Xia, Peng Jia, et al. 2025. World4Drive: End-to-End Autonomous Driving via Intention-aware Physical Latent World Model. In _Proc. IEEE Int. Conf. Comput. Vis._ 

- [245] Chengmin Zhou, Bingding Huang, and Pasi Fränti. 2022. A review of motion planning algorithms for intelligent robots. _J. Intell. Manuf._ 33, 2 (2022), 387–424. doi:10.1007/s10845-021-01867-z 

- [246] Xin Zhou, Dingkang Liang, Sifan Tu, Xiwu Chen, Yikang Ding, Dingyuan Zhang, Feiyang Tan, Hengshuang Zhao, and Xiang Bai. 2025. HERMES: A Unified Self-Driving World Model for Simultaneous 3D Scene Understanding and Generation. In _Proc. IEEE Int. Conf. Comput. Vis._ 

- [247] Yunsong Zhou, Michael Simon, Zhenghao Mark Peng, Sicheng Mo, Hongzi Zhu, Minyi Guo, and Bolei Zhou. 2024. Simgen: Simulator-conditioned driving scene generation. In _Proc. Adv. Neural Inf. Process. Syst._ , Vol. 37. 48838–48874. 

- [248] Haoran Zhu, Zhenyuan Dong, Kristi Topollai, and Anna Choromanska. 2025. AD-L-JEPA: Self-Supervised Spatial World Models with Joint Embedding Predictive Architecture for Autonomous Driving with LiDAR Data. _arXiv preprint arXiv:2501.04969_ (2025). 

- [249] Jian Zhu, Zhengyu Jia, Tian Gao, Jiaxin Deng, Shidi Li, Fu Liu, Peng Jia, Xianpeng Lang, and Xiaolong Sun. 2025. Other Vehicle Trajectories Are Also Needed: A Driving World Model Unifies Ego-Other Vehicle Trajectories in Video Latant Space. _arXiv preprint arXiv:2503.09215_ (2025). 

- [250] Zheng Zhu, Xiaofeng Wang, Wangbo Zhao, Chen Min, Nianchen Deng, Min Dou, Yuqi Wang, Botian Shi, Kai Wang, Chi Zhang, et al. 2024. Is sora a world simulator? a comprehensive survey on general world models and beyond. _arXiv preprint arXiv:2405.03520_ (2024). 

- [251] Julius Ziegler and Christoph Stiller. 2009. Spatiotemporal state lattices for fast trajectory planning in dynamic on-road driving scenarios. In _Proc. IEEE/RSJ Int. Conf. Intell. Robot. Syst._ IEEE, 1879–1884. 

- [252] Sicheng Zuo, Wenzhao Zheng, Yuanhui Huang, Jie Zhou, and Jiwen Lu. 2025. GaussianWorld: Gaussian World Model for Streaming 3D Occupancy Prediction. In _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ 

- [253] Vlas Zyrianov, Xiyue Zhu, and Shenlong Wang. 2022. Learning to generate realistic lidar point clouds. In _Proc. Eur. Conf. Comput. Vis._ Springer, 17–35. 

Received 7 September 2025 

Manuscript submitted to ACM 

