---
title: "Fixed-Priority and EDF Schedules for ROS2 Graphs on Uniprocessor"
date: "2025-11-28"
authors: "Oren Bell; Harun Teper; Mario Günzel; Chris Gill; Jian-Jia Chen"
url: https://arxiv.org/abs/2512.16926
pdf: https://arxiv.org/pdf/2512.16926
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.16926)** / [論文ページ](https://arxiv.org/abs/2512.16926)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Fixed-Priority and EDF Schedules for ROS 2 Graphs on Uniprocessor** 

Oren Bell<sup>1</sup> , Harun Teper<sup>2</sup> , Mario Günzel<sup>2</sup> , Chris Gill<sup>1</sup> , and Jian-Jia Chen<sup>2</sup> 

> 1 Washington University in St Louis, USA, 

```
{oren.bell,cdgill}@wustl.edu
```

> 2 TU Dortmund University, Germany, 

```
{harun.teper,mario.guenzel,jian-jia.chen}@tu-dortmund.de
```

**Abstract.** This paper addresses limitations of current scheduling methods in the Robot Operating System (ROS) 2, focusing on scheduling tasks beyond simple chains and analyzing arbitrary Directed Acyclic Graphs (DAGs). While previous research has focused mostly on chainbased scheduling with ad-hoc response time analyses, we propose a novel approach using the events executor to implement fixed-job-level-priority schedulers for arbitrary ROS 2 graphs on uniprocessor systems. We demonstrate that ROS 2 applications can be abstracted as forests of trees, enabling the mapping of ROS 2 applications to traditional realtime DAG task models. Our usage of the events executor requires a special implementation of the events queue and a communication middleware that supports LIFO-ordered message delivery, features not yet standard in ROS 2. We show that our implementation generates the same schedules as a conventional fixed-priority DAG task scheduler, in spite of lacking access to the precedence information that usually is required. This further closes the gap between established real-time systems theory and ROS 2 scheduling analyses. 

## **1 Introduction** 

The Robot Operating System (ROS) 2 is a widely adopted software framework for developing robotics applications, which has garnered significant attention from the real-time systems research community. While ROS 2 provides mechanisms for modular development using nodes and callbacks, its default scheduling capabilities present challenges for predictable real-time performance, particularly for complex applications involving branching or merging data flows (i.e., arbitrary graphs). 

Since 2019, there has been ongoing research into modeling and analyzing the end-to-end timing behavior of ROS 2 applications. The default ROS 2 scheduler, called an _executor_ , has inherent limitations [2,5,13,15,16] that cause highly pessimistic response times for tasks within an application, compared to classical real-time periodic schedulers. There has been work to provide response time analysis [5,13,16] and strategies to minimize response times [2,6,13]. The limitations of the default executor are discussed further in Section 2. 

2 Oren Bell, Harun Teper, Mario Günzel, Chris Gill, and Jian-Jia Chen 

An alternate executor design, the events executor [8], was mainlined into ROS 2 in 2023. It is detailed further in Section 2.2. Prior work [14] proposed applying classical real-time theory to the events executor. They showed that the events executor could be used to implement arbitrary periodic fixed-priority scheduling. They also provided some preliminary work providing a response-time analysis for basic chain applications. Building upon this, our work addresses predictable scheduling for arbitrary ROS 2 graphs. We demonstrate mapping ROS 2 applications to standard DAG task models and propose a novel events queue implementation for the Events Executor. This enables any Limited Preemption Fixed Job-Level Priority (LP-FJP) scheduler – e.g., Rate Monotonic (RM) or Earliest Deadline First (EDF). 

**Contributions.** In this paper, we (i) provide a mapping showing that an arbitrary ROS 2 graph can be modelled as a set of DAG tasks for analysis purposes (Section 4), including showing that ROS 2 graphs are logically trees for the purposes of scheduling (Section 4.3); (ii) introduce an events queue implementation for the Events Executor that can realize any LP-FJP scheduler for the resulting DAG tasks (Section 5), noting that our approach relies on LIFO-ordered message queues which are not yet standard in ROS 2 middleware; and (iii) provide a formal analysis proving the correctness of this events queue mechanism (Section 6). This work further closes the gap between established real-time systems theory and practical ROS 2 scheduling analysis, moving beyond the ad-hoc approaches and chain-structured applications of existing literature. 

## **2 Background** 

The Robot Operating System (ROS) 2 provides a component-based framework for building robotic systems. A sample application is illustrated in Figure 1. Key concepts include: **Nodes** that encapsulate related functionalities (e.g., sensor driver, path planner); **Topics** , which are named communication channels facilitating data exchange via a publish-subscribe paradigm provided by the Data Distribution Service (DDS); **Callbacks** are functions within nodes triggered by specific events, primarily **Timer Callbacks** that execute periodically based on a configured rate and **Subscription Callbacks** that execute upon receiving a message on a subscribed topic. The sequence of callbacks triggered by data flowing through topics forms the application’s processing logic, often creating implicit dependencies or chains of execution. 

### **2.1 Default ROS 2 Executor** 

ROS 2 uses an entity called an _executor_ to manage the execution of callbacks. The default executor, often referred to as the ‘SingleThreadedExecutor’, has several characteristics and limitations documented in prior work [2,5,13,15,16]. The default ROS 2 executor uses a mechanism called a **Ready Set** to hold callbacks ready for execution. The ready set is not aware of individual instances of callbacks’ releases. It only indicates if a callback is ready for execution, and not how 

3 

Fixed-Priority and EDF Schedules for ROS 2 Graphs on Uniprocessor 


Fig. 1: Sample ROS2 Application. Subscription Callbacks illustrated in orange, Timer Callbacks illustrated in purple. Topics are pipes between nodes. 

many instances are in the backlog. The ready set is populated only at specific **Polling Points** . Once populated, the executor processes callbacks from the set until it is empty before polling again. The interval between two polling points is known as the **Processing Window** . Callbacks becoming ready _during_ this window must wait until the next polling point, potentially leading to significant delays and priority inversions, as lower-priority callbacks already in the ready set execute first. The default ROS 2 executor employs a round-robin **Scheduling Policy** within the ready set, with a static bias favoring timer callbacks over subscription callbacks, and only executing each callback once per processing window, regardless of the number of instances released. These limitations make it difficult to provide strong real-time guarantees, especially for complex applications. 

All these concepts are illustrated in Figure 2a. At time 0, three timer callbacks are released, and enqueued into the ready set. They are executed in round robin order until time 23, when the ready set is empty. This causes another polling point to occur, and another instance of callback _τ_ 1 is enqueued and executed. This is despite the fact that there were two instances of _τ_ 1 that should have executed. The second instance instance, release at time 20, is not acknowledged and implicitly dropped. 

### **2.2 The Events Executor** 

To address the shortcomings of the default executor, the Events Executor was introduced [8]. Key differences are as follows. The Events Executor replaces the ready set with an **Events Queue** . Each triggering event (timer expiration, message arrival) generates a distinct entry in the queue, allowing multiple instances of the same callback to be queued independently if necessary. The Events Executor uses **Continuous Polling** to check for new events (polls) after _each_ callback execution finishes, rather than waiting for the queue to become empty. This eliminates the problematic processing window of the default executor. By default, the events queue operates in a **First-In, First-Out (FIFO)** manner. 

This behavior is illustrated in Figure 2b. Unlike with the default executor in Figure 2a, the additional instance of task _τ_ 2 available at time 20 is acknowl- 

- 4 Oren Bell, Harun Teper, Mario Günzel, Chris Gill, and Jian-Jia Chen 

edged and enqueued into the events queue. No jobs are dropped because of the processing window. 

Teper et al. [14] showed that the structure of the events executor allows for easier application of standard real-time analysis (demonstrated for chains) and demonstrated that the events queue itself could be replaced to implement different scheduling policies. Our work builds directly on this potential. 


Fig. 2: Example schedules contrasting default ROS 2 executor with events executor 

## **3 Related Work** 

**Executor Extensions and Replacements.** Recognizing the default executor’s limitations, researchers proposed modifications and alternatives. PiCAS [6] introduced a priority-driven chain-aware a priori work assignment algorithm, often requiring decomposition of the application across multiple executor instances. Other works explored different executor designs [1]. The Events Executor [8], as discussed in Section 2, represents a significant step towards a more standard scheduling infrastructure within ROS 2. 

**Bridging the Gap for General Graphs (Our Contribution).** While [14] laid important groundwork and demonstrated the potential for chains, it did not provide a concrete mechanism or analysis for applying standard priority-based scheduling (like LP-FJP) to general ROS 2 _graphs_ (involving branching and merging). This paper fills that gap by: (1) presenting the graph unfolding technique to map ROS 2 graphs to standard DAG models for analysis, (2) designing a specific two-queue mechanism for the Events Executor’s queue that equates to LP-FJP scheduling, and (3) providing a formal proof that this mechanism correctly schedules tasks according to their job-level priorities _without_ needing explicit runtime access to the graph structure, relying instead on implicit priority inheritance. This allows direct application of existing LP-FJP DAG scheduling analysis, such as [9]. 

Fixed-Priority and EDF Schedules for ROS 2 Graphs on Uniprocessor 

5 

## **4 System Model** 

In this section, we discuss the unique manner in which ROS 2 schedules callbacks, and the assumptions we must make before mapping applications to a conventional DAG task model, detailed next. 

### **4.1 Task Model** 

Given a set T = _{τ_ 1 _, τ_ 2 _, ..., τn}_ of tasks, a **periodic DAG task** _τi_ is specified by the tuple _τi_ = ( _Ti, Di, ϕi_ ) _∈_ R<sup>3</sup> , where _Ti >_ 0 is the period, _Di >_ 0 is the relative deadline, and _ϕi_ is the phase. The periodic task _τi_ releases its first job (task instance) at time _ϕi_ , and subsequent jobs are released every _Ti_ time units. Every job has an absolute deadline specified as its release time plus the relative deadline. 

A **sporadic DAG task** _τi_ is similarly defined as the tuple _τi_ = ( _Ti, Di_ ) _∈_ R<sup>2</sup> , where _Ti_ is instead the minimum interarrival time between two successive jobs. The _periodic task model_ is a specialization of the _sporadic task model_ . 

Each DAG task is associated with a graph _Gi_ = ( _Vi, Ei_ ). The nodes in the finite set _Vi_ = _{vi_ 1 _, vi_ 2 _, ...}_ model non-preemptible portions of work, or _subtasks_ , in the task _τi_ . Each subtask _vij_ has a worst-case execution time (WCET) _wij_ and may have precedence constraints modeled by the relations in the finite set _Ei_ = _{ei_ 1 _, ei_ 2 _, ...}_ . A subtask is released when all of its precedence constraints (if any exist) are met. We define a precedence relation as _vij ≺ vik_ and say that _vij_ is a **parent** of _vik_ . 

Each subtask _vij_ has an associated amount of work, _Wij_ , which is the WCET the subtask needs to complete. We say a **job** of task _τi_ is complete when one instance each of _vij ∈ Vi_ are complete. We focus specifically on DAG task schedulers with _limited preemption_ and _fixed job-level priority_ . _Limited preemption_ (LP) means that individual subtasks cannot be preempted, but a task can be preempted in between constituent subtasks. We take this approach to conform to the natural behavior of ROS 2 executors, which will not preempt running executables. Thus, the only possible preemption points are at the completion of subtasks. _Fixed job-level priority_ (FJP) means that a task and all its constituent subtasks have the same priority for a given job instance. The priority between two job releases of the same task may vary. All fixed-priority schedulers are naturally also fixed for individual jobs. Earliest Deadline First (EDF) is an example of a dynamic-priority scheduler whose priorities are fixed for individual jobs, i.e., it is FJP. 

### **4.2 Mapping ROS 2 to DAG Task Model** 

As in prior literature [5,6,13], we abstract the dataflow paths of a ROS 2 application into a graph structure. To illustrate, consider an example ROS 2 application with a couple sensor nodes that take periodic measurements, and publish their data to topics subscribed by downstream computation nodes, like sensor fusion, 

6 Oren Bell, Harun Teper, Mario Günzel, Chris Gill, and Jian-Jia Chen 

mapping, planning, etc. The sensors are time triggered and so associated with timers. All data-driven tasks are associated with subscriptions. 

Within the graph structure, each callback (timer, subscription, etc) forms a subtask, which may be released periodically (in the case of timers), or datadriven (in the case of subscriptions). During the course of a its execution, a subtask _τi_ may publish a message to a topic, and any subscribers to that topic, _τj_ will be modeled as children of _τi_ . 

We assume that ROS 2 applications do not have such loops, enabling the connection to DAGs. Given no restrictions on the system design, it is possible for subscriptions to send messages to themselves or form a loop in which data is propagated from one subscription through other subscriptions and back to itself. But if a subscription is allowed to continually trigger itself, it creates a positive feedback loop of exploding message bandwidth, so this is strongly discouraged by good ROS 2 design principles. After establishing these precedence constraints, these subtasks can then be arranged into _DAG tasks_ . In the next section, we will demonstrate they have a tree structure, and so a singular subtask can be described as the root. These _DAG tasks_ are modeled as _periodic tasks_ when a timer is at the root, and externally-driven _sporadic tasks_ when a subscription is at the root. 

In the existing DAG scheduling literature, the term _node_ is synonymous with _subtask_ [4,7,9,12,17]. To avoid confusion, we will strictly use the ROS 2 definition of _node_ , which is an object that serves as a programmatical abstraction to bundle executable entities under a unified namespace. _Subtask_ will be used exclusively to refer to callbacks in the context of scheduling. 

We only concern ourselves with dataflow that occurs through the Data Distribution Service (DDS), a publish-subscribe communication middleware used by default in a ROS 2 based system. Any two subtasks that communicate with shared memory (as is the case with some _fusion node_<sup>3</sup> implementations) are not necessarily modeled as being in the same task. A precedence constraint is only imposed when the execution of one subtask triggers the release of another. Any subtasks that exchange information asynchronously, bypassing the pub/sub mechanism, are not modelled by our work. 

Code within callbacks can be fairly arbitrary. In order for the analysis of a ROS 2 application to be feasible, we must impose some constraints on its behavior: (1) children are eligible for release as soon as parents finish, so no inter-subtask latency needs to be modeled; (2) no new threads are created; (3) no blocking on IO reads occur; and (4) more generally, all execution times of callbacks are bounded. 

Conventional real-time schedulers stipulate that child subtasks are eligible for execution when their parents complete, and thus imposing this requirement is needed to comply with the analysis of a LP-FJP scheduler. We restrict the callback’s ability to spawn new threads, since the scope of this paper is limited 

> 3 A fusion node is a component with a single output that combines data from multiple inputs. Unlike many-to-one topics, the output topic operates at an independent rate, or a rate matching only one of the inputs. 

Fixed-Priority and EDF Schedules for ROS 2 Graphs on Uniprocessor 

7 

to the uniprocessor case. According to the model we established in 4.1, subtasks have a finite WCET. Therefore anything capable of an unbounded delay is not allowed. 

One of the most unique aspects of modeling ROS 2 applications as a DAG task is that precedence constraints are logically disjunctive: a subtask will execute a job for _each_ execution of _each_ of its parents. This is not in line with the conventional DAG task model we laid out above, until we apply the abstraction of virtually unfolding the graph into a forest of trees, described next. 

### **4.3 Graph Unfolding** 

Next, we show that ROS 2 applications that can be modeled as DAGs can be converted to trees due to the logically disjunctive precedence constraints. In conventional DAGs, subtasks will wait for all of their parents before being eligible for execution. In ROS 2, however, when multiple parents publish to the same subtask, the child will execute once for each parent event. To model this behavior _for analysis purposes_ , we adapt the concept of graph unfolding [3] where we virtually duplicate each subtask so that each resulting virtual subtask instance has exactly one parent. 

This transformation is illustrated in Figure 3. This creates a tree (or rather a forest, since there can be multiple trees). We posit some properties of this new representation: (i) each subtask has either 1 or 0 parents; (ii) each subtask is the root of a unique subtree; (iii) subtasks with 0 parents will be the root of a tree; and (iv) root subtasks can be modelled sporadically. 

To justify the last point, we note that timer tasks trigger periodically, and it’s assumed that parentless subscription tasks are triggered by some external event for which a minimum inter-arrival time is known. This assumption is in line with prior literature [13]. As previously mentioned, this transformation is possible for ROS 2 applications that are free of cycles and can be modeled as DAGs. 

### **4.4 Fusion Nodes** 

A common pattern in ROS 2 involves _fusion nodes_ , which combine data from multiple input topics. While the previous sections already sufficient for general DAGs, we present special commentary for the modeling of fusion nodes in graph unfolding. This depends on their implementation: 

- **Trigger-Based Fusion.** If a node subscribes to multiple topics and its single callback executes upon message arrival, potentially varying its behavior or execution time based on which topic triggered it or conditionally publishing, our unfolding process (Section 4.3) still applies. The fusion node is duplicated for each incoming topic edge. While this correctly models the potential execution paths for analysis, applying the node’s full WCET to each unfolded instance can lead to pessimistic (safe, but potentially loose) response time bounds if the actual execution is conditional or significantly shorter for certain triggers. 

- 8 Oren Bell, Harun Teper, Mario Günzel, Chris Gill, and Jian-Jia Chen 


Fig. 3: Unfolding of a ROS 2 Graph into a Forest. Timers in purple, subscriptions in blue 

- **Timer-Based Fusion.** If a node subscribes to multiple topics, buffers the data internally, and uses a separate periodic timer callback to process the fused data and publish it, our model handles this naturally. The subscriber callbacks form the ends of their respective upstream DAGs. The timer callback forms the root of a _new_ separate DAG, as its execution is triggered by its timer, not directly by the arrival of input messages via DDS. 

Now that we’ve established the mapping to a DAG task model, we next describe how to make use of the events executor to create a fixed-job-levelpriority scheduler. 

## **5 Executor Design** 

Prior work [14] demonstrated the usefulness of the new ROS 2 events executor for scheduling task chains on a uniprocessor. We now present a queueing mechanism for the events executor that enables ROS 2 to schedule general DAG tasks as well, with fixed-job-level-priority scheduling. 

In [14], a scheduler segregates a release thread from a scheduler thread. During DDS events, received messages insert an event object into a priority queue (also introduced in [14]). The decision about which subtask to release depends entirely on the implementation of the delegator’s priority queue. This is one of 

Fixed-Priority and EDF Schedules for ROS 2 Graphs on Uniprocessor 

9 

the primary benefits the events executor has over the original ROS 2 executor. By default, it is a FIFO scheduler. However, by replacing this events queue with compatible alternative implementations, other scheduling paradigms can be created. In a traditional first-task-priority scheduler (FTP), all subtasks in the graph (in our case, chain/tree) inherit the same priority as their parent. In a pub/sub system such as ROS 2, the linkage between parent and child is not readily apparent. Even if a ROS 2 executor tracked the relation between publisher and subscriber, a single topic can have multiple publishers. So a subtask may have multiple parents, with no obvious way to distinguish which triggered the release of an individual job. 

We propose a queueing mechanism that allows children to infer which parent triggered their execution and inherit the appropriate priority. It consists of 2 queues: 

**– Priority queue for root subtasks.** Released timer subtasks are kept in a min-heap (or max-heap) sorted by some fixed priority, such as their period for a rate-monotonic scheduler. This queue may include externally driven subscribers, if there is a mechanism to specify their priority. It is referenced in Algorithms 1 and 2 as _root_  queue_ 

- **LIFO queue for child subtasks.** All other subtasks, like subscriptions and services, are held in a LIFO queue. Each entry is paired with a priority, which is initially undefined, but is set on the next scheduling decision. This queue is also sorted by priority, per the discussion in Section 6. It is referenced in Algorithms 1 and 2 as _child_  queue_ 

The release logic is simply sorting a new subtask into the appropriate queue, as shown in Algorithm 1. Root subtasks are assumed to have some known priority (based on a period, deadline, or some fixed value), and child subtasks leave this value undefined. 

### **Algorithm 1** Release Logic 

- 1: **if** event.priority is defined _(event is timer)_ **then** 

- 2: root_queue.push(event) 

- 3: **else if** event.priority is undefined _(event is subscription)_ **then** 

- 4: event.priority = latest_priority 

- 5: child_queue.push(event) 

6: **end if** 

The scheduling logic is detailed in Algorithm 2. Whenever a job is scheduled, its priority is recorded. This is assumed to the be the priority of all subscribers released until the next scheduling decision. Any new subscribers that get released will inherit this priority at the next scheduling decision. 

When a subtask is scheduled, the DDS communication layer, which manages messages and communication, is queried for the message data to pass to the 

10 Oren Bell, Harun Teper, Mario Günzel, Chris Gill, and Jian-Jia Chen 

|**Al**|**gorithm 2** Scheduling Logic|
|---|---|
|1:|**if** root_queue.top.priority _>_ child_queue.top.priority **then**|
|2:|latest_priority = root_queue.top.priority|
|3:|schedule root_queue.pop()|
|4:|**else**|
|5:|latest_priority = child_queue.top.priority|
|6:|schedule child_queue.pop()|
|7:|**end if**|


subtask’s callback. To ensure that the correct instance of a subscriber is released, the underlying DDS layer also should be configured to release messages in LIFO ordering. Subscription events are released in LIFO order, but the messages they operate on are only passed to them after scheduling. Thus, it is crucial that the underlying DDS message queues are also LIFO ordered, since otherwise multiple instances of a single subscription may be assigned the wrong message at scheduling. This would be equivalent to running different jobs of a subtask out of order, which is undesirable. 

## **6 Analysis** 

In this section, we show that a ROS 2 application running on the events executor with our specialized queue implementation is analytically equivalent to a fixedpriority tree scheduler on a uniprocessor system. That is, the application will generate the same schedule as a conventional fixed-task-priority tree scheduler if given the unfolded equivalent of a ROS 2 application’s graph. We focus on limited preemption because ROS 2 executors cannot be preempted during the execution of a subtask, but subtasks from different trees are allowed to interleave, so the task as a whole has limited preemption. 

We first assume that subtasks at the root of a tree have some known integervalued priority for each job release. This may be a fixed priority, or can vary between job releases (such as a deadline for EDF). This priority is inherited by all subtasks. These root subtasks are naturally the first to run. In the following lemmas, we will lay out the natural ordering of scheduled subtasks and the priorities they have in association with each other. 

**Lemma 1.** _When idle, the only subtasks that may be eligible for release are the root subtasks of each tree._ 

_Proof._ Since the system idles, the two queues specified in Algorithms 1 and 2 are empty, by definition of a greedy scheduler. Since we stipulate that all child subtasks are released as soon as their parent complete, no new child tasks will become eligible after the last task has completed. Since the root subtasks are triggered periodically, they are the only ones that can be released when no other subtasks are running. 

11 

Fixed-Priority and EDF Schedules for ROS 2 Graphs on Uniprocessor 

**Lemma 2.** _Any newly released child subtask will have a priority equal to the subtask that just finished execution._ 

_Proof._ In our system model we require that children are released immediately upon the parent finishing and no later. Therefore it would be contradictory to assume anything other that the subtask that just finished is the parent of the child subtask that was released. By definition of FJP, a child inherits the priority of its parent. 

**Lemma 3.** _Any unscheduled subtask, τa, in the events queue must have a priority equal or lesser than the currently running subtask, τb._ 


_Proof._ By contradiction: Otherwise _τa_ would have been scheduled instead. Since our scheduler is nonpreemptive, no new events would have been enqueued by Algorithm 1 since the last scheduling decision. 

**Lemma 4.** _Any element placed into the children queue from Algorithm 1 will always be the highest priority element._ 

_Proof._ Any child subtasks, _τc_ , released at the completion of subtask _τb_ must have the same priority as subtask _τb_ , by Lemma 2. 


Therefore, applying Lemma 3, any already released subtask _τa_ must have a lower priority. 


We can impose the rule that ties are broken in LIFO order, based on release eligibility. 

**Lemma 5.** _Any element removed from the LIFO queue will always be the highest priority element._ 

_Proof._ Lemma 4 combined with definition of LIFO. 

**Theorem 1.** _The highest-priority subtask will always be scheduled next by Algorithm 2._ 

_Proof._ In Algorithm 2, only the top subtasks of the roots queue and children queue are compared. Per Lemma 5, the children queue is functionally a priority queue. Therefore, the two head subtasks have higher priority than any other subtasks in their respective queues. The greater of the two is guaranteed to be a higher priority than any released subtasks. Therefore, scheduling Algorithm 2 is guaranteed to schedule the highest priority released job. 

12 Oren Bell, Harun Teper, Mario Günzel, Chris Gill, and Jian-Jia Chen 

Additionally, this proof considers priorities of individual instances of subtasks to be independent from each other. Therefore, it’s compliant with any job-level fixed-priority scheduler. This assumes that all constraints we detailed in Section 4 are kept, and the DDS layer has been configured to release messages in LIFO order as well. 

### **6.1 Extension to non-LIFO queues** 

The events queue design in Section 5 above uses LIFO-ordering for new subscriber jobs. However, we are not aware of any ROS 2 communication middleware vendors that support LIFO message queues. This means that even when jobs are executed in the correct order, the messages for them to process would be given in the wrong order. This would be equivalent to running different jobs of a specific subtask out of order, which is undesirable. This work provides a motivating usecase for the implementation of LIFO message queuing. Even when LIFO queues are not available, a subset of applications are still schedulable. Specifically, if guarantees can be made that there will never be more than one released job of a task at a time, then the inversion from lacking a LIFO message queue never occurs. Such specific applications are detailed as follows. 

**Lemma 6.** _Any queue that always has at most one element is functionally a LIFO queue._ 

_Proof._ In a queue of size one, the only element able to be removed is the head element, so removing it abides by the LIFO definition. 

**Lemma 7.** _If a subscription C with response time RC is the only subscriber for a topic and its parents A, B, . . . , with response times RA, RB, . . . are harmonic with a_ sufficient _phase shift, then the message queue for that subscription’s topic will never have more than one message in it._ Sufficient _means that the taskset owning A, B, C, . . . is strictly periodic and_ 


_where tRx is the release time of x, occuring at timepoints ϕx_ + _kTx | k ∈_ N _. Without loss of generality, this extends to more than 2 parents by applying these conditions to each pair of parents._ 

_Proof._ A job/message _x_ is added to the queue at each job release, _tRx_ , and will be removed by the time that job completes _tRx_ + _Rx_ . 

The subscription task in question has a release time of _tRC_ = _tRA_ + _RA_ , where _A_ is the triggering parent. It is removed from the message queue by the pessimistic timepoint 


Fixed-Priority and EDF Schedules for ROS 2 Graphs on Uniprocessor 

13 

By the given conditions, this is earlier than the release of the next parent, _tRB_ . Therefore the queue will be empty by the time the next job is released. And that job will be removed before the next, and so on. 

The events queue will only have either zero or one jobs of this subscription. 

**Theorem 2.** _Even if the message queue isn’t configured to be LIFO order, the highest-priority subtask will always be scheduled next by Algorithm 2 if the conditions formulated in Lemma 7 hold._ 

_Proof._ If the conditions in Lemma 7 are true, then the message queue has a maximum size of one. Consequently, due to Lemma 6, the queue is functionally a LIFO queue. Hence, Theorem 1 can be applied. 

### **6.2 Applying Existing Schedulability Tests and Response Time Analysis** 

Our executor design implements a LP-FJP policy, where subtasks run nonpreemptively, but preemption can occur between subtasks. Furthermore, as shown in Section 4.3, ROS 2 graphs can be modeled as a forest of DAGs (trees) for analysis. Therefore, established analyses for LP-FJP scheduling of DAG tasks on uniprocessors are directly applicable. 

Specifically, the analysis provided by Nasri et al. [9] addresses this exact model (LP-FJP for DAGs). Their analysis tool [10] considers factors like release jitter and execution jitter, and supports multiprocessor analysis, though we focus on the uniprocessor case here. We utilize this specific analysis [9] in Section 7 to calculate the theoretical worst-case response times (WCRTs) for comparison with our experimental results. Using an analysis designed for the target scheduling policy (LP-FJP DAGs) is crucial for accurate validation, as opposed to analyses developed for different policies like the default ROS 2 executor [5]. 

When applying these analyses, one should use the **eligibility time** (the time a subtask _could_ run if the executor were free and it had highest priority) as the conceptual **release time** for the analysis calculation. The term ‘release time’ used elsewhere in this paper refers to the point in time when a subtask is enqueued into the events queue, which occurs at scheduling points. 

## **7 Evaluations** 

This evaluation is divided in two parts. In the first part, we implemented the queue detailed in Section 5 for a RM fixed priority scheduler, as well as one for EDF. We first apply the analysis provided by [9] to a synthetic taskset. If our executor truly maps to a Limited Preemption Fixed Job-Level Priority scheduler, we would expect their analysis to accurately bound WCRT. This bound is compared to an empirical evaluation is made in Section 7.1. 

We then present a more empirical measure of performance by assessing the performance of our proposed executor design from Section 5 compared to the existing events executor, as well as the default ROS 2 executor. We use the 

14 Oren Bell, Harun Teper, Mario Günzel, Chris Gill, and Jian-Jia Chen 

Autoware Reference Benchmark, which is intended to compare the performance of different executor designs. 

We are limited to a synthetic taskset and the Autoware Reference Benchmark because, as mentioned in Section 6.1, no communication middleware available provides LIFO-ordered message queueing, which violates the assumptions found in Lemma 5. The synthetic evaluation found in Section 7.1 is data-agnostic, so by tracing scheduling decisions, the hypothetically LIFO-ordered child subtasks can be reassigned to their correct parents in evaluation post-processing. The Autoware Reference Benchmark in Section 7.2 satisfies the condition in Lemma 7, therefore our analysis holds, according to Theorem 2. 

All experiments are ran on a Raspberry Pi Model 4, pinned to a single core with the timer’s management thread in the events executor assigned a higher priority, as suggested in [14]. We report the 99.7th percentile of response times to exclude rare outliers potentially caused by system noise (e.g., OS jitter) rather than by the scheduling algorithm itself. All experiments are conducted for 10 minutes, over multiple hyperperiods. 

### **7.1 Synthetic Many-to-Many Topic** 

To demonstrate that our analysis holds for an unfolded graph, we replicate the same application shown in Figure 3 and vary the WCETs of subtasks to create 3 different utilization levels. Utilization levels are approximate and rounded to even numbers for simplicity. Since this experiment does not use a LIFO-compliant middleware, we take measures to counteract the effect where subsequence jobs from a specific subtask are misordered. Since all data is arbitrary in this synthetic evaluation, jobs of a particular subtask are fungible. That is, if job _xi_ of subscription subtask _x_ is scheduled to run, it does not matter if it is given the data for job _xj_ instead, provided the WCET and priority match the intended job that should run. In post-processing, we identified when each child subtask was released (i.e., when its parent completed) and when it was scheduled. The response time is calculated as the difference between these two timestamps. This correctly measures the scheduling delay introduced by our executor, bypassing the message-data mismatch that would occur from a FIFO message queue. 

Each application is centered around a single topic with three publishers and two subscribers. Each publisher has a different period. After unfolding, we can model this application as a forest of 3 trees, each with 1 parent and 2 children. We created three variations of this taskset for different utilization levels of (approximately) 50%, 70%, and 90%. The WCET times for each subtask in each taskset are illustrated in Table 1. 

The unfolded forest is entered into an analysis tool [9,10], which provides a WCRT across the entire tree for each job with both RM and EDF scheduling. Results are shown in Figure 4. Our measured WCRTs closely match the predicted WCRTs from the analysis. The analysis for the 90% utilization scenario with RM scheduling predicts deadline misses for Task A and Task B, which highlights that the task set is not schedulable under these conditions. Our executor’s behavior aligns with this analysis. 

Fixed-Priority and EDF Schedules for ROS 2 Graphs on Uniprocessor 

15 

Table 1: WCET of Subtasks in Synthetic Tasksets 

||Paren|t by P|eriod|Chil|dren|
|---|---|---|---|---|---|
|Utilization|25ms|41ms|51ms|A|B|
|50%|1ms|1ms|5ms|2ms|2ms|
|70%|2ms|1ms|12ms|2ms|2ms|
|90%|3ms|1ms|12ms|2ms|4ms|


Fig. 4: Response times for the synthetic task set compared against the WCRT bounds from analysis [9]. Task A, B, and C correspond to the root tasks with periods 25ms, 41ms, and 51ms, respectively. Red lines indicate the analytical WCRT. 

### **7.2 Autoware Reference Benchmark** 

We also compare our performance to existing executors in the Autoware Reference Benchmark, a simulated version of the Autoware application detailed in [11], which includes interconnected timers and subscriptions.<sup>4</sup> Specifically, we measure the end-to-end latency of the **hot path** defined in the benchmark from the front and rear LiDAR sensors to the object collision estimator (c.f. the Autoware reference system), as this latency is a key metric for responsiveness in crash avoidance. The data at the start of the hot path is generated at a frequency of 10Hz. 

Results are shown in Figure 5. The default and events executor perform the worst, but are still consistently within the implicit 100ms deadline of the hotpath. However, with our RM and EDF modifications to the events executor, the worst case is consistently under 25ms. This represents a 63% improvement over the default executor, and a 61% improvement over the events executor. In addition to a better WCET, there is less variability as well. 

## **8 Conclusions and Future Work** 

Prior literature [2,5,6,13,16] has catered to the limitations of the default ROS 2 executor. They quantify its behavior and propose multithreaded work-arounds 

> 4 `https://github.com/ros-realtime/reference-system/blob/main/autoware_ reference_system/README.md` 

- 16 Oren Bell, Harun Teper, Mario Günzel, Chris Gill, and Jian-Jia Chen 


Fig. 5: Autoware Reference Benchmark Executor Comparison 

rather than directly addressing the blocking caused by the processing window. In contrast, our work builds on the events executor, which isn’t affected by the processing window. Scheduling decisions are made after each executed job, making it compliant with a limited-preemption scheduler. Additionally, the responsetime analysis provided by prior literature has focused on chains. Our work not only provides support for general branching graphs, but it does so with minimal retooling required and without the need for a priori application analysis and graph decomposition, as is the case with PiCAS [6]. 

This paper introduces a novel abstraction with which ROS 2 applications can be analyzed as forests of trees. It also presents a new design for an events queue that supports arbitrary fixed-job-level-priority schedulers, and naturally honors the precedence relations between subtasks without needing to be aware of them. Finally, it provides an analysis proving that the events executor using our queue is behaviorally identical to a conventional scheduler operating on the unfolded equivalent of our application. Our analysis and empircal evaluation confirm that the schedules created are identical (subject to arbitrary tie-breaks). This further closes the gap between established real-time literature and ROS 2 scheduling analysis. 

The primary limitation to this work is the necessity for a LIFO message queue, which is not to our knowledge provided by any commercially available or open-source DDS middleware. Integrating that feature into an existing opensource middleware framework is a natural direction for future work, to broaden the applicability of the approach presented here beyond the currently targeted set of applications meeting Theorem 2’s conditions (e.g., harmonic periods). Future work could also explore extending this model to mixed-criticality systems or handling other preemption constraints. 

Fixed-Priority and EDF Schedules for ROS 2 Graphs on Uniprocessor 17 

## **References** 

1. A. A. Arafat, S. Vaidhun, K. M. Wilson, J. Sun, and Z. Guo. Response time analysis for dynamic priority scheduling in ROS2. In _Design Automation Conference DAC_ , pages 301–306, 2022. 

2. T. Blaß, D. Casini, S. Bozhko, and B. B. Brandenburg. A ROS 2 response-time analysis exploiting starvation freedom and execution-time variance. In _Real-Time Systems Symposium, RTSS_ , pages 41–53, 2021. 

3. J. Blum and F. Drewes. Language theoretic properties of regular dag languages. _Information and Computation_ , 265:57–76, 2019. 

4. G. C. Buttazzo. _Hard Real-Time Computing Systems - Predictable Scheduling Algorithms and Applications, 4th Edition_ . Springer, 2024. 

5. D. Casini, T. Blaß, I. Lütkebohle, and B. B. Brandenburg. Response-time analysis of ROS 2 processing chains under reservation-based scheduling. In _Euromicro Conference on Real-Time Systems, ECRTS_ , pages 6:1–6:23, 2019. 

6. H. Choi, Y. Xiang, and H. Kim. Picas: New design of priority-driven chain-aware scheduling for ROS2. In _IEEE Real-Time and Embedded Technology and Applications Symposium, RTAS_ , pages 251–263, 2021. 

7. J. C. Fonseca, V. Nélis, G. Raravi, and L. M. Pinho. A multi-dag model for real-time parallel applications with conditional execution. In _ACM Symposium on Applied Computing, Salamanca, Spain, April 13-17, 2015_ , pages 1925–1932. ACM, 2015. 

8. iRobot. Events executor. `https://github.com/irobot-ros/events-executor` , 2022. last access on Nov. 17th, 2024. 

9. M. Nasri, G. Nelissen, and B. B. Brandenburg. Response-time analysis of limitedpreemptive parallel DAG tasks under global scheduling. In _Euromicro Conference on Real-Time Systems, ECRTS_ , pages 21:1–21:23, 2019. 

10. G. Nelissen. Np schedulability analysis. `https://github.com/gnelissen/ np-schedulability-analysis` . last access on Nov. 17th, 2024. 

11. ROS2 Real-time Working Group. Autoware reference system. `https://github. com/ros-realtime/reference-system` . last access on Nov. 17th, 2024. 

12. M. A. Serrano, A. Melani, M. Bertogna, and E. Quiñones. Response-time analysis of DAG tasks under fixed priority scheduling with limited preemptions. In _Design, Automation & Test in Europe Conference & Exhibition, DATE_ , pages 1066–1071, 2016. 

13. Y. Tang, Z. Feng, N. Guan, X. Jiang, M. Lv, Q. Deng, and W. Yi. Response time analysis and priority assignment of processing chains on ROS2 executors. In _Real-Time Systems Symposium, RTSS_ , pages 231–243, 2020. 

14. H. Teper, O. Bell, M. Günzel, C. Gill, and J. Chen. Reconciling ROS 2 with classical real-time scheduling of periodic tasks. In _31st IEEE Real-Time and Embedded Technology and Applications Symposium, RTAS 2025, Irvine, CA, USA, May 6-9, 2025_ , pages 177–189. IEEE, 2025. 

15. H. Teper, T. Betz, G. von der Brüggen, K.-H. Chen, J. Betz, and J.-J. Chen. Timing-aware ROS 2 architecture and system optimization. In _International Conference on Embedded and Real-Time Computing Systems and Applications, RTCSA_ , pages 206–215, 2023. 

16. H. Teper, M. Günzel, N. Ueter, G. von der Brüggen, and J.-J. Chen. End-to-end timing analysis in ROS2. In _IEEE Real-Time Systems Symposium, RTSS_ , pages 53–65, 2022. 

- 18 Oren Bell, Harun Teper, Mario Günzel, Chris Gill, and Jian-Jia Chen 

17. M. Verucchi, I. S. Olmedo, and M. Bertogna. A survey on real-time DAG scheduling, revisiting the global-partitioned infinity war. _Real Time Syst._ , 59(3):479–530, 2023. 

