---
title: "V-JEPA Hand: Simple, Accurate and Fast 3D Hand and Camera Trajectory Recovery from Egocentric Videos"
date: "2026-10-19"
authors: "Ruicheng Li; Qixiu Li; Yu Deng; Sicheng Xu; Jiaolong Yang; Baining Guo"
url: https://arxiv.org/abs/2610.26780
pdf: https://arxiv.org/pdf/2610.26780
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2610.26780)** / [論文ページ](https://arxiv.org/abs/2610.26780)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

V-JEPA HAND: SIMPLE, ACCURATE AND FAST 3D HAND AND CAMERA TRAJECTORY RECOVERY FROM EGOCENTRIC VIDEOS 

**Ruicheng Li**<sup>1</sup><sup>_,∗_</sup> **Qixiu Li**<sup>1</sup><sup>_,∗_</sup> **Yu Deng**<sup>2</sup> **Sicheng Xu**<sup>2</sup> **Jiaolong Yang**<sup>2</sup> **Baining Guo**<sup>2</sup> 1Tsinghua University 2Microsoft Research 


Figure 1: **V-JEPA Hand: joint hand and camera trajectory recovery from egocentric video. Top left and centre:** From a video clip, V-JEPA Hand jointly recovers bilateral 3D hand motion and camera motion in a single forward pass. Blue, orange and teal denote the left hand, right hand and camera, respectively; colour intensity indicates time. **Top right:** ARCTIC detection and coverage-aware reconstruction results across eight metrics, normalized to our result (100%); larger is better. **Bottom:** Qualitative comparisons with HaMeR, WiLoR and WildHands, illustrating differences in hand pose accuracy, missed hands and spurious predictions. 

# ABSTRACT 

Egocentric video supports diverse applications, including robot learning, augmented reality, and human activity understanding. Recovering metric 3D hand trajectories from such video requires estimating both hand motion and camera egomotion to express the hands in a consistent reference frame. Many existing pipelines recover hand and camera motion in separate stages, combining hand detection, hand reconstruction, camera tracking, and trajectory refinement. We present V-JEPA Hand, a simple feed-forward video model that jointly reconstructs bilateral hand motion and camera motion from egocentric clips. It uses 

*Intern at Microsoft Research. 

1 

a self-supervised V-JEPA 2.1 encoder to extract spatio-temporal features from full-frame video and a query-based predictor to decode these features into perframe hand poses, hand presence, and camera motion. We use the predicted camera motion to express the hand trajectories in a common world frame. The model accepts known focal lengths or predicts them when unavailable. It reconstructs each clip in a single forward pass. We train both components end to end in a single stage on a mixture of diverse pseudo-labelled videos and highprecision 3D annotations. A single model achieves the lowest coverage-aware mean per-joint position error (MPJPE) among comparable baselines on ARCTIC, HOT3D, and EgoStandard. It also yields lower world-frame trajectory errors than the compared SLAM-based pipelines. Ablations support the benefits of video pretraining, temporal context, and mixed supervision. V-JEPA Hand achieves a forward-pass throughput of 93 _._ 4 FPS on a single RTX A6000. Project page: https://qft-333.github.io/V-JEPA-Hand-Page/. 

# 1 INTRODUCTION 

Egocentric video provides a natural record of human manipulation and supports a wide range of applications. Recent VLA approaches use 3D hand motion from egocentric demonstrations for pretraining and robot-policy adaptation (Kareer et al., 2025a;b; Luo et al., 2025; Yang et al., 2025; Bi et al., 2026; Zheng et al., 2026; Li et al., 2025). 

Hand motion recovery also supports AR/VR interaction (Han et al., 2022), first-person activity understanding (Kwon et al., 2021), animation and digital humans (Romero et al., 2017), and wristkinematics assessment (Smeragliuolo et al., 2016). These applications benefit from accurate, temporally coherent 3D hand motion. Apparent hand motion in egocentric video can result from movement of the hand, the camera, or both. Recovering metric hand trajectories in a consistent reference frame therefore requires estimating both hands’ positions, orientations, finger articulation, and presence, together with camera motion. 

Single-image models such as HaMeR and WiLoR (Pavlakos et al., 2024; Potamias et al., 2025) reconstruct hands from detected crops. Applied frame by frame, they cannot use neighboring frames to improve reconstruction under occlusion, motion blur, or intermittent visibility. Temporal methods add cross-frame modeling (Zhang et al., 2024), while world-frame approaches combine hand reconstruction with camera tracking, motion infilling, or optimization (Zhang et al., 2025; Chen et al., 2025). More recently, ViDiHand (Wang et al., 2026) uses pretrained video diffusion features for detector-free, full-frame hand reconstruction. Video provides temporal cues for hand reconstruction and scene context for camera motion. We further investigate _how effectively a self-supervised video encoder can support joint hand–camera recovery through end-to-end, single-stage adaptation_ . 

Our central finding is that _a simple video encoder–predictor architecture can achieve accurate and fast joint hand–camera reconstruction_ . We instantiate this design as V-JEPA Hand, pairing the self-supervised V-JEPA 2.1 encoder (Mur-Labadia et al., 2026) with a query-based predictor and fine-tuning both end to end. Cross-frame information is incorporated within the visual encoder, and hand and camera states are decoded from the same spatio-temporal features. The predictor jointly estimates per-frame bilateral hand poses, hand presence, and camera motion; it also accepts known clip-level focal lengths or predicts them when unavailable. The entire clip is reconstructed in one forward pass without a separate hand detector, hand crops, SLAM, or test time optimization. The model thus retains a simple feedforward structure rather than assembling estimates from independent hand and camera systems. 

Training such a model requires accurate 3D annotations across diverse capture conditions. ARCTIC (Fan et al., 2023) and HOT3D (Banerjee et al., 2024) provide high-quality hand-motion annotations using dedicated motion-capture systems, while H2O (Kwon et al., 2021) uses calibrated multi-view RGB-D recordings to annotate bimanual interactions. These resources provide valuable geometric supervision, but their hardware and calibration requirements make collection costly to extend across everyday environments. In contrast, Ego4D (Grauman et al., 2022) and EPICKITCHENS (Damen et al., 2018) capture diverse, unscripted activities without dense metric handmotion labels. Reconstruction offers a complementary source of supervision: HaWoR (Zhang et al., 2025) recovers world-space hand trajectories, while the VITRA annotation pipeline (Li et al., 2025) 

2 

combines hand reconstruction with metric camera tracking to generate frame-aligned hand-action labels at scale. Such automatically recovered trajectories are useful but imperfect pseudo-labels. We therefore train in a single stage on pseudo-labelled Ego4D and our in-house recordings, mixed with a comparatively small pool of precisely annotated videos from ARCTIC and HOT3D. The pseudo-labelled videos broaden scene and action coverage, while the high-quality annotations provide reliable geometric supervision for transfer beyond the capture environments. 

We evaluate the same trained model on ARCTIC (Fan et al., 2023), HOT3D (Banerjee et al., 2024), and EgoStandard (Lightwheel AI, 2025), whose commercial annotation pipeline combines hardware-assisted capture with multi-stage optimization. EgoStandard is excluded from our reconstruction training. Across all three benchmarks, V-JEPA Hand combines high hand-detection coverage with the lowest coverage-aware MPJPE among the previous baselines. It also yields lower world-frame trajectory errors than the compared SLAM-based pipelines. Data ablations show that mixed supervision improves reconstruction on unseen videos, while component ablations support the value of pretrained features and temporal context. V-JEPA Hand achieves forward-pass throughput of 93 _._ 4 FPS on a single RTX A6000. 

We summarize our contributions as follows: 

- A simple yet effective feed-forward framework that jointly recovers bilateral 3D hand motion, hand presence, camera egomotion, and clip-level focal lengths from a shared video representation, without separate hand detection, SLAM, or test-time optimization. 

- A single-stage training recipe combining diverse pseudo-labelled egocentric video with highprecision annotations, with demonstrated benefits for reconstruction on unseen data. 

- A systematic evaluation of detection coverage, hand pose, world-frame trajectories, crossdomain generalization, and inference efficiency, together with ablations of key training and modeling choices. 

# 2 RELATED WORK 

**Monocular 3D hand reconstruction.** Estimating 3D hand pose and shape from monocular images has advanced rapidly with parametric models such as MANO (Romero et al., 2017). Most existing methods detect then regress, cropping each hand with a 2D detector before predicting mesh or kinematic parameters (Pavlakos et al., 2024; Potamias et al., 2025; Dong et al., 2024; Chen et al., 2022; Moon, 2023; Park et al., 2022). In egocentric videos, however, this pipeline struggles with frequent occlusions, motion blur, and boundary truncations, while discarding global context and inter-hand spatial relations. To bypass cropping, detector-free alternatives directly regress hand poses from full frames (Prakash et al., 2024) or leverage video diffusion features (Wang et al., 2026), though diffusion models incur substantial computational overhead. In contrast, V-JEPA Hand recovers both hands and their presence probabilities in a single forward pass via a lightweight query-based decoder, avoiding separate detectors, crops, or iterative diffusion. 

**Temporal and world-coordinate hand motion recovery.** Applying single-frame estimators independently across video frames yields temporally jittery trajectories. While temporal networks and transformers help smooth camera-relative predictions (Yang et al., 2020; Zhang et al., 2024), they do not resolve camera egomotion. To express manipulation in a consistent world frame, current methods decouple hand estimation from camera tracking by combining per-frame regressors, external visual SLAM such as DROID-SLAM (Teed & Deng, 2021), and motion infilling or test-time trajectory optimization (Zhang et al., 2025; Chen et al., 2025; Fan et al., 2024), mirroring pipelines in world-grounded body capture (Ye et al., 2023; Shin et al., 2024). However, SLAM frequently drifts under aggressive head motion, and multi-stage optimization introduces latency and cascading errors. Instead, V-JEPA Hand unifies camera-space bilateral hand motion, hand presence, camera egomotion, and camera intrinsics into a single feedforward prediction, avoiding external SLAM or test-time optimization while achieving superior world-frame accuracy. 

**Self-supervised video representations and foundation models.** Self-supervised video pretraining provides powerful motion and scene priors. While masked autoencoders such as MAE (He et al., 2022), VideoMAE (Tong et al., 2022), and VideoMAE V2 (Wang et al., 2023) reconstruct 

3 


Figure 2: **Overview of V-JEPA Hand.** A V-JEPA 2.1 encoder extracts spatio-temporal features from an egocentric video clip. A ViT predictor jointly processes these features, one learnable handpose query per frame, and an intrinsics token. The output queries predict bilateral MANO pose, hand presence probability, and camera motion. The entire clip is reconstructed in a single forward pass; blue and orange meshes denote the reconstructed left and right hands, respectively. 

masked pixels, pixel-level objectives often overemphasize high-frequency texture details over geometric and physical dynamics. The Joint-Embedding Predictive Architecture (JEPA) family (Assran et al., 2023; Bardes et al., 2024; Assran et al., 2025; Mur-Labadia et al., 2026) addresses this by predicting representations in latent space; notably, V-JEPA 2.1 (Mur-Labadia et al., 2026) learns rich spatio-temporal features and dense motion priors. Although generative video foundation models (Blattmann et al., 2023) also encode temporal priors (Wang et al., 2026), their generative nature requires heavy computation. In comparison, V-JEPA 2.1 offers a discriminative representation that supports high-throughput (91 _._ 3 FPS) inference and outperforms VideoMAE, DINOv3 (Siméoni et al., 2025), and Perception Encoder (Bolya et al., 2025) on both camera- and world-frame metrics. 

# 3 METHOD 

As illustrated in Figure 2, V-JEPA Hand reads a raw video clip and emits, in a single forward pass, the complete bilateral hand trajectory of that clip together with the camera motion and focal lengths. The model has two components: a self-supervised video encoder that turns the clip into a spatiotemporal token grid (Section 3.2), and a query-based trajectory predictor that decodes one output token per frame into the per-frame state defined below. Section 3.3 describes our single-stage training with multi-source supervision, combining large-scale pseudo-labelled video with high-quality data under a shared training objective. 

## 3.1 PROBLEM FORMULATION 

The input is a clip of _T_ RGB frames **V** = ( **I** 1 _, . . . ,_ **I** _T_ ), **I** _t ∈_ R<sup>3</sup><sup>_×H×W_</sup> , recorded by a freely moving egocentric camera. Here _t ∈{_ 1 _, . . . , T }_ indexes frames, and _H_ and _W_ are the image height and width in pixels, respectively. We write _Ct_ for the camera coordinate frame of frame _t_ and index the two hands by _s ∈{_ L _,_ R _}_ , where L and R denote the camera wearer’s left and right hand. Hats denote model predictions. 

**Model output.** The model returns a per-frame hand–camera trajectory together with clip-level camera focal lengths, 


4 

where **Y**<sup>ˆ</sup> stacks the per-frame state vectors **y** ˆ _t_ . Each **x** ˆ<sup>_s_</sup> _t_<sup>_∈_R55is the state of hand</sup><sup>_s_, ˆ</sup><sup>**g**</sup><sup>_t∈_R9is the</sup> camera motion at frame _t_ , and **k**<sup>ˆ</sup> estimates the clip-level focal-length vector **k** = ( _fx, fy_ ), where _fx_ and _fy_ are the horizontal and vertical focal lengths in pixels at the input resolution. Our notation retains only these two varying intrinsic parameters. The per-frame states are decoded from the _T_ query tokens, one row **y** ˆ _t_ per token. The model accepts known focal lengths or predicts them from a dedicated token when unavailable (Section 3.2). The hand and camera motion states are defined next. 

**Hand state.** For frame _t_ and hand _s_ the model predicts 


whose four blocks are: the wrist translation **d**<sup>ˆ</sup><sup>_s_</sup> _t_<sup>_∈_R3,i.e.thepositionofthehandrootinmeters</sup> expressed in _Ct_ ; the wrist orientation ˆ **r**<sup>_s_</sup> _t_<sup>_∈_R6,apredictionofthefirsttworowsoftherotation</sup> matrix **R**<sup>_s_</sup> _t_<sup>_∈_R3</sup><sup>_×_3 that maps the canonical MANO hand frame to</sup><sup>_Ct_; the articulation</sup><sup>**_θ_**ˆ</sup> _t_<sup>_s∈_R45, the</sup> Euler angles of the 15 MANO finger joints, each relative to its parent joint; and the presence score _c_ ˆ<sup>_s_</sup> _t_<sup>_∈_R,alogitthatishighwhenhand</sup><sup>_s_isactuallyinframe</sup><sup>_t_.Thetwohandstogethertherefore</sup> account for the 110 **hand dimensions** of **y** ˆ _t_ . We do not predict the MANO shape coefficient vector **_β_** , and all hands are evaluated at the neutral shape **_β_** = **0** . 

**Camera state.** The camera state encodes the rigid transform **T** _t→_ 1 _∈ SE_ (3) from the current camera frame _Ct_ to the first-frame anchor _C_ 1, where _SE_ (3) is the group of 3D rigid transformations: 


where the superscript cam distinguishes camera rotation from hand rotation. The vector ˆ **r**<sup>cam</sup> _t ∈_ R<sup>6</sup> predicts the first two rows of the camera rotation matrix **R**<sup>cam</sup> _t ∈_ R<sup>3</sup><sup>_×_3</sup> , which maps vectors from _Ct_ to _C_ 1. The vector **a** _t ∈_ R<sup>3</sup> is the translation component of **T** _t→_ 1, expressed in _C_ 1 in metres. We represent this translation by its signed-log encoding **u** _t ∈_ R<sup>3</sup> , and **u** ˆ _t_ is the model’s prediction of that encoding, rather than the translation in metres. Here sgn is the sign function, _⊙_ denotes element-wise multiplication, and the absolute value and natural logarithm are also applied elementwise. 

## 3.2 ARCHITECTURE 

**Video encoder.** We initialize the video encoder with self-supervised pretrained V-JEPA 2.1 ViT-L weights (Mur-Labadia et al., 2026) and jointly optimize all encoder and predictor parameters on the mixed training data. The encoder cuts the video clip into non-overlapping space–time patches, each spanning 2 consecutive frames and a 16 _×_ 16 pixel square, and embeds every patch into one token of dimension _d_ , so the clip becomes a sequence 


Here **Z** is the encoder token sequence, _N_ is the number of space–time patches, and _d_ is the token feature dimension. Each token is located by a rotary encoding of its ( _τ, h, w_ ) patch coordinate, where _τ_ , _h_ , and _w_ index the temporal, vertical, and horizontal positions in the patch grid, respectively. 

**Query-based trajectory predictor.** The predictor is a ViT that operates on the concatenation of the encoder grid, _T_ learnable _query tokens_ **Q** _∈_ R<sup>_T ×d_</sup> , one per output frame, and a single intrinsics token **q** _k ∈_ R<sup>_d_</sup> , whose subscript _k_ denotes its association with camera intrinsics, under joint selfattention: 


Here [ _·_ ; _·_ ] denotes concatenation along the token dimension, and ViT is the predictor’s vision transformer. Tildes denote the corresponding output tokens: **q** ˜ _k ∈_ R<sup>_d_</sup> for intrinsics, **Z**<sup>˜</sup> _∈_ R<sup>_N×d_</sup> for the video features, and **Q**<sup>˜</sup> _∈_ R<sup>_T ×d_</sup> for the per-frame queries. Each query is temporally aligned with its corresponding video frame through rotary positional encoding. A shared MLP maps each output query to the 119-dimensional hand–camera state for that frame. During training, the intrinsics token is set to an embedding of the ground-truth intrinsics with probability 0 _._ 5 and a learned token otherwise. A linear head reads the output token **q** ˜ _k_ to predict **k**<sup>ˆ</sup> , the two focal-length components, with supervision applied only to clips whose intrinsics were withheld. 

5 

## 3.3 TRAINING 

**Single-stage multi-dataset training.** We train V-JEPA Hand end to end in a single stage using four datasets: Ego4D (Grauman et al., 2022), our in-house egocentric recordings, ARCTIC (Fan et al., 2023), and HOT3D (Banerjee et al., 2024). We process Ego4D and our in-house recordings with the VITRA annotation pipeline (Li et al., 2025) to obtain a large-scale pool of pseudo-labelled video spanning diverse scenes, activities, and camera wearers. We mix this noisy pseudo-labelled data with high-quality data from the training splits of ARCTIC and HOT3D. Throughout training, each clip is sampled from the pseudo-labelled pool, ARCTIC, or HOT3D with probabilities 0 _._ 35, 0 _._ 45, and 0 _._ 20, respectively. 

**Training objective.** We supervise hand parameters, 3D joint positions, 2D projections, temporal smoothness, hand presence, and camera estimates with the total training loss 


Each _λ_ coefficient is a nonnegative scalar weight for the loss term with the same subscript. The terms _Ld_ , _Lr_ , and _Lθ_ supervise wrist position, wrist orientation, and finger articulation, respectively. _Lj_ penalizes errors in the 21 camera-space 3D joints obtained through differentiable MANO forward kinematics, while _Lπ_ penalizes errors in their image-plane projections. _La_ penalizes the acceleration of the predicted 3D joints across consecutive frames, which suppresses jitter without penalizing smooth motion. _Lc_ supervises whether each hand is present in each frame. _Lg_ supervises camera rotation and signed-log translation relative to the first frame, and _Lk_ supervises clip-level focal lengths when they are withheld from the input; auxiliary implementation details are given in Appendix D. 

# 4 EXPERIMENTS 

We evaluate V-JEPA Hand on egocentric two-hand reconstruction. We first describe the datasets and evaluation protocol (Section 4.1), then compare with prior work (Section 4.2). Our ablations test the training data, the loss terms, encoder pretraining and temporal context, and encoder choice (Section 4.3). We also report model size and inference cost (Section 4.4), and show qualitative results (Section 4.5). 

## 4.1 EXPERIMENTAL SETUP 

**Datasets.** We evaluate on three egocentric hand benchmarks: **ARCTIC** tests reconstruction under severe occlusion during two-hand object manipulation, while **HOT3D** tests robustness to motion blur from rapid head and hand movements. We additionally evaluate on **EgoStandard** , a commercially annotated egocentric dataset spanning diverse scenes. Its 3D motion annotations are produced by a pipeline that combines hardware-assisted capture with multi-stage optimization. We exclude EgoStandard entirely from training and use it to assess generalization to unseen egocentric data. The EgoStandard evaluation covers approximately 60 minutes of video. For HOT3D, we follow the HaWoR validation split, covering approximately 49 minutes of video. Table 2 uses the same evaluation splits, with all world methods rescored on their common true-positive support. **Metrics.** Metrics follow the coverage-aware evaluation implementation of Wang et al. (2026), which accounts for missed hands. Metric conventions and table abbreviations are provided in Appendix F; evaluation protocols are detailed in Appendix E. 

## 4.2 COMPARISON WITH PRIOR WORK 

Table 1 compares V-JEPA Hand with WiLoR (Potamias et al., 2025), HaMeR (Pavlakos et al., 2024), WildHands (Prakash et al., 2024), and HaWoR (Zhang et al., 2025) on all three datasets. All five methods are evaluated on the same splits, and V-JEPA Hand uses the same checkpoint across all three datasets. We also include published ViDiHand (Wang et al., 2026) results: its ARCTIC scores are directly comparable, while its HOT3D scores use a different split and serve only as a reference. 

6 

Table 1: **Comparison with prior work.** WiLoR, HaMeR, and WildHands are single-frame methods; HaWoR, ViDiHand, and ours are multi-frame methods. We follow ViDiHand’s evaluation protocol, except that pose metrics without the -p suffix are computed on each method’s own intersection of predictions and ground truth (true positives). ViDiHand results are taken from its paper (Wang et al., 2026); its HOT3D row (gray) uses a different split and is shown for reference only, without direct comparison or ranking. 

||Detection||3D P|ose|||Or|ient. &|Positi|on||Temporal|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Method|Acc_↑_Rec_↑_F1_↑_|MP-p_↓_|MP_↓_|PA-p_↓_|PA_↓_|EP-p_↓_|EP_↓_|GO-p_↓_|GO_↓_|CT-p_↓_|CT_↓_|Jit_↓_|
|_ARCTIC_|||||||||||||
|WiLoR|0.909<br>0.949<br>0.971|21.11|15.52|12.74|6.70|65.56|28.84|17.68|**11.74**|0.077|0.050|25.97|
|HaMeR|0.873 0.943<br>0.958|30.78|25.10|16.02|9.44|64.85|28.45|25.14|18.67|0.093|0.063|14.78|
|WildHands|0.874<br>0.944<br>0.958|27.07|21.29|15.99|9.55|65.44|29.58|22.54|16.05|0.070|0.039|12.28|
|HaWoR|0.853<br>0.953 0.945|31.52|26.94|14.48|9.07|44.32|16.24|24.38|18.82|0.076|0.050|19.37|
|ViDiHand|**0.997**<br>**0.999**<br>**0.999**|21.67|-|9.82|-|12.41|-|14.64|-|0.047|-|**3.18**|
|Ours|0.996<br>0.998<br>**0.999**|**15.59**|**15.36**|**6.84**|**6.59**|**8.99**|**8.85**|**12.46**|12.18|**0.032**|**0.031**|6.09|
|_HOT3D_|||||||||||||
|WiLoR|0.810<br>0.879<br>0.922|39.38|26.09|23.10|7.57|79.90|22.11|32.51|16.49|0.103|0.048|17.19|
|HaMeR|0.719<br>0.880<br>0.886|67.09|57.96|25.09|10.26|70.66|15.40|50.01|36.35|0.106|0.055|21.09|
|WildHands|0.425 0.600 0.609|80.23|42.99|61.89|12.40|275.39|37.14|84.35|38.82|0.250|0.076|25.30|
|HaWoR|0.733<br>0.895<br>0.875|28.79|16.71|20.68|7.64|66.60|8.16|25.01|10.50|0.086|0.039|13.41|
|ViDiHand|0.948 0.974 0.983|21.51|-|11.38|-|14.95|-|15.83|-|0.040|-|3.74|
|Ours|**0.971**<br>**0.979**<br>**0.980**|**14.42**|**12.04**|**8.24**|**5.72**|**16.81**|**5.71**|**9.90**|**6.52**|**0.026**|**0.014**|**5.74**|
|_EgoStanda_|_rd_||||||||||||
|WiLoR|0.949<br>0.971<br>0.982|35.19|32.16|11.11|7.35|37.09|12.74|25.88|22.13|0.089|0.080|15.53|
|HaMeR|0.986<br>0.992<br>0.994|37.37|36.60|8.27|**7.26**|18.06|11.45|26.37|25.37|0.093|0.090|18.35|
|WildHands|0.514 0.658 0.659|69.22|33.83|55.04|12.29|325.25|53.66|74.03|31.84|0.214|0.099|20.10|
|HaWoR|0.883<br>0.901<br>0.937|33.38|23.36|20.11|8.62|91.58|8.00|26.58|12.81|0.089|0.058|13.95|
|Ours|**0.990**<br>**0.995**<br>**0.997**|**16.97**|**16.30**|**8.01**|7.29|**11.10**|**6.51**|**10.60**|**9.84**|**0.045**|**0.043**|**4.88**|


Table 2: **World-coordinate reconstruction.** All methods are evaluated on the same hand-frames, using the intersection of true positives across the four compared methods. W-MPJPE and WAMPJPE are in mm; RTE is in %. Lower is better. 

|||ARCTIC|||HOT3D||E|goStandard||
|---|---|---|---|---|---|---|---|---|---|
|Method|W-MP_↓_|WA-MP_↓_|RTE_↓_|W-MP_↓_|WA-MP_↓_|RTE_↓_|W-MP_↓_|WA-MP_↓_|RTE_↓_|
|WiLoR+SLAM|63.36|34.13|29.78|74.78|28.42|40.21|90.67|41.54|26.27|
|HaMeR+SLAM|69.05|33.78|28.21|105.10|35.08|47.31|94.86|42.74|27.16|
|HaWoR|106.05|55.38|48.92|63.08|27.60|51.02|90.23|45.02|35.93|
|Ours|**35.86**|**19.72**|**17.58**|**34.08**|**16.18**|**28.15**|**66.35**|**32.91**|**22.37**|


**From occlusion and blur to unseen scenes.** Table 1 shows that V-JEPA Hand outperforms prior methods on the vast majority of comparable metrics across all three benchmarks. The improvements span hand detection, 3D pose, and camera-space placement. On ARCTIC, this translates into accurate hand recovery despite severe occlusion. Crucially, the advantage extends to EgoStandard’s diverse scenes without any training on that dataset: V-JEPA Hand leads in most metrics on expanded EgoStandard, including both coverage-aware and TP-only MPJPE. Together, these results show that a single video-based model supports both precise reconstruction on ARCTIC and HOT3D and transfer to unseen egocentric scenes. 

**World-frame reconstruction through unified prediction.** Table 2 shows that the simpler architecture also delivers competitive world-frame trajectories, where hand reconstruction must be combined with camera motion. V-JEPA Hand leads all three world-frame metrics on all three datasets. Because this comparison uses shared true-positive hand-frames, the gains reflect trajectory accuracy 

7 

rather than differences in detection coverage. Unlike the SLAM-based baselines, V-JEPA Hand predicts hand and camera motion together from the same video representation, eliminating the need to assemble their estimates from separate systems. The results therefore support unified prediction as an accurate alternative to a multi-stage SLAM-based reconstruction pipeline on these benchmarks. 

## 4.3 ABLATION STUDIES 

Ablations use different training setups from Table 1. For fair comparisons, we change only the component being tested and keep the remaining training settings the same in each ablation. See Appendix G for implementation details. 

**Effect of pseudo-labelled training data.** Table 3 compares training on all four datasets with training on an equal mixture of ARCTIC and HOT3D only, keeping the architecture, initialization, and training budget fixed. We evaluate both models on EgoStandard, which neither sees during training. Adding the pseudo-labelled Ego4D and in-house data helps the model place hands more accurately in these unseen videos: reprojection and translation errors fall, along with pose and world-trajectory errors. The benefit is not simply that the model detects more hands—detection accuracy and recall are slightly lower, while F1 is comparable. Instead, the broader training data improves the geometry of the reconstruction on a benchmark outside either model’s training set. 

**Loss ablation.** Table 4 removes either the jitter loss or the 2D reprojection loss while keeping the rest of training unchanged. Without the jitter loss, predictions vary more from frame to frame even though individual-frame pose accuracy changes little. This shows why accurate poses alone do not guarantee a smooth sequence. Without the reprojection loss, joint-position error improves slightly, but the hands line up less well with the image and their wrist positions become less accurate. The two terms therefore serve different purposes: one discourages temporal jumps, while the other keeps the reconstruction consistent with the image. 

**Pretraining and temporal context.** Table 5 changes one choice at a time: starting the encoder from random weights, freezing its pretrained weights, or replacing the video input with a single frame. The remaining training setup is shared. Training from scratch gives much less accurate poses and world trajectories on both benchmarks. Even a frozen pretrained encoder performs substantially better, and fine-tuning it improves the results further. Thus, pretraining provides useful features for hand reconstruction, while task-specific training helps the model make better use of them. Singleframe predictions remain reasonably accurate in each image, but are much less smooth over time. Seeing neighboring frames therefore helps not only with pose accuracy, but also with keeping successive predictions consistent. 

**Encoder ablation.** Table 6 compares four pretrained ViT-L encoders with the same predictor and fine-tuning recipe. V-JEPA 2.1 gives the most accurate hand poses and world trajectories, and the smoothest predictions, on both benchmarks. Video encoders outperform image encoders on world trajectories, even when the latter provide features from multiple frames. This suggests that video features help recover motion beyond simply combining per-frame image features. Differences in pretraining data and input settings are detailed in Appendix G.3. 

## 4.4 MODEL SIZE AND SPEED 

V-JEPA Hand has 607 _._ 1M parameters and jointly recovers hand and camera trajectories. Table 7 compares single-GPU forward throughput on the same 100 real-video clips at batch size one, excluding detection and postprocessing. Ours uses BF16; baselines use their released FP32 implementations. 

## 4.5 QUALITATIVE RESULTS 

Figure 4 in Appendix A shows challenging cases beyond controlled capture settings, including very low light and outdoor activities. V-JEPA Hand recovers hands that the baselines miss in the darkest example and produces plausible hand reconstructions in outdoor and cluttered scenes. These ex- 

8 

Table 3: **Training-data ablation.** To assess how pseudo-labelled training data affects generalization, we compare models trained with and without it on EgoStandard, a benchmark unseen by either model during training. 

||Detection||3D P|ose<br>O|rient. &|Positi|on<br>|Temporal|Worl|d Frame|
|---|---|---|---|---|---|---|---|---|---|---|
|Method|Acc_↑_Rec_↑_F1_↑_|MP-p_↓_|MP_↓_|PA-p_↓_PA_↓_EP-p_↓_EP_↓_|GO-p_↓_|GO_↓_|CT-p_↓_CT_↓_|Jit_↓_|W-MP_↓_|WA-MP_↓_|
|ARCTIC+HOT3D only|**0.996**<br>**0.998 0.998**|18.68|18.41|8.69 8.39 16.66 15.01|12.05|11.75|0.088 0.087|4.99|70.95|34.30|
|Ours (4 datasets)|0.991 0.996 **0.998**|**17.44**|**16.92**|**8.03**<br>**7.46**<br>**10.28**<br>**6.68**|**11.10**|**10.50**|**0.046**<br>**0.044**|**4.94**|**64.12**|**31.75**|


Table 4: **Loss ablation on ARCTIC.** 

||Detection||3D Po|se|O|rient. &|Position<br>T|emporal|Worl|d Frame|
|---|---|---|---|---|---|---|---|---|---|---|
|Method|Acc_↑_Rec_↑_F1_↑_|MP-p_↓_|MP_↓_|PA-p_↓_PA_↓_EP-p_↓_|EP_↓_|GO-p_↓_|GO_↓_CT-p_↓_CT_↓_|Jit_↓_|W-MP_↓_|WA-MP_↓_|
|Full|**0.997**<br>**0.999 0.999**|15.79|15.63|**7.27**<br>**7.10**<br>**9.91**|**9.81**|11.55|11.35<br>**0.019**<br>**0.018**|**6.46**|**17.98**|**11.98**|
|w/o jitter|**0.997** 0.998 **0.999**|15.81|15.59|7.38 7.15<br>10.16|10.04|11.69|11.42<br>**0.019**<br>**0.018**|8.29|18.33|12.24|
|w/o 2D reproj.|**0.997**<br>**0.999 0.999**|**15.55**|**15.38**|7.32<br>7.14 11.54|11.45|**11.41**|**11.20** 0.021 0.020|6.71|18.07|12.14|


Table 5: **Pretraining and temporal context on ARCTIC and HOT3D.**<sup>_†_</sup> Single-frame world errors use ground-truth camera rotation and translation (oracle), rather than predicted cameras, and are excluded from world-column ranking. 

||Detection||3D Pose|||Or|ient. &|Position<br>|Temporal|Worl|d Frame|
|---|---|---|---|---|---|---|---|---|---|---|---|
|Method|Acc_↑_Rec_↑_F1_↑_|MP-p_↓_|MP_↓_PA-p_↓_|PA_↓_|EP-p_↓_|EP_↓_|GO-p_↓_|GO_↓_CT-p_↓_CT_↓_|Jit_↓_|W-MP_↓_|WA-MP_↓_|
|_ARCTIC_||||||||||||
|Ours (16 frames)|<br>**0.997**<br>**0.999**<br>**0.999**|**15.79**|**15.63**<br>**7.27**|**7.10**|**9.91**|**9.81**|**11.55**|**11.35**<br>**0.019**<br>**0.018**|**6.46**|**17.98**|**11.98**|
|Random init.|0.993 0.996 0.998|24.74|24.32 11.00|10.52|17.07|16.34|16.89|16.38 0.032 0.030|8.74|37.82|23.20|
|Frozen encoder|**0.997**<br>0.998<br>**0.999**|17.28|17.06<br>7.99|7.75|10.60|10.33|12.46|12.19<br>0.027<br>0.025|7.18|21.14<br>|13.72<br>|
|Single frame|0.996<br>0.998<br>**0.999**|17.79|17.54<br>8.42|8.15|11.71|11.10|12.70|12.44<br>0.021<br>0.020|14.71|21.27<sup>_†_</sup>|14.06<sup>_†_</sup>|
|_HOT3D_||||||||||||
|Ours (16 frames)|<br>**0.989**<br>0.993<br>**0.997**|**13.59**|**12.75**<br>**7.46**|**6.57**|8.09|**5.81**|**7.98**|**7.09**<br>**0.020**<br>**0.017**|**6.91**|**19.84**|**11.49**|
|Random init.|0.969 0.984 0.988|29.02|27.04 12.15|9.89|18.97|12.34|22.27|20.23 0.045 0.037|9.91|48.81|26.87|
|Frozen encoder|**0.989**<br>**0.994**<br>**0.997**|15.24|14.50<br>7.92|7.13|**7.79**|6.41|9.41|8.58<br>0.024<br>0.021|7.90|23.75<br>|13.40<br>|
|Single frame|0.985<br>0.992<br>0.995|16.86|15.83<br>8.76|7.66|9.05|7.00|10.62|9.48<br>0.027<br>0.024|18.31|25.37<sup>_†_</sup>|15.63<sup>_†_</sup>|


Table 6: **Encoder ablation on ARCTIC and HOT3D.** 

||Detection||3D Pose|Or|ient. &|Positi|on<br>|Temporal|Worl|d Frame|
|---|---|---|---|---|---|---|---|---|---|---|
|Method|Acc_↑_Rec_↑_F1_↑_|MP-p_↓_|MP_↓_PA-p_↓_|PA_↓_EP-p_↓_EP_↓_|GO-p_↓_|GO_↓_|CT-p_↓_CT_↓_|Jit_↓_|W-MP_↓_|WA-MP_↓_|
|_ARCTIC_|||||||||||
|V-JEPA 2.1 (ours)|<br>**0.997**<br>**0.999**<br>**0.999**|**15.79**|**15.63**<br>**7.27**|**7.10**<br>**9.91**<br>**9.81**|**11.55**|**11.35**|**0.019**<br>**0.018**|**6.46**|**17.98**|**11.98**|
|VideoMAE|0.978 0.988 0.994|20.26|18.62 10.34|8.57 16.65<br>11.56|15.00|13.28|0.038 0.030|7.96|21.69|14.42|
|DINOv3|0.994<br>0.997<br>0.998|18.66|18.32<br>8.58|8.20<br>11.79<br>11.02|13.34|12.95|0.030<br>0.028|8.47|35.76|20.73|
|PE-Spatial|0.994<br>0.997<br>0.998|20.72|20.41<br>9.58|9.24<br>13.28 12.56|14.35|13.99|0.026<br>0.024|8.94|37.60|22.02|
|_HOT3D_|||||||||||
|V-JEPA 2.1 (ours)|<br>**0.989**<br>**0.993**<br>**0.997**|**13.59**|**12.75**<br>**7.46**|**6.57**<br>**8.09**<br>**5.81**|**7.98**|**7.09**|**0.020**<br>**0.017**|**6.91**|**19.84**|**11.49**|
|VideoMAE|0.984<br>0.991<br>0.995|16.92|15.83<br>8.76|7.60<br>9.84<br>6.86|10.96|9.80|0.025<br>0.021|8.58|22.26|12.95|
|DINOv3|0.983<br>0.990<br>0.994|17.85|16.55<br>9.01|7.62<br>10.50<br>7.35|11.78|10.38|0.027<br>0.023|9.95|45.93|25.24|
|PE-Spatial|0.981 0.989 0.993|20.47|19.16 9.76|8.34 11.86 8.27|14.11|12.74|0.030 0.026|10.31|49.21|27.22|


Table 7: **Forward throughput (FPS** _↑_ **).** 

|GPU|WiLoR|HaMeR|WildHands|Ours|
|---|---|---|---|---|
|RTX A6000|16.3|19.8|21.1|**93.4**|
|A100|11.6|15.4|14.5|**115.1**|


amples provide qualitative evidence of generalization to diverse in-the-wild conditions. Additional ARCTIC and HOT3D comparisons are provided in Appendix A (Figure 3). 

9 

# 5 CONCLUSION 

We presented V-JEPA Hand, a simple model that jointly reconstructs bilateral hand motion, camera motion and intrinsics from egocentric video in one forward pass, without hand detection, SLAM or test-time optimization. Built on V-JEPA 2.1 and trained in a single stage on mixed pseudolabelled and high-quality data, it achieves the lowest coverage-aware MPJPE among reproduced baselines on ARCTIC, HOT3D and the unseen EgoStandard benchmark, and lower world-frame MPJPE than SLAM-based pipelines. Ablations show that mixing in pseudo-labelled video improves generalization, and validate video pretraining, temporal context and encoder choice. Running at over 90 frames per second, V-JEPA Hand enables large-scale bilateral hand-motion annotation of egocentric video to support robot imitation learning in embodied AI. 

# REFERENCES 

- Mahmoud Assran, Quentin Duval, Ishan Misra, Piotr Bojanowski, Pascal Vincent, Michael Rabbat, Yann LeCun, and Nicolas Ballas. Self-supervised learning from images with a joint-embedding predictive architecture. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2023. 

- Mahmoud Assran, Adrien Bardes, et al. V-JEPA 2: Self-supervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. 

- Prithviraj Banerjee, Sindi Shkodrani, Pierre Moulon, Shreyas Hampali, Shangchen Han, Fan Zhang, Linguang Zhang, Jade Fountain, Edward Miller, Selen Basol, Richard Newcombe, Robert Wang, Jakob Engel, and Tomas Hodan. HOT3D: Hand and object tracking in 3D from egocentric multiview videos. _arXiv preprint arXiv:2406.09598_ , 2024. 

- Adrien Bardes, Quentin Garrido, Jean Ponce, Xinlei Chen, Michael Rabbat, Yann LeCun, Mahmoud Assran, and Nicolas Ballas. Revisiting feature prediction for learning visual representations from video. _Transactions on Machine Learning Research (TMLR)_ , 2024. V-JEPA. 

- Hongzhe Bi, Lingxuan Wu, Tianwei Lin, Hengkai Tan, Zhizhong Su, Hang Su, and Jun Zhu. H- rdt: Human manipulation enhanced bimanual robotic manipulation. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 40, pp. 18135–18143, 2026. 

- Andreas Blattmann, Tim Dockhorn, Sumith Kulal, Daniel Mendelevitch, Maciej Kilian, Dominik Lorenz, Yam Levi, Zion English, Vikram Voleti, Adam Letts, Varun Jampani, and Robin Rombach. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_ , 2023. 

- Daniel Bolya, Po-Yao Huang, Peize Sun, Jang Hyun Cho, Andrea Madotto, Chen Wei, Tengyu Ma, Jiale Zhi, Jathushan Rajasegaran, Hanoona Rasheed, et al. Perception encoder: The best visual embeddings are not at the output of the network. _arXiv preprint arXiv:2504.13181_ , 2025. 

- Xingyu Chen, Yufeng Liu, Yajiao Dong, Xiong Zhang, Chongyang Ma, Yanmin Xiong, Yuan Zhang, and Xiaoyan Guo. MobRecon: Mobile-friendly hand mesh reconstruction from monocular image. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2022. 

- Zhengdi Chen et al. Dyn-HaMR: Recovering 4D interacting hand motion from a dynamic camera. _arXiv preprint arXiv:2412.12861_ , 2025. 

- Dima Damen, Hazel Doughty, Giovanni Maria Farinella, Sanja Fidler, Antonino Furnari, Evangelos Kazakos, Davide Moltisanti, Jonathan Munro, Toby Perrett, Will Price, and Michael Wray. Scaling egocentric vision: The EPIC-KITCHENS dataset. In _Proceedings of the European Conference on Computer Vision (ECCV)_ , September 2018. 

- Haoye Dong, Aviral Chharia, Wenbo Gou, Francisco Vicente Carrasco, and Fernando De la Torre. Hamba: Single-view 3D hand reconstruction with graph-guided bi-scanning mamba. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 

10 

- Zicong Fan, Omid Taheri, Dimitrios Tzionas, Muhammed Kocabas, Manuel Kaufmann, Michael J. Black, and Otmar Hilliges. ARCTIC: A dataset for dexterous bimanual hand-object manipulation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2023. 

- Zicong Fan, Maria Parelli, Maria Eleni Kadoglou, Xu Chen, Muhammed Kocabas, Michael J. Black, and Otmar Hilliges. HOLD: Category-agnostic 3D reconstruction of interacting hands and objects from video. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 

- Kristen Grauman, Andrew Westbury, Eugene Byrne, et al. Ego4D: Around the world in 3,000 hours of egocentric video. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2022. 

- Shangchen Han, Po-chen Wu, Yubo Zhang, Beibei Liu, Linguang Zhang, Zheng Wang, Weiguang Si, Peizhao Zhang, Yujun Cai, Tomas Hodan, et al. UmeTrack: Unified multi-view end-to-end hand tracking for VR. In _SIGGRAPH Asia 2022 conference papers_ , pp. 1–9, 2022. 

- Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Dollár, and Ross Girshick. Masked autoencoders are scalable vision learners. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2022. 

- Simar Kareer, Dhruv Patel, Ryan Punamiya, Pranay Mathur, Shuo Cheng, Chen Wang, Judy Hoffman, and Danfei Xu. Egomimic: Scaling imitation learning via egocentric video. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 13226–13233. IEEE, 2025a. 

- Simar Kareer, Karl Pertsch, James Darpinian, Judy Hoffman, Danfei Xu, Sergey Levine, Chelsea Finn, and Suraj Nair. Emergence of human to robot transfer in vision-language-action models. _arXiv preprint arXiv:2512.22414_ , 2025b. 

- Taein Kwon, Bugra Tekin, Jan Stühmer, Federica Bogo, and Marc Pollefeys. H2o: Two hands manipulating objects for first person interaction recognition. In _2021 IEEE/CVF International Conference on Computer Vision (ICCV)_ , pp. 10118–10128. IEEE, 2021. 

- Qixiu Li, Yu Deng, Yaobo Liang, Lin Luo, Lei Zhou, Chengtang Yao, Lingqi Zeng, Zhiyuan Feng, Huizhi Liang, Sicheng Xu, et al. Scalable vision-language-action model pretraining for robotic manipulation with real-life human activity videos. _arXiv preprint arXiv:2510.21571_ , 2025. 

- Lightwheel AI. EgoStandard: Hardware-assisted egocentric multi-modal hand motion benchmark. https://lightwheel.ai/egosuite, 2025. 

- Hao Luo, Yicheng Feng, Wanpeng Zhang, Sipeng Zheng, Ye Wang, Haoqi Yuan, Jiazheng Liu, Chaoyi Xu, Qin Jin, and Zongqing Lu. Being-h0: vision-language-action pretraining from largescale human videos. _arXiv preprint arXiv:2507.15597_ , 2025. 

- Gyeongsik Moon. Bringing inputs to shared domains for 3D interacting hands recovery in the wild. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2023. 

- Lorenzo Mur-Labadia, Matthew Muckley, Amir Bar, Mido Assran, Koustuv Sinha, Mike Rabbat, Yann LeCun, Nicolas Ballas, and Adrien Bardes. V-JEPA 2.1: Unlocking dense features in video self-supervised learning. _arXiv preprint arXiv:2603.14482_ , 2026. 

- JoonKyu Park, Yeonguk Oh, Gyeongsik Moon, Hongsuk Choi, and Kyoung Mu Lee. HandOccNet: Occlusion-robust 3D hand mesh estimation network. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2022. 

- Georgios Pavlakos, Dandan Shan, Ilija Radosavovic, Angjoo Kanazawa, David Fouhey, and Jitendra Malik. Reconstructing hands in 3D with transformers. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 

- Rolandos Alexandros Potamias, Jinglei Zhang, Jiankang Deng, and Stefanos Zafeiriou. WiLoR: End-to-end 3d hand localization and reconstruction in-the-wild. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2025. arXiv:2409.12259. 

11 

- Aditya Prakash, Ruisen Tu, Matthew Chang, and Saurabh Gupta. 3D hand pose estimation in everyday egocentric images. In _Proceedings of the European Conference on Computer Vision (ECCV)_ , 2024. 

- Javier Romero, Dimitrios Tzionas, and Michael J. Black. Embodied hands: Modeling and capturing hands and bodies together. _ACM Transactions on Graphics (SIGGRAPH Asia)_ , 36(6), 2017. 

- Soyong Shin, Juyong Kim, Eni Halilaj, and Michael J. Black. WHAM: Reconstructing worldgrounded humans with accurate 3D motion. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 

- Oriane Siméoni, Huy V. Vo, Maximilian Seitzer, Federico Baldassarre, Maxime Oquab, Cijo Jose, Vasil Khalidov, Marc Szafraniec, Seungeun Yi, Michaël Ramamonjisoa, et al. DINOv3. _arXiv preprint arXiv:2508.10104_ , 2025. 

- Anna H Smeragliuolo, N Jeremy Hill, Luis Disla, and David Putrino. Validation of the leap motion controller using markered motion capture technology. _Journal of biomechanics_ , 49(9):1742– 1750, 2016. 

- Zachary Teed and Jia Deng. DROID-SLAM: Deep visual SLAM for monocular, stereo, and RGB-D cameras. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2021. 

- Zhan Tong, Yibing Song, Jue Wang, and Limin Wang. VideoMAE: Masked autoencoders are dataefficient learners for self-supervised video pre-training. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2022. 

- Limin Wang, Bingkun Huang, Zhiyu Zhao, Zhan Tong, Yinan He, Yi Wang, Yali Wang, and Yu Qiao. VideoMAE V2: Scaling video masked autoencoders with dual masking. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2023. 

- Yuxi Wang, Chengkai Jin, Yufei Liu, Wenqi Ouyang, Tianyi Wei, Zhiwei Zeng, Siyuan Huang, Zhiqi Shen, and Xingang Pan. The surprising effectiveness of video diffusion models for hand motion reconstruction. _arXiv preprint arXiv:2606.30308_ , 2026. 

- John Yang, Hyung Jin Chang, Seungeui Lee, and Nojun Kwak. SeqHAND: RGB-sequence-based 3D hand pose and shape estimation. In _Proceedings of the European Conference on Computer Vision (ECCV)_ , 2020. 

- Ruihan Yang, Qinxi Yu, Yecheng Wu, Rui Yan, Borui Li, An-Chieh Cheng, Xueyan Zou, Yunhao Fang, Xuxin Cheng, Ri-Zhao Qiu, et al. Egovla: Learning vision-language-action models from egocentric human videos. _arXiv preprint arXiv:2507.12440_ , 2025. 

- Vickie Ye, Georgios Pavlakos, Jitendra Malik, and Angjoo Kanazawa. Decoupling human and camera motion from videos in the wild. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2023. 

- Jinglei Zhang, Jiankang Deng, Chao Ma, and Rolandos Alexandros Potamias. HaWoR: World-space hand motion reconstruction from egocentric videos. _arXiv preprint arXiv:2501.02973_ , 2025. 

- Xin Zhang, Yuqi Ren, Di Kang, Junyu Xie, et al. OmniHands: Towards robust 4D hand mesh recovery via A versatile transformer. _arXiv preprint arXiv:2405.20330_ , 2024. 

- Ruijie Zheng, Dantong Niu, Yuqi Xie, Jing Wang, Mengda Xu, Yunfan Jiang, Fernando Castañeda, Fengyuan Hu, You Liang Tan, Letian Fu, et al. Egoscale: Scaling dexterous manipulation with diverse egocentric human data. _arXiv preprint arXiv:2602.16710_ , 2026. 

12 

# APPENDIX 

## CONTENTS 

|A|Additional Qualitative Comparisons . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14|
|---|---|
|B|Encoder Feature Visualization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .17|
|C|Hyperparameters . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .18|
|D|Training objective details . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18|
|E|Evaluation protocols and baseline setup . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19|
|F|Evaluation metrics and table conventions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21|
|G|Ablation implementation details . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21|


13 

# A ADDITIONAL QUALITATIVE COMPARISONS 


Figure 3: **Qualitative comparisons on ARCTIC and HOT3D.** Each row shows a reference frame and the four methods’ reconstructions overlaid on that frame. Blue and orange denote left and right hands, respectively. Examples illustrate missed hands and differences in mesh placement under occlusion and partial visibility. 

14 


Figure 4: **Challenging in-the-wild cases.** Comparisons with HaMeR, WiLoR, and WildHands under low light, outdoor backgrounds, and clutter. The first and sixth rows highlight hand reconstructions retained by V-JEPA Hand when the baselines miss the hand. 

15 

Figure 3 compares mesh overlays on ARCTIC and HOT3D during hand–object interactions. The examples highlight partial visibility, object occlusion, and hands near the image boundary. In the ARCTIC box-handling example (Figure 3, fourth row from the top), V-JEPA Hand reconstructs both hands near the lower image boundary, whereas HaMeR and WiLoR omit the left hand. In the HOT3D plate-holding example (Figure 3, eighth row from the top), V-JEPA Hand and WiLoR reconstruct the visible hand, while HaMeR and WildHands do not show a reconstruction. Other examples reveal differences in wrist placement and finger articulation around manipulated objects. These overlays complement the quantitative results by showing where methods miss hands or produce visibly misaligned meshes. 

Figure 4 extends the comparison to challenging in-the-wild videos, including very low light, outdoor pruning, painting, and household activities. In the low-light scenes in the first and sixth rows of Figure 4, V-JEPA Hand reconstructs a hand that all three baselines miss. In the outdoor pruning scene (second row), V-JEPA Hand reconstructs both hands against a background of dense foliage. The painting scene (fourth row) and the sink scene (eighth row) show hand reconstructions during object manipulation in cluttered indoor environments. Across these settings, V-JEPA Hand recovers plausible hand configurations despite substantial changes in lighting, appearance, and scene layout. These examples provide qualitative evidence of generalization beyond laboratory settings. 

16 

# B ENCODER FEATURE VISUALIZATION 

Figure 5 visualizes encoder features after end-to-end training for hand and camera trajectory recovery. V-JEPA 2.1 learns dense representations that capture fine-grained spatial structure as well as global visual information (Mur-Labadia et al., 2026). Our visualizations suggest that meaningful spatial and semantic structure remains present after task-specific training: regions corresponding to hands and forearms form coherent feature patterns, while manipulated objects and surrounding surfaces often exhibit distinct patterns. These observations are consistent with retaining semantically structured features while adapting the encoder to geometric prediction. 


Figure 5: **Encoder features after task-specific training.** Each input frame is paired with its feature visualization on the right. Coherent patterns corresponding to hands, arms, objects, and scene surfaces suggest that the fine-tuned encoder retains meaningful spatial and semantic structure. 

17 

# C HYPERPARAMETERS 

Table 8 lists the architecture, loss, optimization and data settings of the reported V-JEPA Hand model, which is trained in a single stage on the mixture of pseudo-labelled and high-quality data. 

Table 8: **Hyperparameters.** Model and training settings for V-JEPA Hand. For smooth- _L_ 1 regression, _δ_ is the absolute error at which the penalty changes from quadratic to linear. 

|Group|Hyperparameter|Value|
|---|---|---|
|Encoder|backbone<br>tubelet / patch<br>tokens per clip<br>fine-tuning|V-JEPA 2.1 ViT-L/384 ( pretrained)<br>2(time) /16_×_16(space)<br>8_×_24_×_24 = 4608, dim1024<br>full (unfrozen)|
|Predictor|type / depth<br>width / heads<br>query tokens<br>attention<br>stochastic depth|ViT-L /24layers<br>1024/16, MLP ratio4<br>16(one per frame)<br>joint self-attention<br>0_._1|
|Targets|end-effector pose<br>articulation<br>presence|9-dim (3 trans+6D rot), per hand<br>45-dim MANO Euler angles, per hand<br>1logit per hand per frame|
|Loss|regression<br>transition_δ_<br>joint geometry<br>jitter<br>presence|smooth-_L_1; weight1_._0per term<br>0_._05(wrist and camera rotation)<br>0_._03(wrist / camera translation, 3D joints)<br>0_._02(articulation, 2D reproj., focal lengths)<br>neutral-shape MANO FK<br>_L_1 joint acceleration, weight0_._2<br>BCE, weight0_._5|
||optimizer<br>lr (predictor)|AdamW,_β_=(0_._9_,_0_._95), wd0_._05<br>6_×_10<sup>_−_4</sup>|
|Optimization|lr (encoder)<br>schedule<br>training steps<br>effective batch|2_×_10<sup>_−_5</sup><br>1_,_800-step linear warmup+cosine decay, min ratio5_×_10<sup>_−_4</sup><br>30_,_519<br>64clips (8GPUs_×_grad-accum8)|
|Data|sources (prob.)<br>clip length / size<br>augmentation<br>intrinsics input|pseudo-labelled0_._35, ARCTIC0_._45, HOT3D0_._20<br>16frames /384_×_384<br>frame stride_{_1_,_2_,_4_,_8_}_, horizontal flip, aspect ratio[1_,_2]<br>withheld with probability0_._5|


# D TRAINING OBJECTIVE DETAILS 

We detail the losses in Equation 6 using the notation of Section 3.1: _t_ indexes frames and _s ∈{_ L _,_ R _}_ indexes hands. Hats denote predictions and unhatted quantities denote targets. We write _ρδ_ for the standard smooth- _L_ 1 loss averaged over coordinates, where _δ_ is its fixed quadratic-to-linear transition threshold. For hand geometry, _⟨·⟩v_<sup>_s_</sup> averages over frames with a valid, visible target for hand _s_ among the video clips processed together in one forward/backward pass. The two hands’ losses are summed. 

**Hand parameters.** We directly supervise wrist translation **d**<sup>_s_</sup> _t_<sup>_∈_R3 in camera-space metres, wrist</sup> orientation **r**<sup>_s_</sup> _t_<sup>_∈_R6inthe6Drotationrepresentation,andfingerarticulation</sup><sup>**_θ_**</sup> _t_<sup>_s∈_R45asEuler</sup> 

18 

angles in radians: 


The subscripts of _ρ_ give the fixed threshold for each term. 

**Forward kinematics.** The differentiable MANO forward-kinematics layer FK maps the predicted hand state **x** ˆ<sup>_s_</sup> _t_<sup>to</sup><sup>**J**ˆ</sup><sup>_s_</sup> _t_<sup>=FK(ˆ</sup><sup>**x**</sup><sup>_s_</sup> _t_<sup>)</sup><sup>_∈_R21</sup><sup>_×_3, the 21 camera-space joints in metres, using neutral hand</sup> shape. We supervise these positions with 


The target **J**<sup>_s_</sup> _t_<sup>_∈_R21</sup><sup>_×_3is the dataset’s measured 3D joints when available and FK(</sup><sup>**x**</sup> _t_<sup>_s_) otherwise.</sup> This term couples wrist pose and finger articulation through their effect on joint positions. 

**Reprojection.** Let _π_ **k** project 3D joints to image coordinates using the ground-truth calibration, with **k** = ( _fx, fy_ ) denoting the horizontal and vertical focal lengths. The reprojection loss encourages image alignment: 


Ground-truth intrinsics remain available to this loss even when they are withheld from the predictor. 

**Temporal smoothness.** The jitter loss _La_ is the mean absolute second-order difference of predicted joints, 


where _T_ is the clip length. We average over joint coordinates and triplets with valid targets in all three sampled frames, then sum over hands. Constant-velocity motion in camera coordinates incurs no penalty. 

**Hand presence.** The presence loss _Lc_ applies binary cross-entropy to the predicted logit _c_ ˆ<sup>_s_</sup> _t_<sup>and</sup> the binary hand-presence target. It includes both present and absent hands, but excludes unknown targets and frames outside the anchor recording. We average over valid frames for each hand and sum the two losses. 

**Camera motion.** The camera loss _Lg_ supervises the transform from each camera frame to the first-frame anchor. It sums smooth- _L_ 1 losses on the 6D rotation and signed-log translation defined in Equation 3, with thresholds 0 _._ 05 and 0 _._ 03, respectively. Each block is averaged over its coordinates and frames with valid camera targets in the anchor recording. 

**Intrinsics loss.** The intrinsics loss _Lk_ supervises the horizontal and vertical focal lengths ( _fx, fy_ ) using smooth- _L_ 1, averaged over the two components. It is applied only to clips whose intrinsics were withheld from the predictor. 

**Loss weights.** All regression terms have unit weight, including both camera-motion blocks. The jitter and presence losses have weights 0 _._ 2 and 0 _._ 5, respectively. 

# E EVALUATION PROTOCOLS AND BASELINE SETUP 

**Baseline implementations.** We run WiLoR, HaMeR, WildHands and HaWoR for the comparisons in Table 1. ViDiHand’s ARCTIC/HOT3D detection, coverage-aware pose and jitter scores are taken from Table 1 of Wang et al. (2026). Since its pretrained weights are not publicly available, we cannot reproduce its true-positive-only scores or evaluate it on EgoStandard. 

19 

**Hand evaluation.** We follow ViDiHand’s evaluation protocol (Wang et al., 2026). For ARCTIC, we use the dataset’s official validation split; for HOT3D, we follow the validation split used by HaWoR (Zhang et al., 2025). The evaluated clips in Table 1 cover approximately 13 minutes of ARCTIC, 49 minutes of HOT3D and 60 minutes of EgoStandard. We use the same trained V-JEPA Hand model for all three benchmarks. 

**World-coordinate comparison.** Table 2 uses WiLoR+SLAM, HaMeR+SLAM, HaWoR, and V- JEPA Hand. It uses the same evaluation splits and trained V-JEPA Hand model as Table 1. The +SLAM baselines use the DROID-SLAM camera implementation distributed with HaWoR, with metric scale estimation; their camera inference is independent of the hand model. Unlike the handonly evaluation in Table 1, the world-coordinate evaluation augments WiLoR and HaMeR with SLAM-based camera estimates. We first retain clips with completed predictions from all four displayed methods, then evaluate on their common true-positive hands in each frame. We evaluate a hand track only if it contains at least three frames with valid ground truth and true-positive predictions from all four methods. 

**World-coordinate metrics.** For the hand tracks selected above, Table 2 reports joint position errors (W-MPJPE and WA-MPJPE) and relative wrist trajectory error (RTE), evaluated over the full clip. Before measuring errors, we align the predicted hand trajectory to the ground truth using one rotation and translation for the whole track. This rigid alignment does not change scale or adjust frames independently. The metrics differ in how this alignment is estimated and which errors are measured: 

- **W-MPJPE: align at the start.** We fit the rotation and translation using the 21 predicted and ground-truth hand joints in the first evaluated frame, then apply that same transformation to every evaluated frame. We report the mean Euclidean joint error over all 21 joints and all evaluated frames, including the first frame, in millimetres. This measures how well the reconstruction follows the ground truth after the initial alignment. 

- **WA-MPJPE: align the whole track.** We instead fit a single rotation and translation using the corresponding joints from all evaluated frames together. We then compute the same mean joint error in millimetres. Unlike W-MPJPE, the alignment uses the entire track rather than only its first evaluated frame. 

- **RTE: normalize wrist error by motion magnitude.** Using the whole-track alignment from WA-MPJPE, we compute the mean Euclidean distance between predicted and ground-truth wrist positions. We divide this error by the largest distance that the ground-truth wrist moves from its position in the first evaluated frame, and multiply by 100 to obtain a percentage. The denominator is a displacement from the starting position, not the total distance travelled. Tracks with this maximum displacement below 1 mm are excluded from RTE to avoid dividing by a near-zero motion magnitude; they remain included in W-MPJPE and WA-MPJPE. 

**Training-data comparison.** Table 3 isolates the effect of adding pseudo-labelled Ego4D and inhouse videos to ARCTIC and HOT3D training data. Both models start from the same pretrained V-JEPA 2.1 encoder and are trained in a single stage, with the same architecture, training budget, and HOT3D training-window filter. Ours mixes all four datasets throughout training; the two-dataset baseline samples ARCTIC and HOT3D equally and never trains on Ego4D or in-house videos. Neither model uses the task-specific two-stage recipe employed by the loss, pretraining and encoder ablations (Appendix G.1). We evaluate both models on EgoStandard, which is unseen during training, to test generalization rather than performance on the training datasets. Hand evaluation uses unsmoothed predictions, MANO-fit targets and projected MANO mesh boxes for matching. Worldcoordinate evaluation uses the two models’ common true-positive hand-frames and the full-track metrics defined in Appendix E. 

**HOT3D evaluation split.** The official HOT3D test sequences have no public ground-truth MANO. Table 1 uses the HaWoR-aligned held-out split, whereas ViDiHand uses a random 5% of the validation sequences. The reported ViDiHand HOT3D scores are therefore shown in gray for reference only and excluded from ranking. 

20 

# F EVALUATION METRICS AND TABLE CONVENTIONS 

**Coverage-aware and true-positive-only evaluation.** We report two complementary views of pose accuracy, following the coverage-aware evaluation implementation of Wang et al. (2026) for metrics with the _−p_ suffix. The _coverage-aware_ view replaces each unmatched ground-truth hand with a canonical rest-pose MANO placeholder before averaging. These columns carry the - _p_ suffix and reflect both detection coverage and reconstruction accuracy. The _true-positive-only_ view averages pose errors over matched prediction–ground-truth hands. FAcc, recall and F1 report detection separately. 

The main hand comparison and hand-pose ablations report both views. True-positive-only pose scores are unavailable for ViDiHand and are marked with dashes, because they cannot be recovered from its published coverage-aware results. 

**Table notation and units.** Table headers abbreviate frame accuracy (FAcc) as **Acc** , recall as **Rec** , MPJPE as **MP** , PA-MPJPE as **PA** , EPE as **EP** , and Jitter as **Jit** . F1, global-orientation error ( **GO** ), and camera-translation error ( **CT** ) retain their short names. The pairs MP- _p_ /MP, PA- _p_ /PA, EP- _p_ /EP, GO- _p_ /GO, and CT- _p_ /CT report coverage-aware and true-positive-only errors, respectively. In the world comparison and ablations, **W-MP** and **WA-MP** denote W-MPJPE and WA-MPJPE (Zhang et al., 2025). The world comparison additionally reports relative trajectory error ( **RTE** ) as a percentage; alignment and scoring details are given in Appendix E. Across all tables, MP, PA, W-MP, and WA-MP are in millimetres; EP is in pixels, GO in degrees, CT in metres, and Jit in mm/frame<sup>2</sup> . The _−p_ columns use the same units as their unsuffixed counterparts. Detection, Jit, and world-frame metrics are reported once rather than as paired columns. Detection scores lie in [0 _,_ 1] and are higheris-better; all other metrics are lower-is-better. Jitter is true-positive-only in both metric views. Bold marks column bests where applied, and shading runs from white (worst) to yellow (best) within each benchmark block. Colours are normalized within each column and do not indicate the absolute size of an improvement. 

# G ABLATION IMPLEMENTATION DETAILS 

## G.1 TRAINING SETUP 

Unlike the single-stage training-data comparison in Table 3, the loss, pretraining and encoder ablations use a smaller two-stage recipe. The first stage trains on half of the Ego4D pseudo-labelled data; the second fine-tunes the resulting model on ARCTIC and HOT3D. Each ablation changes one component of this shared setup and is evaluated after both training phases. Comparisons within each ablation isolate the component being studied. 

## G.2 WORLD-COORDINATE EVALUATION 

Within each component ablation, all variants use the same evaluation split and the W-MPJPE and WA-MPJPE definitions in Appendix E. The single-frame variant is an exception to the cameramotion evaluation: it cannot estimate camera motion between frames, so its hand predictions are transformed into world coordinates using ground-truth camera poses for scoring, without providing these poses to the hand model. Because this gives it camera information unavailable to the other variants, its world-coordinate scores are marked with a dagger and reported for reference only, not included in ranking. All component ablations share the same HOT3D evaluation split, which differs from Table 1; comparisons therefore focus on variants within each ablation rather than differences from the main table. 

## G.3 ENCODER CONFIGURATIONS 

We use the same ViT-L backbone scale and self-attention predictor design, and match the number of temporal token groups across encoders. V-JEPA 2.1 and VideoMAE use 16 input frames with twoframe tubelets, whereas DINOv3 and PE-Spatial use 8 independently encoded frames, yielding eight temporal groups in both cases. This keeps the number of temporal groups passed to the predictor consistent, although the spatial grids and input durations differ. Output query counts match the input 

21 

frame counts. The configured training image size is 384 for V-JEPA 2.1 and 224 for the alternatives; PE-Spatial’s positional grid is interpolated from its pretrained 448-pixel configuration. For DINOv3 and PE-Spatial, frames are processed as a batch of images, prefix tokens are removed, and patch tokens are concatenated in temporal order for the predictor. Temporal attention is therefore learned in the predictor rather than applied within the image backbone. 

22 

