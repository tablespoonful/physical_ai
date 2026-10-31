---
title: "Genie Sim PanoWorld: An Infinite Indoor 3D World Generation Pipeline via Panoramic Scene Modeling and Simulation"
date: "2026-07-29"
authors: "Yongxin Su; Linjie Hou; Feng Wang; Jialin Tang; Zhijun Li; Qian Wang"
url: https://arxiv.org/abs/2607.26646
pdf: https://arxiv.org/pdf/2607.26646
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2607.26646)** / [論文ページ](https://arxiv.org/abs/2607.26646)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Genie Sim PanoWorld: An Infinite Indoor 3D World Generation Pipeline via Panoramic Scene Modeling and Simulation** 

Yongxin Su<sup>1</sup> Linjie Hou<sup>1</sup> 

Feng Wang<sup>1</sup> Jialin Tang<sup>1</sup> Zhijun Li<sup>2</sup> Qian Wang<sup>_†_</sup> 

Maoqing Yao<sup>_†_</sup> 

## **Abstract** 

_We address the problem of reconstructing a high-fidelity, freely navigable 3D scene from a single_ 360<sup>_◦_</sup> _panorama, without per-scene optimization or multi-view capture. Existing methods either lack metric trajectory control, which hinders reliable downstream 3D reconstruction, or struggle with large disocclusions under long-range camera motion while requiring high-end multi-GPU servers. We present_ **_Genie Sim PanoWorld_** _, a two-stage feed-forward pipeline that bridges generation and reconstruction via an explicit, trajectory-controllable panoramic video. A NavMesh-planned_ SE(3) _roaming trajectory is injected into a latent video diffusion model through dense geometrywarped conditioning; long–short trajectory mixed training and a self-consistency objective based on shortcut models together yield high-fidelity video in four CFG-free denoising steps. A feed-forward panoramic reconstructor then lifts the generated video into a high-fidelity 3D Gaussian scene that supports real-time, free-viewpoint roaming and can be directly used as a simulation-ready asset for embodied AI applications. Experiments show that_ **_Genie Sim PanoWorld_** _outperforms geometry-conditioned baselines in both panoramic video generation and downstream 3D reconstruction, while generalizing zero-shot to unseen indoor scenes._ 

## **1. Introduction** 

Creating immersive, explorable 3D indoor environments has long been a goal in vision and graphics, with applications in virtual tours, embodied AI, and content creation. The classical route to such a scene is per-scene reconstruction: given many calibrated views, whose poses are typically recovered by structure-from-motion, optimize a radiance field such as NeRF [25] or 3D Gaussian Splatting [13] to fit the captured views. These methods produce highquality free-viewpoint renderings, but they require many overlapping views of the scene and a lengthy per-scene optimization, and they only interpolate among the observed 

> †Corresponding author. 


Figure 1. We propose Genie Sim PanoWorld, which requires only an indoor panoramic image and can directly produce a metric-scale 3D point cloud, accurate poses, and feed-forward Gaussian results within seconds. It can also be provided directly to the downstream per-scene-optimized 3DGS to generate embodied intelligence that can use high-fidelity digital twin assets. 

#### regions rather than synthesizing unseen content. 

A single 360<sup>_◦_</sup> panorama is an appealing starting point that sidesteps the multi-view capture burden: it captures a whole room in one shot, is cheap to acquire, and is already the common medium for real-estate and VR-tour products. Yet a panorama is observed from one fixed viewpoint. It records the scene only as seen from that single location, so a user can look around freely but cannot move far because the input provides neither parallax cues nor observations of content hidden behind occluders. Such dense multi-view coverage is precisely what per-scene reconstruction relies 

1 

on. Turning such a single panorama into a freely roamable, full 6-DoF scene in a feed-forward manner, without any per-scene optimization, is the central challenge: the single view must be turned into consistent multi-view evidence and lifted into a renderable 3D model in one forward pass. 

Existing approaches fall short of this goal in different ways. One line of work generates panoramic imagery, videos, or multi-view observations through free-form or text-guided sampling rather than along a prescribed camera trajectory [36, 38]. Without explicit metric trajectory and geometric camera control, the generated views cannot be reliably reconstructed into a roamable 3D model. A second line couples camera-guided generation with explicit geometry [21, 37, 40], but tends to degrade under long indoor camera displacements, where the geometric warp becomes unreliable and disocclusions dominate [37], or discards the metric geometry needed to follow a collision-free path [21]. Many of these systems also build on large backbones with many-step, classifier-free-guided sampling, so they require high-end multi-GPU servers [9, 28] and are hard to deploy on commodity hardware. 

We present **Genie Sim PanoWorld** , a feed-forward pipeline that turns a single ERP panorama into a roamable 3D Gaussian scene. The pipeline bridges generation and reconstruction with an explicit, trajectory-controllable panoramic video. From the input panorama we recover a coarse scene mesh, plan a collision-free roaming trajectory on a navigation mesh, and synthesize a panoramic video that follows that path while inpainting newly disoccluded regions. The generated video provides dense multi-view observations of the scene; a feed-forward panoramic reconstructor then estimates per-frame camera poses and geometry, and a Gaussian-splatting decoder lifts them into a 3D Gaussian model for real-time free-viewpoint rendering. The two stages support each other: the trajectorycontrollable video supplies wide-baseline but geometrically consistent views that make single-panorama reconstruction tractable, while the metric trajectory keeps both stages in one coherent frame. Two components keep generation practical. A _long–short trajectory mixed training_ scheme couples high-fidelity short-range supervision with large-disocclusion long-range supervision, and a _selfconsistency objective based on shortcut models_ [5] eliminates the need for classifier-free guidance and reduces sampling to four steps. As a result, the full single-panorama-toscene pipeline runs without any test-time optimization on a single consumer GPU. 

Our contributions are as follows. 

- A feed-forward single-panorama-to-3D pipeline that couples trajectory-controllable panoramic video generation with Gaussian reconstruction, enabling free-viewpoint rendering without per-scene optimization. 

- A NavMesh-guided panoramic video generator with met- 

ric SE(3) trajectory control, long–short trajectory mixed training, and self-consistency training for shortcut models, achieving improved fidelity and trajectory accuracy while substantially reducing inference cost. 

- A feed-forward panoramic reconstructor with a voxelaligned Gaussian decoder that recovers metric poses, geometry, and renderable 3D Gaussian primitives from wide-baseline panoramic observations. 

- A large-scale indoor panoramic dataset providing dense multi-view trajectories, metric depth, full 6DoF poses, and editable high-fidelity 3D scene assets. 

## **2. Related Work** 

### **2.1. Panoramic Video Generation and Scene Exploration** 

Panoramic content generation has progressed from static panoramic imagery toward dynamic and explorable scenes. Early holistic multi-view image synthesis such as PanoFree [19] produces globally consistent panoramas without per-scene tuning. To bring motion to panoramas, a prominent line of work lifts pretrained perspective video diffusion models into the 360<sup>_◦_</sup> domain: PanoWan [36] introduces latitude/longitude-aware mechanisms to cope with equirectangular distortion and boundary continuity, ViewPoint [4] repurposes pretrained diffusion priors for panoramic video, and PanFlow [39] decouples motion control for panoramic generation. DynamicScaler [20] targets seamless, scalable panoramic scene video, while 4K4DGen [16] pushes panoramic 4D generation to 4K resolution and CubeComposer [15] autoregressively composes 4K 360<sup>_◦_</sup> video from perspective input. These methods produce panoramic imagery or video as the final output, with motion driven by free or text-guided sampling rather than a prescribed camera path. 

More recently, a cluster of panoramic world models pursues large-scale, consistent scene synthesis: concurrent PanoWorld variants address whole-house panorama synthesis [10], geometry-consistent panoramic video [12], and spatial supersensing [31], and PanoWorld-X [38] generates explorable panoramic worlds via sphere-aware video diffusion. A parallel line of work conditions video diffusion on explicit camera motion to enable viewpoint control and scene exploration. For perspective video, GenEx [22] generates an explorable world from imagery, and Voyager [8] produces long-range, world-consistent video for explorable 3D scene generation. A growing family couples cameraguided generation with geometry: Matrix-3D [37] warps a reconstructed scene mesh to condition omnidirectional, explorable 3D world generation, WorldStereo [40] bridges camera-guided video generation and scene reconstruction through 3D geometric memories, and large multi-modal world models such as HY-World 2.0 [9] jointly recon- 

2 

struct, generate, and simulate 3D worlds. In the panoramic regime, OmniRoam [21], an image-to-video model built on the Wan2.1-T2V-1.3B backbone, generates long-horizon panoramic video for world wandering, but encodes camera motion as a scalar speed signal rather than metric SE(3) poses, forfeiting the spatial grounding needed to plan and follow collision-free paths. Our panoramic video module instead injects a dense, metric geometry-warped conditioning signal derived from a NavMesh-planned SE(3) trajectory, so the generated sequence follows the requested collision-free path while inpainting large disocclusions, which we find essential for the downstream feed-forward 3D reconstruction. 

A second gap is resource cost. These systems rely on large backbones with many-step, classifier-free-guided sampling; methods such as WorldStereo [40], Lyra 2.0 [28], and HY-World 2.0 [9] target high-end multi-GPU servers and are hard to deploy on commodity hardware. We trade backbone scale for deployability: shortcut-model training enables guidance-free sampling in a few denoising steps, and the full single-panorama-to-scene pipeline runs feedforward on a single consumer-grade GPU. 

### **2.2. Feed-Forward 3D Reconstruction and Gaussian Splatting** 

Feed-forward 3D reconstruction has recently emerged as a promising paradigm for scalable scene reconstruction, aiming to directly infer 3D geometry and appearance from single or sparse views in a single forward pass, without per-scene optimization. Compared with optimization-based neural rendering methods such as NeRF and its variants, feed-forward approaches significantly reduce reconstruction time while improving deployment efficiency, making them particularly suitable for real-time and large-scale applications. 

#### **2.2.1. Depth Foundation Models for 3D Reconstruction** 

A key enabler of feed-forward reconstruction is the advancement of large-scale depth foundation models. Recent methods, such as Depth Anything V3 [17], demonstrate strong generalization ability across diverse scenes by leveraging large-scale heterogeneous training data and selfsupervised objectives. These models produce high-quality, dense depth maps that serve as robust geometric priors for downstream 3D reconstruction tasks. In modern pipelines, such depth priors are often integrated either as explicit supervision or as initialization for lifting 2D observations into 3D representations. 

#### **2.2.2. Feed-Forward Multi-View Reconstruction** 

Beyond monocular depth estimation, recent works focus on directly learning multi-view geometry in a feedforward manner. Transformer-based architectures such as VGGT [33] and its improved variant VGGT-Ω [34] jointly 

model camera pose estimation, multi-view correspondence, and dense reconstruction within a unified network. By leveraging global attention mechanisms, these methods are capable of reasoning about cross-view consistency without relying on traditional structure-from-motion pipelines. 

Compared with earlier sparse-view reconstruction methods, VGGT-style models significantly improve robustness under limited viewpoints and ambiguous geometry. However, they still face challenges in high-frequency detail preservation and photorealistic rendering quality. 

#### **2.2.3. Gaussian Splatting and Feed-Forward Radiance Representation** 

Recently, 3D Gaussian Splatting (3DGS) has emerged as an efficient alternative to implicit neural radiance fields, enabling high-quality real-time rendering through explicit Gaussian primitives. This representation has inspired a new line of feed-forward reconstruction methods that directly predict or initialize Gaussian parameters from images. 

To improve geometric fidelity and rendering sharpness, methods such as SHARP [23] introduce learning-based refinement mechanisms for Gaussian primitives, reducing over-smoothing artifacts and enhancing structural consistency. These approaches demonstrate that Gaussian representations are particularly well-suited for feed-forward pipelines due to their explicit nature and differentiability. 

#### **2.2.4. Generative Priors and Multi-View Consistency** 

In parallel, recent generative foundation models have begun to influence 3D reconstruction. For example, HunyuanMirror incorporates multi-view generative priors to enforce geometric and photometric consistency across views, improving structural coherence in reconstructed scenes. Such approaches highlight a growing trend of integrating diffusion-based or generative priors with explicit 3D representations, bridging the gap between 2D generative modeling and 3D scene understanding. 

#### **2.2.5. Discussion** 

Overall, feed-forward 3D reconstruction is rapidly evolving toward a unified paradigm that combines: 

- strong depth foundation models (e.g., Depth Anything V3), 

- multi-view transformer reasoning (e.g., VGGT / VGGTΩ), 

- and explicit Gaussian representations (e.g., 3DGS and SHARP [23]), 

while increasingly incorporating generative priors (e.g., Hunyuan-Mirror) to improve global consistency. 

Despite these advances, current methods still struggle with fine-grained geometry recovery, view-consistent texture synthesis, and robustness under extreme viewpoint sparsity, leaving significant room for future improvements. 

3 

## **3. Method** 

### **3.1. Problem Formulation** 

We address the task of recovering a freely roamable 3D scene from a single panoramic observation. The input is one equirectangular (ERP) panorama _I ∈_ R<sup>_H×W ×_3</sup> , and the desired output is a 3D Gaussian scene model 


where each primitive carries a position _µk ∈_ R<sup>3</sup> , orientation _qk_ , scale _sk_ , opacity _αk_ , and view-dependent color _ck_ , enabling rasterization-based real-time free-viewpoint rendering. A single panorama observes the scene from one vantage point and leaves the geometry and appearance behind occluders unconstrained, so directly regressing _G_ from _I_ is ill-posed. 

We therefore factorize the mapping _I →G_ into two feedforward stages bridged by an explicit multi-view representation. First, a trajectory-controllable panoramic video generator _F_ gen synthesizes a temporally coherent panoramic video that walks the scene along an automatically planned, collision-free roaming trajectory _T_ = _{Ti}_<sup>_N_</sup> _i_ =1<sup>with</sup><sup>_Ti∈_</sup> SE(3): 


turning the single-view input into a set of consistent virtual observations that reveal the initially occluded content. Second, a feed-forward panoramic reconstructor _F_ rec consumes the generated video to estimate per-frame camera poses _{T_<sup>ˆ</sup> _i}_<sup>_N_</sup> _i_ =1<sup>and a dense geometry, which a Gaussian-splatting</sup> decoder _F_ dec then converts into the final scene model: 


Both stages are feed-forward and require no per-scene optimization: the generation stage supplies the multi-view evidence that makes reconstruction well-posed, and the trajectory _T_ links the two, since it must be metrically faithful enough for the reconstructor to recover consistent poses and coverage. The remainder of this section details the trajectory-controllable panoramic video generator (Sec. 3.2) and the feed-forward 3D world reconstructor that produces _G_ . 

### **3.2. Trajectory-Controllable Panoramic Video Generation** 

Given a single ERP panorama _I ∈_ R<sup>_H×W ×_3</sup> , the goal of this stage is to synthesize a temporally coherent panoramic video _V_ = _{Vi}_<sup>_N_</sup> _i_ =1<sup>that follows an automatically planned,</sup> collision-free roaming trajectory _T_ = _{Ti}_<sup>_N_</sup> _i_ =1<sup>,</sup><sup>_Ti_</sup> _∈_ SE(3), and that remains photometrically consistent with _I_ . The trajectory is planned on a NavMesh derived from the input panorama’s depth, which keeps every camera pose 

within the navigable floor region and prevents wall penetration. In contrast, OmniRoam [21] conditions on a scalar speed signal and therefore does not preserve the metric spatial layout required for collision-aware path control. Our generator is a trajectory-conditioned latent video diffusion model built on the Wan2.2-TI2V-5B backbone [30], adapted with low-rank adapters [6]. Matrix-3D [37] relies only on geometric warps and degrades under long indoor camera displacements. Our generator keeps the geometry-warped conditioning but adds two changes: (i) it trains on a mixture of long- and short-range trajectories that couples highfidelity supervision with large-disocclusion inpainting, and (ii) it applies a self-consistency objective based on shortcut models to enable high-quality, few-step sampling without classifier-free guidance (CFG), so the model can run on a single consumer GPU. 

#### **3.2.1. NavMesh-Guided Trajectory Planning and Conditioning** 

We first recover the coarse 3D structure of the input scene. A panoramic depth map _D ∈_ R<sup>_H×W_</sup> is estimated with Depth Anything 360<sup>_◦_</sup> [11], back-projected into a dense point cloud, and triangulated into a scene mesh _M_ . We extract the traversable floor region from _M_ and build a NavMesh as the free-space prior for collision-free path planning. 

On the NavMesh we automatically generate a roaming trajectory _T_ = _{Ti}_<sup>_N_</sup> _i_ =1<sup>(</sup><sup>_N_=81frames)bycombin-</sup> ing _sector exploration paths_ , which cover the full 360° extent of the scene, and _ring paths_ , which form closed-loop tours that emphasise temporal consistency. All paths are reparameterized to a near-uniform step length and expressed in a canonical frame anchored at the first view. We then convert the planned trajectory into a dense conditioning signal: for each pose _Ti_ we render the scene mesh into ERP space to obtain a warped panorama _V_<sup>ˆ</sup> _i_ and a disocclusion mask _Mi_ , which are jointly encoded and injected into the DiT, turning the generator into a geometry-aware video inpainter. 

#### **3.2.2. Mixed Training and Self-Consistency Loss** 

**Long–short trajectory mixed training.** The geometrywarped condition degrades with camera displacement: long traversals produce large disocclusions that geometry-only conditioning cannot fill, while short-range warps are nearperfect but provide no inpainting supervision. We therefore train on a mixture of long- and short-range clips drawn from the same ground-truth tracks, with clip lengths sampled uniformly so that every traversal scale is equally represented. Short-range clips anchor appearance fidelity; longrange clips supervise large-disocclusion inpainting. 

**Shortcut-model training for CFG-free sampling.** The model is a flow-matching (rectified-flow) diffusion in latent 

4 


Figure 2. **Overview of Genie Sim PanoWorld.** _Stage 1 (Environment Perception & Trajectory Construction):_ A raw ERP panorama is processed by a depth estimator to build a dense point cloud and 3D mesh; a NavMesh is extracted from the traversable floor region and used to plan a collision-free SE(3) camera trajectory. _Stage 2 (Latent Video Diffusion):_ For each planned pose, a geometry-warped ERP frame and its disocclusion mask are encoded by a frozen 3D VAE and concatenated with the noisy latent along the channel axis. A Latent Rectified-Flow DiT (Wan2.2-TI2V-5B + LoRA) denoises the sequence in 4 CFG-free steps via shortcut-model sampling; the frozen VAE decoder produces the final _T_ -frame panoramic video. _Stage 3 (Feed-Forward 3D Reconstruction & Voxel-Based Gaussian Splatting):_ The generated panoramic frames are fed to PanoVGGT, a geometry transformer that jointly estimates camera poses, dense depth maps, and high-resolution image features. Observations are lifted into world coordinates, aggregated into occupied voxels via multi-view attention and KNN attention blocks, and decoded per voxel into 3D Gaussian primitives for real-time free-viewpoint rendering. 

space [18]. With noise level _σ_ = _t/Nt_ , the noisy latent is _xt_ = (1 _− σ_ ) _x_ 0 + _σ ϵ_ and the velocity target is _v_ = _ϵ − x_ 0. 

To reduce the number of inference steps, we adopt the self-consistency formulation of shortcut models [5], which additionally conditions the network on a step size ∆ _t_ : _sθ_ ( _xt, t,_ ∆ _t, y, c_ ). Rather than retraining the full 5B backbone, we apply LoRA fine-tuning with the self-consistency objective, which removes the need for a CFG unconditional branch entirely. Each iteration is routed with probability _ρ_ = 0 _._ 75 to the flow-matching loss 


and with probability 1 _−ρ_ to the self-consistency loss, where a frozen teacher takes two half-steps to produce a more accurate velocity estimate _v_ ¯ = <u>12</u><sup>(</sup><sup>_v_1+</sup><sup>_v_2)andthestudent</sup> must match it: 


At inference, 4 large Euler steps with _w_ = 1 (no CFG) 

suffice, substantially reducing NFE relative to the Matrix3D baseline. We evaluate Matrix-3D using 10 guided steps, a practical setting that balances generation quality and inference efficiency, instead of its full 50-step schedule. A lightweight RealESRGAN [35] _×_ 2 stage finally upscales the decoded frames. 

**Training objective.** The video generator is trained independently from the reconstruction stage: 


where _b ∼_ Bernoulli( _ρ_ ). Only the LoRA adapters, the conditioning projection, and the step-size embedding are updated; the Wan2.2 backbone and VAE remain frozen. 

### **3.3. Feed-Forward 3D World Reconstruction** 

#### **3.3.1. Feed-Forward Pose and Depth Estimation** 

We build upon recent feed-forward multi-view reconstruction frameworks, particularly VGGT, and extend them to 

5 

panoramic 3D world reconstruction. Unlike conventional perspective-based formulations, which rely on pinhole camera assumptions and explicit intrinsic parameter estimation, we reformulate the problem in an equirectangular projection (ERP) domain to enable holistic scene understanding from a single panoramic observation. 

A key motivation for adopting panoramic ERP representation is its superior spatial efficiency in indoor and confined environments. In narrow indoor scenes, a single panoramic observation can capture the entire surrounding geometry in a unified coordinate system, significantly reducing viewpoint fragmentation and improving global geometric completeness. Compared with multi-view perspective setups, ERP inherently encodes 360° contextual information, which provides stronger constraints for pose inference and reduces ambiguity caused by limited field-of-view observations. 

Specifically, instead of processing multiple perspective views with separate camera intrinsics, we directly operate on ERP images. This design eliminates the need for explicit camera intrinsic estimation, since ERP projection provides a fixed and consistent mapping from spherical directions to the image plane. As a result, the model can focus on learning global scene geometry and pose relations without disentangling per-view calibration parameters, thereby simplifying the learning objective and improving optimization stability. 

This reformulation also benefits pose estimation accuracy. In conventional perspective-based pipelines, pose estimation is often ill-posed in textureless or geometrically ambiguous indoor regions due to limited visibility. In contrast, ERP-based observation provides globally consistent angular coverage, enabling stronger cross-region geometric constraints and improving robustness of relative pose prediction. Empirically, this leads to more stable and accurate pose estimation, particularly in indoor scenes with repetitive structures or narrow corridors. 

A further key modification over VGGT lies in the positional encoding strategy. Existing VGGT-style models rely on perspective-view 3D positional embeddings to encode spatial structure across views. However, such representations are not well-suited for panoramic geometry due to discontinuities and distortions introduced by perspective projection. In contrast, we remove spherical 3D positional encoding and instead adopt a direct ERP-aligned coordinate encoding, which provides a continuous and globally consistent representation of angular coordinates on the panoramic image plane. 

This reformulation enables the model to implicitly reason about full-scene geometry in a unified spherical observation space, improving cross-region consistency and reducing ambiguity at image boundaries. Moreover, by eliminating the need for intrinsic parameter regression and spher- 

ical embedding design, the proposed framework simplifies the overall reconstruction pipeline while maintaining strong geometric reasoning capability. 

#### **3.3.2. Feed-Forward 3D Gaussian Splatting** 

Given the estimated panoramic poses and dense point maps from the feed-forward reconstructor, we decode a renderable 3D Gaussian scene without any per-scene optimization. A straightforward strategy would be to regress one Gaussian from each image pixel independently. However, such pixel-aligned predictions are highly redundant across overlapping views and tend to produce view-dependent primitives. We instead adopt a voxel-aligned Gaussian head that lifts multi-view panoramic observations into a shared 3D volume, fuses them into occupied voxels, and predicts Gaussian primitives from the resulting 3D tokens. 

For each context panorama _Vi_ , the feed-forward network estimates a dense depth map and a camera pose _T_<sup>ˆ</sup> _i_ . We compute the Pl¨ucker ray encoding for every pixel _u_ , which compactly represents both the ray origin _oi_ and the normalized ray direction _di,u_ . The input feature map is then formed by concatenating the RGB color, the predicted depth, and the Pl¨ucker ray encoding along the channel dimension: 


where _Ii,u_ denotes the pixel color and _zi,u_ is the predicted depth at pixel _u_ . 

To capture global structure and cross-view correlations, the feature maps from all context views are partitioned into non-overlapping patches and fed into a global attention module. Self-attention is performed jointly over all patches from all views, enabling the network to reason about interview correspondences and resolve geometric ambiguities. After attention, the processed patches are reassembled into per-view feature maps. To minimize the spatial gap between neighboring pixels and preserve fine-grained detail, we upsample the feature maps back to the original panoramic resolution before back-projection. 

Each pixel feature is then back-projected into 3D world space using the estimated depth and pose. We quantize the resulting 3D points into a voxel grid with cell size _ϵ_ and aggregate all observations falling into the same voxel. To account for varying observation quality, the network predicts a per-pixel confidence weight _wi,u_ , yielding a weighted voxel feature: 


where _Sj_ denotes the set of observations assigned to voxel _j_ , _xi,u_ is the 3D position of pixel _u_ in world coordinates, 

6 

and _pj_ is the resulting voxel center. This fusion step converts redundant multi-view pixel observations into compact, view-consistent 3D tokens. 

To inject 3D structural priors into the fused representations, we apply a _k_ -nearest-neighbor (KNN) attention module over the occupied voxel tokens. Each voxel attends to its spatial neighbors in 3D, allowing the network to capture local geometric relationships and propagate contextual information across adjacent regions, thereby enriching the 2D-originated features with explicit 3D spatial structure. 

Each occupied voxel token, augmented with a positional encoding of its center _pj_ , is decoded by a compact MLP into _K_ Gaussian primitives. For the _k_ -th primitive of voxel _j_ , the network predicts a center offset, scale, rotation quaternion, opacity, and spherical-harmonic color coefficients: 


where _γ_ ( _·_ ) denotes sinusoidal positional encoding. The predicted attributes are parameterized with bounded activations for stable feed-forward inference. The final Gaussian center is obtained as _µj,k_ = _pj_ + ∆ _µj,k_ , and the complete scene is represented as 


which can be rendered in real time via differentiable Gaussian rasterization. 

#### **3.3.3. Training** 

**Training Losses** The feed-forward reconstruction model is trained in two stages. In the first stage, we optimize the camera pose head and depth head using only the camera pose loss and depth loss, following the original formulation of VGGT [33] without modification. Specifically, the camera loss _L_ camera supervises the predicted relative camera poses between frame pairs, while the depth loss _L_ depth applies scale-invariant log-depth regression to the predicted dense point maps. The first-stage objective is 


In the second stage, we freeze the trained camera pose and depth heads and optimize the feed-forward 3D Gaussian Splatting task head. The predicted 3D Gaussians are rendered into the input views, and the task head is supervised using an RGB reconstruction loss implemented as an _ℓ_ 2 loss between the rendered and ground-truth images: 


where<sup>ˆ</sup> **I** and **I** denote the rendered and ground-truth RGB images, respectively. This staged training strategy first establishes reliable geometric predictions and subsequently learns to convert them into feed-forward 3D Gaussian scene representations. 

**Training Data** Our model is trained on three panoramic indoor datasets. **RealSee3D** [14] provides 9 _,_ 000 procedurally-generated synthetic indoor scenes with a total of 270K viewpoints, featuring diverse layouts and decoration styles. **InteriorGS** [24] provides 602 real-world indoor scenes, from which we uniformly sample 50 frames per scene from 800-frame dense trajectories for model training. **Structured3D** [41] offers 3 _,_ 131 synthetic indoor scenes with photorealistic rendering and rich structural annotations. All datasets provide ground-truth camera poses and depth maps, which serve as supervision for the feed-forward reconstruction model. 

To mitigate the scarcity of high-quality synthetic data, we generate our own large-scale dataset, **PanoHome** , a photorealistic indoor panoramic dataset. We build on the procedural scene generators Infinigen [26] and Infinigen Indoors [27], which synthesize fully parametric, physically based 3D rooms; our contribution replaces their perspective camera with an equirectangular (360<sup>_◦_</sup> ) panoramic renderer and a per-room dense trajectory sampler tailored to feedforward panoramic reconstruction. Because every scene is synthesized rather than captured, RGB, depth, and pose are rendered from the same ground-truth geometry and are therefore _perfectly aligned_ , free of the sensor noise, holes, and privacy or licensing constraints of real captures. Each sample provides an equirectangular RGB image (2880 _×_ 1440) and a _continuous metric depth map_ at float32 precision—strictly finer than the 16-bit quantized depth of prior datasets—together with a complete 6DoF camera-toworld pose (the equirectangular parameterization fully determines the projection, so no pinhole intrinsics are needed). We further sample _∼_ 30 panoramas per room along controlled trajectories, yielding _dense multi-view overlap_ , and release every scene as a complete, _editable_ 3D asset that enables re-rendering, additional supervision, and embodied simulation. As summarized in Table 1, these properties directly address the limitations of existing indoor panoramic datasets. Matterport3D [3] and Stanford2D3D [2] provide only discrete panoramas with limited overlap; Structured3D [41] renders a single panorama per room, yielding _no_ cross-view overlap; Pano3D [1] omits camera poses; and 360Loc [7] suffers from RGB–depth misalignment. Crucially, none of them exposes an editable 3D scene, whereas **PanoHome** combines dense, high-overlap trajectories with pixel-perfect metric geometry and full 3D editability, and its procedural nature makes scale and diversity effectively unbounded. 

## **4. Experiments** 

### **4.1. Panoramic Video Generation Data** 

Our experiments use two panoramic sources. **InteriorGS** [29] provides 602 photorealistic indoor scenes with RGB panoramas, dense ERP camera trajectories of up to 

7 

Table 1. Comparison with prior _indoor_ panoramic datasets (✓: available; ×: unavailable; _∼_ : partial / restricted). Unlike existing datasets that are sparse, geometrically imprecise, or provide no editable 3D, our procedurally generated dataset offers pixel-perfect metric geometry, dense per-room multi-view overlap, and a complete editable 3D scene for every sample. 

|Dataset|#Images|Real/Syn.|Pose|Depth|3D Model|Characteristics|
|---|---|---|---|---|---|---|
|PanoSUNCG [32]|_∼_25K|Syn.|6DoF|8-bit<br>|×|Deprecated, not legally available|
|Matterport3D [3]|_∼_10.8K|Real|6DoF|16-bit<sup>_†_</sup>|_∼_recon.|Discrete panos, limited overlap|
|Structured3D [41]|_∼_12K|Syn.|3DoF|16-bit|_∼_CAD|One pano per room, no overlap|
|Stanford2D3D [2]|_∼_1.4K|Real|6DoF|16-bit<sup>_†_</sup>|✓mesh|Small scale, limited overlap|
|Pano3D [1]|_∼_42K|Mixed|×|16-bit<br>|×|No camera pose|
|360Loc [7]|_∼_2.9K|Real|6DoF|sparse<sup>_†_</sup>|×|LiDAR depth, RGB–depth mismatch|
|**PanoHome**|_∼_30K|Syn.|6DoF|float32|✓_editable_|Dense (_∼_30 panos/room), high overlap|


> _†_ Real captured depth: contains sensor noise, missing regions, or RGB–depth misalignment. 

800 frames per scene, and ground-truth depth from SAGE3D [24]. For each scene we build trajectory-conditioned training tuples: the ground-truth camera track defines the roaming trajectory _T_ , and we render the geometry-warped condition video and its visibility mask from the scene’s panorama and depth. Clip lengths are sampled uniformly so that a single scene yields many clips spanning a continuum of traversal scales. All conditions are pre-rendered offline and cached so that training is I/O-bound rather than render-bound. The held-out test split contains 60 scenes for ground-truth evaluation. **RealSee3D** [14] provides 9 _,_ 000 procedurally-generated synthetic indoor scenes with diverse layouts and decoration styles. Since it provides only static RGB-D panoramic captures without roaming video sequences, we use it solely for zero-shot evaluation, drawing 100 panoramic scenes as the generalization set. 

### **4.2. Metrics** 

**Panoramic video generation.** On the InteriorGS test split we report frame-level fidelity (PSNR, SSIM, LPIPS, WSPSNR) and video-level realism (FVD, FID); FVD is used for relative comparison across models only, as the test set is too small for an absolute score. To quantify trajectory controllability, we reconstruct camera poses from the generated frames via COLMAP, align to the ground-truth trajectory with Sim(3) Umeyama, and report ATE, RRE, and RTE. On RealSee3D, which has no roaming-video ground truth, we drive inference with our own collision-free ring trajectories and report FID, a loop-closure score (following OmniRoam [21]), first/last-frame LPIPS-Loop, and the same pose metrics against the planned trajectory. 

**3D reconstruction.** We evaluate the reconstruction module along two axes. _(i) Trajectory estimation accuracy._ Predicted camera poses are Sim(3)-aligned to the ground-truth trajectory via the Umeyama algorithm, and we report the Absolute Trajectory Error (ATE), its RMSE variant (ATE-RMSE), and the Relative Pose Error in translation (RPE _t_ ) and rotation (RPE _r_ , in degrees) computed between consecutive frame pairs. _(ii) Rendering quality._ We render the reconstructed 3D Gaussians from both the input (context) camera poses and held-out novel viewpoints, and report PSNR, SSIM, and LPIPS against the corresponding 

ground-truth panoramas. 

### **4.3. Implementation Details** 

**Panoramic video generation.** We adapt Wan2.2-TI2V5B [30] with LoRA [6] (rank 48, _α_ = 48) initialized from Matrix-3D [37]. The backbone and 3D VAE are frozen; only the LoRA adapters, geometry-warp conditioning tokens, and the step-size embedding are trained. All models are optimized with AdamW in bf16 using DeepSpeed ZeRO-1 and gradient checkpointing, at 720 _×_ 1440 with 81 frames. For ablation we train a +Mixed Training variant using only the flow-matching objective without the shortcutmodel formulation. At inference, the shortcut model uses 4 CFG-free denoising steps; the ablation baseline uses 10 guided steps. 

**Feed-forawrd reconstruction.** We resize equirectangular panoramas of varying resolutions to 392 _×_ 784 for training. The model is trained on 32 NVIDIA H100 (80 GB) GPUs for 8 days. For each batch, we randomly sample 2 to 32 frames from a randomly selected training scene, enabling the model to handle varying numbers of context views at inference time. All training is conducted in bf16 mixed precision with the AdamW optimizer, following the hyperparameter settings of the original VGGT [33]. 

### **4.4. Panoramic Video Generation** 

We evaluate trajectory-controllable panoramic video generation by comparing our full model, Ours (4-step), against the geometry-only conditioning baseline Matrix-3D [37]. Both methods share the same Wan2.2-TI2V-5B [30] backbone, conditions, and trajectories; they differ in the proposed training components and the resulting sampler (10 guided steps for Matrix-3D vs. 4 guidance-free steps for ours). Per-component ablation is reported separately in Table 4. We evaluate trajectory subsampling factors _r ∈ {_ 1 _,_ 2 _,_ 4 _}_ . For a fixed sequence length of 81 frames, _r_ denotes the temporal stride used to sample the ground-truth trajectory. Increasing _r_ therefore enlarges both the interframe camera displacement and the total traversal extent while keeping the number of generated frames fixed. This evaluation targets the long-distance regime that motivates our design. 

8 

Table 2. Panoramic video generation on InteriorGS (60 scenes), merging frame-level fidelity and trajectory controllability under both protocols. _Top block:_ native 720 _×_ 1440. _Bottom block:_ outputs from all methods are resized to a common resolution of 480 _×_ 960 before computing the evaluation metrics. This block also includes OmniRoam [21] (10 steps, CFG scale 5 _._ 0). Pose metrics (ATE, RRE, RTE) are estimated via COLMAP and Sim(3)-aligned to the ground-truth trajectory. _GT track_ = poses re-estimated from the ground-truth frames via COLMAP (reference). _↑_ / _↓_ = higher/lower is better; **bold** = best per trajectory stride within each block (excluding reference). 

||Method|Stride_r_|Steps|PSNR_↑_|SSIM_↑_|LPIPS_↓_|WS-PSNR_↑_|FVD_↓_|FID_↓_|ATE_↓_|RRE (<sup>_◦_</sup>)_↓_|RTE_↓_|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||GT track (ref.)|_r_=1|–||||–|||0.0024|0.0269|0.0008|
||Matrix-3D|_r_=1|10|21.584|0.7977|0.2771|21.146|11.101|26.052|0.0081|0.0274|0.0021|
|40|Ours (4-step)|_r_=1|4|**23.499**|**0.8272**|**0.2330**|**22.970**|**7.932**|**18.249**|**0.0035**|**0.0212**|**0.0016**|
|14|GT track (ref.)|_r_=2|–||||–|||0.0013|0.0158|0.0007|
|_×_|Matrix-3D|_r_=2|10|19.958|0.7562|0.3190|19.489|12.270|27.921|0.0312|0.3212|0.0073|
|720|Ours (4-step)|_r_=2|4|**21.925**|**0.7905**|**0.2718**|**21.367**|**9.228**|**20.310**|**0.0068**|**0.0285**|**0.0026**|
||GT track (ref.)|_r_=4|–||||–|||0.0026|0.0216|0.0010|
||Matrix-3D|_r_=4|10|18.034|0.7064|0.3749|17.607|15.066|30.720|0.0952|0.1333|0.0147|
||Ours (4-step)|_r_=4|4|**20.288**|**0.7506**|**0.3194**|**19.746**|**10.810**|**22.133**|**0.0218**|**0.0460**|**0.0066**|
||GT track (ref.)|_r_=1|–||||–|||0.0026|0.0316|0.0014|
||OmniRoam|_r_=1|10|17.562|0.6596|0.3312|17.303|11.708|24.382|0.0160|0.0872|0.0034|
||Matrix-3D|_r_=1|10|22.003|0.8059|0.2500|21.615|10.831|24.319|0.0085|**0.0358**|0.0024|
||Ours (4-step)|_r_=1|4|**23.889**|**0.8342**|**0.2105**|**23.407**|**7.746**|**18.006**|**0.0048**|0.0371|**0.0023**|
|960|GT track (ref.)|_r_=2|–||||–|||0.0034|0.0311|0.0013|
|_×_|OmniRoam|_r_=2|10|16.826|0.6373|0.3678|16.541|13.121|25.887|0.0358|0.1791|0.0115|
|80|Matrix-3D|_r_=2|10|20.306|0.7585|0.2959|19.880|11.678|26.676|0.0232|0.1358|0.0048|
|4|Ours (4-step)|_r_=2|4|**22.247**|**0.7927**|**0.2498**|**21.727**|**9.022**|**20.122**|**0.0066**|**0.0377**|**0.0028**|
||GT track (ref.)|_r_=4|–||||–|||0.0092|0.1159|0.0034|
||OmniRoam|_r_=4|10|16.021|0.6185|0.4120|15.673|14.665|26.631|0.0685|0.2288|0.0187|
||Matrix-3D|_r_=4|10|18.198|0.6881|0.3517|17.795|15.034|29.885|0.1071|0.5378|0.0210|
||Ours (4-step)|_r_=4|4|**20.545**|**0.7465**|**0.2997**|**20.035**|**10.531**|**21.630**|**0.0224**|**0.1342**|**0.0070**|


#### **4.4.1. Quantitative Comparison** 

The top block of Table 2 reports frame-level fidelity and trajectory controllability on the InteriorGS test split. Ours (4-step) outperforms Matrix-3D at every trajectory stride by roughly +2 dB PSNR with large reductions in LPIPS, FVD and FID. The gap widens with traversal distance: at _r_ =4 Matrix-3D drops to PSNR 18 _._ 03 and FID 30 _._ 72, while our model stays higher at PSNR 20 _._ 29 and FID 22 _._ 13. This indicates that the proposed training strategy mitigates the long-distance quality collapse of geometry-only conditioning. Pose accuracy is verified independently via COLMAP reconstruction on the generated and ground-truth frames. On trajectory accuracy, Matrix-3D’s pose tracking collapses at _r_ =4 (ATE 0 _._ 095 vs. ground-truth reference 0 _._ 003), whereas our model stays stable (ATE 0 _._ 022) and is close to the ground-truth accuracy at the smaller strides. 

#### **4.4.2. Qualitative Comparison** 

Figure 3 compares Matrix-3D with Ours (4-step) on a longrange ( _r_ =4) indoor traversal. As the camera moves far from the input viewpoint, Matrix-3D produces blurred textures and broken structures in newly disoccluded regions, whereas our model remains sharp and geometrically coherent with only 4 denoising steps. 

For a direct comparison with OmniRoam [21], whose native output resolution differs from ours, we resize all outputs 

to a common 480 _×_ 960 and recompute every metric (bottom block of Table 2). OmniRoam, which is based on an imageto-video model (Wan2.1-T2V-1.3B) and therefore uses a considerably smaller and architecturally distinct backbone from ours, trails both geometry-conditioned models by a large margin (PSNR 17 _._ 56 vs. our 23 _._ 96 at _r_ =1) and drifts severely in pose tracking as the traversal lengthens (ATE 0 _._ 069 at _r_ =4), similar to Matrix-3D. OmniRoam is also structurally incompatible with our trajectory-controllable formulation: it conditions on a normalized trajectory representation (raw poses collapsed into a scalar speed signal) that discards the metric geometry needed to follow the collision-free NavMesh paths produced by our planner. Ours (4-step) outperforms both baselines at every trajectory stride on all metrics. 

#### **4.4.3. Zero-Shot Generalization** 

Table 3 evaluates on 99 RealSee3D scenes, which provide only static RGB-D panoramas and thus have no groundtruth videos or trajectories. OmniRoam is excluded from quantitative evaluation because, as shown in Figure 5, it produces visible wall-penetration artifacts: its trajectory representation discards metric geometry, so NavMesh collision constraints are not respected and the resulting frames are geometrically invalid. Our full model achieves the best FID, best loop-closure score, and best LPIPS-Loop, clearly 

9 


Figure 3. Qualitative comparison on a long-range ( _r_ =4) indoor traversal. Matrix-3D degrades into blurry, structurally inconsistent content in disoccluded regions as the camera travels farther, while our full model remains sharp and geometrically coherent. GT shown for reference; per-component ablation in Table 4. 


Figure 4. Qualitative comparison at 480 _×_ 960 ( _r_ =1) including OmniRoam. OmniRoam produces blurry, trajectory-inconsistent frames that diverge progressively from the intended path, while our model remains sharp and geometrically faithful. GT shown for reference; additional scenes in the supplement. 

outperforming Matrix-3D on all three metrics. It also substantially reduces pose drift: relative to Matrix-3D it lowers ATE by roughly 62% and RTE by 49%, and also improves RRE, verified via COLMAP on the generated frames. All of this is achieved with only 4 denoising steps, showing the benefits transfer zero-shot to scenes from a different dataset. 

Table 3. Zero-shot evaluation on RealSee3D (no roaming-video ground truth). Appearance/consistency metrics over 99 scenes; pose metrics (ATE, RRE, RTE) via COLMAP over 95 scenes. Loop = trajectory loop-closure score (following OmniRoam [21]); LPIPS-Loop = first/last-frame LPIPS. **Bold** = best. 

|Method|Steps|FID_↓_|Loop_↑_|LPIPS-Loop_↓_|ATE_↓_|RRE(<sup>_◦_</sup>)_↓_|RTE_↓_|
|---|---|---|---|---|---|---|---|
|Matrix-3D|10|17.29|2.787|0.1629|0.1176|0.2209|0.0563|
|Ours(4-step)|4|**16.36**|**3.383**|**0.1188**|**0.0448**|**0.1662**|**0.0289**|


### **4.5. Feed-Forward 3DGS** 

We next evaluate the feed-forward 3D Gaussian reconstruction that lifts the panoramic video into a real-time renderable scene. 

**Quantitative Comparison.** Table 5 compares our method against DA3, HY-WM2.0, and PanoWorld [10] on the 4 _×_ - speed test set, where we uniformly sample _N_ input (con- 

10 


Figure 5. Zero-shot qualitative comparison on RealSee3D (no ground truth available). OmniRoam exhibits trajectory-inconsistent wallpenetration artifacts (frames pass through walls), which is why its metrics are not reported in Table 3. Our model generates geometrically faithful content and respects collision constraints with only 4 denoising steps. Two representative scenes shown; each row group is one scene. 

Table 4. Ablation of the proposed components across trajectory strides (InteriorGS, 60 scenes). NFE = steps _×_ forward passes per step (CFG adds an unconditional pass). Pose metrics (ATE, RRE, RTE) via COLMAP. **Bold** = best per trajectory stride. 

|Method|Stride_r_|Steps|NFE|PSNR_↑_|SSIM_↑_|LPIPS_↓_|FVD_↓_|FID_↓_|ATE_↓_|RRE(<sup>_◦_</sup>)_↓_|RTE_↓_|
|---|---|---|---|---|---|---|---|---|---|---|---|
|Matrix-3D|_r_=1|10|20|21.584|0.7977|0.2771|11.101|26.052|0.0081|0.0274|0.0021|
|+Mixed Training|_r_=1|10|20|**23.584**|**0.8353**|**0.2220**|8.849|20.209|0.0062|0.0979|0.0024|
|Ours(4-step)|_r_=1|4|4|23.499|0.8272|0.2330|**7.932**|**18.249**|**0.0035**|**0.0212**|**0.0016**|
|Matrix-3D|_r_=2|10|20|19.958|0.7562|0.3190|12.270|27.921|0.0312|0.3212|0.0073|
|+Mixed Training|_r_=2|10|20|21.921|**0.7993**|**0.2585**|9.500|21.892|0.0076|0.0619|0.0028|
|Ours(4-step)|_r_=2|4|4|**21.925**|0.7905|0.2718|**9.228**|**20.310**|**0.0068**|**0.0285**|**0.0026**|
|Matrix-3D|_r_=4|10|20|18.034|0.7064|0.3749|15.066|30.720|0.0952|0.1333|0.0147|
|+Mixed Training|_r_=4|10|20|20.230|**0.7609**|**0.3040**|10.864|22.144|0.0403|0.2018|0.0097|
|Ours(4-step)|_r_=4|4|4|**20.288**|0.7506|0.3194|**10.810**|**22.133**|**0.0218**|**0.0460**|**0.0066**|


text) views and _N_ held-out novel views per scene ( _N ∈ {_ 2 _,_ 4 _,_ 8 _}_ , denoted _N_ @ _N_ ). To isolate the contribution of the reconstruction decoder, we use real captured videos rather than trajectory-controllable generated videos, eliminating the extra variable introduced by generative artifacts. Two observations can be made. **First** , our feed-forward 3DGS decoder consistently outperforms all baselines on both context-view reconstruction and novel-view synthesis across all three settings. For example, at 4@4 our method achieves 25 _._ 95/23 _._ 95 PSNR on context/novel views, sur- 

passing the best baseline PanoWorld by 3 _._ 63/5 _._ 33 dB, and similarly leads in SSIM while remaining competitive in LPIPS. This indicates that our decoder recovers accurate Gaussians from geometrically consistent observations even under sparse, wide-baseline panoramic coverage. We further provide qualitative comparisons in Fig. 6, where our method produces sharper textures and more faithful geometry than the baselines. **Second** , we observe that the rendering quality on context views gradually degrades as the number of reconstructed images increases (e.g., PSNR drops 

11 


Figure 6. Qualitative comparison of novel view synthesis on the InteriorGS dataset (60 scenes). We evaluate all methods under the 4@4 setting. 

Table 5. Comparison on panorama feed-forward 3DGS (trajectory stride _r_ =4). _N_ @ _N_ : _N_ context views, _N_ novel views. **Bold** = best. 

|||PSN|R_↑_|SSI|M_↑_|LPI|PS_↓_|
|---|---|---|---|---|---|---|---|
|Setting|Method|Ctx.|Nov.|Ctx.|Nov.|Ctx.|Nov.|
||DA3<sup>_∗_</sup><br>|17.40|16.45|0.72|0.70|0.47|0.53|
||DA3<sup>_†_</sup>|18.80|17.35|0.74|0.72|0.40|0.46|
|2@2|HY-WM2.0<sup>_∗_</sup>|17.43|15.43|0.66|0.60|0.40|0.48|
||HY-WM2.0<sup>_†_</sup>|21.34|17.92|0.76|0.68|0.29|0.40|
||PanoWorld|24.73|15.53|**0.88**|0.63|**0.11**|0.37|
||Ours|**26.75 **|**19.55**|0.87|**0.76**|0.36|**0.30**|
||DA3<sup>_∗_</sup>|17.68|17.45|0.72|0.72|0.47|0.49|
||DA3<sup>_†_</sup>|19.03|18.78|0.73|0.73|0.40|0.42|
|4@4|HY-WM2.0<sup>_∗_</sup><br>|19.17|18.11|0.71|0.68|0.38|0.42|
||HY-WM2.0<sup>_†_</sup>|20.51|19.58|0.74|0.72|0.34|0.37|
||PanoWorld|22.32|18.62|0.81|0.69|**0.19**|0.30|
||Ours|**25.95 **|**23.95 **|**0.866 **|**0.831**|0.265|**0.299**|
||DA3<sup>_∗_</sup>|17.95|17.87|0.73|0.72|0.46|0.47|
||DA3<sup>_†_</sup>|19.16|19.10|0.73|0.73|0.41|0.41|
|8@8|HY-WM2.0<sup>_∗_</sup>|19.86|19.51|0.72|0.71|0.37|0.39|
||HY-WM2.0<sup>_†_</sup>|19.04|18.85|0.71|0.70|0.38|0.39|
||PanoWorld|21.83|19.91|0.79|0.72|**0.21**|**0.27**|
||Ours|**23.97 **|**23.23**|**0.83**|**0.81**|0.31|0.32|


_∗_ 6-cubemap<sup>_†_</sup> 12-cubemap 

from 26 _._ 75 at 2@2 to 25 _._ 95 at 4@4 and further to 23 _._ 97 at 8@8). This is because, with more images involved in reconstruction, even slight misalignment across views accumulates and is amplified during voxel fusion, which in turn noticeably degrades the final rendering quality. 

### **4.6. Ablation Study** 

Table 4 isolates the contribution of each component across all three traversal speeds and reports NFE, accounting for both step count and the unconditional branch of classifierfree guidance. Long–short mixed training contributes most of the quality gain (+2 _._ 0 dB PSNR, _−_ 5 _._ 8 FID at _s_ =1 _×_ ), and the improvement grows with traversal distance. Shortcut self-consistency training then removes the unconditional branch (CFG-free) and cuts the step count from 10 to 4, reducing NFE by 5 _× without_ a loss in fidelity; it attains the best FVD, FID, and pose accuracy at all speeds. This combination is what makes deployment on a single consumer GPU feasible: the 4-step CFG-free sampler reduces diffusion cost from _∼_ 316 s to 63 s, bringing the complete perscene pipeline to _∼_ 147 s on a single NVIDIA RTX 4090 (24 GB) with no per-scene optimization. 

**Ablation of decoder components.** Table 6 isolates the contribution of each attention mechanism in the Gaussian decoder under the 4@4 setting. Removing the KNN attention blocks (w/o KNN Attn) drops novel-view PSNR by 0 _._ 80 dB and increases LPIPS by 0 _._ 022, confirming that local 3D neighborhood reasoning is critical for resolving geometric ambiguities in the voxel tokens. Removing the multi-view attention blocks (w/o MV Attn) causes a smaller but consistent degradation across all metrics, indicating that cross-view feature exchange helps disambiguate occluded regions and improves multi-view consistency. The full model combining both mechanisms achieves the best performance on all metrics. 

12 

Table 6. Ablation of the 3D Gaussian decoder components (4@4 setting, 4 _×_ speed test set). **Bold** = best. 

||PSN|R_↑_|SSI|M_↑_|LPI|PS_↓_|
|---|---|---|---|---|---|---|
|Method|Ctx.|Nov.|Ctx.|Nov.|Ctx.|Nov.|
|w/o voxel fusion|24.34|23.01|0.837|0.810|0.301|0.336|
|w/o KNN Attn|25.00|23.15|0.849|0.818|0.293|0.321|
|w/o MV Attn|25.66|23.45|0.851|0.827|0.273|0.301|
|1 gaussian per voxel|25.12|23.13|0.847|0.822|0.273|0.317|
|Full Model|**25.95 **|**23.95 **|**0.866 **|**0.831 **|**0.265 **|**0.299**|


### **4.7. Joint Analysis of Generation and 3D Reconstruction** 

We directly compare COLMAP and our feed-forward VGGT estimator as pose recovery tools, on both groundtruth frames and our generated frames across all trajectory strides. Table 8 evaluates on GT frames (upper bound) and Table 7 evaluates on our generated frames (pipeline output). Table 9 reports the end-to-end 3DGS rendering quality from the generated videos. 

On GT frames, COLMAP achieves near-zero ATE ( _≤_ 0 _._ 003) while VGGT has a systematic noise floor around 0 _._ 023–0 _._ 030, so COLMAP is the more precise absolute estimator. On generated frames, COLMAP reveals the true trajectory drift as traversal distance grows ( _r_ =4: ATE 0 _._ 022), whereas VGGT remains more stable (ATE 0 _._ 035) because it relies on local feature matching that is partially robust to global drift. The gap between GT and generated frames is small for VGGT at all trajectory strides (e.g. 0 _._ 029 vs. 0 _._ 030 at _r_ =1), which shows that our generation quality preserves enough texture and structure for the reconstruction module to recover locally consistent metric poses for 3DGS. The 3DGS decoder then achieves 18 _._ 6–19 _._ 7 dB novel-view PSNR across all trajectory strides (Table 9), giving a complete and usable reconstruction pipeline. 

Table 7. Pose estimation on _generated frames_ (Ours, 4-step): COLMAP vs. our feed-forward VGGT estimator. COLMAP exposes trajectory drift; VGGT measures pose recovery quality for downstream 3DGS. 

|Estimator|Stride_r_|ATE_↓_|RRE(<sup>_◦_</sup>)_↓_|RTE_↓_|
|---|---|---|---|---|
|COLMAP|_r_=1|**0.0035**|**0.0212**|**0.0016**|
|VGGT(ours)|_r_=1|0.0290|0.0542|0.0282|
|COLMAP|_r_=2|**0.0068**|**0.0285**|**0.0026**|
|VGGT(ours)|_r_=2|0.0236|0.0531|0.0269|
|COLMAP|_r_=4|**0.0218**|**0.0460**|**0.0066**|
|VGGT(ours)|_r_=4|0.0346|0.0526|0.0357|


Table 8. Pose estimation on _ground-truth frames_ at trajectory stride _r_ =4: COLMAP vs. our feed-forward VGGT estimator. Lower values indicate higher precision. 

|Estimator|ATE_↓_|ATE-RMSE_↓_|RPE_t↓_|RPE_r_(<sup>_◦_</sup>)_↓_|
|---|---|---|---|---|
|COLMAP|**0.0042**|**0.0046**|**0.0019**|**0.03**|
|PanoVGGT|0.0070|0.0083|0.0045|0.51|
|VGGT (ours)|0.0170|0.0218|0.0148|0.04|


Table 9. 3DGS rendering quality on generated frames (Ours, 4- step). _Inp._ = input-view reconstruction; _Nov._ = novel-view synthesis. 

|Stride_r_|PSN|R_↑_|SSI|M_↑_|LPI|PS_↓_|
|---|---|---|---|---|---|---|
||Inp.|Nov.|Inp.|Nov.|Inp.|Nov.|
|_r_=1|21.08|19.45|0.73|0.67|0.22|0.26|
|_r_=2|22.06|19.68|0.76|0.67|0.20|0.26|
|_r_=4|22.56|18.64|0.78|0.64|0.20|0.31|


## **5. Discussion and Limitations** 

Genie Sim PanoWorld demonstrates that a single ERP panorama is sufficient to produce a freely roamable 3D Gaussian scene entirely feed-forward, without any perscene optimization. The key enabler is the two-stage design: the trajectory-controllable video generator converts a single view into wide-baseline, geometrically consistent multi-view evidence, and the metric SE(3) trajectory ties both stages into one coherent frame. Long–short mixed training and self-consistency training for shortcut models make this practical on commodity hardware, substantially reducing NFE relative to a CFG-guided baseline while maintaining or improving all reported quality metrics. 

Several limitations remain. First, the pipeline assumes a static scene: moving objects such as people or furniture are not modeled, and their presence can introduce temporal inconsistencies in the generated video. Second, NavMesh construction depends on the quality of the monocular depth estimate; specular reflections, transparent surfaces, and large textureless planes can produce depth errors that lead to suboptimal trajectories or residual wall-penetration artifacts. Third, the geometry-warped conditioning becomes increasingly unreliable beyond the trajectory strides tested ( _r_ =4), where the fraction of disoccluded content can exceed the model’s inpainting capacity. Finally, the current training distribution is dominated by indoor environments, and performance on outdoor or large-scale scenes has not been evaluated. 

Future work can address these limitations in several ways. Incorporating a video-object segmentation prior to mask dynamic content during training and inference would decouple scene geometry from transient objects. Using a more robust depth-completion approach or fine-tuning the 

13 

depth backbone on panoramic data with known metric scale would improve NavMesh quality. Extending the shortcutmodel framework to longer-context video diffusion models and larger-scale would push the navigable range further. Finally, adapting the 3D Gaussian decoder to outdoor and mixed-scale environments is a natural step toward broader real-world deployment. 

## **6. Conclusion** 

We presented Genie Sim PanoWorld, a feed-forward pipeline that turns a single 360<sup>_◦_</sup> ERP panorama into a freely roamable 3D Gaussian scene without per-scene optimization or multi-view capture. The core insight is to bridge the single-view input and the 3D output with an explicit, trajectory-controllable panoramic video: a NavMeshplanned SE(3) path is injected via dense geometry-warped conditioning into a latent video diffusion model trained with long–short mixed supervision and a self-consistency objective for shortcut models, producing high-fidelity panoramic video in four CFG-free steps; a feed-forward panoramic reconstructor then lifts the result into a real-time renderable 3DGS scene. Experiments show that Genie Sim PanoWorld consistently outperforms prior baselines in both video fidelity and trajectory accuracy while running the complete pipeline efficiently on a single consumer-grade GPU. We hope Genie Sim PanoWorld serves as a practical foundation for panorama-driven scene understanding, interactive virtual tours, and embodied AI navigation. 

## **References** 

- [1] Georgios Albanis, Nikolaos Zioulis, Petros Drakoulis, Vasileios Gkitsas, Vladimiros Sterzentsenko, Federico Alvarez, Dimitrios Zarpalas, and Petros Daras. Pano3D: A holistic benchmark and a solid baseline for 360<sup>_◦_</sup> depth estimation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 3727–3737, 2021. 7, 8 

- [2] Iro Armeni, Sasha Sax, Amir R Zamir, and Silvio Savarese. Joint 2D-3D-Semantic data for indoor scene understanding. _arXiv preprint arXiv:1702.01105_ , 2017. 7, 8 

- [3] Angel Chang, Angela Dai, Thomas Funkhouser, Maciej Halber, Matthias Niessner, Manolis Savva, Shuran Song, Andy Zeng, and Yinda Zhang. Matterport3D: Learning from RGB-D data in indoor environments. _arXiv preprint arXiv:1709.06158_ , 2017. 7, 8 

- [4] Zixun Fang, Kai Zhu, Zhiheng Liu, Yu Liu, Wei Zhai, Yang Cao, and Zheng-Jun Zha. ViewPoint: Panoramic video generation with pretrained diffusion models. In _Advances in Neural Information Processing Systems_ , pages 12486–12508. Curran Associates, Inc., 2025. 2 

- [5] Kevin Frans, Danijar Hafner, Sergey Levine, and 

Pieter Abbeel. One step diffusion via shortcut models. In _International Conference on Learning Representations (ICLR)_ , 2025. 2, 5 

- [6] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. LoRA: Low-Rank Adaptation of Large Language Models. In _International Conference on Learning Representations (ICLR)_ , 2022. 4, 8 

- [7] Huajian Huang, Changkun Liu, Yipeng Zhu, Hui Cheng, Tristan Braud, and Sai-Kit Yeung. 360Loc: A dataset and benchmark for omnidirectional visual localization with cross-device queries. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 22314–22324, 2024. 7, 8 

- [8] Tianyu Huang, Wangguandong Zheng, Tengfei Wang, Yuhao Liu, Zhenwei Wang, Junta Wu, Jie Jiang, Hui Li, Rynson Lau, Wangmeng Zuo, and Chunchao Guo. Voyager: Long-Range and World-Consistent Video Diffusion for Explorable 3D Scene Generation. _ACM Transactions on Graphics_ , 44(6):1–15, 2025. 2 

- [9] Team HY-World, Chenjie Cao, Xuhui Zuo, Zhenwei Wang, Yisu Zhang, Junta Wu, Zhenyang Liu, Yuning Gong, Yang Liu, Bo Yuan, Chao Zhang, Coopers Li, Dongyuan Guo, Fan Yang, Haiyu Zhang, Hang Cao, Jianchen Zhu, Jiaxin Lin, Jie Xiao, Jihong Zhang, Junlin Yu, Lei Wang, Lifu Wang, Lilin Wang, Linus, Minghui Chen, Peng He, Penghao Zhao, Qi Chen, Rui Chen, Rui Shao, Sicong Liu, Wangchen Qin, Xiaochuan Niu, Xiang Yuan, Yi Sun, Yifei Tang, Yifu Sun, Yihang Lian, Yonghao Tan, Yuhong Liu, Yuyang Yin, Zhiyuan Min, Tengfei Wang, and Chunchao Guo. HY-World 2.0: A Multi-Modal World Model for Reconstructing, Generating, and Simulating 3D Worlds, 2026. 2, 3 

- [10] Jinrang Jia, Zhenjia Li, Yijiang Hu, and Yifeng Shi. PanoWorld: A Generative Spatial World Model for Consistent Whole-House Panorama Synthesis, 2026. 2, 10 

- [11] Hualie Jiang, Ziyang Song, Zhiqiang Lou, Rui Xu, and Minglang Tan. Depth Anything in 360<sup>_◦_</sup> : Towards scale invariance in the wild, 2025. 4 

- [12] Le Jiang, Xiangyu Bai, Bishoy Galoaa, Shayda Moezzi, Caleb James Lee, Tooba Imtiaz, Edmund Yeh, Jennifer Dy, Yanzhi Wang, and Sarah Ostadabbas. PanoWorld: Geometry-Consistent Panoramic Video World Modeling, 2026. 2 

- [13] Bernhard Kerbl, Georgios Kopanas, Thomas Leimk¨uhler, and George Drettakis. 3D Gaussian Splatting for Real-Time Radiance Field Rendering. _ACM Transactions on Graphics (TOG)_ , 42(4), 2023. 1 

- [14] Linyuan Li, Yan Wu, Xi Li, Lingli Wang, Tong Rao, Jie Zhou, Cihui Pan, and Xinchen Hui. RealSee3D: 

14 

A Large-Scale Multi-View RGB-D Dataset of Indoor Scenes (Version 1.0), 2025. 7, 8 

- [15] Lingen Li, Guangzhi Wang, Xiaoyu Li, Zhaoyang Zhang, Qi Dou, Jinwei Gu, Tianfan Xue, and Ying Shan. CubeComposer: Spatio-temporal autoregressive 4K 360<sup>_◦_</sup> video generation from perspective video. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 32625–32635, 2026. 2 

- [16] Renjie Li, Panwang Pan, Bangbang Yang, Dejia Xu, Shijie Zhou, zhang xuanyang, Zeming Li, Achuta Kadambi, Zhangyang Wang, Zhengzhong Tu, and Zhiwen Fan. 4K4DGen: Panoramic 4D generation at 4K resolution. In _International Conference on Learning Representations_ , pages 100692–100713, 2025. 2 

- [17] Haotong Lin, Sili Chen, Jun Hao Liew, Donny Y. Chen, Zhenyu Li, Guang Shi, Jiashi Feng, and Bingyi Kang. Depth Anything 3: Recovering the visual space from any views. _arXiv preprint arXiv:2511.10647_ , 2025. 3 

- [18] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. In _International Conference on Learning Representations (ICLR)_ , 2023. 5 

- [19] Aoming Liu, Zhong Li, Zhang Chen, Nannan Li, Yi Xu, and Bryan A. Plummer. PanoFree: Tuning-Free Holistic Multi-view Image Generation with CrossView Self-guidance. In _Computer Vision – ECCV 2024_ , pages 146–164. Springer Nature Switzerland, Cham, 2025. 2 

- [20] Jinxiu Liu, Shaoheng Lin, Yinxiao Li, and MingHsuan Yang. DynamicScaler: Seamless and scalable video generation for panoramic scenes. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 6144–6153, 2025. 2 

- [21] Yuheng Liu, Xin Lin, Xinke Li, Baihan Yang, Chen Wang, Kalyan Sunkavalli, Yannick Hold-Geoffroy, Hao Tan, Kai Zhang, Xiaohui Xie, Zifan Shi, and Yiwei Hu. OmniRoam: World Wandering via LongHorizon Panoramic Video Generation, 2026. 2, 3, 4, 8, 9, 10 

- [22] TaiMing Lu, Tianmin Shu, Alan Yuille, Daniel Khashabi, and Jieneng Chen. GenEx: Generating an explorable world. In _International Conference on Learning Representations_ , pages 52310–52335, 2025. 2 

- [23] Lars Mescheder, Wei Dong, Shiwei Li, Xuyang Bai, Marcel Santos, Peiyun Hu, Bruno Lecouat, Mingmin Zhen, Ama¨el Delaunoy, Tian Fang, Yanghai Tsin, Stephan R. Richter, and Vladlen Koltun. SHARP: Sharp monocular view synthesis in less than a second. _arXiv preprint arXiv:2512.10685_ , 2025. 3 

- [24] Bingchen Miao, Rong Wei, Zhiqi Ge, Xiaoquan Sun, Shiqi Gao, Jingzhe Zhu, Renhan Wang, Siliang Tang, Jun Xiao, Rui Tang, and Juncheng Li. Towards physically executable 3D Gaussian for embodied navigation, 2025. 7, 8 

- [25] Ben Mildenhall, Pratul P. Srinivasan, Matthew Tancik, Jonathan T. Barron, Ravi Ramamoorthi, and Ren Ng. NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis. In _European Conference on Computer Vision (ECCV)_ , pages 405–421, 2020. 1 

- [26] Alexander Raistrick, Lahav Lipson, Zeyu Ma, Lingjie Mei, Mingzhe Wang, Yiming Zuo, Karhan Kayan, Hongyu Wen, Beining Han, Yihan Wang, Alejandro Newell, Hei Law, Ankit Goyal, Kaiyu Yang, and Jia Deng. Infinite photorealistic worlds using procedural generation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 12630–12641, 2023. 7 

- [27] Alexander Raistrick, Lingjie Mei, Karhan Kayan, David Yan, Yiming Zuo, Beining Han, Hongyu Wen, Meenal Parakh, Stamatis Alexandropoulos, Lahav Lipson, Zeyu Ma, and Jia Deng. Infinigen Indoors: Photorealistic indoor scenes using procedural generation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 21783–21794, 2024. 7 

- [28] Tianchang Shen, Sherwin Bahmani, Kai He, Sangeetha Grama Srinivasan, Tianshi Cao, Jiawei Ren, Ruilong Li, Zian Wang, Nicholas Sharp, Zan Gojcic, Sanja Fidler, Jiahui Huang, Huan Ling, Jun Gao, and Xuanchi Ren. Lyra 2.0: Explorable Generative 3D Worlds, 2026. 2, 3 

- [29] SpatialVerse Research Team, Manycore Tech Inc. InteriorGS: A 3D Gaussian Splatting Dataset of Semantically Labeled Indoor Scenes. https : / / huggingface . co / datasets / spatialverse/InteriorGS, 2025. 7 

- [30] Wan Team. Wan: Open and Advanced Large-Scale Video Generative Models, 2025. 4, 8 

- [31] Changpeng Wang, Xin Lin, Junhan Liu, Yuheng Liu, Zhen Wang, Donglian Qi, Yunfeng Yan, and Xi Chen. PanoWorld: Towards Spatial Supersensing in 360<sup>_◦_</sup> Panorama World, 2026. 2 

- [32] Fu-En Wang, Hou-Ning Hu, Hsien-Tzu Cheng, JuanTing Lin, Shang-Ta Yang, Meng-Li Shih, Hung-Kuo Chu, and Min Sun. Self-supervised learning of depth and camera motion from 360<sup>_◦_</sup> videos. In _Asian Conference on Computer Vision_ , pages 53–68. Springer, 2018. 8 

- [33] Jianyuan Wang, Minghao Chen, Nikita Karaev, Andrea Vedaldi, Christian Rupprecht, and David Novotny. VGGT: Visual Geometry Grounded Transformer, 2025. 3, 7, 8 

15 

- [34] Jianyuan Wang, Minghao Chen, Shangzhan Zhang, Nikita Karaev, Johannes Sch¨onberger, Patrick Labatut, Piotr Bojanowski, David Novotny, Andrea Vedaldi, and Christian Rupprecht. VGGT-Ω, 2026. 3 

- [35] Xintao Wang, Liangbin Xie, Chao Dong, and Ying Shan. Real-ESRGAN: Training Real-World Blind Super-Resolution with Pure Synthetic Data. In _International Conference on Computer Vision Workshops (ICCVW)_ , 2021. 5 

- [36] Yifei Xia, Shuchen Weng, Siqi Yang, Jingqi Liu, Chengxuan Zhu, Minggui Teng, Zijian Jia, Han Jiang, and Boxin Shi. PanoWan: Lifting diffusion video generation models to 360<sup>_◦_</sup> with latitude/longitude-aware mechanisms. In _Advances in Neural Information Processing Systems_ , pages 148027–148046. Curran Associates, Inc., 2025. 2 

- [37] Zhongqi Yang, Wenhang Ge, Yuqi Li, Jiaqi Chen, Haoyuan Li, Mengyin An, Fei Kang, Hua Xue, Baixin Xu, Yuyang Yin, Eric Li, Yang Liu, Yikai Wang, HaoXiang Guo, and Yahui Zhou. Matrix-3D: Omnidirectional Explorable 3D World Generation, 2025. 2, 4, 8 

- [38] Yuyang Yin, HaoXiang Guo, Fangfu Liu, Mengyu Wang, Hanwen Liang, Eric Li, Yikai Wang, Xiaojie Jin, Yao Zhao, and Yunchao Wei. PanoWorld-X: Generating Explorable Panoramic Worlds via SphereAware Video Diffusion, 2025. 2 

- [39] Cheng Zhang, Hanwen Liang, Donny Y. Chen, Qianyi Wu, Konstantinos N. Plataniotis, Camilo Cruz Gambardella, and Jianfei Cai. PanFlow: Decoupled Motion Control for Panoramic Video Generation. _Proceedings of the AAAI Conference on Artificial Intelligence_ , 40(15):12385–12393, 2026. 2 

- [40] Yisu Zhang, Chenjie Cao, Tengfei Wang, Xuhui Zuo, Junta Wu, Jianke Zhu, and Chunchao Guo. WorldStereo: Bridging camera-guided video generation and scene reconstruction via 3D geometric memories. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 40327–40339, 2026. 2, 3 

- [41] Jia Zheng, Junfei Zhang, Jing Li, Rui Tang, Shenghua Gao, and Zihan Zhou. Structured3D: A large photorealistic dataset for structured 3D modeling. In _European Conference on Computer Vision_ , pages 519–535. Springer, 2020. 7, 8 

16 

