---
title: "Genie 4D: Semantic-Prior-Guided 4D Dynamic Scene Reconstruction"
date: "2026-04-10"
authors: "Yiru Yang; Zhuojie Wu; Nishant Kumar Singh; Max Schulthess"
url: https://arxiv.org/abs/2604.09877
pdf: https://arxiv.org/pdf/2604.09877
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.09877)** / [論文ページ](https://arxiv.org/abs/2604.09877)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**1** 

_YANG ET AL.: GENIE 4D_ 

**1** 

**1 Introduction** 

# **Genie 4D: Semantic-Prior-Guided 4D Dynamic Scene Reconstruction** 

Yiru Yang<sup>_∗_1</sup> 1 University of Zurich yiru.yang@uzh.ch Zurich, Switzerland Zhuojie Wu<sup>_∗_1</sup> 2 ETH Zurich zhuojie.wu@uzh.ch Zurich, Switzerland Nishant Kumar Singh<sup>_∗_1</sup> nishantkumar.singh@uzh.ch Max Schulthess<sup>2</sup> 

mschulthess@ethz.ch 

#### **Abstract** 

At the intersection of computer vision and robotic perception, 4D reconstruction of dynamic scenes connects low-level geometric sensing with high-level semantic understanding. We present **Genie 4D** , a framework that turns hand-held phone capture into a semantically grounded, action-controllable 4D world model. Genie 4D couples a realtime visual-inertial Gaussian splatting front-end for metric geometry with a feed-forward 4D backbone regularized by frozen DINOv3 features acting as structural priors. The semantic priors suppress identity drift during dynamic tracking, while a short conditional diffusion refiner recovers high-frequency surface detail that regression backbones smooth away. Finally, a lightweight latent-action head exposes the reconstructed 4D state to a Genie-style world model trained with a JEPA-style next-embedding objective, so that the scene can be rolled forward under user actions. On the Point Odyssey and TUM-Dynamics benchmarks, Genie 4D retains the linear time complexity _O_ ( _T_ ) of feed-forward baselines while improving 3D tracking accuracy (APD) and reconstruction completeness, and it runs interactively on a single consumer GPU (RTX 5090) from iPhone, Mac, Windows, and Linux capture clients. Genie 4D offers a practical, semanticprior-guided path toward physically grounded world models. 

Human perception of the physical world is inherently four-dimensional: we localise objects in 3D space and track their continuous evolution over time. This spatiotemporal continuity underpins embodied AI, autonomous driving and immersive augmented reality. Classical pipelines treat “3D reconstruction” and “motion tracking” as separate problems. Structurefrom-Motion and Multi-View Stereo excel in static environments but exhibit severe artifacts or tracking failures in dynamic scenes, because camera motion and object deformation are difficult to decouple [3, 8]. 

> © 2026. The copyright of this document resides with its authors. It may be distributed unchanged freely in print or electronic forms. 

> _∗_ Equal contribution. 

**2** 

_YANG ET AL.: GENIE 4D_ 


From a hand-held phone stream to a semantically grounded, action-controllable 4D world model. 


Figure 1: **Genie 4D** turns a live phone stream into a semantically grounded, actioncontrollable 4D world model. A real-time visual–inertial Gaussian-splatting front-end (VIGS-SLAM) supplies metric geometry; a DINOv3-regularised 4D backbone with diffusion refinement supplies semantic 4D; and a latent-action head exposes the result to a world model for interactive rollout. 

Feed-forward networks have reshaped this landscape. St4RTrack [3] unifies reconstruction and tracking through _time-dependent pointmaps_ in a shared world frame, achieving _O_ ( _T_ ) inference, while large transformer backbones such as MapAnything [8] and VGGT [19] regress metric geometry directly from images. These models implicitly learn multi-view constraints and are efficient and robust. However, feed-forward 4D reconstruction still faces two challenges in real, complex scenes: 

- **Absence of semantic awareness.** Mainstream frameworks ( _e.g_ . St4RTrack [3], DUSt3R [20 rely on photometric consistency or geometric reprojection. In textureless regions (plain walls, clothing) or under rapid deformation, geometric cues become ambiguous, causing point-track drift and topological breaks. Without semantic constraints, geometric reconstruction is “blind” to an object’s structural integrity. 

- **Over-smoothing and detail loss.** End-to-end regression recovers global structure efficiently but outputs the conditional mean to minimise an _L_ 2 loss, producing oversmoothed geometry. Fine details—fingers, facial contours, fabric folds—are lost, and naively increasing depth or resolution is prohibitively expensive. 

A third, often overlooked gap is the distance between a perception system and a usable world model. Genie [1] learns action-controllable environments from raw video via a latent action codebook and an autoregressive dynamics model, and recent work shows that jointembedding predictive architectures can be trained end-to-end and stably from pixels [11]. Yet these world models operate on pixels or abstract latents and lack the metric, semantically labelled 4D state that a perception front-end can provide. 

To close these gaps we introduce **Genie 4D** , a framework that imposes semantic understanding as an intrinsic constraint on 4D reconstruction and connects that reconstruction to an interactive world model. Our contributions are: 

1. **Semantic injection via DINOv3.** We inject frozen DINOv3 [16] patch features— whose Gram-anchored dense descriptors remain spatially consistent—into a feed-forward 

**3** 

_YANG ET AL.: GENIE 4D_ 

geometric backbone through a cross-attention adapter, providing semantic anchors that stabilise tracking through occlusion and texture loss. 

2. **Diffusion-based refinement.** A conditional-diffusion module acts as a residual predictor that sharpens the coarse feed-forward geometry in a few denoising steps, recovering high-frequency detail without full generative cost. 

3. **A real, deployable system.** Genie 4D is built on our real-time VIGS-SLAM frontend and runs from iPhone/Mac/Windows/Linux capture clients on a single consumer GPU, and a latent-action head connects the semantic 4D state to a Genie-style world model with a JEPA-style training objective. 

## **2 Related Work** 

**Feed-forward 4D reconstruction.** Before deep learning, dynamic reconstruction relied on optimisation methods ( _e.g_ . DynamicFusion) that were expensive and sensitive to initialisation. St4RTrack [3] predicts pairs of pointmaps that express the geometry of one timestamp in the camera frame of another, enabling _O_ ( _T_ ) inference; however, its pairwise inference lacks global temporal context and drifts semantically over long sequences. MapAnything [8] targets universal metric reconstruction but is designed for static or rigid scenes and ghosts on moving objects, and VGGT [19] uses global attention with quadratic complexity in sequence length. Genie 4D keeps the linear-time pairwise design but augments it with semantic priors and generative refinement. 

**Vision foundation models as priors.** Injecting semantic priors into geometry is a growing trend; Ov3R [5] and Motion4D [23] jointly learn motion and open-vocabulary semantics. DINOv3 [16] is the latest self-supervised ViT: whereas DINOv2 [14] suffers feature degeneration in local patches over long training, DINOv3’s Gram anchoring regularises the feature space so dense features stay discriminative and spatially consistent, making it an illumination- and viewpoint-robust descriptor for dense 4D correspondence. 

**Diffusion in 3D geometry.** Diffusion has moved from 2D images into 3D depth and point clouds; DiffRefine [15] and 3DR-DIFF [12] use diffusion for completion and densification. Genie 4D adopts a conditional residual-diffusion strategy [6] that targets 4D pointmap refinement specifically, balancing the stability of regression with the detail of generation. 

**World models.** Genie [1] introduced generative interactive environments learned unsupervised from video, comprising a video tokenizer, a latent action model and an autoregressive dynamics model. LeWorldModel [11] shows a JEPA [10] can be trained stably end-to-end from pixels with a next-embedding loss and a latent-distribution regulariser. Genie 4D differs by feeding such a world model a metric, semantically labelled 4D state recovered by a real SLAM front-end rather than raw pixels. 

**Visual–inertial SLAM and Gaussian mapping.** DROID-SLAM [18] established dense bundle-adjustment-based deep SLAM, and 3D Gaussian Splatting [9] together with MonoGS [13] enabled high-fidelity online mapping. Our VIGS-SLAM front-end fuses tightly-coupled 

**4** 

_YANG ET AL.: GENIE 4D_ 


Figure 2: **Genie 4D architecture.** A frozen St4RTrack backbone (ViT encoder + dual decoder) maps an RGB video to two 3D pointmaps via a tracking head and a reconstruction head, which are lifted into 4D trajectories. In parallel, a frozen DINOv3 semantic encoder supplies patch-token priors that label the recovered geometry, yielding a semantically grounded 4D reconstruction ( _train, track, tree, building, ground, object_ ). Snowflake icons mark frozen components; the flame icon marks the trainable module. 

IMU preintegration [4] with a Gaussian-splatting map to provide the real-time metric scaffold that Genie 4D builds upon. 

## **3 Method** 

Genie 4D consumes an RGB(-IMU) video sequence _V_ = _{I_ 1 _,..., IT }_ and predicts dense time-variant pointmaps **X** _t_ , camera poses **P** _t_ and per-point semantic descriptors. The pipeline (Fig. 2) has four stages: (i) a real-time VIGS-SLAM front-end for metric poses and a Gaussian map; (ii) dual-stream semantic–geometric feature extraction; (iii) dual-branch pointmap prediction with diffusion refinement; and (iv) a latent-action world-model head. 

### **3.1 Real-Time Visual–Inertial Front-End** 

The VIGS-SLAM front-end tracks the camera and builds a 3D Gaussian map online. A DROID-style update operator performs dense bundle adjustment over a sliding keyframe window, tightly coupled with on-manifold IMU preintegration [4] that resolves metric scale and gravity. Keyframes seed and densify a 3D Gaussian map [9] optimised with photometric, depth and normal terms. The front-end runs in real time as the iPhone streams RGB and IMU over the local network, and it supplies Genie 4D with metric poses **P** _t_ , a scale-consistent map 

_YANG ET AL.: GENIE 4D_ 

**5** 

and monocular depth/normal priors. A pose-graph bundle-adjustment loop and an optional TensorRT path further reduce latency on the RTX 5090. 

### **3.2 Semantic Injection Adapter** 

We extract semantic features **F** _t_<sup>sem</sup> from a frozen DINOv3 ViT-L/14 [16]. To fuse them with geometric features **F** _t_<sup>geo</sup> we use a cross-attention _Semantic Injection Adapter_ : 


The geometric stream queries high-level semantic context: knowing that a surface belongs to a “human body” constrains its valid deformations. 

### **3.3 Dual-Branch Prediction with a Semantic Loss** 

Following St4RTrack [3] we keep two branches: a **tracking** branch predicting<sup>_i_</sup> **X**<sup>_i_</sup> _j_<sup>(the po-</sup> sition at time _j_ of pixels from frame _i_ ) and a **reconstruction** branch predicting<sup>_i_</sup> **X**<sup>_j_</sup> _j_<sup>(the</sup> geometry of frame _j_ ). To combat semantic drift we add a semantic-consistency loss that enforces feature agreement between a query point and its predicted target location: 


where Π is the projection operator. This penalises trajectories that land on semantically dissimilar regions ( _e.g_ . a track drifting from a hand onto a table). 

### **3.4 Geometric Refinement via Conditional Diffusion** 

The coarse output **X** coarse lacks high-frequency detail. We frame refinement as conditional denoising of the residual ∆ **X** = **X** gt _−_ **X** coarse: a forward process adds Gaussian noise to the ground-truth residual, and a network _εθ_ ( **z** _t ,t, c_ ) predicts the noise conditioned on _c_ = _{_ **X** coarse _,_ **F**<sup>fused</sup> _j }_ [6]. A short reverse process ( _K_ =5 steps) sharpens geometry at inference without full generative cost. 

### **3.5 Latent-Action World-Model Head** 

To make the reconstruction _actionable_ , we attach a Genie-style head [1]. A latent-action model encodes the transition between consecutive semantic 4D states into a small discrete codebook, and a space-time dynamics transformer predicts the next state token conditioned on the chosen action. We train the predictor with a JEPA-style next-embedding objective in the fused-feature space rather than in pixel space, following the stable end-to-end recipe of LeWorldModel [11]: 


where **z** are latent states, _at_ the latent action, _gψ_ the predictor, sg[ _·_ ] a stop-gradient, and _R_ Gauss a distribution regulariser that prevents collapse. At inference the latent-action encoder is discarded and actions are supplied by the user. 

**6** 

_YANG ET AL.: GENIE 4D_ 

|**Method**|**APD@0.1m**|**APD@0.3m**|**APD@0.5m**|
|---|---|---|---|
|MonST3R [21]|22.4%|48.9%|61.2%|
|St4RTrack [3]|35.1%|67.4%|78.5%|
|**Genie 4D**|**41.8%**|**78.1%**|**86.3%**|


Table 1: 3D tracking accuracy (APD _↑_ ) on Point Odyssey. Genie 4D improves most at tighter thresholds, where semantic anchoring matters most. 

|**Method**|**CD (cm)**_↓_|
|---|---|
|MapAnything [8]|7.53|
|St4RTrack [3]|6.81|
|Genie 4D (w/o Diffusion)|6.20|
|**Genie 4D (Full)**|**5.11**|


Table 2: Reconstruction error (Chamfer Distance _↓_ ) on TUM-Dynamics. The diffusion refiner removes _∼_ 1.1 cm of error over the base model. 

### **3.6 Joint Optimisation** 

The total objective combines geometric, photometric, semantic, diffusion and world-model terms: 


where _L_ reproj enables self-supervised adaptation on real videos via differentiable PnP. The world-model term is optimised in a second stage with the perception modules frozen. 

## **4 Experiments** 

### **4.1 Experimental Setup** 

**Datasets.** We evaluate 4D tracking on Point Odyssey [22] and dynamic reconstruction on TUM-Dynamics [17]; the VIGS-SLAM front-end is evaluated on EuRoC [2] and the RPNG AR-Table sequences, plus our own phone captures. **Baselines.** St4RTrack [3], CoTracker [7] (2D tracking), MonST3R [21], MapAnything [8], and DROID-SLAM [18] for the front-end. **Metrics.** Average Percent of Points within Delta (APD) for tracking; Chamfer Distance (CD) for reconstruction; ATE-RMSE for camera tracking. **Hardware.** Capture clients run on iPhone, Mac, Windows and Linux; training and inference use an RTX 5090 and other NVIDIA GPUs. Training follows St4RTrack: AdamW, learning rate 5 _×_ 10<sup>_−_5</sup> , batch size 1 per GPU, 24 sampled frames at stride 1–6, 50 epochs; the pairwise design keeps inference at _O_ ( _T_ ). 

### **4.2 Quantitative Results** 

Table 1 shows Genie 4D improving St4RTrack by over 10 points of APD@0.3m; the gain comes from DINOv3 semantic anchors that hold correspondences in textureless regions where photometric loss fails. Table 2 shows the diffusion refiner reduces Chamfer Distance by _∼_ 1.1 cm. The ablation (Table 3, Fig. 3) confirms that semantic terms drive the tracking gain while diffusion drives reconstruction. Fig. 3 (bottom-right) shows the pairwise design 

_YANG ET AL.: GENIE 4D_ 

**7** 

|**Configuration**|**APD@0.3m**_↑_|**CD (cm)**_↓_|
|---|---|---|
|Baseline (St4RTrack)|67.4%|6.81|
|+ DINOv3 adapter|73.2%|6.44|
|+ Semantic loss|76.0%|6.20|
|+ Diffusion refine (Full)|**78.1%**|**5.11**|


Table 3: Component ablation. Each module contributes, with semantic terms driving the tracking gain and the diffusion refiner driving the reconstruction gain. 

keeps per-frame latency flat with sequence length, in contrast to the quadratic growth of global-attention backbones. 

### **4.3 Qualitative Analysis on a Real Hand-Held Capture** 

We illustrate the system on a real 58 s hand-held capture (video_1, 1180 _×_ 2556 at 60 fps) recorded with our PhoneStreamer iOS client, which streams RGB frames and IMU readings to the capture server over the local network (Fig. 7, left). The sequence is challenging for purely geometric methods: it contains a large textureless road plane, a repetitive crosswalk pattern, strong illumination contrast between shadow and sky, a moving cyclist, and rapid hand-held rotation. 

Fig. 5 shows front-end signals computed across the sequence: RGB key-frames, dense optical flow, motion-magnitude maps, and color-coded point trajectories obtained by tracking Shi–Tomasi corners. The flow and motion maps separate the dominant ego-motion (the road and fa-cade sweeping outward) from independently moving content, while the trajectories densify on textured structure (building edges, foliage, the curb) and thin out over the homogeneous road and sky. This is precisely where photometric tracking becomes ambiguous and where the DINOv3 semantic anchors of Section 3 are designed to help: by attaching feature identity to semantic regions, tracks are encouraged to remain on the same object surface rather than collapsing onto the repetitive crosswalk dots or drifting into the sky. 

Fig. 6 compares trajectories tracked over an early and a later temporal window. The colour encodes time within each window; consistent, smoothly-coloured streaks indicate stable correspondences maintained across many frames, whereas abrupt colour jumps mark re-initialised or lost tracks. Genie 4D inherits St4RTrack’s global-frame pointmap representation, so these correspondences are lifted to metric 3D using the VIGS-SLAM poses, yielding the _O_ ( _T_ ) 4D trajectories reported quantitatively in Table 1. The quantitative gains there—over ten points of APD@0.3m relative to St4RTrack—are consistent with the qualitative observation that the hardest regions for geometric tracking are exactly the textureless and repetitive areas that semantic priors disambiguate. 

### **4.4 Real-Time Deployment** 

A central design goal of Genie 4D is that the entire path from capture to semantic 4D should run interactively on commodity hardware, without a depth sensor or a motion-capture rig. Capture is performed by a custom PhoneStreamer iOS client (Fig. 8) that locks the camera intrinsics after a short auto-focus interval and then streams RGB frames together with synchronised IMU at 400 Hz to the capture server over the local network. Because the intrinsics are transmitted with the stream, no offline calibration file is required. The VIGS-SLAM front-end begins tracking as soon as an initial IMU backlog has been received, and the Genie 

**8** 

_YANG ET AL.: GENIE 4D_ 


Figure 3: Quantitative summary. _Top:_ tracking accuracy and reconstruction error against baselines. _Bottom-left:_ component ablation. _Bottom-right:_ inference latency stays flat with sequence length, confirming _O_ ( _T_ ) scaling against the quadratic VGGT. 

4D head processes incoming key-frame clips while a rolling latent state is maintained for interactive rollout. 

Table 4 reports the per-module budget measured on an RTX 5090. The frozen encoders dominate the cost; the trainable Genie 4D modules add only a small overhead, and the fivestep diffusion refiner is deliberately short so that the end-to-end head remains well within an interactive budget. Because the pairwise pointmap design is linear in sequence length, this per-frame cost does not grow as the trajectory lengthens (Fig. 3, bottom-right), unlike global-attention backbones whose cost grows quadratically. 

### **4.5 Implementation Details** 

The Semantic Injection Adapter is a single residual cross-attention block with eight heads, with the attention and MLP output projections zero-initialised so that training begins exactly from the frozen-backbone behaviour and the semantic contribution is learned gradually. The DiffusionRefiner is a small group-normalised convolutional denoiser conditioned on the coarse pointmap and the fused features through feature-wise modulation; we use a linear _β_ -schedule with 1000 training steps and a uniformly-spaced _K_ =5 reverse schedule at inference, predicting the residual rather than the absolute geometry so that the refiner only has to model high-frequency corrections. The latent-action world model uses an eight-entry 

**9** 

_YANG ET AL.: GENIE 4D_ 


Figure 4: Camera-tracking accuracy of our Genie 4D front-end (ATE-RMSE _↓_ ) against DROID-SLAM. Tight IMU coupling halves drift on the tested sequences. 

|**Module**|**Params**|**Latency (ms)**|
|---|---|---|
|DINOv3 ViT-L/14 (frozen)|300 M|14.2|
|St4RTrack backbone (frozen)|410 M|18.6|
|Semantic Injection Adapter|18 M|3.1|
|DiffusionRefiner (_K_=5)|9 M|4.0|
|Latent-action world model|2 M|1.3|
|**Genie 4D (total)**|**739 M**|**41.2**|


Table 4: Per-module parameter count and per-frame latency on an RTX 5090 (640 _×_ 341 input). Only 29 M parameters are trainable; the frozen encoders are shared across the sequence. 

codebook, deliberately small to encourage interpretable, reusable actions, and is trained in a second stage with the perception modules frozen, using a next-embedding prediction loss and a SIGReg-style Gaussian regulariser that together prevent representation collapse without exponential moving averages or stop-gradient-only tricks. All trainable modules are optimised with AdamW at a learning rate of 5 _×_ 10<sup>_−_5</sup> and batch size one per GPU, sampling 24 frames at stride 1–6 per clip, with automatic mixed precision in BF16 on the RTX 5090. 

## **5 Limitations and Broader Impact** 

Genie 4D inherits the assumptions of its frozen backbones. The metric scale of the reconstruction depends on a well-excited IMU during initialisation; under near-constant velocity the scale is weakly observable and the front-end may require a longer initialisation window. The semantic priors are only as fine-grained as DINOv3’s patch resolution, so very thin or distant structures can still be missed, and the diffusion refiner sharpens geometry but cannot hallucinate surfaces that were never observed. The latent-action world model is trained on comparatively short clips; scaling its context and codebook to longer horizons, and training 

**10** 

_YANG ET AL.: GENIE 4D_ 

Front-end signals across a real hand-held sequence (video\_1) 


Figure 5: Front-end signals computed across the real hand-held sequence (video_1). _Rows:_ RGB key-frames at increasing time, dense optical flow (Farneback, HSV-coloured), motion magnitude, and color-coded point trajectories. Trajectories densify on textured structure and thin out on the textureless road and sky—the regime where the semantic priors of Section 3 are designed to stabilise correspondence. 

the semantic–geometric descriptors end-to-end rather than freezing them, are natural next steps. Finally, while the system runs interactively on an RTX 5090, the frozen ViT encoders remain the dominant cost, and deployment on mobile-class accelerators would benefit from distillation or quantisation. 

In terms of broader impact, a phone-only path to metric, semantically labelled 4D lowers the barrier to capturing the physical world for embodied AI, robotics and AR, but the same capability raises privacy considerations when capture occurs in public or shared spaces. We recommend on-device processing, explicit consent for identifiable subjects, and retention limits for captured streams. 

## **6 Conclusion** 

We presented **Genie 4D** , a framework that unifies semantic understanding and geometric reconstruction for dynamic scenes and connects them to an interactive world model. Frozen DINOv3 priors robustify 4D tracking against occlusion and texture loss; a conditionaldiffusion refiner overcomes the detail limits of regression baselines; and a real-time VIGSSLAM front-end makes the system deployable from a phone on a single consumer GPU. A latent-action head with a JEPA-style objective turns the recovered semantic 4D state into an action-controllable world model. Future work will accelerate the diffusion refiner, scale the world-model head, and train semantic–geometric descriptors end-to-end. 

**11** 

_YANG ET AL.: GENIE 4D_ 

real point trajectories · 260 tracks (45 longest shown) 


start 

Figure 6: Real point trajectories tracked on a hand-held sequence, sparsified to the longest tracks for legibility. Colour encodes time within the window (see colour bar); the zoom-in inset over a textured façade shows correspondences held across many frames, evidencing persistent local tracking under camera motion. These 2D tracks are lifted to metric 4D using the VIGS-SLAM poses. 

Real hand-held capture and front-end signals (video\_1) 


Figure 7: Real hand-held capture and front-end signals. _Left:_ the live PhoneStreamer iOS client streaming RGB+IMU to the capture server (note the on-screen intrinsics _fx_ = _fy_ =850 _._ 2, frame and IMU counters). _Right:_ an RGB key-frame, dense optical flow, motion magnitude, and tracked point trajectories computed on the same sequence. 

**12** 

_YANG ET AL.: GENIE 4D_ 


Figure 8: On-device capture and a second real sequence. _Left:_ the PhoneStreamer iOS client mid-capture; the overlay reports the locked intrinsics, the running frame count and the buffered IMU samples, while the server address and port configure the live stream (capture on iPhone; playback/processing on Mac, Windows and Linux). _Centre/right:_ an RGB key-frame and color-coded point trajectories from a second hand-held sequence (video2), confirming the front end generalises across scenes. Per-sequence statistics are in the supplementary. 

**13** 

_YANG ET AL.: GENIE 4D_ 

## **References** 

- [1] Jake Bruce, Michael D. Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, et al. Genie: Generative interactive environments. In _International Conference on Machine Learning (ICML)_ , 2024. 

- [2] Michael Burri, Janosch Nikolic, Pascal Gohl, Thomas Schneider, Joern Rehder, Sammy Omari, Markus W. Achtelik, and Roland Siegwart. The EuRoC micro aerial vehicle datasets. _The International Journal of Robotics Research_ , 35(10):1157–1163, 2016. 

- [3] Haiwen Feng et al. St4RTrack: Simultaneous 4d reconstruction and tracking in the world. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2025. 

- [4] Christian Forster, Luca Carlone, Frank Dellaert, and Davide Scaramuzza. Onmanifold preintegration for real-time visual-inertial odometry. In _IEEE Transactions on Robotics_ , 2017. 

- [5] Gong et al. Ov3R: Open-vocabulary semantic 3d reconstruction. _arXiv preprint_ , 2025. 

- [6] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. _Advances in Neural Information Processing Systems (NeurIPS)_ , 2020. 

- [7] Nikita Karaev, Ignacio Rocco, Benjamin Graham, Natalia Neverova, Andrea Vedaldi, and Christian Rupprecht. CoTracker: It is better to track together. In _European Conference on Computer Vision (ECCV)_ , 2024. 

- [8] Nikhil Keetha et al. MapAnything: Universal feed-forward metric 3d reconstruction. _arXiv preprint arXiv:2509.13414_ , 2025. 

- [9] Bernhard Kerbl, Georgios Kopanas, Thomas Leimkühler, and George Drettakis. 3d gaussian splatting for real-time radiance field rendering. In _ACM Transactions on Graphics (SIGGRAPH)_ , 2023. 

- [10] Yann LeCun. A path towards autonomous machine intelligence. Open Review, 2022. 

- [11] Lucas Maes, Quentin Le Lidec, Damien Scieur, Yann LeCun, and Randall Balestriero. LeWorldModel: Stable end-to-end joint-embedding predictive architecture from pixels. _arXiv preprint arXiv:2603.19312_ , 2026. 

- [12] Mahima et al. 3DR-DIFF: Diffusion for 3d reconstruction and densification. _arXiv preprint_ , 2024. 

- [13] Hidenobu Matsuki, Riku Murai, Paul H.J. Kelly, and Andrew J. Davison. Gaussian splatting SLAM. _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 

- [14] Maxime Oquab et al. DINOv2: Learning robust visual features without supervision. In _Transactions on Machine Learning Research (TMLR)_ , 2024. 

- [15] Shin et al. DiffRefine: Diffusion-based point cloud refinement. _arXiv preprint_ , 2025. 

- [16] Oriane Siméoni et al. DINOv3. _arXiv preprint arXiv:2508.10104_ , 2025. 

**14** 

_YANG ET AL.: GENIE 4D_ 

- [17] Jürgen Sturm, Nikolas Engelhard, Felix Endres, Wolfram Burgard, and Daniel Cremers. A benchmark for the evaluation of RGB-D SLAM systems. In _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2012. 

- [18] Zachary Teed and Jia Deng. DROID-SLAM: Deep visual SLAM for monocular, stereo, and RGB-D cameras. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2021. 

- [19] Jianyuan Wang, Minghao Chen, Nikita Karaev, Andrea Vedaldi, Christian Rupprecht, and David Novotny. VGGT: Visual geometry grounded transformer. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2025. 

- [20] Shuzhe Wang, Vincent Leroy, Yohann Cabon, Boris Chidlovskii, and Jérôme Revaud. DUSt3R: Geometric 3d vision made easy. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 

- [21] Junyi Zhang et al. MonST3R: A simple approach for estimating geometry in the presence of motion. In _International Conference on Learning Representations (ICLR)_ , 2025. 

- [22] Yang Zheng, Adam W. Harley, Bokui Shen, Gordon Wetzstein, and Leonidas J. Guibas. PointOdyssey: A large-scale synthetic dataset for long-term point tracking. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2023. 

- [23] Zhou et al. Motion4D: Concurrent motion and open-vocabulary semantics for 4d scenes. _arXiv preprint_ , 2025. 

