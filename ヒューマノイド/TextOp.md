---
title: "TextOp: Real-time Interactive Text-Driven Humanoid Robot Motion Generation and Control"
date: "2026-02-07"
authors: "Weiji Xie; Jiakun Zheng; Jinrui Han; Jiyuan Shi; Weinan Zhang; Chenjia Bai"
url: https://arxiv.org/abs/2602.07439
pdf: https://arxiv.org/pdf/2602.07439
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.07439)** / [論文ページ](https://arxiv.org/abs/2602.07439)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# TextOp: Real-time Interactive Text-Driven Humanoid Robot Motion Generation and Control 

Weiji Xie<sup>1,2*</sup> Jiakun Zheng<sup>1,3*</sup> Jinrui Han<sup>1,2</sup> Jiyuan Shi<sup>1</sup> Weinan Zhang<sup>2†</sup> Chenjia Bai<sup>1†</sup> Xuelong Li<sup>1</sup> 

> 1Institute of Artificial Intelligence (TeleAI), China Telecom 2Shanghai Jiao Tong University 

> 3East China University of Science and Technology 

> *Equal contribution †Corresponding author 


Fig. 1: **TextOp enables a humanoid robot to execute a seamless sequence of diverse skills—ranging from expressive gestures to complex physical tasks—driven by real-time, interactive text commands from the user in a single continuous trial.** 

**_Abstract_ —Recent advances in humanoid whole-body motion tracking have enabled the execution of diverse and highly coordinated motions on real hardware. However, existing controllers are commonly driven either by predefined motion trajectories, which offer limited flexibility when user intent changes, or by continuous human teleoperation, which requires constant human involvement and limits autonomy. This work addresses the problem of how to drive a universal humanoid controller in a real-time and interactive manner. We present TextOp, a real-time text-driven humanoid motion generation and control framework that supports streaming language commands and onthe-fly instruction modification during execution. TextOp adopts a two-level architecture in which a high-level autoregressive** 

**motion diffusion model continuously generates short-horizon kinematic trajectories conditioned on the current text input, while a low-level motion tracking policy executes these trajectories on a physical humanoid robot. By bridging interactive motion generation with robust whole-body control, TextOp unlocks freeform intent expression and enables smooth transitions across multiple challenging behaviors such as dancing and jumping, within a single continuous motion execution. Extensive realrobot experiments and offline evaluations demonstrate instant responsiveness, smooth whole-body motion, and precise control. The project page and the open-source code are available at https://text-op.github.io/.** 

## I. INTRODUCTION 

Recent years have witnessed rapid progress in universal humanoid whole-body motion tracking systems [32, 18, 12, 17, 64, 26], capable of robustly executing a wide range of highly coordinated behaviors on real hardware. Leveraging advances in reinforcement learning [3, 43] and large-scale physical simulation [34, 50], modern humanoid platforms can reliably track diverse kinematic references and perform complex full-body motions under a unified control framework. From a control perspective, the problem of executing rich humanoid behaviors is increasingly well-addressed. 

However, **how to flexibly and interactively drive such universal controllers remains an open challenge** . In existing systems, universal humanoid controllers are commonly driven by either predefined motion trajectories [12, 17, 70] or continuous human teleoperation [65, 66, 18]. Predefined trajectories, while effective for reproducing specific motions, offer little flexibility at runtime: once execution begins, the robot’s behavior is mainly determined by the trajectory and cannot easily adapt to changes in intent. Teleoperation, on the other hand, enables direct guidance but relies heavily on sustained human involvement, making long-term operation laborintensive and limiting the autonomy of the robot. As a result, a gap persists between high-level human intent expression and low-level humanoid execution, despite significant advances in the underlying control technology. 

In this context, natural language has emerged as a powerful modality for guiding robot behavior. A growing body of work on text-conditioned motion generation demonstrates that language can flexibly describe complex, semantically meaningful motions [11, 49, 25]. Inspired by this idea, some approaches first explicitly generate full motion sequences and then employ a tracking policy to track them on the robot [18, 44, 64, 17], while others embed motion generation implicitly within endto-end models that map language directly to control signals [45, 55, 27]. Although differing in formulation, these methods share a common characteristic: behavior is determined largely upfront, with limited or no support for revising commands during execution. This limits their applicability to real-world humanoid control, where interaction is continuous and intent may evolve over time. 

Separately, the humanoid animation community has explored interactive motion generation techniques that allow users to steer motions on the fly [8, 47, 71, 56, 7]. A key characteristic is that both the conditioning signal and the generated motion are treated as time-varying signal streams, rather than producing a complete trajectory from a static prompt. These approaches show the feasibility of responsive, user-in-the-loop motion synthesis, but are primarily developed for kinematic animation and virtual characters, without integration into realrobot whole-body control pipelines, due to missing dynamic constraints and the unaddressed sim-to-real gap. 

Taken together, these observations reveal a missing link between interactive language-based intent expression and realtime, physically executable humanoid control. Based on this 

insight, we propose **TextOp** , a real-time text-driven humanoid motion generation and control framework that drives a universal whole-body controller using streaming language commands with on-the-fly instruction modification. Rather than committing to a fixed motion plan, **TextOp** continuously interprets evolving text input and generates short-horizon motion references suitable for immediate execution on real hardware. 

**TextOp** adopts a two-level architecture. At the high level, an autoregressive, text-conditioned motion diffusion model incrementally generates short-horizon kinematic trajectories conditioned on the current language input and recent motion context. At the low level, a robust whole-body motion tracking policy executes these trajectories on a physical humanoid robot, converting kinematic references into joint-level commands at high frequency. This separation allows human intent to be updated flexibly without compromising control stability. 

To effectively integrate interactive motion generation with real-world humanoid control, **TextOp** incorporates two critical design choices tailored to robotic execution. First, we adopt a robot-skeleton motion representation that reflects the constrained, single-DoF joint structure of humanoid robots, enabling compact and effective kinematic motion representation for the motion generation module. Second, to mitigate the distribution gap between motion datasets and the reference motions produced online by the generator, we augment the training data of the tracking policy with generator-produced motions under realistic text streams. Together, these designs align the high-level generator with the low-level controller and improve robustness during real-robot deployment. 

By bridging interactive motion generation with whole-body control, **TextOp** enables the robot to execute long-horizon, continuous motions that smoothly transition across multiple challenging behaviors—such as dancing and jumping—while dynamically responding to user-provided language commands in real time, as validated on a real robot. Offline evaluations further demonstrate that carefully designed robot-skeleton motion representations, together with augmenting tracker training with generator-produced motions, enable the system to reliably translate streaming language commands into real-world robot motion. 

In summary, this work makes the following contributions: 

- We present **TextOp** , a real-time text-driven humanoid motion generation and control system that realizes a novel control mode in which the robot is driven by streaming natural language commands. 

- We introduce two key design choices: (i) a robot-skeleton motion representation to improve generation quality for robot structure, and (ii) a data-augmentation strategy via motion generation to reduce the distribution gap between motion datasets and generator-produced reference motions. 

- We validate **TextOp** through extensive real-robot experiments and offline evaluations, demonstrating instant responsiveness, smooth whole-body motion, and precise control. 


Fig. 2: **Overview of TextOp’s framework.** The framework consists of three main parts: (a) **Interactive Motion Generation** , including VAE training and LDM training, which together model future reference motion sequences conditioned on history motion and text prompt in an autoregressive style; (b) **Dynamic Motion Tracking** , where the MLP-based policy _π_ takes reference motions and robot states to generate joint actions, trained in the simulation for stable execution; (c) **Deployment** , where the real-time user text prompt is converted into motions by the generator, translated into actions by the tracking policy based on the robot state, and executed on the physical robot. 

## II. RELATED WORK 

## _A. Whole-body Humanoid Control_ 

Humanoid whole-body control has advanced significantly, enabling realistic, diverse, and coordinated motion execution on physical robots. From the perspective of the driving mechanism, humanoid robot controllers are mainly driven by three command paradigms. 

**Simple Task Command** encompasses control methods that enable the robot to execute straightforward high-level objectives, such as locomotion [14, 13, 73, 52, 61, 57], navigation [5, 6, 10], object manipulation [20, 59], sports [48, 16, 42], and standing up [23, 21]. This paradigm often provides fast response and reliability for single tasks, but it offers limited expressiveness for complex, semantically rich motions. 

**Static motion tracking** relies on predefined reference trajectories to achieve agile and high-fidelity whole-body motion reproduction, but commits to a fixed motion plan that is difficult to adjust in real time. This paradigm leverages motion data from motion capture [33, 24], video-based extraction [1, 46, 54], and multimodal generation models in both explicit [18, 44] and implicit [45, 55, 27, 60] ways, together with motion retargeting [2, 62] and reinforcement learning methods [28, 32, 58, 17, 70, 18, 12, 38, 64, 9, 74] for whole-body motion tracking. We note that a few prior methods [45, 32] technically allow modifying text inputs at runtime; however, this capability is not a design focus and is only weakly supported in practice, with no systematic empirical validation. 

**Teleoperation** provides flexible real-time control through motion capture suits [65], VR devices [66, 30], camera-based systems [19], or exoskeletons [35, 63, 4], but requires continuous human involvement, limiting autonomy and scalability for long-term operation. 

This work goes beyond both static motion tracking and teleoperation paradigms, achieving flexible semantic intent expression and continuous real-time control with little reliance on manual labor. 

## _B. Interactive Motion Generation_ 

Text-driven motion generation has advanced significantly, with natural language emerging as a powerful modality for describing complex, semantically rich motions. Diffusionbased approaches [68, 49, 11], followed by language-modelintegrated methods [67, 25, 53, 72], have demonstrated that compact textual descriptions can be effectively translated into diverse and high-quality human motions. Nevertheless, most existing motion generation systems remain offline, producing complete motion sequences from static inputs. 

Interactive motion generation has been proposed to address this limitation. Early approaches enable interactive control using low-dimensional signals such as target position and direction [8, 47], while later work incorporate text as control signals. [71] introduces a diffusion-based autoregressive motion primitive model that conditions on historical frames and text prompts for real-time generation. [69] uses a two-stage method that first pretrain an autoregressive diffusion model to capture short-term body movements and then adapts it for 


Fig. 3: **Illustration of the time-aligned data format including text labels, SMPL motions, and robot motions.** 

real-time interactive control. [56] performs continuous causal latent autoregression, alleviating error accumulation caused by discrete tokenization. [7] proposes a diffusion-forcing framework with tailored temporal attention and scheduling to enable seamless real-time synthesis. 

Despite these advances, existing methods focus on virtual character animation and lack physical robot deployment. Our work bridges this gap by integrating autoregressive motion generation with a whole-body tracking policy for real humanoid control. 

## III. METHOD 

## _A. Overview_ 

We consider a humanoid robot operating in a real-time streaming control setting. At each discrete time step _t_ , the system receives a language command _lt_ together with the previous robot state _x_<sup>robot</sup> _<t_<sup>. The goal of the system is to generate</sup> a control signal, i.e., target joint commands _at_ , such that the resulting physical robot behavior _x_<sup>robot</sup> _t_ remains semantically consistent with the language command while maintaining stable and smooth whole-body motion. 

**TextOp** decomposes this task into two levels: Interactive Motion Generation and Dynamic Motion Tracking. Specifically, the high-level motion generator _G_ is implemented as an autoregressive motion latent diffusion model. At each time step, it produces a reference motion sequence _x_<sup>ref</sup> _t_ : _t_ + _T_ future _−_ 1<sup>of</sup> length _T_ future = 8, conditioned on the past _T_ history = 2 frames of reference motion _x_<sup>ref</sup> _t−T_ history: _t−_ 1<sup>andthecurrentlanguage</sup> command _lt_ , i.e., 


The low-level tracking policy _π_ then converts the kinematic reference motion into executable control signals based on the previous robot states, i.e., 


ensuring that the executed motion closely follows the reference trajectory while remaining stable and smooth. 

## _B. Data Preparation_ 

Our training data is built on the large-scale public motion capture dataset AMASS [33], supplemented with a small amount of private motion data featuring complex dance and martial arts motions. All motions are retargeted from the SMPL [29] skeleton to the robot skeleton using GMR [2], extracting the feet contact indicator and resampling to a unified frequency of 50 Hz. We further filter the retargeted motions by pretraining a universal motion tracking policy with privileged information and discarding motion sequences that cannot be reliably tracked. Fig. 3 illustrates our data format across different modalities. 

For training the motion tracking policy, the filtered motions are further segmented into short clips of less than 40 seconds, resulting in a total of 12,296 motion clips with an aggregate duration of 40.67 hours from AMASS. The private dataset contributes an additional 403 clips totalling 3.12 hours. 

For motion generation, we pair filtered AMASS motions with language annotations from BABEL [40], an action-centric dataset in which long motion sequences are segmented, each annotated with a text description, e.g., “walk”, “jump”. Such frame-level annotations are essential for effective language guidance and natural switching during generation, as demonstrated in prior work [71, 7]. We perform mirror augmentation on both the motion sequences and their corresponding textual descriptions, resulting in a dataset of 83,478 segment–text pairs. For complex long-horizon motions in the private dataset, the entire motion is assigned a unique label wrapped with “ _⟨·⟩_ ” markers. 

## _C. Interactive Motion Generation_ 

**Robot-Skeleton Motion Representation.** In contrast to humanoid skeletons like SMPL, where joints are modeled as 3-DoF ball joints to represent full human articulation, robotic skeletons typically employ single-DoF rotational joints, yielding more constrained yet tractable kinematics. Therefore, we propose a DoF-based local incremental motion representation for the robot skeleton, instead of HumanML3D [15]-style representation. This choice naturally enforces robot kinematic constraints and ensures invariance to global pose, providing a compact yet sufficient feature space for the motion generator. For a robot with _nq_ degrees of freedom, we define the perframe motion feature _ft ∈_ R<sup>_d_feat</sup> as: 


where _rt_ = (roll _t,_ pitch _t,_ yaw _t_ ) denotes the root orientation in intrinsic Euler angles and _ϕ_ ( _rt_ ) = [sin(roll _t_ ) _,_ cos(roll _t_ ) _−_ 1 _,_ sin(pitch _t_ ) _,_ cos(pitch _t_ ) _−_ 1] is a continuous trigonometric encoding of roll and pitch. ∆ _ψt_ = yaw _t_ +1 _−_ yaw _t_ denotes the incremental change of the root yaw, _ct ∈ {_ 0 _,_ 1 _}_<sup>_nc_</sup> = represents binary contact indicators of feet, and ∆ _p_<sup>local</sup> _t Rz_ (yaw _t_ )<sup>_⊤_</sup> ( _pt_ +1 _− pt_ ) is the root translation increment expressed in a yaw-aligned local frame. Furthermore, _ht_ denotes the root height, _qt ∈_ R<sup>_nq_</sup> the joint positions, and ∆ _qt_ = _qt_ +1 _− qt_ the corresponding joint-wise increments. 

**Model Architecture.** The motion generator _G_ models the text-conditional probabilistic distribution of the robot motion in an autoregressive style. It follows the DART [71] architecture and is implemented as a VAE combined with a latent diffusion model (LDM), both are Transformer-based networks. The VAE defines a motion latent space by encoding future motion frames into a latent variable conditioned on the motion history, _z ∼ Eϕ_ ( _· | ft−T_ history: _t_ + _T_ future _−_ 1), which can be decoded to reconstruct the future frames _f_<sup>ˆ</sup> _t_ : _t_ + _T_ future _−_ 1 = _Dϕ_ ( _ft−T_ history: _t−_ 1 _, z_ ). The LDM models the text-conditional distribution of future motion latents, where language commands are embedded using a pretrained CLIP encoder [41] as _et_ = CLIP( _lt_ ), and a diffusion transformer predicts clean latents from noise via _z_ ˆ = _Fθ_ ( _zk, k, ft−T_ history: _t−_ 1 _, et_ ), trained in a DDPM [22] style with _n_ denoise = 5 steps. During inference, classifier-free guidance is applied with scale _σ_ CFG = 5 to enhance semantic alignment. 

**Training Process.** The VAE is first trained on motion features reconstruction, and its parameters are fixed during subsequent LDM training. The LDM is then trained to denoise motion latents by minimizing a combination of feature reconstruction, latent reconstruction, and geometric losses. To reduce the distribution gap between training and deployment, a self-rollout strategy is adopted, where _N_ consecutive overlapping motion segments are processed sequentially and the history of each segment is randomly replaced by the predicted future of the previous segment. For classifier-free guidance, the text embedding is randomly set to zero during training. 

## _D. Dynamic Motion Tracking_ 

**Training Universal Motion Tracker.** The low-level universal motion tracker is trained through goal-conditioned RL in large-scale physical simulation with IsaacLab [34]. We adopt a one-stage RL pipeline to train the MLP-based tracking policy, discarding more complex training pipelines and network designs to maintain simplicity while ensuring balanced performance. 

The policy takes as input the robot’s proprioceptive state together with a reference motion over _T_ ref = 5 future frames. During training, an episode starts with a motion segment randomly sampled from the dataset and the robot initialized to the state of the first frame, and ends upon timeout or large tracking deviations. The policy is optimized via PPO [43] with a reward signal that combines tracking objectives and regularization terms. The training setup, including observation structure, reward formulation, and domain randomization, mainly follows established methods such as BeyondMimic [28] and is detailed in the appendix. 

**Data Augmentation via Motion Generation.** To reduce the distribution gap between motion datasets and the reference motions induced by the high-level generator, we augment the training data with generated motions. Specifically, we randomly sample text annotations from the BABEL training set to form 20-second text streams and feed them into the high-level generator, producing 5,368 motion clips totalling 31.48 hours. This approach exposes the policy to realistic 

variability and noise from generator outputs, enhancing its tracking performance during deployment. 

## _E. Deployment_ 

The system is deployed on a Unitree G1 humanoid robot [51] with 29 degrees of freedom. The motion tracking policy executes on the robot’s onboard computer at 50 Hz using ONNX Runtime [37], while the motion generator runs at 6.25 Hz on an external workstation equipped with an NVIDIA RTX 4090 GPU using TensorRT [36]. Communication between the two components occurs over a wired or wireless network, with a motion buffer to synchronize their execution. User textual commands are streamed to the external workstation in real time, encoded via CLIP, and incorporated into subsequent motion generation, enabling interactive control. 

## IV. EXPERIMENTS 

We assess the effectiveness of **TextOp** through a combination of real-world deployment and large-scale simulation studies. Our experiments are designed to evaluate both the practical performance of the system and the contributions of its key components. 

Specifically, the evaluation aims to answer the following research questions: 

- **Q1:** Can **TextOp** achieve precise, stable, and responsive whole-body behaviors in the real world? 

- **Q2:** Can the motion generator produce high-quality and semantically consistent motions from text commands in an interactive setting? 

- **Q3:** Can the motion tracking policy robustly execute diverse reference motions, especially those produced by the generator? 

## _A. Experimental Setup_ 

To systematically evaluate **TextOp** system, we adopt a comprehensive set of evaluation metrics covering **Motion Quality** and **Tracking Fidelity** . Formal definitions of these metrics are provided in the appendix, and different system components are evaluated using the corresponding subsets of these metrics. 

- **Motion Quality.** Evaluates the overall quality of textconditioned motion following prior work [71, 7], measured by FID and Diversity for distribution similarity to the dataset, R-precision (R@K) and multimodal distance (MM-Dist) for semantic alignment with language commands, and PJ and AUJ for temporal smoothness across command transitions. 

- **Tracking Fidelity.** Evaluates tracking fidelity of the motion tracker under physical constraints by reporting the success rate (Succ) and motion discrepancy metrics between executed and reference trajectories, including global MPJPE ( _E_ g-mpjpe, mm), root-relative MPJPE ( _E_ mpjpe, mm), acceleration error ( _E_ acc, mm/frame<sup>2</sup> ), and velocity error ( _E_ vel, mm/frame), following [31, 32]. 

For real-world deployment, the motion tracking policy is trained on a server equipped with an NVIDIA A100 GPU for 


Fig. 4: **Continuous diverse skill execution in the real robot.** The robot seamlessly performs a wide range of tasks, including multiple dance styles, dynamic jumping behaviors, instrument-playing motions, and expressive gestures. For complex longhorizon motions in the private dataset, the entire motion is assigned a unique label wrapped with “ _⟨·⟩_ ” markers. 

approximately one week, using 150,000 training steps, while for simulation studies, the policy is trained for 50,000 steps due to computational resource constraints. The motion generation model is trained on the same hardware for approximately two days, with 200,000 steps for the VAE and 300,000 steps for the LDM. The hyperparameter setup is detailed in the appendix. 

## _B. Real-world Deployment_ 

To address **Q1** , we evaluate **TextOp** in the real world through a combination of qualitative demonstrations, quantitative robustness tests, and real-time performance measurements. **Complex Skill Demonstrations and Interactive Control.** We evaluate the expressiveness and robustness of **TextOp** system through a series of real-world demonstrations performed on the physical robot, as shown in Fig. 1 and Fig. 4. The robot executes a diverse set of skills, including locomotion, dance motions, martial arts sequences, and gestures. Beyond isolated skill execution, a distinctive feature of **TextOp** is its ability to perform continuous long-horizon tasks: the robot seamlessly executes a sequence of varied commands in a single, unbroken trial. This “one-take” demonstration underscores the system’s capacity to maintain motion coherence and control stability. Throughout the entire process, the interactive control capability of **TextOp** allows users to modify commands on the fly, guiding the robot’s behavior and enabling smooth composition 

and transitions between skills. 

TABLE I: **Quantitative evaluation on 30-second longhorizon real-robot executions with diverse text command streams. TextOp** achieves a strong tracking fidelity across all evaluated tasks. 

|Text Command|Succ _↑_|_E_g-mpjpe _↓_|_E_mpjpe _↓_|_E_acc _↓_|_E_vel _↓_|
|---|---|---|---|---|---|
|Random|16 / 20|337.169|153.920|1.452|2.621|
|**Looping**||||||
|“punch”|10 / 10|355.560|123.598|2.705|4.891|
|“wave right hand”|8 / 10|316.480|72.184|2.757|2.906|
|“strum guitar with left hand”|10 / 10|191.562|88.662|1.418|1.974|
|“play the violin”|10 / 10|107.584|33.941|0.518|0.750|


**Robustness Analysis.** We evaluate the system’s robustness through long-horizon real-robot experiments under varying text command streams. In each 30-s trial, the robot executes either randomly sampled commands or fixed loopable instructions, such as waving or punching. As shown in Table I, **TextOp** maintains high success rates and tracking accuracy across both settings. Robustness to disturbances is further demonstrated by manually perturbing the robot during execution, where it recovers gracefully while preserving ongoing motions, as illustrated in Fig. 5. These experiments collectively show that the system as a whole exhibits stable and reliable performance. 

**Real-Time Performance.** We evaluate the real-time per- 


Fig. 5: **Real-time recovery under external perturbations.** The robot dynamically adjusts its actions based on perturbed states to preserve stability and fulfill text-driven commands. 

formance of the system to assess its interactive capabilities. Latency is measured at key stages, from language command input to motion generation and low-level tracking. As summarized in Table II, the system exhibits fast and consistent response across all stages. In particular, the user interaction latency, defined as the time from typing a new command to the robot’s physical response, is 0 _._ 73 s in average, which is sufficiently low to support responsive real-time interaction. 

TABLE II: **Real-time performance of different stages in TextOp.** 

|**Stage**|**Latency**|
|---|---|
|Text encoding|7.64_±_2.56ms|
|Motion generator|29.63_±_3.56ms|
|Tracking policy|2.15_±_0.11ms|
|User Interaction|0.73_±_0.10s|


## _C. Offline Evaluation_ 

To quantitatively evaluate the components of **TextOp** , we conduct offline evaluations, isolating the contributions of the motion generator and the motion tracking policy. All models in these experiments are trained based on public datasets to facilitate reproducibility. 

_1) Motion Generation Evaluation:_ To answer **Q2** , we evaluate the motion generator independently, focusing on the effectiveness of the proposed robot-skeleton motion representation. 

**Baselines:** We compare the generator based on our proposed representation against several established baselines: 

- **DART+Retarget** : Uses the DART [71] model trained on the SMPL human skeleton, with the generated human motions subsequently retargeted to the robot skeleton via GMR [2]. 

- **BeyondMimic** [28] Diffusion State: Replicates the state representation of BeyondMimic, which comprises root position, root linear velocity, root rotation, and root angular velocity relative to the initial character-yaw frame, 

along with local body positions and velocities relative to each character-yaw frame. 

- **HumanML3D** -style Representation [15]: Adapts the HumanML3D human-motion representation for the robot, including root angular velocity along the Z-axis, root linear velocity in the XY-plane, root height and rotation, body positions and velocities relative to the root, joint angles, and foot contact states. Global invariance processing is applied to enable autoregressive motion generation. 

- **RobotMDM** [44]: Reproduces the motion representation proposed in RobotMDM, including root height, root linear velocity in the XY-plane, root angular velocity along the Z-axis, root rotation, and joint angles and velocities. Global invariance processing is applied to facilitate autoregressive generation. 

**Experimental Setup:** Following DART [71], we evaluate text-conditioned motion generation on the BABEL validation set [40]. Text streams are extracted from the dataset and used as conditions to generate rollout trajectories. Evaluation focuses on two aspects: (i) the complete motion segments corresponding to each text command, and (ii) the transitions between consecutive segments. 

**Results:** Table III summarizes the evaluation results. Our proposed motion representation achieves state-of-the-art performance both in generating motions for individual text commands and in maintaining high-quality transitions between consecutive segments. The observed improvements over alternative representations can be attributed to two key design elements: First, the compact DoF-based motion representation reduces the inherent modeling complexity relative to HumanML3D-style representations. Second, our carefully designed incremental root-state representation improves data efficiency compared with RobotMDM and BeyondMimic. In terms of transition smoothness, our approach is slightly below the DART+Retarget baseline, as the retargeting step introduces smoothness in joint displacements. 

_2) Motion Tracking Evaluation:_ To address **Q3** , we evaluate the ability of the motion tracking policy to robustly execute diverse reference motions, with a particular focus on trajectories produced by the motion generator. This evaluation also examines the effect of augmenting the training data with generated motions on tracking robustness and generalization. 

**Baselines and Ablations:** We consider the following configurations: 

- **TextOp-M+G (Ours):** Tracker trained on the combined dataset of motion capture and generated motions. 

- **TextOp-G (Ours):** Tracker trained exclusively on generator-produced motions. 

- **TextOp-M:** Tracker trained exclusively on motion capture data. 

- Pretrained general motion tracker policies from prior work: **GMT** [12], **Any2Track** [70], **TWIST2** [66]. These models are trained on different datasets and simulation platforms; for fair comparison, we adopt the officially released pretrained checkpoints. 

TABLE III: **Comparison of motion generation with different motion representations.** Our method achieves the best overall performance across most segment- and transition-level metrics. Rightarrow “ _→_ ” denotes that closer alignment with the dataset reference is better. Bold and underlined values indicate the best and second-best results, respectively, excluding the dataset. All results are reported as mean _±_ standard deviation over three generator rollout seeds. 

|**Method**|||**Segm**|**ent**||||**Trans**|**ition**||
|---|---|---|---|---|---|---|---|---|---|---|
||FID _↓_|Diversity _→_|R@1 _↑_|R@2 _↑_|R@3 _↑_|MM-dist _↓_|FID _↓_|Diversity _→_|PJ _→_|AUJ _↓_|
|Dataset|0.000 _±_0.000|9.150 _±_0.158|0.357 _±_0.004|0.556 _±_0.006|0.684 _±_0.005|3.729 _±_0.000|0.000 _±_0.000|8.138 _±_0.013|0.005 _±_0.000|0.000 _±_0.000|
|DART+Retarget<br>BeyondMimic<br>HumanML3D<br>RobotMDM|4.837<br>_±_0.070<br>20.550 _±_0.089<br>6.599 _±_0.031<br>5.134 _±_0.131|8.012 _±_0.082<br>5.930 _±_0.146<br>8.236<br>_±_0.046<br>8.210 _±_0.082|0.230 _±_0.007<br>0.134 _±_0.009<br>0.197 _±_0.005<br>0.262<br>_±_0.006|0.372 _±_0.020<br>0.231 _±_0.006<br>0.344 _±_0.005<br>0.427<br>_±_0.004|0.486 _±_0.018<br>0.320 _±_0.013<br>0.453 _±_0.003<br>0.556<br>_±_0.010|5.746 _±_0.026<br>7.578 _±_0.014<br>6.292 _±_0.023<br>5.076<br>_±_0.031|5.249<br>_±_0.245<br>41.414 _±_0.339<br>9.310 _±_0.076<br>6.514 _±_0.178|7.939<br>_±_0.023<br>4.209 _±_0.045<br>7.676 _±_0.178<br>7.602 _±_0.095|**0.007** _±_0.000<br>0.077 _±_0.003<br>0.134 _±_0.014<br>0.032 _±_0.001|**0.123** _±_0.000<br>0.231 _±_0.007<br>0.340 _±_0.019<br>0.150 _±_0.001|
|**TextOp**|**3.072** _±_0.199|**9.220** _±_0.151|**0.300** _±_0.007|**0.481** _±_0.004|**0.607** _±_0.008|**4.272** _±_0.058|**3.238** _±_0.430|**8.226** _±_0.079|0.015<br>_±_0.001|0.125<br>_±_0.001|


TABLE IV: **Simulation evaluation of the motion tracker on generator-produced motion data.** Incorporating generatorproduced motions during training leads to improved performance across both tracking and semantic metrics. Rightarrow “ _→_ ” denotes that closer alignment with the dataset reference is better. Bold and underlined values indicate the best and second-best results, respectively, excluding the dataset. All results are reported as mean _±_ standard deviation over three generator rollout seeds. 

|**Method**||**Tr**|**acking Fidelity**|||||**Motion **|**Quality**|||
|---|---|---|---|---|---|---|---|---|---|---|---|
||Succ _↑_|_E_g-mpjpe _↓_|_E_mpjpe _↓_|_E_acc _↓_|_E_vel _↓_|FID _↓_|Diversity _→_|R@1 _↑_|R@2 _↑_|R@3 _↑_|MM-dist _↓_|
|Dataset|–|–|–|–|–|0.000_±_0.000|9.150_±_0.158|0.357_±_0.004|0.556_±_0.006|0.684_±_0.005|3.729_±_0.000|
|**TextOp**-M+G (Ours)<br>**TextOp**-G (Ours)<br>**TextOp**-M|**0.993** _±_0.003<br>0.991 _±_0.002<br>0.992<br>_±_0.005|**113.552** _±_1.996<br>121.690<br>_±_5.950<br>130.532 _±_14.267|34.665 _±_0.543<br>34.570<br>_±_0.747<br>**34.526** _±_1.050|1.906<br>_±_0.014<br>**1.857** _±_0.015<br>1.935 _±_0.007|4.872<br>_±_0.024<br>**4.786** _±_0.021<br>4.979 _±_0.009|3.454<br>_±_0.225<br>**3.371** _±_0.145<br>3.615 _±_0.175|8.386<br>_±_0.113<br>**8.409** _±_0.100<br>8.381 _±_0.101|0.273 _±_0.005<br>**0.281** _±_0.006<br>0.281<br>_±_0.004|0.453<br>_±_0.002<br>**0.464** _±_0.004<br>0.452 _±_0.007|0.574 _±_0.007<br>**0.577** _±_0.001<br>0.575<br>_±_0.006|4.645<br>_±_0.020<br>**4.642** _±_0.034<br>4.648 _±_0.033|
|TWIST2<br>GMT<br>Any2Track|0.922 _±_0.011<br>0.834 _±_0.018<br>0.714 _±_0.016|847.203 _±_34.405<br>1252.235 _±_35.132<br>1489.394 _±_51.433|58.529 _±_1.659<br>103.138 _±_1.046<br>139.178 _±_1.502|1.999 _±_0.018<br>1.934 _±_0.021<br>2.425 _±_0.019|7.439 _±_0.081<br>8.776 _±_0.085<br>11.476 _±_0.171|4.092 _±_0.094<br>5.142 _±_0.432<br>6.135 _±_0.215|8.187 _±_0.087<br>8.010 _±_0.040<br>7.719 _±_0.013|0.255 _±_0.007<br>0.240 _±_0.012<br>0.222 _±_0.003|0.420 _±_0.005<br>0.397 _±_0.014<br>0.367 _±_0.009|0.543 _±_0.002<br>0.503 _±_0.016<br>0.473 _±_0.006|5.137 _±_0.058<br>5.441 _±_0.125<br>5.876 _±_0.036|


**Experimental Setup:** All evaluations are conducted in the MuJoCo simulator in a Sim2Sim setting. Reference trajectories are drawn from two sources: (i) **Generator-produced motion:** motions synthesized by our generator, conditioned on text streams the same as Sec. IV-C1, to approximate the deploytime distribution; and (ii) **SnapMoGen** [24], a publicly available motion capture dataset, which is unseen to all baselines, to evaluate generalization. Only the test split of SnapMoGen is used for evaluation. 

TABLE V: **Simulation evaluation of the motion tracker on SnapMoGen data.** Exclusive training on generated motions shows reduced generalization, whereas training on both motion capture and generated data offers a better trade-off between deployment performance and generalization. Bold and underlined values indicate the best and second-best results, respectively. 

|Method|Succ _↑_|_E_g-mpjpe _↓_|_E_mpjpe _↓_|_E_acc _↓_|_E_vel _↓_|
|---|---|---|---|---|---|
|**TextOp**-M+G (Ours)|0.814|394.705|79.057|**0.892**|**3.859**|
|**TextOp**-G (Ours)|0.772|565.374|87.755|0.928|4.310|
|**TextOp**-M|**0.823**|**340.145**|**74.761**|0.960|4.020|
|TWIST2|0.634|1019.826|131.292|1.008|4.629|
|GMT|0.542|1095.242|150.067|0.968|4.806|
|Any2Track|0.374|1674.080|203.293|1.253|6.226|


**Results:** Tables IV and V summarize the motion tracking performance on generator-produced trajectories and unseen motion capture data, respectively. On generator-produced motion data, all variants of **TextOp** achieve consistently high success rates and low tracking errors, indicating stable execu- 

tion under text-conditioned reference motions. Among them, **TextOp** -G performs best overall, while **TextOp** -M+G also improves upon **TextOp** -M across several tracking fidelity and motion quality metrics, suggesting that incorporating generator-produced motions into training is beneficial for aligning the tracker with the deployment-time motion distribution. 

On the unseen SnapMoGen dataset, **TextOp** -M achieves the strongest generalization performance, whereas **TextOp** - G exhibits a noticeable performance drop, indicating limited robustness when evaluated beyond the generator’s motion distribution. The combined model, **TextOp** -M+G, maintains competitive performance across both settings, balancing robustness on generator-produced trajectories and generalization to unseen motion capture data. These results reflect a trade-off between deployment-oriented robustness and generalization, motivating the use of mixed motion capture and generated data as a practical training strategy. 

## V. CONCLUSION 

**TextOp** represents a new control paradigm for humanoid robots, where natural language serves as a continuously revisable control signal rather than a one-shot task specification. This paradigm is realized by combining a high-level motion generator with a low-level universal motion tracker, enabling smooth, whole-body motions that respond instantaneously to language commands. Real-world experiments on the Unitree G1 robot demonstrate the system’s ability to execute behaviors ranging from simple gestures to complex skills with high fidelity, robustness, and responsiveness. Offline evaluations 

further indicate that carefully designed robot-skeleton motion features improve the quality of generated motions, and incorporating generator-produced motions into the training data effectively aligns the motion tracker with the generator. 

Despite these strengths, **TextOp** currently lacks explicit environment perception and interactive physical reasoning. Consequently, the robot cannot adapt its motions to obstacles, objects, or dynamic changes in its surroundings. Overcoming this limitation by integrating environment-aware sensing and interactive planning would enable the robot to respond flexibly to dynamic real-world scenarios. Furthermore, combining such capabilities with high-level reasoning in language models into an agent system could provide a solid foundation for autonomous, instruction-driven behavior, paving the way toward fully autonomous, general-purpose humanoid robots. 

## ACKNOWLEDGMENTS 

We are grateful to Zehao Yu, Yiran Wang, Xingyi Wang, and Lei Kuang for their assistance with the real-robot experiments, and to Yiyi Cai, Yang Tang, and Yixuan Pan for their insightful discussions during the preparation of this paper. 

This work was supported by the National Natural Science Foundation of China (Grant No. 62306242), the Young Elite Scientists Sponsorship Program by CAST (Grant No. 2024QNRC001), and the Yangfan Project of Shanghai (Grant No. 23YF11462200). The SJTU team was partially supported by the National Natural Science Foundation of China (Grant No. 62322603). 

## REFERENCES 

- [1] Arthur Allshire, Hongsuk Choi, Junyi Zhang, David McAllister, Anthony Zhang, Chung Min Kim, Trevor Darrell, Pieter Abbeel, Jitendra Malik, and Angjoo Kanazawa. Visual imitation enables contextual humanoid control. _arXiv preprint arXiv:2505.03729_ , 2025. 

- [2] Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, and C Karen Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- [3] Andrew G Barto. Reinforcement learning: An introduction. by richard’s sutton. _SIAM Rev_ , 6(2):423, 2021. 

- [4] Qingwei Ben, Feiyu Jia, Jia Zeng, Junting Dong, Dahua Lin, and Jiangmiao Pang. Homie: Humanoid locomanipulation with isomorphic exoskeleton cockpit. _arXiv preprint arXiv:2502.13013_ , 2025. 

- [5] Qingwei Ben, Botian Xu, Kailin Li, Feiyu Jia, Wentao Zhang, Jingping Wang, Jingbo Wang, Dahua Lin, and Jiangmiao Pang. Gallant: Voxel grid-based humanoid locomotion and local-navigation across 3d constrained terrains. _arXiv preprint arXiv:2511.14625_ , 2025. 

- [6] Wenzhe Cai, Jiaqi Peng, Yuqiang Yang, Yujian Zhang, Meng Wei, Hanqing Wang, Yilun Chen, Tai Wang, and Jiangmiao Pang. Navdp: Learning sim-to-real navigation diffusion policy with privileged information guidance, 2025. URL https://arxiv.org/abs/2505.08712. 

- [7] Yiyi Cai, Yuhan Wu, Kunhang Li, You Zhou, Bo Zheng, and Haiyang Liu. Flooddiffusion: Tailored diffusion forcing for streaming motion generation. _arXiv preprint arXiv:2512.03520_ , 2025. 

- [8] Rui Chen, Mingyi Shi, Shaoli Huang, Ping Tan, Taku Komura, and Xuelin Chen. Taming diffusion probabilistic models for character control. In _ACM SIGGRAPH 2024 Conference Papers_ , pages 1–10, 2024. 

- [9] Sirui Chen, Zi-ang Cao, Zhengyi Luo, Fernando Casta˜neda, Chenran Li, Tingwu Wang, Ye Yuan, Linxi Fan, C Karen Liu, Yuke Zhu, et al. Chip: Adaptive compliance for humanoid control through hindsight perturbation. _arXiv preprint arXiv:2512.14689_ , 2025. 

- [10] Sirui Chen, Yufei Ye, Zi-Ang Cao, Jennifer Lew, Pei Xu, and C. Karen Liu. Hand-eye autonomous delivery: Learning humanoid navigation, locomotion and reaching, 2025. URL https://arxiv.org/abs/2508.03068. 

- [11] Xin Chen, Biao Jiang, Wen Liu, Zilong Huang, Bin Fu, Tao Chen, and Gang Yu. Executing your commands via motion diffusion in latent space. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 18000–18010, 2023. 

- [12] Zixuan Chen, Mazeyu Ji, Xuxin Cheng, Xuanbin Peng, Xue Bin Peng, and Xiaolong Wang. Gmt: General motion tracking for humanoid whole-body control. _arXiv preprint arXiv:2506.14770_ , 2025. 

- [13] Alejandro Escontrela, Justin Kerr, Arthur Allshire, Jonas Frey, Rocky Duan, Carmelo Sferrazza, and Pieter Abbeel. Gaussgym: An open-source real-to-sim framework for learning locomotion from pixels, 2025. URL https: //arxiv.org/abs/2510.15352. 

- [14] Xinyang Gu, Yen-Jen Wang, and Jianyu Chen. Humanoid-gym: Reinforcement learning for humanoid robot with zero-shot sim2real transfer. _arXiv preprint arXiv:2404.05695_ , 2024. 

- [15] Chuan Guo, Shihao Zou, Xinxin Zuo, Sen Wang, Wei Ji, Xingyu Li, and Li Cheng. Generating diverse and natural 3d human motions from text. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 5152–5161, June 2022. 

- [16] Tuomas Haarnoja, Ben Moran, Guy Lever, Sandy H Huang, Dhruva Tirumala, Jan Humplik, Markus Wulfmeier, Saran Tunyasuvunakool, Noah Y Siegel, Roland Hafner, et al. Learning agile soccer skills for a bipedal robot with deep reinforcement learning. _Science Robotics_ , 9(89):eadi8022, 2024. 

- [17] Jinrui Han, Weiji Xie, Jiakun Zheng, Jiyuan Shi, Weinan Zhang, Ting Xiao, and Chenjia Bai. Kungfubot2: Learning versatile motion skills for humanoid whole-body control. _arXiv preprint arXiv:2509.16638_ , 2025. 

- [18] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024. 

- [19] Tairan He, Zhengyi Luo, Wenli Xiao, Chong Zhang, Kris 

Kitani, Changliu Liu, and Guanya Shi. Learning humanto-humanoid real-time whole-body teleoperation. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 8944–8951. IEEE, 2024. 

- [20] Tairan He, Zi Wang, Haoru Xue, Qingwei Ben, Zhengyi Luo, Wenli Xiao, Ye Yuan, Xingye Da, Fernando Casta˜neda, Shankar Sastry, et al. Viral: Visual sim-to-real at scale for humanoid loco-manipulation. _arXiv preprint arXiv:2511.15200_ , 2025. 

- [21] Xialin He, Runpei Dong, Zixuan Chen, and Saurabh Gupta. Learning getting-up policies for real-world humanoid robots. _arXiv preprint arXiv:2502.12152_ , 2025. 

- [22] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. _Advances in neural information processing systems_ , 33:6840–6851, 2020. 

- [23] Tao Huang, Junli Ren, Huayi Wang, Zirui Wang, Qingwei Ben, Muning Wen, Xiao Chen, Jianan Li, and Jiangmiao Pang. Learning humanoid standingup control across diverse postures. _arXiv preprint arXiv:2502.08378_ , 2025. 

- [24] Inwoo Hwang, Jian Wang, Bing Zhou, et al. Snapmogen: Human motion generation from expressive texts. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 

- [25] Biao Jiang, Xin Chen, Wen Liu, Jingyi Yu, Gang Yu, and Tao Chen. Motiongpt: Human motion as a foreign language. _Advances in Neural Information Processing Systems_ , 36:20067–20079, 2023. 

- [26] Yitang Li, Zhengyi Luo, Tonghe Zhang, Cunxi Dai, Anssi Kanervisto, Andrea Tirinzoni, Haoyang Weng, Kris Kitani, Mateusz Guzek, Ahmed Touati, et al. Bfmzero: A promptable behavioral foundation model for humanoid control using unsupervised reinforcement learning. _arXiv preprint arXiv:2511.04131_ , 2025. 

- [27] Zhe Li, Cheng Chi, Yangyang Wei, Boan Zhu, Yibo Peng, Tao Huang, Pengwei Wang, Zhongyuan Wang, Shanghang Zhang, and Chang Xu. From language to locomotion: Retargeting-free humanoid control via motion latent guidance. _arXiv preprint arXiv:2510.14952_ , 2025. 

- [28] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [29] Matthew Loper, Naureen Mahmood, Javier Romero, Gerard Pons-Moll, and Michael J Black. Smpl: A skinned multi-person linear model. In _Seminal Graphics Papers: Pushing the Boundaries, Volume 2_ , pages 851–866. 2023. 

- [30] Chenhao Lu, Xuxin Cheng, Jialong Li, Shiqi Yang, Mazeyu Ji, Chengjing Yuan, Ge Yang, Sha Yi, and Xiaolong Wang. Mobile-television: Predictive motion priors for humanoid whole-body control. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5364–5371. IEEE, 2025. 

- [31] Zhengyi Luo, Jinkun Cao, Kris Kitani, Weipeng Xu, 

et al. Perpetual humanoid control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 10895–10904, 2023. 

- [32] Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Casta˜neda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [33] Naureen Mahmood, Nima Ghorbani, Nikolaus F Troje, Gerard Pons-Moll, and Michael J Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 5442–5451, 2019. 

- [34] Mayank Mittal, Pascal Roth, James Tigue, Antoine Richard, Octi Zhang, Peter Du, Antonio Serrano-Mu˜noz, Xinjie Yao, Ren´e Zurbr¨ugg, Nikita Rudin, Lukasz Wawrzyniak, Milad Rakhsha, Alain Denzler, Eric Heiden, Ales Borovicka, Ossama Ahmed, Iretiayo Akinola, Abrar Anwar, Mark T. Carlson, Ji Yuan Feng, Animesh Garg, Renato Gasoto, Lionel Gulich, Yijie Guo, M. Gussert, Alex Hansen, Mihir Kulkarni, Chenran Li, Wei Liu, Viktor Makoviychuk, Grzegorz Malczyk, Hammad Mazhar, Masoud Moghani, Adithyavairavan Murali, Michael Noseworthy, Alexander Poddubny, Nathan Ratliff, Welf Rehberg, Clemens Schwarke, Ritvik Singh, James Latham Smith, Bingjie Tang, Ruchik Thaker, Matthew Trepte, Karl Van Wyk, Fangzhou Yu, Alex Millane, Vikram Ramasamy, Remo Steiner, Sangeeta Subramanian, Clemens Volk, CY Chen, Neel Jawale, Ashwin Varghese Kuruttukulam, Michael A. Lin, Ajay Mandlekar, Karsten Patzwaldt, John Welsh, Huihua Zhao, Fatima Anes, Jean-Francois Lafleche, Nicolas Mo¨enneLoccoz, Soowan Park, Rob Stepinski, Dirk Van Gelder, Chris Amevor, Jan Carius, Jumyung Chang, Anka He Chen, Pablo de Heras Ciechomski, Gilles Daviet, Mohammad Mohajerani, Julia von Muralt, Viktor Reutskyy, Michael Sauter, Simon Schirm, Eric L. Shi, Pierre Terdiman, Kenny Vilella, Tobias Widmer, Gordon Yeoman, Tiffany Chen, Sergey Grizan, Cathy Li, Lotus Li, Connor Smith, Rafael Wiltz, Kostas Alexis, Yan Chang, David Chu, Linxi ”Jim” Fan, Farbod Farshidian, Ankur Handa, Spencer Huang, Marco Hutter, Yashraj Narang, Soha Pouya, Shiwei Sheng, Yuke Zhu, Miles Macklin, Adam Moravanszky, Philipp Reist, Yunrong Guo, David Hoeller, and Gavriel State. Isaac lab: A gpuaccelerated simulation framework for multi-modal robot learning. _arXiv preprint arXiv:2511.04831_ , 2025. URL https://arxiv.org/abs/2511.04831. 

- [35] Noboru Myers, Obin Kwon, Sankalp Yamsani, and Joohyung Kim. Child (controller for humanoid imitation and live demonstration): A whole-body humanoid teleoperation system. In _2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids)_ , pages 1– 6, 2025. doi: 10.1109/Humanoids65713.2025.11203119. 

- [36] NVIDIA. NVIDIA TensorRT, 2026. URL https://github. 

com/NVIDIA/TensorRT. Accessed: 2026-01-25. 

- [37] ONNX Runtime developers. ONNX Runtime, November 2018. URL https://github.com/microsoft/onnxruntime. 

- [38] Yixuan Pan, Ruoyi Qiao, Li Chen, Kashyap Chitta, Liang Pan, Haoguang Mai, Qingwen Bu, Hao Zhao, Cunyuan Zheng, Ping Luo, et al. Agility meets stability: Versatile humanoid control with heterogeneous data. _arXiv preprint arXiv:2511.17373_ , 2025. 

- [39] Mathis Petrovich, Michael J Black, and G¨ul Varol. Tmr: Text-to-motion retrieval using contrastive 3d human motion synthesis. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 9488– 9497, 2023. 

- [40] Abhinanda R. Punnakkal, Arjun Chandrasekaran, Nikos Athanasiou, Alejandra Quiros-Ramirez, and Michael J. Black. BABEL: Bodies, action and behavior with english labels. In _Proceedings IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR)_ , pages 722–731, June 2021. 

- [41] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pages 8748–8763. PmLR, 2021. 

- [42] Junli Ren, Junfeng Long, Tao Huang, Huayi Wang, Zirui Wang, Feiyu Jia, Wentao Zhang, Jingbo Wang, Ping Luo, and Jiangmiao Pang. Humanoid goalkeeper: Learning from position conditioned task-motion constraints. _arXiv preprint arXiv:2510.18002_ , 2025. 

- [43] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [44] Agon Serifi, Ruben Grandia, Espen Knoop, Markus Gross, and Moritz B¨acher. Robot motion diffusion model: Motion generation for robotic characters. In _SIGGRAPH asia 2024 conference papers_ , pages 1–9, 2024. 

- [45] Yiyang Shao, Xiaoyu Huang, Bike Zhang, Qiayuan Liao, Yuman Gao, Yufeng Chi, Zhongyu Li, Sophia Shao, and Koushil Sreenath. Langwbc: Language-directed humanoid whole-body control via end-to-end learning. _arXiv preprint arXiv:2504.21738_ , 2025. 

- [46] Zehong Shen, Huaijin Pi, Yan Xia, Zhi Cen, Sida Peng, Zechen Hu, Hujun Bao, Ruizhen Hu, and Xiaowei Zhou. World-grounded human motion recovery via gravityview coordinates. In _SIGGRAPH Asia 2024 Conference Papers_ , pages 1–11, 2024. 

- [47] Yi Shi, Jingbo Wang, Xuekun Jiang, Bingkun Lin, Bo Dai, and Xue Bin Peng. Interactive character control with auto-regressive motion diffusion models. _ACM Transactions on Graphics (TOG)_ , 43(4):1–14, 2024. 

- [48] Zhi Su, Bike Zhang, Nima Rahmanian, Yuman Gao, Qiayuan Liao, Caitlin Regan, Koushil Sreenath, and S Shankar Sastry. Hitter: A humanoid table tennis robot via hierarchical planning and learning. _arXiv preprint_ 

_arXiv:2508.21043_ , 2025. 

- [49] Guy Tevet, Sigal Raab, Brian Gordon, Yonatan Shafir, Daniel Cohen-Or, and Amit H Bermano. Human motion diffusion model. _arXiv preprint arXiv:2209.14916_ , 2022. 

- [50] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 5026–5033. IEEE, 2012. doi: 10.1109/IROS.2012.6386109. 

- [51] Unitree Robotics. Unitree G1: Humanoid agent AI avatar. https://www.unitree.com/g1, 2024. Accessed: 2026-0125. 

- [52] Dewei Wang, Xinmiao Wang, Xinzhe Liu, Jiyuan Shi, Yingnan Zhao, Chenjia Bai, and Xuelong Li. More: Mixture of residual experts for humanoid lifelike gaits learning on complex terrains, 2025. URL https://arxiv. org/abs/2506.08840. 

- [53] Yuan Wang, Di Huang, Yaqi Zhang, Wanli Ouyang, Jile Jiao, Xuetao Feng, Yan Zhou, Pengfei Wan, Shixiang Tang, and Dan Xu. Motiongpt-2: A general-purpose motion-language model for motion generation and understanding. _arXiv preprint arXiv:2410.21747_ , 2024. 

- [54] Yufu Wang, Yu Sun, Priyanka Patel, Kostas Daniilidis, Michael J Black, and Muhammed Kocabas. Prompthmr: Promptable human mesh recovery. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1148–1159, 2025. 

- [55] Yuxuan Wang, Haobin Jiang, Shiqing Yao, Ziluo Ding, and Zongqing Lu. Sentinel: A fully end-to-end languageaction model for humanoid whole body control. _arXiv preprint arXiv:2511.19236_ , 2025. 

- [56] Lixing Xiao, Shunlin Lu, Huaijin Pi, Ke Fan, Liang Pan, Yueer Zhou, Ziyong Feng, Xiaowei Zhou, Sida Peng, and Jingbo Wang. Motionstreamer: Streaming motion generation via diffusion-based autoregressive model in causal latent space. _arXiv preprint arXiv:2503.15451_ , 2025. 

- [57] Weiji Xie, Chenjia Bai, Jiyuan Shi, Junkai Yang, Yunfei Ge, Weinan Zhang, and Xuelong Li. Humanoid wholebody locomotion on narrow terrain via dynamic balance and reinforcement learning, 2025. URL https://arxiv.org/ abs/2502.17219. 

- [58] Weiji Xie, Jinrui Han, Jiakun Zheng, Huanyu Li, Xinzhe Liu, Jiyuan Shi, Weinan Zhang, Chenjia Bai, and Xuelong Li. Kungfubot: Physics-based humanoid wholebody control for learning highly-dynamic skills. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. URL https://openreview.net/ forum?id=LCPoXt0pzm. 

- [59] Haoru Xue, Tairan He, Zi Wang, Qingwei Ben, Wenli Xiao, Zhengyi Luo, Xingye Da, Fernando Casta˜neda, Guanya Shi, Shankar Sastry, et al. Opening the simto-real door for humanoid pixel-to-action policy transfer. _arXiv preprint arXiv:2512.01061_ , 2025. 

- [60] Haoru Xue, Xiaoyu Huang, Dantong Niu, Qiayuan Liao, Thomas Kragerud, Jan Tommy Gravdahl, Xue Bin Peng, 

Guanya Shi, Trevor Darrell, Koushil Sreenath, et al. Leverb: Humanoid whole-body control with latent visionlanguage instruction. _arXiv preprint arXiv:2506.13751_ , 2025. 

- [61] Yufei Xue, Wentao Dong, Minghuan Liu, Weinan Zhang, and Jiangmiao Pang. A unified and general humanoid whole-body controller for fine-grained locomotion. _arXiv e-prints_ , pages arXiv–2502, 2025. 

- [62] Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, Pieter Abbeel, Carmelo Sferrazza, C Karen Liu, Rocky Duan, and Guanya Shi. Omniretarget: Interactionpreserving data generation for humanoid whole-body loco-manipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

Tao Chen, Linjie Luo, Youyi Zheng, and Xin Chen. Motiongpt3: Human motion as a second modality. _arXiv preprint arXiv:2506.24086_ , 2025. 

   - [73] Shaoting Zhu, Ziwen Zhuang, Mengjie Zhao, Kun-Ying Lee, and Hang Zhao. Hiking in the wild: A scalable perceptive parkour framework for humanoids, 2026. URL https://arxiv.org/abs/2601.07718. 

   - [74] Ziwen Zhuang, Shaoting Zhu, Mengjie Zhao, and Hang Zhao. Deep whole-body parkour. _arXiv preprint arXiv:2601.07701_ , 2026. 

- [63] Shiqi Yang. Ace: A cross-platform visual-exoskeleton system for low-cost dexterous teleoperation. Master’s thesis, University of California, San Diego, 2025. 

- [64] Kangning Yin, Weishuai Zeng, Ke Fan, Minyue Dai, Zirui Wang, Qiang Zhang, Zheng Tian, Jingbo Wang, Jiangmiao Pang, and Weinan Zhang. Unitracker: Learning universal whole-body motion tracker for humanoid robots. _arXiv preprint arXiv:2507.07356_ , 2025. 

- [65] Yanjie Ze, Zixuan Chen, Jo˜ao Pedro Ara´ujo, Zi ang Cao, Xue Bin Peng, Jiajun Wu, and C. Karen Liu. Twist: Teleoperated whole-body imitation system, 2025. URL https://arxiv.org/abs/2505.02833. 

- [66] Yanjie Ze, Siheng Zhao, Weizhuo Wang, Angjoo Kanazawa, Rocky Duan, Pieter Abbeel, Guanya Shi, Jiajun Wu, and C Karen Liu. Twist2: Scalable, portable, and holistic humanoid data collection system. _arXiv preprint arXiv:2511.02832_ , 2025. 

- [67] Jianrong Zhang, Yangsong Zhang, Xiaodong Cun, Yong Zhang, Hongwei Zhao, Hongtao Lu, Xi Shen, and Ying Shan. Generating human motion from textual descriptions with discrete representations. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 14730–14740, 2023. 

- [68] Mingyuan Zhang, Zhongang Cai, Liang Pan, Fangzhou Hong, Xinying Guo, Lei Yang, and Ziwei Liu. Motiondiffuse: Text-driven human motion generation with diffusion model. _IEEE transactions on pattern analysis and machine intelligence_ , 46(6):4115–4128, 2024. 

- [69] Yan Zhang, Yao Feng, Alp´ar Cseke, Nitin Saini, Nathan Bajandas, Nicolas Heron, and Michael J. Black. PRIMAL: physically reactive and interactive motor model for avatar learning. October 2025. 

- [70] Zhikai Zhang, Jun Guo, Chao Chen, Jilong Wang, Chenghuai Lin, Yunrui Lian, Han Xue, Zhenrong Wang, Maoqi Liu, Jiangran Lyu, et al. Track any motions under any disturbances. _arXiv preprint arXiv:2509.13833_ , 2025. 

- [71] Kaifeng Zhao, Gen Li, and Siyu Tang. Dartcontrol: A diffusion-based autoregressive motion model for real-time text-driven motion control. _arXiv preprint arXiv:2410.05260_ , 2024. 

- [72] Bingfan Zhu, Biao Jiang, Sunyi Wang, Shixiang Tang, 

APPENDIX A 

## ADDITIONAL IMPLEMENTATION DETAILS 

This appendix provides supplementary implementation details that are omitted from the main text due to space constraints. 


Fig. 6: **Word cloud of text annotations in the BABEL dataset.** 

standard termination conditions, and any motion that fails is removed. 

**Dataset Construction for Motion Generation.** For the AMASS dataset: 

- 1) Motion segments are paired with textual annotations from the BABEL dataset [40] via filename-based indexing and temporal alignment. The distribution of text annotations is shown in Fig. 6. 

- 2) Mirror augmentation is applied to both motion sequences and their corresponding textual labels, effectively doubling the dataset size. 

For the proprietary dataset, which mainly contains complex long-horizon motions, we manually assign a unique label to each sequence. To distinguish such long-form descriptions from segment-level annotations, we wrap these labels with “ _⟨·⟩_ ” markers, e.g., multiple hip hop dance segments of several tens of seconds will be named as “ _⟨_ hiphop 1 _⟩_ ”, “ _⟨_ hiphop 2 _⟩_ ”, and so on. Since this labeling is coarse-grained, we found it allows the model to associate each label with a distinct motion style and generate stylistically consistent motions, rather than reproducing an entire reference sequence. 

## **Dataset Construction for Motion Tracking.** 

## _A. Data Preprocessing and Dataset Construction_ 

We describe the complete data preprocessing pipeline and the construction of datasets used for training the motion generator and motion tracker. All datasets share a common preprocessing procedure, followed by task-specific preparation for motion generation and motion tracking. 

## **Shared Preprocessing Pipeline.** 

- 1) All motion sequences are first retargeted from the SMPL [29] human skeleton to the 29-DoF G1 humanoid robot using GMR [2]. 

- 2) The retargeted motions are then temporally resampled from 30 Hz to a unified frequency of 50 Hz. 

- 3) Following PBHC [58], feet contact indicators are extracted from the retargeted motions using a thresholdbased rule: 

   - _c_<sup>left</sup> _t_ = I[ _∥_ **_p_**<sup>l</sup> _t_<sup>-</sup> +1<sup>ankle</sup> _−_ **_p_**<sup>l</sup> _t_<sup>-ankle</sup> _∥_<sup>2</sup> 2<sup>_< ϵ_vel]</sup><sup>_·_I[</sup><sup>_p_l</sup> _t,z_<sup>-ankle</sup> _< ϵ_ height] _,_ (1) 

   - where _c_<sup>left</sup> _t_ represents the contact mask of the left foot and **_p_**<sup>l</sup> _t_<sup>-ankle</sup> denotes the position of the left ankle joint at time _t_ . _ϵ_ vel = 0 _._ 002 and _ϵ_ height = 0 _._ 2 are empirically chosen thresholds. Similarly for the right foot. 

- 4) Filtering: (1) Based on the unfiltered dataset, we train a universal motion tracking policy with privileged information, without domain randomization, and with relaxed termination conditions by removing End-Effector Height Deviation and Pelvis Height Deviation. The policy is trained for 40,000 steps, and we record the failure rate of each motion using a sliding average method. (2) We remove those motions with a tracking failure probability greater than 0.05, using the relaxed termination conditions. (3) The remaining motions are re-evaluated using 

- 1) For data undergoing the **Shared Preprocessing Pipeline** , we further segment motions into short clips with a maximum duration of 40 seconds (i.e., 2000 frames). Specifically, each motion sequence is partitioned into multiple clips whose lengths are constrained to lie within [100 _,_ 2000] frames, and adjacent clips are allowed to temporally overlap, with the overlap length constrained to lie within [50 _,_ 200] frames. 

- 2) Data Augmentation via Motion Generation: We sample text annotations from the BABEL training set to construct 20-second text streams. For each motion sequence, all associated text annotations are extracted, and the generation length assigned to each annotation is proportional to its temporal duration within the original motion. Using these constructed text streams, we then generate synthetic motions with our trained motion generation model. 

## _B. Motion Generation_ 

**Robot Skeleton Motion Representation.** We define a pair of deterministic forward and inverse algorithms that transform between a raw robot motion trajectory and a perframe, local incremental motion representation. The forward algorithm maps a raw motion sequence _{pt, Rt, qt, ct}_<sup>_T_</sup> _t_ =0<sup>to</sup> a feature sequence _{ft}_<sup>_T_</sup> _t_ =0<sup>_−_1andaninitialpose(</sup><sup>_p_0</sup><sup>_, R_0).The</sup> inverse algorithm reconstructs the motion sequence from the feature sequence given the initial pose. Both transformations are invariant to global translation and yaw and are exactly invertible up to numerical precision. In these algorithms, _pt ∈_ R<sup>3</sup> denotes the root translation, _Rt_ the root rotation, _qt_ the joint positions, and _ct_ the feet contact indicators. The motion feature _ft_ consists of: _ϕt_ representing the roll and pitch angles as (sin _θ,_ cos _θ −_ 1), ∆ _ψt_ the yaw increment, ∆ _p_<sup>local</sup> _t_ 

## **Algorithm 1** Forward Transformation: Raw Motion _→_ Motion <u>Features</u> 

|**Req**<br>|**uire:** Raw Motion _{pt, Rt, qt, ct}_<sup>_T_</sup><br>_t_=0<br>|
|---|---|
|**Ens**|**ure:** Motion Features _{ft}_<sup>_T −_1</sup><br>_t_=0 <sup>, Initial Pose (</sup><sup>_p_0</sup><sup>_, R_0)</sup>|
|1:|(_p_0_, R_0)_←_(_p_0_, R_0)|
|2:|**for** _t_= 0 **to** _T −_1 **do**|
|3:|(roll_t,_pitch_t,_yaw_t_)_←_QUATTOEULER(_Rt_)|
|4:|(<br>_,_<br>_,_yaw_t_+1)_←_QUATTOEULER(_Rt_+1)|
|5:|_sr ←_sin(roll_t_)_,_<br>_cr ←_cos(roll_t_)_−_1|
|6:|_sp ←_sin(pitch_t_)_,_<br>_cp ←_cos(pitch_t_)_−_1|
|7:|_ϕt ←_[_sr, cr, sp, cp_]|
|8:|∆_ψt ←_yaw_t_+1_−_yaw_t_<br><br>|
|9:|∆_p_<sup>local</sup><br>_t_<br>_←Rz_(yaw_t_)<sup>_⊤_</sup>(_pt_+1_−pt_)|
|10:|∆_qt ←qt_+1_−qt_<br>|
|11:|_ht ←_(_pt_)_z_<br>|
|12:<br>13:|_ft ←_[_ϕt,_∆_ψt, ct,_∆_p_<sup>local</sup><br>_t_<br>_, ht, qt,_∆_qt_]<br> **end for**|


## **Algorithm 2** Inverse Transformation: Motion Features _→_ Raw <u>Motion</u> 

**Require:** Motion features _{ft}_<sup>_T_</sup> _t_ =0<sup>_−_1,Initialpose(</sup><sup>_p_init</sup><sup>_, R_init)</sup> **Ensure:** Reconstructed raw motion _{pt, Rt, qt, ct}_<sup>_T_</sup> _t_ =0<sup>_−_1</sup> 1: <u>(</u> _<u>, ,</u>_ yaw0) _←_ QUATTOEULER( _R_ init) 2: _p_<sup>_′_</sup> 0<sup>_←p_init</sup> 3: **for** _t_ = 0 **to** _T −_ 1 **do** 4: [ _ϕt,_ ∆ _ψt, ct,_ ∆ _p_<sup>local</sup> _t , ht, qt,_ ∆ _qt_ ] _← ft_ 5: ( _sr, cr, sp, cp_ ) _← ϕt_ 6: roll _t ←_ arctan 2( _sr, cr_ + 1) 7: pitch _t ←_ arctan 2( _sp, cp_ + 1) 8: _Rt ←_ EULERTOQUAT(roll _t,_ pitch _t,_ yaw _t_ ) 9: _pt ←_ [( _p_<sup>_′_</sup> _t_<sup>)</sup><sup>_x,_(</sup><sup>_p′_</sup> _t_<sup>)</sup><sup>_y, ht_]</sup><sup>_⊤_</sup> 10: **if** _t < T −_ 1 **then** 11: yaw _t_ +1 _←_ yaw _t_ + ∆ _ψt_ 12: ∆ _pt ← Rz_ (yaw _t_ )∆ _p_<sup>local</sup> _t_ 13: _p_<sup>_′_</sup> _t_ +1<sup>_←p_</sup> _t_<sup>_′_+ ∆</sup><sup>_pt_</sup> 14: **end if** 15: **end for** 

the local translation increment, _ht_ the absolute root height, and ∆ _qt_ the joint velocities. In the inverse transformation, _p_<sup>_′_</sup> _t_ serves as an intermediate integration variable for translation, while _pt_ represents the final reconstructed position with its _z_ -component assigned by _ht_ . 

**Architecture.** We design the VAE and LDM modules following the DART [71]. The VAE adopts a transformerbased structure, where both the encoder and decoder are implemented as stacks of transformer encoder layers augmented with skip connections. In the encoding stage, the historical and future motion sequences are concatenated, linearly projected into a high-dimensional space, and prepended with a set of learnable distribution parameters. After incorporating positional encodings, the combined sequences are processed by the transformer encoder. The output corresponding to the distribution parameters is used to parameterize a Gaussian 

distribution in the latent space, from which latent variables are sampled. During decoding, the sampled latent variables, together with the historical motion sequences, are used to reconstruct the future motion sequences through another transformer stack and a final linear projection layer. 

The LDM is implemented as a transformer encoder that operates in the latent space. It takes four types of inputs: noisy latent variables, the diffusion timesteps, historical motion sequences, and text embeddings. Each input modality is independently embedded into a shared hidden dimension. To support classifier-free guidance, the text embeddings are randomly masked during training with a fixed probability of 0 _._ 1. All embedded representations are concatenated into a sequence of tokens, enhanced with sinusoidal positional encodings, and fed into multiple transformer encoder layers. The output corresponding to the noisy latent token is then mapped back to the noise dimension, predicting the cleaned latent variables for the diffusion process. The detailed Motion Generator hyperparameters are shown in Table VI. 

## **Training Details.** 

When training the VAE and LDM, we organize motion data into fixed-length motion primitives to ensure temporal continuity and stable learning. 

Specifically, each motion primitive **P**<sup>_i_</sup> consists of two parts: (1) _T_ history frames of historical motion, and (2) _T_ future frames of future motion to be predicted. The historical part of **P**<sup>_i_</sup> is the same as the last _T_ history frames of the preceding primitive **P**<sup>_i−_1</sup> , which enforces continuity between adjacent primitives. 

During data loading, we sample _N_ prim consecutive primitives from a full motion sequence to form one training sample. This results in a motion clip of length _T_ history + _N_ prim _· T_ future frames. The model is therefore trained on an ordered sequence of primitives that together represent a coherent motion segment. 

To reduce distribution mismatch between training and inference, we further adopt a self-rollout curriculum. As training progresses, with a linearly increasing probability, the history frames of a primitive are replaced by the last _T_ history frames generated by the model from the previous step, instead of being directly sampled from the dataset. The replacement probability is capped at 0 _._ 8 to maintain training stability and avoid excessive error accumulation. 

For the LDM, we adopt the DDPM framework. The diffusion process gradually adds Gaussian noise to the latent motion latent _z_ 0 over _K_ timesteps. The forward noising process is defined as a Markov chain: 


Here _βk ∈_ (0 _,_ 1) is the noise schedule determined by a cosine scheduler. Let _αk_ = 1 _−βk_ and _α_ ¯ _k_ =<sup>�</sup><sup>_k_</sup> _s_ =1<sup>_αs_. Then the noisy</sup> latent _zk_ at an arbitrary timestep _k_ can be directly sampled from _z_ 0 via: 


During training, we randomly sample a timestep _k ∼U{_ 1 _, K}_ and compute _zk_ from _z_ 0 using Eq. 3. The LDM model _Fθ_ then takes _zk_ , the timestep _k_ , the historical motion features _ft−T_ history: _t−_ 1, and the text embedding _et_ as inputs, and predicts the original _z_ 0. 

**Losses.** The VAE is optimized with a combined loss function consisting of a reconstruction term, a lightweight KL divergence term, and a comprehensive geometric loss that ensures physical plausibility. The overall objective is defined as follows: 


where _L_ rec is the reconstruction loss. We adopt the Huber loss (smooth L1 loss) as the reconstruction objective to measure the discrepancy between the predicted future motion features _f_ ˆ and the ground truth _f_ : 


This encourages the decoder to accurately reconstruct the motion sequences. To maintain a well-structured latent space without sacrificing expressiveness, we impose a KL penalty toward a standard Gaussian distribution: 


To enhance physical coherence and motion quality, we introduce a multi-term geometric loss evaluated in forwardkinematics space: 


where _L_ body <u>trans</u><sup>and</sup><sup>_L_</sup> body <u>rot</u><sup>penalizeerrorsinbodyglobal</sup> translation and rotation. _L_ dof and _L_ dof <u>vel</u><sup>penalizeerrorsin</sup> dof angles and angular velocities. _L_ contact focuses on foot positions during contact phases to improve grounding. Each geometric term is computed using the Huber loss between predicted and ground-truth kinematic quantities, which ensemble significantly improves motion smoothness and physical realism. 

The LDM is trained with the following losses: 

where _σ_ CFG is the guidance scale. Then, the predicted _z_ ˆ0 is used to compute the estimated noise _ϵθ_ : 


Finally, we sample _zk−_ 1 from the reverse transition distribution: 


where _σk_<sup>2=</sup><sup>_βk_. The final clean latent</sup><sup>_z_0 is then passed through</sup> the VAE decoder to produce the future motion features. 

TABLE VI: **Hyperparameters for Motion Generator.** 

|**Hyperparameter**|**Value**|
|---|---|
|History Length _T_history|2|
|Future Length _T_future|8|
|Primitive Number _N_prim|4|
|Batch Size|512|
|Learning Rate|1_e −_4|
|Feature Dim _d_feat|69|
|_λ_rec|1_._0|
|_λ_KL|1_e −_4|
|_λ_simple|1_._0|
|_λ_trans|0_._05|
|_λ_rot|1_e −_2|
|_λ_dof|0_._03|
|_λ_vel|1_e −_5|
|_λ_contact|0_._01|
|VAE Training||
|Hidden Dim|512|
|FFN Dim|1024|
|Latent Dim|128|
|Transformer Layers Number|9|
|Heads Number|4|
|Maximum Rollout Probability|1_._0|
|LDM Training||
|Noise Dim|128|
|Hidden Dim|512|
|FFN Dim|1024|
|Transformer Layers Number|8|
|Heads Number|4|
|Diffusion Steps _n_denoise|5|
|Max Rollout Probability|0_._8|


where the definitions of _L_ rec and _L_ geo are consistent with the losses used for training the VAE and _L_ simple is defined as 


**Inference Details.** During inference, we first sample a Gaussian noise _zK ∼N_ (0 _, I_ ), and then iteratively denoise for timestep _k_ = _K, K −_ 1 _, . . . ,_ 1 to obtain the clean latent _z_ 0. At each denoising step _k_ , classifier-free guidance is applied to make motion latent predictions: 


## _C. Motion Tracking Policy_ 

The training of the motion tracking policy adopts an asymmetric actor-critic style, where the critic network takes additional privileged information as input. The observation space, reward functions, termination conditions, and domain randomization setting are listed in Table VII, Table VIII, Table IX, and Table X, respectively. 

## APPENDIX B 

## ADDITIONAL EXPERIMENTAL DETAILS 

This appendix provides supplementary descriptions of the experimental setup, evaluation protocols, and additional results. 

TABLE VII: **Observation space for Motion Tracker.** The **Type** column distinguishes between policy inputs (Base) and criticonly inputs (Privileged). The 14 key bodies include: Pelvis, Hips (2), Knees (2), Ankles (2), Torso, Shoulders (2), Elbows (2), and Wrists (2). The total dimensionality is 431 for Base observations and 557 when including Privileged inputs. 

|**Term**|**Description**|**Dim.**|**Type**|
|---|---|---|---|
|Reference Motion|Target joint positions and velocities over a 5-step future horizon|290 = 2_×_29_×_5|Base|
|Reference Pelvis Position|Relative pelvis positions in the base frame over a 5-step horizon|15 = 3_×_5|Base|
|Reference Pelvis Orientation|Pelvis orientations in the base frame using a 6D representation over a 5-step horizon|30 = 6_×_5|Base|
|Projected Gravity|Gravity vector expressed in the robot base frame|3|Base|
|Base Velocity|Linear and angular velocities of the pelvis link.|6 = 3 + 3|Base|
|Joint State|Joint positions and velocities|58 = 2_×_29|Base|
|Last Action|Previous joint position commands|29|Base|
|Key Body Position|Relative positions of 14 key bodies in the base frame|42 = 3_×_14|Priv.|
|Key Body Orientation|Relative orientations of 14 key bodies in the base frame using a 6D representation|84 = 6_×_14|Priv.|


TABLE VIII: **Reward functions for Motion Tracker.** Tracking terms adopt a negative exponential form reward, _ri_ = exp( _−∥e∥_<sup>2</sup> _/σ_<sup>2</sup> ), where _e_ denotes the corresponding tracking error and _σ_ is the scale factor. 

|**Term**|**Weight**|**Description**|
|---|---|---|
|_Tracking Terms_|||
|Pelvis Position|0_._5|Global pelvis position error (_σ_ = 0_._3 m)|
|Pelvis Orientation|0_._5|Global pelvis orientation error (_σ_ = 0_._4 rad)|
|Key Body Position|1_._0|Relative body position error in the base frame (_σ_ = 0_._3 m)|
|Key Body Orientation|1_._0|Relative body orientation error in the base frame (_σ_ = 0_._4 rad)|
|Body Linear Velocity|1_._0|Global body linear velocity error in the base frame (_σ_ = 1_._0 m/s)|
|Body Angular Velocity|1_._0|Global body angular velocity error in the base frame (_σ_ = 3_._14 rad/s)|
|_Regularization_|||
|Action Rate|_−_0_._1|L2 penalty on action differences|
|Joint Limit|_−_10_._0|Penalty for joint position limit violations|
|Undesired Contact|_−_0_._1|Penalty for contacts on non-end-effector links|
|Feet Slide|_−_0_._3|Penalty on foot velocity during contact|
|Soft Landing|_−_3_._0_e −_4|Penalty on impact forces for smooth footfalls|
|Overspeed|_−_1_._0|Penalty for joint velocities exceeding 20.0 rad/s|
|Overeffort|_−_1_._0|Penalty for joint torques exceeding actuator limits|


TABLE IX: **Termination conditions for Motion Tracker.** 

|**Term**|**Description**|
|---|---|
|Timeout|Episode terminates when reaching the maximum duration (_T_ = 10s) or when the reference motion sequence is completed.|
|Pelvis Orientation Deviation|Deviation in gravity-aligned orientation between the reference and robot pelvis exceeds a threshold of 0_._8, measured by<br>the difference in the projected gravity vector along the pelvis _z_-axis.|
|Pelvis Height Deviation|_z_-axis tracking error of the robot pelvis relative to the reference motion exceeds 0_._25 m.|
|End-Effector Height Deviation|_z_-axis tracking error of the robot end-effectors (ankles and wrists) relative to the reference motion exceeds 0_._5 m.|


## _A. Experimental Procedure_ 

**Real-world Deployment.** In the quantitative evaluation of real-robot executions, we record the real-world robot trajectory by combining joint angles from motor sensors and the global position and orientation of the pelvis provided by the built-in odometry of the G1 robot. 

In the “Random” command experiments, we construct a 30second text stream by randomly sampling action descriptions from the BABEL training set. Specifically, 3–5 words are first sampled from the dataset vocabulary, and each word is assigned a random duration uniformly selected from 6 _,_ 7 _,_ 8 _,_ 9 _,_ 10 seconds. To ensure a well-defined start and termination, the sequence is prefixed and suffixed with a fixed 2-second “stand” command. Based on this text stream, reference motions are generated offline using our model. Owing to the limited physical space of the experimental environment, we discard 

any generated motion whose maximum displacement from the initial position exceeds 2 meters. The remaining motion trajectories are then executed on the real robot. 

To evaluate real-time performance, we deploy the entire system on the physical robot with motor command execution disabled and measure the latency of each module independently. The latency of the text encoding and motion generator modules is evaluated over 100 runs, whereas the tracking policy latency is measured over 1000 runs. To assess the latency of user interaction, we repeatedly command the real robot to switch from a “stand” command to a “wave left hand” command, and manually record the elapsed time between the moment a new text command is entered by the user and the moment the user perceives the robot initiating the corresponding motion. This latency is measured over 10 runs. 

**Motion Generation Evaluation.** We evaluate motion generation quality through a two-stage procedure consisting of 

TABLE X: **Domain randomization settings for Motion Tracker.** 

|**Term**|**Value**|
|---|---|
|Static friction|_U_(0_._3_,_1_._6)|
|Dynamic friction|_U_(0_._3_,_1_._2)|
|Restitution|_U_(0_._0_,_0_._5)|
|Joint default position offset|_U_(_−_0_._01_,_0_._01) rad|
|Torso CoM offset (_x, y, z_)|_U_(_−_0_._025_,_0_._025) m, _U_(_−_0_._05_,_0_._05) m, _U_(_−_0_._05_,_0_._05) m|
|External Push|Interval in _U_(1_._0_,_3_._0) s|


TABLE XI: **Training and simulation hyperparameters for Motion Tracker.** 

|**Parameter**|**Value**|
|---|---|
|Number of Environments|8192|
|Actor MLP Size|[2048_,_1024_,_512]|
|Critic MLP Size|[2048_,_1024_,_512]|
|Activation Function|ELU|
|Step per Environment|24|
|PPO Init Learning Rate|1_._0_e −_3|
|PPO Mini-batches|4|
|PPO Learning Epochs|5|
|PPO Clip Parameter|0_._2|
|Simulation Frequency|200 Hz|
|Policy Frequency|50 Hz|


motion rollout and metric-based assessment. 

We first construct a evaluation set from the BABEL validation split. Each motion sequence, together with its associated textual annotations and temporal durations, is segmented into chunks with a maximum length of 200 frames. Given these reconstructed textual prompts, the trained motion generation model is used to generate corresponding motion sequences. The generated motions are then evaluated from two complementary perspectives: segment-level quality and transitionlevel quality. 

Segment-level quality assesses how well each generated motion segment matches its corresponding textual description, using standard motion–text consistency metrics computed independently for each segment. 

Transition-level quality focuses on the temporal smoothness and coherence at textual transition boundaries. For each transition point, we extract a short motion clip consisting of 15 frames before and after the boundary, centered at the transition. Metrics are then computed on these clips to specifically assess the quality of motion transitions. 

**Motion Tracking Evaluation.** The explanation of experimental procedure in the main text is detailed enough. 

- _B. Evaluation Metrics_ 

We provide detailed definitions of the evaluation metrics used in our experiments. 

**Motion Quality.** We train the motion and text feature extractors based on TMR [39] to evaluate the quality of the generated motions. Specifically, we construct the BABEL dataset into individual text-motion pairs, with a maximum motion length of 200 frames. Through contrastive learning, we train motion and text feature extractors to produce closely aligned embeddings for semantically matching text-motion pairs. 

- **Frechet Inception Distance (FID).** FID is the principal metric for assessing the distributional similarity between generated and real motions in the extracted feature space. Let _Pg_ represent the empirical distribution of generated motion features and _Pr_ the empirical distribution of real motion features, with _µg_ , Σ _g_ and _µr_ , Σ _r_ as their respective means and covariances. The FID is computed as: 


- **Diversity (DIV).** Diversity measures the variance across the entire set of generated motions. To compute DIV, all generated motions are randomly split into two subsets of equal size _D_ , with feature vectors _{xi}_<sup>_D_</sup> _i_ =1<sup>and</sup><sup>_{x′_</sup> _i_<sup>_}D_</sup> _i_ =1<sup>.</sup> The metric is defined as: 


- **R-precision (R@K).** R@K evaluates text-to-motion semantic alignment by measuring retrieval accuracy within the feature space. Each time, a batch of _M_ = 32 motiontext pairs is sampled from the generated motion. For each motion, its corresponding text is used as a query to retrieve the most similar motions from the batch, by ranking motions based on Euclidean distance in the extracted feature space learned by the text and motion extractors. R@K is then defined as the percentage of queries for which the correct motion appears among the top-K retrieved results. 

- **Multimodal distance (MM-Dist).** MM-Dist directly measures the average proximity between a generated motion and its corresponding text in the feature space. For a batch of _M_ = 32 generated motions with their 

corresponding text descriptions, let _{hi}_<sup>_M_</sup> _i_ =1<sup>and</sup><sup>_{xi}M_</sup> _i_ =1 be their respective text and motion feature vectors. MMDist is computed as: 


- **Peak Jerk (PJ).** PJ captures the most extreme instantaneous jerk occurring during a motion transition. It is defined as the maximum absolute jerk value observed across all joints _K_ and all time steps within the transition sequence of length _L_ tr: 


where _ji_ ( _t_ ) is the jerk of joint _i_ at time _t_ . 

- **Area Under the Jerk (AUJ).** AUJ measures the cumulative deviation from natural smoothness over the entire transition. It aggregates the absolute difference between the instantaneous jerk at each frame and the dataset’s jerk level _javg_ . The metric is computed as: 


## **Tracking Fidelity.** 

- **Success Rate (Succ).** In the real-world experiments, a trial is considered successful if the robot completes the full motion execution without falling, encountering hardware malfunctions, or exceeding the predefined safety boundaries of the workspace. In the simulation experiments, success rate measures the proportion of motion sequences whose root-relative tracking error remains below a predefined threshold over the entire trajectory. For each sequence _i_ , we define the maximum root-relative mean per-link position error as 


The success rate is then computed as 


where _N_ is the number of test sequences and _θ_ = 0 _._ 3 m. 

- **Global MPJPE (** _E_ **g-mpjpe)** . Global Mean Per Joint Position Error measures the average 3D position error across all links: 


where _T_ is the number of time steps, _J_ is the total number of links, and the factor of 1000 converts from meters to millimeters. 

Although termed _Per Joint_ , the name follows conventions established in prior virtual character animation literature; in our robot setting, the metric is computed over all corresponding links. 

- **Root-relative MPJPE (** _E_ **mpjpe)** . Root-relative MPJPE measures position errors relative to the root link, eliminating systematic translation errors: 


where joint 0 represents the root (pelvis) link. 

- **Velocity Error (** _E_ **vel)** . Velocity error measures temporal consistency of motion execution: 


where velocities are computed as **v** _t_ = **p** _t_ +1 _−_ **p** _t_ . 

- **Acceleration Error (** _E_ **acc)** . Acceleration error captures higher-order temporal dynamics: 


where accelerations are computed as **a** _t_ = **v** _t_ +1 _−_ **v** _t_ . 

## _C. Baseline Methods_ 

This subsection describes the baseline methods used for comparison. 

**Motion Representation.** Table XII illustrates the differences in motion feature representations between **TextOp** and the baselines. 

## **Motion Tracking.** 

- TWIST2 [66] is a scalable and holistic humanoid data collection system designed to generate highquality, whole-body demonstrations. Within its hierarchical framework, the low-level controller is implemented as a task-agnostic motion tracking engine. We adopt the officially released checkpoint of the low-level controller to conduct the experiment. 

- GMT [12] trains a single unified policy for general humanoid motion tracking through two core components: an adaptive sampling strategy that balances easy and difficult motions during training, and a Motion Mixtureof-Experts architecture that specializes across different regions of the motion manifold. 

- Any2Track [70] employs a two-stage reinforcement learning framework that reformulates dynamics adaptability as an additional capability on top of basic action execution. The system consists of AnyTracker, a general motion tracker for handling diverse, highly dynamic motions within a single policy, and AnyAdapter, a history-informed adaptation module that provides online dynamics adaptability. We adopt the officially released 

TABLE XII: **Comparison of motion representation components used by different methods.** ✓ indicates the representation is used, _×_ indicates it is not used. Components are reported based on the actual feature vectors used by each method, regardless of semantic overlap between each other. For the following tables, in the Unitree G1 skeleton, the term “Body” refers to 29 body links, excluding the root link, whereas in the SMPL skeleton it corresponds to 22 spherical joints. The “Base Frame” denotes the coordinate frame attached to the root link. In contrast, the “Character Frame” is a local frame aligned with the root’s yaw: its origin coincides with the root position, its yaw matches the root yaw, and its roll and pitch are set to zero. 

|**Components**|**Dimension**|**DART+Retarget**|**BeyondMimic**|**HumanML3D**|**RobotMDM**|**TextOp**|
|---|---|---|---|---|---|---|
|Is Robot-Skeleton Generation|-|_×_|✓|✓|✓|✓|
|Root Trigonometric Encoding of Roll and Pitch|4|_×_|_×_|_×_|_×_|✓|
|Root Rotation 6D Representation|6|✓|_×_|_×_|_×_|_×_|
|Root Rotation Quaternion Representation|4|_×_|✓|✓|✓|_×_|
|Difference of Root Rotation 6D Representation|6|✓|_×_|_×_|_×_|_×_|
|Root Yaw Velocity|1|_×_|_×_|_×_|_×_|✓|
|Root Angular Velocity in the Z-axis|1|_×_|_×_|✓|✓|_×_|
|Root Angular Velocity|3|_×_|✓|_×_|_×_|_×_|
|Root Position|3|✓|✓|_×_|_×_|_×_|
|Root Height|1|_×_|_×_|✓|✓|✓|
|Root Linear Velocity in the Character Frame|3|✓|✓|_×_|_×_|✓|
|Root Linear Velocity in the XY-plane in the Character Frame|2|_×_|_×_|✓|✓|_×_|
|Dof Angle|29|_×_|_×_|✓|✓|✓|
|Dof Velocity|29|_×_|_×_|_×_|✓|✓|
|Body Rotation 6D Representation in the Base Frame|126 for SMPL|✓|_×_|_×_|_×_|_×_|
|Body Position in the Character Frame|87 (66 for SMPL)|✓|✓|✓|_×_|_×_|
|Body Linear Velocity in the Character Frame|87 (66 for SMPL)|✓|✓|✓|_×_|_×_|
|Foot Contact|2|_×_|_×_|✓|_×_|✓|
|Total Dim|-|276|187|213|66|69|


checkpoint of AnyTracker, the model trained in the first stage to conduct the experiment, since the second stage is not open-source. 

## _D. Additional Ablation Studies_ 

As shown in Table XIII, we conduct additional ablation studies to analyze the impact of key design choices in the motion generation module, including history length _T_ history, future length _T_ future, number of primitives _N_ prim, hidden dimension and layer count of LDM, guidance scale _σ_ CFG, number of denoising steps, and maximum rollout probability. Through a trade-off analysis considering distribution matching, semantic alignment, and motion smoothness, we ultimately select a set of parameters that achieves balanced performance across all metrics. 

## _E. Additional Real-World Results_ 

Additional real-world robot results are shown in Fig. 7. 

## _F. Computational Resources_ 

Model training is conducted on a server equipped with an NVIDIA A100-PCIE GPU with 40 GB memory and an Intel Xeon Gold 6348 CPU operating at 2.60 GHz. The training system runs Ubuntu 22.04.3 LTS. 

For deployment, we use a separate workstation with an NVIDIA GeForce RTX 4090 GPU and a 13th Gen Intel Core i7-13700 CPU. The deployment environment runs Ubuntu 20.04.6 LTS. 

TABLE XIII: **Ablation study on key hyperparameters for Motion Generation.** All results are reported as mean _±_ standard deviation over three generator rollout seeds. 

|**Setting**|||**Seg**|**ment**||||**Tran**|**sition**|||
|---|---|---|---|---|---|---|---|---|---|---|---|
||FID _↓_|Diversity _→_|R@1 _↑_|R@2 _↑_|R@3 _↑_|MM-dist _↓_|FID _↓_|Diversity _→_|PJ|_→_|AUJ _↓_|
|Dataset|0.000 _±_0.000|9.150 _±_0.158|0.357 _±_0.004|0.556 _±_0.006|0.684 _±_0.005|3.729 _±_0.000|0.000 _±_0.000|8.138 _±_0.013|0.005|_±_0.000|0.000 _±_0.000|
|_T_history = 1|2.972 _±_0.032|9.082 _±_0.139|0.283 _±_0.011|0.461 _±_0.002|0.588 _±_0.004|4.321 _±_0.107|4.107 _±_0.268|8.528 _±_0.139|0.017|_±_0.002|0.128 _±_0.002|
|_T_history = 2 (Ours)|3.072 _±_0.199|9.220 _±_0.151|0.300 _±_0.007|0.481 _±_0.004|0.607 _±_0.008|4.272 _±_0.058|3.238 _±_0.430|8.226 _±_0.079|0.015|_±_0.001|0.125 _±_0.001|
|_T_history = 3|3.718 _±_0.091|9.218 _±_0.094|0.287 _±_0.012|0.467 _±_0.009|0.594 _±_0.007|4.366 _±_0.062|3.695 _±_0.167|8.470 _±_0.085|0.016|_±_0.001|0.126 _±_0.001|
|_T_history = 5|4.713 _±_0.046|9.060 _±_0.079|0.279 _±_0.012|0.453 _±_0.001|0.566 _±_0.006|4.508 _±_0.049|4.750 _±_0.121|8.432 _±_0.154|0.019|_±_0.000|0.127 _±_0.001|
|_T_future = 4|3.339 _±_0.089|8.808 _±_0.104|0.256 _±_0.010|0.431 _±_0.011|0.549 _±_0.003|4.747 _±_0.023|2.904 _±_0.140|8.301 _±_0.136|0.013|_±_0.000|0.127 _±_0.000|
|_T_future = 6|2.930 _±_0.098|9.096 _±_0.027|0.283 _±_0.010|0.467 _±_0.011|0.584 _±_0.006|4.481 _±_0.027|2.910 _±_0.193|8.453 _±_0.135|0.016|_±_0.001|0.126 _±_0.001|
|_T_future = 8 (Ours)|3.072 _±_0.199|9.220 _±_0.151|0.300 _±_0.007|0.481 _±_0.004|0.607 _±_0.008|4.272 _±_0.058|3.238 _±_0.430|8.226 _±_0.079|0.015|_±_0.001|0.125 _±_0.001|
|_T_future = 10|4.126 _±_0.073|9.206 _±_0.070|0.326 _±_0.004|0.501 _±_0.004|0.624 _±_0.004|3.854 _±_0.015|5.467 _±_0.192|8.606 _±_0.163|0.028|_±_0.002|0.186 _±_0.002|
|_T_future = 12|3.161 _±_0.062|9.213 _±_0.175|0.300 _±_0.003|0.478 _±_0.013|0.603 _±_0.010|4.101 _±_0.025|4.080 _±_0.244|8.496 _±_0.125|0.016|_±_0.001|0.127 _±_0.002|
|_N_prim = 1|3.044 _±_0.204|8.391 _±_0.066|0.196 _±_0.005|0.346 _±_0.011|0.452 _±_0.014|6.245 _±_0.058|3.074 _±_0.183|8.047 _±_0.275|0.013|_±_0.001|0.123 _±_0.001|
|_N_prim = 2|2.578 _±_0.037|8.861 _±_0.117|0.256 _±_0.011|0.419 _±_0.011|0.547 _±_0.015|4.990 _±_0.038|2.277 _±_0.197|8.265 _±_0.087|0.011|_±_0.000|0.122 _±_0.000|
|_N_prim = 4 (Ours)|3.072 _±_0.199|9.220 _±_0.151|0.300 _±_0.007|0.481 _±_0.004|0.607 _±_0.008|4.272 _±_0.058|3.238 _±_0.430|8.226 _±_0.079|0.015|_±_0.001|0.125 _±_0.001|
|_N_prim = 6|3.733 _±_0.088|9.141 _±_0.092|0.307 _±_0.008|0.492 _±_0.010|0.616 _±_0.012|4.011 _±_0.012|4.802 _±_0.205|8.421 _±_0.054|0.022|_±_0.002|0.133 _±_0.002|
|_N_prim = 10|3.344 _±_0.098|9.111 _±_0.102|0.314 _±_0.010|0.482 _±_0.014|0.611 _±_0.005|3.897 _±_0.060|5.131 _±_0.272|8.315 _±_0.064|0.023|_±_0.001|0.134 _±_0.001|
|Hidden= 128|4.030 _±_0.242|9.493 _±_0.126|0.255 _±_0.006|0.435 _±_0.005|0.558 _±_0.006|4.640 _±_0.032|5.353 _±_0.208|8.903 _±_0.126|0.015|_±_0.001|0.126 _±_0.002|
|Hidden= 256|3.110 _±_0.082|9.089 _±_0.123|0.273 _±_0.009|0.448 _±_0.004|0.582 _±_0.009|4.487 _±_0.051|2.506 _±_0.197|8.279 _±_0.159|0.011|_±_0.000|0.123 _±_0.000|
|Hidden= 512 (Ours)|3.072 _±_0.199|9.220 _±_0.151|0.300 _±_0.007|0.481 _±_0.004|0.607 _±_0.008|4.272 _±_0.058|3.238 _±_0.430|8.226 _±_0.079|0.015|_±_0.001|0.125 _±_0.001|
|Hidden= 1024|3.552 _±_0.194|9.028 _±_0.167|0.277 _±_0.009|0.464 _±_0.012|0.598 _±_0.007|4.324 _±_0.040|3.607 _±_0.076|8.451 _±_0.100|0.014|_±_0.000|0.124 _±_0.001|
|Hidden= 2048|3.688 _±_0.131|9.154 _±_0.211|0.285 _±_0.010|0.449 _±_0.009|0.581 _±_0.004|4.509 _±_0.038|4.326 _±_0.385|8.633 _±_0.161|0.013|_±_0.000|0.125 _±_0.000|
|Layers= 4|4.186 _±_0.098|9.315 _±_0.089|0.303 _±_0.010|0.477 _±_0.006|0.597 _±_0.004|4.225 _±_0.024|5.151 _±_0.280|8.584 _±_0.117|0.014|_±_0.000|0.124 _±_0.000|
|Layers= 6|3.868 _±_0.203|9.213 _±_0.077|0.291 _±_0.005|0.462 _±_0.009|0.596 _±_0.004|4.275 _±_0.034|4.609 _±_0.365|8.701 _±_0.187|0.015|_±_0.001|0.127 _±_0.004|
|Layers= 8 (Ours)|3.072 _±_0.199|9.220 _±_0.151|0.300 _±_0.007|0.481 _±_0.004|0.607 _±_0.008|4.272 _±_0.058|3.238 _±_0.430|8.226 _±_0.079|0.015|_±_0.001|0.125 _±_0.001|
|Layers= 10|3.342 _±_0.082|9.030 _±_0.051|0.296 _±_0.003|0.476 _±_0.002|0.601 _±_0.007|4.254 _±_0.021|3.272 _±_0.199|8.205 _±_0.056|0.012|_±_0.000|0.123 _±_0.001|
|_σ_CFG = 3|2.537 _±_0.056|8.919 _±_0.227|0.259 _±_0.003|0.441 _±_0.004|0.567 _±_0.006|4.667 _±_0.048|1.493 _±_0.168|8.036 _±_0.092|0.013|_±_0.001|0.124 _±_0.001|
|_σ_CFG = 4|2.818 _±_0.118|9.058 _±_0.133|0.295 _±_0.008|0.480 _±_0.007|0.597 _±_0.005|4.384 _±_0.052|2.499 _±_0.199|8.258 _±_0.150|0.014|_±_0.000|0.124 _±_0.001|
|_σ_CFG = 5 (Ours)|3.072 _±_0.199|9.220 _±_0.151|0.300 _±_0.007|0.481 _±_0.004|0.607 _±_0.008|4.272 _±_0.058|3.238 _±_0.430|8.226 _±_0.079|0.015|_±_0.001|0.125 _±_0.001|
|_σ_CFG = 6|3.588 _±_0.148|9.197 _±_0.071|0.304 _±_0.001|0.486 _±_0.002|0.610 _±_0.010|4.141 _±_0.016|4.015 _±_0.282|8.279 _±_0.090|0.015|_±_0.000|0.125 _±_0.000|
|_σ_CFG = 7|3.702 _±_0.118|9.195 _±_0.109|0.306 _±_0.013|0.489 _±_0.009|0.608 _±_0.010|4.094 _±_0.037|4.365 _±_0.369|8.323 _±_0.138|0.016|_±_0.000|0.127 _±_0.001|
|Steps= 3|3.755 _±_0.057|9.111 _±_0.164|0.309 _±_0.010|0.481 _±_0.011|0.608 _±_0.007|4.078 _±_0.017|4.786 _±_0.193|8.542 _±_0.144|0.017|_±_0.000|0.384 _±_0.001|
|Steps= 5 (Ours)|3.072 _±_0.199|9.220 _±_0.151|0.300 _±_0.007|0.481 _±_0.004|0.607 _±_0.008|4.272 _±_0.058|3.238 _±_0.430|8.226 _±_0.079|0.015|_±_0.001|0.125 _±_0.001|
|Steps= 7|3.451 _±_0.047|9.230 _±_0.078|0.308 _±_0.014|0.483 _±_0.007|0.616 _±_0.006|3.855 _±_0.012|4.913 _±_0.212|8.427 _±_0.114|0.017|_±_0.001|0.127 _±_0.002|
|Steps= 10|3.640 _±_0.072|8.951 _±_0.106|0.317 _±_0.008|0.497 _±_0.007|0.623 _±_0.007|3.858 _±_0.022|5.132 _±_0.309|8.350 _±_0.117|0.021|_±_0.000|0.133 _±_0.001|
|Rollout= 0|2.310 _±_0.112|8.540 _±_0.044|0.208 _±_0.003|0.349 _±_0.005|0.474 _±_0.015|5.936 _±_0.015|1.129 _±_0.159|8.087 _±_0.214|0.011|_±_0.000|0.123 _±_0.001|
|Rollout= 0_._4|2.461 _±_0.089|8.831 _±_0.074|0.262 _±_0.010|0.419 _±_0.017|0.543 _±_0.008|4.960 _±_0.040|2.525 _±_0.202|8.541 _±_0.102|0.015|_±_0.000|0.125 _±_0.000|
|Rollout= 0_._6|3.323 _±_0.016|9.198 _±_0.075|0.305 _±_0.017|0.479 _±_0.013|0.610 _±_0.006|4.176 _±_0.045|3.537 _±_0.201|8.386 _±_0.074|0.013|_±_0.001|0.124 _±_0.001|
|Rollout= 0_._8 (Ours)|3.072 _±_0.199|9.220 _±_0.151|0.300 _±_0.007|0.481 _±_0.004|0.607 _±_0.008|4.272 _±_0.058|3.238 _±_0.430|8.226 _±_0.079|0.015|_±_0.001|0.125 _±_0.001|
|Rollout= 1|4.008 _±_0.026|9.185 _±_0.137|0.315 _±_0.005|0.500 _±_0.008|0.624 _±_0.008|3.847 _±_0.006|4.363 _±_0.253|8.192 _±_0.062|0.018|_±_0.001|0.129 _±_0.003|


Fig. 7: **Additional results of continuous diverse skill execution in the real robot.** 

