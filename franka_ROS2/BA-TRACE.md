---
title: "BA-TRACE: Boundary-Aware Trace Reconstruction for Scenario-Based Evaluation of Mixed AUTOSAR Adaptive and ROS 2 Vehicular Embedded Systems"
date: "2026-09-17"
authors: "Shunsuke Ito; Ryudai Iwakami; Hiroyuki Hanyu; Tasuku Ishigooka; Takuya Azumi"
url: https://arxiv.org/abs/2609.19699
pdf: https://arxiv.org/pdf/2609.19699
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2609.19699)** / [論文ページ](https://arxiv.org/abs/2609.19699)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# BA-TRACE: Boundary-Aware Trace Reconstruction for Scenario-Based Evaluation of Mixed AUTOSAR Adaptive and ROS 2 Vehicular Embedded Systems 

Shunsuke Ito<sup>_∗_</sup> , Ryudai Iwakami<sup>_∗_</sup> , Hiroyuki Hanyu<sup>_†_</sup> , Tasuku Ishigooka<sup>_†_</sup> , and Takuya Azumi<sup>_‡_</sup> 

_∗ Graduate School of Science and Engineering, Saitama University_ 

_† Technology Development Functional Division, Astemo, Ltd._ 

_‡ Academic Association (Graduate School of Science and Engineering), Saitama University_ 

**_Abstract_ —Modern vehicular embedded systems increasingly combine ROS 2-based autonomous-driving stacks with AUTOSAR Adaptive Platform (AUTOSAR AP). Such mixed stacks make scenario-based evaluation hard to interpret because execution paths cross DDS–SOME/IP middleware boundaries between ROS 2 and AUTOSAR AP. Existing simulators and tracing tools execute scenarios or collect platform-local traces but cannot reconstruct cross-domain data flows. This paper presents** **_BATRACE_ , a boundary-aware trace reconstruction framework for scenario-based evaluation of mixed AUTOSAR AP and ROS 2 vehicular embedded systems. BA-TRACE combines ROS 2 trace events, AUTOSAR ara::log events, ARXML-derived structural dependencies, and bridge-level instrumentation to reconstruct an end-to-end execution graph across the DDS–SOME/IP boundary. A case study with an AWSIM/OpenSCENARIObased object-detection and braking scenario shows that BATRACE reconstructs the expected cross-platform path and exposes boundary-specific latency such as point-cloud transfer overhead. The reconstructed topology is used as evidence of traceability, not as proof of behavioral correctness or safety.** 

**_Index Terms_ —AUTOSAR Adaptive Platform, ROS 2, DDS, SOME/IP, trace reconstruction, timing analysis, vehicular embedded systems, OpenSCENARIO.** 

## I. INTRODUCTION 

Autonomous driving technologies are moving from laboratory prototypes toward practical deployment, and credible safety validation is becoming increasingly important. Developers must evaluate not only nominal driving behavior but also rare and hazardous edge cases (e.g., cut-in with sudden stop) involving complex interactions with surrounding traffic participants [1]. Scenario-based validation has emerged as a promising approach to this challenge [2], and standard scenario description languages such as OpenSCENARIO [3] enable reusable and structured test design. 

Software-Defined Vehicles (SDVs) are increasing the heterogeneity of automotive software environments. In practice, development and validation are increasingly conducted in mixed environments combining AUTOSAR Adaptive Platform (AUTOSAR AP), a production-grade automotive foundation, with Robot Operating System 2 (ROS 2) [4]. Such mixed software stacks make scenario-based evaluation difficult to interpret because execution paths cross heterogeneous middleware boundaries, namely DDS-based ROS 2 communication and SOME/IP-based AUTOSAR AP communication. Existing 

simulation and tracing tools can execute driving scenarios or collect platform-local traces, but do not reconstruct how scenario-triggered data flows across these execution domains. 

This paper does not propose a new simulator or scenario description language. Instead, it proposes _BA-TRACE_ , a boundary-aware trace reconstruction workflow making scenario-based evaluation diagnostically interpretable for mixed AUTOSAR AP and ROS 2 vehicular embedded systems. BA-TRACE combines ROS 2 trace events, AUTOSAR ara::log events, ARXML-derived structural dependencies, and bridge-level instrumentation to reconstruct an end-to-end execution graph across the DDS–SOME/IP boundary. 

Based on this objective, the following research questions (RQs) are formulated: 

- **RQ1:** What traceability gap arises when scenario-based evaluation is applied to mixed AUTOSAR AP and ROS 2 vehicular embedded systems? 

- **RQ2:** Can boundary-aware trace reconstruction recover the expected end-to-end execution topology across DDS and SOME/IP communication domains? 

- **RQ3:** How does the reconstructed cross-platform execution graph support timing interpretation of scenariotriggered behavior? 

The contributions of this paper are summarized as follows: 

- We formulate the traceability problem in scenariobased evaluation of mixed AUTOSAR AP–ROS 2 systems, identifying semantic and timing gaps across DDS, SOME/IP, and bridge-level boundaries. 

- We propose _BA-TRACE_ , a boundary-aware trace reconstruction workflow combining ROS 2 traces, AUTOSAR ara::log events, ARXML-derived dependencies, and bridge-level instrumentation to reconstruct an end-to-end execution graph across the DDS–SOME/IP boundary. 

- We implement BA-TRACE in a vehicular embedded testbed using Autoware, AUTOSAR AP, AWSIM, OpenSCENARIO, and an instrumented bridge converter. An edge-case object-detection and braking scenario shows the reconstructed graph exposes cross-platform paths and boundary-specific latency. 

- The reconstructed topology is used as evidence of traceabil- 

- ity, not as proof of behavioral correctness or safety. 


Fig. 1. Architecture of the BA-TRACE framework. 

The remainder of this paper is organized as follows. Section II describes the technical background of AUTOSAR AP and ROS 2. Section III presents the proposed framework, and Section IV reports the evaluation results. Section V discusses lessons learned, and Section VI reviews related work. Finally, a brief conclusion is given. 

## II. SYSTEM MODEL 

The BA-TRACE framework targets mixed AUTOSAR AP– ROS 2 vehicular embedded systems, where scenario-triggered execution paths cross the DDS–SOME/IP boundary at a bridge converter. Its overall architecture is shown in Fig. 1. The framework integrates five technical building blocks: OpenSCENARIO as the scenario specification language, AWSIM as the autonomous driving simulator, ROS 2-based Autoware and AUTOSAR AP applications as the heterogeneous mixed stack, and the CART [5]/CARET [6] pipeline as the trace correlation and visualization backend used to render the reconstructed cross-platform execution graph. The remainder of this section reviews each building block, starting with OpenSCENARIO as the entry point of the workflow. 


Fig. 2. ROS 2 architecture. 

## _B. Autonomous Driving Simulator_ 

Autonomous driving simulators provide a virtual environment with road structures, traffic participants, and weather/lighting conditions, and are equipped with sensor models such as LiDAR, cameras, radar, and GNSS. They model the ego-vehicle and surrounding entities and reproduce diverse driving scenarios in a controlled manner, including situations that are difficult or dangerous to reproduce in the real world. Representative examples include CARLA [7], which features high-fidelity rendering on Unreal Engine, and AWSIM [8], which is Unity-based, lightweight, and suitable for cloud environments; trade-offs therefore exist among realism, flexibility, and computational cost. AWSIM is the simulator used in BATRACE. 

Most autonomous driving simulators are independent systems and do not natively use the DDS-based communication of ROS 2; they expose simulator-specific client–server APIs in Python or C++. A dedicated bridge is therefore required to integrate them with ROS 2-based stacks. The bridge converts simulator-internal data into ROS 2 messages and synchronizes control commands back to the simulator, allowing the simulator to function as a virtual sensor input source for the autonomous driving stack. 

## _C. Robot Operating System 2 (ROS 2)_ 

## _A. OpenSCENARIO_ 

In scenario-based evaluation of autonomous driving systems, OpenSCENARIO is used as a standard description format for defining test cases [3]. Critical traffic situations and edge cases, such as sudden lane changes or pedestrians darting out, are described concretely as XML-based scenarios. As an open standard independent of specific tools, scenarios written once can be reused across various simulators, enabling efficient and reproducible testing. 

OpenSCENARIO uses a hierarchical structure of Story, Act, Maneuver, and Event, and supports precise behavior definition via tags such as <LaneChangeAction> (with attributes specifying, for example, completion within 0.5 seconds for aggressive cut-in) and <StartTrigger> (firing at a deterministic simulation time), enabling reproducible and platformindependent test cases. 

ROS 2 is open-source middleware widely used in autonomous driving software and industrial systems [4] and meets real-time constraints through DDS. The three-layer ROS 2 architecture (Fig. 2) comprises application, middleware, and OS layers; the application hosts user code and ROS 2 nodes, while the middleware uses DDS for inter-node communication. ROS 2 _nodes_ exchange data through _topics_ via a publish/subscribe model. This loose coupling enables efficient data sharing and a broad tool ecosystem, including the tracing tools ros2 <u>tracing</u> [9] and CARET, both used by BA-TRACE on the ROS 2 side. 

## _D. AUTOSAR Adaptive Platform (AUTOSAR AP)_ 

AUTOSAR AP is a software architecture for nextgeneration automotive embedded systems [4]. Compared to ROS 2 with DDS, AUTOSAR AP uses SOME/IP (Scalable 


Fig. 4. CART structure within BA-TRACE. 

service-Oriented MiddlewarE over IP) as its main communication protocol. Unlike ROS 2, AUTOSAR AP requires a license, is less openly documented, and can be more difficult to handle due to extensive standardization. Its architecture (Fig. 3) is layered into application, middleware, and OS, similar to ROS 2 [4]. 

The middleware, AUTOSAR Runtime for Adaptive Application (ARA), provides core services including the standard logging interface ara::log. Adaptive Applications (AAs) communicate via service requests under a Service-Oriented Architecture (SOA) supported by SOME/IP. The data types and interfaces handled by AAs, the SOME/IP configurations, and the inter-AA structural dependencies are all defined in AUTOSAR XML (ARXML), which BA-TRACE consumes as its static structural source for trace reconstruction. 

_E. CART (Combined AUTOSAR AP and ROS 2 Tracing Framework)_ 

CART (Combined AUTOSAR AP and ROS 2 Tracing) [5] is the trace correlation backend used by BA-TRACE for mixed AUTOSAR AP and ROS 2 systems. CART first extracts structural dependencies among Adaptive Applications from ARXML files and represents them as a directed acyclic graph (DAG). It then reads execution timestamps from ara::log and converts AUTOSAR-side events into Common Trace Format (CTF)-based trace data compatible with ROS 2 analysis 

tools. These traces are merged with native ROS 2 trace data collected via ros2 <u>tracing,</u> allowing the entire cross-platform execution flow to be analyzed and visualized in a unified manner. Within BA-TRACE, CART is the component that fuses ARXML-derived static structure with dynamic ROS 2 and AUTOSAR-side events, producing the merged trace from which the reconstructed cross-platform execution graph and latency breakdown are derived. The open-source implementation of CART is publicly available on GitHub [10]. 

## _F. CARET_ 

CARET (Chain-Aware ROS 2 Evaluation Tool) [6] is a performance analysis tool for ROS 2 applications and serves as the BA-TRACE frontend for visualizing and analyzing latency in the merged trace produced by CART (Fig. 4). By adding tracepoints to ROS 2 tracing, CARET measures inter-node communication and callback execution times and message-flow dependencies without modifying application code, enabling bottleneck and lost-message detection. CARET presents latency-distribution histograms, tables of minimum, average, and maximum latency, and message-flow graphs, which BA-TRACE reuses to render the reconstructed crossplatform execution graph and the latency breakdown reported in Section IV. 

## III. DESIGN AND IMPLEMENTATION 

## _A. Overview of BA-TRACE_ 

The BA-TRACE framework, whose architecture is shown in Fig. 1, integrates a scenario-driven simulation testbed with a boundary-aware trace reconstruction workflow. The testbed executes reproducible OpenSCENARIO-defined scenarios in a cloud-native environment, and the workflow combines ROS 2 trace events, AUTOSAR ara::log events, ARXML-derived structural dependencies, and bridge-level instrumentation to reconstruct an end-to-end execution graph across the DDS– SOME/IP boundary. The remainder of this section first describes the trace reconstruction workflow (Section III-B) and the bridge-level instrumentation that anchors it (Section III-C), and then the cloud simulation testbed (Section III-D) and the mixed Autoware–AUTOSAR AP implementation (Section III-E) on which BA-TRACE is exercised. 

## _B. Boundary-Aware Trace Reconstruction Workflow_ 

BA-TRACE reconstructs an end-to-end execution graph by correlating four sources: ROS 2 trace events, AUTOSAR ara::log events, ARXML-derived structural dependencies, and bridge-level boundary events. The Bridge Converter is treated as an explicit observation point because it is the only component that simultaneously observes ROS 2-side DDS topic semantics and AUTOSAR-side SOME/IP service semantics. 

Concretely, BA-TRACE reconstructs the execution graph in four steps: (1) extracting ROS 2 callback and communication events from ros2 <u>tracing; (2) extracting AUTOSAR-side struc-</u> tural dependencies from ARXML and runtime timestamps 

from ara::log; (3) correlating DDS-side and SOME/IPside events using bridge-level instrumentation and correlation identifiers; and (4) merging the ROS 2, AUTOSAR AP, and boundary edges into a single cross-platform execution graph from which the latency breakdown is derived. 

## _C. Bridge-Level Instrumentation at the DDS–SOME/IP Boundary_ 

A Bridge Converter (BC) handles bidirectional translation between the DDS protocol used in ROS 2 and the SOME/IP protocol used in AUTOSAR AP, including datatype serialization. The Bridge Converter is the only component that simultaneously observes both ROS 2-side topic semantics and AUTOSAR-side SOME/IP service semantics. BATRACE therefore instruments it as a boundary observation point: in addition to protocol and data conversion, the bridge captures timing information at the DDS–SOME/IP boundary and embeds correlation identifiers that link DDS-side and SOME/IP-side events. This boundary-level instrumentation is the technical core of BA-TRACE and is what makes the crossplatform execution graph reconstructible. 

## _D. Scenario-Driven Cloud Simulation Testbed_ 

Scenario-driven evaluation of BA-TRACE relies on a cloudnative testbed combining OpenSCENARIO as the scenario specification language with AWSIM as the autonomous driving simulator. 

_1) Cloud-Native Evaluation Environment:_ The foundation of the testbed is a cloud-native evaluation environment, aligned with the Scalable Open Architecture for Embedded Edge (SOAFEE) framework that promotes cloud-native development for SDVs. The primary rationale for adopting a cloud environment is reproducibility and resource elasticity, which are often compromised in on-premise setups due to “environment drift”, subtle discrepancies in OS versions, drivers, or library dependencies that lead to the “it works on my machine” paradox. Cloud infrastructure resolves this by enabling preconfigured machine images: cloning a standardized image instantiates identical instances for every test run, eliminating environmental variability and keeping evaluation results consistent regardless of when or by whom the tests are executed. This cloning capability also synergizes with resource elasticity, allowing scenarios to be parallelized across multiple instances (scale-out) or migrated to higher-performance instance types (scale-up), which is crucial for future integration with Continuous Integration pipelines. 

_2) Adoption of OpenSCENARIO for Reproducible Validation:_ ASAM OpenSCENARIO 1.x is adopted as the standard format for defining test cases that cover both routine driving situations and rare safety-critical edge cases. The decision to adopt OpenSCENARIO, as opposed to simulatorspecific proprietary scripts or random traffic generation, is driven by interoperability and reproducibility. Random traffic generation lacks the determinism required to consistently reproduce specific hazardous situations such as a pedestrian darting out at a precise timing, while proprietary scripts lock 


Fig. 5. Implementation of the proposed platform for evaluation. 

validation assets to a specific simulator and hinder crossplatform verification. By using OpenSCENARIO, BA-TRACE keeps scenario assets portable and ensures that complex interaction events can be defined with strict temporal and spatial precision. At runtime, the simulator parses .xosc files to spawn entities and set initial conditions, monitors triggers such as ego-vehicle speed or position, and dynamically executes maneuvers, supporting controlled replay of logically equivalent scenario conditions and providing a scenario stimulus for subsequent trace reconstruction. 

## _E. Mixed Autoware–AUTOSAR AP Implementation_ 

The evaluation target is a mixed environment in which Autoware provides the ROS 2-side autonomous driving stack and AUTOSAR Adaptive Applications carry functions deployed on the AUTOSAR Adaptive Platform. The simulator transmits sensor inputs (e.g., LiDAR point clouds) to Autoware via a dedicated simulator-to-ROS 2 bridge, and the Bridge Converter described in Section III-C handles the DDS–SOME/IP boundary between Autoware nodes and the AUTOSAR-side AAs. The specific deployment used for evaluation, in which object detection is hosted by an AUTOSAR Adaptive Application, is detailed in Section IV. 

## IV. EVALUATION 

The BA-TRACE framework is implemented as described below and evaluated from three perspectives aligned with the research questions in Section I. First, the evaluation examines the traceability gap that arises when a scenariotriggered execution path crosses the DDS–SOME/IP boundary in a mixed AUTOSAR AP–ROS 2 stack (RQ1). Second, it examines whether boundary-aware trace reconstruction recovers the expected end-to-end execution topology across DDS and SOME/IP communication domains (RQ2). Third, it examines whether the reconstructed execution graph supports timing interpretation of scenario-triggered behavior (RQ3). The reported results should be interpreted as evidence of diagnostic traceability and timing interpretability, not as proof of behavioral correctness or safety. 

## _A. Evaluation Platform Details_ 

The detailed implementation of the evaluation platform is shown in Fig. 5. AWS (Amazon Web Services) [11] was selected for the cloud environment, and the testbed was implemented on EC2 instances. The Bridge Converter employs an open-source implementation [12], [13] enhanced with the 

|TA<br>EVALUATI<br>CONFI|BLE I<br>ONINSTANCE<br>GURATION|TA<br>USED SOFTW<br>Software|BLE II<br>ARE VERSIONS<br>Version|
|---|---|---|---|
|Instance Type|g5.8xlarge|OS|Ubuntu 22.04|
|CPU|AMD EPYC 7R32|AUTOSAR AP|R20-11|
||32 cores|ROS 2|Humble Hawksbill|
|RAM|128 GB|Autoware|0.45.1|
|GPU|NVIDIA A10G|AWSIM|v2.0.1|
||Tensor Core GPU|LTTng|2.13|
|VRAM|24 GB|ros2<br>tracing|v0.3.0|
|||CARET|v0.6.1|


improvements described in Section III. AWSIM was selected as the autonomous driving simulator for its native ROS 2/Autoware integration and direct OpenSCENARIO ingestion. 

The simulator and the autonomous driving system were deployed on a single high-performance instance to remove network jitter and bandwidth bottlenecks inherent in distributed setups, which would otherwise introduce noise into the timing measurements. This lets boundary-specific overhead (such as the 7.62 ms point-cloud transfer cost reported in Section IV-B) be attributed to the software stack itself rather than to external network variability, a methodological choice for diagnostic clarity, not a substitute for distributed-deployment evaluation. 

Logs are collected from the executing autonomous driving system using CART (Combined AUTOSAR AP and ROS 2 Tracing framework), the trace correlation backend used by BATRACE. Because AWSIM and the autonomous driving stack require a GPU and significant memory, a high-performance instance was adopted (Table I). 

The Bridge Converter, adopted from the open-source implementation [12], was modified to enable boundary-aware tracing across the heterogeneous DDS–SOME/IP boundary. Since its original SOME/IP transmission and reception modules do not natively generate traceable events via ara::log or ros2 <u>tracing,</u> tracepoints were added only at the bridge to capture protocol-boundary timing and embed correlation identifiers, without modifying the core logic of the AUTOSAR Adaptive Application or the ROS 2 nodes. 

Autoware served as the base, with object detection handled by an AUTOSAR Adaptive Application (AA), creating a mixed AUTOSAR AP and ROS 2 environment. As illustrated in Fig. 5, point cloud data acquired from AWSIM is transmitted via DDS to the Bridge Converter, which converts the data to SOME/IP and forwards it to the Object Detection AA on the AUTOSAR AP side. The detection results are returned to Autoware through the Bridge Converter by converting them back from SOME/IP to DDS, and the system issues a stop command upon detecting an object in front. To exercise this logic, an edge-case scenario was defined in OpenSCENARIO: on a two-lane main road, an NPC vehicle overtakes the egovehicle from the right lane, cuts in front of it, and immediately performs a sudden stop. This setup verifies object detection responsiveness and braking maneuver execution under aggressive cut-in and sudden deceleration. The software versions used in this evaluation are listed in Table II. 

_B. Boundary-Aware Trace Reconstruction in a Practical Simulation Environment_ 

In this section, BA-TRACE is evaluated using the simulation testbed described in the previous section. By executing the autonomous driving system under the defined edge-case scenario, three properties are examined: (i) the traceability gap that emerges when scenario-triggered data crosses the DDS– SOME/IP boundary, (ii) the recovery of the expected end-toend execution topology by boundary-aware trace reconstruction, and (iii) the timing interpretation of scenario-triggered behavior via the reconstructed execution graph. 

_1) Scenario-Triggered Execution and the Traceability Gap:_ The testbed was exercised under the edge-case cut-in scenario described in the previous subsection. AWSIM reproduced the specified traffic situation, and the mixed autonomous driving stack operated on the same cloud instance while processing sensor data and object detection results across the ROS 2– AUTOSAR AP boundary, providing a stable testbed condition under which scenario-triggered execution can be observed. 

This result establishes the testbed condition needed to investigate RQ1. Concretely, the scenario-triggered data flow visibly crosses the DDS–SOME/IP boundary at the bridge converter, the point at which ROS 2 trace events or AUTOSAR ara::log events alone become insufficient to describe the cross-platform path. The traceability gap motivated in Section I therefore manifests in the testbed as a concrete observation problem, which the next subsubsection addresses by topologylevel reconstruction. 

_2) Topology Reconstruction and Timing Interpretation:_ The collected logs are fed into BA-TRACE to reconstruct the cross-platform execution graph and measure the end-toend latency of the mixed Autoware–AUTOSAR AP system. End-to-end latency is defined as the duration from the reception of point cloud data by the ROS 2 input node ( _/pointcloud_ _<u>downsampler</u>_ ) to the issuance of the corresponding control command by the actuation node ( _/relay_ _<u>node</u>_ ), which immediately forwards the command to the simulator interface. Topology coverage is defined as the edge coverage between the expected graph (from design artifacts) and the observed graph reconstructed by CARET from merged traces. 

Here, _E_ expected denotes the set of dependency edges in the complete end-to-end path, defined by the design artifacts (i.e., ARXML for AUTOSAR AP and node configurations for ROS 2) prior to execution. Meanwhile, _E_ observed denotes the set of edges actually extracted from the merged runtime traces. Accordingly, the coverage metric is defined as: 


In this evaluation, the reconstructed topology achieved a coverage of 100% with respect to the expected end-to-end graph. This indicates that all expected dependency edges, including the cross-platform edges between ROS 2 and AUTOSAR AP, were observed in the reconstructed graph. Topology coverage is a diagnostic indicator that the cross-platform path was exercised, not a measure of behavioral correctness, 


Fig. 6. Latency breakdown along the reconstructed end-to-end path (min/avg/max). 


Fig. 7. End-to-end message flow reconstructed from merged ROS 2 and AUTOSAR AP traces. 

scenario coverage, or safety. This is visually corroborated by the end-to-end chain latency in Fig. 6: the reconstructed path extends without discontinuity from the ROS 2 sensor node ( _/pointcloud_ _<u>downsampler</u>_ ) to the actuation node, supporting the answer to RQ2. 

The reconstructed message flow within the end-to-end path is visualized in Fig. 7. The reconstructed trace extends to the final actuation callback (relay <u>node/callback 1/callback start)</u> only when the object detection result is true (i.e., a stop command has been actively issued); when the result is false, the flow terminates earlier without reaching the actuation node. This visual distinction shows that the reconstructed graph captures the dynamic scenario in which the obstacle disappears, the detection becomes false, and the ego-vehicle resumes motion, indicating that BA-TRACE traces varying control logic across the heterogeneous boundary in response to changes in the traffic situation. 

The latency statistics in Fig. 6 localize boundary-specific overhead along the reconstructed path. The stages leading up to the Object Detection AA, specifically the _/SOMEIP_ _<u>in</u>_ 

path, involve the transmission of heavy point cloud data, and the reconstructed graph attributes a relatively larger communication overhead (avg: 7.62 ms) to this section compared with other sections. The latency observed in _/SOMEIP_ _<u>in</u>_ includes serialization, transport, and deserialization overhead, and should be interpreted as an aggregated communication cost across the DDS–SOME/IP boundary. In contrast, the subsequent stages, which transmit only lightweight detection results or stop commands via _/SOMEIP_ _<u>out</u>_ , exhibit minimal latency (avg: 0.59 ms), an order of magnitude smaller than the /SOMEIP <u>in</u> path. This ability to distinguish boundaryspecific overhead according to data payload illustrates that BA-TRACE makes scenario-triggered behavior diagnostically interpretable in realistic mixed-platform environments. 

These results support RQ3: the reconstructed graph turns external scenario outcomes into diagnostically interpretable timing evidence about internal cross-platform behavior at the DDS–SOME/IP boundary. 

## V. LESSONS LEARNED 

Based on the evaluation results, the three research questions of Section I are revisited, followed by practical insights obtained through the design and operation of _BA-TRACE_ . The discussion focuses on the role of boundary-aware trace reconstruction in interpreting scenario-triggered behavior of mixed AUTOSAR AP–ROS 2 vehicular embedded systems. 

## _A. Validation of Research Questions_ 

Regarding **RQ1** , the evaluation made the traceability gap concrete. Scenario-triggered data flow in the mixed stack crosses the DDS–SOME/IP boundary at the bridge converter, and ROS 2 trace events or AUTOSAR ara::log events alone cannot describe the cross-platform path. ARXMLderived structural dependencies and bridge-level instrumentation were both required to fill this gap, confirming that the gap is structural rather than incidental to a particular scenario. 

Regarding **RQ2** , BA-TRACE reconstructed an end-to-end execution graph aligned with the expected cross-platform processing topology, including the path through the pointcloud transfer stage, the AUTOSAR-side object-detection application, and the actuation-side return path. This indicates that boundary-aware trace reconstruction can recover expected execution topology across DDS and SOME/IP domains. The topology, however, is evidence of traceability rather than proof of behavioral correctness or safety. 

Regarding **RQ3** , the reconstructed graph supported timing interpretation of scenario-triggered behavior. The latency breakdown localized boundary-specific overhead: point-cloud transfer dominated the DDS-to-SOME/IP path, while the lighter detection-result return path was an order of magnitude smaller. In addition, the reconstructed message flow showed that the actuation path is reached only when the objectdetection result is true and terminates earlier otherwise. These results show that the reconstructed graph turns external scenario outcomes into diagnostically interpretable timing evidence about internal cross-platform behavior. 

TABLE III 

COMPARISON OF VALIDATION METHODOLOGIES 

|Method / Paper|AUTOSAR AP|ROS 2|Validation Type|Scenario|Simulation|
|---|---|---|---|---|---|
|Real-world Testing [14]–[16]|✓|✓|Functional|Limited||
|HIL Testing [16]–[20]|✓|✓|Real-time|Limited|Partially|
|ASAM OpenSCENARIO [3]|||Functional (Black-box)|✓|✓|
|CARLA [7]||✓|Functional (Black-box)|✓|✓|
|Logical scenario generation (ISO 34502-aligned) [21]|||Methodology / Process|✓|✓|
|Survey on safety-critical scenario generation [2]|||Survey / Taxonomy|✓|Limited|
|Scenario-based accelerated testing for SOTIF [22]|||Survey / Taxonomy|✓|Limited|
|VIVAS [23]||✓|Functional / Formal|✓|✓|
|SimValidation [24]||✓|Functional / Formal|✓|✓|
|Formal scenario-based testing (sim-to-track) [15]||Limited|Formal|✓|✓|
|SimADFuzz [25]||✓|Robustness (Black-box)|✓|✓|
|Adaptive scenario generation [26]||✓|Robustness (Search-based)|✓|✓|
|Diversity-oriented exploration [27]||✓|Robustness (Diversity-driven)|✓|✓|
|SafeVar [28]||✓|Robustness (Uncertainty)|✓|✓|
|This paper|✓|✓|Performance / Interpretability (White-box)|✓|✓|


## _B. Practical Insights_ 

**Bridge converters are observation points, not just protocol mappers:** The bridge is the only component that simultaneously observes ROS 2-side topic semantics and AUTOSARside SOME/IP service semantics. Treating it as an instrumentation point rather than a transparent translator is what makes cross-platform reconstruction tractable. 

**Static and dynamic sources must be combined:** Neither dynamic traces nor ARXML-derived structural dependencies are individually sufficient. Dynamic events miss declared structure that is not exercised in a given scenario, while ARXML alone cannot describe runtime timing. Combining them allowed expected dependency edges to be checked against observed ones. 

**Topology coverage is a diagnostic indicator, not a safety metric:** The fraction of expected dependency edges observed in the reconstructed graph indicates how completely a scenario exercised the cross-platform path. It does not indicate scenario coverage, behavioral correctness, or safety, and should be reported with this scope. 

**Single-instance deployment supports timing interpretability:** Co-locating the simulator and the software stack on a single instance removes network-induced variability and lets boundary-specific latency be attributed to the software stack itself. This is a methodological choice for diagnostic clarity, not a substitute for distributed-deployment evaluation. 

## VI. RELATED WORK 

Prior work on scenario-based validation, autonomous driving simulators, and systematic testing provides the basis for practical scenario-driven validation of mixed AUTOSAR AP– ROS 2 systems. The comparison results are summarized in Table III. 

## _A. Scenario-based Validation Foundations_ 

Scenario-based validation turns complex traffic situations into analyzable, reproducible artifacts and supports automated generation, execution, and analysis beyond mileage-oriented testing. ISO 34502-aligned logical scenario generation defines parameter ranges for concrete tests [21], while existing surveys and SOTIF-oriented studies organize generation, classification, 

risk-oriented testing, and accelerated assessment [2], [22]. These studies ground scenarios as validation artifacts, although they emphasize design and generation rather than execution and internal interpretation in mixed software environments. 

## _B. Simulation-based Validation Frameworks_ 

Simulation-based validation frameworks automate scenario execution through simulators and standardized descriptions, with CARLA [7] supporting controlled testing of perception, planning, and control stacks and ASAM OpenSCENARIO [3] enabling repeatable, interoperable dynamic scenarios. 

VIVAS [23], SimValidation [24], and formal scenario-based testing [15] link scenario execution with coverage criteria, runtime monitoring, or safety properties. These frameworks strengthen functional and formal assurance, although they evaluate observable outcomes and provide limited support for interpreting cross-platform internal behavior in heterogeneous software architectures. 

_C. Search-based and Robustness-oriented Scenario Exploration_ 

Falsification and search-based testing discover failure cases in scenario parameter spaces. SimADFuzz [25] uses simulation feedback and guided mutation to prioritize violationinducing scenarios, while related methods characterize limits through adaptive search, diversity-oriented exploration, and uncertainty-aware analysis. Adaptive search identifies performance boundaries and clusters [26], diversity-oriented exploration promotes distinct failures [27], and SafeVar shows physical-parameter variations, such as mass and friction, can increase unsafe outcomes [28]. 

These studies support failure discovery and robustness assessment, although they differ from validation integrating scenario execution with white-box interpretation of mixedplatform behavior. 

## _D. Positioning of This Study_ 

Existing scenario-based studies focus on generating, executing, or evaluating driving scenarios from an externally observable perspective, while existing tracing tools provide detailed observations within specific platforms such as ROS 2 

or AUTOSAR AP. The gap addressed in this paper lies between these two directions: in mixed vehicular embedded systems, scenario-triggered behavior must be interpreted across heterogeneous middleware boundaries. BA-TRACE bridges this gap by reconstructing scenario-triggered execution paths across DDS and SOME/IP, combining ROS 2 trace events, AUTOSAR ara::log events, ARXML-derived structural dependencies, and bridge-level instrumentation to provide diagnostic timing interpretability for mixed AUTOSAR AP– ROS 2 vehicular embedded systems. 

## VII. CONCLUSION 

Modern vehicular embedded systems increasingly combine ROS 2-based autonomous-driving software with AUTOSAR AP applications, but execution paths in such mixed stacks cross heterogeneous middleware boundaries that platform-local simulation and tracing tools cannot reconstruct on their own. This paper presented _BA-TRACE_ , a boundaryaware trace reconstruction framework for scenario-based evaluation of mixed AUTOSAR AP and ROS 2 vehicular embedded systems. BA-TRACE combines ROS 2 trace events, AUTOSAR ara::log events, ARXML-derived structural dependencies, and bridge-level instrumentation to reconstruct an end-to-end execution graph across DDS and SOME/IP communication domains. 

The AWSIM/OpenSCENARIO-based evaluation, conducted as an edge-case object-detection and braking case study, showed that BA-TRACE reconstructed the expected crossplatform processing path and related externally observed scenario behavior to internal timing behavior. In particular, the reconstructed latency breakdown exposed boundary-specific communication overhead associated with point-cloud transfer across the DDS–SOME/IP boundary, while the lighter detection-result return path remained an order of magnitude smaller. These results provided evidence of diagnostic traceability and timing interpretability for scenario-triggered behavior, not proof of behavioral correctness or safety. 

Future work will extend BA-TRACE along three directions: broader scenario sets to test the generality of the reconstruction workflow, alternative component placements between AUTOSAR AP and ROS 2 to assess sensitivity to deployment topology, and larger-scale regression testing environments. A complementary direction is to combine BA-TRACE with automated scenario generation and search-based testing so that high-risk or low-coverage situations can be explored systematically across the DDS–SOME/IP boundary. 

## ACKNOWLEDGMENTS 

This work was supported by JST FOREST Grant Number JPMJFR242G. 

## REFERENCES 

- [1] S. Riedmaier, T. Ponn, D. Ludwig, B. Schick, and F. Diermeyer. Survey on Scenario-Based Safety Assessment of Automated Vehicles. _IEEE Access_ , 8:87456–87477, 2020. 

- [2] W. Ding, C. Xu, M. Arief, H. Lin, B. Li, and D. Zhao. A Survey on Safety-Critical Driving Scenario Generation—A Methodological Perspective. _IEEE Trans. Intell. Transp. Syst._ , 24(7):6971–6988, 2023. 

- [3] ASAM OpenSCENARIO. https://www.asam.net/standards/detail/ openscenario/. Accessed: Apr. 29, 2026. 

- [4] J. Henle, M. Stoffel, M. Schindewolf, A.-T. N¨agele, and E. Sax. Architecture platforms for future vehicles: a comparison of ROS 2 and Adaptive AUTOSAR. In _Proc. of IEEE ITSC_ , pages 3095–3102, 2022. 

- [5] R. Iwakami, H. Hanyu, T. Ishigooka, and T. Azumi. CART: Combined AUTOSAR AP and ROS 2 Tracing Framework. In _Proc. of IEEE/ACM RSP_ , pages 15–21, 2026. 

- [6] T. Kuboichi, A. Hasegawa, B. Peng, K. Miura, K. Funaoka, S. Kato, and T. Azumi. CARET: Chain-Aware ROS 2 Evaluation Tool. In _Proc. of IEEE EUC_ , pages 1–8, 2022. 

- [7] CARLA. https://carla.org/. Accessed: Apr. 29, 2026. 

- [8] AWSIM. https://tier4.github.io/AWSIM/. Accessed: Apr. 29, 2026. 

- [9] C. B´edard, I. L¨utkebohle, and M. Dagenais. ros2 <u>tracing:</u> Multipurpose Low-Overhead Framework for Real-Time Tracing of ROS 2. _IEEE Robot. Autom. Lett._ , 7(3):6511–6518, 2022. 

- [10] CART. https://github.com/azu-lab/ CART-Combined-AUTOSAR-AP-and-ROS-2-Tracing-Framework. Accessed: Apr. 29, 2026. 

- [11] AWS. https://aws.amazon.com/jp/?nc2=h <u>lg.</u> Accessed: Apr. 29, 2026. [12] ROS 2 AUTOSAR AP Bridge Converter. https://github.com/azu-lab/ ROS2 <u>AUTOSARAP Bridge Converter.</u> Accessed: Apr. 29, 2026. 

- [13] R. Iwakami, B. Peng, H. Hanyu, T. Ishigooka, and T. Azumi. AUTOSAR AP and ROS 2 Collaboration Framework for Development in Cloud Environment. _IEEE Open J. Ind. Electron. Soc._ , pages 1–13, 2025. 

- [14] Z. Fei, M. Andersson, and A. Tingberg. Correlation of Software-inthe-Loop Simulation with Physical Testing for Autonomous Driving. In _Proc. of IEEE ITSC_ , pages 2050–2057, 2024. 

- [15] D. J. Fremont, E. Kim, Y. V. Pant, S. A. Seshia, A. Acharya, X. Bruso, P. Wells, S. Lemke, Q. Lu, and S. Mehta. Formal Scenario-Based Testing of Autonomous Vehicles: From Simulation to the Real World. In _Proc. of IEEE ITSC_ , pages 1–8, 2020. 

- [16] J. P. Allamaa, P. Listov, H. Auweraer, C. N. Jones, and T. D. Son. Real-time Nonlinear MPC Strategy with Full Vehicle Validation for Autonomous Driving. In _Proc. of ACC_ , pages 1982–1987, 2022. 

- [17] M. Abboush, C. Knieke, and A. Rausch. A Virtual Testing Framework for Real-Time Validation of Automotive Software Systems Based on Hardware in the Loop and Fault Injection. _Sensors_ , 24, 2024. 

- [18] J. van de Sluis, O. Op den Camp, J. Broos, I. Yalcinkaya, and E. de Gelder. Describing I2V Communication in Scenarios for Simulation-Based Safety Assessment of Truck Platooning. _Electronics_ , 2021. 

- [19] Y.-G. Chung and Y.-P. Yang. Hardware-in-the-Loop Simulation of Self-Driving Electric Vehicles by Dynamic Path Planning and Model Predictive Control. _Electronics_ , 2021. 

- [20] K. Devika, A. Bera, V. Ramani, S. Yellapantula, A. Behera, Y. Liu, and S. Subramanian. Driver Distraction Recognition-driven Collision Avoidance Algorithm for Active Vehicle Safety. In _Proc. of IEEE ITSC_ , pages 237–243, 2021. 

- [21] J. Jeon, J. Yoo, T. Oh, and J. Yoo. Simulation-Based Logical Scenario Generation and Analysis Methodology for Evaluation of Autonomous Driving Systems. _IEEE Access_ , 13:43338–43359, 2025. 

- [22] L. Tang, R. Wang, Z. Liu, Y. Liang, Y. Niu, W. Zhu, and Z. Duan. Scenario-Based Accelerated Testing for SOTIF in Autonomous Driving: A Review. _IEEE Internet Things J._ , 12(2):1453–1470, 2025. 

- [23] S. Goyal, A. Griggio, and S. Tonetta. System-level simulation-based verification of Autonomous Driving Systems with the VIVAS framework and CARLA simulator. _Sci. Comput. Program._ , 242:103253, 2025. 

- [24] Y. Li, J. Sun, Y. Peng, M. Zhang, and Y. Zhao. SimValidation: ScenarioBased Runtime Validation for Autonomous Driving Systems. _IEEE Trans. Intell. Transp. Syst._ , 24(6):5781–5794, 2023. 

- [25] Z. Xie, J. Sun, Y. Li, M. Zhang, and Y. Zhao. SimADFuzz: Efficient Simulation-Based Adversarial Testing for Autonomous Driving Systems. In _Proc. of ICSE_ , pages 1–13, 2022. 

- [26] G. E. Mullins, P. G. Stankiewicz, N. J. Hejderup, and S. K. Gupta. Adaptive generation of challenging scenarios for testing and evaluation of autonomous vehicles. _J. Syst. Softw._ , 137:197–215, 2018. 

- [27] X. Ji, L. Xue, Z. He, and X. Luo. Autonomous Driving System Testing via Diversity-Oriented Driving Scenario Exploration. _ACM Trans. Softw. Eng. Methodol._ , 34(7):1–28, 2025. 

- [28] Q. Pan, T. Wang, J. Ma, P. Arcaini, and T. Yue. Simulation-based Safety Assessment of Vehicle Characteristics Variations in Autonomous Driving Systems. _ACM Trans. Softw. Eng. Methodol._ , 2025. 

