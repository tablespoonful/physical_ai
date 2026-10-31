---
title: "From Human Videos to Robot Manipulation: A Survey on Scalable Vision-Language-Action Learning with Human-Centric Data"
date: "2026-05-18"
authors: "Zhiyuan Feng; Qixiu Li; Huizhi Liang; Rushuai Yang; Yichao Shen; Zhiying Du"
url: https://arxiv.org/abs/2606.00054
pdf: https://arxiv.org/pdf/2606.00054
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.00054)** / [論文ページ](https://arxiv.org/abs/2606.00054)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **From Human Videos to Robot Manipulation: A Survey on Scalable Vision-Language-Action Learning with Human-Centric Data** 

**Zhiyuan Feng**<sup>1</sup><sup>_,_5</sup><sup>_∗_</sup> **Qixiu Li**<sup>1</sup><sup>_,_5</sup><sup>_∗_</sup> **Huizhi Liang**<sup>1</sup><sup>_,_5</sup><sup>_∗_</sup> **Rushuai Yang**<sup>2</sup><sup>_,_5</sup><sup>_∗_</sup> **Yichao Shen**<sup>3</sup><sup>_,_5</sup><sup>_∗_</sup> **Zhiying Du**<sup>4</sup><sup>_,_5</sup><sup>_∗_</sup> **Zhaowei Zhang**<sup>5</sup><sup>_,_6</sup><sup>_∗_</sup> **Yu Deng**<sup>5</sup><sup>_†_</sup> **Li Zhao**<sup>5</sup> **Hao Zhao**<sup>1</sup> **Zongqing Lu**<sup>6</sup> 

**Oier Mees**<sup>7</sup> **Marc Pollefeys**<sup>7</sup> **Jiaolong Yang**<sup>5</sup><sup>_†_</sup> **Baining Guo**<sup>5</sup> 

1Tsinghua University 2HKUST 3Xi’an Jiaotong University 4Fudan University 

6Peking University 7Microsoft Zurich 

5Microsoft Research Asia 

� Repo 

� Project Page 

## **Abstract** 

Recent progress in generalizable embodied control has been driven by large-scale pretraining of Vision–Language–Action (VLA) models. However, most existing approaches rely on large collections of robot demonstrations, which are costly to obtain and tightly coupled to specific embodiments. Human videos, by contrast, are abundant and capture rich interactions, providing diverse semantic and physical cues for real-world manipulation. Yet, embodiment differences and the frequent absence of task-aligned annotations make their direct use in VLA models challenging. This survey provides a unified view of how human videos are transformed into effective knowledge for VLA models. We categorize existing approaches into four classes based on the action-related information they derive: (i) latent action representations that encode inter-frame changes; (ii) predictive world models that forecast future frames; (iii) explicit 2D supervision that extracts image-plane cues; and (iv) explicit 3D reconstruction that recovers geometry or motion. Beyond this taxonomy, we highlight three key open challenges in this area: structuring unstructured videos into trainingready episodes, grounding video-derived supervision into robot-executable actions under embodiment and viewpoint heterogeneity, and designing evaluation protocols that better predict realworld deployment performance and transfer efficiency, thereby informing future research directions. A curated list of papers and resources is available at https://github.com/AaronFengZY/ HumanCentricToVLA-Survey. 

## **1 Introduction** 

Embodied robotic tasks require agents to perceive the world, interpret instructions, and produce temporally coherent actions under physical constraints. Recent progress in VLA 

- *Work done during internship at Microsoft Research Asia. 

> †Corresponding authors. 


Figure 1: **Overview of scalable representation bridges for VLA models.** To leverage internet-scale human video data (top), existing methods bridge the embodiment gap via four routes: **Latent Action Abstraction** , **Predictive World Modeling** , **Explicit 2D Cues** , and **Explicit 3D Structure** . These representations transform diverse human videos into action-relevant learning signals, enabling VLA models to generate executable robot actions from image observations and language instructions (bottom). 

models suggests that large-scale multimodal pretraining can yield increasingly generalizable robotic policies, echoing the “foundation model” paradigm in language and vision [14, 38, 10, 9]. However, scaling VLA models is bottlenecked by the availability of grounded robot control data: robot demonstrations provide grounded control signals but are costly, safety-constrained, and strongly tied to a specific embodiment, sensor suite, and control frequency. Even with recent efforts to scale robot data [54, 65, 37, 2], robot-only 

datasets still under-represent long-horizon task structure, rare failure modes, and the distribution shifts in objects and environments encountered at deployment, which limits the robustness and generalization of VLA policies. 

To address this bottleneck, we turn to _human-centric data_ as a scalable complement to robot demonstrations. In this survey, we are particularly interested in the visually instantiated subset of human-centric data, namely _human videos_ . Compared to robot demonstrations, human videos are available at vastly larger scale—ranging from instructional videos sourced from platforms like YouTube and curated into datasets such as HowTo100M [51] to diverse activities captured via lightweight wearable devices [30, 31]. Beyond quantity, these resources provide rich semantic and physical cues relevant to embodied learning, such as egocentric object manipulations [44, 24], multi-view procedural assemblies [59], and controlled interactions with commonsense physics [29]. However, human videos are not “action data” for robots, they lack aligned, robot-executable action labels and proprioceptive context, and human motion does not directly map to robot kinematics and control interface. This challenge motivates the central inquiry of this survey: _when human videos enter a VLA training pipeline, what type of information do they become, and how does that information interface with policy learning?_ 

To bridge the gap between passive human observation and active robot control, the core challenge lies in translating the rich interaction knowledge embedded in human videos into action-relevant representations compatible with robotic policy learning. In this survey, we systematize this rapidly evolving field by categorizing methods based on the **nature of the constructed representations** along the processing pipeline. From this perspective, as illustrated in Figure 1, we identify four distinct routes: (i) **Latent Action Abstraction** , which circumvents explicit alignment by encoding inter-frame changes or intents into discrete codes or continuous embeddings [74, 19]; (ii) **Predictive World Modeling** , which uses video as a source of predictive learning signal to forecast future outcomes and distill these representations into policies [69, 6]; (iii) **Explicit 2D Cues** , which extract interpretable image-plane signals—such as point tracks, masks, or flow—using off-the-shelf vision tools [68, 72, 61]; and (iv) **Explicit 3D Structure** , which recovers 3D structure (poses/trajectories) to retarget motion into robot-compatible action spaces [73, 47]. This taxonomy highlights the diverse _representation bridges_ researchers build to convert passive video observations into active control signals. 

Building on this taxonomy, our survey makes three contributions: 

1. **Signal-centric taxonomy.** We introduce a pipelinebased taxonomy of _representation bridges_ that transform human videos into action-relevant representations for VLA learning, and compare the four routes—latent actions, predictive world models, explicit 2D cues, and explicit 3D structure—in terms of their representation form, scalability, and grounding requirements. 

2. **Dataset map and available signals.** We systematize representative human-video datasets along two axes— 

the availability of explicit geometric/3D signals and scripted vs. in-the-wild collection—and summarize how different supervision affordances (RGB-only vs. 2D/3D signals) support different transfer pipelines. 

3. **Challenges at three interfaces.** We distill open problems at three critical interfaces in the human-video-torobot pipeline: scalable episodization of unstructured videos, heterogeneity-aware grounding under embodiment/viewpoint mismatch, and deployment-predictive evaluation of transfer efficiency. 

## **2 Background** 

VLA learning addresses the challenge of mapping multimodal observations to executable actions for embodied agents. At each time step _t_ , the agent receives a current visual observation _ot_ , a proprioceptive state _st_ capturing lowdimensional robot state, such as joint configurations, gripper status, or end-effector pose, and a language instruction _l_ . Modern VLA policies typically adopt a sequence-modeling formulation that conditions on the history of observations and states and predicts a chunk of future actions _at_ : _t_ + _H_ over a horizon _H_ , promoting temporal consistency. This process is commonly formulated as maximum-likelihood imitation learning over a dataset of robot trajectories _D_ robot, where each trajectory _τ_ contains aligned sequences ( _ot, st, l, at_ )<sup>_T_</sup> _t_ =1<sup>:</sup> 


In practice, the action _at_ is instantiated as physically grounded control targets, such as end-effector motion in SE(3) (6-DoF pose or twist), gripper open/close (binary or continuous), arm joint commands, and, for dexterous hands, high-dimensional hand pose parameters (finger joint angles) that specify 3D interaction-relevant motion. Standard approaches derive such action supervision from largescale robot datasets such as Open X-Embodiment [54], DROID [37], and AgiBot World [2]. However, collecting robot demonstrations at scale is prohibitively expensive and often constrained by specific hardware setups, creating a bottleneck for generalizable policy learning. 

To mitigate this data scarcity, the community has turned to _human-centric data_ as a scalable source of interaction data. In this survey, we consider human-centric data through the lens of VLA learning: given the formulation in Eq. (1), where policies are conditioned on visual observations _ot_ , we focus on the portion of human-centric data that is available as _human videos_ and, within this visual setting, primarily refer to this subset simply as human videos. Before large-scale end-to-end VLAs became prevalent, early works leveraged human videos primarily as auxiliary signals or in specialized domains. For example, large-scale human video datasets were used to learn robust visual representations such as R3M and MVP [52, 70], define reward functions for reinforcement learning [48], or extract interaction affordances to guide planning [4, 13, 50]. 

More recently, HERMES [78] formulates a unified reinforcement learning framework that transforms multi-source human motions—including raw videos—into physically 


Figure 2: **Taxonomy of Human-to-Robot Policy Transfer.** Representative methods are organized into four paradigms by intermediate representations: **Latent Actions** , **World Models** , **Explicit 2D Representations** , and **Explicit 3D Representations** . The bottom band illustrates commonly used large-scale human-video datasets that serve as shared foundations for these methods. 

plausible behaviors for mobile dexterous robots. Similarly, EMMA [82] scales mobile manipulation by co-training on egocentric human data to reduce reliance on expensive robot teleoperation. These approaches leverage human videos to augment RL-based or modular control systems, rather than to learn generic representation bridges inside a single end-toend VLA model. 

In contrast, this survey focuses on the emerging paradigm of _VLA learning from human videos_ , which emphasizes the end-to-end integration of vision, language, and action within a unified generative or predictive framework. 

## **3 From Video to Action: A Taxonomy of Representation Bridges** 

Effectively learning VLA models from human videos necessitates a mechanism to bridge the morphology and dynamics <mark>gap between humans and robots. This is typically achieved</mark> by transforming raw video observations into structured _intermediate representation bridges_ —ranging from explicit 3D hand poses to abstract latent vectors—which distill controlrelevant semantics while discarding action-irrelevant visual variation. 

To provide a structured overview of this evolving landscape, we categorize representative methods into four paradigms based on their choice of intermediate representation (Fig. 2). We further summarize these works in Table 1, detailing their human video data sources, data scale, and the types of robotic end-effectors used for evaluation. This taxonomy highlights a rapidly diversifying space: explicit geometric representations continue to drive progress in high- 

precision dexterous control, and in parallel, implicit latent representations and predictive world models are increasingly explored to harness the vast potential of internet-scale, unlabelled human videos. 

### **3.1 Latent Actions** 

Latent-action learning methods aim to derive compact action representations from videos in a self-supervised manner, thereby circ <mark>umventin</mark> g the high <mark>cost of ac</mark> quiring additional action annotations. A common paradigm is to take observations at two time steps, _ot_ and _ot_ + _H_ , as input and infer a latent vector _zt_ , such that the future observation _ot_ + _H_ can be reconstructed from _zt_ and _ot_ . By introducing a strong information bottleneck ( _e.g._ , a VQ-VAE–style discretization [64]), _zt_ is forced to capture <mark>only the most</mark> salient inter-frame changes associated with action-relevant dynamics, effectively serving as a <mark>p</mark> rox <mark>y</mark> for the action variable in E <mark>q</mark> . <mark>(</mark> 1 <mark>)</mark> when absorbin <mark>g</mark> action knowledge from human videos. Since its introduction in VLA frameworks such as **LAPA** [74], key challenges have been: (i) learning a compact, expressive representation of action-relevant dynamics that generalizes across diverse embodiments and data sources; and (ii) effectively integrating latent action prediction into the VLA training pipeline. 

For learning latent actions, **IGOR** [19] applies asymmetric cropping augmentations during encoding and decoding to discourage incorporating absolute positional information. **UniVLA** [15] replaces pixel-space supervision with DINOv2 [53] features to avoid learning noisy details, and introduces a two-stage discretization with the aid of task instruction to disentangle task-irrelevant motions ( _e.g._ , camera 

Table 1: Taxonomy of representation bridges from human videos to robot manipulation. We categorize existing methods based on the intermediate representation used to bridge the domain gap between human videos and robotic control. The table summarizes video sources, data scale, representations, and the end-effectors evaluated in each work. **Source & Scale:** “Source” and “Clips / Hours” denote only humanvideo data; “–” indicates not reported or not applicable, and “*” indicates frame-based statistics. 

|**Paper**|**Source**|**Clips / Hours**|**Representation**|**End Effector**|
|---|---|---|---|---|
|**_Latent Actions_**|||||
|LAPA [2025]|SSv2|220k / –|VQ Latent Actions|Gripper|
|IGOR [2024]|SSv2, Epic, Ego4D, EGTEA|2m / –|VQ Latent Actions|Gripper|
|Moto [2025d]|SSv2|105k / –|VQ Latent Actions|Gripper|
|GO-1 [2025]|Ego4D|– / –|VQ Latent Actions|Gripper, Dex. Hand|
|GR00T [2025]|Ego4D, Ego-Exo4D,<br>Assembly-101, Epic, HOI4D,<br>HoloAssist, RH20T-Human|– / 2.5k|VQ Latent Actions|Gripper, Dex. Hand|
|UniVLA [2025]|Ego4D|– / –|VQ Latent Actions|Gripper|
|Villa-X [2025c]|Ego4D, EgoPAT3D, EGTEA<br>Gaze+, Epic, HO-Cap, HOI4D,<br>HoloAssist, RH20T, SSv2|3.6m / –|VQ Latent Actions|Gripper, Dex. Hand|
|ViPRA [2025]<br>|SSv2<br>|198k / –<br>|VQ Latent Actions<br>|Gripper<br>|
|Motus [2025a]|EgoDex|230k / –|Optical-Flow Latent Actions|Gripper|
|CLAP [2026]|Ego4D|– / 90h|VQ Latent Actions|Gripper|
|LAWM [2026]|YouTube Temporal-1B|– / 13k|Sparsity/Noise-Constrained<br>Latent Actions|Gripper|
|**_World Models_**|||||
|GR-1 [2024]|Ego4D|800k / 667|Generative Video Priors|Gripper|
|GR-2 [2024]|Ego4D, SSv2, Epic,<br>HowTo100M, Kinetics-700|38m / –|Generative Video Priors|Gripper|
|VPP [2024]|SSv2|192k / –|Generative Video Priors|Gripper, Dex. Hand|
|FLARE [2025]|Self-collected|– / –|Future Visual Features|Gripper, Dex. Hand|
|mimic-video [2025]|Web-scale|– / –|Generative Video Priors|Gripper, Dex. Hand|
|Gen2Act [2025]|Web-scale|270m+ / –|Predicted Frames|Gripper|
|**_Explicit 2D_**|||||
|ATM [2024]|Self-collected|0.3k / –|2D Point Trajectories|Gripper|
|Magma [2025a]|SSv2, Epic, Ego4D|4m / –|<br>2D Point Trajectories|Gripper|
|<br>Gemini Robotics [2025]|<br>Web-scale|– / –|<br>Boxes, Keypoints, Trajectories|Gripper|
|A0 [2025]|HOI4D|22k / –<br>|<br>Contact Points/Trajectories|Gripper|
|Masquerade [2025]|Epic|675k<sup>* </sup>/ –|2D Pose Trajectories|Gripper|
|**_Explicit 3D_**|||||
|VidBot [2025a]|Epic|– / –|3D Affordance|Gripper|
|EgoVLA [2025b]|HoloAssist, TACO, HOI4D,<br>HOT3D|500k<sup>* </sup>/ –|6-DoF Wrist Pose/MANO<br>Params|Dex. Hand|
|Being-H0 [2025]|UniHand|2.5m / 1155|MANO Params|Dex. Hand|
|<br>H-RDT [2025b]|EgoDex|338k / 829h|6-DoF Wrist Pose/3D Fingertips|Gripper|
|MotionTrans [2025a]|Self-collected|1.7k / –|<br>6-DoF Wrist Pose/Hand Joints|Dex. Hand|
|Yoshida et al. [2025]|Ego4D, EgoExo4D, Epic,<br>Nymeria|45k / –|6-DoF Object Pose|Gripper|
|VITRA [2025]|Ego4D, Epic, EgoExo4D, SSv2<br>|1m / –|3D Hand Pose|Dex. Hand|
|In-N-On [2025]|PH<sup>2</sup>SD|– / 1k+|6-DoF Wrist Pose/3D Fingertips|Dex. Hand|
|Simar et al. [2025]|Self-collected|– / 14|3D Hand Pose|Gripper|


motions). **ViPRA** [58] enforces optical flow consistency loss during reconstruction to encourage physically plausible motion encoding, whereas **Motus** [7] takes optical flow between observations as direct input, explicitly reducing the influence of appearance variations in latent action encoding. Some methods further incorporate robot data with ground-truth actions to better align latent actions with robot control. For example, **villa-X** [22] jointly learns human and robot latent 

action spaces conditioned on embodiment context, leveraging labeled robot data to ground the latent space in actionconditioned dynamics. Similarly, **CLAP** [80] aligns humanvideo latents with a quantized robot-derived latent space via contrastive learning, mitigating entanglement with irrelevant visual changes. Moving beyond discrete tokens, **LAWM** [28] adopts continuous actions with sparsity constraints to better capture large-scale, in-the-wild action dynamics. 

From another perspective, several works explore how to integrate latent action prediction into VLA training. **Moto** [23] adopts an autoregressive pretraining scheme for next latent action prediction, followed by inserting additional query tokens for robot action decoding during finetuning. **GO-1** [2] employs a hierarchical design, learning a latent planner that predicts future latent actions to bridge the vision-language backbone and a flow-based action expert. **GR00T N1** [9] uses latent actions as pseudo-targets for action decoding on human demonstrations, while jointly training with real action labels from heterogeneous robot data. 

Nevertheless, despite their effectiveness in extracting knowledge from human videos, it remains an open question whether highly compressed latent tokens can adequately represent the rich structure of complex, high-DoF dexterous manipulation. 

### **3.2 World Models** 

World-model-based approaches aim to predict how the environment evolves over time. For human videos, this encompasses not only the future actions of the human agent but also changes induced by its interactions with the environment. The underlying assumption is that accurately forecasting such dynamics equips the model with the action-relevant information needed for downstream control. Formally, this process can be expressed as _p_ ( _St_ +1: _t_ + _H | o≤t, l_ ), where _St_ +1: _t_ + _H_ denotes future environment state ( _e.g._ , raw pixels or visual features), conditioned on past observations _o≤t_ and the language instruction _l_<sup>1</sup> . This formulation can be learned via video generation without action supervision, analogous to latent actions but potentially more expressive for complex dynamics. 

Existing methods mainly study world-model architectures and how to transfer their learned knowledge to VLA action prediction. An early representative is **GR-1** [69], which proposes a GPT-style world model that autoregressively predicts future frames conditioned on the language instructions and visual observations. The model is pretrained on egocentric human videos, and subsequently fine-tuned on robot datasets with an additional next-action prediction objective, leveraging internal features learned during frame generation. This paradigm is scaled by **GR-2** [18] using web-scale human data [51] and VQGAN-based [25] visual tokens to improve the fidelity of future frame prediction, thereby facilitating the acquisition of more accurate action-related knowledge. **FLARE** [81] jointly trains its action decoder to perform action prediction and implicit world modeling by enforcing representation alignment (REPA) [76] between decoder’s internal features and future visual features on actionunlabeled human video. In contrast, VPP [34] treats a pretrained video generation model (SVD [12]) as a frozen feature extractor, using its “predictive visual representations” as conditions for downstream action policies. More recently, **Mimic-Video** [55] also shows that action prediction can be enhanced by leveraging intermediate representations from partially denoised steps of a pretrained video diffusion model 

> 1A stricter variant further conditions on future actions; in this survey, we focus on approaches that do not rely on action inputs. 

as conditioning signals. 

A complementary direction uses video generation as an explicit planning interface. **Gen2Act** [6] employs a pretrained video generation model to synthesize a “hallucinated” video plan from a static image. It constructs paired data by conditioning the generator on the initial frame of each robot demonstration to produce a corresponding human-like video, and then trains a video-conditioned policy that maps generated plans to robot actions. 

Despite their promising results, world-model-based methods often incur substantial training overhead, since learning world models requires generating large numbers of visual tokens. In addition, effectively distilling and transferring the knowledge embedded in world model to action prediction remains a non-trivial and under-explored challenge. 

### **3.3 Explicit 2D Representations** 

A complementary line of work relies on 2D visual primitives ( _e.g._ , keypoints, bounding boxes, 2D point trajectories) as intermediate representations. Unlike self-supervised latent actions or world models, these approaches leverage explicit and interpretable spatiotemporal cues, often extracted using 2D vision models, to bridge perception and action learning. The extracted cues are typically used as additional supervision to facilitate the acquisition of action-relevant knowledge from human videos. 

For example, **ATM** [68] uses dense point trajectories as action-like supervision, training a transformer to predict future motion, which then serves as a dynamic spatial prior for downstream manipulation. **Magma** [72] turns trajectories into an in-context control cue by rendering them as “Traceof-Mark” visual prompts, effectively converting unlabeled videos into VLA-style training pairs with explicit temporal structure. At larger scale, **Gemini Robotics** [62] trains an embodied reasoning backbone on human videos annotated with diverse 2D primitives (boxes, keypoints, and tracks), leveraging these signals to improve long-horizon generalization. 

Beyond generic motion cues, **A0** [71] focuses on explicit spatial-affordance supervision by modeling object-centric contact points and post-contact trajectories as embodimentagnostic interaction representations, enabling robust spatial reasoning across heterogeneous embodiments. From a complementary perspective, **Masquerade** [39] reduces the human–robot embodiment gap by editing in-the-wild human videos to visually resemble robot demonstrations, providing explicit 2D robot keypoint supervision that improves data efficiency and long-horizon generalization. 

While these methods efficiently exploit existing vision tools to extract action-relevant cues, they may inherit label noise from the underlying models and often require additional filtering. Furthermore, 2D cues can be fundamentally limited in expressing complex manipulation, due to the lack of depth information and occlusion reasoning, as real-world interactions are inherently three-dimensional. 

### **3.4 Explicit 3D Representations** 

Similar in spirit to 2D-based approaches, recent methods leverage 3D information extracted from human videos to train 

Table 2: **Classification of Human-Video Datasets for VLA. Scale** reports dataset size using the most standard unit for each dataset. **Geo Signal** indicates available geometric/3D-related signals (not necessarily explicit 3D labels). **Scripted** denotes whether data collection follows predefined tasks/procedures (staged/structured) rather than fully in-the-wild recording. 

|**Dataset**|**Scale**|**View**|**Language Annotation**|**Geo Signal**|**Scripted**|
|---|---|---|---|---|---|
|_Category 1: Datasets w/o Explicit 3D_|_Action Labels_|||||
|Something-Something V2 (SSv2) [29]|220K clips|3rd|✓|RGB|✓|
|EPIC-KITCHENS-100 (Epic) [24]|100 hours|Ego|✓|RGB|✗|
|Ego4D [30]|3.6K hours|Ego|✓|RGB|✗|
|EgoExo4D [31]|1.3K hours|MV + Ego|✓|MV (calib)|✗|
|HowTo100M [51]|136M clips|Mix|✓|RGB|✗|
|Egocentric-100K [3]|100K hours|Ego|✗|RGB|✗|
|EGTEA Gaze+ [40]|28 hours|Ego|✓|Gaze + Hand|✓|
|RH20T [27]|110K clips|MV + Ego|✓|MV (calib)|✓|
|Kinetics-700 [17]|650K clips|3rd|✓|RGB|✗|
|_Category 2: Datasets w/ Explicit 3D A_|_ction Labels_|||||
|HOI4D [44]|2.4M frames|Ego|✗|RGB-D|✓|
|Assembly-101 [59]|513K clips|MV + Ego|✓|MV (calib)|✓|
|EgoDex [33]|300K episodes|Ego|✓|RGB|✓|
|OAKINK2 [79]|4.0M frames|MV + Ego|✓|MV (calib)|✓|
|ARCTIC [26]|2.1M frames|MV + Ego|✓|MV (calib)|✓|
|TACO [46]|5.2M frames|MV + Ego|✗|MV (calib)|✓|
|HoloAssist [66]|166 hours|MV + Ego|✓|RGB-D|✓|
|HOT3D [5]|3.7M images|Ego|✗|MV (calib)|✓|


VLA policies. Compared to 2D cues, 3D representations provide a coordinate-consistent interface ( _e.g._ , SE(3) trajectories, parametric hand states, object poses), reducing viewpoint dependence and depth ambiguity, and aligning more naturally with VLA action prediction. In many systems, **parametric hand models** ( _e.g._ , MANO [57]) serve as a canonical and compact 3D representation of human manipulation and are widely used as a shared kinematic space linking human videos to robot control. Methods primarily vary in the types of videos they exploit, the strategies used to estimate 3D labels, and the mechanisms for bridging human and robot action spaces. 

**EgoVLA** [73] leverages videos with high-quality 3D hand action annotations, obtained via multi-view optimization or RGB-D SLAM, to pretrain VLA models. It unifies human and robot action prediction by considering only wrist poses and fingertip positions, and adopts inverse kinematics from this human action space for robot execution. **H-RDT** [8] adopts a similar hand-centric representation and leverages videos with hand annotations collected using AR/VR devices. **In-N-On** [16] also leverages AR-captured human videos and incorporates additional head poses into the unified action representation. **Being-H0** [47] scales to larger human-video corpora and discretizes continuous MANO hand trajectories into a vocabulary of motion tokens for VLA pretraining. 

Beyond learning from videos captured in controlled settings, recent methods have explored recovering 3D information from more in-the-wild videos. **VidBot** [20] combines structure-from-motion with depth foundation models to recover 3D affordance trajectories from unscripted videos. **VITRA** [43] proposes an automated pipeline that converts large 

collections of unscripted real-world human videos into robotaligned atomic action segments with MANO hand annotations and language instructions, enabling more scalable pretraining. **Yoshida et al.** [75] instead reconstruct 3D object pose changes from egocentric videos as supervisions. 

In addition to the human-pretraining and robot-fine-tuning paradigm, recent work has investigated alternative learning schemes for VLA. For example, **MotionTrans** [77] and work by **Kareer et al.** [36] collect human demonstrations with 3D action annotations using wearable devices and jointly train VLA models on both human and robot data, showing that such co-training improves robots’ generalization to previously unseen tasks. 

Although 3D representations are better aligned with VLA action prediction and facilitate human-to-robot transfer, acquiring accurate 3D labels remains difficult. Wearable devices can provide high-quality annotations in controlled settings, but web-scale data must rely on 3D reconstruction from vision models, which is particularly challenging in in-thewild scenarios and often introduces larger errors than 2D supervision. Moreover, directly predicting actions in 3D space requires models to not only understand image-space observations but also infer the underlying 3D world structure from 2D projections. From a generalization perspective, whether this paradigm is ultimately more effective than predicting in 2D image space remains an open question. 

## **4 Human-Centric Data for VLA Learning** 

In this section, we provide a detailed review of the humancentric data sources underpinning the aforementioned approaches, with a focus on their visual instantiation in the form 

of human videos. We organize them along two axes: whether they provide _explicit metric 3D action labels_ and whether collection is _scripted_ or _unscripted_ . Explicit 3D action labels determine whether action supervision can be directly grounded into robot-executable actions or are typically inferred from visual state transitions [11, 32]. Table 2 summarizes this taxonomy. 

**Datasets without Explicit 3D Action Labels.** These datasets provide RGB videos with semantic annotations (e.g., scenes, objects, action descriptions) but lack metric 3D trajectories of hands or bodies in a camera/world frame, such as 3D keypoints or MANO parameters. Consequently, they are mainly used to support _latent-action_ or _world-model_ -based approaches, where actions are inferred from visual state transitions rather than directly specified in a 3D action space. 

Representative datasets include Something-Something V2 (short hand–object clips for manipulation dynamics) [29], EPIC-KITCHENS (large-scale egocentric kitchen activities) [24], Ego4D (egocentric daily-life video across diverse scenarios) [30], HowTo100M (Internet-scale instructional video) [51], Egocentric-100K (100K hours from factory environments, largely without annotations) [3], and Ego-Exo4D (synchronized ego–exo multi-view recordings for cross-view learning) [31]. Despite their scale and diversity, these datasets are typically used as video sources rather than as providers of metric 3D action representations. In terms of collection protocol, Something-Something V2 is scripted via predefined action templates [29], whereas EPIC-KITCHENS, Ego4D, Ego-Exo4D, HowTo100M, and Egocentric-100K are unscripted [24, 30, 31, 51, 3]. The absence of predefined boundaries in continuous in-the-wild recordings complicates both action segmentation and instruction annotation for imitation learning. 

**Datasets with Explicit 3D Action Labels.** A smaller but crucial class of datasets provides _explicit metric 3D action annotations_ , including 3D keypoint trajectories of hands/bodies and parametric representations such as MANO or SMPL. They are typically captured with instrumented setups (e.g., AR/VR headsets, depth sensors, or motion capture) that record motion in camera/world coordinates. 

Representative datasets in this domain include HOI4D [44], HOT3D [5], EgoDex [33], ARCTIC [26], TACO [46], Assembly101 [59], OakInk2 [79] and HoloAssist [66]. These works advance egocentric perception across varying levels of granularity and task complexity. In terms of 3D perception, HOI4D provides egocentric RGB-D with frame-wise 3D hand and object poses [44], while HOT3D further addresses occlusion challenges by leveraging egocentric multiview videos to achieve high-fidelity hand and object tracking [5]. Regarding fine-grained manipulation, EgoDex uses headmounted AR to collect 3D hand trajectories for dexterous imitation learning [33], ARCTIC captures bimanual articulation with dynamic contact information [26], and Taco establishes a benchmark for generalizable bimanual tool-action-object understanding [46]. At the task and assistance level, Assembly101 focuses on long-horizon procedural activities with dense segmentation [59], OakInk2 adopts an object-centric hierarchy (affordances to complex tasks) for structured mo- 

tion generation [79], and HoloAssist targets interactive AI assistants with real-world data centered on human intent and guidance [66]. These datasets enable direct supervision with explicit 2D/3D action labels and are closest to robot imitation learning, often improving data efficiency [43]. However, they are usually smaller-scale and collected in laboratory or instrumented settings, trading diversity for annotation fidelity. Consistent with this, collection is commonly _scripted_ , with predefined interactions and objects and carefully segmented action units that align well with imitation-learning supervision, but limit behavioral diversity, scalability, and representativeness relative to large unscripted corpora. 

## **5 Challenges and Future Directions** 

In this section, we analyze open challenges shared across methods that leverage human videos, organizing them around three key interfaces in the human-video-to-robot pipeline: transforming unstructured videos into trainingready episodes, handling heterogeneity when mapping videoderived supervision to robot-executable actions, and designing evaluations that predict real deployment performance. 

### **5.1 Transforming Human Videos to Episodes** 

A bottleneck appears upstream of policy learning. Web-scale human videos from platforms such as YouTube and TikTok are rarely packaged into episodes that match the supervision granularity required by robot learning. Instructional corpora such as HowTo100M [51] offer a scalable proxy but suffer from weak alignment between narration and manipulation, while egocentric datasets [30, 31, 24] remain largely untrimmed and often contain viewpoint changes and off-task segments. As a result, clips frequently mix intents, and similar visual transitions can correspond to different latent actions. This ambiguity degrades learning signals by destabilizing discrete tokenization and diverting model capacity toward control-irrelevant dynamics. Procedural datasets such as HOI4D and Assembly101 [44, 59] mitigate this issue by aligning video units with manipulation primitives, whereas in-the-wild video requires explicit episodization, as explored by systems such as VITRA [43]. Future episodization would benefit from semantic- and interaction-driven segmentation, defining segments around manipulation phases and object state changes rather than fixed time windows. Standardized construction protocols are also needed to reduce hidden variance and support rigorous comparison. 

### **5.2 Addressing Heterogeneity** 

**Embodiment Mismatch.** Embodiment mismatch stems from kinematic and contact-mechanics differences between human hands and robotic end-effectors. Retargeting is intrinsically under-constrained when high-DoF human motion is mapped onto lower-DoF robot control spaces. As a result, distinct human motions can yield the same robot command, and some motions may admit no feasible realization [56]. This issue is amplified for simple grippers and across diverse end-effector morphologies, where action spaces are not aligned, complicating cross-morphology VLA training [8]. A practical response is to emphasize embodiment-invariant supervision, such as interaction intent and object-centric effects, 

rather than literal trajectory imitation. Hardware advances may reduce the gap [60, 63], but reliable transfer will still require morphology-conditioned grounding mechanisms that map shared priors into feasible commands under platformspecific constraints. 

**Viewpoint Heterogeneity.** Robot manipulation policies are typically trained and deployed with fixed, robot-centric views, such as head-mounted cameras, often supplemented by wrist or eye-in-hand cameras for contact-centric detail [10]. In contrast, web-scale human video, however, is predominantly exocentric, where fine contacts are weakly observed and occlusions around the interaction site are common [51]. Egocentric human video is closer but still mismatched, since head-mounted streams ( _e.g._ , Ego4D, EPICKITCHENS) exhibit rapid viewpoint shifts driven by head turns and frequent occlusions, which can remove active hand–object contact from view during manipulation [30, 24]. Progress will likely require explicit cross-view alignment between human and robot observations and an action representation that is anchored to interaction outcomes, for example, object state changes, rather than view-specific appearance. 

### **5.3 Benchmarking and Evaluation** 

A key challenge is that existing benchmarks only partially reflect the regime in which human video supervision is intended to help. Standard suites such as LIBERO [45], CALVIN [49], and SIMPLER [42] support controlled comparison, but their task templates and simulated scenes under-represent the diversity and long-horizon structure typical of internet human videos. As a result, reported improvements can be benchmark-specific and do not directly answer the central question, namely transfer efficiency under a fixed robot-data budget. Real-robot evaluation remains necessary, yet scaling and standardizing it is difficult due to cost, safety, and platform variability. Progress will benefit from evaluation protocols that explicitly track deployment-relevant generalization and transfer efficiency. This includes reporting performance as a function of robot-data budget, using held-out splits over novel objects and scenes, and quantifying robustness under viewpoint and embodiment shifts. In particular, to isolate the contribution of human video pretraining, evaluation protocols should compare models with and without human-video-based initialization under matched robot-data and compute budgets across diverse downstream tasks and embodiments. Testbeds closer to human activity distributions, such as BEHAVIOR-1K [41], together with scalable digital-twin and domain-randomized toolchains such as Cosmos [1] and RoboTwin [21], can increase coverage and reproducibility. Complementary efforts on LLM-driven task generation in simulation, such as GenSim and GenSim2 [67, 35], suggest a path toward automatically constructing more diverse and long-horizon evaluation suites, although these approaches currently operate largely without directly leveraging human videos. 

## **6 Conclusion** 

Human videos offer a scalable route to easing the data bottleneck in VLA learning, but only when the gap between hu- 

man observation and robot execution is bridged in a principled way. In this survey, we organized recent progress around a taxonomy of representation bridges that transform human videos into action-relevant signals, covering approaches that infer latent actions, learn predictive world models, and construct explicit 2D and 3D representations. This taxonomy highlights complementary strengths, with implicit representations scaling across diverse video sources and explicit geometric cues offering stronger grounding and a clearer interface to robot-executable actions. 

Looking ahead, progress will depend not only on better representations, but also on the surrounding pipeline, including episodizing in-the-wild video, handling kinematic and viewpoint mismatch, and developing evaluation protocols that better predict deployment performance and transfer efficiency. Addressing these challenges is central to making broadly pretrained VLA models, learned from human videos, generalize reliably across tasks, embodiments, and real-world environments. 

## **References** 

- [1] Niket Agarwal, Arslan Ali, et al. Cosmos world foundation model platform for physical ai. _arXiv preprint arXiv:2501.03575_ , 2025. 

- [2] AgiBot-World-Contributors. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _IROS_ , pages 3549–3556, 2025. 

- [3] Build AI. Egocentric-100k, 2025. 

- [4] Shikhar Bahl, Russell Mendonca, et al. Affordances from human videos as a versatile representation for robotics. In _CVPR_ , 2023. 

- [5] Prithviraj Banerjee, Sindi Shkodrani, Pierre Moulon, Shreyas Hampali, Shangchen Han, Fan Zhang, Linguang Zhang, Jade Fountain, Edward Miller, Selen Basol, et al. Hot3d: Hand and object tracking in 3d from egocentric multi-view videos. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 7061–7071, 2025. 

- [6] Homanga Bharadhwaj, Debidatta Dwibedi, et al. Gen2act: Human video generation in novel scenarios enables generalizable robot manipulation. In _CoRL_ , volume 305 of _PMLR_ , pages 3936–3951. PMLR, 2025. 

- [7] Hongzhe Bi, Hengkai Tan, et al. Motus: A unified latent action world model. _arXiv:2512.13030_ , 2025. 

- [8] Hongzhe Bi, Lingxuan Wu, et al. H-RDT: Human manipulation enhanced bimanual robotic manipulation. _arXiv:2507.23523_ , 2025. 

- [9] Johan Bjorck, Fernando Casta˜neda, et al. GR00T N1: An open foundation model for generalist humanoid robots. _arXiv:2503.14734_ , 2025. 

- [10] Kevin Black, Noah Brown, et al. _π_ 0: A visionlanguage-action flow model for general robot control. _arXiv:2410.24164_ , 2024. 

- [11] Nils Blank, Moritz Reuss, et al. Scaling robot policy learning via zero-shot labeling with foundation models. _Conference on Robot Learning (CoRL)_ , 2024. 

- [12] Andreas Blattmann, Tim Dockhorn, et al. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_ , 2023. 

- [13] Jessica Borja-Diaz, Oier Mees, et al. Affordance learning from play for sample-efficient policy learning. In _ICRA_ , Philadelphia, USA, 2022. 

- [14] Anthony Brohan, Noah Brown, et al. RT-2: Visionlanguage-action models transfer web knowledge to robotic control. In _CoRL_ , 2023. arXiv preprint available. 

- [15] Qingwen Bu, Yanting Yang, et al. UniVLA: Learning to act anywhere with task-centric latent actions. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- [16] Xiongyi Cai, Ri-Zhao Qiu, et al. In-N-On: Scaling egocentric manipulation with in-the-wild and on-task data. _arXiv:2511.15704_ , 2025. 

- [17] Joao Carreira, Eric Noland, Chloe Hillier, and Andrew Zisserman. A short note on the kinetics-700 human action dataset. _arXiv preprint arXiv:1907.06987_ , 2019. 

- [18] Chi-Lam Cheang, Guangzeng Chen, et al. GR-2: A generative video-language-action model with web-scale knowledge for robot manipulation. _arXiv:2410.06158_ , 2024. 

- [19] Xiaoyu Chen, Junliang Guo, et al. Igor: Image-goal representations are the atomic control units for foundation models in embodied AI. _arXiv:2411.00785_ , 2024. 

- [20] Hanzhi Chen, Boyang Sun, et al. VidBot: Learning generalizable 3D actions from in-the-wild 2D human videos. In _CVPR_ , 2025. 

- [21] Tianxing Chen, Zanxin Chen, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 

- [22] Xiaoyu Chen, Hangxing Wei, et al. Villa-x: enhancing latent action modeling in vision-language-action models. _arXiv preprint arXiv:2507.23682_ , 2025. 

- [23] Yi Chen, Yuying Ge, et al. Moto: Latent motion token as the bridging language for learning robot manipulation from videos. In _ICCV_ , 2025. 

- [24] Dima Damen, Hazel Doughty, et al. The EPICKITCHENS dataset: Collection, challenges and baselines. _TPAMI_ , 43(11), 2020. 

- [25] Patrick Esser, Robin Rombach, and Bjorn Ommer. Taming transformers for high-resolution image synthesis. In _CVPR_ , pages 12873–12883, 2021. 

- [26] Zicong Fan, Omid Taheri, et al. Arctic: A dataset for dexterous bimanual hand-object manipulation. In _CVPR_ , pages 12943–12954, 2023. 

- [27] Hao-Shu Fang, Hongjie Fang, Zhenyu Tang, Jirong Liu, Chenxi Wang, Junbo Wang, Haoyi Zhu, and Cewu Lu. Rh20t: A comprehensive robotic dataset for learning diverse skills in one-shot. _arXiv preprint arXiv:2307.00595_ , 2023. 

- [28] Quentin Garrido, Tushar Nagarajan, et al. Learning latent action world models in the wild, 2026. 

- [29] Raghav Goyal, Samira Ebrahimi Kahou, et al. The ”something something” video database for learning and evaluating visual common sense. In _ICCV_ , 2017. 

- [30] Kristen Grauman, Andrew Westbury, et al. Ego4D: Around the world in 3,000 hours of egocentric video. In _CVPR_ , 2022. 

- [31] Kristen Grauman, Andrew Westbury, et al. Ego-Exo4D: Understanding skilled human activity from first-and thirdperson perspectives. In _CVPR_ , 2024. 

- [32] Noriaki Hirose, Catherine Glossop, et al. Lelan: Learning a language-conditioned navigation policy from in-thewild videos. In _Conference on Robot Learning_ , 2024. 

- [33] Ryan Hoque, Peide Huang, et al. Egodex: Learning dexterous manipulation from large-scale egocentric video. _arXiv preprint arXiv:2505.11709_ , 2025. 

- [34] Yucheng Hu, Yanjiang Guo, et al. Video prediction policy: A generalist robot policy with predictive visual representations. In _ICML_ . PMLR, 2024. 

- [35] Pu Hua, Minghuan Liu, Annabella Macaluso, Yunfeng Lin, Weinan Zhang, Huazhe Xu, and Lirui Wang. Gensim2: Scaling robot data generation with multi-modal and reasoning llms. _arXiv preprint arXiv:2410.03645_ , 2024. 

- [36] Simar Kareer, Karl Pertsch, et al. Emergence of human to robot transfer in vision-language-action models. _arXiv preprint arXiv:2512.22414_ , 2025. 

- [37] Alexander Khazatsky, Karl Pertsch, et al. Droid: A large-scale in-the-wild robot manipulation dataset. In _DGR@RSS 2024 (Poster)_ , 2024. 

- [38] Moo Jin Kim, Karl Pertsch, et al. OpenVLA: An opensource vision-language-action model. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2024. 

- [39] Marion Lepert, Jiaying Fang, et al. Masquerade: Learning from in-the-wild human videos using data-editing. In _H2R Workshop at the Conference on Robot Learning (CoRL)_ , 2025. 

- [40] Yin Li, Miao Liu, and James M Rehg. In the eye of the beholder: Gaze and actions in first person video. _IEEE transactions on pattern analysis and machine intelligence_ , 45(6):6731–6747, 2021. 

- [41] Chengshu Li, Ruohan Zhang, et al. Behavior-1k: A human-centered, embodied ai benchmark with 1,000 everyday activities and realistic simulation. _arXiv preprint arXiv:2403.09227_ , 2024. 

- [42] Xuanlin Li, Kyle Hsu, et al. Evaluating real-world robot manipulation policies in simulation. In _Conference on Robot Learning_ , 2024. 

- [43] Qixiu Li, Yu Deng, et al. Scalable vision-languageaction model pretraining for robotic manipulation with real-life human activity videos. _arXiv:2510.21571_ , 2025. 

- [44] Yunze Liu, Yun Liu, et al. HOI4D: A 4d egocentric dataset for category-level human-object interaction. In _CVPR_ , 2022. 

- [45] Bo Liu, Yifeng Zhu, et al. Libero: Benchmarking knowledge transfer for lifelong robot learning. _NIPS_ , 36:44776–44791, 2023. 

- [46] Yun Liu, Haolin Yang, Xu Si, Ling Liu, Zipeng Li, Yuxiang Zhang, Yebin Liu, and Li Yi. Taco: Benchmarking generalizable bimanual tool-action-object understanding. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 21740– 21751, 2024. 

- [47] Hao Luo, Yicheng Feng, et al. Being-H0: Visionlanguage-action pretraining from large-scale human videos. _arXiv:2507.15597_ , 2025. 

- [48] Jason Yecheng Ma, Shagun Sodhani, et al. VIP: Towards universal visual reward and representation via value-implicit pre-training. In _ICLR_ , 2023. Spotlight presentation. 

- [49] Oier Mees, Lukas Hermann, et al. Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7(3):7327–7334, 2022. 

- [50] Oier Mees, Jessica Borja-Diaz, et al. Grounding language with visual affordances over unstructured data. In _ICRA_ , London, UK, 2023. 

- [51] Antoine Miech, Dimitri Zhukov, et al. HowTo100M: Learning a text-video embedding by watching hundred million narrated video clips. In _ICCV_ , 2019. 

- [52] Suraj Nair, Aravind Rajeswaran, et al. R3M: A universal visual representation for robot manipulation. In _CoRL_ , 2022. 

- [53] Maxime Oquab, Timoth´ee Darcet, et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 

- [54] Abby O’Neill, Abdul Rehman, et al. Open X- Embodiment: Robotic learning datasets and RT-X models. In _ICRA_ , 2024. 

- [55] Jonas Pai, Liam Achenbach, et al. mimic-video: Videoaction models for generalizable robot control beyond vlas. _arXiv preprint arXiv:2512.15692_ , 2025. 

- [56] Yuzhe Qin, Yueh-Hua Wu, et al. Dexmv: Imitation learning for dexterous manipulation from human videos. In _ECCV_ , 2022. 

- [57] Javier Romero, Dimitrios Tzionas, et al. Embodied hands: Modeling and capturing hands and bodies together. _ACM Transactions on Graphics_ , 36(6), 2017. 

- [58] Sandeep Routray, Hengkai Pan, et al. ViPRA: Video prediction for robot actions. _arXiv:2511.07732_ , 2025. 

- [59] Fadime Sener, Dibyadip Chatterjee, et al. Assembly101: A large-scale multi-view video dataset for understanding procedural activities. In _CVPR_ , 2022. 

- [60] Shenzhen ShARPA Robotics. Wave humanoid robot. https://www.sharpa.com/pages/wave, 2024. Accessed 2025-01. 

- [61] Reuben Tan, Baolin Peng, et al. Multimodal reinforcement learning with agentic verifier for ai agents. _arXiv preprint arXiv:2512.03438_ , 2025. 

- [62] Gemini Robotics Team. Gemini Robotics: Bringing AI into the physical world. _arXiv:2503.20020_ , 2025. 

- [63] Tesla, Inc. Tesla ai day 2022. https://www.youtube. com/watch?v=ODSJsviD ~~S~~ U, September 2022. Official technical presentation. 

- [64] Aaron Van Den Oord, Oriol Vinyals, et al. Neural discrete representation learning. _NIPS_ , 30, 2017. 

- [65] Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pages 1723–1736. PMLR, 2023. 

- [66] Xin Wang, Taein Kwon, Mahdi Rad, Bowen Pan, Ishani Chakraborty, Sean Andrist, Dan Bohus, Ashley Feniello, Bugra Tekin, Felipe Vieira Frujeri, et al. Holoassist: an egocentric human interaction dataset for interactive ai assistants in the real world. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 20270–20281, 2023. 

- [67] Lirui Wang, Yiyang Ling, Zhecheng Yuan, Mohit Shridhar, Chen Bao, Yuzhe Qin, Bailin Wang, Huazhe Xu, and Xiaolong Wang. Gensim: Generating robotic simulation tasks via large language models, 2024. 

- [68] Chuan Wen, Xingyu Lin, et al. Any-point trajectory modeling for policy learning. In _RSS_ , 2024. 

- [69] Hongtao Wu, Ya Jing, et al. Unleashing large-scale video generative pre-training for visual robot manipulation. In _ICLR_ , 2024. Poster presentation. 

- [70] Tete Xiao, Ilija Radosavovic, et al. Masked visual pretraining for motor control. _arXiv:2203.06173_ , 2022. 

- [71] Rongtao Xu, Jian Zhang, et al. A0: An affordanceaware hierarchical model for general robotic manipulation. In _ICCV_ , 2025. 

- [72] Jianwei Yang, Reuben Tan, et al. Magma: A foundation model for multimodal AI agents. In _CVPR_ , 2025. 

- [73] Ruihan Yang, Qinxi Yu, et al. EgoVLA: Learning vision-language-action models from egocentric human videos. _arXiv:2507.12440_ , 2025. 

- [74] Seonghyeon Ye, Joel Jang, et al. Latent action pretraining from videos. In _ICLR_ , 2025. Poster presentation. 

- [75] Tomoya Yoshida, Shuhei Kurita, et al. Developing vision-language-action model from egocentric videos. _arXiv:2509.21986_ , 2025. 

- [76] Sihyun Yu, Sangkyung Kwak, Huiwon Jang, et al. Representation alignment for generation: Training diffusion transformers is easier than you think. _arXiv preprint arXiv:2410.06940_ , 2024. 

- [77] Chengbo Yuan, Rui Zhou, et al. Motiontrans: Human vr data enable motion-level learning for robotic manipulation 

policies. In _H2R Workshop at the Conference on Robot Learning (CoRL)_ , 2025. 

- [78] Zhecheng Yuan, Tianming Wei, et al. Hermes: Humanto-robot embodied learning from multi-source motion data for mobile dexterous manipulation. In _Proceedings of the 9th Conference on Robot Learning (CoRL)_ , 2025. 

- [79] Xinyu Zhan, Lixin Yang, et al. Oakink2: A dataset of bimanual hands-object manipulation in complex task completion. In _CVPR_ , pages 445–456, 2024. 

- [80] Chubin Zhang, Jianan Wang, et al. Clap: Contrastive latent action pretraining for learning vision-language-action models from human videos, 2026. 

- [81] Ruijie Zheng, Jing Wang, et al. FLARE: Robot learning with implicit world modeling. In _SWOMO Workshop at Robotics: Science and Systems (RSS)_ , 2025. 

- [82] Lawrence Y. Zhu, Pranav Kuppili, et al. Emma: Scaling mobile manipulation via egocentric human data. In _H2R Workshop at the Conference on Robot Learning (CoRL)_ , 2025. 

