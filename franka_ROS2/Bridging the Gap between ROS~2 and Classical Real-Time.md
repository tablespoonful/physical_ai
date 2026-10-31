---
title: "Bridging the Gap between ROS~2 and Classical Real-Time Scheduling for Periodic Tasks"
date: "2024-08-07"
authors: "Harun Teper; Oren Bell; Mario Günzel; Chris Gill; Jian-Jia Chen"
url: https://arxiv.org/abs/2408.03696
pdf: https://arxiv.org/pdf/2408.03696
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2408.03696)** / [論文ページ](https://arxiv.org/abs/2408.03696)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Bridging the Gap between ROS 2 and Classical Real-Time Scheduling for Periodic Tasks 

Harun Teper<sup>1</sup> , Oren Bell<sup>2</sup> , Mario G¨unzel<sup>1</sup> , Chris Gill<sup>2</sup> , and Jian-Jia Chen<sup>13</sup> 

> 1 TU Dortmund University, Germany 

> 2 Washington University in St Louis, USA 

> 3 Lamarr Institute for Machine Learning and Artificial Intelligence, Germany 

Emails: _{_ harun.teper, mario.guenzel, jian-jia.chen _}_ @tu-dortmund.de and _{_ oren.bell, cdgill _}_ @wustl.edu 

**_Abstract_ —The Robot Operating System 2 (ROS 2) is a widely used middleware that provides software libraries and tools for developing robotic systems. In these systems, tasks are scheduled by ROS 2 executors. Since the scheduling behavior of the default ROS 2 executor is inherently different from classical real-time scheduling theory, dedicated analyses or alternative executors, requiring substantial changes to ROS 2, have been required.** 

**In 2023, the events executor, which features an** **_events queue_ and allows the possibility to make scheduling decisions immediately after a job completes, was introduced into ROS 2. In this paper, we show that, with only minor modifications of the events executor, a large body of research results from classical real-time scheduling theory becomes applicable. Hence, this enables analytical bounds on the worst-case response time and the end-to-end latency, outperforming bounds for the default ROS 2 executor in many scenarios. Our solution is easy to integrate into existing ROS 2 systems since it requires only minor backend modifications of the events executor, which is natively included in ROS 2. The evaluation results show that our ROS 2 events executor with minor modifications can have significant improvement in terms of dropped jobs, worst-case response time, end-to-end latency, and performance compared to the default ROS 2 executor.** 

## I. INTRODUCTION 

The Robot Operating System 2 (ROS 2) is a widely used middleware for creating robotics applications. It provides tools and libraries to build modular systems consisting of many interacting components. In comparison to the original Robot Operating System (ROS), it provides opportunities to configure real-time properties through its use of the Data Distribution Services (DDS) for real-time communication and its custom scheduling abstraction, called an executor, that manages the execution of time-triggered and event-triggered tasks. 

The standard scheduling mechanism in ROS 2 relies on _polling points_ and _processing windows_ . That is, at each polling point, jobs that are eligible for execution are moved to a _wait set_ , followed by a processing window within which to schedule the jobs in the wait set non-preemptively by a predefined priority order. Due to this round-robin-like approach, even tasks with a high priority may experience long blocking times. That is, a high-priority task may be blocked for the length of a _full_ processing window — including the execution time of _every_ lower-priority task. Moreover, the implementation of ROS 2 only releases one job of a task, even if the task period has been reached several times during one processing window. 

Dedicated analyses for the ROS 2 standard executor have been provided [5], [7], [31], [33], [35]. To mitigate potentially long response times of the ROS 2 default executor, alternative executor designs have been proposed and analyzed, such as fixed-priority schedulers [9] and dynamic-priority schedulers [1]. However, they can not be integrated easily into existing ROS 2 systems, as they require substantial changes in the source code of ROS 2. 

In 2023, the events executor [21] was introduced in ROS 2, replacing the wait set with an _events queue_ , and passing only one job to the processing window at a time. This paper addresses the following fundamental question: 

_Is it possible to use the events executor in ROS 2 in a manner that is compatible with the classical realtime scheduling theory of periodic task systems, in which every high-priority task can only be blocked by at most_ one _lower-priority task, and a job is released_ every time _the task period is reached?_ 

Our answer is _yes, but only under certain conditions._ 

In this paper, we uncover these conditions and show that any priority-based non-preemptive scheduling strategy, with slight modifications of the events executor, can be realized, including Fixed-Priority (FP) and Earliest-Deadline-First (EDF) scheduling. Our solution is easy to integrate into existing ROS 2 systems since it requires only minor backend modifications of the events executor, which is natively included in ROS 2. With our solution, typical results from the real-time systems literature for priority-based non-preemptive scheduling of periodic tasks can be applied. 

**Our Contributions** : The contributions of this paper are: 

- In Section II, we outline the different characteristics of typical priority-based schedulers and the default ROS 2 executor. We define the problem this paper investigates in Section III. The events executor is introduced in Section IV. 

- We present modifications to allow priority-based scheduling for the events executor in Section V. 

- We state the conditions that make our proposed executor compatible with priority-based non-preemptive scheduling theory for periodic tasks in Section VI. Furthermore, we demonstrate how the analytical results in the literature 

can be applied to bound typical metrics like the worstcase response time and the end-to-end latency for the proposed ROS 2 scheduler. 

- While the previous sections focus on timer tasks (i.e., tasks with periods), we extend our paper to subscription tasks (i.e., tasks triggered by other tasks) in Section VII. 

- In Section VIII we evaluate our findings, showing our compatibility with the classical real-time scheduling theory and the benefits of our proposed scheduler. We show that response-time bounds from the literature can be directly applied to ROS 2 systems, improving end-to-end latencies significantly in many cases. 

## II. PERIODIC TASK SYSTEMS AND EXECUTORS IN ROS 2 

In this section, we first present the basic model widely used in real-time scheduling theory for periodic task systems, followed by the default ROS 2 executor. For simplicity of presentation, we focus on ROS 2 timers in this section. 

## _A. Typical Priority-Based Scheduler_ 

We first introduce the widely adopted periodic task model in real-time systems. Given a set T of tasks, a **periodic task** _τi_ is specified by the tuple _τi_ = ( _Ci, Ti, Di, ϕi_ ) _∈_ R<sup>4</sup> , where _Ci ≥_ 0 is the worst-case execution time (WCET), _Ti >_ 0 is the period, _Di >_ 0 is the relative deadline, and _ϕi_ is the phase. The periodic task _τi_ releases its first job (task instance) at time _ϕi_ , and subsequent jobs are released every _Ti_ time units. Every job of _τi_ executes for at most _Ci_ time units and has an absolute deadline specified as its release time plus the relative deadline. When a job is released at time _t_ , it is placed into the ready queue and the job is removed from the ready queue after it finishes executing. We restrict our paper to _constrained deadline systems_ , where _Di ≤ Ti_ for all tasks _τi ∈_ T. 

In real-time operating systems (RTOSes), the release of the jobs of the periodic tasks can be implemented as a job _releaser_<sup>1</sup> based on a _timer interrupt service routine_ . Specifically, suppose that _Ti_ is an integer multiple of a predefined system tick for every task _τi ∈_ T. A timer interrupt is triggered every tick and the releaser has to decide whether a job of task _τi ∈_ T should be released or not. 

A _scheduler_ determines which job in the ready queue should be executed. _Priority-based schedulers_ , in which scheduling decisions are made by assigning priorities to jobs, have been widely studied in the literature. At any point in time when a scheduling decision has to be made, the _highest-priority job among the jobs in the ready queue_ is allocated to the processor for execution. In the literature, such priority-based schedulers (on the task level) are classified into fixed-priority and dynamic-priority schedulers. A scheduler is a _fixed-priority scheduler_ if, for any two tasks _τi_ and _τj_ , either all jobs of _τi_ have higher priority than all jobs of _τj_ or all jobs of _τj_ 

> 1We use the term _releaser_ to indicate an independent component of a system that is responsible for determining whether and if so when a job should be released. Its role is distinct from that of the _scheduler_ , which decides which of the released jobs should be running at any point in time. 

have higher priority all jobs of _τi_ . In contrast, for _dynamicpriority_ scheduling, a job of _τi_ may have a higher priority than some jobs of _τj_ but a lower priority than other jobs of _τj_ . 

Specifically, the rate monotonic (RM) scheduler (where a task with a smaller period has a higher priority) is a wellknown fixed-priority scheduling policy, whilst the earliestdeadline-first (EDF) scheduler (where a job with the earliest absolute deadline has the highest priority) is a well-known dynamic-priority scheduling policy [28]. 

Scheduling algorithms also may be preemptive or nonpreemptive. That is, while for preemptive scheduling a scheduling decision is made at every timer interrupt, for non-preemptive scheduling decisions are only made at a few specific checkpoints of job execution. 

More specifically, in preemptive scheduling, at every timer interrupt it is checked whether the currently running job is still the highest-priority job in the ready queue, and if so, it continues executing. Otherwise, the system performs a context switch, preempts the currently executing job, and executes the new highest-priority job in the ready queue instead. 

On the other hand, for non-preemptive scheduling, a scheduling decision is only made when (i) a running job finishes its execution or (ii) a job is inserted into an empty ready queue. Since the scheduler can make a scheduling decision to start the execution of the highest-priority available job only at those time points, a running job is never preempted and continues to be executed until it finishes. Worst-case analysis of non-preemptive schedulers for real-time systems has been widely studied, e.g., [11], [12], [14], [22], [29]. 

## _B. Default Executor in ROS 2_ 

Next, we describe the default executor in ROS 2, and how it relates to the periodic task model presented in Section II-A. 

The default ROS 2 executor non-preemptively schedules tasks’ eligible jobs using a wait set. Its scheduling mechanism is split up into two iterative phases, the _polling point_ and the _processing window_ . At each polling point, the executor updates the wait set by sampling at most one job of each eligible task. During each processing window, the executor iterates over the wait set and executes the jobs non-preemptively according to the fixed-priority order of their respective tasks. The executor thread executes a job by calling a function (callback). After finishing the execution of all jobs in the wait set, the wait set is empty, and the executor starts a new polling point. 

Compared to classical real-time schedulers, the polling point describes the moment when tasks’ jobs are released, and the processing window describes the interval over which the released jobs are scheduled. 

Furthermore, timers are handled differently in ROS 2 compared to the classical real-time releaser. Instead of actively being inserted into the wait set by a releaser at the time of release, timers are passively sampled by the executor at the polling point by determining if they are eligible for execution. 

The mechanism of the default executor for timers is as follows: Each timer stores its next _activation time_ at which it will be eligible for execution. At the moment at which the 

2 

executor determines if a timer is eligible, it checks whether the current time is greater than or equal to the _activation time_ of the timer. If so, a job of that timer is sampled, and the next _activation time_ point is determined by increasing the current _activation time_ by the minimal multiple of the timer period, such that it is greater than the current time. As a result, the executor may skip timer jobs if the time between two polling points is longer than the period of the timer, as the executor may increase the _activation time_ of the timer by a multiple of the period. For the rest of the paper, we refer to the _activation time_ as the _timestamp_ of the timer job. 

In general, this combination of a non-preemptive scheduler using a wait set and the passive sampling of timers can lead to interference between the release and scheduling of a job. For the default executor, the _timestamp_ is incremented at the time of scheduling the timer job, instead of the time at which the job is sampled and added to the wait set. Potentially, this leads to the timer being prevented from releasing jobs at its specified period, if the processing window is long enough to prevent the executor from updating the _timestamp_ of the timer before the next period elapses. 

While this design may have disadvantages in guaranteeing the periodic release of timers, it ensures that all jobs that are polled into the wait set are executed in the subsequent processing window. That is, a timer may not generate as many jobs as its period indicates, but whenever a job is ready it is executed in the following processing window. Although this may lead to tasks being executed less often than expected, it improves ease of development and also makes it possible to set a very short timer to ensure that some actions are performed as frequently as possible, e.g., by setting a timer to 0. 

As the default ROS 2 executor (based on the concept of polling points and processing windows in an interleaved manner) does not match the model (based on an independent _releaser_ and _scheduler_ ) of the classic real-time scheduling theory presented in Section II-A, the rich literature of real-time scheduling theory is not applicable for ROS 2 systems that use the default executor. Hence, dedicated response-time analyses have been developed for the default ROS 2 executor [5], [7], [31], and suggestions have been made on how to optimize the ROS 2 application code to mitigate long response times [31]. Casini et al. [7] also introduced the concept of processing chains, in which tasks may be triggered due to the arrival of data, and output a result, triggering other tasks. This propagation of data creates a natural structure of chained tasks, that can be used to measure end-to-end latency of the task set. Specifically, Teper et al. have analyzed [32], [35] and optimized [33] such end-to-end latencies in the ROS 2 single-threaded executor. Multi-threaded executors have been developed and analyzed [23], [27], [30], but these are still constrained by the wait set behavior of the default executor. Their implementation either shares the wait set among threads in a thread pool or runs multiple unmodified executors in different threads. The latter approach also requires the manual assignment of nodes to executors. 

Although incompatibility with classical real-time schedulers 

can be addressed by designing alternative executors for fixedpriority [9] or dynamic-priority [1] schedulers as we have noted earlier, the ability to use executors provided directly by ROS 2 for periodic task systems is still desirable. It reduces design, implementation, and maintenance costs for system developers. Section IV describes the new ROS 2 events executor, which offers just such an opportunity. 

## III. PROBLEM DEFINITION 

As we have discussed in Section II-B, the default executor of ROS 2 is not compatible with typical literature results on real-time systems. That is, the default executor shows a behavior that is typically not considered when looking at typical priority-based schedulers. More specifically, typical priority-based schedulers have the following properties: 

- Each job is inserted into the ready queue (almost) immediately by the releaser. 

- Each scheduling decision determines only one job to be executed next. 

Contrarily, the default scheduler of ROS 2 works as follows: 

- A job is inserted into a wait set only at polling points, and only if the corresponding task has been activated since the preceding polling point. 

- At the polling point, the scheduler makes the scheduling decision to run all jobs in the wait set in a deterministic order and does not make another scheduling decision until the next polling point. 

As a direct consequence, the default ROS 2 scheduler shows behavior that usually can not occur in typical priority-based schedulers. For example, a job release can be delayed for a whole processing window, including the execution of all lower-priority jobs, and job releases can even be skipped if a processing window takes longer than a task period. 

In this paper, we study the possibility of utilizing the events executor of ROS 2, introduced in Section IV, to link to the classical real-time scheduling theory of periodic task systems. We discuss the necessary modifications of the events executor in Section V and discuss the compatibility of the proposed executor in Section VI. While Sections V and VI focus on applications that are composed of _only timer tasks_ , we extend our results to ROS 2 applications with non-timer tasks (i.e., callbacks based on the publisher/subscriber model) in Section VII. 

## IV. THE EVENTS EXECUTOR 

In 2023, ROS 2 added the events executor to its distribution [21], providing an alternative to the default executor. It does not use a wait set, but instead uses a FIFO queue, called an _events queue_ , that stores the jobs of tasks that are eligible for execution. It uses two threads, the _timer management thread_ and the _default thread_ , to manage the release and scheduling of tasks jobs, respectively. Non-timer tasks are by default only handled by the _default thread_ , including releasing and scheduling them. For timer tasks, the _timer management thread_ manages a _timer release queue_ , and there are two options for how it handles the tasks in the queue: 

3 

- Option 1 — **Release-Only** (denoted as **RO** ): The _timer management thread_ only releases the timer jobs from the _timer release queue_ to the _events queue_ (where also nontimer events reside), and all jobs are scheduled by the _default thread_ in FIFO order. 

- Option 2 — **Release-and-Execute** (denoted as **RE** ): The _timer management thread_ holds both released and unreleased timer jobs in its _timer release queue_ , and orders and schedules them based on their _timestamp_ . 

Option **RO** is more in line with the classical real-time scheduling theory, as it separates the _releaser_ and _scheduler_ for timers, while Option **RE** is more in line with the default executor, as it does not separate them. However, neither option incorporates priority-based ordering. In the following, we discuss the behavior of the scheduler under both options. 

Algorithm 1 summarizes the implementation of the _timer management thread_ in ROS 2 using the _timer release queue_ . In Algorithm 1, the _timers_ variable refers to the _timer release queue_ , which stores the timers ordered by their _timestamp_ . 

We now describe the algorithm in detail. For each release, the _timer management thread_ checks the head of the queue in Lines 4-5, as the timers are ordered by their _timestamp_ . If the current time is greater than or equal to the _timestamp_ of the timer, the timer is considered eligible. When a timer is released, the _timestamp_ of the timer is updated to the next _timestamp_ in Line 6, which is the smallest multiple of the period that is greater than the current time. For the **RO** option, the timer job is released into the _events queue_ in Line 8. Likewise, for the _RE_ option, the timer job is immediately scheduled in Line 10. Afterward, in Line 12, as the _timestamp_ is updated, the queue is reordered according to the new _timestamps_ of the tasks in the queue. 

Contrary to the default executor, for the **RO** option, the release is separated from the thread that schedules the timer jobs. Furthermore, the events executor updates the _timestamp_ of the timers between each release. This guarantees that all future scheduling decisions are based on the most recent _timestamps_ of the timers. 

In both options, the _timer management thread_ is responsible for releasing the timer jobs. The events executor does not specify the priorities of the _timer management thread_ and the _default thread_ . 

As we intend to ensure that the releaser can release the jobs of a timer periodically, in our design and discussions, we assign a higher priority to the _timer management thread_ to ensure that the timer release can not be delayed by the scheduling of non-timer tasks. We note that this is not a limitation, but a treatment that we propose. 

For both **RO** and **RE** options, we will highlight the effects of this assumption on the scheduling of the timer jobs.In the following, we discuss the behavior of the scheduler under both options in detail. For simplicity of presentation, we focus on ROS 2 timers in this section. 


Fig. 1: Release-Only model of the events executor 


Fig. 2: Release-and-Execute model of the events executor 

## _A. Release-Only (_ **_RO_** _) Option_ 

We first consider the **RO** option of the events executor, where the _timer management thread_ only releases the timer jobs to the _events queue_ , while the _default thread_ is responsible for scheduling the released timer jobs in the _events queue_ . Figure 1 illustrates the mechanism of the **RO** option. The blue color represents a data structure holding unreleased timer jobs, the orange color represents released but not-yet-scheduled timer jobs, and the green color represents scheduled timer jobs. 

For this option, the _default thread_ can be in one of three states, _waiting_ , _suspended_ , or _executing_ . Initially, the thread is _waiting_ , until the _timer management thread_ releases a job into the _events queue_ . Once a job is released, the _default thread_ selects the first job from the _events queue_ and executes it, transitioning to the _executing_ state. In the _executing_ state, the _default thread_ iteratively selects the next job from the _events queue_ and executes it (non-preemptively), until no more 

**Algorithm 1** _Timer Management Thread_ in Events Executor 

|1:|**while** Running **do**|
|---|---|
|2:|_time_<br>_to_<br>_sleep ←_next timer release time|
|3:|_wait_<br>_for_(_time_<br>_to_<br>_sleep_)|
|4:|head<br>timer _←_timers.front()|
|5:|**while** head<br>timer is eligible **do**|
|6:|head<br>timer.update<br>timestamp()|
|7:|**if** Option **RO** is configured **then**|
|8:|_events_<br>_queue.enqueue_(_head_<br>_timer, data_)|
|9:|**else if** Option **RE** is configured **then**|
|10:|_execute_(_head_<br>_timer, data_)|
|11:|**end if**|
|12:|Reorder timers by release time|
|13:|head<br>timer _←_timers.front()|
|14:|**end while**|
|15:|**end while**|


4 

eligible jobs are in the _events queue_ . Once the queue is empty, the _default thread_ transitions back to the _waiting_ state. 

For the scheduling of the threads, we need to consider the priorities of the _timer management thread_ and the _default thread_ . Specifically, we assume the _timer management thread_ has a higher priority than the _default thread_ . As a result, every release of a timer job by the _timer management thread_ can preempt the _default thread_ when it is executing a job, leading to the _default thread_ transitioning to the _suspended_ state. 

We note that the above discussion simplifies the interactions between the _default thread_ and the _timer management thread_ by ignoring the mutual exclusion (mutex) lock that is used to ensure no race conditions when using the _events queue_ . Therefore, the _timer management thread_ also can be blocked by the _default thread_ if the mutex has been locked already by the _default thread_ . Such blocking is considered part of the job release overhead and is ignored for the rest of the paper. 

## _B. Release-and-Execute (_ **_RE_** _) Option_ 

Next, we consider the **RE** option of the events executor, where the _timer management thread_ is responsible for both releasing and executing the timer jobs. The mechanism of this option is illustrated in Figure 2. 

As in the **RO** option, the _timer management thread_ uses the _timer release queue_ to store the timers ordered by their _timestamp_ . The _timer release queue_ is responsible for storing both the unreleased and released timer jobs. This is possible, as the timers in the queue are ordered by their _timestamp_ , and the _timer management thread_ can directly select the first timer in the queue for execution. 

Non-timer tasks are released and scheduled by the _default thread_ in the **RE** option, as in the **RO** option. Therefore, if a system only has timer tasks, the _default thread_ is not used. 

For this option, the _timer management thread_ can be in one of two states, _waiting_ , or _executing_ . When the _timer management thread_ is _waiting_ , it waits for the release of the next timer, given by the wake-up time of the first timer in the queue. After a job is released, the _timer management thread_ transitions to the _executing_ state, where it selects the first timer from the _timer release queue_ and executes it. In this state, timers are executed until the queue does not have any more eligible timers. After there are no more eligible timers, the _timer management thread_ transitions back to the _waiting_ state. 

As in the **RO** option, the _timer management thread_ updates the _timestamp_ of the timer at the moment of releasing the timer job and reorders the _timer release queue_ finishing the execution of the timer job. Thus, each release considers the most recent _timestamps_ of the timers, but in contrast to the **RO** option, the release of timer jobs may be delayed, if the _timer management thread_ is executing a timer job. 

## V. MODIFICATIONS TO ALLOW PRIORITY-BASED SCHEDULING 

With its current implementation, the events executor executes the timers in FIFO ordering only. This section presents 


Fig. 3: Prioritized Release-and-Execute model of the events executor 

the modifications that are necessary to execute timers with RM and EDF prioritization. 

Our main proposal is to manage the release of timer jobs and the scheduling of timer jobs using separate queues. Furthermore, we propose to use a priority queue to store the released timer jobs, which allows for arbitrary fixed-priority or dynamic-priority non-preemptive scheduling policies. 

## _A. Release-Only (_ **_RO_** _) Option_ 

For the **RO** option, there are already different queues for managing the release and scheduling of timers. That is, the _timer management thread_ manages the release of timer jobs separately from the _default thread_ , and all released jobs are stored in the _events queue_ . Furthermore, the insert operation of the priority-based _events queue_ does not simply insert the job at the end of the queue but inserts it at the correct position according to the priority of the job, which allows for arbitrary fixed-priority or dynamic-priority scheduling policies. 

To ensure that timers are moved from the release queue to the _events queue_ (almost) immediately, we assign a higher priority to the _timer management thread_ , so that the job releases are not blocked by the _default thread_ . As a result, there may be suspensions of the _default thread_ , but the timer jobs can be released periodically, as detailed in Section VI. 

## _B. Release-and-Execute (_ **_RE_** _) Option_ 

For the **RE** option, we propose to add a priority-based queue to the _timer management thread_ , which stores the timer jobs that have been released for execution, i.e., a prioritized ready queue. We refer to this queue as the _timer ready queue_ . The new design for the **RE** option is illustrated in Figure 3. Unreleased timer jobs are stored in the _timer release queue_ , indicated by the blue color, and released timer jobs in the _timer ready queue_ , represented by the orange color. 

Furthermore, all eligible timer jobs are inserted into the _timer ready queue_ in a priority-based manner. Therefore, all scheduling decisions consider the priority of all released timer jobs, and the highest-priority job is selected for execution. The _timer release queue_ is reordered after each release, while the _timer ready queue_ is ordered through priority-based insertions. 

## _C. Priority-based Scheduling_ 

We now discuss how to enable priority-based scheduling for timer tasks in ROS 2 using the events executor. For both 

5 

options, the proposed design is compatible with the classical real-time scheduling theory. Specifically, the releasing and scheduling of jobs are separated, and the executor makes scheduling decisions between the execution of timer jobs. Furthermore, the executor uses a _priority-based events queue_ to prioritize the timer jobs. 

Our method only adds an overhead of _O_ (log _n_ ) for each priority insert, where _n_ is the number of tasks in the system. This overhead is necessary for priority-based management, unless special treatments/assumptions are made for prioritybased management. It is negligible compared to other ROS 2 management routines. 

The proposed design is theoretically compatible with any job-level fixed-priority non-preemptive scheduler if the priority can be decided when the job arrives, e.g., the nonpreemptive rate-monotonic (RM) and earliest-deadline-first (EDF) scheduling policies for uniprocessor systems. For RM, the executor can use the timer period as the priority, and for EDF with implicit deadlines, the executor can use the next _timestamp_ of the timer as the priority. We note that our current implementations support any task-level fixed-priority nonpreemptive scheduler as well as EDF (for implicit deadlines) which are fully compatible with the current ROS 2 codebase. 

## VI. COMPATIBILITY WITH NON-PREEMPTIVE SCHEDULERS FOR PERIODIC TASKS 

In this section, we explain how our proposed scheduler from Section V bridges the gap between the literature on prioritybased scheduling and ROS 2. We assume that the ROS 2 application has only timers and the system is exclusively used to execute the ROS 2 application on one processor. Furthermore, we assume that tasks have different priorities and ties are broken arbitrarily but deterministically. We show that our scheduler behaves analytically _like_ a non-preemptive work-conserving priority-based scheduler in Section VI-A. In Section VI-B we discuss the overhead that results from our scheduler. We derive a worst-case response time analysis in Section VI-C and an end-to-end latency bound (which is one of the predominantly studied metrics for ROS 2 systems) in Section VI-D, using existing literature results on priority-based real-time scheduling. 

## _A. Analytical Behavior of Our Scheduler_ 

Our solution uses the events executor with a modification of the _events queue_ for priority-based job ordering. In the following, we examine both options, Release-Only ( **RO** ) and Release-and-Execute ( **RE** ), individually and explain how they mimic typical priority-based schedulers. 

_a) Release-Only (_ **_RO_** _):_ With the **RO** option, the release of timer jobs into the _events queue_ is done in a separate thread. Therefore, under the assumption that the _timer management thread_ is not blocked whenever the _timestamp_ of the timer task is reached, a job of that task is inserted into the _events queue_ immediately. Therefore, with **RO** , jobs are released (i.e., inserted into the _events queue_ ) periodically. Moreover, scheduling decisions are effectively made after a job finishes, 

by pulling the first job (i.e., the highest priority job) from the _events queue_ . Therefore, our scheduler with **RO** behaves like a typical non-preemptive scheduler. 

_b) Release-and-Execute (_ **_RE_** _):_ With the **RE** option, the _timer management thread_ manages the release of timer jobs using the _timer release queue_ , and the scheduling of timer jobs with the _timer ready queue_ . Therefore, the execution of a task can block the release of a timer job, and the scheduler does not achieve periodic job releases by design. However, this does not mean that analytical results are not applicable by default. If the following criteria are met, then the scheduler mimics the typical priority-based scheduler, in the sense that it generates the same schedule (although the job releases are not periodic): 

- C1 Whenever the _timestamp_ of a timer is reached, this eventually leads to a job release, and the _timestamp_ is increased by exactly one period. (That is, no job release is skipped.) 

- C2 After a _timestamp_ is reached, then a job must be released before the next scheduling decision is made (where it will be considered eligible). (That is, jobs are released fast enough.) 

If these conditions are satisfied, the schedule coincides with the schedule obtained by a typical priority-based scheduler. 

Under our scheduler with the **RE** option, whenever a job finishes, the tasks in the _timer release queue_ are reordered, and released jobs are added to the _timer ready queue_ before a scheduling decision is made. That is, C2 is naturally fulfilled. We achieve criteria C1 if a job execution does not span over two possible timestamps. That is, if we assume that 


for all _τj̸_ = _τi_ , then both criteria C1 and C2 are fulfilled, and our scheduler indeed generates schedules that coincide with the schedules obtained by typical priority-based schedulers. Since the scheduling decision is made only after completing job execution and not during job execution, this behaves like a non-preemptive scheduling mechanism. 

## _B. Bounding the Releaser Overhead_ 

In this subsection, we provide bounds on the amount of overhead that the releaser can introduce into the system. This overhead has to be accounted for when applying the results in the literature for non-preemptive schedulers. 

We assume that releasing a job takes up to _δ >_ 0 time units. Then, if a job is released into the _events queue_ or _timer ready queue_ , this prolongs the execution time of the job that is currently running or that is about to start right after the release. Hence, by counting the maximal number of released jobs right before and during the execution of a job, we obtain a bound on the overhead. We denote by ∆ _i_ the overhead that jobs of _τi_ can experience. 

With the **RE** option, releasing jobs cannot happen during the execution of a job, but may only prolong the execution right before. Only one job of each task can be released into the _timer ready queue_ , leading to an overhead of 


6 

time units, where _n_ is the number of tasks in the system. Please note that this covers the time for the release of the job that is about to start. 

With the **RO** option, job releases can be done whenever a timestamp is reached. That is, releasing can also take place during job execution. The number of timestamps that can occur for a task _τj_ during an interval of length _t_ is � _Ttj_ �. Let _t_ 0 _∈_ R _>_ 0 be the lowest positive real number such that _t_ 0 _≥ Ci_ + � _nj_ =1 � _Tt_ <u>0</u> _j_ � _· δ_ . Then _t_ 0 is the amount of time that a job of _τi_ can execute, including the overhead from releasing other tasks. Hence, the release overhead for task _τi_ is bounded by 


This bound on the overhead ∆ _i_ can be tightened further if the following two conditions hold: 

- The task set has constrained deadlines. 

- The task set is already shown to be schedulable (e.g., by using the bound on the overhead from Equation (3) together with a schedulability test from Section VI-C). 

Under these conditions, every other task can only release one job during the execution of a job of _τi_ . Otherwise, assuming a task _τj_ releases two jobs at timestamps _t_ 1 and _t_ 2 = _t_ 1 + _TJ_ during the execution of a job of _τi_ , then the job of _τj_ can not be executed until time _t_ 2. Hence, it would miss its constrained deadline, which violates the schedulability of the task set. Therefore, under the two conditions, the overhead for the releaser is upper bounded by 


where _n_ is the number of tasks in the system. 

We note that it is unsafe to apply the tightened bound directly for calculating a response time bound and checking the schedulability based on that. However, when the response time is already shown to be _≤ Di_ , we can use this formula to tighten the response time bound further. This can be beneficial when applying analyses that utilize the worst-case response time (cf. Section VI-D). 

## _C. Worst-Case Response Time Analysis_ 

In the following, we analyze the WCRT of timer tasks under our scheduler. We assume that the overhead is accounted for by prolonging the WCET, i.e., by redefining _Ci_ := _Ci_ + ∆ _i_ . Following our discussion in Section VI-A, the timer tasks _τi ∈_ T behave like non-preemptive periodic tasks with period _Ti_ . Therefore, literature results for non-preemptive periodic tasks (cf. [11], [14], [22], [29], [37]) are applicable. 

Although this pertains to any scheduling algorithm that can be modeled by reordering the _events queue_ or _timer ready queue_ , we focus specifically on Fixed-Priority (FP) and Earliest-Deadline-First (EDF) scheduling. Although we present only a few results that we utilized in the evaluation, the results of this work are not limited to only these. 

The following theorem is a reformulation of the schedulability test for non-preemptive FP scheduling presented for example in the work by von der Br¨uggen et al. [38]. _Theorem 1 (Non-preemptive FP, Reformulated from Eq. (6) in [38]):_ Assume that the tasks T = _{τ_ 1 _, . . . , τn}_ are ordered by their priority, i.e., _τ_ 1 has the highest priority and _τn_ has the lowest priority. If there exists a _t ≥_ 0 _∈_ R such that _t ≤ Dk_ and 


then the WCRT _Rk_ of _τk ∈_ T under non-preemptive FP scheduling is upper bounded by _t_ . 

That is, an upper bound on the WCRT can be computed using fixed-point iteration, starting with _t_ = 0, to find the smallest _t_ that fulfills Equation (5). Moreover, if we can find a response time upper bound _Rk ≤ Dk_ for all _τk ∈_ T, then we know that the task set is schedulable. 

Bounds under non-preemptive EDF have for example been explored by George et al. [14]. In the following, we restate their theorem for completeness. Please note that while their work considers the discrete time domain, we formulate it for the continuous time domain. 

_Theorem 2 (Non-preemptive EDF, Reformulated from [14]):_ The task set is schedulable under non-preemptive EDF if for all _t >_ 0 the equation 


holds, where _dbf i_ is the _demand bound function_ of task _τi_ , defined by _dbf i_ ( _t_ ) := max �0 _,_ � _<u>t−TDi i</u>_ + 1�� _· Ci_ . We note that when a task set is shown to be schedulable under non-preemptive EDF, then we can also claim an upper bound on the WCRT, namely _Ri ≤ Di_ . 

## _D. Application of End-to-End Latency Analysis_ 

One of the predominantly studied metrics for ROS 2 applications is end-to-end latency. That is, given a sequence of tasks _E_ = ( _τi_ 1 _→ . . . τiN_ ), a so-called _cause-effect chain_ , then we are interested in the amount of time that data needs to traverse the cause-effect chain. Specifically, the Maximum Reaction Time (MRT), i.e., the amount of time until an external cause is fully processed, and the Maximum Data Age (MDA), i.e., the age of data utilized in an actuation, have been analyzed extensively in the literature. While there are only a few analytical results for the standard ROS 2 application [32], [34] there is a large body of literature results for typical periodic tasks [2]–[4], [10], [13], [15]–[20], [24]. Our scheduler enables such results and insights from end-to-end analysis for periodic task systems. Recently, it has been shown that MRT and MDA are equivalent. Hence, we use _Lat_ to denote the end-to-end latency in general. 

7 

One typical approach to derive end-to-end latency in periodic priority-based scheduling (cf. [10]<sup>2</sup> ) is to sum up the task periods and bounds on the WCRT. The end-to-end latency is upper bounded by: 


More specifically, given a cause-effect chain _E_ on the task set T scheduled by our scheduler, then the following steps result in a bound on the end-to-end latency: 

- 1) Calculating the overhead ∆ _i_ from Section VI-B and incorporating it in the WCET by _Ci_ := _Ci_ + ∆ _i_ . 

- 2) Providing an upper bound on the WCRT _Ri_ using results from Section VI-C. 

- 3) Calculating a bound for the end-to-end latency using Equation (7). 

In Section VIII, we compare this bound on the end-to-end latency with the latency that can be analytically guaranteed for the typical ROS 2 scheduler [34]. 

## VII. SUBSCRIPTION TASKS 

The previous sections focused on the behavior of timer tasks. However, besides timers, ROS 2 allows tasks to be triggered through the built-in Data Distribution Service (DDS). That is, when a job finishes its execution it can publish a message to a certain predefined topic, and all subscription tasks subscribing to this topic are activated, such that they can be released. Since subscription tasks are widely used in practice, this section explains how our findings can be extended to systems involving subscription tasks. 

In the default ROS 2 executor, all activated subscriptions are released at the polling point. In the events executor, subscriptions are only processed by the _default thread_ , and before every scheduling decision of the _default thread_ , it releases all activated subscriptions by moving them to the _events queue_ . To that end, we first consider the **RE** option, and afterward, we consider the **RO** option. This section does not aim to provide specific analytical results, but rather links different scenarios to the corresponding real-time systems literature. 

**RE Option** : For this configuration, timers are handled completely separately by the _timer management thread_ , while subscriptions are fully handled by the _default thread_ . 

As subscriptions are not activated or released periodically, the analysis of this work is not directly applicable. If a minimum inter-arrival time _>_ 0, i.e., a minimum time between two publications of a topic that the subscription subscribes to can be determined, then the literature on sporadic nonpreemptive tasks may be applicable. However, to apply the literature it has to be ensured that every activation also leads to a job release, i.e., no jobs are lost. This is beyond the scope of this paper. 

> 2Although Davare et al. [10] formulate this bound using preemptive FP scheduling, this result is universally applicable when utilizing a correct bound on the WCRT. 

**RO Option** : In this configuration, both timers and subscriptions are released to the prioritized _events queue_ of the _default thread_ . For this option, we use our proposal from Section IV-A to give the _timer management thread_ a higher priority than the _default thread_ , to ensure that jobs are released before scheduling decisions are made. Since the execution of all jobs is handled by the same thread, the literature on non-preemptive scheduling is applicable. However, to apply the results for the timer tasks, the subscription tasks have to be taken into account as well. To that end, a minimum inter-arrival time _>_ 0 has to be determined for each subscription task. To ensure that no job is lost, the minimum inter-arrival times and task periods have to be larger than the WCET of any task. 

One special case that we would like to emphasize is when tasks are arranged in _sequences_ . That is, each task invokes the activation of at most one subscription task, and each subscription task can be activated by exactly one task. An example of such sequences can look as follows: 

- sequence1 = timer1 _→_ subscription1 _→_ subscription2 

_•_ sequence2 = timer2 _→_ subscription3 _→_ subscription4 We consider the special case where the first task of a sequence is a timer task, as this guarantees a minimum inter-arrival time for the subsequent subscription tasks. Furthermore, all subsequent tasks are subscription tasks since they subscribe to a topic by definition. Each job of the timer task of a sequence releases one job of the subsequent subscription tasks. When considering the whole sequence as a task, with timer tasks and subscription tasks only being subtasks of the sequence, then this relates to the literature on limited preemptive scheduling [6]. 

Each subtask is scheduled non-preemptively, and between subtasks, the task can be preempted. The benefit of considering sequences is that there is no need to determine the minimum inter-arrival time of subscription tasks. However, as soon as the data dependencies of the DDS become more complex, this approach is not applicable anymore. 

We further note that, in case the DDS introduces a certain delay to release the subsequent subscription [26], another lower priority job may be started in between the execution of two non-preemptive subtasks. In that case, the additional delay can be modeled as self-suspension [8]. More specifically, the set of sequences behaves like a set of segmented selfsuspending tasks scheduled non-preemptively on a single core. This delay can be assumed to be zero if zero-copy middleware is used, or if the DDS communication is synchronous. In these cases, downstream tasks are activated by the time the upstream task finishes and are immediately eligible for execution. 

## VIII. EVALUATION 

In this section, we evaluate our proposed modifications of the ROS 2 events executor and the corresponding analyses. The evaluation consists of three contributions: 

- We confirm **compatibility with scheduling theory** on non-preemptive schedulers for periodic tasks in Section VIII-A. More specifically, we demonstrate for a 

8 

timers-only task set that the analytical results of Section VI are applicable. That is, the modified ROS 2 events executor does not drop jobs, and it respects the worstcase response time bounds for non-preemptive scheduling presented in Section VI-C. 

- In Section VIII-B, we show that the **bounds on end-toend latency** for cause-effect chains, enabled by the theory of non-preemptive scheduling bounds, are tighter than the state-of-the-art analytical end-to-end latency bounds for the default executor. To that end, we apply the analyses to synthetic task sets using the WATERS [25] benchmark. 

- We compare the performance of our modified executor using the RM scheduling policy with the default executor in the Autoware reference system in Section VIII-C. The Autoware reference system includes both timers and subscriptions and demonstrates that we can achieve lower end-to-end latency than the other executor options provided natively by ROS 2. 

Our experiments feature the following executor configurations: 

- default executor ( **Default** ), 

- static default single-threaded Executor ( **Static** ), 

- unmodified default events executor ( **Events** ), 

- our rate-monotonic events executor ( **RM (RO)** and **RM (RE)** ), and 

- our earliest-deadline-first events executor ( **EDF (RO)** and **EDF (RE)** ). 

We include the static default executor for completeness. It behaves like the default executor, but with less overhead, as it does not have to handle dynamic system configurations. 

## _A. Compatibility with Scheduling Theory_ 

In this subsection, we demonstrate that existing results on non-preemptive scheduling apply to our scheduler, and analytical results correctly predict the behavior of the system. 

To that end, we examine a timers-only task set that consists of three types of components, and seven nodes in total. The system has four cameras, two LiDARs, and an IMU. Each node has one timer task, and each component is independent of the others, meaning that they do not pass data between each other and have no precedence constraints. By varying the maximum execution time of the tasks, we configure the system to have a utilization of 60%, 80%, or 90%. Our three configurations are as follows: 

## **60% utilization** 

- 4 Camera Nodes: 84ms period, 10ms execution each 

- 2 LiDAR Nodes: 200ms period, 10ms execution each 

- 1 IMU Node, 30ms period, 1ms execution 

## **80% utilization** 

- 4 Camera Nodes: 84ms period, 14ms execution each 

- 2 LiDAR Nodes: 200ms period, 10ms execution each 

- 1 IMU Node, 30ms period, 1ms execution 

## **90% utilization** 

- 4 Camera Nodes: 84ms period, 16ms execution each 

- 2 LiDAR Nodes: 200ms period, 10ms execution each 


Fig. 4: Dropped jobs on timers-only task sets: A checkmark indicates no dropped jobs across all utilization levels. 

- 1 IMU Node, 30ms period, 1ms execution 

Task periods stay consistent across all utilization levels, so all task sets have the same hyperperiod of 4.2 seconds. Each task set is run for 5 minutes, elapsing over 70 hyperperiods. We repeat this for each executor design. 

Each of these tasksets are pinned to a single core of a Raspberry Pi Model 4B with 4GB of RAM running Ubuntu 22.04 and ROS 2 Humble. VIII-A uses one core, while VIII-C uses two cores with no thread pinning. VIII-B has one executor thread running on one processing core. 

**Number of Dropped Jobs:** The rate of dropped jobs for different configurations is shown in Figure 4. We can see that the default, static, and unmodified events executor repeatedly drop jobs. In some cases, a drop rate of 10% is observed. Following our analytical results of Section VI-A, our proposed events executor do not have any job drops for any configuration of the RM and EDF events executors. 

**Response Time Bounds:** In the following, we analytically derive upper bounds on the worst-case response time, following Section VI, and then confirm that the response time bounds are not violated by our RM events executor. 

For the analysis, we measured that a job release takes up to _δ_ = 0 _._ 12 _ms_ . The total overhead ∆ _i_ for a timer task _τi_ can be determined by Equation (3). Doing the calculations for the task sets of this section, every timer task has an overhead of ∆ _i_ = 0 _._ 84 _ms_ . Afterward, we apply Theorem 1 with the updated worst-case response time bounds _Ci_ := _Ci_ + ∆ _i_ . 

We consider implicit-deadline task systems, i.e., the relative deadline of a timer task is equal to its timer period. The analyzed worst-case response times for our RM events executor are reported in Table I, indicating no deadline misses. Thus, we should not observe any job drops, as verified in Figure 4, and all tasks are guaranteed to meet their deadlines. 

We measured the response times during the experiment. The aggregated results of the Camera nodes are shown in Fig 5, the LiDAR nodes in Fig 6, and the IMU node in Fig 7. 

9 

TABLE I: Analytical worst-case response times (ms) of our RM events executor. 


Fig. 7: Response Time of IMU Tasks (ms), D=30ms 

executor. The task sets are synthetically generated using the WATERS benchmark [25] for automotive systems. 

Fig. 5: Response Time of Camera Tasks (ms), D=84ms 

As shown in the figures, the response times are consistent with the analytical results, and no deadline overruns are observed. Furthermore, in Figure 7, we see that the IMU tasks have deadline overruns on the Default, Static, and Events executors. We note that Figures 5, 6 and 7 only account for the response times of jobs that are not dropped. Hence, for a significant amount of timestamps, the Default, Static, and Events executors do not provide a response within the deadline, as observed in Figure 4. 

In conclusion, our analysis not only correctly indicates the absence of dropped jobs in our RM events executor, but also a correct upper bound on the response time of each task. 

## _B. Tighter End-to-End Bounds for ROS 2_ 

In this section, we evaluate the differences between the analytically derived upper bounds of the end-to-end latencies between the default ROS 2 executor and our RM events 


Fig. 6: Response Time of LiDAR Tasks (ms), D=200ms 

We evaluate task sets for utilization levels of 60%, 80%, and 90%. For each configuration, we generate one thousand task sets, each including 10 to 200 tasks. To calculate the endto-end latencies, we generate 5 to 60 chains of tasks, each of which consists of 2 to 15 tasks. 

For each task set, we calculate the end-to-end latency for the default ROS 2 executor and our RM (including both RO- and RE-options, as the analysis) events executor, as presented in Section VI-D. Specifically, we use Equation (7) in Section VI to calculate the end-to-end latency of each chain. 

The end-to-end latency of the default ROS 2 executor has been analyzed by Teper et al. [32]. We use Equation (15) of Lemma VI.1 and Equation (17) of Lemma VI.2 of their paper [32] to get an upper bound on the latency of each timer. For each chain, we sum up the latency upper bounds of all chain tasks to get the end-to-end latency of the chain. 

For each chain, we calculate the normalized reduction of the end-to-end latency by using<sup>_Ede_</sup> _E_<sup>_<u>fault</u>_</sup> _default_<sup>_−ERM_</sup> , where _Edefault_ ( _ERM_ , respectively) is the end-to-end latency of the chain under the default executor (under our RM events executor, respectively). The results of the evaluation are shown in Figure 8, where the _x_ -axis is the normalized reduction and the _y_ -axis is the number of chains within the binned normalized reduction. 

We can see that the end-to-end latencies of the chains are usually significantly lower when using our RM events executor. As the utilization level increases, the number of chains with a higher end-to-end latency increases as well. This is because the default ROS 2 executor is comparatively fair to all callbacks regarding their priorities. When using static-priority scheduling, some callbacks may be assigned lower priorities, leading to an increase of response time (see Figure 6), resulting in a negative reduction of end-to-end latencies for chains that include such tasks. However, the majority of chains have lower end-to-end latency when using the RM events executor, compared to the default ROS 2 executor. In some cases, we observe a normalized reduction of 

10 


Fig. 8: Reduction of the end-to-end latency between the default ROS 2 executor and our RM events executor. 

the end-to-end latency bound of almost 90%. Our experiment shows that our design can be applied to different kinds of task sets and potentially leads to latency improvements. 

## _C. Performance of Autoware Reference System_ 

In this section, we conduct an end-to-end latency evaluation for the Autoware reference system, detailed in [36], which includes interconnected timers and subscriptions.<sup>3</sup> The Autoware reference benchmark runs a simulated version of the Autoware application on a Raspberry Pi Model 4B running Ubuntu 22.04 and ROS 2 Humble. We run the ROS 2 Autoware benchmark on two dedicated cores, whilst the other two cores are handling the remaining services on the operating system. Specifically, we measure the end-to-end latency of the **hot path** defined in the benchmark from the front and rear LiDAR sensors to the object collision estimator (c.f. the Autoware reference system), as this latency is a key metric for the responsiveness to crash avoidance. The data at the start of the hot path is generated at a frequency of 10Hz. 

For our RM events executor, the subscription tasks inherit the highest priority from their corresponding upstream publishers. Non-preemptive EDF in this scenario is not well specified, as subscription tasks do not have any assigned deadlines, and hence is not evaluated. For the default events executor and the RM events executor, we use **RO** , so that all jobs are scheduled by and executed on the _default thread_ . 

Figure 9 shows the violin plot for the latency of the hot path in the Autoware reference system from a test run of 600 

> 3https://github.com/ros-realtime/reference-system/blob/main/autoware reference <u>system/README.md</u> 


Fig. 9: End-to-end latency of the hot path in the Autoware reference system under different executors. 

seconds. Of the executors measured, our RM events executor has a better worst-case latency, significantly outperforming the other executors. Compared to our work, the default ROS 2 executor has a 2.6x slowdown along the hot path. Our evaluation shows that our executor design using existing scheduling policies from classical real-time systems can be applied to practical ROS 2 applications, and can provide major benefits in terms of end-to-end latency. 

## IX. CONCLUSION 

This paper provides deep investigations of the recently introduced events executor (in 2023) in ROS 2 to provide compatibility with the classical real-time scheduling theory of periodic task systems. Specifically, our solution is easy to integrate into existing ROS 2 systems, since it requires only minor backend modifications of the events executor, already natively included in ROS 2. Our study enables the rich literature of the real-time scheduling theory for nonpreemptive schedules to apply to ROS 2. Furthermore, we intensively validate the feasibility of our modifications for nonpreemptive RM and non-preemptive EDF in the ROS 2 events executor for several scenarios. The evaluation results show that our ROS 2 events executor with minor modifications can have significant improvement in terms of dropped jobs, worstcase response time, end-to-end latency, and performance, in comparison to the default ROS 2 executor. 

We note that the emphasis of our paper is the compatibility of the ROS 2 events executor with the classical scheduling theory of periodic tasks. As a result, we focus on the transformation of a timer into a periodic task properly and only sketch how the event-triggered subscription tasks can be integrated. The interaction of the built-in DDS and the events executor when both timers and subscriptions exist requires further investigation. Furthermore, although we have successfully implemented non-preemptive EDF into the events executor, extending non-preemptive EDF of timers to deal with subscription tasks is not well specified, as subscription tasks do not have any assigned deadlines. Further investigations on 

11 

the combinations of non-preemptive EDF for timers and other scheduling strategies for subscription tasks are needed. 

## REFERENCES 

- [1] Abdullah Al Arafat, Sudharsan Vaidhun, Kurt M. Wilson, Jinghao Sun, and Zhishan Guo. Response time analysis for dynamic priority scheduling in ROS2. In _Proceedings of the 59th ACM/IEEE Design Automation Conference_ , page 301–306, 2022. 

- [2] Matthias Becker, Dakshina Dasari, Saad Mubeen, Moris Behnam, and Thomas Nolte. Synthesizing job-level dependencies for automotive multi-rate effect chains. In _International Conference on Embedded and Real-Time Computing Systems and Applications (RTCSA)_ , pages 159– 169, 2016. 

- [3] Matthias Becker, Dakshina Dasari, Saad Mubeen, Moris Behnam, and Thomas Nolte. End-to-end timing analysis of cause-effect chains in automotive embedded systems. _Journal of Systems Architecture - Embedded Systems Design_ , 80:104–113, 2017. 

- [4] Ran Bi, Xinbin Liu, Jiankang Ren, Pengfei Wang, Huawei Lv, and Guozhen Tan. Efficient maximum data age analysis for cause-effect chains in automotive systems. In _DAC_ , pages 1243–1248. ACM, 2022. 

- [5] Tobias Blass, Daniel Casini, Sergey Bozhko, and Bj¨orn B. Brandenburg. A ROS 2 Response-Time Analysis Exploiting Starvation Freedom and Execution-Time Variance. In _Proceedings of the 42nd Real-Time Systems Symposium (RTSS)_ , 2021. 

- [6] Giorgio C. Buttazzo, Marko Bertogna, and Gang Yao. Limited preemptive scheduling for real-time systems. A survey. _IEEE Trans. Ind. Informatics_ , 9(1):3–15, 2013. 

- [7] Daniel Casini, Tobias Blaß, Ingo L¨utkebohle, and Bj¨orn Brandenburg. Response-time analysis of ros 2 processing chains under reservationbased scheduling. In _31st Euromicro Conference on Real-Time Systems_ , pages 1–23. Schloss Dagstuhl, 2019. 

- [8] Jian-Jia Chen, Geoffrey Nelissen, Wen-Hung Huang, Maolin Yang, Bj¨orn B. Brandenburg, Konstantinos Bletsas, Cong Liu, Pascal Richard, Fr´ed´eric Ridouard, Neil C. Audsley, Raj Rajkumar, Dionisio de Niz, and Georg von der Br¨uggen. Many suspensions, many problems: a review of self-suspending tasks in real-time systems. _Real Time Syst._ , 55(1):144– 207, 2019. 

- [9] Hyunjong Choi, Yecheng Xiang, and Hyoseung Kim. Picas: New design of priority-driven chain-aware scheduling for ros2. In _2021 IEEE 27th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ , pages 251–263. IEEE, 2021. 

- [10] Abhijit Davare, Qi Zhu, Marco Di Natale, Claudio Pinello, Sri Kanajan, and Alberto L. Sangiovanni-Vincentelli. Period optimization for hard real-time distributed automotive systems. In _Design Automation Conference, DAC_ , pages 278–283, 2007. 

- [11] Robert I. Davis, Alan Burns, Reinder J. Bril, and Johan J. Lukkien. Controller area network (CAN) schedulability analysis: Refuted, revisited and revised. _Real Time Syst._ , 35(3):239–272, 2007. 

- [12] Robert I. Davis, Abhilash Thekkilakattil, Oliver Gettings, Radu Dobrin, Sasikumar Punnekkat, and Jian-Jia Chen. Exact speedup factors and suboptimality for non-preemptive scheduling. _Real Time Syst._ , 54(1):208– 246, 2018. 

- [13] Marco D¨urr, Georg von der Br¨uggen, Kuan-Hsun Chen, and Jian-Jia Chen. End-to-end timing analysis of sporadic cause-effect chains in distributed systems. _ACM Trans. Embedded Comput. Syst. (Special Issue for CASES)_ , 18(5s):58:1–58:24, 2019. 

- [14] Laurent George, Nicolas Rivierre, and Marco Spuri. Preemptive and non-preemptive real-time uni-processor scheduling. _Research Report RR-2966, Project REFLECS_ , 1996. 

- [15] Pourya Gohari, Mitra Nasri, and Jeroen Voeten. Data-age analysis for multi-rate task chains under timing uncertainty. In _RTNS_ , pages 24–35. ACM, 2022. 

- [16] Mario G¨unzel, Kuan-Hsun Chen, Niklas Ueter, Georg von der Br¨uggen, Marco D¨urr, and Jian-Jia Chen. Timing analysis of asynchronized distributed cause-effect chains. In _RTAS_ , pages 40–52. IEEE, 2021. 

- [17] Mario G¨unzel, Kuan-Hsun Chen, Niklas Ueter, Georg von der Br¨uggen, Marco D¨urr, and Jian-Jia Chen. Compositional timing analysis of asynchronized distributed cause-effect chains. _ACM Trans. Embed. Comput. Syst._ , 22(4):63:1–63:34, 2023. 

      - of _LIPIcs_ , pages 10:1–10:22. Schloss Dagstuhl - Leibniz-Zentrum f¨ur Informatik, 2023. 

   - [19] Mario G¨unzel, Niklas Ueter, Kuan-Hsun Chen, and Jian-Jia Chen. Timing analysis of cause-effect chains with heterogeneous communication mechanisms. In _RTNS_ , pages 224–234. ACM, 2023. 

   - [20] Arne Hamann, Dakshina Dasari, Simon Kramer, Michael Pressler, and Falk Wurst. Communication centric design in complex automotive embedded systems. In _Euromicro Conference on Real-Time Systems, ECRTS_ , pages 10:1–10:20, 2017. 

   - [21] iRobot. Events executor. https://github.com/irobot-ros/events-executor, 2022. 

   - [22] Kevin Jeffay, Donald F. Stanat, and Charles U. Martel. On nonpreemptive scheduling of period and sporadic tasks. In _RTSS_ , pages 129–139. IEEE Computer Society, 1991. 

   - [23] Xu Jiang, Dong Ji, Nan Guan, Ruoxiang Li, Yue Tang, and Yi Wang. Real-Time Scheduling and Analysis of Processing Chains on Multithreaded Executor in ROS 2. In _2022 IEEE Real-Time Systems Symposium (RTSS)_ , pages 27–39, 2022. 

   - [24] Tomasz Kloda, Antoine Bertout, and Yves Sorel. Latency analysis for data chains of real-time periodic tasks. In _IEEE International Conference on Emerging Technologies and Factory Automation, ETFA_ , pages 360– 367, 2018. 

   - [25] Simon Kramer, Dirk Ziegenbein, and Arne Hamann. Real world automotive benchmarks for free. In _International Workshop on Analysis Tools and Methodologies for Embedded and Real-time Systems (WATERS)_ , 2015. 

   - [26] Tobias Kronauer, Joshwa Pohlmann, Maximilian Matth´e, Till Smejkal, and Gerhard Fettweis. Latency analysis of ros2 multi-node systems. In _2021 IEEE international conference on multisensor fusion and integration for intelligent systems (MFI)_ , pages 1–7. IEEE, 2021. 

   - [27] Ralph Lange. Mixed real-time criticality with ros2 - the callback-grouplevel executor. ROSCon Lightning Talk, 2018. 

   - [28] C. L. Liu and James W. Layland. Scheduling algorithms for multiprogramming in a hard-real-time environment. _Journal of the ACM_ , 20(1):46–61, 1973. 

   - [29] Mitra Nasri and Bj¨orn B. Brandenburg. An exact and sustainable analysis of non-preemptive scheduling. In _RTSS_ , pages 12–23. IEEE Computer Society, 2017. 

   - [30] Hoora Sobhani, Hyunjong Choi, and Hyoseung Kim. Timing Analysis and Priority-driven Enhancements of ROS 2 Multi-threaded Executors. In _2023 IEEE 29th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ , pages 106–118, 2023. 

   - [31] Yue Tang, Zhiwei Feng, Nan Guan, Xu Jiang, Mingsong Lv, Qingxu Deng, and Wang Yi. Response time analysis and priority assignment of processing chains on ros2 executors. In _2020 IEEE Real-Time Systems Symposium (RTSS)_ , pages 231–243. IEEE, 2020. 

   - [32] Harun Teper, Tobias Betz, Mario G¨unzel, Dominic Ebner, Georg von der Br¨uggen, Johannes Betz, and Jian-Jia Chen. End-to-end timing analysis and optimization of multi-executor ROS 2 systems. In _RTAS_ , 2024. 

   - [33] Harun Teper, Tobias Betz, Georg von der Br¨uggen, Kuan-Hsun Chen, Johannes Betz, and Jian-Jia Chen. Timing-aware ros 2 architecture and system optimization. In _2023 IEEE 29th International Conference on Embedded and Real-Time Computing Systems and Applications (RTCSA)_ , pages 206–215, 2023. 

   - [34] Harun Teper, Mario G¨unzel, Niklas Ueter, Georg von der Br¨uggen, and Jian-Jia Chen. End-to-end timing analysis in ROS2. In _RTSS_ , pages 53–65. IEEE, 2022. 

   - [35] Harun Teper, Mario G¨unzel, Niklas Ueter, Georg von der Br¨uggen, and Jian-Jia Chen. End-To-End Timing Analysis in ROS2. In _2022 IEEE Real-Time Systems Symposium (RTSS)_ , pages 53–65, 2022. 

   - [36] ROS2 Real time Working Group. Autoware reference system. https: //github.com/ros-realtime/reference-system, 2022. 

   - [37] Ken Tindell, Alan Burns, and Andy J. Wellings. An extendible approach for analyzing fixed priority hard real-time tasks. _Real Time Syst._ , 6(2):133–151, 1994. 

   - [38] Georg von der Br¨uggen, Jian-Jia Chen, and Wen-Hung Huang. Schedulability and optimization analysis for non-preemptive static priority scheduling based on task utilization and blocking factors. In _27th Euromicro Conference on Real-Time Systems, ECRTS 2015, Lund, Sweden, July 8-10, 2015_ , pages 90–101, 2015. 

- [18] Mario G¨unzel, Harun Teper, Kuan-Hsun Chen, Georg von der Br¨uggen, and Jian-Jia Chen. On the equivalence of maximum reaction time and maximum data age for cause-effect chains. In _ECRTS_ , volume 262 

12 

