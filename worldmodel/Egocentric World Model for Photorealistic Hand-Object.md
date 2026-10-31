---
title: "Egocentric World Model for Photorealistic Hand-Object Interaction Synthesis"
date: "2026-03-13"
authors: "Dayou Li; Lulin Liu; Bangya Liu; Shijie Zhou; Jiu Feng; Ziqi Lu"
url: https://arxiv.org/abs/2603.13615
pdf: https://arxiv.org/pdf/2603.13615
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.13615)** / [論文ページ](https://arxiv.org/abs/2603.13615)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Egocentric World Model for Photorealistic Hand-Object Interaction Synthesis** 

Dayou Li<sup>1*</sup> , Lulin Liu<sup>1</sup><sup>_,_2*</sup> , Bangya Liu<sup>3</sup> , Shijie Zhou<sup>4</sup> , Jiu Feng<sup>5</sup> , Ziqi Lu<sup>6</sup> , Minghui Zheng<sup>1</sup> , Chenyu You<sup>7</sup> , Zhiwen Fan<sup>1�</sup> 

   - 1Texas A&M University 2University of Minnesota 

- 3University of Wisconsin–Madison 4University of California, Los Angeles 

      - 5University of Texas at Austin 6Amazon 

> 7State University of New York at Stony Brook 

**Abstract.** To serve as a scalable data source for embodied AI, world models should act as true simulators that infer interaction dynamics strictly from user actions, rather than mere conditional video generators relying on privileged future object states. In this context, egocentric Human–Object Interaction (HOI) world models are critical for predicting physically grounded first-person rollouts. However, building such models is profoundly challenging due to rapid head motions, severe occlusions, and high-DoF hand articulations that abruptly alter contact topologies. Consequently, existing approaches often circumvent these physics challenges by resorting to conditional video generation with access to known future object trajectories. We introduce EgoHOI, an egocentric HOI world model that breaks away from this shortcut to simulate photorealistic, contact-consistent interactions from action signals alone. To ensure physical accuracy without future-state inputs, EgoHOI distills geometric and kinematic priors from 3D estimates into physics-informed embeddings. These embeddings regularize the egocentric rollouts toward physically valid dynamics. Experiments on the HOT3D dataset demonstrate consistent gains over strong baselines, and ablations validate the effectiveness of our physics-informed design. 

**Keywords:** Egocentric vision · World model · Hand-object Interaction 

## **1 Introduction** 

Egocentric Human-Object Interaction (HOI) world models aim to simulate physically grounded interaction dynamics from a first-person perspective driven by user controls. The resulting predictive rollouts are increasingly important beyond visual synthesis; they can serve as scalable training and evaluation data for a wide range of downstream tasks, including dexterous manipulation [11,29,51], VisionLanguage-Actions Models (VLAs) [8,44,45], spatiotemporal reasoning [53], physical intelligence [26], and data augmentation [23]. Despite this potential, the 

> * Equal contribution. 

- Project page: `https://egohoi.github.io/` 

2 D. Li, L. Liu et al. 


**Fig. 1: Qualitative comparison between a baseline world model and EgoHOI.** Starting from the same first frame, EgoHOI integrates physics-informed embeddings to model hand–object interaction dynamics, improving ego-motion consistency, kinematic fidelity, and object integrity over time. Zoom-ins highlight clearer contact details and reduced drift. 

inherent complexity of egocentric HOI poses major challenges. High-DoF hand articulation rapidly changes contact topologies and object states, while severe occlusions and small head motions make the interaction highly ambiguous. The difficulty of this domain is also evident in recent spatiotemporal representation research: as demonstrated by VLM4D [53], even state-of-the-art VLMs still struggle to reliably understand and reason about the complex dynamics in egocentric HOI videos. If interpreting these interactions is already challenging, building an egocentric HOI world model is even harder. Such a model must go beyond passive observation and actively generate future frames that satisfy user-specified actions, physical laws, and dynamical consistency, producing reliable physical rollouts rather than only visual plausibility. 

Despite recent progress in HOI video generation, a reliable egocentric HOI world model remains largely absent. This gap stems from two fundamental limitations in existing pipelines. First, current HOI video generation [30, 34, 48] is predominantly studied in static, exocentric views. These third-person perspectives do not directly support first-person rollouts with dynamic interactions, which are essential in embodied AI and robotics. Second, many existing approaches [10,18,19,27] condition heavily on privileged future object information, such as ground-truth trajectories and waypoints. By explicitly defining how the object should move in the future, these methods largely bypass the core challenge of contact-driven dynamics reasoning. This turns the task into conditional video 

EgoHOI 3 

generation, which conflicts with the formulation of a world model that must infer interaction dynamics and future states strictly from current observations and user-specified actions. Ideally, the model should predict future hand-object interaction purely from action signals, rather than replaying privileged future object states. Because this removes future-state shortcuts, simply scaling RGB data is insufficient for physical accuracy. Instead, the model should be augmented with physics-informed embeddings that inject explicit metric and kinematic structure. Fortunately, recent advances in 3D foundation models for geometry [20, 37, 38] and hand pose [31] now make it increasingly practical to extract these crucial metric and kinematic priors directly from unstructured videos, opening opportunities to model high-DoF interaction through explicit 3D hand kinematics, camera motion, and contact-aware geometry. 

In this paper, we present EgoHOI, an egocentric HOI world model for photorealistic hand-object interaction simulation that integrates physics-informed embeddings into the generative rollout process. EgoHOI uses interpretable estimates from scene, hand, and geometry models, and converts them into embeddings that provide complementary physical structure for learning egocentric dynamics, including hand kinematics, metric-scale ego motion, and object integrity. These embeddings are incorporated through lightweight adapters to preserve the pretrained generative prior while imposing the metric grounding, temporal consistency, and contact-aware dynamics. Unlike earlier trials utilizing access to privileged future states, EgoHOI enables causal simulation of physically plausible hand-object interactions while retaining the generative diversity and reconstruction quality trained from massive data. We demonstrate an example in Fig. 1 to show the resulting simulated rollouts, and summarize our contributions as follows: 

- We introduce EgoHOI, an egocentric HOI world model that simulates firstperson hand–object interaction dynamics under user-specified actions and controls, without privileged future object states. 

- We introduce physics-informed embeddings derived from 3D geometry and kinematic priors to regularize egocentric HOI rollouts toward physically consistent interaction dynamics. 

- We show EgoHOI better aligns rollouts with user actions and improves hand–object interaction realism, with comprehensive metrics and ablations validating our physics-informed embeddings. 

## **2 Related Works** 

**Egocentric World Model & Video Generation.** Egocentric World model aims to simulate the physical world by predicting future visual observations in a first-person viewpoint. Recently, there has been progress in the general world models [6, 33], which usually take in detailed language descriptions as control signals to generate future rollouts. For instance, Nvidia’s Cosmos [1], which was trained on 100M language-video pairs, can capture diverse real-world physics and 

4 D. Li, L. Liu et al. 

be fine-tuned for specific tasks. However, most of these models operate primarily in image space, which makes physically plausible rollouts under high degrees of freedom still challenging in practice. Unlike general world models, egocentric world models often focus on more challenging tasks. In egocentric settings, viewpoints constantly change, while hand-object interactions frequently influence the dynamic evolution of the scene, making it significantly more difficult for world models to simulate [3,13,16]. PlayerOne [35] drives a first-person simulator with whole-body motion to maintain consistent visual rendering across scenes, while GEM [14] jointly generates RGB and depth streams conditioned on ego-trajectory and object identity features. Beyond PlayerOne and GEM, many existing efforts focus on designing view-transformation or hand-trajectory controls for first-person generation, rather than grounding rollouts in reconstructionbased 3D priors or causal hand–object dynamics. EgoExo-Gen [41] is one example that generates a first-person video by watching a third-person view of the same scene. Zhang et al. [2] first predict a coarse hand trajectory and then condition a latent diffusion model to generate future frames. 

Overall, prior egocentric world models focus on plausible first-person rendering, but hand–object interaction is less emphasized, and maintaining physically consistent interaction dynamics remains difficult. 

**Hand-Object Interactions Synthesis.** Hand–object interaction (HOI) synthesis targets interactions that are visually realistic and physically plausible by jointly modeling appearance, relative geometry, and contact semantics [7,9,12, 22,24,25,28]. In the egocentric setting, MEgoHand [52] synthesizes hand–object motion from first-person RGB together with text and an initial hand pose. Beyond egocentric inputs, a dominant trend in general HOI generation is referenceconditioned interaction alignment, where models leverage reference signals such as target poses, relative transforms, or motion trajectories to improve controllability and contact quality. These include image-level refinement of hand–object alignment [19], geometry and relation aware motion generation with diffusion [43], multimodal video generation guided by an HOI adapter [18], open world synthesis with affordance guidance and physics refinement [49], and tokenized sequence models that translate between language and long 3D HOI sequences [17]. 

## **3 Method** 

### **3.1 Preliminary** 

**World Model Formulation** A world model **f** _θ_ captures action-driven internal state dynamics and enables rollouts by iteratively predicting how the state evolves under actions. Let _xt ∈X_ denote the internal state and let _at_ denote the action applied at time _t_ . The action-driven transition dynamics are: 


and the observation function _gϕ_ maps the internal state to the observation space: 


**Fig. 2: Overview of EgoHOI pipeline.** We formulate EgoHOI as an egocentric world model that represents frames with a latent internal state and predicts action-driven transitions with a DiT backbone. Physics-informed embeddings distilled from reconstruction-based 3D priors, together with the first-frame object appearance, are integrated into the latent dynamics via lightweight adapters, enabling realistic hand–object interactions, geometry-consistent ego-motion, and stable object identity under viewpoint changes. 

where _ot_ denotes the observable signal. Given an initial observation _o_ 1, an encoder produces the initial internal state _x_ 1 = _eϕ_ ( _o_ 1). A rollout over horizon _L_ is obtained by recursively applying **f** _θ_ under an action sequence _{at}_<sup>_L_</sup> _t_ =1<sup>and</sup> mapping the resulting latent states to predicted observations via _gϕ_ . 

In this view, a world model serves as an action-driven simulator: actions are treated as interventions that induce state transitions, and rollouts should predict the causal effects of actions on the world state, instead of only reconstructing the agent’s kinematic trajectory. In EgoHOI’s setting, we instantiate the transition model **f** _θ_ with a DiT backbone to realize action-driven evolution of the model’s internal state in a VAE latent space; _eϕ_ and _gϕ_ are the VAE encoder and decoder that map video frames to and from this latent representation. 

**Diffusion Process** Video generative models [4, 15] generates samples by iteratively denoising random noise through a learned reverse diffusion process. Formally, we consider a latent representation _z_ 0 of an initial clean data sample obtained from a variational autoencoder (VAE) that encodes the video into its latent space. A forward (noising) process _q_ gradually adds Gaussian noise to _z_ 0 over _T_ time steps, producing a sequence _z_ 1 _, z_ 2 _, . . . , zT_ . At each step, noise is added according to a variance schedule _βt_<sup>_T_</sup> =1<sup>.Acommonformulationis:</sup> 


6 D. Li, L. Liu et al. 

with _βt ∈_ (0 _,_ 1) controlling the noise level. As _t_ increases, the latent _zt_ becomes increasingly noisy; in the limit _zT_ approaches a standard Gaussian noise. Equivalently, one can express _zt_ in closed form as a noisy mixture of the original latent and noise: 


where _αt_ := 1 _−βt_ , and _α_ ¯ _t_ :=<sup>�</sup><sup>_t_</sup> _s_ =1<sup>_αs_is the accumulated noise attenuation. Here</sup> _ϵ ∼N_ (0 _,_ **I** ) represents standard Gaussian noise. The reverse process learns to invert this degradation by removing the noise from _zt_ to reconstruct the original latent representation. The denoiser is trained to predict the noise added to the latent, with respect to the loss function: 


By minimizing this objective, the model learns to remove noise and recover the clean latent _z_ 0 from a noisy _zt_ . 

### **3.2 Latent-Space World Modeling for Egocentric HOI** 

We model egocentric hand–object interaction (HOI) synthesis as action-driven world modeling in a compact latent state space. Given the first-frame observation **I1** _∈_ R<sup>_H×W ×_3</sup> , we obtain an initial latent state _z_ 1 via the VAE encoder. The action signal at each step _t_ is specified by hand kinematics **H**<sup>_t_</sup> and metric head motion **C**<sup>_t_</sup> , forming an _L_ -step action sequence _{_ ( **H**<sup>_t_</sup> _,_ **C**<sup>_t_</sup> ) _}_<sup>_L_</sup> _t_ =1<sup>.Ourgoalisto</sup> predict the temporal evolution of latent states under actions and decode them into future first-person observations. Concretely, the world model defines actiondriven latent dynamics that evolve the state over time, 


and the predicted observation rollout is obtained by decoding _{zt}_ into<sup>ˆ</sup> **I** 2: _L_ +1. 

Modeling egocentric HOI dynamics in latent space is challenging due to the coupled effects of high-DoF hand articulation, metric ego motion, and contactdriven object dynamics. We regularize the action-driven latent evolution without relying on privileged future object states. The next section introduces physicsinformed embeddings distilled from 3D geometric and kinematic estimates, which promote physically plausible latent dynamics. 

### **3.3 Physics-Informed Embeddings** 

To constrain HOI rollouts without using privileged future object states, we distill 3D geometric and kinematic estimates into compact physics-informed embeddings. Concretely, we derive three embeddings from complementary sources of structure: (i) hand kinematics that describe high-DoF articulation, (ii) metric ego motion that encodes the viewpoint trajectory, and (iii) an object-entity anchor tied to the first frame to stabilize object-centric appearance under interaction. These embeddings are injected into the latent dynamics to provide per-step geometric and kinematic context, thereby guiding state evolution toward physically plausible dynamics. 

EgoHOI 7 

**Hand Kinematic Embeddings (HKE).** The goal of HKE is to capture dense hand motion structure from reconstructed 3D hand estimates, which is essential for contact-consistent HOI rollouts under high-DoF articulation. Rather than representing actions as sparse coordinate vectors, we use explicit per-frame hand renders obtained from reconstructed meshes as a dense 3D representation. We stack a sequence of hand render frames _{Ht}_<sup>_L_</sup> _t_ =1<sup>and encode them with a tempo-</sup> ral 3D convolutional stack with SiLU activations, which gradually increases the channel dimension and maps the hand stream to the shared the 5120-dimension latent space. To stabilize hand identity and reduce temporal drift, we add a reference-hand branch that encodes the first-frame hand pose **P**<sup>1</sup> into a compact feature **R** ref _∈_ R<sup>_H′′×W ′′×_20</sup> via a six-layer 2D convolutional pyramid (3 _×_ 3 Conv + SiLU). Together, the temporal 3D Conv stack and the reference encoder produce hand kinematic embeddings that preserve fine-grained articulation structure and support physically plausible hand evolution during rollouts. 

**Ego-Motion Embeddings (EME).** Ego head motion is a dominant factor in first-person rollouts, where viewpoint changes couple tightly with hand motion and occlusions. EME encodes metric head trajectory estimates into embeddings aligned with the latent space, enabling geometry-consistent viewpoint evolution over time. Given a head pose sequence _{_ **C**<sup>_t_</sup> _}_<sup>_L_</sup> _t_ =1<sup>withintrinsics</sup><sup>**K**</sup><sup>_∈_R3</sup><sup>_×_3and</sup> extrinsics **E** = [ **R** : **t** ] _∈_ R<sup>3</sup><sup>_×_4</sup> (relative to the first frame), we adopt Plücker embeddings to represent the per-pixel ray field induced by the head pose. For each pixel ( _u, v_ ), its embedding is **p** _u,v_ = ( **o** _×_ **d** _u,v,_ **d** _u,v_ ) _∈_ R<sup>6</sup> , where **o** is the head-frame optical center and **d** _u,v_ is the world-direction ray computed as: 


This ray-based representation is invariant to the choice of scene origin and preserves metric structure under head motion. By representing ego motion as an image-aligned ray field, it avoids collapsing geometry into a low-dimensional pose vector and instead imposes spatially resolved constraints on viewpoint evolution. We stack per-frame Plücker tensors into a trajectory representation, process it with causal 3D convolutions and hybrid spatiotemporal blocks that combine 2D residual convolutions with temporal self-attention, and finally use a projection head and patchifier to map features into the latent grid, yielding ego-motion embeddings that regularize long-horizon viewpoint dynamics. 

**Object Entity Embeddings (OEE).** Egocentric rollouts can suffer from object entity drift, which often appears as instability in color, texture, and fine details under rapid ego motion and partial occlusions. To stabilize object entities over time, OEE anchors each object to the first frame, providing a persistent reference that supports coherent HOI evolution across the rollout. Concretely, we use the first-frame object segmentation image, obtained from an off-the-shelf 

8 D. Li, L. Liu et al. 

segmentation model, to isolate object-centric evidence and reduce background interference under viewpoint changes. The segmentation is encoded by the frozen video VAE encoder into a latent grid, and a 3D convolutional patchifier converts it into tokens aligned with the main latent stream. Operating in the same latent parameterization as the backbone, OEE yields features that mitigate drift and preserve object-centric details throughout the rollout. 

### **3.4 Latent Space Integration** 

We incorporate physics-informed embeddings into the frozen Wan-DiT in a single token-space forward pass by first aligning each embedding stream to the main token layout and shared token dimension _d_ . Let the Wan-VAE latent be _z ∈_ R<sup>_B×F ×H×W ×C_</sup> and the corresponding main token sequence be **T** main _∈_ R<sup>_B×N×d_</sup> . Each embedding tensor is projected and patchified into an aligned token sequence compatible with **T** main, enabling Wan-DiT to leverage physics-informed structure for latent evolution without modifying the original backbone architecture. 

**Action-Driven Token.** The hand encoder produces hand tokens **T**<sup>HKE</sup> in R<sup>_B×N×d_</sup> , which are fused into the main token stream via a gated residual update: 


where _γh_ is a learnable gate. In parallel, the reference-hand branch produces a first-frame hand feature that is added to the first-frame latent and concatenated with the noise latent before patchification, tying the initial hand configuration to the latent state space. The ego-motion adapter outputs geometry tokens **T**<sup>EME</sup> _∈_ R<sup>_B×N×d_</sup> . For compatibility with the extended sequence length introduced below, we zero-pad **T**<sup>EME</sup> to obtain with the same length as the active token sequence. In the first _D_ DiT blocks, we apply per-block zero-initialized linear adapters **U** _l_ : R<sup>_d_</sup> _→_ R<sup>_d_</sup> to generate residuals: 


which are added to the block input. This construction regularizes viewpoint evolution under metric head motion while preserving backbone stability at initialization. 

**Object-Entity Token.** A object patchifier converts first-frame object entity features into tokens _T_<sup>OEE</sup> _∈_ R<sup>_B×N×d_</sup> . We assign shifted RoPE to spatially anchor these tokens as an independent reference stream, then append them to form the extended sequence 


Within each DiT block, the object-entity tokens participate as KV-only context during self-attention; only the main tokens are decoded, which provides a persistent entity reference that reduces drift in long rollouts. 

EgoHOI 

9 


**Fig. 3: Qualitative comparison with baselines.** Columns from left to right show the ground truth (GT), Wan, Cosmos-2B, Cosmos-14B, Uni3C, and our EgoHOI model. All methods receive the same first frame as input; compared with the baselines, our model better preserves hand and object geometry, maintains object identity, and produces more stable interaction dynamics over time. See the zooming boxes for comparison of the fine-grained details. 

**First-Frame Anchor** The first frame is encoded by the Wan VAE encoder as **Y** , and the reference-hand feature is added to **Y** to couple initial kinematics and appearance. Before patchification, we concatenate **Y** with the noise latent along the channel dimension. In parallel, the first frame is processed by the CLIP image encoder [32] to obtain global image embeddings; these embeddings are linearly projected and provided as fixed keys and values to the cross-attention layers of Wan-DiT, encouraging preservation of overall scene structure and appearance consistency during denoising. 

## **4 Experiment** 

### **4.1 Experiment Setup** 

**Implementation Details** We choose Wan 2.1 14B [36] as our model backbone. We start from the official checkpoint with LoRA rank set to 128 and LoRA alpha set to 128. The inference step and the learning rate are set to 50 and 1 _×_ 10<sup>_−_5</sup> . We use the Adam optimizer with BF16 precision. The cfg is set to 1.0. We train our model for 8000 steps on 16 NVIDIA H100 GPUs with a batch size of 1 and a sample resolution of 480 _×_ 480. The training process lasts for approximately 1 day. During training and inference, our frame length is set to 81. After training, our model can achieve 16 FPS when simulating human-object interaction. 

**Benchmark** Since there is no publicly available benchmark for world modeling in egocentric hand–object interaction, we construct an evaluation benchmark from HOT3D. We select 100 clips from scenes that are excluded from the training 

10 D. Li, L. Liu et al. 

**Table 1: Comparison with baselines.** We compare EgoHOI against a Wan backbone, Cosmos world models (2B, 14B) and Uni3C on frame prediction (PSNR/SSIM/LPIPS/Object-CLIP), ego-motion consistency (ATE/RRE/RPE), and kinematic fidelity (MR/MPJPE/RMSE). _↑_ higher is better, _↓_ lower is better. 

|**Method**|PSNR _↑_|Fram<br>SSIM _↑_|e Predic<br>LPIPS _↓_|tion<br>Object-CLIP _↑_|Ego-M<br>ATE _↓_|otion Co<br>RRE _↓_|nsistency<br>RPE _↓_|Kin<br>MR _↓_|ematic F<br>MPJPE|idelity<br>_↓_RMSE _↓_|
|---|---|---|---|---|---|---|---|---|---|---|
|Wan [36]|14.78|0.46|0.52|0.86|0.124|10.687|0.036|19.67%|0.049|0.083|
|Cosmos 2B [1]|15.49|0.56|0.41|0.87|0.116|9.515|0.026|16.23%|0.044|0.078|
|Cosmos 14B [1]|15.89|0.59|0.38|0.88|0.112|9.046|0.022|14.61%|0.041|0.074|
|Uni3C [5]|14.21|0.50|0.55|0.82|0.168|14.209|0.026|20.50%|0.073|0.089|
|Ours (EgoHOI)|**21.05**|**0.65**|**0.27**|**0.92**|**0.084 **|**5.192**|**0.021**|**5.84%**|**0.014**|**0.044**|


set. Each clip contains 150 frames and provides hand mesh renders and camera trajectories. Although our model operates on 81-frame rollouts, we make full use of each 150-frame clip by extracting multiple 81-frame sub-clips with a slidingwindow scheme, where the window length is fixed to 81 frames and is shifted along the clip to form evaluation samples. 

**Metrics** We evaluate the model from three complementary aspects: visual prediction, ego-trajectory consistency, and kinematic fidelity. Visual prediction is measured by PSNR, SSIM [39], LPIPS [47], and Object-CLIP [42]. We additionally report VBench [50] scores to assess perceptual and temporal quality, including Subject Consistency, Background Consistency, Motion Smoothness, Dynamic Degree, Aesthetic Quality, and Imaging Quality. Ego-motion consistency is quantified by ATE, RPE, and RRE between the estimated and ground-truth camera trajectories. Kinematic accuracy is computed with HaMeR [31] on both ground-truth and generated results, reporting Missing Ratio (MR), MPJPE, and RMSE on hand segmentation images. Details are in the supplementary material. 

### **4.2 Comparison with Baselines** 

We compare EgoHOI with three tiers of baselines for egocentric HOI rollouts. Wan [36] serves as a backbone-level video generation baseline. Cosmos 2B and 14B [1] are general-purpose world models at two parameter scales. We also include Uni3C [5], which offers stronger camera and human motion control. Wan and Cosmos are fine-tuned from released checkpoints using the same data and protocol as EgoHOI, and all methods are evaluated on the same datasets, metrics, and pipeline. Several recent egocentric world models [35, 40] are omitted because their implementations are not publicly available at submission time, which prevents a reproducible evaluation under our protocol. 

Table 1 reports frame prediction, ego-motion consistency, and kinematic fidelity. Scaling from Wan to Cosmos yields modest gains in frame quality, but motion-related performance remains limited. For example, Cosmos 14B reaches 

EgoHOI 11 

ATE 0.112 and MR 14.61%. Uni3C improves motion control, yet it degrades under rollout evaluation, with the largest ego-motion errors and weakest kinematic fidelity (ATE 0.168, RRE 14.209, MR 20.50%), suggesting that motion control alone does not recover contact-driven interaction dynamics. In contrast, EgoHOI performs best across all metric groups. It increases PSNR to 21.05 while substantially reducing ego-motion and hand kinematic errors, indicating that our physics-informed embedding extraction and injection improve interaction dynamics and temporal physical consistency, rather than only per-frame quality. Additional object-level comparisons are provided in the supplementary material, including OPE and OOE from our ablation study. 

For VBench in Tab. 2, EgoHOI achieves the highest subject consistency (95.51%), background consistency (94.91%), aesthetic quality (52.03%), and imaging quality (64.48%). Its lower Dynamic Degree (53.29%) reflects a design choice that prioritizes stable hand–object interactions over highly dynamic camera motion. Qualitatively (Fig. 3), Wan exhibits drift; Cosmos produces sharper frames but shows contact-region errors and small-object inconsistencies; Uni3C constrains camera motion but remains unreliable around contact. Overall, changing backbones, scaling model size, or enforcing motion control does not address the core challenge of egocentric HOI world models, whereas EgoHOI regularizes action-driven dynamics with physics-informed embeddings distilled from 3D priors to yield more plausible rollouts. More visualization is included in the supplementary material. 

**Table 2: VBench Evaluation of the Baselines.** Reported scores cover subject consistency, background consistency, motion smoothness, dynamic degree, aesthetic quality, and imaging quality. For the consistency and perceptual quality metrics, higher values correspond to better results, whereas dynamic degree characterizes how dynamic the generated content is rather than its realism. 

|**Method**|Subject<br>Consistency|Background<br>Consistency|Motion<br>Smoothness|Dynamic<br>Degree|Aesthetic<br>Quality|Imaging<br>Quality|
|---|---|---|---|---|---|---|
|Wan [36]|91.40%|93.14%|99.19%|64.75%|46.57%|58.58%|
|Cosmos 2B [1]|89.01%|93.00%|99.27%|87.50%|46.88%|62.98%|
|Cosmos 14B [1]|93.21%|93.56%|99.32%|**89.50%**|49.83%|63.78%|
|Uni3C [5]|91.91%|94.29%|99.33%|49.00%|47.03%|61.47%|
|Ours (EgoHOI)|**95.51%**|**94.91%**|**99.40%**|53.29%|**52.03%**|**64.48%**|


### **4.3 Ablation Study** 

We provide a detailed ablation analysis of EgoHOI by isolating how each component supports egocentric hand–object rollouts along three aspects: kinematic fidelity, object entity stability, and ego-motion consistency. Across kinematic fidelity (Tab. 3), ego-motion consistency (Tab. 4), and object integrity (Tab. 3), we compare several configurations of EgoHOI. Base uses the Wan 2.1 DiT video backbone without HKE, OEE, or EME. The HKE Injection, OEE Injection, and EME Injection variants each enable a single component on top of this backbone, which isolates its contribution under otherwise identical settings. EgoHOI 

12 D. Li, L. Liu et al. 


**Fig. 4: Qualitative results for ablation on kinematic fidelity.** Rows: GT, Base, HKE Injection, Ours (EgoHOI). HKE improves hand articulation stability and reduces local shape distortion. Zoom-in boxes highlight clearer hand–object contact details. The full model is the most stable, matching MR/MPJPE/RMSE. 

activates three components jointly and corresponds to the model used in the main experiments. All variants share the same data, training and optimization settings. We measure kinematic fidelity with MR, MPJPE, and RMSE, object entity with Object-CLIP together with VBench Subject Consistency and Imaging Quality, and ego-motion consistency with ATE, RPE, and RRE. 

**Study on Kinematic Fidelity** Tab. 3 examines the effect of HKE on hand state evolution over egocentric rollouts. Compared with the base variant, adding HKE reduces the MR and MPJPE to 6.47% and 0.015 from 28.77% and 0.576, respectively, indicating more reliable hand localization and substantially improved joint accuracy under interaction and partial occlusions. The reduction in RMSE further suggests that the hand region matches the ground truth more closely in both shape and RGB appearance over the sequence. The full model, which combines HKE with OEE and EME, further improves these metrics to 5.84%, 0.014, and 0.044. Qualitatively (Fig. 4), HKE mitigates hand-shape collapse and temporal fluctuations, while the full model yields the most stable hand evolution across time with fewer distortions during frequent hand–object interaction. 

**Table 3: Ablation on kinematic fidelity.** We ablate HKE Injection and report hand motion fidelity in generated videos using MR, MPJPE, and RMSE; _↓_ indicates lower is better. 

|**Method**|MR _↓_|MPJPE _↓_|RMSE _↓_|
|---|---|---|---|
|Ours (base)|28.77%|0.576|0.089|
|HKE Injection|6.47%|0.015|0.044|
|**Ours (EgoHOI)**|**5.84%**|**0.014**|**0.044**|


EgoHOI 13 

**Study on Ego-Motion Consistency** Tab. 4 and Fig. 5 examine ego-motion consistency over egocentric rollouts using ATE, RRE, and RPE. Compared with the base variant, enabling EME reduces these ego-motion errors and alleviates accumulated viewpoint drift over time. The full model achieves the best ego-motion metrics, reaching ATE/RRE/RPE of 0.084/5.192/0.021, which indicates closer agreement with the ground-truth viewpoint changes. Qualitatively (Fig. 5), EME injection yields more stable viewpoints with less drift across time, and the full model further improves global temporal coherence. Overall, improving ego-motion consistency is important for egocentric rollouts, and our ablation shows that EME is a key factor in reducing viewpoint drift and lowering ATE/RRE/RPE. 

**Table 4: Ablation on ego-motion consistency.** We evaluate the EME injection variant on long-horizon egocentric rollouts using ATE, RRE, and RPE, and compare it with the base backbone and the full EgoHOI model; _↓_ indicates more consistent ego-motion trajectories and reduced accumulated drift. 

|**Method**|ATE _↓_|RRE _↓_|RPE _↓_|
|---|---|---|---|
|Ours (base)|0.133|15.249|0.039|
|EME Injection|0.096|6.525|0.023|
|**Ours (EgoHOI)**|**0.084**|**5.192**|**0.021**|


**Fig. 5: Qualitative results for ablation of ego-motion consistency** Rows: GT, Base, EME Injection, Ours (EgoHOI). EME mitigates long-horizon ego-motion drift and improves viewpoint stability. Zoom-ins highlight cleaner details under viewpoint changes. The full model best matches ATE/RRE/RPE gains. 

**Study on Object Integrity.** Tab. 3 examines the effect of OEE on object integrity over egocentric rollouts. Compared with the base variant, OEE injection improves Object-CLIP from 0.81 to 0.83 and increases VBench Subject Consistency and Imaging Quality from 85.26% and 52.55% to 87.90% and 54.75%, 

14 D. Li, L. Liu et al. 

**Table 5: Ablation on object integrity.** We evaluate the OEE injection variant on egocentric rollouts, where object integrity refers to preserving object identity and maintaining stable object pose under interaction. We report Object CLIP, Subject Consistency, and Imaging Quality ( _↑_ is better), together with object position error (OPE) and 2D orientation error (OOE) computed from object masks ( _↓_ is better). 

|**Method**|Object<br>CLIP|<sup>_↑_</sup><br>Subject<br>Consistency <sup>_↑_</sup>|Imaging<br>Quality <sup>_↑_</sup>|OPE _↓_|OOE _↓_|
|---|---|---|---|---|---|
|Ours (base)|0.81|85.26%|52.55%|0.141|27.739|
|OEE Injection|0.83|87.90%|54.75%|0.131|24.124|
|**Ours (EgoHOI)**|**0.92**|**95.51%**|**64.48%**|**0.015**|**9.412**|


respectively, indicating more stable object appearance over time. We additionally report object pose errors in this ablation: object position error (OPE) and 2D orientation error (OOE) computed from object masks (details are included in supplementary materials). OEE injection reduces OPE from 0.141 to 0.131 and OOE from 27.739 to 24.124. The full model further improves these metrics to 0.92, 95.51%, and 64.48%, while substantially reducing OPE/OOE to 0.015/9.412. Qualitatively (Fig. 6), OEE injection mitigates drift in object appearance and reduces pose deviations, and the full model yields the most coherent object evolution during periods of frequent hand–object interaction. 


**Fig. 6: Qualitative results for ablation of object integrity.** Rows: GT, Base, OEE Injection, Ours (EgoHOI). OEE reduces texture flicker and appearance drift, preserving object-specific details through interaction and occlusion. Zoom-ins highlight more stable patterns and edges. The full model yields the most consistent results. 

## **5 Conclusion** 

We present EgoHOI, an egocentric world model that instantiates action-driven hand–object interaction dynamics with a large video diffusion backbone and a latent internal state. On HOT3D, EgoHOI improves visual quality, ego-motion consistency, and kinematic fidelity. Ablations show that physics-informed embeddings distilled from 3D priors, together with first-frame appearance, preserve object identity, stabilize viewpoints, and maintain realistic interactions. 

EgoHOI 

15 

## **References** 

1. Agarwal, N., Ali, A., Bala, M., Balaji, Y., Barker, E., Cai, T., Chattopadhyay, P., Chen, Y., Cui, Y., Ding, Y., et al.: Cosmos world foundation model platform for physical ai. arXiv preprint arXiv:2501.03575 (2025) 

2. Anonymous: Ego-centric predictive model conditioned on hand trajectories. In: Submitted to The Fourteenth International Conference on Learning Representations (2025), `https://openreview.net/forum?id=GTFISI3Clc` , under review 

3. Bai, Y., Tran, D., Bar, A., LeCun, Y., Darrell, T., Malik, J.: Whole-body conditioned egocentric video prediction. arXiv preprint arXiv:2506.21552 (2025) 

4. Blattmann, A., Dockhorn, T., Kulal, S., Mendelevitch, D., Kilian, M., Lorenz, D., Levi, Y., English, Z., Voleti, V., Letts, A., et al.: Stable video diffusion: Scaling latent video diffusion models to large datasets. CoRR (2023) 

5. Cao, C., Zhou, J., Li, S., Liang, J., Yu, C., Wang, F., Xue, X., Fu, Y.: Uni3c: Unifying precisely 3d-enhanced camera and human motion controls for video generation. arXiv preprint arXiv:2504.14899 (2025) 

6. Chen, D., Moutakanni, T., Chung, W., Bang, Y., Ji, Z., Bolourchi, A., Fung, P.: Planning with reasoning using vision language world model (2025), `https: //arxiv.org/abs/2509.02722` 

7. Christen, S., Hampali, S., Sener, F., Remelli, E., Hodan, T., Sauser, E., Ma, S., Tekin, B.: Diffh2o: Diffusion-based synthesis of hand-object interactions from textual descriptions. In: SIGGRAPH Asia 2024 Conference Papers. pp. 1–11 (2024) 

8. Dai, W., Lan, K., Zhou, J., Zhao, B., Su, X., Tong, J., Guan, W., Yang, S.: Conla: Contrastive latent action learning from human videos for robotic manipulation. arXiv preprint arXiv:2602.00557 (2026) 

9. Diller, C., Dai, A.: Cg-hoi: Contact-guided 3d human-object interaction generation. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 19888–19901 (2024) 

10. Fan, Y., Yang, Q., Wang, K., Zhou, H., Li, Y., Feng, H., Ding, E., Wu, Y., Wang, J.: Re-hold: Video hand object interaction reenactment via adaptive layout-instructed diffusion model. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 17550–17560 (2025) 

11. Gavryushin, A., Wang, X., Malate, R.J., Yang, C., Liconti, D., Zurbrügg, R., Katzschmann, R.K., Pollefeys, M.: Maple: Encoding dexterous robotic manipulation priors learned from egocentric videos. arXiv preprint arXiv:2504.06084 (2025) 

12. Ghosh, A., Dabral, R., Golyanik, V., Theobalt, C., Slusallek, P.: Imos: Intent-driven full-body motion synthesis for human-object interactions. In: Computer Graphics Forum. vol. 42, pp. 1–12. Wiley Online Library (2023) 

13. Grauman, K., Westbury, A., Byrne, E., Chavis, Z., Furnari, A., Girdhar, R., Hamburger, J., Jiang, H., Liu, M., Liu, X., et al.: Ego4d: Around the world in 3,000 hours of egocentric video. In: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. pp. 18995–19012 (2022) 

14. Hassan, M., Stapf, S., Rahimi, A., Rezende, P., Haghighi, Y., Brüggemann, D., Katircioglu, I., Zhang, L., Chen, X., Saha, S., et al.: Gem: A generalizable egovision multimodal world model for fine-grained ego-motion, object dynamics, and scene composition control. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 22404–22415 (2025) 

15. Ho, J., Salimans, T., Gritsenko, A., Chan, W., Norouzi, M., Fleet, D.J.: Video diffusion models. Advances in neural information processing systems **35** , 8633– 8646 (2022) 

16 D. Li, L. Liu et al. 

16. Huang, J., Hao, S., Hu, B., Wang, G.: Understanding dynamic scenes in ego centric 4d point clouds. arXiv preprint arXiv:2508.07251 (2025) 

17. Huang, M., Chu, F., Tekin, B., Liang, K.J., Ma, H., Wang, W., Chen, X., Gleize, P., Xue, H., Lyu, S., Kitani, K., Feiszli, M., Tang, H.: Hoigpt: Learning long-sequence hand-object interaction with language models. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). pp. 7136–7146 (June 2025) 

18. Huang, Z., Zhou, Z., Cao, J., Ma, Y., Chen, Y., Rao, Z., Xu, Z., Wang, H., Lin, Q., Zhou, Y., et al.: Hunyuanvideo-homa: Generic human-object interaction in multimodal driven human animation. arXiv preprint arXiv:2506.08797 (2025) 

19. Jiang-Lin, J.Y., Huang, K.Y., Lo, L., Huang, Y.N., Lin, T., Wu, J.C., Shuai, H.H., Cheng, W.H.: Record: Reasoning and correcting diffusion for hoi generation. In: Proceedings of the 32nd ACM International Conference on Multimedia. pp. 9465– 9474 (2024) 

20. Keetha, N.V., Müller, N., Schönberger, J., Porzi, L., Zhang, Y., Fischer, T., Knapitsch, A., Zauss, D., Weber, E., Antunes, N., et al.: Mapanything: Universal feed-forward metric 3d reconstruction. In: ICCV 2025 Workshop on Wild 3D: 3D Modeling, Reconstruction, and Generation in the Wild 

21. Kirillov, A., Mintun, E., Ravi, N., Mao, H., Rolland, C., Gustafson, L., Xiao, T., Whitehead, S., Berg, A.C., Lo, W.Y., et al.: Segment anything. In: Proceedings of the IEEE/CVF international conference on computer vision. pp. 4015–4026 (2023) 

22. Lee, J., Saito, S., Nam, G., Sung, M., Kim, T.K.: Interhandgen: Two-hand interaction generation via cascaded reverse diffusion. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 527–537 (2024) 

23. Lepert, M., Fang, J., Bohg, J.: Masquerade: Learning from in-the-wild human videos using data-editing. arXiv preprint arXiv:2508.09976 (2025) 

24. Li, J., Clegg, A., Mottaghi, R., Wu, J., Puig, X., Liu, C.K.: Controllable humanobject interaction synthesis. In: European Conference on Computer Vision. pp. 54–72. Springer (2024) 

25. Li, M., Christen, S., Wan, C., Cai, Y., Liao, R., Sigal, L., Ma, S.: Latenthoi: On the generalizable hand object motion generation with latent hand diffusion. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 17416–17425 (2025) 

26. Lin, X., Lian, S., Yu, B., Yang, R., Wu, C., Miao, Y., Jin, Y., Shi, Y., Huang, C., Cheng, B., et al.: Physbrain: Human egocentric data as a bridge from vision language models to physical intelligence. arXiv preprint arXiv:2512.16793 (2025) 

27. Liu, B., Gong, X., Zhao, Z., Song, Z., Lu, Y., Wu, S., Zhang, J., Banerjee, S., Zhang, H.: Byteloom: Weaving geometry-consistent human-object interactions through progressive curriculum learning (2025), `https://arxiv.org/abs/2512.22854` 

28. Liu, X., Yi, L.: Geneoh diffusion: Towards generalizable hand-object interaction denoising via denoising diffusion. arXiv preprint arXiv:2402.14810 (2024) 

29. Luo, H., Wang, Y., Zhang, W., Zheng, S., Xi, Z., Xu, C., Xu, H., Yuan, H., Zhang, C., Wang, Y., et al.: Being-h0. 5: Scaling human-centric robot learning for crossembodiment generalization. arXiv preprint arXiv:2601.12993 (2026) 

30. Pang, Y., Shao, R., Zhang, J., Tu, H., Liu, Y., Zhou, B., Zhang, H., Liu, Y.: Manivideo: Generating hand-object manipulation video with dexterous and generalizable grasping. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). pp. 12209–12219 (June 2025) 

31. Pavlakos, G., Shan, D., Radosavovic, I., Kanazawa, A., Fouhey, D., Malik, J.: Reconstructing hands in 3d with transformers. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 9826–9836 (2024) 

EgoHOI 17 

32. Radford, A., Kim, J.W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., Krueger, G., Sutskever, I.: Learning transferable visual models from natural language supervision. In: Proceedings of the 38th International Conference on Machine Learning (ICML). pp. 8748–8763. PMLR (2021) 

33. Routray, S., Pan, H., Jain, U., Bahl, S., Pathak, D.: Vipra: Video prediction for robot actions (2025), `https://arxiv.org/abs/2511.07732` 

34. Shen, Z., Wu, C., Zhou, J., Zhao, C., Wang, K., Zhou, H., Li, Y., Feng, H., He, W., Wang, J.: idit-hoi: Inpainting-based hand object interaction reenactment via video diffusion transformer. arXiv preprint arXiv:2506.12847 (2025) 

35. Tu, Y., Luo, H., Chen, X., Bai, X., Wang, F., Zhao, H.: Playerone: Egocentric world simulator. arXiv preprint arXiv:2506.09995 (2025) 

36. Wang, A., Ai, B., Wen, B., Mao, C., Xie, C.W., Chen, D., Yu, F., Zhao, H., Yang, J., Zeng, J., et al.: Wan: Open and advanced large-scale video generative models. CoRR (2025) 

37. Wang, J., Chen, M., Karaev, N., Vedaldi, A., Rupprecht, C., Novotny, D.: Vggt: Visual geometry grounded transformer. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (2025) 

38. Wang, S., Leroy, V., Cabon, Y., Chidlovskii, B., Revaud, J.: Dust3r: Geometric 3d vision made easy. In: CVPR (2024) 

39. Wang, Z., Bovik, A.C., Sheikh, H.R., Simoncelli, E.P.: Image quality assessment: From error visibility to structural similarity. IEEE Transactions on Image Processing **13** (4), 600–612 (2004) 

40. Xie, L., Sun, L.C., Neall, A., Wu, T., Cai, S., Wetzstein, G.: Generated reality: Human-centric world simulation using interactive video generation with hand and camera control (2026), `https://arxiv.org/abs/2602.18422` 

41. Xu, J., Huang, Y., Pei, B., Hou, J., Li, Q., Chen, G., Zhang, Y., Feng, R., Xie, W.: Egoexo-gen: Ego-centric video prediction by watching exo-centric videos. In: The Thirteenth International Conference on Learning Representations (2025) 

42. Xu, Z., Huang, Z., Cao, J., Zhang, Y., Cun, X., Shuai, Q., Wang, Y., Bao, L., Li, J., Tang, F.: Anchorcrafter: Animate cyberanchors saling your products via humanobject interacting video generation. arXiv preprint arXiv:2411.17383 (2024) 

43. Xue, M., Liu, Y., Guo, L., Huang, S., Ding, C.: Guiding human-object interactions with rich geometry and relations. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 22714–22723 (2025) 

44. Yang, R., Yu, Q., Wu, Y., Yan, R., Li, B., Cheng, A.C., Zou, X., Fang, Y., Cheng, X., Qiu, R.Z., et al.: Egovla: Learning vision-language-action models from egocentric human videos. arXiv preprint arXiv:2507.12440 (2025) 

45. Yoshida, T., Kurita, S., Nishimura, T., Mori, S.: Developing vision-language-action model from egocentric videos. arXiv preprint arXiv:2509.21986 (2025) 

46. Yuan, L., Wang, J., Sun, H., Zhang, Y., Lin, Y.: Tarsier2: Advancing large visionlanguage models from detailed video description to comprehensive video understanding. arXiv preprint arXiv:2501.07888 (2025) 

47. Zhang, R., Isola, P., Efros, A.A., Shechtman, E., Wang, O.: The unreasonable effectiveness of deep features as a perceptual metric. In: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR). pp. 586–595 (2018) 

48. Zhang, W., Foo, L.G., Beeler, T., Dabral, R., Theobalt, C.: Vhoi: Controllable video generation of human-object interactions from sparse trajectories via motion densification. arXiv preprint arXiv:2512.09646 (2025) 

- 18 D. Li, L. Liu et al. 

49. Zhang, Z., Shi, Y., Yang, L., Ni, S., Ye, Q., Wang, J.: Openhoi: Open-world handobject interaction synthesis with multimodal large language model. arXiv preprint arXiv:2505.18947 (2025) 

50. Zheng, D., Huang, Z., Liu, H., Zou, K., He, Y., Zhang, F., Gu, L., Zhang, Y., He, J., Zheng, W.S., et al.: Vbench-2.0: Advancing video generation benchmark suite for intrinsic faithfulness. arXiv preprint arXiv:2503.21755 (2025) 

51. Zheng, R., Niu, D., Xie, Y., Wang, J., Xu, M., Jiang, Y., Castañeda, F., Hu, F., Tan, Y.L., Fu, L., et al.: Egoscale: Scaling dexterous manipulation with diverse egocentric human data. arXiv preprint arXiv:2602.16710 (2026) 

52. Zhou, B., Zhan, Y., Zhang, Z., Lu, Z.: Megohand: Multimodal egocentric handobject interaction motion generation. arXiv preprint arXiv:2505.16602 (2025) 

53. Zhou, S., Vilesov, A., He, X., Wan, Z., Zhang, S., Nagachandra, A., Chang, D., Chen, D., Wang, X.E., Kadambi, A.: Vlm4d: Towards spatiotemporal awareness in vision language models. In: Proceedings of the IEEE/CVF international conference on computer vision. pp. 8600–8612 (2025) 

# **Egocentric World Model for Photorealistic Hand-Object Interaction Synthesis (Supplementary Material)** 

- Dayou Li<sup>1*</sup> , Lulin Liu<sup>1</sup><sup>_,_2*</sup> , Bangya Liu<sup>3</sup> , Shijie Zhou<sup>4</sup> , Jiu Feng<sup>5</sup> , Ziqi Lu<sup>6</sup> , Minghui Zheng<sup>1</sup> , Chenyu You<sup>7</sup> , Zhiwen Fan<sup>1�</sup> 

> 1Texas A&M University 2University of Minnesota 

> 3University of Wisconsin–Madison 4University of California, Los Angeles 

> 5University of Texas at Austin 6Amazon 

> 7State University of New York at Stony Brook 

This supplement is organized as follows: 

- Section A reinforces the motivation of EgoHOI by clarifying how 3D annotations and reconstruction-derived hand, camera, and object signals are used in our framework. 

- Section B provides implementation details of the physics-informed embeddings used in EgoHOI; 

- Section C describes how the training and test datasets have been built; 

- Section D includes the details of the evaluation metrics, and some definitions of some customized metrics; 

- Section E contains additional visualization results of the experiments. 

- Section F discusses the scope of EgoHOI and remaining challenges in evaluating physical plausibility. 

## **A Motivation** 

Egocentric Human-Object Interaction (HOI) world models aim to simulate physically grounded interaction dynamics from a first-person perspective driven by user controls. Such predictive rollouts are increasingly important as scalable training and evaluation data for downstream embodied tasks. However, building a reliable egocentric HOI world model is profoundly challenging due to rapid head motions, severe occlusions, and high-DoF hand articulations that abruptly alter contact topologies and object states. Despite recent progress in HOI video generation, this setting remains largely absent in existing pipelines. Current methods are either predominantly studied in static, exocentric views, which do not directly support first-person rollouts with dynamic interactions, or they condition heavily on privileged future object information such as groundtruth trajectories and waypoints, which largely bypasses the core challenge of contact-driven dynamics reasoning. Once these future-state shortcuts are removed, simply scaling RGB data is insufficient for physical accuracy. Instead, 

> * Equal contribution. 

20 D. Li, L. Liu et al. 

the model should be augmented with physics-informed embeddings that inject explicit metric and kinematic structure. Motivated by recent advances in 3D foundation models, we present EgoHOI, an egocentric HOI world model that integrates physics-informed embeddings distilled from 3D estimates into the generative rollout process, providing complementary structure for learning hand kinematics, metric-scale ego motion, and object integrity, while enabling causal simulation of physically plausible hand-object interactions without privileged future object states. 

## **B Physics-Informed Embedding Details** 

For completeness, this section provides implementation details for the physicsinformed embeddings used in EgoHOI. Following the main paper, we construct three embedding streams from complementary sources of structure: hand kinematics, metric ego motion, and an object-entity anchor tied to the first frame. These embeddings are converted into token sequences aligned with the Wan-DiT latent space and are incorporated into the generative rollout process to regularize action-driven latent dynamics without relying on privileged future object states. Unless otherwise noted, all embedding streams share the token dimension of the Wan-DiT backbone and are aligned to its latent patch layout. 

### **B.1 Hand Kinematic Embeddings (HKE)** 

HKE captures dense hand motion structure from reconstructed 3D hand estimates, which is essential for contact-consistent HOI rollouts under high-DoF articulation. Rather than encoding hand dynamics as sparse coordinate signals, we use explicit per-frame hand renders obtained from reconstructed meshes as a dense 3D representation and convert them into hand kinematic features aligned with the Wan-DiT latent space. 

**Input** For each frame _t_ , we render a hand-kinematics map _Ht ∈_ R<sup>_S×S×_3</sup> from the reconstructed hand mesh, where _S_ = 480. Stacking an _L_ -step rollout yields _H ∈_ R<sup>_L×S×S×_3</sup> . In our implementation, _L_ = 81. For a batch of size _B_ , the temporal hand volume has shape _B × L × S × S ×_ 3. 

**Temporal 3D Convolutional Stack** The temporal hand volume is processed by a temporal 3D convolutional stack with SiLU activations, which gradually increases the channel dimension and maps the hand stream to the shared latent token dimension of the Wan-DiT backbone. The exact layer configuration used in our implementation is summarized in Tab. 1. 

**Reference-Hand Branch** To stabilize hand identity and reduce temporal drift, we add a reference-hand branch that encodes the first-frame hand render into a compact feature through a 2D convolutional pyramid. This branch produces a 

EgoHOI Supplementary Material 21 

**Table 1: Implementation details of the temporal 3D convolutional stack used in HKE.** For each Conv3d layer we list the kernel size, stride, input _→_ output channels, and padding. 

|Layer|Kernel|Stride|Channels|Padding|
|---|---|---|---|---|
|Conv3d|(3,3,3)|(1,1,1)|3_→_16|(1,1,1)|
|Conv3d|(3,3,3)|(1,1,1)|16_→_16|(1,1,1)|
|Conv3d|(3,3,3)|(1,1,1)|16_→_16|(1,1,1)|
|Conv3d|(3,3,3)|(1,2,2)|16_→_16|(1,1,1)|
|Conv3d|(3,3,3)|(2,2,2)|16_→_16|(1,1,1)|
|Conv3d|(3,3,3)|(2,2,2)|16_→_16|(1,1,1)|
|Conv3d|(1,2,2)|(1,2,2)|16_→_5120|(0,0,0)|


first-frame hand feature that is incorporated into the initial latent during latentspace integration. The exact layer configuration is summarized in Tab. 2. 

**Table 2: Implementation details of the reference-hand branch used in HKE.** This branch processes the first-frame hand render; for each Conv2d layer we list the kernel size, stride, input _→_ output channels, and padding. 

|Layer|Kernel|Stride|Channels|Padding|
|---|---|---|---|---|
|Conv2d|3|1|3_→_16|1|
|Conv2d|3|1|16_→_16|1|
|Conv2d|3|1|16_→_16|1|
|Conv2d|3|2|16_→_16|1|
|Conv2d|3|2|16_→_16|1|
|Conv2d|3|2|16_→_20|1|


### **B.2 Ego-Motion Embeddings (EME)** 

EME encodes metric head trajectory estimates into embeddings aligned with the latent space, enabling geometry-consistent viewpoint evolution over time. Following the main paper, we represent ego motion as an image-aligned Plücker ray field and map the resulting trajectory representation into ego-motion tokens compatible with the Wan-DiT backbone. 

**Input and Plücker Ray Field** For each frame, the calibrated intrinsics _Kt_ and extrinsics _Et_ = [ _Rt | tt_ ], measured relative to the first frame, are converted into an image-aligned Plücker ray field on a regular grid. For each pixel ( _u, v_ ), we 

22 D. Li, L. Liu et al. 

form a 6D ray representation _pu,v_ = ( _o × du,v, du,v_ ), where _o_ is the head-frame optical center and: 


Stacking the per-frame Plücker tensors over time yields a trajectory volume of shape _P ∈_ R<sup>_B×_6</sup><sup>_×L×S×S_</sup> , where _L_ = 81 and _S_ = 480 in our implementation. 

**Temporal Causal Downsampling** We first process the trajectory volume with a temporal causal downsampler composed of three causal 3D convolutional blocks. Each block uses kernel size 3 _×_ 3 _×_ 3, GroupNorm, and SiLU activation. The first two blocks use stride (2 _,_ 2 _,_ 2), and the third uses stride (1 _,_ 2 _,_ 2). This stage reduces the temporal and spatial resolutions while preserving metric structure under head motion, and produces a feature map _F_ 0 _∈_ R<sup>_B×_64</sup><sup>_×_21</sup><sup>_×_60</sup><sup>_×_60</sup> . 

**Hybrid Spatiotemporal Processing** After temporal downsampling, the feature map is processed by a stack of hybrid spatiotemporal stages that combine 2D residual convolutions with temporal self-attention. In our implementation, the stage channels are [64 _,_ 128 _,_ 256]. Each stage reshapes the tensor from [ _B, C,_ 21 _, H, W_ ] to [ _B ·_ 21 _, C, H, W_ ], applies two 3 _×_ 3 Conv2d layers with stride 1, and uses an additional stride-2 Conv2d in stages that reduce the spatial resolution. The features are then reshaped back to [ _B, Ci,_ 21 _, Hi, Wi_ ] and passed through a temporal self-attention block along the 21-frame dimension. This design preserves spatially resolved constraints on viewpoint evolution instead of collapsing ego motion into a low-dimensional pose vector. 

**Projection Head and Patchification** The final feature volume is normalized and projected before tokenization. The output head consists of: (i) a GroupNorm layer, (ii) a 1 _×_ 1 _×_ 1 convolution for channel mixing, and (iii) a 3D convolutional patchifier with kernel size (1 _,_ 2 _,_ 2) and the same stride. After patchification, the feature map has shape (B, 5120, 21, 30, 30). Flattening the (21 _,_ 30 _,_ 30) grid into the sequence dimension yields ego-motion tokens _T_ EME _∈_ R<sup>_B×N_EME</sup><sup>_×d_</sup> , where _N_ EME = 21 _×_ 30 _×_ 30 and _d_ = 5120. These tokens are later injected into the latent dynamics through the zero-initialized linear adapters described in the main paper. 

### **B.3 Object-Entity Embeddings (OEE)** 

OEE anchors the manipulated object to the first frame to provide a persistent object-centric reference throughout the rollout. Concretely, we use the firstframe object segmentation image, obtained from an off-the-shelf segmentation model, to isolate object-centric evidence and reduce background interference under viewpoint changes. The segmentation is encoded by the frozen video VAE encoder into a latent grid, and a 3D convolutional patchifier converts it into tokens aligned with the main latent stream. 

EgoHOI Supplementary Material 

23 

**Input and VAE Latent** From the first frame, we obtain an object segmentation image and resize it to 480 _×_ 480. The image is normalized to [ _−_ 1 _,_ 1], arranged as [ _B,_ 3 _, H, W_ ], and expanded to [ _B,_ 3 _,_ 1 _, H, W_ ] before being passed to the frozen Wan VAE encoder. Operating in the same latent parameterization as the backbone, OEE yields a latent grid of shape [B,16,21,60,60]. 

**Object Patchifier** The latent grid is fed directly into a 3D convolutional patchifier without further convolutional processing beforehand. The patchifier uses kernel size (1 _,_ 2 _,_ 2) and the same stride, preserving the temporal length of 21 while reducing the spatial grid from 60 _×_ 60 to 30 _×_ 30. The output channel dimension equals the Wan-DiT hidden dimension, yielding a feature map of [B,5120,21,30,30]. 

**Object-Entity Tokens and Positional Shift** Flattening the (21 _,_ 30 _,_ 30) grid into the sequence dimension yields object-entity tokens _T_ OEE _∈_ R<sup>_B×N_OEE</sup><sup>_×d_</sup> , where _d_ = 5120 matches the hidden dimension of the Wan-DiT token space. To spatially anchor these tokens as an independent reference stream, we assign shifted rotary position indices when constructing the RoPE frequency grid. During latent-space integration, the OEE tokens are appended to the active token sequence and participate as KV-only context in self-attention, while only the main tokens are decoded. This design provides a persistent entity reference that reduces object drift in long rollouts. 

## **C Data Preparation** 

### **C.1 HOT3D Benchmark** 

HOT3D-Clips is a curated subset of the HOT3D dataset, released in WebDataset format as synchronized frame streams instead of ready-made videos. Each clip contains 150 egocentric frames of hand–object interaction with metric 3D annotations, including calibrated camera intrinsics and extrinsics, a world-aligned camera trajectory, articulated 3D hand kinematics, and 6-DoF object pose linked to scanned meshes. Project Aria provides multiple synchronized camera streams per frame; EgoHOI uses the forward-facing RGB stream (stream id is 214-1, labeled camera-rgb) as visual input, together with the associated 3D priors. Frames from stream 214-1 are grouped into 150-frame clips at 16 FPS. Clips are then randomly partitioned at the clip level, with 90% used for training and 10% reserved for testing, so that no frame from a test clip appears in training. In total, we have 1,364 samples for training and 152 samples for testing. 

In addition, we convert the 3D hand annotations in HOT3D-Clips into imagespace renderings that serve as input to the kinematics stream. For each frame, the MANO-based hand meshes are projected with the calibrated intrinsics and extrinsics of stream 214-1 and rasterized onto a blank canvas, producing a grayscale rendering of the visible hands in the current viewpoint, aligned pixel-wise with the corresponding RGB frame (as shown in Fig. 1). These hand-only renderings 

24 D. Li, L. Liu et al. 


**Fig. 1: Visualization of hand kinematics.** For each frame, we use the egocentric RGB image (left) together with a rendered hand-kinematics map (right) that visualizes the articulated meshes of both hands in the camera coordinate frame. 

preserve the precise 3D articulation while stripping away appearance, which makes the kinematic prior independent of texture and lighting. 

Since the Wan-based backbone in EgoHOI can only take 81 frames in a single rollout, a full 150-frame clip cannot be processed in one pass. During training, 81-frame trajectories are therefore sampled on the fly by sliding a temporal window over each clip with a stride of 5 frames. For every window, the corresponding RGB frames from stream 214-1 and their 3D priors are collected. These overlapping windows share the same scene but have different starting times, which increases trajectory diversity. 

### **C.2 Text Prompt Generation** 

To train text-conditioned baselines, each HOT3D clip is paired with an automatic caption generated by Tarsier2-7B [46], a large video-language model designed for detailed, low-hallucination video description and comprehensive video understanding. Tarsier2 combines a vision encoder, a lightweight adaptor, and a language model, and is trained in multiple stages on large-scale video–text corpora, which yields accurate and temporally grounded captions. For each 150frame clip, we uniformly sample representative keyframes and feed them to Tarsier2 together with an instruction asking for a concise yet detailed description of the scene and hand–object interaction. The resulting caption is stored as the text prompt for that clip and reused for all sliding-window segments derived from it when training the text-conditioned baseline world models. 

## **D Evaluation Metrics** 

The evaluation protocol examines generated rollouts from four complementary perspectives: visual prediction, ego-trajectory consistency, object integrity, and kinematic fidelity. Visual prediction is assessed using standard image and video 

EgoHOI Supplementary Material 25 

quality metrics, together with VBench scores that reflect perceptual and temporal quality. Ego-trajectory consistency is quantified from estimated camera trajectories. Object integrity is evaluated using Object-CLIP, object position error (OPE), and object orientation error (OOE), which together measure object appearance preservation, location preservation, and in-plane orientation preservation under interaction. Kinematic fidelity is measured from hand reconstructions obtained from both ground-truth and generated videos. Overall, the evaluation protocol combines standard metrics for comparison with prior work and custom measures designed for egocentric hand-object interaction. 

### **D.1 Visual Prediction Metrics** 

Visual prediction is evaluated using standard image quality metrics, including peak signal-to-noise ratio (PSNR), structural similarity (SSIM), perceptual similarity (LPIPS), and Object-CLIP. These metrics capture complementary aspects of rollout quality, ranging from pixel-level fidelity and perceptual similarity to object appearance preservation between ground-truth frames and the corresponding generated frames. Since these measures are widely used in video generation and reconstruction, they also enable direct comparison with prior world models. 

### **D.2 Ego-Motion Consistency Metrics** 

To quantify ego-motion consistency, we evaluate camera trajectories using Absolute Trajectory Error (ATE), Relative Pose Error (RPE), and Relative Rotation Error (RRE). Concretely, we apply MapAnything [20] to both the ground-truth video and the generated rollout under the same configuration to obtain two sequences of estimated head poses. These pose sequences are then temporally synchronized and aligned in a common coordinate frame, after which ATE, RPE, and RRE are computed in the standard way. This protocol measures whether the generated rollout preserves ego-motion that is geometrically consistent with the reference trajectory rather than merely producing visually plausible frames. 

### **D.3 Object-CLIP Score** 

We evaluate object appearance preservation by computing CLIP similarity between masked ground-truth frames and the corresponding generated frames. For each evaluation clip, we load object-masked RGB frames, align the ground-truth and generated sequences in time, and resize the ground-truth frames to match the generated resolution for one-to-one frame pairing. All frames are encoded with a single CLIP image encoder implemented with the `open_clip` backend using ViT-B/32 pretrained on LAION-2B S/34B, with images resized and normalized to 224 _×_ 224. We extract L2-normalized embeddings and compute cosine similarity for each paired frame ( _It_<sup>gt</sup><sup>_, I_</sup> _t_<sup>gen</sup> ). The Object-CLIP score for one clip is the average similarity over all paired frames, and the reported value is the mean over the evaluation set. 

26 D. Li, L. Liu et al. 

### **D.4 Object Position and Orientation Metrics** 

To provide a more fine-grained evaluation of object integrity, we introduce two object-level metrics computed from object masks in the ground-truth and generated frames: Object Position Error (OPE) and Object Orientation Error (OOE). These metrics complement Object-CLIP by explicitly measuring geometric consistency in image space. 

**Object Position Error (OPE)** For each frame, we extract binary object masks from the ground-truth and generated images. Given a mask with foreground pixels _{_ ( _xi, yi_ ) _}_<sup>_A_</sup> _i_ =1<sup>,itscentroidis:</sup> 


Let ( _c_<sup>gt</sup> _x_<sup>_, c_gt</sup> _y_<sup>)and(</sup><sup>_c_</sup> _x_<sup>gen</sup><sup>_, c_gen</sup> _y_ ) denote the centroids of the ground-truth and generated masks. We define the frame-level position error as the centroid distance normalized by the image diagonal: 


If both masks are empty, we set _e_ pos _,t_ = 0; if only one mask is empty, we assign a penalty of 1 _._ 0. 

**Object Orientation Error (OOE)** For a non-empty mask, we estimate its in-plane orientation from the second-order central moments: 


which define the principal-axis angle: 


To discard nearly isotropic masks, we compute the anisotropy score: 


EgoHOI Supplementary Material 27 

**Table 3: Ablation on object integrity.** In addition to the object integrity analysis in the main paper, we report object position error (OPE) and 2D orientation error (OOE) to further quantify how well each method preserves object location and inplane orientation under interaction. _↓_ is better for both metrics. 

|**Method**|OPE _↓_|OOE _↓_|
|---|---|---|
|Wan|0.078|19.295|
|Cosmos 2B|0.112|23.823|
|Cosmos 14B|0.108|23.312|
|Uni3C|0.083|24.751|
|**Ours (EgoHOI)**|**0.015**|**9.412**|


where _λ_ 1 _, λ_ 2 are the covariance eigenvalues. Orientation is considered valid only when _A ≥_ 20 and _α ≥_ 0 _._ 15. For valid ground-truth and generated masks, the angular difference is computed modulo _π_ and folded into [0 _, π/_ 2]: 


The frame-level orientation error is: 


Frames with invalid orientation are excluded from OOE. For each clip, OPE is averaged over all frames, and OOE is averaged over frames with valid orientation. We report the dataset-level macro-average of both metrics, together with the valid-frame ratio used for OOE. 

### **D.5 Kinematic Fidelity Metrics** 

We evaluate kinematic fidelity by applying HaMeR [31] to both ground-truth and generated frames. The evaluation reports three metrics: the missing ratio (MR), which measures how often a valid hand reconstruction is absent when a ground-truth hand is present; the mean per-joint position error (MPJPE), which measures 3D joint accuracy; and a root mean squared error (RMSE) computed on hand segmentation images. MPJPE is a standard metric in 3D hand pose estimation, while MR and segmentation RMSE capture characteristic failure modes in egocentric HOI rollouts, including complete hand disappearance and gradual degradation of the visible arm extent in image space. 

### **D.6 Hand Visibility Missing Ratio (MR)** 

The missing ratio measures how often the model fails to provide a valid hand prediction when a ground-truth hand is present. Let _H_ denote the set of all ground-truth hand instances indexed by time and hand identity: 


28 D. Li, L. Liu et al. 

For each ground-truth instance ( _t, i_ ), define an indicator: 


where validity is determined by the presence of a confident reconstruction and a bounded MPJPE. The missing ratio is then defined: 


A lower MR indicates that hands are reconstructed more reliably and remain present throughout the rollout, which is crucial for long-horizon egocentric sequences where hands frequently enter and leave the field of view. 

### **D.7 RMSE on Hand Segmentation Images** 

To directly assess how well the generated video preserves the spatial extent of the visible arm, a root mean squared error is computed between hand segmentation images extracted from the ground-truth and generated frames. For each frame _t_ , the Segment Anything [21] model is applied to obtain an arm mask from both the ground-truth frame and the corresponding generated frame under the same prompt. This yields two segmentation images (as shown in Fig. 2, represented as binary or probabilistic masks _Mt_ ( _x_ ) and _M_<sup>ˆ</sup> _t_ ( _x_ ) for each pixel _x_ in the image _M_ ˆ _t_ ( _x_ domain) _∈_ [0 _,_ 1] _Ω_ ,denoteswhere _M_ the _t_ ( _x_ predicted) _∈{_ 0 _,_ 1 _}_ armdenotesprobability.the ground-truthWith _T_ framesarm maskand pixeland 


**Fig. 2: Hand Segmentation for RMSE Evaluation.** For each frame, we extract the ground-truth hand region (left) and the corresponding inferred hand region produced by EgoHOI (right). The RMSE is computed as the per-pixel root-mean-square error between these two hand masks, averaged over all frames. 

domain _Ω_ , the RMSE on hand segmentation images is defined as: 


EgoHOI Supplementary Material 29 

A lower RMSEseg indicates a closer match between the generated and groundtruth arm regions in pixel space, penalizing errors in arm shape, position, and scale. This metric focuses on the spatial footprint of the arm rather than joint coordinates, and it complements MPJPE and MR by capturing subtle drifts in arm appearance that may not be reflected in joint-level errors alone. Taken together, MR and the segmentation RMSE isolate two characteristic failure modes in egocentric HOI rollouts, namely complete disappearance of the hand and gradual degradation of arm extent in image space, while standard frame and camera metrics account for global appearance and viewpoint consistency. 

### **D.8 VBench Scores** 

VBench [50] provides metrics that decompose video generation quality into temporal consistency and per-frame visual quality. In the egocentric HOI setting on HOT3D, only a subset of VBench dimensions can be applied directly to our generated rollouts without requiring text prompts or class labels. Therefore, the evaluation reports six scores: Subject Consistency, Background Consistency, Motion Smoothness, Dynamic Degree, Aesthetic Quality, and Imaging Quality. Other VBench dimensions that require explicit category, attribute, or style specifications are not used in this benchmark. 

Subject Consistency and Background Consistency measure how stable the foreground entities and the surrounding scene remain over time. High Subject Consistency indicates that the hand and manipulated object preserve identity and appearance across the rollout, rather than gradually drifting to different shapes or textures. High Background Consistency indicates that walls, tables, and other scene elements maintain coherent geometry and semantics under ego-motion, rather than exhibiting flickering layouts or implausible structural changes. Motion Smoothness uses a frame-interpolation prior to assess whether motion between adjacent frames evolves gradually and remains temporally coherent, without abrupt changes. 

Dynamic Degree aggregates optical flow magnitude to characterize the overall level of motion in a video. This metric reflects how active the sequence is, rather than how physically correct the dynamics are. In HOT3D, ground-truth clips already exhibit moderate ego-camera motion and purposeful hand-object interaction, so Dynamic Degree should be interpreted together with the consistency metrics. Very low values correspond to nearly static views or frozen hands, which under-represent the intended trajectories. Extremely high values indicate unnecessarily strong or unstable motion that no longer matches the underlying egocentric path. An appropriate Dynamic Degree in this benchmark therefore reflects a balanced amount of movement, rather than being interpreted as “the higher the better.” 

Aesthetic Quality and Imaging Quality capture complementary aspects of frame-level appearance. Aesthetic Quality correlates with judgments of composition, color, and overall visual appeal, while Imaging Quality focuses on low-level fidelity, including blur, noise, and exposure. Reporting these scores together veri- 

30 D. Li, L. Liu et al. 

fies that improvements in subject and background consistency or motion stability do not come at the expense of perceived visual quality. 


**Fig. 3: Qualitative comparison with baselines (part I).** Rows from top to bottom show the ground truth (GT), Cosmos-2B, Cosmos-14B, Wan, Uni3C, and our EgoHOI model. Each column block shows consecutive frames from one egocentric test sequence in temporal order. All methods receive the same first frame as input. Compared with the baselines, our model better preserves hand and object geometry, maintains object identity, and produces more stable interaction dynamics over time. See the zooming boxes for comparison of the fine-grained details. 

## **E Qualitative Results** 

In this section, we provide additional qualitative results that complement the main paper. We first compare EgoHOI with baseline methods on representative HOT3D examples, highlighting improvements in hand geometry, contact realism, and local appearance around the interaction region. We then provide qualitative examples under different user inputs to illustrate how the generated rollout varies with changes in ego-motion input. 

### **E.1 Comparison with Baselines** 

As shown in Fig. 3 and Fig. 4, our method produces images that are visually more realistic and spatially more coherent: hand shapes follow plausible anatomy, con- 

EgoHOI Supplementary Material 31 


**Fig. 4: Qualitative comparison with baselines (part II).** Rows from top to bottom show the ground truth (GT), Cosmos-2B, Cosmos-14B, Wan, Uni3C, and our EgoHOI model. Each column block shows consecutive frames from one egocentric test sequence in temporal order. All methods receive the same first frame as input. Compared with the baselines, our model better preserves hand and object geometry, maintains object identity, and produces more stable interaction dynamics over time. See the zooming boxes for comparison of the fine-grained details. 

tact regions agree with the intended manipulation, and local appearance around the hands preserves sharper details and cleaner boundaries. Competing models frequently exhibit deformed or incomplete fingers, inaccurate hand-object overlap, and artifacts near the contact area, which reduces the perceived realism of the interaction. These qualitative comparisons indicate that incorporating our 3D priors yields more reliable hand geometry and higher-fidelity hand appearance in egocentric views. Additional visualization videos are available on the webpage attached to the supplementary materials. 

### **E.2 Qualitative Analysis under Different User Inputs** 

To further illustrate the action-driven world modeling behavior of EgoHOI, we provide qualitative examples generated from the same first frame under different user inputs. As shown in Fig. 5, changing the user input leads to distinct rollout outcomes, while the generated videos remain physically plausible and preserve coherent hand-object interaction dynamics over time. These examples suggest that EgoHOI does not merely reproduce visually plausible continuations 

32 D. Li, L. Liu et al. 


**Fig. 5: Qualitative analysis under different user inputs.** For each example, both rows start from the same first frame but use different user inputs. EgoHOI produces distinct rollout outcomes with different viewpoint evolution and interaction trajectories, while preserving coherent scene structure and plausible hand-object interaction. 

from a fixed initial observation; instead, it responds to different user controls by simulating different and plausible interactions. 

## **F Discussion** 

Egocentric HOI world models are critical for simulating physically grounded firstperson rollouts. In this work, EgoHOI breaks away from privileged future-state shortcuts by integrating physics-informed embeddings into the generative rollout process, enabling photorealistic, contact-consistent hand-object interactions from action signals alone. The empirical gains in visual prediction, ego-trajectory consistency, kinematic fidelity, and object integrity suggest that explicit metric and kinematic structure provides an effective inductive bias for egocentric HOI simulation. At the same time, fully evaluating physical plausibility remains an open problem. While our current benchmark captures multiple complementary aspects of rollout quality through reconstruction-derived and perceptual metrics, future work should develop more direct contact-aware and dynamics-aware evaluations for first-person hand-object interaction rollouts. 

