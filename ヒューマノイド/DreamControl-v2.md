---
title: "DreamControl-v2: Simpler and Scalable Autonomous Humanoid Skills via Trainable Guided Diffusion Priors"
date: "2026-03-31"
authors: "Sudarshan Harithas; Sangkyung Kwak; Pushkal Katara; Srujan Deolasee; Dvij Kalaria; Srinath Sridhar"
url: https://arxiv.org/abs/2604.00202
pdf: https://arxiv.org/pdf/2604.00202
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.00202)** / [論文ページ](https://arxiv.org/abs/2604.00202)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **DreamControl-v2: Simpler and Scalable Autonomous Humanoid Skills via Trainable Guided Diffusion Priors** 

Sudarshan Harithas<sup>1</sup><sup>_,_2</sup> , Sangkyung Kwak<sup>1</sup> , Pushkal Katara<sup>1</sup> , Srujan Deolasee<sup>1</sup> , Dvij Kalaria<sup>1</sup><sup>_,_3</sup> , Srinath Sridhar<sup>2</sup> , Sai Vemprala<sup>1</sup> , Ashish Kapoor<sup>1</sup> , Jonathan Chung-Kuan Huang<sup>1</sup> 


Fig. 1: **DreamControl-v2 enables scalable and autonomous humanoid skill acquisition.** We demonstrate diverse real-world skills (left), including Drawer Open, Deep Squat & Pick , and Punch. The right panel compares the reference trajectory generation pipelines used before RL: DreamControl relies on a fixed human motion diffusion model, and requires trial-and-error prompting (�) and manual filtering, whereas DreamControl-v2 trains a native humanoid diffusion prior from large heterogeneous datasets. Retargeting is performed before training, yielding cleaner task-ready trajectories and a pipeline that scales more easily. 

**_Abstract_ — Developing robust autonomous loco-manipulation skills for humanoids remains an open problem in robotics. While RL has been applied successfully to legged locomotion, applying it to complex, interaction-rich manipulation tasks is harder given long-horizon planning challenges for manipulation. A recent approach along these lines is DreamControl, which addresses these issues by leveraging off-the-shelf human motion diffusion models as a generative prior to guide RL policies during training. In this paper, we investigate the impact of DreamControl’s motion prior and propose an improved framework that trains a guided diffusion model directly in the humanoid robot’s motion space, aggregating diverse human and robot datasets into a unified embodiment space. We demonstrate that our approach captures a wider range of skills due to the larger training data mixture and establishes a more automated pipeline by removing the need for manual filtering interventions. Furthermore, we show that scaling the generation of reference trajectories is important for achieving robust downstream RL policies. We validate our approach through extensive experiments in simulation and on a real Unitree-G1. Project website: https: //genrobo.github.io/DreamControl-v2/** 

## I. INTRODUCTION 

Recently there have been major advancements in methods for teleoperating humanoid robots [1]–[3], but learning fully autonomous humanoid skills remains a critical challenge, generally requiring a significant amount of data not readily available on the web. A promising trend involves utilizing generative priors to produce “plausible” robot trajectories (conditioned, e.g., on a text snippet), which are then fed to an Reinforcement Learning (RL) policy to be followed as 

> 1General Robotics, USA: Work partially conducted while Sudarshan Harithas and Dvij Kalaria were at General Robotics. 

> 2Brown University, USA. 

> 3University of California, Berkeley, USA. 

targets [4], [5]. This approach leads to solutions that look human and often transfer more readily to a real robot [4]–[6]. 

A recent contribution along these lines is the DreamControl framework [5], which proposed a two stage pipeline for training humanoid policies: **(1)** first sampling trajectories from a guided diffusion model followed by **(2)** training an RL policy to track these sampled trajectories (essentially to be teleoperated by these “dreamed” trajectories) while simultaneously accomplishing some task of interest autonomously. A key benefit of DreamControl is its ability to train policies capable of autonomous environment interactions — leveraging the diffusion model guided by both text and spatio-temporal constraints, allowing for fine-grained control over the timing of contact with various objects in the environment. 

Despite some impressive initial results, DreamControl has limited scalability and general utility due to multiple technical issues. Specifically, DreamControl is built upon a generate-then-retarget pipeline. It first uses OmniControl [7]—a diffusion model trained exclusively on human motion capture (mocap) data—to generate human-centric motion data, which are subsequently retargeted to a specific robot form factor, such as the Unitree- _G_ 1. While convenient, this process induces various bottlenecks. First, spatial conditioning is enforced in the human body space rather than the robot’s embodiment. During reference trajectory generation– for example, given the instruction “pick a box from the ground” and a spatio-temporal constraint _x_ ( _t_ ) for the hands to approaching and lifting the box, a human motion trajectory is generated through OmniControl [7] where the human hand follows _x_ ( _t_ ). However, after retargeting this motion to the Unitree G1, the robot’s end-effector no longer follows _x_ ( _t_ ), but instead arrives at a different position _x_ 1( _t_ ). The spatial constraint satisfied in human space is therefore 

not preserved in robot space. To compensate, practitioners manually adjust the input spatial condition—prompting the human model to reach a different location _x_ 2( _t_ ), hoping that after retargeting, the robot will approximate _x_ ( _t_ ). Because the human-motion motion model can generate humans at an arbitrary scale, the parameter _x_ 2( _t_ ) must be found through trial-and-error. This manual tuning process is labor-intensive and bottlenecks scalability, and is especially difficult for longhorizon (tens of seconds), and high-dimensional humanoid loco-manipulation tasks [5], [6]. Secondly, models such as OmniControl [7] can primarily generate AMASS [8], [9] style actions, which are in general not relevant for various robotics tasks. To address these limitations, DreamControl [5] proposes several workarounds, including the use of Inverse Kinematics (IK) on tasks not covered within AMASS (such as the Drawer Opening task) and also employs manual filtering of generated trajectories. This reliance on taskspecific fixes and human intervention inherently restricts the overall scalability of the original DreamControl approach. 

To address these limitations, DreamControl-v2 trains a guided diffusion model directly in the target robot’s action space (e.g., Unitree- _G_ 1). Specifically, we construct a robotspace dataset by pre-retargeting a diverse mixture of human motion datasets to the Unitree- _G_ 1 form factor, and use this dataset to train a flexible robot-motion generation model. Integrating this model into a DreamControl-inspired workflow streamlines the pipeline and yields two advantages: ( **1** ) By expanding the training data beyond AMASS [8], the model can now capture a diverse range of actions. Coupled with the automated filtering process, this approach removes the requirement of task-specific IK and the need for manual trajectory filtering. Replacing the out-of-the-box OmniControl model with the DreamControl-v2 demonstrates scaling and simplicity (Sec. IV-C, Sec. IV-D). ( **2** ) The DreamControl-v2 diffusion model can now directly generate and accept spatial guidance within the robot’s state space, eliminating post-hoc retargeting and the associated trial-and-error tuning (Sec. IV-D.2). Finally, we conduct a detailed analysis of the diffusion model, its effects on downstream RL performance (Sec. IV), and validate our approach with real-world experiments on the Unitree- _G_ 1. 

## II. RELATED WORKS 

## _A. Motion Synthesis for Robots_ 

The success of generative models in domains such as text [10], [11] and images [12] has motivated a range of robotics works that similarly generate actions for manipulation and navigation tasks [13]–[16]. With the availability of largescale human motion datasets such as AMASS [8], motion generation methods have adopted diffusion-based [7], [17] and autoregressive [18]–[20] architectures for human motion synthesis. These approaches generate motion trajectories for a human conditioned on textual descriptions [17], [19], [20] and spatio-temporal constraints [7], [21]. The robustness of these generative modeling techniques has led humanoid robots to adopt similar formulations. CLOS-D [4] builds a closely coupled diffusion and RL pipeline to generate physically plausible actions for an animated humanoid. Similarly, Humanoid- 

X [22] learns only a text-conditioned model for trajectory generation that is subsequently tracked by a whole-body RL controller. In comparison, the DreamControl-v2 diffusion model can generate trajectories jointly conditioned on both open vocabulary text and spatio-temporal constraints, and performs tasks on a real-robot. 

## _B. Physics-Based Motion Imitation_ 

Motion imitation addresses the problem of constructing controllers that enable physics-based tracking of reference motions. Such motion-tracking formulations provide a general mechanism for acquiring diverse behaviors on humanoid robots. A large body of work has focused on tracking motions for simulated humanoid characters. Classical approaches rely on optimization-based controllers [23] to mimic reference trajectories. With the advent of learning-based methods, RL has been used to train tracking controllers in simulation [1]– [3], [24]–[27]. More recently, several works have coupled RL with generative priors [4], [6], [28] for motion tracking and scene interactions within simulation. However, accurate tracking of a motion reference alone does not constitute autonomous execution. Methods that require a reference trajectory at inference time are inherently constrained, making them more suitable for teleoperation [1], [3]. Such reliance on reference trajectories during deployment limits a model’s ability to autonomously adapt to novel environments and task variations. Inspired by prior work such as OmniGrasp [6], both DreamControl and DreamControl-v2 reformulate motion tracking as a reward signal rather than an input observation. This design enables policies to execute autonomously at inference time and facilitates direct sim-to-real deployment. 

## _C. Data Sources for Humanoid Loco-Manipulation_ 

Prior work has explored several data sources for learning loco-manipulation skills on humanoid robots. One line of research relies on human teleoperation, where skilled operators control the robot to collect high-quality, task-specific demonstrations with real-time feedback [1]–[3], [27], [29], [30]. While effective for bootstrapping particular tasks, it is inherently expensive and difficult to scale to the breadth of skills required for general-purpose humanoids. Another line of work leverages human motion data captured through either Mocap or from RGB videos, primarily for their volume and diversity [22], [31]–[33]. In contrast to approaches that directly use these motions for physically plausible humanoid control [32], [33], DreamControl-v2 first trains a generative prior on diverse human datasets, enabling it to synthesize motions spanning a wide range of interactive tasks. 

## III. DREAMCONTROL-V2 METHODOLOGY 

We first review the original DreamControl approach, which begins by generating robot trajectories using an off-the-shelf diffusion prior (OmniControl [7]). These trajectories are retargeted to the Unitree- _G_ 1 embodiment and are constrained to satisfy spatio-temporal requirements, such as making contact with an object at a pre-defined location and time. An RL policy is subsequently trained, which receives a reward 


Fig. 2: **DreamControl-v2 Overview.** Our four-stage pipeline enables humanoid whole-body manipulation: (1) large-scale human motion datasets are retargeted into a unified robot-space; (2) a humanoid motion diffusion model is trained to generate reference trajectories conditioned on text and spatio-temporal control signal; (3) multiple reference trajectories are used to train a physics-based RL policy; (4) The learned policy is deployed in simulation and on a real robot. 

for both successfully accomplishing the task of interest and for accurately tracking the provided reference trajectory. 

DreamControl-v2 takes an identical approach to RL and sim-to-real, but differs in the first stage of the pipeline — in this section, we focus on the method for training the diffusion prior to generating humanoid robot trajectories (see Fig. 2). 

## _A. Massive Human Data to Robot-Space_ 

To train our humanoid motion diffusion model, we construct a large-scale robot-space dataset by retargeting diverse human motion sequences spanning a wide range of activities and interactions into the unified kinematic space of the _G_ 1 humanoid embodiment. This yields a consistent representation suitable for model training. Conveniently, we can easily train on a union of human mocap datasets and newly collected teleoperated data (and thus we have a way to extend the prior to new tasks if they are not already included in the prior). 

_1) Data Sources:_ Our data pool is primarily composed of large-scale human motion datasets AMASS/HumanML3D [8], [9], GRAB [34], and Nymeria [35] which collectively cover locomotion, everyday activities, and rich human–object interactions. We also incorporate robot trajectories from OmniRetarget [33], which originate from human data [36] but have undergone additional RL and physics-based refinement, resulting in improved bimanual manipulation motions. These human- and robot-sourced datasets span complementary regions of the motion distribution, enabling our model to learn diverse, whole-body interaction behaviors. 

_2) Human-to-Robot Retargeting:_ We retarget all human motion trajectories in our dataset to the _G_ 1 humanoid. The retargeting process begins by selecting a set of keypoints on the human body ( _Phuman_ ), specifically 12 joints shared between human and robot, including the hips, knees, ankles, shoulders, elbows, and wrists. We then solve an optimization problem ( _Fretarget_ ) given in Eq. 1, that minimizes differences in relative joint angles, relative keypoint positions, foot slip, 

and a scale factor that compensates for the difference in link lengths between the human body and the _G_ 1 robot. The optimization problem results in the joint angles ( _qrobot_ ) and global ( `SE` ( `3` )) poses ( _Trobot_ ) for the _G_ 1 at every timestep: 


Our retargeting system is built over pyroki [37] that uses JAX [38] based solvers to perform the optimization. We further enhance the efficiency by implementing a single compilation and caching system, along with multi-thread process, which prevents multiple re-compilations overheads. 

_3) Handling Non-SMPL Parameterizations:_ Datasets such as AMASS [8] and GRAB [34] represent human motion using the SMPL kinematic model [39]. In contrast, Nymeria [35] capture motion with Xsens body suits [40], producing joint trajectories defined in an alternative kinematic skeleton. This mismatch, especially in the definition and placement of the pelvis and hip keypoints, introduces inconsistencies between the Xsens and SMPL keypoint sets. To resolve these differences, we solve the optimization in Eq. 2 to recover SMPL parameters: the joint angles _θ_ and global pose _T_ pose _∈_ SE(3) that best explain the Xsens keypoint observations. Here, _F_ smpl denotes the SMPL _differentiable forward kinematics_ mapping ( _θ, T_ pose) to 3D SMPL keypoints. We employ a confidence-weight vector **w** that assigns higher weights to reliable joints (e.g., wrists, knees, ankles) and lower weights elsewhere. The resulting SMPL parameters produce keypoints that are consistent with AMASS and GRAB. 


_4) Filtering and Pre-processing:_ Not all raw trajectories are suitable for training, so we apply the feasibility filters from PHC [41], [42] to remove motions which are infeasible without environment context (e.g., “treadmill running” is 

not possible to transfer to humanoid without knowing the speed of the belt.). Nymeria additionally contains text annotations describing atomic actions; we use a keyword-based retrieval to extract task-specific segments e.g., “drawer”, “open”, “cabinet” for articulated object manipulation. The keyword-based search returns timestamped trajectories that are associated with a particular keyword. We segment the trajectory using the timestamps and include it in the dataset. Lastly, we do not apply any filtering over the GRAB [34] and OmniRetarget [33] sequences. 

## _B. Diffusion Prior Training_ 

Given the Robot-Space dataset containing _G_ 1 motion trajectories (from Sec. III-A), we train a diffusion model generating reference trajectories ( _T ∈_ R<sup>_N×D_</sup> ) conditioned on open vocabulary text instructions **p** and spatio-temporal control signals **c** _∈_ R<sup>_N×J×_3</sup> over any joint at any time, where _N_ is the length of the trajectory, _J_ is the number of joints, and _D_ is the dimension of the _G_ 1 pose representation. The control signal **c** provides 3D-control positions per-joints across timestamps (or for a select number of key frames), while for all other joints that are left unconstrained is set to zero. For example, in the Drawer Open task, the text and spatial controls jointly specify: “open the drawer” while constraining the right wrist to reach the drawer handle at position _xyz_ at time _tj_ , the intended interaction moment. Depending on the task, the spatio-temporal controls may be sparse and provided for only one or two joints, while the text instruction remains fully open-vocabulary. 

_1) Trajectory Parameterization:_ Given the structural similarities between humans and humanoid robots, we adopt the trajectory parameterization commonly used in human motion generation [9]. Specifically, we utilize the canonicalized SMPL representation [9], which defines 22 keypoints [39] within a local, root-centered coordinate frame. By selecting 22 semantically corresponding joints on the _G_ 1 humanoid and processing them through the identical pipeline, we achieve a _G_ 1 trajectory representation equivalent to the SMPL format. This alignment allows for the direct adaptation and fine-tuning of prior human motion models for humanoid control. 

After retargeting, each _G_ 1 trajectory is represented as a sequence of poses _T_ = [ _x_ 0 _, x_ 1 _, . . . , xn_ ], where each pose consists of the robot joint angles and global pose: _xt_ = ( _q_ robot _, T_ robot). Following the pre-processing in [9], [17], [33], we (1) resample all trajectories to 20 FPS, (2) crop or pad them to a maximum duration of 10 seconds, and (3) canonicalize orientations by rotating each sequence so the root at timestep _t_ = 0 faces the _Z_ + direction. Each processed pose is encoded as _xt_ = ( ˙ _ra, r_ ˙ _xz, ry, jp, jv, jr, cf_ ) _∈ R_<sup>263</sup> where _rxz_ ˙ _∈_ R<sup>2</sup> is the root planar velocity, _ra_ ˙ _∈_ R is the root angular velocity, _ry ∈_ R is the root height, _jp, jv ∈_ R<sup>3</sup><sup>_k_</sup> denote joint positions and velocities, _jr ∈_ R<sup>6</sup><sup>_k_</sup> is the 6D rotation representation, and _cf ∈_ R<sup>4</sup> contains foot contact features, which are binary values (2 values per foot) indicating contact (or no-contact) with the floor near the toe and heels. with _k_ = 22 joints. 

_2) Training Strategy:_ Our trajectory parameterization enables adapting existing human motion generation pipelines for humanoid control. Here, we use the OmniControl architecture [7] initialized with MDM [17] weights for training humanoid motion diffusion model. We next briefly summarize the diffusion model and describe how it is conditioned and trained for controllable humanoid trajectory generation. **Diffusion Models.** We treat motion trajectories as samples from an unknown distribution _Q_ ( _x_ ) and train a denoising model _Pθ_ to approximate it. Following DDPM [43], we use a Markovian forward process that gradually perturbs a clean trajectory _x_<sup>1:</sup><sup>_N_</sup> with Gaussian noise according to a variance schedule _αt_ , and train _Pθ_ to invert this process. Consistent with prior work in human motion generation [7], [17], the model predicts the clean signal _x_ ˆ<sup>1:</sup> 0<sup>_N_</sup> rather than the noise _ϵt_ , which has previously shown to empirically stabilize training and improve sample quality. 

**Controllable Humanoid Motion Generation.** Given the spatio-temporal signal **c** _∈ R_<sup>_N×J×_3</sup> , and an open-vocabulary text instruction, the model generates trajectories consistent with both modalities. We adopt the realism-guidance module from OmniControl [7], which is similar to ControlNet [44]. The realism guidance block is a trainable copy of the transformer encoder with weights initialized with zeros, so that they have no controlling effect at the beginning. The module takes the text input **p** and spatial constrains **c** and modulates the transformer features. Through training the realism guidance transformer learns spatial constraints and adds corrections to encourage physical plausibility and reduce artifacts such as foot-skating. 

_3) Sampling:_ OmniControl [7] employs spatial guidance (Eq. 3) during sampling to satisfy spatial constraints. At each denoising step, forward kinematics maps the trajectory _µt_ to keypoint space. An MSE loss _G_ ( _µt,_ **c** ) against the target positions **c** then shifts _µt_ toward these desired constraints. 


Given that we parameterize humanoid trajectories using the same representation as human motion, we can directly adopt OmniControl’s spatial guidance procedure together with CFG [45] sampling for humanoid trajectory generation. 

_4) Post-Processing and Filtering:_ The generated trajectories ( **x** _t ∈_ R<sup>_N×_263</sup> ) are converted into executable robot motions via a post-optimization module _Fpost_ , which recovers joint angles _qt ∈_ R<sup>27</sup> and global poses _Tt ∈_ `SE` ( `3` ): _τt_ : _qt, , Tt_ = _Fpost_ ( **x** _t_ ). 

We apply automated filtering and refinement steps to ensure physical plausibility and task feasibility. Our filtering uses simple, error-based heuristics to remove noisy trajectories from the generated set. For example, in the Drawer Open task, we measure the _L_ 2 distance between the drawer-handle position and the robot hand link; if this error exceeds a threshold, we discard the trajectory. Similarly, we apply taskspecific conditions to remove trajectories with unsafe root heights (e.g., the root falling below a threshold), enforce foot stability to prevent slipping or floating artifacts, impose obstacle-avoidance constraints, and enforce wrist-orientation 

constraints when grasping is required. 

## _C. RL for Physics-Based Motion Imitation_ 

The diffusion model produces semantically meaningful but physics-free whole-body trajectories. To execute them on the humanoid, we train a physics-based controller using RL following the DreamControl framework [5]. 

_1) Reference Trajectory Parameterization for RL:_ The RL policy receives a set of reference trajectories _{τ_ ˆ _}_<sup>_κ_</sup> _i_ =0<sup>,</sup> where _κ_ is the number of sampled trajectories. Each reference trajectory is parameterized as _τ_ ˆ = _{τ, s_<sup>left</sup> _t_<sup>_,s_</sup> _t_<sup>right</sup> _}_ , where _τ_ is the post-processed diffusion output and _s_<sup>left</sup> _t_<sup>_, s_</sup> _t_<sup>right</sup> _∈{_ 0 _,_ 1 _}_ denote binary hand open/closed states inferred from the spatiotemporal conditioning signal **c** . 

_2) Action Space:_ A 27-DOF _G_ 1 (pitch and roll are locked at the waist) equipped with two Inspire hands. Action at timestep _t_ includes _qt ∈_ R<sup>27</sup> , which denotes the target joint angles and the two scalars represent binary hand commands. 

_3) Observation Space:_ Following prior work [5], [32], [33], observations consist of real-robot proprioceptive signals, with object poses expressed in the robot’s local root frame to facilitate sim-to-real transfer. 

## _D. Sim2Real Deployment_ 

Real-world experiments are conducted on a Unitree- _G_ 1 robot, with the waist configured to allow only yaw rotation while roll and pitch are locked. Inspire hands are controlled through binary open/close commands. The robot also uses its on-board IMU to provide root angular velocities and the gravity vector for state estimation. The DreamControl-v2 skill library consists of 8 skills shown in Table III, and the deployment results are provided in the _accompanying video_ , and is shown in Fig. 1. 

## IV. EXPERIMENTS & ANALYSIS 

To analyze the impact of the DreamControl-v2’s preretargetting recipe, we pose three key questions: ( **Q1** ) Does a trained diffusion model operating in robot-space provide high-quality reference trajectories? (Sec IV-B) ( **Q2** ) Does scaling the diffusion training data and the number of samples drawn during RL yield any benefits (Sec IV-C)? ( **Q3** ) How do the design choices of DreamControl-v2 impact the system-level simplicity and overall performance (Sec. IV-D)? 

## _A. Evaluation Setup_ 

We evaluate DreamControl-v2 across multiple data configurations, and tasks to analyze its fidelity, generalization, and impact on downstream control. Here, we summarize the training data mixtures, evaluation metrics, and key implementation details used in our experiments. 

**Training Data Mixtures.** We train three diffusion model variants with progressively richer motion datasets: 

- AMASS: Locomotion and simple pick/place motions, identical to the corpus used by OmniControl [7]. 

- AMASS + Nymeria (subset): Adds the subset of Nymeria containing articulated-object interactions (e.g., drawers, cabinets), following the filtering procedure in Sec. III-A.4. 

- Full-Mix: Augments the above with GRAB [34] and robot trajectories from OmniRetarget [33]. 

**Baseline.** We evaluate DreamControl-v2 against the zeroshot OmniControl [7] model (this model operates in human space and is trained on AMASS [8], [9] and the default model used by DreamControl [5]). The tasks used for RL evaluations are divided into two groups. _Group-1_ consists of Drawer Open and Deep Squat & Pick, and _Group2_ consists of Pick and Punch. Tasks in _Group-1_ are not within the original distribution of AMASS [8], [9] for which DreamControl [5] leveraged task-specific IK and manual filtering. Tasks in _Group-2_ are those that are available within the AMASS [8], [9]. Trial-and-error-based prompting to obtain suitable reference trajectories and the generated trajectories from zero-shot OmniControl [7] are passed through our automated filtering procedure and used to train the a downstream RL baseline. This baseline is the fully automated variant of DreamControl [5] (by replacing the manual filtering used in the original paper). 

**Task Library.** After training the diffusion prior, we train a skill library consisting of 8 tasks, including articulatedobject interaction, single-hand pick-and-place, and bimanual manipulation skills. Each RL evaluation is conducted over 100 randomized simulation environments per task. Unless stated otherwise, all RL policy results across tasks are derived from the Full-Mix model. 

**Evaluation Metrics.** We evaluate the diffusion model using standard metrics from the human-motion generation literature [7], [9], [20], [46]. 

- FID ( _↓_ ) [47] measures the distributional similarity between generated trajectories and real motion data. We compute FID on trajectories generated directly for the _G_ 1 humanoid, using a ground-truth evaluation set obtained by retargeting human motion data to the _G_ 1 form factor. Because our trajectory parameterization follows [9], we directly apply the HumanML3D feature extractor [9] to compute FID. 

- R-Precision ( _↑_ ) evaluates how well a generated trajectory matches its input text instruction. For each generated sample _y_ ˆ, we retrieve the correct text description from a set of 32 candidates (1 ground-truth and 31 distractors) by ranking feature distances. Higher top- _k_ retrieval accuracy indicates better text–motion alignment. 

- Diversity ( _→_ ) measures the average distance between features of _N_ = 32 randomly sampled generated trajectories, ( _→_ ) indicates the value closer to groundtruth is better. 

- Control L2 ( _↓_ ) measures spatial accuracy between generated trajectories and input control signal. 

- Skating Ratio ( _↓_ ) is a proxy for physical plausibility, measuring undesired foot sliding. 

For the downstream RL policy, we report two metrics: 

- Success Ratio ( _↑_ ) is the fraction of rollouts in which the humanoid successfully completes the task. 

- Control Error ( _↓_ ) Is the _L_ 2 distance between the expected point of interaction and the actual point of interaction when rolling out the policy. 

- **Implementation Details.** The large-scale human-to-robot 

TABLE I: **Comparison Across Training Data Mixtures.** We evaluate diffusion models trained on three data configurations: AMASS, AMASS + Nymeria, and Full-Mix. For downstream control, we additionally report the average RL policy success ratio (in simulation). Refer to Sec. IV-A for details related to baselines, and note that zero-shot refers to fully automated DreamControl [7] for RL evaluation, and diffusion is evaluated using OmniControl [7]. All results are evaluated on the _Full-Mix_ test set. 

|Train Data|# Samples (K)|FID_↓_|R<br>Top-1|-Precision<br>Top-2|_↑_<br>Top-3|Diversity_→_<br>(3.362)|Control L2_↓_|Skating Ratio_↓_|Downstrea<br>_Group-1_|m RL Policy_↑_<br>_Group-2_|
|---|---|---|---|---|---|---|---|---|---|---|
|Zero-Shot|-|0.981|0.105|0.260|0.329|3.647|0.112|0.101|0.040|**0.995**|
|AMASS|21.8|0.305|0.110|0.184|0.266|3.174|0.104|0.142|0.030|0.985|
|AMASS + Nymeria|26.4|0.298|0.101|0.204|0.281|3.084|0.108|0.132|0.860|0.985|
|**Full-Mix**|**29.6**|**0.265**|**0.114**|**0.217**|**0.388**|**3.252**|**0.066**|**0.096**|**0.925**|0.985|


TABLE II: **Comparison Across Test Splits.** We report FID, R-Precision (Top-3), Control L2, and Skating Ratio on two distinct evaluation sets: (1) the _AMASS Test Set_ , and (2) a _Non-AMASS Test Set_ constructed from Nymeria (subset), GRAB, and OmniRetarget samples within the Full-Mix distribution. 

|Train Data|FID_↓_|R-Precision_↑_<br>Control L2_↓_|Skating Ratio_↓_|
|---|---|---|---|
|||_AMASS Test Set_||
|AMASS|0.328|0.291<br>0.070|0.100|
|Full-Mix|0.320|0.280<br>0.050|0.120|
|||_Non-AMASS Test Set_||
|AMASS|2.720|0.117<br>0.065|0.539|
|Full-Mix|0.316|0.264<br>0.042|0.032|


dataset by retargeting human motion sequences across 5 NVIDIA H100 GPUs in parallel, cropping or padding each trajectory to 10 seconds. The diffusion model is trained on a single NVIDIA H100 GPU using the AdamW optimizer [48] with a learning rate of 1 _×_ 10<sup>_−_5</sup> . The RL controller is trained in IsaacLab [49], which runs on IsaacSim. We use PPO [50] on a single NVIDIA A6000 GPU for 2 _,_ 000–5 _,_ 000 iterations depending on the task, on approximately 8 _,_ 912 parallel simulation environments. 

## _B. Scaling Data Improves Diffusion Models_ 

To understand how expanding the training corpus affects the fidelity and breadth of skills learned by DreamControlv2, we evaluate three data-mixture variants from Sec. IVA: AMASS, AMASS + Nymeria, and Full-Mix. Table I shows that enlarging the training distribution consistently improves trajectory quality. Specifically, FID decreases across all mixtures, indicating clear gains in generated motion fidelity. Compared to the zero-shot OmniControl baseline, all trained variants demonstrate substantial improvements. This highlights the value of our pipeline, which transfers large-scale human motion data into robot space and trains a dedicated humanoid motion diffusion model, rather than relying on human-domain generation. Among all variants, the Full-Mix model delivers the strongest and most stable performance across metrics, demonstrating that broader human–robot motion coverage yields higher-fidelity trajectories. 

To assess whether expanding the training corpus preserves previously learned behaviors while enabling new ones, we evaluate the AMASS and Full-Mix models on two test splits (Table II). The first test split, the _AMASS test set_ , contains only AMASS [9] test sequences. The second split, the _Non-AMASS test set_ , includes test data from Nymeria [35], 


Fig. 3: **Effect of Trajectory Scaling on RL Performance.** More diffusiongenerated trajectories consistently lead to higher policy success ratios across 3 different tasks. The figure on the right indicates the variance of test distribution on multiple tasks. 

GRAB [34], and OmniRetarget [33]. On the AMASS test set, the Full-Mix model performs on par with the AMASSonly variant, indicating that incorporating additional datasets does not compromise performance on the original domain. This suggests that our normalization pipeline (Sec. IIIA.4) effectively aligns heterogeneous datasets, allowing new datasets to integrate smoothly without disrupting existing capabilities. Moreover, on the non-AMASS test set, the FullMix model improves over the AMASS-only variant. 

## _C. Improved Diffusion Models Yield Stronger RL Policies_ 

_1)_ **_Skill Acquisition from Diffusion_** _:_ To study skill acquisition We benchmark two representative task groups ( _Group-1/2_ refer to baselines in Sec. IV) and report the RL success ratio for each. _Group-1_ includes relatively more complex actions, requiring whole body coordination such as squatting, grasping, and lifting (Deep Squat & lift) or interaction with an articulated object (Drawer Open). Because these tasks do not appear in AMASS, the AMASSonly model and the zero-shot model (fully automated original DreamControl [5]) is limited by its training distribution, thereby leading to low results, while incorporating interactionrich Data from multiple sources allows the policy to succeed. Policies trained using trajectories from increasingly diverse diffusion models exhibit steadily higher success ratios (see Table I). Overall, DreamControl-v2 matches the performance of DreamControl [5] on simpler _Group-2_ tasks, while handling the complex, interaction-heavy _Group-1_ tasks far more effectively—all through a fully automated pipeline. 

_2)_ **_Scaling Diffusion Trajectories Yield Stronger RL Policies_** _:_ We study how scaling the number of diffusion- 

TABLE III: **Task-wise Performance** . We report the Success Ratio and Control Error (m) averaged over 100 randomized simulation environments for all 8 tasks in our skill library. 

|Task|Success Ratio _↑_|Control Error _↓_|
|---|---|---|
|Pick|0.99|0.03|
|Punch|0.99|0.04|
|Deep Squat & Pick|0.94|0.06|
|Drawer Open|0.96|0.02|
|Pour|0.92|0.03|
|Vertical Wipe|1.00|0.04|
|Deep Squat|0.99|0.08|
|Step & Punch|0.91|0.06|


generated trajectories affects generalization in downstream RL. Using the Full-Mix model, we generate varying numbers of trajectories and train RL policies for tasks with objects placed at diverse spatial locations. As shown in Fig. 3, scaling of sampled trajectories consistently improves policy success, eventually approaching optimal saturation. The model has been evaluated with target locations sampled with an average variance of _x ∼_ 0 _._ 15 _m, y ∼_ 0 _._ 2 _m_ and _z ∼_ 0 _._ 08 _m_ . 

## _D. Performance Analysis_ 

_1) Overall Performance in Simulation:_ Table III reports task-wise performance across the 8 skills in our library. Success criteria are defined per task; for example, in Drawer Open, the drawer must move at least 5 cm. Across all skills, DreamControl-v2 achieves consistently high success rates with low control error, demonstrating robust and reliable execution of diverse loco-manipulation tasks. 

_2) Inference-Time Prompt Calibration vs. Pre-retargeting:_ We consider an inference-time prompt calibration baseline that keeps the human-motion diffusion model fixed and instead tunes spatial prompting parameters in human space. We sample a human trajectory _x_ ( _t_ ) from OmniControl [7], generate _N_ candidates by perturbing the prompt scale _{x_<sup>1</sup> ( _t_ ) _, . . . , x_<sup>_N_</sup> ( _t_ ) _}_ , retarget each candidate to robot space, and select the one that best matches the target spatial constraints. Table IV reveals two key limitations. First, because spatial prompts constrain multiple joints together, uniform scaling often produces off-balance motions or misses the intended constraints, resulting in higher FID and larger control errors (Ctrl L2). Second, this search is sampleinefficient: most candidates are rejected by the automated filter as indicated by Valid Traj.(%). On the AMASS test set, the Pick is used for evaluation and Drawer Open is used for the Full-Mix evaluation; sample efficiency is reported over 100 samples. This indicates that the search space is high and requires careful parameter selection and pre-retargetting is a simpler design choice. The qualitative results are given in Fig. 4, and we notice that in both tasks, the prompt calibration method leads to inaccurate samples with unstable poses, which are not near the object. Together with Table I, these results show that pre-retargeting eliminates trial-and-error prompting and improves fidelity and RL performance. 

_3) Network Initialization:_ Our trajectory parameterization for the humanoid robot (given in Sec. III-B.1) allows us to use the strong priors from human motion diffusion model 


Fig. 4: **Spatial Prompting Qualitative Results.** The figure depicts successful ( ) and rejected samples ( ) obtained from various spatial prompting techniques. The DreamControl-v2 model is directly prompted in robot space (blue line), trial-and-error is used for the zero-shot model (red line), and prompt calibration is indicated with green lines. 

TABLE IV: **Prompt calibration vs. pre-retargeting.** Prompt-Calib. uses samples from the zero-shot OmniControl model [7]. FID and Ctrl L2 are evaluated on the respective AMASS and Full-Mix test sets. Valid Traj. (%) is reported for the Pick task corresponding to AMASS and the Drawer Open task for Full-Mix. Our Pre-retargeting method is evaluated on Full-Mix and Valid Traj.(%) represents the average across both tasks. 

|Method|FID_↓_|Ctrl L2_↓_|Valid Traj.(%)|
|---|---|---|---|
|Prompt-Calib. (_AMASS_)|2.010|0.180|8.0|
|Prompt-Calib. (_Full-Mix_)|3.260|0.260|4.0|
|Pre-retargetting (_Full-Mix_)|**0.265**|**0.066**|**68.0**|


TABLE V: **Network Initialization** . We report FID, R-Precision (Top-3), Control L2 and Skating Ratio for models randomly initialized (✗) and with the pretrained weights from MDM [17] (✓). 

|Pretrained|Iters _×_10<sup>3</sup>|FID_↓_|R@3_↑_|Ctrl L2_↓_|Skt Ratio_↓_|
|---|---|---|---|---|---|
|✗|104|0.741|0.254|0.114|0.112|
|✓|102|**0.265**|**0.388**|**0.066**|**0.096**|


(MDM [17]) for humanoid motion generation. Table. V reports an ablation comparing models trained from scratch versus those fine-tuned from the MDM checkpoint. Finetuning yields clear gains in fidelity and physical plausibility, suggesting that human-motion priors provide a strong initialization that adapts effectively to the robot embodiment. 

REFERENCES 

- [1] Y. Ze, S. Zhao, W. Wang, A. Kanazawa, R. Duan, P. Abbeel, G. Shi, J. Wu, and C. K. Liu, “Twist2: Scalable, portable, and holistic humanoid data collection system,” _arXiv preprint arXiv:2511.02832_ , 2025. 

- [2] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi, “Omnih2o: Universal and dexterous human-tohumanoid whole-body teleoperation and learning,” _arXiv preprint arXiv:2406.08858_ , 2024. 

- [3] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Castañeda, Z.-A. Cao, J. Li, D. Minor, Q. Ben, X. Da, R. Ding, C. Hogg, L. Song, E. Lim, E. Jeong, T. He, H. Xue, W. Xiao, Z. Wang, S. Yuen, J. Kautz, Y. Chang, U. Iqbal, L. Fan, and Y. Zhu, “Sonic: Supersizing motion tracking for natural humanoid whole-body control,” _arXiv preprint arXiv:2511.07820_ , 2025. 

- [4] G. Tevet, S. Raab, S. Cohan, D. Reda, Z. Luo, X. B. Peng, A. H. Bermano, and M. van de Panne, “Closd: Closing the loop between simulation and diffusion for multi-task character control,” _arXiv preprint arXiv:2410.03441_ , 2024. 

- [5] D. Kalaria, S. S. Harithas, P. Katara, S. Kwak, S. Bhagat, S. Sastry, S. Sridhar, S. Vemprala, A. Kapoor, and J. C.-K. Huang, “Dreamcontrol: Human-inspired whole-body humanoid control for scene interaction via guided diffusion,” _arXiv preprint arXiv:2509.14353_ , 2025. 

- [6] Z. Luo, J. Cao, S. Christen, A. Winkler, K. Kitani, and W. Xu, “Omnigrasp: Grasping diverse objects with simulated humanoids,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 2161– 2184, 2024. 

- [7] Y. Xie, V. Jampani, L. Zhong, D. Sun, and H. Jiang, “Omnicontrol: Control any joint at any time for human motion generation,” in _The Twelfth International Conference on Learning Representations_ , 2024. [Online]. Available: https://openreview.net/forum?id=gd0lAEtWso 

- [8] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black, “AMASS: Archive of motion capture as surface shapes,” in _International Conference on Computer Vision_ , Oct. 2019, pp. 5442–5451. 

- [9] C. Guo, S. Zou, X. Zuo, S. Wang, W. Ji, X. Li, and L. Cheng, “Generating diverse and natural 3d human motions from text,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , June 2022, pp. 5152–5161. 

- [10] J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat _et al._ , “Gpt-4 technical report,” _arXiv preprint arXiv:2303.08774_ , 2023. 

- [11] T. B. Brown, “Language models are few-shot learners,” _arXiv preprint arXiv:2005.14165_ , 2020. 

- [12] R. Rombach, A. Blattmann, D. Lorenz, P. Esser, and B. Ommer, “High-resolution image synthesis with latent diffusion models,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2022, pp. 10 684–10 695. 

- [13] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A vision-language-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [14] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai _et al._ , “ _π_ 0 _._ 5: a vision-language-action model with open-world generalization,” _arXiv preprint arXiv:2504.16054_ , 2025. 

- [15] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi _et al._ , “Openvla: An opensource vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

- [16] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” _The International Journal of Robotics Research_ , vol. 44, no. 10-11, pp. 1684–1704, 2025. 

- [17] G. Tevet, S. Raab, B. Gordon, Y. Shafir, D. Cohen-Or, and A. H. Bermano, “Human motion diffusion model,” _arXiv preprint arXiv:2209.14916_ , 2022. 

- [18] J. Zhang, Y. Zhang, X. Cun, S. Huang, Y. Zhang, H. Zhao, H. Lu, and X. Shen, “T2m-gpt: Generating human motion from textual descriptions with discrete representations,” _arXiv preprint arXiv:2301.06052_ , 2023. 

- [19] B. Jiang, X. Chen, W. Liu, J. Yu, G. Yu, and T. Chen, “Motiongpt: Human motion as a foreign language,” _Advances in Neural Information Processing Systems_ , vol. 36, 2024. 

- [20] S. Harithas and S. Sridhar, “Motionglot: A multi-embodied motion generation model,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 16 109–16 116. 

- [21] E. Pinyoanuntapong, M. Saleem, K. Karunratanakul, P. Wang, H. Xue, C. Chen, C. Guo, J. Cao, J. Ren, and S. Tulyakov, “Maskcontrol: Spatio-temporal control for masked motion synthesis,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2025, pp. 9955–9965. 

- [22] J. Mao, S. Zhao, S. Song, T. Shi, J. Ye, M. Zhang, H. Geng, J. Malik, V. Guizilini, and Y. Wang, “Learning from massive human videos for universal humanoid pose control,” _arXiv preprint arXiv:2412.14172_ , 2024. 

- [23] M. Al Borno, M. De Lasa, and A. Hertzmann, “Trajectory optimization for full-body movements with complex contacts,” _IEEE transactions on visualization and computer graphics_ , vol. 19, no. 8, pp. 1405–1414, 2012. 

- [24] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “Ex- 

pressive whole-body control for humanoid robots,” _arXiv preprint arXiv:2402.16796_ , 2024. 

- [25] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang, “Exbody2: Advanced expressive humanoid whole-body control,” _arXiv preprint arXiv:2412.13196_ , 2024. 

- [26] T. He, Z. Luo, W. Xiao, C. Zhang, K. Kitani, C. Liu, and G. Shi, “Learning human-to-humanoid real-time whole-body teleoperation,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 8944–8951. 

- [27] Y. Ze, Z. Chen, J. P. AraÃšjo, Z.-a. Cao, X. B. Peng, J. Wu, and C. K. Liu, “Twist: Teleoperated whole-body imitation system,” _arXiv preprint arXiv:2505.02833_ , 2025. 

- [28] L. Pan, J. Wang, B. Huang, J. Zhang, H. Wang, X. Tang, and Y. Wang, “Synthesizing physically plausible human motions in 3d scenes,” in _2024 International Conference on 3D Vision (3DV)_ . IEEE, 2024, pp. 1498–1507. 

- [29] M. Seo, S. Han, K. Sim, S. H. Bang, C. Gonzalez, L. Sentis, and Y. Zhu, “Deep imitation learning for humanoid loco-manipulation through human teleoperation,” in _2023 IEEE-RAS 22nd International Conference on Humanoid Robots (Humanoids)_ . IEEE, 2023, pp. 1–8. 

- [30] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “Humanplus: Humanoid shadowing and imitation from humans,” _arXiv preprint arXiv:2406.10454_ , 2024. 

- [31] A. Allshire, H. Choi, J. Zhang, D. McAllister, A. Zhang, C. M. Kim, T. Darrell, P. Abbeel, J. Malik, and A. Kanazawa, “Visual imitation enables contextual humanoid control,” in _Proceedings of the Conference on Robot Learning (CoRL)_ , 2025. 

- [32] H. Weng, Y. Li, N. Sobanbabu, Z. Wang, Z. Luo, T. He, D. Ramanan, and G. Shi, “Hdmi: Learning interactive humanoid whole-body control from human videos,” _arXiv preprint arXiv:2509.16757_ , 2025. 

- [33] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi, “Omniretarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction,” _arXiv preprint arXiv:2509.26633_ , 2025. 

- [34] O. Taheri, N. Ghorbani, M. J. Black, and D. Tzionas, “Grab: A dataset of whole-body human grasping of objects,” in _European conference on computer vision_ . Springer, 2020, pp. 581–600. 

- [35] L. Ma, Y. Ye, F. Hong, V. Guzov, Y. Jiang, R. Postyeni, L. Pesqueira, A. Gamino, V. Baiyya, H. J. Kim _et al._ , “Nymeria: A massive collection of multimodal egocentric daily motion in the wild,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 445–465. 

- [36] J. Li, J. Wu, and C. K. Liu, “Object motion guided human motion synthesis,” _ACM Trans. Graph._ , vol. 42, no. 6, 2023. 

- [37] C. M. Kim*, B. Yi*, H. Choi, Y. Ma, K. Goldberg, and A. Kanazawa, “Pyroki: A modular toolkit for robot kinematic optimization,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2025. [Online]. Available: https://arxiv.org/abs/2505.03728 

- [38] J. Bradbury, R. Frostig, P. Hawkins, M. J. Johnson, C. Leary, D. Maclaurin, G. Necula, A. Paszke, J. VanderPlas, S. WandermanMilne, and Q. Zhang, “JAX: composable transformations of Python+NumPy programs,” 2018. [Online]. Available: http://github. com/jax-ml/jax 

- [39] M. Loper, N. Mahmood, J. Romero, G. Pons-Moll, and M. J. Black, “Smpl: A skinned multi-person linear model,” in _Seminal Graphics Papers: Pushing the Boundaries, Volume 2_ , 2023, pp. 851–866. 

- [40] Movella Technologies B.V., “Movella Xsens mvn link motion capture system,” https://www.movella.com/products/motion-capture/ xsens-mvn-link, 2025, accessed: 2025-11-04. 

- [41] Z. Luo, J. Cao, A. W. Winkler, K. Kitani, and W. Xu, “Perpetual humanoid control for real-time simulated avatars,” in _International Conference on Computer Vision (ICCV)_ , 2023. 

- [42] Z. Luo, R. Hachiuma, Y. Yuan, and K. Kitani, “Dynamics-regulated kinematic policy for egocentric pose estimation,” _Advances in Neural Information Processing Systems_ , vol. 34, pp. 25 019–25 032, 2021. 

- [43] R. Rombach, A. Blattmann, D. Lorenz, P. Esser, and B. Ommer, “High-resolution image synthesis with latent diffusion models,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2022, pp. 10 684–10 695. 

- [44] L. Zhang, A. Rao, and M. Agrawala, “Adding conditional control to text-to-image diffusion models,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2023, pp. 3836–3847. 

- [45] J. Ho and T. Salimans, “Classifier-free diffusion guidance,” _arXiv preprint arXiv:2207.12598_ , 2022. 

- [46] E. Pinyoanuntapong, M. U. Saleem, K. Karunratanakul, P. Wang, H. Xue, C. Chen, C. Guo, J. Cao, J. Ren, and S. Tulyakov, “Con- 

trolmm: Controllable masked motion generation,” _arXiv preprint arXiv:2410.10780_ , 2024. 

- [47] H. Martin, R. Hubert, U. Thomas, N. Bernhard, and H. Sepp, “Gans trained by a two time-scale update rule converge to a local nash equilibrium,” _Advances in neural information processing systems_ , vol. 30, pp. 6626–6637, 2017. 

- [48] P. K. Diederik, “Adam: A method for stochastic optimization,” _(No Title)_ , 2014. 

- [49] M. M. et.al, “Isaac lab: A gpu-accelerated simulation framework for multi-modal robot learning,” _arXiv preprint arXiv:2511.04831_ , 2025. [Online]. Available: https://arxiv.org/abs/2511.04831 

- [50] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

## V. APPENDIX 

## _A. Key-point Correspondence Between Human & G1_ 

In DreamControl-v2 correspondances are needed to first retarget human data to the G1 embodiment. Table VI show the keypoint correspondences used for retargetting, Table VII shows the correspondences used for the trajectory representation given in Sec. III-B.1. 

TABLE VI: Human and G1 link correspondances for retargetting 

|**SMPL**|**G1 link name**|
|---|---|
|pelvis<br>left hip|pelvis_contour_link<br>left_hip_pitch_link|
|right hip|right_hip_pitch_link|
|left knee|left_knee_link|
|right knee|right_knee_link|
|left ankle|left_ankle_roll_link|
|right ankle|right_ankle_roll_link|
|left shoulder|left_sholuder_roll_link|
|right sholuder|right_shoulder_roll_link|
|left elbow<br>right elbow|left_elbow_link<br>right_elbow_link|
|left wrist|left_wrist_yaw_link|
|right wrist|right_wrist_yaw_link|


## TABLE VII: SMPL and G1 link keypoint correspondances for Trajectory represenatation 

|**Human**|**G1 link name**|
|---|---|
|pelvis|pelvis contour link|
|left hip|left hip pitch link|
|right hip<br>|right hip pitch link<br>|
|spine 1|imu link|
|left knee|left knee link|
|right knee<br>|right knee link<br>|
|spine 2|torso link|
|left ankle|left ankle pitch link|
|right ankle|right ankle pitch link|
|spine 3|imu link|
|left foot|left ankle roll link|
|right foot|right ankle roll link|
|neck|mid360 link|
|left collar|left shoulder yaw link|
|right collar|right shoulder yaw link|
|head|d435 link|
|left shoulder|left shoulder pitch link|
|right shoulder|right shoulder pitch link|
|left elbow|left elbow link|
|right elbow|right elbow link|
|left wrist|left wrist yaw link|
|right wrist|right wrist yaw link|


## _B. Diffusion Model Qualitative Results_ 

The qualitative results of the reference trajectory generation using the diffusion model are shown in Fig. 4. The results demonstrate that the model can generate trajectories while satisfying a wide range of spatiotemporal constraints. For example, in the walk scenario, the generated trajectory adheres to a continuous constraint on the head joint. Likewise, the model can be conditioned on discrete joint positions at specific timesteps to produce actions such as kick or run in place. Furthermore, the model supports conditioning on multiple joints simultaneously—such as both wrists—to generate coordinated behaviors like a bimanual pick action. 


Fig. 4: Key-point correspondences used for retargetting human data to G1. A similar correspondence mapping is used for diffusion trajectory representation Sec. III-B.1. 

## _C. Diffusion Model Prompting_ 

_1) Text Prompts:_ The task-specific text prompts used are given in Table VIII. 

_2) SpatioTemporal Prompts:_ In this section we detail the spatiotemporal prompts used to sample reference trajectories from the trained diffusion model. Note that the DreamControlv2 diffusion model can be directly prompted in the robot space, simplifying the prompting process previously used in [5]. 

- Pick: The right wrist is used to perform the pick task, where a cube object is placed on a table. The spatial control for the right wrist is given as ( **pright** _ **wrist** ) is sampled uniformly in the distribution _x ∼U_ ( _−_ 0 _._ 22 _,_ 0 _._ 12) _, y ∼U_ (0 _._ 2 _,_ 0 _._ 4) _, z ∼_ 0 _._ 94. The time of contact is chosen as _t ∼U_ (40 _,_ 50). Similar to [5], to encourage side-grasp of the cup, we further condition the elbow joints using the equation _pelbow_ = [ _x − αll_ cos( _θ_ ) _, y, z − l_ sin( _θ_ )]. Where _l_ is the link length from elbow to wrist and _θ_ = _π/_ 4. To encourage a stationary position during the pick task, we further constrain both the knee positions. 

- Open Drawer: The right wrist is used to perform the drawer open task. To encourage drawer opening samples with a stationary stance, we further add constraints _∼ ∼_ 

- on the knees. **pright** _ **wrist** _x U_ (0 _._ 3 _,_ 0 _._ 50) _, y U_ ( _−_ 0 _._ 20 _, −_ 0 _._ 30) _, z ∼U_ (0 _._ 75 _,_ 0 _._ 82). **p** _right_  kneey ∼ ∼ ∼_ 

- _N_ ( _−_ 0 _._ 13 _,_ 0 _._ 01) _, z N_ (0 _._ 35 _,_ 0 _._ 01) _, x N_ ( _−_ 0 _._ 02 _,_ 0 _._ 01). A target timestep **tg** _∼U_ (35 _,_ 40) is selected. The spatiotemporal prompt ( **_τ_** right_wrist) of total time _T_ is given as 


- The parameter **p** _offset_ is set to indicate the distance to open the drawer is set to 0 _._ 2 _m_ . 

- Pour:The prompt procedure for the pour task is similar to that of the pick task. The spatial control of the right wrist, denoted by **p** right_wrist, is sampled from a uniform distribution with _x ∼U_ ( _−_ 0 _._ 10 _,_ 0 _._ 10), _y ∼U_ (0 _._ 2 _,_ 0 _._ 4), and _z_ = 0 _._ 94. The contact time is sampled as _t ∼ U_ (40 _,_ 42). 


## Fig. 4: **Trajectory Generation Qualitative Results** 

## TABLE VIII: Task-specific Text Prompts 


- Vertical Wipe: the right wrist is prompted using **_τ_** right_wrist, setting the spatial constrain to 0 would disable spatial constrains until the target time _tg_ . A linear trajectory is used to 


- Deep Squat: For the deep squat, we condition the pelvis position to be **p** _pelvis_ sampled from _x ∼U_ ( _−_ 0 _._ 15 _, −_ 0 _._ 05), _y ∼U_ ( _−_ 0 _._ 04 _,_ 0 _._ 04) , _z ∼ U_ (0 _._ 35 _,_ 0 _._ 45). 

- Punch: The right wrist is conditioned for the punch task. The target ( **pright** _ **wrist** ) are sampled as _y ∼ U_ ( _−_ 0 _._ 2 _,_ 0 _._ 1) , _z ∼U_ (0 _._ 95 _,_ 1 _._ 1) , _x ∼U_ (0 _._ 45 _,_ 0 _._ 55). The time step _tg ∼U_ (90 _,_ 120). 

- Step & Punch: The right wrist is conditioned for the punch task. The target ( **pright** _ **wrist** ) are sampled as _y ∼ U_ ( _−_ 0 _._ 2 _,_ 0 _._ 1) , _z ∼U_ (0 _._ 95 _,_ 1 _._ 1) , _x ∼U_ (0 _._ 95 _,_ 1 _._ 05). The time step _tg ∼U_ (110 _,_ 140). 

## _D. Filtering Process & Optimization_ 

Here, we provide details on the task-specific filtering steps used and the post optimization steps before tracking the trajectory with RL. 

- Pick: To pick the object the trajectories are expected to avoid the table on which they are placed, similar to DreamControl [5] we follow an SDF based obstacle avoidance process. In addition to the obstacle avoidance we have an additional cost to ensure smoothness while grasping the object and the hand remains close to the 

control point _pwrist_ . 


The costs include a smoothing term to ensure continuity, the function _d_ ( _._ ) is the SDF function that returns 0 if the distance is greater than _λ_ , and _ψ_ refers to the cost function that minimizes the distance between the actual and the desired end-effector pose for grasping. Lastly we apply a generic filtering step, where if the position of the wrist is expected to avoid the obstacle by at-least _β_ = 0 _._ 03 and the the error between the wrist position and the target must be less than 0 _._ 15 _m_ to be selected for RL training. 

- Open Drawer: The drawer opening cost consists of the trajectory reaching cost given by. 


Additionally, a trajectory is chosen if the position of the wrist is within the threshold _β <_ 0 _._ 15 _m_ at the point of contact. 

- Deep Squat & Pick: Stability is enforced by introducing cost terms that minimize foot slippage, including penalties on foot velocity and on changes in inter-foot distance. To further improve the grip on the object we add the following cost. 

_q_<sup>_ref_</sup> = _argmin||deef − λeef ||_ 2 

TABLE IX: Task-specific Rewards 

|**Task**|**Reward (r1)**<br>|**Description**<br>|
|---|---|---|
|Pick|_h_<sup>_obj_</sup><br>_t_<br>_> h_<sup>_thresh_ </sup>, _t ≥tg_<br>|_h_<sup>_thresh_ </sup>= 0_._95 ,_h_<sup>_obj_</sup><br>_t_<br>is object height|
|Deep Squat & Pick|_h_<sup>_obj_</sup><br>_t_<br>_> h_<sup>_thresh_</sup>, _t ≥tg_<br>|_h_<sup>_thresh_ </sup>= 0_._65<br>|
|Drawer Open<br>Pour|_a_<sup>_obj_</sup><br>_t_<br>_> h_<sup>_thresh_</sup>, _t ≥tg_<br>_h_<sup>_obj_</sup><br>_t_<br>_> h_<sup>_thresh_</sup>, _t ≥tg_<br>|_a_<sup>_obj_</sup><br>_t_<br>_≥_0_._05, distance traversed by drawer<br>_h_<sup>_thresh_ </sup>= 0_._65|
|Vertical Wipe|_||ptarget −pt||_<sup>2</sup><br>2 <sup>_≤λ_</sup><br>|_pt_ position of wrist at timestep _t_ and _λ_= 0_._05|
|Punch|_||ptarget −pt||_<sup>2</sup><br>2 <sup>_≤λ_</sup><br>|_pt_ position of wrist at timestep _t_ and _λ_= 0_._05|
|Step & Punch|_||ptarget −pt||_<sup>2</sup><br>2 <sup>_≤λ_</sup>|_pt_ position of wrist at timestep _t_ and _λ_= 0_._05|


. This cost minimizes the distance ( _deef_ ) between the right and left hand end-effectors to match the width of the box _λeef_ . A filtering step prior to optimization is performed, we eliminate all trajectories that have yaw rotation _|ψroot| > π/_ 6 this would lead to a distribution of trajectories facing forward. 

- Pour: The obstacle avoidance and filtering process of pour is similar to that of pick. Additionally we perform the following optimization on the wrist to pour rotate the wrist. 


- Vertical Wipe: A cost is added to to track the control trajectory _τwrist_ . 

- Deep Squat: Similar to Bimanual Pick, we add costs to minimize feet slippage and for better stability. 

## _E. RL Policy Details_ 

The task specific rewards used in individual tasks is given in Table. IX, additionally the policy uses motion tracking rewards. The Deep Squat and Bimanual Pick have rewards to minimize root planar linear and angular velocity. The actor and critic networks are initialized by MLPs. 

