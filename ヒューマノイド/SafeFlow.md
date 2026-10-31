---
title: "SafeFlow: Real-Time Text-Driven Humanoid Whole-Body Control via Physics-Guided Rectified Flow and Selective Safety Gating"
date: "2026-03-25"
authors: "Hanbyel Cho; Sang-Hun Kim; Jeonguk Kang; Donghan Koo"
url: https://arxiv.org/abs/2603.23983
pdf: https://arxiv.org/pdf/2603.23983
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.23983)** / [論文ページ](https://arxiv.org/abs/2603.23983)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **SafeFlow: Real-Time Text-Driven Humanoid Whole-Body Control via Physics-Guided Rectified Flow and Selective Safety Gating** 

Hanbyel Cho Sang-Hun Kim Jeonguk Kang Donghan Koo Physical AI Lab, RX, Samsung Electronics Project page: https://hanbyelcho.info/safeflow/ 

**_Abstract_ — Recent advances in real-time interactive textdriven motion generation have enabled humanoids to perform diverse behaviors. However, kinematics-only generators often exhibit physical hallucinations, producing motion trajectories that are physically infeasible to track with a downstream motion tracking controller or unsafe for real-world deployment. These failures often arise from the lack of explicit physicsaware objectives for real-robot execution and become more severe under out-of-distribution (OOD) user inputs. Hence, we propose SafeFlow, a text-driven humanoid whole-body control framework that combines physics-guided motion generation with a 3-Stage Safety Gate driven by explicit risk indicators. SafeFlow adopts a two-level architecture. At the high level, we generate motion trajectories using Physics-Guided Rectified Flow Matching in a VAE latent space to improve real-robot executability, and further accelerate sampling via Reflow to reduce the number of function evaluations (NFE) for real-time control. The 3-Stage Safety Gate enables selective execution by detecting semantic OOD prompts using a Mahalanobis score in text-embedding space, filtering unstable generations via a directional sensitivity discrepancy metric, and enforcing final hard kinematic constraints such as joint and velocity limits before passing the generated trajectory to a low-level motion tracking controller. Extensive experiments on the Unitree G1 demonstrate that SafeFlow outperforms diffusion- and retargeting-based baselines in success rate, physical compliance, and inference speed while preserving motion diversity, with consistent gains across three downstream tracking controllers.** 

## I. INTRODUCTION 

Recent advances in text-driven motion generation [1–5] have enabled humanoid robots to synthesize diverse and expressive behaviors from natural language. Beyond offline text-to-motion [6, 7], recent work has progressed toward realtime interactive control, where robots respond to streaming text commands. In particular, systems such as TextOp [8] demonstrate a new control paradigm in which natural language serves as a continuously revisable control signal rather than a one-shot task specification, suggesting a promising direction toward intuitive, text-based humanoid control. 

Despite this progress, high-level motion generators often fail to produce motions that are physically executable and safe on real hardware. Kinematics-only generators [1, 3, 4] can exhibit physical hallucinations—including joint limit violations, self-collisions, and unstable balance—and although downstream motion tracking controllers can partially compensate, large violations degrade motion fidelity and can lead to unstable or unsafe behaviors. These failures become more severe under open-ended or out-of-distribution (OOD) 


Fig. 1. **Failure Cases of a Kinematics-Only Generator [8].** Feasible motion for a simple prompt ( **a** ); joint limit violations ( **b** ) and self-collisions ( **c** ) under _in-distribution_ commands; structural collapse under _OOD_ prompts ( **d** )—motivating physics-guided generation and runtime safety gating. 

inputs, where generators may produce severely distorted motions unsuitable for direct execution (Fig. 1). This calls for improving physical feasibility at the generation stage _and_ detecting and rejecting unsafe behaviors prior to execution. 

To this end, we propose **SafeFlow** , a real-time textdriven humanoid whole-body control framework that combines _physics-guided motion generation_ with _deploymenttime selective execution_ to improve robustness under openended or OOD text inputs. At the core of **SafeFlow** is a physics-guided motion generator based on rectified flow matching in a VAE latent space. Unlike purely kinematic generation [1–5], our approach incorporates physics-aware objectives relevant to real-robot execution, including joint feasibility, self-collision avoidance, stability, and motion smoothness, to steer sampling toward executable motion regions. While physics-guided sampling has been explored in character animation and offline motion generation [9], its use for improving real-robot executability in real-time text-driven control remains underexplored. To enable real-time deployment, we further leverage reflow [10] distillation so that the model internalizes the physics-aware guidance, drastically reducing the required number of function evaluations while retaining physically executable behaviors. These generationlevel improvements substantially enhance executability and efficiency, while deployment-time safety under ambiguous 

or adversarial prompts remains a complementary challenge, motivating an additional selective execution mechanism. 

**SafeFlow** therefore incorporates a training-free 3-Stage Safety Gate driven by explicit risk indicators that operates hierarchically across input semantics, generation reliability, and final kinematic feasibility. We first detect semantic OOD prompts in text-embedding space, then filter structurally unstable generations by measuring directional flow sensitivity, and finally enforce a last-line kinematic screen to strictly reject motions that violate hardware constraints, including joint and velocity limits, before execution. This hierarchical filtering enables the system to proactively reject unsafe motions rather than attempting to execute all generated outputs. 

By integrating physics-aware generation with indicatordriven selective execution, **SafeFlow** advances real-time textdriven humanoid control toward safe and robust deployment under unconstrained text inputs. We validate the proposed framework through extensive experiments on the Unitree G1 humanoid. Results show that **SafeFlow** improves success rate, physical compliance, and inference speed compared to diffusion-based baselines while preserving motion diversity. Our main contributions are summarized as follows: 

- We propose **SafeFlow** , a real-time text-driven humanoid whole-body control framework that couples physicsguided generation with deployment-time selective execution for robustness under unconstrained prompts. 

- We introduce **physics-guided rectified flow matching** in a VAE latent space and leverage **reflow distillation** to achieve real-time execution while significantly improving the physical feasibility and real-robot executability of generated motions. 

- We propose a **training-free 3-Stage Safety Gate** to proactively block unsafe behaviors under OOD prompts, utilizing explicit risk indicators: Mahalanobis semantic OOD filtering, directional sensitivity discrepancy metric for generation instability, and hard kinematic screening. 

lective execution to improve both reference executability and robustness to unsafe OOD inputs. 

## _B. Physics-Aware Humanoid Motion Generation_ 

Text-conditioned motion generators [1–5] often produce kinematically plausible yet physically invalid motions ( _e.g_ ., foot sliding, ground penetration). To improve realism, simulator-in-the-loop diffusion methods such as PhysDiff [9] incorporate physics during sampling but introduce substantial latency. Meanwhile, physics-based RL approaches such as PhysHOI [24] are tailored to virtual characters rather than hardware-constrained humanoid robots. In robotics, RobotMDM [6] and Humanoid-R0 [7] bridge the kinematicexecution gap but are inherently limited to offline generation. Specifically, RobotMDM synthesizes full reference sequences from discrete prompts, while Humanoid-R0 relies on computationally heavy autoregressive generation. Both require motions to be pre-computed, making realtime streaming control infeasible. In contrast, **SafeFlow** combines physics-guided rectified flow matching with reflow distillation to generate physically executable motions at the latency required for real-time streaming control. 

## _C. Deployment-Time Safety Gating and OOD Robustness_ 

Real-time, interactive text-driven control exposes robots to open-ended and OOD prompts, which can induce _unsafe_ reference trajectories at deployment time. Most existing frameworks lack an explicit runtime mechanism to reject such unsafe references; for instance, TextOp [8] relies on downstream tracking controllers to cope with the resulting references [16–18], while end-to-end language policies such as LangWBC [25] do not expose an explicit intermediate kinematic reference for pre-execution screening. **SafeFlow** addresses this gap with a 3-Stage Safety Gate that hierarchically screens semantic OOD inputs, generation instability via a directional sensitivity discrepancy metric, and hard kinematic limits, ensuring that only executable and safe reference trajectories are passed to the motion tracking controller. 

## III. METHOD 

## II. RELATED WORK 

## _A. Overview of SafeFlow_ 

## _A. Interactive Language-Driven Humanoid Control_ 

Conventional humanoid whole-body control executes taskspecific commands [11, 12] or tracks predefined references from motion capture [13] or videos [14, 15] with RLbased tracking controllers [16–19]; teleoperation [20–22] adds flexibility at the cost of human involvement. Generative motion models [1–5] translate language into robot motion, but mostly offline. More recently, TextOp [8] demonstrates real-time interactive control with an autoregressive diffusion model [23], allowing on-the-fly intent revision. However, such systems primarily optimize semantic alignment and can produce references that violate actuation limits or exhibit self-collisions and unstable balance—especially under outof-distribution (OOD) commands—burdening downstream trackers [16–18]. In the same streaming setting, **SafeFlow** couples physics-aware guidance with deployment-time se- 

**SafeFlow** is a two-level framework for real-time interactive text-driven humanoid control (Fig. 2), targeting two failure modes: _physically infeasible_ references from kinematicsonly generation and _unsafe_ generations under open-ended or OOD prompts. To address these complementary challenges, **SafeFlow** combines physics-aware motion generation (Sec. III-B) with deployment-time selective execution via a training-free 3-Stage Safety Gate (Sec. III-C), followed by an RL-based motion tracking controller (Sec. III-D). **Streaming Text Control.** Following TextOp [8]’s streaming _reference generation–low-level tracking_ formulation, **SafeFlow** augments the loop with deployment-time safety gating (Fig. 2). At each time step _t_ , the system receives a text command _lt_ and the robot proprioceptive state _x_<sup>robot</sup> _t−_ 1<sup>.We</sup> first apply the Stage-1 Safety Gate to _lt_ ; if _accepted_ , the physics-guided motion generator _G_ produces a horizon- _T_ fut 


Fig. 2. **Overview of SafeFlow. Top (Deployment, Online):** A 3-Stage Safety Gate hierarchically filters OOD semantics, generation instability, and kinematic violations. A reflow-accelerated high-level motion generator provides physically feasible reference motions. If accepted, these are executed by the downstream motion tracking controller; otherwise, a safe fallback is triggered. **Bottom (Training, Offline):** The motion generator is trained via VAE latent learning and physics-guided flow matching with reflow distillation (NFE=1). The motion tracking controller is trained in simulation via RL. 

(= 8) future reference motion sequence conditioned on the previous _T_ hist (=2) reference states, 


The generated reference is then screened by the Stage2/3 Safety Gates before execution. The low-level tracking controller _π_ runs at the control rate and converts the _accepted_ kinematic reference into executable joint commands as _aτ_ = _π_ ( _x_<sup>robot</sup> _τ −_ 1<sup>_, aτ−_1</sup><sup>_, x_ref</sup> _τ_ : _τ_ + _T_ ref _−_ 1<sup>),where</sup><sup>_x_ref</sup> _τ_ : _τ_ + _T_ ref _−_ 1<sup>denotesthe</sup> corresponding segment of the latest accepted reference. If a prompt or generated segment is _rejected_ , the system executes a safe fallback motion and continues with updated streaming commands. 

## _B. Physics-Guided Rectified Flow Motion Generation_ 

Real-time interactive control requires generating physically executable reference motions with low latency. We formulate the high-level motion generator _G_ using _rectified flow matching_ for stable kinematic modeling. However, purely kinematic generation often violates physical constraints critical for robot execution. To ensure physical feasibility, **SafeFlow** introduces _physics-guided sampling_ to steer generation toward executable motion regions. Finally, to support lowlatency streaming, we apply _reflow_ distillation [10], enabling highly efficient sampling via straight flow trajectories. 

**Latent-Space Motion Representation.** We represent reference motion _x_<sup>ref</sup> _t_ using _the same_ DoF-based local incremental per-frame feature _ft ∈_ R<sup>_d_feat</sup> as in TextOp [8]. We train a VAE to learn a compact motion latent space. The encoder infers a motion latent from both past and future reference motion as **z** _∼_ Enc( _· | ft−T_ hist: _t_ + _T_ fut _−_ 1), while the decoder reconstructs the future reference using only the past reference and the motion latent as _ft_ : _t_ + _T_ fut _−_ 1 =Dec ( _ft−T_ hist: _t−_ 1 _,_ **z** ). 

**Text-Conditioned Rectified Flow Matching.** We model the text-conditional distribution of future motion latent using rectified flow matching [10]. We embed the streaming text command using a CLIP text encoder [26] as **e** _t_ = CLIP( _lt_ ) and condition on the motion history _ft−T_ hist: _t−_ 1. We learn a velocity field _vθ_ ( **z** _, u | ft−T_ hist: _t−_ 1 _,_ **e** _t_ ) that defines an Ordinary Differential Equation (ODE) transporting a noise distribution to the data distribution: 


During training, we sample a ground truth motion latent **z** 1 = Enc( _ft−T_ hist: _t_ + _T_ fut _−_ 1) and a noise latent **z** 0 _∼N_ ( **0** _,_ **I** ). We define a linear interpolation path **z** _u_ = _u_ **z** 1+(1 _−u_ ) **z** 0, which implies a constant target velocity **z** 1 _−_ **z** 0. The model is trained to minimize the rectified flow matching objective: 


At inference, we sample **z** 0 _∼N_ ( **0** _,_ **I** ) and integrate the ODE from _u_ =0 to _u_ =1 using an explicit solver ( _e.g_ ., Euler) with _N_ steps ( _i.e_ ., NFE= _N_ ) to obtain the generated motion latent **z** 1, then decode _ft_ : _t_ + _T_ fut _−_ 1 =Dec( _ft−T_ hist: _t−_ 1 _,_ **z** 1). 

**Physics-Guided Sampling.** Text conditioning does not guarantee physical feasibility on a real robot, so **SafeFlow** employs _physics-guided sampling_ to steer the motion latent toward executable manifolds, imposing constraints purely = at inference time without retraining. Let _ft_ : _t_ + _T_ fut _−_ 1 Dec( _ft−T_ hist: _t−_ 1 _,_ **z** _u_ ) denote the decoded motion feature sequence at ODE integration time _u_ , with _x_<sup>ref</sup> _t_ : _t_ + _T_ fut _−_ 1<sup>denoting</sup> the corresponding kinematic reference trajectory. 

We define a differentiable physics cost _C_ to quantify executability violations. While gradient-based guidance has been explored in character animation and offline motion [1, 9, 27], to the best of our knowledge, **SafeFlow** is the first to adapt 

this mechanism for _real-robot executability_ by enforcing strict hardware limits, self-collision avoidance, and postural stability via CoM regularization. The total cost is a weighted sum of four terms as _C_ � _x_<sup>ref</sup> _t_ : _t_ + _T_ fut _−_ 1� =<sup>�</sup> _i_<sup>_λiCi_,where</sup><sup>_Ci_</sup> represents specific constraints ( _detailed below_ ). During ODE integration, we compute the gradient of the cost with respect to the _generated motion latent_ **z** . This involves passing **z** through the frozen VAE decoder to reconstruct the kinematic reference for cost evaluation, and then backpropagating. We then steer the flow using the _guided velocity field v_ ˜ _θ_ : 


where _α_ ( _u_ ) is a time-dependent guidance scale. We use this steered velocity _v_ ˜ _θ_ for numerical integration to push the trajectory toward physically feasible regions. 

We define _C_ as a weighted sum of four terms designed for real-robot executability. Let **q** _τ_ be the joint configuration at time _τ_ decoded from _fτ_ . 

_(1) Joint Limit & (2) Self-Collision:_ To strictly enforce hardware limits and prevent physical penetrations, we penalize violations using ReLU-squared barriers: 


where _ra, rb_ are collision sphere radii for links _a, b_ , _dab_ is their Euclidean distance, and _m_ is a safety margin. 

_(3) Smoothness & (4) CoM Stability:_ To generate smooth, jitter-free motions suitable for tracking, we regularize highorder derivatives of joints and the Center of Mass (CoM). <u>�</u> _mi_ **<u>p</u>** _i_ <u>(</u> **<u>q</u>** <u>)</u> Let **c** ( **q** ) = <u>�</u> _mi_ be the global CoM position computed via forward kinematics, where _mi_ and **p** _i_ are the mass and position of the _i_ -th link. 


Here, time derivatives are computed via finite differences. 

**Physics-Aware Reflow.** Physics-guided sampling improves executability but increases latency due to iterative gradient computations ( _∇_ **z** _C_ ). To enable real-time control, we apply the _reflow_ procedure [10] to distill the guided trajectories into a straighter velocity field. We generate synthetic pairs ( **z** 0 _,_ **z**<sup>guided</sup> 1 ), where **z**<sup>guided</sup> 1 is obtained through the expensive guided integration in Eq. 4. We then retrain the model along the straight paths connecting **z** 0 and **z**<sup>guided</sup> 1 . This process _internalizes_ the physics-aware guidance into the network weights, eliminating online cost-gradient computation and enabling physically executable motion generation with fewer function evaluations ( _e.g_ ., NFE=1) at deployment. 

## _C. Selective Execution via 3-Stage Safety Gate_ 

While physics-guided motion generation improves average executability, it cannot inherently prevent failures caused by 

open-ended or OOD text inputs. Such inputs often reside in sparse regions of the training distribution, leading to physical hallucinations or structurally unstable motions. To ensure robust deployment without compromising real-time interactivity, **SafeFlow** introduces a _training-free_ selective execution mechanism. As a hierarchical _firewall_ , it filters failure modes at the _input semantic_ , _latent generative_ , and _output kinematic_ levels, rejecting unsafe references with acceptable latency before reaching the motion tracking controller. 

**Stage 1: Semantic OOD Filtering (Input Level).** Standard generators often fail unpredictably when facing outof-distribution (OOD) prompts. We detect these efficiently in the CLIP [26] text embedding space. Since the statistics of training prompts (mean **_µ_** and covariance **Σ** ) are _precomputed offline_ , inference requires only a lightweight Mahalanobis distance calculation on the streaming text embedding **e** _t_ : _d_<sup>2</sup> ( **e** _t_ ) = ( **e** _t −_ **_µ_** )<sup>_⊤_</sup> **Σ**<sup>_−_1</sup> ( **e** _t −_ **_µ_** ). The threshold _τ_ sem is calibrated to the _N_ -th percentile of distances computed on the training set. Prompts satisfying _d_<sup>2</sup> _> τ_ sem are rejected instantly, bypassing the motion generator to prevent synthesizing _undefined_ reference motions. 

**Stage 2: Generation Instability Filtering (Model Level).** Even for valid prompts, the flow can traverse unstable regions where the vector field becomes highly anisotropic. To detect this structural instability, we introduce a novel _directional sensitivity discrepancy_ metric. The key intuition is that, in stable regions, the flow responds consistently to perturbations across directions, whereas high variance indicates fragility to specific directional noise. 

We estimate this by probing the Jacobian _J_ = _∂vθ/∂_ **z** along _M_ random unit vectors _{_ **_ϵ_** _m}_<sup>_M_</sup> _m_ =1<sup>(</sup><sup>_e.g_.,</sup><sup>_M_=16). First,</sup> we compute the directional sensitivity scalar _gm_ for each probe using a finite-difference approximation: 


where _δ_ is a small perturbation. This scalar _gm_ represents the expansion or contraction of the flow along **_ϵ_** _m_ . Finally, we define the _generation instability score_ _<u>R</u>_ as the standard deviation of these sensitivities, _R_ = ~~�~~ _M_ <u>1 �</u> _Mm_ =1<sup>(</sup><sup>_gm−g_¯)2, where ¯</sup><sup>_g_</sup> denotes the mean of _{gm}_ . Leveraging _parallel batching_ , this computation incurs negligible latency, enabling _real-time risk monitoring_ during generation. A high _R_ ( _> τ_ stab) indicates that the flow field is disjointed or near-singular, triggering early rejection to prevent executing _structurally unreliable_ reference motions. 

**Stage 3: Hard Kinematic Screening (Output Level).** As a final fail-safe, we perform a lightweight, deterministic screen on _x_<sup>ref</sup> , strictly rejecting segments that violate joint position bounds ( _qj ∈/_ [ _qj_<sup>min</sup> _, qj_<sup>max</sup> ]) or dynamic constraints ( _|_ ˙ _qj| > q_ ˙ _j_<sup>max</sup> , _|q_ ¨ _j| > q_ ¨ _j_<sup>max</sup> ). While this local check cannot guarantee global stability ( _e.g_ ., balance), it serves as a necessary _lastline defense_ to prevent immediate actuator damage. If a rejection is triggered at any stage, the system executes a safe fallback by replacing the current user command with 

a “stand” prompt while simultaneously interpolating to a nominal pose, and awaits the next command. 

## _D. RL-Based Motion Tracking Controller_ 

We adopt a goal-conditioned RL motion tracking controller trained with PPO in Isaac Lab [28]. The controller outputs residual joint corrections ∆ _qπ_ , forming control targets as _q_ target = _q_ ref( _t_ ) + ∆ _qπ_ , which improves robustness to imperfect references. To enhance generalization, future reference observations are expressed in the body-local frame (linear/angular velocities, root height, roll–pitch, and joint targets), ensuring invariance to global position and heading. 

## _E. Implementation Details_ 

**Physics-Guided Motion Generator & Safety Gating.** Our model is trained on BABEL [29] retargeted to Unitree G1. We follow TextOp [8] for data preprocessing and splits. Training tuples use sliding windows of ( _T_ hist _, T_ fut)=(2 _,_ 8), enabling the generator to operate at 6.25 Hz. Building upon TextOp, we adopt its exact motion representations, Transformer architectures, and remaining training hyperparameters, training the velocity field _vθ_ for 200k iterations. We build a physics-guided teacher ( **SafeFlow** (+ Guid.), NFE = 10) using classifier-free guidance (CFG) decaying from 5.0 to 3.0. Physics-guided sampling uses _λ_ lim = _λ_ stab = 1 _._ 0, _λ_ sm = 0 _._ 1, _λ_ col = 0 _._ 01, _βq_ = 50 _._ 0, and _βc_ = 10 _._ 0. We apply physics guidance scale _α_ ( _u_ ) with a linearly increasing schedule from 500 to 10 _,_ 000 across the denoising trajectory, with per-element gradient clamping at _±_ 0 _._ 2. For real-time deployment ( **SafeFlow** (+ Guid. & Reflow), NFE = 1), we distill guided ODE trajectories into straight paths via reflow for an additional 200k iterations. Self-collision is computed over 14 link pairs with sphere radii _r ∈_ [0 _._ 03 _,_ 0 _._ 10] m and margin _m_ = 0 _._ 03 m. For safety gating, Stage 1 uses _τ_ sem calibrated to accept 95% of training prompts (trade-off analyzed in Table II). Stage 2 evaluates _R_ using 16 probes ( _δ_ = 10<sup>_−_6</sup> ) with threshold _τ_ stab = 5 _._ 0, which matches the F1-optimal value on evaluated rollouts ( _τ_<sup>_∗_</sup> = 4 _._ 9; Sec. IV-C). Stage 3 enforces G1 hardware limits. 

**Motion Tracking Controller.** Since our contributions lie in the physics-guided generator and the 3-Stage Safety Gate, we adopt the same RL tracking setup as TextOp [8] ( _i.e_ ., training data, observations, rewards, and domain randomization). For the primary comparison, the identical trained tracking policy, referred to as the _Base Tracker_ [8], is used for all evaluated generation methods. The controller runs at 50 Hz on the onboard Jetson Orin. Cross-tracker generalization is further evaluated with SONIC [19] and MOSAIC [30] in Table I. 

## IV. EXPERIMENTS 

We evaluate the effectiveness of **SafeFlow** through a combination of extensive simulation studies and real-world deployment on the Unitree G1 humanoid. Our experiments are designed to validate the system’s physical executability, deployment-time safety and robustness, computational efficiency, and overall practical performance. Specifically, the evaluation aims to answer the following questions: 

- **Q1 (Executability):** How much does physics-guided generation improve physical feasibility of reference motions and downstream tracking fidelity across trackers? 

- **Q2 (Safety and Robustness):** Can the 3-Stage Safety Gate detect and filter out OOD prompts and generation instability to improve deployment-time safety? 

- **Q3 (Real-Time Performance):** Do the reflow-accelerated motion generator and safety gating pipeline achieve the low latency required for real-time control? 

- **Q4 (Real-Robot Deployment):** Can **SafeFlow** transfer to real hardware to enable robust interactive control under challenging and potentially unsafe commands? 

## _A. Experimental Setup_ 

To evaluate **SafeFlow** across _Physical Executability_ , _Deployment-Time Safety_ , and _Computational Efficiency_ , the motion generator is trained offline in PyTorch [31], while the tracking controller is trained in Isaac Lab [28]. Systemlevel evaluations of the integrated pipeline are conducted in MuJoCo [32] to assess closed-loop Unitree G1 behavior. 

**Baselines.** We compare against (i) TextOp [8], the state-ofthe-art autoregressive diffusion baseline; (ii) _MDM + GMR_ , an offline (non-streaming) kinematics-only pipeline retargeting pretrained MDM [1] generations to the G1 with the same GMR retargeting used for our training data (SMPL parameters recovered from MDM’s rotation channels; median +1 _._ 5 cm SMPL-space FK error vs. per-motion SMPLify [33] fits on a 1,344-motion subset); and (iii) _TextOp + criticalign_ , a RobotMDM [6]-style baseline fine-tuning the same diffusion backbone with a tracking-outcome critic (motionlevel AUC 0.987, trained on 9.4k evaluated rollouts). 

**Tracking Controllers.** To verify that our conclusions are not tied to a particular controller, all generation methods are additionally evaluated with two public large-scale trackers— SONIC [19] and MOSAIC [30]—using their unmodified deployment stacks in sim-to-sim under identical prompts and a common success criterion. We report Succ., _E_ mpjpe, and _E_ dof for all three trackers; for comparability, _E_ dof is averaged over the 23 non-wrist joints shared across all stacks. 

## _B. Physical Executability (Q1)_ 

We first evaluate whether the physics-guided generation improves the physical feasibility of reference motions. To strictly decouple the performance of the motion generator from the capabilities of the downstream tracking controller, we assess executability in two stages: _Generator-Only_ (kinematic evaluation prior to tracking) and _System-Level_ (closedloop evaluation with the tracking controller). For evaluation, we utilize the BABEL [29] validation prompts, generating 1,000 motion frames per prompt and reporting the averages. 

**Generator-Only Kinematic Feasibility.** We measure the _Joint Limit Violation Rate_ (JV, %) and _Self-Collision Rate_ (SC, %) of generated motions. As shown in Table I, TextOp [8] frequently violates hardware limits (JV: 43.14%, SC: 11.05%). Notably, adopting our base Flow Matching formulation ( **SafeFlow** (Flow)) already reduces violations to 

TABLE I 

**PHYSICAL EXECUTABILITY AND CROSS-TRACKER TRACKING FIDELITY.** JV/SC DENOTE JOINT-LIMIT-VIOLATION/SELF-COLLISION RATES. TRACKING ERRORS ARE EVALUATED ON VALID FRAMES BEFORE FAILURE (COMMON-PREFIX), WITH SUCCESS-ONLY VALUES IN PARENTHESES. ALL TRACKING ERRORS ARE COMPUTED RELATIVE TO EACH GENERATOR’S OWN REFERENCE. THE BASE TRACKER IS SHARED WITH TEXTOP [8]; SONIC [19] AND MOSAIC [30] USE THEIR UNMODIFIED DEPLOYMENT STACKS.<sup>_†_</sup> JV IS MEASURED POST-RETARGETING (IK CLAMPS LIMITS). 

||**Generat**|**or-Only**||||**System**|**-Level Tracki**|**ng Fidelity**||||
|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|**JV**_↓_|**SC**_↓_||**Base Tracker**|[8]||**SONIC** [19|]||**MOSAIC** [3|0]|
||||**Succ.**_↑_|**E**mpjpe _↓_|**E**dof _↓_|**Succ.**_↑_|**E**mpjpe _↓_|**E**dof _↓_|**Succ.**_↑_|**E**mpjpe _↓_|**E**dof _↓_|
|MDM+GMR [1] (offline)|0.79%<sup>_†_</sup>|30.48%|87.3%|45.2<br>(42.2)|4.96 (4.74)|92.6%|40.3 (38.6)|8.97 (8.71)|89.0%|44.3 (42.1)|7.53 (7.23)|
|TextOp [8]|43.14%|11.05%|80.6%|82.5 (79.2)|5.94 (5.72)|81.3%|45.9 (43.1)|8.36 (8.05)|74.6%|49.3 (46.3)|8.38 (8.05)|
|+critic-align (RobotMDM-style) [6]|24.08%|12.94%|87.6%|92.2 (89.5)|5.28 (5.11)|84.5%|43.7 (41.3)|8.19 (7.90)|79.3%|47.1 (43.8)|7.68 (7.30)|
|**SafeFlow**(Flow)|12.75%|7.25%|92.8%|59.6 (58.3)|4.73 (4.64)|91.9%|34.4 (33.2)|6.42 (6.26)|90.2%|36.2 (35.1)|6.13 (6.00)|
|**SafeFlow**(+ Guid.)|6.32<br>%|4.39<br>%|97.9<br>%|51.2 (50.9)|4.43<br>(4.41)|96.4<br>%|30.8<br>(30.3)|5.77<br>(5.71)|97.1<br>%|31.2<br>(30.9)|5.52<br>(5.48)|
|**SafeFlow**(+ Guid. & Reflow)|**3.08**%|**1.42**%|**98.6**%|**44.0**(43.9)|**4.32**(4.30)|**99.1**%|**29.6**(29.5)|**5.15**(5.14)|**98.7**%|**27.6**(27.4)|**5.00**(4.99)|


12.75% JV and 7.25% SC. Building upon this foundation, our physics-guided sampling ( **SafeFlow** (+ Guid.)) further reduces these errors to 6.32% and 4.39%, respectively. The reflow-distilled model ( **SafeFlow** (+ Guid. & Reflow)) further lowers them to 3.08% JV and 1.42% SC while enabling single-step (NFE=1) generation for real-time control (Tab. III). Among alternative generator baselines, _MDM + GMR_ exhibits a low post-retargeting JV of 0.79% because IK clamps joint limits, but still incurs a high 30.48% self-collision rate. Outcome-supervised _TextOp + critic-align_ reduces TextOp’s JV from 43.14% to 24.08%, but leaves SC at 12.94%, remaining substantially less feasible than **SafeFlow** . _CoM velocity_ and _joint acceleration_ plots (Fig. 3 (a)) further show that **SafeFlow** suppresses erratic spikes (baseline peak: 263.5 rad _/_ s<sup>2</sup> ), yielding more trackable references. 

**System-Level Tracking Fidelity.** We next evaluate how reference feasibility translates to closed-loop tracking. Across all trackers, we report the _Success Rate_ (Succ., defined as completing the sequence without falling, _i.e_ ., base height _>_ 0.3 m) and _MPJPE_ ( _E_ mpjpe, mm). We also report mean joint-angle error _E_ dof (deg), averaged over the 23 nonwrist joints shared across all trackers. On the Base Tracker, **SafeFlow** (+ Guid. & Reflow) raises success from 80.6% to 98.6% and reduces _E_ mpjpe from 82.5 to 44.0 mm vs. TextOp. The kinematics-only _MDM + GMR_ pipeline reaches only 87.3% success despite 3.5 _×_ lower mean joint acceleration, while _TextOp + critic-align_ improves success to 87.6% but worsens _E_ mpjpe to 92.2 mm. These results suggest that posthoc retargeting or outcome supervision alone does not provide the same tracking benefits as physics-aware generation within the sampler. Moreover, _torque_ and _joint velocity_ plots (Fig. 3 (b)) show that **SafeFlow** mitigates torque chattering and erratic velocity spikes ( _e.g_ ., baseline peak: 5.2 rad _/_ s). 

**Tracker Generalization.** This improvement is not specific to the Base Tracker. Table I shows that the full **SafeFlow** model reaches 98.6–99.1% success across the Base Tracker [8], SONIC [19], and MOSAIC [30], compared with 74.6– 81.3% for TextOp, corresponding to gains of 17.8–24.1 pp. It also consistently reduces _E_ mpjpe from 82.5/45.9/49.3 mm to 44.0/29.6/27.6 mm across the three trackers, respectively. These consistent gains indicate that the benefits of physics- 


Fig. 3. **Kinematic Feasibility and Tracking Stability.** Despite generating dynamic motions (left), our full pipeline, **SafeFlow** (+ Guid. & Reflow), stabilizes kinematic references and improves tracking. (a) _Generator-only_ : **SafeFlow** suppresses erratic spikes in CoM velocity and joint acceleration. (b) _System-level_ : **SafeFlow** mitigates torque chattering and joint velocity spikes, enabling hardware-safe tracking. The x-axis represents time in frames, showing a representative active segment (frames 600–950). 

aware generation are not specific to any downstream tracker. 

**Diversity Preservation.** Improved physical feasibility does not sacrifice motion diversity. We measure _Multimodality_ (MModality) [34] as the mean pairwise L2 distance in 29DoF joint-angle space (rad) over 10 generations per prompt. Across all 2,362 prompts, TextOp shows higher diversity (1.40 vs. 1.09 rad), but this gap is largely driven by unstable motions. Among the 1,889 prompts where tracking succeeds for both methods, the gap shrinks to 1.26 vs. 1.06 rad; among the 915 prompts with no joint-limit violations from either method, the two are nearly identical (1.00 vs. 0.99 rad, ∆= 1 _._ 1%). On the 437 prompts where only TextOp fails, its multimodality rises to 1.99 rad—66% above **SafeFlow** ’s 1.20 rad on the same prompts—indicating that much of TextOp’s apparent diversity advantage stems from physically implausible motions rather than meaningful variation. 

## _C. Deployment-Time Safety and Robustness (Q2)_ 

We evaluate the 3-Stage Safety Gate’s ability to filter outof-distribution (OOD) prompts and generative instabilities, improving deployment-time safety. 

TABLE II 

**STAGE 1 SEMANTIC OOD FILTERING.** WITH _τ_ 95 PASSING 95% OF TRAINING PROMPTS, STAGE 1 REJECTS OOD INPUTS WHILE PRESERVING HIGH ID COVERAGE. 


Fig. 4. _R_ **Detects Failure-Prone References.** Mean tracking MPJPE of 10-frame windows increases monotonically across shared absolute _R_ quintiles in both ID and OOD. Even ID prompts produce high-instability windows (ID Q5, 87.4 mm) exceeding low- _R_ OOD windows (OOD Q1, 56.6 mm)—showing Stage 1 alone is insufficient and motivating Stage 2. 

**Stage 1: Input-Level Semantic Filtering.** To evaluate robustness to unseen and potentially unsafe text commands, we generate two OOD prompt sets with an LLM [35] (100 each): **Type A (Unseen Verbs)** , containing actions absent from training ( _e.g_ ., “levitate”, “crochet a sweater”), and **Type B (Extreme Dynamics)** , containing extreme acrobatic motions exceeding hardware limits ( _e.g_ ., “flying tornado kick”). We compare them against 2,362 ID BABEL validation prompts. 

We use a Mahalanobis distance-based filter with _τ_ 95, calibrated to pass 95% of training prompts. As Table II shows, Stage 1 achieves high AUROCs (0.9872, 0.9715) for Types A and B, rejecting 91%/77% of OOD prompts while rejecting only 3.7% of ID prompts. A more conservative _τ_ 90 raises OOD rejection to 95%/93% at 9.4% ID rejection, demonstrating a tunable safety–coverage trade-off. Stage 1 serves as a semantic OOD filter rather than a physical-failure predictor; accepted prompts are therefore further screened by Stages 2–3. Stage 2 directly monitors the flow dynamics during inference to detect generative instabilities. 

**Stage 2 & 3: Model- and Output-Level Filtering.** Stage 1 filters semantically OOD prompts, but cannot detect internal generative instabilities, even under ID prompts. Thus, Stage 2 monitors the _generation instability score R_ online and triggers a fallback when the current reference becomes failure-prone. 

_(1) Is R a Meaningful Indicator?_ We validate _R_ against downstream tracking error. We divide generated sequences into 10-frame windows, recording _R_ and MPJPE (mm), then group them into _shared absolute R_ quintiles across ID (BABEL val., 220,944 windows) and OOD (Type B, 7,161 windows) sequences, excluding windows after tracking failure. Figure 4 shows MPJPE increases monotonically with _R_ in both domains, confirming that high- _R_ references are harder to track. OOD windows also skew heavily toward the high-instability regime (Q5: _n_ =4 _,_ 466 vs. Q1: _n_ =178). 


Fig. 5. **Instability-Triggered Safe Fallback.** When _R_ exceeds threshold, Stage 2 overrides the command with a standing prompt and interpolates to a nominal pose. Without Stage 2 the robot collapses on the unstable reference; with it, the robot remains stable and awaits the next prompt. 

Importantly, this trend holds _within ID alone_ : even after Stage 1 acceptance, some ID windows fall into the highinstability regime (ID Q5: 87.4mm), exhibiting larger errors than low- _R_ OOD windows (OOD Q1: 56.6mm). This shows Stage 1 alone is insufficient and motivates Stage 2. 

We further validate the design of _R_ : as a fall predictor it outperforms the mean directional sensitivity _g_ ¯ on matched rollouts (AUC 0.617 vs. 0.592), and _R_ reaches an AUC of up to 0.899 with large-scale trackers. The F1-optimal threshold on evaluated rollouts is _τ_<sup>_∗_</sup> =4 _._ 9—closely matching our deployed _τ_ stab = 5 _._ 0—with a cross-tracker spread of only _±_ 0.3, indicating that the gate’s operating point is stable across controllers. 

_(2) How Does R Behave During Streaming Generation?_ Figure 5 (top, mid) shows _R_ during streaming. For stable ID prompts ( _e.g_ ., “walk forward”, “wave hands”), _R_ remains low and smooth. Conversely, for extreme dynamics (“Taekwondo”), _R_ sharply spikes, indicating unreliable flow dynamics and often preceding motion collapse. 

_(3) Instability Score-Triggered Safe Fallback:_ When _R_ exceeds a threshold _τ_ stab, Stage 2 temporarily overrides the input with a safe “stand” prompt, interpolates the reference toward a predefined standing pose, and awaits the next input. Figure 5 (bottom) shows the impact: without Stage 2 (w/o SFB), the tracker collapses; with Stage 2 enabled (w/ SFB), the system transitions to standing and remains stable. 

Finally, Stage 3 performs deterministic output-level checks on joint position, velocity, and acceleration limits as the ultimate fail-safe before execution. 

## _D. Real-Time Performance (Q3)_ 

Since **SafeFlow** shares the text encoder [26] and tracking controller with TextOp [8], we report generator and safetygate latency only (RTX A6000, average of 100 runs). As Table III shows, physics-guided sampling increases latency, but _Reflow_ distillation reduces generation to 10 _._ 80 ms. The 3-Stage Safety Gate adds 3 _._ 98 ms cumulatively, yielding 14 _._ 78 ms ( _∼_ 67 _._ 7 Hz) for the guarded generator. The shared text encoder ( _∼_ 2 _._ 99 ms) and ONNX-compiled controller 


Fig. 6. **Real-Robot Deployment on Unitree G1.** A continuous long-horizon sequence spanning upper-body gestures and whole-body actions; a high-risk prompt (“double backflip”) is filtered by the Safety Gate, triggering a standing fallback and allowing execution to continue—demonstrating sim-to-real transfer and deployment-time safety filtering. 

TABLE III **INFERENCE LATENCY AND PIPELINE BREAKDOWN. SAFEFLOW** ACHIEVES REAL-TIME INFERENCE VIA REFLOW ACCELERATION, WHILE DEPLOYMENT-TIME SAFETY GATES ADD MINIMAL OVERHEAD. 

|**Pipeline Component**|**Added (ms)**_↓_|**Latency (ms)**_↓_|**Freq. (Hz)**_↑_|
|---|---|---|---|
|TextOp Generator [8]|-|23.59_±_1.60|42.4|
|**SafeFlow** Generator (+ Guid.)|-|172.03_±_6.33|5.8|
|**SafeFlow** Generator (+ Guid. & Reflow)|-|10.80_±_0.98|92.6|
|+ Stage 1 (Semantic OOD)|0.006_±_0.006|10.81_±_0.98|92.5|
|+ Stage 2 (Generation Instability)|3.96_±_1.04|14.77_±_1.43|67.7|
|+ Stage 3 (Hard Kinematic Screen)|0.013_±_0.003|**14.78**_±_1.43|**67.7**|


( _∼_ 0 _._ 98 ms) add little overhead, supporting real-time closedloop control with asynchronous reference generation [8]. 

## _E. Real-Robot Deployment (Q4)_ 

We deploy **SafeFlow** on the Unitree G1 to evaluate sim-toreal transfer and on-hardware safety. As shown in Fig. 6, the robot executes a continuous, long-horizon sequence—from upper-body gestures (“wave hands”, “punch”) to demanding whole-body dynamics (“squat down”, “hop on left leg”)— without intermediate stops or manual resets. Crucially, when a high-risk prompt (“double backflip”) known to induce unstable generation is issued mid-sequence, the safety gate filters the unsafe reference before it reaches the tracking controller and triggers the standing fallback, after which execution continues under subsequent prompts. These results demonstrate expressive long-horizon behaviors with enforced deployment-time safety on real hardware. 

**Quantitative Hardware Comparison.** We further quantify hardware tracking fidelity by replaying each method’s reference on the G1 for three commands (five 10 s trials per cell) and measuring _E_ dof from the joint encoders against each method’s _own_ reference (23 non-wrist joints, as in Table I). All executed trials completed without falls or operator intervention, and **SafeFlow** tracks more accurately on every command (16–52% lower _E_ dof ; Table IV). Since _E_ dof is measured against each method’s own reference, low error cannot be obtained merely by conservative generation: 

TABLE IV 

**REAL-ROBOT JOINT TRACKING ON UNITREE G1.** _E_ dof (DEG): ENCODER-MEASURED MAE OVER THE 23 NON-WRIST JOINTS AGAINST EACH METHOD’S OWN REFERENCE (MEAN _±_ STD OVER 5 TRIALS). 

|Command|TextOp [8]|**SafeFlow (Ours)**|
|---|---|---|
|“_Wave hands_”|9.0_±_0.2|**4.4**_±_0.1|
|“_Squat down_”|9.3_±_0.4|**6.1**_±_0.2|
|“_Boxing_”|17.5_±_0.8|**14.6**_±_0.2|


Fig. 7. **Joint-Limit Infeasibility on Real Hardware** (“Squat down”, right knee). TextOp’s reference commands the knee 10–20<sup>_◦_</sup> beyond the hardware limit for the entire hold phase, which the robot cannot track; **SafeFlow** ’s reference stays within limits and is tracked closely. 

on “Squat down”, where the two references have comparable amplitude and mean joint speed (within 19%), the gap persists. Moreover, the gap concentrates where TextOp’s references leave the feasible range: on “Squat down”, 18.0% of its commanded joint samples lie outside the G1’s hardware limits (Fig. 7), tracking error on those samples is 3.2 _×_ that of in-limit samples (21.4<sup>_◦_</sup> vs. 6.7<sup>_◦_</sup> ), and the three violating joints account for 88% of the per-joint gap—the deploymentside counterpart of the JV statistics in Table I. 

## V. CONCLUSION 

**SafeFlow** advances real-time text-driven humanoid control toward safer deployment by addressing physically infeasible generations and OOD prompts through physicsguided generation and selective execution. Physics-Guided Rectified Flow with Reflow improves real-robot executability 

and real-time efficiency, while a 3-Stage Safety Gate filters semantic OOD inputs, generative instabilities, and kinematic violations before execution. Experiments on the Unitree G1 demonstrate improved physical feasibility, tracking success, and inference speed over diffusion- and retargeting-based baselines, with consistent gains across multiple downstream trackers. Overall, **SafeFlow** enables robust text-conditioned humanoid control under open-ended commands. 

## REFERENCES 

- [1] G. Tevet, S. Raab, B. Gordon, Y. Shafir, D. Cohen-Or, and A. H. Bermano, “Human motion diffusion model,” in _ICLR_ , 2023. 

- [2] M. Petrovich _et al._ , “TMR: Text-to-motion retrieval using contrastive 3D human motion synthesis,” in _ICCV_ , 2023. 

- [3] X. Chen, B. Jiang, W. Liu, Z. Huang, _et al._ , “Executing your commands via motion diffusion in latent space,” in _CVPR_ , 2023. 

- [4] J. Zhang, Y. Zhang, _et al._ , “Generating human motion from textual descriptions with discrete representations,” in _CVPR_ , 2023. 

- [5] M. Zhang, Z. Cai, _et al._ , “Motiondiffuse: Text-driven human motion generation with diffusion model,” _arXiv:2208.15001_ , 2022. 

- [6] A. Serifi _et al._ , “Robot motion diffusion model: Motion generation for robotic characters,” in _SIGGRAPH Asia Conference Papers_ , 2024. 

- [7] Z. Zhuang, T. Wang, _et al._ , “Humanoid-r0: Bridging text-to-motion generation and physical deployment via RL,” 2025. 

- [8] W. Xie, J. Zheng, J. Han, J. Shi, _et al._ , “Textop: Real-time interactive text-driven humanoid robot motion generation and control,” _arXiv:2602.07439_ , 2026. 

- [9] Y. Yuan, J. Song, U. Iqbal, _et al._ , “PhysDiff: Physics-guided human motion diffusion model,” in _ICCV_ , 2023. 

- [10] X. Liu _et al._ , “Flow straight and fast: Learning to generate and transfer data with rectified flow,” _arXiv:2209.03003_ , 2022. 

- [11] Y. Xue, W. Dong, _et al._ , “A unified and general humanoid whole-body controller for fine-grained locomotion,” _arXiv:2502.03206_ , 2025. 

- [12] W. Xie, C. Bai, _et al._ , “Humanoid whole-body locomotion on narrow terrain via dynamic balance and reinforcement learning,” _arXiv:2502.17219_ , 2025. 

- [13] N. Mahmood, N. Ghorbani, N. F. Troje, _et al._ , “Amass: Archive of motion capture as surface shapes,” in _ICCV_ , 2019. 

- [14] A. Allshire, H. Choi, J. Zhang, _et al._ , “Visual imitation enables contextual humanoid control,” _arXiv:2505.03729_ , 2025. 

- [15] Z. Shen, H. Pi, Y. Xia, _et al._ , “World-grounded human motion recovery via gravity-view coordinates,” in _SIGGRAPH Asia 2024 Conference Papers_ , 2024. 

- [16] Z. Chen, M. Ji, X. Cheng, _et al._ , “GMT: General motion tracking for humanoid whole-body control,” _arXiv:2506.14770_ , 2025. 

- [17] Q. Liao, T. E. Truong, X. Huang, _et al._ , “Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv:2508.08241_ , 2025. 

- [18] Z. Zhang, J. Guo, C. Chen, J. Wang, C. Lin, _et al._ , “Track any motions under any disturbances,” _arXiv:2509.13833_ , 2025. 

- [19] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, _et al._ , “Sonic: Supersizing motion tracking for natural humanoid whole-body control,” _arXiv:2511.07820_ , 2025. 

- [20] T. He, Z. Luo, W. Xiao, C. Zhang, _et al._ , “Learning human-tohumanoid real-time whole-body teleoperation,” in _IROS_ , 2024. 

- [21] T. He, Z. Luo, _et al._ , “Omnih2o: Universal and dexterous human-tohumanoid whole-body teleoperation and learning,” in _CoRL_ , 2024. 

- [22] Y. Ze, Z. Chen, J. P. Araújo, _et al._ , “Twist: Teleoperated whole-body imitation system,” _arXiv:2505.02833_ , 2025. 

- [23] K. Zhao _et al._ , “DartControl: A diffusion-based autoregressive motion model for real-time text-driven motion control,” in _ICLR_ , 2025. 

- [24] Y. Wang, J. Lin, A. Zeng, _et al._ , “PhysHOI: Physics-based imitation of dynamic human-object interaction,” _arXiv:2312.04393_ , 2023. 

- [25] Y. Shao _et al._ , “Langwbc: Language-directed humanoid whole-body control via end-to-end learning,” _arXiv:2504.21738_ , 2025. 

- [26] A. Radford, J. W. Kim, _et al._ , “Learning transferable visual models from natural language supervision,” _arXiv:2103.00020_ , 2021. 

- [27] Y. Xie, V. Jampani, L. Zhong, _et al._ , “Omnicontrol: Control any joint at any time for human motion generation,” in _ICLR_ , 2024. 

- [28] M. Mittal _et al._ , “Isaac lab: A gpu-accelerated simulation framework for multi-modal robot learning,” _arXiv:2511.04831_ , 2025. 

- [29] A. R. Punnakkal, A. Chandrasekaran, _et al._ , “Babel: Bodies, action and behavior with english labels,” in _CVPR_ , 2021. 

- [30] Z. Sun, B.-S. Huang, Y. Peng, _et al._ , “MOSAIC: Bridging the sim-toreal gap in generalist humanoid motion tracking and teleoperation with rapid residual adaptation,” _arXiv preprint arXiv:2602.08594_ , 2026. 

- [31] A. Paszke, S. Gross, _et al._ , “Pytorch: An imperative style, highperformance deep learning library,” _arXiv:1912.01703_ , 2019. 

- [32] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for model-based control,” in _IROS_ , 2012. 

- [33] F. Bogo, A. Kanazawa, C. Lassner, _et al._ , “Keep it SMPL: Automatic estimation of 3D human pose and shape from a single image,” in _ECCV_ , 2016. 

- [34] C. Guo, S. Zou, X. Zuo, _et al._ , “Generating diverse and natural 3d human motions from text,” in _CVPR_ , 2022. 

- [35] G. Team, R. Anil, S. Borgeaud, _et al._ , “Gemini: A family of highly capable multimodal models,” _arXiv:2312.11805_ , 2023. 

