---
title: "CReF: Cross-modal and Recurrent Fusion for Depth-conditioned Humanoid Locomotion"
date: "2026-03-31"
authors: "Yuan Hao; Ruiqi Yu; Shixin Luo; Guoteng Zhang; Jun Wu; Qiuguo Zhu"
url: https://arxiv.org/abs/2603.29452
pdf: https://arxiv.org/pdf/2603.29452
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.29452)** / [論文ページ](https://arxiv.org/abs/2603.29452)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED JULY, 2026 

1 

# CReF: Cross-modal and Recurrent Fusion for Depth-conditioned Humanoid Locomotion 

Yuan Hao<sup>1</sup> , Ruiqi Yu<sup>1</sup> , Shixin Luo<sup>1</sup> , Guoteng Zhang<sup>2</sup> , Jun Wu<sup>1</sup> and Qiuguo Zhu<sup>_∗_1</sup> 

**_Abstract_ —Stable traversal over geometrically complex terrain increasingly requires exteroceptive perception, yet prior perceptive humanoid locomotion methods often remain tied to explicit geometric abstractions, either by mediating control through robot-centric 2.5D terrain representations or by shaping depth learning with auxiliary geometry-related targets. While effective, these approaches introduce additional map-construction procedures or multi-stage skill-transfer processes beyond direct depth-to-control learning. We propose CReF (Cross-modal and Recurrent Fusion), a single-stage depth-conditioned humanoid locomotion framework that learns locomotion-relevant features directly from raw forward-facing depth without explicit geometric intermediates. CReF couples proprioception and depth tokens through proprioception-queried cross-modal attention, fuses the resulting representation with a gated residual fusion block, and performs temporal integration with a Gated Recurrent Unit (GRU) regulated by a highway-style output gate for statedependent blending of recurrent and feedforward features. To further improve terrain interaction, we introduce a terrain-aware foothold placement reward that extracts supportable foothold candidates from foot-end point-cloud samples and rewards touchdown locations that lie close to the nearest supportable candidate. Experiments in simulation and on a physical humanoid demonstrate robust traversal over diverse terrains and effective zeroshot transfer to real-world scenes containing handrails, hollow pallet assemblies, severe reflective interference, and visually cluttered outdoor surroundings.** 

**_Index Terms_ —Legged robots, Reinforcement learning, Deep learning for visual perception.** 


Fig. 1. Our CReF framework enables robust real-world humanoid locomotion, including more than 20 consecutive stair traversals, a 40 cm high platform, an 80 cm gap, and real-world stairs with a 20 cm rise and 26 cm tread, while generalizing robustly beyond the training terrains. 

## I. INTRODUCTION 

**H** UMANOID robots promise versatile mobility in human-centered environments. Deep reinforcement learning has enabled agile locomotion across diverse platforms and surface conditions, and proprioception-dominant policies can already achieve strong standing and walking performance through reactive stabilization [1]–[4]. However, perceptive locomotion becomes essential when safe traversal depends on anticipating terrain geometry before contact. This is especially critical on stairs, particularly during descent, and near gaps or abrupt 

Manuscript received: April 22, 2026; Revised June 13, 2026; Accepted July 26, 2026. 

This paper was recommended for publication by Editor Olivier Stasse upon evaluation of the Associate Editor and Reviewers comments. This work was supported by the “Leading Goose” R&D Program of Zhejiang (Grant No. 2023C01177), the National Key R&D Program of China (Grant No. 2022YFB4701502), and the 2035 Key Technological Innovation Program of Ningbo City (Grant No. 2024Z300). 

> 1The authors are with Institute of Cyber-Systems and Control, Zhejiang University, Hangzhou 310027, China. 

> 2Guoteng Zhang is with the School of Control Science and Engineering, Shandong University, Jinan 250061, China. 

> _∗_ Corresponding author: Qiuguo Zhu (qgzhu@zju.edu.cn). Project website: https://cometlogic.github.io/cref/. 

> Digital Object Identifier (DOI): see top of this page. 

height transitions, where foothold errors can lead to edge contacts or slipping [5], [6]. 

A widely adopted way to incorporate exteroception into legged locomotion is to construct a robot-centric 2.5D terrain representation for foothold selection, predictive control, or policy conditioning [7]–[11]. Hybrid planner-guided methods and attention-based map encoders further extend this paradigm by providing structured references or emphasizing future steppable regions [12], [13]. This line of work is attractive because elevation maps offer a compact, interpretable perceptioncontrol interface. However, point-cloud data must first be projected, fused, filtered, and maintained in a consistent frame before being used for downstream planning and control. This process often involves smoothing, inpainting, segmentation, terrain classification, or drift compensation. [8], [14]. Forwardfacing depth provides an egocentric geometric signal directly from the onboard camera, reducing reliance on a separate terrain-map construction pipeline. 

A further line of work uses depth as the exteroceptive input, but often shapes depth learning with auxiliary targets [15], [16] because forward facing depth provides look ahead cues 

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED JULY, 2026 

2 

without directly observing the instantaneous underfoot region [17], [18]. Rather than letting the locomotion objective alone organize the visual representation, these methods regularize the depth branch through terrain reconstruction [6], [19], [20], decoder-constrained latent estimation [21], or transfer from privileged teachers [22]. This strategy is attractive because geometry-related targets provide structured guidance that can ease optimization and improve transfer. However, it also changes how depth features are learned. The encoder is encouraged to preserve information supporting the chosen auxiliary target, making the representation partly dependent on the target design and fidelity rather than solely on the locomotion objective. A more direct and simpler formulation is to learn locomotion-relevant structure from depth without explicit terrain reconstruction or privileged geometric targets. Recent humanoid work has begun to pursue this route by training end-to-end policies that consume raw depth and proprioception directly, using temporal depth history to mitigate partial observability and improve traversal over challenging terrain and obstacle sequences [23]. In parallel, recent perceptive humanoid pipelines have reduced the depth sensing sim-to-real gap through transfer-oriented training and realistic sensor simulation [23], [24]. These methods are effective, but simulated artifacts may not fully capture real sensor failures. We therefore examine whether a depth-conditioned policy can maintain stable locomotion under real sensing artifacts without precise depth-noise modeling during training. 

In this work, we propose CReF, a perceptive humanoid locomotion policy that directly maps proprioception and raw forward-facing depth to joint position targets without explicit geometric intermediates or multi-stage supervision. This design explores whether a single-stage policy can learn locomotion-relevant structure directly from raw depth and achieve or even exceed the performance of geometry-guided methods. CReF combines cross-modal attention, gated residual fusion, and recurrent fusion to extract depth features and modulate temporal memory based on the locomotion state. We further introduce a terrain-aware foothold placement reward that extracts supportable foothold candidates from local footend point-cloud samples and shapes touchdown toward them. Unlike purely prohibitive do-not-step constraints [10], [22], it encourages landing near supportable regions and thus provides more directional supervision for contact placement. CReF transfers zero-shot to real hardware and remains effective in challenging real-world scenes. 

This work makes the following contributions: 

- A single-stage depth-conditioned humanoid locomotion framework that organizes raw forward-facing depth and proprioception into locomotion-relevant multimodal and temporal representations, enabling robust terrain traversal without explicit geometric intermediates or multi-stage supervision. 

- A terrain-aware foothold placement reward that extracts supportable foothold candidates from local foot-end point-cloud samples and guides touchdown during terrain transitions, yielding substantial gains in long-duration stair traversal, especially in descent. 

- Real-world zero-shot deployment of a single depth- 

conditioned humanoid locomotion policy across multiple terrain-transition tasks and broader unseen environments, demonstrating robust transfer beyond simulation. 


## _A. Overview_ 

CReF is a single-stage depth-conditioned humanoid locomotion framework that maps onboard proprioception and forward-facing depth directly to joint position targets. It comprises an onboard actor, an asymmetric critic with privileged training signals, and a lightweight velocity estimator. The architecture is shown in Fig. 2, and training is performed with PPO [25]. 

_1) Policy Network:_ At each control step _t_ , the policy network takes the current proprioceptive observation **o**<sup>_p_</sup> _t_<sup>and</sup> the current forward-facing depth image **D** _t ∈_ R<sup>_H×W_</sup> as input: 


Following standard legged locomotion pipelines, the proprioceptive observation is defined as 


where **_ω_** _t_ is the base angular velocity, **r**<sup>grav</sup> _t_ is the gravity direction expressed in the body frame, **u**<sup>cmd</sup> _t_ is the commanded motion, **q** _t_ and **q** ˙ _t_ are the joint positions and velocities, **q** 0 is the nominal standing pose, and **a** _t−_ 1 is the previous action. 

_2) Value Network:_ To obtain a more accurate estimate of the state value, the value network is trained asymmetrically with privileged information available only in simulation. In addition to the proprioceptive observation **o**<sup>_p_</sup> _t_<sup>, its input includes</sup> the ground-truth base linear velocity **v** _t_ and a robot-centric terrain height observation **m** _t_ , which is defined as local elevation samples around the robot. The value-network input is 


_3) Action space:_ The policy outputs an action **a** _t ∈_ R<sup>_na_</sup> that parameterizes joint position targets tracked by a low-level PD controller. We adopt a residual parameterization around the nominal standing pose **q** 0: 


where **q** 0 is the nominal standing pose and **q**<sup>target</sup> _t_ is the commanded joint position vector. 

_4) Reward function:_ Following recent analyses on robust humanoid reward design [3], [26], we adopt a low-speed-aware linear-velocity tracking term and a contact-shaping term that rewards standing while encouraging short-horizon single-foot contact during locomotion. The reward terms used in training are listed in Table I. 

Here, **e** _v_ = **u**<sup>cmd</sup> _xy_<sup>_−_</sup><sup>**v**</sup><sup>_xy_is the planar velocity tracking error,</sup> and I _s_ = I( _∥_ **u**<sup>cmd</sup> _xy_<sup>_∥_2</sup><sup>_<vs_)switchestothelow-speedform</sup> when the commanded planar speed is below _vs_ . The standing indicator is defined as Istand = I( _∥_ **u**<sup>cmd</sup> _∥_ 2 _< us_ ). I<sup>0</sup> single<sup>_._2sis</sup> equal to 1 if a single-foot contact has occurred within the last 

HAO _et al._ : CREF: CROSS-MODAL AND RECURRENT FUSION FOR DEPTH-CONDITIONED HUMANOID LOCOMOTION 

3 


Fig. 2. Overview of CReF. The proposed single-stage depth-conditioned policy combines cross-modal attention, gated residual fusion, recurrent fusion, and a terrain-aware foothold placement reward for robust terrain locomotion. 

TABLE I 

REWARD TERMS USED IN TRAINING. 

|Term|Expression (_ri_)|_wi_|
|---|---|---|
|Lin. vel. tracking|exp<br>�<br>_−_<br>I_s∥_**e**_v∥_1+(1_−_I_s_)_∥_**e**_v∥_<sup>2</sup><br>2<br>_σv_<br>�<br><br>|2_._5|
|Ang. vel. tracking|exp<br>�<br>_−_(_ωz −ω_<sup>cmd</sup><br>_z_<br>)<sup>2</sup>_/σω_<br>�<br><br>|1_._5|
|Orientation|exp<br>�<br>_−_10_∥_**r**<sup>grav</sup><br>_xy_<br>_∥_2<br>�|1_._0|
|Feet contact|Istand + (1_−_Istand)I<sup>0</sup><sup>_._2s</sup><br>single<br><br>|1_._5|
|Feet _y_ distance|exp<br>�<br>_−_10_|d_<sup>feet</sup><br>_y_<br>_−_0_._27_|_<br>�|0_._1|
|Foothold placement|Eq. (23)<br><br>|2_._0|
|Base height|exp<br>�<br>_−_10_|_(_z_<sup>base</sup> _−_¯_z_<sup>supp</sup>)_−_0_._55_|_<br>�|0_._8|
|Lin. vel. _z_|_v_<sup>2</sup><br>_z_<br>|_−_1_._0|
|Ang. vel. _xy_|_∥_**_ω_**_xy∥_<sup>2</sup><br>|_−_0_._05<br>|
|Joint velocity|_∥_˙**q**_∥_<sup>2</sup><br>|_−_10<sup>_−_3</sup>|
|Action rate|_∥_**a**_t −_**a**_t−_1_∥_<sup>2</sup><br>|_−_0_._01|
|Action smoothness|_∥_**a**_t −_2**a**_t−_1 +**a**_t−_2_∥_<sup>2</sup><br><br><br><br>|_−_0_._01|
|Feet air time|�<br>_f_ <sup>I</sup><sup>_f_</sup><br>first<br>�<br>0_._5_−T _<sup>_f_</sup><br>air<br>�<br><br>|_−_2_._5|
|Foot slip|�<br>_f_ <sup>I</sup><br>�<br>_∥_**F**<sup>_f _</sup>_∥>_ 5<br>�<br>_∥_**v**<sup>_f_</sup><br>_xyz_<sup>_∥_</sup><br>|_−_0_._2|
|Foot impact acc.|�<br>_f_<br>�<br>_|_˙_v_<sup>_f_</sup><br>_z _<sup>_| −a_0</sup><br>�<br>+<br>|_−_0_._5|
|Foot impact vel.|�<br>_f_<br>�<br>_|v_<sup>_f_</sup><br>_z _<sup>_| −v_0</sup><br>�<br>+<br><br>|_−_1_._5|
|DoF position limits|�<br>_j_<br>��<br>_q_<sup>min</sup><br>_j_<br>_−qj_<br>�<br>+ <sup>+</sup><br>�<br>_qj −q_<sup>max</sup><br>_j_<br>�<br>+<br>�|_−_10|
|DoF velocity limits|�<br>_j_<br>�<br>_|_˙_qj| −_˙_q_<sup>max</sup><br>_j_<br>�<br>+|_−_0_._6|
|Hip pos|�<br>_j∈J_hip x_/_z<sup>(</sup><sup>_qj −q_0</sup><br>_j_ <sup>)2</sup>|_−_7|
|Ankle pos|�<br>_j∈J_ank x<sup>(</sup><sup>_qj −q_0</sup><br>_j_ <sup>)2</sup><br><br>|_−_10|
|Stumble|I<br>�<br>_∃f_ : _∥_**F**<sup>_f_</sup><br>_xy_<sup>_∥>_ 5</sup><sup>_|F f_</sup><br>_z _<sup>_|_</sup><br>�|_−_10|


0.2 s, and 0 otherwise. We use **r**<sup>grav</sup> _xy_ for the _xy_ component of the projected gravity direction, and 


for the average height of supporting feet. 

In Table I, the superscript _f_ indexes feet. Accordingly, **F**<sup>_f_</sup> and **v**<sup>_f_</sup> denote the contact force and velocity of foot _f_ , while 

_Fz_<sup>_f_and</sup><sup>**F**</sup><sup>_f_</sup> _xy_<sup>denoteitsnormalandtangentialcontact-force</sup> components. I<sup>_f_</sup> first<sup>indicatesthefirstcontacteventoffoot</sup><sup>_f_</sup> after an aerial phase, and _T_ air<sup>_f_isthecorrespondingairtime.</sup> We use [ _x_ ]+ = max( _x,_ 0) for the positive-part operator, and _qj_<sup>0denotesthe</sup><sup>_j_-thcomponentofthestandingpose</sup><sup>**q**0.</sup> 

## _B. Policy Architecture_ 

The policy is designed to extract state-relevant terrain features from forward-facing depth observations and to adaptively control the contribution of temporal memory according to the current locomotion state. In what follows, we refer to the fusion block after cross-modal attention as gated residual fusion (GRF), and to the temporal module as recurrent fusion, which consists of GRU-based temporal integration followed by a highway output gate. The architectural components are detailed in the following subsections. 

_1) Depth encoding and velocity estimation:_ The raw depth image is normalized as **D** _t_ = **D**<sup>raw</sup> _t /d_ max _−_ 0 _._ 5, where _d_ max is the preset maximum depth range. Then the normalized depth image is encoded by a lightweight CNN-based depth tokenizer _Tθ_ ( _·_ ) into a set of local depth tokens, 


where _N_ is the number of tokens and _d_ is the token dimension. These depth tokens are used by the policy for subsequent cross-modal attention. 

To facilitate velocity-command tracking, we jointly train an auxiliary base-velocity estimator, 


where _Cψ_ ( _·_ ) is a lightweight depth compression module. The estimator is supervised by the simulator ground-truth base linear velocity using an _ℓ_ 2 loss. 

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED JULY, 2026 

4 

_2) Cross-modal attention for proprioception-conditioned depth feature extraction:_ The proprioceptive tokenizer takes the concatenation of proprioception and the estimated base linear velocity as input: 


where _Pϕ_ ( _·_ ) denotes the proprioceptive tokenizer and **E** _t_<sup>_d_is</sup> the normalized depth-token set. 

Cross-modal attention then uses the proprioceptive token as the query and the depth tokens as the keys and values: 


where **Q** _t ∈_ R<sup>1</sup><sup>_×d_</sup> and **K** _t,_ **V** _t ∈_ R<sup>_N×d_</sup> . Multi-head attention (MHA) then aggregates locomotion-relevant information from the depth tokens conditioned on the current proprioceptive state. The resulting attention output is 


which is concatenated with the proprioceptive token to form the fusion input, 


_3) Gated residual fusion and recurrent fusion:_ Given the fusion input **x** _t_ , the GRF first computes 


where _ϕ_ ( _·_ ) is ELU. This projection mixes the proprioceptive and depth-conditioned features in a shared latent space while keeping the block lightweight. 

A second linear layer then produces a content branch and a gate branch, 


and the fusion output is 


Here, **c** _t_ provides a candidate residual update, while _σ_ ( **g** _t_ ) adaptively controls its channel-wise contribution. This design allows the policy to emphasize informative multimodal corrections while preserving a direct residual path for stable optimization. 

Within recurrent fusion, **f** _t_ is first processed by a GRU for temporal integration, 


where **z**<sup>rec</sup> _t ∈_ R<sup>2</sup><sup>_d_</sup> is the recurrent feature. The GRU aggregates short-horizon temporal context, which is important when a single depth frame is insufficient to disambiguate terrain structure or contact timing. 

The recurrent feature is then combined with the current fused feature through a highway output gate, 


This gate enables state-dependent fusion between instantaneous multimodal evidence and recurrent memory, so that the policy can rely more on temporal features in ambiguous or 

risky phases while retaining stronger feedforward responses when current observations are already sufficient. The final action is produced by an MLP head from **y** _t_ . 

## _C. Terrain-Aware Foothold Placement Reward_ 

We introduce a terrain-aware foothold placement reward to shape foot placement at touchdown. For each foot, we maintain a compact local point buffer of 60 _×_ 5 foot-frame samples. At each update, command-conditioned forward gating removes near-foot points, where the minimum retained forward distance is set by the commanded step extent and taken as the distance covered in 0.5 s under the current forward command. The remaining points are partitioned into overlapping candidate windows of size 24 _cm ×_ 10 _cm_ with a stride of 4 _cm_ . To reduce computation and chattering, candidates are updated only at liftoff and fixed until touchdown. 

_n_<sup>_f_</sup> Let _Pt,k_<sup>_f_=</sup><sup>_{_</sup><sup>**p**</sup><sup>_f_</sup> _t,k,i_<sup>_}_</sup> _i_ =1 _t,k_<sup>denotethe</sup><sup>_k_-thcandidatewindow</sup> for foot _f_ at time _t_ , where _n_<sup>_f_</sup> _t,k_<sup>isthenumberofpointsin</sup> that window. For each window, we compute the mean and covariance, 


We then perform eigen-decomposition, 

Σ<sup>_f_</sup> _t,k_<sup>_v_</sup> _t,k,j_<sup>_f_=</sup><sup>_λf_</sup> _t,k,j_<sup>_v_</sup> _t,k,j_<sup>_f,_</sup> _λ_<sup>_f_</sup> _t,k,_ 1<sup>_≤λf_</sup> _t,k,_ 2<sup>_≤λf_</sup> _t,k,_ 3<sup>_._</sup> (18) 

and define the roughness as 


A window is accepted as a foothold candidate if it is sufficiently planar, approximately horizontal, and not recessed: 

_ρ_<sup>_f_</sup> _t,k_<sup>_< r_th</sup><sup>_,_</sup> _|vt,k,_<sup>_f_</sup> 1 _,z_<sup>_| > η_th</sup><sup>_,_</sup> _µ_<sup>_f_</sup> _t,k,z_<sup>_> h_min</sup><sup>_,_</sup> (20) 

For each accepted window, the candidate foothold is set to its mean, 


To avoid chattering, the candidate set is refreshed only at liftoff and then held fixed until the next touchdown. At touchdown, we compute the nearest planar distance in the _x_ - _z_ plane between the realized contact position and the candidate set, 


and define the reward as 


where _I_ td<sup>_f_indicatesatouchdowneventand</sup><sup>_sxz_isatolerance</sup> scale. Although computed at touchdown, this term provides an anticipatory shaping objective by encouraging the swing foot to approach locally supportable regions before contact. 

5 

HAO _et al._ : CREF: CROSS-MODAL AND RECURRENT FUSION FOR DEPTH-CONDITIONED HUMANOID LOCOMOTION 

## _D. Training Details_ 

CReF is trained in Isaac Gym with 4096 parallel environments at a control frequency of 50 Hz. The depth stream is rendered at 64 _×_ 48 resolution and updated at 20 Hz. The terrain-aware foothold placement reward adds a small training overhead. It increases the wall clock time by approximately 0.5 s per iteration. The full CReF policy still completes training within about 30 hours for 20,000 iterations on a single RTX 4090. 

To support large-batch training, depth rendering is implemented with NVIDIA Warp [27]. Robot links are approximated as capsules, and self-occlusion is computed on the GPU via first-hit ray-capsule intersection. No synthetic depth corruption is injected during training. 

## III. EXPERIMENTS 

We evaluate CReF in simulation and on hardware. The simulation experiments examine three questions: (i) whether the proposed framework improves terrain traversal performance relative to ablated variants and a perceptive locomotion baseline, (ii) whether the foothold placement reward improves stair contact placement, and (iii) how the highway gate recruits recurrent features under different traversal conditions. We then assess zero-shot real-world transfer and out-of-distribution robustness on a physical humanoid robot. 

## _A. Experimental Setup_ 

Our deployment platform is an AGIBOT X2 Ultra humanoid [28], which is approximately 1.31 m tall, weighs 39 kg. We choose Humanoid Parkour Learning (HPL) [22] as the main external baseline because it is a representative teacher-student perceptive parkour framework that learns a deployable depth-based policy under guidance from privileged terrain information, providing a paradigm-level comparison to our single-stage raw-depth design. Since HPL was originally developed for the Unitree H1 [29], we re-implement it on the AGIBOT X2 Ultra in simulation to ensure hardware-controlled comparison. 

For onboard sensing and inference, the robot uses a forwardfacing Intel RealSense D435i mounted with a downward pitch of 50<sup>_◦_</sup> relative to the horizontal plane, together with an NVIDIA Jetson AGX Orin for onboard policy inference. The policy is transferred zero-shot from simulation, without taskspecific fine-tuning. Using the hardware timestamps provided by the RealSense, we fit a linear regression to map camera time to system time and select the depth frame with an effective latency of 20 ms. 

We compare the following policy variants, all trained from scratch under matched reward, optimization, and terrain settings: 

- **Full CReF** : cross-modal attention + gated residual fusion (GRF) + recurrent fusion. 

- **w/o Cross-Attn** : removes cross-modal attention while preserving the remaining architecture. 

- **w/o GRF** : replaces gated residual fusion with a residual MLP block of matched depth and width. 


Fig. 3. Simulation terrains used in the experiments. The upper panel shows representative terrains used during training. The lower panel presents additional MuJoCo out-of-distribution terrains for cross-simulator evaluation, including terrains with perforated or hollow foothold surfaces that induce depth-distribution shift through missing or discontinuous support geometry, as well as scenes containing lateral heterogeneous structures (e.g., trailer handrails) that introduce cluttered side geometry absent from training. 

- **w/o Highway Gate** : removes the highway output gate from recurrent fusion and decodes actions directly from the GRU feature. 

- **HPL** : a perceptive locomotion baseline trained and evaluated under the same terrain protocol. 

For architectural comparison, each policy is evaluated in 2000 parallel environments for up to 40 s, with forward commands randomly sampled from 0.4–0.8 m/s. Failure is defined as becoming unable to recover to normal walking. For stair foot-placement analysis, we use 2048 parallel stair rollouts. For highway-gate analysis, we log gate statistics from 4096 parallel environments under a fixed forward command. MuJoCo [30] is used only for an additional out-of-distribution evaluation in the architectural comparison. Fig. 3 shows the simulated training terrains together with the out-of-distribution evaluation terrains. 

For the foothold-objective comparison, we replace the foothold placement reward in Eq. (23) with a foot contact quality reward (FCQR) following BeamDojo [10], and also evaluate a no-foothold-reward variant (NoFR), while keeping the remaining training settings unchanged. 

## _B. Simulation Experiments_ 

This subsection reports the simulation results of CReF. We focus on architectural comparison, stair foothold distribution analysis, and highway-gate behavior analysis. 

_1) Architectural Comparison:_ Table II summarizes the architectural comparison. For the trained terrain categories, the stair entries are indexed by riser height and tread depth, while the gap and platform entries are indexed by gap width and platform height, all in centimeters. For stairs, gap, and platform, the OOD columns denote difficulty levels outside the training range. In the additional MuJoCo OOD evaluation, the values in parentheses denote the numbers of successful terrains out of 20 test terrains. The Overall score is computed from the stair, gap, and platform success rates only, excluding MuJoCo. Full CReF achieves the best overall performance 

6 

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED JULY, 2026 

TABLE II 

ARCHITECTURAL COMPARISON OF TERRAIN TRAVERSAL SUCCESS RATES (%). 

|Method|Easy<br>(10/30 cm)|Stairs<br>Medium<br>(15/30 cm)|, SR<br>Hard<br>(20/30 cm)|OOD<br>(23/30 cm)|Easy<br>(30 cm)|Gap, <br>Medium<br>(50 cm)|SR<br>Hard<br>(75 cm)|OOD<br>(80 cm)|Easy<br>(20 cm)|Platfor<br>Medium<br>(30 cm)|m, SR<br>Hard<br>(40 cm)|OOD<br>(43 cm)|MuJoCo<br>OOD|Overall<br>(w/o MuJoCo)|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Full CReF|**99.85**|**99.75**|**97.25**|**73.45**|**99.30**|**98.35**|**92.15**|**44.70**|**99.65**|**99.35**|**97.35**|**84.35**|100(_20_/20)|**90.45**|
|w/o Cross-Attn|96.25|87.50|78.70|34.00|97.10|97.70|83.00|8.60|99.40|98.75|96.90|64.80|95(_19_/20)|78.56|
|w/o GRF|99.60|93.40|83.60|49.10|98.00|98.25|90.05|29.95|99.45|99.15|96.20|68.55|95(_19_/20)|83.78|
|w/o Highway Gate|97.65|98.40|93.65|50.20|98.50|96.90|86.35|17.20|98.45|97.65|91.45|73.10|100(_20_/20)|83.29|
|HPL|95.45|81.45|71.05|27.40|97.45|94.40|78.25|20.85|98.05|92.65|81.80|55.15|5(_1_/20)|74.57|


TABLE III STAIR FAILURES IN ASCENT AND DESCENT. 

|Method|E|asy|Me|dium|H|ard|O|OD|
|---|---|---|---|---|---|---|---|---|
||Up|Down|Up|Down|Up|Down|Up|Down|
|Full CReF|1|**2**|**2**|**3**|**3**|**52**|**93**|**438**|
|w/o Cross-Attn|**0**|75|47|203|88|338|496|824|
|w/o GRF|2|6|25|107|39|289|128|890|
|w/o Highway Gate|13|34|3|29|39|88|293|703|
|HPL|29|62|136|235|241|338|493|959|


and consistently outperforms the ablated variants and the perceptive baseline HPL, with larger advantages on harder and out-of-distribution terrains, including the additional MuJoCo evaluation. These results demonstrate improved robustness and generalization. 

Among the ablations, removing cross-modal attention causes the largest degradation, especially on hard and out-of-distribution terrains, indicating that proprioceptionconditioned depth querying is crucial for extracting terrainscale cues for adaptive traversal. Without it, the policy tends to fall back to an average-terrain locomotion pattern, with less adaptive foot clearance and weaker generalization beyond the training range, which also explains the noticeable drop even on easy descending stairs. The particularly low success rate on the OOD gap terrain is mainly due to the evaluation protocol: large-gap traversal requires high actuation, but success rate is averaged over a range of commanded speeds, so lowcommand cases fail disproportionately and pull down the aggregate result. By comparison, removing GRF or the highway gate causes a milder but consistent decline, mainly on more challenging terrains, indicating that these modules improve the stability of multimodal fusion and temporal feature usage under demanding traversal conditions. For the HPL baseline, depth features are learned under privileged terrain guidance, making severe depth-distribution shifts more likely to generate unreliable geometry-related cues. CReF instead keeps control in a raw-depth feature space with recurrent temporal integration, which can help recent observations complement incomplete or irregular current depth frames. 

Table III further analyzes the failed stair trials from the same 2000 environment evaluation rollouts used for Table II. Across all methods, descending failures increase much more rapidly than ascending failures as stair difficulty rises, indicating that stair descent is the more challenging regime. Full CReF 


Fig. 4. Stair foothold distribution comparison between the proposed foothold placement reward and the FCQR baseline. The proposed reward produces more concentrated and repeatable touchdown distributions in both ascent and descent, reduces touchdown deviation within the stair tread, and eliminates the logged ankle-riser collisions in ascending rollouts. 

consistently yields the fewest descending failures, especially on hard and OOD stairs, which is consistent with improved anticipatory foothold selection and temporal integration. 

_2) Stair Foothold Distribution Analysis:_ Fig. 4 compares the stair touchdown distributions produced by the foothold placement reward, FCQR, and NoFR. The distributions are computed from converged rollouts on the hard stair setting, by pooling touchdown samples from both feet across all evaluated environments. The reported touchdown positions are the projected contact points of the foot-end geometric centers at touchdown. The proposed reward yields the tightest and most repeatable contact placement in both ascent and descent. On ascending stairs, it achieves the highest concentration and eliminates logged ankle-riser collisions. On descending stairs, it reduces the median absolute deviation from 2.8 cm (FCQR) and 9.8 cm (NoFR) to 1.4 cm. 

HAO _et al._ : CREF: CROSS-MODAL AND RECURRENT FUSION FOR DEPTH-CONDITIONED HUMANOID LOCOMOTION 

7 


Fig. 5. Representative real-world rollouts of CReF across multiple terrains and deployment scenes. The figure includes stair traversal with side railings, entrance-step and platform-like transitions, outdoor pathways, and other real-world terrain configurations. Red boxes highlight examples where environmental factors introduce out-of-distribution depth observations, such as large invalid regions in the sensed depth image. 


Fig. 6. Highway gate behavior under different traversal conditions. Higher gate values indicate stronger reliance on recurrent features. 

The improvement is not merely a shift of the touchdown mean. Instead, the entire distribution becomes more concentrated, indicating that the reward improves contact precision and repeatability. This is consistent with its design: although computed at touchdown, it provides an anticipatory shaping objective toward locally supportable regions, rather than only discouraging unfavorable contacts after they occur. 

_3) Highway Gate Behavior Analysis:_ Fig. 6 analyzes the learned highway gate, where larger values indicate stronger reliance on recurrent features. For analysis, gate values are averaged over channels and then aggregated within each 

TABLE IV 

INDOOR REAL-WORLD TRAVERSAL RESULTS. 

|Task|Setting|Success / Trials|
|---|---|---|
|Stairs|Indoor, 15 cm / 30 cm|20/20|
|Platform|Indoor, 40 cm|20/20|
|Gap|Indoor, 80 cm|18/20|
|OOD terrain|Indoor OOD scene|19/20|


state group. We define _risky_ states as timesteps satisfying _|_ roll _| >_ 0 _._ 20 rad or _|_ pitch _| >_ 0 _._ 20 rad, and treat the remaining timesteps as _stable_ states. Flight phases are identified from the foot-contact pattern. Across terrain types, the gate dynamically takes higher values on step-like terrains than on flat terrain over continuous rollout trajectories, showing that the policy recruits temporal memory more strongly when precise terrain anticipation is required. Across contact phases, gate values are higher during flight than during stable support. Across posture states, risky states consistently induce larger gate activation than stable states. 

These trends are consistent with the intended function of the highway gate: recurrent features are emphasized when instantaneous observations are less sufficient for reliable control, and attenuated when feedforward perception is adequate. 

## _C. Real-World Experiments_ 

Real-world experiments validate zero-shot transfer of CReF to a humanoid robot across stair traversal, platform ascent, gap crossing, and diverse indoor and outdoor scenes. The indoor OOD scene follows the MuJoCo OOD setting and includes hollow pallet-like structures and side clutter, as shown in the middle row of Fig. 1. Table IV reports representative indoor quantitative evaluations, where each task is assessed over 20 trials. For stairs, one trial consists of a complete ascent-descent traversal on indoor stairs with 15 cm rise and 30 cm tread. On 

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED JULY, 2026 

8 

the AGIBOT X2 Ultra, CReF achieves strong performance across these standardized indoor tasks, including successful traversal of a 40 cm platform and an 80 cm gap. Beyond these evaluations, CReF further demonstrates stable deployment in broader real-world environments. 

Fig. 5 shows representative real-world rollouts. The policy stably climbs real stairs with side railings at a rise of 20 cm and a tread of 26 cm, even under changing illumination. It also maintains stable locomotion under severe depth degradation, including large invalid depth holes caused by strong reflection, and in outdoor scenes with dense vegetation, asymmetric boundaries, and other non-traversable structures that induce substantial depth out-of-distribution effects. These results suggest that CReF can still exploit useful cues under degraded visual input, although such artifacts may still affect traversal behavior. 

## IV. CONCLUSIONS 

This paper presents CReF, which maps proprioception and forward-facing depth directly to joint position targets without explicit geometric intermediates. By combining cross-modal attention, gated residual fusion, recurrent fusion, and a terrainaware foothold placement reward, CReF improves terrain anticipation and foot placement consistency, with clear gains on stair traversal. Experiments in simulation and on hardware demonstrate strong terrain-traversal performance and zero-shot transfer to challenging real-world scenes. 

At the same time, certain limitations still exist. Depth alone does not preserve appearance and texture cues that may improve perceptual robustness. A natural direction for future work is therefore to investigate binocular RGB-based sensing, which can jointly provide depth structure and texture information for richer scene representations and stronger adaptability across diverse real-world environments. 

## REFERENCES 

- [1] J. Hwangbo, J. Lee, A. Dosovitskiy, D. Bellicoso, V. Tsounis, V. Koltun, and M. Hutter, “Learning agile and dynamic motor skills for legged robots,” _Science Robotics_ , vol. 4, no. 26, p. eaau5872, 2019. 

- [2] S. Choi, G. Ji, J. Park, H. Kim, J. Mun, J. H. Lee, and J. Hwangbo, “Learning quadrupedal locomotion on deformable terrain,” _Science Robotics_ , vol. 8, no. 74, p. eade2256, 2023. 

- [3] B. van Marum, A. Shrestha, H. Duan, P. Dugar, J. Dao, and A. Fern, “Revisiting reward design and evaluation for robust humanoid standing and walking,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 11 256–11 263. 

- [4] C. Zhang, N. Rudin, D. Hoeller, and M. Hutter, “Learning agile locomotion on risky terrains,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 11 864–11 871. 

- [5] J. Long, J. Ren, M. Shi, Z. Wang, T. Huang, P. Luo, and J. Pang, “Learning Humanoid Locomotion with Perceptive Internal Model,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 9997–10 003. 

   - [9] T. Miki, J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter, “Learning robust perceptive locomotion for quadrupedal robots in the wild,” _Science Robotics_ , vol. 7, no. 62, p. eabk2822, 2022. 

   - [10] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang, “BeamDojo: Learning Agile Humanoid Locomotion on Sparse Footholds,” in _Robotics: Science and Systems (RSS)_ , 2025. 

   - [11] M. Dai, W. D. Compton, J. Li, L. Yang, and A. D. Ames, “Walk the PLANC: Physics-Guided RL for Agile Humanoid Locomotion on Constrained Footholds,” _arXiv preprint arXiv:2601.06286_ , 2026. 

   - [12] F. Jenelten, J. He, F. Farshidian, and M. Hutter, “DTC: Deep tracking control,” _Science Robotics_ , vol. 9, no. 86, p. eadh5401, 2024. 

   - [13] J. He, C. Zhang, F. Jenelten, R. Grandia, M. B¨acher, and M. Hutter, “Attention-based map encoding for learning generalized legged locomotion,” _Science Robotics_ , vol. 10, no. 105, p. eadv3604, 2025. 

   - [14] T. Miki, L. Wellhausen, R. Grandia, F. Jenelten, T. Homberger, and M. Hutter, “Elevation mapping for locomotion and navigation using GPU,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2022, pp. 2273–2280. 

   - [15] X. Cheng, K. Shi, A. Agarwal, and D. Pathak, “Extreme parkour with legged robots,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 11 443–11 450. 

   - [16] Y. Liu, T. Yu, H. Song, H. Zhu, N. Hu, Y. Hao, X. Yao, X. Zang, H. Chen, and J. Zhao, “FastStair: Learning to Run Up Stairs with Humanoid Robots,” _arXiv preprint arXiv:2601.10365_ , 2026. 

   - [17] R. Yang, G. Yang, and X. Wang, “Neural volumetric memory for visual locomotion control,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023, pp. 1430–1440. 

   - [18] Z. Zhuang, Z. Fu, J. Wang, C. Atkeson, S. Schwertfeger, C. Finn, and H. Zhao, “Robot parkour learning,” in _Conference on Robot Learning (CoRL)_ , 2023. 

   - [19] R. Yu, Q. Wang, H. Li, Z. Jun, Z. Wang, J. Wu, and Q. Zhu, “START: Traversing Sparse Footholds With Terrain Reconstruction,” _IEEE Robotics and Automation Letters_ , vol. 11, no. 2, pp. 2194–2201, 2025. 

   - [20] H. Duan, B. Pandit, M. S. Gadde, B. Van Marum, J. Dao, C. Kim, and A. Fern, “Learning vision-based bipedal locomotion for challenging terrain,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 56–62. 

   - [21] S. Luo, S. Li, R. Yu, Z. Wang, J. Wu, and Q. Zhu, “PIE: Parkour with implicit-explicit learning framework for legged robots,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 11, pp. 9986–9993, 2024. 

   - [22] Z. Zhuang, S. Yao, and H. Zhao, “Humanoid Parkour Learning,” in _8th Annual Conference on Robot Learning_ , 2024. 

   - [23] S. Zhu, Z. Zhuang, M. Zhao, K.-Y. Lee, and H. Zhao, “Hiking in the Wild: A Scalable Perceptive Parkour Framework for Humanoids,” _arXiv preprint arXiv:2601.07718_ , 2026. 

   - [24] W. Sun, Y. Su, L. Huang, A. Zhang, D. Wei, M. San, D. Tian, E. Cao, F. Yan, E. Xie, and Z. Xie, “Now You See That: Learning End-toEnd Humanoid Locomotion from Raw Pixels,” in _Robotics: Science and Systems (RSS)_ , 2026. 

   - [25] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal Policy Optimization Algorithms,” 2017. 

   - [26] N. Rudin, D. Hoeller, P. Reist, and M. Hutter, “Learning to walk in minutes using massively parallel deep reinforcement learning,” in _Conference on Robot Learning_ . PMLR, 2022, pp. 91–100. 

   - [27] M. Macklin, “Warp: A High-performance Python Framework for GPU Simulation and Graphics,” https://github.com/nvidia/warp, March 2022, NVIDIA GPU Technology Conference (GTC). 

   - [28] AGIBOT, “AGIBOT X2 Ultra,” https://www.agibot.com/products/X2, accessed on 2026-03-25. 

   - [29] Unitree Robotics, “Unitree H1,” https://www.unitree.com/h1/, accessed on 2026-03-25. 

   - [30] E. Todorov, T. Erez, and Y. Tassa, “MuJoCo: A physics engine for model-based control,” in _2012 IEEE/RSJ international conference on intelligent robots and systems_ . IEEE, 2012, pp. 5026–5033. 

- [6] H. Song, H. Zhu, T. Yu, Y. Liu, M. Yuan, W. Zhou, H. Chen, and H. Li, “Gait-Adaptive Perceptive Humanoid Locomotion with Real-Time Under-Base Terrain Reconstruction,” _arXiv preprint arXiv:2512.07464_ , 2025. 

- [7] F. Jenelten, T. Miki, A. E. Vijayan, M. Bjelonic, and M. Hutter, “Perceptive locomotion in rough terrain–online foothold optimization,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 4, pp. 5370–5376, 2020. 

- [8] R. Grandia, F. Jenelten, S. Yang, F. Farshidian, and M. Hutter, “Perceptive locomotion through nonlinear model-predictive control,” _IEEE Transactions on Robotics_ , vol. 39, no. 5, pp. 3402–3421, 2023. 

