---
title: "Deterministic Execution of ROS 2 Applications via Lingua Franca"
date: "2026-06-08"
authors: "Harun Teper; Shaokai Lin; Shulu Li; Edward A. Lee; Jian-Jia Chen"
url: https://arxiv.org/abs/2606.09203
pdf: https://arxiv.org/pdf/2606.09203
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.09203)** / [論文ページ](https://arxiv.org/abs/2606.09203)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Deterministic Execution of ROS 2 Applications via Lingua Franca 

Harun Teper 

TU Dortmund University 

Dortmund, Germany harun.teper@tu-dortmund.de 

Shaokai Lin 

University of California, Berkeley Berkeley, CA, USA shaokai@berkeley.edu 

Shulu Li 

University of California, Berkeley Berkeley, CA, USA shulu@berkeley.edu 

Edward A. Lee 

Jian-Jia Chen 

University of California, Berkeley RWTH Aachen University Berkeley, CA, USA Aachen, Germany eal@berkeley.edu jian-jia.chen@rwth-aachen.de 

**_Abstract_ —The Robot Operating System 2 (ROS 2) is a widely used middleware for robotic systems, characterized by a publishsubscribe (pub-sub) communication mechanism in which computation is structured as callbacks dispatched by ROS 2 executors. Despite its popularity, the pub-sub pattern in ROS 2 is inherently nondeterministic: the order in which these callbacks run is nondeterministic even within a single executor, and distributed deployments add further nondeterminism from the interleaving of messages across nodes and from network latency. Such nondeterminism often leads to concurrency issues and makes it virtually impossible to analyze for safeness and provide guarantees.** 

**We present a framework that is able to convert an unmodified ROS 2 application and run it under Lingua Franca (LF), a coordination language for deterministic execution using logical time, so that the same input always produces the same deterministic execution order. We first describe which ROS 2 features can be executed deterministically under logical time. Such features enable the possibility to establish an automatic conversion framework to extract information from a ROS 2 application and directly convert it into an LF program. The rich features of LF, such as logical-time delays, federated execution across processes, and fault handling, can then be applied to make the ROS 2 application be executed in a deterministic and timing-predictable manner without changing the ROS 2 code. We evaluate the framework on a synthetic example and on the Autoware reference system. We show that the order in which callbacks are executed differs in default ROS 2, while also having end-to-end latencies that vary across executions. In contrast, our LF-controlled ROS 2 system produces a deterministic execution order and consistent end-to-end latencies.** 

## I. INTRODUCTION 

ROS 2 [25] is a widely used middleware for building robotics systems. It uses the publish-subscribe architecture built on the Data Distribution Service (DDS) [24] to enable modular design of distributed systems. ROS 2 has been adopted across different sectors, including autonomous driving, logistics, and industrial automation [22]. Some of these applications are safety-critical, which means they require not only timely but also deterministic behavior. 

The order in which concurrent events happen on a real machine, however, depends on the operating system, the network, and the hardware. Without explicit synchronization, 

that order is nondeterministic, and ROS 2 provides no such synchronization in its execution model. Considerable effort has gone into making the timing of ROS 2 systems more predictable [7]. On the analysis side, Casini et al. [6] gave the first response time analysis for ROS 2 systems, and subsequent work extended this with response time and end-to-end latency analyses [4], [5], [27], [28], [30]–[32]. On the runtime side, custom executors aim to reduce nondeterminism in practice: PiCAS [8] prioritizes callbacks along causal chains, RTeX [19] adds lock-free multithreaded scheduling, and the events executor adopted by Teper et al. [29] enables nonpreemptive fixedand dynamic-priority scheduling on top of a FIFO event queue. These approaches improve predictability, but they do not give the system deterministic execution by construction. 

Determinism by construction has been studied in a rich literature on synchronous and dataflow languages [3], [9], [13], [14], and Lingua Franca (LF) is one such coordination language that has emerged for distributed, concurrent systems. LF separates _logical time_ , the time in which a program reasons about events, from _physical time_ , the wall-clock time of the underlying machine, so that any execution of an LF program produces the same logical-time trace. LF is already used in high-performance robotics middleware research [12] and in early industry exploration for safety-critical automotive orchestration [10]. ROS 2, however, has a large body of robotics code, libraries, and tooling that LF does not, and porting existing ROS 2 systems to LF manually is impractical. 

In this paper, we would like to bridge ROS 2 applications with the well-studied LF execution paradigm so that we can ensure deterministic execution and achieve timing predictability. This leads to the central question: 

_Is it possible to convert ROS 2 applications automatically to LF to enable deterministic execution behavior and strong timing guarantees?_ 

Our vision is to place an unmodified ROS 2 system under the control of the LF runtime, replacing the execution model of ROS 2 and its executor with the runtime coordination of LF, 

enabling deterministic execution by design, while preserving the original code of the ROS 2 system. 

To the best of our knowledge, the central question above has not been addressed in the literature. The Lingua Franca Project provides minimal use cases for ROS 2 that wrap ROS 2-native code and run it under LF [18], but these are small didactic systems with a single publisher and subscriber, far from an automatic conversion of arbitrary ROS 2 applications. 

Furthermore, converting any arbitrary ROS 2 application into LF is impossible, since some system design aspects of ROS 2 cannot be replicated in LF. For example, ROS 2 allows multiple components to send messages to a single message channel, making it impossible for the receiver of said channel to distinguish where the message came from. This design naturally results in nondeterministic execution and timing behavior, already posing troublesome issues for timing analysis, and is also not possible to be mapped to LF. 

As a result, to enable automatic conversion, we have to explore the ROS 2 features that admit deterministic execution and ensure the determinism of a ROS 2 system through Lingua Franca. The result of our solution is a conversion framework that extracts the topology of the original ROS 2 system and generates a runtime instantiation of the system under LF, without modifying any of the original application code. _We plan to release the framework as open source for the community to adopt and build upon._ 

## **Contributions:** We make the following contributions: 

- **Deterministic Subset of ROS 2.** In Section VI, we characterize which ROS 2 features can be executed deterministically under logical time and which types of ROS 2 applications are nondeterministic even under logical time. Combining both, we determine the deterministic subset of ROS 2 features that we can run deterministically. Such characterizations are fundamental to the research question, since it is impossible to enable deterministic and timing-predictable execution if the original semantics of the ROS 2 application are naturally unpredictable. 

- **Automatic Conversion and LF-controlled Runtime for ROS 2.** The features of the deterministic subset of ROS 2 enable the possibility to extract information from a ROS 2 application and directly convert it into an LF program. Towards this, in Section VII, we establish the first automatic conversion framework which extracts the runtime topology of a ROS 2 application from its source code and emits an LF program that can run the unmodified ROS 2 application code in a deterministic and timing-predictable manner. We specify how the LF runtime controls the execution of the ROS 2 application and how communication is handled. To the best of our knowledge, this is the first framework in this direction. 

- **Semantic Enrichment.** After the automatic conversion, we can adopt the rich features of LF, such as logicaltime delays, federated execution across processes, fault handling, etc., and add them to the converted LF program without modifying the original ROS 2 code. In Section VIII, we focus on the logical-time delays that allow 

us to run the system under different latency specifications, and we specify how we use federated execution to enable the concurrent execution of distributed systems in a deterministic and timing-predictable manner. 

- **Evaluation.** We demonstrate the effectiveness of the framework in enabling deterministic execution and timing predictability for ROS 2 applications. In Section IX, we apply the framework to a synthetic example system and to the Autoware reference system, showing deterministic execution and static ordering of callbacks, a reduction in end-to-end latency variability compared to stock ROS 2, and consistent timer execution behavior. 

**Paper Organization.** In addition to the above technical contributions, Section II introduces ROS 2, and Section III introduces Lingua Franca and its logical-time determinism. Section IV contrasts the two execution models on a running example, leading to the problem statement in Section V. 

## II. ROS 2 

In this section, we introduce ROS 2 [7], [25], including its basic components and executor model. 

A ROS 2 system consists of a set of _nodes_ , each of which represents one system component. Each node implements its functionality through a set of _callbacks_ , which are methods of the node class. ROS 2 then provides a set of APIs to define how callbacks are triggered, specifying the task types of the system. There are two types of tasks, time-triggered and event-triggered. Timers are time-triggered tasks and periodically activated. Tasks like subscriptions are event-triggered and activated by the arrival of messages on the system’s communication channels. 

For the communication, ROS 2 nodes use _Data Distribution Services_ (DDS), a publish-subscribe middleware. ROS 2 defines three forms of communication through DDS: _topics_ , _services_ , and _actions_ . 

A _topic_ is a publish-subscribe channel. Any node can define a publisher on a topic, and any callback of that node can use that publisher to send messages. Subscriptions are defined given a topic, a callback, and a fixed size for its FIFO queue. When a message is published on a topic, it is broadcast to all subscriptions of that topic, triggering their callbacks. When a subscriber’s callback is executed, it processes the oldest message in its FIFO queue. 

In order to run a ROS 2 system, the user creates one or more _executors_ , which are responsible for scheduling and executing callbacks. Each node and its callbacks are assigned to exactly one executor, which then manages the execution order of the callbacks that are assigned to it. 

Figure 1 shows the running example used throughout the paper. It contains four nodes, _A_ , _B_ , _C_ , and _D_ , arranged in a diamond and communicating through four topics, /alpha, /beta, /gamma, and /delta. Node _A_ has a timer with period _T_ that triggers a callback _cA_ that publishes messages on /alpha and /beta. Node _B_ has a callback _cB_ that subscribes to /alpha and publishes on /gamma. Node _C_ has a callback _cC_ that subscribes to /beta and publishes 

2 


Figure 1: Running example as a ROS 2 system. 

on /delta. Node _D_ has two callbacks, _cD_ 1 subscribed to /gamma and _cD_ 2 subscribed to /delta, joining the two paths _A → B → D_ and _A → C → D_ . 

## III. LINGUA FRANCA 

Lingua Franca (LF) [20], [23] is a coordination language for deterministic concurrent systems. An LF program describes the structure of a system: which components exist, what triggers them, and how they connect. Underpinning LF is the reactor model [21]: events, such as the execution of system functions in the program, are ordered by _logical time_ rather than wall-clock time, which is what lets LF impose a deterministic order on concurrent execution. Section III-A introduces the structural building blocks of an LF program, and Section III-B introduces logical time and the resulting determinism guarantee. We explain LF by example, using the corresponding system in Figure 2 (as an LF copycat of Figure 1) as reference. 

## _A. Reactors, Reactions, and Ports_ 

An LF program specifies the interactions between concurrent components called _reactors_ . Each reactor is a state machine with a fixed set of input ports, output ports, state variables, and reactions. Reactions are the functions that specify the computation and functionality in an LF system. Inside of a reactor, reactions can read from and write to the state variables, which encapsulate the state of the reactor. Reactors can communicate with other reactors only via emitting events on output ports, which then trigger the reactions of the connected input ports of other reactors. A complete LF program is built by composition. A top-level reactor instantiates child reactors and wires their input and output ports together, forming the program’s dataflow graph. 

In our example, illustrated before in Figure 1, there are four reactors _A_ , _B_ , _C_ , and _D_ , with a connection from _A_ to _B_ via the port alpha, a connection from _A_ to _C_ via the port beta, a connection from _B_ to _D_ via the port gamma, and a connection from _C_ to _D_ via the port delta. 

An _event_ can be emitted to trigger reactions. There are four kinds of event sources in LF. First, messages carried by input/output ports. Second, LF _timers_ , which are periodic event sources declared in a reactor that are triggered at fixed periods. Third, the built-in triggers startup and shutdown of a reactor, which are triggered once at the first and last moment of the program running. A fourth source, _actions_ , is introduced together with logical time in Section III-B, together with the time units for each connection in the dataflow graph. 


Figure 2: The running example expressed in LF. 

Reactor _A_ has one reaction that is triggered by a timer and writes to the output ports alpha and beta. Reactor _B_ and _C_ have one reaction each that is triggered by the input ports alpha and beta respectively, and write to the output port gamma and delta, respectively. Reactor _D_ has two reactions, one triggered by the input port gamma and the other triggered by the input port delta. 

## _B. Logical Time and Determinism_ 

Logical time is the basis for all causal reasoning in an LF program, enabling the deterministic execution of LF programs. Instead of relying on the physical clock of the system, a central LF runtime maintains a logical clock and advances it according to the events in the program. The logical time of LF is defined using tags, which are pairs ( _t, m_ ), where _t_ is a logical timestamp and _m_ is a microstep index. For an LF system, tags are totally ordered, i.e., for any two tags _g_ = ( _t, m_ ) and _g_<sup>_′_</sup> = ( _t_<sup>_′_</sup> _, m_<sup>_′_</sup> ), _g ≺ g_<sup>_′_</sup> iff _t < t_<sup>_′_</sup> , or _t_ = _t_<sup>_′_</sup> and _m < m_<sup>_′_</sup> . Every event in an LF program carries a tag, whether it is an event generated by an output port, by a timer, or an action. A reaction triggered at tag _g_ reads only the values present at _g_ and writes outputs at _g_ or later. 

An _action_ is a reactor element which can be used to trigger reactions at a tag determined by the runtime. A _logical action_ is used to add a logical delay to the program. The runtime computes the trigger’s tag as the current tag plus a programmerspecified delay _d_ , and the trigger occurs deterministically at that tag. A delay of zero at logical time _t_ with a microstep _m_ does not produce the same tag but a tag at the next microstep _m_ +1. Hence, chains of zero-delay events are ordered without logical time advancing. In our example, each connection in the dataflow graph carries a delay through _after delays_ , an equivalent form of logical actions that delay events sent over connections. Each of the four connections carries a logical delay of 1 ms, so that the two paths _A → B → D_ and _A → C → D_ accumulate the same total delay and their events arrive at _D_ at the same logical tag. 

The logical time is independent of the physical execution times of reactions by default, forming a well-defined, deterministic timeline of events. To guarantee determinism for the execution order of multiple reactions inside a reactor, Lingua Franca requires a predetermined static order of all reactions inside of a reactor. Thus, reactions that are part of the same reactor are run sequentially ( _e.g.,_ in Figure 2, the two reactions of reactor _D_ execute in their static order when both are triggered), while reactions that are part of different reactors are 

3 

independent of each other when run at the same logical time, and can be run concurrently. Thus, LF derives a determinism guarantee that holds for every program, providing a static order of events if the program is run with the same inputs. 

For time-sensitive systems, logical time can be used as timing specifications for the system’s physical-time behavior. In this setting, the logical-time delays introduced by logical actions can represent the execution times, network delays, and deadlines of the system. The LF runtime then only processes events for which the current physical time is greater than the time value of the logical time tag, i.e., logical time tries to catch up to the physical time. 

There is also the possibility to use physical connections in LF, which enables a downstream component to re-timestamp incoming events using the physical time of the system. This makes the logical timestamps depend on the physical latencies of the system, resulting in nondeterministic execution, as the order of events would depend on the timing of message arrivals, function execution times, and timer firings. 

**Concurrency and federated execution.** The LF runtime is responsible for the execution of reactions, using worker threads to run reactions concurrently whenever possible. In LF, all reactions inside a reactor are guaranteed to be executed sequentially, while reactions of different reactors that are triggered at the same logical time can be executed concurrently, as they are independent of each other. 

When extending LF to multi-machine distributed execution, the LF runtime can be implemented as a _federated_ runtime [2]. Under federation, each machine runs a separate _federate_ of the program, which controls a subset of the system’s reactors. The federates are coordinated by the LF Runtime Infrastructure (RTI) [2], which maintains the global logical time and ensures the determinism guarantee across machines. Each federate advances its local logical time independently, but before processing events at tag _g_ it must receive a _Tag Advance Grant_ from the RTI, which guarantees that no upstream federate will produce events at tags _≤ g_ in the future. The determinism guarantee therefore extends from the single-machine setting to the federated setting. 

## IV. ROS 2 VS. LF 

We now use the running example from Figures 1 and 2 to illustrate the similarities between the two systems and which components of ROS 2 and LF correspond to each other, as well as the differences in their execution models and the resulting nondeterminism in ROS 2 that LF closes by design. 

Each ROS 2 node corresponds to one reactor in LF, the callbacks correspond to the reactions, and each topic connection corresponds to a port connection in LF. Furthermore, both ROS 2 and LF provide a timer to periodically activate the callbacks and reactions, respectively. The main difference is that the ROS 2 system has no logical time components, which are present in the LF system as after delays at each port connection. In the following, we explain how the actual execution of the systems may differ. 

We start with the ROS 2 system. We assume a deployment where each node runs independently in its own process and they communicate over a network via DDS. Node _A_ ’s timer activates after its period elapses, executing the callback _cA_ which publishes on topics /alpha (to B) and /beta (to C). B’s callback _cB_ receives the message on topic /alpha and publishes on topic /gamma to D, where _cD_ 1 receives it. C’s callback _cC_ receives the message on topic /beta and publishes on topic /delta to D, where _cD_ 2 receives it. 

After the callback of node _A_ publishes the messages, the order in which the callbacks _cB_ , _cC_ , _cD_ 1, and _cD_ 2 are executed is not deterministic, and depends on the execution times and network latencies of each component. For example, if the path through _B_ finishes before the path through _C_ , then /gamma arrives at D before /delta, even if the developers intend the message of /delta to be processed before the message of /gamma or vice versa. 

Next, we move to the LF system, which uses logical-time delays and static ordering inside of the reactor _D_ to provide deterministic execution at every step. First, after the timer generates an event at the logical time tag ( _t, m_ ), the reaction of reactor _A_ is executed. This produces two output events, one on port alpha and one on port beta, both at the same tag ( _t, m_ ). Next, due to the after delay of 1 ms on the connections from _A_ , reactors _B_ and _C_ receive their inputs at the tag ( _t_ +1 ms _, m_ ), and each reactor produces an output on gamma and delta, respectively, at the same tag. Finally, the two reactions of reactor _D_ are triggered by the outputs of the after delays on gamma and delta, being activated at the same tag ( _t_ + 2 ms _, m_ ). Due to the static ordering of reactions in reactor _D_ , the reaction triggered by gamma is executed before the reaction triggered by delta, regardless of the physical execution times and network latencies. After 100 ms, the timer of reactor _A_ generates another event at tag ( _t_ + 100 ms _, m_ ), and the same sequence of reactions is executed again, with the same order of execution for the reactions of reactor _D_ . 

LF produces a deterministic execution order of reactions, and the differences between ROS 2 and LF in our running example are as follows: 

- **Logical time.** LF uses logical time to order events, while ROS 2 relies on physical time, which can lead to nondeterministic execution order due to varying execution times and network latencies. 

- **Static ordering.** LF requires a static order of reactions within the same reactor, which ensures a deterministic execution order for reactions triggered at the same logical time. While ROS 2 provides a fixed-priority order of callbacks for each node, their execution order is heavily dependent on the timing of message arrivals and timer firings, leading to nondeterministic execution ordering. 

- **Determinism guarantee.** LF provides a determinism guarantee that holds for every program, ensuring that the same input produces the same execution trace, while ROS 2 does not provide such a guarantee, resulting in different execution traces even with the same inputs. 

4 

## V. PROBLEM DEFINITION 

After demonstrating the differences between ROS 2 and LF and the causes of nondeterminism in ROS 2, we can now turn towards the problem of creating a deterministic version of a ROS 2 system by using LF. For this, we first restate the previous work on the deterministic execution of ROS 2 systems and the use of LF for ROS 2 systems, and then we define the problem we want to solve in this paper. 

Existing work by Bateni et al. [2] demonstrates the shortcomings of ROS 2 that are caused by its nondeterministic behavior. Specifically, they investigate the autonomous driving software stack Autoware.Auto [11], which is built on ROS 2, and observe dangerous out-of-order state sequences that can lead to undefined system behavior and bad data alignment. First, for multiple data streams that are published from the same component, the order in which other components receive the messages is not fixed. In Autoware.Auto, one component could receive a velocity signal that does not match the direction in which the car plans to drive, resulting in undefined behavior. Second, for multi-node systems, the alignment of data from multiple sources is not guaranteed, i.e., if there is a "stop and reverse" signal, and the reverse operation is received and processed without coming to a stop first, then the car may end up trying to reverse at high speed, which can lead to dangerous situations. To solve this issue, they extracted the application code of Autoware.Auto and re-implemented the components in Lingua Franca manually, demonstrating that the aforementioned issues can be resolved through deterministic execution. However, this manual conversion is not scalable and does not preserve the original code, making it incompatible with the existing ROS 2 ecosystem. 

Another line of work by Sagmeister et al. [26] presents a custom ROS 2 executor, called RSLCPP, that enables deterministic execution for single-executor systems. RSLCPP aggregates all nodes into a single process and drives them through a custom event loop under simulation time, a logical time control mechanism in ROS 2, enabling deterministic execution. It first determines which timer functions are ready to execute, and then executes all timer functions and all downstream functions that are triggered by the messages sent by the timer functions. This is repeated until there are no more functions to execute, at which point the logical time is advanced to the next point in time when a timer function is ready to execute. This approach achieves determinism in ROS 2, but it comes with significant structural restrictions. First, it is restricted to a single process, since the coordination between multiple processes under simulation time poses significant challenges regarding the synchronization of logical time across processes and the ordering of events across processes. Second, the authors cut off communication to all components that are not run by the RSLCPP executor, since those could introduce nondeterminism through their interactions with the components run by RSLCPP. 

Interestingly, the authors of RSLCPP also identify that certain design patterns of ROS 2 systems cannot be included 

in their approach, such as blocking functions, which can cause the entire system to stall and thus break the logical time control of the RSLCPP executor. Furthermore, they also explore and implement the idea of delay modeling for execution times of callbacks, which introduces logical time offsets for the callback execution. This allows them to analyze the system behavior under varying latency conditions, while staying independent of the actual runtimes of the functions. 

These works demonstrate the importance of deterministic execution for ROS 2 systems, and the potential of LF to achieve it. However, they are limited regarding their usability, expressiveness, and compatibility with the existing ROS 2 ecosystem. In order to bring deterministic execution to ROS 2, we aim to answer the following questions: 

- **Q1.** _Which ROS 2 features admit deterministic execution, and which cannot?_ Section VI defines the deterministic subset of ROS 2 and the features that fall outside it. 

- **Q2.** _Given a ROS 2 system built entirely from the deterministic subset of ROS 2, can we construct the corresponding LF program automatically from the source?_ Section VII and the Appendix answer this with an extraction-and-generation pipeline that produces an LF program running the unmodified ROS 2 code. 

- **Q3.** _What execution-time semantics can be added and adjusted through LF to the converted system on top of deterministic callback ordering?_ Section VIII details the LF features the converted system may use and their effect on its behavior. 

## VI. DETERMINISTIC SUBSET OF ROS 2 

In this section, we characterize the subset of ROS 2 that admits deterministic execution. For this, we first discuss what currently prevents ROS 2 from coordinating the execution of its components in a deterministic way, and then we explain what is needed to enable determinism, and which parts of ROS 2 cannot be included in the deterministic subset. 

## _A. Nondeterminism in ROS 2_ 

ROS 2 systems are nondeterministic by design in (at least) three identifiable ways. 

**(A) Callback execution ordering.** The execution of callbacks in ROS 2 solely depends on the elapsing of timer periods and the arrival timing of messages. When several callbacks arrive at roughly the same time, the ROS 2 executor simply starts executing as soon as the first callback arrives and is ready, resulting in nondeterminism. 

**(B) Multi-component coordination.** For a system with multiple components, the sequence in which those components are executed and how data propagates through the system depends on the execution times and network latencies, causing nondeterminism in the order of execution across components and the alignment of data from different components. The discussion in Section IV already demonstrates this, where we have two different data paths that arrive at a final component, whose execution order depends on when the data arrives, resulting in nondeterministic behavior. 

5 

**(C) Unsynchronized timers.** ROS 2 timers should be executed periodically. However, two problems arise due to the design of ROS 2 timers. (i) Their behavior depends on the execution times of other callbacks, which can delay the timer execution due to the nonpreemptive scheduling behavior of ROS 2. (ii) For multiple components, there is no mechanism to synchronize timers or control the offset at which they execute relative to one another. For example, if there are two timers with the same period, ROS 2 provides no mechanism to control their offsets. Instead, the offset simply depends on the timing of when the timers are created, which depends on startup times and system delays, causing misaligned timer executions. 

The common cause underlying (A), (B), and (C) is that ROS 2 ties scheduling decisions to physical time. Callback ordering depends on which message a thread picks up first, multi-component coordination depends on execution times and network latencies, and timer offsets depend on startup delays. A scheduler that advances time independently of how fast the hardware runs and that fixes the order of simultaneous events at the program level would remove all three sources at once. 

## _B. Determinism via Logical Time_ 

Determinism requires two concepts that ROS 2 lacks by default. The first is a discrete time model independent of the physical clock, so that the schedule is a property of the program rather than of the hardware running it. The second is a deterministic ordering rule for events that share an instant in that time model. As shown by Sagmeister et al. [26], the simulation time of ROS 2 provides a discrete clock that components can follow. However, their solution did not yet resolve coordinating multiple components and arbitrating what should run when multiple events occur simultaneously. 

Lingua Franca supplies both concepts needed for deterministic execution directly through logical time, as described in Section III-B. Using tags ( _t, m_ ), LF ensures a total order of events across the entire program, and advances time only when every reaction at the current tag has produced its outputs. This decouples the schedule from physical execution times so that an LF program always has the same sequence of tags regardless of how fast the hardware happens to be. At each tag, reactions inside a reactor execute in a static order declared in the reactor, while reactions in different reactors at the same tag are unordered and may run concurrently. However, once events with the same tag from different components arrive at the same reactor, the static order of reactions inside that reactor determines the execution order of those events. This enables developers to control both the order of events inside a component, as well as the order in which data from different components is processed. 

Logical time also serves as a means of modeling timesensitive systems. Logical-time delays on connections ( _after delays_ in LF) can stand for execution times, network latencies, and deadlines, making the runtime only advance time once the corresponding physical time has elapsed. This way, the schedule remains a property of the program rather than of the hardware, even when the program describes real-time behavior. 

Under this model, the three sources from Section VI-A dissolve. (A) Reaction order inside a reactor is statically declared, i.e., two callbacks on the same node execute in the order the source defines. (B) Tag-ordered delivery replaces latency-dependent arrival of events. Thus, all components wait for the logical clock rather than for the wall-clock to schedule callbacks, making coordination deterministic across components. (C) Two logical timers with the same nominal period fire at the same sequence of tags throughout the program. Their relative offset can be configured and is fixed, making them deterministic by design. 

We can define the deterministic subset of ROS 2 as the set of ROS 2 systems that only use the features which admit deterministic execution under a logical-time scheduler. 

## _C. Nondeterminism Even under Logical Time_ 

Some ROS 2 features remain nondeterministic even under a logical-time scheduler, since ROS 2 provides a lot of freedom regarding the system design. In the following, we briefly present some of the features that can be used in ROS 2 but cannot be included in the deterministic subset. To the best of our knowledge, those features have not been included in any prior studies on real-time systems and ROS 2, since they introduce behaviors that are difficult to analyze. 

- **Multiple publishers on one topic.** When multiple DDS publishers share a topic, the order in which their messages arrive at a subscriber depends on the execution order and network delay of the message senders. For example, take two publishers _p_ 1 _, p_ 2 on topic /state and one subscriber _s_ on the same topic, where each publisher publishes at period _T_ = 100 ms. At the subscriber, the delivery sequence may be ( _p_ 1 _, p_ 2 _, p_ 1 _, p_ 2 _, . . ._ ) on one run and ( _p_ 2 _, p_ 1 _, p_ 2 _, p_ 1 _, . . ._ ) on another, depending on OS scheduling and network load. As ROS 2 uses a FIFO queue for subscriptions, there is no way to control in which order the messages in the buffer are processed. Thus, the order of messages from multiple publishers on the same topic is nondeterministic, and we restrict ourselves to systems where each topic has at most one publisher. This is also a common assumption in existing ROS 2 analyses, which either assume a DAG structure or at most one publisher per subscription [7]. 

- **Blocking service clients.** ROS 2 callbacks are intended to be non-blocking functions. However, if developers use blocking functions inside their callbacks, for example by calling a service client synchronously, the calling executor thread stalls until the response arrives, preventing the advancement of logical time, and stalling the complete system. This was also excluded by Sagmeister et al. [26] for deterministic execution. 

- **Dynamic system structure.** The structure of a ROS 2 system can change at runtime in ways that are not predetermined. This contradicts the static structure of the underlying reactor model of LF. Existing work on ROS 2 systems assumes that the system and the resulting model are fixed and do not change at runtime [7]. 

6 

## VII. LF-BASED EXECUTION OF ROS 2 SYSTEMS 

After determining the set of features that admit deterministic execution, we now turn to the problem of running a ROS 2 system using Lingua Franca, and how we can enable LFbased execution of ROS 2 systems without modifying the original application code. For this, we first present how we convert a ROS 2 system into an LF program automatically, and how the generated program preserves the behavior of the original system while providing deterministic execution. Then, we present how we integrate the LF runtime to control the execution of ROS 2-native code without any changes, and how we handle communication for data transport and scheduling. 

## _A. Automatic Conversion of ROS 2 to LF_ 

The first part is the automatic conversion of a ROS 2 system into an LF program. For this, we have built a tool that reads the source code the user provides, and extracts a static system graph that captures every node, callback, timer, publisher, subscription, and topic connection. It extracts the information from the launch files of the ROS 2 system, which specify which nodes are part of the system and what parameters are used. Furthermore, we use static code analysis for the C++ source code of each node, which provides the details of the callbacks and what functions they call, such as publish and subscribe functions, and what variables they write to and read from. Finally, we also extract the CMake metadata of a built ROS 2 workspace, which provides information about how the nodes are built and connected together. The extracted graph captures the structure of the system, the callbacks and their interactions, and how the system is built and connected together, which are all necessary for the conversion to LF. 

From the graph, the tool emits .lf source files that mirror the structure of the original system. For example, every node is a reactor, every callback a reaction, and all topic connections are port connections in the generated LF program. The LF runtime can then use the LF program to determine the order for the execution of the callbacks. Importantly, the generated program preserves the callbacks of the original ROS 2 program, their connections, but adds the possibility to control their execution order using logical time. 

Please note that this tool may not successfully convert every system, as described in Section VI-C, but it can convert any system that is built using the deterministic subset of ROS 2. The Appendix describes the framework in detail. 

## _B. Lingua Franca Runtime for ROS 2_ 

Next, we present how to integrate the LF runtime to run ROS 2-native code using the LF runtime instead of the ROS 2 executor. For this, we consider two main designs, either (1) to run the original callbacks in a ROS 2 executor that coordinates with the LF runtime, or (2) to run the callbacks directly using the LF runtime. 

For option (1), this would entail that there are both LF processes and ROS 2 processes running together, and the LF runtime would have to coordinate with the ROS 2 executors when to execute which callbacks. This coordination between 

the processes poses great challenges for the deterministic execution of the system. First, it would still rely on ROS 2 executors running the callbacks, which would require changes to their scheduling behavior to control the execution order and make it deterministic. Second, the LF runtime would need to receive updates from the executors to know when the callbacks are executed and when they are done. This would require additional communication and synchronization to guarantee deterministic execution. 

Option (2) directly runs the original callbacks using the LF runtime. This design is simpler, since there is only one runtime that is processing everything, making it possible to directly execute the callbacks without needing to coordinate with a separate ROS 2 executor. Furthermore, concurrency in the program is directly handled by the LF runtime, which automatically decides which callbacks can run simultaneously. Thus, we opt for this option in our final design. 

We note that for Option (2), the LF runtime creates one executor instance to store references of all system nodes and their callbacks. Importantly, that executor is not running at all and does not control any part of the execution of callbacks. The LF runtime uses the executor and a binding function to directly call and execute the unmodified ROS 2 callbacks. 

## _C. Communication and Coordination_ 

To run the ROS 2 system under LF control, we need to manage the communication between the components of the system. There are two types of communication we need to consider. First, the data transport between the components, which is originally handled by DDS in the ROS 2 system. Second, the event transport between the components in the LF program, which generates the events that are used to ensure that the execution order of the callbacks is deterministic and follows the logical time semantics of LF. 

For the data transport, since we do not want to modify any application code, we leave the ROS 2 callbacks untouched. Therefore, they still exchange data with other components via DDS. Furthermore, this design preserves the ability for data to be received by ROS 2 components that are not controlled by LF, e.g., debugging, data logging, and visualization tools that are part of the ROS 2 ecosystem, but do not necessarily need to be run in a deterministic way. 

For the event transport, we mirror the structure of the original system in the generated LF program, including the connections between reactions. These connections then use dummy LF events that are needed only to encode the corresponding logical times to control the deterministic ordering of the system. The event messages are minimal, so they have negligible overhead. 

## VIII. ADDING LF SEMANTICS ON TOP 

Once a ROS 2 system is realized under the LF runtime, the runtime can enforce execution-time semantics that ROS 2 has no equivalence for, such as logical-time delays, custom event ordering, and fault handling. In the following, we detail how we augment the converted system with some LF semantics and discuss how they affect the system behavior. 

7 

## _A. After Delays and Logical Actions_ 

Each connection in the generated LF program may carry a logical-time delay (also known as an after delay) that represents the time that passes for execution and network operations. We use the connections between ports to insert those delays, representing the time for the callback to run, and the DDS message to pass from the publisher to the subscription. Just like in RSLCPP [26], the delays allow _defining_ the system behavior under varying latency conditions. Through the logical delays, system timing is a first-class, statically configurable property of the program rather than just an observed quantity at runtime. 

For the choice of the delays, different approaches are viable, depending on whether consistency (i.e., ensuring that the system agrees on the shared information) or availability (i.e., ensuring that the system reacts in time when some data is not available) is more important for the system, as described by the CAL theorem ( **c** onsistency, **a** vailability, **l** atency) [15], [16]. 

When ensuring strong consistency, as a first option, one would not set a logical delay to the connection, rendering the upstream sending event and the downstream receiving event logically instantaneous. When the downstream reaction is invoked, the reaction blocks until the underlying payload is delivered over DDS. With the absence of a logical delay, when the upstream component sends a message at timestamp _t_ , the downstream component cannot process its internal events with timestamps greater than _t_ . Thus the downstream component moves in sync with the upstream component and always agrees on the shared data value at the _same_ timestamp _t_ regardless of the physical latencies incurred, achieving strong consistency. 

A second option favoring strong availability would use a _physical connection_ , which enables the downstream component to re-timestamp an incoming message using its physical clock, making the timing of the system dependent on the physical latencies strictly. By replacing the sending timestamp with the receiving component’s physical clock value, the physical connection removes the monotonicity constraint of the messages sent, effectively falling back to the pub/sub semantics of ROS 2, which delivers maximum availability. 

A third option landing a trade-off between the two extremes is to set the logical delay to the maximum observed latency between the upstream and the downstream components. This produces schedules whose logical time is guaranteed to be no faster than the physical time, resulting in behavior where the upstream and the downstream suffer _bounded_ inconsistency, while preserving some degree of availability. 

Yet another option is to set the latencies to the mean observed latency, which produces schedules that are faster than the physical time in average, but can lead to some messages being late. Through LF, one can then detect late messages, and add custom fault handling mechanisms, such as warnings, recovery code, or even stopping the program, without modifying the original ROS 2 code. 

In total, the choice of the logical delays affects the logical time steps of events and thus also the physical time it takes to process data along the tasks. Furthermore, the logical-time 

delays can be used to extend the semantics of the system with custom fault handling for late messages, without modifying the original code. 

## _B. Federated Coordination_ 

As ROS 2 systems are distributed, we employ LF’s federated execution model to coordinate the execution of multiple components across processes and machines. Federation allows multiple LF programs, called federates, to run concurrently and coordinate their execution through a shared logical time. The federates communicate through the LF Runtime Infrastructure (RTI) [2], which ensures that the logical time of each federate advances in a way that respects causality across the entire system. As a result, the use of federation extends the determinism guarantee from a single process to a distributed multi-process deployment. 

## IX. EVALUATION 

We apply our automatic conversion framework to two ROS 2 systems to run them using the LF runtime, showing that the converted systems have deterministic execution order of callbacks, consistent end-to-end latencies, and consistent timer execution behaviors. 

The first system is the Autoware reference system [1], a synthetic benchmark that replicates the autonomous driving pipeline of Autoware [11], including 24 nodes, 23 topics, and 39 causal connections spanning perception, localization, planning, and control. The second system is our running example based on Figure 1, which we use to demonstrate the effects of different logical-time delays on the execution behavior, and the trade-offs between consistency and availability. 

## _A. Setup_ 

Experiments are run on ROS 2 Jazzy in a Docker container on an Ubuntu 22 _._ 04 host with Linux kernel 6 _._ 8, using an AMD Ryzen 9 5900X (12 cores / 24 threads), and 32 GB of RAM. For the native ROS 2 execution, all nodes are launched as separate processes using the default SingleThreadedExecutor. For the DDS communication, we use the default rmw_fastrtps_cpp implementation. The LF-based execution uses Lingua Franca 0 _._ 12 _._ 1 [17]. We use ros2_tracing to capture ROS 2 tracepoints, including the start times of callbacks to reconstruct per-callback invocations and their causal ordering. We run each experiment configuration twenty times for 60 s per run. _We intend to release the source of the conversion framework, the two systems under test, and the experiment scripts._ 

## _B. Autoware reference system_ 

The Autoware reference system includes 24 nodes that run as separate processes communicating over DDS, so nondeterminism from DDS arrival timing, executor races, and timer phase differences is expected to occur. We focus on the full LiDAR pipeline [1], in which ten nodes process data originating from a LiDAR sensor to produce control signals for the actuators of the vehicle. 

8 

Table I: Autoware reference system: per-runtime metrics, _N_ = 20 runs of 60 s each, over the full run and over the steady state. 

|_Metric_|_Default ROS 2_|_LF runtime_|
|---|---|---|
|Pair order drift across runs|up to 100%|0%|
|Pairs with _>_10% order drift|12 / 15|0 / 15|
|_Full_ 60_s run_|||
|E2E mean [ms] (per run)|5.4 – 93.6|100.8 – 100.9|
|E2E std [ms] (per run)|15.4 – 130.6|0.22 – 0.41|
|E2E p99 [ms] (worst run)|866.1|101.7|
|E2E max [ms] (worst run)|1 455.1|102.1|
|_Steady state (_5_s discarded)_|||
|E2E mean [ms] (per run)|2.8 – 87.4|100.8 – 100.9|
|E2E std [ms] (per run)|0.06 – 25.8|0.22 – 0.42|
|E2E p99 [ms] (worst run)|101.7|101.7|
|E2E max [ms] (worst run)|101.8|102.1|


For the end-to-end latency, we measure the time from the moment the LiDAR starts executing until the moment the corresponding control signal is emitted by the VehicleInterface node. There are two timers with a period of 100 ms in the data path, one in the FrontLidarDriver node that produces the LiDAR messages, and one in the BehaviorPlanner node that produces a plan based on the LiDAR data and other inputs. Percallback execution times are implemented as a fixed amount of arithmetic work, set to roughly 0 _._ 2 ms of execution time per callback on our platform. 

Table I reports the metrics across 20 runs of 60 s each, both over the full run and over the steady state after discarding the first 5 s. The first seconds are affected by a startup transient, as DDS discovery and ROS 2 node creation complete only after the program begins. Our framework removes this transient from the LF execution by anchoring logical time zero to the instant all subscriptions have matched a publisher, which keeps the logical ordering unchanged but aligns the first events’ physical-time release with the logical schedule. Default ROS 2 does not have such a mechanism. 

**Within-node callback ordering.** We focus on BehaviorPlanner, which subscribes to six topics (NDTLocalizer, ObjectCollisionEstimator, Lanelet2GlobalPlanner, Lanelet2MapLoader, ParkingPlanner, LanePlanner) and outputs a plan when its 100 ms timer executes. For each of the fifteen pairs of subscription callbacks and each 100 ms timer interval between the planner executions, we record which subscription fires first. We then investigate, for each callback pair, whether the order is the same across runs. 

Under default ROS 2, the order between two subscriptions changes from run to run. For twelve of the fifteen pairs, how often one subscription fires before the other shifts by more than ten percentage points between runs. For three pairs the dominant order flips entirely. One run has sub _A_ firing before sub _B_ in nearly every window, while another run of the same 

system has _B_ firing before _A_ in nearly every window. The same system processing the same workload thus processes data in different sequences, resulting in the planner using different information to generate its output on every run. 

Under LF the order of every pair is identical across all twenty runs. Each subscription callback fires at a deterministic logical-time tag, and ties at the same tag are resolved by the static reaction order inside the reactor. 

**End-to-end latency.** In the steady state, both runtimes reach a comparable worst case, a p99 of 101 _._ 7 ms and a maximum near 102 ms. What differs is the mean and its reproducibility. Under LF the mean is 100 _._ 8–100 _._ 9 ms across all runs with a within-run standard deviation of 0 _._ 22–0 _._ 42 ms, whereas under default ROS 2 the mean differs on every run, ranging from 2 _._ 8 to 87 _._ 4 ms. Over the full run, the LF statistics are unchanged because no chain-job is delayed by the startup transient, while default ROS 2 reaches a p99 of 866 ms and a maximum of 1 455 ms from the chain-jobs that run during discovery. Both runtimes thus reach the same steady state, but only LF reaches it without a large startup transient. 

The dominant component of the steady-state chain latency is caused at the BehaviorPlanner node. The BehaviorPlanner processes LiDAR data only when its own 100 ms timer fires. A LiDAR sample that arrives at the planner gate must therefore wait until the next timer execution before the data is processed. The duration of this wait depends entirely on the relative phase of the two 100 ms timers along the chain. Under LF, both timers fire at the same sequence of tags from logical time _T_ = 0 onwards (Section VI-B), resulting in a consistent delay of about 100 ms on every run for the end-to-end latency. Under default ROS 2, the two timers run on independent physical clocks, and the phase offset between them is whatever it happened to be when each node finished its initialization. The delay introduced by waiting on the timer is therefore a run-specific constant somewhere in the range of [0 _,_ 100) ms, producing a different value on every run. 

## _C. Determinism on the running example_ 

In the following, we show how we can use the running example (Figure 1) to demonstrate the effects of different logical-time delays on the execution behavior. The running example is instantiated with a timer period of _T_ = 100 ms. To expose the nondeterministic execution order at Node _D_ identified in Section VI-A, the execution times of the two paths _A → B → D_ and _A → C → D_ are designed to be comparable but varying over runs. Specifically, Node _A_ ’s timer callback _cA_ publishes on /alpha and /beta after a fixed 1 ms of execution time. The parallel paths via _B_ and _C_ propagate the data to Node _D_ . Node _B_ ’s callback _cB_ runs for a random execution time drawn uniformly from the interval [0 _,_ 10] ms before publishing on /gamma, and Node _C_ ’s callback _cC_ runs for an independent random execution time drawn from the same interval [0 _,_ 10] ms before publishing on /delta. Node _D_ ’s callbacks _cD_ 1 and _cD_ 2 each run at a fixed 1 ms of execution time. 

9 


Figure 3: Running example: end-to-end latency distribution under default ROS 2 and LF across the after-delay sweep ( _N_ = 20 runs of 60 s each). Boxes show the interquartile range, whiskers the 5th–95th percentiles. 

The arrival order of /gamma and /delta at _D_ in ROS 2 due to the above design varies over time. We measure two quantities on Node _D_ across 20 _×_ 60 s runs per configuration. First, the fraction of timer ticks for which _cD_ 1 starts before _cD_ 2. Second, the end-to-end latency from _A_ ’s timer start to the later of _cD_ 1’s and _cD_ 2’s end for the same tick. 

**Ordering.** Under default ROS 2, _cD_ 1 precedes _cD_ 2 on 49 _._ 0% of executions, showing the randomness of the order at _D_ . The randomly varying work for the reactions in reactors _B_ and _C_ makes the two paths to _D_ finish in a different order from one execution to the next, and the ROS 2 executor on _D_ serves whichever message arrived first. Under LF, every configuration places _cD_ 1 before _cD_ 2 on all ticks, since their logical arrival times at _D_ are identical by construction, and the static reaction order inside _D_ resolves ties in favor of reaction _cD_ 1. 

**The after delay as a latency-consistency knob.** We study the effects of logical-time delays on the execution behavior of the system, and how logical delays can be used as a design knob to control the consistency and availability of the system. For this, we choose different values for the logical-time delays of the connections while preserving the constraint that both paths from _A_ to _D_ carry the same total logical delay _d_ : _d/_ 2 on each of the four edges _A → B_ , _B → D_ , _A → C_ , and _C → D_ . Figure 3 reports the default ROS 2 baseline against LF configurations sweeping _d_ from 0 to 25 ms in steps of 5 ms. 

The median end-to-end latency rises from _≈_ 10 ms at _d_ = 0 to _≈_ 27 ms at _d_ = 25 ms, gaining roughly 5 ms for every 5 ms added to _d_ , on top of a workload floor of a few milliseconds. The spread of the distribution tells a more interesting story. At _d_ = 0 the standard deviation of the end-to-end latency is about 2 _._ 4 ms, because the two paths propagate their data randomly to the output without any controlled delay. This setting maximizes consistency, since both paths deliver the freshest data the moment it is ready. As _d_ grows, the logical delay progressively absorbs the temporal variability of the two paths, and the boxes tighten until, at _d_ = 20 ms and beyond, the standard deviation collapses below 0 _._ 1 ms because both reactions are triggered at the same fixed tag on every tick. This setting maximizes availability, since the latency becomes a constant the rest of the system can rely on, at the cost of no longer using the most up-to-date data. The after delay 

therefore trades consistency for availability, and the designer can configure this aspect through the logical-time delays of the connections. Default ROS 2 does not offer such control, and its latency and ordering are dependent on when the executor finishes callbacks and DDS delivers messages. 

## X. CONCLUSION 

We characterize the subset of ROS 2 features that admits deterministic execution under Lingua Franca, and build a tool to convert any ROS 2 application in this subset into an LF program automatically. The generated program runs the unmodified ROS 2 callbacks under the LF runtime, which takes over scheduling and callback ordering to guarantee deterministic execution. On top of this conversion, the system gains LF-native mechanisms for logical-time delays, federated coordination, and fault handling, without any change to the application code, which can be used to control the consistency and availability of the system. Evaluation on the Autoware reference system and a synthetic scenario shows deterministic callback ordering and controlled end-to-end latency variability. 

## APPENDIX 

In the following, we detail the extraction and conversion tools that we use to automatically convert a ROS 2 system into an LF program and run it, as illustrated in Figure 4. 

## _A. Extraction_ 

We start from the ROS 2 code from which we extract the system information. We first describe how ROS 2 code is organized in a codebase, and how we extract the necessary information from it to build a system graph that captures the structure of the system and the components’ interactions. 

ROS 2 provides so-called packages in which the source code of a ROS 2 system is organized. A package is a directory that contains the source code of said package, configuration files, and any resources necessary to run the system. Each package specifies its libraries and executables in a CMakeLists.txt file, which is used to build the package and link the source code together. Furthermore, each package may include launch files, which specify the executables to run and their parameters. Launch files can also be nested to include launch files from multiple packages. 

Our extraction tool is built on top of the colcon build system, which is the standard build system for ROS 2, and we call this step colcon lf-analyze. It parses all packages in a workspace, and extracts the necessary information from the launch files, source code, and CMake metadata using static code analysis. Since we only require an instantiation of the static system for conversion, static code analysis is sufficient for the extraction. If the extracted system contains any feature that prevents deterministic execution, as described in Section VI-C, the tool refuses to generate a program and provides feedback on which features are blocking the conversion and which part of the code includes them. 

10 


Figure 4: The colcon lf pipeline: launch files, C++ source, and CMake metadata are extracted to system.json, then converted to .lf source by applying the embedding _E_ , compiled by lfc, and executed under LF time authority. 

The output of the extraction tool is a _system graph_ written to a single json file, enumerating all components that are extracted, including launch files, executables, libraries, callbacks, timers, publishers, subscriptions, and so on. 

execution of all callbacks that are part of the group, while callbacks of different mutually-exclusive callback groups are allowed to run concurrently. By default, each node has one mutually-exclusive callback group. If not specified otherwise, each callback is part of the default callback group of its node. 

In LF, all reactions inside a reactor are guaranteed to be executed sequentially. Thus, we map callback groups as nested callback group reactors inside node reactors. This reproduces the concurrency of ROS 2 in LF, as reactions from different callback group reactors can run concurrently, while the reactions in one callback group reactor are run sequentially. **Statically known topic names, namespaces, and remappings.** All naming schemes, such as for nodes, topics, callbacks, can be extracted from the ROS 2 system under the assumption that these do not change during runtime. 

While there are many more features in ROS 2, such as lifecycle nodes, actions, and reentrant callback groups, that are used in practice, we focus on the previously described features, as they are sufficient to cover the conversion of a large class of ROS 2 systems to LF programs. 

## _C. Compilation_ 

## _B. Generation_ 

Next, we take the system graph and generate .lf source files that mirror the structure of the original system. This step is called colcon lf-generate. The trivially convertible ROS 2 components map one-to-one to LF features as follows: 

- **Nodes:** Each node maps to an LF reactor. 

- **Callbacks:** Each callback of a node maps to a reaction of the reactor. 

- **Timers:** Each timer with a fixed period _T_ maps to an LF timer with the same period. 

- **Publishers:** Each publisher maps to an output port. 

- **Subscriptions:** Each subscription maps to an input port. 

- **Topics:** A topic determined by the unique publisher and subscription pair corresponds to the connection between an output port and input port. 

Next, we move on to the more complex features that have a non-trivial LF realization, but still can be converted. **Topics with multiple subscribers.** A topic with multiple subscribers maps to one output port connected to multiple input ports. 

**Async service clients.** A service client and a service server are usually implemented as two nodes, where a client sends a request to a server, and the server sends a response back. In the node hosting the service client, one callback is responsible for sending the request, and another callback is responsible for processing the response. In the node hosting the service server, one callback is responsible for processing the request and sending the response back. Our tool maps each of the three callbacks to its own reaction, and adds two connections: client-request to server, and server-response to client. 

**Mutually exclusive callback groups.** ROS 2 provides the concept of callback groups, which are a way to group callbacks together and specify if they can be executed concurrently. Mutually exclusive callback groups prevent the concurrent 

The generated .lf sources are compiled by the LF compiler lfc, which emits C++ reaction code that links against the LF runtime. We refer to this step as colcon lf-build, which builds the resulting binaries together with thin C++ wrapper packages and new launch files that connect the LF executables to the original ROS 2 code. 

**Runtime binding.** The generated program runs under the LF runtime, which schedules reaction firings according to the logical time semantics of the LF runtime. A thin C++ library, ros2_lf_binding, bridges the two runtimes. Each generated reaction calls a corresponding function, e.g. ros2_lf_invoke_timer for timers or ros2_lf_invoke_sub for subscriptions, which dispatches into the unmodified ROS 2 callback body through the registered handle. The ROS 2 runtime threads are not started. Instead, the binding extends the default ROS 2 executor with a function that runs a single callback, which keeps DDS message reception and other built-in ROS 2 services available, while the program is under direct control of the LF runtime. **Communication and time.** Message payloads continue to flow over DDS exactly as in the original program, since the unmodified callback bodies still call publish() and take() for DDS communication. On the LF side, the replicated system sends only dummy messages between ports, because the LF runtime is used solely to coordinate activation and ordering, not payload transport. The ROS 2 clock is wired to logical time, and a custom ROS 2 publisher inside the LF runtime emits the current logical time on a dedicated topic using a custom message type that includes both the logical time and the microstep data. All original ROS 2 timers are kept inactive, since the LF runtime controls the triggering of those timers. 

## _D. Execution_ 

The final step in the pipeline launches the compiled program under the LF runtime. Invoking ros2 lf launch starts the 

11 

binaries produced by colcon lf-build using the generated launch files and registers the binaries as standard ROS 2 executables, so external ROS 2 tools such as ros2 topic, ros2 bag, and rqt continue to work with the running system without any modification. The command replaces the original ros2 launch call that is used to start the system. 

In a federated deployment, ros2 lf launch additionally starts the LF Runtime Infrastructure (RTI) and the configured federates, either co-located on one machine or distributed across hosts according to the grouping selected in Section VIII-B. The RTI coordinates the logical clocks of the federates, so the determinism guarantee covers the entire deployment rather than a single process. Our tool supports per-node federation (one federate per ROS 2 node), and also any custom grouping of federates that are on the same system, as part of the compile step configuration. 

## REFERENCES 

- [1] Autoware Foundation. Autoware reference system, 2026. https://github.com/ros-realtime/reference-system, Last Accessed: 2026-05-26. 

- [2] S. Bateni, M. Lohstroh, H. S. Wong, H. Kim, S. Lin, C. Menard, and E. A. Lee. Risk and mitigation of nondeterminism in distributed cyber-physical systems. In _21st ACM/IEEE International Symposium on Formal Methods and Models for System Design (MEMOCODE)_ , pages 1–11, 2023. 

- [3] A. Benveniste, P. Caspi, S. Edwards, N. Halbwachs, P. Le Guernic, and R. de Simone. The synchronous languages 12 years later. _Proceedings of the IEEE_ , 91(1):64–83, 2003. 

- [4] T. Blaß, D. Casini, S. Bozhko, and B. B. Brandenburg. A ROS 2 response-time analysis exploiting starvation freedom and execution-time variance. In _2021 IEEE Real-Time Systems Symposium (RTSS)_ , pages 41–53, 2021. 

- [5] T. Blaß, A. Hamann, R. Lange, D. Ziegenbein, and B. B. Brandenburg. Automatic latency management for ROS 2: Benefits, challenges, and open problems. In _27th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ , pages 264–277. IEEE, 2021. 

- [6] D. Casini, T. Blaß, I. Lütkebohle, and B. B. Brandenburg. ResponseTime Analysis of ROS 2 Processing Chains Under Reservation-Based Scheduling. In S. Quinton, editor, _31st Euromicro Conference on RealTime Systems (ECRTS 2019)_ , volume 133 of _Leibniz International Proceedings in Informatics (LIPIcs)_ , pages 6:1–6:23, Dagstuhl, Germany, 2019. Schloss Dagstuhl – Leibniz-Zentrum für Informatik. 

- [7] D. Casini, J.-J. Chen, J. Li, F. Reghenzani, and H. Teper. A Survey of Real-Time Support, Analysis, and Advancements in ROS 2. _Leibniz Transactions on Embedded Systems_ , 11(1):1:1–1:37, 2026. 

- [8] H. Choi, Y. Xiang, and H. Kim. Picas: New design of priority-driven chain-aware scheduling for ros2. In _2021 IEEE 27th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ , pages 251– 263. IEEE, 2021. 

- [9] N. Halbwachs, P. Caspi, P. Raymond, and D. Pilaud. The synchronous data flow programming language lustre. _Proceedings of the IEEE_ , 79(9):1305–1320, 1991. 

- [10] W. K. Huang, Y. Terazawa, Y. Matsubara, and A. Iwai. Software-defined vehicles: Challenges and orchestrating mixed-criticality services using Lingua Franca. _IEEE Embedded Systems Letters_ , 2025. 

   - [14] E. Lee and T. Parks. Dataflow process networks. _Proceedings of the IEEE_ , 83(5):773–801, 05 1995. 

   - [15] E. A. Lee, R. Akella, S. Bateni, S. Lin, M. Lohstroh, and C. Menard. Consistency vs. availability in distributed cyber-physical systems. _ACM Trans. Embed. Comput. Syst._ , 22(5s):138:1–138:24, Sept. 2023. 

   - [16] E. A. Lee, S. Bateni, S. Lin, M. Lohstroh, and C. Menard. Quantifying and generalizing the CAP theorem. _arXiv_ , abs/2109.07771, 2021. 

   - [17] Lingua Franca Project. Lingua Franca coordination language, 2026. https://github.com/lf-lang/lingua-franca, Version 0.12.1, Last Accessed: 2026-05-26. 

   - [18] Lingua Franca Project. Playground for the Lingua Franca coordination language, 2026. https://github.com/lf-lang/playground-linguafranca, Last Accessed: 2026-05-26. 

   - [19] S. Liu, X. Jiang, N. Guan, Z. Wang, M. Yu, and W. Yi. Rtex: An efficient and timing-predictable multithreaded executor for ROS 2. _IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems_ , 43(9):2578–2591, 2024. 

   - [20] M. Lohstroh, C. Menard, S. Bateni, and E. A. Lee. Toward a lingua franca for deterministic concurrent systems. _ACM Trans. Embed. Comput. Syst._ , 20(4):36:1–36:27, 2021. 

   - [21] M. Lohstroh, Í. Í. Romeo, A. Goens, P. Derler, J. Castrillón, E. A. Lee, and A. L. Sangiovanni-Vincentelli. Reactors: A deterministic model for composable reactive systems. In R. Chamberlain, M. Edin Grimheden, and W. Taha, editors, _Cyber Physical Systems. Model-Based Design_ , pages 59–85, Cham, 2020. Springer International Publishing. 

   - [22] S. Macenski, T. Foote, B. P. Gerkey, C. Lalancette, and W. Woodall. Robot Operating System 2: Design, architecture, and uses in the wild. _Science Robotics_ , 7(66):eabm6074, 2022. 

   - [23] C. Menard, M. Lohstroh, S. Bateni, M. Chorlian, A. Deng, P. Donovan, C. Fournier, S. Lin, F. Suchert, T. Tanneberger, H. Kim, J. Castrillón, and E. A. Lee. High-performance deterministic concurrency using lingua franca. _ACM Transactions on Architecture and Code Optimization_ , 20(4):48:1–48:29, 2023. 

   - [24] Object Management Group. Data distribution service (DDS) specification, version 1.4. Technical report, Object Management Group, 2015. 

   - [25] Open Robotics. ROS 2: Robot operating system 2, 2026. 

   - [26] S. Sagmeister, M. Weinmann, P. Pitschi, and M. Lienkamp. RSLCPP – deterministic simulations using ROS 2, 2026. https://arxiv.org/abs/2601.07052. 

   - [27] Y. Tang, N. Guan, X. Jiang, X. Luo, and W. Yi. Real-time performance analysis of processing systems on ros 2 executors. In _2023 IEEE 29th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ , pages 80–92. IEEE, 2023. 

   - [28] Y. Tang, X. Jiang, N. Guan, X. Luo, M. Yang, and W. Yi. Timing analysis of processing chains with data refreshing in ros 2. _Journal of Systems Architecture_ , 155:103259, 2024. 

   - [29] H. Teper, O. Bell, M. Günzel, C. Gill, and J.-J. Chen. Reconciling ROS 2 with classical real-time scheduling of periodic tasks. In _31st Real-Time and Embedded Technology and Applications Symposium (RTAS)_ , pages 177–189. IEEE, 2025. 

   - [30] H. Teper, T. Betz, M. Günzel, D. Ebner, G. Von Der Brüggen, J. Betz, and J.-J. Chen. End-to-end timing analysis and optimization of multiexecutor ROS 2 systems. In _2024 IEEE 30th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ , pages 212–224, 2024. 

   - [31] H. Teper, T. Betz, G. Von Der Brüggen, K.-H. Chen, J. Betz, and J.-J. Chen. Timing-aware ROS 2 architecture and system optimization. In _29th International Conference on Embedded and Real-Time Computing Systems and Applications (RTCSA)_ , pages 206–215. IEEE, 2023. 

   - [32] H. Teper, M. Günzel, N. Ueter, G. von der Brüggen, and J.-J. Chen. End-to-end timing analysis in ROS 2. In _2022 IEEE Real-Time Systems Symposium (RTSS)_ , pages 53–65, 2022. 

- [11] S. Kato, S. Tokunaga, Y. Maruyama, S. Maeda, M. Hirabayashi, Y. Kitsukawa, A. Monrroy, T. Ando, Y. Fujii, and T. Azumi. Autoware on board: Enabling autonomous vehicles with embedded systems. In _2018 ACM/IEEE 9th International Conference on Cyber-Physical Systems (ICCPS)_ , pages 287–296. IEEE, 2018. 

- [12] J. Kwok, S. Li, M. Lohstroh, and E. A. Lee. HPRM: High-performance robotic middleware for intelligent autonomous systems. In _IEEE International Conference on Robotics and Automation (ICRA)_ , pages 8093–8099, 2025. 

- [13] E. Lee and D. Messerschmitt. Synchronous data flow. _Proceedings of the IEEE_ , 75(9):1235–1245, 1987. 

12 

