---
title: "Silent Failures in Physical AI: A Literature Review of Runtime Action Authorization for Autonomous Systems"
date: "2026-05-23"
authors: "Barak Or"
url: https://arxiv.org/abs/2606.00090
pdf: https://arxiv.org/pdf/2606.00090
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.00090)** / [論文ページ](https://arxiv.org/abs/2606.00090)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。



**Silent Failures in Physical AI: A Literature Review of Runtime Action Authorization for Autonomous Systems** 

Barak Or, Ph.D. STATE16 May 10, 2026 

Founder and Chief Executive Officer, STATE16 

_Author note._ Dr. Or also serves externally as Lecturer at the Technion – Israel Institute of Technology, Lecturer at Reichman University, and Academic Director of the Google–Reichman AI Tech School. These appointments are listed solely for biographical context. The paper was prepared under the STATE16 affiliation; the external organizations listed here have not sponsored, reviewed, approved, or endorsed it, and the paper does not represent their institutional positions. 

# **Abstract** 

Physical AI systems increasingly map multimodal observations, language instructions, and learned world representations into physically consequential actions [10, 13, 20, 43, 56, 85, 86]. Robotics foundation models, vision-language-action models, and world-model-based autonomous systems can condition decisions that move vehicles, robots, drones, and industrial machines. This transition exposes a safety problem that is not fully captured by conventional AI content moderation or by classical robot safety alone: a black-box model may issue a physically consequential action while appearing confident, plausible, and semantically aligned. The resulting failure can be silent, arising from sensor drift, occlusion, state-estimation error, distribution shift, hallucinated affordances, or invalid physical assumptions before downstream hardware controllers detect a violation [76, 87, 89, 95, 104]. 

Across embodied foundation models, world models, robotics simulation, embodied safety benchmarks, safe control, runtime assurance, uncertainty estimation, verification, and guardrail evaluation, model capability and safety mechanisms have advanced along largely separate technical tracks [33, 42, 43, 51, 64, 67, 85, 86]. A recurring gap synthesized here is that no single stream surveyed 

in this review supplies a complete runtime authorization boundary between black-box Physical AI models and physical execution. The resulting analysis develops a bounded problem formulation, a definition of silent physical-action failure, a taxonomy of runtime guardrail functions, and evaluation requirements for comparing guardrails as Physical AI assurance mechanisms. 

**Keywords:** Physical AI, world models, runtime guardrails, embodied AI, vision-language-action models, silent failures, runtime assurance, autonomous systems, safety filters. 

# **1 Introduction** 

A growing class of AI systems now sits upstream of physical execution. Robotics foundation models, visionlanguage-action (VLA) systems, world models, and embodied agents increasingly transform observations and instructions into trajectories, manipulation policies, navigation decisions, or controller inputs [2, 10, 12, 13, 20, 56, 84– 86]. In this setting, a model does not merely describe a scene or answer a prompt. It may infer affordances, predict future states, choose a trajectory, command a manipulator, or condition a downstream autonomy stack. 

The problem is timely because three technical trends now coincide. First, action-generating foundation models are moving from narrow demonstrations toward crossembodiment robot policies [10, 15, 56, 85, 86]. Second, world models and simulators are becoming more central to robot learning, planning, and evaluation [17, 43, 64, 73, 82, 83]. Third, guardrail research is expanding from content filtering toward policy-grounded, trajectory-level, and embodied safety evaluation [51, 55, 67, 71, 89, 105]. Existing safety methods were largely developed for settings in which the relevant state, controller interface, safe set, or policy boundary is inspectable [4, 42, 59, 108]. Physical AI increasingly combines learned action generation, uncertain state evidence, heterogeneous hardware, and site-specific operational constraints. Under that combination, runtime action authorization becomes a distinct technical question: when, and on what evidence, may a plausible model proposal become a physical commitment? 

This shift changes the meaning of guardrails. In textonly systems, guardrails often focus on content policy, harmful instructions, privacy, bias, or misuse [51]. In Physical AI, guardrails often involve mechanisms for evaluating whether a proposed action is physically, operationally, and temporally safe in a particular world state [55, 89]. A model can generate a plausible action that is unsafe because the world state is corrupted, the environment is partially observed, the system is outside its training distribution, or the action violates a hard operational boundary [71, 76, 87, 104]. 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


audit. 

The reviewed literature motivates an independent authorization boundary between black-box model outputs and physical execution [42, 51, 55, 59, 67, 89, 97]. This boundary functions as a composition point for model proposals, state evidence, physical constraints, fallback behavior, and audit traces. 

The relevant failure mode is the _silent failure_ : a case in which an autonomous system acts with high apparent confidence on an incorrect, incomplete, or physically invalid representation of the world. Silent failures are especially concerning in closed-loop autonomy because they may not appear as explicit software crashes. Instead, the system continues operating while its internal assumptions drift away from reality. Examples include drones acting on false free-space estimates, autonomous mobile robots navigating under occlusion, vehicles misinterpreting rare scenarios, or robot policies executing hallucinated affordances [5, 71, 76, 89, 92, 105]. 

The deployment motivation is safety-relevant autonomy, where incident investigations and safety evaluations indicate that failures can arise from perception, prediction, control, operational context, and monitoring assumptions rather than from a single isolated model error [16, 76, 78, 79, 89, 92]. For black-box world models, robotic foundation models, or learned autonomy stacks, the recurring question is: _Should this proposed physical action be authorized in this context?_ Model confidence, semantic refusal, offline benchmark scores, and hardware controllers each address part of the problem, but they do not by themselves define the full action-authorization boundary. 

### **Main Problem** 

A central problem is **runtime action authorization under uncertain world state** . Physical AI systems can map language, images, and learned world representations into physical actions at increasing scale [10, 13, 56, 85, 86]. A recurring issue is the limited treatment of a common, auditable boundary that evaluates four conditions before execution: whether the world state is reliable, whether the proposed action is physically feasible, whether it satisfies task and operational constraints, and whether the decision can be reconstructed after deployment [42, 55, 67, 89]. 

The scope is runtime action authorization for blackbox VLA, world-model, and foundation-model-based autonomous systems whose outputs can become physical actions [10, 43, 56, 104]. This is not a general Physical AI survey, a robotics standards survey, a simulator survey, a certification manual, or a survey of AI ethics. Adjacent literatures are included when they clarify one part of the authorization pathway: model proposal, state evidence, physical feasibility, operational constraints, fallback, or 

Figure 1 illustrates the embodiment scope of this problem. The specific constraints differ across manipulators, autonomous mobile robots, legged robots, and aerial vehicles, but the runtime question is structurally similar: whether a proposed physical action should be authorized in the current state, under the active constraints, before the action becomes a hardware commitment. Examples of platform-specific evidence include payload and contact limits, clearance and routing constraints, terrain and balance conditions, and airspace or energy limits. 

## **1.1 Contributions** 

Five technical contributions follow from this framing. First, the paper defines a linked vocabulary: _silent physical-action failure_ , _runtime action authorization_ , _authorization event_ , and the _authorization gap_ . Second, it formalizes runtime action authorization under uncertain state as a decision interface between black-box model outputs and physical execution. Third, it synthesizes eleven research streams into a guardrail taxonomy spanning semantic validity, state validity, physical feasibility, spatial and operational constraints, temporal validity, fallback authority, and auditability. Fourth, it derives evaluation requirements and metric families for guardrails that measure intervention quality rather than only model task success. Fifth, it distills these elements into a minimal authorization event schema for comparing guardrails across models, simulators, controllers, and physical platforms. 

The next sections proceed from formalization and guardrail taxonomy to the literature map, Physical AI capability trends, silent failures, runtime authority, evaluation, synthesis, implications, limitations, and conclusion. 

# **2 Problem Formalization and Theoretical Anchors** 

A minimal notation is sufficient for the central safety question. Each equation below corresponds to one point in the runtime pathway: what action is proposed, what evidence is available, whether the action is authorized, where a silent failure appears, and how existing safety theory can be attached to the boundary. 

Let _o≤t_ denote the observation history available to the autonomy stack up to time _t_ , and let _g_ denote the task goal or instruction. A black-box Physical AI model can be represented as a policy, following the common abstraction of learned robot and VLA policies as mappings from observations and goals to actions [10, 12, 13, 56, 85]: 


where _πθ_ is the learned policy or generative action model, _θ_ denotes its parameters, _at ∈A_ is the proposed physical action, and _A_ is the action space. The system also maintains an estimated world state _st ∈S_ , where _S_ is 

2 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


Figure 1: Scope of the review. Different embodiments require different evidence, but the shared unit of analysis is the authorization event before physical execution. 

the state space. The estimate may differ from the true but unobserved physical state because of noise, occlusion, drift, latency, or distribution shift [40, 76, 87, 95]. 

Let _Ct_ = _{c_ 1 _, . . . , cK}_ denote the active constraint set at time _t_ , where each normalized constraint is satisfied when _ck_ ( _at, st_ ) _≤_ 0. The set may include kinematic constraints, collision constraints, geofences, workspace limits, payload limits, mission rules, and operational policies [4, 16, 44, 78, 79, 108]. For evaluation and audit, the runtime layer can be described by an authorization event: 


where _G_ is the runtime authorization function, _ρt ∈ {_ authorize _,_ modify _,_ block _,_ fallback _,_ escalate _}_ is the decision, _et_ is runtime evidence, and _ft_ is the fallback or recovery action. The evidence term may include sensor health, uncertainty, OOD indicators, constraint checks, policy evidence, or monitor outputs. The fallback term may be empty when the action is authorized, or may describe a safe stop, modified action, backup controller, or human escalation. 

The core authorization gap is that model likelihood is not a safety certificate, consistent with prior work on calibration, uncertainty under shift, and physically invalid action generation [34, 87, 104]: 


Equation (3) is the minimal formal claim. A fluent, highprobability, or semantically aligned action still has to pass state-validity, physical-feasibility, operational, timing, fallback, and audit checks before physical commitment. 

**Definition: silent physical-action failure.** Let _s_ ¯ _t_ denote the true, partially unobserved physical state. Let _Mt_ = 1 mean that the true stateaction pair is authorizable, i.e., _G_ ( _at,_ ¯ _st, Ct, et_ ) = authorize, and let _Mt_ = 0 otherwise. Let _Vt_ = _V_ ( _et_ ) _∈{_ 0 _,_ 1 _}_ indicate whether the runtime evidence is sufficient for physical commitment. The silent-failure indicator is 


A silent physical-action failure occurs when _Ft_ = 1. The failure is silent because the autonomy stack remains operational while the accepted state-action pair is invalid under physical, state, temporal, or operational constraints. 

## **2.1 Connection to Existing Safety Theory** 

The notation above is close to established safety-control and runtime-assurance formalisms, but it places them at the action-authorization boundary rather than only at the low-level controller [4, 42, 59, 108]. Three safety-theory anchors are especially useful. 

First, state uncertainty can be handled conservatively. Let _Ut_ denote an uncertainty set around _st_ , constructed from perception uncertainty, latency, calibration evidence, or OOD signals [34, 41, 62, 66, 68, 87, 95]. A conservative guardrail authorizes only actions whose constraints hold throughout that uncertainty set: 


Here _qt_ ( _at_ ) is the worst-case normalized violation. If _Ut_ = _{st}_ , Equation (5) reduces to a nominal constraint check. If _Ut_ grows because the state estimate is stale, occluded, or unreliable, _qt_ ( _at_ ) can become positive and 

3 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


the runtime decision should move toward modification, fallback, escalation, or blocking. 

Second, when _at_ is a continuous control input and the relevant constraints are explicit, a runtime guardrail can resemble a safety filter. Let _A_<sup>safe</sup> _t_ = _{a ∈A_ : _ck_ ( _a, st_ ) _≤_ 0 _, k_ = 1 _, . . . , K}_ denote the actions that satisfy the active constraints. The guardrail can then be written compactly as a projection: 


Here ˜ _at_ is the closest authorized replacement action under the chosen norm. This projection view is aligned with safety-filter and predictive-safety-filter work, where intervention minimally modifies a proposed command while enforcing known constraints [22, 44, 108]. The important limitation is the interface assumption: the action, state, and constraints must be expressed in a form the filter can evaluate. 

Third, control barrier functions express safety as forward invariance of a safe set. If _h_ ( _st_ ) _≥_ 0 defines the safe set, a common continuous-time barrier condition is 


where _h_ is the barrier function and _α_ is an extended class- _K_ function [4, 27]. This is a strong physical-feasibility tool, but it is not the whole runtime guardrail problem for blackbox VLA systems. It does not by itself decide whether the state estimate is valid, whether the model proposal is semantically acceptable, whether the site policy permits the action, or whether the fallback and audit record are adequate. 

These anchors clarify the scope of runtime action authorization. The guardrail interface does not replace CBFs, safety filters, shielding, reachability, or runtime assurance [3, 4, 22, 42, 44, 108]. It composes them with semantic, state, temporal, spatial, operational, fallback, and audit evidence around one proposed physical action: 


The set _L_ names the semantic, state-validity, physicalfeasibility, timing, operational, fallback, and audit components. Each component is binary or thresholded into a binary authorization component. The decision should be authorize only when all required components are satisfied; otherwise _ρt_ records modification, blocking, fallback, escalation, or another non-authorization outcome. 

Figure 2 summarizes where the equations sit in the safety argument and where the main gaps arise. 

## **2.2 The Authorization Event as a Unit of Analysis** 

The authorization event is not a software API or implementation standard. It is a research and engineering abstraction for comparing how different Physical AI systems connect model proposals, state evidence, constraints, 

runtime decisions, fallback behavior, and audit traces. This keeps the abstraction concrete without making it implementation-specific, while remaining close to runtime assurance and safety-filter thinking [42, 44, 97, 108]. 

The event record in Equation (2) provides a common unit of analysis across otherwise different systems. A VLA policy, a world model, a simulator, a safety filter, a runtime-assurance monitor, and an embodied safety benchmark may expose different internal representations, but each can still be examined by asking which part of _ξt_ it informs: the proposed action _at_ , the state estimate _st_ , the constraint set _Ct_ , the evidence _et_ , the decision _ρt_ , or the fallback _ft_ [42, 43, 56, 71, 82, 85]. This is also the basis for the evaluation metrics below: guardrails are compared at the level of authorization events, not only at the level of task success. Table 7 gives a compact schema for this record. 

## **2.3 Illustrative Deployment Example** 

Consider an autonomous mobile robot operating in a warehouse aisle. A black-box VLA or world-model-based planner receives the instruction “move to the target pallet” and proposes a short-horizon velocity command. The estimated state includes robot pose, obstacle clearance, perception uncertainty, and a workspace map with allowed and restricted zones. A runtime authority does not need to expose the model internals; it needs to decide whether the action is safe to commit under the available evidence. 

For collision clearance, a conservative stopping-distance check is enough to show the safety gap: 


where _τ_ is perception-control latency, _a_ brake is available braking deceleration, and _d_ margin is an added safety margin. The corresponding clearance question is not merely whether the action is task-relevant. If the uncertaintyadjusted clearance _d_<sup>ˆ</sup> _t − ϵt_ is smaller than _d_ stop( _vt_ ), the correct runtime decision is a block, modification, or fallback even when the proposed motion is plausible and high confidence. For example, _vt_ = 1 _._ 2 m/s, _τ_ = 0 _._ 25 s, _a_ brake = 1 _._ 6 m/s<sup>2</sup> , and _d_ margin = 0 _._ 2 m imply _d_ stop = 0 _._ 95 m. If an occlusion reduces reliable clearance to 0 _._ 8 m, the safety evidence is insufficient for physical commitment. **Operational failure chain.** The same example becomes a silent failure if the authorization event is incomplete. A stale occupancy map or occluded pallet first makes the world state appear safer than it is. The VLA planner then proposes a shortcut through the aisle because the action is task-relevant and semantically benign. A semantic guardrail passes the instruction because “move to the target pallet” is not malicious. A low-level controller may also accept the velocity command if it treats the stale map as valid input. The missing check is _G_ state: the runtime authority should reject the command because the evidence term _et_ does not support physical commitment. 

4 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


The critical safety gap is the boundary between a plausible model action and an auditable pre-commit authorization decision. 

Figure 2: Minimal formal structure of runtime action authorization. The equations are organized around the safety boundary rather than presented as an independent mathematical system. 

Table 1: A runtime <u>guardrail</u> taxonomy for black-box Physical AI. 

|**Guardrail function**|**Question evaluated at runtime**|**Representative evidence**|
|---|---|---|
|Semantic validity|Is the requested behavior aligned with task<br>intent, human intent, and misuse policy?|Instruction analysis, policy engine, prompt-injection checks,<br>operator confirmation.|
|State validity|Is the current world state reliable enough<br>for this action?|Sensor integrity, perception anomaly, state-estimate<br>consistency, OOD or drift indicators.|
|Physical feasibility|Can the proposed action be executed un-<br>der robot, vehicle, or machine constraints?|Kinematics, dynamics, collision checks, velocity limits, payload<br>limits, workspace envelope.|
|Spatial and operational<br>validity|Is the action allowed in this location, zone,<br>mission phase, and operational context?|Geofences, restricted zones, fleet policy, task permissions,<br>site-specific rules.|
|Temporal validity|Is the action safe over the relevant future<br>horizon, not only instantaneously valid?|Prediction horizon, time-to-collision, latency margins,<br>counterfactual rollouts, stale-state checks.|
|Fallback authority|If authorization fails, what action should<br>replace or interrupt the model proposal?|Modify/block/escalate decision, safe stop, backup controller,<br>human-in-the-loop routing.|
|Auditability|Can the decision be reconstructed after<br>deployment or incident review?|Structured logs, constraint traces, evidence snapshots,<br>model/action versioning, authorization reason codes.|


If the system authorizes anyway, the failure is silent: the stack remains operational, confidence remains high, and the wrong state-action pair becomes hardware motion. 

# **3 Guardrail Taxonomy** 

The formalization above separates model preference from physical authorization. Table 1 turns that separation into a functional taxonomy. The taxonomy is not a replacement for standards, controller design, or certification; it is an organizing interface for what a runtime authority is expected to evaluate before a black-box Physical AI proposal becomes a hardware commitment [42, 55, 89, 97]. 

# **4 Literature Map and Interface Assumptions** 

## **4.1 Source Selection** 

The source selection follows a focused review strategy suited to a fast-moving AI, robotics, and autonomoussystems literature. The analysis is organized around the technical pathway from observation and learned prediction to physical execution. Sources were identified through arXiv, OpenReview, IEEE, ACM, NeurIPS proceedings, robotics and autonomous-systems venues, official techni- 

cal reports, and platform documentation when the source was needed to describe a simulator or deployed autonomy incident. Works were prioritized when they contribute to at least one of four interfaces: (i) models that generate or condition physical actions; (ii) methods for estimating uncertainty, distribution shift, or invalid state; (iii) safety mechanisms that constrain or monitor autonomous behavior at runtime; and (iv) embodied safety evaluations, guardrail benchmarks, or real-world autonomy incidents that expose failures of monitoring, authorization, or operational control. 

The inclusion criterion was relevance to the actionauthorization pathway. Included work spans VLA models, world models, embodied robot policies, simulation platforms, safe control, runtime assurance, uncertainty and OOD detection, neural-network verification, embodied safety benchmarks, guardrail datasets, and documented physical-autonomy incidents. Broader robotics standards, general AI ethics, generic LLM safety, human factors, and certification processes are excluded unless they directly clarify the connection between model output, state evidence, physical constraints, and execution. This boundary keeps the analysis focused on runtime authorization rather than the full Physical AI literature. 

Search terms were organized around topic families rather than a single keyword query: vision-languageaction models, robot foundation models, world models for robotics, runtime assurance, safety filters, control barrier 

5 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


functions, out-of-distribution detection, embodied safety benchmarks, robot guardrails, physical AI hallucination, simulation for robot learning, and autonomous-system incidents. Each selected source was then coded by the part of the authorization event it informs: model proposal, state evidence, physical feasibility, operational constraints, runtime decision, fallback behavior, evaluation protocol, or audit evidence. This coding scheme is used to organize the related-work synthesis rather than to claim exhaustive coverage of every adjacent field. 

Descriptive claims about prior systems, benchmarks, incidents, and technical results are cited directly. The formal definition of silent physical-action failure, the taxonomy in Table 1, and the evaluation requirements and metric families in Tables 4 and 5 are synthesized from the cited literature rather than attributed to any single source. 

## **4.2 Related Work Streams** 

The analysis draws on eleven bodies of work that jointly define the runtime guardrail problem for black-box Physical AI systems: 

1. embodied foundation models, VLA systems, and robot generalist policies [2, 10, 12, 13, 15, 18, 20, 23, 31, 49, 56, 88, 91, 100, 101, 116]; 

2. large-scale robot datasets, cross-embodiment learning, and VLA data engines [21, 54, 75, 85, 86, 111]; 

3. world models, predictive environment models, and joint-embedding predictive architectures [14, 17, 36– 39, 43, 45, 61, 64, 73, 96]; 

4. robotics simulators, synthetic-data environments, and embodied evaluation platforms [19, 32, 57, 58, 74, 77, 80–83, 94, 98, 107, 113]; 

5. autonomous driving and planning-oriented embodied intelligence [25, 46, 48, 102, 110, 112, 115]; 

6. safe reinforcement learning, safety filters, and control barrier functions [1, 4, 8, 22, 26, 27, 33, 44, 90, 108, 109, 117]; 

7. runtime assurance, shielding, runtime enforcement, and neural-network verification [3, 28, 42, 52, 59, 63, 97, 103]; 

8. uncertainty, calibration, distribution shift, OOD detection, and robustness [24, 30, 34, 40, 41, 53, 60, 62, 66, 68, 87, 95, 106]; 

9. multimodal hallucination and physical-consistency diagnostics [6, 65, 104]; 

10. policy-grounded and trajectory-level guardrail benchmarks [51, 67]; 

11. LLM/VLM-enabled robot safety, jailbreaks, and embodied safety benchmarks [55, 71, 89, 92, 105]. 

Across these literatures, no single family surveyed here provides a complete unifying runtime layer that links model outputs, state evidence, physical constraints, and action authorization into one inspectable system boundary. Table 2 summarizes the hidden interface assumptions that make the gap visible [42, 51, 55, 67, 95]. Entries use compact qualitative codes: “yes”, “partial”, “limited”, “assumes”, “signal”, and “simulated”. 

## **4.3 Interface Assumptions and Failure Points** 

The table should be read as an assumption map rather than a ranking of fields. VLA and embodied foundationmodel works are closest to the model-output side of the boundary: they improve cross-task and cross-embodiment action generation, but their reported success metrics do not by themselves specify whether a proposed action is admissible under deployment-specific rules [10, 56, 85, 86]. Task success, imitation quality, or action fluency can therefore be insufficient evidence for action validity. In a deployed Physical AI system, that assumption is fragile when a high-probability action is grounded in stale state, violates a site policy, or requires a fallback that the model does not represent [76, 89, 104]. 

CBFs and safety filters provide strong mathematical tools when dynamics, state variables, and safe sets are explicit [4, 27, 44, 108]. The limitation for the present argument is not theoretical weakness. It is interface mismatch: black-box VLA systems may output plans, waypoints, latent actions, code-like actions, or language-conditioned action sequences that are not directly expressed as control inputs over a verified safe set. A CBF can help once the relevant state and control interface are exposed, but it does not by itself decide whether the state estimate is reliable, the model proposal is semantically valid, or the deployment policy permits the action. 

Runtime assurance and shielding provide the most direct architectural precedent [3, 42, 59, 97]. Their implicit assumption is that the monitor can evaluate the active controller against trusted safety conditions and switch to an acceptable backup when needed. Physical AI weakens that assumption in two ways: the proposed action may be produced by an opaque model whose action representation is not stable across versions, and the monitor may also need to judge whether the estimated world state is current and coherent enough to support any action at all. 

Semantic guardrails face a different limitation. They evaluate content, intent, policy compliance, jailbreak risk, or harmful requests [51, 67]. Physical execution requires geometry, timing, dynamics, observability, spatial permission, and fallback [55, 89]. A prompt can be benign and still produce an infeasible manipulation, an unsafe velocity command, or an action that is valid in one zone but prohibited in another. This is a structural mismatch between semantic safety and physical authorization [92, 104]. 

This contrast is the main reason action authorization 

6 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


Table 2: Hidden interface assumptions across safety and Physical AI literatures. 

Entries are interpretive synthesis. 

|**Method family**|**State**<br>**validity**|**Uncertainty **|**Model inde-**<br>**pendent**|**Real time**|**Formal**<br>**guarantees**|**Black-box**<br>**policies**|**Multi-step**<br>**actions**|**Auditability**|
|---|---|---|---|---|---|---|---|---|
|VLA and robot foundation<br>models [10, 56, 85, 86]|limited|limited|no|partial|no|yes|partial|limited|
|World models and predic-<br>tive architectures [14, 39,<br>61, 73]|partial|partial|partial|partial|no|partial|yes|limited|
|CBFs and safety filters [4,<br>27, 44, 108]|assumes|partial|yes|yes|assumption-<br>dependent|limited|partial|limited|
|Runtime<br>assurance<br>and<br>shielding [3, 42, 59, 97]|assumes|partial|partial|yes|assumption-<br>dependent|partial|partial|partial|
|OOD, uncertainty, and cal-<br>ibration [34, 62, 66, 68, 87]|signal|yes|partial|partial|no|partial|limited|partial|
|Embodied<br>safety<br>and<br>guardrail<br>benchmarks<br>[51, 67, 71, 89, 92, 105]|partial|partial|partial|limited|no|yes|yes|partial|
|Simulation platforms [19,<br>74, 94, 98, 107, 113]|simulated|partial|yes|partial|no|yes|yes|partial|


is treated as a composition problem. The gap is not that any one literature is weak. It is that each literature makes a different interface assumption, and the assumptions do not automatically compose in a deployment where model proposals, perception evidence, physical constraints, site policy, fallback, and auditability are evaluated around the same event [42, 55, 89, 95]. 

learned action distribution are structurally mismatched; topological, precision, and horizon barriers provide one formal explanation for why fluent action generation is not equivalent to feasible physical execution [104]. This supports the narrower claim that candidate actions should be evaluated against physical constraints rather than treated as self-authorizing. 

# **5 Capability Trends: From Prediction to Action** 

Physical AI can be understood as the class of AI systems whose outputs influence behavior in the physical world. This includes robot policies, autonomous vehicle stacks, drones, industrial automation, humanoids, mobile manipulators, and embodied agents [43, 72, 93, 114]. The recent acceleration in this field is driven by foundation models that combine perception, language, action data, and predictive world representations. 

Robotics foundation models such as RT-1, RT-2, PaLME, Open X-Embodiment, OpenVLA, _π_ 0, GR00T N1, and Octo demonstrate that large-scale data and generalpurpose model architectures can transfer knowledge across tasks, scenes, and embodiments [10, 12, 13, 20, 56, 84– 86]. Earlier systems such as SayCan, VIMA, PerAct, Diffusion Policy, ALOHA, Mobile ALOHA, RoboCat, RoboAgent, and VoxPoser established important design patterns for grounding language, vision, prompts, action representations, and planning in real robot behavior [2, 9, 11, 18, 23, 47, 49, 100, 116]. 

Surveys of VLA models highlight a rapid movement toward policies that map visual observations and naturallanguage goals into action sequences [72, 93, 99, 114, 118]. These systems expand cross-task generalization, but they also make action generation more opaque. The model’s reasoning may be distributed across learned representations that are difficult to inspect or formally verify. 

Recent work on action hallucination makes this risk more explicit. Generative VLA policies can produce physically invalid actions when feasible robot behavior and the 

## **5.1 Empirical Milestones and Remaining Authorization Questions** 

Empirical milestones in Physical AI now span manipulation, mobile robots, autonomous driving, humanoids, data engines, simulation infrastructure, and embodied safety evaluation. Manipulation and mobile-manipulation work has demonstrated language-conditioned and visionconditioned policies for real robot skills, including RT1/RT-2, ALOHA, Mobile ALOHA, Diffusion Policy, PerAct, VoxPoser, OpenVLA, _π_ 0, LeRobot, and SmolVLA [10, 12, 13, 15, 18, 23, 47, 56, 100, 101, 116]. Crossembodiment datasets and policies such as Open X- Embodiment, RT-X, Octo, DROID, BridgeData, and MimicGen show that robot-learning pipelines are increasingly evaluated across robots, tasks, scenes, and data sources [21, 54, 75, 85, 86]. Recent data-centric VLA analysis makes the same point from the infrastructure side: datasets, benchmarks, and data engines have become central objects of research rather than secondary implementation details [111]. 

Autonomous-driving and embodied-navigation work adds planning-oriented and environment-scale evaluation through systems and platforms such as UniAD, DriveLM, LINGO-2, CARLA, AirSim, Habitat, and AI2-THOR [19, 46, 58, 94, 98, 102, 112]. Driving-specific VLA work further shows that language-action coupling is moving from scene interpretation toward trajectory generation, critic-based refinement, and physically informed planning objectives [25, 48, 110, 115]. Humanoid, embodiedreasoning, and synthetic-data infrastructure efforts such as GR00T N1, Gemini Robotics-ER 1.6, NVIDIA Cosmos, and physical-AI data-factory workflows extend the same 

7 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


trend toward larger action spaces, richer state evidence, and more simulation-driven evaluation [31, 81, 83, 84]. 

Several recent VLA and world-model works now report reliability-adjacent numbers, although these numbers are not yet a common safety metric. OpenVLA reports a 7B-parameter model trained on 970k robot demonstrations and absolute task-success gains of 16.5 percentage points over RT-2-X and 20.4 percentage points over Diffusion Policy [56]. WoVR reports average LIBERO success improving from 39.95% to 69.2%, and real-robot success from 61.7% to 91.7%, when hallucination in imagined rollouts is explicitly controlled [50]. VLAW reports a 39.2% absolute success-rate improvement over a base policy and an 11.6% improvement from training with generated synthetic rollouts [35]. VISTA reports out-of-distribution manipulation success increasing from 14% to 69% when world-model-generated visual subgoals guide a hierarchical VLA policy [70]. 

Belief- and hallucination-oriented VLA work gives a complementary signal. RB-VLA reports that its belief module raises success from 32.5% to 77.5% in ablation and reduces inference latency by up to five times [7]. EvoVLA reports a reduction in stage hallucination from 38.5% to 14.8%, together with 54.6% average real-world success across four manipulation tasks [69]. These results are valuable because they make progress measurable, but they mix task completion, hallucination reduction, prediction fidelity, sample efficiency, and latency. They therefore do not yet define a unified probability that the authorization decision _ρt_ is correct for a proposed action _at_ , state estimate _st_ , and active constraint set _Ct_ . 

These milestones sharpen the authorization question rather than making it disappear. Reported task success, cross-platform transfer, large-scale robot data, embodied reasoning, and simulation coverage demonstrate that Physical AI systems are becoming more capable [10, 15, 56, 83, 85, 86]. They do not by themselves answer three deployment questions: whether the state evidence is valid enough for commitment, whether the proposed action satisfies the active physical and operational constraints, and whether a fallback and audit record exist when the answer is no. Table 3 summarizes representative milestones through this lens. The comparison is not a leaderboard; the middle column reports claims from the cited sources, while the right column states the remaining action-authorization question. 

Figure 3 illustrates the boundary emphasized in this argument: the guardrail decision is positioned before a proposed model action becomes a hardware commitment. 

World models add another important dimension. **World models learn predictive representations of environment dynamics, future states, and possible outcomes** [14, 36–39, 61, 96]. Joint-embedding and physics-aligned approaches such as LeWorldModel and ABot-PhysWorld extend this line by learning predictive representations and physically plausible manipulation futures from visual data [17, 73]. For autonomous driving, 

GAIA-1, UniAD, DriveLM, LINGO-2, and recent driving VLA systems show adjacent trends toward generative, planning-oriented, and language-conditioned driving systems [25, 45, 46, 102, 110, 112, 115]. Recent surveys argue that world models are becoming a central component of robot learning, planning, simulation, and evaluation [43, 64]. 

The literature therefore shows a capability trend: AI systems are becoming more general, multimodal, predictive, data-intensive, and action-oriented [10, 15, 17, 43, 56, 73, 85, 86, 111]. However, this capability trend is not yet matched by a comparably standardized runtime authorization boundary. Many works measure task success, generalization, benchmark performance, or data-engine scale, while fewer address how a black-box model’s proposed action should be independently authorized under real-world uncertainty, as summarized in Tables 2 and 3. 

# **6 Silent Failures in Closed-Loop Autonomy** 

Classical software failures are often visible: a program crashes, a sensor disconnects, or a controller returns an error. Silent failures are different. They occur when a system continues operating while its internal representation of the world becomes unsafe. In closed-loop autonomy, this may happen when perception, prediction, planning, and control remain computationally active, but the assumptions flowing through the loop are wrong [5, 76, 95, 104]. Figure 4 expresses this as a physical commitment made from an invalid but internally accepted state. 

Several mechanisms can create silent failure modes: 

- **Sensor drift and corruption.** Inertial, visual, lidar, radar, GPS, and proprioceptive signals may degrade gradually or intermittently, creating false state estimates [76]. 

- **Occlusion and partial observability.** Robots and vehicles act under incomplete information. A model may infer a safe path where the unobserved region contains a person, obstacle, or constraint. 

- **Distribution shift.** Training data rarely captures all physical contexts, weather conditions, lighting patterns, object configurations, and human behaviors encountered during deployment [40, 87]. 

- **Hallucinated affordances.** Multimodal and actiongenerating models may infer that an object, surface, tool, path, or motion is usable when the physical preconditions are absent [6, 47, 65, 92, 104, 105]. 

- **Semantic-physical mismatch.** A command may be linguistically valid but physically invalid, unsafe, or operationally disallowed in the current state [55, 89]. 

- Silent failures matter because they can bypass both 

- human intuition and simple threshold alarms. The system 

8 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


Table 3: Selected empirical milestones and remaining action-authorization <u>questions.</u> 

|**System / line of work**|**Reported scale, result, or infrastructure milestone**|**Remaining authorization question**|
|---|---|---|
|Open X-Embodiment / RT-X<br>Octo|22 robots; 21 institutions; 527 skills; 160,266 tasks [86].<br>800k trajectories; 9 robot platforms [85].|Transfer does not establish runtime authorization.<br>Adaptation still leaves state validity external.|
|OpenVLA|7B parameters; 970k demonstrations; +16.5 points over<br>RT-2-X and +20.4 points over Diffusion Policy [56].|Task success is not auditable authorization.|
|_π_0 / FAST|VLA flow model plus action-tokenization work at large<br>robot-data scale [10, 88].|Better actions still require authorization.|
|World-model-guided<br>VLA<br>variants|WoVR: 39.95_→_69.2% LIBERO and 61.7_→_91.7% real robot;<br>RB-VLA: 32.5_→_77.5% ablation; EvoVLA: 38.5_→_14.8%<br>stage hallucination [7, 50, 69].|Reliability-adjacent metrics still differ from<br>authorization reliability.|
|LeRobot / SmolVLA|Open robotics stack; efficient VLA training and deployment<br>claims [15, 101].|Open deployment still needs evidence and audit<br>semantics.|
|GR00T N1|Open humanoid foundation model with dual-system archi-<br>tecture [84].|Humanoids increase cross-layer monitoring needs.|
|Gemini Robotics-ER 1.6|Reported embodied-reasoning and physical-safety-constraint<br>improvements [31].|Reasoning evidence still needs an execution<br>authority.|
|LeWorldModel<br>/<br>ABot-<br>PhysWorld|Predictive pixel representations; 14B model with 3M ma-<br>nipulation clips [17, 73].|Forecasting still needs constraint and recovery<br>checks.|
|NVIDIA Cosmos / Data Fac-<br>tory|Synthetic worlds, action simulation, data processing, RL,<br>and evaluation workflows [81, 83].|Infrastructure exposes cases; authorization decides<br>action.|
|Driving VLA systems|LinkVLA, StyleVLA, and CriticVLA report trajectory, style,<br>and critic-refinement advances [25, 110, 115].|Planning metrics do not replace runtime validation.|
|Action hallucination / Video-<br>Hallu|Physical-action and video-consistency failures [65, 104].|Plausibility is not physical commitment evidence.|
|RoboPAIR / RoboGuard|High attack success; RoboGuard reduces unsafe execution<br>from 92% to below 2.5% [89, 92].|Robot guardrails still need state and feasibility<br>checks.|
|Modular robot guardrails<br>SAFEL / EMBODYGUARD<br>/ IS-Bench|Action, decision, and human-centered safety modules [55].<br>942 scenarios across 13 LLMs; 161 interactive scenarios and<br>388 risks [71, 105].|Layering still needs deployment-wide authority.<br>Benchmarks need links to runtime enforcement.|
|Poly-Guard / AgentDoG|8 domains, 19 guardrail models; agentic-risk diagnosis [51,<br>67].|Needs extension to physical-action constraints.|
|Sensor<br>data|Estimated<br>world state<br>Black-box<br>world model<br>Proposed<br>physical action|**Runtime**<br>**authority**<br>Hardware<br>actuation|
||drift<br>occlusion<br>OOD<br>plausible<br>but unsafe||


Figure 3: Runtime action authorization boundary. The guardrail question arises before hardware commitment: should this proposed action be allowed in this state under these constraints? 


Figure 4: Silent physical-action failure. The system remains operational, but an invalid world state can still lead to a physically consequential commitment. 

may look normal until the physical consequence appears. In Physical AI, the safety-critical moment is often not the final actuator command, but the earlier moment when an invalid world state becomes accepted as a basis for action [76, 95, 104]. 

Recent robot safety work illustrates this problem. RoboPAIR reports that LLM-controlled robots can be jailbroken into harmful physical actions, including robot and autonomous-driving scenarios [92]. RoboGuard argues that LLM-enabled robots need contextual safety rules and conflict resolution beyond generic LLM filtering [89]. SAFEL/EMBODYGUARD and IS-Bench indicate that embodied safety failures often emerge during multi-step interaction, not in static final-state evaluation 

[71, 105]. Modular guardrail research frames foundationmodel-enabled robot safety across action safety, decision safety, and human-centered safety [55]. 

Multimodal hallucination research adds a complementary diagnosis. VideoHallu uses synthetic-video understanding tasks with abnormal physical and common-sense events to test whether vision-language models detect violations that are perceptually salient to humans [65]. Spatialsimulation work similarly treats hallucinated or phantom affordances as evidence that an agent’s representation of possible action can diverge from the environment’s actual affordance structure [6]. For Physical AI, these findings matter because a hallucination is no longer only a wrong description; it can become a candidate action. 

Historical autonomous-system incidents show why this is not only a rare-tail concern. The NTSB investigation of the 2018 Tempe crash involving an Uber developmental automated driving system identified inadequate safety risk assessment, oversight, and mechanisms for addressing automation complacency as contributing factors [79]. In 2023, California suspended Cruise’s driverless testing and deployment permits after determining that the vehicles created an unreasonable risk to public safety and that 

9 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


safety-related information had been misrepresented [16]. The same year, NHTSA Recall 23V-838 covered 2,031,220 Tesla vehicles because Autopilot controls were insufficient to prevent misuse [78]. GM later announced that it would no longer fund Cruise robotaxi development work, citing the time and resources needed to scale the program [29]. These examples are not VLA foundation-model deployments, but they are relevant operational analogues for Physical AI: failures in monitoring, operational boundaries, and runtime intervention can become safety events and regulatory actions. 

## **6.1 Confidence Is Not Safety** 

Modern neural networks often produce confidence scores, probabilities, logits, value estimates, or other internal signals that can be mistaken for safety evidence. The calibration literature warns against this interpretation. Deep models can be miscalibrated, overconfident, and sensitive to distribution shift [34, 87]. Bayesian approximations, dropout approximations, ensembles, and uncertainty-aware methods can improve reliability, but they do not eliminate the difference between epistemic uncertainty, aleatoric uncertainty, and action-level safety [24, 53, 60]. 

Out-of-distribution detection and robustness benchmarks provide partial remedies [40, 41, 62, 66, 68]. Adversarial-example research further provides evidence that high-confidence model behavior can be brittle under small or structured perturbations [30, 106]. Runtime perception-monitoring surveys connect these issues to safety-critical perception stacks; action authorization still calls for a decision layer that can block, modify, or escalate a proposed action [95]. 

In Physical AI, this distinction is crucial. A model may be confident that an action follows from its learned representation, while the representation itself is wrong. A robot policy may confidently choose a trajectory based on a false free-space map. A drone may confidently continue navigation after subtle sensor drift. A VLA model may confidently interpret an instruction but ignore a workspacespecific safety rule. In each case, the model’s confidence is a property of its internal computation, not a guarantee that the physical action is authorized [34, 76, 87, 89, 104]. 

This distinction matters for runtime authorization. Softmax or token confidence can indicate an internal model preference, but not physical safety or compliance with operational rules. Uncertainty estimates can indicate possible unreliability, but not the correct fallback action. OOD detectors can flag input mismatch with the training distribution, but not whether a specific proposed action is authorized. Task-success benchmarks can measure average performance on predefined scenarios, but not runtime safety under dynamic, evolving, or deployment-specific edge cases [24, 34, 40, 41, 53, 60, 62, 66, 68, 71, 87, 105]. 

The guardrail problem is an action authorization problem. A runtime system is often expected to decide 

what to do next: authorize, modify, defer, request human input, degrade gracefully, switch to a fallback controller, block the action, or log the event for evaluation [42, 55, 59, 89, 97]. 

# **7 Runtime Authority as an Independent Layer** 

The safety-control literature provides important tools for constraining actions. Safe reinforcement learning formalizes optimization under constraints [1, 26, 33, 90, 109, 117]. Control barrier functions, safety filters, reachability analysis, and predictive safety filters formalize the idea that actions should remain inside a safe set [4, 8, 22, 27, 44, 108]. Runtime assurance and shielding architectures similarly propose monitored autonomy, in which an advanced controller operates when acceptable and a trusted backup or enforcement mechanism intervenes when safety conditions are violated [3, 42, 59, 97]. 

These approaches are essential, but they do not by themselves cover the emerging Physical AI problem. Many assume access to system dynamics, low-level control variables, verified safe sets, or a limited autonomy stack [4, 27, 42, 44, 108]. By contrast, deployed Physical AI systems may incorporate black-box world models, heterogeneous hardware, learned planners, vendor-specific controllers, cloud-edge pipelines, and site-specific constraints. Runtime guardrails are therefore analyzed here as multi-dimensional interfaces across semantic, state, physical, spatial, operational, and audit evidence. 

The distinction is architectural rather than merely terminological. Semantic guardrails evaluate language, intent, content policy, and misuse [51, 67]. Safety filters and control barrier functions constrain low-level actions with respect to a modeled safe set [4, 27, 44, 108]. Runtime assurance monitors an operational controller and may switch to a trusted fallback [42, 59, 97]. _Physical action authorization_ is the interface between these ideas: it asks whether a proposed action from a learned, possibly black-box model should be executed in the current state, under the current constraints, with a decision that can be reconstructed later [55, 89, 95]. This framing makes the guardrail layer broader than content moderation, less controller-specific than a single safety filter, and more directly tied to deployment evidence than offline evaluation alone. 

## **7.1 Why Existing Guardrails Do Not Transfer Directly** 

Existing guardrail approaches do not transfer directly to Physical AI for four reasons. First, semantic validity is not physical validity: an instruction can be benign, coherent, and policy-compliant while still producing an infeasible or unsafe trajectory [55, 89, 104]. Second, controller-level safety filters often assume known dynam- 

10 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


Semantic guardrails: intent, prompt injection, harmful requests, human intent 

State-validity guardrails: sensor integrity, perception anomaly, state-estimate consistency 

Physical feasibility guardrails: kinematics, dynamics, collisions, velocity, payload, workspace envelope 

Spatial and operational guardrails: geofencing, restricted zones, fleet rules, operational policy 


Figure 5: Layered runtime authority. Semantic, state, physical, and operational checks are composed before the validated action and audit trace reach hardware. 

ics, explicit state variables, and well-defined safe sets, whereas black-box Physical AI systems may output plans, waypoints, code-like actions, latent actions, or naturallanguage-conditioned policies [4, 10, 44, 56, 88]. Third, runtime assurance assumes that the monitor can evaluate the active controller against trusted safety conditions; in Physical AI, the monitor also has to assess whether the state estimate itself is reliable enough to support the proposed action [42, 59, 76, 95]. Fourth, operational deployments introduce fleet-specific rules, restricted spaces, payload constraints, human-workflow constraints, and audit requirements that are not captured by generic model refusal policies [16, 78, 79]. 

The implication is not that existing methods are insufficient individually; it is that their assumptions require explicit composition. Physical AI guardrails can be studied as interfaces that connect semantic policy, state validity, physical feasibility, spatial constraints, fallback behavior, and audit evidence around the same proposed action [42, 55, 89, 97]. Figure 5 illustrates this layered interpretation. 

The architectural point is separation. A runtime guardrail ideally should not depend entirely on the same black-box model whose behavior it is evaluating [42, 55, 59, 89, 97]. This separation enables independent checks, deterministic rules, reproducible logs, and crossmodel comparison. It also supports evaluation workflows in which the foundation model, hardware platform, task policy, or deployment environment can change while the action-authorization interface remains consistent. 

Runtime guardrails may be hybrid. They may combine learned anomaly detection, formal constraints, geomet- 

ric reasoning, model predictive checks, semantic policy engines, temporal logic, and classical control monitors [4, 41, 44, 51, 68, 95, 108]. A key design principle is that the final authority over physical action should include inspectable constraints that are external to the generative model. 

Recent guardrail work can be read as a sequence of increasingly deployment-oriented assumptions. RoboGuard argues that LLM-enabled robots require contextual safety rules and conflict resolution beyond generic content filtering, and reports large reductions in unsafe plan execution under its experimental setup [89]. Modular guardrail work extends this point by arguing for multiple guardrail modules across action safety, decision safety, and humancentered safety in foundation-model-enabled robots [55]. These works are especially relevant to the Physical AI problem because they treat the model output as an object of mediation before robot execution. 

Action hallucination and multimodal hallucination benchmarks sharpen the failure mechanism. Action hallucination work argues that generative VLA policies can emit physically invalid actions because the learned action distribution and feasible robot behavior are not necessarily aligned [104]. VideoHallu provides evidence that multimodal models can fail to identify physical, logical, or common-sense violations in synthetic video understanding tasks [65]. Together, these works support the claim that plausibility, confidence, and perceptual fluency are not sufficient evidence for action authorization. 

Poly-Guard and AgentDoG contribute a different but complementary direction. Poly-Guard benchmarks guardrail behavior across eight safety-critical domains and 

11 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


reports that optimized adversarial attacks remain effective against advanced guardrail models [51]. AgentDoG moves from binary safe/unsafe labels toward trajectorylevel diagnosis of agentic risks and root causes [67]. These works make guardrails more contextual, policy-grounded, and auditable. Their limitation for Physical AI is not weakness; it is scope. Physical execution introduces additional evidence types: state validity, physical feasibility, spatial constraints, hardware limits, fallback behavior, and action-level audit records. 

# **8 Evaluation Under Dynamic Edge Cases** 

Evaluation is central to Physical AI because safety risk accumulates through interaction among model uncertainty, environment change, human behavior, and hardware constraints. General benchmarks are useful, but static benchmarks can miss failure modes that only emerge through closed-loop behavior. Embodied safety benchmarks therefore increasingly evaluate agents across multi-step scenarios, hazardous instructions, adversarial prompts, object interactions, context-dependent constraints, physicalconsistency errors, and trajectory-level risk diagnosis [65, 67, 71, 105]. 

For runtime guardrails, evaluation should measure more than task success. It should ask: 

- Did the system detect corrupted or insufficient state before action? 

- Did it block physically invalid actions even when the model was confident? 

- Did it enforce spatial, kinematic, and operational constraints consistently? 

- Did it degrade gracefully under uncertainty? 

- Did it produce auditable traces that explain why an action was authorized or rejected? 

- Did the same guardrail policy generalize across models, hardware, and environments? 

Rather than proposing a new benchmark or final protocol, this section identifies requirements that a comparative evaluation would need to satisfy. Existing benchmarks and simulator platforms illuminate important parts of the problem, but no single evaluation setup reviewed here covers the full runtime authorization pathway for Physical AI guardrails [67, 71, 74, 82, 105]. These requirements follow from the gaps between embodied safety benchmarks, simulator platforms, runtime assurance, uncertainty estimation, and guardrail datasets [42, 51, 87, 95]. Table 4 summarizes these requirements and the measurement problems that remain open. 

These requirements can be instantiated by illustrative failure classes rather than treated as a fixed benchmark 

suite. Examples include an occluded obstacle in a mobilerobot aisle, a stale perception frame, a hallucinated manipulation affordance, a restricted-zone violation, a payload or velocity-limit violation, an adversarial instruction that passes semantic checks, a late intervention, and an unsafe fallback [71, 76, 89, 92, 104, 105]. The point is not that this list is exhaustive; it shows the range of evidence types that runtime guardrail evaluation should cover. 

The requirements can be measured around the authorization record _ξt_ defined in Equation (2). A comparative study built around this record can compare models and guardrail layers without requiring that every system share the same internal architecture. 

Let a comparative evaluation contain _N_ authorization records _{ξi}_<sup>_N_</sup> _i_ =1<sup>.Let</sup><sup>_yi_=1denotethattheproposed</sup> action is valid under the evaluation oracle and _yi_ = 0 denote that it is invalid. Let _D_ 0 = _{i_ : _yi_ = 0 _}_ be the invalid-action set, _D_ 1 = _{i_ : _yi_ = 1 _}_ the valid-action set, and _I_ = _{_ modify _,_ block _,_ escalate _}_ the intervention decisions. Here _|D|_ denotes set cardinality and I[ _·_ ] denotes an indicator function. A primary safety metric is unsafeaction intervention rate: 


The corresponding operational-cost metric is false block rate, FBR = _|D_ 1 _|_<sup>_−_1 �</sup> _i∈D_ 1<sup>I[</sup><sup>_ρi∈I_],whichcaptures</sup> usability cost rather than direct safety prevention. For physical systems, timing is itself a safety variable. If _t_<sup>prop</sup> _i_ is the proposal time, _t_<sup>_ρ_</sup> _i_<sup>is the guardrail decision time,and</sup> _t_<sup>commit</sup> _i_ is the latest time before physical commitment, then pre-commit intervention rate is 


Finally, guardrails should be evaluated not only by binary decisions but also by residual violation severity. If _a_<sup>out</sup> _i_ is the action after guardrail intervention, _K_ is the number of evaluated constraints, and each normalized constraint is written as _c_ ˜ _k_ ( _a_<sup>out</sup> _i , si_ ) _≤_ 0, a residual violation score is 


Equations (10)–(12) are not meant to exhaust evaluation; they define a minimum quantitative core for comparing guardrails. Table 5 groups the quantitative core with the additional qualitative checks needed for deployment review. 

These metrics also have clear boundary cases. UAIR = 1 means every invalid proposed action received an intervention, while UAIR = 0 means none did. FBR = 0 means valid actions were not unnecessarily interrupted; a high FBR indicates an over-conservative guardrail. PCIR = UAIR when all interventions arrive before physical commitment, whereas PCIR _<_ UAIR indicates that 

12 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


Table 4: Evaluation requirements derived from the reviewed benchmark, simulator, and assurance literatures. 

|**Requirement**|**Literature or formal anchor**|**Open measurement problem**|
|---|---|---|
|State-reliability stress|Uncertainty, OOD, calibration, perception mon-<br>itoring [68, 76, 87, 95].|When is state evidence sufficient for this action?|
|Invalid-action intervention|Action hallucination, robot jailbreaks, embodied<br>guardrails [89, 92, 104].|Necessary block or over-conservative interruption?|
|Operational constraints|Autonomy incidents and site constraints [16, 78,<br>79].|How to compare heterogeneous deployment rules?|
|Pre-commit timing|Runtime assurance and physical commitment<br>[42, 97].|What counts as “before execution” across platforms?|
|Fallback correctness|Shielding and runtime enforcement [3, 42, 59].|How to score stop, modify, and escalation?|
|Cross-model / platform|Cross-embodiment policies, simulators, robot<br>datasets [10, 56, 85, 86].|How to compare without shared internals?|
|Audit completeness|Incident analysis and runtime records [16, 29,<br>79].|What is the minimal reconstructable record?|


Table 5: Compact metric families for Physical AI runtime <u>guardrail</u> evaluation. 

|**Metric family**|**Operational definition**|**Why it matters**|
|---|---|---|
|Intervention effectiveness|UAIR: invalid proposals interrupted.|Catches unsafe proposals.|
|Operational over-blocking|FBR: valid proposals interrupted.|Captures usability cost.|
|Pre-commit timing|PCIR and decision latency.|Detects late interventions.|
|State-validity sensitivity|Corrupt, stale, shifted, or inconsistent state<br>evidence.|Separates action safety from state trust.|
|Constraint coverage|Semantic, state, physical, temporal, spatial,<br>operational constraints.|Tests breadth beyond content filters.|
|Residual violation severity|RVS after intervention.|Measures remaining violation magnitude.|
|Fallback correctness|Block, modify, or escalation leads to safe<br>behavior.|Avoids unsafe recovery.|
|Audit completeness|Evidence, constraints, versions, reason codes.|Supports review and reproducibility.|


Table 6: Representative simulation <u>platforms</u> and their relationship to runtime action authorization. 

|**Simulator**<br>**/**<br>**platform**<br>**family**|**Primary contribution for evaluation**|**Remaining gap for guardrails**|
|---|---|---|
|NVIDIA Isaac Sim / Lab /<br>Gym|Physically based simulation, synthetic data, GPU<br>robot learning [74, 77, 82].|Scales testing; does not authorize actions.|
|Newton physics engine|GPU physics for robot learning on Warp/OpenUSD<br>[80].|Improves physics substrate, not runtime policy.|
|MuJoCo / Gazebo|Dynamics, contact-rich control, multi-robot experi-<br>mentation [57, 107].|Controller tests are not action authorization.|
|CARLA / AirSim|Driving and aerial simulation with sensors and envi-<br>ronments [19, 98].|Scenario tests lack deployment audit authority.|
|Habitat / AI2-THOR|Embodied navigation and indoor interaction [58,94].|Task completion is not physical validity.|
|SAPIEN / ManiSkill2|Manipulation and articulated-object benchmarks<br>[32, 113].|Needs feasibility, fallback, audit decisions.|


some interventions are too late to prevent execution. RVS = 0 means the post-guardrail action satisfies all measured constraints; larger values indicate residual violation magnitude. If _D_ 0 or _D_ 1 is empty, the corresponding rate should be reported as not applicable rather than zero. 

Simulation environments are therefore important, but their role should be stated precisely. They can generate edge cases, synthetic sensor data, software- or hardwarein-the-loop tests, and repeatable task conditions [19, 74, 82, 94, 98, 113]; they do not by themselves decide whether a black-box model’s proposed action should be authorized at runtime. Table 6 compares representative simulator families and the corresponding action-authorization gap. The right column is an interpretation of the authorization gap, not a claim made by the simulator papers themselves. 

Together, world models and simulation environments support a continuous-evidence workflow: offline scenario generation, runtime monitoring, edge-case discovery, and guardrail refinement [43, 64, 83, 95]. Figure 6 summarizes how benchmark evidence and deployment evidence can inform the same guardrail evaluation process. 

Offline tests can characterize model behavior before deployment, while runtime logs can reveal new edge cases during operation [67, 71, 95, 105]. As Physical AI systems become more general and more frequently updated, evaluation is better treated as a continuing deployment concern rather than a one-time benchmark result. 

13 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


Figure 6: Continuous evaluation loop. Offline benchmarks and runtime logs can feed the same guardrail evaluation process through authorization records. 

# **9 Synthesis: Action-Authorization Gap and Open Questions** 

The literature points to an action-authorization gap across model-centric, control-centric, and safety-centric work. Model-centric work focuses on capabilities, datasets, architectures, and training [10, 56, 85, 86, 88]. Robotics and control work focuses on hardware, dynamics, and task performance [4, 27, 44, 108]. Safety research contributes formal methods, uncertainty quantification, runtime monitoring, and evaluation protocols [28, 42, 52, 87, 95, 103]. The open problem is how to connect these perspectives into a repeatable method for authorizing physical action under uncertainty. 

### **Current Literature Gap** 

Existing surveys and technical works cover VLA models, world models, safety filters, runtime assurance, OOD detection, and embodied robot safety [33, 42, 43, 55, 64, 72, 93, 95, 114]. A remaining assurance category is model-independent runtime authorization for translating heterogeneous Physical AI outputs into validated, constrained, auditable physical actions. The gap is not a lack of safety techniques; it is the limited availability of a common authorization boundary that composes these techniques around proposed physical actions. 

## **9.1 Fragmented Safety Assumptions** 

Classical control methods often assume well-specified dynamics and safe sets [4, 27, 44, 108]. Foundation-model works often evaluate success rates and generalization [10, 56, 85, 86, 88]. LLM and multimodal safety research often focuses on harmful instructions, hallucination, jailbreaks, and policy compliance [51, 65, 67, 92]. Physical AI deployments bring these concerns together: semantic policy, state reliability, and deterministic physical constraints. 

## **9.2 Limited Model-Independent Runtime Authority** 

interface for proposed actions, state evidence, operational constraints, and authorization decisions would make it easier to compare systems without forcing every model or robot into the same internal representation. This supports research reproducibility, cross-model evaluation, system comparison, and heterogeneous deployments. 

## **9.3 Insufficient Treatment of Silent Failures** 

Terms such as hallucination, distribution shift, OOD detection, perception error, and adversarial attack describe parts of the problem [6, 41, 65, 68, 76, 87, 104]. Silent failure provides a deployment-oriented framing: the system is still running, still confident, and still acting, but the action is grounded in an invalid state. This framing connects model-level and perception-level errors to physical consequences. 

## **9.4 Limited Auditability for Physical Action** 

Physical AI systems are easier to evaluate when records explain why actions were allowed, modified, blocked, or escalated. Auditability supports scientific reproducibility, benchmarking, incident analysis, operational accountability, and regulatory readiness, especially when failures involve interacting perception, planning, control, and organizational factors [16, 29, 42, 78, 79]. Without structured traces, it becomes difficult to determine whether a failure came from perception, model reasoning, guardrail configuration, controller behavior, or the environment. 

## **9.5 Open Questions** 

The surveyed literature motivates several open questions for runtime action authorization. 

1. **Action interface.** What is the right abstraction for a proposed physical action across drones, autonomous mobile robots, vehicles, manipulators, and humanoids? 

2. **State reliability.** How can runtime systems quantify whether the current world representation is reliable enough for a specific action? 

3. **Constraint composition.** How should semantic, spatial, kinematic, operational, and safety constraints be combined without creating brittle rule systems? 

4. **Guardrail evaluation.** What comparative evaluation methods can measure whether a guardrail layer reduces or detects silent failures beyond ordinary task completion? 

5. **Cross-platform learning.** How can deployment logs and edge cases improve guardrail policies while preserving model independence and auditability? 

Many safety interventions are embedded inside a specific model, robot, or task [55, 67, 89]. A model-independent 

14 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


6. **Runtime governance.** When should a system block, modify, defer, or escalate a proposed action, and how should that decision be explained? 

This synthesis complements advances in model training and control. Better world models may reduce some errors, yet open-world conditions make it difficult to treat any model as perfect [17, 43, 64, 73]. Better controllers can reduce some violations, while upstream state validity and task intent call for separate evidence [4, 44, 76, 108]. Runtime guardrails address the intermediate event: a black-box Physical AI system proposes an action, and the surrounding system evaluates whether that action is allowed. 

## **9.6 Falsifiable Implications** 

The main inference is falsifiable. It would be weakened if future Physical AI systems routinely exposed certified action representations, reliable state-validity evidence, formally composable constraints, and auditable authorization decisions as part of the model or controller interface. It would also be weakened if empirical benchmarks showed that model-internal confidence, low-level safety filters, or semantic guardrails alone consistently reduce or prevent silent physical-action failures across heterogeneous robots, vehicles, drones, environments, and operational policies. Conversely, repeated findings that plausible model outputs benefit from external state, feasibility, spatial, temporal, or audit checks would strengthen the case for an independent runtime authorization layer. 

# **10 Assurance Implications and Minimal Event Schema** 

A technical implication is that guardrail evaluation should measure intervention quality, not only task success [67, 71, 105]. Researchers can treat the authorization event as a concrete unit of analysis: whether unsafe, invalid, or poorly grounded actions are detected, modified, blocked, or escalated before execution. System architects can separate this interface from model training, lowlevel control, and hardware-specific safety mechanisms [42, 55, 97]. Deployment reviews can ask whether the system produces independent evidence about why actions were allowed or rejected under uncertainty [16, 29, 79]. 

The contribution is a structured map of the gap between model capability and physical-action assurance: the failure mode, the relevant literatures, the minimum formal interface, evaluation requirements, representative metric families, and the evidence needed to compare guardrail layers across platforms. It is not a new standard or a complete guardrail design. 

## **10.1 Minimal Authorization Event Schema** 

A minimal unit for comparing runtime guardrails is the authorization event. For each proposed physical action, a structured record can be defined independently of the internal representation of the policy, world model, simulator, or controller. Such a record does not prescribe a software API or implementation standard; it defines the information needed to evaluate whether an action was authorized, modified, blocked, escalated, or routed to fallback. 

The schema is deliberately limited to fields that recur across platforms. Different platforms may instantiate the fields differently: an aerial system may emphasize geofences, energy margins, and GNSS integrity; a mobile robot may emphasize clearance, occupancy maps, and human proximity; a manipulator may emphasize contact constraints, payload, workspace limits, and grasp feasibility. The common point is that the unit of comparison is not the model architecture or the controller alone, but the authorization event that links a proposed action to state evidence, active constraints, runtime decision, fallback, and auditability. 

# **11 Limitations and Threats to Validity** 

The analysis is limited to runtime guardrails and action authorization for black-box Physical AI systems. It does not attempt to survey the entire Physical AI literature, nor does it provide a complete treatment of robotics standards, simulation infrastructure, certification processes, or general AI ethics. The source selection is centered on the action-authorization pathway; therefore, some adjacent literatures are represented only when they directly clarify the connection between model output, state evidence, physical constraints, and execution. 

Several limitations follow from this scope. First, the formalization is intentionally minimal and abstracts away many hardware-specific dynamics, perception-stack details, and organizational deployment processes. Second, the autonomous-vehicle incidents discussed above are used as operational analogues for assurance failures in physical autonomy; they should not be read as direct examples of VLA or world-model foundation systems. Third, the review derives evaluation requirements and metric families but does not introduce a new benchmark or empirical evaluation of a guardrail implementation. Fourth, runtime guardrails are not presented as a complete safety solution. They are one assurance layer among model design, perception robustness, classical control, hardware redundancy, human oversight, and organizational safety processes. 

There are also technical boundary conditions. Runtime authorization cannot guarantee safety when observabil- 

15 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


Table 7: Minimal authorization event schema for comparing runtime <u>guardrails.</u> 

|**Field**|**Meaning**|**Why it matters**|
|---|---|---|
|Observation context|Sensor inputs, history, timestamp, platform con-<br>text.|What evidence was available.|
|Proposed action|Command, waypoint, plan, tool action, or trajec-<br>tory fragment.|Separates proposal from execution.|
|State estimate|Objects, agents, maps, robot state, environment<br>state.|States what authorization depends on.|
|State-validity evidence|Sensor health, latency, uncertainty, OOD, consis-<br>tency flags.|Separates unsafe action from unreliable state.|
|Active constraints|Physical, semantic, spatial, temporal, operational,<br>policy constraints.|Defines the evaluation boundary.|
|Authorization decision|Authorize, modify, block, escalate, or fallback.|Records runtime judgment.|
|Fallback or modification|Replacement action, safe stop, backup controller,<br>human escalation.|Captures recovery semantics.|
|Timing evidence|Proposal, decision, commitment times, latency.|Checks pre-commit intervention.|
|Audit trace|Versions, constraint IDs, reason codes, evidence<br>pointers.|Supports incident analysis and comparison.|


ity is poor, constraints are incomplete, the fallback behavior is underspecified, or the physical environment is adversarial. Formal guarantees from safety filters, CBFs, or runtime assurance can weaken when state estimates are stale, when the dynamics model is wrong, or when the action representation exposed by the learned policy is not the representation assumed by the safety proof [4, 42, 76, 87, 108]. Authorization latency can itself become hazardous: a correct block that arrives after physical commitment is operationally insufficient. Finally, fallback is not automatically safe; safe stop, human escalation, and backup control each require their own validity conditions. 

These limitations are also useful boundary conditions. A runtime guardrail layer should not replace certified control, verified hardware limits, operator training, incident response, or regulatory compliance. Its role is narrower and more specific: to provide a model-independent authorization boundary where proposed physical actions can be checked, modified, blocked, escalated, and logged before they become hardware commitments. 

**Selection validity.** The source selection is curated around runtime action authorization and therefore may underrepresent adjacent work whose relevance is indirect, such as broader robotics standards, human factors, or simulation infrastructure. 

**Construct validity.** The term “silent failure” groups several mechanisms: hallucination, OOD behavior, sensor drift, state-estimation error, and invalid affordance inference. This grouping is useful for deployment analysis, but each mechanism may call for different instrumentation and mitigation. 

**External validity.** Physical AI deployments vary across robots, vehicles, drones, factories, warehouses, hospitals, roads, and homes. A guardrail taxonomy that is useful across domains still needs domain-specific constraints, fallback policies, and evidence thresholds. 

**Temporal validity.** The literature is moving quickly. New VLA models, world models, robot benchmarks, and guardrail datasets may narrow parts of the gap identified here. The claim should therefore be read as an argument 

about an assurance category, not a fixed statement about any single model generation. 

**Evidence validity.** The autonomous-vehicle incidents discussed above provide operational analogues for runtime monitoring and boundary failures. They are not direct evidence about current VLA or world-model-based robotic systems, and they are used only as examples of how physical autonomy failures can create safety and regulatory consequences. 

# **12 Conclusion** 

The main conclusion is that Physical AI safety is not only a model-training problem, a controller problem, or a simulation problem. It is also an authorization problem. Before a learned system’s proposed action becomes a physical commitment, the surrounding autonomy stack should provide independent evidence that the state is valid, the action is feasible, operational constraints are satisfied, fallback is available, and the decision is auditable. 

The critical failure mode is often silent: a system acts confidently on a corrupted or incomplete world state. The literature provides many ingredients for addressing this problem, including safe control, runtime assurance, shielding, uncertainty estimation, OOD detection, embodied safety benchmarks, neural-network verification, simulation infrastructure, and robot-specific guardrails. One unresolved task is their integration into a runtime authority that evaluates and records physical-action decisions before execution. 

Three implications follow. Researchers should evaluate authorization events, not only task success. System builders should separate model proposal from runtime authority, especially when models, hardware, policies, and environments change independently. Safety teams and regulators can use reconstructable action records to examine why actions were authorized, modified, blocked, or escalated under uncertainty. 

Runtime guardrails can therefore be studied as assur- 

16 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


ance mechanisms for the transition from AI that predicts the world to AI that acts in it. 

# **References** 

- [1] Joshua Achiam, David Held, Aviv Tamar, and Pieter Abbeel. Constrained policy optimization. In _Proceedings of the 34th International Conference on Machine Learning_ , pages 22–31, 2017. 

- [2] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, et al. Do as i can, not as i say: Grounding language in robotic affordances, 2022. 

- [3] Mohammed Alshiekh, Roderick Bloem, Rüdiger Ehlers, Bettina Könighofer, Scott Niekum, and Ufuk Topcu. Safe reinforcement learning via shielding. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 32, 2018. 

- [4] Aaron D. Ames, Samuel Coogan, Magnus Egerstedt, Gennaro Notomista, Koushil Sreenath, and Paulo Tabuada. Control barrier functions: Theory and applications. In _2019 18th European Control Conference_ , pages 3420–3431, 2019. doi: 10.23919/ECC.2019.8796030. 

- [5] Dario Amodei, Chris Olah, Jacob Steinhardt, Paul Christiano, John Schulman, and Dan Mane. Concrete problems in ai safety, 2016. 

- [6] Javier Argota Sánchez-Vaquerizo and Luis Borunda Monsivais. From particles to agents: Hallucination as a metric for cognitive friction in spatial simulation. In _Proceedings of Navigating the Disruptive and Wild Landscape of Large Language Models and Agentic AI, AlpCHI 2026 Workshop on Human Cognition, AI, and the Future of HCI_ , 2026. URL `https://arxiv.org/abs/2601.21977` . 

- [7] Vaidehi Bagaria, Bijo Sebastian, and Nirav Kumar Patel. Recursive belief vision language action models, 2026. URL `https://arxiv.org/abs/2602. 20659` . 

- [8] Felix Berkenkamp, Matteo Turchetta, Angela P. Schoellig, and Andreas Krause. Safe model-based reinforcement learning with stability guarantees. In _Advances in Neural Information Processing Systems_ , 2017. 

- [9] Homanga Bharadhwaj, Jay Vakil, Mohit Sharma, Abhinav Gupta, Shubham Tulsiani, and Vikash Kumar. Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking, 2023. 

- [10] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control, 2024. 

- [11] Konstantinos Bousmalis, Giulia Vezzani, Dushyant Rao, Coline Devin, Alex X. Lee, Maria Bauza, Todor Davchev, Yuxiang Zhou, Agrim Gupta, Ashwin Raju, et al. Robocat: A self-improving generalist agent for robotic manipulation, 2023. 

- [12] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. RT-1: Robotics transformer for real-world control at scale, 2022. 

- [13] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. RT-2: Vision-language-action models transfer web knowledge to robotic control, 2023. 

- [14] Jake Bruce, Michael D. Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, et al. Genie: Generative interactive environments, 2024. 

- [15] Remi Cadene, Simon Aliberts, Francesco Capuano, Michel Aractingi, Adil Zouitine, Pepijn Kooijmans, Jade Choghari, Martino Russi, Caroline Pascal, Steven Palma, Mustafa Shukor, Jess Moss, Alexander Soare, Dana Aubakirova, Quentin Lhoest, Quentin Gallouédec, and Thomas Wolf. LeRobot: An open-source library for end-to-end robot learning, 2026. URL `https://arxiv.org/abs/2602. 22818` . 

- [16] California Department of Motor Vehicles. DMV statement on Cruise LLC suspension, 2023. URL `https : / / www . dmv . ca . gov / portal / news - and - media / dmv - statement - on - cruise - llc - suspension/` . 

- [17] Yuzhi Chen, Ronghan Chen, Dongjie Huo, Yandan Yang, Dekang Qi, Haoyun Liu, Tong Lin, Shuang Zeng, Junjin Xiao, Xinyuan Chang, Feng Xiong, Xing Wei, Zhiheng Ma, and Mu Xu. ABotPhysWorld: Interactive world foundation model for robotic manipulation with physics alignment, 2026. URL `https://arxiv.org/abs/2603.23376` . 

- [18] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion, 2023. 

- [19] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. CARLA: An 

17 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


open urban driving simulator, 2017. URL `https: //arxiv.org/abs/1711.03938` . 

- [20] Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, et al. PaLM-E: An embodied multimodal language model, 2023. 

- [21] Frederik Ebert, Yanlai Yang, Karl Schmeckpeper, Bernadette Bucher, Georgios Georgakis, Kostas Daniilidis, Chelsea Finn, and Sergey Levine. Bridge data: Boosting generalization of robotic skills with cross-domain datasets, 2021. 

- [22] Jaime F. Fisac, Anayo K. Akametalu, Melanie N. Zeilinger, Shahab Kaynama, Jeremy Gillula, and Claire J. Tomlin. Bridging hamilton-jacobi safety analysis and reinforcement learning. In _2019 International Conference on Robotics and Automation_ , pages 8550–8556, 2019. doi: 10.1109/ICRA.2019. 8794107. 

- [23] Zipeng Fu, Tony Z. Zhao, and Chelsea Finn. Mobile ALOHA: Learning bimanual mobile manipulation with low-cost whole-body teleoperation, 2024. 

- [24] Yarin Gal and Zoubin Ghahramani. Dropout as a bayesian approximation: Representing model uncertainty in deep learning. In _Proceedings of the 33rd International Conference on Machine Learning_ , pages 1050–1059, 2016. 

- [25] Yuan Gao, Dengyuan Hua, Mattia Piccinini, Finn Rasmus Schäfer, Korbinian Moller, Lin Li, and Johannes Betz. StyleVLA: Driving style-aware vision language action model for autonomous driving, 2026. URL `https://arxiv.org/abs/2603.09482` . 

- [26] Javier García and Fernando Fernández. A comprehensive survey on safe reinforcement learning. _Journal of Machine Learning Research_ , 16(1):1437– 1480, 2015. URL `https://jmlr.org/papers/v16/ garcia15a.html` . 

- [27] Kunal Garg, James Usevitch, Joseph Breeden, Mitchell Black, Devansh Agrawal, Hardik Parwana, and Dimitra Panagou. Advances in the theory of control barrier functions: Addressing practical challenges in safe control synthesis for autonomous and robotic systems. _Annual Reviews in Control_ , 57: 100945, 2024. doi: 10.1016/j.arcontrol.2024.100945. 

- [28] Timon Gehr, Matthew Mirman, Dana DrachslerCohen, Petar Tsankov, Swarat Chaudhuri, and Martin Vechev. AI2: Safety and robustness certification of neural networks with abstract interpretation. In _2018 IEEE Symposium on Security and Privacy_ , pages 3–18, 2018. doi: 10.1109/SP.2018.00058. 

- [29] General Motors. GM to refocus autonomous driving development on personal vehicles, 2024. URL `https : / / news . gm . com / home . detail . html / Pages/news/us/en/2024/dec/1210-gm.html` . 

- [30] Ian J. Goodfellow, Jonathon Shlens, and Christian Szegedy. Explaining and harnessing adversarial examples. In _International Conference on Learning Representations_ , 2015. 

- [31] Laura Graesser and Peng Xu. Gemini Robotics-ER 1.6: Powering real-world robotics tasks through enhanced embodied reasoning. Google DeepMind technical blog, 2026. URL `https://deepmind.google/ blog/gemini-robotics-er-1-6/` . Google DeepMind technical blog, accessed May 13, 2026. 

- [32] Jiayuan Gu, Fanbo Xiang, Xuanlin Li, Zhan Ling, Xiqiang Liu, Tongzhou Mu, Yihe Tang, Stone Tao, Xinyue Wei, Yunchao Yao, Xiaodi Yuan, Pengwei Xie, Zhiao Huang, Rui Chen, and Hao Su. ManiSkill2: A unified benchmark for generalizable manipulation skills, 2023. URL `https://arxiv.org/ abs/2302.04659` . 

- [33] Shangding Gu, Long Yang, Yali Du, Guang Chen, Florian Walter, Jun Wang, and Alois Knoll. A review of safe reinforcement learning: Methods, theories, and applications. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 46(12): 11216–11235, 2024. doi: 10.1109/TPAMI.2024. 3457538. 

- [34] Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q. Weinberger. On calibration of modern neural networks. _Proceedings of the 34th International Conference on Machine Learning_ , pages 1321–1330, 2017. 

- [35] Yanjiang Guo, Tony Lee, Lucy Xiaoyang Shi, Jianyu Chen, Percy Liang, and Chelsea Finn. VLAW: Iterative co-improvement of vision-language-action policy and world model, 2026. URL `https:// arxiv.org/abs/2602.12063` . 

- [36] David Ha and Jürgen Schmidhuber. World models, 2018. 

- [37] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels, 2019. 

- [38] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. In _International Conference on Learning Representations_ , 2020. 

- [39] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. URL `https://arxiv. org/abs/2301.04104` . 

18 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


- [40] Dan Hendrycks and Thomas Dietterich. Benchmarking neural network robustness to common corruptions and perturbations. In _International Conference on Learning Representations_ , 2019. 

- [41] Dan Hendrycks and Kevin Gimpel. A baseline for detecting misclassified and out-of-distribution examples in neural networks, 2017. 

- [42] Kerianne L. Hobbs, Mark L. Mote, Matthew Abate, Samuel Coogan, and Eric Feron. Run time assurance for safety-critical systems: An introduction to safety filtering approaches for complex control systems. _IEEE Control Systems Magazine_ , 43(2):28–65, 2023. doi: 10.1109/MCS.2023.3234380. 

- [43] Bohan Hou, Gen Li, Jindou Jia, Tuo An, Xinying Guo, Sicong Leng, Haoran Geng, Yanjie Ze, Tatsuya Harada, Philip Torr, et al. World model for robot learning: A comprehensive survey, 2026. 

- [44] Kai-Chieh Hsu, Haimin Hu, and Jaime F. Fisac. The safety filter: A unified view of safety-critical control in autonomous systems. _Annual Review of Control, Robotics, and Autonomous Systems_ , 7:47–72, 2024. doi: 10.1146/annurev-control-071723-102940. 

- [45] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. GAIA-1: A generative world model for autonomous driving, 2023. 

- [46] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. Planning-oriented autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 17853–17862, 2023. 

- [47] Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, and Li Fei-Fei. Voxposer: Composable 3d value maps for robotic manipulation with language models, 2023. 

- [48] Sicong Jiang, Zilin Huang, Kangan Qian, Ziang Luo, Tianze Zhu, Yang Zhong, Yihong Tang, Menglin Kong, Yunlong Wang, Siwen Jiao, et al. A survey on vision-language-action models for autonomous driving, 2025. 

- [49] Yunfan Jiang, Agrim Gupta, Zichen Zhang, Guanzhi Wang, Yongqiang Dou, Yanjun Chen, Li Fei-Fei, Anima Anandkumar, Yuke Zhu, and Linxi Fan. VIMA: General robot manipulation with multimodal prompts, 2022. 

- [50] Zhennan Jiang, Shangqing Zhou, Yutong Jiang, Zefang Huang, Mingjie Wei, Yuhui Chen, Tianxing Zhou, Zhen Guo, Hao Lin, Quanlu Zhang, Yu Wang, Haoran Li, Chao Yu, and Dongbin Zhao. WoVR: World models as reliable simulators for post-training 

VLA policies with RL, 2026. URL `https://arxiv. org/abs/2602.13977` . 

- [51] Mintong Kang, Zhaorun Chen, Chejian Xu, Jiawei Zhang, Chengquan Guo, Minzhou Pan, Ivan Revilla, Yu Sun, and Bo Li. Poly-Guard: Massive multidomain safety policy-grounded guardrail dataset. In _Advances in Neural Information Processing Systems, Datasets and Benchmarks Track_ , 2025. URL `https: //openreview.net/forum?id=mORzRZaqT4` . 

- [52] Guy Katz, Clark Barrett, David L. Dill, Kyle Julian, and Mykel J. Kochenderfer. Reluplex: An efficient smt solver for verifying deep neural networks. In _International Conference on Computer Aided Verification_ , pages 97–117. Springer, 2017. doi: 10.1007/978-3-319-63387-9_5. 

- [53] Alex Kendall and Yarin Gal. What uncertainties do we need in bayesian deep learning for computer vision? In _Advances in Neural Information Processing Systems_ , 2017. 

- [54] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. DROID: A large-scale in-the-wild robot manipulation dataset, 2024. 

- [55] Joonkyung Kim, Wenxi Chen, Davood Soleymanzadeh, Yi Ding, Xiangbo Gao, Zhengzhong Tu, Ruqi Zhang, Fan Fei, Sushant Veer, Yiwei Lyu, Minghui Zheng, and Yan Gu. Modular safety guardrails are necessary for foundation-model-enabled robots in the real world, 2026. URL `https://arxiv.org/ abs/2602.04056` . 

- [56] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. OpenVLA: An open-source vision-languageaction model, 2024. 

- [57] Nathan Koenig and Andrew Howard. Design and use paradigms for Gazebo, an open-source multirobot simulator. In _2004 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 2149–2154, 2004. doi: 10.1109/IROS.2004.1389727. 

- [58] Eric Kolve, Roozbeh Mottaghi, Winson Han, Eli VanderBilt, Luca Weihs, Alvaro Herrasti, Matt Deitke, Kiana Ehsani, Daniel Gordon, Yuke Zhu, Aniruddha Kembhavi, Abhinav Gupta, and Ali Farhadi. AI2-THOR: An interactive 3d environment for visual AI, 2017. URL `https://arxiv. org/abs/1712.05474` . 

- [59] Bettina Könighofer, Roderick Bloem, Rüdiger Ehlers, and Christian Pek. Correct-by-construction runtime enforcement in AI – a survey, 2022. 

19 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


- [60] Balaji Lakshminarayanan, Alexander Pritzel, and Charles Blundell. Simple and scalable predictive uncertainty estimation using deep ensembles. In _Advances in Neural Information Processing Systems_ , 2017. 

- [61] Yann LeCun. A path towards autonomous machine intelligence. OpenReview manuscript, 2022. URL `https://openreview.net/forum?id=BZ5a1rkVsf` . 

- [62] Kimin Lee, Kibok Lee, Honglak Lee, and Jinwoo Shin. A simple unified framework for detecting outof-distribution samples and adversarial attacks. In _Advances in Neural Information Processing Systems_ , 2018. 

- [63] Martin Leucker and Christian Schallhart. A brief account of runtime verification. _The Journal of Logic and Algebraic Programming_ , 78(5):293–303, 2009. doi: 10.1016/j.jlap.2008.08.004. 

- [64] Xinqing Li, Xin He, Le Zhang, Min Wu, Xiaoli Li, and Yun Liu. A comprehensive survey on world models for embodied ai, 2025. 

- [65] Zongxia Li, Xiyang Wu, Guangyao Shi, Yubin Qin, Hongyang Du, Tianyi Zhou, Dinesh Manocha, and Jordan Lee Boyd-Graber. VideoHallu: Evaluating and mitigating multi-modal hallucinations on synthetic video understanding. In _Advances in Neural Information Processing Systems_ , 2025. URL `https: //openreview.net/forum?id=NoC9HT7Kf7` . 

- [66] Shiyu Liang, Yixuan Li, and R. Srikant. Enhancing the reliability of out-of-distribution image detection in neural networks. In _International Conference on Learning Representations_ , 2018. 

- [67] Dongrui Liu, Qihan Ren, Chen Qian, Shuai Shao, Yuejin Xie, Yu Li, Zhonghao Yang, Haoyu Luo, Peng Wang, Qingyu Liu, Binxin Hu, Ling Tang, Jilin Mei, Dadi Guo, Leitao Yuan, Junyao Yang, Guanxu Chen, Qihao Lin, Yi Yu, Bo Zhang, Jiaxuan Guo, Jie Zhang, Wenqi Shao, Huiqi Deng, Zhiheng Xi, Wenjie Wang, Wenxuan Wang, Wen Shen, Zhikai Chen, Haoyu Xie, Jialing Tao, Juntao Dai, Jiaming Ji, Zhongjie Ba, Linfeng Zhang, Yong Liu, Quanshi Zhang, Lei Zhu, Zhihua Wei, Hui Xue, Chaochao Lu, Jing Shao, and Xia Hu. AgentDoG: A diagnostic guardrail framework for ai agent safety and security, 2026. URL `https: //arxiv.org/abs/2601.18491` . Code and models: `https://github.com/AI45Lab/AgentDoG` . 

- [68] Weitang Liu, Xiaoyun Wang, John D. Owens, and Yixuan Li. Energy-based out-of-distribution detection. In _Advances in Neural Information Processing Systems_ , volume 33, pages 21464–21475, 2020. 

- [69] Zeting Liu, Zida Yang, Zeyu Zhang, and Hao Tang. EvoVLA: Self-evolving vision-language-action model, 2025. URL `https://arxiv.org/abs/2511. 16166` . 

- [70] Qian Long, Yueze Wang, Jiaxi Song, Junbo Zhang, Peiyan Li, Wenxuan Wang, Yuqi Wang, Haoyang Li, Shaoxuan Xie, Guocai Yao, Hanbo Zhang, Xinlong Wang, Zhongyuan Wang, Xuguang Lan, Huaping Liu, and Xinghang Li. Scaling world model for hierarchical manipulation policies, 2026. URL `https://arxiv.org/abs/2602.10983` . 

- [71] Xiaoya Lu, Zeren Chen, Xuhao Hu, Yijin Zhou, Weichen Zhang, Dongrui Liu, Lu Sheng, and Jing Shao. IS-Bench: Evaluating interactive safety of vlmdriven embodied agents in daily household tasks. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 40, pages 35680–35688, 2026. doi: 10.1609/aaai.v40i42.40880. 

- [72] Yueen Ma, Zixing Song, Yuzheng Zhuang, Jianye Hao, and Irwin King. A survey on vision-languageaction models for embodied ai, 2024. 

- [73] Lucas Maes, Quentin Le Lidec, Damien Scieur, Yann LeCun, and Randall Balestriero. LeWorldModel: Stable end-to-end joint-embedding predictive architecture from pixels, 2026. URL `https: //arxiv.org/abs/2603.19312` . 

- [74] Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, and Gavriel State. Isaac Gym: High performance GPU-based physics simulation for robot learning, 2021. URL `https://arxiv.org/abs/ 2108.10470` . 

- [75] Ajay Mandlekar, Soroush Nasiriany, Bowen Wen, Iretiayo Akinola, Yashraj Narang, Linxi Fan, Yuke Zhu, and Dieter Fox. Mimicgen: A data generation system for scalable robot learning using human demonstrations, 2023. 

- [76] Francisco Matos, Jorge Bernardino, João Durães, and João Cunha. A survey on sensor failures in autonomous vehicles: Challenges and solutions. _Sensors_ , 24(16):5108, 2024. doi: 10.3390/s24165108. 

- [77] Mayank Mittal, Kelly Guo, Gavriel State, Spencer Huang, et al. Isaac Lab: A GPU accelerated simulation framework for multi-modal robot learning. NVIDIA Research publication, 2025. URL `https: / / research . nvidia . com / publication / 2025 - 09_isaac-lab-gpu-accelerated-simulationframework - multi - modal - robot - learning` . NVIDIA Research publication. 

- [78] National Highway Traffic Safety Administration. Part 573 safety recall report 23v-838: Autopilot 

20 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


controls insufficient to prevent misuse, 2023. URL `https://static.nhtsa.gov/odi/rcl/2023/ RCLRPT-23V838-8276.PDF` . 

- [79] National Transportation Safety Board. Collision between vehicle controlled by developmental automated driving system and pedestrian, tempe, arizona, march 18, 2018. Technical Report NTSB/HAR-19/03, National Transportation Safety Board, 2019. URL `https://www. ntsb . gov / investigations / AccidentReports / Reports/HAR1903.pdf` . 

- [80] NVIDIA. Newton physics engine. NVIDIA Developer documentation, 2025. URL `https : / / developer.nvidia.com/newton-physics` . Developer documentation. 

- [81] NVIDIA. NVIDIA and global robotics leaders take physical AI to the real world. NVIDIA press release, 2026. URL `https : / / nvidianews . nvidia . com / _gallery / download _ pdf / 69b86b823d6332366cc17dcd/` . NVIDIA press release, March 16, 2026. 

- [82] NVIDIA. NVIDIA Isaac Sim: Robotics simulation and synthetic data generation. NVIDIA Developer documentation, 2026. URL `https://developer. nvidia.com/isaac/sim` . NVIDIA Developer documentation, accessed May 12, 2026. 

- [83] NVIDIA. NVIDIA announces open physical AI data factory blueprint to accelerate robotics, vision AI agents and autonomous vehicle development. NVIDIA press release, 2026. URL `https : / / nvidianews . nvidia . com / news / nvidia- announces- open- physical- ai- datafactory-blueprint-to-accelerate-roboticsvision-ai-agents-and-autonomous-vehicledevelopment` . NVIDIA press release, March 16, 2026. 

- [84] NVIDIA, Johan Bjorck, Fernando Castaneda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, et al. GR00T N1: An open foundation model for generalist humanoid robots, 2025. 

- [85] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy, 2024. 

- [86] Open X-Embodiment Collaboration. Open x- embodiment: Robotic learning datasets and RT-X models, 2023. 

- [87] Yaniv Ovadia, Emily Fertig, Jie Ren, Zachary Nado, D. Sculley, Sebastian Nowozin, Joshua V. Dillon, Balaji Lakshminarayanan, and Jasper Snoek. Can 

you trust your model’s uncertainty? evaluating predictive uncertainty under dataset shift. In _Advances in Neural Information Processing Systems_ , pages 13969–13980, 2019. 

- [88] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. FAST: Efficient action tokenization for vision-language-action models, 2025. 

- [89] Zachary Ravichandran, Alexander Robey, Vijay Kumar, George J. Pappas, and Hamed Hassani. Safety guardrails for llm-enabled robots. _IEEE Robotics and Automation Letters_ , 2026. doi: 10.1109/LRA. 2026.3667488. URL `https://arxiv.org/abs/ 2503.07885` . 

- [90] Alex Ray, Joshua Achiam, and Dario Amodei. Benchmarking safe exploration in deep reinforcement learning. _OpenAI technical report_ , 2019. URL `https://cdn.openai.com/safexp-short.pdf` . 

- [91] Scott Reed, Konrad Zolna, Emilio Parisotto, Sergio Gomez Colmenarejo, Alexander Novikov, Gabriel Barth-Maron, Mai Gimenez, Yury Sulsky, Jackie Kay, Jost Tobias Springenberg, et al. A generalist agent, 2022. 

- [92] Alexander Robey, Zachary Ravichandran, Vijay Kumar, Hamed Hassani, and George J. Pappas. Jailbreaking llm-controlled robots, 2024. 

- [93] Ranjan Sapkota, Yang Cao, Konstantinos I. Roumeliotis, and Manoj Karkee. Vision-language-action (VLA) models: Concepts, progress, applications and challenges, 2025. 

- [94] Manolis Savva, Abhishek Kadian, Oleksandr Maksymets, Yili Zhao, Erik Wijmans, Bhavana Jain, Julian Straub, Jia Liu, Vladlen Koltun, Jitendra Malik, Devi Parikh, and Dhruv Batra. Habitat: A platform for embodied AI research. In _2019 IEEE/CVF International Conference on Computer Vision_ , pages 9338–9346, 2019. doi: 10.1109/ICCV.2019.00943. 

- [95] Albert Schotschneider, Svetlana Pavlitska, and J. Marius Zöllner. Runtime safety monitoring of deep neural networks for perception: A survey, 2025. 

- [96] Julian Schrittwieser, Ioannis Antonoglou, Thomas Hubert, Karen Simonyan, Laurent Sifre, Simon Schmitt, Arthur Guez, Edward Lockhart, Demis Hassabis, Thore Graepel, et al. Mastering atari, go, chess and shogi by planning with a learned model. _Nature_ , 588(7839):604–609, 2020. doi: 10.1038/s41586-020-03051-4. 

- [97] Danbing Seto, Bruce H. Krogh, Lui Sha, and Alongkrit Chutinan. The simplex architecture for safe online control system upgrades. In _Proceedings_ 

21 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


_of the 1998 American Control Conference_ , pages 3504–3508, 1998. doi: 10.1109/ACC.1998.703255. 

- [98] Shital Shah, Debadeepta Dey, Chris Lovett, and Ashish Kapoor. AirSim: High-fidelity visual and physical simulation for autonomous vehicles. In _Field and Service Robotics_ , pages 621–635. Springer, 2018. URL `https://arxiv.org/abs/1705.05065` . 

- [99] Rui Shao, Wei Li, Lingsen Zhang, Renshan Zhang, Zhiyang Liu, Ran Chen, and Liqiang Nie. Large vlm-based vision-language-action models for robotic manipulation: A survey, 2025. 

- [100] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Perceiver-actor: A multi-task transformer for robotic manipulation, 2022. 

- [101] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, Simon Alibert, Matthieu Cord, Thomas Wolf, and Remi Cadene. SmolVLA: A vision-language-action model for affordable and efficient robotics, 2025. URL `https://arxiv.org/ abs/2506.01844` . 

- [102] Chonghao Sima, Katrin Renz, Kashyap Chitta, Li Chen, Hanxue Zhang, Chengen Xie, Ping Luo, Andreas Geiger, and Hongyang Li. DriveLM: Driving with graph visual question answering, 2023. 

- [103] Gagandeep Singh, Timon Gehr, Markus Püschel, and Martin Vechev. An abstract domain for certifying neural networks. _Proceedings of the ACM on Programming Languages_ , 3(POPL):1–30, 2019. doi: 10.1145/3290354. 

- [104] Harold Soh and Eugene Lim. Action hallucination in generative vision-language-action models, 2026. URL `https://arxiv.org/abs/2602.06339` . 

- [105] Yejin Son, Minseo Kim, Sungwoong Kim, Seungju Han, Jian Kim, Dongju Jang, Youngjae Yu, and Chan Young Park. Subtle risks, critical failures: A framework for diagnosing physical safety of llms for embodied decision making. In _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , pages 25692–25733, 2025. doi: 10.18653/v1/2025.emnlp-main.1305. URL `https: //aclanthology.org/2025.emnlp-main.1305/` . 

- [106] Christian Szegedy, Wojciech Zaremba, Ilya Sutskever, Joan Bruna, Dumitru Erhan, Ian Goodfellow, and Rob Fergus. Intriguing properties of neural networks. In _International Conference on Learning Representations_ , 2014. 

- [107] Emanuel Todorov, Tom Erez, and Yuval Tassa. MuJoCo: A physics engine for model-based control. In 

   - _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 5026–5033, 2012. doi: 10.1109/IROS.2012.6386109. 

- [108] Kim P. Wabersich and Melanie N. Zeilinger. A predictive safety filter for learning-based control of constrained nonlinear dynamical systems. _Automatica_ , 129:109597, 2021. doi: 10.1016/j.automatica. 2021.109597. 

- [109] Akifumi Wachi, Xun Shen, and Yanan Sui. A survey of constraint formulations in safe reinforcement learning. In _Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence_ , pages 8262–8271, 2024. doi: 10.24963/ijcai.2024/ 913. 

- [110] Xinyang Wang, Qian Liu, Wenjie Ding, Zhao Yang, Wei Li, Chang Liu, Bailin Li, Kun Zhan, Xianpeng Lang, and Wei Chen. Unifying language-action understanding and generation for autonomous driving, 2026. URL `https://arxiv.org/abs/2603.01441` . 

- [111] Ziyao Wang, Bingying Wang, Hanrong Zhang, Tingting Du, Tianyang Chen, Guoheng Sun, Yexiao He, Zheyu Shen, Wanghao Ye, and Ang Li. Vision-language-action in robotics: A survey of datasets, benchmarks, and data engines, 2026. URL `https://arxiv.org/abs/2604.23001` . 

- [112] Wayve. LINGO-2: Driving with natural language. Technical blog, 2024. URL `https://wayve.ai/ thinking/lingo- 2- driving- with- language/` . Technical blog. 

- [113] Fanbo Xiang, Yuzhe Qin, Kaichun Mo, Yikuan Xia, Hao Zhu, Fangchen Liu, Minghua Liu, Hanxiao Jiang, Yifu Yuan, He Wang, Li Yi, Angel X. Chang, Leonidas J. Guibas, and Hao Su. SAPIEN: A SimulAted part-based interactive environment. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 11097–11107, 2020. doi: 10.1109/CVPR42600.2020.01111. URL `https : / / openaccess . thecvf . com / content _ CVPR_2020/html/Xiang_SAPIEN_A_SimulAted_ Part- Based_Interactive_ENvironment_CVPR_ 2020_paper.html` . 

- [114] Mengdi Xu, Zhenjia Song, Peide Wang, Yizhou Wang, Dingkang Chen, Yifei Wang, Weizhe Zhang, Zhe Wang, Junnan Li, Dahua Lin, et al. A survey on robotics with foundation models: Toward embodied ai, 2024. 

- [115] Lijin Yang, Jianing Huang, Zhongzhan Huang, Shu Liu, and Hao Yang. Judge, then drive: A criticcentric vision language action framework for autonomous driving, 2026. URL `https://arxiv. org/abs/2604.27366` . 

22 

Silent Failures in Physical AI 

Barak Or, Ph.D. 


- [116] Tony Z. Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware, 2023. 

- [117] Weiye Zhao, Tairan He, Rui Chen, Tianhao Wei, and Changliu Liu. State-wise safe reinforcement learning: A survey. In _Proceedings of the ThirtySecond International Joint Conference on Artificial Intelligence_ , pages 6814–6822, 2023. doi: 10.24963/ ijcai.2023/763. 

- [118] Yifan Zhong, Fengshuo Bai, Shaofei Cai, Xuchuan Huang, Zhang Chen, Xiaowei Zhang, Yuanfei Wang, Shaoyang Guo, Tianrui Guan, Ka Nam Lui, et al. A survey on vision-language-action models: An action tokenization perspective, 2025. 

23 

