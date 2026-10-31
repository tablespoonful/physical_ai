---
title: "Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation"
date: "2026-03-17"
authors: "Mutian Xu; Tianbao Zhang; Tianqi Liu; Zhaoxi Chen; Xiaoguang Han; Ziwei Liu"
url: https://arxiv.org/abs/2603.16669
pdf: https://arxiv.org/pdf/2603.16669
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.16669)** / [論文ページ](https://arxiv.org/abs/2603.16669)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation** 

Mutian Xu<sup>1</sup> Tianbao Zhang<sup>2</sup> Tianqi Liu<sup>1</sup> Zhaoxi Chen<sup>1</sup> Xiaoguang Han<sup>2</sup> Ziwei Liu<sup>1</sup><sup>_†_</sup> 

> 1 S-Lab, Nanyang Technological University 

> 2 SSE, CUHKSZ 

mutianxu.github.io/Kinema4D-project-page 


**Fig. 1:** We propose **Kinema4D** , a new _action-conditioned 4D generative embodied simulator_ . Given an initial world image with a robot at a canonical setup space, and an action sequence, our method generates future robot-world interactions in 4D space. It simulates physically plausible and geometrically consistent interactions between complex robot actions and diverse objects across various spatial constraints, providing a new foundation for advancing next-generation embodied simulation. 

**Abstract.** Simulating robot-world interactions is a cornerstone of Embodied AI. Recently, a few works have shown promise in leveraging video generations to transcend the rigid visual/physical constraints of traditional simulators. However, they primarily operate in 2D space or are guided by static environmental cues, ignoring the fundamental reality that robot-world interactions are _inherently 4D spatiotemporal events_ that require _precise_ interactive modeling. To restore this 4D essence while ensuring the precise robot control, we introduce Kinema4D, a new action-conditioned 4D generative robotic simulator that disentangles the robot-world interaction into: i) _Precise_ 4D representation of 

> † Corresponding author. 

2 Xu et al. 

_robot controls_ : we drive a URDF-based 3D robot via kinematics, producing a precise 4D robot control trajectory. ii) _Generative_ 4D modeling of _environmental reactions_ : we project the 4D robot trajectory into a pointmap as a spatiotemporal visual signal, controlling the generative model to synthesize complex environments’ reactive dynamics into synchronized RGB/pointmap sequences. To facilitate training, we curated a large-scale dataset called Robo4D-200k, comprising 201,426 robot interaction episodes with high-quality 4D annotations. Extensive experiments demonstrate that our method effectively simulates physically-plausible, geometry-consistent, and embodiment-agnostic interactions that faithfully mirror diverse real-world dynamics. For the first time, it shows potential _zero-shot_ transfer capability, providing a high-fidelity foundation for advancing next-generation embodied simulation. 

**Keywords:** Embodied simulation · 4D generative world model · Spatiotemporal-aware · Precise control · Large-scale 4D robotic data 

## **1 Introduction** 

In the field of Embodied AI, the ability to roll out robot trajectories within a world environment is pivotal for scaling up robot demonstrations [54], policy evaluation [41, 66], and reinforcement learning [18]. Nevertheless, executing actions in the real world is prohibitively costly, potentially unsafe, and necessitates constant expert maintenance [7,38]. Consequently, robotic simulation in virtual environments has emerged as a vital surrogate for real-world deployment. 

While significant efforts have been dedicated to developing robust physical simulators [16, 51, 52, 74], these platforms often lack visual realism and rely on hand-crafted and pre-defined physical properties/rules. Such dependencies create a significant scalability bottleneck, particularly when attempting to synthesize new environments. Very recently, to circumvent these limitations, researchers have begun leveraging the intrinsic world dynamics captured by video generative models to synthesize robot-environment interactions across diverse scenes [2,91]. By casting robot actions as conditional prompts for video synthesis, these methods directly simulate the visual outcome of adding robot controls to an environment, bypassing the need for predefined physical modeling required for traditional simulation. However, a critical gap remains. Current models primarily operate within a 2D pixel space [2,91], whereas robot-world interactions are _inherently 4D spatiotemporal events_ . Without 4D constraints, physical interaction loses its most fundamental grounding. Although a few latest works [48,89] explored 4D simulation, they primarily rely on high-level linguistic instructions to represent robot control. Such semantic representations, while intuitive, _lack the precise guidance_ essential for high-fidelity 4D world modeling. As a result, existing methods struggle to simulate precise interactive effects—such as material deformations or occluded object dynamics (see Figs. 4 and 5). 

To bridge this gap and advance this problem, we propose Kinema4D, a new action-conditioned 4D generative robotic simulator. Our core motivation is to 

Kinema4D 3 

restore robot-world interactions to their _4D spatiotemporal essence_ , while ensuring _precise robot control_ . This motivation is further grounded in two synergetic insights that support our design philosophy—disentangling the simulation into _robot control_ and their _resultant environmental changes_ : 

**i)** **_Precise_ 4D representation of robot actions via kinematic control** : We recognize the fact that robot action is a _precise physical certainty in 4D space_ and should not be “guessed” by a generative model. A joint-angle sequence or an end-effector pose is merely an abstract vector until it is mapped onto a physical structure. Reflecting on this, our framework enables a bridge that is otherwise impossible in 2D: we drive a 3D-reconstructed, URDF-based robot model via explicit kinematics to produce a continuous 4D robot trajectory that is guaranteed to be kinematically correct, providing the high-granularity spatiotemporal information that serves as the _causal driver_ for any interaction. **ii)** **_Generative_ 4D modeling of environmental reactions via controllable generation** : While robot controls are deterministic, we argue that complex environments’ dynamics require a _flexible generative modeling_ . To this end, we project the previously derived 4D robot trajectory into a pointmap sequence—serving as a spatiotemporal visual signal, which controls the generative model to offload the burden of kinematic modeling and focus exclusively on synthesizing the environment’s _reactive dynamics_ . Moreover, our architecture simultaneously predicts synchronized RGB and pointmap sequences, effectively transforming the generation into a spatiotemporal reasoning task within a unified 4D space. This makes the result not only visually realistic but also geometrically consistent. In this paradigm, spatiotemporal awareness is enforced not merely as a control signal but as an intrinsic constraint throughout the generative process. This fosters a symbiosis between _precise control_ and _flexible synthesis_ . 

To facilitate the training of our framework, we curated a large-scale dataset called Robo4D-200k, comprising 201,426 real-world and synthetic demonstrations with high-quality 4D annotations. We extensively benchmark our method using both video and geometric metrics, as well as policy evaluation. Experiments show that our Kinema4D generalizes to simulate physically-plausible robot-world interactions that closely mirror diverse real-world dynamics, and for the first time, shows potential zero-shot OOD transfer capability. 

Our contributions are summarized as: 

- Kinema4D, a new action-conditioned 4D generative robotic simulator that enjoys both spatiotemporal rigor and generative flexibility. 

- Robo4D-200k, to our knowledge, the largest-scale 4D robotic dataset comprising 201,426 demonstrations with high-quality 4D annotations. 

- A comprehensive evaluation scheme demonstrating that our method mirrors real-world dynamics, providing a new foundation for embodied simulation. 

- Our code, dataset, and checkpoints will all be public upon acceptance. 

4 Xu et al. 

## **2 Related Work** 

We review the evolution of embodied simulation, tracing its trajectory from classical physics engines to the recent emergence of generative world models. 

_Physical simulation._ Classical robotic simulation methods rely on physics engines, such as MuJoCo, IssacSim, SAPIEN [19, 51–53, 67, 74]. They simulate interactions based on rigid-body dynamics, requiring meticulously hand-crafted meshes, precise physical properties ( _e.g_ ., friction, mass), and pre-defined rules. Recent real-to-sim advancements further leverage 3D Gaussian Splatting (3DGS) with continuum mechanics or rigid-body solvers to reconstruct digital twins directly from real-world captures [1, 25, 36, 40, 55]. A few methods also focus on simulating realistic depth [46, 76]. Nevertheless, they rely on explicit physical solvers and predefined laws, which struggle to generalize to complex environmental responses, limiting their scalability across unstructured environments. 

_Learning world models._ World Models [3, 24] aim to internalize the underlying dynamics of the environment, allowing agents to “dream” and plan within a learned latent space. With the advent of diffusion models [27,56,63] and largescale video pre-training [8,28,69,85], video generative models have demonstrated an extraordinary ability to capture complex visual dynamics [4,12]. Furthermore, _interactive_ video generation has advanced through the integration of various conditioning mechanisms [87] designed to represent diverse control signals. Early efforts in this direction have focused on injecting viewpoint trajectories [22,43, 59,82,83] to synthesize immersive, navigable environments. 

_Embodied video-generation models._ Recently, research has pivoted toward using embodied actions as controls for interactive video generation, aiming to synthesize robot-world interactions with both visual and physical fidelity. Based on the representation of embodied actions at the input level, this research stream can be categorized into four sub-groups. 1) Text: A main-stream works [13,20,77,78,90] generate visual outcomes from high-level text instructions, which lack the finegrained precision required for low-level manipulations. 2) Latent embedding: Another type of works [2, 9, 10, 21, 23, 35, 44, 50, 73, 84, 91] such as IRASim [91] and Ctrl-World [23] typically encode 7-DoF end-effector poses into compressed embeddings. This forces the generative model to infer or ‘guess’ the underlying robot kinematics, often resulting in physically implausible failures. 3) Semantics: ORV [80] introduces 3D semantic occupancy of static environments; however, it needs an off-the-shelf occupancy-prediction model to acquire and lacks temporal dynamics, still requiring action encodings or text to provide dynamic information. 4) 2D visual prompt: EVAC [37], AnchorDream [81], and VAP [71] represent embodied actions using 2D prompts like angle arrows, 2D renders, and skeletons. A concurrent work, BridgeV2W [14], utilizes URDF to drive robots but merely renders the resulting trajectory into 2D binary masks. Such 2D-based signals lack spatiotemporal constraints and struggle to provide precise control guidance. Commonly, as for the output, all aforementioned methods use video 

Kinema4D 5 

generations to predict 2D ( _i.e_ ., RGB) frames, treating the robot/environment as a monolithic pixel stream. Due to the lack of spatiotemporal awareness, they struggle to simulate complex physical interactions. 

**Summary** : Whether evaluated by action conditioning or output modality, the aforementioned methods fail to resolve the **_challenging trilemma_** of _dynamics, precision_ and _spatiotemporal awareness_ —the three pillars of reliable embodied simulation. To overcome this, our Kinema4D learns intricate dynamics through a 4D generative model, where abstract action controls are grounded via kinematics, securing precision and spatiotemporal awareness, which in turn anchors the generative model to synthesize complex dynamics. 

_3D/4D world models._ Several recent works have been able to output 3D/4D worlds. First, ParticleFormer [33] and PointWorld [34] directly utilize simple transformers to predict the trajectories of pre-defined 3D particles for both robots and environments. However, they lack the generative flexibility required to synthesize new geometry that depicts emergent world dynamics beyond the initial 3D input. On the other hand, 4D-native generative models that aim to generate full spatio-temporal sequences have gained significant attention. For instance, Aether [65] unifies geometry-aware reasoning by jointly optimizing 4D dynamic reconstruction and goal-conditioned video prediction, while 4DNex [15] enables 4D world generation in a single feed-forward pass. Although recent advancements such as TesserAct [89], GWM [49], iMoWM [84], and Robo4DGen [48] demonstrate the ability to synthesize 4D embodied worlds at the output stage, they remain constrained by a critical design bottleneck: they solely inject _static_ guidance ( _e.g_ ., depth maps, surface normals, or Gaussian splats) from the initial world environment, which _lacks temporal dynamics_ . Consequently, these models still rely on text instructions or latent tokens to inject robot actions, which _lack the granularity_ required for fine-grained interactions. In contrast, by transforming abstract robot actions into 4D pointmaps, our Kinema4D accepts _precise_ robot controls with _both spatial and temporal cues_ . To fully utilize such controls, we apply a 4D-native generative model with spatiotemporal reasoning abilities, allowing the model to not only understand robot movement but also to flexibly predict its physical effects on the environment for high-fidelity simulation. 

## **3 Our Approach** 

Fig. 2 illustrates our architecture, composed of two components: Kinematic Control (Sec. 3.1) and 4D Generative Modeling (Sec. 3.2). 

### **3.1 Kinematics Control** 

The core of our framework lies in transforming abstract robot actions into a precise 4D representation, via a progressive process. 

6 Xu et al. 


**Fig. 2: Overview of our** **_Kinema4D_** . **_1) Kinematics Control_** : Given a 3D robot with its URDF at initial canonical setup space, and an action sequence, we drive the 3D robot via kinematics to produce a 4D robot trajectory, which is then projected into a pointmap sequence. This process re-represents raw actions as a spatiotemporal visual signal. **_2) 4D Generative Modeling_** : This signal and the initial main-view world image are sent to a shared VAE encoder, then fused with an occupancy-aligned robot mask and noise, which are denoised by a Diffusion Transformer [56] to generate a full future 4D (pointmap+RGB) world sequence. 

_3D robot asset acquisition._ To ground the robot in 4D space, we first establish its geometric entity. For standardized robots, we utilize factory-provided 3D CAD meshes. For unknown platforms, we implement a reconstruction pipeline: 

We first capture orbital videos of the robot and sample representative frames, then employ Grounded-SAM2 [47,58] to segment the robot in the initial frame using a robust prompt ( _e.g_ ., `“the robot arm”` ), followed by SAM2 [58] to propagate masks across the sequence via video tracking. Next, given the masked multiview images, we leverage ReconViaGen [11] to recover a high-quality textured robot mesh _Crecon_ in under one minute. This pipeline facilitates the efficient acquisition of our 3D asset library for diverse robotic configurations. To enable articulation, we establish a digital twin alignment: the joint anchor points from the robot’s URDF model _M_ are mapped to their corresponding coordinates of _Crecon_ within the canonical reconstruction space. This ensures that the analytical kinematic chain can directly drive the reconstructed mesh segments. 

_Kinematics-driven 4D robot trajectory expansion._ Given the aligned robot model _M_ within _Crecon_ , we transform input actions **a** 1: _T_ into full-body 4D trajectories. Our framework handles two primary control modalities: 

- _End-effector control_ . When actions are provided as Cartesian poses _{_ **T** _ee,t}t_<sup>_T_</sup> =1<sup>,</sup> we employ an Inverse Kinematics (IK) solver to resolve the joint configurations at time _t_ : **q** _t_ = IK( **T** _ee,t,_ **q** _t−_ 1 _, M_ ), where the previous state **q** _t−_ 1 serves as the seed to ensure temporal smoothness and prevent joint-space flipping. 

- _Joint-space control_ . When actions are directly provided as joint angles or velocities, **q** _t_ is obtained via direct mapping or integration. For each time _t_ , we perform Forward Kinematics (FK) to compute the 6-DoF 

- poses for all _K_ links within the reconstruction space: _{_ **T**<sup>_recon_</sup> _k,t }_<sup>_K_</sup> _k_ =1<sup>= FK(</sup><sup>**q**</sup><sup>_t, M_).</sup> 

_Spatial-visual projection._ We select a primary viewpoint—typically a medialfrontal perspective—for projection and later generation, as single-view robot demonstration data is extensively accessible to ensure training scalability and 

Kinema4D 7 

diversity. To place the articulated robot within the initial main-view world image _I_ 0, we utilize the extrinsic camera transformation **T**<sup>_cam_</sup> _recon_<sup>_∈SE_(3)ofthese-</sup> lected main view, which is derived during the previous 3D robot reconstruction phase [11]. With the camera transformation **T**<sup>_cam_</sup> _recon_<sup>andthepreviouslycom-</sup> puted link poses _{_ **T**<sup>_recon_</sup> _k,t }_ within the reconstruction space, the full-body trajectory is projected onto the image plane to generate the 4D robot pointmap **M** 1: _T ∈_ R<sup>_H×W ×_3</sup> . For any point **x** on the surface of link _k_ , its projected pixel coordinates ( _u, v_ ) and depth _z_ are determined by: 


where **K** is the camera intrinsic matrix. The resulting pointmap **M** 1: _T_ is pixelaligned with the RGB grid, while its pixel values store the camera-space ( _x, y, z_ ) coordinates. This transformation precisely maps the 4D robot trajectory from the canonical reconstruction space into the target camera coordinate system, ensuring that the robot occupancy is spatially consistent with the environmental background. Optionally, we project the textured trajectory to RGB sequence. 

Tab. 4 ablates the robustness to the noisy pointmap. More details of our reconstruction and projection are provided in the supplementary material. 

### **3.2 4D Generative Modeling** 

Next, we utilize a 4D diffusion model to focus on synthesizing the environment’s reactive dynamics in response to the robot control signal. 

_Preliminary: Latent Video Diffusion._ We build our framework upon Latent Diffusion Models (LDM) [60], extending them to the 4D spatiotemporal domain. Instead of pixel-space denoising, the model operates on a compressed latent space _Z_ provided by a pre-trained VAE. A video sequence **V** 1: _T_ is encoded into a latent tensor **z** 0 _∈_ R<sup>_T ×C×H×W_</sup> . The diffusion process learns to generate this latent sequence by optimizing a conditional denoising objective: 


where **z** _τ_ is the noisy latent at diffusion step _τ_ , and _ϵθ_ is typically a SpatioTemporal Transformer ( _e.g_ ., DiT [56]) that models dependencies across both frames and pixels. The condition **c** guides the denoising process to ensure the generated video adheres to specific inputs. 

_Multi-modal latent construction._ To prepare the multi-modal input for our generative backbone, we first align the temporal dimensions of the initially captured RGB world image _I_ 0 and the robotic control signals. Specifically, _I_ 0 is extended along the temporal axis via zero-padding or by concatenating the previously robot RGB sequence. Next, following the data formatting strategy in 4DNex [15], we concatenate this input with the previously produced robot pointmap sequence **M**<sup>_robot_</sup> 1: _T_ along the width dimension. This unified spatiotemporal signal is then processed by a shared VAE to obtain input latents, which maps the heterogeneous inputs—RGB and pointmap—into a synchronized latent representation. 

8 Xu et al. 

To further enforce pixel-level control, we introduce a guided mask **m** _∈ {_ 0 _,_ 1 _}_<sup>_T ×H×W_</sup> , where **m** _t,i,j_ = 1 indicates the spatial occupancy of the robot (derived from **M**<sup>_robot_</sup> 1: _T_<sup>)and0indicatestheareatobegenerated.Inpractice,</sup> rather than employing a binary hard-mask, we implement a soft strategy by setting the value of 10% occupied regions to 0 _._ 5 (ablated in Tab. 4). This design choice ensures that the generative model retains the capacity to _refine_ the robot’s visual signal. By doing so, we mitigate the impact of noise introduced during the previous phase, enhancing the structural robustness and visual coherence. 

We concatenate input latents, noisy latents, and robot masks channel-wise. This fused input ensures that the generative model focuses exclusively on synthesizing the environment’s reactive dynamics while _strictly adhering to the robot’s trajectory_ . 

_4D-aware joint modeling._ Our backbone is a Diffusion Transformer [56] that predicts synchronized RGB and pointmap sequences. To preserve pixel-wise alignment across these modalities, we adopt a shared Rotary Positional Encoding (RoPE) [64] across both RGB and pointmap latents. Additionally, following 4DNex [15], we distinguish these domains using learnable domain embeddings. These embeddings act as modality-specific signatures, allowing the Transformer to perform cross-modal reasoning—effectively using the robot pointmap as geometric anchors to guide the synthesis of the RGB environmental response. 

_4D sequence synthesis._ The denoised latents are processed by the shared VAE Decoder to reconstruct the full-world pointmap/RGB sequence. By predicting the environment’s pointmap **M**<sup>_world_</sup> 1: _T_ , the model produces a simulation that is not only visually realistic but also geometrically rigorous, ultimately yielding a 4D world where every pixel’s depth and motion are grounded in 3D space. 

_Underlying insight._ By jointly modeling RGB and pointmap latents, the generative process is transformed into a spatiotemporal reasoning task. The model does not merely “draw” pixels; it must resolve the 3D occupancy and deformations of the world that are consistent with the robot’s movement. 

### **3.3 Robo4D-200k: A Large-Scale 4D Robotic Dataset** 

_Data preparation._ To facilitate the training of Kinema4D, a large-scale dataset is a prerequisite. To begin with, we aggregate 2D RGB video streams from leading real-world robotic demonstration repositories, including DROID [38], Bridge [68], and RT-1 [6]. We further incorporate the LIBERO [45] platform to synthesize an extensive array of both successful executions and critical failure modes. 

_4D annotation._ A significant challenge lies in lifting the raw 2D RGB videos from real-world datasets into the 4D metric space required for our joint generative modeling. We extensively tried several state-of-the-art 3D/4D reconstruction frameworks, including MonST3R [86], MegaSaM [42], VGGT/VGGT4D [31,70], ViPE [32], and ST-V2 [75]. ST-V2 [75] yields the most robust and temporally 

Kinema4D 9 


**Fig. 3: Samples from our** **_Robo4D-200k_ dataset** . Our dataset provides a comprehensive data foundation by aggregating diverse real-world demonstrations, including DROID [38], Bridge [68], and RT-1 [6]. We further incorporate the LIBERO [45] to synthesize a vast array of successful/failure cases. Each episode captures a _complete_ robot-world interaction ( _e.g_ ., pick-and-place)—providing the continuous information necessary for robust reasoning. The 4D point clouds viewed from various camera frustums are shown here, demonstrating the spatial precision of our pseudo-annotations. 

consistent pointmap sequences, particularly for robot manipulations involving rapid motion. It is used to reconstruct high-quality, pixel-aligned 4D trajectories for real datasets. For synthetic data from LIBERO, we directly leverage the native, noise-free depth parameters to ensure absolute ground-truth precision. 

_Dataset curation._ To ensure the quality of the generative simulation, we performed a rigorous data curation process. We applied a manual verification to prune low-quality captures and reconstruction artifacts. For very-long demonstrations, we applied uniform temporal downsampling to yield 49-frame sequences per episode; this ensures consistent motion frequencies across the dataset. Each curated episode captures a complete/contiguous spatiotemporal interaction ( _e.g_ ., a full pick-and-place cycle), providing the long-term dependencies necessary for robust physical reasoning. Following this pipeline, we established _Robo4D-200k_ , which—to our knowledge—represents the largest-scale 4D robot-interaction dataset. Comprising 201,426 high-fidelity episodes, Robo4D200k provides the unprecedented data volume and interaction diversity required to train foundation models with spatiotemporal and physical awareness. More details of our dataset can be found in the supplementary material. 

## **4 Experiments** 

### **4.1 Setting** 

_Implementation Details._ We build our framework upon the WAN 2.1 [69] base model (14B parameters), utilizing the 4D-aware pre-trained weights from 4DNex [15]. Given the substantial scale of the backbone, we employ Low-Rank Adaptation (LoRA) [30] for parameter-efficient fine-tuning. This allows us to inject domain-specific robotic dynamics into the Diffusion Transformer [56] while preserving the powerful generative priors of the base model. While the original WAN 2.1 includes a text encoder, we intentionally replace the text embedding with 

10 Xu et al. 

**Table 1: Quantitative comparison of video generation metrics** . _↑_ and _↓_ respectively indicates higher and lower is better. **xxx** denotes the best and <u>xxx</u> indicates the 2nd-best. “Action” means the representation of robot controls, where “Emb.” is token embedding. “Output” represents the modality of generation output. 

|**Method**|**Action**|**Output**|**PSNR**_↑_|**SSIM**_↑_|**L2**_latent↓_|**FID**_↓_|**FVD**_↓_|**LPIPS**_↓_|
|---|---|---|---|---|---|---|---|---|
|UniSim [ICLR’24] [78]|Text|RGB|19.32|0.681|0.2120|32.3|153.2|0.175|
|IRA-Sim [ICCV’25] [91]|Emb.|RGB|20.21|0.813|0.1722|25.2|126.0|0.135|
|Cosmos [arXiv’25] [2]|Emb.|RGB|20.39|0.787|0.1935|27.1|113.4|0.110|
|EVAC [arXiv’25] [37]|Emb.+2D|RGB|20.88|0.832|0.1896|29.3|122.0|0.150|
|ORV [CVPR’26] [80]|Emb.+3D|RGB|19.45|0.790|0.2002|30.1|130.1|0.143|
|Ctrl-World [ICLR’26] [23]|Emb.|RGB|21.03|0.803|0.1533|**24.9**|112.8|0.122|
|TesserAct [ICCV’25] [89]|Text|4D|19.35|0.766|0.1911|29.5|120.3|0.158|
|**Ours**|**4D**|**4D**|**22.50**|**0.864**|**0.1380**|25.2|**98.5**|0.105|


**Table 2: Quantitative comparison of geometric metrics** . “(temp)” denotes the self-temporal consistency across frames. The threshold of F-Score is set to @0.01. 

|**Method**|**CD-**_L_1_↓_|**CD-**_L_1 **(temp)**_↓_|**CD-**_L_2_↓_|**CD-**_L_2 **(temp)**_↓_|**F-Score**_↑_|**F-Score (temp)**_↑_|
|---|---|---|---|---|---|---|
|TesserAct [ICCV’25] [89]|0.0836|**0.0067**|0.0130|0.0008|0.2896|0.9523|
|**Ours**|**0.0479**|0.0074|**0.0077**|**0.0002**|**0.4733**|**0.9686**|


the VAE latents of robot sequences. By omitting high-level instructions, we force the network to decouple visual synthesis from semantic ambiguity and focus on the precise execution of action controls. For all other configurations, we follow the protocol established in the official 4DNex implementation. 

We curated a stratified benchmark suite comprising 2% of our Robo4D-200k dataset for the validation. More implementation details, ablations of text embeddings, and benchmark details are provided in the supplementary material. 

_Baselines._ We benchmark our method against a diverse set of state-of-the-art generative embodied simulators with different action-conditioning strategies and output modalities. UniSim [78] pioneered the generative simulator by synthesizing visual outcomes from text instructions. IRASim [91], Cosmos [2], and CtrlWorld [23] utilize adaptive layers to inject robot-specific action embeddings. EVAC [37] and ORV [80] introduce auxiliary cues, such as 2D angle arrows and 3D environmental occupancy grids. While most predecessors generate pure RGB video, TesserAct [89] represents the current frontier by outputting 4D signals (RGB, depth, and surface normals), though it remains limited by its reliance on coarse language instructions. As the field in its infancy, we prioritize models with open-sourced implementations to ensure a fair comparison. 

_Metrics._ To compare with the methods that output RGB videos, we use two types of metrics: computation-based (PSNR [29], SSIM [72]) and model-based (Latent L2 loss, FID [26], FVD [57] and LPIPS [88]). As both TesserAct and our method output 4D videos, we additionally measure geometric metrics, including Chamfer Distance and F-Score@0.01, considering both the accuracy with the Ground Truth and the temporal consistency across frames (indicated by “temp”). 

### **4.2 Main Results** 

_Quantitative results._ The quantitative evaluation of video synthesis quality is summarized in Tab. 1. Our Kinema4D is uniquely characterized by its ability to 

Kinema4D 11 


**Fig. 4: Qualitative comparison of 2D video synthesis** between our Kinema4D and Ctrl-World [23]. Our method achieves superior fidelity. In contrast, Ctrl-World exhibits distorted actions and unrealistic environmental transitions. 


**Fig. 5: 4D qualitative comparison between our Kinema4D and TesserAct [89]** . Unlike TesserAct that hallucinate outcomes, our Kinema4D precisely reflects Ground-Truth executions, including “near-miss” failure cases. For example, in the bottom left corner example, our model _correctly interprets the spatial gap_ between the gripper and the plant, _even when their_ **_RGB textures overlap in 2D views_** . 

precisely represent actions and synthesize outcomes within a unified 4D space. This advantage allows our framework to achieve either the leading or secondbest performance across all metrics. The geometric fidelity of the generated 4D sequences is detailed in Tab. 2. While TesserAct [89] exhibits slightly better performance in temporal CD- _L_ 1, our approach outperforms TesserAct across all other metrics. When evaluated against absolute ground-truth rather than mere self-consistency, our method shows a significant margin of superiority. 

12 Xu et al. 

_Qualitative results._ We compare our method with the best baseline that output 2D videos ( _i.e_ ., Ctrl-World [23]), focusing on the qualitative results under 2D video modality. As shown in Fig. 4, our Kinema4D demonstrates a superior ability to synthesize high-fidelity sequences that strictly adhere to input action trajectories while generating physically consistent environmental responses that are highly similar to the ground truth. In contrast, as Ctrl-World is limited to 2D video synthesis and relies on implicit robot embeddings, it often produces distorted robot kinematics and unrealistic environmental changes. 

In Fig. 5, we present a 4D qualitative comparison between our framework and TesserAct [89]. As TesserAct relies on text instructions, it struggles to align with the actual robot actions, and often yields incorrect environmental outcomes. Instead, by utilizing precise 4D controls, our Kinema4D demonstrates the ability to simulate **_both successful_** _rollouts and_ **_subtle execution failures_** . **_Most notably_** , even when the RGB textures of the gripper and the object appear to “contact” from a 2D perspective, our 4D-aware framework correctly interprets the spatial gap and simulates a ‘near-miss’ or a failed grasp. More animated results are presented in the supplementary material. 

### **4.3 Policy Evaluation** 

We investigate the utility of our Kinema4D as a high-fidelity tool for evaluating robotic policies—if the simulator can accurately simulating realistic outcomes of executing a policy’s rollout. We deploy our evaluation across both standardized simulation platforms (noise-free) and real-world (complex physics) environments. 

_Setup and implementations._ In the simulation platform, we execute a Diffusion Policy [17] within the LIBERO [45] to generate a sequence of action rollouts, then synthesize the environmental outcomes using our Kinema4D. Since the robot mesh and camera rendering are integrated within the platform, we can easily get the robot pointmap without any reconstruction or calibration, showing the simplicity of deploying our Kinematic Control in the simulation platform. By leveraging native simulation parameters, this evaluation protocol isolates external noise and establishes a standard setup, ensuring that the benchmarking of future methods is conducted under a strictly equitable framework. 

As for real-world evaluation, we deploy a physical robot setup in a laboratory environment to evaluate the zero-shot generalization of our framework. We execute a Diffusion Policy [17] on the hardware to provide rollouts. Next, we follow the reconstruction pipeline described in Sec. 3.1 to get the robot pointmap and then synthesize the resulting world transitions. Notably, our experiments are conducted **_without_** _any fine-tuning on real-world data_ ; the physical environment remains _entirely_ **_out-of-distribution_** _(OOD)_ . Unlike existing simulators rely on real-world finetuning [91], or use the real-world setup same with training data [23], we represent the **_first-time_** evaluation of a embodied world model under rigorous OOD conditions. We omit qualitative comparisons with baselines here, as their performance degrades significantly. For both the simulation and real-world evaluation, we set 3 different evaluation scenarios with 50 runs each. 

Kinema4D 13 

**Table 3:** Policy evaluation of actual pick&place under 3 different setups of both simulation platform and real-world (zero-shot OOD) environment. “Ground Truth” denotes the actual execution, “Ours” indicates our simulation, and “Diff” is their difference. 

|**Evaluator**|Si|mulatio|n|Real-|world|(OOD)|
|---|---|---|---|---|---|---|
||1|2|3|1|2|3|
|Ground Truth|0.48|0.38|0.80|0.34|0.46|0.78|
|Ours|0.56|0.46|0.84|0.60|0.76|0.90|
|Diff|0.08|0.08|0.04|0.26|0.30|0.12|


**Fig. 6: Qualitative comparison between real-world Ground Truth (GT) and our method for zero-shot OOD evaluation** . To intuitively compare with GT, we also reconstruct the GT using [75] and present both 4D and 2D results. Our results strongly align with real outcomes, accurately synthesizing both successful rollouts and “near-miss” failures. For instance, in the right figure, our model _correctly interprets the spatial gap_ between the gripper and the cube, _even when their_ **_RGB textures overlap in 2D views_** . Besides, the _noisy_ robot pointmap produced by our reconstruction pipeline is shown, proving the robustness of our framework. 

_Results._ The quantitative success rates are summarized in Tab. 3. Within the simulation platform, our framework achieves a success rate closely aligned with the ground truth. Since our training data includes LIBERO-produced data, this proves that our method effectively captures the in-domain knowledge. In the realworld (OOD) evaluation, while we observe _a comparatively wider gap_ between our simulated and actual results, the discrepancy _remains within a reasonable margin_ . This suggests the challenges of zero-shot transfer. Moreover, the success rates synthesized by our model are higher than actual executions, highlighting that simulating complex failure modes remains more challenging. 

The qualitative performance in real-world environments is illustrated in Fig. 6, highlighting our two critical strengths: **i)** Consistent with Fig. 5, even in scenarios where the 2D RGB textures of the gripper and object overlap, our Kinema4D correctly interprets the spatial gap and synthesizes ‘near-miss’ failures. **ii)** We also visualize the robot pointmaps produced by our real-world reconstruction pipeline (Sec. 3.1). Despite the presence of noisy artifacts, our model refines these irregularities to produce coherent and physically plausible videos. This shows the robustness and real-world deployability of our kinematiccontrolled framework. Due to the space limit, the qualitative results of simulation and more details of our evaluation are presented in the supplementary material. 

14 Xu et al. 

**Table 4:** Quantitative results of ablation studies. 

|Metrics|Ours|text|binary|emb.|RGB<br>|RGB+pm|single|2D-out|w/o mask|0%|20%|50%|70%|remove|gaus.|trans.|rot.|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**PSNR**_↑_|22.50|19.89|21.47|20.89|21.53|**22.98**|21.26|20.07|21.03|21.10|22.04|21.75|21.83|22.48|21.98|21.87|22.34|
|**FID**_↓_|25.2|28.8|27.5|26.3|25.8|25.7|26.7|27.4|26.8|26.1|25.2|**25.0**|26.0|26.0|25.3|25.6|26.3|
|**CD-**_L_1_↓_|0.0479|0.0750|0.0639|0.0528|0.0677|0.0495|0.0581|0.0712|0.0510|0.0528|**0.0433**|0.0455|0.0463|0.0499|0.0501|0.0513|0.0483|


### **4.4 Ablation Studies and Analysis** 

We provide comprehensive ablation analysis and report results in Tab. 4. 

_Different representations of robot controls._ We replace our robot pointmap conditions with other types of robot control representations, including text instructions (“text”), robot binary masks (“binary”), token embeddings (“emb.”), robot RGB (“RGB”) and robot RGB+pointmap (“RGB+pm”) sequence. Our pointmap representation yields the 2nd-best results. Interestingly, using RGB+pointmap sequence yields marginal improvements, as RGB data potentially introduces more noise and overfitting risks. Instead, pointmap already captures the essential spatial information required for precise control. 

_Embodiment-agnostic modeling enables scalable training._ Unlike raw action vectors that are sensitive to embodiment morphology, our pointmap-based control enables embodiment-agnostic modeling by decoupling kinematic intent from specific hardware configurations. To validate this, we compare our mixed-dataset training against a single-domain baseline trained and tested exclusively on Droid [38]. The baseline (“single”) exhibited degraded performance. This confirms that our approach effectively leverages data diversity to enhance generalization, demonstrating a significant _scaling advantage_ over domain-specific modeling. 

_Why not generate RGB videos first, then reconstruct?_ We trained our method to purely output RGB videos (no pointmap, “2D-out”) and then reconstruct the produced RGB videos using ST-v2 [75]. This significantly degrades the performance, proving the necessity of 4D awareness throughout the generative process. 

_The robot mask map._ As in Sec. 3.2, we introduced a robot occupancy mask and softly set 10% occupied regions to 0.5. Here we trained our method without robot mask or using different soft mask ratio. Our method performs stably well under different ratios, yet discarding the mask or setting 0% regions to 0.5 degrades the performance, showing the necessity of generative refinement. 

_The robustness to the robot pointmap noise._ We disturb the produced robot pointmap by randomly removing (5%), adding gaussian noise (“gaus.”), translating ( _±_ 5 pixel coordinates, “trans.”) and rotating ( _±_ 5<sup>_◦_</sup> , “rot.”). Our framework is robust to the noise of robot pointmap control, potentially due to the prior of the initial world image and the refinement of generative modeling. 

Kinema4D 15 

## **5 Conclusion** 

We presented Kinema4D, a novel framework that shifts the paradigm of robotic simulation to 4D spatial-temporal reasoning. By integrating a kinematics-driven grounding stage with a diffusion transformer-based generative pipeline, we effectively decouple deterministic robot motion from stochastic environmental reactions. Experimental results demonstrate that Kinema4D can generalize to simulate diverse real-world dynamics. By providing a 4D world, Kinema4D paves the way for scalable, high-fidelity, and complex embodied simulations. 

_Limitations._ Since the environmental dynamics are learned through statistical synthesis rather than governed by explicit physical constraints (such as rigidbody dynamics or friction coefficients), our method may occasionally produce behaviors that violate conservation laws or exhibit penetration artifacts, leaving a future research direction of incorporating physical laws into our model. 

16 Xu et al. 

## **References** 

1. Abou-Chakra, J., Rana, K., Dayoub, F., Suenderhauf, N.: Physically embodied gaussian splatting: A realtime correctable world model for robotics. In: CoRL (2024) 

2. Agarwal, N., Ali, A., Bala, M., Balaji, Y., Barker, E., Cai, T., Chattopadhyay, P., Chen, Y., Cui, Y., Ding, Y., et al.: Cosmos world foundation model platform for physical ai. arXiv preprint arXiv:2501.03575 (2025) 

3. Allen, J.F., Koomen, J.A.: Planning using a temporal world model. In: IJCAI (1983) 

4. Assran, M., Bardes, A., Fan, D., Garrido, Q., Howes, R., Muckley, M., Rizvi, A., Roberts, C., Sinha, K., Zholus, A., et al.: V-jepa 2: Self-supervised video models enable understanding, prediction and planning. arXiv preprint arXiv:2506.09985 (2025) 

5. Bai, S., Cai, Y., Chen, R., Chen, K., Chen, X., Cheng, Z., Deng, L., Ding, W., Gao, C., Ge, C., Ge, W., Guo, Z., Huang, Q., Huang, J., Huang, F., Hui, B., Jiang, S., Li, Z., Li, M., Li, M., Li, K., Lin, Z., Lin, J., Liu, X., Liu, J., Liu, C., Liu, Y., Liu, D., Liu, S., Lu, D., Luo, R., Lv, C., Men, R., Meng, L., Ren, X., Ren, X., Song, S., Sun, Y., Tang, J., Tu, J., Wan, J., Wang, P., Wang, P., Wang, Q., Wang, Y., Xie, T., Xu, Y., Xu, H., Xu, J., Yang, Z., Yang, M., Yang, J., Yang, A., Yu, B., Zhang, F., Zhang, H., Zhang, X., Zheng, B., Zhong, H., Zhou, J., Zhou, F., Zhou, J., Zhu, Y., Zhu, K.: Qwen3-vl technical report. arXiv preprint arXiv:2511.21631 (2025) 

6. Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., Ibarz, J., Ichter, B., Irpan, A., Jackson, T., Jesmonth, S., Joshi, N., Julian, R., Kalashnikov, D., Kuang, Y., Leal, I., Lee, K.H., Levine, S., Lu, Y., Malla, U., Manjunath, D., Mordatch, I., Nachum, O., Parada, C., Peralta, J., Perez, E., Pertsch, K., Quiambao, J., Rao, K., Ryoo, M., Salazar, G., Sanketi, P., Sayed, K., Singh, J., Sontakke, S., Stone, A., Tan, C., Tran, H., Vanhoucke, V., Vega, S., Vuong, Q., Xia, F., Xiao, T., Xu, P., Xu, S., Yu, T., Zitkovich, B.: Rt-1: Robotics transformer for real-world control at scale. arXiv preprint arXiv:2212.06817 (2022) 

7. Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al.: Rt-1: Robotics transformer for real-world control at scale. arXiv preprint arXiv:2212.06817 (2022) 

8. Bruce, J., Dennis, M.D., Edwards, A., Parker-Holder, J., Shi, Y., Hughes, E., Lai, M., Mavalankar, A., Steigerwald, R., Apps, C., et al.: Genie: Generative interactive environments. In: ICML (2024) 

9. Cen, J., Huang, S., Yuan, Y., Li, K., Yuan, H., Yu, C., Jiang, Y., Guo, J., Li, X., Luo, H., et al.: Rynnvla-002: A unified vision-language-action and world model. arXiv preprint arXiv:2511.17502 (2025) 

10. Cen, J., Yu, C., Yuan, H., Jiang, Y., Huang, S., Guo, J., Li, X., Song, Y., Luo, H., Wang, F., et al.: Worldvla: Towards autoregressive action world model. arXiv preprint arXiv:2506.21539 (2025) 

11. Chang, J., Ye, C., Wu, Y., Chen, Y., Zhang, Y., Luo, Z., Li, C., Zhi, Y., Han, X.: Reconviagen: Towards accurate multi-view 3d object reconstruction via generation. arXiv preprint arXiv:2510.23306 (2025) 

12. Chefer, H., Singer, U., Zohar, A., Kirstain, Y., Polyak, A., Taigman, Y., Wolf, L., Sheynin, S.: Videojam: Joint appearance-motion representations for enhanced motion generation in video models. In: ICML (2025) 

Kinema4D 17 

13. Chen, H., Wang, B., Guo, J., Zhang, T., Hou, Y., Huang, X., Tie, C., Shao, L.: World4omni: a zero-shot framework from image generation world model to robotic manipulation. arXiv preprint arXiv:2506.23919 (2025) 

14. Chen, Y., Li, P., Yang, J., He, K., Wu, X., Xu, Y., Wang, K., Liu, J., Liu, N., Huang, Y., Wang, L.: Bridgev2w: Bridging video generation models to embodied world models via embodiment masks. arXiv preprint arXiv:2602.03793 (2026) 

15. Chen, Z., Liu, T., Zhuo, L., Ren, J., Tao, Z., Zhu, H., Hong, F., Pan, L., Liu, Z.: 4dnex: Feed-forward 4d generative modeling made easy. arXiv preprint arXiv:2508.13154 (2025) 

16. Chen, Z., Walsman, A., Memmel, M., Mo, K., Fang, A., Vemuri, K., Wu, A., Fox, D., Gupta, A.: Urdformer: A pipeline for constructing articulated simulation environments from real-world images. arXiv preprint arXiv:2405.11656 (2024) 

17. Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., Song, S.: Diffusion policy: Visuomotor policy learning via action diffusion. IJRR (2025) 

18. Ebert, F., Finn, C., Dasari, S., Xie, A., Lee, A., Levine, S.: Visual foresight: Modelbased deep reinforcement learning for vision-based robotic control. arXiv preprint arXiv:1812.00568 (2018) 

19. Erez, T., Tassa, Y., Todorov, E.: Simulation tools for model-based robotics: Comparison of bullet, havok, mujoco, ode and physx. In: ICRA (2015) 

20. Fu, X., Wang, X., Liu, X., Bai, J., Xu, R., Wan, P., Zhang, D., Lin, D.: Learning video generation for robotic manipulation with collaborative trajectory control. In: ICLR (2026) 

21. Gao, S., Liang, W., Zheng, K., Malik, A., Ye, S., Yu, S., Tseng, W.C., Dong, Y., Mo, K., Lin, C.H., et al.: Dreamdojo: A generalist robot world model from large-scale human videos. arXiv preprint arXiv:2602.06949 (2026) 

22. Gu, Z., Yan, R., Lu, J., Li, P., Dou, Z., Si, C., Dong, Z., Liu, Q., Lin, C., Liu, Z., et al.: Diffusion as shader: 3d-aware video diffusion for versatile video generation control. In: SIGGRAPH (2025) 

23. Guo, Y., Shi, L.X., Chen, J., Finn, C.: Ctrl-world: A controllable generative world model for robot manipulation. In: ICLR (2026) 

24. Ha, D., Schmidhuber, J.: World models. arXiv preprint arXiv:1803.10122 (2018) 25. Han, X., Liu, M., Chen, Y., Yu, J., Lyu, X., Tian, Y., Wang, B., Zhang, W., Pang, J.: Generating high-fidelity simulation data via 3d-photorealistic real-to-sim for robotic manipulation. arXiv preprint arXiv:2502.08645 (2025) 

26. Heusel, M., Ramsauer, H., Unterthiner, T., Nessler, B., Hochreiter, S.: Gans trained by a two time-scale update rule converge to a local nash equilibrium. In: NeurIPS (2017) 

27. Ho, J., Jain, A., Abbeel, P.: Denoising diffusion probabilistic models. In: NeurIPS (2020) 

28. Hong, W., Ding, M., Zheng, W., Liu, X., Tang, J.: Cogvideo: Large-scale pretraining for text-to-video generation via transformers. arXiv preprint arXiv:2205.15868 (2022) 

29. Hore, A., Ziou, D.: Image quality metrics: Psnr vs. ssim. In: ICPR (2010) 30. Hu, E.J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., Chen, W., et al.: Lora: Low-rank adaptation of large language models. In: ICLR (2022) 

31. Hu, Y., Cheng, C., Yu, S., Guo, X., Wang, H.: Vggt4d: Mining motion cues in visual geometry transformers for 4d scene reconstruction. arXiv preprint arxiv:2511.19971 (2025) 

32. Huang, J., Zhou, Q., Rabeti, H., Korovko, A., Ling, H., Ren, X., Shen, T., Gao, J., Slepichev, D., Lin, C.H., Ren, J., Xie, K., Biswas, J., Leal-Taixe, L., Fidler, 

18 Xu et al. 

- S.: Vipe: Video pose engine for 3d geometric perception. In: NVIDIA Research Whitepapers arXiv:2508.10934 (2025) 

- 33. Huang, S., Chen, Q., Zhang, X., Sun, J., Schwager, M.: Particleformer: A 3d point cloud world model for multi-object, multi-material robotic manipulation. In: CoRL (2025) 

- 34. Huang, W., Chao, Y.W., Mousavian, A., Liu, M.Y., Fox, D., Mo, K., Fei-Fei, L.: Pointworld: Scaling 3d world models for in-the-wild robotic manipulation. arXiv preprint arXiv:2601.03782 (2026) 

- 35. Huang, Y., Zhang, J., Zou, S., Liu, X., Hu, R., Xu, K.: Ladi-wm: A latent diffusionbased world model for predictive manipulation. arXiv preprint arXiv:2505.11528 (2025) 

- 36. Jiang, G., Chang, H., Qiu, R.Z., Liang, Y., Ji, M., Zhu, J., Dong, Z., Zou, X., Wang, X.: Gsworld: Closed-loop photo-realistic simulation suite for robotic manipulation. arXiv preprint arXiv:2510.20813 (2025) 

- 37. Jiang, Y., Chen, S., Huang, S., Chen, L., Zhou, P., Liao, Y., He, X., Liu, C., Li, H., Yao, M., et al.: Enerverse-ac: Envisioning embodied environments with action condition. arXiv preprint arXiv:2505.09723 (2025) 

- 38. Khazatsky, A., Pertsch, K., Nair, S., Balakrishna, A., Dasari, S., et al.: DROID: A large-scale in-the-wild robot manipulation dataset. In: RSS 2024 Workshop: Data Generation for Robotics (2024) 

- 39. Kim, M., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., Vuong, Q., Kollar, T., Burchfiel, B., Tedrake, R., Sadigh, D., Levine, S., Liang, P., Finn, C.: Openvla: An open-source visionlanguage-action model. arXiv preprint arXiv:2406.09246 (2024) 

- 40. Li, X., Li, J., Zhang, Z., Zhang, R., Jia, F., Wang, T., Fan, H., Tseng, K.K., Wang, R.: Robogsim: A real2sim2real robotic gaussian splatting simulator. arXiv preprint arXiv:2411.11839 (2024) 

- 41. Li, X., Hsu, K., Gu, J., Mees, O., Pertsch, K., Walke, H.R., Fu, C., Lunawat, I., Sieh, I., Kirmani, S., Levine, S., Wu, J., Finn, C., Su, H., Vuong, Q., Xiao, T.: Evaluating real-world robot manipulation policies in simulation. In: CORL (2024) 

- 42. Li, Z., Tucker, R., Cole, F., Wang, Q., Jin, L., Ye, V., Kanazawa, A., Holynski, A., Snavely, N.: MegaSaM: Accurate, fast and robust structure and motion from casual dynamic videos. In: CVPR (2025) 

- 43. Liang, H., Cao, J., Goel, V., Qian, G., Korolev, S., Terzopoulos, D., Plataniotis, K.N., Tulyakov, S., Ren, J.: Wonderland: Navigating 3d scenes from a single image. In: CVPR (2025) 

- 44. Liao, Y., Zhou, P., Huang, S., Yang, D., Chen, S., Jiang, Y., Hu, Y., Liu, S., Luo, J., Chen, L., YAN, S., Yao, M., Ren, G.: Genie envisioner: A unified world foundation platform for robotic manipulation. In: ICLR (2026) 

- 45. Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., Stone, P.: Libero: Benchmarking knowledge transfer for lifelong robot learning. In: NeurIPS (2023) 

- 46. Liu, M., Zhu, Z., Han, X., Hu, P., Lin, H., Li, X., Chen, J., Xu, J., Yang, Y., Lin, Y., et al.: Manipulation as in simulation: Enabling accurate geometry perception in robots. arXiv preprint arXiv:2509.02530 (2025) 

47. Liu, S., Zeng, Z., Ren, T., Li, F., Zhang, H., Yang, J., Li, C., Yang, J., Su, H., Zhu, J., et al.: Grounding dino: Marrying dino with grounded pre-training for open-set object detection. arXiv preprint arXiv:2303.05499 (2023) 

48. Liu, Z., Li, S., Cousineau, E., Feng, S., Burchfiel, B., Song, S.: Geometry-aware 4d video generation for robot manipulation. In: ICLR (2026) 

49. Lu, G., Jia, B., Li, P., Chen, Y., Wang, Z., Tang, Y., Huang, S.: Gwm: Towards scalable gaussian world models for robotic manipulation. In: ICCV (2025) 

- Kinema4D 19 

- 50. Luo, H., Lu, Z.: Learning video-conditioned policy on unlabelled data with joint embedding predictive transformer. In: ICLR (2025) 

- 51. Makoviychuk, V., Wawrzyniak, L., Guo, Y., Lu, M., Storey, K., Macklin, M., Hoeller, D., Rudin, N., Allshire, A., Handa, A., et al.: Isaac gym: High performance gpu-based physics simulation for robot learning. arXiv preprint arXiv:2108.10470 (2021) 

- 52. Mittal, M., Yu, C., Yu, Q., Liu, J., Rudin, N., Hoeller, D., Yuan, J.L., Singh, R., Guo, Y., Mazhar, H., et al.: Orbit: A unified simulation framework for interactive robot learning environments. IRAL (2023) 

- 53. Mu, Y., Chen, T., Chen, Z., Peng, S., Lan, Z., Gao, Z., Liang, Z., Yu, Q., Zou, Y., Xu, M., Lin, L., Xie, Z., Ding, M., Luo, P.: Robotwin: Dual-arm robot benchmark with generative digital twins. In: CVPR (2025) 

- 54. O’Neill, A., Rehman, A., Maddukuri, A., Gupta, A., Padalkar, A., Lee, A., Pooley, A., Gupta, A., Mandlekar, A., Jain, A., et al.: Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In: ICRA (2024) 

- 55. Pashevich, A., Strudel, R., Kalevatykh, I., Laptev, I., Schmid, C.: Learning to augment synthetic images for sim2real policy transfer. In: IROS (2019) 

- 56. Peebles, W., Xie, S.: Scalable diffusion models with transformers. In: ICCV (2023) 57. Ranftl, R., Lasinger, K., Hafner, D., Schindler, K., Koltun, V.: Towards robust monocular depth estimation: Mixing datasets for zero-shot cross-dataset transfer. TPAMI (2020) 

- 58. Ravi, N., Gabeur, V., Hu, Y.T., Hu, R., Ryali, C., Ma, T., Khedr, H., Rädle, R., Rolland, C., Gustafson, L., Mintun, E., Pan, J., Alwala, K.V., Carion, N., Wu, C.Y., Girshick, R., Dollár, P., Feichtenhofer, C.: Sam 2: Segment anything in images and videos. arXiv preprint arXiv:2408.00714 (2024), `https://arxiv.org/ abs/2408.00714` 

59. Ren, X., Shen, T., Huang, J., Ling, H., Lu, Y., Nimier-David, M., Müller, T., Keller, A., Fidler, S., Gao, J.: Gen3c: 3d-informed world-consistent video generation with precise camera control. In: CVPR (2025) 

60. Rombach, R., Blattmann, A., Lorenz, D., Esser, P., Ommer, B.: High-Resolution Image Synthesis with Latent Diffusion Models . In: CVPR (2022) 

61. Schonberger, J.L., Frahm, J.M.: Structure-from-motion revisited. In: CVPR (2016) 62. Schönberger, J.L., Zheng, E., Frahm, J.M., Pollefeys, M.: Pixelwise view selection for unstructured multi-view stereo. In: ECCV (2016) 

63. Song, Y., Ermon, S.: Generative modeling by estimating gradients of the data distribution. In: NeurIPS (2019) 

64. Su, J., Ahmed, M., Lu, Y., Pan, S., Bo, W., Liu, Y.: Roformer: Enhanced transformer with rotary position embedding. Neurocomput. (2024) 

65. Team, A., Zhu, H., Wang, Y., Zhou, J., Chang, W., Zhou, Y., Li, Z., Chen, J., Shen, C., Pang, J., He, T.: Aether: Geometric-aware unified world modeling. In: ICCV (2025) 

66. Team, G.R., Choromanski, K., Devin, C., Du, Y., Dwibedi, D., Gao, R., Jindal, A., Kipf, T., Kirmani, S., Leal, I., et al.: Evaluating gemini robotics policies in a veo world simulator. arXiv preprint arXiv:2512.10675 (2025) 

67. Todorov, E., Erez, T., Tassa, Y.: Mujoco: A physics engine for model-based control. In: IROS (2012) 

68. Walke, H., Black, K., Lee, A., Kim, M.J., Du, M., Zheng, C., Zhao, T., HansenEstruch, P., Vuong, Q., He, A., Myers, V., Fang, K., Finn, C., Levine, S.: Bridgedata v2: A dataset for robot learning at scale. In: CoRL (2023) 

- 20 Xu et al. 

69. Wan, T., Wang, A., Ai, B., Wen, B., Mao, C., Xie, C.W., Chen, D., Yu, F., Zhao, H., Yang, J., et al.: Wan: Open and advanced large-scale video generative models. arXiv preprint arXiv:2503.20314 (2025) 

70. Wang, J., Chen, M., Karaev, N., Vedaldi, A., Rupprecht, C., Novotny, D.: Vggt: Visual geometry grounded transformer. In: CVPR (2025) 

71. Wang, Y., Wen, C., Guo, H., Peng, S., Qin, M., Bao, H., Zhou, X., Hu, R.: Precise action-to-video generation through visual action prompts. In: ICCV (2025) 

72. Wang, Z., Bovik, A.C., Sheikh, H.R., Simoncelli, E.P.: Image quality assessment: from error visibility to structural similarity. TIP (2004) 

73. Wu, J., Yin, S., Feng, N., He, X., Li, D., Hao, J., Long, M.: ivideogpt: Interactive videogpts are scalable world models. In: NeurIPS (2024) 

74. Xiang, F., Qin, Y., Mo, K., Xia, Y., Zhu, H., Liu, F., Liu, M., Jiang, H., Yuan, Y., Wang, H., et al.: Sapien: A simulated part-based interactive environment. In: CVPR (2020) 

75. Xiao, Y., Wang, J., Xue, N., Karaev, N., Makarov, I., Kang, B., Zhu, X., Bao, H., Shen, Y., Zhou, X.: Spatialtrackerv2: 3d point tracking made easy. In: ICCV (2025) 

76. Xu, M., Ye, C., Liu, H., Wu, Y., Chang, J., Han, X.: Stable-sim2real: Exploring simulation of real-captured 3d data with two-stage depth diffusion. In: ICCV (2025) 

77. Yang, L., Bai, Y., Eskandar, G., Shen, F., Altillawi, M., Chen, D., Majumder, S., Liu, Z., Kutyniok, G., Valada, A.: Roboenvision: A long-horizon video generation model for multi-task robot manipulation. In: IROS (2025) 

78. Yang, S., Du, Y., Ghasemipour, S.K.S., Tompson, J., Kaelbling, L.P., Schuurmans, D., Abbeel, P.: Learning interactive real-world simulators. In: ICLR (2024) 

79. Yang, X., Shi, H., Zhang, B., Yang, F., Wang, J., Zhao, H., Liu, X., Wang, X., Lin, Q., Yu, J., Wang, L., Chen, Z., Liu, S., Liu, Y., Yang, Y., Wang, D., Jiang, J., Guo, C.: Tencent hunyuan3d-1.0: A unified framework for text-to-3d and image-to-3d generation. arXiv preprint arXiv:2411.02293 (2024) 

80. Yang, X., Li, B., Xu, S., Wang, N., Ye, C., Zhaoxi, C., Qin, M., Yikang, D., Jin, X., Zhao, H., Zhao, H.: Orv: 4d occupancy-centric robot video generation. In: CVPR (2026) 

81. Ye, J., Xue, R., Van Hoorick, B., Tokmakov, P., Irshad, M.Z., Wang, Y., Guizilini, V.: Anchordream: Repurposing video diffusion for embodiment-aware robot data synthesis. arXiv preprint arXiv:2512.11797 (2025) 

82. Yu, H.X., Duan, H., Herrmann, C., Freeman, W.T., Wu, J.: Wonderworld: Interactive 3d scene generation from a single image. In: CVPR (2025) 

83. Yu, M., Hu, W., Xing, J., Shan, Y.: Trajectorycrafter: Redirecting camera trajectory for monocular videos via diffusion models. In: ICCV (2025) 

84. Zhang, C., Wu, Z., Lu, G., Tang, Y., Wang, Z.: imowm: Taming interactive multimodal world model for robotic manipulation. arXiv preprint arXiv:2510.09036 (2025) 

85. Zhang, D.J., Wu, J.Z., Liu, J.W., Zhao, R., Ran, L., Gu, Y., Gao, D., Shou, M.Z.: Show-1: Marrying pixel and latent diffusion models for text-to-video generation. IJCV (2025) 

86. Zhang, J., Herrmann, C., Hur, J., Jampani, V., Darrell, T., Cole, F., Sun, D., Yang, M.H.: Monst3r: A simple approach for estimating geometry in the presence of motion. arXiv preprint arxiv:2410.03825 (2024) 

87. Zhang, L., Rao, A., Agrawala, M.: Adding conditional control to text-to-image diffusion models. In: ICCV (2023) 

88. Zhang, R., Isola, P., Efros, A.A., Shechtman, E., Wang, O.: The unreasonable effectiveness of deep features as a perceptual metric. In: CVPR (2018) 

   - Kinema4D 21 

89. Zhen, H., Sun, Q., Zhang, H., Li, J., Zhou, S., Du, Y., Gan, C.: Tesseract: learning 4d embodied world models. In: ICCV (2025) 

90. Zhou, S., Du, Y., Chen, J., Li, Y., Yeung, D.Y., Gan, C.: Robodreamer: learning compositional world models for robot imagination. In: ICML (2024) 

91. Zhu, F., Wu, H., Guo, S., Liu, Y., Cheang, C., Kong, T.: Irasim: Learning interactive real-robot action simulators. In: ICCV (2025) 

22 Xu et al. 

# **_Supplementary Material_ for Kinema4D** 

## **Outline** 

This supplementary document is arranged as follows: 

(1) Sec. A provides more qualitative results; 

(2) Sec. B elaborates more technical details and discussions of our framework implementation, dataset, and real-world deployment; 

(3) Sec. C discusses more ablation studies and analysis. 

## **A More Qualitative Results** 

Fig. VII shows more 2D qualitative comparison with Ctrl-World [23], Fig. VIII visualizes more 4D qualitative comparison with TesserAct [89], Fig. IX illustrates our qualitative results for policy evaluation in simulation platform, and Fig. X provides extensive qualitative results of our method with Ground Truth as the reference. These results again demonstrate the effectiveness of our Kinema4D. 

We also provide a demo video, **_demo.mp4_** , for our work. In this video, a teaser introduction is provided from the beginning to 1:20. 1:20 _∼_ 2:40 illustrates our framework, 2:40 _∼_ 3:46 describes our dataset acquisition, 3:50 _∼_ 7:00 provides quantitative and animated qualitative results for the main comparison, 7:00 _∼_ 8:18 shows animated qualitative results for policy evaluation, 8:20 _∼_ 8:30 visualizes extensive animated results. 

## **B More Technical Details** 

### **B.1 Framework Implementations.** 

_Deployment of Kinematic Control._ In the initial Kinematics Control phase, we implement a multi-view reconstruction-projection pipeline. For individual robot reconstruction, we capture sparse orbit videos via a smartphone and sample 20 representative frames. We employ Grounded-SAM2<sup>_∗_</sup> [47,58] to segment the target object in the initial frame using the prompt `“the object on the desk”` , a strategy that proved highly robust across varying lighting conditions. These segments are then propagated throughout the sequence using the temporal tracking capabilities of SAM2<sup>_†_</sup> [58]. Given these masked multi-view images, we utilize ReconViaGen<sup>_‡_</sup> [11] for pose-free high-fidelity shape synthesis. Compared to traditional Structure-from-Motion (SfM) pipelines like COLMAP [61, 62] or recent feed-forward models like VGGT [70], ReconViaGen generates more complete meshes with significantly fewer holes in unobserved regions—a critical advantage under sparse, unconstrained viewpoints. Furthermore, it outperforms 

> ∗ `https://github.com/IDEA-Research/Grounded-SAM-2` 

> † `https://github.com/facebookresearch/sam2` 

> ‡ `https://github.com/estheryang11/ReconViaGen` 

Kinema4D 23 


**Fig. VII: Qualitative comparison of 2D video synthesis** between our Kinema4D and Ctrl-World [23]. Our method achieves superior fidelity. In contrast, Ctrl-World exhibits distorted actions and unrealistic environmental transitions. 


**Fig. VIII: 4D qualitative comparison between our Kinema4D and TesserAct [89]** . Unlike TesserAct that hallucinate outcomes, our Kinema4D precisely reflects Ground-Truth executions, including “near-miss” failure cases. For example, in the two bottom examples, our model _correctly interprets the spatial gap_ between the gripper and the objects, _even when their_ **_RGB textures overlap in 2D views_** . 

commercial-grade alternatives such as Hunyuan3D [79] in our specific laboratory setting. This pipeline produces a high-quality textured mesh and precise camera poses in approximately **_15_** _seconds_ on a single NVIDIA A100 GPU, facilitating the rapid construction of robot pointmap sequences in real-world deployment. 

24 Xu et al. 


**Fig. IX: 4D qualitative results of our Kinema4D for policy evaluation in simulation platform** . Our simulated results strongly align with actual executions, accurately synthesizing both successful rollouts and “near-miss” failures. For instance, in the bottom figures, our model correctly interprets the spatial gap between the gripper and the object, even when their RGB textures overlap in 2D views. Throughout both training and inference, we normalize each robot pointmap to a [0 _,_ 1] range based on the extrema (minimum and maximum values) across the entire pointmap sequence prior to VAE encoding. This sequence-level normalization facilitates affine-invariant 4D control, encouraging the framework to prioritize relative spatial geometry and inter-object relationships over absolute coordinate values. By mapping diverse robot trajectories into a canonical latent space, this approach enhances the model’s ability to generalize across different scales and workspace configurations. 

_Details of 4D Generative Modeling._ In the second phase of 4D Generative Modeling, we employ Parameter-Efficient Fine-Tuning (PEFT) via LoRA [30], initializing weights from 4DNeX<sup>_§_</sup> [15]. The base model, 4DNeX, was originally fine-tuned on the Wan2.1 [69] 14B image-to-video architecture. To mitigate the distribution shift between RGB and pointmap latents, we adopt the latent normalization strategy from 4DNeX. Specifically, we compute the empirical statistics of the pointmap domain in the latent space over 5,000 random training samples, yielding a mean _µ_ = _−_ 0 _._ 17 and a standard deviation _σ_ = 1 _._ 36. These values serve as constant normalization terms for the XYZ latents during both training and inference. The LoRA fine-tuning is configured with a rank of 64 to balance parameter efficiency with representational capacity. Training is conducted with a batch size of 32 using the AdamW optimizer, a peak learning rate of 2 _×_ 10<sup>_−_5</sup> , and a cosine warmup followed by constant decay. The model is trained 

> § `https://github.com/3DTopia/4DNeX` 

Kinema4D 25 


**Fig. X: Extensive 4D qualitative results of our Kinema4D** , across diverse domains, environments, robot actions, and the manipulated objects. These results are _non-overlapping_ with other figures. More animated results are provided in _demo.mp4_ . 

for 5,000 iterations across 32 NVIDIA A100 GPUs, taking approximately 2 days, at a spatial resolution of 480 _×_ 720 per modality, occupying 67GB of memory per GPU. While the original 4DNeX or WAN uses a text encoder to inject text conditions, we intentionally replace the text embedding with the VAE latents of robot sequences, which is discussed and ablated in Sec. C (“Text conditions”). During training and inference, our robot mask map is spatially and temporally downsampled according to the VAE latent transformation rules, ensuring exact alignment with the latent tensors. It is subsequently expanded to four channels (yielding a shape of _B ×_ 4 _× Hlatent × Wlatent_ ), where non-zero values are restricted to robot-occupied positions, and is then channel-wise concatenated with both the noisy and input latents. In addition, we follow ControlNet [87] to add a 1 × 1 zero-initialized convolution layer on the robot latent, to eliminate random noise as gradients in the initial finetuning steps. 

26 Xu et al. 

### **B.2 Dataset** 

_Acquisition of LIBERO simulated data._ Our data generation framework is built upon the MuJoCo [67] engine within the LIBERO [45] platform. We extend the OpenVLA [39] dataset pipeline<sup>_¶_</sup> by integrating MuJoCo’s depth-buffer rendering to capture per-pixel depth maps alongside RGB sequences. These are subsequently back-projected into world-coordinate pointmaps using intrinsic and extrinsic camera parameters. To maintain a consistent data format, these pointmaps are stored as pseudo-RGB MP4 videos after undergoing per-sequence min-max normalization. To ensure high data variance, we perform procedural randomization of background objects within each scene. While the core dataset consists of successful demonstrations, we systematically synthesize failure cases to enhance the model’s discriminative capabilities. Specifically, each successful trajectory is partitioned into three temporal segments, where Gaussian noise of varying intensities ( _σ ∈{_ 0 _._ 5 _,_ 0 _._ 8 _,_ 1 _._ 2 _}_ ) is injected into the 6-DoF pose dimensions. This process yields nine distinct failure trajectories per demonstration, as the cumulative error causes the robot to deviate progressively from the target path. Notably, the gripper state remains unperturbed to ensure that the resulting failures stem from reaching or positioning errors rather than unnatural grasping artifacts. 

_Extracting robot pointmap from 4D data annotations._ Using either simulation platform for producing synthetic data or ST-v2 [75] for processing real-world data, we can easily gain the whole pointmap (including both the robot and environment) sequence at a main camera view. To further gain the robot-only pointmap as the control signal, we need to extract the robot area from the given pointmap. To realize this, we segment the robot’s presence within RGB frames by utilizing SAM2 [58] with a robust semantic prompt ( _e.g_ ., “the robot arm”), and apply the segmented mask on both pointmap and RGB frames to gain robotonly sequences. By doing so, we maintain the automated property of our data processing pipeline, so that our framework can leverage scalable video data from diverse, in-the-wild sources without manual labeling overhead. During both the model training and inference, we use the processed robot pointmap sequence as the control signal. 

_Language annotations._ As we find that many text instruction labels are incomplete in our original data resource [7, 38, 68]. We utilize Qwen3-VL-plus<sup>_∥_</sup> [5] to generate the language descriptions for each episode. Two types of texts are generated, including the complete text (considering the whole robot-world dynamic interactions across the whole video) and the environment-centric descriptions (only considering the static environment at the initial frame). 

_Validation split._ To ensure a rigorous and fair comparison, we constructed a unified validation set by sampling and aggregating 3200 episodes from the official 

> ¶ `https://github.com/openvla/openvla` 

> ‖ `https://github.com/QwenLM/Qwen3-VL` 

Kinema4D 27 

validation episodes of all baselines. This evaluation set is sampled from our core data sources—2,000 from DROID, 1,000 from Bridge, 100 from RT-1, and 100 from LIBERO (50 successful and 50 failure modes)—preserving the proportional distribution of the training set. This composition ensures comprehensive coverage of complex robot-world interactions, ranging from articulated/deformable object manipulation and pick-and-place of objects. Crucially, all samples within this combined validation set were strictly excluded from our training set to prevent data leakage. This setup allows us to evaluate the generalization capability of our model across multiple data distributions simultaneously, whereas baselines are often specialized to a single domain. 

_The underlying logic behind 4D pseudo annotation._ To facilitate efficient largescale data synthesis, we employ ST-v2 [75] to generate pseudo-annotations directly from diverse robotic demonstration datasets. Our core design philosophy _prioritizes_ **_scalability_** as the primary driver for building a _generalizable_ robotic simulator. While we acknowledge that 4D reconstruction methods like ST-v2 may not achieve absolute, sub-millimeter geometric ground truth, they provide sufficiently high-fidelity relative spatial geometry. This level of accuracy is adequate for our generative framework to internalize the underlying spatial constraints and physical affordances of the environment (as verified in our qualitative results). By prioritizing the breadth of data over the exhaustive precision of individual samples, we enable the model to learn robust, generalizable motion priors that transcend the noise inherent in pseudo-labels. 

_Frame number_ . Each raw video is sliced into 49 frames per sample and maintains a unified frequency of motion dynamics for stable training. 

### **B.3 Real-World Deployment** 

_Reconstruction and projection._ Our real-world evaluation platform utilizes a YAM Arm<sup>_∗∗_</sup> (6-DoF collaborative manipulator). For comprehensive rollout recording and visual input, a primary RGB camera _cam_ is positioned at an oblique top-down angle relative to the workspace _W_ , ensuring a clear view of the manipulation area. After capturing orbit videos of the workspace, the primary viewpoint (fixed camera) image is integrated with the orbit-scan frames and processed via ReconViaGen [11] to produce 3D robot mesh and the camera pose of the primary viewpoint. To ensure the robot’s digital twin accurately reflects the physical state, we perform a rigid-body transformation **T**<sup>_base_</sup> _recon_<sup>be-</sup> tween the physical robot’s mounting point at _Fbase_ and the reconstructed global mesh at _Frecon_ via manual calibration. By retrieving the real-time joint encoders from the YAM Arm’s URDF, we solve the Forward Kinematics (FK) to update the pose of each link mesh **x** _base_ at _Fbase_ and transform it into _Frecon_ : **x** _recon_ = **T**<sup>_base_</sup> _recon_<sup>_·_</sup><sup>**x**</sup><sup>_base_.</sup> 

> ∗∗ `https://i2rt.com/collections/yam-arm` 

28 Xu et al. 

_Experimental setup._ We designed three distinct pick-and-place scenarios, denoted as _S ∈{_ Easy, Medium, Hard _}_ , to evaluate the zero-shot generalization of our Kinema4D. Each scenario consists of _N_ = 50 trials to ensure statistical significance. The task complexity is categorized by the density of distractor objects _D_ and the spatial constraints _C_ within the workspace _W_ . Critically, both the physical embodiment and the unseen laboratory environment are entirely outof-distribution (OOD) relative to our training data. This rigorous setup evaluates the framework’s ability to transcend the reality gap without any real-world fine-tuning or domain-specific adaptation. 

**Table V:** Specifications of Real-World Evaluation Scenarios. 

|**Scenario**|**Difficulty**|**Distractors** (_D_)|**Constraints / Challenges**|
|---|---|---|---|
|I. Canonical|Easy|_∅_|Basic OOD texture grasping|
|II. Cluttered|Medium|_n ∈_[3_,_5]_, r ≤_5cm|Spatial proximity & collision avoidance|
|III. Dynamic|Hard|_n >_5, randomized|Partial occlusion & narrow passages|


## **C More Ablation Studies and Analysis** 

_Why not also use the initial environmental pointmap as additional input?_ During the Kinematics Control phase, our primary objective is the extraction of precise 4D robotic trajectories. Consequently, we prioritize reconstructing the robot’s geometry from masked multi-view images rather than the entire scene. This produces robot-centric pointmap sequences, which are fused with the initial world RGB frame as the conditioning input for generative modeling. While it is technically feasible to reconstruct the full static environment and provide an initial-frame world pointmap for enhanced 4D spatial grounding, our empirical results suggest this is unnecessary. As listed in Tab. VI (“add env. pm”), incorporating the complete initial-frame pointmap does not yield performance gains. We attribute this to the pre-trained weights from 4DNeX [15], which already endow our framework with sufficient spatial inference capabilities derived from RGB signals alone. 

To further validate this design, we extended this ablation to our real-world setup. By reconstructing the entire physical environment, we provided the model with an initial real-world environmental pointmap. However, this led to a significant performance degradation, with a larger discrepancy between the policy simulation and the ground truth. Specifically, it yields [0.70, 0.82, 0.96] success rates for three different real-world test setups, respectively. We hypothesize that full-scene reconstruction introduces aleatoric noise and sensor artifacts from the physical world, which compromises the robustness of the latent control signal. This ablation confirms that our original design—focusing on precise robot kinematics while relying on RGB for environmental context—optimizes the balance between spatial accuracy and system robustness. 

Kinema4D 29 

**Table VI:** Quantitative results of more ablation studies. 

|Metrics|Ours|add env. pm|env. text|null text|depth|
|---|---|---|---|---|---|
|**PSNR**_↑_|**22.50**|21.93|20.97|22.31|21.04|
|**FID**_↓_|25.9|26.2|27.0|**25.6**|26.3|
|**CD-**_L_1_↓_|**0.0479**|0.0420|0.0592|0.0501|0.0583|


_Text conditions._ Since our model is designed to simulate the deterministic physical outcomes of actual robotic actions that could be either successful or failed for a task execution, relying solely on high-level task instruction texts is infeasible. To investigate the impact of language conditioning, we evaluated three variants: Environment-centric text, which describes only the static scene geometry; Null conditioning (“null text”); and our proposed robot VAE latents. 

As shown in Tab. VI, we observed that incorporating environment-centric text (“env. text”) slightly degrades performance, likely due to the modality gap between abstract linguistic descriptions and the requirement for precise 4D transitions. In contrast, our framework maintains high stability when using either null text (“null text”) or Robot VAE latents (“Ours”). Ultimately, we opt for robot VAE latents as the primary conditioning signal, as they provide a dense, kinematically-informed representation that significantly enhances the fine-grained control over robot pointmap generation, surpassing the spatial ambiguity inherent in natural language. 

_Depth map as the spatial representation._ While our framework utilizes 4D pointmaps as the spatial representation, we evaluate the versatility of our model by training and testing on depth-map sequences. Leveraging our ST-v2 [75] annotation pipeline, high-fidelity depth information is derived directly from our existing data without requiring additional effort. However, empirical results reported in Tab. VI (“depth”) indicate that relying solely on depth maps leads to a performance degradation. We hypothesize that while depth captures distances from the camera, it lacks the explicit tri-coordinate geometric constraints ( _X, Y, Z_ ) inherent in pointmaps. This weakens the model’s ability to maintain precise metric-space control, particularly for off-axis manipulation tasks. 

_Discussion on efficiency and memory usage._ We provide a comparison of computational efficiency and peak memory usage against the leading 2D-based baseline, Ctrl-World [23], and the 4D-based framework, TesserAct [89]. All evaluations were conducted on a single NVIDIA A100 GPU to ensure parity. We also report the results of cross-domain evaluation, which is trained on DROID [38] but tested on Bridge [68]. All the baseline implementations use their official codes. As summarized in Tab. VII, although both TesserAct and Ctrl-World show better efficiency, they are limited in cross-domain ability. 

Especially, Ctrl-World uses an auto-regressive architecture that offers superior throughput and a lower memory footprint. However, by relying on tokenbased action embeddings, it exhibits severe overfitting to the training dataset and lacks cross-embodiment capabilities due to the large gap between different 

30 Xu et al. 

**Table VII:** Comparison of the efficiency and cross-domain transfer. While the baseline methods offer better efficiency, their generalization abilities are extremely worse than our method, considering both the actual quality and the self-temporal consistency. 

|Method|Time (min)|Memory (GB)|**PSNR**_↑_|**PSNR (temp)**_↑_|**FID**_↓_|**FID (temp)**_↓_|**CD-**_L_1_↓_|**CD-**_L_1 **(temp)**_↓_|
|---|---|---|---|---|---|---|---|---|
|**Ours**|15|56|**19.23**|**36.95**|**29.3**|**15.4**|**0.0621**|**0.0068**|
|Ctrl-World [23]|**2.5**|**15**|12.14|19.32|38.5|49.5|-|-|
|TesserAct [89]|10|31|10.80|25.87|41.8|28.7|0.0928|0.0125|


embodiments’ raw action spaces. Consequently, when deployed in unseen domains, it produces extremely inconsistent temporal frames (denoted by “(temp)” in Tab. VII) and inferior visual quality due to the accumulated errors inherent in auto-regressive generation. As for TesserAct, it uses text instructions to represent action information, which lacks precise control and makes it fundamentally ineffective for the task-agnostic simulation. 

In contrast, our framework prioritizes generative fidelity and structural consistency as a generalizable and robust foundation for 4D world simulation. We argue that for a foundation model, the priority must be the **_reliability_** _and_ **_generalizability_** _of the physical transitions_ . We leave efficiency optimizations, such as knowledge distillation and model quantization, for future work. 

