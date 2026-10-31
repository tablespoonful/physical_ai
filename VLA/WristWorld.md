---
title: "WristWorld: Generating Wrist-Views via 4D World Models for Robotic Manipulation"
date: "2025-10-08"
authors: "Zezhong Qian; Xiaowei Chi; Yuming Li; Shizun Wang; Zhiyuan Qin; Xiaozhu Ju"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2510.07313
pdf: https://arxiv.org/pdf/2510.07313
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2510.07313)** / [論文ページ](https://arxiv.org/abs/2510.07313)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

WRISTWORLD: GENERATING WRIST-VIEWS VIA 4D WORLD MODELS FOR ROBOTIC MANIPULATION 

**Zezhong Qian**<sup>1,*</sup> **Xiaowei Chi**<sup>2,*,</sup><sup>_†_</sup> **Yuming Li**<sup>1</sup> **Shizun Wang**<sup>3</sup> **Zhiyuan Qin**<sup>4</sup> **Xiaozhu Ju**<sup>4</sup> **Sirui Han**<sup>2,�</sup> **Shanghang Zhang**<sup>1,�</sup> 

> 1 State Key Laboratory of Multimedia Information Processing, School of Computer Science, Peking University 

> 2 Hong Kong University of Science and Technology 

> 3 National University of Singapore 

> 4 Beijing Innovation Center of Humanoid Robotics 

# ABSTRACT 

Wrist-view observations are crucial for VLA models as they capture fine-grained hand–object interactions that directly enhance manipulation performance. Yet large-scale datasets rarely include such recordings, resulting in a substantial gap between abundant anchor views and scarce wrist views. Existing world models cannot bridge this gap, as they require a wrist-view first frame and thus fail to generate wrist-view videos from anchor views alone. Amid this gap, recent visual geometry models such as VGGT emerge with precisely the geometric and cross-view priors that make it possible to address such extreme viewpoint shifts. Inspired by these insights, we propose **WristWorld** , the first 4D world model generates wrist-view videos solely from anchor views. WristWorld operates in two stages: (i) _Reconstruction_ , which extends VGGT and incorporates our Spatial Projection Consistency (SPC) Loss to estimate geometrically consistent wrist-view poses and 4D point clouds; (ii) _Generation_ , which employs our designed video generation model to synthesize temporally coherent wrist-view videos from the reconstructed perspective. Experiments on Droid, Calvin, and Franka Panda demonstrate stateof-the-art video generation with superior spatial consistency, while also improving VLA performance, raising the average task completion length on Calvin by 3.81% and closing **42.4%** of the anchor-wrist view gap. 

## � Project Page | � Code 


Figure 1: We present **WristWorld** , a framework that synthesizes realistic wrist-view videos from anchor views through a two-stage process: a _reconstruction stage_ for estimating wrist-view projections, and a _generation stage_ for producing coherent wrist-view videos. The generated wrist observations effectively expanding training data to novel view and lead to significant performance improvements for downstream VLA models across various tasks. 

* Equal contribution, _†_ Project leader 

1 

# 1 INTRODUCTION 

Wrist-view observations play a central role in vision–language–action (VLA) models because they directly capture the fine-grained hand–object interactions that underlie precise manipulation. However, most large-scale robotic datasets provide only limited wrist-view coverage (Ebert et al., 2024; Mandlekar et al., 2018; Collaboration et al., 2025), producing a substantial and practically important gap between abundant anchor (third-person) views and scarce wrist-centric recordings. Models pretrained on external perspectives therefore often underperform when tasks require detailed wristcentric perception or control. 

Collecting wrist-view data at scale is expensive: it demands extra sensors, careful calibration, and specialized recording setups. While world models have been proposed for data completion and synthesis (Wang et al., 2025c; Yang et al., 2023; Zhen et al., 2025), existing approaches are not designed to close the anchor-to-wrist gap in realistic, dynamic manipulation settings. Many of them (Liao et al., 2025; Liu et al., 2024) require a wrist-view first frame as a condition and thus cannot generate wrist-view sequences from anchor views alone. This raises a natural question: **_can we enrich existing third-person datasets with automatically generated, geometrically consistent wrist-view sequences that support both perception and control?_** 

However, bridging anchor views to wrist views is highly challenging: First, scenes are dynamic and dominated by articulated arms and manipulators that cause severe, time-varying occlusions. Second, the target wrist perspective is often not seen during training of current viewpoint transfer methods. Third, geometric reconstructions from anchor views are typically sparse and temporally inconsistent, making naïve view-synthesis prone to spatial or temporal artifacts (Liu et al., 2024). 

To address these challenges, we propose **WristWorld** , the first _4D world model_ that synthesizes wrist-view videos solely from anchor views. Motivated by recent advances in visual geometric modeling (Wang et al., 2025b) and diffusion-based video synthesis (Blattmann et al., 2023), WristWorld features a two-stage pipeline that explicitly enforces both geometric and temporal consistency. In the _Reconstruction_ stage, we extend VGGT with a dedicated wrist head that encodes the extreme viewpoint transform and estimates geometrically consistent 4D point clouds and wrist-view camera poses. A novel _Spatial Projection Consistency_ (SPC) loss is proposed to enforce alignment between 2D correspondences and the reconstructed 3D/4D geometry, improving spatial fidelity. In the _Generation_ stage, a diffusion-based video generator conditioned on the reconstructed wrist projections and CLIP-encoded anchor-view features synthesizes temporally coherent wrist-view videos that respect the recovered geometry and scene semantics. 

We validate WristWorld on Droid (Khazatsky et al., 2024), Calvin (Mees et al., 2022), and Franka Panda setups. Results show state-of-the-art wrist-view video generation with superior spatial consistency, and practical downstream gains for VLA: on Calvin we increase average task completion length by **3.81%** and close **42.4%** of the anchor–wrist performance gap. Importantly, WristWorld can be used as a plug-in to extend existing single-view world models with multi-view capability without requiring new wrist-view data collection. 

## **Our contributions are three-fold:** 

- A novel two-stage framework for anchor-view to wrist-view video generation that achieves both temporal Consistency and geometric consistency. 

- Leveraging a wrist head, SPC loss, and CLIP-encoded anchor-view features to synthesize consistent wrist-view sequences from anchor views. 

- Experiments showing that our approach improves VLA performance and can be applied in a plugand-play manner to extend single-view world models into multi-view settings. 

# 2 RELATED WORK 

**3D Reconstruction for Robotic Perception** . Accurate multi-view 3D reconstruction and camera pose are key for manipulation, yet many frameworks assume fixed calibration or static views. Recent work injects geometry into policies; e.g., GNFactor jointly optimizes a NeRF scene model and a manipulation policy, sharing one 3D representation for multi-task learning (Ze et al., 2023). Transformer-based vision models have also been explored; for instance, VGGT encodes multi-view 

2 

observations into fused geometric features for 3D prediction (Wang et al., 2025b). Still, moving wrist-camera pose is rarely modeled, and large datasets rely on manual calibration instead of online wrist-centric pose prediction. Cross-view consistency remains crucial in dynamic 3D scene reconstruction (Wang et al., 2025d; Hu et al., 2025), with MTVCrafter introducing 4D motion tokens to enforce coherence (Ding et al., 2025). 

**Video Generation Models for Manipulation** . Diffusion-based video generators let planners “imagine” robot futures. Web-scale text-to-video models look realistic but struggle with novel object–action combinations. RoboDreamer improves compositionality by factorizing generation via language parsing (Zhou et al., 2024). This&That adds gesture conditioning for controllable plans beyond text-only inputs (Wang et al., 2025a). Coupling prediction with control, VideoAgent iteratively self-refines diffused plans to reduce hallucinations (Soni et al., 2025), and action-conditioned diffusion in generative predictive control approximates dynamics for policy improvement (Qi et al., 2025). Synthetic data routes like DreamGen synthesize diverse “dream” trajectories for stronger generalization (Jang et al., 2025). For spatial consistency, EnerVerse combines multi-view diffusion with 4D reconstruction (Gaussian splatting) to produce geometry-consistent futures and better long-horizon planning (Huang et al., 2025; Li et al., 2025). Large frameworks such as UniPi use text-guided video generation to learn universal multi-task policies (Du et al., 2023; Chi et al., 2025a). 

**Vision–Language–Action (VLA) Robotics Models** . VLA policies learn directly from paired visual and linguistic inputs without constructing an explicit world model. GR-1, a GPT-style videoconditioned policy, is pretrained on large human video corpora and fine-tuned to achieve state-ofthe-art multi-task performance on CALVIN (88.9% to 94.9%) with zero-shot generalization to novel scenes (Wu et al., 2023; Mees et al., 2022). GR-2 scales training to 38M video–text pairs, producing a generalist agent capable of executing 100+ manipulation tasks by grounding instructions in action sequences (Cheang et al., 2024). Beyond internet video pretraining, Vid2Robot maps human video demonstrations to robot policies via cross-attention (Jain et al., 2024), and MimicPlay derives hierarchical plans from unstructured human play (Wang et al., 2023). Label-free alignment has also been explored by grounding a frozen video generator into continuous actions through goal-conditioned self-exploration (Luo & Du, 2024). Conversely, human-in-the-loop fine-tuning attains high dexterity yet forgoes an explicit visual world model (Luo et al., 2025; Chi et al., 2025b). 

# 3 METHOD 

Our method is a two-stage 4D Generative World Model designed to synthesize geometrically consistent wrist-view videos from third-person observations. The first _reconstruction stage_ estimates wrist poses and generates condition maps via point cloud projection. The second _generation stage_ synthesizes temporally coherent wrist-view sequences conditioned on these maps and enriched by semantic guidance. The overall framework is illustrated in Figure 2. 

## 3.1 PRELIMINARY 

**Video Diffusion Models.** Recent advances in video synthesis are largely driven by diffusionbased generative models. A video **X** = _{x_<sup>_t_</sup> _}_<sup>_T_</sup> _t_ =1<sup>isfirstcompressedintoalatentrepresentation</sup> **Z** 0 = _{z_<sup>_t_</sup> _}_<sup>_T_</sup> _t_ =1<sup>_∈_R</sup><sup>_T ×C×H×W_using a video VAE, which reduces spatial and temporal resolution</sup> while preserving content semantics. The diffusion framework then defines a forward noising process that gradually perturbs **Z** 0 into Gaussian noise, and a learned denoising model _ϵθ_ that reverses this process. At training time, the objective is to predict the added noise given the noisy latent **Z** _τ_ at step _τ_ and the conditioning signal _S_ : 


where **_ϵ_** _∼N_ (0 _,_ **I** ) and **Z** _τ_ is obtained by a variance-scheduled corruption of **Z** 0. In a Diffusion Transformer (DiT), conditioning _c_ is typically realized as _text embeddings_ , which are projected into conditioning tokens and injected into the transformer blocks, thereby guiding the denoising process. 

**Visual Geometry Models.** To capture multi-view geometry and establish dense cross-view correspondences, we build on VGGT (Wang et al., 2025b), a large Transformer that encodes multicamera observations into fused features **F** and predicts 3D quantities such as point clouds and correspondences. Given a query point **u**<sup>_j_</sup> _q_<sup>in image</sup><sup>_Iq_, the matching head predicts corresponding points</sup> 

3 


Figure 2: **Overview of our method.** We introduce a two-stage 4D Generative World Model. In the reconstruction stage, VGGT Wang et al. (2025b) is extended with a wrist head to regress wrist pose, guided by a Spatial Projection Consistency Loss that supervises directly from RGB without depth or extrinsics. The predicted pose projects point clouds into the wrist view. In the generation stage, these projections, combined with external-view CLIP embeddings, condition a video generator to synthesize wrist-view sequences. Without first-frame guidance, the model produces additional wrist views for VLA datasets, yielding substantial performance gains. 

_{_ **u** ˆ<sup>_j_</sup> _i_<sup>_}_</sup> _i_<sup>_N_</sup> =1<sup>in other views</sup><sup>_{Ii}_, where</sup><sup>_N_is the number of anchor views and</sup><sup>_M_the number of sampled</sup> query points. The resulting correspondences are 


providing dense pixel-level matching across anchor and wrist views. We adopt the pinhole camera model, where a 3D point **y** ˆ _∈_ R<sup>3</sup> projects to pixel **u** _∈_ R<sup>2</sup> via camera intrinsics **K** , extrinsics ( **R** _,_ **T** ), and projection function Π( _·_ ): 


## 3.2 RECONSTRUCTION STAGE 

**Wrist Head Design.** To estimate the wrist-mounted viewpoint, we extend VGGT with a specialized _wrist head_ . Based on the aggregated multi-view features **F** , we introduce a set of learnable wrist queries that attend to these tokens through a Transformer decoder. The wrist head regresses the wrist camera extrinsics, denoted as rotation **R** _w ∈ SO_ (3) and translation **T** _w ∈_ R<sup>3</sup> : 


where **q** _w_ are the wrist queries. This design allows the model to capture hand-centered motion and implicit camera pose even when wrist-view data is unavailable. 

**Spatial Projection Consistency Loss.** Direct supervision of wrist extrinsics or depth maps is often missing. To address this, we propose a _Spatial Projection Consistency (SPC) loss_ that enforces 

4 

geometric consistency from RGB correspondences alone. As shown in Figure 3, given dense 2D– 2D correspondences _C_ = _{_ ( **u**<sup>_j_</sup> _q_<sup>_,_ˆ</sup><sup>**u**</sup> _w_<sup>_j_)</sup><sup>_}M_</sup> _j_ =1<sup>between an anchor view</sup><sup>_Iq_and the wrist view</sup><sup>_Iw_,and a</sup> reconstructed point cloud _Y_ = _{_ **y** ˆ _k}_ from anchor views, we associate each anchor pixel **u**<sup>_j_</sup> _q_<sup>with its</sup> corresponding 3D point **y** ˆ _j ∈Y_ . This yields a set of 3D–2D pairs 


linking reconstructed world points to wrist-view pixels. 

For each pair (ˆ **y** _j,_ ˆ **u**<sup>_j_</sup> _w_<sup>),theprojectionof</sup><sup>**y**ˆ</sup><sup>_j_underthepredictedwristpose(</sup><sup>**R**</sup><sup>_w,_</sup><sup>**T**</sup><sup>_w_)isdenoted</sup> by **u**<sup>_′_</sup> _w_<sup>_j_=Π(</sup><sup>**K**</sup><sup>_,_</sup><sup>**R**</sup><sup>_w,_</sup><sup>**T**</sup><sup>_w,_ˆ</sup><sup>**y**</sup><sup>_j_), where</sup><sup>**K**is fixed by the dataset.We then divide points into</sup><sup>_S_frontfor</sup> positive depth values and _S_ back for negative ones. The SPC loss consists of two terms: 


where _zj_ is the depth value of point **y** ˆ _j_ in the wrist camera coordinate frame. Finally, the projection loss is defined as _L_ proj = _λuLu_ + _λ_ depth _L_ depth, where _λu_ and _λ_ depth control the balance between reprojection consistency and depth feasibility. 

**Condition Map Generation.** With the estimated wrist poses across frames, reconstructed 3D scenes are projected into the wrist-view image plane to form a temporally aligned sequence of _condition maps_ . These maps provide frameconsistent structural guidance for the subsequent video generation stage. 

## 3.3 GENERATION STAGE 

**Video Generation Model.** We adopt a DiT (Peebles & Xie, 2022) for video synthesis and introduce two targeted modifications. First, the conditioning **c** comprises third-person CLIP features together with text embeddings to modulate the DiT. Second, we modify the patch embedding to ingest the concatenated latent stream **Z** 0 = _{_ [ **z**<sup>_t_</sup> _w_<sup>;</sup><sup>**z**</sup><sup>_t_</sup> _c_<sup>]</sup><sup>_}T_</sup> _t_ =1 _∈_ R<sup>_T ×_2</sup><sup>_C×H×W_</sup> , expanding the standard input from ( _T, C, H, W_ ) to ( _T,_ 2 _C, H, W_ ). 


Figure 3: **Spatial Projection Consistency (SPC) loss.** We first establish anchor–wrist 2D point matching and then lift the matched pixels to 2D–3D correspondences using the reconstructed point cloud. The 3D points are subsequently projected into the wrist view with the predicted wrist pose, after which the SPC loss is computed to enforce geometric consistency. 

**Wrist-View-Projection-Guided Generation.** Since the projected condition maps are geometrically aligned with the wrist viewpoint, they directly provide spatial structure. We encode each wrist view projection **C**<sup>_t_</sup> into a latent representation **z**<sup>_t_</sup> _c_<sup>usingaVAE,andconcatenateitwiththenoisy</sup> wrist latent **z**<sup>_t_</sup> _w_<sup>:</sup> 


which is then processed by the video generation model. This integration allows the model to synthesize temporally coherent wrist-view sequences that remain consistent with 3D geometry. 

**CLIP-Encoded Anchor-View Semantics.** Because condition maps may miss global semantics (e.g., small or blurred objects from point-cloud projection), we introduce an external semantic pathway. Each third-person frame from _N_ anchor views is encoded by a CLIP image encoder to obtain per-frame, per-view features: 


where **e** _t,i_ denotes the CLIP embedding of the _t_ -th frame from the _i_ -th external view. 

A text prompt is also encoded, and both modalities are projected into a shared conditioning space: 


5 


Figure 4: **Visualization of our generation result.** As illustrated in the figure, we compare our generated condition maps against the 3D Base (VGGT without the SPC Loss), where our approach demonstrates superior viewpoint consistency. Furthermore, in comparison to the WoW 14B (Chi et al., 2025c) baseline which based on Wan 14B (Wan et al., 2025), our method achieves both higher generation quality and improved viewpoint alignment accuracy. These results highlight the effectiveness of our framework and underscore its potential to serve as training data for downstream VLA models. 

|Method|Wrist RGB||Dr|oid|||Franka|Panda||
|---|---|---|---|---|---|---|---|---|---|
||First Frame|FVD_↓_|LPIPS_↓_|SSIM_↑_|PSNR_↑_|FVD_↓_|LPIPS_↓_|SSIM_↑_|PSNR_↑_|
|VGGT (Wang et al., 2025b)|_×_|-|0.74|0.28|9.56|-|0.73|0.49|12.05|
|Pix2Pix (Isola et al., 2017)|_×_|-|0.55|0.58|12.81|-|0.58|0.71|15.60|
|WoW 1.3B (Chi et al., 2025c)|_×_|1142.15|0.61|0.46|10.08|1944.59|0.72|0.53|10.45|
|SVD (Blattmann et al., 2023)|✓|2005.44|0.56|0.50|11.12|1354.56|0.60|0.68|14.10|
|Cosmos-Predict2 (NVIDIA, 2025)|✓|1990.72|0.51|0.56|12.74|1156.69|0.65|0.67|12.59|
|WoW 14B (Chi et al., 2025c)|✓|935.03|0.53|0.54|11.98|985.99|0.59|0.68|13.93|
|**Ours**|_×_|**421.10**|**0.39**|**0.64**|**14.78**|**231.43**|**0.33**|**0.78**|**17.84**|


Table 1: Quantitative comparison on Droid and our Franka Panda. Green rows denote methods without wrist-view input, yellow rows require a wrist-view first frame, and red highlights our method. Our method achieves the best performance across all metrics without first-frame guidance. 

We then form the conditioning tokens by concatenating along the token dimension: 


where **p**<sup>1:</sup> temporal<sup>_T_are temporal embeddings,</sup><sup>**p**</sup> view<sup>1:</sup><sup>_N_are view-identity embeddings distinguishing the</sup><sup>_N_</sup> anchor views, which are both learnable parameters. And **p** text is a text-token positional embedding. The resulting **c** injects global semantics into the video generation process. 

# 4 EXPERIMENT 

## 4.1 IMPLEMENTATION DETAILS 

**Dataset.** We conduct experiments on three sources of data: 

1. **Droid (Khazatsky et al., 2024).** The _Droid_ dataset is a large-scale robotics video corpus with about 76k videos covering 59 diverse manipulation tasks. Each video is recorded at 1280 _×_ 720 resolution from multiple static viewpoints, including _ext1_ , _ext2_ , and a wrist-mounted camera. For pretraining, we sample a 10k subset and use two anchor views as model inputs. For evaluation, we additionally hold out 100 videos as a validation set. 

6 

|Method|Inputs|1/5|2/5|3/5|4/5|5/5|Avg. Len.|
|---|---|---|---|---|---|---|---|
|MDT (Reuss et al., 2024)|Static RGB + Gripper RGB|93.7%|84.5%|74.1%|64.4%|55.6%|3.72|
|HULC++ (Mees et al., 2023)|Static RGB + Gripper RGB|93%|79%|64%|52%|40%|3.30|
|VPP (Hu et al., 2024)|Static RGB + Gripper RGB|94.9%|86.8%|80.4%|72.9%|65.4%|4.00|
|SuSIE (Black et al., 2023)|Static RGB|87.7%|67.4%|49.8%|41.9%|33.7%|2.80|
|TaKSIE (Kang & Kuo, 2025)|Static RGB|90.4%|73.9%|61.7%|51.2%|40.8%|3.18|
|VPP + VGGT (Wang et al., 2025b)|Static RGB|91.8%|79.9%|65.4%|54.3%|44.1%|3.33|
|VPP|Static RGB|91.2%|82.2%|73.2%|65.2%|55.4%|3.67|
|**VPP + Ours**|Static RGB|**92.9%** _↑_1.7|**84.2%** _↑_2.0|**75.4%** _↑_2.2|**67.6%** _↑_2.4|**60.4%** _↑_5.0|**3.81** _↑_0.14|


Table 2: VLA performance on the Calvin (Mees et al., 2022) benchmark with and without wristview generation. We use the Video Prediction Policy (VPP) (Hu et al., 2024) as our VLA. In Calvin, each episode consists of five sequential tasks and terminates once a failure occurs. The columns 1/5–5/5 report success rates of completing at least _k_ tasks in sequence, while _Avg. Len._ denotes the mean number of tasks completed per episode. 

|Inputs|Close the upper drawer|Pick bread and place into drawer|Pick up the milk|Mean|
|---|---|---|---|---|
|Anchor + Wrist|80.0%|73.3%|46.7%|66.7%|
|Anchor|60.0%|40.0%|13.3%|37.8%|
|**Anchor + Ours Gen Wrist**|73.3% _↑_13.3|53.3% _↑_13.3|33.3% _↑_20.0|53.3% _↑_15.5|


Table 3: VLA performance on our Franka Panda dataset with and without wrist-view generation. 

2. **Calvin (Mees et al., 2022).** To benchmark vision-language-action learning in simulation, we adopt the _Calvin_ environment. Calvin provides multi-view demonstrations across multiple task splits; in this work we focus on the D split and use 10% of the data for training. For downstream VLA models, we follow the standard Task _D → D_ configuration for training and evaluation. 

3. **Franka Panda.** Beyond simulation, we collect 1700 demonstrations on a real Franka Panda manipulator. Our setup includes three static cameras ( _left_ , _right_ , _top_ ) and one wrist-view camera. Videos are captured at 30 fps and downsampled temporally by a factor of three. For evaluation, we hold out 100 videos from this collection. 

**Training.** Our framework is trained in two stages: reconstruction and video generation. During pretraining on the Droid dataset, the reconstruction stage is optimized on 8 _×_ A800 GPUs for 12 hours with a batch size of 4 and resolution of 640 _×_ 480, followed by the video generation stage on 8 _×_ A800 GPUs for 24 hours using a condition token length of 512. Building upon this, we perform cross-view fine-tuning with the Franka demonstrations. The reconstruction stage fine-tuning requires 8 GPUs for 6 hours, while the generation stage is trained on 8 GPUs for 12 hours under the same batch size, resolution, and token length settings. 

**Model.** Our framework consists of two stages: reconstruction and generation. In the _reconstruction stage_ , a VGGT backbone encodes multi-view features, and a dedicated _wrist head_ predicts wrist camera parameters through attention-based token fusion and transformer refinement, supervised by projection and optional L1 losses. In the _generation stage_ , We use the VAE (Kingma & Welling, 2013) compresses frames into latent sequences, while the DiT applies spatio-temporal attention on tokenized latents. Conditioned jointly on text and visual features, the DiT generates geometrically consistent and temporally coherent videos. 

- 4.2 VIDEO GENERATION QUANTITATIVE EVALUATION 

We compare against recent baselines on Droid and Franka-Panda (Tab. 1). Our method surpasses prior work across all metrics (FVD (Unterthiner et al., 2019), LPIPS (Zhang et al., 2018), SSIM (Wang et al., 2004), PSNR) without first-frame guidance, achieving large FVD gains (temporal coherence) and improved perceptual and structural fidelity. Even on the challenging Franka-Panda dataset with viewpoint variation, our framework consistently outperforms all baselines. 

Qualitative results are shown in Fig. 4, Fig. 5, and Fig. 6. In Fig. 4, our wrist view projection yield more viewpoint-aligned generations than both the 3D Base and WoW 14B. On Calvin (Fig. 5), our approach improves spatial/viewpoint consistency over SVD. On Franka Panda data (Fig. 6), our wrist-view generations closely match ground truth, showing strong third-to-wrist generalization. 

7 

|Wrist view Projection|Ext view clip embedding|SPC Loss|FVD_↓_|LPIPS_↓_|SSIM_↑_|PSNR_↑_|
|---|---|---|---|---|---|---|
|_×_|✓|_×_|3091.74|0.74|0.55|10.42|
|✓|✓|_×_|790.10|0.59|0.47|10.75|
|✓|_×_|✓|474.32|0.44|0.61|13.67|
|✓|✓|✓|**421.10**|**0.39**|**0.64**|**14.78**|


Table 4: Ablation on wrist view projection, clip embeddings, and SPC loss. 


Figure 5: **Visualization on the Calvin (Mees et al., 2022) benchmark.** We compare our generated wrist-view videos (bottom row) with the ground truth (second row) and a baseline method (third row, Stable Video Diffusion (Blattmann et al., 2023)). Our approach achieves better spatial and viewpoint consistency than the baseline, while also producing more faithful wrist-view frames. These results highlight the effectiveness of our method in bridging anchor-view and wrist-view perspectives. 

Together, these qualitative and quantitative results highlight that our generated videos not only serve as high-quality reconstructions but also provide valuable data for downstream VLA models. 

## 4.3 DATA-DRIVEN VLA ENHANCEMENT 

We evaluate whether synthesized wrist-view videos improve vision–language–action (VLA) policies. Our framework generates wrist-view sequences from _anchor-view_ rollouts and augments the training data of an unchanged VLA model (Video Prediction Policy, VPP (Hu et al., 2024)), without adding demonstrations, losses, or architectural changes. 

On Calvin, this augmentation increases average task completion length by _3.81%_ , narrows the anchor–wrist gap by **42.4%** , and improves full five-task completion by **5%** . These results show that wrist-view generation provides effective supervisory signals and yields measurable VLA gains without extra data collection. 

Similarly, on Franka-Panda demonstrations (Tab. 3), generated wrist views consistently improve task performance, confirming that the synthetic data is realistic and beneficial. Overall, wrist-view generation enriches robot datasets and yields measurable VLA gains. 

## 4.4 PLUG-AND-PLAY EXTENSION TO SINGLE-VIEW WORLD MODELS 

Our framework serves as a _plug-and-play_ add-on to an existing single-view world model (SVWM) while leaving the SVWM unchanged. In the baseline, the SVWM takes an _anchor-view first frame_ and predicts an _anchor-view_ rollout; with our module, that rollout is then converted into a temporally 

8 


Figure 6: **Visualization on Franka real-robot data.** Multiple input anchor views (left) are used to generate wrist-view sequences (top right), which are compared with ground-truth wrist observations (bottom right). Our approach yields highly consistent predictions that closely match real data, demonstrating strong generalization from third-view to wrist-view perspectives. 

|Method|Input|FVD_↓_|LPIPS_↓_|SSIM_↑_|PSNR_↑_|
|---|---|---|---|---|---|
|Ours|Left, right, top view videos|231.43|0.33|0.78|17.84|
|Ours|Left view videos|234.30|0.34|0.78|18.13|
|Cosmos|Wrist view first frame|1156.69|0.65|0.67|12.59|
|WoW 14B|Wrist view first frame|985.99|0.59|0.68|13.93|
|Ours + Cosmos|Left view first frame|467.19_↓_689.50|0.58_↓_0.07|0.70_↑_0.03|14.66_↑_2.07|
|Ours + WoW 14B|Left view first frame|**455.57**_↓_530.42|**0.57**_↓_0.02|**0.71**_↑_0.03|**14.60**_↑_0.67|


Table 5: **Plug-and-play extension to single-view world models.** Our framework enhances models trained solely on external viewpoints by synthesizing virtual wrist-view videos. We adopt CosmosPredict2 (NVIDIA, 2025) as the baseline Single-view World Model(SWM) and observe substantial gains. This plug-and-play design improves spatial consistency and perceptual quality across different baselines, while still delivering high-quality results with fewer anchor views. 

aligned _wrist-view_ video without wrist first frame required. This post-hoc wrist synthesis resolves the core hurdle for multi-view extension, namely cross-view consistency without wrist initialization, while enriching the observation space without additional data. As shown in Tab. 5, integrating our module with WoW (Chi et al., 2025c) improves spatial and perceptual fidelity, and the gains persis 

## 4.5 ABLATION STUDY 

We conduct an ablation study to disentangle the contribution of different components, as summarized in Tab. 4. The results show that the _wrist view projection_ plays the most critical role: removing it leads to a drastic drop in video quality, as reflected by a large increase in FVD and degraded perceptual metrics. Moreover, the SPC loss proves essential for ensuring that the condition map carries accurate guidance information; without it, the model struggles to align wrist-view synthesis with external observations. The combination of condition map, external-view embeddings, and tracking loss yields the best performance across all metrics. Although experiments without projection embeddings are still in progress, we estimate that their performance will be similarly poor, further reinforcing the necessity of projection-based conditioning for coherent multi-view generation. 

# 5 CONCLUSION 

In this work, we introduced **WristWorld** , a two-stage 4D framework for synthesizing geometrically and temporally consistent wrist-view videos from anchor-view inputs. In the reconstruction stage, 

9 

a wrist head and SPC loss augment a geometric transformer to estimate poses and generate condition maps without explicit wrist supervision. These maps are then fused with CLIP semantics and text guidance in a diffusion transformer, producing high-fidelity wrist-view sequences aligned with geometry and task semantics. 

Experiments on Calvin, Droid, and Franka Panda validate our framework: **WristWorld** achieves strong video generation across metrics and visual quality, while the synthesized wrist-view videos significantly boost downstream VLA learning. By augmenting datasets with wrist-centric views, **WristWorld** bridges the exocentric–egocentric gap and provides a scalable, data-driven solution for robotic training. 

# REFERENCES 

- Kevin Black, Mitsuhiko Nakamoto, Pranav Atreya, Homer Walke, Chelsea Finn, Aviral Kumar, and Sergey Levine. Zero-shot robotic manipulation with pretrained image-editing diffusion models. _arXiv preprint arXiv:2310.10639_ , 2023. 

- Andreas Blattmann, Tim Dockhorn, Sumith Kulal, Daniel Mendelevitch, Maciej Kilian, Dominik Lorenz, Yam Levi, Zion English, Vikram Voleti, Adam Letts, Varun Jampani, and Robin Rombach. Stable video diffusion: Scaling latent video diffusion models to large datasets, 2023. 

- Chi-Lam Cheang, Guangzeng Chen, Ya Jing, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Hongtao Wu, Jiafeng Xu, Yichu Yang, et al. Gr-2: A generative video-language-action model with webscale knowledge for robot manipulation. _arXiv preprint arXiv:2410.06158_ , 2024. 

- Xiaowei Chi, Chun-Kai Fan, Hengyuan Zhang, Xingqun Qi, Rongyu Zhang, Anthony Chen, ChiMin Chan, Wei Xue, Qifeng Liu, Shanghang Zhang, et al. Empowering world models with reflection for embodied video prediction. In _Forty-second International Conference on Machine Learning_ , 2025a. 

- Xiaowei Chi, Kuangzhi Ge, Jiaming Liu, Siyuan Zhou, Peidong Jia, Zichen He, Yuzhen Liu, Tingguang Li, Lei Han, Sirui Han, Shanghang Zhang, and Yike Guo. Mind: Learning a dualsystem world model for real-time planning and implicit risk analysis, 2025b. URL https: //arxiv.org/abs/2506.18897. 

- Xiaowei Chi, Peidong Jia, Chun-Kai Fan, Xiaozhu Ju, Weishi Mi, Kevin Zhang, Zhiyuan Qin, Wanxin Tian, Kuangzhi Ge, Hao Li, et al. Wow: Towards a world omniscient world model through embodied interaction. _arXiv preprint arXiv:2509.22642_ , 2025c. 

- Embodiment Collaboration, Abby O’Neill, Abdul Rehman, Abhinav Gupta, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, Albert Tung, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, Anant Rai, Anchit Gupta, Andrew Wang, Andrey Kolobov, Anikait Singh, Animesh Garg, Aniruddha Kembhavi, Annie Xie, Anthony Brohan, Antonin Raffin, Archit Sharma, Arefeh Yavary, Arhan Jain, Ashwin Balakrishna, Ayzaan Wahid, Ben Burgess-Limerick, Beomjoon Kim, Bernhard Schölkopf, Blake Wulfe, Brian Ichter, Cewu Lu, Charles Xu, Charlotte Le, Chelsea Finn, Chen Wang, Chenfeng Xu, Cheng Chi, Chenguang Huang, Christine Chan, Christopher Agia, Chuer Pan, Chuyuan Fu, Coline Devin, Danfei Xu, Daniel Morton, Danny Driess, Daphne Chen, Deepak Pathak, Dhruv Shah, Dieter Büchler, Dinesh Jayaraman, Dmitry Kalashnikov, Dorsa Sadigh, Edward Johns, Ethan Foster, Fangchen Liu, Federico Ceola, Fei Xia, Feiyu Zhao, Felipe Vieira Frujeri, Freek Stulp, Gaoyue Zhou, Gaurav S. Sukhatme, Gautam Salhotra, Ge Yan, Gilbert Feng, Giulio Schiavi, Glen Berseth, Gregory Kahn, Guangwen Yang, Guanzhi Wang, Hao Su, Hao-Shu Fang, Haochen Shi, Henghui Bao, Heni Ben Amor, Henrik I Christensen, Hiroki Furuta, Homanga Bharadhwaj, Homer Walke, Hongjie Fang, Huy Ha, Igor Mordatch, Ilija Radosavovic, Isabel Leal, Jacky Liang, Jad Abou-Chakra, Jaehyung Kim, Jaimyn Drake, Jan Peters, Jan Schneider, Jasmine Hsu, Jay Vakil, Jeannette Bohg, Jeffrey Bingham, Jeffrey Wu, Jensen Gao, Jiaheng Hu, Jiajun Wu, Jialin Wu, Jiankai Sun, Jianlan Luo, Jiayuan Gu, Jie Tan, Jihoon Oh, Jimmy Wu, Jingpei Lu, Jingyun Yang, Jitendra Malik, João Silvério, Joey Hejna, Jonathan Booher, Jonathan Tompson, Jonathan Yang, Jordi Salvador, Joseph J. Lim, Junhyek Han, Kaiyuan Wang, Kanishka Rao, Karl Pertsch, Karol Hausman, Keegan Go, Keerthana Gopalakrishnan, Ken Goldberg, Kendra Byrne, Kenneth Oslund, Kento Kawaharazuka, Kevin 

10 

Black, Kevin Lin, Kevin Zhang, Kiana Ehsani, Kiran Lekkala, Kirsty Ellis, Krishan Rana, Krishnan Srinivasan, Kuan Fang, Kunal Pratap Singh, Kuo-Hao Zeng, Kyle Hatch, Kyle Hsu, Laurent Itti, Lawrence Yunliang Chen, Lerrel Pinto, Li Fei-Fei, Liam Tan, Linxi "Jim" Fan, Lionel Ott, Lisa Lee, Luca Weihs, Magnum Chen, Marion Lepert, Marius Memmel, Masayoshi Tomizuka, Masha Itkina, Mateo Guaman Castro, Max Spero, Maximilian Du, Michael Ahn, Michael C. Yip, Mingtong Zhang, Mingyu Ding, Minho Heo, Mohan Kumar Srirama, Mohit Sharma, Moo Jin Kim, Muhammad Zubair Irshad, Naoaki Kanazawa, Nicklas Hansen, Nicolas Heess, Nikhil J Joshi, Niko Suenderhauf, Ning Liu, Norman Di Palo, Nur Muhammad Mahi Shafiullah, Oier Mees, Oliver Kroemer, Osbert Bastani, Pannag R Sanketi, Patrick "Tree" Miller, Patrick Yin, Paul Wohlhart, Peng Xu, Peter David Fagan, Peter Mitrano, Pierre Sermanet, Pieter Abbeel, Priya Sundaresan, Qiuyu Chen, Quan Vuong, Rafael Rafailov, Ran Tian, Ria Doshi, Roberto MartínMartín, Rohan Baijal, Rosario Scalise, Rose Hendrix, Roy Lin, Runjia Qian, Ruohan Zhang, Russell Mendonca, Rutav Shah, Ryan Hoque, Ryan Julian, Samuel Bustamante, Sean Kirmani, Sergey Levine, Shan Lin, Sherry Moore, Shikhar Bahl, Shivin Dass, Shubham Sonawani, Shubham Tulsiani, Shuran Song, Sichun Xu, Siddhant Haldar, Siddharth Karamcheti, Simeon Adebola, Simon Guist, Soroush Nasiriany, Stefan Schaal, Stefan Welker, Stephen Tian, Subramanian Ramamoorthy, Sudeep Dasari, Suneel Belkhale, Sungjae Park, Suraj Nair, Suvir Mirchandani, Takayuki Osa, Tanmay Gupta, Tatsuya Harada, Tatsuya Matsushima, Ted Xiao, Thomas Kollar, Tianhe Yu, Tianli Ding, Todor Davchev, Tony Z. Zhao, Travis Armstrong, Trevor Darrell, Trinity Chung, Vidhi Jain, Vikash Kumar, Vincent Vanhoucke, Vitor Guizilini, Wei Zhan, Wenxuan Zhou, Wolfram Burgard, Xi Chen, Xiangyu Chen, Xiaolong Wang, Xinghao Zhu, Xinyang Geng, Xiyuan Liu, Xu Liangwei, Xuanlin Li, Yansong Pang, Yao Lu, Yecheng Jason Ma, Yejin Kim, Yevgen Chebotar, Yifan Zhou, Yifeng Zhu, Yilin Wu, Ying Xu, Yixuan Wang, Yonatan Bisk, Yongqiang Dou, Yoonyoung Cho, Youngwoon Lee, Yuchen Cui, Yue Cao, Yueh-Hua Wu, Yujin Tang, Yuke Zhu, Yunchu Zhang, Yunfan Jiang, Yunshuang Li, Yunzhu Li, Yusuke Iwasawa, Yutaka Matsuo, Zehan Ma, Zhuo Xu, Zichen Jeff Cui, Zichen Zhang, Zipeng Fu, and Zipeng Lin. Open x-embodiment: Robotic learning datasets and rt-x models, 2025. 

Yanbo Ding, Xirui Hu, Zhizhi Guo, Chi Zhang, and Yali Wang. Mtvcrafter: 4d motion tokenization for open-world human image animation. _arXiv preprint arXiv:2505.10238_ , 2025. 

- Yilun Du, Sherry Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Josh Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning universal policies via text-guided video generation. _Advances in neural information processing systems_ , 36:9156–9172, 2023. 

- F. Ebert, C. Finn, A. X. Lee, and S. Levine. BAIR robot pushing dataset. Dataset, 2024. URL https://doi.org/10.57702/hpe85xky. Self-supervised visual planning with temporal skip connections. 

- Jonathan Ho and Tim Salimans. Classifier-free diffusion guidance, 2022. URL https://arxiv. org/abs/2207.12598. 

- Jie Hu, Shizun Wang, and Xinchao Wang. Pe3r: Perception-efficient 3d reconstruction. _arXiv preprint arXiv:2503.07507_ , 2025. 

- Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with predictive visual representations. _arXiv preprint arXiv:2412.14803_ , 2024. 

- Siyuan Huang, Liliang Chen, Pengfei Zhou, Shengcong Chen, Zhengkai Jiang, Yue Hu, Yue Liao, Peng Gao, Hongsheng Li, Maoqing Yao, et al. Enerverse: Envisioning embodied future space for robotics manipulation. _arXiv preprint arXiv:2501.01895_ , 2025. 

- Phillip Isola, Jun-Yan Zhu, Tinghui Zhou, and Alexei A Efros. Image-to-image translation with conditional adversarial networks. _CVPR_ , 2017. 

- Vidhi Jain, Maria Attarian, Nikhil J Joshi, Ayzaan Wahid, Danny Driess, Quan Vuong, Pannag R Sanketi, Pierre Sermanet, Stefan Welker, Christine Chan, et al. Vid2robot: End-to-end videoconditioned policy learning with cross-attention transformers. _arXiv preprint arXiv:2403.12943_ , 2024. 

11 

- Joel Jang, Seonghyeon Ye, Zongyu Lin, Jiannan Xiang, Johan Bjorck, Yu Fang, Fengyuan Hu, Spencer Huang, Kaushil Kundalia, Yen-Chen Lin, et al. Dreamgen: Unlocking generalization in robot learning through neural trajectories. _arXiv e-prints_ , pp. arXiv–2505, 2025. 

- Xuhui Kang and Yen-Ling Kuo. Incorporating task progress knowledge for subgoal generation in robotic manipulation through image edits. In _2025 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)_ , pp. 7490–7499. IEEE, 2025. 

- Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 

- Diederik P Kingma and Max Welling. Auto-encoding variational bayes. _arXiv preprint arXiv:1312.6114_ , 2013. 

- Ying Li, Xiaobao Wei, Xiaowei Chi, Yuming Li, Zhongyu Zhao, Hao Wang, Ningning Ma, Ming Lu, and Shanghang Zhang. Manipdreamer3d : Synthesizing plausible robotic manipulation video with occupancy-aware 3d trajectory, 2025. URL https://arxiv.org/abs/2509.05314. 

- Yue Liao, Pengfei Zhou, Siyuan Huang, Donglin Yang, Shengcong Chen, Yuxin Jiang, Yue Hu, Jingbin Cai, Si Liu, Jianlan Luo, Liliang Chen, Shuicheng Yan, Maoqing Yao, and Guanghui Ren. Genie envisioner: A unified world foundation platform for robotic manipulation, 2025. URL https://arxiv.org/abs/2508.05635. 

- Jia-Wei Liu, Weijia Mao, Zhongcong Xu, Jussi Keppo, and Mike Zheng Shou. Exocentric-toegocentric video generation. _Advances in Neural Information Processing Systems_ , 37:136149– 136172, 2024. 

- Jianlan Luo, Charles Xu, Jeffrey Wu, and Sergey Levine. Precise and dexterous robotic manipulation via human-in-the-loop reinforcement learning. _Science Robotics_ , 10(105):eads5033, 2025. 

- Yunhao Luo and Yilun Du. Grounding video models to actions through goal conditioned exploration. _arXiv preprint arXiv:2411.07223_ , 2024. 

- Ajay Mandlekar, Yuke Zhu, Animesh Garg, Jonathan Booher, Max Spero, Albert Tung, Julian Gao, John Emmons, Anchit Gupta, Emre Orbay, Silvio Savarese, and Li Fei-Fei. Roboturk: A crowdsourcing platform for robotic skill learning through imitation. _CoRR_ , abs/1811.02790, 2018. URL http://arxiv.org/abs/1811.02790. 

- Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7(3):7327–7334, 2022. 

- Oier Mees, Jessica Borja-Diaz, and Wolfram Burgard. Grounding language with visual affordances over unstructured data. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , London, UK, 2023. 

- NVIDIA. Cosmos-predict2: World foundation models for physical ai. GitHub repository, 2025. URL https://github.com/nvidia-cosmos/cosmos-predict2. 

- William Peebles and Saining Xie. Scalable diffusion models with transformers. _arXiv preprint arXiv:2212.09748_ , 2022. 

- Han Qi, Haocheng Yin, Aris Zhu, Yilun Du, and Heng Yang. Strengthening generative robot policies through predictive world modeling. _arXiv preprint arXiv:2502.00622_ , 2025. 

- Moritz Reuss, Ömer Erdinç Ya˘gmurlu, Fabian Wenzel, and Rudolf Lioutikov. Multimodal diffusion transformer: Learning versatile behavior from multimodal goals. _arXiv preprint arXiv:2407.05996_ , 2024. 

- Achint Soni, Sreyas Venkataraman, Abhranil Chandra, Sebastian Fischmeister, Percy Liang, Bo Dai, and Sherry Yang. Videoagent: Self-improving video generation for embodied planning. In _Workshop on Reinforcement Learning Beyond Rewards@ Reinforcement Learning Conference 2025_ , 2025. 

12 

- Thomas Unterthiner, Sjoerd van Steenkiste, Karol Kurach, Raphael Marinier, Marcin Michalski, and Sylvain Gelly. Towards accurate generative models of video: A new metric & challenges, 2019. URL https://arxiv.org/abs/1812.01717. 

- Team Wan, Ang Wang, Baole Ai, Bin Wen, Chaojie Mao, Chen-Wei Xie, Di Chen, Feiwu Yu, Haiming Zhao, Jianxiao Yang, Jianyuan Zeng, Jiayu Wang, Jingfeng Zhang, Jingren Zhou, Jinkai Wang, Jixuan Chen, Kai Zhu, Kang Zhao, Keyu Yan, Lianghua Huang, Mengyang Feng, Ningyi Zhang, Pandeng Li, Pingyu Wu, Ruihang Chu, Ruili Feng, Shiwei Zhang, Siyang Sun, Tao Fang, Tianxing Wang, Tianyi Gui, Tingyu Weng, Tong Shen, Wei Lin, Wei Wang, Wei Wang, Wenmeng Zhou, Wente Wang, Wenting Shen, Wenyuan Yu, Xianzhong Shi, Xiaoming Huang, Xin Xu, Yan Kou, Yangyu Lv, Yifei Li, Yijing Liu, Yiming Wang, Yingya Zhang, Yitong Huang, Yong Li, You Wu, Yu Liu, Yulin Pan, Yun Zheng, Yuntao Hong, Yupeng Shi, Yutong Feng, Zeyinzi Jiang, Zhen Han, Zhi-Fan Wu, and Ziyu Liu. Wan: Open and advanced large-scale video generative models, 2025. 

- Boyang Wang, Nikhil Sridhar, Chao Feng, Mark Van der Merwe, Adam Fishman, Nima Fazeli, and Jeong Joon Park. This&that: Language-gesture controlled video generation for robot planning. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 12842–12849. IEEE, 2025a. 

- Chen Wang, Linxi Fan, Jiankai Sun, Ruohan Zhang, Li Fei-Fei, Danfei Xu, Yuke Zhu, and Anima Anandkumar. Mimicplay: Long-horizon imitation learning by watching human play. _arXiv preprint arXiv:2302.12422_ , 2023. 

- Jianyuan Wang, Minghao Chen, Nikita Karaev, Andrea Vedaldi, Christian Rupprecht, and David Novotny. Vggt: Visual geometry grounded transformer. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2025b. 

- Jiayu Wang, Aws Albarghouthi, and Frederic Sala. Cosmos: Predictable and cost-effective adaptation of llms, 2025c. URL https://arxiv.org/abs/2505.01449. 

- Shizun Wang, Xingyi Yang, Qiuhong Shen, Zhenxiang Jiang, and Xinchao Wang. Gflow: Recovering 4d world from monocular video. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, pp. 7862–7870, 2025d. 

- Zhou Wang, A.C. Bovik, H.R. Sheikh, and E.P. Simoncelli. Image quality assessment: from error visibility to structural similarity. _IEEE Transactions on Image Processing_ , 13(4):600–612, 2004. doi: 10.1109/TIP.2003.819861. 

- Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. Unleashing large-scale video generative pre-training for visual robot manipulation. _arXiv preprint arXiv:2312.13139_ , 2023. 

- Mengjiao Yang, Yilun Du, Kamyar Ghasemipour, Jonathan Tompson, Dale Schuurmans, and Pieter Abbeel. Learning interactive real-world simulators. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2023. 

- Yanjie Ze, Ge Yan, Yueh-Hua Wu, Annabella Macaluso, Yuying Ge, Jianglong Ye, Nicklas Hansen, Li Erran Li, and Xiaolong Wang. Multi-task real robot learning with generalizable neural feature fields. _CoRL_ , 2023. 

- Richard Zhang, Phillip Isola, Alexei A. Efros, Eli Shechtman, and Oliver Wang. The unreasonable effectiveness of deep features as a perceptual metric, 2018. URL https://arxiv.org/abs/ 1801.03924. 

- Haoyu Zhen, Qiao Sun, Hongxin Zhang, Junyan Li, Siyuan Zhou, Yilun Du, and Chuang Gan. Tesseract: Learning 4d embodied world models. arXiv preprint arXiv:2504.20995, 2025. URL https://arxiv.org/abs/2504.20995. Preprint. 

- Siyuan Zhou, Yilun Du, Jiaben Chen, Yandong Li, Dit-Yan Yeung, and Chuang Gan. Robodreamer: Learning compositional world models for robot imagination. _arXiv preprint arXiv:2404.12377_ , 2024. 

13 

# A APPENDIX 

## A.1 DATASETS 

**Calvin.** The Calvin benchmark (Mees et al., 2022) ( _Composing Actions from Language and Vision_ ) is a simulated environment designed for studying long-horizon, language-conditioned robotic manipulation. It defines a set of five core manipulation tasks— _opening and closing drawers, switching lights, placing objects in containers, pushing blocks, and rotating knobs_ —which can be composed into multi-step instructions. Each demonstration is collected via teleoperation in simulation and includes synchronized RGB observations from multiple static cameras, robot states, low-level actions, and the corresponding language command. The benchmark further provides different environment variations, enabling controlled evaluations of generalization to new objects, layouts, and task compositions. CALVIN thus serves as a standardized testbed to validate whether synthesized wrist-view videos can enhance task-conditioned learning in a controlled simulation setting. 

**Droid.** The Droid dataset (Khazatsky et al., 2024) ( _Distributed Robot Interaction Dataset_ ) is one of the largest collections of real-world robotic demonstrations. It contains approximately 76k trajectories spanning 350 hours, collected across 564 unique scenes and 86 manipulation tasks by over 50 contributors from multiple institutions. To ensure consistency, each robot setup follows a unified configuration: a Franka Panda 7-DoF manipulator, two ZED 2 stereo cameras for external anchor views, and a ZED Mini wrist-mounted camera for egocentric observations, along with standardized calibration. Each trajectory records synchronized multi-view RGB-D streams, camera intrinsics and extrinsics, joint states, and control commands. The scale and diversity of DROID make it a challenging but rich source of anchor-view data, while the presence of a dedicated wrist camera offers an opportunity to validate generated views against ground-truth egocentric observations. 

**Franka Panda demonstrations.** To further evaluate our method on a controlled real-robot setup, we collected a dataset of _∼_ 1.7 k demonstrations using a Franka Panda manipulator. The hardware setup mirrors that of DROID, with multiple fixed anchor cameras and a wrist-mounted camera, but data collection was conducted entirely in-house. Demonstrations span diverse manipulation skills such as grasping, transporting, and placing objects under natural occlusions from the robot arm. For each sequence, we log synchronized anchor-view and wrist-view videos, as well as proprioceptive states and control commands. While smaller in scale than DROID, this dataset captures calibration imperfections and actuation variability, making it particularly valuable for fine-tuning and validating wrist-view generation under true physical dynamics. 

## A.2 TRAINING AND IMPLEMENTATION DETAILS 

This section provides the full setup for both stages of **WristWorld** in the 1.3B configuration, with emphasis on novel components and implementation details. We also include short explanations of key terms to aid readers unfamiliar with video generation or geometric reconstruction. 

**Implementation Details.** The **wrist head** is implemented as a lightweight transformer decoder with 3 layers, 8 attention heads per layer, and an embedding dimension of 1024. It attends to aggregated multi-view tokens from VGGT and directly regresses wrist camera extrinsics ( **R** _w,_ **T** _w_ ). 

The **Spatial Projection Consistency (SPC) loss** is computed using dense 2D–2D correspondences. For each 3D point **y** ˆ _j_ , we project it into the wrist view as 


where **K** is the dataset-provided intrinsics. We then split the projected points into _S_ front = _{_ **y** ˆ _j | zj >_ 0 _}_ and _S_ back = _{_ **y** ˆ _j | zj <_ 0 _}_ , with _zj_ denoting the depth value in the wrist frame. The loss is defined as 


and _L_ proj = _λuLu_ + _λ_ depth _L_ depth. 

14 

For video generation, we use **wrist-view projections** as conditioning inputs. Each frame is encoded by a VAE into latents _zc_<sup>_t_and concatenated with the noisy wrist-view latents</sup><sup>_z_</sup> _w_<sup>_t_.The patch embed-</sup> ding of the DiT is modified from a standard 2 _×_ 2 convolution, expanding input channels to 32 to accommodate concatenated latents. CLIP features from anchor views are projected from 512 dimensions into the DiT token space, while text embeddings from T5 are 4096-dimensional. Temporal and view embeddings are added to capture sequence alignment and camera identity. 

**Reconstruction stage (VGGT + Wrist Head).** We adopt VGGT-1B with point, depth, and camera heads (frozen) and train a new wrist head. Training images are resized to 518 _×_ 518, and intrinsics are scaled accordingly. Two anchor views ( _ext1_ , _ext2_ ) are inputs, and the wrist pose is predicted relative to _ext1_ . SPC loss enforces consistency: visible points are supervised with normalized reprojection error, while back-facing points are penalized if their predicted depth is negative. 

|Component|Setting|
|---|---|
|Backbone|VGGT-1B|
|Image size|518_×_518|
|Token aggregation|Attention-based|
|Wrist decoder|3 layers, 8 heads|
|Optimizer|AdamW (wd = 0.05)|
|Learning rate|2_×_10<sup>_−_5 </sup>(cosine decay)|
|Batch size|4 per GPU, grad accum = 3|
|Hardware|8_×_A800 GPUs|
|Training time|_∼_12h pretrain, 6h finetune|


Table 6: Reconstruction stage hyperparameters. 

**Generation stage (Video DiT).** We build on Wan 1.3B DiT, which is a diffusion transformer pretrained for text-to-video. Condition maps are encoded with a VAE and concatenated with noisy wrist-view latents. CLIP embeddings from anchor views are projected into the text space and added as pseudo tokens, together with temporal and view embeddings. A maximum of 512 conditioning tokens is used. Classifier-Free Guidance (CFG) is set to 5.0. 

|Component|Setting|
|---|---|
|Backbone|Wan 1.3B DiT|
|Resolution|640_×_480(latent scale 1/8)|
|Patch in-channels|Expanded to 32 (for concat latents)|
|LoRA config|Rank 4,_α_= 4, targets {q,k,v,o,ffn}|
|Condition tokens|512 total (CLIP + text + temporal/view)|
|CFG|5.0|
|Optimizer|AdamW, lr= 1_×_10<sup>_−_5</sup>|
|Batch size|4 per GPU|
|Hardware|8_×_A800 GPUs|
|Training time|_∼_24h pretrain, 12h finetune|


Table 7: Generation stage hyperparameters. 

## A.3 VISUALIZATION 

To assess appearance fidelity and viewpoint stability under realistic manipulation, we run inference on a **Franka Panda** platform for all compared video generation methods, including ours, using identical input trajectories and pre-processing. For each generated clip, we visualize the _middle frame_ so as to emphasize long-horizon behavior and to minimize the bias introduced by the initial condition. The compared models comprise _Pix2Pix_ (Isola et al., 2017), _SVD_ (Blattmann et al., 2023), _Wan 1.3B_ (Wan et al., 2025), _Wan 14B_ , _Cosmos-Predict2_ (NVIDIA, 2025), and **Ours** . Following common practice for controllable synthesis, **SVD** , **Wan 14B** , and **Cosmos-Predict2** are evaluated 

CFG balances diversity and fidelity in diffusion sampling by mixing conditional and unconditional generations. A higher value yields sharper but less diverse outputs (Ho & Salimans, 2022). 

15 


Figure 7: **Qualitative visualization on Franka Panda.** For each method, we generate videos and visualize the _middle frame_ of each sequence to probe long-horizon stability. **Rows** denote methods (the top row shows ground-truth wrist-camera frames), and **columns** denote different manipulation scenes from the Franka Panda setup. Our approach maintains superior geometric consistency (crisp boundaries, coherent occlusions, stable perspective/scale) and wrist-following behavior (viewpoint motion aligned with end-effector motion and consistent object-relative poses) compared with prior models. 

with _first-frame guidance_ , while the remaining methods use their public default settings. Qualitative results are shown in Fig. 7. 

Across diverse scenes, our method exhibits the strongest **geometric consistency** and **wristfollowing capability** . By geometric consistency we refer to coherent object shapes and boundaries, stable perspective and scale, and physically plausible occlusions (e.g., hand–object and object–table contacts). By wrist-following we mean that the synthesized wrist-camera view remains aligned with the end-effector motion, yielding stable object-relative poses and camera parallax over time. In contrast, baselines frequently suffer from accumulated drift in the middle of the sequence: textures smear or dissolve, straight edges warp, object scale fluctuates, and the rendered viewpoint decouples from the manipulator pose, producing noticeable misalignment between the camera motion and the underlying action. Methods that rely on first-frame guidance preserve appearance early on but tend to exhibit background and pose drift as the sequence proceeds; methods without guidance avoid overfitting to the first frame but often display ghosting and fine-detail loss under fast motions or partial occlusions. While our approach may still blur very small, fast-moving details in rare cases, its overall spatial coherence and camera–motion coupling are substantially more reliable, which agrees with the improvements observed in video quantitative metrics. 

## A.4 FRANKA PANDA SETTING 

As shown in Figure. 8, we employ a Franka Emika Panda manipulator in our experimental setup, augmented with multiple Intel RealSense cameras to provide diverse visual perspectives. Specifically, a wrist-mounted camera enables close-up views of the manipulation workspace, while a topmounted camera captures overhead information. In addition, left and right side cameras provide 

16 

complementary viewpoints for robust perception. This multi-view sensing arrangement facilitates both accurate 3D reconstruction and reliable visual feedback for manipulation tasks. 


Figure 8: Experimental setup with the Franka Panda manipulator. The system is equipped with multiple Intel RealSense cameras: wrist-mounted, top, left, and right. This configuration enables multi-view visual input for robust perception and manipulation. 

17 

