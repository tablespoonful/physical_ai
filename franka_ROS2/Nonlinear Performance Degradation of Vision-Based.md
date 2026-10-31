---
title: "Nonlinear Performance Degradation of Vision-Based Teleoperation under Network Latency"
date: "2026-03-06"
authors: "Aws Khalil; Jaerock Kwon"
url: https://arxiv.org/abs/2603.06850
pdf: https://arxiv.org/pdf/2603.06850
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.06850)** / [論文ページ](https://arxiv.org/abs/2603.06850)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Nonlinear Performance Degradation of Vision-Based Teleoperation under Network Latency** 

Aws Khalil<sup>1</sup> and Jaerock Kwon<sup>2</sup> 

**_Abstract_ — Teleoperation is increasingly being adopted as a critical fallback for autonomous vehicles. However, the impact of network latency on vision-based, perception-driven control remains insufficiently studied. The present work investigates the nonlinear degradation of closed-loop stability in camerabased lane keeping under varying network delays. To conduct this study, we developed the Latency-Aware Vision Teleoperation testbed (LAVT), a research-oriented ROS 2 framework that enables precise, distributed one-way latency measurement and reproducible delay injection. Using LAVT, we performed 180 closed-loop experiments in simulation across diverse road geometries. Our findings reveal a sharp collapse in stability between 150 ms and 225 ms of one-way perception latency, where route completion rates drop from 100% to below 50% as oscillatory instability and phase-lag effects emerge. We further demonstrate that additional control-channel delay compounds these effects, significantly accelerating system failure even under constant visual latency. By combining this systematic empirical characterization with the LAVT testbed, this work provides quantitative insights into perception-driven instability and establishes a reproducible baseline for future latencycompensation and predictive control strategies. Project page, supplementary video, and code are available at https:// bimilab.github.io/paper-LAVT** 

**_Index Terms_ — Teleoperation; Network Latency; VisionBased Control; Lane Keeping; Autonomous Driving; ClosedLoop Control; Perception-Driven Control** 

## I. INTRODUCTION 

Teleoperation has emerged as an important fallback and transitional capability for autonomous driving systems, enabling remote intervention when onboard autonomy is unable to safely resolve a situation. Recent industrial deployments and research prototypes increasingly rely on teleoperation to handle edge cases, disengagements, and recovery scenarios without requiring a safety driver onboard [1], [2]. As teleoperation becomes more tightly coupled with autonomous driving pipelines, understanding its operational limitations under realistic network conditions has become a critical research challenge. 

A fundamental limitation of teleoperation is its sensitivity to network-induced latency. Teleoperated driving relies on a closed-loop exchange of sensory information and control commands between a remote client and a vehicle-side execution stack. Delays in this loop introduce stale observations and delayed actuation, which can degrade control performance and, in extreme cases, induce instability. This challenge is particularly pronounced in continuous control tasks 

Both authors are with the Department of Electrical and Computer Engineering, University of Michigan - Dearborn, Dearborn, MI, USA. awskh@umich.edu<sup>1</sup> , jrkwon@umich.edu<sup>2</sup> 

such as lane keeping, where timely perception and feedback are essential for maintaining stable vehicle behavior. 

Prior work has demonstrated that increasing network latency leads to measurable degradation in teleoperated driving performance, and has established latency tolerance benchmarks under controlled experimental conditions [3]. However, existing system-centric latency studies predominantly rely on localization- or map-based control pipelines, often using LiDAR perception and geometric path-following controllers. In such settings, perception is relatively decoupled from control timing, and sensing delay has a limited impact on control stability. 

In contrast, vision-based teleoperation introduces a distinct set of challenges. Camera-driven perception pipelines operate directly on image data and are inherently sensitive to temporal misalignment between visual observations and vehicle motion. Even moderate perception delay can result in outdated lane geometry, shifted visual features, or misaligned control inputs, particularly in closed-loop control settings. Although cameras are widely used in autonomous driving and teleoperation systems, the impact of network latency on _vision-based, perception-driven lane keeping_ has not been systematically studied. 

This paper addresses this gap by focusing explicitly on the effect of network-induced latency on camera-based lane keeping under teleoperation. Rather than proposing new teleoperation architectures, prediction mechanisms, or latency mitigation strategies, the goal of this work is to _characterize_ how delayed visual feedback affects closed-loop control behavior in a controlled and repeatable setting. To this end, we introduce a research-oriented ROS 2 teleoperation system, referred to as the _Latency-Aware Vision Teleoperation testbed_ (LAVT), designed specifically to support systematic latency studies for vision-based control. 

LAVT enables distributed execution across client and server nodes, explicit time-stamping of perception and control signals, and controlled injection of network latency using standard Linux traffic control tools. While the system is deployable on a full-scale drive-by-wire research vehicle, all experiments in this paper are conducted in simulation to ensure safety, repeatability, and isolation of latency effects from confounding real-world factors. LAVT is designed specifically to enable controlled and reproducible latency characterization in vision-based teleoperation. The framework prioritizes measurement transparency, timing fidelity, and experimental controllability over feature completeness, making it suitable for systematic latency analysis across both simulation and real-vehicle deployments. 

Using LAVT, we perform a systematic evaluation of how increasing network latency affects the stability and tracking performance of a vision-based lane-keeping controller operating in a closed loop. The study highlights degradation trends and failure modes that emerge as perception and control become increasingly desynchronized. These results provide empirical insights into the sensitivity of perceptiondriven control to latency and inform the design of future teleoperation and autonomous driving systems that rely on camera-based perception. 

The contributions of this paper are threefold: 

- We provide empirical insights into degradation patterns and failure modes specific to perception-driven control under delayed visual feedback, without introducing mitigation or predictive strategies. 

- We conduct a systematic simulation-based evaluation of how network-induced latency impacts stability and tracking performance in vision-based teleoperated lane keeping. 

- We present LAVT, a research-oriented ROS 2-based teleoperation testbed designed to enable controlled studies of network latency effects on vision-based closedloop driving, implemented in the CARLA simulation [4] and integrated with a full-scale drive-by-wire research vehicle. 

## II. RELATED WORK 

Teleoperation has been widely studied in autonomous driving, including system architectures, operator interfaces, communication pipelines, and human-in-the-loop evaluation. This section focuses on prior work most relevant to networkinduced latency in teleoperated driving and vision-based control. 

_1) Teleoperation Systems and Frameworks for Autonomous Driving:_ Several teleoperation software stacks have been proposed to enable remote driving and assistance for autonomous vehicles. Open-source and modular frameworks support distributed deployment, operator interfaces, and integration with simulation and real vehicles [2], [5], [6]. Kerbl et al. introduced a ROS 2-based framework integrating remote driving, remote assistance, and Autoware, emphasizing modularity and deployability [1]. These works primarily address architectural design and operational feasibility. Although they recognize latency as a system concern, they do not explicitly isolate or quantify the latency in closed-loop, perception-driven vehicle control. In contrast, the present study uses a dedicated testbed to systematically analyze latency-induced degradation in visionbased lane keeping. 

_2) Latency in Teleoperated Driving:_ The impact of network latency on teleoperated driving has been investigated in several studies. Alsolami et al. conducted a system-centric evaluation using LiDAR-based localization and geometric path-following control, identifying latency tolerance thresholds under controlled delay injection [3]. 

Other work has examined teleoperation reliability under network impairments, often emphasizing human oper- 

ators. Tener et al. analyzed constrained-network teleoperation focusing on operator behavior and safety [7]–[10]. Implementation-oriented feasibility studies were reported by Kim et al. and Sato et al. [11]–[13]. From a networking perspective, Fezeu et al. analyzed teleoperation over commercial 5G networks, highlighting tail-latency variability [14]. 

While these works demonstrate that latency affects teleoperated driving performance, they primarily consider humanin-the-loop systems or localization-based control pipelines. The degradation mechanisms introduced by delayed visual perception in camera-driven closed-loop control remain insufficiently studied. 

_3) Vision-Based Control and Perception Delay:_ Visionbased perception is central to modern lane detection and lateral control, but camera pipelines are sensitive to temporal misalignment between perception and vehicle motion. Prior research has studied perception delay and mitigation strategies in autonomous driving and robotics [15], [16], and surveys have identified latency as a fundamental challenge in networked robotic systems [17]. 

In teleoperation, video streaming under network constraints has largely been evaluated in terms of operator situational awareness and communication efficiency [18], [19], without analyzing closed-loop autonomous control under delayed visual feedback. 

The present work focuses on characterizing the impact of network-induced latency on a vision-based, perceptiondriven lane-keeping controller operating in a closed loop, exposing degradation patterns specific to delayed camera feedback. 

## III. METHOD 

## _A. Latency-Aware Vision Teleoperation Testbed_ 

LAVT is a distributed ROS 2 framework for controlled evaluation of network-induced latency in vision-based closed-loop teleoperation. The system separates perception, transport, and control layers while providing explicit timestamping and one-way latency measurement. 

LAVT operates across two nodes: a _server_ (vehicle side) and a _client_ (remote side). 

_a) Server:_ The server hosts the vehicle platform (CARLA or a DBW-enabled vehicle), acquires camera frames, embeds send-time stamps, streams video via RTP/H.264 over UDP, receives control commands, and applies actuation. 

_b) Client:_ The client receives and decodes the video stream, extracts embedded timestamps for one-way latency estimation, executes a vision-based lane-keeping controller, and transmits time-stamped control commands. 

Both human teleoperation and remote autonomous driving are supported. All experiments in this study use a deterministic client-side controller to eliminate human reaction variability and ensure repeatable latency sensitivity analysis. The autonomy module shares the same communication pathways as teleoperation, so injected network delay affects both modes identically. 


Fig. 1. Architecture of the Latency-Aware Vision Teleoperation testbed (LAVT). The system operates in a distributed client–server configuration. On the vehicle side (server), a forward-facing camera publishes a local ROS 2 image topic. A video bridge node subscribes to this topic and transmits frames via a dedicated RTP/H.264 stream (GStreamer) over UDP. On the remote side (client), a corresponding video bridge decodes the stream and republishes the received frames as a local ROS 2 image topic for downstream processing by either a teleoperator interface or a vision-based autonomy module. Control commands are exchanged as ROS 2 topics over rmw zenoh, with independent Zenoh routers running on both server and client and connected via configured peer-to-peer sessions. The blue path denotes the perception channel with one-way video latency _τv_ , while the orange path denotes the actuation channel with one-way control latency _τc_ . Linux Traffic Control and Network Emulator (TC NetEm) is applied independently on each direction to inject controlled delay. Chrony provides system-level clock synchronization between machines, enabling accurate offset estimation and one-way latency computation using embedded frame timestamps. The resulting architecture forms a fully closed-loop teleoperation system suitable for systematic latency characterization in both simulation and real-vehicle deployments. 

_c) Real-vehicle integration:_ Although quantitative experiments are conducted in simulation, LAVT has been integrated with a full-scale drive-by-wire research vehicle (Fig. 2). Only sensing and actuation interfaces differ; streaming, synchronization, and latency measurement remain unchanged. 


Fig. 2. A full-scale drive-by-wire (DBW) research vehicle integrated with LAVT for real-world deployment. The DBW system includes brake, throttle, steering, and shift-by-wire control modules. The platform is equipped with a multi-sensor suite including LiDAR, RGB cameras, and GPS. While quantitative latency experiments in this study are conducted in simulation, the complete teleoperation and streaming stack has been integrated with this vehicle without architectural modification. 

teleoperation scenarios in which vehicle and operator nodes may be separated by routed networks or cloud infrastructure. Zenoh [21] enables flexible discovery and communication across heterogeneous network topologies without modifying application-layer logic. 

## _C. Closed-Loop Control Under Asymmetric Delay_ 

We model the closed-loop teleoperation dynamics with separate perception and actuation delays. Let _It_ denote the camera observation captured on the server at time _t_ , and let _ut_ denote the control command applied to the vehicle at time _t_ . The remote policy/controller _π_ ( _·_ ) operates on delayed observations, 


where _τv_ is the end-to-end video (server _→_ client) latency. The vehicle state _xt_ evolves under delayed actuation, 


## _B. ROS 2 Middleware Configuration_ 

LAVT uses ROS 2 with the rmw ~~z~~ enoh ~~c~~ pp backend [20] to support routed and peer-to-peer deployment across distributed networks. This property is particularly relevant for 

where _τc_ is the control (client _→_ server) latency. This formulation cleanly separates perception and actuation delay channels and supports independent latency injection for each direction (Section III-F). 

_D. Video Transport via GStreamer RTP/H.264_ 

Video is transmitted using RTP over UDP with H.264 encoding via GStreamer [22]. The server pipeline is: 

appsrc _→_ H.264 encoder _→_ rtph264pay _→_ udpsink 

The client pipeline is: 

udpsrc _→_ rtpjitterbuffer _→_ rtph264depay _→_ decoder _→_ appsink 

RTP payloading, depayloading, and jitter buffering elements [23]–[25] introduce codec and buffering delays depending on configuration. Measured latencies under each experimental condition are reported in Section V. 

## _E. Time Synchronization and One-Way Latency Measure-_ 

_ment_ 

Accurate one-way latency measurement requires crossmachine clock alignment. All nodes run Chrony [26], [27] to discipline system clocks and minimize drift. 

The inter-machine clock offset ∆ is obtained directly from Chrony synchronization reports: 


An optional RTT-based probe provides redundancy under a symmetric-delay assumption. The estimated ∆ is used to convert timestamps when computing one-way video and control latency. Because latency injection is applied to the data plane, injected delay alters packet transit times without modifying underlying clock alignment. 

_1) Video Send-Time Embedding:_ The server embeds a 64-bit nanosecond timestamp _t_ send<sup>server</sup> into each frame prior to H.264 encoding using an 8 _×_ 8 pixel stamp. The client extracts this value and computes one-way video latency: 


_2) Control Latency:_ Control commands are time-stamped at transmission from the client. The server extracts the value and read one-way control latency computed as: 


## _F. Latency Injection Model (NetEm)_ 

Network delay is injected using Linux Traffic Control (tc) with the NetEm queueing discipline [28]. Delay is applied independently on (i) the server egress interface (video) and (ii) the client egress interface (control), enabling separate manipulation of _τv_ and _τc_ . 

Baseline runs include only inherent transport and codec buffering. Experimental conditions apply additional constant delay (and optional jitter/loss) while measured latencies are verified using the framework in Section III-E. 


Fig. 3. Client-side autonomy module in LAVT. The module receives a compressed video stream and vehicle speed from the server. A deterministic classical vision pipeline estimates lane boundaries in a bird’s-eye-view (BEV) representation, from which a centerline is computed. Lateral control is generated using a speed-adaptive Pure Pursuit controller, and longitudinal motion is regulated by a PI speed controller. Safety mechanisms include frame staleness detection and safe-stop behavior. 

## _G. Client-Side Autonomy Module_ 

Figure 3 illustrates the high-level architecture of the clientside autonomy module. It is a deterministic classical visionbased lane-keeping controller designed to expose latency sensitivity without learning-based compensation. The module operates exclusively on the received compressed image stream and vehicle speed topic, without access to simulator ground-truth. A lightweight image-processing pipeline performs region-of-interest cropping, color/gradient thresholding, and bird’s-eye-view (BEV) transformation. Lane boundaries are estimated via sliding-window initialization followed by polynomial tracking. A lane confidence metric governs speed reduction and safety fallback. Lateral control is implemented using a speed-adaptive Pure Pursuit controller [29] in the BEV domain, while longitudinal motion is regulated by a PI controller targeting constant speed. Safety mechanisms include frame staleness detection and controlled braking under persistent perception failure. 

## IV. EXPERIMENTAL DESIGN 

This section describes the protocol used to quantify latency-induced degradation in closed-loop vision-based lane keeping using LAVT. 

## _A. Simulation Environment_ 

All experiments are conducted in CARLA to ensure safety and repeatability. A single forward-facing RGB camera serves as the sole perception input. No ground-truth pose or simulator state is provided, ensuring that control relies exclusively on delayed visual feedback. 

## _B. Route Design_ 

Experiments are performed in CARLA Town04, which contains straight segments, 90<sup>_◦_</sup> turns, and sustained curvature. Three predefined routes (A, B, and C) are constructed 


Fig. 4. Predefined evaluation routes in CARLA Town04. Route A emphasizes short straight segment followed by 90<sup>_◦_</sup> right turn then a long straight segment. Route B starts with a 90<sup>_◦_</sup> left turn contains followed by a short straight segment and a sustained left-hand curvature. Route C contains short straight _→_ and right-hand curvature. Colored arrows indicate nominal driving direction. Key subsets (black boxes) isolate steeringintensive segments used for focused stability analysis. 

(Fig. 4) to expose distinct lateral-control demands. _Route A:_ short straight _→_ 90<sup>_◦_</sup> right turn _→_ long straight. _Route B:_ 90<sup>_◦_</sup> left turn _→_ short straight _→_ sustained left-hand curvature. _Route C:_ short straight _→_ sustained right-hand curvature. 

For each route, we additionally analyze a corresponding _key_ subset that isolates steering-intensive segments where latency-induced instability first emerges, enabling focused curvature-driven evaluation. 


Fig. 5. Verification of injected one-way latencies across all routes (Town04) for L0–L5. For each condition, colored boxplots show video latency ( _τv_ ) and control-command latency ( _τc_ ) on the same axis. L0–L3 increase video latency only. L4 and L5 reuse the video-delay profiles of L2 and L3, respectively, while injecting additional control-command latency (visible as a distinct _τc_ distribution at L4–L5). 

## completion status. 

Latency measurements incorporate Chrony-based clock alignment (Section III-E). Injected delay is verified by comparing measured one-way latency distributions before and after NetEm configuration. 

## _F. Evaluation Metrics_ 

## _C. Controller Configuration_ 

All experiments use the deterministic client-side controller described in Section III-G. Lane boundaries are estimated from the image stream and converted to a BEV centerline. Lateral control uses speed-adaptive Pure Pursuit, and longitudinal motion is regulated by a PI controller targeting 30 km/h. Controller parameters remain fixed across latency conditions. 

Baseline runs (L0) include only inherent transport and codec latency and establish reference tracking statistics for comparison. 

## _D. Latency Injection Protocol_ 

Latency is injected using tc netem, applied independently to the video (server _→_ client) and control (client _→_ server) channels to manipulate perception delay ( _τv_ ) and actuation delay ( _τc_ ). 

The evaluated conditions are listed in Table I. Jitter and packet loss are excluded to isolate deterministic delay effects. For each condition, 30 runs (6 routes × 5 repetitions) are performed. Across L0–L5, this yields 180 closed-loop runs. 

## _E. Measurement and Logging_ 

Each run records one-way video and control latency ( _τv_ , _τc_ ), lateral and heading errors, steering statistics, and route 

Performance is quantified using mean absolute lateral error (MAE), root-mean-square error (RMS), and 95th-percentile absolute cross-track error. Stability is further assessed via maximum lateral deviation and route completion rate. We additionally report collision rate (Coll.) and lane-invasion events (LaneInv) as discrete safety indicators derived from simulator event flags. 

Results under latency condition _Li_ are compared to baseline _L_ 0 to characterize degradation trends. Environmental conditions remain fixed, and the controller is deterministic to ensure that performance variations arise solely from latency manipulation. 

## V. RESULTS 

This section presents quantitative and qualitative evaluation of closed-loop lane-keeping performance under increasing latency (L0–L5), aggregated over 30 runs per condition. 

## _A. Latency Verification_ 

Before analyzing control performance, we first verify that the measured end-to-end latencies match the intended experimental configurations and that the baseline teleoperation stack operates under low-delay conditions. 


Fig. 6. Trajectory overlays for key route segments (Town04) under latency conditions L0–L5. Top: Route A Key, Middle: Route B Key, Bottom: Route C Key. Thin colored lines show individual runs; the thick black curve denotes the reference trajectory (L0 run05). Red crosses indicate aborted runs due to collision. Increasing perception latency induces growing deviation and phase-lag effects, while additional control-command delay (L4–L5) further amplifies instability and termination frequency, demonstrating nonlinear degradation of closed-loop stability. 

Figure 5 reports the measured one-way latencies for both the video stream ( _τv_ ) and the control-command channel ( _τc_ ) across all routes under conditions L0–L5. 

Under the baseline condition (L0), the LAVT system exhibits low inherent network delay over WiFi 5, with a 

median video latency of approximately 62 ms (p95 _≈_ 86 ms) and a median control-command latency of approximately 8– 10 ms. These values reflect encoding, transport, buffering, and wireless transmission overhead, establishing that the system operates in a stable low-latency regime prior to artificial delay injection. 

Conditions L1–L3 increase video latency only. The measured video medians shift deterministically to approximately 136 ms (L1), 211 ms (L2), and 287 ms (L3), with tight interquartile ranges across all routes. This confirms that NetEm successfully imposed controlled perception delay without introducing significant jitter. 

Conditions L4 and L5 are designed to isolate the effect of _control-command_ delay. In these configurations, the videodelay profiles of L2 and L3 are reused, respectively, while additional latency is injected exclusively in the control channel. The measurements reflect this design: video latency at L4 closely matches L2, and at L5 matches L3, whereas controlcommand latency increases sharply (median _≈_ 83 ms at L4 and _≈_ 108 ms at L5) compared to the _≈_ 8–10 ms observed for L0–L3. 

The narrow distributions and close agreement between configured and measured values confirm deterministic delay injection and accurate clock alignment. 

## _B. Trajectory Behavior Under Increasing Latency_ 

Figure 6 visualizes representative trajectory overlays for key routes under all latency conditions. Each colored trace corresponds to one run, while the black curve denotes the reference trajectory (L0 run05). Red markers indicate termination due to collision events. 

Under L0, trajectories remain tightly clustered around the reference, indicating stable closed-loop behavior. Mild perception delay (L1) introduces small deviations, particularly in curvature transitions. 

At L2 ( _τv ≈_ 211 ms), dispersion increases substantially and multiple runs fail, with instability emerging first in curved segments. At L3, oscillatory steering and overshoot produce frequent lane departures. 

L4 shows slightly improved geometry among surviving runs due to survivorship bias, while L5 exhibits widespread early termination and large-amplitude oscillations consistent with delayed-feedback instability. 

## _C. Quantitative Degradation Trends_ 

Figure 7 summarizes performance degradation as a function of latency using two complementary metrics: (i) the 95th-percentile absolute cross-track error computed over completed runs only, and (ii) the route completion rate computed over all runs. Tracking error is computed exclusively over runs that successfully complete the route without collision, thereby avoiding artificial inflation of error statistics due to premature termination. 

_a) Tracking Performance.:_ Under L0, P95 cross-track error is approximately 2.3 m. Mild delay (L1) produces modest degradation. At L2, error nearly doubles while completion drops to 50%, indicating onset of instability. At L3, 


Fig. 7. Latency-induced degradation in closed-loop lane keeping (Town04; routes A–C and key subsets). Top: Route-balanced mean 95th-percentile absolute cross-track error computed over runs that successfully complete the route without collision; faint markers indicate per-run values. Error bars denote 95% confidence intervals of the mean. Bottom: Route completion rate over all runs; annotations show completed/total runs (out of 30). Tracking degradation emerges at L2 ( _≈_ 211 ms one-way perception delay), while completion exhibits a nonlinear collapse beyond this threshold. L4 isolates additional control-command delay under matched perception latency. 

oscillatory corrections further increase error. The apparent improvement at L4 reflects survivorship bias, as unstable runs terminate early. At L5, P95 exceeds 13 m among surviving runs while completion collapses to approximately 10%. 

_b) Completion Collapse.:_ Completion rate exhibits nonlinear degradation: robust at L0–L1, partial failure at L2, and rapid collapse beyond L3. Instability emerges between 150 ms and 225 ms one-way perception latency, where completion falls below 50%. Notably, completion degradation precedes extreme geometric divergence, indicating loss of closed-loop stability before catastrophic tracking error appears in surviving runs. 

Table II summarizes aggregate driving performance metrics across all routes for each latency condition, including completion rate, collision frequency, lane-invasion events, and 95th-percentile cross-track error. Consistent with Fig. 7, the aggregate statistics confirm nonlinear degradation of 

TABLE II 

DRIVING PERFORMANCE UNDER LATENCY CONDITIONS (TOWN04, ALL 

ROUTES). 

|**Cond.**|**Comp. (%)**|**Coll.**|**LaneInv**|_P_95_x_ **(m)**|
|---|---|---|---|---|
|L0|100|0.20|0.40|2.30|
|L1|93.3|0.23|3.97|2.73|
|L2|50.0|0.67|15.10|3.91|
|L3|36.7|0.83|22.13|9.25|
|L4|30.0|0.77|18.80|4.64|
|L5|10.0|0.97|16.83|13.15|


closed-loop lane keeping as perception latency increases, with a sharp transition between 150 ms and 225 ms one-way delay. The system remains stable at 75 ms, exhibits clear instability by 150 ms, and undergoes widespread collapse by 225 ms. Additional control-command latency further accelerates this collapse. 

## VI. DISCUSSION 

## _A. Delay-Induced Instability Mechanisms_ 

The observed degradation is consistent with classical control theory. Perception delay introduces phase lag, causing corrective steering to act on stale lane geometry. As _τv_ increases, overshoot and counter-corrections produce oscillatory behavior. The sharp transition between L2 and L3 suggests a stability boundary rather than gradual decay. 

The divergence between tracking error and completion rate highlights survivorship bias: unstable runs terminate early, leaving only comparatively stable trajectories in completedrun statistics. Reporting both metrics is therefore essential for accurate stability assessment. 

## _B. Implications for Teleoperation_ 

Perception delay in the 150–300 ms range substantially reduces stability margins in vision-driven teleoperation. As shown in Table II, completion drops from 100% at L0 to 50% at L2 and 10% at L5, while P95 cross-track error increases nearly sixfold between L0 and L5. Network variability may intermittently push systems beyond this boundary unless mitigation mechanisms are applied. 

Although compensation strategies are not evaluated here, the identified stability threshold provides a baseline for assessing predictive perception or latency-compensation methods. 

## VII. CONCLUSION AND FUTURE WORK 

This paper presented a systematic experimental characterization of network-induced latency in vision-based teleoperation. Using controlled delay injection and 180 closed-loop experiments across diverse geometric regimes, we identified an empirical stability transition region between 150 ms and 225 ms one-way perception delay. Below this threshold, lane keeping remains robust; beyond it, completion rate collapses rapidly. Additional control-command delay further accelerates instability even when visual delay is unchanged. 

These findings demonstrate that perception-driven teleoperation exhibits sharp delay-dependent stability limits rather 

than gradual degradation. Quantifying this boundary is essential for safe deployment and for benchmarking latencycompensation strategies. 

_a) Limitations.:_ The study is conducted in simulation under deterministic delay without jitter or packet loss. Dynamic traffic, weather variation, and higher-speed driving conditions are not considered. Furthermore, the study evaluates a deterministic vision-based lane-keeping controller to isolate latency effects; stability boundaries may shift under alternative control architectures. 

_b) Future Work.:_ Future work will extend this characterization to real-vehicle experiments and stochastic network conditions, including jitter and packet loss. Additional controller architectures will be evaluated across several road types in different towns. In addition, predictive perception and latency-compensation techniques will be evaluated against the baseline stability threshold identified in this study. 

## REFERENCES 

- [1] Tobias Kerbl, David Brecht, Nils Gehrke, Nijinshan Karunainayagam, Niklas Krauss, Florian Pfab, Richard Taupitz, Ines Trautmannsheimer, Xiyan Su, Maria-Magdalena Wolf, et al. Tum teleoperation: Open source software for remote driving and assistance of automated vehicles. _arXiv preprint arXiv:2506.13933_ , 2025. 

- [2] Andreas Schimpe, Johannes Feiler, Simon Hoffmann, Domagoj Majstorovi´c, and Frank Diermeyer. Open source software for teleoperated driving. In _2022 International Conference on Connected Vehicle and Expo (ICCVE)_ , pages 1–6. IEEE, 2022. 

- [3] Mustafa Alsolami, Arpan Bhattacharjee, and Weisong Shi. Evaluating the impact of network latency on the teleoperation of autonomous vehicles. In _Proceedings of the Tenth ACM/IEEE Symposium on Edge Computing_ , pages 1–7, 2025. 

- [4] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. CARLA: An open urban driving simulator. In _Proceedings of the 1st Annual Conference on Robot Learning_ , pages 1–16, 2017. 

- [5] Markus Hofbauer, Christopher B Kuhn, Goran Petrovic, and Eckehard Steinbach. Telecarla: An open source extension of the carla simulator for teleoperated driving research using off-the-shelf components. In _2020 IEEE Intelligent Vehicles Symposium (IV)_ , pages 335–340. IEEE, 2020. 

- [6] Martin Gontscharow, Stefan Orf, Albert Schotschneider, Sven Ochs, Marc Ren´e Zofka, and J Marius Z¨ollner. Open-source fleet supervision for real-world multi-vehicle autonomous driving. In _2025 IEEE International Automated Vehicle Validation Conference (IAVVC)_ , pages 1–8. IEEE, 2025. 

- [7] Felix Tener and Joel Lanir. Driving from a distance: challenges and guidelines for autonomous vehicle teleoperation interfaces. In _Proceedings of the 2022 CHI conference on human factors in computing systems_ , pages 1–13, 2022. 

- [8] Felix Tener and Joel Lanir. Design of a high-level guidance user interface for teleoperation of autonomous vehicles. In _Adjunct Proceedings of the 15th International Conference on Automotive User Interfaces and Interactive Vehicular Applications_ , pages 287–290, 2023. 

   - [12] Keonil Kim, Yangho Jeon, Minji Kim, Sangyoung Lee, and SeokCheol Kee. Development of tele-operated driving assistance system for autonomous vehicles with an open-source platform. _International Journal of Automotive Technology_ , pages 1–12, 2025. 

   - [13] Yudai Sato, Shuntaro Kashihara, and Tomohiko Ogishi. Implementation and evaluation of latency visualization method for teleoperated vehicle. In _2021 IEEE Intelligent Vehicles Symposium (IV)_ , pages 1–7. IEEE, 2021. 

   - [14] Rostand AK Fezeu, Jason Carpenter, Rushikesh Zende, Sree Ganesh Lalitaditya Divakarla, Nitin Varyani, Faaiq Bilal, Steven Sleder, Nanditha Naik, Duncan Joly, Eman Ramadan, et al. Teleoperating autonomous vehicles over commercial 5g networks: Are we there yet? _arXiv preprint arXiv:2507.20438_ , 2025. 

   - [15] Nan Tian, Ajay Kummar Tawani, Ken Goldberg, and Somayeh Sojoudi. Motion segmentation and synthesis for latency mitigation in a cloud robotic tele-operation system. In _International Symposium on Robotics Research_ , 2019. 

   - [16] Xiyan Su, Jianning Gao, Mahmoud Ashri, and Frank Diermeyer. Mitigating concept drift in qos prediction for teleoperation of autonomous vehicles using historic data. In _2025 IEEE International Conference on Systems, Man, and Cybernetics (SMC)_ , pages 6654–6658. IEEE, 2025. 

   - [17] Sidharth Bhanu Kamtam, Qian Lu, Faouzi Bouali, Olivier CL Haas, and Stewart Birrell. Network latency in teleoperation of connected and autonomous vehicles: A review of trends, challenges, and mitigation strategies. _Sensors (Basel, Switzerland)_ , 24(12):3957, 2024. 

   - [18] Antonia Stornig, Aymen Fakhreddine, Hermann Hellwagner, Petar Popovski, and Christian Bettstetter. Video quality and latency for uav teleoperation over lte: A study with ns3. In _2021 IEEE 93rd Vehicular Technology Conference (VTC2021-Spring)_ , pages 1–7. IEEE, 2021. 

   - [19] Zexin Deng, Zhenhui Yuan, and Longhao Zou. Telesim: A networkaware testbed and benchmark dataset for telerobotic applications. _arXiv preprint arXiv:2507.04425_ , 2025. 

   - [20] ROS 2 Zenoh Working Group. rmw ~~z~~ enoh: Ros 2 middleware implementation using zenoh. https://github.com/ros2/rmw_ zenoh, 2024. Accessed: 2026-02-28. 

   - [21] Eclipse Zenoh Project. Zenoh: The zero overhead pub/sub/query protocol. https://zenoh.io, 2024. Accessed: 2026-02-28. 

   - [22] GStreamer Project. Gstreamer: Open source multimedia framework. https://gstreamer.freedesktop.org/, 2026. Accessed: 2026-02-16. 

   - [23] GStreamer Project. rtph264pay: Rtp h264 payloader. https: //gstreamer.freedesktop.org/documentation/rtp/ rtph264pay.html, 2026. Accessed: 2026-02-16. 

   - [24] GStreamer Project. rtph264depay: Rtp h264 depayloader. https: //gstreamer.freedesktop.org/documentation/rtp/ rtph264depay.html, 2026. Accessed: 2026-02-16. 

   - [25] GStreamer Project. rtpjitterbuffer. https://gstreamer. freedesktop.org/documentation/rtpmanager/ rtpjitterbuffer.html, 2026. Accessed: 2026-02-16. 

   - [26] The Chrony Project. Chrony – ntp client and server for synchronizing system clocks. https://chrony-project.org/, 2026. Accessed: 2026-02-16. 

   - [27] Red Hat, Inc. Configuring ntp using the chrony suite. https: //docs.redhat.com/en/documentation/red_hat_ enterprise_linux/7/html/system_administrators_ guide/ch-configuring_ntp_using_the_chrony_ suite, 2026. Accessed: 2026-02-16. 

   - [28] Linux Man Pages Project. tc-netem(8) – network emulation. https://man7.org/linux/man-pages/man8/tc-netem. 8.html, 2026. Accessed: 2026-02-16. 

   - [29] R Craig Coulter. Implementation of the pure pursuit path tracking algorithm. Technical report, 1992. 

- [9] Felix Tener and Joel Lanir. Toward the design of a tele-assistance user interface for autonomous vehicles. In _AutomationXP@ CHI_ , 2023. 

- [10] Felix Tener, Andreas Schrank, Philipp Wintersberger, and Shadan Sadeghian. Towards seamless remote interactions: Exploring novel paradigms for teleoperation of autonomous vehicles. In _Adjunct Proceedings of the 16th International Conference on Automotive User Interfaces and Interactive Vehicular Applications_ , pages 256–259, 2024. 

- [11] Keonil Kim and Seok-Cheol Kee. Teleoperated driving with virtual twin technology: A simulator-based approach. _World Electric Vehicle Journal_ , 15(7):311, 2024. 

