---
title: "SSR: Scaling Surefooted and Symmetric Humanoid Traversal to the Open World"
date: "2026-05-29"
authors: "Ruiqi Yu; Yiwen Wang; Yuan Hao; Jun WU; Qiuguo Zhu"
url: https://arxiv.org/abs/2605.30770
pdf: https://arxiv.org/pdf/2605.30770
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.30770)** / [論文ページ](https://arxiv.org/abs/2605.30770)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **SSR: Scaling Surefooted and Symmetric Humanoid Traversal to the Open World** 

**Ruiqi Yu**<sup>1</sup><sup>_∗_</sup> **Yiwen Wang**<sup>1</sup><sup>_∗_</sup> **Yuan Hao**<sup>1</sup> **Jun Wu**<sup>1</sup> **Qiuguo Zhu**<sup>1</sup><sup>_†_</sup> 1Zhejiang University 


Figure 1: SSR scales surefooted and symmetric humanoid traversal to diverse open-world human environments. Driven by egocentric vision, the robot reliably traverses grassy slopes, stairs of varying sizes and structures, steps onto high platforms, and crosses wide gaps. Throughout long-horizon traversal, it maintains safe foot placement together with coordinated and natural whole-body motion. 

**Abstract:** Extending humanoid traversal to the open world is key to practical deployment in human environments, but remains challenging. The robot must use vision to ensure safe and reliable foot placement on heterogeneous terrain under highly dynamic motion, while producing coordinated, natural whole-body behaviors. We propose **SSR** , an efficient end-to-end framework for egocentric vision-based humanoid traversal that jointly learns these capabilities. SSR introduces _imagined foothold guidance_ , which learns to model forthcoming swing-foot contacts and evaluates their support to guide pre-touchdown swings toward stable regions, reducing edge slips. It further employs _equivariant latent-space symmetry augmentation_ to efficiently induce bilateral coordination under high-dimensional visual observations, and uses _terrain-specific multi-discriminator motion priors_ to encourage human-like behavior across scenes. Extensive experiments show that SSR achieves safe, stable, and high-quality locomotion on diverse real-world terrains, including stairs with varied structures and extreme challenges such as wide gaps and high platforms, while enabling reliable long-horizon traversal in open outdoor environments. Project website: `https://ssr-humanoid.github.io/` . 

**Keywords:** Open-World Humanoid Traversal, Safe Foot Placement, Equivariant Symmetry Learning 

> _∗_ Equal contribution 

> _†_ Corresponding author 

## **1 Introduction** 

Open-world human environments require humanoids to traverse heterogeneous terrains with agile, stable, and natural whole-body motion, from everyday stairs to wide gaps, and high platforms [1]. This demands that the robot perceive changing surroundings, place each step within safe support regions, and maintain coordinated, human-like behavior throughout long-horizon locomotion [2]. 

Recent learning-based humanoid locomotion methods leverage onboard perception to adapt to terrain changes. Among them, policies conditioned on egocentric depth images are especially promising for dynamic real-world scenes, as they avoid explicit, noise-sensitive mapping [3, 4, 5, 6]. However, turning such perception into robust open-world traversal remains an open challenge. The policy must infer local terrain structure from visual cues and convert this understanding into reliable foothold decisions. This is critical for flat-footed humanoids, since stepping near terrain edges sharply reduces the available support area and increases the risk of slips or falls. Beyond safety, traversal in human environments also requires coordinated, controllable, and natural whole-body motion. Prior work often introduces symmetry priors [7, 8, 9] or human-motion imitation [10, 11, 12], yet integrating them into egocentric-vision policies can be inefficient and brittle. High-dimensional visual observations make symmetry learning computationally expensive, while terrain-dependent dynamics can destabilize a shared human-like style prior. Overall, an efficient framework that jointly enables safe foot-placement behavior, symmetric and natural whole-body motion, and robust traversal across diverse terrains under vision is still lacking. 

To address these challenges, we propose **SSR** , a unified single-stage end-to-end reinforcement learning (RL) framework for vision-based humanoid traversal in complex real-world environments. SSR learns directly from egocentric depth and proprioception to jointly acquire reliable foot placement and high-quality whole-body motion, coupling gait symmetry with human-like behavior. 

For safe and accurate foot placement, we first introduce imagined foothold guidance during training. It learns to model forthcoming swing-foot contacts and evaluates their local support before touchdown, converting sparse contact-time safety assessment into dense predictive guidance. Unlike prior methods that assess foothold safety only at or after contact, leaving swing-phase actions with delayed feedback [3, 4, 13], this imagined interaction enables the policy to steer the foot early toward flat and well-supported regions, thereby reducing edge contacts, slips, and falls. 

To efficiently acquire coordinated whole-body motion, we develop equivariant latent-space symmetry augmentation. It applies mirror transformations to compact latent representations rather than high-dimensional visual observations. Compared with input-level augmentation and symmetry regularization, as well as strict equivariant architectures [8, 9, 14], this strategy reduces the overhead of symmetry learning for vision-based policies while preserving flexibility for exploration. We further incorporate a terrain-specific multi-discriminator adversarial motion prior [15] to capture terrainconditioned styles and maintain human-like motion across scenes. 

We evaluate SSR in diverse environments. As shown in Fig. 1, the robot robustly traverses slopes, rough ground, and stairs with varied structures. It can climb onto platforms up to 45 cm high, about 1 _._ 6 _×_ its shank length, and cross gaps as wide as 90 cm. More importantly, these capabilities transfer to complex outdoor scenes and support reliable long-horizon locomotion with precise foot placement, strong bilateral coordination, robust controllability, and natural motion. 

In summary, our main contributions are as follows: 

1. We present a novel single-stage training framework that jointly learns safe, symmetric, and human-like motion for vision-based humanoid traversal in diverse environments. 

2. We introduce imagined foothold guidance, which learns foot-contact foresight, providing dense swing-phase signals for timely correction of unsafe landing decisions and robust foot placement. 

3. We develop equivariant latent-space augmentation for efficient symmetry learning, and combine it with terrain-specific style priors to jointly improve whole-body motion quality. 

4. We validate the learned policy through extensive indoor and outdoor experiments, demonstrating agile and reliable humanoid locomotion over heterogeneous and challenging open-world terrains. 

2 

## **2 Related Work** 

**Learning Perceptive Humanoid Locomotion.** Data-driven RL has advanced humanoid locomotion under complex contact dynamics and environmental variation [1, 16, 17], and exteroceptive sensing lets controllers adapt to terrain before touchdown. Earlier methods construct height maps from LiDAR and odometry [18, 19, 20, 21], but depend on accurate localization and are sensitive to latency, drift, limited update rates, and occlusion. Recent approaches infer terrain directly from egocentric depth images [3, 4, 5, 22, 23], reducing reliance on mapping. However, many vision-based humanoid systems still target structured settings or require multi-stage pipelines, expert distillation, or dedicated depth modeling and augmentation [5, 17, 24, 25, 26]. In contrast, we learn a unified traversal policy from egocentric vision in a single-stage framework for diverse unstructured terrains. 

**Safe Foot Placement.** Classical footstep control decomposes locomotion into perception, planning, and tracking [27, 28, 29]. While effective in specific settings, they rely on hand-crafted design and conservative assumptions. RL-based methods learn foot placement end to end by tracking planner-generated footholds [30, 31, 32, 33] or penalizing unsafe landing regions [3, 4, 13, 34]. Yet these signals are often sparse, appearing only at or after contact, weakening swing-phase guidance and training efficiency [16, 35]. Liu et al. [25] densify learning by swing-trajectory tracking, but still depend on rule-based foothold generation and focus on stairs. Zhu et al. [36] reward derived foothold actions to improve landing quality. We learn to imagine future footholds during swing, assessing support before touchdown to guide flatter, safer landings without planners or edge detection. 

**Symmetry Learning in Legged Locomotion.** High-quality humanoid traversal requires coordinated bilateral motion. Prior work exploits morphological symmetry via data augmentation or regularization [8, 9, 14, 37], but under visual inputs with short-term memory, these methods require mirrored forward passes on high-dimensional inputs or mirrored hidden-state rollout, increasing computational and memory cost. Strictly equivariant architectures reduce this overhead [7], but may limit symmetry breaking near neutral states for gait exploration [38]. We use an equivariant encoder to move augmentation into latent space, balancing efficiency and flexibility in symmetry learning. 

## **3 Method** 

Our goal is safe and high-quality humanoid traversal over diverse unstructured terrains directly from proprioception and raw depth in a unified, efficient framework. SSR achieves this with imagined foothold guidance for dense pre-contact swing correction (Sec. 3.2), equivariant latent-space symmetry augmentation for efficient bilateral gait learning via compact latent mirroring (Sec. 3.3), and cross-terrain motion priors for human-like whole-body behavior (Sec. 3.4). Fig. 2 summarizes SSR. 

### **3.1 Single-Stage Learning of Generalizable Traversal Skills** 

We formulate humanoid locomotion as a partially observable Markov decision process (POMDP) and optimize the policy with PPO [39] under an asymmetric actor-critic architecture [40]. 

**Observations and Action.** At timestep _t_ , the policy receives proprioceptive and visual inputs. The proprioception **o**<sup>_p_</sup> _t_<sup>_∈_R72 includes base angular velocity</sup><sup>**_ω_**</sup><sup>_t_, projected gravity</sup><sup>**g**</sup><sup>_t_, velocity commands</sup> **u** _t_ , joint positions **_θ_** _t_ , joint velocities **_θ_**<sup>˙</sup> _t_ , and previous action **a** _t−_ 1. We stack a short history **o**<sup>_p_</sup> _t−h_ +1: _t_ to reduce partial observability. Together with the depth image **I** _t ∈_ R<sup>36</sup><sup>_×_36</sup> , this forms the policy observation **o** _t_ = ( **o**<sup>_p_</sup> _t−h_ +1: _t_<sup>_,_</sup><sup>**I**</sup><sup>_t_), which maps to actuated joint position targets</sup><sup>**a**</sup><sup>_t∈_R21.The critic</sup> additionally uses privileged information, including ground-truth base velocity **v** _t_ , foot velocities **v** _t_<sup>_f_,</sup> contact states **c** _t_ , limb positions **p**<sup>_h_</sup> _t_<sup>and</sup><sup>**p**</sup> _t_<sup>_f_, and height maps around the feet and body,</sup><sup>**H**</sup><sup>_f_</sup> _t_<sup>and</sup><sup>**H**</sup><sup>_b_</sup> _t_<sup>.</sup> **Policy Architecture.** Our policy comprises a recurrent cross-modal encoder, a motion-state estimator, and a MoE actor [41, 42]. The encoder extracts compact robot-environment context for environmental awareness and adaptability [43, 44]. It encodes the image with a convolutional neural network (CNN) and temporal proprioception with a multi-layer perceptron (MLP), then fuses them with a gated recurrent unit (GRU) into a latent representation with three heads, **ˆz** _t_ = [ **ˆz**<sup>_f_</sup> _t_<sup>_,_</sup><sup>**ˆz**</sup><sup>_b_</sup> _t_<sup>_,_</sup><sup>**ˆz**</sup> _t_<sup>_p_]</sup><sup>_⊤_.</sup> Here, **ˆz**<sup>_f_</sup> _t_<sup>and</sup><sup>**ˆz**</sup><sup>_b_</sup> _t_<sup>capture foot- and base-centric terrain geometry and decode</sup><sup>**ˆH**</sup> _t_<sup>_f_and</sup><sup>**ˆH**</sup><sup>_b_</sup> _t_<sup>[45], while</sup> **ˆz**<sup>_p_</sup> _t_<sup>,learned with a variational autoencoder (VAE), predicts next proprioception</sup><sup>**ˆo**</sup><sup>_p_</sup> _t_ +1<sup>to model sys-</sup> tem dynamics [40]. A separate MLP estimator predicts base velocity **ˆv** _t_ from temporal proprioception. During training, they are optimized with a hybrid prediction loss. We further impose mirror 

3 


Figure 2: **Overview of the SSR framework** . The policy combines a recurrent equivariant encoder, an estimator, and a MoE actor to learn unified traversal across terrains from egocentric depth images and temporal proprioception. During training, SSR learns surefooted, symmetric, and human-like motion through three mechanisms: (a) imagined foothold guidance for dense pre-contact swing correction, (b) equivariant latent augmentation for efficient symmetry learning, and (c) terrain-specific multi-discriminator AMP. 

equivariance on the encoder to support symmetry learning in Sec. 3.3. The actor takes current proprioception, **ˆv** _t_ , and **ˆz** _t_ as input, allowing one policy to represent terrain-dependent motion modes. **Reward Functions.** We group the objective into _r_<sup>_l_</sup> for task-oriented objectives, _r_<sup>_f_</sup> for foothold guidance, and _r_<sup>_s_</sup> for human-like motion style. We use three critics to improve estimation of corresponding value functions [46, 47]. See detailed reward definitions in Appendix A.3. 

### **3.2 Imagined Foothold Guidance for Foresighted Foot Placement Correction** 


Early in training, unstable gaits produce noisy future-contact targets. We therefore use terrain level as a reliability proxy and enable pre-contact guidance beyond a preset curriculum level. 

**Guiding Safer Swings Before Touchdown.** 


Given the imagined landing distribution, we form the guidance signal by measuring the unsupported fraction within a sole-covered region. Let **H**<sup>_f_</sup> ( **p** )= _{hk_ ( **p** ) _}_<sup>_n_</sup> _k_ =1<sup>denote the</sup> height map of a 22.5 cm _×_ 10 cm sole patch centered at **p** _∈_ R<sup>2</sup> , sampled every 2.5 cm. Here, _hk_ ( **p** ) is the terrain height at **p** + _δk_ and _δk_ is the _k_ -th offset. We define _support deficiency_ at foothold **p** as: 

Figure 3: **Imagined foothold guidance** . We measure support deficiency over a sole-sized terrain patch. During swing, a foothold imagination model anticipates futurecontact distributions for pre-contact dense guidance. 


where _h_<sup>_f_</sup> ( **p** ) is the sole height. For imagined pre-contact locations, we use _h_<sup>_f_</sup> ( **p** ) = max _k hk_ ( **p** ). Larger _ρ_ ( **p** ) indicates less support overlap, often near terrain edges or suspended regions. As each foot alternates between stance and swing, we instantiate this _foothold guidance_ in the RL objective: 


4 

where _ci,t_ indicates whether foot _i_ is in stance. Stance feet are evaluated at current contacts, while swing feet use expected deficiency under the imagined-contact distribution _qi,t_ , approximated with discrete Gaussian-weighted samples. This formulation converts touchdown-only safety signals into dense pre-contact guidance, encouraging earlier foot-placement correction before touchdown. 

### **3.3 Efficient Symmetry Learning with Equivariant Latent-Space Augmentation** 

Input-level symmetry augmentation is costly for visual recurrent policies, as each mirrored sample entails re-encoding the depth image and rolling out a mirrored memory state. We instead encode the original observation once and augment the compact actor input. The key requirement is a mirrorequivariant encoder, so that mirroring the latent is equivalent to encoding the mirrored observation. 

**Mirror Transformations.** Let _Mo_ , _Ms_ , and _Ma_ denote mirror transformations for actor observation, privileged state, and action. Since **o**<sup>_a_</sup> _t_<sup>=[</sup><sup>**o**</sup> _t_<sup>_p,_ˆ</sup><sup>**v**</sup><sup>_t,_ˆ</sup><sup>**z**</sup><sup>_t_]</sup><sup>_⊤_,</sup><sup>_Mo_combinesthephysicalpropri-</sup> oceptive and velocity transforms _Mp_ and _Mv_ with the latent transform _Mc_ . For latent variables without predefined mirror signs, we impose a symmetry-structured representation: each head ˆ **z**<sup>(</sup> _t_<sup>_k_)</sup> , _k ∈{f, b, p}_ , is organized as paired left-right channel groups, and _Mc_ swaps the two groups. Detailed component-wise rules are listed in Appendix B.1. 


**Equivariant Latent Encoding.** To make this latent transform valid, the encoder must map mirrored observations to mirrored latents. We first organize its inputs into symmetry-structured form: a fixed operator _T_ reorganizes temporal proprioception as **o** ¯<sup>_p_</sup> _t_<sup>=</sup><sup>_T_(</sup><sup>**o**</sup><sup>_p_</sup> _t−h_ +1: _t_<sup>),</sup> while the first CNN layer lifts the image into paired channels. Inspired by Cesa et al. [48], we then implement the MLP, CNN, and GRU with equivariant linear or convolutional layers. For each head _Eϕ_<sup>(</sup><sup>_k_),</sup> 

Figure 4: **Equivariant latent-space augmentation** . We form symmetry-structured inputs and build the encoder from equivariant linear and convolutional layers, allowing each latent head to be mirrored by _Mcc_ . 

**tation** . We form symmetry-structured _Eϕ_<sup>(</sup><sup>_k_)(</sup><sup>_Mc_</sup><sup>**o**¯</sup> _t_<sup>_p, M_2D</sup><sup>_It_) =</sup><sup>_McE_</sup> _ϕ_<sup>(</sup><sup>_k_)(¯</sup><sup>**o**</sup> _t_<sup>_p, It_)</sup><sup>_,_</sup> (4) and build the encoder from equivariant where _M_ 2D denotes horizontal reflection. Thus, the enand convolutional layers, allowing each latent coder compresses original inputs into a low-dimensional head to be mirrored by _Mcc_ . latent that supports channel-swap mirroring. Appendix B.2 gives the construction and proof. 

**Latent-Space Symmetry Augmentation.** During training, the encoder runs only on the original = observation. We then mirror the compact actor observation, privileged state, and action: **o**<sup>_a,g_</sup> _t Mo_ **o**<sup>_a_</sup> _t_<sup>,</sup><sup>**s**</sup> _t_<sup>_g_=</sup><sup>_Ms_</sup><sup>**s**</sup><sup>_t_,and</sup><sup>**a**</sup><sup>_g_</sup> _t_<sup>=</sup><sup>_Ma_</sup><sup>**a**</sup><sup>_t_.Thisgivesamirroredtrajectory</sup><sup>_τ g_= (</sup><sup>**o**</sup><sup>_a,g_</sup> 0<sup>_,_</sup><sup>**s**</sup><sup>_g_</sup> 0<sup>_,_</sup><sup>**a**</sup><sup>_g_</sup> 0<sup>_, r_0</sup><sup>_. . ._),</sup> which is appended to the original rollout _τ_ for PPO updates [8]. Compared with input-level augmentation, this avoids mirrored image encoding and recurrent hidden-state rollout, reducing memory and time while retaining flexible symmetry learning. 

### **3.4 Cross-Terrain Motion Priors with Multiple Discriminators** 

To encourage terrain-appropriate motion style, we employ multiple discriminators [15], one for each terrain type _i_ . Each _Di_ models terrain-specific reference motion style from a five-frame history **_ψ_** _t_ , where each frame **s**<sup>amp</sup> _t ∈_ R<sup>63</sup> contains projected gravity, base linear and angular velocities, joint positions and velocities, and limb positions. Following AMP [10], _Di_ is trained to distinguish reference from policy motions and produce a style reward that encourages terrain-appropriate natural behavior. We collect motion datasets for each terrain type. See details in Appendix A.8. 

## **4 Experiments** 

### **4.1 Experimental Setup** 

We evaluate SSR in extensive simulation and real-world experiments to answer three questions: (1) Can it learn a unified policy for high-performance traversal over diverse challenging terrains? (2) Do the key designs improve motion quality and learning efficiency? (3) Can it transfer zero-shot to unseen open-world scenes with long-horizon robustness and generalization? 

**Training Environment.** We perform single-stage training in Isaac Gym [49] with 4,096 AgiBot X2 humanoids on an NVIDIA RTX 4090 for about 20k iterations. We use NVIDIA Warp [50] to render deployment-consistent depth with terrain and self-occlusion. See Appendices A and C. 

5 


Figure 5: Traversal performance across terrains and difficulty levels in simulation. Top row compares SSR with prior methods, and bottom row reports ablation results.<sup>⋆</sup> denotes difficulties beyond the training curriculum. 

**Onboard Implementation.** On the real robot, a waist-mounted Intel RealSense D435i captures forward-facing depth at 60 Hz. Images are downsampled and cropped from 640 _×_ 360 to 36 _×_ 36. An onboard Jetson AGX Orin runs network inference and outputs actions at 50 Hz. 

**Compared Baselines.** We compare SSR with two perceptive baselines: (1) _HPL_ [3], a multi-stage egocentric vision parkour method; and (2) _PIM_ [18], a single-stage height-map traversal method with a hybrid internal model. We further consider ablations: (3) _NoFoothold_ removes foothold guidance _r_<sup>_f_</sup> ; (4) _NoImgn_ removes the imagination branch and keeps only the contact-time support assessment in _r_<sup>_f_</sup> ; (5) _NoSym_ disables data augmentation and uses a non-equivariant encoder; (6) _InpSym_ applies input-level mirroring with a non-equivariant encoder; as its peak memory exceeds 24 GB, this baseline alone was trained on a 48 GB RTX 4090; (7) _NoStyle_ removes the AMP style reward _r_<sup>_s_</sup> ; and (8) _SglDisc_ replaces multiple terrain-specific discriminators with a shared one. **Evaluation Metric and Protocol.** We use success rate, defined as the percentage of trials that complete a 20 s traversal without termination, as the primary metric of traversability. In simulation, each method is evaluated over 1,000 randomized trials per terrain under a 1.0 m/s forward command. 

### **4.2 Simulation Results** 

**Overall Traversal Performance.** Fig. 5 shows that SSR outperforms all baselines. It maintains near-100% success across all training difficulties, even on the hardest stairs, where a 22 cm foot has only a 3 cm support margin. It also traverses a 90 cm gap and a 45 cm platform beyond the curriculum range, demonstrating strong geometric adaptability and extrapolation. By contrast, _HPL_ and _PIM_ degrade rapidly as difficulty increases, suggesting that sparse or indirect foothold guidance is insufficient for precise foothold learning in these settings. Ablation results show that all SSR components matter, with the largest drops in _NoFoothold_ and _NoImgn_ , highlighting the importance of reliable foot placement for stable traversal. 

**Safer Foot Placement via Imagined Foothold Guidance.** We evaluate safe foot placement with two metrics: safe foothold rate (SFR), the fraction of footholds with support ratio above 75%, and mean support ratio (MSR), averaged over footholds. The support ratio is one minus support deficiency in Sec. 3.2. As shown in Fig. 6, SSR achieves the highest SFR on all terrains, indicating consistently safer contacts. Even on terrains requiring precise landing such as stairs down and gap, it concentrates footholds within valid support regions. The checkpoint-wise MSR curves further show SSR reaches 75% earliest, reflecting better learning efficiency. In contrast, _NoFoothold_ produces more aggressive gaits and the lowest safety. _NoImgn_ uses only contact-time assessment, so swing correction is often delayed until the foot nears the ground and contacts remain edge-biased. These 


Figure 6: Ablation study of safe foot placement learning. (a) Foothold distributions on stairs down and gap, smoothed with kernel density estimation (KDE). For each terrain, (b) the safe foothold rate (SFR); and (c) the mean support ratio (MSR) versus training iterations, evaluated using checkpoints saved every 100 iterations, with the dashed line marking the first point at which the MSR reaches 75%. 

6 


Figure 7: Ablation study of symmetry learning. (a) Trajectories under eight linear-velocity and two in-place yaw-rate commands. (b) SSR shows either-leg-led traversal on gaps and platforms, indicating bilateral balance. (c) Training-time curves of episodic return and maximum-terrain-level reach rate, with peak GPU memory. 

results show that guidance from imagined future contacts improves credit assignment for swingphase decisions, yields consistently supported landings, and accelerates safe traversal learning. **Bilateral Coordination via Efficient Latent-Space Symmetry Augmentation.** Fig. 7(a),(b) shows that symmetry augmentation improves controllability and bilateral coordination. With eightdirection velocity commands, SSR tracks more accurately and, under bidirectional yaw-rate commands, stays more localized during in-place turning, with nearly mirror-symmetric trajectories. _NoSym_ instead accumulates drift and left-right imbalance, revealing direction-dependent biases and fixed lead-leg dominance. In contrast, SSR supports both left- and right-foot-led traversal, indicating stronger bilateral skill acquisition. Fig. 7(c) further evaluates training efficiency. Compared with _InpSym_ , SSR achieves higher returns within the same training time, reaches maximum difficulty earlier, and reduces GPU memory from 28.8 GB to 23.7 GB (18%), making training feasible on one RTX 4090. This gain comes from mirroring a compact latent rather than high-dimensional inputs, avoiding extra encoding passes and hidden-state rollouts. Overall, equivariant latent-space augmentation scales symmetry-driven high-quality locomotion to visual recurrent policy learning. 

**Human-Like Motion via Stairs Up Stairs Down Gap High Platform Terrain-Specific Style PriMethod AP** (W) **PFCF** (N) **AP** (W) **PFCF** (N) **AP** (W) **PFCF** (N) **AP** (W) **PFCF** (N) **ors.** Human-like legged loSSR **381.3** _±_ 5 _._ 4 **507.7** _±_ 12 _._ 6 **342.4** _±_ 8 _._ 6 **519.2** _±_ 19 _._ 3 **214.4** _±_ 5 _._ 7 **463.4** _±_ 15 _._ 3 **253.0** _±_ 6 _._ 3 **480.4** _±_ 14 _._ 9 comotion is associated with NoStyle 451.6 _±_ 10 _._ 1 538.5 _±_ 13 _._ 5 371.4 _±_ 43 _._ 5 555.5 _±_ 21 _._ 5 317.0 _±_ 6 _._ 5 518.1 _±_ 16 _._ 6 292.3 _±_ 6 _._ 3 508.7 _±_ 16 _._ 4 low mechanical cost and SglDisc 391.8 _±_ 5 _._ 9 544.7 _±_ 9 _._ 7 345.3 _±_ 24 _._ 3 549.4 _±_ 23 _._ 4 241.1 _±_ 7 _._ 4 481.8 _±_ 14 _._ 7 258.2 _±_ 5 _._ 9 505.8 _±_ 16 _._ 4 smooth contacts [51, 52]. Table 1: Ablation study of human-like motion, measured by average power We therefore report average (AP) and peak foot contact force (PFCF). Results are reported as mean _±_ std. power and peak foot contact force as motion-quality proxies. Table 1 shows that SSR achieves the best overall metrics, with more harmonious whole-body motion, including a more natural arm swing and softer impacts, suggesting that the terrain-specific discriminators provide motion priors better aligned with terrain dynamics. Fig. 8 illustrates these natural motions across terrains. 

### **4.3 Real-World Results** 

**Lab-Level Evaluation.** We evaluate SSR’s sim-to-real transfer via zero-shot deployment on the real robot. Table 2 shows high success rates on all terrains, including unseen 90 cm gap and 45 cm platform, close to simulation. To the best of our knowledge, these settings are among the most challenging real-world terrain levels reported for a single traversal policy. Fig. 8 shows consistently 


Figure 8: Key frames of zero-shot real-world lab-level deployment. SSR enables stair traversal, 90 cm gap crossing, and 45 cm platform climbing with safe foot placement and natural whole-body motion. 

|**Terrain**|**Settings**|**Success Rate**|
|---|---|---|
||_Standard Settin_|_gs_|
|Stairs Up|15 / 30 cm|100.0%(20/20)|
|Stairs Down|15 / 30 cm|100.0%(20/20)|
|Gap|80 cm|95.0%(19/20)|
|Platform|40 cm|100.0%(20/20)|
||_Hard Setting_|_s_|
|Gap-H|90 cm <sup>⋆</sup>|85.0%(17/20)|
|Platform-H|45 cm <sup>⋆</sup>|95.0%(19/20)|


Table 2: Real-world lab-level traversal performance. Success rates are computed over 20 trials per terrain. 

7 


Figure 9: (a) The humanoid completes a 1.3 km, 40 min open-world traversal in an industrial heritage park, reliably crossing stairs of varying sizes, high platforms, rough ground, and grassy slopes. We further test robustness to (b) external disturbances, including wheeled-trolley shaking and pushes on descending stairs, and (c) visual occlusions from tall grass. (d) Zero-shot transfer to OOD terrains, including perforated grid flooring, a slippery trolley, movable forklift pallets, narrow 1.3 m-wide open-riser stairs, and spiral stairs. 

precise footholds on flat support regions, coordinated gait, and natural whole-body behavior, jointly improving traversal reliability and motion quality. 

**Outdoor Deployment.** We validate SSR in extensive outdoor environments, as shown in Fig. 1 and Fig. 9. In an outdoor industrial-park route, the robot completes a continuous 1.3 km traversal across diverse terrains without a reset or misstep, maintaining safe and coordinated locomotion over 40 min. Fig. 9(b)–(d) further presents three qualitative stress tests. **Perturbation Recovery** : the robot remains stable under horizontal and torsional shaking; when pushed from behind during stair descent, it still lands on the flat tread, showing timely and accurate foothold decisions under limited response time. **Visual Occlusion Adaptation** : under grass-induced occlusion, it shows no obvious gait degradation and actively steers away from poorly observed regions. **Zero-Shot Outof-Distribution (OOD) Generalization** : despite no prior exposure to perforated grids, slippery trolleys, or movable pallets during training, the policy traverses them stably. On narrow open-riser stairs and spiral stairs, it handles visual interference from holes and handrails, avoids sidewalls that could trap the feet, and adapts to varying stair widths, showing strong open-world generalization. 

**Cross-Platform Validation.** To evaluate embodiment-level applicability, we instantiate SSR on a full-size DEEP Robotics DR02 humanoid. Despite major differences from AgiBot X2, Appendix E reports high DR02 success rates, suggesting that SSR is not tied to a single humanoid platform. 

## **5 Conclusion** 

In this paper, we present SSR, a unified humanoid traversal framework that maps egocentric vision to stable, high-quality whole-body locomotion over diverse open-world terrains. Through imagined foothold guidance, SSR models forthcoming foot-terrain contacts to steer foresighted swing-phase foot-placement correction, enabling precise stepping in dynamic, complex settings. Our framework also leverages equivariant latent-space symmetry augmentation to efficiently learn bilateral coordination, while terrain-specific multi-discriminator AMP further encourages consistently natural motion across terrains. Extensive experiments demonstrate that SSR generalizes surefooted, symmetric, and human-like traversal to a broad spectrum of challenging scenarios, supporting reliable long-horizon real-world deployment. 

## **6 Limitations and Future Work** 

While SSR traverses diverse terrains effectively, several limitations remain. First, its fixed forwardfacing depth camera limits perceptual coverage, making omnidirectional traversal challenging. Future work may incorporate multi-view sensing or active viewpoint adjustment. Second, although SSR is robust to visual occlusions and several outdoor OOD terrains, severe depth-sensing failures, such as specular reflections under strong sunlight, can still distort local geometry. Integrating more robust perceptual embeddings may mitigate this issue. Third, SSR mainly focuses on foot-ground interaction, leaving upper-body contacts underexplored. Extending the framework to multi-contact skills and richer human demonstrations could further expand humanoid mobility. 

8 

### **Acknowledgments** 

We thank Qianshi Wang for assistance with the real-world experiments, and gratefully acknowledge AgiBot and DEEP Robotics for providing hardware support. This work was supported in part by the “Leading Goose” R&D Program of Zhejiang under Grant 2023C01177, the National Key R&D Program of China under Grant 2022YFB4701502, and the 2035 Key Technological Innovation Program of Ningbo City under Grant 2024Z300. 

## **References** 

- [1] I. Radosavovic, S. Kamat, T. Darrell, and J. Malik. Learning humanoid locomotion over challenging terrain. _arXiv preprint arXiv:2410.03654_ , 2024. 

- [2] K. Bonnen, J. S. Matthis, A. Gibaldi, M. S. Banks, D. M. Levi, and M. Hayhoe. Binocular vision and the control of foot placement during walking in natural terrain. _Scientific reports_ , 11(1):20881, 2021. 

- [3] Z. Zhuang, S. Yao, and H. Zhao. Humanoid parkour learning. In _Conference on Robot Learning (CoRL)_ , 2024. 

- [4] S. Zhu, Z. Zhuang, M. Zhao, K.-Y. Lee, and H. Zhao. Hiking in the wild: A scalable perceptive parkour framework for humanoids. _arXiv preprint arXiv:2601.07718_ , 2026. 

- [5] W. Sun, Y. Su, L. Huang, A. Zhang, D. Wei, M. San, D. Tian, E. Cao, F. Yan, E. Xie, et al. Now you see that: Learning end-to-end humanoid locomotion from raw pixels. _arXiv preprint arXiv:2602.06382_ , 2026. 

- [6] J. Sun, G. Han, P. Sun, W. Zhao, J. Cao, J. Wang, Y. Guo, and Q. Zhang. Dpl: Depthonly perceptive humanoid locomotion via realistic depth synthesis and cross-attention terrain reconstruction. _arXiv preprint arXiv:2510.07152_ , 2025. 

- [7] B. Nie, Y. Zhang, R. Jin, Z. Cao, H. Lin, X. Yang, and Y. Gao. Coordinated humanoid robot locomotion with symmetry equivariant reinforcement learning policy. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 40, pages 18523–18531, 2026. 

- [8] M. Mittal, N. Rudin, V. Klemm, A. Allshire, and M. Hutter. Symmetry considerations for learning task symmetric robot policies. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 7433–7439. IEEE, 2024. 

- [9] Z. Su, X. Huang, D. Ordo˜nez-Apraez, Y. Li, Z. Li, Q. Liao, G. Turrisi, M. Pontil, C. Semini, Y. Wu, et al. Leveraging symmetry in rl-based legged locomotion control. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 6899–6906. IEEE, 2024. 

- [10] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ , 40(4): 1–20, 2021. 

- [11] A. Tang, T. Hiraoka, N. Hiraoka, F. Shi, K. Kawaharazuka, K. Kojima, K. Okada, and M. Inaba. Humanmimic: Learning natural locomotion and transitions for humanoid robot via wasserstein adversarial imitation. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 13107–13114. IEEE, 2024. 

- [12] Q. Zhang, P. Cui, D. Yan, J. Sun, Y. Duan, G. Han, W. Zhao, W. Zhang, Y. Guo, A. Zhang, et al. Whole-body humanoid robot locomotion with human reference. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 11225–11231. IEEE, 2024. 

9 

- [13] X. Cheng, K. Shi, A. Agarwal, and D. Pathak. Extreme parkour with legged robots. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11443–11450. IEEE, 2024. 

- [14] C. Zhang, W. Xiao, T. He, and G. Shi. Wococo: Learning whole-body humanoid control with sequential contacts. In _Conference on Robot Learning (CoRL)_ , 2024. 

- [15] E. Vollenweider, M. Bjelonic, V. Klemm, N. Rudin, J. Lee, and M. Hutter. Advanced skills through multiple adversarial motion priors in reinforcement learning. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5120–5126. IEEE, 2023. 

- [16] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang. Beamdojo: Learning agile humanoid locomotion on sparse footholds. In _Robotics: Science and Systems (RSS)_ , 2025. 

- [17] Z. Wu, X. Huang, L. Yang, Y. Zhang, K. Sreenath, X. Chen, P. Abbeel, R. Duan, A. Kanazawa, C. Sferrazza, et al. Perceptive humanoid parkour: Chaining dynamic human skills via motion matching. _arXiv preprint arXiv:2602.15827_ , 2026. 

- [18] J. Long, J. Ren, M. Shi, Z. Wang, T. Huang, P. Luo, and J. Pang. Learning humanoid locomotion with perceptive internal model. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9997–10003. IEEE, 2025. 

- [19] X. Cui, L. Feng, Y. Zhou, H. Han, Z. Liu, and H. Wang. Pilot: A perceptive integrated low-level controller for loco-manipulation over unstructured scenes. _arXiv preprint arXiv:2601.17440_ , 2026. 

- [20] S. Ma, H. Chen, Z. Xu, Y. Zhao, K. Wu, R. Yang, L. Zou, Z. Gan, and W. Ding. Cmoe: Contrastive mixture of experts for motion control and terrain adaptation of humanoid robots. _arXiv preprint arXiv:2603.03067_ , 2026. 

- [21] J. He, C. Zhang, F. Jenelten, R. Grandia, M. B¨acher, and M. Hutter. Attention-based map encoding for learning generalized legged locomotion. _Science Robotics_ , 10(105):eadv3604, 2025. 

- [22] D. Wang, X. Wang, X. Liu, J. Shi, Y. Zhao, C. Bai, and X. Li. More: Mixture of residual experts for humanoid lifelike gaits learning on complex terrains. _arXiv preprint arXiv:2506.08840_ , 2025. 

- [23] Z. Zhuang, S. Zhu, M. Zhao, and H. Zhao. Deep whole-body parkour. _arXiv preprint arXiv:2601.07701_ , 2026. 

- [24] Q. Zhang, G. Han, J. Sun, W. Zhao, C. Sun, J. Cao, J. Wang, Y. Guo, and R. Xu. Distillationppo: A novel two-stage reinforcement learning framework for humanoid robot perceptive locomotion. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 2916–2922. IEEE, 2025. 

- [25] Y. Liu, T. Yu, H. Song, H. Zhu, N. Hu, Y. Hao, X. Yao, X. Zang, H. Chen, and J. Zhao. Faststair: Learning to run up stairs with humanoid robots. _arXiv preprint arXiv:2601.10365_ , 2026. 

- [26] N. Rudin, J. He, J. Aurand, and M. Hutter. Parkour in the wild: Learning a general and extensible agile locomotion policy using multi-expert distillation and rl fine-tuning. _arXiv preprint arXiv:2505.11164_ , 2025. 

- [27] C. Mastalli, I. Havoutis, M. Focchi, D. G. Caldwell, and C. Semini. Motion planning for quadrupedal locomotion: Coupled planning, terrain mapping, and whole-body control. _IEEE Transactions on Robotics_ , 36(6):1635–1648, 2020. 

10 

- [28] A. Agrawal, S. Chen, A. Rai, and K. Sreenath. Vision-aided dynamic quadrupedal locomotion on discrete terrain using motion libraries. In _2022 International Conference on Robotics and Automation (ICRA)_ , pages 4708–4714. IEEE, 2022. 

- [29] S. Fahmi, V. Barasuol, D. Esteban, O. Villarreal, and C. Semini. Vital: Vision-based terrainaware locomotion for legged robots. _IEEE Transactions on Robotics_ , 39(2):885–904, 2022. 

- [30] V. Tsounis, M. Alge, J. Lee, F. Farshidian, and M. Hutter. Deepgait: Planning and control of quadrupedal gaits using deep reinforcement learning. _IEEE Robotics and Automation Letters_ , 5(2):3699–3706, 2020. 

- [31] F. Jenelten, J. He, F. Farshidian, and M. Hutter. Dtc: Deep tracking control. _Science Robotics_ , 9(86):eadh5401, 2024. 

- [32] W. Yu, D. Jain, A. Escontrela, A. Iscen, P. Xu, E. Coumans, S. Ha, J. Tan, and T. Zhang. Visual-locomotion: Learning to walk on complex terrains with vision. In _Conference on Robot Learning (CoRL)_ , 2021. 

- [33] S. Gangapurwala, M. Geisert, R. Orsolino, M. Fallon, and I. Havoutis. Rloc: Terrain-aware legged locomotion using reinforcement learning and optimal control. _IEEE Transactions on Robotics_ , 38(5):2908–2927, 2022. 

- [34] Z. Zhuang, Z. Fu, J. Wang, C. Atkeson, S. Schwertfeger, C. Finn, and H. Zhao. Robot parkour learning. In _Conference on Robot Learning (CoRL)_ , 2023. 

- [35] R. S. Sutton. _Temporal credit assignment in reinforcement learning_ . University of Massachusetts Amherst, 1984. 

- [36] D. Zhu, C. Zhu, Z. Zhang, S. Xin, and Y. Liu. Learning safe locomotion for quadrupedal robots by derived-action optimization. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 6870–6876. IEEE, 2024. 

- [37] C. Zhang, N. Rudin, D. Hoeller, and M. Hutter. Learning agile locomotion on risky terrains. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 11864–11871. IEEE, 2024. 

- [38] F. Abdolhosseini, H. Y. Ling, Z. Xie, X. B. Peng, and M. Van de Panne. On learning symmetric locomotion. In _Proceedings of the 12th ACM SIGGRAPH Conference on Motion, Interaction and Games_ , pages 1–10, 2019. 

- [39] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [40] I. M. A. Nahrendra, B. Yu, and H. Myung. Dreamwaq: Learning robust quadrupedal locomotion with implicit terrain imagination via deep reinforcement learning. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5078–5084. IEEE, 2023. 

- [41] R. Huang, S. Zhu, Y. Du, and H. Zhao. Moe-loco: Mixture of experts for multitask locomotion. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 14218–14225. IEEE, 2025. 

- [42] R. A. Jacobs, M. I. Jordan, S. J. Nowlan, and G. E. Hinton. Adaptive mixtures of local experts. _Neural computation_ , 3(1):79–87, 1991. 

- [43] S. Luo, S. Li, R. Yu, Z. Wang, J. Wu, and Q. Zhu. Pie: Parkour with implicit-explicit learning framework for legged robots. _IEEE Robotics and Automation Letters_ , 9(11):9986–9993, 2024. 

- [44] P. Li, H. Li, Y. Ma, L. Chang, X. Yang, R. Yu, Y. Zhang, Y. Cao, Q. Zhu, and G. Sartoretti. Kivi: Kinesthetic-visuospatial integration for dynamic and safe egocentric legged locomotion. _arXiv preprint arXiv:2509.23650_ , 2025. 

11 

- [45] R. Yu, Q. Wang, H. Li, Z. Jun, Z. Wang, J. Wu, and Q. Zhu. Start: Traversing sparse footholds with terrain reconstruction. _IEEE Robotics and Automation Letters_ , 11(2):2194–2201, 2025. 

- [46] F. Zargarbashi, J. Cheng, D. Kang, R. Sumner, and S. Coros. Robotkeyframing: Learning locomotion with high-level objectives via mixture of dense and sparse rewards. In _Conference on Robot Learning (CoRL)_ , 2024. 

- [47] T. Huang, J. Ren, H. Wang, Z. Wang, Q. Ben, M. Wen, X. Chen, J. Li, and J. Pang. Learning humanoid standing-up control across diverse postures. In _Robotics: Science and Systems (RSS)_ , 2025. 

- [48] G. Cesa, L. Lang, and M. Weiler. A program to build e(n)-equivariant steerable cnns. In _International Conference on Learning Representations (ICLR)_ , 2022. 

- [49] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa, et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 

- [50] M. Macklin. Warp: A high-performance python framework for gpu simulation and graphics. In _NVIDIA GPU Technology Conference (GTC)_ , volume 3, 2022. 

- [51] Z. Fu, A. Kumar, J. Malik, and D. Pathak. Minimizing energy consumption leads to the emergence of gaits in legged robots. In _Conference on Robot Learning (CoRL)_ , 2021. 

- [52] B. R. Whittington and D. G. Thelen. A simple mass-spring model with roller feet can induce the ground reactions observed in human walking. _Journal of biomechanical engineering_ , 131 (1):011013, 2009. 

- [53] N. Rudin, D. Hoeller, P. Reist, and M. Hutter. Learning to walk in minutes using massively parallel deep reinforcement learning. In _Conference on Robot Learning (CoRL)_ , 2021. 

- [54] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 5442–5451, 2019. 

- [55] W. Xie, J. Han, J. Zheng, H. Li, X. Liu, J. Shi, W. Zhang, C. Bai, and X. Li. Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills. In D. Belgrave, C. Zhang, H. Lin, R. Pascanu, P. Koniusz, M. Ghassemi, and N. Chen, editors, _Advances in Neural Information Processing Systems_ , volume 38, pages 62406–62433. Curran Associates, Inc., 2025. URL `https://proceedings.neurips.cc/paper_files/paper/ 2025/file/5a0e51901cff2b42d379ec7869603e91-Paper-Conference.pdf` . 

12 

## **A Policy Training Details** 

### **A.1 Terrain Curriculum** 

As shown in Fig. 10, we generate five types of terrain for policy learning. Each terrain type contains 20 difficulty levels, with the difficulty progressively increased according to the curriculum strategy in [53]. Each terrain instance is constructed over a rectangular region measuring 8 m _×_ 4 m. 


Figure 10: Overview of terrain types used for training. 

|**Terrain Type**|**Parameter**|**Range**|
|---|---|---|
|Slope|Incline|[0_,_ 20]<sup>_◦_</sup>|
|Stairs|Step length<br>Stepheight|[0_._25_,_ 0_._4] m<br>[0_._05_,_ 0_._2]m|
|Discrete|Obstacle height|[0_._05_,_ 0_._2]m|
|Ga|Width|[0_._1_,_ 0_._8] m|
|p|Depth|[0_._3_,_ 0_._6]m|
|Platform|Height|[0_._05_,_ 0_._4]m|


Table 3: Parameter ranges in the terrain curriculum. 

### **A.2 Commands** 

At timestep _t_ , the locomotion command is defined as **u** _t_ = [ _vx_<sup>cmd</sup> _, vy_<sup>cmd</sup> _, ωz_<sup>cmd</sup> ]<sup>_⊤_</sup> . During training, the robot is commanded to traverse the terrain along a straight path aligned with the _x_ -axis of the world frame while tracking a target heading. The yaw angular velocity command _ωz_<sup>cmd</sup> is computed from the heading error, while the translational commands _vx_<sup>cmd</sup> and _vy_<sup>cmd</sup> are obtained by projecting the prescribed forward velocity from the world frame into the base frame. The terrain-specific ranges of the forward velocity and target heading are summarized in Table 4. 

|**Terrain Type**|**Forward Velocity (m/s)**|**Heading (°)**|
|---|---|---|
|Slope|_U_(_−_1_,_1)|_U_(_−_80_,_80)|
|Stairs, discrete|_U_(0_,_1_._2)|_U_(_−_30_,_30)|
|Gap, platform|_U_(0_,_1_._2)|_U_(_−_15_,_15)|


Table 4: Ranges of the forward velocity and target heading. 

To encourage omnidirectional locomotion, we further uniformly sample **u** _t_ in the base frame from a predefined command space after the robot has cleared the highest terrain difficulty and exited the terrain region. This stage exposes the policy to diverse combinations of forward, lateral, and turning motions beyond structured terrain-traversal commands. The corresponding command ranges are listed in Table 5. 

|**Command Term**|**Range**|
|---|---|
|Forward velocity|_U_(_−_1_,_1)m/s|
|Lateral velocity|_U_(_−_0_._4_,_0_._4)m/s|
|Yaw angular velocity|_U_(_−_1_._2_,_1_._2)rad/s|


Table 5: Ranges of the locomotion commands. 

### **A.3 Rewards** 

Table 6 summarizes the reward terms used for policy learning, grouped by reward category. For each term, the table provides its mathematical expression and coefficient. It also reports the advantage weight associated with each reward group in the multi-critic formulation. Table 7 defines the main symbols used in these reward expressions. 

13 

|**Term**|**Expression**<br>**Weight**|
|---|---|
|(a)_Locomotion Reward_|_r_<sup>_l_</sup><br>_wl_ = 1_._0|
|Linear Velocity Tracking|exp<br>�<br>_−∥_**v**_xy −_**v**<sup>cmd</sup><br>_xy _<sup>_∥_2</sup><br>2<sup>_/σ_</sup>_v_<br>�<br>1.0<br>|
|Angular Velocity Tracking|exp<br>�<br>_−_(**_ω_**yaw_−_**_ω_**<sup>cmd</sup><br>yaw <sup>)2</sup><sup>_/σ_</sup>_ω_<br>�<br>0.8<br><br><br>|
|Orientation|exp<br>�<br>_−∥_**g**_xy∥_<sup>2</sup>_/σg_<br>�<br>0.5<br>|
|Angular Velocity (xy)|exp<br>�<br>_−∥_**_ω_**_xy∥_<sup>2</sup><br>2<sup>_/σ_</sup>_ω_<br>�<br>0.25|
|Base Height|exp<br>�<br>_−_(_hb −h_<sup>tar</sup><br>_b_ <sup>)2</sup><sup>_/σh_</sup><br>�<br>0.4|
|Action Rate|1<br>_N_ <sup>_∥_</sup><sup>**a**</sup><sup>_t −_</sup><sup>**a**</sup><sup>_t−_1</sup><sup>_∥_2</sup><br>2<br>_−_0_._12<br>|
|Smoothness|1<br>_N_ <sup>_∥_</sup><sup>**a**</sup><sup>_t −_2</sup><sup>**a**</sup><sup>_t−_1 +</sup><sup>**a**</sup><sup>_t−_2</sup><sup>_∥_2</sup><br>2<br>_−_0_._06<br>|
|DoF Velocity|1<br>_N_ <sup>_∥_˙</sup><sup>**_θ_**</sup><sup>_/_ ˙</sup><sup>**_θ_**max</sup><sup>_∥_2</sup><br>2<br>_−_0_._96|
|DoF Torque|1<br>_N_ <sup>_∥_</sup><sup>**_τ_**</sup><sup>_/_</sup><sup>**_τ_** max</sup><sup>_∥_2</sup><br>2<br>_−_0_._6|
|DoF Deviation|1<br>_N_ <sup>_∥_</sup><sup>**_θ_**</sup><sup>_−_</sup><sup>**_θ_**def</sup><sup>_∥_1</sup><br>_−_1_._8|
|DoF Position Limits|1<br>_N_ <sup>_∥_1(</sup><sup>**_θ_**</sup> <sup>_/∈_[</sup><sup>**_θ_**min</sup><sup>_,_</sup><sup>**_θ_**max])</sup><sup>_∥_1</sup><br>_−_1_._5<br><br><sup>˙˙</sup>|
|DoF Velocity Limits|1<br>_N_ <sup>_∥_1(</sup><sup>_|_ </sup><sup>**_θ_**</sup><sup>_| >_ </sup><sup>**_θ_**max)</sup><sup>_∥_1</sup><br>_−_6_._0|
|DoF Torque Limits|1<br>_N_ <sup>_∥_1(</sup><sup>_|_</sup><sup>**_τ_**</sup><sup>_| >_</sup><sup>**_τ_** max)</sup><sup>_∥_1</sup><br>_−_6_._0|
|Stand Still|1<br>_N_ <sup>_∥_</sup><sup>**_θ_**</sup><sup>_−_</sup><sup>**_θ_**def</sup><sup>_∥_1</sup><sup>_·_ 1(</sup><sup>_∥_</sup><sup>**u**</sup><sup>_t∥_2</sup> <sup>_≤ϵ_)</sup><br>_−_0_._12|
|Single Support|1[_∥_**u**_t∥_2 _≤ϵ ∨∃t_<sup>_′ _</sup>_∈_[_t −_0_._2 s_, t_]s.t._n_<sup>con</sup><br>_t_<sup>_′_</sup><br>= 1]<br>0.2<br>|
|Impact Velocity|�2<br>_i_=1 <sup>_vf_</sup><br>_z,i_<br>2_· ci_<br>_−_1_._3|
|Contact Slippage|�2<br>_i_=1<sup>_∥_</sup><sup>**v**</sup><sup>_f_</sup><br>_xy,i_<sup>_∥_2</sup><br>2 <sup>_· c_</sup>_i_<br>_−_0_._2<br><br><sup>i</sup>|
|Feet Air Time|�2<br>_i_=1 <sup>max(</sup><sup>_t_air</sup><sup>_,i −t_tar</sup><br>air<sup>_,_ 0)</sup><sup>_· c_first</sup><br>_i_<br>_−_2_._0<br><br><br>|
|Feet Stumble|�2<br>_i_=1 <sup>1(</sup><sup>_∥_</sup><sup>**F**</sup><sup>_f_</sup><br>_xy,i_<sup>_∥_2</sup> <sup>_>_ 3</sup><sup>_|F f_</sup><br>_z,i_<sup>_|_)</sup><br>_−_2_._0<br>|
|Feet Lateral Distance|exp<br>�<br>min(_dy −d_<sup>min</sup><br>_y_<br>_,_0)_/σd_<br>�<br>0.08|
|(b)_Foothold Reward_|_r_<sup>_f_</sup><br>_wf_ = 0_._25|
|Imagined Foothold Guidance<sup>1 </sup>|exp<br>�<br>_−_(<sup>�2</sup><br>_i_=1 <sup>˜</sup><sup>_ρi,t_)2</sup><sup>_/σf_</sup><br>�<br>1.0|
|(c)_Style Reward_|_r_<sup>_s_</sup><br>_ws_ = 0_._2|
|AMP|max[0_,_ 1_−_0_._25(_Di_(**_ψ_**_t_)_−_1)<sup>2</sup>]<br>1.0|


> 1 On slope terrains, we set _ρ_ ˜ _i,t_ =0 for both feet, so that _rtf_<sup>=1, avoiding unintended suppression on inclined contacts.</sup> 

Table 6: Reward terms and weights. 

|**Symbol**|**Description**|
|---|---|
|_σv, σω, σg, σh, σd, σf_<br>**_θ_**<sup>min</sup>_,_ **_θ_**<sup>max</sup>|Gaussian variance scales, set to 0.25, 0.25, 0.01, 0.01, 0.03, and 0.0625.<br>Lower and upper joint position limits.|
|**_θ_**<sup>def</sup>|Default joint positions.|
|˙**_θ_**<sup>max</sup>|Maximum allowable joint velocities.|
|**_τ_**|Computed joint torques.|
|**_τ_** <sup>max</sup>|Maximum allowable joint torques.|
|_ϵ_|Threshold for identifying zero-command, set to 0.15.|
|_hb, h_<sup>tar</sup><br>_b_|Base height and target base height relative to the ground. _h_<sup>tar</sup><br>_b_<br>= 0_._68.|
|_t_air_,i, t_<sup>tar</sup><br>air<br>_c_<sup>first</sup><br>_i_|Air time of foot_i_and target air time. _t_<sup>tar</sup><br>air <sup>= 0</sup><sup>_._4.</sup><br>Binary indicator of whether foot_i_makes its first contact with the ground.|
|_n_<sup>con</sup><br>_t_<sup>_′_</sup>|Number of feet in contact with the ground at time_t_<sup>_′_</sup>.|
|**F**<sup>_f_</sup><br>_i_<br>|Contact force on foot_i_.|
|**v**<sup>_f_</sup><br>_i_|Velocity of foot_i_.|
|_dy_|Lateral distance between the two feet.|
|_d_<sup>min</sup><br>_y_|Minimum allowable lateral distance between two feet, set to 0.22.|


Table 7: Symbols in the reward definitions. 

14 

### **A.4 Network Architectures** 

Table 8 summarizes the network architectures used in our framework. 

|**Module**|**Submodule**|**Component**|**Structure**|
|---|---|---|---|
|||Number of experts|5|
||MoE Actor|Expert MLP hidden size|[1024, 512, 128]|
|Asymmetric<br>Actor-Critic||Gate MLP hidden size<br>Activation|128<br>ELU|
|||Number of critics|3|
||Multi-Critic|MLP size|[512, 256, 128]|
|||Activation|ELU|
|||MLP hidden size|[512, 256, 128]|
||Proprioception Encoder|Activation|ELU|
|||MLP embeddingdim|128|
|||CNN Channels|[32, 64, 128]|
|||CNN kernel sizes|[8, 4, 3]|
||Depth Encoder|CNN strides|[4, 2, 2]|
|Encoder||Activation|ELU|
|||CNN embeddingdim|128|
||Temporal Encoder|GRU hidden dim<br>GRU layers|256<br>1|
|||MLP hidden size|[512, 256, 128]|
||Fusion Encoder|Activation|ELU|
|||MLP embeddingdim|48<br>|
||Latent Linear Heads|Output dims|ˆ**z**<sup>_f_</sup><br>_t_ <sup>: 16</sup><sup>_,_ ˆ</sup><sup>**z**</sup><sup>_b_</sup><br>_t_ <sup>: 16</sup><sup>_,_ ˆ</sup><sup>**z**</sup><sup>_p_</sup><br>_t_ <sup>: 16</sup>|
|||MLP hidden size|[512, 256, 128]|
||Estimator|Activation|ELU|
|||Output dims|ˆ**v**_t_ : 3|
|Foothol|d Imagination Model|MLP hidden size<br>Activation|[256, 128]<br>ELU|
|||Number of discriminators|5|
|Mul|ti-Discriminator|MLP hidden size<br>Activation|[512, 256, 128]<br>ReLU|


Table 8: Network architectures. 

### **A.5 Training Hyperparameters** 

Table 9 summarizes the main hyperparameters used to train the components of our framework. We use four separate Adam optimizers for PPO, the encoder and estimator, the foothold imagination model, and the multi-discriminator, all initialized with a learning rate of 5 _×_ 10<sup>_−_4</sup> . 

|**Component**|**Parameter**|**Value**|
|---|---|---|
||Value loss coef<br>Entropy coef|1.0<br>0.005|
||Desired KL|0.01|
||Minimum policy std|0.2|
|PPO|GAE_λ_|0.95|
||Reward discount_γ_|0.99|
||Number of environments|4096|
||Num steps per iteration|24|
||Num learning epochs|5|
||Num mini-batches|4|
||Base height map MSE coef|2.0|
|Encoder|Foot height maps MSE coef|1.0|
||Next proprioception MSE coef|5.0|
||VAE KL divergence coef|1.0|
|Estimator|VelocityMSE coef|2.0|
|MltiDiiit|Weight decay|1_×_10<sup>_−_4</sup>|
|u-scrmnaor|Gradient penalty coef_w_<sup>gp</sup>|20.0|


Table 9: Training hyperparameters. 

15 

### **A.6 Domain Randomization** 

Table 10 summarizes the domain randomization settings used in our framework, including those applied to the system dynamics and depth sensing. 

|**Category**|**Parameter**|**Range / Value**|
|---|---|---|
||Base added mass|_U_(_−_2_._0_,_12_._5) kg|
||Base CoM offset|_U_(_−_0_._1_,_0_._1) m|
||Link mass|_U_(0_._9_,_1_._1)_×_default|
||Link CoM offset|_U_(_−_0_._01_,_0_._01) m|
|Dnamics|Motor strength|_U_(0_._8_,_1_._2)_×_default|
|y|PD gains|_U_(0_._9_,_1_._1)_×_default|
||Ground friction|_U_(0_._2_,_1_._25)|
||Action delay|_U_(0_,_2)control steps|
||Push interval|12 s|
||Push velocity|_U_(_−_0_._4_,_0_._4)m_/_s|
||Camera position offset|_U_(_−_0_._01_,_0_._01) m|
|Dth Si|Camera orientation offset|_U_(_−_1_,_1)<sup>_◦_</sup>|
|ep ensng|Horizontal FoV offset|_U_(_−_1_,_1)<sup>_◦_</sup>|
||Vertical FoV offset|_U_(_−_1_,_1)<sup>_◦_</sup>|


Table 10: Domain randomization settings. 

### **A.7 Termination Criteria** 

An episode is terminated when any of the following conditions is satisfied: 

- The episode reaches its maximum duration. 

- The robot moves outside the terrain boundary. 

- The contact force on any termination-contact link exceeds a predefined threshold. 

- The robot exhibits severe orientation instability. 

- On gap terrain, any foot drops below a predefined threshold beneath the ground plane. 

### **A.8 Motion Prior Dataset** 

For each terrain type, the corresponding motion priors are sourced from two datasets: customized motion recordings collected using a motion capture system and a selected subset of the open-source AMASS dataset [54]. All motion sequences are retargeted to our humanoid following Xie et al. [55]. Table 11 summarizes the statistics of the motion datasets used for training. 

|**Terrain Te**|**Flat-g**|**round motio**|**ns**||**Terr**|**ain tra**|**versals**||**Ttl Ti ()**|
|---|---|---|---|---|---|---|---|---|---|
|**yp**|**Forward**|**Backward**|**Turn**|**Slope**|**Stairs**|**Step**|**Gap**|**Platform**|**oa me s**|
|Slope|✓|✓|✓|✓|||||261.3|
|Stairs|✓||✓||✓||||295.8|
|Discrete|✓||✓|||✓|||136.0|
|Gap|✓||✓||||✓||174.5|
|Platform|✓||✓|||✓||✓|181.6|


Table 11: Motion dataset statistics. 

16 

## **B Equivariant Network Details** 

### **B.1 Mirror Transformations and Symmetry-Structured Encoder Inputs** 

This section formalizes the mirror transformations and symmetry operators used in our method. We first define the mirror transformations used for data augmentation in Sec. 3.3. We then describe the structure of the encoder inputs and introduce the associated operators for constructing symmetrystructured representations, which are also used in the proofs in Appendix B.2. 

We begin with the mirror transformation _Mc_ for the latent representation ˆ **z** _t_ , defined as an exchange between the left and right channel groups. More generally, _Mc_ is the primitive mirror operator for symmetry-structured vectors. For a vector whose channel dimension is partitioned into two paired groups, _Mc_ swaps the two groups: 


We next define the mirror transformation _Mp_ for proprioception. To specify its action on joint-space variables, we introduce the following block notation. For any joint-space quantity, including joint positions, joint velocities, and actions, we write **x** = � **x**<sup>leg</sup> _R_<sup>_,_</sup><sup>**x**</sup> _L_<sup>leg</sup><sup>_,x_waist</sup><sup>_,_</sup><sup>**x**</sup> _R_<sup>arm</sup> _,_ **x**<sup>arm</sup> _L_ � _⊤ ∈_ R21 _._ Each leg block is ordered as _(hip pitch, hip roll, hip yaw, knee, ankle pitch, ankle roll)_ , and each arm block is ordered as _(shoulder pitch, shoulder roll, shoulder yaw, elbow)_ . 

Under reflection about the sagittal plane, the left and right kinematic chains are exchanged, and the sign of each coordinate depends on the corresponding physical axis convention. We therefore define the sign vectors for the joint blocks as **_s_** leg = [1 _, −_ 1 _, −_ 1 _,_ 1 _,_ 1 _, −_ 1]<sup>_⊤_</sup> and **_s_** arm = [1 _, −_ 1 _, −_ 1 _,_ 1]<sup>_⊤_</sup> . The resulting joint-block reflection is defined as 


where _⊙_ denotes element-wise multiplication. For the remaining proprioceptive quantities with explicit physical semantics, namely base-frame polar vectors, base angular velocities, and velocity commands, we use the sign vectors **_s_** _y_ = [1 _, −_ 1 _,_ 1]<sup>_⊤_</sup> , **_s_** _ω_ = [ _−_ 1 _,_ 1 _, −_ 1]<sup>_⊤_</sup> , and **_s_** _u_ = [1 _, −_ 1 _, −_ 1]<sup>_⊤_</sup> . 

Table 12 summarizes the mirror transformations used for data augmentation in Sec. 3.3, including those for proprioception, actor observations, privileged states, and actions. 

|**Transformation**|**Component**|**Variable**|**Mirror rule**|**Dim.**|
|---|---|---|---|---|
|||**Proprioce**|**ption o**<sup>_~~p~~_</sup><br>_t_||
||Base angular velocity|**_ω_**_t_|**_ω_**_t ⊙_**_s_**_ω_|3|
||Projected gravity|**g**_t_|**g**_t ⊙_**_s_**_y_|3|
|_Mp_|Velocity command|**u**_t_|**u**_t ⊙_**_s_**_u_|3|
||Joint positions|**_θ_**_t_|_F_(**_θ_**_t_)|21|
||Joint velocities|˙**_θ_**_t_|_F_(<sup>˙</sup>**_θ_**_t_)|21|
||Previous action|**a**_t−_1|_F_(**a**_t−_1)|21|
|||**Actor obser**|**vation o**<sup>_a_</sup><br>_t_||
|_Mo_|Proprioception<br>Base velocity estimate|**o**<sup>_p_</sup><br>_t_<br>ˆ**v**_t_<br>|_Mp_**o**<sup>_p_</sup><br>_t_<br>_Mv_ˆ**v**_t_ = ˆ**v**_t ⊙_**_s_**_y_<br>|72<br>3|
||Encoder latent|ˆ**z**_t_ = [ˆ**z**<sup>_f_</sup><br>_t _<sup>_,_ ˆ</sup><sup>**z**</sup><sup>_b_</sup><br>_t_<sup>_,_ ˆ</sup><sup>**z**</sup><sup>_p_</sup><br>_t_ <sup>]</sup><sup>_⊤_</sup>|[_Mc_ˆ**z**<sup>_f_</sup><br>_t _<sup>_, Mc_ˆ</sup><sup>**z**</sup><sup>_b_</sup><br>_t_<sup>_, Mc_ˆ</sup><sup>**z**</sup><sup>_p_</sup><br>_t_ <sup>]</sup><sup>_⊤_</sup>|48|
|||**Privileged**|**state s**_t_||
||Proprioception|**o**<sup>_p_</sup><br>_t_|_Mp_**o**<sup>_p_</sup><br>_t_|72|
||Base linear velocity|**v**_t_|_Mv_**v**_t_ = **v**_t ⊙_**_s_**_y_|3|
|_Ms_|Foot linear velocities<br>Foot contact|[**v**<sup>_f_</sup><br>_t,R_<sup>_,_</sup> <sup>**v**</sup><sup>_f_</sup><br>_t,L_<sup>]</sup><sup>_⊤_</sup><br>[_ct,R, ct,L_]<sup>_⊤_</sup>|[**v**<sup>_f_</sup><br>_t,L _<sup>_⊙_</sup><sup>**_s_**</sup><sup>_y,_</sup> <sup>**v**</sup><sup>_f_</sup><br>_t,R _<sup>_⊙_</sup><sup>**_s_**</sup><sup>_y_]</sup><sup>_⊤_</sup><br>[_ct,L, ct,R_]<sup>_⊤_</sup>|6<br>2|
||Hand positions|[**p**<sup>_h_</sup><br>_t,R_<sup>_,_</sup> <sup>**p**</sup><sup>_h_</sup><br>_t,L_<sup>]</sup><sup>_⊤_</sup><br><br>|[**p**<sup>_h_</sup><br>_t,L _<sup>_⊙_</sup><sup>**_s_**</sup><sup>_y,_</sup> <sup>**p**</sup><sup>_h_</sup><br>_t,R _<sup>_⊙_</sup><sup>**_s_**</sup><sup>_y_]</sup><sup>_⊤_</sup><br><br>|6|
||Foot positions<br>Base height map|[**p**<sup>_f_</sup><br>_t,R_<sup>_,_</sup> <sup>**p**</sup><sup>_f_</sup><br>_t,L_<sup>]</sup><sup>_⊤_</sup><br>**H**<sup>_b_</sup><br>_t_<br><br>|[**p**<sup>_f_</sup><br>_t,L _<sup>_⊙_</sup><sup>**_s_**</sup><sup>_y,_</sup> <sup>**p**</sup><sup>_f_</sup><br>_t,R _<sup>_⊙_</sup><sup>**_s_**</sup><sup>_y_]</sup><sup>_⊤_</sup><br>_M_2D**H**<sup>_b_</sup><br>_t_<br><br>|6<br>18_×_10|
||Foot height maps|(**H**<sup>_f_</sup><br>_t,R_<sup>_,_</sup> <sup>**H**</sup><sup>_f_</sup><br>_t,L_<sup>)</sup>|(_M_2D**H**<sup>_f_</sup><br>_t,L_<sup>_, M_2D</sup><sup>**H**</sup><sup>_f_</sup><br>_t,R_<sup>)</sup>|2_×_10_×_5|
|||**Actio**|**n a**_t_||
|_Ma_|Action|**a**_t_|_F_(**a**_t_)|21|


Table 12: Component-wise mirror rules used in the data augmentation procedure for proprioceptions, latent representations, actor observations, privileged states, and actions. 

17 

Next, we analyze the structure of the encoder inputs and define the corresponding mirror operators used in the proofs in Appendix B.2. Because mirror equivariance is implemented through modules with explicitly paired left-right channels, their inputs must share the same symmetry-structured form. In our setting, this form is obtained by organizing the features into paired left and right channels. We describe this construction below for temporal proprioceptive and image inputs. 

We first consider the temporal proprioception **o**<sup>_p_</sup> _t−h_ +1: _t_<sup>.Thisrepresentationdoesnotexplicitly</sup> separate the left and right sides. We therefore introduce a fixed reorganization operator _T_ that maps the length- _h_ proprioceptive history into a symmetry-structured left-right representation: 


Each branch is constructed by concatenating the corresponding per-frame slices over the past _h_ time steps. The definitions of the per-frame slices ¯ **o**<sup>_p_</sup> _t−k,L_<sup>and ¯</sup><sup>**o**</sup><sup>_p_</sup> _t−k,R_<sup>, for</sup><sup>_k∈{_0</sup><sup>_, . . . , h−_1</sup><sup>_}_, are listed in</sup> Table 13. Under this reorganization, the mirror transformation reduces to simple branch exchange: 

|||_Mc_<br>�¯**o**_p_<br>_t_<br>�|= [¯**o**<sup>_p_</sup><br>_t,R_<sup>_,_ ¯</sup><sup>**o**</sup><sup>_p_</sup><br>_t,L_<sup>]</sup><sup>_⊤._</sup>|(8)|
|---|---|---|---|---|
|**Component**|**Left slice**¯**o**<sup>_p_</sup><br>_t−_|_k,L_|**Right slice**¯**o**<sup>_p_</sup><br>_t−k,R_|**Dim.**|
|Base angular velocity|**_ω_**_t−k_||**_ω_**_t−k ⊙_**_s_**_ω_|3|
|Gravity vector|**g**_t−k_||**g**_t−k ⊙_**_s_**_y_|3|
|Velocity command<br>Joint angles|**u**_t−k_<br>[**_θ_**<sup>leg</sup><br>_t−k,L_<sup>_,_</sup> <sup>**_θ_**arm</sup><br>_t−k,L_<sup>_,_</sup>|<sup>_θ_waist</sup><br>_t−k_ <sup>]</sup><sup>_⊤_</sup>|**u**_t−k ⊙_**_s_**_u_<br>[**_θ_**<sup>leg</sup><br>_t−k,R _<sup>_⊙_</sup><sup>**_s_**leg</sup><sup>_,_</sup> <sup>**_θ_**arm</sup><br>_t−k,R _<sup>_⊙_</sup><sup>**_s_**arm</sup><sup>_, −θ_waist</sup><br>_t−k_ <sup>]</sup><sup>_⊤_</sup>|3<br>11|
|Joint angular velocities|[<sup>˙</sup>**_θ_**<sup>leg</sup><br>_t−k,L_<sup>_,_ ˙</sup><sup>**_θ_**arm</sup><br>_t−k,L_<sup>_,_</sup>|<sup>˙</sup><sup>_θ_waist</sup><br>_t−k_ <sup>]</sup><sup>_⊤_</sup>|[<sup>˙</sup>**_θ_**<sup>leg</sup><br>_t−k,R _<sup>_⊙_</sup><sup>**_s_**leg</sup><sup>_,_ ˙</sup><sup>**_θ_**arm</sup><br>_t−k,R _<sup>_⊙_</sup><sup>**_s_**arm</sup><sup>_, −_˙</sup><sup>_θ_waist</sup><br>_t−k_ <sup>]</sup><sup>_⊤_</sup>|11|
|Previous action|[**a**<sup>leg</sup><br>_t−k−_1_,L_<sup>_,_</sup> <sup>**a**arm</sup><br>_t−k−_1_,_|_L_<sup>_, a_waist</sup><br>_t−k−_1<sup>]</sup>|<sup>_⊤_</sup><br>[**a**<sup>leg</sup><br>_t−k−_1_,R _<sup>_⊙_</sup><sup>**_s_**leg</sup><sup>_,_</sup> <sup>**a**arm</sup><br>_t−k−_1_,R _<sup>_⊙_</sup><sup>**_s_**arm</sup><sup>_, −a_waist</sup><br>_t−k−_1<sup>]</sup><sup>_⊤_</sup>|11|


Table 13: Per-frame left and right slices used by the reorganization operator _T_ . 

We then consider the image input **I** _t_ . Images naturally exhibit a left-right spatial structure. We therefore use the horizontal reflection operator _M_ 2D for two-dimensional vectors. For **Y** _∈_ R<sup>_H×W_</sup> , including an image or any image-derived representation, _M_ 2D acts along the width dimension and performs a horizontal flip: 


Although an image already has a left-right spatial structure, it does not directly provide paired leftright channels along the channel dimension. To address this issue, we introduce a lift convolution layer in the equivariant CNN (Appendix B.2), which lifts the input image to a symmetry-structured feature representation with explicitly paired left and right channels. 

### **B.2 Equivariance Proofs for Network Components** 

To construct an encoder that satisfies the desired equivariance property, we design each module as an equivariant network. These modules include equivariant MLPs, equivariant GRUs, and an equivariant CNN, which can in turn be decomposed into compositions of equivariant linear and convolutional layers. In this section, we first present the construction and properties of these equivariant network components and provide the corresponding proofs. We then use these results to establish the equivariance of each latent head in the encoder of Sec. 3.3. 

**Equivariant Linear Layer** An equivariant linear layer has the same affine form as a standard linear layer, but its weight matrix and bias are constrained to follow a symmetry-preserving block structure. We define _f_ : R<sup>2</sup><sup>_C_in</sup> _→_ R<sup>2</sup><sup>_C_out</sup> as 


Here, **x** _∈_ R<sup>2</sup><sup>_C_in</sup> is the symmetry-structured input feature vector, _A, B ∈_ R<sup>_C_out</sup><sup>_×C_in</sup> are learnable weight blocks, and **a** _∈_ R<sup>_C_out</sup> is the shared bias. **Proposition B.1.** _The linear layer f is Mc-equivariant:_ 


18 

_Proof._ Direct substitution yields 


**Equivariant MLP** The equivariant MLP follows the standard MLP form, except that each linear layer is replaced with an equivariant linear layer _fℓ_ : 


where _σ_ denotes the activation function. 

**Proposition B.2.** _The equivariant MLP F_ MLP _is Mc-equivariant:_ 


_Proof._ Let 


By Proposition B.1, each equivariant linear layer _fℓ_ commutes with _Mc_ . Since _σ_ is applied elementwise, it also commutes with _Mc_ . Hence every _Gℓ_ is _Mc_ -equivariant. Because a composition of equivariant maps is equivariant, 


also satisfies 


= **Equivariant GRU** The equivariant GRU follows the standard update rule, with **h** _t F_ GRU( **x** _t,_ **h** _t−_ 1), where all affine transformations use the same block-structured parameterization as the equivariant linear layer: 


Here, **x** _t ∈_ R<sup>2</sup><sup>_C_in</sup> denotes the input feature at time _t_ ; **h** _t−_ 1 and **h** _t_ are the previous and updated hidden states in R<sup>2</sup><sup>_C_h</sup> , and **r** _t_ , **z** _t_ , and **n** _t_ denote the reset gate, update gate, and candidate hidden state, respectively. 

**Proposition B.3.** _The one-step GRU update is equivariant under channel exchange:_ 


_Proof._ By Proposition B.1, all affine maps in the GRU update commute with _Mc_ . Since _σ_ , tanh, subtraction from **1** , and the Hadamard product are all pointwise operations, they also commute with _Mc_ . Therefore 


For the candidate hidden state, 


Hence 


19 

**Equivariant Convolution Layer** We define the equivariant convolutional layers using crosscorrelation and symmetry-constrained kernels. For an input feature map **x** _∈_ R<sup>_C_in</sup><sup>_×H×W_</sup> , let **x** ¯ _∈_ R<sup>_C_in</sup><sup>_×_</sup> _H_<sup>¯</sup> _×W_<sup>¯</sup> denote its padded version, where _H_ ¯ = _H_ + 2 _pH_ and _W_ ¯ = _W_ + 2 _pW_ . Given a convolution kernel **k** _∈_ R<sup>_C_out</sup><sup>_×C_in</sup><sup>_×KH×KW_</sup> , we define cross-correlation with stride _s_ as 


Here, _h_ =1 _, . . . , Ho_ and _w_ =1 _, . . . , Wo_ , where _Ho_ = _⌊_ ( _H_<sup>¯</sup> _−KH_ ) _/s⌋_ +1 and _Wo_ = _⌊_ ( _W_<sup>¯</sup> _−KW_ ) _/s⌋_ +1. When _s>_ 1, we assume _W_<sup>¯</sup> _−KW_ is divisible by _s_ so that horizontal sampling grid remains aligned under flipping. To describe mirror equivariance in the spatial domain, we define the horizontal flip operator on padded feature maps and kernels as 


An ordinary image does not explicitly contain paired symmetry channels. We therefore use a lift convolution to map it to a symmetry-structured representation: 


Here, **k** l _∈_ R<sup>_C_out</sup><sup>_×C_in</sup><sup>_×KH×KW_</sup> is a learnable kernel, and **a** l _∈_ R<sup>_C_out</sup> is a shared bias. After lifting, the subsequent layers preserve the symmetry-structured representation through constrained kernels. Each non-lift convolution is defined as 


Here, **x**<sup>(1)</sup> _,_ **x**<sup>(2)</sup> _∈_ R<sup>_C_in</sup><sup>_×H×W_</sup> are the two symmetry branches, **k** a _,_ **k** b _∈_ R<sup>_C_out</sup><sup>_×C_in</sup><sup>_×KH×KW_</sup> are learnable kernels, and **a** nl _∈_ R<sup>_C_out</sup> is a shared bias. 

**Lemma B.4.** _Cross-correlation satisfies_ 


_Proof._ For the left-hand side, 


For the right-hand side, substituting _v_<sup>_′_</sup> = _KW_ + 1 _− v_ gives 


Using _Wo_ = _<u>W</u>_ ¯ _−sKW_ + 1 and the alignment assumption, the last index equals 


so the two expressions coincide. 

**Proposition B.5.** _The lift convolution satisfies_ 


_Proof._ By Lemma B.4, 


Hence 


20 

**Proposition B.6.** _The non-lift convolution satisfies_ 


_Proof._ Let 


Then 

Using Lemma B.4, 


**Equivariant CNN** The equivariant CNN is constructed by composing the layer-wise equivariant convolutions defined above. It consists of one lift convolution _f_ l followed by _N −_ 1 non-lift convolutions _f_ nl<sup>_i_:</sup> 


Let _F_ CNN( **x** ) _∈_ R<sup>2</sup><sup>_CN×HN×WN_</sup> denote the output feature map of the equivariant CNN, where _HN_ and _WN_ are its spatial height and width. 

**Proposition B.7.** _The equivariant CNN satisfies_ 


_Proof._ Let 


By Proposition B.5, the lift convolution is _T_ -equivariant. By Proposition B.6, each non-lift convolution is also _T_ -equivariant. Since _σ_ is applied element-wise, it commutes with both channel exchange and horizontal flipping, and hence with _T_ . Therefore every layer in the composition defining _F_ CNN is _T_ -equivariant. By closure under composition, 


**Corollary B.8.** _If the output feature map has spatial resolution_ 1 _×_ 1 _, then_ 


**Theorem B.9.** _Let Eϕ_<sup>(</sup><sup>_k_)</sup><sup>_, k∈{f, b, p}denotethemappingfromthesymmetry-structuredpropri-_</sup> _oception_ **o** ¯<sup>_p_</sup> _t_<sup>_andtheimage_</sup><sup>**I**</sup><sup>_ttothek-thlatenthead_</sup><sup>**z**ˆ</sup><sup>_k_</sup> _t_<sup>_intheencoderusedinSec.3.3.Then_</sup> _each latent head is equivariant under the joint action of channel exchange on proprioception and horizontal reflection on images:_ 


_where Mc denotes the mirror operator acting on the k-th latent head._ 

_Proof._ The encoder in Sec. 3.3 consists of an equivariant proprioceptive MLP, an equivariant visual CNN, a GRU applied to their concatenated features, a fusion MLP, and the _k_ -th latent head. 

First, the proprioceptive branch is implemented by equivariant MLPs. By Proposition B.2, each such MLP is _Mc_ -equivariant. Hence the proprioceptive feature transforms equivariantly under channel exchange. 

21 

Second, the visual branch is implemented by an equivariant CNN. By Proposition B.7, the CNN satisfies 


For the architecture used in this work, the output spatial resolution is 1 _×_ 1. Hence, by Corollary B.8, the visual feature produced by the CNN satisfies 


Next, let _⊕_ denote feature concatenation along the symmetry-structured channel dimension. Since both proprioceptive and visual features transform under the same channel-exchange operator, concatenation preserves equivariance: 


The concatenated feature is then processed by the GRU. By Proposition B.3, the GRU is _Mc_ - equivariant. Its output is further mapped by the fusion MLP, which is also _Mc_ -equivariant by Proposition B.2 _._ 

Finally, the fused feature is mapped to the _k_ -th latent head by an equivariant head mapping. By Proposition B.2, this mapping is equivariant with respect to _Mc_ on both its input and output. Combining the equivariance of the proprioceptive MLP, the visual CNN, the feature concatenation, the GRU, the fusion MLP, and the final head yields 


This completes the proof. 

## **C Efficient Depth Rendering with Self-Occlusion** 

To synthesize depth observations consistent with deployment-time sensing, we ray-cast against both the static terrain mesh and the robot’s dynamic link meshes. A naive implementation would update dynamic mesh poses and repeatedly refit the corresponding ray-query acceleration structures, such as bounding volume hierarchies (BVHs), at every simulation step, which quickly becomes a bottleneck in massively parallel training. To avoid this overhead, we keep each mesh in its local frame and instead transform each camera ray from the world frame into the queried mesh frame before raymesh intersection. Because these transformations are rigid, hit distances remain directly comparable across meshes. This yields an efficient depth renderer with self-occlusion, implemented in NVIDIA Warp [50], for large-scale GPU-parallel simulation. The procedure is summarized in Algorithm 1. 

**Algorithm 1: Efficient Depth Rendering with Self-Occlusion** 

**Require:** terrain mesh _M_<sup>ter</sup> with pose ( **p**<sup>ter</sup> _,_ **R**<sup>ter</sup> ); per-link meshes _{M_<sup>_ℓ_</sup> _j_<sup>_}Nℓ_</sup> _j_ =1<sup>with per-env link poses</sup><sup>_{_(</sup><sup>**p**</sup><sup>_ℓ_</sup> _j,e_<sup>_,_</sup><sup>**R**</sup><sup>_ℓ_</sup> _j,e_<sup>)</sup><sup>_}_; per-env</sup> camera poses _{_ ( **p**<sup>cam</sup> _e ,_ **R**<sup>cam</sup> _e_ ) _}_<sup>_N_</sup> _e_ =1<sup>env; half-FoV tangents (tan</sup><sup>_x,e,_tan</sup><sup>_y,e_); depth bounds (</sup><sup>_d_min</sup><sup>_, d_max).</sup> **Ensure:** clipped camera-depth maps **D** _∈_ R<sup>_N_env</sup><sup>_×H×W_</sup> . _▷ Parallel mesh-based occluder rendering with one thread per pixel_ 1: **for each** pixel ( _e, h, w_ ) _∈_ [ _N_<sup>env</sup> ] _×_ [ _H_ ] _×_ [ _W_ ] **in parallel do** 2: Image-plane ray coordinates: _tx ←_ �2( _w −_<sup><u>1</u></sup> 2<sup>)</sup><sup>_/W−_1</sup> � tan _x,e, ty ←_ �2( _h −_ 2<sup><u>1</u>)</sup><sup>_/H−_1</sup> � tan _y,e_ 3: World frame ray origin: **o** _←_ **p**<sup>cam</sup> _e_ 4: World frame ray direction: **d** _←_ Normalize�Rot( **R**<sup>cam</sup> _e ,_ [ _tx, ty, −_ 1]<sup>_⊤_</sup> )� 5: Terrain frame ray: ( **o**<sup>ter</sup> _,_ **d**<sup>ter</sup> ) _←_ Transform<sup>_−_1�</sup> ( **p**<sup>ter</sup> _,_ **R**<sup>ter</sup> ) _,_ ( **o** _,_ **d** )� 6: Terrain hit distance: _t_<sup>ter</sup> _←_ RayQuery( _M_<sup>ter</sup> _,_ **o**<sup>ter</sup> _,_ **d**<sup>ter</sup> ) 7: Initialize nearest self-occlusion distance: _t_<sup>occ</sup> _←_ + _∞_ 8: **for** _j_ = 1 **to** _N_<sup>_ℓ_</sup> **do** 9: Link frame ray: ( **o**<sup>_ℓ_</sup> _j_<sup>_,_</sup><sup>**d**</sup><sup>_ℓ_</sup> _j_<sup>)</sup><sup>_←_Transform</sup><sup>_−_1�</sup> ( **p**<sup>_ℓ_</sup> _j,e_<sup>_,_</sup><sup>**R**</sup><sup>_ℓ_</sup> _j,e_<sup>)</sup><sup>_,_(</sup><sup>**o**</sup><sup>_,_</sup><sup>**d**)</sup> � 10: Link hit distance: _t_<sup>_ℓ_</sup> _j_<sup>_←_RayQuery(</sup><sup>_Mℓ_</sup> _j_<sup>_,_</sup><sup>**o**</sup><sup>_ℓ_</sup> _j_<sup>_,_</sup><sup>**d**</sup> _j_<sup>_ℓ_)</sup> 11: _t_<sup>occ</sup> _←_ min( _t_<sup>occ</sup> _, t_<sup>_ℓ_</sup> _j_<sup>)</sup> 12: **if** _t_<sup>occ</sup> _≤ d_ min **then break** 13: **end for** 14: Convert ray distance to camera _z_ -depth: _c ←_ (1 + _t_<sup>2</sup> _x_<sup>+</sup><sup>_t_2</sup> _y_<sup>)</sup><sup>_−_1</sup><sup>_/_2</sup> 15: **D** [ _e, h, w_ ] _←_ clamp� _c ·_ min( _t_<sup>ter</sup> _, t_<sup>occ</sup> ) _, d_ min _, d_ max� 16: **end for** 

- 17: **return D** 

22 

## **D Real-World Deployment Details** 

|**Joint Name**|_Kp _|_Kd_|**Action Scale**|
|---|---|---|---|
|Hip pitch|120|4|0.25|
|Hip yaw|100|2|0.25|
|Hip roll|100|2|0.25|
|Knee|120|4|0.25|
|Ankle pitch|40|2.0|0.25|
|Ankle roll|20|1.0|0.25|
|Waist yaw|100|3|0.2|
|Shoulder pitch|30|1|0.2|
|Shoulder roll|30|1|0.2|
|Shoulder yaw|30|1|0.2|
|Elbow|30|1|0.2|


We deploy our policy on the AgiBot X2 humanoid robot, which has 29 joints, stands 1.31 m tall, and weighs approximately 39 kg. A forward-facing Intel RealSense D435i depth camera is mounted at the waist and pitched downward by 50<sup>_◦_</sup> relative to the horizontal plane. The camera provides horizontal and vertical fields of view of 87<sup>_◦_</sup> and 58<sup>_◦_</sup> , respectively. Raw 640 _×_ 360 depth images are filtered, downsampled, and holefilled using the Intel RealSense SDK, and then cropped to a resolution of 36 _×_ 36 before being fed into the policy. Depth observations are streamed to the controller at 60 Hz. 

For onboard execution, we establish a 1 kHz communication pipeline between the motion control unit (RK3588) and the Table 14: Joint-wise deployment gains and action scales. inference unit (Jetson AGX Orin) via lightweight ROS 2 topicbased messaging. Policy inference runs with ONNX Runtime at 50 Hz and outputs target joint positions for all 21 policy-controlled joints. During deployment, each actuated joint is assigned an individual proportional gain _Kp_ , derivative gain _Kd_ , and action scale, as summarized in Table 14. 

## **E Cross-Platform Validation** 

|**Terrain**|**Settings**|**Success Rate**|
|---|---|---|
|Stairs Up|15 / 40 cm|100.0% (20/20)|
|Stairs Down|15 / 40 cm|100.0% (20/20)|
|Gap|80 cm|100.0% (20/20)|
|Platform|45 cm|95.0% (19/20)|


To evaluate the generalizability of SSR across different robotic **Terrain Settings Success Rate** platforms, we conduct a cross-platform validation on the fullStairs Up 15 / 40 cm 100.0% (20/20) size DEEP Robotics DR02 humanoid. We retain the same Stairs Down 15 / 40 cm 100.0% (20/20) training and deployment pipeline used for the primary platGap 80 cm 100.0% (20/20) form, AgiBot X2, without introducing any platform-specific Platform 45 cm 95.0% (19/20) algorithmic changes. Compared with AgiBot X2, DR02 difTable 15: Cross-platform real-world fers substantially in physical scale and dynamics, standing at lab-level traversal performance on roughly 1.8 m tall and weighing around 70 kg. Despite these DEEP Robotics DR02. Success rates embodiment differences, SSR can be instantiated effectively are computed over 20 trials per terrain. on the new platform. As reported in Table 15 and illustrated in Fig. 11, the policy achieves high success rates across representative lab-level terrains, while maintaining precise foothold placement and coordinated, natural whole-body motion. These results indicate that SSR is not tightly coupled to a specific hardware configuration and exhibits promising cross-platform applicability across distinct humanoid embodiments. 


Figure 11: Key frames of cross-platform laboratory deployment on the full-size DEEP Robotics DR02 humanoid. The SSR policy successfully traverses stairs, an 80 cm gap, and a 45 cm platform, demonstrating its cross-platform generalization. 

23 

