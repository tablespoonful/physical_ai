---
title: "Recursive Belief Vision Language Action Models"
date: "2026-02-24"
authors: "Vaidehi Bagaria; Bijo Sebastian; Nirav Kumar Patel"
url: https://arxiv.org/abs/2602.20659
pdf: https://arxiv.org/pdf/2602.20659
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.20659)** / [論文ページ](https://arxiv.org/abs/2602.20659)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Recursive Belief Vision Language Action Models 

Vaidehi Bagaria, Bijo Sebastian, Nirav Patel 

_Department of Engineering Design_ , _Indian Institute of Technology, Madras_ , Chennai, India Email: ed21b070@smail.iitm.ac.in 

**_Abstract_ —Vision-language-action models must enable agents to execute long-horizon tasks under partial observability. However, most existing approaches remain observation-driven, relying on short context windows or repeated queries to vision-language models (VLMs). This leads to loss of task progress, action repetition under perceptual aliasing, and high inference latency. While semantic grounding is important, long-horizon manipulation fundamentally requires persistent, action-conditioned state representations. Current VLAs lack such representations and exhibit limited temporal and physical reasoning, making them ill-suited for multi-stage control. This paper introduces RB-VLA, a belief-centric architecture trained with self-supervised worldmodel objectives that maintains a compact latent state encoding task-relevant history, dynamics and object interactions. Queried once per task, the VLM provides high-level intent, while the belief tracks task progress and enables phase-aware, causally grounded control under partial observability without storing raw observations or scaling memory with time. The belief and intent jointly condition a diffusion policy for robust closed-loop execution. RB-VLA outperforms prior VLAs on long-horizon benchmarks, achieving 52.5% and 37.5% higher success rates on multi-stage pick-and-place and stacking tasks, respectively, compared to** _π_ 0 **. It also reduces inference latency by up to 5× relative to baselines and eliminates memory growth across timesteps observed in existing VLAs. The model demonstrates increased robustness under occlusion and more consistent task progression in multi-stage settings. Ablations show the belief module is the primary driver of performance, increasing success rates from 32.5% without belief to 77.5% with belief. These results demonstrate the effectiveness of belief-based state representations for long-horizon, multi-stage control.** 

# I. INTRODUCTION 

Vision–language–action models [1]–[3] have shown strong generalization by combining language understanding with visual perception to directly produce robot actions, improving scalability over classical control systems. However, most VLAs implicitly adopt a Markovian assumption, conditioning actions only on the current observation or a short history window [4]–[6]. Such reactive reasoning fails to capture longterm context under noisy observations, perceptual aliasing, occlusion and temporally static short observation histories. This limitation reduces its effectiveness for long-horizon, multistage, partially observable real-world manipulation. While longer context could address this, current VLAs scale memory through token accumulation, resulting in high latency and unreliable task state retention. Effective decision-making therefore requires reasoning over past actions and their consequences through compact state representations. 

Some approaches rely on defining multi-stage dynamics with explicit task-stage supervision for long-horizon behavior [7], [8]. However, manipulation is driven by smoothly evolv- 

ing, action-grounded internal dynamics rather than discrete labels. Learning continuous dynamics better captures shared physical structure across tasks, whereas stage-based supervision is task-specific and poorly generalizable. 

World models [9] address this by modeling agent–environment dynamics, enabling future-aware planning in VLAs. Although vision–language models excel at semantic inference, they lack explicit grounding in physical dynamics and state evolution, ignoring physical constraints [10]. World models bridge this gap by linking visual observations to action-conditioned dynamics that enable reasoning about future states beyond semantics alone. Existing approaches refine VLM decisions by predicting future observations with world models for online correction [11]–[13], but rely on repeated, computationally expensive dynamic rollouts. In contrast, maintaining a compact internal belief state that tracks task progress through the consequences of past actions, enables action selection without continual forward simulation at each timestep. 

In the absence of an internal state, VLAs repeatedly re-interpret observations with VLMs, leading to high computational cost and latency. Since VLMs provide semantic abstraction, they can be invoked sparsely, while causal reasoning governs low-level task execution. Hierarchical approaches improve computational efficiency and robustness by decoupling planning and control for long-horizon tasks [14], [15]. However, they still struggle with memory and task awareness. To address these issues, we introduce the Recursive Belief VLA (RB-VLA) framework. Our key contributions are: 

- 1) **Belief-centric VLA formulation:** We introduce a fixedsize, action conditioned recursive belief memory that captures task-relevant interaction history and system dynamics, enabling causal reasoning and consistent decision-making under partial observability. 

- 2) **Phase-aware long-horizon control:** The recursive belief provides short and long-horizon predictive context, supporting implicit phase estimation and conditioning a diffusion policy for dynamics-consistent closed-loop control in place of short observation windows. 

- 3) **Decoupled semantic grounding and control:** We treat semantic reasoning as episodic by querying a VLM once to extract grounded task intent, eliminating dense semantic re-inference. 

- 4) **Empirical validation on long-horizon benchmarks:** We demonstrate substantial improvements on longhorizon, multi-stage manipulation tasks and under oc- 


Fig. 1: **Overall Architecture of RB-VLA** . a) A VLM generates high-level intent from the current observation and instruction at t=0, implicitly grounding task semantics and relevant scene entities. b) Recursive belief estimator maintains a compact belief encoding task-relevant history. c) A DiT-based action head generates action chunks for closed-loop control 

clusion, outperforming prior VLAs while maintaining constant memory usage and significantly lower latency. 

# II. RELATED WORK 

# _A. Vision–Language–Action Models_ 

Recent vision–language–action models [1], [16] remain reactive by framing control as autoregressive action token prediction using large language models. While effective for semantic alignment, invoking a full language model at every step to produce only a small number of action tokens is computationally expensive. Prior work attempts to reduce this cost through chunked or parallel decoding [17], [18], selective activation [19], and visual token compression [20]. However, discrete action token prediction limits smooth continuous control and precise multimodal action generation, motivating recent approaches that replace the language head with continuous action decoders, such as diffusion [21] or flow-based policies [22]. These approaches nevertheless remain fundamentally observation-driven, relying on dense semantic re-inference that recomputes the same goals and instructions at every step. RBVLA addresses these limitations by maintaining a persistent state that tracks task progress and replaces computationally heavy VLM-based reinterpretation. 

# _B. Long Horizon Manipulation_ 

Long-horizon, multi-stage manipulation requires policies to reason over extended interactions. Existing approaches introduce inductive structure for long horizon tasks by explicitly predicting subgoals [23] or by conditioning policies on manually defined motion phases [24]. While effective for skill chaining and temporal abstraction, these methods rely on task-specific subtask or phase supervision. 

Some recent methods improve reasoning by introducing explicit intermediate inference before action selection. ECoT [25], ThinkAct [26], and related approaches [27], [28] generate visually grounded reasoning over sub-tasks, affordances, or latent plans to condition action prediction. Although these methods improve reasoning and reduce hallucination, they operate primarily in image–text space and lack persistent awareness 

of task progress, often failing in multi-stage execution. This motivates belief-based dynamics-grounded representations that summarize interaction history and enable robust closed-loop long-horizon behavior. 

# _C. Memory and Context_ 

As interaction history grows unbounded over time, relying on noisy raw or compressed observation windows over long horizons becomes infeasible. Short histories discard taskcritical temporal information, leading to failure under perceptual aliasing and in visually static multi-stage scenarios [29]. In RB-VLA the belief instead provides a fixed-size, dynamicsconsistent memory that filters observation noise and selectively retains motion-relevant information from past interactions and dynamics. 

Some prior works incorporate history through recurrent features [30] or growing memory tokens over time [31], but these mechanisms do not explicitly ground memory in actionconditioned dynamics. Other approaches learn long-horizon memory via selective context retention and gated fusion [32], where memory primarily serves as a post-hoc modulator of policy outputs rather than an internal state that shapes perception and encodes action-induced transitions. Predictive world-model methods explicitly model dynamics and generate dense future rollouts for planning or inference [33]–[35], while classical belief-space planners rely on explicit models and forward simulation [36]. Both incur substantial computational overhead and limit real-world applicability. 

Using world-model training objectives, RB-VLA learns a belief state sufficient for future prediction, without heavy rollout-based forward simulation at inference. The belief recursively modulates perception toward interaction-driven dynamics. 

# III. METHOD 

# _A. System Overview_ 

Long-horizon manipulation is formulated as a partially observable control problem with a learned belief estimator. The belief links perception to underlying motion dynamics 

rather than relying on raw observations, providing invariance to visual and environmental variation. 

The system consists of three components (Fig. 1): a vision–language reasoning module, a belief estimator, and a diffusion-based controller. We decouple semantic task specification from causal state estimation: a vision–language model is queried sparsely to extract a static latent goal embedding **I** _t_ from language and initial observations, binding instructions to concrete objects in the scene. This grounded goal embedding remains fixed throughout execution, as object identity and task semantics are static. 

At each step, the belief estimator integrates the previous belief **b** _t−_ 1, a window of tokenized observations _ot−K_ : _t_ , actions _at−K_ : _t_ , and proprioceptive states _xt−K_ : _t_ (end-effector pose, velocity, acceleration and force–torque measurements) using a temporal transformer to produce a latent belief **b** _t_ that tracks physical interaction progress. Low-level control is executed by a diffusion policy conditioned on ( **b** _t,_ **I** _t_ ), operating in closed loop at high frequency. 

# _B. Belief Estimator_ 

Long-horizon execution under partial observability is enabled by maintaining a belief state that captures information unavailable at a single timestep - such as occluded object states, contact history, and interaction progress—while being recursively updated and fixed in dimensionality. Similar to a state estimator [37], this belief produces a coherent task representation for planning and control. 

The belief transformer is trained as an RSSM-style world model [9], [38], separating deterministic dynamics from stochastic latent uncertainty. At each timestep, visual observations are encoded into patch-level features using a pretrained DINOv2 [39] backbone, while low-dimensional robot proprioceptive signals are embedded into a shared latent space. These multimodal tokens are fused by a transformer-based frame encoder with multi-head self-attention and pooled via learned attention to produce a task-relevant frame summary. This frame summary _ft_ highlights image regions that are linked to robot dynamics and produces interaction and dynamics-aware representations: 


where _ti_ are the patch tokens and _dq_ is a learned query vector. We warm-start the frame encoder with a temporal contrastive objective that aligns nearby interaction states and separates dynamically inconsistent ones: 


encouraging representations to reflect action-conditioned dynamics rather than appearance similarity. 

Temporal integration is performed by a transformer over a recent fixed-length window of the frame encoder representations, providing short-term temporal context. To enable recursion across arbitrarily long horizons, the previous belief state **b** _t−_ 1 is pre-pended as a token, allowing the model to 

condition new evidence on accumulated dynamics-relevant history. This belief token actively conditions temporal attention, biasing integration toward relevant interactions and dynamics rather than simply propagating state. The corresponding output yields an evidence representation **e** _t_ , which summarizes new observations conditioned on the prior belief. To capture uncertainty and branching futures, the model further introduces a stochastic latent variable _zt_ . The model learns a prior _p_ ( _zt |_ **b** _t−_ 1) = _N_ ( _µp, σp_ ) representing predicted uncertainty before observing the next frame, and a posterior _q_ ( _zt |_ **b** _t−_ 1 _,_ **e** _t_ ) = _N_ ( _µq, σq_ ) incorporating new evidence. The deterministic belief is then updated via, 

# **b** _t_ = GRU( **b** _t−_ 1 _,_ [ **e** _t, zt_ ]) _._ 

The belief is trained using a standard ELBO objective on predicted future latent observations _xt_ +1 from an exponential moving average (EMA)-updated frame encoder, which stabilizes training and reduces target drift. Unlike prior methods [40] that predict future visual embeddings, our targets are action-grounded, causing the belief to capture dynamics rather than just appearance. In addition to one-step prediction, we include a lightweight multi-step auxiliary decoder that predicts _xt_ +5 encouraging the belief to encode longer-horizon dynamical evolution beyond immediate transitions. The reconstruction objective is: 


A KL divergence term with a scheduled weight encourages exploration early in training and structured belief refinement later. Introducing stochasticity prevents collapse to a single averaged future, allowing the belief to represent multiple consistent hypotheses and maintain a sharp, coherent latent state under partial observability. To further enforce action grounding, we include an inverse dynamics loss, 


encouraging the belief to encode controllable state information relevant for predicting executed actions. 

The belief model runs at 10-20 Hz during inference and provides a persistent, anticipatory state sufficient for predicting future observations, enabling robust long-horizon execution without stage supervision or dense future rollout. 

# _C. High-Level Intent Prediction and Action Generation_ 

We adopt a vision–language–action framework in which a vision–language model (VLM) is decoupled with a diffusionbased low-level controller. The VLM is queried once per task using the instruction and the initial visual observation to produce an image-conditioned semantic task representation. This vector is projected through a lightweight MLP to obtain a 

compact intent embedding **It** , which remains static throughout task execution, since the semantic goal is fixed for a given task. The intent encodes the desired semantic outcome of the next execution phase - specifying _what_ should happen - while a diffusion policy determines _how_ it is achieved through continuous actions. During control, the intent is combined with the recursively updated belief state **bt** , enabling goal-directed control conditioned on the current execution stage. 

Unlike approaches that repeatedly invoke a VLM for stepwise reasoning, we treat semantic grounding as an episodic process. The VLM is not re-queried during execution unless the task specification changes or replanning is required. Task progress is instead inferred implicitly through the evolution of the belief state, which tracks physical events such as contact, grasp, release, and object motion even when visual evidence is ambiguous or occluded. 


Fig. 2: Environment with similar objects 

Fig. 1 illustrates how the intent embedding is obtained from the VLM. We remove the language generation head and use the frozen vision–language encoder to extract the final multi-modal hidden states. Let _X ∈_ R<sup>(</sup><sup>_T_+</sup><sup>_V_)</sup><sup>_×D_</sup> denote the final multimodal hidden states of the VLM after fusion, where _T_ and _V_ correspond to language and visual tokens respectively, and _D_ is the hidden dimensionality. To extract an image-conditioned task representation, we apply a singlequery attention pooling over these tokens. Specifically, we introduce a learned goal query vector **q** _∈_ R<sup>_D_</sup> and compute 


where _Wk_ is a learned projection matrix. This operation selectively aggregates visual and linguistic tokens into a single grounded representation. The pooled task vector is then projected through a lightweight MLP to obtain the intent vector **I** _t_ . The MLP adapts high-dimensional VLM features to the control space. The intent extraction module is trained end-to-end with the diffusion policy using the action prediction loss, while the VLM backbone remains frozen. Figure 2 shows a multiobject manipulation task where short-horizon memory fails: once an object leaves view after being placed by the robot, stateless VLAs forget the interaction and reattempt grasping a similar object, while RB-VLA infers stage completion and continues the task. 

# _D. Low-Level Action Generation_ 

Low-level control is produced by a diffusion transformer policy that operates in latent space and is conditioned on the belief **b** _t_ , intent **I** _t_ , and a fused state representation **s** _t_ from the state encoder. This encoder fuses robot proprioception and DINOv2 image embeddings to the same dimensions, decoupling multimodal perception from belief- and intent-level reasoning. The policy samples action chunks from 


via iterative denoising, warm-started from the previously predicted action sequence with added low-variance Gaussian noise to improve sampling efficiency and temporal coherence. Actions are executed in a receding-horizon manner at high frequency (50 Hz), enabling smooth, closed-loop control under partial observability without reliance on dense semantic inference. 

# IV. DATASET AND TRAINING 

We use a staged training pipeline for the vision–language module, the belief model, and the diffusion controller. The Belief transformer is first trained with the self-supervised objectives described in III-B. The intent extraction layers and the diffusion policy are trained jointly. All models are trained using mixed precision and gradient accumulation. 

# _A. Dataset_ 

Training uses 40,000 simulated manipulation trajectories ( _∼_ 40M timesteps) across 10 tasks, collected in RoboSuite, LIBERO-Long, LIBERO-Object and a UR5 MuJoCo environment. The dataset spans single and multi-object pick-andplace under occlusion, multi-block stacking in RoboSuite, and household tasks in LIBERO such as placing objects into drawers and cabinets. In practice, we observe that the belief converges reliably using a moderate number of trajectories, as the model focuses on learning control-relevant dynamics and action-conditioned state transitions rather than improving dense per-step semantic reasoning. We further finetune the belief and diffusion model with real-world manipulation tasks, adapting to sensor noise and unmodeled dynamics. During training, RGB observations are augmented with random brightness/contrast jitter, additive Gaussian noise, and minor spatial cropping to improve robustness and encourage learning of task-relevant state information. 

# _B. Training details_ 

The belief model uses a DINOv2 ViT-S/14 vision encoder and produces a 256-dimensional belief state from multimodal tokens. Temporal integration in the belief transformer uses a fixed window of _K_ = 5 frames. The belief module contains 150M parameters and is trained for 80k iterations with batch size 128 and learning rate 1 _e_<sup>_−_4</sup> . The VLM is initialized from Qwen2.5-VL-7B [41] and remains frozen during training. We replace the original language head with a lightweight intent extraction module, which is trained on top of the frozen VLM to produce a 256-dimensional continuous intent vector. 

The extracted intent, together with the 256-dimensional belief state, conditions the diffusion policy. The diffusion controller has 120M parameters and uses a DDPM objective with 100 steps to predict 16-step action chunks. It is trained for 100K iterations with batch size 32 and a learning rate 1e-4. All experiments are run on 12 NVIDIA A100 GPUs (80GB) using distributed data parallel training. 

# V. RESULTS 

Recursive Belief VLA (RB-VLA) is evaluated in simulation and the real world, using RoboSuite and LIBERO-Long. The evaluation focuses on: (a) Long-horizon tasks; (b) Latency and memory growth; (c) Belief representation analysis; (d) Ablation studies; (e) Real world tasks. 

# _A. Long Horizon Tasks_ 

We evaluate RB-VLA on long-horizon, multi-stage manipulation tasks with and without occlusion, assessing robustness under partial observability as well as sustained task progression over extended horizons. Experiments are conducted in RoboSuite and LIBERO-Long environments. 

We ran 40 trials per task with different random seeds. Robustness was evaluated at inference by randomizing object identities and placements, environment configurations, lighting conditions, object order, as well as introducing dropped frames and observation noise. Performance is measured by task success rate, defined as completing the task within a fixed horizon without collisions or premature termination. Quantitative results for two-object pick and place under occlusion and stacking are reported in Table I. RB-VLA achieves 

TABLE I: Long-horizon success rates (%) 

|Method|Single P&P|Multi P&P|Single Stack|Multi Stack|
|---|---|---|---|---|
|GROOT-N1|52.5|20.0|65.0|32.5|
|OpenVLA|22.5|_×_|_×_|_×_|
|_π_0|55.0|25.0|67.5|42.5|
|RB-VLA (ours)|**82.5**|**77.5**|**85.0**|**80.0**|


substantially higher performance across all long-horizon tasks, exceeding _π_ 0 by 52.5% and GROOT-N1 by 57.5% on multistage pick-and-place under partial observability, while OpenVLA fails to complete the task in this setting. These baselines repeatedly invoke VLMs for step-wise semantic reasoning, but lack awareness of task progression in multi-stage tasks and lose object or state awareness under occlusion. Beliefbased models address this limitation by capturing temporal dynamics and enabling causal reasoning, whereas VLMs are primarily used for semantic inference. This demonstrates that belief-based state estimation is crucial for robust long-horizon task execution. 

Figure 3 illustrates representative multi-stage executions in which earlier object interactions become occluded. The learned belief state preserves the necessary context to disambiguate visually similar objects and maintain consistent task progression. 

# _B. Latency and Memory Analysis_ 

We evaluate computational efficiency using latency and memory, with all inference measurements performed on one NVIDIA A100 GPU. Figure 4 compares the average episode latency of RB-VLA with prior methods. Since task instructions and semantic goals remain fixed within an episode, RB-VLA queries the VLM only once at the beginning of the task to obtain the intent embedding, and does not re-invoke it during execution. As a result, RB-VLA achieves over five times lower latency than stateless OpenVLA and RT1-X, and is more than three times faster than multi-frame GR00TN1, which repeatedly processes multiple visual frames. This demonstrates that decoupling semantic grounding from control enables efficient real-time deployment. 

Many VLA systems maintain temporal context by accumulating multiple past frames or memory tokens, causing memory and compute to scale with interaction horizon. Table II shows that both large VLM backbones (Qwen2-VL-7B) and end-to-end VLA systems (GR00T-N1) exhibit superlinear memory growth as the number of observed frames increases. In contrast, RB-VLA recursively compresses all task-relevant interaction history into a fixed-size belief state, yielding constant memory usage independent of episode length and enabling scalable long-horizon control. 

|**Temporal Context**|**Qwen2-VL-7B**|**GR00T-N1**|**RB-VLA (Ours)**|
|---|---|---|---|
|1 frame|1_._00_×_|1_._00_×_|1_._0_×_|
|2 frames|1_._81_×_|2_._21_×_|1_._0_×_|
|4 frames|3_._64_×_|3_._85_×_|1_._0_×_|
|8 frames|6_._82_×_|7_._12_×_|1_._0_×_|


TABLE II: Relative memory usage as a function of temporal context length, comparing RB-VLA with baseline models. 

# _C. Belief Representation Analysis_ 

We evaluate belief quality by sampling pairs of belief states and testing whether proximity in belief space predicts similarity in future dynamics and control behavior. For each pair, we compute cosine similarity between their belief representations and compare it to (i) the _ℓ_ 2 distance between the corresponding future action sequences and (ii) the cosine similarity between their future visual feature representations. Unlike stage-labeled analysis with discrete phases (e.g., grasp, transport, place), manipulation dynamics evolve smoothly, thus belief quality is reflected in predictive consistency rather than phase separability. 

As shown in Fig. 5, belief similarity exhibits a strong monotonic relationship with both future visual similarity (Pearson _r_ = 0 _._ 78) and future action similarity ( _r_ = 0 _._ 87). The shaded red region represents the variance, with _σ_ bottom 20% = 2 _._ 3 _σ_ top 20%, indicating that similar beliefs encode consistent underlying dynamics and lead to similar action outcomes and future observations, while dissimilar beliefs correspond to different dynamical regimes, admitting multiple plausible future trajectories. This provides evidence that the belief 


Fig. 3: **Long-horizon tasks under partial observability** . After the first object is placed and becomes occluded, the model correctly selects the subsequent target despite visually similar objects, avoiding re-grasping the same object. 


Fig. 4: Average inference latency per episode for RB-VLA and baseline VLA methods. 

acts as a latent action-conditioned dynamical state, governing future closed-loop evolution under control. 

To analyze stochasticity, we fix a belief state _bt_ and sample multiple latent variables _zt ∼ p_ ( _zt | bt_ ). Figure 6 shows that different latent samples produce diverse yet structured future predictions, indicating that the belief encodes sharp underlying dynamics while _zt_ captures uncertainty and multimodality over plausible future evolutions. The KL divergence stabilizes at a non-zero value, indicating sustained usage of _zt_ and preventing collapse to a single averaged future. These results demonstrate that the belief filters perceptual noise and preserves controlrelevant structure. 

Figure 7 visualizes attention weights at timesteps where the manipulated object becomes occluded. The belief attends to its recursive state and causally informative past frames, adaptively retaining relevant dynamical history while discarding irrelevant information for future prediction. 

# _D. Ablation Study_ 

We ablate key components by selectively removing them and measuring the drop in average success rate over 40 episodes on the same long-horizon, multi-stage tasks under partial observability. Starting from the full RB-VLA, we evaluate: (i) no frame-encoder targets for training the belief (using only vision embeddings), (ii) deterministic belief without stochastic latent variables, and (iii) no belief–policy conditioning. As shown in Table III, each removal degrades 


Fig. 5: (a) Future _ℓ_ 2 action divergence versus belief cosine similarity. (b) Future observation cosine similarity versus belief cosine similarity. Both plots exhibit strong monotonic correlation, indicating that proximity in belief space predicts similarity in future perception and control behavior. 

performance, with the lowest performance when belief is decoupled from control (a standard DiT policy) and the highest success achieved by the full RB-VLA. This highlights the need for a dynamics-grounded belief state, since diffusion model alone lacks the dynamics-consistent causal state required for long-horizon, multi-stage behavior. 

# _E. Real World Deployment_ 

We deploy RB-VLA on a physical UR5 manipulator under conditions closely matching the UR5 MuJoCo setup used in simulation. The model successfully transfers to real hardware without architectural changes, demonstrating effective sim-to- 


Fig. 6: (i) Future divergence using cosine distance with multiple sampled latent variables ( _n_ = 16) from a fixed belief state _bt_ , illustrating stochastic rollout diversity. (ii) KL divergence loss across training, showing stable convergence of the belief model’s latent distribution. 


Fig. 7: Normalized self attention weights of the temporal transformer over the previous recursive belief token and short history of input frame encoder tokens, indicating which tokens contribute to the belief state at time _t_ 

real transfer. The diffusion policy is further fine-tuned on 100 real-world trajectories to adapt to sensor noise and unmodeled dynamics. Using the learned belief representation, the system achieves reliable long-horizon execution on multi-object pickand-place tasks under partial observability, maintaining low inference latency and stable closed-loop control despite visual noise and actuation variability. Over 25 real-world trials, RB- 

TABLE III: Component Ablation on Two-Object Pick-andPlace task. Average success rate over 40 episodes under partial observability. 

|**Frame Encoder**|**Stoch.**|_z_<br>**Belief**_→_**Policy**|**Success**|
|---|---|---|---|
|_×_|_×_|_×_|32.5|
|_×_|_×_|✓|57.5|
|_×_|✓|✓|62.5|
|✓|✓|✓|**77.5**|


VLA achieves 68.0% success rate, successfully completing grasp–transport–place cycles without manual intervention. Fig- 


Fig. 8: Real World UR5 setup 

ure 8 illustrates the real-world setup. An Intel RealSense D435i RGB camera is mounted to capture the gripper and workspace, and five objects of varying shapes and colors are placed in randomized configurations. Only RGB images are used for perception. After placement, the first object becomes fully occluded and is no longer visible in the camera view. Tasks are specified through natural language instructions describing the target object and goal location. 

# VI. CONCLUSION AND FUTURE WORK 

We presented RB-VLA, a belief conditioned vision language action framework for long-horizon manipulation under partial observability. By maintaining a compact, actionconditioned belief state, the system preserves task progress and interaction history without growing memory, enabling robust multi-stage control with reduced latency. The architecture can be integrated into large pretrained VLAs as a fine-tuning layer for scalable robotic manipulation. 

Future work will focus on scaling data and task diversity, integrating reinforcement learning for improved recovery behaviors, and extending the belief framework to support greater adaptability in dynamic environments. 

# VII. ACKNOWLEDGMENTS 

We would like to thank Nikshep Grampurohit for his valuable contributions in refining the core ideas of this work. The authors also express great gratitude to Prof. Rengaswamy Jayaganthan for his constant support. 

REFERENCES 

- [1] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi _et al._ , “Openvla: An opensource vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

- [2] A. Ye, Z. Zhang, B. Wang, X. Wang, D. Zhang, and Z. Zhu, “Vla-r1: Enhancing reasoning in vision-language-action models,” _arXiv preprint arXiv:2510.01623_ , 2025. 

- [3] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

- [4] H. Jang, S. Yu, H. Kwon, H. Jeon, Y. Seo, and J. Shin, “Contextvla: Vision-language-action model with amortized multi-frame context,” _arXiv preprint arXiv:2510.04246_ , 2025. 

- [5] M. Lin, P. Ding, S. Wang, Z. Zhuang, Y. Liu, X. Tong, W. Song, S. Lyu, S. Huang, and D. Wang, “Hif-vla: Hindsight, insight and foresight through motion representation for vision-language-action models,” _arXiv preprint arXiv:2512.09928_ , 2025. 

- [6] X. Wang, X. Gao, J. Fu, Z. Li, D. Fortier, G. Mullins, A. Kolobov, and B. Guo, “Lola: Long horizon latent action learning for general robot manipulation,” _arXiv preprint arXiv:2512.20166_ , 2025. 

- [7] F. Xu, G. Zhai, X. Kong, T. Fu, D. F. Gordon, X. An, and B. Busam, “Stare-vla: Progressive stage-aware reinforcement for fine-tuning visionlanguage-action models,” _arXiv preprint arXiv:2512.05107_ , 2025. 

- [8] Y. Ji, H. Tan, J. Shi, X. Hao, Y. Zhang, H. Zhang, P. Wang, M. Zhao, Y. Mu, P. An _et al._ , “Robobrain: A unified brain model for robotic manipulation from abstract to concrete,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 1724–1734. 

- [9] C. Chen, Y.-F. Wu, J. Yoon, and S. Ahn, “Transdreamer: Reinforcement learning with transformer world models,” _arXiv preprint arXiv:2202.09481_ , 2022. 

- [10] Q. Gao, X. Pi, K. Liu, J. Chen, R. Yang, X. Huang, X. Fang, L. Sun, G. Kishore, B. Ai _et al._ , “Do vision-language models have internal world models? towards an atomic evaluation,” _arXiv preprint arXiv:2506.21876_ , 2025. 

- [11] Y. Feng, J. Han, Z. Yang, X. Yue, S. Levine, and J. Luo, “Reflective planning: Vision-language models for multi-stage long-horizon robotic manipulation,” _arXiv preprint arXiv:2502.16707_ , 2025. 

- [12] K. Wang, P. Zhang, Z. Wang, Y. Gao, L. Li, Q. Wang, H. Chen, C. Wan, Y. Lu, Z. Yang _et al._ , “Vagen: Reinforcing world model reasoning for multi-turn vlm agents,” _arXiv preprint arXiv:2510.16907_ , 2025. 

- [13] J. Cen, C. Yu, H. Yuan, Y. Jiang, S. Huang, J. Guo, X. Li, Y. Song, H. Luo, F. Wang _et al._ , “Worldvla: Towards autoregressive action world model,” _arXiv preprint arXiv:2506.21539_ , 2025. 

- [14] D. Li, Y. Zhang, M. Cao, D. Liu, W. Xie, T. Hui, L. Lin, Z. Xie, and Y. Li, “Towards long-horizon vision-language-action system: Reasoning, acting and memory,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2025, pp. 6839–6848. 

- [15] J. Zhang, C. Mu, X. Xu, and L. Ren, “A hierarchical vision-language and reinforcement learning framework for robotic task and motion planning in collaborative manipulation,” _IEEE Robotics and Automation Letters_ , vol. 11, no. 1, pp. 65–72, 2025. 

- [16] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu _et al._ , “Rt-1: Robotics transformer for real-world control at scale,” _arXiv preprint arXiv:2212.06817_ , 2022. 

- [17] M. J. Kim, C. Finn, and P. Liang, “Fine-tuning vision-languageaction models: Optimizing speed and success,” _arXiv preprint arXiv:2502.19645_ , 2025. 

- [18] W. Song, J. Chen, P. Ding, H. Zhao, W. Zhao, Z. Zhong, Z. Ge, J. Ma, and H. Li, “Accelerating vision-language-action model integrated with action chunking via parallel decoding,” _arXiv preprint arXiv:2503.02310_ , 2025. 

- [19] Y. Yang, Y. Wang, Z. Wen, L. Zhongwei, C. Zou, Z. Zhang, C. Wen, and L. Zhang, “Efficientvla: Training-free acceleration and compression for vision-language-action models,” _arXiv preprint arXiv:2506.10100_ , 2025. 

   - [21] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang _et al._ , “Gr00t n1: An open foundation model for generalist humanoid robots,” _arXiv preprint arXiv:2503.14734_ , 2025. 

   - [22] K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. R. Equi, C. Finn, N. Fusai, M. Y. Galliker _et al._ , “Pi-0.5: A visionlanguage-action model with open-world generalization,” in _9th Annual Conference on Robot Learning_ , 2025. 

   - [23] Y. Yang, J. Sun, S. Kou, Y. Wang, and Z. Deng, “Lohovla: A unified vision-language-action model for long-horizon embodied tasks,” _arXiv preprint arXiv:2506.00411_ , 2025. 

   - [24] Y. Fan, P. Ding, S. Bai, X. Tong, Y. Zhu, H. Lu, F. Dai, W. Zhao, Y. Liu, S. Huang _et al._ , “Long-vla: Unleashing long-horizon capability of vision language action model for robot manipulation,” _arXiv preprint arXiv:2508.19958_ , 2025. 

   - [25] M. Zawalski, W. Chen, K. Pertsch, O. Mees, C. Finn, and S. Levine, “Robotic control via embodied chain-of-thought reasoning,” _arXiv preprint arXiv:2407.08693_ , 2024. 

   - [26] C.-P. Huang, Y.-H. Wu, M.-H. Chen, Y.-C. F. Wang, and F.-E. Yang, “Thinkact: Vision-language-action reasoning via reinforced visual latent planning, 2025,” _URL https://arxiv. org/abs/2507.16815_ , 2025. 

   - [27] Q. Zhao, Y. Lu, M. J. Kim, Z. Fu, Z. Zhang, Y. Wu, Z. Li, Q. Ma, S. Han, C. Finn _et al._ , “Cot-vla: Visual chain-of-thought reasoning for vision-language-action models,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 1702–1713. 

   - [28] J. Li, Y. Zhu, Z. Tang, J. Wen, M. Zhu, X. Liu, C. Li, R. Cheng, Y. Peng, Y. Peng _et al._ , “Coa-vla: Improving vision-language-action models via visual-text chain-of-affordance,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2025, pp. 9759–9769. 

   - [29] M. T. Spaan, “Partially observable markov decision processes,” in _Reinforcement learning: State-of-the-art_ . Springer, 2012, pp. 387–414. 

   - [30] L. Xiao, J. Li, J. Gao, F. Ye, Y. Jin, J. Qian, J. Zhang, Y. Wu, and X. Yu, “Ava-vla: Improving vision-language-action models with active visual attention,” _arXiv preprint arXiv:2511.18960_ , 2025. 

   - [31] M. Koo, D. Choi, T. Kim, K. Lee, C. Kim, Y. Seo, and J. Shin, “Hamlet: Switch your vision-language-action model into a history-aware policy,” _arXiv preprint arXiv:2510.00695_ , 2025. 

   - [32] Z. Liu, Z. Yang, Z. Zhang, and H. Tang, “Evovla: Self-evolving visionlanguage-action model,” _arXiv preprint arXiv:2511.16166_ , 2025. 

   - [33] J. Cen, S. Huang, Y. Yuan, H. Yuan, C. Yu, Y. Jiang, J. Guo, K. Li, H. Luo, F. Wang _et al._ , “Rynnvla-002: A unified vision-language-action and world model,” _arXiv preprint arXiv:2511.17502_ , 2025. 

   - [34] Z. Liu, Y. Gu, S. Zheng, X. Xue, and Y. Fu, “Trivla: A unified triplesystem-based unified vision-language-action model for general robot control,” _arXiv preprint arXiv:2507.01424_ , 2025. 

   - [35] Q. Lv, W. Kong, H. Li, J. Zeng, Z. Qiu, D. Qu, H. Song, Q. Chen, X. Deng, and J. Pang, “F1: A vision-language-action model bridging understanding and generation to actions,” _arXiv preprint arXiv:2509.06951_ , 2025. 

   - [36] L. P. Kaelbling and T. Lozano-P´erez, “Integrated task and motion planning in belief space,” _The International Journal of Robotics Research_ , vol. 32, no. 9-10, pp. 1194–1227, 2013. 

   - [37] Z. Chen _et al._ , “Bayesian filtering: From kalman filters to particle filters, and beyond,” _Statistics_ , vol. 182, no. 1, pp. 1–69, 2003. 

   - [38] S. Chaudhry, “Semantic belief-state world model for 3d human motion prediction,” _arXiv preprint arXiv:2601.03517_ , 2026. 

   - [39] M. Oquab, T. Darcet, T. Moutakanni, H. Vo, M. Szafraniec, V. Khalidov, P. Fernandez, D. Haziza, F. Massa, A. El-Nouby _et al._ , “Dinov2: Learning robust visual features without supervision,” _arXiv preprint arXiv:2304.07193_ , 2023. 

   - [40] D. Chen, M. Shukor, T. Moutakanni, W. Chung, J. Yu, T. Kasarla, A. Bolourchi, Y. LeCun, and P. Fung, “Vl-jepa: Joint embedding predictive architecture for vision-language,” _arXiv preprint arXiv:2512.10942_ , 2025. 

   - [41] S. Bai, K. Chen, X. Liu, J. Wang, W. Ge, S. Song, K. Dang, P. Wang, S. Wang, J. Tang _et al._ , “Qwen2. 5-vl technical report,” _arXiv preprint arXiv:2502.13923_ , 2025. 

- [20] P. K. A. Vasu, F. Faghri, C.-L. Li, C. Koc, N. True, A. Antony, G. Santhanam, J. Gabriel, P. Grasch, O. Tuzel _et al._ , “Fastvlm: Efficient vision encoding for vision language models,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 19 769– 19 780. 

