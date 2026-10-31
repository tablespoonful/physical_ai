---
title: "Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control"
date: "2026-03-29"
authors: "Zelin Tao; Zeran Su; Peiran Liu; Jingkai Sun; Wenqiang Que; Jiahao Ma"
url: https://arxiv.org/abs/2603.27756
pdf: https://arxiv.org/pdf/2603.27756
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.27756)** / [論文ページ](https://arxiv.org/abs/2603.27756)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control** 


**X-Humanoid Heracles Project Team** 

# **Abstract** 

**Achieving general-purpose humanoid control requires a delicate balance between the precise execution of commanded motions and the flexible, anthropomorphic adaptability needed to recover from unpredictable environmental perturbations. Current general controllers predominantly formulate motion control as a rigid reference-tracking problem. While effective in nominal conditions, these trackers often exhibit brittle, non-anthropomorphic failure modes under severe disturbances, lacking the generative adaptability inherent to human motor control. To overcome this limitation, we propose Heracles, a novel state-conditioned diffusion middleware that bridges precise motion tracking and generative synthesis. Rather than relying on rigid tracking paradigms or complex explicit mode-switching, Heracles operates as an intermediary layer between high-level reference motions and low-level physics trackers. By conditioning on the robot’s real-time state, the diffusion model implicitly adapts its behavior: it approximates an identity map when the state closely aligns with the reference, preserving zero-shot tracking fidelity. Conversely, when encountering significant state deviations, it seamlessly transitions into a generative synthesizer to produce natural, anthropomorphic recovery trajectories. Our framework demonstrates that integrating generative priors into the control loop not only significantly enhances robustness against extreme perturbations but also elevates humanoid control from a rigid tracking paradigm to an open-ended, generative general-purpose architecture.** 

# **1. Introduction** 

Humanoid robots are rapidly transitioning from structured laboratory settings to complex, unstructured realworld environments. This shift demands general-purpose control architectures capable of executing precise, goal-directed motions while maintaining the flexible, anthropomorphic resilience characteristic of human motor control. In biological systems, motor behavior is rarely a rigid execution of a predefined plan; rather, humans seamlessly blend exact task execution with intuitive, generative recovery when faced with unexpected physical disturbances. Emulating this dual capability remains a formidable challenge in modern robotics. 

The prevailing paradigm for general-purpose humanoid control relies heavily on reference-driven tracking. Recent advancements formulate motion control primarily as a problem of minimizing the kinematic deviation between the robot’s current state and a provided reference trajectory. Powered by deep reinforcement learning, these tracking-based controllers He et al. (2025); Luo et al. (2025); Wang et al. (2026); Yin et al. (2025), such as those mimicking reference motions or utilizing universal trackers, excel in nominal conditions. They enable humanoids to faithfully replicate highly diverse sets of motion capture (MoCap) data, achieving impressive zero-shot execution for an array of highly agile and dynamic skills. 

However, formulating general control strictly as a rigid tracking objective introduces a critical vulnerability: catastrophic and non-anthropomorphic failure modes under severe environmental perturbations. When a robot is pushed far from its reference trajectory, a pure tracker blindly attempts to minimize the immediate state error, often resulting in rigid, physically infeasible joint torques that lead to unnatural and unrecoverable falls. Conversely, entirely dropping the tracking objective in favor of pure generative models Li et al. (2026); Zeng et al. (2025), such as end-to-end behavior cloning, yields more natural, human-like movements but 

© 2026 X-Humanoid All rights reserved. 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 


Figure 1: **Heracles synthesizes diverse, anthropomorphic recovery motions via state-conditioned diffusion.** In contrast to recovery policies trained with termination tricks that converge to a limited set of stereotypical maneuvers, Heracles leverages its generative middleware to produce a rich repertoire of agile, human-like recovery behaviors, enabling more general and robust responses across a wide range of extreme perturbations. 

fundamentally sacrifices the spatial and temporal precision required for strict task execution. A significant gap remains: bridging the exactitude of precise trackers with the generative adaptability of robust human recovery. 

To overcome this fundamental limitation, we propose Heracles, a novel state-conditioned diffusion middleware designed to bridge precise motion tracking and generative synthesis (Fig. 1). Rather than engineering a monolithic end-to-end controller or relying on complex, explicit state machines to switch between tracking and recovery modes, Heracles operates elegantly as an intermediary layer. Situated between the high-level original motion commands and the low-level physical execution policy, it injects powerful generative priors directly into the control loop without disrupting the high-frequency physics execution. 

The core innovation of Heracles lies in its implicit, state-driven adaptability. By tightly conditioning the diffusion process on the robot’s real-time physical state, the model dynamically shapes its output without explicit heuristics. When the robot’s state closely aligns with the reference command, the diffusion process approximates an identity map, allowing the commands to pass through with near-zero modification to preserve strict tracking 

2 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

fidelity. Conversely, when encountering significant state deviations—such as a severe push or an imminent fall—the model seamlessly transitions into a generative synthesizer. It synthesizes natural, anthropomorphic recovery trajectories that guide the underlying physics tracker back to stability. This mechanism not only enhances physical robustness but elevates humanoid control from a rigid tracking paradigm to an open-ended, generative architecture. 

In summary, the primary contributions of this work are three-fold: 

- **A Generative Control Middleware Paradigm:** We introduce Heracles, a novel state-conditioned diffusion middleware that uniquely bridges the precision of motion tracking with the flexibility of generative synthesis, effectively decoupling high-level intent generation from low-level physical execution. 

- **Enhanced Architecture for General-Purpose Control:** We improve the underlying physics tracker and the overall control framework to better serve general-purpose tasks. This optimized architecture ensures the retention of high-fidelity tracking characteristics while seamlessly integrating with the generative priors from the middleware. 

- **Robust Anthropomorphic Recovery and Motion Generalization:** We successfully deploy the proposed framework on physical humanoid robots. Extensive hardware experiments demonstrate emergent, humanlike recovery behaviors and robust generative adaptability under severe, out-of-distribution physical disturbances. 

# **2. Related Work** 

## **2.1. General Humanoid Motion Controller** 

Recent advances in deep reinforcement learning catalyze the development of general-purpose controllers for high-degree-of-freedom humanoid robots. These architectures aim to provide a unified execution policy for diverse motor behaviors, predominantly dividing into mimic-based reference trackers and unsupervised reinforcement learning (URL) methods. 

**Mimic-Based Motion Trackers.** A dominant paradigm formulates motor behavior execution as a highfidelity motion imitation task. Pioneered by DeepMimic Peng et al. (2018), which demonstrated that deep reinforcement learning can train physics-based characters to closely imitate reference motion clips, this paradigm has since been scaled to general-purpose humanoid control. Foundational large-scale frameworks, including the Generalized Motion Tracker (GMT) Chen et al. (2025), demonstrate that adaptive sampling and mixture-of-experts (MoE) architectures enable humanoids to track diverse motions via a single unified policy. Extending this paradigm, recent efforts structurally scale these models. SONIC Luo et al. (2025) expands network capacity and datasets to over 100 million frames, establishing motion tracking as a robust scalable foundation task. To break the representation bottleneck in multi-motion RL optimization, OmniXtreme Wang et al. (2026) introduces a flow-matching policy to decouple general motor skill learning from sim-to-real physical refinement. Beyond pure kinematic tracking, researchers continuously enhance the versatility and stability of these frameworks. HOVER He et al. (2025) employs multi-mode policy distillation to consolidate specific control modes—specifically navigation and loco-manipulation—into a unified controller. Concurrently, AMS Pan et al. (2026) proposes a hybrid reward scheme combining agile human MoCap data with physically constrained synthetic balance motions. More recently, BeyondMimic Liao et al. (2025) integrates a guided diffusion mechanism directly into the tracking formulation, allowing the system to solve diverse downstream tasks via classifier guidance. Beyond pure kinematics, Sun et al. (2024) pioneer the integration of large language models with adversarial imitation learning for zero-shot task execution through quantized skill representations. RoboGhost Li et al. (2026) integrates language-grounded motion latents from a motion generator with reinforcement learning for retarget-free whole-body controller. OmniRetarget Yang et al. (2025) incorporates human-scene interaction (HSI) and human-object interaction (HOI) constraints into the motion retargeting pipeline, improving the physical plausibility of transferred motions. Along similar lines, recent 

3 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

works have further advanced humanoid parkour-style locomotion Zhu et al. (2026); Zhuang et al. (2026) and contact-rich interaction tasks Lin et al. (2026). MeshMimic Zhang et al. (2026) further advances the paradigm by incorporating 3D scene reconstruction from monocular video, enabling humanoid robots to learn coupled motion-terrain interactions on complex, non-flat terrains. Despite these structural advancements, tracking-first controllers remain fundamentally anchored to their reference trajectories and typically require computationally expensive test-time guidance for generation. Under severe out-of-distribution physical perturbations, relying purely on the tracking formulation predominantly results in rigid, physically infeasible joint torques rather than seamless, real-time anthropomorphic recovery. 

**Unsupervised RL and Skill Discovery.** Conversely, unsupervised reinforcement learning (URL) and the emerging paradigm of Behavioral Foundation Models (BFMs) seek to equip robots with a diverse repertoire of motor skills devoid of explicit reference trajectories. Recent extensive surveys on BFMs Yuan et al. (2025) delineate a clear trajectory toward leveraging large-scale pre-training to capture broad behavioral priors. Zhang et al. (2024) extended this paradigm to full-size humanoid robots by developing an adversarial motion prior framework that achieves human-comparable whole-body locomotion performance. The foundational BFM framework Zeng et al. (2025) utilizes masked online distillation alongside Conditional Variational Autoencoders (CVAEs) to model behavioral distributions flexibly from unstructured data. Pushing the boundaries of autonomous exploration, cutting-edge URL approaches establish entirely reference-free policies. BFMZero Li et al. (2026) leverages unsupervised RL and Forward-Backward (FB) representations to create an objective-centric, promptable latent space, enabling a single generalist policy to perform zero-shot tasks and reward inference seamlessly in the real world. Several recent works Chen et al. (2026); Luo et al. (2024); Wang et al. (2025); Yu et al. (2025); Zhang et al. (2026) leverage motion tracking as a foundational mechanism to acquire human athletic skills, enabling humanoid robots to perform highly dynamic ball sports. Because these URL-driven policies and foundation models explore the state-action space unconstrained by rigid references, they inherently exhibit remarkable physical compliance and naturalistic robustness when perturbed. However, mapping these autonomously discovered, unconstrained latent spaces to high-precision, strict-fidelity spatial tracking tasks remains a formidable challenge. They fundamentally struggle to achieve the exactitude characteristic of dedicated mimic controllers in complex, dynamic execution scenarios. 

## **2.2. Motion Generation** 

Synthesizing diverse, naturalistic human movements represents a foundational pursuit within computer animation. Motion-X Lin et al. (2023) provides a large-scale multi-modal human motion dataset comprising over 81K motion sequences with unified whole-body annotations spanning face, hands, and body, while its successor Motion-X++ Zhang et al. (2025) further extends the scale and diversity by incorporating additional motion sources and richer semantic labels to support more comprehensive whole-body motion generation and understanding. Early paradigm shifts leveraged score-based generative models, with the Human Motion Diffusion Model (MDM) Tevet et al. (2023) establishing a robust transformer-based baseline for text-driven kinematic synthesis. Subsequently, researchers integrated motion generation into the Large Language Model (LLM) ecosystem. MotionGPT Jiang et al. (2023) first demonstrated that treating human motion as a foreign language and unifying motion-text tasks via discrete tokenization yields strong multi-task performance. Building upon this insight, MotionGPT-2 Wang et al. (2024) further quantizes multimodal inputs—including text and single-frame poses—into LLM-interpretable tokens for unified generation and understanding. Meanwhile, the MotionMillion framework Fan et al. (2025) demonstrates that million-scale high-quality datasets coupled with autoregressive architectures unlock unprecedented zero-shot capabilities. Expanding modality fusion, OmniMotion Li et al. (2025) utilizes a continuous masked autoregressive transformer to seamlessly integrate text, speech, and music into a cohesive whole-body generation mechanism. Pushing model capacity limits, HY-Motion 1.0 Wen et al. (2025) successfully scales diffusion transformer-based flow matching models to the billion-parameter regime, yielding instruction-following digital animations with unparalleled fidelity. Despite achieving remarkable anthropomorphism and diversity, these generative foundation models fundamentally 

4 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

operate in an open-loop, pure kinematic domain. They synthesize trajectories comprising joint angles and global translations completely devoid of physical constraints. Implementing these raw kinematic outputs directly on a physical humanoid invariably triggers dynamics mismatches, leading to instability and falls, because the generative process ignores crucial embodied parameters including joint torque limits, contact friction, and center-of-mass dynamics. 

## **2.3. Hybrid Architectures for Motion Tracking and Synthesis** 

To overcome the inherent limitations of isolated physical trackers and open-loop generative models, recent research actively constructs hybrid architectures integrating generative synthesis with tracking objectives. Within the kinematic domain, frameworks attempt to constrain generation via tracking formulations; COMET Lee et al. (2025) employs a conditional VAE framework with a reference-guided feedback loop to prevent long-term motion degradation, while MotionStreamer Xiao et al. (2025) and DART Zhao et al. (2024) enforce sequential synthesis driven by rigorous spatial constraints. Transitioning to physically simulated characters, building upon the foundational reference-tracking paradigm of DeepMimic Peng et al. (2018), Adversarial Skill Embeddings (ASE) Peng et al. (2022) constructs continuous latent spaces from large-scale unstructured motion data, enabling characters to maintain highly anthropomorphic behaviors during diverse downstream tasks. Advancing this trajectory, the Versatile Motion Priors (VMP) framework Serifi et al. (2024) optimizes the robust control of physical characters by distilling multipurpose motion priors through a two-stage variational approach, significantly enhancing both reference trajectory tracking and resilience against external perturbations. Recent investigations further deepen this paradigm: AMOR Alegre et al. (2025) proposes multi-objective reinforcement learning to train weight-conditioned policies spanning the Pareto front of reward trade-offs, while adversarial differential discriminators Zhang et al. (2025) eliminate the need for manually-designed reward functions in physics-based motion imitation. In the multi-agent competitive domain, RoboStriker Yin et al. (2026) constructs a hierarchical framework that decouples high-level strategic reasoning from low-level physical execution via topologically constrained latent manifolds, demonstrating emergent boxing behaviors with sim-to-real transfer. However, these hybrid control paradigms retain structural deficiencies when confronting extreme, out-of-distribution physical disturbances. They typically couple high-level generative priors with low-level execution policies loosely, preventing high-frequency physical state deviations from reshaping the generative target in real time. Consequently, when encountering severe imbalance, the system fails to transition implicitly from nominal tracking to generative recovery, often reverting to rigid, explicit state-switching mechanisms. Our proposed Heracles framework resolves this bottleneck through a state-conditioned diffusion middleware that dynamically modulates the generative output based on real-time state deviations, achieving a seamless unification of precise zero-shot tracking and anthropomorphic generative recovery within a closed control loop. 

# **3. Method** 

## **3.1. System Overview and Problem Formulation** 

General humanoid control requires executing desired motion commands while maintaining physical balance against unpredictable environmental disturbances. We formulate this dual objective—high-fidelity motion tracking and robust physical recovery—within a hierarchical control architecture. The proposed framework, Heracles, intrinsically decouples high-level intent generation from high-frequency physical execution (Fig. 2). It comprises two primary components: a state-conditioned generative middleware and a low-level, generalpurpose physics tracking policy. 

In standard tracking paradigms Chen et al. (2025); Luo et al. (2025); Peng et al. (2018), a policy minimizes the kinematic deviation between the robot’s real-time proprioceptive state **p** _𝑡_ and a reference motion command **m** _𝑡_ . When the state remains close to the reference manifold, directly tracking **m** _𝑡_ yields optimal zero-shot performance. However, when severe physical perturbations push the state into out-of-distribution (OOD) 

5 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 


Figure 2: **Overview of the Heracles framework. (a)** A flow matching model _𝐷_<sup>^</sup> _𝜃_ learns to synthesize feasible keyframe trajectories conditioned on the current state. **(b)** Reference motions are quantized into discrete tokens via FSQ, shared by reconstruction and action prediction heads. **(c)** At inference, the middleware generates trajectories through closed-loop replanning for the motion tracker to execute. 

regions, forcing strict adherence to **m** _𝑡_ produces rigid, myopic corrective actions that lack the coordinated multi-step reasoning required for physical recovery, invariably precipitating catastrophic failure. 

To resolve this limitation, we formulate the core problem as learning an intermediary mapping that dynamically modulates the reference command based on real-time physical feasibility. The generative middleware functions as this state-conditioned trajectory synthesizer. Operating at a lower planning frequency, it observes the current state **p** _𝑡_ and the original reference **m** _𝑡_ , predicting a short-horizon, dynamically feasible keyframe trajectory: 


where _𝐾_ denotes the number of keyframes and _𝐷_ represents the state dimension. This mapping design unifies nominal tracking and OOD recovery: when the robot operates near the reference manifold, _𝑓𝜃_ approximates an identity transformation to preserve high-fidelity tracking; conversely, under large disturbances, _𝑓𝜃_ synthesizes entirely new, physically feasible transition trajectories that guide the robot back toward the reference manifold. 

The synthesized keyframes **_𝜏_** _𝑡_ are subsequently densified and written into a reference buffer consumed by the low-level physics tracker. We model this continuous tracking process as a discounted Markov decision process (MDP) defined by the tuple _ℳ_ = ( _𝒮, 𝒜, 𝒫, 𝑟, 𝛾_ ). At each high-frequency control step, the tracking policy _𝜋_ receives an observation: 


where **m**<sup>_′_</sup> _𝑡_<sup>denotes the modulated reference commands sampled from the densified</sup><sup>**_𝜏_**</sup><sup>_𝑡_, and</sup><sup>**z**</sup><sup>_𝑑_constitutes a</sup> high-level motion embedding (detailed in Sec. 3.3). The policy outputs joint-level actions _𝑎𝑡 ∈𝒜_ to maximize the expected discounted return: 


where _𝑟𝑡_ represents a task reward composed of tracking precision and physical regularization terms. Deployment follows a receding-horizon replanning loop. Every _𝑁_ exec control steps, the middleware updates **_𝜏_** _𝑡_ from the 

6 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

latest proprioceptive observation, while the tracking policy executes the dense trajectory at the fundamental control frequency, forming a seamless, closed-loop tracking-generation architecture. 

## **3.2. State-Conditioned Generative Middleware via Flow Matching** 

We formulate the trajectory generation process as a conditional flow matching problem over a geometrically constrained residual space, bridging exact motion tracking and generative synthesis without relying on explicit mode-switching heuristics. 

**Geometric Residual Parameterization.** Directly predicting absolute state coordinates wastes model capacity on approximating the identity mapping during near-nominal execution. Instead, we predict residual trajectories relative to the current state. Let **_𝛽_** _𝑡_ denote the static baseline anchored at the current proprioceptive state: 


The middleware predicts only the residual deviation **r** _𝑡_ , recovering the final trajectory as: 


Under this parameterization, the residual directly encodes the motion increment from the current state over the planning horizon. When the robot closely follows the reference manifold ( **p** _𝑡 ≈_ **m** _𝑡_ ), the synthesized trajectory closely reproduces the original reference motion, and the middleware effectively acts as an identity map on the command signal. Under severe deviations, the model leverages the conditioning gap between **p** _𝑡_ and **m** _𝑡_ to synthesize recovery trajectories that diverge from the reference in favor of physical plausibility. Crucially, the target command **m** _𝑡_ enters exclusively through the conditioning vector, ensuring that the residual prediction target remains independent of the state-command distance. 

**Continuous Conditional Flow Matching.** To synthesize the complex, multimodal distributions of these recovery residuals, we employ continuous flow matching Lipman et al. (2023). Let **x** 0 denote the normalized ground-truth residual data and **x** 1 _∼𝒩_ (0 _,_ **I** ) represent the prior Gaussian noise. We define a probability path via linear interpolation: 


The model is trained to regress the underlying continuous vector field by minimizing the velocity matching objective: 


where **c** _𝑡_ = [ **p** _𝑡,_ **m** _𝑡_ ] serves as the strict state-conditioning vector. During inference, physically viable recovery trajectories are sampled by integrating the learned velocity field **v** ˆ from _𝑡_ = 1 to _𝑡_ = 0 utilizing a minimal number of Euler steps. 

**Architecture and Kinematic Continuity.** The velocity field is parameterized by an AdaLN-modulated Transformer Peebles and Xie (2023), where the conditioning vector **c** _𝑡_ and the flow timestep embedding are injected into each block via adaptive shift-scale-gate modulation. To guarantee kinematic continuity between the realtime physical state and the synthesized trajectory, we pin the first residual token via an inpainting constraint during integration: 


where **r** 0 strictly defines the zero-residual anchor corresponding to the initial state. 

**Receding-Horizon Planning with Directional Warm Start.** A key design principle is that the middleware always predicts a fixed temporal window of motion, regardless of the distance to the target command. The target is set to the current reference frame **m** _𝑡_ , and both the temporal window ∆ _𝑡_ and execution interval _𝑁_ exec are held constant. Whether the robot is closely tracking the reference or operating far from the reference 

7 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

manifold, the generated keyframes consistently encode the next ∆ _𝑡_ seconds of motion. Long-horizon recovery emerges autoregressively through successive replan cycles, rather than requiring the model to reason about the full trajectory in a single pass. 

During inference, we initialize the ODE solver with a directional motion prior rather than pure Gaussian noise. We construct an initial residual trajectory linearly interpolating toward the target: 


and begin ODE integration from a partially noised version of this prior at _𝑡_ start _<_ 1: 


where _𝑡_ start controls the noise-to-prior ratio. Inspired by SDEdit Meng et al. (2022), this warm start provides the linear prior as an immediate directional estimate, while the learned velocity field refines it into a natural trajectory within a reduced number of ODE steps. The resulting _𝐾_ keyframes are then densified into the tracker’s operating frequency via cubic spline interpolation for joint positions and spherical linear interpolation for root orientations, yielding the complete dense reference signal consumed by the tracking policy. 

## **3.3. General-Purpose Physics Tracker** 

### **3.3.1. Motion Tracking Formulation** 

**Observation Space.** The observation space is formally defined as a composite vector **o** _𝑡_ = _{_ **p** _𝑡,_ **m** _𝑡,_ **z** _𝑑}_ , comprising the robot’s proprioceptive state **p** _𝑡_ , the kinematic motion reference trajectory **m** _𝑡_ , and the discrete high-level motion embedding **z** _𝑑_ . Specifically, the proprioceptive state **p** _𝑡_ encapsulates the immediate physical condition of the robot: 


where **g** _𝑡_<sup>proj</sup> _∈_ R<sup>3</sup> denotes the gravity vector projected into the local root frame, **_𝜔_** _𝑡 ∈_ R<sup>3</sup> represents the root angular velocity, **q** _𝑡 ∈_ R<sup>29</sup> and **q** ˙ _𝑡 ∈_ R<sup>29</sup> represent the current joint positions and velocities respectively, **q** 0 defines the default nominal joint configuration, and **a** _𝑡−_ 1 _∈_ R<sup>29</sup> records the previous action to ensure temporal smoothness. 

The reference observation **m** _𝑡_ provides per-step target kinematics: 


During training, **m** _𝑡_ is extracted directly from the motion dataset. At deployment, it is seamlessly replaced by the densified middleware output **m**<sup>_′_</sup> _𝑡_<sup>without any modification to the tracker architecture.Here,</sup><sup>**v**</sup> _𝑡_<sup>ref</sup> _∈_ R<sup>3</sup> and **_𝜔_** _𝑡_<sup>ref</sup> _∈_ R<sup>3</sup> denote the reference root linear and angular velocities expressed in the body frame, **q**<sup>ref</sup> _𝑡 ∈_ R<sup>29</sup> specifies the target joint positions. The root orientation error **e**<sup>root</sup> _𝑡 ∈_ R<sup>6</sup> is strictly parameterized using a 6D continuous rotation feature (Rot6D), computed from the first two columns of the relative rotation matrix _𝑅_ root<sup>des</sup><sup>_𝑅_</sup> root<sup>_⊤_.The discrete motion token</sup><sup>**z**</sup><sup>_𝑑_captures temporally coherent, high-level motion semantics and is</sup> detailed in the subsequent policy architecture description. 

**Action Space.** The policy _𝜋_ outputs target joint positions **a** _𝑡 ∈_ R<sup>29</sup> . Each physical joint tracks these respective targets utilizing a low-level Proportional-Derivative (PD) controller operating at high frequency, ensuring stable torque generation. 

**Rewards and Domain Randomization.** The reward combines positive tracking terms—covering root velocities, body-link orientations, and joint-position matching—with regularization penalties on action jerks, joint-limit violations, and undesired contacts (Tab. 1a). To ensure sim-to-real transferability, we inject comprehensive 

8 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

domain randomization during training, perturbing both the simulator’s physical properties (friction, center-ofmass offsets) and the command-level kinematic targets (Tab. 1b). 

Table 1: **Training configuration for the general-purpose physics tracker.** Left: reward function with exponential tracking terms and regularization penalties. Right: domain randomization ranges for command-level, physical, and external disturbance parameters. 

|(a) Reward function. Trackin|g: _𝑟𝑖_=|_𝑤𝑖_exp<br>(<br>_−‖𝑒𝑖‖_<sup>2</sup>_/𝜎_<sup>2</sup><br>_𝑖_<br>)<br>.|(b) Domain randomization r|anges.|
|---|---|---|---|---|
|**Tracked Quantity**|**_𝑤_**|**_𝜎_**|**Parameter**|**Range**|
|Root Position|0_._1|0_._30|_Command-level perturba_|_tions_|
|Root Orientation|0_._5|0_._40|Target Joint Pos. (rad)|_±_0_._01|
|Root Linear Vel.|1_._0|0_._50|Target Ang. Vel. (rad/s)|_±_0_._2|
|Root Angular Vel.|1_._0|1_._00|Target Root Rot. (rad)|_±_0_._05|
|Rel. Body Position|1_._0|0_._30|Default Joint Pos. (rad)|_±_0_._01|
|Rel. Body Orientation<br>|1_._0|0_._40|_Physical properties_||
|Body Linear Vel.<br>|1_._0|1_._00<br>|<br>CoM Offset (m)|_𝑥_: _±_0_._5; _𝑦, 𝑧_: _±_0_._1|
|Body Angular Vel.|1_._0|_~~√~~_<br>_𝜋_|Static Friction|[0_._3_,_ 1_._6]|
|**Regularization**|**_𝑤_**|**Penalty**|Dynamic Friction|[0_._3_,_ 1_._2]|
|Action Rate<br>Joint Limit<br>Undesired Contacts|_−_0_._1<br>_−_10<br>_−_0_._1|_‖𝑎𝑡−𝑎𝑡_-1_‖_<sup>2</sup><br>∑︀max(0_, 𝑞−𝑞_lim)<br>∑︀⊮(_𝐹𝑐>_1)|_External disturbances_<br>Push Frequency (s)<br>Push Lin. Vel. (m/s)<br>Push Ang. Vel. (rad/s)|1_._0–3_._0<br>_𝑥𝑦_: _±_0_._5; _𝑧_: _±_0_._2<br>_𝑅𝑃_: _±_0_._52; _𝑌_: _±_0_._78|


### **3.3.2. General Motion Tracking Policy** 

Our tracking policy is built on a shared motion-latent representation with an encoder–quantizer–decoder structure. A motion encoder maps the kinematic observations **m** _𝑡_ to a continuous latent **z** _𝑐_ , which is then discretized into tokenized codes **z** _𝑑_ . Two parallel heads consume **z** _𝑑_ : a reconstruction decoder for representation learning, and an action decoder that fuses **z** _𝑑_ with the proprioceptive state **p** _𝑡_ to produce control actions. 

**Improved Discrete Quantization.** We adopt an improved Finite Scalar Quantization (iFSQ) Lin et al. (2026) to distill high-frequency kinematic signals into compact semantic tokens. Given continuous latent features **z** _𝑐 ∈_ R<sup>_𝑁×𝑑_</sup> , with _𝑁_ the batch size and _𝑑_ the embedding dimension, each channel is bounded to [ _−_ 1 _,_ 1] and quantized into _𝐿_ = 2<sup>_𝐾_</sup> + 1 uniformly spaced levels, where the extra center level guarantees an exact zero-state. Element-wise quantization maps each dimension to an integer index _𝑧𝑑 ∈{_ 0 _, . . . , 𝐿 −_ 1 _}_ via: 


Rather than the standard tanh bounding, we employ a sigmoid-based mapping that improves bin utilization while preserving uniform quantization intervals: 


We apply the straight-through estimator (stop-gradient) for the rounding operation, yielding the discrete tokens **z** _𝑑_ injected into the policy observation. 

**Encoder-Decoder Architecture.** The motion encoder ingests a 10-frame future window **M** _𝑡_ : _𝑡_ +9 and produces a continuous embedding **z** _𝑐 ∈_ R<sup>_𝑑_</sup> . After iFSQ discretization, the reconstruction decoder maps **z** _𝑑_ back to the full 10-frame motion sequence **M**<sup>ˆ</sup> _𝑡_ : _𝑡_ +9, optimized via: 


The action decoder concatenates **z** _𝑑_ with a 10-step proprioceptive history **P** _𝑡−_ 9: _𝑡_ to produce the control action **a** _𝑡_ . 

9 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

**Adaptive Motion Sampling.** Training a unified policy over a large, heterogeneous motion corpus introduces severe optimization imbalance: uniform sampling overfits to trivial locomotion while underperforming on dynamic, agile skills. Inspired by the bin-level adaptive curriculum in ZEST Sleiman et al. (2026), we design a continuous temporal-bin variant with smoothed difficulty propagation. 

We partition the concatenated motion corpus into _𝐵_ uniformly spaced temporal bins. At each episode termination, the per-step tracking score _𝑠𝑡 ∈_ [0 _,_ 1] is averaged over the episode to yield a difficulty estimate _𝑑_ = 1 _− 𝑠_ ¯, which is accumulated into the corresponding bin via exponential moving average: 


where _𝐹𝑏_ denotes the difficulty of bin _𝑏_ and _𝛼_ controls the update rate. To prevent isolated hard bins from dominating the sampling distribution and to propagate difficulty to temporally adjacent regions, we apply a 1D kernel smoothing operation followed by an outlier cap: 


where _𝒦_ is an exponentially decaying kernel and _𝑐_ bounds the maximum bin weight relative to the global mean _𝐹_ ¯. The final sampling distribution mixes the smoothed difficulty with a uniform baseline to ensure exploration: 


where _𝜂_ controls the balance between difficulty-driven and uniform sampling. This mechanism continuously steers the training distribution toward challenging temporal regions of the motion manifold, while the kernel smoothing ensures that difficulty information propagates to neighboring segments, preventing abrupt sampling discontinuities. 

## **3.4. Training Paradigm for Unified Tracking and Generation** 

**Dataset Construction.** Training tuples for the state-conditioned middleware are generated from a diverse motion corpus using a receding-horizon sampling strategy. For each motion sequence, segment starting points are selected at regular intervals, and the temporal segment length _ℓ_ is drawn from a log-uniform distribution: 


where _ℓ_ min = _𝐻_ is set equal to the planning horizon. From each segment, _𝐾_ uniformly spaced keyframes are extracted covering only the first _𝐻_ frames (corresponding to ∆ _𝑡_ = _𝐻/_ fps seconds), regardless of the total segment length. The conditioning vector **c** _𝑡_ = [˜ **p** _𝑡,_ **m** _𝑡_ ] pairs the start state with the reference command at the segment endpoint. The residual supervision is computed against the static baseline **_𝛽_** _𝑡,𝑘_ = **p** ˜ _𝑡_ (Eq. (5)), so each training target encodes the motion increment over the next ∆ _𝑡_ seconds from the current state. This design ensures that (i) the model never needs to predict trajectories exceeding a fixed temporal horizon, bounding the residual magnitude regardless of the state-command gap; (ii) training naturally covers every phase of long recovery sequences, as successive starting points within the same motion yield overlapping local windows; and (iii) eliminating near-zero-length segments ( _ℓ< 𝐻_ ) removes the trivial zero-residual bias that otherwise dominates under mean-squared-error training. 

**Noisy-State Augmentation.** Deployment introduces a systematic discrepancy between noisy physical state estimation and the clean reference commands available during training. To close this gap, we apply asymmetric start-state perturbations: only the initial proprioceptive state is corrupted with channel-wise Gaussian noise, 


10 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

while the target reference command remains clean. The noise magnitude is scaled per channel to reflect the varying sensitivity of different state dimensions. This asymmetric augmentation mirrors the deployment scenario where the robot’s proprioceptive state reflects both sensor noise and accumulated tracking errors, while the reference command is always clean, improving robustness to real-world state-command discrepancies. 

**Kinematics-Aware Loss Weighting.** Beyond the primary velocity matching objective (Eq. (7)), we introduce a kinematics-aware weighting scheme motivated by the observation that identical joint-space errors can induce vastly different body-space deviations depending on the current kinematic configuration. Concretely, we weight each state dimension _𝑞𝑑_ by a pose-dependent Jacobian magnitude: 


where **p** _𝑏_ is the Cartesian position of tracked body link _𝑏_ . This approximates the diagonal of **J**<sup>_⊤_</sup> **J** evaluated independently at each training pose and keyframe, producing a weight tensor of shape ( _𝑁, 𝐾, 𝐷_ ). This captures pose-dependent lever arm geometry: for example, a shoulder joint in a T-pose configuration commands a longer moment arm than when the arm hangs at rest, and receives a correspondingly larger gradient signal. The weights are normalized to unit mean per dimension and clamped to a minimum value to prevent zero-gradient dimensions. In practice, all weights are precomputed via differentiable forward kinematics during dataset construction and cached alongside training tuples, eliminating all online overhead. 

**State Representation and Model Variants.** We evaluate two state parameterizations: a 38D configuration comprising joint positions (29D), root position (3D), and root orientation in 6D continuous rotation representation, and a 35D variant omitting the global root position. The 38D formulation enables the middleware to synthesize root translational commands, allowing the robot to autonomously correct global positional drift relative to the reference trajectory. The 35D variant delegates root translation entirely to the reference motion, decoupling the middleware from global localization. While this sacrifices autonomous position correction, it eliminates dependence on external positioning systems, making it directly deployable with onboard proprioception and IMU alone. Both configurations retain equivalent fall recovery and general motion tracking performance. All quantitative results reported in this work use the 38D configuration unless otherwise noted. 

# **4. Experiments** 

## **4.1. Implementation Details** 

**Simulation Environment.** All experiments are conducted on the Unitree G1 humanoid platform, a full-size bipedal robot standing approximately 1.32 m tall with a total mass of roughly 35 kg. The robot features 29 actuated degrees of freedom spanning the torso, two 7-DoF arms, and two 6-DoF legs, all driven by proprietary electric actuators. Training is carried out in IsaacLab Mittal et al. (2025), a GPU-accelerated simulator built on NVIDIA Isaac Sim, where we instantiate 16,384 parallel environments on a single NVIDIA A100 (80 GB) GPU. The physics simulation runs at a 5 ms timestep (200 Hz) on flat ground with randomized friction coefficients (Tab. 1b), while the control policy queries observations and emits actions at 50 Hz (every 4 simulation substeps). Each action is converted to joint torques by a per-joint PD controller executing at the full 200 Hz rate. For evaluation, all policies are tested in the MuJoCo physics engine on a held-out set comprising 101 unseen motion sequences that span locomotion, dance, martial arts, daily activities, fall-and-recovery, acrobatic jumps, and discretized motion clips in which continuous reference trajectories are replaced with piecewise-constant signals consisting of static poses separated by abrupt transitions, thereby removing all smooth interpolation and testing the policy’s ability to track discontinuous commands. Each sequence is rolled out for its full duration (up to 20 s). 

**Motion Dataset.** The training corpus is curated from diverse, complementary sources, comprising selected clips from LAFAN1 Harvey et al. (2020), 100STYLE Mason et al. (2022), SnapMoGen Guo et al. (2025), 

11 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

AMASS Mahmood et al. (2019), and proprietary in-house motion capture recordings. The assembled dataset spans locomotion, martial arts, dance, daily activities, fall-and-recovery sequences, and jumping motions, thereby providing broad stylistic and temporal coverage for evaluating tracking fidelity, robustness, and execution stability under heterogeneous motion commands. 

**Tracker Training.** The general-purpose physics tracker is trained via Proximal Policy Optimization (PPO) within an asymmetric actor–critic framework, following established practices in prior whole-body tracking systems Li et al. (2026); Liao et al. (2025); Luo et al. (2025). The iFSQ encoder, reconstruction decoder, and action decoder are trained jointly end-to-end with the PPO objective, where the reconstruction loss (Eq. (15)) and the RL policy gradient share the same encoder–quantizer pathway. The adaptive motion sampling curriculum (Eq. (18)) is activated after an initial warm-up phase to allow early-stage uniform coverage. The complete reward function and domain randomization ranges are specified in Tab. 1; all remaining hyperparameters are listed in Tab. 2. 

**Trajectory Generator Training.** The state-conditioned flow matching trajectory generator is trained offline on paired trajectory tuples extracted from the motion corpus following the dataset construction procedure described in Eq. (19). The velocity field **v** ˆ is parameterized by an AdaLN-modulated Transformer Peebles and Xie (2023) that predicts _𝐾_ =8 uniformly spaced keyframes over a fixed planning horizon of ∆ _𝑡_ =0 _._ 2 s. We train two state representation variants: a **38D** configuration encoding 29 joint positions, 3D root position, and 6D root orientation, and a **35D** variant that omits root position entirely. The 38D model retains full awareness of global positioning, enabling recovery toward the reference command manifold in both pose and location. The 35D model relies solely on joint encoders and an IMU for root orientation, making it directly deployable on hardware without external localization; global position tracking is delegated to the reference motion source. We optimize the velocity matching objective (Eq. (7)) jointly with the kinematics-aware loss weighting (Eq. (21)). Noisy-state augmentation (Eq. (20)) is applied throughout training with channel-wise Gaussian noise with reduced magnitudes for root pose and orientation channels. During deployment, trajectory samples are generated via 5 Euler integration steps from _𝑡_ =0 _._ 9 to _𝑡_ =0, initialized with the directional warm start (Eq. (10)) at _𝑡_ start=0 _._ 9. The generator replans every _𝑁_ exec=2 control steps (0.04 s), yielding a closed-loop replanning frequency of 25 Hz. Full hyperparameters for both the tracker and the trajectory generator are listed in Tab. 2. 

Table 2: **Training hyperparameters for the physics tracker and the trajectory generator.** Left: PPO-based tracker training configuration. Right: flow matching trajectory generator architecture, optimization, and inference settings. 

|**Tracker Hyperparameter**|**Value**|**Generator Hyperparameter**|**Value**|
|---|---|---|---|
|Parallel environments|16,384|Attention blocks / heads / dim|6 / 4 / 512|
|Rollout horizon|24 steps|Conditioning injection|AdaLN (**c**_𝑡_=[**p**_𝑡,_**m**_𝑡_]+ timestep)|
|Discount factor_𝛾_|0.99|Keyframes_𝐾_/ horizonΔ_𝑡_|8 / 0.2 s|
|GAE_𝜆_|0.95|State dimension_𝐷_|38 / 35|
|PPO epochs / mini-batches|5 / 4|Optimizer|AdamW (_𝛽_1=0_._9,_𝛽_2=0_._999)<br>|
|Clipping ratio_𝜖_|0.2<br>|Learning rate|1_×_10<sup>_−_4 </sup>(cosine decay)<br>|
|Actor learning rate|2_×_10<sup>_−_3</sup><br>|Weight decay|10<sup>_−_4</sup>|
|Critic learning rate|1_×_10<sup>_−_3</sup>|Batch size|256|
|KL target|0.01|Training epochs|4,000|
|Entropy coefficient|0.005|Parameters|22.9 M|
|Gradient clip norm|1.0|Inference ODE steps|5 (Euler,_𝑡_: 0_._9_→_0)|
|Total training iterations|_∼_100,000|Warm-start_𝑡_start|0.9|
|||Replan interval_𝑁_exec|2 steps (0.04 s, 25 Hz)|


## **4.2. Comparisons** 

We evaluate eight model configurations that systematically vary four design axes—policy architecture, motion tokenizer, observation design, and generative trajectory planning—to isolate the contribution of each component. All variants share the same simulator, robot morphology, reward function, and training budget, and are evaluated 

12 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

### on the identical held-out motion set. 

**Compared Methods.** All policies receive a 10-frame proprioceptive history and a 10-frame future motion reference window (frames _𝑡_ through _𝑡_ +9) unless otherwise noted. We organize the evaluated methods into two groups; detailed network architecture specifications are provided in Tab. 3. 

_Architecture and external baselines._ **MLP** employs a standard MLP actor–critic with BeyondMimic-style (BM) observations Liao et al. (2025). **Transformer** follows the TokenHSI architecture Pan et al. (2025), encoding proprioceptive and motion inputs into per-modality tokens that are processed by a multi-head Transformer with a learnable aggregation token before an MLP action head. **VQ-VAE** replaces the iFSQ quantizer with a VQ-VAE tokenizer Sun et al. (2024) while retaining the same encoder–decoder policy structure. **SONIC** Luo et al. (2025) is reproduced from its official open-source release with the original observation design. 

_Heracles variants._ **iFSQBM** pairs the iFSQ tokenizer and encoder–decoder policy with BeyondMimic observations augmented by height features (BM+H), isolating the tokenizer contribution under a standard observation design. **iFSQ+H** combines the iFSQ-based policy with the proposed observation design (Sec. 3.3) including explicit height features. **iFSQ** uses the proposed observation design without height, representing the best standalone tracker configuration. **Heracles** augments the iFSQ tracker with the state-conditioned trajectory generator (Eq. (1)), constituting the full proposed system. 

**Evaluation Protocol.** All methods are evaluated on the same held-out set of 101 motion sequences unseen during training, spanning locomotion, dance, martial arts, daily activities, and fall-and-recovery. Each sequence is rolled out for its full duration (up to 20 s). We report five metrics: (i) _Completion Rate (CR)_ —the fraction of reference frames for which the policy maintains a root height error below 0.3 m and a root orientation error below 1.2 rad; (ii) _Joint Position Error_ —the _𝐿_ 2 norm of joint-position deviations; (iii) _Root Height Error_ — absolute height deviation in the world frame; (iv) _Root Orientation Error_ —orientation error excluding yaw; and (v) _Root Linear Velocity Error_ —velocity error in the body frame. 

Table 3: **Network architecture specifications for all evaluated methods.** [ _·_ ] denotes MLP hidden-layer widths. iFSQ _*_ covers all iFSQ variants (iFSQBM, iFSQ+H, iFSQ), which share the same network but differ in observation design. 

|**Method**|**Component**|**Configuration**|
|---|---|---|
|MLP|Actor<br>Critic|[4096_,_2048_,_1024_,_512_,_256]MLP<br>[4096_,_2048_,_1024_,_512_,_256]MLP|
|Transformer|Tokenizer<br>Backbone<br>Action head<br>Critic|[512_,_512]MLP_×_2modalities_→_3 tokens (512-dim)<br>3-layer, 4-head, 512-dim Transformer<br>[2048_,_1024_,_256]MLP<br>[3072_,_1536_,_768_,_512]MLP|
|VQ-VAE|Quantizer<br>Policy|Codebook_|𝒞|_=10_,_240, dim=512<br>Enc-Dec (identical to iFSQ)|
|SONIC|–|Official releaseLuo et al.(2025); stride-5 reference sampling|
|iFSQ_*_|Policy|iFSQ Enc-Dec (Sec. 3.3)|
|Heracles|Tracker<br>Traj. gen.|iFSQ Enc-Dec (Sec. 3.3)<br>6-layer, 4-head, 512-dim AdaLN TransformerPeebles and Xie(2023)|


**Results.** Tab. 4(a) summarizes the component configuration of each variant, and quantitative tracking performance is reported in Tab. 4(b). We highlight four principal findings. 

_Robustness._ The three variants equipped with the proposed observation design and iFSQ tokenizer (iFSQ+H, iFSQ, Heracles) consistently outperform all baselines in completion rate, achieving 87.3%, 87.2%, and 90.6% respectively. Heracles attains the highest completion rate, exceeding the best external baseline VQ-VAE (86.0%) by 4.6 percentage points and MLP (84.8%) by 5.8 points. Among external baselines, completion rates range from 79.3% (SONIC) to 86.0% (VQ-VAE). Switching from BM to the proposed observation design while keeping 

13 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

### Table 4: **Component configuration and quantitative comparison of all evaluated methods. (a)** Obs. 

column: BM = BeyondMimic-style Liao et al. (2025); _†_ = proposed (Sec. 3.3); +H = with height features. ✓/✗ indicates presence or absence of the trajectory generator. **(b)** Completion rate measures the fraction of reference frames for which the root height error remains below 0.3 m and the root orientation error stays below 1.2 rad; tracking errors are reported for joint positions, root height, root orientation (excl. yaw), and root linear velocity. <mark>Blue</mark> cells mark the best result per metric. Colored percentages show relative change from MLP: teal = better, red = worse. 

|||**(a)**Comp i|onent config|iuration|||
|---|---|---|---|---|---|---|
||**Metho**|**d**<br>**Obs.**|**Tokenizer**|**Policy**|**Traj. Gen.**||
||MLP<br>Transf<br>VQ-VA<br>SONIC|BM<br>ormer<br>BM<br>E<br>BM<br><br>SONIC|–<br>–<br>VQ<br>–|MLP<br>Trans.<br>Enc-Dec<br>SONIC|✗<br>✗<br>✗<br>✗||
||iFSQBM<br>iFSQ+<br>iFSQ<br>Heracl|BM+H<br>H<br>_†_+H<br>_†_<br>es<br>_†_|iFSQ<br>iFSQ<br>iFSQ<br>iFSQ|Enc-Dec<br>Enc-Dec<br>Enc-Dec<br>Enc-Dec|✗<br>✗<br>✗<br>✓||
|||**(b)**Trac|king perfor|mance|||
|**Method**|**CR**<br>(%)_↑_|**Joint Err**<br>(rad)_↓_|**Heigh**<br>(m)|**t Err**<br>_↓_|**Ori Err**<br>(rad)_↓_|**LinVel Err**<br>(m/s)_↓_|
|MLP|84_._8|**1**_._**1572**|0_._11|94|0_._3590|0_._2230|
|Transformer|80_._6(_−_5_._0%)|1_._5436(_−_33_._4%)|0_._1426(_−_|19_._4%)|0_._3410(+5_._0%)|0_._2046(+8_._3%)|
|VQ-VAE|86_._0(+1_._4%)|2_._3013(_−_98_._9%)|0_._1077(|+9_._8%)|0_._3675(_−_2_._4%)|0_._2376(_−_6_._5%)|
|SONIC|79_._3(_−_6_._5%)|1_._9828(_−_71_._3%)|0_._1402(_−_|17_._4%)|0_._3771(_−_5_._0%)|0_._2334(_−_4_._7%)|
|iFSQBM|85_._1(+0_._4%)|1_._4760(_−_27_._5%)|0_._1096(|+8_._2%)|0_._3474(+3_._2%)|0_._2362(_−_5_._9%)|
|iFSQ+H|87_._3(+2_._9%)|1_._2924(_−_11_._7%)|**0**_._**0271**(|+77_._3%)|**0**_._**1539**(+57_._1%)|0_._1709(+23_._4%)|
|iFSQ|87_._2(+2_._8%)|1_._1863(_−_2_._5%)|0_._0955(+|20_._0%)|0_._3614(_−_0_._7%)|**0**_._**1561**(+30_._0%)|
|Heracles|**90**_._**6**(+6_._8%)|1_._3272(_−_14_._7%)|0_._0764(+|36_._0%)|0_._2728(+24_._0%)|0_._2325(_−_4_._3%)|


the iFSQ tokenizer fixed (iFSQBM _→_ iFSQ) raises completion from 85.1% to 87.2%, confirming the role of observation design in robust tracking. 

_Tokenizer effectiveness._ Comparing VQ-VAE and iFSQBM—which share the same encoder–decoder policy and BM-style observation design but differ in the quantizer—reveals that iFSQ reduces the joint-position error from 2.3013 to 1.4760 rad ( _−_ 35.8%) while maintaining a comparable completion rate (85.1% vs. 86.0%). The dramatic reduction in tracking precision highlights the superior codebook utilization of finite scalar quantization over conventional VQ-VAE in this high-frequency control domain. _Observation design and height features._ Among the iFSQ variants, iFSQ+H achieves the lowest height error (0.0271 m) and orientation error (0.1539 rad) across all methods, while iFSQ attains the best linear-velocity tracking (0.1561 m/s) and a competitive joint-position error (1.1863 rad). Removing explicit height features (iFSQ+H _→_ iFSQ) yields lower joint error (1.1863 vs. 1.2924 rad) at the expense of higher height error (0.0955 vs. 0.0271 m) and markedly degraded orientation control (0.3614 vs. 0.1539 rad), confirming that the height channel is critical for vertical and orientation precision. _Trajectory generator._ Heracles achieves the highest completion rate (90.6%) among all methods—a 6.8% relative improvement over MLP and a 3.9% improvement over the standalone iFSQ tracker—while maintaining competitive tracking quality. Compared to iFSQ, the trajectory generator reduces root orientation error from 0.3614 to 0.2728 rad (24.5% relative reduction) and height error from 0.0955 to 0.0764 m (20.0% reduction), at a modest cost in joint-position error (1.3272 vs. 1.1863 rad). This indicates that the stateconditioned generative planner synthesizes spatially-aware recovery trajectories that refine both vertical and heading control, a capability absent in the reactive tracker alone. 

We present qualitative sim-to-sim evaluation results on an out-of-distribution martial arts sequence in MuJoCo, as shown in Fig. 3. Among the baseline methods, MLP, Transformer, and SONIC fail to maintain balance and collapse early in the sequence, while VQ-VAE barely tracks the motion throughout. For our ablation variants, 

14 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 


Figure 3: **Qualitative sim-to-sim comparison on an out-of-distribution martial arts sequence.** Each row shows a different method tracking the same reference motion on a Unitree G1 humanoid alongside a reference ghost in MuJoCo. MLP, Transformer, and SONIC collapse early; VQ-VAE barely tracks the motion. Among our ablations, iFSQBM and iFSQ survive without falling, while iFSQ+H falls but later recovers. **Heracles** (Ours) tracks the full sequence most accurately, demonstrating the strongest robustness to OOD motions. 

iFSQBM and iFSQ successfully survive the entire sequence without falling; however, iFSQ+H experiences a fall at an intermediate stage but manages to recover afterwards. In contrast, **Heracles** not only survives the full sequence but also accurately tracks the root position and body pose across all frames, demonstrating the strongest robustness to out-of-distribution motions among all evaluated approaches. 

We further validate our method through real-world deployment on a Unitree G1 humanoid robot, as illustrated in Fig. 4. The experiments span a broad spectrum of behaviors, ranging from everyday locomotion such as walking and running, to highly dynamic skills including kicking and full 360° kicks, as well as human-object interaction (HOI) scenarios. 

15 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 


Figure 4: **Real-world motion tracking across diverse and dynamic behaviors.** Real-world experiments demonstrate that our model generalizes to a broad spectrum of motions, from everyday locomotion (walk, run) to highly dynamic skills (kick, 360° kick) and human-object interaction. 

## **4.3. Fall-and-Recovery Evaluation** 

To specifically assess the fall-and-recovery capabilities that distinguish Heracles from pure tracking approaches, we conduct a dedicated evaluation on a curated subset of fall-and-recovery motion sequences extracted from the test corpus. These sequences encompass diverse recovery scenarios including lie-to-stand, prone-to-stand, and stand-to-lie transitions, with varied initial fallen configurations and recovery directions. All sequences are evaluated in both their original continuous form and discretized variants, in which the trajectories are replaced with piecewise-constant poses, to assess robustness under discontinuous reference signals. Quantitative results are summarized in Tab. 5; qualitative sim-to-sim comparisons are shown in Fig. 5. 

Table 5: **Fall-and-recovery evaluation on challenging lie-to-stand, prone-to-stand, and stand-to-lie sequences.** CR denotes completion rate. <mark>Blue</mark> marks the best result per metric. Colored percentages show relative change from MLP: teal = better, red = worse. 

|**Method**|**CR**<br>(%)_↑_|**Joint Err**<br>(rad)_↓_|**Height Err**<br>(m)_↓_|**Ori Err**<br>(rad)_↓_|**LinVel Err**<br>(m/s)_↓_|
|---|---|---|---|---|---|
|MLP|44_._0|2_._1720|0_._3586|1_._0157|0_._2710|
|Transformer|40_._6(_−_7_._7%)|2_._8309(_−_30_._3%)|0_._3706(_−_3_._3%)|0_._8355(+17_._7%)|0_._2708(+0_._1%)|
|VQ-VAE|69_._8(+58_._6%)|2_._5700(_−_18_._3%)|0_._1898(+47_._1%)|0_._4307(+57_._6%)|0_._2719(_−_0_._3%)|
|SONIC|42_._8(_−_2_._7%)|2_._9897(_−_37_._6%)|0_._3342(+6_._8%)|0_._8629(+15_._0%)|0_._2895(_−_6_._8%)|
|iFSQBM|52_._4(+19_._1%)|2_._4482(_−_12_._7%)|0_._2880(+19_._7%)|0_._9109(+10_._3%)|0_._3134(_−_15_._6%)|
|iFSQ+H|52_._7(+19_._8%)|1_._7660(+18_._7%)|**0**_._**0419**(+88_._3%)|0_._2744(+73_._0%)|0_._2793(_−_3_._1%)|
|iFSQ|48_._2(+9_._5%)|2_._0236(+6_._8%)|0_._3024(+15_._7%)|1_._0488(_−_3_._3%)|**0**_._**2405**(+11_._3%)|
|Heracles|**90**_._**0**(+104_._5%)|**1**_._**4114**(+35_._0%)|0_._0762(+78_._7%)|**0**_._**2427**(+76_._1%)|0_._2830(_−_4_._4%)|


The fall-and-recovery evaluation reveals a stark performance divide that underscores the fundamental limitations 

16 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

of pure tracking paradigms (Tab. 5). All reactive tracking baselines—MLP, Transformer, and SONIC—achieve completion rates below 45%, indicating complete inability to execute fall-recovery motions. While these methods function adequately under nominal tracking conditions (Tab. 4), they fail catastrophically when the reference motion demands transitions through extreme pose configurations inherent to fall-and-recovery sequences. 

Among the compared methods, VQ-VAE demonstrates unexpected resilience (CR = 69.8%), suggesting that its less precise but more flexible latent representation provides some implicit generalization to extreme poses. The iFSQ tracker variants without the generative middleware show mixed results: iFSQ+H achieves the highest completion rate among standalone trackers (52.7%) and the lowest height error (0.0419 m) due to its explicit height features, while iFSQBM and iFSQ achieve completion rates of 52.4% and 48.2% respectively with substantially higher tracking errors. 

**Heracles achieves the highest completion rate by a decisive margin** (90.0%), exceeding the second-best method VQ-VAE by 20.2 percentage points—a 104.5% relative improvement over MLP. Critically, Heracles also attains the lowest joint-position error (1.4114 rad) and orientation error (0.2427 rad) among all methods, confirming that the state-conditioned generative middleware is essential for maintaining coherent tracking through the extreme state transitions characteristic of fall-and-recovery motions. By dynamically synthesizing feasible recovery trajectories conditioned on the robot’s real-time physical state, Heracles bridges the gap between the reference motion and the robot’s actual configuration, enabling graceful execution of motions that drive purely reactive trackers to catastrophic failure. 

## **4.4. Ablation Studies and Architectural Analysis** 

To isolate the contribution of each design choice within the generative middleware, we conduct ablation experiments on the trajectory generator while keeping the iFSQ tracker fixed. All ablations are evaluated on the full 101-sequence test set spanning the complete diversity of the evaluation corpus. Results are summarized in Tab. 6. 

Table 6: **Ablation study on the trajectory generator’s key design components.** All variants are evaluated on the full 101-sequence test set using the same iFSQ tracker. <mark>Blue</mark> marks the best result per metric. Colored percentages show relative change from Heracles (full): teal = better, red = worse. 

|**Variant**|**CR**|**Joint Err**|**Height Err**|**Ori Err**|**LinVel Err**|
|---|---|---|---|---|---|
||(%)_↑_|(rad)_↓_|(m)_↓_|(rad)_↓_|(m/s)_↓_|
|Heracles (full)|**90**_._**6**|**1**_._**3272**|**0**_._**0764**|**0**_._**2728**|0_._2325|
|w/o directional warm start|87_._2 (-3.8%)|1_._6236 (-22.3%)|0_._0962 (-25.9%)|0_._3393 (-24.4%)|0_._2423 (-4.2%)|
|w/o noisy-state augmentation|78_._6 (-13.2%)|1_._8896 (-42.4%)|0_._1463 (-91.5%)|0_._4318 (-58.3%)|**0**_._**2182** (+6.1%)|
|w/o kinematics-aware weighting|82_._1 (-9.4%)|1_._6931 (-27.6%)|0_._1200 (-57.1%)|0_._4055 (-48.6%)|0_._2394 (-3.0%)|


**Directional Warm Start.** Replacing the directional motion prior (Eq. (10)) with pure Gaussian initialization degrades all metrics: completion drops from 90.6% to 87.2% ( _−_ 3.8%) and joint error increases by 22.3%. The warm start seeds the ODE solver with a coarse linear interpolation toward the target, enabling the learned velocity field to focus its refinement budget on naturalness rather than gross direction estimation. Without this prior, the generator must expend additional integration steps to discover the correct recovery heading, yielding failures particularly on fall-and-recovery sequences. 

**Noisy-State Augmentation.** Removing the asymmetric noise injection (Eq. (20)) during training produces the most severe degradation in completion rate among all ablation variants, with CR falling to 78.6% ( _−_ 13.2%) and joint error increasing by 42.4%. Height error nearly doubles (+91.5%), and orientation error increases by 58.3%. Without noise augmentation, the generator overfits to clean state inputs; at deployment, accumulated tracking drift and sensor noise push the conditioning state away from the training distribution, causing catastrophic failure on out-of-distribution motions. The augmented variant bridges this train–deploy distribution gap, 

17 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 


Figure 5: **Qualitative sim-to-sim comparison on an OOD lie-to-stand sequence.** Same setup as Fig. 3. MLP, Transformer, SONIC, and iFSQBM fail to stand up; VQ-VAE, iFSQ+H, and iFSQ partially track the motion. **Heracles** (Ours) completes the full lie-to-stand transition and most accurately tracks the root position. 

enabling robust trajectory generation even from noisy proprioceptive readings. 

**Kinematics-Aware Loss Weighting.** Removing the Jacobian-based weighting (Eq. (21)) produces the largest degradation in completion rate after noisy-state augmentation, with CR falling to 82.1% ( _−_ 9.4%). Height error increases by 57.1% and orientation error by 48.6%. The severity of this ablation indicates that pose-dependent lever-arm geometry is critical for robust tracking: a unit-radian shoulder error in an extended-arm configuration induces far larger Cartesian displacement than the same error with arms at rest, and the weighting scheme enables the generator to prioritize these geometrically sensitive configurations. 

**Learned Discrete Representation.** Beyond component-level ablations, we examine whether the iFSQ tokenizer acquires a semantically structured codebook after training on the full motion corpus. Fig. 6 visualizes the discrete code activations projected into a three-dimensional embedding space, with each point representing a quantized motion token colored by its source motion category. The visualization reveals clearly separable clusters corresponding to distinct motor skills—walking, running, jumping, martial arts, dance, parkour, crawling, balance, and fall recovery—despite the quantizer receiving no explicit category labels during training. Notably, semantically related skills occupy neighboring regions (walking and running clusters lie adjacent, while crawling and balance form a separate group), indicating that the iFSQ codebook captures meaningful 

18 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

kinematic similarity structure. This emergent organization confirms that the finite scalar quantization not only compresses high-frequency motion signals into compact tokens but also distills a structured motion taxonomy that enables the downstream action decoder and trajectory generator to reason over semantically coherent motion abstractions. 


Figure 6: **Emergent semantic clustering in the learned iFSQ codebook.** Each point represents a quantized motion token projected into 3D via PCA; colors denote motion categories. Despite receiving no category labels during training, the codebook self-organizes into semantically coherent clusters corresponding to distinct motor skills. 

**Architectural Motivation.** The ablation results collectively reveal why a hierarchical architecture—with a dedicated generative planner layered above a physics tracker—is preferable to monolithic alternatives for general-purpose humanoid control. On the 101-sequence evaluation, removing any single component reduces completion rate by 3.8–13.2%, demonstrating that all three design choices are essential for robust performance. Noisy-state augmentation has the largest impact on tracking quality (CR: _−_ 13.2%, height error: +91.5%), underscoring that bridging the train–deploy distribution gap is the most critical challenge for sustained tracking fidelity. Kinematics-aware weighting produces the second-largest CR degradation ( _−_ 9.4%) alongside substantial increases in height (+57.1%) and orientation error (+48.6%), revealing that accurate lever-arm modeling is essential for navigating complex multi-step transitions. These findings reinforce the design principle of frequency separation: the generative middleware reasons over a 0.2 s planning window at 25 Hz, synthesizing 

19 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

temporally coherent recovery strategies that the tracker then faithfully executes at 50 Hz—mirroring the hierarchical structure of biological motor systems. 

## **4.5. Recovery Behaviors and Analysis** 

Beyond quantitative metrics, we examine the qualitative character of recovery behaviors to understand _how_ the generative middleware transforms the robot’s response to severe disturbances. This analysis reveals a fundamental distinction between tracking-based and generation-based control paradigms. 

**Tracking-Only Failure Modes.** When subjected to large external perturbations, standalone trackers—including all baselines and the iFSQ variant—exhibit a characteristic failure pattern. Upon being displaced from the reference trajectory, the tracker computes a single-step corrective action that minimizes the instantaneous state-reference error. This myopic strategy produces rigid, jerky corrective torques that lack the temporal coordination required for dynamic balance recovery. In the most severe cases, the tracker’s insistence on returning to the exact reference pose forces physically infeasible joint configurations, accelerating rather than preventing the fall. Even when the tracker avoids catastrophic failure, its recovery motions appear distinctly non-anthropomorphic: abrupt whole-body stiffening, unnatural arm postures, and a conspicuous absence of the compensatory stepping strategies that characterize human balance recovery. 

**Generative Recovery Behaviors.** Heracles produces qualitatively different recovery dynamics. When a large perturbation displaces the robot from the reference manifold, the generative middleware detects the state-reference discrepancy and synthesizes a short-horizon trajectory that prioritizes physical feasibility over immediate reference fidelity. This manifests as emergent human-like recovery strategies: compensatory stepping to widen the base of support, coordinated arm counter-motions to redistribute angular momentum, and gradual torso realignment before resuming the original motion. Crucially, these behaviors are not hand-designed or reward-engineered—they emerge naturally from the flow matching model’s learned distribution over physically plausible motion transitions, conditioned on the robot’s real-time state. 

**From Tracking to Planning: Rethinking General Humanoid Control.** The observed behavioral difference reveals a deeper conceptual insight into what constitutes a truly general-purpose humanoid controller. The dominant tracking paradigm implicitly assumes that control reduces to minimizing the deviation between the robot’s state and a predefined kinematic reference. While effective for nominal execution, this formulation conflates two fundamentally distinct objectives: executing a desired motor intent and maintaining physical viability. 

Human motor control does not operate as a rigid reference tracker. When a person stumbles, they do not attempt to snap back to a pre-planned gait trajectory. Instead, the motor system rapidly _revises_ the intended trajectory itself, generating a new plan that accounts for the current physical state, gravitational constraints, and available momentum. The original intent is temporarily deprioritized in favor of a dynamically feasible recovery path, and only once stability is restored does the system smoothly re-engage with the original task objective. 

Heracles embodies precisely this principle through its state-conditioned middleware. The generative planner continuously modulates the reference signal based on real-time physical feasibility: passing commands through unmodified when tracking is viable, but seamlessly _rewriting_ them when the physical state demands a different motor strategy. This transforms the controller from a passive trajectory follower into an active trajectory synthesizer that reasons about what the robot _should_ do given its current physical reality, rather than what it was _told_ to do by a reference signal computed without knowledge of real-time dynamics. 

**Implications for General-Purpose Deployment.** This paradigm shift has concrete implications for deploying humanoid robots in unstructured environments. Real-world scenarios invariably introduce perturbations absent from any training distribution: unexpected collisions, terrain irregularities, payload changes, or degraded actuation. A tracking-only controller can only succeed if its training-time domain randomization happens to 

20 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 


Figure 7: **Omnidirectional fall recovery motion tracking.** Real-world experiments demonstrate that our model generalizes to arbitrary lie-to-stand recovery motions, successfully handling varied initial fallen configurations and recovery directions without task-specific engineering. 

cover the encountered disturbance; beyond this envelope, it fails brittly. The generative middleware, by contrast, provides a principled mechanism for _open-ended_ adaptation: as long as the learned motion prior contains transitions between sufficiently diverse physical states, the model can compose novel recovery strategies for previously unseen perturbations. This compositional generalization—the ability to recombine learned motion primitives into new sequences conditioned on novel states—is what distinguishes a truly general controller from one that merely covers a large but finite set of pre-trained behaviors. 

We further evaluate this generalization capability on omnidirectional fall recovery tasks in both simulation and the real world. As shown in Fig. 5, Heracles completes the full lie-to-stand transition in MuJoCo while all baseline methods fail or only partially succeed. Fig. 7 presents the corresponding real-world results: across three trials, the robot is initialized in distinct fallen configurations—supine, lateral, and prone postures. In all cases, the robot successfully executes a complete lie-to-stand recovery by following the reference motion, progressively transitioning through intermediate support phases. Critically, the recovery directions vary across trials, with the robot rising toward different orientations relative to its initial fallen heading, demonstrating true omnidirectional recovery rather than a memorized fixed-direction strategy. 

21 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

# **5. Conclusion** 

In conclusion, this work presents Heracles, a state-conditioned generative middleware that fundamentally resolves the longstanding dichotomy between strict kinematic tracking and robust physical recovery in humanoid robotics. By embedding a continuous flow matching process within a closed-loop control architecture, the framework dynamically bridges high-fidelity intent execution with anthropomorphic resilience. Without relying on explicit mode-switching heuristics, Heracles intrinsically preserves exact zero-shot tracking under nominal conditions while seamlessly synthesizing dynamically feasible recovery maneuvers during severe environmental perturbations. Ultimately, this unified paradigm liberates embodied control from rigid, reference-bound execution, establishing a highly scalable foundation for deploying agile and resilient general-purpose humanoids in complex physical environments. 

# **6. X-Humanoid Heracles Project Team** 

This report reflects a collaborative effort by the X-Humanoid Heracles project team. The roles and contributors are listed below. 

**Project Leader.** Qiang Zhang 

**Equal Contribution.** Zelin Tao, Zeran Su 

**Project Team Members.** Peiran Liu, Jingkai Sun, Wenqiang Que, Jiahao Ma, Jialin Yu, Jiahang Cao, Pihai Sun, Hao Liang 

**Technical Support.** Gang Han, Wen Zhao, Zhiyuan Xu, Yijie Guo, Jian Tang 

22 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

# **References** 

- [1] Lucas N Alegre, Agon Serifi, Ruben Grandia, David Müller, Espen Knoop, and Moritz Bächer. Amor: Adaptive character control through multi-objective reinforcement learning. In _Proceedings of the Special Interest Group on Computer Graphics and Interactive Techniques Conference (SIGGRAPH)_ , 2025. 5 

- [2] Yeke Chen, Shihao Dong, Xiaoyu Ji, Jingkai Sun, Zeren Luo, Liu Zhao, Jiahui Zhang, Wanyue Li, Ji Ma, Bowen Xu, et al. Learning human-like badminton skills for humanoid robots. _arXiv preprint arXiv:2602.08370_ , 2026. 4 

- [3] Zixuan Chen, Mazeyu Ji, Xuxin Cheng, Xuanbin Peng, Xue Bin Peng, and Xiaolong Wang. Gmt: General motion tracking for humanoid whole-body control. _arXiv preprint arXiv:2506.14770_ , 2025. 3, 5 

- [4] Ke Fan, Shunlin Lu, Minyue Dai, Runyi Yu, Lixing Xiao, Zhiyang Dou, Junting Dong, Lizhuang Ma, and Jingbo Wang. Go to zero: Towards zero-shot motion generation with million-scale data. 2025. 4 

- [5] Chuan Guo, Inwoo Hwang, Jian Wang, and Bing Zhou. Snapmogen: Human motion generation from expressive texts. In _In Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. 11 

- [6] Félix G Harvey, Mike Yurick, Derek Nowrouzezahrai, and Christopher Pal. Robust motion in-betweening. _ACM Transactions on Graphics (TOG)_ , 39(4):60–1, 2020. 11 

- [7] Tairan He, Wenli Xiao, Toru Lin, Zhengyi Luo, Zhenjia Xu, Zhenyu Jiang, Jan Kautz, Changliu Liu, Guanya Shi, Xiaolong Wang, Linxi Fan, and Yuke Zhu. Hover: Versatile neural whole-body controller for humanoid robots. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 1, 3 

- [8] Biao Jiang, Xin Chen, Wen Liu, Jingyi Yu, Gang Yu, and Tao Chen. Motiongpt: Human motion as a foreign language. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2023. 4 

- [9] Eunjong Lee, Eunhee Kim, Sanghoon Hong, Eunho Jung, and Jihoon Kim. Controllable long-term motion generation with extended joint targets. In _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)_ , 2025. 5 

- [10] Yitang Li, Zhengyi Luo, Tonghe Zhang, Cunxi Dai, Anssi Kanervisto, Andrea Tirinzoni, Haoyang Weng, Kris Kitani, Mateusz Guzek, Ahmed Touati, Alessandro Lazaric, Matteo Pirotta, and Guanya Shi. Bfmzero: A promptable behavioral foundation model for humanoid control using unsupervised reinforcement learning. In _In International Conference on Learning Representations (ICLR)_ , 2026. 1, 4, 12 

- [11] Zhe Li, Weihao Yuan, Weichao Shen, Siyu Zhu, Zilong Dong, and Chang Xu. Omnimotion: Multimodal motion generation with continuous masked autoregression. _arXiv preprint arXiv:2510.14954_ , 2025. 4 

- [12] Zhe Li, Cheng Chi, Yangyang Wei, Boan Zhu, Yibo Peng, Tao Huang, Pengwei Wang, Zhongyuan Wang, Shanghang Zhang, and Chang Xu. From language to locomotion: Retargeting-free humanoid control via motion latent guidance. In _In International Conference on Learning Representations (ICLR)_ , 2026. 3 

- [13] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Guy Tevet, Koushil Sreenath, and C Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 3, 12, 13, 14 

- [14] Bin Lin, Yujia Ge, Xinyang Cheng, Ye Zhu, Shubin Ye, Yuan Li, Jiaxi Zhu, Jiahao Yan, Haoqian Zeng, Zhenyu Wang, Liuhan Zhang, Fang Wan, Qingdong Liu, Xianyi Zhao, Yonghong Li, and Limin Yang. ifsq: Improving fsq for image generation with 1 line of code. _arXiv preprint arXiv:2601.17124_ , 2026. 9 

- [15] Jing Lin, Ailing Zeng, Shunlin Lu, Yuanhao Cai, Ruimao Zhang, Haoqian Wang, and Lei Zhang. Motion-x: A large-scale 3d expressive whole-body human motion dataset. _Advances in Neural Information Processing Systems ( (NeurIPS)_ , 36:25268–25280, 2023. 4 

23 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

- [16] Yutang Lin, Jieming Cui, Yixuan Li, Baoxiong Jia, Yixin Zhu, and Siyuan Huang. Lessmimic: Long-horizon humanoid interaction with unified distance field representations. _arXiv preprint arXiv:2602.21723_ , 2026. 4 

- [17] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matthew Le. Flow matching for generative modeling. In _International Conference on Learning Representations (ICLR)_ , 2023. 7 

- [18] Zhengyi Luo, Jiashun Wang, Kangni Liu, Haotian Zhang, Chen Tessler, Jingbo Wang, Ye Yuan, Jinkun Cao, Zihui Lin, Fengyi Wang, et al. Smplolympics: Sports environments for physically simulated humanoids. _arXiv preprint arXiv:2407.00187_ , 2024. 4 

- [19] Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Castañeda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 1, 3, 5, 12, 13 

- [20] Naureen Mahmood, Nima Ghorbani, Nikolaus F Troje, Gerard Pons-Moll, and Michael J Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 5442–5451, 2019. 12 

- [21] Ian Mason, Sebastian Starke, and Taku Komura. Real-time style modelling of human locomotion via feature-wise transformations and local motion phases. _Proc. ACM Comput. Graph. Interact. Tech._ , 5(1), May 2022. doi: 10.1145/3522618. URL `https://doi.org/10.1145/3522618` . 11 

- [22] Chenlin Meng, Yutong He, Yang Song, Jiaming Song, Jiajun Wu, Jun-Yan Zhu, and Stefano Ermon. SDEdit: Guided image synthesis and editing with stochastic differential equations. In _International Conference on Learning Representations (ICLR)_ , 2022. 8 

- [23] Mayank Mittal, Pascal Roth, James Tigue, Antoine Richard, Octi Zhang, Peter Du, Antonio Serrano-Muñoz, Xinjie Yao, René Zurbrügg, Nikita Rudin, et al. Isaac lab: A gpu-accelerated simulation framework for multi-modal robot learning. _arXiv preprint arXiv:2511.04831_ , 2025. 11 

- [24] Liang Pan, Zeshi Yang, Zhiyang Dou, Wenjia Wang, Buzhen Huang, Bo Dai, Taku Komura, and Jingbo Wang. Tokenhsi: Unified synthesis of physical human-scene interactions through task tokenization. In _In Proceedings of IEEE Conference on Computer Vision and Pattern Recognition_ , 2025. 13 

- [25] Yixuan Pan, Ruoyi Qiao, Li Chen, Kashyap Chitta, Liang Pan, Haoguang Mai, Qingwen Bu, Hao Zhao, Cunyuan Zheng, Ping Luo, and Hongyang Li. Agility meets stability: Versatile humanoid control with heterogeneous data. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , 2026. 3 

- [26] William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2023. 7, 12, 13 

- [27] Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37 (4):1–14, 2018. 3, 5 

- [28] Xue Bin Peng, Yunrong Guo, Lina Halper, Sergey Levine, and Sanja Fidler. Ase: Large-scale reusable adversarial skill embeddings for physically simulated characters. _ACM Transactions On Graphics (TOG)_ , 41(4):1–17, 2022. 5 

- [29] Agon Serifi, Ruben Grandia, Espen Knoop, Markus Gross, and Moritz Bächer. Vmp: Versatile motion priors for robustly tracking motion on physical characters. In _Proceedings of the ACM SIGGRAPH/Eurographics Symposium on Computer Animation (SCA)_ , pages 1–11, 2024. 5 

24 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

- [30] Jean-Pierre Sleiman, He Li, Alphonsus Adu-Bredu, Robin Deits, Arun Kumar, Kevin Bergamin, Mohak Bhardwaj, Scott Biddlestone, Nicola Burger, Matthew A. Estrada, Francesco Iacobelli, Twan Koolen, Alexander Lambert, Erica Lin, M. Eva Mungai, Zach Nobles, Shane Rozen-Levy, Yuyao Shi, Jiashun Wang, Jakob Welner, Fangzhou Yu, Mike Zhang, Alfred Rizzi, Jessica Hodgins, Sylvain Bertrand, Yeuhi Abe, Scott Kuindersma, and Farbod Farshidian. Zest: Zero-shot embodied skill transfer for athletic robot control. _arXiv preprint arXiv:2602.00401_ , 2026. 10 

- [31] Jingkai Sun, Qiang Zhang, Yiqun Duan, Xiaoyang Jiang, Chong Cheng, and Renjing Xu. Prompt, plan, perform: Llm-based humanoid control via quantized imitation learning. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024. 3, 13 

- [32] Guy Tevet, Sigal Raab, Brian Gordon, Yonatan Shafir, Daniel Cohen-Or, and Amit H Bermano. Human motion diffusion model. In _International Conference on Learning Representations (ICLR)_ , 2023. 4 

- [33] Yinhuai Wang, Qihan Zhao, Runyi Yu, Hok Wai Tsui, Ailing Zeng, Jing Lin, Zhengyi Luo, Jiwen Yu, Xiu Li, Qifeng Chen, et al. Skillmimic: Learning basketball interaction skills from demonstrations. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 17540–17549, 2025. 4 

- [34] Yuan Wang, Di Huang, Yaqi Zhang, Wanli Ouyang, Jile Jiao, Xuetao Feng, Yan Zhou, Pengfei Wan, Shixiang Tang, and Dan Xu. Motiongpt-2: A general-purpose motion-language model for motion generation and understanding. _arXiv preprint arXiv:2410.21747_ , 2024. 4 

- [35] Yunshen Wang, Shaohang Zhu, Peiyuan Zhi, Yuhan Li, Jiaxin Li, Yong-Lu Li, Yuchen Xiao, Xingxing Wang, Baoxiong Jia, and Siyuan Huang. Omnixtreme: Breaking the generality barrier in high-dynamic humanoid control. _arXiv preprint arXiv:2602.23843_ , 2026. 1, 3 

- [36] Yuxin Wen, Qing Shuai, Di Kang, Jing Li, Cheng Wen, Yue Qian, Ningxin Jiao, Changhai Chen, Weijie Chen, Yiran Wang, et al. Hy-motion 1.0: Scaling flow matching models for text-to-motion generation. _arXiv preprint arXiv:2512.23464_ , 2025. 4 

- [37] Lixing Xiao, Shunlin Lu, Huaijin Pi, Ke Fan, Liang Pan, Yueer Zhou, Ziyong Feng, Xiaowei Zhou, Sida Peng, and Jingbo Wang. Motionstreamer: Streaming motion generation via diffusion-based autoregressive model in causal latent space. _arXiv preprint arXiv:2503.15451_ , 2025. 5 

- [38] Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, Pieter Abbeel, Carmelo Sferrazza, C Karen Liu, Rocky Duan, and Guanya Shi. Omniretarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 3 

- [39] Kangning Yin, Weishuai Zeng, Ke Fan, Minyue Dai, Zirui Wang, Qiang Zhang, Zheng Tian, Jingbo Wang, Jiangmiao Pang, and Weinan Zhang. Unitracker: Learning universal whole-body motion tracker for humanoid robots. _arXiv preprint arXiv:2507.07356_ , 2025. 1 

- [40] Kangning Yin, Zhe Cao, Wentao Dong, Weishuai Zeng, Tianyi Zhang, Qiang Zhang, Jingbo Wang, Jiangmiao Pang, Ming Zhou, and Weinan Zhang. Robostriker: Hierarchical decision-making for autonomous humanoid boxing. _arXiv preprint arXiv:2601.22517_ , 2026. 5 

- [41] Runyi Yu, Yinhuai Wang, Qihan Zhao, Hok Wai Tsui, Jingbo Wang, Ping Tan, and Qifeng Chen. Skillmimicv2: Learning robust and generalizable interaction skills from sparse and noisy demonstrations. In _Proceedings of the Special Interest Group on Computer Graphics and Interactive Techniques Conference Conference Papers_ , pages 1–11, 2025. 4 

- [42] Mingqi Yuan, Tao Yu, Wenqi Ge, Xiuyong Yao, Huijiang Wang, Jiayu Chen, Bo Li, Wei Zhang, Wenjun Zeng, Hua Chen, and Xin Jin. A survey of behavior foundation model: Next-generation whole-body control system of humanoid robots. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2025. 4 

25 

Heracles: Bridging Precise Tracking and Generative Synthesis for General Humanoid Control 

- [43] Weishuai Zeng, Shunlin Lu, Kangning Yin, Xiaojie Niu, Minyue Dai, Jingbo Wang, and Jiangmiao Pang. Behavior foundation model for humanoid robots. _arXiv preprint arXiv:2509.13780_ , 2025. 1, 4 

- [44] Qiang Zhang, Peter Cui, David Yan, Jingkai Sun, Yiqun Duan, Gang Han, Wen Zhao, Weining Zhang, Yijie Guo, Arthur Zhang, and Renjing Xu. Whole-body humanoid robot locomotion with human reference. _arXiv preprint arXiv:2402.18294_ , 2024. 4 

- [45] Qiang Zhang, Jiahao Ma, Peiran Liu, Shuai Shi, Zeran Su, Zifan Wang, Jingkai Sun, Wei Cui, Jialin Yu, Gang Han, Wen Zhao, Pihai Sun, Kangning Yin, Jiaxu Wang, Jiahang Cao, Lingfeng Zhang, Hao Cheng, Xiaoshuai Hao, Yiding Ji, Junwei Liang, Jian Tang, Renjing Xu, and Yijie Guo. Meshmimic: Geometryaware humanoid motion learning through 3d scene reconstruction. _arXiv preprint arXiv:2602.15733_ , 2026. 4 

- [46] Yuhong Zhang, Jing Lin, Ailing Zeng, Guanlin Wu, Shunlin Lu, Yurong Fu, Yuanhao Cai, Ruimao Zhang, Haoqian Wang, and Lei Zhang. Motion-x++: A large-scale multimodal 3d whole-body human motion dataset. _arXiv preprint arXiv:2501.05098_ , 2025. 4 

- [47] Zhikai Zhang, Haofei Lu, Yunrui Lian, Ziqing Chen, Yun Liu, Chenghuai Lin, Han Xue, Zicheng Zeng, Zekun Qi, Shaolin Zheng, et al. Learning athletic humanoid tennis skills from imperfect human motion data. _arXiv preprint arXiv:2603.12686_ , 2026. 4 

- [48] Ziyu Zhang, Sergey Bashkirov, Dun Yang, Yi Shi, Michael Taylor, and Xue Bin Peng. Physics-based motion imitation with adversarial differential discriminators. In _Proceedings of the SIGGRAPH Asia 2025 Conference Papers_ , SA Conference Papers ’25, New York, NY, USA, 2025. Association for Computing Machinery. ISBN 9798400721373. doi: 10.1145/3757377.3763819. URL `https://doi.org/10.1145/3757377.3763819` . 5 

- [49] Kaifeng Zhao, Gen Li, and Siyu Tang. Dartcontrol: A diffusion-based autoregressive motion model for real-time text-driven motion control. _arXiv preprint arXiv:2410.05260_ , 2024. 5 

- [50] Shaoting Zhu, Baijun Ye, Jiaxuan Wang, Jiakang Chen, Ziwen Zhuang, Linzhan Mou, Runhan Huang, and Hang Zhao. Ttt-parkour: Rapid test-time training for perceptive robot parkour. _arXiv preprint arXiv:2602.02331_ , 2026. 4 

- [51] Ziwen Zhuang, Shaoting Zhu, Mengjie Zhao, and Hang Zhao. Deep whole-body parkour. _arXiv preprint arXiv:2601.07701_ , 2026. 4 

26 

