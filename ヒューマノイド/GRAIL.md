---
title: "GRAIL: Generating Humanoid Loco-Manipulation from World Models"
date: "2026-06-03"
authors: "Tianyi Xie; Haotian Zhang; Jinhyung Park; Zi Wang; Bowen Wen; Jiefeng Li"
url: https://arxiv.org/abs/2606.05160
pdf: https://arxiv.org/pdf/2606.05160
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.05160)** / [論文ページ](https://arxiv.org/abs/2606.05160)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

_2026-10-20_ 


# **GRAIL: Generating Humanoid Loco-Manipulation from World Models** 

**Tianyi Xie**<sup>1</sup><sup>_,_2</sup><sup>_,_:</sup> **, Haotian Zhang**<sup>1</sup><sup>_,_:</sup> **, Jinhyung Park**<sup>1</sup><sup>_,_:</sup> **, Zi Wang**<sup>1</sup><sup>_,_:</sup> **, Bowen Wen**<sup>1</sup> **, Jiefeng Li**<sup>1</sup> **, Xueting Li**<sup>1</sup> **, Qingwei Ben**<sup>1</sup> **, Haoyang Weng**<sup>1</sup> **, Yufei Ye**<sup>1</sup> **, David Minor**<sup>1</sup> **, Tingwu Wang**<sup>1</sup> **, Chenfanfu Jiang**<sup>2</sup> **, Sanja Fidler**<sup>1</sup> **, Jan Kautz**<sup>1</sup> **, Linxi Fan**<sup>1</sup> **, Yuke Zhu**<sup>1</sup> **, Zhengyi Luo**<sup>1</sup><sup>_,_;</sup> **, Umar Iqbal**<sup>1</sup><sup>_,_;</sup> **, Ye Yuan**<sup>1</sup><sup>_,_;</sup> 

- 1 NVIDIA 2 UCLA 

- : Co-First Authors ; Project Leads 

```
https://research.nvidia.com/labs/dair/grail/
```


Figure 1: **From Fully Digital Data Generation to Real-World Deployment.** GRAIL generates humanoid loco-manipulation data by grounding video world models in fully specified 3D scenes, without physical scene rebuilds or robot teleoperation. _Top:_ simulated humanoids execute generated references spanning pick-up, whole-body manipulation, sitting, and terrain traversal. _Bottom:_ egocentric visual policies trained only on GRAIL-generated data are deployed on a Unitree G1 for stair-climbing and object pick-up. 

> © 2026 NVIDIA. All rights reserved. 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 

## **Abstract** 

**Scaling humanoid loco-manipulation requires robot-compatible demonstrations across diverse objects, whole-body motions, and scene geometries, but teleoperation and motion capture are difficult to scale because each collection depends on physical setups, instrumented actors, and robot operation. We present GRAIL, a digital generation pipeline that remains fully virtual until deployment: it grounds video world models in 3D assets and simulator-ready scenes to synthesize interactions without rebuilding physical environments or teleoperating the robot. Rather than reconstructing unconstrained in-thewild videos, GRAIL starts from fully specified 3D configurations in which object geometry, camera parameters, metric scale, environment depth, and a robot-proportioned character are known before video generation and reused during reconstruction. This privileged setup better conditions 4D recovery, allowing model-based object tracking, human motion estimation, and interaction-aware optimization to reconstruct metric 4D human-object interaction (HOI) trajectories with reduced depth ambiguity and morphology mismatch. We retarget the recovered motions to a humanoid robot and train complementary task-general trackers: an object-aware latent adaptor for manipulation and a scene-aware tracker for terrain traversal. GRAIL produces over 20,000 sequences spanning pick-up, whole-body manipulation, sitting, and terrain traversal. Using only GRAIL-generated data, we train egocentric visual policies through a sim-to-real pipeline and deploy them on a Unitree G1 humanoid, achieving 84% real-world success on diverse object pick-up and 90% success on stair-climbing.** 

## **1. Introduction** 

Humanoid loco-manipulation requires policies that coordinate whole-body balance, object contact, and sceneaware locomotion across a broad distribution of objects and terrain geometries. Scaling the corresponding demonstration data is challenging because each trajectory must be both physically plausible and executable by the target robot. Teleoperation (Aldaco et al., 2024; Ben et al., 2025; Khazatsky et al., 2024; Ze et al., 2025a,b) and motion capture (Lu et al., 2025; Taheri et al., 2020) provide high-quality demonstrations, but they are difficult to scale: each new object or terrain layout can require human-operated robot demonstrations, instrumented actors, and physical scene reconfiguration. Reconstructing robot-ready 4D trajectories from in-the-wild videos (Hou et al., 2023; Kim et al., 2023; Petrov et al., 2023; Wang et al., 2022; Xie et al., 2022, 2026; Zhang et al., 2020) offers broad visual coverage, but requires inferring camera, scale, object geometry, human shape, contacts, and world-space motion from ambiguous monocular observations. Recent advances in 3D asset generation and video world models suggest an alternative route: instead of recovering the entire 3D interaction from an uncontrolled video, can we first specify the 3D scene and then let a world model roll out diverse interactions within it for humanoid policy learning? 

We introduce GRAIL, a humanoid-centric data-generation pipeline that remains fully digital until real-world deployment. It uses video foundation models (VFMs) as world models inside a simulator-ready 3D asset pipeline: rather than reconstructing uncontrolled videos into ambiguous 4D scenes, GRAIL first specifies the object, scene geometry, camera, scale, and robot-proportioned character, lets the VFM roll out the interaction from a rendered view of this scene, then recovers it in 4D within this known metric frame. This design addresses two bottlenecks of prior data sources: it avoids repeated physical collection required by teleoperation and motion capture, and it produces robot-trackable trajectories already aligned with simulation for downstream sim-to-real policy training. 

The recovered 4D HOI trajectories are retargeted to a Unitree G1 and converted into task-general tracking policies built on a pretrained whole-body controller (Luo et al., 2025). Rather than fitting one controller per sequence or per object, we pool related trajectories so the trackers cover families of manipulation and scene-interaction behaviors. This stage uses two complementary specializations: an object-aware latent adaptor that augments the frozen whole-body controller with manipulation by modulating its latent tokens and emitting 

2 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 

hand actions, and a scene-aware tracker that fine-tunes the controller together with a height-map encoder for terrain-conditioned whole-body control. With this pipeline, we generate a large-scale dataset of over 20,000 humanoid loco-manipulation sequences spanning pick-up, whole-body manipulation, sitting, and terrain traversal. Using only this generated data, we train egocentric visual policies (He et al., 2025a) with visual domain randomization and camera alignment as a closed-loop sim-to-real validation; deployed on a Unitree G1, the resulting RGB-based policies perform autonomous loco-manipulation on pick-up and stair-climbing tasks. 

In summary, GRAIL makes the following contributions: (i) a fully digital humanoid-centric data-generation framework that uses VFMs as world models inside a fully specified 3D asset pipeline, producing over 20,000 physically plausible loco-manipulation sequences; (ii) an interaction-aware 4D HOI reconstruction stack that exploits known geometry, metric scale, camera parameters, environment depth, and a robot-proportioned character; (iii) complementary task-general trackers for reconstructed 4D HOI, pairing object-aware latent adaptation for manipulation with scene-aware height-map conditioning for terrain traversal and sitting; and (iv) an end-to-end sim-to-real validation of GRAIL-generated data through egocentric visual policies deployed on a Unitree G1, achieving 84% pick-up success and 90% stair-climbing success in the real world. 

## **2. Related Work** 

**Human-Object Interaction Generation and Reconstruction.** Synthesizing human-object interactions (HOI) requires reasoning about human motion, object affordances, and physical contact. Existing data sources rely on motion capture (Bhatnagar et al., 2022; Fan et al., 2023; Huang et al., 2022; Jiang et al., 2023; Kim et al., 2025b; Li et al., 2023a; Lu et al., 2025; Taheri et al., 2020; Zhang et al., 2023b; Zhao et al., 2024) or RGB-based reconstruction (Hou et al., 2023; Kim et al., 2023; Petrov et al., 2023; Wang et al., 2022; Xie et al., 2022, 2026; Zhang et al., 2020), but remain expensive, category-limited, or underconstrained. Learning-based methods synthesize HOI from affordance, language, or vision-language priors (Dang et al., 2025; Diller and Dai, 2024; Dwivedi et al., 2025; Jiang et al., 2024; Kulkarni et al., 2024; Li et al., 2024; Li and Dai, 2024; Li et al., 2023b; Peng et al., 2025; Wu et al., 2025; Xu et al., 2023, 2024; Ye et al., 2023; Zhang et al., 2023a, 2025; Zheng et al., 2023; Zhou et al., 2022), but physical realism and temporal coherence remain challenging. VFM-based pipelines such as DAViD (Kim et al., 2025a), ZeroHSI (Li et al., 2026), and related methods (Lou et al., 2025) use generated videos as priors for 4D HOI recovery, yet typically leave camera, scale, character morphology, object geometry, or environment structure to be inferred after generation. GRAIL instead specifies the 3D scene before generation and reuses it during reconstruction, yielding robot-compatible 4D HOI trajectories grounded by known metric scale, environment geometry, and a robot-proportioned character, facilitating downstream sim-to-real policy learning. 

**Human Video as Humanoid Supervision.** Human video has become an increasingly important supervision source for humanoids: large-scale mining, retargeting, and robotized-video generation provide broad posecontrol or pretraining data (Mao et al., 2024; Yang et al., 2025), while VideoMimic (Allshire et al., 2025), HumanX (Wang et al., 2026), and related systems (Shi et al., 2026; Weng et al., 2025; Yin et al., 2025; Yu et al., 2025) train interaction policies from third-person, monocular, or egocentric videos. In parallel, physics-based control and whole-body imitation (Fu et al., 2024; He et al., 2024, 2025b; Luo et al., 2023, 2025; Peng et al., 2018, 2021), residual adaptors (Zhao et al., 2025), and multimodal controllers (He et al., 2026; Jiang et al., 2026) show how robot-ready references can be converted into executable policies. The shared bottleneck is data: videos still require recovering metric motion, contacts, object state, and scene geometry, while teleoperation, motion capture, wearable interfaces, and generated robot-video demonstrations (Ben et al., 2025; Khazatsky et al., 2024; Lu et al., 2025; Nai et al., 2026; Patel et al., 2025; Taheri et al., 2020; Ze et al., 2025a,b) remain limited by human effort, retargeting, platform dependence, or morphology mismatch. GRAIL addresses this upstream bottleneck by using video world models for behavioral priors while keeping geometry, scale, camera, environment, and target morphology known, producing robot-compatible 4D references for task-general tracking policies. 

3 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 


Figure 2: **Asset-Conditioned 4D HOI Generation.** Given a 3D object asset, we render a fully specified 3D scene with a character prefitted to the target humanoid and known camera parameters, synthesize a static-camera interaction video via a VFM conditioned on the rendered frame, and reconstruct metric 4D human-object motion by jointly refining initial human and object trajectory estimates with keypoint, depth, and contact losses anchored to the privileged 3D configuration. 

## **3. Method** 

Given a 3D object asset _ℳ_<sup>_𝒪_</sup> , GRAIL produces humanoid loco-manipulation demonstrations comprising humanoid kinematic motion t **Θ**<sup>_ℛ_</sup> _𝑡_<sup>u</sup><sup>_𝑇_</sup> _𝑡_ “1<sup>, object kinematic motion t</sup><sup>**Θ**</sup> _𝑡_<sup>_𝒪_u</sup><sup>_𝑇_</sup> _𝑡_ “1<sup>, and robot actions t</sup><sup>**_𝑎_**</sup> _𝑡_<sup>_ℛ_u</sup><sup>_𝑇_</sup> _𝑡_ “1<sup>.Our data</sup> generation pipeline proceeds in three stages. First, we assemble a fully specified 3D configuration with a character prefitted to the target robot, render an initial frame, and feed it into a VFM to synthesize a reference HOI video t _𝐼𝑡_ u<sup>_𝑇_</sup> _𝑡_ “1<sup>(Sec. 3.1).Second, leveraging the known 3D configuration, we reconstruct coherent 4D HOI</sup> trajectories tp **Θ**<sup>r</sup><sup>_ℋ_</sup> _𝑡_<sup>_,_</sup><sup>**Θ**r</sup><sup>_𝒪_</sup> _𝑡_<sup>qu</sup><sup>_𝑇_</sup> _𝑡_ “1<sup>through human pose estimation, object tracking, and joint optimization (Sec. 3.2).</sup> Third, we retarget the reconstructed motions to the target humanoid and train task-general tracking policies across each task family (Sec. 3.3). Using the generated data, we further train egocentric visual policies through a sim-to-real pipeline and deploy them on a real Unitree G1 for pick-up and stair-climbing (Sec. 3.4). 

### **3.1. Robot-Centric Human Video Generation** 

Although one could generate robot videos directly, current VFMs have stronger priors over human manipulation, and human body and hand reconstruction tools are more mature than robot reconstruction tools. We therefore synthesize human interaction videos using a character asset prefitted to the target humanoid, which facilitates retargeting the recovered motion to the robot. To assemble the 3D configuration, we construct candidate environments using Infinigen (Raistrick et al., 2023) and position the human asset in a rest pose alongside the object. We use rigid body simulation (Macklin et al., 2016) to settle the object into a stable, collision-free initial configuration **Θ**<sup>_𝒪_</sup> 1<sup>.WethenrenderthefirstframeusingBlenderwithknowncameraintrinsics</sup><sup>**_𝐶_**</sup><sup>_𝐾_PR3ˆ3</sup> and extrinsics **_𝐶_** _𝐸_ “ p **_𝑟_**<sup>_𝒞_</sup> _,_ **_𝑡_**<sup>_𝒞_</sup> q. The generated environment serves two purposes: realistic visual context for VFM generation and a ground-truth point cloud for metric-scale depth alignment during reconstruction (Sec. 3.2). A VLM (OpenAI, 2024) generates an interaction prompt from the rendered frame, and a VFM ( _e.g_ ., Kling (Kuaishou, 2025)), acting as a world model, then rolls out the reference HOI video t _𝐼𝑡_ u<sup>_𝑇_</sup> _𝑡_ “1<sup>under a</sup> static-camera setting that preserves the known camera parameters p **_𝐶_** _𝐾,_ **_𝐶_** _𝐸_ q for reconstruction. 

### **3.2. Interaction-Aware HOI Reconstruction** 

Given the generated interaction video, we recover the 4D HOI trajectory tp **Θ**<sup>r</sup><sup>_ℋ_</sup> _𝑡_<sup>_,_</sup><sup>**Θ**r</sup><sup>_𝒪_</sup> _𝑡_<sup>qu</sup><sup>_𝑇_</sup> _𝑡_ “1<sup>in two steps:inde-</sup> pendent initial estimation of human and object motion, followed by interaction-aware joint optimization that anchors the trajectories to the privileged 3D configuration. 

#### **3.2.1. Initial Motion Estimation** 

We first estimate human and object motion independently, yielding initial world-space trajectories t **Θ**<sup>p</sup><sup>_ℋ_</sup> _𝑡_<sup>u</sup><sup>_𝑇_</sup> _𝑡_ “1 and t **Θ**<sup>p</sup><sup>_𝒪_</sup> _𝑡_<sup>u</sup><sup>_𝑇_</sup> _𝑡_ “1<sup>.</sup> 

4 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 

**Human Motion Estimation.** For the human body, GENMO (Li et al., 2025) provides per-frame SMPL-X (Pavlakos et al., 2019) pose parameters from the generated video in camera space; the body shape is held fixed at the prefitted character morphology from Sec. 3.1 rather than re-estimated, so GENMO only contributes per-frame pose parameters. The camera-space motion is then transformed into world coordinates using the known camera extrinsics **_𝐶_** _𝐸_ . For the hands, WiLoR (Potamias et al., 2025) refines per-frame MANO (Romero et al., 2017) parameters for the left and right hands independently; missing detections due to partial occlusion or detection failure are filled via temporal linear interpolation and smoothed with a Savitzky-Golay filter (Savitzky and Golay, 1964) to suppress per-frame jitter. The smoothed hand poses are integrated into the SMPL-X body through wrist inverse-kinematic (IK) alignment, preserving the WiLoR-predicted finger configuration. 

**Object Pose Tracking.** For the object, we fine-tune FoundationPose (Wen et al., 2024) on its proposed synthetic dataset for 5 epochs with the depth channels zeroed at both training and inference to adapt to our RGB-only setup; at inference, the 6-DoF tracker is initialized from the known first-frame pose **Θ**<sup>_𝒪_</sup> 1<sup>and propagates the</sup> object pose across all frames. FoundationPose requires known object geometry, texture, and camera parameters, all available in our pipeline by construction, which ensures accurate object tracking. We additionally validate tracking quality by comparing predicted poses against SAM2 (Ravi et al., 2024) segmentation masks and discard sequences with inconsistent geometry (Sec. A.3). 

#### **3.2.2. Joint Optimization** 

Directly combining the independent reconstructions often produces misaligned interactions (floating contacts, penetration, and depth-scale drift). We therefore jointly refine both trajectories through a global optimization over all frames, holding the hand poses fixed for stability. Rather than optimizing full trajectories directly, we optimize residual motion parameters t∆ **Θ**<sup>_ℋ_</sup> _𝑡_<sup>u</sup><sup>_𝑇_</sup> _𝑡_ “1<sup>and t∆</sup><sup>**Θ**</sup> _𝑡_<sup>_𝒪_u</sup><sup>_𝑇_</sup> _𝑡_ “1<sup>;the final poses are</sup><sup>**Θ**</sup> _𝑡_<sup>_ℋ_“</sup><sup>**Θ**p</sup><sup>_ℋ_</sup> _𝑡_<sup>‘ ∆</sup><sup>**Θ**</sup><sup>_ℋ_</sup> _𝑡_ and **Θ**<sup>_𝒪_</sup> _𝑡_ “ **Θ**<sup>p</sup><sup>_𝒪_</sup> _𝑡_<sup>‘∆</sup><sup>**Θ**</sup><sup>_𝒪_</sup> _𝑡_<sup>,with‘denotingresidualtranslationandrotationupdatesandthe6Drotation</sup> representation (Zhou et al., 2019) used for continuous parameterization. The full refinement objective is: 


**Keypoint Alignment.** To keep the optimized human trajectory aligned with the generated video, we minimize the distance between projected and detected 2D body and hand keypoints: 


where _𝑝𝑡_ P R<sup>_𝐽_ˆ3</sup> are 2D keypoints obtained from body and hand keypoint estimators (Potamias et al., 2025; Xu et al., 2022), and _𝒦_<sup>_ℋ_</sup> p¨q projects the SMPL-X parameters using the known camera. 

**Object Projection Alignment.** Since FoundationPose provides image-aligned object poses, we regularize the optimized object pose to preserve that alignment: 


where _𝒫_ p¨q is the camera projection function, and _𝑉𝑡_<sup>_𝒪_</sup> and _𝑉_<sup>p</sup> _𝑡_<sup>_𝒪_</sup> are object vertices under the optimized and initial poses. 

**Depth Alignment.** Leveraging the known 3D configuration, we first estimate a depth map with MoGe-2 (Wang et al., 2025) and align it to the ground-truth background depth rendered from the environment, recovering metric-scale depth. We then segment human and object regions with SAM2 (Ravi et al., 2024) and unproject 

5 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 

them into per-frame point clouds **P**<sup>_ℋ_</sup> _𝑡_<sup>and</sup><sup>**P**</sup><sup>_𝒪_</sup> _𝑡_<sup>.The depth-alignment loss encourages the reconstructed meshes</sup> to match these point clouds: 


where _𝑉𝑡_<sup>_ℋ,_vis</sup> and _𝑉𝑡_<sup>_𝒪,_vis</sup> are visible mesh vertices and _𝒞𝒟_ is bidirectional Chamfer distance. 

**Contact Alignment.** To encourage physically plausible contact, we query a VLM (OpenAI, 2024) on uniformly sampled video frames to predict per-frame contact labels ( _e.g_ ., left or right hand) and propagate each label to its surrounding interval. Using these labels, we identify the relevant SMPL-X vertices _𝑉𝑡_<sup>_ℋ,_cont</sup> via SMPL-X part segmentation and apply the contact loss only to frames where contact is detected. Since the image-space losses already enforce projection consistency, the contact loss only needs to resolve depth discrepancies, so we restrict it to object vertices whose projected positions overlap with the contact body region and penalize only their depth offset: 


where _𝒯𝑐_ is the set of frames where contact is detected. The filter _ℱ_ projects both vertex sets to screen space and keeps the object vertices whose projections fall within a distance threshold of the contact body vertices, and _𝒞𝒟𝑧_ p¨ _,_ ¨q is a depth-only bidirectional Chamfer distance that penalizes the positional difference along the viewing direction. _𝐿_ cont is disabled for terrain-only sequences without hand-object interaction. 

**Regularization.** The regularization term decomposes as _𝐿_ reg “ _𝐿_ foot ` _𝐿_ vel ` _𝐿_ smooth. _𝐿_ foot leverages per-frame foot contact labels from GENMO (Li et al., 2025) to penalize foot vertex displacement during detected contact frames, suppressing foot skating. _𝐿_ vel regularizes the optimized pelvis velocity to match GENMO’s global-space velocity estimate, suppressing the depth-direction oscillations that camera-space estimates exhibit under depth-scale ambiguity. _𝐿_ smooth penalizes the first- and second-order temporal finite differences of the human and object mesh vertex positions for temporal coherence. 

### **3.3. Task-General Loco-Manipulation Tracking** 

This robot-proportioned reconstruction allows GMR (Araújo et al., 2025) to retarget the SMPL-X motion t **Θ**<sup>r</sup><sup>_ℋ_</sup> _𝑡_<sup>u</sup><sup>_𝑇_</sup> _𝑡_ “1<sup>to the Unitree G1 with reduced morphology mismatch, better preserving hand-object and body-scene</sup> contacts. The result is a kinematic reference motion t **_𝑞_** r _𝑡_ u<sup>_𝑇_</sup> _𝑡_ “1<sup>in the robot’s joint space, while the reconstructed</sup> object trajectory t **Θ**<sup>r</sup><sup>_𝒪_</sup> _𝑡_<sup>u</sup><sup>_𝑇_</sup> _𝑡_ “1<sup>provides the reference object pose. We then train tracking policies built on SONIC (Luo</sup> et al., 2025), a pretrained whole-body controller, to convert these retargeted 4D HOI trajectories into robotaction data. Rather than fitting a controller per sequence or per object, we train task-general policies across each task family; as related trajectories are added, existing policies provide initialization for fine-tuning, amortizing adaptation across the pool. As outlined in Fig. 3, we instantiate this stage with two complementary specializations: an _object-aware_ latent adaptor trained on object-manipulation trajectories and a _scene-aware_ tracker trained on terrain traversal and chair-sitting trajectories. The object-aware adaptor adds hand actions and modulates the latent tokens fed to the controller’s frozen action decoder, enabling manipulation while preserving the locomotion prior; the scene-aware tracker fine-tunes the controller with a height-map encoder, improving terrain-conditioned whole-body control for traversal and scene interaction. 

**Object-Aware Tracking.** For object-manipulation 4D HOI trajectories, we extend the pretrained whole-body controller with an object-aware adaptor policy _𝜋𝜑_ that modulates its latent token space and emits hand actions, giving the frozen controller object-manipulation capability while preserving its pretrained locomotion behavior. The controller encodes kinematic motion targets into a discrete latent token **_𝑧_** _𝑡_ “ _ℰ_ p **_𝑞_** r _𝑡_ q via finite scalar quantization and decodes them into joint-level actions through _𝒢_ p **_𝑧_** _𝑡_ q. We keep its encoder, quantizer, and 

6 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 


Figure 3: **Task-General Tracking via Complementary Controller Adaptation.** Retargeted 4D HOI trajectories are converted into robot-action data by adapting different parts of a pretrained whole-body controller. Objectmanipulation trajectories are used to train an object-aware adaptor _𝜋𝜑_ while the controller remains frozen: the adaptor observes proprioception **_𝑠_** _𝑡_ and an object reference **_𝑜_** _𝑡_ , injects a latent residual ∆ **_𝑧_** _𝑡_ , and emits hand actions **_𝑎_**<sup>hand</sup> _𝑡_ . Terrain traversal and chair-sitting trajectories are used to fine-tune the controller with a sceneaware height encoder _𝜖ℎ_ : the encoder maps the local height map _ℎ𝑡_ into terrain context for scene-conditioned whole-body control. 

decoder frozen, then train only _𝜋𝜑_ to inject manipulation-specific residuals. The adaptor observes proprioception **_𝑠_** _𝑡_ and an object reference **_𝑜_** _𝑡_ consisting of the object pose in robot body frame, hand-to-object transforms, finger contact forces, a precomputed basis point set (BPS) (Prokudin et al., 2019) shape encoding, and, critically, delta observations encoding the difference between the reference future object pose and the current simulated pose. It outputs a 64-dim latent residual ∆ **_𝑧_** _𝑡_ together with a 2-dim binary hand primitive **_𝑎_**<sup>hand</sup> _𝑡_ that maps to 7 finger DoFs per hand: 


with _𝜆_ “ 0 _._ 1 scaling the residual before FSQ quantization. Each hand primitive produces a binary open/close grasp signal, which is mapped to 7 finger joint positions per hand via predefined grasp configurations. The BPS encoding provides the adaptor with object-shape awareness, enabling a single _𝜋𝜑_ to track motions across diverse object geometries. An auxiliary _ℓ_ 2 penalty is applied on ∆ **_𝑧_** _𝑡_ to encourage the adapted latent to remain close to the pretrained controller’s behavior. 

**Scene-Aware Tracking.** For tasks involving scene-aware interactions, such as stepping over curbs, climbing up stairs, and sitting on chairs, the controller’s flat-ground prior is not directly usable. We therefore fine-tune the controller on a mixture of reconstructed 4D HOI scene-interaction trajectories and its original flat-ground data, while augmenting the encoder input with a local height map _ℎ𝑡_ around the robot processed by a 2Dconvolutional projector _𝜖ℎ_ . This preserves the base locomotion distribution while teaching the controller to adapt whole-body motions to terrain and scene geometry. To stabilize the training, in addition to the action decoder _𝒢_ , we train a parallel kinematic decoder _𝒢_ rec that reconstructs the input motion targets to provide an auxiliary MSE loss that regularizes the latent to remain faithful to the trajectory. 


where **_𝑥_** r _𝑖,𝑡_ and **_𝑥_** _𝑖,𝑡_ are reference and simulated quantities spanning root pose, per-body positions and orien- 

7 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 

tations, and linear and angular velocities; for object-aware tracking we additionally boost the weight on the wrist links to encourage accurate hand placement. For object-aware tracking, the total reward adds an object term and a contact-gated grasp term, _𝑅𝑡_ “ _𝑅𝑡_<sup>motion</sup> ` _𝑅𝑡_<sup>reg</sup> ` _𝑅𝑡_<sup>obj</sup> ` ⊮t _𝐶𝑡_ u _𝑅𝑡_<sup>grasp</sup> , where ⊮t _𝐶𝑡_ u is a per-frame contact indicator carried by the reconstructed trajectory, so the grasp reward is active only during contact phases. The _object tracking reward_ penalizes deviation from the reference object pose: 


with scaling coefficients _𝛼𝑝, 𝛼𝑟_ ą 0. The _grasp reward_ combines three terms per hand: 


The first term rewards sustained finger contact with the object (saturating at _𝑁_ min contacts), the second encourages the thumb and index finger to approach from opposing sides for a stable pinch grasp ( **_𝑑_**<sup>thumb</sup> _𝑡_ , **_𝑑_**<sup>index</sup> _𝑡_ are vectors from the object center to each fingertip), and the third draws all fingertips **_𝑓_** _𝑗,𝑡_ toward the object contact centroid **_𝑐_** _𝑡_ . Since scene-aware tasks involve no hand-object interaction, the scene-aware tracker uses only _𝑅𝑡_<sup>motion</sup> and _𝑅𝑡_<sup>reg</sup> . 

**Training.** We train each stage with PPO (Schulman et al., 2017) in Isaac Lab on 64 NVIDIA L40 GPUs, running for 30,000 iterations with 1,024 environments per GPU. Object-aware tracking updates only _𝜋𝜑_ while the controller’s encoder, quantizer, and decoder remain frozen. Scene-aware tracking instead fine-tunes the controller together with the height-map encoder _𝜖ℎ_ . Multiple reference motions are trained jointly within each task family, with environments sampling motions from a shared 4D HOI pool, and we apply reference state initialization at every episode reset. 

Full reward definitions and implementation details are provided in Appendix B. 

### **3.4. Sim-to-Real Deployment** 

For sim-to-real deployment, we distill the object-aware and scene-aware tracking policies into separate egocentric visual policies (Chi et al., 2023; He et al., 2025a; Luo et al., 2025) for object pick-up and stair-climbing, respectively. The deployed models consume head-camera RGB inputs and output the latent tokens of the SONIC controller, and are trained with domain randomization to facilitate sim-to-real transfer. To deploy on the real Unitree G1, we connect the robot to a desktop with an NVIDIA RTX 5090 GPU and stream visual and proprioceptive input to the desktop before streaming robot actions to the G1. We use a Luxonis OAK-D W camera on the G1 and run inference at 10 Hz. 

## **4. Results** 

Our experiments cover the three stages of the GRAIL pipeline. We first evaluate whether the generated 4D HOI sequences are more physically executable than existing generation baselines. We then ask whether these 4D HOI sequences can be converted into task-general loco-manipulation policies at scale, rather than only replayed through per-sequence tracking. Finally, we demonstrate the practical value of the generated data by deploying egocentric visual policies on the real robot for autonomous loco-manipulation. 

8 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 


Figure 4: **Generated Loco-Manipulation Data.** Representative simulated Unitree G1 executions from the generated dataset span pick-up, whole-body manipulation, sitting, and terrain traversal across diverse objects and scene geometries. 

9 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 

||**Geom**|**etric**|**Perceptual**|**Smooth**|**ness**|**Ph**|**ysical Execu**|**tability**|
|---|---|---|---|---|---|---|---|---|
|**Methods**|ContactÓ|Pen. Ó|Inter. ScoreÒ|Human Smo. Ó|Obj Smo. Ó|SRÒ|Body Dev. Ó|Obj Dev. Ó|
|HOIDiff (Peng et al.,2025)|0.012|2.07%|1.79|0.0043|0.0118|15.8%|0.2120|0.3352|
|CHOIS (Li et al.,2024)|0.034|3.74%|2.47|0.0055|0.0062|10.5%|0.2564|0.3642|
|DAViD (Kim et al.,2025a)|0.246|1.46%|2.74|**0.0024**|0.0605|24.0%|0.4723|0.5826|
|Ours|**0.008**|**0.90%**|**3.58**|0.0033|**0.0022**|**88.9%**|**0.0913**|**0.0851**|


Table 1: **Comparison of HOI Generation.** Geometric quality, perceptual realism (Interaction Score, 1-5 scale), motion smoothness, and physics-based tracking on the shared 20-object evaluation set. 

|**Method**|SRÒ|ObjPosÓ|MPJPE-LÓ|
|---|---|---|---|
|HDMI (Weng et al.,2025)|48.5%|0.283|122.3|
|ResMimic (Zhao et al.,2025)|49.2%|0.393|80.9|
|Ours w/o SONIC|45.0%|0.395|243.5|
|Ours w/o_𝜋𝜑_|39.7%|0.303|**37.1**|
|Ours w/o Rel. Obs.|57.9%|0.257|43.0|
|Ours (Full)|**81.4%**|**0.135**|41.8|


Table 2: **Task-General Loco-Manipulation Tracking.** Comparison against loco-manipulation baselines (top) and ablations of GRAIL’s object-aware adaptor (bottom). Metrics: success rate (SR), object position error (ObjPos), and local per-joint error (MPJPE-L). 

### **4.1. Human-Object Interaction Generation** 

**Setup.** We compare the HOI generation component of GRAIL against training-based (CHOIS (Li et al., 2024), HOIDiff (Peng et al., 2025)) and training-free (DAViD (Kim et al., 2025a)) 4D HOI generation approaches on a shared evaluation set of 20 everyday objects from ComAsset (Kim et al., 2024). Detailed baseline configurations are provided in Appendix C.1. 

**Metrics.** We evaluate the generated 4D HOI sequences along three axes. (i) _Geometric quality: contact distance_ (Contact) is the average top- _𝑘_ vertex-to-vertex distance between the SMPL-X human surface and the object surface; _penetration ratio_ (Pen.) is the percentage of SMPL-X vertices that interpenetrate the object mesh. (ii) _Perceptual realism: Interaction Score_ (Inter. Score) is a VLM rating (OpenAI, 2024) of sampled keyframes on a 1-5 scale based on physical plausibility and affordance correctness; _motion smoothness_ for the human (Human Smo.) and the object (Obj Smo.) is the second-order temporal derivative of their vertex trajectories. (iii) _Physical executability:_ we apply InterMimic (Xu et al., 2025), an SMPL-X humanoid tracking framework, to reproduce each method’s 4D HOI sequences in physics simulation using humanoids built from capsule primitives that conform to the input body shape (no motion retargeting required). We report the full-body mean per-joint position deviation (Body Dev.) and the mean object surface deviation (Obj Dev.), and define the tracking success rate (SR) as the fraction of frames where the normalized full-body and object deviations (divided by the object’s maximum dimension) are both below 0 _._ 25. 

**Comparison.** As shown in Table 1, GRAIL achieves the strongest performance across nearly all metrics: the lowest contact distance and penetration ratio, the highest interaction score, the smoothest object trajectories, and, by a large margin, the highest tracking success rate with the lowest body and object deviation. This confirms that the generated 4D HOI sequences are both perceptually realistic and physically executable, making them well-suited for downstream robot learning. We further conduct a user study and present additional qualitative comparisons in Appendix C.1. 

10 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 


Figure 5: **Sim-to-Real Deployment.** Egocentric visual policies trained only on GRAIL-generated data transfer to a Unitree G1 for object pick-up and stair-climbing. 

||||**Seen**|**Objects**|||||**Unsee**|**n Objects**|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Cube|Apple|Tea Box|Carrot|Wet Wipes|**Avg.**|Spray Can|Lint Roller|Peach|Flashlight|Medicine Bottle|**Avg.**|
|SRÒ|100%|60%|100%|70%|90%|**84%**|100%|50%|90%|80%|80%|**80%**|


Table 3: **Sim-to-Real Pick-up Results for Seen and Unseen Objects.** Success rates are computed over 10 trials. 

### **4.2. Task-General Loco-Manipulation Tracking** 

**Scaling Loco-Manipulation Data.** Using the asset-conditioned generation pipeline, we generate a large-scale loco-manipulation dataset for the Unitree G1 with 1,000 object assets sourced from Robocasa (Nasiriany et al., 2024), ComAsset (Kim et al., 2024), OMOMO (Li et al., 2023a), and Hunyuan3D (Team, 2025), paired with 1,000 procedurally generated terrain configurations. The resulting dataset contains over 20,000 sequences (Fig. 4) spanning four categories. _Pick-up_ covers tabletops and the ground, exercising diverse grasp strategies across varying object shapes and placement heights. _Whole-body manipulation_ covers tabletop manipulation motions and mobile interactions in which the robot carries, pushes, or repositions larger items such as boxes and carts while walking. _Sitting_ spans diverse chair styles, requiring approach, lower-body adjustment, and settling into a seated posture. _Terrain traversal_ covers procedurally generated curbs, slopes, and stairs, a setting essential for real-world deployment but underrepresented in existing datasets. 

**Baseline Comparison.** We compare our method against two recent humanoid loco-manipulation baselines, HDMI (Weng et al., 2025) and ResMimic (Zhao et al., 2025), using their official implementations on a benchmark of 124 motions across 43 objects. We report manipulation success rate (SR), object position error (ObjPos), and local mean per-joint position error (MPJPE-L); SR is the fraction of episodes where the average object position error falls below 20 cm. Both train whole-body tracking policies from human references but differ from our approach in two key ways. First, neither method actuates per-finger DoFs, so their evaluated interactions rely on whole-arm or whole-body contact such as carrying, lifting, and pushing. Second, both 

11 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 

train a separate policy per task: ResMimic trains a per-task residual on top of a general motion-tracking base, while HDMI trains one specialist policy per task. In contrast, GRAIL trains task-general policies across large in-family pools of 4D HOI trajectories. As shown in the top block of Table 2, GRAIL outperforms the baselines by a large margin across success rate, object position error, and body tracking accuracy. 

**Ablation Study.** We ablate the object-aware latent adaptor for manipulation cases on the same benchmark and report results in Table 2 (bottom block). Removing SONIC and training from scratch substantially degrades body tracking and reduces success rate. Disabling the latent adaptor _𝜋𝜑_ (i.e., vanilla SONIC) yields the lowest manipulation success rate despite the best body tracking, indicating that accurate body imitation alone is insufficient for object interaction. Replacing relative object observations with absolute ones also decreases success rate. 

### **4.3. Sim-to-Real Deployment** 

To demonstrate GRAIL’s real-world applicability, we deploy trained egocentric visual policies for stair-climbing and diverse object pick-up. For stair-climbing, a policy trained on diverse terrain-traversal sequences from GRAIL achieves a 90% real-world success rate, as shown in Fig. 5. For object pick-up, we train on 200 approachand-pick-up sequences per object across cubes, apples, tea boxes, carrots, and wet wipes. The resulting policy achieves an 84% real-world success rate, as shown in Table 3, and transfers effectively to unseen objects, attaining an 80% success rate. 

## **5. Conclusion** 

We presented GRAIL, a fully digital pipeline for generating humanoid loco-manipulation data from video world models grounded in 3D assets, requiring the physical robot and environment only at deployment. Instead of reconstructing uncontrolled videos, GRAIL starts from fully specified 3D scenes where object geometry and texture, camera parameters, metric scale, environment depth, and robot-proportioned morphology are available by construction. This privileged setup turns key ambiguities in 4D HOI reconstruction into controlled inputs, enabling model-based object tracking, metric depth alignment, and interaction-aware optimization to recover robot-compatible trajectories. The recovered motions are retargeted to the Unitree G1 and converted into complementary task-general trackers: object-aware latent adaptation for manipulation and scene-aware height-map conditioning for terrain traversal and sitting. From over 20,000 generated sequences, we train egocentric visual policies using only GRAIL-generated data and deploy them on a real G1, achieving 84% pick-up success across diverse objects and 90% stair-climbing success. These results suggest that world-modelgenerated data, grounded in known 3D scenes, can complement teleoperation and motion capture as a scalable route toward humanoid loco-manipulation. 

## **6. Limitations** 

Our pipeline assumes 3D object assets, simulator-ready scene setup, and a video world model that follows the requested interaction. Reconstruction quality degrades under severe occlusion, fast motion, or inconsistent object appearance from the VFM, and the failure-filtering step discards a non-trivial fraction of sequences. The task-general tracking policies amortize learning over related 4D HOI pools, but still require training or fine-tuning when the motion family changes substantially. 

12 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 

## **References** 

- Jorge Aldaco, Travis Armstrong, Robert Baruch, Jeff Bingham, Sanky Chan, Kenneth Draper, Debidatta Dwibedi, Chelsea Finn, Pete Florence, Spencer Goodrich, et al. ALOHA 2: An enhanced low-cost hardware for bimanual teleoperation. _arXiv preprint arXiv:2405.02292_ , 2024. 2 

- Arthur Allshire, Hongsuk Choi, Junyi Zhang, David McAllister, Anthony Zhang, Chung Min Kim, Trevor Darrell, Pieter Abbeel, Jitendra Malik, and Angjoo Kanazawa. Visual imitation enables contextual humanoid control. _arXiv preprint arXiv:2505.03729_ , 2025. 3 

- João Pedro Araújo, Yanjie Ze, Pei Xu, Jiajun Wu, and C. Karen Liu. Retargeting matters: General motion retargeting for humanoid motion tracking, 2025. URL `https://arxiv.org/abs/2510.02252` . ICRA 2026. 6 

- Qingwei Ben, Feiyu Jia, Jia Zeng, Junting Dong, Dahua Lin, and Jiangmiao Pang. Homie: Humanoid locomanipulation with isomorphic exoskeleton cockpit. _arXiv preprint arXiv:2502.13013_ , 2025. 2, 3 

- Bharat Lal Bhatnagar, Xianghui Xie, Ilya Petrov, Cristian Sminchisescu, Christian Theobalt, and Gerard Pons-Moll. BEHAVE: Dataset and method for tracking human object interactions. In _CVPR_ , 2022. 3 

- Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 8 

- Lingwei Dang, Ruizhi Shao, Hongwen Zhang, Wei Min, Yebin Liu, and Qingyao Wu. SViMo: Synchronized diffusion for video and motion generation in hand-object interaction scenarios. In _NeurIPS_ , 2025. 3 

- Christian Diller and Angela Dai. Cg-hoi: Contact-guided 3d human-object interaction generation. In _Proc. Computer Vision and Pattern Recognition (CVPR), IEEE_ , 2024. 3 

- Sai Kumar Dwivedi, Dimitrije Antić, Shashank Tripathi, Omid Taheri, Cordelia Schmid, Michael J Black, and Dimitrios Tzionas. Interactvlm: 3d interaction reasoning from 2d foundational models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 22605–22615, 2025. 3 

- Zicong Fan, Omid Taheri, Dimitrios Tzionas, Muhammed Kocabas, Manuel Kaufmann, Michael J. Black, and Otmar Hilliges. ARCTIC: A dataset for dexterous bimanual hand-object manipulation. In _CVPR_ , 2023. 3 

- Zipeng Fu, Qingqing Zhao, Qi Wu, Gordon Wetzstein, and Chelsea Finn. HumanPlus: Humanoid shadowing and imitation from humans. In _Conference on Robot Learning (CoRL)_ , 2024. 3 

- Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. OmniH2O: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. In _Conference on Robot Learning (CoRL)_ , 2024. 3 

- Tairan He, Zi Wang, Haoru Xue, Qingwei Ben, Zhengyi Luo, Wenli Xiao, Ye Yuan, Xingye Da, Fernando Castañeda, Shankar Sastry, et al. Viral: Visual sim-to-real at scale for humanoid loco-manipulation. _arXiv preprint arXiv:2511.15200_ , 2025a. 3, 8 

- Tairan He, Wenli Xiao, Toru Lin, Zhengyi Luo, Zhenjia Xu, Zhenyu Jiang, Jan Kautz, Changliu Liu, Guanya Shi, Xiaolong Wang, Linxi Fan, and Yuke Zhu. HOVER: Versatile neural whole-body controller for humanoid robots. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2025b. 3 

- Xialin He, Sirui Xu, Xinyao Li, Runpei Dong, Liuyu Bian, Yu-Xiong Wang, and Liang-Yan Gui. Ultra: Unified multimodal control for autonomous humanoid whole-body loco-manipulation. _arXiv preprint arXiv:2603.03279_ , 2026. 3 

13 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 

- Zhi Hou, Baosheng Yu, and Dacheng Tao. Compositional 3d human-object neural animation. _arXiv preprint arXiv:2304.14070_ , 2023. 2, 3 

- Yinghao Huang, Omid Taheri, Michael J. Black, and Dimitrios Tzionas. InterCap: Joint markerless 3D tracking of humans and objects in interaction. In _GCPR_ , 2022. 3 

- Haoran Jiang, Jin Chen, Qingwen Bu, Li Chen, Modi Shi, Yanjie Zhang, Delong Li, Chuanzhe Suo, Chuang Wang, Zhihui Peng, and Hongyang Li. WholeBodyVLA: Towards unified latent VLA for whole-body locomanipulation control. In _ICLR_ , 2026. 3 

- Nan Jiang, Tengyu Liu, Zhexuan Cao, Jieming Cui, Zhiyuan Zhang, Yixin Chen, He Wang, Yixin Zhu, and Siyuan Huang. Full-body articulated human-object interaction. In _ICCV_ , 2023. 3 

- Nan Jiang, Zhiyuan Zhang, Hongjie Li, Xiaoxuan Ma, Zan Wang, Yixin Chen, Tengyu Liu, Yixin Zhu, and Siyuan Huang. Scaling up dynamic human-scene interaction modeling. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 1737–1747, 2024. 3 

- Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. DROID: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 2, 3 

- Hyeonwoo Kim, Sookwan Han, Patrick Kwon, and Hanbyul Joo. Beyond the contact: Discovering comprehensive affordance for 3D objects from pre-trained 2D diffusion models. In _European Conference on Computer Vision_ , pages 400–419. Springer, 2024. 10, 11 

- Hyeonwoo Kim, Sangwon Baik, and Hanbyul Joo. David: Modeling dynamic affordance of 3d objects using pre-trained video diffusion models. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 10330–10341, 2025a. 3, 10, 22, 23 

- Jeonghwan Kim, Jisoo Kim, Jeonghyeon Na, and Hanbyul Joo. ParaHome: Parameterizing everyday home activities towards 3d generative modeling of human-object interactions. In _CVPR_ , 2025b. 3 

- Taeksoo Kim, Shunsuke Saito, and Hanbyul Joo. NCHO: Unsupervised learning for neural 3d composition of humans and objects. In _ICCV_ , 2023. 2, 3 

- Kuaishou. Kling ai video generator (image-to-video model), 2025. URL `https://klingai.com/` . Version 2.1, image-to-video generative model. 4, 19 

- Nilesh Kulkarni, Davis Rempe, Kyle Genova, Abhijit Kundu, Justin Johnson, David Fouhey, and Leonidas Guibas. Nifty: Neural object interaction fields for guided human motion synthesis. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 947–957, June 2024. 3 

- Black Forest Labs, Stephen Batifol, Andreas Blattmann, Frederic Boesel, Saksham Consul, Cyril Diagne, Tim Dockhorn, Jack English, Zion English, Patrick Esser, Sumith Kulal, Kyle Lacey, Yam Levi, Cheng Li, Dominik Lorenz, Jonas Müller, Dustin Podell, Robin Rombach, Harry Saini, Axel Sauer, and Luke Smith. Flux.1 kontext: Flow matching for in-context image generation and editing in latent space, 2025. URL `https://arxiv.org/abs/2506.15742` . 22 

- Hongjie Li, Hong-Xing Yu, Jiaman Li, and Jiajun Wu. Zerohsi: Zero-shot 4d human-scene interaction by video generation. In _3DV_ , 2026. 3 

- Jiaman Li, Jiajun Wu, and C Karen Liu. Object motion guided human motion synthesis. _ACM Transactions on Graphics (TOG)_ , 42(6):1–11, 2023a. 3, 11 

- Jiaman Li, Alexander Clegg, Roozbeh Mottaghi, Jiajun Wu, Xavier Puig, and C. Karen Liu. Controllable human-object interaction synthesis. In _ECCV_ , 2024. 3, 10, 22, 23 

14 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 

- Jiefeng Li, Jinkun Cao, Haotian Zhang, Davis Rempe, Jan Kautz, Umar Iqbal, and Ye Yuan. GENMO: A GENeralist model for human MOtion. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2025. 5, 6 

- Lei Li and Angela Dai. Genzi: Zero-shot 3d human-scene interaction generation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 20465–20474, 2024. 3 

- Quanzhou Li, Jingbo Wang, Chen Change Loy, and Bo Dai. Task-oriented human-object interactions generation with implicit neural representations. _arXiv preprint arXiv:2303.13129_ , 2023b. 3 

- Yuke Lou, Yiming Wang, Zhen Wu, Rui Zhao, Wenjia Wang, Mingyi Shi, and Taku Komura. Zero-shot humanobject interaction synthesis with multimodal priors. _arXiv preprint arXiv:2503.20118_ , 2025. 3 

- Jiaxin Lu, Chun-Hao Paul Huang, Uttaran Bhattacharya, Qixing Huang, and Yi Zhou. Humoto: A 4d dataset of mocap human object interactions. _arXiv preprint arXiv:2504.10414_ , 2025. 2, 3 

- Zhengyi Luo, Jinkun Cao, Alexander Winkler, Kris Kitani, and Weipeng Xu. Perpetual humanoid control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 10895–10904, 2023. 3 

- Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Castañeda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, et al. SONIC: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 2, 3, 6, 8, 19 

- Miles Macklin, Matthias Müller, and Nuttapong Chentanez. Xpbd: position-based simulation of compliant constrained dynamics. In _Proceedings of the 9th International Conference on Motion in Games_ , pages 49–54, 2016. 4 

- Jiageng Mao, Siheng Zhao, Siqi Song, Tianheng Shi, Junjie Ye, Mingtong Zhang, Haoran Geng, Jitendra Malik, Vitor Guizilini, and Yue Wang. Learning from massive human videos for universal humanoid pose control, 2024. URL `https://arxiv.org/abs/2412.14172` . 3 

- Ruiqian Nai, Boyuan Zheng, Junming Zhao, Haodong Zhu, Sicong Dai, Zunhao Chen, Yihang Hu, Yingdong Hu, Tong Zhang, Chuan Wen, and Yang Gao. HuMI: Humanoid whole-body manipulation from robot-free demonstrations, 2026. URL `https://arxiv.org/abs/2602.06643` . 3 

- Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang, Adeet Parikh, Aaron Lo, Abhishek Joshi, Ajay Mandlekar, and Yuke Zhu. Robocasa: Large-scale simulation of everyday tasks for generalist robots. _arXiv preprint arXiv:2406.02523_ , 2024. 11 

- OpenAI. Chatgpt. `https://chat.openai.com/` , 2024. Large language model used for text generation and editing. 4, 6, 10, 19 

- Shivansh Patel, Shraddhaa Mohan, Hanlin Mai, Unnat Jain, Svetlana Lazebnik, and Yunzhu Li. Robotic manipulation by imitating generated videos without physical demonstrations, 2025. URL `https://arxiv. org/abs/2507.00990` . 3 

- Georgios Pavlakos, Vasileios Choutas, Nima Ghorbani, Timo Bolkart, Ahmed AA Osman, Dimitrios Tzionas, and Michael J Black. Expressive body capture: 3D hands, face, and body from a single image. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 10975–10985, 2019. 5 

- Xiaogang Peng, Yiming Xie, Zizhao Wu, Varun Jampani, Deqing Sun, and Huaizu Jiang. Hoi-diff: Text-driven synthesis of 3d human-object interactions using diffusion models. In _CVPR 2025 Workshop of HuMoGen_ , 2025. 3, 10, 22, 23 

15 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 

- Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 3 

- Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ , 40(4):1–20, 2021. 3 

- Ilya A Petrov, Riccardo Marin, Julian Chibane, and Gerard Pons-Moll. Object pop-up: Can we infer 3d objects and their poses from human interactions alone? In _CVPR_ , 2023. 2, 3 

- Rolandos Alexandros Potamias, Jinglei Zhang, Jiankang Deng, and Stefanos Zafeiriou. Wilor: End-to-end 3d hand localization and reconstruction in-the-wild. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 12242–12254, 2025. 5 

- Sergey Prokudin, Christoph Lassner, and Javier Romero. Efficient learning on point clouds with basis point sets. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 4332–4341, 2019. 7 

- Alexander Raistrick, Lahav Lipson, Zeyu Ma, Lingjie Mei, Mingzhe Wang, Yiming Zuo, Karhan Kayan, Hongyu Wen, Beining Han, Yihan Wang, et al. Infinite photorealistic worlds using procedural generation. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 12630–12641, 2023. 4, 19 

- Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman Rädle, Chloe Rolland, Laura Gustafson, et al. Sam 2: Segment anything in images and videos. _arXiv preprint arXiv:2408.00714_ , 2024. 5, 19 

- Javier Romero, Dimitrios Tzionas, and Michael J Black. Embodied hands: modeling and capturing hands and bodies together. _ACM Transactions on Graphics (TOG)_ , 36(6):1–17, 2017. 5 

- Abraham Savitzky and Marcel JE Golay. Smoothing and differentiation of data by simplified least squares procedures. _Analytical chemistry_ , 36(8):1627–1639, 1964. 5 

- John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 8, 20 

- Modi Shi, Shijia Peng, Jin Chen, Haoran Jiang, Yinghui Li, Di Huang, Ping Luo, Hongyang Li, and Li Chen. Egohumanoid: Unlocking in-the-wild loco-manipulation with robot-free egocentric demonstration, 2026. URL `https://arxiv.org/abs/2602.10106` . 3 

- Omid Taheri, Nima Ghorbani, Michael J Black, and Dimitrios Tzionas. Grab: A dataset of whole-body human grasping of objects. In _European conference on computer vision_ , pages 581–600. Springer, 2020. 2, 3 

- Tencent Hunyuan3D Team. Hunyuan3d 2.1: From images to high-fidelity 3d assets with production-ready pbr material, 2025. 11 

- Ruicheng Wang, Sicheng Xu, Yue Dong, Yu Deng, Jianfeng Xiang, Zelong Lv, Guangzhong Sun, Xin Tong, and Jiaolong Yang. Moge-2: Accurate monocular geometry with metric scale and sharp details. _arXiv preprint arXiv:2507.02546_ , 2025. 5, 19 

- Xi Wang, Gen Li, Yen-Ling Kuo, Muhammed Kocabas, Emre Aksan, and Otmar Hilliges. Reconstructing action-conditioned human-object interactions using commonsense knowledge priors. In _3DV_ , 2022. 2, 3 

- Yinhuai Wang, Qihan Zhao, Yuen Fui Lau, Runyi Yu, Hok Wai Tsui, Qifeng Chen, Jingbo Wang, Jiangmiao Pang, and Ping Tan. HumanX: Toward agile and generalizable humanoid interaction skills from human videos, 2026. URL `https://arxiv.org/abs/2602.02473` . 3 

16 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 

- Bowen Wen, Wei Yang, Jan Kautz, and Stan Birchfield. Foundationpose: Unified 6d pose estimation and tracking of novel objects. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 17868–17879, 2024. 5 

- Haoyang Weng, Yitang Li, Nikhil Sobanbabu, Zihan Wang, Zhengyi Luo, Tairan He, Deva Ramanan, and Guanya Shi. HDMI: Learning interactive humanoid whole-body control from human videos, 2025. URL `https://arxiv.org/abs/2509.16757` . 3, 10, 11 

- Zhen Wu, Jiaman Li, Pei Xu, and C Karen Liu. Human-object interaction from human-level instructions. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 11176–11186, 2025. 3 

- Xianghui Xie, Bharat Lal Bhatnagar, and Gerard Pons-Moll. Chore: Contact, human and object reconstruction from a single rgb image. In _ECCV_ , 2022. 2, 3 

- Xianghui Xie, Bowen Wen, Yan Chang, Hesam Rabeti, Jiefeng Li, Ye Yuan, Gerard Pons-Moll, and Stan Birchfield. CARI4D: Category agnostic 4D reconstruction of human-object interaction. In _CVPR_ , 2026. 2, 3 

- Sirui Xu, Zhengyuan Li, Yu-Xiong Wang, and Liang-Yan Gui. Interdiff: Generating 3d human-object interactions with physics-informed diffusion. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 14928–14940, October 2023. 3 

- Sirui Xu, Ziyin Wang, Yu-Xiong Wang, and Liang-Yan Gui. Interdreamer: Zero-shot text to 3d dynamic human-object interaction. In _NeurIPS_ , 2024. 3 

- Sirui Xu, Hung Yu Ling, Yu-Xiong Wang, and Liang-Yan Gui. Intermimic: Towards universal whole-body control for physics-based human-object interactions. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 12266–12277, 2025. 10 

- Yufei Xu, Jing Zhang, Qiming Zhang, and Dacheng Tao. Vitpose: Simple vision transformer baselines for human pose estimation. _Advances in neural information processing systems_ , 35:38571–38584, 2022. 5 

- Pei Yang, Hai Ci, Yiren Song, and Mike Zheng Shou. X-Humanoid: Robotize human videos to generate humanoid videos at scale, 2025. URL `https://arxiv.org/abs/2512.04537` . 3 

- Yufei Ye, Xueting Li, Abhinav Gupta, Shalini De Mello, Stan Birchfield, Jiaming Song, Shubham Tulsiani, and Sifei Liu. Affordance diffusion: Synthesizing hand-object interactions. In _CVPR_ , 2023. 3 

- Shaofeng Yin, Yanjie Ze, Hong-Xing Yu, C. Karen Liu, and Jiajun Wu. VisualMimic: Visual humanoid locomanipulation via motion tracking and generation, 2025. URL `https://arxiv.org/abs/2509.20322` . 3 

- Justin Yu, Letian Fu, Huang Huang, Karim El-Refai, Rares Andrei Ambrus, Richard Cheng, Muhammad Zubair Irshad, and Ken Goldberg. Real2render2real: Scaling robot data without dynamics simulation or robot hardware. In _Conference on Robot Learning (CoRL)_ , 2025. 3 

- Yanjie Ze, Zixuan Chen, Joao Pedro Araújo, Zi-ang Cao, Xue Bin Peng, Jiajun Wu, and C. Karen Liu. TWIST: Teleoperated whole-body imitation system. In _Conference on Robot Learning (CoRL)_ , 2025a. 2, 3 

- Yanjie Ze, Siheng Zhao, Weizhuo Wang, Angjoo Kanazawa, Rocky Duan, Pieter Abbeel, Guanya Shi, Jiajun Wu, and C. Karen Liu. TWIST2: Scalable, portable, and holistic humanoid data collection system. _arXiv preprint arXiv:2511.02832_ , 2025b. 2, 3 

- Hui Zhang, Sammy Christen, Zicong Fan, Luocheng Zheng, Jemin Hwangbo, Jie Song, and Otmar Hilliges. ArtiGrasp: Physically plausible synthesis of bi-manual dexterous grasping and articulation. _arXiv preprint arXiv:2309.03891_ , 2023a. 3 

17 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 

- Jason Y. Zhang, Sam Pepose, Hanbyul Joo, Deva Ramanan, Jitendra Malik, and Angjoo Kanazawa. Perceiving 3d human-object spatial arrangements from a single image in the wild. In _European Conference on Computer Vision (ECCV)_ , 2020. 2, 3 

- Jinlu Zhang, Yixin Chen, Zan Wang, Jie Yang, Yizhou Wang, and Siyuan Huang. Interactanything: Zero-shot human object interaction synthesis via llm feedback and object affordance parsing. In _CVPR_ , 2025. 3 

- Juze Zhang, Haimin Luo, Hongdi Yang, Xinru Xu, Qianyang Wu, Ye Shi, Jingyi Yu, Lan Xu, and Jingya Wang. NeuralDome: A neural modeling pipeline on multi-view human-object interactions. In _CVPR_ , 2023b. 3 

- Chengfeng Zhao, Juze Zhang, Jiashen Du, Ziwei Shan, Junye Wang, Jingyi Yu, Jingya Wang, and Lan Xu. I’M HOI: Inertia-aware monocular capture of 3d human-object interactions. In _CVPR_ , 2024. 3 

- Siheng Zhao, Yanjie Ze, Yue Wang, C. Karen Liu, Pieter Abbeel, Guanya Shi, and Rocky Duan. ResMimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning, 2025. URL `https://arxiv.org/abs/2510.05070` . 3, 10, 11 

- Juntian Zheng, Qingyuan Zheng, Lixing Fang, Yun Liu, and Li Yi. CAMS: Canonicalized manipulation spaces for category-level functional hand-object manipulation synthesis. In _CVPR_ , 2023. 3 

- Keyang Zhou, Bharat Lal Bhatnagar, Jan Eric Lenssen, and Gerard Pons-Moll. TOCH: Spatio-temporal objectto-hand correspondence for motion refinement. In _ECCV_ , 2022. 3 

- Yi Zhou, Connelly Barnes, Jingwan Lu, Jimei Yang, and Hao Li. On the continuity of rotation representations in neural networks. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 5745–5753, 2019. 5 

18 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 

## **A. Human-Object Interaction Generation Details** 

### **A.1. Video Generation** 

We construct two candidate scene configurations using Infinigen (Raistrick et al., 2023): an indoor floor-only environment and a furnished room with a table (Fig. 6). For each input object, a VLM (OpenAI, 2024) determines whether it should be placed on the floor ( _e.g_ ., a sofa) or on the table ( _e.g_ ., a frypan) based on its typical affordances. We pair the object with a human asset prefitted to the Unitree G1’s morphology, render the initial frame, and use a VLM (OpenAI, 2024) to generate a text prompt describing the intended interaction. The rendered frame and prompt are then passed to Kling 2.5 Turbo Pro (Kuaishou, 2025), which supports generating 5 or 10 second videos at 24 fps with resolution of 1920ˆ1080. We can optionally render an ending frame to control the final positions of the human and object, and produce longer sequences auto-regressively by feeding the last frame of each segment as the initial frame of the next. 

### **A.2. Generation Runtime** 

Table 4 reports the wall-clock time for each stage of the 4D HOI generation pipeline per sequence (a 5-second video at 24 fps, 121 frames), measured on a single NVIDIA A100 GPU. The full pipeline takes approximately 14 minutes per sequence. Video generation and initial motion estimation (human and object) together account for about 4 minutes. The optimization preprocessing stage, which runs MoGe2 (Wang et al., 2025) for metric depth estimation and SAM2 (Ravi et al., 2024) for human and object segmentation to produce per-frame point clouds as optimization targets, takes roughly 2 minutes. The joint optimization stage dominates at approximately 8 minutes, as it jointly optimizes human and object trajectories across all frames. 

|**Stage**|**Time**|
|---|---|
|Video Generation (Kling API)|„1 min|
|Human Motion Estimation|„2 min|
|Object Pose Tracking|„1 min|
|Optimization Preprocessing|„2 min|
|Joint Optimization|„8 min|
|**Total**|„14 min|


Table 4: **Runtime Breakdown.** Wall-clock time per stage of the GRAIL 4D HOI generation pipeline, measured on a single NVIDIA A100 GPU for a 5- second, 121-frame sequence. 

### **A.3. Failure Case Filtering** 

While image-to-video models produce realistic HOI sequences, they may introduce artifacts such as texture inconsistencies or geometry mismatches across frames, causing FoundationPose to lose tracking. To automatically filter such failures, we compare SAM2 (Ravi et al., 2024) object masks t _ℳ_<sup>x</sup> _𝑡_ u<sup>_𝑇_</sup> _𝑡_ “1<sup>against rendered silhouettes</sup> t _ℳ𝑡_ u<sup>_𝑇_</sup> _𝑡_ “1<sup>from the predicted poses, and compute the mask tracking error:</sup> 


where Sump¨q counts non-zero pixels. This measures the fraction of SAM2-tracked mask pixels not covered by the predicted mask. We discard sequences where _𝑒_<sup>_ℳ_</sup> exceeds _𝜏_ “ 0 _._ 2, effectively removing cases caused by fast motion, blurry frames, or inconsistent object appearance. 

## **B. Task-General Loco-Manipulation Tracking Details** 

We train two physics-based tracking policies on top of SONIC (Luo et al., 2025), a pretrained whole-body controller: an _object-aware adaptor_ for manipulation 4D HOI trajectories and a _scene-aware tracker_ for terrainand chair-conditioned 4D HOI trajectories. Per-tracker policy observations are summarized in Table 5 and reward terms in Table 6. 

19 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 


Figure 6: **Candidate Scene Configurations.** Two pre-built 3D scene templates used to place objects: an indoor floor-only environment for ground-level objects ( _e.g_ ., a sofa), and a furnished room with a table for tabletop objects ( _e.g_ ., a frypan). A VLM selects between the two based on each object’s typical affordances. 

### **B.1. Object-Aware Adaptor** 

**Architecture.** The adaptor policy _𝜋𝜑_ is a 3-layer MLP with hidden dimensions r512 _,_ 256 _,_ 128s and SiLU activations. It outputs a 66-dim meta-action: 64 dims for the latent residual (matching the controller’s token dim of 2 ˆ 32) and 2 dims for left/right hand primitives. The residual is scaled by _𝜆_ “ 0 _._ 1 and added to the controller’s encoder output _before_ finite scalar quantization, then decoded to 29 body joint position targets. Each hand primitive is passed through a sigmoid and thresholded to a binary open/close signal, mapped to 7 finger joint positions per hand via predefined grasp configurations. The critic is a separate 3-layer MLP r512 _,_ 256 _,_ 128s that receives privileged observations including full body state and ground-truth contact flags. 

**Training.** We train _𝜋𝜑_ with PPO (Schulman et al., 2017) on 64 NVIDIA L40 GPUs with 1,024 parallel environments per GPU in Isaac Lab for 30,000 iterations; the pretrained encoder, FSQ quantizer, and decoder remain frozen and only _𝜋𝜑_ is updated. Environments sample reference motions from a shared task-family 4D HOI pool, and we apply reference state initialization at every episode reset: the start frame is sampled uniformly from the first 30 frames and clipped to precede the labeled hand-object contact. PPO hyperparameters: actor learning rate 2 ˆ 10<sup>´5</sup> with an adaptive schedule targeting KL “ 0 _._ 01, critic learning rate 10<sup>´3</sup> , discount factor _𝛾_ “ 0 _._ 99, GAE parameter _𝜆_ GAE “ 0 _._ 95, clipping parameter _𝜖_ “ 0 _._ 2, entropy coefficient 0 _._ 01, 24 steps per environment, 5 learning epochs with 4 mini-batches, and maximum gradient norm 0 _._ 1. Episodes terminate when the object’s _𝑧_ -position deviates by more than 0 _._ 4 m from the reference, the root height deviates by more than 0 _._ 25 m, or the root orientation error exceeds 1 _._ 0 rad. 

### **B.2. Scene-Aware Tracker** 

For scene-level interactions such as stepping over curbs, traversing slopes and stairs, or sitting on chairs, the controller’s flat-ground prior is not directly applicable. Instead of attaching a latent adaptor, we fine-tune the controller end-to-end together with a height-map encoder _𝜖ℎ_ and an auxiliary kinematic decoder _𝒢_ rec on the reconstructed scene-aware data. 

**Architecture.** We construct an 11 ˆ 11 height map grid centered on the robot with a total extent of 1 _._ 5 m and a resolution of 0 _._ 15 m. At each grid point, a downward ray is cast against the scene mesh to obtain the terrain hit position; positions are then transformed into the robot’s yaw-aligned local frame, yielding a p11 _,_ 11 _,_ 3q tensor. The height map is processed by a 3-layer CNN with channels r64 _,_ 128 _,_ 256s, kernel size 3ˆ3, stride 2, and LeakyReLU activations; spatial dimensions reduce as 11 Ñ 6 Ñ 3 Ñ 2, and the output is flattened to a 1,024-dim feature vector. This vector is concatenated with the proprioceptive observation and the controller’s tokenizer features, then passed through a fusion MLP (r256s, SiLU) that produces the latent input to the controller’s motion decoder. 

**Training.** We train with PPO (Schulman et al., 2017) on 64 NVIDIA L40 GPUs with 1,024 parallel environments per GPU in Isaac Lab for 30,000 iterations. Unlike object-aware tracking, we fine-tune the controller (encoder, FSQ quantizer, and action decoder _𝒢_ ) end-to-end together with the height-map encoder _𝜖ℎ_ and the parallel kinematic decoder _𝒢_ rec. _𝒢_ rec reconstructs the input motion targets to provide an auxiliary MSE loss (weight 0 _._ 01) that regularizes the latent to remain faithful to the reference. Reference state initialization is sampled 

20 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 

|**Term**|**Description**|**Dim**|**Used**|
|---|---|---|---|
|**Proprioception**||||
|Joint position|robot joint angles|43 / 29|Both|
|Joint velocity|robot joint angular velocities|43 / 29|Both|
|Base angular velocity|in body frame|3|Both|
|Previous action|last meta-action|66 / 29|Both|
|Base linear velocity|in body frame|3|O|
|Gravity direction|in body frame|3|S|
|**Reference motion targets**||||
|Motion anchor position|target root position in body frame|3|O|
|Motion anchor orientation|target root orientation 6D|6|O|
|Current command|ref. joint position + velocity, current frame|58|O|
|Multi-future command|ref. joint position + velocity, 10 future frames|580|O|
|Multi-future anchor ori|10 future root orientations 6D|60|O|
|**Object state**||||
|Object position|current object pos in body frame|3|Both|
|Object orientation 6D|current object ori in body frame|6|Both|
|Object pos delta (10 fut.)|reffut´simcur, position|30|Both|
|Object ori delta (10 fut.)|relative rotation, 6D|60|Both|
|Target object position|reference object pos in base frame|3|O|
|Object BPS encoding|per-object shape descriptor|10|O|
|Table position|in body frame|3|O|
|Table orientation 6D|in body frame|6|O|
|**Hand-object contact**||||
|Hand-to-object transform|per right hand (3 pos + 6 ori)|9|O|
|<br>Fingertip contact forces|<br>3D force per fingertip|12|O|
|**Scene**||||
|Local height map|11ˆ11terrain_𝑧_in body frame|121|S|


Table 5: **Policy Observations.** Observations for the object-aware adaptor (O) and the scene-aware tracker (S), grouped by category. When two dims are listed ( _e.g_ ., 43 / 29), the first applies to the object-aware policy (43-DoF G1 including fingers) and the second to the scene-aware policy (29-DoF G1, no fingers). Proprioceptive and previous-action observations are stored as 10-frame histories; instantaneous values are listed above. 

uniformly across the full motion at every episode reset. Since hand-object interaction is not involved in these tasks, manipulation-specific reward terms (grasp and object-pose tracking) are disabled. Episodes terminate under cumulative tracking-error thresholds with adaptive strict orientation and foot _𝑥𝑦𝑧_ constraints. 

### **B.3. Training Cost** 

Because each tracking policy is trained jointly over a shared task-family pool rather than fit per sequence, we report the amortized training cost per motion, defined as the total training wall-clock of a run divided by the number of motions in its pool. A full policy is trained for 30 _,_ 000 PPO iterations on 64 NVIDIA L40 GPUs with 1 _,_ 024 environments per GPU, which takes roughly 30 hours, and each run trains 2 _,_ 000–4 _,_ 000 motions jointly. The amortized cost is therefore only about 0 _._ 5–0 _._ 9 minutes per motion, far below the per-sequence cost of fitting a controller to each trajectory in isolation. As the pool grows with additional in-family motions, we do not retrain from scratch: we warm-start from the current policy and fine-tune, which typically converges within 6 _,_ 000 iterations (about one fifth of a full run, „6 hours), reducing the amortized cost of incorporating new motions to roughly one fifth of the full-training figure. 

21 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 

|**Term**|**Formula**|**Weight**|**Used**|
|---|---|---|---|
|**Motion tracking reward**||||
|Anchor position|exp<br>`<br>´}r**_𝑝_**<sup>root</sup><br>_𝑡_<br>´**_𝑝_**<sup>root</sup><br>_𝑡_<br>}<sup>2</sup>{_𝜎_<sup>2˘</sup>|0_._5|Both|
|Anchor orientation|exp<br>`<br>´}r**_𝑟_**<sup>root</sup><br>_𝑡_<br>a**_𝑟_**<sup>root</sup><br>_𝑡_<br>}<sup>2</sup>{_𝜎_<sup>2˘</sup>|2_._5|Both|
|Relative body position|exp<br>`<br>´ <sup>1</sup><br>_𝑁_<br>ř<br>_𝑖_<sup>}r</sup><sup>**_𝑝_**</sup><sup>_𝑖,𝑡_´</sup><sup>**_𝑝_**</sup><sup>_𝑖,𝑡_}2{</sup><sup>_𝜎_2˘</sup>|1_._0|Both|
|Relative body orientation|exp<br>`<br>´ <sup>1</sup><br>_𝑁_<br>ř<br>_𝑖_<sup>}r</sup><sup>**_𝑟_**</sup><sup>_𝑖,𝑡_a</sup><sup>**_𝑟_**</sup><sup>_𝑖,𝑡_}2{</sup><sup>_𝜎_2˘</sup>|5_._0|Both|
|Body linear velocity|exp<br>`<br>´ <sup>1</sup><br>_𝑁_<br>ř<br>_𝑖_<sup>}r</sup><sup>**_𝑣_**</sup><sup>_𝑖,𝑡_´</sup><sup>**_𝑣_**</sup><sup>_𝑖,𝑡_}2{</sup><sup>_𝜎_2˘</sup><br><br><br>|1_._0|Both|
|Body angular velocity|exp<br>`<br>´ <sup>1</sup><br>_𝑁_<br>ř<br>_𝑖_<sup>}r</sup><sup>**_𝜔_**</sup><sup>_𝑖,𝑡_´</sup><sup>**_𝜔_**</sup><sup>_𝑖,𝑡_}2{</sup><sup>_𝜎_2˘</sup><br><br>|1_._0|Both|
|5-point local body|exp<br>`<br>´<br>1<br>|_𝒮_5|<br>ř<br>_𝑖_P_𝒮_5 <sup>}r</sup><sup>**_𝑝_**loc</sup><br>_𝑖,𝑡_<sup>´</sup><sup>**_𝑝_**loc</sup><br>_𝑖,𝑡_<sup>}2{</sup><sup>_𝜎_2˘</sup>|2_._0|S|
|**Object reward**||||
|Object pose tracking|_𝑤𝑝_exp<br>`<br>´_𝛼𝑝_}r**_𝑝_**<sup>_𝒪_</sup><br>_𝑡_<sup>´</sup><sup>**_𝑝_**</sup><sup>_𝒪_</sup><br>_𝑡_<sup>}</sup><br>˘<br>`_𝑤𝑟_exp<br>`<br>´_𝛼𝑟_}r**_𝑟_**<sup>_𝒪_</sup><br>_𝑡_<sup>a</sup><sup>**_𝑟_**</sup><sup>_𝒪_</sup><br>_𝑡_<sup>}</sup><br>˘|20_._0|O|
|**Grasp reward**||||
|Grasp contact count|min<br>`<br>_𝑁_<sup>contact</sup><br>_𝑡_<br>{_𝑁_min_,_ 1<br>˘|40_._0|O|
|Grasp finger direction|´cosp**_𝑑_**<sup>thumb</sup><br>_𝑡_<br>_,_ **_𝑑_**<sup>index</sup><br>_𝑡_<br>q⊮t_𝐶𝑡_u|10_._0|O|
|Grasp contact center|exp<br>`<br>´_𝛾_<br>1<br>_𝑁𝑓_<br>ř<br>_𝑗_<sup>}</sup><sup>**_𝑓_**</sup><sup>_𝑗,𝑡_´</sup><sup>**_𝑐_**</sup><sup>_𝑡_}</sup><br>˘<br>⊮t_𝐶𝑡_u|0_._1|O|
|**Regularization**||||
|Latent residual_ℓ_2|}Δ**_𝑧_**_𝑡_}<sup>2</sup><br>|0_._1|O|
|Finger-primitive limit|⊮<br>“<br>|_𝑎_<sup>fp</sup><br>_𝑗,𝑡_<sup>| ą 0</sup><sup>_._5</sup><br>‰<br>|´10_._0|O|
|Action rate_ℓ_2|}**_𝑎_**_𝑡_´**_𝑎_**_𝑡_´1}<sup>2</sup><br>|´0_._1|S|
|Anti-shake angular velocity|1<br>|_ℬ_|<br>ř<br>_𝑖_P_ℬ_<br>“<br>maxp0_,_}**_𝜔_**_𝑖,𝑡_} ´_𝜏_q<br>‰2|´5ˆ10<sup>´3</sup>|S|
|Ankle joint acceleration|ř<br>_𝑗_P_𝒥_kl <sup>:</sup><sup>_𝑞_2</sup><br>_𝑗,𝑡_|´2_._5ˆ10<sup>´7</sup>|S|
|Kinematic reconstruction|ane <br>}r**_𝑞_**_𝑡_´_𝒢_recp**_𝑧_**_𝑡_q}<sup>2</sup>|0_._01|S|
|Joint limit|ř<br>_𝑗_<sup>max</sup><br>`<br>0_,_ |_𝑞𝑗,𝑡_| ´_𝑞_<sup>lim</sup><br>_𝑗_<br>˘|´10_._0|S|
|Undesired body contact|_𝑁_<sup>undesired</sup><br>_𝑡_|´0_._1|Both|


Table 6: **Reward Terms.** Rewards for the object-aware adaptor (O) and the scene-aware tracker (S), organized by the four categories from Sec. 3.3. The rightmost column indicates which tracker uses each term. For grasp terms, the listed weight is the right-hand value; in object-aware training, the left hand uses half the listed weight. ⊮t _𝐶𝑡_ u is the per-frame motion-label contact indicator that gates the grasp finger-direction and contact-center terms. The object pose-tracking reward is additionally gated by a simulated finger–object contact indicator, so it is active only while the hand is in contact with the object. For anti-shake, _ℬ_ “ tleft wrist, right wrist, headu with deadzone _𝜏_ “ 1 _._ 5 rad/s. Per-term Gaussian-kernel bandwidth _𝜎_ varies by term and is given in the released config. Negative weights indicate penalties. 

## **C. Experiment Details** 

### **C.1. Human-Object Interaction Generation** 

**Baselines.** We compare against training-based and training-free 4D HOI generation approaches. Training-based baselines include CHOIS (Li et al., 2024), a controllable motion generation framework guided by language and sparse waypoints, and HOIDiff (Peng et al., 2025), a diffusion-based model for affordance-conditioned HOI synthesis. For training-free comparison, we evaluate DAViD (Kim et al., 2025a), which generates the first frame using an image generative model (Labs et al., 2025) and produces the video from that frame. Since image generation often fails under partial control signals ( _e.g_ ., Canny edge maps), we generate 24 images per object and manually select a successful result as the starting frame. To ensure fairness, DAViD uses Kling’s image-to-video model under the same setting as our approach. 

**User Study.** Beyond the quantitative metrics reported in Sec. 4.1, we conduct a user study with 30 participants to assess perceptual quality. In each trial, participants view sequences from three of the four methods drawn at random and select the result with the most appropriate object affordances (Aff. Real.) and the most physically plausible motion (Phys. Real.). As shown in Table 7, GRAIL is preferred by a wide margin on both criteria. This perceptual study complements, but does not replace, the physics-based tracking and robot-execution metrics reported in Sec. 4.1 and Sec. 4.3. 

22 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 

|**Methods**|Aff. Real. Ò|Phys. Real. Ò|
|---|---|---|
|HOIDiff (Peng et al.,2025)|2.0%|1.9%|
|CHOIS (Li et al.,2024)|12.2%|16.8%|
|DAViD (Kim et al.,2025a)|11.2%|10.4%|
|Ours|**74.7%**|**70.9%**|


Table 7: **User Study.** 30-participant pick rates for the most appropriate object affordances (Aff. Real.) and the most physically plausible motion (Phys. Real.) on the shared 20-object evaluation set. Pick rates have a theoretical upper bound of 75% under 3-of-4 random sampling. 


Figure 7: **Qualitative Comparison.** Representative 4D HOI sequences from each method on the shared 20-object evaluation set. GRAIL produces more coherent motions with accurate contact and natural hand poses, while baseline methods often yield unrealistically flat or static hand configurations. 

|||**R**|**econstruc**|**tion Quality**||**T**|**racking Q**|**uality**|
|---|---|---|---|---|---|---|---|---|
|**Methods**|ContactÓ|Pen. Ó|MPJPEÓ|Human Smo. Ó|Obj Smo. Ó|SRÒ|ObjPosÓ|MPJPE-LÓ|
|w/o_𝐿_proj|0.016|1.93%|16.70|0.0023|0.0011|41.6%|0.374|47.1|
|w/o_𝐿_depth|0.017|1.97%|4.35|0.0020|0.0011|42.6%|0.372|49.3|
|w/o_𝐿_cont|0.024|1.52%|4.81|0.0022|0.0009|53.3%|0.332|52.4|
|Ours (Full)|0.015|1.81%|4.89|0.0020|0.0009|81.4%|0.135|41.8|


Table 8: **Ablation Study on Reconstruction Losses.** Reconstruction quality (Contact, Pen., MPJPE in pixel space, motion smoothness) and downstream tracking quality (SR, ObjPos, MPJPE-L) for each loss ablation. Each loss targets a different failure mode in reconstruction; the full model achieves the best downstream tracking despite not minimizing every reconstruction proxy in isolation. 

**Qualitative Comparison.** Fig. 7 shows that GRAIL produces more coherent motions with accurate contact and natural hand poses, while baseline methods often yield unrealistically flat or static hand configurations unsuitable for downstream humanoid skill learning. 

**Reconstruction Ablation.** We ablate the interaction-aware reconstruction losses ( _𝐿_ proj, _𝐿_ depth, _𝐿_ cont) on the 124-motion benchmark. As shown in Table 8, removing _𝐿_ proj degrades image-space consistency, while removing _𝐿_ depth or _𝐿_ cont weakens metric interaction quality. These reconstruction-level errors propagate to downstream tracking: each ablation substantially reduces tracking success rate and increases trajectory deviation, while the 

23 

GRAIL : Generating Humanoid Loco-Manipulation from World Models 

full model achieves the best overall downstream tracking quality. 

24 

