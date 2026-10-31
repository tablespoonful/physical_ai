---
title: "Probabilistic Latency Analysis of the Data Distribution Service in ROS 2"
date: "2025-08-14"
authors: "Sanghoon Lee; Hyung-Seok Park; Jiyeong Chae; Kyung-Joon Park"
url: https://arxiv.org/abs/2508.10413
pdf: https://arxiv.org/pdf/2508.10413
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2508.10413)** / [論文ページ](https://arxiv.org/abs/2508.10413)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# Probabilistic Latency Analysis of the Data Distribution Service in ROS 2 

Sanghoon Lee , Hyung-Seok Park , Jiyeong Chae , and Kyung-Joon Park 

**_Abstract_ —Robot Operating System 2 (ROS 2) is now the de-facto standard for robotic communication, pairing UDP transport with the Data Distribution Service (DDS) publishsubscribe middleware. DDS achieves reliability through periodic heartbeats that solicit acknowledgments for missing samples and trigger selective retransmissions. In lossy wireless networks, the tight coupling among heartbeat period, IP fragmentation, and retransmission interval obscures end-to-end latency behavior and leaves practitioners with little guidance on how to tune these parameters. To address these challenges, we propose a probabilistic latency analysis (PLA) that analytically models the reliable transmission process of ROS 2 DDS communication using a discrete-state approach. By systematically analyzing both middleware-level and transport-level events, PLA computes the steady-state probability distribution of unacknowledged messages and the retransmission latency. We validate our PLA across 270 scenarios, exploring variations in packet delivery ratios, message sizes, and both publishing and retransmission intervals, demonstrating a close alignment between analytical predictions and experimental results. Our findings establish a theoretical basis to systematically optimize reliability, latency, and performance in wireless industrial robotics.** 

**_Index Terms_ —DDS (Data Distribution Service), Latency Analysis, Probabilistic Modeling, Quality of Service (QoS), ROS 2 (Robot Operating System 2)** 

## I. INTRODUCTION 

Communication has become an increasingly critical factor in modern robotics. Conventional fixed-station robots have long relied on wired links-such as Ethernet-based fieldbusesfor control and data exchange, benefiting from their stability and low latency. For mobile robots and multi-robot systems, however, the need to cut the tether and adopt wireless communication is rapidly growing [1]. Wireless links not only expand a robot’s mobility but also enable remote control that circumvents on-board computing constraints; they are especially indispensable in environments where cabling is impractical. Guaranteeing timely communication and predicting latency under diverse network conditions are therefore essential to the stability and efficiency of robotic systems [2], yet research on wireless networking within the robotics community remains comparatively limited. 

Recently, the robotics community is rapidly adopting the Robot Operating System (ROS) framework, known for its flexibility and rich ecosystem, to accommodate increasingly complex and distributed robotic systems. In particular, ROS 2 is designed with real-time, networked deployments in mind, making it the de facto standard for many modern robotic 

S. Lee, H.-S. Park, J. Chae, and K.-J. Park are with DGIST, Daegu, Korea (e-mail: leesh2913@dgist.ac.kr; hyungseok@dgist.ac.kr; cowldud3@dgist.ac.kr; kjp@dgist.ac.kr). 

applications [3]. For its message handling, ROS 2 relies on the Data Distribution Service (DDS), which operates atop the UDP protocol using the Real-Time Publish-Subscribe (RTPS) standard. This DDS protocol enables a real-time publish/subscribe architecture and distributed design to facilitate low-latency, peer-to-peer data exchange between robotic controllers and sensors [4]. Furthermore, DDS offers a wide range of configurable parameters, including Quality of Service (QoS) policies and User Transport settings. These configurations support diverse scenarios, ranging from high-speed, loss-tolerant data transmissions to mission-critical messages requiring guaranteed delivery. As a result, ROS 2 DDS has emerged as a vital infrastructure for robotic applications in which different data streams have varying requirements for reliability and latency. 

Despite the advantages of ROS 2 DDS, new challenges have emerged for DDS-based communication in deployments that rely on wireless networks. The acknowledgment and retransmission mechanisms DDS employs for reliability add significant complexity in lossy wireless environments. Although DDS offers reliable delivery through QoS profiles, there have been few studies that theoretically analyze the timing behavior and delays induced by retransmissions. Consequently, practitioners and researchers still depend largely on empirical testing in the absence of systematic methodologies [5]. Network latency is a critical factor in robotic applications, and this concern becomes even more pronounced over wireless links [6]. Nevertheless, ROS 2 DDS still lacks a systematic methodology for predicting how wireless link quality influences retransmission latency. 

In this paper, we propose a probabilistic latency analysis (PLA) for ROS 2 DDS communication. Our main contributions are as follows: 

- We conduct a systematic analysis of ROS 2 DDS communication under strict reliability requirements. Specifically, we model the transmission of an ROS 2 sample from the publisher to the subscriber as a probabilistic process, representing it through a discrete-state framework. Note that our approach spans both middleware-level and transportlevel operations. 

- Building on this discrete-state model, we introduce the PLA algorithm, which computes the steady-state probabilities and delays in DDS-based reliable communication. PLA leverages dynamic programming to derive the distributions of unacked messages and retransmission latencies under any given packet loss ratio. 

- We validate PLA’s accuracy and robustness through 270 scenarios, covering the packet loss ratio, message sizes, publishing rates, and retransmission intervals. Our exper- 

2 

imental results show mean errors of 0.91%, 1.82%, and 4.57% for the message delivery ratio, average latency, and jitter, respectively, which are closely aligned with the experimental values. 

The remainder of this paper is organized as follows. Section II reviews the relevant literature. Section III describes the RTPS standard and reliability mechanisms in DDS. In Section IV, we detail our PLA model design. Section V provides extensive experimental validation. Finally, Section VI concludes the paper. 

## II. RELATED WORK 

Existing analytical models of ROS 2 DDS-based communication commonly assume a perfect network with no packet loss or unpredictable delay. One study [7] presents a formal DDS model and performs a real-time schedulability analysis to bound end-to-end latency in ROS 2, yet it presumes an ideal, deterministic network that ignores wireless uncertainties like packet loss. Another paper [8] explores ROS 2 DDS latency at the intra- or inter-process level on a single host, proposing an analytical approach to upper-bound software-stack delays. While this process-level view is valuable for understanding ROS 2 overhead, it assumes messages are instantly delivered by the network layer, leaving additional delays and jitter from non-deterministic wireless links unmodeled. 

Given the complexity of theoretical latency analyses that include network effects, many researchers have relied on experimental methods to measure ROS 2 DDS latency in diverse settings. One study [5] evaluates ROS 2 overhead by varying parameters such as message frequency, size, and DDS vendor choice, but its purely empirical approach lacks a general latency model and focuses on worst-case latency rather than probabilistic delay distributions. Other work [9] examines ROS 2 DDS performance in wireless swarms, reporting mean latencies and distributions through a physical testbed. These experiments reveal the influence of QoS on delay but offer only scenario-specific insights without proposing a theoretical foundation. Another paper [10] investigates ROS 2 DDS with large messages, showing that reliable transmission can generate burst traffic and increase latency and jitter. While this finding highlights a key cause of extreme latency, it remains purely experimental and does not provide a predictive model of behavior. 

One study [11] provides closed-form analyses of DDS retransmission delays by modeling data transmission at the ROS 2 layer with a single success probability _p_ for each message. This abstraction assumes that all fragmentation occurs below the ROS 2 layer and thus does not explicitly capture the effects of RTPS/UDP-level fragmentation. As a result, it is only applicable to very small ROS 2 message sizes for which fragmentation does not occur. 

In summary, most ROS 2 DDS latency studies rely on analytical models under restrictive assumptions or remain constrained by specific experimental setups. Although previous research acknowledges the added complexity of wireless scenarios, no general theoretical analysis have emerged. This work develops a robust model of DDS retransmission delays 

in lossy networks. Compared to wired environments, wireless channels are vulnerable to interference and packet loss, leading to significant delay and jitter variations [12]. Without an appropriate analytical framework, quantifying latency probabilities in wireless robotic systems is difficult. Hence, we propose an analytical approach for ROS 2 DDS that accommodates probabilistic latency in wireless contexts and validate its accuracy through extensive experiments. 

## III. PRELIMINARIES 

In this section, we provide preliminary knowledge about how data is transmitted within ROS 2 and outline the retransmission mechanism that ensures reliable delivery. 

## _A. Data Transmission Process in ROS 2_ 

At the ROS 2 level, data transmission occurs when nodes exchange messages on a specific topic. A topic identifies the unique message type shared by a publisher (sending messages) and a subscriber (receiving messages). Each ROS 2 node on a separate host generally corresponds to a DDS participant. Because DDS uses a decentralized, peer-to-peer architecture, nodes automatically discover and communicate without explicit IP addresses. Once nodes discover each other, they begin exchanging data through DDS. Whenever a node publishes a ROS 2 message, DDS multicasts it to every subscriber on that topic. In multi-host scenarios, DDS typically employs the RTPS protocol over UDP for data transmission. Although DDS can use shared memory when nodes run on the same host, this work focuses on nodes executing on different hosts. 

Then suppose Node A (publisher) intends to send a message on a specific topic to Node B (subscriber). After discovery completes, Node A and Node B are aware of each other. Figure 1 shows how a ROS 2 message travels from Node A to Node B, which can be divided into the following steps: 


Fig. 1. Data Transmission Process in ROS 2 

- 1) **Application Layer: ROS 2 Message** 

   - When Node A publishes a ROS 2 message, it is serialized into a binary format for DDS. An RTPS header is then attached, and if the message is large, DDS may split it into multiple RTPS sub-messages. 

- 2) **Middleware Layer: RTPS Message** 

   - The RTPS message (or sub-messages) is further encapsulated for network transport. A UDP header is added, 

3 

and due to MTU constraints at the IP layer, the message may be split across multiple UDP datagrams. This can lead to IP fragmentation when transmitting larger RTPS messages. 

- 3) **Transport Layer: UDP Datagram** The resulting UDP packets are sent via network to all IP addresses in the relevant multicast group. If the RTPS message is large, it may be distributed across multiple UDP packets. 

- 4) **Reception and Reconstruction** Since Node B (subscriber) has indicated interest in receiving data on the same topic, it listens for RTPS packets on the corresponding UDP port. When these packets arrive from Node A, Node B’s DDS layer reassembles them into the original RTPS message. If the RTPS message was split across multiple datagrams, DDS collects all fragments and verifies data integrity by examining the RTPS headers. After confirming that all parts are successfully received and intact, the DDS middleware deserializes the data back into the ROS 2 message format and delivers it to Node B. 

Through these steps, a message from Node A is delivered to Node B. Most packet loss occurs at the transport layer, where UDP datagrams can be dropped. The next subsection outlines DDS reliability mechanisms that ensure complete data delivery, even if Node B initially fails to receive some packets. 

## _B. Reliability Mechanism of DDS_ 

DDS primarily relies on UDP, which does not inherently guarantee reliable delivery. Therefore, DDS includes its own reliability mechanism to ensure messages can be transmitted reliably when needed. This mechanism operates through acknowledgment and retransmission protocols, governed by QoS policies. Two key QoS policies involved in DDS reliability are Reliability and History. 

**Reliability QoS** governs retransmissions, offering two key modes: Best-Effort and Reliable. Best-Effort mode sends messages without acknowledgment, so a lost UDP packet means the subscriber never sees that message. Reliable mode confirms each message is received, retransmitting as needed until the subscriber acknowledges it. Hence, if the network eventually delivers the packets, all messages reach the subscriber. 

**History QoS** controls how published messages are stored for potential retransmission, offering two modes: KEEP(N) and KEEP ALL. KEEP(N) retains only the most recent N messages for a topic. KEEP ALL stores every message in memory, enabling full recovery if reliability requires it. Hence, a topic with “Reliability = Reliable” and “History = KEEP ALL” seeks complete delivery in order, here referred to as strict reliability. 

Under strict reliability, DDS employs additional RTPS messages (heartbeats and AckNack) to ensure delivery. As depicted in Figure 2, this process can be visualized as a loop between the publisher and subscriber: 

1) **Publisher sends and stores ROS 2 message:** 


Fig. 2. Heartbeat and AckNack Process in DDS (Green: Acked state, Red: Unacked state) 

The publisher publish a ROS 2 message and keeps a copy in its memory cache. Delivery of the ROS 2 message follows the process in the subsection III-A. 

- 2) **Publisher sends heartbeat messages:** The publisher’s DDS layer periodically sends heartbeat messages (RTPS packets) to all subscribers, informing them of the latest ROS 2 message sequence number and triggering acknowledgments. 

- 3) **Subscriber detects loss and sends AckNack:** Upon receiving a heartbeat, the subscriber always sends an AckNack message to the publisher, indicating whether any sequences are missing. If one or more sequences are lost, the subscriber requests those missing fragments, for example, “Please resend fragment #11 of ROS 2 message #3.” If all sequences are present, the AckNack simply serves as a positive acknowledgment. 

- 4) **Publisher retransmits lost data:** After receiving the AckNack, the publisher retransmits any messages (or fragments) the subscriber reported missing. This recovers lost data and fulfills the reliability guarantee. Steps 2, 3, and 4 repeat as long as there are unacknowledged or newly published messages. 

Through these mechanisms, DDS establishes a reliability layer over UDP, enabling ROS 2 to leverage UDP’s performance while achieving TCP-like reliability when necessary. A critical point to note is that a single ROS 2 message may be fragmented at both the middleware and transport layers, yet DDS remains unaware of any fragmentation that occurs at the transport level. This makes DDS prone to problems with large data in lossy networks. For example, if the RTPS message size limit is 64 KB and the UDP MTU is 1.5 KB, transmitting a single RTPS message can require up to 32 UDP packets. Losing just one packet forces DDS to retransmit the entire RTPS message, causing all 32 packets to be resent. 

A previous study [10] reports that sending large-scale data over DDS can trigger burst traffic in lossy networks but does not clarify the underlying cause. We pinpoint DDS’s lack of fragmentation awareness as the key factor behind these bursts. To alleviate retransmission-induced burst traffic, we recommend setting the maximum RTPS message size slightly below the UDP MTU. Although this approach adds minor 

4 

overhead from repeating RTPS headers, it effectively prevents bursts in lossy networks. 

## IV. PROBABILISTIC LATENCY ANALYSIS MODEL 

In this section, we propose a PLA model to probabilistically estimate the reliability and latency of a DDS publishsubscribe system in lossy wireless networks. When a ROS 2 message requires retransmission, DDS may split it into multiple packets, each independently subject to loss. However, during each heartbeat-AckNack cycle that determines retransmissions, DDS triggers only one heartbeat at the system level, irrespective of how many packets require resending. This complexity makes it difficult to derive a closed-form expression for DDS reliability. 

To address this issue, we treat publish and heartbeat events as probabilistic operators that update the discrete distribution of unacked RTPS messages, then use a dynamic programming approach to estimate latency. Subsection IV-A defines the assumptions of our model. Subsection IV-B models these events in a discrete state space. Next, Subsection IV-C shows that the DDS system converges to a steady state. Finally, Subsection IV-C presents the proposed latency analysis model. 

## _A. Assumptions_ 

In this subsection, we introduce the assumptions underlying our model. We model DDS system based on three main assumptions, which are as follows: 

- 1) **Strict Reliability (Reliable, KEEP ALL)** 

We assume that all messages from the publisher eventually arrive at the subscriber without any loss, ensuring strict reliability. Reliability QoS is set to RELIABLE, retransmitting data until it is received, and History QoS is KEEP ALL, storing every item the publisher sends. Thus, no messages are discarded, as DDS will continue sending until each one is acknowledged. 

- 2) **Avoiding UDP Fragmentation of RTPS Messages** DDS does not recognize fragmentation at the transport layer, so if a single RTPS message spans multiple UDP packets, the entire message is retransmitted whenever a packet is lost. This behavior can cause bursts of retransmissions leading to queue saturation. To avoid this, we set the maximum RTPS message size slightly below the UDP MTU, preventing fragmentation at the transport level. 

- 3) **Excluding Transmission Delay** 

   - This study focuses on probabilistically estimating how packet loss and retransmission over wireless links affect latency. For simplicity, we do not consider any transmission delay or additional latency due to queue saturation in DDS or UDP. Thus, potential queuing delays in transmitters, as well as physical delays of a few hundred microseconds to several milliseconds, are excluded. 

## _B. DDS Event Model_ 

In this section, we describe how the two types of DDS events, (1) the publish event and (2) the heartbeat event, 

affect the probability distribution of unacked messages. The proposed probabilistic model operates in discrete time (eventdriven), updating the probability distribution 


whenever an event occurs. Here, _Pk_ = _p_ ( _X_ = _k_ ) _,_ where _X_ is the random variable denoting the number of unacked RTPS messages, represents the probability that there are _k_ unacked messages immediately after the event. 

_1) Publish Event:_ A DDS publisher begins sending ROS 2 messages to a subscriber at time 0 ms, repeating every _r_ ms. We call each transmission a publish event, where the _i_ th publish event occurs at 


Depending on the ROS 2 message size and the UDP MTU, the message may be split into _m_ UDP packets. We define _m_ as the ratio of the total message size to the MTU: _m_ = _<u>m</u>_ MTUtotal<sup>_._</sup> For simplicity, we assume _m_ or its reciprocal is always an integer, so each message is a multiple or divisor of the MTU. Hence, the number of UDP packets for a single publish is 


The ROS 2 message is thus divided into _u_ UDP packets. Each packet is independently lost with probability 1 _− p_ , so the probability that exactly _x_ out of _y_ packets fail is given by the binomial distribution: 


After one publish event, the probability of having _k_ unacked messages is the convolution of the distribution _P_ with Prfail: 


Because a negative number of unacked packets is physically impossible, we set _Pn_ = 0 for _n <_ 0. Thus, the change in _P_ , driven by a single publish event can be written as 


Upon receiving a heartbeat, the subscriber detects any missing messages and sends an AckNack, prompting the publisher to retransmit. Both the heartbeat and AckNack must arrive successfully (probability _p_<sup>2</sup> ) for retransmission to occur; otherwise (with probability 1 _−p_<sup>2</sup> ), no retransmission takes place. When retransmission occurs, the publisher batches unacked messages until reaching the RTPS message’s maximum size, assumed close to the UDP MTU. Hence, one UDP packet can carry up to _M_ = � _m_ <u>1</u> � messages. Retransmitting _x_ unacked messages then needs _f_ = � _Mx_ � UDP packets. 

5 

We define Γ( _x → k_ ) as the probability that _x_ unacked messages become _k_ after retransmission, determined by: 


- **Case 2:** _x > k_ and _x_ mod _M_ = 0. 


Otherwise, if _Mk_<sup>_∈/_Z,Γ(</sup><sup>_x →k_) = 0.</sup> 

- **Case 3:** _x > k_ and _x_ mod _M_ = _n̸_ = 0. Messages are sent in ( _f −_ 1) full packets plus one residual packet of size _n_ . Two sub-cases arise: 


Combining these cases, the probability that there are _k_ unacked messages after one heartbeat is 


where _δx,k_ is the Kronecker delta (1 if _x_ = _k_ , 0 otherwise) and Γ( _x → k_ ) is given by the cases above. Thus, the change in _P_ , driven by a single heartbeat event can be written as 


## _C. Steady-State Distributions_ 

This section shows that the probability distribution _P_ of unacked messages eventually reaches a steady state. The operators Pub( _P_ ) and Hb( _P_ ) from Subsection IV-B update _P_ whenever a publish or heartbeat occurs, i.e., _P ←_ Pub( _P_ ) for a publish event, or _P ←_ Hb( _P_ ) for a heartbeat event. We can treat DDS system as a discrete-time Markov chain whose distribution _P_ changes over time, depending only on the previous state and the event type. For a wireless link with _p >_ 0, the probability that _k →∞_ (unbounded unacked messages) is negligible. Hence, _P_ has an effectively finite state space and only two event types, forming a finite-state Markov chain. A finite-state Markov chain converges to a fixed distribution or a finite cycle. Under repeated events, the DDS model settles into a periodic behavior for _P_ . We refer to this periodic distribution as steady-state distributions, meaning _P_ returns periodically to the same (or nearly the same) value. 

In a DDS publish-subscribe system where publish and heartbeat occur periodically at intervals _r_ and _h_ , respectively, we define steady-state distributions _Q_ , the steady-state distributions after publish events, repeating with period _R_ : 


We can approximate _Q_ by simulating discrete events over a long horizon, as in Algorithm 1, using a dynamic programming approach to update _P_ and _Q_ each step. For large integers _t_ and _k_ max (e.g., _t >_ 20 _r_ , _k_ max _≈_ 10 _m_ ), the algorithm repeat updating _P_ and _Q_ until convergence yields the steady-state distributions. 

## **Algorithm 1:** Steady-State Distributions Computation 

## **Input:** 

_m_ (ratio of message size to MTU), _r_ (Publish period), _h_ (Heartbeat period) _p_ (Packet delivery rate) **Output:** _Q_ (steady-state distributions) 

## **Step 1: Event Timeline Construction** 


_E ←_ sort _E_ in ascending order 


**Step 3: Main Loop** 

**for** _e ∈E_ **do** 


**end** 

**Step 4: Return** _<u>Q</u> ←_ _<u>Q</u>_<sup>(new)</sup> 

Figure 3 shows how _P_ 0 changes during Algorithm 1. We see that _P_ converges to its steady-state distributions, with _P_ 0 stabilizing after about 10 publish events in all three scenarios. As noted in (9), the steady-state probabilities repeat with period _R_ =<sup>LCM</sup> _r_<sup><u>(</u></sup><sup>_r,h_</sup><sup><u>)</u></sup> . For instance, if _r_ = 50 and _h_ = 200, the steady-state cycle has period 4, whereas _r_ = 100 and _h_ = 200 gives period 2, and _r_ = 200 and _h_ = 200 yields no cycle. 

6 


Fig. 3. Change in _P_ 0 according to the Steady-State Distributions Computation 

## _D. Latency Analysis_ 

Building on the steady-state distributions _Q_ , we can estimate metrics such as message delivery ratio (MDR), average latency, and jitter for a given DDS system. This section describes how to derive MDR, average latency, and jitter. 

_1) Message Delivery Ratio (MDR):_ In the steady-state distributions _Q_ = � _P_<sup>(1)</sup> _, P_<sup>(2)</sup> _, . . . , P_<sup>(</sup><sup>_R_)�</sup> _,_ each _P_<sup>(</sup><sup>_n_)</sup> is the distribution of unacked messages right after a publish event. In particular, _P_ 0<sup>(</sup><sup>_n_)</sup> represents the probability that there are zero unacked messages, meaning all messages have been received (acked). We approximate the MDR by taking the average of _P_ 0<sup>(</sup><sup>_n_)</sup> over all distributions in _Q_ : 


_2) Average Latency:_ We propose a method to estimate average latency in a DDS system by computing, for each distribution _P_<sup>(</sup><sup>_n_)</sup> _∈ Q_ , the expected time for additional Hb operations to bring _P_ 0 _≃_ 100. First, consider _P_ at a point immediately after a publish event. _P_ 0 _>_ 0 denotes a positive probability that no messages remain unacked, then the latency in that case is zero. When heartbeats occur repeatedly, the probability that the next retransmission completes all unacked messages can be seen as the likelihood that every nonzero state in _P_ transitions into _P_ 0, where no unacked messages remain. 


where Hb() is the operator defined in eq. 8, yielding the distribution after one heartbeat event from a previous distribution. If the heartbeat period is _h_ ms, then the time until the _v_ -th heartbeat is 


where _tc_ is the average offset from the current publish event to the first heartbeat, and can depend on _n_ . Hence, the average latency of _P_<sup>(</sup><sup>_n_)</sup> is 


In the steady-state distributions _Q_ , each _P_<sup>(</sup><sup>_n_)</sup> occurs equally. Therefore, the overall average latency of the DDS system is approximated by averaging _L_ � _P_<sup>(</sup><sup>_n_)�</sup> over all _n_ : 


In this work, _tc_ depends on how the publish period _r_ and heartbeat period _h_ interact. To approximate _tc_ , we consider three key properties of the heartbeat mechanism: 

- 1) The actual heartbeat period is roughly 0.2 ms longer than its nominal setting. 

- 2) If all data have been acknowledged, heartbeat transmissions stop until the next publish event. 

- 3) Once heartbeat stops, restarting it requires an offset of _h_ ms. If a new publish arrives in an acked state, the first heartbeat is delayed by _h_ ms. 

Taking these properties into account, we refer to Appendix A for a detailed approximation of _tc_ depending on the relationship between _r_ and _h_ . 

_3) Jitter:_ Finally, we discuss estimating jitter, defined here as how much each latency varies from the average latency. It is equivalent to the standard deviation of the latencies across _Q_ . Thus, if we denote Std� _L_ ( _Q_ )� as the jitter, we have 


## V. EXPERIMENTAL EVALUATION 

In this section, we evaluate how accurately the proposed PLA model reflects actual communication behaviors in ROS 2 environments. The experiments are carried out on two computers running ROS 2 Humble (Fast DDS), directly connected via Ethernet. A total of 270 scenarios are considered by varying parameters such as packet delivery rates, message sizes, publishing intervals, and retransmission intervals. We compare the PLA model’s predicted results-including the Message Delivery Ratio (MDR), average latency, and jitterwith their corresponding experimental measurements. 

## _A. Experimental Environment_ 

The experimental setup consists of two computers, each equipped with a Realtek RTL8153 NIC, connected directly 

7 

via Ethernet to minimize external latency and unintentional packet loss. Both systems run Ubuntu 22.04 LTS and use ROS 2 Humble with eProsima’s Fast DDS as the underlying middleware. One computer acts as a ROS 2 publisher, while the other functions as a ROS 2 subscriber. 

We intentionally selected a wired link to maintain strict experimental control. In preliminary 802.11ax Wi-Fi testsconducted late at night in an isolated laboratory-we observed background loss below 0.1 percent as long as channel utilisation remained below saturation. Nevertheless, the transmission-delay distribution was wide and highly sensitive to external interference. Because our goal is to quantify the latency and jitter that arise when a link degrades to specific loss ratios, we require a channel in which the injected loss rate is the only variable and the transmission delay distribution is stable. A direct Ethernet connection meets these requirements. Moreover, our experiments do not assume network saturation (i.e., traffic exceeding available bandwidth), so the practical difference between Ethernet and Wi-Fi in this study lies only in Wi-Fi’s more variable transmission delay distribution-an aspect that is orthogonal to the system model presented in this paper. 

## _B. Parameter Settings_ 

DDS QoS parameters are configured for strict reliability, following Section IV-A. The publisher sends an array of uint32 data, totaling _m_ total bytes, at a fixed interval _r_ ms over a link with packet delivery rate _p_ . The packet delivery rate _p_ is artificially adjusted via the Linux tc command. Heartbeat messages are sent every _h_ ms. With a default MTU of 1.5 kB, the maximum ROS 2 message that fits in a single UDP datagram (including RTPS headers) is 1322 B, so _m_ total _∈{_ 12 _,_ 661 _,_ 1322 _,_ 3966 _,_ 13220 _}_ B. Table I summarizes the main parameters. The ratio _m_ (message-to-MTU) and the publish interval _r_ are controlled at the ROS 2 application layer, whereas the heartbeat interval _h_ is set in an XML file before ROS 2 node starts. 

TABLE I 

EXPERIMENTAL PARAMETER SETTINGS 

|**Parameter**|**Values**|
|---|---|
|Message-to-MTU ratio (_m_)|0.008, 0.5, 1, 3, 5, 10|
|Publish interval (_r_)|50 ms, 100 ms, 200 ms|
|Heartbeat interval (_h_)|50 ms, 100 ms, 200 ms|
|Packet delivery rate (_p_)|0.95, 0.9, 0.85, 0.80, 0.75|


## _C. Experimental Results_ 

Each of the 270 parameter scenarios undergoes 5,000 transmissions of ROS 2 messages. For each transmission, we record the message publication time _T_ pub at the publisher and its arrival time _T_ arrive at the subscriber, then compute delay ∆= _T_ arrive _− T_ pub. Delays of 0–3 ms, typical in networking, are treated as zero. Accordingly, the measured MDR is the fraction of transmissions with zero delay among 5000. We compute average latency and jitter as the mean and standard deviation of these 5000 delay values. 

We compare analytical and experimental MDR, average latency, and jitter. Figure 4 shows the case _r_ = 100 ms, _h_ = 200 ms, with the experimental trend (dotted) and the PLA-based analytic trend (solid). As _p_ rises, MDR increases, while average latency and jitter decline. All three metrics align closely between analytics and experiments, confirming the PLA approach’s reliability. 


Fig. 4. Comparison between Analytical and Experimental result ( _r_ = 100 _, h_ = 200) 

Appendix B presents comprehensive experimental results for all 270 scenarios, comparing analytical values with experimental measurements for MDR, average latency, and jitter. We report absolute error for MDR and relative error (in %) for average latency and jitter. Table II gives a concise summary of these comparisons. These results show minimal discrepancy 

8 


Fig. 5. The impact of _h_ and _m_ on the DDS system ( _r_ = 500 _, p_ = 0 _._ 85) 

TABLE II 

SUMMARY OF PERFORMANCE METRICS COMPARISON 

|**Metric**|**Average Error**|**Error Std**|
|---|---|---|
|MDR|0.91|0.85|
|Average Latency|1.82|2.40|
|Jitter|4.57|4.99|


between analytical and experimental values across all metrics, reflected in small average errors and low standard deviations. In particular, average errors for MDR, latency, and jitter are 0.91%, 1.82%, and 4.57%, respectively, with consistently low deviations. This consistency indicates our analytical model closely matches the experimental data. 

We analyzed how _m_ and _h_ affect a DDS system, given fixed _r_ and _p_ . Figure 5 illustrates how MDR, average latency, and jitter vary with _m_ and _h_ when _r_ = 500 and _p_ = 0 _._ 85. In these plots, blue denotes low gradients, and red indicates steep gradients. 

MDR is driven more by the fragmentation that occurs during publish events than by the heartbeat interval, which explains why changes in _m_ have a greater impact on successful message delivery than changes in _h_ . As _m_ increases from 1 to 5, MDR drops sharply and then gradually approaches zero. This suggests that DDS publish events are more prone to failure on lossy networks when they must handle large, fragmented messages. Hence, keeping _m ≤_ 5 proves advantageous for preserving MDR. 

Average latency and jitter are jointly influenced by both _m_ and _h_ , but in this case they are more sensitive to _h_ than to _m_ . As _h_ increases, both metrics grow almost linearly. Interestingly, when _h_ = 250 (i.e., _h_ = _r/_ 2), a local convex pattern emerges. This is explained by the heartbeat’s behavior: once there are no unacked messages, the heartbeat stops and resumes with an offset of _h_ . At _h_ = 250, half the time the offset is zero and half the time it is 250, whereas at _h_ = 200, the offset is consistently _h_ = 200. Thus, setting _h_ to _r/_ 2 proves to be a highly effective way to reduce delay. Meanwhile, with respect to _m_ , average latency and jitter undergo a steep initial rise from _m_ = 1 to _m_ = 5, then increase more gradually. This trend parallels the MDR results, again suggesting that keeping _m ≤_ 5—and ideally _m ≤_ 1—is beneficial for minimizing latency. 

VI. CONCLUSION 

In this paper, we have proposed a PLA model for ROS 2 DDS communication under strict reliability. Our model tracks the journey of a ROS 2 message from publisher to subscriber as a discrete-state process across both the middleware and the transport layers, yielding the distribution of unacked messages and delays under given network conditions. We have validated the proposed PLA in 270 scenarios with varied packet delivery rates, message sizes, publish intervals, and retransmission intervals. The mean errors for MDR, latency, and jitter are 0.91%, 1.82%, and 4.57%, respectively, aligning well with experiments. This extensive validation suggests that our model can be generalized to real-world DDS deployments. 

Several key insights emerge from PLA. First, to sustain higher MDR and reduce latency, keeping message sizes at or below the MTU (or at most 5 times larger) helps mitigate fragmentation overhead. Second, setting the heartbeat period to half the publish interval is highly cost-effective, as shown by our heartbeat analysis. These findings, as the first theoretical study of DDS latency in a lossy network, offer a foundation for optimizing ROS 2 DDS QoS parameters. Future guidelines built on this work will aid practitioners in designing more resilient robot networks with ROS 2 and spur further research into DDS-based systems. 

Currently, our approach does not capture packet loss from collisions, queue saturation, or bandwidth constraints. In practice, DDS may experience divergent delays under heavier traffic if queue overflows or collisions rise. Future work will extend PLA with traffic modeling in lossy networks, incorporating queue buildup and bandwidth saturation to further refine predictions and strengthen QoS configurations. 

9 

REFERENCES 

- [1] J. Chae, S. Lee, J. Jang, S. Hong, and K.-J. Park, “A survey and perspective on industrial cyber-physical systems (ICPS): From ICPS to AI-augmented ICPS,” _IEEE Transactions on Industrial Cyber-Physical Systems_ , vol. 1, pp. 257–272, 2023. 

- [2] H. Lv, Z. Pang, K. Bhimavarapu, and G. Yang, “Impacts of wireless on robot control: The network hardware-in-the-loop simulation framework and real-life comparisons,” _IEEE Transactions on Industrial Informatics_ , vol. 19, no. 9, pp. 9255–9265, 2022. 

- [3] V. Petrone, E. Ferrentino, and P. Chiacchio, “The dynamic model of the UR10 robot and its ROS2 integration,” _IEEE Transactions on Industrial Informatics_ , pp. 1–11, 2025. 

- [4] R. Kurte, Z. Salcic, I. Kevin, and K. Wang, “A distributed service framework for the Internet of Things,” _IEEE Transactions on Industrial Informatics_ , vol. 16, no. 6, pp. 4166–4176, 2019. 

- [5] T. Kronauer, J. Pohlmann, M. Matth´e, T. Smejkal, and G. Fettweis, “Latency analysis of ROS 2 multi-node systems,” in _Proceedings of the 2021 IEEE International Conference on Multisensor Fusion and Integration for Intelligent Systems (MFI)_ . IEEE, 2021, pp. 1–7. 

- [6] S. Paul, D. Lephuoc, and M. Hauswirth, “Performance evaluation of ROS 2-DDS middleware implementations facilitating cooperative driving in autonomous vehicle,” _arXiv preprint arXiv:2412.07485_ , 2024. 

- [7] G. Sciangula, D. Casini, A. Biondi, C. Scordino, and M. Di Natale, “Bounding the data-delivery latency of DDS messages in real-time applications,” in _35th Euromicro Conference on Real-Time Systems (ECRTS 2023)_ , vol. 262, 2023, pp. 9:1–9:26. 

- [8] X. Luo, X. Jiang, N. Guan, H. Liang, S. Liu, and W. Yi, “Modeling and analysis of inter-process communication delay in ROS 2,” in _Proceedings of the 2023 IEEE Real-Time Systems Symposium (RTSS)_ , 2023, pp. 198– 209. 

- [9] J.-B. Castillo-S´anchez, E. Gonz´alez-Parada, and J.-M. Cano-Garc´ıa, “Swarm robot communications in ROS 2: An experimental study,” _IEEE Access_ , vol. 12, pp. 142 930–142 943, 2024. 

- [10] J. Peeck, M. M¨ostl, T. Ishigooka, and R. Ernst, “A middleware protocol for time-critical wireless communication of large data samples,” in _Proceedings of the 2021 IEEE Real-Time Systems Symposium (RTSS)_ , 2021, pp. 1–13. 

- [11] H.-S. Park, S. Lee, D. Um, H. Ryu, and K.-J. Park, “An analytical latency model of the data distribution service in ROS 2,” in _IEEE INFOCOM 2025 - IEEE Conference on Computer Communications_ , 2025, pp. 1–10. 

- [12] B. Almadani, M. N. Bajwa, S.-H. Yang, and A.-W. A. Saif, “Performance evaluation of DDS-based middleware over wireless channel for reconfigurable manufacturing systems,” _International Journal of Distributed Sensor Networks_ , vol. 11, no. 7, p. 863123, 2015. 

VII. APPENDIX A: APPROXIMATION OF _tc_ 

This appendix describes how to approximate _tc_ depending on the relationship between the Publish period _r_ and the Heartbeat period _h_ . The parameter _tc_ is the average offset from a Publish event to the next Heartbeat. We consider three cases: 

the first Publish event is _δ ∈_ [0 _, r_ ). Then the next Publish event offset is ( _δ_ + _r_ ) mod _h_ . More generally, if we consider the _n_ -th Publish event, its offset can be written as ( _δ_ + _n r_ ) mod _h_ . Let [ _s, e_ ) = �( _n −_ 1) _r_ mod _h, n r_ mod _h_ � be the offset interval for _P_<sup>(</sup><sup>_n_)</sup> . Assuming a continuous uniform distribution within this interval, we approximate the mean offset by 


If _e ≥ s_ , the offset remains within a single segment [ _s, e_ ) _⊆_ [0 _, h_ ). Otherwise ( _e < s_ ), it wraps around _h_ and splits into two segments, [ _s, h_ ) and [0 _, e_ ). 

## _C. Case 3: r ¿ h_ 

If _r_ exceeds _h_ , the Heartbeat mechanism may stop once all data are acknowledged (acked), and resume when a new Publish event arrives. Thus, the offset _δ_ follows a repeating pattern of length _L_ : 


When Heartbeat stops and restarts following a new Publish, the offset could become _h_ . This case is _δ_ 1 = _h_ . _δ_ 1 instead becomes 0 only if unacked _̸_ = 0 at that moment. The probability that unacked messages are already zero is given by Hb<sup>_H−_1</sup> ( _P_ )0, where _H_ =<sup>LCM</sup> _h_<sup><u>(</u></sup><sup>_r,h_</sup><sup><u>)</u></sup> _−_ 1. Hence, we approximate 


When _r > h_ , the offset _δ_ follows a pattern _{δl}_ that may reset according to whether Heartbeat stops or continues. We incorporate the probability that it does not stop into the average offset _tc_ using Hb<sup>_H−_1</sup> ( _P_ )0 term. 

VIII. APPENDIX B: EXPERIMENTAL RESULTS 

## _A. Case 1: r = h_ 

If the Publish and Heartbeat periods are the same, exactly one Publish event occurs between consecutive Heartbeats. In practice, the Heartbeat period exceeds its nominal value by about 0.2 ms, so the offset _δ_ between Heartbeat and Publish varies continuously over [0 _, r_ ). Interpreting _δ_ as uniformly distributed in [0 _, r_ ), we approximate the average offset: 


## _B. Case 2: r ¡ h_ 

If the Publish period is shorter than the Heartbeat period, then Heartbeat also does not stop. However, note that the offset cannot exceed the Heartbeat interval _h_ . Suppose the offset of 

10 

|IDX<br>_r_|_h_|_m_|_p_|Analytical|MDR (%)<br>Experimenta|l<br>Error|Analytical|Latency(ms)<br>Experimental|Error (%)|Analytical|Jitter<br>Experimental|Error (%)|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|1<br>50<br><br>|50<br>|0<br>|0.95<br>|94.22<br>|93.84<br>|0.37<br>|1.92<br>|1.86<br>|3.44<br>|9.33<br>|11.78<br>|20.73<br>|
|2<br>50<br><br>|50<br>|0<br>|0.9<br>|86.77<br>|87.23<br>|0.45<br>|5.75<br>|5.46<br>|5.16<br>|19.51<br>|19.42<br>|0.45<br>|
|3<br>50<br><br>|50<br>|0<br>|0.85<br>|77.68<br>|77.45<br>|0.23<br>|12.57<br>|12.51<br>|0.5<br>|33.35<br>|33.77<br>|1.25<br>|
|4<br>50<br><br>|50<br>|0<br>|0.8<br>|67.19<br>|66.78<br>|0.41<br>|23.8<br>|24.5<br>|2.84<br>|51.64<br>|56.9<br>|9.24<br>|
|5<br>50<br>6<br>50<br><br>|50<br>50<br>|0<br>0.5<br>|0.75<br><br>0.95<br><br>|55.86<br>94.22<br>|55.92<br>94.09<br>|0.06<br>0.13<br>|41.21<br>1.92<br>|41.21<br>2.13<br>|0.01<br>9.63<br>|75.42<br>9.33<br>|72.43<br>10.72<br>|4.14<br>12.94<br>|
|7<br>50<br>8<br>50|50<br>50|0.5<br>0.5|0.9<br><br>0.85|86.77<br>77.66|85.81<br>78.18|0.96<br>0.52|5.75<br>12.6|5.68<br>12.6|1.19<br>0.01|19.51<br>33.4|22.14<br>32.61|11.88<br>2.42|
|9<br>50|50|0.5|0.8|67.09|65.76|1.33|24|23.88|0.48|51.95|52.96|1.92|
|10<br>50|50|0.5|0.75|55.49|57.65|2.16|42.19|39.21|7.61|76.64|73.86|3.77|
|11<br>50|50|1|0.95|94.21|94.18|0.03|1.92|1.88|2.19|9.35|9.64|3.06|
|12<br>50|50|1|09|8674|8597|077|579|586|125|1963|2134|8|
|13<br>50|50|1|.<br>085|.<br>7746|.<br>7871|.<br>124|.<br>1289|.<br>1289|.<br>001|.<br>34|.<br>3466|19|
|14<br>50<br>15<br>50|50<br>50|1<br>1|.<br>0.8<br>075|.<br>66.47<br>541|.<br>66.78<br>5441|.<br>0.32<br>031|.<br>25.2<br>4588|.<br>25.2<br>446|.<br>0.01<br>288|53.76<br>8099|.<br>53.5<br>9224|.<br>0.5<br>1219|
|16<br>50|50|3|.<br>095|.<br>837|.<br>8295|.<br>075|.<br>545|.<br>525|.<br>378|.<br>1519|.<br>156|.<br>263|
|17<br>50|50|3|.<br>09|.<br>6578|.<br>6614|.<br>036|.<br>1532|.<br>1456|.<br>525|.<br>3022|.<br>3124|.<br>325|
|18<br>50<br><br>|50<br>|3<br>|.<br>0.85<br>|.<br>47.93<br>|.<br>47.65<br>|.<br>0.27<br>|.<br>31.51<br>|.<br>29.14<br>|.<br>8.15<br>|.<br>49.23<br>|.<br>48.15<br>|.<br>2.25<br>|
|19<br>50<br>20<br>50<br><br>|50<br>50<br>|3<br>3<br>|0.8<br>0.75<br>|31.85<br>18.89<br>|32.52<br>16.91<br>|0.67<br>1.98<br>|56.78<br>95.43<br>|55.53<br>95.27<br>|2.26<br>0.17<br>|73.54<br>105.24<br>|77.17<br>105.25<br>|4.71<br>0.01<br>|
|21<br>50<br>22<br>50<br><br>|50<br>50<br>|5<br>5<br>|0.95<br>0.9<br>|74.44<br>50.31<br>|74.24<br>50.13<br>|0.2<br>0.18<br>|8.61<br>22.78<br>|8.78<br>20.73<br>|1.98<br>9.87<br>|18.57<br>35.12<br>|20<br>35.74<br>|7.17<br>1.75<br>|
|23<br>50|50|5|0.85|30.49|29.06|1.42|44.38|43.13|2.92|55.38|56.34|1.7|
|24<br>50|50|5|0.8|16.25|16.05|0.2|76.5|76.53|0.04|80.98|80.2|0.97|
|25<br>50|50|5|0.75|7.4|7.1|0.31|123.91|122.3|1.32|113.79|119.76|4.98|
|26<br>50<br>27<br>50|50<br>50|10<br>10|0.95<br><br>0.9|55.74<br>26.39|55.01<br>25.37|0.73<br>1.02|15.12<br>35.82|14.8<br>36.68|2.21<br>2.36|22.88<br>40.69|23.72<br>43.52|3.53<br>6.5|
|28<br>50|50|10|085|1052|1147|095|6466|5984|805|6235|6202|053|
|29<br>50<br>30<br>50|50<br>50|10<br>10|.<br><br>0.8<br><br>075|.<br>3.43<br>087|.<br>5.54<br>162|.<br>2.11<br>075|.<br>106.03<br>16538|.<br>101.4<br>1619|.<br>4.56<br>215|.<br>89.34<br>12324|.<br>94.03<br>12795|.<br>4.98<br>367|
|31<br>50|100|0|.<br>095|.<br>9115|.<br>912|.<br>005|.<br>53|.<br>528|.<br>034|.<br>2249|.<br>227|.<br>091|
|32<br>50<br><br>|100<br>|0<br>|.<br>0.9<br>|.<br>79.86<br>|.<br>77.99<br>|.<br>1.87<br>|.<br>16.45<br>|.<br>16.58<br>|.<br>0.78<br>|.<br>46.8<br>|.<br>42.79<br>|.<br>9.37<br>|
|33<br>50<br><br>|100<br>|0<br>|0.85<br>|66.95<br>|65.91<br>|1.05<br>|35.87<br>|37.18<br>|3.51<br>|78.32<br>|79.54<br>|1.54<br>|
|34<br>50<br><br>|100<br>|0<br>|0.8<br>|53.61<br>|50.65<br>|2.96<br>|65.81<br>|64.38<br>|2.23<br>|117.45<br>|128.64<br>|8.7<br>|
|35<br>50<br><br>|100<br>|0<br>|0.75<br><br>|41.03<br>|41.02<br>|0.01<br>|108.67<br>|108.68<br>|0.01<br>|165.8<br>|166.07<br>|0.17<br>|
|36<br>50<br>37<br>50<br><br>|100<br>100<br>|0.<br>0.5<br>|0.95<br><br>0.9<br><br>|91.15<br>79.84<br>|90.75<br>79.63<br>|0.4<br>0.21<br>|5.3<br>16.49<br>|5.3<br>16.41<br>|0.02<br>0.48<br>|22.49<br>46.88<br>|21.59<br>46.91<br>|4.17<br>0.05<br>|
|38<br>50<br>|100|0.5<br>|0.85<br>|66.8<br>|66<br>|0.8<br>|36.3<br>|36.79<br>|1.35<br>|78.98|79.38|0.51<br>|
|39<br>50|100|0.5|0.8|53.02|52.34|0.68|68.19|67.85|0.5|120.38|120.44|0.05|
|40<br>50|100|0.5|0.75|39.54|35.48|4.06|117.47|119.16|1.42|174.29|177.19|1.64|
|41<br>50|100|1|0.95|91.13|90.91|0.21|5.33|5.32|0.12|22.59|22.41|0.82|
|42<br>50|100|1|0.9|79.63|79.56|0.07|16.93|16.92|0.01|47.89|48.02|0.26|
|43<br>50|100|1|0.85|66.02|64.61|1.41|38.45|38.39|0.16|82.17|79.8|2.96|
|44<br>50|100|1|08|5123|5125|002|7531|7524|01|1283|12663|132|
|45<br>50|100|1|.<br>075|.<br>3653|.<br>3406|.<br>247|.<br>13559|.<br>13565|.<br>005|.<br>1899|.<br>1871|.<br>15|
|46<br>50|100|3|.<br>095|.<br>7607|.<br>755|.<br>057|.<br>1466|.<br>1502|.<br>242|.<br>3599|.<br>3753|.<br>41|
|47<br>50<br>48<br>50<br><br>|100<br>100<br>|3<br>3<br>|.<br>0.9<br>0.85<br>|.<br>52.3<br>32.18<br>|.<br>51<br>29.75<br>|.<br>1.3<br>2.44<br>|.<br>41.85<br>85.5<br>|.<br>41.75<br>85.94<br>|.<br>0.23<br>0.51<br>|.<br>70.11<br>111.84<br>|.<br>70.44<br>117.76<br>|.<br>0.47<br>5.03<br>|
|49<br>50<br><br>|100<br>|3<br>|0.8<br>|17.39<br>|17.58<br>|0.19<br>|152<br>|152.36<br>|0.23<br>|164.23<br>|164.28<br>|0.03<br>|
|50<br>50<br><br>|100<br>|3<br>|0.75<br>|8<br>|3.95<br>|4.05<br>|251.05<br>|250.92<br>|0.05<br>|230.96<br>|223.96<br>|3.12<br>|
|51<br>50<br>52<br>50<br><br>|100<br>100<br>|5<br>5<br>|0.95<br>0.9<br>|63.89<br>35.54<br>|64.76<br>34.61<br>|0.87<br>0.94<br>|22.54<br>59.5<br>|21.95<br>60.55<br>|2.69<br>1.74<br>|43.06<br>79.41<br>|43.09<br>82.65<br>|0.09<br>3.92<br>|
|53<br>50<br><br>|100<br>|5<br>|0.85<br>|17.12<br>|15.2<br>|1.92<br>|114.7<br>|118.95<br>|3.57<br>|122.93<br>|131.41<br>|6.46<br>|
|54<br>50|100|5|0.8|6.95|6.22|0.72|195.46|195.49|0.01|176.8|174.22|1.48|
|55<br>50|100|5|0.75|2.27|0.58|1.69|312.3|312.34|0.01|244.83|250.31|2.19|
|56<br>50|100|10|0.95|42.23|42.33|0.1|37.66|36.95|1.93|51.45|52.28|1.58|
|57<br>50|100|10|0.9|14.88|10.11|4.77|87.95|89.23|1.43|89.42|94.06|4.94|
|58<br>50<br>59<br>50|100<br>100|10<br>10|0.85<br><br>0.8|4.29<br>0.95|3.71<br>0.13|0.59<br>0.82|158.7<br>258.81|158.68<br>259.01|0.01<br>0.08|135.1<br>190.38|135.6<br>190.4|0.37<br>0.01|
|60<br>50|100|10|075|015|007|008|39884|40221|084|25994|26261|102|
|61<br>50<br>62<br>50<br>63<br>50|200<br>200<br>200|0<br>0<br>0|.<br>0.95<br>0.9<br>085|.<br>85.47<br>68.61<br>5208|.<br>85.13<br>68.47<br>5282|.<br>0.34<br>0.14<br>074|.<br>16.57<br>50.16<br>10275|.<br>16.61<br>50.31<br>10274|.<br>0.25<br>0.3<br>001|.<br>55.65<br>112.66<br>17944|.<br>56.77<br>109.25<br>17646|.<br>1.98<br>3.12<br>169|
|64<br>50|200|0|.<br>08|.<br>3778|.<br>3758|.<br>021|.<br>17541|.<br>17539|.<br>001|.<br>25747|.<br>26082|.<br>128|
|65<br>50<br><br>|200<br>|0<br>|.<br>0.75<br><br>|.<br>26.47<br>|.<br>23.95<br>|.<br>2.53<br>|.<br>270.09<br>|.<br>270.35<br>|.<br>0.1<br>|.<br>350.64<br>|.<br>322.06<br>|.<br>8.87<br>|
|66<br>50<br>67<br>50<br><br>|200<br>200<br>|0.<br>0.5<br>|0.95<br><br>0.9<br><br>|85.47<br>68.46<br>|84.96<br>68.8<br>|0.51<br>0.34<br>|16.59<br>50.73<br>|16.58<br>51.71<br>|0.02<br>1.88<br>|55.69<br>113.59<br>|55.65<br>127.29<br>|0.08<br>10.77<br>|
|68<br>50<br><br>|200<br>|0.<br>|0.85<br><br>|51.36<br>|50.5<br>|0.86<br>|107.15<br>|107.11<br>|0.04<br>|184.68<br>|174.96<br>|5.56<br>|
|69<br>50<br><br>|200<br>|0.<br>|0.8<br><br>|35.88<br>|33.73<br>|2.15<br>|193.45<br>|194.51<br>|0.54<br>|274.29<br>|274.41<br>|0.05<br>|
|70<br>50|200|0.5|0.75|23.07|21.4|1.67|323.1|323.78|0.21|390.93|357.07|9.48|
|71<br>50|200|1|0.95|85.38|84.66|0.72|16.83|16.84|0.07|56.3|53.15|5.93|
|72<br>50|200|1|0.9|67.78|67.87|0.09|53.5|53.66|0.29|117.92|117.75|0.15|
|73<br>50|200|1|0.85|49.45|50.41|0.97|118.88|117.95|0.78|197.6|193.66|2.03|
|74<br>50<br>75<br>50|200<br>200|1<br>1|0.8<br>075|32.61<br>1898|30.67<br>1896|1.94<br>003|225.46<br>39173|224.75<br>39148|0.31<br>006|300.06<br>43214|299<br>43142|0.35<br>017|
|76<br>50|200|3|.<br>095|.<br>6355|.<br>6381|.<br>027|.<br>4366|.<br>437|.<br>009|.<br>8561|.<br>9058|.<br>548|
|77<br>50|200|3|.<br>09|.<br>3508|.<br>3439|.<br>069|.<br>11915|.<br>11919|.<br>003|.<br>16077|.<br>16094|.<br>01|
|78<br>50|200|3|.<br>085|.<br>1676|.<br>1616|.<br>059|.<br>23426|.<br>23426|.<br>0|.<br>25003|.<br>24114|.<br>369|
|79<br>50|200|3|.<br>08|.<br>671|.<br>454|.<br>217|.<br>40376|.<br>40299|019|.<br>35955|.<br>35987|.<br>009|
|80<br>50<br><br>|200<br>|3<br>|.<br>0.75<br>|.<br>2.14<br>|.<br>2.08<br>|.<br>0.06<br>|.<br>648.37<br>|.<br>647.7<br>|.<br>0.1<br>|.<br>497.1<br>|.<br>471.89<br>|.<br>5.34<br>|
|81<br>50<br>82<br>50<br><br>|200<br>200<br>|5<br>5<br>|0.95<br>0.9<br>|48.4<br>20.04<br>|47.28<br>18.88<br>|1.12<br>1.16<br>|64.09<br>160.01<br>|64<br>161.68<br>|0.14<br>1.03<br>|98.83<br>176.76<br>|100.53<br>172.85<br>|1.69<br>2.26<br>|
|83<br>50<br><br>|200<br>|5<br>|0.85<br>|6.98<br>|6.54<br>|0.44<br>|299.1<br>|298.46<br>|0.22<br>|268.4<br>|262.23<br>|2.35<br>|
|84<br>50<br><br>|200<br>|5<br>|0.8<br>|1.92<br>|1.32<br>|0.6<br>|497.45<br>|498.28<br>|0.17<br>|379.3<br>|380.52<br>|0.32<br>|
|85<br>50<br>|200|5|0.75<br>|0.39<br>|0.32<br>|0.07|776.15<br>|756.19|2.64|519.03|490.26|5.87<br>|
|86<br>50<br>87<br>50|200<br>200|10<br>10|0.95<br><br>0.9|26.45<br>6.3|24.45<br>5.31|2.01<br>0.99|99.05<br>222.06|99.72<br>222.08|0.66<br>0.01|112.82<br>194.72|112.88<br>184.92|0.05<br>5.3|
|88<br>50<br>89<br>50|200<br>200|10<br>10|0.85<br><br>0.8|1.17<br>0.14|0.67<br>0.06|0.5<br>0.09|394.4<br>629.47|393.38<br>629.27|0.26<br>0.03|288.11<br>400.19|287.96<br>395.06|0.05<br>1.3|
|90<br>50|200|10|0.75|0.01|0|0.01|951.66|1016.61|6.39|544.93|660.37|17.48|


11 

|IDX<br>_r_|_h_|_m_|_p_|Analytical|MDR (%)<br>Experiment|al<br>Error|Analytical|Latency(ms)<br>Experimental|Error (%)|Analytical|Jitter<br>Experimental|Error (%)|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|91<br>100<br><br>|50<br><br>|0<br>|0.95<br>|94.9<br>|94.14<br>|0.76<br>|1.68<br>|1.59<br>|6.17<br>|8.76<br>|11.76<br>|25.55<br>|
|92<br>100<br><br>|50<br><br>|0<br>|0.9<br>|89.29<br>|88.82<br>|0.47<br>|4.57<br>|4.54<br>|0.72<br>|17.53<br>|18.78<br>|6.67<br>|
|93<br>100<br><br>|50<br><br>|0<br>|0.85<br>|82.83<br>|81.29<br>|1.54<br>|9.37<br>|9.36<br>|0.04<br>|29.13<br>|32.65<br>|10.76<br>|
|94<br>100<br><br>|50<br><br>|0<br>|0.8<br>|75.29<br>|74.04<br>|1.26<br>|17.15<br>|17.11<br>|0.26<br>|44.93<br>|52.26<br>|14.02<br>|
|95<br>100<br>96<br>100<br><br>|50<br><br>50<br><br>|0<br>0.5<br>|0.75<br><br>0.95<br><br>|66.64<br>94.9<br>|64.64<br>94.77<br>|2<br>0.13<br>|29.52<br>1.68<br>|29.51<br>1.74<br>|0.03<br>3.07<br>|66.34<br>8.76<br>|67.67<br>11.45<br>|1.96<br>23.54<br>|
|97<br>100|50|0.5|0.9|89.29|88.06|1.24|4.57|4.58|0.11|17.53|18.99|7.7|
|98<br>100|50|0.5|0.85|82.83|81.65|1.17|9.37|9.37|0.01|29.14|38.71|24.73|
|99<br>100|50|0.5|0.8|75.29|73.49|1.8|17.17|17.17|0|44.97|48.21|6.73|
|100<br>100|50|0.5|0.75|66.6|62.96|3.63|29.64|28.77|3.03|66.54|72.37|8.05|
|101<br>100<br>102<br>100|50<br><br>50|1<br>1|0.95<br>0.9|94.9<br>89.29|94.31<br>88.31|0.59<br>0.98|1.68<br>4.58|1.67<br>4.44|0.57<br>3.07|8.76<br>17.55|10.3<br>19.05|14.96<br>7.9|
|103<br>100|50|1|085|828|8041|239|942|941|01|2928|3162|74|
|104<br>100<br>105<br>100|50<br><br>50|1<br>1|.<br>0.8<br>075|.<br>75.17<br>6623|.<br>74.05<br>635|.<br>1.12<br>273|.<br>17.45<br>307|.<br>16.47<br>3075|.<br>5.91<br>016|.<br>45.53<br>6822|.<br>46.08<br>7074|.<br>1.2<br>355|
|106<br>100|50|3|.<br>095|.<br>8548|.<br>8471|.<br>077|.<br>477|.<br>518|.<br>792|.<br>1425|.<br>1851|.<br>2299|
|107<br>10|50|3|.<br>09|.<br>7127|.<br>6955|.<br>173|.<br>1216|.<br>1215|.<br>005|.<br>273|.<br>2919|.<br>647|
|108<br>100<br><br>|50<br><br>|3<br>|.<br>0.85<br>|.<br>57.11<br>|.<br>54.98<br>|.<br>2.13<br>|.<br>23.32<br>|.<br>23.37<br>|.<br>0.22<br>|.<br>43.52<br>|.<br>45.23<br>|.<br>3.77<br>|
|109<br>100<br>110<br>100<br><br>|50<br><br>50<br><br>|3<br>3<br>|0.8<br>0.75<br>|43.32<br>30.54<br>|39.93<br>29.26<br>|3.39<br>1.28<br>|40.36<br>66.68<br>|39.82<br>66.66<br>|1.36<br>0.03<br>|65.02<br>93.6<br>|67.37<br>93.09<br>|3.5<br>0.55<br>|
|111<br>100<br><br>|50<br><br>|5<br>|0.95<br>|77<br>|76.81<br>|0.19<br>|7.53<br>|7.54<br>|0.01<br>|17.46<br>|21.08<br>|17.16<br>|
|112<br>100<br><br>|50<br><br>|5<br>|0.9<br>|56.97<br>|55.14<br>|1.83<br>|18.07<br>|18.1<br>|0.19<br>|31.98<br>|34.91<br>|8.38<br>|
|113<br>100|50|5|0.85|39.64|37.56|2.08|32.98|32.99|0.02|49.92|53.54|6.77|
|114<br>100|50|5|0.8|25.41|23.94|1.47|54.93|54.95|0.04|73.23|73.31|0.11|
|115<br>100|50|5|0.75|14.66|14.13|0.53|88.44|88.49|0.05|103.9|108.54|4.27|
|116<br>100|50|10|0.95|59.31|56.92|2.4|13.2|13.2|0.01|21.6|26.07|17.15|
|117<br>100|50|10|0.9|32.67|32.12|0.55|28.23|27.01|4.51|37.62|42.13|10.72|
|118<br>100|50|10|0.85|16.18|15.65|0.53|47.9|47.82|0.16|57.61|62.7|8.11|
|119<br>100|50|10|08|7|679|02|7707|7734|034|8333|7997|42|
|120<br>100<br>121<br>100|50<br><br>100|10<br>0|.<br>0.75<br>095|2.55<br>9422|.<br>2.73<br>942|.<br>0.18<br>001|.<br>122<br>384|.<br>124.64<br>382|.<br>2.12<br>052|.<br>116.15<br>1867|.<br>113.02<br>2004|.<br>2.78<br>683|
|122<br>100|100|0|.<br>09|.<br>8677|.<br>8667|.<br>011|.<br>1149|.<br>1096|.<br>488|.<br>3901|.<br>3779|.<br>324|
|123<br>100<br><br>|100<br><br>|0<br>|.<br>0.85<br>|.<br>77.68<br>|.<br>77.73<br>|.<br>0.06<br>|.<br>25.14<br>|.<br>25.15<br>|.<br>0.04<br>|.<br>66.7<br>|.<br>66.68<br>|.<br>0.03<br>|
|124<br>100<br><br>|100<br><br>|0<br>|0.8<br>|67.19<br>|68.48<br>|1.29<br>|47.6<br>|45.93<br>|3.63<br>|103.28<br>|103.61<br>|0.31<br>|
|125<br>100<br><br>|100<br><br>|0<br>|0.75<br><br>|55.86<br>|57.11<br>|1.24<br>|82.43<br>|77.68<br>|6.12<br>|150.85<br>|148.88<br>|1.33<br>|
|126<br>100<br><br>|100<br><br>|0.5<br>|0.95<br><br>|94.22<br>|93.9<br>|0.31<br>|3.84<br>|3.81<br>|0.91<br>|18.67<br>|19.33<br>|3.44<br>|
|127<br>100<br><br>|100<br><br>|0.5<br>|0.9<br><br>|86.77<br>|86.89<br>|0.11<br>|11.5<br>|11.18<br>|2.83<br>|39.02<br>|39.7<br>|1.73<br>|
|128<br>100|100|0.5<br>|0.85<br>|77.66<br>|77.12<br>|0.54|25.19|25.37|0.68|66.81|69.99<br>|4.54|
|129<br>100|100|0.5|0.8|67.09|67.88|0.79|47.99|47.98|0.02|103.9|105.45|1.47|
|130<br>100|100|0.5|0.75|55.49|54.23|1.26|84.38|83.58|0.97|153.27|165.62|7.45|
|131<br>100|100|1|0.95|94.21|94.41|0.2|3.85|3.83|0.36|18.69|19.92|6.15|
|132<br>100|100|1|0.9|86.74|86.94|0.2|11.58|11.21|3.31|39.27|38.29|2.54|
|133<br>100|100|1|0.85|77.46|78.4|0.94|25.78|25.76|0.08|68|70.79|3.95|
|134<br>100|100|1|08|6647|6712|065|5039|4822|45|10752|10629|117|
|135<br>100|100|1|.<br>075|.<br>541|.<br>554|.<br>131|.<br>9177|.<br>8878|.<br>336|.<br>16199|.<br>15866|.<br>21|
|136<br>100|100|3|.<br>095|.<br>837|.<br>8389|.<br>018|.<br>1089|.<br>1089|.<br>001|.<br>3037|.<br>3263|.<br>692|
|137<br>100<br>138<br>100|100<br><br>100|3<br>3|.<br>0.9<br>085|.<br>65.78<br>4793|.<br>64.7<br>4643|.<br>1.08<br>15|.<br>30.65<br>6303|.<br>30.7<br>6304|.<br>0.17<br>001|.<br>60.45<br>9846|.<br>61.89<br>9956|.<br>2.33<br>11|
|139<br>100<br><br>|100<br><br>|3<br>|.<br>0.8<br>|.<br>31.85<br>|.<br>32.06<br>|.<br>0.21<br>|.<br>113.57<br>|.<br>109.52<br>|.<br>3.69<br>|.<br>147.07<br>|.<br>143.66<br>|.<br>2.38<br>|
|140<br>100<br><br>|100<br><br>|3<br>|0.75<br>|18.89<br>|18.96<br>|0.07<br>|190.86<br>|190.53<br>|0.18<br>|210.48<br>|210.52<br>|0.02<br>|
|141<br>100<br>142<br>100<br><br>|100<br><br>100<br><br>|5<br>5<br>|0.95<br>0.9<br>|74.44<br>50.31<br>|74.2<br>49.79<br>|0.24<br>0.52<br>|17.22<br>45.56<br>|16.46<br>44.36<br>|4.61<br>2.69<br>|37.14<br>70.23<br>|39.14<br>72.19<br>|5.12<br>2.72<br>|
|143<br>100<br><br>|100<br><br>|5<br>|0.85<br>|30.49<br>|29.9<br>|0.58<br>|88.77<br>|87.38<br>|1.59<br>|110.77<br>|114.38<br>|3.16<br>|
|144<br>100|100|5|0.8|16.25|16.37|0.12|153|149.1|2.62|161.95|163.2|0.76|
|145<br>100|100|5|0.75|7.4|7.52|0.11|247.82|237.46|4.37|227.59|223.48|1.84|
|146<br>100|100|10|0.95|55.74|56.59|0.85|30.25|29|4.3|45.77|59.73|23.37|
|147<br>100|100|10|0.9|26.39|27.66|1.27|71.64|66.46|7.79|81.38|84.83|4.07|
|148<br>100<br>149<br>100|100<br><br>100|10<br>10|0.85<br>08|10.52<br>343|12.45<br>356|1.93<br>013|129.32<br>21206|121.38<br>21176|6.54<br>014|124.69<br>17869|125.57<br>18206|0.7<br>185|
|150<br>100|100|10|.<br>075|.<br>087|.<br>06|.<br>027|.<br>33077|.<br>33054|.<br>007|.<br>24649|.<br>25902|.<br>484|
|151<br>100<br>152<br>100|200<br><br>200|0<br>0|.<br>0.95<br>09|.<br>91.15<br>7986|.<br>91.19<br>7959|.<br>0.04<br>027|.<br>10.6<br>329|.<br>10.6<br>3291|.<br>0.05<br>001|.<br>44.98<br>9359|.<br>44.76<br>9414|.<br>0.49<br>058|
|153<br>100<br>154<br>1|200<br><br>2|0<br>|.<br>0.85<br>|.<br>66.95<br>561|.<br>66.59<br>51|.<br>0.36<br>42|.<br>71.74<br>116|.<br>71.81<br>1166|.<br>0.1<br>2|.<br>156.64<br>241|.<br>156.01<br>221|.<br>0.4<br>25|
|0<br>155<br>100<br><br>|00<br><br>200<br><br>|0<br>0<br>|0.8<br>0.75<br><br>|3.<br>41.03<br>|3.9<br>40.53<br>|0.<br>0.5<br>|3.3<br>217.35<br>|3.<br>219.5<br>|0.0<br>0.98<br>|3.9<br>331.59<br>|9.9<br>327.63<br>|.<br>1.21<br>|
|156<br>100<br><br>|200<br><br>|0.5<br>|0.95<br><br>|91.15<br>|91.33<br>|0.18<br>|10.6<br>|10.59<br>|0.03<br>|44.98<br>|48.09<br>|6.47<br>|
|157<br>100<br><br>|200<br><br>|0.5<br>|0.9<br><br>|79.84<br>|80.14<br>|0.3<br>|32.98<br>|33.04<br>|0.19<br>|93.76<br>|96.22<br>|2.55<br>|
|158<br>100<br><br>|200<br><br>|0.5<br>|0.85<br><br>|66.8<br>|66.3<br>|0.49<br>|72.59<br>|72.58<br>|0.02<br>|157.96<br>|157.31<br>|0.42<br>|
|159<br>100<br><br>|200<br><br>|0.5<br>|0.8<br><br>|53.02<br>|51.19<br>|1.83<br>|136.38<br>|144.14<br>|5.39<br>|240.75<br>|247<br>|2.53<br>|
|160<br>100<br>161<br>100|200<br><br>200|0.5<br>1|0.75<br>0.95|39.54<br>91.13|38.53<br>91.48|1.01<br>0.35|234.93<br>10.65|234.89<br>10.58|0.02<br>0.64|348.58<br>45.18|346.72<br>46.4|0.53<br>2.64|
|162<br>100|200|1|0.9|79.63|79.54|0.1|33.85|33.85|0|95.78|94.52|1.33|
|163<br>100|200|1|0.85|66.02|65.46|0.57|76.9|76.9|0|164.34|157.76|4.17|
|164<br>100<br>165<br>100|200<br><br>200|1<br>1|0.8<br>075|51.23<br>3653|51.61<br>3595|0.38<br>058|150.63<br>27118|150.58<br>2709|0.03<br>01|256.61<br>37981|250.56<br>36681|2.41<br>354|
|166<br>100|200|3|.<br>095|.<br>7607|.<br>7608|.<br>001|.<br>2932|.<br>2954|.<br>074|.<br>7199|.<br>7511|.<br>415|
|167<br>100|200|3|.<br>09|.<br>523|.<br>5218|.<br>013|.<br>8369|.<br>8342|.<br>033|.<br>14022|.<br>14081|.<br>042|
|168<br>100|200|3|.<br>085|.<br>3218|.<br>3319|.<br>1|.<br>171|.<br>16984|.<br>068|.<br>22368|.<br>22737|.<br>163|
|169<br>100<br><br>|200<br><br>|3<br>|.<br>0.8<br>|.<br>17.39<br>|.<br>15.95<br>|1.43<br>|304<br>|.<br>308.21<br>|.<br>1.37<br>|.<br>328.46<br>|.<br>301.59<br>|.<br>8.91<br>|
|170<br>100<br><br>|200<br><br>|3<br>|0.75<br>|8<br>|4.34<br>|3.66<br>|502.09<br>|502.64<br>|0.11<br>|461.92<br>|469.26<br>|1.56<br>|
|171<br>100<br><br>|200<br><br>|5<br>|0.95<br>|63.89<br>|64<br>|0.12<br>|45.09<br>|45.15<br>|0.13<br>|86.11<br>|90.7<br>|5.06<br>|
|172<br>100<br><br>|200<br><br>|5<br>|0.9<br>|35.54<br>|35.18<br>|0.36<br>|118.99<br>|117.58<br>|1.2<br>|158.83<br>|161.52<br>|1.66<br>|
|173<br>100<br><br>|200<br><br>|5<br>|0.85<br>|17.12<br>|16.37<br>|0.75<br>|229.4<br>|229.34<br>|0.03<br>|245.86<br>|243.75<br>|0.86<br>|
|174<br>100<br><br>|200<br><br>|5<br>|0.8<br>|6.95<br>|7.06<br>|0.11<br>|390.93<br>|395.64<br>|1.19<br>|353.6<br>|353.83<br>|0.07<br>|
|175<br>100<br>|200|5|0.75<br>|2.27|1.67<br>|0.6|624.61<br>|624.86<br>|0.04|489.65|471.8|3.78<br>|
|176<br>100<br>177<br>100|200<br><br>200|10<br>10|0.95<br>0.9|42.23<br>14.88|42.52<br>14.6|0.29<br>0.28|75.32<br>175.91|75.23<br>174.75|0.12<br>0.66|102.9<br>178.84|111.79<br>186.32|7.96<br>4.02|
|178<br>100<br>179<br>100|200<br><br>200|10<br>10|0.85<br>0.8|4.29<br>0.95|4.04<br>0|0.25<br>0.95|317.4<br>517.61|317.6<br>517.55|0.06<br>0.01|270.2<br>380.76|270.14<br>377.11|0.02<br>0.97|
|180<br>100|200|10|0.75|0.15|0|0.15|797.68|797.84|0.02|519.88|505.33|2.88|


12 

|IDX<br>_r_<br>_h_|_m_<br>_p_|Analytical|MDR (%)<br>Experimenta|l<br>Error|Analytical|Latency(ms)<br>Experimental|Error (%)|Analytical|Jitter<br>Experimental|Error (%)|
|---|---|---|---|---|---|---|---|---|---|---|
|181<br>200<br>50<br><br><br>|0<br>0.95<br><br>|95<br>|95.34<br>|0.34<br>|2.91<br>|2.89<br>|0.65<br>|13.57<br>|14.24<br>|4.68<br>|
|182<br>200<br>50<br>183<br>200<br>50<br><br><br>|0<br>0.9<br>0<br>0.85<br><br>|89.95<br>84.71<br>|89.53<br>84.17<br>|0.42<br>0.54<br>|6.84<br>12.24<br>|6.83<br>12.05<br>|0.08<br>1.57<br>|23.31<br>34.77<br>|23.31<br>35.37<br>|0.01<br>1.69<br>|
|184<br>200<br>50<br><br><br>|0<br>0.8<br><br>|79.05<br>|78.29<br>|0.76<br>|19.89<br>|19.36<br>|2.74<br>|49.43<br>|52.46<br>|5.78<br>|
|185<br>200<br>50<br>186<br>200<br>50<br><br><br><br><br>|0<br>0.75<br>0.5<br>0.95<br><br>|72.71<br>95<br>|71.42<br>94.89<br>|1.3<br>0.11<br>|31.03<br>2.91<br>|29.76<br>2.91<br>|4.28<br>0.05<br>|68.85<br>13.57<br>|69.15<br>13.63<br>|0.43<br>0.41<br>|
|187<br>200<br>50<br>|0.5<br>0.9|89.95|90.19|0.23|6.84|6.55|4.47|23.31|22.77|2.38|
|188<br>200<br>50<br>|0.5<br>0.85|84.71|85.01|0.3|12.24|11.49|6.48|34.77|35.17|1.13|
|189<br>200<br>50<br>|0.5<br>0.8|79.05|78.15|0.9|19.89|18.71|6.27|49.43|47.41|4.27|
|190<br>200<br>50<br>|0.5<br>0.75|72.71|70.53|2.18|31.04|30.79|0.8|68.87|68.92|0.07|
|191<br>200<br>50<br>192<br>200<br>50|1<br>0.95<br>1<br>09|95<br>8995|94.88<br>8976|0.12<br>019|2.91<br>684|2.91<br>683|0.12<br>013|13.57<br>2331|13.57<br>2452|0.04<br>493|
|193<br>200<br>50|.<br>1<br>085|.<br>8471|.<br>8414|.<br>057|.<br>1224|.<br>1224|.<br>001|.<br>3479|.<br>3626|.<br>406|
|194<br>200<br>50<br>195<br>200<br>50|.<br>1<br>0.8<br>1<br>075|.<br>79.04<br>7267|.<br>77.99<br>7146|.<br>1.05<br>121|.<br>19.93<br>3125|.<br>19.25<br>3126|.<br>3.53<br>001|.<br>49.53<br>6928|.<br>48.29<br>739|.<br>2.57<br>625|
|196<br>200<br>50|.<br>3<br>095|.<br>8573|.<br>8565|.<br>008|.<br>83|.<br>824|.<br>075|.<br>2196|.<br>2191|.<br>023|
|197<br>200<br>50|.<br>3<br>09|.<br>7279|.<br>7294|.<br>015|.<br>1855|.<br>1772|.<br>466|.<br>3573|.<br>3561|.<br>033|
|198<br>200<br>50<br><br><br>|.<br>3<br>0.85<br><br>|.<br>60.82<br>|.<br>60.1<br>|.<br>0.71<br>|.<br>31.35<br>|.<br>29.2<br>|.<br>7.35<br>|.<br>50.75<br>|.<br>50.77<br>|.<br>0.05<br>|
|199<br>200<br>50<br><br><br>|3<br>0.8<br><br>|49.51<br>|50.12<br>|0.61<br>|48.04<br>|44.85<br>|7.11<br>|69.41<br>|84.82<br>|18.17<br>|
|200<br>200<br>50<br><br><br>|3<br>0.75<br><br>|38.71<br>|37.74<br>|0.98<br>|70.83<br>|69.35<br>|2.14<br>|93.78<br>|96.87<br>|3.19<br>|
|201<br>200<br>50<br><br><br>|5<br>0.95<br><br>|77.37<br>|76.56<br>|0.81<br>|13.18<br>|13.17<br>|0.07<br>|26.54<br>|26.7<br>|0.62<br>|
|202<br>200<br>50<br><br><br>|5<br>0.9<br><br>|58.9<br>|59.74<br>|0.85<br>|28.05<br>|25.61<br>|9.53<br>|41.07<br>|40.08<br>|2.46<br>|
|203<br>200<br>50|5<br>0.85|43.69|42.73|0.95|45.22|44.02|2.73|56.57|58.93|4.01|
|204<br>200<br>50|5<br>0.8|31.08|30.62|0.46|66.27|62.67|5.75|75.9|83.33|8.91|
|205<br>200<br>50|5<br>0.75|20.79|20.07|0.72|94.36|89.73|5.16|102.1|102.96|0.83|
|206<br>200<br>50|10<br>0.95|59.86|62.28|2.42|23.49|21.83|7.59|32.12|32.69|1.75|
|207<br>200<br>50|10<br>0.9|34.7|32.66|2.04|44.94|41.89|7.27|45.24|46.39|2.46|
|208<br>200<br>50|10<br>0.85|19.13|18.22|0.92|66.47|62.08|7.07|60.91|63.91|4.7|
|209<br>200<br>50<br>210<br>200<br>50|10<br>0.8<br>10<br>075|9.77<br>448|10.83<br>466|1.06<br>018|91.72<br>12659|85.69<br>12444|7.03<br>172|82.43<br>11202|83.78<br>11843|1.61<br>542|
|211<br>200<br>100|.<br>0<br>095|.<br>949|.<br>9512|.<br>022|.<br>337|.<br>322|.<br>464|.<br>1751|.<br>2071|.<br>1542|
|212<br>200<br>100<br><br><br>|.<br>0<br>0.9<br><br>|.<br>89.29<br>|.<br>88.15<br>|.<br>1.14<br>|.<br>9.15<br>|.<br>9.08<br>|.<br>0.79<br>|.<br>35.05<br>|.<br>37.69<br>|.<br>7<br>|
|213<br>200<br>100<br><br><br>|0<br>0.85<br><br>|82.83<br>|80.68<br>|2.14<br>|18.73<br>|18.74<br>|0.06<br>|58.27<br>|62.03<br>|6.07<br>|
|214<br>200<br>100<br><br><br>|0<br>0.8<br><br>|75.29<br>|73.81<br>|1.48<br>|34.3<br>|34.24<br>|0.18<br>|89.86<br>|99.13<br>|9.35<br>|
|215<br>200<br>100<br><br><br><br>|0<br>0.75<br><br>|66.64<br>|64.42<br>|2.22<br>|59.04<br>|59.06<br>|0.03<br>|132.69<br>|141.02<br>|5.91<br>|
|216<br>200<br>100<br><br><br><br><br>|0.5<br>0.95<br><br>|94.9<br>|94.64<br>|0.26<br>|3.37<br>|3.38<br>|0.41<br>|17.51<br>|21.79<br>|19.62<br>|
|217<br>200<br>100<br><br><br><br><br>|0.5<br>0.9<br><br>|89.29<br>|88.35<br>|0.95<br>|9.15<br>|8.57<br>|6.72<br>|35.05<br>|37.84<br>|7.38<br>|
|218<br>200<br>100<br><br>|0.5<br>0.85<br>|82.83<br>|81.35<br>|1.48<br>|18.73|18.73|0.01|58.27|66.79<br>|12.75|
|219<br>200<br>100<br>|0.5<br>0.8|75.29|71.68|3.61|34.33|34.33|0.02|89.93|93.95|4.27|
|220<br>200<br>100<br>|0.5<br>0.75|66.6|64.56|2.03|59.28|59.31|0.05|133.09|143.78|7.44|
|221<br>200<br>100|1<br>0.95|94.9|94.53|0.37|3.37|3.36|0.23|17.52|19.78|11.44|
|222<br>200<br>100|1<br>0.9|89.29|88.57|0.72|9.16|9.15|0.08|35.09|39.41|10.94|
|223<br>200<br>100|1<br>0.85|82.8|80.92|1.88|18.84|18.8|0.21|58.56|62.68|6.58|
|224<br>200<br>100<br>225<br>200<br>100|1<br>0.8<br>1<br>075|75.17<br>6623|74.12<br>6405|1.05<br>217|34.9<br>614|33.45<br>6102|4.32<br>063|91.06<br>13645|95.28<br>16152|4.44<br>1552|
|226<br>200<br>100|.<br>3<br>095|.<br>8548|.<br>8469|.<br>079|.<br>954|.<br>1001|.<br>472|.<br>285|.<br>349|.<br>1832|
|227<br>200<br>100|.<br>3<br>09|.<br>7127|.<br>6962|.<br>165|.<br>2431|.<br>2431|.<br>0|.<br>546|.<br>613|.<br>1094|
|228<br>200<br>100|.<br>3<br>085|.<br>5711|.<br>5426|.<br>285|.<br>4663|.<br>4665|004|.<br>8705|.<br>9018|.<br>348|
|229<br>200<br>100<br>230<br>200<br>100<br><br><br>|.<br>3<br>0.8<br>3<br>0.75<br><br>|.<br>43.32<br>30.54<br>|.<br>41.03<br>29.18<br>|.<br>2.29<br>1.36<br>|.<br>80.73<br>133.37<br>|.<br>79.32<br>133.22<br>|.<br>1.78<br>0.11<br>|.<br>130.03<br>187.2<br>|.<br>130.08<br>191.76<br>|.<br>0.04<br>2.38<br>|
|231<br>200<br>100<br><br><br>|5<br>0.95<br><br>|77<br>|77.25<br>|0.25<br>|15.07<br>|15.12<br>|0.32<br>|34.92<br>|41.03<br>|14.89<br>|
|232<br>200<br>100<br><br><br>|5<br>0.9<br><br>|56.97<br>|55.13<br>|1.84<br>|36.14<br>|36.28<br>|0.38<br>|63.97<br>|71.1<br>|10.03<br>|
|233<br>200<br>100<br><br><br>|5<br>0.85<br><br>|39.64<br>|35.97<br>|3.67<br>|65.96<br>|66.01<br>|0.08<br>|99.83<br>|106.81<br>|6.53<br>|
|234<br>200<br>100|5<br>0.8|25.41|23.21|2.2|109.87|109.79|0.07|146.45|156.18|6.23|
|235<br>200<br>100|5<br>0.75|14.66|13.46|1.2|176.88|177.01|0.07|207.8|209.19|0.66|
|236<br>200<br>100|10<br>0.95|59.31|57.06|2.26|26.39|26.38|0.03|43.2|52.93|18.38|
|237<br>200<br>100|10<br>0.9|32.67|31.24|1.44|56.46|55.72|1.33|75.24|85.61|12.12|
|238<br>200<br>100<br>239<br>200<br>100|10<br>0.85<br>10<br>08|16.18<br>7|15.29<br>651|0.89<br>049|95.79<br>15414|93.41<br>15309|2.56<br>069|115.23<br>16665|124.88<br>16992|7.73<br>192|
|240<br>200<br>100|.<br>10<br>075|255|.<br>228|.<br>027|.<br>24401|.<br>262|.<br>687|.<br>23231|.<br>2305|.<br>078|
|241<br>200<br>200|.<br>0<br>095|.<br>9422|.<br>9454|.<br>033|.<br>768|72|.<br>671|.<br>3734|.<br>406|.<br>803|
|242<br>200<br>200|.<br>0<br>09|.<br>8677|.<br>8601|.<br>076|.<br>2299|.<br>2273|.<br>114|.<br>7802|.<br>8074|.<br>337|
|243<br>200<br>200|.<br>0<br>085|.<br>7768|.<br>7855|.<br>087|.<br>5028|.<br>4853|.<br>361|.<br>1334|.<br>13476|.<br>101|
|244<br>200<br>200<br><br><br>|.<br>0<br>0.8<br><br>|.<br>67.19<br>|.<br>67.68<br>|.<br>0.49<br>|.<br>95.2<br>|.<br>90.44<br>|.<br>5.26<br>|.<br>206.56<br>|.<br>198.96<br>|.<br>3.82<br>|
|245<br>200<br>200<br>246<br>200<br>200<br><br><br><br><br>|0<br>0.75<br>0.5<br>0.95<br><br>|55.86<br>94.22<br>|56.13<br>93.78<br>|0.26<br>0.43<br>|164.86<br>7.68<br>|159.83<br>7.57<br>|3.14<br>1.49<br>|301.7<br>37.34<br>|297.76<br>38.38<br>|1.32<br>2.72<br>|
|247<br>200<br>200<br><br><br><br><br>|0.5<br>0.9<br><br>|86.77<br>|87.1<br>|0.32<br>|22.99<br>|22.73<br>|1.16<br>|78.04<br>|78.65<br>|0.77<br>|
|248<br>200<br>200<br><br><br><br><br>|0.5<br>0.85<br><br>|77.66<br>|78.72<br>|1.06<br>|50.39<br>|50.44<br>|0.11<br>|133.62<br>|141.1<br>|5.3<br>|
|249<br>200<br>200<br><br><br><br><br>|0.5<br>0.8<br><br>|67.09<br>|66.54<br>|0.55<br>|95.99<br>|96.35<br>|0.38<br>|207.8<br>|209.5<br>|0.81<br>|
|250<br>200<br>200<br><br>251<br>200<br>200|0.5<br>0.75<br>1<br>0.95|55.49<br>94.21|56.13<br>94.3|0.64<br>0.09|168.77<br>7.69|168.9<br>7.44|0.08<br>3.34|306.55<br>37.39|312.35<br>40.26|1.86<br>7.12|
|252<br>200<br>200|1<br>0.9|86.74|86.47|0.27|23.16|22.68|2.14|78.53|81.66|3.83|
|253<br>200<br>200|1<br>0.85|77.46|77.35|0.11|51.56|48.42|6.49|136|133.09|2.19|
|254<br>200<br>200<br>255<br>200<br>200|1<br>0.8<br>1<br>075|66.47<br>541|66.14<br>5467|0.33<br>057|100.78<br>18353|99.68<br>18384|1.11<br>017|215.05<br>32397|217.7<br>32586|1.22<br>058|
|256<br>200<br>200|.<br>3<br>095|.<br>837|.<br>8512|.<br>142|.<br>2179|.<br>21|.<br>373|.<br>6074|.<br>6521|.<br>685|
|257<br>200<br>200|.<br>3<br>09|.<br>6578|.<br>6698|.<br>12|.<br>613|5762|.<br>639|.<br>12089|.<br>12256|.<br>136|
|258<br>200<br>200|.<br>3<br>085|.<br>4793|.<br>4913|.<br>121|.<br>12606|.<br>12278|.<br>267|.<br>19691|.<br>21273|.<br>744|
|259<br>200<br>200<br><br><br>|.<br>3<br>0.8<br><br>|.<br>31.85<br>|.<br>31.08<br>|.<br>0.77<br>|.<br>227.14<br>|.<br>227.23<br>|.<br>0.04<br>|.<br>294.15<br>|.<br>294.13<br>|.<br>0.01<br>|
|260<br>200<br>200<br><br><br>|3<br>0.75<br><br>|18.89<br>|18.63<br>|0.26<br>|381.72<br>|376.82<br>|1.3<br>|420.95<br>|407.27<br>|3.36<br>|
|261<br>200<br>200<br><br><br>|5<br>0.95<br><br>|74.44<br>|73.98<br>|0.46<br>|34.44<br>|32.08<br>|7.38<br>|74.28<br>|75.93<br>|2.18<br>|
|262<br>200<br>200<br><br><br>|5<br>0.9<br><br>|50.31<br>|50.65<br>|0.34<br>|91.12<br>|85.29<br>|6.84<br>|140.46<br>|140.1<br>|0.26<br>|
|263<br>200<br>200<br><br><br>|5<br>0.85<br><br>|30.49<br>|31.28<br>|0.8<br>|177.53<br>|174.8<br>|1.57<br>|221.53<br>|239.06<br>|7.33<br>|
|264<br>200<br>200<br><br><br>|5<br>0.8<br><br>|16.25<br>|17.21<br>|0.96<br>|306<br>|293.88<br>|4.12<br>|323.91<br>|336.99<br>|3.88<br>|
|265<br>200<br>200<br>|5<br>0.75<br>|7.4<br>|7.96<br>|0.55|495.65<br>|492.74<br>|0.59|455.17<br>|425.36<br>|7.01|
|266<br>200<br>200<br>267<br>200<br>200|10<br>0.95<br>10<br>0.9|55.74<br>26.39|55.83<br>27.46|0.09<br>1.07|60.49<br>143.28|59.29<br>132.55|2.02<br>8.09|91.54<br>162.75|102.54<br>162.38|10.73<br>0.23|
|268<br>200<br>200<br>269<br>200<br>200|10<br>0.85<br>10<br>0.8|10.52<br>3.43|10.39<br>3.54|0.13<br>0.11|258.65<br>424.11|252.35<br>417.88|2.49<br>1.49|249.39<br>357.38|262.1<br>370.28|4.85<br>3.48|
|270<br>200<br>200|10<br>0.75|0.87|0.23|0.65|661.53|661.86|0.05|492.97|496.58|0.73|


