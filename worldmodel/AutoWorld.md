---
title: "AutoWorld: Learning Multi-Agent Traffic Simulation with Self-Supervised World Models"
date: "2026-03-30"
authors: "Mozhgan Pourkeshavarz; Tianran Liu; Nicholas Rhinehart"
url: https://arxiv.org/abs/2603.28963
pdf: https://arxiv.org/pdf/2603.28963
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.28963)** / [論文ページ](https://arxiv.org/abs/2603.28963)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **AutoWorld: Learning Multi-Agent Traffic Simulation with Self-Supervised World Models** 

**Mozhgan Pourkeshavarz** , **Tianran Liu** , **Nicholas Rhinehart** 

Learning, Embodied Autonomy, and Forecasting (LEAF) Lab, University of Toronto 

Simulation with realistic traffic agents is essential for validating autonomous driving systems. Existing data-driven simulators learn agent behavior from higher-level abstractions such as 3D bounding boxes and polylines, inferred by upstream perception pipelines. These lossy abstractions discard sensory context that directly shapes agent behavior, limiting the distributional realism that simulation aims to reproduce. To address this limitation, we propose AutoWorld, a traffic simulation framework that grounds agent behavior in raw sensor observations through a self-supervised world model trained on LiDAR occupancy data. Given world model samples, AutoWorld constructs a coarse-to-fine predictive scene context as input to a multi-agent motion generation model. Furthermore, we designed a motionaware latent supervision objective that enriches AutoWorld’s latent representation of scene dynamics. To better exploit this latent space during inference, AutoWorld employs a cascaded Determinantal Point Process framework to guide diversity-aware sampling across both the world model and motion model. Experiments on nuPlan and Waymo demonstrate that AutoWorld improves generation realism, with larger gains in partially observed scenarios where trajectory abstractions are most limited, reducing collision rates by 36%. AutoWorld also remains physically plausible under planner-controlled ego behavior and supports controllable, diverse safety-critical scenario generation. 


**Project Website: https://github.com/mpourkeshavarz/AutoWorld** 


### **1 Introduction** 

Traffic simulation is essential for developing and testing autonomous driving systems. Data-driven approaches have gained increasing attention for their ability to overcome limitations of heuristic-based simulators. Existing methods [7, 19, 22, 38, 40, 53, 58, 59, 65] learn agent behavior from motion forecasting datasets [2, 9], which represent driving scenes as sequences of 3D bounding boxes and polylines, abstractions inferred by upstream perception pipelines. However, these trajectory abstractions are a lossy compression of the original sensory observations, discarding rich scene information that shapes how real drivers behave, including geometric structure and occlusion context. For example, a driver slowing near a blind intersection responds to raw sensory geometry that no bounding box encodes. Models trained on these abstractions therefore learn the kinematic response without the sensory cause, which limits their ability to reproduce the distributional realism that faithful simulation requires. While [5] demonstrated that augmenting trajectory data with raw LiDAR observations improves agent behavior generation, how to effectively harness this signal for traffic simulation remains largely unexplored. 

Models that forecast future sensor observations, with or without action conditioning, are broadly referred to as “world models” and have proven effective for modeling high-dimensional environments [24, 66]. In autonomous driving, video-generative world models have been widely explored, with a primary focus on photorealistic scene synthesis [11, 16, 43, 50, 55]. To favor geometric information, a complementary line of work investigates world modeling through LiDAR data, framed as LiDAR or occupancy forecasting [30, 51, 52, 57]. Yet, these methods typically rely on semantic occupancy prediction, which requires costly dense annotation, and apply 

1 


**Figure 1 Comparison of traffic simulation approaches** . (Left) Conventional traffic simulation methods. (Right) AutoWorld grounds simulation in future scene occupancies predicted by a self-supervised LiDAR world model, preserving sensory context discarded by trajectory representations. 

uniform supervision across spatial regions, underemphasizing the motion dynamics most relevant to behavior generation for traffic simulation. 

In this work, rather than learning agent behavior solely from trajectory abstractions, we propose to ground traffic simulation in a world model learned directly from raw LiDAR observations (See Fig. 1). Our key insight is that a self-supervised world model of the driving environment can capture the geometric and dynamic context that trajectory data discards, providing a richer foundation for realistic behavior generation. To this end, we introduce **AutoWorld** , a traffic simulation framework that conditions a multi-agent motion generation model on world model predictions, transferring the world model’s sensor-grounded understanding of scene dynamics into the simulation process. 

AutoWorld trains a latent LiDAR world model with a motion-aware supervision objective that prioritizes dynamic scene elements without using semantic labels, allowing fully self-supervised training. We then propose a conditional diffusion policy that leverages future latent occupancies and a predictive scene context, encapsulating the anticipated occupancy sequence, to model the joint distribution of future agent behaviors. By doing so, AutoWorld is equipped with a coarse-to-fine context derived from sensory observation. Notably, agent identity is not provided during world model learning; the world model captures only occupancy dynamics, while agent-specific behaviors are produced by the diffusion model, allowing the two components to play complementary roles. Furthermore, to better exploit the latent representations of both models, we propose a cascaded latent sampling strategy applied at inference time without additional training. This strategy promotes structured exploration across two complementary levels: the scene level, guiding sampling of future occupancies from the world model, and the agent level, driving variation in the diffusion-based motion generation. We formalize this using a flow space determinantal point process (DPP) [25] with a quality-weighted kernel that balances and sample realism, enabling AutoWorld to cover the space of plausible scene evolutions and agent behaviors without modifying training. 

In summary, our **main contributions** are: (1) We propose AutoWorld, a traffic simulation framework that grounds traffic simulation in raw sensor observations through a self-supervised LiDAR world model, addressing the fundamental limitations of trajectory-based approaches. (2) We introduce a motion-aware latent supervision objective that emphasizes dynamic scene elements, enabling self-supervised world model training without semantic labels. (3) We propose a cascaded latent sampling strategy based on a quality-weighted DPP that promotes structured exploration of the joint latent space of both models at inference. (4) Extensive experiments on nuPlan and Waymo demonstrate AutoWorld’s competitive generation realism, with larger gains under partial observability. AutoWorld remains reactive to planner-induced ego behaviors and enables controllable and diverse safety-critical scenario generation, while ablations validate its key components. 

### **2 Related Work** 

We describe two related areas: (1) Traffic Simulation and (2) World Models in Autonomous Driving. 

**Traffic Simulation.** Traffic simulation models the distribution of multi-agent behaviors in dynamic driving environments. Recently, data-driven approaches have gained significant attention as they can overcome limitations of heuristic-based simulators such as poor adaptability to ego-vehicle behavior. Prior work spans CVAEs [20, 46, 54], Transformer-based architectures [12, 36, 44, 64], diffusion models [19, 21, 32, 41, 61, 62], 

2 


**Figure 2 Overview of AutoWorld** . AutoWorld learns latent scene dynamics from unlabeled LiDAR occupancy sequences and uses predicted future occupancies to condition diffusion-based motion generation. At inference, a cascaded sampling strategy further improves use of the learned latent spaces across both scene evolution and agent behavior without additional training. 

and more recently autoregressive next-token formulations for joint trajectory generation [39, 40, 53, 58, 59, 65]. Despite architectural differences, these methods learn behavior solely from trajectory abstractions, which discard sensory cues shaping real driving behavior [5]. In contrast, AutoWorld grounds behavior generation in raw sensor observations through self-supervised world models, mitigating the information bottleneck of trajectory-only approaches. 

**World Models in Autonomous Driving.** World models represent and forecast the evolution of driving environments. One line of work uses future sensor prediction for end-to-end driving, either jointly optimized with planning [15, 28, 37, 60] or used for pretraining perception encoders [33, 34, 56]. Another line develops generative neural simulators that produce future video [16, 49, 50], LiDAR [30, 51, 52, 57], or multimodal observations [1] for synthesis, counterfactuals, or imagination-based planning. These methods mainly emphasize fidelity or controllability, often decoupled from behavior modeling. Rather than treating the world model as a standalone generator, AutoWorld integrates its predictions into motion generation, providing sensor-grounded scene context for traffic simulation. 

### **3 AutoWorld** 

AutoWorld grounds traffic simulation in raw sensor observations by building simulation around a worldmodeling formulation. Instead of modeling future agent behavior in isolation, AutoWorld models the joint future distribution of sensor observations and agent states, factorized into a self-supervised LiDAR world model and a diffusion-based motion generation model. This factorization makes world modeling the interface through which raw sensor data informs traffic simulation: the world model learns predictive scene dynamics from high-dimensional unlabeled LiDAR data, while the motion model retains structured trajectory-based inputs for agent-centric behavior generation. 

Specifically, we first learn a motion-aware latent occupancy world model in a fully self-supervised manner from unlabeled LiDAR data to forecast future latent occupancies (Sec. 3.2). From these predictions, we build a coarse-to-fine representation of the future scene to condition the diffusion-based motion generation model. (Sec. 3.3). Finally, to promote structured exploration of plausible multi-agent behaviors, we introduce a cascaded latent sampling strategy applied at inference time without additional training (Sec. 3.4). The overall framework is illustrated in Fig. 2. 

#### **3.1 Problem Formulation.** 

Given past states of _A_ agents over _Th_ and contextual information, traffic simulation predicts their future states over _Tf_ . At timestep _t_ , agent states are _st_ = [ _st_<sup>1</sup><sup>_, . . . , sA_</sup> _t_<sup>],where</sup><sup>_si_</sup> _t_<sup>=(</sup><sup>_xi_</sup> _t_<sup>_, y_</sup> _t_<sup>_i, v_</sup> _t_<sup>_i, θ_</sup> _t_<sup>_i_)denotesthe2Dposition,</sup> speed, and yaw of agent _i_ . We denote the history by _St−Th_ : _t_ = [ _st−Th, . . . , st_ ], with LiDAR observations _Ot−Th_ : _t_ available over the same horizon. Context includes an HD map _V ∈_ R<sup>_v×dv_</sup> with up to _v_ vector points of dimension _dv_ , and traffic-light states _R ∈_ R<sup>_r×dr_</sup> for up to _r_ lights with feature dimension _dr_ . Actions are 

3 

_at_ = [ _a_<sup>1</sup> _t_<sup>_, . . . , aA_</sup> _t_<sup>],where</sup><sup>_ai_</sup> _t_<sup>=(˙</sup><sup>_v_</sup> _t_<sup>_i,θ_˙</sup> _t_<sup>_i_)denotesaccelerationandyawrate.Ourflow-matchinganddiffusion</sup> timesteps, denoted _kµ_ and _kf_ , are distinct from the state-sequence timestep _t_ . 

#### **3.2 Motion-Aware Latent Occupancy Forecasting** 

**Latent Occupancy Forecasting.** We formulate our world model as a LiDAR-based occupancy predictor operating in the latent space of voxelized occupancies encoded by a VAE. We assume access to additional unlabeled LiDAR sequences _Ot−Th_ : _t_ + _Tf_ , which are used to train the latent occupancy predictor. Let _Zt−Th_ : _t_ denote past latent occupancies and _Zt_ +1: _t_ + _Tf_ the future sequence to be predicted. We build upon [30], which adopts a rectified flow formulation [31]. We denote the conditioning information as _c_<sup>_µ_</sup> = _{Zt−Th_ : _t, τt_<sup>ego</sup> _−Th_ : _t_<sup>_}_,</sup> where _τt_<sup>ego</sup> _−Th_ : _t_<sup>denotes the ego vehicle’s past trajectory embedding.The model learns a time-dependent velocity</sup> field _µθ_ ( _zt, t, c_<sup>_µ_</sup> ) that transports samples from a Gaussian prior toward a target future latent occupancy _z_ ˜. During training, we sample flow matching timestep _kµ ∼U_ (0 _,_ 1) and _z_ 0 _∼N_ (0 _, I_ ), construct the interpolation _zt_ = (1 _− t_ ) _z_ 0 + _tz_ ˜, and optimize the rectified flow objective in Eq. 1: 


**Motion-Aware Latent Supervision.** Occupancy grids are spatially imbalanced. Static structures dominate the volume while dynamic objects occupy sparse but behaviorally critical regions. Uniform flow supervision therefore biases learning toward static structure and underweights motion-driven evolution — an issue amplified in our fully unsupervised setting, which lacks the semantic labels that prior methods use to implicitly separate dynamic from static content. 

To address this, we introduce a motion-aware supervision strategy derived directly from temporal occupancy changes. Let _Yt_ and _Yt_ +∆ denote non-semantic occupancy grids with validity masks _Mt_ and _Mt_ +∆. After compensating for ego motion by warping _Yt_ into the frame of _t_ + ∆, producing _Y_<sup>˜</sup> _t→t_ +∆, we compute voxel-wise occupancy transitions: 


where _M_<sup>˜</sup> _t→t_ +∆ is the validity mask _Mt_ warped to the frame of _t_ + ∆. We downsample this motion map to the latent resolution to obtain _C_<sup>¯</sup> _t,_ ∆ _∈_ R<sup>_H×W_</sup> and construct a latent weight map _Wt_ ( _i, j_ ) = 1 + _λC_<sup>¯</sup> _t,_ ∆( _i, j_ ), where _λ >_ 0 controls the strength of motion emphasis. The resulting motion-aware rectified flow objective is 


where _Wt_ is normalized to unit spatial mean. This formulation preserves the standard rectified flow objective while biasing gradient magnitude toward temporally changing regions. 

#### **3.3 World-Model-Grounded Traffic Simulation** 

We formulate traffic simulation as conditional diffusion over joint future agent trajectories in the action space. Let _τ_ 0 = _a_<sup>1:</sup> _t_ +1:<sup>_A_</sup> _t_ + _Tf_<sup>denote the clean future action trajectory over the prediction horizon</sup><sup>_Tf_.The diffusion model</sup> generates trajectories by initializing from Gaussian noise _τKf ∼N_ (0 _, I_ ) and progressively reversing a predefined noising process over _Kf_ steps. This reverse process defines a conditional Markov chain _pψ_ ( _τkf −_ 1 _| τkf , c_<sup>_f_</sup> ), where _c_<sup>_f_</sup> denotes the conditioning information. At each denoising step _kf_ = _Kf , . . . ,_ 1, the transition is: 


where _fψ_ and Σ _kf_ are the reverse-transition mean predictor and variance schedule, respectively. 

**World-model Conditioning.** Given the world-model rollout _Z_<sup>ˆ</sup> _t_ +1: _t_ + _Tf_ = [ˆ _zt_ +1 _, . . . ,_ ˆ _zt_ + _Tf_ ], we construct a compact predictive scene context by temporally subsampling the predicted latent occupancies and aggregating them through multi-head cross-attention pooling (“MHCA”) with a learned token, defined as _g_ = MHCA(Q = _ξ,_ K = V = _ϕ_ 1( _{z_ ˆ _t_ + _eδ}e_<sup>_⌊T_</sup> =1<sup>_f /δ⌋_</sup> )), where _ϕ_ 1( _·_ ) indicates a learnable linear projection. The resulting context _g_ 

4 

summarizes the forecasted occupancies, where each latent occupancy encodes a predicted scene configuration without explicit agent identities. 

Next, we condition the diffusion denoiser on both local and global predictive cues, forming a coarse-to-fine guidance mechanism for multi-agent behavior generation. Specifically, for each future timestep _t_ + _r_ , where _r_ = 1 _, . . . , Tf_ , we combine the corresponding per-step latent occupancy ˆ _zt_ + _r_ with the global predictive scene context _g_ . As such, the timestep-specific diffusion condition is defined as _c_<sup>_f_</sup> _t_ + _r_<sup>= MHCA (Q =</sup><sup>_h,_K = V =</sup><sup>_ϕ_2([ˆ</sup><sup>_zt_+</sup><sup>_r⊕g_])),</sup> where _h_ denotes the scene encoding obtained from a query-centric Transformer [44]. The _⊕_ indicates concatenation along the token dimension, and _ϕ_ 2( _·_ ) maps the concatenated latent occupancies into a shared space. The full diffusion condition is therefore _c_<sup>_f_</sup> = _{c_<sup>_f_</sup> _t_ + _r_<sup>_}_</sup> _r_<sup>_T_</sup> =1<sup>_f_, which combines historical scene context with predicted</sup> future occupancies. This allows the diffusion model to generate agent-specific behaviors grounded in past observations while being guided by the world-model. 

#### **3.4 Cascaded Latent Sampling** 

To better exploit the learned latent spaces, we introduce a cascaded latent sampling strategy that applies Determinantal Point Processes (DPPs) [25, 35] at both the world-modeling and behavior-generation stages. At inference, this mechanism promotes structured exploration by discouraging similar latent samples, yielding diverse yet plausible future scene evolutions and agent behaviors. 

**Determinantal Point Processes.** Let _X_ = _{x_ ˆ<sup>(</sup><sup>_i_)</sup> _}_<sup>_K_</sup> _i_ =1<sup>_s_be the ground set of generated candidates, and let</sup><sup>_x_ˆ</sup><sup>_i∈_R</sup><sup>_d_.</sup> Let _κ_ : R<sup>_d_</sup> _×_ R<sup>_d_</sup> _→_ R be a symmetric positive semidefinite kernel (e.g. cosine similarity), and define the kernel matrix Λ _∈_ R<sup>_Ks×Ks_</sup> by Λ _ij_ = _κ_ (ˆ _x_<sup>(</sup><sup>_i_)</sup> _,_ ˆ _x_<sup>(</sup><sup>_j_)</sup> ). Following the standard L-ensemble DPP [25] formulation on a finite ground set, we define a DPP-based probability mass for the _Ks_ jointly generated samples, i.e., treating _X_ as the ground set, we evaluate the DPP probability of selecting the full subset as: _Pκ_ ( _X_ ) = det(Λ+det(Λ) _I_ )<sup>.</sup><sup>_Pκ_increases when</sup> samples are diverse and approximately linearly independent, and decreases as redundancy increases, becoming 0 when _X_ contains any exact duplicates under _κ_ (equivalently, when Λ is rank-deficient). This provides a principled continuous measure of diversity. However, maximizing diversity alone may push samples away from the data manifold. To balance diversity and plausibility, we incorporate quality-aware modulation [35] by assigning each sample a quality weight _q_<sup>(</sup><sup>_i_)</sup> _∈_ (0 _,_ 1] and defining _κq_ (ˆ _x_<sup>(</sup><sup>_i_)</sup> _,_ ˆ _x_<sup>(</sup><sup>_j_)</sup> ) = _q_<sup>(</sup><sup>_i_)</sup> _κ_ (ˆ _x_<sup>(</sup><sup>_i_)</sup> _,_ ˆ _x_<sup>(</sup><sup>_j_)</sup> ) _q_<sup>(</sup><sup>_j_)</sup> . This yields the quality-balanced kernel Λ<sup>_q_</sup> = diag( _q_ )Λ diag( _q_ ) and the quality-aware DPP probability _Pκ_<sup>_q_(</sup><sup>_X_) =</sup> det(Λdet(Λ<sup>_q_</sup> +<sup>_q_</sup> <u>)</u> _I_ )<sup>,</sup> whose maximization balances diversity and sample quality. 

**DPP-Guided Sampling.** To jointly generate _Ks_ diverse candidates � _x_ ˆ<sup>(</sup><sup>_i_)�</sup><sup>_K_</sup> _i_ =1<sup>_s_, we evaluate</sup><sup>_P_</sup> _κ_<sup>_q_over the predicted</sup> target outputs and incorporate a repulsive guidance term proportional to _∇_ log _Pκ_<sup>_q_into the flow ODE during</sup> sampling. This term encourages candidate trajectories to spread across distinct modes of the predictive distribution while maintaining high-quality solutions. The guidance is applied only at inference time and remains independent of the underlying training objective. We apply diversity-guided sampling at both world modeling and behavior generation through a two-stage cascaded inference procedure. First, we sample _N_ future latent occupancies from the world model _X_<sup>world</sup> =<sup>_._</sup> _{Z_<sup>ˆ</sup> _t_<sup>(</sup> +1:<sup>_i_)</sup> _t_ + _Tf_<sup>_}_</sup> _i_<sup>_N_</sup> =1<sup>, where each latent rollout represents a distinct plausible future occupancy development.We</sup> quantify rollout quality via the Mahalanobis distance of the one-step latent estimate to a Gaussian fit of the training data. Let _P_<sup>_q,_world</sup> =<sup>_._</sup> _Pκ_<sup>_q_(</sup><sup>_X_world).Thediversity-guidedworld-modelsamplingdynamicsfollowthe</sup> continuous-time flow formulation given by 


where _γ_ ( _._ ) controls the strength of diversification. Next, conditioned on the step-aware representation derived from each sampled latent representation, we generate _M_ agent behavior trajectories using our conditional diffusion model, _{τ_<sup>(</sup><sup>_i,j_)</sup> _}_<sup>_M_</sup> _j_ =1<sup>.Since behavior generation proceeds via discrete reverse diffusion steps, we apply</sup> diversity guidance as a gradient shift to the reverse-step mean at each timestep _kf_ . Let _P_<sup>_q,_motion</sup> =<sup>_._</sup> _Pκq_ ( _X_<sup>motion</sup> ). The diversity-guided sampling dynamics for the behavior trajectory simulation, similar to the dynamics for the world model, becomes 


5 

**Table 1 Simulation realism and physical plausibility on nuPlan.** Realism measures the distributional deviation from logged driving statistics (longitudinal/lateral acceleration magnitude and jerk); other metrics assess physical plausibility. D-dir. Viol. denotes driving-direction violation. 

|**Model**|**Realism**(_↓_)|**Collision**(_↓_)|**Off-road Time**(_↓_)|**D-dir. Viol.**(_↓_)|**Kinematic**(_↑_)|
|---|---|---|---|---|---|
|CTG [62]|0.584|27.79|25.22|16.59|79.37|
|GUMP [17]|0.472|23.81|30.57|20.52|73.48|
|SceneD. [42]|0.355|36.93|14.02|12.59|89.35|
|D. Policy [6]|0.604|33.68|19.84|21.00|88.29|
|Nexus [63]|0.318|27.19|16.03|15.64|84.41|
|OMEGA [29]|0.348|23.91|14.68|19.48|90.63|
|**AutoWorld (Ours)**|**0.266**|**8.14**|**5.93**|**7.31**|**94.89**|


where _c_<sup>_f_(</sup><sup>_i_)</sup> denotes the conditioning signal derived from the _i_ -th world-model rollout. For notational simplicity, we omit the stochastic noise term from the variance schedule. Trajectory embeddings are obtained from the scene encoder over agent states. At the behavior level, quality weights encode trajectory-space realism constraints, including collisions, kinematic infeasibility, and off-road violations [13], preventing diversity from favoring physically invalid rollouts. Overall, cascaded diversity-guided inference produces _N × M_ diverse and plausible rollouts. 

### **4 Experiments** 

Our experiments focus on five key questions: **Q1:** Does AutoWorld generate _realistic_ traffic behavior that matches real-world human driving? (Sec 4.1) **Q2:** What benefits does sensor-grounded world modeling provide over trajectory-based simulation? (Sec 4.2) **Q3:** Can AutoWorld exhibit realistic _reactiveness_ to planner-controlled ego behavior? (Sec 4.3) **Q4:** Beyond realism and reactiveness, can AutoWorld generate _diverse_ and _controllable_ behaviors? (Sec 4.4) **Q5:** How do AutoWorld’s key design choices contribute to its overall performance? (Sec 4.5) 

**Experimental Design.** AutoWorld is trained on **nuPlan** [23] and **Waymo** [45]. We follow Occ3D-Waymo [47] and NuPlan-Occ [27] to construct voxel-wise occupancy grids for world-model training. AutoWorld predicts 8 seconds ahead from 2 seconds of history on nuPlan and 1 second on Waymo in closed loop, following the Open Sim Agents benchmark. We use receding-horizon closed-loop simulation at 1 Hz for both occupancy and motion. The world model is rolled out autoregressively without access to future ground-truth occupancy. Notably, Waymo provides LiDAR data _only for the observation horizon_ in the test split. For DPP sampling, we use a cosine-similarity kernel at both levels with a power-cosine schedule [10], yielding weaker guidance early and stronger guidance toward the end of sampling. We follow each benchmark’s realism criteria. On nuPlan, we measure the Wasserstein distance between simulated and logged driving-profile distributions, together with log-independent physical-plausibility metrics, including collision rate, off-road time (fraction of simulation time spent off-road), driving-direction violation rate, and kinematic feasibility rate. On Waymo, we follow the Open Sim Agents protocol and report likelihood-based realism metrics covering kinematic behavior, agent interactions, and map adherence, their aggregate Realism Meta Metric (RMM), and minADE. Thus, realism metrics are benchmark-specific and not directly comparable across datasets. 

#### **4.1 Comparison to State of the Art** 

We begin by evaluating AutoWorld on nuPlan for distributional realism against logged human driving and physical plausibility, comparing against recent and reproduced traffic-generation methods in Table 1. AutoWorld achieves state-of-the-art performance across all reported metrics, improving both realism and physical plausibility over prior diffusion-based methods. Notably, it reduces collision by nearly 16 percentage points over the next-best method (8.14 vs. 23.91), while reducing off-road time (5.93 vs. 14.02 for the next best), showing that the collision reduction does not come at the expense of road adherence. We further evaluate AutoWorld on the Waymo Open Sim Agents benchmark, a complementary evaluation focused on matching the distribution of human driving behavior. Table 2 groups methods by training paradigm, following [14]. AutoWorld is trained solely with imitation objectives and uses no reward-based post-training. Among imitation-trained simulators, AutoWorld achieves the highest realism (RMM 0.7865) and matches RL-fine-tuned simulators without reward-based fine-tuning. See Figure 3 for qualitative examples. 

6 

**Table 2 Simulation realism under the Waymo Open Sim Agents evaluation protocol.** RMM (Realism Meta Metric) is a weighted aggregation of kinematic, interactive, and map-based metrics and serves as the primary ranking metric. 

|**Training**|**Method**|**RMM**(_↑_)|**Kinema**|**tic**(_↑_)|**Interactive**(_↑_)|**Map-based**(_↑_)|**minADE**(_↓_)|
|---|---|---|---|---|---|---|---|
||RLFTSim [8]|0.7857|0.49|27|0.8129|0.9183|1.3252|
|**RL Post-**|SMART-R1 [38]|0.7858|0.49|44|0.8110|0.9201|1.2885|
|**training**|DecompGAIL [14]|0.7864|0.49|19|0.8152|0.9176|1.4209|
||LLM2AD [48]|0.7779|0.48|46|0.8048|0.9109|1.2827|
||SMART [53]|0.7814|0.48|54|0.8089|0.9153|1.3931|
|**Imitation**|CAT-K [58]|0.7846|**0.49**|**31**|0.8106|0.9177|1.3065|
|**Li**|TrajTok [59]|0.7852|0.48|87|0.8116|**0.9207**|1.3179|
|**earnng**|SceneStreamer [3|9]<br>0.7731|0.44|93|0.8084|0.9127|1.4252|
||**AutoWorld (Ours)**|<br>**0.7865**|**0.49**|**31**|**0.8143**|0.9185|**1.3051**|
|0S||3S||7S||8S||
|0S||3S||7S||8S||


**Figure 3 Qualitative rollout comparison.** Trajectory-baseline (top) leads to a collision between the vehicle <mark>( )</mark> and pedestrian ( <mark>)</mark> , while AutoWorld (bottom) maintains a realistic yielding interaction. 

#### **4.2 Benefit of Sensor-Grounded Simulation** 

To study when raw sensor data provides information beyond lossy trajectory abstractions, we consider occlusion as a representative test case [5], following the protocol of [26]. Both Waymo and nuPlan provide high-quality agent tracks from offline auto- 


labeling pipelines [9, 23], allowing trajectories to persist even when agents are unobservable by ego sensors. We estimate occlusion using BEV line-of-sight ray casting from the ego vehicle and count, for each valid agent, timesteps where it is geometrically occluded but present in the trajectory labels. We compute a scene-level occlusion score and form equal-sized **Low-** , **Moderate-** , and **High-Occlusion** subsets with comparable agent densities. We compare AutoWorld against Nexus [63], a recent diffusion-based SOTA with public code and checkpoints, and two controlled diffusion baselines.Traj.-Diffusion predicts joint multi-agent actions from trajectory context only, while LiDAR-Diffusion additionally incorporates LiDAR observations, fused with 

**Figure 4 Simulation performance across occlusion levels** Dashed lines denote low-occlusion performance as reference for degradation at higher occlusion levels. 

HD-map features following DeTra [3]. Figure 4 reveals a clear sensitivity of trajectory-based simulation to partial observability on nuPlan. As occlusion increases, Nexus and Traj.-Diffusion degrade substantially in realism and physical plausibility. Directly incorporating LiDAR alleviates this degradation, reducing collision rate from 58.01% to 42.68% over Traj.-Diffusion under high occlusion. AutoWorld further reduces collisions to 14.63%— _about 36 percentage points below Nexus_ —while achieving a realism score of 0.298 and substantially 

7 

less degradation across occlusion levels. These results indicate that sensory information is valuable beyond trajectory abstractions, and that _explicitly modeling sensory-world dynamics_ is more effective than direct sensor conditioning. 

#### **4.3 Closed-Loop Reactiveness** 

The evaluations in Sec. 4.1 let the behavior model control both the ego and surrounding agents. To test reactiveness beyond this self-controlled setting, we instead use an independent ego planner while the simulator controls surrounding agents. We consider both rule-based and learning-based planners. As shown in Tab. 3, AutoWorld remains robust under externally controlled ego behavior, consistently outperforming Nexus across both planners. Compared with its self-controlled setting, AutoWorld retains high kinematic feasibility (94.89 _→_ 89.38/88.05) while maintaining substantially lower collision and offroad rates than Nexus. This demonstrates that AutoWorld can respond safely and feasibly when ego behavior is generated independently of the simulator. 

**Table 3 Closed-loop reactiveness under plannercontrolled ego behavior on nuPlan.** The ego vehicle is controlled by an external planner, while all other agents are generated by the simulator. E2A/A2A denote egoto-agent and agent-to-agent collision rates, respectively. 

|**Model**|**Collisi**<br>**E2A**|**on**(_↓_)<br>**A2A**|**Off-road**<br>**Time**(_↓_)|**Kinem-**<br>**atic**(_↑_)|
|---|---|---|---|---|
|**_Rule-based_**|**_Planner_**||||
|Nexus|34.51|22.02|17.93|81.59|
|AutoWorld|10.48|8.93|12.69|89.38|
|**_Learning-b_**|**_ased Plan_**|**_ner [6]_**|||
|Nexus|38.29|27.24|21.83|74.46|
|AutoWorld|13.05|11.32|13.25|88.05|


#### **4.4 Diverse and Controllable Simulation** 

A useful simulator should support both _diverse_ and _controllable_ generation. We probe these properties through safety-critical scenario generation, explicitly steering the simulator toward challenging interactions with a downstream planner. Diffusion models naturally support inference-time guidance, unlike the less explicit control of next-token prediction methods. We therefore investigate whether AutoWorld can generate targeted safety-critical interactions while preserving its simulation realism. Following Safe-Sim [4], we evaluate on nuPlan with a planner in the loop and apply the same safety-critical guidance objective to AutoWorld and Nexus. The objective steers a designated adversarial agent toward collision with the planner-controlled ego while discouraging other-agent collisions and off-road behavior. As shown in Table 5, AutoWorld achieves a higher adversarial collision rate than Nexus (41.84 vs. 36.12), while substantially reducing unintended collisions (7.03 vs. 23.68) and off-road time (3.60 vs. 13.92). We further assess diversity through the variance of collision properties across generated outcomes, following Safe-Sim. DPP increases diversity across all three attributes, particularly relative speed (1.27 _→_ 4.58) and collision point (1.53 _→_ 6.19), while improving both controllability and realism. 

**Figure 5 Controllable and diverse safety-critical scenario generation on nuPlan.** Target Collision denotes ego– adversarial-agent collision, while Non-Target Collision denotes all other collisions. Off-road Time is measured for the adversarial agent, and Relative Speed is the ego–adversarial speed at collision. AutoWorld achieves a higher target collision rate while substantially reducing non-target collisions; DPP sampling further increases collision diversity. 

|||**Collision**|**Metrics**||**Collisi**|**on Diversity (**|**Var)**(_↑_)|
|---|---|---|---|---|---|---|---|
|**Model**|**Target**<br>**Collision**(_↑_)|**Non-Target**<br>**Collision**(_↓_)|**Off-road**<br>**Time**(_↓_)|**Realism**(_↓_)|**Angle**<br>**(rad)**|**Relative**<br>**Speed(m/s)**|**Point**<br>**(m)**|
|Nexus|36.12|23.68|13.92|0.437|2.41|1.04|1.86|
|AutoWorld-DPP|34.56|9.42|5.28|0.289|1.93|1.27|1.53|
|AutoWorld+DPP|**41.84**|**7.03**|3.60|**0.274**|3.77|**4.58**|**6.19**|


#### **4.5 Ablation Studies** 

**Motion-Aware Latent Supervision.** We study whether motion-aware latent supervision improves dynamic scene forecasting without semantic labels and whether these gains transfer to traffic simulation. We compare semantic supervision (Sem-RF), uniform non-semantic supervision (NSem-RF), and our motion-aware nonsemantic supervision (NSem-MA-RF) on Waymo. Table 4 shows that uniform supervision performs reasonably on static regions but underperforms on dynamic ones, indicating a bias toward dominant static occupancy. 

8 

**Table 4 Effect of motion-aware latent supervision on Table 5 Ablation study on world-model grounding and Waymo.** The MA-RF objective improves world modeling **DPP sampling strategies on Waymo** . The design choices and translates into gains in traffic simulation without reprovide complementary gains, with full AutoWorld achieving quiring semantic labels. Except for FVD(10<sup>_−_3</sup> ) and mithe best performance. Higher values are better. nADE, higher values are better. 

|||||**fi**|**fi**|**Model**|**RMM**|**Kinematic**|**Interactive**|**Map-based**|
|---|---|---|---|---|---|---|---|---|---|---|
||**W**|**orld mo**|**del**|**Traffic s**|**fi imulation**|AutoWorld|0.7746|0.4878|0.7968|0.9099|
|**Model**|**FVD**|**IoUst**|**IoUd**|**RMM**|**minADE**|w/o mo-DPP|0.7648|0.4846|0.7926|0.8892|
|Sem-RF|23|0.89|**y**<br>0.73|0.7651|1.4081|w/o occ-DPP|0.7563|0.4833|0.7758|0.8871|
|NSem-RF<br>NSem-MA-RF|51<br>35|0.85<br>0.87|0.58<br>0.71|0.7547<br>0.7618|1.4826<br>1.4334|w/o DPP<br>w/o WM|0.7597<br>0.7472|0.4840<br>0.4749|0.7839<br>0.7741|0.8861<br>0.8682|


Motion-aware supervision mitigates this bias, raising dynamic IoU to 0.71 while preserving static IoUst (0.87), and improves rollout fidelity (FVD: 51 vs. 35). These world-model gains translate to simulation, improving both realism and trajectory accuracy over uniform supervision (RMM: 0.7547 to 0.7618), nearly matching the semantic baseline in RMM. Overall, motion-aware supervision provides a label-free alternative that strengthens dynamic forecasting and closes much of the gap to semantic supervision. 

**World-model Grounding and Cascaded Sampling.** Table 5 shows that world-model grounding is the primary contributor to AutoWorld’s performance. Removing the world model (WM) leads to the largest degradation across all metric groups, reducing RMM from 0 _._ 7746 to 0 _._ 7472 while also lowering kinematic, interactive, and map-based scores. Diversity sampling further provides consistent gains on top of world-model grounding. Removing motion-level DPP (mo-DPP) reduces interactive realism (0 _._ 7968 _→_ 0 _._ 7926), whereas removing occupancy-level DPP (occ-DPP) causes a larger drop in overall realism (0 _._ 7746 _→_ 0 _._ 7563). Notably, removing both DPP modules still outperforms the variant without the world model, indicating that predictive scene grounding contributes more substantially than sampling diversity alone. Combining world-model grounding with cascaded DPP sampling yields the best performance. Ablations use data from the Waymo interactive validation split. 

**Scaling with Additional Data.** Finally, we investigate whether sensor-grounded world modeling provides a more scalable path for leveraging additional data. We compare against the trajectorydiffusion baseline from Sec. 4.2, augmented to match AutoWorld’s parameter count. The baseline converts additional data into trajectory supervision, while AutoWorld uses the corresponding LiDAR observations to incrementally train its world model. As shown in Fig. 6, AutoWorld improves more consistently with data, while the trajectory baseline quickly saturates. This suggests that world modeling better exploits sensor data by transforming raw observations into predictive scene context. While AutoWorld’s gains also diminish at larger scales, stronger world models and tighter integration of scene dynamics with behavior generation may enable further scaling, pointing to future directions. 


**Figure 6 Scaling with different data modalities on Waymo.** Dashed line denotes Traj.-Diffusion without additional data. 

### **5 Conclusion** 

We introduced **AutoWorld** , a world-model-grounded framework for traffic simulation that uses raw LiDAR observations to complement structured trajectory representations. Across nuPlan and Waymo, AutoWorld improves simulation realism and physical plausibility, with larger gains under partial observability. Additional experiments showed that AutoWorld reacts consistently to planner-induced ego behaviors and supports controllable safety-critical scenario generation, while diverse sampling produces varied yet realistic agent behaviors. We further demonstrated more favorable scaling with additional raw sensor data than a trajectory-only baseline. Our results highlight sensor-grounded world modeling as a promising direction for realistic and scalable traffic simulation beyond trajectory abstractions. Future work can explore stronger multimodal world models, where cameras provide complementary semantic and appearance cues for more realistic and human-like behavior, as well as tighter coupling between sensory-world prediction and behavior generation. 

9 

### **6 Acknowledgments** 

This research was enabled in part by access to NVIDIA A100 GPUs and Google TPUs. 

### **References** 

- [1] Daniel Bogdoll, Yitian Yang, Tim Joseph, Melih Yazgan, and J Marius Zollner. Muvo: A multimodal generative world model for autonomous driving with geometric representations. In _2025 IEEE Intelligent Vehicles Symposium (IV)_ . IEEE, 2025. 

- [2] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In _2020 IEEE/CVF conference on computer vision and pattern recognition (CVPR)_ . IEEE, 2020. 

- [3] Sergio Casas, Ben Agro, Jiageng Mao, Thomas Gilles, Alexander Cui, Thomas Li, and Raquel Urtasun. Detra: A unified model for object detection and trajectory forecasting. In _European Conference on Computer Vision (ECCV)_ . Springer, 2024. 

- [4] Wei-Jer Chang, Francesco Pittaluga, Masayoshi Tomizuka, Wei Zhan, and Manmohan Chandraker. Safe-sim: Safetycritical closed-loop traffic simulation with diffusion-controllable adversaries. In _European conference on computer vision (ECCV)_ . Springer, 2024. 

- [5] Kan Chen, Runzhou Ge, Hang Qiu, Rami Ai-Rfou, Charles Qi, Xuanyu Zhou, Zoey Yang, Scott Ettinger, Pei Sun, Zhaoqi Leng, et al. Womd-lidar: Raw sensor dataset benchmark for motion forecasting. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024. 

- [6] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 2025. 

- [7] Lukas Brostek Christian Rossert, Johannes Drever. combot: an ensemble combination model combining results from smart-tiny-clsft with a cognitive behavior mode. _CVPR Workshop on Autonomous Driving (WAD)_ , 2025. 

- [8] Hunter Schofield Ehsan Ahmadi. Rlftsim: Multi-agent traffic simulation via reinforcement learning fine-tuning. _CVPR Workshop on Autonomous Driving (WAD)_ , 2025. 

- [9] Scott Ettinger, Shuyang Cheng, Benjamin Caine, Chenxi Liu, Hang Zhao, Sabeek Pradhan, Yuning Chai, Ben Sapp, Charles R Qi, Yin Zhou, et al. Large scale interactive motion forecasting for autonomous driving: The waymo open motion dataset. In _Proceedings of the IEEE/CVF international conference on computer vision (CVPR)_ , 2021. 

- [10] Shanghua Gao, Pan Zhou, Ming-Ming Cheng, and Shuicheng Yan. Masked diffusion transformer is a strong image synthesizer. In _2023 IEEE/CVF International Conference on Computer Vision (ICCV)_ . IEEE, 2023. 

- [11] Shenyuan Gao, Jiazhi Yang, Li Chen, Kashyap Chitta, Yihang Qiu, Andreas Geiger, Jun Zhang, and Hongyang Li. Vista: A generalizable driving world model with high fidelity and versatile controllability. _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 

- [12] Roger Girgis, Florian Golemo, Felipe Codevilla, Martin Weiss, Jim Aldon D’Souza, Samira Ebrahimi Kahou, Felix Heide, and Christopher Pal. Latent variable sequential set transformers for joint multi-agent motion prediction. _arXiv preprint arXiv:2104.00563_ , 2021. 

- [13] Cole Gulino, Justin Fu, Wenjie Luo, George Tucker, Eli Bronstein, Yiren Lu, Jean Harb, Xinlei Pan, Yan Wang, Xiangyu Chen, et al. Waymax: An accelerated, data-driven simulator for large-scale autonomous driving research. _Advances in Neural Information Processing Systems (NeurIPS)_ , 2023. 

- [14] Ke Guo, Haochen Liu, Xiaojun Wu, and Chen Lv. Decompgail: Learning realistic traffic behaviors with decomposed multi-agent generative adversarial imitation learning. In _International Conference on Learning Representations (ICLR)_ , 2026. 

- [15] Anthony Hu, Gianluca Corrado, Nicolas Griffiths, Zachary Murez, Corina Gurau, Hudson Yeo, Alex Kendall, Roberto Cipolla, and Jamie Shotton. Model-based imitation learning for urban driving. _Advances in Neural Information Processing Systems_ , 35:20703–20716, 2022. 

- [16] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 

10 

- [17] Yihan Hu, Siqi Chai, Zhening Yang, Jingyu Qian, Kun Li, Wenxin Shao, Haichao Zhang, Wei Xu, and Qiang Liu. Solving motion planning tasks with a scalable generative model. In _European Conference on Computer Vision (ECCV)_ . Springer, 2024. 

- [18] Zhiyu Huang, Peter Karkus, Boris Ivanovic, Yuxiao Chen, Marco Pavone, and Chen Lv. Dtpp: Differentiable joint conditional prediction and cost evaluation for tree policy planning in autonomous driving. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024. 

- [19] Zhiyu Huang, Zixu Zhang, Ameya Vaidya, Yuxiao Chen, Chen Lv, and Jaime Fernández Fisac. Versatile scene-consistent traffic scenario generation as optimization with diffusion. _arXiv preprint arXiv:2404.02524_ , 2024. 

- [20] Maximilian Igl, Punit Shah, Paul Mougin, Sirish Srinivasan, Tarun Gupta, Brandyn White, Kyriacos Shiarlis, and Shimon Whiteson. Hierarchical imitation learning for stochastic environments. In _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2023. 

- [21] Chiyu Jiang, Andre Cornman, Cheolho Park, Benjamin Sapp, Yin Zhou, Dragomir Anguelov, et al. Motiondiffuser: Controllable multi-agent motion prediction using diffusion. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2023. 

- [22] Max Jiang, Yijing Bai, Andre Cornman, Christopher Davis, Xiukun Huang, Hong Jeon, Sakshum Kulshrestha, John Lambert, Shuangyu Li, Xuanyu Zhou, et al. Scenediffuser: Efficient and controllable driving simulation initialization and rollout. _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 

- [23] Napat Karnchanachari, Dimitris Geromichalos, Kok Seang Tan, Nanxiang Li, Christopher Eriksen, Shakiba Yaghoubi, Noushin Mehdipour, Gianmarco Bernasconi, Whye Kit Fong, Yiluan Guo, et al. Towards learning-based planning: The nuplan benchmark for real-world autonomous driving. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024. 

- [24] Lingdong Kong, Wesley Yang, Jianbiao Mei, Youquan Liu, Ao Liang, Dekai Zhu, Dongyue Lu, Wei Yin, Xiaotao Hu, Mingkai Jia, et al. 3d and 4d world modeling: A survey. _arXiv preprint arXiv:2509.07996_ , 2025. 

- [25] Alex Kulesza and Ben Taskar. Determinantal point processes for machine learning. _Foundations and Trends® in Machine Learning_ , 2012. 

- [26] Bernard Lange, Jiachen Li, and Mykel J Kochenderfer. Scene informer: Anchor-based occlusion inference and trajectory prediction in partially observable environments. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024. 

- [27] Bohan Li, Xin Jin, Hu Zhu, Hongsi Liu, Ruikai Li, Jiazhe Guo, Kaiwen Cai, Chao Ma, Yueming Jin, Hao Zhao, et al. Scaling up occupancy-centric driving scene generation: Dataset and method. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2026. 

- [28] Qifeng Li, Xiaosong Jia, Shaobo Wang, and Junchi Yan. Think2drive: Efficient reinforcement learning by thinking with latent world model for autonomous driving (in carla-v2). In _European conference on computer vision_ . Springer, 2024. 

- [29] Shihao Li, Naisheng Ye, Tianyu Li, Kashyap Chitta, Tuo An, Peng Su, Boyang Wang, Haiou Liu, Chen Lv, and Hongyang Li. Optimization-guided diffusion for interactive scene generation. In _European Conference on Computer Vision (ECCV)_ . Springer, 2026. 

- [30] Tianran Liu, Shengwen Zhao, and Nicholas Rhinehart. Towards foundational lidar world models with efficient latent flow matching, 2025. URL https://arxiv.org/abs/2506.23434. 

- [31] Xingchao Liu, Chengyue Gong, and Qiang Liu. Flow straight and fast: Learning to generate and transfer data with rectified flow. _arXiv preprint arXiv:2209.03003_ , 2022. 

- [32] Jack Lu, Kelvin Wong, Chris Zhang, Simon Suo, and Raquel Urtasun. Scenecontrol: Diffusion for controllable traffic scene generation. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024. 

- [33] Chen Min, Dawei Zhao, Liang Xiao, Yiming Nie, and Bin Dai. Uniworld: Autonomous driving pre-training via world models. _arXiv preprint arXiv:2308.07234_ , 2023. 

- [34] Chen Min, Dawei Zhao, Liang Xiao, Jian Zhao, Xinli Xu, Zheng Zhu, Lei Jin, Jianshu Li, Yulan Guo, Junliang Xing, et al. Driveworld: 4d pre-trained scene understanding via world models for autonomous driving. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 15522–15533, 2024. 

- [35] Mashrur M Morshed and Vishnu Boddeti. Diverseflow: Sample-efficient diverse mode coverage in flows. In _Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)_ , 2025. 

11 

- [36] Jiquan Ngiam, Benjamin Caine, Vijay Vasudevan, Zhengdong Zhang, Hao-Tien Lewis Chiang, Jeffrey Ling, Rebecca Roelofs, Alex Bewley, Chenxi Liu, Ashish Venugopal, et al. Scene transformer: A unified architecture for predicting multiple agent trajectories. _arXiv preprint arXiv:2106.08417_ , 2021. 

- [37] Minting Pan, Xiangming Zhu, Yunbo Wang, and Xiaokang Yang. Iso-dream: Isolating and leveraging noncontrollable visual dynamics in world models. _Advances in neural information processing systems_ , 2022. 

- [38] Muleilan Pei, Shaoshuai Shi, and Shaojie Shen. Advancing multi-agent traffic simulation via r1-style reinforcement fine-tuning. In _International Conference on Learning Representations (ICLR)_ , 2026. 

- [39] Zhenghao Peng, Yuxin Liu, and Bolei Zhou. Scenestreamer: Continuous scenario generation as next token group prediction. In _International Conference on Learning Representations (ICLR)_ , 2026. 

- [40] Jonah Philion, Xue Bin Peng, and Sanja Fidler. Trajeglish: Traffic modeling as next-token prediction. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- [41] Ethan Pronovost, Meghana Reddy Ganesina, Noureldin Hendy, Zeyu Wang, Andres Morales, Kai Wang, and Nick Roy. Scenario diffusion: Controllable driving scenario generation with diffusion. _Advances in Neural Information Processing Systems_ , 2023. 

- [42] Tianwen Qian, Jingjing Chen, Linhai Zhuo, Yang Jiao, and Yu-Gang Jiang. Nuscenes-qa: A multi-modal visual question answering benchmark for autonomous driving scenario. In _Proceedings of the AAAI conference on artificial intelligence_ , 2024. 

- [43] Lloyd Russell, Anthony Hu, Lorenzo Bertoni, George Fedoseev, Jamie Shotton, Elahe Arani, and Gianluca Corrado. Gaia-2: A controllable multi-view generative world model for autonomous driving. _arXiv preprint arXiv:2503.20523_ , 2025. 

- [44] Shaoshuai Shi, Li Jiang, Dengxin Dai, and Bernt Schiele. Mtr++: Multi-agent motion prediction with symmetric scene modeling and guided intention querying. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2024. 

- [45] Pei Sun, Henrik Kretzschmar, Xerxes Dotiwalla, Aurelien Chouard, Vijaysai Patnaik, Paul Tsui, James Guo, Yin Zhou, Yuning Chai, Benjamin Caine, et al. Scalability in perception for autonomous driving: Waymo open dataset. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition (CVPR)_ , 2020. 

- [46] Simon Suo, Sebastian Regalado, Sergio Casas, and Raquel Urtasun. Trafficsim: Learning to simulate realistic multi-agent behaviors. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2021. 

- [47] Xiaoyu Tian, Tao Jiang, Longfei Yun, Yucheng Mao, Huitong Yang, Yue Wang, Yilun Wang, and Hang Zhao. Occ3d: A large-scale 3d occupancy prediction benchmark for autonomous driving. _Advances in Neural Information Processing Systems (NeurIPS)_ , 2023. 

- [48] Mingyi Wang, Jingke Wang, Tengju Ye, Junbo Chen, and Kaicheng Yu. Do llm modules generalize? a study on motion generation for autonomous driving. _Conference on Robot Learning (CoRL)_ , 2025. 

- [49] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Jiagang Zhu, and Jiwen Lu. Drivedreamer: Towards realworld-drive world models for autonomous driving. In _European conference on computer vision_ . Springer, 2024. 

- [50] Yuqi Wang, Jiawei He, Lue Fan, Hongxin Li, Yuntao Chen, and Zhaoxiang Zhang. Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 

- [51] Xinshuo Weng, Jianren Wang, Sergey Levine, Kris Kitani, and Nicholas Rhinehart. Inverting the pose forecasting pipeline with spf2: Sequential pointcloud forecasting for sequential pose forecasting. In _Conference on Robot Learning (CoRL)_ , 2021. 

- [52] Xinshuo Weng, Jiayuan Nan, K-H Lee, Rowan McAllister, Adrien Gaidon, Nicholas Rhinehart, and Kris M Kitani. S2net: Stochastic sequential pointcloud forecasting. In _European Conference on Computer Vision (ECCV)_ , 2022. 

- [53] Wei Wu, Xiaoxin Feng, Ziyan Gao, and Yuheng Kan. Smart: Scalable multi-agent real-time motion generation via next-token prediction. _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 

- [54] Danfei Xu, Yuxiao Chen, Boris Ivanovic, and Marco Pavone. Bits: Bi-level imitation for traffic simulation. _arXiv preprint arXiv:2208.12403_ , 2022. 

- [55] Jiazhi Yang, Shenyuan Gao, Yihang Qiu, Li Chen, Tianyu Li, Bo Dai, Kashyap Chitta, Penghao Wu, Jia Zeng, Ping Luo, et al. Generalized predictive model for autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 

12 

- [56] Zetong Yang, Li Chen, Yanan Sun, and Hongyang Li. Visual point cloud forecasting enables scalable autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024. 

- [57] Lunjun Zhang, Yuwen Xiong, Ze Yang, Sergio Casas, Rui Hu, and Raquel Urtasun. Copilot4d: Learning unsupervised world models for autonomous driving via discrete diffusion. _arXiv preprint arXiv:2311.01017_ , 2023. 

- [58] Zhejun Zhang, Peter Karkus, Maximilian Igl, Wenhao Ding, Yuxiao Chen, Boris Ivanovic, and Marco Pavone. Closedloop supervised fine-tuning of tokenized traffic models. In _Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)_ , 2025. 

- [59] Zhiyuan Zhang, Xiaosong Jia, Guanyu Chen, Qifeng Li, and Junchi Yan. Trajtok: What makes for a good trajectory tokenizer in behavior generation? In _International Conference on Learning Representations (ICLR)_ , 2026. 

- [60] Wenzhao Zheng, Weiliang Chen, Yuanhui Huang, Borui Zhang, Yueqi Duan, and Jiwen Lu. Occworld: Learning a 3d occupancy world model for autonomous driving. In _European conference on computer vision_ . Springer, 2024. 

- [61] Ziyuan Zhong, Davis Rempe, Yuxiao Chen, Boris Ivanovic, Yulong Cao, Danfei Xu, Marco Pavone, and Baishakhi Ray. Language-guided traffic simulation via scene-level diffusion. In _Conference on robot learning (CoRL)_ , 2023. 

- [62] Ziyuan Zhong, Davis Rempe, Danfei Xu, Yuxiao Chen, Sushant Veer, Tong Che, Baishakhi Ray, and Marco Pavone. Guided conditional diffusion for controllable traffic simulation. In _2023 IEEE international conference on robotics and automation (ICRA)_ . IEEE, 2023. 

- [63] Yunsong Zhou, Naisheng Ye, William Ljungbergh, Tianyu Li, Jiazhi Yang, Zetong Yang, Hongzi Zhu, Christoffer Petersson, and Hongyang Li. Decoupled diffusion sparks adaptive scene generation. In _2025 IEEE/CVF International Conference on Computer Vision (ICCV)_ . IEEE, 2025. 

- [64] Zikang Zhou, Jianping Wang, Yung-Hui Li, and Yu-Kai Huang. Query-centric trajectory prediction. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2023. 

- [65] Zikang Zhou, HU Haibo, Xinhong Chen, Jianping Wang, Nan Guan, Kui Wu, Yung-Hui Li, Yu-Kai Huang, and Chun Jason Xue. Behaviorgpt: Smart agent simulation for autonomous driving with next-patch prediction. _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 

- [66] Zheng Zhu, Xiaofeng Wang, Wangbo Zhao, Chen Min, Bohan Li, Nianchen Deng, Min Dou, Yuqi Wang, Botian Shi, Kai Wang, et al. Is sora a world simulator? a comprehensive survey on general world models and beyond. _arXiv preprint arXiv:2405.03520_ , 2024. 

13 

## **Appendix** 

|**A**<br>**The  l**|**AutoWorld Workflow**|**15**|
|---|---|---|
|A.1|Training . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . .<br>15|
|A.2|Inference<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . .<br>16|
|**B**<br>**Add**|**itional Experiments**|**16**|
|B.1|Effect of Coarse-to-Fine Predictive Scene Context<br>. . . . . . . . . . . . . . . . . . . .|. . . . .<br>16|
|B.2|Effect of Budget Allocation between World Model and Motion Generation.<br>. . . . . .|. . . . .<br>16|
|B.3|Multimodal Behavior Coverage<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . .<br>17|
|**C**<br>**Imp**|**lementation Details**|**20**|
|C.1|Scene Encoder<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . .<br>21|
|C.2|World Model<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . .<br>21|
|C.3|Motion Generation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . .<br>21|
|C.4|Cascaded Latent Diversity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . .<br>22|
|C.5|AutoWorld’s Notations<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . .<br>22|


14 

### **A The AutoWorld Workflow** 

Algorithms 1 and 2 summarize AutoWorld’s training and inference procedures. 

|**Algo **|**rithm 1** AutoWorld Training|**Algorithm 2** AutoWorld Inference|
|---|---|---|
|1: **In**<br>|**put:**<br>|1: **Input:** initial scene(_Ot−Th_:_t, St−Th_:_t, V_),<br>|
|2: unl<br>|abeled data_Dµ_=_{_(_Ot−Th_:_t_+_Tf_ )_i}_<sup>_Nµ_</sup><br>_i_=1<br>|VAE encoder_E_, world model_µθ_,<br>motion model_fψ_|
|lab<br>VA|eled data_Df_ =_{_(_Ot−Th_:_t, St−Th_:_t_+_Tf , V_)_i}_<sup>_Nf_</sup><br>_i_=1<br>E encoder_E_, world model_µθ_|<br>2: **Output:** (_N × M_)simulated rollouts Sen<br>3: **Required:** sample counts(_N × M_)|
|mo|tion model_fψ_ with projections_ϕ_1_, ϕ_2||
|3: **O**<br>|**utput:** trained parameters_θ, ψ_<br>|4: _Zt−Th_:_t ←E_(Voxelize(_Ot−Th_:_t_))|
|4: **Re**|**quired:** hyperparameters_λ,_∆_, δ_|5: condition_c_<sup>_µ _</sup>_←{Zt−Th_:_t, τ_ <sup>ego</sup><br>_t−Th_:_t_<sup>_}_</sup>|
|5: _D_<br>|<sup>_′_</sup><br>_µ_ <sup>=</sup> <sup>_{Yt−T_</sup>_h_<sup>:</sup><sup>_t_+</sup><sup>_T_</sup>_f_ <sup>= Vox(</sup><sup>_Ot−T_</sup>_h_<sup>:</sup><sup>_t_+</sup><sup>_T_</sup>_f_ <sup>)</sup><sup>_}_</sup>|// Determinantal Point Process (DPP)-|
|6: _D_<br>|<sup>_′′_</sup><br>_µ_ <sup>=</sup> <sup>_{Zt−T_</sup>_h_<sup>:</sup><sup>_t_+</sup><sup>_T_</sup>_f_ <sup>=</sup> <sup>_E_(</sup><sup>_Yt−T_</sup>_h_<sup>:</sup><sup>_t_+</sup><sup>_T_</sup>_f_ <sup>)</sup><sup>_}_</sup>|guided world-model sampling<br>6: **for**_i_ = 1_, . . . , N_ **do**<br>|
|//<br>|**(a)**Initialize motion-aware weight maps<br> <sup>_′_</sup><br>|7:<br>_z_<sup>(</sup><sup>_i_)</sup><br>_Kµ _<sup>_∼N_ (0</sup><sup>_, I_)</sup>|
|7: **fo**<br>|**r**_Yt−Th_:_t_+_Tf ∈D_<br>_µ_ <sup>**do**</sup><br>|8: **for**_k_ = _K . . ._1**do**|
|8:|**for**_t ∈_[_t −Th_ : _t_+_Tf_]**do**|_µ_ _µ,    ,_<br>9<br><sup>_q,_world</sup><br><sup>(</sup><sup>_i_)</sup><br><sup>_N_</sup><br>|
|9:|˜_Yt←t_+∆_←Yt_|:<br>_P_<br>_kµ_<br>_←_DPP(_{z_<br>_kµ_<sup>_}_</sup><br>_i_=1<sup>)</sup><br><br>|
|10:<br>11:|¯<br>_Ct,_∆_←_Transition(_Yt_+∆_,_ <sup>˜</sup>_Yt←t_+∆)<br>_Wt ←_1 +_λ_ <sup>¯</sup><br>_Ct,_∆|10:<br>**for**_i_ = 1_, . . . , N_ **do**<br>11:<br>_z_<sup>(</sup><sup>_i_)</sup><br>_kµ−_1 <sup>_←µθ_(</sup><sup>_z_(</sup><sup>_i_)</sup><br>_kµ_<sup>_, kµ, cµ_)</sup><sup>_−_</sup><br><br> <sup>_q_world</sup>|
|//|**(b)**World modeling (WM)|_γµ_(_kµ_)_∇_<br>_z_<sup>(</sup><sup>_i_)</sup><br>_kµ_<br>log_P_<sup>_,_</sup><br>_kµ_|
|12: **f**<br>|**or**_Zt−Th_:_t_+_Tf ∈D_<sup>_′′_</sup><br>_µ_ <sup>**do**</sup><br>|12:<br>ˆ<br>_Z_<sup>(</sup><sup>_i_)</sup><br>_t_+1:_t_+_Tf _<sup>_←z_(</sup><sup>_i_)</sup><br>0 <sup>_,_</sup><br>_i_ = 1_, . . . , N_|
|13:|Condition_c_<sup>_µ _</sup>_←{ZT τ_ <sup>ego</sup><br><sup>_}_</sup>||
||_t−h_:_t, _ <br>_t−Th_:_t_||
|14:|Target ˜_z ←Zt_+1:_t_+_T_|// cascaded latent sampling<br>|
||_f_<br>|13: **for**_i_ = 1_. . .  N_ **do**|
|15:<br>16:|Sampling_z_0 _∼N_(0_, I_)_, kµ ∼U_(0_,_1)<br>Interpolation_zkµ ←_(1_−kµ_)_z_0 +_kµ_˜_z_<br>// motion-aware latent supervision|_,    ,_<br>14:<br>_g_<sup>(</sup><sup>_i_)</sup> _←_MHCA(_ϕ_1(_{_ˆ_z_<sup>(</sup><sup>_i_)</sup><br>_t_+_eδ_<sup>_}_</sup><br>_⌊Tf /δ⌋_<br>_e_=1<br>))<br>// per time-step condition<br>|
|17:|_L_<sup>_world_</sup>(_θ_) _←_<br><br>|15:<br>_c_<sup>_f_(</sup><sup>_i_)</sup><br>_t_<br>_←{_MHCA(_ϕ_2([ˆ_z_<sup>(</sup><sup>_i_)</sup><br>_t_<br>;_g_<sup>(</sup><sup>_i_)</sup>]))_}_<br>_t_+_Tf_<br>_t_=_t_+1|
||�<br>_i,j _<sup>_Wt_(</sup><sup>_i, j_)</sup><sup>_∥µθ_(</sup><sup>_zk_</sup>_µ_<sup>_, kµ, cµ_)</sup><sup>_i,j,_:</sup><br>|16:<br>**for**_j_ = 1_, . . . , M_ **do**<br>|
||_−_(˜_z −z_0)_i,j,_:_∥_<sup>2</sup><br>2<br> <sup>_world_</sup>|17:<br>_τ_ <sup>(</sup><sup>_i,j_)</sup><br>_Kf_<br>_∼N_(0_, I_)|
|18:|_θ ←_Update(_θ, ∇θL_)|18:<br>**for**_kf_ = _Kf , . . . ,_1**do**<br><br>|
|//<br>|**(c)**WM-conditioned motion generation<br>|19:<br>_P_<sup>_q,_motion</sup><br>_kf_<br>_←_DPP(_{τ_ <sup>(</sup><sup>_i,j_)</sup><br>_kf_<br>_}_<sup>_M_</sup><br>_j_=1<sup>)</sup>|
|19: **f**|**or**(_Ot−Th_:_t, St−Th_:_t_+_Tf , V_) _∈Df_ **do**|20:<br>**for**_j_ = 1_, . . . , M_ **do**|
|20:<br>|_Zt−Th_:_t ←E_(Vox(_Ot−Th_:_t_))<br><br>|21:<br>_τ_ <sup>(</sup><sup>_i,j_)</sup><br>_kf −_1 <sup>_←fψ_(</sup><sup>_τ_ (</sup><sup>_i,j_)</sup><br>_kf_<br>_, kf , c_<sup>_f_(</sup><sup>_i_)</sup><br>_t_<br>)_−_|
|21:<br>|Condition_c_<sup>_µ _</sup>_←{Zt−Th_:_t, τ_ <sup>ego</sup><br>_t−Th_:_t_<sup>_}_</sup><br>// sample one future occupancy rollout<br>ˆ|<br><br>_γf_(_kf_)_∇_<br>_τ_<sup>(</sup><sup>_i,j_)</sup><br>_kf_<br>log_P_<sup>_q,_motion</sup><br>_kf_|
|22:|_Zt_+1:_t_+_Tf ←µθ_(_·, c_<sup>_µ_</sup>)|22:<br>ˆ_τ_ <sup>(</sup><sup>_i,j_)</sup><br>_t_+1:_t_+_T _<sup>_←τ_ (</sup><sup>_i,j_)</sup><br>0<br>_,_<br>_i_ = 1_, . . . , N,_|
|23:|_g ←_MHCA(_ϕ_1(_{_ˆ_zt_+_eδ}_<br>[_Tf /δ_]<br>_e_=1<br>))<br>// per-time-step condition<br>|_f _<br><br>_j_ = 1_, . . . , M_|
|24:|_c_<sup>_f_</sup><br>_t _<sup>_←{_MHCA(</sup><sup>_ϕ_2([ˆ</sup><sup>_zt_;</sup><sup>_g_]))</sup><sup>_}_</sup><br>_t_+_Tf_<br>_t_=_t_+1<br>||
|25:|_L_<sup>_motion_</sup>(_ψ_) _←_DiffLoss(_fψ_(_·, c_<sup>_f_</sup><br>_t_ <sup>))</sup><br>||
|26:|_ψ ←_Update(_ψ, ∇ψL_<sup>_motion_</sup>)||


#### **A.1 Training** 

Algorithm 1 begins by voxelizing LiDAR sequences and encoding them into latent occupancies using the VAE encoder (L5–6). (a) Motion-aware weight maps are then computed (L7–11) by compensating for ego motion and measuring occupancy transitions. These weights emphasize dynamic regions and are used to reweight the world-model supervision. (b) The world model is trained to predict future latent occupancies (L12–18). Given past latents and the ego past trajectory, a noisy latent state is constructed by interpolating between Gaussian noise and the target latent sequence. The model learns a velocity field that matches the displacement between the noise and the target under the motion-aware weighted loss. (c) The WM-conditioned motion generator is trained using labeled trajectory data (L19–26). For each scene, the world model produces a single future occupancy rollout (L22). These predicted occupancies are aggregated to form the predictive scene context (L23) and combined with per-timestep latents to form conditioning signals for the diffusion model (L24). The motion model is optimized using the standard diffusion loss. Training therefore uses one world-model rollout and one trajectory sample per scene, _without any diversity mechanism_ . 

15 

#### **A.2 Inference** 

Algorithm 2 generates diverse simulations by introducing DPP-guided sampling at inference time. After encoding the observed LiDAR history (L4), the world model produces multiple latent scene rollouts (L6–11). Sampling begins from Gaussian noise and is iteratively refined. At each step, a quality-weighted DPP objective is computed across the current samples. The gradient of the log determinant introduces a repulsive force between samples, encouraging diversity while preserving high quality predictions. This process yields _N_ diverse future scene rollouts _Z_<sup>ˆ</sup> _t_<sup>(</sup> +1:<sup>_i_)</sup> _t_ + _Tf_<sup>(L12).Given these scene forecasts, the motion model generates trajectories using cascaded</sup> latent sampling (L13–21). For each predicted latent occupancy sequence, a global context embedding _g_<sup>(</sup><sup>_i_)</sup> is computed (L14) and combined with timestep latents to form the diffusion conditioning signals (L15). The diffusion process then generates _M_ trajectories per scene rollout. As in the world model, DPP guidance is applied during sampling to encourage trajectory diversity while maintaining consistency with the predicted scene dynamics. The final set of _N × M_ trajectories corresponds to _N × M_ diverse and plausible driving scenarios (L22). 

### **B Additional Experiments** 

#### **B.1 Effect of Coarse-to-Fine Predictive Scene Context** 

We study the effect of coarse-to-fine guidance from the world model in a controlled setting. To isolate this component, we disable DPP and use IID sampling at both stages. We compare a variant that conditions only on future latent occupancies with one that additionally incorporates the predictive scene context. As shown in Table 6, adding the predictive scene context improves both realism and trajectory accuracy, increasing RMM from 0 _._ 7562 to 0 _._ 7618 and reducing minADE from 1 _._ 4519 to 1 _._ 4334. This suggests that aggregating future latents into a global context provides useful long-horizon structure for multi-agent coordination, whereas per-step latents alone offer only local guidance. Overall, the predictive scene context serves as a coarse-to-fine signal that improves the quality of generated traffic scenarios. 

**Table 6 Effect of coarse-to-fine predictive scene context on traffic simulation.** We compare conditioning on future latent occupancies alone versus combining them with a predictive scene context, under a fixed sampling budget with IID sampling. Incorporating the predictive scene context improves overall realism. 

|**Conditioning**|**RMM**(_↑_)|**minADE**(_↓_)|
|---|---|---|
|Future latent only|0.7562|1.4519|
|+ Pred. scene context|**0.7618**|**1.4334**|


#### **B.2 Effect of Budget Allocation between World Model and Motion Generation.** 

Table 7 studies how a fixed budget of 32 rollouts is allocated between world-model hypotheses ( _N_ ) and motion samples per hypothesis ( _M_ ). The baseline refers to AutoWorld’s diffusion motion generator without world-model grounding. The same baseline is also used as the trajectory-only variant in Sec. 4.3 of the main paper. The results show that adding world-model grounding improves over this baseline across all budget allocations, but the allocation matters: using only one scene hypothesis (1 _×_ 32) limits future-scene diversity, while using too few motion samples per hypothesis (32 _×_ 1) weakens behavioral realism. Performance is highest with the balanced 8 _×_ 4 allocation, suggesting that allocating budget to both world-model hypotheses and motion samples is more effective than concentrating it on either stage alone. With cascaded latent sampling, 4 _×_ 8 achieves the best performance, improving RMM to 0.7746 and substantially reducing minADE. This indicates that once scene hypotheses are selected diversely, allocating more samples to motion generation better exploits the rollout budget. For fair comparison, all ablations in Sec. 4.4 of the main paper use a fixed 4 _×_ 8 allocation, corresponding to the best-performing configuration under a budget of 32 rollouts. 

16 

**Table 7 Effect of budget allocation between world model and motion generation.** _N_ and _M_ denote the numbers of world-model hypotheses and motion samples per hypothesis, respectively. Allocating the full budget to either world-model hypotheses or motion samples hurts realism, while a balanced allocation achieves the best overall performance. The “<sup>_†_</sup> ” denotes the model used for leaderboard submission. 

|**Model**|**_N_**_×_**_M_**|**RMM**|**Kinematic**|**Interactive**|**Map-based**|**minADE**|
|---|---|---|---|---|---|---|
|Baseline|-_×_32|0.7472|0.4749|0.7741|0.8682|1.4892|
||1_×_32|0.7610|0.4849|0.7855|0.8873|1.4369|
|+ Wld dl di|4_×_8|0.7597|0.4840|0.7839|0.8861|1.4256|
|or moe grounng|8_×_4|0.7618|0.4846|0.7876|0.8870|1.4334|
||32_×_1|0.7523|0.4796|0.7728|0.8819|1.4178|
|_Full AutoWorld (Cascaded Diver_<br>Cdd L Sli|_sity; only_<br>4_×_8<sup>_†_</sup>|_meaningf_<br>0.7746|_ul when N >_ <br>0.4878|1_and M >_1_)_<br>0.7968|0.9099|1.3102|
|+ ascae atent ampng|8_×_4|0.7728|0.4889|0.7948|0.9067|1.3097|


#### **B.3 Multimodal Behavior Coverage** 

We also qualitatively illustrate AutoWorld’s multimodal behaviors by visualizing the generated trajectories alongside the _SDC paths_ provided in the Waymo dataset [9]<sup>1</sup> . The self-driving car (SDC) refers to the ego vehicle in each Waymo scenario. The SDC paths annotation provides a set of candidate route polylines representing plausible future routes the ego vehicle could follow according to the road topology, such as lane following, turning, or merging behaviors. Since these paths are geometric route hypotheses rather than time-aligned trajectories, they often extend beyond the 8-second forecasting horizon used in motion prediction. For visualization, we therefore first retain only single continuous path segments and truncate each path to a comparable horizon based on the future distance traveled by the ground-truth SDC. To avoid displaying many nearly identical routes that arise from map discretization, the truncated paths are further deduplicated by resampling them to a fixed number of points and removing paths whose mean pointwise distance falls below a similarity threshold. This process yields a compact set of distinct route hypotheses that represent the primary topological futures available to the ego in the scene. 

Figure 7 visualizes the ground-truth SDC trajectory, the resulting candidate SDC paths, and 32 predicted ego rollouts generated by AutoWorld. For visualization, SDC paths are loaded using the procedure described in the official Waymax tutorial<sup>2</sup> . Across scenarios, AutoWorld demonstrates meaningful multimodal coverage, producing diverse behaviors such as alternative turning directions and lane changes within a single scene, capturing both topological and kinematic diversity. While most candidate routes are covered, a few SDC paths corresponding to more complex topological traversals remain uncovered. We view this as an opportunity for future work, where incorporating explicit road-topology reasoning into the sampling process may enable better coverage of such complex routes over longer horizons. 

> 1Waymo Open Motion Dataset: v1.3.1 

> 2Official Waymax tutorial 

17 

**Figure 7 Qualitative analysis of multimodal behavior coverage** . The ground-truth ego trajectory, candidate SDC paths from Waymo, and 32 rollouts generated by AutoWorld are visualized (left to right). The model produces diverse behaviors within a single scenario, including alternative turning directions and lane changes, with diversity that also reflects different kinematic profiles. 


18 


19 


### **C Implementation Details** 

In this section, we describe the implementation details of the main components of AutoWorld. 

20 

#### **C.1 Scene Encoder** 

The scene encoder processes three inputs derived from the problem formulation: the agent history _St−Th_ : _t ∈_ R<sup>_A×_(</sup><sup>_Th_+1)</sup><sup>_×da_</sup> , the HD map _V ∈_ R<sup>_v×dv_</sup> , and the traffic light states _R ∈_ R<sup>_r×dr_</sup> . In our implementation, we use _A_ = 32 agents, _v_ = _vlvp_ map vector points corresponding to _vl_ = 256 polylines each containing _vp_ = 30 sampled waypoints, and _r_ = 16 traffic lights. The agent history is encoded using a shared GRU, producing agent embeddings of shape [ _A, D_ ], which are combined with agent-type embeddings. The map representation _V_ is organized into polylines and encoded using a PointNet-like polyline encoder: each waypoint is processed by a shared MLP to produce features of dimension _D_ , followed by max pooling along the waypoint dimension to obtain polyline-level features of shape [ _vl, D_ ]. The resulting agent, map, and traffic-light embeddings are concatenated to form the initial scene representation of shape [ _A_ + _vl_ + _r, D_ ]. To model interactions among scene elements, we apply six query-centric Transformer layers following [44]. This architecture encodes relationships between agents, map polylines, and traffic lights using relative positional features while preserving the element-centric representation of each token. The encoder outputs a final scene representation of shape [ _A_ + _vl_ + _r, D_ ], with _D_ = 256. 

#### **C.2 World Model** 

We build the latent occupancy world model on top of the LiDAR-based framework of [30]. Raw LiDAR point clouds are first voxelized into non-semantic occupancy grids with voxel size _v_ = [0 _._ 4 _,_ 0 _._ 4 _,_ 0 _._ 4] meters within spatial range [ _−_ 40 _, −_ 40 _, −_ 1 _,_ 40 _,_ 40 _,_ 5 _._ 4]. This results in occupancy volumes of size ( _Ho, Wo, Do_ ) = (200 _,_ 200 _,_ 16), producing binary occupancy tensors _Yt ∈{_ 0 _,_ 1 _}_<sup>_Ho×Wo×Do_</sup> with corresponding validity masks _Mt_ , following [47]. We employ a Swin Transformer-based VAE [30] to encode voxel occupancies into spatial latent representations _Zt ∈_ R<sup>_H×W ×C_</sup> . The VAE is trained for 100 epochs with batch size 16 on the voxelized occupancy data. The latent representation has spatial size _H × W × C_ = 16 _×_ 16 _×_ 50. 

For latent occupancy forecasting, we follow the rectified flow matching architecture of [30]. The world model predicts future latent occupancies _Z_<sup>ˆ</sup> _t_ +1: _t_ + _Tf ∈_ R<sup>_Tf ×H×W ×C_</sup> conditioned on past latent context _c_<sup>_µ_</sup> = _{Zt−Th_ : _t, τt_<sup>ego</sup> _−Th_ : _t_<sup>_}_.Here,</sup><sup>_Zt−T_</sup> _h_<sup>:</sup><sup>_t_denotes the latent occupancy history and</sup><sup>_τ_ego</sup> _t−Th_ : _t_<sup>represents the ego trajectory</sup> over the same horizon. The ego trajectory is encoded using the same trajectory encoder employed for agent history in the scene encoder. The encoded trajectory is concatenated with the latent history features and projected through an MLP to produce the final conditioning representation. The temporal horizons _Th_ and _Tf_ are shared with the motion generation model. 

The rectified flow model operates on latent sequences _zt, z_ 0 _,_ ˜ _z ∈_ R<sup>_Tf ×H×W ×C_</sup> , where _z_ 0 _∼N_ (0 _, I_ ) and _z_ ˜ denotes the ground-truth future latent occupancy sequence. The flow model is first trained for 100 epochs with batch size 8 using the standard rectified flow objective. Training then continues for an additional 50 epochs using the proposed motion-aware latent supervision objective, where the motion-aware loss weight is empirically set to _λ_ = 0 _._ 2. Following [30], we maintain an exponential moving average (EMA) of model parameters with decay rate 0 _._ 9999 to stabilize training. We also employ classifier-free guidance by randomly dropping the conditional input _c_<sup>_µ_</sup> with probability 0.25. 

#### **C.3 Motion Generation** 

Given a sampled world-model rollout _Z_<sup>ˆ</sup> _t_ +1: _t_ + _Tf_ , we flatten each latent into _HW_ spatial tokens and project them into the denoiser embedding space of dimension _D_ . We then build the predictive scene context _g ∈_ R<sup>1</sup><sup>_×D_</sup> using temporal subsampling at 1 Hz (i.e., stride _δ_ = 10 frames). For each future step, we concatenate the corresponding latent occupancy and the predictive scene context along the token dimension. These tokens are fused with the scene encoding through cross-attention to produce a refined step-wise conditioning representation _c_<sup>_f_</sup> _t_ +1: _Tf_<sup>, matching the shape of the scene encoding and used to condition the diffusion denoiser.The denoising</sup> network consists of two decoding blocks, each composed of two Transformer decoder layers. Within each block, self-attention models the joint distribution of multi-agent future trajectories while enforcing temporal causality through a causal mask [18] that prevents information leakage from future timesteps. Cross-attention layers condition the trajectory tokens on the world-model-guided context _c_<sup>_f_</sup> _t_ +1: _Tf_<sup>, allowing the predicted actions to</sup> remain consistent with both the observed scene history and the predicted scene evolution. The decoder outputs clean actions _τ_ ˆ0 _∈_ R<sup>_A×Tf ×_2</sup> . These actions are then integrated using a unicycle dynamics model to obtain the 

21 

corresponding future agent states ( _x, y, v, θ_ ) over the horizon. We set the number of diffusion timesteps to _Kf_ = 50. 

#### **C.4 Cascaded Latent Diversity** 

We use time-dependent scaling coefficients _γµ_ ( _kµ_ ) and _γf_ ( _kf_ ) to control the strength of the diversity gradients during sampling in the world model and motion generation stages, respectively. These coefficients follow the diffusion and flow-matching timestep schedules and are normalized by the norm of the corresponding DPP gradients to ensure stable updates. When _γ_ ( _·_ ) = 0, the procedure reduces to standard IID sampling. When _γ_ ( _·_ ) _>_ 0, the DPP gradient encourages diversity by pushing similar samples apart. If the generated samples are already sufficiently diverse, the DPP gradient becomes negligible, and the process naturally behaves like IID sampling. 

As stated in the main paper, we evaluate the plausibility of generated trajectories using the violation metrics provided by the Waymax simulation platform [13]. Specifically, we consider the kinematic infeasibility (kin.), collision (col), off-road (off.), and wrong-way metrics (wro.). To obtain a single scalar score for use in DPP-based sampling, we combine these metrics using weights inspired by the Realism Meta-Metric (RMM), which aggregates kinematic, interactive, and map-based realism as RMM = 0 _._ 20 (kinematic) + 0 _._ 45 (interactive) + 0 _._ 35 (map-based). Following this structure, we compute the trajectory quality score as _Q_ = 1 _−_ (0 _._ 20 (kin.) + 0 _._ 45 (col.) + 0 _._ 35<sup><u>of.f+</u></sup> 2<sup><u>wro.</u></sup> ). The weights reflect the relative importance of kinematic feasibility, interaction safety, and adherence to map constraints. This scalar score is used as the quality term in the DPP kernel, encouraging the selection of trajectories that are physically feasible, collision-free, and consistent with the road geometry. 

#### **C.5 AutoWorld’s Notations** 

For clarity, the key notations used throughout the method are summarized in Table 9. 

**Table 9** Main notations used in AutoWorld. For functions, “Domain” refers to the domain of the function’s output. 

|**Notation**|**Name / Description**|**Domain**|
|---|---|---|
|Scene encoder<br>|||
|_A_|Number of agents<br>|N<br>|
|_vl_|Number of map polylines<br>|N<br>|
|_vp_|Number of sampled waypoints per polyline<br>|N<br>|
|_v_|Total number of map vector points (_v_ = _vlvp_)<br>fi|N<br>|
|_r_<br>|Number of traffic lights<br>|N|
|_da_|Agent state dimension|N|
|_dv_|Map feature dimension<br>fi|N|
|_dr_|Traffic-light feature dimension|N<br>|
|_V_|HD map vector representation|R<sup>_v×dv_</sup><br>|
|_R_<br>|Traffic light states<br>|R<sup>_r×dr_</sup><br>|
|_s_<sup>_i_</sup><br>_t_|State of agent_i_at time_t_|R<sup>4</sup><br>|
|_st_|Joint agent states|R<sup>_A×_4</sup><br>|
|_St−Th_:_t_|Agent state history|R<sup>_A×_(</sup><sup>_Th_+1)</sup><sup>_×_4</sup><br>|
|_h_|Scene encoding output|R<sup>(</sup><sup>_A_+</sup><sup>_vl_+</sup><sup>_r_)</sup><sup>_×D_</sup>|
|_D_|Scene embedding dimension|N|
|World model|||
|_t_|Discrete scene timestep|N|
|_Th_<br>|History horizon<br>|N<br>|
|_Tf_|Future prediction horizon|N<br>|
|_Yt_|Occupancy grid at time_t_|_{_0_,_1_}_<sup>_Ho×Wo×Do_</sup><br>|
|_Mt_<br>˜|Validity mask|_{_0_,_1_}_<sup>_Ho×Wo×Do_</sup><br>|
|_Yt→t_+∆<br>|Ego-motion compensated occupancy grid<br>|_{_0_,_1_}_<sup>_Ho×Wo×Do_</sup><br>|
|_Ct,_∆(_v_)<br>¯|Voxel occupancy transition indicator|{0,1}<br>|
|_Ct,_∆|Downsampled motion map|R<sup>_H×W_</sup><br>|
|_Wt_<br>|Motion-aware latent weight map<br>fi|R<sup>_H×W_</sup><br>|
|_λ_|Motion emphasis coefficient|R_>_0<br>|
|_Zt_|Latent occupancy representation at time_t_|R<sup>_H×W ×C_</sup><br>|
|_Zt−Th_:_t_|Latent occupancy history|R<sup>(</sup><sup>_Th_+1)</sup><sup>_×H×W ×C_</sup><br>|
|_Zt_+1:_t_+_Tf_|Ground-truth future latent occupancies|R<sup>_Tf ×H×W ×C_</sup>|
|ˆ<br>_Zt_+1:_t_+_Tf_|Predicted future latent occupancies|R<sup>_Tf ×H×W ×C_</sup><br>|
|_z_0|Gaussian prior latent sequence sample|R<sup>_Tf ×H×W ×C_</sup><br>|
|_zkµ_|Latent variable at rectified-flow step_kµ_|R<sup>_Tf ×H×W ×C_</sup>|
|||Continued on next page|


22 

|**Notation**|**Name / Description**|**Domain**|
|---|---|---|
|_µθ_(_·_)|World-model velocity field network|R<sup>_Tf ×H×W ×C_</sup>|
|_kµ_|Rectified-flow timestep|N|
|Motion generation<br>|||
|_a_<sup>_i_</sup><br>_t_|Agent action (acceleration, yaw rate)|R<sup>2</sup><br>|
|_at_|Joint agent actions|R<sup>_A×_2</sup><br>|
|_τ_0|Clean future trajectory (action sequence)|R<sup>_A×Tf ×_2</sup><br>|
|_τkf_|Noisy trajectory during diffusion step_kf_|R<sup>_A×Tf ×_2</sup><br>|
|_g_|Predictive scene context|R<sup>1</sup><sup>_×D_</sup>|
|_δ_|Temporal subsampling stride|N<br>|
|_ξ_|Learned pooling query token|R<sup>1</sup><sup>_×D_</sup><br>|
|_ϕ_1(_·_)|Latent projection for context pooling|R<br>_Dϕ_1_×_1<br>|
|_ϕ_2(_·_)<br>|Conditioning projection|R<br>_Dϕ_2_×_1<br>|
|_c_<sup>_f_</sup><br>_t_<br>|Diffusion conditioning representation at timestep_t_|R<sup>(</sup><sup>_A_+</sup><sup>_vl_+</sup><sup>_r_)</sup><sup>_×D_</sup><br>|
|_c_<sup>_f_</sup>|Full diffusion conditioning sequence|R<sup>_Tf ×_(</sup><sup>_A_+</sup><sup>_vl_+</sup><sup>_r_)</sup><sup>_×D_</sup><br>|
|_fψ_(_·_)<br>Σ_kf_|Diffusion denoiser network<br>Diffusion variance schedule|R<sup>_A×Tf ×_2</sup><br>_M⪰_0|
|_kf_|Diffusion timestep|N|
|Cascaded latent sampling|||
|_X_|Candidate sample set|_{_ˆ_x_<sup>(</sup><sup>_i_)</sup>_}_<sup>_Ks_</sup><br>_i_=1|
|ˆ_x_<sup>(</sup><sup>_i_)</sup>|Candidate sample representation|R<sup>_d_</sup>|
|_Ks_|Number of samples in DPP set|N|
|_κ_(_·, ·_)|Similarity kernel|R<br>|
|Λ|Kernel matrix|R<sup>_Ks×Ks_</sup>|
|_P_<sup>_q_</sup><br>_κ_<sup>(</sup><sup>_X_)</sup><br>|Quality-aware DPP diversity probability|[0,1]|
|_q_<sup>(</sup><sup>_i_)</sup>|Quality weight for sample_i_|R|
|Λ<sup>_q_</sup><br>|Quality-aware kernel matrix|R<sup>_Ks×Ks_</sup>|
|_X_ <sup>world</sup> <sup>_._</sup>=_{_ <sup>ˆ</sup><br>_Z_<sup>(</sup><sup>_i_)</sup><br>_t_+1:_t_+_Tf _<sup>_}N_</sup><br>_i_=1|World-model rollout set|R<sup>_N×Tf ×H×W ×C_</sup>|
|<br>_γµ_(_kµ_)|World-model diversity guidance strength|R_>_0|
|_N_|Number of sampled world-model rollouts|N<br>|
|_X_ <sup>motion</sup> <sup>_._</sup>= _{τ_ <sup>(</sup><sup>_i,j_)</sup>_}_<sup>_M_</sup><br>_j_=1|Motion trajectory sample set|R<sup>_M×A×Tf ×_2</sup>|
|_γf_(_kf_)|Motion diversity guidance strength|R_>_0|
|_M_|Number of motion samples per rollout|N|


23 

