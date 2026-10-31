---
title: "Adaptive Bridge: A Proxy-Based Decoupling Layer for Mitigating DDS Backpressure in ROS 2"
date: "2026-08-15"
authors: "Kaushalraj Puwar; B. Thangaraju"
url: https://arxiv.org/abs/2608.15380
pdf: https://arxiv.org/pdf/2608.15380
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2608.15380)** / [論文ページ](https://arxiv.org/abs/2608.15380)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Adaptive Bridge: A Proxy-Based Decoupling Layer for Mitigating DDS Backpressure in ROS 2 

Kaushalraj Puwar 

_International Institute of Information Technology Bangalore_ Bangalore, India Kaushalrajsinh.Puwar@iiitb.ac.in 

B. Thangaraju 

_International Institute of Information Technology Bangalore_ 

Bangalore, India 

B.Thangaraju@iiitb.ac.in 

**_Abstract_ —In systems built on Robot Operating System 2 (ROS 2) and using Data Distribution Service (DDS), a single networkimpaired or throttled subscriber on a RELIABLE topic can cause backpressure that degrades throughput and latency for all other subscribers, including safety-critical ones sharing the publisher, because the publisher’s DDS writer can no longer accept new samples. We present Adaptive Bridge, a proxy-based layer that decouples critical subscribers from degraded or noncritical ones, thereby isolating the critical path through topic splitting and dynamic rate control. The proxy acts as a middleman and subscribes to the original topic and republishes the messages to two independent DDS writers: one RELIABLE writer for critical nodes and one BEST EFFORT writer for noncritical or degraded nodes, thus isolating the degraded nodes and safeguarding the publisher and critical nodes from backpressure. A probe-based classifier actively monitors subscriber health through sampling with hysteresis and adjusts subscriber rate limits in real time. We evaluate the system under a Gilbert-Elliott bursty wireless loss model using a reproducible Docker-based harness. The results show that using the Adaptive Bridge in our evaluation harness reduces the critical subscriber tail p95 latency from up to 15 s to 1.55 ms across all impairment severities while preserving the publisher’s configured throughput.** 

**_Index Terms_ —Data Distribution Service, middleware, quality of service, real-time systems, Robot Operating System** 

## I. INTRODUCTION 

Consider a scenario in which a mobile robot publishes laser scans at 30 Hz, while a remote visualization node receives the data over Wi-Fi. Packet loss triggers Data Distribution Service (DDS) retransmissions, and the publisher stalls, leaving local collision avoidance without fresh data. The slow-subscriber backpressure coupling problem arises in Robot Operating System 2 (ROS 2) systems using the DDS middleware [1]–[3]. 

The coupling comes from the writer’s handling of RELIABLE data. Samples remain in the writer history until all matched readers acknowledge them. A reader experiencing packet loss, limited bandwidth, or central processing unit (CPU) overload can leave samples unacknowledged. Once the history reaches its capacity, the publisher cannot write new samples. The writer blocks, the publisher drops messages, and healthy subscribers also see delayed delivery and reduced throughput [3], [4]. A degraded link affects every subscriber sharing that DDS writer. 

Using BEST <u>EFFORT</u> for all subscribers removes this coupling, but it also gives up the delivery guarantees needed by 

safety-critical local subscribers. Quality of service (QoS) settings applied per subscriber do not change the shared writer’s reliability policy, so a misconfigured or remote reader can still affect the pipeline. Differentiated Services (DiffServ) traffic prioritization has a different limitation: it operates on packets and does not use DDS semantics or subscriber criticality. 

Adaptive Bridge places a middleware-level proxy between the publisher and its subscribers. The proxy subscribes to the original topic and sends the data through two independent DDS output writers. The critical path uses RELIABLE QoS for subscribers such as local collision avoidance; the noncritical path uses BEST <u>EFFORT</u> QoS, for subscribers such as remote visualization. This two-writer arrangement implements _topic splitting_ and interrupts the backpressure chain at the application layer without changes to DDS internals, ROS 2 Middleware Interface (RMW) implementations, or the publisher node. The proxy also runs a classifier that uses active round-trip time (RTT) probes and hysteresis to monitor subscriber health and adjust noncritical rate limits when impairment is detected. 

The contributions of this work are: 

- 1) A proxy-based architecture for subscriber decoupling in ROS 2 that structurally isolates critical and noncritical data paths via independent DDS writers. 

- 2) An active-probe classifier with hysteresis for adaptive rate management on the noncritical path. 

- 3) A reproducible evaluation methodology using the Gilbert-Elliott bursty loss model on a Docker-based testbed with per-subscriber network impairment. 

- 4) Quantitative demonstration: publisher throughput preserved at 30 Hz (vs. a 29–36% collapse in baseline) and critical subscriber tail latency reduced from up to 15 s to 1.55 ms at p95 across all impairment levels. 

## II. RELATED WORK 

## _A. DDS QoS and Performance Characterization_ 

RELIABLE and BEST <u>EFFORT</u> delivery in DDS determine how writers and readers match and how long samples remain in writer history [3], [5]. Sciangula et al. derive formal bounds for DDS data delivery under real-time constraints [2]. Park et al. relate writer history depth to end-toend delay in an analytical ROS 2 model [6]. Measurements 

across ROS 2 middlewares and deployment scenarios report throughput variability [7], [8]. The characterization stops at the coupling problem; no application-layer mechanism is proposed to separate the coupled paths. 

## _B. Adaptive QoS and Middleware Adaptation_ 

Runtime DDS frameworks adjust reliability and durability policies as conditions change [9]. Per-stream scheduling priorities have also been used in publish-subscribe communication [10]. Real-Time Publish-Subscribe Protocol (RTPS)/DDSaware traffic handling has been studied for scalable wireless video streaming [11]. The changes occur at the publisher or transport level. Readers attached to the modified publisher still share one writer, so the policy change does not give each subscriber an independent data path or remove the shared reliability semantics. 

## _C. ROS 2 Real-Time and Backpressure Analysis_ 

Casini et al. examine response times in ROS 2 callback chains and analyze the impact of ROS 2 execution and scheduling behavior [12]. Luo et al. quantify the communication-delay effect in a multi-subscriber ROS 2 setting; their analysis demonstrates the coupling effect and its impact on end-to-end latency [4]. Middleware protocols for time-critical wireless transfer pursue similar throughput preservation goals, but operate below the ROS 2 application layer [13]. The analyses address the backpressure problem, and the protocol work addresses throughput at a lower layer. A deployable, noninvasive mitigation at the application layer is still absent. 

## _D. Contribution in Context_ 

Adaptive Bridge applies the mitigation at the ROS 2 application layer, without changes to DDS internals, RMW implementations, or publisher-side QoS reconfiguration. Its proxy places critical and noncritical subscribers on independent DDS writers, so the separation is in the writer structure rather than in a shared-writer QoS profile. The rate-control path uses active probes of per-subscriber network health and adjusts forwarding accordingly, instead of applying one static profile uniformly. 

## III. SYSTEM DESIGN 


Fig. 1. Adaptive Bridge architecture. The proxy receives the original topic and republishes it through two independent DDS writers. The classifier probes the slow subscriber and changes the noncritical forwarding rate. 

## _B. Topic Splitting – Isolation_ 

For an input such as /scan, the proxy publishes the received data through two independent DDS writers [3]. The critical writer uses RELIABLE QoS with KEEP <u>LAST</u> depth 10 and VOLATILE durability. The noncritical writer uses BEST <u>EFFORT</u> QoS with KEEP <u>LAST</u> depth 5. 

Each writer matches its own readers. A slow reader on the BEST <u>EFFORT</u> writer cannot backpressure the RELIABLE writer because the DDS entities have separate history queues and acknowledgment schedules. This provides separation at the DDS endpoint level; it does not tune per-subscriber QoS. The critical readers are local and fast, so acknowledgments for the critical writer are received promptly. The publisher-toproxy link does not accumulate unacknowledged samples, and the publisher is not blocked. 

Park et al.’s analytical DDS latency model [6] shows that writer history queue length dominates end-to-end delivery delay. Splitting the writers gives each reader group its own queue. The critical queue is determined by the number of critical readers, typically one or two. The DDS data-delivery bounds from Sciangula et al. [2] confirm that writer-level separation is the correct granularity for breaking backpressure. 

Classification changes later affect only routing decisions and rate limits inside the proxy. No publisher is destroyed or recreated at runtime. 

## _A. Architecture Overview_ 

Fig. 1 shows the arrangement of Adaptive Bridge, which has four components. The Proxy Node receives input topics and republishes them on two independent output topics, one critical and one noncritical. Active probes from the Classifier Node provide subscriber-health measurements, and the Classifier Node publishes the resulting classification decisions. The Policy Engine uses those decisions to set rate limits and drop policies. The Configuration Manager reads the YAML configuration at startup, when all publishers are also created. Pre-creating them avoids discovery churn and runtime race conditions. 

## _C. Classifier – Subscriber Health Monitoring_ 

The classifier assigns each subscriber a link-quality state from active probes and maintains a per-subscriber state machine with hysteresis (Fig. 2). 

**Probe mechanism.** Probe messages carry a sequence number. The proxy sends them at 5 Hz on a dedicated BEST <u>EFFORT</u> topic, and a responder at the subscriber returns the sequence number and timestamps. Over a sliding window of 50 samples (10 s), the classifier calculates mean round-trip time (RTT) and loss rate, where loss is the fraction of probes that receive no response. 


The noncritical path also applies the following policies: 

- **Stale-drop:** messages older than 200 ms (configurable) are discarded before forwarding. 

- **Queue-overflow protection:** all internal proxy queues are bounded; overflowing queues trigger backpressure on the noncritical path only. 

- **Critical priority:** critical forwarding is always performed first; noncritical forwarding may be queued, throttled, or dropped but never blocks critical delivery. 

## _E. Safety Supervisor_ 

A global state machine watches internal queue occupancy, callback processing lag, and error counts to track proxy health. As overload approaches, the supervisor enters DEGRADED mode: noncritical forwarding is suspended entirely, while the critical path is preserved. Under extreme failure conditions, it enters EMERGENCY mode, stops all forwarding, and publishes diagnostics. The supervisor prevents proxy overload from silently degrading critical-path delivery. 

## IV. EXPERIMENTAL METHODOLOGY 

Fig. 2. Classifier state machine. A state change requires threshold crossings over three consecutive classifier evaluations, while manual configuration overrides take precedence. 

**State machine.** A new subscriber starts in UNKNOWN. CRITICAL denotes a healthy subscriber whose data is forwarded at full rate through the critical writer. NONCRITICAL denotes a degraded subscriber whose data is ratelimited through the noncritical writer. UNKNOWN indicates insufficient probe data; it is treated as CRITICAL when allow_unknown_state is false. 

Two threshold sets govern transitions and prevent oscillation. Demotion from CRITICAL to NONCRITICAL occurs when RTT exceeds 50 ms or loss exceeds 1.5% for three consecutive classifier evaluations. Promotion back to CRITICAL requires RTT below 35 ms and loss below 0.5% over the same number of evaluations. A reading between the promotion and demotion thresholds leaves the state unchanged and resets the evaluation counters. A manual override in the YAML configuration forces the specified state regardless of probe data. 

The safety bias is explicit: misclassifying a critical subscriber as noncritical could drop safety-critical messages, whereas the reverse error only wastes bandwidth. The defaults and UNKNOWN handling reflect that bias. 

## _D. Policy Engine and Rate Limiting_ 

The Policy Engine selects forwarding behavior from the classifier state. In NORMAL mode, a CRITICAL subscriber receives all messages at the publisher’s native rate through the critical RELIABLE writer. The noncritical path still forwards at the configured 10 Hz, providing a view of the stream without saturating bandwidth. A NONCRITICAL subscriber enters DEGRADED mode, where the noncritical BEST <u>EFFORT</u> writer is limited to 3 Hz by a token-bucket rate limiter. 

## _A. Evaluation Goals_ 

The evaluation tests three hypotheses. Hypothesis 1 (H1) concerns the baseline: bursty wireless loss causes DDS backpressure, which degrades publisher throughput and subscriber latency. Hypothesis 2 (H2) concerns the proxy: topic splitting through an intermediary proxy removes this degradation for critical subscribers by breaking the writer-level coupling. Hypothesis 3 (H3) concerns adaptation: compared with static topic splitting, adaptive classification provides an additional benefit by reducing noncritical bandwidth during impairment. 

## _B. Testbed Setup_ 

As shown in Fig. 3, the testbed uses four Docker containers on a bridge network. One container publishes sensor_msgs/LaserScan messages at 30 Hz. In bridge experiments, a second container contains the proxy. The critical subscriber shares the local area network (LAN), while the slow subscriber represents a remote node subject to wireless impairment and runs a probe responder. 

Fast DDS Extensible Markup Language (XML) profiles enforce User Datagram Protocol (UDP)-only transport by disabling shared memory (SHM) and specifying only the User Datagram Protocol version 4 (UDPv4) transport descriptor [7]. DDS traffic therefore crosses the container’s network interface and is exposed to the tc rules. To reproduce the boundedpool behavior observed in default Fast DDS configurations, the writer resource limit is set to max_samples=200. 

Linux tc netem applies the network impairment using the Gilbert-Elliott two-state Markov loss model [14]–[18]. The model switches between a Good state with low loss and a Bad state with high burst loss according to state-transition probabilities. The impairment is applied only to the slowsubscriber path; the critical subscriber path remains pristine. Probe responses receive an asymmetric return-path impairment of 20 _±_ 10 ms to model return-path network delay. 


Fig. 3. Experimental testbed topology. Four containers on a Docker bridge network. tc netem applies Gilbert-Elliott loss on publisher egress, filtered to the slow subscriber’s Internet Protocol (IP) address only. 

use the ROS epoch clock. Publisher rate is computed from the number of publication attempts per 5-second window. To capture burst-driven throughput instability, rate standard deviation is computed over 5-second sliding windows. 

## V. RESULTS AND DISCUSSION 

## _A. Baseline: Confirming Backpressure (H1)_ 

Table II gives the baseline measurements. With no impairment, the publisher sustains 30.0 Hz with sub-millisecond latency. Under impairment, throughput collapses to 19.2– 21.4 Hz, a 29–36% drop, while critical-subscriber tail latency reaches 11.7–15.0 s. The 200-sample writer pool fills with unacknowledged samples as DDS backpressure develops, preventing the publisher from writing at its intended rate. The rate standard deviation of 8.5–8.7 Hz confirms burst-driven instability: slow-subscriber acknowledgments arrive as the pool fills and drains erratically. This simultaneous, measurable collapse in throughput and latency confirms H1 and results from DDS backpressure. 

TABLE II 

BASELINE RESULTS (NO BRIDGE) 

## _C. Impairment Parameters_ 

The four evaluated impairment levels and their resulting loss characteristics are given in Table I. 

|Scenario|Crit. p50 (ms)|Crit. p95 (ms)|Rate (Hz)|Rate std (Hz)|
|---|---|---|---|---|
|Clean|0.65|0.95|30.0|0.0|
|Mild|0.97|15,013|21.4|8.5|
|Moderate|0.97|11,666|21.4|8.7|
|Strong|1.02|15,043|19.2|8.7|


TABLE I 

GILBERT-ELLIOTT IMPAIRMENT PARAMETERS 

|Scenario|_p_ (G_→_B)|_r_ (B_→_G)|Good loss|Bad loss|Avg loss|
|---|---|---|---|---|---|
|Clean|–|–|–|–|0%|
|Mild|1%|15%|0.5%|30%|2.3%|
|Moderate|3%|15%|0.5%|40%|7.1%|
|Strong|2%|10%|1.0%|50%|9.2%|


Median latency remains near 1 ms because messages experience negligible queuing before the 200-sample pool cap is reached. Backpressure therefore appears primarily in tail latency and throughput: slowed acknowledgments fill the pool until publisher skips reduce the measured rate. 

## _B. Bridge: Eliminating the Coupling (H2)_ 

Impaired experiments run for 180 s and the clean experiment for 120 s, with up to approximately 5,400 latency samples at 30 Hz per run. The toggle experiment runs for 240 s, alternating impairment at 60 s intervals. 

## _D. Scenarios and Metrics_ 

The evaluation comprises ten experiments. Four are baseline runs, one for each impairment level, with no bridge. Five use the bridge with the classifier enabled. The remaining experiment is an ablation with the bridge present and the classifier disabled. The evaluation measures are critical-subscriber latency at p50 and p95, with p99 additionally reported for the cross-RMW comparison; publisher throughput rate and its standard deviation; noncritical-subscriber latency; and the classifier transition count. 

The evaluation uses fixed, version-controlled configurations and impairment parameters, and the complete orchestration and analysis scripts are provided to enable reproducibility of the reported scenarios. 

For each message, latency is the receive time minus the ROS message header timestamp; both publisher and subscriber 

TABLE III 

BRIDGE RESULTS (ADAPTIVE BRIDGE ENABLED) 

|Scenario|Crit. p50 (ms)|Crit. p95 (ms)|Rate (Hz)|Clf. trans.|
|---|---|---|---|---|
|Clean|1.07|1.51|30.0|5|
|Mild|1.09|1.55|30.0|2|
|Moderate|1.10|1.55|30.0|2|
|Strong|1.09|1.55|30.0|2|
|Toggle|1.11|1.57|30.0|9|
|Ablation|1.09|1.57|30.0|0|


Table III shows the Adaptive Bridge measurements. Publisher throughput remains 30.0 Hz across bridge runs, with 5 s windowed rate standard deviation of 0.0 Hz at the reported one-decimal resolution. Critical-subscriber p95 latency does not exceed 1.57 ms across bridge runs, compared with 15.0 s in the baseline. The publisher-to-proxy link remains unblocked, which is consistent with the proxy draining its queue and the writer pool not accumulating. 

The impaired runs show only two classifier transitions: after initial stabilization, sustained impairment causes a single 

demotion to NONCRITICAL, after which hysteresis prevents further changes. The clean run shows five transitions during startup and probe settling despite no network impairment; these affect only noncritical rate control and not the critical path. 

Under strong impairment, publisher throughput rises from 19.2 Hz to 30.0 Hz and critical p95 latency falls from 15,043 ms to 1.55 ms, a factor of approximately 9,700. In clean mode, the bridge hop adds approximately 0.4 ms, increasing p50 latency from 0.65 ms to 1.07 ms, which is small relative to the baseline latency and throughput loss. 

Topic splitting eliminates the backpressure coupling entirely: the slow subscriber and the critical subscriber use independent DDS writers. These measurements confirm H2. 

## _C. Cross-RMW Validation_ 

We repeated the evaluation matrix with Cyclone DDS (rmw_cyclonedds_cpp) under identical Gilbert-Elliott impairment conditions; Table IV reports the four bridge-enabled scenarios. This tests whether critical-path protection depends on Fast DDS; the harness switches RMW implementations with the --rmw flag without code changes. 

For both RMWs, Table IV shows critical subscriber p99 latency below 2 ms and publisher throughput at 30.0 Hz across all impairment levels. The bridge’s protection is RMWportable across both implementations. 

TABLE IV CROSS-RMW VALIDATION: BRIDGE SCENARIOS 

|Scenario|F-DDS crit p99 (ms)|C-DDS crit p99 (ms)|F-DDS rate (Hz)|C-DDS rate (Hz)|
|---|---|---|---|---|
|bridge<br>clean|1.7|1.9|30.0|30.0|
|bridge<br>mild|1.8|1.9|30.0|30.0|
|bridge<br>moderate|1.8|1.6|30.0|30.0|
|bridge<br>strong|1.8|1.6|30.0|30.0|


The two RMWs handle publish() differently when backpressure occurs. Fast DDS uses non-blocking publish(). Once the max_samples=200 writer pool is full, the call returns an error while the timer continues to fire; messages then accumulate as a backlog, and baseline critical p99 latency reaches 14,000–17,000 ms. Cyclone DDS uses blocking publish(). When its 600 KiB writer history cache fills, dds_write() blocks and prevents further message creation. No backlog forms, and critical p99 remains near 1 ms even under impairment. Fast DDS shows backpressure as an undelivered-message backlog, whereas Cyclone DDS shows it as reduced message generation. The topic-split architecture prevents the slow subscriber from causing backpressure in either implementation. 

Cyclone DDS required one transport-level configuration adjustment, AllowMulticast=spdp, to force unicast dataplane traffic. This aligned its default multicast distribution with the per-subscriber tc filter, analogous to Fast DDS’s explicit XML writer resource limits. 

## _D. Comparison Visualization_ 

Fig. 4 places critical subscriber p95 latency and publisher throughput side by side for the baseline and bridge at each impairment level. 


Fig. 4. Critical subscriber p95 latency (top) and publisher throughput (bottom) across impairment levels. The bridge removes the two manifestations of backpressure. The dashed line indicates the publisher’s 30 Hz target rate. 

Fig. 5 shows the critical subscriber latency cumulative distribution functions (CDFs) for both experimental conditions at all impairment levels. 


Fig. 5. **Critical** subscriber latency CDFs across all impairment levels. The top panel is the baseline, where tail latency increases with impairment (clean below 1 ms; impaired tails exceed 18 s). The bottom panel is Adaptive Bridge, where all four CDFs overlap near 1–2 ms, showing no observable effect of impairment on critical-path delivery. 

## _E. Ablation: Topic Splitting vs. Classification (H3)_ 

The ablation retained the topic split but disabled the classifier. Critical latency was p50=1.09 ms and p95=1.57 ms in the ablation, compared with p50=1.10 ms and p95=1.55 ms for bridge <u>moderate.</u> The two conditions are nearly identical, so the topic split alone provides the same critical latency benefit. 

The classifier changes the noncritical path: with the classifier disabled, noncritical traffic continues at 10 Hz during impairment, while with it enabled, the rate falls to 3 Hz during degraded periods. On a bandwidth-constrained Wi-Fi 

link, the reduction from 10 Hz to 3 Hz during deep fades saves approximately 70% of noncritical bandwidth and reduces proxy load and contention. 

H3 is partially confirmed. The classifier adds adaptive control of noncritical bandwidth but does not improve criticalpath protection beyond the static topic split. In the toggle experiment, impairment changed at 60 s intervals, producing 9 synchronized state transitions; detection and recovery occurred within approximately 20 s, consistent with the 10-second sliding window and three-evaluation hysteresis requirement. 

## VI. LIMITATIONS 

**Proxy overhead.** The bridge adds approximately 0.4 ms of latency. That overhead is negligible relative to the seconds of backpressure prevented by the bridge, but a proxy may become a bottleneck at high aggregate bandwidth. The evaluation focuses on network-induced backpressure and subscriber latency; CPU and memory overhead of the proxy were not independently measured and are therefore left for future evaluation. 

**Reactive classification.** The classifier detects sustained impairments within approximately 20 s from a 50-sample sliding window; intermittent impairment shorter than the evaluation window may not cause a state change. Predictive classification based on network trends remains future work. 

**RMW scope and message type.** The evaluation covers Fast DDS and Cyclone DDS under identical impairment conditions (see Section V-C). Both implementations achieve equivalent critical-path protection, with sub-2 ms p99 latency, despite their fundamentally different publish() semantics. Additional RMWs, such as RTI Connext, and larger message types, such as PointCloud2, remain to be evaluated. 

**Controlled network model.** The Gilbert-Elliott parameters in Table I are used to produce controlled, bursty loss. These parameters are not claimed to replicate any specific real-world Wi-Fi deployment. Validation against empirically measured Wi-Fi traces remains future work. 

**Single point of failure.** The Safety Supervisor monitors queue pressure, callback lag, and error counts and enters degraded or emergency modes under overload, but the proxy process remains a single point of failure. An external watchdog or redundant proxy configuration would improve resilience to process-level crashes. 

## VII. CONCLUSION 

The proxy-based topic split eliminates DDS backpressure coupling in mixed-criticality ROS 2 deployments. Across all impairment levels, the bridge preserves the 30 Hz publisher rate rather than the 29–36% baseline collapse and reduces critical-subscriber p95 latency from 11.7–15.0 s to 1.55 ms. Topic splitting supplies the critical-latency benefit, while the adaptive classifier manages bandwidth on the noncritical path but does not provide additional critical-path protection. 

The approach is deployable at the ROS 2 application layer without modifying DDS internals, RMW implementations, or the publisher node. Cross-RMW evaluation with Fast DDS and 

Cyclone DDS shows comparable critical-path protection under the evaluated impairments. Future work includes multi-proxy redundancy, evaluation across additional RMW implementations, and real-robot deployment validation. The complete implementation and configuration files are publicly available at the project repository [19], and the released ROS 2 package is indexed for the Jazzy distribution in the ROS Index [20]. 

## REFERENCES 

- [1] S. Macenski, T. Foote, B. Gerkey, C. Lalancette, and W. Woodall, “Robot Operating System 2: Design, architecture, and uses in the wild,” _Science Robotics_ , vol. 7, no. 66, p. eabm6074, May 2022. 

- [2] G. Sciangula, D. Casini, A. Biondi, C. Scordino, and M. Di Natale, “Bounding the data-delivery latency of DDS messages in real-time applications,” in _Proc. 35th Euromicro Conf. on Real-Time Systems (ECRTS)_ , Vienna, Austria, Jul. 2023, vol. 262, pp. 9:1–9:26. 

- [3] Object Management Group, _Data Distribution Service (DDS), Version 1.4_ , OMG Document Number formal/2015-04-10, Apr. 2015. 

- [4] X. Luo, X. Jiang, Y. Tang, H. Liang, N. Guan, and Y. Wang, “Analysis and optimization of communication delay in multi-subscriber environments of ROS 2,” _Journal of Systems Architecture_ , vol. 164, p. 103428, Jul. 2025. 

- [5] G. Pardo-Castellote, “OMG Data-Distribution Service: Architectural overview,” in _Proc. 23rd Int. Conf. Distributed Computing Systems Workshops (ICDCSW)_ , Providence, RI, USA, May 2003, pp. 200–206. 

- [6] H.-S. Park, S. Lee, D. Um, H. Ryu, and K.-J. Park, “An analytical latency model of the Data Distribution Service in ROS 2,” in _Proc. IEEE INFOCOM 2025_ , London, UK, May 2025, pp. 1–10. 

- [7] L. P. Chovet, G. M. Garcia, A. Bera, A. Richard, K. Yoshida, and M. A. Olivares-Mendez, “Performance comparison of ROS 2 middlewares for multi-robot mesh networks in planetary exploration,” _Journal of Intelligent & Robotic Systems_ , vol. 111, art. no. 18, Jan. 2025. 

- [8] Y. Maruyama, S. Kato, and T. Azumi, “Exploring the performance of ROS 2,” in _Proc. ACM Int. Conf. Embedded Software (EMSOFT)_ , Pittsburgh, PA, USA, Oct. 2016, pp. 5:1–5:10. 

- [9] J. F. Ingl´es-Romero, A. Romero-Garc´es, C. Vicente-Chicote, and J. Mart´ınez, “A model-driven approach to enable adaptive QoS in DDSbased middleware,” _IEEE Trans. Emerg. Topics Comput. Intell._ , vol. 1, no. 3, pp. 176–187, Jun. 2017. 

- [10] A. Paikan, D. Domenichelli, and L. Natale, “Communication channel prioritization in a publish-subscribe architecture,” in _Proc. IEEE Workshop on Software Engineering and Architectures for Realtime Interactive Systems (SEARIS)_ , Arles, France, Mar. 2015, pp. 41–45. 

- [11] B. Al-Madani, M. Al-Saeedi, and A. A. Al-Roubaiey, “Scalable wireless video streaming over Real-Time Publish-Subscribe Protocol (RTPS),” in _Proc. 17th IEEE/ACM Int. Symp. Distributed Simulation and Real Time Applications (DS-RT)_ , Delft, Netherlands, Oct. 2013, pp. 221–230. 

- [12] D. Casini, T. Blaß, I. L¨utkebohle, and B. B. Brandenburg, “Responsetime analysis of ROS 2 processing chains under reservation-based scheduling,” in _Proc. 31st Euromicro Conf. Real-Time Systems (ECRTS)_ , Stuttgart, Germany, Jul. 2019, vol. 133, pp. 6:1–6:23. 

- [13] J. Peeck, M. M¨ostl, T. Ishigooka, and R. Ernst, “A middleware protocol for time-critical wireless communication of large data samples,” in _IEEE Real-Time Syst. Symp. (RTSS)_ , Dec. 2021, pp. 1–13. 

- [14] S. Hemminger, “Network emulation with NetEm,” in _Proc. Linux Conf. Australia (LCA)_ , Canberra, Australia, Apr. 2005. 

- [15] A. Jurgelionis, J.-P. Laulajainen, M. Hirvonen, and A. I. Wang, “An empirical study of NetEm network emulation functionalities,” in _Proc. IEEE Int. Conf. Computer Communications and Networks (ICCCN)_ , Maui, HI, USA, Jul. 2011, pp. 1–6. 

- [16] E. N. Gilbert, “Capacity of a burst-noise channel,” _Bell System Technical Journal_ , vol. 39, no. 5, pp. 1253–1265, Sep. 1960. 

- [17] E. O. Elliott, “Estimates of error rates for codes on burst-noise channels,” _Bell System Technical Journal_ , vol. 42, no. 5, pp. 1977–1997, Sep. 1963. 

- [18] H. S. Wang and N. Moayeri, “Finite-state Markov channel – a useful model for radio communication channels,” _IEEE Trans. Veh. Technol._ , vol. 44, no. 1, pp. 163–171, Feb. 1995. 

- [19] K. Puwar, “Adaptive Bridge,” GitHub repository, 2026. [Online]. Available: https://github.com/KaushalrajPuwar/adaptive-bridge. 

- [20] K. Puwar, “adaptive <u>bridge,” ROS Index (Jazzy), 2026. [Online]. Avail-</u> able: https://index.ros.org/p/adaptive <u>bridge/#jazzy.</u> 

