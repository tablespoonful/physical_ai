---
title: "Demo: Closed-Loop Sionna-Isaac Sim Co-Simulation Framework for Wireless-Aware Robot Navigation over ROS 2"
date: "2026-10-06"
authors: "Yi Shen Lim; Seungeun Oh; Jihong Park"
url: https://arxiv.org/abs/2610.08618
pdf: https://arxiv.org/pdf/2610.08618
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2610.08618)** / [論文ページ](https://arxiv.org/abs/2610.08618)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Demo: Closed-Loop Sionna–Isaac Sim Co-Simulation Framework for Wireless-Aware Robot Navigation over ROS 2** 

Yi Shen Lim, Seungeun Oh, Jihong Park Singapore University of Technology and Design 

Singapore 

{yishen_lim,seungeun_oh,jihong_park}@sutd.edu.sg 

## **Abstract** 

A robot that offloads its control loop to the network carries the receiver with it, so link quality is decided by where it goes. Simulating this requires both a physics engine and a site-specific propagation model at once; to our knowledge no simulator natively unifies both, with existing couplings of the two limited to offline analyses. We demonstrate a real-time co-simulation framework coupling NVIDIA Isaac Sim and NVIDIA Sionna over ROS 2 that closes the perception–action–communication (PAC) loop between them. Sionna raytraces the base-station-to-robot channel over the exact geometry Isaac Sim simulates on—rather than modeling it stochastically—and feeds channel states back into the control loop in real time. Raytraced on GPU, the coverage map is refreshed in ∼16 ms (∼60 Hz), fast enough for real-time control. To showcase the framework’s utility, we implement a wireless-aware navigation application in an OpenStreetMap(OSM)-derived SUTD campus twin with two Nova Carter robots: the closed-loop planner eliminates communication outage at only +7 _._ 4% traversal time over the shortest-path baseline (which spends 7 _._ 9 s of its 81 _._ 2 s run disconnected). 

## **CCS Concepts** 

• **Networks** → **Network simulations** ; **Cyber-physical networks** ; • **Computer systems organization** → _Robotics_ ; • **Computing methodologies** → _Motion path planning_ . 

## **Keywords** 

Digital twin, ray tracing, closed-loop simulation, co-simulation, wireless-aware motion planning, ROS 2, robotics 

### **ACM Reference Format:** 

Yi Shen Lim, Seungeun Oh, Jihong Park. 2026. Demo: Closed-Loop Sionna– Isaac Sim Co-Simulation Framework for Wireless-Aware Robot Navigation over ROS 2. In _The Twenty-seventh International Symposium on Theory, Algorithmic Foundations, and Protocol Design for Mobile Networks and Mobile Computing (MobiHoc ’26), November 23–26, 2026, Tokyo, Japan._ ACM, New York, NY, USA, 2 pages. https://doi.org/10.1145/3842721.3850090 

## **1 Introduction** 

Cloud robotics, teleoperation, and autonomous logistics offload perception and decision-making to edge servers, so a robot’s control loop depends on a low-latency wireless link. Link quality varies with the robot’s own position, as structures reflect, diffract, and block the signal. Where the robot goes will decide the connectivity 

This work is licensed under a Creative Commons Attribution 4.0 International License. _MobiHoc ’26, Tokyo, Japan_ 

© 2026 Copyright held by the owner/author(s). ACM ISBN 979-8-4007-2975-1/2026/11 

https://doi.org/10.1145/3842721.3850090 


**Figure 1: Co-simulation view: Isaac Sim simulates robots, Sionna ray-traces channels, ROS 2 relays states, RViz2 (ROS 2’s visualization tool) overlays RSS heatmap and planned routes; attendees drive all views live in Scenario 1.** it gets, coupling planning and communication into one PAC loop [3]. Safe deployment requires a platform where motion and site-specific propagation can be studied, before a robot meets a dead zone. 

No single simulator offers this. Robotic simulators lack channel models, and wireless ones (Sionna [4], ns-3) lack physics. Communication-aware planning [5] feeds the planner a statistical channel map; DT-RaDaR [1] ray-traces an OSM/Blender twin with Sionna, as we do, but once and offline, with no physics engine. Robot–network co-simulators [3] close the PAC loop, but over stochastic propagation. Ray-tracing twins such as CAVIAR [2], AODT [6], and SimART [8] are site-specific but close the loop only on communication-side decisions (e.g., beam selection), with mobility given, not planned. None, to our knowledge, combines sitespecific ray tracing, a physics engine, and a channel that reaches the _motion planner_ online, at control-loop rates. 

We demonstrate a framework that does, coupling **NVIDIA Isaac Sim** [7] (a GPU-accelerated robotics simulator for physics and sensors) and **NVIDIA Sionna** [4] (a differentiable wireless ray tracing library) over **ROS 2** (Robot Operating System 2, the standard robotics publish–subscribe middleware), inheriting planning (Nav2, ROS 2’s navigation stack), robot interfacing, and visualization (RViz2) from the ROS 2 ecosystem. Isaac Sim, Sionna, and the planner exchange states over ROS 2 as asynchronous nodes. The ray-traced coverage map is published as a standard costmap layer that any ROS 2 planner can consume, and a campus-scale demo quantifies the resulting connectivity–travel-time trade-off. 

The difficulty is not running the two simulators in parallel but _unifying_ them: both must share one scene geometry—so the raytraced map registers cell-for-cell with the navigation grid and a moved obstacle casts physical and RF shadows simultaneously— while loops at milliseconds (ray tracing), tens of milliseconds (physics), and seconds (planning) must interlock without stalling. 

MobiHoc ’26, November 23–26, 2026, Tokyo, Japan 

Y. S. Lim et al. 

We resolve the first with a single OSM-derived twin. Its Blenderextruded building footprints serve as Isaac Sim’s physics geometry, Sionna’s ray-tracing scene, and the 0 _._ 5 m navigation grid, so raytraced cells register with navigation cells and moved obstacles updates all three at once. We resolve the second in real-time, running asynchronous, message-triggered ROS 2 nodes (Sec. 2). 

## **2 System Architecture** 

**(1) Perception: Scene, Physics & State.** We rebuild the 540×540 m SUTD campus from OSM footprints via Blender, importing it into Isaac Sim [7], simulating two Nova Carter robots at 3 _._ 0 m/s (Fig. 1, left). Poses (physics state) publish over ROS 2 at 60 Hz decoupled from the main loop (Fig. 1, _○_ 1 ). The 0 _._ 5 m navigation grid derives from the same twin; onboard sensing adds runtime obstacles. 

**(2) Communication: Ray Tracing & Coverage.** Control flows over the downlink as planning resides on the network. Two 5G base stations (gNodeBs) act as Txs delivering commands to the robot-mounted Rx, each at 18 dBm EIRP in band n78 (3 _._ 425 GHz, 50 MHz), mirroring our physical private-5G small cell. Both Txs sit 2 _._ 5 m on building facades (marked in Fig. 1); the robot’s vertically polarized dipole Rx (omnidirectional in azimuth) sits at 1 _._ 5 m. Sionna RT 2.0.1’s GPU ray tracer [4] runs over the shared geometry (2 × 10<sup>6</sup> rays, ≤ 5 specular reflections) with ITU-R P.2040 concrete, brick, and metal across 48 building meshes and a ground plane. It computes RSS over a coarser 1 _._ 5 m grid of candidate Rx positions (360×360 cells). The coverage map is sampled at the robot’s live pose for instantaneous RSS; active Tx–Rx paths are rendered in Sionna’s view (Fig. 1, lower left). Recomputing the map, triggered only by Tx motion or geometry changes, takes ∼16 ms (9.5–29.5 ms over 5 runs), i.e., ∼60 Hz (34–105 Hz), and publishes as a ROS 2 OccupancyGrid (Fig. 1, _○_ 2 ). _Scope._ For scenes, channels are deterministic (RSS varies with position and changes only when the map is re-traced), poses are ground truth, channels are reciprocal, sharing one map, and association is best-server without inter-cell interference. 

**(3) Action: Wireless-Aware Motion Planning.** To demonstrate how the framework closes the PAC loop, we instantiate a wirelessaware navigation application on top of its runtime ROS 2 topics. The threshold _RSS_ min=−80 dBm is the lowest power at which our link budget (7 dB noise figure, ≈−90 dBm noise floor) sustains the command stream with margin. Each cell takes a wireless cost _𝐶𝑤_ = min<sup>�</sup> 254 _,_<sup><u>254</u></sup> Δ<sup>max(0</sup><sup>_, RSS_min−</sup><sup>_RSS_)�, withΔ=30 dB spanning</sup> Nav2’s [0 _,_ 254] cost range (free at _RSS_ min, lethal Δ below). As a straightforward example to expose the PAC trade-off, we register this layer alongside physical obstacles _𝐶_ obs (static map, detected obstacles, inflation) to give the combined traversal cost: 

_𝐶_ total ( _𝑥,𝑦_ ) = _𝐶_ obs ( _𝑥,𝑦_ ) + _𝛼_ · _𝐶𝑤_ ( _𝑥,𝑦_ ) _,_ (1) which a custom A* planner searches (accumulating unit step costs per cell), though the framework’s costmap interface can feed arbitrary downstream planners. Here, _𝛼_ =0 recovers shortest-path planning and larger _𝛼_ buys detours around dead zones. A new search is triggered whenever the costmap changes, and the resulting velocity commands return to Isaac Sim over ROS 2 (Fig. 1, _○_ 3 ), closing the loop that drives Scenario 1’s interactive replanning. 

## **3 Demonstration** 

**Scenario 1: Interactive Closed-Loop Operation.** Attendees set waypoints in the operator view (Fig. 1) over the RSS heatmap; 


**Figure 2: Routes (a) and RSS along each traversal (b) for** _𝛼_ =0 **(red),** 10<sup>−2</sup> **(blue),** 10<sup>−1</sup> **(green),** 1 **(black) over the ray-traced coverage map; Tx positions marked, sub-threshold region shaded; outage falls from** 7 _._ 9 **s (red) to** 0 **s (black).** moving or adding gNodeBs and obstacles into the planned path recomputes the map and exposes handover boundaries. Onboard sensing writes it into _𝐶_ obs, the re-traced map casts its RF shadow into _𝐶𝑤_ , and the robot detours around both a few seconds later. 

**Scenario 2: System Performance & Closed-Loop Evaluation.** _System Latency (_ 10 _runs)._ Within the steady-state loop, state ingestion (0 _._ 83 ms), Sionna’s ray-tracing kernel (5 _._ 53±0 _._ 6 ms once warm; 118 ms initial JIT), and costmap fusion (0 _._ 96 ms) deliver updated costmaps in 7 _._ 3 ms; the global A* search dominates, achieving a full loop at 4 _._ 73±0 _._ 10 s. _Closed-Loop Evaluation._ Each robot plans and traverses at 3 m/s in a static scene without halting on link loss, so every _𝛼_ ∈{0 _,_ 10<sup>−2</sup> _,_ 10<sup>−1</sup> _,_ 1} yields a complete, comparable traversal (Fig. 2); _outage_ is time below _RSS_ min. The shortest-path baseline ( _𝛼_ =0) cuts through a building’s RF shadow: 7 _._ 9 s of outage over an 81 _._ 2 s run. _𝛼_ =10<sup>−2</sup> leaves 1 _._ 3 s of outage at +1 _._ 6% traversal time, and by _𝛼_ =10<sup>−1</sup> the route clears the shadow entirely (87 _._ 0 s, +7 _._ 4%, min. RSS −60 _._ 9 dBm); larger _𝛼_ changes little. 

**Logistics.** A single RTX 5090 workstation runs the three views side by side; attendees set goals in the GUI. We bring the workstation and two monitors and need one table (∼1 _._ 5×0 _._ 8 m), three outlets; no network, ∼30 min setup. Video: https://youtu.be/_TE7tGWxK6A. 

## **Acknowledgments** 

This work was supported in part by the NVIDIA Academic Grant Program, in part by A<sup>∗</sup> STAR under its IAF-ICP (H25-MCP3438), in part by SUTD Kickstarter Initiative (SKI 2021 06 08), and in part by the National Research Foundation, Singapore and Infocomm Media Development Authority under its Communications and Connectivity Bridging Funding Initiative. 

## **References** 

- [1] Sunday Amatare et al. 2024. Dt-radar: Digital twin assisted robot navigation using differential ray-tracing. _arXiv preprint arXiv:2411.12284_ (2024). 

- [2] João Borges et al. 2024. CAVIAR: Co-simulation of 6G communications, 3-D scenarios, and AI for digital twins. _IEEE IoTJ_ 11, 19 (2024), 31287–31300. 

- [3] Miguel Calvo-Fullana et al. 2021. Ros-netsim: A framework for the integration of robotic and network simulators. _IEEE RA-L_ 6, 2 (2021), 1120–1127. 

- [4] Jakob Hoydis et al. 2023. Sionna RT: Differentiable ray tracing for radio propagation modeling. In _2023 IEEE Globecom Workshops (GC Wkshps)_ . 317–321. 

- [5] Arjun Muralidharan and Yasamin Mostofi. 2021. Communication-aware robotics: Exploiting motion for communication. _Annual Review of Control, Robotics, and Autonomous Systems_ 4, 1 (2021), 115–139. 

- [6] NVIDIA. 2025. Aerial Omniverse Digital Twin. https://developer.nvidia.com/aerialomniverse-digital-twin. 

- [7] NVIDIA. 2025. Isaac Sim: Robotics Simulation and Synthetic Data Generation. https://developer.nvidia.com/isaac/sim. 

- [8] Kang Yan et al. 2026. SimART: A Unified and Open Real-world Multimodal Simulation Platform for 6G Integrated Sensing and Communication. _arXiv preprint arXiv:2605.13309_ (2026). 

