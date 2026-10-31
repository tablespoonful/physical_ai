---
title: "Learning to Evolve: Multi-modal Interactive Fields for Robust Humanoid Navigation in Dynamic Environments"
date: "2026-05-21"
authors: "Peifeng Jiang; Hong Liu; Jin Jin; Wenshuai Wang; Xia Li"
url: https://arxiv.org/abs/2605.21935
pdf: https://arxiv.org/pdf/2605.21935
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.21935)** / [論文ページ](https://arxiv.org/abs/2605.21935)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Learning to Evolve: Multi-modal Interactive Fields for Robust Humanoid Navigation in Dynamic Environments 

Peifeng Jiang<sup>1</sup> , Hong Liu<sup>1,*</sup> , Jin Jin<sup>2</sup> , Wenshuai Wang<sup>1</sup> , Xia Li<sup>3</sup> 

> 1 State Key Laboratory of General Artificial Intelligence, Peking University, Shenzhen Graduate School 

> 2 Oxford Robotics Institute, University of Oxford 

> 3 Institute for Machine Learning, Department of Computer Science, ETH Zurich 

jpf@stu.pku.edu.cn, hongliu@pku.edu.cn, jinjin@robots.ox.ac.uk, wangws@stu.pku.edu.cn, xia.li@inf.ethz.ch 


Fig. 1: **Multi-modal Interactive Fields (MIF) for Robust Humanoid Navigation.** We propose a hierarchical framework composed of three coupled fields: **(1) Appearance Field:** Provides dense semantic grounding for robust view synthesis. **(2) Spatial Field:** Maintains a dynamic topological Scene Graph that updates upon object relocation, enabling seamless re-planning from obsolete paths to correct trajectories. **(3) Geometry Field:** Generates water-tight meshes to ensure Interaction Pose Safety (IPS) before manipulation. 

**_Abstract_ —Safe manipulation-oriented navigation for humanoid robots requires scene memory that remains reliable under locomotion-induced perceptual distortion, environmental changes, and interaction-level geometric safety constraints. Existing semantic mapping and scene-graph systems are difficult to deploy directly in this setting because they often assume stable camera trajectories, static environments, or coarse object geometry. We introduce the Multi-modal Interactive Field (MIF), a humanoid-oriented system that integrates confidenceaware semantic 3D Gaussian Splatting, discrepancy-triggered spatial memory updates, and task-driven geometric reconstruction within a closed-loop perception-adaptation pipeline. MIF couples three fields: an uncertainty-aware 3DGS Appearance Field that suppresses gait-induced blur, a Spatial Field that maintains topological memory, and a Geometry Field that supports Interaction Pose Safety (IPS) before manipulation. A discrepancy** 

**detection score is introduced to separate locomotion-induced false-positive changes from persistent changes and updates only locally inconsistent regions. On a Unitree-G1 humanoid in a real dynamic office, MIF improves relocation success in non-static environments from 12% to 94% compared with static scene-graph memory, while reducing semantic memory footprint by 91.4% through feature distillation for practical online operation. Project page and code: https://ziya-jiang.github.io/MIF-homepage/.** 

**_Index Terms_ —Semantic Scene Understanding, Safe Navigation, Humanoid Robots, Active Perception, 3D Gaussian Splatting, Multiplex Interactive Learning** 

##### I. INTRODUCTION 

Humanoid robots are increasingly expected to operate in human-centric environments where navigation is tightly 

coupled with subsequent physical interaction. Approximate navigation to an object is therefore insufficient: the robot must reach a terminal stance and body configuration from which manipulation is collision-free, kinematically reachable, and stable. This requires scene memory that grounds openvocabulary semantics into reliable geometry while remaining robust to locomotion-induced perceptual distortion and environmental changes. 

Unlike wheeled platforms, humanoids introduce bipedal dynamics, including torso oscillations and abrupt viewpoint shifts, that can degrade egocentric RGB-D observations during mapping [44, 21]. This challenges a common assumption behind many semantic mapping and scene-graph pipelines, such as HOV-SG [46] and ConceptGraphs [16], which are typically built from stable, quasi-static observations. At the same time, such systems often follow a map-once-query-forever paradigm, whereas human environments contain relocated, removed, or newly introduced objects. Together, these assumptions expose two coupled failure modes for manipulationoriented humanoid navigation: 

- **P1: Locomotion-Induced Semantic-Geometric Distortion.** Humanoid locomotion induces camera jitter and noisy state estimation for pose that can cause unstable observations to be fused into the map. This produces blurred semantics and noisy geometry, degrading both object grounding and the surface evidence needed to compute a safe terminal interaction pose. 

- **P2: Map-Reality Mismatch under Scene Changes.** Real-world layouts change as objects are relocated, removed, or added, while static scene memories may continue to guide the robot toward obsolete coordinates. For a humanoid, stale memory not merely cause error in semantic grounding: it can lead to unsafe interaction poses, unnecessary re-planning, or failures to recognize task-relevant changes. 

To address these coupled failures, we propose the Multimodal Interactive Field (MIF), a humanoid-oriented system that maintains appearance, spatial, and geometry fields within a closed-loop perception-adaptation pipeline, as shown in Fig. 1. 

For P1, the Appearance Field builds a confidence-aware semantic 3D Gaussian Splatting representation in which each Gaussian carries a reliability estimate for identifying gaitcorrupted primitives. This reliability gate suppresses gaitcorrupted primitives during rendering and scene-graph construction, reducing the propagation of locomotion artifacts into semantic grounding. For interaction-level safety, the Geometry Field selects better views around the target object and uses a Flow Matching-based model [10, 27] to recover objectcentric meshes on demand. The recovered mesh provides the geometric proxy required by Interaction Pose Safety (IPS), allowing navigation completion to depend on collisionawareness, kinematically reachability, and stability rather than just coordinate-level arrival. 

For P2, MIF uses a closed-loop Interaction and Adaptation Mechanism that treats scene memory as locally revisable dur- 

ing task execution. Rather than globally re-scanning the environment, the system monitors a multi-modal discrepancy score _D_ between the live local graph and the stored global graph. Because _D_ is gated by reliability and aggregates positional, semantic, and relational evidence, it separates locomotioninduced false-positive changes from persistent scene changes. When _D_ exceeds the selected threshold, MIF triggers a spatially selective update that revises only the inconsistent region. This local evolution loop avoids the cost of global re-mapping while supporting adaptation to relocated, removed, and newly added objects. Accordingly, our contributions emphasize the integrated system: 

- MIF provides a humanoid-oriented integration of confidence-aware semantic 3D Gaussian Splatting, VLMbased scene-graph reasoning, and object-centric geometry recovery for manipulation-safety-aware navigation. 

- A discrepancy-triggered local update mechanism compares live and stored graph evidence, filters locomotioninduced false positives through confidence gating, and revises only inconsistent regions of the spatial memory. 

- Interaction Pose Safety (IPS) is formulated as a systemlevel navigation criterion, supported by target-centered view selection and on-demand Flow Matching-based mesh recovery. 

- Real-world validation on a Unitree G1 humanoid in a dynamic office reports task success, memory, and latency evidence for online deployment. Under non-static environment settings, MIF improves relocation success from 12% to 94% compared with static scene-graph memory. 

##### II. RELATED WORK 

##### _A. Semantic 3D Scene Representations_ 

Neural Radiance Fields (NeRF) [28] and Instant NGP [29] have advanced continuous 3D scene modeling. 3D Gaussian Splatting (3DGS) [22] further offers explicit primitives and real-time rendering, making it attractive for robotic mapping and online scene representations. To attach open-vocabulary semantics to such representations, prior work [23, 25, 34, 42, 26, 13, 14] integrates vision foundation models [25, 38, 33] into 3D fields. Extensions such as Gaussian Grouping [51], LangSplat [35], and Feature Splatting [36] distill or attach high-dimensional semantic features to Gaussian primitives for object-centric understanding, language querying, and editing. LangSplat reduces language-feature storage through a scene-wise autoencoder, while LatentBKI [47] studies openvocabulary mapping in visual-language latent spaces with quantifiable uncertainty. These methods reduce the cost of open-vocabulary 3D querying, but dense semantic embeddings can still impose nontrivial memory and latency overhead for online humanoid deployment. 

In parallel, motion-deblurring 3DGS methods such as Deblur-GS [32] reconstruct sharper Gaussian radiance fields from camera motion-blurred images, while uncertainty-aware methods such as PUP 3D-GS [17] estimate Gaussian sensitivity for pruning and efficient rendering. However, these lines of 

work are usually studied as reconstruction, feature storage, or pruning problems, rather than as a coupled humanoid system that must use the reliability signal for image rendering, scenegraph construction, and manipulation-safety verification. For humanoid deployment, bipedal locomotion can introduce gaitinduced artifacts, while dense semantic features can also create memory and latency costs. 

MIF addresses these constraints by integrating confidencegated semantic 3DGS with feature distillation: the former suppresses gait-corrupted primitives for P1, while the latter is an efficiency-enabling design for practical online deployment rather than a standalone novelty claim. 

##### _B. 3D Scene Graphs and Hierarchical Mapping_ 

3D Scene Graphs (3DSGs) provide a structured abstraction by organizing environments into floors, rooms, objects, and their relations [1, 46, 48, 45, 3]. Early systems such as KimeraSemantics [40] focused on geometric-semantic consistency, while Hydra [19] introduced real-time spatial perception. With the advent of large language and vision-language models [20], recent frameworks [46, 39, 5, 31, 52] leverage symbolic or language-conditioned reasoning for complex tasks. 

Dynamic scene-graph and spatio-temporal mapping methods, such as Khronos [41], further consider how scene memories evolve when objects move, disappear, or appear. ConceptGraphs [16] can also be adapted with periodic rescanning, providing a useful rescan-style baseline for testing whether scene memories can be refreshed after changes. Nevertheless, static scene-graph memories expose a map-once-query-forever failure mode, while dynamic or rescan-style alternatives may rely on revisiting, periodic rescanning, or sensing assumptions that differ from our non-revisiting humanoid navigation protocol. Moreover, graph nodes and coarse object boxes often lack the surface-level geometry needed to evaluate manipulationready terminal poses. 

MIF bridges this gap by coupling the Spatial Field with an on-demand Geometry Field, while using discrepancy-triggered updates to revise only inconsistent regions of the memory during navigation. 

##### _C. Generative Geometry for Embodied AI_ 

Robotic interaction requires reliable geometric priors, especially when only partial observations are available. Learningbased mesh generation has been studied through methods such as BSP-based reconstruction, Scan2Mesh, AtlasNet-style surface generation, and PolyGen [11, 12, 15, 30]. Generative models, including diffusion-based [18] and Flow Matchingbased [27] approaches, have further improved shape recovery from sparse or partial observations. Recent studies such as MeshGPT [43] and SAM-3D [10] explore object-centric completion that can support downstream manipulation. However, these generative priors are typically used as offline or objectcentric modules, rather than being integrated with online navigation and memory adaptation. 

MIF incorporates a Flow Matching-based Geometry Field that recovers object-centric meshes _on demand_ during the 

approaching phase and uses them as geometric proxies for Interaction Pose Safety (IPS) verification. Our use of generative geometry is therefore not a standalone mesh-generation contribution; rather, it provides an on-demand geometric proxy selected from target-centered views and used by IPS during humanoid navigation. 

##### _D. Active Perception and Interactive Learning_ 

Interactive perception [4] studies how an agent’s actions can reduce perceptual ambiguity. Related work spans low-level active SLAM [2, 54, 49, 24, 7] and high-level semantic exploration [53, 55, 9, 8]. Modern foundation models provide useful zero-shot priors, but they can still hallucinate or produce stale semantic assumptions in novel environments [6, 9]. Although active perception connects sensing with action, humanoidspecific constraints such as locomotion-induced viewpoint oscillations remain less explored. In contrast to coverageoriented exploration, MIF uses two task-driven mechanisms: target-centered view selection for interaction geometry and discrepancy-triggered local memory revision for map-reality conflicts. This makes scene memory locally revisable during navigation, moving the humanoid beyond passive use of a static map. 

##### III. METHODOLOGY 

We propose the Multi-modal Interactive Field (MIF), a humanoid-oriented system representation _M_ = _{Fapp, Fspat, Fgeom}_ for safe manipulation-oriented navigation from egocentric RGB-D observations. Unlike static mapping pipelines, MIF is designed to mitigate _locomotioninduced distortion_ (P1) and _map-reality mismatches_ (P2) by grounding language queries into spatial memory and interaction-ready geometry. The pipeline operates as a persistent perception-adaptation loop that incrementally stabilizes appearance, updates spatial memory, and verifies interaction geometry. The overview of the Multi-modal Interactive Fields (MIF) framework is shown in Fig 2. In the following sections, we detail: (i) the construction of the confidence-gated Appearance Field _Fapp_ via jitter-aware semantic 3DGS (Sec. III-A); (ii) the abstraction of the Spatial Field _Fspat_ from stabilized rendered views for semantic grounding and mismatch detection (Sec. III-B); and (iii) the on-demand generation of the Geometry Field _Fgeom_ for Interaction Pose Safety (IPS) verification (Sec. III-C). 

##### _A. Appearance Field Construction (Fapp)_ 

The Appearance Field _Fapp_ serves as the sensory grounding layer of MIF. Unlike standard reconstruction pipelines that assume relatively stable camera motion, _Fapp_ is designed to mitigate the semantic-geometric distortion (P1) caused by bipedal locomotion. Rather than directly fusing all raw frames, it uses per-Gaussian reliability to downweight observations likely affected by high-frequency torso oscillations and local pose uncertainty, producing a more view-consistent semantic radiance field. 


Fig. 2: **Overview of the Multi-modal Interactive Fields (MIF) framework. (Red)** Incremental Appearance Field: Constructs a dense semantic base by fusing 3DGS SLAM [50] with multi-modal features [33, 38] to generate confidence-aware maps. **(Blue)** Spatial Field: Abstracts the dense map into a topological Scene Graph, utilizing VLMs [20] to reason over object relationships from synthesized views. **(Green)** Geometry Field: Recovers high-fidelity meshes for interaction. It employs a Task-Driven View Selection strategy for object-centric geometry recovery by adapting a Flow-matching Transformer [10]. 

We represent the field as a collection of 3D Gaussian primitives _G_ = _{Gi}_ . Each primitive is augmented with a confidence scalar _Ci ∈_ [0 _,_ 1], which acts as a reliability gate for identifying and suppressing gait-corrupted primitives. 

_1) Jitter-Aware Confidence Estimation:_ To reduce transient artifacts such as motion blur and pose-induced misalignment, we introduce a differentiable confidence module. The key observation is that gait-corrupted primitives tend to remain optimization-unstable across training, whereas stable hightexture boundaries usually converge after multi-view optimization. Accordingly, we compute _Ci_ from each Gaussian’s weighted gradient magnitude and opacity, normalized by their global means as _gn,i_ and _αn,i_ , respectively. The subscript _n_ denotes normalization by the corresponding global mean. The gradient term aggregates instability from position, scale/rotation, color, and opacity updates, while opacity reflects whether a primitive has accumulated stable structural evidence. 

The confidence _Ci_ is then computed through a smooth gating mechanism that penalizes high instability while preserving structurally supported primitives: 


where _σ_ ( _·_ ) denotes the sigmoid function, which maps the term _γαn,i_ (1 _− gn,i_ ) into the range [0 _,_ 1]. _β_ controls the penalty on optimization instability and _γ_ controls the opacitybased reliability scaling. This mechanism downweights lowconfidence, ghosting-like artifacts in rendering and object re- 

liability estimation, reducing their influence on the subsequent spatial graph. 

_2) Open-Vocabulary Feature Distillation:_ To enable online semantic querying with bounded memory, we distill highdimensional CLIP/DINOv2 features [38, 33] into a compact 32-dimensional latent space **f** _i_<sup>_distill_</sup> _∈_ R<sup>32</sup> . This compression reduces the memory footprint needed to maintain large-scale semantic maps and supports practical online deployment (see Sec. IV-E). 

A co-trained MLP decoder projects the latent features back to the original CLIP/DINOv2 feature space for openvocabulary matching. Feature rendering follows standard alpha-blending but is weighted by the confidence metric so that unstable primitives contribute less to semantic evidence: 


Here, **F**<sup>_distill_</sup> ( **p** ) denotes the rendered distilled semantic feature at pixel **p** , obtained by accumulating per-primitive features along the ray. By coupling feature accumulation with _Ci_ , the field reduces semantic smearing (P1) and anchors semantic evidence primarily to stable regions. 

_3) Stabilized View Synthesis for Spatial Reasoning:_ Once optimized, _Fapp_ functions as a confidence-weighted rendering engine for downstream spatial reasoning. Instead of feeding raw, gait-affected camera frames to the perception stack, we render stabilized views _Istable_ from smoothed virtual trajectories. These rendered views reduce gait-induced artifacts before 

object detection and the extracting spatial relation, providing more stable evidence for subsequent Spatial Field construction. A later discrepancy-computation step uses the node positions, semantic features, and relation sets extracted from these views to determine whether a local memory update is needed. 

##### _B. Spatial Field Construction (Fspat)_ 

The Spatial Field _Fspat_ serves as the topological memory and reasoning layer of MIF. While _Fapp_ provides confidenceweighted visual evidence, _Fspat_ abstracts the scene into a hierarchical graph _Mspat_ = ( _V, E_ ) for high-level task reasoning. Its function is twofold: (1) grounding linguistic concepts into physical space using stabilized evidence, and (2) detecting likely Map-Reality Mismatches (P2) by comparing local and stored graph structure. 

_1) Graph Generation via Stabilized Re-perception:_ Direct object detection and semantic parsing on raw humanoid camera streams can suffer from segmentation jitter under gaitinduced viewpoint changes. We therefore employ a stabilized re-perception strategy. We query the optimized _Fapp_ to render confidence-weighted stabilized views _{Istable}_ . These rendered inputs reduce gait-induced artifacts before object detection and relation extraction, providing more stable evidence for scene-graph construction. Formally, each node _vi ∈V_ is represented as _vi_ = _{Si,_ Ω _i, Ai,_ **c** _i}_ , containing a semantic caption _Si_ , room affiliation _Ai_ , node reliability Ω _i_ , and 3D centroid **c** _i_ computed via confidence-weighted backprojection: 


where **x** _j_ denotes the mean position of the _j_ -th Gaussian primitive associated with node _vi_ . We define the node-level reliability score as Ω _i_ = _⟨Cj⟩j∈Ni_ , where _⟨·⟩_ denotes the arithmetic mean over associated Gaussians. This score acts as a reliability filter: detections supported mainly by lowconfidence primitives receive low Ω _i_ , reducing the chance that gait-induced artifacts or unstable semantic proposals become persistent graph nodes. 

_2) Detecting Map-Reality Mismatch via Discrepancy D:_ To address P2, the system must separate transient sensing artifacts from persistent environmental changes. We implement a closed-loop Interaction and Adaptation Mechanism that monitors a multi-modal discrepancy score _D_ . The agent compares a live local subgraph _Mloc_ against the stored global graph _Mspat_ . For a matched local-global node pair, the nodelevel discrepancy _δi_ is defined as: 


Here, **c**<sup>_loc_</sup> _i_ and **c**<sup>_glob_</sup> _j_ are matched local/global centroids,<sup>ˆ</sup> **f** _i_ and ˆ **f** _j_ are normalized semantic features, _wpos_ and _wsem_ weight geometric and semantic drift. This reduces the influence of low-confidence nodes on change detection, limiting false positives caused by motion blur or gait-induced artifacts (P1). The 

total discrepancy _D_ aggregates node-level shifts and relational changes: 


Here, _Vloc_ averages local node discrepancies, while _Eloc_ and _Espat_ are live and stored edge sets; ∆ and _| · |_ denote symmetric difference and cardinality, with _wrel_ weighting relational inconsistency. When _D > τ_ , the system treats the local region as a likely Map-Reality Mismatch and selectively updates only the inconsistent region using accumulated multiview evidence. Implementation-level definitions of the three fields and the partial graph-update procedure are provided in Sec. S.3 and Algorithm 1. 

##### _C. Geometry Field Construction (Fgeom)_ 

The Geometry Field _Fgeom_ serves as the interaction-safety layer of MIF. Although _Fapp_ and _Fspat_ enable semantic grounding and topological reasoning, their sparse or implicit geometry is insufficient for selecting terminal poses for manipulation. Safe humanoid manipulation benefits from explicit object surfaces that can support collision and reachability checks. To bridge this gap, _Fgeom_ functions as an on-demand module that recovers object-centric meshes from stable visual evidence and uses them to evaluate Interaction Pose Safety (IPS). 

_1) Task-Local View Selection for Interaction Geometry:_ To reduce geometric ambiguity before interaction, the agent employs a task-local active gaze strategy around the target object. This process samples candidate viewpoints in the local neighborhood of the object on a local hemisphere and ranks them by a geometric observation utility for the object’s interaction surfaces. We rank candidate viewpoints using the task-local utility _Q_ ( _k_ ): 


where **p** _k_ and **d** _k_ denote the position and optical-axis direction of candidate view _k_ , and **v** _ik_ = ( **c** _i −_ **p** _k_ ) _/∥_ **c** _i −_ **p** _k∥_ 2 is the normalized direction from the camera center to the object centroid **c** _i_ . The distance term favors nearby views, while ( **d** _k ·_ **v** _ik_ )<sup>_γ_</sup> favors foveal alignment between the optical axis and the object center. The confidence term favors views that observe high-reliability Gaussian neighborhoods, so the generative model is conditioned on stable evidence rather than gait-corrupted observations. This links active perception to interaction feasibility by improving the observability of surfaces that are relevant to the intended manipulation. 

_2) Conditional Flow Matching for 3D Mesh Recovery:_ To infer partially observed object surfaces ( _e.g._ , the occluded back side), we employ a Flow Matching-based [27] reconstruction model [10]. We formulate geometric recovery as a conditional generation problem. Specifically, the model learns a time-dependent vector field that transports a Gaussian noise 

distribution toward the target mesh distribution conditioned on the selected observation. 

This generation is conditioned on the selected view ranked by the task-local utility _Q_ ( _k_ ). By conditioning on this highconfidence visual evidence, the model recovers an objectcentric mesh that is consistent with the denoised observations from _Fapp_ and can be used by the IPS check. 

_3) Asynchronous Grounding and IPS Verification:_ To avoid blocking navigation during generative inference, we implement an asynchronous grounding pipeline. While the robot approaches the target, the selected-view mesh is synthesized asynchronously and aligned to the Gaussian support using scale-invariant ICP: 


Here, ICP estimates the rotation **R** , translation **t** , and scale _s_ that align each generated mesh point **x**<sup>_m_</sup> _gen_<sup>toitsnearest</sup> Gaussian-support point **x**<sup>_NN_</sup> _app_<sup>(</sup><sup>_m_)</sup> , with robust loss _ρ_ reducing outlier influence. The registered mesh _Mgen_ provides dense local geometry for evaluating the final standing pose **p** _se_ 3. 

_4) Interaction Pose Safety:_ The IPS score _SIP S_ ( **p** _se_ 3) is an operational safety criterion for checking whether the terminal pose is suitable for manipulation: 


where: 

- **I** _col_ ( Geometric Safety): evaluates the signed distance to _Mgen_ and checks whether the collision margin exceeds _δsafe_ . 

- **I** _ik_ ( Kinematic Reachability): returns 1 if a valid collision-free inverse-kinematics solution exists for reaching the target point **t** _obj_ . 

- **I** _stab_ ( Postural Stability): returns 1 if the projected center of mass (CoM) lies within the support polygon _Psup_ , defined by the foot contact region at pose **p** _se_ 3. 

Thus, navigation is considered complete only when the robot reaches a pose that is collision-free, kinematically reachable, and stable for the subsequent manipulation task, rather than merely arriving near the target coordinate. 

##### _D. Language-Conditioned Navigation and Adaptation_ 

The final stage converts language-conditioned goals into navigation and verification actions. Using the hierarchical structure of MIF, the system selects semantically grounded targets, verifies geometry-aware terminal poses, and updates local memory when persistent scene changes are detected. 

_1) Hierarchical Semantic Grounding:_ Following a hierarchical search strategy similar to [46], the agent parses a natural-language instruction ( _e.g._ , _“Grasp the blue mug on the table”_ ) into a _⟨_ Region _,_ Landmark _,_ Object _⟩_ triplet using a VLM [20]. The system sequentially queries _Fspat_ to constrain the search space by localizing the room, identifying 


Fig. 3: **Humanoid navigation control via Pure Pursuit.** The schematic illustrates the geometric tracking logic where the Unitree-G1 robot targets a lookahead point at distance _L_ along the planned trajectory. The heading error ∆ _θ_ is used to compute the required curvature _κ_ = 2 sin(∆ _θ_ ) _/L_ . The overlaid velocity curve demonstrates the adaptive scaling mechanism, where _L_ is dynamically adjusted to suppress oscillations and maintain humanoid balance during high-curvature maneuvers. 

the landmark, and retrieving the target object node _vi_ . The object’s centroid **c** _i_ , computed by Eq. 3, provides the initial navigation goal, while the final stance is verified by IPS before interaction. 

_2) Stability-Aware Execution and Safety Verification:_ To manage humanoid locomotion constraints, we use a stabilityaware local planner that prioritizes center-of-mass (CoM) stability when tracking the planned path. The planner scales velocity according to angular tracking error to reduce gaitinduced oscillations and preserve perception quality during motion, as shown in Fig. 3. 

Navigation completion is defined by the IPS criterion rather than simple coordinate arrival. Before manipulation, the agent evaluates the candidate stance against the registered geometry _Mgen_ . If the IPS checks indicate collision risk or insufficient reachability, the local planner adjusts the stance within the nearby feasible region and re-evaluates _SIP S_ . 

_3) Closed-Loop Memory Evolution:_ During navigation, the Interaction and Adaptation Mechanism uses new observations to validate the local consistency of the stored memory. The discrepancy score _D_ distinguishes between two operational cases: 

- Transient Discrepancy: temporary obstacles ( _e.g._ , moving people) trigger local avoidance without updating the persistent scene memory. 

- Structural Mismatch: a persistent increase in _D_ above _τ_ indicates a likely map-reality conflict ( _e.g._ , relocated furniture). The system then scans the discrepant region, updates only the locally inconsistent parts of _Fapp_ and _Fspat_ , and re-grounds the query in the updated topology. 

##### IV. EXPERIMENTAL EVALUATION 

The experiments evaluate whether MIF enables a humanoid robot to maintain, query, and revise a multi-modal scene memory during real-world navigation and interaction. We organize the evaluation around the two vulnerabilities introduced earlier: locomotion-induced semantic-geometric distortion (P1) and map-reality mismatch under scene changes (P2). The main paper reports the following three questions, with additional implementation details and visualizations provided in the supplementary material. 

- **Q1 (Solving P1):** Can the Appearance and Spatial Fields preserve semantic grounding under bipedal camera jitter and fast walking? 

- **Q2 (Enabling Interaction):** Does target-centered geometry reconstruction improve IPS-verified interaction feasibility compared with point-cloud and static-fusion alternatives? 

- **Q3 (Solving P2):** Can the discrepancy-triggered adaptation loop distinguish persistent scene changes from transient sensing artifacts and update only inconsistent local memory? 

Because the system spans mapping, semantic grounding, interaction safety, and memory adaptation, we report the tasklevel evidence in the main paper and keep extended qualitative sequences and parameter settings in the supplementary. 

##### _A. Experimental Setup_ 

We conduct real-world experiments in an approximately 100 m<sup>2</sup> office environment containing more than 100 object categories, where objects can be relocated, removed, or newly introduced after mapping. The full ROS1 [37] system runs on a centralized workstation with an NVIDIA RTX 4090 and communicates with a Unitree G1 humanoid during navigation and interaction trials. All compared methods use the same SLAM backend where applicable, so the reported differences mainly reflect memory construction, semantic grounding, geometry reconstruction, and adaptation. The supplementary material provides additional system implementation details, hyperparameter settings, and qualitative visualization results. 

The baselines are selected according to each question rather than treated as a single universal set. 

- For semantic-feature baselines, we include FeatureSplatting [36], LangSplat [35], LatentBKI [47], and MIF variants with different feature dimensions. 

- For scene-graph and dynamic-memory baselines, we compare with HOV-SG [46], ConceptGraphs [16] with periodic rescanning, and Khronos [41] when evaluating adaptation after scene changes, without allowing a separate global rescan before task execution. 

- For rendering robustness under humanoid walking, we further compare against Deblur-GS and PUP-3DGS using slow- and fast-walk image-quality metrics. 

##### _B. Robust Semantic Grounding under Distortion (Q1)_ 

This experiment evaluates whether confidence-gated rendering in _Fapp_ provides stable evidence for semantic localization 

and graph construction in _Fspat_ under P1. The Unitree G1 receives open-vocabulary object queries, such as “Find the water bottle”, and must localize the target in the current scene memory. 

_1) Quantitative Results:_ Following HOV-SG, a query is counted as successful when the predicted object matches the ground-truth category and its centroid is within 1 _._ 0 m of the target. Because interaction requires tighter spatial accuracy than goal-level navigation, we also report mean distance error (MDE). Table I shows that MIF improves task-level semantic localization under humanoid motion, with higher success rate and lower MDE than HOV-SG and Feature-Splatting in this setup. The lower MDE suggests that confidence-gated integration suppresses locomotion-induced smearing that otherwise shifts semantic anchors away from object centers. 

TABLE I: Quantitative results of semantic grounding under locomotion-induced distortion. 

|**Method**|**Success Rate**|**MDE (m)**|**Latency (s)**|
|---|---|---|---|
|Feature-Splatting [36]|65%|0.42|3.2|
|HOV-SG [46]|74%|0.35|2.8|
|**MIF (Ours)**|**92%**|**0.18**|**1.6**|


To isolate rendering robustness, Table II compares MIF with Deblur-GS and PUP-3DGS under slow and fast walking. 

TABLE II: Rendering results under slow (S-) and fast (F-) walk. 

|**Method**|**S-PSNR**_↑_|**S-SSIM**_↑_|**F-PSNR**_↑_|**F-SSIM**_↑_|
|---|---|---|---|---|
|w/o Confidence|28.4|0.88|21.6|0.72|
|Deblur-GS [32]|25.14|0.80|24.67|0.70|
|PUP-3DGS [17]|20.44|0.67|17.89|0.53|
|**MIF** _Ci_ **(Ours)**|**31.2**|**0.93**|**29.8**|**0.89**|


MIF is not using confidence only for visual quality; the same reliability estimate is used to gate map integration and reduce unstable evidence before graph construction. 

Table III further shows that scene graphs constructed from stabilized rendered views achieve better object localization than those constructed from raw walking frames, especially under fast walking. 

TABLE III: Semantic object localization on scene graphs constructed from rendered vs. raw frames. 

|**Input Source**|**Recall**_↑_|**Precision**_↑_|**mAP**_↑_|
|---|---|---|---|
|Raw frames (Slow)|0.87|0.91|0.84|
|Raw frames (Fast)|0.61|0.79|0.58|
|**MIF Rendered (Slow)**|**0.94**|**0.95**|**0.93**|
|**MIF Rendered (Fast)**|**0.92**|**0.94**|**0.91**|
|Static camera (Ref.)|_∼_1.00|_∼_1.00|_∼_1.00|


##### _C. High-fidelity Geometry for Interaction Safety (Q2)_ 

This experiment evaluates the transition from object semantic grounding and navigation to IPS-verified interaction. We 

test whether the Geometry Field provides a safer physical proxy for terminal interaction poses than sparse point-cloud or static-fusion alternatives. 

_1) The Necessity of High-fidelity Geometry:_ Compared with raw point-cloud planning, MIF reduces IPS failure from 38% to 6% in our trials, mainly because continuous surfaces expose feasible clearances more reliably than sparse point clouds formed by Gaussian centers. The point-cloud baseline often misses surface connectivity, while the static mesh baseline can preserve locomotion-induced artifacts that occlude otherwise feasible workspaces. 

For safety, sparse point clouds can make IPS checks unreliable: without continuous surface connectivity, they provide incomplete normal and boundary information for manipulation, causing **I** _col_ to mark some risky poses as feasible. The generated watertight meshes reduce this failure mode and make the collision term in IPS better aligned with physical contact constraints. 

_2) Interaction Performance:_ We count an interaction trial as successful only when the robot arrives and the terminal pose satisfies _SIP S_ = 1. MIF achieves a mean terminal position error of 0 _._ 12 m in these trials. This precision supports the reachability check **I** _ik_ , since larger terminal errors can move the target outside the feasible manipulation workspace.. 

The active viewpoint score _Q_ ( _k_ ) is reported as a task-local geometric observation utility: it selects views with better distance, alignment, and high-confidence Gaussian support before mesh reconstruction. These cleaner conditioning views support Flow-Matching reconstruction and improve IPS performance as part of the overall system. 

- _3) Baseline Comparison Analysis:_ To examine these gains, 

- we compared MIF against two ablative baselines: 

- Pt-Cloud Baseline: Pt-Cloud plans on sparse Gaussian centroids; without surface connectivity, collision checks can be unreliable around gaps. 

- Static Mesh Baseline: Static Mesh uses TSDF fusion without the confidence gate; locomotion artifacts can be integrated into the mesh and reduce feasible terminalpose estimates. 

As shown in Table IV, MIF attains 94% IPS success with no observed collisions, suggesting that confidence-gated mapping and on-demand geometry are complementary for interaction safety. 

TABLE IV: Interaction Feasibility Comparison. We compare our generative approach against a Pt-Cloud Baseline and a Static Mesh Baseline. 

|**Method**|**IPS Success (%)**|**Nav. Err. (m)**|**Collision Rate**|
|---|---|---|---|
|Pt-Cloud|62%|0.28|32%|
|Static Mesh|78%|0.22|14%|
|**MIF (Ours)**|**94%**|**0.12**|**0%**|


_D. Dynamic Adaptation to Map-Reality Mismatches (Q3)_ 

This experiment evaluates whether the discrepancytriggered adaptation loop mitigates P2 after the initial map 

becomes stale. After initial mapping, we introduce three types of scene changes: object relocation, removal, and addition. For relocation, the target is moved by more than 1 _._ 5 m, and the robot must adapt during task execution without a separate global rescan after the scene change. 

_1) Evaluation Protocol:_ A trial is successful only if the robot either reaches the target’s current physical location with an IPS-valid final pose or correctly reports that the target has been removed. Arriving at obsolete memory coordinates is counted as failure. All methods start from the same initial map and post-change task condition, and no method is allowed to perform a separate global rescan before task execution. During execution, each method uses the observations produced by its own navigation or adaptation strategy. 

_2) Results Analysis:_ During navigation, MIF compares the live local graph with the stored Spatial Field using _D_ , which aggregates positional, semantic, and relational evidence. Fig. 4 illustrates how a detected discrepancy triggers a local Spatial Field update after scene changes. Table V reports the ROCbased threshold selection used to set _τ_ = 0 _._ 45, showing the trade-off between change recall and false-positive updates. 

TABLE V: ROC-based threshold selection in real scenarios. 

|**Threshold** **_τ_**|**True Positive Rate**_↑_|**False Positive Rate**_↓_|**F1**_↑_|
|---|---|---|---|
|0.25|99.2%|18.7%|0.817|
|0.35|97.8%|9.3%|0.893|
|**0.45 (Ours)**|**95.1%**|**4.2%**|**0.934**|
|0.55|89.6%|1.8%|0.913|
|0.65|78.3%|0.7%|0.866|


This threshold is fixed for all scene-change trials. Table VI then compares static-memory, periodic-rescan, dynamic scenegraph, and MIF variants under the same setting. HOV-SG has low success when the target is no longer at the stored coordinates, while ConceptGraphs+Rescan and Khronos provide stronger baselines for evaluating whether scene memories can be revised after changes. For MIF, we report two stages to separate performance without memory revision from the final performance after memory revision is enabled. MIF (Initial) disables the local memory update mechanism and only uses local observations near the obsolete memory location; it can still succeed when the relocated object remains visible or close enough for local perception and planning. MIF (Post-Update) reports the final success rate of the full system, including the initially solved cases and the additional cases recovered after _D > τ_ triggers active scanning, local graph revision, and replanning. 

##### _E. System Efficiency_ 

We finally report computational cost because online humanoid deployment requires a balanced allocation of computational resources, with sufficient headroom for perception, language grounding, geometry generation, and control. 

Table VII compares MIF’s 32D and 64D variants with LangSplat, LatentBKI, and FeatSplat under slow and fast walking. 


Fig. 4: **Dynamic adaptation of the hierarchical scene graph to environmental changes.** (a) **Detection** : Upon arriving at the goal, the G1 robot detects a structural discrepancy ( _e.g._ , a moved sofa) that contradicts its prior memory, triggering an increase in the discrepancy score _D_ . (b) **Resolution** : MIF initiates a local update of the Spatial Field with fresh observations. The updated graph better aligns with the physical reality, reducing _D_ and improving consistency for subsequent tasks. 

TABLE VI: Scene-change task success without a separate global rescan before task execution. Reloc/Remov/Addit denote relocated ( _>_ 1 _._ 5m), removed, and newly added objects. MIF (Initial) uses local observations near the obsolete memory location without local memory revision, while MIF (PostUpdate) reports final task success after active scanning, local graph revision, and replanning are enabled. 

|**Method**|**Reloc SR**_↑_|**Remov SR**_↑_|**Addit SR**_↑_|
|---|---|---|---|
|HOV-SG [46]|12%|10%|0%|
|ConceptGraphs + Rescan [16]|38%|35%|12%|
|Khronos [41]|_∼_18%|61%|_∼_12%|
|MIF (Initial)|64%|68%|42%|
|**MIF (Post-Update)**|**94%**|**98%**|**86%**|


> _~~∗~~_ The two-session protocol first builds the initial map, then changes the scene and evaluates task completion during post-change navigation. The robot is not required to exactly repeat the initial mapping trajectory. 

TABLE VII: Semantic localization under slow (S-) and fast (F-) walk conditions, memory usage, and latency. 

|**Method**|**VRAM**_↓_**(GB)**|**Latency**_↓_**(s)**|**S-SR**_↑_|**F-SR**_↑_|
|---|---|---|---|---|
|LangSplat [35]|18.45|2.3|95%|72%|
|LatentBKI-64D [47]|23.5|7.1|**98%**|74%|
|FeatSplat-32D [36]|4.8|3.2|81%|59%|
|**MIF 64D (Ours)**|18.0|4.6|92%|**88%**|
|**MIF 32D (Ours)**|_<_**4.0**|**1.6**|90%|86%|


the tested office map, leaving capacity for the VLM/LLM and mesh-generation modules on the RTX 4090. 

##### V. CONCLUSION 

We presented Multi-modal Interactive Field (MIF), a humanoid-oriented system for manipulation-safety-aware navigation in changing indoor environments. MIF integrates a confidence-aware Appearance Field, a topology-aware Spatial Field, and an object-centric Geometry Field to mitigate locomotion-induced semantic-geometric distortion (P1) and map-reality mismatch under scene changes (P2). On a Unitree G1 humanoid, MIF achieves 92% semantic-grounding success, 94% IPS success with no observed collisions, and final adaptation success rates of 94%, 98%, and 86% for relocation, removal, and addition. These results suggest that coupling reliability estimation, discrepancy-based local memory revision, and target-centered geometry verification improves humanoid interaction in non-static environments. Remaining limitations include several-second geometry generation latency and reliance on a centralized RTX 4090 workstation; future work will reduce latency, move more computation onboard, and develop multiplex interactive learning so that visual, spatial, geometric, and human feedback can jointly refine the robot’s memory and adaptation policy over repeated interactions. 

##### ACKNOWLEDGMENTS 

In practice, _Fapp_ supports real-time incremental updates at 22 FPS, while the asynchronous generation of _Fgeom_ takes around 6.2s and is scheduled during approach or verification rather than blocking low-level control. The 32D semantic feature field further reduces VRAM usage to below 4GB for 

This work is jointly supported by the National Natural Science Foundation of China (No.62373009), and Guangdong S&T Program (No.2024B0101050002). We specifically thank Jin Jin for his critical insights into the overall methodology and extensive revisions of the manuscript. 

REFERENCES 

- [1] Iro Armeni, Zhi-Yang He, JunYoung Gwak, Amir R Zamir, Martin Fischer, Jitendra Malik, and Silvio Savarese. 3d scene graph: A structure for unified semantics, 3d space, and camera. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 5664–5673, 2019. 

- [2] Ruzena Bajcsy. Active perception. _Proceedings of the IEEE_ , 76(8):966–1005, 1988. 

- [3] Hriday Bavle, Jose Luis Sanchez-Lopez, Muhammad Shaheer, Javier Civera, and Holger Voos. Situational graphs for robot navigation in structured indoor environments. _IEEE Robotics and Automation Letters_ , 7(4): 9107–9114, 2022. 

- [4] Jeannette Bohg, Karol Hausman, Bharath Sankaran, Oliver Brock, Danica Kragic, Stefan Schaal, and Gaurav S Sukhatme. Interactive perception: Leveraging action in perception and perception in action. _IEEE Transactions on Robotics_ , 33(6):1273–1291, 2017. 

- [5] Georgia Chalvatzaki, Ali Younes, Daljeet Nandha, An Thai Le, Leonardo FR Ribeiro, and Iryna Gurevych. Learning to reason over scene graphs: a case study of finetuning gpt-2 into a robot language model for grounded task planning. _Frontiers in Robotics and AI_ , 10:1221739, 2023. 

- [6] Matthew Chang, Th´eophile Gervet, Mukul Khanna, Sriram Yenamandra, Dhruv Shah, So Yeon Min, Kavit Shah, Chris Paxton, Saurabh Gupta, Dhruv Batra, et al. Goat: Go to any thing. In _Robotics: Science and Systems (RSS)_ , 2024. 

- [7] Devendra Singh Chaplot, Dhiraj Gandhi, Saurabh Gupta, Abhinav Gupta, and Ruslan Salakhutdinov. Learning to explore using active neural slam. In _International Conference on Learning Representations (ICLR)_ , 2020. 

- [8] Devendra Singh Chaplot, Dhiraj Prakashchand Gandhi, Abhinav Gupta, and Russ R Salakhutdinov. Object goal navigation using goal-oriented semantic exploration. _Advances in Neural Information Processing Systems (NeurIPS)_ , 33:4247–4258, 2020. 

- [9] Junting Chen, Guohao Li, Suryansh Kumar, Bernard Ghanem, and Fisher Yu. How to not train your dragon: Training-free embodied object goal navigation with semantic frontiers. 2024. 

- [10] Xingyu Chen, Fu-Jen Chu, Pierre Gleize, Kevin J Liang, Alexander Sax, Hao Tang, Weiyao Wang, Michelle Guo, Thibaut Hardin, Xiang Li, et al. Sam 3d: 3dfy anything in images. _arXiv preprint arXiv:2511.16624_ , 2025. 

- [11] Zhiqin Chen, Andrea Tagliasacchi, and Hao Zhang. Bspnet: Generating compact meshes via binary space partitioning. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 45–54, 2020. 

- [12] Angela Dai and Matthias Nießner. Scan2mesh: From unstructured range scans to 3d meshes. In _Proceedings of the IEEE/CVF Conference on Computer Vision and_ 

- _Pattern Recognition (CVPR)_ , pages 5574–5583, 2019. 

- [13] Francis Engelmann, Fabian Manhardt, Michael Niemeyer, Keisuke Tateno, and Federico Tombari. Opennerf: Open set 3d neural scene segmentation with pixel-wise features and rendered novel views. In _International Conference on Learning Representations (ICLR)_ , volume 2024, pages 8396–8407, 2024. 

- [14] Samir Yitzhak Gadre, Mitchell Wortsman, Gabriel Ilharco, Ludwig Schmidt, and Shuran Song. Cows on pasture: Baselines and benchmarks for language-driven zeroshot object navigation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 23171–23181, 2023. 

- [15] Thibault Groueix, Matthew Fisher, Vladimir G Kim, Bryan C Russell, and Mathieu Aubry. A papier-mˆach´e approach to learning 3d surface generation. In _Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 216–224, 2018. 

- [16] Qiao Gu, Ali Kuwajerwala, Sacha Morin, Krishna Murthy Jatavallabhula, Bipasha Sen, Aditya Agarwal, Corban Rivera, William Paul, Kirsty Ellis, Rama Chellappa, et al. Conceptgraphs: Open-vocabulary 3d scene graphs for perception and planning. In _IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5021–5028, 2024. 

- [17] Alex Hanson, Allen Tu, Vasu Singla, Mayuka Jayawardhana, Matthias Zwicker, and Tom Goldstein. Pup 3dgs: Principled uncertainty pruning for 3d gaussian splatting. In _Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)_ , pages 5949–5958, 2025. 

- [18] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. _Advances in neural information processing systems (NeurIPS)_ , 33:6840–6851, 2020. 

- [19] Nathan Hughes, Yun Chang, and Luca Carlone. Hydra: A real-time spatial perception engine for 3d scene graph construction and optimization. _Robotics: Science and Systems (RSS)_ , 2022. 

- [20] Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, Alec Radford, et al. Gpt4o system card. _arXiv preprint arXiv:2410.21276_ , 2024. 

- [21] Shuuji Kajita, Fumio Kanehiro, Kenji Kaneko, Kazuhito Yokoi, and Hirohisa Hirukawa. The 3d linear inverted pendulum mode: A simple modeling for a biped walking pattern generation. In _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , volume 1, pages 239–246, 2001. 

- [22] Bernhard Kerbl, Georgios Kopanas, Thomas Leimk¨uhler, and George Drettakis. 3d gaussian splatting for real-time radiance field rendering. _ACM Trans. Graph._ , 42(4):139– 1, 2023. 

- [23] Justin Kerr, Chung Min Kim, Ken Goldberg, Angjoo Kanazawa, and Matthew Tancik. Lerf: Language embedded radiance fields. In _Proceedings of the IEEE/CVF_ 

_International Conference on Computer Vision (CVPR)_ , pages 19729–19739, 2023. 

- [24] Ayoung Kim and Ryan M Eustice. Perception-driven navigation: Active visual slam for robotic area coverage. In _IEEE International Conference on Robotics and Automation (ICRA)_ , pages 3196–3203, 2013. 

- [25] Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C Berg, Wan-Yen Lo, et al. Segment anything. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 4015–4026, 2023. 

- [26] Sosuke Kobayashi, Eiichi Matsumoto, and Vincent Sitzmann. Decomposing nerf for editing via feature field distillation. _Advances in Neural Information Processing Systems (NeurIPS)_ , 35:23311–23330, 2022. 

- [27] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matthew Le. Flow matching for generative modeling. In _The Eleventh International Conference on Learning Representations (ICLR)_ , 2023. 

- [28] Ben Mildenhall, Pratul P Srinivasan, Matthew Tancik, Jonathan T Barron, Ravi Ramamoorthi, and Ren Ng. Nerf: Representing scenes as neural radiance fields for view synthesis. _Communications of the ACM_ , 65(1):99– 106, 2021. 

- [29] Thomas M¨uller, Alex Evans, Christoph Schied, and Alexander Keller. Instant neural graphics primitives with a multiresolution hash encoding. _ACM transactions on graphics_ , 41(4):1–15, 2022. 

- [30] Charlie Nash, Yaroslav Ganin, SM Ali Eslami, and Peter Battaglia. Polygen: An autoregressive generative model of 3d meshes. In _International conference on machine learning (ICML)_ , pages 7220–7229. PMLR, 2020. 

- [31] Zhe Ni, Xiaoxin Deng, Cong Tai, Xinyue Zhu, Qinghongbing Xie, Weihang Huang, Xiang Wu, and Long Zeng. Grid: Scene-graph-based instruction-driven robotic task planning. In _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 13765–13772, 2024. 

- [32] Jeongtaek Oh, Jaeyoung Chung, Dongwoo Lee, and Kyoung Mu Lee. Deblurgs: Gaussian splatting for camera motion blur. _arXiv preprint arXiv:2404.11358_ , 2024. 

- [33] Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin ElNouby, et al. Dinov2: Learning robust visual features without supervision. _Transactions on Machine Learning Research Journal_ , pages 1–31, 2024. 

- [34] Songyou Peng, Kyle Genova, Chiyu Jiang, Andrea Tagliasacchi, Marc Pollefeys, Thomas Funkhouser, et al. Openscene: 3d scene understanding with open vocabularies. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 815–824, 2023. 

- [35] Minghan Qin, Wanhua Li, Jiawei Zhou, Haoqian Wang, and Hanspeter Pfister. Langsplat: 3d language gaussian 

splatting. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 20051–20060, 2024. 

- [36] Ri-Zhao Qiu, Ge Yang, Weijia Zeng, and Xiaolong Wang. Language-driven physics-based scene synthesis and editing via feature splatting. In _European conference on computer vision (ECCV)_ , pages 368–383, 2024. 

- [37] Morgan Quigley, Ken Conley, Brian Gerkey, Josh Faust, Tully Foote, Jeremy Leibs, Rob Wheeler, Andrew Y Ng, et al. Ros: an open-source robot operating system. In _IEEE International Conference on Robotics and Automation Workshop on Open Source Software_ , volume 3, page 5, 2009. 

- [38] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _International Conference on Machine Learning (ICML)_ , pages 8748–8763, 2021. 

- [39] Krishan Rana, Jesse Haviland, Sourav Garg, Jad AbouChakra, Ian Reid, and Niko Suenderhauf. Sayplan: Grounding large language models using 3d scene graphs for scalable robot task planning. In _Conference on Robot Learning (CoRL)_ , pages 23–72. PMLR, 2023. 

- [40] Antoni Rosinol, Arjun Gupta, Marcus Abate, Jingnan Shi, and Luca Carlone. 3d dynamic scene graphs: Actionable spatial perception with places, objects, and humans. In _Robotics: Science and Systems (RSS)_ , 2020. 

- [41] Lukas Schmid, Marcus Abate, Yun Chang, and Luca Carlone. Khronos: A unified approach for spatio-temporal metric-semantic slam in dynamic environments. 2024. 

- [42] Jin-Chuan Shi, Miao Wang, Hao-Bin Duan, and ShaoHua Guan. Language embedded 3d gaussians for openvocabulary scene understanding. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 5333–5343, 2024. 

- [43] Yawar Siddiqui, Antonio Alliegro, Alexey Artemov, Tatiana Tommasi, Daniele Sirigatti, Vladislav Rosov, Angela Dai, and Matthias Nießner. Meshgpt: Generating triangle meshes with decoder-only transformers. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 19615– 19625, 2024. 

- [44] Olivier Stasse, Andrew J Davison, Ramzi Sellaouti, and Kazuhito Yokoi. Real-time 3d slam for humanoid robot considering pattern generator information. In _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 348–355, 2006. 

- [45] Johanna Wald, Helisa Dhamo, Nassir Navab, and Federico Tombari. Learning 3d semantic scene graphs from 3d indoor reconstructions. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 3961–3970, 2020. 

- [46] Abdelrhman Werby, Chenguang Huang, Martin B¨uchner, Abhinav Valada, and Wolfram Burgard. Hierarchical open-vocabulary 3d scene graphs for language-grounded 

   - robot navigation. In _Robotics: Science and Systems (RSS)_ , 2024. 

- [47] Joey Wilson, Ruihan Xu, Yile Sun, Parker Ewen, Minghan Zhu, Kira Barton, and Maani Ghaffari. Latentbki: Open-dictionary continuous mapping in visuallanguage latent spaces with quantifiable uncertainty. _IEEE Robotics and Automation Letters_ , 2025. 

- [48] Shun-Cheng Wu, Johanna Wald, Keisuke Tateno, Nassir Navab, and Federico Tombari. Scenegraphfusion: Incremental 3d scene graph prediction from rgb-d sequences. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 7515–7525, 2021. 

- [49] Mengya Xu, Yang Song, Yongbo Chen, Shoudong Huang, and Qi Hao. Invariant ekf based 2d active slam with exploration task. In _IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5350–5356, 2021. 

- [50] Chi Yan, Delin Qu, Dan Xu, Bin Zhao, Zhigang Wang, Dong Wang, and Xuelong Li. Gs-slam: Dense visual slam with 3d gaussian splatting. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 19595–19604, 2024. 

- [51] Mingqiao Ye, Martin Danelljan, Fisher Yu, and Lei Ke. Gaussian grouping: Segment and edit anything in 3d scenes. In _European conference on computer vision (ECCV)_ , pages 162–179. Springer, 2024. 

- [52] Hang Yin, Xiuwei Xu, Zhenyu Wu, Jie Zhou, and Jiwen Lu. Sg-nav: Online 3d scene graph prompting for llmbased zero-shot object navigation. _Advances in neural information processing systems (NeurIPS)_ , 37:5285–5307, 2024. 

- [53] Naoki Yokoyama, Sehoon Ha, Dhruv Batra, Jiuguang Wang, and Bernadette Bucher. Vlfm: Vision-language frontier maps for zero-shot semantic navigation. In _IEEE International Conference on Robotics and Automation (ICRA)_ , pages 42–48, 2024. 

- [54] Yao Zhao, Zhi Xiong, Shuailin Zhou, Jingqi Wang, Ling Zhang, and Pascual Campoy. Perception-aware planning for active slam in dynamic environments. _Remote Sensing_ , 14(11):2584, 2022. 

- [55] Ziyu Zhu, Xilin Wang, Yixuan Li, Zhuofan Zhang, Xiaojian Ma, Yixin Chen, Baoxiong Jia, Wei Liang, Qian Yu, Zhidong Deng, et al. Move to understand a 3d scene: Bridging visual grounding and exploration for efficient and versatile embodied navigation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 8120–8132, 2025. 

## **Learning to Evolve: Multi-modal Interactive Fields for Robust Humanoid Navigation in Dynamic Environments** 

### **- Supplementary Material -** 

_The supplementary material provides implementation details, algorithmic workflow, parameter settings, and additional visual evidence for the Multi-modal Interactive Field (MIF) system reported in the main paper. These details clarify how the appearance, spatial, geometry, navigation, and adaptation modules are integrated in the real humanoid deployment. We include the distributed system architecture, execution loop, selected hyperparameters, and navigation-control details. We also provide qualitative examples of locomotion-robust mapping, local memory updates, and IPS-based interaction checks._ 

#### **Outline of Supplementary Material** 

This document provides additional implementation details, extended analyses, and qualitative examples that complement the main manuscript. The content is organized as follows: 

- **Section S.1: System Implementation Details** 

   - **Hardware Architecture:** Specifications of the Unitree G1 humanoid platform, RealSense D435i sensor setup, and onboard/offboard computation split. 

   - **Software Stack:** Implementation details for the confidence-aware 3DGS backend, VLM-assisted scene-graph construction, and Flow Matching-based geometry service. 

   - **System Architecture:** A dataflow diagram showing asynchronous coordination among perception, spatial reasoning, geometry generation, and navigation. 

- **Section S.2: Algorithmic Workflow** 

   - **Algorithm 1 (MIF Execution Loop):** Pseudo-code describing the closed-loop interaction between semantic grounding, stability-aware navigation, and the Memory Evolution Loop. 

- **Section S.3: Hyperparameter Settings** 

   - **Confidence Gating Parameters:** Specific values for gradient penalty ( _β_ ) and opacity scaling ( _γ_ ) used to suppress locomotion-induced noise. 

   - **Interaction & Adaptation:** Weighting coefficients ( _wpos, wsem, wrel_ ) for the multi-modal discrepancy score _D_ and re-planning thresholds. 

   - **Safety Protocol:** Geometric margins ( _δsafe_ ) and support polygon definitions for the Interaction Pose Safety (IPS) check. 

- **Section S.4: Additional Quantitative Results** 

   - **Ablation Study (Confidence Gating):** Extended PSNR/SSIM and change-detection measurements illustrating the effect of confidence gating under walking-induced distortion. 

   - **Navigation Stability Analysis:** Measurements of torso oscillation and cross-track error under the stability-aware local planner. 

- **Section S.5: More Qualitative Visualizations** 

   - **Robustness of Appearance Field:** Visual examples comparing mapping with and without confidence gating, plus examples of local appearance updates after scene changes. 

   - **Geometric Safety Verification:** Comparison between sparse Gaussian centroids and generated meshes for IPS collision checking. 

   - **Dynamic Adaptation Sequence:** Chronological visualization of the Memory Evolution Loop in a “Sofa Relocation” (P2) scenario. 

   - **Real-World Deployment Showcase:** Examples of social navigation, narrow-passage traversal, dynamic adaptation, and mobile manipulation. 

##### S.1. SYSTEM IMPLEMENTATION DETAILS 

This section describes the hardware and software setup used in our real-world MIF experiments. 

**System Instruction:** You are a robot’s spatial reasoning engine. Analyze the provided image (synthesized from a stable view) and extract key objects. 

###### **Input:** 

##### _A. Hardware Architecture_ 

_1) Robot Platform and Sensors:_ We deploy our system on the Unitree G1 humanoid robot. The robot is equipped with a head-mounted Intel RealSense D435i RGB-D camera, configured to provide synchronized color and depth streams at a resolution of 640 _×_ 480 (30 Hz). Camera intrinsics are calibrated offline, and the camera-to-base transform is obtained from the calibrated mounting and robot kinematic chain. 

_2) Computation and Communication:_ We split computation between onboard control and offboard perception/reasoning: 

- Onboard Compute: The robot’s built-in NVIDIA Jetson Orin NX handles robot-provided low-level control interfaces, state feedback (IMU/Odometry), and hardware bridging. 

- Offboard Compute: The high-load MIF modules, including 3DGS mapping, VLM-assisted graph construction, and Flow Matching-based geometry generation, run on the workstation. 

- Communication Stack: We use ROS1 Noetic and compressed image transport for RGB-D streams. In our setup, this configuration provided approximately 25 Hz transmission with latency below 50 ms. 

_3) Server Specifications:_ The offboard workstation uses commercial desktop hardware. It is equipped with an Intel Core i9-13900K CPU, 64 GB DDR5 RAM, and an NVIDIA RTX 4090 GPU with 24 GB VRAM. This setup was sufficient for the reported 22 FPS Appearance Field updates and approximately 6.2 s Geometry Field generation latency in our experiments. 

##### _B. Software Stack_ 

_1) 3DGS Backend:_ The Appearance Field is implemented on an incremental Gaussian Splatting backend. We use differentiable Gaussian rasterization libraries and CUDA kernels for primitive updates and rendering. The SLAM frontend is implemented in Python/PyTorch, leveraging diff-gaussianrasterization-w-depth for differentiable rasterization with depth supervision. The confidence gate (Ω _i_ ) is implemented in PyTorch/CUDA and applied during rendering and pose optimization with low runtime overhead. 

_2) VLM & Prompt Engineering:_ For Spatial Field ( _Fspat_ ) construction, we use GPT-4o (OpenAI) to parse stabilized rendered views into structured scene-graph evidence. The parsed outputs are post-processed into scene graph nodes and relations. 

To encourage structured output for topological parsing, we use the JSON-style prompt template shown in Fig. S.1. This prompt requests object categories, 2D bounding box estimates, and spatial prepositions (e.g., “on”, “next to”) relative to known landmarks. 

An image of an office scene. 

###### **Output Constraint:** 

Return a JSON-style list. Each item should contain: 

- "object_id": unique integer 

- "category": specific object name (e.g., "monitor", not "electronics") 

- "relations": list of spatial relations to other objects (e.g., ["on", "desk_1"]) 

- "attributes": visual descriptors (e.g., "black", "off") 

- **User Query:** ”Identify all interactable objects in this view and their spatial relationships.” 

Fig. S.1: **Prompt template for scene graph construction.** The prompt requests structured JSON-style output that can be parsed into the topological graph _Mspat_ . 

_3) Flow Matching Model Architecture:_ The Geometry Field ( _Fgeom_ ) uses a pre-trained conditional Flow Matching model [10]. Using a pre-trained model avoids training a geometry prior from scratch and provides object-level mesh hypotheses for IPS verification. _•_ Backbone Architecture: We utilize a pre-trained FlowMatching Transformer backbone that processes latent shape tokens and produces object-level mesh hypotheses used by the IPS module. 

- Conditioning & Tokenization: The conditioning image is encoded with frozen visual features and projected into the model’s latent space, allowing the generation process to use both visual and geometric cues. 

- Inference Strategy: We use a distilled inference setting with _N_ = 25 function evaluation steps. In our setup, geometry generation takes about 6.2 s and is scheduled asynchronously during approach or verification. 

_4) System Architecture Implementation:_ Fig. S.2 summarizes the onboard/offboard dataflow used by MIF. The system comprises distinct computational modules distributed as follows: 

**Onboard Computation (Unitree G1 with Jetson Orin):** The onboard layer provides sensor streams, robot state feedback, and low-level command execution. 

- Sensors: Acquires raw data from the RGB-D Camera (D435i) and IMU/Kinematics. 

- Image Transport Bridge: Compresses high-bandwidth RGB-D streams to minimize latency before transmission to the offboard server. 

- Low-Level Interface: Executes admissible velocity and body commands through the robot control stack. 


Fig. S.2: **System architecture and dataflow.** The architecture is divided between the Onboard Robot for sensing and low-level control, and the Offboard Compute Server for high-load perception and reasoning. On the server, processing is structured into four main engines: Perception Engine (constructing _Fapp_ ), Spatial Reasoning Engine (constructing _Fspat_ ), Interaction & Planning Core, and the On-Demand Geometry Service (generating _Fgeom_ ). The Discrepancy Monitor connects online observations with local memory updates when map-reality mismatch is detected. 

**Offboard Compute Server:** Incoming compressed streams are first handled by the Data Decompression & Synchronization module before being dispatched to four primary engines: 

- Perception Engine (Appearance Field - _Fapp_ ): Maintains the confidence-aware Appearance Field using the 3DGS SLAM backend, reliability estimation, and CLIP/DINOv2 feature distillation. 

- Spatial Reasoning Engine (Spatial Field - _Fspat_ ): Processes stabilized rendered views with VLM-assisted parsing and scene graph construction to build local graph evidence and update the Spatial Field when triggered by the adaptation loop. 

- Interaction & Planning Core: Uses real-time observations for semantic grounding and target refinement, runs the global planner and stability-aware local planner, and sends control commands back to the onboard robot. 

- On-Demand Geometry Service (Geometry Field - _Fgeom_ ): Triggered when approaching an interaction target. It uses the task-local viewpoint score _Q_ ( _k_ ) to select conditioning views for Flow Matching-based mesh generation, which is then checked by IPS. 

The discrepancy monitor compares live local graph evidence with stored Spatial Field evidence. When _D > τ_ , it triggers local updates in the Appearance and Spatial Fields rather than global remapping. Algorithm 1 summarizes this logic. 

##### S.2. HYPERPARAMETER SETTINGS 

We list the fixed parameter values used in our experiments. Unless otherwise noted, these values were kept unchanged across real-world trials. 

##### _A. Confidence Gating Parameters_ 

In the Appearance Field ( _Fapp_ ), the confidence score _Ci_ (Eq. 1) uses the sharpness of the gradient penalty ( _β_ ) and the opacity scaling factor ( _γ_ ). The values used in our experiments, along with the confidence threshold, are listed in Table S.1. 

TABLE S.1: **Parameters for confidence-aware filtering.** 

|**Symbol**|**Value**|**Description**|
|---|---|---|
|_β_|5.0|Controls sensitivity to normalized optimization instability.|
|_γ_|2.0|Scaling factor for opacity-based reliability.|
|_τconf_|0.6|Minimum confidence threshold for VLM rendering.|


##### _B. Interaction & Adaptation Mechanism_ 

The discrepancy score _D_ (Eq. 4, 5) aggregates positional, semantic, and relational graph evidence to trigger local memory update and replanning. The weighting coefficients for these components and the triggering threshold are listed in Table S.2. 

TABLE S.2: **Parameters for discrepancy detection.** 

|**Symbol**|**Value**|**Description of Weight or Threshold**|
|---|---|---|
|_wpos_|1.0|Centroid Euclidean distance error (in meters).|
|_wsem_|0.5|CLIP/DINO semantic feature cosine distance.|
|_wrel_|0.8|Jaccard distance of graph edge sets.|
|_τ_|0.45|Threshold of _D_ for local memory update and replanning.|


##### _C. Interaction Pose Safety (IPS) Protocol_ 

The IPS check is used as a pre-interaction feasibility gate. 

- Geometric Safety Margin ( _δsafe_ ): We set _δsafe_ = 0 _._ 05 m. In our implementation, a pose is considered collision-free only if the minimum signed distance between the robot model and the generated mesh _Mgen_ is greater than 5 cm. 

- Support Polygon ( _Psup_ ): Defined as the convex hull of the robot’s feet contact area, with a safety shrinkage of 2 cm to account for control noise. 

##### S.3. ALGORITHMIC WORKFLOW 

Algorithm 1 summarizes the task execution loop, including semantic grounding, navigation monitoring, local memory update, and IPS verification. 

MIF is a system-level integration rather than a standalone 3DGS, scene-graph, or mesh-generation algorithm. The Appearance Field _Fapp_ stores confidence-gated semantic Gaussian primitives; the Spatial Field _Fspat_ stores a hierarchical scene graph whose nodes contain semantic labels, centroids, reliability, and room affiliation; and the Geometry Field _Fgeom_ is an on-demand object mesh used only for IPS verification. The gradient magnitude in _Fapp_ is not used as a generic 3DGS densification or pruning heuristic; here it is interpreted as a physical instability cue caused by humanoid gait and pose jitter. During adaptation, MIF only revises the graph nodes, edges, and Gaussian support inside the discrepancy-triggered local region, while unaffected memory remains unchanged. 

##### S.4. ADDITIONAL QUANTITATIVE RESULTS 

This section provides extended quantitative analyses that complement the task-level results in the main paper. We report an ablation of confidence gating under walking-induced distortion and a stability analysis of the local planner. 

##### _A. Ablation Study: Efficacy of Confidence Gating_ 

To isolate the effect of confidence gating (Ω _i_ ) defined in Eq. 1, we compare MIF with a variant without the gate (“w/o Gating”). 

Quantitative Analysis. We evaluate the rendered-view quality (PSNR and SSIM) under different robot walking speeds. As shown in Table S.3, the ungated variant degrades under fast walking (0 _._ 5 m/s), with PSNR dropping to 21.6 dB. MIF retains higher PSNR/SSIM under the same condition. The lower false-positive rate (FPR) further suggests that stable appearance evidence helps reduce false updates in the adaptation loop. 

TABLE S.3: **Extended ablation of confidence gating under walking motion.** 

|**Method**|**Slow Walk **<br>PSNR _↑_|**(**0_._2**m/s)**<br>SSIM _↑_|**Fast Walk **<br>PSNR _↑_|**(**0_._5**m/s)**<br>SSIM _↑_|**Change Det.**<br>FPR _↓_|
|---|---|---|---|---|---|
|w/o Gating|28.4|0.88|21.6|0.72|46.5%|
|**MIF (Ours)**|**31.2**|**0.93**|**29.8**|**0.89**|**4.2%**|


##### _B. Navigation Stability Analysis_ 

We also report torso oscillation and cross-track error for the stability-aware local planner. We define _Torso Oscillation_ as the standard deviation of the camera’s roll/pitch angles during traversal. Compared to a standard Pure Pursuit controller, adaptive velocity scaling reduces torso oscillation by 45% (from 5 _._ 2<sup>_◦_</sup> to 2 _._ 8<sup>_◦_</sup> ) while maintaining a low cross-track error ( _<_ 0 _._ 15 m). This reduction in oscillation is consistent with the improved perceptual quality reported in Table S.3. 

##### S.5. QUALITATIVE VISUALIZATIONS 

This section provides qualitative examples illustrating the system’s behavior under humanoid locomotion noise (P1) and dynamic scene changes (P2). 

##### _A. Robust Mapping under Locomotion (P1)_ 

_1) Robustness of Appearance Field: Jitter Suppression & Dynamic Adaptation:_ We visualize rendered RGB/depth quality from the Appearance Field _Fapp_ under humanoid walking. Rows 1-3 of Fig. S.3 illustrate the effect of confidence gating during high-speed walking (0 _._ 5 m/s). The ungated variant shows ghosting artifacts in RGB and noisier depth estimates (e.g., Depth L1 error increases to 0 _._ 07 cm). In contrast, confidence gating prioritizes higher-reliability observations, maintaining high PSNR ( _>_ 30 dB) and piecewise-smooth geometry in this example. 

Furthermore, Row 4 shows an example in which local field updates reflect object removal or placement without visibly accumulating motion artifacts. 

_2) Generated Geometry for IPS Checking:_ To illustrate why sparse point clouds are insufficient for IPS collision checking, we present a comparative analysis in Fig. S.4. The raw 3D Gaussian point cloud (Left panels), while useful for visual navigation, remains sparse and lacks surface connectivity. Gaps between centroids may make collision checks overly optimistic. 

The Flow Matching module synthesizes a dense mesh (Right panels) for the target object. The generated mesh provides a continuous proxy for signed-distance checks in IPS. Fig. S.5 further shows examples across several object categories used in our experiments. 

##### _B. Dynamic Adaptation Sequence (P2)_ 

Fig. S.6 presents a step-by-step breakdown of the Interaction Adaptation Mechanism in a real-world ”Sofa Relocation” scenario. 

|**Alg**|**orithm 1** Multi-modal Interactive Field (MIF) execution loop|
|---|---|
|**Req**<br>|**uire:** User Instruction _I_, Initial Memory _M_=_{Fapp, Fspat}_<br>|
|1:|**Phase 1: Semantic Grounding (Sec. 3.4)**|
|2: <br>|_⟨_Region_,_Target_⟩←_VLM<br>Parse(_I_)<br>|
|3: <br>4: <br>|**v**_target ←_QueryGraph(_Fspat,_Target) _{_Retrieve target node_}_<br> **c**_goal ←_RefineCentroid(**v**_target, Fapp_) _{_Eq. 3: Confidence-weighted position_}_<br>|
|5: <br>|_Pglobal ←_PlanPath(**c**_goal_)<br>|
|6:|**Phase 2: Navigation & Monitoring (Sec. 3.2)**|
|7:|**while** distance(**p**_robot,_**c**_goal_) _> δarrival_ **do**|
|8:|_Oloc ←_GetObservation()|
|9:|_Mloc ←_BuildLocalGraph(_Oloc_) _{_Live nodes, edges, and centroids_}_|
|10:|_D ←_CalcDiscrepancy(_Mloc, Fspat_) _{_Eq. 5: Monitor P2 Mismatch_}_|
|11:|**if** _D > τ_ **then**|
|12:|**Trigger Memory Evolution Loop:**|
|13:|Pause navigation.|
|14:|_Oscan ←_ActiveScan(Region) _{_Gather multi-view evidence_}_|
|15:|_Rbad ←_AffectedRegion(_Mloc, Mspat_) _{_Nodes/edges with high discrepancy_}_<br>|
|16:|_Fapp_[_Rbad_]_←_FuseHighConf(_Oscan_) _{_Local Gaussian support only_}_|
|17:|_M_<sup>_new_</sup><br>_loc _<sup>_←_BuildLocalGraph(</sup><sup>_Fapp_[</sup><sup>_Rbad_])</sup>|
|18:|_Fspat ←_PatchGraph(_Fspat, M_<sup>_new_</sup><br>_loc_ <sup>)</sup> <sup>_{_Replace/insert affected nodes and edges</sup><sup>_}_</sup><br>|
|19:|**c**_goal ←_ReQuery(_Fspat_) _{_Refresh target estimate_}_<br>|
|20:|_Pglobal ←_PlanPath(**c**_goal_) _{_Re-plan on updated map_}_<br>|
|21:|**else**|
|22:|_v, ω ←_StabilityAwareControl(_Pglobal_) _{_Sec. S.1.3_}_<br>|
|23:|Execute(_v, ω_)|
|24:|**end if**|
|25:|**end while**|
|26:|**Phase 3: Interaction Verification (Sec. 3.3)**|
|27:|**while** _SIP S_ ==False and retry budget remains **do**|
|28:|_k_<sup>_∗_</sup>_←_SelectViewpoint(_Q_(_k_)) _{_Eq. 6: Active Gaze_}_|
|29:|MoveTo(_k_<sup>_∗_</sup>)|
|30:|_Ibest ←_CaptureImage()|
|31:|_Mgen ←_FlowMatching(_Ibest,_cond=**v**_target._sem) _{_Eq. 7_}_|
|32:|_SIP S ←_CheckIPS(_Mgen_) _{_Eq. 9: Safety Check_}_|
|33:|**if** _SIP S_ ==False **then**|
|34:|MicroAdjustStance(_Mgen_) _{_Adjust stance or select another viewpoint_}_|
|35:|**end if**|
|36:|**end while**|
|37:|**return** Task status|


Fig. S.6: **Memory Evolution Loop under sofa relocation. (a)** The discrepancy score _D_ rises when the sofa is missing. **(b)** The robot actively scans the area. **(c)** The local graph is updated with the observed sofa location. **(d)** The planner reroutes to the updated goal. 

##### _C. Real-World Deployment Showcase_ 

We provide additional deployment examples on the Unitree G1 humanoid. As shown in Fig. S.7, these examples cover social navigation, narrow-passage traversal, dynamic adaptation, and a mobile-manipulation task. 

**Social Navigation (Row 1).** The robot patrols a corridor, detects a human, stops at a socially compliant distance (1 _._ 5 m), and executes a greeting gesture before resuming navigation. **Cluttered Navigation (Row 2).** The robot traverses a narrow office passage toward the target area, illustrating the navigation stack operating with the maintained Appearance Field _Fapp_ . **Dynamic Adaptation (Rows 3-5).** In the ”Sofa Relocation” scenario (P2), the baseline (HOV-SG, Row 5) follows stale scene-graph memory toward the obsolete sofa location, while 


Fig. S.3: **Qualitative Evaluation of Appearance Field Robustness. (Rows 1-3) Ablation of Confidence Gating:** We compare rendered RGB and depth maps between our method (Left) and the baseline without gating (Right) under locomotion noise. **Without gating** , the map shows motion blur (ghosting) and depth discontinuities. **With confidence gating** , the system reduces visible jitter artifacts, yielding higher PSNR and lower Depth L1 errors. **(Row 4) Dynamic Adaptation:** The bottom row visualizes an Appearance Field update after environmental changes (e.g., object relocation on the table/shelf) while maintaining visual consistency in the rendered views. 

MIF (Row 4) detects a discrepancy, updates local memory, and replans toward the observed layout. **Mobile Manipulation (Row 6).** Finally, we show a service task in an elderly care setting. The robot navigates to a fridge, retrieves a drink, and hands it to a user. This example illustrates how the generated Geometry Field _Fgeom_ can support IPSbased interaction checks before manipulation. 


Fig. S.4: **From sparse perception to interaction checking.** Comparison between the raw environmental point cloud and the generated Geometry Field. **(Left)** The sparse 3D Gaussian centroids capture the scene context but contain noise and gaps (visualized with bounding boxes), making them insufficient for fine-grained collision checks. **(Right)** The corresponding meshes generated by _Fgeom_ provide a denser geometric proxy for collision and reachability checks. 


Fig. S.5: **Gallery of generated interactive geometries.** Examples of meshes generated by the Flow Matching model during real-world experiments, covering rigid appliances (e.g., washing machines, routers), furniture (e.g., chairs, tables), and semirigid objects (e.g., pillows). These assets are used as geometric proxies for the Interaction Pose Safety (IPS) check. 


Fig. S.7: **Real-world deployment examples.** We show: **Row 1:** Social patrol with compliant human interaction (waving at 1 _._ 5 m). **Row 2:** Narrow-passage traversal through an office passageway. **Rows 3-5:** Dynamic adaptation to layout changes (“ _Bypass the sofa_ ”). The baseline follows stale memory (Row 5), while MIF updates local memory and replans (Row 4). **Row 6:** Mobile-manipulation example for fetching a drink. 

