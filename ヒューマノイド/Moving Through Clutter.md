---
title: "Moving Through Clutter: Scaling Data Collection and Benchmarking for 3D Scene-Aware Humanoid Locomotion via Virtual Reality"
date: "2026-03-06"
authors: "Beichen Wang; Yuanjie Lu; Linji Wang; Liuchuan Yu; Xuesu Xiao"
url: https://arxiv.org/abs/2603.05993
pdf: https://arxiv.org/pdf/2603.05993
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.05993)** / [論文ページ](https://arxiv.org/abs/2603.05993)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Moving Through Clutter: Scaling Data Collection and Benchmarking for 3D Scene-Aware Humanoid Locomotion via Virtual Reality** 

Beichen Wang, Yuanjie Lu, Linji Wang, Liuchuan Yu, and Xuesu Xiao 

**_Abstract_ — Recent advances in humanoid locomotion have enabled dynamic behaviors such as dancing, martial arts, and parkour, yet these capabilities are predominantly demonstrated in open, flat, and obstacle-free settings. In contrast, real-world environments—homes, offices, and public spaces—are densely cluttered, three-dimensional, and geometrically constrained, requiring scene-aware whole-body coordination, precise balance control, and reasoning over spatial constraints imposed by furniture and household objects. However, humanoid locomotion in cluttered 3D environments remains underexplored, and no public dataset systematically couples full-body human locomotion with the scene geometry that shapes it. To address this gap, we present Moving Through Clutter (MTC), an opensource Virtual Reality (VR)-based data collection and evaluation framework for scene-aware humanoid locomotion in cluttered environments. Our system procedurally generates scenes with controllable clutter levels and captures embodimentconsistent, whole-body human motion through immersive VR navigation, which is then automatically retargeted to a humanoid robot model. We further introduce benchmarks that quantify environment clutter level and locomotion performance, including stability and collision safety. Using this framework, we compile a dataset of 348 trajectories across 145 diverse 3D cluttered scenes. The dataset provides a foundation for studying geometry-induced adaptation in humanoid locomotion and developing scene-aware planning and control methods.** 

## I. INTRODUCTION 

Humanoid locomotion on flat terrain has witnessed rapid progress in recent years, with learning-based controllers achieving highly dynamic behaviors such as agile running, recovery from perturbations, and acrobatic motion synthesis [1], [2]. A central driver of this progress is the availability of large-scale human motion datasets. By leveraging motion priors derived from resources such as AMASS dataset [3], reinforcement learning policies can acquire diverse and natural locomotion strategies that would be difficult to engineer manually. The scale and diversity of motion data have emerged as a key factor shaping the capabilities of modern humanoid locomotion systems. 

Despite these advances, most existing methods are developed and evaluated in open, obstacle-free settings. Realworld deployment, however, requires humanoid robots to operate within cluttered environments where locomotion is 

All authors are with George Mason University, 4400 University Dr, Fairfax, VA 22030, USA {bwang25, ylu22, lwang44, lyu20, xiao}@gmu.edu 

This work has taken place in the RobotiXX Laboratory at George Mason University. RobotiXX research is supported by National Science Foundation (NSF, 2350352), Army Research Office (ARO, W911NF2320004, W911NF2420027, W911NF2520011), Air Force Research Laboratory (AFRL), US Air Forces Central (AFCENT), Google DeepMind (GDM), Clearpath Robotics, Raytheon Technologies (RTX), Tangenta, Mason Innovation Exchange (MIX), and Walmart. 


Fig. 1. We introduce MTC, a dataset and benchmark for humanoid locomotion in cluttered 3D environments. We first procedurally generate cluttered simulation scenes with diverse geometric constraints, then collect immersive, embodiment-scaled locomotion trajectories using VR-based fullbody tracking within these environments. The resulting dataset enables benchmarking of scene-aware humanoid locomotion behaviors. 

constrained by surrounding three-dimensional (3D) geometry, like in homes or offices. Locomotion in such settings demands continuous whole-body postural adaptation coupled to environmental structure, including lateral clearance management, height-aware motion, and acyclic and asymmetric limb adjustment to avoid collisions. These requirements fundamentally differ from flat-ground locomotion and remain largely underexplored from a data-centric perspective. 

Although human motion datasets have proven essential for humanoid locomotion learning, no publicly available resource currently provides scene-aware, embodimentconsistent humanoid locomotion trajectories that are explicitly aligned with 3D cluttered environments. The primary bottleneck lies in scalable data acquisition. Traditional motion capture pipelines rely on open studios without occlusions and therefore fail to encode interactions with spatial constraints. Constructing diverse physical environments, e.g., with large furniture and household objects, for data collection is expensive and difficult to reproduce at scale. Meanwhile, recent Virtual Reality (VR)-based teleoperation systems demonstrate that immersive interfaces can bridge human motion and robot embodiment [4], [5], yet these efforts are primarily designed for real-time control rather than systematic dataset construction. 

Motivated by these limitations, we introduce an open- 


Fig. 2. System overview of **MTC** . **MTC Capturer** : immersive VR-based system for collecting embodiment-scaled human locomotion trajectories in cluttered environments. **MTC Dataset** : a large-scale collection of locomotion trajectories recorded in procedurally generated cluttered scenes. **MTC Benchmark** : evaluation framework for measuring scene-aware locomotion behaviors relative to normal walking. 

source framework, Moving Through Clutter (MTC), for collecting and evaluating scene-aware humanoid locomotion data. Our approach combines procedural cluttered environment generation with embodiment-scaled virtual reality capture. By scaling the human operator to match the physical proportions of the target humanoid during data acquisition, the recorded trajectories become geometrically consistent with robot-scale locomotion, effectively transforming human-scale demonstrations into embodimentaligned motion data. The entire pipeline operates in virtual environments without requiring physical scene construction, enabling scalable and reproducible dataset generation under controlled clutter level and geometric difficulty. To systematically validate the collected trajectories, we further introduce a quantitative evaluation benchmark that measures locomotion difficulty and collision safety under geometric constraints, providing a standardized protocol for assessing scene-aware humanoid locomotion. The contributions of our MTC framework are summarized as follows: 

- MTC Capturer: An embodiment-scaled VR capture paradigm that produces geometrically consistent locomotion trajectories aligned with humanoid embodiment and procedurally generated 3D scenes with continuous clutteredness parameterization; 

- MTC Dataset: An open-source dataset that jointly provides whole-body locomotion trajectories and corresponding 3D scene configurations; and 

- MTC Benchmark: A dual evaluation benchmark that quantitatively measures locomotion difficulty and collision safety in geometrically constrained environments. 

## II. RELATED WORKS 

We review related work in learning humanoid locomotion, human motion datasets and VR teleoperation, and procedural simulation environment generation. 

## _A. Learning-Based Humanoid Locomotion_ 

Reinforcement learning has enabled significant progress in humanoid locomotion. Radosavovic et al. [6] and Haarnoja et al. [7] demonstrated robust sim-to-real transfer and agile dynamic behaviors, establishing that learning-based controllers can achieve stable and versatile locomotion. Human motion priors further accelerate this progress: DeepMimic [8] and Adversarial Motion Priors (AMP) [9] introduced exampleguided and style-based rewards derived from human demonstrations, while ExBody [10], ExBody2 [11], and SONIC [5] scaled whole-body tracking with large motion datasets. 

Despite these advances, existing policies are predominantly trained and evaluated on flat or sparsely structured terrain, where the primary challenge is balance and contact stability. Even terrain-variant settings typically consist of engineered primitives such as slopes or isolated obstacles. In contrast, locomotion in cluttered 3D indoor environments requires continuous modulation of torso orientation, lateral clearance, and full-body posture to avoid multi-height collisions. Current approaches achieve dynamic locomotion yet rarely condition control on detailed scene geometry, leaving geometry-conditioned traversal strategies largely unexplored. 

While Xue et al. [12] make an important step toward cluttered indoor traversal by introducing HumanoidPF as an informative representation and training traversal behaviors purely with RL, their formulation is primarily optimized for collision avoidance learnable via strong, hand-designed directional guidance—HumanoidPF is explicitly queried at body parts as policy observation and also shapes dense reward signals. As a result, the learned behaviors are naturally biased toward a compact set of goal-directed traversal skills (e.g., hurdle/crouch/squeeze) that can be efficiently acquired under such guidance, rather than toward rich, human-like, and reusable geometry-conditioned locomotion strategies grounded in large-scale demonstrations. This leaves open how to systematically capture and leverage diverse full-body locomotion data paired with the exact 3D scene geometry 

that induces it, so that policies can be learned not only to be collision-free, but also to be expressive, natural, and broadly reusable across clutter distributions. 

## _B. Human Motion Datasets and VR Teleoperation_ 

Large-scale motion capture datasets such as AMASS [3], BABEL [13], HumanML3D [14], and Motion-X [15] provide diverse human motion sequences and semantic annotations, substantially advancing motion modeling. However, these datasets are recorded in obstacle-free studios and do not encode explicit coupling between motion and environmental geometry, preventing models from learning how locomotion adapts to spatial constraints. 

Scene-aware datasets including PROX [16], SAMP [17], HUMANISE [18], and TRUMANS [19] introduce motion aligned with 3D indoor scenes. Yet they focus primarily on human motion prediction and generation characterized by quasi-static interactions from the computer vision perspective, limiting applicability to humanoid locomotion with different kinematics and actuation constraints, particularly for sustained traversal through narrow or irregular passages. 

VR-based teleoperation systems [4], [20]–[24] and retargeting frameworks [25], [26] demonstrate effective humanto-humanoid motion transfer. However, these efforts emphasize real-time control for loco-manipulation rather than systematically constructing reusable locomotion datasets paired with procedurally varied environments and quantitative benchmarking protocols. 

## _C. Procedural Simulation Environment Generation_ 

Procedural environment generation has primarily supported embodied navigation and visual understanding. ProcTHOR [27], Infinigen [28], [29], Holodeck [30], and Habitat [31] generate large-scale interactive indoor or outdoor scenes with semantic coherence and navigational accessibility. 

However, humanoid locomotion in cluttered indoor spaces is constrained by full-body volumetric clearance, multiheight collision risks, and kinematic feasibility. Existing procedural generators neither model embodiment-aware traversal constraints nor parameterize scene difficulty in terms of clearance margins or collision risk. As a result, they are not designed to support geometry-conditioned humanoid locomotion learning or benchmarking. 

Taken together, prior work has advanced locomotion control, motion modeling, teleoperation, and scene generation largely in isolation. What remains missing is a unified framework that couples procedural clutter generation, immersive embodiment-scaled locomotion data capture scalable by VR, motion retargeting, and quantitative benchmarking for sceneaware humanoid traversal in cluttered 3D environments. 

## III. MTC CAPTURER 

We now formalize the 3D scene-aware humanoid locomotion task and describe the MTC Capturer, the core data acquisition module that enables embodiment-scaled motion capture within generated cluttered environments in VR. 

## _A. Problem Formulation_ 

We consider goal-directed humanoid locomotion in cluttered 3D environments. Let a humanoid robot with kinematic model _K_ operate in a scene _S_ . The robot configuration space is denoted by _C_ , where a configuration **q** _∈ C_ encodes all joint configurations of the robot. A goal-directed humanoid locomotion task is specified by an initial configuration **q** 0 _∈ C_ and a goal set _G ⊂ C_ . A trajectory is defined as a timeordered sequence of configurations 


which is considered successful if its terminal configuration satisfies 


A traversal trajectory is considered valid only if it satisfies the following necessary conditions throughout execution: 

- **Collision safety.** The robot must remain collision-free with respect to the scene geometry at all times: 

   - _M_ robot( **q** _t, K_ ) _∩M_ env( _S_ ) = _∅, ∀t ∈{_ 0 _, . . . , T }._ 

   - Here _M_ robot( **q** _t, K_ ) denotes the robot body mesh obtained via forward kinematics and _M_ env( _S_ ) denotes the environment geometry. 

- **Postural stability.** The robot must maintain dynamic support throughout execution and must not undergo irrecoverable loss of balance. 

We denote by _T_ ( _S, K, G_ ) the set of trajectories that satisfy both goal completion defined by _G_ and the above physical feasibility conditions defined by _S_ and _K_ . 

## _B. Data-Driven Solutions with MTC Capturer_ 

Learning-based approaches require a humanoid robot dataset of embodiment-specific traversal trajectories, 


where each _τi_ is a physically feasible, goal-directed humanoid locomotion trajectory executed under the kinematic embodiment _K_ in a cluttered scene _Si_ . 

However, constructing _D_<sup>robot</sup> directly with real humanoid platforms is impractical. First, constructing geometryconditioned locomotion data requires a diverse distribution of scene geometries _S_ that impose structured 3D spatial constraints. Physical construction of such environments is costly and difficult to regulate systematically. Second, collecting collision-free and stable humanoid trajectories in such environments presupposes solving the scene-aware locomotion problem under study; moreover, human demonstration from direct teleoperation of highly articulated humanoids under tight geometric constraints is extremely challenging. 

To overcome these limitations, we introduce the **MTC Capturer** , a virtual-reality data collection pipeline that enables scalable scene generation and embodiment-consistent motion acquisition in VR. The MTC Capturer first procedurally generates geometrically diverse cluttered scenes in simulation to enable scalable environment construction, 

avoiding the need to set up any physical geometry in the real world. After that, it captures embodiment-scaled human reference motions as operators traverse these virtual environments, allowing geometric constraints to induce whole-body adaptation at the target robot’s proportions. Let 


denote a human reference motion sequence collected. The resulting motion is subsequently mapped to the humanoid configuration space through a retargeting function 


yielding robot traversal trajectories consistent with embodiment _K_ . MTC Capturer’s objective is therefore to construct a reproducible embodiment-consistent dataset that couples procedurally generated scene geometries with immersive human reference motions, 


where each sample consists of a generated scene _Si_ and an embodiment-scaled human reference motion _ξi_ . Corresponding robot trajectories are obtained via retargeting. 

The two components of MTC Capturer are detailed in the following subsections. The first component addresses scalable scene construction, while the second enforces embodiment-consistent geometry during motion acquisition. 

## _C. Procedural Environment Generation_ 

- A locomotion-relevant cluttered scene _S_ must satisfy three 

- essential requirements: 

- It must preserve the semantic characteristics of a realworld scenario. Scenes should reflect recognizable room types (e.g., bedroom, living room, and kitchen) with functionally meaningful object arrangements rather than arbitrary object scattering; 

- It must exhibit sufficient geometric clutter such that traversal cannot be accomplished by trivial straightline walking. Instead, the environment should induce constraint-driven whole-body adaptation, such as sidestepping through narrow passages, torso reorientation, crouching under height-constrained obstacles, or clearance-aware stepping; and 

- It must guarantee at least one feasible traversal path from a start to a goal for the target humanoid. 

- MTC Capturer addresses these three requirements through a structured procedural pipeline described below. 

_1) Geometric Regimes:_ Each scene is generated under one of two geometric regimes. The first structured domestic regime models semantically organized indoor layouts dominated by furniture-induced lateral confinement and corridorlike free space. The second debris-style regime introduces irregular obstacle configurations that create both planar entanglement and vertical clearance restrictions. In addition to dense and non-axis-aligned ground-level clutter, this regime incorporates overhead beams and structural elements that constrain height clearance, jointly inducing behaviors such as crouching, ducking, or crawling. Representative examples of the two regimes are shown in Fig. 3. 


Fig. 3. Examples of cluttered environments from two geometric regimes in MTC: structured domestic layouts (left) and debris-style layouts (right). 

_2) Semantic Layout Structure:_ Each scene begins by sampling a geometric regime and room type. To preserve structural coherence while enabling controllable variation, assets are organized into functional tiers and placed in a hierarchical order: 

- **Anchor Element Layer:** A dominant structural or functional component that defines the primary spatial organization of the scene. In structured domestic layouts, this corresponds to a functional core object (e.g., bed, sofa, and dining table), around which the room is organized. In the debris regime, the anchor role is fulfilled by major structural elements (e.g., load-bearing pillars or primary beam assemblies) that determine the global obstruction pattern. The anchor element is instantiated first according to regime-specific placement priors, ensuring plausible spatial structure. 

- **Supporting Large Elements Layer:** Large objects or structures that establish the dominant topology of the environment. In domestic layouts, these include wall-aligned furniture such as wardrobes, cabinets, or bookshelves. In the debris regime, these may include secondary pillars or extended structural members. Placement is performed via probabilistic sampling conditioned on room type and size tier, followed by rejection checks to avoid overlap. 

- **Small Clutter Layer:** Density-controlling objects that perturb navigable free space at a finer scale. These include freestanding items (e.g., chairs) as well as scattered small obstacles. Small clutter is injected after the primary layout has been established, allowing density to vary without altering global structure. 

- **Vertical Obstruction Layer (debris regime only):** Additional structural members (e.g., overhead beams, rebars, and I-shaped steel) are attached to pillars or walls to introduce height-clearance constraints. These elements create coupled planar and vertical restrictions, inducing crouching, ducking, or crawling behaviors beyond lateral navigation. 

During generation, anchor elements are instantiated first, followed by supporting large elements, and finally small clutter and regime-specific obstructions. This hierarchical layout strategy ensures that global spatial structure is determined before local density perturbations are introduced, preserving semantic plausibility while progressively shaping 

the navigable topology. 

Two diagonally opposite spawn zones, denoted as _Z_ start and _Z_ goal, are reserved as obstacle-free regions prior to placement, defining an origin–destination traversal pair. 

_3) Clutterness-Driven Density Control:_ To provide continuous and interpretable control over scene density, we introduce a scalar parameter _c ∈_ [0 _,_ 1] representing the target floor-occupancy ratio. Rather than manually specifying discrete object counts, the number of items injected into each placement layer is computed from the room area and the typical footprint size of assets in that layer. 

Let _A_ denote the room floor area. We allocate the clutterness budget only to non-anchor placement layers. Specifically, for each density-controlled layer _i ∈ {_ Supporting Large Elements _,_ Small Clutter _}_ , the target number of items is determined by 


Here, _wi_ is the weight that distributes the occupancy budget between large structural elements and small clutter, while the anchor element is instantiated independently of _wi_ and _c_ . _a_ ¯ _i_ denotes the mean ground-plane footprint area of all assets that can be assigned for that layer. The footprint _a_ ¯ _i_ is computed at runtime from each asset’s axis-aligned bounding box on the floor plane. This formulation ensures that the number of items scales proportionally with room size, and that larger assets naturally result in fewer instances under the same clutterness parameter _c_ due to their increased footprint. 

While the clutterness parameter _c_ controls obstacle density in expectation, high-density configurations may inadvertently eliminate feasible traversal paths for the target morphology. We therefore perform an explicit navigability verification step after object placement. 

_4) Morphology-Aware Navigability Verification:_ After object placement, scene feasibility is validated through a 2D grid-based reachability test. The floor is discretized at a fixed resolution. Before rasterization, each obstacle footprint is inflated by a configurable humanoid clearance radius _K_ , derived from the embodiment descriptor _K_ , effectively constructing a morphology-aware configuration-space map. The occupancy grid is then constructed from these inflated obstacles, and Breadth First Search is performed on the resulting free-space map. The search is initialized from all free cells within _Z_ start, and the scene is considered traversable if any cell within _Z_ goal can be reached. If no feasible traversal path exists, the scene is not discarded outright. Instead, we invoke a constraint-preserving annealed resampling procedure to restore connectivity while maintaining structural coherence. 

_5) Constraint-Preserving Annealed Resampling:_ If a candidate layout fails the reachability check, the system applies an annealing schedule that progressively removes assets while preserving structural elements. Small clutter—the most expendable layer—is reduced first via multiplicative decay (20% per annealing level), as these elements primarily perturb local free space without defining global structure. If connectivity remains unsatisfied, supporting large elements 

are subsequently reduced starting from the next annealing level using the same decay rate. Regime-defining anchor elements and major structural furniture are preserved until higher annealing stages, ensuring that the global spatial organization of the scene remains intact as long as the scene is physically navigable. This hierarchical relaxation policy defines a monotonic density schedule and guarantees convergence to a feasible layout given an appropriate scene size within a bounded number of retries while preserving structural coherence. 

Following annealed resampling, the realized clutterness level may differ from the originally specified target _c_ . We therefore define the realized density 


where _ak_ is the ground-plane footprint of each non-anchor object in the final layout. While _c_ controls density in expectation during sampling, _c_<sup>_′_</sup> reflects the actual floor occupancy ratio after reachability-constrained annealing. 

Collectively, hierarchical layout construction, morphology-aware verification, and constraint-preserving annealing yield semantically structured, density-controlled environments whose navigability is explicitly conditioned on the target humanoid embodiment. 

## _D. Embodiment-Scaled Immersive Motion Capture_ 

Standard motion-capture datasets record human motion at natural body proportions. When retargeted to a robot with different stature, geometric clearances experienced during capture may no longer correspond to those encountered by the robot, leading to unintended collisions or infeasible postures. To mitigate this embodiment mismatch, we enforce embodiment-consistent geometry during data collection. 

To match the scale of the humanoid and human operator, let _hr_ denote the standing height of the target robot and _ho_ the measured standing height of the human operator. We define the embodiment scale factor as _α_ = _hr/ho_ . During data collection, the virtual environment is rendered with a uniform scale factor 1 _/α_ , such that spatial clearances experienced by the operator correspond to those encountered by the robot at its embodiment scale. Joint poses are recorded at human scale and uniformly rescaled by the factor _α_ after capture, yielding an embodiment-consistent motion sequence expressed in the robot’s spatial scale. 

To match the skeletal structure of the humanoid and human operator, existing retargeting framework can be employed. For this work, we use General Motion Retargeting framework of Ze et al. [4] without modification. 

## IV. MTC DATASET AND BENCHMARK 

We introduce the MTC Dataset and Benchmark to support learning approaches and systematic evaluation of sceneaware humanoid locomotion in cluttered environments. 


Fig. 4. Distribution of realised floor-occupancy ratio _c_<sup>_′_</sup> across 145 generated scenes. Individual scene values are shown as jittered strips below the density curves; dashed lines indicate per-regime means. 

## _A. MTC Dataset_ 

_1) Dataset Overview:_ The MTC dataset consists of 145 procedurally generated scenes _{Sk}_ and 348 associated traversal trajectories _{ξj}_ collected under the Unitree G1 humanoid embodiment. Scenes span both geometric regimes, i.e., domestic and debris-style, and multiple semantic room types, e.g., bedroom, living room, and kitchen. While the target clutterness parameter _c_ is defined over [0 _,_ 1], empirical analysis under the G1 embodiment indicates that realised densities _c_<sup>_′_</sup> in the range [0 _._ 2 _,_ 0 _._ 6] most frequently correspond to geometrically challenging yet traversable layouts. 

Human motion is captured using a PICO 4 Ultra VR system with integrated full-body tracking, providing 24-joint skeletal pose measurements per frame. In total, the current dataset contains approximately 731,000 motion frames across 348 trajectories, corresponding to roughly 2.3 hours of humanoid locomotion data. Individual trajectories range from 431 to 6,939 frames in length, with a mean of 2,101 frames. The MTC dataset is actively expanding and the MTC capturer pipeline will be open-sourced to encourage community contributions. 

_2) Scene Density Distribution:_ To characterize geometric variability across the dataset, we analyze the distribution of realised clutterness levels _c_<sup>_′_</sup> over all generated scenes. Fig. 4 shows the kernel density estimates of _c_<sup>_′_</sup> for both regimes, computed as the fraction of room floor area occupied by non-anchor object footprints on a 5 cm rasterization grid. 

_3) Case Study: Goal-Conditioned Route Diversity:_ To illustrate the richness of geometry-induced behavior, we analyze a representative scene under four goal configurations. Fig. 5 presents the scene floor plan together with the groundplane projections of pelvis trajectories, along with representative snapshots of the corresponding obstacle-avoidance behaviors. Markers _•_ , _⋆_ , and _×_ denote start locations, goal positions, and obstacle avoidance maneuvers, respectively. 

Although all motions occur within the same environment, different goal placements induce distinct traversal routes that expose the agent to different local geometric constraints—such as narrow passages, low-clearance structures, or densely cluttered regions. This example illustrates that behavioral diversity in MTC arises not only from varying scene layouts, but also from goal-conditioned routing within 

a single environment. 

## _B. MTC Benchmark_ 

_1) Motion Adaptation Score:_ Locomotion under geometric constraints induces coordinated deviations from nominal flat-ground walking across multiple kinematic dimensions. To quantify geometry-induced whole-body adaptation, we evaluate trajectory statistics within four complementary subspaces: 

- _Posture_ : pelvis-relative joint positions and velocities, capturing configuration-level whole-body adjustments; 

- _Vertical motion_ : pelvis height, vertical velocity, and vertical acceleration, reflecting height-clearance adaptation; 

- _Foot interaction_ : foot heights and vertical velocities, characterizing stepping and obstacle negotiation; and 

- _Smoothness_ : third-order positional differences (jerk) across joints, measuring dynamic modulation under constraint. 

For each subspace, frame-wise feature vectors are extracted and summarized by their empirical mean and covariance. A reference distribution is estimated from a corpus of temporally aligned, speed-normalized flat-ground walking trajectories and approximated by a multivariate Gaussian. Given a test trajectory, we compute the Fréchet distance between its empirical feature distribution and the baseline distribution within the same subspace. The Fréchet distance captures both mean displacement and covariance shift, enabling joint evaluation of first- and second-order kinematic deviations. 


Subspace distances are normalized and aggregated via uniform weighting to produce a scalar adaptation score. Higher values indicate greater deviation from nominal flat-ground locomotion. The score is intended as a relative deviation measure rather than an absolute proxy for task difficulty. 

_2) Collision Safety Assessment:_ Physical feasibility within cluttered 3D geometry is treated as an explicit evaluation criterion in the MTC Benchmark. Given an evaluated trajectory _{_ **q** _t}_<sup>_T_</sup> _t_ =1<sup>andscenemesh</sup><sup>_M_,collisionsafetyis</sup> assessed via signed distance queries against the original (nonconvex) scene geometry. 

For each frame _t_ , forward kinematics maps the joint configuration **q** _t_ to world-frame link poses. Surface sample points are generated on each link and queried against a precomputed signed distance field of _M_ . Let _st,i_ denote the signed distance of sample point _i_ at frame _t_ , where negative values indicate penetration into the scene geometry. The frame-wise penetration depth is then defined as 


so that _dt_ = 0 indicates a collision-free configuration and _dt >_ 0 measures the maximum instantaneous penetration 


Fig. 5. Case study of goal-conditioned route diversity in a representative MTC scene. The left panel visualizes the scene floorplan together with the ground-plane projections of pelvis trajectories under four goal configurations. Markers _•_ , _⋆_ , and _×_ denote start locations, goal positions, and obstacleavoidance maneuvers, respectively. Insets (a–d) show representative locomotion behaviors observed along the corresponding routes: (a) crouched lateral shuffling, (b) crouched forward shuffling, (c) high-knee lateral step-over, and (d) prone crawling. 


depth at frame _t_ . Based on _{dt}dt}t}}_<sup>_T_</sup> _t_ =1<sup>,thebenchmarkreports</sup> four quantitative safety metrics: 

Here, _R_ col measures collision frequency over the trajectory, _d_ max captures the worst-case geometric violation, _d_<sup>¯</sup> cond quan- quantifies average penetration severity conditioned on collision events (defined as zero when no collision occurs), and _I_ pd reflects time-normalized penetration magnitude across the full traversal. Together, these metrics characterize both discrete collision occurrence and continuous penetration severity under full scene geometry. The evaluation code will be released as part of the MTC framework to ensure reproducibility. 

Fig. 6. PCA projections of per-frame kinematic features for four subspaces. Red: baseline level-ground walking; Blue: cluttered-environment trajectories. 

spaces, the dataset distributions extend substantially beyond the baseline patterns, indicating diverse posture and footinteraction adaptations induced by cluttered environments. 

_3) Dataset-Level Benchmark Statistics:_ To analyze the behavioral coverage of the collected trajectories, we examine the distribution of per-frame kinematic features across four subspaces, defined by MTC benchmark. For each subspace, feature vectors are extracted from all trajectories as well as from a baseline recording of unobstructed level-ground walking, and projected onto the first two principal components for visualization (Fig. 6). 

In the _smoothness_ subspace, the baseline and dataset distributions largely overlap, indicating that the collected trajectories remain consistently smooth despite geometric constraints—a property not always achieved by learned robot policies. 

Together, these projections confirm that the dataset captures a broad spectrum of posture and foot-interaction adaptations while maintaining high motion quality, providing a challenging and diverse benchmark for locomotion in cluttered environments. 

In the _posture_ subspace, baseline frames form a compact closed orbit consistent with a regular gait cycle. In the _foot_ subspace, the baseline distribution concentrates into a narrow, phase-structured wedge with two symmetric lobes, reflecting alternating left–right foot interactions rather than a closed loop. Similarly, in the _pelvis height_ subspace, baseline frames concentrate within a narrow band corresponding to the nearly constant pelvis height of normal walking. Across these sub- 

## V. CONCLUSION AND LIMITATIONS 

We presented MTC, a framework that comprises a data capturer, a dataset, and a benchmark for data-driven, scene- 

aware humanoid locomotion in cluttered 3D environments. The MTC Capturer leverages immersive VR to capture human locomotion in virtual 3D cluttered environments at scale. The MTC Dataset couples procedurally generated geometric regimes with embodiment-consistent traversal trajectories, while the MTC Benchmark evaluates trajectories along two complementary axes: geometry-induced kinematic adaptation and collision safety under full scene geometry. 

Through dataset-level analysis and goal-conditioned case studies, we demonstrate that MTC captures diverse wholebody adaptation induced by rich spatial constraints, rather than merely diversifying different scene layouts. Quantitative results show that distinct geometric regimes elicit measurably different traversal behaviors from human demonstrators, revealing structured adaptation patterns that existing benchmarks, which vary only scene layout or goal placement, are insufficient to characterize. Furthermore, the proposed benchmark metrics provide a principled protocol for analyzing locomotion performance under spatial constraints, offering actionable guidance for downstream algorithm development. 

Preliminary results show that a reinforcement learningbased motion tracking policy, trained to imitate MTC trajectories, can reproduce geometry-induced traversal behaviors with low collision rates. 

Despite these contributions, several limitations remain. First, the current pipeline employs scene-agnostic retargeting; fully scene-aware motion generation remains an open challenge requiring advances in control and learning. Second, scene layout generation relies on manually designed placement priors rather than learned distributions, which may not fully capture real-world variability. Integrating generative scene models such as Vision-Language Models could improve realism and diversity. Third, the dataset focuses on locomotion-centric traversal and does not model contactassisted progression, which may be necessary in extreme clutter where multi-contact support is required for balance. Finally, the VR-based motion capture relies on pose estimation and may introduce tracking noise. Our future work will incorporate high-precision motion capture to further improve accuracy. 

In summary, MTC provides a foundation for systematic study of geometry-induced adaptation in humanoid locomotion and stimulates further research on scene-aware humanoid planning and control with scalable data collection. 

## REFERENCES 

- [1] D. Kim, J. Bae, J. Lee, D. Son, and S. Oh, “Stage-wise reward shaping for acrobatic robots: A constrained multi-objective reinforcement learning approach,” _arXiv preprint_ , 2024. 

- [2] Y. Wang, S. Zhu, P. Zhi, Y. Li, J. Li, Y.-L. Li, Y. Xiao, X. Wang, B. Jia, and S. Huang, “OmniXtreme: Breaking the generality barrier in high-dynamic humanoid control,” _arXiv preprint_ , 2026. 

- [3] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black, “AMASS: Archive of motion capture as surface shapes,” in _Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV)_ , 2019, pp. 5442– 5451. 

- [4] Y. Ze, S. Zhao, W. Wang, A. Kanazawa, R. Duan, P. Abbeel, G. Shi, J. Wu, and C. K. Liu, “TWIST2: Scalable, portable, and holistic humanoid data collection system,” _arXiv preprint_ , 2025. 

- [5] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Castaneda, Z.-A. Cao, J. Li _et al._ , “SONIC: Supersizing motion tracking for natural humanoid whole-body control,” _arXiv preprint_ , 2025. 

- [6] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath, “Real-world humanoid locomotion with reinforcement learning,” _Sci. Robot._ , vol. 9, no. 89, p. eadi9579, 2024. 

- [7] T. Haarnoja, B. Moran, G. Lever, S. H. Huang, D. Tirumala, J. Humplik, M. Wulfmeier, S. Tunyasuvunakool, N. Y. Siegel, R. Hafner _et al._ , “Learning agile soccer skills for a bipedal robot with deep reinforcement learning,” _Sci. Robot._ , vol. 9, no. 89, p. eadi8022, 2024. 

- [8] X. B. Peng, P. Abbeel, S. Levine, and M. van de Panne, “DeepMimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Trans. Graph._ , vol. 37, no. 4, pp. 1–14, 2018. 

- [9] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “AMP: Adversarial motion priors for stylized physics-based character animation,” _ACM Trans. Graph._ , vol. 40, no. 4, pp. 1–20, 2021. 

- [10] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “Expressive whole-body control for humanoid robots,” in _Proc. Robot., Sci. Syst. (RSS)_ , 2024. 

- [11] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang, “ExBody2: Advanced expressive humanoid whole-body control,” _arXiv preprint_ , 2024. 

- [12] H. Xue, S. Liang, Z. Zhang, Z. Zeng, Y. Liu, Y. Lian, J. Wang, Q. Liu, X. Shi, and L. Yi, “Collision-free humanoid traversal in cluttered indoor scenes,” _arXiv preprint_ , 2025. 

- [13] A. R. Punnakkal, A. Chandrasekaran, N. Athanasiou, A. QuirosRamirez, and M. J. Black, “BABEL: Bodies, action and behavior with English labels,” in _Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)_ , 2021, pp. 722–731. 

- [14] C. Guo, S. Zou, X. Zuo, S. Wang, W. Ji, X. Li, and L. Cheng, “Generating diverse and natural 3D human motions from text,” in _Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)_ , 2022, pp. 5152–5161. 

- [15] J. Lin, A. Zeng, S. Lu, Y. Cai, R. Zhang, H. Wang, and L. Zhang, “Motion-X: A large-scale 3D expressive whole-body human motion dataset,” in _Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)_ , 2023. 

- [16] M. Hassan, V. Choutas, D. Tzionas, and M. J. Black, “Resolving 3D human pose ambiguities with 3D scene constraints,” in _Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV)_ , 2019, pp. 2282–2292. 

- [17] M. Hassan, D. Ceylan, R. Villegas, J. Saito, J. Yang, Y. Zhou, and M. J. Black, “Stochastic scene-aware motion prediction,” in _Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV)_ , 2021, pp. 11 374–11 384. 

- [18] Z. Wang, Y. Chen, T. Liu, Y. Zhu, W. Liang, and S. Huang, “HUMANISE: Language-conditioned human motion generation in 3D scenes,” in _Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)_ , 2022. 

- [19] N. Jiang, Z. Zhang, H. Li, X. Ma, Z. Wang, Y. Chen, T. Liu, Y. Zhu, and S. Huang, “TRUMANS: Scaling up dynamic humanscene interaction modeling,” in _Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)_ , 2024. 

- [20] T. He, Z. Luo, W. Xiao, C. Zhang, K. Kitani, C. Liu, and G. Shi, “Learning human-to-humanoid real-time whole-body teleoperation,” in _Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS)_ , 2024. 

- [21] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi, “OmniH2O: Universal and dexterous human-to-humanoid whole-body teleoperation and learning,” in _Proc. Conf. Robot Learn. (CoRL)_ , 2024. 

- [22] X. Cheng, J. Li, S. Yang, G. Yang, and X. Wang, “Open-TeleVision: Teleoperation with immersive active visual feedback,” in _Proc. Conf. Robot Learn. (CoRL)_ , 2024. 

- [23] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “HumanPlus: Humanoid shadowing and imitation from humans,” in _Proc. Conf. Robot Learn. (CoRL)_ , 2024. 

- [24] Y. Ze, Z. Chen, J. P. Araujo, Z.-a. Cao, X. B. Peng, J. Wu, and C. K. Liu, “TWIST: Teleoperated whole-body imitation system,” _arXiv preprint_ , 2025. 

- [25] J. P. Araujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu, “Retargeting matters: General motion retargeting for humanoid motion tracking,” in _Proc. IEEE Int. Conf. Robot. Autom. (ICRA)_ , 2026. 

- [26] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi, “OmniRetarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction,” _arXiv preprint_ , 2025. 

- [27] M. Deitke, E. VanderBilt, A. Herrasti, L. Weihs, J. Salvador, K. Ehsani, W. Han, E. Kolve, A. Farhadi, A. Kembhavi, and R. Mottaghi, 

   - “ProcTHOR: Large-scale embodied AI using procedural generation,” in _Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)_ , 2022. 

- [28] A. Raistrick, L. Lipson, Z. Ma, L. Mei, M. Wang, Y. Zuo, K. Kayan, H. Wen, B. Han, Y. Wang, A. Newell, H. Law, A. Goyal, K. Yang, and J. Deng, “Infinite photorealistic worlds using procedural generation,” in _Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)_ , 2023, pp. 12 630–12 641. 

- [29] A. Raistrick, L. Mei, K. Kayan, D. Yan, Y. Zuo, B. Han, H. Wen, M. Parakh, S. Alexandropoulos, L. Lipson, Z. Ma, and J. Deng, “Infinigen indoors: Photorealistic indoor scenes using procedural generation,” in _Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)_ , 2024. 

- [30] Y. Yang, F.-Y. Fan, K. Dickinson, J. Wu, D. Khashabi, Y. Choi, and A. Kembhavi, “Holodeck: Language guided generation of 3D embodied AI environments,” in _Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)_ , 2024. 

- [31] M. Savva, A. Kadian, O. Maksymets, Y. Zhao, E. Wijmans, B. Jain, J. Straub, J. Liu, V. Koltun, J. Malik, D. Parikh, and D. Batra, “Habitat: A platform for embodied AI research,” in _Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV)_ , 2019, pp. 9339–9347. 

