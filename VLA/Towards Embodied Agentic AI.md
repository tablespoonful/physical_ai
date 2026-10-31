---
title: "Towards Embodied Agentic AI: Review and Classification of LLM- and VLM-Driven Robot Autonomy and Interaction"
date: "2025-08-07"
authors: "Sahar Salimpour; Lei Fu; Kajetan Rachwał; Pascal Bertrand; Kevin O'Sullivan; Robert Jakob"
url: https://arxiv.org/abs/2508.05294
pdf: https://arxiv.org/pdf/2508.05294
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2508.05294)** / [論文ページ](https://arxiv.org/abs/2508.05294)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# Towards Embodied Agentic AI: Review and Classification of LLM- and VLM-Driven Robot Autonomy and Interaction 

Sahar Salimpour<sup>*1</sup> , Lei Fu<sup>*1,2</sup> , Kajetan Rachwał<sup>5,7</sup> , Pascal Bertrand<sup>4</sup> , Kevin O’Sullivan<sup>4</sup> , Robert Jakob<sup>4</sup> , Farhad Keramat<sup>1</sup> , Leonardo Militano<sup>2</sup> , Giovanni Toffetti<sup>2</sup> , Harry Edelman<sup>6</sup> , Jorge Pe˜na Queralta<sup>3,6</sup> 

> 1Department of Computing, University of Turku 

> 2Institute of Computer Science, Zurich University of Applied Sciences 

> 3Centre for Artificial Ingelligence, Zurich University of Applied Sciences 

> 4Agentic Systems Lab, Department of Management, Technology and Economics, ETH Z¨urich 

- 7 Faculty of Mathematics and Information Science, Warsaw University of Technology 

5Robotec.ai 6Binabik.ai 

- *Authors with equal contribution. Emails: _{_ sahars, fakera _}_ @utu.fi, _{_ fule, milt, toff, penq _}_ @zhaw.ch, pbertrand@student.ethz.ch, 

_{_ kosullivan, rjakob _}_ @ethz.ch, kajetan.rachwal@robotec.ai, harry@binabik.ai 


Fig. 1: Illustration of the main approaches to integrating large language models (LLMs), vision-language models (VLMs), and related foundation models into robotic systems. This survey focuses on the integration perspective and the role of such models within the wider robotic system where it is deployed. Our goal is to discuss The current state-of-the-art within the context of Embodied Agentic AI applications. The figure highlights how model integration differs in terms of **agent architecture** , **interaction topology** , and the resulting level of _agency_ . In **Protocol-Focused Integration** , an LLM serves as a translator between user commands and predefined APIs or protocols, typically through single-shot tool calls. **Interface or Agentic Integration** introduces ReAct-style loops and conversational interaction, allowing the agent to reason, call tools, and respond iteratively within the physical or simulated environment. **Orchestration-Oriented Integration** elevates the model to a supervisory role, coordinating multiple agents, skills, or robotic subsystems through structured workflows. Finally, **Direct or Embedded Integration** corresponds to end-to-end or model-centric policies (e.g., VLA or LBM architectures) that directly map perception to action in continuous control loops. 

**_Abstract_ — Foundation models, including large language models (LLMs) and vision-language models (VLMs), have recently enabled novel approaches to robot autonomy and human-robot interfaces. In parallel, vision-language-action models (VLAs) or large behavior models (LBMs) are increasing the dexterity and capabilities of robotic systems. This survey paper reviews works that advance agentic applications and architectures, including initial efforts with GPT-style interfaces and more complex systems where AI agents function as coordinators, planners, perception actors, or generalist interfaces. Such agentic architectures allow robots to reason over natural language instructions, invoke APIs, plan task sequences, or assist in operations and diagnostics. In addition to peer-reviewed research, due to the fast-evolving nature of the field, we highlight and include community-driven projects, ROS packages, and industrial frameworks that show emerging trends. We propose a taxonomy for classifying model integration approaches and present a comparative analysis of the role that agents play in different solutions in today’s literature.** 

## I. INTRODUCTION 

Large language models (LLMs) and vision-language models (VLMs) have recently enabled new modalities of interaction and reasoning in robotics. While early work focused on end-toend pipelines, mapping raw sensory input and natural language directly to robot actions, there is growing interest in modular systems that use foundation models as high-level agents. These agents interpret user intent, generate plans, invoke robot APIs, or interface with middleware such as the Robot Operating System (ROS), without replacing the underlying robot stack. 

This agentic approach offers several advantages. By integrating with existing functionality, LLMs can extend the flexibility and usability of robots without discarding tested software modules. Agents can reason over unstructured instructions, select or sequence robot capabilities, and adapt responses through interaction. Recent examples include ROS interfaces for LLMs, protocol-based control layers, and agents that coordinate multiple subsystems or external tools. 

Several surveys have addressed the broader intersection of foundation models and robotics [1]–[5], with a focus on multimodal architectures and their components and primarily emphasizing the general use of multimodal models in robotic decision-making and high-level planning, as well as end-toend learning frameworks for low-level control in domainspecific settings such as manipulation. However, with the very recent rise of emergence of embodied and generalist AI agents, no prior survey to date has examined the emerging design patterns in which AI agents interface with existing control software, libraries, or middleware. Moreover, many practical systems (GitHub-hosted projects, ROS packages, or startup prototypes) remain underrepresented in the literature despite their increasing real-world relevance and impact. 

This survey addresses that gap. We review recent academic and community-driven work on AI agents in robotics, emphasizing architectures that position LLMs and VLMs as intelligent intermediaries rather than direct policy generators. Our contributions are twofold: 

- We discuss the concept of _Agentic AI_ in robotics and distinguish it from end-to-end learning or classical symbolic planning approaches. 

- We propose a taxonomy across two dimensions: integration approach to foundation models (Section III, see also Fig. 1), and agent role (Section IV, see also Fig. 3). 

- We include the section (§V) presenting a practical design toolkit to guide implementation and prototyping. 

- Finally, the paper concludes with a detailed discussion (§VI) that highlights key open questions and outlines promising directions for future research in agentic embodied AI. 

Together, these elements provide an alternative view, more technical and application-oriented, to the use of foundation models in robot systems. 

## II. TOWARDS EMBODIED AGENTIC AI 

The concept of an embodied robotic agent was introduced in the late 1980s, grounded in the idea that intelligent behavior emerges from a system’s physical embodiment and its continuous sensorimotor interaction with the environment [18]. This laid the foundation for early end-to-end neural models that directly mapped perception to action, enabling autonomous control without explicit symbolic reasoning [7], [19], [20]. The emergence of LLMs has significantly expanded the functional scope of autonomous agents, shifting them from narrowly scoped, rule-driven systems to more flexible entities capable of generalization, contextual reasoning, and adaptive behavior [21]. At pre-ChatGPT era, Code as Policies (CaP) [6] introduced robot-executable language model generated programs (LMPs), enabling reactive and vision-based control via indirect tool calling through code generation. 

The release of OpenAI’s ChatGPT in November 2022 marked a major progression in the trajectory of embodied agentic AI, catalyzing the widespread adoption of LLMs as foundational components in robotic systems. While ROS has long been a standard framework for robot software integration, initial efforts to operationalize LLMs as autonomous agents predominantly targeted ROS-compatible platforms. By 2023, early prototypes began to explicitly integrate LLMs with robotic frameworks, mainly focusing on protocol integration and bidirectional communication interfaces between LLMs and ROS. 

Early exploration in this domain focused on natural language interfaces for ROS 2, including _ros2ai_ [22], an extension to augment the ROS 2 command line interface with LLM, and ROScribe [23], a tool using LLMs to generate ROS codebases from a high-level description (e.g. a user describes a desired ROS graph (sensors, topics, and functionality) and ROScribe will output Python code for ROS nodes and launch files to implement that spec). Furthermore, the ROS-LLM framework [24] was proposed to enable embodied intelligence applications. It provides a template to define your robot’s API in a config file, then handles the prompt engineering and calls to the OpenAI API, effectively acting like a customizable agent. Concurrently, Microsoft’s ChatGPT for Robotics [8] introduced a modular approach to LLM-based robot control and programming, defined a high-level API specific to each robot, leveraging prompt engineering and pre-defined function libraries to enable natural language control across diverse tasks 

2 

### First end-to-end models 


Fig. 2: Progression of projects at the intersection of Generative AI and Robotics with a focus on LLMs, VLMs and VLAs. 

and simulation environments. During this phase, most implementations adopted a chatbot-style design, deploying LLMs to interpret free-form textual inputs and generate appropriate commands for general robot integration. 

Building on these advances, 2024 marked a transformative shift with the development of specialized LLM interfaces for robotics and VLA systems, unlocked unprecedented generalization and semantic reasoning capabilities in robotic control systems. These frameworks enabled agents to process open-ended natural language instructions, ground them in visual perception, and execute corresponding actions [15]. A notable breakthrough was RT-2 [9], which introduced a novel VLA framework by co-fine-tuning pretrained VLMs on both robotic trajectory data and internet-scale vision-language tasks. _π_ 0 [13] advanced the field by introducing real-time, continuous control via flow-matched diffusion policies, unifying perception, reasoning, and motion generating in a single differentiable framework. 

Simultaneously, agentic middleware frameworks such as ROSA (Robot Operating System Agent) [10], RAI (Robotic AI Agent) [11], and BUMBLE [12] emerged, bridging the gap between LLM-based reasoning and traditional robotic middleware, in the pursuit of embodied AI. Initially open-sourced in late 2023, ROSA represents a significant advancement in AIdriven robotic control by implementing an LLM agent built on the LangChain framework and the ReAct (Reasoning and Acting) agent paradigm. Its core innovation was the abstraction of ROS operations into tool-enabled Python functions - including listing available nodes, reading sensor data, moving a joint, etc. This allowed ROSA to translate natural language commands into validated robot actions. ROSA also embedded safety mechanisms like parameter validation, constraint enforcement, and optional human approval for critical actions. The authors demonstrate ROSA across heterogeneous platforms, including JPL’s NeBula-Spot quadruped and NVIDIA Isaac Sim environments. However, its architecture remains tightly coupled to ROS-based middleware, limiting interoperability with non-ROS systems and constraining deployment in broader contexts. RAI is another approach in this field as a flexible embodied multi-agent framework designed to integrate LLM reasoning with robotic systems (e.g. ROS 2). Its architecture introduces a novel distributed paradigm where specialized LLM agents, including perception modules, task planners, motion controllers, and safety monitors, collaborate 

through well-defined roles to enable concurrent, real-time task execution while maintaining system safety and reliability. The framework’s core components (Agents, Connectors, and Tools) provide integrated capabilies for multimodel sensing and actuation, retrieval-augmented generation through vector stores and pre-configured agent types (voice, conversational, state-based). The framework demonstrates particular advancement in dynamic environments, featuring capabilities like online replanning and failure recovery. Proven on both physical (Husarion ROSBot XL) and simulated (tractor and manipulator) platforms. However, the framework is constrained by the limited spatial reasoning and unreliable self-correction of LLM-based agents, which repeatedly led to failures in understanding physical boundaries, object interactions, and task completion. BUMBLE (BUilding-wide MoBiLE Manipulation) is another recent contribution that uses a unified VLMbased framework for building-wide mobile manipulation. It integrates open-world perception, dual-layered memory systems, and a wide range of motor skills, allowing effective operation over extended spatial and temporal horizons. Unlike frameworks such as ROSA, which rely heavily on ROSbased middleware integration, BUMBLE features tighter coupling with navigation systems through the use of predefined landmark images. While this provides efficient and precise navigation, it also introduces limitations, such as requiring prior manual collection of landmark imagery. Nevertheless, BUMBLE’s combination of perception and action capabilities presents a significant advance in addressing the complexity of real-world environment. 

Another notable development is the concept of an MCP (Model Context Protocol) server, driving agentic use and quick integration of new capabilities into existing tools (e.g., Anthropic’s Claude or AI-driven code editors like Cursor). Their penetration in robotics is so far community-driven, with several projects openly available on GitHub. The ROS-MCP library [25], for example, connects to AI assistants such as Claude and enables interaction with installed ROS 2 applications. The capabilities include (i) launching UI applications, including the Gazebo simulator and the RViz visualizer; (ii) ROS resource management (topics, nodes); (iii) ROS system interaction (publishing to topics, calling services, send action goals); (iv) environment debugging; and (v) process management (e.g., cleaning up running ROS 2 processes). This represents a paradigm shift from other frameworks that provide 

3 

a complete application system such as ROSA and RAI, with MCP servers taking a _plugin_ -based approach instead, requiring standard AI assistant applications. Another example is the _rosmcp-server_ [25], which uses _rosbridge_ to connect to either ROS 1 or ROS 2 systems through WebSockets, and contains specific interfaces to odometry and velocity control topics. A benefit of leveraging assistants like Claude is that they already have other built-in tooling, such as web search, and the ability to run code internally in a sandboxed environment. This opens the possibility to more advanced behaviors without additional implementation. Additional implementation developed by robotmcp [26] provides a unified interface that connects LLMs with existing ROS/ROS 2 systems without requiring source code changing, enabling true two-way integration where natural language commands are translated into ROS actions while AI can simultaneously monitor the robot states and sensor data in real time. 

A final and more recent open-source framework for agentic AI in robotics is driven by the startup OpenMind [17]. OpenMind’s OM1 introduces a modular, hardware-agnostic AI runtime intended for various robotic platforms. Compared to earlier frameworks such as ROSA and RAI, which primarily target integration with ROS-based middleware, OM1 differentiates itself with its decentralized FABRIC coordination protocol. FABRIC enables secure identity management and interoperability among heterogeneous robotic systems, diverging from the centralized orchestration common in earlier systems. While OM1 utilizes Python-based configurations and incorporates perception-action loops similar to VLA-driven systems like RT-2, it notably emphasizes decentralization. Overall, OM1 represents a step toward more collaborative and flexible robotic ecosystems. 

In summary, the past three years have seen a rapid proliferation of interfaces and integration approaches for foundation models and robotics frameworks. From ROSA’s polished LangChain tools, to community-driven MCP servers, to bespoke industry solutions, the trend is clear: robots are getting a higher-level “AI agent” layer that can understand human intent and manage the robot’s own software toolkit. 

Figure 2 illustrates in a timeline format some of the key milestones and most representative works of the past three years. The top part of the figure focuses on agentic-oriented approaches, while the bottom part lists other relevant models that have shaped the advances of the field. A more comprehensive list of works, both academic papers and community projects, is available in Table II. The categorization of integration approaches is discussed in detail in Section III. The toolset/skillset primarily reflects the mechanisms through which each system executes actions. In most works, these actions are realized through custom toolsets, referring to predefined tool classes within agentic frameworks or task-specific functions designed by developers. In other cases—particularly for vision-based systems—the actions are driven by pretrained models or policy networks that interpret sensory inputs to perform manipulation or navigation tasks. The memory component, a fundamental aspect of agentic systems, is generally implemented in relatively common forms such as chat history or logging-based storage. In a few recent works, memory 

modules are extended to structured databases or multimodal memory architectures that store both textual and visual context. The world model refers not only to the representation of the physical environment, objects, and robot dynamics but also to high-level behavioral and reasoning constructs, such as system prompts that define goals, constraints, and operational rules. While the concept of a world model is closely related to the notion of adaptation, as both contribute to an agent’s ability to generalize and reason about novel situations, the world model primarily supports environmental understanding, whereas adaptability reflects the system’s capacity to update or extend its skills in response to new tasks. 

## III. APPROACHES TO LLMS/VLMS/VLAS AND AI AGENTS IN ROBOTICS 

We propose a taxonomy to classify the work to date based on the way that large language or foundation models are integrated into robotic systems. Instead of focusing on the role, use case or type of model, our objective here is to classify the integration from a conceptual and interaction point of view. 

To that end, we propose the existence of, currently, four main directions in which foundation models are integrated into robotic systems: (i) _protocol_ integration, where the focus is on using the model as a _translator_ between protocols (e.g., user input to predefined toolset); (ii) _interface_ integration, where the focus is to provide an interactive approach connecting user, robotic system and the environment; (iii) _orchestrationoriented_ integration, where the model is in charge of managing resources, tools or subsystems; and (iv) _direct_ or _embedded_ integration, where the model acts as a perception or control policy, either end-to-end, or as a specific subsystem. These approaches are illustrated in Fig. 1. Table I also provides a summary of the principal aspects and differences within this categorization. In addition, we classify a selection of representative works based on their integration approach in Table II. 

## _A. Protocol Integration_ 

The first category, and arguably the conceptually simplest way of integrating foundation models such as LLMs into a robotic system, is to use them as _translators_ of user inputs. 

For example, _ros2ai_ [22] does this by translating a generic user prompt into one specific ROS 2 command line interface tool call. The interaction is limited, although possible, and the process is mostly _unidirectional_ (e.g., the user is presented with the response of the ROS command). 

More recently, with the advent of the MCP protocol as the de-facto standard for tool use in LLMs/VLMs, multiple authors have proposed technical integrations [25], [29]. The available tooling can span multiple domains: interaction with graphical interfaces (e.g., launching a simulator), the previously mentioned execution of ROS 2 command line interface commands, or the connectivity with ROS communication paradigms (publishing/subscribing) to specific topics, calling services, or executing actions. Indeed, the MCP protocol maps well with, e.g., the service and action interfaces in ROS. 

4 

TABLE I: Comparison of Integration Approaches 

|**Aspect**|**Protocol-Focused Integration**|**Interface / Agentic Integration**|**Orchestration-Oriented Integration**|
|---|---|---|---|
|**Main role**|LLM maps user text directly to<br>tool/API calls|LLM acts as user-facing agent that<br>reasons and executes actions|LLM (or small crew) coordinates multiple<br>agents, skills, or robots|
|**Tooling focus**|Individual API or CLI calls, simple<br>wrappers|MCP or internal tools, loops or<br>concurrent tool calls|LangChain/LangGraph, or custom multi-agent<br>orchestration pipelines|
|**Typical frameworks**|MCP servers, ROS CLI bindings|LangChain,<br>LangGraph<br>(ReAct<br>agents), ROSA, RAI|LangGraph, custom orchestrators (e.g., AutoRT)|
|**User interaction**|Direct query–response|Conversational, human-in-the-loop<br>reasoning|Limited direct dialogue; user gives high-level<br>goal, orchestrator manages subtasks internally|
|**Physical interaction**|Minimal or indirect (via one API)|Yes: calls tools that affect sensors<br>or actuators|Indirect: delegates real-world execution to sub-<br>agents or robots|
|**Agent focus**|Translation between natural lan-<br>guage and system commands|Reasoning + execution|Task assignment, scheduling, and monitoring|
|**Analogy**|Command translator|Assistant / operator|Project manager / mission control|


A notable related approach is code-as-policies [6], where the LLM outputs Python code to perform the task (using a predefined API for sensorimotor actions). The code is then executed in a loop. Essentially, the LLM “programs” the robot on the fly. 

## _B. Interface Integration_ 

Keeping the tool calling capabilities of a _protocol_ integration, but enhancing the interactiveness, we classify as _interface_ integrations those approaches where either (i) the output of tools (often in terms of actions in the real world) affects future commands or additional tool calls from the model; or (ii) the focus is on the user interaction, e.g., in HRI applications. 

This category also goes in line of the research towards more _agentic_ applications, where foundation models gain further agency with respect to user commands, perform more complex tool calls, and often run in a loop with multiple iterations and multiple tool calls per iteration. 

In this paradigm, user commands can stay high level, while the foundation models can decompose the command into a number of tool calls. Additionally, as in ROSA, RAI, or BUMBLE, actions or tool calls might span a certain amount of time, requiring action feedback to be given back to the user and/or the model. 

The most recent and arguably complete open-source agentic system to date is OpenMind [17], a commercial effort that has been demonstrated in humanoid and quadruped robots, among others, and is defining a new AI-centric “operating system” for intelligent robots. 

## _C. Orchestration-Oriented Integration_ 

We separate _interface_ from _orchestration_ integration approaches in that the latter are focused on the problem of resource management, rather than the interaction with the user. These include mainly approaches where LLMs or VLMs act as planners or coordinators, often with other AI agents involved. 

This classification category spans both the integration approach and the role of the model, which is described in Section IV, where we further describe planner and orchestration agent roles. 

## _D. Embedded or Direct Integration_ 

This category encompasses approaches where the LLM (or a multimodal variant) directly produces either (i) actions for the robot in an end-to-end manner, or (ii) a specific output (e.g., to be used as a perception module). These are often referred to as robotic foundation models, in their end-to-end variant. These approaches are also well covered in existing review papers [1]– [4]. Therefore, we only include in this survey those that are most relevant from a historical perspective, or have potential to advance towards more agentic systems. Those works are included in Table II. 

## _E. Agentic Frameworks_ 

It is important to note that more complex systems might span multiple categories. For example, a system might encompass an interface agent for user input, an internal coordinator agent, and potentially both protocol and direct agents as subsystems managed by the coordinator. However, most works to date focus on one specific integration approach, owing to the relative low maturity of the field. 

In that context, we can also consider solutions such as RAI or OpenMind as frameworks, as they also provide tooling and infrastructure for multi-agent coordination and support for specialist agents. However, the current stage of development and deployment is closer to the _interface_ integration class. 

## IV. ROLES AND ARCHITECTURES OF ROBOTIC AGENTS WITH LLMS 

As we surveyed recent LLM-integrated robotic systems, it became clear that many differ not in the tasks they perform, but in how they structure decision-making, control, and modularity. To capture these architectural distinctions, we group the agents according to their functional design rather than their application domain. This perspective enables a clearer comparison of how different systems reason, sequence actions, invoke tools or skills, and interface with low-level controllers. While the boundaries between categories are often blurred, since many systems integrate multiple capabilities, the classification in Figure 3 highlights each work’s primary role and functionality. 

5 

|**Adaptation**|N.A|N.A|N.A|N.A|Sys. prompt<br>& tools|Sys. prompt<br>& tools|Custom tools|Sys. prompt<br>& tools|Custom skills|Pretrained<br>policies|Custom tools|-|Pretrained<br>policies|Custom tools|Custom tools|N.A|Custom tools|Custom<br>Skillsets|Sys. prompts|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Open-**<br>**source**|✓|✓|✓|✓|✓|✓|✓|✓|✓|✗|✓|✗|✓soon|✓soon|✓|✓|✓|✓|✓|
|**World**<br>**model**|✓|✗|✗|-|✓|✓|✓|✓|✓|✗|-|-|✗|✗|✗|✗|✗|✗|✓|
|**Multi-**<br>**modal**|LLM|LLM|LLM|LLM|LLM|VLM|VLM|VLM|VLM|VLM/<br>VLA|LLM|VLA|VLA|VLM|VLM|LLM/<br>VLM|LLM/<br>VLM|LLM|VLM/<br>LLM|
|**Memory**|Variable<br>logging|✗|Logging|-|✗|Chat<br>history|-|Semantic<br>Memory|Multimodal<br>memory|-|-|-|-|Multimodal<br>memory|Chat<br>history|Multimodal<br>vector<br>database|✗|Dynamic<br>memory|Logging|
|**Toolset/ skillset**|Indirect tool through<br>coding|ROS 2 CLI|ROS actions/services<br>or code API|Custom tools|Custom tools|Custom tools|Custom toolsets|Custom tools|Predefined skill<br>library|Pretrained RT<br>policies|Custom tools|Tool library|Pretrained policies|Custom toolsets|Custom toolsets|Custom toolsets|Custom toolsets|Custom Policies for<br>manipulation|Custom toolsets/ On<br>the fly code generation|
|**Integration**<br>**Approach**|Protocol|Protocol|Protocol|Protocol/<br>Interface|Protocol/<br>Interface|Interface|Interface/<br>Framework|Interface|Interface|Orchestration|Protocol|Embedded|Embedded|Embedded|Interface/<br>Framework|Protocol|Protocol/<br>Interface|Orchestration|Framework|
|**Year**|2022|2023|2023|2023|2023|2024|2024|2024|2024|2024|2025|2025|2025|2025|2025|2024|2024|2024|2025|
|**Description**|Robot-Centric formulation of<br>language model programs|ROS 2 command line<br>interface extension with LLM|ROS framework for embodied<br>intelligence applications|Create ROS packages using<br>LLMs|High-level functions library<br>for robotics application|ROS Agent, interact with<br>ROS-based robotics systems|AI agent framework for<br>embodied AI|ROS 2 based framework for<br>robot to understand models|Framework for open-world<br>perception system|Models for Orchestration of<br>Robotic Agents|Converts natural language to<br>ROS command|Generalist VLA model|VLA for general mobile<br>manipulation|General-Purpose Robotic<br>Navigation via LVLM|Modular AI runtime for<br>agents and robots|Explanations of robot<br>behavior using RAG method|Integrate llama.cpp with<br>ROS 2 to enable LLM<br>inference|Orchestrates skills for<br>language-directed mobile<br>manipulation|Distributed AI Agents for<br>Underwater Robot Autonomy|
|**Project**|**CaP** [6]|**ros2ai**[22]|**ROS**_−_**LLM**<br>[24]|**ROScribe**<br>[23]|**ChatGPT**<br>**Robotics**[8]|**ROSA**[10]|**RAI** [11]|**Embodied**<br>**Agents**[27]|**BUMBLE**[12]|**AutoRT**[28]|**ROS**_−_**MCP**<br>[25], [26],<br>[29]|**Gemini**<br>**Robotics**[14]|**MoManip**<br>**VLA** [30]|**ARNA**[31]|**OpenMind**<br>**OM1** [17]|**explainable**<br>**ros** [32]|**LLama**<br>**ros** [33]|**Stretch**<br>**AI** [34]|**UROSA**[35]|


6 


Fig. 3: Classification of existing works by primary role and functionality. 

_1)_ **_Planner Agents_** _:_ In this paradigm, an LLM plans a sequence of actions for the robot, typically by selecting or sequencing discrete skills. The LLM does not directly control actuators; instead, it outputs high-level plans that are grounded and executed by lower-level controllers. This design allows the LLM to focus on reasoning and decomposition while ensuring safety and feasibility through separate modules. 

A foundational example is Google’s SayCan [36], where the LLM (PaLM) generates possible next actions (e.g., “pick up can” or “move to kitchen”), and a learned value function (affordance model) evaluates each option based on the robot’s current state. The most feasible action is then executed by the appropriate skill module. Similarly, SELP [37] uses an LLM to generate symbolic task plans, followed by structured safety and efficiency filtering before execution. ConceptAgent [38] extends this idea further by incorporating a symbolic planner and a precondition-grounding module, enabling robust task decomposition and dynamic re-planning based on environment feedback. 

In contrast to orchestration agents—which continuously interact with perception, memory, and tool APIs in realtime—planning agents produce a plan upfront or iteratively refine it, with limited API interaction during execution. While orchestration agents serve as active runtime managers, planning agents focus on task structuring and leave execution monitoring to other components. 

_2)_ **_Orchestration Agents_** _:_ As robotic systems become increasingly modular and skill-rich, a new class of agents has emerged where the LLM functions not as a planner for a single robot, but as an orchestrator that manages interactions between multiple skills, components, or even agents. These systems 

treat the LLM as a central controller that interprets high-level task instructions and delegates responsibility to subsystems or external tools capable of execution. 

In this setting, the LLM does not execute physical actions itself, nor does it merely plan a single sequence. Instead, it performs decision-level control over which skill to invoke, which robot should act, or when to switch between behaviors. This architecture enables modularity, scalability, and adaptability, especially in multi-agent or high-skill-count environments. 

For example, AutoRT [28] deploys an LLM to orchestrate a fleet of real-world mobile manipulators. The system uses prompt-based reasoning to map natural language instructions to specific skill invocations (e.g., grasping, opening, navigating), while integrating filtering layers to ensure safety and feasibility. Similarly, LABOR Agent [40] enables bimanual robotic manipulation by selecting among hundreds of pretrained skills. The LLM determines which skill or skill chain should be used given a complex manipulation instruction, using grounding modules to connect symbolic task descriptions to real-world motor behaviors. 

In our categorization, orchestration agents primarily refer to systems that handle high-level task planning and assignment, either by coordinating multiple internal agents within a single robot [39], or by distributing tasks across multiple embodied agents (i.e., multiple robots) [41]. While they rely on predefined capabilities, the orchestration logic remains flexible, enabling adaptive responses to novel combinations of goals, environments, or agent configurations. 

_3)_ **_Task-Specific Agents_** _:_ Task-specific agents are designed to solve narrowly defined problems, which used to rely on specialized training data or domain-specific policies. Recent 

7 

work, however, explores how large language and visionlanguage models can enhance task-specific performance by enabling zero-shot reasoning or dynamic planning for particular objectives. For instance, LGX enables an embodied agent to find novel, uniquely described objects (e.g., ”catshaped mug”) using language-guided exploration and visionlanguage grounding without task-specific training [44]. Similarly, NavGPT uses explicit reasoning over visual and linguistic cues to follow navigation instructions, demonstrating that language models can guide task-specific behavior without prior tuning on navigation data [43]. ARNA leverages an LVLM to dynamically orchestrate perception and control modules for general-purpose navigation, but it can also be framed as a task-specific agent when executing goal-directed exploration in unseen environments [31]. Similarly, BUMBLE demonstrates a highly capable agent for manipulation and navigation by integrating an LLM with a world model and structured memory, enabling it to follow user instructions across tasks. 

_4)_ **_Model-Centric Agents_** _:_ Unlike traditional VLA models that often require separate components for perception, reasoning, and action, each trained or tuned independently, model-centric agents adopt a unified architecture where a single model is responsible for grounding multimodal inputs (e.g., images, language, proprioception) and directly producing action outputs. Examples include LEO [45], which leverages a decoder-only large language model to integrate 2D egocentric vision, 3D point clouds, and text for both instruction following and physical interaction in 3D environments; RoboCat [46], which uses a goal-conditioned decision transformer to generalize across robotic embodiments and tasks through large-scale training and self-improvement; and RoboAgent [47], which achieves high data efficiency and broad task generalization through semantic augmentation and action chunking within a unified policy model. 

_5)_ **_Generalist Agents_** _:_ This category of agents reflects a shift toward foundation-style architectures for robotics, where a centralized reasoning model (often an LLM or a multimodal transformer) interfaces flexibly with grounded, executable components. Although each system may differ in how tools are created, selected, or executed, they share a common philosophy: general-purpose reasoning layered on top of taskspecialized capabilities. 

Generalist agents are typically built for multi-task, multidomain operation. Their architectures are modular by design: the high-level model interprets goals, decomposes them into subtasks, and delegates execution to a set of low-level modules, which are usually predefined skills, learned action models, or custom tools. These execution modules may be static (pretrained) or dynamic (created and expanded during deployment). 

For example, Voyager [48] is an open-ended generalist agent that autonomously explores new tasks in Minecraft by generating its own tools (as Python functions), evaluating them, and storing them for future use—effectively building a lifelong, self-curated skill library. Similarly, Code as Policies uses an LLM to generate executable Python policies that map observations directly to robot actions. ODYSSEY [49] likewise operates in an open-world setting, using an LLM 

to reason about tasks and select from a rich library of skills grounded in the environment. In the real world, RoboGPT [50] demonstrates generalist behavior by interpreting language instructions and invoking appropriate pretrained skills for manipulation and navigation, without needing task-specific retraining. 

What distinguishes these agents is not just their task breadth, but their ability to generalize across tasks through modular reasoning and flexible skill integration—an architectural pattern increasingly central to the future of scalable robotic intelligence. 

_6)_ **_Generalist Systemic Agents_** _:_ Generalist Systemic Agents focus on building reusable, modular frameworks that simplify the development and orchestration of LLM-based robotic systems. Rather than targeting specific tasks, these approaches—such as ROSA, and RAI emphasize systemlevel design, where perception, reasoning, and action modules are cleanly separated and easily composed. Many of these agents are built upon general-purpose LLM frameworks like LangChain, enabling flexible memory, tool integration, and conversational interfaces. Notably, this category closely overlaps with the _Agentic Frameworks_ paradigm discussed in Section III, as these systems rely on structured interfaces through which the LLM can invoke robotic capabilities. 

## V. TOOLKITS FOR AGENTIC PHYSICAL AI 

Early agent systems in artificial intelligence, such as symbolic planners, belief–desire–intention (BDI) architectures, and the SOAR cognitive framework, laid the groundwork for connecting reasoning with action. The advent of deep learning shifted the focus to data-driven methods, and more recently, LLMs have enabled agents to integrate reasoning, perception, and action in naturalistic ways. Toolkits for _agentic physical AI_ now aim to close the loop between high-level reasoning and embodied control, making it possible to deploy agents in robotics and other physical domains. This section surveys the main components of this emerging ecosystem. 

## _A. Large Language Models and Providers_ 

State-of-the-art LLMs form the backbone of agentic systems. Closed-source providers such as OpenAI (GPT-4o), Anthropic (Claude 3.5), and Google DeepMind (Gemini 1.5) offer advanced reasoning and multimodal capabilities, along with integrated tool use. Open-source efforts include Meta (Llama 3.1), Mistral AI (Mixtral MoE), and xAI (Grok). These models differ in openness, context length, and function-calling capabilities, but all increasingly support structured integration with external systems. 

## _B. Tool Calling_ 

While impressive, LLMs originally operated only through isolated textual interfaces limited to their training data, without the ability to directly access real-time information, external tools, or APIs. To bridge this gap, one of the first major steps was function calling, introduced by OpenAI, where models were fine-tuned to recognize when a function should be 

8 

invoked and respond with structured JSON that matched the function’s signature [51]. Over time, this approach evolved into what is now broadly known as tool calling (renamed from function calling), which is supported by most modern LLMs. However, implementations differ across vendors in how JSON structures are defined and handled directly by LLMs. The Model Context Protocol (MCP) builds on this idea by introducing an open, interoperable standard that enables consistent and reliable communication between clients (LLMpowered applications) and servers (e.g., tools). Unlike vendorspecific tool calling, MCP ensures that hosts can access tools, resources, and real-time context updates in a standardized way without constant custom integration work. 

In the MCP, there are three key components: the MCP Server, MCP Client, and MCP Host. The MCP Server is a program that provides context in the form of tools (callable functions or actions), resources (structured data or knowledge), and prompts (predefined templates). A server can define multiple of these and communicate them using the JSONRPC 2.0 protocol, either locally through stdio transport or remotely through streaming HTTP. The MCP Client is a protocol-level component that connects to exactly one server and is responsible for handling this communication, passing the context back to the host. Finally, the MCP Host is any AI application that integrates one or more MCP Clients to extend its capabilities; examples include Claude Desktop, Cursor, VS Code with MCP integrations, and agentic frameworks such as LangChain. 

## _C. Frameworks for Agentic Systems_ 

Several frameworks provide abstractions for building complex, multi-step, and multi-agent workflows. These frameworks vary in their focus (retrieval, orchestration, or collaboration) but share the goal of simplifying agent construction and deployment. In this section, we explore key aspects and highlight the use cases of several prominent frameworks, with more detailed attention to the LangChain and on top of that LangGraph framework, which has gained notable popularity in recent agentic robotics systems. 

_1) LangGraph/LangChain:_ LangGraph is a graph-based framework (nodes and edges) built on top of LangChain. To situate it briefly, LangChain is a modular framework that provides structured components for building tool-integrated and memory-aware agents based on LLMs. While LangChain focuses on modularity, LangGraph introduces a state-machine paradigm and supports conditional, non-linear workflows such as loops and retrievals. This makes it particularly suitable for building robust agent pipelines and even coordinating multiple interacting agents. 

In LangGraph, each _node_ represents a discrete piece of logic—this can be a call to an LLM, a function for data processing, or even another agent—while the _edges_ define the control flow, including conditional branching and iterative loops. Several features are especially relevant for designing agentic physical AI systems: 

- _Pre-built implementations:_ LangGraph provides readyto-use templates for common agent patterns. Examples include: 

- _Single-tool calling ReAct:_ Implements the ReAct pattern, combining reasoning traces with tool use in a structured way. 

- _Supervisor multi-agent system:_ Individual agents are coordinated by a central supervisor agent, which controls all communication flow and task delegation. The supervisor decides which agent to invoke based on the current context and task requirements. 

- _Swarm multi-agent system:_ Agents dynamically hand off control to one another depending on their specializations. The system tracks which agent was last active so that subsequent interactions resume with the same agent, ensuring conversational and task continuity. 

- _MCP adapters:_ The framework integrates with the Model Context Protocol (MCP), making it easier to connect external tools and services in a standardized way. 

- _Human-in-the-Loop capabilities:_ Developers can insert checkpoints where human users review or approve agent outputs before execution continues, ensuring safety and reliability. 

- _Memory:_ LangGraph natively supports short- and longterm memory, enabling agents to retain context across steps or sessions, which is critical for persistent autonomy in physical environments. 

_2) LlamaIndex:_ LlamaIndex specializes in RAG, providing structured ingestion and query pipelines over heterogeneous data sources. For agentic physical AI, this allows agents to ground decisions in sensor logs, spatial maps, or multimodal datasets. It is frequently paired with orchestration frameworks such as LangGraph for more complex workflows. 

_3) CrewAI:_ CrewAI focuses on multi-agent collaboration, where agents are assigned roles and tasks within a coordinated “crew.” This makes it suitable for collaborative problem solving, distributed control, and simulation. 

_4) AutoGen:_ AutoGen (Microsoft) emphasizes conversational multi-agent systems, supporting both AI–AI and AI– human collaboration. Its modular design makes it extensible to embodied AI scenarios, where agents must interact with humans and physical systems in tandem. 

## _D. Domain-specific considerations_ 

Robotic data and control pipelines present unique challenges for agentic integration due to their inherent multimodality and temporal diversity. Typical robotic systems combine heterogeneous data streams (vision, laser ranging, tactile sensing, audio, joint encoders, or radio telemetry) each with distinct payload sizes, update frequencies, and latency tolerances. High-bandwidth modalities such as camera or depth feeds require continuous streaming and compression strategies, while others, like status or event messages, demand reliability and strict quality-of-service guarantees. Designing an agentic layer that can flexibly operate across these heterogeneous data rates and protocols remains nontrivial. Agents must reason over asynchronous information and decide which data to process, summarize, or ignore in real time, often under constraints of compute, bandwidth, and safety. 

9 

Another domain-specific constraint lies in embodiment variability. A general-purpose agent should be capable of interfacing with multiple robotic platforms; even if constrained to mobile agents, at least: mobile bases, mobile manipulators, drones, or legged robots (e.g., quadrupeds or humanoids). Each of these embodiments comes with different control interfaces and sensing configurations. Middlewares such as ROS or ROS 2 already provide abstraction layers, from abstracting hardware drivers with topics, services, and actions, to providing out-of-the-box manipulation (e.g., moveit) or navigation (e.g., nav2) capabilities. However, the degree to which an LLM- or VLM-driven agent can remain at a high level of reasoning depends on the embodiment. While protocol-based and interface-level integrations can remain platform-agnostic, models that generate low-level actions or policies (e.g., VLA or RL-based systems) still face challenges in transferring across morphologies. Generalizing such embodied control requires richer world models and modular skill representations that can decouple reasoning from actuation. 

Finally, many real-world robotic tasks are inherently longhorizon and involve unpredictable interaction with the physical environment. Unlike static API calls, physical actions introduce variable execution times, uncertainties, and potential failure modes. Tasks such as “navigate to gate A42” in an airport, or “deliver this object to the suite in the top floor”, involve navigation through dynamic, human-centric spaces, possibly requiring waiting, replanning, or the use of elevators and constrained corridors. For an agentic autonomy solution, reasoning about such extended temporal dependencies (potentially spanning minutes or hours) requires continuous situational awareness, progress monitoring, and adaptive recovery strategies. These factors underscore that agentic systems in robotics must not only manage data and tools, but also reason about time, uncertainty, and embodiment, bridging symbolic decision-making with the continuous realities of physical interaction. 

## VI. DISCUSSION 

Agentic Embodied AI is a rapidly developing field where research is arguably in its infancy. While embedded policies such as VLAs or BLMs are relatively mature, the approaches to integrating foundation models into existing or new autonomy stacks are still underexplored. Below, we outline some of the key open questions and promising directions for future work. 

## _A. AI Agents, AI Workflows and Agentic AI_ 

The deployment of LLMs across systems with differing levels of autonomy, decision logic, and task scope necessitates a conceptual distinction between AI Workflows, AI Agents, and Agentic AI Systems. These categories differ primarily in how control, reasoning, and coordination are distributed between humans, models, and the surrounding infrastructure. 

AI Workflows operate along predefined, human-engineered paths in which the sequence of tool use and model calls is explicitly programmed. Here, the LLM acts as a component within a deterministic pipeline, executing a bounded 

subtask such as summarization. This approach prioritizes predictability, control, and auditability, making it well-suited for regulated environments or applications requiring reproducible outputs [52]. 

In contrast, AI Agents are systems that delegate control of task execution to the model itself. Rather than following a fixed sequence, the LLM dynamically decides which actions to take: planning, executing, and iterating toward a defined goal. The agent perceives its environment, evaluates progress, and selects subsequent actions such as invoking tools. This autonomy enables agents to tackle open-ended problems that cannot be easily pre-specified in a workflow. However, this flexibility comes at the expense of predictability, interpretability, and verifiability [52], [53]. 

Finally, Agentic AI Systems represent a higher level of organization, in which multiple autonomous agents collaborate, coordinate, and share memory to achieve complex or long-horizon objectives. Rather than focusing on individual problem-solving capabilities, the emphasis shifts to the emergent behaviors that arise from interaction, negotiation, and collective reasoning among agents. This conceptual progression, from isolated task execution toward emergent multiagent organization, is increasingly discussed in the context of robotics and autonomous systems [53]. 

## _B. Embodiment_ 

Embodiment can be understood as the capacity of a cyberphysical system to process information about its physical component. It can be viewed as a spectrum: some systems possess limited awareness of their physical properties, while others exhibit more advanced self-modeling. At the simplest level, this involves reasoning about the system’s own physical capabilities: its actuator modalities or “skills,” as outlined in the Internet of Skills [54]. On the other hand, it has been argued that true embodiment requires a more comprehensive internal model. Duffy and Joue [55] introduced the notion of strong embodiment, describing agents that not only understand their actuator modalities but also use this understanding to explore their environment, reason about it, and infer its physical laws. 

Therefore, embodiment can be understood not only as an agent’s capacity to reason about its own body, but also about the environment in which it operates. It is thus better viewed not as an intrinsic property of the agent, but as a trait emerging from the dynamic coupling between the agent and its environment. Consequently, an agent’s embodiment may be context-dependent: a robot designed to perceive and act within a structured warehouse may lose embodiment when deployed in an open field. 

For this reason, in this work we adopt the broadest possible definition of embodiment when conducting our survey. All systems considered possess some capacity to model and reason about their physical component within their operational context. While this capacity differs in form and degree (ranging from direct sensorimotor feedback to abstract physical modeling) each system can nonetheless be regarded as embodied. This diversity shows that embodiment is not a binary property 

10 

but a spectrum shaped by how agents process information within, and about their environments. 

## _C. Applications to Multi-Robot/agent Systems_ 

In this work, we focus on embodied agentic AI solutions, in contrast to other surveys that explicitly categorize into singleagent and multi-agent approaches [56]. The term multi-agent does not necessarily imply multi-robot; its interpretation varies across frameworks. For instance, in systems such as RAI [11], a single robot may host multiple agents, whereas in orchestration architectures, one agent may control multiple robots. Furthermore, many frameworks adopt a one-to-one mapping between robots and agents [41]. Nonetheless, understanding the distribution of agents among robots remains an important aspect, as it reintroduces the debate between centralized and decentralized coordination architectures. 

A key challenge is the development of general multirobot/agent embodied AI frameworks. While recent progress has largely targeted constrained tasks, current methods struggle with scalability, heterogeneous agent teams, and variable objectives. Extending the principles of single-agent generalist models to multi-agent settings introduces difficulties such as non-stationarity, intricate interactions, and multiple equilibria. Unlike the closed and static scenarios often assumed in research, real-world deployments involve dynamic, uncertain, and adversarial conditions with noisy observations, shifting tasks, and fluid team compositions. Achieving robust performance in such environments requires resilient policies, continual learning, and context-aware reasoning to adapt rapidly to novel agents and evolving tasks. 

Finally, applications across domains highlight both the promise and the challenges of embodied multi-robot/agent AI. Robotics for manufacturing, logistics, and autonomous driving demand scalable coordination and adaptability; education and healthcare require socially appropriate, ethical, and privacypreserving interactions; and defense applications necessitate robustness under adversarial conditions with human oversight. Beyond these, smart cities, simulations, and energy systems call for efficient, trustworthy, and safe agent collectives. Addressing these diverse needs will require progress in multimodal perception, collaborative and social learning, and ethical governance, ensuring that multi-robot embodied AI evolves into a reliable, interpretable, and impactful technology for society. 

## _D. Ethical consideration_ 

Ethical issues arise when considering the deployment of embodied agents with humans: the possibility of physical harm, misinformation, or privacy violations. These are compounded by social threats posed by such systems, such as the rapidly changing labor market, and lack of sufficient policies regarding responsibility [57]. They are said to fail to address the division of obligations between manufacturers of such systems, model providers, and organizations deploying them in the real world. Addressing these distinctions is crucial for responsible development and application of embodied AI systems. However, it comes with a complex set of challenges. 

It could be argued that introducing legislation forcing agentic AI system providers to comply with regulation could lead to a decrease in competition by making it harder for new companies to join the market [58] [59]. Finding a balance between appropriate regulation, while not stifling innovation, is crucial for successful and ethical deployment of AI-driven cyber-physical systems. 

## _E. AI Agents in the Edge-Cloud Continuum_ 

The increasing distribution of computational intelligence across robots, edge nodes, and cloud infrastructures introduces new challenges for embodied agentic AI. Robotic agents often operate in dynamic conditions where compute, storage, and connectivity must be balanced across heterogeneous devices and administrative domains. Agentic systems must therefore reason about where and how to execute perception, reasoning, and planning processes, dynamically orchestrating components in response to context and performance requirements. Distributed and federated approaches have begun to address this by enabling semantic task decomposition, runtime component migration, and adaptive resource selection across the compute continuum [60]–[62]. These methods emphasize low-latency execution for perception at the edge while offloading heavy reasoning or model adaptation to the cloud, supporting a resilient and scalable paradigm for embodied autonomy. As such, the edge–cloud continuum becomes not merely an infrastructure layer but an integral part of the embodied agent’s cognitive architecture. 

## _F. Memory_ 

Long-term and contextually grounded memory remains one of the least mature capabilities in current agentic architectures. Although tool-based integration servers, such as Bagel [63] and rosbag MCP, provide standardized access to past sensor data and execution traces [64], most existing agents still operate over transient, session-bound context windows. The lack of persistent, semantically indexed memory prevents agents from maintaining situational continuity, sharing experience between tasks, or reasoning over past states in real time. Emerging frameworks explore structured and distributed memory abstractions to support multi-session persistence and retrieval across agents [65], [66], yet real-time synchronization and consistency remain open problems. Overcoming these limitations will require live, queryable memory layers capable of bridging symbolic reasoning with embodied experience—enabling agents to continuously learn, adapt, and recontextualize actions across time and embodiment. 

## _G. Continuous data streams_ 

Integrating data streams with LLMs, VLMs, and Embodied AI systems remains an active area of research. 

In robotics, a central challenge lies in handling continuous data streams from sensors such as cameras, LiDAR, and radar. These streams provide real-time sensor input, but conflict with the discrete mode of operation of most LLMs and VLMs. Continuous data must therefore be transformed into suitable 

11 

representations. For example, a 10 Hz video feed cannot be directly used by an LLM which takes more than 0.1 seconds to process an image. That would lead to desynchronization and potential information loss. 

Recent work explores strategies for selecting and summarizing data streams. For example, Hu [67] introduced a method using a multimodal LLM for the selection of frames from a video. Similarly, Lin [68] proposed a keyframe identification model that uses captioning and scoring to preserve context. Such approaches highlight promising directions for aligning continuous perception with discrete reasoning. However, integrating streaming data into embodied AI systems remains an open challenge. 

## _H. World Models_ 

The concept of _world models_ has recently gained significant attention in the field of robotics and artificial intelligence. World models are internal representations that an agent (e.g., a robot) constructs to reason about its environment, predict the consequences of its actions, and plan its behavior. One of the pioneering works on world models is the paper by Ha and Schmidhuber [69], which proposed a framework for building compact, compressed representations of the world using deep neural networks. The authors demonstrated the effectiveness of world models in various reinforcement learning tasks, where the agent learns to navigate and complete tasks in simulated environments. Following the work of Ha and Schmidhuber, several researchers have explored different aspects of world models and their applications in robotics. For a recent survey please see [70]. Recent works are for instance [71], proposing DreamerV3, a general algorithm that outperforms specialized methods across over 150 diverse tasks, or [72], introducing TD-MPC2, a model-based RL algorithm designed for learning generalist world models on large non-curated datasets composed of multiple task domains, embodiments, and action spaces. The authors of [73] present DINO-WM, a method for training visual models by using pretrained DINOv2 embeddings of image frames: once trained, given a target observation, one can directly optimize agent behavior by planning through DINO-WM using model-predictive control (MPC). 

World models can be valuable tools to enhance the robot’s understanding of the environment, more specifically to gauge the consequences/effects of its actions on the environment. Coupled with an exploratory strategy (e.g., an agentic loop) to assess what possible actions could be undertaken to perform a specific task and their predicted effects, the robot can choose to enact the most promising strategies from the world model in the real world, leading to safer and more robust task execution. While a world model is learnt and possibly updated from ”experience”, another similar exploration approach could be implemented by using simulation. 

## _I. Evaluation Metrics_ 

Evaluation metrics for embodied agentic systems can be defined along the Perceive–Reason–Act paradigm. Task performance is often measured through success rate and com- 

pletion time, particularly in multi-stage navigation and manipulation tasks. The efficiency of tool and function definition significantly influences these outcomes, as clear and adaptable tool descriptions improve task execution regardless of the underlying tool-use capabilities of the foundation models. A critical aspect of evaluating physical agentic systems is the level of autonomy, defined as the ability of a system to plan, decide, and act without constant human intervention. Many existing frameworks demonstrate a medium level of autonomy, as they rely on predefined commands, functions, or tool sets. Achieving higher autonomy requires agents to generate their own sub-goals and corresponding actions. In some settings, especially those involving limited human interaction, this trait may be desirable. However, evaluating systems with higher autonomy is much more difficult. 

Systems with a low degree of autonomy, i.e., those which utilize advanced tooling, can be often evaluated through monitoring the order and arguments of the tools. The higher the degree of autonomy, the need arises to evaluate the system through its impact on the environment in which it operates. This can lead to some undesirable behaviors, such as excessive movement, being missed during the evaluation. For example, in a highly autonomous agent responsible for its own path planning, simply checking whether it reached the goal may overlook inefficient or excessive movement. That issue is not present in low-autonomy systems using predefined navigation tools. 

Adaptability is another key factor, reflecting the agent’s ability to generalize across unseen tasks, environments, or robotic embodiments with minimal additional data or modification. Memory consistency and recallability assess how effectively an agent stores, retains, and reuses contextually relevant information, serving as a foundation for stable, context-aware behavior. Other factors, such as safety, transparency, are also essential in evaluating embodied AI agents [74] and have been extensively discussed in recent surveys on agentic AI [75]. 

## VII. CONCLUSION 

This survey reviewed the emerging field of agentic AI in robotics, where large language and vision-language models function as intelligent intermediaries between users and robotic systems. Unlike end-to-end learning approaches, agentic systems preserve the structure of traditional robotics pipelines, using LLMs to translate goals, generate plans, and invoke APIs or tools based on available capabilities. 

We organized the current landscape into two key taxonomic dimensions: model integration patterns, and agent role. Across all dimensions, we included both academic literature and practical systems from the open-source community, or industrial applications. Most of the literature today can be classified under one specific area, e.g., with a focus on either _protocol_ , _interface_ , _orchestration_ , or _embedded_ integration of foundation models. However, there are already a number of works that propose more complex system that span multiple areas. Similarly, from the perspective of agent roles, model-centric agents operate as either orchestration or generalist agents. Therefore, we see significant value in combining different approaches and subsystems to achieve higher degrees of intelligence. 

12 

Embodied or Physical Agentic AI for robotics is still in an early but rapidly evolving stage. Future work will need to address challenges related to grounding, memory, safety, deployment efficiency, and evaluation. As modular agent frameworks continue to improve, we expect increased adoption across industrial and academic robotics, making intelligent interaction with complex systems more accessible, interpretable, and adaptive. 

## REFERENCES 

- [1] R. Firoozi, J. Tucker, S. Tian, A. Majumdar, J. Sun, W. Liu, Y. Zhu, S. Song, A. Kapoor, K. Hausman _et al._ , “Foundation models in robotics: Applications, challenges, and the future,” _The International Journal of Robotics Research_ , vol. 44, no. 5, pp. 701–739, 2025. 

- [2] J. Urain, A. Mandlekar, Y. Du, M. Shafiullah, D. Xu, K. Fragkiadaki, G. Chalvatzaki, and J. Peters, “Deep generative models in robotics: A survey on learning from multimodal demonstrations,” _arXiv preprint arXiv:2408.04380_ , 2024. 

- [3] F. Zeng, W. Gan, Y. Wang, N. Liu, and P. S. Yu, “Large language models for robotics: A survey,” _arXiv preprint arXiv:2311.07226_ , 2023. 

- [4] X. Xiao, J. Liu, Z. Wang, Y. Zhou, Y. Qi, S. Jiang, B. He, and Q. Cheng, “Robot learning in the era of foundation models: A survey,” _Neurocomputing_ , p. 129963, 2025. 

- [5] Y. Kim, D. Kim, J. Choi, J. Park, N. Oh, and D. Park, “A survey on integration of large language models with intelligent robots,” _Intelligent Service Robotics_ , vol. 17, no. 5, pp. 1091–1107, 2024. 

- [6] J. Liang, W. Huang, F. Xia, P. Xu, K. Hausman, B. Ichter, P. Florence, and A. Zeng, “Code as policies: Language model programs for embodied control,” _arXiv preprint arXiv:2209.07753_ , 2022. 

- [7] M. Bojarski, D. Del Testa, D. Dworakowski, B. Firner, B. Flepp, P. Goyal, L. D. Jackel, M. Monfort, U. Muller, J. Zhang _et al._ , “End to end learning for self-driving cars,” _arXiv preprint arXiv:1604.07316_ , 2016. 

- [8] S. H. Vemprala, R. Bonatti, A. Bucker, and A. Kapoor, “Chatgpt for robotics: Design principles and model abilities,” _Ieee Access_ , vol. 12, pp. 55 682–55 696, 2024. 

- [9] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

- [10] R. Royce, M. Kaufmann, J. Becktor, S. Moon, K. Carpenter, K. Pak, A. Towler, R. Thakker, and S. Khattak, “Enabling novel mission operations and interactions with rosa: The robot operating system agent,” in _2025 IEEE Aerospace Conference_ . IEEE, 2025, pp. 1–16. 

- [11] K. Rachwal, M. Majek, B. Boczek, K. Dabrowski, P. Liberadzki, A. Dabrowski, and M. Ganzha, “Rai: Flexible agent framework for embodied ai,” _arXiv preprint arXiv:2505.07532_ , 2025. 

- [12] R. Shah, A. Yu, Y. Zhu, Y. Zhu, and R. Martin-Martin, “Bumble: Unifying reasoning and acting with vision-language models for buildingwide mobile manipulation,” _arXiv preprint arXiv:2410.06237_ , 2024. 

- [13] K. Black, N. Brown, D. Driess, A. Esmail _et al._ , “ _π_ 0: A vision-languageaction flow model for general robot control. corr, abs/2410.24164, 2024. doi: 10.48550,” _arXiv preprint ARXIV.2410.24164_ , 2024. 

- [14] G. R. Team, S. Abeyruwan, J. Ainslie, J.-B. Alayrac, M. G. Arenas, T. Armstrong, A. Balakrishna, R. Baruch, M. Bauza, M. Blokzijl _et al._ , “Gemini robotics: Bringing ai into the physical world,” _arXiv preprint arXiv:2503.20020_ , 2025. 

- [15] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang _et al._ , “Gr00t n1: An open foundation model for generalist humanoid robots,” _arXiv preprint arXiv:2503.14734_ , 2025. 

- [16] Z. Zhou, Y. Zhu, J. Wen, C. Shen, and Y. Xu, “Vision-languageaction model with open-world embodied reasoning from pretrained knowledge,” _arXiv preprint arXiv:2505.21906_ , 2025. 

- [17] OpenMind: https://docs.openmind.org/developing/0 <u>introduction.</u> 

- [18] R. Brooks, “A robust layered control system for a mobile robot,” _IEEE journal on robotics and automation_ , vol. 2, no. 1, pp. 14–23, 2003. 

- [19] P. Sermanet, C. Lynch, Y. Chebotar, J. Hsu, E. Jang, S. Schaal, S. Levine, and G. Brain, “Time-contrastive networks: Self-supervised learning from video,” in _2018 IEEE international conference on robotics and automation (ICRA)_ . IEEE, 2018, pp. 1134–1141. 

- [20] M. Laskin, K. Lee, A. Stooke, L. Pinto, P. Abbeel, and A. Srinivas, “Reinforcement learning with augmented data,” _Advances in neural information processing systems_ , vol. 33, pp. 19 884–19 895, 2020. 

- [21] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao, “React: Synergizing reasoning and acting in language models,” in _International Conference on Learning Representations (ICLR)_ , 2023. 

- [22] ros2ai: https://github.com/fujitatomoya/ros2ai. 

- [23] ROSCribe: https://github.com/RoboCoachTechnologies/ROScribe. 

- [24] ROS-LLM: https://github.com/Auromix/ROS-LLM. 

- [25] ROS-MCP-Server: https://github.com/lpigeon/ros-mcp-server. 

- [26] ROS-MCP-Server by robotmcp: https://github.com/robotmcp/ ros-mcp-server. 

- [27] EmbodiedAgents: https://automatika-robotics.github.io/ embodied-agents/intro.html. 

- [28] M. Ahn, D. Dwibedi, C. Finn, M. G. Arenas, K. Gopalakrishnan, K. Hausman, B. Ichter, A. Irpan, N. Joshi, R. Julian _et al._ , “Autort: Embodied foundation models for large scale orchestration of robotic agents,” _arXiv preprint arXiv:2401.12963_ , 2024. 

- [29] ROS-MCP: https://github.com/Yutarop/ros-mcp. 

- [30] Z. Wu, Y. Zhou, X. Xu, Z. Wang, and H. Yan, “Momanipvla: Transferring vision-language-action models for general mobile manipulation,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 1714–1723. 

- [31] B. Lange, A. Yildiz, M. Arief, S. Khattak, M. Kochenderfer, and G. Georgakis, “General-purpose robotic navigation via lvlm-orchestrated perception, reasoning, and acting,” _arXiv preprint arXiv:2506.17462_ , 2025. 

- [32] D. Sobr´ın-Hidalgo, M. ´A. Gonz´alez-Santamarta, ´A. M. GuerreroHigueras, F. J. Rodr´ıguez-Lera, and V. Matell´an-Olivera, “Enhancing robot explanation capabilities through vision-language models: a preliminary study by interpreting visual inputs for improved human-robot interaction,” _arXiv preprint arXiv:2404.09705_ , 2024. 

- [33] M. A. Gonzalez-Santamarta, https://github.com/mgonzs13/llama <u>ros.</u> 

- [34] HelloRobotInc, https://github.com/hello-robot/stretch <u>ai.</u> 

- [35] M. Buchholz, I. Carlucho, M. Grimaldi, and Y. R. Petillot, “Distributed ai agents for cognitive underwater robot autonomy,” _arXiv preprint arXiv:2507.23735_ , 2025. 

- [36] M. Ahn, A. Brohan, N. Brown, Y. Chebotar, O. Cortes, B. David, C. Finn, C. Fu, K. Gopalakrishnan, K. Hausman _et al._ , “Do as i can, not as i say: Grounding language in robotic affordances,” _arXiv preprint arXiv:2204.01691_ , 2022. 

- [37] Y. Wu, Z. Xiong, Y. Hu, S. S. Iyengar, N. Jiang, A. Bera, L. Tan, and S. Jagannathan, “Selp: Generating safe and efficient task plans for robot agents with large language models,” _arXiv preprint arXiv:2409.19471_ , 2024. 

- [38] C. Rivera, G. Byrd, W. Paul, T. Feldman, M. Booker, E. Holmes, D. Handelman, B. Kemp, A. Badger, A. Schmidt _et al._ , “Conceptagent: Llm-driven precondition grounding and tree search for robust task planning and execution,” _arXiv preprint arXiv:2410.06108_ , 2024. 

- [39] M. Glocker, P. H¨onig, M. Hirschmanner, and M. Vincze, “Llmempowered embodied agent for memory-augmented task planning in household robotics,” _arXiv preprint arXiv:2504.21716_ , 2025. 

- [40] K. Chu, X. Zhao, C. Weber, M. Li, W. Lu, and S. Wermter, “Large language models for orchestrating bimanual robots,” in _2024 IEEERAS 23rd International Conference on Humanoid Robots (Humanoids)_ . IEEE, 2024, pp. 328–334. 

- [41] S. S. Kannan, V. L. Venkatesh, and B.-C. Min, “Smart-llm: Smart multi-agent robot task planning using large language models,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 12 140–12 147. 

- [42] X. Zhang, H. Qin, F. Wang, Y. Dong, and J. Li, “Lamma-p: Generalizable multi-agent long-horizon task allocation and planning with lmdriven pddl planner,” _arXiv preprint arXiv:2409.20560_ , 2024. 

- [43] G. Zhou, Y. Hong, and Q. Wu, “Navgpt: Explicit reasoning in visionand-language navigation with large language models,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 38, no. 7, 2024, pp. 7641–7649. 

- [44] V. S. Dorbala, J. F. Mullen, and D. Manocha, “Can an embodied agent find your “cat-shaped mug”? llm-based zero-shot object navigation,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 5, pp. 4083–4090, 2023. 

- [45] J. Huang, S. Yong, X. Ma, X. Linghu, P. Li, Y. Wang, Q. Li, S.-C. Zhu, B. Jia, and S. Huang, “An embodied generalist agent in 3d world,” _arXiv preprint arXiv:2311.12871_ , 2023. 

- [46] K. Bousmalis, G. Vezzani, D. Rao, C. Devin, A. X. Lee, M. Bauz´a, T. Davchev, Y. Zhou, A. Gupta, A. Raju _et al._ , “Robocat: A selfimproving generalist agent for robotic manipulation,” _arXiv preprint arXiv:2306.11706_ , 2023. 

13 

- [47] H. Bharadhwaj, J. Vakil, M. Sharma, A. Gupta, S. Tulsiani, and V. Kumar, “Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 4788–4795. 

- [48] G. Wang, Y. Xie, Y. Jiang, A. Mandlekar, C. Xiao, Y. Zhu, L. Fan, and A. Anandkumar, “Voyager: An open-ended embodied agent with large language models,” _arXiv preprint arXiv:2305.16291_ , 2023. 

- [49] S. Liu, Y. Li, K. Zhang, Z. Cui, W. Fang, Y. Zheng, T. Zheng, and M. Song, “Odyssey: Empowering minecraft agents with open-world skills,” _arXiv preprint arXiv:2407.15325_ , 2024. 

- [50] Y. Chen, W. Cui, Y. Chen, M. Tan, X. Zhang, J. Liu, H. Li, D. Zhao, and H. Wang, “Robogpt: an llm-based long-term decision-making embodied agent for instruction following tasks,” _IEEE Transactions on Cognitive and Developmental Systems_ , 2025. 

- [51] C. B˘adic˘a, A. B˘adic˘a, M. Ganzha, M. Ivanovi´c, M. Paprzycki, D. Selis¸teanu, and Z. Wrona, “Contemporary agent technology: Llmdriven advancements vs classic multi-agent systems,” _arXiv preprint arXiv:2509.02515_ , 2025. 

- [52] E. Schluntz and B. Zhang. (2024, Dec. 19) Building effective agents. Anthropic PBC. Accessed: YYYY-MM-DD. [Online]. Available: https://www.anthropic.com/engineering/building-effective-agents 

- [53] R. Sapkota, K. Roumeliotis, and M. Karkee, “Ai agents vs. agentic ai: A conceptual taxonomy, applications and challenges. arxiv 2025,” _arXiv preprint arXiv:2505.10468_ . 

- [54] L. Guzman, V. Morellas, and N. Papanikolopoulos, “Robotic embodiment of human-like motor skills via reinforcement learning,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 2, pp. 3711–3717, 2022. 

   - [68] S.-Y. Lin, S. Paul, and C. Chen, “From captions to keyframes: Keyscore for multimodal frame scoring and video-language understanding,” 2025. [Online]. Available: https://arxiv.org/abs/2510.06509 

   - [69] D. Ha and J. Schmidhuber, “World models,” 2018. [Online]. Available: https://zenodo.org/record/1207631 

   - [70] K. Kawaharazuka, T. Matsushima, A. Gambardella, J. Guo, C. Paxton, and A. Zeng, “Real-world robot applications of foundation models: a review,” _Advanced Robotics_ , vol. 38, no. 18, p. 1232–1254, Sep. 2024. [Online]. Available: http://dx.doi.org/10.1080/01691864.2024.2408593 

   - [71] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap, “Mastering diverse domains through world models,” 2024. [Online]. Available: https://arxiv.org/abs/2301.04104 

   - [72] N. Hansen, H. Su, and X. Wang, “Td-mpc2: Scalable, robust world models for continuous control,” 2024. [Online]. Available: https://arxiv.org/abs/2310.16828 

   - [73] G. Zhou, H. Pan, Y. LeCun, and L. Pinto, “Dino-wm: World models on pre-trained visual features enable zero-shot planning,” 2024. [Online]. Available: https://arxiv.org/abs/2411.04983 

   - [74] E. K. Raptis, A. C. Kapoutsis, and E. B. Kosmatopoulos, “Agentic llm-based robotic systems for real-world applications: a review on their agenticness and ethics,” _Frontiers in Robotics and AI_ , vol. 12, p. 1605405, 2025. 

   - [75] A. Bandi, B. Kongari, R. Naguru, S. Pasnoor, and S. V. Vilipala, “The rise of agentic ai: A review of definitions, frameworks, architectures, applications, evaluation metrics, and challenges,” _Future Internet_ , vol. 17, no. 9, p. 404, 2025. 

- [55] B. Duffy and G. Joue, “Intelligent robots: The question of embodiment,” 01 2000. 

- [56] Z. Feng, R. Xue, L. Yuan, Y. Yu, N. Ding, M. Liu, B. Gao, J. Sun, X. Zheng, and G. Wang, “Multi-agent embodied ai: Advances and future directions,” _arXiv preprint arXiv:2505.05108_ , 2025. 

- [57] J. Perlo, A. Robey, F. Barez, L. Floridi, and J. M A´skander,<sup>˘</sup> “Embodied ai: Emerging risks and opportunities for policy action,” _arXiv preprint arXiv:2509.00117_ , 2025. 

- [58] B. Mueller, “How much will the artificial intelligence act cost europe?” Center for Data Innovation, Information Technology and Innovation Foundation, Tech. Rep. July 26, 2021, 2021, estimates the EU AI Act will cost Europe ~~C~~ 31 billion over 5 years, reduce AI investment by 20%, impose up to ~~C~~ 400,000 compliance costs on an SME deploying a high-risk AI system. [Online]. Available: https://itif.org/publications/ 2021/07/26/how-much-will-artificial-intelligence-act-cost-europe/ 

- [59] Department for Science, Innovation and Technology, “Evidence to support the analysis of impacts for artificial intelligence governance,” UK Government, Tech. Rep., March 2023, evidence review underpinning the UK’s AI governance impact analysis. [Online]. Available: https://assets.publishing.service.gov.uk/media/ 64255c0460a35e000c0cb176/evidence <u>to support the analysis of</u> impacts <u>for artifical intelligence governance.pdf</u> 

- [60] D. B. Acharya, P. Gupta, L. He, and J. Morales, “Agentic ai: Autonomous intelligence for complex goals,” _IEEE Access_ , vol. 13, pp. 21 548–21 563, 2025. 

- [61] N. Filinis, K. Mei, A. Ehtesham, and F. Strati, “Edge ai-driven robotic applications in the computing continuum,” _IEEE Internet of Things Magazine_ , 2026, submitted. 

- [62] E. Baccour, M. Chen, and S. K. Das, “Pervasive ai for iot applications: A survey on resource-efficient distributed artificial intelligence,” _IEEE Communications Surveys & Tutorials_ , vol. 24, no. 4, pp. 2366–2418, 2022. 

- [63] Bagel: https://github.com/Extelligence-ai/bagel. 

- [64] L. Fu, S. Salimpour, L. Militano, H. Edelman, J. Pe˜na Queralta, and G. Tofetti, “Rosbag mcp server analyzing robot data with llms for agentic embodied ai applications,” _arXiv preprint_ , 2025. [Online]. Available: https://arxiv.org/abs/2503.09842 

- [65] A. Ehtesham, R. Sapkota, and D. B. Acharya, “A survey of agent interoperability protocols: Model context protocol (mcp), agent communication protocol (acp), agent-to-agent protocol (a2a), and agent network protocol (anp),” _arXiv preprint_ , 2025. [Online]. Available: https://arxiv.org/abs/2504.16736 

- [66] K. Mei, J. Li, and X. Zhang, “Aios: Llm agent operating system,” in _Proceedings of the Conference on Language Modeling (COLM)_ , Vienna, Austria, 2025. 

- [67] K. Hu, F. Gao, X. Nie, P. Zhou, S. Tran, T. Neiman, L. Wang, M. Shah, R. Hamid, B. Yin, and T. Chilimbi, “M-llm based video frame selection for efficient video understanding,” 2025. [Online]. Available: https://arxiv.org/abs/2502.19680 

14 

