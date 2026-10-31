---
title: "CoFreeVLA: Short-Horizon Collision-Free Dual-Arm Manipulation via Vision-Language-Action Model and Risk Estimation"
date: "2026-01-29"
authors: "Yaohua Liu; Binkai Ou; Hengjun Zhang"
url: https://arxiv.org/abs/2601.21712
pdf: https://arxiv.org/pdf/2601.21712
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.21712)** / [論文ページ](https://arxiv.org/abs/2601.21712)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

CoFreeVLA: Short-Horizon Collision-Free DualArm Manipulation via Vision-Language-Action Model and Risk Estimation 

Yaohua Liu<sup>1</sup> , Binkai Ou<sup>2</sup> , Hengjun Zhang<sup>3*</sup> 

> 1Chinese Medicine Guangdong Laboratory, Hengqin, Zhuhai, 519031, Guangdong, China. 

> 2BoardWare Information System Company, Macau, 999078, China. 

> 3School of Electronic Engineering and Automation, Guilin University of Electronic Technology, Guilin, 541000, Guangxi, China. 

*Corresponding author(s). E-mail(s): zhanghengjun@guet.edu.cn; Contributing authors: liuyaohua@hqcmlab.cn; yoanmike666@gmail.com; 

### **Abstract** 

Vision–Language–Action (VLA) models enable instruction-following manipulation, yet their deployment on coordinated dual-arm platforms remains severely constrained by under-modeled self-collisions between manipulators and grasped objects. To address this critical safety gap, we propose CoFreeVLA, a novel framework that augments end-to-end VLA policies with a lightweight, shorthorizon self-collision risk estimator. The estimator predicts collision likelihoods directly from proprioceptive states, visual embeddings, and candidate action sequences. Deeply integrated into the closed-loop control system, this estimator proactively gates risky commands, autonomously synthesizes recovery trajectories to safe states via risk-guided adjustments, and biases policy refinement for safer rollouts. To ensure robust calibration, the estimator utilizes a two-stage training pipeline: pre-training with model-based synthetic collision labels, followed by post-training on real-robot rollouts. Across five bimanual tasks, six VLA backbones, and 30 trials per variant, the task-averaged collision rate decreases from 0.54 to 0.23, while the task-averaged success rate increases from 0.45 to 0.61. Compared to representative baselines, CoFreeVLA substantially reduces selfcollision frequencies and improves overall task success rates, providing a crucial step toward the safe deployment of foundational models in multi-arm continuous control. 

**Keywords:** Robot Manipulation, Vision-Language-Action Model, Collision Avoidance 

1 

# **1 Introduction** 

Vision–Language–Action (VLA) models have recently emerged as a powerful paradigm for robotic control, demonstrating remarkable capabilities in grounding natural language instructions into visual observations and executable actions [1–5]. While these models have shown impressive generalization in single-arm manipulation tasks, extending them to dual-arm systems introduces new challenges. Dual-arm manipulation requires coordination across two high-degree-of-freedom manipulators, making spatial reasoning and safety-critical planning considerably more complex [6–8]. Existing approaches largely focus on avoiding external collisions with the environment or task objects—via classical trajectory optimization and widely deployed toolchains—yet self-collisions between the two arms or between an arm and a grasped object remain underexplored in end-to-end VLA settings [9–15]. Such self-collisions can result in task failure, hardware damage, or unsafe behaviors, and therefore pose a fundamental obstacle to deploying VLA-based dual-arm systems in real-world environments. 

Classical motion planners and engineering toolchains have been widely used to avoid collisions with the environment and with task objects [9, 10, 13–15]. Those approaches are effective for planning geometry-aware trajectories but typically operate in separate modules from learned VLA policies, which limits the responsiveness and end-to-end adaptability of learned controllers. In particular, self-collisions between the two arms and collisions involving a grasped object are often overlooked in end-toend VLA pipelines despite being frequent causes of task interruption, hardware stress, and unsafe behavior. This gap is especially consequential for real-world dual-arm deployment where perceptual uncertainty, kinematic calibration errors, and dynamic interactions with objects raise the risk of unintended contact. 

To address this gap, we propose CoFreeVLA, a risk-aware VLA framework designed for collision-free dual-arm manipulation. At the core of CoFreeVLA is a self-collision risk estimator that predicts the likelihood of future collisions given the current observation and planned actions from the VLA policy. This risk estimator is integrated into the control loop in three complementary ways: (i) by halting unsafe actions before collisions occur, (ii) by guiding the system to recover toward safe configurations when risk is detected, and (iii) by refining the VLA policy itself through optimization with risk-aware feedback. By embedding explicit collision reasoning into VLA decision-making—complementary to classical safety layers such as control barrier functions [16, 17]—CoFreeVLA enables safer and more reliable dual-arm manipulation without sacrificing task performance. 

We evaluate CoFreeVLA across a set of dual-arm manipulation tasks that highlight the need for safe spatial reasoning, including handover, cooperative grasping, and assembly [18–20]. To train and validate the risk estimator, we employ a twostage strategy: pre-training with synthetic collision data generated from a model-based checker [11–13], followed by post-training with real-robot rollouts under VLA policies. Our experiments assess both the predictive accuracy of the risk estimator and the downstream benefits of risk-aware policy refinement. We benchmark CoFreeVLA against recent dual-arm learning baselines, including APEX and RDT-1B [21, 22], on an AgileX-based dual-arm platform [23], measuring performance in terms of task success, collision rate, and recovery effectiveness. 

2 

In summary, our contributions are as follows: 

1. We propose CoFreeVLA, a framework that addresses the overlooked problem of inter-arm and arm–object collision in dual-arm VLA-based manipulation. 

2. We design a self-collision risk estimator that predicts collision likelihood from visual observations and action sequences, and integrate it into execution, recovery, and policy refinement. 

3. We conduct extensive experiments on dual-arm manipulation tasks, validating the effectiveness of CoFreeVLA in reducing risky collisions while maintaining task performance. 

The remainder of this paper is organized as follows. Section 2 reviews VLA models and collision avoidance. Section 3 formulates the control problem and presents CoFreeVLA, including estimation, recovery, and training. Section 4 evaluates transferability, task-level safety, ablations, and real-time control. Section 5 summarizes the findings and discusses future directions. 

# **2 Related Work** 

## **2.1 Vision–Language–Action Models** 

Vision–language–action models combine visual–linguistic representations with learned control policies to map natural-language instructions and sensory observations to robot actions. Early systems established this paradigm by transferring large-scale multimodal knowledge to embodied control. RT-2 connected web-scale vision–language pretraining to end-to-end robotic actions, while PaLM-E incorporated visual, linguistic, and proprioceptive inputs for embodied reasoning [1, 2]. Octo and OpenVLA subsequently scaled generalist policy learning through heterogeneous robot data and open-source pretraining, respectively [3, 4]. Compact models such as TinyVLA target lower inference cost and improved data efficiency through lightweight multimodal backbones and diffusion-based action decoding [24]. 

_π_ 0.5 extends this direction through co-training on heterogeneous multi-robot and multimodal data, with high-level semantic supervision supporting long-horizon manipulation [25]. SmolVLA focuses on accessible deployment through asynchronous inference and chunked action generation on consumer hardware [26]. Other recent efforts address cross-embodiment transfer and decoding efficiency: X-VLA uses embodimentspecific soft prompts, PD-VLA accelerates action-chunk decoding through parallel fixed-point iterations, and UniVLA learns task-centric latent actions from heterogeneous videos [27–29]. SayCan further influenced VLA design by using language-model affordances for skill selection [5]. Despite these advances in instruction following, generalization, and efficiency, existing VLA policies typically rely on data priors or external planning modules for safety and do not explicitly forecast imminent self-collision from perceptual inputs and candidate dual-arm actions. CoFreeVLA addresses this gap by coupling a compact risk predictor with execution-time gating and recovery. 

3 

## **2.2 Collision Avoidance for Robot Manipulation** 

Collision avoidance in manipulation spans geometric planning, collision detection, feedback control, and learned motion generation. Functional-gradient planning and sequential convex optimization incorporate distance costs into trajectory generation, while GPU-oriented toolchains accelerate parallel collision queries and constrained replanning [9, 10, 13, 30]. Robot-collision surveys further emphasize detection under sensing and model uncertainty rather than geometric post-processing alone [31]. This issue is particularly important for dual-arm systems, where links, grippers, and grasped objects can collide during otherwise task-valid motions. 

At the control level, control-barrier-function filters provide formal set-invariance guarantees, and collision-free model-predictive control extends safety constraints to whole-body motion [16, 17, 32]. Dual-arm systems have been addressed through kinematic avoidance rules, MoveIt extensions, neural self-collision controllers, and spatiotemporal diffusion policies [14, 15, 33, 34]. Other learning-based approaches combine collision-aware representations with bimanual action generation, including VLM-assisted flow-diffusion, manipulability-aware diffusion, and collision-free latent motion generation [21, 35, 36]. Learned collision detectors can complement geometric checkers in cluttered scenes [37, 38]. However, these methods typically plan in geometric state spaces, intervene at the low-level controller, or generate collision-aware actions without forecasting imminent self-collision from perceptual inputs and candidate VLA actions. CoFreeVLA addresses this gap by coupling a compact risk predictor with execution gating, recovery, and policy refinement. 

# **3 Methodology** 

## **3.1 Problem formulation** 

We consider a dual-arm manipulator whose left and right arms have _nL_ and _nR_ degrees of freedom, respectively. At time _t_ , its joint configuration is 


subject to the prescribed joint-position and joint-velocity limits. For each arm _k ∈ {L, R}_ , let _x_<sup>_k_</sup> _t_<sup>_∈SE_(3)denotetheend-effectorposeand</sup><sup>_g_</sup> _t_<sup>_k_thegripperstate.The</sup> action consists of Cartesian increments of the two end-effectors, 


which we identify with the control command as _at ≡_ ∆ _xt._ The decision state is defined as 


where _xt_ and _gt_ collect the end-effector poses and gripper states of both arms, respectively, and _ot_ comprises onboard perceptual observations, such as RGB-D data, together with the task instruction. An end-to-end vision–language–action policy 

4 


**Fig. 1 (a) Risk Estimator.** Given a state–action pair, the model applies a cross-attention module followed by three heads to predict collision risk _r_ , minimum distance _d_ , and time-to-collision _τ_ . **(b) Data Collection** and **(c) Dataset.** For each state, we sample candidate actions and check their outcomes for labeling. **(d) CoFree VLA.** At run time, the system continuously estimates risk; when it exceeds a threshold, the policy will be blocked and the arms will be returned to a safe configuration, after which the policy resumes to complete the task. 

maps images, language, and proprioceptive measurements to executable actions. Its stochastic form is expressed as 


or, equivalently, its deterministic implementation can be written as 


## **3.2 Self-collision risk estimator** 

As in Fig. 1(a), the estimator takes the current dual-arm state and a short-horizon plan as input. We form the action sequence _At_ : _t_ + _H−_ 1 from the VLA policy, pair it with proprioceptive state ( _xt, gt_ ), and a visual embedding _zt_ = _f_ VLA( _ot_ ) from the VLA backbone. The estimator predicts a calibrated self-collision risk _r_ ˆ _t_ and optionally geometric surrogates such as the minimum inter-body distance _d_<sup>ˆ</sup> min (mm) and timeto-collision _τ_ ˆttc (s), produced by auxiliary heads: 


The model architecture encodes inputs as two parallel streams: (i) an observation stream and (ii) an action stream. The observation stream encodes a compact feature _zt_ taken from the penultimate VLA image token together with the proprio state ( _xt, gt_ ); the action stream encodes _At_ : _t_ + _H−_ 1 as a length- _H_ token sequence with positional encodings. A lightweight temporal encoder (MLP for small _H_ , or a small Transformer for _H ≥_ 5) fuses the two streams via cross-attention, followed by pooling and prediction 

5 

heads for _r_ ˆ _t_ , _d_<sup>ˆ</sup> min, and _τ_ ˆttc. We apply temperature scaling to calibrate _r_ ˆ _t_ , and size the network for sub-5 ms inference so it can run at control rates (10–50 Hz). As illustrated in Fig. 1(b) and (c), we construct a dataset 


where _yt_ = _{yt_<sup>bin</sup> _, yt_<sup>_d, y_</sup> _t_<sup>ttc</sup><sup>_}_denotesthecorrespondinglabels.Duringpre-training,we</sup> use a model-based checker, such as a mesh-distance checker, to evaluate candidate action sequences _At_ : _t_ + _H−_ 1 generated by the VLA with added jitter. For each sequence, we record a binary indicator _yt_<sup>bin</sup> _∈{_ 0 _,_ 1 _}_ of whether a collision occurs within the horizon _H_ , the minimum inter-arm or arm–object distance _yt_<sup>_d_,andthefirsttimeto</sup> collision _yt_<sup>ttc.Weemphasizenear-collisioncasesbyoversamplingsampleswithsmall</sup> _yt_<sup>_d_.Duringpost-training,werelabelreal-robotrolloutsusingcontactevents,torque</sup> spikes, and visual overlap to account for calibration and grasp uncertainties. 

## **3.3 Collision-Free VLA Structure** 

As summarized in Algorithm 1, Collision-Free VLA operates in three stages: 1) risk estimation to stop unsafe actions, 2) recovery to safe states, and 3) policy optimization for collision-free control. 

**Risk estimation to stop.** In Fig. 1(d), at each control step, the VLA proposes a short-horizon plan _At_ : _t_ + _H−_ 1 = ( _at, . . . , at_ + _H−_ 1). We evaluate the self-collision risk _r_ ˆ _t_ = _Eϕ_ ( _st, At_ : _t_ + _H−_ 1) _∈_ [0 _,_ 1]. If _r_ ˆ _t > τ↑_ , execution of _at_ is blocked and the controller enters a protective mode; execution resumes only when ˆ _rt ≤ τ↓_ (hysteresis with _τ↓ < τ↑_ reduces chattering). As an optional soft gate when not blocked, commanded velocities are scaled by _αt_ = clip(1 _− r_ ˆ _t/τ↑,_ 0 _,_ 1) before sending to the low-level controller. 

**Recovery to safe states.** When blocked, we synthesize a short recovery sequence _A_<sup>rec</sup> _t_ : _t_ + _h−_ 1<sup>thatdrivesthesystemtowardtheself-safeset</sup><sup>_S_safe=</sup><sup>_{ q_:</sup><sup>_d_min(</sup><sup>_q_)</sup><sup>_≥d_0</sup><sup>_}_.</sup> We optimize a risk-shaped objective _A_<sup>rec</sup> _t_ : _t_ + _h−_ 1<sup>_←_arg min</sup><sup>_AEϕ_(</sup><sup>_st, A_) +</sup><sup>_λ∥A∥_2under</sup> joint and velocity limits, solved by a few projected-gradient steps. This locally reduces predicted collision risk; recovery terminates once _r_ ˆ _t ≤ τ↓_ for _K_ consecutive cycles. **Policy optimization for collision-free control.** Beyond online gating, we fine-tune the VLA with a safety-aware objective that trades off task intent against predicted risk. We minimize a surrogate that keeps the refined plan close to the original while lowering _Eϕ_ : min _θ_ E _st_ � _α ∥A_<sup>_′_</sup> _t_ : _t_ + _H−_ 1<sup>_−At_:</sup><sup>_t_+</sup><sup>_H−_1</sup><sup>_∥_2+</sup><sup>_β Eϕ_(</sup><sup>_st, A′_</sup> _t_ : _t_ + _H−_ 1<sup>)</sup> �, where _A_<sup>_′_</sup> _t_ : _t_ + _H−_ 1<sup>isobtainedbyrollingout</sup><sup>_fθ_(</sup><sup>_st_)for</sup><sup>_H_steps.Practically,weperform</sup> (i) supervised fine-tuning on a filtered dataset _D_ safe = _{_ ( _s, a_ ) : _Eϕ_ ( _s, At_ : _t_ + _H−_ 1) _≤ τ↓}_ with risk-weighted losses _w_ ( _s_ ) = exp( _−κ Eϕ_ ( _s, At_ : _t_ + _H−_ 1)), biasing the model toward a collision-free target distribution; and (ii) test-time action refinement by solving min _A′ α ∥A_<sup>_′_</sup> _− At_ : _t_ + _H−_ 1 _∥_<sup>2</sup> + _β Eϕ_ ( _st, A_<sup>_′_</sup> ) under control limits, then executing only the first optimized step to preserve reactivity. This balances task success with collision-free behavior. 

6 

## **3.4 Training Procedure for CoFreeVLA** 

**Risk estimator pre-training.** We first pre-train _Eϕ_ offline using model-based collision labels. Given a state _st_ , we generate horizon plans _At_ : _t_ + _H−_ 1 by rolling out the base VLA with beam variants and added jitter. We collect these plans in simulation and on the real robot operating in guard mode. For each pair ( _st, At_ : _t_ + _H−_ 1), meshdistance queries and a predictive checker provide three labels. The first is a binary indicator _yt_<sup>bin</sup> _∈{_ 0 _,_ 1 _}_ of collision within _H_ . The second is the minimum inter-arm or arm–grasped-object distance _yt_<sup>_d_(mm)overthehorizon.Thethirdisthefirsttime</sup> to collision _yt_<sup>ttc</sup> (s). The training objective combines binary cross-entropy (BCE) and regression terms: 


We address class imbalance by assigning higher weights to false negatives and oversampling near-miss samples with small _yt_<sup>_d_.Wealsoapplyahorizoncurriculumthat</sup> begins with a short _H_ and gradually increases it. After training, temperature scaling on a held-out set calibrates _r_ ˆ _t ∈_ [0 _,_ 1]. 

**Closed-loop fine-tuning.** We then adapt both _Eϕ_ and the VLA through safetysupervised closed-loop fine-tuning. With the risk gate ( _τ↑, τ↓_ ) enabled, we collect tuples ( _st, At_ : _t_ + _H−_ 1 _,_ ˆ _rt_ ) together with contact events and recovery-corrected actions. These data are aggregated in a DAgger-like buffer and support two updates. First, we posttrain _Eϕ_ on real-robot labels to account for calibration and grasp uncertainty. Second, we refine the VLA using the risk-weighted objective 


where _w_ ( _s_ ) = exp� _−κEϕ_ ( _s, At_ : _t_ + _H−_ 1)�. When available, pairwise preferences between safe and unsafe variants or a small reinforcement-learning term can provide an additional risk penalty. We tune the thresholds through receiver operating characteristic (ROC) analysis while prioritizing a low false-negative rate. Hysteresis suppresses chattering, and a watchdog halts execution if _r_ ˆ _t_ saturates. 

## **3.5 Implementation Notes** 

We use a PyBullet 3.2.6 digital twin with an EGL RGB-D renderer and the Flexible Collision Library (FCL), version 0.7.0 [13], for nominal pre-training. PyBullet advances the AgileX-based PIPER-style URDF scene and renders synchronized observations. FCL independently processes the corresponding inflated link and object meshes to generate collision and proximity labels. For simulation pre-training, robot-link and gripper meshes are loaded from the PIPER-style URDF package. Environment obstacles and task objects are represented by CAD meshes or dimension-matched primitives in the randomized digital twin. 

Each sample contains a scene, a joint state, a rendered RGB-D observation, and a candidate action chunk. We generate 200,000 samples and partition complete scene trajectories into 80% training, 10% calibration, and 10% test splits. This trajectory-level 

7 

**Algorithm 1** Collision-Free VLA Execution, Recovery, and Policy Refinement **Require:** policy _fθ_ , estimator _Eϕ_ , buffer _B_ , thresholds _τ↓ < τ↑_ , horizons _H, h_ , and termination window _K_ 1: observe _st_ = ( _xt, gt, ot_ ) and compute _zt_ = _f_ VLA( _ot_ ) 2: generate _N_ candidate plans _{A_<sup>(</sup> _t_ :<sup>_n_</sup> _t_<sup>)</sup> + _H−_ 1<sup>_}_</sup> _n_<sup>_N_</sup> =1<sup>from</sup><sup>_fθ_(</sup><sup>_st_)withbeamsearchand</sup> jitter 3: **for** each candidate _A_<sup>(</sup><sup>_n_)</sup> _t_ : _t_ + _H−_ 1<sup>**do**</sup> 4: evaluate _r_ ˆ _t_<sup>(</sup><sup>_n_)</sup> and, optionally, _d_<sup>ˆ(</sup> min<sup>_n_)</sup> _,t_<sup>and</sup><sup>_τ_ˆ (</sup> ttc<sup>_n_)</sup> _,t_ 5: **end for** 6: _n_<sup>_∗_</sup> _←_ arg min _n∈{_ 1 _,...,N }_ ˆ _rt_<sup>(</sup><sup>_n_)</sup> 7: _A_<sup>_∗_</sup> _t_ : _t_ + _H−_ 1<sup>_←A_(</sup> _t_ :<sup>_n_</sup> _t_<sup>_∗_</sup> +<sup>)</sup> _H−_ 1<sup>,</sup><sup>_r_ˆ</sup> _t_<sup>_∗←r_ˆ</sup> _t_<sup>(</sup><sup>_n∗_)</sup> 8: **if** _Eϕ_ is differentiable and the real-time budget permits **then** 9: refine _A_<sup>_∗_</sup> _t_ : _t_ + _H−_ 1<sup>by minimizing its deviation from the proposal and its predicted</sup> risk 10: reevaluate _r_ ˆ _t_<sup>_∗_,</sup><sup>_d_ˆ</sup><sup>_∗_</sup> min _,t_<sup>,and</sup><sup>_τ_ˆ</sup><sup>_∗_</sup> ttc _,t_ 11: **end if** 12: **if** _r_ ˆ _t_<sup>_∗≤τ↓_</sup><sup>**then**</sup> 13: execute the first action _a_<sup>_∗_</sup> _t_<sup>of</sup><sup>_A∗_</sup> _t_ : _t_ + _H−_ 1<sup>;set</sup><sup>_a_</sup> _t_<sup>exec</sup> _← a_<sup>_∗_</sup> _t_ 14: **else if** _r_ ˆ _t_<sup>_∗> τ↑_</sup><sup>**then**</sup> 15: solve _A_<sup>rec</sup> _t_ : _t_ + _h−_ 1<sup>_←_arg min</sup><sup>_A Eϕ_(</sup><sup>_st, A_) +</sup><sup>_λ∥A∥_2underthecontrollimits</sup> 16: execute its first action _a_<sup>rec</sup> _t_<sup>;set</sup><sup>_a_exec</sup> _t ← a_<sup>rec</sup> _t_ 17: keep recovery mode active until _r_ ˆ _t ≤ τ↓_ for _K_ consecutive cycles 18: **else** 19: _αt ←_ clip(1 _− r_ ˆ _t_<sup>_∗/τ↑,_0</sup><sup>_,_1)</sup> 20: execute _a_<sup>exec</sup> _t ← αta_<sup>_∗_</sup> _t_ 21: **end if** 22: append ( _st, A_<sup>_∗_</sup> _t_ : _t_ + _H−_ 1<sup>_, a_</sup> _t_<sup>exec</sup> _,_ ˆ _rt_<sup>_∗,d_ˆ</sup><sup>_∗_</sup> min _,t_<sup>_,_ˆ</sup><sup>_τ ∗_</sup> ttc _,t_<sup>)to</sup><sup>_B_</sup> 23: **if** a post-training update is scheduled **then** 24: update _Eϕ_ using the composite loss in Eq. (10) 25: update _fθ_ using the risk-weighted objective in Eq. (11) 26: **end if** 

partition prevents adjacent chunks from crossing splits. Candidate chunks comprise nominal policy actions, bounded perturbations that represent proposal and tracking variation, and boundary-seeking actions that increase coverage near small clearances. Cartesian increments are converted to joint trajectories using warm-started dampedleast-squares inverse kinematics. Chunks without a joint-limit-feasible solution are marked infeasible and never receive a safe label. 

For hardware adaptation, robot, tool, and task-object geometries are represented by calibrated copies of the corresponding URDF, CAD, or dimension-measured models. These models are aligned with the physical workspace through the robot and camera calibration transforms. Real RGB-D frames are consumed by the estimator and FCL replays measured joint and object poses against the calibrated geometries to provide model-based clearance and _τ_ ˆttc targets. Hardware adaptation initializes the 

8 

estimator from the nominal checkpoint and fine-tunes it on the 350 training rollouts for at most 30 epochs. The RGB-D encoder is frozen for the first three epochs to stabilize the geometric heads, after which all estimator layers are jointly updated. Training windows are sampled by rollout, with at most one window per control cycle; no window from the calibration or test partitions is used for optimization. The calibration split is used first for temperature scaling and then for selecting the frozen risk and _τ_ ˆttc operating points. Once these quantities are fixed, all estimator parameters and calibration values remain unchanged during closed-loop evaluation. 

As illustrated in Fig. 1(a), the risk estimator adopts a four-layer temporal Transformer backbone with a model width of 384 and eight attention heads. Prior to multimodal fusion, the observation and action streams are projected into this shared latent dimension. Each Transformer layer is equipped with pre-layer normalization, a gated feed-forward block, and a dropout rate of 0.1. The proprioceptive measurements together with _H_ standardized future actions are encoded as temporal tokens, which are further conditioned on the visual embedding _zt_ via cross-attention operations. The learned temporal representations are then shared across three task-specific prediction heads. Among them, the _d_<sup>ˆ</sup> min head and the _τ_ ˆttc head regress continuous physical quantities around collision boundaries, addressing the limitation that binary collision labels fail to characterize relative spatial proximity. 

All training runs use a single NVIDIA GeForce RTX 4090 GPU with 24 GB of memory. Synthetic pre-training uses AdamW with a batch size of 512 and a learning rate of 1 _×_ 10<sup>_−_4</sup> , whereas hardware adaptation uses batch size 64 and the same learning rate. In Eq. (10), we set _λ_ bce = 1 _._ 0, _λd_ = 0 _._ 5, and _λ_ ttc = 0 _._ 1. These weights balance binary collision classification against the two auxiliary geometric regression objectives. Pretraining takes approximately 3 h, whereas real-robot post-training takes approximately 45 min. 

At deployment, we run the VLA [22] at 10 Hz and the low-level controller at 30 Hz. The deployed action horizon is _H_ = 16. Using the calibration split described above, we select the risk thresholds, risk weight _κ_ , and recovery penalty _λ_ . We set _τ↑_ = 0 _._ 85 to trigger blocking and _τ↓_ = 0 _._ 30 to resume execution. This hysteresis reduces oscillatory switching during precision tasks. At each VLA update, _Eϕ_ evaluates _N_ beam-and-jitter candidates, and the controller executes the first action of the lowest-risk feasible sequence. We export _Eϕ_ to ONNX or TorchScript and prefetch _zt_ from the VLA backbone. These optimizations maintain a sub-5 ms forward pass on a CPU or GPU. When gradient-based refinement is unavailable, recovery uses a quadratic-programming/control-barrier-function (QP/CBF) fallback with constraints derived from the distance head. 

# **4 Experiment** 

## **4.1 Experiment Setup** 

All experiments are conducted on an AgileX-based PIPER-style bimanual mobile manipulator. To systematically evaluate the system, we select five representative bimanual tasks that span a wide spectrum of inter-arm interference and precision demands: 

9 


**Fig. 2** Experimental results in 5 dual-arm manipulation tasks. Evaluations of collision and success rates are on 30 trials 

- **Pour beans into cup:** High spatial overlap with a high risk of inter-arm and arm-object collisions. 

- **Hand over screwdriver:** Requires close-proximity coordination and dynamic object transfer. 

- **Put cups into bowl (Tubes):** Emphasizes spatial reasoning under restricted clearance. 

- **Remove pen cap & Nest two cups:** High-precision tasks demanding millimeterlevel alignment where arms must naturally operate in extreme proximity. 

We employ six structurally diverse baseline policies as the underlying action policies: two lightweight models, TinyVLA [24] and SmolVLA [26]; three representative vision–language–action (VLA) models, OpenVLA [4], RDT-1B [22], and _π_ 0.6 [39]; and a dual-arm-specific generative policy, APEX [21]. For each task and method variant, we conduct 30 trials. We report two primary metrics: the Collision Rate (CR), defined as the proportion of trials involving self-collision, and the Success Rate (SR), defined as the proportion of trials satisfying the task-completion criteria. Aggregated results are presented in Fig. 2. 

## **4.2 Self-Collision Risk Estimation** 

Table 1 and Fig. 2 show that the short-horizon risk estimator and execution gate improve both safety and task completion for every evaluated backbone. Averaged across the six backbones and five tasks, the task-averaged CR decreases from 0.54 to 0.23, corresponding to an absolute reduction of 0.31 (57.6%). Over the same trials, the task-averaged SR increases from 0.45 to 0.61, an absolute gain of 0.16 (34.5%). The consistent direction of these changes across all policy families indicates that the execution-time safety layer is not dependent on a particular VLA architecture. 

The backbone-level averages further quantify this consistency. CoFreeVLA reduces Avg. CR by 0.40 for TinyVLA, 0.35 for OpenVLA, 0.37 for RDT-1B, 0.28 for SmolVLA, 0.24 for _π_ 0.6, and 0.22 for APEX. The corresponding Avg. SR gains are 

10 

**Table 1** Collision Rates (CR _↓_ ) and Success Rates (SR _↑_ ) Across Diverse VLA Backbones on 5 Bimanual Tasks 

|**Backbone**|**Method Variant**|**Pouri**|**ng Beans**|**Pen Ca**|**p Removal**|**Tool **|**Handover**|**Tubes **|**Placement**|**Cups **|**Nesting**|**Ave**|**rage**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||CR|SR|CR|SR|CR|SR|CR|SR|CR|SR|**CR**|**SR**|
|**TiVLA**|Vanilla|0.93|0.20|0.40|0.33|0.73|0.43|0.80|0.40|0.63|0.27|0.70|0.33|
|**ny**|**+ CoFreeVLA**|0.32|0.40|0.28|0.50|0.30|0.57|0.29|0.53|0.31|0.43|**0.30**|**0.49**|
|**OVLA**|Vanilla|0.87|0.27|0.37|0.40|0.60|0.53|0.67|0.47|0.47|0.33|0.60|0.40|
|**pen**|**+ CoFreeVLA**|0.30|0.43|0.24|0.57|0.27|0.67|0.20|0.63|0.22|0.50|**0.25**|**0.56**|
|**RDT1B**|Vanilla|0.80|0.28|0.33|0.39|0.70|0.52|0.73|0.47|0.53|0.34|0.62|0.40|
|**-**|**+ CoFreeVLA**|0.30|0.43|0.21|0.58|0.26|0.66|0.23|0.63|0.27|0.50|**0.25**|**0.56**|
|**SlVLA**|Vanilla|0.73|0.30|0.29|0.47|0.50|0.60|0.57|0.53|0.40|0.40|0.50|0.46|
|**mo**|**+ CoFreeVLA**|0.27|0.47|0.19|0.63|0.21|0.70|0.20|0.67|0.23|0.57|**0.22**|**0.61**|
|**06**|Vanilla|0.67|0.37|0.27|0.57|0.43|0.70|0.47|0.63|0.33|0.47|0.43|0.55|
|_π_**.**|**+ CoFreeVLA**|0.23|0.57|0.16|0.70|0.18|0.77|0.17|0.73|0.20|0.63|**0.19**|**0.68**|
|**APEX**|Vanilla|0.63|0.40|0.23|0.60|0.40|0.73|0.37|0.67|0.27|0.50|0.38|0.58|
||**+ CoFreeVLA**|0.20|0.67|0.16|0.77|0.14|0.83|0.13|0.80|0.17|0.73|**0.16**|**0.76**|
|_Note_: <br>Average <br>obtaine<br>Pouring B|“Vanilla” deno<br> columns summ<br>d with our CoF<br>eans task, whil|tes the<br>arize <br>reeVL<br>e prec|origina<br> the safe<br>A fram<br>ision tas|l basel<br>ty (CR<br>ework. <br>ks reta|ine policy<br> reductio<br> The larg<br>in consist|with<br>n) an<br>est C<br>ent re|out safe<br>d task-e<br>R reduct<br>duction|ty inte<br>xecuti<br>ions o<br>s in C|rventions<br>on (SR in<br>ccur on t<br>R and cor|. Bol<br>creas<br>he int<br>respo|d value<br>e) impr<br>erferen<br>nding g|s in t<br>ovem<br>ce-he<br>ains|he<br>ents<br>avy<br>in SR.|


0.16, 0.16, 0.16, 0.15, 0.13, and 0.18, respectively. Thus, the framework provides measurable improvements for lightweight, foundation, and dual-arm-specific policies, while the magnitude of the gain varies with the nominal policy and task geometry. 

Task-level results show that the benefit is largest when the planned motion creates substantial geometric interference. For Pouring Beans, vanilla policies yield CR values of 0.63–0.93, whereas CoFreeVLA reduces them to 0.20–0.32; SR correspondingly increases from 0.20–0.40 to 0.40–0.67. The remaining tasks also show lower CR and higher SR for every backbone, although the CR reductions are generally smaller in the tight-clearance precision tasks. This trend is consistent with the estimator providing the greatest advantage when inter-arm or arm–object overlap is the dominant failure mode. At the same time, fixed thresholds can remain conservative when successful manipulation requires intentional close proximity, which defines an operating boundary for the current calibration. 

## **4.3 Collision-Free VLA** 

Figure 3 illustrates how the risk gate modifies closed-loop VLA execution. The qualitative comparison contrasts a nominal rollout with a rollout in which CoFreeVLA screens each proposed action and invokes recovery when the predicted risk exceeds the blocking threshold. 

In the Pouring Beans sequence (Fig. 3(A)), vanilla RDT-1B completes the preparation stage and begins tilting the cup, after which the two arms and the grasped object converge within the shared workspace. The resulting contact causes the dual-arm episode to fail. With CoFreeVLA, the gate intercepts the high-risk action before physical contact, and the recovery controller generates a separating motion that returns the arms to a lower-risk configuration. The policy then resumes and completes the task. This qualitative behavior is consistent with the quantitative results in Table 1: for RDT-1B on Pouring Beans, CR decreases from 0.80 to 0.30 and SR increases from 0.28 to 0.43. 

11 


**Fig. 3** Qualitative comparison of VLA execution with and without the CoFreeVLA framework. (A) Pouring Beans with collision interception and synthesized recovery. (B) Remove Pen Cap with a conservative-gating false-positive intervention. 

The Remove Pen Cap sequence illustrates the principal failure boundary (Fig. 3(B)). Vanilla APEX executes the preparation, grasping, and removal stages successfully. In the CoFreeVLA rollout, however, the gate flags the intentional closeproximity motion as risky. The resulting intervention and recovery are unnecessary for this valid maneuver, so the episode terminates unsuccessfully. This individual falsepositive event coexists with the aggregate improvement for APEX in Table 1, where Pen Cap Removal CR decreases from 0.23 to 0.16 and SR increases from 0.60 to 0.77. 

Taken together, these sequences show that CoFreeVLA is most effective when a nominal plan produces a genuine inter-arm or arm–object overlap. They also show that a fixed conservative threshold can suppress valid actions in millimeter-scale alignment tasks. Task-conditioned calibration is therefore needed to preserve collision reduction without compromising legitimate close-contact manipulation. 

## **4.4 Ablation Study** 

We conduct a controlled ablation using RDT-1B as the backbone. Each variant is evaluated on the same five tasks with 30 trials per task. The configurations form an incremental sequence, followed by targeted removals of the auxiliary geometric heads and hysteresis. We report Avg. CR, Avg. SR, the fraction of control steps blocked by the gate, and the fraction of blocked episodes that return to safe execution and complete the task. 

Table 2 summarizes the observed ablation results. The gate alone reduces collisions but leaves blocked episodes without a mechanism for returning to a feasible trajectory. Adding recovery further reduces Avg. CR and increases Avg. SR. Risk-aware policy refinement provides an additional gain by shifting proposed actions away from 

12 

high-risk plans. Restoring the clearance and time-to-collision heads improves recovery success by providing information about correction direction and urgency. Removing hysteresis increases the blocked-step fraction and slightly reduces SR, consistent with oscillatory switching near the decision boundary. The complete system achieves the best joint safety and task-performance profile. These results confirm that each CoFreeVLA component contributes to lower collision rates and higher task success, with the full configuration providing the strongest overall performance. 

**Table 2** Ablation results on RDT-1B. 

|Variant|Avg. CR _↓_|Avg. SR _↑_<br>B|locked steps _↓_|Recovery success _↑_|
|---|---|---|---|---|
|Vanilla RDT-1B|0.62|0.40|–|–|
|Gate only|0.42|0.46|0.17|0.31|
|Gate + recovery|0.34|0.50|0.14|0.68|
|Gate + recovery + refinement<sup>_∗_</sup>|0.29|0.53|0.13|0.70|
|Full, no hysteresis|0.27|0.54|0.22|0.73|
|**Full CoFreeVLA**|**0.25**|**0.56**|**0.10**|**0.82**|


> _<u>∗</u>_ The refinement variant omits the auxiliary clearance and time-tocollision heads. 

## **4.5 Real-Time Control Viability** 

We also evaluate whether the safety module can operate within the control budget. The VLA updates at 10 Hz, while the low-level controller runs at 30 Hz. The estimator is exported to ONNX or TorchScript, and visual features are prefetched from the VLA backbone. A single estimator forward pass remains below 5 ms, corresponding to less than 5% of the 100 ms VLA update interval and approximately 15% of one 30 Hz controller period. The full model therefore leaves sufficient time for candidate evaluation and command dispatch without changing the backbone update rate. 

# **5 Conclusion** 

We present CoFreeVLA, a closed-loop execution layer for screening short-horizon VLA action proposals against dual-arm self-collision risk. The framework combines multimodal risk estimation, command gating, recovery synthesis, and optional action refinement. Across the evaluated bimanual tasks and policy backbones, it consistently reduces collision exposure while improving task completion. Ablation results show that the individual components contribute to the overall safety–performance trade-off, and the estimator operates within the underlying VLA control budget. Fixed conservative thresholds can nevertheless intercept valid close-contact motions in millimeter-scale precision tasks. Future work will investigate task-conditioned thresholds, uncertainty-aware calibration, and adaptive prediction horizons. 

# **References** 

- [1] Brohan, A., et al.: Rt-2: Vision-language-action models transfer web knowledge to robotic control, 2023. URL https://arxiv. org/abs/2307.15818 (2024) 

13 

- [2] Driess, D., et al.: Palm-e: An embodied multimodal language model (2023) 

- [3] Team, O.M., et al.: Octo: An open-source generalist robot policy. arXiv preprint arXiv:2405.12213 (2024) 

- [4] Kim, M., et al.: Openvla: An open-source vision-language-action model. arXiv preprint arXiv:2406.09246 (2024) 

- [5] Ahn, M., et al.: Do as i can, not as i say: Grounding language in robotic affordances. arXiv preprint arXiv:2204.01691 (2022) 

- [6] Abbas, M., Narayan, J., Dwivedy, S.K.: A systematic review on cooperative dual-arm manipulators: modeling, planning, control, and vision strategies. International Journal of Intelligent Robotics and Applications **7** (4), 683–707 (2023) 

- [7] Bi, J., Ma, K.Y., Hao, C., Shou, M.Z., Soh, H.: Vla-touch: Enhancing vision-language-action models with dual-level tactile feedback. arXiv preprint arXiv:2507.17294 (2025) 

- [8] Zhai, X., Hao, C.: Vfp: Variational flow-matching policy for multi-modal robot manipulation. arXiv preprint arXiv:2508.01622 (2025) 

- [9] Zucker, M., _et al._ : Chomp: Covariant hamiltonian optimization for motion planning. The International journal of robotics research **32** (9-10), 1164–1193 (2013) 

- [10] Schulman, J., _et al._ : Motion planning with sequential convex optimization and convex collision checking. The International Journal of Robotics Research **33** (9), 1251–1270 (2014) 

- [11] MoveIt Tutorials: OMPL Planner — Collision/Self-Collision Checking. https:// moveit.github.io/ Accessed 2025-09-12 

- [12] MoveIt Docs: Planning Scene — Self-Collision Checking. https://moveit.picknik. ai/ Accessed 2025-09-12 

- [13] Pan, J., Chitta, S., Manocha, D.: Fcl: A general purpose library for collision and proximity queries. In: 2012 IEEE International Conference on Robotics and Automation, pp. 3859–3866 (2012). IEEE 

- [14] Lei, M., _et al._ : Real-time kinematics-based self-collision avoidance algorithm for dual-arm robots. Applied Sciences **10** (17), 5893 (2020) 

- [15] Fresnillo, P., _et al._ : Extending the motion planning framework—moveit with advanced manipulation functions for industrial applications. Robotics and Computer-Integrated Manufacturing **83** , 102559 (2023) 

14 

- [16] Ames, A., _et al._ : Control barrier function based quadratic programs for safety critical systems. IEEE Transactions on Automatic Control **62** (8), 3861–3876 (2016) 

- [17] Ames, A.D., Coogan, S., Egerstedt, M., Notomista, G., Sreenath, K., Tabuada, P.: Control barrier functions: Theory and applications. In: 2019 18th European Control Conference (ECC), pp. 3420–3431 (2019). Ieee 

- [18] Grotz, M., Shridhar, M., Chao, Y.-W., Asfour, T., Fox, D.: Peract2: Benchmarking and learning for robotic bimanual manipulation tasks. In: CoRL 2024 Workshop on Whole-body Control and Bimanual Manipulation: Applications in Humanoids and Beyond (2024) 

- [19] Fu, Z., et al.: Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation. arXiv preprint arXiv:2401.02117 (2024) 

- [20] Yu, Q., Hao, C., Wang, J., Liu, W., Liu, L., Mu, Y., You, Y., Yan, H., Lu, C.: Manipose: A comprehensive benchmark for pose-aware object manipulation in robotics. arXiv preprint arXiv:2403.13365 (2024) 

- [21] Dastider, A., _et al._ : Apex: ambidextrous dual-arm robotic manipulation using collision-free generative diffusion models. In: 2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 9526–9533 (2024). IEEE 

- [22] Liu, S., et al.: Rdt-1b: a diffusion foundation model for bimanual manipulation. arXiv preprint arXiv:2410.07864 (2024) 

- [23] AgileX Robotics: AgileX Robotics — Global. https://global.agilex.ai/ Accessed 2025-09-14 

- [24] Wen, J., Zhu, Y., Li, J., Zhu, M., Tang, Z., Wu, K., Xu, Z., Liu, N., Cheng, R., Shen, C., et al.: Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation. IEEE Robotics and Automation Letters (2025) 

- [25] Intelligence, P., Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., et al.: _π_ 0. 5: A visionlanguage-action model with open-world generalization. arxiv 2025. arXiv preprint arXiv:2504.16054 (2025) 

- [26] Shukor, M., Aubakirova, D., Capuano, F., Kooijmans, P., Palma, S., Zouitine, A., Aractingi, M., Pascal, C., Russi, M., Marafioti, A., et al.: Smolvla: A vision-language-action model for affordable and efficient robotics. arXiv preprint arXiv:2506.01844 (2025) 

- [27] Zheng, J., Li, J., Wang, Z., Liu, D., Kang, X., Feng, Y., Zheng, Y., Zou, J., Chen, Y., Zeng, J., et al.: X-vla: Soft-prompted transformer as scalable 

15 

cross-embodiment vision-language-action model. arXiv preprint arXiv:2510.10274 (2025) 

- [28] Song, W., Chen, J., Ding, P., Zhao, H., Zhao, W., Zhong, Z., Ge, Z., Ma, J., Li, H.: Accelerating vision-language-action model integrated with action chunking via parallel decoding. arXiv preprint arXiv:2503.02310 (2025) 

- [29] Bu, Q., Yang, Y., Cai, J., Gao, S., Ren, G., Yao, M., Luo, P., Li, H.: Univla: Learning to act anywhere with task-centric latent actions. arXiv preprint arXiv:2505.06111 (2025) 

- [30] Sundaralingam, B., Hari, S.K.S., Fishman, A., Garrett, C., Van Wyk, K., Blukis, V., Millane, A., Oleynikova, H., Handa, A., Ramos, F., _et al._ : Curobo: Parallelized collision-free robot motion generation. In: 2023 IEEE International Conference on Robotics and Automation (ICRA), pp. 8112–8119 (2023). IEEE 

- [31] Haddadin, S., De Luca, A., Albu-Sch”affer, A.: Robot collisions: A survey on detection, isolation, and identification. IEEE Transactions on Robotics **33** (6), 1292–1312 (2017) https://doi.org/10.1109/TRO.2017.2723903 

- [32] Chiu, J.-R., Sleiman, J.-P., Mittal, M., Farshidian, F., Hutter, M.: A collision-free mpc for whole-body dynamic locomotion and manipulation. In: 2022 International Conference on Robotics and Automation (ICRA), pp. 4686–4693 (2022). IEEE 

- [33] Kramar, V., Kramar, O., Kabanov, A.: Self-collision avoidance control of dualarm multi-link robot using neural network approach. Journal of Robotics and Control (JRC) **3** (3), 309–319 (2022) 

- [34] Lv, Q., Li, H., Deng, X., Shao, R., Li, Y., Hao, J., Gao, L., Wang, M.Y., Nie, L.: Spatial-temporal graph diffusion policy with kinematic modeling for bimanual robotic manipulation. In: Proceedings of the Computer Vision and Pattern Recognition Conference, pp. 17394–17404 (2025) 

- [35] Chen, J., Jiang, Y., Huang, A., Li, Y., Pan, W.: Vlm-sfd: Vlm-assisted siamese flow diffusion framework for dual-arm cooperative manipulation. IEEE Robotics and Automation Letters (2025) 

- [36] Li, Z., Liu, J., Li, D., Teng, T., Li, M., Calinon, S., Caldwell, D., Chen, F.: Manidp: Manipulability-aware diffusion policy for posture-dependent bimanual manipulation. In: 2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 9956–9962 (2025). IEEE 

- [37] Golluccio, G., Di Vito, D., Antonelli, G., Marino, A.: Deep learning-based collision detection framework for robot tasks in clutter. Robotica, 1–20 (2025) 

- [38] Zhu, X., Xin, Y., Li, S., Liu, H., Xia, C., Liang, B.: Efficient collision detection framework for enhancing collision-free robot motion. In: 2025 IEEE International 

16 

Conference on Robotics and Automation (ICRA), pp. 16162–16168 (2025). IEEE 

- [39] Intelligence, P., Amin, A., Aniceto, R., Balakrishna, A., Black, K., Conley, K., Connors, G., Darpinian, J., Dhabalia, K., DiCarlo, J., et al.: Pi0.6: A vla that learns from experience. arXiv preprint arXiv:2511.14759 (2025) 

17 

