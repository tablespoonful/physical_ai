---
title: "AUTOSAR AP and ROS 2 Collaboration Framework"
date: "2025-11-07"
authors: "Ryudai Iwakami; Bo Peng; Hiroyuki Hanyu; Tasuku Ishigooka; Takuya Azumi"
url: https://arxiv.org/abs/2511.17540
pdf: https://arxiv.org/pdf/2511.17540
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.17540)** / [論文ページ](https://arxiv.org/abs/2511.17540)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# AUTOSAR AP and ROS 2 Collaboration Framework 

Ryudai Iwakami Bo Peng Hiroyuki Hanyu and Tasuku Ishigooka Takuya Azumi Graduate School of EMB IV Technology Development Functional Division Graduate School of Science and Engineering Hitachi Astemo, Ltd. Science and Engineering Saitama University Saitama University 

Abstract—The field of autonomous vehicle research is advancing rapidly, necessitating platforms that meet real-time performance, safety, and security requirements for practical deployment. AUTOSAR Adaptive Platform (AUTOSAR AP) is widely adopted in development to meet these criteria; however, licensing constraints and tool implementation challenges limit its use in research. Conversely, Robot Operating System 2 (ROS 2) is predominantly used in research within the autonomous driving domain, leading to a disparity between research and development platforms that hinders swift commercialization. This paper proposes a collaboration framework that enables AUTOSAR AP and ROS 2 to communicate with each other using a Data Distribution Service for Real-Time Systems (DDS). In contrast, AUTOSAR AP uses Scalable service-Oriented Middleware over IP (SOME/IP) for communication. The proposed framework bridges these protocol differences, ensuring seamless interaction between the two platforms. We validate the functionality and performance of our bridge converter through empirical analysis, demonstrating its efficiency in conversion time and ease of integration with ROS 2 tools. Furthermore, the availability of the proposed collaboration framework is improved by automatically generating a configuration file for the proposed bridge converter. 

Index Terms—ROS 2, AUTOSAR AP, DDS, SOME/IP, autonomous vehicle. 

## I. INTRODUCTION 

Autonomous driving technology [1] has rapidly advanced, drawing worldwide attention and spurring significant research and development efforts. This surge in activity has brought autonomous vehicles closer to widespread practical use for transporting both people and goods. As these vehicles approach commercial readiness, consumer expectations and the landscape of automotive development are evolving. Research in this domain is dynamic, propelled by technological advancements and market demand. Autonomous driving systems must process data from numerous sensors and cameras in real time, necessitating high technical competence. These systems require not only real-time processing capabilities but also flexibility, safety, and security to be viable in practical scenarios. 

AUTOSAR Adaptive Platform (AUTOSAR AP) [2], [3] is the chosen platform for addressing the requirements of automotive embedded systems, offering a software architecture that ensures compatibility and extensibility across various vendors and applications. Its adoption promotes a standardized approach, revolutionizing automotive development. Internet of Vehicles (IoV) strategy enhances this by enabling cloud-based 

development, testing on actual devices, and iterative feedbackdriven enhancements. Additionally, AUTOSAR AP supports Software-Defined Vehicles (SDV) concept, which allows for post-purchase software updates to add new functionalities and value, contrasting with traditional vehicles’ static features. The framework for integrating these ideas and accelerating the development of software-defined vehicles is called SOAFEE [4], [5]. Following the SOAFEE trend, AUTOSAR AP has become an important element in the development of autonomous vehicles. 

AUTOSAR AP is gaining traction as the norm for developing actual autonomous vehicles. However, its recent establishment means that many current studies opt for alternative platforms, resulting in limited research utilizing AUTOSAR AP. Another reason for the lack of research using AUTOSAR AP is that the use of AUTOSAR AP requires an expensive license. Another, SOME/IP that is a communication protocol used only for in-vehicle networks, is used as a standard. Given the trend of SOAFEE, it is expected that AUTOSAR AP and other platforms will be developed in a mixed manner, requiring collaboration and communication with other platforms. Therefore, support for other communication protocols is desired. A few existing studies have attempted to communicate between SOME/IP and other communication protocols. 

This paper proposes an AUTOSAR AP and ROS 2 collaboration framework that enables communication between SOME/IP and Data Distribution Service for Real-Time Systems (DDS) [6]. ROS 2 [7] employs DDS for communication between nodes, the smallest execution units, and uses the same publish/subscribe model as SOME/IP. ROS 2 is also characterized by its open-source nature, which means that a wealth of documentation, evaluation, and visualization tools are available; this abundance of tools is another reason why ROS 2 is actively used in research. The bridge converter proposed in this paper enables the integration between AUTOSAR AP and ROS 2, which makes it possible to develop AUTOSAR AP using the comprehensive ROS 2 tools. ROS 2 platform can also be used more effectively as a standard platform for actual vehicle development. This synergy aids the rapid transition of ROS 2 research findings into the commercial development of autonomous vehicles. Furthermore, it contributes to the realization of SOAFEE, which is expected to be developed with a mixture of AUTOSAR AP and ROS 2, and facilitates the development of autonomous vehicles. 

© 2024 IEEE. Personal use of this material is permitted. DOI: 10.1109/DSD64264.2024.00050 


Fig. 1. The rough architecture proposed in this study. 

The primary contributions of this paper are summarized as follows: 

- Facilitating AUTOSAR AP and ROS 2 collaboration: The proposed bridge converter performs DDS and SOME/IP conversion between AUTOSAR AP and ROS 2, allowing communication between the two platforms. 

- Enabling SOME/IP data visualization: The proposed bridge converter enables the use of ROS 2’s rich evaluation and visualization tools for AUTOSAR AP applications. 

- Supporting diverse custom messages: By entering the necessary ID and name details for SOME/IP communication, our system auto-generates the configuration file, simplifying the use of our bridge converter. 

The remainder of this paper is organized as follows. Section II describes the characteristics of AUTOSAR AP and ROS 2, which are the prerequisites for this study. Section III describes the proposed communication method. Section IV describes the evaluation of the proposed communication method, and Section V describes related work. Finally, a brief conclusion is given. 

## II. SYSTEM MODEL 

This section presents an overview of the proposed method and explains AUTOSAR AP and ROS 2, which are considered in the proposed method. An overview of the proposed method is summarized in Fig. 1. The proposed method implements a bridge that converts the communication method between the ROS 2 node and the AUTOSAR AP application for communication between each component. This bridge resolves the differences between DDS and SOME/IP and converts the communication between the two.The following is a prerequisite knowledge of the proposed method. 

Firstly, the structure and features of another platform, AUTOSAR AP, are described. Secondly, the structure of ROS 2 and an overview of the communication schemes implemented are described. Thirdly, SOME/IP, the communication protocol mainly used in AUTOSAR AP, is explained. Fourthly, DDS used in ROS 2 is explained. Finally, vsomeip and CommonAPI used in this implementation are described. 


Fig. 2. Communication between AUTOSAR AP applications. 


Fig. 3. Communication between ROS 2 nodes. 

A. AUTomotive Open System ARchitecture Adaptive Platform (AUTOSAR AP) 

AUTOSAR AP [8] is a software architecture for nextgeneration automotive embedded systems. Compared to ROS 2 with DDS, AUTOSAR AP uses SOME/IP as its main communication protocol. Besides, while ROS 2 is open-source, AUTOSAR AP requires a license for use and is not freely available. Therefore, AUTOSAR AP is not as richly documented as ROS 2 and has few existing results. Another feature is the difficulty of handling due to excessive standardization. 

Similar to the design of ROS 2 [8], the architecture of AUTOSAR AP can be classified into three layers: the application layer, the middleware layer, and the OS layer. The application layer includes the application and Non-Platform (Non-PF) Service, where services specific to a particular application or system are defined by the user. The middleware layer provides the basic functionalities and services of AUTOSAR AP and is called AUTOSAR Runtime for Adaptive Application (ARA). POSIX-based OSs can be used as the OS layer. For example, multiple operating systems such as Linux, QNX, and INTEGRITY can be used. 

The communication flow of an AUTOSAR AP is shown in Fig. 2. AUTOSAR AP uses a Service-Oriented Architecture (SOA), and the nodes in ROS 2 are called applications. Applications are provided as services, and communication with other applications and components is done as service requests. SOME/IP is a protocol that supports service-oriented communication, enabling dynamic service discovery and service requests. Next, another platform, ROS 2, is described in comparison with AUTOSAR AP. 

## B. Robot Operating System 2 (ROS 2) 

ROS 2 [8], an open-source middleware, finds use in autonomous driving software. This platform represents an improved version of ROS and frequently appears in industrial 


Fig. 5. Publish/Subscribe model. 

Fig. 4. Comparison of DDS and SOME/IP send/receive sequences. 

Fig. 4 because the nuance of Publish/Subscribe in SOME/IP is slightly different from that in ROS 2. In addition, “cbk” is an abbreviation for “callback.” The difference from the DDS described in the next section is that the application side recognizes the matching part by checking the existence of the receiver. The following section describes DDS used in ROS 2. 

applications due to its ability to meet the strict real-time constraints inherent to such settings. In contrast to ROS, ROS 2’s most notable feature is the incorporation of DDS for real-time processing. With ROS 2’s open-source nature and broad application across industries, researchers have access to a plethora of tools for efficient study. 

## D. Data Distribution Service for Real-Time Systems (DDS) 

The architecture of applications based on ROS 2 comprises three layers: the application layer, the middleware layer, and the OS layer. The application layer has user code and ROS 2 nodes. Internal processing of each ROS 2 node occurs in the middleware layer, with DDS handling communication between nodes. This architecture supports multiple operating systems, including Linux, Windows, macOS, and real-time OSs. 

DDS [7], [9] is a middleware protocol for real-time distributed systems, especially fitting for large and demanding systems. The main feature of DDS is that it employs a data-centric communication model, which is called the Publish/Subscribe model. The flow of the Publish/Subscribe model is shown in Fig. 5. In the publish/subscribe model, data is exchanged via a data bus called a topic. Sending a topic is called publishing, and receiving a topic is called subscribing. When a topic is published, the publisher node can communicate without specifying a subscriber node, and information is exchanged dynamically via topics. In other words, the middleware manages the matching so that a sending node can publish information to a topic regardless of whether or not a receiving node is present. The lower part of Fig. 4 shows the flow of sending and receiving DDS. The topic type is statically described in the node’s internal source code. When a publisher node is invoked, a topic of the type based on the node’s description is published. The published data is managed by the DDS middleware, and when the appropriate subscriber node is invoked, the topic is subscribed, and data reception is complete. The difference with SOME/IP is that a node is not aware of its communication partners. 

The communication flow of ROS 2 is shown in Fig. 3. ROS 2 creates nodes as units of communication, and each node exchanges information with each other using a data bus (hereafter referred to as “topic”). DDS is discussed in detail in Section II-D below. 

## C. Scalable service-Oriented MiddlewarE over IP (SOME/IP) 

SOME/IP [9] is a communication protocol specialized for automotive networks among real-time distributed systems and enables service-oriented communication over Ethernet. SOME/IP incorporates SOME/IP Service Discovery (SOME/IP-SD), which can dynamically discover and register services on the network. SOME/IP-SD uses service-specific identifiers to discover and register services. ServiceID and InstanceID are used as identifiers. ServiceID is an identifier to identify a specific service uniquely. InstanceID is an identifier to identify different instances of the same service when there are multiple instances of the same service. 

## III. DESIGN AND IMPLEMENTATION 

This section introduces the DDS-SOME/IP conversion tool implemented in this study. First, the structure of the tool, as shown in Fig. 1, is described. Then, specific implementation techniques are described. 

The flow of SOME/IP-SD is shown in the upper part of Fig. 4. First, the sending application sends an Offer message, and the receiving application sends a Find message. Next, when the offered function matches the function being searched for, the receiver sends a subscribe message and data is exchanged. SOME/IP messages are divided into a header part and a payload part. The payload part contains the data to be sent and received. The header part of a SOME/IP message contains SOME/IP’s unique identifiers, such as ServiceID and InstanceID, and the information in the header part is used to match the functionality of the message. “Subscribe request” in 

## A. Structure of DDS-SOME/IP Bridge Converter 

This study implemented a bridge facilitating communication between AUTOSAR AP applications and ROS 2 nodes by performing DDS and SOME/IP conversion, as illustrated in Fig. 6. The two main functionalities of the bridge are: 

- Support for SOME/IP-SD: Since SOME/IP has a service discovery functionality that DDS does not have, 


Fig. 6. Two cases of the bridge as ROS 2 node. 

the bridge performs SOME/IP-SD process to establish communication. 

- Type conversion: Since AUTOSAR AP and ROS 2 use different types for data exchange, the bridge performs conversion to a mutually recognized type. 

The data exchange between a ROS 2 node and an AUTOSAR AP application can be divided into two cases according to the direction of data flow, as shown in Fig. 6. The upper side represents the case where ROS 2 node is the sender and the AUTOSAR AP application is the receiver. The lower side represents the case where the AUTOSAR AP application is the sender and ROS 2 node is the receiver. The bridge converter implemented in this study was implemented as a “node” on the ROS 2 side in both cases. By implementing a bridge converter as a “node” on the ROS 2 side, ROS 2 tools such as Rviz [10] and ROSbag [11] can be easily used. This method is easier to achieve the goal of this study, which is to link AUTOSAR AP and ROS 2, than other methods. 

In this study, the bridge was implemented as a “node” on the ROS 2 side, yet alternative methods exist for linking AUTOSAR AP and ROS 2. One of the methods is to implement a component with bridge functionality as an “application” on the AUTOSAR AP side. However, as mentioned in Section 2.B, AUTOSAR AP requires a license, so there are fewer existing achievements compared to ROS 2. Implementing the bridge converter on the AUTOSAR AP side would be less scalable than implementing the bridge converter on the ROS 2 side. On the other hand, ROS 2 is open source and has many tools and libraries. Therefore, implementing the bridge converter as a “node” rather than as an “application” is considered to increase the scalability of the bridge converter. Another possible approach is to make AUTOSAR AP compatible with DDS. The AUTOSAR AP specification document describes support for DDS. However, most of the descriptions of DDS are drafts and only partially supported in practice [12]. With only a partial specification, to make AUTOSAR AP compatible with DDS will be a future technical debt. For this reason, this method was not selected for this study. With the above background, this study implemented a component with bridge functionality as a “node” on the ROS 2 side. 

### TABLE I 


B. Implementation Method of the Proposed Bridge Converter 

To implement the proposed bridge converter, CommonAPI [13] and vsomeip [13], [14] were used. CommonAPI supports development as an AUTOSAR standard and provides a high-level API to facilitate application development for automotive systems. Its compliance with the AUTOSAR standard and its open-source nature were the reasons for its adoption in the implementation of this study. vsomeip is also one of the open-source implementations of SOME/IP protocol used in the automotive industry to facilitate communication between different devices in a vehicle. 

Since the implementation adheres to the industry-standard SOME/IP protocol, this approach offers superior compatibility and standardization. The open-source nature of the protocol influenced its selection for use in this study’s implementation. CommonAPI uses FIDL (Franca Interface Definition Language) files and FDEPL (Franca Deployment) files to define the service interface, which describe the methods provided by the service, events to be sent, and attributes to be exposed. They also describe information about type conversion. The schematic of the bridge converter implementation is shown in Fig. 7. The yellow components represent vsomeip functions, and the red arrows represent data flow. As shown in Fig 6, the proposed bridge converter can be divided into two patterns. First, when ROS 2 is the sender, the RegisterService function performs SOME/IP-SD based on the information in the FIDL file. When a sender is found, it subscribes to the data from the predecessor node and performs type conversion. Finally, the data is sent as a SOME/IP message using the FireDataEvent function. Next, if ROS 2 is the receiver, the BuildProxy 


Fig. 8. Evaluation program structure. 

function performs SOME/IP-SD based on the information in the FIDL file. When a receiver is found, it receives the data using the GetDataEvent function and performs type conversion. Finally, the data is published to the successor node. 

## C. FIDL Automatic Generator 

SOME/IP requires the matching of information, such as ServiceID, between the server and client sides. The specifications are all described in ARXML files, and the settings of identification information such as ServiceID are also described in ARXML files. In contrast, the proposed bridge converter using CommonAPI uses FIDL and JSON files to set the identification information. Since the identification information for both files needs to be aligned, the FIDL and JSON files need to be re-generated each time the AUTOSAR AP application changes. Therefore, the collaboration framework proposed in this study implements the FIDL Automatic Generator, which can automatically generate FIDL files. 

The FIDL Automatic Generator is a GUI-based program using Python. The FIDL file and FDEPL file that can be used with the bridge converter can be generated automatically by entering the items shown in Table I. The FIDL Automatic Generator can automatically generate tens of lines of FIDL and FDEPL files with only a few lines of input, facilitating the use of the proposed bridge converter. In addition, by loading msg files that define custom messages, a FIDL file describing the conversion specifications can be automatically generated. For example, when dealing with sensor msgs::msg::PointCloud2 type messages, the file generated for the conversion is 78 lines long. Using the proposed tool, a configuration file can be generated automatically with only a few entries. 

## IV. EVALUATION 

This section summarizes the delay evaluation of the DDSSOME/IP conversion bridge converter implemented in this study by message size. In addition, the evaluation using Rviz as a ROS 2 evaluation tool and the extension of the development method using the bridge converter is presented. First, the environment used for the evaluation is described. 

## A. Evaluation Environment 

First of all, the environment used to evaluate the latency of the DDS-SOME/IP bridge converter by message size is 

Fig. 9. Architecture of communication between AUTOSAR AP and ROS 2 in this paper. 

TABLE II ENVIRONMENT ON PC1 

|Hardware|Processor|Intel®Core i9-12900HX CPU@2.3 GHz|
|---|---|---|
|OS|Memory<br>Ubuntu|32 GB<br>22.04.3|
|Middleware|ROS 2|Humble Hawksbill|
|Communication Protocol|DDS|Fast DDS|
||SOME/IP|vsomeip 3.4.9.1 [15]|


shown in Fig. 9. In this evaluation, PC1 shown in Table II and PC2 shown in Table III were used to execute the evaluation program shown in Fig. 8 to evaluate latency. Since the default in ROS 2 humble is FastDDS, FastDDS is used in the evaluation in this study. For CycloneDDS, we confirmed that the proposed bridge converter works. In addition, in the latency evaluation of the communication with AUTOSAR AP applications, as shown in Fig. 9, PC1 and Table IV were used via the proposed bridge converter. The latency was evaluated by communicating with applications in the AUTOSAR AP environment as shown in Fig. 8, through the proposed bridge converter. QNX and AUTOSAR AP were built on QEMU, and a sending application and a receiving application were created as AUTOSAR AP applications. In the evaluation of this paper, ROS 2 is used on an actual device, but AUTOSAR AP is used on QEMU. This is because, although AUTOSAR AP is guaranteed to work on POSIX OS, it is not guaranteed to work on general development environments (e.g., Linux, Windows). Therefore, in the function development stage, it is common to use an environment such as QEMU. 

## B. Latency Evaluation of DDS-SOME/IP Conversion Tool 

This section describes the latency evaluation results of the proposed bridge converter. The structure of the evaluation program and the six checkpoints are shown in Fig. 8. The details of the checkpoints are summarized in Table V. Section IV-B1 provides an overview of the simple program used for the evaluation, in which both SOME/IP and DDS are used. The delay evaluation of the proposed bridge converter is based on two possible use cases: in Section IV-B2, the measurements are based on the case where the sender is a ROS 2 node and the receiver is an AUTOSAR AP application, as shown in the upper part of Fig. 6. Section IV-B3 is based on the case where the sender is an AUTOSAR AP application, and the receiver is a ROS 2 node, as shown in the lower part of Fig. 6. 


1) Program Overview for Evaluation: The point cloud data of sensor msgs::msg::PointCloud2 type was used for the evaluation, and measurements were performed on seven different data sizes with different numbers of point clouds. ROS 2 node A generates sensor msgs::msg::PointCloud2 type data and sends the data to bridge converter node B via DDS. The bridge converter node at C receives the data, converts the data to sensor msgs::msg::PointCloud2 type based on the description in the FIDL file, and sends the data to the ROS 2 node at D through DDS. Finally, the ROS 2 node in D receives and displays the data. The above program was executed in the environment shown in Tables II and III. 

2) Latency to Convert and Send PointCloud2 Type Data from DDS to SOME/IP: The measurements in this section are based on the case shown in the upper part of Fig. 6, where the sender is a ROS 2 node, and the receiver is an AUTOSAR AP application. This case requires conversion from DDS to SOME/IP. Therefore, the evaluation in this section uses the time from ⃝1 to ⃝2 in Fig. 8. The latency was measured for each number of point clouds and is summarized in the box-and-whisker diagram on the left side of Fig. 10. The results show that the latency increases as the data size increases. However, the latency is kept below 100 µs for all data sizes, indicating that the latency caused by the conversion from DDS to SOME/IP is small. 

Using this measurement result and the time taken from ⃝2 to ⃝3 in Fig. 8, we can calculate ⃝1 to ⃝3 was used to calculate the ratio of the execution time of the ⃝1 to ⃝2 part. The result of calculating the percentage of execution time is shown in the box-and-whisker diagram on the left side of Fig. 11. Most of the values are within 1% or less, indicating that the time spent for conversion is a small latency compared to the communication latency. Furthermore, the ratio does not vary significantly with data size, suggesting that it increases at the same rate as the communication latency. 

3) Latency to Convert and Receive PointCloud2 Type Data from SOME/IP to DDS: The measurements in this section are based on the case shown in the lower part of Fig. 6, where the sender is an AUTOSAR AP application, and the receiver is a 


ROS 2 node. This case requires conversion from SOME/IP to DDS. Therefore, the evaluation in this section uses the time from ⃝3 to ⃝4 in Fig. 8. The latency was measured for each number of point clouds and is summarized in the box-andwhisker diagram on the right side of Fig. 10. The results show that the latency increases as the data size increases, similar to the latency for the conversion from DDS to SOME/IP. The latency of the conversion from SOME/IP to DDS is small. 

Using these measurements and the time taken from ⃝2 to ⃝3 in Fig. 8, the proportions of the conversion time to the communication time were calculated. The box-and-whisker diagram on the left side of Fig. 11 shows the result of calculating the ratio of the execution time of parts ⃝2 to ⃝4 to the time taken from ⃝3 to ⃝4 . A similar trend to Section IV-B2 is observed, and most of the values are within 1% or less, indicating that the time spent for conversion is a small latency compared to the latency for communication. Furthermore, this ratio does not vary significantly with data size, suggesting that it increases at the same rate as the communication latency. C. Latency Evaluation in Communication with AUTOSAR AP Application 

For the AUTOSAR AP application, the proposed bridge converter was used to convert DDS to SOME/IP, and 10 types of String type data were sent with different sizes, and the latency was measured. The results are summarized in Fig. 12. It can be seen that the measured latency is higher than expected despite the small data size, and that the latency does not increase as the data size increases. Furthermore, considering the results of Section IV-B2, it is considered that the communication bottleneck is not the bridge converter but other parts such as QEMU. 

D. Improved Usability of AUTOSAR AP with ROS 2 Tools 

ROS 2 has a wealth of development support tools, such as Rviz [10]. AUTOSAR AP does not have such a convenient 


Fig. 12. Latency of sending String type data to AUTOSAR AP applications. 

tool, and the debugger must use Wireshark and other tools to investigate the cause steadily. As a result, the efficiency of the research will be reduced compared to ROS 2. The proposed bridge converter makes it possible to use the following ROS 2 development support tools even in an environment using SOME/IP communication, such as AUTOSAR AP. 

1) Visualization of Communication Using Rviz: As shown in the upper left corner of Fig. 1, the proposed method enables Rviz to be used with AUTOSAR AP applications as well, which contributes to more efficient research and development by visualizing topics and facilitating understanding of the data being exchanged. In this study, we have made it possible to use Rviz to visualize data sent from AUTOSAR AP applications via the bridge converter. Furthermore, in communication with Autoware (Autonomous driving software), data can be visualized through Rviz. Autoware [1] is ROS 2-based autonomous driving software widely used in the autonomous driving field. The proposed framework enables communication with ROS 2- based software such as Autoware. 

2) Easier Debugging with ROSbag: As well as Rviz, the proposed method makes ROSbags available to AUTOSAR AP applications, allowing topics to be saved and replayed, making it easier to reproduce the same situation. As a result, debugging is much more efficient, contributing to more efficient research and development. As shown in Fig. 1, this paper uses ROSbag to store data to be sent to an AUTOSAR AP application, and the same data can be sent repeatedly without effort via a bridge converter. As a result, it contributes to the improvement of debugging efficiency in AUTOSAR AP. E. Ease of Setting up SOME/IP Conversions 

AUTOSAR AP uses many IDs, such as ServiceID and InstanceID, which need to be set in the bridge converter. 

TABLE VI 

NUMBER OF AUTO OUTPUT LINES AND MANUAL INPUT ITEMS 

|Message type|Manual inputs|a|b|Total|
|---|---|---|---|---|
|Point.msg|14|51|20|71|
|NavSatFix.msg|14|51|24|75|
|PointCloud2.msg|14|51|27|78|
|TFMessage.msg|14|51|34|85|
|Waypoint.msg|14|51|89|140|


a: Number of generated lines does not vary by message type 

b: Number of generated lines that vary by message type 

Just by entering the IDs, a configuration file is automatically generated. By using the proposed FIDL maker, users can easily create a configuration file and use the bridge converter. Table VI summarizes the number of lines in the four configuration files and the number of fields to be entered by the user when applied to custom messages in ROS 2 or Autoware and used with the bridge converter. 

## V. RELATED WORK 

Much work have been conducted on AUTOSAR AP and ROS 2, SOME/IP, and DDS, and other communication protocols. This section presents work related to AUTOSAR AP and ROS 2, SOME/IP and DDS, which are strongly related to this study. The results of the comparisons are shown in Table VII. 

While the use of SOA is commonplace in autonomous vehicle research in terms of interoperability and scalability, the study by Mehmet et al. [16] introduces a dynamic serviceoriented software architecture that provides flexibility in the development of autonomous vehicles. The study by Alexandru et al. [17] adds Quality-of-Service (QoS) requirements to SOME/IP for SOA implementation and proposes a framework more suitable for autonomous vehicles. Furthermore, the study by Marc et al. [5] proposes a resilient architecture with dynamic orchestrators to cope with and manage the steadily increasing amount of software installed in the vehicle. 

AUTOSAR AP is being standardized for scenarios such as highly autonomous vehicles and Car-2-X, according to Simon et al. [18], with the goal of smoothly connecting nonAUTOSAR systems while maintaining essential features for autonomous driving systems such as safety, determinism, and real-time functionality. The study by Jacqueline et al. [8] presents an overall picture of AUTOSAR AP and ROS 2 and compares the two in terms of how well ROS 2 satisfies the functionalities provided by AUTOSAR AP. Additionally, the study assesses how appropriate ROS 2 is for autonomous vehicles. The study shows that ROS 2 fully satisfies some of the features of AUTOSAR AP, but not all of them. 

AUTOSAR Adaptive Platform (AP) is currently under standardization to enable the integration of non-AUTOSAR systems. As part of this effort, AUTOSAR AP provides support for various communication protocols beyond SOME/IP, including DDS and Open Platform Communications Unified Architecture (OPC UA). However, this support is not yet comprehensive. The standard also supports protocols other than SOME/IP, such as DDS and Open Platform Communications Unified Architecture (OPC UA). The study by Anna et al. [3] 

TABLE VII 

RELATED WORK AND RELEVANT FIELDS 

||ROS 2|AUTOSAR AP|DDS|SOME/IP|SOA|
|---|---|---|---|---|---|
|SOA for autonomous vehicles [16], [17]||||✓|✓|
|SOA using dynamic orchestration [5]|✓||||✓|
|Beginning of AUTOSAR AP [18]||✓||||
|Comparison of AUTOSAR AP and ROS 2 [8]|✓|✓|||✓|
|Use OPC UA on AUTOSAR AP [3]||✓||||
|Gateway for DDS and OPC UA [19]|||✓|||
|Gateway for SOME/IP and OPC UA [20]||||✓||
|Gateway for DDS, SOME/IP and e-CAL [9]||✓|✓|✓||
|Bridge between ROS 2 and Adaptive-AUTOSAR [21]||✓|△|✓|△|
|This paper|✓|✓|✓|✓|✓|


proposes a new concept of communication via Time-Sensitive Networking (TSN) using OPC UA in AUTOSAR AP. The study by Alexandru et al. [19] compares DDS and OPC UA and proposes a gateway that enables communication between the two protocols. The study by Alexandru et al. [20] also compares SOME/IP and OPC UA similarly and proposes a gateway that enables communication between the two protocols. Note that this study is implemented using VSOMEIP. 

The study by Alexandru et al. [9] focused on SOME/IP, DDS, and eCAL, comparing their advantages, disadvantages, and compatibility. They implemented a multi-protocol gateway that allows communication between the three different protocols. This multi-protocol gateway focuses mainly on communication between AUTOSAR Classic and AUTOSAR AP. This study concentrates on DDS and SOME/IP communication, with a distinct emphasis on facilitating communication between two diverse platforms, AUTOSAR AP and ROS 2 Adaptive Platform (AP). Research on AUTOSAR AP is still scarce but gradually increasing, and the work of Dongwon et al. [21] focuses on ROS 2 and AUTOSAR AP as well as this study. The communication between ROS 2 and AdaptiveAUTOSAR [22], an open source platform that partially meets the AUTOSAR standard, is verified. However, AdaptiveAUTOSAR is not software used in the actual automotive industry and its SOME/IP implementation differs from the AUTOSAR standard. Therefore, the triangles are marked in Table VII. This study uses the software used in the actual automotive industry, and SOME/IP is also compliant with the AUTOSAR AP standard. 

## VI. CONCLUSION 

This paper proposed a DDS and SOME/IP collaboration framework. The proposed collaboration framework bridges the gap between DDS and SOME/IP and enables communication AUTOSAR AP and ROS 2. The result is a mix of AUTOSAR AP and ROS2 in the development of autonomous vehicles. The proposed bridge converter is implemented using CommonAPI and vsomeip. The bridge converter is implemented as a node of ROS 2, and type conversion and SOME/IP-SD functionalities are added to enable conversion between DDS and SOME/IP. The results showed that the time required for conversion is small and that the proposed bridge converter can quickly convert even large data. The proposed framework makes useful ROS 2 development support tools 

such as Rviz and ROSbag, which are not yet available for AUTOSAR AP, available for AUTOSAR AP. In addition, communication with ROS 2-based software such as Autoware is also possible. Finally, we implemented FIDL automatic generator to reflect AUTOSAR AP settings easily in the bridge converter. FIDL automatic generator automatically generates FIDL and FDEPL files for this purpose. In addition, by loading an msg file that defines an original custom message, FIDL files describing the conversion specifications can be automatically generated. The use of FIDL automatic generator facilitates the use of the proposed collaboration framework. 

Future challenges include the current support for a limited number of message types and the need to accommodate complex systems requiring multiple message types. The proposed bridge converter will evolve by supporting a wider variety of message types and by automating their integration. QEMU was employed in the AUTOSAR AP environment for functionality verification during the evaluation. However, considering the collaboration between ROS 2 and AP at the control level in an automobile, both must operate on the actual device. FIDL automatic generator can read the ARXML files used in AUTOSAR AP and automatically generate the files from them, and we are considering improving it for greater convenience. 

## REFERENCES 

- [1] S. Kato, S. Tokunaga, Y. Maruyama, S. Maeda, M. Hirabayashi, Y. Kitsukawa, A. Monrroy, T. Ando, Y. Fujii, and T. Azumi, “Autoware on board: Enabling autonomous vehicles with embedded systems,” in Proc. of the 9th ACM/IEEE ICCPS, 2018, pp. 287–296. 

- [2] “AUTomotive Open System ARchitecture Adaptive Platform (AUTOSAR AP),” https://www.autosar.org/standards/adaptive-platform/. 

- [3] A. Arestova, M. Martin, K.-S. J. Hielscher, and R. German, “A Service-Oriented Real-Time Communication Scheme for AUTOSAR Adaptive Using OPC UA and Time-Sensitive Networking,” Sensors, vol. 21, no. 7, p. 2337, 2021. [Online]. Available: https://www.mdpi.com/1424-8220/21/7/2337 

- [4] “Scalable Open Architecture for Embedded Edge (SOAFEE) ,” https://www.soafee.io/. 

- [5] M. Schindewolf, D. Grimm, C. Lingor, and E. Sax, “Toward a resilient automotive service-oriented architecture by using dynamic orchestration,” in Proc. of the 1st IEEE International Conference on CogMob, 2022, pp. 000 147–000 154. 

- [6] “Object Management Group (OMG)/Data Distribution Service (DDS),” https://www.omg.org/omg-dds-portal/. 

- [7] Y. Maruyama, S. Kato, and T. Azumi, “Exploring the performance of ROS 2,” in Proc. of the 16th ACM International Conference on EMSOFT, 2016, pp. 1–10. 

- [8] J. Henle, M. Stoffel, M. Schindewolf, A.-T. N¨agele, and E. Sax, “Architecture platforms for future vehicles: a comparison of ROS 2 and adaptive AUTOSAR,” in Proc. of the 25th IEEE ITSC, vol. 8, 2022, pp. 3095–3102. 

- [9] A. Ioana, A. Korodi, and I. Silea, “Automotive IoT ethernet-based communication technologies applied in a V2X context via a multiprotocol gateway,” Sensors, vol. 22, no. 17, p. 6382, 2022. [Online]. Available: https://www.mdpi.com/1424-8220/22/17/6382 

- [10] “ROS Visualization (Rviz),” https://github.com/ros2/rviz/. [11] “ROS 2/Rosbag 2,” https://github.com/ros2/rosbag2/. [12] “AUTOSAR AP R23-11/Specification of Communication Management,” https://www.autosar.org/fileadmin/standards/R23-11/AP/AUTOSAR AP SWS CommunicationManagement.pdf/. 

- [13] “miketsukerman/vsomeip-ros-bridge,” https://github.com/miketsukerman/vsomeip-ros-bridge/. [14] “COVESA/vsomeip,” https://github.com/COVESA/vsomeip/. [15] “Scalable service-Oriented MiddlewarE over IP (SOME/IP),” https://some-ip.com/index.shtml/. 

- [16] M. C¸ akır, T. H¨ackel, S. Reider, P. Meyer, F. Korf, and T. C. Schmidt, “A QoS Aware Approach to Service-Oriented Communication in Future Automotive Networks,” in Proc. of the 11th IEEE VNC, 2019, pp. 1–8. 

- [17] A. Kampmann, B. Alrifaee, M. Kohout, A. W¨ustenberg, T. Woopen, M. Nolte, L. Eckstein, and S. Kowalewski, “A dynamic service-oriented software architecture for highly automated vehicles,” in Proc. of the 20th IEEE ITSC, 2019, pp. 2101–2108. 

- [18] S. F¨urst and M. Bechter, “Autosar for connected and autonomous vehicles: The autosar adaptive platform,” in Proc. of the 46th IEEE/IFIP International Conference on DSN-W, 2016, pp. 215–217. 

- [19] A. Ioana and A. Korodi, “DDS and OPC UA Protocol Coexistence Solution in Real-Time and Industry 4.0 Context Using Non-Ideal Infrastructure,” Sensors, vol. 21, no. 22, p. 7760, 2021. [Online]. Available: https://www.mdpi.com/1424-8220/21/22/7760 

- [20] ——, “OPC UA Publish-Subscribe and VSOME/IP Notify-Subscribe Based Gateway Application in the Context of Car to Infrastructure Communication,” Sensors, vol. 20, no. 16, p. 4624, 2020. [Online]. Available: https://www.mdpi.com/1424-8220/20/16/4624 

- [21] D. Hong and C. Moon, “Autonomous driving system architecture with integrated ros2 and adaptive autosar,” Electronics, vol. 13, no. 7, p. 1303, 2024. [Online]. Available: https://www.mdpi.com/2079-9292/13/7/1303 

- [22] “langroodi/Adaptive-AUTOSAR,” https://github.com/langroodi/Adaptive-AUTOSAR?tab=readme-ov-file/. 

