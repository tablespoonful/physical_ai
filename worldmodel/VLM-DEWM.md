---
title: "VLM-DEWM: Dynamic External World Model for Verifiable and Resilient Vision-Language Planning in Manufacturing"
date: "2026-02-17"
authors: "Guoqin Tang; Qingxuan Jia; Gang Chen; Tong Li; Zeyuan Huang; Zihang Lv"
url: https://arxiv.org/abs/2602.15549
pdf: https://arxiv.org/pdf/2602.15549
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.15549)** / [論文ページ](https://arxiv.org/abs/2602.15549)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

VLM-DEWM: Dynamic External World Model for Verifiable and Resilient Vision-Language Planning in Manufacturing 

Guoqin Tang<sup>a</sup> , Qingxuan Jia<sup>a</sup> , Gang Chen<sup>a,</sup><sup>_∗_</sup> , Tong Li<sup>a</sup> , Zeyuan Huang<sup>a</sup> , Ning Ji<sup>a</sup> , Zihang Lv<sup>a</sup> _aSchool of Intelligent Engineering and Automation, Beijing University of Posts and Telecommunications, Beijing, 100876, China_ 

# **Abstract** 

Vision-language model (VLM) shows promise for high-level planning in smart manufacturing, yet their deployment in dynamic workcells faces two critical challenges: (1) stateless operation—they cannot persistently track out-of-view states, causing world-state drift; and (2) opaque reasoning—failures are difficult to diagnose, leading to costly blind retries. This paper presents VLMDEWM, a cognitive architecture that decouples VLM reasoning from world-state management through a persistent, queryable Dynamic External World Model (DEWM). Each VLM decision is structured into an Externalizable Reasoning Trace (ERT)—comprising action proposal, world belief, and causal assumption—which is validated against DEWM before execution. When failures occur, discrepancy analysis between predicted and observed states enables targeted recovery instead of global replanning. We evaluate VLM-DEWM on multi-station assembly, largescale facility exploration, and real-robot recovery under induced failures. Compared to baseline memory-augmented VLM systems, VLM-DEWM improves state-tracking accuracy from 56% to 93%, increases recovery success rate from below 5% to 95%, and significantly reduces computational overhead through structured memory. These results establish VLM-DEWM as a verifiable and resilient solution for long-horizon robotic operations in dynamic manufacturing environments. _Keywords:_ Vision-language model, Long-horizon planning, State tracking, Failure diagnosis, Smart manufacturing 

# **1. Introduction** 

Flexible manufacturing systems increasingly rely on autonomous robots to execute long-horizon tasks such as multi-station assembly, inter-station material handling, and inventory management [1]. Unlike single-station operations, these tasks span multiple work areas where the workspace changes dynamically due to inventory replenishment, human intervention, occlusions, and execution disturbances. Reliable operation therefore requires long-horizon planning across stations, persistent tracking of out-of-view states, and fast failure diagnosis and recovery to minimize downtime. 

Pre-trained vision–language models (VLMs) offer strong semantic understanding and task decomposition capabilities, making them attractive for high-level robotic planning. However, VLMbased planners face a fundamental responsibility mismatch in dynamic manufacturing workcells: they are required to both reason semantically _and_ maintain long-horizon world states within a 

> _∗_ Corresponding author 

> _Email address:_ `buptcg@163.com` (Gang Chen) 

_Preprint submitted to Robotics and Computer-Integrated Manufacturing_ 

_February 18, 2026_ 

transient context window. This coupling is inherently fragile—cross-station consistency degrades under occlusion and inventory changes, leading to world-state drift over time [2, 3]. Moreover, when execution fails due to stale beliefs, the system lacks interpretable root-cause explanations [4], and recovery degenerates into blind retries or expensive global replanning, increasing cycle time and downtime. 

Consider a representative multi-station task: a mobile manipulator retrieves a Type-1 part from Station A, transports it to Station C, and completes assembly. The robot’s memory indicates one Type-1 part at Station A, but upon arrival perception detects two identical parts due to replenishment. Without resolving this memory–observation conflict, the robot may pick the wrong part or fail to terminate. If the part is later dropped at an unobserved location, recovery further requires diagnosing both the failure cause (e.g., grasp loss, collision, or actuator fault) and the updated part location; otherwise the system again resorts to blind retries or global replanning. 

In isolation, each of these issues—memory staleness, observation conflict, undiagnosed failure—might be recoverable through local corrections. However, long-horizon tasks amplify their impact in ways that single-station operations do not. First, errors accumulate: a single unresolved memory–observation conflict propagates incorrect beliefs to all downstream decisions, causing cascading failures that compound across subsequent stations. Second, retry costs escalate non-linearly: each blind retry consumes cycle time without addressing the root cause, and over a 50-step task, even a 5% per-step failure rate yields near-zero end-to-end success (0 _._ 95<sup>50</sup> _≈_ 8%). Third, diagnosis grows intractable: as the action history lengthens, identifying which step introduced the error becomes increasingly difficult without structured state tracking. These compounding effects point to three requirements for reliable long-horizon VLM planning: state persistence across stations and occlusions, decision verifiability to arrest error propagation, and failure diagnosability to enable efficient recovery. 

Rather than relying on larger context windows, we address this mismatch through architectural separation: persistent state maintenance is delegated to an external, queryable world model, while the VLM focuses solely on semantic reasoning over structured state representations.This separation yields two design principles. First, decouple state from reasoning: maintain an explicit, queryable world state that is continuously synchronized with perception and remains accessible across station transitions, instead of implicitly encoding state in the context window. Second, make decisions verifiable and diagnosable: externalize VLM outputs into auditable artifacts, validate them against physical consistency before execution, and compare them with post-execution outcomes to enable informed recovery. 

Based on these principles, we propose VLM-DEWM (VLM with Dynamic External World Model), a cognitive architecture operating on a “Database–Transaction–Verification” paradigm. DEWM maintains a persistent, queryable database of semantic relations, 3D geometry, and execution history.<sup>1</sup> On top of DEWM, an “Externalizable Reasoning Trace (ERT)” structures each VLM decision into an action proposal, a world belief, and a causal assumption, all of which are validated against physical consistency before execution. A closed-loop cognitive pipeline synthesizes task-specific queries from DEWM, audits VLM outputs through multi-layer checks, and performs targeted failure diagnosis when discrepancies arise. 

> 1Our “world model” refers to a persistent state database for maintaining the current world state, distinct from learned dynamics models in model-based RL that predict _P_ ( _s_<sup>_′_</sup> _|s, a_ ), or manually engineered PDDL domains that encode symbolic preconditions. DEWM does not model dynamics; it maintains a synchronized snapshot that supports structured, verifiable zero-shot task decomposition. 

2 

We evaluate VLM-DEWM in simulation and real-robot experiments across three manufacturingrelevant scenarios: multi-station assembly under occlusions, large-scale facility exploration with spatial queries, and dynamic recovery under induced execution failures. Compared to state-of-theart memory-augmented VLM systems, VLM-DEWM improves state-tracking accuracy from 56% to 93% in exploration tasks, achieves 95% recovery success rate in settings where the baselines rarely succeed, and reduces VLM inference overhead by over 70%. These results demonstrate that architectural separation of state maintenance from semantic reasoning substantially improves robustness for long-horizon robotic operations in dynamic manufacturing environments. The main contributions are: 

1. **Dynamic External World Model (DEWM):** Resolves world-state drift by decoupling state maintenance from reasoning, ensuring persistent cross-station memory despite occlusions and transient context limitations. 

2. **Externalizable Reasoning Trace (ERT):** Mitigates opaque reasoning by structuring VLM decisions into verifiable artifacts, enabling pre-execution physical checks to arrest error propagation. 

3. **Discrepancy-Driven Diagnosis:** Eliminates costly blind retries via _CS_ -anchored discrepancy analysis, which leverages prediction-observation mismatches to enable precise, targeted recovery. 

# **2. Related Work** 

As established in Section 1, long-horizon robotic manipulation poses three core challenges: **state persistence** across occlusions and station transitions, **decision verifiability** for auditable execution, and **failure diagnosability** for efficient recovery. We review related work through these three lenses, examining how existing approaches in VLM-driven planning (Section 2.1), memory-augmented agents (Section 2.2), and scene representations (Section 2.3) address—or fail to address—each challenge. 

# _2.1. VLM-Driven Robot Planning: From Generalization to Auditable Execution_ 

Research in VLM-driven planning generally falls into two paradigms: joint training (e.g., PaLME [5], PaLi-X [6]) and frozen deployment (e.g., RT-2 [7], OpenVLA [8]). The latter has recently expanded to scalable transformers such as _π_ 0 [9] and RDT-1B [10], enabling end-to-end visuomotor policies that operate closer to the control interface. 

While these methods demonstrate impressive generalization, they face a critical bottleneck in manufacturing: state accountability. In production environments, execution must be auditable: when an assembly task fails (e.g., insertion jamming), operators need to trace whether the error arose from perceptual occlusion, geometric drift, or an invalid logical precondition. However, endto-end models encode state implicitly in transient contexts, making root-cause attribution ill-posed without explicit state variables. Strategies like Inner Monologue [11] or ProgPrompt [12] attempt to externalize reasoning via textual logs, yet free-form language does not guarantee the metric determinism required for digital twins or MES integration. Consequently, purely VLM-based planners remain “open-loop” with respect to state auditability. 

# _2.2. Memory-Augmented VLMs: Semantic Persistence without Metric Verification_ 

The implicit state encoding discussed above manifests as _state forgetting_ —the inability to persistently track object states across occlusions and station transitions. To address this, recent 

3 

works couple VLMs with external knowledge bases, exemplified by SAGE [13] and GEAR [14], which employ Retrieval-Augmented Generation (RAG) to fetch context from semantic maps or vector databases. 

While RAG improves persistence [15], it introduces a dual mismatch in geometric grounding and update latency. First, a fundamental geometric gap exists: RAG relies on vector-space similarity (e.g., cosine distance), which cannot verify metric spatial relations required for physical manipulation. Retrieving a statement like “Part A is aligned” is insufficient to certify feasibility without explicit pose verification [16]. Even graph-based variants [17] abstract away metric details (e.g., object poses, spatial offsets) essential for collision-free planning. Second, a dynamic mismatch persists: the standard “update–index–retrieve” loop often lags behind fast-changing workcell states, causing retrieved context to reflect outdated information and leading to execution failures [18]. 

Agentic frameworks with self-correction (e.g., Corrective RAG [19], Agent-G [20]) partially address staleness but still lack geometry-grounded verification, limiting their applicability to longhorizon manipulation where persistent state tracking and metric validation are essential. 

# _2.3. Scene Representations: Bridging Geometry and Assembly-Process-State_ 

Scene representations in robotics must balance geometric fidelity with semantic reasoning. Current approaches struggle to satisfy both demands simultaneously. 

On the geometric end, representations have evolved from discrete grids (OctoMap [21]) to continuous neural fields (CATNIPS [22], BundleSDF [23]) and Gaussian splatting (GraspSplats [24]). While achieving high visual fidelity, these methods typically treat assembly constraints as opaque optimization costs and lack explicit encoding of interaction phases—such as the transition from free-space motion to constrained insertion—creating barriers for failure-mode identification. 

On the semantic end, 3D scene graphs (e.g., DovSG [25], RoboEXP [26]) encode logical relations and action affordances, while methods like RP-SG [27] infer spatial relations under occlusion via graph networks. However, these approaches often discard metric details (e.g., precise 6-DoF poses) essential for physical feasibility verification and failure diagnosis. 

Existing frameworks rarely capture the complete picture: they either track geometry without process-aware semantics, or encode task logic without reliable metric grounding. VLM-DEWM addresses this gap through a hybrid _S_ - _G_ architecture that couples high-fidelity geometric tracking with diagnosable, process-aware state abstraction—providing both the metric substrate for physical verification and the semantic interface for VLM reasoning. 

# **3. Methodology** 

As argued in Section 1, reliable VLM-based planning requires separating persistent state maintenance from semantic reasoning. We instantiate this principle through VLM-DEWM, a framework operating on a “Database–Transaction–Verification paradigm”: the DEWM serves as a persistent database maintaining world state, the VLM outputs an Externalizable Reasoning Trace (ERT) as a verifiable transaction, and a Verification Engine audits the ERT against DEWM before execution. Formally, the DEWM state at time _t_ is defined as: 


where Ω _t_ = _⟨S, G, L⟩_ is the environment memory core (spatial network, semantic graph, and shape prior library), _Mt_ is the task memory tracking execution progress, and _CSt_ is the constraint state anchoring the robot’s interaction phase for failure diagnosis. 

4 


Figure 1: **Architectural Overview of the VLM-DEWM Framework.** Operating on a Database-Transaction paradigm, the system is orchestrated through three tightly coupled modules. The perception module first projects raw multimodal sensory streams into a structured instantaneous snapshot ( _Envt_ ) via geometric projection and filtration. This snapshot drives the thinking module, where the VLM serves as the reasoning core to simultaneously update the external world model (DEWM)—the central knowledge hub comprising environmental (Ω) and internal ( _M, CS_ ) memory—and synthesize a structured _External Reasoning Trace (ERT)_ . Crucially, the validation module treats the persistent memory in the DEWM as ground-truth evidence to rigorously verify the ERT’s logical and physical consistency before dispatching the final action sequence to the Robot Skill Library _A_ for execution. 

As illustrated in Fig. 1, this formalism is instantiated as a closed-loop system with four modules: _Perception_ , _DEWM State Management_ , _VLM-based Reasoning_ , and _Validation_ . At each step, the system first perceives raw observations _Ot_ and updates the world state Ω together with an interaction-stage state _CS_ . It then queries Ω to construct task-relevant context for the VLM, which generates an ERT hypothesis for the next subtask. Before dispatching actions to the primitive skill library _A_ , the validation module checks the ERT against Ω and blocks geometrically infeasible plans; after execution, the system compares the observed outcome with the ERT’s causal assumption to trigger diagnosis and informed replanning when discrepancies occur. 

_3.1. The Environment Memory Core (_ Ω _): A Hybrid Semantic-Geometric Representation_ 

The Dynamic External World Model (DEWM) serves as the system’s knowledge foundation. Its primary component, the Environment Memory Core Ω, is designed based on the philosophy of _structural decoupling_ : separating high-level semantic logic from low-level geometric precision. Formally, we define Ω as a tripartite tuple: 


where _S_ represents the physical state, _G_ encapsulates logical relations, and _L_ provides shape priors (see Fig. 2). 

5 


Figure 2: **Structural Composition of the Environment Memory Core (** Ω **).** The Spatial Network ( _S_ ) maintains geometric state (left), while the Hierarchical Semantic Graph ( _G_ ) encodes logical relations (right). The Grounding Link (Φ _ground_ , red) anchors every semantic node to its physical instantiation. 

In this architecture, _G_ provides a queryable interface for VLM reasoning, _S_ serves as the metric substrate for feasibility checking and motion planning, and _L_ supplies on-demand high-fidelity geometry for robust 6-DoF registration and occlusion-robust shape inference. All downstream modules interact with Ω via a _semantic-to-metric grounding path_ : semantic queries on _G_ are resolved to geometric entities in _S_ via explicit links, enabling verification against metric constraints. 

# _3.1.1. The Geometric Layer: Spatial Network (S)_ 

The Spatial Network _S_ maintains the probabilistic state estimate of the physical state of the environment. To balance global planning efficiency with local manipulation precision, we adopt a dual-representation strategy: _S_ = _⟨Sbg, Sobj⟩_ . 

This design emulates human spatial memory— _“focus on foreground, blur the background”_ —where task-relevant objects receive high-fidelity tracking while static structures are compressed into occupancy grids. Specifically, entities segmented with task-relevant labels (Section 3.2.2) are registered in _Sobj_ , while unassociated geometric primitives are fused into _Sbg_ . 

1. Global Background Map ( _Sbg_ ): We utilize a coarse-grained, semantically labeled probabilistic voxel grid to represent static structures (e.g., walls, workbenches). This provides the freespace information necessary for global collision avoidance and coarse motion planning. 

2. Dynamic Object Map ( _Sobj_ ): This is an instance-indexed registry tracking all interactive entities. For each tracked object _i_ , its geometric state _s_<sup>_i_</sup> _obj_<sup>isdefinedas:</sup> 


Here, id _i_ is a pointer to the Shape Library _L_ ; **T** _i ∈ SE_ (3) denotes the precise 6-DoF pose updated via multi-frame tracking; and _Ei_ ( **_µ_** _i,_ **Σ** _i_ ) represents a Gaussian Envelope. 

_Remark:_ The Gaussian envelope _Ei_ acts as a _probabilistic spatial index_ for rapid VLM queries (e.g., “near X”) and candidate pruning, rather than for fine-grained contact modeling. When highprecision pose estimation is required (e.g., for grasping or insertion), precise geometry is retrieved on-demand from _L_ via the shape prior link. 

6 

# _3.1.2. The Semantic Layer: Hierarchical Semantic Graph (G)_ 

The semantic layer _G_ serves as the interface for VLM reasoning. We construct a Hierarchical Semantic Graph (HSG) to support multi-resolution planning: _G_ = _⟨Gzone, Gobj⟩_ . 

- Zone Graph ( _Gzone_ ): Acts as the spatial root, where nodes represent topological regions (e.g., `Workbench_A` ) and edges denote reachability, allowing the planner to efficiently prune the search space. 

- Object Graph ( _Gobj_ ): Modeled as a graph _Gobj_ = ( _V, E_ ), where each vertex _vi ∈V_ represents an object instance: 

_vi_ = _⟨_ uid _i,_ label _i,_ state _i,_ Attr _i,_ Φ _ground⟩_ (4) 

Here, Attr _i_ stores feature attributes extracted from VLM perception (e.g., “fragile”, “stack_on _X”). The function Φ _ground_ : _V →Sobj_ explicitly links the semantic node to its geometric counterpart in _S_ , ensuring that every abstract concept is physically grounded. Edges _eij ∈E_ encode spatial relations (e.g., `On` ) or affordances, derived from VLM inference. Note that these relations are stored as soft hypotheses and can be revised by the verification engine if inconsistent with geometric observations. 

# _3.1.3. The Shape Prior Library (L): Digital-Twin-Aligned Priors_ 

The library _L_ stores high-fidelity geometric priors derived from CAD models, providing digitaltwin-aligned references for robust pose estimation and shape completion. In manufacturing settings, we pre-process CAD meshes into canonical point clouds associated with functional frames. These priors support robust 6-DoF registration under sparse visual features and occlusion-robust shape inference when objects are partially covered by the gripper. Detailed registration algorithms and occlusion handling strategies are provided in Appendix B.1. 

# _3.1.4. Dynamic Maintenance_ 

The mechanisms for updating Ω from perception—including data association, state fusion, and lifecycle management—are detailed in Section 3.2. 

# _3.1.5. Formal State Transition Semantics_ 

To ensure the deterministic maintenance of the world model, we define the DEWM update as a state transition function _δ_ : (Ω _t, CSt_ ) _× πact →_ (Ω _t_ +1 _, CSt_ +1). This transition is designed to approximate database-style atomicity: if the rollback trigger is activated, the state reverts to (Ω _t, CSt_ ). Specifically, for a primitive action _πact_ , the update is an atomic transaction defined in Table 1. 

# _3.2. Perception and Memory Dynamics: Maintaining Model Veracity_ 

While Section 3.1 defined the static structure of the DEWM, this section details the dynamic processes that synchronize the internal model Ω with the evolving physical world. We employ a closed-loop pipeline “ _Perceive → Associate → Fuse → Verify_ ” to transform raw sensory streams into structured, physically grounded beliefs(see Fig. 3). 

7 

Table 1: Atomic State Transition Rules for Primitive Skills 

|**Action** _π_|**Pre-Condition** (_G_)|**Atomic Effects** (Ω_t_+1_, CSt_+1)|**Rollback Trigger**|
|---|---|---|---|
|`Pick(obj)`|_∃_`Clear(obj)`|1. _Sobj_: Detach _PCobj_<br>2. _G_: Del `On(obj, *)`<br>3. _CS_: Set `Holding(obj)`|Gripper width _>_ limit<br>(Slip)|
|`Place(loc)`|_CS_ =`Holding(obj)`|1. _Sobj_: Anchor at _loc_<br>2. _G_: Add `On(obj, loc)`<br>3. _CS_: Set `Idle`|Force feedback _>_ limit<br>(Collision)|
|`Insert(A, B)`|_∃_`Aligned(A, B)`|1. _G_: Add `Inserted(A, B)`<br>2. _CS_: Set `Idle`|Torque _>_ limit / Stall|


_Note:_ If the Rollback Trigger is activated via low-level controller feedback (see Appendix B.7 for the specific force-torque thresholds and event mapping logic), the state reverts to (Ω _t, CSt_ ). This table presents representative primitives. The full skill library _A_ includes additional primitives such as `Move(loc)` , `Rotate(obj, angle)` , and `Open/Close_Gripper` , each with corresponding transition rules. 

# _3.2.1. Task-Focused Perception Interface_ 

Unlike passive perception, our system employs a VLM-driven attention mechanism. Given a task instruction, the VLM generates a set of _Target Entities_ and _Regions of Interest_ . Raw RGB-D streams _Ot_ are processed to extract geometric primitives only for these relevant targets, lifting 2D masks into 3D space. Formally, this produces an instantaneous snapshot _Envt_ = _{ok}_<sup>_K_</sup> _k_ =1<sup>,where</sup> each observation _ok_ contains a semantic label, a confidence score, and a distance-adaptive geometric abstraction—dense point clouds for near-field manipulation, voxels for mid-range collision checking, or billboard textures for far-field situational awareness (detailed in Appendix A). 

# _3.2.2. VLM-Driven Data Association_ 

Integrating new observations requires robust data association. Purely geometric matching fails in cluttered scenes, while purely semantic matching is computationally prohibitive. We therefore adopt a “Filter-then-Adjudicate” protocol that combines geometric pre-screening with VLMassisted global assignment. 

_a. Geometric Gating (Filter):_ 

We prune infeasible pairs by computing the Mahalanobis distance _dM_ between the observation’s Gaussian envelope ( **_µ_** _obs,_ **Σ** _obs_ ) and the memory entry’s envelope _Ei_ = ( **_µ_** _i,_ **Σ** _i_ ) defined in Section 3.1 


Pairs with _dM ≥ τgeo_ are rejected, avoiding physically impossible matches before semantic evaluation. 

_b. Semantic–Geometric Adjudication (Judge)_ 

On the remaining feasible pairs, we solve a global one-to-one assignment via the Hungarian algorithm using a hybrid cost: 


We implement geometric gating by masking infeasible edges, i.e., setting _Cki_ = + _∞_ for pairs failing _dM < τgeo_ . Here, IoU is computed over 3D oriented bounding volumes (with a 2D fallback when 

8 


Figure 3: **The Perception-to-Memory Synchronization Pipeline.** Raw observations ( _Ot_ ) are transformed into persistent belief updates via three stages: (1) task-focused perception producing _Envt_ , (2) geometric-semantic data association, and (3) dual-layer updates (continuous S-Update and discrete G-Update with geometric verification). 

depth is unreliable), and sim( _·_ ) denotes VLM-based semantic similarity. Matches must pass a final quality gate _Cki ≤ τmatch_ . Unmatched observations enter a short confirmation window before being promoted to active entries, suppressing one-off false detections and preventing ghost artifacts. 

All prompts, parsing rules, and association hyperparameters are provided in Appendix B.1. 

# _3.2.3. VLM-Modulated Gaussian Envelope Fusion_ 

(S-Update) Once associated, the state update is modulated by VLM reasoning. Standard filters degrade when semantic context affects reliability (e.g., transparent objects or gripper-induced occlusion). We therefore perform a semantically-adaptive Gaussian fusion. 

For matched pairs, we maintain a Gaussian belief ( **_µ_** _t,_ **Σ** _t_ ) representing the object’s spatial envelope. Given a new observation with parameters ( **_µ_** _obs,_ **Σ** _obs_ ), we perform a weighted fusion in the information filter form: 


where _αt ∈{_ High, Medium, Low, Bad _}_ is a discrete reliability judgment produced by the VLM from scene context (e.g., occlusion, lighting, and sensor quality), and _γ_ ( _αt_ ) maps this judgment to a continuous weight factor that modulates the contribution of the new observation. 

This formulation treats the VLM as a meta-cognitive controller: when the VLM judges the observation as “High” reliability, _γ_ is large, allowing the new measurement to strongly influence the belief; when judged as “Bad” (e.g., due to heavy occlusion), _γ_ approaches zero, effectively 

9 

“freezing” the belief at its prior value. This enables context-aware state estimation that traditional adaptive filters cannot achieve—for instance, adopting a conservative update strategy for fragile objects even when observation quality appears high. 

The noise models, prompt templates, decoding/parsing rules, and the full mapping table used in all experiments are provided in Appendix B.2. 

# _3.2.4. Geometric Refinement and Background Maintenance_ 

For key objects requiring high-precision assembly, we perform a scale-aware robust ICP registration to align the current observation with the canonical Shape Prior _L_ , refining the pose estimate **T** _i ∈ SE_ (3) (details in Appendix B.3). Simultaneously, unassociated points are fused into the global background map _Sbg_ using probabilistic occupancy updates, and open boundaries are handled via view-dependent billboard textures to provide visual context for navigation (details in Appendix B.4). 

# _3.2.5. Hypothesis-Verification Loop (G-Update)_ 

To maintain semantic consistency, relations proposed by the VLM (e.g., _On_ ( _A, B_ )) are treated as hypotheses and verified against _S_ at _action boundaries_ . For proximity-type relations (e.g., `Contact(` _A, B_ `)` ), we validate consistency via a Chi-square test on Gaussian position estimates: 


For support-type relations (e.g., `On(` _A, B_ `)` ), we additionally apply conservative bounding-volume support checks with tolerance _δsupp_ as a proxy for physical support. The statistical basis, threshold selection, and verification criteria (including _δsupp_ ) for common relations are provided in Appendix B.5. This verification acts as a geometry-grounded firewall, preventing hallucinated relations from propagating into the planner’s worldview. 

# _3.2.6. Long-Term Memory Curation_ 

To prevent memory saturation in long-horizon tasks, we implement region-based confidence decay and lifecycle management. When the robot scans a zone _Zk_ and fails to re-observe an expected entity _vi_ , its confidence score decays: 


Entities transition through `Active` / `Uncertain` / `Archived` states based on confidence thresholds, and archived entities can be restored when re-observed. The complete lifecycle policy and curation algorithm are provided in Appendix B.6. 

# _3.2.7. Commit Conditions and Failure Handling_ 

The state transition is committed if and only if (1) the physical action is successfully executed by the controller (verified via force-torque feedback), and (2) the post-action perception verifies the expected geometric change specified in the ERT’s `causal_assumption` field (Section 3.3.3). Specifically, for `Pick(obj)` , we verify that _obj_ ’s position now tracks the gripper frame; for `Place(loc)` , we verify _obj_ is stationary at _loc_ within tolerance _ϵplace_ ; for `Insert(A,B)` , we verify the relative pose **T** _AB_ matches the expected mating geometry. 

If either condition fails (e.g., the object slips during transport), the transaction is rolled back and the Diagnosis Module (Section 3.3.5) is triggered, preventing the “hallucination accumulation” common in open-loop VLM planners. 

10 


Figure 4: **The Progressive VLM-Guided Planning and Deep Recovery Loop (Sec. 3.3).** Dynamic Context Engineering distills the DEWM state (Ω _, M, CS_ ) into a task-relevant prompt. The VLM then generates an External Reasoning Trace (ERT) which is mathematically validated before execution. On failure, the Deep Causal Diagnosis module computes the belief-outcome discrepancy (∆= Ω _t_ +1 _⊖Acausal_ ) to generate targeted feedback for belief correction and informed recovery. 

# _3.3. VLM-Guided Planning, Execution, and Recovery_ 

Having established a dynamic world model (Ω), we now detail the decision-making engine: the “Progressive VLM-Guided Planning Algorithm (Π)”. As illustrated in Fig. 4, this engine operates as a closed-loop controller that tightly couples VLM reasoning with the structured DEWM. Assuming a primitive skill library _A_ for low-level execution, the decision process follows a rigorous _StateInput-Process-Output_ cycle to generate verifiable, adaptive behavior. 

# _3.3.1. Internal Working Memory: Tracking Task and Ego-States_ 

Robust long-horizon autonomy requires tracking not just the external environment, but also the agent’s internal progress. We introduce two dedicated working memory modules: 

_a. Task Memory (Mt)_ 

This module serves as the “project manager”, tracking global operation progress. Formally, _Mt_ = _⟨TDAG, sst, Hash⟩_ : 

- _TDAG_ : The “Task Topology Path”, a Directed Acyclic Graph (DAG) decomposed from user instructions via VLM-based task decomposition (prompt template in Appendix C.2). 

- _sst_ : A state pointer to the active node in _TDAG_ (Status: `Executing` / `Completed` ). 

11 

- _Hash_ : The “Action Sequence History”, a structured log recording every executed ERT. This serves as the “episodic memory” enabling causal diagnosis. 

# _b. Constraint State (CSt)_ 

The Constraint State _CSt_ is central to our diagnosis mechanism (Contribution 3). While _S_ tracks geometric configurations, _CSt_ anchors the robot’s semantic interaction phase (e.g., _⟨_ `Holding` _,_ blue_block_1 or _⟨_ `Approaching` _,_ target_zone _⟩_ ). Updates to _CSt_ are event-driven, occurring only when the `causal_assumption` of a validated ERT is functionally fulfilled. This mechanism provides the micro-topological anchor required for precise failure localization: when an anomaly occurs, _CSt_ identifies _which interaction phase_ failed, enabling targeted diagnosis rather than generic task-level error handling. 

# _3.3.2. Dynamic Context Engineering_ 

VLMs are inherently context-agnostic. To ground their reasoning and prevent “lost-in-themiddle” hallucinations, we design a “Subgraph Extraction Pipeline” that acts as a deterministic filter between the DEWM and the VLM. 

Instead of feeding the entire world state Ω, which introduces irrelevant noise, the mechanism utilizes the current subtask _sst_ and topological state _CSt_ to index the Hierarchical Semantic Graph ( _G_ ). It extracts a “Task-Relevant Subgraph”—the minimal set of objects and relations required for the current decision—and serializes it into a concise natural language prompt. This strategy minimizes token usage while maximizing information density. The subgraph extraction algorithm is detailed in Appendix C.1, with context-specific prompt templates for task decomposition (Appendix C.2), motion planning (Appendix C.3), and fine manipulation (Appendix C.4). 

# _3.3.3. The Cognitive Core: External Reasoning Trace (ERT)_ 

To transform the VLM from an opaque “black box” into a verifiable agent, we enforce a structured output format called the “External Reasoning Trace (ERT)”. Every planning step produces a JSON object containing four key fields: 


Here, _πact_ is the action proposal, _Bworld_ represents structured assertions about the pre-condition, _Acausal_ encodes the expected post-conditions, and _κconf_ is the self-evaluated confidence. 

Crucially, the ERT functions as a probabilistic hypothesis subject to verification. Before execution, it undergoes a Multi-Layered Validation Protocol (see Appendix D), which rigorously checks the consistency between the VLM’s semantic beliefs ( _Bworld_ ) and the geometric ground truth in DEWM. This mechanism acts as a cognitive firewall, intercepting hallucinations before they manifest as physical errors. 

It is important to note that the ERT protocol focuses exclusively on Semantic Task Feasibility (e.g., verifying geometric containment). We explicitly decouple low-level kinematics and dynamics—such as collision avoidance and singularity handling—to the downstream execution layer. Exceptions at this lower level are captured as feedback signals and routed to the Constraint State ( _CS_ ) module to trigger the diagnosis pipeline. 

# _3.3.4. Main Planning Loop and Adaptive Control_ 

The core control logic is encapsulated in the progressive planning algorithm (Algorithm 1). To ensure robustness, all inference calls are encapsulated within a “Verify-Retry” wrapper, `GetValidERT` . The system operates in two hierarchical modes: 

12 

1. Macro-Planning (Algorithm 1): Handles high-level state transitions and discrete single-step actions. 

2. Micro-Routine (Algorithm 2): Synthesizes detailed primitive sequences for contact-rich manipulation. 

**Algorithm 1** Progressive VLM-Guided Planning <u>(Main</u> Loop) 

**Require:** Task _T_ , Skill Library _A_ , Max Retries _Nmax_ **Ensure:** Task Status: `Completed` or `Failed` 1: Ω _, M, CS ←_ InitializeSystem( _T_ ) 2: **while** GetStatus( _M_ ) _̸_ = `Completed` **do** 3: Ω _t, Mt, CSt ←_ PerceiveAndUpdate(Ω _t−_ 1) 4: _sst ←_ GetCurrentSubtask( _Mt_ ) 5: **if** _sst_ is `ManipulationTask` **then** 6: _status ←_ ExecuteMicroRoutine(Ω _t, Mt, CSt, sst_ ) 7: **else** 8: _Prompt ←_ SynthesizeContext(Ω _t, Mt, CSt_ ) 9: _ERT, valid ←_ GetValidERT( _Prompt, Nmax_ ) 10: **if** _¬valid_ **then return** `Failed` 11: **end if** 12: _skill ←_ ExtractAction( _ERT_ ) 13: _status ←_ Execute( _skill, A_ ) 14: **end if** 15: UpdateState( _Mt, CSt, status, ERT_ ) 16: **if** _status_ == `Failed` **then** 17: DeepCausalDiagnosis(Ω _t, Mt, ERT_ ) _▷_ Trigger Recovery 18: **end if** 19: **end while** 

20: **return** `Completed` 

# _3.3.5. Deep Causal Diagnosis and Belief Correction (CS-Anchored Recovery)_ 

When a subtask fails (Line 18, Algorithm 1), the recovery mechanism goes beyond simple retries. The Belief-Action History ( _Hash_ ) retains the full ERT recorded prior to the failure. The `DeepCausalDiagnosis` function triggers a diagnostic flow by computing the semantic divergence ∆ between the `causal_assumption` in the ERT and the actual post-failure reality Ω _t_ +1: 


Here, _⊖_ denotes the set difference of semantic states (formally defined in Appendix C.6). 

This calculation generates a precise **Belief-Outcome Discrepancy Report** (Appendix C.6), which is fed back to the VLM via `SynthesizeReplanPrompt` (template in Appendix C.5). This enables the agent to perform _Belief Correction_ —updating its internal model based on evidence—rather than merely generating a different plan, fundamentally distinguishing our approach from blind retry strategies. 

# **4. Experiments** 

To rigorously validate the effectiveness of the proposed VLM-DEWM cognitive architecture, we designed a comprehensive suite of experiments across high-fidelity simulation and real-world physical platforms. Our evaluation aims to answer three core Research Questions (RQs): 

13 

# **Algorithm 2** Micro-Manipulation Subroutine 

**Require:** World Ω _t_ , Memory _Mt_ , State _CSt_ , Subtask _sst_ 

- 1: _Prompt ←_ SynthesizeMicroPrompt(Ω _t, Mt, CSt, sst_ ) 

- 2: _ERTmicro, valid ←_ GetValidERT( _Prompt, Nmax_ ) 

- 3: **if** _¬valid_ **then return** `Failed` 

- 4: **end if** 

- 5: _Seq ←_ ExtractSequence( _ERTmicro_ ) 

- 6: **for** _skill_ in _Seq_ **do** 

- 7: _status ←_ Execute( _skill, A_ ) 

- 8: UpdateState( _Mt, CSt, status, ERTmicro_ ) 

- 9: **if** _status_ == `Failed` **then return** `Failed` 

- 10: **end if** 

- 11: **end for** 

- 12: **return** `Success` 

1. Long-Horizon Reliability: Can DEWM provide persistent, cross-regional world memory to support state tracking and zero-shot spatial reasoning, outperforming pure VLMs that rely solely on context history? 

2. Precise Diagnosis: Compared to other memory-enhanced strategies, does the _Micro-Topological State Anchoring_ ( _CS_ ) mechanism enable more accurate causal diagnosis and intelligent recovery in dynamic environments? 

3. Sim-to-Real Generalization: Can the core cognitive logic of VLM-DEWM generalize from simulation to physical interaction with real-world sensor noise and latency? 

# _4.1. Experimental Setup_ 

This section details our experimental configuration. We describe the baseline methods in Section 4.1.1, platform implementation details in Section 4.1.2, experimental assumptions in Section 4.1.3, task design in Section 4.1.4, and evaluation metrics in Section 4.1.5. 

# _4.1.1. Baseline Methods_ 

We compare VLM-DEWM against two categories of baselines representing mainstream embodied planning paradigms. 

# _a. Context-Only VLM Planners_ 

This category relies exclusively on the VLM’s context window to maintain world understanding, without explicit external memory structures. We include both SOTA closed-source models (Gemini 2.5 Pro, GPT-5) and open-source models (Qwen3-VL-32B-Instruct, GLM-4.5V). For fairness, all VLM baselines are integrated into the same perception-planning loop, with their “memory” consisting solely of historical images and text prompts. 

# _b. Memory-Enhanced Strategies_ 

This category constructs external memories for VLMs and is most relevant to our work. We select “SAGE” [13] (a 3D Scene Graph approach) and “GEAR” [14] (a SOTA VLM-RAG method) as representative competitors, reproducing them according to their official specifications. 

# _c. Ours (VLM-DEWM)_ 

We utilize Gemini 2.5 Pro as the core “cognitive collaborator”. This choice allows for a direct “apples-to-apples” comparison with the Pure Gemini 2.5 Pro baseline, isolating the performance gains attributable to the DEWM architecture rather than the underlying model capability. 

14 

# _4.1.2. Implementation Details_ 

# _a. Simulation Environment_ 

Our simulation platform is built on PyBullet and Gazebo. To rigorously isolate cognitive performance from perceptual noise, we adopt a "privileged information" strategy in simulation. Perfect segmentation masks (via `p.getCameraImage` ) and ground-truth 6D poses are fed directly to the cognitive module. This ensures that the evaluation strictly benchmarks the DEWM’s logic (memory, planning, diagnosis) rather than the upstream perception model errors. 

_b. Real-World Platform and Protocols_ 

- The physical validation was conducted on a high-fidelity robotic cell designed to emulate in- 

- dustrial assembly (Fig. 11). • Hardware Specs: We use a Franka Emika Panda (7-DoF, 1kHz control loop) equipped with a Robotiq 2F-85 gripper. Perception is provided by an Intel RealSense D435i (848 _×_ 480 resolution @ 30fps), mounted extrinsically. 

   - Sample Size ( _N_ ): For Task 3, we conducted a total of 60 trials among which 20 trials were subjected to induced failures (covering 3 failure modes: Part Slip, Obstacle, Target Moved). 

   - Success Criteria: A trial is successful if and only if the final assembly is completed within a 5mm position tolerance and 2 degree orientation tolerance relative to the CAD specification, verified by a calibrated overhead camera. 

   - Throughput Metric: We define _Effective Throughput_ as Avg. Cycle3600Time _<u>s</u>_ +MTTR<sup>.Thispenalizes</sup> methods that require manual reset after failure. 

To filter perceptual noise, we adopt our prior Coarse-to-Fine 3D-Grounded Perception framework [28], ensuring the evaluation focuses on cognitive performance rather than upstream perception errors. This framework integrates open-vocabulary 2D detection with 3D point cloud clustering and outlier removal. By enforcing both semantic consistency and geometric density constraints, it effectively filters out perceptual hallucinations before they enter the DEWM update loop. This allows our evaluation to focus specifically on the cognitive performance of the memory and reasoning modules. 

# _4.1.3. Experimental Assumptions and Priors_ 

To ensure rigor and alignment with target applications (e.g., smart manufacturing), we define the following assumptions: 

- Semi-Structured Environment: We assume object categories are known, but their poses, quantities, and topological relationships are unknown and dynamic. 

- Shape Prior Library ( _L_ ): For high-precision interaction (Task 3), the system is provided with a Shape Prior Library containing CAD models and grasp priors, as described in Section 3.2. 

- Fairness Note: This library _L_ is provided to _all_ baselines (including SAGE and GEAR) to ensure the comparison focuses on “memory and diagnosis” rather than “grasp pose learning”. 

15 

# _4.1.4. Experimental Tasks_ 

We designed three distinct tasks to evaluate the system’s performance across long-horizon planning, large-scale memory retention, and dynamic resilience. To ensure relevance to RCIM readers, these tasks are modeled after core scenarios in flexible manufacturing and intralogistics. 

_Task 1: Long-Horizon Multi-Stage Assembly (Simulation)_ 

Modeled after a “PCB Component Kitting and Insertion” process. The robot operates in a multi-zone workcell ("Factories") containing various "components" (blocks/cylinders representing capacitors/chips). _Goal:_ The VLM must parse a high-level manufacturing order (e.g., "Assemble the Red Kit and transfer to Zone C"), decomposing it into a sequence of 10+ manipulation steps (pick, place, stack), requiring strict adherence to geometric constraints and logical dependencies. 

_Task 2: Large-Scale Facility Inventory (Simulation)_ 

Simulates an automated inventory management task in a large-scale warehouse or town environment. _Goal:_ The robot performs a random-walk exploration to build a semantic map of the facility. The system is then subjected to a rigorous "Inventory Audit" (Q&A phase), assessing its ability to recall the location ("Where is the emergency stop?"), count ("How many pallets?"), and spatial relations of entities across the entire facility, testing the capacity of DEWM to handle large-scale static data. 

_Task 3: Dynamic Exception Handling (Real-World)_ 

Replicates a “High-Mix Low-Volume Assembly Line” prone to runtime disturbances. _Goal:_ The robot performs a standard pick-and-place assembly on the physical Franka platform. We introduce real-world anomalies common in factory settings, such as part slippage (gripper failure) and unexpected obstacles (safety stops). The system must diagnose these interruptions in real-time and generate "Informed Recovery" strategies (e.g., "Re-grasp" or "Clear Obstacle") to minimize downtime, rather than blindly halting or retrying. 

# _4.1.5. Evaluation Metrics_ 

Let _N_ be the total number of trials and I( _·_ ) be the indicator function. We employ five quantitative metrics to evaluate system performance: 

# _a. Industrial Reliability (Task Success Rate - TSR)_ 

Serves as the primary measure of end-to-end operational effectiveness (proxy for manufacturing yield rate). A trial is deemed successful only if all physical sub-goals are met and (for Task 2) all verification questions are answered correctly. 


where _N_ is the total number of experimental trials. 

# _b. Digital Twin Fidelity (State Tracking Accuracy - STA)_ 

Quantifies the accuracy of the DEWM in maintaining object states when they are Out-ofView (OOV), acting as a metric for process monitoring quality. At each timestep _t_ , we compare the estimated state _SEWM_ ( _o_ ) against the simulation ground truth _SGT_ ( _o_ ), averaged over the task duration _T_ : 


16 

This metric rigorously evaluates the "Object Permanence" capability required for reliable inventory tracking. 

# _c. Operational Cost & Latency (Planning Efficiency - PE)_ 

Acts as a proxy for economic cost (Token consumption) and cycle time (Inference latency). It is defined as the total count of VLM API calls per trial ( _Ncalls_ ), separating initial planning ( _Ninit_ ) from error-induced replanning ( _Nreplan_ ): 


A lower PE indicates a stable memory context that minimizes expensive model queries, directly translating to a more cost-effective production cycle. 

_d. Memory Storage Efficiency (Information Efficiency - IE)_ 

Measures the storage density of the system, critical for long-term deployment. It is calculated as the ratio of valid information queries answered ( _NInfo_ ) to the total number of memory entries ( _NItems_ ) stored in the database: 


High IE indicates that the system stores highly relevant, structured knowledge rather than redundant raw logs (as seen in baseline SAGE). 

_e. Diagnostic Precision (Causal Diagnosis Accuracy - CDA)_ 

Evaluates the system resilience and ability to minimize “Mean Time to Recovery (MTTR)”. It measures the percentage of diagnostic attempts where the system-generated reason _Rgen_ matches the ground truth reason _RGT_ : 


where _M_ is the total number of diagnostic attempts (not failure events), as a single failure may require multiple diagnosis rounds before successful recovery. Unlike “Blind Retry” strategies (CDA=0), a high CDA enables “Informed Replanning”, significantly reducing downtime. 

_Ground Truth Labeling Protocol:_ To ensure objectivity and reproducibility, _RGT_ is determined through a post-hoc sensor log analysis protocol rather than subjective judgment. Specifically, for each induced failure event, we record synchronized multi-modal logs including: (1) gripper width and force-torque readings from the Franka controller, (2) RGB-D frames at 10 Hz, and (3) joint states and end-effector poses. 

# _4.2. Main Results: Comparison with Baselines_ 

We conducted comprehensive comparisons against the baselines defined in Section 4.1.1 across both simulation and real-world platforms. The results for the three core tasks are presented in Tables 2, 4, and 5. 

# _4.2.1. Task 1: Long-Horizon Assembly & Reasoning (Simulation)_ 

Task 1 evaluates the system’s ability to handle multi-step physical interactions and maintain state persistence. The scene comprises three distinct zones (“Factories”) containing blocks, spheres, and cylinders (see Fig. 5). 

17 


Figure 5: **Task 1 Environment Setup.** The multi-zone factory simulation scene containing blocks, spheres, and cylinders distributed across three distinct platforms. This raw visual input triggers the memory construction process. 

# _a. Memory Construction Analysis_ 

Starting from the raw simulation input (Fig. 5), the system successfully decouples the static background _Sbg_ from dynamic entities _Sobj_ (Fig. 6a-b). Simultaneously, the initial topological state is grounded in the Semantic Graph _G_ (Fig. 6c). 


Figure 6: **Initial Memory Construction in Task 1. (a-b)** The Geometric Layer of DEWM separates the static background (Left) from dynamic objects (Right). **(c)** The Semantic Layer initializes the topological graph and its matrix representation, anchoring the scene’s logical structure before manipulation. 

# _b. Reasoning and Execution Analysis_ 

The reasoning process is captured in Fig. 7. Specifically, the robot received the high-level instruction: “Transport the red cube from Zone A and stack it onto the blue cylinder in Zone B.” The Task Memory _M_ (Fig. 7a) decomposes the high-level instruction into a structural plan. Most importantly, by comparing the initial matrix in Fig. 6(c) with the post-execution matrix in 

18 

Fig. 7(b), we observe the dynamic graph update: relations are rewritten in real-time upon action completion (e.g., `On(cube, table)` _→_ `On(cube, cylinder)` ). This capability explains our high STA scores compared to the static memory of GEAR. 


(a) VLM-Generated Task Topology Path ( _M_ ) 


Figure 7: **Reasoning and Dynamic Update Process. (a)** Based on the initial memory, the VLM decomposes the instruction “Complete Red Assembly” into a hierarchical execution tree. **(b)** After execution, the DEWM reflects the new physical reality. By comparing this with Fig. 6c, we observe the real-time topology update (e.g., edge `On(cube, table)` is replaced by `On(cube, cylinder)` ), verifying the system’s dynamic tracking capability. 

# _c. Quantitative Analysis_ 

As shown in Table 2, VLM-DEWM outperforms all baselines ( _N_ = 50 trials). 

- Ours: We achieved a 94.0% TSR with near-perfect 100% STA. The PE (75) is higher than pure VLMs because our architecture actively invokes the VLM for verification and geometric adjudication (Sec. 3.3.3), whereas pure VLMs rely on a single, hallucination-prone generation (PE=1). Crucially, our 100% IE confirms that the structured memory ( _G, S_ ) stores zero redundant information. 

- Memory-Enhanced Baselines: SAGE achieved a moderate 72% TSR but suffered from severe inefficiency (PE=261, IE=12.26%). Its unstructured “agent-to-agent” dialogue logging forces the VLM to parse redundant text, degrading performance. GEAR failed completely (0% TSR) because its static RAG knowledge base could not update object locations after manipulation, leading to fatal conflicts between memory and reality. 

- Pure VLMs: Despite receiving initial positions, pure VLMs struggled with the long horizon, exhibiting severe hallucination (TSR 0–28%). Only the strongest models (Gemini 2.5 Pro, GPT-5) managed sporadic successes. 

19 

Table 2: Quantitative Results for Task 1 (Long-Horizon Assembly) 

|**Method**|**VLM Core**|**TSR (%)** _↑_|**STA (%)** _↑_|**PE** _↓_|**IE (%)** _↑_|
|---|---|---|---|---|---|
|**VLM-DEWM (Ours)**|Gemini 2.5 Pro|**94.00**|**100.00**|75|**100.00**|
|SAGE [13]|Gemini 2.5 Pro|72.00|83.33|261|12.26|
|GEAR [14]|Gemini 2.5 Pro|0.00|–|148|–|
|Gemini 2.5 Pro|Gemini 2.5 Pro|28.00|39.74|**1**|–|
|GPT-5|GPT-5|12.00|34.62|**1**|–|
|Qwen3-VL|Qwen3-VL|0.00|30.77|**1**|–|
|GLM-4.5V|GLM-4.5V|0.00|15.38|**1**|–|


_Note:_ Pure VLMs achieve PE=1 due to a single long-context prompt, but fail to complete the task (Low TSR). 

# _4.2.2. Task 2: Large-Scale Exploration (Simulation)_ 

This task evaluates memory construction and zero-shot spatial reasoning in a town-scale environment. We introduce “Query Success Rate (QSR)” as the primary metric, assessed via a graded question set (Table 3). 


Figure 8: **Task 2 Environment Setup.** Multi-modal inputs (LIDAR + Camera) + semantic segmentation acquired during the town-scale exploration. This raw sensory stream serves as the input for constructing the DEWM. 

- _a. Hierarchical Memory Construction_ 

The DEWM construction process is visualized in Fig. 9. Starting from raw inputs, the system builds a persistent global map _Sbg_ and extracts key landmarks into the object registry _Sobj_ (Fig. 9ab). These geometric entities are abstracted into the town-scale semantic graph _G_ (Fig. 9c), which serves as the knowledge base for answering the Q&A set defined in Table 3. 

- _b. Exploration Process Analysis_ 

In this scenario, the robot performed a 240-step random-walk exploration mission to map the 

20 

Table 3: Task 2 Spatial Question Set Distribution 

|**Difficulty**|**Count**|**Description**|
|---|---|---|
|Easy|15|Basic Recognition (e.g., “Is there a bank?”)|
|Medium|20|Spatial Relations (e.g., “Is the bench near the park?”)|
|Hard|5|Multi-step Reasoning (e.g., Navigation heuristics)|
|High|10|Daily Scenario Q&A|


Figure 9: **Hierarchical Memory Construction in Task 2. (a)** The reconstructed global semantic map serves as the metric substrate. **(b)** Key landmarks (e.g., hydrants) are extracted as object-centric instances. **(c)** The Semantic Graph abstracts these entities into topological relations (e.g., `Near(bench, park)` ), enabling efficient spatial querying. 

21 

unknown facility. The temporal evolution of this mission is captured in the exploration history (Fig. 10). The sparsity of Green nodes (New Entity) versus Yellow nodes (Re-observation) in the tree visually demonstrates our high Information Efficiency (IE), as the system effectively recognizes previously seen areas without redundant memory writes, creating a compact yet comprehensive map. 


Figure 10: **Exploration Execution History (** _M_ **).** The temporal tree visualizes the robot’s 240-step exploration path. Color-coded nodes indicate memory events: **Green** nodes mark steps where new entities were discovered and registered into _G_ ; **Yellow** nodes indicate steps with only re-observations, demonstrating the system’s efficiency in avoiding redundant updates. 

# _c. Quantitative Analysis_ 

As shown in Table 4, VLM-DEWM exhibits overwhelming advantages in memory quality. 

- **Ours:** We achieved **94.0% QSR** and **90.14% IE** . By structuring the town into a hierarchical graph _G_ , our system converts spatial reasoning into efficient _database queries_ rather than text processing. The PE (509) reflects the necessary cost of building a persistent map over 240 observation points. 

- **Baselines:** SAGE showed disastrous efficiency (PE=2162, IE=1.30%). Its unstructured logging forced the VLM to perform “needle-in-a-haystack” retrieval on redundant text, limiting QSR to 52%. Pure VLMs acted as streaming processors with no long-term retention (STA _≈_ 29%), failing to answer cross-regional queries. 

22 

Table 4: Quantitative Results for Task 2 (Exploration & Q&A) 

|**Method**|**VLM Core**|**QSR (%)**|_↑_**STA (%)** _↑_|**PE** _↓_|**IE (%)** _↑_|
|---|---|---|---|---|---|
|**VLM-DEWM (Ours)**|Gemini 2.5 Pro|**94.00**|**92.68**|509|**90.14**|
|SAGE|Gemini 2.5 Pro|52.00|56.10|2162|1.30|
|GEAR|Gemini 2.5 Pro|74.00|-|240|-|
|Gemini 2.5 Pro|Gemini 2.5 Pro|-|29.27|240|-|


# _4.2.3. Task 3: Real-World Dynamic Recovery_ 

Finally, we validated the system on the physical Franka platform (Fig. 11) using a dynamic assembly task with induced failures. 

Fairness Note: As specified in Section 4.1.3, all methods utilized the same Shape Prior Library ( _L_ ) for grasp pose generation. This isolates the evaluation to strictly focus on _memory, state tracking, and diagnosis_ , decoupling it from low-level manipulation skill proficiency. 

# _a. Mechanism and Qualitative Analysis_ 

Figure 11 illustrates the mechanism behind this resilience. In a standard cycle, the robot is tasked to retrieve a gear and insert it into a shaft. During the transport phase, we induced a “Gripper Slip” failure, causing the part to fall onto the table. 

The core challenge in Task 3 is the dynamic evolution of the environment (e.g., new obstacles appearing during failure). Baselines like SAGE and GEAR rely on a static snapshot memory; once the environment changes, their knowledge base suffers from _epistemic stagnation_ , leading to inevitable planning conflicts. In contrast, VLM-DEWM maintains a live topology. When the transport failure occurs (Fig. 11, bottom), the system detects the topological breach (Expected: `Holding` , Actual: `Idle` ). Instead of hallucinating success or freezing, it autonomously triggers a “Re-perception and Search” routine, effectively closing the cognitive loop in the physical world. _b. Quantitative Analysis_ 

Table 5 reveals a stark contrast: VLM-DEWM achieved an 95.0% TSR, while all baselines failed completely (0% TSR). 

- Cognitive Resilience via Iterative Diagnosis (Ours): A critical insight lies in the relationship between CDA (36.96%) and TSR (95.0%). Among the 20 induced failures, the system diagnosed the root cause _immediately_ in only 6 cases. However, in 11 cases, it successfully anchored the failure after multiple diagnostic rounds ( _N < Nmax_ = 5). This proves that VLM-DEWM possesses cognitive resilience: it does not require perfect zero-shot diagnosis but can progressively converge to the correct causal explanation through interaction, a capability entirely absent in standard VLM planners. 

- Catastrophic Failure of Baselines: Baselines consistently scored 0% CDA. Without the micro-topological anchoring provided by the _CS_ module, baselines suffered from “state aliasing”—they could not distinguish between physically distinct failure modes (e.g., `Slip` vs. `Collision` ). Consequently, they defaulted to a “Blind Retry” loop, repeating the same erroneous trajectory without updating their internal world model. 

23 


Figure 11: **Real-World Deployment.** The Franka Emika Panda performing the dynamic assembly task. The system successfully diagnoses and recovers from induced execution failures using the _CS_ -based causal diagnosis. 

24 

Table 5: Real-World Dynamic Recovery Results ( _N_ = 60) 

|**Method**|**VLM Core**|**TSR (%)** _↑_|**CDA (%)** _↑_|
|---|---|---|---|
|**VLM-DEWM (Ours)**|Gemini 2.5 Pro|**95.00**|**36.96**|
|SAGE|Gemini 2.5 Pro|0.00|0.00|
|GEAR|Gemini 2.5 Pro|0.00|0.00|
|Pure VLM|Gemini 2.5 Pro|0.00|0.00|


# _4.2.4. Baseline Failure Analysis_ 

The zero TSR achieved by all baselines in Task 3 warrants detailed explanation, as it may raise concerns about task fairness. We emphasize that this outcome reflects _fundamental architectural limitations_ rather than unfair task design. Below we analyze the failure modes of each baseline category. 

# _a. Pure VLM (Stateless Reasoning)_ 

Pure VLMs operate in a _single-shot, stateless_ manner: they receive the current image and task instruction, then generate an action without persistent memory. When a gripper slip occurs midtransport, the VLM observes an image where the target object has “disappeared” from the gripper. Without access to the prior state (i.e., the object was being held), the VLM cannot distinguish between three possibilities: (1) the object was successfully placed, (2) the object was dropped, or (3) the object was never picked. In our experiments, Pure VLMs consistently misinterpreted slip events as successful placement, proceeding to the next subtask and causing cascading failures. 

# _b. SAGE (Dialogue-Based Memory)_ 

SAGE [13] maintains memory through unstructured agent-to-agent dialogue logs. While this enables semantic persistence, it lacks two critical capabilities for failure recovery. First, SAGE has no _geometric grounding_ : when the robot reports “I dropped the object,” SAGE cannot determine _where_ the object fell because its memory contains only textual descriptions without metric coordinates. Second, SAGE lacks _interaction-phase awareness_ : it cannot distinguish whether a failure occurred during `Approaching` , `Grasping` , or `Transporting` phases. Without this microstate anchoring (provided by _CS_ in our architecture), SAGE’s recovery attempts were spatially ungrounded, causing the robot to search in incorrect locations. 

# _c. GEAR (Static Knowledge Graph)_ 

GEAR [14] constructs a knowledge graph from initial observations but does not support _dynamic relation updates_ . In Task 3, when an object’s spatial relation changes due to external disturbance (e.g., from `On(obj, gripper)` to `On(obj, floor)` ), GEAR’s static graph retains the outdated relation. This causes a fatal _belief-reality divergence_ : the planner continues to assume the object is held while perception shows otherwise. GEAR has no mechanism to reconcile this conflict, leading to repeated execution of invalid actions until timeout. 

# _d. Architectural Implications_ 

These failure patterns validate our core thesis: failure recovery in dynamic environments requires (1) _persistent geometric memory_ to localize anomalies, (2) _dynamic state updates_ to track relation changes, and (3) _interaction-phase anchoring_ to diagnose failure causes. VLM-DEWM integrates all three through the _S_ - _G_ - _CS_ architecture, explaining its qualitative advantage in recovery scenarios. We acknowledge that Task 3 was designed to stress-test these capabilities; however, such disturbances (gripper slips, unexpected obstacles) are _routine occurrences_ in real manufacturing 

25 

Table 6: Ablation Study of Core Components in Real-World Task 3 ( _N_ = 20) 

|**Method**|**TSR (%)** _↑_|**CDA (%)** _↑_|**STA (%)**|_↑_<br>**QSR (%)** _↑_|**PE (calls)** _↓_|
|---|---|---|---|---|---|
|**VLM-DEWM (Full)**|**95.00**|**68.97**|**100.00**|**100.00**|**54**|
|w/o _S_|0.00|-|0.00|60.00|-|
|w/o _G_|0.00|-|0.00|0.00|-|
|w/o _M_|90.00|-|100.00|100.00|266|
|w/o _CS_|55.00|0.00|97.50|95.50|-|


environments, making this evaluation industrially relevant rather than artificially adversarial. 

# _4.3. Ablation Studies_ 

To rigorously validate the necessity of the four core components— _S_ (Geometric Layer), _G_ (Semantic Layer), _M_ (Task Memory), and _CS_ (Constraint State)—we conducted a comprehensive ablation study on the real-world Franka platform. 

# _4.3.1. Experimental Setup_ 

We reused the task 3 (Dynamic Recovery) setup as it involves complex manipulation sequences that fully exercise all cognitive modules. We evaluated five model variants ( _N_ = 20 trials each). 

Protocol Note: To ensure independence, all scene-specific memories in DEWM were cleared between trials. However, aligned with industrial assembly scenarios, the Shape Prior Library ( _L_ ) containing grasp poses for known parts was retained. 

Additional Metric: We introduced a specific Q&A set for this ablation, comprising 5 spatial questions (e.g., “Relation between Part A and B?”) and 5 semantic questions (e.g., “Count of green parts?”), to measure the internal consistency of the memory. 

# _4.3.2. Model Variants_ 

- **VLM-DEWM (Full):** The complete architecture proposed in this paper. 

- **w/o** _S_ **(No Geometric Anchor):** _S_ is removed. The system retains _G_ , _M_ , and _CS_ , but VLM reasoning lacks physical anchoring and the “Geometric Adjudication” capability. 

- **w/o** _G_ **(No Semantic Interface):** _G_ is removed. The VLM must attempt to extract context directly from raw geometric data ( _S_ ), losing the structured symbolic interface. 

- **w/o** _M_ **(No Task Memory):** _M_ is removed. The system possesses a world model ( _G_ + _S_ ) and micro-states ( _CS_ ) but lacks the Task Topology Path (TTP) and Action State History (ASH). 

- **w/o** _CS_ **(No Diagnostic Anchor):** The micro-topological state module is removed. In failure events, the system perceives only macro-task failure without micro-state granularity. 

26 

# _4.3.3. Analysis of Ablations_ 

As presented in Table 6, all four components proved indispensable. 

# _a. VLM-DEWM (Full)_ 

The full architecture served as the benchmark, achieving a 95.0% TSR and perfect state tracking (100% STA/QSR). _Failure Analysis:_ Only one trial failed completely, caused by a hardware safety stop triggered by LIDAR glare, which positioned the target out of the workspace. This hardwarelevel exception confirms that the cognitive logic itself remained robust, achieving a high diagnosis rate (68.97% CDA) for induced failures. 

# _b. w/o S: Epistemic Detachment_ 

This variant failed completely (0% TSR). When an object was deliberately moved, the semantic belief in _G_ (e.g., `On(blue_cube, table)` ) became obsolete. Lacking _S_ for “Geometric Adjudication” (Section 3.3.3) and spatial memory for Out-of-View objects, the system could not detect this deviation. _Result:_ The VLM generated plans based on stale beliefs, causing execution at incorrect locations. While it could answer semantic questions (QSR 60%), the 0% STA reveals a fatal detachment between “Belief” and “Reality”. 

# _c. w/o G: Symbol Grounding Failure_ 

Removing _G_ rendered the system inoperable (0% TSR). _G_ acts as the “Translation Interface” that bi-directionally binds high-level VLM symbols to physical entities in _S_ . Without this interface, the VLM could not “ground” its instructions into raw pose data, failing to generate even the first step. Consequently, semantic awareness vanished (STA/QSR _≈_ 0%), proving _G_ is critical for VLM-compatible interaction. 

# _d. w/o M: Efficiency Collapse (Transient Memory)_ 

This variant highlights the efficiency role of _M_ . Without TTP and ASH, the system exhibited “transient memory”, forgetting long-term goals after every step. It was forced to replan from scratch continuously. _Result:_ While perception modules ( _G, S, CS_ ) kept accuracy high (90% TSR), the computational cost exploded. In trials with induced failures, the redundant replanning drove the VLM API calls to 266 (compared to 54 for Full), confirming _M_ ’s role in guaranteeing long-horizon efficiency. 

# _e. w/o CS: Diagnostic Blindness_ 

This variant validated the “Deep Causal Diagnosis” mechanism (Section 3.4.4). In the 20 trials, we observed 6 gripper slips and 3 perception deviations. Lacking the micro-topological states (e.g., `Approaching` vs. `Transporting` ) as anchors, the system perceived these only as generic macrofailures (CDA 0%). Lacking a detailed Discrepancy Report, it defaulted to “Blind Retry”, which fails in dynamic environments. The significant drop in TSR (to 55%) confirms that _CS_ is essential for intelligent recovery. 

# _f. Remark on ERT_ 

Notably, our ablation does not include a “w/o ERT” variant. In our architecture, ERT is not a removable component but the fundamental communication protocol (Section 3.4.2) connecting “Thought” (VLM) and “Memory” (DEWM). As shown by the “Pure VLM” baselines in Section 4.1.1 (TSR _≈_ 0%), removing this structured verification protocol causes the system to fail fundamentally. 

27 

# _4.4. Discussion_ 

Our experiments in simulation and real-world environments (Sections 4.2, 4.3) fundamentally validate the efficacy of our core contribution: the ERT cognitive Paradigm. The results unambiguously demonstrate that the failure of baseline methods stems from their opaque nature—they lack a verifiable “transaction” mechanism (ERT) and a persistent “database” (DEWM). 

Conversely, the success of VLM-DEWM derives from this verifiable closed loop. In this section, we deeply analyze how the specific data structures of DEWM ( _G, S, M, CS_ ) serve as indispensable components for this paradigm (Section 4.4.1) and candidly discuss the system’s failure boundaries (Section 4.4.2). 

# _4.4.1. Structured Memory Beyond Context Windows_ 

The ablation results (Table 6) reveal a clear architectural necessity: each DEWM component addresses a specific cognitive deficit that causes baseline failures. The Semantic Graph ( _G_ ) provides a structured, queryable interface that eliminates the inefficient “needle-in-a-haystack” retrieval seen in SAGE (IE=1.30%). The Spatial Network ( _S_ ) serves as a geometric anchor that maintains belief-reality synchronization, preventing the “epistemic detachment” observed in GEAR and Pure VLMs. The Task Memory ( _M_ ) provides temporal scaffolding for long-horizon planning, avoiding the efficiency collapse (PE=266) of memoryless agents. Finally, the Constraint State ( _CS_ ) enables micro-topological diagnosis, transforming “blind retry” into “informed recovery”. The complete failure of single-component ablations (TSR=0% for w/o _G_ and w/o _S_ ) confirms that these modules form an indivisible cognitive whole. 

# _4.4.2. Limitations and Failure Mode Analysis_ 

While VLM-DEWM demonstrates robust cognitive resilience, it operates under specific assumptions. Violating these boundaries leads to performance degradation or failure. 

_a. World Model Pollution (Upstream Perception Errors)_ 

The quality of DEWM is bounded by the Symbolic Perception Interface (Section 3.3.1). The system cannot self-correct corrupted sensory inputs; it faithfully “memorizes” errors. 

- _Scenario:_ If the segmentation model erroneously merges two red cubes into one large cuboid, _G_ will register a single entity. A VLM instruction to “Pick one of the cubes” becomes unexecutable. 

- _Scenario:_ As observed in one failed trial, LIDAR glare or transparent objects can prevent _S_ from building stable Gaussian envelopes, causing “Geometric Adjudication” to return null results continuously. 

# _b. Open-Vocabulary Disaster (Closed-World Assumption)_ 

Our architecture, specifically the category fields in _G_ and the Shape Prior Library _L_ , implicitly assumes a semi-structured world where object categories are known. 

- _Scenario:_ If a novel object (e.g., a “yellow banana”) appears on the industrial assembly table, VLM-driven Data Association (Section 3.3.2) will fail. The system may either ignore it as an obstacle or, worse, hallucinate it as a geometrically similar known part (e.g., “yellow cylinder”) and attempt a forceful insertion, leading to physical damage. 

28 

# _c. Scope of Physical Verification (Dynamics Gap)_ 

Our current "Physical Consistency Check" focuses on geometric feasibility (e.g., collisions, containment). We explicitly acknowledge that the current framework does not verify dynamics (e.g., payload stability under acceleration) or kinematics (e.g., joint limits during trajectory). In our implementation, these checks are offloaded to the low-level impedance controller. Future work will integrate a physics simulator (e.g., MuJoCo) into the ERT verification loop to catch dynamic failures _ex-ante_ . 

- _d. Granularity Limits of Causal Diagnosis_ 

The _CS_ module enables topological diagnosis but lacks physical granularity. 

   - _Scenario:_ If an object slips during transport due to low friction, the system correctly diagnoses the topological mismatch (Expected: `Holding` , Actual: `Idle` ). However, it does not know the _physical cause_ (friction vs. force). Consequently, the recovery strategy (“Retry Grasp”) might fail again if the underlying physical parameter (grasp force) is not adjusted. 

- _e. The “Cognitive Cost” of Deliberation_ 

Our architecture is deliberative, not reactive. The “Verify-Reflect” loop imposes a latency cost. 

- _Scenario:_ In highly dynamic tasks requiring reflex-level responses (e.g., catching a rolling ball), the system’s cognitive cycle time (reflected in PE) creates a “Reactivity Gap”. By the time an ERT is generated and verified, the world state may have already drifted, rendering the action obsolete. 

# **5. Conclusion and Future Work** 

This paper addresses two critical challenges in VLM-based long-horizon robotic planning: world-state drift caused by implicit, transient state encoding, and opaque failure diagnosis that necessitates costly blind retries. We attribute these failures to a fundamental responsibility mismatch—asking VLMs to simultaneously perform semantic reasoning and maintain dynamic world states within a limited context window. To resolve this, we proposed VLM-DEWM, an architecture that decouples persistent state maintenance from semantic reasoning, thereby transforming the VLM into a verifiable planning component. 

Our experiments support the efficacy of this architectural separation. The DEWM framework, through its dual geometric ( _S_ ) and semantic ( _G_ ) grounding, ensures persistent state tracking across stations; ablation studies confirm that removing either component consistently fails. Furthermore, by structuring VLM outputs into Externalizable Reasoning Traces (ERT), the system enables preexecution validation against physical consistency, effectively converting opaque decisions into auditable transactions. This structural transparency also facilitates interaction-phase tracking ( _CS_ ), which proved essential for targeted failure localization and informed recovery. Quantitatively, the approach significantly improved state-tracking accuracy and recovery success rates while reducing inference overhead compared to memory-augmented VLM baselines. 

Beyond specific performance gains, this work highlights a broader design principle: the interface between foundation models and physical systems should be structured, verifiable, and auditable. The ERT protocol instantiates this by exposing VLM reasoning to external validation, a strategy likely to be critical for deploying foundation models in safety-critical industrial settings where accountability and traceability are required. 

29 

Future work will focus on relaxing the current assumptions of the framework. First, we aim to incorporate uncertainty explicitly by modeling pose covariance within the world model, enabling risk-aware planning. Second, we plan to extend the system to open-vocabulary scenarios, moving beyond the current semi-closed Shape Library to handle novel object categories dynamically. Finally, fusing force-torque and acoustic signals into the constraint state ( _CS_ ) offers a promising avenue for finer-grained diagnosis, allowing the system to distinguish between physically distinct failure modes such as slip and collision. 

In summary, VLM-DEWM provides a persistent, interpretable memory core that supports cross-station consistency and resilient recovery. This transition from reactive intelligence to deliberative autonomy offers a principled path for embodied agents to operate reliably in dynamic physical environments. 

# **CRediT authorship contribution statement** 

- **Guoqin Tang** : Conceptualization, Methodology, Validation, Formal analysis, Investigation, Writing–original draft, Software, Data curation, Visualization. 

- **Qingxuan Jia** : Resources, Project administration, Funding acquisition. 

- **Gang Chen** : Conceptualization, Investigation, Writing– review & editing, Funding acquisition. 

- **Tong Li** : Conceptualization, Investigation, Writing– review & editing, Funding acquisition. 

- **Zeyuan Huang** : Writing – review & editing, Validation, Formal analysis, Conceptualization. 

- **Zihang Lv** : Investigation, Validation. 

- **Ning Ji** : Investigation, Funding acquisition. 

# **Declaration of competing interest** 

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. 

# **Data availability** 

The authors do not have permission to share data. 

# **Acknowledgments** 

This work is supported by the National Natural Science Foundation of China under Grant No. 62573064; and State Key Laboratory of Robotics and Systems (HIT) (SKLRS-2025-KF-07). All authors have read and agreed to the published version of the manuscript. 

# **Appendix A. Implementation Details of the Symbolic Perception Interface** 

This appendix details the technical implementation of the symbolic perception pipeline described in Section 3.2. The objective is to transform raw RGB-D observations _Ot_ into a structured symbolic snapshot _Envt_ efficiently. 

30 

_Appendix A.1. Vocabulary-Guided 2D Attention Focusing_ 

To avoid computationally expensive dense reconstruction of irrelevant background, we leverage the VLM to filter the scene in the 2D domain first. 

_a. Task-Relevant Category Generation:_ 

Given the task description _T_ and RGB image _It_ , the VLM infers a list of relevant object categories _Ctask_ : 


_Example:_ For _T_ = "Fetch the drink", _Ctask →_ [’bottle’, ’can’, ’cup’, ’table’]. 

_b. Open-Vocabulary Segmentation:_ 

This list _Ctask_ serves as the text prompt for an open-vocabulary segmentation model (specifically, we use “Mask2Former” trained on cityscapes/COCO). The model outputs a set of binary masks _M_ : 


Pixels not belonging to _Ctask_ are masked out ( _null_ ), significantly reducing the data volume for downstream 3D processing. 

_Appendix A.2. Sparse 3D Lifting and Coordinate Transformation_ 

We establish a precise mapping from selected 2D pixels to the robot’s 3D workspace. 

_a. Depth Back-Projection:_ 

For a valid pixel ( _u, v_ ) with depth _d_ = _Dt_ ( _u, v_ ), we project it to the camera coordinate frame 

_pc_ : 


where **K** is the camera intrinsic matrix. 

_b. Kinematic Transformation:_ 

The point is then transformed to the robot base frame _pb_ using the kinematic chain: 


where<sup>_b_</sup> **T** _e_ is the end-effector pose (from forward kinematics) and<sup>_e_</sup> **T** _c_ is the hand-eye calibration matrix. 

_c. Ray-Casting Correspondence:_ 

To robustly associate semantic masks with noisy depth data, we employ a ray-casting check. A ray **r** ( _t_ ) originating from the optical center passes through pixel ( _u, v_ ) into the point cloud _Pb_ . A point _p ∈ Pb_ is assigned the label of pixel ( _u, v_ ) if and only if it lies within a distance threshold _ϵ_ of the ray: 


31 

_Appendix A.3. Distance-Aware Multi-Resolution Quantization_ 

We partition the workspace into concentric zones based on the robot’s physical reach capabilities. 

- _a. Threshold Definition:_ 

   - _rnear_ (e.g., 0.8m): The maximum reach of the robotic arm without base movement. 

   - _rfar_ (e.g., 2.0m): The trusted sensing range for reliable object identification. 

- _b. Quantization Logic:_ 

Based on the centroid distance _di_ = _∥p_ ¯ _i∥_ , the object’s geometry _geomi_ is constructed as: 

- **Near Zone (** _di < rnear_ **):** We retain the raw point cloud _PCi_ . This supports high-fidelity ICP registration for grasping. 

- **Mid Zone (** _rnear ≤ di < rfar_ **):** We discretize points into a Voxel Grid _Vi_ (voxel size = 2cm). This preserves topology while compressing data for collision checking. 

- **Far Zone (** _di ≥ rfar_ **):** We abstract the object as a “Directed Billboard” _Bi_ = _⟨Icrop,⃗vview,_ **p** _cen⟩_ , where _Icrop_ is the RGB crop, _⃗vview_ is the viewing vector, and **p** _cen_ is the centroid. This acts as a visual proxy for situational awareness with minimal memory cost. 

_Appendix A.4. Final Symbolic Object Encapsulation_ 

Finally, we aggregate the fragmented mappings into coherent object instances. For each unique instance ID detected in the mask set, we gather its geometric primitives and query the VLM for a descriptive summary. The final observation snapshot _Envt_ is a set of tuples, where each object _obji_<sup>_t_isdefinedas:</sup> 


- id _i_ : Unique instance identifier (e.g., "blue_block_1"). 

- label _i_ : Semantic category from VLM (e.g., "block"). 

- _geom_<sup>_t_</sup> _i_<sup>:TheheterogeneousgeometricrepresentationderivedinAppendixA.3.</sup> 

- desc _i_ : A VLM-generated attribute description (e.g., "A metallic cube, possibly heavy"). 

_Appendix A.5. Perception Pipeline Triggering Policy_ 

The perception-to-memory pipeline (Section 3.2) does not run at a fixed frame rate. Instead, we employ an event-driven triggering policy to balance computational cost and state freshness. 

_Appendix A.5.1. Trigger Events_ 

The full perception pipeline is invoked upon: 

1. **Action Boundary:** Before and after each skill execution (e.g., pre-grasp, post-place). 

2. **Zone Transition:** When the robot enters a new _Gzone_ region. 

3. **Anomaly Detection:** When F/T feedback or motion tracking indicates unexpected events. 

4. **Explicit Query:** When the VLM requests updated state for a specific object. 

5. **Timeout:** If no trigger occurs for _Tmax_ = 10 seconds (background refresh). 

32 

_Appendix A.5.2. Handling Drift During Non-Observation Periods_ 

Between perception events, object states in _Sobj_ are **not updated** . We address potential drift through: 

_a. Conservative Covariance Inflation:_ 

For each object _oi_ not observed in the current cycle, we inflate its position uncertainty by a fixed process noise: 


where **Q** _drift_ = diag(0 _._ 001 _,_ 0 _._ 001 _,_ 0 _._ 001) m<sup>2</sup> represents per-cycle drift uncertainty (approximately 3 cm standard deviation per axis). This accumulation signals to the planner that unobserved objects have increased positional uncertainty. 

_b. Pre-Action Verification:_ 

Before any manipulation action targeting object _oi_ , the system _mandatorily_ triggers a perception update for _oi_ , regardless of recency. This ensures no action is executed based on stale beliefs. 

_c. Static Object Assumption:_ 

For objects tagged as “static” in _G_ (e.g., fixtures, tables), we assume zero drift and skip reobservation unless explicitly invalidated. 

_Appendix A.5.3. Complexity Implications_ 

The event-driven policy means the per-cycle costs in Appendix E are **amortized** , not perframe. In our experiments: 

- Task 1 (Assembly): _∼_ 15 perception events over _∼_ 120 seconds ( _≈_ 0 _._ 125 Hz effective rate) 

- Task 2 (Exploration): _∼_ 240 perception events over _∼_ 600 seconds ( _≈_ 0 _._ 4 Hz effective rate) 

- Task 3 (Recovery): Variable, with bursts during failure diagnosis 

This is significantly lower than continuous SLAM-style updates, validating the efficiency claims. 

# **Appendix B. Algorithmic Details for DEWM Dynamics and Maintenance** 

This appendix provides the specific hyperparameters, noise models, and prompt templates required to reproduce the DEWM dynamics. 

_Appendix B.1. Data Association and Similarity Scoring_ 

This section specifies the association cost, gating rules, and VLM prompt templates used to match observations _ok ∈ Envt_ to memory entries _si ∈Sobj_ in the Hungarian assignment. 

_Appendix B.1.1. Association Cost and Weights_ 

We construct a hybrid cost matrix: 


Unless otherwise stated, we set ( _λiou, λsem_ ) = (0 _._ 7 _,_ 0 _._ 3), prioritizing geometric consistency while allowing semantic cues to resolve visually similar instances. 

33 

_Appendix B.1.2. IoU Definition (3D/2D Fallback)_ 

For each observation–memory pair, we compute IoU over _3D oriented bounding volumes_ when depth is reliable. If depth is unreliable (e.g., reflective surfaces or missing depth), we fall back to 2D mask IoU in the image plane using the most recent view: 


where _B_ denotes an oriented bounding volume and _M_ denotes a 2D segmentation mask. 

_Appendix B.1.3. Semantic Similarity Prompt and Parsing_ 

The semantic similarity sim( _ok, si_ ) _∈_ [0 _,_ 1] is queried from the VLM when geometric cues alone are ambiguous (e.g., multiple nearby candidates or visually similar parts). The inputs `{loc}` are 3D Euclidean coordinates relative to the robot base, and `{feat}` are short attribute strings extracted from perception. 

Prompt Template: Semantic Similarity 

**System:** You are a spatial reasoning assistant. 

**Context:** An object described as a ‘{category_i}’ was last seen at {loc_old} with features {feat_i}. A new object is perceived at {loc_new} with features {feat_new}. **Query:** Is this the same object instance? Analyze the spatial offset and feature consistency. Answer with a single confidence score between 0.0 and 1.0. 

We use greedy decoding with temperature 0 and parse the first numeric token in the VLM output as sim( _ok, si_ ). If parsing fails, we set sim = 0 as a conservative default. We use _τsim_ = 0 _._ 5 as the neutral decision boundary. 

_Appendix B.1.4. Hungarian Assignment and Match Gating_ 

Given _Cki_ , we solve a one-to-one assignment using the Hungarian algorithm. A proposed match ( _ok, si_ ) is accepted only if it passes a match-quality gate: 


Unless otherwise stated, we set _τmatch_ = 0 _._ 55. This gate rejects low-confidence matches and prevents identity switches in cluttered scenes. 

_Appendix B.1.5. Confirmation Window for Unmatched Observations_ 

If _ok_ is not matched to any active entry (or all candidate matches violate _τmatch_ ), it enters a confirmation window and is tracked tentatively for _nconfirm_ consecutive observations before being promoted to a new active entity. We set _nconfirm_ = 2 by default. Tentative tracks that are not re-observed within the window are discarded, suppressing one-off false detections and preventing ghost artifacts. 

_Appendix B.2. Adaptive Fusion and VLM Gain Modulation_ 

This section provides the implementation details for the VLM-modulated Gaussian envelope fusion described in Section 3.2.3. 

34 

_Appendix B.2.1. Quantifying Observation Uncertainty (_ **Σ** _obs)_ 

The observation covariance **Σ** _obs_ in Equations (7)–(8) is computed based on the geometric abstraction available at time _t_ : 


where _N_ is the point count and _ϵ_ = 10<sup>_−_6</sup> m<sup>2</sup> prevents singularities. 


with default ( _σx, σy, σz_ ) = (0 _._ 01 _,_ 0 _._ 01 _,_ 0 _._ 02) meters. 

_Appendix B.2.2. Gain Mapping Table_ 

Table B.7 specifies the numerical mapping _γ_ ( _αt_ ) used in all experiments. 

Table B.7: Mapping from VLM Reliability Judgment to Fusion Weight 

|**VLM Judgment** (_αt_)|**Weight** (_γ_)|**Effect**|
|---|---|---|
|High|1.0|Full observation contribution|
|Medium|0.5|Balanced fusion|
|Low|0.1|Conservative update|
|Bad|0.01|Near-freeze at prior|


_Appendix B.2.3. Prompt Template for Reliability Assessment_ 

We use greedy decoding ( _T_ = 0) and parse the first matching token. 

Prompt: Observation Reliability Assessment 

**Context:** You are assessing the reliability of a sensor observation. **Object:** {object_category} at position {position} **Observation Conditions:** 

- Occlusion level: {occlusion_percentage}% 

- - Lighting: {lighting_quality} - Object material: {material_type} - Depth confidence: {depth_confidence} **Task:** Rate the observation reliability as one of: High, Medium, Low, or Bad. Respond with only one word. 

35 

_Appendix B.3. Scale-Aware Robust ICP Solver Details_ 

To handle scale discrepancies (e.g., between canonical CAD models and real-world instances) and sensor noise, we solve the joint optimization problem: 


where _pi ∈P_<sup>_∗_</sup> are source model points and _qi_ are corresponding target points. 

_a. Robust Cost Function:_ 

We use the Huber loss _ρδ_ ( _·_ ) to mitigate the effect of outliers (e.g., segmentation artifacts): 


We adaptively set _δ_ = 2 _._ 5 _·_ median( _r_ ) at each iteration. 

_b. Closed-Form Update Steps:_ 

While the joint optimization is non-convex, we decouple it into two convex sub-problems solved iteratively.At each iteration, we compute weights from the Huber loss: 


where _ρ_<sup>_′_</sup> _δ_<sup>isthederivativeoftheHuberfunction(</sup><sup>_ρ′_</sup> _δ_<sup>(</sup><sup>_r_) = min(1</sup><sup>_, δ/|r|_)</sup><sup>_·_sign(</sup><sup>_r_)).</sup> 


Check: If det( **R** ) _<_ 0, we correct **V** by multiplying its last column by -1 to ensure a valid rotation. 

- **Scale Update (** _s_ **):** With **R** _,_ **t** fixed, the optimal scale is analytically derived: 


_Appendix B.4. Background Map Maintenance Implementation_ 

The background model _Sbg_ employs a hybrid volumetric-visual representation. 

_a. Probabilistic Volumetric Fusion:_ 

For voxel occupancy _O_ ( _n_ ), we use the standard log-odds notation _L_ ( _n_ ) = log 1 _−PP_ <u>(</u> _O_ ( _O_ <u>(</u> _n_ ()) _n_ ))<sup>.The</sup> update rule for measurement _zt_ is: 


where _lmin_ = _−_ 2 _, lmax_ = 3 _._ 5 prevent over-confidence. 

36 

Simultaneously, we maintain a semantic distribution _P_ ( _Ck|z_ 1: _t_ ) over classes _Ck ∈{_ wall, table, floor, ... _}_ using a recursive Bayesian update: 


where _η_ = (<sup>�</sup> _k_<sup>_′ P_(</sup><sup>_zt|Ck′_)</sup><sup>_P_(</sup><sup>_Ck′|z_1:</sup><sup>_t−_1))</sup><sup>_−_1ensuresnormalization.</sup> 

_b. Directed Billboard Management:_ 

For ray endpoints exceeding _rfar_ , we generate a visual proxy. 

- **Storage:** A billboard _Bk_ = _⟨Icrop,⃗vview,_ **p** _cen⟩_ stores the RGB appearance _Icrop_ and the viewing direction _⃗vcam_ . 

- **Retrieval Metric:** When the planner queries a frontier direction _⃗vquery_ , we retrieve the most relevant billboard _k_<sup>_∗_</sup> maximizing cosine similarity: 


This simple metric effectively handles the view-dependent nature of open boundaries (e.g., looking "out" a window vs. looking "at" a wall). 

# _Appendix B.5. Statistical Basis for Geometric Verification_ 

The verification module treats relation proposals as statistical hypothesis tests. We assume the position estimates of objects follow multivariate normal distributions _N_ ( **_µ_** _,_ **Σ** ). 

_a. Containment Test (A ⊃ B):_ 

The condition verifies if the bulk of _B_ ’s probability mass lies within the high-likelihood region of _A_ . We compute the Mahalanobis distance of _B_ ’s centroid relative to _A_ ’s distribution: 


Note that only **Σ** _A_ is used in the metric because the constraint is defined by the boundary of _A_ . _b. Contact Test (A touches B):_ 

This tests the hypothesis that the two distributions overlap significantly. The uncertainty of the relative difference vector ∆ **x** = **x** _B −_ **x** _A_ is given by the convolution of variances (sum of covariance matrices): 


_c. Threshold Selection (χ_<sup>2</sup> _thresh_<sup>_):_</sup> 

The squared Mahalanobis distance follows a Chi-square distribution with _k_ degrees of freedom. Since we evaluate spatial relations in 3D translational space ( _x, y, z_ ), we set _k_ = 3. For a strict 95% confidence level (i.e., we are 95% sure the relation holds), we consult the _χ_<sup>2</sup> table: 


Any relation with a distance score _D_<sup>2</sup> _>_ 7 _._ 815 is rejected as a statistical anomaly or noise. 

37 

_Appendix B.6. Long-Term Memory Lifecycle Management_ 

To ensure robustness in long-horizon operations, the “Memory Curation” is not merely a deletion process but a full Entity Lifecycle Management system. We define three states for every memory entity: `Active` , `Uncertain` , and `Archived` . 

# _a. State Transitions and Decay Dynamics:_ 

When the robot performs a perception scan in Zone _Zk_ , the confidence _ct_ of an unobserved entity _vi_ follows an exponential decay model, representing the increasing probability that the object has been moved or removed: 


Entities transition states based on thresholds: 

- **Active** _→_ **Uncertain:** When _ct < τuncertain_ (set to 0.6). The planner adds a "Verify" sub-task before interacting. 

- **Uncertain** _→_ **Archived:** When _ct < τarchive_ (set to 0.1). The entity is removed from the spatial index tree (KD-Tree) to optimize query speed but retained in cold storage (Disk). 

# _b. Restoration of Archived Entities (The "Zombie" Problem):_ 

A critical feature is the ability to recover from false negatives. If a new observation _onew_ appears but fails to match any `Active` entity, the system queries the `Archived` database. If a match is found (using the logic in B.1), the entity is restored to `Active` state with _ct_ reset to 1.0, preserving its historical semantic attributes (e.g., "fragile"). 

# _c. Curation Algorithm:_ 

The complete lifecycle maintenance logic is detailed in Algorithm 3. 

**Parameter Rationale:** We select _λdecay_ = 0 _._ 95. This implies a "half-life" of approx 13 scans. The archiving threshold _τarchive_ = 0 _._ 1 requires _≈_ 45 consecutive misses, providing a robust buffer against transient occlusions common in collaborative construction. 

# _Appendix B.7. Force-Torque Feedback Integration_ 

While VLM-DEWM focuses on cognitive-level planning (not low-level impedance control), the system interfaces with the robot controller’s force-torque (F/T) signals to trigger state transitions in the _CS_ module. This section specifies the integration protocol. 

# _a. Scope Clarification_ 

We do _not_ design force control laws. Instead, we treat F/T readings as **binary event triggers** that signal the success or failure of contact-rich actions to the cognitive layer. The underlying impedance/admittance control is handled by the robot’s native controller (Franka Control Interface in our experiments). 

- _b. Threshold-Based Event Detection_ 

For each contact-rich action type, we define conservative thresholds based on the Franka Emika Panda’s specifications and empirical tuning: 

# _c. Mapping to CS State Transitions_ 

The F/T events are mapped to _CS_ updates as follows: 

- **Grasp Failure** ( _Fg <_ 5N after gripper close command): _CS_ remains at _⟨_ `Idle` _,_ `NULL` _⟩_ ; ERT’s _Acausal_ is invalidated. 

38 

**Algorithm 3** Entity Lifecycle Maintenance **Require:** DEWM Ω, Current Zone _Zk_ , Observed IDs _Ok_ 1: _Kk ←_ Ω _._ GetEntitiesInZone( _Zk_ ) 2: _Uk ←Kk \ Ok ▷_ Unobserved entities 3: _// Phase 1: Decay and Archive_ 4: **for** _id_ in _Uk_ **do** 5: _v ←_ Ω _._ GetEntity( _id_ ) 6: _v.confidence ← v.confidence × λdecay_ 7: **if** _v.confidence < τarchive_ **then** 8: Ω _._ ArchiveEntity( _id_ ) _▷_ Move to cold storage 9: **else if** _v.confidence < τuncertain_ **then** 10: _v.state ←_ `Uncertain` 11: **end if** 12: **end for** 13: _// Phase 2: Reinforcement and Restoration_ 14: **for** _id_ in _Ok_ **do** 15: **if** _id ∈_ Ω _._ Archived **then** 16: Ω _._ RestoreEntity( _id_ ) _▷_ Restoration Event 17: **end if** 18: _v ←_ Ω _._ GetEntity( _id_ ) 19: _v.confidence ←_ 1 _._ 0 20: _v.state ←_ `Active` 21: **end for** 

- **Collision Detected** ( _|Fext| >_ 15N during transport): Motion halts; _CS_ transitions to _⟨_ `Interrupted` _,_ last_target _⟩_ ; triggers re-perception. 

- **Contact Confirmed** ( _Fz >_ 10N sustained for 0.5s during place): _CS_ transitions from _⟨_ `Placing` _,_ obj _⟩_ to _⟨_ `Idle` _,_ `NULL` _⟩_ ; placement success logged. 

# _d. Implementation Note_ 

These thresholds are **fixed** in our experiments, calibrated once for the Franka+Robotiq platform. For deployment on different hardware, re-calibration is required. Adaptive thresholding based on object properties (e.g., fragile objects use lower _Fg_ limits) is a direction for future work (Section 4.4.2). 

# **Appendix C. Implementation Details of Dynamic Context Engineering** 

This appendix details the subgraph extraction algorithm and prompt synthesis logic for the context engineering pipeline described in Section 3.3.2. 

# _Appendix C.1. Task-Relevant Subgraph Extraction Algorithm_ 

The “Information Bottleneck” principle in Section 3.3.2 is operationalized through a **two-stage filtering** algorithm, not learned compression. We prioritize interpretability and determinism over optimality. 

39 

Table B.8: Force-Torque Thresholds for State Transition Triggers 

|**Action**|**Signal**|**Threshold**|**Triggered Event**|
|---|---|---|---|
|Grasp|Gripper Force _Fg_|_<_5 N (after close)|Grasp Failure|
|Grasp|Gripper Force _Fg_|_>_40 N|Over-squeeze (abort)|
|Transport|End-effector _|Fext|_|_>_15 N|Collision Detected|
|Place|End-effector _Fz_|_>_10 N (sustained)|Contact Confirmed|
|Insert|End-effector _|τext|_|_>_2 Nm|Jamming Detected|


_Appendix C.1.1. Stage 1: Zone-Based Spatial Filtering_ 

Given the current subtask _sst_ and robot state _CSt_ , we first identify the **relevant zones** : 


This exploits the hierarchical structure of _G_ to immediately prune objects in distant, task-irrelevant areas. 

_Example:_ For _sst_ = “Pick red_block from Zone_A”, we have _Zrelevant_ = _{_ Zone_A _}_ , ignoring all objects in Zone_B, Zone_C, etc. 

_Appendix C.1.2. Stage 2: Task-Driven Relevance Scoring_ 

Within _Zrelevant_ , we compute a relevance score for each vertex _vi ∈Gobj_ : 


where: 


_Appendix C.1.3. Subgraph Construction_ 

The extracted subgraph _Gsub_ is formed by selecting vertices that exceed a relevance threshold: 


We set _τrel_ = 0 _._ 3 empirically. This value was chosen to effectively prune irrelevant background objects (typically _r <_ 0 _._ 2) while retaining indirect dependencies (e.g., support surfaces with _r ≈_ 0 _._ 5). This filtering typically yields _|Vsub| ≈_ 3–8 vertices for standard manipulation tasks. 

40 

_Appendix C.1.4. Algorithm Pseudocode_ 

**Algorithm 4** Task-Relevant Subgraph Extraction 

**Require:** _G_ , _sst_ , _CSt_ , threshold _τrel_ **Ensure:** _Gsub_ = ( _Vsub, Esub_ ) 1: _Zrel ←_ GetRelevantZones( _sst, CSt_ ) 2: _Vcandidates ←{v ∈Gobj | v._ zone _∈Zrel}_ 3: _Vsub ←∅_ 4: **for** _vi ∈ Vcandidates_ **do** 5: _ri ←_ ComputeRelevance( _vi, sst_ ) 6: **if** _ri > τrel_ **then** 7: _Vsub ← Vsub ∪{vi}_ 8: **end if** 9: **end for** 10: _Esub ←{_ ( _vi, vj_ ) _∈E | vi, vj ∈ Vsub}_ 11: **return** ( _Vsub, Esub_ ) 

_▷_ Eq. above 

_Appendix C.1.5. Clarification on “Information Bottleneck”_ 

We use the Information Bottleneck (IB) principle as a **conceptual motivation** , not a learned objective. Our rule-based extraction approximates the IB goal of minimizing _I_ ( _Z_ ; Ω) (irrelevant info) while maximizing _I_ ( _Z_ ; _Y_ ) (task-relevant info) through: 

- Zone filtering _≈_ spatial compression 

- Relevance scoring _≈_ task-conditional selection 

A learned IB encoder (e.g., via variational methods) is left for future work. 

_Appendix C.2. Initialization and Task Decomposition Context_ 

**Objective:** To decompose a high-level user command into a structured Directed Acyclic Graph (DAG) of sub-tasks. 

_a. Data Extraction:_ 

The system scans the initial environment Ω0 and compiles a list of available entities: _Lres_ = _{_ ( _idi, cati,_ **p** _i_ ) _}_ . 

_b. Prompt Template:_ 

41 

Prompt: Task Decomposition 

**Role:** Expert Robotic Planner. **User Command:** "{T}" **Available Resources:** 

- {resource_list} 

**Objective:** Decompose the command into a sequence of sub-tasks. Output a JSON object representing a DAG, where each node contains: "id", "function" (e.g., pick, place), "args", and "dependencies". 

**Example Output:** { "nodes": [ { "id": 1, "function": "pick", "args": ["blue_block_1"], "dependencies": [] } ] } 

_Appendix C.3. Coarse Motion Planning Context_ 

**Objective:** To generate collision-free waypoints for macro-navigation. 

_a. Data Extraction:_ 

We cluster the background map _Sbg_ (e.g., using DBSCAN) to extract obstacle bounding boxes _Olist_ . 

_b. Prompt Template:_ 

Prompt: Coarse Path Planning **Current Goal:** "{SS_t.description}" **Robot State:** {CS_t} **Constraints:** - Obstacles (BBoxes): {obstacle_list} - Semantic Constraints: {relevant_relations_from_G} **Task:** Generate a list of SE(3) waypoints for the end-effector to reach the target area while avoiding obstacles. 

# _Appendix C.4. Fine-Grained Manipulation Context_ 

**Objective:** To generate precise delta-pose adjustments for contact-rich interaction. 

_a. Data Extraction:_ 

We query high-fidelity data sources: Shape Prior _L_ , Force-Torque sensors _Ft_ , and precise object pose **T** _obj_ . 

_b. Prompt Template:_ 

42 

Prompt: Fine Manipulation 

**Target Object:** {target.id} ({target.category}) 

- Pose (SE3): {target.pose} 

- Envelope ( _µ,_ Σ): {target.envelope} 

- Shape Prior: {shape_desc} 

- Force Readings: {force_torque_data} 

**Task:** Based on the geometry and force feedback, compute the next optimal delta-pose (∆ **T** ) for the end-effector. Return a JSON with "action_type" and "value". 

# _Appendix C.5. Failure Diagnosis and Recovery Context_ 

**Objective:** To analyze execution failures and propose a recovery plan. 

- _a. Data Extraction:_ 

We compile the Action Sequence History _Hash_ and the post-failure world state Ω _fail_ . 

- _b. Prompt Template:_ 

Prompt: Failure Diagnosis 

# **CRITICAL FAILURE REPORT** 

**1. Failed Action:** "{failed_SS_t.description}" 

**2. Context:** 

- State Before: {CS_t_before} 

- Action Log: {recent_action_log} 

- **3. Post-Mortem:** 

- Error Code: {failure_reason} 

- Current World State: {summary_of_S_and_G} 

- **Task:** 

1. Diagnose the root cause of the failure. 

2. Propose a new TTP (DAG JSON) to recover and achieve the original goal. 

# _Appendix C.6. Formal Definition of Semantic Discrepancy Operator (⊖)_ 

The semantic discrepancy ∆= Ω _t_ +1 _⊖Acausal_ in Section 3.3.5 is computed via a **rule-based state comparison** , not probabilistic VLM inference. This ensures deterministic and auditable diagnosis. 

# _a. Definition_ 

Given the expected post-state _Acausal_ = _⟨CSexp, Rexp⟩_ (where _CSexp_ is the expected constraint state and _Rexp_ is a set of expected relation changes) and the actual observed state Ω _t_ +1, we define: 


# _b. Component-wise Computation:_ 

**b.1. Constraint State Discrepancy (** ∆ _CS_ **):** A direct symbolic comparison between expected and actual micro-topological states: 


43 

_Example:_ If _CSexp_ = _⟨_ `Holding` _,_ obj_1 _⟩_ but _CSt_ +1 = _⟨_ `Idle` _,_ `NULL` _⟩_ , then ∆ _CS_ = ( `Holding` _→_ `Idle` ), indicating a grasp failure. 

**b.2. Semantic Graph Discrepancy (** ∆ _G_ **):** We perform a structural graph difference on the object-level semantic graph: 


where _E_ denotes the edge set of _Gobj_ . This is implemented as a deterministic set operation on relation tuples. 

_Example:_ If the action was `Place(A, B)` with _Rexp_ = _{_ + `On` ( _A, B_ ) _}_ , but post-observation shows `On` ( _A,_ `floor` ), then: 


• ∆<sup>+</sup> _G_<sup>=</sup><sup>_{_</sup><sup>`On`(</sup><sup>_A,_</sup><sup>`floor`)</sup><sup>_}_(unexpectededgepresent)</sup> 

**b.3. Geometric Discrepancy (** ∆ _S_ **):** For objects involved in the action, we compute the 

pose deviation: 


A significant deviation ( _> τgeo_  drift_ , default 0.05m) flags potential unmodeled disturbances. 

_c. Discrepancy Report Generation:_ 

The structured ∆ is serialized into natural language for VLM-based recovery planning: 

# Discrepancy Report Template 

# **DISCREPANCY DETECTED** 

- CS Mismatch: Expected { _CSexp_ }, Actual { _CSt_ +1} 

- - Missing Relations: {∆<sup>_−_</sup> _G_<sup>}</sup> - Unexpected Relations: {∆<sup>+</sup> _G_<sup>}</sup> 

- Geometric Drift: {object: drift_distance} 

**Likely Cause:** [Inferred from ∆ _CS_ pattern, see Table C.9] 

# _d. Diagnosis Rule Table:_ 

The ∆ _CS_ pattern deterministically maps to failure categories: 

Table C.9: Rule-Based Failure Diagnosis from ∆ _CS_ 

|_CSexp_|_CSt_+1|**Diagnosed Failure**|
|---|---|---|
|Holding(X)|Idle|Grasp Slip / Gripper Failure|
|Holding(X)|Holding(Y)|Object Misidentification|
|Approaching(X)|Idle|Motion Interrupted / Collision|
|Placing(X, Y)|Holding(X)|Placement Rejected / Unstable|


This rule-based approach ensures that the _⊖_ operator produces **deterministic, explainable** discrepancy reports, while the subsequent VLM call (Appendix C.5) is responsible only for **recovery strategy synthesis** —not diagnosis itself. 

44 

# **Appendix D. Implementation Details of the ERT Validation Protocol** 

This appendix details the schema and verification logic for the External Reasoning Trace (ERT) described in Section 3.3.3. 

# _Appendix D.1. ERT Schema Definition_ 

The VLM output must strictly adhere to the schema defined in Table D.10. 

Table D.10: Schema Definition for External Reasoning Trace (ERT) 

|**Field**|**Type**|**Description & Example**|
|---|---|---|
|`action_proposal`|String|The proposed skill call.|
|||_Ex: "Grasp(blue_block_1)"_|
|`world_belief`|Object|Structured assertion about state.|
|||_Ex: {"pred": "On", "args": ["A", "B"]}_|
|`causal_assump`|String|Expected outcome.|
|||_Ex: "CS becomes Holding(A)"_|
|`confidence`|Float|Self-evaluated score [0.0, 1.0].|
|`fallback`|String|Contingency plan.|


_Appendix D.2. Multi-Layered Validation Logic_ 

The `GetValidERT()` function enforces a three-stage check: 

# _a. Syntactic Validation:_ 

We use a JSON schema validator to ensure the output contains all required fields (Table D.10) and that data types are correct (e.g., 0 _._ 0 _≤_ `confidence` _≤_ 1 _._ 0). 

# _b. Semantic Validation:_ 

We extract all entity IDs from `action_proposal` and `world_belief` . The validator queries the DEWM to ensure existence: 


This prevents hallucinations of non-existent objects. 

_c. Physical Consistency Validation:_ 

We verify the `world_belief` against the geometric ground truth _S_ . 

- **Verify On(A, B):** 

   1. _Support:_ Check if _A_ ’s centroid **_µ_** _A_ projected onto the XY plane lies within _B_ ’s XYenvelope. 

   2. _Contact:_ Check if the vertical gap is minimal: _|Zmin_ ( _A_ ) _− Zmax_ ( _B_ ) _| < ϵcontact_ . 

- **Verify Inside(A, B):** Check if _A_ ’s bounding box is fully contained within _B_ ’s boundaries: 


- **Verify Near(A, B):** Check Euclidean distance: _∥_ **_µ_** _A −_ **_µ_** _B∥ < dnear_ . 

45 

_Appendix D.3. System Briefing (Meta-Instruction)_ 

To ensure the VLM utilizes the DEWM correctly, the following system prompt is injected at the start of every session: 

# System Briefing 

# **SYSTEM INSTRUCTION:** 

You are interacting with the **VLM-DEWM** system. This system maintains a persistent World Model with the following queryable modules: 

1. **Semantic Graph (G):** Tracks entity IDs, states (e.g., "OnTable"), and relations. 

2. **Spatial Network (S):** Maintains precise poses and geometry (Point Clouds/Voxels). 

3. **Task Memory (M):** Tracks current sub-task and dependency graph (TTP). 

4. **Robot State (CS):** Tracks interaction status (e.g., "Holding X"). 

**RULE:** Do not hallucinate state. Do not re-infer facts from raw images if they are already provided in the context. Treat the provided DEWM data as the Single Source of Truth. 

# **Appendix E. Computational Complexity Analysis** 

This appendix analyzes the computational complexity of the VLM-DEWM framework. The overall cost comprises three main components: (1) perception and world model update, (2) dynamic context engineering, and (3) VLM inference and validation. We assume the DEWM maintains _Nobj_ object instances, and each perception snapshot _Envt_ observes _Nobs_ objects. 

_Appendix E.1. Per-Cycle Update Cost_ 

This is the foundational cost incurred in each cognitive cycle. 

- _a. Symbolic Perception Interface_ 

The VLM-driven semantic focusing requires one VLM call. Geometric processing (point cloud segmentation, projection, voxelization) scales as _O_ ( _Npoints_ ) with the input point cloud size. Due to task-driven focusing, the actual processed point cloud is significantly smaller than the full scene. _b. Data Association_ 

This is one of the main bottlenecks in the update process. 

   - **Geometric Candidate Screening:** A naive implementation comparing _Nobs_ observations against _Nobj_ memory entries has complexity _O_ ( _Nobs · Nobj_ ). In our implementation, by leveraging the Hierarchical Semantic Graph (HSG) for spatial indexing (first matching to Zone) and octree-based nearest neighbor search on the Spatial Network _S_ , the average complexity is reduced to _O_ ( _Nobs_ log _Nobj_ ). 

   - **VLM Semantic Adjudication:** For each observation, we select from _k_ geometric candidates (typically _k ≪ Nobj_ ), requiring _Nobs · k_ VLM scoring calls (optimizable via batching), or a single VLM call containing all candidates. 

- _c. Geometric Layer Update (S-Update)_ 

For each successfully associated object (at most _Nobs_ ), the Gaussian envelope fusion (Equations 7–8) is _O_ (1). When high-precision pose estimation is required, the scale-aware ICP algorithm 

46 

has complexity _O_ ( _I · Np_ log _Np_ ), where _I_ is the number of iterations and _Np_ is the number of points in the object’s local point cloud. 

# _d. Semantic Layer Update (G-Update)_ 

VLM relation hypothesis generation requires one VLM call. The geometric verification step checks object-pair relations; in the worst case, this could involve _O_ ( _Nobj_<sup>2) pairs, but in practice, the</sup> VLM typically proposes only a constant number of the most relevant relation hypotheses. Each hypothesis verification (e.g., Mahalanobis distance computation) is _O_ (1). 

# _Appendix E.2. Context Engineering Cost_ 

The goal of this process is to extract task-relevant information from the DEWM. 

# _a. Subgraph Extraction_ 

Thanks to the hierarchical structure of HSG, we first perform _O_ (1) indexing to identify the relevant Zone nodes. This restricts the search space from the global graph size _|Vglobal|_ to the local zone size _|Vzone|_ (where _|Vzone| ≪|Vglobal|_ ). Consequently, the relevance scoring involves iterating only over _|Vzone|_ , while the text serialization complexity scales with the much smaller final subgraph size _O_ ( _|Vsub|_ + _|Esub|_ ). Since _|Vzone|_ is physically bounded (i.e., independent of the total facility scale), the overall context engineering overhead remains _O_ (1) relative to the global DEWM scale. 

# _Appendix E.3. VLM-Guided Planning Cost_ 

# _a. VLM Inference_ 

VLM inference is the highest-latency component of the entire framework. Its complexity depends on the model architecture (typically Transformer) and input/output lengths. We can approximate it as _f_ ( _Lprompt, Lgen_ ), where _Lprompt_ is the token length of the context and prompt, and _Lgen_ is the token length of the generated ERT. A core objective of dynamic context engineering is to minimize _Lprompt_ . 

# _b. ERT Validation_ 

- **Syntactic Validation:** JSON schema validation scales linearly with ERT length, _O_ ( _Lgen_ ). 

- **Semantic Validation:** Checking whether entities in the ERT exist in _G_ . If _G_ ’s vertices are stored using a hash table, each lookup has average complexity _O_ (1). 

- **Physical Consistency Validation:** Checking _world_  belief_ against _S_ typically involves _O_ (1) geometric computations. 

# _Appendix E.4. Summary_ 

The main computational bottlenecks are **VLM inference latency** and **data association overhead in densely cluttered scenes** . Our architectural design, particularly the **Hierarchical Semantic Graph (HSG)** and **Dynamic Context Engineering** , aims to significantly prune the search space through spatial and task context, thereby effectively controlling the growth of data association cost and VLM context length. This enables the system to maintain high operational efficiency even when facing long-term, complex tasks. 

Table E.11 provides a summary of the complexity analysis. 

47 

Table E.11: Summary of Computational Complexity 

|**Component**|**Complexity**|
|---|---|
|Data Association (naive)|_O_(_Nobs · Nobj_)|
|Data Association (with HSG)|_O_(_Nobs_log_Nobj_)|
|Gaussian Envelope Fusion<br>|_O_(1) per object<br><br>_Note: |Vzone| denotes the number of entities in the_|
|Scale-aware ICP|_O_(_I · Np_log_Np_)|
|Subgraph Extraction|_O_(_|Vzone|_)<br>|
|ERT Semantic Validation|_O_(1) per entity|
|VLM Inference|_f_(_Lprompt, Lgen_)|


_relevant topological zone, which is physically bounded._ 

# **References** 

- [1] L. Ren, J. Dong, S. Liu, L. Zhang, L. Wang, Embodied intelligence toward future smart manufacturing in the era of ai foundation model, IEEE/ASME Transactions on Mechatronics (2024) 1–11doi:10.1109/TMECH.2024.3456250. 

- [2] P. Chen, X. Sun, H. Zhi, R. Zeng, T. H. Li, G. Liu, M. Tan, C. Gan, _a_<sup>2</sup> nav: Action-aware zeroshot robot navigation by exploiting vision-and-language ability of foundation models (2023). arXiv:2308.07997. URL `https://arxiv.org/abs/2308.07997` 

- [3] H. Fang, M. Grotz, W. Pumacay, Y. R. Wang, D. Fox, R. Krishna, J. Duan, Sam2act: Integrating visual foundation model with a memory architecture for robotic manipulation (2025). arXiv:2501.18564. 

   - URL `https://arxiv.org/abs/2501.18564` 

- [4] S. Belkhale, T. Ding, T. Xiao, P. Sermanet, Q. Vuong, J. Tompson, Y. Chebotar, D. Dwibedi, D. Sadigh, Rt-h: Action hierarchies using language (2024). arXiv:2403.01823. URL `https://arxiv.org/abs/2403.01823` 

- [5] D. Driess, F. Xia, M. S. M. Sajjadi, C. Lynch, A. Chowdhery, B. Ichter, A. Wahid, J. Tompson, Q. Vuong, T. Yu, W. Huang, Y. Chebotar, P. Sermanet, D. Duckworth, S. Levine, V. Vanhoucke, K. Hausman, M. Toussaint, K. Greff, A. Zeng, I. Mordatch, P. Florence, Palm-e: An embodied multimodal language model (2023). arXiv:2303.03378. URL `https://arxiv.org/abs/2303.03378` 

- [6] X. C. ..., Pali-x: On scaling up a multilingual vision and language model (2023). arXiv:2305.18565. URL `https://arxiv.org/abs/2305.18565` 

- [7] A. Brohan, N. Brown, J. Carbajal..., Rt-2: Vision-language-action models transfer web knowledge to robotic control (2023). arXiv:2307.15818. URL `https://arxiv.org/abs/2307.15818` 

- [8] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, C. Finn, Openvla: An open-source vision-language-action model (2024). 

48 

arXiv:2406.09246. 

URL `https://arxiv.org/abs/2406.09246` 

- [9] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, L. X. Shi, J. Tanner, Q. Vuong, A. Walling, H. Wang, U. Zhilinsky, _π_ 0: A visionlanguage-action flow model for general robot control (2024). arXiv:2410.24164. URL `https://arxiv.org/abs/2410.24164` 

- [10] S. Liu, L. Wu, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, J. Zhu, Rdt-1b: a diffusion foundation model for bimanual manipulation (2025). arXiv:2410.07864. URL `https://arxiv.org/abs/2410.07864` 

- [11] W. Huang, F. Xia, T. Xiao, H. Chan, J. Liang, P. Florence, A. Zeng, J. Tompson, I. Mordatch, Y. Chebotar, et al., Inner monologue: Embodied reasoning through planning with language models, arXiv preprint arXiv:2207.05608 (2022). 

- [12] I. Singh, V. Blukis, A. Mousavian, A. Goyal, D. Xu, J. Tremblay, D. Fox, J. Thomason, A. Garg, Progprompt: Generating situated robot task plans using large language models, in: 2023 IEEE International Conference on Robotics and Automation (ICRA), 2023, pp. 11523–11530. doi:10.1109/ICRA48891.2023.10161317. 

- [13] X. Liang, M. Tao, Y. Xia, J. Wang, K. Li, Y. Wang, Y. He, J. Yang, T. Shi, Y. Wang, M. Zhang, X. Wang, Sage: Self-evolving agents with reflective and memory-augmented abilities, Neurocomputing 647 (2025) 130470. doi:https://doi.org/10.1016/j.neucom.2025.130470. URL `https://www.sciencedirect.com/science/article/pii/S0925231225011427` 

- [14] Z. Shen, C. Diao, P. Vougiouklis, P. Merita, S. Piramanayagam, E. Chen, D. Graux, A. Melo, R. Lai, Z. Jiang, Z. Li, Y. Qi, Y. Ren, D. Tu, J. Z. Pan, GeAR: Graph-enhanced agent for retrieval-augmented generation, in: W. Che, J. Nabende, E. Shutova, M. T. Pilehvar (Eds.), Findings of the Association for Computational Linguistics: ACL 2025, Association for Computational Linguistics, Vienna, Austria, 2025, pp. 12049–12072. doi:10.18653/v1/2025.findingsacl.624. 

   - URL `https://aclanthology.org/2025.findings-acl.624/` 

- [15] S. Chen, Y. Liu, W. Han, W. Zhang, T. Liu, A survey on llm-based multi-agent system: Recent advances and new frontiers in application (2025). arXiv:2412.17481. URL `https://arxiv.org/abs/2412.17481` 

- [16] M. J. Alenjareghi, F. Ghorbani, S. Keivanpour, Y. A. Chinniah, S. Jocelyn, Proactive safety reasoning in human-robot collaboration in disassembly through llm-augmented stpa and fmea, Robotics and Computer-Integrated Manufacturing 98 (2026) 103162. doi:https://doi.org/10.1016/j.rcim.2025.103162. 

   - URL `https://www.sciencedirect.com/science/article/pii/S0736584525002169` 

- [17] L. Li, Y. Zhang, I. L. D. Makanda, P. Jiang, 3dprintmind: An ai-agent system using large language models and dynamic manufacturing knowledge graphs for smart manufacturing, Robotics and Computer-Integrated Manufacturing 99 (2026) 103214. doi:https://doi.org/10.1016/j.rcim.2025.103214. 

   - URL `https://www.sciencedirect.com/science/article/pii/S0736584525002686` 

49 

- [18] D. Li, Y. Liang, S. Qian, H. Wu, W. Jia, Y. Fu, Y. Sun, A review of background, methods, limitations and opportunities of knowledge graph completion, Computer Science Review 58 (2025) 100809. doi:https://doi.org/10.1016/j.cosrev.2025.100809. URL `https://www.sciencedirect.com/science/article/pii/S1574013725000851` 

- [19] S.-Q. Yan, J.-C. Gu, Y. Zhu, Z.-H. Ling, Corrective retrieval augmented generation (2024). arXiv:2401.15884. URL `https://arxiv.org/abs/2401.15884` 

- [20] L. Huang, H. Lan, Z. Sun, C. Shi, T. Bai, Emotional rag: Enhancing role-playing agents through emotional retrieval, in: 2024 IEEE International Conference on Knowledge Graph (ICKG), 2024, pp. 120–127. doi:10.1109/ICKG63256.2024.00023. 

- [21] A. Hornung, K. M. Wurm, M. Bennewitz, C. Stachniss, W. Burgard, Octomap: an efficient probabilistic 3d mapping framework based on octrees, Auton. Robots 34 (3) (2013) 189–206. doi:10.1007/s10514-012-9321-0. 

   - URL `https://doi.org/10.1007/s10514-012-9321-0` 

- [22] T. Chen, P. Culbertson, M. Schwager, Catnips: Collision avoidance through neural implicit probabilistic scenes, IEEE Transactions on Robotics 40 (2024) 2712–2728. doi:10.1109/TRO.2024.3386394. 

- [23] B. Wen, J. Tremblay, V. Blukis, S. Tyree, T. Müller, A. Evans, D. Fox, J. Kautz, S. Birchfield, Bundlesdf: Neural 6-dof tracking and 3d reconstruction of unknown objects, in: 2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2023, pp. 606–617. doi:10.1109/CVPR52729.2023.00066. 

- [24] M. Ji, R.-Z. Qiu, X. Zou, X. Wang, Graspsplats: Efficient manipulation with 3d feature splatting (2024). arXiv:2409.02084. URL `https://arxiv.org/abs/2409.02084` 

- [25] Z. Yan, S. Li, Z. Wang, L. Wu, H. Wang, J. Zhu, L. Chen, J. Liu, Dynamic open-vocabulary 3d scene graphs for long-term language-guided mobile manipulation, IEEE Robotics and Automation Letters 10 (5) (2025) 4252–4259. doi:10.1109/LRA.2025.3547643. 

- [26] H. Jiang, B. Huang, R. Wu, Z. Li, S. Garg, H. Nayyeri, S. Wang, Y. Li, Roboexp: Action-conditioned scene graph via interactive exploration for robotic manipulation (2024). arXiv:2402.15487. URL `https://arxiv.org/abs/2402.15487` 

- [27] Z. Ying, X. Yuan, B. Yang, Y. Song, Q. Xu, F. Zhou, W. Sheng, Rp-sg: Relation prediction in 3d scene graphs for unobserved objects localization, IEEE Robotics and Automation Letters 9 (2) (2024) 1412–1419. doi:10.1109/LRA.2023.3342666. 

- [28] G. Tang, Q. Jia, G. Chen, Z. Huang, Z. Yao, N. Ji, Three-dimensional-grounded visionlanguage framework for robotic task planning: Automated prompt synthesis and supervised reasoning, Engineering Applications of Artificial Intelligence 164 (2026) 113268. doi:https://doi.org/10.1016/j.engappai.2025.113268. 

   - URL `https://www.sciencedirect.com/science/article/pii/S0952197625032993` 

50 

