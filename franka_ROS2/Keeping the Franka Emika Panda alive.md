---
title: "Keeping the Franka Emika Panda alive: a ROS 2 stack with a reliable position interface"
date: "2026-08-20"
authors: "Antonio Langella; Davide Risi; Vincenzo Petrone; Enrico Ferrentino; Pasquale Chiacchio"
url: https://arxiv.org/abs/2608.19740
pdf: https://arxiv.org/pdf/2608.19740
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2608.19740)** / [論文ページ](https://arxiv.org/abs/2608.19740)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Keeping the Franka Emika Panda alive: a ROS 2 stack with a reliable position interface** 

Antonio Langella a, Davide Risi b, Vincenzo Petrone c, Enrico Ferrentino d, and Pasquale Chiacchio e 

_Department of Information Engineering, Electrical Engineering, and Applied Mathematics (DIEM), University of Salerno, 84084 Fisciano, Italy_ 

_{alangella, drisi, vipetrone, eferrentino, pchiacchio}@unisa.it_ 

Keywords: Franka Emika Panda, ROS 2, Robot Operating System, Position Control, Real-Time Robot Control, Reference Generation, Human-Robot Collaboration 

Abstract: This paper presents an open-source software stack that restores ROS 2 support for the Franka Emika Panda robot while resolving the long-standing unreliability of its external position control interface. We first analyze the root causes of unstable position control and show that the observed vibrations and protective stops arise from the timing of the external control loop and sampling jitter, rather than from limitations of the robot itself. Building on this analysis, we introduce an asynchronous hardware interface that decouples real-time communication from the ROS 2 control loop, a rate-matching mechanism for slower command sources, and a position-domain reference generation strategy that produces reliable, smooth position commands. Experimental validation shows that the proposed architecture reliably tracks velocity references by reducing motion artifacts introduced by the official implementation, and the stack is validated across motion planning, compliance control, position-controlled manipulation, and haptic teleoperation on two independent Panda platforms. By restoring a modern, reliable, and open ROS 2 ecosystem for the Panda, this work lowers the barrier to developing safe, responsive, and reproducible human-robot collaboration applications that integrate planning, perception, interaction, and shared autonomy. Code and videos are available on our website at https://sites.google.com/view/fer-ros2/. 

## **1 INTRODUCTION** 

The Franka Emika Robot (FER), widely known in the community as the Franka Emika Panda (Panda, in the following), is one of the most common platforms for manipulation research and collaborative robotics (Haddadin et al., 2022). Its torque-controlled arm, force sensitivity and open control interface made it a de-facto standard in academic laboratories, where a large installed base is still in daily use (Daniel et al., 2024; de Melo et al., 2025; Shahid et al., 2025; Petrone et al., 2026). Vendor software support for the Panda, however, has been discontinued: current releases of franka ~~r~~ os2 and libfranka target the newer Franka Research 3 (FR3) arm and recent ROS 2 distributions (Macenski et al., 2022), but no longer 

> a https://orcid.org/0009-0009-7656-8325 

> b https://orcid.org/0009-0001-3077-5371 

> c https://orcid.org/0000-0003-4777-1761 

> d https://orcid.org/0000-0003-0768-8541 

> e https://orcid.org/0000-0003-3385-8866 

support the Panda (Franka Robotics, 2026). Laboratories that rely on the Panda are therefore left on outdated, unmaintained software, an obstacle which matters most in collaborative applications, where the robot must be integrated with modern planning, perception and interaction tooling. 

A second obstacle concerns position control. On the Panda, commanding joint positions or Cartesian poses through the external control interface is unreliable: the motion is prone to vibrations and to protective stops, to the point that existing frameworks discourage the position interface altogether (Skerlj et al.,<sup>ˇ</sup> 2026b). This is a serious limitation for collaborative use, since position commands are the natural output of, e.g., motion planners or perception-based modules, thus forcing researchers to put additional effort in devising a dedicated control architecture to execute such high-level commands. As we show in this work, the problem is not inherent to the robot, but to the specific implementation of the external control loop, and it can be resolved. 

This work restores support for the Panda on ROS 2 Jazzy, a long-term support distribution, makes its position interface reliable, and releases the code as open source. Our contributions are: 

1. An analysis of why external position control performs poorly on the Panda, tracing it to the timing of the control interface rather than to the robot itself (Sec. 2); 

2. An asynchronous hardware interface that decouples the ros2 ~~c~~ ontrol loop from the robot’s realtime channel, together with a position-domain reference-generation scheme that makes the position interface reliable, and an optional ratematching stage that enables slower command sources (Sec. 3); 

3. The porting of franka ~~r~~ os2 (Franka Robotics, 2025c) to ROS 2 Jazzy for the Panda, built on an extended and packaged libfranka driver which can run on a stock kernel without a real-time patch, both released as citable open-source repositories; 

4. An experimental validation of the proposed reference-generation scheme (Sec. 4) and a demonstration in collaborative application scenarios at two experimental sites (Sec. 5). 

### **1.1 Related Works** 

The reference software for Franka arms is the vendor franka ~~r~~ os2 stack, built on ros2 ~~c~~ ontrol (Chitta et al., 2017); its current releases require a libfranka version that supports only the FR3, leaving the Panda unsupported. The closest work to ours is multipanda ~~r~~ os2 (Skerlj<sup>ˇ</sup> et al., 2026a), a ROS 2 framework for multi-robot control of Franka arms. It targets real-time _torque_ control and multimanual coordination, with a MuJoCo-based simulation (Todorov et al., 2012) for bridging the sim-to-real gap, and it is implemented for the torque control mode only, explicitly leaving other modes as future work. Our goals are complementary: we focus on a current single-arm stack and, specifically, on making the _position_ interface reliable, which multipanda ~~r~~ os2 does not address. 

### **1.2 Paper Structure** 

The remainder of this paper is structured as follows. Sec. 2 analyzes the Franka Control Interface (FCI) and its official ROS 2 implementation, and identifies the two mechanisms that make external position control fail. Sec. 3 presents the proposed architecture, and Sec. 4 validates it against the official one on the 

same robot and trajectory. Sec. 5 then demonstrates the stack on four applications chosen to span key capabilities for human-robot collaboration: planning and executing motions in a shared workspace, regulating the compliance the arm reacts to physical contact with, manipulating objects through position commands, and teleoperating the system through a haptic device. Each exercises a different command interface of the same hardware interface, and the first two are reproduced on two independent Panda instances. Lastly, Sec. 6 concludes the paper. 

## **2 THE FCI AND ITS ROS 2 IMPLEMENTATION** 

### **2.1 FCI Communication Protocol** 

The FCI connects the robot’s onboard controller (INT in the following) to an external workstation (EXT) over UDP (Franka Robotics, 2025a). Every _T_ δ _≡_ 1ms, INT exchanges one packet pair with EXT, sending the current robot state and receiving the next command, and steps its internal controller (Franka Robotics, 2025a). Two properties of this interface, illustrated in Fig. 1, are at the origin of the problem addressed in this work. First, libfranka exposes _blocking_ reads only: the external process waits until a state packet arrives, so the EXT cycle is paced by INT. Second, when operating in external control mode, EXT must supply one reference sample for _every_ INT cycle, since INT performs no onboard interpolation of sparse setpoints, unlike most industrial controllers. For a command to be applied at a given cycle, its round trip must fit within the cycle: the documentation requires the sum of the network round-trip time (RTT), the execution time of the external loop, and the INT’s processing time to stay below _T_ δ, 


and in practice recommends keeping the external-loop contribution below _d_<sup>EXT</sup> _<_ 0 _._ 5ms (Franka Robotics, 2025a). Whenever the budget of (1) is exceeded for a cycle, FCI discards that command; INT then holds the last commanded acceleration constant and keeps running, and only after 20 consecutive discarded commands does it stop the session with a communication error (Franka Robotics, 2025a). This extrapolation lets the actual and commanded references drift apart during loss bursts. 


Figure 1: External control over the FCI (nominal synchronous model). Every _T_ δ, INT measures the state of the robot (R) and applies the command returned by EXT one or more cycles earlier. The vertical arrows represent the periodic exchange of state and commands between INT and R (via an undisclosed interface); the diagonal arrows represent the transmission of states from INT to EXT and the corresponding command from EXT to INT through UDP. A command is applied only if its round trip meets the budget of (1); otherwise it is discarded and INT holds the last commanded acceleration. 

### **2.2 Admissible References** 

Upon receiving a reference, INT reconstructs the kinematic quantities it was not given and verifies them against the robot’s limits. Let ∆ denote the backward finite-difference operator, 


with higher-order differences defined recursively as ∆<sup>_m_</sup> **x** ( _k_ ) = ∆�∆<sup>_m−_1</sup> **x** ( _k_ )�. For a joint position reference **q** _s_ ( _k_ ), the case analyzed in this work, the reconstruction reduces to 


from which the required actuation torques follow through the rigid-body dynamics (Featherstone and Orin, 2008) 


where **B** _∈_ R<sup>_n×n_</sup> is the inertia matrix, **C** _∈_ R<sup>_n×n_</sup> accounts for the centrifugal and Coriolis effects, **f** _∈_ R<sup>_n_</sup> contains joint friction, **g** _∈_ R<sup>_n_</sup> collects the gravitational torques, and **q** _,_ ˙ **q** _,_ ¨ **q** _∈_ R<sup>_n_</sup> respectively represent actual joint positions, velocities, and accelerations, with _n ∈_ N being the number of degrees of freedom<sup>1</sup> . 

Table 1: Loop timings over the benchmark runs. LF: bare libfranka motion-generation example; RS: official synchronous ROS 2 implementation executing a joint trajectory; RA: our asynchronous ROS 2 implementation executing the same joint trajectory as RS. Measurements are obtained with the LTTng tracer. 

||**LF**|**RS**|**RA**|
|---|---|---|---|
|_d_<sup>EXT</sup> median [ms]|0.012|0.065|0.013|
|_d_<sup>EXT </sup>p99 [ms]|0.040|0.137|0.048|
|_d_<sup>EXT </sup>max [ms]|0.087|2.174|0.141|
|unserved cycles [%]|0.18|5.91|0.41|


INT verifies that positions, velocities, accelerations and jerks, as well as the torques in (3) and their rates, lie within their admissible ranges (Franka Robotics, 2025b); a violation aborts the motion with a discontinuity or limit error. The admissible set of references is narrow. Since (2) divides successive differences by powers of _T_ δ, a deviation ε of **q** _s_ ( _k_ ) from the value that would preserve the previously established acceleration produces an additional jerk term of ε _/T_ δ<sup>3.At</sup> _T_ δ = 1ms, a deviation of a few microradians is enough to reach the jerk limit of the Panda (Franka Robotics, 2025b), and the other limits act analogously. Informally, we experimentally confirmed this microradianscale tolerance: perturbing an otherwise feasible trajectory with uniform noise on the order of 10<sup>_−_6</sup> rad was sufficient to trigger violations. 

### **2.3 The Synchronous ROS 2 Implementation** 

The official franka ~~r~~ os2 hardware interface performs the blocking FCI state read inside the read phase of the ros2 ~~c~~ ontrol main loop (Chitta et al., 

> 1 _n_ = 7 for the Panda robot. 


Figure 2: Distribution of the read-to-read interval, normalized by the number of measurements of each capture. For the synchronous implementation, the distribution peaks at multiples of _T_ δ (labeled as A, B and C). Measurements are obtained with the LTTng tracer. 

2017). The latter is driven by its own periodic thread: at every cycle, it wakes on a workstation timer, performs the read phase, the controllers’ updates and the write phase, then it sleeps until the next cycle boundary. Because the FCI read is blocking, the read phase itself does not complete until a new state packet arrives from INT. As a result, each iteration of the loop is paced by two different clocks: the beginning of the read phase is determined by the workstation timer (EXT), while its completion is determined by the arrival of the state packet generated by the robot controller (INT). Since INT and EXT’s clocks are independent, the relative phase between the two drifts slowly and leads to periodic unserved cycles. 

Because the controllers execute between the read and the write, their computation lies on the critical path that (1) constrains. The immediate cost of this arrangement is visible in Table 1: the external ROS 2 control loop (RS) takes a median of 0 _._ 065 ms, against 0 _._ 012 ms for a bare libfranka program (LF) driving the same robot, and reaches 2 _._ 174 ms in the worst cycle, exceeding _T_ δ and leading to the discard of the command of that cycle. It is worth highlighting that the controllers exercised for these measurements only forward joint position commands; critically, the margin is expected to shrink as the application becomes more demanding. 

A more damaging consequence is produced by the drifting phase between the two clocks. When the EXT timer wakes shortly before receiving the next state packet from INT, the blocking read returns after a short wait and the cycle completes comfortably, producing a read-to-read interval close to _T_ δ (Fig. 2, peak A). Conversely, when the EXT timer wakes immediately after a state packet has already been sent by 


Figure 3: Reference distortion under sampling jitter. EXT samples the trajectory after each INT tick, at instants whose jitter displaces the samples (dotted lines); INT files them on its uniform grid and differences them, so the reconstructed reference (red) departs from the desired one (dashed). On a steep segment (inset) the resulting increment leaves the admissible cone and aborts the motion. Jitter amplitude exaggerated for legibility. 

INT, the read must wait almost a full period _T_ δ for the following packet, since it returns only on a fresh state. This causes the ROS 2 cycle to overrun, and the next completed read will happen on a future wake of the EXT timer (as in Fig. 2, peaks B and C). When the EXT cycle overruns, one or more INT cycles remain unserved. During those cycles, INT holds the last commanded acceleration, as described in Sec. 2.1, thus distorting the intended reference. In our benchmarks (Table 1), RS results in 5 _._ 91 % unserved cycles, against 0 _._ 18 % for LF. 

### **2.4 Reference Distortion under Sampling Jitter** 

Careful real-time configuration can reduce the number of unserved cycles, but a second effect survives it: on the cycles that are served, the reference itself is distorted by _sampling jitter_ . In a typical ROS 2 deployment, a planned trajectory is sampled using the EXT workstation clock, which is typically a soft realtime machine communicating with INT through standard TCP/IP protocols. Network round trip, the nondeterministic latency of the operating-system network stack and scheduler on EXT, and the processing time of INT are all irreducible causes of sampling jitter (Reghenzani et al., 2019; Casini et al., 2019). 

More formally, let **q**<sup>_∗_</sup> ( _t_ ) be the planned trajectory, intended as a continuous function; the refer- 

ence applied by INT at cycle _k_ is the trajectory evaluated by EXT at some instant _ts_ ( _k_ ), i.e., **q**<sup>_∗_�</sup> _ts_ ( _k_ )�, but (2) treats it as the uniform sample taken at _kT_ δ. Even if the two clocks were perfectly aligned and INT were perfectly real-time, the jitter sources listed above would induce a time-domain sampling error of δ _t_ ( _k_ ) = _ts_ ( _k_ ) _− kT_ δ. By first order Taylor expansion **q** _s_ ( _k_ ) _≈_ **q**<sup>_∗_</sup> ( _kT_ δ) + **q** ˙<sup>_∗_</sup> ( _kT_ δ)δ _t_ ( _k_ ), therefore the sampling jitter induces an error in the finite differences calculated by INT. For the velocity, 


By chaining the finite differences of (2), the error induced by sampling jitter on the calculated jerk is **q** ˙<sup>_∗_</sup> ∆<sup>3</sup> δ _t/T_ δ<sup>3.</sup> At _q_ ˙ = 1rad _/_ s, a single sample displaced by 4 µs displaces the commanded position by 4 µrad and produces a jerk error of 1 _._ 2 _×_ 10<sup>4</sup> rad _/_ s<sup>3</sup> , above the jerk limit of every joint of the robot (Franka Robotics, 2025b). In the synchronous implementation, where the sample is taken as soon as the packet arrives, the problem is amplified as _ts_ ( _k_ ) inherits the arrival jitter directly. This is shown in Fig. 3 and it explains why, in our tests, discontinuity aborts coincided with the cycles carrying the longest inter-arrival gaps. 

Sampling the trajectory with INT’s own timestamps, i.e., the robot time carried by each state packet, removes this effect, and in our tests eliminated all violations; it requires, however, the trajectory in closed form and an external loop running exactly at INT’s rate, neither of which a controller-agnostic ROS 2 stack running on a general-purpose OS can assume. 

To work around the problem, libfranka offers a rate limiter and a low-pass filter, but neither addresses its cause: the rate limiter only saturates the command derivatives to the admissible ranges, trading the discontinuity aborts for sustained link oscillations, while the low-pass filter attenuates the distortion without removing it, leaving audible motor noise and sporadic aborts. 

### **2.5 Robustness of the Velocity and Torque Interfaces** 

The same jitter affects velocity and torque commands, yet these interfaces appear to work reliably, which explains why the problem has drawn little attention and why existing frameworks simply advise against the position interface (Skerlj<sup>ˇ</sup> et al., 2026a). The reason follows from (2). Repeating the calculation of Sec. 2.4 for the velocity command interface, one ob- 

tains that the error induced on the calculated jerk is **q** ¨<sup>_∗_</sup> ∆<sup>2</sup> δ _t/T_ δ<sup>2:thesensitivitytothesametimingerror</sup> is reduced, making the position interface the most sensitive one. Another reason this problem is often unnoticed is that, when using the velocity or torque commands to control position, the loop closure itself absorbs the residual distortion as a disturbance. The scheme of Sec. 3.3 recovers both mechanisms within the position interface: the motion is driven by the commanded velocity, so that the increment reaching INT is not the difference of two displaced position samples, and the position command acts only through a loop closed on the robot’s own commanded state. 

## **3 PROPOSED ARCHITECTURE** 

The proposed stack, summarized in Fig. 4, rests on two open-source components: a communitymaintained libfranka repository (Tingelstad, 2024) that brings the modern control API to the Panda, extended with the Panda kinematic limits (Franka Robotics, 2025b), and a ROS 2 Jazzy package built on top of it providing a hardware interface for the robot (Franka Robotics, 2025c). On this basis, Sec. 3.1 introduces the asynchronous communication thread that decouples the ros2 ~~c~~ ontrol loop from the FCI channel; Sec. 3.2 exploits this decoupling to run the ros2 ~~c~~ ontrol loop at a lower rate, matched to the robot loop by a rate matching stage applicable to any command interface; and Sec. 3.3 presents the position-domain reference generation that makes the position interface reliable. 

### **3.1 Asynchronous Communication Thread** 

The asynchronous interface addresses the problem of Sec. 2.3 by confining FCI communication to a dedicated real-time thread, scheduled under SCHED ~~F~~ IFO at the highest priority (99) and only containing the communication pipeline. The thread runs its own loop paced by the robot: each iteration blocks on the state read, publishes the received state into a mutexprotected buffer, fetches the next command from a second mutex-protected buffer, and transmits it within the budget of (1). On the ros2 ~~c~~ ontrol side, the logic reduces to buffer exchanges: the read phase copies the latest state and the write phase deposits the latest command. ROS-side jitter — being due to scheduling, DDS activity or controller cost — therefore terminates at the buffers and never reaches the FCI channel; conversely, a late ROS cycle no longer implies a missed robot cycle, since the thread keeps 


Figure 4: Proposed architecture. The ros2 ~~c~~ ontrol thread and the real-time thread run on the workstation (EXT); they exchange state and command through mutex-protected buffers, so ROS-side jitter never reaches the robot. The real-time thread talks to the onboard controller (INT) over the UDP link, and matches a slower command stream to 1 kHz through the rate-matching stage on the write path. 

serving INT with a consistent command. The measurements of Table 1 quantify both effects: thanks to the dedicated thread, _d_<sup>EXT</sup> has a median of 0 _._ 013 ms, comparable to the 0 _._ 012 ms of a bare libfranka program; the synchronous interface produces 5 _._ 91 % unserved cycles while our asynchronous implementation only produces 0 _._ 41 %. Furthermore, with the controllers moved off the real-time path, the delay added to the FCI exchange does not scale with the complexity of the application. In Fig. 2 the quantization of the synchronous interface gives way to the broad, continuous distribution of the bare libfranka loop: the thread is paced by the arrival of the packets rather than by a workstation timer, and the phase competition of Sec. 2.3 does not arise. 

Robustness to packet loss is handled at the same level. The thread timestamps every state read and compares the measured inter-arrival period _T_ ˆ ( _k_ ) against _T_ δ; whenever _|T_<sup>ˆ</sup> ( _k_ ) _− T_ δ _| >_ 0 _._ 25ms, the cycle is flagged as anomalous, the write is skipped, and the last consistent command is held, preventing a command computed against a stale or duplicated state from being differentiated by (2). Position-type modes are additionally gated at activation: no command is transmitted until both the thread and the ROS-side loop have consumed a fresh state, avoiding first-cycle steps at controller switches. 

Because the timing requirement is confined to the communication thread, and the processing in the latter is reduced to a bare minimum, the stack does not enforce the use of a real-time kernel patch: the experiments of Sec. 4 were obtained on a stock kernel with 

SCHED ~~F~~ IFO scheduling alone. 

### **3.2 Rate Matching for Slower Control Loops** 

The proposed architecture admits control loops slower than what FCI prescribes: the ros2 ~~c~~ ontrol loop may run at any rate _f_ EXT _≤ f_ INT, which relaxes its real-time requirements and matches the native rate of most command sources, from motion planners to teleoperation devices. The rate-matching stage described here is what makes this possible. 

A source running at _f_ EXT delivers one update every _N_ = _⌈ f_ INT _/ f_ EXT _⌉_ robot cycles. Passing those command updates on as they arrive would hold each value for _N −_ 1 cycles and step on the _N_ -th, and (2) would turn that staircase into impulsive motor actions. To prevent this, a rate-matching moving-average filter is run on the communication thread to smooth the reference without distorting it. By choosing the window of the filter as _N_ = _⌈ f_ INT _/ f_ EXT _⌉_ , each command update is distributed across the _N_ cycles separating it from the next, and the staircase becomes a piecewiselinear ramp. The filter introduces a group delay of _<u>N−</u>_ 2 <u>1</u><sup>_T_δ=(</sup><sup>_N −_1)</sup><sup>_×_0</sup><sup>_._5 ms.</sup> The delay is limited to a few milliseconds assuming a reasonable value of _f_ EXT _≥_ 100Hz. Because it acts on the command samples irrespective of their meaning, the filter applies to any command interface. 

### **3.3 Position-Domain Reference Generation** 

The analysis of Sec. 2.4 indicates that any scheme sampling the trajectory with the workstation clock inherits sampling jitter and, over time, clock drift. As a consequence, the proposed control scheme abandons external time references and recovers the two mechanisms that make the velocity and torque interfaces robust (Sec. 2.5). 

Let **q** _d_ ( _k_ ) be the last commanded position reported by INT in the state packet; **q** ext( _k_ ) be the position command (raw or filtered) most recently deposited by the ROS side and **q** ˙ ext( _k_ ) be its feed-forward velocity obtained by finite-differencing successive position commands. The proposed method generates the reference in the _position domain_ from the latest available position command 


where λ is a tunable parameter. 

Equation (5) has three properties that address the failure modes of Sec. 2: (i) the motion is driven by the feed-forward term _T_ δ ˙ **q** ext( _k_ ) while the position enters only through a proportional term closing the loop on **q** _d_ ( _k_ ), so the position inherits the sensitivity of the velocity interface; (ii) if the external stream stalls, the reference degrades gracefully toward the last target instead of stepping; (iii) no timestamp of either machine appears in it, making it immune to clock drift. 

An analogous scheme covers the Cartesian pose interface: the commanded pose is propagated by the externally commanded twist over one period, and a proportional twist correction toward the externally commanded pose is applied incrementally. 

Since the scheme already delivers a continuous command stream, the command low-pass filter offered by libfranka is redundant, and it must in fact be disabled: applied to an incremental command it scales the increment itself, and with it both the feedforward term and the correction gain, so that the robot follows a fraction of the commanded motion (Sec. 4). 

We do not claim formal guarantees for the proposed scheme; its behavior is assessed empirically in our experiments. 

Jazzy, connected to the robot by a dedicated Ethernet link. We compare the official (synchronous) franka ~~r~~ os2 hardware interface ported to ROS 2 Jazzy with our asynchronous interface. Joint trajectories are produced by a robot-agnostic reference generator (Risi et al., 2026), which validates and interpolates the waypoints and publishes the resulting command stream to the controller under test. The same _∼_ 18 _._ 32s multi-joint trajectory is replayed in every run. 

Loop timings are collected with LTTng user-space tracepoints placed around the state read and the command write, as reported in Sec. 2.3 and Sec. 3.1; robot states and the trajectory results of each run are recorded from the ROS 2 graph. 

### **4.2 Position Control** 

We evaluate the performance of the proposed position reference generation scheme in (5) by comparing executions of the same trajectory with both the synchronous and asynchronous interfaces. For the synchronous interface, the low-pass filter is active as it is required to safely control the arm via position commands. For the asynchronous interface, we compare the behavior with and without the low-pass filter and set the control frequency to _f_ EXT = _f_ INT = 1kHz. All three configurations have the rate limiter enabled to prevent communication errors. For the experiments we set λ = 1 _×_ 10<sup>_−_3</sup> . 

Fig. 5 compares the measured joint velocity and its spectrum for three configurations: synchronous, the proposed asynchronous configuration, and the proposed one with the addition of the low-pass filter. The synchronous interface follows the reference but carries an order of magnitude more spectral power than the other two configurations in the 20 _−_ 150 Hz band: this is the roughness the rate limiter leaves behind once it has removed the invalid commands, and it manifests as motor noise during the execution of the trajectory. The low-pass filter suppresses that excess but, as discussed in Sec. 3.3, it hinders the tracking by scaling the incremental command (visible as the shrunken joint velocity curve in Fig. 5). The proposed configuration attains faithful tracking while keeping the low band power of the filtered case. The remaining joints behave consistently<sup>2</sup> . 

## **4 EXPERIMENTAL VALIDATION** 

### **4.3 Rate Matching** 

### **4.1 Setup** 

All experiments run on a Panda controlled from a workstation running Ubuntu 24.04 (patched with PREEMPT ~~R~~ T (Reghenzani et al., 2019)) and ROS 2 

To validate the rate matching mechanism described in Sec. 3.2, the robot is driven from a velocity com- 

2Results for all joints are available at https://sites.goog le.com/view/fer-ros2/results 


Figure 5: Measured joint velocity (top) and its power spectral density (bottom) on joint 1, for the synchronous configuration, the proposed asynchronous one, and the proposed one with the low-pass filter enabled. The synchronous velocity tracks the reference, but is visibly rough; the filtered one is smooth, but follows a fraction of the commanded motion; the proposed one tracks and stays smooth. 

mand source running at _f_ EXT = 125Hz (hence _N_ = 8) and we measure what reaches the robot with the ratematching stage enabled and disabled. 

Results are shown in Fig. 6: with the stage disabled, the command is the zero-order hold of the source, constant for _N −_ 1 cycles and stepping on the _N_ -th; the single step carries the whole update, so the per-cycle increment presented to INT is _N_ times the intended one. With the stage enabled, the same update is spread across the _N_ cycles it spans and the command becomes a ramp whose per-cycle increment is the intended one, at the analytical cost of a group delay of<sup>_<u>N−</u>_</sup> 2<sup><u>1</u></sup><sup>_T_δ = 3</sup><sup>_._5ms.</sup> 


Figure 6: Commanded joint velocity reaching the robot from a 125 Hz source, with rate matching disabled and enabled. The two commands, from separate runs, are aligned to the reference. The envelopes coincide over the trajectory (main), while the detail shows the zero-order-held staircase, whose single riser spans the _N_ = 8 cycles that the ratematched command crosses as a ramp. 

3. an end-to-end, _position_ -controlled pick-and-place (Sec. 5.3); 

4. haptic teleoperation of a mobile manipulator (Sec. 5.4). 

Together they exercise the position, velocity and torque command interfaces of our hardware interface. The MoveIt! planning and compliance control applications were run on two different Panda setups, hosted in two different institutions, hereinafter referred to as Lab A and Lab B<sup>3</sup> , while pick-and-place and teleoperation were run in Lab A only, showing that the same software runs unchanged across different setups and machines. Moreover, to ease the shake-out of the system for new users, we have restored all the basic libfranka examples<sup>4</sup> which, for the sake of brevity, are shown on our website<sup>5</sup> . It is worth highlighting that, in Lab A, the applications are run with a nonrealtime kernel, to demonstrate that, as mentioned in Sec. 3.1, patching the system with PREEMPT ~~R~~ T is not a strict requirement as it was for the official release of libfranka. 

## **5 APPLICATIONS** 

### **5.1 MoveIt! planning and execution** 

We demonstrate the proposed stack on four applications, each exercising a capability that collaborative robotics commonly relies on: 

1. collision-aware motion planning and execution via MoveIt! and ROS2-native controllers (Sec. 5.1); 

2. compliance control for physical human-robot interaction, at standstill and along trajectories, with and without human perturbation (Sec. 5.2); 

This application exercises the MoveIt! planning and execution pipeline (Fig. 7). Starting from the initial configuration (Fig. 7a), the robot plans a motion to a randomly sampled goal pose (Fig. 7b) 

- 3The labs’ names will be disclosed together with the 

- authors’ names in case of acceptance. 

> 4https://anonymous.4open.science/r/libfranka-636F 

> 5https://sites.google.com/view/fer-ros2/libfranka 


(a) Initial pose (b) MoveIt! plan (c) Final pose Figure 7: MoveIt! planning and execution, reproduced on both Panda setups: (top) Lab A; (bottom) Lab B. Full videos at https://sites.google.com/view/fer-ros2/applications/mov eit 

Table 2: Control parameters: the **Sec.** column points to the subsection presenting the application; in the **Axis** column, numbers indicate joints, while _{x, y, z}_ and _{R, P,Y }_ represent Cartesian-space linear and angular components respectively. 

|**Sec.**|**Axis**|**K**_P_|**K**_I_|**K**_D_|
|---|---|---|---|---|
||1,2,3,4|600|0|30|
|51|5|250|0|10|
|.|6<br>7|150<br>50|0<br>0|10<br>5|
|5.2 A,C|_x,y,z_<br>_R,P,Y_|1000<br>100|–<br>–|100<br>10|
|5.2 B,D|_x,y,z_<br>_R,P,Y_|100<br>10|–<br>–|10<br>5|
|5.3|_x,y,z_<br>_R,P,Y_|10<br>10|–<br>–|–<br>–|
||_x,y,z_|900|–|100|
|5.4|_R_|90|–|10|
||_P,Y_|90|–|1|


and executes it (Fig. 7c) through an effort-based joint ~~t~~ rajectory ~~c~~ ontroller tuned with the PID gains of Table 2. This confirms that the stack effortlessly integrates with the standard ROS 2 planning tools, letting users move the robot to any feasible desired pose defined by the target application. 

### **5.2 Compliance control** 

This application deploys a custom torque controller, named the _compliance controller_ , which applies a Cartesian-space PD control law at the end-effector, whose gains set how compliant the arm is to human interaction: 


where **x** and **x** ˙ are the end-effector pose and twist, _•_ ˜ ≜ _•d −•_ indicates the error, and _•d_ represents 

the desired quantity. **I** _n_ is the _n × n_ identity matrix, and **J** ( **q** ) _∈_ R<sup>6</sup><sup>_×n_</sup> is the configuration-dependent Jacobian matrix, with † indicating the pseudoinverse of its transpose, while _k_ 0 := 1 _._ 0 and **q** 0 := [0 _,_ 0 _,_ 0 _, −_ 90<sup>_◦_</sup> _,_ 0 _,_ 107<sup>_◦_</sup> _,_ 0]<sup>_⊤_</sup> are the nullspace stiffness and setpoint, respectively. 

We exercise this controller in four different setups, with control gains **K** _P_ and **K** _D_ set according to Table 2: 

- A) standstill human perturbation with stiff behavior; 

- B) standstill human perturbation with compliant behavior; 

- C) trajectory tracking with stiff behavior; 

- D) trajectory tracking with compliant behavior and human perturbation. 

By retuning the Cartesian gains **K** _P_ and **K** _D_ as in Table 2, the controller ranges from stiff to compliant behavior. With stiff gains, the arm holds its pose or tracks its trajectory tightly and resists contact; with compliant gains, it yields to external forces. Fig. 8 shows both regimes: at standstill (top), the robot reacts softly to a human push under compliant gains while staying firm under stiff ones; along a trajectory (bottom), the human can deflect the compliant robot, whereas the stiff run is executed without human contact for safety (2C) and tracks unperturbed. Readers are invited to see the full videos for a better visualization of these behaviors<sup>6</sup> . 

### **5.3 Pick-and-place** 

This application runs a complete pick-and-place task through the _position_ command interface, the interface discouraged on the Panda by (Skerlj et al., 2026a) and<sup>ˇ</sup> made reliable by this work. We adopt a second custom controller, the _Cartesian pose controller_ , defined by: 


with **K** _P_ set as in Table 2 and α := 1 _×_ 10<sup>_−_6</sup> . Notably, this controller claims the _position_ command interfaces directly by commanding **q** _c_ , thus exercising the interface this work makes reliable. 

The robot grasps an object from one surface and places it, re-oriented, on another at a different height. Fig. 9 illustrates the procedure, pairing snapshots of the real execution (top) with the MoveIt! planning requests computed through its C++ API and previewed to the user in RViz (bottom). 

6https://sites.google.com/view/fer-ros2/applications/c ompliance-control 


(a) Lab A 


(b) Lab B 

Figure 8: Compliance control, reproduced on both Panda setups. Within each block: (top) standstill, (bottom) trajectory tracking, (left) stiff, (right) compliant. Full videos at https://sites.google.com/view/fer-ros2/applications/compliance-control. 


Figure 9: Pick and place application on the Panda of Lab A; (top) execution, (bottom) planning with MoveIt!: current robot state and planned goal are shown solid and shaded, respectively. Arrows indicate the temporal sequence of operations. Full video at https://sites.google.com/view/fer-ros2/applications#h.q9xn7np3mlnj. 

### **5.4 Teleoperation** 

A human operator teleoperates the system through a _haptic device_ , whose motion is mapped either to Cartesian-space references ( **x** _d_ in (6)) for the arm or to twist commands for a Husky A200 mobile base, alternating between the two. The arm tracks these references with the _compliance controller_ (6), using the gains of Table 2 and _k_ 0 := 0 _._ 3. The task is similar to the pick-and-place of Sec. 5.3, but the mobile base extends the arm’s workspace: as Fig. 10 shows, it carries the manipulator to objects beyond its fixed reach, which it then grasps and releases at new locations. 


Figure 10: Teleoperation application in Lab A. Full video at https://sites.google.com/view/fer-ros2/applications#h.i 21u2awf44m2. 

## **6 CONCLUSIONS** 

This work brings the Franka Emika Panda back onto a current ROS 2 stack and makes its position command interface usable. As a preliminary analysis, we traced the failure of external position control to the timing of the control loop rather than to the robot. In the official implementation, the external workstation timer triggers the blocking FCI read, but the robot’s controller dictates when new data arrives. We concluded that, as these two clocks are independent, their relative phase drifts, causing periodic delays that leave robot cycles unserved and make the external computer distort the command stream by sampling the trajectory at instants whose jitter the onboard motion generator reads as spurious velocity and jerk. 

To address this issue, the proposed architecture separates the two concerns. A real-time thread owns the communication with the robot and keeps the external loop within the interface budget, at a cost indistinguishable from a bare libfranka program, while the ros2 ~~c~~ ontrol loop is free to run at its own rate, matched to the robot’s by a filtering stage. References are generated in the position domain, anchored to the robot’s own commanded state, so no clock of the workstation enters the command. The position interface then tracks as accurately as the synchronous one while reducing the spectral content that the rate limiter leaves behind, and the four applications of Sec. 5 exercise the position, velocity and torque interfaces on two independent setups. Both repositories are released as open source. 

The approach has limits that are worth stating. The reference generation is assessed empirically: we make no formal claim on the smoothness or the stability of the resulting command stream, and the gain λ trades the speed at which the robot’s state rejoins the external reference against the size of the percycle correction. The rate-matching stage costs a group delay that grows with the ratio of the two rates, which bounds how slowly the ROS side can usefully run. Unserved cycles are reduced but not removed, since a general-purpose workstation retains a residual scheduling latency of its own. 

Future work follows these limits. A correction saturated at the admissible per-cycle increment would replace the fixed gain and reconcile the two states at the fastest feasible rate, which also opens the way to the constraint-aware reference generation needed under sustained packet loss. The stack will be ported to the next ROS 2 distribution, and the position-domain scheme, which assumes nothing specific to this robot beyond the structure of its command interface, is a candidate for other manipulators whose controllers 

expose a commanded state. 

## **ACKNOWLEDGEMENTS** 

The authors would like to thank A.Z., A.R., and F.S. for their contribution in developing the software that made this work possible. The authors warmly thank _Lab B_ for hosting the executions of part of the experiments conducted in this work. 

## **REFERENCES** 

- Casini, D., Blaß, T., L¨utkebohle, I., and Brandenburg, B. B. (2019). Response-time analysis of ROS 2 processing chains under reservation-based scheduling. In _31st Euromicro Conference on Real-Time Systems (ECRTS)_ , volume 133 of _LIPIcs_ , pages 6:1–6:23. Schloss Dagstuhl – Leibniz-Zentrum f¨ur Informatik. 

- Chitta, S., Marder-Eppstein, E., Meeussen, W., Pradeep, V., Tsouroukdissian, A. R., Bohren, J., Coleman, D., Magyar, B., Raiola, G., L¨udtke, M., and Perdomo, E. F. (2017). ros ~~c~~ ontrol: A generic and simple control framework for ROS. _The Journal of Open Source Software_ , 2(20):456. 

- Daniel, M., Magassouba, A., Aranda, M., Lequi`evre, L., Corrales Ram´on, J. A., Iglesias Rodriguez, R., and Mezouar, Y. (2024). Multi actor-critic ddpg for robot action space decomposition: A framework to control large 3d deformation of soft linear objects. _IEEE Robotics and Automation Letters_ , 9(2):1318–1325. 

- de Melo, V. R., Jetti, G., Braghin, F., and Roveda, L. (2025). Unified safety-aware physical human-robot collaborative controller with online continuous learning and personalized tuning. In _2025 IEEE International Conference on Advanced Robotics (ICAR)_ , page 818–825. IEEE. 

- Featherstone, R. and Orin, D. E. (2008). _Dynamics_ , page 35–65. Springer Berlin Heidelberg. 

- Franka Robotics (2025a). Franka control interface documentation. https://frankarobotics.github.io/docs/. Accessed: 2026-07-24. 

- Franka Robotics (2025b). Franka Emika Panda: Robot and interface specifications. https://frankarobotics.github. io/docs/control ~~p~~ arameters.html. Accessed: 2026-0724. 

- Franka Robotics (2025c). franka ~~r~~ os2: ROS 2 integration for Franka research robots. https://github.com/frank arobotics/franka ~~r~~ os2. Accessed: 2026-07-24. 

- Franka Robotics (2026). franka ~~r~~ os2 releases. https://gith ub.com/frankarobotics/franka ~~r~~ os2/releases. v3.4.1 requires libfranka _≥_ 0.20.4; accessed 2026-07-24. 

- Haddadin, S., Parusel, S., Johannsmeier, L., Golz, S., Gabl, S., Walch, F., Sabaghian, M., J¨ahne, C., Hausperger, L., and Haddadin, S. (2022). The Franka Emika robot: A reference platform for robotics research and 

education. _IEEE Robotics & Automation Magazine_ , 29(2):46–64. 

- Macenski, S., Foote, T., Gerkey, B., Lalancette, C., and Woodall, W. (2022). Robot operating system 2: Design, architecture, and uses in the wild. _Science Robotics_ , 7(66). 

- Petrone, V., Puricelli, L., Pozzi, A., Ferrentino, E., Chiacchio, P., Braghin, F., and Roveda, L. (2026). Optimized residual action for interaction control with learned environments. _IEEE Transactions on Control Systems Technology_ , 34(2):1044–1050. 

- Reghenzani, F., Massari, G., and Fornaciari, W. (2019). The real-time Linux kernel: A survey on PREEMPT ~~R~~ T. _ACM Computing Surveys_ , 52(1):18. 

- Risi, D., Petrone, V., Langella, A., Pagliara, G., Ferrentino, E., and Chiacchio, P. (2026). Simplifying ROS2 controllers with a modular architecture for robot-agnostic reference generation. _arXiv preprint arXiv:2601.08514_ . 

- Shahid, A. A., Moroncelli, A., Brscic, D., Kanda, T., and Roveda, L. (2025). Gear: Gaze-enabled human-robot collaborative assembly. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , page 4457–4464. IEEE. 

- ˇSkerlj, J., Bien, S., Naceri, A., and Haddadin, S. (2026a). Bridging the sim-to-real gap with multipanda ~~r~~ os2: A real-time ROS2 framework for multimanual systems. _arXiv preprint arXiv:2602.02269_ . 

- ˇSkerlj, J., Bien, S., Naceri, A., and Haddadin, S. (2026b). multipanda ~~r~~ os2: A sim- and real Panda robot integration based on the ros2 ~~c~~ ontrol framework. https: //github.com/tenfoldpaper/multipanda ros2. Accessed: 2026-07-24. 

- Tingelstad, L. (2024). libfranka with active control for the Franka Emika Panda. https://github.com/tingelst/libf ranka. Accessed: 2026-07-24. 

- Todorov, E., Erez, T., and Tassa, Y. (2012). Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , page 5026–5033. IEEE. 

