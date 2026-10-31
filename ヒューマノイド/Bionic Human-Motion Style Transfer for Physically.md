---
title: "Bionic Human-Motion Style Transfer for Physically Executable Whole-Body Control of Humanoid Robots"
date: "2026-06-02"
authors: "Tianchen Huang; Mingkuan Zhao; Yang Gao; Feiyang Yuan; Junchi Gu; Xiaohu Zhang"
url: https://arxiv.org/abs/2606.03536
pdf: https://arxiv.org/pdf/2606.03536
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.03536)** / [論文ページ](https://arxiv.org/abs/2606.03536)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Bionic Human-Motion Style Transfer for Physically Executable Whole-Body Control of Humanoid Robots 

Tianchen Huang<sup>1</sup><sup>**_†_**</sup> , Mingkuan Zhao<sup>2</sup><sup>**_†_**</sup> , Yang Gao<sup>1</sup> , Feiyang Yuan<sup>1</sup> , Junchi Gu<sup>1</sup> , Xiaohu Zhang<sup>1</sup> , Dongdong Zhao<sup>3</sup> , Shi Yan<sup>3</sup> , Yu Wang<sup>1*</sup> , Wei Gao<sup>1*</sup> , Shiwu Zhang<sup>1</sup> 

> 1Institute of Humanoid Robots, Department of Precision Machinery and Precision Instrumentation, University of Science and Technology of China, Hefei, Anhui, 230026, China. 

> 2School of Computer Science and Technology, Faculty of Electronic and Information Engineering, Xi’an Jiaotong University, Xi’an, Shaanxi, 710049, China. 

- 3School of Information Science and Engineering, Lanzhou University, Lanzhou, Gansu, 730000, China. 

*Corresponding author(s). E-mail(s): wangyuustc@ustc.edu.cn; weigao@ustc.edu.cn; 

> **_†_** These authors contributed equally to this work. 

#### **Abstract** 

Expressive whole-body motion is important for humanoid robots operating in human environments, where robots are expected to move stably while presenting readable and adjustable body behaviors. However, most expressive motions are still obtained from fixed demonstrations or manually designed scripts, making it difficult to reuse a demonstrated style across different motion contents. Inspired by the way human motion styles convey affective and intentional cues through gait rhythm, posture, arm swing and body sway, this paper proposes a bionic generation-to-control framework for exemplar-driven style transfer on humanoid robots. Given a short human style exemplar and a target content motion, the proposed framework generates a stylized whole-body reference that preserves the intended motion content while transferring the demonstrated style. A physics-aware multi-condition latent diffusion model is developed to fuse style, content and trajectory conditions, and classifier-free guidance is used to 

1 

adjust the style intensity without retraining. To improve hardware executability, contact-consistency and temporal-smoothness regularization are imposed on decoded motions during training. The generated references are then converted into G1-compatible robot references and executed by a preview-based whole-body tracking policy trained with a cluster-and-distill strategy. Simulation and Unitree G1 experiments show that the proposed method can transfer short human style exemplars to diverse robot motion contents, reduce contact and jitter artifacts compared with animation-oriented style-transfer baselines, and achieve a **96** **_._ 0%** success rate over **125** reported real-robot trials. The results demonstrate the feasibility of using short human motion exemplars as reusable bionic sources for physically executable expressive humanoid motion. 

**Keywords:** bionic motion generation, humanoid robot, human motion style transfer, whole-body control, motion diffusion, physically executable motion, expressive locomotion 

# **1 Introduction** 

Humanoid robots are increasingly expected to work in social, service and humancoexistence environments. In these settings, stable locomotion and task completion are necessary but not sufficient: the robot’s body motion should also be legible, human-like and adjustable. Human motion style is an important bionic source for this capability because people perceive affect and intent from gait rhythm, arm swing, trunk posture and movement dynamics [1–4]. Recent studies on robot emotion expression further indicate that body movement itself can shape how humans interpret a robot’s state and communicative intent [5, 6]. This makes expressive locomotion a relevant engineering target for humanoid robots, not only an animation problem. 

Most humanoid control research still emphasizes stability margins, tracking errors, disturbance rejection and task success. These objectives are essential for real hardware, yet they usually treat a reference motion as fixed and pay limited attention to style variations on the same motion content. In contrast, arbitrary motion style transfer in computer animation can generate visually natural stylized motions from short exemplars [7–10]. Directly applying such generated sequences to humanoid robots is difficult because robot execution must satisfy contact stability, joint velocity limits, torque limits and closed-loop tracking constraints. A visually plausible motion may still contain stance-foot drift, ground penetration or high-frequency joint oscillations that make hardware execution unreliable. 

This paper studies the following problem: given a content motion and a short human style exemplar, generate a full-body reference that preserves the content trajectory, expresses the target human motion style, and can be stably executed by a real humanoid robot. The content motion specifies task semantics such as walking direction or turning pattern; the style exemplar supplies bionic expressive cues such as slower rhythm, asymmetric sway or raised-arm posture; and the robot controller must turn the generated reference into physically executable joint commands. 

2 

This formulation introduces several coupled challenges. First, style amplification can alter contact rhythm and center-of-mass motion, which may reduce balance robustness. Second, diffusion-based generation may produce foot sliding, ground penetration and high-frequency joint jitter if contact and smoothness are only checked after sampling. Third, the whole-body tracker must handle different style intensities and motion contents without retraining for each generated sequence. Fourth, style recognizability and physical executability form a practical trade-off: stronger stylization may improve perceptual metrics but degrade support-foot stability or hardware tracking. 

To address these issues, we propose a bionic generation-to-control pipeline for humanoid robots. The method is not intended as a pure animation generator or a pure controller trainer. Instead, it connects human-motion-inspired style transfer with robot execution through a physics-aware multi-condition latent diffusion model, retargeting and a preview-based whole-body tracking policy. Contact-consistency and temporal-smoothness regularization are computed on decoded motions during diffusion training, so that style cues are encouraged to remain within a robot-executable motion space before tracking. The tracker is trained with generated stylized trajectories and a cluster-and-distill procedure, improving robustness to style-dependent reference variations. 

The main contributions are: 

1. We formulate human-motion-inspired style transfer as a bionic whole-body control problem for humanoid robots, linking exemplar-based human motion styles with real robot executability. 

2. We develop a physics-aware multi-condition latent diffusion model that injects style cues while suppressing contact inconsistency and high-frequency joint oscillations through decoded-motion regularization. 

3. We integrate the generated stylized references with a whole-body tracking policy trained on style-diverse motion references through a cluster-and-distill strategy, enabling robust deployment of diverse stylized motions. 

4. We validate the pipeline in simulation and on a Unitree G1 humanoid robot, reporting both perceptual style metrics and robot-oriented feasibility metrics. 

# **2 Bionic Motivation and Related Background** 

## **2.1 Human-Motion-Inspired Bionic Background** 

Bionic robot research converts biological motion principles, morphology and interaction cues into engineered mechanisms and controllers. In humanoid and legged robots, human-inspired jumping, smooth foot trajectory planning, anthropomorphic exoskeleton design, and bio-inspired gait generation with CPGs or reflex mechanisms have been used to improve dynamic motion, physical feasibility and human–robot compatibility [11–13]. These studies suggest that human motion should not be treated only as visual animation data. For humanoid robots, human-derived motion patterns must also be transformed into references that satisfy contact, balance and tracking constraints. 

Classical humanoid locomotion control provides the physical substrate for this work. Preview control of ZMP [14], capture-point and capturability analysis [15, 

3 

16], DCM/MPC formulations [17, 18], and optimization-based systems on full humanoids [19] established how planned trajectories can respect balance and contact constraints. These methods usually focus on robust walking and task-space tracking rather than style variation. Our work uses this control perspective to constrain generated expressive motions toward a space that can be tracked by a humanoid platform. 

## **2.2 Expressive Body Motion as Style Source** 

Human motion style is a perceptual and kinematic phenomenon. Studies in affective neuroscience and movement science show that emotions and intentions can be recognized from body expressions, gait, posture and motion dynamics [1–4]. For human–robot interaction, this matters because robots can communicate nonverbal states through body motion even when facial or speech channels are limited. Reviews and experiments on emotional robot movement report that gesture, body pose, vertical oscillation and movement timing influence perceived affect and clarity [5, 6]. These findings support the bionic premise of this paper: human style exemplars can serve as compact sources of expressive cues for humanoid whole-body behaviors. 

Compared with social-robot gesture studies, humanoid whole-body expression has a stronger physical constraint. A stylized gait modifies support timing, trunk posture and arm swing simultaneously. Therefore, expressive locomotion cannot be treated as an upper-body animation overlay; it must be designed together with contact consistency, balance and tracking robustness. 

## **2.3 Robot Executability Gap in Generative Style Transfer** 

Motion style transfer aims to change the style of a motion while preserving its content. Feed-forward and unpaired methods demonstrated that content and style can be separated and recombined for character animation [7, 8, 20]. Motion Puzzle introduced body-part-level composition for arbitrary style transfer [9], and recent latent or diffusion-based methods further improved diversity and controllability [10, 21–24]. Text-to-motion diffusion models such as MDM, MotionDiffuse and MoFusion also provide a broader foundation for conditional human motion generation [25–27]. 

These animation-oriented methods are important baselines, but they rarely guarantee robot executability. A generated motion may look natural or carry recognizable style cues in kinematic evaluation, while still exhibiting stance-foot sliding, ground penetration or high-frequency joint jitter that violates hardware constraints. Physicsguided motion generation methods such as PhysDiff identify floating, foot sliding and penetration as common artifacts in motion diffusion [28]. Our method follows this deployment-oriented motivation, but focuses on exemplar-driven style transfer for humanoid robots: physics-aware losses are imposed on decoded stylized references, and the resulting motions are further retargeted and tracked by a whole-body controller. 

4 

## **2.4 Whole-Body Control Requirements for Humanoid Execution** 

Whole-body tracking has become a practical route for deploying diverse humanoid skills. DeepMimic and AMP showed how reference tracking and adversarial motion priors can produce natural-looking simulated skills [29, 30]. PHC and universal humanoid representations improved persistent imitation and recovery across large motion sets [31, 32]. Recent humanoid trackers further emphasize deployment: ExBody and ExBody2 focus on expressive upper-body imitation with robust locomotion [33, 34], GMT and Any2Track pursue generalized tracking under motion diversity and disturbances [35, 36], and ASAP, BeyondMimic, KungfuBot and related systems address sim-to-real adaptation or highly dynamic skills [37–40]. 

Our work is complementary to these trackers. Rather than only asking whether a policy can track an existing reference, we study how to generate a short-exemplarbased stylized reference that remains suitable for tracking. The closed loop from human style exemplar to physics-aware generation, retargeting, tracking and real-robot validation is the central distinction. 

# **3 Human-Motion-Inspired Style Generation** 

## **3.1 Pipeline Overview** 

A unified pipeline from human-motion style generation to humanoid execution is presented. For any executable content motion from MoCap, video-derived skeletons or open motion repositories, the user supplies a short human style exemplar together with a guidance scale _λ_ to control style intensity at inference. The content motion specifies the intended action and global trajectory, such as straight walking, turning or circular walking. The style exemplar provides reusable human-motion cues, such as gait rhythm, body sway, arm posture and asymmetric movement tendency. The goal is to transfer the demonstrated style to the given content motion, instead of replaying the style exemplar as a fixed scripted behavior. 

The pipeline synthesizes a stylized motion using a physics-aware multi-condition latent diffusion model, converts the generated motion into a G1-compatible reference, and executes it on the robot with a whole-body tracking policy. The generation model is conditioned on content, style and trajectory so that the produced motion can preserve the target action, express the human-derived style and maintain the global path structure. Contact-consistency and temporal-smoothness regularization are applied during generation training to reduce artifacts that would hinder downstream execution. The tracker is trained with both human motion data and generated stylized trajectories, allowing it to adapt to style-dependent reference variations without switching controllers. This cascaded design separates bionic style transfer at the generation stage from physical execution at the tracking stage, and yields style-faithful whole-body behaviors on humanoid robots. 

5 


**Fig. 1** Physics-aware multi-condition latent diffusion architecture. Content, style and trajectory streams are encoded and fused as conditional context for the denoising Transformer. The style stream transfers human-derived motion cues from a short exemplar, the content stream preserves the target action, and the trajectory stream maintains the global path. Contact-consistency and temporal-smoothness losses are computed on decoded motions during training to improve downstream humanoid execution. 

## **3.2 Physics-Aware Multi-Condition Latent Diffusion** 

As illustrated in Fig. 1, the motion generation framework follows a multi-condition latent diffusion formulation for exemplar-driven motion style transfer. Similar to MCM-LDM [10], content, style and trajectory are used as complementary conditions during denoising. The difference lies in how these conditions are fused and optimized for humanoid execution. Instead of relying only on content concatenation and adaptive modulation of self-attention and feed-forward layers, the proposed denoiser organizes content, style and trajectory as explicit condition tokens and fuses them with motion latent tokens through cross-attention. 

The framework consists of multi-stream condition encoding, context fusion and a Transformer denoiser with staged conditioning. In each denoising block, the style condition modulates the self-attention branch, the fused condition context is used for cross-attention, and the trajectory condition modulates the feed-forward branch. This design allows motion tokens to retrieve content, style and trajectory cues at the token level, while the subsequent physics-aware regularization constrains the generated references toward downstream humanoid execution. 

### **3.2.1 Framework Architecture** 

The diffusion model is defined in the latent space of a pre-trained motion VAE. For each motion sequence, the VAE encoder maps the input motion to a fixed-length latent token sequence. At timestep _τ_ , the denoiser takes as input the noised latent token sequence **x** _τ ∈_ R<sup>_B×S×D_</sup> together with three conditional streams, namely content, style and trajectory, and predicts the additive Gaussian noise. Here, _B_ , _S_ and _D_ denote the batch size, the number of latent tokens and the latent dimension, respectively. The 

6 

reverse diffusion process estimates clean latent tokens in the VAE latent space. These denoised latent tokens are then decoded by the frozen VAE decoder to recover motion features, which are subsequently used for retargeting and tracking. To synchronize the three conditional streams, the timestep _τ_ is encoded by a sinusoidal embedding followed by an MLP to obtain a diffusion-step embedding _eτ ∈_ R<sup>_B×D_</sup> , which is injected additively into the three condition representations before they are fused. 

For the content stream, the root translation of the content motion _x_ cnt is removed before being fed into the content encoder. The encoder is pre-trained with SmoothL1 reconstruction in feature and joint spaces and a KL regularizer as 


where _x ∈_ R<sup>_B×T ×_263</sup> is the input motion feature sequence, J( _·_ ) is the deterministic mapping to joint space, _qϕ_ ( _z|x_ ) is a Gaussian posterior parameterized over a sequence of latent tokens, _x_ ˆ is the motion feature reconstructed by the decoder, and _β_ rec, _β_ joint and _β_ kl are VAE pre-training weights. After pre-training, both the VAE encoder and decoder are kept fixed during diffusion training and inference. The produced latent token sequence is instance-normalized, shifted by _eτ_ through broadcasted addition, augmented with positional encoding, and refined by a single-layer Transformer encoder. A learned token-mixing linear projection is then used to obtain the final content token sequence _C_ cnt _∈_ R<sup>_B×_6</sup><sup>_×D_</sup> . 

For the trajectory stream, the root translation sequence _c_ path _∈_ R<sup>_B×T ×_3</sup> extracted from the content motion is encoded by a Transformer-based trajectory encoder. The output single global trajectory token is shifted by _eτ_ to obtain the time-conditioned trajectory token sequence _C_ traj<sup>seq</sup><sup>_∈_R</sup><sup>_B×_1</sup><sup>_×D_, and its squeezed version defines the global</sup> trajectory vector _c_ traj _∈_ R<sup>_B×D_</sup> . 

For the style stream, the style motion _x_ sty is encoded by a frozen MotionCLIP encoder [41] into a single embedding vector. This embedding is projected to the diffusion latent dimension by a ReLU-linear layer and shifted by the timestep embedding _eτ_ to form a time-conditioned single-token sequence _C_ sty<sup>seq</sup><sup>_∈_R</sup><sup>_B×_1</sup><sup>_×D_.Thesameten-</sup> sor with the token dimension removed defines the global style vector _c_ sty _∈_ R<sup>_B×D_</sup> , which is used to condition the adaptive normalization parameters of the self-attention branch in each denoiser block. 

Condition fusion is implemented inside a multi-condition Diffusion Transformer. The three time-conditioned token sequences are concatenated along the sequence dimension to form an explicit condition context, 


Different from modulation-only fusion used in prior multi-condition style-transfer diffusion models [10], this context is used as Keys and Values in a cross-attention branch, while the current motion latent tokens serve as Queries. This enables the denoising tokens to retrieve content, style and trajectory information directly from the condition tokens at each denoising stage. 

7 

Each denoiser block contains a style-conditioned self-attention branch, a crossattention branch over _C_ , and a trajectory-conditioned feed-forward branch. In the self-attention branch, LayerNorm is applied without affine parameters, and the affine shift, affine scale and residual gate are produced by an MLP conditioned on _c_ sty. In the feed-forward branch, an MLP conditioned on _c_ traj produces the corresponding affine and gating parameters. The cross-attention branch adds the context-dependent update to the motion tokens through a residual connection. 

### **3.2.2 Training Objective and Controllable Inference** 

Given a clean latent motion **x** 0, the forward process of the conditional latent diffusion produces **x** _τ_ by injecting Gaussian noise under a fixed schedule. The denoiser _ϵθ_ is trained with a mean squared error objective as 


Classifier-free guidance is enabled by randomly dropping the style condition with probability _p_ drop during training. Specifically, the MotionCLIP style embedding before the style projection network is replaced by a zero vector for unconditional noise prediction, while the content and trajectory conditions are kept unchanged. During inference, the unconditional and conditional noise predictions are computed and combined using a guidance scale _λ_ as 


where _ϵ_<sup>(</sup> _θ_<sup>_u_)</sup> denotes the denoiser output obtained by using a zero style encoding, and _ϵ_<sup>(</sup> _θ_<sup>_c_)</sup> denotes the output obtained with the original style encoding. The guidance scale _λ_ therefore controls the strength of the transferred style at inference without retraining the generation model. After iterative denoising, the final latent estimate is decoded by the frozen VAE decoder to produce the stylized motion feature sequence. 

### **3.2.3 Physics-Aware Regularization** 

While latent diffusion models can generate diverse stylized motions, kinematically plausible results are not necessarily executable by a humanoid robot. In contrast to animation-oriented style-transfer objectives that mainly evaluate content preservation, style expression and trajectory consistency, we augment the diffusion objective with physics-aware regularization for robot deployment. These terms are not computed directly on **x** _τ_ , but on joint trajectories decoded from the model’s estimate of the clean latent motion at a randomly sampled training timestep. This design biases the denoising model toward references with fewer contact and smoothness artifacts before they are converted to G1-compatible references and tracked. 

Specifically, for each training sample, **x** _τ_ is formed by adding Gaussian noise to the VAE latent tokens, and a noise prediction _ϵ_ ˆ _τ_ is obtained. Using the noise-scheduler 

8 

coefficient _α_ ¯ _τ_ , an estimate of the clean latent tokens is constructed as 


**x** ˆ0 is then decoded with the frozen VAE decoder to obtain predicted motion features, which are converted to joint positions using the mapping function J( _·_ ). The corresponding joint references are obtained by applying the same mapping to the ground-truth motion features in the training batch. This results in the predicted and reference jointposition trajectories ( _q_<sup>pred</sup> _, q_<sup>ref</sup> ), where _qf,t_ denotes the position of foot-related joint _f_ at frame _t_ . These trajectories are used only during training for the two losses below. 

First, to enforce contact stability, undesired foot sliding and ground penetration are penalized during stance. Let _F_ denote the foot-related joints used in the loss. The reference foot speed is defined by finite differences of joint positions as _vf,t_<sup>ref=</sup><sup>_∥q_</sup> _f,t_<sup>ref</sup><sup>_−_</sup> _qf,t_<sup>ref</sup> _−_ 1<sup>_∥_2, and the stance mask is constructed as</sup><sup>_sf,t_=1[</sup><sup>_v_</sup> _f,t_<sup>ref</sup><sup>_< δv_] with</sup><sup>_δv_= 0</sup><sup>_._002. The</sup> contact loss applies hinge penalties to the predicted foot speed _vf,t_<sup>pred</sup> = _∥qf,t_<sup>pred</sup><sup>_−q_</sup> _f,t_<sup>pred</sup> _−_ 1<sup>_∥_2</sup> and height _h_<sup>pred</sup> _f,t_ with a penetration tolerance _δh_ = 0 _._ 001 as 


Second, to suppress high-frequency joint oscillations, a smoothness regularization is imposed on first- and second-order temporal differences of the joint trajectories. Let **v** _t_ = _qt − qt−_ 1 and **a** _t_ = **v** _t −_ **v** _t−_ 1 denote the velocity and acceleration tensors. The smoothness loss matches predicted and reference derivatives using _ℓ_ 1 penalties as 


Both _L_ contact and _L_ smooth require reference motions to construct _q_<sup>ref</sup> and the stance mask, and are therefore applied only during training. 

# **4 Humanoid Control and Deployment** 

## **4.1 Reference-Preview Whole-Body Tracking** 

Before tracking, each generated motion is converted offline into a G1-compatible reference with joint ordering, joint-limit handling and kinematic filtering. The same conversion procedure is used for all generated motions and all baseline motions before robot-oriented evaluation. 

Whole-body motion tracking is then formulated as closed-loop control with respect to the converted reference. The policy receives proprioceptive observations and a shorthorizon future reference. The proprioceptive observation includes body orientation, 

9 

body angular velocity, joint positions, joint velocities, the previous action and a fixedlength history buffer. The future reference covers a one-second preview window with 10 uniformly sampled future instants. For each preview instant, root height, roll and pitch, root linear velocity, yaw angular velocity in the local root frame, and joint references are provided. 

The preview features are concatenated into a temporal feature, compressed by a lightweight temporal encoder, and fused with the proprioceptive observation. This design allows the policy to anticipate style-dependent rhythm and contact timing, which is important for stabilizing the robot near swing–stance transitions. The policy outputs target joint positions at 50 Hz, which are tracked by a low-level PD controller running at 1000 Hz. Joint-specific PD gains are used on the real robot, with proportional gains ranging from 50 to 200 across different joints. 

## **4.2 Style-Diverse Cluster-and-Distill Training** 

The tracker is trained to handle the G1-compatible reference distribution produced from the proposed style-transfer model. The training set contains G1-compatible references converted from LaFAN1, a filtered subset of AMASS, and 1000 stylized trajectories generated by the proposed generator. In this work, we retain locomotionrelated and whole-body motions that can be retargeted to the G1 platform, resulting in 77 LaFAN1 sequences and 3142 AMASS clips for tracker training. Non-executable motions are filtered following the PHC protocol [31]. Introducing stylized trajectories allows the policy to encounter and adapt to them from the outset of training, because style transfer can change gait rhythm, trunk motion, arm posture and contact timing. 

The expert policies are trained with a DeepMimic-style reference-tracking reward, following the design principle used in recent humanoid motion-tracking systems: reference-tracking terms are kept positive and dominant, while a small number of regularization terms are added for sim-to-real robustness and smooth control [29, 35, 38]. The reward encourages the simulated robot to track the converted reference in joint space, root state and key end-effectors, while penalizing stance-foot slip, joint-limit violation and abrupt action changes. The detailed reward definitions and weights are provided in Appendix A. 

Because different motion categories exhibit distinct patterns that cannot be well captured by a single policy, the motions are first grouped into four content-level clusters, including straight walking, turning, circular walking and upper-body-emphasized locomotion, and one expert policy is trained for each cluster. During expert training, mild domain randomization is applied to link mass, link inertia, ground friction, joint friction, motor response and sensor noise. The same randomization setting is used for all experts and tracker-ablation variants. After training the experts, DAgger is employed to distill them into a single deployable generalist policy. The whole process is illustrated in Fig. 2. 

## **4.3 Deployment Protocol** 

The proposed framework is deployed in two stages. In the offline stage, the styletransfer model generates a stylized human-motion reference, which is converted and 

10 


**Fig. 2** Cluster-and-distill training for stylized whole-body tracking. Expert policies are first trained on content-specific motion clusters with dynamics randomization. Their behaviors are then distilled into a single deployable policy through Dataset Aggregation, allowing the robot to execute diverse stylized references without switching controllers. 

filtered into a G1-compatible whole-body reference. Diffusion sampling is performed with DDIM using 50 inference steps. On a workstation with an Intel Core i7-12700 CPU and two NVIDIA GeForce RTX 3080 Ti GPUs, the average pure generation time is about 0 _._ 24 s per action after warm-up. The complete offline export, including generation, saving motion files and video rendering, takes about 0 _._ 98 s per action. Video rendering is used only for visualization and is not part of the robot control loop. 

In the online stage, only the reference-preview tracking policy and the low-level PD controller run on the robot. The reference motion is provided at 30 Hz, the policy is updated at 50 Hz, and the low-level PD controller runs at 1000 Hz. Therefore, the real-time requirement is imposed on the tracking policy and the low-level control loop, while diffusion sampling is treated as offline preparation. Hardware trials are terminated when the robot falls, triggers a safety shutdown, or shows unrecoverable tracking divergence. 

# **5 Experimental Results and Analysis** 

## **5.1 Experimental Platform and Settings** 

The experiments evaluate three questions. First, whether the proposed generator can preserve motion content while transferring human-motion-inspired style cues. Second, whether the decoded-motion regularization improves robot-oriented feasibility, especially contact consistency and joint smoothness. Third, whether the converted references can be tracked on a real humanoid robot under different style intensities. Unless otherwise specified, all generated references are processed through the same reference-conversion and tracking pipeline before computing robot-oriented metrics. 

11 

**Table 1** Robot deployment and evaluation settings. 

|**Item**|**Setting**|
|---|---|
|Robot platform|Unitree G1 humanoid robot|
|Simulation backend|Isaac Sim 5.0|
|Robot model|Unitree G1, 29 active DoFs|
|Reference source|Stylized whole-body references generated offline and converted to the G1 robot<br>model|
|Reference conversion|Offline conversion from generated human motion to G1-compatible joint refer-<br>ences, with joint-limit handling and infeasible-motion filtering|
|Reference rate|30 Hz|
|Policy update rate|50 Hz|
|Low-level control rate|1000 Hz|
|Control interface|Joint-position targets tracked by low-level PD control|
|PD gains|Joint-specific proportional gains in the range of 50–200|
|Deployment terrain|Flat indoor ground|
|Trial protocol|Guidance-scale trials over _λ ∈{_0_,_0_._25_,_0_._5_,_0_._75_,_1_._0_}_, with 25 hardware trials per<br>scale|
|Success criterion|Completion of the full motion without falling, safety shutdown or unrecoverable<br>tracking divergence|
|Offline computation|DDIM sampling with 50 inference steps; about 0_._24 s per action for pure generation<br>and about 0_._98 s per action for complete offline export|
|Workstation|Intel Core i7-12700 CPU and 2_×_ NVIDIA GeForce RTX 3080 Ti GPUs|


## **5.2 Evaluation Metrics for Style and Robot Executability** 

We report two groups of metrics. The perceptual group evaluates whether the generated motions remain close to human motion distributions and preserve recognizable content and style. Fr´echet Motion Distance (FMD), Content Recognition Accuracy (CRA) and Style Recognition Accuracy (SRA) are computed following common motion style transfer protocols [9, 42, 43]. These metrics are useful for comparison with animation-oriented baselines, but they do not directly measure whether a humanoid robot can execute the generated reference. 

The robot-oriented group evaluates physical feasibility and closed-loop execution. Foot Sliding Factor (FSF) measures horizontal stance-foot drift per contact frame. A frame is labeled as a contact frame if the foot height is below _hc_ = 0 _._ 05 m and the inter-frame displacement satisfies _∥_ **p** _f_ ( _t_ ) _−_ **p** _f_ ( _t −_ 1) _∥_ 2 _<_ 0 _._ 02 m. For foot _f_ , the accumulated horizontal sliding is computed as 


where **p**<sup>_xy_</sup> _f_<sup>(</sup><sup>_t_)isthehorizontalfootpositionand</sup><sup>_Cf_isthesetofcontactframes.FSF</sup> is then defined as 


where _S_<sup>¯</sup> _f_ = _Sf /Nf_ and _Nf_ = _|{t | t ∈Cf , t −_ 1 _∈Cf }|_ is the number of valid consecutive contact-frame pairs for foot _f_ . A lower FSF indicates more stable stance-foot contact. 

_A_ pos and _J_ pos measure acceleration-level and jerk-level finite differences of joint positions, reflecting reference smoothness. Given a joint-position trajectory **q** ( _t_ ) with 

12 

length _T_ , they are defined as 


where 


and 


where 


Lower values indicate smoother references with fewer high-frequency joint oscillations. 

Success Rate (SR) is the ratio of trials completed without falling, safety shutdown or unrecoverable tracking divergence. Tracking error is additionally reported in the tracking-strategy ablation to evaluate closed-loop reference-following accuracy. It is computed as the mean normalized joint-pose deviation between the simulated robot state and the converted reference over the controlled joints and rollout horizon. 

## **5.3 Human Motion Style Generation Results** 

Table 2 compares the proposed method with MotionDiffuse [26], Motion Puzzle [9] and MCM-LDM [10]. The purpose is not to claim the best animation score, but to examine whether style transfer remains executable after conversion to G1-compatible references and tracking. For all methods, the simulated success rate in Table 2 is evaluated under the same reference-conversion and closed-loop tracking protocol. We use 16 converted actions for each method, and each action is rolled out 256 times with different random seeds and perturbations, resulting in 4096 simulation rollouts per method. The reported Sim. SR is computed as the number of successful rollouts divided by 4096. A rollout is counted as successful if the robot completes the full reference without falling, safety termination or unrecoverable tracking divergence. 

MCM-LDM achieves the best FMD and SRA among the reported methods, indicating strong kinematic perceptual quality. However, its higher FSF and lower simulated SR show that perceptual quality alone is insufficient for robot deployment. The proposed method shows a more favorable trade-off, with lower FSF, smoother joint references and a higher simulated closed-loop SR. For MotionDiffuse, FMD, CRA and SRA are not reported because its text-conditioned interface does not provide the same exemplar-style label setting required by the classifier-based style-transfer evaluation protocol; therefore, only robot-oriented feasibility metrics are reported after conversion to G1-compatible references and tracking. 

Qualitative examples are shown in Fig. 3. The same human style exemplar can be reused across different content motions, while different exemplars produce visibly distinct gait rhythm, trunk posture and arm-motion patterns. 

13 

**Table 2** Comparison of perceptual quality and robot-oriented physical feasibility. Simulated SR is computed over 4096 rollouts for each method, using 16 converted actions and 256 rollouts per action. _↑_ indicates higher is better, _↓_ indicates lower is better. 

||**Per**|**ceptual Qua**|**lity**|**Ro**|**bot-Orient**|**ed Feasibili**|**ty**|
|---|---|---|---|---|---|---|---|
|**Method**|**FMD** _↓_|**CRA** _↑_<br>(%)|**SRA** _↑_<br>(%)|**FSF** _↓_<br>(m/frame)|**_A_pos** _↓_<br>(a.u.)|**_J_pos** _↓_<br>(a.u.)|**Sim. SR** _↑_<br>(%)|
|MotionDiffuse|–|–|–|0.006233|0.497825|0.339368|27.93%|
|Motion Puzzle|113.31|26.31|46.33|0.005853|0.568928|0.822193|67.14%|
|MCM-LDM|**34.78**|33.62|**58.66**|0.006273|0.372012|0.316419|59.81%|
|**Ours**|39.81|**35.18**|55.55|**0.004722**|**0.307976**|**0.283434**|**96.02%**|


**Fig. 3** Exemplar-driven style transfer across different contents and styles. Short human style exemplars are transferred to different target content motions while the intended trajectory and action structure are preserved. 

## **5.4 Ablation of Tracking Strategy** 

To evaluate the contribution of the tracking design, we compare four tracker-training strategies under the same set of converted stylized references. The evaluation set in Table 3 is different from that in Table 2 and contains more diverse stylized references. This ablation isolates the control stage: the generated references and referenceconversion procedure are fixed, while the tracker training strategy is changed. The evaluation uses 64 converted stylized references covering different content motions, 

14 

**Table 3** Ablation of tracker-training strategies under the same converted stylized references. SP denotes a single policy, SE denotes clustered specialized experts, and CD denotes the final cluster-and-distill policy. Simulated success rate is computed over 4096 rollouts for each variant. 

|**Strategy**|**Stylized refs.**|**Experts**|**DAgger**|**Tracking err. (a.u.)** _↓_|**Sim. SR (count, %)** _↑_|
|---|---|---|---|---|---|
|SP-original|No|No|No|0.122|3328/4096, 81.25%|
|SP-stylized|Yes|No|No|0.096|3624/4096, 88.48%|
|SE-only|Yes|Yes|No|**0.083**|**3856/4096, 94.14%**|
|**CD-generalist**|Yes|Yes|Yes|0.086|3808/4096, 92.97%|


style exemplars and guidance scales. Each reference is rolled out 64 times in simulation with different random seeds and perturbations, resulting in 4096 rollouts for each tracker variant. A rollout is counted as successful if the robot completes the full reference without falling, safety termination or unrecoverable tracking divergence. 

Table 3 compares four variants. SP-original trains a single policy only on original motion references. SP-stylized additionally includes generated stylized references. SEonly uses clustered specialized experts without distillation. CD-generalist distills the experts into one deployable policy. The results show that stylized references improve adaptation to the generated reference distribution. SE-only achieves the best simulated metrics because each expert specializes in one motion cluster, but it assumes that the correct expert is selected for each reference. CD-generalist slightly sacrifices simulated tracking performance, removes this runtime expert-selection requirement, and is therefore used as the deployed controller. 

## **5.5 Robot-Oriented Physical Feasibility and Generation Ablation** 

Table 4 evaluates the two decoded-motion regularizers used during generation. Contact regularization reduces stance-foot drift, while smoothness regularization reduces highfrequency joint oscillation. The full model obtains the best values across FSF, _A_ pos and _J_ pos, supporting the role of physics-aware regularization in constraining style expression toward the robot-executable reference space. 

These results should be interpreted together with the downstream reference conversion and tracking stages. The decoded-motion regularizers are imposed before conversion to the G1 morphology, and therefore do not mathematically guarantee that contact and smoothness properties are exactly preserved after conversion. Instead, they reduce severe artifacts in the generated human-motion reference. The final executability claim is based on robot-oriented metrics computed after conversion to G1-compatible references and closed-loop tracking. 

## **5.6 Style Intensity Analysis** 

The classifier-free guidance scale _λ_ controls the intensity of the transferred style. We evaluate _λ ∈{_ 0 _,_ 0 _._ 25 _,_ 0 _._ 5 _,_ 0 _._ 75 _,_ 1 _._ 0 _}_ to examine the trade-off between style recognizability and robot executability. As _λ_ increases, the generated motion shows stronger style cues, reflected by higher SRA and qualitative body-motion changes. At the same time, excessive style amplification may increase foot sliding, joint jitter and tracking 

15 

**Table 4** Ablation of physics-aware regularization terms. 

||**FSF**|_A_pos|_J_pos|
|---|---|---|---|
|**Configuration**|(m/frame)_↓_|(a.u.)_↓_|(a.u.)_↓_|
|w/o both|0.005005|0.333533|0.308064|
|w/ contact regularization|0.004825|0.320142|0.294568|
|w/ smoothness regularization|0.004770|0.319252|0.294946|
|**w/ both**|**0.004722**|**0.307976**|**0.283434**|


**Table 5** Effect of guidance scale _λ_ on style expression and robot executability. Hardware SR is computed from 25 Unitree G1 trials per guidance scale. 

|**_λ_**|**SRA** _↑_|**FSF** _↓_|**_A_pos** _↓_|**_J_pos** _↓_|**Hardware**<br>**SR** _↑_|
|---|---|---|---|---|---|
||(%)|(m/frame)|(a.u.)|(a.u.)|(%)|
|0.00|17.22|0.002125|0.106100|0.082846|100.0%|
|0.25|42.44|0.002309|0.116894|0.092362|100.0%|
|0.50|51.56|0.002767|0.134200|0.109798|100.0%|
|0.75|55.56|0.002877|0.135287|0.111264|96.0%|
|1.00|58.30|0.003422|0.144717|0.120689|84.0%|


failure. SRA and robot-oriented feasibility metrics are averaged over the generated test motions for each guidance scale, while Hardware SR is computed from 25 Unitree G1 trials per scale. Table 5 therefore reports both style and robot-oriented metrics for each guidance scale. 

Figure 4 visualizes the effect of _λ_ in both simulation and real-robot deployment. Larger _λ_ values make the transferred style more recognizable, but also increase the risk of contact inconsistency and tracking difficulty. 

## **5.7 Real-Robot Deployment** 

The real-robot study deploys the generated references on a Unitree G1 humanoid robot using the G1-compatible reference conversion and reference-preview tracking policy described in Section 4. A trial is counted as successful only when the robot completes the full sequence without falling, triggering safety shutdown or showing unrecoverable tracking divergence. 

The deployment tests evaluate whether the generated style variations remain trackable after conversion to G1-compatible references. We quantitatively test multiple guidance scales and qualitatively examine representative style-content combinations, and report trial-level success according to the termination criteria in Table 1. Figure 3 shows representative style-content combinations, and Fig. 4 shows the corresponding intensity modulation in simulation and on hardware. 

In the reported guidance-scale experiment, 25 hardware trials are conducted for each _λ ∈{_ 0 _,_ 0 _._ 25 _,_ 0 _._ 5 _,_ 0 _._ 75 _,_ 1 _._ 0 _}_ , resulting in 125 Unitree G1 trials. The robot completes 120 out of 125 trials, corresponding to a hardware success rate of 96 _._ 0%. Most failures 

16 


**Fig. 4** Style intensity control in simulation and real Unitree G1 deployment. Increasing _λ_ strengthens human-like expressive cues, such as slower gait rhythm and upper-body sway, while the style intensity must remain within the physically executable range of the humanoid robot. 

occur at larger guidance scales, where stronger stylization increases upper-body sway, stance-timing distortion and tracking difficulty. 

## **5.8 Failure Analysis and Limitations** 

Several limitations are observed in deployment. First, excessive style amplification can produce high-frequency jitter and over-extended postures, indicating that the guidance scale must be bounded by robot kinematics and tracking robustness. Second, strong upper-body swing may shift the center of mass and reduce the support margin, especially when the style exemplar contains exaggerated arm motion. Third, asymmetric styles can disturb contact rhythm and cause stance-phase inconsistencies. Fourth, sharp turns and circular paths may increase yaw tracking error because style-dependent trunk motion is coupled with root orientation changes. 

17 

A further limitation is possible content-style entanglement. The MotionCLIP style embedding may contain not only expressive cues but also content-related motion tendencies, such as turning bias, stride asymmetry or arm-use patterns. The content and trajectory conditions help preserve the intended action and global path, but they do not provide a formal guarantee of perfect disentanglement. When a style exemplar contains strong turning or asymmetric stepping while the content motion is straight walking, residual yaw bias or stance-timing distortion may appear. 

Finally, the current real-robot validation is mainly conducted on flat indoor ground and uses a limited number of hardware trials compared with large-scale simulation evaluation. The present framework does not yet model complex terrain, external contacts or object interaction. Future work will extend the framework to terrain-aware generation, interaction-aware reference conversion and broader hardware evaluation. 

# **6 Conclusion** 

This paper presents a bionic generation-to-control framework for physically executable humanoid motion style transfer. Given a short human style exemplar and a target content motion, the proposed method generates a stylized whole-body reference that preserves the target action while transferring reusable human-motion cues. The generator uses a multi-condition latent diffusion model with explicit condition-token fusion, classifier-free style-intensity control, and decoded-motion contact-consistency and temporal-smoothness regularization. The generated references are converted into 29-DoF Unitree G1-compatible references and executed by a reference-preview whole-body tracker trained with style-diverse trajectories and a cluster-and-distill strategy. 

Experiments demonstrate that the proposed method achieves a favorable balance between style-transfer quality and robot-oriented physical feasibility. Although animation-oriented baselines obtain better kinematic perceptual scores in some reported metrics, the proposed pipeline improves stance-foot stability, joint smoothness and hardware execution success. The reported Unitree G1 experiments achieve a 96 _._ 0% success rate over 125 guidance-scale trials, showing the feasibility of transferring short human style exemplars to real humanoid whole-body motion. Future work will extend the framework to broader real-robot style-content combinations and richer human–robot interaction scenarios. 

# **A Tracking Reward Design** 

The expert policies are optimized with a weighted reference-tracking reward. To avoid notation conflict with the generation model, the robot joint position is denoted by **_θ_** _t_ , the policy action by **u** _t_ , the root pose by **b** _t_ , and the root velocity by **_ν_** _t_ . The subscript _θ_ in the denoising network _ϵθ_ denotes model parameters, whereas the bold symbol **_θ_** _t_ in this appendix denotes robot joint positions. Superscript _⋆_ denotes the converted G1-compatible reference. The total reward is the weighted sum of the terms in Table 6. 

The reward used at control step _t_ is therefore computed as the sum of each term multiplied by its weight in Table 6. The weights are kept fixed for all expert policies and all tracker-ablation variants. 

18 

**Table 6** Tracking reward terms used for expert-policy training. 

|**Term **|**Weight**|**Scale**|**Definition**|**Purpose**|
|---|---|---|---|---|
|_ρθ_|0_._30|_κθ_ = 2_._0|exp<br>�<br>_−κθ∥_**_θ_**_t −_**_θ_**<sup>_⋆_</sup><br>_t _<sup>_∥_2</sup><br>2<br>�<br><br>|Joint-position tracking over<br>controlled G1 joints.|
|_ρ_˙_θ_|0_._08|_κ_˙_θ_ = 0_._10|exp<br>�<br>_−κ_˙_θ∥_<sup>˙</sup>**_θ_**_t −_<sup>˙</sup>**_θ_**<sup>_⋆_</sup><br>_t _<sup>_∥_2</sup><br>2<br>�|Joint-velocity tracking to<br>reduce phase lag during style-<br>dependent rhythm changes.|
|_ρb_|0_._16|_κb_ = 4_._0|exp<br>�<br>_−κbdb_(**b**_t,_**b**<sup>_⋆_</sup><br>_t_ <sup>)2�</sup><br>|Root height, roll and pitch<br>tracking for balance.|
|_ρν_|0_._10|_κν_ = 1_._0|exp<br>�<br>_−κν∥_**_ν_**_t −_**_ν_**<sup>_⋆_</sup><br>_t _<sup>_∥_2</sup><br>2<br>�|Root linear velocity and<br>yaw-rate tracking.|
|_ρe_|0_._16|_κe_ = 8_._0|exp<br>�<br>_−κe|E|_<sup>_−_1 �</sup><br>_k∈E _<sup>_∥_</sup><sup>**p**</sup><sup>_k,t −_</sup><sup>**p**</sup><sup>_⋆_</sup><br>_k,t_<sup>_∥_2</sup><br>2<br>�|End-effector tracking for feet<br>and hands.|
|_ρ_slip|0_._06|_κ_slip = 25_._0|exp<br>�<br>_−κ_slip_|F|_<sup>_−_1 �</sup><br>_f∈F _<sup>_mf,t∥_</sup><sup>**v**</sup><sup>_xy_</sup><br>_f,t_<sup>_∥_2</sup><br>2<br>�|Stance-foot slip suppression.|
|_ρ_lim|0_._05|_κ_lim = 10_._0|exp<br>�<br>_−κ_lim_∥_[**_θ_**_t −_**_θ_**max]+ + [**_θ_**min _−_**_θ_**_t_]+_∥_<sup>2</sup><br>2<br>�<br>|Soft joint-limit regularization.|
|_ρu_|0_._06|_κu_ = 0_._05|exp<br>�<br>_−κu∥_**u**_t −_**u**_t−_1_∥_<sup>2</sup><br>2<br>�|Action-rate smoothing for<br>stable low-level PD tracking.|
|_ρ_alive|0_._03|–|1 if no termination condition is triggered,<br>otherwise 0|Sequence completion under fall<br>and safety checks.|


**Table 7** Symbols used in the tracking reward. 

|**Symbol**|**Meaning**|
|---|---|
|**_θ_**_t_<br>˙|Controlled G1 joint positions at control step _t_.|
|**_θ_**_t_|Controlled G1 joint velocities.|
|**u**_t_|Policy action, represented as joint-position targets.|
|**b**_t_<br>**_ν_**_t_|Root pose components used for tracking, including root height, roll and pitch.<br>Root velocity components, including local linear velocity and yaw angular velocity.|
|**p**_k,t_|Cartesian position of end-effector _k_.|
|_E_<br>_F_|End-effector set used for tracking, including feet and hands.<br>Foot set used for slip regularization.|
|_mf,t_<br>**v**<sup>_xy_</sup><br>_f,t_|Stance mask of foot _f_ at step _t_.<br>Horizontal velocity of foot _f_.|
|**_θ_**min_,_**_θ_**max<br>(_·_)<sup>_⋆_</sup><br>[_·_]+|Lower and upper joint limits of the G1 model.<br>Converted G1-compatible reference quantity.<br>Element-wise positive part.|
|_db_(_·, ·_)<br>_κ·_|Root-pose distance over height, roll and pitch.<br>Exponential penalty scale.|


**Author Contributions.** T.H. and M.Z. contributed equally to this work, including conceptualization, methodology, implementation, experiments, data analysis and writing the original draft. Y.G., F.Y., J.G., X.Z., D.Z. and S.Y. contributed to experiments, data processing, validation and manuscript revision. Y.W., W.G. and S.Z. supervised the work and contributed to review and editing. All authors read and approved the final manuscript. 

**Acknowledgements.** The authors have no additional acknowledgements to declare. 

**Funding.** This work was supported in part by the National Natural Science Foundation of China under Grants U22B2040, in part by the Major Project of Anhui Province’s Science and Technology Innovation Breakthrough Plan (202423h08050003), in part by the Key Science & Technology Project of Anhui 

19 

Province (202523j08050001), and in part by the Fundamental Research Funds for the Central Universities with grant No. YD2090002019. 

**Data Availability.** The data that support the findings of this study are available from the corresponding author upon reasonable request. 

**Conflict of Interest.** The authors certify that there is no conflict of interest pertaining to the content of this paper. 

**Ethical Approval and Consent to Participate.** Not applicable. 

**Consent for Publication.** Not applicable. 

# **References** 

- [1] De Gelder, B.: Why bodies? twelve reasons for including bodily expressions in affective neuroscience. Philosophical Transactions of the Royal Society B: Biological Sciences **364** (1535), 3475–3484 (2009) 

- [2] Zhang, M., Yu, L., Zhang, K., Du, B., Zhan, B., Chen, S., Jiang, X., Guo, S., Zhao, J., Wang, Y., _et al._ : Kinematic dataset of actors expressing emotions. Scientific data **7** (1), 292 (2020) 

- [3] Lott, L.L., Spengler, F.B., St¨achele, T., Schiller, B., Heinrichs, M.: Embody/emface as a new open tool to assess emotion recognition from body and face expressions. Scientific Reports **12** , 14165 (2022) https://doi.org/10.1038/ s41598-022-17866-w 

- [4] Riemer, H., Joseph, J.V., Lee, A.Y., Riemer, R.: Emotion and motion: Toward emotion recognition based on standing and walking. PLOS ONE **18** (9), 0290564 (2023) https://doi.org/10.1371/journal.pone.0290564 

- [5] Matsumaru, T.: Methods of generating emotional movements and methods of transmitting behavioral intentions: A perspective on human-coexistence robots. Sensors **22** (12), 4587 (2022) https://doi.org/10.3390/s22124587 

- [6] Mahzoon, H., Ueda, A., Yoshikawa, Y., Ishiguro, H.: Effect of robot’s vertical body movement on its perceived emotion: A preliminary study on vertical oscillation and transition. PLOS ONE **17** (8), 0271789 (2022) https://doi.org/10.1371/ journal.pone.0271789 

- [7] Aberman, K., Weng, Y., Lischinski, D., Cohen-Or, D., Chen, B.: Unpaired motion style transfer from video to animation. ACM Transactions on Graphics **39** (4) (2020) https://doi.org/10.1145/3386569.3392469 

- [8] Holden, D., Habibie, I., Kusajima, I., Komura, T.: Fast neural style transfer for motion data. IEEE Comput. Graph. Appl. **37** (4), 42–49 (2017) https://doi.org/ 10.1109/MCG.2017.3271464 

20 

- [9] Jang, D.-K., Park, S., Lee, S.-H.: Motion puzzle: Arbitrary motion style transfer by body part. ACM Transactions on Graphics **41** (3), 1–16 (2022) https://doi. org/10.1145/3516429 

- [10] Song, W., Jin, X., Li, S., Chen, C., Hao, A., Hou, X., Li, N., Qin, H.: Arbitrary motion style transfer with multi-condition motion latent diffusion model. 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 821–830 (2024) 

- [11] Wang, X., Guo, W., He, Z., Li, R., Zha, F., Sun, L.: Bionic jumping of humanoid robot via online centroid trajectory optimization and high dynamic motion controller. Journal of Bionic Engineering **21** (6), 2759–2778 (2024) https://doi.org/ 10.1007/s42235-024-00586-4 

- [12] Li, J., Gao, H., Wan, Y., Yu, H., Zhou, C.: A real-time planning and control framework for robust and dynamic quadrupedal locomotion. Journal of Bionic Engineering **20** , 1449–1466 (2023) https://doi.org/10.1007/s42235-023-00347-9 

- [13] Fang, J., Jin, Y., Wang, B., Liu, Z.: Bio-inspired central pattern generator for adaptive gait generation and stability in humanoid robots on sloped surfaces. Biomimetics **10** (9), 637 (2025) https://doi.org/10.3390/biomimetics10090637 

- [14] Kajita, S., Kanehiro, F., Kaneko, K., Fujiwara, K., Harada, K., Yokoi, K., Hirukawa, H.: Biped walking pattern generation by using preview control of zero-moment point. In: 2003 IEEE International Conference on Robotics and Automation (Cat. No.03CH37422), vol. 2, pp. 1620–16262 (2003). https://doi. org/10.1109/ROBOT.2003.1241826 

- [15] Pratt, J., Carff, J., Drakunov, S., Goswami, A.: Capture point: A step toward humanoid push recovery. In: 2006 6th IEEE-RAS International Conference on Humanoid Robots, pp. 200–207 (2006). https://doi.org/10.1109/ICHR.2006. 321385 

- [16] Koolen, T., Boer, T.D., Rebula, J., Goswami, A., Pratt, J.: Capturability-based analysis and control of legged locomotion, part 1: Theory and application to three simple gait models. The International Journal of Robotics Research **31** (9), 1094–1113 (2012) 

- [17] Wieber, P.-b.: Trajectory free linear model predictive control for stable walking in the presence of strong perturbations. In: 2006 6th IEEE-RAS International Conference on Humanoid Robots, pp. 137–142 (2006). https://doi.org/10.1109/ ICHR.2006.321375 

- [18] Herdt, A., Diedam, H., Wieber, P.-B., Dimitrov, D., Mombaur, K., Diehl, M.: Online walking motion generation with automatic foot step placement. Advanced Robotics **24** , 719–737 (2010) https://doi.org/10.1163/016918610X493552 

21 

- [19] Kuindersma, S., Deits, R., Fallon, M., Valenzuela, A., Dai, H., Permenter, F., Koolen, T., Marion, P., Tedrake, R.: Optimization-based locomotion planning, estimation, and control design for the atlas humanoid robot. Autonomous Robots **40** (2015) https://doi.org/10.1007/s10514-015-9479-3 

- [20] Aberman, K., Weng, Y., Lischinski, D., Cohen-Or, D., Chen, B.: Unpaired motion style transfer from video to animation. ACM Transactions on Graphics (TOG) (2020) 

- [21] Kim, B., Kim, J., Chang, H.J., Choi, J.Y.: Most: Motion style transformer between diverse action contents. IEEE (2024) 

- [22] Guo, C., Mu, Y., Zuo, X., Dai, P., Yan, Y., Lu, J., Cheng, L.: Generative human motion stylization in latent space (2024) 

- [23] Zhong, L., Xie, Y., Jampani, V., Sun, D., Jiang, H.: SMooDi: Stylized Motion Diffusion Model (2024). https://arxiv.org/abs/2407.12783 

- [24] Hu, L., Zhang, Z., Ye, Y., Xu, Y., Xia, S.: Diffusion-based Human Motion Style Transfer with Semantic Guidance (2024). https://arxiv.org/abs/2405.06646 

- [25] Tevet, G., Raab, S., Gordon, B., Shafir, Y., Cohen-Or, D., Bermano, A.H.: Human Motion Diffusion Model (2022). https://arxiv.org/abs/2209.14916 

- [26] Zhang, M., Cai, Z., Pan, L., Hong, F., Guo, X., Yang, L., Liu, Z.: MotionDiffuse: Text-Driven Human Motion Generation with Diffusion Model (2022). https:// arxiv.org/abs/2208.15001 

- [27] Dabral, R., Mughal, M.H., Golyanik, V., Theobalt, C.: Mofusion: A framework for denoising-diffusion-based motion synthesis. In: Computer Vision and Pattern Recognition (CVPR) (2023) 

- [28] Yuan, Y., Song, J., Iqbal, U., Vahdat, A., Kautz, J.: Physdiff: Physics-guided human motion diffusion model. In: Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), pp. 16010–16021 (2023) 

- [29] Peng, X.B., Abbeel, P., Levine, S., Panne, M.: Deepmimic: example-guided deep reinforcement learning of physics-based character skills. ACM Transactions on Graphics **37** (4), 1–14 (2018) https://doi.org/10.1145/3197517.3201311 

- [30] Peng, X.B., Ma, Z., Abbeel, P., Levine, S., Kanazawa, A.: Amp: adversarial motion priors for stylized physics-based character control. ACM Transactions on Graphics **40** (4), 1–20 (2021) https://doi.org/10.1145/3450626.3459670 

- [31] Luo, Z., Cao, J., Winkler, A., Kitani, K., Xu, W.: Perpetual Humanoid Control for Real-time Simulated Avatars (2023). https://arxiv.org/abs/2305.06456 

- [32] Luo, Z., Cao, J., Merel, J., Winkler, A., Huang, J., Kitani, K., Xu, W.: Universal 

22 

Humanoid Motion Representations for Physics-Based Control (2024). https:// arxiv.org/abs/2310.04582 

- [33] Cheng, X., Ji, Y., Chen, J., Yang, R., Yang, G., Wang, X.: Expressive Whole-Body Control for Humanoid Robots (2024). https://arxiv.org/abs/2402.16796 

- [34] Ji, M., Peng, X., Liu, F., Li, J., Yang, G., Cheng, X., Wang, X.: ExBody2: Advanced Expressive Humanoid Whole-Body Control (2025). https://arxiv.org/ abs/2412.13196 

- [35] Chen, Z., Ji, M., Cheng, X., Peng, X., Peng, X.B., Wang, X.: Gmt: General motion tracking for humanoid whole-body control. arXiv:2506.14770 (2025) 

- [36] Zhang, Z., Guo, J., Chen, C., Wang, J., Lin, C., Lian, Y., Xue, H., Wang, Z., Liu, M., Lyu, J., Liu, H., Wang, H., Yi, L.: Track Any Motions under Any Disturbances (2025). https://arxiv.org/abs/2509.13833 

- [37] He, T., Gao, J., Xiao, W., Zhang, Y., Wang, Z., Wang, J., Luo, Z., He, G., Sobanbab, N., Pan, C., Yi, Z., Qu, G., Kitani, K., Hodgins, J., Fan, L.J., Zhu, Y., Liu, C., Shi, G.: ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills (2025). https://arxiv.org/abs/2502.01143 

- [38] Liao, Q., Truong, T.E., Huang, X., Gao, Y., Tevet, G., Sreenath, K., Liu, C.K.: BeyondMimic: From Motion Tracking to Versatile Humanoid Control via Guided Diffusion (2025). https://arxiv.org/abs/2508.08241 

- [39] Xie, W., Han, J., Zheng, J., Li, H., Liu, X., Shi, J., Zhang, W., Bai, C., Li, X.: KungfuBot: Physics-Based Humanoid Whole-Body Control for Learning HighlyDynamic Skills (2025). https://arxiv.org/abs/2506.12851 

- [40] Han, J., Xie, W., Zheng, J., Shi, J., Zhang, W., Xiao, T., Bai, C.: KungfuBot2: Learning Versatile Motion Skills for Humanoid Whole-Body Control (2025). https://arxiv.org/abs/2509.16638 

- [41] Tevet, G., Gordon, B., Hertz, A., Bermano, A.H., Cohen-Or, D.: Motionclip: Exposing human motion generation to clip space. arXiv preprint arXiv:2203.08063 (2022) 

- [42] Park, S., Jang, D.-K., Lee, S.-H.: Diverse motion stylization for multiple style domains via spatial-temporal graph-based generative model. Proc. ACM Comput. Graph. Interact. Tech. **4** (3) (2021) https://doi.org/10.1145/3480145 

- [43] Song, W., Jin, X., Li, S., Chen, C., Hao, A., Hou, X.: Finestyle: Semanticaware fine-grained motion style transfer with dual interactive-flow fusion. IEEE Transactions on Visualization and Computer Graphics **29** (11), 4361–4371 (2023) https://doi.org/10.1109/TVCG.2023.3320216 

23 

