---
title: "Safe Learning for Contact-Rich Robot Tasks: A Survey from Classical Learning-Based Methods to Safe Foundation Models"
date: "2025-12-10"
authors: "Heng Zhang; Rui Dai; Gokhan Solak; Pokuang Zhou; Nikos Tsagarakis; Yu She"
url: https://arxiv.org/abs/2512.11908
pdf: https://arxiv.org/pdf/2512.11908
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.11908)** / [論文ページ](https://arxiv.org/abs/2512.11908)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Safe Learning for Contact-Rich Robot Tasks: A Survey from Classical Learning-Based Methods to Safe Foundation Models 

Heng Zhang<sup>1,2,3*</sup> , Rui Dai<sup>4</sup> , Gokhan Solak<sup>1</sup> , Pokuang Zhou<sup>3</sup> , Nikos Tsagarakis<sup>4</sup> , Yu She<sup>3,5,6</sup> , Arash Ajoudani<sup>1</sup> 

- 1Human-Robot Interfaces and Interaction Lab, Istituto Italiano di Tecnologia, Genova, Italy. 

> 2Ph.D. program of national interest in Robotics and Intelligent Machines (DRIM), Universit`a di Genova, Genoa, Italy. 

> 3Edwardson School of Industrial Engineering, Purdue University, West Lafayette, IN, USA. 

> 4Humanoids and Human Centered Mechatronics Lab, Istituto Italiano di Tecnologia, Genova, Italy. 

> 5School of Mechanical Engineering, Purdue University, West Lafayette, IN, USA. 

- 6Elmore Family School of Electrical and Computer Engineering, Purdue University, West Lafayette, IN, USA. 

*Corresponding author(s). E-mail(s): heng.zhang@iit.it; 

#### **Abstract** 

Contact-rich tasks remain difficult for robotic systems due to uncertainty, complex dynamics, and the risk of damage during interaction. As learning-based methods increasingly enable robots to acquire and generalize advanced manipulation skills, ensuring safety during both learning and deployment has become essential. We present, to our knowledge, the first scoping survey that places safety at the center of learning for contact-rich robotic tasks, spanning classical provable safety, safe reinforcement learning, and emerging robotic foundation models. We analyze how safety principles are formulated, enforced, and evaluated across established learning approaches and foundation-model-enabled methods. Existing work is organized into two domains: safe exploration, which reduces unsafe actions during learning, and safe execution, which ensures robustness and constraint satisfaction during deployment. We further examine how safe learning 

1 

principles extend to robotic foundation models, particularly vision-language models (VLMs) and vision-language-action models (VLAs). These models introduce opportunities such as language-based constraint specification and multimodal safety grounding, while also posing new risks and evaluation challenges. Finally, we outline current limitations and highlight promising directions toward reliable, safety-aligned robotic systems capable of operating in complex, contact-rich environments. 

**Keywords:** contact-rich tasks, safe learning, robot manipulation, physical interaction 

_“Contact is the heart of robotic manipulation. To understand manipulation, you must understand contact.”_ The Heart of Robotic Manipulation **—— Matthew T. Mason** 

## **Introduction** 

Robots are increasingly expected to operate in unstructured and dynamic environments, where interaction with the physical world is inevitable [1, 2]. Among such interactions, contact-rich tasks such as assembly, insertion, cutting, or tool use are particularly challenging due to their complex, discontinuous dynamics and the need for precise force and motion control. Traditional model-based control methods often struggle in these scenarios due to inaccurate or hard-to-obtain models, while learning-based methods promise flexibility and adaptability by leveraging data-driven representations [3]. 

However, applying learning-based methods to contact-rich tasks raises critical safety concerns. Exploration during training may lead to unsafe actions that damage the robot, the environment, or nearby humans. Similarly, the execution of learned policies in deployment must guarantee constraint satisfaction and robustness, especially under distributional shifts. Therefore, safety must be addressed both during exploration and during execution to ensure the reliable operation of autonomous systems in the real world. 

This survey focuses on safe learning-based approaches that address the dual challenges of safe exploration and safe execution in robot contact-rich tasks. We categorize and analyze a wide range of methods, including constrained and risk-aware reinforcement learning, uncertainty-aware control, model-based safety filters, and hybrid approaches that combine learning with formal guarantees. These methods aim to strike a balance between learning efficiency, task performance, and safety assurance. 

We begin by outlining the unique challenges posed by contact-rich tasks and the requirements for safety in this context. We then present a taxonomy of existing methods based on the learning paradigm and safety mechanism employed. Finally, we identify open problems and future research directions, including benchmark design, generalization, and integration of safety across system levels. 

This survey aims to provide a structured overview of the current landscape, foster a deeper understanding of safe learning in contact-rich robotics, and inspire new 

2 

research toward safe and capable autonomous systems. In particular, it emphasizes the emerging role of vision-language models (VLMs) and vision-language-action models (VLAs) as robotic foundation models that unify perception, language, vision, and control, but safety in contact-rich tasks is still an open challenge [4, 5]. By framing safety challenges and design principles in the context of these models, the survey seeks to provide timely guidance for the development of VLM/VLA-based systems that are not only powerful and general but also verifiably safe in real-world deployment. 

A number of recent surveys have explored topics at the intersection of safety, learning, and contact-rich robotic manipulation. However, none comprehensively address the unique challenges and opportunities posed by safe learning in contact-rich tasks. Our survey aims to bridge this gap by providing a focused, methodical overview of the state-of-the-art, specifically within this critical niche. 

Several surveys have investigated safe learning and reinforcement learning (RL) more generally. An early and influential reference is the comprehensive safe-RL survey of Garc´ıa and Fern´andez [6], whose taxonomy remains a common organizing lens for subsequent work, separating approaches that modify the optimization criterion from those that modify the exploration process. Works such as [7–9] provide comprehensive overviews of safety mechanisms in learning-based control and safe RL, including constraints, shielding, and exploration strategies. More specialized perspectives are offered in surveys on state-wise safety [8], control barrier functions in RL [10] and shielded RL [11]. While these surveys address safety in learning, they often neglect the complexities introduced by physical interaction and contact dynamics. 

From the perspective of robotic manipulation and contact, surveys such as [12, 13] and [14] analyze manipulation strategies and control frameworks, including both model-based and model-free methods. Others review variable impedance control [15] and compliant mechanisms [16], which are crucial for adapting to contact uncertainties but do not directly integrate learning-based safety frameworks. 

The application of RL in robotic assembly has also been reviewed in recent literature [3, 17, 18] with emphasis on task success and sample efficiency. However, these surveys primarily focus on task performance and learning architectures, offering limited discussion on safety guarantees during exploration or deployment. A recent survey paper [19] reviews the imitation learning methods for contact-rich robotic tasks. Differently, we center our review specifically on online safe learning methods, without focusing on imitation learning. 

More recent efforts begin to address physical risk and safety in the era of data-driven and foundation model-based robotics [20–23], highlighting the growing relevance of scalable safety mechanisms. However, they often center on high-level policy alignment or general-purpose systems, lacking specificity in contact-rich manipulation contexts. 

This survey also concentrates on the key safety gaps and data requirements underlying robot foundation models [4, 24]. Advanced agentic embodied AI sheds light on a generalist robotic system, while the safety issue remains due to a lack of physical interaction data [25]. Safety for VLA robotic generalists lags because high-fidelity, failure and near-miss contact data are scarce, and foundational semantic models still 

3 

mis-ground force, region, and tolerance constraints in physically complex interaction regimes [26]. Hybrid plan–parameterize–filter stacks that couple semantic/VLM layers with compliant action abstractions and certified online shields improve robustness under distribution shift but remain challenged by contact mode transitions and geometry/material variation [4, 18, 24, 27]. Advancing VLA safety thus hinges on curated multimodal contact corpora, standardized force/violation metrics, and tighter analytical–data-driven integration for adaptive constraint grounding and reactive invariance maintenance [25]. 

Most closely related to the present work is the concurrent review of [28], which surveys cost-effective and safe contact-rich robotic manipulation with reinforcement learning. Our scope is broader and complementary: rather than restricting to RL, we (i) place safety across both exploration and execution at the center specifically for contact-rich interaction; (ii) bridge classical provable-safety methods (Lyapunov, control barrier functions, contraction metrics, and reachability) with learning-based and robotic foundation-model (VLM/VLA) approaches under a single set of safety axes; and (iii) contribute a multi-perspective categorization spanning sensing/policy modality, safety enforcement space, safety abstraction level, a data pyramid, and a three-level evaluation scheme. Accordingly, rather than claiming priority in absolute terms, we position this survey as the first to jointly span these classical and foundationmodel perspectives for safe contact-rich learning. 

Lastly, surveys on human-like manipulation [29], force/torque control [30], and safety in robotic manufacturing [31] provide valuable domain-specific insights but remain largely disconnected from the safe learning perspective, although safety standards are discussed in [31]. 

In contrast to the aforementioned surveys, our work focuses specifically on the intersection of safe learning and contact-rich robotics, where safety must be ensured not only in policy learning but also in dynamic interaction with the environment. We systematically review methods that account for safety during physical contact, discuss open challenges in real-world applications, and outline promising directions for future research. We conducted a detailed analysis of the research intensity in this field over recent years, covering the period from 2018 through 2025. Because our literature search has a fixed cut-off date, the 2025 count is necessarily partial; we therefore mark 2025 as incomplete and base any year-over-year comparison on the complete years (2018– 2024) rather than on the partial 2025 data. Figure 1 illustrates the trend of research interest in this area, along with the examples of robotic experiments associated with the keywords “safety,” “contact-rich robotics,” and “learning.” 

Therefore, it is necessary to provide a comprehensive and timely survey of recent advancements in safe learning for robotic contact-rich tasks. This survey focuses on learning-based approaches that directly integrate safety mechanisms into the learning process, such as safe reinforcement learning and model-based safety strategies. To be precise, we exclude _pure_ imitation-learning methods without an online mechanism for actively managing safety during exploration or execution. We do _not_ , however, exclude every method that uses demonstration data: approaches that are pre-trained or bootstrapped from demonstrations, including VLA policies, fall within our scope when they additionally incorporate an online-learning component and/or an explicit 

4 


**Figure 1** Trend of research publications that include keywords related to both safety, contact-rich robotics and learning. Representative example works are shown: contact-rich tasks, safe control, and learning-based methods [32, 33]. The count for 2025 is incomplete: it contains only the publications indexed up to our literature-search cut-off (August 2025), so the 2025 bar is not directly comparable with the complete years. Year-over-year comparisons should therefore be based on the complete years 2018–2024, and the trend should be read from the yearly counts rather than from a single overall growth percentage. 

safety mechanism (constraint satisfaction, shielding, compliant enforcement, or riskaware objectives). It is this criterion, rather than the learning-paradigm label, that determines inclusion. Our scope of contact-rich tasks is defined explicitly in Section of Robotic Contact-Rich Tasks 

In light of the aforementioned challenges and recent advancements, we systematically review the landscape of safe learning methods for robotic contact-rich tasks, which pose unique challenges due to the dynamic, force-intensive, and uncertain nature of physical interactions. Our contributions are threefold: 

1. We introduce a structured safety-centric taxonomy that categorizes safe learning approaches by key dimensions, including learning phase (exploration vs. execution), level of safety integration (planning, control, or end-to-end), and modalities used (force/torque, vision, etc.). This survey provides a comprehensive lens for analyzing existing methods and identifying safety design trade-offs. 

2. Beyond general safe learning, we focus on its application to contact-rich robotic tasks such as insertion, polishing, and assembly. We detail how safety constraints are embedded in these tasks, and map the methods used to specific operational challenges (e.g., compliance, contact-invariant tasks, collision avoidance, and force control). 

3. We synthesize open research questions and outline critical challenges such as simto-real transfer under safety constraints, the scarcity of standardized benchmarks, and the need for provably safe generalization. We also discuss underexplored directions, including hybrid control-learning frameworks and human-in-the-loop 

5 


**Figure 2** Schematic illustrations of four representative contact-rich tasks: surface grinding, peg-inhole insertion, massaging, and non-prehensile pushing, highlighting the dominant contact configuration and force directions ( _Fn_ : normal contact force). 

safety mechanisms. Most importantly, we highlight the challenges and future opportunities in integrating safe contact-rich learning with large robotic foundation models, particularly VLM and VLA. 

## **Results** 

This section presents the main outcomes of our scoping review through a structured synthesis of the existing literature on safe learning for contact-rich robotic tasks. The findings of our review are organized to highlight the current state of the field, including the principal technical challenges, methodological trends, representative approaches, and emerging research directions. By systematically analyzing and categorizing the reviewed studies, we identify common design principles, unresolved limitations, and opportunities for future development, providing a comprehensive overview of the evolving landscape of safe learning for contact-rich manipulation. 

### **Categorization of Methods from Different Perspectives** 

This section organizes existing safe learning approaches for contact-rich robot tasks along several complementary dimensions to clarify their underlying assumptions and design trade-offs. By examining methods through perspectives such as task characteristics, sensing and policy modalities, data acquisition strategies, simulation environments and benchmarks, safety evaluation metrics, safety abstraction levels, and safety enforcement spaces, the survey highlights common patterns and gaps that are not apparent from any single taxonomy. This multi-view categorization also helps connect classical control-theoretic techniques with modern learning-based and foundation-model-based approaches, providing a unified lens for analyzing current methods and guiding future developments. 

The **definition of contact-rich tasks** varies in the literature, and it was also referred to by different terms such as physical interaction tasks [34], or manipulation in 

6 

contact [12]. According to our definition, a task is contact-rich when its successful execution requires dynamic and sustained physical contact with the environment, where motion and force are tightly coupled through contact constraints. 

In this regard, for instance, obstacle avoidance is not a contact-rich task: even though contact can happen sometimes, the task can be accomplished without contact. Simple pick-and-place tasks are not included even though they involve contacts with objects, because these contacts are fixed (i.e., not dynamic) after the grasp. However, tool-use tasks where the grasped object interacts with the environment, or in-hand manipulation where the contacts between the object and the robot hand are not fixed, are considered contact-rich. The definition also excludes the impact-based tasks such as throwing [35], hitting [36] or catching [37] an object, in which the contact is momentary or sparse (i.e., not extended). These tasks are dynamic, but not contact-rich. 

Some examples of typical contact-rich tasks are peg-in-hole insertion, surface grinding, massaging a human, multi-finger manipulation, vegetable cutting, and box pushing (Fig. 2). We advance our discussion on the contact-rich tasks in _ContactRich Task Categories_ , by grouping the tasks in the reviewed literature into four main categories, and presenting uncommon task variants that introduce novel challenges. 

The defining features of contact-rich tasks, namely dynamic, sustained contact with tightly coupled motion and force, are what make them uniquely challenging from a safety standpoint in three interrelated ways. First, the dynamics are _hybrid and discontinuous_ : as the system transitions between free motion, impact, sticking, and sliding, the governing equations and the set of active contact constraints switch abruptly, so a single smooth certificate (e.g., one Lyapunov function or one control barrier function) often fails to remain valid across mode boundaries, and one may instead require multiple Lyapunov functions or mode-aware certificates (see _Provable safety methods_ ) [34, 38, 39]. Second, motion and force are _tightly coupled_ : at contact, position-tracking and force-regulation objectives directly conflict, since commanding a position into a stiff surface produces large interaction forces, and safety therefore cannot be reasoned about in position space alone. Compliant parameterizations such as impedance and admittance control make this trade-off explicit, which is also why the learning-based methods surveyed here predominantly output pose/force/impedance references rather than raw torques. Third, these two properties raise the _relative degree_ of the safety constraints: physically meaningful limits such as contact-force envelopes and friction cones depend on the contact mode and on higher-order derivatives of the configuration, which complicates the synthesis of provable safety filters and is a recurring difficulty for high-relative-degree CBFs in contact-rich settings [40–42]. 

### **Definition of Safety in Contact-Rich Tasks** 

The definition of safety in contact-rich manipulation spans multiple, complementary notions that arise from diverse objectives, stakeholders, and operational contexts [23]. Rather than a single definition, safety should be understood along several axes: physical interaction and energy exchange; stability and invariance; constraint satisfaction and reachability; risk- and data-driven guarantees; human-centered factors and standards [43]; and phase- and level-specific integration (exploration vs. execution; 

7 

planning vs. control). We formalize these axes and situate them within contact-rich robotics with representative references. 

**Physical interaction safety, including contact force, energy, and passivity,** forms a primary foundation for safety in contact-rich manipulation. Excessive normal or tangential forces, whether arising as high transient impacts at contact onset or as sustained interaction forces during steady contact, can damage workpieces and tooling or injure humans in collaborative settings. A practical definition of safety therefore specifies force envelopes over time, including bounds on force magnitude, rate of change, and impulse, together with region- or phase-specific limits (e.g., fragile surfaces and no-touch zones). Reviews on interaction, impedance control, and force regulation provide formal treatments of these aspects and their implications for stability [2, 44]. 

Achieving force-centric safety requires (i) reliable sensing/estimation of contact forces and states, (ii) controllers that prioritize force regulation under uncertainty, and (iii) runtime mechanisms that enforce hard limits. Force/torque sensing combined with observers and multimodal perception [45] supports contact-state estimation (onset, sticking/slip) and force-grounded policy inputs; this enables early guard actions (e.g., approach deceleration, alignment) to reduce peaks and avoid lateral overload. Classical hybrid position-force control and impedance/admittance control provide physically interpretable means to track force references while maintaining compliant interaction; variable impedance schemes adapt stiffness/damping online to keep forces within bounds amid modeling error and task variation [2, 44]. In learning-integrated systems, producing high-level references (pose/force/impedance gains) rather than direct torques helps preserve stability margins while meeting force objectives [2, 46]. 

Enforcement at execution time benefits from casting force bounds (and friction cones) as constraints. Model-based safety filters, such as MPC with hard/soft constraints or barrier-based action projection, can minimally modify a nominal (possibly learned) command to preserve admissible contact forces, especially near transitions (free-space to contact, contact to sliding). This projection viewpoint also supports chance/risk-aware limits to reduce rare but damaging force spikes [46–48]. When specifications are given in natural language or task rules (e.g., “do not exceed 5 N on cable,” “avoid pressing the painted surface”), grounding them into formal force/region constraints and injecting them into the safety layer provides reliable guardrails during execution [24, 35]. 

Energy and passivity complement the force-first view by regulating how much energy the robot injects into the environment. Passivity indices and energy reservoirs (energy tanks) offer monitors and buffers that cap impact energy and prevent force runaway under delays, unmodeled compliance, or high-gain settings. In practice, combining passivity-aware impedance/admittance with explicit force envelopes yields robust behavior across approach, impact, and sustained-contact phases, and remains compatible with learning-based references and uncertainty-aware shields [2, 44, 46]. 

**Stability and invariance, as characterized by Lyapunov and control barrier function (CBF) formulations,** provide a second perspective on safety by treating it as stability and set invariance. Lyapunov methods certify convergence or boundedness and can imply safety when safe sets are invariant sublevel sets of a Lyapunov function [49, 50]. Control Barrier Functions (CBFs) enforce forward invariance 

8 

of safety sets online by minimally modifying actions to prevent constraint violations, and have seen increasing use in contact-aware robotics and safe reinforcement learning [10, 51–53]. End-to-end safe RL can further embed barrier-based constraints into training or runtime filtering [54, 55]. From this perspective, safety means remaining within certified invariant sets while preserving task feasibility. 

**Constraint satisfaction and reachability** provide another complementary view of safety by emphasizing the persistent satisfaction of physical constraints. Safety is defined through state, input, and contact constraints, including joint, velocity, and torque limits, friction cones, and contact-force envelopes. Safe MPC enforces these constraints over a prediction horizon using robust tubes or uncertainty sets [56, 57]. Hamilton–Jacobi reachability and safety filters compute (or approximate) safe sets and veto actions that would leave them [23, 58, 59]. Under this constraint-centric view, safety is achieved by maintaining physically meaningful bounds throughout approach, impact, sliding, and re-grasp phases. 

**Risk- and data-driven safety** complements analytical formulations by quantifying safety through statistical measures of uncertainty and risk. Data-driven definitions characterize safety using risk-sensitive objectives, recovery regions, or auxiliary critics that predict and penalize unsafe outcomes. Recovery RL separates exploration from recovery to reduce unsafe excursions [60], while safety critics and pessimistic objectives downweight risky actions under uncertainty [7, 9, 61]. Recent work further provides theoretical formulations, including safe value functions, shielding, and generalization guarantees, that connect statistical learning with formal notions of safety [62, 63]. From this perspective, safety is expressed as a probabilistic guarantee or risk bound over contact outcomes under imperfect models and noisy sensing. 

**Human-centered and standard-driven safety** extends the notion of safety beyond robot performance to include human well-being and acceptability. In human– robot collaboration and assistance, safety must address not only physical limits, such as contact pressure, speed-and-separation distance, and ergonomics, but also perceived safety, including predictability, comfort, and trust [2, 64]. Standards such as ISO 10218 and ISO/TS 15066 codify acceptable limits and safety procedures, shaping permissible forces, speeds, and safety-rated monitoring [31, 65]. Perception- and policy-level safeguards further reduce human exposure to risk during collaborative and assistive tasks [66–69]. Accordingly, safety encompasses not only protecting robots and objects but also ensuring human well-being and acceptance. 

**Semantic safety enabled by vision-language(-action) models** introduces a higher level of safety reasoning by aligning task intent, environmental context, and contact constraints with robot execution. In contact-rich settings, semantic safety requires grounding task semantics, including objects, affordances, no-touch regions, insertion axes, and force limits, together with safety rules such as force thresholds, PPE requirements, and human proximity, into actionable constraints and runtime monitors for execution [46]. 

It is useful to separate two notions that are easily conflated. _Semantic (task-level) safety_ concerns whether the model selects an appropriate, non-harmful plan, for example, refusing an unsafe instruction, identifying a fragile object or a no-touch region, 

9 

and choosing a sensible approach. _Physical contact safety_ concerns whether the _executed_ interaction respects quantitative limits on force, impulse, velocity, and contact region. The two are not interchangeable: a plan can be semantically correct yet still produce an unsafe contact, and a semantically awkward plan can remain physically safe if the low-level controller bounds the interaction. The current state-of-the-art VLAs contribute to semantic safety and reasoning, including parsing intent and grounding constraints. In contrast, physical contact safety is still ensured by the downstream compliant or shielding layer (impedance control, CBF/MPC/reachability filters) rather than by the language model itself. We use “semantic safety” for the former and reserve force/region/impulse guarantees for the latter throughout this survey. 

Modern VLM/VLA systems can (i) parse natural-language goals and safety rules, (ii) ground them in the sensed scene (objects, surfaces, grasp points) [24, 27, 70, 71], and (iii) parameterize low-level compliant controllers or skill libraries with safetyaware references (pose/force/impedance) [4, 72, 73] rather than direct torques. Typical architectures use a hierarchical split: a language–vision planner selects certified skills/options; mid-level skills expose safety-relevant parameters; low-level safety enforcers (impedance, CBF/MPC, rate limiters) guarantee contact stability and constraint satisfaction during execution [73–76]. We instantiate this hierarchical split concretely in the Safety Abstraction Level section (Fig. 9), where the plan–parameterize–enforce stack is shown with named modules and example systems, alongside a representative failure mode in which the low-level shield catches a mis-grounded language constraint. 

**A general problem formulation for contact-rich manipulation** considers tasks arising across assembly, insertion, forceful surface interaction, and human–robot collaboration. We adopt a formulation that does not commit to a single mathematical model. Tasks are described by (i) a state representation _xt_ that includes robot kinematics and dynamics, latent contact modes, and measured or estimated wrenches; (ii) a control signal _ut_ that may consist of low-level torques or velocities, or higher-level references such as force targets and impedance/admittance gains; and (iii) safety and feasibility specifications involving force and torque envelopes, friction and approach cones, motion limits, and human-centric constraints [2, 44, 46]. Depending on the underlying assumptions and application requirements, the decision model may be formulated as an unconstrained Markov decision process (MDP), a partially observable Markov decision process (POMDP), a constrained Markov decision process (CMDP), or a hybrid systems/control-theoretic framework with explicit contact transitions. Across these formulations, safety is operationalized through limits on contact forces, pressures, and motion, potentially augmented by risk-aware or semantic constraints [4, 24, 35, 46]. 

Observability and abstraction are key design choices. When direct force/torque sensing is available, controllers can track force references and tighten safety envelopes; otherwise, observers or learned estimators provide wrench/contact-state cues for policy inputs and online monitoring [44]. Action abstraction often improves safety and simto-real transfer: outputting pose/force targets or impedance parameters instead of raw torques yields compliant interaction and clearer hooks for runtime safety mechanisms [2, 44, 46]. Finally, semantics (VLM/VLA) supply high-level task structure and safety 

10 


**Figure 3** Structure of this survey. We introduce the background and definitions in the beginning of, and categorize existing methods from different perspectives, including task characteristics, sensing and policy modalities, data acquisition strategies, simulation environments and benchmarks, safety evaluation metrics, safety abstraction levels, and safety enforcement spaces. Our results consist of the discussion of open challenges and new perspectives. 

rules that must be grounded into formal constraints and checked during execution [4, 24, 35, 77, 78]. 

Fig. 3 provides an overview of this survey. Our review is based on the background and key definitions given at the beginning of _Robotic Contact-Rich Tasks and Definition of Safety in Contact-Rich Tasks_ . The core of our review is organizing related work from multiple perspectives, covering task characteristics, sensing and policy modalities, data acquisition strategies, simulation environments and benchmarks. Our results are presented as the identified key challenges and new perspectives. 

11 

**Learning paradigms for safe contact-rich manipulation** can be broadly categorized into reinforcement learning, imitation learning, learning-enhanced model-based control, foundation-model-based methods, and hybrid integration, each interfacing with safety through different mechanisms. 

**Reinforcement learning** learns policies for variable-impedance forceful skills and insertion tasks, often using action spaces that output force targets or stiffness and damping parameters to preserve compliant interaction. Safety is enhanced through conservative objectives, recovery strategies, and shielded execution mechanisms, such as barrier-function, reachability-based, and MPC-based safety layers [17, 79–83]. 

**Imitation learning** acquires initial policies for contact sequencing and force modulation (e.g., approach, touch, and sliding) from demonstrations. These policies are commonly refined through reinforcement learning or supervised updates, while hybrid trajectory-force learning has become prevalent in insertion and assembly tasks [33, 84, 85]. In this survey, we focus on methods with a substantial online learning component and refer readers to recent surveys for purely imitation-learning approaches [19]. Although VLA policies are typically trained through imitation learning, we include them under the criterion defined in the Robotic Contact-Rich Tasks section, because they incorporate explicit safety mechanisms and/or online refinement rather than simply replaying demonstrations. 

**Learning-enhanced model-based and control-theoretic methods** combine learning with established control frameworks, including impedance and admittance regulation, robust and adaptive force control, MPC with contact constraints, and barrier- or reachability-based safety filters. In these approaches, learning augments classical controllers by identifying system dynamics, adapting controller gains, or shaping feasible sets, thereby improving adaptability while retaining transparent runtime safety enforcement [38, 53, 86–88]. 

**Foundation-model-based methods** leverage large-scale vision-language (and action) pretraining to interpret open-ended task descriptions, infer affordances, and generate safety-aware plans before execution. In contact-rich settings, these methods are commonly organized into a plan–parameterize–enforce pipeline: (i) a VLM/VLA interprets natural-language goals and scene context to generate task sketches and safety rules (e.g., force thresholds, no-touch regions, and speed limits); (ii) the resulting semantic plan is translated into formal constraints and parameterized skill references (pose, force, or impedance) rather than raw torque commands to preserve compliant interaction [70]; and (iii) certified low-level safety layers, such as MPC or CBF filters and rate limiters, execute the policy while enforcing bounds on contact forces and approach geometry [4, 24, 35]. We discuss these safety guardrails in greater detail in the Safety Abstraction Level section, together with representative systems, an architectural overview, and a worked failure case. 

**Hybrid integration** combines complementary strengths across planning, learning, and formal safety. High-level planning and skill graphs, potentially guided by VLMs or VLAs, provide semantic structure, while learned policies generate pose, force, or impedance references and certified safety layers project actions into admissible sets. Semantic reasoning modules further align high-level task intent and safety rules with 

12 

the certified execution stack [4, 27, 77, 78]. Performance is commonly evaluated using standardized simulation suites and benchmarks that report safety violations, near misses, and generalization performance [48, 89, 90]. 

In this section, we categorize existing **safe learning approaches** for contactrich robot tasks based on the phase: safe exploration (learning before contact) and safe execution (learning during contact) and provable safety methods, and discuss representative methods in each category. This categorization helps clarify the distinct challenges and strategies associated with each phase, as well as their implications for safety in contact-rich manipulation. 

**Safe exploration, corresponding to learning before contact,** is the most safety-critical phase of contact-rich robot learning because unsafe exploration can lead to collisions, excessive contact forces, and hardware damage before a reliable policy is obtained. This section reviews representative methods for safe exploration and discusses how they improve learning efficiency while minimizing physical risk prior to task execution. 

Safe human-robot cooperation (HRC) is a major application branch within the broader class of contact-rich tasks, and it has traditionally been approached through path planning algorithms such as rapidly-exploring random tree star (RRT<sup>_∗_</sup> ) [91] for dynamic human-robot systems, or artificial potential field (APF) [92] and virtual fixtures [93] for real-time adjustment of the robot’s trajectory. However, these methods often yield slow trajectory computation and limited generalization, since they require task-specific tuning, assume simplified environments, and adapt poorly to dynamic or unstructured settings [93]. 

Recent approaches enforce safety constraints via control barrier functions (CBFs), where quadratic programs compute minimal trajectory deviations to maintain safety [94–96]. Extensions to uncertain CBFs (U-CBFs) handle environmental uncertainty [97, 98], though worst-case assumptions often yield conservative designs. Stochastic frameworks using chance constraints offer less conservative alternatives [99, 100], but remain computationally intractable for most HRC applications due to nonconvex feasible regions [101]. Complementary work examines risk factors in HRC [102– 105]. Although these approaches can better characterize tolerable risk bounds for different applications, risk-tunable CBFs can further reduce conservatism [32]. 

Ensuring system safety while maintaining performance requires sophisticated approaches that balance computational efficiency, safety guarantees, and adaptability. Below, we present four prominent categories of methods that address these challenges through different theoretical frameworks and computational strategies. 

Across these reachability-based methods, a common theme is to shift most of the computational burden into the offline construction of trajectory-parameterized reachable sets based on a reasonably accurate model. Reachability-based Trajectory Safeguard (RTS) [59] is an offline–online safety layer for continuous-control RL that precomputes trajectory-parameterized forward reachable sets and, at runtime, projects the RL agent’s chosen plan parameters to a nearest safe plan while preserving learning efficiency. A reachability-based manipulator planner [106] builds joint-space, trajectory-parameterized reachable sets offline and then uses them to 

13 

constrain receding-horizon optimization. Another paper [107] introduces a recedinghorizon planner for mobile robots that performs offline reachability analysis over a continuum of trajectory parameters and then selects safe parameters online. Those approaches rely on a reasonably accurate system model and can be less adaptive when dynamics or obstacles change significantly during operation. 

Model predictive shielding (MPS) [108] provides a model-predictive shield around any RL policy: it forecasts violations and replaces unsafe actions with safe, goaldirected recoveries, enabling zero-violation training and deployment. CBF-Guided MPC [52] embeds barrier constraints in MPC and tunes them online for proactive, explainable hard-safety during tracking/avoidance at the cost of online optimization and careful model or CBF design. These MPC-based methods trade offline precomputation for online optimization to improve task progress with interpretable constraints. Planner-augmented approaches such as MoPA-RL [109] can be viewed as a broader shield that uses classical motion planning (and reactive shaping) to intervene and generate collision-free long-horizon actions around a learned policy, improving exploration and execution safety without CBF-style hard guarantees. 

RTS-style reachability safeguards shift burden offline, enabling fast runtime projection with hard safety so long as the precomputed reachable sets remain valid; their main limitation is reduced adaptivity under model mismatch or rapidly changing contact dynamics. In contrast, MPS and CBF-guided MPC place more computation online: they can respond to changing constraints and goals within a receding horizon, but require repeated optimization and careful dynamics/constraint modeling, with feasibility and real-time performance becoming the bottleneck in high-dimensional HRC. Practically, reachability filters suit fixed platforms with stable dynamics and tight real-time budgets, whereas MPC/CBF variants suit environments where constraints and intent change quickly and online compute is available. 

Implicit Safe Set Algorithm [110]. A model-free safe control method that queries a black-box dynamics (e.g., digital twin) to synthesize a safety index (barrier certificate) and a corresponding safe control law, guaranteeing forward invariance and finite-time convergence. Data-Driven Permissible Safe Control with Barrier Certificates [111] learns unknown stochastic dynamics via Gaussian Processes and constructs piecewise stochastic barrier functions to compute a maximal set of permissible strategies that satisfy a target probabilistic safety level; as data increases, the permissible set grows toward the known-model benchmark while maintaining safety. Together with safe exploration methods [112–114], these approaches illustrate how pre-deployment safe learning can constrain exploration to certified-safe behaviors before execution. 

Advantage-Based Intervention [115] achieves safety by online interventions and surrogate MDP training (requires a safe backup policy/advantage estimates), whereas AlwaysSafe [116] achieves safety by a model-based abstraction of safety dynamics (requires a correct abstraction); both enable safe data collection for learning. 

Reachability filters policy actions via offline reachable sets for real-time, hard-safety execution; MPC/CBF enforces safety online via predictive checks and constraints with interpretable but optimization-heavy control; safety-set constructs invariant or permissible safe regions model-free or GP-based for certified operation; and safe exploration 

14 


**Figure 4** Hexagonal ratings across six comparison axes (higher values indicate stronger relative performance on a 1–5 scale). (A1) Guarantee strength: 1 = empirical/heuristic only, 5 = hard safety (invariance/reachability-style). (A2) Model independence: 1 = requires an accurate known model, 5 = model-free / black-box / learned abstraction. (A3) Online efficiency: 1 = heavy online optimization, 5 = lightweight runtime (most computation offline). (A4) Conservatism / tunability: 1 = highly conservative with few tuning knobs, 5 = explicitly risk-tunable and typically less conservative in practice. (A5) Scalability / real-time viability: 1 = struggles in high-dimensional contact-rich or multi-agent settings, 5 = scales well and runs in real time. (A6) Data efficiency (safe learning): 1 = data-hungry, 5 = requires little data to ensure safety or supports efficient safe data collection. These ratings are an explicit, rubric-based _relative_ synthesis, not benchmark measurements: the 1–5 anchors for each axis are defined in Table 1, the per-method rationale and supporting evidence are given in Table 2, and each score was assigned independently by two of the authors using that rubric and reconciled by discussion. 

guarantees no violations during learning via interventions or abstract safety models, trading flexibility and sample efficiency against model/backup policy assumptions. 

Here we group learning-based methods by what they learn and how they ensure safety. Lyapunov actor–critic [117] learns policy weights under an explicit Lyapunov constraint, and executes through an adaptive impedance layer for compliant, stabilityguaranteed motion. Safety-Aware Unsupervised Skill Discovery [118] learns a skill policy and a safety critic that estimates failure probability, yielding intrinsically safe skills for downstream tasks. Variable-Impedance Skill Learning [119] learns a latent skill prior/decoder, a latent policy, and impedance as part of the action, 

15 

**Table 1** Scoring rubric for the hexagonal ratings of Fig. 4. For each axis we give the anchors for scores 1, 3, and 5 on the relative 1–5 scale; scores of 2 and 4 denote intermediate cases that interpolate between adjacent anchors. The ratings are an ordinal, relative synthesis across the cited studies, not absolute benchmark measurements. 

|**Axis**|**Score 1**|**Score 3**|**Score 5**|
|---|---|---|---|
|A1 Guarantee strength|Empirical / heuristic<br>only|Stability- or<br>probability-based<br>guarantee|Hard safety (set<br>invariance /<br>reachability)|
|A2 Model independence|Requires an accurate<br>known model|Approximate or<br>partially identified<br>model|Model-free /<br>black-box / learned<br>abstraction|
|A3 Online efficiency|Heavy online<br>optimization|Moderate per-step<br>optimization (e.g., a<br>QP)|Lightweight runtime<br>(most computation<br>offline)|
|A4 Conservatism / tunability|Highly conservative,<br>few tuning knobs|Some tunable safety<br>margins|Explicitly<br>risk-tunable, less<br>conservative in<br>practice|
|A5 Scalability / real-time|Struggles in<br>high-dimensional<br>contact-rich or<br>multi-agent settings|Moderate (limited<br>horizon or contact<br>count)|Scales well and runs<br>in real time|
|A6 Data efficiency|Data-hungry|Moderate data<br>requirement|Little data needed, or<br>supports efficient safe<br>data collection|


achieving safety via compliant interaction and bounded contact forces. Impedancelearning adaptive control for HRI [120] learns impedance gains, feedforward interaction force, dynamics parameters, and robust Sliding Mode Control (SMC) gain, with Lyapunov proofs of bounded tracking. Impedance iterative-learning SMC [121] updates impedance and SMC gains across trials, combining compliance and robustness guarantees for non-repetitive tasks. Model-accelerated maximum-entropy RL for highprecision assembly [122] learns a stochastic policy executed through an impedance controller and leverages a GP dynamics model for sample-efficient training, achieving practical safety via compliant interaction. 

Learning-based approaches directly optimize policies, skills and impedance from data, offering greater adaptability to unmodeled dynamics and complex contact phenomena with less hand-crafted modeling, most advantageous when rich demonstrations or interactive rollouts are available and the task/environment is hard to model yet demands fast, compliant behavior under distribution shift. 

Since the literature lacks a unified benchmark that evaluates different safety paradigms on the same contact-rich task under matched conditions, the comparisons in this section are necessarily synthesis-based: we distill the reported assumptions, guarantees, and practical constraints from the above studies into a common set of criteria. To provide a unified lens for analyzing trade-offs across method families, we compare them using six recurring axes: (A1) guarantee strength/type (hard invariance/reachability vs. probabilistic vs. empirical), (A2) model reliance (known dynamics vs. approximate/black-box vs. data-driven), (A3) compute placement (offline precomputation vs. online optimization/filtering), (A4) conservatism and risk 

16 

**Table 2** Per-method rationale for the hexagonal profiles in Fig. 4, scored with the rubric of Table 1. We give the qualitative justification and supporting references for each method family; the plotted 1–5 values themselves are shown in Fig. 4. Two of the authors assigned scores independently using the rubric and reconciled disagreements by discussion. 

|**Method family**|**Rationale for its A1–A6 profile (with supporting**<br>**references)**|
|---|---|
|RTS (reachability-based safeguard)|Strong guarantee (A1: hard reachability invariance) and online<br>efficiency (A3: reachable sets precomputed offline, lightweight<br>online projection), and data-efficient (A6: model-based safety<br>preserves RL learning); lower model independence (A2: needs a<br>reasonably accurate model) and tunability (A4: few online knobs,<br>conservative under mismatch) [59, 106, 107].|
|MPS (model predictive shielding)|Strong guarantee (A1: forecasts and substitutes unsafe actions<br>for zero violation) and adaptivity within the horizon (A4); lower<br>online efficiency (A3: receding-horizon optimization each step)<br>and model independence (A2: needs a predictive model)<br>[108, 123].|
|CBF-QP safety filter|Strong guarantee (A1: forward invariance when assumptions<br>hold) and good online efficiency (A3: a cheap per-step QP); can<br>be conservative under uncertainty (A4 low for worst-case<br>U-CBFs) and depends on an accurate model (A2 low) [94–96].|
|Risk-tunable CBF|Like the CBF-QP filter but with explicit risk tuning (A4 high,<br>less conservative) at a probabilistic rather than hard guarantee<br>(A1 moderate); still an online QP (A3 moderate) [32].|
|Lyapunov actor–critic (+ impedance)|Strong model independence (A2: largely model-free policy with<br>an impedance layer) and lightweight execution after training<br>(A3); guarantee is stability-based rather than hard invariance<br>(A1 moderate) and effectiveness depends on training coverage<br>(A6 lower) [117, 119, 124].|
|Advantage-based intervention|Designed for safe exploration: supports efficient safe data<br>collection (A6) and is model-free (A2 high); guarantee depends<br>on a safe backup policy (A1 moderate) and conservatism is set<br>by the intervention frequency (A4 moderate) [60, 115].|


tuning (worst-case bounds vs. chance levels vs. tunable safety margins), (A5) scalability and real-time viability (state dimension, horizon length, contacts/multi-agent), and (A6) data/sample efficiency (how safety constraints affect exploration and learning speed). In Fig. 4, we summarize these axes using hexagonal ratings for representative methods. To complement the qualitative hexagonal view with an explicit, inspectable basis for these scores, Table 3 compiles the underlying criteria for the same representative method families, guarantee type, model assumptions, compute placement and cost, conservatism/tunability, and data efficiency, so that the figure and the table are mutually consistent. The table columns map to axes A1 (guarantee strength/type), A2 (model reliance), A3 (compute placement), A4 (conservatism/tunability), and A6 (data/sample efficiency); axis A5 (scalability/real-time viability) is discussed qualitatively in the synthesis paragraph below and reflected in Fig. 4. 

Across the six axes (A1–A6), the literature reveals a recurring trade-off between guarantee strength and adaptability/compute. Classical planning and reactive shaping are intuitive but often provide weaker or indirect guarantees and require task-specific tuning, limiting scalability in dynamic HRC. CBF-style methods offer explicit, interpretable safety enforcement with strong guarantees when modeling assumptions hold, but can become conservative under uncertainty (e.g., worst-case U-CBFs) or computationally heavy when using less conservative probabilistic constraints. Learning-based 

17 

compliant skills improve adaptability to complex contact phenomena and can achieve practical safety via compliance and stability arguments, but their effective safety depends on training coverage and may trade formal hardness for data requirements. Reachability-based safeguards deliver the strongest hard-safety behavior with predictable runtime by shifting computation offline, yet rely on accurate models and can be less adaptive under mismatch or rapidly changing environments. MPC/shielding approaches sit between these extremes, improving adaptivity through online prediction and constraint handling but incurring repeated optimization costs and feasibility concerns in high-dimensional contact-rich settings. Safe-set/certificate construction and intervention/abstraction-based safe exploration further enable pre-deployment or training-time safety, but their conservatism and scalability are governed by certificate fidelity, backup/abstraction correctness, and how often safety mechanisms override exploration. 

**Safe execution, which focuses on maintaining safety after contact has been established,** is crucial in contact-rich robotic tasks because robots must interact not only with complex and uncertain environments but often also in close proximity to humans [2]. During these interactions, unsafe behaviors can damage the robot, the manipulated objects, or even endanger human safety. Ensuring safe execution therefore requires that robot actions consistently satisfy physical constraints [125], avoid hazardous situations, and maintain robust performance despite uncertainties and disturbances. These requirements become particularly critical in real-world deployments, where unpredictable events and unmodeled dynamics are inevitable. Consequently, developing methods that provide reliable safety guarantees during execution is essential for the trustworthy deployment of robots in contact-rich environments. 

A widely adopted and effective approach to enhance safe execution in contactrich robotic tasks is the use of compliant controllers [16, 119, 120, 126, 127]. These controllers enable robots to interact safely with their environment and with humans by allowing controlled flexibility and adaptability in response to external forces. Among the most common compliant control strategies are impedance control and admittance control. Impedance control regulates the dynamic relationship between the robot’s motion (position or velocity) and the forces it experiences, effectively making the robot behave like a virtual mass-spring-damper system [127]. This allows the robot to absorb impacts and maintain stable contact with uncertain or moving surfaces. Admittance control, on the other hand, measures external forces and commands the robot to move accordingly, making it suitable for tasks where the environment imposes significant forces on the robot [128, 129]. Both approaches are fundamental in ensuring that robots can safely and robustly perform manipulation tasks involving physical contact, reducing the risk of damage or injury during interaction. 

One key challenge in ensuring safe execution is properly tuning controller parameters (such as stiffness, damping, and inertia) to suit different task scenarios and contact conditions [44]. Incorrect parameter settings can lead to unsafe behaviors, such as excessive contact forces, instability, or failure to accomplish the task. Traditionally, these parameters are manually tuned based on expert knowledge and trial and error, which is time-consuming and may not generalize well across diverse tasks or environments. 

18 

Learning-based methods offer a promising solution by automatically adapting controller parameters through data-driven optimization, enabling robots to achieve both safety and high performance in varying and uncertain contact-rich scenarios [26, 27]. 

A major research direction in safe execution for contact-rich tasks is the use of RL to automatically tune the parameters of compliant controllers [3], such as impedance or admittance control. In these approaches, RL algorithms are employed to learn optimal values for parameters such as stiffness [79], damping, and inertia, enabling the robot to adapt its compliance to varying task requirements and contact conditions [130]. This data-driven adaptation helps maintain safety by minimizing excessive contact forces, preventing instability, and improving task performance. 

Recent research has demonstrated the effectiveness of RL-based parameter learning in a variety of contact-rich scenarios. For example, RL has been used to adjust impedance parameters online to ensure safe and robust assembly [17, 131–133], insertion [134–136], and surface interaction tasks [137]. Some works incorporate safety constraints directly into the RL framework, such as limiting the maximum allowable force or ensuring stability margins during learning [54, 79, 138]. Others combine RL with model-based safety filters [139] or control barrier functions [140] to guarantee constraint satisfaction throughout the learning and execution process [79]. 

These methods offer several advantages: they reduce the need for manual parameter tuning, allow for adaptation to unmodeled dynamics or changes in the environment, and can explicitly balance safety and performance objectives. However, challenges remain in ensuring sample efficiency, generalization across tasks, and providing formal safety guarantees during both training and deployment. Ongoing research continues to address these issues by integrating uncertainty estimation, risk-sensitive objectives, and hybrid learning-control architectures. 

Large vision-language(-action) “robot foundation” models also contribute to safe execution by converting unstructured scene and instruction inputs into structured, verifiable plans that parameterize compliant low-level skills. Because these mechanisms recur across the survey, we consolidate their detailed treatment in the plan–parameterize–enforce architecture, concrete example systems, and a worked failure mode in the Safety Abstraction Level section, rather than repeating it here. 

**Provable safety methods** provide the theoretical foundation for understanding and certifying safe learning in contact-rich robotic tasks. Long before learning-based approaches became prevalent, robotic safety was extensively studied within classical control through mathematically rigorous frameworks for stability and safety analysis [34, 49, 58, 127]. These include Lyapunov-based methods, control barrier functions (CBFs), contraction metrics, reachability analysis, and invariant-set theory, which offer formal guarantees of stability, safety, and constraint satisfaction [50, 141–143]. Although originally developed for model-based control, many of these techniques have increasingly been integrated into modern learning-based frameworks [23, 68, 144–147]. The following subsections review these foundational approaches and discuss their role in enabling provably safe learning for contact-rich robotic manipulation. 

**Lyapunov-based methods** build on the concept of a Lyapunov function, a scalar energy-like function _V_ ( **_x_** ) that decreases along trajectories of a dynamical system. Formally, consider a system **_x_** ˙ = _f_ ( **_x_** _,_ **_u_** ) with state **_x_** _∈X_ and control input **_u_** _∈U_ . 

19 

A continuously differentiable function _V_ : R<sup>_n_</sup> _→_ R _≥_ 0 is a Lyapunov function for a closed-loop system if it is positive definite ( _V_ ( **0** ) = 0, _V_ ( **_x_** ) _>_ 0 for **_x_** _̸_ = **0** ) and its time derivative is negative semi-definite ( _V_<sup>˙</sup> ( **_x_** ) _≤_ 0 _∀x_ ). For safety, Lyapunov analysis is often used to certify invariant sets. If we can identify a set of safe states _S_ ( _e.g. S_ = _{_ **_x_** _| V_ ( **_x_** ) _≤ c}_ ) and a Lyapunov-like function _V_ ( **_x_** ) that decreases or stays constant on _S_ , then any trajectory starting in _S_ will remain in _S_ for all time, making _S_ a forward-invariant safe set [49]. 

Lyapunov-based methods are well-suited to scenarios where the main objective is stability, for example, regulating contact force to a desired value. Nearly all classical robot controllers, e.g., PD controllers or compliance controllers, are derived with an implicit Lyapunov function to prove stability [117, 148, 149]. Passivity-based control is another Lyapunov-related approach. By designing the closed-loop system to be passive, one can guarantee stable interactions, which means the robot can safely interact with the environment because it will not generate energy that could cause instability [144, 145, 150–152]. 

Despite their broad use, a major challenge for Lyapunov methods is finding a suitable Lyapunov function for complex nonlinear systems [49]. For high-dimensional robots with complex contact dynamics, hand-designing a _V_ ( **_x_** ) that decreases in all conditions, especially across contact/non-contact modes, is difficult. In hybrid systems, standard Lyapunov theory does not directly apply and one may need multiple Lyapunov functions [39, 153, 154]. Another limitation is that classical Lyapunov methods are primarily designed to certify stability or asymptotic convergence of the closed-loop system. Unless the Lyapunov sublevel sets are explicitly constructed to be forward invariant and contained in a prescribed safe set, Lyapunov stability alone does not guarantee that state or input constraints are respected along the entire transient [155, 156]. In particular, a Lyapunov-stable controller may drive a robot back to its desired equilibrium after a disturbance but still allow temporary violations of safe force or workspace limits [157, 158]. Therefore, Lyapunov-based designs are well-suited for ensuring long-term stability or boundedness, but typically need to be augmented with barrier-type conditions to enforce state constraints and safety [51, 141]. 

**Control barrier functions (CBFs)** provide a formal, Lyapunov-like tool specifically for enforcing safety constraints. While Lyapunov functions certify the stability of an equilibrium, barrier functions certify forward invariance of a safe set, which proves the system will never enter certain unsafe regions [51, 155, 159]. The typical setup is as follows: Define a continuously differentiable scalar boundary function _h_ ( **_x_** ) such that the safe set _C_ is _{_ **_x_** _| h_ ( **_x_** ) _≥_ 0 _}_ and the unsafe set is _{_ **_x_** _| h_ ( **_x_** ) _<_ 0 _}_ . As an example, the boundary _h_ ( **_x_** ) = 0 can describe the contact force reaching a limit. A valid CBF satisfies a condition that ensures _h_ ( **_x_** ) cannot decrease into the negative unsafe region. One common form: There exists an extended class- _K_ function _α_ ( _·_ ) such that for all states on the boundary of _C_ , we can choose control inputs **_u_** to yield _h_ ˙ ( **_x_** _,_ **_u_** ) _≥−α_ ( _h_ ( **_x_** )). If this holds, then whenever _h_ ( **_x_** ) is zero or positive, its derivative cannot drive _h_ ( **_x_** ) across the zero boundary into the unsafe region. Geometrically, _h_ ( **_x_** ) can be seen as a ”barrier” that goes to zero at the safety boundary and typically to negative values outside the safe set. The CBF condition forces the controlled 

20 

dynamics to hover at or increase _h_ ( **_x_** ) at the boundary, never allowing a drop below zero [158]. 

CBFs are especially powerful for real-time enforcement of safety constraints. Unlike open-loop potential field methods [160, 161], CBFs offer a guarantee of safety because the CBF condition is a hard constraint on the control input. 

Despite their strengths, CBFs come with several challenges. First, they require a reasonably accurate model of the system and environment. Model uncertainty or external disturbances can break the guarantee. There is active research on robust CBFs and adaptive CBFs to account for uncertainty, but guaranteeing safety under uncertainty often leads to conservative controllers [162–164]. Second, there can be conflicts between multiple CBFs or between a CBF and control goals. It is possible that no single controller can simultaneously satisfy all constraints and achieve the desired motion. In such cases, typically one should relax constraints [165, 166]. Third, the design of CBFs becomes significantly more involved for safety constraints with high relative degree, such as contact and force constraints that depend on higher-order derivatives of the state, which are ubiquitous in contact-rich robotic tasks [40–42]. 

**Contraction metrics** offer a fundamentally different viewpoint than the Lyapunov-based and CBF methods that provide scalar certificates for stability or safety with respect to particular equilibria or safe sets. Rather than analyzing the behavior of trajectories relative to a fixed point or a boundary, contraction theory studies the evolution of the differential distance between arbitrary trajectories of a dynamical system. A system is said to be contracting if infinitesimal displacements between trajectories converge exponentially to zero under an appropriate Riemannian metric. When such a contraction metric exists, all trajectories within a contraction region converge exponentially toward one another, independent of their initial conditions. This yields a strong form of incremental stability: not only do trajectories converge to a specific equilibrium, but they converge toward a unique flow or invariant trajectory structure of the system. The contraction metric thus serves as the formal certificate ensuring this incremental convergence and generalizes classical Lyapunov analysis to trajectory-to-trajectory stability [154, 167–169]. 

A metric is typically given by a positive definite matrix function **_M_** ( **_x_** ) defining a weighted norm _|δ_ **_x_** _|_<sup>2</sup> **_M_**<sup>=</sup><sup>_δ_</sup><sup>**_x_**</sup><sup>_⊤_</sup><sup>**_M_**(</sup><sup>**_x_**)</sup><sup>_δ_</sup><sup>**_x_**forinfinitesimalperturbations</sup><sup>_δ_</sup><sup>**_x_**.Thesystem</sup> **_x_** ˙ = _f_ ( **_x_** _,_ **_u_** ) is contracting with rate _λ >_ 0 if there exists a uniformly positive definite metric **_M_** ( **_x_** ) such that the Jacobian of the dynamics satisfies a matrix inequality: 


Here **_M_** ˙ ( **_x_** ) =<sup>�</sup> _i_ _<u>∂∂x</u>_ **_<u>M</u>_** _i_<sup>_fi_(</sup><sup>**_x_**</sup><sup>_,_</sup><sup>**_u_**)denotesthederivativeofthemetricalongthesys-</sup> tem flow. This term must be included for a state-dependent metric **_M_** ( **_x_** ), and the commonly quoted form without it is recovered only in the special case of a constant metric **_M_** . This condition means the distance between two nearby solutions measured by **_M_** decays at least at rate _λ_ . One can interpret it as a generalized Lyapunov condition applied to the difference dynamics. If we consider the error _|_ **_x_** ˜ _|_ = **_x_** 1 _−_ **_x_** 2 between 

21 

two trajectories **_x_** 1 and **_x_** 2, contraction theory guarantees _|_ **_x_** ˜ _| ≤ ke_<sup>_−λt_</sup> _|_ **_x_** ˜( **0** ) _|_ for some _k >_ 0. A remarkable property is that if a system is contracting, it has a unique equilibrium or invariant trajectory that is globally exponentially stable [168]. In control contexts, we often speak of control contraction metrics (CCMs). A CCM extends the problem to controlled systems. It provides a condition under which a feedback controller can be designed so that the closed-loop system is contracting. If a CCM exists, one can synthesize a controller that achieves exponential tracking of any feasible reference trajectory [154]. 

Contraction metrics are particularly useful in scenarios requiring robust trajectory tracking and disturbance rejection. A major challenge of this approach is finding a contraction metric for a given system, which can be challenging as finding a Lyapunov function. For complicated robots, **_M_** ( **_x_** ) might need to be very complex or even nonexistent in closed form [170, 171]. Another challenge is that contraction typically addresses stability properties but not explicit state constraints [172]. 

**Reachability analysis and invariant sets** approaches compute the set of states from which the system can remain safe indefinitely or the set of states that could lead to an unsafe condition. Techniques like Hamilton-Jacobi (HJ) reachability solve a PDE to find the backward reachable set of an unsafe target [58, 173]. Consider a system whose dynamics are described by an ordinary differential equation **_x_** ˙ = **_f_** ( **_x_** ( _t_ ) _,_ **_u_** ( _t_ )) where **_x_** is the system’s states, **_u_** ( _t_ ) is the control input. To compute the reachable set, a value function _V_ ( **_x_** _, t_ ) is defined whose zero sublevel set _{_ **_x_** : _V_ ( **_x_** _, t_ ) _≤_ 0 _}_ is the backward reachable set of the unsafe (avoid) target, the set of states from which the system cannot avoid reaching that unsafe target within the time horizon, so that the safe set is its complement. This value function satisfies the HJ equation: 


where _H_ is the Hamiltonian defined as 


The optimization over **_u_** _∈U_ in the Hamiltonian encodes the control for the chosen avoid formulation, following the convention of [58, 173]. Intuitively, it propagates the unsafe target backward in time so that the zero sublevel set _{_ **_x_** : _V_ ( **_x_** _, t_ ) _≤_ 0 _}_ collects the states from which the unsafe set cannot be avoided, and safety is maintained by keeping the system in its complement. By solving this equation, the boundary of the reachable set can be obtained, allowing for the analysis of the system’s behavior under various control strategies [174–176]. 

The limitation is the curse of dimensionality. Solving HJ PDEs or exhaustive reachability is only feasible for simplified systems [177–179]. In safe learning contexts, reachability is often used as a runtime safety filter, where the reachable set boundary serves as a constraint. The filter minimally adjusts the nominal control input to satisfy the safety condition, thereby guaranteeing forward invariance of the safe set without strictly limiting the learning agent’s performance [59, 180–183]. 

22 


**Figure 5** We review the contact-rich tasks under four main categories indicated with separate colors. Each category is further divided into sub-categories. The categories are not mutually exclusive. Examples of some downstream tasks that belong to multiple categories are shown as rectangular nodes. 

In this section, we introduce the **contact-rich task categories** from a safetyconcerned online learning methods perspective. In accordance with our scope, we compile and discuss the contact-rich robotics tasks that are tackled with these methods in the literature. For this purpose, we identified the tasks in each of the papers we scanned for this survey. Our analysis shows that the _insertion_ or _assembly_ tasks are the most common type of physical interaction tasks. These are followed by the _surface interaction_ tasks such as polishing and grinding. We also identify the task types of _object manipulation_ and _physical human-robot interaction (pHRI)_ . We reviewed the tasks in the recent works under these four categories as shown in Fig. 5. Details and downstream examples of these categories are given in the following sections. Please see Fig. 2 for example task illustrations. 

Our categorization is application-independent, however, it is possible to categorize the tasks also w.r.t. the application areas such as industry, household and healthcare [19]. Many contact-rich tasks are demonstrated for household applications that cannot be automated, as opposed to industry. These include general household tasks such as wiping a table or a vase [184, 185], inserting a plug [186, 187], and opening a door [188, 189]; and kitchen tasks such as cutting vegetables [57, 190], stirring or scooping food [191, 192], and rolling pizza [193]. Industry applications usually focus on flexible manufacturing tasks such as inserting a gear [131, 194], nut threading [195], building furniture [196], and disassembly [197, 198]. Healthcare applications mostly include the surgery operations [199, 200] and physically assisting humans. 

Please note that there may be overlaps and similarities between the four categories as shown in Fig. 5. For example, many peg insertion tasks could also be seen as object manipulation, or specific tool use tasks may aim for surface interaction. Depending on 

23 

the problem formulation some downstream tasks may bring the challenges of multiple categories, which are detailed below. 

**Assembly and insertion** tasks have been studied in the control literature for a long time both for their importance in industry and the challenges they offer [201]. Robotic solutions to this problem can enable flexible assembly applications [202], and human-like activities such as inserting a key or a plug [203, 204]. 

The challenges include the precision requirement to achieve the tight fit, safety requirements to avoid damaging the equipment or getting stuck, and sensing difficulties as the vision modality is less informative due to occlusions and the force-based nature of the task. Assembly problems may involve multi-step insertion actions to achieve a more complex plan [195, 196]. The classical peg-in-hole task focuses on a single insertion of a securely grasped peg into a single upright hole [205]. The problem is gradually made more challenging through limited or noisy sensor data, leading to uncertainties over the peg and hole poses [206], varying peg shapes and sizes [207], or limited control options, such as rigid position-control [208]. 

Other varieties were introduced for covering different application cases: Inserting multiple pegs (e.g., plugs) simultaneously [209, 210], assembly in obstructed environments that also require path planning [109], bimanually manipulating the hole and peg in the same time [211, 212], multi-stage insertion of vertically complex pegs (e.g., L-shape) [85], inserting into a deformable hole [213], reverse insertion (ring-on-pole) [131], and bolt threading [195]. The task varieties add new challenges such as synchronization between manipulators, added degrees of freedom, added constraints such as obstacles, multi-stage task solving and more complex dynamics. 

Additionally, the _disassembly_ tasks should be mentioned here. They invert the assembly task goal: There is already an inserted piece that has to be removed such as extracting a tightly fit part [198], sliding a bolt along a groove [197], or removing batteries [214]. The challenges of the disassembly tasks are similar to constrained object manipulation tasks such as opening a door or a drawer. However, disassembly presents tighter constraints that may easily lead to jamming. 

**Surface interaction tasks** involve continuous and purposeful physical contact with a surface throughout task execution. They play an important role in both industrial applications that are hazardous to humans, such as sanding [215], and everyday assistive tasks in human environments, including table cleaning [144] and porridge stirring [192]. These tasks usually require keeping a stable contact with the surface and applying consistent force while also following a desired trajectory. Maintaining a precise force and velocity profile enables the consistent quality of results. The problem is made more challenging by varying the surface curvature [148, 216] or tracking complex motion trajectories [217]. The robot may be equipped with a power tool such as a polisher that causes significant vibrations [218]. 

The goal of the surface interaction tasks is to achieve a change on the surface. We observe these tasks under 3 categories: 1. _Surface altering_ tasks that change the surface geometry by removing material, such as grinding and sanding [215, 216]; 2. _surface non-altering_ tasks that do not cause a physical change in the surface, such as wiping and polishing [138, 219]; 3. _particle interaction_ tasks that go beyond the surface and move particles, such as scooping a soft tissue [200] or stirring a granular medium 

24 

[191, 192]. These tasks may require intricate 6-dof maneuvers and high force to move through or process the particles [211]. In case of deformable objects [220], _surface altering_ is easily achieved and revertible; in case of elastic objects such as a sponge [221], shape deformation is temporal and naturally reversed. Massaging is a special surface interaction task that is challenging due to involving a human, thus the safety concerns are more critical [222]. Interaction with deformable surfaces is an underexplored area, attracting more contributions. 

We also identify the _surface exploration_ tasks as a type of surface non-altering tasks that are less explored in the literature. In these works, the touch is fundamental to facilitate navigation and direct the agent towards the goal, such as in blind maze exploration [79, 223]. These tasks are similar to other surface interaction tasks as the interaction is usually non-prehensile and continuous, however, the goal of these tasks is not manipulating the surface, but navigating or following a trajectory [224]. 

Surface interaction tasks are different than the object manipulation tasks as the target object is not expected to move. On the contrary, it is desired to keep the object stable while achieving the surface interaction. The object of these tasks are usually physically constrained, however, wiping the surface of an unconstrained object, such as a vase, requires bimanual coordination to keep it stable during interaction [185]. 

**Object manipulation tasks** involve sustained and dynamic physical interactions with one or more objects throughout task execution. In most cases, the manipulated object itself is the target of the task. However, objects may also be grasped and used as tools to perform physical interaction tasks [225]. Such tools enable indirect interaction with the environment and can facilitate surface interaction, insertion, and other contact-rich manipulation tasks. 

The object manipulation tasks are commonly categorized as prehensile and nonprehensile. The former requires grasping an object, while the latter interacts with the object without holding it, such as pushing [109, 226], sliding [227] and pivoting [228]. Non-prehensile tasks can be done with a simpler manipulator that maintains a single contact with the object, however, they also have a limited control over the object motion. Consequently, the safety of these tasks depend on the motion of the object in challenging environmental conditions: [109] evaluate their method in cluttered environments where collisions are frequent and the object should be moved through narrow paths; the experiments of [226] involve pushing the object through a narrow gap where the object orientation becomes important, or through a bridge with the risk of the object falling. On the other hand, prehensile tasks require at least two contacts with the object to maintain a grasp. Simple grippers can tightly grasp an object, however they do not allow complex object manipulations, thus they are limited to pick-and-place or tool-use tasks. In contrast, bimanual manipulation is done through two high-DoF manipulators, and it can achieve complex interactions with the object such as lifting, pushing, flipping and rotating [118, 229]. Safe bimanual manipulation requires maintaining safe levels of contact forces without dropping the object, in addition to the workspace and motion limits [118]. Multi-fingered hands allow high manipulability of the object with increased control complexity. For a detailed review on dexterous hand manipulation we direct the reader to another survey [29]. 

25 

The object manipulation tasks can be further categorized with respect to the nature of the object, such as constrained, articulated, and deformable. Constrained object manipulation tasks, such as opening a door or a drawer, impose strict kinematic constraints on the object motion [230]. These constraints may lead to high levels of force, if not handled with compliant and adaptive behavior [188]. Objects like a door, drawer or lever are also termed articulated objects [231]. _Disassembly_ tasks are challenging examples of constrained object manipulation. On the other hand, deformable object manipulation is an under-explored research problem that is challenging due to the sensing and modeling complexities [220]. 

**Physical human–robot interaction (pHRI) tasks** require robots to intentionally establish and maintain physical contact with humans, in contrast to human–robot coexistence scenarios, where safety is primarily achieved by avoiding human contact [64, 68]. These tasks present unique challenges because they must simultaneously guarantee human safety and accommodate the inherent uncertainty, variability, and unpredictability of human behavior during physical interaction. Thus, the methods should estimate the human behavior and accommodate the uncertainty [2]. In traditional pHRI, the robot assumes the passive role, and follows the human intention through compliance control. A special case of this is a robot interacting with both the human and the environment, as in [232], where the human guides the robot while it interacts with a surface. In [233], the robot can switch between human-guided and autonomous in-contact manipulation modes to adapt its impedance characteristics. 

The safety-critical contact-rich interactions between an active robot and human fit better to our scope. In prominent scenarios, the robot touches the human while the human takes a passive role, such as eating [234], dressing [69] and bathing assistance [121], ultrasound scanning [146], and massaging [222, 235]. When the robot is physically coupled with the human, such as the rehabilitation robotics, the controller should estimate the human impedance parameters to ensure stability [120]. 

Crucially, the notion of safety expands with the inclusion of a human. For example, [121] limit the vision system to a LIDAR during bathing assistance for ethical considerations. Human _perceived safety_ also becomes important for the trustworthy and socially acceptable interactions [236]. 

26 

# **Takeaway: Safety Across Contact-Rich Tasks** 

The safety notion depends on the type of physical interaction. 

In **assembly and insertion** , safety is closely tied to avoiding jamming, excessive contact forces, and damage under tight geometric constraints. 

In **surface interaction** , the challenge shifts toward maintaining stable, purposeful contact while regulating force, velocity, and trajectory quality over extended interactions. 

**Object manipulation** introduces additional risks through object motion, grasp stability, environmental contacts, and deformable or constrained dynamics. In **pHRI** , safety becomes even broader, incorporating not only physical injury prevention but also uncertainty in human behavior, ethical sensing choices, and perceived safety. While many of these task families have long been studied in robotics, recent work continues to introduce less constrained and more diverse scenarios, including deformable contacts, multi-stage interactions, cluttered environments, and human-centered applications. 

### **Sensing and Policy Modalities** 

In contact-rich manipulation, the choice of policy input has a direct impact on safety. The controller must detect the onset and evolution of contact, respect safety constraints such as joint/torque limits, admissible contact forces and friction cones, and remain robust to modelling errors and partial observability. To this end, modern safe learning pipelines leverage a spectrum of sensing modalities, ranging from purely proprioceptive state, through force/torque and high-bandwidth vision, to rich multimodal and language-conditioned inputs. Table 4 summarizes the dominant input types and how they are typically exploited for safety. 

**Pose and proprioceptive state information** forms the basis of many safe learning approaches, which rely predominantly on proprioceptive and kinematic observations, including joint configurations, end-effector poses, and their derivatives, sometimes augmented with a small number of task-level geometric variables, while omitting explicit force/torque (F/T) measurements from the policy input. In these settings, safety primarily emerges from conservative motion generation, collision-aware planning, and geometric reasoning about contact, often supported by explicit constraints, recovery sets, or safety-oriented value functions [36, 57, 60, 85, 109, 118, 208, 237–240]. 

A first group of approaches couples a compact state representation (pose and velocity) with an explicit description of goals and safety constraints, and then uses model-predictive or safe-RL updates to keep trajectories inside a certified safe set. The policy or controller observes the current system state together with reference poses and bounds on states and inputs, sometimes augmented with uncertainty estimates, safety penalties or human-provided safety signals [57, 68, 118, 238–241]. Because distances to constraint boundaries are part of the observation, the algorithm can reason explicitly about safety margins without having to infer risk from raw contact forces, e.g. tightening constraints near obstacles, slowing down near joint limits, or triggering backup controllers when the state approaches a learned unsafe region. 

27 

A second family of methods organises behaviour around pose-based skills or motion primitives. Here, the observation typically consists of robot joint or end-effector states together with task-relevant geometric features, such as relative part poses or plannergenerated waypoints, while the policy outputs bounded pose increments or selects from a library of safe trajectories [85, 109, 208, 237]. Motion-planner-augmented RL and planner or demonstration-driven frameworks exemplify this pattern. The learned policy reasons over kinematic state and high-level task features, whereas collision-free paths and smooth accelerations are enforced by a downstream planner or stabilising controller. Safety is thus embedded in the way pose sub-goals are parameterised and filtered, ensuring that abrupt or large displacements are routed through a geometryaware planning layer. 

Pose-dominant observations are also used when exteroceptive information is represented directly in configuration space rather than as raw pixels. Benchmark interaction tasks encode the positions of pucks, tools or human partners as Cartesian poses, combined with the robot’s own pose and velocity, so that learning algorithms can enforce distance-based constraints, safety fields around humans, or recovery zones in a low-dimensional geometric space [36, 60, 242]. Even in visuomotor settings where images are available, the safety shaping is often defined over the proprioceptive and pose coordinates through joint limits, collision distances or certified invariant sets, while the visual input mainly serves to infer these geometric quantities or to disambiguate task context [109, 217, 243–245]. Compared with force-centric designs, such pose-based formulations trade direct measurement of contact forces for simpler, more structured safety reasoning in configuration space, and are particularly attractive when high-quality kinematic models and planners are available. 

**Force and torque sensing** provides the primary safety interface for many contact-rich manipulation tasks, particularly insertion, surface following, and physical human–robot interaction. Policies typically combine force/torque (F/T) measurements from the wrist or fingers with joint and end-effector states to regulate contact loads, detect slip or jamming, and adapt impedance so that tracking performance is maintained without violating force or pressure limits [79, 119, 148, 246, 247]. Compared with purely kinematic formulations, these approaches expose safety-critical quantities directly in the observation space, enabling controllers to respond immediately to unsafe contact events in assembly, surface interaction, and terrain-contact scenarios [137, 149, 235, 248]. 

A large family of methods couples F/T sensing with variable impedance or admittance control. The policy input in these works typically concatenates joint or end-effector pose and velocity with measured interaction forces/torques, and sometimes task descriptors such as surface or tissue properties, environment stiffness, or task phase [148, 149, 222, 235]. The action space is parameterized in terms of stiffness, damping, or target forces, and safety is enforced by bounding these impedance parameters, shaping them over time, or embedding stability and performance objectives into the learning problem [119, 249–251]. This pattern appears across industrial assembly and sanding, massage and rehabilitation, and sliding or surface following tasks, where the policy learns to reshape compliance in response to the measured wrench so that interaction forces remain within prescribed envelopes [137, 248, 252, 253]. Some 

28 

approaches further introduce latent policy classes or structured action spaces over impedance parameters, which makes it easier to impose smoothness and magnitude limits on the learned stiffness and damping profiles [233, 246, 254, 255]. 

F/T signals are also combined with explicit safety margins, constraints or stability certificates derived from control theory. In this line of work, the observation space does not stop at raw wrench measurements and state. Controllers additionally receive features derived from Lyapunov functions, control barrier functions, passivity errors or other safety indicators that are computed using the measured forces and state trajectories [47, 117, 146, 233]. Learning algorithms then operate directly on these structured safety variables, for example by penalizing trajectories that approach constraint boundaries, adjusting admittance or impedance gains when passivity residuals grow [81, 256], or biasing exploration away from regions with high estimated risk [68, 147, 221, 248]. This idea extends naturally to uncertainty-aware formulations, where system state, force/torque and uncertainty estimates are combined, and the policy is trained to remain robustly within contact-safe sets despite modelling errors and partial observability [191, 257]. 

In physical human–robot interaction and teleoperation, F/T channels additionally encode human intent and comfort. Many frameworks treat human-applied forces at the end-effector, interaction torques, or teleoperated wrenches as part of the policy input together with robot joint or end-effector state and task phase [120, 232, 258, 259]. These signals are interpreted either as demonstrations of desired compliant behaviour or as real-time preferences over interaction forces, and are used to adapt impedance online, to learn tele-impedance mappings, or to construct task-oriented safety fields around the human partner [64, 252, 260, 261]. Safety here is twofold: the robot must both respect human-specified force envelopes and ensure that the resulting closed-loop behaviour remains stable under changing human dynamics. 

Another recurrent pattern is to use F/T sensing for contact-state estimation, search, and long-horizon assembly. In such settings, policies augment pose and geometry with force histories, contact-state labels, or belief maps over likely contact locations [134, 231, 262, 263]. Contact cues extracted from wrench measurements, such as contact onset, sticking versus sliding, or successful insertion, are then used to gate skills, switch admittance gains, or trigger recovery behaviours when jamming or misalignment is detected [47, 149, 210, 264]. Active-search methods in particular combine end-effector pose and force/torque with Bayesian belief updates and safety features, enabling the robot to probe cautiously, back off when measured forces exceed certified bounds, and refine subsequent search motions while remaining within safe contact regions [146, 219, 257, 265]. Compared with vision-only pipelines, these force-centric designs provide a direct window into the quality of contact, enabling safer behaviour under occlusion, poor lighting, or inaccurate geometric models. 

Even when richer sensory modalities such as vision or tactile arrays are available, force/torque remains a core channel through which safety is enforced. Multimodal policies often use vision primarily to infer geometry and high-level task context, while relying on force/torque and proprioception to regulate local interaction [69, 211, 212, 226]. End-to-end sensorimotor models that consume images, joint state and force/torque 

29 

typically define safety shaping, through penalties, auxiliary critics or recovery policies, over wrench and configuration features rather than pixels, underscoring that F/T sensing is the main substrate on which safe contact behaviour is learned and executed [35, 245, 264]. 

**Vision sensing** provides non-contact, global information about objects, surfaces, and humans that is difficult or impossible to infer from proprioception and force sensing alone. Depending on the camera configuration, visual observations range from bird’s-eye or third-person views covering the entire workspace, to fixed eye-to-hand cameras monitoring a local workspace, and wrist-mounted or eye-in-hand cameras that continuously observe the interaction region from the robot’s perspective [68, 121, 188, 197, 243, 260, 262, 266]. Across these configurations, vision contributes to safety in two complementary ways: by anticipating future contact and potential collisions through scene understanding and geometric reasoning, and by monitoring contact evolution and interaction dynamics in the immediate vicinity of the end-effector. 

Global and external viewpoints are typically used to capture task geometry, object and fastener poses, and human motion. Assembly and disassembly systems exploit RGB or RGB-D images, often converted into scene graphs or object pose estimates, alongside joint and end-effector state to ensure that motion plans respect part tolerances and obstacle constraints before contact is made [122, 188, 197, 202, 245]. Surface-interaction and bathing applications reconstruct patient or workpiece shape from point clouds or depth maps and use this geometry, together with robot pose, to generate reference paths that avoid sharp curvature and maintain safe approach angles during contact [121, 137, 148, 246]. In human–robot collaboration, visual tracking of human pose or trajectories is fused with robot state and sometimes interaction forces to construct task-oriented safety fields around the person. These fields enter the policy input as spatial risk maps that reshape robot motion to avoid unsafe proximity or contact [68, 260]. Pixel-based safe RL and visuomotor world models further push this idea by using raw images as the primary observation, with safety-aware critics or constraint penalties guiding behaviour toward image regions that correspond to safe configurations [60, 118, 243, 266]. 

Local eye-in-hand or wrist-mounted cameras provide a complementary, close-range view that is particularly valuable in contact-rich tasks where the relative pose between tool and environment must be controlled with high precision. Insertion and fastening pipelines use visual estimates of peg–hole or object–fixture pose from such cameras as part of the policy input, so that approach and alignment motions are corrected before large contact forces occur [204, 207, 262, 267]. Diffusion-based compliance policies and force-constrained dressing controllers condition on sequences of RGB or RGB-D images from wrist or nearby cameras, together with end-effector poses, to predict how candidate motions will influence contact geometry and thereby avoid unsafe configurations [69, 185, 211]. In variable-impedance manipulation with image-conditioned action spaces, multiple RGB views of the workspace are combined with end-effector pose and velocity, so that the controller can adapt stiffness and damping not only to measured forces but also to visually perceived contact conditions, occlusions and environmental changes [35, 215, 217]. 

30 

A prominent trend is to fuse visual information with haptic and proprioceptive sensing in a joint representation that directly feeds safety-aware policies. Visual–haptic variable impedance controllers combine latent visual features extracted from RGB images with force/torque or tactile readings and robot state, enabling the policy to reason simultaneously about global geometry and local contact quality when selecting compliant actions [212, 230]. Dressing and bathing systems integrate segmented point clouds or image-based features with end-effector force histories and candidate motions, using learned dynamics or prediction models to filter out actions whose predicted contact forces exceed task-dependent thresholds [69, 121, 211]. In furniture assembly and other complex contact-rich tasks, multimodal context sequences concatenate proprioceptive vectors, RGB observations and high-resolution tactile readings, allowing residual policies or skill-transfer mechanisms to refine motion precisely at the moment of contact while keeping interaction forces within safe ranges [196, 268, 269]. Recurrent or belief-state architectures extend this idea by maintaining a latent estimate of the scene and contact state under partial observability, with both vision and force/torque streams contributing to belief updates and safety-aware action selection [35, 226]. 

Finally, several frameworks place visual perception within larger safety-aware learning stacks that combine high-level reasoning with low-level control. Safety-aware unsupervised skill discovery and recovery-based RL methods treat vision as part of the state used to infer which regions of the environment are safe to explore, and to learn recovery zones or backup skills that can be invoked when the system approaches unsafe visual configurations [60, 118, 226]. Vision–language–action models extend this further by taking images alongside natural-language instructions and past interaction histories, and by incorporating safety feedback into the training objective so that the resulting policies can interpret human intent while avoiding visually grounded unsafe behaviours [24]. Overall, these works highlight that visual inputs, whether global or hand-centric and whether raw pixels or structured geometry, play a central role in making safety-relevant aspects of the environment explicit to the policy, so that contact-rich behaviour can be regulated proactively rather than reactively. 

**Language instructions** provide an increasingly important high-level interface through which humans specify tasks, constraints, and preferences, while lower-level controllers remain responsible for enforcing physical safety during execution. Rather than hard-coding task objectives into cost functions or reward formulations, these approaches allow users to describe what the robot should do, and often how cautiously it should behave, using natural language [270]. Such instructions are subsequently grounded into symbolic plans, motion goals, or policy parameters [24, 71, 271]. From a safety perspective, language complements geometric and haptic observations by explicitly communicating human intent and safety requirements at the policy interface. 

One line of work couples language with visual and proprioceptive observations in large vision–language–action architectures. In such systems, camera images and robot state are processed jointly with a natural-language instruction to produce either lowlevel actions or intermediate code that can be executed by downstream controllers [24, 271]. Safety is then imposed at two levels: the model is aligned to avoid generating obviously harmful plans, and the generated code or action sequences are checked against constraint sets or safety filters before deployment [24, 271]. Compared to purely 

31 

numeric task encodings, this design allows the same sensorimotor stack to be reused across tasks, while safety-relevant differences are captured in the language input rather than in separate controllers. 

Another set of approaches emphasizes preference-driven interaction. Here, users do not only issue initial instructions, but also provide follow-up signals indicating whether a behaviour is safe, comfortable, or acceptable, and these signals are incorporated into the learning objective or alignment procedure [24, 241]. Text-conditioned models, for instance, may take as input a description of the desired interaction style together with histories of states, actions and safety feedback, and are trained to predict actions that satisfy both task and safety preferences [24, 71]. Human-centered safe RL frameworks complement this by treating human feedback as an additional observation channel that shapes the policy toward behaviours that humans deem safe, even when those behaviours are not easily captured by simple numerical constraints [241]. 

Across these works, language does not replace low-level safety mechanisms such as force limits, control barrier functions or conservative exploration. Rather, it provides a flexible interface for specifying and updating what safe means in a given context [24]. High-level instructions determine which regions of the state and action spaces are desirable or forbidden, while the underlying visuomotor and force-aware controllers ensure that, once a plan is chosen, contact forces, distances and stability constraints remain within acceptable bounds [24, 71, 241, 271]. As language models and alignment techniques improve, this combination of linguistic intent with structured safety inputs offers a promising route to robots that can be both responsive to human guidance and reliably safe in contact-rich environments. 

**Tactile sensing** provides direct measurements of contact states, including contact location, normal and shear forces, and incipient slip, making it a key sensing modality for the safe execution of contact-rich manipulation. Among the various tactile sensing technologies, vision-based tactile sensors, such as the GelSight family [272, 273], have become particularly popular in robot learning due to their ability to capture rich contact geometry and force-related information. In parallel, low-cost and scalable tactile sensing technologies, including flexible tactile sensor arrays [274], have enabled dense tactile perception for contact-rich manipulation. By providing localized measurements of contact conditions that are unavailable from vision or proprioception alone, tactile sensing enables robots to detect slip, estimate contact quality, and regulate manipulation forces for safer physical interaction. There has also been progress in vision-based tactile sensors with task-adaptive geometries, such as hemispherical and finger-shaped designs [275–277]. High-resolution vision-based tactile sensing provides high-resolution, local information about contact that complements global vision and low-dimensional F/T measurements. Rather than only measuring a single wrench at the wrist, tactile skins and fingertip arrays reveal pressure distributions, shear and incipient slip at the exact points of interaction, making it possible to detect unsafe contact patterns, such as concentrated loads on corners or sliding on fragile surfaces, before they escalate into damage or failure [196, 212, 253]. Beyond conventional parallel-jaw grippers and tactile-equipped dexterous hands [278–280], other end-effectors—such as multi-DoF (e.g.,5-DoF) grippers—can enable manipulation primitives like cable/rope disentangling and thin-card flipping [281]. These designs broaden the repertoire of 

32 

feasible manipulation tasks and could be promising to combine with safety modules or learned control policies in future work. For safe learning, these rich contact cues are typically fed directly into the policy alongside proprioceptive state, so that both exploration and execution can be guided away from behaviours that produce sharp spikes or unstable contact transitions [253, 282]. 

One group of methods uses tactile arrays as the main channel for encoding task success and safe contact configurations. [283] uses a large-scale visuo-tactile dataset consisting of over 2.6 million vision–touch pairs, collected across multiple environments and covering 43 manipulation tasks. The dataset is used to pretrain a visuo-tactile representation (encoder) as an upstream step, which can later serve as a foundation for downstream work such as safe contact-rich interaction or manipulation. In furniture assembly, for example, tactile ensembles distributed across fingers or grippers are used to characterise how surfaces, edges and fasteners behaviors during successful insertions or alignments. Policies are then trained to reproduce these tactile signatures while avoiding contact patterns associated with jamming or over-tightening [196]. Gentle manipulation frameworks similarly treat touch as the primary feedback for regulating interaction intensity. Policies observe proprioception and tactile events, and are rewarded for acquiring task-relevant information while keeping per-taxel pressures and impact magnitudes low, which naturally steers exploration toward soft, sliding contacts rather than hard impacts [282]. In both cases, safety is not an external constraint but an emergent property of how tactile patterns are encoded in the observation and reward. 

Tactile sensing plays a key role in variable-impedance control for contact-rich motion along surfaces. In aerial or lightweight manipulators that slide along uneven terrain or structural elements, the policy often receives only proprioceptive state and tactile readings, without full base F/T sensing [253]. The tactile stream reveals contact loss, stick–slip, and localized high-pressure/unsafe contact, while proprioception captures global motion; impedance can then be updated online—stiffening when contact is well supported and softening/backing off when tactile cues indicate high pressure or impending slip [253]. Beyond aerial sliding, tactile/visuo-tactile interaction controllers explicitly use curvature/alignment monitoring to adapt stiffness and force regulation when exploring unknown 3D curved surfaces, including contact-loss recovery and passivity-aware safety mechanisms [284, 285]. For continuous surface tasks (e.g., cleaning/inspection), closed-loop tactile coverage methods encode the target on point clouds and use task-space impedance with force regulation to maintain contact while covering curved surfaces [286]. 

A further set of approaches embeds tactile input within multimodal visual haptic proprioceptive representations [287]. Hierarchical variable-impedance controllers, for instance, build high-level policies on visual features that capture object pose and scene layout, while lower-level modules refine actions using haptic channels that may include both force/torque and tactile measurements [212]. In such designs, vision plans where and when contact should occur, while tactile feedback confirms whether contact is distributed and stable in the way the planner expects. More recent multimodal RL systems explicitly combine visual observations, tactile signals and joint state into a shared latent space, and train adaptive policies that allocate different roles to each 

33 

modality. Vision is used to anticipate geometric constraints, tactile cues to detect unsafe local pressure or slip, and proprioception to enforce kinodynamic limits [230]. By tying safety-related decisions to tactile cues rather than to coarse force thresholds alone, these methods achieve more nuanced and robust protection for delicate objects, complex assemblies and human collaborators. 

# **Takeaway: Safety Roles of Different Modalities** 

No single modality dominates; the right choice follows the binding safety quantity. **Force/torque sensing** is the primary substrate for bounding interaction forces and is hard to replace for force-limited tasks. 

**Vision** contributes global, anticipatory context (approach, collision avoidance, scene geometry) but cannot by itself bound contact forces. **Tactile sensing** supplies local pre-failure cues (incipient slip, pressure concentration) valuable for fragile contacts. **Multimodal fusion** helps most under occlusion or inaccurate models. 

The recurring effective pattern is therefore to use vision and language for _where_ and _whether_ to make contact, and force/tactile sensing with a compliant action abstraction for _how hard_ . 

### **Data Acquisition** 

Data acquisition plays a foundational role in safe learning for contact-rich manipulation. The quality, diversity, and safety-relevance of the data directly influence the performance and generalizability of learned policies, especially in scenarios involving unpredictable contacts or constrained physical interaction. In this section, we discuss three key paradigms in data acquisition: (i) simulation-based data generation, (ii) real-world data collection, and (iii) hybrid and self-supervised data acquisition. 

Data matters for policy learning, especially for a safe policy where negative samples play a significant role in training the agent to be aware of what unsafe scenarios are. However, acquiring such data is time-consuming and labor-intensive. Crucially, unlike the vast text and image corpora scraped from the Internet to train LLMs and VLAs, physical interaction data, specifically high-fidelity contact forces, torques, and safety-critical failure modes, cannot be obtained from the web. This scarcity of contact data in foundation models creates a significant gap in their ability to reason about physical dynamics and safety. Consequently, physical data collection remains inevitable and irreplaceable for contact-rich tasks, despite efforts to leverage simulation and internet-scale proxies. As shown in the data pyramid in Fig. 6, real-world contact data sits at the apex and is both scarce and essential. And in Fig.6 we retain only the most representative concepts in each layer to highlight the progression rather than exhaustively listing all sources. Within each layer, the listed keywords are ordered by increasing contact fidelity and safety relevance: for real-world data, from generic task execution logs to explicit safety and failure cases; for simulation, from generic randomized environments to simulation elements that most directly support sim-toreal transfer; and for internet and shared datasets, from general web-scale corpora to task-specific real-robot benchmarks. 

34 


**Figure 6** Data pyramid for safe policy learning in contact-rich manipulation. The pyramid is organized into three layers according to physical fidelity and safety relevance. (1) Real-world data: includes task execution logs, high-frequency proprioception (joint states, velocities, tactile and force–torque sensing ), contact-rich interaction episodes, and safe and unsafe or failure cases, which provide the most direct evidence about real physical contacts and safety-critical events. (2) Simulation: includes domain randomization (dynamics, appearance, noise), ground-truth physical quantities (forces, poses, contacts), physics engines (MuJoCo, PyBullet, Isaac Lab), procedural scene and task generation, and residual or learned dynamics models with sim-to-real adaptation, enabling large-scale exploration of contact scenarios under controllable yet imperfect dynamics. (3) Internet and shared datasets: includes web-scale language corpora (LLM data), generic vision datasets (web images and videos), large-scale robot logs with weak contact labels, manipulation datasets with limited contact or safety labels, and task-specific real-robot benchmarks with small scale, which are abundant but only indirectly capture contact-rich and safety-critical phenomena. 

**Simulation-based data generation** provides a safe, scalable, and cost-effective means of collecting large volumes of training data for contact-rich manipulation without risking damage to robots, tools, or workpieces. Physics engines such as MuJoCo [288], MuJoCo Playground [289], PyBullet [290], Isaac Gym [291], and Isaac Lab [292] enable learning agents to interact with objects under diverse contact conditions while providing ground-truth access to quantities such as contact forces, velocities, object poses, and other latent states that are difficult or expensive to measure on physical platforms. These simulators further support massively parallel rollouts, substantially accelerating the training of data-intensive methods, including deep reinforcement learning and imitation learning, for contact-rich robotic manipulation. 

To improve generalization and robustness, domain randomization and procedural scene generation are widely used to expose policies to variations in geometry, mass, friction, sensor noise, and task parameters, which is crucial for sim-to-real transfer in assembly, insertion, and other tight-tolerance tasks [228, 264, 293]. Recent work further combines high-fidelity rendering and physics to generate multimodal datasets 

35 

(vision, force/torque, tactile) that can be used to train VLM/VLA-style models and other foundation models for contact-rich robotics. 

However, simulations still suffer from a pronounced reality gap, particularly for phenomena such as material deformation, frictional sticking and sliding, smallclearance contacts, and compliant or flexible components, which can lead to significant discrepancies in policy behavior when transferred to real hardware. To mitigate this, recent approaches incorporate learned residual models, online adaptation, or humanin-the-loop corrections on top of simulation-trained policies, for example by learning residual compliance parameters or gated residual policies that refine the base controller in the real world [294, 295]. Together, these trends point toward hybrid pipelines in which accurate simulation, structured domain randomization, and residual or adaptive components jointly address the sim-to-real challenges of safe contact-rich manipulation. 

**Real-world data collection** remains indispensable for safe learning because it captures the complexities and uncertainties of physical interactions that cannot yet be faithfully reproduced in simulation. By deploying robots in controlled laboratory environments or real-world settings, researchers can collect data on contact forces, object dynamics, sensor measurements, and task performance under realistic operating conditions. Such data expose learning algorithms to unmodeled dynamics, sensing noise, hardware imperfections, and unexpected contact events, thereby improving the robustness and reliability of policies intended for deployment in safety-critical contactrich tasks. 

However, collecting high-quality data in the real world is often time-consuming, expensive, and potentially unsafe, especially in contact-rich tasks where excessive forces or unexpected contacts can damage hardware or pose safety risks to humans. To address these challenges, researchers often employ techniques such as teleoperation, where human operators guide the robot through tasks while collecting data on safe and unsafe interactions [296, 297]. Additionally, safety constraints can be integrated into the data collection process, ensuring that the robot operates within predefined limits to avoid damaging itself or its environment [121, 298]. Furthermore, real-world data can be augmented with simulation data through techniques like domain adaptation or transfer learning, allowing policies trained in simulation to be fine-tuned on real-world data [79, 299]. 

**Hybrid and self-supervised data acquisition** combines simulation, real-world experience, and autonomous data generation to improve the scalability and robustness of safe learning. Hybrid strategies leverage the complementary strengths of simulation and physical interaction by pre-training policies in simulation and subsequently adapting them using real-world data, or by augmenting limited physical datasets with simulated experience [299]. Such approaches enable efficient exploration of diverse contact scenarios while retaining the ability to adapt to the complexities of real-world interactions. Complementarily, self-supervised learning exploits the robot’s own experience to generate additional supervisory signals without requiring extensive manual annotation [79]. For example, robots may learn to predict future states, contact forces, or interaction outcomes directly from multimodal sensory observations, thereby acquiring representations that improve policy robustness and exploration. Together, hybrid 

36 

and self-supervised data acquisition strategies help bridge the sim-to-real gap, expand the diversity of contact-rich training data, and improve the generalization and safety of learned manipulation policies. 

# **Takeaway: Trade-offs in Data Acquisition** 

Simulation provides a scalable and safe means of data collection, but the sim-to-real gap is particularly pronounced for safety-critical contact tasks, including friction, small-clearance interactions, and deformation. Real-world data capture these effects more faithfully but are costly and potentially risky to collect, particularly for safety-critical failures and near-miss events. 

A practical strategy is therefore to combine large-scale simulation and domain randomization for broad coverage with monitored real-world fine-tuning or adaptation, leveraging the complementary strengths of both data sources. 

### **Simulation Environment and Benchmarks** 

Simulation plays a critical role in the development and evaluation of safe learning algorithms for contact-rich robotic tasks. These tasks often involve complex dynamics, high-dimensional state spaces, and the potential for hardware damage, making direct deployment on real robots risky and costly during early stages of learning. Simulated environments provide a safe, controllable, and repeatable platform to test algorithms, enabling rapid iteration and the generation of large-scale data without physical wear [314]. 

Moreover, standardized benchmarks enable consistent comparison across different approaches, thereby fostering reproducibility and progress in the field. By utilizing well-defined simulation platforms and task suites, researchers can more effectively assess safety, generalization, and performance under varied conditions before transitioning to real-world applications. 

**Simulation environments** can be grouped into a richer taxonomy reflecting the underlying physics engine, parallelism, sensing realism, and intended evaluation protocols, as detailed in Table 5. We highlight the perspective of contact-rich tasks in this survey, while readers can find more comprehensive comparisons in [299]. 

**General robotics simulators (ROS-ready)** emphasize sensor realism (e.g., RGB-D and LiDAR), ROS integration, and extensible plugins for actuation and perception. Representative platforms include Gazebo [208, 253, 268, 315–317], Webots [245], CoppeliaSim [318], and Drake [225], making them well-suited for closed-loop, system-level validation, including the evaluation of safety monitors. 

**Rigid-body dynamics engines** are primarily designed for accurate simulation of contact dynamics and articulated systems. **_CPU-based engines_** such as DART (via robot ~~d~~ art) [319] emphasize accurate contact modeling, joint limits, and articulated constraints. PyBullet [61, 293, 320–323] remains one of the most widely used opensource engines owing to its strong community support. MuJoCo, which is one of the most popular simulators for contact-rich tasks for its inherent contact modeling and fast simulation speed. It powers standard benchmarks such as RoboSuite [307] and Safe-Control-Gym [46], and is extensively used in contact-rich manipulation tasks 

37 

including insertion [135, 204, 206], assembly [109, 133], and surface interaction [138, 184]. Furthermore, it supports research in safe exploration and control [47, 55, 60, 266], as well as data collection and skill learning [255, 264, 265, 298, 324]. It is also widely adopted in non-prehensile and articulated object manipulation [226–228, 231], dynamic and locomotion tasks [35, 325], and complex media interaction [191, 282]. Additional applications span diverse contact-rich scenarios [326–340]. 

**_GPU engines_** leverage massive parallelism to accelerate data collection for RL. The Isaac ecosystem is widely adopted, including Isaac Gym and Isaac Sim, along with their modular frameworks like Factory [303], Orbit [302], Isaac Lab [292], and RoboVerse [77]. These platforms support large-scale training for contactrich tasks [118, 195, 341–344]. Recently, MuJoCo MJX [289] has also introduced GPU-accelerated physics to the MuJoCo ecosystem. 

**Domain-specific environments** support safety-critical perception and planning. Assistive Gym [320] focuses on assistive robotics scenarios, while Box2D [345] remains useful for rapid prototyping of 2D contact and control tasks. 

**Interfaces and experiment factories** standardize and streamline the development of contact-rich robotic applications. OpenAI Gym-style wrappers [322, 346] provide unified observation and action APIs across simulation engines and tasks, whereas SAI 2.0 [347] and related software stacks offer perception–control scaffolding for contact-rich manipulation. 

**Benchmarks** are essential for quantifying progress in safety, generalization, and contact robustness. We categorize them into general manipulation suites, contactintensive benchmarks, and safety-specific environments, as detailed in Table 6. 

**General manipulation suites** provide standardized platforms for evaluating manipulation algorithms across a diverse range of tasks. RoboSuite [307] standardizes robot models and canonical tasks (e.g., insertion and door opening), serving as a primary testbed for modular algorithm design. Meta-World [311] and RLBench [313] offer broad multi-task evaluation, although they often rely on simplified contact physics. Recently, RoboVerse [77] and RoboCasa [306] have scaled these to large-scale, scene-level manipulation tasks using foundation models. 

**Contact-intensive and generalizable benchmarks** address the reality gap in contact physics by providing more realistic contact-rich manipulation scenarios. ManiSkill [308] and ManiSkill2 [309] feature diverse articulated objects and highfidelity physics for learning generalizable policies, including contact-rich tasks such as charger insertion and peg insertion. Factory [303] provides physically accurate assembly tasks, such as nut-and-bolt threading, specifically designed for evaluating contact-rich policies in Isaac Gym. 

**Safety-oriented benchmarks** focus explicitly on evaluating safety-aware learning and control algorithms. Safe-Control-Gym [46] and its successor, Safety Gymnasium [48, 348], are the de facto standards for safe reinforcement learning, defining constrained navigation and manipulation tasks with hazard maps and cost signals. Beyond penalty-based safety, Safe-Control-Gym [46] integrates control-theoretic constraints, including symbolic priors and partial observability, for evaluating methods with formal safety guarantees. Robust Gymnasium [78] further targets safety under distributional shifts and adversarial disturbances, which are critical for robust sim-to-real transfer. 

38 

# **Takeaway: Choosing Simulation and Benchmark Platforms** 

Engine choice is governed by a contact-fidelity-versus-parallelism trade-off: MuJoCo-family engines are favored for contact-rich fidelity, whereas GPU engines (the Isaac ecosystem) are favored for large-scale parallel data collection. More importantly for this survey, safety-specific suites (Safety Gymnasium, Safe-ControlGym, Robust Gymnasium) remain few and largely abstract: they under-represent deformables, multi-stage and tool-supported tasks, and critically standardized contact-force evaluation, the very gap our Reporting recommendations are intended to mitigate. 

### **Safety Evaluation Metrics** 

Safe learning works differ from traditional learning works in their primary goals. Traditionally, the learned models are evaluated for their predictive performance or their task completion success. Some works also focus on the efficiency of the learning system and generalization to novel situations. Although the safe learning works are still concerned with these metrics, they add new ones related to safety, such as a statistic of constraint violations or a cost value. In the case of contact-rich problems, the safety metrics are usually related to the contact forces. 


**Figure 7** The metrics in the contact-rich safe learning literature can be categorized according to their objectives: Safety, task and efficiency. There are trade-offs between these objectives. The researchers aim to develop safe systems with a good trade-off for task success and efficiency. Some metrics, such as force, velocity and energy serve to measure multiple objectives. 

In the following, we present and categorize the evaluation metrics used by the relevant works scanned in our survey. We present the prominent metrics as categorized according to their goals in Fig. 7. The identified metrics aim to measure the safety, task (success) and efficiency objectives. 

**Safety, efficiency, and task objectives** are the primary criteria used to evaluate safe learning methods for contact-rich manipulation. Safety is usually assessed through violations of predefined constraints [243, 258] or the value of a cost function [266, 

39 

349]. In physical interaction tasks, it is often quantified using physical metrics such as contact force, acceleration, and velocity [188, 221]. Control stability and human safety constitute two important subcategories of the safety objective. Stability can be evaluated through convergence rates [57, 148] or the energy flow of the system [81, 223, 256]. Human safety includes primarily the _physical safety_ of the human in direct contact tasks like massaging or bathing assistance [121, 235], however, _perceived safety_ concepts such as trust, predictability and comfort gain importance for the acceptance of robots in social spaces [64]. A relevant work [69] evaluates the perceived safety through a 7-point Likert survey in their dressing assistance experiments. 

The safety objective is the main topic of this survey, however, it cannot be considered in isolation from the other criteria. The task objective is quantified by the frequency of achieving success [226] or the value of a task cost function (i.e., reward) [245]. In some works, the quality of a solution is assessed by the progress of task completion ([69]: dressing rate, [57]: vegetable slicing progress), size of the explored space [246], amount of produced output ([211]: ground fine powder), or the tracking accuracy [121]. [197] defines an instability index to quantify the episode reward deviation between runs. On the other hand, the efficiency objective is assessed by the energy consumption [230], and time requirements of the data collection (e.g., teaching) [269], learning a model [109], task execution [245, 262], or computation of an action or a plan [226, 260]. Since robot hardware is costly, reducing real-world trials by learning in simulation is preferable [247]. 

**Trade-offs between safety, efficiency, and task objectives** are inherent to contact-rich robot learning because these objectives often conflict (Fig. 7). Safety evaluation should therefore not rely on a single metric in isolation. For example, a method that achieves a high task success rate by repeatedly exceeding contact-force limits cannot be considered truly safe, whereas a method that rarely violates safety constraints but rarely completes the task may be impractical for real-world deployment. Having both task and safety objectives increases the optimization complexity, and consequently the amount of data to learn effective policies [349]. Thus, in contact-rich tasks, it is expected that a safe method may achieve a lower raw success rate or longer training times than an unconstrained or unsafe baseline. What matters is whether the loss is justified by a clear reduction in unsafe contacts, excessive forces, instability, or hardware risk. 

The trade-off can be measured by a combined metric, such as the ratio of the safe and successful experiments to constraint violating ones [60, 79]. A safety-efficiency reward function was proposed by [267] to achieve a good trade-off. On the other hand, [258], [231] and [243] compare the numbers of successful and violating runs side-byside instead of directly calculating a ratio between them. Side-by-side comparison can capture more nuanced conclusions and is thus recommended when reporting the final results. However, when evaluating many runs, such as in parameter optimization and ablation studies, it is more practical to use a combined metric for direct comparison. 

Care should be taken when reporting combined trade-off metrics. If task success, safety, and efficiency are collapsed into a single reward or cost value, it becomes difficult to determine whether a lower score is caused by poor task execution, conservative 

40 

safety behavior, excessive contact forces, or inefficient motion. We therefore recommend building trade-off analyses on simple and directly interpretable quantities, such as the number of successful episodes, the number of violating episodes, and the number of safe successful episodes. 

Machine learning metrics such as prediction accuracy have been used to measure task objectives, however, they are also relevant in works that use learned models for safety-related predictions [57, 247]. Just as the learning curves provide insights on the success and efficiency trade-off, some works present the learning curves of success, violation and their ratio to portray the trade-off between the three objectives during training [60, 79]. We further recommend reporting variability across random seeds and training runs, especially for reinforcement learning methods, where inter-seed variation and hyperparameter sensitivity can be large. Reporting only the best run or a single seed can obscure unsafe failure modes and overstate robustness. 

Although shifting the focus to safety can decrease the task performance or learning efficiency, these objectives can be aligned in the case of physically interpretable metrics such as force and motion tracking errors, and energy consumption. Physically meaningful results such as the force-velocity behavior can provide intuition towards the safety of the system [219, 246]. Tracking the target force without large deviations in the Lyapunov-based boundaries directly translates to both the control stability and task achievement quality [148]. On the other hand, learning energy-based stability from data directly translates to energy efficiency in deployment [81]. 

**Improved safety evaluation** can be achieved by assessing system robustness under noise and disturbances. The safety of a learning system can be further evaluated by introducing external disturbances or uncertainty during testing. For example, [121] evaluates the convergence of a trajectory-tracking controller under external disturbances. Noise can be injected into the observation space [195, 226, 298] or the action space [197], while vision-based systems can be challenged using varying backgrounds or cluttered scenes [350]. These evaluations help reveal the limitations of learning systems and characterize their sensing and robustness requirements. [207] evaluate their system under uniformly sampled simulation parameters, in addition to localization uncertainties. [234] compares the safety and success of different approaches in nonstationary environments. These and similar evaluation efforts allow demonstrating the robustness and generalization capacity of a method. 

Apart from the added conditions, the evaluation can be strengthened by presenting metrics at different levels of detail. In Fig. 8, we define 3 levels of analyses to establish a common understanding and encourage more insightful results: 1. _global_ (high-level) analyses present aggregated summary statistics such as the maximum force, total number of violations, or mean ( _±_ variance) tracking error over many episodes. 2. _variational_ (mid-level) analyses show the trends of metrics among many episodes or seeds, such as a learning curve, a histogram of execution times, or a scatter plot of success ratio versus force violation. 3. _exemplar_ (low-level) analyses present descriptive case studies, often real-time measurements from a single episode, such as motion trajectories, force measurements, or even multimedia material. Going downwards, the amount of detail and depth of analysis increase; going upwards, the results get more general 

41 


**Figure 8** Three levels of result analyses: Global (high-level), variational (mid-level), and exemplar (low-level). 

and memorable. _Variational_ comparisons allow a more in-depth analysis of the system behavior from temporal, spatial or multi-variate perspectives. _Exemplar_ results can give valuable insights on why and how the method works, or when it fails, without deriving general conclusions. We recommend providing analyses at all levels for a more comprehensive communication of the results. 

**Reporting recommendations** begin with presenting a compact yet interpretable set of evaluation metrics rather than relying on a single reward or cost. At a minimum, evaluations of safe learning for contact-rich tasks should report task success, constraint violations, violation severity, and efficiency, together with variability across random seeds or repeated runs. Violation severity should further be complemented by physically meaningful contact metrics, such as maximum or mean contact force, force-tracking error, or injected energy when applicable. For learning-based methods, the evaluation should also report the parameter-tuning protocol, including the number of seeds and the search range of important hyperparameters. Since hyperparameter choices and tuning seeds can substantially affect final performance and sample efficiency, separating tuning and testing conditions improves the fairness and reproducibility of comparisons [351]. When possible, the same metrics should also be reported under controlled perturbations or distribution shifts. This reflects the practical reality of contact-rich deployment, where pose, sensing, friction, stiffness, geometry, and human motion can vary across trials. In this way, safety evaluation can communicate not only whether a method works, but also how it trades off success, safety, efficiency, robustness, and tuning effort. 

42 

### **Safety Abstraction Level** 

In contact-rich robotic tasks, safety can be embedded at various abstraction levels in the system hierarchy, ranging from high-level task planning to low-level control, and even spanning across end-to-end learning architectures. Each level presents different trade-offs between interpretability, reactivity, and generalizability. This section categorizes learning-based safety approaches by the level of abstraction at which they operate and discusses their respective advantages, challenges, and applications. This abstraction-level view is orthogonal to the _enforcement-space_ view : the present section asks _at which layer_ of the hierarchy a safety mechanism is introduced (planning, control, or end-to-end), whereas _enforcement-space_ asks _in which coordinate space_ the resulting constraints are expressed and enforced (task, joint, or policy space). A given method occupies one position on each axis. 

**High-level planning** typically encodes safety through symbolic reasoning, task graphs, or decision-making policies that govern long-horizon robot behavior. Learningbased approaches at this level often involve hierarchical reinforcement learning (HRL) [352, 353], safe policy search with task constraints [244, 319], or logic-based planning augmented by learned models [354, 355]. In contact-rich settings, these methods aim to avoid unsafe task sequences or infeasible contact configurations by reasoning over constraints such as force thresholds, joint limits, or task success probabilities [356, 357]. 

For example, shielded planning mechanisms and arbitration graphs can learn to prune unsafe high-level actions using safety classifiers or predictive models [108, 358, 359]. While such methods provide good interpretability and modularity, they depend heavily on accurate abstractions and may suffer from limited reactivity to unforeseen contact dynamics during execution. Temporal logic specifications have also been integrated into diffusion-based planning to satisfy temporally-extended symbolic constraints [360]. 

Recently, the emergence of LLMs and VLMs has enabled advanced high-level planning capabilities for robotic systems, including in contact-rich tasks. These models can interpret complex task instructions, reason about safety constraints from natural language or visual cues, and generate high-level action sequences or code that proactively avoid unsafe situations [4, 271, 361, 362]. For example, VLM-enhanced planners can leverage multimodal perception to identify hazardous regions or delicate objects in the environment, integrating this information into symbolic task planning or policy generation [24, 71, 363, 364]. This allows robots to adapt their strategies dynamically, ensuring that safety considerations are embedded from the outset of task execution. 

**Low-level control** ensures safe interactions at the actuation and feedback levels by enforcing physical constraints in real time. These constraints include limits on force, torque, impedance, and stability, which are particularly critical in contact-rich scenarios. Learning-based methods here typically involve adaptive impedance control, learning CBFs, model-predictive safety filters, or robust policy adaptation techniques [209]. 

Compliant control and impedance learning constitute one of the most widely adopted strategies for achieving safe low-level control in contact-rich manipulation. Instead of learning direct torque commands, these methods learn variable impedance or admittance parameters [119, 126, 249, 267]. By modulating stiffness and damping 

43 

online according to contact feedback, they ensure compliant behavior that naturally limits interaction forces and absorbs impacts [246, 254, 255]. Recent approaches further integrate passivity constraints or energy tanks into the learning process to guarantee coupled stability during dynamic contact [81, 144]. 

Safety filters and barrier-based methods provide hard safety guarantees by wrapping a learned policy with a protective control layer. To enforce constraints such as joint limits, friction cones, and maximum contact forces, control barrier functions (CBFs) and related safety filters monitor the control input and minimally modify it to keep the system within a forward-invariant safe set [47, 53]. Model Predictive Safety Filters (MPSFs) extend this idea by reasoning over a finite prediction horizon to prevent inevitable future violations, which is particularly important for systems with inertia or actuation limits [57, 108]. 

Robust and adaptive safety addresses uncertainties arising from imperfect models and changing task conditions. For scenarios involving unknown friction, payload variations, or other modeling uncertainties, robust control techniques such as sliding mode control (SMC) and adaptive control are combined with learning to preserve safety margins [121, 226, 257]. These low-level controllers compensate for disturbances and unmodeled dynamics that might otherwise destabilize a high-level learned policy. 

**End-to-end safety enhancement** seeks to integrate perception, decisionmaking, and actuation within a unified model while embedding safety either implicitly (e.g., through regularization) or explicitly (e.g., via constrained optimization or safety critics). This includes safe reinforcement learning frameworks that learn both task policies and safety constraints simultaneously from raw sensory data [54, 109, 325]. For instance, [35] proposed a neural network-based approach that learns to predict safe actions directly from raw sensory inputs, such as images and proprioceptive data, allowing the robot to adapt its behavior in real-time to avoid unsafe actions during contact-rich tasks. 

Recently, VLA models have emerged as a powerful paradigm for end-to-end safety enhancement. These models bridge perception, reasoning, and control by learning from large-scale multimodal datasets that include language instructions, visual observations, and robot actions [4, 24, 27]. Safety is enhanced in VLA systems through several mechanisms: (i) Safety-aware prompting and grounding: VLA models can be conditioned on safety-specific prompts or rules (e.g., “move slowly near the glass”) to generate compliant behaviors [71, 271]. (ii) Safety critics and filtering: Auxiliary safety modules or critics can be trained to evaluate the risk of generated actions before execution, filtering out potentially hazardous commands [76, 362, 364]. (iii) Multimodal alignment: By aligning visual and linguistic representations with physical safety constraints (e.g., force limits), VLA models can better generalize safety concepts to novel objects and environments [360, 361, 363]. While these methods promise scalability and generalization, especially in contact-uncertain environments, they often suffer from limited interpretability and pose challenges in formal safety verification compared to modular architectures. 

To make this concrete, Fig. 9 instantiates the prevailing plan–parameterize–enforce (PPE) architecture of recent safe VLA systems with named modules. In the _plan_ 

44 

stage, a VLM/VLA parses the instruction and scene into a task sketch and a set of explicit, machine-checkable safety rules (e.g., a force cap on a cable, a no-touch label on a painted face, a speed cap near a human), optionally grounding physical reachability as in PhysVLM [72]. In the parameterize stage, mid-level skills expose safety–relevant references, including target pose, force, and impedance or stiffness gains, so the semantic plan is compiled into bounded, compliant skill parameters rather than raw torques [75, 76]. In the _enforce_ stage, a low-level shield (a CBF-QP, a reachability filter, or an MPC safety filter) projects each command onto the admissible set at run time, bounding force, region, and velocity regardless of upstream errors [4]. Two complementary design choices recur: SafeVLA casts safety as a _constrained-learning_ objective, so the policy is trained to respect explicit cost limits rather than relying on prompt compliance alone [24], whereas tactile-augmented models (Tactile-VLA [365], VTLA [366], BiTLA [367], OmniVTLA [368]) add contact/force tokens to the observation so the policy can condition on, and react to, contact onset and incipient slip rather than vision alone. 

This layering matters because semantic and physical safety can diverge. Consider a “wipe the table but do not press the cup” instruction in which the VLM mis-grounds the fragile-object mask and treats the cup as part of the table surface. At the plan level the action remains semantically valid, wiping is permitted, so prompt- and alignmentbased checks pass; the error surfaces only physically, as the end-effector drives its tracking setpoint into the cup and a contact-force spike develops. In a PPE stack the enforce layer intercepts this: a force/region control barrier function detects the barrier value _h_ ( **_x_** ) _→_ 0 at the no-touch boundary and the force limit, minimally modifies the command to arrest penetration before an overload occurs, and logs the event for recalibration. The same failure would go undetected by a language-only safeguard. This illustrates why language-level constraint specification alone is insufficient for physical contact safety, a point we revisit among the VLM/VLA-specific challenges and why a certified low-level shield remains the component that actually bounds interaction forces. 

Crucially, these foundation-model mechanisms are not new safety _principles_ but re-instantiations, at the semantic level, of the classical notions. Language- and ruleto-constraint grounding is the foundation-model counterpart of constraint satisfaction and reachability; safety critics, refusal, and risk-aware filtering of generated actions instantiate risk- and data-driven safety; the low-level shields beneath a VLA planner are exactly the invariance/CBF certificates; conservative default force/velocity caps and compliant references reduce to the force/energy/passivity view; no-touch and humanproximity rules map to human-centered and standard-driven safety; and the grounding of intent itself is the semantic-safety axis. Table 7 summarizes this correspondence. Read this way, the contribution of robotic foundation models to contact-rich safety is to _specify and ground_ constraints from open-ended language and perception, whereas the guarantee that those constraints actually hold during contact still rests on the classical low-level mechanisms surveyed above. The open problem is therefore not to replace those mechanisms but to ensure that the semantic layer feeds them correct, physically meaningful constraints, a requirement that current systems meet only partially. 

45 


**Figure 9** The plan–parameterize–enforce (PPE) architecture used by recent safe VLA systems, instantiated with named modules. The plan stage (e.g., SafeVLA [24]; safe robot foundation models [4]) emits a task sketch and explicit safety rules; the parameterize stage exposes pose/force/impedance references; the enforce stage applies a certified CBF/reachability/MPC shield. Tactile-augmented variants (e.g., Tactile-VLA [365]) feed contact/force signals back to the shield, which is the component that actually bounds interaction forces when upstream semantic grounding is wrong. 

**Hybrid methods** combine safety mechanisms across multiple abstraction levels to leverage the strengths of each. For instance, a high-level planner may filter task options using a safety-aware graph while a low-level controller enforces contact-force constraints through learned CBFs [120]. Alternatively, end-to-end models may be guided by high-level logic rules or shielded by low-level safety filters during deployment. 

Plan–learn–filter pipelines represent one of the most common hybrid architectures for safe contact-rich manipulation. A high-level planner (graph, sampling, optimization, or semantic decomposition) proposes nominal contact strategies or intermediate sub-goals; a learned policy (often variable impedance/admittance or residual) generates parameterized actions (pose, force, or stiffness); and a runtime safety layer (CBF, reachability, MPC shield, or action projection) minimally modifies unsafe commands while preserving task progress [46, 47, 130, 249, 263, 267]. This layered design reduces unsafe transients during approach, impact, and sustained contact by deferring exact constraint satisfaction to an online safety filter. 

Compliant action abstraction and certified projection provide another effective hybrid strategy by learning safe action representations instead of directly predicting joint torques. Rather than outputting raw torques, these methods learn action abstractions such as desired Cartesian displacements, force targets, or diagonal/structured stiffness gains that preserve passivity margins while exposing explicit interfaces for safety modification [79–81, 126, 249, 267]. Certified projection, implemented through quadratic programs with CBF constraints, shield vetoes, or reachability pre-checks, enforces forward invariance or constraint satisfaction without retraining the underlying policy [46–48, 263]. 

Generative or residual policies under safety wrappers combine expressive policy representations with certified runtime safety mechanisms. Diffusion or residual reinforcement learning policies generate candidate motions or compliance updates, while a safety critic or barrier/MPC layer evaluates predicted force envelopes, energy flow, or constraint margins before execution (”generate–score–project”) [35, 47, 79, 81, 211, 

46 

369, 370]. Residual admittance and stiffness adaptation compensate for unmodeled contact geometry, whereas the surrounding safety wrapper prevents excessive contact forces and other unsafe behaviors [126, 249, 267, 324]. 

Semantic or VLM/VLA hybrid safety extends hybrid architectures by integrating vision-language(-action) models into the safety pipeline. Vision-language(-action) and other foundation-model components parse unstructured instructions and scene context into structured constraint representations [4, 24, 27]. These constraints are subsequently passed to the plan–learn–filter stack, where a semantic planner produces task goals or action sequences, a learned variable-impedance or residual policy generates compliant control parameters [76, 364], runtime CBF, reachability, or MPC safety layers enforce physical limits, and a logging module records violations for calibration and continual improvement [46, 47, 249, 267]. Multimodal fusion, particularly of vision, tactile sensing, and force sensing, further disambiguates occlusions and anticipates risky contact transitions, while structured prompting and action schemas reduce hallucination-induced unsafe commands [4, 24, 35]. This hybridization aligns high-level semantic intent with certifiable low-level execution, enabling scalable yet physically grounded safe manipulation in contact-rich settings. 

Such multi-layered architectures can offer robustness and flexibility, especially in unstructured contact-rich tasks. However, hybrid methods also introduce complexity in integration and may require careful coordination to avoid conflicts between safety modules operating at different levels. 

### **Safety Enforcement Spaces** 

In the context of learning for contact-rich manipulation, safety is not only a monolithic concept but also is enforced hierarchically across the robot’s control architecture. Constraints can be imposed at the level of physical interaction (task space), internal actuation (joint space), or within the decision-making abstraction (policy space). Each of these domains provides distinct opportunities and challenges for incorporating safety. Task-space enforcement directly regulates end-effector motion and contact forces with the environment, joint-space methods shape internal robot behavior to avoid unsafe configurations or torques, while policy-level mechanisms ensure that the agent’s decision-making respects safety constraints from the outset. This section categorizes existing literature based on these architectural levels, synthesizing the dominant control strategies and emerging hybrid paradigms. This enforcement-space view is complementary to, not a repetition of, the abstraction-level view: there we asked at which layer safety is added, here we ask in which coordinate space the constraints live. To avoid duplication, the cross-layer _plan–learn–filter_ hybrids are treated once, under _Hybrid methods_ ; the present section instead focuses on how constraints expressed in task, joint, and policy space differ and combine. 

**Task-space safety mechanisms** operate directly at the interface of physical interaction by regulating the kinematics and dynamics of the end-effector. By defining safety in Cartesian coordinates, these methods directly constrain the contact forces and motions exerted on the environment. A predominant strategy for task-space safety is the use of compliance and stiffness modulation. Rather than tracking rigid trajectories, impedance and admittance control schemes allow the robot to deviate from 

47 

reference paths in response to external forces, thereby absorbing impact energy and maintaining stable contact [117, 185, 211, 231, 247]. The works in [246, 262] explicitly bound the forces and torques at the end-effector to prevent excessive contact pressures, integrating such constraints into the controller and learning process. Recent learning-based frameworks have extended this architecture by parameterizing variable impedance policies, where the agent learns to output context-aware stiffness or virtual force targets to ensure gentle interaction [119, 217, 249]. To guarantee stability in these interactions, energy-based approaches often enforce passivity constraints, ensuring that the robot behaves as a passive system and does not inject unbounded energy into the environment [144, 145]. 

Beyond inherent compliance, formal constraints are frequently applied to bound the workspace. CBFs and safety filters are employed to strictly confine end-effector states within a safe set, overriding policy actions that threaten to violate positional or force limits [68, 146, 147]. These safe manifolds can be learned from demonstrations or modeled via Gaussian processes, restricting the planner to regions with high probability of safety [57, 325]. In reinforcement learning settings, task-space safety is often formulated via reward shaping to penalize excessive contact forces [195, 197, 198, 316], or by restricting the action space to a safe subset of the workspace to prevent collisions during exploration[118, 122, 208, 258]. The works in [237, 271] also use planning-based approaches to build safety into motion generation. Before execution or learning, they compute contact-rich trajectories that satisfy contact stability, task unrelated collision avoidance, and joint limits, so that any subsequent policy learning begins with inherently safe trajectories. 

Notably, in human–robot interaction scenarios, the constraints are adapted to dynamic environments, utilizing safety fields to enforce separation distances, and controllers are designed to comply with industry safety standards, e.g. ISO force limits, during physical contact [71, 260, 320]. 

**Joint-space safety mechanisms** prioritize the robot’s intrinsic integrity, whereas task-space methods focus on extrinsic interaction. These methods operate in the configuration space, constraining joint angles, velocities, and torques to prevent self-collisions, singularity proximity, and actuator saturation. 

Safety in this domain is often realized by augmenting low-level controllers with limiting functions. Joint-level CBFs and saturation filters ensure that commanded torques do not exceed hardware capabilities or result in unsafe kinetic energy, thereby indirectly limiting the force transfer to the environment [221]. Stability is further ensured through Lyapunov-based formulations, such as enforcing positive-definiteness in learned joint stiffness matrices to guarantee system passivity [229, 233]. 

To mitigate the risks of dynamic impacts, adaptive joint-torque controllers utilize proprioceptive feedback to dissipate shock through joint compliance [226, 257]. In the context of RL, policies operating in joint space are frequently constrained to prevent erratic high-frequency actuation. Strategies include penalizing proximity to joint limits [371] or employing hierarchical schemes where the RL agent dictates high-level goals while a lower-level motion planner generates smooth, collision-free configuration trajectories [109]. Specific applications, such as robotic massage, have demonstrated that limiting joint-space velocities and applying compliance controls effectively bounds 

48 

the output torque, ensuring safe physical interaction through intrinsic actuation limits [222]. 

**Dual-space safety enforcement** combines task-space and joint-space constraints to eliminate the safety blind spots associated with relying on either representation alone. While task-space control may inadvertently command infeasible joint configurations, joint-space safety mechanisms may overlook excessive contact forces or pressures at the end-effector. Consequently, hybrid architectures have emerged to enforce safety concurrently across both spaces, achieving a balance between safe physical interaction and protection of the robot itself. This dual-space sense of _hybrid_ is distinct from the cross- _level_ hybrids: here it refers to enforcing constraints simultaneously in two _coordinate spaces_ (task and joint), not to combining abstraction levels (planning, control, end-to-end). We therefore keep the plan–learn–filter discussion in _Hybrid methods_ and restrict this subsection to task/joint coordination. 

Hierarchical control frameworks typically employ a task-space loop to manage environmental interaction forces, coupled with an inner joint-space loop to handle redundancy resolution and torque limits. A Cartesian impedance controller regulates contact stiffness, while a secondary joint-space reflex module monitors for collisions or internal limits, overriding commands to dissipate energy if discrepancies arise [41, 138]. Theoretical guarantees for such dual-loop architectures have been established via Lyapunov analysis, proving that errors in both force tracking and joint deviation remain bounded [219, 372]. Additionally, in [373], the constrained manifold is imposed in both joint and Cartesian space to ensure safety. 

Ensuring stability in the joint space can indirectly enforce task-space safety [374]. In [375], a model-based actor–critic method confines the joint controller’s behavior within stability limits using an analytical model of the robot and environment stiffness. As a result, the end-effector also never pushes beyond safe force limits. Similarly, in dynamic locomotion tasks like hopping, strictly respecting joint torque and angle limits is shown to inherently stabilize the task-space center-of-mass trajectory, preventing falls [325]. 

**Policy-space safety enforcement** incorporates safety directly into high-level decision making by embedding safety considerations into the learning objective or planning horizon. Rather than relying solely on real-time control interventions, these methods proactively avoid states or action sequences that would otherwise require low-level emergency corrections. 

A standard formalism for this is the CMDP, where the agent optimizes a reward signal subject to a cost threshold associated with unsafe states [376–379]. Lagrangian relaxation is commonly used to dynamically weight this cost, training the policy to satisfy safety constraints asymptotically [24]. Alternatively, safety can be encoded into the value function itself[62, 380]. Safety critics or feasibility value functions estimate the long-term probability of constraint violation, guiding the policy to select actions that maximize the margin of safety [239]. To handle potential failures, [60] introduces a separate safety policy that intervenes when the agent approaches a high-risk region, steering the system back to a safe state before returning control to the task policy. 

Implementing such boundaries becomes non-trivial when the state space is highdimensional or unstructured. In high-dimensional visual manipulation tasks, safety 

49 

barriers are often learned in latent spaces, allowing the agent to distinguish between safe and unsafe visual manifolds without explicit state estimation [266, 380, 381]. Furthermore, when safety constraints are difficult to formalize mathematically, Human-inthe-Loop paradigms incorporate human oversight to shape the policy’s risk sensitivity, utilizing human feedback and intervention to define safety boundaries during the exploration phase [241]. Beyond defining constraints and boundaries, generative models such as diffusion policies have been employed to synthesize action sequences that prioritize smoothness and low uncertainty, thereby reducing the stochasticity that often leads to unsafe behaviors [238, 382, 383]. 

We summarize how the task-, joint-, dual-, and policy-space enforcement strategies differ along unified criteria in Table 8. 

### **Current Limitations and Research Gaps** 

Despite rapid progress in learning-based methods for contact-rich robotic manipulation, several **key challenges** remain before these approaches can be deployed safely and reliably at scale. This section outlines major open problems, with particular attention to how emerging VLM/VLA-based methods both amplify and help address these issues. 

**Fragile safety and stability guarantees** remain a fundamental challenge for learning-based controllers, including those using deep networks and VLAs, which often lack formal guarantees of passivity, stability, and constraint satisfaction under hard contacts [81, 145, 384]. This limitation can lead to unsafe behaviors and hardware damage. While passivity-centric and energy-constrained formulations offer promising directions, integrating them seamlessly with large, expressive policies remains technically challenging, especially when contact conditions change rapidly or unpredictably. 

**Data scarcity and biased supervision** continue to hinder the development of robust contact-rich manipulation systems. Contact-rich skills require precise force control and tight tolerances, but high-quality demonstrations and interaction data are expensive, brittle, and difficult to scale compared to standard vision–language datasets. VLMs and VLAs promise better generalization through pretraining, yet they are typically supervised by weak or indirect signals that do not capture fine-grained contact events, leading to policies that may look competent visually but fail under subtle force or geometry variations. 

**Limited robustness, generalization, and uncertainty awareness** remain major obstacles to reliable deployment. Learning-based policies for contact-rich manipulation, especially those trained on narrow task distributions, often overfit to specific layouts, materials, or sensing conditions and degrade sharply under distribution shifts. Although VLAs offer broader prior knowledge, current models typically have weak uncertainty estimation, making it difficult to detect when a contact-rich interaction [24, 385] is entering an unsafe regime and requiring fallback to safer behaviors or human intervention. 

**Safe exploration under physical risk** remains the most safety-critical phase, as naive probing can cause jamming, surface damage, or tool wear in insertion, 

50 

polishing, and assembly contexts [46, 79]. Existing constrained and risk-sensitive reinforcement learning frameworks provide expectation- or probabilistic-based safety guarantees, yet remain vulnerable under distribution shifts. Shielding and actionprojection mechanisms, including control barrier functions, reachability analysis, and model predictive safety filters, provide hard online guarantees but typically rely on conservative uncertainty sets, thereby limiting exploration efficiency and data utilization. 

**Safe execution and performance trade-offs** remain an equally important challenge after policy learning. Ensuring sustained constraint satisfaction during deployment requires balancing responsiveness, task efficiency, and physical safety margins. Variable impedance or admittance policies learned from demonstrations or reinforcement signals can adapt compliance online [79, 249, 267]; however, their stability margins under rapid parameter adaptation are rarely quantified. Moreover, runtime safety filters may degrade task performance through overly conservative interventions, whereas softer filtering strategies risk cumulative force or constraint violations. Existing methods therefore lack a principled framework for jointly optimizing (i) safety violation probability, (ii) force and energy envelopes, and (iii) task efficiency. 

**Benchmark and dataset limitations** continue to hinder the systematic evaluation of safe learning methods for contact-rich manipulation. Existing simulation suites and benchmarks provide limited coverage of deformable objects, multi-stage processes, tool-supported tasks, and tasks performed in close collaboration with humans [77, 78, 89]. Public datasets rarely include (i) high-frequency wrench traces aligned with failure annotations; (ii) rich near-miss episodes essential for learning recovery policies; or (iii) semantic safety labels, such as forbidden regions and fragile surfaces. This scarcity impedes reproducible comparisons of safety violations, recovery latency, and generalization. Although emerging safety-oriented RL frameworks and robust benchmarks partially address constrained exploration, they still lack standardized protocols for evaluating contact-force safety [48, 90]. Until standardized safe-contact benchmarks mature, future evaluations can follow the reporting recommendations, which emphasize interpretable task, safety, efficiency, variability, and robustness metrics. 

**Safety risks specific to VLMs and VLAs** arise from the introduction of generalist, language-conditioned policies into contact-rich manipulation. Such models may misinterpret language instructions, hallucinate feasible contact strategies, or overconfidently execute plans that violate implicit safety constraints. Recent work on safety-aligned VLAs and failure detection for generalist policies highlights the difficulty of systematically eliciting unsafe behaviors, constraining them during learning, and verifying that deployment remains within acceptable risk bounds. A specific consequence of conflating semantic and physical safety concerns the interpretation of _evidence_ . Language-level constraint specification, such as prompting “do not exceed 5 N” or “do not touch the painted face,” demonstrably improves semantic or planlevel behavior, but to our knowledge no published study has isolated language-level specification and shown that it alone reduces _measured_ contact-force or impulse violations on real hardware. Reported safety gains are typically evaluated at the planning or refusal level, or they rely on downstream low-level controllers that enforce physical 

51 

constraints regardless of the language input. We therefore caution against interpreting semantic-level safety as evidence of physical contact safety, and identify the controlled evaluation of this relationship, namely, whether language-level constraints reduce real contact-force violations when the low-level safety layer is held fixed or ablated, as an important open research question and a concrete benchmark target. 

**Human–robot collaboration safety** introduces additional challenges beyond physical constraint satisfaction by requiring robots to account for both hard safety limits (e.g., force and speed) and softer human-centered factors such as comfort, predictability, and trust. During contact-rich interaction, operators must be able to anticipate robot behavior and intervene effectively, yet current learning-based controllers often lack transparency and interpretable failure modes. Existing safe learning pipelines predominantly encode physical thresholds while overlooking temporal predictability and trust metrics that are central to user acceptance [386–388]. Although adaptive safety frameworks have begun integrating ergonomic considerations and standard-driven constraints, such as the force envelopes defined in ISO/TS 15066 [43], their combination with learning-enabled adaptation remains limited. Advanced models, including VLAs, can in principle explain their intentions or request human assistance; however, designing effective interaction protocols, shared-autonomy mechanisms, and explanations that are both faithful and useful in high-contact scenarios remains an important open challenge. 

### **Perspectives** 

Safe robot learning for contact-rich manipulation is entering a phase where systematic advances in data, evaluation, and architectural composability must complement incremental improvements in algorithms. We outline key forward-looking directions. 

**Standardized safe-contact benchmarks** are essential for advancing reproducible evaluation of safe learning methods. Current benchmark suites under-represent multi-stage forceful interactions, deformable objects, and human-adjacent tasks [46, 77, 78, 89]. Future benchmarks should move beyond isolated manipulation tasks to standardized suites that stress high-force interactions, tight clearances, and diverse materials and fixtures. A key opportunity is to design benchmarks in which VLM/VLA models must interpret natural-language task descriptions and safety rules before executing contact-rich skills under explicit constraints on contact forces, slippage, and failure recovery. Future benchmark suites should also adopt consistent reporting practices, such as those summarized in Safety Evaluation Metrics section, to facilitate fair comparison of safety, task performance, efficiency, and robustness across methods. In particular, benchmarks should make it possible to attribute safety gains to the appropriate system layer, for example, by fixing or ablating the low-level safety filter to evaluate whether language-level constraint specification alone reduces measured contact-force violations. 

**Safety-aware and data-efficient learning frameworks** will be central to the next generation of contact-rich robotic systems. Future methods should tightly integrate formal safety mechanisms with advanced function approximators, including VLAs and other large policies pretrained on internet-scale multimodal data and robot demonstrations. Promising directions include risk-sensitive and constraint-aware VLA 

52 

controllers, hybrid model-based/model-free frameworks that combine high-level reasoning from large models with certified low-level safety filters, and approaches that leverage language for specifying, verifying, and adapting safety constraints during contact-rich interaction. 

**Bridging the sim-to-real safety gap** remains a prerequisite for deploying safe learning algorithms in real-world environments. Closing this gap will require simulators that faithfully reproduce contact dynamics while also capturing the perceptual and linguistic variability encountered by VLM/VLA policies. This opens the possibility of using generative models and large-scale VLAs to create diverse synthetic curricula of tasks, objects, and safety-critical edge cases, followed by safety-aware adaptation and online refinement on physical robots with continuous monitoring of contact forces, constraint violations, and failure modes. 

**Multimodal semantic grounding** is another critical direction for improving the reliability of VLA-based manipulation. Although VLA models have demonstrated impressive capabilities in scene understanding and semantic reasoning [4, 24, 27], robust grounding remains fragile under occlusion, clutter, and ambiguous physical interactions. A promising direction is layered grounding, progressing from scene parsing to affordance and constraint extraction, followed by formal constraint compilation (e.g., CBF/MPC formulations) and ultimately runtime conformance validation. In addition, safety-aware prompting and structured action representations can help reduce the risk of hallucinated unsafe behaviors [389]. 

**Human-centric and lifecycle-aware safety** extends beyond enforcing physical safety envelopes, such as limits on force and speed, which are necessary but not sufficient for the widespread adoption of collaborative robots [2]. Future safe learning frameworks can benefit from language-conditioned policies that understand instructions, preferences, and corrections expressed in natural language, enabling nonexpert users to shape safe behavior during contact-rich collaboration. Over the system lifecycle, advanced models such as VLAs may also support continual learning and selfdiagnostics, allowing robots to explain their contact strategies, identify emerging risks, and adapt their policies while preserving guarantees of human safety and equipment integrity. 

**Scalable verification for learned controllers** remains a major challenge as modern policy representations become increasingly expressive. Diffusion policies, latent-variable policies, and residual impedance controllers are difficult to analyze using classical verification techniques. A promising direction is to abstract policy outputs, such as stiffness and damping parameters, into reachable or invariant sets that admit formal safety analysis. Likewise, data-driven certificates, including learned control barrier functions and neural safety critics, require systematic mechanisms for failure detection, online adaptation, and certificate repair to prevent the gradual degradation of safety guarantees during long-term deployment. 

**Physically-aware foundation models** offer another promising direction for improving safe contact-rich manipulation. Current generalist manipulation models often fail to capture the underlying mechanics of physical interaction, resulting in unsafe extrapolation beyond the training distribution. Integrating structured physical priors, such as friction cones, passivity constraints, energy tanks, and contact mechanics, into 

53 

large-scale action models could substantially improve physical reliability. A hybrid “plan–parameterize–enforce” paradigm, in which a foundation model generates highlevel plans that are subsequently refined under impedance and barrier-based safety constraints, provides a principled framework for combining semantic reasoning with certified low-level execution [4, 35]. Furthermore, building large-scale datasets that are rich in contact interactions and explicitly annotated with safety-relevant events, failure modes, and physical constraints will be essential for training reliable next-generation robotic foundation models. 

**Open problems** remain at the intersection of learning, control, and physical interaction. Key unresolved issues include certified generalization under simultaneous geometric and material shifts [18], the synthesis of minimally conservative safe sets for multi-contact interactions, robust grounding of semantic constraints into physically enforceable safety guarantees, and lifelong adaptation with formal transient safety bounds. Addressing these challenges will require tighter integration of analytical safety frameworks with data-driven representations and robotic foundation models, enabling systems that are both adaptive and verifiably safe under complex contact dynamics. 

**The outlook for safe learning in contact-rich robotics** is increasingly shaped by the convergence of physically grounded control, formal safety theory, and foundation-model-based intelligence. Future progress will depend on combining physically grounded control methods, such as impedance control and passivity, with formal safety tools including control barrier functions and reachability analysis, scalable data resources such as standardized benchmarks, and high-level semantic reasoning enabled by VLMs and VLAs. A growing consensus supports layered “plan–learn– filter–execute” architectures that integrate semantic planning, adaptive learning, and certified low-level safety enforcement into a unified framework. Ultimately, establishing standardized evaluation protocols, interpretable safety metrics, and reproducible benchmarks will be essential for translating recent advances in safe learning into reliable deployment of autonomous robotic systems operating in complex, contact-rich environments. 

## **Discussion** 

In this survey, a comprehensive overview of safe learning methods for contact-rich robotic tasks has been presented, with a particular focus on how emerging foundation models reshape the landscape. Existing approaches have been organized along multiple dimensions, including sensing modalities, data acquisition strategies, simulation environments, safety evaluation metrics, abstraction levels, and task mobility contexts, to provide a structured view of the design space for safe contact-rich manipulation. 

The survey highlights the central role of multimodal sensing, such as force/torque, tactile, and vision, in enabling safe and robust behavior under complex contact conditions. Key challenges persist in data acquisition, safety metrics and certification, modeling of contact-rich interactions, and consistently enforcing safety constraints from high-level reasoning down to low-level control. Although we systematically searched multiple major academic databases and applied predefined inclusion criteria, the literature search was restricted to studies published between 2018 and 2025 and 

54 

may not capture all relevant work, particularly rapidly emerging research on robotic foundation models and safe contact-rich learning. 

Looking forward, hybrid architectures and advanced learning paradigms offer promising avenues. Opportunities include combining high-level planning with low-level compliant control, integrating classical safety mechanisms with learning-based policies, and leveraging VLM and VLA models to interpret safety requirements, ground them in multimodal observations, and support transparent, human-centered interaction in contact-rich scenarios. 

## **Methods** 

To ensure a comprehensive and systematic review of safe learning methods for robotic contact-rich tasks, we employed a multi-step methodology: 

### **Literature Investigation** 

We conducted an extensive investigation across major academic databases, including IEEE Xplore, ACM Digital Library, SpringerLink, and Google Scholar. Keywords used in the literature search included combinations of ”safe”, ”contact-rich tasks,” and ”learning”. To capture the most recent advancements, specifically, we use the following compliant search string: _(”robot” OR ”robotic”) AND (”safe” OR ”safety” OR ”stable”) AND (”contact-rich” OR ”multi-contact” OR ”contact-intensive” OR ”physical interaction” OR ”environment interaction” OR ”contact interaction” OR ”contact manipulation” OR ”contact force”) AND (intitle:”learning” OR intitle:”learn”)_ . The database search was last executed in August 2025; in addition, we screened the reference lists of the related surveys discussed above for further relevant works (backward snowballing). 

### **Inclusion Criteria** 

We focused on both peer-reviewed and preprint articles published from 2018 to 2025 that specifically addressed and/or discussed safety in learning-based approaches for contact-rich robotic tasks. Both theoretical contributions and empirical studies with experimental validation were considered. 

### **Analysis** 

Each paper was analyzed for its methodological contributions, safety guarantees and discussion among multiple different perspectives, experimental setups including simulation and real-world experiments, and limitations. 

### **Exclusion Criteria** 

We excluded works that (i) do not involve contact-rich interaction as defined in the section on Robotic Contact-Rich Tasks (e.g., free-space motion or pure pick-andplace), (ii) do not incorporate any learning component, (iii) do not address safety, stability, or constraint satisfaction in any form, or (iv) fall outside the 2018–2025 window. Duplicate records and non-archival materials were also removed. 

55 


**Figure 10** PRISMA-style flow of the systematic review, with the identification, de-duplication, screening, eligibility, and inclusion stages; the databases and the exact Boolean search string are given in the text. 

### **Selection and Screening** 

Records were processed in the standard identification–screening–eligibility–inclusion stages summarized in the PRISMA-style diagram of Fig. 10. Title/abstract screening and full-text eligibility assessment were each performed independently by two of the authors, and disagreements were resolved by discussion. The stage-wise counts, including records identified, records after de-duplication, records screened, full texts assessed, records excluded with reasons, and studies finally included, are reported in Fig. 10. 

## **Declarations** 

### **Data Availability** 

The curated literature dataset used to organize and analyse the studies included in this review is publicly available in the project repository at: https://github.com/ jack-sherman01/Awesome-Learning4Safe-Contact-rich-tasks/tree/main/docs 

### **Code Availability** 

The scripts used to curate and analyse the literature included in this review are available in the project repository at https://github.com/jack-sherman01/ Awesome-Learning4Safe-Contact-rich-tasks/tree/main/scripts. We also share the paper collection list with links for readers, which is available explicitly at: https: //github.com/jack-sherman01/Awesome-Learning4Safe-Contact-rich-tasks 

56 

### **Acknowledgements** 

This work was supported by the European Union Horizon Project TORNADO (Grant GA 101189557). 

### **Author Contributions** 

HZ conceived the study and led the manuscript development. HZ, RD, GS, and PZ conducted the literature investigation and analysis and prepared the initial draft of the manuscript. NT, YS, and AA contributed to the interpretation of the literature and provided critical revisions to the manuscript. AA supervised the study. All authors revised the manuscript, approved the final version, and agree to be accountable for the work. 

### **Competing Interests** 

The authors declare no competing interests. 

## **References** 

- [1] Billard, A. & Kragic, D. Trends and challenges in robot manipulation. _Science_ **364** , eaat8414 (2019). 

- [2] Ajoudani, A. _et al._ Progress and prospects of the human–robot collaboration. _Autonomous robots_ **42** , 957–975 (2018). 

- [3] Elguea-Aguinaco, I. _et al._ A review on reinforcement learning for contact-rich robotic manipulation tasks. _Robotics and Computer-Integrated Manufacturing_ **81** , 102517 (2023). 

- [4] T¨olle, M. _et al._ Towards safe robot foundation models. _arXiv preprint arXiv:2503.07404_ (2025). 

- [5] Zhang, H. _et al._ Compliantvla-adaptor: Vlm-guided variable impedance action for safe contact-rich manipulation (2026). URL https://arxiv.org/abs/2601. 15541. arXiv:2601.15541. 

- [6] Garc´ıa, J. & Fern´andez, F. A comprehensive survey on safe reinforcement learning. _Journal of Machine Learning Research_ **16** , 1437–1480 (2015). 

- [7] Brunke, L. _et al._ Safe learning in robotics: From learning-based control to safe reinforcement learning. _Annual Review of Control, Robotics, and Autonomous Systems_ **5** , 411–444 (2022). 

- [8] Zhao, W., He, T., Chen, R., Wei, T. & Liu, C. State-wise safe reinforcement learning: A survey. _International Joint Conference on Artificial Intelligence_ (2023). 

57 

- [9] Gu, S. _et al._ A review of safe reinforcement learning: Methods, theories and applications. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ (2024). 

- [10] Guerrier, M., Fouad, H. & Beltrame, G. Learning control barrier functions and their application in reinforcement learning: A survey. _arXiv preprint arXiv:2404.16879_ (2024). 

- [11] Odriozola-Olalde, H., Zamalloa, M. & Arana-Arexolaleiba, N. Shielded reinforcement learning: A review of reactive methods for safe learning. _2023 IEEE/SICE International Symposium on System Integration (SII)_ 1–8 (2023). 

- [12] Suomalainen, M., Karayiannidis, Y. & Kyrki, V. A survey of robot manipulation in contact. _Robotics and Autonomous Systems_ **156** , 104224 (2022). 

- [13] Kroemer, O., Niekum, S. & Konidaris, G. A review of robot learning for manipulation: Challenges, representations, and algorithms. _Journal of machine learning research_ **22** , 1–82 (2021). 

- [14] Xu, J., Hou, Z., Liu, Z. & Qiao, H. Compare contact model-based control and contact model-free learning: A survey of robotic peg-in-hole assembly strategies. _arXiv preprint arXiv:1904.05240_ (2019). 

- [15] Abu-Dakka, F. J. & Saveriano, M. Variable impedance control and learning—a review. _Frontiers in Robotics and AI_ **7** , 590681 (2020). 

- [16] Samadikhoshkho, Z., Saive, E. & Lipsett, M. G. A review of compliant mechanisms for contact robotics applications. _Robotics and Autonomous Systems_ **186** , 104902 (2025). 

- [17] Stan, L., Nicolescu, A. F. & Pup˘az˘a, C. Reinforcement learning for assembly robots: A review. _Proceedings in Manufacturing Systems_ **15** , 135–146 (2020). 

- [18] Das, A. R. & Koskinopoulou, M. Towards sustainable manufacturing: A review on innovations in robotic assembly and disassembly. _IEEE Access_ (2025). 

- [19] Tsuji, T. _et al._ A survey on imitation learning for contact-rich tasks in robotics. _arXiv preprint arXiv:2506.13498_ (2025). 

- [20] Kojima, T. _et al._ A comprehensive survey on physical risk control in the era of foundation model-enabled robotics. _arXiv preprint arXiv:2505.12583_ (2025). 

- [21] Lamba, P., Ravish, K., Kushwaha, A. & Kumar, P. Alignment and safety of diffusion models via reinforcement learning and reward modeling: A survey. _arXiv preprint arXiv:2505.17352_ (2025). 

- [22] Xie, W. & Correll, N. Towards forceful robotic foundation models: a literature survey. _arXiv preprint arXiv:2504.11827_ (2025). 

58 

- [23] Wabersich, K. P. _et al._ Data-driven safety filters: Hamilton-jacobi reachability, control barrier functions, and predictive methods for uncertain systems. _IEEE Control Systems Magazine_ **43** , 137–177 (2023). 

- [24] Zhang, B. _et al._ Safevla: Towards safety alignment of vision-language-action model via constrained learning. _arXiv preprint arXiv:2503.03480_ (2025). 

- [25] Salimpour, S. _et al._ Towards embodied agentic ai: Review and classification of llm-and vlm-driven robot autonomy and interaction. _arXiv preprint arXiv:2508.05294_ (2025). 

- [26] Cruz-Oliver, R. _Learning for contact-rich tasks with cobots_ . Master’s thesis, Eidgen¨ossische Technische Hochschule Z¨urich (ETH Zurich) (2024). 

- [27] Zhao, Z. _et al._ A survey of optimization-based task and motion planning: From classical to learning approaches. _IEEE/ASME Transactions on Mechatronics_ 1–27 (2024). 

- [28] Parnada, A., Qu, M., Castellani, M., Jin Chang, H. & Wang, Y. Towards costeffective and safe contact-rich robotic manipulation with reinforcement learning: A review of techniques for future industrial automation. _Proceedings of the Institution of Mechanical Engineers, Part I: Journal of Systems and Control Engineering_ **240** , 3–35 (2026). 

- [29] Huang, Y. _et al._ Human-like dexterous manipulation for anthropomorphic fivefingered hands: A review. _Biomimetic Intelligence and Robotics_ 100212 (2025). 

- [30] Sy Horng Ting, T. _et al._ A review of advanced force torque control strategies for precise nut-to-bolt mating in robotic assembly. _International Journal of Robotics & Control Systems_ **5** (2025). 

- [31] Lakshminarayanan, S. _et al._ Robots in manufacturing: Programming, control, and safety standards. _Digital Manufacturing_ 85–131 (2024). 

- [32] Sharma, V. K., Zhou, P., Xu, Z., She, Y. & Sivaranjani, S. Safe human–robot collaboration with risk tunable control barrier functions. _IEEE/ASME Trans. Mechatron._ **30** , 3133–3141 (2025). 

- [33] Luu, Q. K. _et al._ Manifeel: Benchmarking and understanding visuotactile manipulation policy learning. _arXiv preprint arXiv:2505.18472_ (2025). 

- [34] Hogan, N. Contact and physical interaction. _Annual Review of Control, Robotics, and Autonomous Systems_ **5** , 179–203 (2022). 

- [35] Bahl, S., Mukadam, M., Gupta, A. & Pathak, D. Neural dynamic policies for end-to-end sensorimotor learning. _Advances in Neural Information Processing Systems_ **33** , 5058–5069 (2020). 

59 

- [36] Chuck, C. _et al._ Robot air hockey: A manipulation testbed for robot learning with reinforcement learning. _arXiv preprint arXiv:2405.03113_ (2024). 

- [37] Tassi, F. _et al._ Ima-catcher: An impact-aware nonprehensile catching framework based on combined optimization and learning. _The International Journal of Robotics Research_ 02783649251345851 (2025). 

- [38] Pang, T. _Planning, sensing, and control for contact-rich robotic manipulation with quasi-static contact models_ (Massachusetts Institute of Technology, 2023). 

- [39] Branicky, M. S. Multiple lyapunov functions and other analysis tools for switched and hybrid systems. _IEEE Transactions on automatic control_ **43** , 475–482 (2002). 

- [40] Breeden, J. & Panagou, D. High relative degree control barrier functions under input constraints. _2021 60th IEEE Conference on Decision and Control (CDC)_ 6119–6124 (2021). 

- [41] Wang, H., Peng, J., Zhang, F., Zhang, H. & Wang, Y. High-order control barrier functions-based impedance control of a robotic manipulator with time-varying output constraints. _ISA transactions_ **129** , 361–369 (2022). 

- [42] Wong, K. _et al._ Contact-aware safety in soft robots using high-order control barrier and lyapunov functions. _arXiv preprint arXiv:2505.03841_ (2025). 

- [43] International Organization for Standardization. Robots and robotic devices — collaborative robots. ISO/TS 15066:2016, International Organization for Standardization, Geneva, Switzerland (2016). URL https://www.iso.org/standard/ 62996.html. Technical Specification. 

- [44] Calanca, A., Muradore, R. & Fiorini, P. A review of algorithms for compliant control of stiff and fixed-compliance robots. _IEEE/ASME transactions on mechatronics_ **21** , 613–624 (2015). 

- [45] Huang, Z., Hou, H. & Berenson, D. Unified Multimodal Diffusion Forcing for Forceful Manipulation (2025). URL http://arxiv.org/abs/2511.04812. ArXiv:2511.04812 [cs] version: 1. 

- [46] Yuan, Z. _et al._ Safe-control-gym: A unified benchmark suite for safe learningbased control and reinforcement learning in robotics. _IEEE Robotics and Automation Letters_ **7** , 11142–11149 (2022). 

- [47] Khader, S. A., Yin, H., Falco, P. & Kragic, D. Stability-guaranteed reinforcement learning for contact-rich manipulation. _IEEE Robotics and Automation Letters_ **6** , 1–8 (2020). 

60 

- [48] Ji, J. _et al._ Safety gymnasium: A unified safe reinforcement learning benchmark. _Advances in Neural Information Processing Systems_ **36** , 18964–18993 (2023). 

- [49] Khalil, H. K. & Grizzle, J. W. _Nonlinear systems_ Vol. 3 (Prentice hall Upper Saddle River, NJ, 2002). 

- [50] Kumar, S. & Prakash, R. Safe and Optimal Variable Impedance Control via Certified Reinforcement Learning (2025). URL http://arxiv.org/abs/2511.16330. ArXiv:2511.16330 [cs]. 

- [51] Ames, A. D. _et al._ Control barrier functions: Theory and applications. _2019 18th European control conference (ECC)_ 3420–3431 (2019). 

- [52] Liu, J. _et al._ Flexible active safety motion control for robotic obstacle avoidance: A cbf-guided mpc approach. _IEEE Robotics and Automation Letters_ **10** , 2686– 2693 (2025). URL http://dx.doi.org/10.1109/lra.2025.3534519. 

- [53] Liang, H., Wang, X., Mao, J. & Yang, J. Control barrier function-based force constrained safety compliance control for manipulator. _2023 28th International Conference on Automation and Computing (ICAC)_ 1–7 (2023). URL http: //dx.doi.org/10.1109/icac57885.2023.10275266. 

- [54] Cheng, R., Orosz, G., Murray, R. M. & Burdick, J. W. End-to-end safe reinforcement learning through barrier functions for safety-critical continuous control tasks. _Proceedings of the AAAI conference on artificial intelligence_ **33** , 3387–3395 (2019). 

- [55] Bouvier, J.-B., Nagpal, K. & Mehr, N. Policed rl: Learning closed-loop robot control policies with provable satisfaction of hard constraints. _Robotics: Science and Systems_ (2024). 

- [56] Hewing, L., Wabersich, K. P., Menner, M. & Zeilinger, M. N. Learning-based model predictive control: Toward safe learning in control. _Annual Review of Control, Robotics, and Autonomous Systems_ **3** , 269–296 (2020). URL https://www. annualreviews.org/content/journals/10.1146/annurev-control-090419-075625. 

- [57] Mitsioni, I., Tajvar, P., Kragic, D., Tumova, J. & Pek, C. Safe data-driven model predictive control of systems with complex dynamics. _IEEE Transactions on Robotics_ **39** , 3242–3258 (2023). 

- [58] Bansal, S., Chen, M., Herbert, S. & Tomlin, C. J. Hamilton-jacobi reachability: A brief overview and recent advances. _2017 IEEE 56th Annual Conference on Decision and Control (CDC)_ 2242–2253 (2017). 

- [59] Shao, Y. S., Chen, C., Kousik, S. & Vasudevan, R. Reachability-based trajectory safeguard (rts): A safe and fast reinforcement learning safety layer for continuous control. _IEEE Robotics and Automation Letters_ **6** , 3663–3670 (2021). URL 

61 

http://dx.doi.org/10.1109/lra.2021.3063989. 

- [60] Thananjeyan, B. _et al._ Recovery rl: Safe reinforcement learning with learned recovery zones. _IEEE Robotics and Automation Letters_ **6** , 4915–4922 (2021). 

- [61] Srinivasan, K., Eysenbach, B., Ha, S., Tan, J. & Finn, C. Learning to be safe: Deep rl with a safety critic. _arXiv preprint arXiv:2010.14603_ (2020). 

- [62] Massiani, P.-F., Heim, S., Solowjow, F. & Trimpe, S. Safe value functions. _IEEE Transactions on Automatic Control_ **68** , 2743–2757 (2023). URL http: //dx.doi.org/10.1109/tac.2022.3200948. 

- [63] Hsu, K.-C., Ren, A. Z., Nguyen, D. P., Majumdar, A. & Fisac, J. F. Sim-to-labto-real: Safe reinforcement learning with shielding and generalization guarantees. _Artificial Intelligence_ **314** , 103811 (2023). URL http://dx.doi.org/10.1016/j. artint.2022.103811. 

- [64] Farajtabar, M. & Charbonneau, M. The path towards contact-based physical human–robot interaction. _Robotics and Autonomous Systems_ 104829 (2024). 

- [65] Chemweno, P., Pintelon, L. & Decre, W. Orienting safety assurance with outcomes of hazard analysis and risk assessment: A review of the iso 15066 standard for collaborative robot systems. _Safety Science_ **129** , 104832 (2020). URL http://dx.doi.org/10.1016/j.ssci.2020.104832. 

- [66] Zhao, X., Fan, T., Li, Y., Zheng, Y. & Pan, J. An efficient and responsive robot motion controller for safe human-robot collaboration. _IEEE Robotics and Automation Letters_ **6** , 6068–6075 (2021). 

- [67] El-Shamouty, M., Wu, X., Yang, S., Albus, M. & Huber, M. F. Towards safe human-robot collaboration using deep reinforcement learning. _2020 IEEE international conference on robotics and automation (ICRA)_ 4899–4905 (2020). 

- [68] Zhang, D., Van, M., Mcllvanna, S., Sun, Y. & McLoone, S. Adaptive safetycritical control with uncertainty estimation for human–robot collaboration. _IEEE Transactions on Automation Science and Engineering_ **21** , 5983–5996 (2023). 

- [69] Sun, Z., Wang, Y., Held, D. & Erickson, Z. Force-constrained visual policy: Safe robot-assisted dressing via multi-modal sensing. _IEEE Robotics and Automation Letters_ (2024). 

- [70] Xu, F. _et al._ Stare-vla: Progressive stage-aware reinforcement for fine-tuning vision-language-action models. _arXiv preprint arXiv:2512.05107_ (2025). 

- [71] Thumm, J., Agia, C., Pavone, M. & Althoff, M. Text2interaction: Establishing safe and preferable human-robot interaction. _Conference on Robot Learning_ 

62 

1250–1267 (2025). 

- [72] Zhou, W. _et al._ PhysVLM: Enabling Visual Language Models to Understand Robotic Physical Reachability (2025). URL http://arxiv.org/abs/2503.08481. ArXiv:2503.08481 [cs]. 

- [73] Wei, X. _et al._ Audio-VLA: Adding Contact Audio Perception to VisionLanguage-Action Model for Robotic Manipulation (2025). URL http://arxiv. org/abs/2511.09958. ArXiv:2511.09958 [cs]. 

- [74] Cui, Y. _et al._ End-to-End Dexterous Arm-Hand VLA Policies via Shared Autonomy: VR Teleoperation Augmented by Autonomous Hand VLA Policy for Efficient Data Collection (2025). URL https://arxiv.org/abs/2511.00139v1. 

- [75] Lu, G. _et al._ VLA-RL: Towards Masterful and General Robotic Manipulation with Scalable Reinforcement Learning (2025). URL http://arxiv.org/abs/2505. 18719. ArXiv:2505.18719 [cs]. 

- [76] Zhang, H., Huang, W.-H., Solak, G. & Ajoudani, A. Omnivic: A self-improving variable impedance controller with vision-language in-context learning for safe robotic manipulation. _arXiv preprint arXiv:2510.17150_ (2025). 

- [77] Geng, H. _et al._ Roboverse: Towards a unified platform, dataset and benchmark for scalable and generalizable robot learning. _arXiv preprint arXiv:2504.18904_ (2025). 

- [78] Gu, S. _et al._ Robust gymnasium: A unified modular benchmark for robust reinforcement learning. _arXiv preprint arXiv:2502.19652_ (2025). 

- [79] Zhang, H., Solak, G., Lahr, G. J. G. & Ajoudani, A. Srl-vic: A variable stiffnessbased safe reinforcement learning for contact-rich robotic tasks. _IEEE Robotics and Automation Letters_ **9** , 5631–5638 (2024). 

- [80] Roveda, L. _et al._ Model-based reinforcement learning variable impedance control for human-robot collaboration. _Journal of Intelligent & Robotic Systems_ **100** , 417–433 (2020). 

- [81] Zhang, H., Solak, G., Hjorth, S. & Ajoudani, A. Passivity-centric safe reinforcement learning for contact-rich robotic tasks (2025). URL https://arxiv.org/abs/ 2503.00287. arXiv:2503.00287. 

- [82] Lin, N. _et al._ Reinforcement learning for robotic safe control with force sensing. _2019 WRC Symposium on Advanced Robotics and Automation (WRC SARA)_ 148–153 (2019). 

63 

- [83] Li, A., Liu, R., Yang, X. & Lou, Y. _Reinforcement Learning Strategy Based on Multimodal Representations for High-Precision Assembly Tasks_ , 56– 66 (Springer International Publishing, 2021). URL http://dx.doi.org/10.1007/ 978-3-030-89095-7 ~~6~~ . 

- [84] Luo, J., Dong, P., Zhai, Y., Ma, Y. & Levine, S. Rlif: Interactive imitation learning as reinforcement learning. _arXiv preprint arXiv:2311.12996_ (2023). 

- [85] Wang, Y., Beltran-Hernandez, C. C., Wan, W. & Harada, K. Robotic imitation of human assembly skills using hybrid trajectory and force learning. _2021 IEEE International Conference on Robotics and Automation (ICRA)_ 11278–11284 (2021). 

- [86] Anand, A. S., Gravdahl, J. T. & Abu-Dakka, F. J. Model-based variable impedance learning control for robotic manipulation. _Robotics and Autonomous Systems_ **170** , 104531 (2023). URL http://dx.doi.org/10.1016/j.robot.2023. 104531. 

- [87] Zhou, H., Ma, S., Wang, G., Deng, Y. & Liu, Z. A hybrid control strategy for grinding and polishing robot based on adaptive impedance control. _Advances in Mechanical Engineering_ **13** (2021). URL http://dx.doi.org/10.1177/ 16878140211004034. 

- [88] Xu, Y. _et al._ Look before you leap: Safe model-based reinforcement learning with human intervention. _Conference on robot learning_ 332–341 (2022). 

- [89] Towers, M. _et al._ Gymnasium: A standard interface for reinforcement learning environments. _arXiv preprint arXiv:2407.17032_ (2024). 

- [90] Raffin, A. _et al._ Stable-baselines3: Reliable reinforcement learning implementations. _Journal of machine learning research_ **22** , 1–8 (2021). 

- [91] Chi, W. & Meng, M. Q.-H. Risk-rrt*: A robot motion planning algorithm for the human robot coexisting environment. _Proc. 18th Int. Conf. Adv. Robot. (ICAR)_ 583–588 (2017). 

- [92] Rodr´ıguez-Guerra, D., Mosca, A., Valente, A., Cabanes, I. & Carpanzano, E. An advanced dual apf-based controller for efficient simultaneous collision and singularity avoidance for human-robot collaborative assembly processes. _CIRP Annals_ **72** , 5–8 (2023). 

- [93] Bowyer, S. A., Davies, B. L. & y Baena, F. R. Active constraints/virtual fixtures: A survey. _IEEE Trans. Robot._ **30** , 138–157 (2013). 

- [94] Hsu, K.-C., Hu, H. & Fisac, J. F. The safety filter: A unified view of safetycritical control in autonomous systems. _Annu. Rev. Control Robot. Auton. Syst._ **7** (2023). 

64 

- [95] Ferraguti, F. _et al._ Safety barrier functions and multi-camera tracking for human–robot shared environment. _Rob. Auton. Syst._ **124** , 103388 (2020). 

- [96] Dai, B. _et al._ Safe navigation and obstacle avoidance using differentiable optimization based control barrier functions. _IEEE Robot. Autom. Lett._ (2023). 

- [97] Das, E. & Burdick, J. W. Robust control barrier functions using uncertainty estimation with application to mobile robots. _arXiv preprint arXiv:2401.01881_ (2024). 

- [98] Li, J., Liu, Q., Jin, W., Qin, J. & Hirche, S. Robust safe learning and control in an unknown environment: An uncertainty-separated control barrier function approach. _IEEE Robot. Autom. Lett._ (2023). 

- [99] Wang, D. & Zhang, J. Flow shop scheduling with human–robot collaboration: A joint chance-constrained programming approach. _Int. J. Prod. Res._ **62** , 1297– 1317 (2024). 

- [100] Toit, N. E. D. & Burdick, J. W. Probabilistic collision checking with chance constraints. _IEEE Trans. Robot._ **27** , 809–815 (2011). 

- [101] Ahmed, S. & Shapiro, A. Solving chance-constrained stochastic programs via sampling and integer programming. _State-of-the-Art Decision-Making Tools in the Information-Intensive Age_ 261–269 (2008). 

- [102] Berx, N., Decr´e, W., Morag, I., Chemweno, P. & Pintelon, L. Identification and classification of risk factors for human-robot collaboration from a system-wide perspective. _Computers & Industrial Engineering_ **163** , 107827 (2022). 

- [103] Inam, R. _et al._ Risk assessment for human-robot collaboration in an automated warehouse scenario. _2018 IEEE 23rd International Conference on Emerging Technologies and Factory Automation (ETFA)_ **1** , 743–751 (2018). 

- [104] Liu, Z. _et al._ Dynamic risk assessment and active response strategy for industrial human-robot collaboration. _Computers & Industrial Engineering_ **141** , 106302 (2020). 

- [105] Majumdar, A. & Pavone, M. How should a robot assess risk? towards an axiomatic theory of risk in robotics. _Robotics Research: The 18th International Symposium ISRR_ 75–84 (2020). 

- [106] Holmes, P. _et al._ Reachable Sets for Safe, Real-Time Manipulator Trajectory Design. _Proceedings of Robotics: Science and Systems_ (2020). 

- [107] Kousik, S., Vaskov, S., Bu, F., Johnson-Roberson, M. & Vasudevan, R. Bridging the gap between safety and real-time performance in receding-horizon trajectory design for mobile robots. _The International Journal of Robotics Research_ **39** , 

65 

1419–1469 (2020). 

- [108] Banerjee, A., Rahmani, K., Biswas, J. & Dillig, I. Dynamic model predictive shielding for provably safe reinforcement learning. _Advances in Neural Information Processing Systems_ **37** , 100131–100159 (2024). 

- [109] Yamada, J. _et al._ Motion planner augmented reinforcement learning for robot manipulation in obstructed environments. _Conference on Robot Learning_ 589– 603 (2021). 

- [110] Zhao, W., Li, F. & Liu, C. Implicit safe set algorithm for provably safe reinforcement learning. _arXiv preprint arXiv:2405.02754_ (2024). 

- [111] Mazouz, R. _et al._ Data-driven permissible safe control with barrier certificates. _2024 IEEE 63rd Conference on Decision and Control (CDC)_ 6844–6849 (2024). URL http://dx.doi.org/10.1109/cdc56724.2024.10886850. 

- [112] Sootla, A. _et al._ Saut´e rl: Almost surely safe reinforcement learning using state augmentation. _International Conference on Machine Learning_ 20423–20443 (2022). 

- [113] Yang, Q., Sim˜ao, T. D., Tindemans, S. H. & Spaan, M. T. J. Wcsac: Worstcase soft actor critic for safety-constrained reinforcement learning. _Proceedings of the AAAI Conference on Artificial Intelligence_ **35** , 10639–10646 (2021). URL http://dx.doi.org/10.1609/aaai.v35i12.17272. 

- [114] Lei, F. _et al._ Langevin policy for safe reinforcement learning. _Forty-first International Conference on Machine Learning_ (2024). 

- [115] Wagener, N. C., Boots, B. & Cheng, C.-A. Safe reinforcement learning using advantage-based intervention. _International Conference on Machine Learning_ 10630–10640 (2021). 

- [116] Sim˜ao, T. D., Jansen, N. & Spaan, M. T. Alwayssafe: Reinforcement learning without safety constraint violations during training. _Proceedings of the 20th International Conference on Autonomous Agents and MultiAgent Systems (AAMAS)_ (2021). 

- [117] Li, X., Xiao, J., Cheng, Y. & Liu, H. An actor-critic learning framework based on lyapunov stability for automatic assembly. _Applied Intelligence_ **53** , 4801–4812 (2023). 

- [118] Kim, S., Kwon, J., Lee, T., Park, Y. & Perez, J. Safety-aware unsupervised skill discovery. _ICRA_ 894–900 (2023). 

- [119] Yang, Q., D¨urr, A., Topp, E. A., Stork, J. A. & Stoyanov, T. Variable impedance skill learning for contact-rich manipulation. _IEEE robotics and automation_ 

66 

_letters_ **7** , 8391–8398 (2022). 

- [120] Sharifi, M., Azimi, V., Mushahwar, V. K. & Tavakoli, M. Impedance learningbased adaptive control for human–robot interaction. _IEEE Transactions on Control Systems Technology_ **30** , 1345–1358 (2022). 

- [121] Xu, Y. _et al._ A learning control strategy for robot-assisted bathing via impedance sliding mode technique with non-repetitive tasks. _International Journal of Control, Automation and Systems_ **22** , 946–962 (2024). 

- [122] Zhao, X., Zhao, H., Chen, P. & Ding, H. Model accelerated reinforcement learning for high precision robotic assembly. _International Journal of Intelligent Robotics and Applications_ **4** , 202–216 (2020). URL http://dx.doi.org/10.1007/ s41315-020-00138-z. 

- [123] Bastani, O., Li, S. & Xu, A. Safe reinforcement learning via statistical model predictive shielding. _Robotics: Science and Systems_ 1–13 (2021). 

- [124] Han, M., Zhang, L., Wang, J. & Pan, W. Actor-critic reinforcement learning for control with stability guarantee. _IEEE Robotics and Automation Letters_ **5** , 6217–6224 (2020). 

- [125] Guo, M., Yao, B., Ji, Z., Xu, W. & Zhou, Z. Adaptive admittance control for physical human-robot interaction based on imitation and reinforcement learning. _2023 29th International Conference on Mechatronics and Machine Vision in Practice (M2VIP)_ 1–5 (2023). URL http://dx.doi.org/10.1109/m2vip58386. 2023.10413438. 

- [126] Murtaza, M. A., Aguilera, S., Waqas, M. & Hutchinson, S. Safety compliant control for robotic manipulator with task and input constraints. _IEEE Robotics and Automation Letters_ **7** , 10659–10664 (2022). 

- [127] Hogan, N. Impedance control: An approach to manipulation: Part i—theory. _Journal of Dynamic Systems, Measurement, and Control_ **107** , 1–7 (1985). 

- [128] Sun, Y. _et al._ Adaptive admittance control for safety-critical physical human robot collaboration. _IFAC-PapersOnLine_ **56** , 1313–1318 (2023). URL http: //dx.doi.org/10.1016/j.ifacol.2023.10.1772. 

- [129] Samuel, K., Haninger, K., Oboe, R., Haddadin, S. & Oh, S. A perturbationrobust framework for admittance control of robotic systems with high-stiffness contacts and heavy payload. _IEEE Robotics and Automation Letters_ **9** , 6432– 6439 (2024). URL http://dx.doi.org/10.1109/lra.2024.3406055. 

- [130] Mart´ınez, D., Alenya, G. & Torras, C. Safe robot execution in model-based reinforcement learning. _2015 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ 6422–6427 (2015). 

67 

- [131] Luo, J. _et al._ Reinforcement learning on variable impedance controller for highprecision robotic assembly. _2019 International Conference on Robotics and Automation (ICRA)_ 3080–3087 (2019). 

- [132] Gai, Y., Wang, B., Zhang, J., Wu, D. & Chen, K. Robotic assembly control reconfiguration based on transfer reinforcement learning for objects with different geometric features. _Engineering Applications of Artificial Intelligence_ **129** , 107576 (2024). URL http://dx.doi.org/10.1016/j.engappai.2023.107576. 

- [133] Hafez, A., Awad, M. I., Gomaa, W. & Maged, S. A. Meta reinforcement learning for robust and adaptable robotic assembly tasks. _2021 16th International Conference on Computer Engineering and Systems (ICCES)_ 1–7 (2021). URL http://dx.doi.org/10.1109/icces54031.2021.9686128. 

- [134] Chen, C., Zhang, C. & Pan, Y. Active compliance control of robot peg-in-hole assembly based on combined reinforcement learning. _Applied Intelligence_ **53** , 30677–30690 (2023). URL http://dx.doi.org/10.1007/s10489-023-05156-5. 

- [135] Schoettler, G., Nair, A., Ojea, J. A., Levine, S. & Solowjow, E. Metareinforcement learning for robotic industrial insertion tasks. _2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ 9728–9735 (2020). 

- [136] Wu, X., Zhang, D., Qin, F. & Xu, D. Deep reinforcement learning of robotic precision insertion skill accelerated by demonstrations. _2019 IEEE 15th International Conference on Automation Science and Engineering (CASE)_ 1651–1656 (2019). URL http://dx.doi.org/10.1109/coase.2019.8842940. 

- [137] Ding, Y., Zhao, J. & Min, X. Impedance control and parameter optimization of surface polishing robot based on reinforcement learning. _Proceedings of the Institution of Mechanical Engineers, Part B: Journal of Engineering Manufacture_ **237** , 216–228 (2022). URL http://dx.doi.org/10.1177/09544054221100004. 

- [138] Zhu, X., Kang, S. & Chen, J. A contact-safe reinforcement learning framework for contact-rich robot manipulation. _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ 2476–2482 (2022). 

- [139] Tang, Y., Chu, X., Huang, J. & Au, K. S. Learning-based mpc with safety filter for constrained deformable linear object manipulation. _IEEE Robotics and Automation Letters_ **9** , 2877–2884 (2024). 

- [140] Zhang, T., Xu, J. & Zhang, H. Enhancing Safety in ModelBased Reinforcement Learning With High-Order Control Barrier Functions. _International Journal of Robust and Nonlinear Control_ **n/a** (2025). URL https://onlinelibrary.wiley.com/doi/abs/10.1002/rnc.7888. ~~e~~ print: https://onlinelibrary.wiley.com/doi/pdf/10.1002/rnc.7888. 

68 

- [141] Blanchini, F. Set invariance in control. _Automatica_ **35** , 1747–1767 (1999). 

- [142] Blanchini, F., Miani, S. _et al. Set-theoretic methods in control_ Vol. 78 (Springer, 2008). 

- [143] Slotine, J.-J. E., Li, W. _et al. Applied nonlinear control_ Vol. 199 (Prentice hall Englewood Cliffs, NJ, 1991). 

- [144] Dalle Vedove, M., Lamon, E., Fontanelli, D., Palopoli, L. & Saveriano, M. A passivity-based variable impedance controller for incremental learning of periodic interactive tasks. _2024 IEEE 20th International Conference on Automation Science and Engineering (CASE)_ 2604–2609 (2024). 

- [145] Karacan, K., Sadeghian, H., Kirschner, R. & Haddadin, S. Passivity-based skill motion learning in stiffness-adaptive unified force-impedance control. _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ 9604–9611 (2022). 

- [146] Vinter-Hviid, F., Sloth, C., Savarimuthu, T. R. & Iturrate, I. Safe contact-based robot active search using bayesian optimization and control barrier functions. _Frontiers in Robotics and AI_ **11** , 1344367 (2024). 

- [147] Wang, C., Zhang, X., Kuang, Z. & Tomizuka, M. Safe online gain optimization for cartesian space variable impedance control. _2022 IEEE 18th International Conference on Automation Science and Engineering (CASE)_ 751–757 (2022). 

- [148] Li, Y. _et al._ Deep reinforcement learning-based variable impedance control for grinding workpieces with complex geometry. _Robotic Intelligence and Automation_ (2025). 

- [149] Li, Y., Zheng, L., Wang, Y., Dong, E. & Zhang, S. Impedance learning-based adaptive force tracking for robot on unknown terrains. _IEEE Transactions on Robotics_ (2025). 

- [150] Van Der Schaft, A., Jeltsema, D. _et al._ Port-hamiltonian systems theory: An introductory overview. _Foundations and Trends® in Systems and Control_ **1** , 173–378 (2014). 

- [151] Forni, F. & Sepulchre, R. Differential dissipativity theory for dominance analysis. _IEEE Transactions on Automatic Control_ **64** , 2340–2351 (2018). 

- [152] Hill, D. J. & Liu, T. Dissipativity, stability, and connections: Progress in complexity. _IEEE Control Systems Magazine_ **42** , 88–106 (2022). 

- [153] Giesl, P. & Hafstein, S. Review on computational methods for lyapunov functions. _Discrete and Continuous Dynamical Systems-B_ **20** , 2291–2331 (2015). 

69 

- [154] Manchester, I. R. & Slotine, J.-J. E. Control contraction metrics: Convex and intrinsic criteria for nonlinear feedback design. _IEEE Transactions on Automatic Control_ **62** , 3046–3053 (2017). 

- [155] Romdlony, M. Z. & Jayawardhana, B. Stabilization with guaranteed safety using control lyapunov–barrier function. _Automatica_ **66** , 39–47 (2016). 

- [156] Li, B., Wen, S., Yan, Z., Wen, G. & Huang, T. A survey on the control lyapunov function and control barrier function for nonlinear-affine control systems. _IEEE/CAA Journal of Automatica Sinica_ **10** , 584–602 (2023). 

- [157] Manjunath, A. & Nguyen, Q. Safe and robust motion planning for dynamic robotics via control barrier functions. _Proc. IEEE Conf. Decis. Control (CDC)_ 2122–2128 (2021). 

- [158] Wu, G. & Sreenath, K. Safety-critical and constrained geometric control synthesis using control lyapunov and control barrier functions for systems evolving on manifolds. _2015 American Control Conference (ACC)_ 2038–2044 (2015). 

- [159] Ames, A. D., Xu, X., Grizzle, J. W. & Tabuada, P. Control barrier function based quadratic programs for safety critical systems. _IEEE Transactions on Automatic Control_ **62** , 3861–3876 (2016). 

- [160] Batinovic, A., Goricanec, J., Markovic, L. & Bogdan, S. Path planning with potential field-based obstacle avoidance in a 3d environment by an unmanned aerial vehicle. _2022 International Conference on Unmanned Aircraft Systems (ICUAS)_ 394–401 (2022). 

- [161] Pan, Z., Zhang, C., Xia, Y., Xiong, H. & Shao, X. An improved artificial potential field method for path planning and formation control of the multi-uav systems. _IEEE Transactions on Circuits and Systems II: Express Briefs_ **69** , 1129–1133 (2021). 

- [162] Pati, T. & Yong, S. Z. Robust control barrier functions for control affine systems with time-varying parametric uncertainties. _IFAC-PapersOnLine_ **56** , 10588– 10594 (2023). 

- [163] Buch, J., Liao, S.-C. & Seiler, P. Robust control barrier functions with sectorbounded uncertainties. _IEEE Control Systems Letters_ **6** , 1994–1999 (2021). 

- [164] Wang, S. & Wen, S. Safe control against uncertainty: A comprehensive review of control barrier function strategies. _IEEE Systems, Man, and Cybernetics Magazine_ **11** , 34–47 (2025). 

- [165] Isaly, A., Ghanbarpour, M., Sanfelice, R. G. & Dixon, W. E. On the feasibility and continuity of feedback controllers defined by multiple control barrier functions. _IEEE Transactions on Automatic Control_ **69** , 7326–7339 (2024). 

70 

- [166] Breeden, J. & Panagou, D. Compositions of multiple control barrier functions under input constraints. _2023 American Control Conference (ACC)_ 3688–3695 (2023). 

- [167] Liu, R., Huang, J., Lu, B. & Ding, W. Certified neural network control architectures: Methodological advances in stability, robustness, and cross-domain applications. _Mathematics_ **13** , 1677 (2025). 

- [168] Lohmiller, W. & Slotine, J.-J. E. On contraction analysis for non-linear systems. _Automatica_ **34** , 683–696 (1998). 

- [169] Slotine, J.-J. E. Modular stability tools for distributed computation and control. _International Journal of Adaptive Control and Signal Processing_ **17** , 397–416 (2003). 

- [170] Giesl, P., Hafstein, S. & Mehrabinezhad, I. Computing contraction metrics for three-dimensional systems. _IFAC-PapersOnLine_ **54** , 297–303 (2021). 

- [171] Giesl, P., Hafstein, S. & Kawan, C. Review on contraction analysis and computation of contraction metrics. _arXiv preprint arXiv:2203.01367_ (2022). 

- [172] Singh, S., Majumdar, A., Slotine, J.-J. & Pavone, M. Robust online motion planning via contraction theory and convex optimization. _2017 IEEE International Conference on Robotics and Automation (ICRA)_ 5883–5890 (2017). 

- [173] Mitchell, I. M., Bayen, A. M. & Tomlin, C. J. A time-dependent hamilton-jacobi formulation of reachable sets for continuous dynamic games. _IEEE Transactions on automatic control_ **50** , 947–957 (2005). 

- [174] Mballo, C. E., Lee, D. & Tomlin, C. J. A hamilton-jacobi reachability framework with soft constraints for safety-critical systems. _arXiv preprint arXiv:2510.24933_ (2025). 

- [175] Choi, J. J. _et al._ A forward reachability perspective on robust control invariance and discount factors in reachability analysis. _arXiv preprint arXiv:2310.17180_ (2023). 

- [176] Liu, V., Manzie, C. & Dower, P. M. A hamilton-jacobi-bellman approach to ellipsoidal approximations of reachable sets for linear time-varying systems. _IEEE Transactions on Automatic Control_ (2024). 

- [177] Darbon, J. & Osher, S. Algorithms for overcoming the curse of dimensionality for certain hamilton–jacobi equations arising in control theory and elsewhere. _Research in the Mathematical Sciences_ **3** , 19 (2016). 

- [178] Bansal, S. & Tomlin, C. J. Deepreach: A deep learning approach to highdimensional reachability. _2021 IEEE International Conference on Robotics and_ 

71 

_Automation (ICRA)_ 1817–1824 (2021). 

- [179] Ganai, M., Gong, Z., Yu, C., Herbert, S. & Gao, S. Iterative reachability estimation for safe reinforcement learning. _Advances in Neural Information Processing Systems_ **36** , 69764–69797 (2023). 

- [180] Liu, S. _Reachable Sets for Control and Planning: from Reactive Safety to Contact-Rich Manipulation_ . Ph.D. thesis, Carnegie Mellon University Pittsburgh (2025). 

- [181] Selim, M. _et al._ Safe reinforcement learning using black-box reachability analysis. _IEEE Robotics and Automation Letters_ **7** , 10665–10672 (2022). 

- [182] Kochdumper, N., Krasowski, H., Wang, X., Bak, S. & Althoff, M. Provably safe reinforcement learning via action projection using reachability analysis and polynomial zonotopes. _IEEE Open Journal of Control Systems_ **2** , 79–92 (2023). 

- [183] Suh, H., Pang, T., Zhao, T. & Tedrake, R. Dexterous contact-rich manipulation via the contact trust region. _arXiv preprint arXiv:2505.02291_ (2025). 

- [184] Lew, T. _et al._ Robotic table wiping via reinforcement learning and wholebody trajectory optimization. _2023 IEEE International Conference on Robotics and Automation (ICRA)_ 7184–7190 (2023). URL http://dx.doi.org/10.1109/ icra48891.2023.10161283. 

- [185] Hou, Y. _et al._ Adaptive compliance policy: Learning approximate compliance for diffusion guided control. _arXiv preprint arXiv:2410.09309_ (2024). 

- [186] Rundong, W. _et al._ Robomt: Human-like compliance control for assembly via a bilateral robotic teleoperation and hybrid mamba-transformer framework. _IEEE Robotics and Automation Letters_ **10** , 7771–7778 (2025). URL http://dx.doi. org/10.1109/lra.2025.3579238. 

- [187] Tracy, K. _et al._ Efficient online learning of contact force models for connector insertion. _2025 IEEE International Conference on Robotics and Automation (ICRA)_ 10944–10950 (2025). URL http://dx.doi.org/10.1109/icra55743.2025. 11127717. 

- [188] Kang, G., Seong, H., Lee, D. & Shim, D. H. A versatile door opening system with mobile manipulator through adaptive position-force control and reinforcement learning. _Robotics and Autonomous Systems_ **180** , 104760 (2024). 

- [189] Okada, M., Komatsu, M., Okumura, R. & Taniguchi, T. Learning compliant stiffness by impedance control-aware task segmentation and multi-objective bayesian optimization with priors. _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ 8155–8162 (2023). URL http: //dx.doi.org/10.1109/iros55552.2023.10342096. 

72 

- [190] Padalkar, A., Nieuwenhuisen, M., Schulz, D. & Stulp, F. _Closing the Gap: Combining Task Specification and Reinforcement Learning for Compliant Vegetable Cutting_ , 187–206 (Springer International Publishing, 2022). URL http: //dx.doi.org/10.1007/978-3-030-92442-3 ~~1~~ 1. 

- [191] Kuo, C.-Y., Schaarschmidt, A., Cui, Y., Asfour, T. & Matsubara, T. Uncertainty-aware contact-safe model-based reinforcement learning. _IEEE Robotics and Automation Letters_ **6** , 3918–3925 (2021). 

- [192] Mathew, M. J. _et al._ Online learning of feed-forward models for task-space variable impedance control. _2019 IEEE-RAS 19th International Conference on Humanoid Robots (Humanoids)_ 222–229 (2019). 

- [193] Si, W., Guan, Y. & Wang, N. Adaptive compliant skill learning for contact-rich manipulation with human in the loop. _IEEE Robotics and Automation Letters_ **7** , 5834–5841 (2022). 

- [194] Oikawa, M., Kusakabe, T., Kutsuzawa, K., Sakaino, S. & Tsuji, T. Reinforcement learning for robotic assembly using non-diagonal stiffness matrix. _IEEE Robotics and Automation Letters_ **6** , 2737–2744 (2021). URL http://dx.doi.org/ 10.1109/lra.2021.3060389. 

- [195] Noseworthy, M. _et al._ Forge: Force-guided exploration for robust contact-rich manipulation under uncertainty. _IEEE Robotics and Automation Letters_ (2025). 

- [196] Lin, H., Corcodel, R. & Zhao, D. Generalize by touching: Tactile ensemble skill transfer for robotic furniture assembly. _2024 IEEE International Conference on Robotics and Automation (ICRA)_ 9227–9233 (2024). 

- [197] Qu, M., Wang, Y. & Pham, D. T. Robotic disassembly task training and skill transfer using reinforcement learning. _IEEE Transactions on Industrial Informatics_ **19** , 10934–10943 (2023). 

- [198] Serrano-Munoz, A., Arana-Arexolaleiba, N., Chrysostomou, D. & Bøgh, S. Learning and generalising object extraction skill for contact-rich disassembly tasks: an introductory study. _The International Journal of Advanced Manufacturing Technology_ **124** , 3171–3183 (2023). 

- [199] Ren, Q., Zhu, W., Feng, Z. & Liang, W. Learning-based force control of a surgical robot for tool-soft tissue interaction. _IEEE Robotics and Automation Letters_ **6** , 6345–6352 (2021). URL http://dx.doi.org/10.1109/lra.2021.3093018. 

- [200] Straiˇzys, A., Burke, M. & Ramamoorthy, S. Surfing on an uncertain edge: Precision cutting of soft tissue using torque-based medium classification. _2020 IEEE International Conference on Robotics and Automation (ICRA)_ 4623–4629 (2020). 

73 

- [201] Jiang, J., Huang, Z., Bi, Z., Ma, X. & Yu, G. State-of-the-art control strategies for robotic pih assembly. _Robotics and Computer-Integrated Manufacturing_ **65** , 101894 (2020). 

- [202] Li, J., Pang, D., Zheng, Y., Guan, X. & Le, X. A flexible manufacturing assembly system with deep reinforcement learning. _Control Engineering Practice_ **118** , 104957 (2022). 

- [203] Luo, J. _et al._ Robust multi-modal policies for industrial assembly via reinforcement learning and demonstrations: A large-scale study. _arXiv preprint arXiv:2103.11512_ (2021). 

- [204] Spector, O. & Di Castro, D. Insertionnet-a scalable solution for insertion. _IEEE Robotics and Automation Letters_ **6** , 5509–5516 (2021). 

- [205] Levine, S. & Abbeel, P. Learning neural network policies with guided policy search under unknown dynamics. _Advances in neural information processing systems_ **27** (2014). 

- [206] Beltran-Hernandez, C. C., Petit, D., Ramirez-Alpizar, I. G. & Harada, K. Variable compliance control for robotic peg-in-hole assembly: A deep-reinforcementlearning approach. _Applied Sciences_ **10** , 6923 (2020). 

- [207] Spector, O. & Zacksenhouse, M. Learning contact-rich assembly skills using residual admittance policy. _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ 6023–6030 (2021). 

- [208] Beltran-Hernandez, C. C. _et al._ Learning force control for contact-rich manipulation tasks with rigid position-controlled robots. _IEEE Robotics and Automation Letters_ **5** , 5709–5716 (2020). 

- [209] Hou, Z., Li, Z., Hsu, C., Zhang, K. & Xu, J. Fuzzy logic-driven variable timescale prediction-based reinforcement learning for robotic multiple peg-in-hole assembly. _IEEE Transactions on Automation Science and Engineering_ **19** , 218– 229 (2020). 

- [210] Li, X., Xiao, J., Zhao, W., Liu, H. & Wang, G. Multiple peg-in-hole compliant assembly based on a learning-accelerated deep deterministic policy gradient strategy. _Industrial Robot: the international journal of robotics research and application_ **49** , 54–64 (2022). 

- [211] Aburub, M., Beltran-Hernandez, C. C., Kamijo, T. & Hamaya, M. Learning diffusion policies from demonstrations for compliant contact-rich manipulation. _arXiv preprint arXiv:2410.19235_ (2024). 

- [212] Li, X., Shang, W., Rao, W. & Cong, S. Hierarchical learning based on visualhaptic perception for robotic variable impedance control. _IEEE Transactions_ 

74 

_on Industrial Electronics_ (2025). 

- [213] Luo, J., Solowjow, E., Wen, C., Ojea, J. A. & Agogino, A. M. Deep reinforcement learning for robotic assembly of mixed deformable and rigid objects. _2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ 2062–2069 (2018). 

- [214] Kang, J. H., Joshi, S., Huang, R. & Gupta, S. K. Robotic compliant object prying using diffusion policy guided by vision and force observations. _IEEE Robotics and Automation Letters_ (2025). 

- [215] Huo, Y., Li, P., Chen, D., Liu, Y.-H. & Li, X. Model-free adaptive impedance control for autonomous robotic sanding. _IEEE Transactions on Automation Science and Engineering_ **19** , 3601–3611 (2021). 

- [216] Zheng, Z. _et al._ Admittance control for robot polishing force tracking based on reinforcement learning. _International Conference on Intelligent Robotics and Applications_ 335–345 (2023). 

- [217] Mart´ın-Mart´ın, R. _et al._ Variable impedance control in end-effector space: An action space for reinforcement learning in contact-rich tasks. _2019 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ 1010–1017 (2019). 

- [218] Solak, G. & Ajoudani, A. Online learning for vibration suppression in physical robot interaction using power tools. _arXiv preprint arXiv:2508.03559_ (2025). 

- [219] Yu, X., Liu, S., Zhang, S., He, W. & Huang, H. Adaptive neural network force tracking control of flexible joint robot with an uncertain environment. _IEEE Transactions on Industrial Electronics_ **71** , 5941–5949 (2023). 

- [220] Zhu, J. _et al._ Challenges and outlook in robotic manipulation of deformable objects. _IEEE Robotics & Automation Magazine_ **29** , 67–77 (2022). 

- [221] Wang, X. _et al._ Guarding force: Safety-critical compliant control for robotenvironment interaction. _arXiv preprint arXiv:2405.04859_ (2024). 

- [222] Li, Z. _et al._ Learning variable impedance control for robotic massage with deep reinforcement learning: A novel learning framework. _IEEE Systems, Man, and Cybernetics Magazine_ **10** , 17–27 (2024). 

- [223] Huang, B., Gong, Y., Yang, Z., Ren, T. & Figueredo, L. Contact-Safe Reinforcement Learning with ProMP Reparameterization and Energy Awareness (2025). URL http://arxiv.org/abs/2511.13459. ArXiv:2511.13459 [cs] version: 1. 

- [224] Peng, G., Chen, C. P. & Yang, C. Neural networks enhanced optimal admittance control of robot–environment interaction using reinforcement learning. _IEEE_ 

75 

_Transactions on Neural Networks and Learning Systems_ **33** , 4551–4561 (2021). 

- [225] Wang, L., Zhao, J., Du, Y., Adelson, E. H. & Tedrake, R. Poco: Policy composition from and for heterogeneous robot learning. _arXiv preprint arXiv:2402.02511_ (2024). 

- [226] Wirnshofer, F., Schmitt, P. S., von Wichert, G. & Burgard, W. Controlling contact-rich manipulation under partial observability. _Robotics: Science and Systems_ (2020). 

- [227] Kim, M., Niekum, S. & Deshpande, A. D. Scape: Learning stiffness control from augmented position control experiences. _Conference on Robot Learning_ 1512–1521 (2022). 

- [228] Zhang, X. _et al._ Efficient sim-to-real transfer of contact-rich manipulation skills with online admittance residual learning. _Conference on Robot Learning_ 1621– 1639 (2023). 

- [229] De Risi, P., Amadio, F., Garofalo, G., Ficuciello, F. & Falco, P. Variable impedance control combining reinforcement learning and gaussian process regression. _2024 IEEE-RAS 23rd International Conference on Humanoid Robots (Humanoids)_ 343–350 (2024). 

- [230] Ulmer, M., Aljalbout, E., Schwarz, S. & Haddadin, S. Learning robotic manipulation skills using an adaptive force-impedance action space. _arXiv preprint arXiv:2110.09904_ (2021). 

- [231] Abbatematteo, B. _et al._ Composable interaction primitives: A structured policy class for efficiently learning sustained-contact manipulation skills. _2024 IEEE International Conference on Robotics and Automation (ICRA)_ 7522–7529 (2024). 

- [232] Xing, X., Burdet, E., Si, W., Yang, C. & Li, Y. Impedance learning for humanguided robots in contact with unknown environments. _IEEE Transactions on Robotics_ **39** , 3705–3721 (2023). 

- [233] Pan, Y., Li, Z., Shi, T. & Wen, C. Composite learning variable impedance robot control with stability and passivity guarantees. _IEEE Robotics and Automation Letters_ **9** , 119–126 (2023). 

- [234] Chen, B. _et al._ Context-aware safe reinforcement learning for non-stationary environments. _2021 IEEE International Conference on Robotics and Automation (ICRA)_ 10689–10695 (2021). URL http://dx.doi.org/10.1109/icra48506.2021. 9561593. 

76 

- [235] Xiao, M., Zhang, T., Zou, Y., Chen, S. & Wu, W. Research on robot massage force control based on residual reinforcement learning. _IEEE Access_ **12** , 18270– 18279 (2023). 

- [236] Bartneck, C., Kuli´c, D., Croft, E. & Zoghbi, S. Measurement instruments for the anthropomorphism, animacy, likeability, perceived intelligence, and perceived safety of robots. _International journal of social robotics_ **1** , 71–81 (2009). 

- [237] Zhu, H. _et al._ Should we learn contact-rich manipulation policies from samplingbased planners? _IEEE Robotics and Automation Letters_ **10** , 6248–6255 (2025). URL http://dx.doi.org/10.1109/lra.2025.3564701. 

- [238] Chen, B. _et al._ Diffusion forcing: Next-token prediction meets full-sequence diffusion. _Advances in Neural Information Processing Systems_ **37** , 24081–24125 (2024). 

- [239] G¨unster, J., Liu, P., Peters, J. & Tateo, D. Handling long-term safety and uncertainty in safe reinforcement learning. _arXiv preprint arXiv:2409.12045_ (2024). 

- [240] Thananjeyan, B. _et al._ Safety augmented value estimation from demonstrations (saved): Safe deep model-based rl for sparse cost robotic tasks. _IEEE Robotics and Automation Letters_ **5** , 3612–3619 (2020). URL http://dx.doi.org/10.1109/ lra.2020.2976272. 

- [241] Gu, S. _et al._ A human-centered safe robot reinforcement learning framework with interactive behaviors. _Frontiers in Neurorobotics_ **17** , 1280341 (2023). 

- [242] Zhang, H., Solak, G. & Ajoudani, A. Bresa: Bio-inspired reflexive safe reinforcement learning for contact-rich robotic tasks. _arXiv preprint arXiv:2503.21989_ (2025). 

- [243] Lancaster, P., Hansen, N., Rajeswaran, A. & Kumar, V. Modem-v2: Visuomotor world models for real-world robot manipulation. _2024 IEEE International Conference on Robotics and Automation (ICRA)_ 7530–7537 (2024). 

- [244] Mayr, M. _Learning with skill-based robot systems: Combining planning & knowledge representation with reinforcement learning_ (Lund University, 2024). 

- [245] Hou, Z., Fei, J., Deng, Y. & Xu, J. Data-efficient hierarchical reinforcement learning for robotic assembly control applications. _IEEE Transactions on Industrial Electronics_ **68** , 11565–11575 (2020). 

- [246] Cramer, E., J¨aschke, L. & Trimpe, S. Cheq-ing the box: Safe variable impedance learning for robotic polishing. _arXiv preprint arXiv:2501.07985_ (2025). 

77 

- [247] Okada, M., Komatsu, M. & Taniguchi, T. A contact model based on denoising diffusion to learn variable impedance control for contact-rich manipulation. _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ 7286–7293 (2024). 

- [248] Jadav, S. & Palanthandalam-Madapusi, H. J. Configuration and force-field aware variable impedance control with faster re-learning. _Journal of Intelligent ; Robotic Systems_ **110** (2023). URL http://dx.doi.org/10.1007/ s10846-023-02022-x. 

- [249] Yang, Q., D¨urr, A., Topp, E. A., Stork, J. A. & Stoyanov, T. Learning impedance actions for safe reinforcement learning in contact-rich tasks. _NeurIPS 2021 Workshop on Deployable Decision Making in Embodied Systems (DDM),(Online conference), Sydney, Australia, December 6-14, 2021_ (2021). 

- [250] Ji, Z. _et al._ Deep reinforcement learning on variable stiffness compliant control for programming-free robotic assembly in smart manufacturing. _International Journal of Production Research_ **62** , 7073–7095 (2024). URL http://dx.doi.org/ 10.1080/00207543.2024.2318488. 

- [251] Feng, X., Shi, T., Li, W., Lu, P. & Pan, Y. Reinforcement learning-based impedance learning for robot admittance control in industrial assembly. _2022 International Conference on Advanced Robotics and Mechatronics (ICARM)_ 1092–1097 (2022). URL http://dx.doi.org/10.1109/icarm54641.2022.9959152. 

- [252] Anand, A. S., Hagen Myrestrand, M. & Gravdahl, J. T. Evaluation of variable impedance- and hybrid force/motioncontrollers for learning force tracking skills. _2022 IEEE/SICE International Symposium on System Integration (SII)_ 83–89 (2022). URL http://dx.doi.org/10.1109/sii52469.2022.9708826. 

- [253] Zhang, W., Ott, L., Tognon, M. & Siegwart, R. Learning variable impedance control for aerial sliding on uneven heterogeneous surfaces by proprioceptive and tactile sensing. _IEEE Robotics and Automation Letters_ **7** , 11275–11282 (2022). URL http://dx.doi.org/10.1109/lra.2022.3194315. 

- [254] Anand, A. S., Kaushik, R., Gravdahl, J. T. & Abu-Dakka, F. J. Data-efficient reinforcement learning for variable impedance control. _IEEE Access_ **12** , 15631– 15641 (2024). URL http://dx.doi.org/10.1109/access.2024.3355311. 

- [255] Liu, G., Yao, B., Xu, W. & Liu, X. Optimizing non-diagonal stiffness matrix of compliance control for robotic assembly using deep reinforcement learning. _Journal of Physics: Conference Series_ **2402** , 012013 (2022). URL http://dx. doi.org/10.1088/1742-6596/2402/1/012013. 

- [256] Zanella, R., Palli, G., Stramigioli, S. & Califano, F. Learning passive policies with virtual energy tanks in robotics. _IET Control Theory & Applications_ **18** , 541–550 (2024). 

78 

- [257] Yao, Z., Xu, F., Jiang, G.-P. & Yao, J. Data-driven control of hydraulic manipulators by reinforcement learning. _IEEE/ASME Transactions on Mechatronics_ **29** , 2673–2684 (2024). URL http://dx.doi.org/10.1109/tmech.2023.3336070. 

- [258] Padalkar, A., Quere, G., Raffin, A., Silv´erio, J. & Stulp, F. Guiding real-world reinforcement learning for in-contact manipulation tasks with shared control templates. _Autonomous Robots_ **48** , 12 (2024). 

- [259] Giammarino, A., Gandarias, J. M. & Ajoudani, A. An open tele-impedance framework to generate data for contact-rich tasks in robotic manipulation. _2023 IEEE International Conference on Advanced Robotics and Its Social Impacts (ARSO)_ 140–146 (2023). URL http://dx.doi.org/10.1109/arso56563.2023. 10187436. 

- [260] Zhu, C., Yu, T. & Chang, Q. Task-oriented safety field for robot control in human-robot collaborative assembly based on residual learning. _Expert Systems with Applications_ **238** , 121946 (2024). 

- [261] Roveda, L., Testa, A., Shahid, A. A., Braghin, F. & Piga, D. Q-learningbased model predictive variable impedance control for physical human-robot collaboration. _Artificial Intelligence_ **312** , 103771 (2022). 

- [262] Zang, Y. _et al._ Safe peg-in-hole automatic assembly using virtual guiding force: A deep reinforcement learning solution. _Robotics and Autonomous Systems_ **185** , 104894 (2025). 

- [263] Yan, C., Wu, J. & Zhu, Q. Learning-based contact status recognition for peg-inhole assembly. _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ 6003–6009 (2021). 

- [264] Zhang, X., Tomizuka, M. & Li, H. Bridging the sim-to-real gap with dynamic compliance tuning for industrial insertion. _2024 IEEE International Conference on Robotics and Automation (ICRA)_ 4356–4363 (2024). URL http://dx.doi. org/10.1109/icra57147.2024.10610707. 

- [265] Beltran-Hernandez, C. C. _Reinforcement Learning for Contact-Rich Assembly_ . Ph.D. thesis, The University of Osaka (2022). 

- [266] Zhan, S. _et al._ State-wise safe reinforcement learning with pixel observations. _6th Annual Learning for Dynamics & Control Conference_ 1187–1201 (2024). 

- [267] Li, Y. & Xu, D. Skill learning for robotic insertion based on one-shot demonstration and reinforcement learning. _International Journal of Automation and Computing_ **18** , 457–467 (2021). 

- [268] Wang, C. _et al._ Cognitive manipulation: Semi-supervised visual representation and classroom-to-real reinforcement learning for assembly in semi-structured 

79 

environments. _arXiv preprint arXiv:2406.00364_ (2024). 

- [269] Shi, Y. _et al._ Combining learning from demonstration with learning by exploration to facilitate contact-rich tasks. _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ 1062–1069 (2021). 

- [270] Kyaw, A. H. _et al._ Text to Robotic Assembly of Multi Component Objects using 3D Generative AI and Vision Language Models (2025). URL http://arxiv.org/ abs/2511.02162. ArXiv:2511.02162 [cs]. 

- [271] Ni, M. _et al._ Don’t let your robot be harmful: Responsible robotic manipulation via safety-as-policy. _arXiv preprint arXiv:2411.18289_ (2024). 

- [272] Yuan, W., Dong, S. & Adelson, E. H. Gelsight: High-resolution robot tactile sensors for estimating geometry and force. _Sensors_ **17** , 2762 (2017). 

- [273] Wang, S., She, Y., Romero, B. & Adelson, E. Gelsight wedge: Measuring high-resolution 3d contact geometry with a compact robot finger. _2021 IEEE International Conference on Robotics and Automation (ICRA)_ 6468–6475 (2021). 

- [274] Huang, B., Wang, Y., Yang, X., Luo, Y. & Li, Y. 3d-vitac: Learning fine-grained manipulation with visuo-tactile sensing. _arXiv preprint arXiv:2410.24091_ (2024). 

- [275] Jiang, J., Zhang, X., Gomes, D. F., Do, T.-T. & Luo, S. Rotipbot: Robotic handling of thin and flexible objects using rotatable tactile sensors. _IEEE Transactions on Robotics_ **41** , 3684–3702 (2025). 

- [276] Sun, H., Kuchenbecker, K. J. & Martius, G. A soft thumb-sized vision-based sensor with accurate all-round force perception. _Nature Machine Intelligence_ **4** , 135–145 (2022). 

- [277] Do, W. K. & Kennedy, M. Densetact: Optical tactile sensor for dense shape reconstruction. _2022 International Conference on Robotics and Automation (ICRA)_ 6188–6194 (2022). 

- [278] Zhao, Z. _et al._ Embedding high-resolution touch across robotic hands enables adaptive human-like grasping. _Nature Machine Intelligence_ **7** , 889–900 (2025). 

- [279] Bhirangi, R. _et al._ All the feels: A dexterous hand with large-area tactile sensing. _IEEE Robotics and Automation Letters_ **8** , 8311–8318 (2023). 

- [280] Suresh, S. _et al._ Neuralfeels with neural fields: Visuotactile perception for inhand manipulation. _Science Robotics_ **9** , eadl0628 (2024). 

- [281] Zhou, Y., Zhou, P., Wang, S. & She, Y. In-hand singulation and scooping manipulation with a 5 dof tactile gripper. _2024 IEEE/RSJ International Conference_ 

80 

_on Intelligent Robots and Systems (IROS)_ 5238–5243 (2024). 

- [282] Huang, S. H. _et al._ Learning gentle object manipulation with curiosity-driven deep reinforcement learning. _arXiv preprint arXiv:1903.08542_ (2019). 

- [283] Zhu, X., Huang, B. & Li, Y. Touch in the wild: Learning fine-grained manipulation with a portable visuo-tactile gripper. _arXiv preprint arXiv:2507.15062_ (2025). 

- [284] Karacan, K., Grover, D., Sadeghian, H., Wu, F. & Haddadin, S. Tactile exploration using unified force-impedance control. _IFAC-PapersOnLine_ **56** , 5015–5020 (2023). 

- [285] Karacan, K., Zhang, A., Sadeghian, H., Wu, F. & Haddadin, S. Visuo-tactile exploration of unknown rigid 3d curvatures by vision-augmented unified forceimpedance control. _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ 2243–2250 (2024). 

- [286] Bilaloglu, C., L¨ow, T. & Calinon, S. Tactile ergodic coverage on curved surfaces. _IEEE Transactions on Robotics_ (2025). 

- [287] Zhang, K. _et al._ Vibecheck: Using active acoustic tactile sensing for contact-rich manipulation. _arXiv preprint arXiv:2504.15535_ (2025). 

- [288] Todorov, E., Erez, T. & Tassa, Y. Mujoco: A physics engine for model-based control. _2012 IEEE/RSJ international conference on intelligent robots and systems_ 5026–5033 (2012). 

- [289] Zakka, K. _et al._ Mujoco playground. _arXiv preprint arXiv:2502.08844_ (2025). 

- [290] Coumans, E. & Bai, Y. Pybullet, a python module for physics simulation for games, robotics and machine learning.(2016). _URL http://pybullet. org_ (2016). 

- [291] Makoviychuk, V. _et al._ Isaac gym: High performance gpu-based physics simulation for robot learning (2021). 

- [292] Mittal, M. _et al._ Isaac lab: A gpu-accelerated simulation framework for multimodal robot learning. _arXiv preprint arXiv:2511.04831_ (2025). URL https: //arxiv.org/abs/2511.04831. 

- [293] Shi, Y. _et al._ A sim-to-real learning-based framework for contact-rich assembly by utilizing cyclegan and force control. _IEEE Transactions on Cognitive and Developmental Systems_ **15** , 2144–2155 (2023). URL http://dx.doi.org/10.1109/ tcds.2023.3237734. 

- [294] Lin, Z., Wang, C., Wu, S. & Xie, L. Multimodal task attention residual reinforcement learning: Advancing robotic assembly in unstructured environment. _IEEE Robotics and Automation Letters_ **10** , 3900–3907 (2025). URL 

81 

http://dx.doi.org/10.1109/lra.2025.3547647. 

- [295] Shi, Y. _et al._ Proactive action visual residual reinforcement learning for contactrich tasks using a torque-controlled robot. _2021 IEEE International Conference on Robotics and Automation (ICRA)_ 765–771 (2021). URL http://dx.doi.org/ 10.1109/icra48506.2021.9561162. 

- [296] Mower, C. _et al._ Ros-pybullet interface: A framework for reliable contact simulation and human-robot interaction. _Conference on robot learning_ 1411–1423 (2023). 

- [297] Luo, C. _et al._ Multi-modal autonomous ultrasound scanning for efficient human– machine fusion interaction. _IEEE Transactions on Automation Science and Engineering_ **22** , 4712–4723 (2024). 

- [298] Liu, Q. _et al._ Knowledge-guided robot learning on compliance control for robotic assembly task with predictive model. _Expert Systems with Applications_ **234** , 121037 (2023). 

- [299] Berrocal, E., Sierra, B. & Herrero, H. Evaluating pybullet and isaac sim in the scope of robotics and reinforcement learning. _2024 7th Iberian Robotics Conference (ROBOT)_ 1–6 (2024). 

- [300] Authors, G. Genesis: A generative and universal physics engine for robotics and beyond (2024). URL https://github.com/Genesis-Embodied-AI/Genesis. 

- [301] NVIDIA, D. Isaac Sim (2022). URL https://developer.nvidia.com/isaac/sim. 

- [302] Mittal, M. _et al._ Orbit: A unified simulation framework for interactive robot learning environments. _IEEE Robotics and Automation Letters_ **8** , 3740–3747 (2023). 

- [303] Narang, Y. _et al._ Factory: Fast contact for robotic assembly. _arXiv preprint arXiv:2205.03532_ (2022). 

- [304] Yu, M. _et al._ Roboassembly: Learning generalizable furniture assembly policy in a novel multi-robot contact-rich simulation environment. _arXiv preprint arXiv:2112.10143_ (2021). 

- [305] Tedrake, R. _et al._ Drake: A planning, control, and analysis toolbox for nonlinear dynamical systems (2014). 

- [306] Nasiriany, S. _et al._ Robocasa: Large-scale simulation of everyday tasks for generalist robots. _RSS 2024 Workshop: Data Generation for Robotics_ (2024). 

- [307] Zhu, Y. _et al._ robosuite: A modular simulation framework and benchmark for robot learning. _arXiv preprint arXiv:2009.12293_ (2020). 

82 

- [308] Mu, T. _et al._ Maniskill: Generalizable manipulation skill benchmark with largescale demonstrations. _Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)_ (2021). 

- [309] Gu, J. _et al._ Maniskill2: A unified benchmark for generalizable manipulation skills. _The Eleventh International Conference on Learning Representations_ (2023). 

- [310] Liu, P. _et al._ A retrospective on the robot air hockey challenge: Benchmarking robust, reliable, and safe learning techniques for real-world robotics. _Advances in Neural Information Processing Systems_ **37** , 9690–9726 (2024). 

- [311] Yu, T. _et al._ Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning. _Conference on robot learning_ 1094–1100 (2020). 

- [312] Brockman, G. _et al._ Openai gym. _arXiv preprint arXiv:1606.01540_ (2016). 

- [313] James, S., Ma, Z., Arrojo, D. R. & Davison, A. J. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ **5** , 3019–3026 (2020). 

- [314] Long, X. _et al._ A survey: Learning embodied intelligence from physical simulators and world models. _arXiv preprint arXiv:2507.00917_ (2025). 

- [315] Xu, J., Lin, Y., Zhou, H. & Min, H. Generating manipulation sequences using reinforcement learning and behavior trees for peg-in-hole task. _2022 IEEE International Conference on Systems, Man, and Cybernetics (SMC)_ 2715–2720 (2022). URL http://dx.doi.org/10.1109/smc53654.2022.9945269. 

- [316] Wang, Y., Beltran-Hernandez, C. C., Wan, W. & Harada, K. Hybrid trajectory and force learning of complex assembly tasks: A combined learning framework. _IEEE Access_ **9** , 60175–60186 (2021). 

- [317] Yang, Q., Stork, J. A. & Stoyanov, T. Null space based efficient reinforcement learning with hierarchical safety constraints. _2021 European Conference on Mobile Robots (ECMR)_ 1–6 (2021). 

- [318] Gabrielli, G. & Secchi, C. An actor-critic strategy for a safe and efficient human robot collaboration. _2021 20th International Conference on Advanced Robotics (ICAR)_ 919–926 (2021). URL http://dx.doi.org/10.1109/icar53236. 2021.9659462. 

- [319] Mayr, M., Ahmad, F., Chatzilygeroudis, K., Nardi, L. & Krueger, V. Combining planning, reasoning and reinforcement learning to solve industrial robot tasks. _arXiv preprint arXiv:2212.03570_ (2022). 

83 

- [320] Erickson, Z., Gangaram, V., Kapusta, A., Liu, C. K. & Kemp, C. C. Assistive gym: A physics simulation framework for assistive robotics. _2020 IEEE International Conference on Robotics and Automation (ICRA)_ 10169–10176 (2020). URL http://dx.doi.org/10.1109/icra40945.2020.9197411. 

- [321] Kiemel, J. C. & Kroger, T. Learning collision-free and torque-limited robot trajectories based on alternative safe behaviors. _2022 IEEE-RAS 21st International Conference on Humanoid Robots (Humanoids)_ (2022). URL http: //dx.doi.org/10.1109/humanoids53995.2022.10000077. 

- [322] Yuan, C. _et al._ Sim-to-real transfer of robotic assembly with visual inputs using cyclegan and force control. _2022 IEEE International Conference on Robotics and Biomimetics (ROBIO)_ 1426–1432 (2022). URL http://dx.doi.org/10.1109/ robio55434.2022.10011878. 

- [323] Palenicek, D. _et al._ Learning tactile insertion in the real world. _arXiv preprint arXiv:2405.00383_ (2024). 

- [324] Ranjbar, A., Vien, N. A., Ziesche, H., Boedecker, J. & Neumann, G. Residual feedback learning for contact-rich manipulation tasks with uncertainty. _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ 2383–2390 (2021). URL http://dx.doi.org/10.1109/iros51168.2021.9636176. 

- [325] Soni, R. _et al._ End-to-end reinforcement learning for torque based variable height hopping. _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ 7531–7538 (2023). 

- [326] Mestres, P., Marzabal, A. & Cort´es, J. Anytime safe reinforcement learning. _arXiv preprint arXiv:2504.16417_ (2025). 

- [327] Choi, S. _et al._ Diverse policy learning via random obstacle deployment for zeroshot adaptation. _IEEE Robotics and Automation Letters_ **10** , 2510–2517 (2025). URL http://dx.doi.org/10.1109/lra.2025.3532162. 

- [328] Chane-Sane, E. _et al._ Cat: Constraints as terminations for legged locomotion reinforcement learning. _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ 13303–13310 (2024). URL http://dx.doi.org/10. 1109/iros58592.2024.10802334. 

- [329] Rozzi, F., Roveda, L. & Haninger, K. Combining sampling- and gradient-based planning for contact-rich manipulation. _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ 9901–9907 (2024). URL http://dx.doi.org/10.1109/iros58592.2024.10802369. 

- [330] Cen, Z., Yao, Y., Liu, Z. & Zhao, D. Feasibility consistent representation learning for safe reinforcement learning. _arXiv preprint arXiv:2405.11718_ (2024). 

84 

- [331] Zhou, Z., Xie, X., Song, J., Shu, Z. & Ma, L. Gensafe: A generalizable safety enhancer for safe reinforcement learning algorithms based on reduced order markov decision process model. _IEEE Transactions on Neural Networks and Learning Systems_ **36** , 10678–10692 (2025). URL http://dx.doi.org/10.1109/tnnls.2024. 3496492. 

- [332] Fan, Y. _et al._ Learning robust skills for tightly coordinated arms in contactrich tasks. _IEEE Robotics and Automation Letters_ **9** , 2973–2980 (2024). URL http://dx.doi.org/10.1109/lra.2024.3359542. 

- [333] Kovaˇc, L. & Farkaˇs, I. _Safe Reinforcement Learning in a Simulated Robotic Arm_ , 585–589 (Springer Nature Switzerland, 2023). URL http://dx.doi.org/10. 1007/978-3-031-44207-0 ~~5~~ 3. 

- [334] Xiang, G., Li, S., Shuang, F., Gao, F. & Yuan, X. Sc-airl: Share-critic in adversarial inverse reinforcement learning for long-horizon task. _IEEE Robotics and Automation Letters_ **9** , 3179–3186 (2024). URL http://dx.doi.org/10.1109/lra. 2024.3366023. 

- [335] Kim, M., Han, J., Kim, J. & Kim, B. Pre-and post-contact policy decomposition for non-prehensile manipulation with zero-shot sim-to-real transfer. _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ (2023). URL http://dx.doi.org/10.1109/iros55552.2023.10341657. 

- [336] Langaa, J. & Sloth, C. Expert initialized reinforcement learning with application to robotic assembly. _2022 IEEE 18th International Conference on Automation Science and Engineering (CASE)_ 1405–1410 (2022). URL http://dx.doi.org/10. 1109/case49997.2022.9926540. 

- [337] Lee, A. X. _et al._ Beyond pick-and-place: Tackling robotic stacking of diverse shapes. _Conference on Robot Learning_ 1089–1131 (2022). 

- [338] Zhang, X., Sun, L., Kuang, Z. & Tomizuka, M. Learning variable impedance control via inverse reinforcement learning for force-related tasks. _IEEE Robotics and Automation Letters_ **6** , 2225–2232 (2021). 

- [339] Kuutti, S., Fallah, S. & Bowden, R. Training adversarial agents to exploit weaknesses in deep control policies. _2020 IEEE International Conference on Robotics and Automation (ICRA)_ 108–114 (2020). URL http://dx.doi.org/10. 1109/icra40945.2020.9197351. 

- [340] As, Y. _et al._ Actsafe: Active exploration with safety constraints for reinforcement learning. _arXiv preprint arXiv:2410.09486_ (2024). 

- [341] He, T. _et al._ Agile but safe: Learning collision-free high-speed legged locomotion. _Robotics: Science and Systems XX_ (2024). URL http://dx.doi.org/10.15607/ rss.2024.xx.059. 

85 

- [342] Tang, B. _et al._ Industreal: Transferring contact-rich assembly tasks from simulation to reality. _Robotics: Science and Systems XIX_ (2023). URL http: //dx.doi.org/10.15607/rss.2023.xix.039. 

- [343] Elguea-Aguinaco, I. _et al._ Goal-conditioned reinforcement learning within a human-robot disassembly environment. _Applied Sciences_ **12** , 11610 (2022). URL http://dx.doi.org/10.3390/app122211610. 

- [344] Cho, Y., Han, J., Cho, Y. & Kim, B. Corn: Contact-based object representation for nonprehensile manipulation of general unseen objects. _arXiv preprint arXiv:2403.10760_ (2024). 

- [345] Hamaya, M. _et al._ Learning robotic assembly tasks with lower dimensional systems by leveraging physical softness and environmental constraints. _2020 IEEE International Conference on Robotics and Automation (ICRA)_ 7747–7753 (2020). 

- [346] Mguni, D. _et al._ Desta: A framework for safe reinforcement learning with markov games of intervention. _arXiv preprint arXiv:2110.14468_ (2021). 

- [347] Lee, M. A. _et al._ Making sense of vision and touch: Learning multimodal representations for contact-rich tasks. _IEEE Transactions on Robotics_ **36** , 582–596 (2020). 

- [348] Ray, A., Achiam, J. & Amodei, D. Benchmarking safe exploration in deep reinforcement learning. _arXiv preprint arXiv:1910.01708_ (2019). 

- [349] Gu, S. _et al._ Enhancing efficiency of safe reinforcement learning via sample manipulation. _Advances in Neural Information Processing Systems_ **37** , 17247– 17285 (2024). 

- [350] Zhao, Z., Haldar, S., Cui, J., Pinto, L. & Bhirangi, R. Touch begins where vision ends: Generalizable policies for contact-rich manipulation. _arXiv preprint arXiv:2506.13762_ (2025). 

- [351] Eimer, T., Lindauer, M. & Raileanu, R. Hyperparameters in reinforcement learning and how to tune them. _International conference on machine learning_ 9104–9149 (2023). 

- [352] Liu, X. _et al._ Hierarchical reinforcement learning integrating with human knowledge for practical robot skill learning in complex multi-stage manipulation. _IEEE Transactions on Automation Science and Engineering_ **21** , 3852–3862 (2024). URL http://dx.doi.org/10.1109/tase.2023.3288037. 

- [353] Liu, G. _et al._ A task-efficient reinforcement learning task-motion planner for safe human-robot cooperation. _arXiv preprint arXiv:2510.12477_ (2025). 

86 

- [354] Kicki, P. _et al._ Bridging the gap between learning-to-plan, motion primitives and safe reinforcement learning. _arXiv preprint arXiv:2408.14063_ (2024). 

- [355] Krasowski, H., Akella, P., Ames, A. D. & Althoff, M. Safe reinforcement learning with probabilistic guarantees satisfying temporal logic specifications in continuous action spaces. _2023 62nd IEEE Conference on Decision and Control (CDC)_ 4372–4378 (2023). URL http://dx.doi.org/10.1109/cdc49753.2023.10383601. 

- [356] Zhu, X. _et al._ Multi-level reasoning for robotic assembly: From sequence inference to contact selection. _2024 IEEE International Conference on Robotics and Automation (ICRA)_ 816–823 (2024). URL http://dx.doi.org/10.1109/icra57147. 2024.10611259. 

- [357] Tian, Y. _et al._ Assemble them all: Physics-based planning for generalizable assembly by disassembly. _ACM Transactions on Graphics (TOG)_ **41** , 1–11 (2022). 

- [358] Politowicz, A., Mazumder, S. & Liu, B. Safety through permissibility: Shield construction for fast and safe reinforcement learning. _arXiv preprint arXiv:2405.19414_ (2024). 

- [359] Spieker, P., Large, N. L. & Lauer, M. Better safe than sorry: Enhancing arbitration graphs for safe and robust autonomous decision-making. _arXiv preprint arXiv:2411.10170_ (2024). 

- [360] Feng, Z., Luan, H., Goyal, P. & Soh, H. Ltldog: Satisfying temporally-extended symbolic constraints for safe diffusion-based planning. _IEEE Robotics and Automation Letters_ **9** , 8571–8578 (2024). URL http://dx.doi.org/10.1109/lra.2024. 3443501. 

- [361] Macaluso, A., Cote, N. & Chitta, S. Toward automated programming for robotic assembly using chatgpt. _2024 IEEE International Conference on Robotics and Automation (ICRA)_ 17687–17693 (2024). URL http://dx.doi.org/10.1109/ icra57147.2024.10610554. 

- [362] Yin, S. _et al._ Safeagentbench: A benchmark for safe task planning of embodied llm agents. _arXiv preprint arXiv:2412.13178_ (2024). 

- [363] Wi, Y., Van der Merwe, M., Florence, P., Zeng, A. & Fazeli, N. Calamari: Contact-aware and language conditioned spatial action mapping for contact-rich manipulation. _7th Annual Conference on Robot Learning_ (2023). 

- [364] Batool, F. _et al._ Impedancegpt: Vlm-driven impedance control of swarm of mini-drones for intelligent navigation in dynamic environment. _arXiv preprint arXiv:2503.02723_ (2025). 

87 

- [365] Huang, J. _et al._ Tactile-vla: unlocking vision-language-action model’s physical knowledge for tactile generalization. _arXiv preprint arXiv:2507.09160_ (2025). 

- [366] Zhang, C. _et al._ Vtla: Vision-tactile-language-action model with preference learning for insertion manipulation. _arXiv preprint arXiv:2505.09577_ (2025). 

- [367] Yang, S. _et al._ Bitla: A bimanual tactile-language-action model for contactrich robotic manipulation. _Proceedings of the 1st International Workshop on Multi-Sensorial Media and Applications_ 12–17 (2025). 

- [368] Cheng, Z. _et al._ Omnivtla: Vision-tactile-language-action model with semanticaligned tactile sensing. _arXiv preprint arXiv:2508.08706_ (2025). 

- [369] Geiger, N., Asfour, T., Hogan, N. & Lachner, J. Diffusion-based impedance learning for contact-rich manipulation tasks. _arXiv preprint arXiv:2509.19696_ (2025). 

- [370] Wu, Y. _et al._ Tacdiffusion: Force-domain diffusion policy for precise tactile manipulation. _2025 IEEE International Conference on Robotics and Automation (ICRA)_ 11831–11837 (2025). URL http://dx.doi.org/10.1109/icra55743.2025. 11127334. 

- [371] Bogdanovic, M., Khadiv, M. & Righetti, L. Learning variable impedance control for contact sensitive tasks. _IEEE Robotics and Automation Letters_ **5** , 6129–6136 (2020). URL http://dx.doi.org/10.1109/lra.2020.3011379. 

- [372] Michel, Y., Rahal, R., Pacchierotti, C., Giordano, P. R. & Lee, D. Bilateral teleoperation with adaptive impedance control for contact tasks. _IEEE Robotics and Automation Letters_ **6** , 5429–5436 (2021). 

- [373] Liu, P., Bou-Ammar, H., Peters, J. & Tateo, D. Safe reinforcement learning on the constraint manifold: Theory and applications. _IEEE Transactions on Robotics_ (2025). 

- [374] Long, K. _et al._ Neural configuration-space barriers for manipulation planning and control. _arXiv preprint arXiv:2503.04929_ (2025). 

- [375] Zhao, X., Han, S., Tao, B., Yin, Z. & Ding, H. Model-based actor-critic learning of robotic impedance control in complex interactive environment. _IEEE Transactions on Industrial Electronics_ **69** , 13225–13235 (2021). 

- [376] Agnihotri, A., Jain, R., Ramachandran, D. & Singla, S. e-cop: Episodic constrained optimization of policies. _Advances in Neural Information Processing Systems_ **37** , 110909–110934 (2024). 

- [377] Ding, Y. & Lavaei, J. Provably efficient primal-dual reinforcement learning for cmdps with non-stationary objectives and constraints. _Proceedings of the AAAI_ 

88 

_Conference on Artificial Intelligence_ **37** , 7396–7404 (2023). 

- [378] Wang, Y. _et al._ Enforcing hard constraints with soft barriers: Safe reinforcement learning in unknown stochastic environments. _International Conference on Machine Learning_ 36593–36604 (2023). 

- [379] Yu, H., Xu, W. & Zhang, H. Towards safe reinforcement learning with a safety editor policy. _Advances in Neural Information Processing Systems_ **35** , 2608– 2621 (2022). 

- [380] Tan, D. C. _et al._ Safe value functions: Learned critics as hard safety constraints. _2024 IEEE 20th International Conference on Automation Science and Engineering (CASE)_ 2441–2448 (2024). 

- [381] Wilcox, A., Balakrishna, A., Thananjeyan, B., Gonzalez, J. E. & Goldberg, K. Ls3: Latent space safe sets for long-horizon visuomotor control of sparse reward iterative tasks. _Conference on Robot Learning_ 959–969 (2022). 

- [382] Guo, J. _et al._ Don’t trade off safety: Diffusion regularization for constrained offline rl. _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ (2025). 

- [383] Zhang, J., Zhao, L., Papachristodoulou, A. & Umenberger, J. Constrained diffusers for safe planning and control. _arXiv preprint arXiv:2506.12544_ (2025). 

- [384] Spyrakos-Papastavridis, E., Childs, P. R. N. & Dai, J. S. Passivity preservation for variable impedance control of compliant robots. _IEEE/ASME Transactions on Mechatronics_ **25** , 2342–2353 (2020). 

- [385] Gu, Q. _et al._ Safe: Multitask failure detection for vision-language-action models. _arXiv preprint arXiv:2506.09937_ (2025). 

- [386] Lyu, S. & Cheah, C. C. Human–robot interaction control based on a general energy shaping method. _IEEE Transactions on Control Systems Technology_ **28** , 2445–2460 (2020). URL http://dx.doi.org/10.1109/tcst.2019.2949525. 

- [387] Sharkawy, A.-N. & Koustoumpardis, P. N. Human–robot interaction: A review and analysis on variable admittance control, safety, and perspectives. _Machines_ **10** , 591 (2022). URL http://dx.doi.org/10.3390/machines10070591. 

- [388] Hanna, A., Bengtsson, K., G¨otvall, P.-L. & Ekstr¨om, M. Towards safe human robot collaboration–risk assessment of intelligent automation. _2020 25th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA)_ **1** , 424–431 (2020). 

- [389] Team, G. R. _et al._ Evaluating gemini robotics policies in a veo world simulator (2025). URL https://arxiv.org/abs/2512.10675. arXiv:2512.10675. 

89 

|**Refs.**|[59], [106], [107]<br>[108]<br>[94–96]<br>[32]<br>[117]<br>[115]|
|---|---|
|**Data efficiency**<br>**(A6)**|High: preserves RL<br>learning efficiency;<br>model-based safety<br>needs little data<br>Model-based; mod-<br>erate<br>Analytic, not<br>data-driven<br>Moderate<br>Data-dependent<br>Enables safe data<br>collection|
|**Conservatism /**<br>**tunability (A4)**|Conservative<br>under model mis-<br>match; few online<br>knobs<br>Adapts to<br>changing<br>goals/constraints<br>within the horizon<br>Can become con-<br>servative under<br>uncertainty<br>Explicitly risk-<br>tunable, less<br>conservative<br>Depends on train-<br>ing coverage<br>Conservatism set<br>by intervention<br>frequency|
|**Compute place-**<br>**ment & cost**<br>**(A3)**|Heavy offline pre-<br>computation;<br>lightweight online<br>projection<br>Online receding-<br>horizon<br>optimization at<br>each step<br>Lightweight per-<br>step quadratic<br>program<br>Online quadratic<br>program<br>Lightweight online<br>execution after<br>training<br>Lightweight online<br>intervention check|
|**assump-**<br>**(A2)**|es a rea-<br>y accurate<br>for offline<br>ble-set con-<br>on<br>es a pre-<br> (forward)<br>an accurate<br> uncertainty<br>d via ro-<br>daptive<br>based CBF<br> risk param-<br>tion<br>y model-<br>data-driven<br>free; re-<br>a safe<br> policy|
|**Model**<br>**tions **|Requir<br>sonabl<br>model <br>reacha<br>structi<br>Requir<br>dictive <br>model<br>Needs <br>model; <br>handle<br>bust/a<br>CBFs<br>Model-<br>with a <br>eteriza<br>Largel<br>free / <br>policy<br>Model-<br>quires <br>backup|
|**Guarantee type**<br>**(A1)**|Hard (forward-<br>reachability<br>invariance) while<br>precomputed sets<br>remain valid<br>Hard online: fore-<br>casts violations<br>and substitutes<br>safe goal-directed<br>recoveries<br>Hard (forward in-<br>variance) when<br>modeling assump-<br>tions hold<br>Probabilistic /<br>explicitly tunable<br>risk bound<br>Stability-based<br>(explicit Lyapunov<br>constraint)<br>Safe data collec-<br>tion via online<br>intervention|
|**Method family**|RTS (reachability-<br>based safeguard)<br>MPS (model pre-<br>dictive shielding)<br>CBF-QP safety<br>filter<br>Risk-tunable CBF<br>Lyapunov<br>actor–critic (+<br>impedance layer)<br>Advantage-based<br>intervention|


90 

|e give its typical safety<br> sensing and modeling<br>the text of this section.|**Principal limita-**<br>**tion**|Cannot bound<br>interaction<br>force/pressure,<br>blind to unmod-<br>eled/unexpected<br>contact, only as safe<br>as the geometric<br>model<br>Local and non-<br>anticipatory, missing<br>distributed-contact<br>detail<br>Cannot directly<br>bound contact<br>force/pressure,<br>degrades under<br>occlusion, poor<br>lighting, or pose-<br>ii|estmaton error<br>No measurement<br>of force/geometry,<br>can hallucinate or<br>mis-ground, physical<br>safety still rests on<br>low-level controllers<br>Senses only where it<br>touches, no global<br>context, cover-<br>age and durability<br>limited, cannot an-<br>ticipate non-local<br>events<br>Complexity and<br>calibration bur-<br>den, modality<br>dropout/miscalibration<br>can mislead, no<br>bound unless a<br>measuring modality<br>is present|
|---|---|---|---|
|For each modality w<br>rantee character, its<br>odality are given in|**Cost / band-**<br>**width**|Low-<br>dimensional,<br>cheap, high-<br>rate, no contact<br>hardware<br>Cheap sensor,<br>low-dimensional,<br>high control-<br>rate, negligible<br>compute<br>High-<br>bandwidth,<br>heavier percep-<br>tion compute<br>and latency|High inference<br>latency, off the<br>real-time loop,<br>coarse update<br>rate<br>High-resolution<br>data but spa-<br>tially local,<br>medium rate<br>Highest aggre-<br>gate bandwidth<br>and compute,<br>synchronization<br>overhead|
|safe contact-rich learning.<br>only infer, the resulting gua<br>rting references for each m|**Key requirements /**<br>**assumptions**|Accurate kinematic<br>model and calibrated<br>pose, object/obstacle<br>poses observable, good<br>planner<br>Wrist/finger F/T sensor<br>with bias/gravity calibra-<br>tion, torque-controlled or<br>compliant robot<br>Calibrated cameras,<br>adequate lighting,<br>occlusion-free view, pose-<br>estimation or learned<br>perception|grounding to symbolic<br>plan, constraint set /<br>safety filter for verifica-<br>tion<br>Tactile skin / vision-<br>based fingertip at the<br>contact sites, calibration<br>/ representation learning<br>Multiple calibrated sen-<br>sors with temporal/cross-<br>modal alignment, fusion<br>architecture, higher<br>data/engineering burden|
|d policy inputs for<br>tly bound versus <br>e mode. The suppo|**Guarantee**<br>**character**|Configuration-<br>space, model-<br>based reasoning,<br>no contact-force<br>certificate<br>Direct<br>measurement-<br>based bound,<br>supports hard<br>force caps<br>and passiv-<br>ity/stability<br>certificates from<br>the measured<br>wrench<br>spatial risk<br>maps and pre-<br>dicted contact,<br>not a measured-<br>force bound|Semantic-only:<br>specifies and<br>grounds con-<br>straints but<br>cannot itself<br>certify physical<br>safety, a down-<br>stream filter is<br>needed<br>Direct, high-<br>resolution local<br>measurement,<br>inherently local<br>Composite:<br>anticipatory<br>where-to-<br>contact plus<br>measurement-<br>based how-hard<br>bounds from<br>F/T and tactile|
|comparison of sensing an<br>ety quantity it can direc<br>, and its principal failur|**Safety quantity**|Kinematic safety di-<br>rectly: joint/velocity<br>limits, collision dis-<br>tances, geometric<br>invariant sets<br>Interaction wrench<br>directly: con-<br>tact force/torque,<br>impulse,<br>impedance/passivity<br>energy, slip/jamming<br>onset<br>Scene geometry,<br>object/obstacle pose,<br>human proximity|Semantic/task-level<br>intent and con-<br>straints only, no<br>physical quantity<br>Local contact state<br>directly: pressure<br>distribution, shear,<br>contact location, in-<br>cipient slip, bounds<br>per-taxel/contact-<br>patch loads<br>Combined: global<br>geometry, bounded<br>local interaction, and<br>intent in a shared<br>representation|
|**Table 4** Structured cross-modality<br>leverage and then contrast which saf<br>requirements, its cost and bandwidth|**Modality**<br>**Typical safety**<br>**leverage**|Proprioceptive<br>/ kinematic<br>state<br>Contact reasoning<br>from joint con-<br>figurations and<br>end-effector pose,<br>conservative motion<br>generation<br>Force/torque<br>Real-time enforce-<br>ment of force and<br>impedance limits,<br>slip detection, com-<br>pliant correction of<br>model error<br>Vision<br>Contact evaluation,<br>localizing task fea-<br>tures, and supplying<br>global context that<br>force sensors cannot<br>provide|Natural-<br>language<br>instruction<br>Large multimodal<br>models interpret a<br>human’s instruction<br>and then check inter-<br>nal low-level safety<br>Tactile<br>High-resolution con-<br>tact localization,<br>pressure distribution<br>monitoring, and in-<br>cipient slip detection<br>Multimodal<br>fusion<br>Enables high preci-<br>sion under occlusion|


91 

**Table 5** Representative simulation platforms used in learning-based contact-rich robotics, compared in terms of deformable-object support, GPU acceleration, and primary task domains. The table covers general-purpose physics engines, GPU-accelerated robot-learning platforms, and task-specific environments for contact-rich tasks. 

|Simulators|Deformable|GPU|Tasks|References|
|---|---|---|---|---|
|MuJoCo|✓|✗|Manipulation, Locomotion|[288]|
|MuJoCo XLA/MJX|✓|✓|Manipulation, Locomotion|[289]|
|Genesis|✓|✓|Soft-body, Articulated|[300]|
|PyBullet|✓|✗|Manipulation, Grasping|[290]|
|Isaac Gym|✓|✓|RL Training, Manipulation|[291]|
|Isaac Sim|✓|✓|Photorealistic, Digital Twin|[299, 301]|
|Isaac Lab|✓|✓|Robot learning|[292]|
|Orbit|✓|✓|Interactive Robot Learning|[302]|
|Factory|✗|✓|RL, Assembly|[303]|
|RoboAssembly|✗|✗|furniture assembly|[304]|
|Drake|✗|✗|Model-based Control|[305]|


**Table 6** Representative benchmarks commonly used to evaluate learning-based, contact-rich robotic systems. The comparison emphasizes scalability, deformable-object support, GPU acceleration, and core task domains, spanning general manipulation, reinforcement learning, and safety-oriented assessment. 

|Benchmarks|Scalable|Deformable|GPU|Tasks|References|
|---|---|---|---|---|---|
|RoboVerse|✓|✓|✓|Manipulation, RL Benchmarks|[77]|
|RoboCasa|✓|✓|✓|Household Tasks, Manipulation|[306]|
|RoboSuite|✓|✓|✓|Manipulation, RL Benchmarks|[307]|
|ManiSkill|✓|✓|✓|Manipulation, RL Benchmarks|[308, 309]|
|Robot Air Hockey|✓|✗|✓|Air Hockey game|[310]|
|Meta-World|✓|✗|✓|Manipulation, RL Benchmarks|[311]|
|OpenAI Gym|✓|✗|✓|RL Benchmarks, Manipulation|[312]|
|RLBench|✓|✗|✓|Manipulation, RL Benchmarks|[313]|
|Stable Baselines|✓|✗|✓|RL Benchmarks, Manipulation|[90]|
|Gymnasium|✓|✗|✓|RL Benchmarks, Manipulation|[89]|
|Safety Gymnasium|✓|✗|✓|Safety in RL, Manipulation|[48]|
|Robust gymnasium|✓|✗|✓|Safety in RL, Robotics|[78]|
|Safe-Control-Gym|✓|✗|✓|Safety in RL, Control|[46]|


**Table 7** Mapping from foundation-model (VLM/VLA) safety mechanisms to the classical safety principles they instantiate 

|**Foundation-model mechanism**|**Classical safety principle it instantiates**|
|---|---|
|Grounding language and rules into formal<br>constraints|Constraint satisfaction & reachability|
|Semantic scene grounding (affordances,<br>no-touch, fragile regions)|Semantic safety|
|Safety critics, refusal, risk-aware action<br>filtering|Risk- & data-driven safety|
|Low-level shields under a VLA planner<br>(CBF / reachability / MPC)|Stability & set invariance|
|Conservative default caps and compliant<br>references|Physical-interaction safety: force, energy, passivity|
|Human-proximity / speed–separation /<br>PPE rules|Human-centered & standard-driven safety|


92 

|**Limitations**|May command kine-<br>matically infeasible or<br>limit-violating joint<br>configurations, ignores<br>internal actuator and<br>self-collision integrity<br>May overlook excessive<br>end-effector contact<br>pressure at the envi-<br>ronment interface, safe<br>joints do not imply safe<br>interaction<br>Integration complexity<br>and possible inter-<br>loop conflicts, larger<br>modeling burden than<br>either single space<br>Only preemp-<br>tive/asymptotic, no<br>instantaneous hard<br>bound, needs a low-<br>level backup or shield,<br>degrades under dis-<br>tribution shift and<br>high-dimensional state|
|---|---|
|**Compute placement**<br>**& cost**|Online QP/safety filter<br>or compliant controller<br>at the control rate,<br>modest per-step cost<br>Low-level<br>torque/saturation fil-<br>ter or joint-level CBF<br>at the servo rate,<br>lightweight<br>Coupled dual loop<br>controllers, higher<br>integration and coordi-<br>nation overhead<br>Training-time con-<br>strained optimization<br>with lightweight run-<br>time policy/critic<br>evaluation|
|**Assumptions**|Accurate task-space<br>kinematics and an<br>impedance/force<br>controller, known<br>force/region limits, reli-<br>able wrench sensing<br>Accurate robot dy-<br>namics/actuator<br>model, proprioceptive<br>feedback, access to low-<br>level torque control<br>Both a task-space in-<br>teraction model and a<br>joint-space dynamics<br>model, consistent re-<br>dundancy resolution,<br>dual-loop coordination<br>Adequate training cov-<br>erage, a specified cost<br>threshold/labels, state<br>representation, fre-<br>quently a safe backup<br>policy|
|**Guarantee type**|Direct contact-<br>force/region<br>bounding via compli-<br>ance/impedance &<br>passivity, or forward-<br>invariant safe set via<br>CBF/safety filter, can<br>be hard on the EE<br>state when the model<br>holds<br>Intrinsic integrity via<br>joint limits and sat-<br>uration filters plus<br>Lyapunov/passivity<br>Combined: task-space<br>invariance/compliance<br>with joint-limit and<br>Lyapunov guarantees,<br>bounded-error proofs<br>for both force tracking<br>and joint deviation<br>Typically<br>soft/asymptotic, con-<br>straint satisfaction<br>in expectation via<br>CMDP/Lagrangian re-<br>laxation or feasibility<br>value functions / safety<br>critics, preemptive<br>rather than instanta-<br>neous|
|**Enforcement space**<br>**Where safety lives**|Task space<br>Cartesian end-<br>effector motion and<br>contact force/wrench<br>at the physical in-<br>terface, workspace<br>region<br>Joint space<br>Configuration-space<br>quantities, joint<br>angles, velocities,<br>torques, actuator<br>saturation, singu-<br>larity proximity,<br>self-collision<br>Dual-space<br>Both coordinate<br>frames concurrently,<br>EE force/motion and<br>joint limits/torques<br>Policy space<br>Decision-level<br>quantities, CMDP<br>cost/value, expected<br>constraint cost, fea-<br>sibility/safety value,<br>shapes exploration<br>before low-level in-<br>tervention|


93 

