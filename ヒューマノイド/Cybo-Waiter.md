---
title: "Cybo-Waiter: A Physical Agentic Framework for Humanoid Whole-Body Locomotion-Manipulation"
date: "2026-03-11"
authors: "Peng Ren; Haoyang Ge; Chuan Qi; Cong Huang; Hong Li; Jiang Zhao"
url: https://arxiv.org/abs/2603.10675
pdf: https://arxiv.org/pdf/2603.10675
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.10675)** / [論文ページ](https://arxiv.org/abs/2603.10675)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Cybo-Waiter: A Physical Agentic Framework for Humanoid Whole-Body Locomotion–Manipulation 

Peng Ren<sup>1,2,*</sup> , Haoyang Ge<sup>3,2,*</sup> , Chuan Qi<sup>4,2</sup> , Cong Huang<sup>2,5</sup> , Hong Li<sup>6</sup> , Jiang Zhao<sup>1</sup> , Pei Chi<sup>1,</sup><sup>_†_</sup> , Kai Chen<sup>2,5,6,</sup><sup>_†_</sup> , 

> 1Beihang University, Beijing, China 

> 2Zhongguancun Academy, Beijing, China 

> 3Tianjin University, Tianjin, China 

> 4University of Science and Technology of China, Hefei, China 

> 5Zhongguancun Institute of Artificial Intelligence, Beijing, China 

> 6DeepCybo, Beijing, China 

> *Equal contribution. 

> _†_ Corresponding authors: Pei Chi (peichi@buaa.edu.cn), Kai Chen (kaichen@zgci.ac.cn). 

**_Abstract_ —Robots are increasingly expected to execute open ended natural language requests in human environments, which demands reliable long horizon execution under partial observability. This is especially challenging for humanoids because locomotion and manipulation are tightly coupled through stance, reachability, and balance. We present a humanoid agent framework that turns VLM plans into verifiable task programs and closes the loop with multi object 3D geometric supervision. A VLM planner compiles each instruction into a typed JSON sequence of subtasks with explicit predicate based preconditions and success conditions. Using SAM3 and RGB-D, we ground all task relevant entities in 3D, estimate object centroids and extents, and evaluate predicates over stable frames to obtain condition level diagnostics. The supervisor uses these diagnostics to verify subtask completion and to provide condition-level feedback for progression and replanning. We execute each subtask by coordinating humanoid locomotion and whole-body manipulation, selecting feasible motion primitives under reachability and balance constraints. Experiments on tabletop manipulation and long horizon humanoid loco manipulation tasks show improved robustness from multi object grounding, temporal stability, and recovery driven replanning.** 

**_Index Terms_ —Humanoid Robot, Locomotion, Reinforcement Learning, Whole-body Control, VisionLanguage-model** 

## I. Introduction 

Robots are increasingly expected to execute open-ended natural-language requests in real human environments, such as “tidy up the desk” or “bring me a drink” [1]–[4]. Such tasks are long-horizon and spatially extended: the robot must navigate and manipulate under clutter and occlusion while ensuring safe whole-body motion near people and furniture [5]. Accordingly, many works cast instruction following as a _robot agent_ problem that compiles language into executable steps and revises them online. During execution, the agent must continually decide what to do 

Equal contribution. 

next, ground language to scene entities, and verify step completion under noisy observations, motivating designs that couple high-level reasoning with grounded perception and reliable execution. 

Under this problem setting, many language-conditioned robot systems instantiate a modular pipeline with three stages: task planning, semantic grounding, and execution evaluation. Planning methods decompose instructions into skill sequences and may leverage feedback, e.g., feasibilityaware selection [6], code-generated feedback loops [7], and language-based self-feedback for replanning [8]; grounding methods map language to spatial or geometric representations for 3D-aware action generation and constraint reasoning [9]. Because long-horizon success is ultimately determined by interaction outcomes over time, platforms and benchmarks emphasize evaluation in closed-loop execution beyond offline VQA [10], [11]. 

Nevertheless, achieving robust long-horizon execution in the real world remains brittle. Free-form model outputs can be underspecified for downstream controllers, implicit success detection is susceptible to transient perception noise, and failures are hard to attribute and recover from. These challenges motivate explicit verification and replanning, such as logic-based plan checking [12] and sceneperception-driven proactive replanning [13], [14]. However, most existing frameworks are validated on mobile manipulators or wheeled platforms and do not fully account for the tighter coupling and safety constraints of humanoid whole-body execution. 

This limitation becomes even more critical for humanoid agents, where whole-body constraints tightly couple locomotion and manipulation through stance, reachability, and balance [15]–[18]. Consequently, small distance and pose errors can cascade into failures during subsequent locomotion and manipulation. Recent humanoid systems can pursue two directions: (i) hierarchical agent stacks that improve online efficiency via learned intermediate decision layers and modular skills [19], as well as VLM-based 

monitoring for skill sequencing on real humanoids [20]; and (ii) learning-heavy vision-language-action policies trained at scale for large-space whole-body loco-manipulation, studied in either real-robot or large-scale simulation settings [21], [22]. While highly promising, these approaches typically emphasize efficiency or broad generalization. In contrast, a key requirement for a dependable humanoid agent remains under-explored: a _verifiable and diagnosable_ execution loop that grounds all task-relevant entities in actionable 3D geometry, evaluates explicit success conditions with temporal stability under noisy perception, and triggers targeted recovery when conditions are violated, helping to avoid premature termination and unsafe motions. 

To address this, we propose a training-light humanoid agent framework that turns open-ended VLM plans into _verifiable task programs_ and closes the loop with _multiobject 3D geometric supervision_ . Given an instruction, a VLM-based planner compiles it into a sequence of structured subtasks in a typed JSON schema, where each subtask specifies task-conditioned entity descriptions and explicit preconditions/success conditions as predicate assertions with temporal stability. We then ground _all task-relevant entities_ , including the manipulation target, the destination region, and any objects referenced by predicates, in 3D using SAM3 segmentation and RGBD observations, recovering object-centric geometric states and pairwise relations [23]. A geometry-grounded supervisor evaluates predicates over stable frames, produces condition-level diagnostics, and triggers targeted recovery, such as re-grounding, re-approach adjustment, or replanning. Finally, these supervision signals are integrated with whole-body execution by gating locomotion and MPCbased upper-body manipulation through task-conditioned feasibility and safety constraints, enabling robust longhorizon humanoid loco-manipulation. 

In this paper, our main contributions are: 

- A structured and verifiable task interface that compiles VLM outputs into typed subtasks with explicit predicate-based preconditions and success conditions. 

- Task-conditioned _multi-object_ 3D grounding using SAM3+RGB-D to recover object-centric geometric states and relations for verification. 

- A geometry-grounded supervisor with temporal stability and condition-level diagnostics that enables targeted recovery and feedback-driven replanning. 

- An integrated humanoid execution layer that bridges geometric supervision to whole-body control for longhorizon loco-manipulation. 

## II. Related Work 

## _A. Language-conditioned Robot Agents_ 

Recent language-conditioned robot agents leverage LLM/VLMs to decompose open-ended instructions into modular skill sequences and execute them with varying 

degrees of online feedback, e.g., feasibility-aware skill selection [6], program/code-based policies with embedded feedback loops [7], zero-shot language planning [24], and self-reflective replanning via language feedback [8], with benchmarks further emphasizing that reliable evaluation should go beyond offline VQA and include closed-loop execution [10], [25]. 

## _B. Grounding and Geometric Verification for Execution_ 

Complementary to high-level planning, prior work grounds language into spatial or object-centric representations for action generation and verification, including 3D-aware grounding and affordance reasoning [9], [26], [27] as well as explicit verification and replanning mechanisms such as logic-based plan checking [12] and scenegraph/perception-driven proactive replanning [13], [14], but these approaches often provide limited condition-level diagnostics tied to multi-object 3D geometry. 

## _C. Humanoid Agents and Whole-Body Loco-Manipulation_ 

Humanoid agents pose additional challenges due to whole-body coupling between locomotion, balance, and manipulation, and recent systems pursue either hierarchical stacks that improve online efficiency via connectorstyle intermediate decision layers and modular skills [19], [28], [29] or VLM-based monitoring for skill sequencing on real humanoids [20], or learning-heavy vision-languageaction policies trained at scale for large-space whole-body loco-manipulation [21], [22], [30]. 

## III. Methods 

We address long-horizon humanoid loco-manipulation from a natural language instruction _I_ using RGB-D observations and robot state in a closed loop. Our system, as shown in Fig. 1, comprises structured VLM task decomposition, task conditioned multi object Tracking, predicate based supervision and targeted recovery, feedback driven replanning, and integrated whole body execution for locomotion and MPC-based manipulation. 

## _A. Structured VLM Task Decomposition_ 

We decouple semantic planning from perception and execution through a structured subtask interface. Given a high level command _I_ and observation _ot_ , a VLM-based planner generates a task plan _P_ = _⟨task_  id, I, {τi}_<sup>_N_</sup> _i_ =1<sup>_⟩_.</sup> We compile form VLM outputs into a typed JSON. 

## _τi_ = _⟨_ `subtask_id` _,_ `type` _,_ `target` _,_ `destination` _,_ 

`manipulation` _,_ `locomotion` _,_ `preconditions` _,_ (1) `success_conditions` _,_ `failure_handlers` _,_ 

## `timeout_sec` _,_ `max_retry` _⟩._ 

Here, type identifies the subtask family. The field `target` specifies the object to be grounded through a symbolic handle ( `ref` ) and a language descriptor ( `phrase` ), optionally augmented with `category` , `attributes` , and 


Fig. 1: System overview of the humanoid agent. 

`relations` . We use `destination` to describe the intended goal region or reference object in natural language. The `manipulation` block instantiates an action primitive together with actuation settings such as arm selection and whether to enable upper-body MPC. Finally, `preconditions` and `success_conditions` are represented as predicate assertions with temporal stability specified by `stable_frames` , which enables deterministic monitoring and closed-loop replanning. An example is provided in Appendix A. 

We detail how task-conditioned specifications are grounded into segmentation and 3D geometry, and how predicates are evaluated over stable frames in next subsection. 

_B. Conditional Segmentation and Geometric Coordinate Estimation_ 

This module grounds the task-conditioned plan from Sec. III-A into _multi-object_ 3D geometric estimates. Given an RGB-D observation _ot_ and the active subtask _τi_ , we identify a set of task-relevant entities 


where `relation references` are objects mentioned in `target.relations` , and `predicate references` are objects appearing in `preconditions` / `success_conditions` arguments, e.g., the `support` object in `SUPPORTED_BY` . This ensures that both the manipulation target and goal/reference entities are segmented and localized. 

_a) Task-conditioned multi-object segmentation.:_ For each entity _e ∈Ei_ , we query SAM3 to obtain a set of candidate masks _Me_ = _{me,k}_ [23]. The query is conditioned 

on the plan fields: `target.phrase` prompts segmentation of the manipulated object, `destination.phrase` prompts segmentation of the goal container/region, and referenced entities are prompted by their associated phrases or predicate roles. Optional attributes and relations refine the query to resolve ambiguity. When multiple instances are detected, we maintain temporal consistency for each entity by favoring candidates that remain stable across time. For entities without an explicit `ref` in the plan, we create an internal identifier and maintain a mapping in the workspace state. 

_b) Lifting masks to 3D geometric states.:_ For each candidate mask _me,k_ , we back-project masked depth pixels into a point cloud _Pe,k_ using calibrated RGB-D intrinsics, and estimate a compact geometric state: (i) centroid _ce,k_ in the world frame, (ii) spatial extent _be,k_ , and (iii) confidence _qe,k_ combining segmentation confidence with depth validity and point support. For subtasks requiring orientation cues, we additionally estimate an orientation descriptor from _Pe,k_ , such as a dominant surface normal or a principal axis via PCA. To improve robustness under sensor noise and partial observations, we apply temporal filtering and reject outliers with inconsistent depth, insufficient inlier support, or abrupt geometric changes. 

_c) Candidate selection and object-centric representation:_ For each entity _e ∈Ei_ , we select the best instance by jointly scoring semantic consistency, relational consistency, geometric feasibility, and temporal stability: 


The selected target instance is packaged as the handle _hi_ = _⟨_ `ref` _, m_ `target` _,k_ `target`<sup>_⋆,c_</sup><sup>`target`</sup><sup>_,k_</sup> `target`<sup>_⋆,b_</sup><sup>`target`</sup><sup>_,k_</sup> `target`<sup>_⋆,q_</sup><sup>`target`</sup><sup>_,k_</sup> `target`<sup>_⋆⟩_,</sup> while all entities, including `destination` and predicate references, are stored in an object-centric workspace state _Wt_ . From _Wt_ , we derive pairwise geometric relations such as object–container distance, object–support height difference, end-effector–object distance, and relative alignment, which are consumed by the supervisor to evaluate plan predicates and trigger recovery or replanning when needed. 

## _C. Supervisor: Task Monitoring with RGB-D and SAM3_ 

_a) Role and inputs:_ The supervisor verifies task progress and completion in a closed loop. At each time step _t_ , it consumes the active subtask _τi_ from the plan = (Sec. III-A), the target handle _hi ⟨_ `ref` _, m, c, b, q⟩_ , and the object-centric workspace state _Wt_ constructed in Sec. III-B. It outputs a discrete subtask status ( `in_progress` , `done` , `blocked` , `failed` ) together with an `uncertain` flag, condition-wise flags, and continuous diagnostic metrics to support recovery and replanning. 

_b) Predicate representation:_ For each active subtask _τi_ , the plan specifies a set of preconditions _Pi_ and success conditions _Gi_ . Each condition is a parameterized predicate _p_ = _⟨k, a,_ op _, v, n⟩_ , where _k_ is a predicate key such as `VISIBLE` , `SUPPORTED` _BY, `SUPPORTED_BYINSIDE` , _a_ denotes grounded arguments instantiated from the plan, op is a comparator, _v_ is a target value, and _n_ is the required stability length given by `stable_frames` . Let _Wt_ be the object-centric geometric workspace state at time _t_ , which contains per-object estimates, including mask, centroid, extent, confidence, and optional orientation descriptors, as well as derived pairwise relations. We evaluate predicates via a monitoring function _ϕ_ ( _k, a_ ; _Wt_ ) _∈_ R that returns a scalar geometric measure parameterized by _a_ . We treat safety/feasibility checks as invariant preconditions that must remain satisfied throughout execution. 

_c) Evaluation, temporal stability, and subtask status.:_ For a predicate _p_ = _⟨k, a,_ op _, v, n⟩_ , we compute a scalar measure _ϕ_ ( _k, a_ ; _Wt_ ) _∈_ R from the geometric workspace state _Wt_ , and convert it into an instantaneous boolean value: 


where **1** ( _·_ ) is an indicator function that equals 1 if its argument is true and 0 otherwise. To suppress transient noise, we require the predicate to hold for _n_ consecutive frames: 


which equals 1 iff eval( _p, u_ ) = 1 for all _u ∈_ [ _t − n_ + 1 _, t_ ]. 

We define readiness and completion as conjunctions over predicate sets: 


where _∧_ denotes logical AND. If Ready( _τi, t_ ) = 0, the supervisor marks the subtask as `blocked` and reports the failing predicates. If Done( _τi, t_ ) = 0 for longer than `timeout_sec` , or if safety/feasibility predicates are violated, the supervisor marks `failed` and triggers recovery or replanning; otherwise it remains `in_progress` . 

_d) Diagnostics and corrective feedback:_ Beyond discrete subtask status, the supervisor returns a diagnostic vector **d** _t_ computed from _Wt_ , including continuous measures such as object–support height gap, relative distance, alignment angle, and confidence/stability scores. These metrics localize which constraints/predicates fail and quantify the magnitude of error, enabling targeted corrections. When estimates are unreliable, the supervisor requests re-observation or re-grounding before proceeding. The diagnostic vector is forwarded to downstream modules as structured signals for corrective motion and replanning. 

_e) VLM-assisted semantic verification:_ In addition to geometric predicates, we optionally invoke a VLM as a semantic verifier when the supervisor raises the `uncertain` flag, or when completion depends on non-geometric cues. Given the active subtask _τi_ and a compact visual context (RGB image, optional masks, and key geometric diagnostics), the VLM outputs a boolean judgment and a short rationale about whether the subtask is completed. We use this signal as _auxiliary_ feedback rather than a primary success criterion: geometric verification takes precedence whenever predicates are reliably evaluable from _Wt_ , and VLM verification is consulted only when geometric evidence is missing, ambiguous, or low-confidence. If the two signals disagree, the system triggers re-observation or regrounding before declaring success. 

## _D. Feedback-Driven Replanning for Robust Task Execution_ 

_a) Replanning triggers:_ Replanning is triggered by structured feedback from the supervisor. Concretely, we initiate replanning when (i) a subtask becomes `blocked` due to unsatisfied preconditions, (ii) a subtask is marked `failed` , or (iii) the supervisor raises an `uncertain` flag due to low-confidence or inconsistent geometric estimates. 

_b) Structured feedback:_ At runtime, the supervisor returns (1) the discrete subtask status, (2) the set of failing predicate instances and their grounded arguments, and (3) continuous diagnostics **d** _t_ . Conditioned on the subtask phase, we define the failing predicate set as 


and form a compact feedback record _Ft_ = _⟨τi,_ `status` _, Pt_<sup>fail</sup> _,_ **d** _t⟩_ , which is consumed by the planner to decide whether to re-observe, re-ground, retry with modified parameters, or replan the remaining subtasks. For `in_progress` , we primarily use **d** _t_ to diagnose progress and select corrective actions. 

_c) Recovery actions:_ We employ a small set of reusable recovery operators conditioned on the failure type: (i) _Re-observation_ : adjust viewpoint or pause to acquire a more reliable RGB-D frame, (ii) _Re-grounding_ : re-run conditional segmentation and 3D estimation with updated prompts/relations, (iii) _Skill/parameter adaptation_ : switch the manipulation primitive or refine target tolerances based on **d** _t_ , micro-adjust end-effector pose when alignment error is small, and (iv) _Task-level revision_ : modify the remaining plan by inserting corrective subtasks. These operators can be specified in `failure_handlers` and executed before calling the VLM planner for full replanning. 

_d) Retry budget and plan update:_ Each subtask carries an execution budget via `timeout_sec` and `max_retry` . If the retry budget is not exhausted, we re-execute _τi_ after applying a recovery operator; otherwise, we request the planner to generate an updated plan _P_<sup>_′_</sup> conditioned on _Ft_ , while preserving completed subtasks and updating symbolic references for consistent grounding. 

## _E. Integrated Execution Framework for Robust Humanoid_ 

## _Task Execution_ 

_a) Execution interface:_ The execution layer instantiates plan-level subtasks _τi_ into low-level humanoid controllers. It takes as input the active subtask schema together with the grounded target handle _hi_ , and dispatches either locomotion or manipulation skills depending on `type` . Crucially, the layer follows the plan fields `locomotion` and `manipulation` as an explicit control interface, and returns execution status and telemetry to the supervisor for monitoring and replanning. 

_b) Locomotion as a gait-conditioned RL skill library:_ For `LOCOMOTION` subtasks, we use a single reinforcementlearned locomotion policy as a stand-alone skill. The policy is _gait-conditioned_ : at runtime the agent selects a discrete gait identifier `gait_id` , and the policy produces lowerbody commands for robust balance and stepping while tracking desired base velocity and yaw-rate commands. We train this policy with a multi-clip locomotion dataset consisting of 12 motion clips, covering forward/backward walking, lateral stepping, running, and in-place turning. 

To expose a compact action interface to the planner/supervisor, we map the 12 clip-level gaits into 7 locomotion primitives: _forward walk_ ( `gait_id` _∈{_ 0 _,_ 1 _}_ ), _backward walk_ ( `gait_id` _∈ {_ 2 _,_ 3 _}_ ), _carry-and-walk_ ( `gait_id` _∈{_ 4 _,_ 5 _}_ ), _run_ ( `gait_id` _∈{_ 6 _,_ 7 _}_ ), _side-walk_ ( `gait_id` _∈{_ 8 _,_ 9 _}_ ), _turn-left_ ( `gait_id` = 10), and _turnright_ ( `gait_id` = 11). For primitives with multiple available clips, we either select a canonical clip or sample 

within the clip group, which improves coverage and reduces overfitting to a single clip. This gait-conditioned design provides a unified locomotion skill library for longhorizon execution and recovery, enabling task-dependent repositioning without hand-coded motion scripts. 

The policy is trained in simulation to track commanded base velocities and yaw rates while maintaining balance and contact stability. We condition the policy on `gait_id` and train on a mixture of motion clips with domain randomization to improve robustness. 

_c) Manipulation with decoupled upper-body control.:_ For `MANIPULATION` subtasks, the execution layer performs arm motion while maintaining lower-body stability. The arm and action are specified by the plan, and the target handle _hi_ provides the geometric reference for motion generation. When `use_upper_body_mpc` is enabled, we solve an upper-body MPC problem to produce constraintaware end-effector trajectories. Meanwhile, the lower body is controlled independently to preserve balance and support stance, allowing manipulation to proceed without destabilizing the humanoid. 

_d) Cross-skill coordination and transitions.:_ Longhorizon tasks typically require alternating between repositioning and manipulation. We implement a lightweight coordinator that switches between the RL locomotion skill and the upper-body manipulation controller based on subtask type and supervisor feedback. In particular, if geometric preconditions are not satisfied, the coordinator triggers a locomotion subskill to reposition until the supervisor marks the subtask `ready` ; if manipulation tracking errors increase or safety predicates are violated, the coordinator pauses arm motion and requests recovery actions. This decoupled design enables robust locomotionmanipulation execution while preserving a clean agentfacing interface defined by the JSON plan. 

## IV. EXPERIMENTS 

## _A. Real-World Setup_ 

We conduct real-world experiments on a Unitree G1 humanoid robot equipped with a Dex3-1 dexterous hand for manipulation and a head-mounted RGB-D camera for egocentric perception. Our system is deployed in a twocomputer setup. A desktop workstation with an RTX 5080 GPU runs the perception and decision modules, including SAM3-based multi-object segmentation, the VLM-based planning module, and the geometry-grounded supervisor. The robot’s onboard Unitree computer runs the low-level controllers, including the arm control stack and the RL locomotion policy. 

Our experiments are performed in an indoor office environment that includes typical furniture and everyday objects. The scene is cluttered to induce partial observability, occlusions, and viewpoint changes, providing a challenging testbed for loco-manipulation. 

We evaluate the agent on a suite of long-horizon humanoid loco-manipulation tasks. To enable direct com- 


(a) Initial scene with the bottle (b) Reaching and grasping the (c) Lifting and transporting (d) Placing the bottle into the and tray. bottle. the bottle toward the tray. tray. 

Fig. 2: Partial “Tidy-the-desk” subtasks: bottle pick-and-place into a tray. 


(a) Searching for the user. (b) Approaching the user. 

(c) Handing over the drink. (d) The user receives the drink. 

searches for the user, approaches them, hands over the 

Fig. 3: Partial “Bring-me-a-drink” subtasks: the humanoid drink, and completes the delivery. 

parison with Being-0, we include the same tasks [19]: `Fetch-bottle` , `Deliver-box` , `Grasp-bottle` , `Place-box` , and `Place-coffee` . 

Beyond these, we introduce additional long-horizon tasks not reported in Being-0 to stress open-ended instruction following and multi-object tabletop reasoning: (i) `Tidy-desk` , which requires repeatedly picking and placing multiple objects until the desk is cleared. (ii) `Tabletop-sorting` , which requires categorizing objects into different containers. (iii) `I’m in a bad mood, bring me a drink` , which requires fetching a drink and handing it over to the user. 

## _B. Results on Being-0-aligned Multi-step Tasks_ 

We report success rates on the Being-0-aligned multistep task suite in Table I. We follow the task definitions and success criteria from Being-0 as closely as possible, and report our results over 10 trials per task. Across multistep routines, our agent achieves reliable completion by combining structured task programs with multi-object 3D grounding and predicate-based supervision. 

TABLE I: Comparing the proposed method with being-0, the results show the number of successful manipulations in 10 trials. 

|**Task**|**Being-0**|**Cybo-Waiter**|
|---|---|---|
|**Fetch-bottle**|9/10|9/10|
|**Deliver-basket**|8/10|8/10|
|**Grasp-bottle**|8/10|**10/10**|
|**Place-basket**|6/10|**9/10**|
|**Place-coffee**|6/10|**8/10**|


## _C. Results on Long-Horizon Tasks_ 

Table II reports success counts over 10 trials for each task. Our full system consistently outperforms the ablation **W/O Supervisor** , improving success from 5/10 to 7/10 on `Tidy-desk` , from 6/10 to 8/10 on `Tabletop-sorting` , and from 7/10 to 9/10 on `Bring-me-a-drink` (see Figs. 2 and 3 for qualitative examples). These gains highlight the importance of the supervisor in long-horizon execution: by evaluating predicate-based preconditions and success conditions over stable frames, the supervisor reduces pre- 

TABLE II: Success counts over 10 trials on additional long-horizon tasks. We compare the full system (CyboWaiter) with an ablation that disables the supervisor (W/O Supervisor). 

|**Task**|**W/O Supervisor**|**Cybo-Waiter**|
|---|---|---|
|**Tidy-desk**|5/10|7/10|
|**Tabletop-sorting**|6/10|**8/10**|
|**Bring-me-a-drink**|7/10|**9/10**|


mature transitions caused by transient perception noise, detects off-nominal states, and triggers targeted recovery instead of restarting the entire task. Overall, the results suggest that geometry-grounded monitoring and feedback are critical for maintaining reliable task progression when tasks require repeated object-level actions and extended navigation. 

## V. Conclusion and Limitations 

We have presented a VLM-driven hierarchical agent framework for humanoid locomotion-manipulation task execution. By combining task-conditioned grounding, segmentation-grounded geometric monitoring, structured feedback-driven replanning, and a humanoid integrated execution layer, the proposed system has enabled more reliable long-horizon execution and recovery. Experiments on representative tasks have demonstrated the effectiveness of the framework and have highlighted the value of explicit monitoring and structured recovery in humanoid agent systems. 

## Appendix 

**Example.** A minimal plan snippet following our schema is: 

```
{
"task_id":"6e0d3831",
"command":"Helpmetidyupthedesk.",
"subtasks":[
{"subtask_id":1,
"type":"MANIPULATION",
"name":"subtask_1",
"target":{"ref":"obj_1",
"category":"unknown",
"attributes":[],
"relations":[],
"phrase":"cup"},
"destination":{"phrase":"container"},
"manipulation":{"arm":"RIGHT",
"action":"PLACE",
"use_upper_body_mpc":true},
"locomotion":{},
"preconditions":[{"key":"VISIBLE",
"args":{"object":"obj_1"},
"op":"==",
"value":true,
"stable_frames":3}],
"success_conditions":[{"key":"SUPPORTED_BY",
"args":{"object":"obj_1",
"support":"table_1"},
"op":"==",
"value":true,
"stable_frames":10}],
```

```
"failure_handlers":[],
"timeout_sec":30,
"max_retry":2}
]
}
```

## References 

- [1] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A visionlanguage-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [2] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai _et al._ , “ _π_ 0 _._ 5 : a vision-language-action model with open-world generalization,” _arXiv preprint arXiv:2504.16054_ , 2025. 

- [3] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu _et al._ , “Rt-1: Robotics transformer for real-world control at scale,” _arXiv preprint arXiv:2212.06817_ , 2022. 

- [4] X. Zhao, M. Li, C. Weber, M. B. Hafez, and S. Wermter, “Chat with the environment: Interactive multimodal perception using large language models,” in _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2023, pp. 3590–3596. 

- [5] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-languageaction models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

- [6] A. Brohan, Y. Chebotar, C. Finn, K. Hausman, A. Herzog, D. Ho, J. Ibarz, A. Irpan, E. Jang, R. Julian _et al._ , “Do as i can, not as i say: Grounding language in robotic affordances,” in _Conference on robot learning_ . PMLR, 2023, pp. 287–318. 

- [7] J. Liang, W. Huang, F. Xia, P. Xu, K. Hausman, B. Ichter, P. Florence, and A. Zeng, “Code as policies: Language model programs for embodied control,” in _2023 IEEE International conference on robotics and automation (ICRA)_ . IEEE, 2023, pp. 9493–9500. 

- [8] W. Huang, F. Xia, T. Xiao, H. Chan, J. Liang, P. Florence, A. Zeng, J. Tompson, I. Mordatch, Y. Chebotar _et al._ , “Inner monologue: Embodied reasoning through planning with language models,” _arXiv preprint arXiv:2207.05608_ , 2022. 

- [9] W. Huang, C. Wang, R. Zhang, Y. Li, J. Wu, and L. Fei-Fei, “Voxposer: Composable 3d value maps for robotic manipulation with language models,” _arXiv preprint arXiv:2307.05973_ , 2023. 

- [10] P. Guo, Z. Mai, Z. Xu, K. Zhang, H. Zhang, Z. Miao, A. Ajoudani, Z. Kingston, Q. Qiu, and Y. She, “Agenticlab: A real-world robot agent platform that can see, think, and act,” _arXiv preprint arXiv:2602.01662_ , 2026. 

- [11] S. Antol, A. Agrawal, J. Lu, M. Mitchell, D. Batra, C. L. Zitnick, and D. Parikh, “Vqa: Visual question answering,” in _Proceedings of the IEEE international conference on computer vision_ , 2015, pp. 2425–2433. 

- [12] D. S. Grigorev, A. K. Kovalev, and A. I. Panov, “Verifyllm: Llmbased pre-execution task plan verification for robots,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2025, pp. 18 489–18 496. 

- [13] C. R. Yu, D. Chae, D. Seo, S. Lee, H. Im, and J. Kim, “Scene graph-guided proactive replanning for failure-resilient embodied agent,” _arXiv preprint arXiv:2508.11286_ , 2025. 

- [14] A. Mei, G.-N. Zhu, H. Zhang, and Z. Gan, “Replanvlm: Replanning robotic tasks with visual language models,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 11, pp. 10 201–10 208, 2024. 

- [15] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu, “Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv preprint arXiv:2508.08241_ , 2025. 

- [16] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions On Graphics (TOG)_ , vol. 37, no. 4, pp. 1–14, 2018. 

- [17] X. Lin, Y. Huang, T. Fu, X. Xiong, and C. Wang, “iwalker: Imperative visual planning for walking humanoid robot,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2025, pp. 2865–2872. 

- [18] Y. Ze, Z. Chen, W. Wang, T. Chen, X. He, Y. Yuan, X. B. Peng, and J. Wu, “Generalizable humanoid manipulation with 3d diffusion policies,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2025, pp. 2873–2880. 

- [19] H. Yuan, Y. Bai, Y. Fu, B. Zhou, Y. Feng, X. Xu, Y. Zhan, B. F. Karlsson, and Z. Lu, “Being-0: A humanoid robotic agent with vision-language models and modular skills,” _arXiv preprint arXiv:2503.12533_ , 2025. 

- [20] A. Schakkal, B. Zandonati, Z. Yang, and N. Azizan, “Hierarchical vision-language planning for multi-step humanoid manipulation,” _arXiv preprint arXiv:2506.22827_ , 2025. 

- [21] H. Jiang, J. Chen, Q. Bu, L. Chen, M. Shi, Y. Zhang, D. Li, C. Suo, C. Wang, Z. Peng _et al._ , “Wholebodyvla: Towards unified latent vla for whole-body loco-manipulation control,” _arXiv preprint arXiv:2512.11047_ , 2025. 

- [22] H. Zhang, J. Sun, M. Caprio, J. Tang, S. Zhang, Q. Zhang, and W. Pan, “Humanoidverse: A versatile humanoid for visionlanguage guided multi-object rearrangement,” _arXiv preprint arXiv:2508.16943_ , 2025. 

- [23] N. Carion, L. Gustafson, Y.-T. Hu, S. Debnath, R. Hu, D. Suris, C. Ryali, K. V. Alwala, H. Khedr, A. Huang _et al._ , “Sam 3: Segment anything with concepts,” _arXiv preprint arXiv:2511.16719_ , 2025. 

- [24] W. Huang, P. Abbeel, D. Pathak, and I. Mordatch, “Language models as zero-shot planners: Extracting actionable knowledge for embodied agents,” in _International conference on machine learning_ . PMLR, 2022, pp. 9118–9147. 

- [25] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. R. Narasimhan, and Y. Cao, “React: Synergizing reasoning and acting in language models,” in _The eleventh international conference on learning representations_ , 2022. 

- [26] M. Shridhar, L. Manuelli, and D. Fox, “Cliport: What and where pathways for robotic manipulation,” in _Conference on robot learning_ . PMLR, 2022, pp. 894–906. 

- [27] M. Shridhar and L. Manuelli, “Perceiver-actor: A multi-task transformer for robotic manipulation,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 785–799. 

- [28] H. Xue, X. Huang, D. Niu, Q. Liao, T. Kragerud, J. T. Gravdahl, X. B. Peng, G. Shi, T. Darrell, K. Sreenath _et al._ , “Leverb: Humanoid whole-body control with latent vision-language instruction,” _arXiv preprint arXiv:2506.13751_ , 2025. 

- [29] J. Wang, A. Laurenzi, and N. Tsagarakis, “Autonomous behavior planning for humanoid loco-manipulation through grounded language model,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 10 856–10 863. 

- [30] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath, “Real-world humanoid locomotion with reinforcement learning,” _Science Robotics_ , vol. 9, no. 89, p. eadi9579, 2024. 

