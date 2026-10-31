---
title: "PhysDrift: Bridging the Embodiment Gap in Humanoid Co-Speech Motion Generation"
date: "2026-06-18"
authors: "Zhangzhao Liang; Xiaofen Xing; Mingyue Yang; Wenlve Zhou; Xiangmin Xu"
url: https://arxiv.org/abs/2606.19935
pdf: https://arxiv.org/pdf/2606.19935
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.19935)** / [論文ページ](https://arxiv.org/abs/2606.19935)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# PhysDrift: Bridging the Embodiment Gap in Humanoid Co-Speech Motion Generation 

Zhangzhao Liang<sup>1</sup> , Xiaofen Xing<sup>_∗_1</sup> , Mingyue Yang<sup>2</sup> , Wenlve Zhou<sup>3</sup> , Xiangmin Xu<sup>_∗_3</sup> 1South China University of Technology 2DexForce Technology 3Foshan University 

> _∗_ Corresponding Author 

**_Abstract_ —Humanoid robots require co-speech motions that are not only expressive and speech-aligned, but also physically executable under embodiment constraints. Existing co-speech generation pipelines are predominantly human-centric: motions are first generated in human-body representations such as SMPLX and subsequently retargeted to humanoid robots. In this work, we identify a fundamental embodiment gap in this paradigm, where the mismatch between human motion manifolds and humanoid embodiment constraints disrupts embodiment consistency during motion transfer and physical execution. Through extensive analysis, we show that although retargeting can preserve coarse motion semantics, it significantly compresses motion diversity and weakens prosody-motion synchronization, limiting expressive humanoid behaviors. To address this problem, we first propose IK-EER, a prosody-preserving humanoid motion curation framework that jointly optimizes kinematic feasibility and speech-motion temporal alignment during retargeting. Building upon the curated robot-native motion dataset, we further introduce PhysDrift, an embodiment-aware co-speech motion generation framework that directly predicts executable humanoid joint trajectories from speech without relying on intermediate human-body representations. Unlike conventional human-centric pipelines, PhysDrift maintains embodiment consistency throughout both training and inference while incorporating physical regularization to stabilize robot motion dynamics. Extensive experiments and real-world humanoid deployment demonstrate that embodiment-aware robot-native generation substantially improves speech-motion alignment, physical plausibility, motion smoothness, inference efficiency, and real-time interaction capability. The results further reveal that robot-native motion representations are fundamentally more suitable than humancentric intermediates for embodied co-speech interaction in humanoid robots.** 

**_Index Terms_ —Co-Speech Motion, Retargeting, Motion Generation, Human-Robot Interaction.** 

## I. INTRODUCTION 

**H** UMANOIDral face-to-facerobotsinteractionare expectedwith humansto engage[1]–[5in], wherenatuspeech is tightly coupled with expressive body motion. Cospeech motions play a critical role in this process by conveying emphasis, rhythm, emotion, and conversational intent beyond verbal content alone. Recent advances in generative modeling have substantially improved the realism and diversity of human co-speech motion synthesis [6], [7]. These approaches demonstrate impressive capability in learning speech-motion correspondence from large-scale human motion datasets and have shown promising results for virtual avatars and digital humans. 

Despite this progress, transferring co-speech motion generation from virtual humans to physical humanoid robots remains 

fundamentally challenging. Similar to the motion of general humanoid robots, existing pipelines [8], [9] are predominantly human-centric: motion is first generated in human-body representations such as SMPL-X [10] and subsequently retargeted onto humanoid embodiments through inverse kinematics or optimization-based motion transfer. While effective for animation, this paradigm implicitly assumes that human motion representations are compatible with humanoid embodiment constraints. However, humanoid robots differ substantially from humans in kinematic structure, joint limits, actuation capability, balance constraints, and feasible motion manifolds. As a result, motion representations learned in human-centric latent spaces are not naturally aligned with the physically executable motion space of humanoid robots [11]. 

In this work, we identify and formalize this discrepancy as an _embodiment gap_ in humanoid co-speech motion generation. Unlike prior works that primarily focus on motion retargeting accuracy or kinematic feasibility, we show that the embodiment gap manifests more fundamentally as a distribution mismatch between human motion manifolds and robot-executable motion manifolds. Our experiments reveal that although modern retargeting methods can largely preserve coarse motion semantics and avoid severe joint violations, the retargeting process significantly compresses motion diversity and weakens prosody-motion synchronization. Consequently, expressive speech-driven motions learned in humancentric representations become progressively distorted during humanoid reconstruction and physical execution. 

A natural solution is to abandon human-centric intermediate representations and directly model humanoid co-speech behavior in robot joint space. However, robot-native generation introduces a new challenge. Without embodiment-aware constraints, highly expressive generative models, particularly flow-based models [12], can easily produce physically unstable motions with excessive jerk, contact artifacts, and jointlimit violations, despite achieving strong distributional metrics. Therefore, effective humanoid co-speech motion generation requires not only expressive generative capability, but also embodiment-consistent physical regularization. 

To address these challenges, we propose PhysDrift, an embodiment-aware robot-native framework for humanoid cospeech motion generation. Instead of relying on intermediate human-body representations, PhysDrift directly predicts executable humanoid joint trajectories from speech. To construct high-quality robot-native training data, we further introduce Inverse Kinematics-Energy Envelope Retargeting (IK-EER), a prosody-preserving humanoid motion curation framework that 

2 


Fig. 1. From human motion capture data to humanoid robot co-speech motion. The entire pipeline consists of four steps. First, data that clearly violates physical laws or severely distorts limbs in human motions is filtered out. Next, the proposed IK-EER maps human motions onto humanoid robots to obtain co-speech motions in the robot’s native motion space, while further removing data that does not match the robot’s attributes. Then, a PhysDrift generation model is trained using the robot’s co-speech motions. Finally, the whole-body controller takes the motion generated by PhysDrift as a reference to execute actions on the real robot. 

jointly optimizes kinematic feasibility and speech-motion temporal alignment during retargeting. Building upon the curated dataset, PhysDrift incorporates embodiment-aware regularization to stabilize generated motion dynamics while preserving speech-motion alignment and real-time generation capability. Fig. 1 provides an overview of the research presented in this paper. 

Extensive experiments across motion quality, physical feasibility, speech alignment, and deployment efficiency demonstrate that embodiment-aware robot-native generation substantially outperforms conventional human-centric pipelines. In particular, our method achieves superior speech-motion synchronization, smoother physical dynamics, significantly faster inference speed, and more stable humanoid execution while maintaining expressive motion diversity. We further validate the proposed framework through real-world humanoid deployment, demonstrating robust real-time co-speech interaction capability. 

Our contributions are summarized as follows: 

- We identify and formalize the embodiment gap in humanoid co-speech motion generation, showing that human-centric motion representations fundamentally disrupt embodiment consistency during retargeting and physical execution. 

- We propose IK-EER, a prosody-preserving humanoid motion curation framework that jointly considers kinematic feasibility and speech-motion temporal alignment during retargeting. 

- We propose PhysDrift, an embodiment-aware robotnative co-speech motion generation framework that directly predicts executable humanoid joint trajectories from speech without relying on intermediate human-body representations. 

- We demonstrate through extensive experiments and humanoid deployment that embodiment-aware generation substantially improves physical plausibility, motion smoothness, speech alignment, inference efficiency, and real-time interaction capability for humanoid co-speech motion. 

## II. RELATED WORK 

In this section, we review prior work from three perspectives closely related to humanoid co-speech motion generation: human-centric co-speech generation, motion retargeting for humanoid robotics, and robot-native humanoid motion generation. Unlike conventional categorizations, we particularly focus on how existing methods model the relationship between motion representation and physical embodiment, which forms the core challenge addressed in this work. 

## _A. Human-Centric Co-Speech Motion Generation_ 

Recent progress in co-speech motion generation has been primarily driven by the computer vision and graphics communities. Existing approaches typically formulate the task as generating human body motion conditioned on speech signals, where motions are represented in human skeletal spaces 

3 

or parametric body models such as SMPL-X. Large-scale conversational motion datasets have substantially accelerated this research direction. BEAT [13] and BEAT2 [14] provide multilingual conversational motion capture datasets with synchronized speech and body motion annotations. ZeroEGGS [15] further contributes high-fidelity expressive speaking styles for gesture synthesis. In parallel, large-scale Internet video datasets such as AVSpeech [16] and the TED Gesture Dataset [17] enable scalable learning of speech-driven gestures from unconstrained audio-visual data. Building upon these datasets, recent generative models have achieved remarkable progress in producing realistic and semantically meaningful human gestures. HOP [18] models multimodal interactions among speech, text, and gesture dynamics. SemGes [19] improves semantic consistency through local-global constraints. DIDiffGes [20] introduces an efficient decoupled diffusion framework for gesture generation, while MotionCraft [21] employs unified diffusion transformers for multimodal whole-body motion synthesis. Despite their impressive visual quality, these methods are fundamentally designed for digital humans rather than physically embodied humanoid robots. More importantly, their learned motion representations are intrinsically humancentric, assuming motion manifolds defined by human kinematics and morphology. Such representations do not explicitly account for embodiment-specific constraints including robot joint structures, actuator limitations, balance constraints, or physically executable humanoid motion spaces. Consequently, transferring these generated motions onto humanoid robots inevitably requires an additional embodiment transfer stage, introducing a mismatch between human motion representations and robot-executable behaviors. 

## _B. Motion Retargeting for Humanoid Robotics_ 

Motion retargeting aims to transfer human motion onto humanoid embodiments while preserving motion semantics and physical feasibility. In humanoid robotics, retargeting has become a practical strategy for leveraging large-scale human motion priors to improve robot motion generation and control. Traditional humanoid motion generation approaches [22]–[26] mainly rely on trajectory optimization or manually designed controllers. Although these methods achieve stable motion control, they often struggle to reproduce expressive and socially meaningful human motion dynamics. To address this limitation, recent retargeting frameworks attempt to transfer natural human movements onto humanoid embodiments. Recent studies have significantly improved the physical plausibility of retargeted humanoid motion. Jeong et al. [27] proposed a standardized retargeting framework addressing self-collision and contact consistency. Exbody [28] introduced local joint mapping strategies for transferring human motion onto the Unitree H1 humanoid platform. Lu et al. [29] refined inverse-kinematics-based upper-body retargeting to preserve natural motion characteristics under embodiment differences. Mao et al. [30] further demonstrated scalable retargeting pipelines for converting Internet-scale human motions into executable humanoid datasets. However, existing retargeting methods primarily optimize spatial pose reconstruction and 

physical feasibility while paying limited attention to embodiment consistency in speech-driven interaction. In particular, co-speech motions depends not only on pose accuracy but also on subtle temporal coupling between speech prosody and motion dynamics. Retargeting processes based on frame-wise inverse kinematics, smoothing, or projection into feasible robot subspaces often distort expressive motion distributions and weaken prosody-motion synchronization. As a result, motions that remain physically executable after retargeting may still lose expressive diversity and conversational naturalness during humanoid interaction. 

## _C. Robot-Native Humanoid Motion Generation_ 

More recent research has begun exploring robot-native humanoid motion generation frameworks that operate directly within robot action spaces instead of relying entirely on human-body intermediates. These methods aim to incorporate embodiment constraints during generation and control more explicitly. Several approaches explore language-conditioned humanoid generation and interaction. Harmon [31] combines human motion priors with vision-language reasoning for whole-body humanoid generation. Xu et al. [32] proposed a text-driven humanoid motion generation framework on the NAO platform using angle-space representations and reinforcement learning controllers. Bao et al. [33] introduced a hierarchical framework integrating intention reasoning and diffusion-based social gesture generation for humanoid interaction. Parallel advances have also emerged in imitation learning and diffusion-policy-based humanoid control. Ze et al. [34] combined teleoperation and diffusion policies for fullbody humanoid skill learning. HOVER [35] proposed a neural whole-body humanoid controller, while ManiDP [36] introduced manipulability-aware diffusion policies for bimanual humanoid manipulation. Although these methods operate more closely to robot embodiments, most focus on locomotion, manipulation, or general task-oriented motion rather than speechdriven social interaction. Moreover, many approaches still rely on human-derived motion priors, reference trajectories, or intermediate representations during training. Consequently, the problem of jointly preserving speech alignment, expressive motion dynamics, and embodiment-consistent physical execution remains insufficiently explored in humanoid co-speech motion generation. 

## _D. Summary_ 

Existing co-speech motion generation methods predominantly rely on human-centric motion representations and posthoc retargeting pipelines, while existing humanoid motion generation approaches mainly focus on task-oriented behaviors rather than expressive speech-driven interaction. As a result, current methods lack an explicit mechanism for maintaining embodiment consistency between speech prosody, expressive motion dynamics, and physically executable humanoid behavior. In contrast, this work proposes an embodiment-aware robot-native co-speech generation framework that jointly considers humanoid motion curation, embodiment-consistent motion representation, and physically grounded speech-driven generation directly within humanoid joint space. 

4 


Fig. 2. The feasible region of the end effectors and the joint rotation space between SMPL-X and Unitree-G1 are illustrated. In (a), the end effectors are the wrist and foot, which are common to both G1 and SMPL-X. (b) shows the joint rotation space of the shoulders, wrists, and hips for SMPL-X and Unitree-G1. 

## III. EMBODIMENT GAP ANALYSIS AND PROBLEM FORMULATION 

**Embodiment Gap.** The primary distinction between SMPL-X pose representation and robotic joint configuration lies in the nature of rotational freedom and physical constraints. For a given joint, SMPL-X uses an axis-angle representation: 

### TABLE I 

THE DIFFERENCE IN BODY STRUCTURE BETWEEN SMPL-X AND UNITREE-G1 

|Body|# Joints|DoF|Rotation Rep.|Rotation Restrict|
|---|---|---|---|---|
|SMPL-X|24 Body + 30 Fingers|162|Axis-Angle|_×_|
|G1|1 Root + 29 Body|29|Joint Angle|✓|


where **ˆu** _∈_ R<sup>3</sup> denotes the unit rotation axis satisfying _∥_ **ˆu** _∥_ = 1, _∥·∥_ denotes the Euclidean norm, and _θ_ is the rotation magnitude. This formulation allows arbitrary 3D orientations without consideration of mechanical limits or collisions, effectively sampling from the mathematical rotation group _SO_ (3). Consequently, SMPL-X can represent poses that are physically impossible for a real human or a robot, including extreme rotations or self-intersecting limbs. 

In contrast, a robot’s joint configuration is defined as 


where each _qi_ corresponds to a mechanically constrained degree of freedom (DoF), often restricted to rotation about a fixed axis. _qi_<sup>min</sup> and _qi_<sup>max</sup> denote the rotation range of the joint. These limits arise from actuator capabilities, structural design, collision avoidance, and stability requirements. Unlike SMPLX, robotic joints cannot arbitrarily rotate, and multiple axis rotations require solving inverse kinematics under constraints. 

The embodiment gap is summarized as Table I highlighting that while SMPL-X represents idealized human-like orientations, robotic joints encode physically realizable actuator configurations. 

**Problem Formulation.** Humanoid co-speech motion generation aims to synthesize expressive body motion conditioned 

on speech signals while maintaining physical executability on humanoid platforms [14], [31]. Given an input speech sequence _A_ = _{at}_<sup>_T_</sup> _t_ =1<sup>_,_the goal is to generate a corresponding</sup> humanoid motion sequence _Q_ = _{qt}_<sup>_T_</sup> _t_ =1<sup>,where</sup><sup>_qt∈_R</sup><sup>_D_de-</sup> notes the humanoid joint configuration at time step _t_ , including whole-body joint rotations and root motion parameters. 

Due to the lack of in-depth research on the co speech motion of native humanoid robots. Therefore, a more widespread approach is first generate motion in human-centric representations such as skeletal pose spaces or parametric body models, and subsequently transfer the generated motions onto humanoid embodiments through retargeting pipelines. This process can be summarized as 


where _H_ denotes motion represented in a human-body joint space and the second stage corresponds to humanoid retargeting. 

Although this paradigm has demonstrated strong visual performance for digital humans, it implicitly assumes that human motion representations are compatible with humanoid embodiment constraints. However, humanoid robots differ fundamentally from humans in morphology, kinematic structure, joint limits, actuation capability, and balance dynamics [28], 

5 

[37]. As a result, the feasible humanoid motion space does not coincide with the motion manifold learned from human motion data. Shown in Fig. 2 are the feasible region of the end effectors and the joint rotation manifold between SMPL-X and Unitree-G1. Bridging this gap requires mapping unconstrained human poses to constrained robot motions, typically via inverse kinematics with joint limits and collision avoidance. We denote the human motion manifold as _Mh_ and the physically executable humanoid motion manifold as _Mr_ . Existing human-centric generation methods effectively learn distributions over _Mh_ , while humanoid execution is constrained within _Mr_ . Since _Mh̸_ = _Mr_ , retargeting inevitably becomes a projection process from human motion space into the feasible humanoid motion subspace: 


Fig. 3. Pipeline of IK-EER. “Joint DoF” and “Root Position” are optimized through gradient-based motion refinement, while the root orientation is directly inherited from the human motion sequence. 

## IV. METHOD 


This discrepancy forms what we define as the _embodiment gap_ in humanoid co-speech motion generation. 

Importantly, the embodiment gap does not necessarily manifest as severe kinematic failure. Modern retargeting methods can often maintain basic physical feasibility and preserve coarse motion semantics. However, the projection from _Mh_ to _Mr_ inevitably compresses expressive motion distributions and alters fine-grained temporal dynamics. In co-speech interaction, where gesture rhythm, motion energy, and speech prosody are tightly coupled, such distortions accumulate into perceptually significant degradation of conversational naturalness. This phenomenon is particularly evident in expressive gestures. Human co-speech motions often rely on subtle upperbody coordination, asymmetric arm dynamics, and temporally localized motion emphasis synchronized with speech rhythm [38], [39]. During retargeting, these high-frequency expressive components are frequently smoothed or projected into more conservative feasible robot motions, reducing motion diversity and weakening prosody-motion synchronization even when the resulting motions remain physically executable. 

Our experimental analysis further confirms this observation. While retargeted motions retain relatively similar semantic alignment scores, motion diversity decreases substantially after retargeting across multiple generation methods. These results suggest that the primary limitation of human-centric pipelines is not merely physical feasibility, but the loss of embodiment consistency between expressive speech-driven motion dynamics and humanoid execution constraints. 

A natural solution is therefore to directly model humanoid co-speech motion within robot-native action spaces [31]. Instead of learning human motion distributions followed by embodiment transfer, we aim to directly learn the conditional distribution _p_ ( _Q|A_ ), where motion generation and embodiment constraints are jointly modeled within humanoid joint space. This formulation motivates the proposed PhysDrift framework, which combines embodiment-aware motion curation and robot-native speech-conditioned motion generation to preserve both expressive dynamics and physical executability. 

## _A. Overview_ 

The embodiment mismatch manifests in two aspects. First, human-centric representations contain large regions that are unreachable for humanoid embodiments, leading to unstable or over-smoothed motions after retargeting. Second, frame-wise inverse kinematics and motion smoothing operations distort subtle temporal patterns synchronized with speech rhythm and emphasis, which are essential for natural co-speech behavior. 

To address these issues, we reformulate humanoid cospeech motion generation as a direct robot-space generation problem. Instead of treating robotic embodiment as a postprocessing constraint, embodiment consistency is explicitly modeled during both dataset construction and motion generation. Our framework consists of two tightly coupled components. First, we propose IK-EER, an embodiment-aware humanoid motion construction framework that converts human co-speech motions into robot-native supervision while preserving speech-motion synchronization and physical feasibility. Second, we introduce PhysDrift, a robot-native speech-driven motion generation framework that directly learns executable humanoid motion distributions in joint space without relying on intermediate human-body representations. 

## _B. Embodiment-Aware Motion Construction_ 

Constructing a high-quality humanoid co-speech motion dataset is critical for robot-native motion generation. However, due to the lack of available robot co-speech motion, a common method is to retarget from human motion data to the robot body. Existing retargeting pipelines [40]–[42] primarily optimize spatial pose reconstruction fidelity, implicitly assuming that physically feasible reconstruction is sufficient for downstream learning. However, for co-speech motions, preserving temporal synchronization between speech prosody and motion dynamics is equally important. Motions that are physically executable but temporally inconsistent with speech often appear socially unnatural during interaction. 

To address this issue, we propose IK-EER, an embodimentaware motion construction framework designed not merely for pose transfer, but for generating robot-native supervision suitable for humanoid co-speech learning. The details of IKEER is shown in Fig. 3. 

6 

Starting from the BEAT2 dataset, We removed physically infeasible sequences from the source data (such as floating, twisted limbs, ground penetration). Instead of directly adopting SMPL-X parameters as training targets, all motions are transformed into the native joint space of the humanoid robot. For each frame, robot joint configurations are initialized through sparse human-to-robot keypoint correspondences using inverse kinematics. Let **q** denote robot joint angles. The initialization objective is formulated as 


where **p** _i_ and **R** _i_ denote the position and orientation of the corresponding robot joint _i_ . _wi_ is the weighting factor and _target_ denotes the target human motion position or orientation. 

Although inverse kinematics provides feasible initialization, conventional retargeting pipelines often weaken the intrinsic coupling between speech rhythm and motion dynamics due to smoothing and kinematic corrections. Human co-speech motions naturally exhibit strong correlations between acoustic emphasis and motion intensity. However, this relationship is highly sensitive to temporal distortion during embodiment projection. 

To preserve this synchronization, we introduce an Energy Envelope (EE) objective. The synchronization objective is defined using normalized cross-correlation (NCC) [43] bewteen motion energy _Em_ and audio energy _Ea_ : 


Due to the fact that movement speed is an important manifestation of motion rhythm, given a motion sequence **m** , motion energy is estimated from joint velocities: 


Similary, the raw waveform be denoted as **a** _∈_ R<sup>_B×L_</sup> . We first compute an 80-bin log-Mel spectrogram using an shorttime Fourier transform, yielding **S** _∈_ R<sup>_B×_80</sup><sup>_×T_</sup> . The framelevel log-Mel energy is then defined as 


where _ϵ_ = 10<sup>_−_6</sup> . Both signals are normalized before alignment. 

In addition, physical regularization terms _Lphys_ [44] are incorporated to enforce embodiment feasibility, including jointlimit penalties, foot-contact consistency, and skating suppression: 


Unlike conventional retargeting methods that prioritize geometric pose reconstruction, IK-EER explicitly prioritizes embodiment-consistent temporal dynamics. More importantly, IK-EER serves as a humanoid co-speech motion _curation framework_ rather than merely a retargeting algorithm. Since 

robot-native generation requires large-scale physically executable humanoid motion supervision, preserving speechmotion synchronization during humanoid reconstruction becomes essential for downstream learning. The resulting dataset provides robot-native motion distributions that simultaneously preserve embodiment feasibility and conversational expressiveness. 

## _C. Robot-Native Motion Representation_ 

Existing co-speech motion generation methods typically operate on human-centric representations such as SMPL-X parameters or discretized latent motion tokens. Although these representations are suitable for digital human animation, they introduce substantial embodiment mismatch for humanoid robots. 

From the perspective of motion manifolds, human-centric joint spaces contain large regions that are unreachable for robot embodiments due to differences in kinematic topology, actuation structure, and joint constraints. Consequently, learning in human representation space inevitably introduces representation-level embodiment inconsistency. 

To eliminate this mismatch, we directly represent motions in the native control space of the humanoid robot. For each frame, the motion state is defined as 


where **r** _root_ denotes the root orientation represented using continuous 6D rotation [45], _θi_ are robot joint angles, **p** _root_ represents the global root position, and superscript _(t)_ denotes the timestep _t_ . 

This formulation establishes a one-to-one correspondence between generated motion trajectories and executable motor commands, removing the need for intermediate humanbody reconstruction or post-hoc retargeting. More importantly, robot-native representation constrains motion learning directly within the feasible humanoid motion manifold, substantially reducing embodiment inconsistency during generation. 

## _D. PhysDrift_ 

Building upon the robot-native motion representation, we propose PhysDrift, a direct speech-to-motion generation framework that operates entirely in humanoid joint space. Unlike conventional co-speech generation pipelines that first model human motions and subsequently adapt them to robotic embodiments, PhysDrift directly learns the distribution of executable humanoid motions, thereby eliminating the embodiment gap introduced by intermediate human-body representations. Fig. 4 shows the pipeline of PhysDrift. 

Recent advances in generative modeling have demonstrated the effectiveness of diffusion models and Flow Matching for motion synthesis. In particular, Flow Matching learns a continuous transport process by estimating a velocity field 


which progressively transforms samples from a simple prior distribution into samples from the target motion distribution 

7 


Fig. 4. The proposed PhysDrift pipline. Left: the model architecture. Right: the loss function used during the training phase. Speech and text will be separately represented by modal encoders, and then fused with noisy motion sequences through cross-attention. Finally, the model outputs the corresponding predicted motion sequences. 

[46]. Compared with diffusion models, Flow Matching (FM) significantly reduces inference cost because the generation process can be formulated as deterministic trajectory transport. 

However, we identify that directly learning velocity fields introduces a previously overlooked form of embodiment gap when applied to humanoid co-speech motion generation. Velocity-field learning implicitly assumes that generated trajectories will be decoded or smoothed before execution. This assumption is generally valid for digital human animation, where latent motions are reconstructed through VQVAE [47] Decoder or rendering pipelines that naturally suppress highfrequency artifacts. In contrast, humanoid robots directly execute generated joint trajectories through motor controllers. Consequently, small velocity estimation errors are accumulated through temporal integration: 


causing local oscillations to propagate into large acceleration fluctuations. As a result, velocity-based transport often produces excessive motioaan jerk, unstable joint accelerations, and physically undesirable behaviors. This issue becomes particularly severe for co-speech motions, where subtle rhythmic variations synchronized with speech prosody create highfrequency motion components that are easily amplified during velocity integration. 

From an embodiment perspective, the root cause is that velocity fields are defined in the tangent space (the vector space formed by all possible “directions” or “velocities” at a certain point on a manifold) of the motion manifold 


where _T X_ denotes the tangent bundle of the motion manifold. Whereas humanoid execution is performed directly in configuration space (Eq. (10)). Therefore, minimizing velocity transport error does not necessarily minimize the execution error of robot motions since robot execution is ultimately performed in configuration space rather than velocity space. 

This mismatch constitutes a generation-level embodiment gap that remains even after robot-native motion representations are adopted. 

We address this issue by reformulating motion generation as a manifold attraction problem rather than a velocity transport problem, which leads to the proposed Motion Drift Field (MDF). To better understand its relationship with FM, we revisit the transport dynamics learned by velocity-based generative models. 

The continuous dynamics in Eq. (11) can be discretized as 


Therefore, FM can be interpreted as repeatedly predicting infinitesimal transport directions and accumulating them through numerical integration. While this formulation provides an accurate approximation of continuous transport trajectories, it requires the model to learn dynamics in tangent space rather than the robot execution space. 

Instead of learning infinitesimal transport directions, PhysDrift directly models the accumulated displacement between a generated sample and the feasible humanoid motion manifold. Let 


where **x**<sup>_∗_</sup> denotes an equilibrium state on the target humanoid motion manifold. The proposed MDF directly estimates this displacement: 


From this perspective, MDF can be viewed as a one-step relaxation formulation of velocity transport. Rather than explicitly learning tangent-space dynamics and integrating them over time, PhysDrift directly learns the correction required to move a sample toward the target motion manifold. Consequently, the transport process is implicitly absorbed into the network parameters during training. 

Let _p_ denote the distribution of robot-native motions constructed by IK-EER and let _q_ denote the generated motion 

8 

distribution. For a motion sample **x** , the MDF is formally defined as 


where **y**<sup>+</sup> _∼ p_ , **y**<sup>_−_</sup> _∼ q_ . In order to better adapt to the robot’s motion space, we have redefined _∥· ∥_ as a set of structured distances to accommodate different motion representations in Eq. (10), rather than _L_ 2 distance used in [48]. Specifically, for the root orientation **r** _root_ , we reconstruct the rotation using the 6D representation and map it to _SO_ (3). The distance between two orientations _d_ rot is measured using the geodesic distance on _SO_ (3). 


where **R**<sup>(1)</sup> _,_ **R**<sup>(2)</sup> _∈ SO_ (3) are the corresponding root rotation matrices. tr( _·_ ) represents the trace of the matrix. For joint angle _θi_ , we compute rotational differences using the periodic distance between joint angles. 


For the root position **p** _root_ , we measure positional errors _d_ pos using the _L_ 2 distance. In summary, 


The corresponding training objective minimizes the residual magnitude of the drift field: 


where sg( _·_ ) denotes the stop-gradient operator. The proposed formulation naturally possesses several desirable theoretical properties. 

**Proposition 1 (Equilibrium Property).** When the generated distribution matches the target distribution, the expected drift vanishes: 

An important consequence of the proposed attraction dynamics is that motion corrections are predicted directly in the robot execution space. Consequently, PhysDrift avoids derivative amplification caused by high-frequency motion components, substantially reducing motion jerk and improving temporal smoothness. This property is particularly important for physically embodied co-speech motion, where motion stability strongly influences interaction quality. 

To further preserve embodiment consistency during generation, we incorporate physical feasibility and speech-motion synchronization constraints. The final training objective is defined as 


## _E. Inference_ 

The proposed formulation naturally enables one-step generation. Conventional diffusion models require iterative denoising, while FM requires numerical integration of learned velocity trajectories. In contrast, PhysDrift directly learns the equilibrium correction that moves a sample toward the target humanoid motion manifold. 

Because the transport dynamics are absorbed into the learned MDF during training, the multi-step transport process is compressed into a single network evaluation. Therefore, inference does not require iterative denoising, trajectory rollout, or numerical ordinary differential equation integration. 

Given speech features **A** and Gaussian noise **_ϵ_** , humanoid motion is generated through a single forward pass: 


By directly learning motion-space attraction dynamics in robot configuration space, PhysDrift eliminates the generationlevel embodiment gap introduced by velocity transport, produces smoother and more physically executable trajectories, and enables real-time one-step humanoid co-speech motion generation. 

## V. EXPERIMENT 

## _A. Implemented Details._ 

We refer to the experimental settings in Syntalker [49] and GestureLSM [12]. All models used in the experiment were trained for 1000 epochs and optimized using Adam with a learning rate of 1e-4. The training process were conducted on single NVIDIA A100. 


This indicates that the target humanoid motion manifold corresponds to a stationary equilibrium of the learning dynamics. Furthermore, the kernelized formulation induces a local attraction process. Since the similarity kernel suppresses longrange interactions and emphasizes nearby motion samples, the resulting dynamics behave similarly to a contraction mapping in local neighborhoods. Consequently, generated motions are progressively attracted toward feasible humanoid motion regions while avoiding abrupt trajectory jumps. 

## _B. Evaluation Metrics_ 

To comprehensively evaluate humanoid co-speech motion generation, we consider multiple metrics covering speechmotion synchronization, motion distribution quality, physical feasibility, motion smoothness, and real-time inference capability. 

**Alignment** (Align.) [14] measures the temporal alignment between speech and generated motion. Specifically, it evaluates whether motion rhythm and motion energy changes 

9 

are synchronized with speech prosody and acoustic emphasis. Higher values indicate better speech-motion temporal consistency. 

**Diversity** [14] measures the variability of generated motions across different samples. Higher diversity indicates richer expressive motion distributions and reduced mode collapse. 

**FMD** (Fr´echet Motion Distance) evaluates the distributional similarity between generated motions and ground-truth motions. Similar to Fr´echet Inception Distance (FID) [50] in image generation and Fr´echet Gesture Distance (FGD) [14] in gesture generation, FMD computes the Fr´echet distance between feature distributions extracted from generated and real motion sequences. Lower values indicate that the generated motions are statistically closer to real humanoid motion distributions. 

**<u>G MPJPE</u>** (Global Mean Per Joint Position Error) [9] is defined as the average Euclidean distance between generated joint positions and reference joint positions in global coordinate space, measured in meters (m). Unlike local pose reconstruction metrics, <u>G MPJPE</u> additionally evaluates global spatial consistency of the reconstructed humanoid motion. Lower values indicate more accurate pose reconstruction. 

**Joint Violation** [9] is defined as the joint-angle violation beyond predefined humanoid joint limits during motion execution. 

**Foot Contact Distance** [51] evaluates the average height of the feet above the ground during frames that are expected to maintain foot contact, measured in meters (m). Lower values indicate more stable foot-ground contact behavior. 

**Skating Velocity** [51] quantifies the sliding velocity of the feet during contact phases, with the unit meters per second (m/s). Lower values indicate reduced foot skating artifacts and more physically plausible humanoid motion. 

**Jerk** is defined as the third-order temporal derivative of endeffector (wrist and foot) position trajectories, corresponding to the rate of change of acceleration, measured in meters per second cubed ( _m/s_<sup>3</sup> ). Lower jerk values indicate smoother and more physically stable humanoid motion dynamics. FMD, Align., and Diversity alone cannot accurately reflect highfrequency jitter; in fact, stronger jitter may even improve these metrics. Therefore, Jerk should be added as a core reference. Only when Jerk and the other three metrics are all within reasonable ranges can motion naturalness be assessed. 

**APS** (Actions Per Second) measures the number of motion frames generated per second during inference, reflecting endto-end latency from speech input to motion output. Higher APS indicates faster inference speed and stronger real-time interaction capability. 

## _C. Embodiment Gap in Human-Centric Co-Speech Generation_ 

We first analyze how retargeting affects speech-driven motion distributions in existing human-centric co-speech generation pipelines. Table II compares motion quality before and after humanoid retargeting across both ground-truth (GT) motions and generated motions from different co-speech generation models. 

TABLE II 

THE IMPACT OF RETARGETING ON SPEECH MOTION TEMPORAL ALIGNMENT AND MOTION DIVERSITY. “ALIGN.*” REFERS TO THE ALIGNMENT OF ONLY UPPER BODY AND HAND JOINT MOVEMENTS WITH SPEECH. “SYNTALKER” AND “GESTURELSM” MEANS DATA GENERATED BY SYNTALKER AND GESTURELSM MODEL. 

|Data|Retargeting|Align.*_↑_|Diversity_↑_|
|---|---|---|---|
|GT|_×_|0.6897|12.76|
|GT|✓|0.6600|7.319|
|Syntalker [49]|_×_|0.7359|12.31|
|Syntalker|✓|0.7291|9.527|
|GestureLSM_Diffusion_ [12]|_×_|0.7384|12.57|
|GestureLSM_Diffusion_|✓|0.7370|7.571|
|GestureLSM_ShortcutF low_ [12]|_×_|0.7490|12.46|
|GestureLSM_ShortcutF low_|✓|0.7447|7.525|


A consistent phenomenon can be observed across all methods: retargeting causes degradation in both speech-motion alignment and motion diversity. For example, the alignment score of GT motion decreases from 0.6897 to 0.6600 after retargeting and the diversity score drops substantially from 12.76 to 7.319. Similar trends can also be observed for Syntalker and GestureLSM. 

These results suggest that modern retargeting pipelines are generally capable of preserving coarse semantic correspondence between speech and motion. However, the projection from human motion space into feasible humanoid motion space substantially compresses expressive motion distributions. Instead of causing severe kinematic failure, the embodiment gap primarily manifests as a loss of expressive variability and temporal dynamics. This observation is consistent with the formulation introduced in Section 3, where retargeting acts as a projection from the human motion manifold _Mh_ into the feasible humanoid motion manifold _Mr_ . 

Importantly, co-speech interaction is highly sensitive to such distribution compression. Human co-speech gestures rely heavily on subtle rhythmic variations, asymmetric arm dynamics, and localized motion emphasis synchronized with speech prosody. During retargeting, these expressive components are often smoothed into more conservative feasible motions, resulting in weaker conversational expressiveness despite relatively preserved semantic alignment. 

## _D. Retargeting for Humanoid Co-Speech Motion Curation_ 

We further evaluate different humanoid retargeting strategies in Table III. Unlike conventional retargeting evaluation that focuses primarily on pose reconstruction accuracy, we additionally evaluate speech-motion alignment to analyze whether retargeted motions preserve conversational dynamics required for co-speech interaction. 

Existing retargeting baselines such as GMR, Mink, and PHC exhibit relatively poor physical quality and alignment performance. In particular, Mink and PHC produce severe skating artifacts with infinite skating velocity, indicating unstable contact behavior during humanoid execution. Their 

10 

TABLE III 

RETARGETING EXPERIMENT. GRADIENT-BASED REFERS TO OPTIMIZING BASED SOLELY ON THE REMAINING PHYSICAL LOSS FUNCTIONS IN FIG.3 WHILE WITHOUT USING IK INIT. AND EE LOSS. “NAN” MEANS THAT DUE TO THE REPOSITIONING, THE REAR ROBOT IS IN A SUSPENDED STATE AND CANNOT MEASURE THE SLIDING SPEED WHEN THE FOOT TOUCHES THE GROUND.BEST RESULTS IN **BOLD** , SECOND BEST <u>UNDERLINED.</u> 

|Method|G<br>MPJPE_↓_|Foot Contact Distance_↓_|Skating Velocity_↓_|Align._↑_|
|---|---|---|---|---|
|GMR [40]|0.72|0.024|0.19|0.59|
|Mink [41]|0.85|0.32|NaN|0.53|
|PHC [42]|0.88|0.35|NaN|0.50|
|Gradient-Based Optimization|**0.040**|0.0041|0.072|0.55|
|IK-EER (Ours)|0.046|**0.0019**|**0.063**|**0.69**|
|IK-EER w/o EE Loss|0.045|0.0019|0.063|0.55|


alignment scores also remain relatively low, ranging from 0.50 to 0.53. 

Optimization-based methods substantially improve physical feasibility. Gradient-Based optimization reduces <u>G MPJPE</u> from 0.72 to 0.040. Introducing inverse-kinematics initialization and end-effector constraints further stabilizes motion quality. The slight increase in <u>G MPJPE</u> can be attributed to motion matching with high-energy audio signals, where the increased motion amplitude leads to minor violations. 

However, the most important observation is that physical feasibility alone does not guarantee high-quality co-speech motion. Although Gradient-Based optimization and IK-EER w/o EE Loss achieve excellent kinematic metrics, their alignment scores remain limited at 0.55. In contrast, the full IK-EER framework improves alignment significantly to 0.69 while maintaining highly stable physical behavior. This result demonstrates that preserving speech-motion temporal synchronization is an independent and essential objective beyond conventional retargeting feasibility. 

More importantly, these results highlight the role of IK-EER as a humanoid co-speech motion curation framework rather than merely a retargeting algorithm. Since robot-native cospeech generation requires large-scale physically executable humanoid motion data, preserving prosody-motion coupling during humanoid reconstruction becomes critical for dataset quality. The proposed IK-EER framework enables the construction of robot-native co-speech datasets that simultaneously preserve embodiment feasibility and conversational dynamics. 

## _E. Effect of Motion Representation and Embodiment-Aware Generation_ 

Table IV investigates the influence of motion representation and generation framework design on humanoid co-speech generation. 

Using human-centric representations such as “6D w. VQVAE” leads to relatively poor distribution quality, achieving an FMD of 4.183. Removing VQVAE slightly improves diversity from 7.254 to 9.612, but the overall motion distribution remains significantly inferior to robot-native representations. In contrast, directly modeling humanoid motion using “6D Root & Joint Angle” dramatically improves motion distribution quality, reducing FMD to 0.6244. 

TABLE IV 

EXPERIMENT ON MOTION REPRESENTATION AND MODEL ARCHITECTURE ABLATION. BEST RESULTS IN **BOLD** , SECOND BEST <u>UNDERLINED.</u> 

|Motion Representation|Method|FMD_↓_|Align._↑_|Diversity_↑_|
|---|---|---|---|---|
|6D w. VQVAE|Diffusion|4.183|**0.7593**|7.254|
|6D w/o. VQVAE|Diffusion|4.165|0.6961|9.612|
|6D Root & Joint Angle|Diffusion|0.6244|0.6241|10.95|
|6D Root & Joint Angle|FM|**0.3799**|0.6746|**29.41**|
|6D Root & Joint Angle|PhysDrift|0.540|0.6803|11.17|


These results indicate that motion representation itself strongly influences embodiment consistency. Human-centric latent representations introduce structural mismatch between learned motion distributions and feasible humanoid motion spaces, whereas robot-native joint-space representations provide a more suitable representation for humanoid co-speech behavior. 

Flow-based generation further improves distribution learning capability. FM achieves the best FMD score of 0.3799 together with extremely high diversity of 29.41, demonstrating the strong expressive capability of flow matching models. However, as shown later in Table V, such unconstrained expressive generation also introduces severe jerk during humanoid execution. 

Compared with purely generative flow matching, PhysDrift achieves a more balanced trade-off between motion quality, alignment, and physical stability. Although its diversity is lower than unconstrained flow generation, PhysDrift maintains substantially better embodiment consistency while preserving competitive distribution quality. 

## _F. Overall Comparison_ 

Table V presents the overall comparison between humancentric pipelines, robot-native generation methods, and the proposed PhysDrift framework. 

Human-centric pipelines based on SMPL-X generation followed by retargeting exhibit limited motion diversity and relatively slow inference speed. For example, “Syntalker & GMR” achieves only 11.74 APS with a diversity score of 9.527. Although “GestureLSM _MeanF low_ & GMR” improves generation quality and speed, the resulting motion diver- 

11 

TABLE V 

COMPARATIVE EXPERIMENT BETWEEN DIGITAL HUMAN WITH RETARGETING PIPELINE AND ROBOT NATIVE GENERATION. “NFE” REFERS TO THE NUMBER OF FORWARD PROCESS STEPS REQUIRED FOR INFERENCE. “ _†_ ” INDICATES THAT THE MODEL IS MODIFIED TO ACCOMMODATE ROBOT MOTION REPRESENTATION. BEST RESULTS IN **BOLD** , SECOND BEST <u>UNDERLINED.</u> 

|Method|NFE|FMD_↓_|Aglin._↑_|Diversity_↑_|Joint Violation|Jerk_↓_|APS_↑_|
|---|---|---|---|---|---|---|---|
|GT|–|–|0.5366|7.319|_×_|86.59|–|
||SMPL-X &<br>|Retargeti<br>|ng<br>|||||
|Syntalker [49] & GMR [40]|1000|0.5633|0.6978|9.527|_×_|133.9|11.74|
|GestureLSM_ShortcutF low_ [12] & GMR [40]|2|0.7012|0.6781|7.769|_×_|141.6|40.51|
|GestureLSM_MeanF low_ [12] & GMR [40]|1|0.4241|0.6964|7.525|_×_|149.3|42.32|
|Robo|tic Native Mo|tion Repre|sentation|||||
|Syntalker_†_|1000|0.6244|0.6241|10.95|_×_|141.4|18.11|
|GestureLSM_ShortcutF low†_|2|**0.3799**|0.6747|**29.41**|✓|975.4|2010|
|GestureLSM_MeanF low†_|1|0.5542|**0.7102**|10.92|_×_|437.2|2350|
|PhysDrift (Ours)|**1**|0.5462|0.6856|12.20|_×_|118.0|**2880**|
|PhysDrift w/o. Joint Limitaion|1|0.5310|0.6901|11.64|✓|118.6|2880|
|PhysDrift w/o. Joint Limitaion & Energy Envelope|1|0.5409|0.6803|11.17|✓|**106.9**|2880|


sity remains constrained after retargeting, consistent with the embodiment-gap analysis in Table II. 

Robot-native generation substantially improves efficiency. Flow-based methods achieve extremely high inference throughput, with “GestureLSM _MeanF low_ ” reaching 2350 APS. Moreover, robot-native generation also avoids the diversity collapse introduced by retargeting. However, these methods often suffer from severe physical instability. “GestureLSM _ShortcutF low_ ” achieves very high diversity (29.41) and low FMD (0.3799), but simultaneously produces catastrophic joint violations and extremely high jerk (975.4), making the generated motions unsuitable for stable humanoid execution. According to the definition of Diversity, strong jitter may actually lead to higher scores. Therefore, high diversity scores alone does not necessarily indicate an advantage of the method in robot space. The high jerk of “GestureLSM _ShortcutF low_ ” and “GestureLSM _MeanF low_ ” also demonstrates that, without a VAE Decoder to smooth the motions, learning velocity fields is not suitable for the native motion space of robots. PhysDrift achieves a substantially better balance among expressiveness, physical plausibility, and real-time capability. Compared with unconstrained flow-based generation, PhysDrift reduces jerk from 437.2 to 118.0 while maintaining competitive diversity and alignment performance. 

The ablation variants further demonstrate the importance of embodiment-aware regularization. Removing joint constraints result in joint violations, while removing both Joint Limitation and Energy Envelope constraints reduces alignment and diversity simultaneously. These results confirm that embodimentaware constraints are essential for stabilizing robot-native cospeech generation. 

Overall, the experimental results consistently support the central hypothesis of this work: the primary limitation of existing co-speech pipelines lies not merely in physical feasibility, but in the embodiment inconsistency introduced by human-centric motion representations. By directly modeling 

speech-driven motion in robot joint space while incorporating embodiment-aware physical regularization, PhysDrift achieves more expressive, physically plausible, and real-time humanoid co-speech interaction. 

## VI. CONCLUSION 

In this work, we investigated the problem of humanoid cospeech motion generation from the perspective of embodiment consistency. Unlike existing human-centric pipelines that generate motion in intermediate human-body representations and subsequently retarget them onto humanoid robots, we showed that such approaches introduce a fundamental embodiment gap between human motion manifolds and physically executable humanoid motion spaces. Through extensive analysis, we demonstrated that the primary limitation of existing pipelines is not merely kinematic feasibility, but the distortion of expressive motion distributions and speech-motion temporal dynamics during embodiment transfer. 

To address this problem, we proposed an embodiment-aware robot-native co-speech generation framework composed of two complementary components. First, IK-EER enables prosodypreserving humanoid motion curation by jointly optimizing kinematic feasibility and speech-motion synchronization during retargeting. Building upon the curated robot-native dataset, PhysDrift directly models speech-conditioned humanoid joint trajectories while incorporating embodiment-aware physical regularization to stabilize motion dynamics and preserve expressive behavior. 

Experimental results consistently validated the proposed formulation of the embodiment gap. Our analysis showed that retargeting degraded speech-motion alignment and motion diversity, even when semantic information was largely preserved. Furthermore, while robot-native flow-based generation substantially improves expressiveness and inference efficiency, unconstrained generation often leads to unstable humanoid dynamics. By jointly modeling embodiment constraints and 

12 

expressive generation within robot joint space, PhysDrift achieves a substantially better balance between motion realism, physical plausibility, speech alignment, and real-time interaction capability. 

More broadly, this work suggests that humanoid co-speech generation should move beyond conventional human-centric motion representations toward embodiment-aware generative modeling directly grounded in robot morphology and dynamics. We believe that preserving embodiment consistency will become increasingly important for future socially interactive humanoid systems, where natural communication depends not only on semantic correctness, but also on physically grounded expressive motion. 

## REFERENCES 

- [1] W. Budiharto, A. D. Cahyani, P. C. Rumondor, and D. Suhartono, “Edurobot: Intelligent humanoid robot with natural interaction for education and entertainment,” _Procedia Computer Science_ , vol. 116, pp. 564–570, 2017. 1 

- [2] S. Ekstr¨om and L. Pareto, “The dual role of humanoid robots in education: As didactic tools and social actors,” _Educ. Inf. Technol._ , vol. 27, no. 9, pp. 12 609–12 644, 2022. 1 

- [3] L. Cui, Y. Li, X. Yang, X. Liu, L. Zhang, and L. Hou, “Humanoid robot–assisted support for health care in older adults: Systematic scoping review,” _JMIR Aging_ , vol. 9, p. e83849, 2026. 1 

- [4] U. Tripathi, R. S. J, V. Chamola, A. Jolfaei, and A. Chintanpalli, “Advancing remote healthcare using humanoid and affective systems,” _IEEE Sens. J._ , vol. 22, no. 18, pp. 17 606–17 614, 2022. 1 

- [5] W. Jutharee, B. Kaewkamnerdpong, and T. Maneewarn, “Joint reconfiguration after failure for performing emblematic gestures in humanoid receptionist robot,” _Sensors_ , vol. 23, no. 22, p. 9277, 2023. 1 

- [6] M. U. Saleem, M. J. Patel, E. Pinyoanuntapong, Z. Qin, L. Yang, H. Xue, A. Helmy, C. Chen, and P. Wang, “Livegesture: Streamable co-speech gesture generation model,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit., (CVPR)_ , Denver, Colorado, USA, Jun, 2026, pp. 2264–2273. 1 

- [7] F. Fang, S. Yang, and W. Yang, “Coordspeaker: Exploiting gesture captioning for coordinated caption-empowered co-speech gesture generation,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit., (CVPR)_ , Denver, Colorado, USA, Jun, 2026, pp. 30 761–30 771. 1 

- [8] K. Yin, W. Zeng, K. Fan, M. Dai, Z. Wang, Q. Zhang, Z. Tian, J. Wang, J. Pang, and W. Zhang, “Unitracker: Learning universal whole-body motion tracker for humanoid robots,” _IEEE Rob. Autom. Lett._ , vol. 11, no. 7, pp. 8124–8131, 2026. 1 

- [9] W. Xie, J. Han, J. Zheng, H. Li, X. Liu, J. Shi, W. Zhang, C. Bai, and X. Li, “Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills,” in _Proc. Adv. neural inf. proces. syst., (NeurIPS)_ , San Diego, CA, USA, 2025, pp. 62 406–62 433. 1, 9 

- [10] G. Pavlakos, V. Choutas, N. Ghorbani, T. Bolkart, A. A. A. Osman, D. Tzionas, and M. J. Black, “Expressive body capture: 3d hands, face, and body from a single image,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit., (CVPR)_ , Long Beach, CA, USA, Jun, 2019, pp. 10 975–10 985. 1 

- [11] H. Jia, J. Song, Y. Zhang, H. Jin, Y. Fan, W. Chen, W. Zhang, and Y. Yue, “ECHO: edge-cloud humanoid orchestration for language-tomotion control,” _arXiv preprint arXiv:2603.16188_ , 2026. 1 

- [12] P. Liu, L. Song, J. Huang, H. Liu, and C. Xu, “Gesturelsm: Latent shortcut based co-speech gesture generation with spatial-temporal modeling,” in _Proc. IEEE Int. Conf. Comput. Vis., (ICCV)_ . Honolulu, HI, USA: IEEE, Oct, 2025, pp. 10 929–10 939. 1, 8, 9, 11 

- [13] H. Liu, Z. Zhu, N. Iwamoto, Y. Peng, Z. Li, Y. Zhou, E. Bozkurt, and B. Zheng, “BEAT: A large-scale semantic and emotional multimodal dataset for conversational gestures synthesis,” in _Proc. Eur. Conf. Comput. Vis., (ECCV)_ , Tel Aviv, Israel, Oct. 2022, pp. 612–630. 3 

- [14] H. Liu, Z. Zhu, G. Becherini, Y. Peng, M. Su, Y. Zhou, X. Zhe, N. Iwamoto, B. Zheng, and M. J. Black, “EMAGE: towards unified holistic co-speech gesture generation via expressive masked audio gesture modeling,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit., (CVPR)_ , Seattle, WA, USA, Jun. 2024, pp. 1144–1154. 3, 4, 8, 9 

- [15] S. Ghorbani, Y. Ferstl, D. Holden, N. F. Troje, and M. Carbonneau, “Zeroeggs: Zero-shot example-based gesture generation from speech,” _Comput. Graph. Forum_ , vol. 42, no. 1, pp. 206–216, 2023. 3 

- [16] A. Ephrat, I. Mosseri, O. Lang, T. Dekel, K. Wilson, A. Hassidim, W. T. Freeman, and M. Rubinstein, “Looking to listen at the cocktail party: a speaker-independent audio-visual model for speech separation,” _ACM Trans. Graph._ , vol. 37, no. 4, p. 112, 2018. 3 

- [17] Y. Yoon, B. Cha, J. Lee, M. Jang, J. Lee, J. Kim, and G. Lee, “Speech gesture generation from the trimodal context of text, audio, and speaker identity,” _ACM Trans. Graph._ , vol. 39, no. 6, pp. 222:1–222:16, 2020. 3 

- [18] H. Cheng, T. Wang, G. Shi, Z. Zhao, and Y. Fu, “HOP: heterogeneous topology-based multimodal entanglement for co-speech gesture generation,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit., (CVPR)_ , Nashville, TN, USA, Jun, 2025, pp. 906–916. 3 

- [19] L. Liu, E. Ghaleb, A. Ozyurek, and Z. Yumak, “Semges: Semanticsaware co-speech gesture generation using semantic coherence and relevance learning,” in _Proc. IEEE Int. Conf. Comput. Vis., (ICCV)_ , Honolulu, Hawaii, USA, Oct, 2025, pp. 13 963–13 973. 3 

- [20] Y. Cheng, S. Huang, X. Chen, J. Ning, and M. Gong, “Didiffges: Decoupled semi-implicit diffusion models for real-time gesture generation from speech,” in _Proc. AAAI Conf. Artif. Intell., (AAAI)_ , T. Walsh, J. Shah, and Z. Kolter, Eds., Philadelphia, PA, USA, Mar, 2025, pp. 2464–2472. 3 

- [21] Y. Bian, A. Zeng, X. Ju, X. Liu, Z. Zhang, W. Liu, and Q. Xu, “Motioncraft: Crafting whole-body motion with plug-and-play multimodal controls,” in _Proc. AAAI Conf. Artif. Intell., (AAAI)_ , T. Walsh, J. Shah, and Z. Kolter, Eds., Philadelphia, PA, USA, Mar, 2025, pp. 1880–1888. 3 

- [22] S. Kajita, F. Kanehiro, K. Kaneko, K. Fujiwara, K. Harada, K. Yokoi, and H. Hirukawa, “Biped walking pattern generation by using preview control of zero-moment point,” in _Proc. IEEE Int. Conf. Robot. Autom., (ICRA)_ , Taipei, Taiwan, China, Sep, 2003, pp. 1620–1626. 3 

- [23] S. Feng, E. C. Whitman, X. Xinjilefu, and C. G. Atkeson, “Optimization based full body control for the atlas robot,” in _IEEE-RAS Int. Conf. Humanoid Rob._ , Madrid, Spain, Nov, 2014, pp. 120–127. 3 

- [24] W. Suleiman, F. Kanehiro, E. Yoshida, J. Laumond, and A. Monin, “Time parameterization of humanoid-robot paths,” _IEEE Trans. Robot._ , vol. 26, no. 3, pp. 458–468, 2010. 3 

- [25] H. T. Kalidindi, A. Balachandran, and S. V. Shah, “Optimal wholebody motion planning of humanoids in cluttered environments,” _Robotics Auton. Syst._ , vol. 118, pp. 263–277, 2019. 3 

- [26] M. F. Stollenga, L. Pape, M. Frank, J. Leitner, A. F¨orster, and J. Schmidhuber, “Task-relevant roadmaps: A framework for humanoid motion planning,” in _2013 IEEE/RSJ Int. Conf. Intell. Robots Syst., (IROS)_ , Tokyo, Japan, Nov, 2013, pp. 5772–5778. 3 

- [27] T. Jeong, Y. Chai, S. Choi, J. Bak, C. Kim, J. Yoon, Y. Lee, J. Lee, K. Lee, J. Kim, and S. Choi, “Core: A hybrid approach of contact-aware optimization and learning for humanoid robot motions,” in _IEEE-RAS Int. Conf. Humanoid Rob._ , Seoul, Republic of Korea, Sep, 2025, pp. 293–300. 3 

- [28] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “Expressive whole-body control for humanoid robots,” in _Robotics: Science and Systems XX_ , Delft, The Netherlands, Jul, 2024. 3, 4 

- [29] C. Lu, X. Cheng, J. Li, S. Yang, M. Ji, C. Yuan, G. Yang, S. Yi, and X. Wang, “Mobile-television: Predictive motion priors for humanoid whole-body control,” in _Proc. IEEE Int. Conf. Robot. Autom., (ICRA)_ , Atlanta, GA, USA, May, 2025, pp. 5364–5371. 3 

- [30] J. Mao, S. Zhao, S. Song, C. Hong, T. Shi, J. Ye, M. Zhang, H. Geng, J. Malik, V. Guizilini, and Y. Wang, “Universal humanoid robot pose learning from internet human videos,” in _IEEE-RAS Int. Conf. Humanoid Rob._ , Seoul, Republic of Korea, Sep, 2025, pp. 1–8. 3 

- [31] Z. Jiang, Y. Xie, J. Li, Y. Yuan, Y. Zhu, and Y. Zhu, “Harmon: Whole-body motion generation of humanoid robots from language descriptions,” in _Proc. Conf. Robot Learning, (CoRL)_ , Munich, Germany, Nov, 2024, pp. 3015–3026. 3, 4, 5 

- [32] Z. Xu, M. Hu, K. Xiao, Q. Fang, C. Liu, and Q. Chen, “Realizing text-driven motion generation on NAO robot: A reinforcement learningoptimized control pipeline,” _arXiv preprint arXiv:2506.05117_ , 2025. 3 

- [33] L. Bao, Y. Pan, T. Peng, D. Kanoulas, and C. Zhou, “Hierarchical intention-aware expressive motion generation for humanoid robots,” _arXiv preprint arXiv:2506.01563_ , 2025. 3 

- [34] Y. Ze, Z. Chen, W. Wang, T. Chen, X. He, Y. Yuan, X. B. Peng, and J. Wu, “Generalizable humanoid manipulation with 3d diffusion policies,” in _Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst.,(IROS)_ , Hangzhou, China, Oct, 2025, pp. 2873–2880. 3 

- [35] T. He, W. Xiao, T. Lin, Z. Luo, Z. Xu, Z. Jiang, J. Kautz, C. Liu, G. Shi, X. Wang, L. J. Fan, and Y. Zhu, “HOVER: versatile neural whole-body controller for humanoid robots,” in _Proc. IEEE Int. Conf. Robot. Autom., (ICRA)_ , Atlanta, GA, USA, May, 2025, pp. 9989–9996. 3 

13 

- [36] Z. Li, J. Liu, D. Li, T. Teng, M. Li, S. Calinon, D. G. Caldwell, and F. Chen, “Manidp: Manipulability-aware diffusion policy for posturedependent bimanual manipulation,” in _Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst.,(IROS)_ , Hangzhou, China, Oct, 2025, pp. 9956–9962. 3 

- [37] A. Tang, T. Hiraoka, N. Hiraoka, F. Shi, K. Kawaharazuka, K. Kojima, K. Okada, and M. Inaba, “Humanmimic: Learning natural locomotion and transitions for humanoid robot via wasserstein adversarial imitation,” in _Proc. IEEE Int. Conf. Robot. Autom., (ICRA)_ , Yokohama, Japan, May, 2024, pp. 13 107–13 114. 4 

- [38] X. Qi, C. Liu, L. Li, J. Hou, H. Xin, and X. Yu, “Emotiongesture: Audio-driven diverse emotional co-speech 3d gesture generation,” _IEEE Trans. Multimedia_ , vol. 26, pp. 10 420–10 430, 2024. 5 

- [39] C. Fu, Y. Wang, H. He, S. Wang, C. Wang, Y. Tai, Y. Liu, and J. Zhang, “Mambagesture2: Co-speech gesture generation via hierarchical fusion and spatiotemporal aggregation,” _IEEE Trans. Multimedia_ , vol. Early Access, pp. 1–9, 2026. 5 

- [40] J. P. Ara´ujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu, “Retargeting matters: General motion retargeting for humanoid motion tracking,” _arXiv preprint arXiv:2510.02252_ , 2025. 5, 10, 11 

- [41] K. Zakka. (2026, Feb.) Mink: Python inverse kinematics based on MuJoCo. [Online]. Available: https://github.com/kevinzakka/mink 5, 10 

- [42] Z. Luo, J. Cao, A. Winkler, K. Kitani, and W. Xu, “Perpetual humanoid control for real-time simulated avatars,” in _Proc. IEEE Int. Conf. Comput. Vis., (ICCV)_ , Paris, France,, Oct, 2023, pp. 10 861–10 870. 5, 10 

- [43] G. Li, H. Shao, X. Deng, and Y. Jiang, “Adaptive convolutional network pruning through pixel-level cross-correlation and channel independence for enhanced model compression,” _Eng. Appl. Artif. Intell._ , vol. 154, p. 110920, 2025. 6 

- [44] K. Lee, S. Kim, M. Park, H. Kim, D. Hwang, H. Lee, and J. Choo, “PHUMA: physically-grounded humanoid locomotion dataset,” _arXiv preprint arXiv:2510.26236_ , 2025. 6 

- [45] Y. Zhou, C. Barnes, J. Lu, J. Yang, and H. Li, “On the continuity of rotation representations in neural networks,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit., (CVPR)_ , Long Beach, CA, USA, Jun, 2019, pp. 5745–5753. 6 

- [46] Y. Lipman, R. T. Q. Chen, H. Ben-Hamu, M. Nickel, and M. Le, “Flow matching for generative modeling,” in _Proc. Int. Conf. Learn. Represent.,(ICLR)_ , Kigali, Rwanda, May, 2023. 7 

- [47] A. van den Oord, O. Vinyals, and K. Kavukcuoglu, “Neural discrete representation learning,” in _Proc. Adv. neural inf. proces. syst., (NeurIPS)_ , Long Beach, CA, USA, 2017, pp. 6309–6318. 7 

- [48] M. Deng, H. Li, T. Li, Y. Du, and K. He, “Generative modeling via drifting,” _arXiv preprint arXiv:2602.04770_ , 2026. 8 

- [49] B. Chen, Y. Li, Y.-X. Ding, T. Shao, and K. Zhou, “Enabling synergistic full-body control in prompt-based co-speech motion generation,” in _Proceedings of the 32nd ACM International Conference on Multimedia_ . New York, NY, USA: ACM, 2024, p. 10. 8, 9, 11 

- [50] M. Heusel, H. Ramsauer, T. Unterthiner, B. Nessler, and S. Hochreiter, “Gans trained by a two time-scale update rule converge to a local nash equilibrium,” in _Proc. Adv. neural inf. proces. syst., (NeurIPS)_ , Long Beach, California, USA, Dec, 2017, pp. 6629–6640. 9 

- [51] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi, “Omniretarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction,” _arXiv preprint arXiv:2509.26633_ , 2025. 9 

