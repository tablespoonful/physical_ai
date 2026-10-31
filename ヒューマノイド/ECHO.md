---
title: "ECHO: Edge-Cloud Humanoid Orchestration for Language-to-Motion Control"
date: "2026-03-17"
authors: "Haozhe Jia; Jianfei Song; Yuan Zhang; Honglei Jin; Youcheng Fan; Wenshuo Chen"
url: https://arxiv.org/abs/2603.16188
pdf: https://arxiv.org/pdf/2603.16188
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.16188)** / [論文ページ](https://arxiv.org/abs/2603.16188)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **ECHO: Edge-Cloud Humanoid Orchestration for Language-to-Motion Control** 

Haozhe Jia<sup>1</sup><sup>_,_2</sup><sup>_,∗_</sup> , Jianfei Song<sup>2</sup><sup>_,∗_</sup> , Yuan Zhang<sup>3</sup><sup>_,∗_</sup> , Honglei Jin<sup>1</sup><sup>_,_3</sup> , Youcheng Fan<sup>1</sup> , Wenshuo Chen<sup>1</sup> , Wei Zhang<sup>2</sup><sup>_,†_</sup> , and Yutao Yue<sup>1</sup><sup>_,_4</sup><sup>_,†_</sup> 

**_Abstract_ — We present ECHO, an edge–cloud framework for language-driven whole-body control of humanoid robots. A cloud-hosted diffusion-based text-to-motion generator synthesizes motion references from natural language instructions, while an edge-deployed reinforcement-learning tracker executes them in closed loop on the robot. The two modules are bridged by a compact, robot-native 38-dimensional motion representation that encodes joint angles, root planar velocity, root height, and a continuous 6D root orientation per frame, eliminating inferencetime retargeting from human body models and remaining directly compatible with low-level PD control. The generator adopts a 1D convolutional UNet with cross-attention conditioned on CLIP-encoded text features; at inference, DDIM sampling with 10 denoising steps and classifier-free guidance produces motion sequences in approximately one second on a cloud GPU. The tracker follows a Teacher–Student paradigm: a privileged teacher policy is distilled into a lightweight student equipped with an evidential adaptation module for sim-toreal transfer, further strengthened by morphological symmetry constraints and domain randomization. An autonomous fall recovery mechanism detects falls via onboard IMU readings and retrieves recovery trajectories from a pre-built motion library. We evaluate ECHO on a retargeted HumanML3D benchmark, where it achieves strong generation quality (FID 0.029, R-Precision Top-1 0.686) under a unified robot-domain evaluator, while maintaining high motion safety and trajectory consistency. Real-world experiments on a Unitree G1 humanoid demonstrate stable execution of diverse text commands with zero hardware fine-tuning.** 

**For an online demo and additional video results, please visit our Project Page.** 

## I. INTRODUCTION 

Natural language is an appealing interface for humanoid robots: it is expressive, low-effort for humans, and naturally describes goals, styles, and constraints. The past few years have witnessed rapid progress in _language-conditioned wholebody control_ , driven by stronger vision-language representations, large-scale motion datasets, and improved simulationto-real (sim2real) reinforcement learning. Recent systems can follow diverse instructions and produce agile full-body behaviors in simulation and, in some cases, on real hardware [1], [2]. In parallel, modular pipelines that leverage powerful human motion generators (e.g., SMPL/SMPL-X based representations) have enabled language-to-motion generation 

> _∗_ Equal contribution. 

> _†_ Corresponding authors: Wei Zhang and Yutao Yue. 

> 1The Hong Kong University of Science and Technology (Guangzhou). 

> 2LimX Dynamics Technology Co., Ltd. 

> 3Shandong University. 

> 4Institute of Deep Perception Technology, Jiangsu Industrial Technology Research Institute (JITRI). 

followed by retargeting and tracking on humanoid platforms [3], [4]. More recently, retargeting-free directions have emerged, for instance by conditioning policies on compact motion latents rather than explicit decoded human poses [5]. 

Despite these advances, _deployment-oriented_ language-tohumanoid control still faces a fundamental tension between semantic expressivity, real-time closed-loop control, and engineering practicality. First, fully end-to-end language-action models (e.g., LangWBC/SENTINEL-style approaches) couple high-level language understanding with low-level control in a single on-board policy [1], [2]. While elegant, this design often implies that the robot must execute substantial languageaction inference under high-frequency control constraints. On resource-limited humanoid computers, maintaining low latency and high control rates can directly compete with running large models, which in turn makes it difficult to scale semantic complexity without sacrificing real-time stability. Moreover, forcing one network to simultaneously solve openvocabulary instruction grounding _and_ contact-rich dynamics increases training and sim2real burdens, and complicates safety enforcement. 

Second, modular _human-motion-first_ pipelines such as FRoM-W1 generate human whole-body motion in a body model space and then retarget to a specific humanoid [3], [4]. Although they benefit from abundant human motion data, they introduce non-trivial retargeting engineering: morphology mismatch (human body model vs. robot kinematics), constraint inconsistencies (joint limits, contacts, balance), and error accumulation across stages. In addition, human body parameterizations often include degrees of freedom that are unnecessary for robot execution, making the generation-toexecution interface less efficient for real-time streaming and tracking. 

Third, while retargeting-free latent-guidance approaches [5] mitigate decoding overhead, their latent interfaces are typically co-trained and tightly coupled with downstream policies. This entanglement severely degrades modularity: migrating across robot platforms or integrating with established tracking stacks necessitates complete interface realignment, thereby restricting portability and interpretability. 

To address these limitations, we advocate for a strict decoupling of generation and execution in language-tohumanoid pipelines: a generative model should synthesize semantically consistent motion references, whereas a dedicated tracker enforces physical feasibility via closed-loop control. Consequently, we propose **ECHO** , an inferencetime retargeting-free, _edge–cloud_ framework for language- 


Fig. 1. **Overview of the proposed framework:** The system features a Cloud-Edge decoupled deployment. The Cloud module utilizes a Diffusion Generator to synthesize motion from text instructions via CLIP encoding. The Edge module employs an RL-trained Student Policy that tracks targets using estimated privileged information. The resulting actions are executed via a PD controller for stable humanoid motion in the real world. 

directed whole-body control. Specifically, a cloud-deployed diffusion model generates _robot-native_ motion references, which are streamed as short-horizon chunks to an on-board, lightweight tracking controller. This distributed architecture circumvents stringent hardware constraints, ensuring low onboard compute overhead while sustaining high-frequency, robust physical execution. 

On the **cloud side** , our generator adopts a 1D convolutional UNet backbone conditioned on language via a frozen CLIP encoder [6] and cross-attention injection. The model is trained with DDPM [7] using a masked _L_ 2 objective and classifierfree guidance [8], and uses DDIM [9] at inference to produce high-quality motion in as few as 10 denoising steps, achieving approximately one-second cloud-to-robot latency, balancing generation fidelity and real-time deployment constraints. The training corpus retargets HumanML3D motions [10] (a captioned subset of AMASS [11]) to the robot skeleton via General Motion Retargeting (GMR), preserving the original text–motion pairing. On the **edge side** , our tracker employs an Asymmetric Actor-Critic Teacher-Student pipeline [12]: a teacher policy is first trained with access to privileged physical states under PPO [13]. A student adaptation module is then trained with Evidential Deep Regression [14] to handle sim-to-real uncertainty and distill the teacher’s behavior using only proprioceptive history. A morphological symmetry loss is further introduced to eliminate asymmetric gait artifacts during training. 

A key element bridging both modules is a compact 

38D velocity-based robot motion representation that directly matches the humanoid execution interface. Each frame is a 38-dimensional vector composed of: (i) 29D joint positions (robot joint angles), (ii) 2D root planar velocity in an aligned global frame, (iii) 1D root height, and (iv) 6D continuous root rotation representation to avoid discontinuities [15]. Motions are generated at 50 FPS and transmitted to the on-board tracker via a persistent WebSocket connection. This representation avoids explicit global root positions (reducing drift and improving robustness), removes unnecessary humanbody degrees of freedom, and provides a stable target for a receding-horizon tracker to follow under contacts and disturbances. 

We validate the proposed framework in extensive simulation experiments and on a real humanoid robot. Results show that our system produces instruction-consistent, temporally coherent whole-body behaviors while improving deployment efficiency and robustness, compared with representative endto-end and retargeting-based baselines. 

Our main contributions are: 

- A deployment-oriented **edge–cloud** language-tohumanoid control paradigm that streams diffusiongenerated motion references from the cloud and executes them with an on-board tracker in closed loop. 

- A **robot-native 38D velocity-based** motion interface that is retargeting-free at inference time, streamable, and tracker-friendly, bridging generative motion planning and real-time humanoid execution. 

- Comprehensive evaluations in simulation and **real-robot** experiments, along with two novel robot-centric metrics: **Motion Safety Score (MSS)** and **Root Trajectory Consistency (RTC)** , which quantify hardware constraint compliance and path-shape fidelity, two properties critical for safe deployment that standard text-to-motion benchmarks do not cover. 

## II. RELATED WORK 

## _A. Motion Generation_ 

3D human motion generation has evolved from early GANbased [16] and AE-based [17] deterministic mappings to highfidelity probabilistic synthesis. To improve diversity, VAEbased frameworks like TEMOS [18] aligned text and motion in joint latent spaces. Recently, diffusion models such as MDM [19] and MotionDiffuse [20] have set new benchmarks via iterative denoising, while MLD [21] enhances efficiency through latent space diffusion. Further advancements continue to improve temporal alignment [22], frequency-domain robustness for robotic applications [23], and fundamental diffusion properties [24], [25]. Despite these advances, purely kinematic methods often struggle with physical artifacts such as foot sliding and penetration. While models like PhysDiff [26] integrate physics-based projection into the diffusion loop to mitigate these issues, they often incur significant computational overhead. Beyond standalone T2M synthesis, recent deployment-oriented systems further couple motion generation with physically executable humanoid control, either through modular pipelines with retargeting/tracking [3], [27] or by bypassing explicit decoding/retargeting via latent-guided control [5]. 

Different from previous monolithic or purely kinematic approaches, our framework facilitates an integrated pipeline that decouples instruction parsing, T2M diffusion generation, and RL-based physical tracking. The diffusion component ensures semantic alignment and temporal consistency in the synthesized motion, while the tracking module translates these kinematic references into dynamically feasible whole-body maneuvers for robust execution on humanoid platforms. 

## _B. Whole Body Motion Tracking_ 

The core objective of motion tracking is to faithfully execute given kinematic references. Early approaches relied heavily on trajectory optimization [28], while Deep Reinforcement Learning (DRL) popularized data-driven imitation, utilizing task-specific rewards to minimize tracking errors for individual skills [29]. To overcome the scalability bottlenecks of this “one-skill-one-policy” paradigm, unified tracking controllers emerged. By leveraging adversarial objectives [30], a single policy can robustly track extensive motion databases without per-task retraining. 

Recently, the scope of tracking has expanded to executing dynamically synthesized trajectories, particularly those from language-conditioned motion generators [1], [2]. In such hierarchical pipelines, a universal low-level tracking policy operates in a closed loop to follow upstream kinematic references [3], [27]. To minimize staging latency during 

tracking, retargeting-free approaches condition the tracker directly on language-grounded latents rather than explicit poses [5]. Finally, deploying these universal tracking policies onto physical humanoids relies fundamentally on robust simto-real transfer to bridge the dynamics gap. 

## III. METHOD 

As illustrated in Fig. 1, the proposed framework decouples language understanding from real-time control by distributing computation across cloud and edge. A diffusion-based text-tomotion generator running on a remote server synthesizes robot-native motion references from natural language instructions. These reference sequences, represented in the compact 38D format described below, are then streamed to the on-board controller. The edge-deployed tracking policy executes the received references in closed loop, maintaining high control rates and robustness under contact and external disturbances. This separation of concerns enables flexible scaling of semantic complexity on the cloud side while preserving low-latency, physically grounded execution on the robot. In the following, we detail each component. 

## _A. Robot-Skeleton Motion Representation._ 

To enable stable diffusion-based generation, we transform raw robot kinematics into a compact, learning-friendly feature space. Given a robot with _Ndof_ = 29 actuators, the framewise state **m** _t ∈_ R<sup>38</sup> is defined as: 


where **q** _t ∈_ R<sup>29</sup> are joint angles, **v** _t_<sup>_root_</sup> _∈_ R<sup>2</sup> is the planar root velocity, _h_<sup>_root_</sup> _t ∈_ R is root height, and **R**<sup>6</sup> _t_<sup>_D_</sup> _∈_ R<sup>6</sup> represents root orientation. 

**Why Velocity for Root XY?** A critical design choice is representing the planar root translation as frame-wise velocity **v** _t_<sup>_root_</sup> = **p**<sup>_xy_</sup> _t_<sup>_−_</sup><sup>**p**</sup><sup>_xy_</sup> _t−_ 1<sup>, while keeping other dimensions absolute.</sup> This is because absolute XY coordinates are _unbounded_ and non-periodic, making them difficult for neural networks to predict directly. Learning absolute positions often leads to mode collapse or “teleportation” artifacts where the robot jumps discontinuously. In contrast, joint angles (physically limited), root height (ground-constrained), and rotations (cyclic) naturally lie on bounded manifolds. By predicting local velocity, we ensure the diffusion model learns consistent locomotion dynamics rather than memorizing global locations. **Why 6D Rotation?** We employ the continuous 6D representation [15] for root orientation instead of quaternions. The primary limitation of quaternions is the strict _unit norm constraint_ ( _∥_ **q** _rot∥_ 2 = 1). Neural networks struggle to output strictly normalized vectors, and enforcing normalization posthoc can disrupt gradient flow. The 6D representation is formed by the first two columns of the rotation matrix and requires no such constraint. Any 6 _D_ vector can be mapped to a valid rotation through Gram–Schmidt orthogonalization, which significantly stabilizes the training process. 

**Control-Centric Advantages.** This joint-space representation ( **q** _t_ ) is inherently compatible with robotic control. Unlike 

Cartesian-based methods that require Inverse Kinematics (IK), our generated sequences directly map to the robot’s actuators, ensuring kinematic feasibility and enabling seamless tracking by low-level PD controllers. 

## _B. Cloud: Text-to-Motion Generator_ 

We adopt a diffusion-based generative model to synthesize full-body motion sequences conditioned on natural language instructions. The model directly operates on the robot-native 38D representation, eliminating the need for inference-time retargeting from human body models. 

**Model Architecture.** The generative backbone employs a 1D convolutional UNet architecture with residual temporal blocks and adaptive group normalization (AdaGN). Text instructions are first encoded by a frozen CLIP ViT-B/32 visionlanguage model [6], whose output is refined by a lightweight Transformer encoder to produce a _dtext_ -dimensional language latent **z** _text_ . This latent is injected into each UNet block via cross-attention layers, enabling the network to condition motion generation on semantic instruction features. The UNet structure with down/up-sampling paths provides efficient multi-scale temporal modeling for motion sequences. 

We also implement a Transformer-based encoder-decoder variant (referred to as ECHO-Transformer in Table I) for architectural comparison. The model is trained to reverse a forward diffusion process that gradually corrupts a clean motion sequence **M** = _{_ **m** 1 _, . . . ,_ **m** _T }_ with Gaussian noise. Given a text prompt _c_ , the network learns to predict the denoised sequence **M** ˆ 0 from a noisy observation **M** _t_ at timestep _t_ . 

**Training.** We follow the DDPM objective [7] with _T_ diffusion timesteps and a linear noise schedule. At each training step, a random timestep _t ∼_ Uniform(1 _, T_ ) is sampled, and the network is tasked with directly predicting the clean motion **M** 0 from the noised input **M** _t_ . The loss function is a masked _L_ 2 reconstruction error, computed only over valid frames to handle variable-length sequences: 


where **mask** indicates valid frame positions and **M** _t_ = _~~√~~_ _<u>α</u>_ <u>¯</u> _t_ **<u>M</u>** 0 +<sup>_~~√~~_</sup> 1 _− α_ ¯ _t ϵ_ with _ϵ ∼N_ (0 _,_ **I** ). 

To enable classifier-free guidance [8], we randomly drop the text condition during training with probability _puncond_ , replacing **z** _text_ with a learned null embedding. At inference time, the model steers generation beyond the conditional prediction to enhance instruction adherence. 

The training corpus retargets HumanML3D motions [10] (a captioned subset of AMASS [11]) to the target robot skeleton using General Motion Retargeting (GMR), which preserves motion naturalness while adapting to the robot’s kinematic constraints; the original text–motion pairing is retained. All motion features are z-score normalized per dimension to stabilize training. We optimize the model using AdamW [31] with learning rate _η_ , and maintain an Exponential Moving Average (EMA) of the weights with decay _βema_ for stable generation at inference. 

**Inference.** At deployment, we employ DDIM [9] as our sampling strategy, which was selected through extensive ablation studies comparing DDPM, DDIM, and DPM-Solver schedulers (see Table II for details). DDIM enables efficient generation with only 10 denoising steps while maintaining high fidelity, reducing latency compared to the full 1000-step DDPM sampling. Classifier-free guidance is applied with scale _s_ = 2 _._ 5 to enhance semantic fidelity: 


The generator is deployed as a persistent inference server on cloud infrastructure, serving text-driven motion requests in real time (communication details in Section III-D). 

## _C. Tracker_ 

To execute precise whole-body motions, we build upon the teacher-student tracking architecture from prior work [32]. The teacher phase pre-trains an asymmetric actorcritic model [12]. First, an encoder _Eϕ_ compresses highdimensional privileged states into latent features _zt_ = _Eϕ_ ( _xt_ ). The teacher policy _πθ_ ( _at|ot, zt_ ) then maps these features alongside proprioceptive observations _ot_ to joint targets. To reduce variance, the critic _Vψ_ ( _ot, xt_ ) leverages the complete environmental state. We optimize the policy using Proximal Policy Optimization (PPO) [13] with Generalized Advantage Estimation [33]. 

The composite reward comprises a tracking term _Rtrack_ and a regularization term _Rreg_ . Following DeepMimic [29], _Rtrack_ aggregates exponential squared errors across joint positions and velocities: 


where **x** _k_ and **x**<sup>_∗_</sup> _k_<sup>denotethesimulatedactualstateand</sup> the desired reference state for feature _k_ , respectively. _wk_ represents the weight coefficient for each specific feature, and _σk_ is the scale factor controlling the sensitivity of the reward kernel. 

Furthermore, pure kinematic tracking often leads to destructive interaction forces. Therefore, strict physical feasibility penalties are introduced, including joint acceleration limits, motor torque soft limits, and a quadratic penalty for excessive landing impact forces _rimpact_ = _−_<sup>�</sup> ( _vz_<sup>_↓_)2</sup><sup>_·_I</sup><sup>_contact_.Con-</sup> currently, by incorporating a dense feet air-time reward, the robot is guided to form smooth swing-stance phase transitions [34]. 

To deploy the policy to the real world without privileged information _xt_ , the student adaptation phase trains an adaptation module _Aω_ using proprioceptive history _Ht_ = _{ot−H , . . . , ot}_ . To mitigate sim-to-real uncertainties, we model hidden state inference via evidential deep regression [14]. Specifically, _Aω_ ( _Ht_ ) outputs a Normal-Inverse-Gamma (NIG) distribution parameterized by **_ϕ_** _t_ = ( _µz, ν, α, β_ ), capturing both the estimated latent _zt_ and its predictive variance. We optimize this module using a negative log-likelihood 

## **Sim (MuJoCo)** 


Fig. 2. **Sim-to-Real Results:** Validation of robust tracking performance from simple gestures to dynamic maneuvers. 

(NLL) loss augmented with an evidence regularizer: 

_Ladapt_ ( _ω_ ) = _LNLL_ ( _zt|µz, ν, α, β_ ) + _λ_ reg _∥zt − µz∥_ (2 _ν_ + _α_ ) (5) 

This regularizer strictly penalizes overconfident erroneous predictions. The student policy _πS_ ( _at|ot, µz_ ) then recovers the teacher’s behavior via behavioral cloning, followed by low-rate PPO fine-tuning. 

To accelerate learning and eliminate asymmetric gaits (e.g., limping) [35], [36], we embed a morphological symmetry prior directly into the PPO update. Let _Tobs_ and _Tact_ denote mirror operators for the observation and action spaces. We penalize asymmetric policy outputs via: 


where _cµ_ and _cσ_ are weighting coefficients. Finally, we apply domain randomization to physical parameters (e.g., link masses, friction, actuator dynamics) during simulation rollouts to further bridge the reality gap. 

## _D. Deployment_ 

The trained generator and tracker are integrated into a distributed edge-cloud deployment architecture designed for practical humanoid control. 

**Edge-Cloud Communication.** The cloud-side inference server receives natural language instructions via a WebSocket connection, generates the corresponding motion sequence using the text-to-motion diffusion model, and transmits the result back to the robot. The server maintains a persistent connection, allowing successive instructions to be issued without re-initialization. The compact 38D representation 

minimizes network bandwidth, making the system viable even under moderate wireless latency. 

**On-Board Execution.** The student tracking policy, trained via the Teacher-Student distillation pipeline described in Section III-C, is exported to a lightweight inference format optimized for embedded deployment. At each control cycle, the policy receives the current proprioceptive state and the received motion reference, computes target joint positions, and remaps them to the robot’s actuation interface. To mitigate discretization artifacts and sudden reference transitions, an exponential moving average filter is applied to smooth action outputs before dispatching them to the low-level PD controller. This filtering preserves responsiveness while preventing torque spikes that could destabilize contact. 

**Sim-to-Real Transfer.** Policies are first validated in a MuJoCo-based simulation environment (sim2sim) before hardware deployment. We then transfer the student policy directly to a physical Unitree G1 (29-DoF EDU) humanoid robot without any hardware fine-tuning; the extensive domain randomization described in Section III-C proves critical in bridging the reality gap. 

**Fall Recovery.** To enhance real-world robustness, we implement an IMU-triggered autonomous fall recovery mechanism. It utilizes a two-stage retrieval procedure that first filters candidates by gravity alignment and then ranks them by joint configuration similarity to extract and execute the optimal recovery trajectory from a pre-built library. 

## IV. EXPERIMENTS AND RESULTS 

In this section, we evaluate the proposed ECHO framework from two complementary perspectives: 

TABLE I 

QUANTITATIVE COMPARISON OF TEXT-TO-MOTION GENERATION METHODS ON THE RETARGETED HUMANML3D. ALL BASELINES ARE RE-EVALUATED UNDER THE SAME MOCLIP ON THE RETARGETED TEST SPLIT. _±_ DENOTES 95% CONFIDENCE INTERVALS. **BOLD** : BEST OVERALL; <u>UNDERLINE:</u> BEST AMONG PRIOR WORKS. 

|Method||R-Precision _↑_||FID_↓_|Div._↑_|MM Dist._↓_|MSS _↑_|RTC _↑_|
|---|---|---|---|---|---|---|---|---|
||Top 1|Top 2|Top 3||||||
|Ground Truth|0_._774<sup>_±._004</sup>|0_._902<sup>_±._002</sup>|0_._943<sup>_±._001</sup>|0_._002|1_._375<sup>_±._003</sup>|-|0_._546<sup>_±._000</sup>|-|
|MDM [19]|0_._578<sup>_±._004</sup>|0_._755<sup>_±._004</sup>|0_._832<sup>_±._004</sup>|0_._073<sup>_±._001</sup>|1_._362<sup>_±._004</sup>|0_._651<sup>_±._017</sup>|0_._527<sup>_±._001</sup>|0_._442<sup>_±._002</sup>|
|TM2T [37]|0_._461<sup>_±._003</sup>|0_._612<sup>_±._004</sup>|0_._695<sup>_±._004</sup>|0_._183<sup>_±._001</sup>|1_._300<sup>_±._004</sup>|0_._561<sup>_±._017</sup>|**0**_._**542**<sup>_±._</sup><sup>**001**</sup>|0_._413<sup>_±._002</sup>|
|MotionDiffuse [20]|0_._269<sup>_±._003</sup>|0_._477<sup>_±._003</sup>|0_._696<sup>_±._002</sup>|0_._213<sup>_±._004</sup>|1_._310<sup>_±._006</sup>|1_._226<sup>_±._082</sup>|0_._323<sup>_±._002</sup>|0_._195<sup>_±._008</sup>|
|StableMofusion [38]|0_._683<sup>_±._003</sup>|0_._843<sup>_±._003</sup>|0_._905<sup>_±._002</sup>|0_._037<sup>_±._000</sup>|1_._368<sup>_±._004</sup>|0_._414<sup>_±._013</sup>|0_._405<sup>_±._001</sup>|0_._421<sup>_±._002</sup>|
|ECHO-Transformer|0_._668<sup>_±._004</sup>|0_._829<sup>_±._003</sup>|0_._895<sup>_±._002</sup>|0_._061<sup>_±._001</sup>|**1**_._**370**<sup>_±._</sup><sup>**005**</sup>|0_._375<sup>_±._013</sup>|0_._511<sup>_±._001</sup>|**0**_._**505**<sup>_±._</sup><sup>**002**</sup>|
|**ECHO-UNet (Ours)**|**0**_._**686**<sup>_±._</sup><sup>**004**</sup>|**0**_._**845**<sup>_±._</sup><sup>**002**</sup>|**0**_._**906**<sup>_±._</sup><sup>**003**</sup>|**0**_._**029**<sup>_±._</sup><sup>**001**</sup>|1_._366<sup>_±._004</sup>|**0**_._**343**<sup>_±._</sup><sup>**011**</sup>|0_._484<sup>_±._001</sup>|0_._493<sup>_±._002</sup>|


(1) Generative Quality, assessing the fidelity, diversity, and semantic alignment of the generated motions from text prompts; 

(2) Tracking Success Rate in Real-World Deployment, verifying the physical feasibility and robustness of our tracker on hardware. 

## _A. Evaluation of Generation Quality_ 

**Metrics.** We evaluate kinematic reference quality using standard HumanML3D benchmarks via a robot-domain **MoCLIP** evaluator. We further propose two robot-centric metrics: **Motion Safety Score (MSS)** for hardware constraint compliance, and **Root Trajectory Consistency (RTC)** for path-shape fidelity. Full definitions are in Appendix V-A. 

TABLE II 

ABLATION STUDY ON INFERENCE CONFIGURATIONS (SCHEDULER, DENOISING STEPS, AND CFG SCALE). ALL VARIANTS USE THE ECHO-UNET BACKBONE. **BOLD** : BEST RESULT WITHIN EACH GROUP. 

marginally higher RTC, the significant performance gap in semantic and diversity metrics validates the UNet backbone’s advantage in capturing multi-scale temporal structures. 

**Ablation Study.** Table II presents ablations on three inference hyperparameters. _(i) Scheduler_ : DDIM yields the best semantic generation quality, achieving the lowest FID while maintaining competitive R-Precision, MSS, and RTC. _(ii) Denoising Steps_ : Performance largely saturates within 5–10 steps. We adopt 10 steps as the default setting, which preserves strong generation quality while keeping the cloud-to-edge latency at about 1.02 s. _(iii) CFG Scale_ : Lower guidance scales ( _s_ = 1 _._ 0) favor physical compliance, as reflected by higher MSS and RTC, whereas _s_ = 2 _._ 5 provides the strongest semantic alignment, achieving the best R-Precision and FID. Performance degrades at _s_ = 5 _._ 0, so we select _s_ = 2 _._ 5 as the best trade-off between instruction fidelity and physical safety. 

|Variant|R1 _↑_|FID _↓_|MSS _↑_|RTC _↑_|Time (s) _↓_|
|---|---|---|---|---|---|
|**Scheduler**||||||
|DPM-Solver|0.643|0.040|0.466|0.431|1.02|
|DDPM|0.686|0.030|**0.492**|**0.498**|1.02|
|DDIM|**0.686**|**0.029**|0.484|0.493|1.02|
|**Denoising Steps **|**(DDIM)**|||||
|5 steps|**0.697**|0.029|0.481|**0.508**|**0.50**|
|10 steps|0.686|**0.029**|**0.484**|0.493|1.02|
|20 steps|0.691|0.029|0.483|0.480|2.05|
|50 steps|0.690|0.031|0.480|0.466|5.16|
|100 steps|0.685|0.031|0.479|0.458|10.33|
|**CFG Scale (DD**|**IM, 10 st**|**eps)**||||
|CFG = 1.0|0.630|0.039|**0.530**|**0.582**|1.02|
|CFG = 2.5|**0.686**|**0.029**|0.484|0.493|1.02|
|CFG = 5.0|0.663|0.047|0.290|0.378|1.02|
|**ECHO (Ours)**|**0.686**|**0.029**|**0.484**|**0.493**|**1.02**|


We first analyze the quality of the generated reference motions prior to the tracking stage. As shown in Table I, ECHOUNet achieves the best overall performance, outperforming prior baselines in FID (0.029, a 21 _._ 6% improvement over StableMofusion), MM Dist. (0.343), and R-Precision (Top-1: 0.686). Notably, it attains the highest RTC (0.493) among all prior baselines, confirming superior trajectory consistency for downstream tracking. While ECHO-Transformer yields a 

## _B. Real-World Deployment_ 

We conduct real-world experiments across a diverse set of tasks. A trial is counted as a “Success” only if the humanoid completes the instructed behavior without losing balance, falling, or violating joint torque limits during execution. 

Fig. 2 presents a qualitative comparison between the simulated kinematics in MuJoCo and the real-world execution. The evaluated tasks encompass varying degrees of wholebody dynamics, ranging from upper-body gestures (“A man is waving his right hand.”) to highly dynamic lower-body maneuvers and postural transitions (“A man walks forward then squats.”, “A man kicks forward.”). The policy successfully bridges the reality gap; the physical robot closely tracks the simulated reference motions without exhibiting instability, effectively handling the unmodeled real-world dynamics and hardware constraints inherent in agile tasks. 

Quantitative metrics for text-driven command execution are detailed in Table III. For each command, we conducted 20 independent trials, reporting the Success Rate (Succ), Global Mean Per Joint Position Error ( _E_ g-mpjpe), and Local Mean Per Joint Position Error ( _E_ mpjpe). 

TABLE III 

REAL-WORLD TRACKING PERFORMANCE OVER 20 TRIALS. _E_ G-MPJPE AND _E_ MPJPE ARE IN MM; _±_ DENOTES STANDARD DEVIATION. 

|Text Command|Succ _↑_|_E_g-mpjpe (mm) _↓_|_E_mpjpe (mm) _↓_|
|---|---|---|---|
|“punch”|20_/_20|287_._420<sup>_±_50</sup><sup>_._200</sup><br>|32_._274<sup>_±_1</sup><sup>_._764</sup><br>|
|“wave right hand”|20_/_20|89_._681<sup>_±_6</sup><sup>_._345</sup><br>|22_._780<sup>_±_0</sup><sup>_._619</sup><br>|
|“strum guitar with left hand”|20_/_20|72_._392<sup>_±_6</sup><sup>_._687</sup><br>|24_._810<sup>_±_0</sup><sup>_._573</sup><br>|
|“play the violin”|20_/_20|111_._449<sup>_±_20</sup><sup>_._439</sup>|23_._933<sup>_±_1</sup><sup>_._169</sup>|


The framework achieved a 100% success rate across all evaluated commands, corresponding to 80/80 successful trials in total, which demonstrates reliable real-world deployment. The local joint tracking error ( _E_ mpjpe) remains within 22– 33 mm, indicating precise joint-level control. The global tracking error ( _E_ g-mpjpe) is higher for high-momentum motions such as “punch” due to root translation drift, but it remains within acceptable bounds and does not compromise semantic fidelity or physical stability. 

## V. DISCUSSION AND CONCLUSION 

ECHO introduces an edge-cloud architecture for languagedirected humanoid control, bypassing onboard constraints by decoupling diffusion generation from high-frequency RL tracking. Unitree G1 deployments validate that our 38D interface ensures dynamically feasible execution. To address current network and environmental limitations, future work will integrate visual feedback to evolve ECHO into an obstacle-aware Vision-Language-Action (VLA) architecture , ultimately providing a scalable, retargeting-free foundation for agile control. 

## REFERENCES 

- [1] Y. Shao, X. Huang, B. Zhang, Q. Liao, Y. Gao, Y. Chi, Z. Li, S. Shao, and K. Sreenath, “Langwbc: Language-directed humanoid whole-body control via end-to-end learning,” _arXiv preprint arXiv:2504.21738_ , 2025. 

- [2] Y. Wang, H. Jiang, S. Yao, Z. Ding, and Z. Lu, “Sentinel: A fully end-to-end language-action model for humanoid whole body control,” _arXiv preprint arXiv:2511.19236_ , 2025. 

- [3] P. Li, Z. Zhuang, Y. Gao, Y. Dong, S. Li, C. Jiang, S. Dou, Z. Xi, E. Zhou, J. Huang, _et al._ , “From-w1: Towards general humanoid whole-body control with language instructions,” _arXiv preprint arXiv:2601.12799_ , 2026. 

- [4] M. Loper, N. Mahmood, J. Romero, G. Pons-Moll, and M. J. Black, “Smpl: A skinned multi-person linear model,” _ACM Transactions on Graphics (Proc. SIGGRAPH Asia)_ , vol. 34, no. 6, pp. 248:1–248:16, 2015. 

- [5] Z. Li, C. Chi, Y. Wei, B. Zhu, Y. Peng, T. Huang, P. Wang, Z. Wang, S. Zhang, and C. Xu, “From language to locomotion: Retargetingfree humanoid control via motion latent guidance,” _arXiv preprint arXiv:2510.14952_ , 2025. 

- [6] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark, _et al._ , “Learning transferable visual models from natural language supervision,” in _International conference on machine learning_ . PmLR, 2021, pp. 8748–8763. 

- [7] J. Ho, A. Jain, and P. Abbeel, “Denoising diffusion probabilistic models,” _Advances in neural information processing systems_ , vol. 33, pp. 6840– 6851, 2020. 

- [8] J. Ho and T. Salimans, “Classifier-free diffusion guidance,” _arXiv preprint arXiv:2207.12598_ , 2022. 

- [9] J. Song, C. Meng, and S. Ermon, “Denoising diffusion implicit models,” in _International Conference on Learning Representations_ , 2021. 

- [10] C. Guo, S. Zou, X. Zuo, S. Wang, W. Ji, X. Li, and L. Cheng, “Generating diverse and natural 3d human motions from text,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2022, pp. 5152–5161. 

- [11] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black, “Amass: Archive of motion capture as surface shapes,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2019, pp. 5442–5451. 

- [12] L. Pinto, M. Andrychowicz, P. Welinder, W. Zaremba, and P. Abbeel, “Asymmetric actor critic for image-based robot learning,” _arXiv preprint arXiv:1710.06542_ , 2017. 

- [13] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

- [14] A. Amini, W. Schwarting, A. Soleimany, and D. Rus, “Deep evidential regression,” _Advances in neural information processing systems_ , vol. 33, pp. 14 927–14 937, 2020. 

- [15] Y. Zhou, C. Barnes, J. Lu, J. Yang, and H. Li, “On the continuity of rotation representations in neural networks,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2019, pp. 5745–5753. 

- [16] H. Ahn, T. Ha, Y. Choi, H. Yoo, and S. Oh, “Text2action: Generative adversarial synthesis from language to action,” in _2018 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2018, pp. 5915–5920. 

- [17] C. Ahuja and L.-P. Morency, “Language2pose: Natural language grounded pose forecasting,” in _2019 International conference on 3D vision (3DV)_ . IEEE, 2019, pp. 719–728. 

- [18] M. Petrovich, M. J. Black, and G. Varol, “Temos: Generating diverse human motions from textual descriptions,” in _European conference on computer vision_ . Springer, 2022, pp. 480–497. 

- [19] G. Tevet, S. Raab, B. Gordon, Y. Shafir, D. Cohen-Or, and A. H. Bermano, “Human motion diffusion model,” _arXiv preprint arXiv:2209.14916_ , 2022. 

- [20] M. Zhang, Z. Cai, L. Pan, F. Hong, X. Guo, L. Yang, and Z. Liu, “Motiondiffuse: Text-driven human motion generation with diffusion model,” _IEEE transactions on pattern analysis and machine intelligence_ , vol. 46, no. 6, pp. 4115–4128, 2024. 

- [21] X. Chen, B. Jiang, W. Liu, Z. Huang, B. Fu, T. Chen, and G. Yu, “Executing your commands via motion diffusion in latent space,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2023, pp. 18 000–18 010. 

- [22] W. Chen, K. Yu, J. Haozhe, K. Yuan, Z. Huang, B. Tian, S. Lai, H. Xiao, E. Zhang, L. Wang, and Y. Yue, “Ant: Adaptive neural temporal-aware text-to-motion model,” in _Proceedings of the 33rd ACM International Conference on Multimedia_ , ser. MM ’25. ACM, Oct. 2025, pp. 9852–9861. [Online]. Available: http://dx.doi.org/10.1145/3746027.3755168 

- [23] W. Chen, H. Jia, S. Lai, L. Wang, Y. Lin, H. Xiao, L. Hu, and Y. Yue, “Free-t2m: Robust text-to-motion generation for humanoid robots via frequency-domain,” 2025. [Online]. Available: https://arxiv.org/abs/2501.18232 

- [24] W. Chen, H. Li, S. Liang, L. Wang, H. Jia, K. Yuan, J. Wu, B. Tian, and Y. Yue, “Polaris: Projection-orthogonal least squares for robust and adaptive inversion in diffusion models,” 2025. [Online]. Available: https://arxiv.org/abs/2512.00369 

- [25] M. Ning, M. Li, J. Su, H. Jia, L. Liu, M. Benes,ˇ W. Chen, A. A. Salah, and I. O. Ertugrul, “Dctdiff: Intriguing properties of image generative modeling in the dct space,” 2025. [Online]. Available: https://arxiv.org/abs/2412.15032 

- [26] Y. Yuan, J. Song, U. Iqbal, A. Vahdat, and J. Kautz, “Physdiff: Physics-guided human motion diffusion model,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2023, pp. 16 010–16 021. 

- [27] W. Xie, J. Zheng, J. Han, J. Shi, _et al._ , “Textop: Real-time interactive text-driven humanoid robot motion generation and control,” _arXiv preprint arXiv:2602.07439_ , 2026. 

- [28] S. Kuindersma, R. Deits, M. Fallon, A. Valenzuela, H. Dai, F. Permenter, T. Koolen, P. Marion, and R. Tedrake, “Optimization-based locomotion planning, estimation, and control design for the atlas humanoid robot,” _Autonomous robots_ , vol. 40, no. 3, pp. 429–455, 2016. 

- [29] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions On Graphics (TOG)_ , vol. 37, no. 4, pp. 1–14, 2018. 

- [30] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “Amp: Adversarial motion priors for stylized physics-based character control,” _ACM Transactions on Graphics (ToG)_ , vol. 40, no. 4, pp. 1–20, 2021. 

- [31] I. Loshchilov and F. Hutter, “Decoupled weight decay regularization,” in _International Conference on Learning Representations_ , 2019. 

- [32] Q. Lu, Y. Feng, B. Shi, M. Piseno, Z. Bao, and C. K. Liu, “Gentlehumanoid: Learning upper-body compliance for contact-rich human and object interaction,” _arXiv preprint arXiv:2511.04679_ , 2025. 

- [33] J. Schulman, P. Moritz, S. Levine, M. Jordan, and P. Abbeel, “Highdimensional continuous control using generalized advantage estimation,” _arXiv preprint arXiv:1506.02438_ , 2015. 

- [34] N. Rudin, D. Hoeller, P. Reist, and M. Hutter, “Learning to walk in minutes using massively parallel deep reinforcement learning,” in _Conference on robot learning_ . PMLR, 2022, pp. 91–100. 

- [35] Z. Su, X. Huang, D. Ordonez-Apraez,˜ Y. Li, Z. Li, Q. Liao, G. Turrisi, M. Pontil, C. Semini, Y. Wu, _et al._ , “Leveraging symmetry in rlbased legged locomotion control,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 6899–6906. 

- [36] J. Siekmann, Y. Godse, A. Fern, and J. Hurst, “Sim-to-real learning of all common bipedal gaits via periodic reward composition,” in _2021 IEEE international conference on robotics and automation (ICRA)_ . IEEE, 2021, pp. 7309–7315. 

- [37] C. Guo, X. Zuo, S. Wang, and L. Cheng, “Tm2t: Stochastic and tokenized modeling for the reciprocal generation of 3d human motions and texts,” in _European Conference on Computer Vision_ . Springer, 2022, pp. 580–597. 

- [38] Y. Huang, H. Yang, C. Luo, Y. Wang, S. Xu, Z. Zhang, M. Zhang, and J. Peng, “Stablemofusion: Towards robust and efficient diffusionbased motion generation framework,” in _Proceedings of the 32nd ACM International Conference on Multimedia_ , 2024, pp. 224–232. 

- [39] H. Jia, W. Chen, Y. Lin, Y. Yang, L. Wang, M. Ning, B. Tian, S. Lai, N. Jia, Y. Chen, and Y. Yue, “Luma: Low-dimension unified motion alignment with dual-path anchoring for text-to-motion diffusion model,” 2025. [Online]. Available: https://arxiv.org/abs/2509.25304 

- [40] M. Heusel, H. Ramsauer, T. Unterthiner, B. Nessler, and S. Hochreiter, “Gans trained by a two time-scale update rule converge to a local nash equilibrium,” _Advances in neural information processing systems_ , vol. 30, 2017. 

## APPENDIX 

This appendix details the evaluation metrics, reward formulations, domain randomization, and network hyperparameters. 

## _A. Evaluation Metrics_ 

**Feature Extraction (MoCLIP).** Since the standard HumanML3D evaluator [10] is incompatible with our 38D format, we train a dedicated **MoCLIP** [39] model: a 4-layer Transformer motion encoder (768-dim, 8 heads) aligned with a frozen CLIP ViT-L/14 text encoder [6] via contrastive learning on the retargeted HumanML3D corpus. All experiments target the Unitree G1 EDU variant with 29 actuated DoF (hip _×_ 6, knee _×_ 2, ankle _×_ 4, waist _×_ 3, shoulder _×_ 6, elbow _×_ 4, wrist _×_ 4; dexterous hands excluded). 

- **FID [40]:** Frechet´ distance between Gaussians fitted on generated and ground-truth MoCLIP embeddings. Lower is better. 

- **R-Precision:** Top-1/2/3 retrieval accuracy of a generated motion against 32 text candidates in MoCLIP space. Higher is better. 

- **Diversity:** Average pairwise Euclidean distance over 300 randomly sampled motion pairs. 

- **MM. Dist. (Multimodal Distance):** Assesses the semantic alignment between generated motions and corresponding texts. Lower MM Dist. indicates better cross-modal correspondence. 

**Robot-Centric Metrics (Proposed).** We introduce two metrics assessing physical executability, which standard textto-motion benchmarks omit. 

- **Motion Safety Score (MSS):** Measures compliance with Unitree G1 hardware constraints: joint position soft limits (90% of range), velocity ( _±_ 10 rad/s), and acceleration (100 rad/s<sup>2</sup> ). For constraint _k_ , a normalized violation _<u>vk</u> ≥_ 0 is mapped to a sub-score _Sk_ = exp( _−_ 100 _·_ _<u>vk</u>_ ). The per-motion score is: 

   - MSS _i_ = _S_ pos<sup>0</sup><sup>_._5</sup><sup>_·S_</sup> vel<sup>0</sup><sup>_._3</sup><sup>_·S_</sup> acc<sup>0</sup><sup>_._2</sup><sup>_,_</sup> MSS = _N_<sup><u>1</u></sup> � _i_<sup>MSS</sup><sup>_i∈_[0</sup><sup>_,_1]</sup><sup>_._</sup> (7) 

- **Root Trajectory Consistency (RTC):** Measures whether the generated root path matches the ground-truth in shape and travel extent. A Shape Score _S_ shape compares arclength-reparameterized waypoints ( _K_ = 50, _σ_ = 0 _._ 35); an Extent Score _S_ extent compares total arc lengths ( _σ_ = 0 _._ 8): 


## _B. Reward Functions_ 

The detailed weight configurations are presented in Table IV. All regularization terms are computed as penalties and scaled by their absolute weights. 

TABLE IV 

REWARD FUNCTION CONFIGURATIONS 

|**Reward Term**|**Weight**|
|---|---|
|_Motion Tracking_||
|Root Position Tracking|0.5|
|Root Rotation Tracking|0.5|
|Root Lin / Ang Velocity|1.0 / 1.0|
|Keypoint Tracking|1.0|
|Upper / Lower Keypoint Tracking<br>|0.5 / 0.5<br>|
|Joint Position Tracking|1.0|
|Joint Velocity Tracking|0.5|
|_Locomotion Regularizati_|_on_|
|Survival|3.0|
|Feet Air Time Ref|5.0|
|Feet Air Time Dense|1.0<br>|
|Joint Velocity Penalty|5_._0_×_10<sup>_−_4</sup><br>|
|Joint Acceleration Penalty|2_._0_×_10<sup>_−_8</sup>|
|Action Rate Penalty|0.01|
|Joint Position Limits|1.0|
|Joint Torque Limits|0.01|


## _C. Domain Randomization_ 

To facilitate zero-shot sim-to-real transfer, we apply domain randomization to physical parameters (sampled uniformly within bounds) as detailed in Table V. 

TABLE V 

DOMAIN RANDOMIZATION PARAMETERS 

|**Parameter**|**Randomization Range**|
|---|---|
|Pelvis & Torso Mass|[0_._9_×,_1_._1_×_]|
|Pelvis & Torso COM Offset|[_−_0_._02_,_0_._02] m|
|Ankle Static Friction|[0_._5_×,_1_._5_×_]|
|Ankle Solref Time Constant|[0_._015_,_0_._03] s|
|Ankle Solref Damping Ratio|[0_._5_,_2_._0]|
|Joint Offset Error|[_−_0_._01_,_0_._01] rad<br>|
|Motor Stiffness / Damping|[0_._8_×,_1_._2_×_]|
|Motor Armature|[0_._75_×,_1_._25_×_]|


## _D. Network Architecture and Training Setup_ 

**Network Architecture:** The Teacher network encodes privileged information into a 256-dim latent vector using an MLP [512 _,_ 256]. The Student Adaptation Module (MLP: [512 _,_ 512 _,_ 256]) predicts this latent using proprioceptive history. Both Actor and Critic use MLPs [1024 _,_ 512 _,_ 512] with LayerNorm and Mish activations. To encourage proper exploration, initial noise scales are explicitly set based on joint types: 1.5 for hips/knees/waist, 1.2 for shoulders/elbows, and 1.0 for wrists/ankles. Table VI summarizes the hyperparameters. 

TABLE VI 

PPO HYPERPARAMETERS & DETAILS 

|**Parameter**|**Value**|
|---|---|
|Total Training Frames<br>|8_×_10<sup>9</sup><br>|
|PPO Epochs / Minibatches|5 / 8<br>|
|Learning Rate<br>|5_×_10<sup>_−_4</sup><br>|
|Target KL Divergence<br>|0.01<br>|
|Discount Factor (_γ_) / GAE (_λ_)<br>|0.99 / 0.95<br>|
|Clip Range<br>i|0.2<br>|
|Entropy Coefficient<br>|Decays 0.01 _→_0.0025<br>|
|Distillation Weight (_λ_reg)<br>|0.2<br>|
|Action Delay Buffer<br>|3 steps<br>|
|Action Scaling (Upper / Lower)<br>Symmetry Loss|1.0 / 0.5<br>Enabled|


