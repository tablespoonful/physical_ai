---
title: "Work in Progress: Middleware-Transparent Callback Enforcement in Commoditized Component-Oriented Real-time Systems"
date: "2025-05-10"
authors: "Takahiro Ishikawa-Aso; Atsushi Yano; Takuya Azumi; Shinpei Kato"
url: https://arxiv.org/abs/2505.06546
pdf: https://arxiv.org/pdf/2505.06546
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2505.06546)** / [論文ページ](https://arxiv.org/abs/2505.06546)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Work in Progress: Middleware-Transparent Callback Enforcement in Commoditized Component-Oriented Real-time Systems 

Takahiro Ishikawa-Aso<sup>_†‡_</sup> , Atsushi Yano<sup>_∗‡_</sup> , Takuya Azumi<sup>_∗_</sup> , Shinpei Kato<sup>_†_</sup> 

> _†_ The University of Tokyo, Japan _∗_ Saitama University, Japan 

> _‡_ TIER IV Incorporated, Japan 

**_Abstract_ —Real-time scheduling in commoditized componentoriented real-time systems, such as ROS 2 systems on Linux, has been studied under nested scheduling: OS thread scheduling and middleware layer scheduling (e.g., ROS 2 Executor). However, by establishing a persistent one-to-one correspondence between callbacks and OS threads, we can ignore the middleware layer and directly apply OS scheduling parameters (e.g., scheduling policy, priority, and affinity) to individual callbacks. We propose a middleware model that enables this idea and implements** **_CallbackIsolatedExecutor_ as a novel ROS 2 Executor. We demonstrate that the costs (user-kernel switches, context switches, and memory usage) of** **_CallbackIsolatedExecutor_ remain lower than those of the** **_MultiThreadedExecutor_ , regardless of the number of callbacks. Additionally, the cost of** **_CallbackIsolatedExecutor_ relative to** **_SingleThreadedExecutor_ stays within a fixed ratio (1.4x for inter-process and 5x for intra-process communication). Future ROS 2 real-time scheduling research can avoid nested scheduling, ignoring the existence of the middleware layer.** 

**_Index Terms_ —Middleware, Publish-subscribe, Robot programming, Real-time systems, Scheduling algorithms, Multithreading** 

## I. INTRODUCTION 

Many modern autonomous cyber-physical systems (CPS), such as autonomous driving and robotics systems, are modeled as component-oriented real-time systems (Fig. 1). A typical system comprises independent nodes that mutually publish and subscribe to messages, collectively creating integrated dataflows throughout the system. Nodes operate independently by either publishing to or subscribing to topics defined by specific data types and identifiers. Due to the extensive ecosystem, they are typically deployed on the most commoditized platform: Robot Operating System 2 (ROS 2) [1] on Linux. 

Due to the real-time interaction with the physical world, autonomous CPS requires temporal correctness as well as functional correctness. The temporal constraints on the dataflows are defined in terms of _freshness_ , _consistency_ , and _stability_ [2]. Research on real-time scheduling in ROS 2 has primarily targeted the optimization of end-to-end _response time_ , a metric similar to freshness. In this context, cause-effect chains with ROS 2 semantics incorporated have been commonly employed as a model [3]–[5]. There are also studies where systems are modeled as Directed Acyclic Graphs (DAGs) [6], [7]. 

In both models, the real-time community has assumed nested scheduling (Fig. 2 (a)) where both the callback scheduler and the thread scheduler are considered. This approach has led to unnecessarily complex response time analysis and 


Fig. 1: Component-oriented real-time system (e.g., ROS 2). 

scheduling algorithms [3], [5], [8]–[18]. The nested scheduling is an artificial complexity imposed by the ROS 2 implementation rather than an inherent necessity. This complexity has prevented the effective utilization of traditional scheduling techniques. An effort of extending the _EventsExecutor_ addressed this issue [19], but it provides only limited functionality. 

We propose a middleware design that enables direct configuration of OS scheduling parameters (scheduler, schedulerspecific parameters, and affinity) for each callback, bypassing nested scheduling. Consequently, real-time scheduling in ROS 2 no longer needs to account for the presence of the Executor in theoretical models. Instead, focus can be placed exclusively on the callback dependency graph and enforcement of the scheduling parameters on callback vertices. We develop **_CallbackIsolatedExecutor_** and the corresponding _Component Container_ with the one-to-one correspondence between callbacks and OS threads. _CallbackIsolatedExecutor_ eliminates the need for future research to address the nested scheduling problem in ROS 2 applications. Furthermore, we evaluate the overhead of _CallbackIsolatedExecutor_ compared to _SingleThreadedExecutor_ and _MultiThreadedExecutor_ . 

**Contributions.** The main contributions of this paper include the following: 

- 1) We propose a middleware design that eliminates nested scheduling by establishing a persistent one-to-one correspondence between callbacks and OS threads. 

- 2) We formulate the scheduling problem of ROS 2 on Linux so the Executor layer can be ignored. 

- 3) We demonstrate that _CallbackIsolatedExecutor_ keeps acceptable overheads compared to existing Executors. 

© 2025 IEEE. Personal use of this material is permitted. DOI: 10.1109/RTAS65571.2025.00017 


(a) Existing Executors’ callback enforcement 


Fig. 2: Middleware design of existing Executors and _CallbackIsolatedExecutor_ in ROS 2 applications on Linux. 

II. NEW ROS 2 EXECUTOR DESIGN 

**Essence of ROS 2 Real-time Scheduling** . A ROS 2 application comprises DAGs formed by callback chains. Dependencies between DAGs via shared variables in nodes are incorporated into the cause-effect model. A recent study [20] proposes setting independent deadlines for each DAG, as applying cause-effect chains to complex ROS 2 applications, such as Autoware [21], [22], is impractical. Regardless of the modeling approach, the scheduling problem of ROS 2 systems fundamentally concerns how CPU resources are allocated to callbacks, which act as subtasks in DAG scheduling. 

**Artificial Complexity in Scheduling Imposed by ROS 2’s Implementation** . In ROS 2 systems, scheduling parameters should ideally be applied directly to each individual callback (subtask). However, due to the implementation constraints of the existing ROS 2 Executors, this is not feasible (Fig. 2(a)). ROS 2 provides two primary types of Executors: the _SingleThreadedExecutor_ and the _MultiThreadedExecutor_ . In the _SingleThreadedExecutor_ , multiple callbacks are assigned to a single OS thread. Since scheduling parameters are set at the OS thread level, they cannot be configured per callback in this model. In contrast, the _MultiThreadedExecutor_ employs multiple OS threads and dispatches callbacks in a many-tomany relationship, with each invocation randomly assigned to a thread. As a result, specific scheduling parameters cannot be assigned to individual callbacks. Both Executors adopt a ROS 2-specific round-robin-like scheduling policy, hindering the direct application of classical real-time and DAG scheduling theories. Consequently, ROS 2 Executor-specific scheduling theories have been studied in recent years. Unlike existing Executors that poll a _wait-set_ , the _EventsExecutor_ pushes executable callbacks directly into a FIFO queue upon event occurrence. However, it also encounters nested scheduling. 

**Ignore the Executor, Focus on the Callback Graph** . To 

configure scheduling parameters on a per-callback basis, we propose a novel middleware design where each callback has a dedicated OS thread (Fig. 2 (b)). Since each OS thread corresponds to a single callback, scheduling parameters can be applied by setting them on the corresponding thread. If a callback never gets ready for the next period until the previous execution finishes (i.e., its minimum inter-arrival time exceeds its worst-case turnaround time), the middleware layer can be ignored in scheduling. Thus, scheduling reduces to applying OS parameters to DAG vertices, where vertices are callbacks and edges denote execution dependencies. The only concern with _CallbackIsolatedExecutor_ is the overhead introduced by maintaining a one-to-one mapping between callbacks and OS threads. This issue is discussed and evaluated in Section IV. 

III. PROPOSED ROS 2 SCHEDULING PROBLEM 

With _CallbackIsolatedExecutor_ , the scheduling in ROS 2 applications can be modeled without considering the presence of the middleware layer. The proposed scheduling problem formulation on ROS 2 Linux assumes the following two constraints. We should design ROS 2 applications accordingly. 

- **Each** **_CallbackGroup_ Contains One Callback** . In ROS 2, _CallbackGroup_ is a mechanism for grouping callbacks intended not to be executed in parallel. The previous section discussed a one-to-one mapping between callbacks and OS threads, but in practice, _CallbackGroups_ , not callbacks, are mapped to threads. To implement Fig. 2 (b), each callback must belong to a separate _CallbackGroup_ . The primary purpose of a _CallbackGroup_ is to facilitate mutual exclusion for shared resources, but they should fundamentally be managed using mutexes. 

- **Callbacks are Not Reentrant** . As mentioned in Section II, the assumption “a callback never gets ready for the next period until the previous execution finishes” must hold. Many practical ROS 2 applications do not implement 


Fig. 3: Proposed formulation of ROS 2 scheduling enforcement. We directly specify scheduler, scheduler-specific parameters, and core affinity for each callback. 

reentrant callbacks, making this constraint reasonable. If this assumption does not hold (e.g., when a callback has a long execution time), the callback can be split into multiple smaller callbacks to enable pipeline processing. 

Under these two constraints, scheduling enforcement in ROS 2 on Linux follows Fig. 3, where each callback is assigned a scheduling policy, policy-specific parameters, and core affinity (i.e., which CPU core it runs on). This formulation aligns with classical real-time and DAG scheduling theories, enabling the leverage of existing research assets. 

Linux provides three types of schedulers, ranked in order of priority: Earliest Deadline First (EDF), FIFO, and Completely Fair Scheduler (CFS). Each scheduler operates independently, such that higher-priority schedulers may preempt or affect lower-priority ones, but not vice versa. Leveraging this property, as illustrated in Fig. 2 (b), the unused CPU time from EDF and FIFO schedulers can be fully exploited by CFS. Real-time DAGs run on an EDF scheduler or FIFO scheduler, while non-real-time DAGs and other threads use CFS, ensuring real-time scheduling and maximizing CPU utilization. Largescale ROS 2 applications, such as Autoware, often involve hundreds of nodes. Additionally, efficient CPU utilization is crucial for power efficiency, making this approach essential. The characteristics of each scheduler are described below: 

- **EDF scheduler:** In Linux, the EDF scheduler is combined with the Constant Bandwidth Server (CBS). Originally designed for traditional periodic tasks, it may have potential applications for DAG scheduling. 

- **FIFO scheduler:** A preemptive static priority scheduler. Scheduling of callback graphs on this scheduler is formulated as fixed-priority preemptive DAG scheduling. It is a primary option for DAG scheduling. 

- **CFS:** A scheduler that aims to achieve fair CPU time distribution by prioritizing tasks with the least virtual runtime (vruntime). The nice value reduces vruntime growth by about 10% per decrement, increasing a task’s CPU share. 

## IV. OVERHEAD OF CALLBACK ISOLATED EXECUTOR 

From the perspective of theoretical real-time scheduling models, _CallbackIsolatedExecutor_ is a superior choice, of- 


Fig. 4: Experimental conditions. 

fering only advantages. However, the overhead of mapping each callback to a dedicated thread must be discussed. We measure user-kernel switches, context switches, and memory consumption. Additionally, we discuss _wait-set_ contention due to thread count increases. The evaluation platform uses an Intel Xeon E-2278GE (3.30 GHz, 8 cores, 16 threads with HyperThreading), 32 GB RAM, Ubuntu 22.04 LTS, Linux kernel 6.8, and ROS 2 Humble with Cyclone DDS. 

To evaluate overheads of _CallbackIsolatedExecutor_ against existing Executors, we prepare a ROS 2 node pair with publish-subscribe communication with the varied experimental conditions shown in Fig. 4. Each publisher and subscriber node holds N callbacks (N = 1, 4, .., 24), each in a separate CallbackGroup, maintaining a one-to-one mapping. The publisher node runs a timer callback that publishes every 10 ms, while the subscriber node executes a subscription callback that receives messages. We compare the impact of N on overhead across _SingleThreadedExecutor_ , _MultiThreadedExecutor_ , and _CallbackIsolatedExecutor_ . To examine inter-process vs. intraprocess differences, we run publisher and subscriber nodes either in separate or shared processes. For inter-process communication conditions, we plot the sum of the measurements from the publisher and subscriber node processes. 

Fig. 5 shows the impact of callback count on overhead factors for each Executor. Memory consumption in _CallbackIsolatedExecutor_ is slightly higher but negligible. Compared to _MultiThreadedExecutor_ , despite _MultiThreadedExecutor_ being limited by hardware concurrency, _CallbackIsolatedExecutor_ outperforms it in all but user-kernel mode switches in the same process. The slight advantage of _MultiThreadedExecutor_ in user-kernel mode switches under intra-process execution is likely due to pointer passing communication, allowing to bypass kernel-space operations. Compared to _SingleThreadedExecutor_ , _CallbackIsolatedExecutor_ maintains user-kernel mode switches and context switches within a fixed ratio. These switches remain within about 5× for intra-process publishsubscribe and 1.4× for inter-process communication. This ratio is bounded regardless of the number of callbacks. 

In _MultiThreadedExecutor_ , multiple threads share one _waitset_ , incurring overhead from reconstructing the _wait-set_ and acquiring locks. In contrast, _CallbackIsolatedExecutor_ does not share _wait-set_ across threads, eliminating this overhead. 


Fig. 5: Comparison of _CallbackIsolatedExecutor_ overhead with existing Executors (see Fig. 4 for experimental conditions) 

## V. CONCLUSION AND FUTURE WORK 

With _CallbackIsolatedExecutor_ , the real-time community no longer needs to account for the existence of the Executor in ROS 2 scheduling **in practical cases** . This is because realworld ROS 2 systems rarely have dozens of callbacks per node, and the opportunistic locking mechanisms based on futexes in Linux tend to scale well with a large number of threads and low levels of contention. As future work, we plan to evaluate our approach on real-world systems such as Autoware, and to explore concrete scheduling techniques tailored to such systems. Scheduling research will advance based on our formulation proposed for ROS 2 applications on Linux. _CallbackIsolatedExecutor_ is available as open-source<sup>*</sup> . 

## VI. ACKNOWLEDGMENT 

This research is based on results obtained from Green Innovation Fund Projects / Development of In-vehicle Computing and Simulation Technology for Energy Saving in Electric Vehicles, JPNP21027, subsidized by the New Energy and Industrial Technology Development Organization (NEDO) and partially by JST PRESTO Grant Number JPMJPR21P1. 

## REFERENCES 

- [1] “Open source robotics foundation (OSRF). ROS2.” [Online]. Available: https://github.com/ros2. 

- [2] A. Li and N. Zhang, “Data-flow availability: Achieving timing assurance in autonomous systems,” in _Proc. of 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI)_ , 2024. 

- [3] H. Teper, M. G¨unzel, N. Ueter, G. von der Br¨uggen, and J.-J. Chen, “End-to-end timing analysis in ROS2,” in _Proc. of IEEE Real-Time Systems Symposium (RTSS)_ , 2022. 

- [4] H. Teper, T. Betz, G. Von Der Br¨uggen, K.-H. Chen, J. Betz, and J.-J. Chen, “Timing-aware ROS 2 architecture and system optimization,” in _Proc. of IEEE 29th International Conference on Embedded and RealTime Computing Systems and Applications (RTCSA)_ , 2023. 

- [5] H. Teper, T. Betz, M. G¨unzel, D. Ebner, G. von der Br¨uggen, J. Betz, and J.-J. Chen, “End-to-end timing analysis and optimization of multiexecutor ROS 2 systems,” in _Proc. of IEEE 30th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ , 2024. 

- [6] T. Blass, A. Hamann, R. Lange, D. Ziegenbein, and B. B. Brandenburg, “Automatic latency management for ROS 2: Benefits, challenges, and open problems,” in _Proc. of IEEE 27th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ , 2021. 

- [7] A. Partap, S. Grayson, M. Huzaifa, S. Adve, B. Godfrey, S. Gupta, K. Hauser, and R. Mittal, “On-device CPU scheduling for robot systems,” in _Proc. of IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2022. 

- [8] D. Casini, T. Blaß, I. L¨utkebohle, and B. Brandenburg, “Response-time analysis of ROS 2 processing chains under reservation-based scheduling,” in _Proc. of 31st Euromicro Conference on Real-Time Systems (ECRTS)_ , 2019. 

- [9] Y. Tang, Z. Feng, N. Guan, X. Jiang, M. Lv, Q. Deng, and W. Yi, “Response time analysis and priority assignment of processing chains on ROS2 executors,” in _Proc. of IEEE Real-Time Systems Symposium (RTSS)_ , 2020. 

- [10] H. Choi, Y. Xiang, and H. Kim, “PiCAS: New design of priority-driven chain-aware scheduling for ROS2,” in _Proc. of IEEE 27th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ , 2021. 

- [11] T. Blaß, D. Casini, S. Bozhko, and B. B. Brandenburg, “A ROS 2 response-time analysis exploiting starvation freedom and execution-time variance,” in _Proc. of IEEE Real-Time Systems Symposium (RTSS)_ , 2021. 

- [12] H. Choi, D. Enright, H. Sobhani, Y. Xiang, and H. Kim, “Priority-driven real-time scheduling in ROS 2: Potential and challenges,” in _Proc. of 1st International Workshop on Real-time And intelliGent Edge computing (RAGE)_ , 2022. 

- [13] X. Jiang, D. Ji, N. Guan, R. Li, Y. Tang, and Y. Wang, “Real-time scheduling and analysis of processing chains on multi-threaded executor in ROS 2,” in _Proc. of IEEE Real-Time Systems Symposium (RTSS)_ , 2022. 

- [14] K. Chaaban, “A new algorithm for real-time scheduling and resource mapping for robot operating systems (ROS),” _Applied Sciences_ , vol. 13, no. 3, p. 1532, 2023. 

- [15] Y. Tang, N. Guan, X. Jiang, X. Luo, and W. Yi, “Real-time performance analysis of processing systems on ROS 2 executors,” in _Proc. of IEEE 29th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ , 2023. 

- [16] H. Sobhani, H. Choi, and H. Kim, “Timing analysis and priority-driven enhancements of ROS 2 multi-threaded executors,” in _Proc. of IEEE 29th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ , 2023. 

- [17] A. Al Arafat, K. Wilson, K. Yang, and Z. Guo, “Dynamic priority scheduling of multithreaded ROS 2 executor with shared resources,” _IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems_ , vol. 43, no. 11, pp. 3732–3743, 2024. 

- [18] H. Teper, D. Kuhse, M. G¨unzel, G. von der Br¨uggen, F. Howar, and J.-J. Chen, “Thread carefully: Preventing starvation in the ROS 2 multithreaded executor,” _IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems_ , vol. 43, no. 11, pp. 3588–3599, 2024. 

- [19] H. Teper, O. Bell, M. G¨unzel, C. Gill, and J.-J. Chen, “Bridging the gap between ROS 2 and classical real-time scheduling for periodic tasks,” 2024. [Online]. Available: https://arxiv.org/abs/2408.03696 

- [20] A. Yano and T. Azumi, “Work-in-progress: Multi-deadline DAG scheduling model for autonomous driving systems,” in _Proc. of IEEE Real-Time Systems Symposium (RTSS)_ , 2024. 

- [21] S. Kato, E. Takeuchi, Y. Ishiguro, Y. Ninomiya, K. Takeda, and T. Hamada, “An open approach to autonomous vehicles,” _IEEE Micro_ , vol. 35, no. 6, pp. 60–68, 2015. 

- [22] S. Kato, S. Tokunaga, Y. Maruyama, S. Maeda, M. Hirabayashi, Y. Kitsukawa, A. Monrroy, T. Ando, Y. Fujii, and T. Azumi, “Autoware on board: Enabling autonomous vehicles with embedded systems,” in _Proc. of ACM/IEEE International Conference on Cyber-Physical Systems (ICCPS)_ , 2018. 

> *https://github.com/sykwer/callback <u>isolated executor.</u> 

