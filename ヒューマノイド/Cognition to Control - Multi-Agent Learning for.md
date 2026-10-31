---
title: "Cognition to Control - Multi-Agent Learning for Human-Humanoid Collaborative Transport"
date: "2026-03-04"
authors: "Hao Zhang; Yisen Li; Ruize Geng; Yves Tseng; Yaru Niu; Ding Zhao"
url: https://arxiv.org/abs/2603.03768
pdf: https://arxiv.org/pdf/2603.03768
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.03768)** / [論文ページ](https://arxiv.org/abs/2603.03768)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Physical Contracts for Plug-Compatible Human–Humanoid Collaboration 

Hao Zhang<sup>_∗,_1</sup><sup>_,_2</sup> , Yisen Li<sup>_∗,_1</sup> , Ruize Geng<sup>2</sup> , Yves Tseng<sup>1</sup> , Yaru Niu<sup>2</sup> , Ding Zhao<sup>_†,_2</sup> and H. Eric Tseng<sup>_†,_1</sup> 

**_Abstract_ — Full-stack human–robot collaboration (HRC) can become brittle when replacing a planner, partner model, coordination policy, or controller changes the physical meaning of cross-layer signals. We introduce C2C, an object-centric cognition-to-control architecture that preserves these meanings through physical contracts. Rather than standardizing individual modules, C2C standardizes the physical semantics exchanged between them: task intent is represented by a geometrically verified payload path, partner information by a source-independent physical state, learned coordination by bounded 11-D task-space commands, and robot-specific feasibility remains inside wholebody control (WBC). The reference system combines a visionlanguage model with deterministic geometric verification and multi-agent reinforcement learning (MARL) for partner-aware coordination. Across nine transport scenarios, adaptive MARL variants achieve 77.1–82.1% mean success under unchanged interfaces, compared with 56.5% for a scripted-partner reference. The same contracts further support neural and interpretable hard-tree actors, two- and three-carrier teams, and simulated-tohuman partner substitution. Physical Unitree G1–human tests achieve 100% success in spatially confined transport and 80% in super-long-object handling, while a three-carrier system with two G1 humanoids and one human validates the same interface structure on hardware. Together, these results show that C2C converts a tightly coupled HRC stack into a plug-compatible system in which key components can change without redefining the physical collaboration task.** 

# I. INTRODUCTION 

Human–humanoid collaborative transport is a demanding form of physical human–robot collaboration (HRC) because task reasoning, partner adaptation, and whole-body control must agree on the motion of one shared payload. Classical work established whole-body optimization for human– humanoid carrying [1], [2], while recent systems use haptic intent inference and hierarchical control [3], [4], compliant reinforcement learning [5], or model-based planning with whole-body control [6], [7]. These advances show that humanoids can collaborate with humans under substantial physical coupling. They also expose a systems problem: cognition, partner sensing, learned coordination, and robot execution are often connected through representations chosen for a particular stack. 

The resulting failure mode is interface entanglement. A semantic planner may emit a skill identifier or plannerspecific trajectory, a coordination policy may depend on 

> _∗_ Equal contribution. 

> _†_ Correspondance to Ding Zhao (dingzhao@cmu.edu), H. Eric Tseng (hongtei.tseng@uta.edu) and Hao E. Zhang (haoz4@andrew.cmu.edu). 

> 1Hao Zhang, Yisen Li, Yves Tseng and H. Eric Tseng are with the University of Texas at Arlington. (email: haoz4@andrew.cmu.edu; yisen03@upenn.edu; ytseng@duck.com; hongtei.tseng@uta.edu) 

> 2Hao Zhang, Ruize Geng, Yaru Niu and Ding Zhao are with Carnegie Mellon University (haoz4@andrew.cmu.edu; rgeng3@jh.edu; yarun@andrew.cmu.edu; dingzhao@cmu.edu) 


Fig. 1. Cognition-to-control (C2C) resolves interface entanglement around the shared payload. Cognition outputs a verified object path, partner sensing is mapped to a source-independent physical state, coordination outputs bounded task-space adaptation, and robot-specific feasibility remains inside wholebody control. A module is plug compatible when it can change without changing these interface semantics. 

simulator-specific partner states, and a low-level controller may require embodiment-specific references. Replacing any one component can therefore change the physical problem seen by its neighbors even when the software connection remains valid. This issue is becoming more important as semantic planners move closer to robot action [8], [9] and humanoid controllers expose increasingly compact task-space interfaces [10]–[12]. Physical HRC adds a further constraint absent from single-robot modularity: the human and robot continuously perturb the same object, so task, partner, and execution semantics must remain mutually consistent. Fig. 1 illustrates this cross-layer coupling. 

We propose cognition-to-control (C2C), which treats the shared payload as the cross-layer physical invariant. Instead of standardizing internal models, C2C standardizes what each layer is allowed to expose: a verified payload path for task intent, a canonical physical state for the partner, a bounded task-space command for learned coordination, and robotspecific feasibility below the execution boundary. We call a substitution contract preserving when these quantities retain their physical meaning, units, and downstream responsibility after the module behind the boundary changes. The key design principle is therefore not software modularity alone, but preservation of physical semantics across cognition, interaction, and control. To the best of our knowledge, C2C is the first human–humanoid collaborative transport framework to treat cross-layer interface semantics as an explicit systems design objective and enforce them through physical contracts spanning cognition, partner sensing, learned coordination, and whole-body execution. 

The contributions are summarized as follows: 1) We 

introduce object-centric physical contracts that define stable task, partner, coordination, and execution interfaces for full-stack HRC, localizing module changes without redefining the surrounding collaboration problem. 2) We realize these contracts in a human–humanoid transport system that connects verified vision-language guidance, partner-aware multi-agent reinforcement learning (MARL), and wholebody control (WBC) through explicit physical variables from payload path to joint torque. 3) We demonstrate contractpreserving substitution across coordination algorithms, policy representations, partner-state sources, and carrier counts, including executable hard-tree policies and multi-party human– humanoid collaboration. 

# II. RELATED WORK 

# _A. Human–robot collaborative transport_ 

Physical HRC has developed from compliant interaction and role-aware co-manipulation toward full-body collaborative transport [13], [14]. For humanoids, Agravante et al. formulated human–humanoid carrying as constrained whole-body optimization on HRP-4 [1]. Broader co-transport work has combined haptic and human-motion cues to adapt whole-body robot behavior [15]. More recent humanoid systems substantially expand physical capability: H<sup>2</sup> -COMPACT decouples haptic intent interpretation from load-adaptive locomotion [3], COLA learns compliant leader–follower behavior in one policy [5], and Kumbhar et al. combine interaction-aware planning, compliance, and QP whole-body control on Digit [6]. These works establish increasingly capable collaboration mechanisms. C2C targets a different systems question: how the physical task presented to neighboring modules can remain unchanged when the mechanism behind one layer is replaced. The distinction is between optimizing a collaboration stack and defining stable physical interfaces across the stack. 

# _B. From semantic planning to humanoid control_ 

Semantic robot planning has progressed from languageconditioned skill selection in SayCan [8] and closed-loop reasoning in Inner Monologue [16] to vision-languageaction models such as RT-2 [17]. In parallel, humanoid control has moved toward reusable command abstractions. The Masked Humanoid Controller tracks partially specified target trajectories through a common whole-body interface [10]. CEER exposes compliant root and end-effector targets for hierarchical loco-manipulation [11], while HANDOFF uses a compact task-space command that can be driven directly by a VLM planner [12]. These approaches motivate planner-friendly control interfaces, but collaborative transport introduces additional boundaries. The task representation must remain consistent with a shared payload, partner information must survive a change of sensing source, and learned coordination must not expose embodiment-specific commands upstream. C2C therefore extends the interface problem from planner–controller compatibility to cognition– partner–coordination–execution compatibility in a physically coupled team. 

# _C. Adaptive multi-agent coordination and partner substitution_ 

MARL provides a natural framework for coupled decision making, with centralized training and decentralized execution enabling agents to adapt to one another while retaining decentralized policies [18], [19]. HAPPO and HATRPO further address heterogeneous-agent policy updates through sequential and trust-region optimization [20], [21]. Cooperative learning with humans similarly emphasizes adaptation to partner behavior rather than fixed scripted responses [22]. Algorithmic adaptation alone, however, does not guarantee interface compatibility. A policy trained with a simulated teammate can depend on simulator-specific states, while a human partner is observed through measured physical signals. C2C makes the partner representation itself a contract, mapping simulated carriers and measured human motion into the same physical fields. The same principle is used to stress the coordination boundary with different optimizers, neural and hard-tree policies, and different carrier counts while preserving task and action semantics. 

# III. CONTRACT-PRESERVING SYSTEM ARCHITECTURE 

The architecture is defined by what crosses each boundary, not by the algorithm behind it. Fig. 2 traces the data flow from cognition to joint torque. The four interfaces of the reference system are 


where _Pt_ is the verified payload center-of-mass (CoM) path, _x_<sup>_p_</sup> _t_<sup>isthecanonicalpartnerstate,</sup><sup>_ui,t∈_R11isthe</sup> task-space command of carrier _i_ , and _τi,t_ is joint torque. Eq. (1) defines each interface by physical meaning rather than internal representation. A replacement is contract preserving when meaning, units, and downstream responsibility remain unchanged. The experiments evaluate this requirement across the implemented substitutions. 

The task contract ends cognition at an admissible object path rather than a language string or skill ID. The partner contract hides whether state comes from a simulated policy or a human sensor. The coordination contract limits learning to bounded task-space adaptation. The execution contract keeps dynamics, contacts, joint limits, and local clearance inside WBC. These boundaries stop implementation-specific representations before the next layer. A language string or skill ID would bind coordination to the planner vocabulary, a learned partner latent to a particular encoder, and joint targets to one robot morphology. 

C2C instead terminates each module at a physical quantity needed by its neighbor. Planner internals end at _Pt_ , sensing details at _x_<sup>_p_</sup> _t_<sup>,policyinternalsat</sup><sup>_ui,t_,androbotdynamics</sup> below WBC. This localization enables plug compatibility. The partner adapter is 


with identical field ordering, units, and normalization on both branches. Eq. (2) enables simulation-to-human substitution. 


Fig. 2. Reference realization of C2C. The two VLM views produce candidate paths for the same payload, not separate robot paths. A deterministic verifier fuses them into one object reference _Pt_ . The coordination policy receives this reference together with self, partner, object, contact, and range states and outputs the same bounded 11-D task-space command _ui,t_ for every tested policy. The execution layer converts that command to constrained joint torque. During hardware deployment, measured human motion fills the same partner-state fields used by the simulated teammate during training. 

At deployment the frozen robot policy receives measured human motion through the same partner interface. 

# _A. Verified VLM guidance_ 

The left side of Fig. 2 shows the cognition contract in the full stack. The reference cognition adapter uses Qwen2.5VL-7B-Instruct [23] without task-specific fine-tuning. At each query, it receives one carrier-centered 64 _×_ 64 topdown task raster for each carrier over an 8 m _×_ 8 m region. Each raster contains the payload footprint and CoM, goal, obstacles, collaborator locations, and numbered candidate anchors. These are structured task-state maps rather than raw camera images. C2C consumes the resulting task-state maps at the cognition boundary. Fig. 4(a)–(c) shows the two view-conditioned proposals, geometric verification, and shared payload path. 

Candidate anchors are generated before the VLM call. Obstacles are inflated by the payload footprint plus a 0.20 m margin. Free-space points are sampled on a 0.5 m grid, collision-pruned, and capped at 16 visible anchors. The fixed prompt is: “Choose an ordered object-CoM path using only the numbered anchors shown in the image. Prefer progress toward the goal, payload clearance, and smooth heading changes. Return only the ordered anchor IDs. Do not create new coordinates.” Decoding is deterministic and the parser accepts only displayed IDs. 

The two calls use the same frozen model and prompt to produce view-conditioned proposals for the same payload, not independent robot plans. Both outputs are transformed to a common object frame before verification and selection. 

A proposal is admissible only when every segment remains inside the workspace and collision-free in every payloadinflated map. Let _Ct_ be this admissible candidate set. The selected object path is 


where _L_ ( _p_ ) is path length and minimum clearance breaks ties. In Eq. (3), the VLM proposes while deterministic geometry decides what crosses the task boundary. Malformed IDs, unavailable anchors, and invalid geometry trigger one requery. If no valid proposal remains, deterministic shortestpath search produces the same _Pt_ on the fused occupancy map. If planning fails, nominal base motion stops. 

Cognition runs at 0.5 Hz and is re-triggered when the active anchor is reached, the path becomes invalid, the goal changes, or payload deviation exceeds 0.35 m. Proposal, verification, and fallback all preserve the same _Pt_ contract. 

The carriers do not receive independent paths. One payload pose generates compatible grasp targets. For carrier _i_ , 


where _p_<sup>_d_</sup> _o_<sup>_, R_</sup> _o_<sup>_d_arethedesiredpayloadpositionandorientation</sup> and _ri_ is the fixed grasp offset in the payload frame. Thus, 


so Eq. (4) and Eq. (5) derive every carrier target from one payload pose and fixed grasp offsets. The execution layer monitors measured grasp geometry and local clearance, stopping motion outside admissible bounds. Shared-payload 

TABLE I 

geometry and WBC clearance constraints therefore preserve rigid-object consistency during execution. 

_B. Partner-aware MARL behind a fixed task-space contract_ 

The coordination policy is trained in Isaac Lab with two policy-controlled carriers under centralized training and decentralized execution (CTDE). During physical deployment, only the robot actor is executed. The human is a measured partner source and does not participate in gradient updates. MARL exposes the robot to an adaptive teammate during training, while the partner contract allows human substitution without changing the robot policy interface. 

For each carrier, the current interaction block and final policy observation are 


where the blocks have dimensions 10, 13, 13, 18, and 4, and _ri,t ∈_ R<sup>36</sup> is the current range vector. Self and partner fields contain planar pose and velocity, yaw, CoM height, torso pitch, and relative end-effector features. On hardware, motion capture reconstructs the partner fields. Object state contains payload pose, velocity, and four corners. Contact uses four binary end-effector indicators. 

Eq. (6) combines the current block with two previous snapshots for short history without recurrence. The 36-D environment channel is a radial proximity scan normalized as 1 _−_ min( _d,_ 4 _._ 0) _/_ 4 _._ 0. For active path anchor _j_ , the 10-D task block is the next five relative payload waypoints, 


with missing entries padded by the final anchor. Eq. (7) localizes the payload contract by expressing exteroceptive quantities in the carrier frame. 

The actor outputs _ai,t ∈_ [ _−_ 1 _,_ 1]<sup>11</sup> and modulates only a nominal task-space command, 


where diagonal _D_ sets fixed physical residual limits. Eq. (8) keeps learned adaptation in task space and avoids unrestricted joint-level control. The command itself is 


with three planar base commands, CoM height, torso pitch, and two 3-D wrist targets. Eq. (9) and Table I summarize the policy input and output. The planner sets object motion, MARL adapts to the partner, and WBC executes the command. 

The shared task reward is 


where ∆ _st_ is signed progress along the verified payload path, the second term penalizes tilt through the four corner heights, and _I_ drop marks grasp loss or payload drop. Progress is credited only inside the 0.35 m path corridor. The leveling 

DEFAULT TWO-CARRIER POLICY INPUT AND OUTPUT. 

|Component|Size|Description|
|---|---|---|
|Observation space (_o ∈_R<sup>210</sup>)|||
|Global guidance|10|5 anchors (relative planar)|
|Self state|13|Pose/velocity, CoM, torso, wrists|
|Partner state|13|Measured/policy partner|
|Object geometry|18|4 corners, CoM pose/velocity|
|Contact|4|4 binary contact indicators|
|Temporal buffer|116|Two previous 58-D blocks|
|Environment|36|Current 36-ray range|
|Action space (_a ∈_R<sup>11</sup>)|||
|Locomotion|3|Planar velocity/yaw residual|
|Postural|2|CoM/torso residual|
|Wrist control|6|Wrist-position residual|


term is disabled for pushing tasks where payload leveling is not required. Eq. (10) is shared by all coordination methods. 

A centralized critic is used only during training. For proximal policy optimization (PPO)-based variants, actor _i_ uses 


where _ri,t_ is the new/old policy likelihood ratio, _At_ is the centralized GAE advantage, and _c_ is the clip bound. Eq. (11) defines the PPO-style local update used by the corresponding variants. HAPPO retains its sequential update [20], HATRPO its trust-region update [21], and PPO+PCGrad projects conflicting gradients in the shared interaction encoder [24]. These optimizer-specific updates remain inside coordination. Observation, reward, and the 11-D output contract stay fixed. 

_C. Whole-body execution and conversion to joint torque_ 

The center branch in Fig. 2 realizes the execution contract. The execution layer resolves the 11-D command at 100 Hz while the 2 Hz coordination command is held by zero-order hold between policy updates. For each base, CoM, torso, or wrist task, Eq. (12) generates the desired task acceleration, 


and all tasks are solved together by an inverse-dynamics quadratic program (QP), 


In Eq. (13), _M, h_ are robot dynamics, _J, Jc_ are task/contact Jacobians, _S_ is the actuation selector, _fc_ is contact force, _Kf_ is the friction-cone approximation, _W_ contains task weights, and _Jd_ is the clearance Jacobian. The one-step prediction is ∆ _q_ = ∆ _t q_ ˙ +<sup><u>1</u></sup> 2<sup>∆</sup><sup>_t_2</sup><sup>_q_¨.</sup> 

The QP enforces rigid-body dynamics, contact consistency, friction, actuator and joint limits, and robot–obstacle/partner clearance. High weight on common-payload wrist references 


Fig. 3. (a) Episode return during training for IPPO with a scripted partner, HAPPO, HATRPO, and PPO+PCGrad over 2 _._ 0 _×_ 10<sup>9</sup> steps, with shading denoting one standard deviation across five seeds. (b) Mean success rate by task category, comparing the robot-script baseline with the same learning-based tactical variants. (c) Physical deployment: success rate, completion time (s), and mean object tilt rate (<sup>_◦_</sup> /s) for robot-script IPPO and PPO+PCGrad. 

TABLE II 

SYSTEM-LEVEL SUCCESS RATE UNDER THE SHARED C2C INTERFACES ACROSS NINE SCENARIOS (MEAN _±_ STANDARD DEVIATION OVER FIVE SEEDS, 100 EPISODES PER SEED). ∆: RELATIVE DIFFERENCE OF THE MEAN ADAPTIVE-MARL SUCCESS RATE FROM THE ROBOT-SCRIPT REFERENCE. 

|Category|Scenario|Robot-script|HAPPO|HATRPO|PPO+PCGrad|Mean gain ∆|
|---|---|---|---|---|---|---|
||_S_11: Alignment|65.4 _±_ 7.2|83.6 _±_ 5.3|87.9 _±_ 4.5|87.7 _±_ 3.8|+32.1%|
|OSP|_S_12: Turnaround|60.1 _±_ 8.5|77.6 _±_ 6.3|81.5 _±_ 5.5|83.6 _±_ 4.8|+34.6%|
||_S_13: Corner entry|58.2 _±_ 9.1|72.7 _±_ 7.0|75.3 _±_ 6.0|77.8 _±_ 5.3|+29.3%|
||_S_21: Narrow gate|59.2 _±_ 9.0|80.1 _±_ 4.8|83.4 _±_ 4.3|88.6 _±_ 3.5|+42.0%|
|SCT|_S_22: S-shaped path|57.5 _±_ 8.8|76.3 _±_ 5.8|82.1 _±_ 5.0|80.6 _±_ 4.5|+38.6%|
||_S_23: U-shaped path|55.6 _±_ 9.5|75.7 _±_ 6.5|79.2 _±_ 5.3|81.3 _±_ 4.8|+41.6%|
||_S_31: Facing mode|52.8 _±_ 8.1|79.3 _±_ 5.0|84.4 _±_ 1.6|83.2 _±_ 3.5|+55.9%|
|SLH|_S_32: Lateral shuffle|50.4 _±_ 7.5|73.7 _±_ 6.8|75.9 _±_ 5.8|77.3 _±_ 5.0|+50.1%|
||_S_33: Pivoting|49.6 _±_ 8.3|74.9 _±_ 6.0|77.5 _±_ 5.3|78.6 _±_ 4.5|+55.2%|
|Mean succe|ss rate|56.5%|77.1%|80.8%|82.1%|+41.5%|


prevents the bounded MARL residual from breaking rigid grasp geometry. 

The optimized torque is combined with joint feedback and saturation, 


If the QP is infeasible or measured clearance falls below 0.15 m, nominal base motion is zeroed and the last feasible posture is held. Eq. (12)–(14) therefore map the C2C command to joint torque while enforcing robot-specific feasibility. 

TABLE III 

SHARED TRAINING SETTINGS. 

|Parameter|Value|Parameter|Value|
|---|---|---|---|
|Learning rate|10<sup>_−_4</sup>|Hidden layers|[256,256,128]|
|Epochs/update|10|Activation|ReLU|
|Minibatches|16|Initialization|Orthogonal|
|Entropy weight|0.01|Optimizer|Adam<br>|
|Discount factor|0.99|Weight decay|10<sup>_−_4</sup>|
|GAE factor|0.95|Gradient clip|10.0|
|PPO/HAPPO clip|0.2|Learning-rate schedule|Cosine<br>|
|Value-loss weight|0.5|Action steps|2_×_10<sup>9</sup>|


IV. VALIDATION OF CONTRACT PRESERVATION 

We evaluate four substitutions behind C2C boundaries: coordination algorithm, partner-state source, policy representation, and carrier count. Payload reference, observation 

semantics, 11-D task-space command, reward, and robot-side execution remain fixed. Table IV maps each substitution to the preserved semantics and evidence. 

The final row verifies end-to-end dependency. Removing either the guidance source or learned coordination breaks a required boundary on _S_ 33, while the complete stack reaches 78.6% SR in 81.2 s. 

# _A. Experimental setup_ 

_1) Task suite:_ We use nine scenarios as a system stress suite. Orientation-sensitive pushing (OSP) contains _S_ 11 alignment, _S_ 12 turnaround, and _S_ 13 corner entry. Spatially confined transport (SCT) contains _S_ 21 narrow gate, _S_ 22 S-shaped path, and _S_ 23 U-shaped path. Super-long-object handling (SLH) contains _S_ 31 facing mode, _S_ 32 lateral shuffle, and _S_ 33 pivoting. They respectively stress yaw alignment, synchronized confined motion, and long-payload stabilization while sharing the observation, residual-action, reward, and WBC contract. Fig. 4(d)–(f) shows the three task families. 

_2) Training and evaluation:_ Training uses Isaac Lab [25] with two policy-controlled carriers and one rigid payload. Policy, guidance, and WBC rates are 2, 0.5, and 100 Hz. Each scenario uses common success, termination, and horizon rules. SR is evaluated over 100 episodes per seed, and family SR averages its three scenarios. Grasp loss or payload drop 


Fig. 4. VLM guidance and system stress tasks. Panels (a)–(c) show two carrier-centered views. Blue and orange traces are payload-path proposals from the VLM adapter. Deterministic common-frame collision and clearance checks select the verified path, with the active anchor shown in green and the 36-D range observations in cyan. Panels (d)–(f) show the OSP, SCT, and SLH task families used under the same C2C contracts. 

TABLE IV 

SUMMARY OF CONTRACT-PRESERVING SUBSTITUTIONS UNDER THE C2C INTERFACES. 

|Axis|Substitution|Invariant interface|Evidence|
|---|---|---|---|
|Cognition|VLM _→_deterministic fallback|Verified payload path _Pt_|Same downstream path contract|
|Coordination|HAPPO / HATRPO / PPO+PCGrad|Observation, 11-D action, reward, WBC|SR: 77.1 / 80.8 / 82.1%|
|Partner|Simulated carrier _→_human|Partner-state fields and robot action|Physical SR: 100 / 100 / 80%|
|Policy|MLP _→_hard tree|N=3 adapter, action, reward, WBC|SR: 74.7 _→_70.3%|
|Team size|Two _→_three carriers|Guidance, action semantics, reward, WBC|SR: 77.1 _→_74.7%|


is terminal. We report mean _±_ standard deviation over five seeds. 

Training uses Adam with cosine annealing and orthogonal initialization for 2 _._ 0 _×_ 10<sup>9</sup> action steps. Table III lists the shared settings. Optimizer comparisons fix task definitions, the 210-D input, 11-D residual action, reward, geometry checks, WBC, evaluation budget, task gains, and QP weights. 

Robot-script uses independent proximal policy optimization (IPPO) against a scripted kinematic collaborator. HAPPO, HATRPO, and PPO+PCGrad use two adaptive policy-controlled carriers. Robot-script uses the same [256,256,128] multilayer perceptron (MLP) backbone and 2 _._ 0 _×_ 10<sup>9</sup> -step budget. Its partner proxy supplies relative position, velocity, and orientation with 2.0 cm Gaussian vertical jitter, 0.1 m/s uniform velocity noise, and 3.0<sup>_◦_</sup> Gaussian yaw noise. 

All configurations retain the task-space action and execution contracts. Table II therefore compares complete coordination configurations under the same C2C interfaces. For the simulation-to-human study, MARL training uses two adaptive policy-controlled carriers. At hardware deployment the learned robot actor is frozen. The second learned carrier is removed and the human’s motion-capture (MoCap) state fills the same partner fields. The human is not optimized by MARL and no online learning is performed during the physical trials. For scenario _s_ , SRlearn _,s_ averages HAPPO, HATRPO, 

and PPO+PCGrad. Table II reports ∆ _s_ = 100(SRlearn _,s −_ SRscript _,s_ ) _/_ SRscript _,s_ . The mean row applies this definition to the method means. 

# _B. Coordination algorithms under fixed contracts_ 

We compare HAPPO [20], HATRPO [21], and PPO+PCGrad with robot-script IPPO. The adaptive MARL variants use different updates but share fixed task and execution interfaces. Robot-script is a fixed-partner reference. This tests whether coordination algorithms can change without redesigning the surrounding HRC system. 

Mean SR is 56.5%, 77.1%, 80.8%, and 82.1% for robotscript, HAPPO, HATRPO, and PPO+PCGrad. Every adaptive variant improves over robot-script in all nine scenarios while preserving the same payload reference, observation fields, 11-D residual command, reward, geometry checks, and WBC. The largest relative gains occur for long-object handling, where rigid-payload coupling amplifies timing and heading mismatch. No adaptive optimizer leads every scenario. This is precisely the intended separation: coordination performance changes while the HRC task and execution interface remain fixed. Table II and Fig. 3(a)–(b) report the results. 

_C. Simulation-to-human transfer under the same contract_ 

Physical tests use five trials per task with common guidance and robot-side WBC. Measured human motion fills the same 


Fig. 5. Physical human–single robot collaboration demonstrations (a) online heading adjustment, (b) following-to-leading transition, (c) constrained gate traversal, and (d) super-long-payload corridor transport. 


Fig. 6. Task-family success rate for two-carrier HAPPO-MLP, three-carrier HAPPO-MLP, and three-carrier HAPPO-Tree. Parentheses give carrier count. 

partner-state fields used by simulated carriers, and the frozen robot actor retains the same residual base/wrist action space. The partner source changes without changing the robot policy interface. 

Compared with robot-script IPPO, PPO+PCGrad retains 100% SR on OSP, raises SCT from 40% to 100%, and raises SLH from 40% to 80%. Completion time decreases from 101.6 to 81.5 s on SCT and from 113.6 to 86.9 s on SLH, with lower tilt rate in both tasks. Table V and Fig. 3(c) report the results. Fig. 5 shows heading adjustment, following-to-leading transition, gate traversal, and long-payload transport. 


Fig. 7. Physical human–multiple robots collaborative transport with two Unitree G1 humanoids and one human: (a) payload reorientation and (b) passage traversal around laboratory partitions, shown at 20 s intervals. 

TABLE V 

PHYSICAL RESULTS OVER FIVE TRIALS PER TASK. 

# _D. Policy representation and carrier-count extension_ 

|Task||Robot-script IP|PO||PPO+PCGra|d|
|---|---|---|---|---|---|---|
||SR|Tilt (<sup>_◦_</sup>/s)|Time (s)|SR|Tilt (<sup>_◦_</sup>/s)|Time (s)|
|OSP|100%|–|74.2|100%|–|65.2|
|SCT|40%|3.2|101.6|100%|2.4|81.5|
|SLH|40%|3.6|113.6|80%|2.7|86.9|


We next test whether the coordination contract is tied to one function approximator or one fixed team size. Under HAPPO, multilayer perceptron actors are tested with two and three carriers, and a hard oblique decision-tree actor is tested with three. For an internal node _k_ , the tree uses the hard split _gk_ ( _o_ ) = I[ _wk_<sup>_To > bk_].Theselectedleaf</sup><sup>_l_(</sup><sup>_o_)storesanaffine</sup> 

controller and outputs 


where _ac_ and _as_ are the center and half-range of the action bounds, and _Kl, bl_ are leaf parameters. Eq. (15) gives a bounded action with an explicit root-to-leaf path. Forward routing is hard and deterministic, while a soft backward gate optimizes split parameters during training. The tree uses the same physical inputs and bounded 11-D residual action as the neural actor, making its deployed decision path directly inspectable. 

For three carriers, only partner encoding changes inside coordination. Task guidance, action semantics, reward, and WBC remain fixed, and the MLP/tree comparison uses the same three-carrier adapter. This isolates representation and carrier-count changes from cognition and execution. 

Mean SR is 77.1% for two-carrier HAPPO-MLP, 74.7% for three-carrier HAPPO-MLP, and 70.3% for three-carrier HAPPO-Tree. Moving from two to three MLP carriers changes the mean by only 2.4 points, while replacing the three-carrier MLP with the interpretable tree costs 4.4 points without changing the task or action contract. Fig. 6 summarizes this controlled comparison. Fig. 7 shows two Unitree G1 humanoids and one human performing payload reorientation and passage traversal, closing the three-carrier interface on hardware. 

Together, the experiments validate contract preservation across coordination algorithm, policy representation, carrier count, and partner-state source. The deterministic fallback also exercises the cognition boundary by producing the same _Pt_ when VLM proposals are rejected. Quantitative simulations retain the reference VLM and WBC, while hardware closes the sim-to-human and three-carrier interfaces. Across these tested substitutions, neighboring modules retain the same physical semantics and robot-side feasibility checks. 

# V. CONCLUSION 

This work identifies interface semantics as a central systems challenge in full-stack physical HRC. Rather than coupling cognition, partner adaptation, learned coordination, and wholebody control through implementation-specific representations, C2C organizes them around physical contracts defined on the shared payload. The resulting architecture preserves the collaboration task while allowing individual modules to change behind stable interfaces, providing a principled basis for composable human–humanoid collaboration. 

- The proposed object-centric contracts separate task intent, partner state, learned coordination, and robot execution through physically interpretable interfaces, preventing changes within one module from propagating across the full stack. 

- This contract structure supports heterogeneous implementations behind the same interfaces, including different MARL optimizers, neural and hard-tree policies, simulated and human partners, and two- and three-carrier configurations, while retaining common task and action semantics. 

- Across nine simulated scenarios, adaptive MARL achieves 77.1–82.1% mean success compared with 56.5% for the robot-script reference. Physical G1–human experiments achieve 100%, 100%, and 80% success on OSP, SCT, and SLH, while the three-carrier system retains 74.7% success with HAPPO-MLP and 70.3% with the hard-tree policy, with further validation on two G1 humanoids cooperating with one human. 

# REFERENCES 

- [1] D. J. Agravante, A. Cherubini, A. Sherikov, P.-B. Wieber, and A. Kheddar, “Human–humanoid collaborative carrying,” _IEEE Transactions on Robotics_ , vol. 35, no. 4, pp. 833–846, 2019. 

- [2] H. Zhang, Y. Niu, Y. Wang, D. Zhao, and H. E. Tseng, “Halo: Learning human-robot collaboration via heterogeneous-agent lyapunov policy optimization,” _arXiv preprint arXiv:2603.03741_ , 2026. 

- [3] G. C. R. Bethala, H. Huang, N. Pudasaini, A. M. Ali, S. Yuan, C. Wen, A. Tzes, and Y. Fang, “H<sup>2</sup> -compact: Human–humanoid co-manipulation via adaptive contact trajectory policies,” in _2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids)_ , 2025, pp. 1004–1011. 

- [4] H. Zhang, N. Lei, S. E. Li, J. Zhang, and Z. Wang, “Multi-scale reinforcement learning of dynamic energy controller for connected electrified vehicles,” _IEEE Transactions on Intelligent Transportation Systems_ , 2025. 

- [5] Y. Du, Y. Li, B. Jia, Y. Lin, P. Zhou, W. Liang, Y. Yang, and S. Huang, “Learning human–humanoid coordination for collaborative object carrying,” _arXiv preprint arXiv:2510.14293_ , 2025. 

- [6] S. S. Kumbhar, A. M. Kulkarni, and P. Artemiadis, “Efficient and compliant control framework for versatile human–humanoid collaborative transportation,” _arXiv preprint arXiv:2512.07819_ , 2025. 

- [7] H. Zhang, Y. Tseng, D. Zhao, and H. E. Tseng, “Interaction-aware whole-body control for compliant object transport,” _arXiv preprint arXiv:2603.03751_ , 2026. 

- [8] M. Ahn, A. Brohan, and N. Brown, “Do as i can, not as i say: grounding language in robotic affordances,” _arXiv preprint_ , 2022. 

- [9] H. Zhang, N. Lei, W. Peng, B. Li, S. Lv, B. Chen, and Z. Wang, “Bi-level transfer learning for lifelong-intelligent energy management of electric vehicles,” _IEEE Transactions on Intelligent Transportation Systems_ , vol. 26, no. 10, pp. 16 174–16 187, 2025. 

- [10] P. Dugar, A. Shrestha, F. Yu, B. van Marum, and A. Fern, “Learning multi-modal whole-body control for real-world humanoid robots,” in _Proceedings of the AAAI Symposium Series_ , vol. 7, no. 1, 2025, pp. 650–657. 

- [11] X. Luo, X. Chen, X. Yin, H. Wu, B. Xia, Z. Chen, J. Li, B. Chen, and X. Cheng, “Ceer: Compliant end-effector and root control as a unified interface for hierarchical humanoid loco-manipulation,” _arXiv preprint arXiv:2605.19981_ , 2026. 

- [12] L. Yang, J. Li, N. Poddar, Y. Hou, G. Huh, R. Griffin, G. Gkioxari, and A. D. Ames, “Handoff: Humanoid agentic task-space wholebody control via distilled complementary teachers,” _arXiv preprint arXiv:2606.06493_ , 2026. 

- [13] A. Ajoudani, A. M. Zanchettin, S. Ivaldi, A. Albu-Schaffer,¨ K. Kosuge, and O. Khatib, “Progress and prospects of the human–robot collaboration,” _Autonomous Robots_ , vol. 42, no. 5, pp. 957–975, 2018. 

- [14] U. E. Ogenyi, J. Liu, C. Yang, Z. Ju, and H. Liu, “Physical human– robot collaboration: Robotic systems, learning methods, collaborative strategies, sensors, and actuators,” _IEEE Transactions on Cybernetics_ , vol. 51, no. 4, pp. 1888–1901, 2021. 

- [15] D. Sirintuna, A. Giammarino, and A. Ajoudani, “Human–robot collaborative carrying of objects with unknown deformation characteristics,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2022. 

- [16] W. Huang, F. Xia, and T. Xiao, “Inner monologue: embodied reasoning through planning with language models,” _arXiv preprint_ , 2022. 

- [17] M. Kim, K. Pertsch, and S. Karamcheti, “Openvla: an open-source vision-language-action model,” _arXiv preprint_ , 2024. 

- [18] R. Lowe, Y. Wu, and A. Tamar, “Multi-agent actor-critic for mixed cooperative-competitive environments,” in _NeurIPS_ , 2017. 

- [19] A. Oroojlooy and D. Hajinezhad, “A review of cooperative multi-agent deep reinforcement learning,” _Applied Intelligence_ , vol. 53, no. 11, pp. 13 677–13 722, 2023. 

- [20] Y. Zhong, J. Kuba, X. Feng _et al._ , “Heterogeneous-agent reinforcement learning,” _Journal of Machine Learning Research_ , vol. 25, no. 32, pp. 1–67, 2024. 

- [21] J. Kuba, R. Chen, M. Wen _et al._ , “Trust region policy optimisation in multi-agent reinforcement learning,” _arXiv preprint_ , 2021. 

- [22] D. Hadfield-Menell, S. Russell, and P. Abbeel, “Cooperative inverse reinforcement learning,” in _NeurIPS_ , 2016. 

- [23] S. Bai, K. Chen, X. Liu _et al._ , “Qwen2.5-vl technical report,” _arXiv preprint_ , 2025. 

- [24] T. Yu, S. Kumar, A. Gupta _et al._ , “Gradient surgery for multi-task learning,” in _NeurIPS_ , 2020, pp. 5824–5836. 

- [25] M. Mittal, P. Roth, J. Tigue, A. Richard, O. Zhang _et al._ , “Isaac lab: A gpu-accelerated simulation framework for multi-modal robot learning,” _arXiv preprint arXiv:2511.04831_ , 2025. 

