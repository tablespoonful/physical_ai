---
title: "EA-WM: Event-Aware Generative World Model with Structured Kinematic-to-Visual Action Fields"
date: "2026-05-07"
authors: "Zhaoyang Yang; Yurun Jin; Lizhe Qi; Cong Huang; Kai Chen"
url: https://arxiv.org/abs/2605.06192
pdf: https://arxiv.org/pdf/2605.06192
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.06192)** / [論文ページ](https://arxiv.org/abs/2605.06192)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **EA-WM: Event-Aware Generative World Model with Structured Kinematic-to-Visual Action Fields** 

||**Zhaoyang Yang**<sup>**1,3**</sup><br>**Yurun Jin**<sup>**3,4**</sup>|
|---|---|
|**Lizhe**|**Qi**<sup>**1***</sup><br>**Cong Huang**<sup>**2,3**</sup><sup>_∗_</sup><br>**Kai Chen**<sup>**2,3,5**</sup><sup>_∗†_</sup>|


1Fudan University 2Zhongguancun Academy 

3Zhongguancun Institute of Artificial Intelligence 

4University of Science and Technology of China 5DeepCybo 

```
https://github.com/Shownx-c/EA-WM
```

## **Abstract** 

Pretrained video diffusion models provide powerful spatiotemporal generative priors, making them a natural foundation for robotic world models. While recent world-action models jointly optimize future videos and actions, they predominantly treat video generation as an auxiliary representation for policy learning. Consequently, they insufficiently explore the inverse problem: leveraging action signals to guide video synthesis, thereby often failing to preserve precise robot spatial geometry and fine-grained robot-object interaction dynamics in the generated rollouts. To bridge this gap, we present **EA-WM** , an Event-Aware Generative World Model that effectively closes the loop between kinematic control and visual perception. Rather than injecting joint or end-effector actions as abstract, low-dimensional tokens, EA-WM projects actions and kinematic states directly into the target camera view as _Structured Kinematic-to-Visual Action Fields_ (KVAFs). To fully exploit this geometrically grounded representation, we introduce event-aware bidirectional fusion blocks that modulate cross-branch attention, capturing object state changes and interaction dynamics. Evaluated on the comprehensive WorldArena benchmark, EA-WM achieves state-of-the-art performance, outperforming existing baselines by a significant margin. 

## **1 Introduction** 

Recent video foundation models have rapidly improved the ability to synthesize temporally coherent, high-fidelity videos. From latent video diffusion models and space-time diffusion architectures to diffusion-transformer systems such as CogVideoX [27] and the open Wan series [25, 24, 5], these models learn strong priors over appearance, motion, and scene evolution from large-scale video corpora [4, 2, 27, 25]. This progress has motivated the view that scaled video generation can move beyond visual content creation toward world simulation [12, 1]. Since robot manipulation is fundamentally a process of predicting how actions change visual states over time, such spatiotemporal priors make video generation models a natural foundation for robotic world modeling. 

Driven by this potential, recent robotics research has begun to adapt these video priors for several roles. Some methods [26, 16, 32] use video world models as predictive simulators to roll out the visual consequences of candidate actions, enabling action-conditioned video prediction, visual planning, model-based reinforcement learning, and fine-grained robot-object interaction simulation. Other work [6, 11, 15, 10, 22] uses generated rollouts as robot-learning infrastructure: they can synthesize 

> *Corresponding authors. †Project leader. 

Preprint. 


Figure 1: Comparison between direct low-dimensional action conditioning and the proposed _Structured Kinematic-to-Visual Action Fields_ (KVAFs). 

additional robot trajectories beyond manual data collection, provide video-based supervision for policy learning, and offer scalable proxies for evaluating VLA policies without repeatedly executing every policy on physical robots. 

Meanwhile, recent world-action models [31, 28, 7] have begun to jointly tune video generation and action modeling within unified generative frameworks, showing that future videos can provide dense world representations for action generation, policy learning, planning, and value estimation. However, these works predominantly treat video generation merely as an auxiliary representation to optimize action prediction. Consequently, they insufficiently explore the crucial inverse problem: how to effectively leverage control signals to guide accurate video synthesis. This oversight leads to a critical limitation: the generated videos often fail to preserve the precise spatial geometry of robot motion and the complex dynamics of robot-object interactions. As high-quality video rollouts are increasingly relied upon as predictive simulators and synthetic data engines for downstream tasks [6, 11, 15, 10, 22], mitigating this degradation in rollout quality is imperative. A fundamental obstacle lies in the domain misalignment between low-dimensional control signals and high-dimensional video synthesis. Standard practices typically inject raw joint-space parameters, end-effector vectors, or abstract tokens as conditionings [26, 16, 32, 14]. While computationally compact, these representations are heavily tied to specific robot embodiments and carry limited spatial context [30]. They force the video generator to implicitly deduce cross-domain kinematics, frequently resulting in a failure to accurately render robot geometry or capture nuanced physical interactions. Furthermore, conventional architectures often lack an effective interaction mechanism between the action and video pathways, causing the generator to overlook fine-grained interaction information between the robot and objects. 

To address these challenges, we propose **EA-WM** , an event-aware robotic video world model conditioned on _Structured Kinematic-to-Visual Action Fields_ (KVAFs). At the representation level, EA-WM constructs KVAFs by lifting low-dimensional robot actions and kinematic states into the target camera view through robot kinematics and camera projection. Specifically, KVAFs render depthaware arm structures, joint landmarks, gripper geometry, end-effector heatmaps, and pose cues as temporally aligned visual fields. Compared with raw action vectors, KVAFs bring action conditioning into the same image domain as future video generation, thereby alleviating domain misalignment and providing richer spatial and geometric cues for robotic world modeling, as shown in Figure 1. At the architectural level, EA-WM augments a diffusion-transformer backbone with a dedicated KVAF branch and interval-based bidirectional fusion, facilitating continuous interaction between structured kinematic cues and video features. Crucially, we introduce an event-aware bidirectional fusion mechanism driven by _Event-Difference Latent Supervision_ (EDLS). By supervising event predictions with VAE-encoded temporal difference latents, EDLS compels the model to dynamically allocate attention not only to the robot’s geometric progression but also to regions undergoing state 

2 

transitions and interaction dynamics, leading to significantly more physically consistent rollouts. The key contributions of this work are summarized as follows: 

- We introduce **EA-WM** , an innovative Event-Aware Generative World Model framework for robotic video generation. By projecting low-dimensional kinematic states directly into the target camera view, our framework creates _Structured Kinematic-to-Visual Action Fields_ (KVAFs), fundamentally resolving the domain misalignment between raw action tokens and video-domain generation. 

- We propose an _event-aware bidirectional fusion_ mechanism driven by _Event-Difference Latent Supervision_ (EDLS). This module explicitly regularizes cross-stream attention using temporal difference latents, compelling the model to dynamically attend to critical regions of robot motion, object state transitions, and robot-object interaction dynamics, leading to more physically consistent robot videos. 

- We achieve superior performance on the WorldArena benchmark. Compared to existing stateof-the-art baselines, EA-WM significantly enhances the physical adherence, 3D geometric accuracy, and fine-grained controllability of generated rollouts, establishing a new standard for robotic video modeling. 

## **2 Related Work** 

### **2.1 Robotic world models based on video generation models** 

Recent diffusion-based video generators, including Stable Video Diffusion [4], Lumiere [2], CogVideoX, and the Wan series [27, 25, 24, 5], have substantially improved temporal coherence, motion realism, and scene-consistent synthesis, making them increasingly useful as priors for world simulation [12, 1]. These priors are especially useful in robotics, where world models must predict how actions change future visual states. Existing robotic video world models span action-conditioned simulators and forward models for planning, model-based RL, and interaction simulation [26, 16, 32], infrastructure methods that use generated videos as synthetic trajectories, supervision, or policylearning proxies [6, 11], and learned video environments for scalable VLA evaluation and planning [15, 10, 22]. Recent world-action models further couple video and action generation in unified frameworks [31, 28, 7]. Despite these advances, how to fully exploit action information to improve future robot-video generation remains insufficiently explored. 

### **2.2 World action models** 

World Action Models (WAMs) are unified generative models that predict both robot actions and future visual states in an aligned manner, as formulated in DreamZero [28]. Recent work [31, 9, 28, 19, 17, 21, 7, 3, 13] in this line mainly treats future video modeling as dense supervision or latent guidance for better action generation and policy learning. These WAM-style methods demonstrate that future videos can regularize action learning with physical dynamics, provide denser supervision than action-only imitation, and improve generalization for robot control. However, their emphasis remains largely on how video generation can improve action prediction or policy learning. The reverse direction—using action information as structured guidance to improve future robot-video generation— remains much less explored, even though rollout quality directly affects the usefulness of robotic world models as predictive simulators, planning substrates, and policy-evaluation environments [6, 11, 15, 10, 22]. 

A key question is therefore how action information should be represented. Existing methods have explored raw joint-space or end-effector vectors, 7-DoF control tokens, latent actions, universal action tokens, and spatial action abstractions. VideoVLA [19], UVA [9], Motus [3], and ViPRA [17] represent action information through numerical, latent, or video-conditioned action spaces, while UniAct [30] and SpatialVLA [14] study more transferable or spatially structured action representations. While compact and effective for policy learning, these representations remain weakly grounded in the target camera view and carry limited explicit spatial and geometric information for video generation. WoG [21] also highlights the challenge of preserving sufficient fine-grained information under compact future-conditioning representations. Recent visual representations lift actions into image or video space via RGB action targets [20], virtual robot renders [23], pixelgrounded multiview action videos [29], or multiview heatmap videos [8]. However, their action 

3 


Figure 2: Overview of EA-WM. Robot actions and kinematic states are first lifted into camera-aligned KVAFs. RGB videos and KVAFs are encoded into the shared Wan2.2 latent space and processed by a video branch and a KVAF branch. Sparse event-aware bidirectional fusion exchanges information between the two branches, while EDLS guides the model to attend to motion and interaction changes. 

channels are often intentionally compact and robot-centric: they prioritize joint targets, rendered robot bodies, arm-motion cues, or heatmaps, so fine-grained kinematic detail may still be limited, and robot-object interaction information is often modeled only indirectly through companion RGB branches or downstream video generation rather than encoded explicitly in the action representation itself. 

## **3 Method** 

EA-WM is an action-guided robotic video world model built upon the Wan2.2-TI2V backbone [25]. The overall pipeline is shown in Figure 2. Given an initial RGB observation, a language instruction, and a sequence of robot actions, our goal is to generate future robot videos that are not only visually plausible but also consistent with the commanded robot motion and robot-object interactions. Instead of injecting low-dimensional actions directly into the video generator, EAWM first transforms actions and kinematic states into _Structured Kinematic-to-Visual Action Fields_ (KVAFs), which provide camera-aligned visual cues of robot geometry, motion, and end-effector intent. Both RGB videos and KVAFs are encoded into the latent space of the pretrained video VAE, allowing action information to guide generation in the same representation space as the target videos. To effectively exploit this structured action signal, EA-WM introduces a dedicated KVAF branch and event-aware bidirectional fusion blocks on top of the Wan2.2 video DiT. The KVAF branch learns to accurately predict KVAFs, encouraging the branch to understand the geometric and motion information embedded in KVAFs. Meanwhile, the event-aware bidirectional fusion blocks are guided by _Event-Difference Latent Supervision_ (EDLS), which uses VAE-encoded temporal difference latents to supervise event predictions, encouraging the model to capture object motion and robot-object interaction cues. Through cross-attention, the video backbone exchanges information with the KVAF branch, allowing structured action geometry and event-aware interaction cues to be shared with the generative stream for more accurate future video generation. 

### **3.1 Structured Kinematic-to-Visual Action Fields** 

We introduce _Structured Kinematic-to-Visual Action Fields_ (KVAFs), which convert low-dimensional robot actions and kinematic states into camera-aligned visual fields for future video generation. Given a trajectory of length _T_ , we construct a sequence _V_ = _{_ **V** _t}_<sup>_T_</sup> _t_ =1<sup>, where each frame</sup><sup>**V**</sup><sup>_t∈_R</sup><sup>_H×W ×_3</sup> 

4 

is rendered in the target camera view. Here _H_ and _W_ denote the image height and width, and _t_ indexes the video timestep. 

At time step _t_ , we take arm joint values **q** _t_ , gripper states _gt_ , end-effector poses **_ξ_** _t_ , and camera parameters ( **K** _t,_ **E** _t_ ) as input. Here **K** _t_ denotes the camera intrinsic matrix, and **E** _t_ denotes the world-to-camera extrinsic matrix. For simplicity, we omit the left/right arm index in the notation; in practice, KVAFs are constructed for both arms. We first recover 3D robot geometry by forward kinematics, 


where **T**<sup>_W_</sup> _k_<sup>(</sup><sup>_t_) is the world-frame pose of the</sup><sup>_k_-th robot link,</sup><sup>**T**orig</sup> _k_ is the static joint transform from the robot kinematic chain, and **T**<sup>mot</sup> _k_ ( _qt,k_ ) is the motion transform induced by the joint value _qt,k_ . The resulting link poses provide arm and gripper keypoints _Pt_ = _{_ **p**<sup>_W_</sup> _k_<sup>(</sup><sup>_t_)</sup><sup>_}_in the world frame.</sup> 

We then project these 3D keypoints into the camera plane by 


Here **p**<sup>_W_</sup> and **p**<sup>_C_</sup> denote the same robot keypoint in the world and camera coordinate frames, respectively; **u** ˆ is the homogeneous image coordinate, and ( _u, v_ ) is the final projected pixel location. Points behind the camera are discarded. 

Finally, we rasterize depth-aware arm skeletons, joint landmarks, gripper geometry, end-effector heatmaps, and pose axes on a black canvas to obtain 


The rendering operator composes the projected robot keypoints, end-effector pose cues, and gripperrelated visual elements into an RGB visual action field. By expressing robot actions in the same image domain as the target rollout, KVAFs provide spatially grounded and temporally aligned motion cues that are more compatible with video-based robotic world modeling than raw action tokens. 

### **3.2 Event-Aware Generative World Model** 

EA-WM builds upon the Wan2.2-TI2V backbone and preserves its original text-conditioned video denoising path. To inject structured action information, we encode KVAFs with the same video VAE and introduce a dedicated KVAF branch in the latent space. After patchification, the noised video latent and KVAF latent are represented as two token streams, denoted by **H**<sup>_v_</sup> and **H**<sup>_k_</sup> . The video stream follows the original Wan2.2 DiT blocks, while the KVAF stream is modeled by a full-depth copy of these blocks, allowing action information to remain as a structured visual stream rather than being compressed into a low-dimensional token. 

We insert event-aware fusion modules at a sparse set of layers _S_ . For _ℓ ∈S_ , an event MLP first computes a shared event representation from the current video and KVAF tokens, and then predicts both a per-token event gate and an event latent: 


Here **G** _ℓ_ is a per-token event gate that modulates cross-stream information exchange, while **E**<sup>ˆ</sup> _ℓ_ is the predicted event latent supervised by EDLS. Since both outputs are derived from the shared event representation **M** _ℓ_ , EDLS encourages **M** _ℓ_ to encode temporal changes and interaction cues, which are then passed to the gate **G** _ℓ_ and used to regulate video–KVAF fusion. 

The event gate controls bidirectional cross-attention between the two streams: 


The updated video tokens are then processed by the original Wan2.2 block, and the updated KVAF tokens are passed to the next KVAF branch block. At non-fusion layers, the two streams are updated without cross-stream fusion. In this way, EDLS does not merely add an auxiliary event prediction head; it shapes the shared event representation that produces the gate, and the gate directly controls 

5 

Table 1: Quantitative comparison on selected WorldArena metrics.All metrics are normalized to [0 _,_ 1] and higher is better. P3CScore is the average over the six selected metrics multiplied by 100. 

|Model|Physics A<br>Interaction<br>Quality|dherence<br>Trajectory<br>Accuracy|3D A<br>Depth<br>Accuracy|ccuracy<br> Perspectivity|Control<br>Instruction<br>Following|lability<br>Semantic<br>Alignment|P3CScore|
|---|---|---|---|---|---|---|---|
|CogVideoX|0.594|0.353|0.910|0.783|0.727|**0.898**|71.08|
|WoW|0.556|0.206|0.728|0.767|0.569|0.884|61.83|
|Wan 2.2|0.518|0.163|0.777|0.766|0.538|0.888|60.83|
|TesserAct|0.580|0.140|0.716|0.792|0.615|0.878|62.02|
|GigaWorld-0|0.537|0.155|0.632|0.760|0.616|0.859|59.32|
|Vidar|0.535|0.193|0.787|0.759|0.591|0.883|62.47|
|Cosmos-Predict 2.5 (text)|0.387|0.082|0.705|0.796|0.266|0.773|50.15|
|Genie Envisioner|0.205|0.068|0.866|0.528|0.203|0.854|45.40|
|**EA-WM (Ours)**|**0.682**|**0.430**|**0.959**|**0.838**|**0.792**|0.895|**76.60**|


how much KVAF information is injected into the video stream and how much scene information is fed back to the KVAF stream. 

To construct EDLS, we compute a frame-difference video from the input sequence _{Iτ }_<sup>_T_</sup> _τ_ =1<sup>:</sup> 


and encode it with the same VAE to obtain the event latent target **E** . Let **Y**<sup>ˆ</sup><sup>_v_</sup> and **Y**<sup>ˆ</sup><sup>_k_</sup> be the predictions of the video and KVAF heads, and **Y**<sup>_v_</sup> and **Y**<sup>_k_</sup> be their corresponding flow-matching targets. The total training objective is 


Here _ω_ ( _t_ ) denotes the timestep-dependent flow-matching training weight used by the scheduler, and _λ_ evt controls the strength of EDLS. The first video frame is treated as the image condition and excluded from the video prediction loss. This objective encourages EA-WM to use KVAF information in regions where motion and interaction changes occur, preserving action-consistent robot geometry while remaining sensitive to object motion and robot-object interactions. 

## **4 Experiments** 

### **4.1 Experimental Details** 

We train EA-WM in two stages: the first stage freezes the event-aware fusion modules and trains the main DiT LoRA, KVAF-branch LoRA, and KVAF head to stabilize the two streams; the second stage unfreezes the fusion modules to learn cross-stream event-aware interaction. We evaluate generated videos with WorldArena [18], a unified benchmark for embodied world models. We use a LoRA rank of 32, and set the learning rate to 8 _×_ 10<sup>_−_5</sup> for all trainable components. Training is conducted on 32 H100 GPUs with a batch size of 32. Following WorldArena, we use the same Robotwin dataset and segmentation method and select three dimensions for evaluation: Physics Adherence, 3D Accuracy, and Controllability. These dimensions measure interaction plausibility, trajectory consistency, depth and perspective accuracy, instruction following, and semantic consistency. We compare EA-WM with multiple representative video world models under the selected metrics. 

### **4.2 Experimental Results** 

**Quantitative Analysis.** Following WorldArena, we evaluate EA-WM on three dimensions: Physics Adherence, 3D Accuracy, and Controllability. All metrics are normalized to [0 _,_ 1], and higher is better. We report P3CScore, the average score over the six selected metrics multiplied by 100. The final results are shown in Table 1. 

EA-WM achieves the best overall P3CScore of 76.60, outperforming the strongest baseline, CogVideoX, by 5.52 points. The improvement is particularly clear on metrics related to actioninduced motion and interaction: EA-WM improves Interaction Quality from 0.594 to 0.682, Trajectory Accuracy from 0.353 to 0.430, and Instruction Following from 0.727 to 0.792. These gains 

6 


Figure 3: Qualitative comparison on four randomly selected RoboTwin 2.0 tasks. For each task, we visualize results at the same temporal step. Red boxes highlight local robot-object interaction regions. 

suggest that introducing KVAFs and event-aware bidirectional fusion blocks helps the model better preserve robot-object interaction, follow commanded motion trajectories, and generate videos that are more consistent with the task instruction. EA-WM also improves Depth Accuracy and Perspectivity by 0.049 and 0.042 over the strongest baselines, respectively, indicating stronger 3D consistency. Overall, EA-WM outperforms all compared models on five out of six selected metrics, demonstrating stronger physics adherence, 3D consistency, and controllability for robotic video world modeling. 

**Qualitative Analysis.** We further conduct qualitative comparisons on four randomly selected tasks, visualizing GT, the Wan2.2 baseline, and EA-WM at the same temporal step for each task. As shown in Figure 3, we compare the results in four aspects: robot-object interaction, preservation of object geometry, physical consistency of robots, and completion of tasks. Compared with the Wan2.2 baseline, EA-WM jointly models KVAF and video streams through event-aware bidirectional fusion, allowing the model to better follow action-induced motion cues and focus on regions where object states and robot-object interactions change. As a result, EA-WM generates more accurate gripper-object contact relations, better preserves object identity and local geometry, and maintains more physically plausible robot poses during manipulation. Overall, EA-WM is closer to GT in both interaction fidelity and task progress, demonstrating stronger action-consistent future video generation. 

### **4.3 Ablation Study** 

To verify the effectiveness of each component in EA-WM, we conduct ablation studies on the same selected WorldArena metrics used in quantitative evaluation. We compare the full model with three variants: the original Wan2.2 backbone, a variant that replaces KVAFs with numerical action representations, and a variant that removes event-aware fusion while keeping bidirectional crossattention for video–KVAF interaction. We report Physics Adherence, 3D Accuracy, Controllability, and the averaged P3CScore. 

The ablation results reveal the complementary roles of KVAFs and EAF. Compared with the variant without KVAFs, the full EA-WM improves P3CScore by 5.63 points, with particularly clear gains on Trajectory Accuracy and Depth Accuracy. This suggests that camera-aligned KVAFs provide useful geometric motion cues beyond numerical action inputs, especially for preserving robot trajectories and 3D structure in the generated videos. Compared with the variant without EAF, EA-WM improves P3CScore by 1.80 points and shows notable gains on Interaction Quality and Perspectivity, indicating that EDLS-guided event-aware fusion helps the model better focus on motion changes and robotobject interaction regions during cross-stream information exchange. Although the variant without EAF slightly outperforms EA-WM on Semantic Alignment, the full model achieves the best overall score and more balanced performance across physics adherence, 3D accuracy, and controllability. 

We further visualize the `ranking_block_size` task to more intuitively compare the differences among ablation variants. As shown in Figure 4, the two ablations exhibit complementary failure modes. The variant without KVAFs can better maintain the local relations between the robot arm and objects, but it is less accurate in modeling the grasping trajectory and action-induced motion. In contrast, the variant without event-aware fusion can better infer the grasping route of the robot 

7 

Table 2: Ablation study on selected WorldArena metrics. All metrics are normalized to [0 _,_ 1] and higher is better. P3CScore is the average over the six selected metrics multiplied by 100. 

||Physics A|dherence|3D A|ccuracy|Control|lability|P3CScore|
|---|---|---|---|---|---|---|---|
|Variant|Interaction<br>Quality|Trajectory<br>Accuracy|Depth<br>Accuracy|Perspectivity|Instruction<br>Following|Semantic<br>Alignment||
|Wan2.2|0.518|0.163|0.777|0.766|0.538|0.888|60.83|
|w/o KVAFs|0.670|0.298|0.884|0.791|0.726|0.889|70.97|
|w/o EAF|0.656|0.407|0.947|0.800|0.782|**0.896**|74.80|
|**EA-WM**|**0.682**|**0.430**|**0.959**|**0.838**|**0.792**|0.895|**76.60**|


Figure 4: Ablation visualization on the `ranking_block_size` task. 

arm from KVAFs, but it struggles to preserve object consistency, such as the relative shape, size, and spatial arrangement of the blocks. By combining KVAFs with event-aware fusion, EA-WM handles both aspects more effectively: it follows the spatial motion pattern of the robot while preserving object consistency and robot-object interaction fidelity, generating videos that better match the physical progression of the task. 

### **4.4 Additional Analysis** 

**Action recovery and image-domain alignment of KVAFs.** To better understand the information encoded in KVAFs, we conduct a preliminary action-recovery analysis in the numerical action space. We use a heuristic procedure to recover end-effector translation, orientation, and gripper states from generated KVAF videos, and compare the recovered actions with predictions from a raw-action baseline that directly predicts numerical actions. As shown in Table 3, numerical action prediction still performs better on translation, rotation, and gripper errors. This gap is expected, since KVAFs are designed as image-domain action fields rather than direct numerical action outputs, and our current recovery pipeline depends on detecting small visual cues such as heatmap centers, pose axes, and gripper geometry. The detection rate of the heuristic KVAF recovery is approximately 0 _._ 45, suggesting that mapping structured visual action fields back to precise numerical actions remains a challenging problem. Nevertheless, the recovery results indicate that KVAFs contain partially recoverable action information, and motivate future work on more reliable bridges between imagedomain action fields and numerical action spaces. More importantly, the overlay visualizations in Figure 5 show that the predicted KVAFs are well aligned with the generated robot motion across randomly selected tasks. The projected skeletons, end-effector cues, and pose axes follow the robot configuration in the generated videos, indicating that the network has learned the spatial and physical information contained in KVAFs rather than treating them as abstract conditioning signals. This image-domain alignment helps connect action-induced robot motion with object locations and local interaction regions, providing an interpretable bridge between low-dimensional actions and future video generation. 

8 

Table 3: Numerical action recovery from generated KVAFs. Errors are reported for translation, rotation, and gripper actions; lower is better. 

|Method|Translation<br>Error|Rotation<br>Error|Gripper<br>Error|
|---|---|---|---|
|Raw-action baseline|**0.004**|**0.009**|**0.013**|
|KVAF recovery|0.0155|0.110|0.039|


Heuristic KVAF recovery detection rate: _∼_ 0 _._ 45. 

Figure 5: KVAFs overlays on generated videos. The overlays align with generated robot motion and reveal interpretable spatial cues learned from KVAFs. 

Table 4: Comparison with action- or trajectory-conditioned baselines on selected WorldArena metrics. All metrics are normalized to [0 _,_ 1] and higher is better. P3CScore is the average over the six selected metrics multiplied by 100. 

|Model|Physics A<br>Interaction<br>Quality|dherence<br>Trajectory<br>Accuracy|3D A<br>Depth<br>Accuracy|ccuracy<br> Perspectivity|Control<br>Instruction<br>Following|lability<br>Semantic<br>Alignment|P3CScore|
|---|---|---|---|---|---|---|---|
|CtrlWorld|0.621|0.477|0.930|0.796|0.727|0.891|74.03|
|IRASim|0.566|0.364|0.931|0.779|0.660|0.885|69.75|
|Cosmos-Predict 2.5 (action)|0.550|0.295|0.886|0.764|0.584|0.888|66.12|
|RoboMaster|0.536|0.116|0.834|0.759|0.577|0.876|61.63|
|**KVAF-conditioned generation**|**0.682**|**0.494**|**0.977**|**0.850**|**0.784**|**0.901**|**78.13**|


**KVAF-conditioned video generation.** We further compare KVAF-conditioned generation with mainstream action- or trajectory-conditioned baselines. This analysis focuses on whether representing actions as camera-aligned visual fields can provide a stronger conditioning interface than numerical actions or trajectories. As shown in Table 4, KVAF-conditioned generation achieves the best performance across all six selected metrics and obtains the highest P3CScore. Compared with raw action- or trajectory-conditioned models, KVAFs provide richer spatial and geometric cues in the video domain, leading to better physics adherence, 3D consistency, and controllability. These results further suggest that transforming action information into structured visual action fields is an effective way to guide robotic video world modeling. 

## **5 Limitations** 

EA-WM requires robot kinematics, camera calibration, and synchronized action-state logs to construct KVAFs. While this yields accurate, well-aligned action representations in simulation, real-world deployment may be affected by calibration errors, occlusions, sensor noise, or embodiment shifts. Current KVAFs mainly encode robot-side geometric motion cues, while object-state changes and robot-object interactions are captured indirectly through event-aware fusion and EDLS. Extending KVAFs with object-centric or contact-aware visual fields is a promising future direction. 

## **6 Conclusion** 

We present **EA-WM** , an event-aware generative world model for action-consistent robot-video generation. Unlike current WAMs that mainly optimize action prediction or policy learning, EA-WM focuses on preserving robot spatial motion and robot-object interaction dynamics in generated videos. It maps actions and kinematic states into _Structured Kinematic-to-Visual Action Fields_ (KVAFs) aligned with the visual generation domain, and integrates them through EDLS-guided event-aware bidirectional fusion. On WorldArena, EA-WM achieves the best P3CScore among compared models. 

9 

## **References** 

- [1] Niket Agarwal, Arslan Ali, Maciej Bala, Yogesh Balaji, Erik Barker, Tiffany Cai, Prithvijit Chattopadhyay, Yongxin Chen, Yin Cui, Yifan Ding, et al. Cosmos world foundation model platform for physical ai. _arXiv preprint arXiv:2501.03575_ , 2025. 

- [2] Omer Bar-Tal, Hila Chefer, Omer Tov, Charles Herrmann, Roni Paiss, Shiran Zada, Ariel Ephrat, Junhwa Hur, Guanghui Liu, Amit Raj, Yuanzhen Li, Michael Rubinstein, Tomer Michaeli, Oliver Wang, Deqing Sun, Tali Dekel, and Inbar Mosseri. Lumiere: A space-time diffusion model for video generation. _arXiv preprint arXiv:2401.12945_ , 2024. 

- [3] Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Yao Feng, Chendong Xiang, Yinze Rong, Hongyan Zhao, Hanyu Liu, Zhizhong Su, Lei Ma, Hang Su, and Jun Zhu. Motus: A unified latent action world model. _arXiv preprint arXiv:2512.13030_ , 2025. 

- [4] Andreas Blattmann, Tim Dockhorn, Sumith Kulal, Daniel Mendelevitch, Maciej Kilian, Dominik Lorenz, Yam Levi, Zion English, Vikram Voleti, Adam Letts, Varun Jampani, and Robin Rombach. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_ , 2023. 

- [5] Xin Gao, Li Hu, Siqi Hu, Mingyang Huang, Chaonan Ji, Dechao Meng, Jinwei Qi, Penchong Qiao, Zhen Shen, Yafei Song, Ke Sun, Linrui Tian, Guangyuan Wang, Qi Wang, Zhongjian Wang, Jiayu Xiao, Sheng Xu, Bang Zhang, Peng Zhang, Xindi Zhang, Zhe Zhang, Jingren Zhou, and Lian Zhuo. Wan-S2V: Audio-driven cinematic video generation. _arXiv preprint arXiv:2508.18621_ , 2025. 

- [6] Joel Jang, Seonghyeon Ye, Zongyu Lin, Jiannan Xiang, Johan Bjorck, Yu Fang, Fengyuan Hu, Spencer Huang, Kaushil Kundalia, Yen-Chen Lin, et al. Dreamgen: Unlocking generalization in robot learning through video world models. _arXiv preprint arXiv:2505.12705_ , 2025. 

- [7] Moo Jin Kim, Yihuai Gao, Tsung-Yi Lin, Yen-Chen Lin, Yunhao Ge, Grace Lam, Percy Liang, Shuran Song, Ming-Yu Liu, Chelsea Finn, and Jinwei Gu. Cosmos policy: Fine-tuning video models for visuomotor control and planning. _arXiv preprint arXiv:2601.16163_ , 2026. 

- [8] Peiyan Li, Yixiang Chen, Yuan Xu, Jiabing Yang, Xiangnan Wu, Jun Guo, Nan Sun, Long Qian, Xinghang Li, Xin Xiao, Jing Liu, Nianfeng Liu, Tao Kong, Yan Huang, Liang Wang, and Tieniu Tan. Multi-view video diffusion policy: A 3d spatio-temporal-aware video action model. _arXiv preprint arXiv:2604.03181_ , 2026. 

- [9] Shuang Li, Yihuai Gao, Dorsa Sadigh, and Shuran Song. Unified video action model. _arXiv preprint arXiv:2503.00200_ , 2025. 

- [10] Yaxuan Li, Yichen Zhu, Junjie Wen, Chaomin Shen, and Yi Xu. Worldeval: World model as real-world robot policies evaluator. _arXiv preprint arXiv:2505.19017_ , 2025. 

- [11] Junbang Liang, Pavel Tokmakov, Ruoshi Liu, Sruthi Sudhakar, Paarth Shah, Rares Ambrus, and Carl Vondrick. Video generators are robot policies. _arXiv preprint arXiv:2508.00795_ , 2025. 

- [12] OpenAI. Video generation models as world simulators. `https://openai.com/index/ video-generation-models-as-world-simulators/` , 2024. Technical report/blog post. 

- [13] Jonas Pai, Liam Achenbach, Victoriano Montesinos, Benedek Forrai, Oier Mees, and Elvis Nava. mimic-video: Video-action models for generalizable robot control beyond vlas. _arXiv preprint arXiv:2512.15692_ , 2025. 

- [14] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, and Xuelong Li. SpatialVLA: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- [15] Julian Quevedo, Ansh Kumar Sharma, Yixiang Sun, Varad Suryavanshi, Percy Liang, and Sherry Yang. Worldgym: World model as an environment for policy evaluation. _arXiv preprint arXiv:2506.00613_ , 2025. 

10 

- [16] Marc Rigter, Tarun Gupta, Agrin Hilmkil, and Chao Ma. AVID: Adapting video diffusion models to world models. _arXiv preprint arXiv:2410.12822_ , 2024. 

- [17] Sandeep Routray, Hengkai Pan, Unnat Jain, Shikhar Bahl, and Deepak Pathak. Vipra: Video prediction for robot actions. _arXiv preprint arXiv:2511.07732_ , 2025. 

- [18] Yu Shang, Zhuohang Li, Yiding Ma, Weikang Su, Xin Jin, Ziyou Wang, Lei Jin, Xin Zhang, Yinzhou Tang, Haisheng Su, Gao Chen, Wei Wu, Xihui Liu, Dhruv Shah, Zhaoxiang Zhang, Zhibo Chen, Jun Zhu, Yonghong Tian, Tat-Seng Chua, Wenwu Zhu, and Yong Li. WorldArena: A unified benchmark for evaluating perception and functional utility of embodied world models. _arXiv preprint arXiv:2602.08971_ , 2026. 

- [19] Yichao Shen, Fangyun Wei, Zhiying Du, Yaobo Liang, Yan Lu, Jiaolong Yang, Nanning Zheng, and Baining Guo. Videovla: Video generators can be generalizable robot manipulators. _arXiv preprint arXiv:2512.06963_ , 2025. 

- [20] Mohit Shridhar, Yat Long Lo, and Stephen James. Generative image as action models. _arXiv preprint arXiv:2407.07875_ , 2024. 

- [21] Yue Su, Sijin Chen, Haixin Shi, Mingyu Liu, Zhengshen Zhang, Ningyuan Huang, Weiheng Zhong, Zhengbang Zhu, Yuxiao Liu, and Xihui Liu. World guidance: World modeling in condition space for action generation. _arXiv preprint arXiv:2602.22010_ , 2026. 

- [22] Wei-Cheng Tseng, Jinwei Gu, Qinsheng Zhang, Hanzi Mao, Ming-Yu Liu, Florian Shkurti, and Yen-Chen Lin. Scalable policy evaluation with video world models. _arXiv preprint arXiv:2511.11520_ , 2025. 

- [23] Vitalis Vosylius, Younggyo Seo, Jafar Uruç, and Stephen James. Render and diffuse: Aligning image and action spaces for diffusion-based behaviour cloning. _arXiv preprint arXiv:2405.18196_ , 2024. 

- [24] Wan Team. Wan2.2: Open and advanced large-scale video generative models. `https:// github.com/Wan-Video/Wan2.2` , 2025. GitHub repository and model release. 

- [25] Wan Team. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_ , 2025. 

- [26] Jialong Wu, Shaofeng Yin, Ningya Feng, Xu He, Dong Li, Jianye Hao, and Mingsheng Long. iVideoGPT: Interactive videogpts are scalable world models. In _Advances in Neural Information Processing Systems_ , 2024. 

- [27] Zhuoyi Yang, Jiayan Teng, Wendi Zheng, Ming Ding, Shiyu Huang, Jiazheng Xu, Yuanming Yang, Wenyi Hong, Xiaohan Zhang, Guanyu Feng, Da Yin, Xiaotao Gu, Yuxuan Zhang, Weihan Wang, Yean Cheng, Ting Liu, Bin Xu, Yuxiao Dong, and Jie Tang. CogVideoX: Text-tovideo diffusion models with an expert transformer. In _International Conference on Learning Representations_ , 2025. 

- [28] Seonghyeon Ye, Yunhao Ge, Kaiyuan Zheng, Shenyuan Gao, Sihyun Yu, George Kurian, Suneel Indupuru, You Liang Tan, Chuning Zhu, Jiannan Xiang, et al. World action models are zero-shot policies. _arXiv preprint arXiv:2602.15922_ , 2026. 

- [29] Haoyu Zhen, Zixian Gao, Qiao Sun, Yilin Zhao, Yuncong Yang, Yilun Du, Pengsheng Guo, Tsun-Hsuan Wang, Yi-Ling Qiao, and Chuang Gan. Action images: End-to-end policy learning via multiview video generation. _arXiv preprint arXiv:2604.06168_ , 2026. 

- [30] Jinliang Zheng, Jianxiong Li, Dongxiu Liu, Yinan Zheng, Zhihao Wang, Zhonghong Ou, Yu Liu, Jingjing Liu, Ya-Qin Zhang, and Xianyuan Zhan. Universal actions for enhanced embodied foundation models. _arXiv preprint arXiv:2501.10105_ , 2025. 

- [31] Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin Burchfiel, Paarth Shah, and Abhishek Gupta. Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. _arXiv preprint arXiv:2504.02792_ , 2025. 

- [32] Fangqi Zhu, Hongtao Wu, Song Guo, Yuxiao Liu, Chilam Cheang, and Tao Kong. IRASim: A fine-grained world model for robot manipulation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2025. 

11 

## **A Appendix** 

### **A.1 Detailed Network Architecture Pipeline** 

This section describes the full EA-WM network pipeline. We focus on how RGB videos, KVAFs, and event-difference targets are processed by the Wan2.2-based architecture. 

**Latent preparation.** Given an RGB video sequence **X** = _{Iτ }_<sup>_T_</sup> _τ_ =1<sup>,thecorrespondingKVAF</sup> sequence **K** , and text condition **c** , EA-WM first encodes both videos and KVAFs with the same pretrained video VAE: 

**z**<sup>_v_</sup> 0<sup>= VAE(</sup><sup>**X**)</sup><sup>_,_</sup> **z**<sup>_k_</sup> 0<sup>= VAE(</sup><sup>**K**)</sup><sup>_._</sup> 

This places the target video and action-derived KVAFs in a shared latent space. During flow-matching training, both latents are perturbed at timestep _t_ , producing noised latents **z**<sup>_v_</sup> _t_<sup>and</sup><sup>**z**</sup><sup>_k_</sup> _t_<sup>together with</sup> their training targets **Y**<sup>_v_</sup> and **Y**<sup>_k_</sup> . 

**Dual-stream denoising.** After patchification, the video latent and KVAF latent are represented as two token streams, 

**H**<sup>_v_</sup> 0<sup>=</sup><sup>_P_(</sup><sup>**z**</sup> _t_<sup>_v_)</sup><sup>_,_</sup> **H**<sup>_k_</sup> 0<sup>=</sup><sup>_P_(</sup><sup>**z**</sup> _t_<sup>_k_)</sup><sup>_._</sup> 

The video stream follows the original Wan2.2 DiT blocks, while the KVAF stream is processed by a full-depth copy of the DiT blocks. Event-aware fusion modules are inserted at a sparse set of layers _S_ , allowing the two streams to exchange information only at selected depths. This keeps the KVAF branch expressive while avoiding dense, overly expensive cross-stream interaction. 

**Event-Difference Latent Supervision.** EA-WM uses frame-difference latents as event supervision. Given the input video, we compute 


and encode the difference sequence with the same video VAE: 


This target supervises the event prediction branch in each fusion module. Since the event prediction and event gate share the same event representation, EDLS also shapes the gate that controls video– KVAF cross-attention. 

**Algorithm 1** EA-WM training step 

**Require:** RGB video **X** , KVAF sequence **K** , text condition **c** , fusion layers _S_ 1: Encode latents: **z**<sup>_v_</sup> 0<sup>_←_VAE(</sup><sup>**X**),</sup><sup>**z**</sup><sup>_k_</sup> 0<sup>_←_VAE(</sup><sup>**K**)</sup> 

2: Sample timestep _t_ and construct noised latents and flow targets: 

( **z**<sup>_v_</sup> _t_<sup>_,_</sup><sup>**Y**</sup><sup>_v_)</sup><sup>_,_(</sup><sup>**z**</sup><sup>_k_</sup> _t_<sup>_,_</sup><sup>**Y**</sup><sup>_k_)</sup><sup>_←_FlowMatch(</sup><sup>**z**</sup><sup>_v_</sup> 0<sup>_,_</sup><sup>**z**</sup> 0<sup>_k, t_)</sup> 3: Construct EDLS target: **E** _←_ VAE( _{|Iτ − Iτ −_ 1 _|}_<sup>_T_</sup> _τ_ =1<sup>)</sup> 4: Patchify: **H**<sup>_v_</sup> 0<sup>_←P_(</sup><sup>**z**</sup> _t_<sup>_v_),</sup><sup>**H**</sup><sup>_k_</sup> 0<sup>_←P_(</sup><sup>**z**</sup> _t_<sup>_k_)</sup> 5: **for** _ℓ_ = 1 to _L_ **do** 6: Update KVAF stream: **H**<sup>¯</sup><sup>_k_</sup> _ℓ_<sup>_←Bℓ_(</sup><sup>**H**</sup><sup>_k_</sup> _ℓ−_ 1<sup>_,_</sup><sup>**c**</sup><sup>_, t_)</sup> 7: **if** _ℓ ∈S_ **then** 8: **H** ˜<sup>_v_</sup> _ℓ−_ 1<sup>_,_</sup><sup>**H**</sup> _ℓ_<sup>_k,_ˆ</sup><sup>**E**</sup><sup>_ℓ←_EventFusion</sup><sup>_ℓ_(</sup><sup>**H**</sup><sup>_v_</sup> _ℓ−_ 1<sup>_,_</sup><sup>**H**¯</sup><sup>_k_</sup> _ℓ_<sup>)</sup> 9: **else** 10: **H** ˜<sup>_v_</sup> _ℓ−_ 1<sup>_←_</sup><sup>**H**</sup><sup>_v_</sup> _ℓ−_ 1<sup>,</sup> **H**<sup>_k_</sup> _ℓ_<sup>_←_</sup><sup>**H**¯</sup> _ℓ_<sup>_k_</sup> 11: **end if** 12: Update video stream: **H**<sup>_v_</sup> _ℓ_<sup>_←Dℓ_( ˜</sup><sup>**H**</sup><sup>_v_</sup> _ℓ−_ 1<sup>_,_</sup><sup>**c**</sup><sup>_, t_)</sup> 13: **end for** 14: Predict **Y**<sup>ˆ</sup><sup>_v_</sup> _←_ Head _v_ ( **H**<sup>_v_</sup> _L_<sup>),</sup> **Y** ˆ<sup>_k_</sup> _←_ Head _k_ ( **H**<sup>_k_</sup> _L_<sup>)</sup> 15: Compute _L_ = _ω_ ( _t_ )( _∥_ **Y**<sup>ˆ</sup><sup>_v_</sup> _−_ **Y**<sup>_v_</sup> _∥_<sup>2</sup> 2<sup>+</sup><sup>_∥_</sup><sup>**Y**ˆ</sup><sup>_k −_</sup><sup>**Y**</sup><sup>_k∥_2</sup> 2<sup>) +</sup><sup>_λ_evt</sup><sup>_L_EDLS</sup> 16: **return** _L_ 

12 

**Algorithm 2** Event-aware bidirectional fusion at layer _ℓ_ 

**Require:** Video tokens **H**<sup>_v_</sup> _ℓ−_ 1<sup>, KVAF tokens</sup><sup>**H**¯</sup><sup>_k_</sup> _ℓ_ 1: Predict event gate and event latent: 


**Event-aware bidirectional fusion.** The fusion block is the key interaction module between the video stream and the KVAF stream. It first predicts a shared event representation, from which both the event gate and the event latent are derived. The event latent is supervised by EDLS, while the event gate modulates the strength of bidirectional cross-attention. Therefore, EDLS affects video generation not only through an auxiliary prediction loss, but also through the gate that controls information exchange between the two streams. 

**Training objective.** The full training loss consists of video flow matching, KVAF flow matching, and EDLS: 


The video loss trains the future video generation branch, the KVAF loss encourages the KVAF branch to preserve structured robot geometry, and EDLS guides the fusion modules to focus on motion and interaction changes. 

### **A.2 KVAF Construction** 

This section describes how we construct _Structured Kinematic-to-Visual Action Fields_ (KVAFs) from robot actions and kinematic states. KVAFs are designed to convert low-dimensional robot-side information into camera-aligned visual action fields, so that action conditioning can be expressed in the same image domain as future video generation. 

**Inputs.** For each episode, we assume access to the robot URDF, embodiment configuration, camera parameters, and per-frame robot states. At time step _t_ , the input to KVAF construction is 


where **q**<sup>_L_</sup> _t_<sup>_,_</sup><sup>**q**</sup><sup>_R_</sup> _t_<sup>are the left/right arm joint values,</sup><sup>_g_</sup> _t_<sup>_L, g_</sup> _t_<sup>_R_are normalized gripper states,</sup><sup>**_ξ_**</sup><sup>_L_</sup> _t_<sup>_,_</sup><sup>**_ξ_**</sup><sup>_R_</sup> _t_<sup>are</sup> end-effector poses, and ( **K** _t,_ **E** _t_ ) are camera intrinsics and extrinsics. Each end-effector pose is represented by a 3D position and a quaternion: 


**Kinematic lifting.** We first lift low-dimensional joint states into 3D robot geometry using forward kinematics. Let **T**<sup>_W_</sup> _a,k_<sup>(</sup><sup>_t_)</sup><sup>_∈SE_(3) denote the world-frame transform of the</sup><sup>_k_-th link of arm</sup><sup>_a_at time</sup> _t_ . Starting from the robot base transform, each link transform is computed recursively: 


13 

where **T**<sup>orig</sup> _a,k_<sup>is the static joint transform parsed from the URDF, and</sup><sup>**T**</sup> _a,k_<sup>motis the revolute or prismatic</sup> motion induced by the joint value. For the gripper, the normalized signal is mapped to a prismatic displacement 


and used to compute the two finger branches. This gives a set of 3D robot keypoints 

including the arm skeleton, joint landmarks, and gripper endpoints. 

**Camera projection.** Each 3D keypoint is projected to the target camera view. For a world-frame point **p**<sup>_W_</sup> , we compute 


and obtain the image coordinate by perspective division: 


Points with non-positive camera depth are discarded. This step maps robot kinematics from the world frame to the exact image plane used by the video world model. 

**Visual rendering.** Given projected keypoints, we render a KVAF frame **V** _t ∈_ R<sup>_H×W ×_3</sup> on a black canvas. The rendered elements include depth-aware arm skeletons, joint landmarks, gripper geometry, end-effector heatmaps, and pose axes. For depth-aware skeleton rendering, we normalize the camera depth _z_ within an episode-level range ( _z_ min _, z_ max) and map it to a color palette: 


where _C_ denotes the depth color map. This allows the visual field to encode not only image-space position, but also relative depth ordering. 

For the end-effector, we render a truncated Gaussian heatmap centered at the projected end-effector location ( _u_<sup>_a_</sup> _t_<sup>_, v_</sup> _t_<sup>_a_):</sup> 


This heatmap provides an explicit cue for the manipulation focus. We further render the local endeffector pose axes. Given the rotation matrix **R**<sup>_a_</sup> _t_<sup>from the end-effector quaternion, each local axis</sup> endpoint is 

**p**<sup>_a,m_</sup> _t_ = **p**<sup>_a_</sup> _t_<sup>+</sup><sup>_ℓ_axis</sup><sup>**R**</sup> _t_<sup>_a_</sup><sup>**e**</sup><sup>_m,_</sup> _m ∈{x, y, z}._ 

After projection, the three axes are drawn in RGB colors. The final KVAF frame is the composition of all rendered components: 


Stacking all frames gives the KVAF sequence 


In the current implementation, KVAFs explicitly encode robot-side geometric motion information. Object-state changes are not directly rasterized in KVAFs, but are later captured through event-aware fusion and EDLS in the generative model. 

Table 5: Rendered components in KVAFs and their roles. 

|Component|Encoded information|
|---|---|
|Depth-aware skeleton|Arm topology, spatial position, and relative depth|
|Joint landmarks|Local joint locations and articulated structure|
|Gripper geometry|End-effector opening state and finger configuration|
|End-effector heatmap|Manipulation focus and target interaction region|
|Pose axes|End-effector orientation and approach direction|


14 

**Algorithm 3** KVAF construction for one episode 

**Require:** Robot URDF, embodiment config, episode states _{It}_<sup>_T_</sup> _t_ =1<sup>, image size (</sup><sup>_H, W_)</sup> **Ensure:** KVAF sequence _V_ = _{_ **V** _t}_<sup>_T_</sup> _t_ =1 1: Parse URDF to obtain joint origins, joint axes, link hierarchy, and gripper joints 2: Build left/right arm kinematic chains from the robot configuration 3: Estimate an episode-level depth range ( _z_ min _, z_ max) from visible robot keypoints 4: **for** _t_ = 1 to _T_ **do** 5: Initialize a black canvas **V** _t ∈_ R<sup>_H×W ×_3</sup> 6: **for** each arm _a ∈{L, R}_ **do** 7: Compute 3D arm and gripper keypoints by forward kinematics: _Pt_<sup>_a←_FK(</sup><sup>**q**</sup><sup>_a_</sup> _t_<sup>_, g_</sup> _t_<sup>_a,_URDF)</sup> 8: Project keypoints to the target camera: Π<sup>_a_</sup> _t_<sup>_←_Project(</sup><sup>_P_</sup> _t_<sup>_a,_</sup><sup>**K**</sup><sup>_t,_</sup><sup>**E**</sup><sup>_t_)</sup> 9: Render depth-aware arm skeleton and joint landmarks on **V** _t_ 10: Render gripper geometry using projected finger keypoints 11: Project end-effector center and render Gaussian heatmap 12: Project end-effector pose axes and render RGB orientation cues 13: **end for** 14: Append **V** _t_ to _V_ 15: **end for** 16: **return** _V_ 

### **A.3 Heuristic Action Recovery from KVAFs** 

This section describes the heuristic procedure used in our additional analysis to recover numerical actions from generated KVAF videos. This procedure is not part of EA-WM training or inference; it is only used to examine whether the visual action fields contain recoverable low-dimensional action information. Given a generated KVAF video, camera intrinsics and extrinsics, and the known rendered pose-axis length, we recover end-effector trajectories, gripper states, and then convert them into RoboTwin-style relative actions. 

**End-effector detection and pose recovery.** For each KVAF frame, we first detect candidate endeffector centers from high-intensity heatmap regions. Around each detected center, we identify the rendered RGB pose-axis endpoints by thresholding local red, green, and blue regions. Let the detected image points be 


where **u** 0 is the end-effector center and **u** _x,_ **u** _y,_ **u** _z_ correspond to the projected local _x, y, z_ axes. We associate them with the canonical 3D local points 


Using the camera intrinsic matrix, we solve a PnP problem to estimate the end-effector pose in the camera frame, and then transform it to the world frame using the camera extrinsics. This gives a recovered pose 


for each detected arm _a_ at time _t_ . 

**Gripper state and bimanual track association.** The gripper state is estimated from the local gripper geometry around the recovered end-effector center. We detect gripper-like white components near the pose axes and use their relative separation as a raw gripper opening signal. Since RoboTwin contains bimanual manipulation, detections are associated into left and right tracks. When two detections are present, we assign them by their recovered world-frame horizontal position. When only one detection is available, we assign it to the closer existing track. Missing detections are filled by nearest-neighbor interpolation, and the recovered pose and gripper sequences are smoothed with a short temporal median filter. Finally, the gripper curve is normalized to [0 _,_ 1] within each episode. 

15 

**Conversion to relative actions.** After obtaining dense left and right end-effector pose sequences, we convert them into RoboTwin-style relative actions. For each arm _a ∈{L, R}_ , the local translation action is computed in the current end-effector frame: 

The relative rotation is 


which is converted to roll-pitch-yaw angles: 


The gripper action is the temporal difference of the normalized gripper state: 


Thus the recovered bimanual action at time _t_ is 


**Evaluation.** We compare the recovered actions with ground-truth action CSVs using group-wise errors for translation, rotation, and gripper commands. Translation and rotation errors are computed as vector norms over the corresponding action dimensions, while the gripper error is computed as absolute error. Because the recovery depends on detecting small rendered cues such as heatmap centers, pose axes, and gripper components, the current heuristic pipeline is not expected to match direct numerical action prediction. Instead, it serves as an analysis tool for probing how much action information can be recovered from the image-domain KVAF representation. 

The relatively low detection rate of this heuristic recovery pipeline reflects the difficulty of inverting image-domain action fields back into precise numerical actions. This supports our view that KVAFs are better suited as a video-domain conditioning interface rather than as a direct replacement for numerical action labels. 

### **A.4 Full-metric evaluation.** 

In the main paper, we focus on Physics Adherence, 3D Accuracy, and Controllability, as these dimensions are most directly related to robot motion, spatial consistency, and action-conditioned generation. For completeness, we additionally report all 16 WorldArena video perception metrics in Tables 6 and 7. Table 6 compares EA-WM with the representative video and embodied world models used in the main quantitative analysis, while Table 7 compares KVAF-conditioned generation with mainstream action- or trajectory-conditioned baselines. Unlike the main-paper P3CScore, which is computed only on the six selected metrics, the appendix Avg16 averages all 16 metrics including Action Following. Across both comparisons, EA-WM and KVAF-conditioned generation achieve the strongest overall Avg16, while also showing consistent advantages on robot-centric metrics such as Interaction Quality, Trajectory Accuracy, Depth Accuracy, and Perspectivity. These results further support that representing actions as camera-aligned KVAFs provides effective structured guidance for robotic video world modeling. 

Table 6: Full WorldArena video perception metrics for the models compared in the main results. All metrics are normalized to [0 _,_ 1] and higher is better. Avg16 averages all 16 metrics, and multiplies the result by 100. 

||Visu|al Qu|ality|Motion Qu|ality|Conten|t Cons|istency|Physics|3|D|Controllability|Avg16|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Model|Img.|Aes.|JEPA|Dyn. Flow|Smooth|Subj.|Bg.|Photo|Inter. Traj.|Depth|Persp.|Instr. Sem. Action||
|CogVideoX|0.358|0.378|0.938|0.317 0.219|0.739|0.808|0.877|0.358|0.594 0.353|0.910|0.783|0.727 **0.898** 0.008|57.91|
|WoW|0.459|0.387|0.744|0.461 0.271|0.769|0.816|0.903|0.217|0.556 0.206|0.728|0.767|0.569 0.884 0.043|54.87|
|Wan 2.2|0.388|0.396|0.758|0.435 0.127|0.702|**0.839**|0.904|**0.478**|0.518 0.163|0.777|0.766|0.538 0.888 0.051|54.55|
|TesserAct|0.332|**0.459**|0.458|0.515 0.245|0.758|0.825|**0.924**|0.249|0.580 0.140|0.716|0.792|0.615 0.878 0.031|53.23|
|GigaWorld-0|0.504|0.399|0.441|0.671 0.312|0.781|0.730|0.856|0.176|0.537 0.155|0.632|0.760|0.616 0.859 0.113|53.39|
|Vidar|0.415|0.407|0.561|0.277 0.143|**0.797**|0.763|0.830|0.235|0.535 0.193|0.787|0.759|0.591 0.883 0.082|51.61|
|Cosmos-Predict 2.5 (text)|**0.667**|0.450|0.313|0.591 **0.430**|0.788|0.749|0.851|0.138|0.387 0.082|0.705|0.796|0.266 0.773 **0.142**|50.80|
|Genie Envisioner|0.231|0.329|0.334|**0.693** 0.086|0.697|0.776|0.902|0.201|0.205 0.068|0.866|0.528|0.203 0.854 0.011|43.65|
|**EA-WM (Ours)**|0.364|0.387|**0.951**|0.360 0.273|0.730|0.827|0.904|0.220|**0.682 0.430 **|**0.959 **|**0.838 **|**0.792** 0.895 0.048|**60.38**|


16 

**Algorithm 4** Heuristic action recovery from KVAF videos 

- **Require:** Generated KVAF video _V_ , camera intrinsics **K** , camera extrinsics **E** , pose-axis length _ℓ_ axis 

- **Ensure:** Recovered relative action sequence _{_ **a** ˆ _t}_ 1: **for** each frame **V** _t_ **do** 2: Detect candidate end-effector centers from heatmap peaks 3: **for** each detected center **do** 4: Detect local RGB pose-axis endpoints ( **u** _x,_ **u** _y,_ **u** _z_ ) 5: Solve PnP using canonical 3D axis points and detected 2D endpoints 6: Convert the recovered camera-frame pose to world frame 7: Estimate raw gripper opening from local gripper geometry 8: **end for** 9: Store all valid detections for frame _t_ 

- 10: **end for** 


- 17: Compute local rotation: 

- 19: **end for** 

- 20: Concatenate left/right translation, rotation, and gripper deltas: 


- 21: **return** _{_ **a** ˆ _t}_ 

Table 7: Full WorldArena video perception metrics for mainstream action- or trajectory-conditioned baselines. All metrics are normalized to [0 _,_ 1] and higher is better. Avg16 averages all 16 metrics, and multiplies the result by 100. 

||Visual Qua|lity|Motion Qu|ality|Conte|nt Con|sistency|Physics|3|D|Controllability|Avg16|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Model|Img.<br>Aes.|JEPA|Dyn. Flow|Smooth|Subj.|Bg.|Photo|Inter. Traj.|Depth|Persp.|Instr. Sem. Action||
|CtrlWorld|0.352 **0.389**|0.919|0.426 **0.345**|**0.738**|**0.841**|0.906|0.173|0.621 0.477|0.930|0.796|0.727 0.891 0.021|59.70|
|IRASim|0.349 0.362|0.933|0.414 0.208|0.705|0.831|0.907|0.352|0.566 0.364|0.931|0.779|0.660 0.885 **0.053**|58.12|
|Cosmos-Predict 2.5 (action)|**0.449** 0.358|0.930|0.399 0.057|0.710|0.820|0.889|**0.353**|0.550 0.295|0.886|0.764|0.584 0.888 0.013|55.91|
|RoboMaster|0.349 0.384|0.297|**0.612** 0.148|0.694|0.830|**0.912**|0.336|0.536 0.116|0.834|0.759|0.577 0.876 0.035|51.84|
|**KVAF-conditioned generation**|0.364 0.383|**0.950**|0.360 0.268|0.729|0.818|0.899|0.229|**0.682 0.494 **|**0.977 **|**0.850 **|**0.784 0.901** 0.048|**60.84**|


### **A.5 Additional Visualizations of Generated KVAFs and Videos** 

To further examine the learned video-domain action representation, we visualize generated KVAF sequences together with the corresponding generated video frames in Figures 6–10. Across different tasks, the generated KVAFs are well aligned with the robot motion in the videos: skeletons, endeffector cues, gripper geometry, and pose axes follow the generated robot configurations, while the video frames maintain consistent object locations and interaction progress. 

### **A.6 Broader Impacts** 

EA-WM is primarily evaluated in simulation, with a preliminary offline evaluation on real-world RH20T data. The model is not deployed for closed-loop control on physical robots in this work. 

17 


Figure 6: Generated KVAF and video frame sequence 

The model does not directly execute robot actions, nor is it deployed on real robots in this work. Nevertheless, more accurate robotic world models may eventually be used as predictive simulators, planning modules, policy-learning aids, or evaluation environments for downstream VLA systems. If such models generate misleading future rollouts, downstream policies or planners may make unsafe decisions, especially in physical environments involving humans, fragile objects, or safety-critical manipulation. 

This work does not involve human-subject data, personally identifiable information, or real-robot deployment. The primary goal is to study how structured action information can improve robotic video world modeling. 

### **A.7 Controlled Analysis of KVAF Representations** 

We further conduct controlled experiments to disentangle the effect of the KVAF representation from additional geometric information and model capacity. _Geometry49_ contains the same robot kinematic states, end-effector poses, gripper states, and camera parameters used to construct KVAFs, but 

18 


Figure 7: Generated KVAF and video frame sequence 

encodes them as a 49-dimensional numerical representation. We additionally consider two simplified image-space representations: _EEF Pose Map_ , which retains only projected end-effector locations and orientations, and _Binary Embodiment Mask_ , which rasterizes the projected robot structure as a binary mask. The visual representation variants use the same dual-stream architecture, fusion design, training configuration, and parameter budget, differing only in the information retained by the visual action representation. 

Despite containing the same underlying robot and camera information, Geometry49 is substantially weaker than Full KVAF, most notably on Trajectory Accuracy (0.230 vs. 0.430) and Depth Accuracy (0.847 vs. 0.959), resulting in a 6.49-point P3CScore gap. The improvement is also concentrated in robot-centric geometry rather than generic visual quality: compared with Geometry49, Binary Mask changes Image Quality, Aesthetic Quality, and Background Consistency only marginally, while improving Trajectory Accuracy by 12.72 points and Depth Accuracy by 8.54 points. This suggests that camera-aligned spatial organization, rather than privileged geometric information alone, is critical for making robot motion and 3D structure easier for the video model to exploit. 

19 


Figure 8: Generated KVAF and video frame sequence 

20 


Figure 9: Generated KVAF and video frame sequence 

21 


Figure 10: Generated KVAF and video frame sequence 

22 

Table 8: Full WorldArena comparison of KVAF with an information-matched numerical representation and simplified visual representations. All individual metrics are normalized to [0 _,_ 1] and higher is better. EWMScore averages all 16 WorldArena metrics and is multiplied by 100; P3CScore averages the six robot-centric metrics used in the main paper and is also multiplied by 100. Aggregate scores are computed from the unrounded metric values. 

|Metric|Full KVAF|Geometry49|Binary Mask|EEF Pose Map|
|---|---|---|---|---|
|_Visual Quality_|||||
|Image Quality|0.364|0.367|0.360|**0.376**|
|Aesthetic Quality|0.387|0.383|0.383|**0.389**|
|JEPA Similarity|**0.951**|0.830|0.939|0.932|
|_Motion Quality_|||||
|Dynamic Degree|0.360|**0.361**|0.345|0.325|
|<br>Flow Score|**0.273**|0.254|0.258|0.245|
|Motion Smoothness|0.730|**0.740**|0.725|0.690|
|_Content Consistency_|||||
|Subject Consistency|**0.827**|0.804|0.812|0.822|
|Background Consistency|**0.904**|0.894|0.891|0.893|
|Photometric Consistency|0.220|0.231|**0.256**|0.248|
|_Physics Adherence_|||||
|Interaction Quality|0.682|0.666|0.682|**0.696**|
|Trajectory Accuracy|**0.430**|0.230|0.357|0.282|
|_3D Accuracy_|||||
|Depth Accuracy|**0.959**|0.847|0.932|0.892|
|<br>Perspectivity|**0.838**|0.828|0.836|0.812|
|_Controllability_|||||
|Instruction Following|**0.792**|0.758|0.780|0.716|
|Semantic Alignment|**0.895**|0.878|0.888|0.880|
|<br>Action Following|0.0480|0.0476|0.0475|**0.0491**|
|**EWMScore**|**60.38**|56.99|59.32|57.79|
|**P3CScore**|**76.60**|70.11|74.60|71.30|


23 


Figure 11: Qualitative comparison of simplified visual action representations and their corresponding RGB rollouts. EEF Pose Map provides sparse end-effector position and orientation cues, whereas Binary Embodiment Mask additionally exposes coarse full-arm geometry in the camera view. 

The simplified visual controls show a consistent hierarchy. EEF Pose Map remains competitive on local Interaction Quality (0.696), but its sparse endpoint cues leave the global arm trajectory and depth structure under-constrained, yielding 0.282 Trajectory Accuracy and 0.892 Depth Accuracy. Binary Mask improves these metrics to 0.357 and 0.932 by explicitly constraining coarse full-arm occupancy, consistent with the qualitative rollouts in Fig. 11. Full KVAF further reaches 0.430 and 0.959 by retaining articulated topology, relative depth, joint locations, gripper state, manipulation focus, and end-effector pose. These results indicate that the advantage of KVAF comes from the structured kinematic content retained in the representation, rather than simply from additional model capacity or rasterizing robot motion into image space. 

### **A.8 Evaluation Protocol and Baseline Reproduction** 

All EA-WM results, ablations, and locally reproduced baselines are evaluated on the released WorldArena validation set using the same evaluation pipeline and preprocessing. For external baselines, we use the results reported by WorldArena, which evaluates representative video and embodied world models under a unified benchmark protocol. We retain these reported values to maintain consistent provenance across the comparison tables. Since complete model-specific posttraining configurations are not available for every baseline, these comparisons should be interpreted as benchmark-level comparisons under a common data split and evaluator, rather than strictly parameteror optimization-matched comparisons. 

As an additional sanity check, we locally post-trained both Wan2.2 and CtrlWorld on the released RoboTwin split using the same overall data and optimization budget as our main experiments, while retaining their original architectures and conditioning interfaces. The reproduced results closely match the corresponding WorldArena values, as summarized in Table 9. The small discrepancies observed for both a text-conditioned model and an action-conditioned model suggest that our local evaluation setup is well aligned with the benchmark protocol. We therefore use the WorldArenareported numbers for external baselines in the main comparisons and use local reproductions primarily as protocol verification. 

24 

Table 9: Local verification of the WorldArena evaluation protocol. Values report EWMScore; the reproduced Wan2.2 and CtrlWorld results closely match the corresponding WorldArena values. 

|Model|WorldArena|Local reproduction|Abs. difference|
|---|---|---|---|
|Wan2.2|54.55|54.62|0.07|
|CtrlWorld|59.70|58.97|0.73|


EA-WM is evaluated under two separately trained configurations, depending on whether future KVAFs are generated jointly with RGB video or supplied as action-derived conditions. In the main joint-generation setting, the model receives only the initial frame and text instruction; both future RGB and KVAF latents are initialized from noise and generated jointly. This setting is compared with text-conditioned world models. We additionally train a KVAF-conditioned variant for comparison with action- or trajectory-conditioned models. In this setting, the action trajectory is first converted into reference KVAFs, which are provided to the model as conditions for RGB generation, while the KVAF prediction head is removed. 

Table 10: Two evaluation configurations of EA-WM. The joint-generation setting evaluates future RGB–KVAF co-generation from an initial observation and text instruction, whereas the KVAFconditioned setting evaluates KVAFs as an explicit action-conditioning interface. 

|Setting|Inference input|KVAF role|Comparison|
|---|---|---|---|
|Joint-generation<br>EA-WM|Initial frame + text|Future RGB and KVAF latents<br>are jointly generated from noise|Text-conditioned<br>models|
|KVAF-conditioned|Initial frame + text + action-|Reference KVAFs condition|Action-/trajectory-|
|EA-WM|derived KVAFs|RGB generation|conditioned<br>models|


This distinction is important when interpreting the two comparison groups: the joint-generation setting evaluates whether EA-WM can jointly model future visual and kinematic evolution from an initial observation and language instruction, whereas the KVAF-conditioned setting evaluates the effectiveness of KVAFs as an explicit action-conditioning interface. The latter therefore has access to a more informative action-derived condition and is not intended as a directly matched replacement for the joint-generation setting. Together, the two evaluations characterize EA-WM both as a generative world model and as an action-conditioned video predictor. 

### **A.9 Computational Overhead** 

EA-WM introduces a second full-depth DiT stream for modeling KVAFs, and therefore has a larger computational footprint than the original single-stream Wan2.2-TI2V-5B backbone. We quantify this overhead in terms of model size, inference latency, GPU memory usage, and KVAF construction cost. 

**Model size and inference overhead.** We benchmark Wan2.2-TI2V-5B and EA-WM on a single NVIDIA A100-SXM4-80GB GPU using bfloat16, 480 _×_ 640 resolution, and 50 denoising steps. All latency results are averaged over three runs after warm-up and include preprocessing, denoising, and RGB VAE decoding. 

Table 11: Computational overhead of EA-WM relative to Wan2.2-TI2V-5B. DiT-side parameter counts exclude the shared video VAE and text encoder. 

|Method|DiT-side Params.|Latency (s)|Peak Memory (GiB)|
|---|---|---|---|
|Wan2.2-TI2V-5B|5.00B|49_._30_±_0_._08|24.79|
|EA-WM (RGB)|10.40B|96_._38_±_0_._05|34.88|
|EA-WM (RGB + KVAF decoding)|10.40B|100_._89_±_0_._07|34.88|


EA-WM contains 10.40B DiT-side parameters, compared with 5.00B for Wan2.2-TI2V-5B. Most of the additional parameters come from the full-depth KVAF branch. For RGB generation, inference 

25 

latency increases from 49.30 s to 96.38 s, corresponding to an increase of 47.08 s (95.5%), while peak allocated GPU memory increases from 24.79 GiB to 34.88 GiB, an increase of 10.09 GiB (40.7%). We therefore do not claim computational or parameter parity with the single-stream Wan2.2 backbone. Decoding the generated KVAF visualization is optional and adds only 4.51 s without further increasing peak GPU memory. 

Importantly, the architectural overhead above should be distinguished from the contribution of the KVAF representation itself. In the capacity-controlled representation analysis in Sec. A.7, we keep the dual-stream architecture, fusion design, training configuration, and parameter budget fixed while changing only the visual action representation. These controlled experiments show that the performance improvement cannot be explained solely by the increased model capacity. 

**KVAF construction cost.** We separately benchmark KVAF construction on an Intel Xeon Platinum 8362 CPU. The measurement includes HDF5 loading, forward-kinematic projection, depth preprocessing, visual-field rendering, and video encoding. The measured processing times are 0.113 s, 0.401 s, 0.722 s, and 0.879 s for trajectories of 9, 33, 65, and 81 frames, respectively. 


Figure 12: Computational profile of EA-WM. **(a)** End-to-end inference latency under the same sampling configuration. EA-WM introduces a 95.5% latency increase over Wan2.2-TI2V-5B, while optional KVAF decoding adds only 4.51 s. **(b)** Peak allocated GPU memory and DiT-side parameter footprint. Most of the additional computational footprint comes from the full-depth KVAF stream. **(c)** CPU cost of KVAF construction as trajectory length increases. Rendering scales approximately linearly at 10.6 ms per frame ( _R_<sup>2</sup> = 0 _._ 998), with an 81-frame sequence requiring 0.879 s. 

As shown in Fig. 12(b), KVAF construction scales approximately linearly with trajectory length, at about 10.6 ms per frame. Even an 81-frame trajectory requires less than 0.9 s to construct, indicating that KVAF rendering itself accounts for only a small fraction of the end-to-end computational cost. The dominant overhead of the current implementation instead comes from iterative denoising through the additional full-depth DiT stream. 

Moreover, in the main joint-generation setting, no reference future KVAF trajectory is required at inference: both future RGB and KVAF latents are initialized from noise and jointly generated. Therefore, reference KVAF construction does not introduce an additional online conditioning cost in the main EA-WM setting. 

Overall, the current implementation incurs substantial overhead primarily because of the full-depth dual-stream architecture, rather than the construction of KVAFs themselves. At the same time, the capacity-controlled experiments in Sec. A.7 separate this architectural cost from the benefit of the structured KVAF representation. Reducing the computational footprint through a shallower or weight-shared KVAF branch, fewer fusion layers, or model distillation is an important direction for future work. 

### **A.10 Functional Utility of EA-WM** 

Beyond perceptual evaluation, we further examine whether the generated KVAF and RGB rollouts can support downstream robot learning, policy evaluation, and action planning. 

**Data Engine.** Following the WorldArena data-engine setting, we evaluate on `adjust_bottle` and `click_bell` . We use a lightweight temporal Transformer to decode generated KVAF sequences into robot actions. Each 81-frame RGB KVAF sequence is encoded frame-wise by a small convolutional 

26 

encoder into 128-dimensional tokens, followed by a 4-layer, 4-head Transformer encoder and an MLP head that predicts an 80-step, 14-dimensional action sequence. The decoder is trained on ground-truth KVAF–action pairs and kept fixed for downstream evaluation. The decoded trajectories are subsequently used to fine-tune the _π_ 0 _._ 5 policy. 

Table 12: Data-engine evaluation on the two WorldArena tasks. Actions decoded from generated KVAF trajectories provide effective supervision for downstream policy learning. 

|Training data|`adjust_bottle`|`click_bell`|Average|
|---|---|---|---|
|Zero-shot_π_0_._5|2%|5%|3.5%|
|WoW|45%|71%|58.0%|
|GT RoboTwin data|77%|66%|71.5%|
|Generated KVAF_→_actions|75%|69%|**72.0%**|


Actions decoded from generated KVAFs achieve 72.0% average success, compared with 58.0% for the strongest reported world-model data engine and 71.5% for the ground-truth RoboTwin-data reference on these two tasks. This result suggests that the jointly generated KVAF stream retains substantial executable information and can serve as a synthetic interface for downstream policy learning. 

**Policy Evaluation.** Following the WorldArena policy-evaluation protocol, we evaluate five _π_ 0 _._ 5 policies trained with 10%, 20%, 30%, 50%, and 100% of the training data. Each policy is evaluated over the full RoboTwin task set with 10 episodes per task, resulting in 500 rollouts per policy. We compare the execution success measured in RoboTwin with the success estimated from EA-WM rollouts using the WorldArena VLM-based success evaluator. The two measurements exhibit strong correlation, with Pearson _r_ = 0 _._ 922 and Spearman _ρ_ = 0 _._ 800. 


Figure 13: Policy evaluation with EA-WM. **(a)** RoboTwin execution success and EA-WM rolloutbased evaluation for policies trained with different data budgets. **(b)** Correlation between real execution success and EA-WM rollout evaluation across the five policies. EA-WM reaches Pearson _r_ = 0 _._ 922 and Spearman _ρ_ = 0 _._ 800. 

The rollout evaluator is somewhat optimistic in absolute success rate, but tracks policy capability consistently as the training-data budget changes. Its Pearson correlation is close to the strongest result reported by WorldArena (CtrlWorld, _r_ = 0 _._ 986) and substantially higher than Cosmos-Predict 2.5 ( _r_ = 0 _._ 483). These results indicate that EA-WM rollouts provide a useful proxy for comparing policies with different capability levels. 

**Action Planning.** Finally, we use the temporal decoder to convert generated KVAF trajectories into executable actions and evaluate them directly in RoboTwin under the WorldArena action-planning protocol. 

27 

Table 13: Action-planning success on the two WorldArena tasks. EA-WM achieves the strongest average success among the compared world-model planners. 

|Planner|`adjust_bottle`|`click_bell`|Average|
|---|---|---|---|
|_π_0_._5 policy|77%|66%|71.5%|
|WoW|20%|21%|20.5%|
|TesserAct|1%|35%|18.0%|
|EA-WM KVAF planning|35%|**97%**|**66.0%**|


EA-WM reaches 66.0% average planning success, substantially outperforming the other worldmodel planners in this comparison and approaching the direct _π_ 0 _._ 5 policy reference. Performance is particularly strong on `click_bell` (97%), while the lower success on `adjust_bottle` (35%) indicates that precise multi-stage manipulation remains challenging. This gap is consistent with the fact that planning depends on both the accuracy of generated KVAF trajectories and the subsequent KVAF-to-action decoding process. 

### **A.11 Preliminary Real-World Evaluation on RH20T** 

We further conduct a preliminary offline evaluation on RH20T to examine whether EA-WM remains effective beyond the simulated RoboTwin setting. We use data collected with a UR5 robot and WSG50 gripper from a fixed global camera, which introduces both real-world appearance and a different robot embodiment from our main experiments. We construct 2,000 short clips for post-training and evaluate on 10 held-out episodes covering 10 tasks. Table 14 reports the six robot-centric metrics used by P3CScore together with the overall aggregate score. 

Table 14: Preliminary real-world evaluation on RH20T. EA-WM achieves the best overall P3CScore, with the largest gains concentrated on interaction, trajectory, and depth modeling. 

||Physics|Adherence|3D Ac|curacy|Contro|llability|||
|---|---|---|---|---|---|---|---|---|
|Model|Inter.|Traj.|Depth|Persp.|Instr.|Sem.|P3CScore|EWMScore|
|CtrlWorld (w/o PT)|0.400|0.279|0.802|0.600|0.276|0.831|53.12|47.97|
|Wan2.2 (w/o PT)|0.362|0.308|0.801|0.738|0.244|0.840|54.88|51.94|
|CtrlWorld (PT)|0.468|0.507|0.889|0.798|0.342|0.867|64.51|54.41|
|Wan2.2 (PT)|0.508|0.563|0.849|**0.858**|**0.378**|**0.877**|67.22|56.51|
|EA-WM (PT)|**0.542**|**0.608**|**0.927**|0.808|0.374|0.866|**68.75**|**57.59**|


EA-WM achieves the best P3CScore of 68.75 and the highest overall EWMScore of 57.59. Compared with the strongest post-trained baseline, Wan2.2, the improvement is most pronounced on the metrics directly targeted by KVAF: Interaction Quality increases from 0.508 to 0.542, Trajectory Accuracy from 0.563 to 0.608, and Depth Accuracy from 0.849 to 0.927. EA-WM does not improve every individual metric, but its gains are concentrated on robot motion and 3D geometry, consistent with the trends observed in the RoboTwin experiments. 

28 


Figure 14: Qualitative rollouts on held-out RH20T episodes. The examples illustrate that EAWM can preserve the overall real-world scene layout while generating plausible robot motion and interaction progress across different tasks. Occasional appearance and geometry drift remain in some rollouts, indicating that real-world generation is still imperfect. 

The qualitative examples in Fig. 14 show a similar trend. EA-WM can preserve the overall scene layout while generating plausible robot motion and interaction progress across held-out real-world tasks, although occasional appearance and geometry drift remain. Since this evaluation is limited to one robot embodiment, one fixed camera, 2,000 post-training clips, and 10 held-out episodes, we view these results as preliminary evidence of real-world transfer rather than a comprehensive evaluation of robustness or embodiment generalization. 

29 

### **A.12 Counterfactual Condition Following** 

We further examine whether EA-WM generates futures that respond to the supplied conditions rather than relying primarily on the initial observation. We construct a counterfactual test in which the initial frame is kept fixed, while both the text instruction and KVAF trajectory are replaced by those from a different task. Specifically, we retain the initial observation from `beat_block_hammer` and replace its original condition with the instruction and KVAF trajectory from `adjust_bottle` . 


Figure 15: Counterfactual condition-following results. Both rollouts start from the same initial observation. The top row uses the original condition ( `beat_block_hammer` ), while the bottom row uses the counterfactual condition ( `adjust_bottle` ). Changing the text and KVAF conditions leads to clearly different robot trajectories while preserving the initial scene context. 

As shown in Fig. 15, the two rollouts share the same initial scene but quickly diverge in their subsequent robot motion. Under the original condition, the arm follows a trajectory concentrated around the original manipulation region, whereas the counterfactual condition induces a distinct approach and motion pattern. Importantly, the surrounding scene and object layout remain largely consistent while the robot trajectory changes, consistent with the model preserving scene context while responding to condition-dependent motion cues. This result provides qualitative evidence that EA-WM does not simply reproduce a canonical continuation associated with the first frame, but uses the supplied text and KVAF trajectory to modulate future robot motion and generate conditiondependent rollouts. 

30 

