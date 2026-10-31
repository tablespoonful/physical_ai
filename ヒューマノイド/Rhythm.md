---
title: "Rhythm: Learning Interactive Whole-Body Control for Dual Humanoids"
date: "2026-03-03"
authors: "Hongjin Chen; Wei Zhang; Pengfei Li; Shihao Ma; Ke Ma; Yujie Jin"
url: https://arxiv.org/abs/2603.02856
pdf: https://arxiv.org/pdf/2603.02856
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.02856)** / [論文ページ](https://arxiv.org/abs/2603.02856)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Rhythm: Learning Interactive Whole-Body Control for Dual Humanoids 

Hongjin Chen<sup>1,2,*</sup> Wei Zhang<sup>2,*</sup> Pengfei Li<sup>2,3,†</sup> Shihao Ma<sup>1,2</sup> Ke Ma<sup>1,2</sup> Yujie Jin<sup>2</sup> Zijun Xu<sup>1,5</sup> Xiaohui Wang<sup>1,2</sup> Yupeng Zheng<sup>6</sup> Zining Wang<sup>2</sup> Jieru Zhao<sup>4</sup> Yilun Chen<sup>2</sup> Wenchao Ding<sup>1,2,†</sup> 1Fudan University 2TARS Robotics 3Tsinghua University 4Shanghai Jiao Tong University 5Shanghai Innovation Institute 6Institute of Automation, Chinese Academy of Sciences 

> *Equal contribution †Corresponding Authors Project Page: https://hoshi-no-ai.github.io/Rhythm/ 


**Fig. 1:** The proposed framework, **Rhythm** , facilitates a spectrum of humanoid–humanoid interactions. **(a–c) Contact-Rich Interaction:** The method handles interactions ranging from light contact (Greeting) to intensive contact (Hug, Shoulder-to-Shoulder), maintaining fine-grained contact geometry without penetration (shown in the zoomed-in views). **(d) Coordinated Interaction:** The humanoids perform synchronized long-horizon dance ( _La La Land_ ), with trajectories showing consistent spatiotemporal alignment and stable relative positioning over time. 

**_Abstract_ —Realizing interactive whole-body control for multihumanoid systems is critical for unlocking complex collaborative capabilities in shared environments. Although recent** 

**advancements have significantly enhanced the agility of individual robots, bridging the gap to physically coupled multihumanoid interaction remains challenging, primarily due to** 

**severe kinematic mismatches and complex contact dynamics. To address this, we introduce Rhythm, the first unified framework enabling real-world deployment of dual-humanoid systems for complex, physically plausible interactions. Our framework integrates three core components: (1) an Interaction-Aware Motion Retargeting (IAMR) module that generates feasible humanoid interaction references from human data; (2) an InteractionGuided Reinforcement Learning (IGRL) policy that masters coupled dynamics via graph-based rewards; and (3) a real-world deployment system that enables robust transfer of dual-humanoid interaction. Extensive experiments on physical Unitree G1 robots demonstrate that our framework achieves robust interactive whole-body control, successfully transferring diverse behaviors such as hugging and dancing from simulation to reality.** 

## I. INTRODUCTION 

Humanoid robotics has witnessed rapid evolution, achieving remarkable milestones in single-agent capabilities. Recent research has established a strong foundation in dynamic locomotion [12, 19, 23, 40, 48] and general whole-body control [8, 17, 22, 26, 36, 55], significantly enhancing the agility and robustness of individual robots. However, the broader vision of embodied intelligence necessitates agents that can operate beyond isolation [5, 37]. Realizing multi-agent systems capable of physical collaboration represents a critical next step. Yet, research in this domain remains disproportionately focused on single-robot tasks. 

Despite growing interest in multi-agent interaction, current solutions are largely confined to virtual environments or simplified humanoid-object interactions. In computer graphics, physics-based animation has achieved realistic simulations of multi-character interactions [10, 25, 45, 50, 54], yet these methods often prioritize visual fidelity over the strict physical constraints necessary for real-world robotic deployment. 

In robotics, although human–robot collaboration [9, 20] and competitive sports in structured environments [28, 39, 47] have been explored, these typically involve a compliant human partner or passive objects. Research explicitly targeting multi-humanoid interaction remains scarce, and existing works are predominantly validated only in simulation [29]. Consequently, achieving robust, physically coupled wholebody control on real multi-humanoid hardware remains an unbridged gap in the field. 

Two fundamental challenges hinder the Sim-to-Real transition for dual-humanoid systems: (1) the scarcity of feasible interaction data; and (2) the complexity of the training-todeployment paradigm. First, acquiring high-quality interaction references is non-trivial. Directly transferring _Human-Human Interaction_ [38, 41, 45, 46] data to robots introduces severe kinematic conflicts due to morphological differences between humans and humanoids (see Sec. III-A). Standard retargeting methods [3, 30, 49] struggle to preserve both individual motion style and precise interaction geometry, yielding suboptimal motion references. Second, the learning and deployment pipeline presents significant hurdles. Existing tracking policies [26, 44, 52] typically treat agents as isolated entities, failing to model the intricate coupled dynamics essential for close interaction. Meanwhile, a significant disparity exists 

between the global observability available in simulation and the asynchronous, ego-centric, partially observable reality of real hardware, making the deployment unstable. 

To address these challenges, we introduce **Rhythm** (Interactive <u>Whole-Body</u> Control for Dual <u>Humanoids),</u> a unified framework designed to empower dual humanoids to execute complex, physically plausible interactions in realworld scenarios. The framework explicitly models interaction geometry and physical contact to achieve high-fidelity coupled behaviors. First, to resolve kinematic conflicts in reference generation, we introduce **Interaction-Aware Motion Retargeting (IAMR)** . By explicitly modeling interaction geometry and utilizing distance-aware dynamic weighting, this module adaptively balances self-motion fidelity with interaction geometry. The resulting geometrically consistent references serve as a crucial prior, laying the physical foundation for the subsequent training phase. Building upon this, we develop **Interaction-Guided Reinforcement Learning (IGRL)** to master the complex dual-agent dynamics. This module directly leverages the interaction geometry and contact preserved by IAMR through explicit graph-based rewards, guiding agents to learn synchronized and robust behaviors. Finally, to realize dual-humanoid interactive whole-body control in the real world, we implement a relative state estimation and inter-agent synchronization scheme, effectively bridging the gap between global simulation and ego-centric reality. 

Fig. 1 illustrates the robustness of our framework in realworld scenarios, successfully handling tasks ranging from intensive contacts to synchronized long-horizon dancing. Our main contributions are summarized as follows: 

- We propose **Rhythm** , a unified framework for wholebody dual-humanoid interaction that, to our knowledge, achieves the first successful **robust transfer** of complex interactive behaviors to physical hardware. 

- We develop **IAMR** to resolve kinematic conflicts and generate humanoid-humanoid interaction motion references. Furthermore, we release **MAGIC** , the <u>Multi-</u> Humanoid Geometric Interaction Dataset, offering paired raw and retargeted interaction data. 

- We introduce **IGRL** , a multi-agent learning module that masters coupled interaction dynamics. By incorporating graph-based rewards, it enables agents to learn robust, physically consistent interactive behaviors. 

- We conduct extensive experiments on Unitree G1 humanoids in simulation and on physical hardware. Quantitative and qualitative evaluations across diverse interaction tasks demonstrate the superior performance and robustness of our framework. 

## II. RELATED WORK 

_A. Learning-Based Humanoid Control and Interaction_ 

Learning-based whole-body control methods primarily leverage Reinforcement Learning (RL) to endow humanoid robots with diverse motor skills [2, 4, 15–19, 24, 33, 40, 48, 52, 53]. Existing research largely focuses on single-agent 

motion tracking [17, 44, 53], progressing from mimicking specific references to general motion tracking frameworks [7, 13, 26, 52, 55]. Beyond isolation, recent works have addressed the interaction between humanoids and environmental factors in sports such as table tennis [39], badminton [28], and soccer [34, 47], as well as human-robot collaboration [6, 9, 20]. However, these scenarios typically model the partner (human or object) as a passive entity or an external disturbance, ignoring the complex coupled dynamics inherent in multi-agent systems. Achieving interactive whole-body control on dual-humanoid hardware requires moving beyond these assumptions to explicitly model the mutual physical influence and geometric topology between active agents—a capability that remains absent in current robotics literature. 

## _B. Physics-Based Animation of Human-Human Interaction_ 

While robotics research focuses on hardware feasibility, the computer graphics community has expanded the scope of humanoid animation from single-agent generation [30–32] to the complex domain of _Human-Human Interaction_ [38, 41, 46]. Addressing the inevitable physical artifacts caused by sensor inaccuracies in existing datasets [11, 25, 45, 51], recent works [10, 43, 50, 54] employ RL within physics-based simulations to guarantee human-like behavior and physical plausibility. However, these methods prioritize visual fidelity over dynamic feasibility, often relaxing rigorous constraints essential for real robots. Policies trained in these idealized environments struggle with the Sim-to-Real gap. To bridge this gap, we propose **Rhythm** , which, to our knowledge, represents the first demonstration of physically coupled dual-humanoid interaction on real-world hardware. 

## _C. Motion Retargeting for Humanoid_ 

Motion retargeting serves as a fundamental bridge for transferring human skills to humanoids. However, standard approaches like PHC [30] and GMR [3] typically treat agents in isolation, neglecting interaction behaviors. While OmniRetarget [49] advances this by employing _Interaction Meshes_ [1, 56] to enforce human-object interaction constraints, its applicability is restricted to single-humanoid settings. Extending this to human-human interaction presents unique challenges. Recent attempts, such as PAIR [20] and Harmanoid [29], adopt a coupled formulation that intertwines self-motion with interaction constraints. Consequently, in the presence of inherent kinematic conflicts, they often compromise self-motion fidelity (e.g., causing unnatural distortions) to strictly enforce interaction geometry. To address this, we propose IAMR that effectively mitigates these kinematic conflicts to produce highfidelity coupled motion references. 

## III. METHODS 

As illustrated in Fig. 2, **Rhythm** addresses the challenge of dual-humanoid interaction through three tightly integrated components: 1) **Interaction-Aware Motion Retargeting (IAMR)** , which synthesizes physically feasible priors by decoupling interaction geometry from self-motion fidelity 

(Sec. III-A); 2) **Interaction-Guided Reinforcement Learning (IGRL)** , which captures coupled dynamics via topology-aware rewards that enforce interaction consistency (Sec. III-B); and 3) **Real-World Deployment** , which overcomes the limitations of noisy global observability and asynchronous execution to bridge the Sim-to-Real gap (Sec. III-C). 

## _A. Interaction-Aware Motion Retargeting (IAMR)_ 

_1) Problem Formulation:_ Given a source motion sequence of two human demonstrators with different anthropometry, our goal is to synthesize kinematically feasible trajectories for two humanoids. The core challenge lies in synthesizing motions that simultaneously preserve the individual motion style and the dense interaction geometry. 

**Interaction Mesh and Laplacian Coordinates.** To mathematically model the coupled multi-agent system, we adopt the volumetric Interaction Mesh formalism [1, 56]. We represent the system as a connected graph _G_ = ( _V, E_ ), comprising a vertex set _V_ of the agents’ key joints and an edge set _E_ encoding their structural connections. To encode local geometric details, we utilize Laplacian coordinates. For a vertex _pi_ , the Laplacian operator _L_ ( _·_ ) computes the deviation from the weighted average of its neighbors _N_ ( _i_ ): 


where _cij_ denotes the normalized weights. In mesh-based motion retargeting, the objective is to find a target configuration _q_ such that the local geometry of the retargeted vertices _pi_ ( _q_ ) matches the source reference. This is achieved by minimizing the deformation energy<sup>�</sup> _∥L_ ( _pi_ ( _q_ )) _−L_ ( _p_<sup>_src_</sup> _i_ ) _∥_<sup>2</sup> . **The Kinematic Conflict.** While the standard formulation � _∥L_ ( _pi_ ( _q_ )) _−L_ ( _psrci_ ) _∥_<sup>2</sup> is effective for single-agent editing, applying it to the transfer from heterogeneous humans to homogeneous robots creates a fundamental ambiguity in defining the source reference _V_<sup>_src_</sup> . Due to the embodiment mismatch, no single reference manifold can simultaneously satisfy both self-motion and interaction constraints: 

- **Individual Manifold (** _Mind_ **):** Constructed by scaling each human with individual ratios to match the robot’s height. Using this as _V_<sup>_src_</sup> preserves valid self-motion Laplacian coordinates but structurally disrupts the relative interaction geometry (e.g., causing “air handshakes”). 

- **Unified Manifold (** _Muni_ **):** Constructed by applying a single global scale to the entire scene. Using this as _V_<sup>_src_</sup> strictly preserves relative interaction edges but forces the robots to adopt kinematic constraints incompatible with their morphology (e.g., foot floating). 

**Topological Partitioning.** To resolve this conflict, we propose to relax the monolithic structure of the standard Interaction Mesh. Instead of treating the system as a single deformable body, we explicitly partition _E_ into two disjoint functional groups, as visualized in the left part of Fig. 2: (1) **IntraAgent Edges (** _Eself_ **):** Edges connecting joints within a single 


**Fig. 2: Overview of Rhythm.** IAMR utilizes decoupled optimization to generate high-quality humanoid-humanoid motion interaction references from human demonstrations. Guided by these references, IGRL employs MAPPO and graph-based rewards to learn robust coupled dynamics. Finally, the deployment module facilitates Sim-to-Real transfer via Lidar-fused state estimation and inter-agent synchronization. 

robot, encoding the local self-motion topology. (2) **InterAgent Edges (** _Einter_ **):** Edges connecting key joints between the two robots, encoding the relative interaction topology. 

This topological decomposition allows us to assign distinct geometric references to different semantic parts of the graph, forming the basis for our decoupled optimization scheme. 

_2) Decoupled Optimization:_ Leveraging the topological partitioning defined above, we resolve the kinematic conflict by assigning distinct geometric references to the partitioned subgraphs. We formulate the retargeting as a dynamic spring system, where a self-motion term _Eself_ ensures intra-agent edges _Eself_ track the Independent Manifold _Mind_ , while an interaction term _Einter_ constrains inter-agent edges _Einter_ to the Unified Manifold _Muni_ . 

We solve for the optimal joint configuration _q_<sup>_∗_</sup> = _{q_ 1 _, q_ 2 _}_ by minimizing a hybrid energy function: 


where _Cphy_ represents the set of feasible configurations satisfying joint limits and collision constraints. 

**Self-Motion Objective (** _Eself_ **).** To preserve individual motion quality, we align the Laplacian geometry of each robot to its Independent Reference _Mind_ , strictly confining the operator to the local subgraph: 


where _Va_ denotes the vertex set of robot _a_ , and _p_<sup>_ind_</sup> _i_ represents the corresponding vertex position in the reference _Mind_ . For 

rotation, _Ba_ denotes the key links, where _⊖_ measures the geodesic distance on _SO_ (3) between the current orientation _θk_ and the reference _θ_<sup>ˆ</sup> _k_<sup>_src_.</sup> 

**Interaction Objective (** _Einter_ **).** To enforce the relative interaction geometry, we treat the inter-agent edges as extrinsic constraints driven by the Unified Reference _Muni_ . We formulate this as a variable-stiffness spring potential: 


Here, _pi_ and _pj_ denote the current vertex positions of different agents, while _p_ ˆ<sup>_uni_</sup> _i_ and _p_ ˆ<sup>_uni_</sup> _j_ represent the corresponding target coordinates derived from the reference _Muni_ . To naturally prioritize close-range geometry (e.g., contact) over distant relations, we define the stiffness _ωij_ as a continuous exponential decay function of the source distance _dij_ : 


where _ωmax_ denotes peak stiffness and _γ_ the decay rate. This effectively models the interaction as a non-linear spring system that stiffens during close contact to prevent penetration, while becoming compliant at a distance to allow free motion. **Topological Interaction Priors.** Beyond kinematic trajectories, IAMR explicitly extracts inter-agent topological structures to serve as interaction priors for downstream policy learning, as illustrated in the left part of Fig. 2. We generate two cross-agent graph representations: (1) An **Interaction Graph** (derived from _Einter_ ), which encodes the binary connectivity _bridging_ the keypoints of the two agents [54]; (2) A **Contact Graph** (constructed via collision detection), which records the binary physical contact states _between_ the links of the 

two distinct robots [42]. These graphs provide the essential interaction topology required for the graph-based rewards in the subsequent training phase. 

## _B. Interaction-Guided Reinforcement Learning (IGRL)_ 

To master the coupled dynamics of dual-humanoid interaction, we propose **IGRL** , a multi-agent reinforcement learning module. Unlike standard motion tracking policies that treat agents as isolated entities, IGRL explicitly models interaction geometry through graph-based rewards and incorporates specific training strategies to bridge the reality gap. 

_1) Multi-Agent Policy Design:_ As shown in the middle part of Fig. 2, we formulate the problem as a Multi-Agent Markov Decision Process (MA-MDP) and adopt the _Centralized Training with Decentralized Execution_ (CTDE) paradigm using MAPPO [10, 27]. 

**Interaction-Centric Observation.** Effective collaboration requires a comprehensive awareness of both self and partner states. The policy operates on a compact observation space _ot_ = _{oprop, opeer, oref }_ : 

- Proprioception ( _oprop_ ): Defines the agent’s internal state, including joint positions, velocities, base angular velocities, and the previous action. 

- Peer Perception ( _opeer_ ): Encodes the peer’s state relative to the ego agent. It includes the peer’s joint positions and the relative root transform expressed in the ego-centric frame: the relative position _Prel_ = _Rego_<sup>_T_(</sup><sup>_Ppeer−Pego_)</sup> and orientation _Rrel_ = _Rego_<sup>_TRpeer_.Thisexplicitspatial</sup> formation enables the agent to anticipate and handle coupled dynamics. 

- Reference Motion ( _oref_ ): Contains the future reference trajectories and the reference relative state, serving as the correct interaction topology. 

**Network Architecture.** We design a hierarchical policy architecture where 1D-CNN temporal encoders process historical observations and future references, feeding latent features along with the current observation into an MLP action decoder. More details are provided in Appendix B. 

**Robust Training Strategy.** To ensure transferability and handle complex interaction phases, we implement two strategies, with mathematical formulations provided in Appendix B: 

- **Curriculum-based Adaptive Sampling:** Standard RSI [31] relies on sparse failure counts, neglecting nonterminal interaction violations. We propose an erroraware sampling strategy based on a multi-objective landscape composed of integrating failure, tracking, and interaction metrics. The curriculum dynamically evolves from prioritizing stability in early stages to focusing on tracking and interaction precision as the policy matures. 

- **Dual-Agent Domain Randomization:** To bridge the sim-to-real gap, we simulate wireless latency via noisy, delayed peer observations and apply initial state perturbations to enforce recovery from physical misalignment. 

_2) Graph-based Rewards:_ Standard tracking rewards typically treat agents as isolated entities, failing to enforce topological consistency or capture coupled dynamics. To bridge this gap, we introduce graph-based rewards to **guide** the learning of dynamic control policies by translating the _Topological Interaction Priors_ established in IAMR, as shown in Fig. 2. **Interaction Graph Reward (** _rinter_ **).** To ensure precise relative geometry during interaction, we penalize deviations of the _interaction graph_ . The reward is formulated as: 


where _σinter_ is a sensitivity scaling factor, and _dij_ denotes the relative position vector connecting joints _i_ and _j_ in the simulation ( _sim_ ) and reference ( _ref_ ) states. By inheriting the distance-aware dynamic weights _ωij_ from IAMR, the policy inherently learns to prioritize the same geometric constraints that were optimized during retargeting. 

**Contact Graph Reward (** _rcontact_ **).** Since kinematic references lack force information, we utilize _contact graph_ to regularize physical interaction. This reward is designed with two goals: (1) _Contact Consistency_ , which penalizes mismatches between the simulated and reference contact states; and (2) _Force Regularization_ , which constrains contact forces to realistic ranges when active, and penalizes non-zero forces during non-contact phases. This explicitly discourages interpenetration and encourages compliant physical interaction. 

## _C. Real-World Deployment_ 

Deploying **Rhythm** on physical hardware faces the _Sim-toReal Gap_ , specifically the lack of global observability and the issue of asynchronous execution. 

_1) State Estimation and Relative Localization:_ Constructing the observation space for dual-humanoid interaction requires precise global and relative state information. We employ a robust localization system, utilizing _POINT-LIO_ [14] for high-frequency local odometry and _GICP_ [35] to register realtime point clouds against a pre-built map for drift-free global positioning. A Kalman Filter fuses these estimates to ensure robustness under highly dynamic motions. 

Robots broadcast global poses _{P, R}_ via _LCM_ [21]. The ego-agent transforms received data into its local frame to derive _{Prel, Rrel}_ , enabling real-time reconstruction of _opeer_ consistent with the simulation. 

_2) Inter-Agent Synchronization:_ We use the _motion phase ϕ_ [31] as the continuous variable representing the temporal execution progress of the interaction policy. In distributed settings, inherent hardware clock drift inevitably causes the phases of the two agents to diverge over time. 

To maintain temporal alignment, we implement a soft synchronization mechanism based on proportional feedback. Agents exchange their current phase _ϕ_ via the wireless bridge. Upon receiving the peer’s phase _ϕpeer_ , the ego agent dynamically modulates its phase progression rate _ϕ_<sup>˙</sup> _ego_ . Instead of a 


**Fig. 3: Overview of MAGIC.** MAGIC contains _∼_ 3 hours of high-fidelity interaction data balanced across five semantic categories (inner chart). Representative snapshots (outer ring) illustrate the diversity ranging from loose spatiotemporal coordination to intensive contact. 

fixed increment ( _ϕ_<sup>˙</sup> _base_ = 1 _._ 0), we apply a correction: 

## _ϕ_ ˙ _ego_ = 1 _._ 0 + _k_ ( _ϕpeer − ϕego_ ) _,_ 

where _k_ is the synchronization gain. This compensates for temporal drift by modulating execution rate, ensuring smooth alignment without the discontinuities of hard phase resets. 

## IV. EXPERIMENTS 

We design our experiments to systematically validate the proposed framework by answering three core questions: 

- **Q1 (Retargeting Quality):** Can IAMR synthesize kinematically feasible and topologically consistent trajectories that preserve the interaction geometry of the source data? 

- **Q2 (Policy Efficacy):** Can IGRL utilize the interaction guidance to capture the coupled dynamics, overcoming the limitations of treating agents as isolated entities? 

- **Q3 (Real-World Robustness):** Can the learned policies be successfully deployed to physical dual-humanoid systems, overcoming the limitations of noisy global observability and asynchronous communication? 

## _A. The MAGIC Dataset_ 

High-quality motion data is the cornerstone of learning interactions. Addressing the lack of clean human-human interaction data, we introduce **MAGIC** , a high-fidelity motion capture dataset comprising _∼_ 3 hours of valid motion sequences. 

_1) Acquisition and Diversity:_ Distinct from existing datasets [11, 25, 45, 51], we ensured physical plausibility for robot transfer through _Anthropometric Consistency_ (matched actor heights) and _Temporal Continuity_ (long-horizon sequences _>_ 10s). As illustrated in Fig. 3, MAGIC covers 

a diverse semantic spectrum: _Coordinated_ actions (30.4%), _Intimate/Care_ behaviors (24.8%), _Contact_ (18.2%), _Social Rituals_ (13.3%), and _Competitive_ interactions (13.3%). All sequences are captured via high-fidelity optical motion capture in BVH format. Interaction graphs are extracted from the interagent edges _Einter_ of the retargeted motion, while contact labels are derived post-retargeting via collision detection on the retargeted humanoid kinematics. 

_2) Data Release:_ To facilitate future research, we will publicly release both the raw motion capture data and the retargeted humanoid reference trajectories generated by IAMR. 

## _B. Experimental Setup_ 

**Datasets.** We use the proposed MAGIC dataset for both training and evaluation. To systematically assess performance across diverse physical dynamics, we categorize the tasks into three physics-based groups: **Collaborate** (non-contact synchronization), **Light Contact** (transient interaction), and **Intensive Contact** (continuous force transmission). Additionally, we employ the external _Inter-X_ dataset [45] to assess robustness under significant anthropometric mismatches. 

**Baselines.** We benchmark **Rhythm** against representative methods under two evaluation aspects, with full implementation details in Appendix C: 

- **Retargeting Quality (Q1):** We compare against **GMR** [3], which performs Cartesian optimization, **OR** [49], a single-agent interaction mesh method, and **DOR** , our constructed dual-agent extension of OR. 

- **Policy Efficacy (Q2):** To validate the effectiveness of IGRL, we compare against a **Single-Agent** (Status Quo) baseline that performs isolated tracking, as well as key ablated variants of our method, including **w/o Peer Obs** , **w/o Contact Rew** , and **w/o Interaction Rew** . 

**Evaluation Metrics.** We adopt task-specific evaluation metrics for **Retargeting Quality (Q1)** and **Policy Efficacy (Q2)** . For conciseness, detailed metric definitions and mathematical formulations are deferred to Appendix C. 

## _C. Retargeting Quality (Q1)_ 

We evaluate IAMR against baselines across three dimensions: **Safety** , measured by Inter-Penetration Rate (IPR) and Max Penetration Depth (MPD); **Fidelity** , quantified by Interaction Edge Error (IEE) and Contact F1 Score [20, 29]; and **Utility** , assessed via Downstream Success Rate (DSR). 

**Quantitative Analysis.** Table I presents the performance comparison across four interaction categories. We observe three key trends. First, isolated baselines (GMR, OR) fundamentally fail to ensure physical feasibility. Notably, in Intensive Contact, OR exhibits a prohibitive Inter-Penetration Rate (IPR) of 47.3%, rendering the motions physically infeasible and unsuitable for policy learning. Second, while the coupled baseline (DOR) guarantees safety (IPR=0), its rigid formulation compromises interaction fidelity under anthropometric mismatch. This is evident on the Inter-X dataset, where DOR’s F1-Strict drops to 0.589 due to its inability to reconcile conflicting kinematic constraints. In contrast, IAMR achieves 

**TABLE I: Quantitative Results of Retargeting.** Comparison across four interaction categories. Metrics include Safety (IPR, MPD), Fidelity (IEE, F1), and Utility (DSR). IAMR achieves the best balance, strictly eliminating penetration (IPR=0) while maximizing contact F1 scores. 

||**Sa**|**fety**|**F**|**idelity**|**Utility**|
|---|---|---|---|---|---|
||IPR(%)_↓_|MPD(cm)_↓_|IEE(%)_↓_|F1-S_↑_|F1-L_↑_DSR(%)_↑_|
|**_MAGIC: Co_**|**_llaborate_**|||||
|GMR|0.14|1.2|4.3|0.602|0.804<br>85.5|
|OR|0.20|1.4|4.1|0.747|0.902<br>87.4|
|DOR|**0.00**|**0.0**|3.9|0.711|0.899<br>**89.5**|
|**IAMR**|**0.00**|**0.0**|**3.7**|**0.785 **|**0.936**<br>89.0|
|**_MAGIC: Lig_**|**_ht Conta_**|**_ct_**||||
|GMR|2.18|3.3|4.6|0.738|0.893<br>48.5|
|OR|7.62|5.9|3.6|0.844|0.912<br>63.1|
|DOR|**0.00**|**0.0**|3.6|0.810|0.918<br>69.4|
|**IAMR**|**0.00**|**0.0**|**3.1**|**0.905 **|**0.935**<br>**75.3**|
|**_MAGIC: Int_**|**_ensive Co_**|**_ntact_**||||
|GMR|35.2|3.8|9.6|0.864|0.928<br>45.5|
|OR|47.3|5.3|8.0|0.884|0.929<br>56.5|
|DOR|**0.00**|**0.0**|7.8|0.883|0.925<br>63.3|
|**IAMR**|**0.00**|**0.0**|**6.6**|**0.932 **|**0.941**<br>**78.3**|
|**_Inter-X_**||||||
|GMR|11.7|1.7|8.0|0.598|0.752<br>31.7|
|OR|18.4|2.6|6.8|0.587|0.791<br>46.3|
|DOR|**0.00**|**0.0**|6.7|0.589|0.795<br>52.9|
|**IAMR**|**0.00**|**0.0**|**4.9**|**0.843 **|**0.860**<br>**69.9**|


**Fig. 4: Qualitative Visualization of Retargeting on Inter-X. Top:** Baselines suffer from contact loss (“air handshakes”), whereas IAMR preserves precise interaction geometry. **Bottom:** OR leads to severe penetration while DOR forces unnatural stiff postures; IAMR maintains close-proximity topology without collisions. 

the optimal safety-fidelity trade-off. By adaptively decoupling self-motion from interaction objectives, our method eliminates penetration while outperforming DOR by 43% in F1-Strict on Inter-X. Crucially, this strict preservation of interaction topology translates to superior downstream utility, yielding 78.3% DSR in contact-rich tasks. 

**Qualitative Visualization (Inter-X Cases).** Fig. 4 validates robustness under significant mismatches. In transient “Handshakes”, IAMR utilizes dynamic weighting to prioritize critical interaction geometry, effectively resolving the contact loss (“air handshakes”) observed in baselines. Conversely, in continuous “Hugs”, our decoupled optimization reconciles kinematic conflicts, preventing the penetration of OR and the stiffness of DOR to maintain valid close-proximity topology. 

**TABLE II: Quantitative Results of Policy.** We evaluate the contribution of each component. Our full method achieves the most robust balance, effectively integrating coarse-grained geometric alignment (low IEE) with fine-grained physical contact fidelity (high CSR). 

||**Intera**|**ction**|**Con**|**tact**|
|---|---|---|---|---|
||ISR(%)_↑_|IEE(%)_↓_|CSR(%)_↑_|CER_↓_|
|**_MAGIC: Collaborate_**|||||
|Single Agent|18.7|38.9|100.0|0.000|
|w/o Peer Obs|19.5|47.0|100.0|0.000|
|w/o Contact Rew|**93.4**|**4.7**|100.0|0.000|
|w/o Interact Rew|58.1|15.1|100.0|0.000|
|**Ours (Full)**|92.9|4.8|100.0|0.000|
|**_MAGIC: Light Contact_**|||||
|Single Agent|34.3|19.9|24.1|0.283|
|w/o Peer Obs|48.9|13.9|18.6|0.268|
|w/o Contact Rew|85.9|5.4|52.1|0.203|
|w/o Interact Rew|48.7|19.3|28.1|0.243|
|**Ours (Full)**|**90.0**|**4.2**|**78.0**|**0.120**|
|**_MAGIC: Intensive Cont_**|**_act_**||||
|Single Agent|24.0|29.9|37.5|0.312|
|w/o Peer Obs|34.1|21.4|43.7|0.280|
|w/o Contact Rew|**77.3**|**7.7**|70.6|0.174|
|w/o Interact Rew|51.3|17.0|56.8|0.211|
|**Ours (Full)**|75.2|7.9|**78.8**|**0.159**|
|**_Inter-X_**|||||
|Single Agent|25.7|26.9|57.4|0.256|
|w/o Peer Obs|73.2|7.6|75.3|0.143|
|w/o Contact Rew|**95.1**|**3.4**|68.3|0.208|
|w/o Interact Rew|63.2|9.7|**78.6**|**0.110**|
|**Ours (Full)**|92.8|3.5|77.4|0.125|


## _D. Policy Efficacy (Q2)_ 

We assess the robustness and fidelity of the learned control policy across two dimensions: **Interaction Performance** , measured by Interaction Edge Error (IEE) and Interaction Success Rate (ISR); and **Contact Performance** , quantified by Contact Success Rate (CSR) and Contact Error Rate (CER). 

**Quantitative Analysis.** Table II presents the quantitative ablation results, revealing two critical insights. First, Interaction Awareness is non-negotiable. The Single Agent (Vanilla) baseline, limiting agents to isolated tracking, fails to coordinate effectively, achieving only 18.7% ISR in Collaborate scenarios. Similarly, removing peer observations (w/o Peer Obs) severs the closed-loop synchronization, causing physical coupling to collapse (CSR drops to 18.6% in Light Contact). Second, there exists a functional hierarchy between coarsegrained geometric guidance and fine-grained contact regulation. The ablation results reveal that the interaction reward serves as a necessary foundation: removing it (w/o Interaction Rew) causes performance to collapse across all metrics as the policy fails to guide agents into the interaction envelope where contact can be established. For example, ISR drops to 58.1% in Collaborate and CSR drops to 28.1% in Light Contact. Once this spatial proximity is achieved, the contact reward becomes critical for physical realism. Notably, the w/o Contact Rew variant exhibits a “ghosting” phenomenon: it 


**Fig. 5: Qualitative Visualization of Policy.** Single Agent (blue) drifts into collisions. w/o Contact Rew (green) achieves low error but exhibits physical “ghosting”. In contrast, Ours enforces valid physical contact. 

attains high geometric precision (93.4% ISR in Collaborate) by disregarding physical collision constraints, yet fails to maintain valid physical contact (only 52.1% CSR in Light Contact). This is because the policy over-optimizes _rinter_ , exploiting physical interpenetration as a shortcut to minimize geometric error rather than establishing true physical coupling. Ours (Full) effectively integrates these components, leveraging geometric guidance to establish the spatial foundation while using contact regulation to enforce valid physical coupling (above 75% ISR and 77% CSR across all scenarios). 

**Qualitative Visualization.** Fig. 5 highlights the behavioral divergence across methods in the Greeting task. The Single Agent, treating the peer merely as a dynamic obstacle, may initiate interaction but inevitably drifts into collision. While its low-level robustness prevents immediate termination, the interaction topology is destroyed. Similarly, without explicit peer monitoring, the w/o Peer Obs baseline suffers from severe desynchronization (large error spikes). Notably, the w/o Contact Rew variant successfully maintains coarse-grained geometric alignment, yielding an IEE curve comparable to the full method (Green versus Red lines). However, it lacks fine-grained contact fidelity, allowing hands to “ghost” through each other. Ours bridges this gap, achieving the precision as w/o Contact Rew while enforcing valid physical coupling at the contact interface. These visual observations directly align with the quantitative hierarchy in Table II, particularly explaining the discrepancy between geometric (ISR) and physical (CSR) metrics in the baselines. 

**TABLE III: Main Results for Real Robot Experiments.** We conducted 10 trials for each task and evaluated success based on contact establishment at specific keyframes ( _K_ frames per trial). 

|**Task**|**Method**|**Success / Total**|**Rate (%)**|
|---|---|---|---|
|**Hug**|Single Agent<br>**Ours**|8 _/_ 30<br>**26 / 30**|26.7%<br>**86.7%**|
|**Shoulder**|Single Agent|6 _/_ 30|20.0%|
||**Ours**|**24 / 30**|**80.0%**|
|**Greetin**|Single Agent|11 _/_ 90|12.2%|
|**g**|**Ours**|**74 / 90**|**82.2%**|


**Fig. 6: Robustness to disturbances.** Our policy demonstrates strong resilience against aggressive external perturbations (pulling, pushing, and kicking), successfully recovering balance and synchronization. 

## _E. Real-World Robustness (Q3)_ 

We validate the deployment of **Rhythm** on Unitree G1 humanoids to assess its generality, robustness, and success rate in physical environments. 

**Framework Generality.** Fig. 1 demonstrates the system’s versatility across diverse modalities. By strictly preserving finegrained contact geometry in physical coupling tasks (Fig. 1ac) and maintaining spatiotemporal coherence in long-horizon coordination (Fig. 1d), **Rhythm** effectively ensures interaction integrity across the spectrum using a unified formulation. **Quantitative Success Rate.** We evaluate success based on valid contact establishment at task-specific keyframes: _Hug_ uses 3 keyframes (shoulder pat, hand clasp, full hug); _Shoulder_ uses 3 keyframes (start, mid, end of walking); and _Greeting_ uses 9 keyframes (spanning hand, leg, shoulder, and elbow contacts). Table III reports success rates (measured over 10 trials). **Rhythm** consistently outperforms the Single Agent baseline by more than 60%, with the most pronounced gap in _Greeting_ (12 _._ 2% versus 82 _._ 2%). While the baseline fails due to accumulated drift in this long-horizon task, our relative state estimation continuously compensates for misalignment, ensuring robust physical coupling. 

**Robustness to Disturbances.** To evaluate system resilience, we subjected the robots to significant external perturbations during execution. As illustrated in Fig. 6, these disturbances 

included aggressive pushing, pulling, and kicking forces. Despite the severity of these physical interferences, the agents successfully recovered their balance and actively adjusted their relative states to restore the interaction topology. This empirical evidence confirms that our policy has learned robust closed-loop synchronization capabilities, allowing for realtime recovery strategies rather than open-loop motion replay. 

## V. CONCLUSION 

In this work, we present **Rhythm** , a unified framework that, to our knowledge, achieves the first robust transfer of physically coupled interactive behaviors to dual-humanoid hardware. By integrating Interaction-Aware Motion Retargeting (IAMR) to resolve kinematic conflicts and InteractionGuided Reinforcement Learning (IGRL) to master coupled dynamics, our approach effectively bridges the Sim-to-Real gap. Furthermore, we release the MAGIC dataset to facilitate future research in multi-agent embodied intelligence. 

While this work utilizes dual-humanoid setups to rigorously validate the modeling of coupled dynamics, our graph-based formulation is theoretically generic and supports extension to multi-agent systems. A current limitation is the reliance on pre-built maps for state estimation. Future work will focus on eliminating this dependency by shifting towards fully ego-centric perception for map-free collaboration, and scaling the framework to orchestrate complex multi-humanoid interactions in open-world scenarios. 

## REFERENCES 

- [1] Marc Alexa. Differential coordinates for local mesh morphing and deformation. _The Visual Computer_ , 19 (2):105–114, 2003. 

- [2] Arthur Allshire, Hongsuk Choi, Junyi Zhang, David McAllister, Anthony Zhang, Chung Min Kim, Trevor Darrell, Pieter Abbeel, Jitendra Malik, and Angjoo Kanazawa. Visual imitation enables contextual humanoid control. In _Conference on Robot Learning_ , 2025. 

- [3] Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, and C Karen Liu. Retargeting Matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- [4] Qingwei Ben, Feiyu Jia, Jia Zeng, Junting Dong, Dahua Lin, and Jiangmiao Pang. HOMIE: Humanoid locomanipulation with isomorphic exoskeleton cockpit. In _Robotics: Science and Systems_ , 2025. 

- [5] Longbing Cao. Humanoid robots and humanoid ai: Review, perspectives and directions. _ACM Computing Surveys_ , 58(4):1–37, 2025. 

- [6] Haoran Chen, Yiteng Xu, Yiming Ren, Yaoqin Ye, Xinran Li, Ning Ding, Yuxuan Wu, Yaoze Liu, Peishan Cong, Ziyi Wang, et al. Symbridge: A human-in-the-loop cyber-physical interactive system for adaptive humanrobot symbiosis. In _Proceedings of the SIGGRAPH Asia 2025 Conference Papers_ , pages 1–12, 2025. 

- [7] Zixuan Chen, Mazeyu Ji, Xuxin Cheng, Xuanbin Peng, Xue Bin Peng, and Xiaolong Wang. GMT: General 

motion tracking for humanoid whole-body control. _arXiv preprint arXiv:2506.14770_ , 2025. 

- [8] Xuxin Cheng, Yandong Ji, Junming Chen, Ruihan Yang, Ge Yang, and Xiaolong Wang. Expressive whole-body control for humanoid robots. In _Robotics: Science and Systems_ , 2024. 

- [9] Yushi Du, Yixuan Li, Baoxiong Jia, Yutang Lin, Pei Zhou, Wei Liang, Yanchao Yang, and Siyuan Huang. Learning human-humanoid coordination for collaborative object carrying. _arXiv preprint arXiv:2510.14293_ , 2025. 

- [10] Jiawei Gao, Ziqin Wang, Zeqi Xiao, Jingbo Wang, Tai Wang, Jinkun Cao, Xiaolin Hu, Si Liu, Jifeng Dai, and Jiangmiao Pang. CooHOI: Learning cooperative humanobject interaction with manipulated object dynamics. _Advances in Neural Information Processing Systems_ , 37: 79741–79763, 2024. 

- [11] Anindita Ghosh, Rishabh Dabral, Vladislav Golyanik, Christian Theobalt, and Philipp Slusallek. ReMoS: 3D motion-conditioned reaction synthesis for two-person interactions. In _European Conference on Computer Vision (ECCV)_ , 2024. 

- [12] Xinyang Gu, Yen-Jen Wang, Xiang Zhu, Chengming Shi, Yanjiang Guo, Yichen Liu, and Jianyu Chen. Advancing humanoid locomotion: Mastering challenging terrains with denoising world model learning. In _Robotics: Science and Systems_ , 2024. 

- [13] Jinrui Han, Weiji Xie, Jiakun Zheng, Jiyuan Shi, Weinan Zhang, Ting Xiao, and Chenjia Bai. KungfuBot2: Learning versatile motion skills for humanoid whole-body control. _arXiv preprint arXiv:2509.16638_ , 2025. 

- [14] Dongjiao He, Wei Xu, Nan Chen, Fanze Kong, Chongjian Yuan, and Fu Zhang. Point-LIO: robust highbandwidth light detection and ranging inertial odometry. _Advanced Intelligent Systems_ , 5(7):2200459, 2023. 

- [15] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. OmniH2O: Universal and dexterous humanto-humanoid whole-body teleoperation and learning. In _Conference on Robot Learning_ , 2024. 

- [16] Tairan He, Zhengyi Luo, Wenli Xiao, Chong Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Learning humanto-humanoid real-time whole-body teleoperation. In _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2024. 

- [17] Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbabu, Chaoyi Pan, Zeji Yi, Guannan Qu, Kris Kitani, Jessica K. Hodgins, Linxi Fan, Yuke Zhu, Changliu Liu, and Guanya Shi. ASAP: Aligning simulation and real-world physics for learning agile humanoid wholebody skills. In _Robotics: Science and Systems_ , 2025. 

- [18] Xialin He, Runpei Dong, Zixuan Chen, and Saurabh Gupta. Learning getting-up policies for real-world humanoid robots. In _Robotics: Science and Systems_ , 2025. 

- [19] Tao Huang, Junli Ren, Huayi Wang, Zirui Wang, Qingwei Ben, Muning Wen, Xiao Chen, Jianan Li, and 

Jiangmiao Pang. Learning humanoid standing-up control across diverse postures. In _Robotics: Science and Systems_ , 2025. 

- [20] Wei-Jin Huang, Yue-Yi Zhang, Yi-Lin Wei, Zhi-Wei Xia, Juantao Tan, Yuan-Ming Li, Zhilin Zhao, and Wei-Shi Zheng. Learning whole-body human-humanoid interaction from human-human demonstrations. _arXiv preprint arXiv:2601.09518_ , 2026. 

- [21] Yih Huang, Eric Fleury, and Philip K McKinley. LCM: A multicast core management protocol for link-state routing networks. In _ICC’98. 1998 IEEE International Conference on Communications. Conference Record. Affiliated with SUPERCOMM’98 (Cat. No. 98CH36220)_ , volume 2, pages 1197–1201. IEEE, 1998. 

- [22] Jialong Li, Xuxin Cheng, Tianshu Huang, Shiqi Yang, Ri-Zhao Qiu, and Xiaolong Wang. AMO: Adaptive motion optimization for hyper-dexterous humanoid wholebody control. In _Robotics: Science and Systems_ , 2025. 

- [23] Junheng Li, Ziwei Duan, Junchao Ma, and Quan Nguyen. Gait-Net-augmented implicit kino-dynamic MPC for dynamic variable-frequency humanoid locomotion over discrete terrains. In _Robotics: Science and Systems_ , 2025. 

- [24] Yixuan Li, Yutang Lin, Jieming Cui, Tengyu Liu, Wei Liang, Yixin Zhu, and Siyuan Huang. CLONE: Closed-loop whole-body humanoid teleoperation for long-horizon tasks. In _Conference on Robot Learning_ , 2025. 

- [25] Han Liang, Wenqian Zhang, Wenxuan Li, Jingyi Yu, and Lan Xu. InterGen: Diffusion-based multi-human motion generation under complex interactions. _International Journal of Computer Vision (IJCV)_ , 2024. 

- [26] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [27] Michael L. Littman. Markov games as a framework for multi-agent reinforcement learning. In _Proceedings of the Eleventh International Conference on Machine Learning (ICML)_ , volume 157, pages 157–163. Morgan Kaufmann, 1994. 

- [28] Chenhao Liu, Leyun Jiang, Yibo Wang, Kairan Yao, Jinchen Fu, and Xiaoyu Ren. Humanoid whole-body badminton via multi-stage reinforcement learning. _arXiv preprint arXiv:2511.11218_ , 2025. 

- [29] Zuhong Liu, Junhao Ge, Minhao Xiong, Jiahao Gu, Bowei Tang, Wei Jing, and Siheng Chen. It Takes Two: Learning interactive whole-body control between humanoid robots. _arXiv preprint arXiv:2510.10206_ , 2025. 

- [30] Zhengyi Luo, Jinkun Cao, Alexander Winkler, Kris Kitani, and Weipeng Xu. Perpetual humanoid control for real-time simulated avatars. In _IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 10895– 10904, 2023. 

- [31] Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel 

Van de Panne. DeepMimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- [32] Xue Bin Peng, Yunrong Guo, Lina Halper, Sergey Levine, and Sanja Fidler. ASE: Large-scale reusable adversarial skill embeddings for physically simulated characters. _ACM Transactions on Graphics (TOG)_ , 41 (4):1–17, 2022. 

- [33] Skand Peri, Akhil Perincherry, Bikram Pandit, and Stefan Lee. Non-conflicting energy minimization in reinforcement learning based robot control. In _Conference on Robot Learning_ , 2025. 

- [34] Junli Ren, Junfeng Long, Tao Huang, Huayi Wang, Zirui Wang, Feiyu Jia, Wentao Zhang, Jingbo Wang, Ping Luo, and Jiangmiao Pang. Humanoid Goalkeeper: Learning from position conditioned task-motion constraints. _arXiv preprint arXiv:2510.18002_ , 2025. 

- [35] Aleksandr Segal, Dirk Haehnel, and Sebastian Thrun. Generalized-ICP. In _Robotics: Science and Systems_ , volume 2, page 435. Seattle, WA, 2009. 

- [36] Yiyang Shao, Bike Zhang, Qiayuan Liao, Xiaoyu Huang, Yuman Gao, Yufeng Chi, Zhongyu Li, Sophia Shao, and Koushil Sreenath. LangWBC: Language-directed humanoid whole-body control via end-to-end learning. In _Robotics: Science and Systems_ , 2025. 

- [37] Qincheng Sheng, Zhongxiang Zhou, Jinhao Li, Xiangyu Mi, Pingyu Xiang, Zhenghan Chen, Haocheng Xu, Shenhan Jia, Xiyang Wu, Yuxiang Cui, et al. A comprehensive review of humanoid robots. _SmartBot_ , 1(1):e12008, 2025. 

- [38] Sebastian Starke, Yiwei Zhao, Taku Komura, and Kazi Zaman. Local motion phases for learning multi-contact character movements. _ACM Transactions on Graphics_ , 39(4), 2020. 

- [39] Zhi Su, Bike Zhang, Nima Rahmanian, Yuman Gao, Qiayuan Liao, Caitlin Regan, Koushil Sreenath, and S Shankar Sastry. HITTER: A humanoid table tennis robot via hierarchical planning and learning. _arXiv preprint arXiv:2508.21043_ , 2025. 

- [40] Huayi Wang, Zirui Wang, Junli Ren, Qingwei Ben, Tao Huang, Weinan Zhang, and Jiangmiao Pang. BeamDojo: Learning agile humanoid locomotion on sparse footholds. In _Robotics: Science and Systems_ , 2025. 

- [41] Lipeng Wang, Hongxing Fan, Haohua Chen, Zehuan Huang, and Lu Sheng. InterMoE: Individual-specific 3d human interaction generation via dynamic temporalselective moe. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , 2026. 

- [42] Yinhuai Wang, Qihan Zhao, Runyi Yu, Hok Wai Tsui, Ailing Zeng, Jing Lin, Zhengyi Luo, Jiwen Yu, Xiu Li, Qifeng Chen, Jian Zhang, Lei Zhang, and Ping Tan. Skillmimic: Learning basketball interaction skills from demonstrations. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 17540– 17549, June 2025. 

- [43] Jungdam Won, Deepak Gopinath, and Jessica Hodgins. Control strategies for physically simulated characters performing two-player competitive sports. _ACM Transactions on Graphics (TOG)_ , 40(4):1–11, 2021. 

- [44] Weiji Xie, Jinrui Han, Jiakun Zheng, Huanyu Li, Xinzhe Liu, Jiyuan Shi, Weinan Zhang, Chenjia Bai, and Xuelong Li. KungfuBot: Physics-based humanoid wholebody control for learning highly-dynamic skills. _Advances in Neural Information Processing Systems_ , 2025. 

- [45] Liang Xu, Xintao Lv, Yichao Yan, Xin Jin, Shuwen Wu, Congsheng Xu, Yifan Liu, Yizhou Zhou, Fengyun Rao, Xingdong Sheng, Yunhui Liu, Wenjun Zeng, and Xiaokang Yang. Inter-X: Towards versatile humanhuman interaction analysis. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024. 

      - Hodgins, Greg Turk, and Jungdam Won. Simulation and retargeting of complex multi-character interactions. In _ACM SIGGRAPH 2023 Conference Proceedings_ , pages 1–11, 2023. 

   - [55] Zhikai Zhang, Jun Guo, Chao Chen, Jilong Wang, Chenghuai Lin, Yunrui Lian, Han Xue, Zhenrong Wang, Maoqi Liu, Jiangran Lyu, et al. Track any motions under any disturbances. _arXiv preprint arXiv:2509.13833_ , 2025. 

   - [56] Kun Zhou, Jin Huang, John Snyder, Xinguo Liu, Hujun Bao, Baining Guo, and Heung-Yeung Shum. Large mesh deformation using the volumetric graph laplacian. _ACM Transactions on Graphics (TOG)_ , 24(3):496–503, 2005. 

- [46] Liang Xu, Chengqun Yang, Zili Lin, Fei Xu, Yifan Liu, Congsheng Xu, Yiyi Zhang, Jie Qin, Xingdong Sheng, Yunhui Liu, et al. Perceiving and acting in first-person: A dataset and benchmark for egocentric human-objecthuman interactions. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 12535–12548, 2025. 

- [47] Zifan Xu, Myoungkyu Seo, Dongmyeong Lee, Hao Fu, Jiaheng Hu, Jiaxun Cui, Yuqian Jiang, Zhihan Wang, Anastasiia Brund, Joydeep Biswas, et al. Learning agile striker skills for humanoid soccer robots from noisy sensory input. _arXiv preprint arXiv:2512.06571_ , 2025. 

- [48] Yufei Xue, Wentao Dong, Minghuan Liu, Weinan Zhang, and Jiangmiao Pang. A unified and general humanoid whole-body controller for fine-grained locomotion. In _Robotics: Science and Systems_ , 2025. 

- [49] Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, Pieter Abbeel, Carmelo Sferrazza, C Karen Liu, Rocky Duan, and Guanya Shi. OmniRetarget: Interactionpreserving data generation for humanoid whole-body loco-manipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

- [50] Wei Yao, Yunlian Sun, Chang Liu, Hongwen Zhang, and Jinhui Tang. PhysiInter: Integrating physical mapping for high-fidelity human interaction generation. _arXiv preprint arXiv:2506.07456_ , 2025. 

- [51] Yifei Yin, Chen Guo, Manuel Kaufmann, Juan Jose Zarate, Jie Song, and Otmar Hilliges. Hi4D: 4D instance segmentation of close human interaction. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023. 

- [52] Yanjie Ze, Zixuan Chen, Joao Pedro Araujo, Zi-ang Cao, Xue Bin Peng, Jiajun Wu, and Karen Liu. TWIST: Teleoperated whole-body imitation system. In _Conference on Robot Learning_ , 2025. 

- [53] Tong Zhang, Boyuan Zheng, Ruiqian Nai, Yingdong Hu, Yen-Jen Wang, Geng Chen, Fanqi Lin, Jiongye Li, Chuye Hong, Koushil Sreenath, and Yang Gao. HuB: Learning extreme humanoid balance. In _Conference on Robot Learning_ , 2025. 

- [54] Yunbo Zhang, Deepak Gopinath, Yuting Ye, Jessica 

APPENDIX 

_Overview_ 

This appendix is organized into three main sections (A– C) to support the clarity and reproducibility of the proposed framework, **Rhythm** . 

**Terminology.** We refer to our unified framework as **Rhythm** . Within this framework, we define two core components: 

- **IAMR** (Interaction-Aware Motion Retargeting): The retargeting module that resolves kinematic conflicts to generate geometrically consistent motion references from heterogeneous human data (Sec. A). 

- **IGRL** (Interaction-Guided Reinforcement Learning): The multi-agent learning module that masters coupled dynamics via graph-based rewards (Sec. B). 

**Structure.** The Appendix is organized as follows: 

- **A. Details of IAMR (Sec. A):** We first elaborate on the data processing pipeline for heterogeneous motion sources (Part 1). We then provide the mathematical formulations and constraints for the optimization problem (Part 2), followed by a visualization of the topological interaction priors (Part 3). 

- **B. Details of IGRL (Sec. B):** This section specifies the hierarchical network architecture (Part 1), presents the comprehensive definition of graph-based rewards (Part 2), and details the robust training strategies, including curriculum learning and domain randomization (Part 3). 

- **C. Experimental Setup & Metrics (Sec. C):** We provide implementation details for the benchmarking baselines (Part 1), followed by the rigorous mathematical definitions of the evaluation metrics (Part 2). Finally, we describe the hardware configuration and localization system used for Sim-to-Real transfer (Part 3). 

## _A. Details of IAMR_ 

_1) Compatibility with Heterogeneous Motion Sources:_ Human motion datasets contain rich pose and interaction information but differ significantly in data format and physical attributes (e.g., height, body proportions). A key strength of our framework is its input-agnostic design: we first abstract diverse inputs into a standardized representation—time-series of _raw_ global 3D keypoint positions _{p_<sup>raw</sup> _t,i_<sup>_}_—and then process</sup> them into two distinct reference manifolds to resolve the kinematic conflict. 

**Standardization of Input Formats.** Regardless of the source format, our first step is to extract the raw 3D keypoints _p_<sup>raw</sup> _t,i_ for each agent _k ∈{_ 1 _,_ 2 _}_ : 

- **Parametric Human Models (SMPL):** The **Inter-X** dataset [45] utilizes the SMPL format. We compute the raw keypoints via the SMPL forward kinematics function _M_ ( _·_ ) using the recorded pose _q_ and shape _β_ : 

   - _p_<sup>raw</sup> _t_<sup>_,_(</sup><sup>_k_)</sup> = _M_ ( _qt_<sup>(</sup><sup>_k_)</sup> ; _β_<sup>(</sup><sup>_k_)</sup> ) _._ 

- **Skeleton Hierarchy (BVH):** Our **MAGIC** dataset utilizes the standard BVH skeleton hierarchy. Here, raw 

keypoints are derived directly from the skeleton’s forward kinematics _f_<sup>skel</sup> ( _·_ ): 


**Construction of Dual Reference Manifolds.** As discussed in the _Kinematic Conflict_ (Sec. III-A), directly using raw human keypoints is infeasible due to morphological mismatches. To decouple interaction semantics from individual embodiment, we generate two distinct sets of scaled reference keypoints, _Pind_ and _Puni_ , corresponding to the individual ( _Mind_ ) and unified ( _Muni_ ) manifolds respectively. 

Let _h_ robot be the robot’s height, and _h_<sup>(</sup> raw<sup>_k_)betheheightof</sup> the _k_ -th human demonstrator derived from _p_<sup>raw</sup><sup>_,_(</sup><sup>_k_)</sup> . We first compute the individual height ratio _s_<sup>(</sup><sup>_k_)</sup> = _h_ robot _/h_ raw<sup>(</sup><sup>_k_).</sup> 

- **Individual Scaling for Self-Motion (** _Mind_ **):** To ensure kinematic feasibility for each robot’s self-motion (e.g., limb proportions, ground contact), we generate the individual reference set _Pind_ by scaling each agent’s raw keypoints with its own specific ratio _s_<sup>(</sup><sup>_k_)</sup> : 


This set _Pind_ serves as the target for all single-agent tracking objectives (e.g., _Lpos_ , _Lreg_ ), ensuring that each robot tracks a trajectory compatible with its own scale. 

- **Unified Scaling for Interaction Geometry (** _Muni_ **):** To preserve the relative interaction topology (e.g., handholding distance), we generate the unified reference set _Puni_ by applying a single global scale _sunified_ to both agents. We define this scale as the average of the individual factors: 


- This set _Puni_ is exclusively used to compute the _Interaction Graph_ targets (e.g., relative edge lengths). This ensures that the spatial relationship between agents remains consistent with the original performance, preventing the geometric distortion that would arise from non-uniform scaling. 

_2) Optimization Details and Hyperparameters:_ We explicitly formulate the optimization objectives and constraints used to solve the kinematic conflict described in Sec. III-A. 

**Optimization Formulation.** We solve the retargeting problem frame-by-frame using a Sequential Quadratic Programming (SQP) approach. For each frame _t_ , we optimize the joint configurations _qt_ = [ _qt_<sup>(1)</sup> _, qt_<sup>(2)</sup> ] to minimize the following total objective: 


The individual terms are defined as follows: 

- **Self-Motion Preservation (** _Jself_ **):** To maintain local topology and orientation, we minimize deviations from 

the _individual_ reference manifold _Pind_ . 


Here, _L_ ( _·_ ) denotes the discrete Laplacian operator, and _θb_ represents key bone orientations. This term allows the robot to adapt its absolute posture while preserving local motion semantics. 

- **Interaction Preservation (** _Jinter_ **):** This term enforces relative geometric consistency by tracking the _unified_ reference manifold _Puni_ . We split the interaction error term to fit the column width: 


Where _ωij_ is the distance-dependent stiffness. This explicitly penalizes deviations in the relative position vectors between agents. 

- **Regularization (** _Jreg_ **):** Ensures temporal smoothness. It includes a minimum velocity term _∥qt − qt−_ 1 _∥_<sup>2</sup> . 

**Constraints.** The optimization is subject to the following hard constraints: 

- **Joint Limits:** The solution must respect the robot’s physical joint ranges: _q_<sup>_min_</sup> _≤ qt−_ 1 + ∆ _qt ≤ q_<sup>_max_</sup> . 

- **Collision Avoidance:** We enforce non-penetration for all active collision pairs. Linearizing the signed distance field _ϕ_ ( _q_ ), we require _Jcol_ ∆ _qt ≥−ϕ_ ( _qt−_ 1) _−ϵsafe_ , where _Jcol_ is the normal Jacobian and _ϵsafe_ is a safety margin. 

- **Foot Contact:** For feet in strict contact (detected from source motion), we impose a zero-velocity constraint on the end-effectors: _∥Jfoot_ ∆ _qt∥≤ ϵstick_ . 

- **Trust Region:** To ensure the validity of the linearization, we bound the step size: _∥_ ∆ _qt∥_ 2 _≤ δ_ . 

**Implementation & Hyperparameters.** The optimization is implemented in Python using **CVXPY** with the **OSQP** solver. Empirically, we set the weights to prioritizes interaction stability: _wself_ = 2 _._ 0, _winter_ = 10 _._ 0, and _wreg_ = 0 _._ 1. The rotation weight _λrot_ is set to 0 _._ 1. 

_3) Topological Graph Visualization:_ To provide an intuitive understanding of the topological priors, we visualize the extracted graph structures using a representative interaction case (e.g., a handshake task), as shown in Fig. 7. The visualization highlights two distinct connectivity types used by IAMR: 

- **The Interaction Graph (Yellow Edges):** Bridges the keypoints of the two agents based on the Unified Manifold. It captures the _spatial intent_ and proximity required for coordination. 

- **The Contact Graph (Red Edges):** Highlights active physical collision links between specific robot bodies. This explicitly encodes the _physical coupling_ state. 

## **Algorithm 1** Interaction-Aware Motion Retargeting (IAMR) 

- **Require:** Source Motion _Q_<sup>_src_</sup> , Robot Models _R_ 1 _, R_ 2 **Ensure:** Retargeted Motion _Q_<sup>_rob_</sup> 1: **Phase 1: Dual-Manifold Construction** 2: Compute scales: _sk ← hrob/hsrc_<sup>(</sup><sup>_k_),</sup><sup>_s_</sup> _uni_<sup>_←_avg(</sup><sup>_s_</sup> _k_<sup>)</sup> 3: **for** _t_ = 0 _→ T_ **do** 4: _pt_<sup>_raw_</sup> _←_ FK( _qt_<sup>_src_</sup> ) 5: _Pind_<sup>(</sup><sup>_k_)</sup><sup>_←sk · p_</sup> _t_<sup>_raw,_(</sup><sup>_k_)</sup> ; _Puni_<sup>(</sup><sup>_k_)</sup><sup>_←suni · p_</sup> _t_<sup>_raw,_(</sup><sup>_k_)</sup> 6: Pre-compute targets: _Lref ←L_ ( _Pind_<sup>(</sup><sup>_k_))</sup> 7: **end for** 8: **Phase 2: SQP Optimization** 9: Initialize _q_ 0 _← qnom_ 

- 10: **for** _t_ = 1 _→ T_ **do** 11: Detect interaction graph _Einter_ using _Puni_ 12: Let _qprev ← qt−_ 1 13: **Formulate QP Subproblem (Solve for** ∆ _q_ **):** 14: _Objective:_ min∆ _q J_ ( _qprev_ + ∆ _q_ ) 15: = _wself_ ( _∥L_ ( _q_ ) _−Lref ∥_<sup>2</sup> + _λrot∥_ ∆ _θ∥_<sup>2</sup> ) 16: + _winter_ �( _i,j_ ) _∈E_<sup>_ωij∥_∆</sup><sup>_pij−_∆</sup><sup>_p_</sup> _ij_<sup>_uni∥_2</sup> 17: + _wreg∥_ ∆ _q∥_<sup>2</sup> 18: _Subject to Constraints:_ 19: 1) Limits: _q_<sup>_min_</sup> _≤ qprev_ + ∆ _q ≤ q_<sup>_max_</sup> 20: 2) Collision: _Jcol_ ∆ _q ≥−ϕ_ ( _qprev_ ) _− ϵsafe_ 21: 3) Contact: _∥Jfoot_ ∆ _q∥≤ ϵstick_ **if** foot <u>contact</u> 22: 4) Trust Region: _∥_ ∆ _q∥_ 2 _≤ δ_ 23: ∆ _q_<sup>_∗_</sup> _←_ OSQP(Objective _,_ Constraints) 24: Update: _qt ← qprev_ + ∆ _q_<sup>_∗_</sup> 25: Append _qt_ to _Q_<sup>_rob_</sup> 26: **end for** 27: **return** _Q_<sup>_rob_</sup> 


**Fig. 7: Visualization of Topological Interaction Priors.** We illustrate the extracted graph structures on a representative interaction task, where **yellow edges** denote spatial interaction constraints and **red edges** indicate physical contacts. 

By explicitly modeling these connections, IAMR provides topological cues that guide the downstream policy to distinguish between required interaction and unwanted penetration. 

## _B. Details of IGRL_ 

_1) Network Architecture:_ Our policy _πθ_ ( _at|ot_ ) employs a hierarchical encoder-decoder architecture designed to process heterogeneous temporal data. The network input is composed of three semantic groups, which are processed by specialized encoders before being fused for action generation. 

## **Observation Space & Inputs** 

To capture complex coupled dynamics, the policy inputs are organized into two distinct temporal streams: a **Future Window** ( _t_ + 1 _. . . t_ + 20) providing feedforward intent, and a **History Window** ( _t −_ 19 _. . . t_ ) providing feedback control states. 

- **Future Reference (** _ofut ∈_ R<sup>93</sup> **per step):** Encodes the look-ahead trajectory for motion planning. 

   - _Self Future (∈_ R<sup>64</sup> _):_ Contains the reference joint positions ( _∈_ R<sup>29</sup> ) and velocities ( _∈_ R<sup>29</sup> ), along with the reference root orientation ( _∈_ R<sup>6</sup> ). The orientation is represented by the first two columns of the rotation matrix (Rot6D). 

   - _Partner Future (∈_ R<sup>29</sup> _):_ Contains the partner’s reference joint positions to anticipate collaborative intent. 

- **History Observation (** _ohist ∈_ R<sup>239</sup> **per step):** Aggregates the agent’s proprioception and perception of the peer. 

   - **Proprioception (** _oprop ∈_ R<sup>157</sup> **):** 

      - _∗ Tracking State (∈_ R<sup>64</sup> _):_ Includes the current step’s reference joint positions and velocities, combined with the root orientation error ( _∈_ R<sup>6</sup> ). The orientation error is computed from the first two columns of the rotation error matrix ( _Rdes_<sup>_TRcur_).</sup> 

      - _∗ Physical State (∈_ R<sup>93</sup> _):_ Includes projected gravity ( _∈_ R<sup>3</sup> ), base angular velocity ( _∈_ R<sup>3</sup> ), joint positions ( _∈_ R<sup>29</sup> ), joint velocities ( _∈_ R<sup>29</sup> ), and previous actions ( _∈_ R<sup>29</sup> ). 

      - **Peer Perception (** _opeer ∈_ R<sup>82</sup> **):** 

      - _∗ Partner State (∈_ R<sup>64</sup> _):_ Includes the partner’s current reference joint positions ( _∈_ R<sup>29</sup> ), actual joint positions ( _∈_ R<sup>29</sup> ), and the partner’s root orientation error ( _∈_ R<sup>6</sup> ). 

      - _∗ Interaction Topology (∈_ R<sup>18</sup> _):_ Explicitly encodes the formation geometry by including both the _reference_ and _simulation_ relative transforms. Each transform consists of the relative position ( _prel ∈_ R<sup>3</sup> ) and orientation ( _Rrel ∈_ R<sup>6</sup> ) expressed in the ego-centric frame. 

## **Temporal Encoders (1D-CNN)** 

We employ two separate 1D-Convolutional Neural Networks to extract features from the observation history and future trajectories. Distinct from standard implementations, we employ an _Input Projection_ layer to compress high-dimensional inputs before temporal convolution. 

- **Architecture:** Both the History and Future encoders share a dual-layer CNN structure configured as follows: 

   - _Input Projection:_ Linear mapping to latent dim _C_ = 60. 

   - _Layer 1:_ Conv1d(60 _→_ 40, _k_ = 6 _, s_ = 2), ELU. 

   - **–** _Layer 2:_ Conv1d(40 _→_ 20, _k_ = 4 _, s_ = 2), ELU. 

- **Output:** The temporal features are flattened and projected to compact embeddings ( _ehist ∈_ R<sup>67</sup> _, efut ∈_ R<sup>64</sup> ). Uniquely, _ehist_ incorporates an explicit estimation of 

the base linear velocity ( _v_ ˆ _base ∈_ R<sup>3</sup> ) alongside the latent features. This design serves as a fusion of explicit physical estimation and implicit temporal representations, compensating for the lack of direct velocity observations in the real world. 

## **Action Decoder (MLP)** 

The encoded temporal features are concatenated with the current time-step observation and fed into a Multi-Layer Perceptron (MLP) to generate the action distribution. 

- **Structure:** Three hidden layers with [512 _,_ 256 _,_ 128] units and ELU activation. 

- **Output Head:** A linear layer outputs the mean _µt ∈_ R<sup>29</sup> of the Gaussian distribution for target joint positions. The standard deviation _σ_ is a learnable parameter initialized at 1.0. 

_2) Reward Definitions:_ The total reward _rt_ is computed as a weighted sum of terms designed to balance kinematic fidelity with interaction plausibility, as detailed in Table IV. We prioritize interaction-centric objectives (e.g., relative geometry and contact) over individual tracking precision to encourage compliant multi-agent coupling. 

## **Interaction Graph Reward (** _rinter_ **)** 

As formulated in the main text (Sec. III-B, _Graph-based Rewards_ ), this term enforces geometric consistency by penalizing deviations in the interaction edges. 


By inheriting the dynamic weights _wij_ from the IAMR module, the policy inherently learns to prioritize the same spatial topology (e.g., hand-shoulder proximity) as the optimized reference. 

## **Physical Contact Graph Reward (** _rcontact_ **)** 

Unlike kinematic tracking, physical interaction requires satisfying force constraints that are not present in motion datasets. We propose a graph-based formulation that handles contact nodes dynamically based on their reference status. Leveraging the flexible node definition [42], we map simulation links to a set of abstract contact nodes _V_ (e.g., palms, feet, pelvis). The reward is computed as a weighted sum of an _active contact_ term and an _inactive_ term: 


The weights _λact_ and _λinact_ are adaptive, calculated as the ratio of active/inactive nodes in the current reference frame, ensuring balanced supervision across diverse contact phases. _i) Active Contact Error (Eact):_ For nodes where contact is expected ( _k ∈Vact_ ), we define a hybrid error combining binary status consistency and continuous force regularization: 


where _Ck_<sup>_sim_</sup> _∈{_ 0 _,_ 1 _}_ is the detected contact status. The force regularization term _Lforce_ penalizes forces outside the valid range [ _Fmin, Fmax_ ]: 

   - tracking and interaction errors as the agent gains proficiency. 

- _Precision Phase (L_<sup>¯</sup> _max ≥_ 500 _):_ Weights stabilize at **_α_** _target_ . The sampling strictly targets complex interaction phases that impose high control complexity despite low failure probability. 


## **Dual-Agent Domain Randomization** 

To bridge the Sim-to-Real gap, we introduce perturbations targeting both physical dynamics and the specific challenges of distributed multi-agent communication, as detailed in Table V. **Communication & Initialization Strategy.** Beyond standard dynamics randomization, we implement specific strategies for dual-agent coordination: 

This formulation explicitly guides the agent to exert sufficient force for stability ( _> Fmin_ ) while preventing explosive collisions ( _< Fmax_ ), solving the ambiguity of “touching without force”. 

_ii) Inactive Contact Error (Einact):_ For nodes where no contact is expected ( _k ∈V/ act_ ), we strictly penalize any detected “ghost interaction”: 

- **Communication Degradation:** We explicitly model the latency in distributed systems. By training with randomized delays (20 _∼_ 60ms) for both peer proprioception (wireless transmission) and relocalization (vision processing), the policy learns to be robust against asynchronous data reception. 


_3) Robust Training Strategy:_ To ensure transferability to the physical world and handle the complexity of coupled interaction phases, we implement a rigorous training protocol comprising error-aware curriculum-based adaptive sampling and extensive domain randomization. 

- **Initial State Perturbation:** To handle calibration errors, we initialize episodes with random offsets in root position ( _±_ 5cm) and orientation ( _±_ 0 _._ 2rad). This forces the policy to learn active recovery behaviors from suboptimal relative configurations immediately upon activation. 

## **Curriculum-based Adaptive Sampling** 

Standard Reference State Initialization (RSI) relies on sparse failure counts, which is insufficient for interaction tasks where “survival” does not imply “success” (e.g., maintaining balance but losing interaction geometry). We propose a continuous, error-aware sampling strategy defined as follows: 

_C. Experimental Setup & Metrics_ 

_1) Baseline Implementation Details:_ To strictly validate our contributions, we benchmark our framework against two sets of baselines: kinematic retargeting methods (answering Q1) and dynamic policy learning variants (answering Q2). 

- **Multi-Objective Error Landscape:** For each discretized motion bin _s_ , we maintain a smoothed error vector **e** ( _s_ ) = [ _efail, etrack, einter_ ]<sup>_T_</sup> , incorporating failure signals, tracking errors, and interaction violations. To capture temporal causality—where failures stem from preceding suboptimal actions—we smooth these signals using a non-causal Gaussian kernel ( _k_ = 3) implemented via 1D convolution. 

## **Retargeting Baselines (Kinematic Level)** 

All baselines utilize the same source motion data and undergo identical skeletal scaling pre-processing to ensure fair comparison. 

   - **GMR (General Motion Retargeting) [3]:** A standard Cartesian-space optimization method. It treats the two humanoids as isolated entities, optimizing joint angles to minimize the tracking error of individual keypoints’ **positions and rotations** (e.g., end-effectors, pelvis) relative to the source motion. It does not include any interactionaware constraints. 

- **Dynamic Probability:** The sampling probability _P_ ( _s_ ) is a convex combination of uniform exploration ( _η_ = 0 _._ 05) and error-weighted exploitation, modulated by curriculum weights **_α_** : 


- **OR (OmniRetarget) [49]:** A retargeting method utilizing Interaction Mesh (I-Mesh) to preserve geometric topology, originally designed for Human-Object Interaction (HOI) scenarios. In our dual-agent setting, we apply OR to each agent independently. While it preserves individual body topology, it lacks mechanisms to model or preserve inter-agent spatial relationships. 

- **Curriculum Schedule:** The weight vector **_α_** evolves based on the maximum moving average episode length _L_ ¯ _max_ to ensure monotonic progress: 

   - _Stability Phase (L_<sup>¯</sup> _max <_ 350 _):_ Weights are fixed at **_α_** _init_ = [0 _._ 8 _,_ 0 _._ 1 _,_ 0 _._ 1]. The policy prioritizes states leading to terminal failures to learn basic balance capabilities. 

   - **DOR (Dual-OmniRetarget):** A strong baseline we constructed by extending OmniRetarget to the multi-agent setting. We construct a holistic interaction mesh that encompasses both robot bodies, creating “cross-agent” edges between proximal body parts. However, by treating the dual-agent system as a single unified mesh, it fails to distinguish between critical inter-agent interactions and 

- _Transition Phase (_ 350 _≤ L_<sup>¯</sup> _max <_ 500 _):_ We perform **linear interpolation** between **_α_** _init_ and the target weights **_α_** _target_ = [0 _._ 05 _,_ 0 _._ 30 _,_ 0 _._ 65]. This gradually shifts the focus from avoiding failures to minimizing 

**TABLE IV:** Reward Terms and Weights used in IGRL 

|**Term**|**Weight**|**Equation**|**Description**|
|---|---|---|---|
|**_Interaction Gra_**|**_ph Obje_**|**_ctives_**<br><br>||
|Interact Edge|1_._5|exp<br>�<br>_−_<sup>1</sup><br>_σi_<br>�<br>(_i,j_)_∈E _<sup>_wij∥psim_</sup><br>_ij_<br>_−p_<sup>_ref_</sup><br>_ij _<sup>_∥_2�</sup>|Enforces geometric consistency of interaction edges.|
|Contact|1_._0|_λacte_<sup>_−Eact/σ_2</sup><br>_c_ +_λinacte_<sup>_−Einact/σ_2</sup><br>_c_<br>**where** _Eact_ = <sup>�</sup><br>_k∈Vact_<sup>(</sup><sup>_β∥Csim_</sup><br>_k_<br>_−_1_∥_+ (1_−β_)_Lf_)<br>**and**<br>_Einact_ = <sup>�</sup><br>_k /∈Vact _<sup>_∥Csim_</sup><br>_k_<br>_−_0_∥_|Balances active contact enforcement (force constrained)<br>and ghost interaction suppression.|
|**_Motion Trackin_**|**_g Object_**|**_ives_**||
|Upper Pos|1_._0|exp(_−_<sup>1</sup><br>_Nu_<br>�<br>_k∈Upper _<sup>_∥psim_</sup><br>_k_<br>_−p_<sup>_ref_</sup><br>_k_<br>_∥_<sup>2</sup>_/σ_<sup>2</sup><br>_pos_<sup>)</sup><br>|Tracks Euclidean positions of upper body links.|
|Upper Ori|1_._0|exp(_−_<sup>1</sup><br>_Nu_<br>�<br>_k∈Upper _<sup>_∥_log((</sup><sup>_Rsim_</sup><br>_k_<br>)<sup>_⊤_</sup>_R_<sup>_ref_</sup><br>_k_<br>)_∥_<sup>2</sup>_/σ_<sup>2</sup><br>_ori_<sup>)</sup>|Tracks orientation of upper body links.|
|Upper Lin Vel|1_._0|exp(_−_<sup>1</sup><br>_Nu_<br>�<br>_k∈Upper _<sup>_∥vsim_</sup><br>_k_<br>_−v_<sup>_ref_</sup><br>_k_<br>_∥_<sup>2</sup>_/σ_<sup>2</sup><br>_vel_<sup>)</sup>|Matches linear velocities of upper body.|
|Upper Ang Vel|1_._0|exp(_−_<sup>1</sup><br>_Nu_<br>�<br>_k∈Upper _<sup>_∥ωsim_</sup><br>_k_<br>_−ω_<sup>_ref_</sup><br>_k_<br>_∥_<sup>2</sup>_/σ_<sup>2</sup><br>_ang_<sup>)</sup>|Matches angular velocities of upper body.|
|Lower Pos|0_._5|exp(_−_<sup>1</sup><br>_Nl_<br>�<br>_k∈Lower _<sup>_∥psim_</sup><br>_k_<br>_−p_<sup>_ref_</sup><br>_k_<br>_∥_<sup>2</sup>_/σ_<sup>2</sup><br>_pos_<sup>)</sup>|Tracks Euclidean positions of lower body links.|
|Lower Ori|0_._5|exp(_−_<sup>1</sup><br>_Nl_<br>�<br>_k∈Lower _<sup>_∥_log((</sup><sup>_Rsim_</sup><br>_k_<br>)<sup>_⊤_</sup>_R_<sup>_ref_</sup><br>_k_<br>)_∥_<sup>2</sup>_/σ_<sup>2</sup><br>_ori_<sup>)</sup>|Tracks orientation of lower body links.|
|Lower Lin Vel|0_._5|exp(_−_<sup>1</sup><br>_Nl_<br>�<br>_k∈Lower _<sup>_∥vsim_</sup><br>_k_<br>_−v_<sup>_ref_</sup><br>_k_<br>_∥_<sup>2</sup>_/σ_<sup>2</sup><br>_vel_<sup>)</sup>|Matches linear velocities of lower body.|
|Lower Ang Vel|0_._5|exp(_−_<sup>1</sup><br>_Nl_<br>�<br>_k∈Lower _<sup>_∥ωsim_</sup><br>_k_<br>_−ω_<sup>_ref_</sup><br>_k_<br>_∥_<sup>2</sup>_/σ_<sup>2</sup><br>_ang_<sup>)</sup>|Matches angular velocities of lower body.|
|Anchor Pos|0_._3|exp(_−∥p_<sup>_sim_</sup><br>_root _<sup>_−pref_</sup><br>_root_<sup>_∥_2</sup><sup>_/σ_2</sup><br>_root_<sup>)</sup>|Tracks root position in world frame to prevent global drift.|
|Anchor Ori|0_._5|exp(_−∥_log((_R_<sup>_sim_</sup><br>_root_<sup>)</sup><sup>_⊤Rref_</sup><br>_root_<sup>)</sup><sup>_∥_2</sup><sup>_/σ_2</sup><br>_root_<br>_ori_<sup>)</sup>|Tracks root heading in world frame.|
|**_Regularization _**|**_& Penalt_**|**_ies_**||
|Action Rate|_−_0_._3|_∥_**a**_t −_**a**_t−_1_∥_<sup>2</sup>|Penalizes action changes to ensure smooth control.|
|Feet Slip|_−_0_._5|�<br>_k∈F eet_ <sup>I(</sup><sup>_contactk_)</sup><sup>_· ∥vk,xy∥_2</sup>|Penalizes foot sliding velocity during ground contact.|
|Joint Limit|_−_10_._0|�<br>_j_ <sup>max(0</sup><sup>_, |qj| −qlimit_)</sup>|Penalizes violations of physical joint limits.|
|Torque|10<sup>_−_4</sup>|_−∥τ∥_<sup>2</sup>|Prevents excessive torques.|


**TABLE V:** Domain Randomization Parameters 

framework, we compare against the following variants. All variants are trained using the same PPO hyperparameters and network architecture unless specified otherwise. 

|**Term**<br>|**Value**|g    ypp <br>network architecture unless specified otherwise.|
|---|---|---|
|**_Dynamics Randomization_**<br>||_•_ **Single Agent:** Represents the “Status Quo” approach.|
|Link Mass<br>|_U_[0_._9_,_1_._1]_×_default (per link)<br>|This policy treats the peer robot merely as a dynamic|
|CoM Offset (Torso)<br>|∆_x, y, z ∈U_[_−_0_._05_,_0_._05] m<br>|obstacle or ignores it entirely.|
|Joint Friction<br>Actuator Gains<br>Restitution<br>Default Joint Pos<br>Control Delay<br>**_External Perturbations_**|Static: _U_[0_._3_,_2_._0],<br>Dynamic: _U_[0_._3_,_1_._6]<br>Stiffness/Damping: _U_[0_._9_,_1_._1]<br>_U_[0_._0_,_0_._8] (Ground contact)<br>∆_θ_0 _∼U_[_−_0_._01_,_0_._01] rad (Calibration)<br>_U_[0_,_15] ms|_Implementation:_ The peer observation _opeer_ is masked,<br>and the reward function includes only standard tracking<br>terms (_rtrack_) without any interaction (_rinter_) or contact<br>(_rcontact_) objectives. The agent is rewarded solely for<br>tracking its own retargeted reference.<br>_•_ **Ours w/o Peer Obs:** Evaluates the necessity of explicit<br>inter-aentercetion|
|Robot Push (Linear)|_vx,y ∼U_[_−_0_._4_,_0_._4] m/s,<br>_vz ∼U_[_−_0_._16_,_0_._16] m/s|g pp.<br>_Implementation:_ The policy architecture is identical to<br>|
|Robot Push (Angular)|_ωx,y ∼U_[_−_0_._4_,_0_._4] rad/s,<br>_ωz ∼U_[_−_0_._64_,_0_._64] rad/s|IGRL, but the peer observation stream _opeer_ is zeroed<br>out. The reward function remains full (including inter-|
|Push Interval|Applied every 1_._0_∼_3_._0 s|action rewards), forcing the agent to infer interaction|
|Initial Pose Offset|∆_pos ∈_[_−_5_,_5] cm,<br>∆_yaw ∈_[_−_0_._2_,_0_._2] rad|requirements solely from its own proprioception and the<br>reference motion.|
|**_Communication Degradat_**|**_ion_**|_•_ **Ours w/o Contact Rew:** Evaluates the contribution of|
|Peer Latency|Proprioception & Relocalization:<br>_U_[20_,_60] ms|the Physical Contact Graph.<br>_Implementation:_ The policy is trained with the full ob-|


- **Single Agent:** Represents the “Status Quo” approach. This policy treats the peer robot merely as a dynamic obstacle or ignores it entirely. _Implementation:_ The peer observation _opeer_ is masked, and the reward function includes only standard tracking terms ( _rtrack_ ) without any interaction ( _rinter_ ) or contact ( _rcontact_ ) objectives. The agent is rewarded solely for tracking its own retargeted reference. 

- **Ours w/o Contact Rew:** Evaluates the contribution of the Physical Contact Graph. _Implementation:_ The policy is trained with the full observation space, but the contact reward _rcontact_ weight is set to zero. This tests whether kinematic tracking alone is sufficient to establish stable physical coupling. 

individual self-motion, leading to an optimization that lacks focus on core interaction information. 

- **Ours w/o Interaction Rew:** Evaluates the contribution of the Spatial Interaction Graph. _Implementation:_ The interaction graph reward _rinter_ 

## **Policy Learning Baselines (Dynamic Level)** 

To isolate the contribution of specific components in our IGRL 

is removed. The agent relies purely on standard position/rotation tracking rewards to maintain formation. This tests the importance of explicitly optimizing relative topology for resolving geometric ambiguities. 

_2) Evaluation Metric Implementation Details:_ We employ specific metrics for each component of our framework to evaluate kinematic quality and dynamic performance respectively. 

## **Retargeting Evaluation Metrics (Q1)** 

We evaluate retargeting quality from three complementary aspects: physical feasibility, interaction fidelity, and downstream utility. 

- **Inter-Penetration Rate (IPR) & Max Penetration Depth (MPD):** Measure physical feasibility by reporting the percentage of frames exhibiting inter-agent penetration and the maximum penetration depth across the sequence. Lower values indicate safer motion. 

- **Interaction Edge Error (IEE):** Quantifies geometric interaction fidelity as the normalized L2 distance between retargeted interaction edges and the scaled ground-truth edges. 

- **Contact F1 Score:** Evaluates binary contact accuracy against ground-truth interaction edges following [20, 29]. We report F1 scores under **Strict** ( _τ <_ 0 _._ 2 m) and **Loose** ( _τ <_ 0 _._ 4 m) contact settings to assess precision at different scales. 

- **Downstream Success Rate (DSR):** Serves as a proxy for physical learnability. It is defined as the percentage of RL rollouts where the agent can track the retargeted reference while maintaining the interaction structure (i.e., maintaining an IEE deviation _<_ 20% relative to the scaled ground truth). 

## **Policy Learning Evaluation Metrics (Q2)** 

To assess the robustness and fidelity of the learned control policy in dynamic environments, we evaluate interaction and contact performance with respect to the retargeted reference trajectories. 

- **Interaction Performance (ISR & IEE):** Measures interaction fidelity by computing the distance-weighted relative error between simulated interaction edges and the retargeted reference edges. We report the mean **Interaction Edge Error (IEE)** and the **Interaction Success Rate (ISR)** , defined as the percentage of steps where the IEE is kept within a strict tolerance ( _<_ 10%). 

stack written in C++ for real-time performance. 

**Robot Platform & Compute.** The Unitree G1 (approx. 1.3 m height, 29 DoF) serves as our experimental testbed. Unlike simulation where state information is privileged, all computations—including state estimation, policy inference, and low-level control—are performed onboard the robot’s internal CPU. We utilize ONNX Runtime to execute the trained policies, achieving an inference latency of less than 3 ms, ensuring a stable 50 Hz control loop. 

**Hierarchical Localization System.** Precise relative localization is a prerequisite for our _Interaction Graph_ reward calculation. We develop a robust, coarse-to-fine localization framework fusing LiDAR and IMU data: 

- **High-Frequency Odometry:** We utilize **Point-LIO** [14], a robust LiDAR-Inertial Odometry framework, to provide high-bandwidth (10 Hz) state estimation robust to aggressive motions and vibrations. 

- **Global Initialization (Coarse):** To handle the “cold start” problem and global drift, we implement a neural registration service based on **GeoTransformer** . This module extracts superpoint features to perform global registration between the current scan and a pre-built point cloud map, providing a reliable initial pose guess. 

- **Real-Time Tracking (Fine):** During operation, a C++ relocalization node refines the pose using **GICP** (Generalized Iterative Closest Point) [35]. A Kalman Filter fuses the high-frequency relative odometry from PointLIO with the low-frequency global pose corrections from GICP to output smooth, drift-free global states. 

**Control Architecture.** The deployment system operates on a dual-frequency hierarchy to match the simulation setup: 

- **High-Level Policy (50 Hz):** The motion tracking policy constructs observations based on the fused state estimates and computes desired joint positions. 

- **Low-Level Controller (500 Hz):** A real-time PD controller converts these targets into motor torques, enforcing the physical compliance required for safe interaction. 

**Multi-Agent Synchronization.** To enable coordinated interaction, the agents exchange their estimated global poses and full peer observations ( _opeer_ ) via the **LCM** (Lightweight Communications and Marshalling) protocol [21]. 

- **Contact Performance (CSR & CER):** Evaluates physical contact fidelity relative to the retargeted reference contacts. The **Contact Error Rate (CER)** measures the rate of violations of required contact constraints, while the **Contact Success Rate (CSR)** reports the percentage of steps where sufficient reference contacts ( _>_ 80%) are correctly recalled by the policy. 

_3) Sim-to-Real Hardware:_ We validate our approach on the Unitree G1 humanoid robot platform. To bridge the gap between ideal simulation states and real-world noisy sensor data, we implement a fully onboard perception and control 

