---
title: "OccSim: Multi-kilometer Simulation with Long-horizon Occupancy World Models"
date: "2026-03-30"
authors: "Tianran Liu; Shengwen Zhao; Mozhgan Pourkeshavarz; Weican Li; Nicholas Rhinehart"
url: https://arxiv.org/abs/2603.28887
pdf: https://arxiv.org/pdf/2603.28887
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.28887)** / [論文ページ](https://arxiv.org/abs/2603.28887)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **OccSim: Multi-kilometer Simulation with Long-horizon Occupancy World Models** 

**Tianran Liu**<sup>_⋆_</sup> , **Shengwen Zhao** , **Mozhgan Pourkeshavarz** , **Weican Li** , **Nicholas Rhinehart**<sup>_†_</sup> Learning, Embodied Autonomy, and Forecasting (LEAF) Lab, University of Toronto 

Data-driven autonomous driving simulation has long been constrained by its heavy reliance on prerecorded driving logs or spatial priors, such as HD maps. This fundamental dependency severely limits scalability, restricting open-ended generation capabilities to the finite scale of existing collected datasets. To break this bottleneck, we present OccSim, the first 3D occupancy world model driven simulator that requires neither HD maps nor log-derived layouts. OccSim obviates the requirement for continuous logs or HD maps; conditioned only on a single initial frame and a sequence of future ego-actions. It can stably generate over 3000 continuous frames, an _>_ 80 _×_ improvement in stable generation length over previous SoTA occupancy world models, and fuses them into maps spanning over 9 kilometers. Further qualitative stress tests show that it can roll out beyond 110K frames. OccSim is powered by two modules: W-DiT based static occupancy world model and the Layout Generator. W-DiT handles the ultra-long-horizon generation of static environments by explicitly introducing known rigid transformations in architecture design, while the Layout Generator populates the dynamic foreground with reactive agents based on the synthesized road topology. With these designs, OccSim can synthesize massive, diverse simulation streams. Extensive experiments demonstrate its downstream utility: data collected directly from OccSim can pre-train 4D semantic occupancy forecasting models to achieve up to 67% zero-shot performance on unseen data, outperforming previous asset-based simulator by 11%. When the collected data is scaled up to 5 _×_ its original size, zero-shot performance increases to 74%. 


**Project Website: https://orbis36.github.io/OccSim/** 


## **1 Introduction** 

Simulation is indispensable for the advancement of Level 4 autonomous driving systems [3, 6, 7]. Existing work basically obtain these simulation environments in one of two ways, and both are capped by human effort: Replay of recorded data provides authentic data streams, it inherently lacks reactive responses to ego behaviors. In contrast, geometry-based simulators (e.g., CARLA[8]), despite supporting interactivity, suffer from a significant sim-to-real gap regarding sensor realism and content diversity [41, 42]. This creates a fundamental trade-off: current approaches are often forced to compromise between realism, diversity, and interactivity. Although emerging data-driven simulations [37, 46] promise to overcome this dilemma, they remain conditioned on HD maps or BEV layouts, so the set of environments they can produce is still bounded by the coverage of annotated maps rather than by the model itself. 

Specifically, we argue that a comprehensive and scalable data-driven simulator must satisfy the following desiderata: 1. **Sensor realism & semantic richness** : The simulator should not only approximate the distribution of real-world sensor data (high-fidelity sensor realism) to provide diverse testbed, but also should inherently generate dense semantic labels, eliminating the reliance on manual annotation. 2. **Controllable & plausible agents** : infer initial traffic states from the environment rather than replaying logs, and expose agent control as a replaceable interface accepting anything from microscopic heuristics to learned forecasters. 3. **Global spatial persistence** : The simulator should maintain global spatial persistence, overcoming the “memoryless visual 

> _∗_ : Contact: tianran.liu@mail.utoronto.ca. 

> _†_ : Project Manager. 

1 


**Figure 1** Comparison of OccSim and workflow. Given a single frame and a sequence of future actions, the proposed W-DiT builds a multi-kilometer consistent occupancy map for autonomous driving simulation, without HD maps or driving logs at inference time. The agent initial poses are generated via the layout generator and then forward-simulated. OccSim is compatible with multi-agent forward simulation methods as plug-and-play modules; in our experiments, we use an IDM variant [16]. 

hallucination” prevalent in standard generative models. During long-horizon driving, static elements (e.g., road topology, buildings) must preserve strict spatiotemporal consistency. For instance, when the ego-vehicle completes a loop and revisits a previously observed location, the static environment must remain structurally identical. 4. **Log-independent Simulation** : The simulator’s operation should not be overly-constrained by pre-recorded driving logs. Ideally, it possesses the capability for open-ended generation in novel, unseen scenarios in order to overcome the scale limitations of collected data. 

In this paper, we aim to address the overarching question: _“How can we construct a data-driven generative simulator that efficiently satisfies these desiderata?”_ To this end, we present **OccSim** . To the best of our knowledge, OccSim is the first system to drive driving simulation from an occupancy world model, generating multi-kilometer, globally consistent environments without any HD map or BEV layout as input. As illustrated in Figure 1, it satisfies the above desiderata by conditioning solely on a single static frame and a sequence of future ego-actions, while being trained entirely on publicly-available data. 

Specifically, we adopt a decoupling strategy for static and dynamic voxels, modelling simulation as two synergistic generative tasks: a multi-kilometer rollout of the world model that assembles the large-scale static scene, and the conditional generation of dynamic traffic flow within it. These two tasks are also decoupled in time: the static world is generated once and then frozen, whereas agents are controlled online on top of it. For static world generation, the core difficulty is sustaining stable, high-quality and diverse output over long horizons. Prior work lacks this stability: given future actions, SOTA occupancy world models [19, 28] can only stably generate fewer than 50 frames (Fig. 5), while outpainting-based methods need human-labelled HD-Map [21] or trade stability for diversity [17]: their fidelity degrades sharply after certain times of rollouts and the resulting maps remain topologically fragmented (Fig. 15). 

Such a horizon suffices for vehicle control decisions, but not for large-scale map construction (e.g., multiple city blocks, _≥_ 2km<sup>2</sup> ) or long distance task simulation: at a 2Hz sampling rate with roughly 3 meters of ego motion per frame, 20–50 frames span only about 60–150m, far short of real street scale. 

We attribute this short rollout horizon to the architecture of current stochastic 4D occupancy world models, 

2 

which largely inherit their design from video generation: multiple 3D occupancy latents are stacked along the temporal dimension, and features are then aggregated by DiTs over both temporal and spatial dimensions [11, 23]. This paradigm ignores the geometric rigidity of 3D space and forces the network to hallucinate viewpoint changes implicitly, even though most of the observed region at t+1 is related to t by a known rigid transformation. What could be supplied as an exact geometric prior is instead left to be learned, so the residual error is re-injected at every step and compounds over autoregressive rollout until the scene collapses. 

Based on this observation, we propose “W-DiT”, the first occupancy world model capable of diverse, at least 3k-step rollouts of diverse static maps under complex trajectories (tested with over 3,000 frames generated, >80 _×_ improvement in stable rollout length). The core mechanism of W-DiT is a pipeline designed for effective conditioning on the previous frame: W-DiT explicitly utilizes 3D geometric priors through the proposed Maskinjected Conditioning mechanism. Beyond these, we also provide an SNR-weighted occupancy perception loss further supervises the prediction in decoded occupancy space, which we find necessary to keep rollout quality stable over thousands of frames. Orthogonally, we show that a norm-invariant spherical semantic readout in the occupancy VAE reshapes the latent manifold in a way that any occupancy world model can benefit from. 

Single-frame outputs are then consolidated into a persistent static map: we design a keyframe-based fusion scheme and a graph-search-based lane topology extraction algorithm, yielding a large-scale road network that agents can drive on. Populating it without historical logs requires a generative treatment of traffic layout. Rather than placing agents by hand-tuned spawning rules, we train a layout generator based on latent flow matching to produce initial traffic states conditioned on the local road structure; agent motion is then rolled out by a replaceable control module, for which we use a 2D-IDM variant. The inference logic of OccSim is shown in Fig. 1: generate the large-scale static occupancy, fuse them into a large map, extract lanes graph, sample an ego position within it, then populate and control all agents. 

1. **A simulation pipeline that requires no logs or maps as input.** We propose a new pipeline for datadriven occupancy-based simulation: an occupancy world model generates the large-scale static scene, a layout generator infers initial agent states directly from the generated semantic occupancy, and agent motion is produced by a replaceable control module, instantiated here with a 2D-IDM variant, and compatible with any modern trajectory forecasting model. 

2. **An occupancy world model stable over ultra-long horizons.** Using the same training data, our W- DiT-based backbone optimized with the proposed objective achieves a stable rollout length over **80** _×_ longer than before. This makes W-DiT, to our knowledge, the first model to roll out over **3,000 frames** of static occupancy and form complex road topologies without relying on HD maps in any form. Under user-steered trajectories, further stress tests qualitatively show stable and diverse rollout beyond **110K frames** (Fig. 16), building a 100km+ city-scale occupancy map. 

3. **An evaluation protocol for log-free environment generation.** Beyond the logged horizon no paired ground truth exists, and each individual metric admits a trivial optimum. We therefore report fidelity, diversity and road-network connectivity jointly at matched spatial scales, reference them against an explicit collapse baseline, and ground them in the sim-to-real transfer of a downstream forecasting task, an external judge the generator cannot optimise against. Under this protocol, forecasting models trained purely on OccSim data reach 67% of in-domain IoU (vs. 60% for CARLA). These numbers increase to 74% on the 5 _×_ data scale, 22.1% better than CARLA. 

## **2 Related Work** 

### **2.1 Long horizon RGB world models** 

Driven by the abundance of data resources, numerous efforts to construct world models for autonomous driving have utilized RGB signals as their primary input to achieve robust long-horizon rollouts. For instance, GAIA-1 [14] employs a multi-modal transformer architecture with language and action conditioning to autoregressively generate minute-long video clips. GAIA-2 [27] extended this capability to multi-view RGB generation by transitioning the underlying backbone from a deterministic model to flow matching. Furthermore, CosmosDrive-Dreams [25] finetuning the Cosmos [1] foundation model to enhance the roll out of autonomous driving 

3 

scene generation. In the indoor navigation task, Ego2Memory [43] explicitly uses VLM to map 2D features with Frontier Map for long-term persistent rollout. 

By introducing a two-stage training and fine-tuning pipeline alongside better utilization of dynamic priors, Vista [10] significantly improves the resolution and realism of generated videos, as evidenced by FID and FVD metrics. Subsequently, DrivingWorld [15] adopted a purely auto-regressive (AR) based approach. More recently, Epona [42] provided the first open-source implementation for long video rollouts, utilizing an AR diffusion method. This AR-plus-diffusion paradigm has since been extended to unified world models that jointly perform understanding, planning, and generation within a single VLM backbone [36, 47]. 

### **2.2 Occupancy World Models in Autonomous Driving** 

While RGB images offer rich semantic features, accurately capturing and predicting the complex 3D geometry and physical depth of dynamic environments remains a significant challenge. Consequently, there is a growing trend towards developing world models based on 3D occupancy representations, which are typically derived from voxelized and densified LiDAR data. 

Earlier works such as OccWorld [45] and Occllama [34] addressed this by combining discrete encoding techniques (e.g., VQ-VAE [31]) with deterministic auto-regressive (AR) transformer architectures, with Occllama further incorporating Large Language Models (LLMs) to enhance scene comprehension. Currently, generative modeling approaches have gained significant traction. For instance, DOME [11] utilizes a continuous VAE alongside a high-performance diffusion model, enabling fine-grained controllability. Recent advancements have further extended these capabilities: COME [28] introduces a post-trained ControlNet [44] approach, DynamicCity [2] leverages hex-plane decomposition, and OccFM [20] employs a Flow Matching-based multiscale DiT [24] architecture. Expanding the scope, UniScene [18] explores a conditional pipeline that uses BEV layouts to generate comprehensive multi-sensor data, ranging from RGB images to LiDAR point clouds. 

### **2.3 Data driven simulation with generative models** 

High-fidelity simulation is crucial for bridging the sim-to-real gap in autonomous driving, yet conventional physics-based simulators like CARLA [8] often struggle with domain discrepancies. Recent research has shifted towards data-driven approaches to leverage large-scale real-world datasets. Nocturne [32] facilitates highefficiency simulation by replaying trajectories from the Waymo dataset. Building upon this, SLEDGE [5] and Scenario Dreamer[26] extends simulation to synthesized scenarios by generatively modeling road layouts and vehicle agents. In parallel, efforts have been made to generate more realistic sensory observations. ReSim [38] and DriveArena [39] utilize video generation techniques and HD maps to render high-resolution RGB observations for closed-loop policy evaluation. 

The raising of 3D Gaussian Splatting rendering in unbounded scene [4, 35, 46] allow us reconstruct static backgrounds more realistic. While, the SemCity[17] and InifiCube[21] follow the out-painting solution introduced by Repainting[22] while combine it with tri-plane decomposition diffusion. Most recently, X-scene [40] advances the field by proposing an external diffusion module that generates BEV layouts from natural language prompts, thus mitigating dependency on recorded driving logs. 

## **3 Long-horizon static Occupancy World Models** 

OccSim organizes simulation into two loops on different timescales. The _generation loop_ runs once per environment: W-DiT rolls out static occupancy along a given trajectory, and the frames are fused into a single global map, which is then frozen. The _simulation loop_ runs every timestep on top of it: the ego and all background agents re-plan online from their instantaneous neighbourhood states, querying the static environment rather than regenerating it. 

Next, we will introduce the W-DiT architecture and its corresponding optimization methods in Section 3.1, which form the foundation of our infinite-horizon static scene generation. In Section 3.2, we briefly describe how to merge single-frame static scenes generated by W-DiT and infinitely extend them into loop closing 

4 


**Figure 2** Illustration of structure to generate road map of _t_ +1 from condition at timestep t. Here, _t_ represents the sequence frame index, and _τ_ denotes the probability flow timestep. This token-wise scale and shift condition injection method allows precise control of the rigid transformation during long-horizon generation. _I_ ( _·_ ) stands for rasterization process of given future trajectory _Jt_<sup>_t_</sup> +1<sup>+</sup><sup>_n_.Thelatentrepresentations</sup><sup>_zt_and</sup><sup>_zt_+1(</sup><sup>_∈_R</sup><sup>_H×W ×Cz_)atbottomrightcornerarevisualizedas</sup> decoded BEV occupancy maps for intuitive illustration. 

city-scale environments. Furthermore, in Section 3.3, we will demonstrate how to learn the possible distribution of agents layout from data and incorporate them into the scene to interact with test ego vehicle. 

### **3.1 Long-horizon stable generation with W-DiT** 

We find that a geometry-aware alternative to the standard 2+1D aggregation yields substantial improvements in long-term stability. Formally, using an occupancy VAE [20] (consisting of spatial compressor _E_ and decoder _D_ ), we can map the occupancy frames _Ot, Ot_ +1 to their respective latent representations **z** _t,_ **z** _t_ +1 _∈_ R<sup>_H×W ×Cz_</sup> , where _t_ denotes time index. Our aim is to model the joint predictive distribution over an extended future horizon: given an initial latent state **z** 0 and a sequence of future ego-trajectories _J_ 0: _K_ + _σ_ , our goal is to auto-regressively estimate: 


where _K_ is the forecast horizon and _K_ + _σ_ the trajectory length. For _K ≥_ 10<sup>2</sup> , the per-step residual of a learned re-projection compounds into structural drift. The W-DiT block (Fig. 2) instead conditions each step on a deterministic rigid transformation derived from _J_ , warping the latent so that only the newly revealed region is generated. Specifically, assuming planar motion on the _XY_ -plane (zero vertical velocity and roll/pitch), the inter-frame transformation is **T**<sup>_t_</sup> _t_<sup>+1</sup> = exp( _ξ_<sup>�</sup> _t_ ∆ _t_ ), where _ξ_<sup>�</sup> _t ∈_ R<sup>4</sup><sup>_×_4</sup> is the matrix form of the twist induced by the action _at_ = [ _vx,t, vy,t, ωt_ ]<sup>_⊤_</sup> , with planar velocity **v** = [ _vx,t, vy,t,_ 0]<sup>_⊤_</sup> and yaw rate **_ω_** = [0 _,_ 0 _, ωt_ ]<sup>_⊤_</sup> . 

Applying **T**<sup>_t_</sup> _t_<sup>+1</sup> , we forward-warp **z** _t_ to the viewpoint at _t_ + 1, obtaining ˆ **z** _t_ +1. Ego motion inevitably pushes some spatial regions out of the field of view or into occlusion, so we deterministically compute a binary visibility mask **M** vis _∈{_ 0 _,_ 1 _}_<sup>_H×W_</sup> from the known geometry alone. However, the inter-frame displacement is small (3–4 m at ∆ _t_ = 0 _._ 5 s), so **M** vis alone leaves the task nearly degenerate: the model can satisfy it by copying the input, which hinders robust representation learning. Following MAE [12], we therefore add a random 

5 

mask **M** rand _∼B_ (1 _− p_ ) with masking ratio _p_ , and condition on **z** ˜ _t_ +1 = ( **M** vis _⊙_ **M** rand) _⊙_ **z** ˆ _t_ +1, where _⊙_ is the Hadamard product and the spatial masks broadcast across _Cz_ . Next, instead of fusing the future action into _τ_ directly [11, 28], we rasterize it into a spatial signal aligned with index _t_ + 1. We represent the future actions as physical waypoints _Pt_ = _{pt_ + _i ∈_ R<sup>2</sup> _}_<sup>_σ_</sup> _i_ =1<sup>on the BEV plane, anchored in the ego frame at</sup><sup>_t_+ 1 by</sup> cumulatively applying **T**<sup>_t_</sup> _t_<sup>+</sup> +1<sup>_σ_.Connectingthemyieldsapolylinetracingtheintendedpathontothefuture</sup> road surface, which we rasterize to _lt_ +1 _∈{_ 0 _,_ 1 _}_<sup>_H×W ×_1</sup> (denoted _I_ ( _·_ ) in Fig. 2). Since warping introduces interpolation error, we concatenate _lt_ +1 with ˜ **z** _t_ +1 and refine them with a U-Net before injection, yielding the conditioning tokens _f_<sup>ˆ</sup> _t_ +1 _∈_ R<sup>_B×N×Cw_</sup> with _N_ = _H × W_ . We then inject _f_<sup>ˆ</sup> _t_ +1 by token-wise scaling and shifting. Global scale, shift and gate are regressed from the flow timestep _τ_ as in DiT, while a token-wise projection regresses a spatial control signal from _f_<sup>ˆ</sup> _t_ +1 (dual-head injection hereafter); the two are summed per token: 


and analogously for _β_<sup>(</sup><sup>_i_)</sup> _, α_<sup>(</sup><sup>_i_)</sup> . On the main stream, **z**<sup>_τ_</sup> _t_ +1<sup>= (1</sup><sup>_−τ_)</sup><sup>_ϵ_+</sup><sup>_τ_</sup><sup>**z**</sup><sup>_t_+1is tokenized to</sup><sup>_ft_+1</sup><sup>_∈_R</sup><sup>_B×N×Cw_, and</sup> the MHSA block becomes _ft_<sup>_′_</sup> +1<sup>=</sup><sup>_ft_+1+</sup><sup>_α_1</sup><sup>_⊙_MHSA(</sup><sup>_γ_1</sup><sup>_⊙_LN(</sup><sup>_ft_+1)+</sup><sup>_β_1), where</sup><sup>_γ_1= [</sup><sup>_γ_(1)</sup><sup>_, . . . , γ_(</sup><sup>_N_)]</sup><sup>_⊤∈_R</sup><sup>_N×Cw_</sup> stacks the token-wise parameters, with _β_ 1 _, α_ 1 defined analogously and the same scheme applied in the subsequent MLP layer. Each W-DiT block therefore modulates every spatial token by its own warped condition, and the network outputs the instantaneous velocity field _vθ_ ( **z**<sup>_τ_</sup> _t_ +1<sup>_, τ, c_), where</sup><sup>_c_denotes all conditions.</sup> 

Following the success of flow models in high-quality generation with few sampling steps [29, 42], we optimize W-DiT with a velocity regression objective. This objective is sound but not sufficient for long-horizon rollout: supervising only in the continuous latent space leaves errors that are small in latent norm yet consequential once decoded, which will be re-injected at every autoregressive step. Empirically, models trained with the velocity loss alone match the full objective on the first generated frame but degrade within 10 rollout frames (Tab. 3). 

We therefore introduce an SNR-scaled perception loss. Our insight is to exploit the discrete, semantic nature of 3D occupancy: rather than confining supervision to the continuous latent manifold, we project the denoised prediction back into occupancy space, redirecting gradient pressure (from CE loss) onto the directions the decoder is sensitive to and anchoring it to a target that does not drift with the latent. The overall objective is 


where **M** mask = **M** vis _⊙_ **M** rand, _λ_ balances the two terms, and ˆ **z** _t_ +1 = **z**<sup>_τ_</sup> _t_ +1<sup>+ (1</sup><sup>_−τ_)</sup><sup>_vθ_is the one-step denoised</sup> latent recovered from the current velocity field without sampling, decoded by the frozen VAE _D_ for a maskregion-only cross-entropy against _Ot_ +1. Crucially, the _τ_<sup>2</sup> weighting concentrates this supervision in the low-noise regime, where the one-step reconstruction is close enough to the target for the cross-entropy to carry usable geometric signal. We ablate the usage of perception loss and SNR weight in rows 4 and 5 of Tab. 3. 

### **3.2 Multi-kilometer road map fusion from single frames** 

As detailed in Sec. 3.1, our W-DiT is capable of stably rolling out thousands of static map frames. While the stochastic nature of flow models effectively bypasses the data scarcity bottleneck of traditional HD maps, the generated outputs remain discrete, ego-centric local scenes. Furthermore, naive fusion strategies, such as temporal averaging, tend to aggressively over-smooth crucial high-frequency details during sequence aggregation, because of the temporal inconsistency in the forecasted frames. 

Our strategy consists of two components: key-frame based fusion and branch road detection: We first propose a two-pass keyframe-based fusion heuristic (detailed in Alg. 2 in Appendix 9). Given local occupancy predictions and their global poses, we first aggregate a minimally overlapping keyframe subset to establish a sharp foundational map _M_ global. Subsequently, after a gravity alignment step, the redundant non-keyframes are used to robustly inpaint spatial gaps via threshold-based voting and morphological cleaning. 

To enable unbounded map expansion, we systematically identify valid extensible frontiers within _M_ global. By applying morphological skeletonization to the road manifold, we extract a topological graph to isolate 

6 


**Figure 3 Agent initialization within generated static maps.** Each panel displays a 200x200 voxel crop centered on the (unrendered) ego-vehicle from _M_ global. The first two panels show distinct generated scenes, the third and fourth panels demonstrate the model’s multimodality: two different plausible layouts generated for the same revisited location. Orange vehicles (second panel) are stationary. 

candidate branch points (Alg. 3 in Appendix 9). A Dual-Probing Filtering mechanism—comprising topological and 3D semantic probes—is then employed to reject collision-prone directions. By selecting two valid disjoint endpoints and connecting them via a collision-free spline, we prompt W-DiT to autoregressively synthesize the missing intermediate occupancy. This autoregressive bridging paradigm closes the loop, enabling the unbounded, procedural generation of diverse autonomous driving scenarios from a single prompt occupancy. 

### **3.3 Agent generation and control on top of static road map** 

Having constructed the city-scale static map _M_ global (with explicit lane graphs extracted via Alg. 4), we next populate the environment with plausible initial agent states. Unlike log-replay methods, our topologies are procedurally generated, necessitating a generative approach for traffic layouts. 

Formally, our objective is to model the conditional probability distribution of the agent layout given 1 frame of static environment: _P_ ( _A|_ **z** _t_ ), where _A_ = _{_ ( _xi, yi, si_ ) _}_<sup>_N_</sup> _i_ =1<sup>denotes the set of vehicle centers (</sup><sup>_xi, yi_) motion</sup> states _si ∈{_ dynamic _,_ static _}_ and **z** static is cropped from a previously fused large map given a random pose. To make this distribution tractable for our flow-based generative framework, we map the discrete set _A_ into a continuous 2D spatial heatmap _H_ , encoding static and dynamic vehicles as positive and negative standard Gaussian kernels, respectively. Then we train a compact Diffusion Transformer (DiT-S) to learn the continuous distribution _P_ ( _H|_ **z** _t_ ). To prevent the DiT-S from overfitting and memorizing small-scale dataset layouts, we apply multiple spatial augmentations during training (detailed in Appendix) 

During inference, the sampled heatmap _H_ is discretized via Non-Maximum Suppression (NMS) to extract individual vehicle instances. Each vehicle is then projected onto the nearest lane to establish a kinematically feasible initial yaw. In figure 3, we visualize several samples after add the agents to their initial pose. Finally, we employ A* routing and the extended 2D Intelligent Driver Model (2D-IDM) [16] to roll out microscopic kinematic trajectories toward randomly selected junctions in _M_ global (Alg. 6 in Appendix 9). While we utilize classic heuristics to validate simulation feasibility, our initialized map topology and agent poses guarantee plug-and-play compatibility with any modern learning-based trajectory forecasting model. 

## **4 Experiment** 

We organized our experiments to answer the following 3 questions: Q1. **Static Realism & Stability** : Can the proposed W-DiT structure generate highly realistic and spatiotemporally consistent static environments, especially over extended horizons? Q2. **Generation Diversity** : Does OccSim exhibit sufficient multimodality and diversity in long-horizon rollout? Q3. **Dynamic Fidelity & Downstream Utility** : Can OccSim be used to train temporal-based tasks like 4D semantic occupancy forecasting more effectively than data collected from CARLA? 

7 

### **4.1 Metrics Protocol Design** 

No single metric suffices to evaluate log-free generation: beyond the logged horizon no paired ground truth exists, so realism can only be measured against the marginal distribution, which a model repeatedly emitting one plausible scene would satisfy , while diversity scores are themselves inflated by structural breakdown. We therefore report fidelity, diversity and road-network connectivity jointly, reference them against an explicit collapse baseline, and ground the protocol in an external downstream task ( **Q3** ) that the generator cannot optimise against. 

Specifically, to answer **Q1** , we assess its performance across two primary dimensions: the realism of the generated static environments and the dynamic fidelity of the traffic simulation. Following previous works [2, 40], we evaluate static realism via 2D/3D-FID, KID, and MMD (denoted by Dis below). 

To formalize realism, we define two evaluation settings to measure the performance of model under different context: **1. Conditional fidelity** : Dis � _Pθ_ ( _O_<sup>ˆ</sup> _t|O_ 0 _, J_ ) _, Pdata_ ( _Ot|O_ 0 _, J_ )�. This evaluates the structural accuracy at each specific time index _t ∈{_ 1 _, . . . , K}_ ( _K_ equal to the length of GT sequence) under the strict constraint of the initial observation _O_ 0 and ego-trajectory _J_ . **2. Unconditional realism** : Dis � _Pθ_ ( _O_<sup>ˆ</sup> _t|O_ 0 _, J_ ) _, Pdata_ ( _O_ )�, where t depend on the rollout length _K_ . Although the generation inherently relies on the initial observation _O_ 0 and trajectory **J** , long-horizon rollouts can reasonably diverge into various valid structures. Therefore, instead of comparing against the strictly paired future frame, we measure the distance between the conditionally generated samples at time _t_ and the global marginal distribution of the entire ground truth training set _O_ . This ensures long-term rollouts universally reside on the valid data manifold. 

In **Q2** , we introduce the Vendi score [9] and Semantic IoU diverse score. Specifically, the Semantic IoU diverse score evaluates structural divergence in the decoded semantic space by calculating the complement of the average Intersection over Union across multiple stochastic rollouts generated from the same initial scene. Meanwhile, the Vendi score operates in the latent feature space—extracted via a pretrained encoder—to quantify the effective sample size of the generated distributions. These metrics reflect the model’s multimodality, where higher scores indicate a richer variety of plausible future layouts, demonstrating the simulator’s capability to model environmental uncertainty. 

To address **Q3** , we evaluate the dynamic simulation performance through a zero-shot transfer setting. To the best of our knowledge, we are the first to demonstrate the downstream utility of a data-driven simulator by evaluating its pre-training efficacy on the 4D semantic occupancy forecasting task. Specifically, we utilize continuous data streams collected directly from the ego-vehicle’s perspective within our generated simulation. Performance on this downstream task serves as a proxy, directly reflecting the simulator’s capability to faithfully emulate complex, real-world traffic dynamics. 

Regarding datasets, we utilize Occ3D-nuScenes [30] for all static generation realism comparisons to ensure fairness in training data volume. For the remaining experiments, we employ UniOcc-Waymo [33] or UniOccnuScenes due to their unified voxel categorization. Additional simulation metrics and training/implementation details are provided in Appendix 6.4. 

### **4.2 Main results comparisons** 

We first evaluate the realism and stability of the generated static road maps. In Fig. 4, we compare our results with previous occupancy world models in terms of both conditional fidelity and unconditional realism. For a comprehensive analysis, our evaluations are conducted across two distinct VAE latent spaces (derived from UniScene [18] and OccFM [20]). As illustrated in the figure, our method (shown in red) demonstrates superior long-term stability and structural realism, significantly outperforming baseline models that suffer from rapid error accumulation. Furthermore, due to the limited number of ground truth (GT) samples (fewer than 1000 per timestep _t_ ), we specifically selected unbiased metrics—namely KID and MMD with two different kernels—to assess conditional fidelity. Here, 1000 frames rollout generated conditioned on straight trajectory after GT’s, with constant velocity. 

This performance gap observed in the 3D occupancy metrics becomes even more pronounced when evaluating realism on the 2D plane. As illustrated in Fig. 5, to increase the rigor of our evaluation, we selected three 

8 


**Figure 4** Realism evaluation of generated 3D static occupancy. The left three columns report the conditional fidelity (MMD and KID) under a 30-frame constraint. The right two columns showcase the unconditional realism (KID and FID) over a 1000-frame long-horizon rollout. Our W-DiT-based method obtains the best long-horizon stability and conditional realism. 

distinct trajectories to compare our method against the previous state-of-the-art diffusion based occupancy world model, COME (details regarding the specific trajectory shapes are provided in Fig. 13 of the Appendix). Notably, even when evaluated on the most challenging curved and closed-loop trajectories, our approach still outperforms the previous state-of-the-art method’s results on simpler straight-line trajectories. 

Furthermore, to establish a lower-bound reference, we constructed a 1000-frame occupancy map collection to serve as a “chaos” baseline. This was achieved by randomly selecting structurally collapsed samples from the model’s output that lack coherent semantic information. Qualitatively, any metric score surpassing this baseline threshold indicates a completely unusable state. Visualizations of this chaotic baseline collection are available in Appendix 8.6. 

To evaluate the generation diversity over long-term rollouts, we analyze the Pairwise mIoU Diversity and Vendi Scores across first 100 timesteps, as illustrated in Fig. 6. Our proposed method consistently outperforms prior generative baselines. Notably, at early timesteps, our approach demonstrates a rapid increase in diversity, establishing a significant margin over both COME and DOME. As the autoregressive generation extends, our method maintains a high and stable level of diversity without performance degradation. In both OccFM and UniScenes latent spaces, our method achieves the highest Vendi Scores, indicating a richer variety of generated geometric and semantic structures. 

In Tab. 1, we further compare our world model based static occupancy generation method with previous out-painting based solution. Although temporal rollout introduces error accumulation that spatial outpainting does not face, W-DiT still surpasses all outpainting-based baselines in terms of both fidelity (FID) and diversity (Vendi Score), and the gap widens with distance. It is worth noting that both of the 10km spatial distance in Tab. 1 (about 3000 frames) in or 1000 temporal frames in Fig. 5 are the upper bound we can quantitatively 

9 


**Figure 5** Long-horizon 2D realism under varying trajectories. FID and KID comparisons for 2D projections of the 3D generated occupancy. We evaluate three ego-actions: straight, closed-loop, and continuous turning. The dashed reference line indicates the “chaos” threshold characterizing scene collapse. In all scenarios, our model (red) remains strictly below this threshold, vastly outperforming the previous SOTA model(which exceed the “chaos” threshold in 35/40-th frame generated) and ensuring long-term structural integrity regardless of the driving action. 


**Figure 6** Generation diversity comparison with previous occupancy world model. Pairwise mIoU diversity and Vendi scores evaluated over 100 timesteps using **10 random seeds** . Solid lines and shaded areas denote the mean and the 25th-75th percentiles, respectively. Our methods performed the best diversity in the rollout among all tested generative method. 

assess given the compute cost. However, we find that W-DiT consistently maintains stable generation quality on a scale of more than two orders of magnitude. In Sec. 8.4, we qualitatively present the **100km+ city scale occupancy generated from OccSim.** As far as we know, this is the largest scale tested in occupancy based driving scenario generation. 

To validate the practical utility of our generated world: we then use 4D semantic forecasting as a proxy task to show the downstream utility of using OccSim as data generator. For this experiment, we configure the model to unroll along a curved, closed-loop trajectory, expanding the generation horizon from 1,000 to 3,000 frames to construct a significantly larger map. Based on this extended map, we build the simulation environment utilizing the methodologies detailed in Sec. 3.2 and Sec. 3.3. As demonstrated in Tab. 2, even when relying on a relatively straightforward dynamics algorithm such as the 2D IDM to control agents, OccSim provides better training signals for simulating overall traffic flow and background dynamics than CARLA. Notably, models trained on data generated by OccSim achieve better performance compared to those trained on the CARLA simulator (Uni-C), showing an improvement of at least 14% relative in average mIoU across the two semantic forecasting models. When we collect 5x more data from UniOcc to train the downstream model, this gap further expands to 52%. In terms of 3s average IoU, our method reaches 67% and 72% of the upper-bound’s performance. Improvement can also be observed from the alignment of the intent of the human driver measured by the L2 distance. The same ordering holds for the open-loop planning L2 of OccWorld’s ego trajectory head, all using a non-learned IDM controller. Augmenting the full real Waymo logs with an extra 30% of OccSim 

10 

**Table 1** Diversity and fidelity comparison with other non-world-model occupancy generation methods across distances. SemCity and InfiniCubes extend map boundaries via unconditional / HD-Map-conditioned diffusion outpainting, where quality degrades with extrapolation distance. UniScene<sup>_†_</sup> requires a aligned per-frame HD-Map to generate occupancy and is thus distance-independent, we treat it as a performance upper bound; results of condition-free version also reported below. _⋆_ : SemCity’s released code does not support Occ3D, we reproduced results with public released code base. LCC: Largest connected components, measures the road-network completeness of the stitched map. All experiments are run under **5 different seeds** and 150 scenes then averaged. Details and visualization can be found in Appendix 6.1 and 8.3. 

|Model|Dataset|HD-Map?||2D-FID_↓_/ M    f|ean Vendi Score  f|at different ph|f ysical distance|_↑_|LCC. Ratio_↑_|
|---|---|---|---|---|---|---|---|---|---|
||||40m|400m|1km|2km|5km|10km||
|SemCity[17]<sup>_⋆_</sup>|d|✗|46.31/1.00|97.07/2.03|102.01/2.04|147.36/2.06|141.96/1.93|148.29/1.95|11_._7%|
|UniScene[18]<sup>_†_</sup>|Occ3-<br>NS|✓|||33.1|2/1.55|||–|
|UniScene[18]|ucenes|✗|||215.|59/3.82|||–|
|Ours||✗|36.48/1.24|50.00/2.05|50.89/2.22|46.40/2.27|48.60/2.29|47.13/2.35|92_._9%|


**Table 2** The performance of different semantic forecasting model trained with occupancy collected from UniOcc-Carla(UniC) or OccSim, test on UniOcc-NuScenes(Uni-N) validation set. mIOU measured over all background occupancy categories and car category for foreground. _†_ : We collected the same amount of data on OccSim as that provided by UniOcc for Carla for fairness. _⋆_ : Use _×_ 5 amount of data collected from OccSim to train downstream models. Stoch.: whether the model is stochastic. The gray-shaded rows represent the performance upper bound, as the models are trained and tested on the same domain without domain shift. We omit the L2 error for OccFM here as it’s future action conditioned. 

|Model|Train Data||mIoU|||IoU|||L2 (m)||IoUveh|Stoch.|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||1s|2s|3s|1s|2s|3s|1s|2s|3s|||
|OccWorld[45]|Uni-N|26.53|16.73|12.33|32.17|22.88|18.41|0.43|1.08|1.99|17.10|✗|
|OccWorld|Uni-C|11.79|8.35|6.75|18.31|14.09|12.03|0.72|2.31|4.05|6.58|✗|
|OccWorld<sup>_†_</sup>|OccSim|13.51|9.56|7.61|20.53|15.48|13.24|0.65|1.42|3.27|7.46|✗|
|OccWorld<sup>_⋆_</sup>|OccSim|19.54|12.31|9.08|23.87|16.92|13.47|0.61|1.38|2.91|12.41|✗|
|OccFM[20]|Uni-N|36.28|25.10|19.47|41.22|30.90|25.02|-|-|-|28.79|✓|
|OccFM|Uni-C|6.99|5.34|4.70|8.63|6.50|5.71|-|-|-|6.42|✓|
|OccFM<sup>_†_</sup>|OccSim|15.93|11.76|9.26|18.31|14.10|11.75|-|-|-|13.28|✓|
|OccFM<sup>_⋆_</sup>|OccSim|25.32|18.96|13.10|29.19|21.08|13.93|-|-|-|15.82|✓|


data improves the average 1–3s IoU by a further 7% relative (Sec. 7.5), showing OccSim also complements real data. 

### **4.3 Ablation study** 

In Tab. 3, we shows the three components are only effective jointly. Token-wise condition injection alone (row 3) does not stabilise the rollout and is in fact worse than the plain baseline at intermediate horizons; adding the perception loss on top of it (row 4) improves the 500-frame endpoint but still leaves quality degrading monotonically. Only when the perception loss is SNR-scaled (row 5) does the rollout become stable, halving the 500-frame FID relative to row 3 and keeping it within 12% of the first generated frame. This matches the role of the _τ_<sup>2</sup> weighting: it concentrates occupancy-space supervision in the low-noise regime, where the decoded prediction is close enough to the GT for the cross-entropy term to carry geometric signal. 

To evaluate agent motion realism under our log-free setting, following Scenario Dreamer [26], Tab. 4 reports the JSD between simulated and real agent motion, with a GT-vs-GT as an empirical lower bound. We decompose the remaining gap in three steps. Replacing real trajectories with IDM control on lane graphs extracted from GT occupancy (row 2) yields the largest increase. This step bundles two costs: the simplification of the IDM itself, and the representational cost of recovering topology from voxelized semantics rather than from a vectorized map; we analyze the latter in Sec. 7.2, where lane graphs extracted from GT semantic occupancy are compared against those rasterized from HD maps and the residual Chamfer discrepancy remains sub-voxel relative to the 0 _._ 4m grid. Substituting GT agent positions with our Layout Generator (row 3) adds a smaller increment, so initialization is a secondary error source. Most importantly, moving from real to generated 

11 

**Table 3** W-DiT design ablation, reported as the UniScene-AE 3D unconditional realism FID score at the _n_ -th generated frame. All three proposed components are essential for long-horizon stability. When not using dual-head injection, we adopt the classical spatiotemporal architecture in DOME. 

|Architecture|Percep.<br>Loss|Dual-head<br>injection|SNR<br>scaled|1st|5th|10th|30th|50th|100th|500th|
|---|---|---|---|---|---|---|---|---|---|---|
|Sil DiT|✗|✗|✗|663.89|712.56|789.91|1023.51|1281.99|1587.21|1612.40|
|patotempora|✓|✗|✓|661.79|710.63|801.11|1034.75|1342.72|1601.15|1607.97|
||✗|✓|✗|672.15|756.28|1013.12|1335.88|1295.42|1378.56|1526.95|
|W-DiT|✓|✓|✗|696.13|833.17|946.23|1306.21|1415.59|1427.66|1440.57|
||✓|✓|✓|665.23|630.34|645.96|687.90|698.87|712.65|744.71|


occupancy (row 4) changes the JSD only marginally across all four behaviour statistics, and is in fact lower on nearest-distance: our map topology is therefore not the limiting factor, and the remaining gap is dominated by the representation-and-controller stage, i.e. exactly the component our pipeline exposes as replaceable. 

Tab. 5 provide a collision rate v.s. simulation time analyze, and show that initialization from our Layout generator provide a more stable long horizon simulation results. Also in Tab. 6, we measure the time taken by OccSim components. Given a 1000-step action and initial frame, building a scene need encode the first frame, runs 1000 steps of W-DiT rollout, decodes the results, and heuristic to extract lanes (around 656s). During simulation, if the ego-vehicle is still in pre-computed area, the simulation latency is equal to IDM planning time (7.1ms), while after every 40m, frontal-view layout recomputation is required, which encodes the front area, generates a layout, and performs IDM-based planning (92.68ms). 

Furthermore, we report two additional ablations in the appendix. In Sec. 7.3, we ablate the number of function evaluations (NFE) jointly with the single-step rollout stride. In Sec. 7.4, we analyze the semantic readout of our VAE in detail and show that it is crucial for long-horizon stability; we attribute this to the implicit constraint that the spherical readout imposes on the latent manifold during training. As this design is orthogonal to the world model itself, it can be adopted by any occupancy world model to obtain an 11% relative improvement at negligible cost. 

**Table 4** Agent motion realism under our log-free setting. We adopt the behaviour-simulation JSD protocol of Scenario Dreamer [26] (Lin. Spd., Ang. Spd., Acc., Near. Dist.). Most of the discrepancy comes from IDM control and layout initialization rather than the generated occupancy maps. **GT vs. GT split** (real trajectories randomly split in half) serves as an empirical lower bound; **IDM-on-real-map** isolates the effect of our generated road topology by running the _same_ IDM controller on real lane graphs from GT occupancy. Behav. and Occ. : Agent action behavior and occupancy used to extract lanes for IDM control. 

**Table 5** Closed-loop Interaction Safety Evaluation (Collision Rate %). Each setting tested using 7500 samples in 150 maps. We use max 6 agents to collect 10s non-collision video clips for downstream training. 

|**Init. method**|**Max agents**|**3s**|**5s**|**10s**|**20s**|**60s**|
|---|---|---|---|---|---|---|
|Ours|4|0.00|0.00|0.12|0.45|0.49|
||5|0.00|0.03|0.23|0.42|0.61|
||6|0.02|0.11|0.38|0.44|0.77|
||7|0.05|0.11|0.41|0.52|0.79|
|Random|7|0.19|0.23|0.71|0.91|1.00|


|Layout|Behav.|Occ.|Distri<br>|butiona<br>|l JSD (_×_|10<sup>_−_2</sup>)_↓_<br>|
|---|---|---|---|---|---|---|
||||Lin.<br>Spd.|Ang.<br>Spd.|Acc.|Near.<br>Dist.|
|GT split<br>(l.b.)|GT|GT|1.42|0.05|7.61|0.15|
|GT|IDM|GT|5.91|0.13|11.76|0.7|
|Layout<br>Gen.|IDM|GT|8.13|0.35|17.9|1.7|
|Layout<br>Gen. (Ours)|IDM|Gen.|8.76|0.35|18.6|1.4|


**Table 6** Breakdown of inference speed per frame (ms). All results are tested on 1 _×_ RTX4090 with float32 precision. No further acceleration like pre-compile applied here. 

||**Encoder**|**W-DiT**|**Decoder**|**Layout**<br>**Gen.**|**IDM Plan.**<br>**& rendering**|
|---|---|---|---|---|---|
|**Latency**(ms)|16.88|386.4|9.49|68.7|7.1|


12 

## **5 Conclusion** 

In this paper, we present OccSim, the first occupancy world model-driven simulator capable of generating diverse and realistic rollouts spanning thousands of frames without any BEV layout or HD map as input. We demonstrate that a comprehensive simulator built upon such generated road topologies can replicate the spatiotemporal dynamics of driving scenarios with significantly higher fidelity than traditional simulators. As our framework is inherently compatible with complex learning-based policies, future work could study replacing IDM with other data-driven control strategies, alongside extending the simulator to support high-fidelity multi-modal generation. 

### **Acknowledgments** 

This research was enabled in part by the Digital Research Alliance of Canada (alliancecan.ca), the NVIDIA Academic Grant Program, and Google TPU Research Cloud (TRC). 

13 

## **Appendix** 

In this appendix, we supplement the following materials to support the findings and conclusions drawn in the main body of this paper. 

|**6**<br>**Trai**|**ning and metric details**|**15**|
|---|---|---|
|6.1|Details of OccSim configuration . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|.<br>15|
|6.2|Training details of baseline reproduced . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|.<br>15|
|6.3|Augmentation in Layout generator<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|.<br>15|
|6.4|Additional metrics details<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|.<br>16|
|6.5|More simulation pipeline details . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|.<br>16|
|**7**<br>**Add**|**itional ablation experiments**|**17**|
|7.1|Inference speed and condition comparison . . . . . . . . . . . . . . . . . . . . . . . . . . . .|.<br>17|
|7.2|Validating the lane extraction heuristic against HD maps<br>. . . . . . . . . . . . . . . . . . . .|.<br>18|
|7.3|More details in few steps sampling & single step rollout stride . . . . . . . . . . . . . . . . .|.<br>18|
|7.4|Spherical readout: a norm-invariant semantic head . . . . . . . . . . . . . . . . . . . . . . .|.<br>19|
|7.5|Complementing Real Logs with OccSim Data . . . . . . . . . . . . . . . . . . . . . . . . . . .|.<br>20|
|**8**<br>**Add**|**itional visualization**|**21**|
|8.1|Details of trajectory shapes used in Fig. 4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|.<br>21|
|8.2|Comparison with other Occ. World Models in long-horizon rollouts<br>. . . . . . . . . . . . . .|.<br>21|
|8.3|Comparison with out-painting based methods . . . . . . . . . . . . . . . . . . . . . . . . . .|.<br>21|
|8.4|Ultra long rollout from W-DiT: 100+km city scale generation with real world trajectory. . . .|.<br>22|
|8.5|Multi-modal diversity of W-DiT: fix-seed multi-time rollout results . . . . . . . . . . . . . . .|.<br>22|
|8.6|Visualization of chaos baseline constructed . . . . . . . . . . . . . . . . . . . . . . . . . . . .|.<br>23|
|**9**<br>**Algo**|**rithm details**|**23**|
|9.1|Heuristic for Single frame fusion. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|.<br>23|
|9.2|Branch road detection and topology extraction.<br>. . . . . . . . . . . . . . . . . . . . . . . . .|.<br>24|
|9.3|Lane topology extraction.<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|.<br>24|
|9.4|2D-IDM based agent simulation engine.<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . .|.<br>25|
|**10 Pote**|**ntial limitation and Future work**|**27**|


14 

## **6 Training and metric details** 

### **6.1 Details of OccSim configuration** 

For training of OccSim, Occ3D-nuScenes [30] is used for all static realism comparisons to equalise training data volume; Considering the training cost, for performance reported in Fig. 4, we use the public released weight trained on original Occ3d NuSc dataset (with dynamic agent) for all conditional evaluation (First 3 figures on the top), where we can see a close performance between W-DiT and COME. To fairly compare W-DiT with the previous SoTA occupancy world model, we used the preprocessed static occupancy retrained COME in all unconditional experiments in Fig. 4. 

For Tab. 2, OccSim is trained on UniOcc-Waymo [33], and downstream forecasting models trained on the data collected from it are evaluated on the UniOcc-nuScenes validation set. We adopt UniOcc labels rather than Occ3D for their unified voxel categorization; since no Occ3D-nuScenes label is used to train OccSim, no label leakage occurs at test time. The OccSim-collected data ( _†_ ) matches UniOcc-Carla in volume, and 5 _×_ ( _⋆_ ) denotes five times this volume collected from OccSim, with OccSim’s own training data unchanged. 

The two components OccSim’s: W-DiT and the Layout Generator, was conducted separately as follows. For W-DiT, we trained for 200 epochs on 4 Blackwell RTX Pro 6000 GPUs with a batch size of 32. Training on the Nuscenes dataset took approximately 100 GPU hours. For the Layout Generator, we trained for 500 epochs on 8 A100 80G GPUs, taking approximately 160 GPU hours. All experiments used AdamW with cosine annealing, which decayed the learning rate from 3.2e-5 to 3.2e-6. 

In Eq. 3, we set _λ_ = 2, with 20% probability to drop condition during training for classifier-free guidance [13] in sampling stage. When generating **M** rand, we control the maximum of overall masked region **M** mask between 10% to 50% of the full latent size. _τ_ in Eq. 3 is sampled from sigmoid( _N_ (0 _, I_ )). In all W-DiT-based rollout experiments described in the main text, we used NFE=10, CFG=1.1, and a roll-out of 3m per step. We further analyze these hyperparameters in Sec. 7.3. 

### **6.2 Training details of baseline reproduced** 

For SemCity [17] reproduced, we first retrain the triplane autoencoder in existing codes on preprocessed Occ3d-Nusc datasets (filter all of dynamic agents) for 30 epochs, the rIOU/rMIOU is 86.07%/76.7% for Occ3dNusc. Then the triplane diffusion was trained with these triplane representations for 50000 steps and 70000 steps for Occ3d-Nusc and Occ3d-Waymo, with batch size 18, initial learning rate 5 _×_ 10<sup>_−_4</sup> linearly annealed to 0, EMA rate 0.9999. Final training losses were 0.126–0.129 (vs. _∼_ 0 _._ 78 at initialization) for both datasets. All other architectural hyperparameters (embedding dim, MLP depth, triplane channel width, DDPM schedule) match the original SemCity configuration. 

### **6.3 Augmentation in Layout generator** 

Theoretically, the distribution of valid vehicle behaviors given a specific map representation, denoted _P_ ( _H|_ **z** _t_ ), is inherently highly multimodal, as various driving intentions can perfectly align with the same static environment. However, direct optimization on a finite training dataset _D_ = _{_ ( **z**<sup>(</sup> _t_<sup>_i_)</sup><sup>_, H_(</sup><sup>_i_))</sup><sup>_}N_</sup> _i_ =1<sup>poses a severe risk of overfitting,</sup> as the number of samples is only 28K to train the DiT-S. In practice, for any specific scene **z**<sup>(</sup> _t_<sup>_i_)</sup> in the log, we only observe a single deterministic realization of the vehicles’ behavior _H_<sup>(</sup><sup>_i_)</sup> . Consequently, without proper regularization, model tend to memorize these exact map-action pairs, effectively collapsing the learned conditional distribution into a Dirac delta function, _Pθ_ ( _H|_ **z**<sup>(</sup> _t_<sup>_i_))</sup><sup>_≈δ_(</sup><sup>_H −H_(</sup><sup>_i_)).</sup> 

To prevent the model from memorizing spurious correlations between specific voxel arrangements and deterministic position, we introduce the data augmentation in layout generator training. By applying paired spatial transformations _T_ to both the condition and the target, i.e., ( _T_ ( **z** _t_ ) _, T_ ( _H_ )), we artificially expand the support of the empirical distribution. Specifically, we introduce a two-stage data augmentation pipeline comprising agent-level perturbations and global spatial transformations. 

First, to manage scene density and prevent the model from overfitting to overly crowded environments, we cap the maximum number of vehicles per frame at 10; if a frame contains _N >_ 10 vehicles, we uniformly sample a 

15 

subset of exactly 10 vehicles without replacement, ensuring each vehicle has an equal retention probability of 10 _/N_ . For each retained vehicle, we project it onto a 2D spatial heatmap _H ∈_ R<sup>200</sup><sup>_×_200</sup><sup>_×_1</sup> as a Gaussian distribution. Specifically, the Gaussian is centered at the vehicle’s spatial coordinates with a kernel radius of 3. To simulate positional uncertainty and enrich the local behavioral manifold, we independently perturb the center of each Gaussian, randomly shifting it within a local 5 _×_ 5 neighborhood restricted to the drivable surface area. 

Following this localized perturbation, we apply rigid global transformations to the entire augmented scene (including both the occupancy map and the constructed heatmap _H_ ). We uniformly sample and apply discrete rotations _R ∈{_ 90<sup>_◦_</sup> _,_ 180<sup>_◦_</sup> _,_ 270<sup>_◦_</sup> _}_ and axis-aligned reflections (flipping along the x- or y-axis). Crucially, identical spatial transformations are applied to the corresponding latent representations to maintain spatial alignment with _H_ . While such reflections fundamentally invert the handedness of the traffic rules (effectively synthesizing valid left-hand traffic scenarios from right-hand data), this joint transformation ensures that all local topological constraints and relative vehicle dynamics remain physically coherent. This composite strategy effectively artificially expands the empirical distribution, forcing the network to learn robust, viewpoint-invariant geometric representations. 

### **6.4 Additional metrics details** 

To evaluate the diversity of the generated stochastic rollouts, we employ two distinct metrics: Pairwise mIoU Diversity in the decoded semantic space, and the Vendi Score [9] in the latent feature space. 

For the decoded semantic space, we generate _N_ independent sequences over T frames using different random seeds. At any given timestep _t_ , we compute the mean Intersection over Union (mIoU) across all semantic categories for every unique pair of generated occupancy grids. The Pairwise mIoU Diversity at time _t_ is then defined as the complement of the average pairwise similarity: 


where _P_ = _{_ ( _i, j_ ) : 1 _≤ i < j ≤ N }_ denotes the set of all unordered seed pairs. The rollout-level diversity is obtained by averaging _Dt_ over time. 

To capture structural diversity in the latent space, we report the Vendi Score, which measures the effective sample size of the generated distributions. First, we extract frame-level features _{xi}_<sup>_N_</sup> _i_ =1<sup>usingpretrained</sup> encoders (i.e., the OccFM VAE encoder and the UniScenes AE encoder). We then compute a cosine similarity kernel matrix _Q_ , where its elements are given by _Qij_ = (1 + ˜ _x_<sup>_⊤_</sup> _i_<sup>_x_˜</sup><sup>_j_)</sup><sup>_/_2, with</sup><sup>_x_˜ being the</sup><sup>_ℓ_2-normalized feature.</sup> The Vendi Score is calculated as the exponential of the von Neumann entropy of the normalized kernel matrix _Q_ ˆ = _Q/_ tr( _Q_ ): 


where _{λℓ}_ are the non-negative eigenvalues of _Q_<sup>ˆ</sup> . 

Intuitively, the Vendi Score quantifies the effective number of distinct modes within a given set of generations. By evaluating the entropy of the similarity eigenspectrum, it properly penalizes highly correlated samples. A higher Vendi Score indicates that the generated occupancy features are widely distributed across the latent space, reflecting true structural and geometric diversity rather than minor variations of a single collapsed mode. 

### **6.5 More simulation pipeline details** 

In Tab. 2, we quantitatively demonstrate an important downstream application of our proposed method: providing data for training of downstream occupancy world model. Here, in Fig. 7, we show the detailed process of how ego vehicle was designed to run in our simulation environment. 

Specifically, when simulating the motion behavior of agents (vehicles), we do not distinguish between ego and non-ego vehicles, we just collect the training data with the ego as the center. Therefore, in another words, all agents in the simulation are equivalent and we simply selected a car at random to record the data. Considering 

16 


**Figure 7 The simulation pipeline after static occupancy fusion. A** : Part of the lane graph _G_ extracted from the fused global semantic occupancy _M_ global, shown overlaid on it. **B** : All agents, include ego, are instantiated by the same procedure (Layout generator in 3.3); the ego is distinguished only in that observations are rendered from its pose and itself is not rendered in collected data. Grey dots mark sampled initial poses; each agent independently draws a destination from all possible branch road boundary, and routes to it via A<sup>_∗_</sup> over the extracted lane graph. **C** : The routed lane segments are connected and B-Spline smoothed into an initial reference route _π_ traj. **D** : The realized trajectory after closed-loop 2D-IDM execution. Pink dots mark lane switches triggered by agent–agent interaction (Sec. 9.4); because these depend on the joint state of all agents, the realized trajectories differ across rollouts even when the reference routes coincide. No route or trajectory at any stage is replayed from a recorded log. 

the irregularities in the generated occupancy, a closed-loop episode in our setting lasts around 1 min (Tab. 5), whereas Carla can run indefinitely in autopilot mode. 

It is worth noting that the simulation data generated by OccSim exhibits a high degree of diversity and non-deterministic trajectories: 

- W-DiT, which generates static scenes, is multi-modal, which allow us synthesize a large number of occupancy frames with complex road networks. 

- The multi-modality of layout generator: as the ego vehicle moves forward, agents ahead are generated and rendered into the scene in real time, and each generation of a reasonable position is multimodal. 

- Each agent’s destination is a randomly selected point on the map’s boundary, which means that traffic flow behavior can vary even within the same map. 

- The initial velocity and acceleration of each agent also vary slightly, and when multiple agents move under IDM control, their interactions (avoidance maneuvers) with other agents are completely different in multi rollouts. 

## **7 Additional ablation experiments** 

### **7.1 Inference speed and condition comparison** 

In the previous section, we demonstrated a comparison between our method and prior approaches in terms of realism. However, it is worth noting that our method also achieves improvements in real-time performance compared to COME. In Tab. 7, we compare the time and FLOPS required for our method to generate a single frame. Our work generate 1 frame per inference, but still more efficient than COME, which generate 6 frames together per inference step. 

17 

**Table 7** Comparison of efficiency and computational cost among different methods. When evaluating the time taken by our method, we distribute the post-processing time evenly across each frame of the sequence generation. Each result was computed independently using an RTX4090. DOME and COME generate 6 frames together, ours is 1 single frame per step, for fair comparison, we keep measure the GFLOPS / inference time needed per single frame. 

|Method|WM|Input|#Params|FPS|GFLOPS<br>frame|
|---|---|---|---|---|---|
|DOME|✓|4 frames sem. occ.&traj|444.07M|5.48|8891.98|
|COME|✓|4 frames sem. occ.&traj|204.53M|2.33|41333.17|
|InfiniCubes|✕|1 frames sem. occ.|831.75M|0.02|990927.28|
|OccSim (Ours)|✓|1 frames sem. occ. & traj|181.24M|2.58|15570.18|


**Table 8 Geometric validation of lane topology extraction against HD maps.** Both rows run the identical extraction pipeline on the same spatial extent and are evaluated against the same nuScenes HD-map centerlines; they differ only in the input drivable mask. The first row uses a rasterized HD-map polygon and thus lower-bounds the error attributable to our lane construction alone; the excess of the second row is the net cost of operating on fused occupancy. 

|Drivable mask|Error source|Chamfer (m)_↓_|P@1.0m_↑_|R@1.0m_↑_|
|---|---|---|---|---|
|HD-map polygon|Definitional (l.b.)|0.51|0.87|0.90|
|GT semantic occupancy|+ occupancy & fusion|0.74|0.79|0.82|


### **7.2 Validating the lane extraction heuristic against HD maps** 

In design of OccSim, we use the heuristic detailed described in Sec. 9.3, which will later be used as trajectory segments for agents. Here we use the real HD-Map to measure the effectiveness of this approch. 

As shown in Tab. 8, we first rasterize the HD-map drivable-area polygon and feed it to the same heuristic in Alg. 4, which establishes a lower bound on the error that our lane construction incurs regardless of the input quality. We attribute this residual mainly to two properties intrinsic to the construction: the absence of explicit turning connectors at intersections, and the fixed-width assumption of our orthogonal offsetting, which cannot accommodate roads of non-uniform lane width. Substituting GT semantic occupancy for the polygon raises the Chamfer error to 0.74 m, with precision and recall of 0.79 and 0.82. The additional degradation is within one voxel of the 0.4,m grid, and we attribute it to voxel quantization together with the absence of a separate parking-area label in the occupancy taxonomy, which causes parking lanes to be treated as drivable surface. 

### **7.3 More details in few steps sampling & single step rollout stride** 

For NFE step, as shown in Fig. 8a, NFE=10 get the best and stablest results in terms of fidelity. For the rollout stride, we use straight trajectory in Fig. 13 to test fidelity of rollouts under different single step stride, from 3m to 30m. As shown in figure 9, we find that 3 meters per step achieve the best results. 

We do not attributes this to out-of-distribution(OOD) in update size: During training, **M** rand is composed of one to three random rectangular blocks whose spatial extent spans roughly 8–56 m (overall 10%50% of the full scene); a 30 m forward band is therefore not OOD in size, and the model is in principle capable of completing an unknown region at that scale in a single pass. 

We instead attribute the degradation to the autoregressive structure itself: since W-DiT re-synthesizes 


**Figure 8 Effect of sampling steps (NFE) on rollout quality.** Per-frame 3D unconditional FID against the training-set marginal, over 150-frame rollouts on the UniScenes AE latent (3 m per step, cfg = 1 _._ 1). Fidelity does not improve beyond NFE=10, which we adopt as the operating point. 

the complete frame at every step, a given spatial location is refined _⌈_ FOV _/_ ∆ _d⌉_ times over its visible lifetime, and this count falls as the stride ∆ _d_ grows (FOV: Field of View, 80 _m ×_ 80 _m_ here). Prior outpainting-based 

18 

methods like InfiniCube [21] obtain an **equivalent effect** through repeated intra-block resampling [22], at the cost of a 64 _×_ larger per-frame compute budget (Tab. 7); our stride offers a cheaper form of the same fidelity–throughput trade-off, and the ablation shows that the returns are already saturated at 3–5 m. 


**Figure 9** Fidelity of generated frames over time under different moving steps. We use the ground truth trajectories and poses at first 35 frames, concatenated with straight trajectory moving with different stride in single step. We use 3m / step for all of the experiments mentioned in the main text. 

### **7.4 Spherical readout: a norm-invariant semantic head** 

In Tab. 3, we analyzed several factors that influence performance in W-DiT, including the loss function and architectural design. However, we found that the special designed representation readout method is also essential for stable, long-term rollouts. Specifically, when training the VAE for occupancy latent compression, we revise readout method from standard matmul to sphere decode, as shown in Alg. 1. 

**Table 9** Single-frame VAE encode–decode reconstruction on Occ3D-nuScenes (C18). Sphere decoding has almost the same IoU and mIoU. 

|**VAE Decode Method**|**IoU**|**mIoU**|
|---|---|---|
|Matmul|74.66|85.99|
|Sphere|**75.15**|**86.27**|


**Table 10** Geometric analyze of the semantic template **W** before (Matmul) and after (Sphere) _ℓ_ 2 normalization. CV.: coefficient of variation. PC.: principal component. MACS: Mean Absolute Cosine Similarity. 

|**Template statistic**|**Matmul**|**Sphere**|
|---|---|---|
|Avg. length|2.801|1.000|
|Length CV. (_↓_)|0.4385|**0**|
|Top-3 PC. ratio|58.73%|49.89%|
|MACS. (_↓_)|0.2324|**0.2207**|


As shown in Fig. 10 and Tab. 9, the sphere readout has almost the same reconstruction performance as original matmul-based method, but significantly help the rollout stability. Furthermore, when we applied the sphere readout only during testing to VAE representations trained using the matmul readout, as shown by the blue line in Fig. 10, the results were actually worse. This experiment decoupled the decoder design itself from its effect on constraining the latent manifold during VAE training, demonstrating that the sphere readout implicitly reshapes the geometry of the latent manifold, and that this constraint ensures stability. 

Treating each generated latent frame _z ∈_ R<sup>50</sup><sup>_×_50</sup><sup>_×_16</sup> as 2,500 tokens of length 16, the latents from approximately 28,000 samples in the training set form a 16-dimensional space comprising approximately 7 _×_ 10<sup>7</sup> tokens. In this space, we evaluate angular(which isolates directional drift) and radial distance to reflect the OOD of the latents under VAEs with different readout schemes. For rollout frame _zi_<sup>(</sup><sup>_t_)</sup> at frame t, the angular distance is its 

19 

k-th nearest-neighbor _πk_ ( _i_ ) distance in ground-truth latent _zgt_ on the unit sphere, defined below, here k=10. Radial distance is the angular distance without unit sphere constrain. Each is a median over the 2,500 tokens per frame, then across sequences (band: 25–75th pct.). 


**Figure 10** Long-horizon 3D unconditional FID in the UniScenesAE latent space. Standard matmul decoding degrades rapidly as latent energy decays over rollout, while norm-invariant sphere decoding stays stable across all 150 frames. 

**Algorithm 1** Norm-Invariant Sphere Decoding 

**Require:** Decoded feature map **F** _∈_ R<sup>_B×H×W ×Z×C_</sup> , semantic template **W** _∈_ R<sup>_C×K_</sup> , scale _s_ 

**Ensure:** Class logits **L** _∈_ R<sup>_B×K×H×W ×Z_</sup> 

1: **if** method = sphere **then** 2: **F** ˆˆ _←_ **F** _/∥_ **F** _∥_ 2 _▷_ normalize over _C_ (dim = _−_ 1) 3: **W** _←_ **W** _/∥_ **W** _∥_ 2 _▷_ normalize over _C_ (dim = 1) 4: **S** _←_ **F**<sup>ˆ</sup> **W**<sup>ˆ</sup> _▷_ cosine similarity 5: **S** _← s ·_ **S** _▷_ fixed temperature _s_ 6: **else** 

7: **S** _←_ **F W** _▷_ standard matmul; logit _∝∥_ **F** _∥_ 8: **L** _←_ permute( **S** ) 

9: **return L** 

The results are shown in Fig. 11. Under the matmul VAE, the raw kNN distance inflates by _∼_ 2 _._ 2 _×_ over the rollout while the angular distance stays essentially flat ( _∼_ 0 _._ 99 _×_ ); the sphere VAE remains stable in both. Since raw and angular kNN differ only in whether the token norm is retained, this shows the matmul latent drifts _purely radially_ (norm inflation), not by directional change. Although the absolute distances of the two sub-figures are not directly comparable (they live in different latent spaces), the within-space trends consistently indicate that the sphere readout stabilizes the rollout by constraining the norm geometry of the latent space, mirroring the static norm imbalance in Tab. 10. Further analysis in Tab. 10 show that normalization removes inter-class norm imbalance (length CV _→_ 0) in template **W** while leaving inter-class _directions_ almost untouched (MACS nearly unchanged), and flattens the singular-value spectrum toward isotropy. 

Finally, we further verify that the sphere readout is not specific to our architecture: revising OccFM[20]’s VAE with the sphere readout from the matmul based one improves its downstream forecasting mIoU by several points, indicating the gain comes from the geometric regularity it imposes on the latent space rather than any model-specific design. As shown in Fig. 12, the sphere readout thus offers an almost free improvement (+2.74% absolutely, +11% relatively): no extra parameters cost, no reconstruction trade-off, yet a consistent downstream gain. 

### **7.5 Complementing Real Logs with OccSim Data** 

Tab. 11 compares OccWorld trained on real UniOcc-Waymo logs (Uni-W), on OccSim data alone, and on their mixture, all evaluated zero-shot on UniOcc-nuScenes. Trained alone, OccSim data remains below real logs, which is expected: real logs are the realism upper bound of the data OccSim learns from. It nonetheless outperforms the asset-based CARLA data by a large margin. The value of OccSim lies in what logs cannot offer: a log is a fixed recording, whereas OccSim generates new road topologies and traffic layouts on demand and supports closed-loop interaction. Adding OccSim data amounting to 30% of Uni-W improves the average IoU over 1–3s by 6.8% relative (21.95 to 23.44) and the average mIoU by 4.1% (19.13 to 19.91), with gains at every horizon except 3s mIoU, which decreases slightly (15.80 to 15.08). OccSim data thus complements real logs without additional annotation. As in Tab. 2, all metrics here are computed open-loop against logged futures (see limitation 5 in Sec. 10). 

20 


**Figure 11** Per-token latent OOD within each VAE’s own space: raw kNN (with norm) inflates only under matmul, while angular kNN (norm removed) stays flat for both. 


**Figure 12** Downstream forecasting mIoU / IoU across rollout steps. Retraining the VAE with the sphere readout improves both metrics over the matmul baseline with almost no extra cost. 

**Table 11** OccWorld trained on real UniOcc-Waymo logs (Uni-W), OccSim data (5 _×_ volume, as in Tab. 2), their mixture (OccSim data amounting to 30% of Uni-W), and CARLA (Uni-C), evaluated zero-shot on the UniOcc-nuScenes validation set. 

|Train Data||mIoU_↑_|||IoU_↑_||
|---|---|---|---|---|---|---|
||1s|2s|3s|1s|2s|3s|
|Uni-W|23.47|18.11|15.80|27.35|20.86|17.63|
|Uni-W + OccSim|24.95|19.71|15.08|29.73|22.11|18.49|
|OccSim|19.54|12.31|9.08|23.87|16.92|13.47|
|CARLA|11.79|8.35|6.75|18.31|14.09|12.03|


## **8 Additional visualization** 

We provide more visualizations for details of our work here. More information like dynamic traffic simulated can be found in the video in the supplementary materials. 

### **8.1 Details of trajectory shapes used in Fig. 4** 

To systematically evaluate the robustness of our model in long-horizon generation across diverse driving behaviors, we configure three distinct spatial trajectory profiles: Loop, Straight, and Turn. As illustrated in Fig. 13, the trajectory generation process conditioned on is consist of the initial ground-truth (GT) trajectory (highlighted in blue, encompassing frames 1–40) and extended trajectory with 3 modes (red lines). 

### **8.2 Comparison with other Occ. World Models in long-horizon rollouts** 

From Fig. 14, we can clearly observe that our proposed W-DiT significantly extends the duration of stable rollout. Even after 3000 frames (1500s, approximately 25 minutes with 2Hz setting in Occ3d-NuSc), the generated occupancy remains stable. The top half of Fig. 14 shows the output when the loop trajectory from Fig. 13 is used as input, while the bottom half shows the output when the straight-line trajectory from Fig. 13 is used as input. 

### **8.3 Comparison with out-painting based methods** 

World models are indeed one of the technologies used to generate boundary-free driving scenes; however, outpainting-based methods can achieve the same in the context of static occupancy. Therefore, in this section, we aim to qualitatively demonstrate that our proposed method outperforms previous outpainting-based approaches. In Fig. 15, we compare our model against SemCity [17] and InfiniCube [21], both of which generate future 

21 


**Figure 13** Visualization of trajectory shapes (Loop, Straight, and Turn) evaluated in Fig. 4. The green star indicates the starting point. The blue solid line denotes the initial ground-truth (GT) trajectory snippet (frames 1–40) used as the condition prompt, while the red dashed line represents the extended trajectory explicitly designed to guide the long-horizon generation. For visual clarity the displayed trajectories are truncated at 500 frames, whereas our actual synthesis spans up to 3000 frames. 

scenes via outpainting. Notably, InfiniCube additionally requires an HD-map aligned with the region to be generated. 

As shown in the Fig. 15, the outpainting-based InfiniCube not only requires extra HD-map annotations but also suffers from severely limited diversity, exhibiting only minor variations in the foreground across different segments. In contrast, among the HD-map-free approaches, SemCity’s results are markedly inferior to ours in realism, diversity, and continuity. 

### **8.4 Ultra long rollout from W-DiT: 100+km city scale generation with real world trajectory.** 

In Fig. 4, we evaluate the fidelity of model rollout, our proposed method remained stable over a time scale of 1,000 frames. Furthermore, we used a 3,000-frame rollout to construct a static map and collected data based on this map to conduct the experiments presented in Tab. 2. Here we push the length of generation to 100x longer, build a city-scale occupancy in Fig. 16, to further show the stability of W-DiT. 

By manually concatenating all real-world trajectories from the occ3d-waymo training, we obtained driving trajectories from real drivers totaling over 100 km in length (shown at middle of Fig. 16). With this as the user-steered input of our model trained purely on occ3d-nuscenes, we further expanded the rollout to 110K frames, resulting in city-level occupancy data spanning over 100 km. 

Specifically, after fully generating these approximately 110K frames, we fused them using Alg. 2 and presented the fusion results for a portion of the subsequences. Furthermore, we randomly visualized 10 frames from this sequence. As can be seen, driven by a large number of real-world trajectories, our method is able to generate highly diverse and realistic road structures, which provides a foundation for subsequent data collection and training in downstream tasks. As far as we know, this is the largest scale of driving scenario generation. 

### **8.5 Multi-modal diversity of W-DiT: fix-seed multi-time rollout results** 

In the main text, we quantitatively demonstrate the SoTA diversity of our W-DiT-based model rollouts using the Vendi Score. Here, in Figure 17, we qualitatively illustrate our model’s ability to capture the multi-modality of the future when only the input noise (seed) differs. After 50s (100 frames, we use 6m/s speed to generate trajectory) rollout, the branch road topology, vegetation / man-made presents obvious difference. 

22 


**Figure 14** Qualitative comparison of two rollouts for two models: previous SOTA occupancy world model (first and third rows), and our model (second and fourth rows) at different horizons. Ours exhibits long-horizon stability under different trajectory input. 

### **8.6 Visualization of chaos baseline constructed** 

As shown in Fig. 18, the constructed “chaos” baseline primarily comprises severely fragmented road segments, topologically disconnected layouts, and large-scale empty regions. Consequently, as we mentioned in Fig. 4, any model yielding FID/KID scores above this baseline threshold can be deemed completely incapable of synthesizing large-scale, valid road networks. 

## **9 Algorithm details** 

### **9.1 Heuristic for Single frame fusion.** 

After we obtained the raw forecast observation _{Oi}_<sup>_K_</sup> _i_<sup>from the W-DiT based world model, we than use the</sup> following algorithm 2 to fuse all frames to _M_ global. 

The pipeline consists of four primary phases. First, to manage computational overhead and redundancy, we subsample the generated sequences into keyframes based on a spatial distance threshold, projecting them onto a unified SE(2) bird’s-eye-view (BEV) plane. Second, during the initial fusion pass, we introduce a deterministic column sinking operation. This forces all predicted ground-level voxels to align with the absolute zero-elevation plane ( _z_ = 0), effectively rectifying pitch and roll artifacts or elevation drifts accumulated over long-horizon rollouts. Third, to address occlusions and local generation artifacts, we leverage the temporal redundancy of non-keyframes; by applying a spatial majority voting mechanism, we robustly inpaint the remaining gaps on the _z_ = 0 plane. Finally, a morphological refinement stage—comprising binary closing and connected-component area filtering—is applied to enforce spatial continuity on sidewalks and systematically remove isolated noise clusters (e.g., artifacts smaller than 2m<sup>2</sup> ). This pipeline ensures a connected and smooth road topology, which is strictly required for downstream 2D multi-agent simulations. 

23 


**Figure 15** Visualization of static occupancy generated from InfiniCube, SemCity and our approach (from top to down). For InfiniCube, we reuse the boundary HD-map to continuously extend the map along a straight line. Likewise, for SemCity and our method, we extend the scene in the same direction. 

### **9.2 Branch road detection and topology extraction.** 

Then, to bridge the gap between discrete occupancy grids _M_ global and vectorized road networks required for downstream multi-agent simulation, we propose a robust topology extraction and graph refinement algorithm. We first extract the 2D drivable surface mask, apply connected-component filtering, and perform strict singlepixel skeletonization to initialize the graph structure. To mitigate rasterization artifacts, we systematically eliminate spurious triangular loops by removing the longest edges within 3-cliques. Subsequently, a rigorous graph cleaning protocol is executed: we iteratively prune short, noisy spurs and introduce a node contraction mechanism to merge spatially dense junction clusters into unified super-nodes, accurately reflecting complex real-world intersections. Finally, to precisely isolate valid map ingress and egress points, we design a novel Dual-Probe filtering mechanism. A topology probe identifies and discards artificial endpoints caused by internal fragmentation, while a semantic probe leverages the 3D elevation profile of the occupancy map to detect physical occlusions or obstacles along the projected path. Ultimately, this pipeline translates the generated voxel map into a high-fidelity, deadlock-free topological graph, providing a reliable foundation for downstream closed-loop planning and control. 

### **9.3 Lane topology extraction.** 

After we have _G_ , _V_ valid, we use the retained graph information to create lane graphs. As shown in Alg. 4, based on the extracted skeleton, i.e., _E ∈G_ , we introduce a two-phase lane topology extraction algorithm (Algorithm 3). In the first phase, we convert the raw skeletal segments into kinematically smooth reference centerlines using 3rd-degree B-Spline interpolation with a fixed spatial resolution ∆ _s_ step. To reconstruct multi-lane structures, we 

24 

|**Algo **|**rithm 2**Two-pass Keyframe-based OccupancyFusion|
|---|---|
|**Req**<br>|**uire:** Local predictions_{_ <sup>ˆ</sup>_Ot}_<sup>_T_</sup><br>_t_=1<sup>, Ego-poses</sup><sup>_{_</sup><sup>**T**</sup><sup>_t}T_</sup><br>_t_=1<sup>, max step</sup><sup>_d_max, vote threshold</sup><sup>_τ_, number of semantic</sup><br>categories_C_.|
|**Ens**<br>1: <br>2: <br>3:  <br>4:|**ure:** Fused global occupancy map_M_global _∈{_0_,_1_, . . . , C}_<sup>_X×Y ×Z_</sup>.<br>// Phase 1: SE(2) Projection & Keyframe Selection<br>**T**_t_(_x, y_)_←_ProjSE(2)(**T**_t_)_,_<br>_∀t ∈{_1_. . . T}_<br>_▷_Align to BEV plane<br>_K ←{_1_},_<br>**p**last _←_**T**1(_x, y_)<br>**for**_t_= 2**to**_T_ **do**|
|5:|**if** _∥_**T**_t_(_x, y_)_−_**p**last_∥_2 _> d_max **then**|
|6:|_K ←K ∪{t},_<br>**p**last _←_**T**_t_(_x, y_)|
|7: <br>8: <br>9:|// Phase 2: Pass 1 - Keyframe Sinking & Fusion<br>Initialize_M_global(**v**)_←_∅_,_<br>_∀_**v**_∈_Z<sup>_X×Y ×Z_</sup><br>_▷_∅denotes unassigned.<br>**for**_k ∈K_**do**<br><sup>ˆ</sup>|
|10:|_O_<sup>_′_</sup><br>_k _<sup>_←W_( </sup><br>_Ok,_**T**_k_)<br>_▷_Spatial warping to global coordination|
|11:|_▷_Assign key-frame voxels from local map to global map.|
|12:|_M_global(**v**)_←O_<sup>_′_</sup><br>_k_<sup>(</sup><sup>**v**)</sup><sup>_,_</sup><br>_∀_**v**s.t. _M_global(**v**) =∅|
|13:|∆_z_(_x, y_)_←_min_{z | M_global(_x, y, z_)_∈C_ground_}_|
|14:|_M_global(_x, y, z_)_←M_global(_x, y, z_+ ∆_z_)<br>_▷_Column sinking to lowest ground|
|15: <br>16: <br>17:  <br>18:|_M_global(**v**)_←_Mode(_N_3_×_3(**v**))for**v**where_M_global(**v**) =∅_, z_ = 0<br>// Phase 3: Pass 2 - Non-Keyframe Voting Inpainting<br>Initialize vote tensor_V ∈_N<sup>_X×Y ×Z×C _</sup>_←_**0**<br>**for**_t /∈K_**do**<br><sup>ˆ</sup>|
|19:|_O_<sup>_′_</sup><br>_t _<sup>_←W_( </sup><sup>_Ot,_</sup><sup>**T**</sup><sup>_t_)</sup>|
|20:|_V_(**v**_, c_)_←V_(**v**_, c_) +I[_O_<sup>_′_</sup><br>_t_<sup>(</sup><sup>**v**) =</sup><sup>_c_]</sup><sup>_,_</sup><br>_∀_**v**s.t. _M_global(**v**) =∅|
|21: <br>22:|_M_global(**v**)_←_arg max_c V_(**v**_, c_)ifmax_c V_(**v**_, c_)_≥τ_<br>// Phase 4: Morphological Refinement|
|23:|_M_global _←_CloseOp(_M_global_, c_sidewalk)<br>_▷_Binary closing on sidewalk|
|24: <br>25:|_M_global _←_FilterAreaOp(_M_global_, c_road_, A <_2m<sup>2</sup>)<br>_▷_Remove isolated noise<br>**return**_M_global|


generate explicit parallel lanes via orthogonal offsetting along the normal vectors of the reference trajectories. To guarantee physical feasibility, we strictly enforce a topological boundary constraint: the interior of any newly generated lane must be fully bounded by the drivable surface mask _B_ . 

In the second phase, we address the geometric overlaps that inevitably occur at complex intersections where multiple segments converge. We formulate this as a spatial intersection resolution problem. For each candidate lane, we identify conflict points that fall within a minimal distance threshold _ϵ_ of any other independent lane. We then sever the trajectories at these overlapping junctions and exclusively retain the longest continuous sub-trajectory. Finally, a secondary B-Spline interpolation is applied to eliminate any geometric artifacts or non-differentiable kinks introduced by the splitting process. This rigorous pipeline yields a highly precise, non-overlapping lane network, providing a kinematically reliable foundation for multi-agent closed-loop simulation. 

### **9.4 2D-IDM based agent simulation engine.** 

With all geometric information obtained, we introduce a 2D-IDM based simulation in Alg. 6. The algorithm is structurally divided into two phases: global pre-computation (Phase 1) and dynamic step-by-step execution (Phase 2). 

Phase 1 employs a proactive spatial pre-computation strategy. Rather than solely initializing traffic around the starting ego-pose ( **T**<sup>ego</sup> 0<sup>), the engine seamlessly injects background agents at forward and backward anchor</sup> poses ( **T** fwd, **T** bwd) extending up to a predefined horizon _d_ pre. The unified SpawnAgents procedure handles this layout generation, simultaneously sampling valid endpoints, predicting spatial coordinates, and assigning 

25 

**Algorithm 3** Branch point detection / topology extraction **Require:** Fused global map _M_ global _∈{_ 0 _, . . . , C}_<sup>_X×Y ×Z_</sup> , lane width _w_ lane, pruning threshold _τ_ prune. _V_ valid _←_ ∅ for valid branch node set in the graph. **Ensure:** Vectorized road graph _G_ = ( _V, E_ ), valid endpoints **P** valid. 1: // Phase 1: Binary Masking & Skeletonization 2: _B_ ( _x, y_ ) _←_ I[ _M_ global( _x, y,_ 0) = _c_ road] _, ∀_ ( _x, y_ ) _∈_ Z<sup>2</sup> 3: _S ←_ Skeletonize( _B_ ) 4: _S_ ( _x_ + 1 _, y_ + 1) _←_ 0 _, ∀_ ( _x, y_ ) s.t.<sup>�1</sup> _i_ =0 �1 _j_ =0<sup>_S_(</sup><sup>_x_+</sup><sup>_i, y_+</sup><sup>_j_) = 4</sup> 5: // Phase 2: Graph Initialization & Artifact Removal 6: _V ←{_ **v** _∈_ Z<sup>2</sup> _| S_ ( **v** ) = 1 _}_ 7: _E ←{_ ( **u** _,_ **v** ) _|_ **u** _,_ **v** _∈ V, ∥_ **u** _−_ **v** _∥∞_ = 1 _}_ , with weight _w_ ( **u** _,_ **v** ) = _∥_ **u** _−_ **v** _∥_ 2 8: Initialize graph _G ←_ ( _V, E_ ) 9: **for** each 3-clique (triangle) _K_ 3 _∈G_ **do** 10: _e_ max _←_ arg max _e∈K_ 3 _w_ ( _e_ ) 11: _E ← E \ {e_ max _} ▷_ Break loops to expose leaf nodes 12: // Phase 3: Iterative Spur Pruning & Junction Contraction 13: **repeat** 14: _V_ leaf _←{v ∈ V |_ deg( _v_ ) = 1 _}_ 15: Find branch path _Pl→j_ from _l ∈V_ leaf to nearest junction _j_ (deg( _j_ ) _>_ 2) 16: **if**<sup>�</sup> _e∈P_<sup>_w_(</sup><sup>_e_)</sup><sup>_< τ_prune</sup><sup>**then**</sup> 17: _V ← V \_ ( _Pl→j \ {j}_ ) _▷_ Remove short spurs 18: **until** no spurs are removed 19: _V_ junc _←{v ∈ V |_ deg( _v_ ) _>_ 2 _}_ 20: **for u** _,_ **v** _∈V_ junc s.t. _∥_ **u** _−_ **v** _∥_ 2 _<_ 2 _· w_ lane **do** 21: _G ←_ ContractNodes( _G,_ **u** _,_ **v** ) _▷_ Merge clustered junctions 22: // Phase 4: Dual-Probe Endpoint Filtering 23: _O_ obstacle _←_ ( _M_ global( _x, y, z ≥_ 1) _∈{/ c_ road _, c_ sidewalk _,_ ∅ _}_ ) _▷_ Get 3D obstacle occ above ground layer 24: _V_ end _←{v ∈ V |_ deg( _v_ ) = 1 _}_ 25: **for** _v ∈V_ end **do** 26: Let _⃗d_ be the outward normalized direction vector from parent junction to _v_ . 27: _Topology Probe_ : _p_ topo _← v_ + (1 _._ 5 _· w_ lane) _⃗d_ 28: _Semantic Probe_ : Generate 15m _×_ 3 _._ 6m bounding box _B_ sem along _⃗d_ from _v_ . 29: **if** _B_ ( _p_ topo) == 0 **and**<sup>�</sup> **p** _∈B_ sem<sup>I[</sup><sup>_O_3D(</sup><sup>**p**)]</sup><sup>_< τ_obs</sup><sup>**then**</sup> 30: _V_ valid _←V_ valid _∪{v} ▷_ Endpoint is neither internal nor blocked 31: **return** _G_ , _V_ valid 

initial shortest paths via A* routing. 

In the simulation part, algorithm 6 Line 20 defines the spatial identification of candidate leading vehicles ( _Ca_ ). Instead of relying on heuristic bounding box checks, an agent _a_ filters surrounding vehicles using a normalized vector dot product, <u>(</u> _∥_ **<u>pp</u>** _<u>a′a−′</u> −_ **<u>pp</u>** _aa_ <u>)</u> _·∥_ **h** 2 _a_<sup>_>_0</sup><sup>_._5</sup> , to ensure the target is strictly within a 60<sup>_◦_</sup> forward field-of-view cone. � � This is coupled with a trajectory distance constraint (Dist( **p** _a′, π_ traj) _< d_ lat) to confirm the target is actively blocking the planned route. 

Furthermore, algorithm 6 Line 23 explicitly shows the lane-changing logic. An agent initiates a Bezier-smoothed lane transition and A* re-routing only when the longitudinal distance falls below a critical threshold ( _s < d_ lc) under two specific risks: either the ego agent is approaching a slower leader (∆ _v >_ 0), or it encounters a wrong-way/head-on vehicle. The latter scenario is elegantly captured by the negative dot product of their respective heading unit vectors ( **h** _a ·_ **h** _a_ lead _< −_ 0 _._ 5). 

Finally, the kinematic states are updated via IDM, and the dynamic 3D assets are sequentially rendered onto the cropped static background using a spatial overwrite operator (⊛) to handle semantic Z-buffering (Step 2.3), ultimately producing a seamless sequence of dynamic local environments. 

26 

**Algorithm 4** Lane Topology Extraction 

**Require:** Extracted segments _S_ from _G_ , drivable mask _B_ , lane width _w_ lane, distance threshold _ϵ_ , resampling step ∆ _s_ step. 

**Ensure:** Vectorized explicit lanes _L_ final. 1: // Phase 1: B-Spline Smoothing & Parallel Offsetting 

2: _L_ cand _←_ ∅ 3: **for** each _S ∈S_ s.t. _|S| ≥_ 10 **do** 4: **P** _c ←_ BSpline( _S_ path _,_ deg = 3 _,_ ∆ _s_ step) 5: **N** _←_ NormalVectors( **P** _c_ ), _n ←⌊S_ width _/w_ lane _⌋−_ 1 6: **O** _←_ �� _i −_<sup>_<u>n−</u>_</sup> 2<sup><u>1</u></sup> � _w_ lane �� _i ∈{_ 0 _, . . . , n −_ 1 _}_ � 7: **for** _o ∈_ **O do** 8: **P** _l ←_ **P** _c_ + _o ·_ **N** _▷_ Generate parallel lane curves 9: **if P**<sup>_◦_</sup> _l_<sup>_⊂B_</sup><sup>**then**</sup> _▷_ **P**<sup>_◦_</sup> _l_<sup>denotes the interior of the trajectory</sup> 10: _L_ cand _←L_ cand _∪{_ **P** _l}_ 11: // Phase 2: Spatial Intersection Resolution & Resmoothing 12: **for** each _L ∈L_ cand **do** 13: _CL ←{_ **p** _∈ L | ∃L_<sup>_′_</sup> _∈L_ cand _\ {L},_ dist( **p** _, L_<sup>_′_</sup> ) _< ϵ} ▷_ Identify cross-lane overlaps 14: _L ←_ arg max _L_ sub _⊆_ ( _L\CL_ ) _|L_ sub _| ▷_ Retain the longest continuous sub-trajectory 15: _L ←_ BSpline( _L,_ deg = 3 _,_ ∆ _s_ step) _▷_ Smooth artifacts caused by splitting 16: _L_ final _←{L ∈L_ cand _| |L| ≥_ 5 _} ▷_ Remove all lanes short than 5 pixels 17: **return** _L_ final 

## **10 Potential limitation and Future work** 

Although OccSim provide the first implementation of using occupancy world model in simulation, we still observe the following limitation in design and evaluation period of OccSim: 

- **Heuristic based fusion and lane graph extraction** : Although the robustness of our multi-frame fusion/lane graph extraction algorithm has been qualitatively demonstrated in numerous practical applications, given the occasional instability in the quality of the raw occupancy frames output by the model, we still seek an end-to-end fusion approach rather than frame-by-frame fusion. 

- **Latent-space warping.** W-DiT warps in latent space, assuming the VAE is approximately equivariant to planar rigid transforms. The U-Net refinement absorbs the resulting interpolation error in practice, but warping directly in occupancy space or learning an equivariant latent would remove this approximation. 

- **Limited training data** : Compared to image data, semantic occupancy data requires manual semantic 

**Algorithm 5** Spatially-conditioned agent generation and routing initialization 

**Require:** Query anchor pose **T** _∈ SE_ (2) with spatial coordinate **pT** , boolean flag _b_ ego indicating whether to explicitly initialize the ego vehicle at **T** , mean/standard of initial velocity _µv, σv_ , _M_ global as global map, _V_ valid from Alg. 3, Agents asset pool _X_ . 

1: Crop local occupancy _O_ **T** from _M_ global by pose **T** . 2: _A_ new _←_ LayoutGenerator( _O_ **T** ) _∪_ � _{_ **pT** _}_ if _b_ ego else _∅_ � 

- 3: **for** each agent _a ∈A_ new parameterized by pose **p** _a_ **do** 

- 4: Initialize velocity _va ← v_ des _∼N_ ( _µv, σv_ ) 

- 5: **p** target _∼_ Uniform( _V_ valid) _▷_ Random valid endpoint 

6: _§a ∼_ Uniform( _X_ ) 

- 7: _π_ traj _←_ A*( _L_ final _,_ **p** _a,_ **p** target) 

8: **h** _a ←_ Tangent( _π_ traj _,_ **p** _a_ ) 9: _a ←_ ( **p** _a,_ **h** _a, va, π_ traj _, §a_ ) 

      - Random agent asset 

      - Shortest valid path 

   - Generate initial headings from trajectory _▷_ Assign initial states to agent 

- 10: **return** _A_ new 

27 

annotation, which limits the total amount of available training data to fewer than 100,000 frames. This volume is significantly smaller than the amount of available RGB video data, and it also restricts our ability to explore the upper limits of the model’s performance. 

- **IDM based agent behavior simulation** : In this paper, we use IDM, a classic traffic flow control model to simulate the behavior of vehicles. Although this approach has proven effective in downstream tasks, we still hope to find more effective ways to enable this aspect of control to learn from the data, or even integrate it into the process of generating static occupancy. 

- **Open-loop evaluation.** Existing closed-loop driving benchmarks expose either raw sensor inputs (e.g., NAVSIM) or vectorized map and object states (e.g., nuPlan, Waymax), and provide no semantic occupancy interface, so occupancy-input models cannot be evaluated there in closed loop. All our downstream metrics (mIoU, IoU and planning L2) are therefore computed open-loop against logged futures; closed-loop evaluation of learned policies inside OccSim is left for future work. 

28 


**Figure 16** The full 100+ km trajectory (113321 frames) concatenated from Occ3D-Waymo. The connecting angle between every two pose sequences is set manually, and the full trajectory is smoothed with a B-spline after concatenation. This experiment uses the raw step size from real Waymo trajectories (approximately 0.9 m per frame). 

29 


**Figure 17** Visualization of W-DiT’s long-horizon rollouts under different random seeds: given the same input frame (the first frame of scene-039 and scene-105 from Occ3D-nuScenes) and an identical straight-line trajectory. The three rows correspond to seeds 999/2026/3407, respectively. We also show the comparison with GT sequences at 5s, 10s and 20s here, to further illustrate that our method generate diverse future map, instead of just memorize the ground truth. 

30 


**Figure 18** Visualization of frames from the “chaos” baseline. We randomly visualize 20 frames from the 1000 samples pool. The semantic categories represented by colors here are consistent with those in Fig. 3. 

31 

**Algorithm 6** A* routing + 2D-IDM based control engine pseudo codes 

- **Require:** A pool of global maps M generated, IDM parameters, rolling horizon threshold _d_ roll, simulation horizon _ϕ_ , Lane topology _L_ final, ∆ _t_ for Inter-frame time interval, FOV( **T** ): The set of all spatial coordinates within the perception range of the ego vehicle at pose **T** , Agents asset pool _X_ , _d_ lc for distance threshold of lane change. SpawnAgents: method generate initial state of agents, details in Alg. 5. 

- **Ensure:** Rendered sequence of dynamic local environments _{M_<sup>(</sup> local<sup>_t_)</sup><sup>_}_</sup> _t_<sup>_ϕ_</sup> =1<sup>.</sup> 

- 1: // Phase 1: Global Initialization & Pre-computation 

- 2: Randomly select a global map _M_ global _∼_ Uniform(M). 

- 3: Get ego-poses _{_ **T** _t}_<sup>_T_</sup> _t_ =1<sup>used to build</sup><sup>_M_globalin Alg. 2.</sup> 

- 4: Randomly select initial ego pose **T**<sup>ego</sup> 0 _∼_ Uniform( _{_ **T** _t}_<sup>_T_</sup> _t_ =1<sup>).</sup> 5: Find **T** fwd and **T** bwd at distance _±d_ pre along _{_ **T** _t}t_<sup>_T_</sup> =1<sup>from</sup><sup>**T**ego</sup> 0<sup>.</sup> 

- 6: _A ←_ SpawnAgents( **T**<sup>ego</sup> 0<sup>_,_True)</sup><sup>_∪_SpawnAgents(</sup><sup>**T**fwd)</sup><sup>_∪_SpawnAgents(</sup><sup>**T**bwd)</sup> 

- 7: // Phase 2: Closed-Loop Simulation 

- 8: ∆ _d_ ego _←_ 0 _, S_ out _←∅ ▷_ Init movement tracker and empty sequence for frames 

- 9: **for** _t_ = 1 _. . . ϕ_ **do** 

- 10: // Step 2.1: Rolling Horizon Update 

11: ∆ _d_ ego _←_ ∆ _d_ ego + _v_ ego<sup>(</sup><sup>_t_)∆</sup><sup>_t_</sup> 

- 12: **if** ∆ _d_ ego _≥ d_ roll **then** 13: _A ←{a ∈A |_ **p** _a ∈_ FOV( **T**<sup>ego</sup> _t_ ) _} ▷_ Remove out-of-view agents 14: **T** fwd _←_ Pose ahead of **T**<sup>ego</sup> _t_ by _d_ pre, **T** bwd _←_ Pose behind of **T** _t_<sup>ego</sup> by _d_ pre 15: _A ←A ∪_ SpawnAgents( **T** fwd) _∪_ SpawnAgents( **T** bwd) 16: ∆ _d_ ego _←_ 0 

- 17: // Step 2.2: IDM Kinematics & Route Execution 

18: **for** each agent _a ∈A_ parameterized by state ( **p** _a,_ **h** _a, va, π_ traj _,_ **p** target) **do** 19: Let **h** _a_ denote the heading unit vector of agent _a_ . 20: _Ca ←_ � _a_<sup>_′_</sup> _∈A \ {a}_ ��� <u>(</u> _∥_ **<u>pp</u>** _<u>a′a−′</u> −_ **<u>pp</u>** _aa_ <u>)</u> _·∥_ **h** 2 _a_<sup>_>_0</sup><sup>_._5</sup><sup>_∧_Dist(</sup><sup>**p**</sup><sup>_a′, π_traj)</sup><sup>_< d_lat</sup> � 21: _a_ lead _←_ arg min _a′∈Ca ∥_ **p** _a′ −_ **p** _a∥_ 2 _▷_ Select out the agent ahead of current a 22: _s ←∥_ **p** _a_ lead _−_ **p** _a∥_ 2, ∆ _v ← va − v_ lead _▷_ adjusted if head-on 23: **if** _s < d_ lc **and** (∆ _v >_ 0 **or h** _a ·_ **h** _a_ lead _< −_ 0 _._ 5) **then** 24: **p** adj _←_ SearchParallelLane( **p** _a, L_ final) 25: **if p** adj _̸_ = _∅_ **then** 26: _π_ bezier _←_ BezierCurve( **p** _a,_ **p** adj) _▷_ Generate smooth transition 27: _π_ new _←_ A-Star( _L_ final _,_ **p** adj _,_ **p** target) _▷_ Re-route from adjacent lane 28: _π_ traj _← π_ bezier _⊕ π_ new _▷_ Concatenate trajectories 29: _a_ acc _←_ IDM( _va, v_ des _,_ ∆ _v, s_ ) _▷_ Compute acceleration 30: **p** _a ←_ Advance( **p** _a, π_ traj _, va_ ∆ _t_ ) _▷_ Move along trajectory 

   - Concatenate trajectories 

      - Compute acceleration 

      - Move along trajectory 

- 31: // Step 2.3: Rendering 32: _A_ vis _←{a ∈A |_ **p** _a ∈_ FOV( **T**<sup>ego</sup> _t_ ) _}_ 33: _O_ **T**<sup>(</sup><sup>_t_)</sup><sup>_←_Crop(</sup><sup>_M_global</sup><sup>_,_</sup><sup>**T**</sup> _t_<sup>ego</sup> ) 34: _X_<sup>(</sup><sup>_t_)</sup> _←_<sup>�</sup> _a∈A_ vis<sup>Φrigid(</sup><sup>_§a,_</sup><sup>**p**</sup><sup>_a,_</sup><sup>**h**</sup><sup>_a_)</sup> 35: _M_<sup>(</sup> local<sup>_t_)</sup><sup>_←O_</sup> **T**<sup>(</sup><sup>_t_)⊛</sup><sup>_X_(</sup><sup>_t_)</sup> 36: _S_ out _←S_ out _∪{M_<sup>(</sup> local<sup>_t_)</sup><sup>_}_</sup> 

         - Filter visible agents in current view 

            - Extract static local background 

      - Transform and aggregate dynamic assets 

   - Overlay foreground onto static background 

         - Append rendered frame to sequence 

- 37: **return** _S_ out 

32 

## **References** 

- [1] Niket Agarwal, Arslan Ali, Maciej Bala, Yogesh Balaji, Erik Barker, Tiffany Cai, Prithvijit Chattopadhyay, Yongxin Chen, Yin Cui, Yifan Ding, et al. Cosmos world foundation model platform for physical ai. _arXiv preprint arXiv:2501.03575_ , 2025. 

- [2] Hengwei Bian, Lingdong Kong, Haozhe Xie, Liang Pan, Yu Qiao, and Ziwei Liu. Dynamiccity: Large-scale 4d occupancy generation from dynamic scenes. _arXiv preprint arXiv:2410.18084_ , 2024. 

- [3] Holger Caesar, Juraj Kabzan, Kok Seang Tan, Whye Kit Fong, Eric Wolff, Alex Lang, Luke Fletcher, Oscar Beijbom, and Sammy Omari. nuplan: A closed-loop ml-based planning benchmark for autonomous vehicles. _arXiv preprint arXiv:2106.11810_ , 2021. 

- [4] Qifeng Chen, Sheng Yang, Sicong Du, Tao Tang, Rengan Xie, Peng Chen, and Yuchi Huo. Lidar-gs: Real-time lidar re-simulation using gaussian splatting. _arXiv preprint arXiv:2410.05111_ , 2024. 

- [5] Kashyap Chitta, Daniel Dauner, and Andreas Geiger. Sledge: Synthesizing driving environments with generative models and rule-based traffic. In _European Conference on Computer Vision_ , pages 57–74. Springer, 2024. 

- [6] Felipe Codevilla, Antonio M Lopez, Vladlen Koltun, and Alexey Dosovitskiy. On offline evaluation of vision-based driving models. In _Proceedings of the European conference on computer vision (ECCV)_ , pages 236–251, 2018. 

- [7] Daniel Dauner, Marcel Hallgarten, Tianyu Li, Xinshuo Weng, Zhiyu Huang, Zetong Yang, Hongyang Li, Igor Gilitschenski, Boris Ivanovic, Marco Pavone, et al. Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking. _Advances in Neural Information Processing Systems_ , 37:28706–28719, 2024. 

- [8] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. Carla: An open urban driving simulator. In A. D. Dragan, M. Hebert, and S. Levine, editors, _Proceedings of the 1st Annual Conference on Robot Learning_ , volume 78 of _Proceedings of Machine Learning Research_ , pages 1–16, Mountain View, CA, USA, 13–15 Nov 2017. PMLR. URL http://proceedings.mlr.press/v78/dosovitskiy17a.html. 

- [9] Dan Friedman and Adji Bousso Dieng. The vendi score: A diversity evaluation metric for machine learning. _arXiv preprint arXiv:2210.02410_ , 2022. 

- [10] Shenyuan Gao, Jiazhi Yang, Li Chen, Kashyap Chitta, Yihang Qiu, Andreas Geiger, Jun Zhang, and Hongyang Li. Vista: A generalizable driving world model with high fidelity and versatile controllability. _Advances in Neural Information Processing Systems_ , 37:91560–91596, 2024. 

- [11] Songen Gu, Wei Yin, Bu Jin, Xiaoyang Guo, Junming Wang, Haodong Li, Qian Zhang, and Xiaoxiao Long. Dome: Taming diffusion model into high-fidelity controllable occupancy world model. _arXiv preprint arXiv:2410.10429_ , 2024. 

- [12] Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Dollár, and Ross Girshick. Masked autoencoders are scalable vision learners. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 16000–16009, 2022. 

- [13] Jonathan Ho and Tim Salimans. Classifier-free diffusion guidance. _arXiv preprint arXiv:2207.12598_ , 2022. 

- [14] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 

- [15] Xiaotao Hu, Wei Yin, Mingkai Jia, Junyuan Deng, Xiaoyang Guo, Qian Zhang, Xiaoxiao Long, and Ping Tan. Drivingworld: Constructing world model for autonomous driving via video gpt. _arXiv preprint arXiv:2412.19505_ , 2024. 

- [16] Arne Kesting, Martin Treiber, and Dirk Helbing. Enhanced intelligent driver model to access the impact of driving strategies on traffic capacity. _Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences_ , 368(1928):4585–4605, 2010. 

- [17] Jumin Lee, Sebin Lee, Changho Jo, Woobin Im, Juhyeong Seon, and Sung-Eui Yoon. SemCity: Semantic scene generation with triplane diffusion. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 28337–28347, 2024. 

- [18] Bohan Li, Jiazhe Guo, Hongsi Liu, Yingshuang Zou, Yikang Ding, Xiwu Chen, Hu Zhu, Feiyang Tan, Chi Zhang, Tiancai Wang, et al. Uniscene: Unified occupancy-centric driving scene generation. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 11971–11981, 2025. 

33 

- [19] Zhimin Liao, Ping Wei, Ruijie Zhang, Shuaijia Chen, Haoxuan Wang, and Ziyang Ren. I2-world: Intra-inter tokenization for efficient dynamic 4d scene forecasting. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 25810–25819, 2025. 

- [20] Tianran Liu, Shengwen Zhao, and Nicholas Rhinehart. Towards foundational lidar world models with efficient latent flow matching. _arXiv preprint arXiv:2506.23434_ , 2025. 

- [21] Yifan Lu, Xuanchi Ren, Jiawei Yang, Tianchang Shen, Zhangjie Wu, Jun Gao, Yue Wang, Siheng Chen, Mike Chen, Sanja Fidler, et al. Infinicube: Unbounded and controllable dynamic 3d driving scene generation with world-guided video models. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 27272–27283, 2025. 

- [22] Andreas Lugmayr, Martin Danelljan, Andres Romero, Fisher Yu, Radu Timofte, and Luc Van Gool. Repaint: Inpainting using denoising diffusion probabilistic models. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 11461–11471, 2022. 

- [23] Xin Ma, Yaohui Wang, Xinyuan Chen, Gengyun Jia, Ziwei Liu, Yuan-Fang Li, Cunjian Chen, and Yu Qiao. Latte: Latent diffusion transformer for video generation. _arXiv preprint arXiv:2401.03048_ , 2024. 

- [24] William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 4195–4205, 2023. 

- [25] Xuanchi Ren, Yifan Lu, Tianshi Cao, Ruiyuan Gao, Shengyu Huang, Amirmojtaba Sabour, Tianchang Shen, Tobias Pfaff, Jay Zhangjie Wu, Runjian Chen, et al. Cosmos-drive-dreams: Scalable synthetic driving data generation with world foundation models. _arXiv preprint arXiv:2506.09042_ , 2025. 

- [26] Luke Rowe, Roger Girgis, Anthony Gosselin, Liam Paull, Christopher Pal, and Felix Heide. Scenario dreamer: Vectorized latent diffusion for generating driving simulation environments. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 17207–17218, 2025. 

- [27] Lloyd Russell, Anthony Hu, Lorenzo Bertoni, George Fedoseev, Jamie Shotton, Elahe Arani, and Gianluca Corrado. Gaia-2: A controllable multi-view generative world model for autonomous driving. _arXiv preprint arXiv:2503.20523_ , 2025. 

- [28] Yining Shi, Kun Jiang, Qiang Meng, Ke Wang, Jiabao Wang, Wenchao Sun, Tuopu Wen, Mengmeng Yang, and Diange Yang. Come: Adding scene-centric forecasting control to occupancy world model. _arXiv preprint arXiv:2506.13260_ , 2025. 

- [29] Haoming Song, Delin Qu, Yuanqi Yao, Qizhi Chen, Qi Lv, Yiwen Tang, Modi Shi, Guanghui Ren, Maoqing Yao, Bin Zhao, et al. Hume: Introducing system-2 thinking in visual-language-action model. _arXiv preprint arXiv:2505.21432_ , 2025. 

- [30] Xiaoyu Tian, Tao Jiang, Longfei Yun, Yucheng Mao, Huitong Yang, Yue Wang, Yilun Wang, and Hang Zhao. Occ3d: A large-scale 3d occupancy prediction benchmark for autonomous driving. _Advances in Neural Information Processing Systems_ , 36:64318–64330, 2023. 

- [31] Aaron Van Den Oord, Oriol Vinyals, et al. Neural discrete representation learning. _Advances in neural information processing systems_ , 30, 2017. 

- [32] Eugene Vinitsky, Nathan Lichtlé, Xiaomeng Yang, Brandon Amos, and Jakob Foerster. Nocturne: a scalable driving benchmark for bringing multi-agent learning one step closer to the real world. _Advances in Neural Information Processing Systems_ , 35:3962–3974, 2022. 

- [33] Yuping Wang, Xiangyu Huang, Xiaokang Sun, Mingxuan Yan, Shuo Xing, Zhengzhong Tu, and Jiachen Li. Uniocc: A unified benchmark for occupancy forecasting and prediction in autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 25560–25570, 2025. 

- [34] Julong Wei, Shanshuai Yuan, Pengfei Li, Qingda Hu, Zhongxue Gan, and Wenchao Ding. Occllama: An occupancylanguage-action generative world model for autonomous driving. _arXiv preprint arXiv:2409.03272_ , 2024. 

- [35] Haihong Xiao, Jianan Zou, Yuxin Zhou, Ying He, and Wenxiong Kang. Splatco: Structure-view collaborative gaussian splatting for detail-preserving rendering of large-scale unbounded scenes. _arXiv preprint arXiv:2505.17951_ , 2025. 

- [36] Zhexiao Xiong, Xin Ye, Burhan Yaman, Sheng Cheng, Yiren Lu, Jingru Luo, Nathan Jacobs, and Liu Ren. Unidrive-wm: Unified understanding, planning and generation world model for autonomous driving. _arXiv preprint arXiv:2601.04453_ , 2026. 

34 

- [37] Tianyi Yan, Dongming Wu, Wencheng Han, Junpeng Jiang, Xia Zhou, Kun Zhan, Cheng-zhong Xu, and Jianbing Shen. Drivingsphere: Building a high-fidelity 4d world for closed-loop simulation. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 27531–27541, 2025. 

- [38] Jiazhi Yang, Kashyap Chitta, Shenyuan Gao, Long Chen, Yuqian Shao, Xiaosong Jia, Hongyang Li, Andreas Geiger, Xiangyu Yue, and Li Chen. Resim: Reliable world simulation for autonomous driving. _arXiv preprint arXiv:2506.09981_ , 2025. 

- [39] Xuemeng Yang, Licheng Wen, Tiantian Wei, Yukai Ma, Jianbiao Mei, Xin Li, Wenjie Lei, Daocheng Fu, Pinlong Cai, Min Dou, et al. Drivearena: A closed-loop generative simulation platform for autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 26933–26943, 2025. 

- [40] Yu Yang, Alan Liang, Jianbiao Mei, Yukai Ma, Yong Liu, and Gim Hee Lee. X-scene: Large-scale driving scene generation with high fidelity and flexible controllability. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 

- [41] Ze Yang, Yun Chen, Jingkang Wang, Sivabalan Manivasagam, Wei-Chiu Ma, Anqi Joyce Yang, and Raquel Urtasun. Unisim: A neural closed-loop sensor simulator. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 1389–1399, 2023. 

- [42] Kaiwen Zhang, Zhenyu Tang, Xiaotao Hu, Xingang Pan, Xiaoyang Guo, Yuan Liu, Jingwei Huang, Li Yuan, Qian Zhang, Xiao-Xiao Long, et al. Epona: Autoregressive diffusion world model for autonomous driving. _arXiv preprint arXiv:2506.24113_ , 2025. 

- [43] Lingfeng Zhang, Yuecheng Liu, Zhanguang Zhang, Matin Aghaei, Yaochen Hu, Hongjian Gu, Mohammad Ali Alomrani, David Gamaliel Arcos Bravo, Raika Karimi, Atia Hamidizadeh, et al. Mem2ego: Empowering vision-language models with global-to-ego memory for long-horizon embodied navigation. _arXiv preprint arXiv:2502.14254_ , 2025. 

- [44] Lvmin Zhang, Anyi Rao, and Maneesh Agrawala. Adding conditional control to text-to-image diffusion models. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 3836–3847, 2023. 

- [45] Wenzhao Zheng, Weiliang Chen, Yuanhui Huang, Borui Zhang, Yueqi Duan, and Jiwen Lu. Occworld: Learning a 3d occupancy world model for autonomous driving. In _European conference on computer vision_ , pages 55–72. Springer, 2024. 

- [46] Hongyu Zhou, Longzhong Lin, Jiabao Wang, Yichong Lu, Dongfeng Bai, Bingbing Liu, Yue Wang, Andreas Geiger, and Yiyi Liao. Hugsim: A real-time, photo-realistic and closed-loop simulator for autonomous driving. _arXiv preprint arXiv:2412.01718_ , 2024. 

- [47] Xin Zhou, Dingkang Liang, Sifan Tu, Xiwu Chen, Yikang Ding, Dingyuan Zhang, Feiyang Tan, Hengshuang Zhao, and Xiang Bai. Hermes: A unified self-driving world model for simultaneous 3d scene understanding and generation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 27817–27827, 2025. 

35 

