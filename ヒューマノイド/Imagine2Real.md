---
title: "Imagine2Real: Towards Zero-shot Humanoid-Object Interaction via Video Generative Priors"
date: "2026-05-21"
authors: "Jiahe Chen; ZiRui Wang; Feiyu Jia; Xiao Chen; Xiaojie Niu; Weishuai Zeng"
url: https://arxiv.org/abs/2605.22272
pdf: https://arxiv.org/pdf/2605.22272
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.22272)** / [論文ページ](https://arxiv.org/abs/2605.22272)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Imagine2Real: Towards Zero-shot Humanoid-Object Interaction via Video Generative Priors** 

Jiahe Chen<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> Zirui Wang<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> Feiyu Jia<sup>2</sup> Xiao Chen<sup>3</sup><sup>_,_2</sup> Xiaojie Niu<sup>2</sup> Weishuai Zeng<sup>3</sup><sup>_,_2</sup> Tianfan Xue<sup>3</sup> Xiaowei Zhou<sup>1</sup> Jiangmiao Pang<sup>2</sup><sup>_†_</sup> Jingbo Wang<sup>2</sup><sup>_†_</sup> 

1 Zhejiang University 2 Shanghai AI Laboratory 3 The Chinese University of Hong Kong 

- _∗: co-first authors †: co-corresponding authors_ 


Figure 1: The Imagine2Real zero-shot deployment loop. Given (1) an image and text instruction, we (2) synthesize an interaction video, (3) extract 4D keypoints trajectories, and (4) deploy the policy within a mocap system, turning imagined interactions into physical reality. 

## **Abstract** 

Whole-body Humanoid-Object Interaction (HOI) is bottlenecked by the scarcity of high-fidelity 3D data. While video generative priors offer a promising alternative, existing methods suffer from _Representation Misalignment_ due to their reliance on geometric priors (e.g., explicit CAD models), and _Retargeting Complexity_ arising from intensive morphing and morphological mismatch. We propose Imagine2Real, a zero-shot HOI framework for flexible, geometry-free interaction. To resolve misalignment, we formulate robot and object motions as unified 4D point trajectories. To overcome retargeting complexity, our Keypoints Tracker tracks only sparse critical points (base, hands, and object), entirely bypassing the error-amplifying retargeting process. To maintain natural gaits despite these sparse signals, we utilize the latent space of a Behavior Foundation Model (BFM) as the tracker’s search domain. Using a progressive training strategy, Imagine2Real learns robust behaviors with simple tracking rewards, enabling zero-shot physical deployment within a motion capture(mocap) system. 

## **1 Introduction** 

Whole-body Humanoid-Object Interaction (HOI) is critical for deploying humanoid robots in unstructured environments such as households and factories. While proprioceptive control has matured significantly [1, 2, 3], extending these capabilities to complex interactions remains difficult. The 

1 

primary bottleneck is the lack of high-fidelity 3D interaction data for humanoid robots, which prevents the learning of robust and versatile interaction policies. 

This data scarcity imposes a generalization ceiling on current HOI methodologies, where task versatility remains strictly limited by the available training samples. Scaling-based models such as VLA [4, 5, 6] pursue broad generalization through end-to-end training but are constrained by the lack of massive, humanoid-specific datasets. In contrast, approaches incorporating AMP [7, 8] utilize sparse, high-quality data to learn specialized behaviors, yet these methods often suffer from mode collapse[9], which restricts them to specific task categories and necessitates manual, task-specific reward engineering. Motion tracking methods [10, 11] attempt to bypass data scarcity by mimicking single trajectories, but these are essentially limited to rigid motion replay and lack the autonomy needed for novel scenarios. 

To address the shortage of 3D data, recent research employs internet-scale video generation models to provide visual and physical priors for downstream motion trackers. While this pipeline has shown promise in motion tracking [12], applying it to HOI introduces two major challenges. _1) Representation Misalignment._ Extracting 3D motion from 2D videos typically requires strong geometric priors (e.g., explicit object CAD models), which are seldom available in real-world settings. Furthermore, existing methods lack a unified way to jointly estimate robot-object motions. Estimating them independently through mature tools(e.g., GVHMR [13] for robot and FoundationPose [14] for object) introduces spatial and depth discrepancies, leading to low-quality reference motions and tracking failures. Consequently, many works resort to manually designing [11] or heuristically generating [15] methods to rigidly attach objects to robot motions, which still requires CAD models and distorts actual object motion. _2) Retargeting Complexity_ . Most motion tracking models rely on dense, low-level signals like joint positions. To obtain these from human videos, the extracted motion must be explicitly retargeted to a specific humanoid embodiment. In HOI scenarios, this retargeting becomes exceedingly complex: the introduction of object geometry requires intensive, time-consuming morphing [16, 17] to jointly align the robot and object meshes, which inherently amplifies estimation errors from the video source. Avoiding this complex retargeting by tracking sparse keypoints is a promising alternative, but existing methods often struggle with quality. VisualMimic [18] adopts 5-keypoints tracking but fails to achieve natural gaits due to the absence of joint-level information. HEAD [19] employs 3-keypoints tracking and relies on AMP to ensure natural locomotion; however, this reliance restricts its scalability from navigation to interaction tasks. 

In this paper, we propose a zero-shot HOI framework that uses unified 3D point trajectories and a Keypoints Tracker based on the Behavior Foundation Model (BFM) [20, 21, 3] to achieve flexible, geometry-free interaction. To resolve _representation misalignment_ , we extract robot and object motions using a unified 3D point tracker, representing both as 4D point trajectories. This shared representation avoids the need of geometric priors and ensures motions are aligned within a common frame. To address _retargeting complexity_ , our tracker follows only three interaction-critical points: the robot base and hands. By focusing on this minimal set, the framework entirely bypasses the complex, error-amplifying retargeting process. 

To achieve these capabilities despite scarce HOI data, we employ a three-stage progressive training strategy: (1) a whole-body tracking BFM on large-scale proprioceptive motions, (2) a keypoints tracker on loco-manipulation data, and (3) an interaction adaptor on specific HOI data. This approach ensures each stage benefits from the most relevant supervision at scale. By leveraging the BFM, sparse keypoints can still produce stable gaits, allowing the final stages to use simple tracking rewards instead of the complex machinery [11, 10, 22] typically required for learning from scratch. 

This work makes three primary contributions. First, we introduce a unified 4D point trajectory representation for HOI that removes the dependency on geometric priors and resolves motion misalignment. Second, we develop a Keypoints Tracker based on the BFM that focuses on interactioncritical points, enabling flexible interaction alongside stable, natural gaits. Third, we design a progressive training framework that effectively utilizes multi-scale datasets to achieve robust zeroshot HOI without complex, hand-engineered mechanisms. 

2 

## **2 Related Work** 

### **2.1 Humanoid Behavior Foundation Models** 

Humanoid motion tracking [23, 24] serves as the technical cornerstone for robust whole-body control, aiming to produce human-like movements by imitating reference trajectories. To scale these capabilities, recent research [25, 1, 26, 27, 28, 29, 30, 31, 32] focuses on training general-purpose motion trackers using large-scale datasets to reproduce diverse human behaviors. 

Building upon these tracking techniques, Behavior Foundation Models (BFMs) [20, 3, 2, 33, 21] have emerged to construct universal and reusable motion representation spaces. These models distill diverse motor skills into a compact latent space, providing strong physical priors for downstream tasks. Following this paradigm, our proposed framework trains a BFM backbone to function as a robust motion prior. By utilizing the learned latent representation of the BFM as the policy search space, the framework effectively constrains the movements of the humanoid, ensuring natural gaits and whole-body stability even in highly sparse keypoints tracking settings. 

### **2.2 Humanoid-Object Interaction** 

Humanoid-Object Interaction (HOI) has recently achieved significant progress in complex tasks, such as ball sports [34, 35, 36] and pick-and-place operations [8, 37, 38, 39, 40]. However, many of these methods rely heavily on task-specific reward engineering, which limits their generalization across diverse scenarios. Alternative research explores generalizable frameworks through the integration of multimodal instructions [41, 42, 43, 44, 45]. Nevertheless, these approaches often isolate upper-body manipulation from lower-body locomotion or merely concatenate independent modules, thereby failing to exploit the intrinsic whole-body synergies and the high-DoF of the humanoid embodiment. In contrast, recent works have successfully extended the motion tracking paradigm to interaction tasks, enabling humanoids to execute whole-body movements such as carrying boxes or pushing doors [10, 46, 11, 47, 16, 48, 49, 15]. 

To enhance autonomy beyond trajectory replay, recent frameworks establish HOI generation and tracking pipelines [18, 50, 51, 52]. However, due to the scarcity of humanoid interaction data, these generators often synthesize only proprioceptive motions, restricting the robot to static environments or passive interactions. To address this data bottleneck, the proposed method utilizes video generation models as the upstream motion generator. By leveraging the rich visual and physical priors distilled from internet-scale video datasets, the framework achieves autonomous, high-quality, and generalpurpose whole-body interactions. 

### **2.3 Video Generation for Robotics** 

Recent advancements in video generation models have demonstrated remarkable capabilities in synthesizing realistic visual dynamics [53, 54, 55, 56, 57]. Utilizing these priors, research in robotic manipulation tried to employ video generation as an intuitive world model [58, 59, 60, 61]. However, transferring this paradigm to humanoids presents unique challenges. Unlike fixed-base manipulators, humanoids must maintain dynamic stability during complex interactions despite severe data scarcity. 

Pioneering this direction, GenMimic [12] utilizes video generation to synthesize human motions and extract SMPL kinematics for whole-body tracking. However, as discussed in Section 1, extending this pipeline to HOI encounters issues regarding _Representation Misalignment_ and _Retargeting Complexity_ . To bridge this gap, this work introduces unified 3D point trajectories coupled with a BFM-based Keypoints Tracker. By removing the dependency on geometric priors and bypassing complex retargeting, the framework successfully realizes a highly generalizable "video-to-motion-toreal" paradigm for HOI tasks. 

## **3 Methods** 

As illustrated in Figure 2, we address the zero-shot HOI task through a video-guided tracking paradigm. This involves synthesizing an interaction video, extracting reference motions, and controlling the robot to track them. Section 3.1 details the progressive training strategy of the HOI Tracker, which sequentially trains a whole-body tracker backbone, a keypoints tracker, and an interaction 

3 


Figure 2: Overview of the Imagine2Real framework. **Top:** The zero-shot real-world deployment pipeline synthesizes an interaction video, extracts unified 3D point trajectories via a points tracker, and executes the motion using the Keypoints Tracker and Interaction Adaptor. **Bottom:** The policy training adopts a three-stage progressive strategy: (1) training a BFM backbone (Encoder, Predictor, Decoder) on diverse whole-body motions; (2) training a Keypoints Tracker (Planner) on sparse keypoints motions while keeping the BFM decoder frozen; and (3) training an Interaction Adaptor on object manipulation data to refine the final execution. 

adaptor to overcome the scarcity of interaction data. Section 3.2 describes the real-world deployment pipeline, demonstrating the extraction of unified point trajectories from generated videos and their execution within a mocap system. 

### **3.1 HOI Tracker Training** 

Given the disparity between abundant proprioceptive motion data and scarce interaction data, we design a progressive training framework to sequentially develop the humanoid’s interaction capabilities. The pipeline consists of three cascaded modules. A whole-body motion tracker backbone is pre-trained on large-scale datasets (~68.5h) to construct a compact motion representation space. A keypoints tracker is then trained on loco-manipulation data (~8.86h) to track sparse points while maintaining balance. Finally, an interaction adaptor is fine-tuned on limited HOI data (~0.43h). This progressive paradigm fully utilizes multi-level motion datasets under severe data scarcity. By decomposing the complex HOI task, the framework leverages abundant non-interactive data to build foundational priors, reducing the sample complexity required to learn interaction skills. 

### **3.1.1 BFM Backbone** 

Directly learning natural sparse keypoints tracking from scratch via reinforcement learning is fundamentally difficult. When provided with only sparse tracking targets, a naive policy tends to aggressively overfit to the task objectives, severely violating essential physical constraints such as natural gaits and whole-body postural balance. To overcome this, we first train a Behavior Foundation Model (BFM) backbone to construct a versatile and reusable motion representation space. The BFM compresses local motion sequences into a shared latent motion space. At timestep _t_ , given a _δ_ steps motion subsequence **m** _t_ : _t_ + _δ_ = [ **m** _t,_ **m** _t_ +1 _, . . . ,_ **m** _t_ + _δ_ ], a motion encoder _E_ maps it to a latent code **z** _t_ = _E_ ( **m** _t_ : _t_ + _δ_ ) _∈Z_ . Simultaneously, an autoregressive predictor _P_ estimates a latent prior **z** ˆ _t_ based solely on the proprioceptive observation history **o**<sup>prop</sup> 0: _t_ and the previous latent state **z** _t−_ 1, formulated as **z** ˆ _t_ = _P_ ( **o**<sup>prop</sup> 0: _t_<sup>_,_</sup><sup>**z**</sup><sup>_t−_1).To efficiently process the sequential input,the history</sup><sup>**o**prop</sup> 0: _t_ is recursively compressed into a compact hidden state using a Gated Recurrent Unit (GRU). The instantaneous observation at each time step is defined as **o**<sup>prop</sup> _t_ = [ **q** _t,_ **q** ˙ _t,_ **_ω_** _t,_ **_ψ_** _t,_ **p** _t,_ **a** _t−_ 1], capturing joint positions, velocities, base angular velocity, projected gravity, local end-effector positions relative to the base, and the previous action. During the BFM pre-training, this predictor is optimized via a prediction loss to match the encoded reference motion, minimizing _∥_ **z** ˆ _t −_ sg( **z** _t_ ) _∥_ 2<sup>2(where sg is</sup> the stop-gradient operator). The fundamental purpose of training this predictor is to internalize the forward dynamics and natural motion transitions of the humanoid. In downstream tasks where dense 

4 

future reference motions are absent, the frozen predictor functions as an autonomous motor engine. It continuously outputs a physically viable, default motion prior ˆ **z** _t_ to sustain natural locomotion and balance, which can then be slightly modulated by the higher-level sparse tracking policy. 

Finally, a decoder _D_ translates the current latent command **z** _t_ and proprioceptive history into the lowlevel action targets **a** _t_ = _D_ ( **o**<sup>prop</sup> 0: _t_<sup>_,_</sup><sup>**z**</sup><sup>_t_), where</sup><sup>**a**</sup><sup>_t_is the action trained to track the dense whole-body</sup> motion. This pre-trained latent space _Z_ , along with the frozen predictor _P_ and decoder _D_ , serves as a highly structured and physically grounded search space for keypoints tracking. 

### **3.1.2 Keypoints Tracker** 

Rather than tracking the dense reference motion **m** _t_ of the whole body, the Keypoints Tracker is conditioned only on a sparse reference motion subsequence. This module does not relearn a new whole-body controller; instead, it performs task-conditioned biasing on top of the BFM low-level backbone. We treat the predictor _P_<sup>_∗_</sup> and decoder _D_<sup>_∗_</sup> as a frozen low-level backbone. Given the proprioceptive history and the previous latent command, the frozen predictor first produces a latent prior ˆ **z** _t_ = _P_<sup>_∗_</sup> ( **o**<sup>prop</sup> 0: _t_<sup>_,_</sup><sup>**z**</sup> _t_<sup>_′_</sup> _−_ 1<sup>).</sup> 

A latent residual planner _H_ then uses the task commands (i.e., the sparse keypoints tracking targets **m**<sup>kp</sup> _t_ : _t_ + _δ_<sup>), the previous latent</sup><sup>**z**</sup> _t_<sup>_′_</sup> _−_ 1<sup>, and the current latent prior ˆ</sup><sup>**z**</sup><sup>_t_to output a residual command</sup><sup>**z**</sup> _t_<sup>res.</sup> This residual is applied to the latent prior to form the new latent command **z**<sup>_′_</sup> _t_<sup>, which is then decoded</sup> into the full-body action **a**<sup>_′_</sup> _t_<sup>:</sup> 


Here, the superscript _∗_ denotes that the corresponding modules are frozen during training. By applying low-dimensional latent residuals to the current latent prior, the policy preserves natural whole-body dynamics while tracking task-dependent sparse keypoint targets. 

### **3.1.3 Interaction Adaptor** 

Since the BFM backbone is trained solely on non-interactive motion datasets, the latent space of the model inherently lacks the fine-grained dexterity required for object manipulation. To bridge this capability gap, we introduce an Interaction Adaptor that learns a residual joint-level action to refine the output of the Keypoints Tracker, drawing inspiration from the residual control technique used in ResMimic [10]. Specifically, we formulate the Interaction Adaptor as a residual policy _π_ adapt. At each time step, _π_ adapt receives the proprioceptive history **o** 0: _t_ , the sparse robot keypoints motion **m**<sup>kp</sup> _t_<sup>, and the target object motion</sup><sup>**m**obj</sup> _t_ . It then outputs a residual joint-level action ∆ **a** _t_ , which is directly added to the output of the Keypoints Tracker **a**<sup>_′_</sup> _t_<sup>to form the final execution command</sup><sup>**a**int</sup> _t_<sup>:</sup> 


This final adaptation enables precise, contact-rich interactions while preserving stable locomotion from previous stages. Guided by these foundational priors, the adaptor can be efficiently trained with straightforward tracking rewards, bypassing complex mechanisms typically required for learning from scratch, such as object force curriculum [10], contact rewards [10, 11], or Physical State Initialization (PSI) [22]. 

### **3.2 Real-world Deployment** 

**Video-to-Motion Pipeline.** Given a monocular RGB image containing the initial states of the robot and the target object, we synthesize an interaction video conditioned on a text instruction. From this video, we extract reference motions through a three-step process. First, we perform key region segmentation using SAM3 [62] to obtain precise masks for the robot’s left hand, right hand, pelvis, and the target object. Second, we apply SpaTrackerV2 [63] to track the pixels within these masks, yielding 4D point trajectories for each region. Third, to address tracking noise, such as boundary points incorrectly classified as static background, we implement a robust keypoint filtering mechanism. 

5 


Figure 3: Qualitative results in simulation. Time-lapse sequences illustrate natural whole-body coordination across four HOI tasks (carrying/pushing boxes and carrying a suitcase), as well as the robust locomotion capability of our keypoints tracker. 

We filter the tracked points based on the visibility and confidence scores output by SpaTrackerV2, subsequently removing spatio-temporal outliers. The remaining valid point trajectories within each mask are then geometrically averaged and smoothed to produce a single, stable reference trajectory for each corresponding keypoint. 

**Mocap Deployment.** During real-world execution, we utilize a motion capture (mocap) system to fulfill two critical functions. First, it provides real-time global positions of the robot and object keypoints, which serve as inputs to the control policy for the tracking task. Second, it resolves the scale ambiguity inherent in video-generated motions. Because the synthesized videos lack metric depth information, the extracted trajectories represent only relative motions. We utilize the mocap system to directly capture the precise global positions of the keypoints at the initial frame and use them to scale and calibrate the generated trajectories to real-world dimensions. This approach yields higher calibration accuracy compared to monocular metric depth estimation or stereo vision. 

## **4 Experiments** 

The experiments are designed to answer three core questions: (1) Does searching the BFM latent space yield more natural gaits and smoother motions than direct joint-space tracking? (2) For interaction, can our framework complete whole-body HOI tasks despite lacking dense full-body motion information such as joint positions? (3) For real-world deployment, can our pipeline successfully execute the zero-shot process—from video generation to physical HOI execution? 

### **4.1 Experiment Setup** 

**Dataset.** We construct a progressive training and data utilization framework to train the cascaded modules. (1) For the BFM-backbone, we utilize a massive corpus of human motion data from AMASS [64], LAFAN1 [65], and 100STYLE [66], totaling over 10,000 motion clips(~68.5h). These motions are retargeted to the robot using inverse kinematics via pink [67]. (2) For the Keypoints Tracker, we employ the complete body motions from LAFAN1 and OMOMO [68], alongside selected loco-manipulation motions from AMASS. We filter out actions that are inherently difficult to represent with only three critical points (e.g., dancing and flipping), yielding over 4,000 motion clips(~8.86h). (3) For the Interaction Adaptor, we select specific box-carrying and pushing tasks from OMOMO that do not require dexterous hand manipulation. We apply HOI retargeting via holosoma [69], resulting in over 200 motion clips(~0.43h). Note that the policy requires no retargeted data during inference; we use it during training solely to correct human-robot morphological mismatches and provide some auxiliary tracking rewards. 

6 

Table 1: Quantitative evaluation of HOI task execution. We compare our full method (w/ Adaptor) against the baseline keypoints tracker (w/o Adaptor). We report the Success Rate ( **SR** ) and tracking errors (in cm) for the object ( **E** obj), hands ( **E** hands), and robot base ( **E** base). The subscript “-f” denotes the final tracking error at the end of the episode. 

|**Task**|**Method**|**SR**(%)_↑_|**E**obj_↓_|**E**obj-f _↓_|**E**hands|**E**hands-f|**E**base|**E**base-f|
|---|---|---|---|---|---|---|---|---|
|C B|w/o Adaptor|0.00|-|-|-|-|-|-|
|arry ox|w/ Adaptor|82.65|6.34|7.03|7.33|4.46|5.16|4.05|
|Ph B|w/o Adaptor|29.82|11.11|17.87|4.42|2.39|5.85|4.58|
|us ox|w/ Adaptor|64.91|9.00|13.02|7.25|4.81|6.49|4.40|


Table 2: Ablation study of the keypoints tracker. We compare our BFM-based approach against Direct tracking and DAgger baselines. The evaluation reports task success rate ( **SR** ), tracking accuracy ( **E** hands, **E** base), motion naturalness metrics ( **E** mpjae) and action smoothness metrics ( **A** rate, **A** smooth). 

|Method|**SR**(%)_↑_|**E**hands (cm)_↓_|**E**base(cm)_↓_|**E**mpjae (rad)_↓_|**A**rate _↓_|**A**smooth _↓_|
|---|---|---|---|---|---|---|
|Direct|99.16|1.95|1.66|0.44|1.65|0.64|
|DAgger|99.32|3.73|3.32|0.36|0.61|0.20|
|Ours (BFM)|99.36|3.08|3.78|0.25|0.22|0.09|


**Metrics.** We evaluate our method across two primary dimensions: task completion and motion naturalness. <u>(1) Task Completion:</u> _Success Rate (_ **_SR_** _)_ is the percentage of episodes where the relevant tracking errors <u>(hands/base for tracking,</u> object for interaction) remain below 0 _._ 2 m at all times. _Tracking Errors (_ **E** _hands,_ **E** _base,_ **E** _obj)_ and their final-frame counterparts ( **E** hands-f, **E** base-f, **E** obj-f) measure the Euclidean distance between generated and reference trajectories. <u>(2) Motion Naturalness:</u> _Mean Per Joint Angle Error (_ **E** _mpjae)_ reflects gait naturalness (computed against the ground-truth dense motion from which the sparse keypoints were extracted). _Action Rate (_ **A** _rate)_ and _Action Smoothness (_ **A** _smooth)_ compute the first- and second-order derivatives of actions, where lower values indicate smoother commands. 

**Training Details.** We train all policies in Isaac Gym [70] using PPO [71]. The training is accelerated with 8,192 parallel environments on a single RTX 4090 GPU. We employ the Adam optimizer with an initial learning rate of 3 _×_ 10<sup>_−_4</sup> . To simulate 3D tracker noise and enhance robustness, we inject 5cm Gaussian noise into the reference keypoints during the latter two training stages. Due to space constraints, comprehensive training details, including network architectures, hyperparameters, and reward formulations, are deferred to Appendix A. To ensure reproducibility, the anonymized source code and pre-trained checkpoints are provided in the supplementary material. 

### **4.2 Sim2sim Evaluation** 

To verify policy generalization and ensure fair evaluation by preventing overfitting to the Isaac Gym environment, we conduct Sim2Sim evaluations in MuJoCo [72]. All quantitative metrics reported in this section are evaluated in the MuJoCo simulator. 

**Ablation on Keypoints Tracking.** To answer the first question, we ablate our BFM-based Keypoints Tracker against two baselines: a Direct tracking approach (which uses the sparse points directly as commands to track in joint space) and a DAgger baseline (which distills a privileged whole-body tracker into a three-point tracking policy). As shown in Table 2, the Direct baseline achieves the lowest **E** hands and **E** base because it aggressively optimizes for point matching without any physical constraints. However, this comes at the cost of extreme jittering ( **A** rate = 1 _._ 65, **A** smooth = 0 _._ 64) and unnatural whole-body postures ( **E** mpjae is exceptionally high), making it nearly impossible to deploy on a real robot. Distilling a prior via DAgger slightly mitigates these issues, but the errors remain relatively high. In contrast, by restricting the search space to the latent space of the BFM rather than the raw joint space, our framework significantly reduces **A** rate, **A** smooth, and **E** mpjae, proving that our method can execute the necessary tracking while maintaining relative natural gaits and soft actions. 

**HOI Task Execution.** To answer the second question regarding interaction capability under sparse motion information, we evaluate our framework on carrying and pushing boxes. As detailed in Table 1, our framework successfully completes these tasks with high success rates. Furthermore, 

7 


Figure 4: Qualitative results of zero-shot real-world deployment. Time-lapse sequences demonstrate the robot successfully executing diverse physical tasks, including lifting various boxes and performing a semantically rich interaction (hitting an “Iron Man” pillar). 

the comparison between the _w/ Adaptor_ and _w/o Adaptor_ settings demonstrates that the Interaction Adaptor is essential for bridging the gap between kinematic tracking and successful physical object manipulation. The relatively lower success rate for pushing the large box stems from the lack of marker orientation input—omitted because it is notoriously difficult to robustly extract from videos, which hinders the robot from finely adjusting its hands during pushing. Qualitative results of these simulated interactions are visualized in Figure 3. 

### **4.3 Real-world Evaluation** 

**Setup.** The real-world deployment pipeline involves three components. First, for video generation, we select Seedance 2.0 Fast [57], which exhibits the best instruction-following capabilities and generation consistency. The detailed text prompts used for video generation are provided in Appendix B. Second, for point tracking, we utilize SAM3 to segment key parts (the robot’s base and hands, and the object) and SpaTrackerV2 to perform 4D point tracking. Finally, we deploy the policy on a Unitree G1 humanoid robot within a motion capture (mocap) system. 

**Zero-Shot Real-World Pipeline.** To answer the third question, we validate the complete zero-shot deployment capabilities of our pipeline in the real world, see Figure 4. The robot successfully lifts various types of boxes, and by leveraging the generative capabilities of the video model, it can also execute semantically rich interactive tasks, such as hitting an “Iron Man” pillar. 

## **5 Conclusion and Limitations** 

We propose Imagine2Real for zero-shot Humanoid-Object Interaction (HOI). To overcome representation misalignment and retargeting complexity in video-driven methods, we formulate robot and object motions as unified 4D point trajectories and track only sparse critical points. By utilizing the latent space of a Behavior Foundation Model (BFM) as the tracking search domain, Imagine2Real bypasses explicit geometric priors while maintaining natural whole-body gaits. Experiments demonstrate high success rates and robust motion tracking in representative whole-body HOI tasks (e.g., carrying and pushing objects), culminating in successful zero-shot physical deployment on a real humanoid robot. 

Our framework currently faces two main limitations. First, real-world deployment relies on motion capture systems, which are prone to marker occlusion during close-contact tasks(e.g., pushing boxes). Future work could integrate self-tracking systems using on-device SLAM and multi-camera fusion (e.g., HTC VIVE Tracker). Second, the current pipeline is open-loop. While iteratively prompting the video model provides a pseudo-closed-loop approximation, it is highly inefficient. A true closed-loop system requires jointly fine-tuning the video generator and motion tracker using physical feedback. This remains challenging, as the most capable video models are closed-source APIs, and open-source alternatives (e.g., Wan2.2 [56]) still lack the physical consistency required for complex interactions. 

8 

## **References** 

- [1] Zixuan Chen, Mazeyu Ji, Xuxin Cheng, Xuanbin Peng, Xue Bin Peng, and Xiaolong Wang. Gmt: General motion tracking for humanoid whole-body control. _arXiv preprint arXiv:2506.14770_ , 2025. 

- [2] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [3] Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Castaneda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [4] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [5] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 

- [6] Physical Intelligence, Bo Ai, Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Greg Balke, Kevin Black, George Bokinsky, Shihao Cao, Thomas Charbonnier, et al. Pi0.7: a steerable generalist robotic foundation model with emergent capabilities. _arXiv preprint arXiv:2604.15483_ , 2026. 

- [7] Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ , 40(4):1–20, 2021. 

- [8] Huayi Wang, Wentao Zhang, Runyi Yu, Tao Huang, Junli Ren, Feiyu Jia, Zirui Wang, Xiaojie Niu, Xiao Chen, Jiahe Chen, et al. Physhsi: Towards a real-world generalizable and natural humanoid-scene interaction system. _arXiv preprint arXiv:2510.11072_ , 2025. 

- [9] Tim Salimans, Ian Goodfellow, Wojciech Zaremba, Vicki Cheung, Alec Radford, and Xi Chen. Improved techniques for training gans. _Advances in neural information processing systems_ , 29, 2016. 

- [10] Siheng Zhao, Yanjie Ze, Yue Wang, C Karen Liu, Pieter Abbeel, Guanya Shi, and Rocky Duan. Resmimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning. _arXiv preprint arXiv:2510.05070_ , 2025. 

- [11] Haoyang Weng, Yitang Li, Nikhil Sobanbabu, Zihan Wang, Zhengyi Luo, Tairan He, Deva Ramanan, and Guanya Shi. Hdmi: Learning interactive humanoid whole-body control from human videos. _arXiv preprint arXiv:2509.16757_ , 2025. 

- [12] James Ni, Zekai Wang, Wei Lin, Amir Bar, Yann LeCun, Trevor Darrell, Jitendra Malik, and Roei Herzig. From generated human videos to physically plausible robot trajectories. _arXiv preprint arXiv:2512.05094_ , 2025. 

- [13] Zehong Shen, Huaijin Pi, Yan Xia, Zhi Cen, Sida Peng, Zechen Hu, Hujun Bao, Ruizhen Hu, and Xiaowei Zhou. World-grounded human motion recovery via gravity-view coordinates. In _SIGGRAPH Asia 2024 Conference Papers_ , pages 1–11, 2024. 

- [14] Bowen Wen, Wei Yang, Jan Kautz, and Stan Birchfield. Foundationpose: Unified 6d pose estimation and tracking of novel objects. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 17868–17879, 2024. 

- [15] Yinhuai Wang, Qihan Zhao, Yuen Fui Lau, Runyi Yu, Hok Wai Tsui, Qifeng Chen, Jingbo Wang, Jiangmiao Pang, and Ping Tan. Humanx: Toward agile and generalizable humanoid interaction skills from human videos. _arXiv preprint arXiv:2602.02473_ , 2026. 

- [16] Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, Pieter Abbeel, Carmelo Sferrazza, C Karen Liu, Rocky Duan, and Guanya Shi. Omniretarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

9 

- [17] Edmond SL Ho, Taku Komura, and Chiew-Lan Tai. Spatial relationship preserving character motion adaptation. In _ACM SIGGRAPH 2010 papers_ , pages 1–8. 2010. 

- [18] Shaofeng Yin, Yanjie Ze, Hong-Xing Yu, C Karen Liu, and Jiajun Wu. Visualmimic: Visual humanoid loco-manipulation via motion tracking and generation. _arXiv preprint arXiv:2509.20322_ , 2025. 

- [19] Sirui Chen, Yufei Ye, Zi-ang Cao, Jennifer Lew, Pei Xu, and C Karen Liu. Hand-eye autonomous delivery: Learning humanoid navigation, locomotion and reaching. _arXiv preprint arXiv:2508.03068_ , 2025. 

- [20] Yitang Li, Zhengyi Luo, Tonghe Zhang, Cunxi Dai, Anssi Kanervisto, Andrea Tirinzoni, Haoyang Weng, Kris Kitani, Mateusz Guzek, Ahmed Touati, et al. Bfm-zero: A promptable behavioral foundation model for humanoid control using unsupervised reinforcement learning. _arXiv preprint arXiv:2511.04131_ , 2025. 

- [21] Weishuai Zeng, Shunlin Lu, Kangning Yin, Xiaojie Niu, Minyue Dai, Jingbo Wang, and Jiangmiao Pang. Behavior foundation model for humanoid robots. _arXiv preprint arXiv:2509.13780_ , 2025. 

- [22] Sirui Xu, Hung Yu Ling, Yu-Xiong Wang, and Liang-Yan Gui. Intermimic: Towards universal whole-body control for physics-based human-object interactions. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 12266–12277, 2025. 

- [23] Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. Deepmimic: Exampleguided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- [24] Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbab, Chaoyi Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. _arXiv preprint arXiv:2502.01143_ , 2025. 

- [25] Zhengyi Luo, Jinkun Cao, Kris Kitani, Weipeng Xu, et al. Perpetual humanoid control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 10895–10904, 2023. 

- [26] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024. 

- [27] Tairan He, Wenli Xiao, Toru Lin, Zhengyi Luo, Zhenjia Xu, Zhenyu Jiang, Jan Kautz, Changliu Liu, Guanya Shi, Xiaolong Wang, et al. Hover: Versatile neural whole-body controller for humanoid robots. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9989–9996. IEEE, 2025. 

- [28] Mazeyu Ji, Xuanbin Peng, Fangchen Liu, Jialong Li, Ge Yang, Xuxin Cheng, and Xiaolong Wang. Exbody2: Advanced expressive humanoid whole-body control. _arXiv preprint arXiv:2412.13196_ , 2024. 

- [29] Yanjie Ze, Siheng Zhao, Weizhuo Wang, Angjoo Kanazawa, Rocky Duan, Pieter Abbeel, Guanya Shi, Jiajun Wu, and C Karen Liu. Twist2: Scalable, portable, and holistic humanoid data collection system. _arXiv preprint arXiv:2511.02832_ , 2025. 

- [30] Tengjie Zhu, Guanyu Cai, Yang Zhaohui, Guanzhu Ren, Haohui Xie, ZiRui Wang, Junsong Wu, Jingbo Wang, Xiaokang Yang, Yao Mu, et al. Clot: Closed-loop global motion tracking for whole-body humanoid teleoperation. _arXiv preprint arXiv:2602.15060_ , 2026. 

- [31] Yixuan Pan, Ruoyi Qiao, Li Chen, Kashyap Chitta, Liang Pan, Haoguang Mai, Qingwen Bu, Hao Zhao, Cunyuan Zheng, Ping Luo, et al. Agility meets stability: Versatile humanoid control with heterogeneous data. _arXiv preprint arXiv:2511.17373_ , 2025. 

- [32] Yunshen Wang, Shaohang Zhu, Peiyuan Zhi, Yuhan Li, Jiaxin Li, Yong-Lu Li, Yuchen Xiao, Xingxing Wang, Baoxiong Jia, and Siyuan Huang. Omnixtreme: Breaking the generality barrier in high-dynamic humanoid control. _arXiv preprint arXiv:2602.23843_ , 2026. 

- [33] Kangning Yin, Weishuai Zeng, Ke Fan, Minyue Dai, Zirui Wang, Qiang Zhang, Zheng Tian, Jingbo Wang, Jiangmiao Pang, and Weinan Zhang. Unitracker: Learning universal whole-body motion tracker for humanoid robots. _IEEE Robotics and Automation Letters_ , 2026. 

10 

- [34] Zhikai Zhang, Haofei Lu, Yunrui Lian, Ziqing Chen, Yun Liu, Chenghuai Lin, Han Xue, Zicheng Zeng, Zekun Qi, Shaolin Zheng, et al. Learning athletic humanoid tennis skills from imperfect human motion data. _arXiv preprint arXiv:2603.12686_ , 2026. 

- [35] Junli Ren, Yinghui Li, Kai Zhang, Penglin Fu, Haoran Jiang, Yixuan Pan, Guangjun Zeng, Tao Huang, Weizhong Guo, Peng Lu, et al. Smash: Mastering scalable whole-body skills for humanoid ping-pong with egocentric vision. _arXiv preprint arXiv:2604.01158_ , 2026. 

- [36] Junli Ren, Junfeng Long, Tao Huang, Huayi Wang, Zirui Wang, Feiyu Jia, Wentao Zhang, Jingbo Wang, Ping Luo, and Jiangmiao Pang. Humanoid goalkeeper: Learning from position conditioned task-motion constraints. _arXiv preprint arXiv:2510.18002_ , 2025. 

- [37] Zhi Su, Bike Zhang, Nima Rahmanian, Yuman Gao, Qiayuan Liao, Caitlin Regan, Koushil Sreenath, and S Shankar Sastry. Hitter: A humanoid table tennis robot via hierarchical planning and learning. _arXiv preprint arXiv:2508.21043_ , 2025. 

- [38] Jeremy Dao, Helei Duan, and Alan Fern. Sim-to-real learning for humanoid box locomanipulation. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 16930–16936. IEEE, 2024. 

- [39] Fukang Liu, Zhaoyuan Gu, Yilin Cai, Ziyi Zhou, Hyunyoung Jung, Jaehwi Jang, Shijie Zhao, Sehoon Ha, Yue Chen, Danfei Xu, et al. Opt2skill: Imitating dynamically-feasible whole-body trajectories for versatile humanoid loco-manipulation. _IEEE Robotics and Automation Letters_ , 2025. 

- [40] Chong Zhang, Wenli Xiao, Tairan He, and Guanya Shi. Wococo: Learning whole-body humanoid control with sequential contacts. _arXiv preprint arXiv:2406.06005_ , 2024. 

- [41] Yanjie Ze, Zixuan Chen, Wenhao Wang, Tianyi Chen, Xialin He, Ying Yuan, Xue Bin Peng, and Jiajun Wu. Generalizable humanoid manipulation with 3d diffusion policies. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 2873–2880. IEEE, 2025. 

- [42] Zipeng Fu, Qingqing Zhao, Qi Wu, Gordon Wetzstein, and Chelsea Finn. Humanplus: Humanoid shadowing and imitation from humans. _arXiv preprint arXiv:2406.10454_ , 2024. 

- [43] Haoru Xue, Xiaoyu Huang, Dantong Niu, Qiayuan Liao, Thomas Kragerud, Jan Tommy Gravdahl, Xue Bin Peng, Guanya Shi, Trevor Darrell, Koushil Sreenath, et al. Leverb: Humanoid whole-body control with latent vision-language instruction. _arXiv preprint arXiv:2506.13751_ , 2025. 

- [44] Yuanhang Zhang, Yifu Yuan, Prajwal Gurunath, Ishita Gupta, Shayegan Omidshafiei, Ali-akbar Agha-mohammadi, Marcell Vazquez-Chanlatte, Liam Pedersen, Tairan He, and Guanya Shi. Falcon: Learning force-adaptive humanoid loco-manipulation. _arXiv preprint arXiv:2505.06776_ , 2025. 

- [45] Qingwei Ben, Feiyu Jia, Jia Zeng, Junting Dong, Dahua Lin, and Jiangmiao Pang. Homie: Humanoid loco-manipulation with isomorphic exoskeleton cockpit. _arXiv preprint arXiv:2502.13013_ , 2025. 

- [46] Xialin He, Sirui Xu, Xinyao Li, Runpei Dong, Liuyu Bian, Yu-Xiong Wang, and Liang-Yan Gui. Ultra: Unified multimodal control for autonomous humanoid whole-body loco-manipulation. _arXiv preprint arXiv:2603.03279_ , 2026. 

- [47] Yuhui Fu, Feiyang Xie, Chaoyi Xu, Jing Xiong, Haoqi Yuan, and Zongqing Lu. Demohlm: From one demonstration to generalizable humanoid loco-manipulation. _arXiv preprint arXiv:2510.11258_ , 2025. 

- [48] Dayang Liang, Yuhang Lin, Xinzhe Liu, Jiyuan Shi, Yunlong Liu, and Chenjia Bai. Interreal: A unified physics-based imitation framework for learning human-object interaction skills. _arXiv preprint arXiv:2603.07516_ , 2026. 

- [49] Yuhang Lin, Jiyuan Shi, Dewei Wang, Jipeng Kong, Yong Liu, Chenjia Bai, and Xuelong Li. Pro-hoi: Perceptive root-guided humanoid-object interaction. _arXiv preprint arXiv:2603.01126_ , 2026. 

- [50] Dvij Kalaria, Sudarshan S Harithas, Pushkal Katara, Sangkyung Kwak, Sarthak Bhagat, Shankar Sastry, Srinath Sridhar, Sai Vemprala, Ashish Kapoor, and Jonathan Chung-Kuan Huang. Dreamcontrol: Human-inspired whole-body humanoid control for scene interaction via guided diffusion. _arXiv preprint arXiv:2509.14353_ , 2025. 

11 

- [51] Arthur Allshire, Hongsuk Choi, Junyi Zhang, David McAllister, Anthony Zhang, Chung Min Kim, Trevor Darrell, Pieter Abbeel, Jitendra Malik, and Angjoo Kanazawa. Visual imitation enables contextual humanoid control. _arXiv preprint arXiv:2505.03729_ , 2025. 

- [52] Haoran Yang, Jiacheng Bao, Yucheng Xin, Haoming Song, Yuyang Tian, Bin Zhao, Dong Wang, and Xuelong Li. Zerowbc: Learning natural visuomotor humanoid control directly from human egocentric video. _arXiv preprint arXiv:2603.09170_ , 2026. 

- [53] OpenAI. Video generation models as world simulators. Technical report, OpenAI, 2024. 

- [54] Runway. Gen-3 alpha. Technical report, Runway, 2024. 

- [55] Kuaishou. Kling 1.5. Technical report, Kuaishou Technology, 2024. 

- [56] Team Wan, Ang Wang, Baole Ai, Bin Wen, Chaojie Mao, Chen-Wei Xie, Di Chen, Feiwu Yu, Haiming Zhao, Jianxiao Yang, Jianyuan Zeng, Jiayu Wang, Jingfeng Zhang, Jingren Zhou, Jinkai Wang, Jixuan Chen, Kai Zhu, Kang Zhao, Keyu Yan, Lianghua Huang, Mengyang Feng, Ningyi Zhang, Pandeng Li, Pingyu Wu, Ruihang Chu, Ruili Feng, Shiwei Zhang, Siyang Sun, Tao Fang, Tianxing Wang, Tianyi Gui, Tingyu Weng, Tong Shen, Wei Lin, Wei Wang, Wei Wang, Wenmeng Zhou, Wente Wang, Wenting Shen, Wenyuan Yu, Xianzhong Shi, Xiaoming Huang, Xin Xu, Yan Kou, Yangyu Lv, Yifei Li, Yijing Liu, Yiming Wang, Yingya Zhang, Yitong Huang, Yong Li, You Wu, Yu Liu, Yulin Pan, Yun Zheng, Yuntao Hong, Yupeng Shi, Yutong Feng, Zeyinzi Jiang, Zhen Han, Zhi-Fan Wu, and Ziyu Liu. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_ , 2025. 

- [57] ByteDance. Seedance 2.0 fast. Technical report, ByteDance, 2025. 

- [58] Shivansh Patel, Shraddhaa Mohan, Hanlin Mai, Unnat Jain, Svetlana Lazebnik, and Yunzhu Li. Robotic manipulation by imitating generated videos without physical demonstrations. _arXiv preprint arXiv:2507.00990_ , 2025. 

- [59] Kai Ye, Yuhang Wu, Shuyuan Hu, Junliang Li, Meng Liu, Yongquan Chen, and Rui Huang. Gen2real: Towards demo-free dexterous manipulation by harnessing generated video. _arXiv preprint arXiv:2509.14178_ , 2025. 

- [60] Jhen Hsieh, Kuan-Hsun Tu, Kuo-Han Hung, and Tsung-Wei Ke. Dexman: Learning bimanual dexterous manipulation from human and generated videos. _arXiv preprint arXiv:2510.08475_ , 2025. 

- [61] Zeyi Liu, Shuang Li, Eric Cousineau, Siyuan Feng, Benjamin Burchfiel, and Shuran Song. Geometry-aware 4d video generation for robot manipulation. _arXiv preprint arXiv:2507.01099_ , 2025. 

- [62] Nicolas Carion, Laura Gustafson, Yuan-Ting Hu, Shoubhik Debnath, Ronghang Hu, Didac Suris, Chaitanya Ryali, Kalyan Vasudev Alwala, Haitham Khedr, Andrew Huang, et al. Sam 3: Segment anything with concepts. _arXiv preprint arXiv:2511.16719_ , 2025. 

- [63] Yuxi Xiao, Jianyuan Wang, Nan Xue, Nikita Karaev, Yuri Makarov, Bingyi Kang, Xing Zhu, Hujun Bao, Yujun Shen, and Xiaowei Zhou. Spatialtrackerv2: 3d point tracking made easy. _arXiv preprint arXiv:2507.12462_ , 2025. 

- [64] Naureen Mahmood, Nima Ghorbani, Nikolaus F Troje, Gerard Pons-Moll, and Michael J Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 5442–5451, 2019. 

- [65] Félix G Harvey, Mike Yurick, Derek Nowrouzezahrai, and Christopher Pal. Robust motion in-betweening. _ACM Transactions on Graphics (TOG)_ , 39(4):60–1, 2020. 

- [66] Ian Mason, Sebastian Starke, and Taku Komura. Real-time style modelling of human locomotion via feature-wise transformations and local motion phases. _Proceedings of the ACM on Computer Graphics and Interactive Techniques_ , 5(1):1–18, 2022. 

- [67] Stéphane Caron, Yann De Mont-Marin, Rohan Budhiraja, Seung Hyeon Bang, Ivan Domrachev, Simeon Nedelchev, Peter Du, Adrien Escande, Joris Vaillant, Bruce Wingo, Santosh Patapati, Daniel San José Pro, and Nicolas Guillermo Marticorena Vidal. Pink: Python inverse kinematics based on Pinocchio, 2026. 

- [68] Jiaman Li, Jiajun Wu, and C Karen Liu. Object motion guided human motion synthesis. _ACM Transactions on Graphics (TOG)_ , 42(6):1–11, 2023. 

12 

- [69] Amazon FAR, Pieter Abbeel, Juyue Chen, Rocky Duan, Alejandro Escontrela, Manan Gandhi, Samuel Gundry, Xiaoyu Huang, Angjoo Kanazawa, Tomasz Lewicki, Jiaman Li, Karen Liu, Clay Rosenthal, Younggyo Seo, Carlo Sferrazza, Guanya Shi, Linda Shih, Jonathan Tseng, Zhen Wu, Lujie Yang, Brent Yi, and Yuanhang Zhang. Holosoma. 

- [70] Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 

- [71] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [72] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ international conference on intelligent robots and systems_ , pages 5026–5033. IEEE, 2012. 

13 

## **Appendix** 

## **A Training Details** 

In this section, we provide comprehensive training details for the three-stage progressive learning framework introduced in Section 3.1, including the network architectures, hyperparameters, reward functions, and domain randomization strategies. All three policies are trained in the Isaac Gym simulator. 

### **A.1 Simulation Setup** 

The physics simulation runs at a frequency of 250 Hz (∆ _t_ = 0 _._ 004 s). The low-level PD controller updates at 50 Hz, corresponding to a decimation factor of 5. The Keypoints Tracker and Interaction Adaptor operate at a high-level control frequency of 10 Hz (∆ _t_ = 0 _._ 1 s), outputting latent residuals and joint residuals, respectively. To robustly simulate the rich variations of the real world and generate diverse interactions, we deploy 8,192 parallel environments per training session. 

### **A.2 Network Architectures and Optimization** 

Table 3 summarizes the detailed network architectures and Proximal Policy Optimization (PPO) hyperparameters for each stage. 

**BFM Backbone.** The BFM backbone is designed to extract a compact 32-dimensional latent space from diverse whole-body motion datasets. The motion encoder compresses local motion sequences into latents using a 6-layer Multi-Layer Perceptron (MLP) with hidden dimensions of 512, followed by a linear layer projecting to 256. The autoregressive prior predictor processes the proprioceptive history using a Gated Recurrent Unit (GRU) with a hidden size of 256, followed by a 6-layer MLP of size 1024. Finally, the decoder (actor) translates the latent representations into target joint positions via an equivalent 6-layer MLP of size 1024. During training, the BFM is optimized with specialized latent consistency losses over 5 epochs and 10 mini-batches per iteration, where the overlap loss coefficient is 0.35, the commitment loss coefficient is 0.25, and the triplet loss coefficient is set to 5.0. 

**Keypoints Tracker.** Building upon the frozen BFM, the Keypoints Tracker learns to output latent residuals to track sparse marker targets. Its actor network fuses the GRU history (dimension 256) with a 3-layer MLP of dimensions [256 _,_ 256 _,_ 128]. The critic network utilizes a 5-layer MLP of dimensions [512 _,_ 512 _,_ 512 _,_ 512 _,_ 256]. We train this policy with an adaptive learning rate bounded between 1 _×_ 10<sup>_−_5</sup> and 1 _×_ 10<sup>_−_4</sup> (initialized at 2 _×_ 10<sup>_−_4</sup> ), targeting a KL divergence of 0.05. 

**Interaction Adaptor.** The Interaction Adaptor outputs fine-grained joint residuals to complement the Keypoints Tracker. Due to the complexity of object interactions, it employs a slightly larger actor MLP of dimensions [256 _,_ 256 _,_ 128]. It shares the same critic architecture as the Keypoints Tracker but relies on a learnable action noise bounded between [0 _._ 01 _,_ 2 _._ 0] (initialized at 1.0) to encourage enhanced exploration during the contact-rich phases of learning. The target KL divergence is set to 0.02. 

### **A.3 Reward Functions** 

Both the Keypoints Tracker and Interaction Adaptor are trained using straightforward tracking rewards formulated via the exponential kernel function _r_ = exp( _−∥x − x_ ˆ _∥_<sup>2</sup> _/σ_ ), circumventing the need for manually designed complex heuristics. The detailed reward terms, their corresponding scales, and kernel bandwidth parameters ( _σ_ ) are delineated in Table 4. 

For the Keypoints Tracker, tracking precision focuses heavily on the 3D position of the specified marker (e.g., wrist) and the robot base. When advancing to the Interaction Adaptor, the marker tracking bandwidth ( _σ_ ) is sharpened from 0.2 to 0.1 to demand tighter precision, and new highly weighted reward terms are introduced to explicitly track the object’s 6-DoF pose and interaction geometry (IG). This ensures the robot grasps and manipulates the object strictly as demonstrated. Several regularization penalties, including energy constraints, action smoothness, and feet contact stability, are maintained identically across both stages to preserve natural locomotion priors. 

14 

Table 3: PPO Hyperparameters and Network Architectures across the three training stages. 

|**Hyperparameter**|**BFM Backbone**|**Keypoints Tracker**|**Interaction Adaptor**|
|---|---|---|---|
|_Network Architectures_||||
|Prior/Actor RNN|GRU (256)|GRU (256)|GRU (256)|
|Actor/Decoder MLP|[1024]_×_6_→_128|[256_,_256_,_128]|[256_,_256_,_128]|
|Critic MLP|-|[512]_×_4_→_256|[512]_×_4_→_256|
|Latent Dimension|32|32|-|
|_Optimization (PPO)_||||
|Learning Rate|Adaptive (1_×_10<sup>_−_4</sup>)|Adaptive (2_×_10<sup>_−_4</sup>)|Adaptive (1_×_10<sup>_−_4</sup>)|
|Target KL Divergence|0.02|0.05|0.02|
|Discount Factor_γ_|0.99|0.99|0.99|
|GAE_λ_|0.95|0.95|0.95|
|Value Loss Coefficient|2.0|2.0|3.0|
|Entropy Coefficient|0.01|3_×_10<sup>_−_4</sup>|1_×_10<sup>_−_3</sup>|
|Clip Parameter|0.2|0.2|0.2|
|Epochs|5|10|5|
|Mini-batches|10|8|10|
|Action Noise|0.005 (constant)|0.02 (constant)|1.0 (learnable)|


Table 4: Detailed Reward Formulation for the Keypoints Tracker and Interaction Adaptor. Tracking terms utilize an exponential kernel _r_ = exp( _−∥x − x_ ˆ _∥_<sup>2</sup> _/σ_ ). 

|**Reward Term**|**Keypoint**|**s Tracker**|**Interactio**|**n Adaptor**|
|---|---|---|---|---|
||**Weight**|_σ_|**Weight**|_σ_|
|_Tracking Rewards_|||||
|Base Position|4.0|0.2|4.0|0.1|
|Base Rotation|2.0|1.2|2.0|0.6|
|Marker Position|8.0|0.2|4.0|0.1|
|Marker Rotation|2.0|1.2|2.0|1.0|
|Joint Position|4.0|20.0|4.0|10.0|
|Joint Velocity|2.0|50.0|2.0|30.0|
|Feet Height|4.0|0.15|4.0|0.1|
|Object Position|-|-|12.0|0.1|
|Object Rotation|-|-|3.0|1.0|
|_Penalty Rewards_|||||
|Termination|-10.0|-|-10.0|-|
|Joint Torques|-2.0|-|-2.0|-|
|Action Rates|-2.0|-|-2.0|-|
|Action Smoothness|-2.0|-|-2.0|-|


### **A.4 Domain Randomization** 

To facilitate reliable zero-shot sim-to-real transfer, we apply robust domain randomization across the simulation physics parameters, robot configurations, control noises, and external disturbances. During the Interaction Adaptor training, we additionally randomize the target object’s physical attributes, including its mass, friction, and scale, to ensure the policy generalizes against perception inaccuracies and physical discrepancies in unstructured real-world deployment. The exhaustive list of randomization parameters and their ranges is provided in Table 5. 

## **B Video Generation Prompts** 

To ensure the generated videos maintain physical realism and temporal consistency suitable for downstream motion extraction, we append a standardized set of constraints to the task-specific text instructions (e.g., “The robot walks forward and carries the box”). The complete prompt template is structured as follows: 

15 

### **Video Generation Prompt Template** 

**[Task Description] Constraints:** 

- **Camera:** Remain fixed and stationary throughout the entire video, with the perspective matching the original image. 

- **Robot:** The robot’s limbs are rigid bodies, and its motion is restricted to revolute joints without any soft or elastic deformation. 

- **Physics:** The robot’s motion must be physically accurate, natural, smooth, and realistic. 

- **Environment:** Keep the background, floor, and lighting settings in the image unchanged. 

Table 5: Sim-to-Real Domain Randomization Parameters. 

|**Parameter**|**Range / Value**|
|---|---|
|_Robot Dynamics_||
|Link Mass|[0_._8_,_1_._2]_×_default<br>|
|Link Center of Mass (CoM) Offset|[_−_0_._1_,_0_._1]m|
|Base Payload|[_−_0_._1_,_0_._2]kg|
|Link Restitution|[0_._0_,_0_._5]|
|Link Friction|[0_._3_,_1_._5]|
|Joint Friction|[0_._5_,_2_._0]N_·_m<br>|
|Joint Damping|[0_._3_,_1_._5]_×_default|
|Joint Armature|[1_._0_,_1_._05]_×_default|
|_Control & Perturbations_||
|PD Stiffness (_Kp_)|[0_._9_,_1_._1]_×_default<br>|
|PD Damping (_Kd_)|[0_._9_,_1_._1]_×_default|
|Joint Injection Noise|[_−_0_._01_,_0_._01]rad|
|Actuation Offset|[_−_0_._01_,_0_._01]rad|
|Push Robot Base (Linear Velocity)|∆_vxy ≤_0_._5m/s,∆_vz ≤_0_._2m/s (every 1–5s)|
|Push Robot Base (Angular Velocity)|∆_ωxy ≤_0_._6rad/s,∆_ωz ≤_0_._8rad/s (every 1–5s)|
|Push Robot Body (Force)|up to20N for 0.1–0.2s (every 1–5s)|
|_Object Properties (Interaction Adaptor only)_||
|Object Mass|0_._05_∼_1_._5kg (base0_._5kg_±_noise)|
|Object CoM Offset|[_−_0_._05_,_0_._05]m|
|Object Friction|[0_._1_,_1_._2]|
|Object Rolling Friction|[0_._0_,_0_._1]|
|<br>Object Restitution|[0_._0_,_0_._2]|
|Object Scale|[0_._8_,_1_._1]_×_default|
|Initial Position Offset|up to0_._1m|
|Initial Rotation Offset|<br>up to5<sup>_◦_</sup>|


16 

