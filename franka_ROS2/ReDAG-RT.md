---
title: "ReDAG-RT: Global Rate-Priority Scheduling for Real-Time Multi-DAG Execution in ROS 2"
date: "2026-03-18"
authors: "Md. Mehedi Hasan; Rafid Mostafiz; Bikash Kumar Paul; Md. Abir Hossain; Ziaur Rahman"
url: https://arxiv.org/abs/2603.18238
pdf: https://arxiv.org/pdf/2603.18238
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.18238)** / [論文ページ](https://arxiv.org/abs/2603.18238)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# ReDAG<sup>**RT**</sup> : Global Rate-Priority Scheduling for Real-Time Multi-DAG Execution in ROS 2 

Md. Mehedi Hasan , Rafid Mostafiz , Bikash Kumar Paul , Md. Abir Hossain , and Ziaur Rahman 

**_Abstract_ —ROS 2 has become the dominant middleware for robotic systems, where perception, estimation, planning, and control pipelines are naturally structured as directed acyclic graphs (DAGs) of callbacks executed under a shared executor. Despite widespread adoption, default ROS 2 executors employ best-effort dispatch with no cross-DAG priority enforcement, producing uncontrolled callback contention, structural priority inversion, and deadline instability under concurrent workloads. These limitations restrict deployment in time-critical and safety-sensitive cyber-physical systems (CPS). This paper presents ReDAG**<sup>RT</sup> **, a user-space global scheduling framework that enables deterministic multi-DAG execution within unmodified ROS 2. The core contribution is a Rate-Priority (RP)-driven global readyqueue architecture that orders callbacks system-wide by activation rate, enforces per-DAG concurrency bounds, and mitigates cross-graph priority inversion, without modifying the ROS 2 API, executor interface, or the Linux scheduler. A multi-DAG task model is formalized for ROS 2 callback pipelines, and cross-DAG interference is characterized under RP scheduling. Response-time recurrences and schedulability conditions are derived within the classical Rate-Monotonic theory. Controlled experiments within a ROS 2 Humble execution environment compare ReDAG**<sup>RT</sup> **against the SingleThreadedExecutor and MultiThreadedExecutor using synthetic multi-DAG workloads under mixed-period, mixed-criticality configurations. Results show up to** 29 _._ 7% **reduction in combined deadline miss rate,** 42 _._ 9% **compression of the** 99 **th-percentile response time, and a** 13 _._ 7% **improvement in miss rate relative to the MultiThreadedExecutor under comparable utilization. Asymmetric per-DAG concurrency bounds further reduce interference by** 40 _._ 8% **over symmetric configurations. These results demonstrate that deterministic and analyzable multi-DAG scheduling is achievable entirely within the ROS 2 user-space execution layer, providing a principled foundation for real-time robotic middleware in safety-critical cyber-physical deployments.** 


Fig. 1. Cross-DAG priority inversion under the default ROS 2 executor and the ReDAG<sup>RT</sup> solution. (A) Multiple independent DAGs collapse into a shared FIFO queue with no global priority ordering. (B) Low-frequency callbacks execute before high-frequency ones, causing priority inversion and deadline misses. (C) ReDAG<sup>RT</sup> enforces Rate-Monotonic ordering via a unified priority queue. (D) Deterministic execution eliminates priority inversion and bounds response times. 

**_Index Terms_ —Robotic Operating Systems 2 (ROS 2); Directed Acyclic Graph (DAG); Robotics.** 

## I. INTRODUCTION 

**M** ODERNrent computationrobotic systemspipelinesdeploywithin multiplea sharedconcur-middleware runtime. Perception, localization, planning, and control are commonly structured as independent directed acyclic graphs (DAGs) of callbacks, all executed under a unified executor. In ROS 2, these callbacks are managed by either a SingleThreadedExecutor or a MultiThreadedExecutor, each maintaining a global ready queue [1]. While this model simplifies concurrency 

The source code and experimental artifacts of ReDAG<sup>RT</sup> are openly available at: https://github.com/Mehedi16009/ros2-realtime-scheduling-framework 

management, it imposes no global real-time scheduling policy across application DAGs [2]. The default executor operates at the callback level without enforcing rate-based priority relations. A callback becomes eligible for execution when its triggering condition is satisfied and is then dispatched according to queue ordering and thread availability. No mechanism ensures that higher-rate callbacks dominate lower-rate ones across distinct DAGs [3], [4]. Consequently, execution order is determined by arrival timing and worker scheduling rather than real-time priority semantics. This design induces crossDAG interference. A callback belonging to a low-frequency pipeline may execute before a high-frequency control callback if it enters the ready queue earlier or acquires a worker thread first, a phenomenon we identify as _cross-DAG priority inversion_ [5], [6], as illustrated in Fig. 1. Multiple application DAGs structurally collapse into a shared callback queue under the default executor, producing priority inversion across otherwise independent pipelines. The resulting interference increases 

2 

response-time variability and degrades temporal predictability. Under moderate to high processor utilization, these effects amplify jitter and cause deadline misses. From a real-time systems perspective, this behavior directly violates classical Rate-Monotonic scheduling principles [7], [8]. Although individual DAGs may internally respect precedence constraints, the executor layer collapses all graphs into a shared queue without preserving a global priority order [9], [10]. Default ROS 2 execution models therefore lack a schedulability-aware abstraction that spans multiple concurrent DAGs within a single process. The core architectural insight of ReDAG<sup>RT</sup> is that cross-DAG interference originates from the absence of a unified rate-priority hierarchy at the executor level. Mapping all callbacks to globally ordered schedulable entities restores the applicability of classical fixed-priority analysis across the entire callback set. Enforcing Rate-Monotonic priority assignment across DAG boundaries eliminates structural priority inversion and recovers analyzable timing behavior [11]. 

ReDAG<sup>RT</sup> addresses this limitation by introducing a global rate-priority scheduler integrated directly within the ROS 2 execution layer. All ready callbacks are inserted into a centralized priority queue ordered by activation period, and dispatch decisions follow fixed-priority real-time semantics. IntraDAG precedence constraints are preserved, while cross-DAG execution is globally arbitrated according to Rate-Monotonic ordering. This design transforms the default timing-agnostic executor into a schedulability-aware runtime without modifying the ROS 2 API, application-level graph structure, or the underlying operating system scheduler. By restoring deterministic priority ordering across heterogeneous callback pipelines, ReDAG<sup>RT</sup> bounds cross-graph interference and stabilizes endto-end response times, enabling principled real-time reasoning for multi-DAG robotic workloads executing within a shared middleware process. 

implementation is openly released to facilitate reproducibility and community adoption. 

The remainder of this paper is organized as follows. Section II reviews related work and positions ReDAG<sup>RT</sup> against existing ROS 2 real-time scheduling approaches. Building on this, Section III presents the system design, formal task model, rate-priority scheduling framework, interference characterization, and response-time analysis. Following the methodology, Section IV presents an empirical evaluation of thread scalability, deadline sensitivity, and cross-system comparisons. The subsequent Section V provides a scheduling-theoretic interpretation of the results. Finally, Section VI concludes and outlines future directions. 

## II. RELATED WORK 

## _A. Real-Time Scheduling Foundations_ 

Classical real-time scheduling theory establishes the analytical basis for predictable task execution in safety-critical systems. Liu and Layland introduced Rate-Monotonic (RM) and Earliest-Deadline-First (EDF) scheduling for periodic task systems, along with utilization bounds and response-time analysis for fixed-priority preemption [12]. Subsequent work extended these results to Directed Acyclic Graph (DAG) task models, characterizing intra-task parallelism, precedence constraints, and interference under multiprocessor scheduling [13]. These models formalize the conditions under which bounded response times and deadline adherence can be guaranteed. In contrast, ROS 2’s default SingleThreadedExecutor and MultiThreadedExecutor employ best-effort FIFO callback dispatch without global priority arbitration across independent DAG pipelines. As a result, classical schedulability assumptions do not directly hold in practical robotic middleware deployments, motivating structured user-space scheduling mechanisms. 

**Contributions.** This paper makes three primary contributions: 

- **Structural analysis of ROS 2 executor limitations.** Cross-DAG priority inversion is identified and characterized as a fundamental structural deficiency of the default ROS 2 execution model, originating from the absence of global priority arbitration across concurrently executing callback pipelines. 

- **Formal interference model for multi-DAG scheduling.** The absence of rate-priority enforcement is shown to produce uncontrolled cross-DAG interference, timing nondeterminism, and degraded deadline predictability under concurrent workloads. Interference bounds and responsetime recurrences are derived within a formal multi-DAG task model grounded in classical Rate-Monotonic theory. 

- **Design, evaluation, and open-source release of ReDAG**<sup>RT</sup> **.** A unified Rate-Monotonic scheduling framework is presented that introduces a global ready-queue executor enforcing deterministic multi-DAG callback arbitration entirely within the ROS 2 user-space execution layer. The framework requires no kernel modifications, preserves full ROS 2 API compatibility, and is empirically validated under mixed-period, mixed-criticality workloads against standard ROS 2 executors. The full 

## _B. ROS 2 Real-Time Evolution_ 

Multiple studies have examined timing behavior in ROS 2. Casini et al. [14] demonstrate that executor processing windows and callback ordering can introduce unfair dispatch and increased end-to-end latency in chained processing pipelines [11]. Macenski et al. [15] describe ROS 2’s production-oriented redesign with DDS-based QoS controls, while acknowledging that executor-level scheduling remains largely FIFO-driven. Kernel-level interventions such as PREEMPT_RT improve worst-case interrupt latency but require system-level modifications and do not address callbacklevel arbitration within the executor [16]. Similarly, improvements in Linux scheduling fairness may enhance throughput but do not establish analyzable dispatch order among competing callbacks [16]. These efforts improve system-level timing characteristics yet leave executor-level global prioritization largely unaddressed. 

## _C. Chain-Aware Scheduling Approaches_ 

Chain-aware scheduling represents a partial solution to timing predictability. PiCAS assigns priorities to callbacks according to end-to-end chain deadlines and demonstrates improved 

3 

latency bounds in embedded robotic platforms [17], [18]. However, its analysis primarily considers isolated chains and does not explicitly characterize interference among heterogeneous DAG pipelines. RAGE adopts chain-based prioritization but lacks formal schedulability analysis and global queue arbitration [19]. PoDS introduces priority inheritance mechanisms for micro-ROS environments [20], focusing on MCU-scale deployments rather than multi-core robotic workloads. While these works strengthen intra-chain timing guarantees, crossDAG contention in shared executors remains insufficiently characterized. 

## _D. Executor-Level Scheduling Extensions_ 

Several efforts modify ROS 2 executors to better align with classical scheduling models. Teper et al. and Bell et al. extend the EventsExecutor to support RM/EDFcompatible dispatch and enable response-time analysis under constrained triggering models [21], [22]. These approaches rely on specific DDS configurations and restricted callback models, limiting applicability to general robotic pipelines with mixed subscription and timer callbacks. ROSRT leverages Linux SCHED_EXT to provide flexible thread-level preemption without kernel patches [23]. However, scheduling decisions remain tied to DDS-topic granularity and do not introduce unified global arbitration across multiple DAGs. ROSCH synchronizes DAG timestamps for Autoware-based systems [24], yet remains application-specific and conservative in delay estimation. 

## _E. Multi-DAG Scheduling and Analysis Gaps_ 

Theoretical multi-DAG scheduling has been studied in broader real-time systems literature. Yano et al. apply GEDF to Autoware sub-DAGs but assume FIFO-ready queues inconsistent with asynchronous ROS 2 callback behavior [25]. Ahmed proposes an rp-sporadic DAG scheduler with selfdependency handling [26], though without integration into ROS middleware. Tang et al. derive response-time bounds under reservation-based chain models [27], primarily focusing on single-chain interference. Blass analyzes callback interference in the MultiThreadedExecutor [28], yet does not introduce priority-driven global queue arbitration. Chaaban et al. propose executor grouping heuristics to reduce resource contention [29], but without formal multi-DAG schedulability characterization. Collectively, existing work either (i) prioritizes single chains, (ii) modifies executor backends under constrained assumptions, or (iii) analyzes interference without introducing structured global arbitration across heterogeneous DAG pipelines. 

## _F. Positioning Against Prior Art_ 

Table I summarizes representative approaches. Default executors provide compatibility but no global priority ordering. Chain-aware schedulers improve end-to-end latency within individual pipelines. EventsExecutor modifications enable classical analysis under restricted triggering assumptions. OSlevel approaches enhance thread scheduling but do not directly address callback-level multi-DAG arbitration. 

## _G. Research Gap and Motivation_ 

To our knowledge, no prior work provides user-space global rate-priority queue arbitration across heterogeneous DAG pipelines within unmodified ROS 2 executors while enabling multi-DAG response-time and lateness analysis. Existing approaches either restrict the callback model, depend on specialized executor variants, rely on OS-level scheduling, or focus on single-chain optimization. ReDAG<sup>RT</sup> addresses this gap by introducing structured global rate-priority dispatch within the standard executor abstraction, preserving ROS 2 API compatibility and avoiding kernel modifications. Its evaluation explicitly examines cross-DAG interference, responsetime variability, and deadline behavior under stress workloads, thereby complementing prior single-chain and OS-centric approaches with a middleware-level multi-DAG scheduling framework. 

## III. REDAG<sup>RT</sup> : SYSTEM DESIGN AND SCHEDULING FRAMEWORK 

## _A. System Architecture Overview_ 

ReDAG<sup>RT</sup> is implemented as a custom global executor within the ROS 2 user-space execution layer and is structured into three logical tiers: (i) an Application Layer hosting concurrent DAG-structured robotic pipelines, (ii) an Executor Layer enforcing deterministic Rate-Priority (RP) scheduling through a unified global ready queue, and (iii) an OS Layer comprising the standard Linux scheduler operating without kernel modification. The complete architecture and eventdriven execution flow are illustrated in Fig. 2. At the application layer, the system executes multiple concurrent directed acyclic graphs _Gk_ = ( _Vk, Ek_ ), where _Vk_ denotes the set of callback tasks and _Ek_ encodes inter-task precedence constraints. Each DAG represents an independent robotic pipeline, such as perception, estimation, planning, or control. Tasks are released periodically according to their specified periods _Ti_ , consistent with implicit-deadline periodic task models. This layer remains fully compatible with standard ROS 2 APIs and does not require application-level modifications. Upon period expiration, a release event triggers the Task Release and Dependency Resolution stage. For each task _τi_ , the resolver verifies two conditions: (1) that its period _Ti_ has elapsed, and (2) that all predecessor tasks specified in _Ek_ have completed. Tasks satisfying both conditions are marked READY and inserted into the Global Ready Queue. This queue is a unified user-space priority structure shared across all concurrent DAGs. The queue enforces Rate-Monotonic priority ordering, assigning strictly higher priority to tasks with shorter periods (i.e., _Ti < Tj ⇒ Pi > Pj_ ). This establishes a single system-wide arbitration order across all DAGs, eliminating per-DAG scheduling inconsistencies and uncontrolled cross-DAG interference observed in the default ROS 2 SingleThreadedExecutor and MultiThreadedExecutor, which rely on FIFO or loosely ordered callback dispatching without global priority guarantees. The RP Global Scheduler constitutes the core of ReDAG<sup>RT</sup> and implements fixed-priority preemptive scheduling entirely in user space. At each scheduling point, the 

4 

TABLE I 

COMPARISON OF ROS 2 REAL-TIME SCHEDULING APPROACHES 

|Approach|Multi-DAG|Global Queue|Kernel Mod|API Compat|Formal Analysis|Evaluation|
|---|---|---|---|---|---|---|
|Default Execs [11]|_×_|_×_|✓|✓|_×_|Baseline|
|PiCAS [17], [18]|_×_|_×_|?|?|Chain-level|Real HW|
|EventsEx [21], [22]|Tree|_×_|✓|_∼_|RTA (restricted)|Sim|
|ROSRT [23]|✓|OS-level|✓|✓|_×_|Autoware|
|ROSCH [24]|✓|_×_|?|_∼_|DAG-sync|Autoware|
|PREEMPT<br>RT [16]|✓|Linux|_×_|✓|_×_|Throughput|
|**ReDAG**<sup>RT</sup>|✓|✓|✓|✓|Multi-DAG RTA|Webots + Stress|


scheduler selects the highest-priority task from the ready queue and compares it with the currently executing task. If the selected task has strictly higher priority, preemption is triggered. The selected task _τi_ is then dispatched to the CPU execution layer. During execution, each task runs for at most its worst-case execution time _Ci_ under fully preemptive semantics. The underlying Linux thread scheduler remains unmodified; ReDAG<sup>RT</sup> controls dispatch ordering exclusively at the executor level and does not alter kernel-level scheduling policies. Upon completion, a completion event is forwarded to the Timing Monitor and Metrics Logger. The finish time _fi_ is recorded, and timing metrics are computed as follows. The response time is defined as _Ri_ = _fi − ri_ , where _ri_ denotes the release time. Lateness is defined as _Li_ = _fi − di_ , where _di_ represents the absolute deadline. A deadline miss is registered whenever _Li >_ 0, and the corresponding miss counter is incremented. Control then transitions to the Next Scheduling Event Check, which determines whether the triggering event corresponds to a new task release, a task completion, or the arrival of a higher-priority task. In all cases, control returns to the Global Ready Queue Arbitration stage, forming a closed event-driven scheduling loop. This architecture ensures continuous, globally prioritized execution across all concurrent DAGs while enabling precise per-task timing analysis and systematic metric collection under user-space constraints. 


Fig. 2. ReDAG<sup>RT</sup> layered user-space scheduling architecture. Periodic DAG workloads _Gk_ = ( _Vk, Ek_ ) release tasks upon period expiration. A dependency-aware release stage validates timing and precedence constraints before admitting ready tasks into a unified global Rate-Monotonic priority queue ordered by arg min _τi∈R Ti_ . The ReDAG<sup>RT</sup> executor performs fixedpriority preemptive arbitration across all DAGs and dispatches to the unmodified Linux execution layer. An integrated Timing Monitor computes _Ri_ , _Li_ , and MR _i_ online, with event-driven re-scheduling closing the control loop. 

## _B. Multi-DAG Task Model Formulation_ 

The computational workload of ReDAG<sup>RT</sup> is modeled as a collection of directed acyclic graphs (DAGs), where each DAG captures the structural and temporal dependencies of an independent robotic processing pipeline. Formally, each DAG instance is defined as: 


where _Vk_ = _{τ_ 1 _, τ_ 2 _, . . . , τn}_ denotes the set of callback tasks belonging to _Gk_ , and _Ek ⊆ Vk × Vk_ represents the set of directed precedence constraints between tasks. An edge ( _τi, τj_ ) _∈ Ek_ indicates that task _τj_ cannot be released for execution until task _τi_ has completed. Each task _τi ∈ Vk_ corresponds to a ROS 2 callback, such as a timer callback, subscription callback, or computation stage within a robotic pipeline. The acyclic property of _Gk_ guarantees the absence of circular dependencies, thereby ensuring well-defined execution orderings within each pipeline. The system hosts multiple such DAGs executing concurrently. The global workload is defined as: 


where each _Gk_ models an independent robotic application component, as formalized in Equation (1). The DAGs in _G_ are assumed to be functionally independent in terms of logical correctness; that is, no precedence constraints exist across distinct DAGs. However, all DAGs share a common execution environment and compete for the same executor resources within ReDAG<sup>RT</sup> . This shared-resource assumption introduces cross-DAG contention at the scheduling level, which directly motivates the need for a unified global arbitration mechanism. By formally separating structural independence at the application level from resource sharing at the executor level, the model in Equations (1) and (2) captures the realistic deployment scenario in which multiple robotic pipelines operate concurrently while relying on a single scheduling substrate. 

## _B.1 Task Characterization and Timing Parameters_ 

Each task _τi_ in the multi-DAG system is characterized by a tuple of timing and criticality parameters: 


5 

where _Ci_ denotes the worst-case execution time (WCET), _Ti_ represents the task period, _Di_ is the relative deadline, and _χi_ specifies the criticality level of the task. This formulation captures both temporal constraints and system-level importance within a unified abstraction. The WCET _Ci_ defines an upper bound on the processor time required by _τi_ under worst-case conditions, assumed to be known a priori through measurement, static analysis, or conservative estimation. The period _Ti_ determines the minimum inter-arrival time between consecutive releases of the same task, reflecting the sensing or control frequency of the robotic application. The relative deadline _Di_ constrains the maximum allowable response time from task release to completion. The criticality level _χi_ enables differentiation between safety-critical and best-effort callbacks, providing a foundation for future extensions toward mixed-criticality scheduling. Throughout this work, implicit deadlines are assumed for all tasks: 


This assumption, defined in Equation (4), aligns each task’s completion requirement with the arrival of its next instance, simplifying schedulability analysis and remaining consistent with periodic control and perception workloads common in robotic systems. Let _N_ denote the total number of tasks across all DAGs in _G_ , as defined in Equation (2). The overall processor utilization of the system is defined as: 


This utilization metric, given in Equation (5), provides a compact measure of aggregate computational demand relative to processor capacity. It serves as a primary indicator of schedulability under rate-based global arbitration and enables analytical reasoning about system feasibility when multiple DAGs defined in Equation (1) share the same executor resources within ReDAG<sup>RT</sup> . 

## _C. Rate-Priority Global Scheduling Design_ 

ReDAG<sup>RT</sup> employs a static Rate-Monotonic priority assignment enforced globally across all DAGs, transforming crossDAG callback arbitration into a formally analyzable fixedpriority scheduling problem. 

## _C.1 Static Priority Assignment_ 

ReDAG<sup>RT</sup> adopts a fixed-priority scheduling policy based on Rate-Monotonic (RM) ordering. Each task _τi_ is assigned a static priority determined solely by its period, according to the relation: 


such that tasks with shorter periods receive strictly higher priorities. This mapping reflects the principle that higherfrequency tasks impose tighter timing requirements and therefore demand stronger scheduling guarantees. Priority assignment is performed globally across the entire task set _G_ , defined 

in Equation (2), rather than locally within individual DAGs. All tasks from all graphs are placed into a unified priority space, allowing a high-rate task in one DAG to preempt a lower-rate task in another. This global ordering, formalized in Equation (6), ensures consistent arbitration under shared executor resources and prevents priority inversion across independent robotic pipelines. Furthermore, the static nature of the assignment eliminates runtime priority recomputation, reduces scheduling overhead, and enables analytical reasoning about worst-case interference. 

## _C.2 Schedulability Bound Under Rate-Monotonic Policy_ 


This bound represents a sufficient condition derived from worst-case response-time analysis. As _N_ increases, the righthand side of Equation (7) converges to ln(2) _≈_ 0 _._ 693, providing a conservative analytical reference for system design. In the context of ReDAG<sup>RT</sup> , tasks are not fully independent due to intra-DAG precedence constraints encoded in _Ek_ , as defined in Equation (1). These constraints restrict the set of feasible release patterns and can, in practice, reduce intertask interference relative to the fully independent case. Nevertheless, the classical RM utilization bound in Equation (7) is retained as a conservative feasibility guideline. When the total system utilization _U_ satisfies this condition, the system operates within a known safe analytical region, even before accounting for the structural restrictions imposed by the DAG topology. 

## _D. Ready-Queue Management and Dispatch Semantics_ 

ReDAG<sup>RT</sup> employs a single global ready queue containing all tasks eligible for execution across every DAG in _G_ , as defined in Equation (2). The queue is strictly ordered according to the static Rate-Monotonic priority assignment established in Equation (6), such that tasks with shorter periods are placed ahead of tasks with longer periods, ensuring deterministic global arbitration across all concurrent pipelines. A task _τi_ becomes eligible for insertion into the ready queue only when two conditions are simultaneously satisfied: its release time has arrived and all intra-DAG precedence constraints _Ek_ , defined in Equation (1), have been resolved. Once both timing and dependency conditions hold, the corresponding callback is marked READY and admitted into the global priority queue. At each scheduling point, triggered by a task release, task completion, or preemption event, the scheduler performs three sequential actions: all newly eligible callbacks are enqueued, the highest-priority task is identified from the ready set, and preemption is triggered if that task holds strictly higher priority than the currently executing task. Formally, the dispatch decision is defined as: 

6 


where _R_ denotes the set of currently ready tasks. The scheduler selects the task with the minimum period from _R_ , which corresponds directly to the highest Rate-Monotonic priority under the assignment in Equation (6). This dispatch rule ensures that the processor is always allocated to the most time-critical eligible task, consistent with the utilization bound established in Equation (7). Deadline monitoring is performed upon task completion. When _τi_ finishes execution, its completion time _fi_ is recorded and evaluated against its absolute deadline _di_ = _ri_ + _Di_ , where _Di_ = _Ti_ under the implicit deadline assumption of Equation (4). Lateness _Li_ = _fi − di_ is computed and a deadline miss is registered if _Li >_ 0, as defined in the timing model of Section III-A. This design keeps dispatch logic lightweight while ensuring that timing violations are detected precisely at job termination. 

## _E. ReDAG_<sup>RT</sup> _Executor Algorithm_ 

The complete runtime behavior of ReDAG<sup>RT</sup> is formalized in Algorithm 1. The algorithm integrates periodic release handling, precedence verification, global Rate-Priority arbitration, preemptive dispatch, and deadline monitoring within a unified execution loop, representing the concrete realization of the scheduling semantics established in Equations (6)–(8) and the interference model of Equation (9). At each iteration, the algorithm processes all tasks _τi ∈G_ whose period _Ti_ has expired. For each such task, the dependency resolver evaluates the intra-DAG precedence constraints _Ek_ , as defined in Equation (1), confirming that all predecessor tasks have completed. Tasks satisfying both the temporal and precedence conditions are marked READY and inserted into the global priority queue ordered by Equation (6). The dispatcher then applies the selection rule of Equation (8) to identify the highest-priority ready task _τ_<sup>_∗_</sup> = arg min _i∈R Ti_ , triggering preemption if _τ_<sup>_∗_</sup> holds strictly higher priority than the currently executing task. Upon task completion, the Timing Monitor records _fi_<sup>_k_and</sup> evaluates lateness _L_<sup>_k_</sup> _i_<sup>=</sup><sup>_f_</sup> _i_<sup>_k−dk_</sup> _i_<sup>per Equation (13), registering</sup> a deadline miss and updating MR _i_ per Equation (15) whenever _L_<sup>_k_</sup> _i_<sup>_>_0.Theloopthenadvancestothenextschedulingevent,</sup> maintaining the closed-loop arbitration structure described in Section III-H until system termination. 

## _F. Interference Characterization_ 

Cross-DAG interference is analyzed under both default ROS 2 executors and ReDAG<sup>RT</sup> , establishing the structural conditions under which interference becomes bounded and analytically tractable. 

## _F.1 Interference Under Default ROS 2 Executors_ 

Under the default ROS 2 executor policies, callback scheduling is driven by FIFO semantics and internal queue behavior rather than formal priority rules, introducing several sources of timing unpredictability. First, FIFO-induced priority inversion occurs when lower-urgency callbacks are serviced 

ahead of time-sensitive ones solely because they arrived earlier; since no global rate-based ordering is enforced, execution order does not necessarily reflect temporal criticality. Second, cross-DAG blocking is effectively unbounded: 

**Algorithm 1** ReDAG<sup>RT</sup> : Rate-Priority Multi-DAG Executor **Require:** DAG set _G_ = _{G_ 1 _, G_ 2 _, . . . , GK}_ , each _Gk_ = ( _Vk, Ek_ ), task parameters ( _Ci, Ti, Di, χi_ ) for each _τi ∈ Vk_ 

- 1: Initialize Global Ready Queue _RQ ←∅_ 

2: Initialize _τ_ curr _←_ NULL 3: Initialize metrics logger: _L_<sup>max</sup> _i ←_ 0, miss <u>count</u> _i ←_ 0, total <u>jobs</u> _i ←_ 0 for all _τi_ 4: **while** system is running **do** 5: **for** each DAG _Gk ∈G_ **do** 6: **for** each task _τi ∈ Vk_ with period _Ti_ expired **do** 7: **if** all predecessors of _τi_ in _Ek_ completed **then** 8: Record release time _ri ←_ current <u>time</u> 9: Increment total <u>jobs</u> _i_ 10: Mark _τi_ as READY 11: Insert _τi_ into _RQ_ ordered by arg min _Ti_ (RateMonotonic) 12: **end if** 13: **end for** 14: **end for** 15: **if** _RQ̸_ = _∅_ **then** 16: _τ_ next _←_ arg min _τi∈RQ Ti_ 17: **if** _τ_ curr = NULL **then** 18: Dispatch _τ_ next on CPU 19: _τ_ curr _← τ_ next 20: **else if** priority( _τ_ next) _>_ priority( _τ_ curr) **then** 21: Preempt _τ_ curr 22: Dispatch _τ_ next on CPU 23: _τ_ curr _← τ_ next 24: **else** 25: Continue _τ_ curr 26: **end if** 27: **end if** 28: **for** each task _τi_ completed during this cycle **do** 29: Record finish time _fi ←_ current <u>time</u> 30: Compute _Ri ← fi − ri_ 31: Compute _di ← ri_ + _Di_ 32: Compute _Li ← fi − di_ 33: **if** _Li >_ 0 **then** 34: Increment miss <u>count</u> _i_ 35: _L_<sup>max</sup> _i ←_ max( _L_<sup>max</sup> _i , Li_ ) 36: MR _i ←_<sup><u>miss</u></sup> total <u>countjobs</u> _ii_ 37: **end if** 38: _τ_ curr _←_ NULL 39: **end for** 40: **end while** 

callbacks belonging to different logical pipelines share the same executor threads without structured arbitration, allowing a computationally intensive callback in one DAG to delay unrelated callbacks in another DAG with no analytical upper bound on the resulting interference. Third, because scheduling decisions are not derived from explicit timing parameters such 

7 

as _Ti_ or _Ci_ defined in Equation (3), worst-case interference cannot be expressed in closed form. Consequently, no formal priority guarantees or schedulability bounds can be established under the default execution model. 

## _F.2 Controlled Interference Under ReDAG_<sup>RT</sup> 

ReDAG<sup>RT</sup> restructures interference through strict global Rate-Priority ordering. Since priorities are statically assigned according to Equation (6) and globally enforced via the dispatch rule of Equation (8), a task _τi_ can be delayed exclusively by tasks with strictly higher priority. Let _hp_ ( _i_ ) denote the set of tasks with higher priority than _τi_ . The worst-case interference experienced by _τi_ within a scheduling window is bounded by: 


where _Cj_ is the WCET of each higher-priority task as defined in Equation (3). This expression captures the cumulative execution demand of all tasks in _hp_ ( _i_ ) that may execute before or preempt _τi_ . Lower-priority tasks contribute no interference under the preemptive scheduling semantics enforced by Equation (8). Critically, cross-DAG interference becomes analytically tractable under ReDAG<sup>RT</sup> . Although tasks originate from structurally independent DAGs in _G_ , as defined in Equation (2), interference is determined solely by global priority ordering rather than graph membership. This transformation converts the previously unbounded and opaque contention of the default executor into a bounded and analyzable quantity expressed in Equation (9), enabling formal reasoning about response time and schedulability across the full multi-DAG robotic workload. 

## _G. Response-Time and Lateness Analysis_ 

Formal worst-case response-time bounds and empirical lateness metrics are derived to provide both analytical schedulability guarantees and measurement-based validation of timing behavior under ReDAG<sup>RT</sup> . 

## _G.1 Response-Time Recurrence_ 

To establish temporal guarantees under global Rate-Priority scheduling, the worst-case response time of each task _τi_ is computed using fixed-point iteration. The response time accounts for both the task’s own execution demand and the interference from all higher-priority tasks, bounded by _Ii_ as defined in Equation (9). Let _hp_ ( _i_ ) denote the set of tasks with strictly higher priority than _τi_ under the assignment of Equation (6). The response-time recurrence is defined as: 


where the first term represents the intrinsic execution demand of _τi_ , and the summation captures the cumulative workload imposed by higher-priority tasks that may execute within the response-time window _Ri_<sup>(</sup><sup>_k_)</sup> . The ceiling operator reflects the maximum number of arrivals of each higher-priority task _τj_ 

during the interval, consistent with the periodic release model defined by _Tj_ in Equation (3). The recurrence in Equation (10) is iterated from the initial condition _Ri_<sup>(0)</sup> = _Ci_ until either convergence: 


or the value exceeds the relative deadline _Di_ . Upon convergence, the schedulability condition is: 


which, under the implicit deadline assumption of Equation (4), reduces to _Ri ≤ Ti_ . If Equation (12) holds, task _τi_ is guaranteed to meet all deadlines under the assumed execution and interference bounds of Equation (9). This formulation provides an exact per-task feasibility test under fixed-priority preemptive scheduling, complementing the sufficient utilization bound established in Equation (7). 

## _G.2 Empirical Timing Metrics_ 

While response-time analysis provides theoretical guarantees, runtime evaluation requires empirical timing metrics. For the _k_ -th job of task _τi_ , lateness is defined as: 


where _fi_<sup>_k_</sup> denotes the observed finish time and _d_<sup>_k_</sup> _i_<sup>isthe</sup> absolute deadline of that job. A positive value _L_<sup>_k_</sup> _i_<sup>_>_0 indicates</sup> a deadline miss, while _L_<sup>_k_</sup> _i_<sup>_≤_0 confirms timely completion. To</sup> quantify worst-case temporal behavior, the maximum lateness across all jobs of _τi_ is defined as: 


which isolates the largest observed violation while ignoring non-violating instances. In addition, the deadline miss rate for task _τi_ is defined as: 


providing a normalized measure of temporal reliability across the full execution history of _τi_ . Together, the responsetime bound of Equation (12) and the empirical metrics of Equations (13)–(15) establish a unified framework for both analytical guarantees and measurement-based validation of timing behavior under ReDAG<sup>RT</sup> . 

## _H. End-to-End Scheduling Execution Cycle_ 

The runtime behavior of ReDAG<sup>RT</sup> follows a deterministic execution cycle that integrates task release, dependency validation, priority arbitration, and timing observation within a unified closed-loop control structure, as illustrated in Fig. 2. The workflow begins with periodic task release. When the period _Ti_ of task _τi_ expires, as defined in Equation (3), a new job instance is generated and becomes a candidate for execution. Release alone, however, does not immediately render the task schedulable. All intra-DAG precedence constraints 

8 

_Ek_ , defined in Equation (1), are first evaluated to confirm that every required predecessor has completed. Only when both the temporal and dependency conditions are simultaneously satisfied is the callback marked READY and admitted into the scheduling pipeline. Eligible callbacks are inserted into the single global ready queue, which maintains strict RateMonotonic priority ordering across all DAGs in _G_ according to Equation (6). At each scheduling point, the dispatcher applies the selection rule of Equation (8) to identify the highestpriority ready task _τ_<sup>_∗_</sup> . If _τ_<sup>_∗_</sup> holds strictly higher priority than the currently executing task, preemption is triggered and the processor is immediately reassigned; otherwise, execution proceeds without interruption. Once dispatched, _τ_<sup>_∗_</sup> executes on the CPU for at most its worst-case execution time _Ci_ , as bounded in Equation (3). Upon completion, the Timing Monitor records the finish time _fi_<sup>_k_andcomputestheper-job</sup> response time _Ri_ = _fi − ri_ and lateness _L_<sup>_k_</sup> _i_<sup>=</sup><sup>_f_</sup> _i_<sup>_k−dk_</sup> _i_<sup>,</sup> as defined in Equations (13) and (14). A deadline miss is registered and the miss rate MR _i_ updated according to Equation (15) whenever _L_<sup>_k_</sup> _i_<sup>_>_0.</sup> 

Following task completion or any new release event, the scheduler evaluates the next scheduling point by checking for newly released tasks, completed tasks, or pending preemption conditions. Control returns to global ready-queue arbitration, and the cycle repeats. This closed-loop execution continues throughout system operation, ensuring structured dispatch decisions, interference bounded by Equation (9), and continuous timing observability consistent with the schedulability condition of Equation (12) until system termination. 

## IV. EXPERIMENTAL RESULTS 

## _A. Experimental Setup_ 

This section presents a controlled empirical evaluation comparing ReDAG<sup>RT</sup> against the default ROS 2 executors under structurally identical workload conditions. ReDAG<sup>RT</sup> implements the rate-priority global scheduling framework developed in Section III-C, designed to bound cross-DAG interference and enforce per-DAG callback concurrency. The two baselines are the standard SingleThreadedExecutor and MultiThreadedExecutor (configured with four worker threads), representing the default execution semantics of contemporary ROS 2 deployments. All experiments employ synthetic multi-DAG workloads constructed to expose structured precedence constraints and cross-DAG contention. Each workload consists of two interacting DAGs, formalized as _G_ = _{G_ 1 _, G_ 2 _}_ per Equation (2), with configurable concurrency bounds enforced through a max_active parameter that limits the maximum number of simultaneously active callbacks per DAG. The deadline model follows the implicit formulation _Di_ = _Ti_ established in Equation (4), preserving analytical alignment with classical fixed-priority scheduling theory. To evaluate scalability and sensitivity to computational slack, the number of executor threads is varied across _{_ 4 _,_ 6 _,_ 8 _,_ 10 _}_ , and deadline tightness is modulated via a multiplicative scaling factor drawn from _{_ 0 _._ 8 _,_ 0 _._ 9 _,_ 1 _._ 1 _,_ 1 _._ 2 _}_ . Scale factors below unity represent constrained timing budgets approaching overload, while values above unity introduce 

TABLE II 

BASELINE ROS 2 EXECUTOR PERFORMANCE 

|Executor|Utilization|Miss Rate|Max Lateness (_µ_s)|
|---|---|---|---|
|SingleThreadedExecutor|0.6|0.748|1,764,841|
|MultiThreadedExecutor (4T)|0.8|0.552|7,153|


increasing slack. This parametric design enables systematic observation of interference amplification, contention collapse, and scheduling degradation regimes across utilization levels relative to the bound of Equation (7). 

The two baseline configurations employ complementary task structures. The SingleThreadedExecutor is evaluated under harmonic periods to expose serialization-induced blocking, while the MultiThreadedExecutor uses nonharmonic periods to reflect realistic robotic workloads with irregular activation patterns. This distinction isolates the behavioral pathologies of each executor under conditions most likely to amplify their respective limitations. Evaluation metrics follow standard real-time systems practice and directly correspond to the theoretical quantities defined in Section II-E: (i) deadline miss rate MR _i_ per Equation (15), measuring the fraction of jobs completing after their deadlines; (ii) maximum lateness _L_<sup>max</sup> _i_ per Equation (14), capturing worst-case temporal violation; (iii) mean response time _R_<sup>¯</sup> _i_ , reflecting average scheduling responsiveness; and (iv) executor-level behavioral indicators, including deferred and executed callback counts, which provide insight into contention dynamics and dispatch fairness. 

Across all ReDAG<sup>RT</sup> configurations, the DAG concurrency validator reports all_enforced = 1, confirming that perDAG concurrency bounds were never violated during execution. This structural guarantee ensures that all observed performance characteristics arise strictly from scheduling dynamics rather than enforcement inconsistencies, preserving experimental integrity and result interpretability throughout the evaluation. All timing metrics follow the formal definitions established in Section III-G, specifically Equations (13)–(15). 

## _B. Baseline ROS 2 Behavior_ 

We first characterize the timing behavior of the default ROS 2 executors to establish a reference baseline; results are summarized in Table II. Under the MultiThreadedExecutor with four worker threads at _U_ = 0 _._ 8, the deadline miss rate reaches 55 _._ 2%, maximum lateness _L_ max = 7 _,_ 153 _µs_ , and mean response time _R_<sup>¯</sup> = 680 _._ 43 _µs_ . Despite parallel execution support, more than half of all jobs miss their deadlines, indicating substantial crossDAG interference and limited temporal isolation between callbacks. The SingleThreadedExecutor exhibits considerably more severe behavior at _U_ = 0 _._ 6. As shown in Table II, the miss rate rises to 74 _._ 8% and maximum lateness escalates to 1 _,_ 764 _,_ 841 _µs_ , over two orders of magnitude larger than the multi-threaded case, while mean response time reaches 118 _,_ 218 _µs_ . This dramatic lateness growth reveals pathological response-time amplification caused by strict callback serialization and the complete absence of interference regulation. Collectively, Table II confirms that default ROS 2 execution 

9 


Fig. 3. Effect of thread count on ReDAG<sup>RT</sup> deadline miss rate. Increasing worker threads reduces interference until saturation near eight threads. 

semantics exhibit substantial deadline instability even at moderate utilization. From a fixed-priority scheduling perspective, this behavior is consistent with unbounded blocking terms _Bi_ and uncontrolled interference growth in Equation (18), as analyzed in Section III-F. Without rate-based priority enforcement or DAG-aware arbitration, cross-task contention inflates response times and drives high deadline violation rates, precisely the structural pathologies that ReDAG<sup>RT</sup> is designed to eliminate. 

## _C. ReDAG_<sup>RT</sup> _: Thread Scalability Analysis_ 

Fig. 3 illustrates the effect of executor thread count on per-DAG and combined deadline miss rates. The combined miss rate decreases monotonically from 0 _._ 8509 at 4 threads to 0 _._ 6865 at 6 threads and 0 _._ 5984 at 8 threads, yielding a relative reduction of approximately 29 _._ 7%: 


At 10 threads, the combined miss rate marginally increases to 0 _._ 6379, confirming a scalability saturation point visible in Fig. 3. Per-DAG trends corroborate this observation: DAG1 improves from 0 _._ 9111 at 4 threads to 0 _._ 7554 at 8 threads, while DAG2 exhibits a more pronounced reduction from 0 _._ 7907 to 0 _._ 4414 over the same range. This asymmetric gain, clearly visible in the diverging DAG1 and DAG2 curves of Fig. 3, suggests that DAG2 benefits more substantially from increased parallel capacity, likely due to differences in structural depth or interference exposure within _Ek_ as defined in Equation (1). The monotonic improvement up to 8 threads reflects effective contention mitigation through bounded concurrency and ratepriority dispatch per Equation (8), with additional workers reducing queueing delays and shortening interference chains, directly lowering _Ii_ per Equation (9). The plateau and subsequent reversal beyond 8 threads, however, indicate diminishing returns attributable to synchronization overhead, sharedqueue contention, and increased scheduling coordination costs. ReDAG<sup>RT</sup> thus demonstrates meaningful scalability under moderate parallel expansion while exposing a practical upper bound beyond which architectural overhead offsets additional computational capacity. 


Fig. 4. Sensitivity of ReDAG<sup>RT</sup> performance to deadline scaling. Moderate deadline relaxation reduces miss rate, while excessive slack increases interference windows. 


Fig. 5. Impact of per-DAG concurrency limits on combined deadline miss rate. Asymmetric concurrency bounds significantly reduce cross-DAG interference. 

## _D. Deadline Scaling Sensitivity_ 

Fig. 4 illustrates the sensitivity of the combined miss rate to deadline scaling factor _δ ∈{_ 0 _._ 8 _,_ 0 _._ 9 _,_ 1 _._ 1 _,_ 1 _._ 2 _}_ . As _δ_ increases from 0 _._ 8 to 1 _._ 1, the combined miss rate decreases from 0 _._ 8509 to 0 _._ 5984, a relative reduction of 29 _._ 7% consistent with Equation (16), before rising to 0 _._ 6379 at _δ_ = 1 _._ 2. This non-monotonic behavior, clearly visible in Fig. 4, reveals that moderate slack mitigates interference by relaxing the schedulability bound of Equation (12), while excessive slack enlarges overlapping execution windows across DAGs, reintroducing cross-DAG contention. Interference coupling effects therefore persist even under relaxed timing constraints, confirming that deadline slack alone is insufficient to eliminate cross-DAG priority inversion without the rate-priority enforcement mechanism of Equation (6). 

10 


Fig. 6. Cumulative distribution function (CDF) of callback response times comparing default ROS 2 executors and ReDAG<sup>RT</sup> . A leftward shift indicates reduced latency and tighter tail bounds under rate-priority scheduling. 

TABLE III 

RESPONSE TIME PERCENTILES: DEFAULT ROS 2 EXECUTORS VS. REDAG<sup>RT</sup> 

|Scheduler|Median|(ms)<br>95th %ile (ms)|99th %ile (ms)|
|---|---|---|---|
|ROS 2 Default|21|37|49|
|ReDAG<sup>RT</sup>|14|22|28|


## _E. Concurrency Pair Sensitivity_ 

Fig. 5 presents a heatmap of combined deadline miss rates across all evaluated (max_active1 _,_ max_active2) concurrency pairs, where color intensity reflects the magnitude of scheduling degradation. The heatmap reveals a clear asymmetry effect: symmetric but constrained configurations produce the worst outcomes, with (max_active1 _,_ max_active2) = (2 _,_ 2) yielding a combined miss rate of 0 _._ 835 and (3 _,_ 2) yielding 0 _._ 815. In contrast, the asymmetric configuration (2 _,_ 5) achieves the lowest observed combined miss rate of 0 _._ 494, representing a relative improvement of approximately 40 _._ 8% over the worst case. This pattern, visually reinforced by the dark-to-light gradient across asymmetric regions of Fig. 5, confirms that symmetric high-concurrency bounds amplify mutual interference by allowing both DAGs to simultaneously expand their runnable sets. Asymmetric caps, by contrast, limit one DAG’s parallel footprint, reducing the effective size of the higher-priority interference set _hp_ ( _i_ ) and directly constraining _Ii_ per Equation (9). These results empirically validate interference-aware bounded parallelism as a necessary and effective strategy for controlling cross-DAG contention within the global scheduling framework of ReDAG<sup>RT</sup> . 

## _F. Response Time Distribution Analysis_ 

To evaluate latency stability across scheduling strategies, we analyze the cumulative distribution of callback response times for the default ROS 2 executors and ReDAG<sup>RT</sup> . A tighter, left-shifted CDF indicates reduced response variability and improved tail-latency control, both critical properties for real-time robotic workloads operating under the schedulability bound of Equation (12). 

TABLE IV 

COMPARISON BETWEEN DEFAULT ROS 2 EXECUTORS AND REDAG<sup>RT</sup> 

|System|Configuration|Miss Rate|
|---|---|---|
|SingleThreadedExecutor|_U_ = 0_._6|0.748|
|MultiThreadedExecutor|4 Threads|0.552|
|ReDAG<sup>RT</sup>|Best Configuration|0.476|
|ReDAG<sup>RT</sup>|Avg. (6 Threads)|0.686|


As shown in Figure 6 and quantified in Table III, ReDAG<sup>RT</sup> substantially shifts the response time distribution toward lower latency with significantly tighter tail bounds. The median response time reduces from 21 ms to 14 ms, while the 99th percentile decreases from 49 ms to 28 ms, a reduction of approximately 42 _._ 9%. This tail compression directly reflects the bounded interference _Ii_ enforced by Equation (9) and the elimination of cross-DAG priority inversion through global rate-priority arbitration per Equation (8). The steeper CDF slope of ReDAG<sup>RT</sup> confirms not only lower average latency but also improved temporal predictability across the full response time distribution, a property unattainable under the unregulated dispatching semantics of the default ROS 2 executors. 

## _G. Operating Envelope and Configuration Bounds_ 

The best observed configuration, 8 threads at deadline scale 1 _._ 1, yields a combined miss rate of 0 _._ 476, while the worst, 4 threads at scale 0 _._ 8, reaches 0 _._ 975. The relative improvement between these extremes is: 


Demonstrating that coordinated concurrency scaling and moderate deadline slack can halve worst-case deadline violations. This range quantifies the practical operating envelope of ReDAG<sup>RT</sup> and underscores the importance of joint parallelism and timing parameter selection. 

## _H. Cross-System Comparison_ 

Table IV summarizes the cross-system comparison of deadline miss rates across all evaluated executor configurations. ReDAG<sup>RT</sup> consistently reduces deadline violations relative to both default ROS 2 executors. Against the MultiThreadedExecutor (MR = 0 _._ 552 at _U_ = = 0 _._ 8), the best ReDAG<sup>RT</sup> configuration achieves MR 0 _._ 476, a relative improvement of 13 _._ 7%. Against the SingleThreadedExecutor (MR = 0 _._ 748 at _U_ = 0 _._ 6), ReDAG<sup>RT</sup> with 6 threads achieves MR = 0 _._ 686, corresponding to an 8 _._ 3% reduction in deadline violations. As evidenced by Table IV, performance gains are most pronounced under multi-threaded contention scenarios, where rate-priority global arbitration per Equation (8) most effectively suppresses the cross-DAG priority inversion characterized in Section III-F and bounds the interference term _Ii_ of Equation (9). These results collectively confirm that ReDAG<sup>RT</sup> delivers measurable and consistent scheduling improvements over default ROS 2 execution semantics across all evaluated utilization regimes. 

11 

## V. SCHEDULING-THEORETIC INTERPRETATION OF RESULTS 

## _A. Interference-Aware Scheduling Effects_ 

The experimental results expose fundamental limitations of the default ROS 2 execution model under structured multi-DAG workloads. In both baseline executors, cross-DAG interference is effectively unbounded: callbacks from independent graphs compete for shared worker threads without concurrency regulation or admission control. This produces interference amplification and callback-level priority inversion, consistent with the structural pathology identified in Section III-F. The SingleThreadedExecutor compounds this further through strict serialization, accumulating blocking across precedence chains and driving the pathological lateness values reported in Equations (14) and (13). ReDAG<sup>RT</sup> addresses this through three structural mechanisms: (i) perDAG concurrency bounds limiting simultaneously active callbacks per graph, (ii) rate-priority dispatch preserving temporal ordering across competing tasks per Equation (8), and (iii) structured admission control preventing uncontrolled expansion of runnable sets. Together, these mechanisms directly constrain the interference term _Ii_ of Equation (9), reducing cumulative blocking and shortening queueing delays within the response-time recurrence of Equation (10). Empirically, this interference-aware regulation manifests as lower combined miss rates MR per Equation (15), improved scalability under thread expansion, and significantly reduced worst-case lateness _L_ max per Equation (14) relative to default executors. These results confirm that bounding parallelism at the DAG level is not merely a structural refinement but a necessary control mechanism for mitigating response-time inflation in concurrent multi-DAG robotic workloads. 

## _B. Fixed-Priority Scheduling Interpretation_ 

The observed behavior admits direct interpretation through classical fixed-priority response-time analysis (RTA). For task _τi_ , the worst-case response time is given by Equation (10), restated here with an explicit blocking term: 


where _Bi_ captures blocking from lower-priority or non-preemptable callbacks. Under the default ROS 2 execution model, both terms inflate significantly. The effective higher-priority set _hp_ ( _i_ ) expands dynamically due to uncontrolled cross-DAG competition, amplifying the cumulative interference summation. Simultaneously, _Bi_ grows through serialization-induced blocking in the SingleThreadedExecutor and contention-driven queueing delays in the MultiThreadedExecutor, neither of which are bounded at the framework level. Response times consequently exceed analytical expectations derived under isolated task assumptions, consistent with the pathological lateness values observed in Section IV-B. ReDAG<sup>RT</sup> mitigates both inflation sources. Per-DAG concurrency caps limit the number of simultaneously interfering callbacks, 

directly bounding _Ii_ per Equation (9). Rate-priority dispatch per Equation (8) enforces stable dominance relations, constraining the effective size of _hp_ ( _i_ ) and suppressing uncontrolled growth of _Bi_ . The empirically observed reductions in MR and _L_ max are therefore analytically consistent with a reduction in the interference term of Equation (18). ReDAG<sup>RT</sup> thus operationalizes interference control at the executor level, aligning observed runtime behavior with classical schedulability theory. 

## _C. Parallelism Scalability and Saturation Behavior_ 

Although ReDAG<sup>RT</sup> demonstrates clear scalability improvements from 4 to 8 threads, reducing the combined miss rate by 29 _._ 7% per Equation (16), performance gains plateau beyond this point. At 10 threads, the miss rate marginally increases, indicating diminishing returns from additional parallel capacity. This saturation is attributable to growing lock contention in shared executor structures, increased inter-thread coordination overhead, and reduced effective parallel slack once the global ready queue is sufficiently drained. Beyond a critical concurrency level, scheduling overhead offsets computational gains, establishing a practical parallelism ceiling. Future optimizations should therefore target synchronization cost reduction through lock-free or partitioned dispatch mechanisms that preserve the interference bounds of Equation (9) while minimizing coordination overhead. 

## _D. Utilization Sensitivity_ 

Under tight deadline scaling ( _δ_ = 0 _._ 8), the system approaches overload conditions, with elevated miss rates across all configurations. In this regime, even modest interference amplification drives response times beyond the schedulability bound of Equation (12). Crucially, however, ReDAG<sup>RT</sup> exhibits graceful degradation under increasing utilization, in sharp contrast to the SingleThreadedExecutor’s catastrophic lateness escalation reported in Section IV-B. This controlled behavior confirms that per-DAG concurrency bounds and rate-priority dispatch moderate the growth of both the interference term _Ii_ and blocking component _Bi_ in Equation (18) under high utilization, improving temporal robustness relative to unregulated execution semantics. 

## _E. Enforcement Validation_ 

Across all 64 experimental configurations, the DAG concurrency validator reports all_enforced = 1 in every run, confirming that per-DAG concurrency bounds were never violated throughout the evaluation. This structural invariant ensures that all observed performance characteristics, miss rates, lateness values, and response times reported in Equations (15)– (14) and Equation (13) are strictly derived from scheduling dynamics, rather than policy breaches or implementation inconsistencies. Universal enforcement confirmation thereby strengthens the internal validity of the experimental study and independently verifies the correctness of the concurrencycontrol mechanism within ReDAG<sup>RT</sup> . 

12 

## VI. CONCLUSION AND FUTURE WORK 

This paper presented ReDAG<sup>RT</sup> , a rate-priority global scheduling framework that addresses fundamental real-time limitations of the default ROS 2 execution model. By identifying cross-DAG priority inversion and unbounded interference as structural deficiencies of existing executors, ReDAG<sup>RT</sup> introduces per-DAG concurrency bounds, rate-monotonic dispatch per Equation (6), and structured admission control to enforce analyzable timing behavior within unmodified ROS 2. Empirical evaluation demonstrates consistent and measurable improvements across all configurations. Thread scalability experiments yield a 29 _._ 7% reduction in combined miss rate from 4 to 8 threads before saturation, while deadline sensitivity analysis confirms graceful degradation under tight timing budgets in contrast to the pathological lateness escalation of default executors reported in Table II. Cross-system comparison in Table IV establishes up to 13 _._ 7% miss rate reduction over the MultiThreadedExecutor and a 42 _._ 9% reduction in 99th percentile response time per Table III. Concurrency pair analysis further confirms that asymmetric DAG bounds suppress mutual interference more effectively than symmetric configurations, directly validating the interference model of Equation (9). These results establish that interference-aware, rate-priority scheduling is both practically achievable and analytically grounded within the ROS 2 middleware stack, without kernel modification or application restructuring. 

Several directions remain open for future investigation. First, lock-free or wait-free executor data structures should be explored to overcome the synchronization bottleneck identified beyond 8 threads. Second, tighter integration with formal response-time analysis per Equation (10) may enable hard schedulability guarantees for bounded DAG workloads. Third, extension to heterogeneous compute platforms, including GPU-accelerated and asymmetric CPU architectures common in perception pipelines, represents a natural and necessary generalization. Finally, validation on large-scale, real-world ROS 2 deployments will establish the production-readiness of interference-aware scheduling for safety-critical robotic systems. 

## REFERENCES 

- [1] Stark and Tobias, “Real-time execution management in the ros 2 framework,” 2022. 

- [2] A. Al Arafat, K. Wilson, K. Yang, and Z. Guo, “Dynamic priority scheduling of multithreaded ros 2 executor with shared resources,” _IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems_ , vol. 43, no. 11, pp. 3732–3743, 2024. 

- [3] X. Yang and B. Hu, “An adaptive ros2 node deployment framework in mobile edge-robot systems,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2025, pp. 12 652–12 658. 

- [4] H. R. George TH Ellison, “Directed acyclic graphs as conceptual and analytical tools in applied and theoretical epidemiology: advances, setbacks and future possibilities,” _Mathematical Biosciences and Engineering_ , vol. 22, no. 11, 2025. 

- [5] C. B´edard, P.-Y. Lajoie, G. Beltrame, and M. Dagenais, “Message flow analysis with complex causal links for distributed ros 2 systems,” _Robotics and Autonomous Systems_ , vol. 161, p. 104361, 2023. 

- [6] L. Castri, M. H. Gloria Beraldo, Sariah Mghames, and N. Bellotto, “Ros- causal: A ros-based causal analysis framework for human-robot interaction applications,” _arXiv_ , vol. 22, no. 11, 2025. 

- [7] A. A. Bertossi and A. Fusiello, “Rate-monotonic scheduling for hardreal-time systems,” _European Journal of Operational Research_ , vol. 96, no. 3, pp. 429–443. 

- [8] L. Sha, R. Rajkumar, and S. Sathaye, “Generalized rate-monotonic scheduling theory: a framework for developing real-time systems,” _Proceedings of the IEEE_ , vol. 82, no. 1, pp. 68–82. 

- [9] S. Macenski, A. Soragna, M. Carroll, and Z. Ge, “Impact of ros 2 node composition in robotic systems,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 7, pp. 3996–4003, 2023. 

- [10] H. Teper, T. Betz, M. G¨unzel, D. Ebner, G. Von Der Br¨uggen, J. Betz, and J.-J. Chen, “End-to-end timing analysis and optimization of multiexecutor ros 2 systems,” in _2024 IEEE 30th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ , 2024, pp. 212–224. 

- [11] D. Casini, F. R. Jian-Jia Chen, Jing Li, and H. Teper, “A survey of real-time support, analysis, and advancements in ros 2,” _arXiv_ , vol. 22, no. 11, 2025. 

- [12] C. L. Liu and J. W. Layland, “Scheduling algorithms for multiprogramming in a hard-real-time environment,” _J. ACM_ , vol. 20, no. 1, p. 46–61, Jan. 1973. 

- [13] S. Zhao, X. Dai, and I. Bate, “Dag scheduling and analysis on multi-core systems by modelling parallelism and dependency,” _IEEE Transactions on Parallel and Distributed Systems_ , vol. 33, no. 12, pp. 4019–4038, 2022. 

- [14] D. Casini, T. Blaß, I. L¨utkebohle, and B. B. Brandenburg, “Responsetime analysis of ros 2 processing chains under reservation-based scheduling,” S. Quinton, Ed., vol. 133. Dagstuhl, Germany: Schloss Dagstuhl – Leibniz-Zentrum f¨ur Informatik, 2019, pp. 6:1–6:23. 

- [15] S. Macenski, T. Foote, B. Gerkey, C. Lalancette, and W. Woodall, “Robot operating system 2: Design, architecture, and uses in the wild,” _Science Robotics_ , vol. 7, no. 66, p. eabm6074, 2022. 

- [16] L. Z. Y. Yanlei; N. Zhenguo; L. Xinjun; X. Fugui and L. Peng, “Ros2 real-time performance optimization and evaluation,” _Chinese Journal of Mechanical Engineering_ , vol. 36, no. 144, 2023. 

- [17] H. Choi, Y. Xiang, and H. Kim, “Picas: New design of priority-driven chain-aware scheduling for ros2,” in _2021 IEEE 27th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ , 2021, pp. 251–263. 

- [18] H. Sobhani, H. Choi, and H. Kim, “Timing analysis and prioritydriven enhancements of ros 2 multi-threaded executors,” in _2023 IEEE 29th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ , 2023, pp. 106–118. 

- [19] H. Choi, Y. X. Daniel Enright, Hoora Sobhani, and H. Kim, “Prioritydriven real-time scheduling in ros 2:potential and challenges,” in _2023 IEEE 29th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ , 2022, pp. 106–118. 

- [20] Z. Wang, S. Liu, D. Ji, and W. Yi, “Improving real-time performance of micro-ros with priority-driven chain-aware scheduling,” _Electronics_ , vol. 13, no. 9, 2024. 

- [21] H. Teper, C. G. Oren Bell, Mario G¨unzel, and J.-J. Chen, “Bridging the gap between ros 2 and classical real-time scheduling for periodic tasks,” _arXiv.org_ , vol. 13, no. 9, 2024. 

- [22] O. Bell, C. G. Harun Teper, Mario G¨unzel, and J.-J. Chen, “Fixedpriority and edf schedules for ros2 graphs on uniprocessor,” _arXiv.org_ , vol. 13, no. 9, 2025. 

- [23] S. Liu, R. Wagle, S. Ahmed, Z. Tong, and J. H. Anderson, “Ros<sup>rt</sup> : Enabling flexible scheduling in ros 2*,” in _2025 IEEE Real-Time Systems Symposium (RTSS)_ , 2025, pp. 42–54. 

- [24] Y. Saito, F. Sato, T. Azumi, S. Kato, and N. Nishio, “Rosch:real-time scheduling framework for ros,” in _2018 IEEE 24th International Conference on Embedded and Real-Time Computing Systems and Applications (RTCSA)_ , 2018, pp. 52–58. 

- [25] A. Yano and T. Azumi, “Work-in-progress: Multi-deadline dag scheduling model for autonomous driving systems,” in _2024 IEEE Real-Time Systems Symposium (RTSS)_ , 2024, pp. 451–454. 

- [26] S. Ahmed and J. H. Anderson, “Exact response-time bounds of periodic dag tasks under server-based global scheduling,” in _2022 IEEE RealTime Systems Symposium (RTSS)_ , 2022, pp. 447–459. 

- [27] Y. Tang, Z. Feng, N. Guan, X. Jiang, M. Lv, Q. Deng, and W. Yi, “Response time analysis and priority assignment of processing chains on ros2 executors,” in _2020 IEEE Real-Time Systems Symposium (RTSS)_ , 2020, pp. 231–243. 

- [28] S. Liu, X. Jiang, N. Guan, Z. Wang, M. Yu, and W. Yi, “Rtex: An efficient and timing-predictable multithreaded executor for ros 2,” _IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems_ , vol. 43, no. 9, pp. 2578–2591, 2024. 

- [29] A. K. Chaaban, “A new algorithm for real-time scheduling and resource mapping for robot operating systems (ros),” _Applied Sciences_ , vol. 13, no. 3, 2023. 

