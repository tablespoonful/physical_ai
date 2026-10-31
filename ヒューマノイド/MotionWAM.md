---
title: "MotionWAM: Towards Foundation World Action Models for Real-Time Humanoid Loco-Manipulation"
date: "2026-06-08"
authors: "Jia Zheng; Teli Ma; Yudong Fan; Zifan Wang; Shuo Yang; Junwei Liang"
url: https://arxiv.org/abs/2606.09215
pdf: https://arxiv.org/pdf/2606.09215
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.09215)** / [論文ページ](https://arxiv.org/abs/2606.09215)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **MotionWAM: Towards Foundation World Action Models for Real-Time Humanoid Loco-Manipulation** 

**Jia Zheng**<sup>1</sup><sup>_,_2</sup><sup>_,†_</sup> **, Teli Ma**<sup>1</sup><sup>_,_2</sup><sup>_,†_</sup> **, Yudong Fan**<sup>1</sup> **, Zifan Wang**<sup>1</sup><sup>_,_2</sup> **, Shuo Yang**<sup>1</sup><sup>_,∗_</sup> **, Junwei Liang**<sup>2</sup><sup>_,_3</sup><sup>_,∗_</sup> 1 Mondo Robotics 2 HKUST (GZ) 3 HKUST _†_ Equal contribution. _∗_ Corresponding author, Co-advising. 


Figure 1: **MotionWAM: A unified WAM for real-time humanoid loco-manipulation.** On a Unitree G1, MotionWAM produces real-world trajectories spanning waist control, height regulation, squatting locomotion, body-hand coordination, and task-driven foot interaction. 

**Abstract:** World Action Models (WAMs) couple a video dynamics prior to the policy and have shown encouraging results on tabletop manipulation, but iterative denoising over high-dimensional video-action latents leaves them too slow for real-time humanoid loco-manipulation. The problem is compounded by the dominant hierarchical paradigm, in which a high-level manipulation policy controls only the upper body while a low-level controller tracks coarse base commands— placing upper and lower body in inconsistent action spaces and reducing the legs to balance-preserving locomotion. We present **MotionWAM** , a real-time WAM that drives autonomous humanoid loco-manipulation from a single egocentric camera by conditioning the policy on the intermediate denoising features of a video world model. MotionWAM replaces the upper–lower split with a _unified motion latent_ and predicts whole-body _motion tokens_ that jointly cover locomotion, torso 

motion, height regulation, foot interaction, and hand manipulation in a single action space. A three-stage learning framework progressively adapts the video world model to egocentric visual dynamics and to the target humanoid embodiment. On nine real-world Unitree G1 tasks, MotionWAM runs in real time, substantially outperforms Vision-Language-Action (VLA) baselines finetuned on the same demonstrations by over 30% in overall success rate, and executes task-driven foot interaction that decoupled upper-lower policies cannot achieve. Our results suggest that video-pretrained WAMs can be extended from performing tabletop manipulation to coordinated, human-like whole-body humanoid control. 

**Keywords:** Loco-Manipulation, World Action Model, Robotic Manipulation 

## **1 Introduction** 

Humanoid loco-manipulation requires robots to move through human-scale environments while coordinating balance, locomotion, reaching, and object interaction. Prior works have made progress along three largely separate axes: robust whole-body imitation [1, 2, 3, 4], commandfollowing whole-body controllers [5, 6, 7, 8, 9], and manipulation policies as high-level planners [10, 11, 12, 13]. Almost all autonomous humanoid loco-manipulation systems combine these axes by pairing a high-level manipulation policy with a low-level locomotion controller [12, 10, 13], giving fine-grained joint targets to the upper body but only coarse base commands (velocity, torso height, oriInconsis ~~t~~ en ~~t~~ ac ~~t~~ ion space Covers locomoUni ~~f~~ ied mo ~~t~~ ion ~~t~~ ion, ~~t~~ okens entation) to the lower body. This forces the two halves Upper ~~-~~ body ~~t~~ inorso, heigh ~~t~~ erac ~~t~~ ion, hand ~~t~~ , ~~fo~~ o ~~t~~ into inconsistent action spaces and restricts the legs to join ~~t~~ pos manipula ~~t~~ ion balance-preserving locomotion, ruling out task-driven foot interaction such as stepping on a pedal or kicking Lower ~~-~~ body an object, as shown in Fig. 2. commands 


World Action Models (WAMs) have recently emerged as No ~~t~~ ask ~~-~~ driven ~~f~~ oo ~~t~~ in ~~t~~ erac ~~t~~ ion Task ~~-~~ driven ~~f~~ oo ~~t~~ in ~~t~~ erac ~~t~~ ion a promising route to visuomotor control by inversing dynamics [14, 15, 16] or jointly modeling visual and robot Figure 2: **Decoupled vs. unified action** distributions [17, 18, 19, 20, 21, 22]. By learning to roll **spaces.** _Left:_ hierarchical pipelines split control into upper-body joint targets and out future visual states for action prediction, WAMs inlower-body base commands, restricting ject a strong dynamics prior into the policy, yielding temthe legs to balance preservation. _Right:_ porally coherent and physically grounded behavior that MotionWAM predicts _whole-body mo-_ purely image-text-pretrained policies struggle to acquire _tion tokens_ covering locomotion, torso, from demonstrations alone. However, iterative denoising height, foot interaction, and hand maover high-dimensional video-action latents is costly, and nipulation, enabling task-driven foot beexisting WAMs struggle to reach real-time rates even on haviors like pedal stepping and ball tabletop arms. This raises the question: _can WAM’s rich_ kicking. _dynamics priors be deployed in real time, in a unified latent space, for whole-body humanoid locomanipulation?_ 

To resolve these two questions, we present **MotionWAM** , an end-to-end World Action Model for autonomous humanoid loco-manipulation from a single egocentric camera. MotionWAM couples a video DiT with a motion DiT through intermediate denoising features and trains both modalities under a unified flow-matching objective inspired by DiT4DiT [21]. Instead of splitting the body into upper-limb joint targets and lower-limb base commands, MotionWAM represents behavior in a _unified motion latent_ and predicts _whole-body motion tokens_ to drive the humanoid as one integrated system. Each token compactly encodes coordinated whole-body motion across locomotion, torso movement, height change, foot placement, and hand manipulation. Crucially, the same representation gives the lower body a task-driven action vocabulary, unlocking foot interaction such as stepping on a pedal or kicking an object. 

To learn the visual dynamics priors that egocentric loco-manipulation actually requires, we train MotionWAM with a three-stage learning framework. _Stage 1: egocentric video pretraining._ We as- 

2 

semble roughly 2,136 hours of egocentric human video and humanoid-robot video, and pretrain the video branch alone on future-frame generation. Only the video parameters are updated, shifting the world model from its original distribution toward visual dynamics observed from a first-person viewpoint. _Stage 2: cross-embodiment action post-training._ To bridge the pretrained world model to our target embodiment, we train on a heterogeneous mixture of Unitree G1 humanoid data spanning different end-effectors and action-annotation formats, jointly updating the video and action networks under a single joint flow-matching objective. _Stage 3: whole-body fine-tuning._ We collect teleoperated whole-body demonstrations on the target tasks and fine-tune the model from Stages 1–2, switching its action output to unified whole-body motion tokens that drive the humanoid end-to-end. 

To rigorously evaluate MotionWAM, we establish a comprehensive suite of nine real-world humanoid loco-manipulation tasks that jointly stress waist control, height regulation, squatting locomotion, task-driven foot interaction, and body–hand coordination. Across this suite, MotionWAM runs in real time and substantially outperforms VLA baselines finetuned on the same demonstrations—executing task-driven foot interaction that decoupled upper-lower policies cannot reach, with the legs actively contributing to the task rather than passively preserving balance, and producing whole-body motion that is markedly more coherent and human-like. 

Our contributions are: 

- We propose **MotionWAM** , a real-time WAM for autonomous humanoid loco-manipulation that drives the policy with the intermediate denoising features of a video world model. To train it, we introduce a three-stage learning framework that progressively adapts the video world model to egocentric visual dynamics and to the target humanoid embodiment. 

- We replace the upper-lower-body decoupled policies common in hierarchical humanoid systems with unified motion latents, letting one policy predict locomotion, torso motion, height regulation, foot interaction, and hand manipulation in a single action space. Crucially, this unlocks task-driven foot control that prior decoupled policies cannot perform. 

- We present, to our knowledge, the **first** closed-loop end-to-end WAM-driven policy that performs whole-body humanoid loco-manipulation in real time, including task-driven foot behaviors such as ball kicking and pedal stepping that hierarchical upper–lower baselines cannot produce. 

## **2 Related Work** 

In recent years, robot manipulation has evolved from single arms performing tabletop tasks to humanoid robots performing whole-body tasks. Hierarchical structures have become widely used. 

**Imitation policies and VLAs for manipulation.** Imitation policies [23, 24, 25] and VisionLanguage-Action models [26, 27, 28, 29, 30, 31, 32] learn visuomotor manipulation from demonstrations, with VLAs additionally inheriting semantic priors from pretrained vision-language backbones. However, these models rely on a _static_ image–text substrate that lacks an intrinsic model of temporal evolution or contact physics, and are typically restricted to arm-and-gripper action spaces on a single embodiment. In contrast, MotionWAM replaces the VLM backbone with a video world model whose intermediate denoising features condition the policy, and extends the action space to whole-body humanoid control. 

**World Action Models.** World Action Models (WAMs) [14, 15, 16, 17, 18, 19, 20, 21, 22] inject a dynamics prior into the policy by leveraging video generators, often built on internet-scale world models [33, 34, 35, 36, 37]. Despite their promise, deployments to date remain confined to shorthorizon, fixed-base, arm-only tabletop settings, primarily because high-dimensional video-action denoising is too slow for closed-loop control. In contrast, MotionWAM targets dynamically balancing humanoids and is the first WAM, to our knowledge, to operate in real time on whole-body loco-manipulation. 

**Humanoid loco-manipulation.** Existing humanoid loco-manipulation efforts span whole-body imitation of human motion [1, 2, 3, 4], command-conditioned whole-body controllers [5, 6, 7, 8, 9], 

3 

and autonomous policies built on top of such controllers [10, 11, 30, 13]. The latter, while closest to our setting, typically delegate the legs to a low-level controller driven only by base velocity, height, and orientation, leaving upper- and lower-body action spaces decoupled. In contrast, MotionWAM emits a single whole-body action through unified motion tokens, which lets the legs participate in the task itself rather than only stabilizing the base. 

## **3 Method** 

MotionWAM is a dual-DiT WAM that turns egocentric video dynamics into whole-body humanoid action. We first formalize the _predict-video-dynamics–then-invert_ setting and the unified wholebody motion latent it predicts (Sec. 3.1), then describe the dual-DiT architecture that couples a Video DiT and a Motion DiT (Sec. 3.2), and finally detail the three-stage training recipe that progressively specializes the model from egocentric video pretraining, through cross-embodiment action posttraining, to whole-body teleoperation fine-tuning on Unitree G1 (Sec. 3.3). 

### **3.1 Problem Formulation** 

Unlike VLA policies that learn a direct mapping _πθ_ ( **a** _t |_ **o** _t, l_ ) on humanoid embodiments, MotionWAM follows a _predict-video-dynamics–then-invert_ paradigm and predicts a unified _whole-body motion latent_ that drives the entire body in a single action space: 


Here _l_ is the language goal, **o** _t_ is the egocentric observation, _pt_ is the proprioceptive state, **o**<sup>_τ_</sup> _t_ +1<sup>_v_is</sup> the intermediate future-frame state at flow step _τv_ , and _H_ extracts hidden states from this generative process. The whole-body motion latent **m** _t_ jointly covers locomotion, torso motion, height regulation, foot interaction, and hand manipulation, and is converted to joint commands by a low-level motion decoder. Training jointly models the video-action distribution _pva_ ( **o** _t_ +1 _,_ **m** _t |_ **o** _t, pt, l_ ). 

**Whole-body motion latent.** We instantiate **m** _t_ = ( **m**<sup>cont</sup> _t ,_ **k** _t_ ) on top of SONIC [4], a universal whole-body controller that fuses different motion targets through a single shared latent. The shared latent is bottlenecked by Finite Scalar Quantization [38] with 2 tokens of 32 levels each, so the SONIC token **k** _t ∈{−_ 1 _, −_<sup><u>15</u></sup> 16<sup>_, . . . ,_1</sup><sup>_}_64is a 64-dimensional discretized vector that summarises lo-</sup> comotion, torso, height, and foot-interaction intent. The continuous part **m**<sup>cont</sup> _t_ collects the dexterous channels SONIC does not cover—left/right gripper commands or dexterous hand commands—and drives the hands directly. 

### **3.2 Model Architecture** 

MotionWAM follows the dual-DiT video-motion framework, instantiated for whole-body humanoid loco-manipulation. A Video DiT initialized from Cosmos-Predict2.5-2B [39]—a causal spatiotemporal VAE plus a flow-matching diffusion transformer [40] conditioned on Cosmos-Reason1 language embeddings [41]—compresses egocentric conditioning frames **o** _t_ and future frames **o** _t_ +1 into latents **z**<sup>0</sup> _t_<sup>_,_</sup><sup>**z**0</sup> _t_ +1<sup>.Rather than consuming a fully denoised future [40], we install a forward hook</sup> on a single transformer block to intercept its activations at a fixed flow timestep _τf_ : 


where _H_ [ _·_ ] reads hidden states of the velocity network _vθ_<sup>video</sup> in a single forward pass. We fix _τf_ at the pure-noise end of the schedule ( _τf ≈_ 1), so the Video DiT runs in its _one-shot imagination_ regime: given clean conditioning **z**<sup>0</sup> _t_<sup>andGaussiannoiseforthefuture,onepassyieldsactivationsthaten-</sup> code where the scene is _about to go_ , never denoising those frames. This single pass is what keeps MotionWAM real time on a closed-loop humanoid. The Motion DiT then consumes **h**<sup>_τ_</sup> _t_<sup>_f_</sup> via interleaved self/cross-attention together with the embedded proprioceptive state _pt_ and noisy whole-body motion-latent tokens, and outputs the velocity field whose integration yields the motion latent **m** _t_ . Per-embodiment input/output projectors wrap a shared Motion DiT trunk during multi-embodiment pretraining, and the same trunk is reused at deployment with a single Unitree G1 projector. 

4 


Figure 3: **Overview of MotionWAM.** A dual-DiT video–motion model trained in three stages. _Stage 1:_ the Video DiT is pre-trained alone on egocentric human and humanoid videos. _Stage 2:_ the Motion DiT is attached and co-trained across heterogeneous Unitree G1 datasets via specific embodiment tags, conditioned on Video DiT hidden states to predict discrete motion-token index and continuous end-effector values. _Stage 3:_ the full model is finetuned on teleoperated whole-body demonstrations retargeted from SMPL-24 to Unitree G1. 

### **3.3 Training Recipe** 

We train MotionWAM with a three-stage learning framework that progressively adapts the video world model to egocentric visual dynamics and to the target humanoid embodiment, following the intuition that the video and motion branches should specialise in turn rather than be optimised jointly from scratch. The VAE and text encoder remain frozen throughout. Stage 1 updates only the Video DiT trunk; Stage 2 jointly updates the Video DiT and the newly attached Motion DiT; Stage 3 fine-tunes the full network end-to-end on the target embodiment. 

**Flow-matching objectives.** Both the Video DiT and the Motion DiT are trained with flow matching. Reusing the notation of Sec. 3.2, let **z**<sup>0</sup> _t_<sup>and</sup><sup>**z**0</sup> _t_ +1<sup>denotethecleanconditioning-andfuture-frame</sup> VAE latents and **_ϵ_** _v ∼N_ (0 _, I_ ) a noise sample; the noise-perturbed future latent at flow time _τv ∈_ [0 _,_ 1] is **z**<sup>_τ_</sup> _t_ +1<sup>_v_=(1</sup><sup>_−τv_)</sup><sup>**z**</sup> _t_<sup>0</sup> +1<sup>+</sup><sup>_τv_</sup><sup>**_ϵ_**</sup><sup>_v_, and the Video DiT learns the velocity field</sup><sup>_v_</sup> _θ_<sup>video</sup> � **z**<sup>_τ_</sup> _t_ +1<sup>_v, τv|_</sup> **z**<sup>0</sup> _t_<sup>_, l_</sup> � _≈_ **_ϵ_** _v −_ **z**<sup>0</sup> _t_ +1<sup>:</sup> 


For a clean motion-latent chunk **m**<sup>0</sup> _t_<sup>and noise</sup><sup>**_ϵ_**</sup><sup>_m∼N_(0</sup><sup>_, I_), the Motion DiT predicts the velocity</sup> field _vϕ_<sup>motion</sup> � **m**<sup>_τ_</sup> _t_<sup>_a, τa|_</sup><sup>**h**</sup><sup>_τ_</sup> _t_<sup>_f, pt, e_</sup> � conditioned on the Video DiT hidden state **h**<sup>_τ_</sup> _t_<sup>_f_</sup> from Eq. (2), the proprioceptive state _pt_ , and an embodiment index _e_ : 


**Stage 1 — Pretraining on egocentric human and humanoid video.** The Video DiT is pretrained alone with _L_ video on _∼_ 2,136 hours of egocentric human videos and humanoid-robot videos (the full source-level mixture is given in Appendix E), shifting the world model from its original distribution toward the visual dynamics observed from a first-person viewpoint. Our key insight is that egocentric visual dynamics, not action diversity, is the bottleneck at this stage: by training the Video DiT alone on cheap, action-free video, the trunk absorbs scale without being throttled by the much smaller pool of action-labelled demonstrations, and produces a robot-centric dynamics prior whose hidden states encode plausible egocentric futures. 

**Stage 2 — Cross-embodiment action post-training.** We attach the Motion DiT and co-train across heterogeneous Unitree G1 humanoid data spanning different end-effectors and action-annotation formats, routed through per-embodiment input/output projectors around the shared Motion DiT trunk. To prevent the dynamics prior from being overwritten when the action signal arrives, we 

5 

retain the video objective as a representation regulariser, giving the joint loss 


**Stage 3 — Finetuning on whole-body teleoperation data.** With the dynamics prior from Stage 1 and the cross-embodiment action grounding from Stage 2 already in place, MotionWAM rapidly adapts to humanoid loco-manipulation from a small amount of teleoperated whole-body demonstrations collected on Unitree G1 (200 episodes per task across the nine real-world tasks; see Appendix E and the teleoperation pipeline in Appendix B). We carry over the joint loss in Eqn. (5) and the shared-trunk + Unitree G1 projector configuration, so a single network inherits video dynamics, multi-embodiment grounding, and task-specific behavior without any architectural change. The whole-body motion latent decomposes as **m** _t_ = ( **m**<sup>cont</sup> _t , k_<sup>˜</sup> _t_ ): a vector of continuous channels **m**<sup>cont</sup> _t_ (value of end-effectors) and a single scalar slot _k_<sup>˜</sup> _t ∈_ R that holds the SONIC [4] motion-token index _kt ∈{_ 0 _, . . . , K −_ 1 _}_ summarising whole-body loco-manipulation trajectories. Rather than introducing a separate categorical head, we let _k_<sup>˜</sup> _t_ live inside **m** _t_ as a continuous scalar, regress the entire latent under the same flow-matching objective in Eqn. (4), and recover the discrete index at inference by nearest-neighbor rounding before SONIC decodes the assembled latent into joint commands **a** _t_ : 


## **4 Experiments** 

We design our real-robot evaluation around three questions: (Q1) does coupling a video world model into the policy yield a tangible advantage over strong VLA baselines on whole-body humanoid locomanipulation? (Q2) is each of the three training stages necessary, and what does each contribute? (Q3) can WAM runs fast enough for closed-loop humanoid control compared to VLA baselines? 

### **4.1 Experimental Setup** 

**Hardware platform.** We conduct all real-world experiments on a Unitree G1 humanoid with dual ALOHA2 grippers, observing the scene through a head-mounted Intel RealSense D435i RGB camera. **<mark>PnP Bo</mark>** **~~<mark>tt</mark>~~** **<mark>le</mark>** <mark>Kick Soccer Re</mark> ~~<mark>t</mark>~~ <mark>rieve I</mark> ~~<mark>t</mark>~~ <mark>em</mark> Whole-body teleoperation demonstrations are collected via a PICO VR three-point tracking setup retargeted to the robot through SMPL, and at deployment the policy outputs are <mark>Load Car</mark> ~~<mark>t</mark>~~ <mark>Toss Garbage Li</mark> ~~<mark>ft</mark>~~ <mark>Baske</mark> ~~<mark>t</mark>~~ tracked by the SONIC [4] wholebody controller. MotionWAM and all baselines run as WebSocket policy servers on a single NVIDIA RTX 4090 workstation and are <mark>S</mark> ~~<mark>t</mark>~~ <mark>ock Shelves Wipe Board Do Laundry</mark> queried in closed loop by the onboard controller. Full hardware specifications and the VR-based teleoperation pipeline used to collect Stage 3 demonstrations are described in Appendix B. Figure 4: **Real-world task suite.** We design nine whole- 

Figure 4: **Real-world task suite.** We design nine wholebody loco-manipulation tasks on the Unitree G1, each requiring active leg and torso involvement beyond balance preservation. Per-task language prompts are provided in Appendix A.1. A.1.. 

**Task design.** As shown in Fig. 4, we quiring active leg and torso involvement beyond balance evaluate on a suite of nine real-world preservation. Per-task language prompts are provided in Apwhole-body loco-manipulation tasks pendix A.1. A.1.. that jointly stress the five core capabilities highlighted in Fig. 1: _waist control_ , _height regulation_ , _squatting locomotion_ , _task-driven foot interaction_ , and _body–hand coordination_ . The suite is designed so that no single task can be 

6 


Figure 5: **Comparison with the state-of-the-art VLAs on nine real-world whole-body locomanipulation tasks.** We report per-task success rate (%) over 20 trials per task on the Unitree G1. All methods are finetuned on the same Stage 3 demonstrations. 

solved by upper-body manipulation alone; each one forces the legs and torso to actively contribute, exposing behaviors that decoupled upper–lower policies cannot express. 

Each method is tested for 20 trials per task, and we report success as the percentage of successful trials in Fig. 5. Per-task language prompts are listed in Appendix A.1, and representative MotionWAM rollouts for every task are shown in Fig. 7. 

**Baselines.** We compare MotionWAM against five baselines: **Diffusion Policy** [23] and **ACT** [24] as representative non-VLA visuomotor policies; _π_ **0** _._ **5** [31] and **GR00T-N1.7** [30] as state-of-theart generalist VLAs; and **Qwen3DiT** , a custom parameter-matched ablation that pairs the Qwen3VL [42] 2B backbone with our Motion DiT to isolate the contribution of the video world model prior over a static VLM prior at matched capacity. All baselines consume the same egocentric RGB observations, language goals, and proprioceptive states as MotionWAM, and emit unified motion latents in the same action space. Per-baseline descriptions and training recipes are reported in Appendix D, and MotionWAM training configurations in Appendix C. 

### **4.2 Comparison with the State-of-the-Art** 

All policies are finetuned on the same Stage 3 dataset and emit actions through the same SONIC interface, so the sole source of variation is whether the policy is conditioned on intermediate denoising features of a video world model (MotionWAM) or on VLM-style image–text features (GR00TN1.7, _π_ 0 _._ 5, Qwen3DiT). Fig. 5 reports per-task and average success rates. MotionWAM wins on every task and lifts the overall success rate from 43 _._ 9% (the strongest baseline, GR00T-N1.7) to 76 _._ 1%, an over 32% absolute gain. The gap is largest on tasks demanding whole-body coordination beyond the upper limbs— `Kick Soccer` (+40%), `Load Cart` (+40%), `Retrieve Item` (+40%), `Wipe Board` (+45%), and `Do Laundry` (+30%)—where the unified motion latent gives MotionWAM access to task-driven foot and torso behaviors that a decoupled upper–lower interface cannot express. Meanwhile, the VLM-only baseline (Qwen3DiT) collapses to near-zero success on every locomotion-heavy task and even _π_ 0 _._ 5 stays under 20% overall, indicating that strong semantic priors alone do not transfer to the closed-loop physics humanoid loco-manipulation demands. Coupling the policy to a video world model is what closes that gap. 

### **4.3 Ablation on the Three-Stage Training Framework** 

We disentangle the contribution of _egocentric video pretraining_ (Stage 1) from _cross-embodiment action pretraining_ (Stage 2), and show that both are necessary for the final real-robot performance. We disable one stage at a time while keeping Stage 3 fixed, and re-run the full real-robot evaluation on a representative subset of the suite: `Lift Basket` , `Retrieve Item` , `Load Cart` , `Toss Garbage` , `Kick Soccer` . 

As shown in Table 1, removing Stage 1 and Stage 2 leads to 11% and 28% absolute performance drop respectively. _Without Stage 1_ , the Video DiT enters Stage 2 with a generic, non-egocentric dynamics 

7 

Table 1: **Ablation of the three-stage training framework.** Real-robot success rate (%) over 20 trials per task on five representative whole-body loco-manipulation tasks. Stage 3 (real-robot finetuning) is enabled in all variants. 

|Variant|Stage 1|Stage 2|`Lift`<br>`Basket`|`Retrieve`<br>`Item`|`Load`<br>`Cart`|`Toss`<br>`Garbage`|`Kick`<br>`Soccer`|**Avg.**|
|---|---|---|---|---|---|---|---|---|
|w/o Stage 2|✓|–|65|45|30|30|40|42.0|
|<br>w/o Stage 1|–|✓|70|75|60|35|55|59.0|
|<br>**Full**|✓|✓|**80**|**90**|**75**|**45**|**60**|**70.0**|


prior; the resulting hidden states still carry useful semantics, but the predicted motion latents become visibly less accurate. _Without Stage 2_ , the Motion DiT is attached directly to the Stage 1 trunk and trained only on the small target-task dataset; with no cross-embodiment grounding to anchor the action signal, performance collapses on every task. The two stages thus play complementary roles—Stage 1 supplies an egocentric _visual-dynamics_ prior, Stage 2 grounds that prior into the action space across embodiments. This validates the central design choice of training the video and motion branches in turn rather than jointly from scratch. 

### **4.4 Real-Time Inference Frequency** 

We measure closed-loop deployment frequency on an NVIDIA A100 to verify that conditioning on a _single forward pass_ of the Video DiT (Eqn. (2)) keeps MotionWAM real-time. The reported frequency is the _chunk-wise_ rate Model Trainable Params Frequency at which the policy emits a whole action chunk. 

|Model|Trainable Params|Frequency|
|---|---|---|
|GR00T-N1.7 [30]<br>|1.6B|6.5 Hz|
|Qwen3DiT|2.3B|9.0 Hz|
|Cosmos Policy [20]|2.0B|0.7 Hz|
|**MotionWAM (Ours)**|**2.5B**|**4.9 Hz**|


As shown in Table 2, MotionWAM remains competitive with VLA baselines at matched scale. Crucially, against Cosmos Policy [20]— another world-model-based policy with a comparable parameter count—MotionWAM is _seven times faster_ (4 _._ 9 Hz vs. 0 _._ 7 Hz), because 

Table 2: **Deployment efficiency with a single NVIDIA A100.** 

Cosmos Policy must iteratively denoise the future video before producing actions whereas MotionWAM reads off intermediate denoising features in a single pass. This confirms that MotionWAM delivers the accuracy gains in Fig. 5 while still meeting the real-time control rates required for closed-loop humanoid balance. 

## **5 Conclusion** 

We present **MotionWAM** , a real-time World Action Model for autonomous humanoid locomanipulation from a single egocentric camera. By coupling a Video DiT and a Motion DiT through intermediate denoising features and predicting whole-body motion tokens in a unified action space, MotionWAM, trained with a three-stage egocentric-to-embodiment recipe, outperforms the strongest VLA baseline by over 30% on nine real-world tasks and points to a viable path from large-scale video pretraining to human-like whole-body humanoid policies. 

## **6 Limitations** 

MotionWAM has the following limitations. **First** , the Stage 3 fine-tune has been validated only on the Unitree G1 embodiment; the three-stage paradigm has not been verified on other humanoid platforms to confirm that the recipe transfers across hardware. **Second** , our evaluation does not include a controlled novel-object generalization study—training and test object sets share visual similarity, and we do not report success on strictly out-of-distribution objects. **Failure mode:** Relying on a single egocentric camera, MotionWAM falters when the manipulated object leaves the field of view or the head-camera viewpoint drifts from the training distribution, losing visual grounding and stalling; more failure cases are provided in Appendix F. 

8 

## **References** 

- [1] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang. Exbody2: Advanced expressive humanoid whole-body control. _arXiv preprint arXiv:2412.13196_ , 2024. 

- [2] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024. 

- [3] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [4] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Castaneda, Z.-A. Cao, J. Li, D. Minor, Q. Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [5] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang. Homie: Humanoid loco-manipulation with isomorphic exoskeleton cockpit. _arXiv preprint arXiv:2502.13013_ , 2025. 

- [6] Y. Ze, S. Zhao, W. Wang, A. Kanazawa, R. Duan, P. Abbeel, G. Shi, J. Wu, and C. K. Liu. Twist2: Scalable, portable, and holistic humanoid data collection system. _arXiv preprint arXiv:2511.02832_ , 2025. 

- [7] Y. Zhang, Y. Yuan, P. Gurunath, I. Gupta, S. Omidshafiei, A.-a. Agha-mohammadi, M. Vazquez-Chanlatte, L. Pedersen, T. He, and G. Shi. Falcon: Learning force-adaptive humanoid loco-manipulation. _arXiv preprint arXiv:2505.06776_ , 2025. 

- [8] Y. Li, Y. Zhang, W. Xiao, C. Pan, H. Weng, G. He, T. He, and G. Shi. Hold my beer: Learning gentle humanoid locomotion and end-effector stabilization control. _arXiv preprint arXiv:2505.24198_ , 2025. 

- [9] J. Li, X. Cheng, T. Huang, S. Yang, R.-Z. Qiu, and X. Wang. Amo: Adaptive motion optimization for hyper-dexterous humanoid whole-body control. _arXiv preprint arXiv:2505.03738_ , 2025. 

- [10] S. Wei, H. Jing, B. Li, Z. Zhao, J. Mao, Z. Ni, S. He, J. Liu, X. Liu, K. Kang, et al. Ψ0: An open foundation model towards universal humanoid loco-manipulation. _arXiv preprint arXiv:2603.12263_ , 2026. 

- [11] H. Jiang, J. Chen, Q. Bu, L. Chen, M. Shi, Y. Zhang, D. Li, C. Suo, C. Wang, Z. Peng, et al. Wholebodyvla: Towards unified latent vla for whole-body loco-manipulation control. _arXiv preprint arXiv:2512.11047_ , 2025. 

- [12] NVIDIA, J. Bjorck, N. C. Fernando Casta˜neda, X. Da, R. Ding, L. J. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, J. Jang, Z. Jiang, J. Kautz, K. Kundalia, L. Lao, Z. Li, Z. Lin, K. Lin, G. Liu, E. Llontop, L. Magne, A. Mandlekar, A. Narayan, S. Nasiriany, S. Reed, Y. L. Tan, G. Wang, Z. Wang, J. Wang, Q. Wang, J. Xiang, Y. Xie, Y. Xu, Z. Xu, S. Ye, Z. Yu, A. Zhang, H. Zhang, Y. Zhao, R. Zheng, and Y. Zhu. GR00T N1: An open foundation model for generalist humanoid robots. In _ArXiv Preprint_ , March 2025. 

- [13] M. Shi, S. Peng, J. Chen, H. Jiang, Y. Li, D. Huang, P. Luo, H. Li, and L. Chen. Egohumanoid: Unlocking in-the-wild loco-manipulation with robot-free egocentric demonstration. _arXiv preprint arXiv:2602.10106_ , 2026. 

- [14] Y. Hu, Y. Guo, P. Wang, X. Chen, Y.-J. Wang, J. Zhang, K. Sreenath, C. Lu, and J. Chen. Video prediction policy: A generalist robot policy with predictive visual representations. _arXiv preprint arXiv:2412.14803_ , 2024. 

9 

- [15] J. Pai, L. Achenbach, V. Montesinos, B. Forrai, O. Mees, and E. Nava. mimic-video: Videoaction models for generalizable robot control beyond vlas. _arXiv preprint arXiv:2512.15692_ , 2025. 

- [16] L. Li, Q. Zhang, Y. Luo, S. Yang, R. Wang, F. Han, M. Yu, Z. Gao, N. Xue, X. Zhu, et al. Causal world modeling for robot control. _arXiv preprint arXiv:2601.21998_ , 2026. 

- [17] J. Cen, C. Yu, H. Yuan, Y. Jiang, S. Huang, J. Guo, X. Li, Y. Song, H. Luo, F. Wang, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 

- [18] S. Li, Y. Gao, D. Sadigh, and S. Song. Unified video action model. _arXiv preprint arXiv:2503.00200_ , 2025. 

- [19] H. Bi, H. Tan, S. Xie, Z. Wang, S. Huang, H. Liu, R. Zhao, Y. Feng, C. Xiang, Y. Rong, et al. Motus: A unified latent action world model. _arXiv preprint arXiv:2512.13030_ , 2025. 

- [20] M. J. Kim, Y. Gao, T.-Y. Lin, Y.-C. Lin, Y. Ge, G. Lam, P. Liang, S. Song, M.-Y. Liu, C. Finn, et al. Cosmos policy: Fine-tuning video models for visuomotor control and planning. _arXiv preprint arXiv:2601.16163_ , 2026. 

- [21] T. Ma, J. Zheng, Z. Wang, C. Jiang, A. Cui, J. Liang, and S. Yang. Dit4dit: Jointly modeling video dynamics and actions for generalizable robot control. _arXiv preprint arXiv:2603.10448_ , 2026. 

- [22] A. Ye, B. Wang, C. Ni, G. Huang, G. Zhao, H. Li, H. Li, J. Li, J. Lv, J. Liu, et al. Gigaworldpolicy: An efficient action-centered world–action model. _arXiv preprint arXiv:2603.17240_ , 2026. 

- [23] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , page 02783649241273668, 2023. 

- [24] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 

- [25] T. Ma, J. Zhou, Z. Wang, R. Qiu, and J. Liang. Contrastive imitation learning for languageguided multi-task robotic manipulation. _arXiv preprint arXiv:2406.09738_ , 2024. 

- [26] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 

- [27] O. M. Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- [28] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [29] S. Liu, L. Wu, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, and J. Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 

- [30] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

10 

- [31] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, et al. _π_ 0 _._ 5: A vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- [32] R. Yang, Q. Yu, Y. Wu, R. Yan, B. Li, A.-C. Cheng, X. Zou, Y. Fang, X. Cheng, R.-Z. Qiu, et al. Egovla: Learning vision-language-action models from egocentric human videos. _arXiv preprint arXiv:2507.12440_ , 2025. 

- [33] J. Bruce, M. D. Dennis, A. Edwards, J. Parker-Holder, Y. Shi, E. Hughes, M. Lai, A. Mavalankar, R. Steigerwald, C. Apps, et al. Genie: Generative interactive environments. In _Forty-first International Conference on Machine Learning_ , 2024. 

- [34] N. Agarwal, A. Ali, M. Bala, Y. Balaji, E. Barker, T. Cai, P. Chattopadhyay, Y. Chen, Y. Cui, Y. Ding, et al. Cosmos world foundation model platform for physical ai. _arXiv preprint arXiv:2501.03575_ , 2025. 

- [35] M. Assran, A. Bardes, D. Fan, Q. Garrido, R. Howes, M. Muckley, A. Rizvi, C. Roberts, K. Sinha, A. Zholus, et al. V-jepa 2: Self-supervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. 

- [36] G. Lu, B. Jia, P. Li, Y. Chen, Z. Wang, Y. Tang, and S. Huang. Gwm: Towards scalable gaussian world models for robotic manipulation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 9263–9274, 2025. 

- [37] I. Nematollahi, B. DeMoss, A. L. Chandra, N. Hawes, W. Burgard, and I. Posner. Lumos: Language-conditioned imitation learning with world models. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 8219–8225. IEEE, 2025. 

- [38] F. Mentzer, D. Minnen, E. Agustsson, and M. Tschannen. Finite scalar quantization: Vq-vae made simple. _arXiv preprint arXiv:2309.15505_ , 2023. 

- [39] A. Ali, J. Bai, M. Bala, Y. Balaji, A. Blakeman, T. Cai, J. Cao, T. Cao, E. Cha, Y.-W. Chao, et al. World simulation with video foundation models for physical ai. _arXiv preprint arXiv:2511.00062_ , 2025. 

- [40] W. Peebles and S. Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 4195–4205, 2023. 

- [41] A. Azzolini, J. Bai, H. Brandon, J. Cao, P. Chattopadhyay, H. Chen, J. Chu, Y. Cui, J. Diamond, Y. Ding, et al. Cosmos-reason1: From physical common sense to embodied reasoning. _arXiv preprint arXiv:2503.15558_ , 2025. 

- [42] S. Bai, Y. Cai, R. Chen, K. Chen, X. Chen, Z. Cheng, L. Deng, W. Ding, C. Gao, C. Ge, et al. Qwen3-vl technical report. _arXiv preprint arXiv:2511.21631_ , 2025. 

- [43] J. Aldaco, T. Armstrong, R. Baruch, J. Bingham, S. Chan, K. Draper, D. Dwibedi, C. Finn, P. Florence, S. Goodrich, et al. Aloha 2: An enhanced low-cost hardware for bimanual teleoperation. _arXiv preprint arXiv:2405.02292_ , 2024. 

- [44] Z. Zhao, L. Yu, K. Jing, and N. Yang. Xrobotoolkit: A cross-platform framework for robot teleoperation. _arXiv preprint arXiv:2508.00097_ , 2025. 

- [45] K. He, X. Zhang, S. Ren, and J. Sun. Deep residual learning for image recognition. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 770–778, 2016. 

- [46] R. Hoque, P. Huang, D. J. Yoon, M. Sivapurapu, and J. Zhang. Egodex: Learning dexterous manipulation from large-scale egocentric video. _arXiv preprint arXiv:2505.11709_ , 2025. 

11 

- [47] S. Wu, X. Liu, S. Xie, P. Wang, X. Li, B. Yang, Z. Li, K. Zhu, H. Wu, Y. Liu, et al. Robocoin: An open-sourced bimanual robotic data collection for integrated manipulation. _arXiv preprint arXiv:2511.17441_ , 2025. 

- [48] Z. Zhao, H. Jing, X. Liu, J. Mao, A. Jha, H. Yang, R. Xue, S. Zakharor, V. Guizilini, and Y. Wang. Humanoid everyday: A comprehensive robotic dataset for open-world humanoid manipulation, 2025. URL `https://arxiv.org/abs/2510.08807` . 

- [49] Unitree Robotics. UnifoLM-WBT-Dataset: A high-quality real-world humanoid robot whole-body teleoperation dataset. `https://huggingface.co/collections/ unitreerobotics/unifolm-wbt-dataset` , 2026. 

12 

## **A Real-World Task Suite** 

### **A.1 Per-Task Language Prompts** 

Table 3 lists the natural-language task prompts for the real-world task suite listed in Fig. 4. 

|Task ID|Language Prompt|
|---|---|
|PnP Bottle|_Pick the bottle and place it in the basket._|
|Kick Soccer|_Kick the soccer into the goal net._|
|Retrieve Item|_Put the bag on the table and then close the drawer._|
|Load Cart|_Push the cart forward and put the clothes on the table into the cart._|
|Toss Garbage|_Throw the garbage into the trash can._|
|Lift Basket|_Take out the clothes basket under the table and place it on the table._|
|Stock Shelves|_Place the drinks on the upper shelf and the vegetables on the lower shelf._|
|Wipe Board|_Clean the whiteboard thoroughly._|
|Do Laundry|_Throw the clothes into the washing machine._|


Table 3: **Per-task language prompts for the nine real-world whole-body loco-manipulation tasks.** 

## **B Whole-Body Teleoperation Setup** 

### **B.1 Hardware** 

Our real-world experimental platform is built around the Unitree G1 humanoid robot. The robot is equipped with a pair of ALOHA 2 [43] grippers mounted on its 7-DoF dual arms, providing a 16-DoF upper-body manipulation interface. Egocentric observations are captured by a single Intel RealSense D435i RGB camera mounted at the head. A workstation with a single NVIDIA RTX 4090 GPU runs the policy server, which the on-board controller queries in closed loop over WebSocket. 

### **B.2 VR-Based Teleoperation Pipeline** 

We collect Stage 3 demonstrations through a VR-based teleoperation pipeline that produces _wholebody_ trajectories covering locomotion, torso motion, height regulation, foot interaction, and bimanual hand manipulation in a single action space. The operator wears a PICO VR headset and wraps two PICO trackers around the ankles and holds two hand controllers; the XRoboToolkit [44] framework streams a synchronized tracking signal which is converted into a full 24-joint SMPL whole-body pose. SONIC retargets this SMPL pose into 29-DoF joint angles that drive the G1 in closed loop, while the data exporter records the resulting state, command, and visual streams as a LeRobot-format episode at 50 Hz, together with the language goal. 

## **C Model and Training Configuration** 

Table 4 summarizes the model and optimizer hyperparameters of MotionWAM. The Video DiT backbone is initialised from Cosmos-Predict2.5-2B [39], with text and VAE encoders frozen throughout all three stages. Our MotionDiT follows the DiT-B configuration introduced in DiT4DiT [21], with the action and state dimensions enlarged to accommodate our cross-embodiment Stage 2 mixture (see Appendix E). All three stages share a single flow-matching objective with the per-stage modifications described in Sec. 3.3. 

## **D Baseline Training Configurations** 

Every baseline is finetuned on the same Stage 3 demonstrations as MotionWAM (cf. Appendix E) and consumes the same egocentric RGB observations, language goals, and proprioceptive states. 

13 

Table 4: **MotionWAM model and training configurations.** A single flow-matching objective is reused across all three stages; only the data mixture, learning rates, and number of trainable modules change. 

|Parameter|Stage 1|Stage 2<br>Stage 3|
|---|---|---|
|_Video DiT_|||
|Base VGM|Co|smos-Predict2.5-2B [39]|
|Attention implementation||flash-attention 2|
|Hidden feature dim||2048<br>|
|Conditional frame timestep||1_×_10<sup>_−_4</sup>|
|Future flow inference steps||1|
|_Motion DiT_|||
|Action model type||DiT-B|
|Hidden size / Output dim||2560|
|Positional embedding|i|nterleaved self-attention|
|Max sequence length||1024|
|Action dim (_Da_)|–|66<br>66|
|State dim (_Ds_)|–|64<br>64|
|Past action window|–|0<br>0|
|Cross attention dim||2048|
|Dropout / Final dropout||0_._2/ True|
|Norm type||AdaLN|
|Num inference timesteps|–|4<br>4|
|Repeated diffusion steps (train)|–|8<br>4|
|Noise_β_ (_α, β, s_)||(1_._5_,_ 1_._0_,_ 0_._999)|
|Num timestep buckets||1000|
|_Training_|||
|Frozen modules||VAE + text encoder|
|Per-device batch size|8|8<br>8|
|Number of GPUs|128|32<br>8|
|Max training steps|100,000|50,000<br>15,000|
|<br>Num warmup steps|5,000<br>|2,500<br>750<br><br>|
|Video DiT LR|1_×_10<sup>_−_5</sup>|1_×_10<sup>_−_5</sup><br>1_×_10<sup>_−_5</sup><br><br>|
|Motion DiT LR|–|1_×_10<sup>_−_4</sup><br>1_×_10<sup>_−_4</sup>|
|LR scheduler||cosine with min lr|
|Min LR||5_×_10<sup>_−_7</sup>|
|Gradient clipping||1_._0|
|Gradient accumulation steps||1<br>|
|Optimizer|AdamW|,(_β_1_, β_2)=(0_._9_,_0_._95),_ϵ_=10<sup>_−_8</sup><br>|
|Weight decay||10<sup>_−_8</sup>|


**Diffusion Policy (DP)** [23] is a representative non-VLA visuomotor policy that models action sequences via a conditional denoising diffusion process; **ACT** [24] is a transformer-based actionchunking policy that predicts a short sequence of future actions from visual and proprioceptive inputs in a single forward pass; _π_ **0** _._ **5** [31] is a generalist VLA policy that couples a pretrained vision– language backbone with a flow-matching action expert and is co-trained on heterogeneous robot data to support open-world manipulation; and **GR00T-N1.7** [30] is NVIDIA’s open humanoid foundation model, pairing a vision–language reasoning module with a diffusion-transformer action head and pretrained on a large mixture of human and humanoid data for whole-body control. Below we detail the model adaptations and training recipes used for DP, ACT, and our parameter-matched Qwen3DiT baseline; the remaining VLA baselines (GR00T-N1.7 and _π_ 0 _._ 5) follow their respective official fine-tuning recipes. 

**Diffusion Policy (DP) [23].** We follow the original recipe: a pre-trained ResNet-18 [45] is used as the visual encoder and a UNet-based denoiser predicts the action sequence conditioned on the visual and proprioceptive features. We set the learning rate to 1 _×_ 10<sup>_−_4</sup> and the global batch size to 64, and train for 40,000 steps on 8 NVIDIA A100 GPUs. At inference, we run 100 iterative denoising steps to progressively transform random noise into actionable whole-body trajectories. We observe that 

14 

DP fails on most loco-manipulation tasks, suggesting that the UNet-based DP model has insufficient visual capacity for the egocentric, whole-body setting. 

**Action Chunking with Transformers (ACT) [24].** To apply the ACT framework to whole-body humanoid loco-manipulation, we modify the action head to generate a 66-dimensional action vector for the Unitree G1, which includes the two gripper states. Consistent with the public ACT release, we utilize a chunk size of 100 and configure the transformer with 4 encoder layers and 1 decoder layer. The remaining hyperparameters—specifically the learning rate, batch size, and total training steps—remain identical to the DP setup described above. 

**Qwen3DiT.** Qwen3DiT is a custom, parameter-matched baseline that we construct as a direct ablation of the video-pretrained backbone in MotionWAM: it replaces the Cosmos-Predict2.5 Video DiT with the Qwen3-VL [42] 2B foundation model as the visual–language backbone, while keeping the Motion DiT, the unified motion-latent action space, and the observation/proprioception interface identical to MotionWAM. To provide a stringent ablation, Qwen3DiT is subjected to the exact same Stage 2 cross-embodiment action post-training and Stage 3 Unitree G1 fine-tuning pipeline as MotionWAM (see Appendix E); only Stage 1 egocentric video pretraining is omitted, since Qwen3-VL already provides a static image–text prior that replaces the role of Stage 1 in MotionWAM. All training settings follow the Stage 2 and Stage 3 columns of Table 4. This setting isolates the contribution of the video world model prior over a static VLM prior at matched capacity and under a matched training budget. 

## **E Per-Stage Data Composition** 

The three training stages ingest progressively narrower but progressively more action-grounded data. Stages 1 and 2 each draw from a weighted mixture of public datasets while Stage 3 fine-tunes on our in-house Unitree G1 demonstrations. 

**Stage 1 — egocentric video pretraining.** Stage 1 trains the Video DiT alone on a weighted mixture of egocentric human and humanoid-robot video; the action-related sources are read for their video streams only and any action labels are ignored. The mixture weights—budgeted across three domains (human at 30%, G1-class humanoids at 50%, other real robots at 20%)—are listed in Table 5. Inside each domain the per-source weights are allocated by ~~�~~ #episodes to avoid letting any single dataset dominate. 

Table 5: **Stage 1 video-pretraining mixture.** Weights are normalized so that the listed values sum to one. The “human” domain receives 30%, “G1-class humanoid” 50%, and “other real robots” 20% of the budget. 

|Source|Embodiment|Weight|
|---|---|---|
|EgoDex [46]|Human (egocentric)|0.300|
|GR00T-X-Embodiment-Sim (GR1) [30]|Fourier GR1 (sim)|0.255|
|RoboCOIN (G1edu/Galbot/Leju) [47]|G1edu/Galbot/Leju|0.080|
|GR00T-Teleop-GR1-Robot [30]|Fourier GR1 (real)|0.071|
|Humanoid-Everyday [48]|Unitree G1|0.047|
|UnifoLM-WBT [49]|Unitree G1 (WBT)|0.023|
|PSI-Real [10]|Unitree G1|0.013|
|PSI-Simple [10]|Unitree G1|0.011|
|RoboCOIN (R1<br>~~L~~ite + RMC-AIDA-L) [47]|R1<br>~~L~~ite, AIDA-L|0.200|


**Stage 2 — cross-embodiment action post-training.** Stage 2 attaches the Motion DiT and cotrains the Video DiT and Motion DiT on a heterogeneous mixture of action-labelled humanoid datasets, routed through per-embodiment input/output projectors around the shared Motion DiT trunk. Action vectors are right-padded to the maximum action dimension (66) with an accompanying 

15 

mask that marks the valid channels for each embodiment, so heterogeneous action layouts can share the same DiT trunk. 

**Stage 3 — Unitree G1 whole-body fine-tuning.** Stage 3 fine-tunes the full network end-to-end on our in-house teleoperated whole-body dataset. We collect 200 episodes per task on the nine real-world loco-manipulation tasks listed in Table 3, recorded at 50 Hz on the Unitree G1 platform described in Appendix B. All Stage 3 episodes share a single embodiment tag. 

## **F Failure Cases** 

Figure 6 illustrates representative failure modes of MotionWAM observed across the nine real-world loco-manipulation tasks. Because MotionWAM relies on a single egocentric head-mounted camera, the dominant failure mode arises when the manipulated object leaves the camera’s field of view or the head-camera viewpoint drifts away from the training distribution: visual grounding is lost and the policy either stalls or commits to an inaccurate whole-body trajectory. 


Figure 6: **Representative failure cases of MotionWAM on the nine real-world whole-body locomanipulation tasks.** Most failures trace back to loss of visual grounding when the manipulated object exits the egocentric field of view or the head-camera viewpoint drifts from the training distribution. 

16 


Figure 7: **Representative MotionWAM inference demonstrations on the nine real-world whole-** 17 **body loco-manipulation tasks.** 

