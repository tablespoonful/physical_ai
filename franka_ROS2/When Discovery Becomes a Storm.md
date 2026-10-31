---
title: "When Discovery Becomes a Storm: A ROS 2 Discovery Model for Wireless Robotic Networks"
date: "2026-08-03"
authors: "Yeonwoo Choi; Sanghoon Lee; Kyung-Joon Park"
url: https://arxiv.org/abs/2608.02242
pdf: https://arxiv.org/pdf/2608.02242
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2608.02242)** / [論文ページ](https://arxiv.org/abs/2608.02242)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# When Discovery Becomes a Storm: A ROS 2 Discovery Model for Wireless Robotic Networks 

Yeonwoo Choi<sup>†</sup> , Sanghoon Lee<sup>†</sup> , and Kyung-Joon Park<sup>*</sup> 

Department of Electrical Engineering and Computer Science, DGIST, Daegu, Republic of Korea Email: _{_ cyw040306, leesh2913, kjp _}_ @dgist.ac.kr 

**_Abstract_ —In Robot Operating System 2 (ROS 2), Data Distribution Service (DDS) participants must discover one another before exchanging data. In wireless environments, delayed or lost discovery messages cause reliability timers to expire, triggering retransmissions that intensify channel contention and further delay the delivery of discovery messages. This self-reinforcing feedback can escalate into a** **_discovery storm_ . Existing models characterize discovery demand under fixed delivery conditions, but do not capture how shared-channel delay changes protocol state and generates further traffic. To address this issue, we present the first closed-loop analytical model of ROS 2 discovery that characterizes how delay-induced feedback amplifies retransmission overhead and leads to severe discovery storms. Our model represents channel contention as a shared service process, coupling messagedelivery latency with receiver states and reliability timers. The model predicts both discovery completion time and per-class message counts. We validate the model through 1,350 experimental runs across 90 topology configurations. An open-loop airtime baseline captures only a fraction of the high-load completion time. The closed-loop model reproduces this rise and conservatively upper-bounds the observed high-load range. Guided by insights from the model, we further design a response-aware discovery policy that reduces mean discovery completion time by 25.3% to 39.7%.** 

**_Index Terms_ —Discovery storm, ROS 2, DDS, RTPS, wireless robotic networks, closed-loop modeling, reliability repair** 

## I. INTRODUCTION 

Wireless robotic networks coordinate robot functions across distributed processes. These systems commonly rely on the Robot Operating System 2 (ROS 2), a de facto standard software framework that uses the Data Distribution Service (DDS) for communication [1]. Before application data can flow, these processes must discover one another and exchange the communication metadata needed to establish data paths [2]. This decentralized startup supports modular deployment and dynamic joining, but the required metadata must be delivered and recognized before the expected communication paths become ready. In a shared wireless environment, discovery messages contend for the channel and can therefore delay system startup or prevent it from completing. 

A _discovery storm_ is a startup regime in which discovery demand exhausts the available wireless service, causing discovery to complete late or not at all [3]. Even two networked devices, such as a robot computer and a server, can reach this regime when many data publishers and subscribers start discovery 

> †Both authors contributed equally to this research. 

> *Corresponding author 

together. By consuming the available wireless bandwidth with redundant retransmission traffic, a discovery storm paralyzes network startup and prevents distributed processes from exchanging time-critical application data. Therefore, ensuring reliable ROS 2 communications requires a comprehensive closed-loop model to capture the self-reinforcing dynamics of ROS 2 DDS discovery. 

Prior work examines discovery overhead from three complementary perspectives. A deterministic airtime analysis quantifies the deployment-driven initial discovery burst and identifies when it approaches channel capacity [3]. Analytical DDS latency models estimate reliability recovery, but rely on an externally fixed packet-delivery ratio [4]. Other studies focus on reducing initial discovery demand via Bloom filters [5], content-based filtering [6], centralized discovery [7], or node composition [8]. The remaining gap is the causal link through which shared-channel delay postpones receiver recognition, prompting further delivery-check and repair traffic. Modeling this link explains why identical first-transmission workloads can yield different repair counts and completion times. 

In this paper, our contributions are as follows: 

- _Modeling._ We formalize the closed-loop dynamics of the discovery storm, in which shared-channel delay triggers periodic timer-driven repair that reenters the shared channel and deepens the delay, separating this repair from the topology-dependent first-transmission burst and quantifying its amplification. 

- _Validation._ In the 18 high-load configurations, an openloop airtime baseline without the feedback predicts only about 17% of the observed high-load completion time. The closed-loop model captures this rise, upper-bounding roughly 90% of high-load completion-time and message observations as a conservative upper-range estimate. 

- _Mitigation._ The model isolates the periodic reliability messages as a tunable source of contention, and we pace them to receiver responses so that they do not contend with pending discovery traffic, reducing participant-wise mean discovery completion time by 25 _._ 3% to 39 _._ 7%. 

The remainder of this paper is organized as follows. Section II reviews DDS discovery and the delay-induced repair amplification that motivates the model. Section III develops the closed-loop discovery model. Section IV evaluates the model and the response-aware policy on an 802.11n testbed. Section V discusses related work, and Section VI concludes. 


Fig. 1. Homogeneous DDS discovery topology used in the evaluation, with _NH_ wireless hosts, _NP_ participants per host, and _NE_ user endpoints per participant. 

## II. BACKGROUND AND MOTIVATION 

## _A. DDS Discovery Protocol_ 

A DDS deployment consists of hosts, participants, and endpoints. A host runs software processes that create DDS participants, and each participant contains endpoints that publish or subscribe to application data, such as sensor readings or motion commands. In general, hosts may contain different numbers of participants, and participants may advertise different numbers of endpoints. Fig. 1 illustrates the homogeneous special case used for controlled evaluation, with _NH_ hosts, _NP_ participants per host, and _NE_ user endpoints per participant. Communication within one host does not traverse the shared wireless link. Two hosts are therefore the smallest setting that exposes cross-host discovery over the shared channel. 

Discovery proceeds in two stages. The Simple Participant Discovery Protocol (SPDP) first announces each participant’s presence and network addresses. After remote participants recognize one another, the Simple Endpoint Discovery Protocol (SEDP) exchanges metadata describing their publishing and subscribing endpoints. SEDP carries this metadata in RealTime Publish-Subscribe (RTPS) DATA submessages. One RTPS packet carried over the User Datagram Protocol (UDP) may contain several submessages [2]. 

SEDP provides reliable delivery through a check-and-repair cycle. A sender transmits SEDP DATA and uses a HEARTBEAT to announce the available DATA sequence numbers. Sequence numbers label SEDP DATA items so that a receiver can identify which items are missing. The receiver returns an ACKNACK identifying which DATA has arrived and which remains missing, and the sender retransmits the requested metadata. The first transmission of an endpoint’s metadata to a receiver is Initial SEDP DATA. Each later transmission of the same metadata to that receiver is Repair SEDP DATA [2]. 

Discovery completion depends on the receiver state rather than sender transmission. Discovery is completed only after every receiver has processed the metadata for all expected remote endpoints. DATA that has been generated but remains queued or in service is still absent from the receiver state. Here, a reliability timer schedules a protocol decision that checks or responds to the receiver’s delivery state. If a reliability timer expires before that DATA is processed, the protocol treats the 

TABLE I 

DISCOVERY MESSAGE COUNTS AVERAGED OVER 15 RUNS FOR _NH_ = 2, _NP_ = 5, AND _NE_ = 20 

|**Message category**|**Wired**|**Wireless**|**Wireless/**<br>**Wired ratio**|
|---|---|---|---|
|SPDP|327.3|529.8|1.6|
|Initial SEDP DATA|1,850.0|1,850.0|1.0|
|Repair SEDP DATA|0.07|3,644.0|54,660|
|HEARTBEAT|102.5|14,036.1|137.0|
|ACKNACK|100.4|3,798.1|37.8|
|**Total**|**2,380.2**|**23,858.1**|**10.0**|


delayed metadata as missing and may initiate the same repair path as an actual loss. 

## _B. Delay and Repair Amplification_ 

Prior studies show that DDS performance depends on multicast load and wireless-channel conditions [9], [10]. Wireless loss can trigger repair, yet loopback runs produce Repair SEDP DATA despite negligible network loss (Subsection IV-C), showing that loss is not required. We therefore focus on the causal path in which delayed delivery postpones receiver recognition and activates the reliability procedure. The resulting checks, replies, and retransmissions increase contention and further delay the remaining metadata. 

Comparing wired and wireless discovery illustrates this amplification. The wired environment provides a low-delay reference, while the wireless environment allows discovery messages to be delayed or remain unreceived when a receiver checks what has arrived. We use a representative high-load deployment with two hosts, five participants per host, and twenty user endpoints per participant, namely _NH_ = 2, _NP_ = 5, and _NE_ = 20. All processes start simultaneously and advertise the same participants and endpoints under both conditions. Table I separates SPDP announcements, initial and repair SEDP DATA, and the associated reliability-control messages. 

Across the measured runs, both environments produce an average of 1,850 initial SEDP DATA submessages. This confirms that the large difference in total traffic does not come from advertising more endpoints. Participant announcements, delivery checks, receiver replies, and retransmissions produce only 2,380.2 discovery submessages in the wired environment. In the wireless environment, the same categories raise the total to 23,858.1 submessages, which is 10 times more than that of the wired traffic. Fig. 2 extends this representative comparison across all evaluated configurations. The wirelessto-wired ratio of run-mean total discovery-message counts rises jointly with _NP_ and _NE_ and reaches 15.7 in the most amplified configuration. 

## III. CLOSED-LOOP DISCOVERY MODEL 

This section turns the feedback mechanism described in Subsection II-B into a closed-loop model. The deployment input describes the system structure, a DDS profile supplies protocol behavior, and a wireless-service profile describes how transmissions are served. The protocol component generates 


Fig. 2. Ratio of the wireless and wired run-mean total discovery-message counts at each evaluated system size. Color follows the surface height. 

messages from receiver state and timers. The wireless-service component determines when each message leaves the sender and reaches the receiver. Each completed delivery updates the state used by subsequent protocol decisions. A different wireless network is represented by its own wireless-service profile. 

## _A. Structural Discovery Workload_ 

Let _H_ = _{_ 0 _, . . . , NH −_ 1 _}_ be the wireless hosts, _P_ = _{_ 0 _, . . . , n −_ 1 _}_ the DDS participants, and _h_ : _P →H_ maps each participant to the host on which it runs. One descriptor is the SEDP metadata that advertises one publishing or subscribing endpoint. Participant _i_ advertises _Di,s_ descriptors of SEDP metadata type _s ∈{_ pub _,_ sub _}_ . Each participant owns separate built-in discovery streams for publication and subscription metadata. For a directed cross-host pair ( _i, j_ ), _i_ ’s publication writer sends descriptions of its data-sending endpoints to _j_ ’s publication reader, while its subscription writer sends descriptions of its data-receiving endpoints to _j_ ’s subscription reader. Each stream maintains independent reliability state and timers. Consequently, every directed pair contributes one reliable publication relation and one reliable subscription relation. 

Table II summarizes the notation used throughout the closedloop discovery model. We denote the set of directed cross-host pairs by _R_ , the total number of required descriptor deliveries across these relations by _F_ , and the number of reliable SEDP relations by _N_ rel: 


The formulation permits uneven participant placement and participant-specific descriptor counts under a common wireless- 

TABLE II 

NOTATION FOR THE CLOSED-LOOP DISCOVERY MODEL 

|**Symbol**|**Meaning**|
|---|---|
|_NH, n, NP , NE_|Hosts, total participants, participants per host, and user<br>endpoints per participant|
|_H, P, h_|Host set, participant set, and the map assigning each<br>participant to a host|
|_R, i, j, s, d_|Directed cross-host participant pairs, with sender,<br>receiver, metadata-type, and descriptor indices|
|_Di,s, F, N_rel|Type-_s_ descriptors advertised by _i_, required descriptor<br>deliveries, and reliable SEDP relations|
|_α_HB_, α_ACK<br>_αe, αm, αu_|Profile counts used for reference HEARTBEAT,<br>ACKNACK, and SPDP traffic|
|_v, c_|Generated RTPS/UDP packet and one uplink or<br>downlink fragment transmission|
|_B_(_c_)_, κ_(_c_)_, a_(_c_)|Fragment byte count, unicast or multicast mode, and<br>wireless service demand|
|_Wi, Ii_(_t_)|Source-queue capacity and admitted bytes of participant<br>_i_|
|_r_(_c_)_, b_(_c_)_, f_(_c_)|Service-request, service-start, and service-finish times of<br>fragment _c_|
|_Pij, R_<sup>(</sup><sup>_s_)</sup><br>_ij _<sup>_, X_(</sup><sup>_s_)</sup><br>_ij,d_|Participant recognition, SEDP relation, and receiver<br>descriptor states|
|_C_<sup>(</sup><sup>_s_)</sup><br>_ij,d_|Sender acknowledgment and repair state for one<br>descriptor|
|E_n,_∆E_n,_(_e, t_)_, ≺_|Pending events, newly scheduled events, a timed event,<br>and event ordering|
|_τA, τN, τS, τH, τP_|HEARTBEAT-response, repair-response, suppression,<br>HEARTBEAT, and SPDP intervals|
|_T_disc<br>_M_init_, M_repair<br>_M_HB_, M_ACK<br>_M_SPDP_,_m<br>_M_SPDP_,_u|Discovery completion time and generated counts by<br>message category|


service and DDS implementation profile. In the homogeneous specialization used for evaluation, _Di,s_ = _Ds_ and 


Even with _NH_ = 2, _F_ grows quadratically with _NP_ and in proportion to the number of advertised endpoints. 

The failure-free reference delivers every required descriptor on its first transmission. It therefore has 


Let _α_ HB and _α_ ACK be the HEARTBEAT and ACKNACK counts per reliable SEDP relation. For SPDP, let _αe_ be the announcement events per participant, _αm_ the multicast SPDP count per event, and _αu_ the average unicast SPDP count per directed cross-host pair. The remaining reference counts are 


It serves as the counterfactual against which timer-generated delivery checks and repair traffic are measured. 

## _B. Shared Wireless Service_ 

Let _v_ denote one generated RTPS/UDP packet, which may contain multiple discovery submessages. Packet _v_ can be divided into IP fragments when required by the configured maximum transmission unit (MTU). Each fragment then follows the configured transmission route, the ordered path from sender to receiver. In the evaluated profile, this path is an uplink from the sender followed by a downlink to the receiver, and the model represents the two transmissions as separate service stages. Let _c_ denote one uplink or downlink fragment transmission waiting for channel service. For such _c_ , _B_ ( _c_ ) is the transmitted byte count and _κ_ ( _c_ ) _∈{_ u _,_ m _}_ indicates whether the transmission is unicast or multicast. Its wireless service demand is 


where _Rκ_ ( _c_ ) is the configured physical-layer rate and _Oκ_ ( _c_ ) includes fixed channel-access and protocol costs. 

A generated packet first waits in the modeled participant backlog. The model moves it to the abstract finite source queue once that queue has sufficient free capacity in bytes. Only admitted fragments can request channel service. All uplink and downlink fragments then share one modeled wireless channel. The channel carries one fragment at a time, so every other admitted fragment waits until the channel becomes available. The model selects the fragment with the earliest service-request time. After the access point (AP) receives one fragment of a packet, it may be ready to forward that fragment just as the sender is ready to send the next fragment. A fixed rule chooses which transmission goes first, and Subsection IV-D evaluates three forms of this rule. A selected fragment occupies the channel for _a_ ( _c_ ). Completion of packet _v_ ’s final uplink fragment frees the byte capacity occupied by _v_ in the modeled source queue, while complete downlink reception can update discovery state. 

More precisely, index the fragments as _c_ 1 _, c_ 2 _, . . ._ in the order selected for channel service. The symbols _r_ ( _cn_ ), _b_ ( _cn_ ), _f_ ( _cn_ ) represent its service-request, service-start, and service-finish times, respectively. For _n ≥_ 2, 


The first fragment uses the channel-availability time in place of _f_ ( _cn−_ 1). A downstream fragment becomes eligible only after its preceding route stage finishes. Thus, an infrastructure-link transmission is represented by an uplink service followed by the required downlink service, while another wireless technology can supply a different ordered route. 

For participant _i_ , let _Wi_ be the finite source-queue capacity and _Ii_ ( _t_ ) its admitted bytes. Generated packets wait in a first-in, first-out participant backlog until their byte demand fits within _Wi − Ii_ ( _t_ ). The demand is released when the final source-side fragment completes. This admission rule preserves traffic that temporarily exceeds the source queue as delay instead of prematurely declaring it delivered or discarded. For packet _v_ , the model therefore distinguishes its generation 


Fig. 3. Closed-Loop discovery service. Channel service controls receiver recognition, while reliability timers return generated checks and repairs to the same service. 


Fig. 4. Writer-side repair state for one descriptor. Confirmation moves any non-A state to A. 

time, source-completion time, and receiver-completion time. Packet _v_ reaches receiver completion only after all of its fragment-transmission stages have completed. Consequently, receiver state remains unchanged while a packet is queued or only partially transmitted. 

_C. Receiver State and Closed-Loop Evolution_ 

For each directed participant pair ( _i, j_ ), the receiver states are 


The value _Pij_ ( _t_ ) = 1 means that participant _j_ has processed participant _i_ ’s SPDP announcement. _Rij_<sup>(</sup><sup>_s_)(</sup><sup>_t_)=1meansthat</sup> their type- _s_ SEDP relation is open, and _Xij,d_<sup>(</sup><sup>_s_)(</sup><sup>_t_)=1means</sup> that _j_ has processed the metadata describing _i_ ’s type- _s_ endpoint indexed by _d_ . An open relation means that the corresponding SEDP writer and reader can begin exchanging discovery DATA and control messages. All three states start at zero. We omit ( _t_ ) when the current event time is clear. The corresponding sender state is 


Sender state _C_<sup>(</sup><sup>_s_)</sup> _ij,d_<sup>distinguishesanunacknowledgeddescriptor</sup> (U), a repair request (R), queued repair generation (Q), sent Repair SEDP DATA (S), and acknowledgment (A). After sending Repair SEDP DATA, the sender waits before it may generate another repair for the same descriptor. This waiting period is called suppression. 

Fig. 4 summarizes the sender-side repair state. 

Every descriptor starts in U. An ACKNACK that reports it missing moves it to R. Repair preparation moves it to Q. Completion of repair source transmission moves it to S, and suppression expiration returns a still-missing descriptor to U. An ACKNACK that confirms delivery moves any non-A state to A. 

A single time-ordered event queue holds message-generation, source-completion, complete-reception, and timer-expiration events. Each pending entry has the form ( _e, t_ ), where _e_ specifies what happens and _t_ gives its scheduled processing time. Let E _n_ denote all entries awaiting processing immediately before step _n_ . Executing the entry selected at this step may schedule zero or more additional entries, whose set is denoted by ∆E _n_ . The queue update is 


where the pending entry ( _en, tn_ ) is selected according to the ordering _≺_ . After it is removed from E _n_ , every newly scheduled entry in ∆E _n_ is inserted to form E _n_ +1. The ordering gives priority to the earliest timestamp. If message reception completes exactly when the protocol is scheduled to check delivery or decide on repair, reception updates receiver state before that decision is made. Wireless service begins after every event scheduled for that time has been processed. Any remaining simultaneous events follow their insertion order. Five protocol timers determine when announcements, replies, repairs, and repeated delivery checks may occur: 

## _τA_ : HEARTBEAT response delay _,_ 


These configured delays and the same-time sequence yield one deterministic trajectory for a fixed deployment, DDS profile, and wireless-service profile. 

Six rules close the feedback loop. Here, DATA denotes SEDP DATA, gen creates a message at its sender, and exp marks timer expiration. The direction _j → i_ identifies an ACKNACK sender and receiver. Finally, SUP _ijs_ denotes suppression expiration: it ends the wait after Repair SEDP DATA is sent, during which another repair for the same descriptor is not generated. The ACKNACK bitmap 


lists the endpoint metadata that _j_ has not processed at time _t_ . An empty bitmap reports no missing metadata. 

- _SPDP reception._ When participant _j_ completely receives participant _i_ ’s SPDP announcement at time _t_ , the model sets _Pij_ = 1 and _Rij_<sup>(</sup><sup>_s_)= 1for</sup><sup>_s ∈{_pub</sup><sup>_,_sub</sup><sup>_}_,thenadds</sup> the relation-opening events specified by the DDS profile. 

- _HEARTBEAT-timer expiration._ When (HB<sup>exp</sup> _, t_ ) is processed for participant _i_ ’s type- _s_ reliable writer, the 

following events are added if at least one descriptor remains unacknowledged: 


Neither event is added if all its descriptors are acknowledged. 

- _HEARTBEAT reception._ When participant _j_ completely receives a HEARTBEAT from participant _i_ ’s type- _s_ SEDP writer at time _t_ , the model adds (ACK<sup>gen</sup> _j→i,s_<sup>_, t_+</sup><sup>_τA_).At</sup> its scheduled time, this event stores **r**<sup>(</sup> _ij_<sup>_s_)(</sup><sup>_t_+</sup><sup>_τA_)inthe</sup> ACKNACK. Once generated, its bitmap does not change. 

- _ACKNACK reception._ When participant _i_ ’s type- _s_ SEDP writer receives participant _j_ ’s ACKNACK with a nonempty bitmap at time _t_ , each newly requested descriptor changes as _Cij,d_<sup>(</sup><sup>_s_):U</sup><sup>_→_R,andthemodel</sup> adds (DATA<sup>gen</sup> _, t_ + _τN_ ). That event moves the requested descriptors from R to Q and generates their Repair SEDP DATA, which enters the backlog and wireless service used by Initial SEDP DATA. 

- _Repair delivery._ Completion of the final uplink fragment of Repair SEDP DATA sent from participant _i_ to participant _j_ at time _t_ changes _Cij,d_<sup>(</sup><sup>_s_): Q</sup><sup>_→_S and adds the suppression-</sup> expiration event (SUP _ijs, t_ + _τS_ ). Complete reception by participant _j_ changes _Xij,d_<sup>(</sup><sup>_s_): 0</sup><sup>_→_1.</sup> 

- _Post-repair wait expiration._ When SUP _ijs_ occurs at time _t_ , every still-unacknowledged descriptor returns as _Cij,d_<sup>(</sup><sup>_s_):</sup> S _→_ U. If at least one descriptor returns to U, (HB<sup>exp</sup> _, t_ + _τH_ ) is added to check its delivery again. 

Only complete receiver delivery updates _P_ , _R_ , or _X_ , so an earlier timer expiration can generate traffic from the preceding receiver state. 

For example, consider an Initial SEDP DATA message carrying descriptor _d_ . If it remains queued when a HEARTBEAT reaches participant _j_ , then _Xij,d_<sup>(</sup><sup>_s_)=0,and</sup><sup>_j_’sACKNACK</sup> snapshots _d_ as missing. The bitmap does not change after the ACKNACK is generated. Even if the initial DATA subsequently reaches _j_ , the ACKNACK generated before that delivery can still cause participant _i_ to prepare Repair SEDP DATA. That repair reenters the same backlog and competes with the remaining descriptors, potentially delaying more receiver updates beyond later timer expirations. A later clean ACKNACK moves _C_<sup>(</sup><sup>_s_)</sup> _ij,d_<sup>toAandendsthisrepairpath.</sup> 

## _D. Model Outputs_ 

Discovery finishes when every required receiver has processed every descriptor advertised by a participant on a different host: 


Before _T_ disc, the model counts each generated logical message in _M_ init, _M_ repair, _M_ HB, _M_ ACK, _M_ SPDP _,_ m, or 

TABLE III EVALUATION PROFILE SUPPLIED TO THE MODEL 

|Component|Evaluated value or behavior|
|---|---|
|Wireless service|IEEE 802.11n, _R_m = 6 Mbps, _R_u _≈_144_._4<br>Mbps|
|ROS 2 descriptors|_D_<sup>ROS</sup><br>pub <sup>= 9 and</sup> <sup>_D_ROS</sup><br>sub<br>= 8 per default node,<br>then one 460-B descriptor per user endpoint|
|SPDP schedule|Immediate transmission, five 100-ms startup<br>callbacks, then period _τP_ = 3 s|
|Fast DDS SEDP timers|<sup>Initial ACKNACK delay</sup> <sup>_τI_ = 70 ms,</sup> <sup>_τH_ = 1</sup><br>s, _τA_ = 10 _µ_s, and _τN_ = 100 _µ_s|
|Fast DDS triggers|First-recognition SPDP resend, relation-open<br>HEARTBEAT, Initial ACKNACK, and byte-<br>threshold piggyback HEARTBEAT|


_M_ SPDP _,_ u, according to its message category. The first generated occurrence of descriptor ( _i, j, s, d_ ) is counted as initial DATA, and every later occurrence is counted as repair DATA. The total message count is the sum of these six categories. A message is counted when it is generated, even if it remains queued or in transmission at _T_ disc. 

## IV. EXPERIMENTAL EVALUATION 

## _A. Experimental Methodology_ 

_1) Testbed and Wireless Configuration:_ The evaluation instantiates the wireless-service component with two identical hosts connected through an infrastructure IEEE 802.11n link. This two-host setup holds the physical deployment fixed while varying participant and endpoint density, revealing how logical discovery load activates feedback over the shared medium. Wi-Fi provides a controlled shared-medium setting in which discovery uplink and AP downlink traffic contend for the same service resource. The evaluation profile uses a multicast rate of 6 Mbps and a unicast rate of approximately 144 _._ 4 Mbps. A separate master host coordinates run start times, while packet capture and discovery execution occur on the two wireless hosts. 

The evaluated Wi-Fi profile specifies the uplink–downlink route, channel-access overheads, transmission rates, and fragment-service order. The receiver state, reliability timers, and message-generation rules in Section III remain applicable when a different wireless technology is adopted. Such a network requires its own route, admission, scheduling, and service parameters in place of the infrastructure Wi-Fi profile. Experimental validation of these alternative service profiles, including mesh and cellular robotic networks, remains as future work. 

_2) DDS Instantiation:_ This subsection instantiates the general model inputs with the ROS 2 and Fast DDS configuration used in the experiments. Table III first summarizes the resulting evaluation profile. We then explain how its entries determine the discovery workload and protocol events. 

The experiments use ROS 2 with Fast DDS 2.6.11. A default ROS 2 node contributes 


The evaluated workload adds _NE_ application endpoints, so the descriptor count used in Section III-A satisfies 


Each participant advertises this many endpoint descriptions. The airtime required to advertise these descriptors depends on their size. Fast DDS includes each endpoint’s topic name, data type, and communication settings in its SEDP DATA, so a UDP packet carrying one default descriptor ranges from 452 to 532 B. Each additional application endpoint uses 460 B in the evaluated configuration. The model uses these sizes when Fast DDS groups endpoint descriptions into packets and computes the resulting fragment sizes _B_ ( _c_ ). 

The profile also preserves the implementation behaviors that change traffic generation. Fast DDS sends SPDP announcements by multicast and, after learning another participant’s address, also sends a unicast copy directly to that participant. When an SEDP relation opens at time _t_ , the Fast DDS profile adds (HB<sup>gen</sup> _, t_ ) and, if needed, (HB<sup>exp</sup> _, t_ + _τH_ ). An Initial ACKNACK is an optional RTPS optimization that Fast DDS implements with an Initial ACKNACK timer. When participant _j_ opens a type- _s_ relation to participant _i_ at time _t_ , the evaluation model adds (ACK<sup>exp</sup> _j→i,s_<sup>_, t_+</sup><sup>_τI_),where</sup><sup>_τI_=70ms.Ifno</sup> HEARTBEAT has arrived when this event is processed, _j_ generates an Initial ACKNACK and schedules another attempt with twice the delay. RTPS allows one message to carry multiple submessages [2], and Fast DDS uses this flexibility to append a piggyback HEARTBEAT to outgoing SEDP DATA when the writer reaches its configured byte threshold. Repair DATA share this allowance and the same wireless service as initial DATA. Table III therefore supplies the model with the timer values and optional triggers of the evaluated Fast DDS implementation. 

The model inputs are fixed before the model-to-observation comparison. Host placement and descriptor counts come from the workload configuration. Descriptor byte sizes come from the serialized Fast DDS discovery metadata, while the reliability timers and message-generation triggers come from the Fast DDS profile. The physical-layer rates, fragment route, queue rule, and service order come from the evaluated wireless profile. Measured completion times and message counts are then used to evaluate the resulting model predictions. 

_3) Workload and Synchronized Runs:_ The evaluation fixes _NH_ = 2, the smallest cross-host setting, while varying _NP ∈ {_ 1 _, . . . ,_ 6 _}_ and _NE ∈{_ 2 _,_ 4 _, . . . ,_ 30 _}_ , producing 90 participantendpoint configurations. Each configuration is repeated 15 times. Every participant creates approximately half of its user endpoints as publishers and the remainder as subscribers over application-level topics. 

Before each run, the hosts synchronize their clocks to the master using chronyc. The master distributes a target time, and both hosts start packet capture and load the workload before that time. At the target, each process begins creating its ROS 2 node and configured endpoints, which starts SPDP and SEDP. Each process polls the ROS middleware (RMW) matched-endpoint counters every millisecond. The first instant 

at which all expected matches are visible is the application-level discovery completion time. 

_4) Trace Processing and Merge:_ Each host records its transmitted packets, and the two source-side captures are merged by run so that a packet observed at both hosts is not counted twice. The application completion time is the observation cutoff. Because one RTPS/UDP packet can carry several submessages, we count each contained SPDP, SEDP DATA, HEARTBEAT, and ACKNACK separately. 

SEDP DATA is keyed by source and destination globally unique identifier (GUID) prefixes, SEDP writer entity, and writer sequence number. The first occurrence of a key is initial DATA, and later occurrences are repair DATA. HEARTBEAT and ACKNACK counts are restricted to the reliable SEDP endpoints. Before aggregation, we verify that the merged capture contains at least one SEDP DATA occurrence for every required descriptor key defined in Section III. The reference itself is checked separately against topology-normalized loopback captures in Subsection IV-C. 

## _B. Burst and Repair Separation_ 

We first separate topology-determined traffic from wireless amplification by comparing loopback, Ethernet, and Wi-Fi over the evaluated configuration range. Fig. 5 reports total discovery submessages and ACKNACKs for these three environments. 

The loopback measurements follow the model’s firsttransmission reference across all 90 configurations, and Ethernet shows the same failure-free trend. Their totals therefore provide a failure-free reference for each configuration. Relative to this reference, Wi-Fi produces substantial increases in both total and ACKNACK counts as delayed receiver recognition generates additional control traffic. This excess traffic, rather than topology-driven growth alone, is the closed-loop signature of a discovery storm. 

## _C. Wireless Completion Scaling_ 

To evaluate the model’s first-transmission delivery reference with negligible network loss, we use loopback captures. Loopback places all participants on one host, so its number of participant relations differs from that of the evaluated multihost topology. Each participant in a topology with _NH_ hosts and _NP_ participants per host must discover ( _NH −_ 1) _NP_ crosshost peers. Here, peers are the other participants that must be discovered. They exclude the participant itself. Let _lP_ be the number of participants in one loopback run. Matching the peer count gives _lP_ = ( _NH −_ 1) _NP_ +1. For the evaluated _NH_ = 2, _NP_ = 5 therefore gives _lP_ = 6. SEDP DATA, HEARTBEAT, and ACKNACK counts scale with directed participant pairs: _NH_ ( _NH −_ 1) _NP_<sup>2inthemulti-hosttopologyand</sup><sup>_lP_(</sup><sup>_lP−_1)in</sup> loopback. Under the evaluated Fast DDS startup profile, SPDP counts scale with the square of the participant population, giving ( _NH NP_ )<sup>2</sup> and _lP_<sup>2,respectively.Theratiosgive</sup> 


TABLE IV 

EMPIRICAL UPPER-RANGE BEHAVIOR BY PARTICIPANT COUNT 

|Scope|Top.|Runs|Quantity|Cov.|Med. _M/O_ [IQR]|
|---|---|---|---|---|---|
|_NP_ = 1|15|225|Completion<br>Messages|5.8%<br>28.4%|1.35 [1.28, 1.40]<br>1.34 [1.14, 1.36]|
|_NP_ = 2|15|225|Completion<br>Messages|64.4%<br>94.2%|1.51 [1.26, 2.66]<br>2.24 [1.61, 2.98]|
|_NP_ = 3|15|225|Completion<br>Messages|80.9%<br>99.1%|2.70 [1.72, 3.94]<br>2.47 [1.77, 3.29]|
|_NP_ = 4|15|225|Completion<br>Messages|75.1%<br>97.8%|1.75 [1.38, 2.71]<br>1.98 [1.57, 2.68]|
|_NP_ = 5|15|225|Completion<br>Messages|85.8%<br>95.6%|1.77 [1.40, 2.50]<br>1.74 [1.38, 2.20]|
|_NP_ = 6|15|225|Completion<br>Messages|96.0%<br>90.2%|2.14 [1.68, 2.84]<br>1.58 [1.27, 1.98]|
|All|90|1,350|Completion<br>Messages|68.0%<br>84.2%|1.96 [1.44, 2.93]<br>1.85 [1.40, 2.63]|
|**High load**|**18**|**270**|**Completion**<br>**Messages**|**90.7%**<br>**90.4%**|**1.98 [1.52, 2.73]**<br>**1.56 [1.29, 2.07]**|


Each _NP_ scope contains 225 runs over 15 values of _NE_ . High load denotes _NP ≥_ 4 and _NE ≥_ 20. Coverage is the fraction satisfying _O ≤ M_ . Med. _M/O_ [IQR] gives the median and interquartile range among covered runs. 

Initial and Repair SEDP DATA, HEARTBEAT, and ACKNACK counts are multiplied by _c_ pair, while SPDP multicast and unicast counts are multiplied by _c_ SPDP. Loopback runs contain some Repair SEDP DATA in 48 configurations, showing that retransmissions can occur even without wireless delivery. 

Fig. 6 compares application-level wireless discovery completion with the open-loop airtime and closed-loop models under the Section III zero middleware-to-application propagationdelay assumption. Across the 18 high-load configurations, the open-loop airtime model predicts a median 17.1% of the observed topology mean (IQR 15.7%–18.4%), missing the sharp increase. The closed-loop model captures this increase through feedback from delayed recognition to additional check and repair traffic. 

## _D. Model Fit by Message Class_ 

For the failure-free reference, the topology-normalized loopback measurements have a mean absolute percentage error (MAPE) of 0 _._ 82% for total submessages. The messageclass MAPEs are 0 _._ 33%, 0 _._ 68%, 4 _._ 14%, and 8 _._ 17% for SPDP multicast, SPDP unicast, HEARTBEAT, and ACKNACK, respectively. 

Table IV reports the model’s upper-range behavior for the wireless runs. Let _O_ denote the value observed in one run and _M_ the corresponding model prediction. Coverage is the fraction of runs satisfying _O ≤ M_ . For covered runs, the model-toobservation ratio _M/O_ quantifies the remaining margin, with 1 denoting equality. 

At low load, omitted middleware processing, polling, and contention-independent losses can dominate. Shared-airtime feedback instead dominates the targeted high-load region ( _NP ≥_ 4 and _NE ≥_ 20). Table IV shows respective coverage of 90 _._ 7% and 90 _._ 4% for completion time and total messages, with median covered-run _M/O_ ratios of 1.98 and 1.56. 


Fig. 5. Total discovery submessages (top row) and ACKNACKs (bottom row) for loopback, Ethernet, and Wi-Fi. Loopback and Ethernet use the same vertical scale in each row. In the Wi-Fi panels, the blue line connects configuration means. 


Fig. 6. Wireless discovery completion versus workload. Points show application proxy-match timestamps, and blue connects configuration means. The gray dashed line adapts the open-loop airtime model [3] to the fixed first-transmission traffic, while red shows closed-loop SEDP first-recognition completion. 

Instantaneous startup and per-fragment overhead can contribute to this upper-range tendency. In experiments, endpoint creation is staggered under OS scheduling, and 802.11n A-MPDU aggregation can reduce effective per-frame overhead. The model therefore provides conservative upper-range estimates in the storm regime. 

Repair SEDP DATA is the most sensitive metric because packet capture cannot identify whether each duplicate was caused by radio-frequency (RF) failure, queue delay, reordering, or late receiver processing. We therefore report retransmission fit as diagnostic evidence, not as a direct estimate of physical packet loss. 

We evaluate how the AP decides which transmission goes first when the sender is ready to send the next fragment of a packet at the same time that the AP is ready to forward the 

preceding fragment to the receiver. FIFO-Uplink chooses the sender-to-AP transmission, while FIFO-Downlink chooses the AP-to-receiver transmission. Under Datagram-Uplink, the AP receives all uplink fragments of a packet before forwarding any of them on the downlink. Across 90 configurations, the median and maximum completion-time spreads are 0 _._ 43% and 5 _._ 53%. Total messages vary by at most 1 _._ 95%, and each recoverymessage class varies by at most 3 _._ 26%. The small spreads show that the reported trends are insensitive to the choice among the three tested ordering policies. 

## _E. Model-Guided HEARTBEAT Adaptation_ 

The message-class decomposition identifies periodic HEARTBEAT timing as a tunable source of wireless contention. Because the default interval does not reflect reader responses, HEARTBEATs can contend with pending SEDP DATA during a storm. We test a response-aware schedule to mitigate this effect, consistent with the broader observation that periodic network processes can synchronize and concentrate shared load [11]. 

The adaptation changes only periodic HEARTBEATs from the Fast DDS stateful SEDP writers, retaining the default relation-open, ACKNACK-triggered, and piggyback paths. At each cycle, the writer sends a periodic HEARTBEAT to the set _U_ of readers that have not acknowledged all advertised DATA and records its highest announced sequence number _q_ . A reader is responsive if its ACKNACK arrives within period _T_ with an empty bitmap and a base greater than _q_ , indicating no missing DATA through _q_ . Let _H_ = _|U|_ count the contacted readers and _A_ the responsive readers. We then set 


Fig. 7. Discovery completion with the default and adaptive HEARTBEAT implementations. Sky-blue circles and orange triangles denote individual baseline and adaptive runs, respectively. The blue and orange lines connect the corresponding per-configuration means. 

TABLE V 

TOPOLOGY-BALANCED ADAPTATION SUMMARY BY _NP_ . 

||Complet|ion|Total messag|es|
|---|---|---|---|---|
|_NP_|B/A (s)|∆(%)|B/A|∆(%)|
|1|0.147/0.110|-25.3|97.7/97.4|-0.4|
|2|0.216/0.135|-37.8|537.4/531.5|-1.1|
|3|0.571/0.344|-39.7|2315.5/2217.0|-4.3|
|4|1.689/1.158|-31.5|7466.1/8152.8|+9.2|
|5|3.127/1.991|-36.3|18116.0/21153.4|+16.8|
|6|4.307/2.886|-33.0|37939.7/42544.4|+12.1|


_B_ and _A_ denote the baseline and adaptive means, respectively. 

Each writer starts with _T_ = 1 s. Table III provides ( _T_ min _, T_ max) = (0 _._ 1 _,_ 3 _._ 0) s, and _ϵ_ = 0 _._ 05 keeps _λ_ positive when _A_ = 0. If _A_ = _H_ before _T_ expires, the next period becomes the elapsed response time. If _T_ expires with _A < H_ , the cycle extends to _T_<sup>_⋆_</sup> , pacing HEARTBEATs to unconfirmed readers in batches of _⌈Hλ⌉_ until _T_<sup>_⋆_</sup> . The period returns to 1 s when no unacknowledged change remains. 

We compare default and adaptive Fast DDS over the same 90 configurations in Subsection IV-A. This leaves 1,350 observations each for the baseline and adaptive configurations. Fig. 7 shows their individual completion times and configuration means, with mean reductions of 25 _._ 3% to 39 _._ 7% across participant counts. 

Table V equally weights the 15 endpoint-count means for each _NP_ after averaging runs by configuration. At _NP ≥_ 4, total-message counts rise by 9 _._ 2% to 16 _._ 8%, while completion time falls by 31 _._ 5% to 36 _._ 3%. Thus, the schedule improves completion by changing when traffic contends with pending discovery DATA, not by consistently reducing its volume. 

## V. RELATED WORK 

_Discovery scaling and reduction._ Prior work quantifies the first-transmission SPDP and SEDP burst that precedes a discovery storm [3], whereas our model captures the closedloop feedback that can stall discovery even between two hosts. Wireless broadcast-storm research instead attributes overload to 

redundant rebroadcasts, contention, and collisions [12]. DDSspecific techniques reduce initial demand through metadata compression [5], content-based filtering [6], centralized discovery [7], node composition [8], or a compact representation [13]. Across these studies, the primary quantities are initial metadata demand and redundant dissemination traffic. 

_DDS over wireless robotic networks._ ROS 2 and DDS have been benchmarked across middleware implementations [14], [15] and multi-node latency paths [16]. DDS has also been studied under multicast load [9], industrial wireless channels [10], lossy autonomous links [17], and ROS 2 swarm deployments [18]. These measurements establish implementation choice, network conditions, and deployment scale as major determinants of performance. 

_Reliability modeling and network adaptation._ Formal DDS timing analysis bounds data delivery for Fast DDS [19], while analytical reliability models use an externally specified packet-delivery ratio [4]. Periodic-message studies show how timers can synchronize shared load [11], and networkaware ROS resource management adapts communication using programmable-network information [20]. In these models, delivery conditions enter as timing bounds, specified probabilities, or external network information. 

_Relation to this work._ Our model links shared-channel service to the metadata recognized by each receiver, whose state then governs delivery checks and repairs. The resulting traffic reenters the shared channel and changes when the remaining discovery messages arrive. This closed loop connects traffic generation with delivery instead of treating either one as a fixed input. 

## VI. CONCLUSIONS AND FUTURE WORK 

This work separates the endpoint information required at startup from the feedback that turns delayed delivery into a discovery storm. The model links shared-channel delivery, receiver-recognized state, and reliability traffic to the resulting metadata delay. A high density of endpoints and discovery relations can activate this feedback even between a robot computer and its control station. 

Experiments across 90 two-host configurations show that the model tracks configuration-level trends in discovery completion and message overhead while approximating their observed upper range. These results show how delayed delivery amplifies repair and delivery-check traffic beyond the failure-free reference. 

Response-aware HEARTBEAT pacing reduces mean completion time by 25 _._ 3% to 39 _._ 7%, even when total traffic increases, showing that recovery timing matters in addition to volume. This adaptation is a first mitigation step. We will use the model to suppress the feedback loop itself and move wireless discovery toward the failure-free reference. We will also extend the model and its validation beyond synchronized homogeneous startup to asynchronous joins, other DDS implementations, and additional wireless networks. 

REFERENCES 

- [1] S. Macenski, T. Foote, B. Gerkey, C. Lalancette, and W. Woodall, “Robot Operating System 2: Design, architecture, and uses in the wild,” _Science Robotics_ , vol. 7, no. 66, p. eabm6074, May 2022. 

- [2] Object Management Group, “The Real-Time Publish-Subscribe Protocol: DDS Interoperability Wire Protocol (DDSI-RTPS), Version 2.5,” Object Management Group, Tech. Rep. formal/22-04-01, Apr. 2022. [Online]. Available: https://www.omg.org/spec/DDSI-RTPS/2.5 

- [3] S. Lee, Y. Choi, J. Chae, and K.-J. Park, “Discovery Storm: Scalability analysis of DDS and Zenoh in large-scale wireless robotic networks,” in _Proceedings of IEEE INFOCOM_ , May 2026, pp. 1–6. 

- [4] H.-S. Park, S. Lee, D. Um, H. Ryu, and K.-J. Park, “An analytical latency model of the Data Distribution Service in ROS 2,” in _Proceedings of IEEE INFOCOM_ , May 2025, pp. 1–10. 

- [5] J. Sanchez-Monedero,´ J. Povedano-Molina, J. M. Lopez-Vega,´ and J. M. Lopez-Soler, “Bloom filter-based discovery protocol for DDS middleware,”´ _Journal of Parallel and Distributed Computing_ , vol. 71, no. 10, pp. 1305– 1317, Oct. 2011. 

- [6] K. An, A. S. Gokhale, D. C. Schmidt, S. Tambe, P. Pazandak, and G. Pardo-Castellote, “Content-based filtering discovery protocol (CFDP): Scalable and efficient OMG DDS discovery protocol,” in _Proceedings of the 8th ACM International Conference on Distributed Event-Based Systems (DEBS)_ , May 2014, pp. 130–141. 

- [7] F. Luo, Y. Ren, Y. Yu, Y. Li, Q. Liu, and X. Zhang, “A centralized discovery-based method for integrating Data Distribution Service and Time-Sensitive Networking for In-Vehicle Networks,” _Ad Hoc Networks_ , vol. 178, p. 103950, Nov. 2025. 

- [8] S. Macenski, A. Soragna, M. Carroll, and Z. Ge, “Impact of ROS 2 node composition in robotic systems,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 7, pp. 3996–4003, Jul. 2023. 

- [9] K. Peeroo, P. Popov, and V. Stankovic, “Exploring the effects of multicast communication on DDS performance,” in _Proceedings of the 18th European Dependable Computing Conference (EDCC) Student Forum_ , Sep. 2022. 

- [10] B. Almadani, M. N. Bajwa, S.-H. Yang, and A.-W. A. Saif, “Performance evaluation of DDS-based middleware over wireless channel for reconfigurable manufacturing systems,” _International Journal of Distributed Sensor Networks_ , vol. 11, no. 7, p. 863123, Jul. 2015. 

- [11] S. Floyd and V. Jacobson, “The synchronization of periodic routing messages,” _IEEE/ACM Transactions on Networking_ , vol. 2, no. 2, pp. 122–136, Apr. 1994. 

- [12] S.-Y. Ni, Y.-C. Tseng, Y.-S. Chen, and J.-P. Sheu, “The broadcast storm problem in a mobile ad hoc network,” _Wireless Networks_ , vol. 8, no. 2–3, pp. 153–167, 2002. 

- [13] W.-P. Nwadiugwu, D.-S. Kim, W. Ejaz, and A. Anpalagan, “MAD-DDS: Memory-efficient automatic discovery Data Distribution Service for largescale distributed control network,” _IET Communications_ , vol. 17, no. 12, pp. 1432–1446, Jul. 2023. 

- [14] Y. Maruyama, S. Kato, and T. Azumi, “Exploring the performance of ROS 2,” in _Proceedings of the 13th ACM International Conference on Embedded Software (EMSOFT)_ , Oct. 2016, pp. 1–10. 

- [15] V. Bode, D. Buettner, T. Preclik, C. Trinitis, and M. Schulz, “Systematic analysis of DDS implementations,” in _Proceedings of the 24th ACM/IFIP International Middleware Conference_ , 2023, pp. 234–246. 

- [16] T. Kronauer, J. Pohlmann, M. Matthe,´ T. Smejkal, and G. Fettweis, “Latency analysis of ROS 2 multi-node systems,” in _Proceedings of the 2021 IEEE International Conference on Multisensor Fusion and Integration for Intelligent Systems (MFI)_ , Sep. 2021, pp. 1–7. 

- [17] P. Thulasiraman, Y. K. D. Cheng, and B. Allen, “Evaluation of the Data Distribution Service for a lossy autonomous hybrid system,” in _Proceedings of the 2022 IEEE International Systems Conference (SysCon)_ , Apr. 2022, pp. 1–8. 

- [18] J.-B. Castillo-Sanchez,´ E. Gonzalez-Parada,´ and J.-M. Cano-Garc´ıa, “Swarm robot communications in ROS 2: An experimental study,” _IEEE Access_ , vol. 12, pp. 142 930–142 943, 2024. 

- [19] G. Sciangula, D. Casini, A. Biondi, C. Scordino, and M. Di Natale, “Bounding the data-delivery latency of DDS messages in real-time applications,” in _Proceedings of the 35th Euromicro Conference on Real-Time Systems (ECRTS)_ , ser. Leibniz International Proceedings in Informatics, vol. 262, Jul. 2023, pp. 9:1–9:26. 

- [20] G. Szabo, “Toward the automatic network resource management of Robot´ Operating System in programmable mobile networks,” _IEEE Access_ , vol. 11, pp. 65 934–65 955, 2023. 

