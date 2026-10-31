---
title: "ROS 2 Agnocast: Supporting Unsized Message Types for True Zero-Copy Publish/Subscribe IPC"
date: "2025-06-20"
authors: "Takahiro Ishikawa-Aso; Shinpei Kato"
url: https://arxiv.org/abs/2506.16882
pdf: https://arxiv.org/pdf/2506.16882
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2506.16882)** / [論文ページ](https://arxiv.org/abs/2506.16882)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# ROS 2 Agnocast: Supporting Unsized Message Types for True Zero-Copy Publish/Subscribe IPC 

Takahiro Ishikawa-Aso and Shinpei Kato 

The University of Tokyo 

TIER IV, Inc. 

**_Abstract_ —Robot applications, comprising independent components that mutually publish/subscribe messages, are built on inter-process communication (IPC) middleware such as Robot Operating System 2 (ROS 2). In large-scale ROS 2 systems like autonomous driving platforms, true zero-copy communication—eliminating serialization and deserialization—is crucial for efficiency and real-time performance. However, existing true zerocopy middleware solutions lack widespread adoption as they fail to meet three essential requirements: 1) Support for all ROS 2 message types including unsized ones; 2) Minimal modifications to existing application code; 3) Selective implementation of zerocopy communication between specific nodes while maintaining conventional communication mechanisms for other inter-node communications including inter-host node communications. This first requirement is critical, as production-grade ROS 2 projects like Autoware rely heavily on unsized message types throughout their codebase to handle diverse use cases (e.g., various sensors), and depend on the broader ROS 2 ecosystem, where unsized message types are pervasive in libraries. The remaining requirements facilitate seamless integration with existing projects. While IceOryx middleware, a practical true zero-copy solution, meets all but the first requirement, other studies achieving the first requirement fail to satisfy the remaining criteria. This paper presents** **_Agnocast_ , a true zero-copy IPC framework applicable to ROS 2 C++ on Linux that fulfills all these requirements. Our evaluation demonstrates that** **_Agnocast_ maintains constant IPC overhead regardless of message size, even for unsized message types. In Autoware PointCloud Preprocessing,** **_Agnocast_ achieves a 16% improvement in average response time and a 25% improvement in worst-case response time.** 

**_Index Terms_ —Robot programming, Multiprocessing systems, Concurrency control, Low latency communication, Middleware, Publish-subscribe, Memory management, Runtime environment** 

## I. INTRODUCTION 

With recent advancements in computing technology, largescale robotic applications, including autonomous driving systems, have become vital infrastructures in modern society. Robot applications are composed of independent components that interact through a message-passing mechanism on publish/subscribe communication middleware, such as Robot Operating System 2 (ROS 2) [1]. ROS 2 is a de-facto standard platform underlying many robot applications today. The performance of Inter-Process Communication (IPC), foundational to the publish/subscribe mechanism, is critical for minimizing latency and ensuring overall system efficiency. High IPC latency can deteriorate the response times of robotic applications, and the increased CPU and memory costs associated with IPC negatively impact overall system throughput 

and exacerbate memory pressure. To minimize IPC cost, eliminating copies including serialization and deserialization is ideal, which we call **true zero-copy** . In ROS 2, true zero-copy communication can be achieved by placing nodes within the same process through the _ComponentContainer_ feature [2]. However, this method compromises fault isolation. For example, in autonomous driving systems, numerous nodes work collaboratively to achieve functionalities such as localization and object recognition. When fault isolation is not implemented through process separation between nodes, the failure of a single node’s process can lead to complete system failure. Therefore, there is a strong motivation to implement true zero-copy communication that enables node distribution across separate processes without sacrificing IPC performance. 

Although practical true zero-copy middleware already exists, it is restricted to handling messages of static size. IceOryx [3], [4] is a practical true zero-copy middleware that allows direct access from the ROS 2 standard interface when using CycloneDDS [5]. However, its limitation to handling only ROS 2 messages of static size necessitates the rewriting of message definition files for each project to hardcode static array sizes. Additionally, any existing source code that assumes unsized arrays (e.g. std::vector in C++) must also be modified to accommodate the static array requirements. Many libraries in the ROS 2 community are designed under the assumption that message types are unsized. Autoware [6], [7], one of the large-scale ROS 2 applications, relies heavily on unsized message types throughout their codebase to handle diverse use cases (e.g., various sensors) and to utilize broader ROS 2 ecosystem, where unsized message types are pervasive. 

True zero-copy publish/subscribe IPC for unsized message types has involved trade-offs with existing middleware standards compliance. This means it has required substantial rewriting of existing user code and surrounding libraries. Research has explored middleware for ROS 1 and ROS 2 that enables true zero-copy IPC for unsized message types, such as TZC [8] and LOT [9]. However, these approaches fall short of practical application in real-world projects due to limitations in standards compliance and usability. As depicted in Fig. 1, achieving true zero-copy communication while maintaining fault isolation typically necessitates directly constructing all message data in shared memory. This, in turn, often requires library users to be aware of, and directly manage, shared memory allocation. TZC and LOT, while achieving true zero-copy for unsized message types, impose significant constraints on 

© 2025 IEEE. Personal use of this material is permitted. 


Fig. 1: True zero-copy IPC in publish/subscribe communication. Process A constructs messages directly in shared memory, while Processes B and C read them directly from the shared memory without serialization or deserialization. 

application code. TZC’s partial serialization approach requires custom message type implementations and pre-allocation of array sizes. LOT, similarly, requires conversion to custom message formats and imposes library-specific coding constraints. These limitations not only increase development overhead but also severely restrict the flexibility of application development by preventing the free use of methods like std::vector:: push_back, which may require reallocation at arbitrary times. Existing publish/subscribe middleware, including ROS 2 and its underlying rmw implementations [5], [10]–[12], was not designed with true zero-copy support for unsized message types in mind, further compounding the challenge. 

This study introduces a true zero-copy framework, named **_Agnocast_** , applicable to ROS 2 C++ on Linux platforms. It supports all ROS 2 message types including unsized message types, enabling true zero-copy communication without compromising ROS 2 compliance. Adapting _Agnocast_ requires changes only to the ROS 2 publish/subscribe APIs and a smart pointer type for the IPC messages. We first identify a constraint within the C++ language ecosystem and Interface Definition Language (IDL) that makes it impossible to specify a memory allocation strategy for ROS 2 message objects. This constraint impedes the allocation of message objects with unsized types in shared memory while adhering to ROS 2 standards. To address this issue, _Agnocast_ intercepts all heap allocations using the LD_PRELOAD functionality and makes the entire heap area accessible to subscriber processes in a read-only mode. In addition to enabling zero-copy communication, our _bridge_ feature allows ROS 2 communication and _Agnocast_ communication to be mutually relayed, enabling specific edges (communication between two specific nodes) to utilize true zero-copy while allowing the entire ROS 2 system to maintain its original functionality. _Agnocast_ is independent of the 

specifics of existing middleware implementations in ROS 2, such as CycloneDDS [5], FastDDS [10], RTI Connext [11], and Zenoh [12], allowing it to remain agnostic to changes in _rmw_ implementation [13]. The _Agnocast_ IPC framework’s concept is not tied to ROS 2 and can be adapted for other middleware systems with similar requirements and constraints. 

**Contributions.** The main contributions of this paper include the following: 

- 1) We propose a novel IPC technology that achieves true zero-copy communication with minimal code modifications through a new smart pointer design, particularly effective for systems unable to specify memory allocation strategies in application code. 

- 2) The _Agnocast_ IPC framework supports all ROS 2 message types, covering unsized message types, for true zero-copy publish/subscribe communication without compromising compliance with ROS 2 standards. 

- 3) We develop _Agnocast_ for ROS 2 as open-source and demonstrate the performance of the zero-copy feature. 

## II. MOTIVATION 

Autoware [6], [7] is the world’s leading open-source project for autonomous driving, built on ROS 2 C++, representing a widely adopted autonomous system in real-world applications. ROS 2’s component-based architecture enables node-based development of various functionalities. These nodes can be flexibly combined to construct autonomous driving systems that meet specific operational requirements. This paper proposes a design for true zero-copy middleware that is highly applicable to real-world ROS 2 applications. We analyze Autoware as a representative case study to establish the fundamental background for determining middleware requirements. 

Autoware’s autonomous driving systems call for true zerocopy IPC for publish/subscribe messaging. The system combines hundreds of nodes exchanging messages such as large pointcloud data. While these systems often span multiple hosts, most message communication occurs between processes on the same host. Message transfer across processes incurs copy costs from serialization/deserialization and underlying communication middleware such as Data Distribution Service (DDS), resulting in increased inter-node latency, CPU usage, and memory pressure. Therefore, zero-copy communication for same-host processes is essential. While _ComponentContainer_ enables true zero-copy communication through pointer passing within a single process, this approach compromises safety requirements of fault isolation. Autonomous driving systems require fault isolation between nodes, necessitating node deployment in separate processes. These factors establish the need for true zero-copy inter-process communication. 

Despite the existence of true zero-copy middleware solutions such as IceOryx, their adoption in Autoware has been limited. This is primarily because Autoware extensively uses unsized message types (e.g., message types containing C++’s std::vector). Almost all of the ROS 2 nodes implemented in Autoware [14] depend on unsized message types. Existing practical true zero-copy middleware solutions, including 

IceOryx, only support static-sized message types. Autoware’s prevalent use of unsized message types stems from its design goal of handling multiple use cases within a single codebase. For example, a sensor data preprocessing node can handle various sensor types with a single implementation. Furthermore, numerous library assets in the ROS 2 ecosystem depend on standardized unsized message types. Therefore, facilitating adoption in projects such as Autoware, which heavily utilize unsized ROS 2 message types, requires a true zero-copy middleware that supports unsized message types. 

## III. REQUIREMENTS AND CONSTRAINTS 

Based on the requirements listed in Section III-A and the ecosystem constraints outlined in Section III-B, we introduce our middleware architecture in Section IV. 

## _A. Middleware Design Requirements_ 

We design a true zero-copy IPC framework named _Agnocast_ with the following requirements. 

- 1) **True zero-copy with unsized message types.** We do not incur copying costs, including serialization and deserialization when transferring ROS 2 messages between processes. It supports true zero-copy communication for all ROS 2 message types, including unsized ones. 

- 2) **ROS 2 Compliant.** True zero-copy communication can be integrated into ROS 2 applications with minimal modifications to the existing code. We do not need to rebuild tools or libraries, including generated codes related to ROS 2 messages. 

- 3) **Continuous operation of the ROS 2 entire system.** True zero-copy is applied only at the edges between 

- explicitly targeted pairs of nodes. The remainder of the topic communication continues as before utilizing existing _rmw_ communication stacks. 

The first requirement serves as the main purpose of our middleware, while the remaining ones facilitate seamless integration with existing projects. As explained in Section II, supporting unsized message types (e.g., message types including std::vector members) is important for widespread adoption. The definition of an **unsized message type** is a type for which memory reallocation can occur at arbitrary times, whereas a **static-sized message type** is one whose memory size is determined at compile time. In TZC [8] and LOT [9], although array sizes in messages can be specified dynamically at runtime, this is permitted only once during initialization. As they do not support memory reallocations at arbitrary times (e.g., std::vector::resize), they are not considered to support unsized message types. The second requirement is to avoid adoption barrier seen in solutions such as TZC and LOT, which require extensive modifications to existing application code and message structures; instead, as illustrated in Fig. 2, our middleware implements zerocopy functionality through modifications to publish/subscribe APIs and smart pointer types only. Given that some ROS 2 applications involve numerous nodes and topics, the third 


Fig. 2: All needed changes to apply _Agnocast_ in ROS 2 

requirement becomes critical to enable selective and incremental adoption of zero-copy communication, starting with the most bandwidth-intensive edges; furthermore, this requirement ensures seamless integration with existing _rmw_ middleware for cross-host communications, as zero-copy can only be implemented between nodes on the same host. 

## _B. Middleware Design Constraints in ROS 2_ 

In designing true zero-copy middleware for ROS 2 C++, a key constraint is the inability to specify custom memory allocators for ROS 2 message objects. 

Custom memory allocation for ROS 2 message structures is essential for true zero-copy implementation, as messages must be directly constructed on shared memory. For staticsized message types, middleware such as IceOryx [3], [4] can predetermine the required memory size to construct a message. However, for unsized messages (e.g. containing std::vector ), additional memory allocations occur at arbitrary times in runtime, such as during std::vector::push_back operations. Therefore, the memory allocation strategy must be customized to ensure all message data resides on shared memory. 

However, as depicted in Fig. 3, specifying custom memory allocators for ROS 2 message structures faces significant challenges. Container types such as std::vector receive an allocator type as a template argument, seemingly enabling the customization of memory allocation strategies by specifying an allocator that allocates memory from shared memory. However, the _rosidl_ system, responsible for automatically generating source code for ROS 2 message structures, does not allow for the passing of custom memory allocators to container objects within these structures, as the allocator type is hardcoded as std::allocator<void> in its _empy_ template 


Even C++17’s polymorphic allocators (e.g., std::vector< int, std::pmr::polymorphic_allocator<int>>), which enable allocator specification without changing container types, fail to resolve this issue. While hardcoding the allocator type to a polymorphic allocator in the _rosidl_ code generation process might seem promising, container types using polymorphic allocators are incompatible with existing code that assumes standard container types. Converting all container types in ROS 2 libraries to use polymorphic allocators could theoretically solve this incompatibility, but such extensive modifications across the entire ecosystem are impractical. 

Fig. 5: _Agnocast_ memory mapping 

## _A. Agnocast Memory Mapping_ 

Given the constraint that container types like std::vector cannot receive memory allocation strategies, maintaining ROS 2 compliance while placing message objects in shared memory necessitates replacing the entire heap allocation system. Virtual memory allocation in C++ container types is controlled by two layers: the allocation strategy passed as template arguments at the container level, and the underlying heap allocation runtime corresponding to _malloc_ and _free_ functions. Since the top-level allocation strategy cannot be utilized in ROS 2 as discussed in Section III-B, we opt to customize the lower layer. Customizing the heap allocation runtime involves replacing _malloc_ and _free_ functions to handle shared memory regions instead of standard heap memory. 


Fig. 5 illustrates memory mapping in _Agnocast_ using three participating processes as an example. The diagram shows how the Memory Management Unit (MMU) maps the Virtual Address Spaces (VAS) of three processes to shared memory in physical memory. The memory mapping in _Agnocast_ processes has three key characteristics: 

Fig. 4: _Agnocast_ software stack 

## IV. AGNOCAST IPC FRAMEWORK 

- 1) All heap allocations and deallocations are hooked via LD_PRELOAD and redirected to operations within a designated virtual address range. 

In this section, we detail the design of an IPC framework that addresses the requirements specified in Section III-A, considering the constraints outlined in Section III-B. 

- 2) This designated virtual address range is mapped to shared memory in physical memory. 

Fig. 4 illustrates the software stack of _Agnocast_ and its integration with existing IPC middleware, such as ROS 2. _Agnocast_ is positioned independently of existing IPC middleware while operating in coordination with it. As an IPC technology, 

- 3) Subscriber processes map the publisher process’s heap into their VAS at the same offset in read-only mode, prohibiting writes to the publisher’s heap. 

This memory mapping enables subscriber processes to directly reference any objects placed in the publisher process’s heap. In this memory mapping, true zero-copy IPC is achieved by simply passing object addresses from publisher to subscriber processes, as pointers remain valid when referenced objects maintain identical virtual addresses across processes. We assume a fixed heap size on shared memory; however, since this refers to a virtual address range rather than physical memory, it can be set sufficiently large. Since _Agnocast_ explicitly specifies the starting address for mmap, and no pointers to outside shared memory are created within the shared memory, Address Space Layout Randomization (ASLR) has no effect. 

For subscriber processes to reference publisher processes’s message objects through this method, all message objects must reside on the heap. This requirement is naturally satisfied for ROS 2 messages because they consist only of primitive types and arrays (equivalent to standard arrays or std::vector in C++), without direct pointer handling [15]. Conforming to the memory allocation API shown in Fig. 2 ensures all ROS 2 message objects are allocated on the heap. While polymorphic subtype objects typically contain a hidden vtable pointer in process-local memory—requiring techniques like DVT/GVT [16] and IVT [17] for inter-process transfer—ROS 2 message objects are non-polymorphic, eliminating this concern. 

## _B. Shared Metadata Transactionality_ 

The management of publish/subscribe communication metadata, such as message virtual addresses and reference counts, is implemented in a kernel module (Fig. 6). This module maintains topic-specific metadata and message queues for each publisher. Queue entries contain virtual addresses for interprocess message transfer, reference counters, and subscriber receipt tracking information, which are essential for determining message object release timing. The processes update these shared data through _ioctl_ syscall, while the kernel module hooks process exits and maintains data consistency even when a process unexpectedly terminates. 


Fig. 6: _Agnocast_ kernel module 

The key rationale for kernel-based metadata management is to ensure the transactional integrity of shared data operations. To prevent data corruption, metadata operations must either complete atomically or support proper rollback mechanisms. 

For implementation simplicity, _Agnocast_ adopts the former approach by implementing metadata operations as kernel module system calls, ensuring that updates complete regardless of process termination timing. Alternatively, the mechanism could be implemented as a user-space daemon instead of a kernel module, which would require rollback functionality to prevent data corruption. 

## _C. Timing to Deallocate Messages_ 

As shown in Fig. 7, an allocated message object can be freed when both its _reference count_ and _unreceived subscriber count_ drop to zero within the allocating process. While conventional heap memory can be deallocated when its reference count reaches zero (e.g., with std::shared_ptr ), message objects in _Agnocast_ require a different approach due to their multi-process accessibility. _Agnocast_ implements its own smart pointer (Fig. 2) that manages both a _reference count_ and an _unreceived subscriber count_ within the kernel module (Fig. 6). The smart pointer increments the reference count upon creation or duplication and decrements it upon destruction. Memory deallocation occurs when both counts reach zero, and can only be executed by the publisher process that initially allocated the message, according to its release timing policy. As described in Section IV-B, the kernel module monitors process termination and updates both the _reference count_ and _unreceived subscriber count_ accordingly to maintain their validity even when processes terminate unexpectedly. 


Fig. 7: The timing of deallocating _Agnocast_ message data 

## _D. Cooperate with Existing Middleware_ 

To meet Requirement 3 in Section III-A, _Agnocast_ launches a _bridge_ process per topic, as described in Fig. 8, to mediate between existing middleware (e.g. ROS 2) communications and _Agnocast_ communications. This _bridge_ process publishes data received from an existing middleware topic to an _Agnocast_ topic while it publishes data obtained from an _Agnocast_ topic to an existing middleware topic. To prevent infinite loops, the _bridge’s_ subscription callback ignores messages originating from itself in both communication paths. Through this mechanism, messages published in either communication space reach the corresponding subscription callbacks in the other communication space. This satisfies Requirement 3 in 


Fig. 8: Relaying between _Agnocast_ communication and existing middleware communication 

Section III-A, enabling true zero-copy communication for the targeted communication edges while maintaining the functionality of the whole system. 

## V. EVALUATION 

In this chapter, we evaluate _Agnocast_ ’s performance for ROS 2 under the environment specified in TABLE I. Some experimental measurements are represented using violin plots, with vertical bars indicating the maximum and minimum values in the datasets. 

TABLE I: Evaluation platform. 

|Processor|Intel (R) Xeon (R) E-2278GE CPU @ 3.30 GHz|
|---|---|
|Number of Cores|8 * 2 (Hyper-Threading Enabled)|
|Memory|32 GB|
|OS Kernel|Linux Kernel 6.2|
|OS Distribution|Ubuntu 22.04 LTS|
|ROS 2|Humble|
|DDS|Cyclone DDS|


## _A. IPC Efficiency_ 

To evaluate the efficiency of _Agnocast_ IPC mechanisms against other ROS 2 IPC mechanisms, we conduct communication latency measurements between publisher and subscriber nodes running in separate processes. We compare standard ROS 2 communication via CycloneDDS, the existing practical true zero-copy middleware IceOryx, and our proposed _Agnocast_ approach. The evaluation setup consists of one-to-one publisher-subscriber pairs, with threads scheduled by the Completely Fair Scheduler (CFS) under no additional system load, measuring communication latency across varying message sizes (1KB, 10KB, 100KB, and 1MB). For each configuration, we plot the latency distribution of 1,000 message transmissions performed consecutively at 100ms intervals, excluding the first 10 measurements to avoid initialization effects. To demonstrate practical applicability in real-world ROS 2 applications, we focus on the _PointCloud2_ message type communication, which represents a significant bottleneck in Autoware as discussed 

in Section II. Since IceOryx only supports true zero-copy communication for static-sized message types, we evaluate it under two conditions: using the unsized _PointCloud2_ message type and using an equivalent static-sized custom message type. Notably, we exclude existing true zero-copy approaches such as TZC and LOT from our comparison as they fail to meet the requirements outlined in Section III-A: they do not support unsized message types and require significant modifications to existing ROS 2 application code and the use of message type implementations specialized for their respective methods, making them impractical for real-world adoption. 


Fig. 9: Comparison of communication latency ( _Agnocast_ , IceOryx and ROS 2) 

Fig. 9 plots the communication latency from message publication to subscriber callback invocation across different message sizes for _Agnocast_ and the compared IPC mechanisms. _Agnocast_ maintains consistent communication latency regardless of message size, even for unsized message types like _PointCloud2_ . For IceOryx, when using static-sized message types, true zero-copy communication effectively maintains constant latency across message sizes. However, when communicating unsized message types, IceOryx incurs transparent serialization costs to shared memory and deserialization costs from shared memory, leading to increased latency as message size grows. While IceOryx handling unsized message types was expected to show lower IPC costs than CycloneDDSbased communication by avoiding copy costs in the network stack, measurements revealed higher latency for IceOryx; we do not investigate the detailed cause here. The results demonstrate that _Agnocast_ achieves true zero-copy communication even for unsized message types, showing a particular advantage over IceOryx—the only realistic “competitor”—at larger message sizes. 

## _B. IPC Performance Stability under CPU load_ 

Next, we evaluate the stability of IPC performance under CPU load by measuring the communication latency of _Agnocast_ and the compared IPC mechanisms while applying system load using _stress-ng_ [18]. We conduct experiments under the same conditions as Section V-A, except that the message size is fixed at 100KB. We vary the CPU load utilization from 

0% to 90% (0%, 30%, 60%, and 90%) by creating _stressng_ processes equal to the number of logical processors, with each process’s CPU utilization set to the target load condition. In this experiment, we set the subscriber’s callback thread scheduling policy to _SCHED_FIFO_ to eliminate the impact of the subscriber’s runqueue latency on the communication latency measurements. When we define communication latency as the time from message publication to subscriber callback invocation, it can be broken down into two elements: the time from message publication until the subscriber’s callback thread becomes ready, plus the time from the callback thread becoming ready until it is scheduled and begins execution. While the latter element had minimal impact in Section V-A’s experiments due to the absence of CPU load, it becomes significant in the current experiments with CPU load. From the perspective of real-time scheduling problem based on the Directed Acyclic Graph (DAG) task model, we are only interested in the former element (the delay from a DAG’s preceding subtask completion until the subsequent subtask becomes ready for execution), hence we adopt this workaround to effectively eliminate the latter element’s influence. 


Fig. 10: Stability and Real-time Performance under CPU load (Message size is fixed at 100KB) 

Fig. 10 shows the communication latency measurements for _Agnocast_ and the compared IPC mechanisms under different CPU utilization levels. Here, the communication latency is measured as the time from message publication until the subscriber’s callback becomes ready for execution. Additionally, to evaluate real-time characteristics, we present the coefficient of variation (CV) for each experimental condition. _Agnocast_ maintains high real-time performance even under 90% CPU utilization. At 30% CPU utilization, we observe that CPU usage is not always evenly distributed across cores, likely creating conditions conducive to frequent core migrations, which explain the higher CV compared to other conditions. For the other IPC mechanisms, the CV increases with CPU utilization, indicating degradation in real-time performance under higher CPU load. For IceOryx, this is attributed to scheduling delays of the daemon threads that manage IPC operations. For ROS 2 communication via CycloneDDS, the 

impact comes from scheduling delays of various involved threads, including DDS threads. The results demonstrate that _Agnocast_ maintains stable IPC performance and exhibits high real-time capabilities even under high CPU utilization. 

## _C. Bridge overhead_ 

We evaluate the overhead introduced by the “bridge” process described in Section IV-D, which mediates communication between _Agnocast_ and ROS 2. For any given topic, the “bridge” mechanism is unnecessary when all participants (publishers and subscribers) use either _Agnocast_ or ROS 2 exclusively. However, the “bridge” becomes essential when the topic includes a mix of _Agnocast_ and ROS 2 participants that need to communicate. As shown in Fig. 8, there are two bridging routes: “ _Agnocast_ publisher → bridge → ROS 2 subscriber” and “ROS 2 publisher → bridge → _Agnocast_ subscriber”, and we compare the bridging overhead of each route against standard ROS 2 communication. The experimental conditions are identical to those in Section V-A, except for the different comparison targets. 


Fig. 11: Bridge overhead 

Fig. 11 plots the time from message publication to subscriber callback invocation across different message sizes for standard ROS 2 communication and the compared bridgemediated IPC routes. Compared to standard ROS 2 communication, bridge-mediated communication incurs communication overhead proportional to message size, with overhead ranging from 0.25 to 0.50 ms for 1MB messages. This overhead arises from additional message serialization costs in the “ _Agnocast_ publisher → bridge → ROS 2 subscriber” route and additional message copy costs in the “ROS 2 publisher → bridge → _Agnocast_ subscriber” route. When introducing the bridge mechanism for incremental migration of publishers/subscribers to _Agnocast_ or for supporting inter-host communication, these overhead costs need to be considered for acceptability. 

## _D. Demonstrate on Autoware PointCloud Preprocessor_ 

To evaluate response time improvements in actual autonomous driving systems, we apply _Agnocast_ to one of the performance bottlenecks in Autoware from a response time perspective. As shown in Fig. 12, Autoware forms a comprehensive autonomous driving system through message exchanges between multiple functional units (Sensing, Map, 

Localization, Perception, Planning, Control, and Vehicle Interface). Each functional unit comprises multiple ROS 2 nodes, which communicate with other nodes through publish/subscribe messaging. Within the Sensing functionality, which preprocesses various sensor data, the LiDAR preprocessing unit consists of four preprocessing nodes connected in series for each LiDAR. The pointcloud data from all LiDARs is finally merged and published to the entire system. In this evaluation, we focus on measuring the response time of this LiDAR preprocessing functionality. According to [19], timing constraints in autonomous systems consist of three components: Freshness (latency from the occurrence of a physical phenomenon to its processing), Consistency (coherence between the programmatic observation order and physical observation order), and Stability (jitter in periodic tasks). This study contributes to enhancing the system’s capability to meet the Freshness constraint. 


Fig. 12: Overview of Autoware’s functional units and LiDAR preprocessing, showing the message flow between components and the sequential preprocessing nodes for LiDAR data. 

In this evaluation, we compare the response times before and after applying _Agnocast_ to the LiDAR Preprocessing functionality shown in Fig. 12 in Autoware version 2024.07. We use the rosbag (a data format designed for recording and replaying sensor data) publicly available in [20]. The measurement of the response time is conducted using CARET [21]. This rosbag contains data from three LiDARs (Top, Left, and Right), with the Top LiDAR processing being the response time bottleneck and thus our measurement target. While the four preprocessing nodes ( _cropbox filter self_ , _cropbox filter mirror_ , _distortion corrector_ , _ring outlier filter_ ) for each LiDAR are placed in the same process by _ComponentContainer_ , eliminating communication costs between them, the _concatenate_ node resides in a separate process, incurring IPC costs. Therefore, we apply _Agnocast_ to this topic (between _ring outlier filter_ and _concatenate_ ). The Top LiDAR preprocessing becomes a bottleneck because its pointcloud data size is significantly larger than those of the Left and Right LiDARs (Top LiDAR data is in the MB order, while the other two are in the KB order). The reason for not placing all LiDAR 

preprocessing nodes, including the concatenate node, in the same process is to maintain fault isolation. 


Fig. 13: Response time comparison in Top LiDAR preprocessing in Autoware: without (upper) and with (lower) _Agnocast_ . 

Fig. 13 plots the response time series between across Top LiDAR _cropbox filter self_ node to the _concatenate_ node (depicted as “Response Time Bottleneck” in Fig. 12), comparing the performance before and after applying _Agnocast_ . As shown in the figure, applying _Agnocast_ to just a single topic results in significant response time improvements. Before applying _Agnocast_ , the average response time is 64.5ms with a maximum value of 99.5ms. After applying _Agnocast_ , these values improve to an average of 54.5ms and a maximum of 74.3ms, achieving approximately 16% improvement in average response time and 25% improvement in maximum response time. Through _Agnocast_ , we successfully apply true zerocopy IPC for the unsized message type _PointCloud2_ , with its significant impact demonstrated in this real-world application. 

## VI. RELATED WORK 

While several studies have explored true zero-copy communication through shared memory for unsized message types in ROS 1 and ROS 2, none has been practical for real-world ROS 2 projects. TZC (Towards Zero Copy) [8] introduces a 

method of partial serialization. This approach communicates array data with dynamic size in zero-copy on shared memory, while transmitting the remaining fields through socket communication. Implementing TZC’s approach necessitates the creation of original classes with TZC-specific implementations for each message type, preventing the use of default ROS 2 messages. This approach also obliges us to write user code with library constraints in mind, such as pre-determining array sizes before calling memory allocation functions. While TZC supports zero-copy IPC for messages with dynamic size at runtime, this only means that array sizes can be determined dynamically at the beginning of callback functions in the source code. For example, it does not provide full freedom to call arbitrary functions on std::vector properties of messages. LOT (Low Overhead Transport) [9] employs the boost::interprocess shared memory feature to achieve true zero-copy communication in ROS 1, utilizing custom memory allocation on shared memory. However, this approach is impractical for developing a usable library in ROS 2, as it necessitates converting ROS 2 message types into LOTspecific formats, leading to the same challenges encountered with TZC. Like TZC, LOT also requires developers to write their code with library-specific constraints in mind. 

In ROS 2, middleware enabling true zero-copy communication for static-sized message types is already fully practical. IceOryx [3], [4] can communicate ROS 2 messages with static size in true zero-copy. IceOryx is practical for deployment, offering direct access through the ROS 2 C++ API, especially when integrated with CycloneDDS [5]. However, it becomes impractical for applications that heavily depend on unsized message types, as it requires both static array size specification in message files before compilation and extensive modifications to code that assumes unsized message types throughout the codebase. A method also exists for zero-copy communication with peripheral devices, such as GPUs [22]. However, these methods are similarly constrained to handling messages of only static size. 

Transferring polymorphic subtype objects across processes presents challenges due to vtable pointer invalidation in different processes. DVT/GVT [16] addresses this by maintaining consistent vtable addresses or using hash tables, while IVT [17] converts vtable pointers to universal indexes with processspecific correspondence tables. However, this challenge is irrelevant for ROS 2 message structures, which don’t contain polymorphic subtype objects. 

Although not directly aimed at achieving true zero-copy on shared memory, there are ongoing research efforts dedicated to lowering the costs of serialization and deserialization, which is the primary bottleneck of message-passing IPC [23]. FlatData [24], as adopted by Connext DDS [11], and Google’s FlatBuffer [25] enable direct data construction, bypassing the need for serialization and deserialization. However, this approach necessitates using specific APIs for message construction. Conversely, ROS-SF [26] introduces a new format, SFM (Serialization-free Format), which addresses the issue by ensuring the memory layout of serialization-free messages is 

identical to that of standard messages. This approach eliminates the need for code changes but requires modifications to the tool that automatically generates code for message structures from the IDL. ATSA (Adaptive Two-layer Serialization Algorithm) [27] simplifies operations and reduces costs by shifting serialization tasks from the _rmw_ layer to the programming language layer. 

## VII. DISCUSSION 

## _A. Drawbacks of mapping heap to shared memory._ 

While subscriber processes can access the publisher process’s heap, it is protected as read-only by MMU, preventing any corruption of the publisher process’s heap space. _Agnocast_ should not be used for topics where the subscriber could be potentially malicious, such as when the subscriber is a third-party node with unclear implementation details. The risk of message data being modified while being accessed by the subscriber can be eliminated without using locking mechanisms. This is because by accepting only rvalue references as arguments to the _publish()_ function, there is no way for the message content to be modified after _publish()_ is called. 

Mapping the heap onto shared memory does not worsen the total size of allocations across the system. However, it can lead to deterioration in reclaiming physical pages that correspond to virtual memory ranges freed in the heap layer. In other words, even if a shared physical page is no longer used as heap, the Linux kernel cannot reclaim it. This arises from the fact that: 1) in the case of private anonymous pages, when the page table entry (PTE) referencing that physical page is gone, the kernel automatically reclaims that physical page; 2) in the case of shared pages, even if all processes referencing the physical page discard their PTEs and the reference count to the physical page becomes zero, the physical page is not reclaimed. Issuing _MADV_REMOVE_ via the _madvice_ syscall will allow the kernel to reclaim it for reuse. However, it is difficult to determine the reclaimable memory range in the middleware layer, and it must be issued from the application code that understands the meaning of the memory range (e.g., memory for IPC messages or other uses). 

To mitigate or resolve the aforementioned drawbacks, minimizing the use of shared memory is crucial. Since _Agnocast_ aims to transfer messages with true zero-copy in publish/subscribe communication, there is inherently no need to place other memory regions on shared memory. In the prototype _Agnocast_ , all heap memory is provisionally placed on shared memory due to the difficulty in determining the applicationlevel semantics only by simply observing the _malloc_ and _free_ functions intercepted via _LD_PRELOAD_ . For future work in the production version, we will develop a feature to minimize the use of shared memory to only the necessary parts. 

## _B. Limitations on message types handled by Agnocast_ 

While _Agnocast_ is an IPC technology capable of true zerocopy transfer of arbitrary ROS 2 message types, it cannot handle arbitrary objects. Specifically, it cannot handle message types that have a user-assignable pointer type as a property. 

This is because for true zero-copy communication, all message objects must be placed in shared memory. If a message property has an arbitrarily modifiable pointer, application programmers can potentially set an address that points to memory other than shared memory. Since ROS 2 message types do not have properties of user-assignable pointers, they fall within the scope of what _Agnocast_ can handle. 

## VIII. CONCLUSION AND FUTURE WORK 

This paper introduces _Agnocast_ , a new IPC technology that enables true zero-copy IPC with minimum constraints on application code, even when unable to specify memory allocation strategies in application code. _Agnocast_ consists of two key concepts: an idea of directly mapping the heap to shared memory, and a novel smart pointer technology that efficiently manages object lifetimes when objects are accessed across multiple processes. _Agnocast_ can handle any ROS 2 message, including unsized message types, while minimizing code modifications in existing projects. Our evaluation demonstrates both the superior IPC performance of _Agnocast_ compared to existing technologies and its practical utility in a practical autonomous driving system. As the first opensource true zero-copy IPC middleware to fulfill the deployment needs of large-scale, real-world ROS 2 systems, _Agnocast_ represents a significant advancement in ROS 2 communication technologies. Furthermore, its novel approach to IPC extends beyond ROS 2 specific improvements, contributing to the advancement of general IPC technologies. A prototype version of _Agnocast_ is available as open-source<sup>1</sup> . 

As future work, we are developing a production version of _Agnocast_ for real-world ROS 2 projects such as Autoware, supporting various standard ROS 2 features such as ROS 2 clients and servers. We also plan advanced features, including dynamically selecting a virtual address range for shared memory when the intended range is already occupied. 

## IX. ACKNOWLEDGMENT 

This research is based on results obtained from a project, JPNP21027, subsidized by the New Energy and Industrial Technology Development Organization (NEDO). Green Innovation Fund Projects / Development of In-vehicle Computing and Simulation Technology for Energy Saving in Electric Vehicles. 

## REFERENCES 

- [1] (2024) ROS 2 documentation. Open Robotics. Accessed Apr. 16, 2024. [Online]. Available: https://docs.ros.org/en/rolling/ 

- [2] S. Macenski, A. Soragna, M. Carroll, and Z. Ge, “Impact of ros 2 node composition in robotic systems,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 7, pp. 3996–4003, 2023. 

- [3] M. Pöhnl, A. Tamisier, and T. Blass, “A middleware journey from microcontrollers to microprocessors,” in _2022 Design, Automation & Test in Europe Conference & Exhibition (DATE)_ . IEEE, 2022, pp. 282–286. 

- [4] M. Pöhnl, C. Eltzschig, and T. Blass, “Shared-memory-based lock-free queues: The key to fast and robust communication on safety-critical edge devices,” in _Proceedings of Cyber-Physical Systems and Internet of Things Week 2023_ , 2023, pp. 179–184. 

- [5] (2024) Eclipse Cyclone DDS. Eclipse Foundation. Accessed Apr. 16, 2024. [Online]. Available: https://github.com/eclipse-cyclonedds/ cyclonedds 

- [6] S. Kato, E. Takeuchi, Y. Ishiguro, Y. Ninomiya, K. Takeda, and T. Hamada, “An open approach to autonomous vehicles,” _IEEE Micro_ , vol. 35, no. 6, pp. 60–68, 2015. 

- [7] S. Kato, S. Tokunaga, Y. Maruyama, S. Maeda, M. Hirabayashi, Y. Kitsukawa, A. Monrroy, T. Ando, Y. Fujii, and T. Azumi, “Autoware on board: Enabling autonomous vehicles with embedded systems,” in _2018 ACM/IEEE 9th International Conference on Cyber-Physical Systems (ICCPS)_ . IEEE, 2018, pp. 287–296. 

- [8] Y.-P. Wang, W. Tan, X.-Q. Hu, D. Manocha, and S.-M. Hu, “Tzc: Efficient inter-process communication for robotics middleware with partial serialization,” in _2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2019, pp. 7805–7812. 

- [9] C. Iordache, S. M. Fendyke, M. J. Jones, and R. A. Buckley, “Smart pointers and shared memory synchronisation for efficient inter-process communication in ros on an autonomous vehicle,” in _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2021, pp. 6441–6448. 

- [10] (2024) Fast DDS documentation. eProsima. Accessed Apr. 16, 2024. [Online]. Available: https://fast-dds.docs.eprosima.com/en/latest/ 

- [11] (2024) Data distribution service (DDS) standard. RTI. Accessed Apr. 16, 2024. [Online]. Available: https://www.rti.com/products/dds-standard 

- [12] (2024) Zenoh: The zero overhead protocol. Eclipse Foundation. Accessed Apr. 16, 2024. [Online]. Available: https://zenoh.io/ 

- [13] (2024) ROS middleware abstraction interface. Open Robotics. Accessed Apr. 16, 2024. [Online]. Available: https://docs.ros2.org/galactic/api/ rmw/ 

- [14] (2024) Autoware - the world’s leading open-source software project for autonomous driving. Autoware Foundation. Accessed Apr. 16, 2024. [Online]. Available: https://github.com/autowarefoundation/autoware 

- [15] ROS Wiki Contributors. (2023) msg - ROS Wiki. Open Robotics. Accessed Feb. 3, 2025. [Online]. Available: https://wiki.ros.org/msg 

- [16] I. El Hajj, T. B. Jablin, D. Milojicic, and W.-m. Hwu, “Savi objects: sharing and virtuality incorporated,” _Proceedings of the ACM on Programming Languages_ , vol. 1, no. OOPSLA, pp. 1–24, 2017. 

- [17] Y.-P. Wang, X.-Q. Hu, Z.-X. Zou, W. Tan, and G. Tan, “Ivt: an efficient method for sharing subtype polymorphic objects,” _Proceedings of the ACM on Programming Languages_ , vol. 3, no. OOPSLA, pp. 1–22, 2019. 

- [18] (2024) stress-ng - a system load, stress and torture testing tool. Ubuntu. Accessed Apr. 16, 2024. [Online]. Available: https: //wiki.ubuntu.com/Kernel/Reference/stress-ng 

- [19] A. Li and N. Zhang, “Data-flow availability: Achieving timing assurance in autonomous systems,” in _18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24)_ , 2024, pp. 445–463. 

- [20] (2025) Ros 2 bag replay simulation - autoware documentation. Autoware Foundation. Accessed Jan. 27, 2025. [Online]. Available: https://autowarefoundation.github.io/autoware-documentation/ main/tutorials/ad-hoc-simulation/rosbag-replay-simulation/ 

- [21] T. Kuboichi, A. Hasegawa, B. Peng, K. Miura, K. Funaoka, S. Kato, and T. Azumi, “CARET: Chain-aware ROS 2 evaluation tool,” in _2022 IEEE 20th International Conference on Embedded and Ubiquitous Computing (EUC)_ . IEEE, 2022. 

- [22] O. Bell, C. Gill, and X. Zhang, “Hardware acceleration with zerocopy memory management for heterogeneous computing,” in _2023 IEEE 29th International Conference on Embedded and Real-Time Computing Systems and Applications (RTCSA)_ . IEEE, 2023, pp. 28–37. 

- [23] K. Nishimura, T. Ishikawa, H. Sasaki, and S. Kato, “Raplet: Demystifying publish/subscribe latency for ros applications,” in _2021 IEEE 27th International Conference on Embedded and Real-Time Computing Systems and Applications (RTCSA)_ . IEEE, 2021, pp. 41–50. 

- [24] (2024) FlatData API. RTI. Accessed Apr. 16, 2024. [Online]. Available: https://community.rti.com/examples/flatdata-api 

- [25] (2024) FlatBuffers. Google. Accessed Apr. 16, 2024. [Online]. Available: https://flatbuffers.dev 

- [26] Y.-P. Wang, Y. Dong, and G. Tan, “Ros-sf: A transparent and efficient ros middleware using serialization-free message,” in _Proceedings of the 23rd ACM/IFIP International Middleware Conference_ , 2022, pp. 82–93. 

- [27] Z. Jiang, Y. Gong, J. Zhai, Y.-P. Wang, W. Liu, H. Wu, and J. Jin, “Message passing optimization in robot operating system,” _International Journal of Parallel Programming_ , vol. 48, no. 1, pp. 119–136, 2020. 

1https://github.com/sykwer/agnocast. 

