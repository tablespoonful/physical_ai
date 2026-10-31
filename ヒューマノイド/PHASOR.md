---
title: "PHASOR: Phase-Anchored Universal Action Representations for Humanoid Embodiments"
date: "2026-06-01"
authors: "Kihyun Kim; Chaeyun Kim; Jongho Shin; Taeyoun Kwon; Junghyun Kim; Mijin Koo"
url: https://arxiv.org/abs/2606.01851
pdf: https://arxiv.org/pdf/2606.01851
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.01851)** / [論文ページ](https://arxiv.org/abs/2606.01851)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **PHASOR: Phase-Anchored Universal Action Representations for Humanoid Embodiments** 

**Kihyun Kim**<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> **Chaeyun Kim**<sup>1</sup><sup>_,_2</sup><sup>_∗†_</sup> **Jongho Shin**<sup>3</sup> **Taeyoun Kwon**<sup>2</sup><sup>_,_4</sup> **Junghyun Kim**<sup>2</sup><sup>_,_5</sup> **Mijin Koo**<sup>1</sup><sup>_,_2</sup> **Haon Park**<sup>1</sup><sup>_,_2</sup><sup>_†_</sup> 1AIM Intelligence 2Seoul National University 3LG Electronics 4MAUM AI 5OpenMind 

**Abstract:** Learning a good action embedding space is fundamental to scalable robot policy learning, yet existing methods treat action latents as task-specific intermediates rather than first-class representations. The resulting latents are unstructured, embodiment-specific, and weakly tied to motion semantics, limiting interpretability, controllability, and transferability across robots. We position the action embedding space itself as a first-class design target, with downstream policy quality emerging from representation quality. Exploiting motion’s intrinsic periodicity, we factorize it into a phase manifold that captures cyclic structure via FFT-parametric coefficients, together with a pose branch that conditions the manifold on non-periodic configuration detail. Combined with motion-semantic distillation, this factorized structure yields a cross-embodiment motion manifold that is interpretable and embodiment-agnostic by design. Anchoring multiple humanoid robots to a shared human-pretrained manifold then produces a unified action embedding space across diverse platforms, achieving strong cross-embodiment retrieval and consistent gains on downstream robot tasks. 

**Keywords:** Action Latent, Cross-Embodiment, Phase Manifold, Humanoid 

### **1 Introduction** 

The rapid diversification of humanoid robot platforms has created a pressing need for action representations that generalize across embodiments. Modern robot policies, from vision-language-action models [1, 2, 3] to diffusion-based controllers [4, 5], all build on learned action spaces as the intermediate signal between perception and motor execution. In cross-embodiment settings, this space becomes the primary bridge through which knowledge transfers from one body to another, making its quality a bottleneck for generalization. 

Yet current action encoders [6, 7, 8, 9, 10] treat motion as a generic sequence of per-frame joint states, with no motion-specific structure. This leads to two failures. First, the representation entangles with the morphology of the training robot, so the same behavior on a different humanoid maps to a disjoint region and cannot transfer. Second, the latent space lacks temporal organization, and proximity within it does not reflect proximity in time. Thus its dimensions carry no interpretable meaning, leaving trajectories hard to analyze or control. 

To overcome these limitations, we exploit the intrinsic physical structure of motion. Unlike text or images, motion is fundamentally a superposition of periodic components. During walking, the legs oscillate at roughly 1 Hz, the arms swing in antiphase, and the trunk rotates more slowly. Decomposing motion into amplitude, frequency, and phase shift [11] separates two quantities that unstructured encoders conflate. Phase encodes _where in the action_ the body is, while amplitude and frequency encode _what action_ is performed. We hypothesize that this **periodic structure is intrinsic** to the behavior rather than to the body that produces it, and can therefore **serve as a shared substrate for aligning** action embeddings across robots [12]. 

> _∗_ Equal contribution. _†_ Corresponding author. 

Realizing this phase manifold as a cross-embodiment action space requires solving two problems. First, existing approaches [11, 12, 13, 14] compress the whole body into a single representation, blurring the distinct periodicities of individual joints. We instead decompose the phase encoding by body part, preserving each limb’s periodic signature as a natural unit of correspondence across kinematics. Second, encoding motion through velocity alone captures how the body moves but not where it is; so motions with similar oscillation but different poses (e.g., upright vs. crouched walking) collapse to nearby points. We resolve this with a separate pose stream that supplies nonperiodic context to the decoder, leaving **P** ( _τ_ ) uncontaminated. 

With this clean manifold established, the remaining challenge is extending it across embodiments. Since periodic structure belongs to the behavior rather than the skeleton, and human data far outnumbers fragmented robot data, we anchor the shared manifold in human motion. Here, each new robot joins through a lightweight adapter rather than relearning the manifold from scratch. 

We propose **PHASOR** ( **PH** ase **A** ction **S** pace for cross-emb **O** diment **R** epresentation), a framework built on the periodic structure of motion. A per-body-part phase encoder extracts periodic parameters from joint velocities to assemble a phase manifold **P** ( _τ_ ), while a complementary pose branch supplies non-periodic context through FiLM [15] without leaking into **P** ( _τ_ ). The human-pretrained encoder acts as a shared anchor, and each robot joins through a lightweight adapter. An alignment head then projects per-embodiment manifolds onto a unit sphere and pulls semantically equivalent motions together, guided by a pretrained semantic motion prior [16]. 

We validate this design on one human and four humanoid robots along two axes, **_embedding quality_** and **_downstream utility_** . The phase manifold yields a tightly aligned cross-embodiment space, reaching over 88% cross-embodiment retrieval accuracy and surpassing unstructured and quantized baselines. As a learned representation, it further improves motion imitation, teleoperation, and reinforcement learning, confirming that motion-intrinsic periodicity is an effective design prior. 

Our contributions are: 

1. We propose the **phase manifold as a design prior** for cross-embodiment action embedding, where per-body-part parameters yield an interpretable and controllable action space. 

2. We introduce a **human-anchored multi-embodiment alignment strategy** that extends a frozen phase oracle to four robots through lightweight adapters. 

3. Our structured embedding delivers **downstream gains** in motion imitation and teleoperation, with **strong cross-embodiment retrieval** . 

### **2 Related Works** 

**Latent Action Representations for Robot Policy.** Modern robot policies learn an action representation that mediates between observation and motor command, formulating this space through autoregressive tokenization [1, 10, 8, 3], diffusion and flow-matching denoising [4, 2], or structured latents from video reconstruction [6, 9, 17] and discrete codebooks [7, 18, 5]. These treat motion as an unstructured sequence, overlooking the periodic, morphology-invariant nature of humanoid movement. We instead build the action embedding around the periodic structure of motion. 

**Periodic Representations in Motion.** Phase compactly describes where a behavior lies within a periodic cycle. Early methods modulated network weights from foot-contact heuristics [19], later extended to multi-contact and limb-specific phases [20, 21, 22], and unsupervised approaches learned multi-dimensional phase manifolds via FFT bottlenecks [11], extending to style modulation and inbetweening [23, 24]. Recent work applies phase to human-quadruped alignment [12], functional autoencoders [14], per-body-part control [25], and periodic skill discovery [26]. Yet all remain confined to character animation, never used as action representations for humanoid robots or as a substrate for cross-embodiment alignment. 

**Humanoid Cross-Embodiment Transfer.** Humanoid transfer can be grouped by alignment mechanism. Kinematic retargeting maps reference motion to a target body via inverse kinematics or interaction-aware optimization, yielding training data but no shared representation [27, 28, 29, 30, 

2 


Figure 1: **Structural gaps of PAE. (a,b)** Whole-body ( _A, F_ ) conflates distinct motions (walk vs. wave), which per-part features resolve. **(c)** Velocity-based ( _A, F_ ) ignores posture difference. 

31]. Shared-latent approaches instead project motions into a common space via contrastive learning on extrinsic kinematics [32, 33], scaled by per-part embeddings [34], or unified through differentiable retargeting [35], visual transfer [36, 37, 38], and language-guided features [39, 40, 41]. All rest on per-frame similarity over extrinsic or task-specific features, with no motion-intrinsic structure. We instead align heterogeneous robots on a structured, physically meaningful phase manifold. 

### **3 Preliminary: Periodic Motion Decomposition** 

**Periodic Autoencoder (PAE).** Given a motion window **X** _∈_ R<sup>_D×T_</sup> , a 1D convolutional encoder _g_ produces _M_ latent channels **L** = _g_ ( **X** ) _∈_ R<sup>_M×T_</sup> , and an FFT-based bottleneck fits each channel to a single sinusoid with amplitude _Ac_ , frequency _Fc_ , phase shift _Sc_ , and offset _Bc_ , trained end-to-end under a reconstruction loss so that each channel captures one locally periodic component. 


**Phase Manifold.** Each channel is projected onto an amplitude-scaled circle and stacked over channels to form a phase manifold **P** ( _τ_ ) = [ _m_ 1( _τ_ ); _. . ._ ; _mM_ ( _τ_ )] _∈_ R<sup>2</sup><sup>_M_</sup> 


a counter-clockwise trajectory on a product of circles. Here ( _Ac, Fc_ ) encodes _action identity_ (e.g., walking vs. running) while _Sc_ encodes _temporal position_ within action, so points close on **P** are both semantically similar and temporally aligned [11]. 

**Limitations for Cross-Embodiment Encoding.** Applied to the cross-embodiment setting, this formulation has two structural gaps (Fig. 1). First, the encoder compresses the whole body into _M_ shared channels, so parts moving at independent rhythms (e.g., arms waving while walking) collapse into a weighted mixture (Fig. 1.(a)), erasing the part-level periodicity that is the natural unit of crossembodiment correspondence (Fig. 1.(b)). Second, the encoding is velocity-based: it captures how the body moves but not where it is, so motions with similar ( _A, F_ ) but different posture map to nearby points (Fig. 1.(c)). We mitigate both gaps: **per-body-part encoding** recovers part-level periodicity, and **auxiliary pose branch** supplies static configuration without contaminating **P** ( _τ_ ). 

### **4 Method** 

We propose **PHASOR** , which learns a structured action embedding across one human and _K_ humanoid robots using periodic motion structure as its design prior. As shown in Fig. 2, motion is decomposed into a phase manifold **P** ( _τ_ ) that captures periodic dynamics and a complementary pose branch that captures non-periodic configuration. **P** ( _τ_ ) is the shared coordinate system for crossembodiment alignment, while the pose branch stays per-embodiment. We first build this embedding for a single embodiment (Sec. 4.1), then extend it across embodiments via a human-anchored scheme (Sec. 4.2), training in two stages: establish the human oracle, then align robots on top of it. 

3 


Figure 2: **Overview of PHASOR. (a)** A frozen human phase encoder, shared across embodiments via per-robot adapters, yields a morphology-invariant manifold **P** ( _τ_ ); a per-embodiment pose branch couples in only at the decoder via bidirectional FiLM. **(b)** Manifolds are projected onto _S_<sup>63</sup> and aligned by soft InfoNCE (LAMP prior) plus speed and shape consistency terms. 

#### **4.1 From Periodic Prior to Structured Action Manifold** 

**Task Definition.** We consider one human ( _JH_ =22 SMPL-H joints) and _K_ robots with joint counts _Jk_ . Each motion is a root-local window of _T_ =121 frames ( _≈_ 2 s, 60 fps), with joint velocity **v**<sup>joint</sup> _∈_ R<sup>_T ×_3</sup><sup>_J_</sup> , 6D joint rotation **R**<sup>joint</sup> _∈_ R<sup>_T ×_6</sup><sup>_J_</sup> , and root position **X**<sup>root</sup> _∈_ R<sup>_T ×_3</sup> , on normalized time _τ ∈_ [ _−_ 2 fps _T_<sup>_,_</sup> 2 fps _T_<sup>].Our goal is a phase manifold</sup><sup>**P**(</sup><sup>_τ_)</sup><sup>_∈_R</sup><sup>_T ×_2</sup><sup>_M_, paired with a complemen-</sup> tary pose code for non-periodic posture, such that semantically equivalent windows from different embodiments map to nearby trajectories on a shared coordinate system while staying interpretable and controllable per embodiment. 

#### **4.1.1 Per-Part Periodic Decomposition** 

A whole-body encoder conflates joints with independent rhythms (Sec. 3). We instead partition every embodiment into five kinematic parts _B_ = _{_ LA _,_ RA _,_ TK _,_ LL _,_ RL _}_ (left/right arm, trunk, left/right leg), each with its own phase encoder Φ _b_ and periodic bottleneck; per-embodiment joint-topart assignments follow kinematic role (Sec. A.1). For each part _b_ , Φ _b_ models the velocity signal **v** _b_ ( _τ_ ) as _Kb_ sinusoids, extracting ( _Ab,c, Fb,c, Bb,c_ ) via a differentiable FFT layer and _Sb,c_ via a regression head [11]. Channels are allocated by each part’s rhythmic complexity, _M_ = 16 in total. 


We then project every channel onto its amplitude-scaled circle via Eq. (2), now indexed by part as _mb,c_ ( _τ_ ) = _Ab,c_ [cos _ϕb,c_ ( _τ_ ) _,_ sin _ϕb,c_ ( _τ_ )], and concatenate over all ( _b, c_ ) to form the part-structured manifold **P** ( _τ_ ) _∈_ R<sup>_T ×_32</sup> ; a symmetric per-part decoder _Db_ reconstructs Eq. (3). Independent encoders Φ _b_ keep each part’s rhythmic signature free of cross-part contamination. 

#### **4.1.2 Complementary Pose Conditioning** 

Velocity-based phase lacks static postural context (e.g., crouching vs. standing), so we add a complementary pose branch that encodes 6D joint rotations and root positions into a compact token 

4 

sequence **z** pose _∈_ R<sup>_Lp×dp_</sup> ( _Lp_ =8, _dp_ =128), retaining only window-level postural configuration. The two branches interact exclusively at decoding via bidirectional FiLM [15]: phase context conditions pose decoding, while pose context modulates the reconstructed velocity signal before the phase decoder. Crucially, **P** ( _τ_ ) is constructed from FFT parameters _before_ any modulation, keeping the manifold pose-free and suitable as a clean cross-embodiment alignment target (Sec. 4.2). 

#### **4.2 Cross-Embodiment Alignment on the Phase Manifold** 

As the channels of **P** ( _τ_ ) carry rhythmic identity rather than morphology, we treat it as a shared coordinate system. Every robot is mapped onto the **_same_** manifold and aligned by semantic correspondence. We realize this by reusing the human-pretrained backbone as a frozen oracle and routing each robot through it with lightweight adapters. 

#### **4.2.1 Human-Anchored Encoder** 

Human data is abundant and behaviorally diverse while robot data is sparse, so we pretrain the backbone on human motion and freeze it as a **shared anchor** where every robot is aligned to. The per-part encoders _Eh_ = _{_ Φ _b}b∈B_ and the phase-to-pose FiLM head are frozen, fixing the channel semantics once so new robots join without representation drift. For robot _k_ , a linear input adapter _Er_<sup>_k_: R</sup><sup>_Dk→_R66 maps its joint velocities into the human input space, and the shared frozen encoder</sup> _EX ≡ Eh_ extracts the phase parameters: 


Robot joints use the same five-part partition (Sec. A.1). Since _EX_ is shared, all morphological variation is absorbed by the small adapter _Er_<sup>_k_, and</sup><sup>**P**</sup> _R_<sup>_k_(</sup><sup>_τ_) adheres to the human phase prior.</sup> 

#### **4.2.2 Decoder Adaptation and Pose Isolation** 

The decoder mirrors the encoder but allows controlled adaptation: the human phase decoder _Dh_ stays frozen, while robots share a phase decoder _DX_ initialized from _Dh_ and fine-tuned with perrobot output adapters _Dr_<sup>_k_: R66</sup><sup>_→_R</sup><sup>_Dk_.Because posture is morphology-dependent, each robot has</sup> its own pose branch supervised by reconstruction only, keeping morphology-specific detail out of the shared-manifold alignment. 

#### **4.2.3 Alignment Objective** 

All supervision acts on **P** ( _τ_ ), not on the pose branch, keeping the signal independent of kinematics. **Alignment head.** For latent alignment, we concatenate the phase manifold **P** ( _τ_ ) with a temporally pooled pose token **z**<sup>pool</sup> pose<sup>and project the result onto a</sup><sup>**unit sphere**via a lightweight head</sup><sup>_π_.</sup> 


The pose token is added to disambiguate motions that share the same rhythm but hold a different posture, which phase alone cannot tell apart. To keep alignment driven mainly by phase, the poserelated weights in _π_ are initialized near zero, so the head starts phase-only and brings in pose context gradually. Time-pooling _z_ ( _τ_ ) over a clip gives a clip-level descriptor _z_<sup>pool</sup> _∈S_<sup>63</sup> . 

**Hierarchical Pair Loss.** For each human-robot pair we use an InfoNCE objective whose target mixes the hard diagonal label with a soft target from a motion-semantic prior (LAMP [16]). 


The hard term anchors paired windows, while the LAMP term pulls together semantically similar motions that hard labels treat as negatives. We apply _T_<sup>mix</sup> at two granularities, per-window for **_fine_** motion variation and per-clip (mean-pooled _z_ within a clip) for **_coarse_** meaning, summing the symmetric cross-entropy of both into _L_ pair. 

5 

|||**H**|_→_**R**|||**R**|_→_**H**|||**R**|_→_**R**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Method|R@1|R@5|R@10|MRR|R@1|R@5|R@10|MRR|R@1|R@5|R@10|MRR|
|MLP [34,32]|79.9|96.5|98.8|87.1|79.8|97.5|99.3|87.4|74.7|95.0|98.2|83.5|
|VQ [6,5]|37.6|78.6|91.0|55.1|36.3|77.0|89.5|53.6|37.5|77.7|89.8|54.8|
|_(A) Alignment loss desig_|_n_||||||||||||
|Only Phase (zero-shot)|83.0|91.9|93.6|87.0|83.9|92.2|94.1|87.8|73.0|84.3|87.3|78.2|
|Hard only (no LAMP)|84.1|92.2|93.8|87.8|84.1|92.5|94.2|87.8|74.5|85.3|88.1|79.5|
|+Soft Coarse|84.9|92.7|94.3|88.5|85.1|93.0|94.6|88.6|76.1|86.4|88.9|80.7|
|+Soft Fine|85.6|93.4|94.9|89.1|85.7|93.7|95.2|89.1|77.2|87.1|88.6|81.6|
|+Soft Coarse+Fine|86.9|94.3|95.8|89.9|87.2|94.8|96.3|90.2|79.3|89.6|91.8|83.7|
|_(B) Alignment target_ (lo|ss=S|oft Coa|rse+Fi|ne)|||||||||
|_π_(**P**_τ ∥_**X**root)|88.5|96.0|97.2|91.9|89.5|96.5|97.5|92.6|81.0|91.7|93.9|85.8|
|_π_(**P**_τ ∥_**z**pose)**(Ours)**|**90.3**|**98.3**|**99.2**|**93.9**|**90.5**|**98.6**|**99.4**|**94.1**|**84.8**|**96.4**|**98.3**|**90.0**|


Table 1: **Cross-embodiment retrieval and PHASOR ablation.** Each query has one positive, the temporally identical chunk from another embodiment (R _→_ R over �24�=6 pairs, %). **(A)** varies the loss at a fixed target, adding LAMP soft targets at the **_coarse_** clip, **_fine_** window, and **_both_** levels. **(B)** varies the head input at the best loss, **X** root vs. our pooled **z** pose. **Bold** best, underline second. 

**Trajectory Consistency.** Two lightweight geometric penalties regularize the temporal shape of _z_ ( _τ_ ): _L_ speed matches per-frame step size on the sphere (implicit frequency synchronization) and _L_ shape matches half-period distance (implicit amplitude synchronization). The full alignment loss is _L_ align =<sup>�</sup> _k_ � _L_<sup>(</sup> pair<sup>_k_)+</sup><sup>_λ_speed</sup><sup>_L_(</sup> speed<sup>_k_)+</sup><sup>_λ_shape</sup><sup>_L_(</sup> shape<sup>_k_)</sup> �. 

#### **4.2.4 Training** 

We optimize the framework in two continuous phases. We first pretrain the human backbone with a per-part velocity reconstruction loss _L_ phase, a pose reconstruction loss _L_ pose, and a forwardkinematics consistency loss _L_ FK that geometrically links the two branches. We then freeze the human oracle and jointly train the robot components (input/output adapters, shared phase decoder _DX_ , per-robot pose branches, and alignment head _π_ ) under Eq. (7). 


A short reconstruction-only warm-up precedes alignment, so each **P** _Rk_ stabilizes before contrastive supervision begins. Full details are provided in Sec. A.6. 

### **5 Experiments** 

We evaluate PHASOR along two axes. **_Embedding quality_** asks whether the phase manifold yields an interpretable, cross-embodiment-aligned action space (Sec. 5.1), and **_downstream utility_** asks whether that embedding produces concrete gains once frozen and plugged into robot policy learning (Sec. B.3). In every downstream evaluation the phase encoder stays frozen and only a lightweight policy head is trained, so any performance gap comes from representation quality alone. 

**Data.** We use 12,616 clips ( _∼_ 40.4 h, 8.7 M frames at 60 fps) from AMASS CMU and KIT, each retargeted with GMR to four humanoids, Unitree G1 (32 DOF), H1.2 (28 DOF), Booster T1 (24 DOF), and Berkeley Humanoid Lite (25 DOF), yielding 50,464 synchronized human-robot pairs. Every experiment uses a 121-frame chunk ( _∼_ 2 s). 

**Baselines.** We compare two cross-embodiment embedding strategies. **MLP** [34, 32] projects perembodiment features into 80D with a segment-wise MLP under InfoNCE, a contrastive baseline with no structural prior. **VQ** [6, 5] encodes motion into a 10D discrete codebook via cross-reconstruction, isolating discrete quantization against our periodic prior. As objectives vary across quantizer-based methods, we use a representative codebook variant so the comparison reflects quantization itself. 

6 


Figure 3: **Left.** 2D PCA of the alignment embedding _z_ (top) and phase manifold **P** ( _τ_ ) (bottom). Same clip across the human and four robots overlaps tightly (col. 1), while G1 separates four motion types (walk, run, jump, kick) by orbit radius and position (col. 2). **Right.** Phase shifts ∆ _S_ on a running clip yield predictable temporal offsets, each row at a different gait phase. 

#### **5.1 Embedding Quality** 

#### **5.1.1 Cross-Embodiment Retrieval** 

We measure alignment with chunk retrieval. From 100 held-out clips we sample 20 non-overlapping 121-frame chunks each and query the gallery of a different embodiment, where each query has one positive, the temporally identical chunk. We report Recall@ _k_ and Mean Reciprocal Rank (MRR) over three directions, Human _→_ Robot (H _→_ R), Robot _→_ Human (R _→_ H), and Robot _→_ Robot (R _→_ R, averaged over all �24�=6 pairs). 

**Baselines.** MLP reaches reasonable exact-match scores since its objective directly optimizes perframe discrimination, whereas VQ performs far worse, as its codebook maps adjacent chunks to the same code and collapses the fine-grained distinctions retrieval needs. 

**(A) Alignment loss.** Applied to robots without cross-embodiment training, the frozen human-only manifold ( _Only Phase_ ) already beats MLP on H _→_ R (83.0 vs. 79.9 R@1), confirming a strong morphology-invariant temporal prior. Cross-embodiment InfoNCE ( _Hard only_ ) improves every direction, and LAMP soft targets help further, where coarse clip-level ( _Soft Coarse_ ) and fine windowlevel ( _Soft Fine_ ) targets each raise accuracy and their combination ( _Soft Coarse_ + _Fine_ ) is best in (A) at 86.9 R@1. The R _→_ R gain is most telling, as robot pairs are never directly aligned in training. Alignment emerges transitively through the shared human anchor, which the LAMP prior, common to all embodiments, makes possible. 

**(B) Alignment target.** With the loss fixed to Soft Coarse+Fine, we change what the head receives alongside **P** ( _τ_ ). Adding the raw root position **X** root lifts R@1 to 88.5 on H _→_ R and our pooled, FiLM-modulated pose token **z** pose ( _Ours_ ) is best on every metric and direction (90.3 R@1, 93.9 MRR on H _→_ R). The modulated token adds postural context already consistent with the phase manifold, separating same-rhythm motions without injecting raw morphology. 

#### **5.1.2 Manifold Visualization and Interpretability** 

The PCA projections (left of Fig. 3) reveal two properties. _Intra-clip continuity_ (second column), within a clip the advancing phase _ϕc_ ( _τ_ ) traces a smooth counter-clockwise orbit whose radius reflects amplitude, a signature unstructured embeddings lack. _Cross-embodiment overlap_ (first column), matched timestamps from different embodiments cluster tightly, validating the humananchored alignment. The alignment embedding _z_ (top) is mildly distorted relative to the raw manifold **P** ( _τ_ ) (bottom) yet keeps the circular structure and still separates motion types. 

We further show that the phase shift _Sc_ is an interpretable, controllable temporal coordinate (right of Fig. 3). For a G1 running clip we read per-window _Sc_ with the frozen encoder, unwrap it into 

7 

||**Im**|**itation**|**Tele**|**operation**|
|---|---|---|---|---|
|**Variant**|_dz_|MPJPE_↓_|_dz_|MPJPE_↓_|
|Propr. raw|–|1.83|–|64.85|
|MLP|80|1.83|80|66.79|
|VQ|10|1.69|10|65.17|
|**PHASOR**|64|**1.62**|64|**64.75**|


Figure 4: **Left.** Downstream results, all encoders frozen and only the policy head trained (MPJPE in mm, _↓_ ). Propr. raw uses raw proprioceptive input with no embedding. **Right.** IsaacSim walkingforward rollout, left to right PHASOR (ours), VQ, MLP. 

a monotone timeline, and retrieve windows at evenly spaced offsets _Sq_ + ∆ _S_ . The retrieved start point advances in proportion to ∆ _S_ , confirming the embedding captures motion timing and supports per-embodiment phase control. 

#### **5.2 Downstream Tasks** 

We test the frozen embedding on three tasks, each freezing the encoder and training only a lightweight policy head to isolate representation quality. As a floor, we add a _Proprioceptive raw_ baseline that drives the policy head from raw proprioceptive input alone, with no learned embedding (first row of Fig. 4). The exact proprioceptive inputs and downstream settings are in Sec. B.4. 

**Motion Imitation and Teleoperation.** Both predict 3D joint positions from a frozen embedding via a 3-layer MLP. In _imitation_ , the G1’s proprioceptive state and _z_ predict its next-frame pose, where PHASOR scores best (Fig. 4) as its explicit phase parameterization pins down the gait-cycle position while the VQ codebook captures periodicity only implicitly. In _teleoperation_ , a human window maps to the matching G1 pose from _z_ alone, where only PHASOR beats the raw-kinematics baseline and MLP falls below it, showing an unstructured projection can discard useful information. 

**RL Locomotion with Phase Reward.** Here the embedding shapes the reward rather than the policy input. The same frozen encoder _f_ embeds the robot’s online motion and the human reference, and the reward scores their alignment, 


so each method measures phase agreement in _its own_ space without prescribing a joint-level solution. The reference enters only through the reward and all variants share identical settings, isolating embedding geometry. In Fig. 4, PHASOR walks forward steadily on both feet, VQ under-uses one leg and drifts in a circle, and MLP fails to locomote, confirming our phase embedding gives an effective reward for periodic, walking-like motion. 

### **6 Conclusion** 

We present PHASOR, an action representation that treats the periodic structure of motion as a design prior rather than learning the latent space from reconstruction alone. By decomposing motion into per-body-part phase parameters, PHASOR builds a compact, morphology-invariant manifold anchored in human motion, where each new robot joins through a lightweight adapter against a frozen oracle, yielding an interpretable and controllable action space whose coordinates expose behavior timing. Across one human and four humanoids, this frozen manifold transfers effectively to retrieval and downstream policy learning, indicating that motion-intrinsic periodicity is a transferable substrate for cross-embodiment action embeddings. 

**Limitations.** PHASOR is built around periodic structure, so it is most informative for rhythmic, locomotion-style behaviors while providing weaker structure for transient or aperiodic motions, and its pose branch remains per-embodiment, leaving non-periodic posture unshared across bodies. Validation is currently limited to simulation, with physical hardware left to future work. We view these as natural next steps rather than fundamental barriers. 

8 

#### **References** 

- [1] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , 2023. 

- [2] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [3] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [4] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 2025. 

- [5] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Castaneda, Z.-A. Cao, J. Li, D. Minor, Q. Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [6] S. Ye, J. Jang, B. Jeon, S. J. Joo, J. Yang, B. Peng, A. Mandlekar, R. Tan, Y.-W. Chao, B. Y. Lin, et al. Latent action pretraining from videos. In _International Conference on Learning Representations_ , volume 2025, pages 28213–28239, 2025. 

- [7] A. Mete, H. Xue, A. Wilcox, Y. Chen, and A. Garg. Quest: Self-supervised skill abstractions for learning continuous control. _Advances in Neural Information Processing Systems_ , 37: 4062–4089, 2024. 

- [8] O. M. Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- [9] Q. Bu, Y. Yang, J. Cai, S. Gao, G. Ren, M. Yao, P. Luo, and H. Li. Univla: Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2505.06111_ , 2025. 

- [10] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong, et al. Openvla: An open-source vision-language-action model. In _Conference on Robot Learning_ , 2025. 

- [11] S. Starke, I. Mason, and T. Komura. Deepphase: Periodic autoencoders for learning motion phase manifolds. _ACM Transactions on Graphics (ToG)_ , 41(4):1–13, 2022. 

- [12] P. Li, S. Starke, Y. Ye, and O. Sorkine-Hornung. Walkthedog: Cross-morphology motion alignment via phase manifolds. In _ACM SIGGRAPH 2024 Conference Papers_ , pages 1–10, 2024. 

- [13] B. Ji, Y. Pan, Z. Liu, S. Tan, X. Jin, and X. Yang. Pomp: Physics-consistent motion generative model through phase manifolds. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 22690–22701, 2025. 

- [14] M. Pegoraro, E. Atherton, B. Roy, A. Khani, and A. Rampini. Funphase: A periodic functional autoencoder for motion generation via phase manifolds. _arXiv preprint arXiv:2512.09423_ , 2025. 

- [15] E. Perez, F. Strub, H. De Vries, V. Dumoulin, and A. Courville. Film: Visual reasoning with a general conditioning layer. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 32, 2018. 

9 

- [16] Z. Li, W. Yuan, Y. He, L. Qiu, S. Zhu, X. Gu, W. Shen, Y. Dong, Z. Dong, and L. Yang. Lamp: Language-motion pretraining for motion generation, retrieval, and captioning. In _International Conference on Learning Representations_ , volume 2025, pages 84238–84250, 2025. 

- [17] Q. Bu, J. Cai, L. Chen, X. Cui, Y. Ding, S. Feng, S. Gao, X. He, X. Hu, X. Huang, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025. 

- [18] S. Lee, Y. Wang, H. Etukuru, H. J. Kim, N. M. M. Shafiullah, and L. Pinto. Behavior generation with latent actions. _arXiv preprint arXiv:2403.03181_ , 2024. 

- [19] D. Holden, T. Komura, and J. Saito. Phase-functioned neural networks for character control. _ACM Transactions on Graphics (TOG)_ , 36(4):1–13, 2017. 

- [20] H. Zhang, S. Starke, T. Komura, and J. Saito. Mode-adaptive neural networks for quadruped motion control. _ACM Transactions on Graphics (ToG)_ , 37(4):1–11, 2018. 

- [21] S. Starke, H. Zhang, T. Komura, and J. Saito. Neural state machine for character-scene interactions. _ACM Transactions on Graphics_ , 38(6):178, 2019. 

- [22] S. Starke, Y. Zhao, T. Komura, and K. Zaman. Local motion phases for learning multi-contact character movements. _ACM Transactions on Graphics_ , 39(4), 2020. 

- [23] I. Mason, S. Starke, and T. Komura. Real-time style modelling of human locomotion via feature-wise transformations and local motion phases. _Proceedings of the ACM on Computer Graphics and Interactive Techniques_ , 5(1):1–18, 2022. 

- [24] X. Zhang, Z. Chang, Q. Men, and H. P. Shum. Motion in-betweening for densely interacting characters. In _Proceedings of the SIGGRAPH Asia 2025 Conference Papers_ , pages 1–11, 2025. 

- [25] M. Dai, K. Fan, A. Rao, J. Wang, and B. Dai. Controllable text-to-motion generation via modular body-part phase control. _arXiv preprint arXiv:2603.19795_ , 2026. 

- [26] J. Park, D. Cho, J. Lee, D. Shim, I. Jang, and H. J. Kim. Periodic skill discovery. _Advances in Neural Information Processing Systems_ , 38:105404–105438, 2026. 

- [27] M. Gleicher. Retargetting motion to new characters. In _Proceedings of the 25th annual conference on Computer graphics and interactive techniques_ , pages 33–42, 1998. 

- [28] K. Aberman, P. Li, D. Lischinski, O. Sorkine-Hornung, D. Cohen-Or, and B. Chen. Skeletonaware networks for deep motion retargeting. _ACM Transactions on Graphics (ToG)_ , 39(4): 62–1, 2020. 

- [29] Z. Luo, J. Cao, K. Kitani, W. Xu, et al. Perpetual humanoid control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 10895–10904, 2023. 

- [30] Z. Luo, J. Cao, J. Merel, A. Winkler, J. Huang, K. Kitani, and W. Xu. Universal humanoid motion representations for physics-based control. In _International Conference on Learning Representations_ , volume 2024, pages 56766–56782, 2024. 

- [31] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi. Omniretarget: Interaction-preserving data generation for humanoid whole-body locomanipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

- [32] Y. Yan, E. V. Mascaro, and D. Lee. Imitationnet: Unsupervised human-to-robot motion retargeting via shared latent space. In _2023 IEEE-RAS 22nd International Conference on Humanoid Robots (Humanoids)_ , pages 1–8. IEEE, 2023. 

10 

- [33] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang. Expressive whole-body control for humanoid robots. _arXiv preprint arXiv:2402.16796_ , 2024. 

- [34] Y. Yan and D. Lee. Learning a unified latent space for cross-embodiment robot control, 2026. URL `https://arxiv.org/abs/2601.15419` . 

- [35] R.-Z. Qiu, S. Yang, X. Cheng, C. Chawla, J. Li, T. He, G. Yan, D. J. Yoon, R. Hoque, L. Paulsen, G. Yang, J. Zhang, S. Yi, G. Shi, and X. Wang. Humanoid policy human policy, 2025. URL `https://arxiv.org/abs/2503.13441` . 

- [36] C. Wang, L. Fan, J. Sun, R. Zhang, L. Fei-Fei, D. Xu, Y. Zhu, and A. Anandkumar. Mimicplay: Long-horizon imitation learning by watching human play, 2023. URL `https://arxiv.org/ abs/2302.12422` . 

- [37] P. Dan, K. Kedia, A. Chao, E. W. Duan, M. A. Pace, W.-C. Ma, and S. Choudhury. X-sim: Cross-embodiment learning via real-to-sim-to-real. _arXiv preprint arXiv:2505.07096_ , 2025. 

- [38] H. Kim, J. Kang, H. Kang, M. Cho, S. J. Kim, and Y. Lee. Uniskill: Imitating human videos via cross-embodiment skill representations. _arXiv preprint arXiv:2505.08787_ , 2025. 

- [39] Y. Shao, X. Huang, B. Zhang, Q. Liao, Y. Gao, Y. Chi, Z. Li, S. Shao, and K. Sreenath. Langwbc: Language-directed humanoid whole-body control via end-to-end learning. _arXiv preprint arXiv:2504.21738_ , 2025. 

- [40] J. Yue, Z. Wang, Y. Wang, W. Zeng, J. Wang, X. Xu, Y. Zhang, S. Zheng, Z. Ding, and Z. Lu. Rl from physical feedback: Aligning large motion models with humanoid control. _arXiv preprint arXiv:2506.12769_ , 2025. 

- [41] Z. Li, C. Chi, Y. Wei, B. Zhu, Y. Peng, T. Huang, P. Wang, Z. Wang, S. Zhang, and C. Xu. From language to locomotion: Retargeting-free humanoid control via motion latent guidance. _arXiv preprint arXiv:2510.14952_ , 2025. 

11 

## **Appendix** 

### **A Implementation Details** 

#### **A.1 Body-Part Partition and Channel Allocation** 

To systematically capture local periodic structures, we partition kinematic joints of each embodiment into five semantic parts: _B_ = _{_ LA _,_ RA _,_ TK _,_ LL _,_ RL _}_ . We assign the phase channel allocation _Kb_ based on the rhythmic complexity of each part during locomotion. Specifically, legs exhibit strong multi-phase oscillations requiring more capacity ( _K_ LL = _K_ RL = 4), arms show moderate complexity ( _K_ LA = _K_ RA = 3), and the trunk’s dominant modes are set to _K_ TK = 2. 

This allocation is shared across all embodiments, yielding a universal _M_ total = 16 channels and a 32-dimensional phase manifold **P** ( _τ_ ). Tab. I summarizes the joint distributions and kinematic dimensions for the human and four humanoid robots. 

|**Embodiment**|**_J_**|**_Dk_**|LA|**Join**<br>RA|**ts per**<br>TK|**part**<br>LL|RL|**TK Components**|
|---|---|---|---|---|---|---|---|---|
|Human (SMPL-H)|22|66|4|4|6|4|4|pelvis, spine (3), neck, head|
|G1 (Unitree)|32|96|7|7|4|7|7|pelvis, waist (2), torso|
|H12 (Unitree)|28|84|7|7|2|6|6|pelvis, torso|
|T1 (Booster)|24|72|4|4|4|6|6|trunk, head (2), waist|
|BHL (Berkeley)|25|75|6|6|1|6|6|base only|
|**Phase channels (**_Kb_|**)**||**3**|**3**|**2**|**4**|**4**|_M_total = 16|


Table I: **Body-part partition and channel allocation.** We enforce a consistent five-part semantic structure and phase channel allocation ( _Kb_ ) across heterogeneous embodiments. _J_ denotes total joints, and _Dk_ is velocity dimension (3 _J_ ). The 3D root linear velocity is concatenated to the trunk (TK) input. 

|**Embodiment**|**Part**|**Joint Indices & Description**|
|---|---|---|
|Human<br>(SMPL-H)|LA / RA<br>TK<br>LL / RL|[13, 16, 18, 20] / [14, 17, 19, 21]: collar, shoulder, elbow, wrist<br>[0, 3, 6, 9, 12, 15]: pelvis, spine 1–3, neck, head<br>[1, 4, 7, 10] / [2, 5, 8, 11]: hip, knee, ankle, foot|
|G1<br>(Unitree)|LA / RA<br>TK<br>LL / RL|[18–24] / [25–31]: shoulder (3), elbow, wrist (3)<br>[0, 15–17]: pelvis, waist (2), torso<br>[1–7] / [8–14]: hip (3), knee, ankle (2), toe|
|H12<br>(Unitree)|LA / RA<br>TK<br>LL / RL|[14–20] / [21–27]: shoulder (3), elbow, wrist (3)<br>[0, 13]: pelvis, torso<br>[1–6] / [7–12]: hip (3), knee, ankle (2)|
|T1<br>(Booster)|LA / RA<br>TK<br>LL / RL|[3–6] / [7–10]: arm joints 1–3, hand<br>[0–2, 11]: trunk, head 1–2, waist<br>[12–17] / [18–23]: hip (3), shank, ankle (cross), foot|
|BHL<br>(Berkeley)|LA / RA<br>TK<br>LL / RL|[1–6] / [7–12]: shoulder (3), elbow (2), hand<br>[0]: base only<br>[13–18] / [19–24]: hip (3), knee, ankle (2)|


Table II: **Explicit joint index mappings.** Joints are assigned to the five semantic parts following each embodiment’s specific URDF hierarchy. Left/Right symmetric parts are grouped for brevity, and the numbers in parentheses indicate the degrees of freedom (e.g., pitch, roll, yaw) for that joint group. 

i 

#### **A.2 Bidirectional FiLM Coupling Architecture** 

We provide the full architectural details of the bidirectional FiLM coupling described in Sec. 4.1.2. Both directions pass through a learned manifold encoder ( _Eψ_ for phase-to-pose, _Eϕ_ for pose-tophase) that aligns the source representation to the temporal granularity of the target branch. 

**Phase-to-Pose Modulation.** The phase-to-pose direction provides the pose decoder with temporal context: “where in the action the body currently is”. The manifold encoder _Eψ_ compresses the perframe phase manifold **P** _∈_ R<sup>_T ×_32</sup> into a token-aligned context _Eψ_ ( **P** ) _∈_ R<sup>_L_pose</sup><sup>_×dg_</sup> with _dg_ = 128, implemented as three 1D convolutions followed by adaptive pooling to _L_ pose = 8 tokens. A FiLM head produces per-token modulation parameters ( _γ, β_ ) _∈_ R<sup>_L_pose</sup><sup>_×d_pose</sup> that scale and shift the pose tokens: 


**Pose-to-Phase Modulation.** Symmetrically, the pose-to-phase direction provides each per-part decoder with postural context: “what baseline configuration the motion rests on”. The manifold encoder _Eϕ_ expands the pose tokens **z** pose _∈_ R<sup>_L_pose</sup><sup>_×d_pose</sup> into per-frame context _Eϕ_ ( **z** pose) _∈_ R<sup>_T ×dg,_pose</sup> with _dg,_ pose = 64, implemented as two 1D convolutions followed by linear interpolation from _L_ pose = 8 tokens to _T_ = 121 frames. A per-part FiLM head generates per-frame modulation parameters ( _γb_ ( _τ_ ) _, βb_ ( _τ_ )) _∈_ R<sup>_Kb_</sup> that modulate the reconstructed sinusoidal signal **v** ˆ _b_<sup>sig(</sup><sup>_τ_)=</sup> � _k_<sup>_Ab,k_cos</sup><sup>_ϕb,k_(</sup><sup>_τ_) +</sup><sup>_Bb,k_before it enters the per-part decoder</sup><sup>_Db_:</sup> 


**Modulation Strength.** The scalar _α_ is learnable in both directions and initialized to 0 _._ 05. This nearzero start ensures that the modulation begins close to identity, providing the same training stability while allowing the model to gradually scale up modulation as training progresses. 

#### **A.3 Periodic Module Details** 

We detail the per-part periodic encoder Φ _b_ , the FFT-based parameter extraction, and the handling of root velocities. 

**Per-Part Encoder and Decoder.** Each Φ _b_ is a lightweight 1D convolutional encoder of two layers with LayerNorm over the time dimension and ELU activations. The latent map Φ _b_ ( **v** _b_ ) _∈_ R<sup>_Kb×T_</sup> feeds the FFT bottleneck. The per-part decoder _Db_ mirrors Φ _b_ with the same width and depth, taking the modulated sinusoidal signal **v** ˆ _b_<sup>sig,mod</sup> ( _τ_ ) and producing the reconstructed velocity. For the trunk, the decoder output is sliced into the joint-velocity ( **v** ˆTK<sup>joint) and the root linear velocity portion (</sup><sup>**v**ˆ</sup> lin<sup>root).</sup> **FFT Parameter Extraction.** Given the per-part latent Φ _b_ ( **v** _b_ ), the periodic parameters are extracted by applying a differentiable real-valued FFT along the time axis. Let _{cj}_ denote the FFT coefficients of latent channel _k_ . The amplitude, frequency, and offset are computed as 


where _fj_ is the FFT bin frequency. The phase shift _Sb,k_ is predicted by a separate fully-connected head followed by arctan2, producing values in ( _−π, π_ ]. 

**Trunk Input with Root Linear Velocity.** The root linear velocity **v** lin<sup>root</sup> _∈_ R<sup>_T ×_3</sup> exhibits clear periodicity during locomotion (vertical oscillation and forward-backward acceleration), and the phase branch should absorb it. We concatenate it to the trunk joint velocities: **v** TK( _τ_ ) = [ **v** TK<sup>joint(</sup><sup>_τ_);</sup><sup>**v**</sup> lin<sup>root(</sup><sup>_τ_)].Therootyawrateisomittedfromthephasebranch,sincetheposebranch</sup> already absorbs angular changes through the temporal evolution of **R**<sup>joint</sup> . 

**Pelvis** _vx, vz_ **Soft Mask.** Under the root-local frame, the pelvis horizontal velocity components _vx, vz_ are identically zero by definition. Treating them with a hard zero mask in _L_ phase caused training drift of approximately _±_ 0 _._ 8 on neighboring channels. We instead apply a soft mask with 

ii 

weight 0 _._ 1, which anchors these channels to zero while keeping a small but nonzero gradient signal. This stabilizes the trunk reconstruction without distorting the manifold. 

#### **A.4 Cross-Embodiment Pipeline Details** 

We provide details of the encoder and decoder adapters and the robot pose branch. 

**Per-Robot Input Adapter** _Er_<sup>_k_</sup><sup>**.**Theinputadaptermapstherobotvelocitydimension</sup><sup>_Dk_tothe</sup> human dimension 66 via a single global linear layer, _Er_<sup>_k_=Linear(</sup><sup>_Dk→_66).Weconsidereda</sup> per-part variant with five separate linear layers, one per body part, but the two options produced nearidentical retrieval and reconstruction quality. We adopt the global linear variant since it requires no hardcoded joint-to-part mapping and allows cross-joint information flow to be learned end-to-end. **Forward Pipeline for Robots.** Given a robot velocity input, the pipeline proceeds as follows. (1) Apply the per-robot input adapter: **v** ˜ _R_<sup>(66)</sup><sup>_k_</sup> = _Er_<sup>_k_(</sup><sup>**v**</sup> _R_<sup>joint</sup><sup>_k_).(2) Split the 66-D output into the five-part</sup> dictionary using the same partition as the human. (3) Concatenate the robot’s root linear velocity **v** lin<sup>root</sup> _,k_<sup>to the trunk input.(4) Apply the frozen weight-shared encoder</sup><sup>_EX≡Eh_to extract per-part</sup> periodic parameters. (5) Construct **P** _Rk_ ( _τ_ ) _∈_ R<sup>_T ×_32</sup> via Eq. (3). 

**Decoder Split and Mirror Initialization.** The human phase decoder _Dh_ remains frozen and is used only on the human path. Robot paths share a unified decoder _DX_ that is initialized as a weight-copy of _Dh_ and fine-tuned on robot data. This split provides a gradient safety net: robot reconstruction loss flows only through _DX_ and never disturbs _Dh_ . The mirror initialization gives _DX_ a strong starting point, since robot motion is itself a retargeted humanoid signal and the human velocity decoder serves as a valid prior. We also tested freezing _DX_ at its mirror copy; fine-tuning improved retrieval mAP and reconstruction by approximately 1% on average and was adopted as the default. 

**Per-Robot Pose Branch.** The pose branch is instantiated separately for each embodiment, since posture distributions and joint conventions vary across morphologies. Tab. III summarizes which modules are shared with the human oracle and which are trainable per-embodiment. The phase-side modules ( _Eψ_ and the phase-to-pose FiLM head) are shared and frozen, consistent with anchoring the manifold to the human reference. The pose-side modules ( _Eϕ_ and the pose-to-phase FiLM head) are per-embodiment trainable, since their input **z** pose comes from an embodiment-specific encoder with a different distribution. 

|**Module**|**Human**|**Robot**_k_|
|---|---|---|
|Pose encoder + decoder|frozen|per-embodiment, trainable|
|_Eϕ_ (Pose_→_Phase manifold enc.)|frozen|per-embodiment, trainable|
|Pose_→_Phase FiLM head|frozen|per-embodiment, trainable|
|_Eψ_ (Phase_→_Pose manifold enc.)|shared, frozen|shared, frozen|
|Phase_→_Pose FiLM head|shared, frozen|shared, frozen|


Table III: **Pose branch module sharing across embodiments.** Phase-side conditioning modules are shared with the frozen human oracle, while pose-side conditioning modules are trainable perembodiment. 

#### **A.5 Alignment Objective Details** 

**Alignment Head Architecture.** The projection _π_ takes the per-frame concatenated feature **f** ( _τ_ ) = [ **P** ( _τ_ ); **z**<sup>pool</sup> pose<sup>]</sup><sup>_∈_R160and produces a unit-sphere embedding.Its structure is Linear(160</sup><sup>_→_64)</sup><sup>_→_</sup> GELU _→_ Linear(64 _→_ 64) _→ ℓ_ 2. Per-frame normalization yields the trajectory _z_ ( _τ_ ) _∈S_<sup>63</sup> , and a subsequent time-pool with another _ℓ_ 2 normalization yields the clip-level descriptor _z_<sup>pool</sup> _∈S_<sup>63</sup> . The trajectory _z_ ( _τ_ ) feeds _L_ speed and _L_ shape, while _z_<sup>pool</sup> feeds _L_ pair. 

**Pose-Half Near-Zero Initialization.** The first linear layer of _π_ has weight matrix _W ∈_ R<sup>64</sup><sup>_×_160</sup> . We initialize the first 32 columns (the phase input half) with standard Kaiming initialization and the remaining 128 columns (the pose input half) with a near-zero scale of 10<sup>_−_3</sup> . At the start of training, 

iii 

_π_ thus behaves close to a phase-only projection, and the pose contribution grows gradually through gradient updates. This warm-onset prevents pose noise from disrupting alignment early and keeps the pose contribution at an auxiliary level by the end of training. 

**Hierarchical Pair Loss.** We apply the LAMP soft target at two granularities. Let **_ℓ_**<sup>W</sup> _→_<sup>denotethe</sup> _B × B_ window-level logits over the human-to-robot or robot-to-human direction, and _T_ W<sup>soft</sup> the corresponding LAMP-induced soft target from per-window LAMP features. The window-level loss is 


For the clip-pool head, we average _z_ over windows sharing the same clip, normalize, and form a _K × K_ logit matrix where _K_ is the number of unique clips in the batch. The corresponding LAMP soft target _T_ C<sup>soft</sup> uses clip-level LAMP features: 


The clip-pool head uses a pure soft target since same-clip windows are already merged into a single anchor through pooling, removing the gradient-dilution effect of broadcasting soft labels across redundant windows. The final pair loss combines both granularities: 


**Trajectory Consistency Terms.** The two auxiliary geometric penalties on _z_ ( _τ_ ) _∈S_<sup>63</sup> are 


_L_ speed matches per-frame step size on the sphere, an implicit frequency synchronization. _L_ shape matches half-period distance, an implicit amplitude synchronization. Both operate on the postprojection unit sphere, making them scale-invariant by construction. 

**LAMP Teacher.** LAMP [16] is a pretrained motion-language prior trained on human motion. Its 512-D embedding serves as a fixed teacher. We use two granularities of LAMP features: cliplevel embeddings for the clip-pool head, and stride-20 window-level embeddings for the window head. Both are precomputed on the human motion data and applied symmetrically as soft targets for human-to-robot and robot-to-human alignment in each batch. 

#### **A.6 Training Procedure** 

**Reconstruction Loss Terms.** The per-part velocity reconstruction loss applies a weighted MSE over the five body parts: 


where the pelvis _vx, vz_ channels carry a soft weight _w_ = 0 _._ 1 as described in Sec. A.3. The pose reconstruction loss combines a geodesic distance on 6D continuous rotations with a root position MSE: 


The forward kinematics consistency loss links the two branches by enforcing agreement on global joint positions: 


The FK loss is applied only on the human path, since we do not maintain a differentiable kinematic chain for each robot in this work. 

iv 

|**Group**|**Item**|**Value**|
|---|---|---|
|Window|_T_, fps|121, 60|
|Phase|_Kb_ (LA, RA, TK, LL, RL)|(3, 3, 2, 4, 4),_M_total = 16|
|Pose|_L_pose,_d_pose,_dR_,_d_root|8, 128, 96, 32|
|FiLM|_dg_,_dg,_pose,_α_init|128, 64, 0.05|
|Alignment|_π_input dim,_d_align<br>pose-half init scale|160 (= 32 + 128), 64<br>10<sup>_−_3</sup>|
||_τh_,_τs_|0.1, 0.07|
||_λ_mix,_λ_C|0.3, 0.3|
||_λ_pair,_λ_speed,_λ_shape|1.0, 0.5, 0.5|
|Loss weights|_λ_phase,_λ_pose,_λ_FK<br>pelvis_vx, vz_ soft mask|5.0, 5.0, 1.0<br>0.1<br>|
|Optimization|optimizer, lr, weight decay|AdamW,2_×_10<sup>_−_4</sup>,10<sup>_−_4</sup>|
||batch size, grad clip|512, 5.0|
||epochs (each stage)|30|
||FK warmup, alignment warmup|3, 5 epochs|


Table IV: **Hyperparameter configuration** for both training stages. 

|||**H**_→_**R C**|**lip-leve**|**l**||**R**_→_**H C**|**lip-leve**|**l**|**R**|_→_**R C**|**lip-leve**|**l**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Method|R@1|R@5|R@10|mAP|R@1|R@5|R@10|mAP|R@1|R@5|R@10|mAP|
|MLP|**99.6**|**100.0**|**100.0**|**99.8**|**99.8**|**100.0**|**100.0**|**99.9**|**99.0**|**99.8**|**100.0**|**99.4**|
|SONIC|97.8|99.8|99.8|98.7|97.0|99.8|99.8|98.3|97.2|99.5|99.5|98.2|
|Only Phase|93.8|98.1|98.8|95.7|94.2|98.5|99.0|96.2|88.1|96.0|98.0|91.4|
|W.O LAMP|95.8|99.1|99.8|97.2|95.5|99.0|99.8|97.0|91.4|97.8|99.0|94.2|
|W Pos|97.5|99.9|**100.0**|98.5|98.8|99.8|**100.0**|99.3|93.5|99.3|99.7|96.0|
|**W**_Z_**pos (Ours)**|99.1|99.8|99.8|99.4|99.5|99.8|99.8|99.6|98.1|99.4|99.7|98.6|


Table V: Cross-embodiment clip-level retrieval on the DPAE val set (2,472 clips). **H** _→_ **R** : human query _→_ robot gallery (avg. over G1/H1.2/T1/BHL). **R** _→_ **H** : robot query _→_ human gallery (avg. over G1/H1.2/T1/BHL). **R** _→_ **R** : robot _↔_ robot (avg. over �24�=6 pairs, both directions). All values in %. **Bold** : best per column. <u>Underline:</u> second best. 

**Hyperparameters.** Tab. IV lists the full hyperparameter configuration. All experiments share these values across the human and four robot embodiments. 

**Parameter Accounting.** At Stage 2, the human oracle contributes approximately 528K frozen parameters, including the phase encoder body _Eh_ (shared as _EX_ on the robot path), the manifold encoder _Eψ_ , the phase-to-pose FiLM head, the phase decoder _Dh_ , the human pose encoder and decoder, and the human pose-to-phase modules. The trainable budget is approximately 1.46M parameters, consisting of the shared phase decoder _DX_ ( 51K, mirror-initialized from _Dh_ ), the alignment head _π_ ( 10K), per-robot input and output adapters _Er_<sup>_k, D_</sup> _r_<sup>_k_(11Keach),per-robotposeencoder</sup> and decoder ( 225K each), per-robot _Eϕ_ ( 43K each), and per-robot pose-to-phase FiLM head ( 87K each), summed over the four robot embodiments. 

### **B Additional Experiments** 

#### **B.1 Ablation** 

We isolate each design choice through clip-level retrieval on Stage 2 (Sec. B.1). Clip-level matching only requires preserving coarse _semantic_ identity, not fine temporal structure, making it an easy task: all methods exceed 91% mAP and gaps between variants are small. We read this as a sanity check that each variant retains clip-level semantics, while our true advantage appears in exact-match retrieval (Sec. 5.1.1), addressing the limitation in Sec. 6. 

v 

**Only Phase** (phase manifold alone) already reaches 91–96% mAP, confirming the periodic prior captures clip identity on its own; adding LaMP guidance ( **W.O LAMP** _→_ default) and root position ( **W Pos** ) each gives a small, consistent gain, largest on R _→_ R. Our full model **W** _Z_ **pos** is essentially tied with the best configuration everywhere. The MLP and VQ baselines lead at clip level, as expected: an unstructured objective directly optimizes coarse semantic identity, whereas our embedding additionally encodes _when_ each chunk occurs, which is unnecessary here but drives our large margin in exact-match. Adding temporal structure thus costs almost nothing on this easy task while dominating the fine-grained one. 

#### **B.2 Effect of the LAMP Mixing Ratio** 

The hierarchical pair loss (Eq. (12)) mixes a hard-target InfoNCE term with a LAMP-induced soft target via _λ_ mix: at _λ_ mix=0 it is pure InfoNCE, at _λ_ mix=1 it relies entirely on LAMP semantic similarity. We sweep _λ_ mix _∈{_ 0 _._ 0 _,_ 0 _._ 3 _,_ 0 _._ 7 _,_ 1 _._ 0 _}_ and report clip-level and exact-match mAP across the three directions (Fig. I). 

Both granularities peak at _λ_ mix=0 _._ 3, our default. A moderate semantic signal helps, most visibly on the unsupervised R _→_ R direction where it strengthens transitive alignment through the human anchor. But beyond 0 _._ 3 performance degrades, collapsing at _λ_ mix=1 _._ 0: with the hard target removed, the model loses the instance-level correspondence needed for fine-grained matching, since LAMP similarity alone is too coarse to separate chunks within a clip. LAMP thus works best as auxiliary guidance, not a standalone target. 


Figure I: **Effect of the LAMP mixing ratio** _λ_ **mix.** Clip-level (left) and exact-match (right) mAP over _λ_ mix _∈{_ 0 _._ 0 _,_ 0 _._ 3 _,_ 0 _._ 7 _,_ 1 _._ 0 _}_ for all three directions. Both peak at 0 _._ 3 (our default) and collapse at 1 _._ 0 when the hard target is removed. 

#### **B.3 Downstream Tasks** 

We probe the frozen embedding’s utility in three settings: single-embodiment next-frame prediction (imitation), cross-embodiment teleoperation, and locomotion RL with a phase-shaped reward. In both offline tasks the policy head is a 3-layer MLP (256 _→_ 256 _→_ output) trained for 50 epochs (Adam, lr 10<sup>_−_4</sup> , cosine schedule, batch 512). A **no-embedding baseline (A)** receiving only raw proprioceptive state is included for reference. 

#### **B.4 RL Locomotion Details** 

#### **B.4.1 Reference Embedding Preparation** 

Before RL training, every AMASS reference clip is encoded offline into per-frame reference embeddings _z_ ref by each model’s frozen human encoder, yielding a 64D sequence for PHASOR, 10D for VQ, and 80D for MLP. Each variant’s reward uses its own pre-encoded _z_ ref, so the human encoder need not run during training. 

vi 

#### **B.4.2 Environment Configuration** 

- Simulator: IsaacLab with GPU physics. 

- Simulation timestep 1 _/_ 120 s, control decimation 2, giving a policy timestep of 1 _/_ 60 s. 

- 8,192 parallel environments. 

- Episode length: up to 20 s (1 _,_ 200 policy steps). 

- Each episode resets to a standing pose (no reference-state initialization). 

#### **B.4.3 Observation** 

The policy observation is a 10-step history of proprioceptive state, concatenating per step the joint positions (23), joint velocities (23), base angular velocity (3), base roll/pitch/yaw (3), and previous action (23), for a total of 750 dimensions. This is augmented with the frozen robot embedding _z_ align ~~r~~<sup>, whose dimension depends on the encoder:</sup> 

|Variant|_z_align<br>~~r~~ <sup>dim</sup>|Total obs dim|
|---|---|---|
|PHASOR|64|814|
|MLP|80|830|
|VQ|10|760|


The robot embedding is computed online: at each step the latest joint velocities are appended to a 121-frame sliding window, and once the window is full the frozen robot encoder produces _z_ align ~~r~~<sup>.</sup> 

#### **B.4.4 Reference Progression** 

At each reset a reference clip is sampled at random, and its frame index advances by one per policy step (wrapping at the clip end). The corresponding reference embedding _z_ ref ~~c~~ ur<sup>isreadfromthe</sup> precomputed sequence. The reference is used _only_ to compute the reward and is never part of the observation. 

#### **B.4.5 Reward Design (15 Terms)** 

#### **Survival (always active):** 

|#|Term|Weight|
|---|---|---|
|1|Termination penalty (torso height_<_0_._3m)|_−_200|
|2|Alive bonus (+0_._15per step)<br><br>|_×_1|
|3|Flat orientation: _−_(_g_<sup>2</sup><br>_b,x_ <sup>+</sup><sup>_g_2</sup><br>_b,y_<sup>)</sup><br>|_−_1_._0|
|4|Base height: _−_(_z_pelvis_−_0_._78)<sup>2</sup>|_−_10_._0|
|5|Vertical velocity: _−v_<sup>2</sup><br>_z_|_−_2_._0|
|6|Roll/pitch angular velocity|_−_0_._05|


#### **Locomotion (active from iteration 500):** 

|#|Term|Weight|
|---|---|---|
|7|Velocity tracking: exp(_−_(_v_robot_−v_ref)<sup>2</sup>_/_0_._25)|_λ_vel|
|8|Feet air-time (bipedal alternation bonus)|+2_._0|
|9|Feet slide penalty|_−_0_._1|
|10|Hip joint deviation from default|_−_0_._5|
|11|Arm joint deviation from default|_−_0_._1|
|12|Torso joint deviation from default|_−_0_._1|
|13|Ankle soft-limit violation|_−_1_._0<br>|
|14|Joint acceleration (hip, knee)|_−_1_._25_×_10<sup>_−_7</sup>|
|15|Joint torque (hip, knee, ankle)<br>|_−_1_._5_×_10<sup>_−_7</sup>|
|16|Action rate: _−_(_at −at−_1)<sup>2</sup>|_−_0_._001|


#### **Phase (active from iteration 1000):** 

vii 

|#|Term||Weight|
|---|---|---|---|
|17|Phase similarity:|(cos(_z_align<br>~~r~~<sup>_, z_</sup>ref<br>~~c~~ur<sup>) + 1)</sup><sup>_/_2</sup>|_λ_phase|


Non-termination terms are clamped to be non-negative before the termination penalty is added, so the agent cannot reduce its loss by ending an episode early; the termination penalty therefore always applies. 

#### **B.4.6 PPO Configuration** 

- 5 PPO epochs, 4 mini-batches per iteration; 2,500 iterations total. 

- Policy network: MLP [512 _→_ 256 _→_ 128] with ELU, observation normalization, and Gaussian action noise _σ_ = 0 _._ 3. 

- Curriculum weights updated every 50 iterations. 

#### **B.4.7 Curriculum Schedule** 

|Iteration|_λ_vel|_λ_phase|Stage|
|---|---|---|---|
|0–499|0|0|Survival only (stand)|
|500–999|1|0|+velocity (walk)|
|1000–1999|1|0_→_1|+phase ramp (shape gait)|
|2000–2500|1|1|Full reward|


viii 

