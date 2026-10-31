---
title: "AS2FM: Enabling Statistical Model Checking of ROS 2 Systems for Robust Autonomy"
date: "2025-08-26"
authors: "Christian Henkel; Marco Lampacrescia; Michaela Klauck; Matteo Morelli"
url: https://arxiv.org/abs/2508.18820
pdf: https://arxiv.org/pdf/2508.18820
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2508.18820)** / [論文ページ](https://arxiv.org/abs/2508.18820)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# AS2FM: Enabling Statistical Model Checking of ROS 2 Systems for Robust Autonomy 

Christian Henkel<sup>1</sup><sup>_,_2</sup><sup>_,∗_</sup> , Marco Lampacrescia<sup>1</sup><sup>_,_3</sup> , Michaela Klauck<sup>1</sup><sup>_,_4</sup> , Matteo Morelli<sup>5</sup> 

**_Abstract_ —Designing robotic systems to act autonomously in unforeseen environments is a challenging task. This work presents a novel approach to use formal verification, specifically Statistical Model Checking (SMC), to verify system properties of autonomous robots at design-time. We introduce an extension of the SCXML format, designed to model system components including both Robot Operating System 2 (ROS 2) and Behavior Tree (BT) features. Further, we contribute Autonomous Systems to Formal Models (AS2FM), a tool to translate the full system model into JANI. The use of JANI, a standard format for quantitative model checking, enables verification of system properties with off-the-shelf SMC tools. We demonstrate the practical usability of AS2FM both in terms of applicability to real-world autonomous robotic control systems, and in terms of verification runtime scaling. We provide a case study, where we successfully identify problems in a ROS 2-based robotic manipulation use case that is verifiable in less than one second using consumer hardware. Additionally, we compare to the state of the art and demonstrate that our method is more comprehensive in system feature support, and that the verification runtime scales linearly with the size of the model, instead of exponentially.** 

## I. INTRODUCTION 

Autonomous robotic systems are expected to operate autonomously in unforeseen environments. Designing such systems is challenging for several reasons. Firstly, the required software and hardware components have a high inherent complexity. Secondly, the exact environment in which the robot will operate is not known at design time. However, it is required for the robot to robustly operate in the environment by using the available hardware and software components. Here, _robustness_ means that the robot operates successfully in a variety of environments and under a variety of conditions. 

To handle the complexity of autonomous robotic systems, a skill-based architecture is often used. Each skill is responsible for a specific task, such as moving the robot, detecting objects, or planning a path [1, 2, 3]. Responsible for the coordination of the skills is an architectural layer that we call the _deliberation layer_ [4]. This layer can be implemented using a variety of techniques, such as Behavior 

> 1Bosch Research, Robert Bosch GmbH, Stuttgart, Germany, 2hec2le@bosch.com, 3lam2rng@bosch.com, 4michaela.klauck@de.bosch.com, 5List, CEA, Universite ParisSaclay, France Matteo.MORELLI@cea.fr. 

2 _,_ 3 The first two authors contributed equally to this work. 

> _∗_ Corresponding author. 

The research was funded by the European Union’s Horizon Europe Research & Innovation Program under Grant 101070227 (CONVINCE). 

© 2025 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or reuse of any copyrighted component of this work in other works. 


Fig. 1: Example of two state machines and their translation to a network of Markov Decision Processes (MDPs). **(a)** _M_ 1 sends on the transition from _s_ 1 to _s_ 0 an event _e_ 2 highlighted in red that triggers a transition in _M_ 2. Note that the event _e_ 1 colored in blue is sent without any effect. **(b)** Network of MDPs after translation from the state machines in (a). The additional MDP _Me_ 2 in red is used to model the sending and receiving of events. The actions _ae_ 2 _s_ and _ae_ 2 _r_ colored in purple and green respectively are synchronized between the MDPs. Note that the blue action _a_ 1 is not synchronized to any other action. 

Trees (BTs) [5]. The general architecture and communication of modern robotic systems is often implemented using the Robot Operating System 2 (ROS 2) middleware [6] because it provides a flexible and modular framework for it. 

The use of formal methods, such as model checking, can help to ensure that the robot behaves as expected in all situations. This approach is the core idea of the EU Horizon project CONVINCE [7]. In model checking, a formal model of the system is used to verify that the system satisfies a given temporal logic property [8]. However, traditional model checking, also known as full-state space, or exhaustive, model checking, can not handle the complexity of autonomous robotic systems due to the large state space of these systems. We therefore propose to use _statistical model checking_ [9, 10] to verify properties of autonomous robotic systems. 

This paper presents a novel approach to model and verify temporal logic properties of autonomous robotic systems using statistical model checking. Our tool Autonomous Systems to Formal Models (AS2FM), part of the CONVINCE toolbox for enhancing robust robot deliberation [11], facilitates the translation of complete robot models into a formal model in JANI [12] that can be verified, e.g., using SMC Storm [13]. 

AS2FM is available open source under Apache 2.0 license<sup>1</sup> . To define the complete system, we use State Chart XML (SCXML) to model ROS 2 nodes, the environment and BTPlugins, and the BT-definition of the system _as it is_ to model the deliberation layer. 

Our work includes in particular: 

- Syntax and semantics extending SCXML to model ROS 2 communication interfaces, BT-specific features, timers, and non-deterministic transitions, and 

- A translation algorithm from the event-based synchronization of SCXML to synchronization of transitions in JANI models, implemented together with the rest of the model translation form SCXML to JANI in AS2FM. 

These contributions help to increase the robustness of autonomous robotic systems by enabling the verification of properties at design-time. This is to our knowledge the first approach targeting the verification of complete ROS 2 systems (including communication, timers, and BTs). 

The remainder of this paper is structured as follows. Section II discusses related work. Section III introduces the high-level modeling language used to model robotic systems. Section IV describes the translation of the high-level model to a formal model. Section V presents the model checking evaluation of our approach, while Section VI summarizes findings and ideas for future work. 

## II. RELATED WORK 

Formal verification is a rigorous mathematical approach used to ensure that the designed system adheres to specified properties and requirements. It proves the correctness of algorithms and systems, particularly in critical applications such as software, hardware, and protocols. One of the key techniques in formal verification is Model Checking (MC) [14], which systematically explores the state space of a system’s model to verify whether it satisfies certain properties, typically expressed in temporal logic [15]. It provides a powerful tool for validating complex systems against their specifications, ensuring reliability and safety in system design. Traditionally, full-state space (exhaustive) model checking generates traces to explore the entire reachable state space of the model [8], which is quite resource consuming. This is the reason for a lack of methods and tools to validate complex robotic systems efficiently _as a whole_ , despite the longstanding research interest in Verification and Validation (V&V) of autonomous systems [16]. A solution to that problem is using _Statistical Model Checking (SMC)_ [9, 10]. SMC evaluates the model by only simulating enough traces, until statistical evidence whether the investigated property holds is achieved. This is more scalable than full-state space model checking, and it helps finding corner cases faster compared to classic software testing. However, SMC could miss rare edge-cases due to it’s probabilistic nature. Recent work by the authors extend the well-known probabilistic model checker Storm [17] with SMC for robotic use cases [13]. 

Storm uses, beside others, Markov Decision Processes (MDPs) as input models, which is a well-known concept in the robotics community. MDPs provide a formal framework for modeling decision-making under uncertainty and in dynamic environments [18, 19, 20, 21], making them wellsuited for representing the complex and dynamic nature of robotic use cases and scenarios. 

On the other hand, Timed Automata (TAs) are a formalism for modeling and verifying timed systems [22]. While TAs have been used in modeling real-time systems, their application to autonomous robotic decision-making is limited due to the complexity of modeling explicit time constraints [23, 24, 25]. The tooling for TAs is not as mature yet as the one for MDPs [26]. While TAs are possible in general, their current complexity and the lack of performant tooling make them less practical for modeling complex robotic systems. Therefore, we propose to use MDPs for modeling the environment and the system’s behavior, as they are more suitable for the complexity of robotic systems. 

Previous work has focused on the V&V of robotic systems using MC [27], e.g., by verifying entire programs, including scheduling aspects, formalized as timed automata, by compilation to bytecode and translation to UPPAAL for formal analysis [28]. Other work provides a case study on household robots’ behavior definitions that are verified using NuSMV [29]. A Domain Specific Language (DSL) was introduced for specifying the integration of robotic systems to verify the properties of the system using Fiacre and Tina [22]. Further, an integrated approach between offline MC and online monitoring for robotic systems verifying Signal Temporal Logic (STL) properties [30] has been published. 

Research on an UML-based DSL to describe a robotic system and convert it into a TA is presented in [31]. That work has been continued by introducing a new DSL for representing the environment and verifying the resulting TA using UPPAAL [32]. 

Some work has been done on formal verification in ROS 1 [33, 34, 35, 36, 32], but we are to our knowledge the first explicitly targeting ROS 2. 

There also exists work on verifying BTs [37]. The tool BehaVerify focuses on stateful BTs, which means the BT black board is used to keep information in memory. In that approach the BT is converted to an MDP, that can be verified using nuXmv. Though we think this work is the closest to ours, no explicit model of the environment is provided there, since it is described using the black board, and there is no way to describe a more complex system using only BTs. 

## III. HIGH LEVEL MODELING LANGUAGE 

Robotic systems, especially the ones using ROS 2 and BTs, consist of a number of nodes running in parallel and exchanging information via communication interfaces, i.e., topics, services, and actions in ROS 2, as well as ticks and blackboards in BTs. In the following, we describe how these systems can be modelled. 

1https://github.com/convince-project/as2fm 

We introduce High Level SCXML (HL-SCXML), a custom modeling language building on top of SCXML. It supports ROS 2 communication interfaces and timers, and BT functionalities such as input-output ports, the blackboard, and ticks. Each HL-SCXML file represents one state machine: this is used to represent complete ROS 2 nodes and BT nodes. Additionally, we support reading the definition of the BT in the XML format of the _BehaviorTree.CPP_<sup>2</sup> library, so users must only model the behavior of the leaf nodes explicitly. This enables an accurate representation of the actual robotic control architecture. 

The AS2FM tool translates HL-SCXML to standard SCXML [38], replacing all references to ROS 2 and BT features with SCXML events. We provide an overview of the translations from HL-SCXML to SCXML in the next paragraphs but, for brevity, we omit a detailed description in this paper and refer to our tool’s documentation<sup>3</sup> . Using standard SCXML as intermediate format limits the amount of functionalities we need to consider when generating the formal model of the system. Afterwards, AS2FM converts the standard SCXML model into a network of MDPs, that is the formalism used by JANI, to be formally verified. 

## _A. ROS 2 Interfaces_ 

ROS 2 nodes are modeled using the following interface definitions: 

- _ROS Topics_ are implemented by translating them to SCXML events. The data in events is read from the declared ROS message type. 

- _ROS Services_ are implemented by translating the request and response to separate events, where the data is read from the declared ROS types. 

- _ROS Actions_ are implemented by translating the goal, feedback, and result to separate events. The data is read from the declared ROS types. They can be modeled in a multi-threaded architecture, where the action server uses multiple threads to handle multiple goals concurrently. Each thread is a separate SCXML state machine. 

- _ROS Timers_ are realized by the introduction of a state machine serving as a global clock. This distributes the time information to all state machines that may declare callbacks to be triggered at different rates. 

For a full syntax reference, refer to our documentation.<sup>4</sup> 

## _B. Behavior Tree Runtime_ 

BTs can be modeled using the following concepts: 

- The _Runtime_ interprets the BT.xml<sup>5</sup> file and executes the tree. It is ticked at a configurable rate. Also the behavior of ticking based on the tree return state can be configured. 

2https://github.com/BehaviorTree/BehaviorTree.CPP 

3https://convince-project.github.io/AS2FM/scxml-jani-conversion.html 

4https://convince-project.github.io/AS2FM/howto.html 

> 5https://www.behaviortree.dev/docs/learn-the-basics/xml <u>format/</u> 

- All _BT Nodes_ , including control nodes and leaf nodes, are represented as state machines, using HL-SCXML. The tick signal is provided via events. In AS2FM, we provide an implementation of the standard BT nodes. They can be used as they are or as a starting point for custom ones. 

- The _Blackboard_ is a key-value storage to exchange data between nodes at runtime. BT nodes can read and write data, which is exchanged via events from and to a BT management state machine. 

## IV. MODEL TRANSLATION 

The full system model must be translated from a set of SCXML state machines to the JANI format for model checking. 

## _A. SCXML System of State Machines_ 

Consider a set _M_ = _{M_ 1 _, M_ 2 _, . . . , Mk}_ of _k_ state machines, where each _Mi_ is specified in an SCXML-file. Each state machine _Mi_ can communicate with the other ones using the events _E_ . 

= Each state machine _Mi_ is defined as a tuple _Mi_ ( _Di, Ci, Pi, Si, s_ 0 _i, Ti_ ), where: 

- _Di_ is the set of data variables in _Mi_ . 

- _Ci_ is the set of conditions that are defined for _Mi_ . Each condition _c ∈ Ci_ is a boolean expression over the data from the variables in _Di_ and the data from the received events in _E_ . Formally _c_ : ( _Di ∪ E_ ) _→{_ false _,_ true _}_ . 

- _Pi_ defines executable content defined in _Mi_ . Each executable content _p ∈ Pi_ can modify the data variables _Di_ or send events _e ∈ E_ . Each executable content _p ∈ Pi_ can be defined as a sequence of operations _p_ = [ _o_ 1 _, o_ 2 _, . . ._ ]. Each step _ox_ is either a function _of_ modifying data objects or an event _oe_ being sent. A function can modify data entries of this state machine based on the content of other data entries or data from a received event _of_ : ( _Di ∪ E_ ) _× Di_ . An operation may also be to send an event _oe ∈ E_ to other state machines. 

- _Si_ is the set of states in _Mi_ . States may contain executable content that is executed _onentry_ and _onexit_ . A state _s ∈ Si_ may have a tuple _s_ = ( _p_ entry _, p_ exit), with _p_ entry _∈ Pi ∪{_ [ ] _}_ and _p_ exit _∈ Pi ∪{_ [ ] _}_ . 

- _s_ 0 _i ∈ Si_ is the initial state of _Mi_ . 

- _t ∈ Ti_ = ( _Si × Si ×_ ( _Ci ∪{_ true _}_ ) _×_ ( _E ∪{_ 0 _}_ ) _×_ ( _Pi ∪ {_ [ ] _}_ )) is the set of transitions in _Mi_ . Each transition _t_ is defined as a tuple _t_ = ( _s, s_<sup>_′_</sup> _, c, e, p_ ), where: **–** _s, s_<sup>_′_</sup> _∈ Si_ are the source and target states of the transition. 

   - _c ∈ Ci ∪{_ true _}_ is the condition that must be satisfied for the transition to be taken. _c_ is set to true if there is no condition on the transition. 

   - _e ∈ E ∪{_ 0 _}_ is the event that triggers the transition, or 0 if no event triggers the transition. Note that events may send data to this state machine, which we consider as read-only variables. 

- _p ∈ Pi ∪{_ [ ] _}_ is the executable content associated with the transition. 

State machines _Mi_ and _Mj_ may exchange data and influence each other’s execution by sending events. Specifically, an event _e ∈ E_ emitted by _Mi_ may be received by _Mj_ where it is processed according to _Mj_ ’s transitions. Data contained in the event is considered as an update to _Dj_ . This means, the synchronization between state machines is defined implicitly by the events exchanged between them. Figure 1a shows an example of two state machines that exchange events. 

## _B. JANI Network of Markov Decision Processes_ 

The JANI [12] format encodes a complete system as a network of MDPs, including a list of synchronized edges that can only be executed simultaneously. In the remainder of this section, we describe how to compile a JANI model from a system of SCXML state machines. 

Let _M_ = _{M_ 1 _, M_ 2 _, . . . , Mn}_ be the set of _n_ MDPs defined in the JANI model. _Dg_ is the set of global data variables shared by all MDPs in _M_ . This global data is used to implement the exchange of data associated with events in the state machines in _M_ . Each MDP _Mi_ is defined as a tuple _Mi_ = ( _Di,_ Φ _i,_ Σ _i, ς_ 0 _i, Ai, Ti_ ), where: 

- _Di_ is the set of data variables in _Mi_ . 

- Φ _i_ is the set of guards. Each guard _φ ∈_ Φ _i_ is a function of local and global variables evaluating to a binary value _φ_ : _Di ∪Dg →{_ false _,_ true _}_ . 

- Σ _i_ is the set of states in _Mi_ . 

- _ς_ 0 _i ∈_ Σ _i_ is the initial state of _Mi_ . 

- _Ai_ is the set of actions in _Mi_ . 

- _Ti_ = Σ _i ×_ Σ _i ×_ (Φ _i ∪{_ true _}_ ) _×Ai ×_ ( _Pi ∪_ 0) is the set of transitions in _Mi_ . Each transition _τ ∈Ti_ is defined as a tuple _τ_ = ( _ς, ς_<sup>_′_</sup> _, α, φ, ρ_ ), where: 

   - _ς, ς_<sup>_′_</sup> _∈_ Σ _i_ are the source and target states of the transition. 

   - _φ ∈_ (Φ _i ∪{_ true _}_ ) is the guard that must be satisfied for the transition to be taken. It may be set to true if there is no guard on the transition. 

   - _α ∈Ai_ is the action that triggers the transition. 

   - _ρ ∈_ ( _Pi ∪_ 0) is the assignment associated with the transition. Where _Pi_ defines assignments that modify the data variables in _Di_ and _Dg_ . Each assignment _ρ ∈Pi_ is a function _ρf_ : _Di × Dg → Di × Dg_ . _ρ_ is set to 0 if there is no assignment on the transition. 

The network of MDPs includes a set of synchronizations Γ. Each synchronization _γ ∈_ Γ is defined as a tuple _γ_ = ( _α_ 1 _, α_ 2 _, . . . , αn_ ), where _αi ∈Ai_ is an action in the MDP _Mi_ . One or more _αi_ may be 0 indicating that the MDP _i_ does not have an action in this synchronization. All actions _α_ 1 _, α_ 2 _, . . . , αn_ must be executed simultaneously and all of their guards must be satisfied for the synchronization to be taken. Figure 1b shows an example of two MDPs that synchronize using the actions _ae_ 2 _s_ and _ae_ 2 _r_ . 

**Algorithm 1** Translation from a set of SCXML state ma- <u>chines to a network of MDPs.</u> 

**Require:** _M, E,_ unique_id() 

- 1: event_senders _←_ ∅ 

- 2: event_receivers _←_ ∅ 

- 3: _M ←_ ∅ 

- 4: Γ _←_ ∅ 

5: **for** _Mi ∈ M_ **do** 6: Σ _i ← Si_ 7: _Di ← Di_ 8: _ς_ 0 _i ← s_ 0 _i_ 9: _Ti ←_ ∅ 10: **for** _t ∈ Ti_ **do** 11: _ς ← s_ 12: _φ ← c_ 13: _α ←_ unique_id() 14: **if** _e̸_ = 0 **then** 15: event_receivers[ _e_ ] _← α_ 16: **end if** 17: **for** _o ∈ p_ **do** 

18: _ςo ←_ unique_id() 19: **if** _o ∈ E_ **then** 20: event_senders[ _o_ ] _← α_ 21: _ρo ←_ [ ] 22: **else** 23: _ρo ← o_ 24: **end if** 25: _τo ←_ ( _ς, ςo, α, φ, ρo_ ) 26: _Ti ←Ti ∪{τo}_ 27: Σ _i ←_ Σ _i ∪{ςo}_ 28: _ς_ = _ςo_ 29: _α ←_ unique_id() 30: _φ_ = true 

- 31: **end for** 

- 32: _ς_<sup>_′_</sup> _← s_<sup>_′_</sup> 

- 33: _τ ←_ ( _ς, ς_<sup>_′_</sup> _, α, φ,_ [ ]) 34: _Ti ←Ti ∪{τ }_ 

- 35: **end for** 36: _Mi ←_ ( _Di,_ Σ _i, s_ 0 _i, Ti_ ) 

- 37: _M ←M ∪{Mi}_ 

38: **end for** 

- 39: **for** _e ∈ E_ **do** 40: _ςe_ 0 _←_ unique_id() 41: _ςe_ 1 _←_ unique_id() 42: Σ _e ←{se_ 0 _, se_ 1 _}_ 43: _αs ←_ unique_id() 44: _τs ←_ ( _ςe_ 0 _, ςe_ 1 _, αs,_ true _,_ [ ]) 45: _γs ←_ ( _. . . , αs, . . . ,_ event_senders[ _e_ ] _, . . ._ ) 

- 46: _αr ←_ unique_id() 47: _τr ←_ ( _ςe_ 1 _, ςe_ 0 _, αr,_ true _,_ [ ]) 48: _γr ←_ ( _. . . , αr, . . . ,_ event_receivers[ _e_ ] _, . . ._ ) 49: Γ _←_ Γ _∪{γs, γr}_ 50: _M ←M ∪{_ (∅ _,_ Σ _e, ςe_ 0 _, {τs, τr}_ ) _}_ 

51: **end for** 

52: **return** _M_ , Γ 

## _C. Translation Algorithm_ 

The translation is defined in Algorithm 1. It requires a set of SCXML state machines _M_ and the set of events _E_ that are exchanged between the state machines. It further requires a function unique_id() that returns a unique identifier for each element in the model in line 0. The data structures event_senders and event_receivers are used to keep track of the events that are sent and received by the state machines and are initialized empty in lines 1 and 2. Also the set of MDPs _M_ and the set of synchronizations Γ in lines 3 and 4 are initialized empty. 

Then, per state machine _Mi_ in _M_ , the states _Si_ , data variables _Di_ , and initial state _s_ 0 _i_ , are copied to the MDP _Mi_ (lines 6 to 8). The translation of transitions and their executable content _p_ happens in lines 10 to 35. Unique actions get generated and in case events are to be received or sent, they are stored (lines 15 and 20). The MDP _Mi_ gets an additional intermediate state _ςo_ per operation _o_ of the edge’s executable content _p_ (line 18). The same is done for executable content in _p_ entry and _p_ exit, detailed description is omitted for brevity. After all transitions are generated, the MDP _Mi_ is added to the set of MDPs _M_ in line 37. 

For each event _e_ in _E_ , we create a new MDP consisting of two states _ςe_ 0 and _ςe_ 1 (lines 40 - 50). _ςe_ 1 is the active state when an event _e_ is present and needs to be processed on the receiving side, _ςe_ 0 is active otherwise. Therefore, we add a transition from _ςe_ 0 to _ςe_ 1 that is synchronized with the action that sends the event _e_ in line 45. Similarly, we add a transition from _ςe_ 1 to _ςe_ 0, synchronized with the action receiving it in line 48. Finally, the additional MDP (∅ _,_ Σ _e, ςe_ 0 _, {τs, τr}_ ) is added to the set of MDPs _M_ (line 50) before returning _M_ and Γ (line 52). 

## V. EVALUATION 

In this section we evaluate the most important aspects of our approach. Firstly, we show a case study by verifying the correctness of a full robotic system after generating its formal model with AS2FM. Then, we evaluate the model checking runtime on that system across different SMC confidence intervals. Finally, we compare our toolchain consisting of AS2FM and a statistical model checker against the state-ofthe art, BehaVerify [37], in terms of runtime scalability. 

We use the SMC-tool _SMC Storm_ [13] with a confidence of 95% and a maximum error of 0 _._ 01, unless specified differently. All SMC-tools use these two values to define the desired confidence interval, which in turn determines the required amount of traces to generate during the verification process. All experiments are performed with an i7-11850H CPU and 32 GB of memory. 

## _A. Case Study_ 

This section demonstrates how our tooling is applied to a robotic control system based on BTs and ROS 2. The goal is to verify that an autonomous assembly robot reacts correctly in case a block falls from its gripper. The model consists of 14 separate SCXML state machines, including: 


Fig. 2: The BT used for controlling the assembly robot in the case study. 

- The BT executing the policy shown in Figure 2. 

- A model of the user-defined BT plugins: IsBlockFell, MoveBlock, RecoverBlock. 

- ROS 2 nodes encoding specific robot skills triggered from the BT: MoveBlockSkill, RecoverBlockSkill. 

The system is expected to tick the BT root for as long as it returns _RUNNING_ . Our goal is to verify that the move block operation is successful or, in case the block operation is aborted, the block recovery skill is enabled in time. This is described in Linear Temporal Logic (LTL) [15] as: 


where abort and success are boolean flags for representing if the move action was aborted or successful, recovery is a flag signaling if the recovery sequence was started, _tcurr_ is the current time, _tabort_ is the time the move action was aborted, and _ttimeout_ is a constant representing the maximum time the system can take to start the recovery sequence. _U_ is an LTL operator that reads as _until_ and is true if the left side is true in at least all states before the state in which the right side became true for the first time. 

After converting the model of this robot to JANI with AS2FM, and giving it to SMC Storm, the model checker reports that the probability of the model satisfying the property from Equation (1) is 0 _._ 499: this means that there are cases in which the system is not behaving as expected. 

SMC tools offer the possibility of exporting the generated traces as a CSV file, for inspecting them and determining the reason for the failure. In this particular case, the BT checks if the block fell only before starting to move it. It is unable to detect this after the MoveBlock plugin is started. This results in the system being unable to start the recovery sequence in case the block falls from the gripper, which in the model we used happens 50% of the times. 

The issue can be solved by replacing the _Sequence_ control node with a _ReactiveSequence_ one, that keeps checking if the blocks fell and, if that is the case, starts a recovery. Once the BT is fixed, the model can be checked again: this time the tool reports that the probability of satisfying the property is 1, confirming that the implementation is working as expected. 


Fig. 3: Comparing runtime and number of traces for different confidence intervals. Both metrics increase with the confidence interval. 


Fig. 4: Performance and scalability of the AS2FM + SMC Storm toolchain compared to BehaVerify. It is visible that the runtime of our tooling scales linearly with the size of the grid, while BehaVerify scales exponentially. 

## _B. Runtime over Confidence Value_ 

Again on the previous case study, we evaluate how different values for the confidence affect the number of necessary traces and therefore the runtime of the SMC tool. For each confidence value, we run the verification 100 times and measure the average runtime. 

It is visible from the results in Figure 3 that the runtime of SMC Storm increases with the confidence interval. This is expected, as the tool needs to generate more traces to reach the desired confidence. The number of traces generated also increases with the confidence interval, which is the reason for the increased runtime. 

## _C. Runtime and Scalability_ 

The runtime scalability of the AS2FM toolchain was evaluated in direct comparison to _BehaVerify_ [37], the stateof-the-art framework for verifying BTs only, which does not provide robotic-specific features, e.g., ROS communication, but which is the closest tool to ours. We used the example in their paper called _Simple Robot_ , based on a 4-connected grid world with a robot that has to reach randomly placed goal locations. The robot is controlled by a BT. To scale this 

example, the size of the grid in both dimensions is changed to the indicated size. This example was chosen because the other scaling example in their work, _Bigger Fish_ , is perceived as being specifically designed to work well with their custom optimization and does therefore not provide insights into the general performance of the verification tooling. 

In Figure 4 it can be seen, that the runtime of our tool is larger than that of BehaVerify for sizes of 110 or less. This can be attributed to the overhead that is introduced in our much more general approach by a more sophisticated model of communication (e.g., for ROS) which is crucial for the applicability in real-world robotic systems. But it is further visible that the runtime of our approach scales linearly with the size of the environment, while BehaVerify scales exponentially. These results can be attributed to using SMC opposed to full-state space model checking, which further underlines the practical usability of our approach with realworld systems that grow quickly in size. 

## VI. CONCLUSION 

We have demonstrated our approach for using Statistical Model Checking on full models of robotic control systems to increase their robustness. The models consist of SCXML state machines that benefit from an extension allowing the direct modelling of ROS 2 communication interfaces, and Behavior Trees in their native XML syntax. We contribute an algorithm to translate the full model in a network of MDPs. We demonstrated the approach on an industrial case study successfully identifying errors, and showing better scalability compared to the state of the art. In the future, the approach can be extended and improved by adding support for more complex environment models, by providing tools for easier inspection of the generated SMC traces and model checking results, and by making the SCXML format more accessible with the help of graphical interfaces. 

## REFERENCES 

- [1] A. Albore, D. Doose, C. Grand, J. Guiochet, C. Lesire, and A. Manecy, “Skill-based design of dependable robotic architectures,” _Robotics and Autonomous Systems_ , Feb. 2023. 

- [2] F. Rovida, M. Crosby, D. Holz, A. S. Polydoros, B. Großmann, R. P. A. Petrick, and V. Kr¨uger, “SkiROS—A Skill-Based Robot Control Platform on Top of ROS.” Springer International Publishing, 2017. 

- [3] J. Saukkoriipi, T. Heikkil¨a, J. M. Ahola, T. Sepp¨al¨a, and P. Isto, “Programming and control for skill-based robots,” _Open Engineering_ , no. 1, Jan. 2020. 

- [4] F. Ingrand and M. Ghallab, “Deliberation for autonomous robots: A survey,” _Artificial Intelligence_ , 2017. 

- [5] M. Colledanchise and P. ¨Ogren, _Behavior Trees in Robotics and AI_ , 2018. 

- [6] M. Quigley, K. Conley, B. Gerkey, J. Faust, T. Foote, J. Leibs, R. Wheeler, and A. Y. Ng, “ROS: An open- 

   - source Robot Operating System,” in _ICRA Workshop on Open Source Software_ . Kobe, Japan, 2009. 

- [7] M. Klauck, R. Lange, C. Henkel, S. Kchir, and M. Palmas, “Towards robust autonomous robots using statistical model checking,” in _ERF_ , 2024. 

- [8] C. Baier and J.-P. Katoen, _Principles of Model Checking_ . MIT press, 2008. 

- [9] A. Legay, A. Lukina, L. Traonouez, J. Yang, S. A. Smolka, and R. Grosu, “Statistical model checking,” in _Computing and Software Science - State of the Art and Perspectives_ , 2019. 

- [10] H. L. S. Younes, M. Z. Kwiatkowska, G. Norman, and D. Parker, “Numerical vs. statistical probabilistic model checking,” _Int. J. Softw. Tools Technol. Transf._ , no. 3, 2006. 

- [11] C. Street, Y. Warsame, M. Mansouri, M. Klauck, C. Henkel, M. Lampacrescia, M. Palmas, R. Lange, E. Ghiorzi, A. Tacchella, R. Azrou, R. Lallement, M. Morelli, G. I. Chen, D. Wallis, S. Bernagozzi, S. Rosa, M. Randazzo, S. Faraci, and L. Natale, “Towards a verifiable toolchain for robotics,” _AAAI Fall Symposium_ , 2024. 

- [12] C. E. Budde, C. Dehnert, E. M. Hahn, A. Hartmanns, S. Junges, and A. Turrini, “JANI: quantitative model and tool interaction,” in _TACAS 2017_ . 

- [13] M. Lampacrescia, M. Klauck, and M. Palmas, “Towards verifying robotic systems using statistical model checking in storm,” in _AISoLA_ , 2025. 

- [14] E. M. Clarke, T. A. Henzinger, H. Veith, R. Bloem _et al._ , _Handbook of model checking_ . Springer, 2018. 

- [15] M. Y. Vardi, “An automata-theoretic approach to linear temporal logic,” in _8th Banff Higher Order Workshop_ , 1995. 

- [16] M. Luckcuck, M. Farrell, L. A. Dennis, C. Dixon, and M. Fisher, “Formal specification and verification of autonomous robotic systems: A survey,” _ACM Comput. Surv._ , no. 5, 2019. 

- [17] C. Hensel, S. Junges, J. Katoen, T. Quatmann, and M. Volk, “The probabilistic model checker storm,” _Int. J. Softw. Tools Technol. Transf._ , 2022. 

- [18] L. P. Kaelbling, M. L. Littman, and A. R. Cassandra, “Planning and acting in partially observable stochastic domains,” _Artif. Intell._ , 1998. 

- [19] P. Laroche, F. Charpillet, and R. Schott, “Mobile robotics planning using abstract markov decision processes,” in _ICTAI ’99_ , 1999. 

- [20] L. Matignon, L. Jeanpierre, and A. Mouaddib, “Coordinated multi-robot exploration under communication constraints using decentralized markov decision processes,” in _AAAI_ , 2012. 

- [21] F. Ingrand and M. Ghallab, “Deliberation for autonomous robots: A survey,” _Artif. Intell._ , 2017. 

- [22] M. Foughali, B. Berthomieu, S. Dal Zilio, F. Ingrand, and A. Mallet, “Model Checking Real-Time Properties on the Functional Layer of Autonomous Robots,” in 

_Formal Methods and Software Engineering_ , 2016. 

- [23] R. Alur and D. L. Dill, “A theory of timed automata,” _Theor. Comput. Sci._ , no. 2, 1994. 

- [24] G. Behrmann, A. David, and K. G. Larsen, “A tutorial on uppaal,” in _SFM-RT_ , 2004. 

- [25] G. Behrmann, P. Bouyer, K. G. Larsen, and R. Pel´anek, “Lower and upper bounds in zone-based abstractions of timed automata,” _Int. J. Softw. Tools Technol. Transf._ , no. 3, 2006. 

- [26] M. T. B. Waez, J. Dingel, and K. Rudie, “A survey of timed automata for the development of real-time systems,” _Comput. Sci. Rev._ , 2013. 

- [27] M. Luckcuck, M. Farrell, L. A. Dennis, C. Dixon, and M. Fisher, “Formal Specification and Verification of Autonomous Robotic Systems: A Survey,” _ACM Computing Surveys_ , no. 5, Sep. 2020. 

- [28] T. K. Iversen, K. J. Kristoffersen, K. G. Larsen, M. Laursen, R. G. Madsen, S. K. Mortensen, P. Pettersson, and C. B. Thomasen, “Model-checking realtime control programs: Verifying lego mindstorms tm systems using uppaal,” in _Euromicro RTS 2000_ , 2000. 

- [29] C. Dixon, M. Webster, J. Saunders, M. Fisher, and K. Dautenhahn, ““The Fridge Door is Open”–Temporal Verification of a Robotic Assistant’s Behaviours,” in _Advances in Autonomous Robotics Systems_ . Springer International Publishing, 2014. 

- [30] A. Desai, T. Dreossi, and S. A. Seshia, “Combining Model Checking and Runtime Verification for Safe Robotics,” in _Runtime Verification_ . Springer International Publishing, 2017. 

- [31] A. Miyazawa, P. Ribeiro, W. Li, A. Cavalcanti, J. Timmis, and J. Woodcock, “RoboChart: Modelling and verification of the functional behaviour of robotic applications,” _Software & Systems Modeling_ , no. 5, Oct. 2019. 

- [32] J. Baxter, G. Carvalho, A. Cavalcanti, and F. R. J´unior, “RoboWorld: Verification of Robotic Systems with Environment in the Loop,” 2023. 

- [33] M. Y. Hazim, H. Qu, and S. M. Veres, “Testing, Verification and Improvements of Timeliness in ROS Processes,” in _Towards Autonomous Robotic Systems_ , 2016. 

- [34] R. Halder, J. Proenc¸a, N. Macedo, and A. Santos, “Formal verification of ROS-based robotic applications using timed-automata,” in _FormaliSE_ , 2017. 

- [35] R. Carvalho, A. Cunha, N. Macedo, and A. Santos, “Verification of system-wide safety properties of ROS applications,” in _IROS_ , 2020. 

- [36] A. F. F. Santos, “Safety verification for ros software,” 2021. 

- [37] S. S. Serbinowska, P. Robinette, G. Karsai, and T. T. Johnson, “Formalizing Stateful Behavior Trees,” _EPTCS_ , 2024. 

- [38] Jim Barnett, “State Chart XML (SCXML): State Machine Notation for Control Abstraction,” 2015. 

