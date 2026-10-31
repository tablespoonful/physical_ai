---
title: "BridgeV2W: Bridging Video Generation Models to Embodied World Models via Embodiment Masks"
date: "2026-02-03"
authors: "Yixiang Chen; Peiyan Li; Jiabing Yang; Keji He; Xiangnan Wu; Yuan Xu"
venue: "ICLR 2026 Conference Withdrawn Submission"
url: https://arxiv.org/abs/2602.03793
pdf: https://arxiv.org/pdf/2602.03793
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.03793)** / [論文ページ](https://arxiv.org/abs/2602.03793)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**BridgeV2W: Bridging Video Generation Models to Embodied World Models via Embodiment Masks** 

**Yixiang Chen**<sup>1 2</sup> **Peiyan Li**<sup>1 2</sup> **Jiabing Yang**<sup>1 2</sup> **Keji He**<sup>3</sup> **Xiangnan Wu**<sup>1</sup> **Yuan Xu**<sup>1 2</sup> **Kai Wang**<sup>1</sup> **Jing Liu**<sup>4</sup> **Nianfeng Liu**<sup>4</sup> **Yan Huang**<sup>124</sup><sup>_†_</sup> **Liang Wang**<sup>12</sup><sup>_†_</sup> 

# **1. Introduction** 

# **Abstract** 

Embodied world models have emerged as a promising paradigm in robotics, most of which leverage large-scale Internet videos or pretrained video generation models to enrich visual and motion priors. However, they still face key challenges: a misalignment between coordinate-space actions and pixel-space videos, sensitivity to camera viewpoint, and non-unified architectures across embodiments. To this end, we present **BridgeV2W** , which converts coordinate-space actions into pixel-aligned embodiment masks rendered from the URDF and camera parameters. These masks are then injected into a pretrained video generation model via a ControlNet-style pathway, which aligns the action control signals with predicted videos, adds view-specific conditioning to accommodate camera viewpoints, and yields a unified world model architecture across embodiments. To mitigate overfitting to static backgrounds, BridgeV2W further introduces a flow-based motion loss that focuses on learning dynamic and task-relevant regions. Experiments on single-arm (DROID) and dual-arm (AgiBotG1) datasets, covering challenging conditions with unseen viewpoints and scenes, show that BridgeV2W improves video generation quality compared to prior state-of-the-art methods. We further demonstrate the potential of BridgeV2W on downstream real-world tasks, including policy evaluation and goal-conditioned planning. More results can be found on our project website: https://BridgeV2W.github.io. 

_†_ Corresponding Authors. 

> 1New Laboratory of Pattern Recognition (NLPR), Institute of Automation, Chinese Academy of Sciences<sup>2</sup> School of Artificial Intelligence, University of Chinese Academy of Sciences<sup>3</sup> Shandong University<sup>4</sup> FiveAges. Correspondence to: Yixiang Chen _<_ yixiang.chen@cripac.ia.ac.cn _>_ , Yan Huang _<_ yhuang@nlpr.ia.ac.cn _>_ , Liang Wang _<_ wangliang@nlpr.ia.ac.cn _>_ . 

_Preprint. February 4, 2026._ 

Embodied world models have gained increasing attention in the robotics community for their ability to model the physical dynamics of the environment. They support policy evaluation by simulating counterfactual action outcomes (Jiang et al., 2025; Li et al., 2025e; 1X World Model Team, 2025) and goal-conditioned planning by forecasting future states toward specified goal images (Assran et al., 2025; Bar et al., 2025; Baldassarre et al., 2025; Bai et al., 2025). Despite this potential, current embodied world models remain constrained by limited task-relevant data and mismatched design (i.e., coordinate-space actions misaligned with the pixel-space videos). 

Current research on action-conditioning embodied world models generally follows two main paradigms. The first trains models from scratch using only domain-specific robot data. While effective within the same domain, such models often fail to generalize well to unseen scenarios. The second paradigm leverages large-scale Internet videos to incorporate rich visual and motion priors, either by directly pretraining a model or by fine-tuning a pretrained video generation model with action conditioning. Although notable progress has been made, these approaches still suffer from several key limitations, as outlined in Figure 1: 

(1) **Action-Video Gap** : Most action-conditioning methods represent the end-effector poses as coordinate-space actions that lie in a low-dimensional geometric space, whereas pretrained video generation models operate in a high-dimensional pixel space. This representation space mismatch weakens conditioning and limits the reuse of pretrained visual and motion priors. (2) **Viewpoint Sensitivity** : Coordinate-space actions are highly sensitive to camera viewpoint changes. Even for the same action, existing methods still struggle to generate reasonable future states when the camera viewpoint varies, limiting their applicability in unseen camera viewpoint settings. (3) **Non-Unified Architecture Across Embodiments** : These methods lack a unified architecture across robot embodiments. For instance, single-arm and dual-arm systems have different degrees of freedom and typically require separate action encoders, which limits knowledge transfer across embodiments and 

1 

**Bridging Video Generation to Embodied World Models** 


_Figure 1._ BridgeV2W vs. previous methods. Pixel-aligned embodiment masks bridge video generation models to embodied world models, addressing the action–video gap, improving viewpoint robustness, and yielding a unified architecture across embodiments. 

hinders the scalability required for building truly generalpurpose embodied world models. 

We start from a simple observation: **if we transform the action representation into a pixel-aligned mask that reflects the embodiment’s actual motion, the issues mentioned above can be substantially mitigated.** In particular, projecting actions into pixel-aligned masks (i) closes the gap to pixel-space of pretrained video generation models because _the conditioning also lies in pixel space_ , (ii) facilitates viewconditioned robustness across diverse camera viewpoints because _supervision is anchored in the image plane_ , and (iii) unifies action conditioning across embodiments because _the mask is agnostic to robot-specific action space_ . 

To this end, we propose **BridgeV2W** , a framework that bridges pretrained video generation models to embodied world models via embodiment masks. We leverage the robot’s Unified Robot Description Format (URDF), which is easy to obtain and widely available, together with the camera’s intrinsic and extrinsic parameters to render actions into view-specific embodiment masks. These masks encode the embodiment’s structure in pixel space, providing a spatial conditioning signal to pretrained video generation models. Inspired by ControlNet-style conditioning (Zhang et al., 2023), we inject these masks as spatial conditions into the pretrained video generation models, enabling actionconditioned generation while preserving their pretrained visual and motion priors. These pixel-aligned mask actions match the pixel space of the pretrained video generation model, preserve viewpoint-specific variation, and enable a unified world model architecture across embodiments. 

While the above design already enables BridgeV2W to provide effective action conditioning, conventional frame-level 

reconstruction losses reconstruct all regions without distinction, including most task-irrelevant ones. For robotic manipulation, it is more effective to focus on motion regions, including the embodiment and manipulated objects. Thus, we further introduce a flow-based motion loss that computes optical flow between predicted and ground-truth frames. By penalizing discrepancies only in motion regions, BridgeV2W focuses more on task-relevant motion patterns rather than static background details. 

Our main contributions can be summarized as follows: 

- We present BridgeV2W, a framework that bridges pretrained video generation models to embodied world models via embodiment masks. Using a ControlNetstyle conditioning mechanism, BridgeV2W preserves pretrained visual and motion priors while enabling viewpoint robustness and a unified architecture across embodiments, and supports training with uncalibrated and actionless video data by decoupling supervision from precise geometric calibration. 

- We introduce a flow-based motion loss that encourages the model learning toward task-relevant areas of the embodiment and manipulated objects, reducing emphasis on static background reconstruction. 

- We evaluate BridgeV2W on single-arm (DROID (Khazatsky et al., 2024)) and dual-arm (AgiBot-G1 (Bu et al., 2025)) datasets, covering unseen viewpoints and scenes, and demonstrate enhanced generation quality compared to previous state-of-the-art methods. We further validate BridgeV2W on downstream robotic tasks: as a proxy for policy evaluation, it shows strong correlation with real-world success, and as a goalimage–conditioned planner, it achieves promising manipulation performance. 

2 

**Bridging Video Generation to Embodied World Models** 

# **2. Related Works** 

## **2.1. Learning World Models via Video Generation** 

Existing approaches that adopt video generation models as embodied world models can be broadly divided into two categories. The first directly trains a video generation model from scratch using domain-specific robot data (Jiang et al., 2025; Liao et al., 2025; Bai et al., 2025; Wang et al., 2025b; Chen et al., 2025; Zhu et al., 2024; Wu et al., 2024), learning environment dynamics purely from task demonstrations. While such models can accurately capture the physics and visual patterns of the training domain, their reliance on limited and task-specific data often leads to overfitting, resulting in poor generalization to unseen scenarios. 

The second category leverages large-scale Internet videos or pretrained video generation models to incorporate rich visual and motion priors (He et al., 2025; Agarwal et al., 2025; Assran et al., 2025; 1X World Model Team, 2025; Huang et al., 2025). A common strategy is to fine-tune these models by introducing action conditioning. This paradigm benefits from the diversity and scale of pretraining data, making it more adaptable to varied visual scenes. However, existing methods still suffer from several limitations, including the mismatch between coordinate-space actions and pixel-space videos, sensitivity to camera viewpoint changes, and the lack of a unified architecture for different robot embodiments. In contrast, our BridgeV2W integrates embodiment masks into a pretrained video generation model via a ControlNet-style conditioning mechanism, enabling robust multi-view generation, architecture sharing across embodiments, and better alignment between action inputs and the model’s visual priors. 

## **2.2. Injecting Conditions into Pretrained Models** 

ControlNet (Zhang et al., 2023) extends diffusion-based generative models (Rombach et al., 2022) by introducing additional condition-encoding branches that start with zeroinitialized parameters. This design ensures that the pretrained network’s behavior remains unchanged at the beginning of fine-tuning, while gradually learning to incorporate new guidance signals such as sketches, depth maps, or human poses. These conditioning mechanisms provide a natural interface for injecting structured, spatially grounded signals into pretrained models. In both image (Li et al., 2024) and video generation (Guo et al., 2024; Wang et al., 2024b; Bar-Tal et al., 2024) fields, prior works employ ControlNetstyle conditioning to guide generation with diverse control signals, including optical flow (Li et al., 2025d; Shi et al., 2024; Zhang et al., 2025; Yin et al., 2023), bounding boxes (Li et al., 2025b; Namekata et al., 2025; Qiu et al., 2024; Wang et al., 2024a), and point trajectories (Fu et al., 2024; Gu et al., 2025; Wang et al., 2025a;c). In BridgeV2W, we adapt this conditioning strategy to inject embodiment masks 

into a pretrained video generation model, and we further introduce flow-based loss to focus more on task-relevant areas, including embodiments and manipulated objects. 

# **3. BridgeV2W Framework** 

## **3.1. Definition of Embodied World Models** 

The term _world model_ has been broadly discussed in previous works (e.g., latent dynamic predictors or pure video generators without actions). In this paper, we adopt an operational, action-conditioned definition of embodied world models that requires _an initial frame and an action sequence as inputs_ and _an RGB video as output_ . Crucially, the predicted video is expected to reflect the physical consequences of the input actions under a specific embodiment. Given an initial RGB frame _I_ 0 _∈_ R<sup>_H×W ×_3</sup> and an action sequence **a** 0: _T −_ 1, the model _fθ_ predicts the future frames 


where _T_ is the video length and _V_ ≜ _I_ 0: _T_ . The action space _A_ is embodiment- and parameterization-agnostic: we allow _N_ manipulators with _A_ ≜ _A_<sup>(1)</sup> _× · · · × A_<sup>(</sup><sup>_N_)</sup> and _at_ ≜ [ _a_<sup>(1)</sup> _t_<sup>;</sup><sup>_. . ._;</sup><sup>_a_(</sup> _t_<sup>_N_)</sup> ], where each manipulator’s action _a_<sup>(</sup> _t_<sup>_n_)</sup> may be specified either in Cartesian space, _a_<sup>(</sup> _t_<sup>_n_)</sup> = ( _p_<sup>(</sup> _t_<sup>_n_)</sup> _, Rt_<sup>(</sup><sup>_n_)</sup> _, gt_<sup>(</sup><sup>_n_)</sup> ) with _p_<sup>(</sup> _t_<sup>_n_)</sup> _∈_ R<sup>3</sup> , _Rt_<sup>(</sup><sup>_n_)</sup> _∈_ SO(3), and gripper control _gt_<sup>(</sup><sup>_n_)</sup> ; or in joint space, _a_<sup>(</sup> _t_<sup>_n_)</sup> = _qt_<sup>(</sup><sup>_n_)</sup> _∈_ R<sup>_dn_</sup> , with _dn_ the number of actuated joints. Our definition does not prescribe a particular architecture or training objective; thus, any model that maps an initial frame and an action sequence to the corresponding RGB video qualifies as an embodied world model under this definition. 

## **3.2. Embodiment Mask Extraction from Actions** 

To extract embodiment masks from action sequences, we use a URDF description of the embodiment and simulate its motion via forward dynamics to recover its 3D structure. With known camera intrinsics and extrinsics, the embodiment is projected onto the image plane, yielding a per-frame mask _mt_ from the camera’s viewpoint. We align masks to the predicted frames and denote the mask sequence as _M_ ≜ _{mt}_<sup>_T_</sup> _t_ =1<sup>.This ensures that each action</sup><sup>_at_is consis-</sup> tently paired with its associated mask _mt_ , producing tuples ( _I_ 0 _, M, V_ 1: _T_ ). 

The pipeline is extensible to settings without explicit action annotations or camera calibration, e.g., human–hand interaction videos (Goyal et al., 2017; Grauman et al., 2022). In such cases, segmentation tools like GroundedSAM (Ren et al., 2024) can be used to directly extract _M_ from raw video, also enabling datasets of the form ( _I_ 0 _, M, V_ 1: _T_ ). This highlights the flexibility of our framework and its ability to integrate embodiment signals from diverse sources. Additional details are provided in the Experiments section. 

3 

**Bridging Video Generation to Embodied World Models** 


_Figure 2._ Overview of the BridgeV2W pipeline. Actions are projected into pixel-space masks using URDF and camera parameters. The initial image and mask sequence are encoded by VAE, with mask features injected via a ControlNet branch into the DiT backbone. The model generates action-consistent videos, trained with diffusion, dynamics-consistency, and flow-based objectives. 

## **3.3. ControlNet-Based Video Generation** 

The overall pipeline of BridgeV2W is illustrated in Figure 2. We adopt CogVideoX-5B-I2V (Yang et al., 2025c) as the image-to-video backbone, which utilizes 3D full attention to capture high-quality temporal dynamics. Given an input image _I_ 0 _∈_ R<sup>_H×W ×_3</sup> and a target video _V ∈_ R<sup>_T ×H×W ×_3</sup> , a pretrained 3D VAE (Kingma & Welling, 2013) encodes them into latent tensors 


The image latent _z_<sup>_img_</sup> is zero-padded along the temporal axis to length _Tℓ_ and concatenated with a noised version of the video latent tensors (see diffusion below). A Diffusion Transformer (DiT) (Peebles & Xie, 2023) progressively denoises the latent tensors and yields the output _V_<sup>ˆ</sup> 1: _T ∈_ R<sup>_T ×H×W ×_3</sup> after the VAE decoding process. 

We introduce a mask-sequence ControlNet conditioned on pixel-aligned masks _M ∈_ R<sup>_T ×H×W ×_1</sup> . Following ControlNet (Zhang et al., 2023), the mask sequence is encoded by the same 3D VAE into 


and injected via a set of trainable DiT blocks. Each ControlNet block produces features that pass through zeroinitialized convolutional layers and are additively fused into the corresponding backbone DiT block, guiding generation to align with the action-to-mask correspondence. 

Following (Yang et al., 2025c), we adopt velocity prediction in latent space. Let _z_ 0 denote the clean video latents and _ϵ ∼N_ (0 _, I_ ) be Gaussian noise. At diffusion step _τ_ , 


where _ατ_ is the noise-schedule coefficient. The model predicts the velocity _vθ_ , and the training objective is: 


While the standard video diffusion loss (Eq. 3) supervises frames independently, it under-exploits temporal correlations and can degrade spatiotemporal coherence. To mitigate this, we adopt a dynamics-consistency objective from (Yang et al., 2025b) that explicitly supervises latent motion, i.e., differences between video latents across temporal offsets. Let _{zt}_<sup>_T_</sup> _t_ =0<sup>_ℓ_denote the ground-truth video latents</sup> (from the VAE) and _{z_ ˆ _t}_<sup>_T_</sup> _t_ =0<sup>_ℓ_the model-predicted latents in</sup> the same latent grid. The dynamics-consistency loss is: 


where _K_ is the maximum temporal offset (set to 4 in our experiments) and _Tℓ_ is the number of latent frames. By computing this objective over multiple offsets _j_ = 1 _, . . . , K_ , it captures both short and long horizon dynamics. The total training loss combines the frame-wise diffusion objective and the dynamics-consistency term: 


4 

**Bridging Video Generation to Embodied World Models** 

## **3.4. Flow-Loss Enhanced Module** 

While embodiment-aware mask action conditioning helps, conventional frame-level reconstruction still encourages uniform fidelity over entire frames, including task-irrelevant backgrounds. For robotic manipulation, supervision should prioritize the motion of the embodiment and manipulated objects. We therefore adopt an optical-flow-based objective that compares the motion fields of the predicted and groundtruth videos, emphasizing dynamic, task-relevant regions and further improving spatiotemporal coherence. 

Let _V_<sup>ˆ</sup> 1: _T_ denote the predicted video (decoded from the VAE latents) and _V_ 1: _T_ the ground-truth video. We use a pretrained, frozen RAFT flow estimator (Teed & Deng, 2020) to compute optical flows for both sequences. The flow discrepancy aggregates a direction term (cosine-based) and a magnitude term (Huber-based (Huber, 1992)) to focus on learning motion regions. In compact form, 


where _Fϕ_ ( _·_ ) is the frozen flow operator and _Loss_ ( _·, ·_ ) denotes the composite direction–magnitude discrepancy. 

The overall training objective augments the diffusion loss and the latent dynamics-consistency term with flow supervision: 


To ensure stability when video quality is poor at the beginning of training, the flow loss is disabled during an initial warm-up of _eswitch_ epochs and then activated at a fixed weight: 


All flow computations are performed in the pixel domain on VAE-decoded frames, ensuring the penalty directly reflects the perceptual motion of the embodiment and objects. 

# **4. Experiments** 

In this section, we perform experiments on two robotic datasets as well as in the real world to evaluate the proposed BridgeV2W. Through the experiments, we aim to answer five research questions: 

- **RQ1:** Is representing actions as pixel-aligned embodiment masks more compatible with video generation models than coordinate-space action representations? 

- **RQ2:** Can BridgeV2W inherit the visual and motion priors of a pre-trained video generation model and demonstrate generalization in novel scenarios? 

- **RQ3:** Does embodiment-mask supervision enable robustness to unseen camera viewpoints? 

- **RQ4:** Can BridgeV2W be deployed on multiple embodiments under a unified world model? 

- **RQ5:** Can BridgeV2W be applied to downstream tasks, serving as a module for real-world policy evaluation and goal-image-based planning? 

## **4.1. Experimental Setup** 

**Datasets.** We evaluate BridgeV2W on two robotic datasets: DROID (Khazatsky et al., 2024), featuring a singlearm Franka system, and AgiBot-G1 (Bu et al., 2025), featuring a dual-arm system. For training, we use 19k trajectories from DROID, each recorded from two calibrated cameras, and 15k trajectories from AgiBot-G1. The provided camera calibration parameters are used to generate embodiment masks. For evaluation, we reserve 200 trajectories from each dataset as the standard test set. In addition, for DROID, we further hold out 100 trajectories for _unseencamera-viewpoint_ evaluation and another 100 trajectories for _unseen-scene_ evaluation. 

**Implementation Details.** We adopt CogVideoX-5BI2V (Yang et al., 2025c) as the pretrained video generation backbone. All video frames are resized to a resolution of 720 _×_ 480, and the model predicts a horizon of 25 future frames. To accelerate training, we randomly sample 20 clips from each video. Since our world model does not require language input, we ignore the original language instructions provided in the datasets. Instead, because CogVideoX requires a textual prompt for conditioning, we use a fixed placeholder prompt, _“Follow this action sequence represented in mask”_ , for all training and evaluation. More details could be found in Appendix A.2. 

**Baselines.** We compare BridgeV2W with three state-ofthe-art embodied world model methods: 

- IRASim (Zhu et al., 2024): a diffusion transformer–based trajectory-to-video model with frame-level action conditioning to capture robot–object interactions. 

- Cosmos (Agarwal et al., 2025): a world foundation model platform that pretrains on large-scale video data and supports building world models through post-training. 

- EVAC (Jiang et al., 2025): an action-conditioned world model that incorporates multi-level action injection and ray-map encoding for generating controllable videos. 

**Metrics.** Our evaluation uses four standard video quality metrics: PSNR (Hore & Ziou, 2010), SSIM (Wang et al., 2004), LPIPS (Zhang et al., 2018), and FVD (Ranftl et al., 

5 

**Bridging Video Generation to Embodied World Models** 

_Table 1._ Video generation results of BridgeV2W across different DROID dataset variants. 

|Methods|PSNR_↑_|SSIM_↑_|LPIPS_↓_|FVD_↓_|Mask-IoU_↑_|
|---|---|---|---|---|---|
|**In-Domain**||||||
|IRASim (Zhu et al.,2024)|22.11|0.846|0.119|175.7|58.0|
|Cosmos (Agarwal et al.,2025)|21.13|0.826|0.122|184.3|59.2|
|EVAC (Jiang et al.,2025)|21.97|**0.877**|0.124|219.8|57.4|
|BridgeV2W (Ours)|**22.89**|0.874|**0.111**|**145.2**|**62.2**|
|**Unseen Camera Viewpoint**||||||
|IRASim|18.02|0.763|0.162|415.8|45.9|
|Cosmos|19.73|0.786|0.177|303.1|48.0|
|EVAC|20.15|0.830|0.148|224.7|52.6|
|BridgeV2W (Ours)|**20.87**|**0.833**|**0.127**|**191.3**|**55.3**|
|**Unseen Scene**||||||
|IRASim|16.23|0.672|0.166|583.8|32.7|
|Cosmos|19.38|0.709|0.147|412.2|37.0|
|EVAC|17.78|0.693|0.159|486.5|31.4|
|BridgeV2W (Ours)|**19.73**|**0.717**|**0.138**|**362.1**|**44.1**|


_Table 2._ Video generation results of BridgeV2W on AgiBot-G1. 

|Methods|PSNR_↑_|SSIM_↑_|LPIPS_↓_|FVD_↓_|Mask-IoU_↑_|
|---|---|---|---|---|---|
|IRASim (Zhu et al.,2024)|23.38|0.842|0.121|144.6|55.6|
|Cosmos (Agarwal et al.,2025)|22.96|0.857|0.135|239.7|54.8|
|EVAC (Jiang et al.,2025)|23.64|0.858|0.117|169.4|57.9|
|BridgeV2W (Ours)|**24.49**|**0.868**|**0.102**|**129.5**|**58.3**|


2020), which measure pixel-level fidelity, perceptual similarity, and temporal realism of generated videos, respectively. To further assess the alignment between generated videos and input actions, we compute Mask-IoU between embodiment regions in generated and ground-truth frames, obtained via Grounded SAM (Ren et al., 2024) with _“robotic arm”_ as the textual prompt. 

## **4.2. Video Generation Evaluation** 

**Evaluation on DROID.** Video generation results of BridgeV2W across DROID dataset variants are shown in Table 1. On all in-domain, unseen-viewpoint, and unseenscene settings, BridgeV2W consistently achieves stronger temporal realism and perceptual quality (lower FVD/LPIPS) and tighter action–video alignment (higher Mask-IoU), while keeping PSNR/SSIM competitive. Cosmos remains strong in novel scenes given its broad pretraining, and EVAC is competitive under viewpoint shifts due to its image-space action encoding. IRASim degrades under distribution shift, likely because it trains solely on in-domain data with endeffector pose action representations. 

BridgeV2W benefits jointly from pretrained vision and motion priors and pixel-space mask actions that accommodate diverse camera viewpoints. By preserving those priors during adaptation and aligning the action control signal with the pixel space in which pretrained video models operate, BridgeV2W achieves better generalization to novel scenes (RQ2) and camera viewpoints (RQ3) without trading off per-frame fidelity. 

**Evaluation on AgiBot-G1.** Table 2 demonstrates that 

BridgeV2W achieves the best overall performance on the dual-arm AgiBot-G1 dataset: it attains lower FVD/LPIPS and higher Mask-IoU, while keeping PSNR/SSIM better. These results indicate that a unified world model design, conditioned by pixel-aligned embodiment masks, scales from single-arm to dual-arm embodiments without re-designing action encoders. It maintains temporal realism and action–video consistency despite increased kinematic complexity. These findings support RQ4 (a unified, crossembodiment world model) while remaining compatible with the generalization observations made on DROID. 

**Ablation Studies.** Table 3 shows that each component of BridgeV2W contributes to the video generation performance and robustness. Discarding pretraining (Row 1) weakens overall quality and stability under distribution shift, consistent with RQ2 on inheriting priors. Replacing pixel-aligned mask actions with end-effector pose coordinate-space actions (Row 2) yields notably worse temporal/perceptual quality and lower Mask-IoU, especially under unseen cameras and scenes, supporting RQ1 that mask actions better match the pixel-space distribution of pretrained video generators and are more view-aware. Removing the ControlNet-style conditioning (Row 3) further degrades results, indicating the value of a dedicated branch for injecting actions without eroding pretrained knowledge. Dropping the flow-based motion loss (Row 4) primarily reduces Mask-IoU and temporal coherence, aligning with our goal to emphasize dynamic, task-relevant regions rather than static background reconstruction. Taken together, the full design achieves the most reliable video generation quality and action-to-video consistency across all splits. 

**Qualitative Analysis.** Figure 3 demonstrates three key effects of BridgeV2W. (1) Pixel-space supervision on action masks transfers to unseen camera viewpoints, because the supervision is view-aligned rather than tied to a specific frame. (2) A pretrained video generation model enables synthesis in novel scenes, maintaining action-consistent motion despite background changes. (3) The unified mask representation serves as an embodiment-agnostic action representation, supporting a unified embodied world model across different robot platforms. More qualitative results of BridgeV2W could be found in Appendix C. 

**Training with Uncalibrated Segmentation Masks.** A key advantage of BridgeV2W is that training does not require camera calibration or URDF models. The model is supervised by action-conditioned masks, which can be obtained either from geometry-rendered embodiment masks or directly from segmentation-derived masks. This form of supervision does not assume access to accurate 3D geometry during training, but only requires consistent 2D mask signals associated with actions. This design enables BridgeV2W to leverage large-scale uncalibrated and actionless video data, 

6 

**Bridging Video Generation to Embodied World Models** 


_Figure 3._ Qualitative video generation results produced by BridgeV2W. 

_Table 3._ Ablation study on different design choices of BridgeV2W. 

|Model Variant|PSNR_↑_|SSIM_↑_|LPIPS_↓_|FVD_↓_|Mask-IoU_↑_|
|---|---|---|---|---|---|
|||In-Domai|n / Unseen Cam / Unseen|Scene||
|w/o Pretrained Model|21.24 / 19.61 / 17.72|0.842 / 0.770 / 0.568|0.120 / 0.145 / 0.209|211.3 / 245.3 / 513.6|59.7 /**56.1**/ 34.2|
|w/o Mask Action|21.77 / 17.59 / 17.96|0.863 / 0.698 / 0.645|0.119 / 0.173 / 0.178|175.8 / 360.4 / 453.0|58.9 / 47.0 / 41.4|
|w/o ControlNet|21.38 / 19.57 / 17.17|0.819 / 0.716 / 0.687|0.122 / 0.165 / 0.192|194.9 / 255.2 / 446.2|58.9 / 53.4 / 36.8|
|w/o Flow Loss|20.72 / 20.02 / 18.98|0.859 / 0.826 / 0.705|0.132 / 0.146 / 0.153|201.4 / 235.7 / 420.4|58.3 / 52.1 / 39.7|
|BridgeV2W (Ours)|**22.89**/**20.87**/**19.73**|**0.874**/**0.833**/**0.717**|**0.111**/**0.127**/**0.138**|**145.2**/**191.3**/**362.1**|**62.2**/ 55.3 /**44.1**|


_Table 4._ Training with segmentation-derived masks and mixed human–robot data on AgiBot-G1. 

|Data Source|PSNR_↑_|SSIM_↑_|LPIPS_↓_|FVD_↓_|Mask-IoU_↑_|
|---|---|---|---|---|---|
|100% G1**calc mask**<br>(URDF-rendered)|24.49|**0.868**|**0.102**|129.5|**58.3**|
|100% G1**seg mask**<br>(GroundedSAM)|22.87|0.822|0.129|191.6|53.9|
|30% G1**calc**+ Ego4D|24.28|0.850|0.118|133.9|57.2|
|70% G1**seg**<br>+ 30% G1**calc**+ Ego4D|**24.58**|0.863|0.108|**118.5**|58.1|


including egocentric human–hand interaction datasets such as Ego4D (Grauman et al., 2022), during training. We use GroundedSAM (Ren et al., 2024) for extracting masks in those uncalibrated datasets. 

As shown in Table 4, training with segmentation masks alone already provides meaningful supervision, despite the 

mismatch between segmentation masks used in training and URDF-rendered masks used at inference. This suggests that BridgeV2W primarily learns motion-consistent visual dynamics rather than overfitting to precise geometric mask boundaries. More importantly, mixing large-scale uncalibrated human videos with only a small fraction of calibrated robot data nearly matches the performance of full calc-mask training. This indicates that human videos provide strong motion priors, while limited calibrated robot data is sufficient to align the model with the target robotic embodiment. Detailed analysis is provided in Appendix A.5. 

## **4.3. Downstream Applications** 

**Real-World Setup.** Real-world experiments use a Franka Research 3 robotic arm and a fixed third-person ZED 2i RGB-D camera. For a given target gripper action, we em- 

7 

**Bridging Video Generation to Embodied World Models** 


_Figure 4._ Correlation between BridgeV2W policy evaluation and real-world success rates. 

ploy frankapy (Zhang et al., 2020) for trajectory generation and feedback control to reach the target. We evaluate four tasks: put the bottle on the plate, put the toy in the shelf, close the drawer, and flip the cup, each with approximately 80 trajectories collected using a 3D mouse. For each task, initial object poses are randomized, and a trial is successful when the condition is met. We further implement three VLA baselines: OpenVLA-OFT (Kim et al., 2025), _π_ 0 (Black et al., 2024), and SpatialVLA (Qu et al., 2025). More details could be found in Appendix B.1. 

**Policy Evaluation.** We evaluate BridgeV2W as a proxy for policy evaluation. Given an initial image, we feed it to each VLA policy, take the resulting action chunk, and generate future images with BridgeV2W. We then use the last generated image to re-query the VLA models in an autoregressive manner. The correlation between BridgeV2Wbased evaluation and real-world success rates is shown in Figure 4. We observe a strong correlation (Pearson _r_ = 0 _._ 84), indicating that BridgeV2W can serve as a proxy for estimating VLA policy performance without real-world execution. We also note that BridgeV2W sometimes predicts higher success rates than those observed in the real world, because BridgeV2W is trained primarily on successful expert demonstrations, it tends to generate successful rollouts when action errors are modest, whereas such errors can still cause failures in the real world. 

Detailed results are provided in Table 5. We report two metrics: Mean Maximum Rank Violation (MMRV), adopted from SIMPLER (Li et al., 2025c), which measures the consistency between real-world and BridgeV2W policy rankings, and the Pearson correlation coefficient (Pearson _r_ ), which quantifies the linear relationship between the two evaluations. BridgeV2W performs well on both metrics, supporting its use as a proxy for downstream policy evaluation. Additional details are provided in Appendix B.2. 

**Goal-Image Conditioned Manipulation.** We further apply BridgeV2W to goal-conditioned manipulation. For each task, we specify two goal images (a grasping subgoal and a final-state subgoal) and optimize action sequences with the Cross-Entropy Method (CEM). Concretely, at each 

_Table 5._ Policy evaluation across tasks and baselines using BridgeV2W. 

|Tasks|MMRV_↓_|Pearson_r ↑_|
|---|---|---|
|Put on plate|0.133|0.655|
|Put in shelf|0.033|0.944|
|Close Drawer|0.000|0.982|
|Flip Cup|0.033|0.945|
|Avg.|0.050|0.882|


_Table 6._ Real-world planning performance with BridgeV2W. 

|Tasks|OpenVLA-OFT|BridgeV2W|
|---|---|---|
|Put on plate|4 / 10|**5**/ 10|
|Put in shelf|**6**/ 10|5 / 10|
|Close Drawer|**5**/ 10|**5**/ 10|
|Flip Cip|2 / 10|**3**/ 10|
|All Tasks|17 / 40|**18**/ 40|


iteration over the rollout horizon, we sample multiple action trajectories from a Gaussian distribution, use BridgeV2W to predict the resulting final states, score each trajectory by its similarity to the target goal image, select the top- _k_ trajectories as elites, and update the distribution’s mean and variance accordingly. The executed action is taken as the mean of the refined distribution. Crucially, BridgeV2W provides action-conditioned future predictions that preserve both object motion and embodiment constraints, enabling CEM to evaluate long-horizon outcomes in pixel space without requiring explicit reward engineering or task-specific heuristics. Detailed results are reported in Table 6. 

We observe strong performance on tasks where the gripper remains down-facing with moderate rotation. For rotationheavy tasks (e.g., closing a drawer, flipping a cup), the main difficulty stems from searching over high-dimensional rotational controls. Simple planning refinements, such as allocating more CEM samples to rotation and briefly decoupling rotation from translation, lead to clear success-rate gains. Additional analysis is provided in Appendix B.3, which also discusses how BridgeV2W can be integrated with VLA policies for closed-loop planning. 

# **5. Conclusion** 

In this paper, we propose BridgeV2W, which represents actions as pixel-aligned embodiment masks and injects them into pretrained video generation models via a ControlNetstyle pathway with a motion-centric flow loss. This design preserves pretrained visual and motion priors, enables viewpoint robustness, and supports a unified world model across diverse robotic embodiments. We evaluate BridgeV2W on two robotic platforms and in real-world settings, demonstrating strong action-conditioned video generation performance and effectiveness for downstream manipulation tasks such as policy evaluation and goal-image–conditioned planning. 

8 

**Bridging Video Generation to Embodied World Models** 

# **Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning, particularly in the context of embodied agents and world modeling. There are many potential societal consequences of this line of research, none of which we feel must be specifically highlighted here. 

# **References** 

- 1X World Model Team. 1x world model: Evaluating bits, not atoms. Technical report, 1X Technologies, 2025. URL https://www.1x.tech/ 1x-world-model.pdf. 

- Achiam, J., Adler, S., Agarwal, S., Ahmad, L., Akkaya, I., Aleman, F. L., Almeida, D., Altenschmidt, J., Altman, S., Anadkat, S., et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- Agarwal, N., Ali, A., Bala, M., Balaji, Y., Barker, E., Cai, T., Chattopadhyay, P., Chen, Y., Cui, Y., Ding, Y., et al. Cosmos world foundation model platform for physical ai. _arXiv preprint arXiv:2501.03575_ , 2025. 

- Assran, M., Bardes, A., Fan, D., Garrido, Q., Howes, R., Muckley, M., Rizvi, A., Roberts, C., Sinha, K., Zholus, A., et al. V-jepa 2: Self-supervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. 

- Bai, Y., Tran, D., Bar, A., LeCun, Y., Darrell, T., and Malik, J. Whole-body conditioned egocentric video prediction. _arXiv preprint arXiv:2506.21552_ , 2025. 

- Baldassarre, F., Szafraniec, M., Terver, B., Khalidov, V., Massa, F., LeCun, Y., Labatut, P., Seitzer, M., and Bojanowski, P. Back to the features: Dino as a foundation for video world models. _arXiv preprint arXiv:2507.19468_ , 2025. 

- Bar, A., Zhou, G., Tran, D., Darrell, T., and LeCun, Y. Navigation world models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 15791– 15801, 2025. 

- Bar-Tal, O., Chefer, H., Tov, O., Herrmann, C., Paiss, R., Zada, S., Ephrat, A., Hur, J., Liu, G., Raj, A., et al. Lumiere: A space-time diffusion model for video generation. In _SIGGRAPH Asia 2024 Conference Papers_ , pp. 1–11, 2024. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Bu, Q., Cai, J., Chen, L., Cui, X., Ding, Y., Feng, S., Gao, S., He, X., Hu, X., Huang, X., et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025. 

- Chen, Y., Li, P., Huang, Y., Yang, J., Chen, K., and Wang, L. Ec-flow: Enabling versatile robotic manipulation from action-unlabeled videos via embodiment-centric flow. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 11958–11968, October 2025. 

- Chen, Y., Huang, Y., He, K., Li, P., and Wang, L. Verm: Leveraging foundation models to create a virtual eye for efficient 3d robotic manipulation. _IEEE Robotics and Automation Letters_ , 11(3):2482–2489, 2026. doi: 10.1109/LRA.2026.3652073. 

- Chen, Z., Walsman, A., Memmel, M., Mo, K., Fang, A., Vemuri, K., Wu, A., Fox, D., and Gupta, A. Urdformer: A pipeline for constructing articulated simulation environments from real-world images. _arXiv preprint arXiv:2405.11656_ , 2024. 

- Finn, C. and Levine, S. Deep visual foresight for planning robot motion. In _2017 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 2786–2793, 2017. doi: 10.1109/ICRA.2017.7989324. 

- Fu, X., Liu, X., Wang, X., Peng, S., Xia, M., Shi, X., Yuan, Z., Wan, P., Zhang, D., and Lin, D. 3dtrajmaster: Mastering 3d trajectory for multi-entity motion in video generation. _arXiv preprint arXiv:2412.07759_ , 2024. 

- Goyal, R., Ebrahimi Kahou, S., Michalski, V., Materzynska, J., Westphal, S., Kim, H., Haenel, V., Fruend, I., Yianilos, P., Mueller-Freitag, M., et al. The” something something” video database for learning and evaluating visual common sense. In _Proceedings of the IEEE International Conference on Computer Vision_ , pp. 5842–5850, 2017. 

- Grauman, K., Westbury, A., Byrne, E., Chavis, Z., Furnari, A., Girdhar, R., Hamburger, J., Jiang, H., Liu, M., Liu, X., et al. Ego4d: Around the world in 3,000 hours of egocentric video. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 18995–19012, 2022. 

- Gu, Z., Yan, R., Lu, J., Li, P., Dou, Z., Si, C., Dong, Z., Liu, Q., Lin, C., Liu, Z., et al. Diffusion as shader: 3d-aware video diffusion for versatile video generation control. In _Proceedings of the Special Interest Group on Computer Graphics and Interactive Techniques Conference Conference Papers_ , pp. 1–12, 2025. 

- Guo, Y., Yang, C., Rao, A., Liang, Z., Wang, Y., Qiao, Y., Agrawala, M., Lin, D., and Dai, B. Animatediff: Animate 

9 

**Bridging Video Generation to Embodied World Models** 

your personalized text-to-image diffusion models without specific tuning. _International Conference on Learning Representations_ , 2024. 

- He, H., Zhang, Y., Lin, L., Xu, Z., and Pan, L. Pre-trained video generative models as world simulators. _arXiv preprint arXiv:2502.07825_ , 2025. 

- Hore, A. and Ziou, D. Image quality metrics: Psnr vs. ssim. In _2010 20th International Conference on Pattern Recognition_ , pp. 2366–2369. IEEE, 2010. 

- Huang, S., Wu, J., Zhou, Q., Miao, S., and Long, M. Vid2world: Crafting video diffusion models to interactive world models. _arXiv preprint arXiv:2505.14357_ , 2025. 

- Huber, P. J. Robust estimation of a location parameter. In _Breakthroughs in Statistics: Methodology and Distribution_ , pp. 492–518. Springer, 1992. 

- Jiang, Y., Chen, S., Huang, S., Chen, L., Zhou, P., Liao, Y., He, X., Liu, C., Li, H., Yao, M., et al. Enerverse-ac: Envisioning embodied environments with action condition. _arXiv preprint arXiv:2505.09723_ , 2025. 

- Khazatsky, A., Pertsch, K., Nair, S., Balakrishna, A., Dasari, S., Karamcheti, S., Nasiriany, S., Srirama, M. K., Chen, L. Y., Ellis, K., et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- Kingma, D. P. and Welling, M. Auto-encoding variational bayes. _arXiv preprint arXiv:1312.6114_ , 2013. 

- Li, M., Yang, T., Kuang, H., Wu, J., Wang, Z., Xiao, X., and Chen, C. Controlnet++: Improving conditional controls with efficient consistency feedback: Project page: liming-ai. github. io/controlnet ~~p~~ lus ~~p~~ lus. In _European Conference on Computer Vision_ , pp. 129–147. Springer, 2024. 

- Li, P., Chen, Y., Wu, H., Ma, X., Wu, X., Huang, Y., Wang, L., Kong, T., and Tan, T. BridgeVLA: Input-output alignment for efficient 3d manipulation learning with visionlanguage models. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025a. 

- Li, Q., Xing, Z., Wang, R., Zhang, H., Dai, Q., and Wu, Z. Magicmotion: Controllable video generation with dense-to-sparse trajectory guidance. _arXiv preprint arXiv:2503.16421_ , 2025b. 

- Li, X., Hsu, K., Gu, J., Mees, O., Pertsch, K., Walke, H. R., Fu, C., Lunawat, I., Sieh, I., Kirmani, S., et al. Evaluating 

- real-world robot manipulation policies in simulation. In _Conference on Robot Learning_ , pp. 3705–3728. PMLR, 2025c. 

- Li, Y., Wang, X., Zhang, Z., Wang, Z., Yuan, Z., Xie, L., Shan, Y., and Zou, Y. Image conductor: Precision control for interactive video synthesis. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, pp. 5031–5038, 2025d. 

- Li, Y., Zhu, Y., Wen, J., Shen, C., and Xu, Y. Worldeval: World model as real-world robot policies evaluator. _arXiv preprint arXiv:2505.19017_ , 2025e. 

- Liao, Y., Zhou, P., Huang, S., Yang, D., Chen, S., Jiang, Y., Hu, Y., Cai, J., Liu, S., Luo, J., et al. Genie envisioner: A unified world foundation platform for robotic manipulation. _arXiv preprint arXiv:2508.05635_ , 2025. 

- Lu, J., Liang, Z., Xie, T., Richter, F., Lin, S., Liu, S., and Yip, M. C. Ctrnet-x: Camera-to-robot pose estimation in realworld conditions using a single camera. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 1914–1920. IEEE, 2025. 

- Namekata, K., Bahmani, S., Wu, Z., Kant, Y., Gilitschenski, I., and Lindell, D. B. SG-i2v: Self-guided trajectory control in image-to-video generation. In _The Thirteenth International Conference on Learning Representations_ , 2025. 

- Peebles, W. and Xie, S. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 4195–4205, 2023. 

- Qiu, H., Chen, Z., Wang, Z., He, Y., Xia, M., and Liu, Z. Freetraj: Tuning-free trajectory control in video diffusion models. _arXiv preprint arXiv:2406.16863_ , 2024. 

- Qu, D., Song, H., Chen, Q., Yao, Y., Ye, X., Ding, Y., Wang, Z., Gu, J., Zhao, B., Wang, D., et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., Zhou, Y., Li, W., and Liu, P. J. Exploring the limits of transfer learning with a unified text-to-text transformer. _Journal of machine learning research_ , 21 (140):1–67, 2020. 

- Ranftl, R., Lasinger, K., Hafner, D., Schindler, K., and Koltun, V. Towards robust monocular depth estimation: Mixing datasets for zero-shot cross-dataset transfer. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 44(3):1623–1637, 2020. 

10 

**Bridging Video Generation to Embodied World Models** 

- Ren, T., Liu, S., Zeng, A., Lin, J., Li, K., Cao, H., Chen, J., Huang, X., Chen, Y., Yan, F., et al. Grounded sam: Assembling open-world models for diverse visual tasks. _arXiv preprint arXiv:2401.14159_ , 2024. 

- Rombach, R., Blattmann, A., Lorenz, D., Esser, P., and Ommer, B. High-resolution image synthesis with latent diffusion models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 10684–10695, June 2022. 

- Shi, X., Huang, Z., Wang, F.-Y., Bian, W., Li, D., Zhang, Y., Zhang, M., Cheung, K. C., See, S., Qin, H., et al. Motion-i2v: Consistent and controllable image-to-video generation with explicit motion modeling. In _ACM SIGGRAPH 2024 Conference Papers_ , pp. 1–11, 2024. 

- Teed, Z. and Deng, J. Raft: Recurrent all-pairs field transforms for optical flow. In _European Conference on Computer Vision_ , pp. 402–419. Springer, 2020. 

- Wang, H., Ouyang, H., Wang, Q., Wang, W., Cheng, K. L., Chen, Q., Shen, Y., and Wang, L. Levitor: 3d trajectory oriented image-to-video synthesis. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 12490–12500, 2025a. 

- Wang, J., Zhang, Y., Zou, J., Zeng, Y., Wei, G., Yuan, L., and Li, H. Boximator: generating rich and controllable motions for video synthesis. In _Proceedings of the 41st International Conference on Machine Learning_ , pp. 52274– 52289, 2024a. 

- Wang, L., Zhao, K., Liu, C., and Chen, X. Learning realworld action-video dynamics with heterogeneous masked autoregression. _arXiv preprint arXiv:2502.04296_ , 2025b. 

- Wang, Q., Luo, Y., Shi, X., Jia, X., Lu, H., Xue, T., Wang, X., Wan, P., Zhang, D., and Gai, K. Cinemaster: A 3daware and controllable framework for cinematic text-tovideo generation. In _Proceedings of the Special Interest Group on Computer Graphics and Interactive Techniques Conference Conference Papers_ , pp. 1–10, 2025c. 

- Wang, T., Li, L., Lin, K., Zhai, Y., Lin, C.-C., Yang, Z., Zhang, H., Liu, Z., and Wang, L. Disco: Disentangled control for realistic human dance generation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 9326–9336, 2024b. 

- Wang, Z., Bovik, A. C., Sheikh, H. R., and Simoncelli, E. P. Image quality assessment: from error visibility to structural similarity. _IEEE Transactions on Image Processing_ , 13(4):600–612, 2004. 

- Wu, J., Yin, S., Feng, N., He, X., Li, D., Hao, J., and Long, M. ivideogpt: Interactive videogpts are scalable world models. _Advances in Neural Information Processing Systems_ , 37:68082–68119, 2024. 

- Xu, Y., Yang, J., Wang, X., Chen, Y., Zhu, Z., Fang, B., Huang, G., Chen, X., Ye, Y., Zhang, Q., et al. Egodemogen: Novel egocentric demonstration generation enables viewpoint-robust manipulation. _arXiv preprint arXiv:2509.22578_ , 2025. 

- Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Gao, C., Huang, C., Lv, C., et al. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_ , 2025a. 

- Yang, J., Chitta, K., Gao, S., Chen, L., Shao, Y., Jia, X., Li, H., Geiger, A., Yue, X., and Chen, L. Resim: Reliable world simulation for autonomous driving. _arXiv preprint arXiv:2506.09981_ , 2025b. 

- Yang, Z., Teng, J., Zheng, W., Ding, M., Huang, S., Xu, J., Yang, Y., Hong, W., Zhang, X., Feng, G., Yin, D., Yuxuan.Zhang, Wang, W., Cheng, Y., Xu, B., Gu, X., Dong, Y., and Tang, J. Cogvideox: Text-to-video diffusion models with an expert transformer. In _The Thirteenth International Conference on Learning Representations_ , 2025c. 

- Yi, B., Kim, C. M., Kerr, J., Wu, G., Feng, R., Zhang, A., Kulhanek, J., Choi, H., Ma, Y., Tancik, M., and Kanazawa, A. Viser: Imperative, web-based 3d visualization in python, 2025. URL https://arxiv.org/ abs/2507.22885. 

- Yin, S., Wu, C., Liang, J., Shi, J., Li, H., Ming, G., and Duan, N. Dragnuwa: Fine-grained control in video generation by integrating text, image, and trajectory. _arXiv preprint arXiv:2308.08089_ , 2023. 

- Zhang, K., Sharma, M., Liang, J., and Kroemer, O. A modular robotic arm control stack for research: Frankainterface and frankapy. _arXiv preprint arXiv:2011.02398_ , 2020. 

- Zhang, L., Rao, A., and Agrawala, M. Adding conditional control to text-to-image diffusion models. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 3836–3847, 2023. 

- Zhang, R., Isola, P., Efros, A. A., Shechtman, E., and Wang, O. The unreasonable effectiveness of deep features as a perceptual metric. In _Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition_ , pp. 586– 595, 2018. 

- Zhang, Z., Liao, J., Li, M., Dai, Z., Qiu, B., Zhu, S., Qin, L., and Wang, W. Tora: Trajectory-oriented diffusion transformer for video generation. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 2063–2073, 2025. 

- Zhu, F., Wu, H., Guo, S., Liu, Y., Cheang, C., and Kong, T. Irasim: Learning interactive real-robot action simulators. _arXiv preprint arXiv:2406.14540_ , 2024. 

11 

**Bridging Video Generation to Embodied World Models** 

# **Appendix** 

# **A. Video Generation Experiments** 

## **A.1. Datasets** 

We evaluate BridgeV2W on two robotic datasets: DROID (Khazatsky et al., 2024) (single-arm Franka) and AgiBot-G1 (Bu et al., 2025) (dual-arm). For training, we use 19k DROID trajectories, each recorded from two calibrated third-person cameras. We treat the two views as independent view–trajectory pairs sharing the same action stream, yielding 19k _×_ 2 = 38k view–trajectory pairs. For AgiBot-G1, we train on 15k trajectories and include all available calibrated external views per scene. For evaluation, we hold out 200 trajectories from each dataset as a standard test set with no sequence overlap with training. In addition, for DROID, we construct two generalization splits: an unseen-camera-viewpoint set of 100 trajectories (cameras not used in training) and an unseen-scene set of 100 trajectories (novel layouts/skills). 

For the single-arm DROID setting, each action at time _t_ is a 7-D end-effector command **a**<sup>(single)</sup> _t_ = [ _xt, yt, zt, ϕt, θt, ψt, gt_ ] _∈_ R<sup>7</sup> , where ( _xt, yt, zt_ ) is the Cartesian position, ( _ϕt, θt, ψt_ ) are roll, pitch, and yaw, and _gt ∈_ [0 _,_ 1] is the normalized gripper control. For the dual-arm AgiBot-G1 setting, we concatenate left- and right-arm commands, **a**<sup>(dual)</sup> _t_ = [ **a**<sup>(</sup> _t_<sup>_L_)</sup> ; **a**<sup>(</sup> _t_<sup>_R_)</sup> ] _∈_ R<sup>14</sup> _,_ **a**<sup>(</sup> _t_<sup>_L_)</sup> = [ _x_<sup>(</sup> _t_<sup>_L_)</sup> _, yt_<sup>(</sup><sup>_L_)</sup> _, zt_<sup>(</sup><sup>_L_)</sup> _, ϕ_<sup>(</sup> _t_<sup>_L_)</sup> _, θt_<sup>(</sup><sup>_L_)</sup> _, ψt_<sup>(</sup><sup>_L_)</sup> _, gt_<sup>(</sup><sup>_L_)</sup> ] _,_ **a**<sup>(</sup> _t_<sup>_R_)</sup> = [ _x_<sup>(</sup> _t_<sup>_R_)</sup> _, yt_<sup>(</sup><sup>_R_)</sup> _, zt_<sup>(</sup><sup>_R_)</sup> _, ϕ_<sup>(</sup> _t_<sup>_R_)</sup> _, θt_<sup>(</sup><sup>_R_)</sup> _, ψt_<sup>(</sup><sup>_R_)</sup> _, gt_<sup>(</sup><sup>_R_)</sup> ], enabling synchronized bimanual control within the same pixel-aligned mask space. 

Figure 5 visualizes two robot models from URDFs using Viser (Yi et al., 2025). For each action, we convert the Cartesian end-effector command ( _xyz+rpy+gripper_ ) to joint space via inverse kinematics, apply forward kinematics on the URDF to obtain link poses, and project the meshes onto the image plane with calibrated intrinsics/extrinsics to render a pixel-aligned embodiment mask. 


_Figure 5._ The visualization of the URDF of Franka Panda and AgiBot G1. 

## **A.2. Implementation Details** 

We adopt CogVideoX-5B-I2V (Yang et al., 2025c) as the backbone video generator (see Table 7 for model parameters). The text branch uses a T5 encoder (Raffel et al., 2020). Because our embodied world model conditions on action masks rather than language, we do not use the datasets’ language instructions; instead, we supply a neutral placeholder prompt, _“Follow this action sequence represented in mask_ ”, to keep the text encoder active. 

We inject embodiment masks as action conditions into the pretrained CogVideoX via a ControlNet-style conditioning branch. Fine-tuning hyperparameters are listed in Table 8. We fine-tune on 2 _×_ 8 H20 GPUs (96 GB each) for approximately two weeks. 

12 

**Bridging Video Generation to Embodied World Models** 

|Parameter|Value|
|---|---|
|number of layers|42|
|attention heads|48|
|hidden size|3072|
|positional encoding|RoPE|
|time embedding size|256|
|text length|226|
|max sequence length|82k|
|training precision|BF16|


_Table 7._ Hyper-Parameters of CogVideo-5b-I2V. 

|Parameter|Value|
|---|---|
|video size|(480, 720)|
|video length|25|
|_λdyn_|0.1|
|dynamic window size_K_|4|
|_λflow_|0.05|
|_eswitch_|5|
|learning rate|2e-5|
|batch size|5|
|optimizer|_adamw_|
|optimizer beta1|0.9|
|optimizer beta2|0.95|
|optimizer epsilon|1e-8|
|optimizer weight<br>~~d~~ecay|1e-4|
|max rad norm|1.0|
|lr scheduler|_constant with warmup_|
|lr warmup step|100|
|lora rank|64|
|lora alpha|64|


_Table 8._ Hyper-Parameters of BridgeV2W. 

## **A.3. Baselines** 

**IRASim** (Zhu et al., 2024) IRASim formulates robot world modeling as a trajectory to video prediction problem given _h_ historical observations _It−h_ : _t_ and an action sequence _at_ : _t_ + _n_ , the model predicts the next _n_ +1 frames _It_ +1: _t_ + _n_ +1 = _f_ ( _It−h_ : _t, at_ : _t_ + _n_ ). For efficiency, diffusion is performed in a VAE latent space: each frame is encoded/decoded by a frozen VAE, and a DiT backbone with memory-efficient spatio-temporal attention scales to long, high-resolution rollouts. To preserve visual context, historical frames are injected as _clean_ (noise-free) tokens, while only future tokens are noised and supervised, allowing predictions to attend to clean history for temporal consistency. Action conditioning is implemented via adaptive layer normalization at two granularities: (i) _video-level_ conditioning encodes the whole trajectory into a single embedding that modulates all blocks; and (ii) _frame-level_ conditioning linearly encodes each action step, combines it with the diffusion-timestep embedding, and produces per-frame scale and shift parameters for spatial blocks (with a shared temporal-block embedding), explicitly enforcing action and enabling fine-grained robot-object interactions. A current limitation is that IRASim is trained only on in-domain data, which may hinder generalization to unseen cameras and scenes. 

**Cosmos** (Agarwal et al., 2025) Cosmos frames a world foundation model (WFM) as a learnable, at-scale digital twin for physical AI. The pipeline has two stages: (i) pre-train a generalist visual WFM on a large curated video corpus with scalable transformers and learned video tokenizers that compress videos into compact token sequences; (ii) post-train on target environments with prompt–video pairs where prompts encode action commands, trajectories, or instructions to obtain specialized, action-conditioned models. The model predicts future observations conditioned on executed actions, tightening 

13 

**Bridging Video Generation to Embodied World Models** 

the coupling between representation and controllable dynamics. While Cosmos benefits from pretraining to generalize to novel scenes, its end-effector pose action representation constrains transfer to unseen camera viewpoints and diverse embodiments. 

**EVAC** (Jiang et al., 2025) EVAC is an action-conditioned world model that predicts future visual observations from an agent’s proposed actions, serving as a controllable, low-cost proxy for real-robot or 3D-simulator evaluation. It injects control signals via a multi-level conditioning scheme that combines end-effector projection action maps with delta-action encodings. To support multi-view robotics, EVAC encodes camera pose and motion using spatial cross-attention and ray-direction map embeddings, enabling view-consistent synthesis as viewpoints change. By projecting actions into the image plane, EVAC is robust to unseen camera viewpoints; however, because it is trained only on in-domain data and does not leverage pretrained visual or motion priors, its performance degrades in unseen scenes. 

## **A.4. Ablation Settings** 

In our ablation study, we probe four design choices of BridgeV2W while keeping all other factors fixed. 

- _w/o Pretrained Model_ : We keep the CogVideoX architecture but train the transformer backbone from scratch (no pretrained weights); the T5 text encoder and VAE remain pretrained. This isolates the contribution of pretrained visual and motion priors to scene generalization, texture fidelity, and rollout stability. 

- _w/o Mask Action_ : We replace mask-based actions with end-effector pose actions (e.g., _xyz_ + _rpy_ + _gripper_ ), encoded by an MLP. This ablation tests whether pixel-aligned supervision is the main driver of viewpoint robustness and crossembodiment conditioning. 

- _w/o ControlNet_ : We remove the ControlNet-style pathway for mask conditioning and instead route conditions through a separate non-zero-initialized branch. This examines the role of a zero-initialized residual path in preserving pretrained priors during fine-tuning. 

- _w/o Flow Loss_ : We drop the motion-centric flow loss and train with the remaining objectives, to evaluate whether emphasizing task-relevant motion regions improves contact timing, motion sharpness, and background stability. 

## **A.5. Training with Segmentation-Derived Masks and Reduced Calibration Requirements** 

A notable advantage of BridgeV2W is that it does not require camera intrinsics/extrinsics or URDF models during training. The framework only uses this geometric information at inference time to render pixel-aligned embodiment masks (“calc masks”). During training, the action-conditioned supervision can be obtained directly from segmentation-derived masks (“seg masks”), allowing the use of large uncalibrated datasets where no robot model or camera parameters are available. 

To demonstrate this flexibility, we conducted additional experiments combining AgiBot-G1 robot data with the Ego4D FHO subset (Grauman et al., 2022), which contains egocentric human–hand interaction videos without any calibration or articulated models. We extracted hand masks using GroundedSAM and trained BridgeV2W under several data configurations. As shown in Table 4, training solely with segmentation-derived masks on robot data (“100% G1 seg”) still provides meaningful supervisory signals despite the mismatch between segmentation masks and the calc masks used at inference. More importantly, incorporating large-scale Ego4D segmentation masks while mixing in only a small fraction of G1 calc-mask data nearly matches the performance of full calc-mask training. This indicates that: (i) segmentation-only human videos contribute rich motion priors, and (ii) limited calibrated robot data is sufficient for aligning the model with the target embodiment. 

At inference time, BridgeV2W requires approximate camera parameters and a URDF model to render embodiment masks. This requirement is lightweight and practical: such metadata is routinely available in modern robotic systems for control, teleoperation, and simulation. Furthermore, the geometry used in our experiments is not derived from ideal checkerboard calibration. For example, many camera intrinsics/extrinsics in the DROID dataset come from CtRNet-X (Lu et al., 2025), a learned 2D–3D alignment pipeline that introduces estimation noise. Despite this approximation, BridgeV2W maintains strong performance across all benchmarks. Additionally, recent approaches such as URDFormer (Chen et al., 2024) can recover articulated robot models directly from RGB images when a URDF is not available. 

Overall, these results show that BridgeV2W can scale to broad uncalibrated video corpora during training while requiring only lightweight geometric information during deployment. This combination enables both practical scalability and strong 

14 

**Bridging Video Generation to Embodied World Models** 

action-conditioned video generation performance. 

## **A.6. Evaluating Mask-IoU and the Role of Geometric Signals** 

Mask-IoU is used to evaluate action–video consistency, which standard appearance metrics (PSNR/SSIM/LPIPS/FVD) cannot measure. Although BridgeV2W conditions on rendered masks, Mask-IoU compares predictions against _ground-truth_ masks containing object interactions and occlusions, not against the conditioning inputs. Thus, simply receiving masks does not inflate the metric; indeed, ablations that keep the same masks but remove key modeling components yield lower Mask-IoU, showing that the metric reflects accurate motion prediction. 

To test whether baselines could similarly benefit from geometry, we provide ground-truth camera intrinsics and extrinsics to baseline world models via MLP encoders. As shown in Table 9, calibration features do not improve performance and degrade unseen-camera results due to distribution shift. 

_Table 9._ Effect of providing camera intrinsics/extrinsics to baseline world models. 

|**Methods**|**PSNR↑**|**SSIM↑**|**LPIPS↓**|**FVD↓**|**Mask-IoU↑**|
|---|---|---|---|---|---|
|IRASim|22.11/18.02/16.23|0.846/0.763/0.672|0.119/0.162/0.166|175.7/415.8/583.8|58.0/45.9/32.7|
|IRASim (with cam params)|21.98/17.64/15.91|0.839/0.751/0.663|0.124/0.171/0.178|182.3/438.6/605.2|57.3/44.1/31.8|
|Cosmos|21.13/19.73/19.38|0.826/0.786/0.709|0.122/0.177/0.147|184.3/303.1/412.2|59.2/48.0/37.0|
|Cosmos (with cam params)|21.27/18.12/17.75|0.818/0.772/0.695|0.128/0.189/0.159|190.4/336.7/451.9|58.5/45.8/34.9|
|BridgeV2W|22.89/20.87/19.73|0.874/0.833/0.717|0.111/0.127/0.138|145.2/191.3/362.1|62.2/55.3/44.1|


## **A.7. Additional Related Work on Video Prediction in Robotics** 

Beyond action-conditioned world models, several works have explored video prediction and generation as auxiliary tools for robotic learning. Xu et al. (2025) leverages generative video synthesis to augment egocentric demonstrations, improving data efficiency and viewpoint robustness. Chen et al. (2026) shows that selecting task-adaptive viewpoints significantly affects the quality and usefulness of predicted visual observations in robotic manipulation. Early work, such as visual foresight (Finn & Levine, 2017), uses action-conditioned video prediction for planning via imagined rollouts. 

# **B. Real-World Experiments** 

## **B.1. Real-World Setup** 

**Robot Platform** As shown in Fig. 6, our real-world platform consists of a statically mounted _Franka Research 3_ robotic arm and a fixed third-person _Zed2i_ RGB-D camera observing the workspace. The camera is rigidly mounted on a tripod facing the tabletop and provides synchronized RGB-D streams with timestamps. We calibrate the camera to robot extrinsics using a checkerboard, and use factory intrinsics for the _Zed2i_ . For control, we employ frankapy (Zhang et al., 2020) to execute Cartesian pose trajectories with closed-loop feedback. To facilitate teleoperation during data collection, we use a 3D mouse to specify waypoints that frankapy interpolates into smooth, time-parameterized trajectories. 

**Task Definition** As shown in Figure 7, We evaluate four manipulation tasks: (1) _Put the redbull on the plate (put on plate)_ ; (2) _Put the lion on the top shelf (put in shelf)_ ; (3) _Close the upper drawer (close drawer)_ ; (4) _Flip the cup upside down (flip cup)_ . For each task, we collect approximately 80 teleoperated trajectories, yielding diverse object poses and initial scene layouts. Each episode starts from a standardized reset configuration with objects placed within the marked workspace. Success criteria are task-specific and binary (e.g., bottle resting on the plate without toppling; drawer fully closed; cup rotated to the target orientation). **Vision-Language-Action (VLA) model baselines** We consider three representative VLA baselines in our real-world evaluations: 

- OpenVLA-OFT (Kim et al., 2025): An optimized fine-tuning recipe for VLA models that targets both control quality and inference speed. Using OpenVLA as the base policy, the method systematically rethinks three adaptation choices: parallel decoding action chunking, continuous vectorized control space, and a simple L1 regression over continuous actions. 

- _π_ 0 (Black et al., 2024): A generalist VLA policy that augments a pretrained vision–language model with a flow-matching 

15 

**Bridging Video Generation to Embodied World Models** 


_Figure 6._ Illustrations of the real-world Franka robot platform setup. 


_Figure 7._ Illustrations of the real-world task setup. 

action head to model continuous control. The architecture couples Internet-scale semantic priors from the VLM with an action chunking decoder that outputs short horizons of continuous actions, enabling high-frequency control (up to _∼_ 50 Hz). 

- SpatialVLA (Qu et al., 2025): A VLA backbone with 3D spatial awareness via two representations: ego3D position encoding, which injects egocentric 3D cues into visual tokens; and adaptive action grids, which discretize continuous robot motions into data-driven spatial grids and learn action tokens aligned to the workspace geometry. 

## **B.2. Policy Evaluation** 

**Evaluation Procedure.** Starting from the initial observation _x_ 0 (with optional instruction _c_ ), we evaluate each VLA policy _π_ by simulating its closed-loop behavior with BridgeV2W in an autoregressive manner. At step _t_ , the policy consumes the current input image _xt_ and outputs an action chunk **a** _t_ : _t_ + _K−_ 1 = _π_ ( _xt, c_ ). Each action in the chunk is mapped to a pixel-aligned embodiment mask via _ϕ_ , yielding a mask sequence _mt_ : _t_ + _K−_ 1 = _ϕ_ ( **a** _t_ : _t_ + _K−_ 1). The world model _W_ then predicts a _video clip_ conditioned on _xt_ and the mask sequence, 

**x** ˆ _t_ +1: _t_ + _K_ = _W_ ( _xt, mt_ : _t_ + _K−_ 1) _,_ 

16 

**Bridging Video Generation to Embodied World Models** 

where **x** ˆ _t_ +1: _t_ + _K_ denotes _K_ consecutive future frames. We take the _last_ frame of this clip, _x_ ˆ _t_ + _K_ , as the next policy input by setting _xt_ + _K ← x_ ˆ _t_ + _K_ , and continue the rollout by re-querying _π_ to obtain the next action chunk. This loop proceeds until a horizon _H_ is reached, producing a synthetic trajectory _{_ **x** ˆ _t_ +1: _t_ + _K}_<sup>_H_</sup> _t_ =0<sup>_−_1that approximates how the scene would evolve</sup> under each policy. 

**Implementation Details.** BridgeV2W is trained with an action chunk length of 25. For VLA baselines whose chunk length is shorter than 25, we pad the sequence by repeating the final action until it reaches length 25. Task success is assessed by human raters who judge the BridgeV2W-generated videos. As future work, we plan to incorporate large multimodal models (e.g., ChatGPT (Achiam et al., 2023), Qwen (Yang et al., 2025a)) to automate the evaluation of generated rollouts. **Metrics** Let _R_ = _{Ri}_<sup>_N_</sup> _i_ =1<sup>denote real-world success rates and</sup><sup>_RS_=</sup><sup>_{RS,i}_</sup> _i_<sup>_N_</sup> =1<sup>denote BridgeV2W success rates for the</sup> same _N_ policies. We adopt two metrics to evaluate the effectiveness of BridgeV2W as a proxy for policy evaluation: 

(1) Mean Maximum Rank Violation (MMRV) (Li et al., 2025c) quantifies how severely the proxy misorders policies: 


Here 1 [ _·_ ] is the indicator function; a larger MMRV means worse ranking consistency between BridgeV2W and real-world performance. 

(2) Pearson correlation coefficient (Pearson _r_ ), which measures the linear association between _R_ and _RS_ : 


Values close to 1 indicate that higher real-world success corresponds to proportionally higher BridgeV2W success. 

**Failure Cases** As summarized in Figure 4, BridgeV2W tends to overestimate success relative to real-world evaluations. To examine this bias, we conduct a case study illustrated in Figure 8: the left panel shows the correct action sequence from _π_ 0; in the middle and right panels we inject _y_ -axis offsets of _−_ 0 _._ 02 m and _−_ 0 _._ 10 m, respectively. BridgeV2W still predicts a successful grasp under small perturbations, whereas such deviations cause failure on the real robot. We attribute this to training predominantly on expert demonstrations, which encourages the model to “recover” minor errors. Incorporating imperfect and failure trajectories during training (e.g., explicit negatives or perturbation-based augmentation) may improve alignment with real-world policy evaluation. 


_Figure 8._ Case study of the failure cases in policy evaluation. 

## **B.3. Goal-Image Conditioned Manipulation.** 

**Planning Algorithm.** Following V-JEPA 2 (Assran et al., 2025) settings, we adopt the Cross-Entropy Method (CEM) within a Model Predictive Control (MPC) loop to plan. The detailed algorithm is illustrated in Algorithm 1. Given the current RGB frame _x_ 0, the robot pose _p_ 0 = [ _x, y, z, r, p, y, g_ ], a goal frame _x_<sup>goal</sup> , horizon _H_ , world model _W_ , and CEM hyperparameters (iterations _T_ , samples per iteration _S_ , elites _k_ ), we maintain, for each step _h ∈{_ 1 _, . . . , H}_ , a factorized 

17 

**Bridging Video Generation to Embodied World Models** 

sampling distribution over 7-DoF actions: a Gaussian _N_ ( _µh,_ Σ _h_ ) on pose _increments_ ∆ _qh ∈_ R<sup>6</sup> (translation _xyz_ , rotation _rpy_ ), and a Bernoulli parameter _πh ∈_ (0 _,_ 1) for the gripper _gh ∈{_ 0 _,_ 1 _}_ . At the start of each MPC cycle we initialize _{_ ( _µh,_ Σ _h, πh_ ) _}_<sup>_H_</sup> _h_ =1<sup>and run</sup><sup>_T_CEM refinements.In each refinement, we draw</sup><sup>_S_candidate sequences</sup><sup>_A_(</sup><sup>_s_)=</sup><sup>_{a_(</sup> _h_<sup>_s_)</sup><sup>_}_</sup> _h_<sup>_H_</sup> =1<sup>by</sup> sampling ∆ _qh_<sup>(</sup><sup>_s_)</sup> _∼N_ ( _µh,_ Σ _h_ ) and _gh_<sup>(</sup><sup>_s_)</sup> _∼_ Bernoulli( _πh_ ), then forming _a_<sup>(</sup> _h_<sup>_s_)</sup> = [∆ _qh,_<sup>(</sup><sup>_s_</sup> 1:3<sup>)</sup><sup>_,_∆</sup><sup>_q_</sup> _h,_<sup>(</sup><sup>_s_</sup> 4:6<sup>)</sup><sup>_,g_</sup> _h_<sup>(</sup><sup>_s_)].Each candidate is</sup> rolled out with the world model to obtain the terminal prediction 


and scored in a VAE latent space using mean _ℓ_ 1 distance. Let Enc( _·_ ) be the encoder and _d_ the latent dimension; define 


We select the _k_ elites with the lowest losses and refit each step’s distributions: ( _µh,_ Σ _h_ ) to the empirical mean/covariance of _{_ ∆ _qh_<sup>(</sup><sup>_s_)</sup><sup>_}s∈I_and</sup><sup>_πh_=1</sup> � _s∈I_<sup>1</sup><sup>_{g_</sup> _h_<sup>(</sup><sup>_s_)</sup> = 1 _}_ . After _T_ refinements, we extract the receding-horizon plan by taking per-step _k_ means and a 0 _._ 5 threshold for the gripper, 


execute only the first control _a_<sup>_⋆_</sup> 1<sup>=</sup><sup>_A⋆_</sup> 1<sup>, observe the new (</sup><sup>_x_0</sup><sup>_, p_0), and re-plan with a shifted horizon until the goal is reached</sup> or a time limit is met. 

**Implementation Details.** Each task is evaluated over 10 trials per method (VLA baselines and BridgeV2W). We discretize the translational action space with a step of 0 _._ 05 m along each axis, and the rotational space with a step of 20<sup>_◦_</sup> (RPY). For simple pick-and-place tasks, we restrict the search to translation only and set rotational deltas to zero. Gripper commands are determined by a simple heuristic (open during approach, close at grasp, release at the target) without additional search. 

**Planning Results Using BridgeV2W vs. VLA Baselines** Table 10 reports goal-image–based manipulation planning results. BridgeV2W attains strong performance on pick-and-place tasks but lags on tasks that require substantial rotations, likely because searching rotational subspaces is challenging for the world model during planning. 

_Table 10._ BridgeV2W for goal-conditioned planning 

|Tasks|OpenVLA-OFT|_π_0|SpatialVLA|BridgeV2W|
|---|---|---|---|---|
|Put on plate|4 / 10|8 / 10|9 / 10|5 / 10|
|Put in shelf|6 / 10|9 / 10|8 / 10|5 / 10|
|Close Drawer|5 / 10|8 / 10|6 / 10|5 / 10|
|Flip Cip|2 / 10|7 / 10|7 / 10|3 / 10|
|All Tasks|17 / 40|32 / 40|30 / 40|18 / 40|


**Qualitative Results and Failure Cases** Figure 9 presents goal-conditioned planning rollouts generated by BridgeV2W. In the two pick-and-place tasks ( _put on plate_ and _put in shelf_ ), the planner finds feasible action sequences without extensive exploration of rotational subspaces. In _close drawer_ , the arm fails to execute the wrist rotation needed to approach and pull the handle, leading to a stall near the drawer front. In _flip cup_ , the robot successfully grasps the cup but does not achieve the target orientation before placement, yielding an incorrect final pose. 

**Analysis of Rotation-Heavy Manipulation Tasks** Rotation-intensive tasks introduce a significantly more complex action-search landscape than translation-dominated pick-and-place settings. In these tasks, the gripper must rotate around multiple axes while maintaining contact consistency, leading to a higher-dimensional and highly non-convex optimization space for Cross-Entropy Method (CEM) planning. 

Despite the inherent difficulty of these tasks, BridgeV2W itself remains stable under large wrist rotations. As shown in Table 11, metrics such as LPIPS, FVD, and Mask-IoU do not degrade for rotation-heavy tasks, and the predicted trajectories remain visually coherent. This indicates that the world model captures the necessary rotational dynamics and that mask conditioning does not collapse under self-occlusion or viewpoint changes. Our experiments reveal that the dominant source of error arises from the action-search process rather than the world model. Na¨ıve CEM search distributes samples uniformly 

18 

**Bridging Video Generation to Embodied World Models** 

_Table 11._ Model quality metrics and real-world success rates on manipulation tasks. 

|**Task**|**PSNR↑**|**SSIM↑**|**LPIPS↓**|**FVD↓**|**Mask-IoU↑**|
|---|---|---|---|---|---|
|Put on plate|26.25|0.906|0.097|179.0|63.8|
|Put in shelf|26.17|0.914|0.098|190.1|61.4|
|Close drawer|26.42|0.925|0.091|175.6|64.9|
|Flip cup|26.02|0.901|0.103|180.9|62.1|


across translation and rotation, causing the planner to under-explore the rotational subspace. This leads to failure cases where the robot reaches the correct position but does not complete the required rotation. 

We evaluate simple refinements to the search procedure within the same BridgeV2W model: 

- **Rotation-first search** : temporarily freeze translation while optimizing rotation. 

- **Sample reallocation** : increase the number of CEM samples dedicated to rotational dimensions. 

- **Axis-wise decomposition** : search yaw, pitch, and roll components sequentially. 

These strategies yield clear improvements on rotation-heavy tasks: success rates increase from 3/10 to 5/10 for _close drawer_ and from 0/10 to 3/10 for _flip cup_ . Importantly, these gains are achieved without modifying BridgeV2W, indicating that the model already encodes sufficient geometry and dynamics for rotation reasoning. 

**Integration with VLA Frameworks for Closed-Loop Planning** BridgeV2W can be used as a predictive critic within modern vision–language–action (VLA) frameworks (Black et al., 2024; Kim et al., 2025; Li et al., 2025a), enabling efficient closed-loop planning. To examine this capability, we conducted preliminary real-world experiments in which OpenVLA-OFT served as the action proposer. At each control step, OpenVLA-OFT generated ten action rollouts by varying its decoding temperature, and BridgeV2W predicted the visual outcomes of each rollout. The rollout whose predicted outcome best matched the task objective was selected and executed. 

This two-stage OpenVLA-OFT + BridgeV2W framework yields consistent improvements over OpenVLA alone across multiple manipulation tasks (Table 12). Because VLA models generate structured and semantically coherent action hypotheses, this closed-loop paradigm is substantially more search-efficient than offline CEM, which must sample blindly in the continuous action space. The primary limitation is increased inference latency due to evaluating multiple rollouts per step. Potential remedies include distilling BridgeV2W into a lighter predictive model, adding a small learned value head for faster scoring, or caching intermediate video features for incremental rollout evaluation. 

_Table 12._ Real-world success rates when integrating BridgeV2W into an OpenVLA-OFT closed-loop planning pipeline. 

|**Task**|**OpenVLA-OFT**|**OpenVLA + BridgeV2W**|
|---|---|---|
|Put on plate|4/10|6/10|
|Put in shelf|6/10|7/10|
|Close drawer|5/10|5/10|
|Flip cup|2/10|4/10|
|All Tasks|17/40|**22/40**|


# **C. Additional Visualization Results** 

This section presents additional video generation examples produced by **BridgeV2W** . Figure 10 shows in-domain DROID rollouts (top row) alongside the same action sequences rendered from unseen camera viewpoints (bottom row), highlighting viewpoint robustness. Figure 11 illustrates DROID scenes under unseen backgrounds to assess generalization beyond the training distribution. Figure 12 reports examples on the AgiBot G1 dataset to demonstrate cross-embodiment applicability. 

19 

**Bridging Video Generation to Embodied World Models** 

**Algorithm 1:** CEM–MPC planning with BridgeV2W **Input:** Current frame _x_ 0, current pose _p_ 0 = [ _x, y, z, r, p, y, g_ ] (Euler xyz + gripper); Goal frame _x_<sup>goal</sup> ; world model _W_ ; horizon _H_ ; CEM iterations _T_ , VAE Encoder Enc, samples _S_ , elites _k_ ; Init per-step Gaussian ( _µh,_ Σ _h_ ) over ∆ _qh ∈_ R<sup>6</sup> ( _xyz, rpy_ ), and Bernoulli parameter _πh ∈_ (0 _,_ 1) for _gh ∈{_ 0 _,_ 1 _}_ ; Objective _ℓ_ ( _·, ·_ ) (default mean _L_ 1 on latent space). **Output:** First control _a_<sup>_⋆_</sup> 1<sup>and (optionally) plan</sup><sup>_A⋆_</sup> 1: _H_<sup>.</sup> 1 **repeat** // 1) CEM initialization 2 initialize _{µh,_ Σ _h, πh}_<sup>_H_</sup> _h_ =1 3 **for** _t ←_ 1 **to** _T_ **do** 4 **for** _s ←_ 1 **to** _S_ **do** 5 _x_<sup>(</sup> 1<sup>_s_)</sup> _← x_ 0 _, p_<sup>(</sup> 1<sup>_s_)</sup> _← p_ 0 _, A_<sup>(</sup><sup>_s_)</sup> _←∅_ 6 **for** _h ←_ 1 **to** _H_ **do** // Sample 7-DoF action: _xyz_ + _rpy_ + _gripper_ 7 ∆ _qh ∼N_ ( _µh,_ Σ _h_ ), _gh ∼_ Bernoulli( _πh_ ) 8 _ah ←_ [∆ _qh,_ 1:3 _,_ ∆ _qh,_ 4:6 _, gh_ ] 9 Append _ah_ to _A_<sup>(</sup><sup>_s_)</sup> 10 **end** 11 _x_<sup>(</sup> _H_<sup>_s_)</sup> +1<sup>_←W_(</sup><sup>_x_0</sup><sup>_, A_(</sup><sup>_s_))</sup> 12 _L_<sup>(</sup><sup>_s_)</sup> _← ℓ_ (Enc( _x_<sup>(</sup> _H_<sup>_s_)</sup> +1<sup>)</sup><sup>_,_Enc(</sup><sup>_x_goal))</sup> 13 **end** // 2) Select elites and refit distributions 14 _I ←_ argsort( _{L_<sup>(</sup><sup>_s_)</sup> _}_ )[: _k_ ] 15 **for** _h ←_ 1 **to** _H_ **do** 16 Fit _µh,_ Σ _h_ to _{_ ∆ _qh_<sup>(</sup><sup>_s_)</sup><sup>_}s∈I_</sup> 17 _πh ← k_<sup><u>1</u></sup> � _s∈I_<sup>1</sup><sup>_{g_</sup> _h_<sup>(</sup><sup>_s_)</sup> = 1 _}_ 18 **end** 19 **end** // 3) Extract plan & execute 20 _A_<sup>_⋆_</sup> _h_<sup>_←_[</sup><sup>_µh_(1:3)</sup><sup>_,µh_(4:6)</sup><sup>_,_1</sup><sup>_{πh≥_0</sup><sup>_._5</sup><sup>_}_]</sup> for _h_ = 1 _..H_ 21 Apply _a_<sup>_⋆_</sup> 1<sup>_←A⋆_</sup> 1<sup>, observe new (</sup><sup>_x_0</sup><sup>_, p_0), recede horizon</sup> 22 **until** _goal reached_ **or** _time limit_ 

20 

**Bridging Video Generation to Embodied World Models** 


_Figure 9._ Qualitative rollouts for goal-conditioned planning with BridgeV2W. Top row: initial observation and two goal images. Bottom row: model-predicted execution frames. 

21 

**Bridging Video Generation to Embodied World Models** 


_Figure 10._ Visualization results in DROID of in-domain camera and unseen camera. 

22 

**Bridging Video Generation to Embodied World Models** 


_Figure 11._ Visualization results in DROID of unseen scenes. 

23 

**Bridging Video Generation to Embodied World Models** 


_Figure 12._ Visualization results in AgiBot G1. 

24 

