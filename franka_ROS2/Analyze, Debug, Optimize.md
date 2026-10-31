---
title: "Analyze, Debug, Optimize: Real-Time Tracing for Perception and Mapping Systems in ROS 2"
date: "2022-04-25"
authors: "Pierre-Yves Lajoie; Christophe Bédard; Giovanni Beltrame"
url: https://arxiv.org/abs/2204.11778
pdf: https://arxiv.org/pdf/2204.11778
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2204.11778)** / [論文ページ](https://arxiv.org/abs/2204.11778)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Analyze, Debug, Optimize: Real-Time Tracing for Perception and Mapping Systems in ROS 2** 

Pierre-Yves Lajoie, Christophe B´edard, Giovanni Beltrame 

**_Abstract_ — Perception and mapping systems are among the most computationally, memory, and bandwidth intensive software components in robotics. Therefore, analysis, debugging, and optimization are crucial to improve perception systems performance in real-time applications. However, standard approaches often depict a partial picture of the actual performance. Fortunately, instrumentation and tracing offer a great opportunity for detailed performance analysis of realtime systems. In this paper, we show how our novel opensource tracing tools and techniques for ROS 2 enable us to identify delays, bottlenecks and critical paths inside centralized, or distributed, perception and mapping systems.** 

## I. INTRODUCTION 

Perception and mapping are critical for robot autonomy. Thus, real-time performance and reliability are essential to perform robust operations and successfully deploy robots outside controlled environments. Unfortunately, the research community currently lacks efficient diagnosis tools to analyze, debug, and optimize perception and mapping systems. Those systems are complex and usually distributed over multiple processes such as sensors drivers, data preprocessing, state estimation, visualization, etc. A global view of the system, which cannot be obtained through traditional debugging, is often necessary to find failure points, deadlocks, and performance bottlenecks. Researchers and developers are therefore relegated to static code analysis or ad hoc indirect monitoring tools, often with high execution overhead, to troubleshoot and optimize their perception software. Moreover, collaborative and parallel systems, distributed over multiple computers, add another layer of complexity to the debugging and performance analysis problem. 

Software tracing is a practical and effective solution [1]. In particular, the LTTng tracer [2], which has a mostly negligible overhead on performance [1], allows us to create a detailed portrait of the real-time execution of a program. It allows developers to detect bottlenecks and measure latencies, among other metrics. Tracers are an important alternative to classical techniques, such as interactive debugging, when we cannot afford to slow down or pause the execution (e.g., to detect race conditions). Furthermore, interactive debugging is difficult to deploy on multiprocess systems. 

Over the last decade, the _Robot Operating System_ , and its successor ROS 2, have become the most popular software 

This work was supported by Vanier Canada Graduate Scholarships, as well as Ericsson, the Natural Sciences and Engineering Research Council of Canada, and Prompt. 

Department of Computer and Software Engineering, Polytechnique Montr´eal, Montreal, Canada, Corresponding Author: pierre-yves.lajoie@polymtl.ca 

infrastructures for multiprocess management in robotics with their publisher-subscriber messaging scheme [3], [4]. They are the backbone of many robotic applications, and perception systems in particular. 

In this paper, we demonstrate how our novel tracing tools and analyses for ROS 2 [5], [6] can benefit the debugging and performance analysis of perception systems. In particular, we show how important metrics can be extracted from the tracing of a Simultaneous Localization and Mapping (SLAM) system. We also investigate performance and communication issues in a SLAM system distributed over two different computers. Overall, the diagnosis and analysis of ROS 2 execution traces could be important tools for large-scale practical deployments of robotic perception such as during the recent DARPA Subterranean Challenge [7], [8]. Code and documentation of the approach are available online: github.com/christophebedard/ros2-message-flow-analysis. 

## II. BACKGROUND AND RELATED WORK 

## _A. Real-Time Perception_ 

Perception systems, especially those with enhanced capabilities such as semantic understanding, often suffer from performance issues preventing their use in real-time settings. Thus, there is a trade-off between the system capabilities, from localization accuracy to scene understanding, and the available computing resources [9]. Roboticists also have to consider practical aspects such as sensors data management, and USB bandwidth. All those considerations have to be taken into account to achieve real-time performance (e.g., high-speed odometry). Additionally, in distributed systems, one has to consider data serialization, network delays, synchronization, and coordination which can all be measured with execution traces. 

## _B. ROS 2 Tracing_ 

ROS 2, which is a recent framework already used by many perception systems in robotics, is made of multiple layers. First, the client libraries, rclcpp and rclpy, offer C++ and Python APIs for developers. They are based on a common underlying library, rcl, which calls rmw, the middleware interface. The middleware consists of an implementation of the DDS (Data Distribution Service) standard for dependable, high-performance, interoperable, real-time, and scalable data exchanges in publish-subscribe systems. 

The overall performance of ROS 2 is considered superior to its ROS 1 predecessor [10], [11], [12]. To assess this performance, a number of tools have been proposed to evaluate the message transmission latency. For example, 


(b) Message flow analysis of an input image. 

Fig. 1. Visualization of the ROS 2 trace of a SLAM system and the corresponding message flow analysis for an input image. An event timeline is displayed for each ROS 2 topic of each node. Color sections represent callback executions, gray arrows represent links between callbacks and message publication instances, and black arrows show message transfers. This Trace Compass visualization shows the journey of an input image through the SLAM computation pipeline up to the resulting map and pose graph estimate. It enables researchers and engineers to identify delays, bottlenecks, and anomalies. 

[13] proposes a benchmarking tool to measure the latency between publishers and subscriptions directly, while [14] defines a custom message graph topology. To enable deeper analysis, several methods have modeled the exchanges of ROS messages from node to node as event chains and pipelines. They range from online monitoring [15] to formal scheduling to bound worst-case response times [16], [17]. In a similar line of work, [18] proposed an online automatic latency manager for ROS 2. 

To investigate performance issues in a minimally-invasive way, a tracing tool for ROS 1 [19] has been proposed. It is based on LTTng [2], a tracer with low runtime overhead [1]. In previous work, we proposed ros2 ~~t~~ racing [5], a framework with instrumentation and tools for real-time tracing of ROS 2. Our subsequent work [6] extends that instrumentation, and proposes an analysis and visualization of the flow of messages across distributed systems. 

## _C. Trace Analysis_ 

Advanced analysis is required to extract useful pieces of information from tracing data. In particular, critical path 

analysis [20], which searches for the longest execution sequence or pipeline in a distributed system, allows us to compute input-to-output processing time and to identify the bottlenecks. To achieve this, execution traces from multiple computers need to be synchronized [21], [22] and then analyzed as a whole. Inside a ROS system, the execution path takes the form of a message flow in which nodes receiving messages perform some processing, then publish the results to the following nodes, as shown in Fig. 1. Then, users can perform a critical path analysis by comparing chains of messages, or pipelines, and identifying the one which takes the longest time between the initial input (e.g., camera images) and the final desired result of the system (e.g., map of the environment). To extract the chain of messages, the tracing tool needs to associate input subscriptions with output publishers. Those causal links can be specified in the application code using instrumentation as in [5]. In addition to user-defined annotation, [6] offers automatic causal links detection for output messages published directly inside the input subscription callbacks. The resulting message flows can be visualized as graphs using the Trace Compass trace analysis framework [23], as shown in Fig. 1. 

## _D. ROS 2 Tracing for Perception and Mapping_ 

In this paper, we focus on metrics that are important for the performance of perception systems. Tracing can help to identify bottlenecks, as well as race conditions, in perception pipelines. Furthermore, in distributed systems, inter-process and inter-computer communications, including serialization time and network delays, can be measured to analyze the system. Those communication metrics are especially important since ROS 2 offers several Quality of Service (QoS) settings for messages transmission (e.g., reliability, message queue size, etc.). Thus, based on the message flow analysis, one could decide which configuration is best suited for a given system or environment. 

## III. EXPERIMENTS 

In the following experiments, we show how our tracing tools for ROS 2 and our message flow analysis allow us to extract meaningful performance metrics for perception systems. In particular, we test our technique on the ROS 2 RTABMap SLAM system [24]. We also demonstrate our ability to analyze systems distributed across multiple computers. The studied SLAM system is composed of four ROS 2 nodes: the sensor driver (Intel Realsense D455 camera), visual odometry, SLAM (loop closure detection, pose graph optimization, etc.), and map visualization. As shown in Fig. 2, the nodes are linked with message publications and subscriptions, and the raw sensor data is ultimately converted into state and map estimates which can be visualized or used for motion planning and control. The message flow corresponds to this processing of messages through multiple nodes from the inputs to the desired output. 

Causal links between input message subscriptions and output publications are automatically inferred in cases where the processing is done directly in the subscriber callback. In 

more complex cases, the links can be defined by the user using a few lines of code. 


Fig. 2. Sample representation of the flow of messages in a robotic system. Each box represents a ROS 2 node and arrows correspond to messages transmitted from a publisher to a subscriber. The solid lines represent the perception links studied in our experiments. 

Our Trace Compass visualization of the message flow displays a graph in which the message publications are linked to the corresponding subscriber callbacks. Each ROS 2 topic of each node in the system has its associated timeline in which the execution of callbacks is colored, and the idle time is left blank. Transmission of messages from one node to another is represented using arrows from the publication time to the start of the subscription callback. Thus, we can move through time, zoom in and out, to inspect the execution trace, measure performance, and look for anomalies. 

Our approach also includes the ability to select any message and to compute its associated message flow as shown in Fig. 1. Furthermore, the message flow analysis is performed in both directions, i.e., we can select an input to identify the resulting output, or select an output to trace back to the corresponding input. This enables us to find bottlenecks in the processing pipeline. Moreover, singling out messages allows us to diagnose fine-grained issues, such as message drops, or an abnormal processing time. Fig. 1 shows the flow of a camera image message in our SLAM example system. We can see that the critical path goes through the visual odometry node (rgbd ~~o~~ dometry), then the odometry estimate is sent to the SLAM node (rtabmap) which outputs the resulting map and pose graph to the visualization node (rviz). Table I presents a breakdown of the end-to-end processing time from the image publication to the resulting map estimate. 

TABLE I 

TIME BREAKDOWN OF THE MESSAGE FLOW PRESENTED IN FIG. 1. 

|**Message Flow Segment**|**Ti**<br>**(ms)**|**me**<br>**(%)**|
|---|---|---|
|RTAB-Map|191.0|64.3|
|Visual Odometry|81.4|27.4|
|Network Latency + Message Handling|24.7|8.3|
|Visualization|0.3|0.001|
|input-to-output total|297.4|100|


In addition, our approach extends to distributed systems in which multiple traces, synchronized using NTP [25], can be analyzed as a whole. For example, in Fig. 1, the whole 


Fig. 3. Visualization of the message publications and subscription callbacks in a distributed SLAM system. In this example, camera images are transferred from one computer to another. The network congestion and bottleneck result in message drops and high varying transmission delays of up to 500 milliseconds. This illustrates that our proposed approach can be used to analyze delays and communication issues in distributed perception systems. 

SLAM system is located on onboard the robot and the visualization is done from a base station. To investigate the system, and showcase distributed systems analysis, we performed another experiment, shown in Fig. 3, in which the odometry is computed onboard the robot, but the SLAM node is executed on the base station. While costly in terms of communication, similar workload divisions are common since we can afford to compute loop closure detection and pose graph optimization at a slower rate than odometry. Thus, we can offload this expensive process to a more powerful computer or server. Furthermore, offboard computing of SLAM enables collaborative mapping using data from multiple robots simultaneously [26]. As expected, we can see in Fig. 3 that transferring images from the robot to the base station strains the network capacity and introduces delays. Indeed, the overloaded Wi-Fi network results in varying transmission delays, which include network delays and internal ROS 2 message handling, of up to 500 milliseconds. We can also observe that only one image message, in the displayed time frame, leads to significant processing in the SLAM node on the base station. This indicates the loss of critical mapping information as most images messages are not acted upon. Hence, our system analysis approach is able to investigate important problems in distributed perception systems such as networks delays and message drops. 

Besides the message flow, our tracing analysis enables the comparison of message callbacks with the ROS 2 executor threads. As shown in Fig. 4, we can see in the top view the status of each thread during the execution. Active threads are indicated in green and idle threads in orange. The process ID indicates which thread is associated with each ROS 2 node (e.g., ID 540 for rgbd ~~o~~ dometry). Thus, we can extract interesting conclusions for the optimization of the systems. 

In light of these results, we believe that our tracing instrumentation of ROS 2 and our message flow analysis could be important tools for both research and industry. 

## IV. CONCLUSIONS 

In this paper, we presented how novel real-time tracing tools for ROS 2 enable robotic researchers and engineers to analyze, debug, and optimize SLAM systems. This is especially important since perception and mapping are often the most computationally, memory, and bandwidth intensive 


Fig. 4. Visualization of the message publications and subscription callbacks in a distributed SLAM system along with the status of the execution threads (active or idle). The process ID is shown for each ROS 2 node. This combined view allows us to identify computation problems and possible optimizations. 

subsystems in robotics. Our open-source tracing tool can provide detailed metrics such as end-to-end processing time or data transmission latencies. The proposed approach is also compliant with distributed systems since we can simultaneously analyze traces acquired on multiple computers. 

Our work on tracing and analysis tools for perception and mapping systems is still in progress. In the next steps, we plan to develop additional analyses specific for centralized and decentralized SLAM systems including the detection of unused sensor data, and communication bandwidth monitoring. We believe that our analysis technique will help to improve the overall robustness of perception systems, and thus facilitate future deployments of resource-constrained robotic systems. 

## REFERENCES 

- [1] M. Gebai and M. R. Dagenais, “Survey and analysis of kernel and userspace tracers on linux: Design, implementation, and overhead,” _ACM Computing Surveys (CSUR)_ , vol. 51, no. 2, pp. 1–33, 2018. 

- [2] M. Desnoyers and M. R. Dagenais, “The lttng tracer: A low impact performance and behavior monitor for gnu/linux,” in _OLS (Ottawa Linux Symposium)_ , vol. 2006. Citeseer, 2006, pp. 209–224. 

- [3] M. Quigley, K. Conley, B. Gerkey, J. Faust, T. Foote, J. Leibs, R. Wheeler, and A. Y. Ng, “Ros: an open-source robot operating system,” in _ICRA workshop on open source software_ , vol. 3, no. 3.2. Kobe, Japan, 2009, p. 5. 

- [4] D. Thomas, W. Woodall, and E. Fernandez, “Next-generation ROS: Building on DDS,” in _ROSCon Chicago 2014_ . Mountain View, CA: Open Robotics, sep 2014. [Online]. Available: https: //vimeo.com/106992622 

- [5] C. B´edard, I. L¨utkebohle, and M. Dagenais, “ros2 ~~t~~ racing: Multipurpose low-overhead framework for real-time tracing of ros 2,” _IEEE Robotics and Automation Letters_ , 2022. 

- [6] C. B´edard, P.-Y. Lajoie, G. Beltrame, and M. Dagenais, “Message flow analysis with complex causal links for distributed ros 2 systems,” _arXiv preprint arXiv:2204.10208_ , 2022. 

- [7] DARPA. DARPA subterranean challenge. [Online]. Available: https: //www.subtchallenge.com/ 

- [8] M. F. Ginting, K. Otsu, J. A. Edlund, J. Gao, and A.-A. Agha-Mohammadi, “CHORD: Distributed data-sharing via hybrid ROS 1 and 2 for multi-robot exploration of large-scale complex environments,” vol. 6, no. 3, pp. 5064–5071. [Online]. Available: https://ieeexplore.ieee.org/document/9364680/ 

- [9] C. Cadena, L. Carlone, H. Carrillo, Y. Latif, D. Scaramuzza, J. Neira, I. Reid, and J. J. Leonard, “Past, present, and future of simultaneous localization and mapping: Toward the robust-perception age,” vol. 32, no. 6, pp. 1309–1332. 

- [10] Y. Maruyama, S. Kato, and T. Azumi, “Exploring the performance of ros2,” in _Proceedings of the 13th International Conference on Embedded Software_ , 2016, pp. 1–10. 

- [11] C. S. V. Guti´errez, L. U. S. Juan, I. Z. Ugarte, and V. M. Vilches, “Towards a distributed and real-time framework for robots: Evaluation of ros 2.0 communications for real-time robotic applications,” _arXiv preprint arXiv:1809.02595_ , 2018. 

- [12] L. Puck, P. Keller, T. Schnell, C. Plasberg, A. Tanev, G. Heppner, A. R¨onnau, and R. Dillmann, “Distributed and synchronized setup towards real-time robotic control using ros2 on linux,” in _2020 IEEE 16th International Conference on Automation Science and Engineering (CASE)_ . IEEE, 2020, pp. 1287–1293. 

- [13] Apex.AI, “performance ~~t~~ est.” [Online]. Available: https://gitlab.com/ ApexAI/performance ~~t~~ est 

- [14] iRobot, “irobot ros 2 performance evaluation framework.” [Online]. Available: https://github.com/irobot-ros/ros2-performance 

- [15] J. Peeck, J. Schlatow, and R. Ernst, “Online latency monitoring of time-sensitive event chains in safety-critical applications,” in _2021 Design, Automation & Test in Europe Conference & Exhibition (DATE)_ . IEEE, 2021, pp. 539–542. 

- [16] D. Casini, T. Blaß, I. L¨utkebohle, and B. B. Brandenburg, “Responsetime analysis of ros 2 processing chains under reservation-based scheduling,” in _31st Euromicro Conference on Real-Time Systems (ECRTS 2019)_ . Schloss Dagstuhl-Leibniz-Zentrum fuer Informatik, 2019. 

- [17] Y. Tang, Z. Feng, N. Guan, X. Jiang, M. Lv, Q. Deng, and W. Yi, “Response time analysis and priority assignment of processing chains on ros2 executors,” in _2020 IEEE Real-Time Systems Symposium (RTSS)_ . IEEE, 2020, pp. 231–243. 

- [18] T. Blass, A. Hamann, R. Lange, D. Ziegenbein, and B. B. Brandenburg, “Automatic latency management for ros 2: Benefits, challenges, and open problems,” in _2021 IEEE 27th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ . IEEE, 2021, pp. 264–277. 

- [19] Bosch Corporate Research, “Ros 1 tracetools.” [Online]. Available: https://github.com/boschresearch/ros1 ~~t~~ racetools 

- [20] C.-Q. Yang and B. P. Miller, “Critical path analysis for the execution of parallel and distributed programs,” in _The 8th International Conference on Distributed_ . IEEE Computer Society, 1988, pp. 366–367. 

- [21] B. Poirier, R. Roy, and M. Dagenais, “Accurate offline synchronization of distributed traces using kernel-level events,” _ACM SIGOPS Operating Systems Review_ , vol. 44, no. 3, pp. 75–87, 2010. 

- [22] M. Jabbarifar and M. Dagenais, “Liana: Live incremental time synchronization of traces for distributed systems analysis,” _Journal of network and computer applications_ , vol. 45, pp. 203–214, 2014. 

- [23] “Eclipse trace compass.” [Online]. Available: https://www.eclipse.org/ tracecompass/ 

- [24] M. Labb´e and F. Michaud, “Rtab-map as an open-source lidar and visual simultaneous localization and mapping library for large-scale and long-term online operation,” _Journal of Field Robotics_ , vol. 36, no. 2, pp. 416–446, 2019. [Online]. Available: https://onlinelibrary.wiley.com/doi/abs/10.1002/rob.21831 

- [25] D. Mills, “Internet time synchronization: the network time protocol,” _IEEE Transactions on Communications_ , vol. 39, no. 10, pp. 1482– 1493, 1991. 

- [26] P.-Y. Lajoie, B. Ramtoula, F. Wu, and G. Beltrame, “Towards collaborative simultaneous localization and mapping: a survey of the current research landscape.” [Online]. Available: http: //arxiv.org/abs/2108.08325 

