---
title: "Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies"
date: "2026-03-16"
authors: "Utkarsh Grover; Ravi Ranjan; Mingyang Mao; Trung Tien Dong; Satvik Praveen; Zhenqi Wu"
url: https://arxiv.org/abs/2603.16952
pdf: https://arxiv.org/pdf/2603.16952
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.16952)** / [論文ページ](https://arxiv.org/abs/2603.16952)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies** 

UTKARSH GROVER, University of South Florida, USA RAVI RANJAN, Florida International University, USA MINGYANG MAO, University of South Florida, USA TRUNG TIEN DONG, University of South Florida, USA SATVIK PRAVEEN, University of South Florida, USA ZHENQI WU, University of South Florida, USA 

J. MORRIS CHANG, University of South Florida, USA TINOOSH MOHSENIN, Johns Hopkins University, USA YI SHENG, University of South Florida, USA 

AGORITSA POLYZOU, Florida International University, USA 

EIMAN KANJO, Nottingham Trent University, United Kingdom and Imperial College London, United Kingdom 

XIAOMIN LIN, University of South Florida, USA 

Deploying foundation models in embodied edge systems is fundamentally a systems problem, not just a problem of model compression. Real-time control must operate within strict size, weight, and power constraints, where memory traffic, compute latency, timing variability, and safety margins interact directly. The Deployment Gauntlet organizes these constraints into eight coupled barriers that determine whether embodied foundation models can run reliably in practice. Across representative edge workloads, autoregressive Vision-LanguageAction policies are constrained primarily by memory bandwidth, whereas diffusion-based controllers are limited more by compute latency and sustained execution cost. Reliable deployment therefore depends on system-level co-design across memory, scheduling, communication, and model architecture, including decompositions that separate fast control from slower semantic reasoning. 

## **1 Introduction** 

The migration of Foundation Models (FMs) [133] from hyperscale data centers to resource-constrained edge platforms changes the execution model of intelligence itself [15, 99]. Cloud scale FMs are typically developed under assumptions of elastic power, abundant cooling, and comparatively relaxed latency constraints. Embodied platforms violate all three. Autonomous mobile robots (AMRs), aerial systems, and wearables must execute perception, inference, and control within strict Size, Weight, and Power (SWaP) budgets and under hard real-time constraints [46]. In this regime, deploying foundation models is not merely a model compression problem, but a closed-loop systems problem [135]: memory intensive inference must remain reliable despite thermal variation, battery-limited operation, shared-memory contention, and timing-sensitive control. 

This setting makes Moravec’s Paradox operational rather than philosophical. High level reasoning has become increasingly accessible to large models, but robust sensorimotor integration 

Authors’ Contact Information: Utkarsh Grover, University of South Florida, Tampa, FL, USA, utkarshgrover@usf.edu; Ravi Ranjan, Florida International University , Miami, FL, USA, rkuma031@fiu.edu; Mingyang Mao, University of South Florida, Tampa, FL, USA, mmao@usf.edu; Trung Tien Dong, University of South Florida, Tampa, FL, USA, dongt@usf.edu; Satvik Praveen, University of South Florida, Tampa, FL, USA, satvikpraveen@usf.edu; Zhenqi Wu, University of South Florida, Tampa, FL, USA, zhenqi@usf.edu; J. Morris Chang, University of South Florida, Tampa, FL, USA, chang5@usf.edu; Tinoosh Mohsenin, Johns Hopkins University, Baltimore, MD, USA, tinoosh@jhu.edu; Yi Sheng, University of South Florida, Tampa, FL, USA, sheng1@usf.edu; Agoritsa Polyzou, Florida International University, Miami, FL, USA, apolyzou@fiu.edu; Eiman Kanjo, Nottingham Trent University, Nottingham, United Kingdom, eiman.kanjo@ntu.ac.uk and Imperial College London, London, United Kingdom, e.kanjo@Imperial.ac.uk; Xiaomin Lin, University of South Florida, Tampa, FL, USA, xlin2@usf.edu. 

Grover et al. 

2 

remains computationally expensive and architecturally brittle [118]. Embodied autonomy depends on multimodal perception that aligns light, sound, and geometry tightly enough to preserve control fidelity [61]. Once these multi-rate, asynchronous sensor streams are coupled to large, memory-heavy foundation models, the dominant bottlenecks shift from model accuracy alone to timing, bandwidth, synchronization, and runtime stability. These bottlenecks are far less severe in disembodied or cloud-centric deployments. 

Accordingly, this survey examines embodied foundation models through the systems constraints that govern whether they can be deployed reliably on edge platforms. We do not survey the edge stack in full, nor do we treat middleware, embedded operating systems, or sensor hardware as independent topics. We consider them only where they become first-order constraints on closed-loop FM deployment. Our central claim is that many of the most consequential embodied deployment failures arise not from parameter count alone, but from cross-layer interactions among sensing, compute, memory, timing, power, and control. 

## **1.1 The Multimodal Execution Imperative** 

Closed-loop autonomy requires world representations that can be updated and acted upon within tight latency budgets. Vision-Language-Action architectures such as RT-2 and OpenVLA pursue this goal by combining perception, semantic grounding, and policy generation in a unified inference stack [85, 214]. That unification simplifies interfaces and improves cross-modal reasoning, but it also places sensing, inference, and control on the same critical path. A representative 7B-parameter VLA may require sustained high-bandwidth weight movement, dense attention computation, and tightly synchronized ingestion of heterogeneous sensor streams [45]. These requirements often exceed the latency, bandwidth, and scheduling margins available on embedded edge platforms. 

The mismatch is modality specific. On accelerators such as the NVIDIA Jetson AGX Orin and Qualcomm RB5, sparse LiDAR workloads underutilize dense tensor hardware and often incur CPU-mediated scatter-gather overheads [36, 162]. Transformer based audio models can exceed the SRAM capacity of low power DSPs, forcing costly off chip accesses [134, 210]. High resolution visual encoders generate bursty traffic that can saturate LPDDR channels and trigger thermal throttling [40, 43]. More broadly, design trends that favor large, modality spanning foundation models in server class settings [136, 165] become substantially harder to sustain at the sensor edge, where parameter scale, deep attention stacks, and autoregressive decoding amplify memory pressure, latency variance, and scheduling instability [160]. These execution pressures motivate a systems view of embodied FM deployment. 

## **1.2 The Deployment Gauntlet** 

Most current approaches to deploying foundation models on constrained hardware emphasize local optimizations such as quantization and pruning [59, 88]. These methods reduce inference cost and remain valuable, but they do not resolve the dominant failures of embodied deployment, where sensing, computation, memory, timing, and control interact under closed-loop execution. In embodied systems, stress in one layer readily propagates across the stack and degrades overall reliability. To organize this problem, we introduce the **_Deployment Gauntlet_** , a systems taxonomy of the conditions that embodied foundation models must satisfy to operate robustly in real-time edge environments. 

Figure 1 summarizes the eight barriers that constitute the Deployment Gauntlet. They capture recurring bottlenecks across the embodied intelligence pipeline, spanning multimodal sensing and data movement, heterogeneous computation and shared memory, time critical control, long horizon operation, safety enforcement, and edge-cloud coordination. Although analytically distinct, they are tightly coupled in practice: pressure in one dimension often amplifies failure in others. The 

3 

Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies 


Fig. 1. The Deployment Gauntlet. A unified view of the eight major system barriers that limit the deployment of foundation models from the cloud to edge embodied AI platforms. 

taxonomy therefore provides a concrete framework for reasoning about the deployment constraints that govern real time embodied AI. 

We organize the Deployment Gauntlet into eight coupled barriers spanning the sensing to control continuum: 

- (1) _The Sensor Fusion Tax:_ Latency and jitter introduced by temporally aligning asynchronous sensor streams, including middleware-induced serialization and buffering overheads (e.g., ROS 2) [87, 114]. 

- (2) _Heterogeneous Compute Mismatch:_ Inefficiencies that arise when sparse or irregular workloads are mapped onto accelerators optimized for dense, static matrix operations [71]. 

- (3) _Unified Memory Bottleneck:_ Contention between high-bandwidth model weight streaming and continuous sensor ingestion over shared memory channels [126, 179]. 

- (4) _Energy & Thermal Ceiling:_ Performance degradation caused by thermal throttling and battery depletion during sustained operation [22]. 

- (5) _Long-Horizon Drift:_ Progressive degradation of state estimation, calibration, and clock synchronization over extended deployments [19]. 

- (6) _Safety & Verification Gap:_ Safety-critical failures induced by hallucinated states or out-ofdistribution behavior within control loops [9, 209]. 

- (7) _Real-Time Scheduling Interference:_ Control instability driven by OS jitter, non-deterministic kernel execution, and contention on shared accelerators [23]. 

- (8) _Communication Constraints:_ Bandwidth and latency limits that restrict edge-to-cloud offloading and multi-agent coordination [148]. 

The remainder of the survey develops this argument in three parts. We first examine the workload characteristics of embodied foundation models and show why multimodal, closed-loop execution imposes qualitatively different demands from static cloud inference. We then use the Deployment Gauntlet to organize the principal systems barriers reported across the literature. Finally, we synthesize the mitigation strategies and architectural directions that appear most promising for improving reliability under real-time edge constraints. 

## **2 Landscape of Foundation Models on the Edge** 

Grover et al. 

4 

Table 1. Edge-relevant workload classes for embodied foundation model deployment. 

|**Workload Class**|**Representativ**<br>**Models**|**e**|**Primary**<br>**Role**<br>**/**<br>**Modality**|**Dominant Bottleneck**|
|---|---|---|---|---|
|Vision-Language-<br>Action<br>(VLA)<br>Policies|RT-2<br>OpenVLA<br>NanoVLA[26]|[214],<br>[85],|Policy<br>generation;<br>RGB + language to<br>action|Memory traffic and weight streaming during autoregressive decoding,<br>which compete directly with sensor DMA and shared-memory service.|
|Diffusion-Based<br>Policies|Octo<br>OneDP<br>LightDP [188]|[167],<br>[181],|Trajectory genera-<br>tion; RGB / multi-<br>modal to action se-<br>quence|Sustained compute and thermal load from iterative denoising, which<br>imposes a latency floor and high energy cost.|
|Vision Encoders<br>and<br>Multimodal<br>LMMs|LLaVA-Mini<br>MiniCPM-V [1|[206],<br>95]|Perception and rea-<br>soning; RGB + lan-<br>guage|Visual prefill and bursty frame ingestion, which create transient com-<br>pute and memory spikes during high-resolution encoding.|
|3D / LiDAR En-<br>coders|PointPillars<br>DensePillarNet<br>BEVFusion[10|[92],<br><br>[25],<br>7]|Geometric<br>per-<br>ception;<br>LiDAR<br>/<br>LiDAR + RGB|Sparsity and irregular memory access, which reduce accelerator uti-<br>lization and increase synchronization overhead.|
|Multimodal<br>Fu-<br>sion Stacks|MMEdge [74],<br>sion [107]|BEVFu-|Cross-modal<br>state<br>construction; RGB /<br>LiDAR / audio / text|Scheduling and synchronization pressure from shared middleware,<br>memory bandwidth, and callback timing.|


Table 1 summarizes the workload classes most relevant to embodied foundation model deployment at the edge, together with their representative models, functional role, and dominant systems bottleneck. Embodied deployment increasingly favors decomposed execution over monolithic end-to-end inference. In practice, server-resident cognitive backbones are paired with compressed on-device executors that handle latency-critical perception and control. Consumer systems already reflect this pattern. Apple’s iOS 18 “Intelligence,” for example, couples a server-resident model with an on-device model of roughly three billion parameters, using LoRA adapters and mixed 2-bit/4-bit quantization to preserve interactive latency [120]. Google’s _Gemini Robotics On-Device_ likewise executes vision-language-action (VLA) policies entirely on board for bimanual manipulation without network dependence [166]. 

Robotic platforms make the same constraints more severe. Foundation level policies such as PaLM-SayCan and RT-2 demonstrate strong semantic grounding and task planning [4, 214], but deployment still depends on distillation, hardware specialization, or architectural decomposition to satisfy latency and power limits. Recent examples include diffusion-transformer-based Large Behavior Models on Boston Dynamics’ Atlas [202] and the deployable on-board inference engines used in NVIDIA’s R<sup>2</sup> D<sup>2</sup> sim-to-real pipeline [197]. The implication is clear: unconstrained generative inference does not by itself yield safe embodied execution. Reliable deployment requires co-design across model architecture, training strategy, runtime, and embedded hardware [120]. 

This section focuses on the workload classes that most clearly expose the systems pressures later organized by the Deployment Gauntlet. The objective is not to catalog every edge workload in embodied AI, but to identify the classes whose execution is dominated by distinct bottlenecks under Size, Weight, and Power (SWaP) constraints. We therefore focus on workloads governed primarily by memory bandwidth, sustained compute demand, visual prefill cost, sparsity and irregular access, or cross-modal scheduling pressure. 

## **2.1 Taxonomy of Edge-Relevant Workloads** 

Aggregate metrics such as parameter count and FLOPs are poor predictors of whether a foundation model will execute reliably on an embodied edge platform [71]. We therefore classify edge-relevant workloads along three practical axes. The first is the _primary role_ of the model in the control loop, distinguishing perception-heavy models from policy-generating models [52, 98]. The second is the _I/O modality_ , which ranges from dense, high-throughput inputs such as RGB video to sparse, 

Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies 5 

irregular inputs such as LiDAR point clouds [191]. The third is the _dominant execution bottleneck_ : memory capacity and bandwidth, sustained compute demand, or I/O throughput [131, 184]. 

These axes matter because workloads with similar nominal scale can behave very differently once deployed under SWaP and real-time constraints. Two models with comparable parameter counts may place entirely different demands on memory traffic, thermal headroom, accelerator utilization, or scheduler stability. For this reason, the discussion below emphasizes workload structure rather than aggregate model size. 

## **2.2 Vision-Language-Action (VLA) Policies** 

Vision-Language-Action (VLA) policies [64, 144] are among the most demanding workloads in embodied AI because they couple semantic reasoning directly to action generation. Architectures such as RT-2 [214] and OpenVLA [85] jointly tokenize observations and actions, producing discrete control outputs such as end-effector poses or skill tokens from RGB inputs and language commands. This unification improves task generalization, but it also places deliberation and actuation on the same execution path. OpenVLA-7B, for example, requires roughly 14 GB in FP16, which approaches or exceeds the practical memory budget of unified-memory SoCs such as the Jetson Orin NX once operating system overhead and sensor buffering are accounted for. 

At the edge, VLA execution is constrained primarily by memory traffic rather than peak arithmetic throughput. Autoregressive decoding repeatedly streams large weight tensors for each generated action token, creating sustained DRAM pressure. On embedded platforms, this traffic competes directly with high-rate sensor DMA streams and can introduce latency spikes that violate control deadlines [131]. Monolithic VLA inference is therefore difficult to reconcile with deterministic closed-loop control. 

Recent systems address this mismatch by decomposing VLA inference across timescales. NanoVLA [26], for example, assigns high-level semantic reasoning to a heavyweight vision-language model while delegating higher-frequency control to a lightweight visual policy. This separation reduces sustained memory pressure and substantially improves execution speed on edge hardware. For the Deployment Gauntlet, VLA policies are best viewed as a _memory-bandwidth-dominated_ workload, and they directly motivate the barriers associated with shared memory contention and real-time interference [4]. 

## **2.3 Diffusion-Based Policies** 

Diffusion-based policies define a different edge regime. Rather than emitting discrete action tokens, they generate continuous action trajectories through iterative denoising [33]. This structure is attractive for contact-rich manipulation and smooth trajectory generation, and systems such as Octo [167] illustrate its promise for generalist multimodal behavior. The same iterative structure, however, imposes a latency floor that conflicts with the update rates expected in real-time control. 

On edge hardware, diffusion policies are constrained primarily by sustained compute demand and energy draw. Each denoising step performs dense matrix operations over the same control horizon, keeping accelerators active for long intervals and increasing both power and thermal load. Naive multi-step diffusion controllers often operate at only 1–2 Hz, which is inadequate for many closed-loop manipulation settings. The main deployment question is therefore not whether diffusion can produce high-quality trajectories, but whether it can do so within a timing and thermal envelope compatible with embodied control. 

Edge-oriented work has focused on collapsing the denoising process. OneDP [181] distills multistep diffusion into a single-step generator and reports an increase from roughly 1.5 Hz to more than 60 Hz on representative edge hardware. LightDP [188] reduces compute demand through pruning and architectural simplification to stay within mobile thermal limits. These methods 

Grover et al. 

6 

improve responsiveness substantially, but they do not change the fact that diffusion policies remain a _compute and energy-dominated_ workload. In the Deployment Gauntlet, they map most directly to the energy, thermal, and accelerator utilization barriers. 

## **2.4 Vision Encoders and Multimodal LMMs** 

Vision encoders and multimodal large language models (LMMs) impose a third execution profile, dominated by the cost of ingesting high-resolution visual streams at video rate. These models provide the perceptual substrate for downstream planners and controllers, but at the edge their limiting factor is often not steady-state decoding. It is repeated visual _prefill_ . Large encoders such as CLIP-ViT-L provide strong semantic representations [134], yet their quadratic attention cost makes naive frame-rate deployment computationally and thermally expensive on embedded hardware. 

Edge oriented perception pipelines therefore aim to compress or amortize visual ingestion. LLaVAMini [206] reduces prefill cost by compressing visual input to a single token before language-model ingestion. MiniCPM-V [195] shows that architecture choices tuned explicitly for mobile inference, combined with targeted data curation, can approach high-end multimodal performance without increasing model scale. ViT-Edge [141] further systematizes encoder-side optimizations such as low-rank factorization and structured compression. 

For the Deployment Gauntlet, the central point is that these models are _prefill-bound_ and thermally sensitive. Continuous video ingestion creates bursty compute demand during frame processing, and those bursts can dominate the power envelope of fanless edge modules [131]. When visual tokens cannot be cached, reused, or updated incrementally across frames, the encoder becomes a major source of throttling even if downstream reasoning is lightweight. This workload therefore motivates the barriers associated with bandwidth spikes, thermal instability, and burstdriven runtime interference. 

## **2.5 3D & LiDAR Encoders** 

3D and LiDAR encoders expose a different systems limitation: sparsity. Unlike dense vision workloads, point-cloud pipelines are dominated by irregular memory access, dynamic spatial density, and data-dependent control flow. These properties violate the locality and throughput assumptions built into most dense accelerators [36]. PointPillars remains a widely used baseline because it projects sparse point clouds into pseudo-images and thereby recovers partial compatibility with 2D CNN hardware [92]. 

That projection only mitigates the problem. DensePillarNet [25] restructures the backbone to favor denser execution and reduces end-to-end latency on constrained devices, but voxelization and feature aggregation still introduce irregular accesses that are difficult to schedule efficiently. In multimodal systems such as BEVFusion [107], intermediate features must often be scattered and gathered across CPU and GPU boundaries, creating synchronization overhead and latency variance. 

From an execution perspective, 3D perception is _sparsity-bound_ . Voxelization and point aggregation disrupt cache behavior, reduce SIMD utilization, and map poorly to fixed-function inference engines such as NVIDIA’s DLA, which lack native support for sparse indexing and dynamic structures [162]. As a result, even moderately sized 3D perception stacks can monopolize shared compute and memory resources and interfere with time-critical control. Within the Deployment Gauntlet, these workloads motivate the barriers associated with heterogeneous compute mismatch and shared-resource contention. Table 2 summarizes the workload classes most relevant to embodied foundation model deployment at the edge, together with the dominant execution bottleneck and the characteristic failure mode each class introduces under SWaP and real-time constraints. 

Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies 

7 

Table 2. Representative edge-relevant workload classes and their dominant execution bottlenecks in embodied foundation model deployment. 

|**Workload**|**Dominant**<br>**Bottle-**<br>**neck**|**Characteristic Edge Failure Mode**|
|---|---|---|
|Vision-Language-<br>Action<br>(VLA)<br>Policies|Memory traffic and<br>weight streaming|Autoregressive action decoding repeatedly streams large parameter tensors, competing<br>with sensor DMA traffic over shared memory and introducing latency spikes that can<br>violate closed-loop control deadlines [26,85,131].|
|Diffusion-Based<br>Policies|Sustained<br>compute<br>and thermal load|Iterative denoising requires repeated dense matrix execution over the same control horizon,<br>creating a latency floor, high energy draw, and thermal throttling that reduce practical<br>control frequencyon edgeplatforms[33,181,188].|
|Vision<br>Encoders<br>and<br>Multimodal<br>LMMs|Visual<br>prefill<br>and<br>bursty ingestion|High-resolution visual streams require repeated encoder prefill, producing burst-driven<br>compute and memory demand that can dominate the thermal envelope even when down-<br>stream reasoning remains lightweight [134,141,195,206].|
|||Point-cloud pipelines rely on voxelization, sparse indexing, and data-dependent aggregation,|
|3D & LiDAR En-<br>coders|Sparsity and irregular<br>memoryaccess|which map poorly to dense accelerators, reduce utilization, and introduce synchronization<br>overhead in multimodal stacks[36,92,107,162].|
|||Even when unimodal components meet latency targets in isolation, their composition|
|Multimodal Fusion<br>Stacks|Scheduling and syn-<br>chronization|through shared middleware, LPDDR bandwidth, and runtime scheduling can produce<br>temporal misalignment and end-to-end timingfailures[13,50,74,87].|


## **2.6 Multimodal Fusion Stacks** 

Multimodal fusion is where these workload-specific pressures converge. Fusion stacks combine heterogeneous perceptual streams into a temporally consistent state for planning and control [50]. They do not introduce a single new compute primitive so much as couple the execution behavior of all upstream modalities. Fusion is therefore less a model-level bottleneck than a systems-level one. 

Recent systems such as MMEdge [74] replace sequential fusion with pipelined sensing that overlaps ingestion, encoding, and fusion. This improves average throughput, but throughput alone is insufficient. Once modalities share middleware, memory bandwidth, and runtime scheduling, end-to-end behavior depends on callback latency, executor design, DMA contention, and operatingsystem preemption [87]. On unified-memory SoCs, fusion also becomes the locus of contention among sensor ingestion, model weight movement, and intermediate activation storage [13]. Parallel multimodal perception pipelines have also been explored in TinyML deployments. For example, lightweight sensor processing on multiple cores combined with specialised hardware accelerators such as TPUs can enable efficient real-time behaviour recognition directly on edge devices [205] . 

Multimodal fusion is therefore best viewed as a _scheduling- and synchronization-dominated_ workload. Individual models may satisfy latency targets in isolation yet fail once composed through shared middleware and memory. The resulting errors are not necessarily model errors; they are timing errors. This workload class directly motivates the synchronization, scheduling, and communication barriers that appear later in the Deployment Gauntlet. 

_Section summary._ The workload classes in Table 2 motivate a systems taxonomy rather than a model-centric account of edge deployment. VLA policies are dominated by memory traffic and weight streaming, diffusion policies by sustained compute and thermal load, vision encoders by visual prefill and bursty ingestion, 3D perception by sparsity and irregular memory access, and multimodal fusion by scheduling and synchronization. Section 3 builds on this distinction and organizes the resulting deployment failures through the Deployment Gauntlet. 

Grover et al. 

8 


Fig. 2. The taxonomy for the gauntlets and solutions in Foundation Models under Embodied Constraints. 

## **3 The Deployment Gauntlet** 

Section 2 showed that embodied foundation model workloads differ sharply in their dominant execution bottlenecks. In deployment, however, these workloads rarely operate in isolation. Memory intensive VLA policies, compute-heavy diffusion controllers, burst-driven visual encoders, and synchronization sensitive fusion pipelines are typically co-located on the same embedded systemon-chip (SoC), where they compete for shared memory bandwidth, thermal headroom, power budget, and scheduling priority [13]. As a result, end-to-end failures often emerge not from any single model component, but from their interaction under shared physical constraints. 

This interaction is the basis of the _Deployment Gauntlet_ . We use the term to denote a systems taxonomy of the recurring barriers that embodied foundation models must satisfy to operate reliably on edge platforms. These barriers appear across platforms, modalities, and application domains [52] because they arise from a common deployment setting: closed-loop execution under tight constraints on memory, compute, I/O, timing, power, and safety. When these pressures compound, systems exhibit latency variance, deadline misses, synchronization failures, and thermal throttling, even when individual components remain tractable in isolation. Figure 2 summarizes the Deployment Gauntlet as a systems taxonomy of the eight coupled barriers that shape reliable embodied foundation model execution at the edge. 

The Deployment Gauntlet is therefore not a list of isolated implementation defects, nor is it exhausted by local optimizations such as pruning, quantization, or accelerator specialization [71]. Instead, it organizes the recurring systems constraints that emerge when embodied foundation models must sustain real-time perception, inference, and control on shared edge hardware. The remainder of this section develops the Gauntlet through eight coupled barriers, each corresponding to a distinct but strongly interacting source of deployment failure. Table 3 (Barriers I-IV) and Table 4 (Barriers V-VIII), that emerge repeatedly across platforms, modalities, and application domains [52] 

## **3.1 The Sensor Fusion Tax** 

The **Sensor Fusion Tax** is the latency, jitter, and memory overhead incurred when heterogeneous, asynchronous sensor streams are transformed into time-aligned, control-ready representations. In embodied systems, this overhead can consume a substantial fraction of the control-cycle budget. It does not originate from a single bottleneck. Instead, it accumulates across temporal synchronization, spatial calibration, middleware orchestration, and representational translation. Foundation models intensify this burden because they add sustained memory traffic, increase sensitivity to timing error, and enlarge the execution graph that must remain stable under closed-loop operation. 

Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies 

9 

_3.1.1 Temporal and Spatial Misalignment._ Robotic sensing is inherently asynchronous: cameras, LiDAR, and IMUs operate on different clock domains and exhibit variable transport delay. Enforcing temporal consistency therefore requires buffering and synchronization mechanisms such as ROS 2’s _ApproximateTime_ filter. These improve alignment, but they also increase end-to-end latency and reduce control responsiveness. Li et al. [96] show that synchronization can idle downstream computation while waiting for delayed packets, reducing effective throughput. In high-speed manipulation, even millisecond-scale jitter can produce substantial divergence between perceived and true system state [79]. Spatial fusion introduces a second source of overhead. Calibration degrades under vibration, thermal expansion, and mechanical drift, and corrective methods such as LCCNet [113] and CalibRefine [31] add nontrivial computation to the control loop. The resulting trade-off is straightforward: better alignment often consumes more of the available control-cycle budget. 

_3.1.2 Middleware and Pipeline Overheads._ Middleware compounds these costs. ROS 2 enables modular message passing, but serialization and deserialization remain expensive even in intraprocess settings, with reported latency penalties of up to 50% relative to shared-memory designs [87]. For high-bandwidth modalities such as LiDAR and 4K video, repeated copying consumes memory bandwidth that would otherwise be available to inference. Non-deterministic scheduling further creates queue buildup and jitter spikes on the order of 10–40 ms [170]. Conventional fusion pipelines impose an additional constraint: they often block downstream inference until a complete sensor sweep has arrived, effectively tying control frequency to the slowest sensing modality. Pipelined systems such as MMEdge [74] reduce average latency by overlapping sensing and inference, but they do not remove the underlying synchronization and scheduling burden. 

_3.1.3 Representational Mismatch and Foundation Model Sensitivity._ Representational mismatch introduces a third source of overhead. Event cameras, for example, produce sparse, microsecondresolution streams that do not map naturally to frame-based foundation models. Converting these streams into dense tensors through reconstruction or voxelization can offset part of the energy advantage of neuromorphic sensing and increase CPU-side preprocessing overhead when dedicated support is unavailable [55, 57]. Foundation models then amplify the fusion burden in three ways. First, sustained parameter movement can saturate LPDDR bandwidth on unified-memory systems and reduce headroom for sensor buffering and transport [15]. Second, end-to-end VLA policies can be highly sensitive to temporal misalignment, so synchronization error propagates directly into action quality [163]. Third, practical control rate is often bounded not by nominal inference throughput, but by the slowest stage in the sensing and synchronization path [139]. 

_3.1.4 Implications._ The Sensor Fusion Tax is a recurring systems constraint in embodied deployment, not a narrow implementation artifact. Once perception is embedded in a real-time control stack, synchronization, calibration, and data movement become first-order determinants of latency stability, memory pressure, and closed-loop reliability. 

Grover et al. 

10 

Table 3. Deployment Gauntlet barriers 1–4: recurring system-level challenges for embodied foundation models at the edge. 

|**Barrier**|**Representative**<br>**Sub-**<br>**problem**|**Systems Effect**|
|---|---|---|
|Sensor Fusion<br>|Temporal and Spatial Mis-<br>alignment|Asynchronous sensor clocks, transport delay, and calibration drift force buffering, syn-<br>chronization, and corrective alignment, trading control responsiveness for temporal and<br>spatial consistency [31,79,96,113].|
|Tax|Middleware and Pipeline<br>Overheads|Serialization, copying, buffering, and sweep-level pipeline blocking consume bandwidth<br>and introduce latency jitter that destabilizes high-frequency control execution even when<br>average throughput is acceptable[74,87,170].|
||Representational<br>Mis-<br>match and Foundation-<br>Model Sensitivity|Modalities such as event streams require costly reconstruction or voxelization before they<br>can be processed by frame-based models, while foundation models further amplify fusion<br>overhead through higher memory traffic and greater sensitivity to timing error [15,55,<br>57,139,163].|
|Heterogeneous<br>|Operator Coverage Gaps<br>and Execution Bubbles|Limited operator support on edge accelerators forces graph partitioning, CPU fallback,<br>and host–device synchronization, creating execution bubbles and large latency spikes<br>that reduce end-to-end throughput[26,70].|
|Compute<br>Mismatch|Granularity<br>Mismatch<br>and Kernel Launch Over-<br>head|Fine-grained transformer kernels incur substantial launch overhead on embedded GPUs,<br>accounting for 30–60% of latency and driving utilization below 20% during autoregressive<br>decoding [201].|
||The Memory Wall un-<br>der Unified-Memory Ar-<br>chitectures|Shared LPDDR bandwidth contention among CPUs, GPUs, NPUs, and sensors makes<br>execution memory-bound and can offset nominal hardware-acceleration gains through<br>arbitration and tensor movement overhead[76,85].|
||Thermal Constraints and<br>Dark Silicon|Sustained multimodal workloads trigger DVFS throttling, reduce steady-state throughput,<br>and make nominalpeak compute difficult to maintain during prolonged execution[48,82].|
|Unified Memory|Bandwidth Saturation and<br>Arbitration|Concurrent FM parameter streaming and high-rate sensor ingestion saturate shared<br>LPDDR bandwidth, so accelerators stall because memory delivery, rather than arithmetic<br>throughput, becomes the limitingfactor[5,146,201].|
|i<br>Bottleneck|DMA Contention and Ac-<br>cess Pattern Interference|Sensor DMA traffic competes directly with accelerator memory access, while mismatched<br>access patterns reduce cache efficiency and increase latency variance across perception<br>and control loops[13,76].|
||Software Amplification of<br>Memory Pressure|Middleware buffering, serialization, and large FM weight footprints amplify memory<br>pressure, triggering reallocations, evictions, and other memory-management events that<br>reduce throughput and destabilize execution[85].|
||Control-Loop<br>Conse-<br>quences|Memory stalls delay accelerators, block control threads, increase thermal load, and degrade<br>real-time behavior before nominal compute limits are reached[59,82,170].|
||Zero-Sum Power Compe-<br>tition|Foundation-model inference competes directly with propulsion, actuation, and sensing<br>for a fixed onboard energy budget, reducing endurance under sustained execution [73,<br>161201].|
|Energy &<br>Thermal Ceiling|DVFS and Steady-State<br>Throughput Loss|, <br>High-duty-cycle workloads exceed passive cooling capacity and trigger DVFS transitions<br>that reduce sustained throughput once theplatform reaches thermal equilibrium[159].|
||Control Degradation un-<br>der Thermal Stress|Reduced steady-state inference rate increases perception staleness and lowers closed-loop<br>responsiveness byslowingstate updates and control decisions[159].|
||Propagation of Thermal<br>Stress|Thermal coupling across the SoC can throttle CPUs responsible for sensing, middleware,<br>and control orchestration even when the model workload itself is unchanged[175].|
||Control-Loop Jitter and<br>Modal Trade-offs|Thermal limits can introduce actuation jitter and force the system to stagger, reduce,<br>or selectively disable sensing modalities to remain within sustained power and thermal<br>budgets[26,111,175,183].|


## **3.2 Heterogeneous Compute Mismatch** 

The **Heterogeneous Compute Mismatch** arises when embodied foundation model workloads are mapped onto edge platforms whose CPUs, GPUs, and NPUs are optimized for different classes of operators and execution regimes. Modern systems such as Jetson AGX Orin and Apple M- series devices rely on this heterogeneity to balance performance and energy efficiency under tight thermal limits [60]. Embodied FM workloads, however, combine dense tensor kernels, irregular preprocessing, host-side coordination, and latency-sensitive control in the same execution graph. The result is a recurring systems barrier: hardware heterogeneity improves nominal efficiency, but it undermines predictable low-latency execution. In practice, latency becomes sensitive to operator placement, runtime fragmentation, and scheduling effects rather than to peak compute alone [71]. 

Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies 

11 

_3.2.1 Operator Coverage Gaps and Execution Bubbles._ Foundation-model inference depends on a broad operator set, including attention, normalization, tensor reshaping, and irregular preprocessing, whereas edge NPUs accelerate a much narrower subset of dense kernels such as INT8 matrix multiplication. Unsupported operators force graph partitioning and CPU fallback, introducing host– device synchronization and interrupting otherwise continuous execution. These transitions create _execution bubbles_ in which accelerators idle while control returns to the host. Sparse perception stages such as LiDAR voxelization are especially prone to these fallbacks and can introduce large latency spikes [70]. NanoVLA shows that removing even small CPU-resident operators can improve throughput by up to 1 _._ 7×, highlighting that fragmented execution, not peak compute alone, often determines end-to-end performance [26]. 

_3.2.2 Granularity Mismatch and Kernel Launch Overhead._ Foundation-model inference also mismatches the execution granularity of mobile GPUs. Transformer decoding decomposes into many fine-grained kernels, but embedded GPUs cannot amortize launch overhead as effectively as larger server-class devices. On Jetson Orin, CPU-side launch overhead can exceed kernel execution time and account for 30–60% of end-to-end latency during autoregressive decoding [201]. Under these conditions, runtime overhead becomes a major component of inference cost. For VLA policies, sequential token generation can drive utilization below 20%, making multi-billion-parameter models difficult to reconcile with high-frequency control. 

_3.2.3 The Memory Wall under Unified-Memory Architectures._ Unified-memory architectures amplify the mismatch further. On embedded SoCs, CPUs, GPUs, NPUs, and sensor DMA engines share the same LPDDR channels, so FM inference competes directly with high-rate perception traffic for bandwidth [76]. Diffusion-based policies intensify this pressure by revisiting large tensors across repeated denoising steps and sustaining DRAM traffic over long intervals. Cross-device tensor migration introduces an additional penalty. Moving high-resolution features between heterogeneous units, such as the CPU and NPU, serializes execution and can add 4–15 ms of latency, often offsetting the nominal benefit of hardware acceleration [85]. In this regime, end-to-end performance is constrained less by arithmetic throughput than by memory movement and bandwidth arbitration. 

_3.2.4 Thermal Constraints and Dark Silicon._ Thermal limits turn these inefficiencies into sustained deployment failures. Multimodal embodied pipelines often activate CPUs, GPUs, and NPUs concurrently, pushing passive or compact cooling systems beyond their practical envelope. Dynamic voltage and frequency scaling (DVFS) responds by reducing clock rates, and mixed-workload saturation has been reported to reduce steady-state inference throughput by as much as 60% relative to cold-start performance [82]. Foundation-model workloads are especially exposed because they sustain high utilization over time rather than in short bursts. As a result, nominal peak performance becomes difficult to maintain during prolonged operation, and systems that initially satisfy real-time targets may later fall below them as thermal throttling accumulates [48]. 

_3.2.5 Implications._ Heterogeneous Compute Mismatch is therefore not just an efficiency loss; it is a stability problem for closed-loop embodied execution. Once inference spans heterogeneous units under shared thermal and memory limits, operator placement, launch overhead, and runtime fragmentation become first-order determinants of whether the system can sustain safe real-time behavior. 

## **3.3 The Unified Memory Bottleneck** 

The **Unified Memory Bottleneck** arises when embodied workloads force inference, sensing, and runtime services to contend for the same LPDDR bandwidth and memory service time. Unlike server platforms with dedicated GPU VRAM, embedded SoCs place CPUs, GPUs, NPUs, and sensor 

Grover et al. 

12 

peripherals on a shared memory fabric. Under these conditions, performance is constrained less by nominal capacity than by arbitration and data movement under concurrent load [5]. In embodied systems, that contention directly degrades latency stability and closed-loop responsiveness. 

_3.3.1 Bandwidth Saturation and Arbitration._ Foundation-model inference places sustained pressure on memory bandwidth. Autoregressive decoding and diffusion-based policies repeatedly stream large parameter tensors from DRAM [146]. Data-center accelerators can mask much of this cost with bandwidth on the order of terabytes per second, whereas edge SoCs typically operate in the 25–204 GB/s range. In embodied deployment, that same bandwidth must also serve RGB cameras, LiDAR, event streams, and other high-rate inputs. As a result, accelerators often fail to reach nominal arithmetic throughput because execution is limited by memory supply rather than compute availability [201]. As arbitration pressure increases, latency variance rises and real-time margins shrink. 

_3.3.2 DMA Contention and Access Pattern Interference._ DMA traffic adds a second source of interference. On platforms such as Jetson AGX Orin, image signal processors, USB controllers, and other peripheral interfaces compete with GPU and NPU kernels for the same memory cycles [13]. Because DMA traffic is bursty and often hardware-prioritized, inference can stall even when average bandwidth appears sufficient. Access-pattern mismatch further reduces effective throughput. Linear sensor streams interfere with the poor-locality access patterns of attention layers and sparse LiDAR pipelines, reducing cache efficiency and degrading bandwidth utilization [76]. Under unified memory, this interference disrupts both sensor buffering and model weight reuse. 

_3.3.3 Software Amplification of Memory Pressure._ Software abstractions magnify the hardware bottleneck. Middleware frameworks such as ROS 2 often serialize, duplicate, or buffer high-bandwidth sensor messages across node boundaries. When large models already consume 6–8 GB for weights alone, these additional image and LiDAR buffers leave little headroom for stable execution. Small shifts in allocation demand can then trigger buffer reallocation, tensor rematerialization, page eviction, and other costly memory-management events. The result is latency jitter, throughput loss, and, in stressed regimes, node instability or watchdog resets [85]. The bottleneck therefore scales with model size not only because of hardware limits, but also because software layers amplify memory pressure. 

_3.3.4 Control-Loop Consequences._ The effects of memory contention extend well beyond inference throughput. When DRAM service becomes unreliable, NPUs stall waiting for on-chip buffers to refill, and CPU threads responsible for synchronization and control queue behind memory-bound tasks. In robotic systems operating at 50–100 Hz, these delays appear as actuator jitter, delayed servo response, and degraded sensor fusion [170]. Sustained DRAM traffic also raises power draw and accelerates thermal saturation, triggering DVFS before compute units are fully utilized [82]. Empirical studies show that workloads such as diffusion policies can drop from roughly 30 FPS in isolation to 6–12 FPS under realistic sensor load because of memory contention alone. In embodied settings, this is not just a throughput penalty; it directly affects the freshness of observations presented to the control loop [59]. 

_3.3.5 Implications._ The Unified Memory Bottleneck is therefore a first-order systems barrier in embodied edge deployment. Once sensing, inference, and control share the same memory fabric, bandwidth arbitration, DMA behavior, and software buffering become direct determinants of whether the platform can sustain safe real-time operation. 

Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies 

13 

Table 4. Deployment Gauntlet barriers 5–8: recurring system-level challenges for embodied foundation models at the edge. 

|**Barrier**|**Representative**<br>**Sub-**<br>**problem**|**Systems Effect**|
|---|---|---|
|Long-Horizon<br>Execution Drift<br>|The Stationarity Fallacy|Embodied deployment violates the stationarity assumptions of offline training: sensor<br>noise, actuator behavior, and calibration drift shift over time, causing prediction error<br>to accumulate as observations move away from well-supported regions of the training<br>distribution[89].|
|and Adaptation<br>Failure|Latent-State<br>Misalign-<br>ment|Physical drift can disrupt the alignment between sensory embeddings and action-relevant<br>latent structure, causing internally coherent predictions to diverge from the true physical<br>state of theplatform[68].|
||The Adaptation Gap|Edge platforms often cannot support timely online adaptation under SWaP constraints,<br>while cloud-mediated adaptation introduces latency and connectivity dependence, leaving<br>long-duration deploymentsgoverned byincreasinglyoutdated model assumptions[56,137].|
||Residual Hardware and<br>Environment-Coupled<br>Drift|Sensor bias instability, thermal noise, mechanical wear, and terrain-dependent slip intro-<br>duce residual time-varying error that classical compensation can attenuate but not fully<br>remove[142,151,176,212].|
|Safety &|Stochastic<br>Objectives<br>and Constraint Viola-<br>tions|Likelihood-based objectives such as token prediction and diffusion denoising do not in-<br>herently encode hard physical constraints, so actions may be statistically plausible while<br>remainingdynamicallyunsafe under real-worldperturbations[172].|
|<br>Verification Gap|Opacity and Hierarchical<br>Misalignment|High-dimensional latent representations are difficult to interpret formally, and mismatched<br>interfaces between learned planners and constrained controllers can yield semantically<br>valid but dynamicallyinfeasible actions[4,52,194].|
||Limits of Retrofitted Ver-<br>ification|Barrier certificates, reachability analysis, and fallback logic provide only partial coverage<br>when state estimates are shifted, uncertainty is poorly calibrated, or policy dimensionality<br>exceeds the scope ofpractical formal analysis.|
||Operational Sandboxing<br>and Structural Implica-<br>tions|Reduced velocities, geofencing, teleoperation, and runtime safety monitors lower opera-<br>tional risk, but they remain reactive and do not remove the underlying mismatch between<br>generative model behavior andphysicallyconstrained control[117,145].|
|OS & Scheduling<br>|Best-Effort<br>Scheduling<br>and Runtime Nondeter-<br>minism|Throughput-oriented schedulers and runtime-level serialization introduce jitter, deschedul-<br>ing, and callback delay that are difficult to reconcile with bounded-latency control execu-<br>tion[147,154].|
|Bottleneck|Jitter Propagation Across<br>the Stack|Descheduling, priority inversion, and shared-resource contention propagate across sensing,<br>inference, and actuation, producing bursty sensing, irregular frame timing, and cross-layer<br>jitter cascades[154].|
||Control-Theoretic Con-<br>sequences|Best-effort timing violates assumptions such as bounded execution and regular sampling,<br>introducing heavy-tailed delay that can manifest as oscillation, missed grasps, or delayed<br>corrective action[62].|
||Bus<br>Arbitration,<br>Net-|Shared DMA engines, LPDDR arbitration, network delay, and middleware serialization|
|I/O &<br>Communication|work Stochasticity, and<br>Middleware Overhead|<br>jointly disrupt bounded-delay multimodal transport, degrading throughput and timing<br>regularityunder load[115,119,125].|
|Bottleneck|Cross-Layer Timing Cas-<br>cades|Delayed data movement can stall inference, misalign fusion, reorder messages, and propa-<br>gate timing inconsistency across perception, planning, and control rather than remaining<br>local to the transport layer.|


## **3.4 The Energy and Thermal Ceiling** 

The **Energy and Thermal Ceiling** arises because mobile platforms must execute foundation models within fixed power, cooling, and endurance budgets. Unlike cloud infrastructure, mobile and aerial robots operate under strict Size, Weight, Power, and Cost (SWaP-C) constraints and have little thermal headroom. Under these conditions, sustained inference competes directly with propulsion, sensing, and actuation for both energy and heat dissipation capacity [161]. As a result, embodied performance is often bounded by steady-state power and thermal limits before nominal model capacity is reached. 

_3.4.1 Zero-Sum Power Competition._ On embedded platforms, computation and physical actuation draw from the same onboard energy reservoir. In aerial systems, allocating an additional 10–15 W to accelerator-driven transformer inference can reduce flight endurance by several minutes [201]. The trade-off is particularly severe for foundation models because their cost is driven not only by 

Grover et al. 

14 

arithmetic but also by DRAM access, which remains among the most energy-intensive operations in modern hardware [73]. Sustained memory traffic therefore raises both power draw and heat generation, forcing a direct trade-off between model throughput and operational range. 

_3.4.2 DVFS and Steady-State Throughput Loss._ As the platform approaches its thermal envelope, Dynamic Voltage and Frequency Scaling (DVFS) lowers clock rates to maintain safe operation. The result is a drop in sustained throughput that can differ markedly from cold-start performance. A vision encoder that begins near 30 FPS, for example, may settle at a much lower rate after thermal throttling. Benchmark studies indicate that high-duty-cycle foundation-model workloads often enter this regime within minutes of continuous execution [159]. For embodied deployment, the relevant metric is therefore not startup throughput, but the control rate the platform can maintain after reaching thermal equilibrium. 

_3.4.3 Control Degradation under Thermal Stress._ This steady-state slowdown propagates directly into the control stack. A policy that initially runs near 20 Hz may stabilize at a much lower frequency after throttling, increasing perception staleness and reducing closed-loop responsiveness. In embodied systems, timing margins are often narrow, so reduced inference rate leads directly to slower state updates and delayed control decisions. Thermal stress therefore alters not only throughput, but the temporal behavior of the system as a whole. 

_3.4.4 Propagation of Thermal Stress._ Thermal effects are also coupled across the SoC. CPUs, GPUs, and NPUs typically share a die-level or package-level thermal envelope, so sustained GPU or NPU utilization can trigger CPU throttling even when the model workload itself is unchanged. This is consequential because the CPU continues to handle sensor drivers, middleware callbacks, and control orchestration. When CPU frequency drops, those services slow as well, increasing end-to-end latency outside the model proper [175]. 

_3.4.5 Control-Loop Jitter and Modal Trade-offs._ Once throttling spreads through the system, controlloop timing degrades. A nominal 100 Hz loop can develop substantial actuation jitter when CPUbound planning and coordination stages stretch from single-digit milliseconds to tens of milliseconds [175]. Thermal limits also constrain multimodal execution. Running high-resolution vision, LiDAR fusion, and continuous audio concurrently can exceed the thermal design power of compact edge SoCs, forcing the system to reduce rates, stagger execution, or disable modalities selectively. In this setting, compact architectures such as NanoVLA [26], TinyVLA [183], and OneDP [111] are not just efficiency improvements; they are practical mechanisms for keeping multimodal inference within sustained thermal and power budgets. 

_3.4.6 Implications._ The Energy and Thermal Ceiling is a sustained-execution barrier, not a shortburst benchmarking artifact. For embodied deployment, the relevant question is not whether a model can run briefly at peak speed, but whether the platform can maintain the required sensing, inference, and control rate over time without exhausting energy reserves or destabilizing timing. 

## **3.5 Long-Horizon Execution Drift and Adaptation Failure** 

The **Long-Horizon Execution Drift and Adaptation Failure** barrier arises because embodied foundation models are deployed with mostly fixed representations in physical systems whose sensing, actuation, and environment change over time. Unlike cloud inference, embodied execution is inherently non-stationary: sensor characteristics shift, actuator behavior changes, and contact dynamics evolve across deployment horizons. When frozen models continue to assume a stable observation–action mapping under these conditions, prediction error accumulates and control 

Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies 

15 

quality degrades [158]. The core difficulty is not drift alone, but drift combined with limited capacity for online correction on edge platforms. 

_3.5.1 The Stationarity Fallacy._ Embodied deployment violates the stationarity assumptions embedded in offline training. Sensor noise changes with temperature, actuator output degrades with battery discharge, and calibration shifts under vibration and wear. These effects induce persistent covariate shift in _𝑃_ ( _𝑂𝑡_ ). Classical robotics pipelines address such variation through online state estimation and model-based correction, but frozen foundation models typically lack an equally direct mechanism for updating their internal representation of routine physical change. As drift accumulates, observations move away from well-supported regions of the training distribution, and prediction error compounds over time [89]. This yields a gradual degradation mode that is often underrepresented in short-horizon evaluation. 

_3.5.2 Latent-State Misalignment._ Long-horizon drift is especially problematic for policies that rely on latent state integration, including Vision-Language-Action (VLA) and diffusion-based controllers. These systems assume that sensory embeddings remain aligned with the action-relevant structure learned during training. Physical perturbations can disrupt that alignment, mapping observations into latent regions that are less informative for control. The model may then continue to produce internally coherent predictions while diverging from the true physical state of the platform [68]. Recovery becomes difficult because the same drift that corrupted the latent state also weakens the corrective value of subsequent observations. 

_3.5.3 The Adaptation Gap._ The barrier is compounded by an **adaptation gap** at the edge. Online gradient-based adaptation is often incompatible with the compute, timing, and energy budgets of SWaP-constrained platforms, while cloud-mediated adaptation introduces latency and connectivity dependence. As a result, long-duration deployments may be governed by increasingly outdated model assumptions. Test-time adaptation methods are promising [56, 137], but current approaches often remain too costly or too slow for real-time edge execution. In practice, model error and physical drift can therefore reinforce one another over long horizons. 

_3.5.4 Residual Hardware and Environment-Coupled Drift._ Not all long-horizon drift can be removed through classical compensation. Sensor and actuator behavior contain residual, time-varying effects that violate idealized estimator assumptions and remain only partially observable during deployment. At the sensor level, IMUs exhibit bias instability under temperature and vibration, establishing a persistent noise floor [212]. Vision and LiDAR sensors show related non-stationarity through thermally induced noise, gain variation, and dark-current shifts [176]. At the actuation level, mechanical wear changes friction and compliance, while terrain-dependent slip breaks rigidbody assumptions and accumulates odometric error [142, 151]. Classical filters can attenuate part of this drift, but residual error remains and continues to perturb the observation action mapping presented to the model. 

_3.5.5 Implications._ Long-horizon execution drift is therefore not only a perception or calibration issue. It is a systems-level barrier that emerges when fixed model representations are coupled to evolving physical platforms without a practical mechanism for continual correction. Over long missions, robust deployment depends not just on initial model accuracy, but on whether the system can preserve alignment among sensing, latent state, and control as conditions change. 

## **3.6 The Safety and Verification Gap** 

The **Safety and Verification Gap** arises because foundation-model objectives, representations, and inference behavior do not provide the same safety assurances as explicitly constrained control 

Grover et al. 

16 

pipelines. Classical control stacks are often built around known dynamics, feasibility constraints, and analyzable stability conditions; embodied foundation models instead inherit the stochasticity and opacity of large neural architectures. In these systems, strong predictive or generative performance does not imply constraint satisfaction or safe closed-loop behavior. The gap therefore reflects a structural mismatch between how these models are trained and what physical autonomy requires. 

_3.6.1 Stochastic Objectives and Constraint Violations._ Foundation models are typically optimized for predictive likelihood, denoising quality, or sequence modeling objectives rather than explicit physical risk. Vision-Language-Action token prediction, diffusion denoising, and latent interpolation do not inherently encode hard constraints such as joint limits, contact stability, or collision margins. As a result, generated actions may be statistically plausible while still being dynamically unsafe. Modest perturbations, including sensor noise, lighting variation, or adversarial artifacts, can induce action errors and constraint violations in embodied settings [172]. The core limitation is straightforward: likelihood-based objectives do not, by themselves, enforce physical invariants at inference time. 

_3.6.2 Opacity and Hierarchical Misalignment._ The verification problem is compounded by model opacity. Classical controllers expose interpretable state variables, local sensitivities, and feasibility structure; foundation models instead operate through high-dimensional latent representations whose relation to physical state is often indirect [52]. As a result, failure analysis depends heavily on empirical testing rather than formal inspection [194]. Opacity also complicates hierarchical integration. High-level semantic planners may lack explicit contracts with lower-level kinematic or feedback controllers, so a planner can produce linguistically valid but dynamically infeasible actions that downstream systems must reject or repair [4]. The barrier is therefore not only model uncertainty, but also interface mismatch between learned planning and constrained control. 

_3.6.3 Limits of Retrofitted Verification._ Retrofitting formal guarantees onto foundation-model policies remains difficult. Control Barrier Functions can enforce local safety conditions, but those guarantees are only as reliable as the state estimate and model assumptions on which they depend. Under hallucinated or shifted observations, those assumptions may no longer hold. Formal reachability analysis faces a different limitation: it does not scale easily to high-dimensional, stochastic, multimodal transformer-based policies. Weak uncertainty calibration further narrows the available safety margin. When a model cannot reliably express epistemic uncertainty, downstream systems have limited ability to reject low-confidence actions or trigger fallback behavior before error accumulates. In practice, retrofitted verification remains useful, but it covers only part of the safety problem and degrades under the same distribution shifts that challenge the policy itself. 

_3.6.4 Operational Sandboxing and Structural Implications._ Current embodied deployments often manage this gap through operational containment: reduced velocities, geofencing, supervised execution, and human teleoperation oversight. Runtime safety monitors that predict and interrupt imminent violations provide an important additional layer of protection [145]. However, these mechanisms remain largely reactive and depend on the same sensing and representation stack as the policy they supervise. They reduce operational risk, but they do not remove the underlying mismatch between generative model behavior and physically constrained control. Progress will require tighter integration of physical invariants, constraint satisfaction, and uncertainty estimation into the learning and control architecture itself [117]. 

_3.6.5 Implications._ The Safety and Verification Gap is therefore a systems-level barrier, not merely a control-theoretic one. In embodied deployment, the central question is not whether a model can 

Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies 17 

generate a plausible action, but whether the full stack can establish that the action is feasible, safe, and reliable under uncertainty before it reaches the plant. 

## **3.7 The OS and Scheduling Bottleneck** 

The **OS and Scheduling Bottleneck** arises because embodied foundation-model pipelines often execute on software stacks optimized for flexibility and throughput rather than bounded latency. Classical robotic control systems commonly rely on RTOS or bare-metal execution to enforce explicit timing guarantees, whereas FM-based embodied stacks are often built on Linux kernels, containerized environments, and Python-centered orchestration. These layers simplify integration and support heterogeneous workloads, but they also introduce timing variability across kernel scheduling, middleware execution, and user-space coordination. In closed-loop embodied systems, that variability weakens the timing guarantees on which safe control depends. 

_3.7.1 Best-Effort Scheduling and Runtime Nondeterminism._ A primary source of instability is Linux’s Completely Fair Scheduler (CFS), which is designed to maximize aggregate throughput rather than worst-case latency. Under this policy, safety-critical control loops compete with logging, networking, thermal management, and other auxiliary processes for CPU time. At control rates of roughly 100–500 Hz, even modest descheduling becomes consequential. On Jetson-class platforms, empirical studies report jitter spikes of 5–20 ms caused by kernel wake-ups, interrupt bursts, and I/O-driven preemption [147]. Once scheduling delay approaches or exceeds the control period, the problem is no longer throughput; it is a direct loss of timing integrity in the control loop. 

Python-based orchestration compounds the same issue. The Global Interpreter Lock serializes concurrent execution, and garbage collection can introduce pauses that are both unbounded and opaque to the scheduler. As a result, common coordination mechanisms in perception and control stacks, including asynchronous coroutines and ROS 2 executors, are difficult to reconcile with predictable real-time execution. Callback delays of only 5–10 ms can disrupt timestamp alignment, propagate stale observations into Vision-Language-Action policies, and increase execution drift and collision risk [154]. These effects are not isolated anomalies; they follow from the interaction between best-effort scheduling and runtime-level serialization. 

_3.7.2 Jitter Propagation Across the Stack._ Multimodal workloads amplify this problem through priority inversion and shared-resource contention. Background LiDAR decoding threads may preempt safety monitors, asynchronous data loaders may delay control execution, and ROS 2 executors may defer perception updates while servicing unrelated timers [154]. The immediate effect is bursty sensing, irregular frame timing, and transient sensor dropouts. 

The more serious issue is that latency does not remain local to the component in which it originates. CPU descheduling can delay GPU kernel dispatch, and DMA activity from one sensor can block service to another. A single LiDAR burst may therefore delay camera buffering and trigger a _jitter cascade_ across perception, planning, and actuation. Under these conditions, learned policies and predictive filters must operate on temporally inconsistent inputs rather than merely noisy ones. 

_3.7.3 Control-Theoretic Consequences._ OS-level nondeterminism undermines several assumptions used in classical control analysis. Stability arguments typically depend on bounded execution times, Zero-Order Hold discretization, and noise models that do not exhibit heavy-tailed latency behavior [62]. Best-effort scheduling violates those assumptions by introducing irregular sampling and actuation delay. In practice, the resulting failures may appear as oscillations, missed grasps, or delayed corrective action and are easily misattributed to perception or policy quality, even when the underlying cause is temporal interference in the execution stack. 

Grover et al. 

18 

_3.7.4 Implications._ The OS and Scheduling Bottleneck is therefore a systems barrier, not merely an implementation detail. Gains in model efficiency or accelerator utilization do not by themselves restore bounded-latency execution on best-effort software stacks. Embodied FM systems that require dependable physical interaction need real-time-aware runtimes, priority-sensitive scheduling, and explicit timing contracts across sensing, inference, and control. 

## **3.8 The I/O and Communication Bottleneck** 

The **I/O and Communication Bottleneck** arises because embodied foundation-model pipelines depend on multimodal data arriving with bounded delay, consistent ordering, and usable crossmodal synchronization, yet the underlying I/O stack cannot reliably preserve all three under load. Closed-loop perception and control often operate on sub-10 ms timing budgets, but those budgets are eroded by arbitration in the I/O hierarchy, network variability, and middleware overhead. As a result, failures often originate not in model inference alone, but in the data path that feeds and coordinates it. 

_3.8.1 Bus Arbitration, Network Stochasticity, and Middleware Overhead._ The first source of instability appears in the on-chip interconnect and memory subsystem. High-resolution RGB, high-rate IMU, and dense LiDAR streams compete for shared DMA engines and LPDDR bandwidth, which must also support foundation-model inference. This creates direct coupling between sensing and inference: when I/O pressure rises, arbitration delays data movement for both. On Orin-class platforms, such interference has been reported to reduce Vision-Language-Action throughput by 15–30% under background I/O load, primarily because of arbitration stalls rather than compute saturation [125]. 

In cloud-assisted and split-compute deployments, the same problem extends beyond the device. Packet loss, retransmissions, fading, and queueing introduce heavy-tailed delay, and round-trip latencies of 30–80 ms on Wi-Fi 6 can exceed the stability margins of high-frequency control. Related communication limits also affect federated and fleet learning, where aggressive compression and update throttling are often required to keep communication overhead manageable [119]. The main issue is therefore not bandwidth alone, but the inability to maintain regular timing across sensing, inference, and remote coordination. 

Middleware adds a further source of timing distortion. ROS 2 and DDS introduce serialization, copying, marshalling, and discovery overheads that consume CPU time and memory bandwidth for large tensors [115]. More importantly, DDS QoS policies reshape delivery timing through buffering, queueing, and retransmission, which can disrupt cross-modal simultaneity. Without zerocopy transport and explicit end-to-end timing contracts, middleware can invalidate the temporal assumptions required for reliable fusion and state estimation. 

_3.8.2 Cross-Layer Timing Cascades._ These timing disturbances do not remain local to the transport layer. Memory contention can delay DMA, delayed DMA can stall inference, stalled inference can misalign fusion, and middleware buffering can reorder or defer messages. Thermal throttling may further slow packet processing and callback execution. The result is degraded temporal consistency across perception, planning, and control. 

In embodied systems, that inconsistency has direct operational consequences. Obstacle updates become stale, fused state estimates lose coherence, and control actions are issued against an environment that has already changed. These failures are not purely algorithmic; they emerge from the interaction between model execution and the I/O path that supplies its inputs. 

_3.8.3 Implications._ The I/O and Communication Bottleneck is therefore a systems barrier rooted in data movement, ordering, and timing, not just in raw compute latency. Mitigating it requires 

Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies 

19 


Fig. 3. The taxonomy for Mitigation Strategies for Deployment Gauntlet on edge 

data-centric redesign, including prioritization of safety-critical traffic, near-sensor preprocessing and compression, and zero-copy communication paths for large tensor flows [149]. Without such changes, improvements in model efficiency alone will not eliminate timing failures in embodied foundation-model deployment. 

## **4 Mitigation Families for the Deployment Gauntlet** 

The literature does not respond to the Deployment Gauntlet through eight isolated solution streams. The same mitigation often relieves multiple barriers at once by reducing synchronization cost, lowering memory traffic, or improving runtime predictability. For that reason, the solution space is better understood as a small set of recurring mitigation families rather than as a one-to-one mapping from barrier to fix. We group the literature into four such families: transport-aware sensing and synchronization relaxation, hardware-aligned model and compiler co-design, memorytraffic reduction and schedulable memory use, and energy- and thermal-aware execution. Figure 3 summarizes the Mitigation strategies for deployment gauntlet 

## **4.1 Transport-Aware Sensing and Synchronization Relaxation** 

The first family acts on the data path before model inference begins. Its goal is to reduce transport overhead, relax unnecessary synchronization, and preserve temporal structure without forcing the full stack to wait on the slowest modality. Early work pursued this through zero-copy middleware transport. Iceoryx introduced shared-memory communication for fixed-size messages, while ROS 2 formalized loaned messages for middleware-managed buffer reuse [75, 75, 152]. Profiling studies show that default ROS 2 configurations can incur substantial latency relative to optimized sharedmemory pipelines, with behavior strongly shaped by DDS and executor design [87]. Executor-level refinements were therefore introduced to reduce jitter and improve predictability under real-time load [2, 154, 170]. 

Recent work extends this idea beyond fixed-size message transport. Agnocast generalizes zerocopy communication to variable-sized autonomy messages while preserving ROS 2 compatibility [75]. NITROS maintains accelerator-friendly formats through type adaptation and reduces unnecessary copies for high-resolution sensor streams [143]. At the fusion level, MMEdge reduces idle waiting through pipelined sensing and cross-modal speculative skipping [74], while AsyncVLA relaxes rigid action timing by generating control tokens asynchronously [80]. Calibration maintenance belongs in the same family: CalibRefine lowers the downstream cost of spatial misalignment through targetless online refinement [31]. 

A related line of work reduces the need for strict synchronization altogether. Lightweight fusion modules, cooperative edge-oriented VLM pipelines, and hardware-aware multimodal co-design all aim to reduce how much data must be aligned exactly at runtime [192, 203]. Uncertainty-aware fusion methods dynamically gate modality contributions instead of assuming equal reliability and perfect simultaneity [34, 110, 127]. Condition-aware pipelines similarly adapt to environmental 

Grover et al. 

20 

regime rather than enforcing expensive redundancy [17]. Training can also absorb some of the burden. TimeAlign, UniBEV, and sensor-dropout strategies explicitly expose models to temporal misalignment or partial sensing, trading modest training complexity for substantially greater runtime slack [104, 155, 180, 193]. Taken together, these methods treat sensing and synchronization as a transport-and-timing problem, not only as a perception problem. 

## **4.2 Hardware-Aligned Model and Compiler Co-Design** 

The second family addresses the mismatch between transformer-style workloads and heterogeneous edge accelerators. The central idea is to expose hardware constraints at compile time or redesign operators and models so that execution remains on the accelerator as much as possible [178]. Compiler-driven approaches are the most direct expression of this idea. MATCH extends TVM-style compilation with explicit SoC hardware models and BYOC integration to optimize placement and scheduling across heterogeneous engines [65, 69, 112]. TinyIREE similarly unifies compilation and deployment for embedded targets and reduces execution fragmentation across devices [105, 138]. The shared lesson is that heterogeneity must be visible at compile time if host fallback and crossengine synchronization are to be minimized. 

When native hardware support is missing, operator reformulation becomes the next lever. T-MAN replaces unsupported low-bit primitives on NPUs with lookup-table abstractions that preserve endto-end accelerator execution [128, 182]. Quantization methods such as LLM.int8, GPTQ, and AWQ reduce tensor movement while preserving fidelity, improving accelerator residency and reducing host-device traffic [42, 54, 101]. Memory-aware attention redesigns such as FlashAttention reduce high-bandwidth memory access through IO-aware tiling [38, 39, 66], while FlightLLM targets host-device synchronization and kernel-launch overhead during autoregressive decoding [91, 201]. 

The same design logic now appears at the architectural level. NanoVLA and TinyVLA redesign VLA pipelines for edge hardware by reducing redundant computation, sustaining accelerator residency, and separating heavyweight semantic reasoning from lightweight control [26, 153, 183]. SARA-RT replaces quadratic attention with linear-complexity alternatives to recover realtime feasibility in transformer-based robotic control [93]. Across these approaches, robust edge deployment emerges less from post-training cleanup than from joint redesign of compiler, operator, and model. 

## **4.3 Memory-Traffic Reduction and Schedulable Memory Use** 

The third family targets shared memory directly. On edge SoCs, the main problem is often not arithmetic throughput but whether LPDDR service remains predictable when foundation models, sensing, and control all compete for the same memory fabric. One response is isolation and regulation. Early work showed that shared-cache and DRAM interference can inflate tail latency even when average throughput remains acceptable [13, 174]. MemGuard-style reservation and policing mechanisms allocate DRAM budgets and throttle interfering workloads [198, 199]. Later work extends these ideas to heterogeneous CPU–GPU systems through reserved bandwidth for realtime GPU tasks, accelerator-aware isolation, per-bank regulation, LLC control, and microsecondscale policing [3, 49, 132, 156, 216]. In this line of work, memory is treated as a schedulable shared resource rather than a passive substrate. 

A complementary strategy reduces traffic volume. Low-bit quantization lowers bandwidth demand while preserving accuracy; LifeQuant and ProxQ focus specifically on maintaining quantized performance in streaming or non-stationary settings [21, 29, 102]. Structured pruning reduces both parameter count and activation traffic through hardware-aware channel and block removal [97, 103, 106]. Rotation-based methods suppress activation outliers that would otherwise 

Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies 

21 

require precision escalation, and QuaRot extends low-bit execution across weights, activations, and KV caches [10, 11, 27, 109]. 

The KV cache has become a particularly important target because it dominates long-context memory footprint. KIVI and related methods compress the cache through ultra-low-bit or coupled quantization [108, 207], while adaptive-precision schemes vary cache precision across layers or tokens to allocate bits where they are most useful [72, 150]. XQuant instead stores quantized layer inputs and rematerializes keys and values on demand, trading some on-chip computation for lower DRAM pressure [173]. Across these approaches, the picture is consistent: once sensing and inference share unified memory, real-time viability depends on both lowering traffic volume and making the remaining traffic schedulable. 

## **4.4 Energy and Thermal-Aware Execution** 

The fourth family addresses the fact that embodied deployment is governed by steady-state energy and thermal limits rather than by short-burst benchmark throughput. MAVBench makes this explicit by showing that autonomy workloads directly reduce vehicle endurance in micro aerial systems [16]. At a lower level, Horowitz and later efficient-accelerator studies show that memory access often dominates arithmetic energy, which helps explain why memory-heavy foundation models generate disproportionate thermal load even when compute is optimized [30, 73, 86]. The relevant design target is therefore not peak throughput, but _joules per decision_ and sustainable duty cycle under continuous execution [94, 100]. 

One response lowers the cost of each inference step. Distillation and compact architectures such as MobileBERT reduce deployment cost while preserving useful capacity [157]. Post-training quantization methods including ZeroQuant and SmoothQuant further reduce compute and memorytransfer energy by lowering precision without large accuracy loss [189, 196]. These methods do not remove the thermal ceiling, but they shift the steady-state operating point. 

For generative control, runtime duration matters as much as instantaneous cost. Diffusionbased policies are particularly demanding because repeated denoising accumulates heat over many steps [33]. OneDP reduces that burden by collapsing multi-step diffusion into a single-step generator [181], while LightDP prunes and restructures diffusion modules for sustained on-device execution [188]. In this regime, fewer generation steps directly improve thermal sustainability. 

Thermal-aware runtime management provides the final lever. POD TAS uses predictive thermalaware scheduling based on reduced-order thermal models to reduce peak temperature and temperature variance [44, 77]. The broader lesson across this family is that thermal feasibility is a runtime property: compression lowers cost per operation, generative redesign reduces sustained duty cycle, and predictive scheduling shapes temperature growth over time. Under continuous edge deployment, sustainable embodied performance is determined by thermal equilibrium rather than by peak capability. 

## **4.5 Online Robustness, Adaptation, and Runtime Assurance** 

Mitigations for long-horizon drift and safety failures share a common constraint: they must improve robustness without exceeding edge budgets for compute, timing, and energy. As a result, the literature does not pursue unrestricted online relearning of the full model. It instead relies on bounded corrective mechanisms that contain model mismatch before it propagates into unsafe closed-loop behavior. This family includes estimator-level drift compensation, parameter-efficient or gradient-free adaptation, control-theoretic safety filters, runtime assurance architectures, and reactive monitoring. 

One strategy localizes correction outside the full perception or control backbone. In visualinertial navigation, external neural modules estimate bias dynamics and inject corrections into 

Grover et al. 

22 

factor-graph or invariant filtering pipelines [7, 18]. In soft robotics, where sensing drift is intrinsic to the hardware, continual learning with rehearsal [90] and RNN-based observers [58] track nonlinear drift while keeping compensation decoupled from task-level policy representations. These methods are effective precisely because they restrict adaptation to a narrow interface rather than perturbing the full model. 

A second strategy constrains adaptation itself. Test-time adaptation methods suppress lowinformation gradients and stabilize streaming updates [63, 122, 123], but on edge hardware such updates remain subordinate to latency-critical inference. Parameter-efficient methods narrow the update space further through sparse backpropagation [213], lightweight bias modules [20], and bias-only transformer adaptation with well under 0 _._ 1% of parameters [200]. When backpropagation is too costly or poorly supported by the hardware stack, gradient-free methods estimate updates from parameter perturbations [121], while meta-learning shifts most of the adaptation burden offline so that deployment requires only low-dimensional coefficient updates, as in Neural Fly [124]. These approaches make adaptation feasible, but only within a deliberately limited correction range. 

The same logic appears on the safety side. Control Barrier Function wrappers and related quadratic-program filters impose forward-invariant constraints around learned actions [8], while Predictive Safety Filters and MPC-based supervisory schemes accept or replace actions according to an explicit feasibility model [168, 177]. Reachability-based intervention and RL-CBF variants similarly restrict unsafe exploration through safe sets or uncertainty-aware safety envelopes [32, 53], and SafeDiffuser extends this principle to diffusion-based planners by enforcing constraint-aware denoising [190]. These methods improve safety by constraining or correcting learned behavior externally rather than by making the generative model intrinsically safe. 

Runtime assurance architectures generalize that externalization. Simplex-style designs, SOTER, and related supervisory frameworks treat the learned policy as an advanced but uncertified controller that may be overridden by a verified baseline when safety is threatened [28, 41]. Formal verification methods such as Reluplex, Marabou, and neural reachability analysis provide stronger guarantees for small or structured networks [83, 84, 140], but they do not scale naturally to highdimensional multimodal foundation models under deployment shift. Probabilistic safety certificates, conformal wrappers, and runtime shielding partially address that limitation by combining riskbounded guarantees, runtime enforcement, and black-box monitoring [37, 78, 164, 204, 215]. In practice, these methods reduce operational risk, but they still depend on bounded correction, fallback, and supervision. 

The central lesson is consistent across this family. Long-horizon drift and safety failures are mitigated through structured correction, constrained adaptation, and runtime oversight rather than through open-ended online relearning. These mechanisms improve robustness under realistic edge constraints, but they also make clear that dependable embodied deployment still depends on keeping correction bounded, explicit, and computationally tractable. 

## **4.6 Real-Time Systems Support and Timing-Aware Communication** 

Mitigations for the OS, scheduling, I/O, and communication barriers address a different systems problem: preserving timing integrity across the execution stack. Their shared objective is to bound interference, reduce unnecessary data movement, and prevent timing disturbances from cascading across perception, planning, and control. Unlike model-centric optimizations, these methods operate on middleware, runtime, kernel, and transport layers. 

At the middleware layer, chain-aware execution and callback isolation are central. Casini et al. [24] show that default ROS 2 executors produce pessimistic response-time bounds because of priority inversion and callback interference. Later work mitigates this by separating safety-critical callbacks from background activity [194] and by scheduling end-to-end execution chains rather 

23 

Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies 

than isolated callbacks. PiCAS is a representative example: it uses priority-driven, chain-aware scheduling to reduce perception-to-control latency substantially on embedded platforms [35]. These methods improve timing predictability, but they remain dependent on lower-level scheduling and resource isolation. 

Kernel-level real-time support addresses a second part of the same problem. PREEMPT_RT substantially reduces CPU wake-up latency and improves interrupt handling under load [67], which is valuable for classical control and for the CPU-resident orchestration surrounding learned policies. Heterogeneous embodied systems, however, also depend on GPU kernels, DMA engines, and shared memory fabrics that the CPU scheduler governs only indirectly. OS-level real-time support therefore improves timing behavior but does not by itself guarantee end-to-end stability. 

Runtime restructuring provides a more aggressive response. Systems such as Dora remove critical execution from Python and place it in compiled dataflow runtimes with zero-copy shared memory and explicit execution graphs, reducing latency relative to conventional ROS 2 Python pipelines [12]. The broader lesson is that runtime architecture matters: dataflow-style execution, reduced interpreter overhead, and explicit dependency graphs are often more compatible with predictable timing than general-purpose task orchestration. 

Transport and communication optimizations tackle the same issue from the data path. On unified-memory platforms, bandwidth regulation mechanisms such as MemGuard, BWLOCK, and later dynamic or DSU-level policies protect safety-critical traffic by throttling interferers and reserving DRAM service under contention [3, 130, 198, 199]. Zero-copy shared-memory transport such as Iceoryx reduces serialization and large-payload copying overhead [129], while Hazcat and FPGA-assisted DDS reduce host-side transport cost by unifying memory handling or offloading communication across heterogeneous devices [14, 116]. These methods do not remove timing variability, but they reduce how much of it is injected into the critical path. 

When execution spans cloud and edge, communication-aware partitioning becomes necessary. Dynamic split-compute frameworks such as Neurosurgeon and SPINN adapt the partition point to current channel conditions [81, 169]. BottleNet, Elf, and related selective-transmission methods further reduce bandwidth demand through representation compression or sparse token transfer [47, 95, 208]. These approaches improve survivability under communication variability, but they do so by trading model fidelity, freshness, or cross-modal coherence for lower transport load. 

Across this family, the conclusion is straightforward: timing reliability in embodied FM deployment is not recovered by faster models alone. It depends on coordinated support across middleware scheduling, kernel preemption, runtime design, bandwidth isolation, and communication-aware execution. The objective is not perfect determinism under all conditions, but an execution stack in which timing disruptions are bounded, localized, and less likely to cascade into unsafe control behavior. Table 5 summarizes the mitigation families that address the long-horizon robustness, safety-assurance, timing, and communication barriers in embodied foundation model deployment. 

Grover et al. 

24 

Table 5. Mitigation families for the Deployment Gauntlet: representative strategies for improving embodied foundation model deployment at the edge. 

|**Mitigation**<br>**Family**|**Core Strategy**|**Deployment Bene-**<br>**fit**|**Representative Techniques / Evidence**|
|---|---|---|---|
|Transport-<br>Aware Sensing<br>and<br>Syn-<br>chronization<br>Relaxation|Reduce<br>transport<br>overhead, relax rigid<br>synchronization,<br>and preserve usable<br>temporal<br>structure<br>before<br>inference<br>begins.|Lower tail latency<br>and<br>jitter,<br>reduce<br>copy overhead, and<br>improve multimodal<br>alignment<br>without<br>forcing the stack to<br>wait on the slowest<br>modality.|Zero-copy middleware transport and loaned buffers [75,75,152], executor<br>and synchronization refinements [2, 87, 154, 170], variable-sized zero-<br>copy and accelerator-native transport [75,143], pipelined and asynchro-<br>nous sensing/action generation [74,80], calibration maintenance [31], and<br>training-time robustness to misalignment or missing modalities [104,155,<br>180,193].|
|Hardware-<br>Aligned Model<br>and<br>Compiler<br>Co-Design|Expose<br>hardware<br>constraints<br>at<br>compile time and re-<br>design operators or<br>models to reduce fall-<br>back, fragmentation,<br>and<br>unsupported<br>executionpaths.|Higher<br>accelerator<br>residency,<br>fewer<br>host fallbacks, lower<br>synchronization<br>overhead, and better<br>real-time feasibility<br>on<br>heterogeneous<br>edge hardware.|SoC-aware compilation and heterogeneous placement [65,69,105,112,138,<br>178], operator reformulation for end-to-end accelerator execution [128,<br>182], traffic-reducing quantization and IO-aware attention [38,39,42,54,<br>66,101], host-device synchronization reduction [91,201], and hardware-<br>aligned model redesign [26,93,153,183].|
|Memory-<br>Traffic<br>Re-<br>duction<br>and<br>Schedulable<br>Memory Use|Treat shared mem-<br>ory as a schedula-<br>ble resource and re-<br>duce traffic volume<br>so sensing, inference,<br>and control can coex-<br>ist without excessive<br>jitter.|More<br>predictable<br>LPDDR<br>service,<br>lower<br>tail<br>latency,<br>fewer<br>stalls,<br>and<br>improved sustained<br>performance<br>under<br>unified-memory<br>contention.|DRAM isolation and bandwidth policing [3,13,49,132,156,174,198,199,<br>216], streaming-stable quantization and pruning [21,29,97,102,103,106],<br>outlier suppression and uniform low-bit execution [10,11,27,109], and<br>KV-cache redesign that trades compute for lower LPDDR pressure [72,<br>108,150,173,207].|
|Energy-<br>and<br>Thermal-<br>Aware<br>Execu-<br>tion|Optimize for sustain-<br>able duty cycle and<br>steady-state thermal<br>feasibility<br>rather<br>than<br>short-burst<br>benchmark through-<br>put.|Lower<br>joules<br>per<br>decision,<br>better<br>endurance, reduced<br>throttling, and more<br>stable long-horizon<br>real-time behavior.|Endurance-aware deployment evidence [16], energy-per-inference reduc-<br>tion through distillation and quantization [30,73,86,157,189,196], duty-<br>cycle reduction for generative control [33,181,188], and predictive thermal-<br>aware runtime management [44,77,94,100].|
|Online<br>Ro-<br>bustness,<br>Adaptation,<br>and<br>Runtime<br>Assurance|Bound model mis-<br>match<br>through<br>localized correction,<br>constrained adapta-<br>tion, external safety<br>filters, and runtime<br>supervision<br>rather<br>than<br>unrestricted<br>online relearning.|Improves<br>long-<br>horizon<br>robustness<br>and reduces unsafe<br>behavior under real-<br>istic edge constraints<br>while keeping correc-<br>tion computationally<br>tractable.|Estimator-level drift compensation through neural bias prediction and<br>lightweight observers [7,18,58,90], constrained test-time adaptation and<br>streaming-stable updates [63, 122, 123], sparse and parameter-efficient<br>adaptation [20,200,213], gradient-free and meta-learned adaptation [121,<br>124], control-theoretic safety wrappers and predictive safety filters [8,<br>32, 53, 177, 190], runtime assurance architectures [28, 41, 168], formal<br>verification and uncertainty-aware certificates [83,84,140,164,204], and<br>runtime shielding and black-box monitoring [37,78,215].|
|Real-Time<br>Systems<br>Sup-<br>port<br>and<br>Timing-Aware<br>Communica-<br>tion|Bound interference<br>across middleware,<br>runtime,<br>kernel,<br>memory, and trans-<br>port layers so timing<br>disturbances do not<br>cascade across per-<br>ception,<br>planning,<br>and control.|Improves timing pre-<br>dictability,<br>reduces<br>transport-induced<br>jitter, and limits the<br>spread of scheduling<br>and communication<br>variability<br>through<br>the execution stack.|Middleware callback isolation and chain-aware scheduling [24,35,194],<br>kernel-level real-time support [67], compiled dataflow runtimes and zero-<br>copy execution graphs [12], DRAM bandwidth regulation and arbitration<br>control [3,130,198,199], zero-copy and heterogeneous I/O transport opti-<br>mization [14,116,129], and communication-aware cloud–edge partitioning<br>with compression or selective transmission [47,81,95,169,208].|


## **5 Future Directions: Beyond the Deployment Gauntlet** 

The Deployment Gauntlet suggests that incremental gains in compression, quantization, or model scaling often improve _average_ performance more than _worst-case_ deployment behavior under SWaPconstrained, closed-loop execution. Many of the most consequential failures-including memory contention, missed deadlines, thermal excursions, and safety-envelope violations-arise from cloudinference assumptions such as best-effort scheduling, batch-oriented memory traffic, and weak timing contracts. Figure 4 summarizes a set of representative architectural responses to these constraints. 

Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies 

25 

## **Representative architectural directions:** 

- **Event-driven sensing:** Replace dense frame pipelines with event-structured inputs to reduce redundant compute and bandwidth, improve temporal alignment, and tighten endto-end latency budgets [6, 211]. 

- **Memory-centric and near-sensor compute:** Reorganize dataflow to reduce tensor movement through near-sensor preprocessing and PIM-style primitives, mitigating the unifiedmemory contention that often dominates edge latency and energy [185] [1]. 

- **World-model-centric autonomy:** Use predictive state as a synchronization substrate under delay, occlusion, and sensor disagreement, enabling temporally grounded planning rather than purely reactive control [51, 186]. 

- **Bifurcated cognition (System 1 / System 2):** Separate high-rate control authority from lower-rate semantic reasoning so that deliberative stalls do not propagate directly into actuation hazards [4, 52]. 

- **Real-time safety enforcement:** Combine lightweight monitoring with bounded-overhead runtime constraint enforcement, such as CBF-style reflex layers, that remain effective under missed deadlines and resource pressure [52, 171]. 

- **Collaborative embodiment and fleet learning:** Treat robustness partly as a fleet-level property by amortizing rare events and distribution shift across deployments through federated, split, or distilled update mechanisms under limited connectivity [187]. 

## **5.1 Evaluation Trends: From Accuracy to Operational Validity** 

These architectural directions imply a corresponding shift in evaluation. Accuracy and average latency remain necessary, but they are weak predictors of real deployment outcomes when the execution stack is constrained by timing, memory, and thermal pressure. Future benchmarks should therefore report at least three additional properties: (i) **temporal coherence** , including state freshness and synchronization under load; (ii) **bounded failure and recoverability** , including graceful degradation within safety envelopes; and (iii) **resource stability** , including sensitivity to bandwidth pressure, I/O contention, thermal throttling, and scheduling jitter. Stress-test protocols that inject jitter, bus pressure, packet loss, and sensor dropout would make evaluation more operationally meaningful by measuring whether systems remain coherent, bounded, and safe under realistic constraints. 

## **6 Conclusion** 

Deploying foundation models on edge embodied platforms is a systems problem, not simply a problem of compression or accelerator efficiency. Reliable embodied performance depends on the interaction of sensing, computation, memory, timing, power, and safety under closed-loop execution. We organized these recurring constraints through the Deployment Gauntlet, a systems taxonomy that explains why gains in average-case throughput do not necessarily translate into dependable deployment. Across the literature, quantization, pruning, and related optimizations improve deployability, but they do not, on current evidence, resolve the worst-case failures associated with memory contention, timing variability, thermal instability, and limited safety assurance. 

A central implication of this survey is that embodied deployment increasingly favors architectural decomposition over monolithic end-to-end execution. Separating high-rate control from lower-rate semantic reasoning is one promising response to the tension between control-loop determinism and deliberative inference. More broadly, reducing data movement is often as important as reducing arithmetic cost. This makes transport-aware sensing, memory-centric execution, and near-sensor 

Grover et al. 

26 


Fig. 4. Architecture trends for future Embodied Foundation Models: Data volume is minimized via Neuromorphic and event sensing (A), and near sensor compute mechanism (B). A central predictive world model stabilizes perception (C) while cognition is separated into fast reflexes and slow reasoning (D). The rigorous safety policy(E) enforces constraints before actuation. And the Fleet learning (F) extends the feasible complexity. 

or in-memory processing especially relevant for future embodied systems operating under strict SWaP constraints. 

The broader lesson is that robust embodied intelligence will depend less on transferring cloudoriented model assumptions to the edge and more on explicit co-design across sensing, memory hierarchy, runtime scheduling, communication, and model architecture. The semantic capabilities of foundation models remain valuable, but realizing them in physical systems requires stacks designed around edge constraints rather than adapted to them only after training. In that sense, the future of embodied foundation models lies not simply in smaller models on smaller devices, but in systems whose learning objectives, execution substrate, and safety requirements are aligned from the outset. 

## **References** 

- [1] Romina Aalishah, Mozhgan Navardi, and Tinoosh Mohsenin. 2025. EdgeNavMamba: Mamba Optimized Object Detection for Energy Efficient Edge Devices. _arXiv preprint arXiv:2510.14946_ (2025). 

- [2] Hazem Abaza, Debayan Roy, Bohdan Trach, Wanli Chang, Selma Saidi, Antonios Motakis, Wei Ren, and Yutao Liu. 2024. Managing End-to-End Timing Jitters in ROS2 Computation Chains. In _International Conference on Real-Time Networks and Systems (RTNS)_ . 

- [3] Homa Aghilinasab, Waqar Ali, Heechul Yun, and Rodolfo Pellizzoni. 2020. Dynamic memory bandwidth allocation for real-time GPU-based SoC platforms. _IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems_ 39, 11 (2020), 3348–3360. 

- [4] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, et al. 2022. Do as i can, not as i say: Grounding language in robotic affordances. _arXiv preprint arXiv:2204.01691_ . 

- [5] Ghattas Akkad, Ali Mansour, and Elie Inaty. 2023. Embedded deep learning accelerators: A survey on recent advances. _IEEE Transactions on Artificial Intelligence_ 5, 5 (2023), 1954–1972. 

- [6] Asmer Hamid Ali, Mozhgan Navardi, and Tinoosh Mohsenin. 2024. Energy-Aware FPGA Implementation of Spiking Neural Network with LIF Neurons. _arXiv preprint arXiv:2411.01628_ (2024). 

- [7] Abdullah Altawaitan, Jason Stanley, Sambaran Ghosal, Thai Duong, and Nikolay Atanasov. 2025. Learned IMU Bias Prediction for Invariant Visual Inertial Odometry. _arXiv preprint arXiv:2505.06748_ (2025). 

27 

Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies 

- [8] Aaron D Ames, Samuel Coogan, Magnus Egerstedt, Gennaro Notomista, Koushil Sreenath, and Paulo Tabuada. 2019. Control barrier functions: Theory and applications. In _2019 18th European control conference (ECC)_ . Ieee, 3420–3431. 

- [9] Dario Amodei, Chris Olah, Jacob Steinhardt, Paul Christiano, John Schulman, and Dan Mané. 2016. Concrete problems in AI safety. _arXiv preprint arXiv:1606.06565_ (2016). 

- [10] Saleh Ashkboos, Maximilian L Croci, Marcelo Gennari do Nascimento, Torsten Hoefler, and James Hensman. 2024. Slicegpt: Compress large language models by deleting rows and columns. _arXiv preprint arXiv:2401.15024_ (2024). 

- [11] Saleh Ashkboos, Amirkeivan Mohtashami, Maximilian L Croci, Bo Li, Pashmina Cameron, Martin Jaggi, Dan Alistarh, Torsten Hoefler, and James Hensman. 2024. Quarot: Outlier-free 4-bit inference in rotated llms. 100213–100240 pages. 

- [12] Mohammad Abbas Baig, Liang Han, DongLei Yang, and Danaish. 2026. A cloud robotics architecture for greenhouse strawberry harvesting with single-pass data collection. 14 pages. 

- [13] Michael Bechtel and Heechul Yun. 2024. Analysis and mitigation of shared resource contention on heterogeneous multicore: An industrial case study. _IEEE Trans. Comput._ 73, 7 (2024), 1753–1766. 

- [14] Oren Bell, Chris Gill, and Xuan Zhang. 2023. Hardware acceleration with zero-copy memory management for heterogeneous computing. In _2023 IEEE 29th International Conference on Embedded and Real-Time Computing Systems and Applications (RTCSA)_ . IEEE, 28–37. 

- [15] Rishi Bommasani, Drew A Hudson, Ehsan Adeli, Russ Altman, Simran Arora, Sydney von Arx, Michael S Bernstein, Jeannette Bohg, Antoine Bosselut, Emma Brunskill, et al. 2021. On the opportunities and risks of foundation models. _arXiv preprint arXiv:2108.07258_ (2021). 

- [16] Behzad Boroujerdian, Hasan Genc, Srivatsan Krishnan, Wenzhi Cui, Aleksandra Faust, and Vijay Reddi. 2018. Mavbench: Micro aerial vehicle benchmarking. In _2018 51st annual IEEE/ACM international symposium on microarchitecture (MICRO)_ . IEEE, 894–907. 

- [17] Tim Brödermann, Christos Sakaridis, Yuqian Fu, and Luc Van Gool. 2025. Cafuser: Condition-aware multimodal fusion for robust semantic perception of driving scenes. 

- [18] Russell Buchanan, Varun Agrawal, Marco Camurri, Frank Dellaert, and Maurice Fallon. 2022. Deep imu bias inference for robust visual-inertial odometry with factor graphs. _IEEE Robotics and Automation Letters_ 8, 1 (2022), 41–48. 

- [19] Cesar Cadena, Luca Carlone, Henry Carrillo, Yasir Latif, Davide Scaramuzza, José Neira, Ian Reid, and John J Leonard. 2016. Past, present, and future of simultaneous localization and mapping: Toward the robust-perception age. _IEEE Transactions on Robotics_ 32, 6 (2016), 1309–1332. 

- [20] Han Cai, Chuang Gan, Ligeng Zhu, and Song Han. 2020. Tinytl: Reduce memory, not parameters for efficient on-device learning. _Advances in Neural Information Processing Systems_ 33, 11285–11297. 

- [21] Yaohui Cai, Zhewei Yao, Zhen Dong, Amir Gholami, Michael W Mahoney, and Kurt Keutzer. 2020. Zeroq: A novel zero shot quantization framework. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . 13169–13178. 

- [22] Keyan Cao, Yefan Liu, Gongjie Meng, and Qimeng Sun. 2020. An overview on edge computing research. _IEEE access_ 8 (2020), 85714–85728. 

- [23] Nicola Capodieci, Roberto Cavicchioli, Marko Bertogna, and Aingara Paramakuru. 2018. Deadline-based scheduling for GPU with preemption support. In _IEEE Real-Time Systems Symposium (RTSS)_ . 119–130. 

- [24] Daniel Casini, Tobias Blaß, Ingo Lütkebohle, and Björn Brandenburg. 2019. Response-time analysis of ROS 2 processing chains under reservation-based scheduling. In _31st Euromicro Conference on Real-Time Systems_ . Schloss Dagstuhl, 1–23. 

- [25] Adwait Chandorkar, Hasan Tercan, and Tobias Meisen. 2025. Rethinking Backbone Design for Lightweight 3D Object Detection in LiDAR. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . 1698–1706. 

- [26] Jiahong Chen, Jing Wang, Long Chen, Chuwei Cai, and Jinghui Lu. 2025. NanoVLA: Routing Decoupled VisionLanguage Understanding for Nano-sized Generalist Robotic Policies. _arXiv preprint arXiv:2510.25122_ (2025). 

- [27] Mengzhao Chen, Wenqi Shao, Peng Xu, Jiahao Wang, Peng Gao, Kaipeng Zhang, and Ping Luo. 2025. Efficientqat: Efficient quantization-aware training for large language models. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . 10081–10100. 

- [28] Shengduo Chen, Yaowei Sun, Dachuan Li, Qiang Wang, Qi Hao, and Joseph Sifakis. 2022. Runtime safety assurance for learning-enabled control of autonomous driving vehicles. In _2022 International Conference on Robotics and Automation (ICRA)_ . IEEE, 8978–8984. 

- [29] Ting-An Chen, De-Nian Yang, and Ming-Syan Chen. 2023. Overcoming Forgetting Catastrophe in Quantization-Aware Training. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ . 17358–17367. 

- [30] Yu-Hsin Chen, Tushar Krishna, Joel S Emer, and Vivienne Sze. 2016. Eyeriss: An energy-efficient reconfigurable accelerator for deep convolutional neural networks. _IEEE journal of solid-state circuits_ 52, 1 (2016), 127–138. 

- [31] Lei Cheng, Lihao Guo, Tianya Zhang, Tam Bang, Austin Harris, Mustafa Hajij, Mina Sartipi, and Siyang Cao. 2025. CalibRefine: Deep Learning-Based Online Automatic Targetless LiDAR–Camera Calibration with Iterative and Attention-Driven Post-Refinement. 

Grover et al. 

28 

- [32] Richard Cheng, Gábor Orosz, Richard M Murray, and Joel W Burdick. 2019. End-to-end safe reinforcement learning through barrier functions for safety-critical continuous control tasks. In _Proceedings of the AAAI conference on artificial intelligence_ , Vol. 33. 3387–3395. 

- [33] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. 2025. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ 44, 10-11 (2025), 1684–1704. 

- [34] Minkyoung Cho, Yulong Cao, Jiachen Sun, Qingzhao Zhang, Marco Pavone, Jeong Joon Park, Heng Yang, and Z Morley Mao. 2024. Cocoon: Robust multi-modal perception with uncertainty-aware sensor fusion. 

- [35] Hyunjong Choi, Yecheng Xiang, and Hyoseung Kim. 2021. PiCAS: New design of priority-driven chain-aware scheduling for ROS2. In _2021 IEEE 27th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ . IEEE, 251–263. 

- [36] Christopher Choy, JunYoung Gwak, and Silvio Savarese. 2019. 4d spatio-temporal convnets: Minkowski convolutional neural networks. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . 3075–3084. 

- [37] Davide Corsi, Guy Amir, Andoni Rodríguez, César Sánchez, Guy Katz, and Roy Fox. 2024. Verification-guided shielding for deep reinforcement learning. _arXiv preprint arXiv:2406.06507_ (2024). 

- [38] Tri Dao. 2023. Flashattention-2: Faster attention with better parallelism and work partitioning. _arXiv preprint arXiv:2307.08691_ (2023). 

- [39] Tri Dao, Dan Fu, Stefano Ermon, Atri Rudra, and Christopher Ré. 2022. Flashattention: Fast and memory-efficient exact attention with io-awareness. 16344–16359 pages. 

- [40] Allison McCarn Deiana, Nhan Tran, Joshua Agar, Michaela Blott, Giuseppe Di Guglielmo, Javier Duarte, Philip Harris, Scott Hauck, Mia Liu, Mark S Neubauer, et al. 2022. Applications and techniques for fast machine learning in science. _Frontiers in big Data_ 5 (2022), 787421. 

- [41] Ankush Desai, Shromona Ghosh, Sanjit A Seshia, Natarajan Shankar, and Ashish Tiwari. 2019. SOTER: a runtime assurance framework for programming safe robotics systems. In _2019 49th Annual IEEE/IFIP International Conference on Dependable Systems and Networks (DSN)_ . IEEE, 138–150. 

- [42] Tim Dettmers, Mike Lewis, Younes Belkada, and Luke Zettlemoyer. 2022. Gpt3. int8 (): 8-bit matrix multiplication for transformers at scale. 30318–30332 pages. 

- [43] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, et al. 2020. An image is worth 16x16 words: Transformers for image recognition at scale. _arXiv preprint arXiv:2010.11929_ (2020). 

- [44] Anthony Dowling, Lin Jiang, Ming-Cheng Cheng, and Yu Liu. 2025. Regulating CPU temperature with thermal-aware scheduling using a reduced order learning thermal model. 107687 pages. 

- [45] Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, et al. 2023. Palm-e: An embodied multimodal language model. (2023). 

- [46] Jiafei Duan, Samson Yu, Hui Li Tan, Hongyuan Zhu, and Cheston Tan. 2022. A survey of embodied ai: From simulators to research tasks. _IEEE Transactions on Emerging Topics in Computational Intelligence_ 6, 2 (2022), 230–244. 

- [47] Amir Erfan Eshratifar, Amirhossein Esmaili, and Massoud Pedram. 2019. Bottlenet: A deep learning architecture for intelligent mobile cloud computing services. In _2019 IEEE/ACM International Symposium on Low Power Electronics and Design (ISLPED)_ . IEEE, 1–6. 

- [48] Hadi Esmaeilzadeh, Emily Blem, Renée St Amant Karthikeyan Sankaralingam, and Doug Burger. [n. d.]. RETROSPECTIVE: Dark Silicon and the End of Multicore Scaling. ([n. d.]). 

- [49] Juan Fang, Sheng Lin, and Yiming Yan. 2024. RT-DBR: Dynamic Bandwidth Reservation for Real-Time Application on CPU-GPU Heterogeneous SoC. In _Proceedings of the 2024 8th International Conference on Computer Science and Artificial Intelligence_ . 594–600. 

- [50] Di Feng, Christian Haase-Schütz, Lars Rosenbaum, Heinz Hertlein, Claudius Glaeser, Fabian Timm, Werner Wiesbeck, and Klaus Dietmayer. 2020. Deep multi-modal object detection and semantic segmentation for autonomous driving: Datasets, methods, and challenges. _IEEE Transactions on Intelligent Transportation Systems_ 22, 3 (2020), 1341–1360. 

- [51] Tuo Feng, Wenguan Wang, and Yi Yang. 2025. A survey of world models for autonomous driving. _arXiv preprint arXiv:2501.11260_ (2025). 

- [52] Roya Firoozi, Johnathan Tucker, Stephen Tian, Anirudha Majumdar, Jiankai Sun, Weiyu Liu, Yuke Zhu, Shuran Song, Ashish Kapoor, Karol Hausman, et al. 2025. Foundation models in robotics: Applications, challenges, and the future. _The International Journal of Robotics Research_ 44, 5 (2025), 701–739. 

- [53] Jaime F Fisac, Anayo K Akametalu, Melanie N Zeilinger, Shahab Kaynama, Jeremy Gillula, and Claire J Tomlin. 2018. A general safety framework for learning-based control in uncertain robotic systems. _IEEE Trans. Automat. Control_ 64, 7 (2018), 2737–2752. 

- [54] Elias Frantar, Saleh Ashkboos, Torsten Hoefler, and Dan Alistarh. 2022. Gptq: Accurate post-training quantization for generative pre-trained transformers. 

Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies 

29 

- [55] Guillermo Gallego, Tobi Delbrück, Garrick Orchard, Chiara Bartolozzi, Brian Taba, Andrea Censi, Stefan Leutenegger, Andrew J Davison, Jörg Conradt, Kostas Daniilidis, et al. 2020. Event-based vision: A survey. _IEEE transactions on pattern analysis and machine intelligence_ 44, 1 (2020), 154–180. 

- [56] Yingjie Gao, Yanan Zhang, Zhi Cai, and Di Huang. 2025. Test-Time Adaptive Object Detection with Foundation Model. _arXiv preprint arXiv:2510.25175_ (2025). 

- [57] Daniel Gehrig, Mathias Gehrig, Javier Hidalgo-Carrió, and Davide Scaramuzza. 2020. Video to events: Recycling video datasets for event cameras. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . 3586–3595. 

- [58] Thomas George Thuruthel, Paul Gardner, and Fumiya Iida. 2022. Closing the control loop with time-variant embedded soft sensors and recurrent neural networks. _Soft Robotics_ 9, 6 (2022), 1167–1176. 

- [59] Amir Gholami, Sehoon Kim, Zhen Dong, Zhewei Yao, Michael W Mahoney, and Kurt Keutzer. 2022. A survey of quantization methods for efficient neural network inference. In _Low-power computer vision_ . Chapman and Hall/CRC, 291–326. 

- [60] Sukhpal Singh Gill, Muhammed Golec, Jianmin Hu, Minxian Xu, Junhui Du, Huaming Wu, Guneet Kaur Walia, Subramaniam Subramanian Murugesan, Babar Ali, Mohit Kumar, et al. 2025. Edge AI: A taxonomy, systematic review and future directions. _Cluster Computing_ 28, 1 (2025), 18. 

- [61] Rohit Girdhar, Alaaeldin El-Nouby, Zhuang Liu, Mannat Singh, Kalyan Vasudev Alwala, Armand Joulin, and Ishan Misra. 2023. Imagebind: One embedding space to bind them all. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . 15180–15190. 

- [62] Carla P Gomes, Bart Selman, Nuno Crato, and Henry Kautz. 2000. Heavy-tailed phenomena in satisfiability and constraint satisfaction problems. _Journal of automated reasoning_ 24, 1 (2000), 67–100. 

- [63] Taesik Gong, Jongheon Jeong, Taewon Kim, Yewon Kim, Jinwoo Shin, and Sung-Ju Lee. 2022. Note: Robust continual test-time adaptation against temporal correlation. _Advances in Neural Information Processing Systems_ 35, 27253–27266. 

- [64] Ankit Goyal, Hugo Hadfield, Xuning Yang, Valts Blukis, and Fabio Ramos. 2025. Vla-0: Building state-of-the-art vlas with zero modification. _arXiv preprint arXiv:2510.13054_ (2025). 

- [65] Warren J Gross, Brett H Meyer, and Arash Ardakani. 2020. Hardware-aware design for edge intelligence. _IEEE Open Journal of Circuits and Systems_ 2 (2020), 113–127. 

- [66] Ahan Gupta, Hao Guo, Yueming Yuan, Yanqi Zhou, and Charith Mendis. 2023. FLuRKA: Fast and accurate unified low-rank & kernel attention. _arXiv preprint arXiv:2306.15799_ (2023). 

- [67] Carlos San Vicente Gutiérrez, Lander Usategui San Juan, Irati Zamalloa Ugarte, and Víctor Mayoral Vilches. 2018. Real-time Linux communications: an evaluation of the Linux communication stack for real-time robotic applications. _arXiv preprint arXiv:1808.10821_ (2018). 

- [68] David Ha and Jürgen Schmidhuber. 2018. World models. _arXiv preprint arXiv:1803.10122_ 2, 3 (2018). 

- [69] Mohamed Amine Hamdi, Francesco Daghero, Giuseppe Maria Sarda, Josse Van Delm, Arne Symons, Luca Benini, Marian Verhelst, Daniele Jahier Pagliari, and Alessio Burrello. 2025. MATCH: model-aware TVM-based compilation for heterogeneous edge devices. 

- [70] Zhijian He, Xueli Fan, Yun Peng, Zhaoyan Shen, Jianhao Jiao, and Ming Liu. 2022. Empointmovseg: Sparse tensor-based moving-object segmentation in 3-d lidar point clouds for autonomous driving-embedded system. _IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems_ 42, 1 (2022), 41–53. 

- [71] Sara Hooker. 2021. The hardware lottery. _Commun. ACM_ 64, 12 (2021), 58–65. 

- [72] Coleman Hooper, Sehoon Kim, Hiva Mohammadzadeh, Michael W Mahoney, Yakun S Shao, Kurt Keutzer, and Amir Gholami. 2024. Kvquant: Towards 10 million context length llm inference with kv cache quantization. 1270– 1303 pages. 

- [73] Mark Horowitz. 2014. 1.1 computing’s energy problem (and what we can do about it). In _2014 IEEE international solid-state circuits conference digest of technical papers (ISSCC)_ . IEEE, 10–14. 

- [74] Runxi Huang, Mingxuan Yu, Mingyu Tsoi, and Xiaomin Ouyang. 2025. MMEdge: Accelerating On-device Multimodal Inference via Pipelined Sensing and Encoding. 

- [75] Takahiro Ishikawa-Aso and Shinpei Kato. 2025. ROS 2 Agnocast: Supporting unsized message types for true zero-copy publish/subscribe IPC. 01–10 pages. 

- [76] Andrei Ivanov, Nikoli Dryden, Tal Ben-Nun, Shigang Li, and Torsten Hoefler. 2021. Data movement is all you need: A case study on optimizing transformers. _Proceedings of Machine Learning and Systems_ 3 (2021), 711–732. 

- [77] Manu Nicholas Jacob. 2025. ThermML@ Edge: Thermally-Robust Inference on Commodity SBCs via Precision, Threading, and Policy Design. _Authorea Preprints_ (2025). 

- [78] Nils Jansen, Bettina Könighofer, Sebastian Junges, Alex Serban, and Roderick Bloem. 2020. Safe reinforcement learning using probabilistic shields. In _31st International Conference on Concurrency Theory (CONCUR 2020)_ . Schloss Dagstuhl–Leibniz-Zentrum für Informatik, 3–1. 

Grover et al. 

30 

- [79] Erling R Jellum, Torleiv H Bryne, Tor Arne Johansen, and Milica Orlandić. 2022. The syncline model-analyzing the impact of time synchronization in sensor fusion. In _2022 IEEE Conference on Control Technology and Applications (CCTA)_ . IEEE, 1446–1453. 

- [80] Yuhua Jiang, Shuang Cheng, Yan Ding, Feifei Gao, and Biqing Qi. 2025. AsyncVLA: Asynchronous Flow Matching for Vision Language Action Models. arXiv:2511.14148 [cs.RO] 

- [81] Yiping Kang, Johann Hauswald, Cao Gao, Austin Rovinski, Trevor Mudge, Jason Mars, and Lingjia Tang. 2017. Neurosurgeon: Collaborative intelligence between the cloud and mobile edge. _ACM SIGARCH Computer Architecture News_ 45, 1 (2017), 615–629. 

- [82] Leela S Karumbunathan. 2022. Nvidia jetson agx orin series. _A Giant Leap Forward for Robotics and Edge AI Applications. Technical Brief_ (2022). 

- [83] Guy Katz, Clark Barrett, David L Dill, Kyle Julian, and Mykel J Kochenderfer. 2017. Reluplex: An efficient SMT solver for verifying deep neural networks. In _International conference on computer aided verification_ . Springer, 97–117. 

- [84] Guy Katz, Derek A Huang, Duligur Ibeling, Kyle Julian, Christopher Lazarus, Rachel Lim, Parth Shah, Shantanu Thakoor, Haoze Wu, Aleksandar Zeljić, et al. 2019. The marabou framework for verification and analysis of deep neural networks. In _International conference on computer aided verification_ . Springer, 443–452. 

- [85] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. 2024. OpenVLA: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ (2024). 

- [86] Skanda Koppula, Lois Orosa, A Giray Yağlıkçı, Roknoddin Azizi, Taha Shahroodi, Konstantinos Kanellopoulos, and Onur Mutlu. 2019. EDEN: Enabling energy-efficient, high-performance deep neural network inference using approximate DRAM. In _Proceedings of the 52nd Annual IEEE/ACM International Symposium on Microarchitecture_ . 166–181. 

- [87] Tobias Kronauer, Joshwa Pohlmann, Maximilian Matthé, Till Smejkal, and Gerhard Fettweis. 2021. Latency analysis of ros2 multi-node systems. In _2021 IEEE international conference on multisensor fusion and integration for intelligent systems (MFI)_ . IEEE, 1–7. 

- [88] Uday Kulkarni, Abhishek S Hosamani, Abhishek S Masur, Shashank Hegde, Ganesh R Vernekar, and K Siri Chandana. 2022. A survey on quantization methods for optimization of deep neural networks. In _2022 international conference on automation, computing and renewable systems (ICACRS)_ . IEEE, 827–834. 

- [89] Ashish Kumar, Zipeng Fu, Deepak Pathak, and Jitendra Malik. 2021. Rma: Rapid motor adaptation for legged robots. _arXiv preprint arXiv:2107.04034_ (2021). 

- [90] Nilay Kushawaha, Radan Pathan, Niccolò Pagliarani, Matteo Cianchetti, and Egidio Falotico. 2025. Adaptive Drift Compensation for Soft Sensorized Finger Using Continual Learning. In _2025 IEEE 8th International Conference on Soft Robotics (RoboSoft)_ . IEEE, 1–6. 

- [91] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gonzalez, Hao Zhang, and Ion Stoica. 2023. Efficient memory management for large language model serving with pagedattention. 611–626 pages. 

- [92] Alex H Lang, Sourabh Vora, Holger Caesar, Lubing Zhou, Jiong Yang, and Oscar Beijbom. 2019. Pointpillars: Fast encoders for object detection from point clouds. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . 12697–12705. 

- [93] Isabel Leal, Krzysztof Choromanski, Deepali Jain, Avinava Dubey, Jake Varley, Michael Ryoo, Yao Lu, Frederick Liu, Vikas Sindhwani, Quan Vuong, et al. 2024. Sara-rt: Scaling up robotics transformers with self-adaptive robust attention. 6920–6927 pages. 

- [94] Youngmoon Lee. 2021. Thermal-aware design and management of embedded real-time systems. In _2021 Design, Automation & Test in Europe Conference & Exhibition (DATE)_ . IEEE, 1252–1255. 

- [95] Peizheng Li and Adnan Aijaz. 2025. Task-oriented connectivity for networked robotics with generative ai and semantic communications. 6 pages. 

- [96] Ruoxiang Li, Nan Guan, Xu Jiang, Zhishan Guo, Zheng Dong, and Mingsong Lv. 2022. Worst-case time disparity analysis of message synchronization in ROS. In _2022 IEEE Real-Time Systems Symposium (RTSS)_ . IEEE, 40–52. 

- [97] Wei Li, Yongxing He, Xiaoyu Zhang, and Yongchuan Tang. 2023. Filter pruning via feature map clustering. _Intelligent data analysis_ 27, 4 (2023), 911–933. 

- [98] Xinqing Li, Xin He, Le Zhang, Min Wu, Xiaoli Li, and Yun Liu. 2025. A comprehensive survey on world models for embodied ai. _arXiv preprint arXiv:2510.16732_ (2025). 

- [99] Yuanchun Li, Hao Wen, Weijun Wang, Xiangyu Li, Yizhen Yuan, Guohong Liu, Jiacheng Liu, Wenxing Xu, Xiang Wang, Yi Sun, et al. 2024. Personal llm agents: Insights and survey about the capability, efficiency and security. _arXiv preprint arXiv:2401.05459_ (2024). 

- [100] Chengdong Lin, Kun Wang, Zhenjiang Li, and Yu Pu. 2023. A workload-aware DVFS robust to concurrent tasks for mobile devices. In _Proceedings of the 29th Annual International Conference on Mobile Computing and Networking_ . 

31 

Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies 

- 1–16. 

- [101] Ji Lin, Jiaming Tang, Haotian Tang, Shang Yang, Wei-Ming Chen, Wei-Chen Wang, Guangxuan Xiao, Xingyu Dang, Chuang Gan, and Song Han. 2024. Awq: Activation-aware weight quantization for on-device llm compression and acceleration. 87–100 pages. 

- [102] Mingbao Lin, Rongrong Ji, Yan Wang, Yichen Zhang, Baochang Zhang, Yonghong Tian, and Ling Shao. 2020. Hrank: Filter pruning using high-rank feature map. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . 1529–1538. 

- [103] Shaohui Lin, Rongrong Ji, Chenqian Yan, Baochang Zhang, Liujuan Cao, Qixiang Ye, Feiyue Huang, and David Doermann. 2019. Towards optimal structured cnn pruning via generative adversarial learning. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . 2790–2799. 

- [104] Guan-Horng Liu, Avinash Siravuru, Sai Prabhakar, Manuela Veloso, and George Kantor. 2017. Learning end-to-end multimodal sensor policies for autonomous navigation. In _Conference on robot learning_ . PMLR, 249–261. 

- [105] Hsin-I Cindy Liu, Marius Brehler, Mahesh Ravishankar, Nicolas Vasilache, Ben Vanik, and Stella Laurenzo. 2022. TinyIREE: An ML execution environment for embedded systems from compilation to deployment. 9–16 pages. 

- [106] Zechun Liu, Haoyuan Mu, Xiangyu Zhang, Zichao Guo, Xin Yang, Kwang-Ting Cheng, and Jian Sun. 2019. Metapruning: Meta learning for automatic neural network channel pruning. In _Proceedings of the IEEE/CVF international conference on computer vision_ . 3296–3305. 

- [107] Zhijian Liu, Haotian Tang, Alexander Amini, Xinyu Yang, Huizi Mao, Daniela Rus, and Song Han. 2022. Bevfusion: Multi-task multi-sensor fusion with unified bird’s-eye view representation. _arXiv preprint arXiv:2205.13542_ (2022). 

- [108] Zirui Liu, Jiayi Yuan, Hongye Jin, Shaochen Zhong, Zhaozhuo Xu, Vladimir Braverman, Beidi Chen, and Xia Hu. 2024. Kivi: A tuning-free asymmetric 2bit quantization for kv cache. _arXiv preprint arXiv:2402.02750_ (2024). 

- [109] Zechun Liu, Changsheng Zhao, Igor Fedorov, Bilge Soran, Dhruv Choudhary, Raghuraman Krishnamoorthi, Vikas Chandra, Yuandong Tian, and Tijmen Blankevoort. 2024. Spinquant: Llm quantization with learned rotations. _arXiv preprint arXiv:2405.16406_ (2024). 

- [110] Yang Lou, Qun Song, Qian Xu, Rui Tan, and Jianping Wang. 2023. Uncertainty-encoded multi-modal fusion for robust object detection in autonomous driving. 

- [111] Simian Luo, Yiqin Tan, Longbo Huang, Jian Li, and Hang Zhao. 2023. Latent consistency models: Synthesizing high-resolution images with few-step inference. _arXiv preprint arXiv:2310.04378_ (2023). 

- [112] Kai Lv, Honglin Guo, Qipeng Guo, and Xipeng Qiu. 2025. DuoDecoding: Hardware-aware Heterogeneous Speculative Decoding with Dynamic Multi-Sequence Drafting. _arXiv preprint arXiv:2503.00784_ (2025). 

- [113] Xudong Lv, Boya Wang, Ziwen Dou, Dong Ye, and Shuo Wang. 2021. LCCNet: LiDAR and camera self-calibration using cost volume network. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . 2894–2901. 

- [114] Steven Macenski, Tully Foote, Brian Gerkey, Chris Lalancette, and William Woodall. 2022. Robot operating system 2: Design, architecture, and uses in the wild. _Science robotics_ 7, 66 (2022), eabm6074. 

- [115] Yuya Maruyama, Shinpei Kato, and Takuya Azumi. 2016. Exploring the performance of ROS2. In _Proceedings of the 13th international conference on embedded software_ . 1–10. 

- [116] Víctor Mayoral-Vilches, Juan Manuel Reina-Muñoz, Martiño Crespo-Álvarez, and David Mayoral-Vilches. 2024. ROS 2 on a Chip, Achieving Brain-Like Speeds and Efficiency in Robotic Networking. _arXiv preprint arXiv:2404.18208_ (2024). 

- [117] Ali Mirzaeian, Jana Kosecka, Houman Homayoun, Tinoosh Mohsenin, and Avesta Sasan. 2021. Diverse knowledge distillation (dkd): A solution for improving the robustness of ensemble models against adversarial attacks. In _2021 22nd International Symposium on Quality Electronic Design (ISQED)_ . IEEE, 319–324. 

- [118] Hans Moravec. 1988. _Mind children: The future of robot and human intelligence_ . Harvard University Press. [119] Mozhgan Navardi, Romina Aalishah, Yuzhe Fu, Yueqian Lin, Hai Li, Yiran Chen, and Tinoosh Mohsenin. 2025. GenAI at the edge: Comprehensive survey on empowering edge devices. In _Proceedings of the AAAI Symposium Series_ , Vol. 5. 180–187. 

- [120] Chaoyue Niu, Yucheng Ding, Junhui Lu, Zhengxiang Huang, Hang Zeng, Yutong Dai, Xuezhen Tu, Chengfei Lv, Fan Wu, and Guihai Chen. 2025. Collaborative Learning of On-Device Small Model and Cloud-Based Large Model: Advances and Future Directions. _arXiv preprint arXiv:2504.15300_ (2025). 

- [121] Shuaicheng Niu, Chunyan Miao, Guohao Chen, Pengcheng Wu, and Peilin Zhao. 2024. Test-time model adaptation with only forward passes. _arXiv preprint arXiv:2404.01650_ (2024). 

- [122] Shuaicheng Niu, Jiaxiang Wu, Yifan Zhang, Yaofo Chen, Shijian Zheng, Peilin Zhao, and Mingkui Tan. 2022. Efficient test-time model adaptation without forgetting. In _International conference on machine learning_ . PMLR, 16888–16905. 

- [123] Shuaicheng Niu, Jiaxiang Wu, Yifan Zhang, Zhiquan Wen, Yaofo Chen, Peilin Zhao, and Mingkui Tan. 2023. Towards stable test-time adaptation in dynamic wild world. _arXiv preprint arXiv:2302.12400_ (2023). 

Grover et al. 

32 

- [124] Michael O’Connell, Guanya Shi, Xichen Shi, Kamyar Azizzadenesheli, Anima Anandkumar, Yisong Yue, and Soon-Jo Chung. 2022. Neural-fly enables rapid learning for agile flight in strong winds. _Science Robotics_ 7, 66 (2022), eabm6597. 

- [125] Jongyoon Park, Pileun Kim, and Daeil Ko. 2025. Real-time open-vocabulary perception for mobile robots on edge devices: a systematic analysis of the accuracy-latency trade-off. _Frontiers in Robotics and AI_ 12 (2025), 1693988. 

- [126] Junhyeok Park, Osang Kwon, Yongho Lee, Seongwook Kim, Gwangeun Byeon, Jihun Yoon, Prashant J Nair, and Seokin Hong. 2024. A case for speculative address translation with rapid validation for gpus. In _2024 57th IEEE/ACM International Symposium on Microarchitecture (MICRO)_ . IEEE, 278–292. 

- [127] Konyul Park, Yecheol Kim, Daehun Kim, and Jun Won Choi. 2025. Resilient sensor fusion under adverse sensor failures via multi-modal expert fusion. 6720–6729 pages. 

- [128] Taehwan Park, Geonho Lee, and Min-Soo Kim. 2025. MobileRAG: A Fast, Memory-Efficient, and Energy-Efficient Method for On-Device RAG. _arXiv preprint arXiv:2507.01079_ (2025). 

- [129] Michael Pöhnl, Christian Eltzschig, and Tobias Blass. 2023. Shared-memory-based lock-free queues: The key to fast and robust communication on safety-critical edge devices. 179–184 pages. 

- [130] Ashutosh Pradhan, Daniele Ottaviano, Yi Jiang, Haozheng Huang, Jiajia Zhang, Alexander Zuepke, Andrea Bastoni, and Marco Caccamo. 2025. Predictable Memory Bandwidth Regulation for DynamIQ Arm Systems. In _2025 IEEE 31st International Conference on Embedded and Real-Time Computing Systems and Applications (RTCSA)_ . IEEE, 126–137. 

- [131] K Prashanthi S, Kunal Kumar Sahoo, Amartya Ranjan Saikia, Pranav Gupta, Atharva Vinay Joshi, Priyanshu Pansari, and Yogesh Simmhan. 2025. Pagoda: An Energy and Time Roofline Study for DNN Workloads on Edge Accelerators. _arXiv e-prints_ (2025), arXiv–2509. 

- [132] Jon Altonaga Puente, Enrico Mezzetti, Irune Agirre Troncoso, Jaume Abella Ferrer, and Francisco J Cazorla Almeida. 2025. ROSGuard: A Bandwidth Regulation Mechanism for ROS2-based Applications. _arXiv preprint arXiv:2506.04640_ (2025). 

- [133] Muhammad Azlan Qazi, Alexandros Iosifidis, and Qi Zhang. 2025. PRISM: Distributed Inference for Foundation Models at Edge. _arXiv preprint arXiv:2507.12145_ (2025). 

- [134] Alec Radford, Jong Wook Kim, Tao Xu, Greg Brockman, Christine McLeavey, and Ilya Sutskever. 2023. Robust speech recognition via large-scale weak supervision. In _International conference on machine learning_ . PMLR, 28492–28518. 

- [135] Vijay Janapa Reddi, Christine Cheng, David Kanter, Peter Mattson, Guenther Schmuelling, Carole-Jean Wu, Brian Anderson, Maximilien Breughe, Mark Charlebois, William Chou, et al. 2020. Mlperf inference benchmark. In _2020 ACM/IEEE 47th Annual International Symposium on Computer Architecture (ISCA)_ . IEEE, 446–459. 

- [136] Scott Reed, Konrad Zolna, Emilio Parisotto, Sergio Gomez Colmenarejo, Alexander Novikov, Gabriel Barth-Maron, Mai Gimenez, Yury Sulsky, Jackie Kay, Jost Tobias Springenberg, et al. 2022. A generalist agent. _arXiv preprint arXiv:2205.06175_ (2022). 

- [137] Pengzhen Ren, Kaidong Zhang, Hetao Zheng, Zixuan Li, Yuhang Wen, Fengda Zhu, Shikui Ma, and Xiaodan Liang. 2025. Surfer: A world model-based framework for vision-language robot manipulation. _IEEE Transactions on Neural Networks and Learning Systems_ (2025). 

- [138] Markus Rognlien, Zhiqiang Que, Jose GF Coutinho, and Wayne Luk. 2022. Hardware-aware optimizations for deep learning inference on edge devices. In _International Symposium on Applied Reconfigurable Computing_ . Springer, 118–133. 

- [139] Shulan Ruan, Rongwei Wang, Xuchen Shen, Huijie Liu, Baihui Xiao, Jun Shi, Kun Zhang, Zhenya Huang, Yu Liu, Enhong Chen, et al. 2025. A survey of multi-sensor fusion perception for embodied AI: Background, methods, challenges and prospects. _arXiv preprint arXiv:2506.19769_ (2025). 

- [140] Wenjie Ruan, Xiaowei Huang, and Marta Kwiatkowska. 2018. Reachability analysis of deep neural networks with provable guarantees. _arXiv preprint arXiv:1805.02242_ (2018). 

- [141] Shaibal Saha and Lanyu Xu. 2025. Vision transformers on the edge: A comprehensive survey of model compression and acceleration strategies. _Neurocomputing_ (2025), 130417. 

- [142] Go Sakayori and Genya Ishigami. 2024. Modeling of slip rate-dependent traversability for path planning of wheeled mobile robot in sandy terrain. _Frontiers in Robotics and AI_ 11 (2024), 1320261. 

- [143] Sahar Salimpour, Jorge Peña-Queralta, Diego Paez-Granados, Jukka Heikkonen, and Tomi Westerlund. 2025. Sim-toreal transfer for mobile robots with reinforcement learning: from nvidia isaac sim to gazebo and real ros 2 robots. _arXiv preprint arXiv:2501.02902_ (2025). 

- [144] Ranjan Sapkota, Yang Cao, Konstantinos I Roumeliotis, and Manoj Karkee. 2025. Vision-Language-Action (VLA) Models: Concepts, Progress, Applications and Challenges. _arXiv preprint arXiv:2505.04769_ (2025). 

- [145] Sepehr Sharifi, Andrea Stocco, and Lionel C Briand. 2025. System safety monitoring of learned components using temporal metric forecasting. _ACM Transactions on Software Engineering and Methodology_ 34, 6 (2025), 1–43. 

- [146] Noam Shazeer. 2019. Fast transformer decoding: One write-head is all you need. _arXiv preprint arXiv:1911.02150_ (2019). 

Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies 

33 

- [147] Yuwen Shen, Jorrit Vander Mynsbrugge, Nima Roshandel, Robin Bouchez, Hamed FirouziPouyaei, Constantin Scholz, Hoang-Long Cao, Bram Vanderborght, Wouter Joosen, and Antonio Paolillo. 2025. SentryRT-1: A Case Study in Evaluating Real-Time Linux for Safety-Critical Robotic Perception. In _Proceedings of the 19th International Workshop on Operating Systems Platforms for Embedded Real-Time Applications (OSPERT 2025)_ . 35–41. 

- [148] Weisong Shi, Jie Cao, Quan Zhang, Youhuizi Li, and Lanyu Xu. 2016. Edge computing: Vision and challenges. _IEEE internet of things journal_ 3, 5 (2016), 637–646. 

- [149] Yuanming Shi, Kai Yang, Tao Jiang, Jun Zhang, and Khaled B Letaief. 2020. Communication-efficient edge AI: Algorithms and systems. _IEEE communications surveys & tutorials_ 22, 4 (2020), 2167–2191. 

- [150] Alina Shutova, Vladimir Malinovskii, Vage Egiazarian, Denis Kuznedelev, Denis Mazur, Nikita Surkov, Ivan Ermakov, and Dan Alistarh. 2025. Cache me if you must: Adaptive key-value quantization for large language models. 

- [151] Pirmin Sigron, Ivo Aschwanden, and Markus Bambach. 2023. Compensation of geometric, backlash, and thermal drift errors using a universal industrial robot model. _IEEE Transactions on Automation Science and Engineering_ 21, 4 (2023), 6615–6627. 

- [152] K-A Skevik, Thomas Plagemann, Vera Goebel, and Pål Halvorsen. 2001. Evaluation of a zero-copy protocol implementation. In _Proceedings 27th EUROMICRO Conference. 2001: A Net Odyssey_ . IEEE, 324–330. 

- [153] James Seale Smith, Chi-Heng Lin, Shikhar Tuli, Haris Jeelani, Shangqian Gao, Yilin Shen, Hongxia Jin, and Yen-Chang Hsu. 2025. FlexiGPT: Pruning and Extending Large Language Models with Low-Rank Weight Sharing. _arXiv preprint arXiv:2501.14713_ (2025). 

- [154] Hoora Sobhani, Hyunjong Choi, and Hyoseung Kim. 2023. Timing analysis and priority-driven enhancements of ROS 2 multi-threaded executors. In _2023 IEEE 29th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ . IEEE, 106–118. 

- [155] Zhihang Song, Lihui Peng, Jianming Hu, Danya Yao, and Yi Zhang. 2024. Timealign: A multi-modal object detection method for time misalignment fusing in autonomous driving. 

- [156] Connor Sullivan, Alex Manley, Mohammad Alian, and Heechul Yun. 2024. Per-Bank Bandwidth Regulation of Shared Last-Level Cache for Real-Time Systems. In _2024 IEEE Real-Time Systems Symposium (RTSS)_ . IEEE, 336–348. 

- [157] Zhiqing Sun, Hongkun Yu, Xiaodan Song, Renjie Liu, Yiming Yang, and Denny Zhou. 2020. Mobilebert: a compact task-agnostic bert for resource-limited devices. 2158–2170 pages. 

- [158] Niko Sünderhauf, Oliver Brock, Walter Scheirer, Raia Hadsell, Dieter Fox, Jürgen Leitner, Ben Upcroft, Pieter Abbeel, Wolfram Burgard, Michael Milford, et al. 2018. The limits and potentials of deep learning for robotics. _The International journal of robotics research_ 37, 4-5 (2018), 405–420. 

- [159] Tushar Prasanna Swaminathan, Christopher Silver, Thangarajah Akilan, and Jitendra Kumar. 2025. Benchmarking deep learning models on nvidia jetson nano for real-time systems: An empirical investigation. _Procedia Computer Science_ 260 (2025), 906–913. 

- [160] Vivienne Sze, Yu-Hsin Chen, Tien-Ju Yang, and Joel S Emer. 2017. Efficient processing of deep neural networks: A tutorial and survey. _Proc. IEEE_ 105, 12 (2017), 2295–2329. 

- [161] Xiaoqiang Tan, Guangqiang Wu, Zefan Li, Kai Liu, and Chengbao Zhang. 2024. Autonomous emergency collision avoidance and collaborative stability control technologies for intelligent vehicles: a survey. _IEEE Transactions on Intelligent Vehicles_ (2024). 

- [162] Haotian Tang, Zhijian Liu, Shengyu Zhao, Yujun Lin, Ji Lin, Hanrui Wang, and Song Han. 2020. Searching efficient 3d architectures with sparse point-voxel convolution. In _European conference on computer vision_ . Springer, 685–702. 

- [163] Yihong Tang, Haicheng Liao, Tong Nie, Junlin He, Ao Qu, Kehua Chen, Wei Ma, Zhenning Li, Lijun Sun, and Chengzhong Xu. 2025. E3AD: An emotion-aware vision-language-action model for human-centric end-to-end autonomous driving. _arXiv preprint arXiv:2512.04733_ (2025). 

- [164] Manan Tayal, Aditya Singh, Pushpak Jagtap, and Shishir Kolathaya. 2025. Cp-ncbf: A conformal prediction-based approach to synthesize verified neural control barrier functions. _arXiv preprint arXiv:2503.17395_ (2025). 

- [165] Gemini Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. 2023. Gemini: a family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ (2023). 

- [166] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, et al. 2025. Gemini robotics: Bringing ai into the physical world. _arXiv preprint arXiv:2503.20020_ (2025). 

- [167] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. 2024. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ (2024). 

- [168] Ben Tearle, Kim P Wabersich, Andrea Carron, and Melanie N Zeilinger. 2021. A predictive safety filter for learningbased racing control. _IEEE Robotics and Automation Letters_ 6, 4 (2021), 7635–7642. 

Grover et al. 

34 

- [169] Surat Teerapittayanon, Bradley McDanel, and Hsiang-Tsung Kung. 2017. Distributed deep neural networks over the cloud, the edge and end devices. In _2017 IEEE 37th international conference on distributed computing systems (ICDCS)_ . IEEE, 328–339. 

- [170] Harun Teper, Oren Bell, Mario Günzel, Chris Gill, and Jian-Jia Chen. 2024. Bridging the Gap between ROS˜ 2 and Classical Real-Time Scheduling for Periodic Tasks. _arXiv preprint arXiv:2408.03696_ (2024). 

- [171] Max Tölle, Tobias Grüner, David Palenicek, et al. 2023. Runtime Monitoring for Safe Deep Learning Systems: A Survey. _Comput. Surveys_ 56, 3 (2023), 1–38. 

- [172] Maximilian Tölle, Theo Gruner, Daniel Palenicek, Jonas Günster, Puze Liu, Joe Watson, Davide Tateo, and Jan Peters. 2025. Towards Safe Robot Foundation Models. _arXiv preprint arXiv:2503.07404_ (2025). 

- [173] Aditya Tomar, Coleman Hooper, Minjae Lee, Haocheng Xi, Rishabh Tiwari, Wonjun Kang, Luca Manolache, Michael W Mahoney, Kurt Keutzer, and Amir Gholami. 2025. XQuant: Breaking the Memory Wall for LLM Inference with KV Cache Rematerialization. 

- [174] Prathap Kumar Valsan, Heechul Yun, and Farzad Farshchi. 2017. Addressing isolation challenges of non-blocking caches for multicore real-time systems. _Real-Time Systems_ 53, 5 (2017), 673–708. 

- [175] Gijs MC van den Hoven. 2024. _Introducing a performance observation framework to ros2_ . Ph. D. Dissertation. Master’s thesis, Mathematics and Computer Science. 

- [176] Jorge Vargas, Suleiman Alsweiss, Onur Toker, Rahul Razdan, and Joshua Santos. 2021. An overview of autonomous vehicles sensors and their vulnerability to weather conditions. _Sensors_ 21, 16 (2021), 5397. 

- [177] Kim Peter Wabersich and Melanie N Zeilinger. 2021. A predictive safety filter for learning-based control of constrained nonlinear dynamical systems. _Automatica_ 129 (2021), 109597. 

- [178] K Wali. 2024. Hardware-software co-design for power-efficient edge-AI systems. _J Artif Intell Mach Learn Data Sci_ 2, 4 (2024), 2754–60. 

- [179] Qifan Wang and David Oswald. 2024. Confidential Computing on Heterogeneous CPU-GPU Systems: Survey and Future Directions. _arXiv preprint arXiv:2408.11601_ (2024). 

- [180] Shiming Wang, Holger Caesar, Liangliang Nan, and Julian FP Kooij. 2024. Unibev: Multi-modal 3d object detection with uniform bev encoders for robustness against missing sensor modalities. 2776–2783 pages. 

- [181] Zhendong Wang, Zhaoshuo Li, Ajay Mandlekar, Zhenjia Xu, Jiaojiao Fan, Yashraj Narang, Linxi Fan, Yuke Zhu, Yogesh Balaji, Mingyuan Zhou, et al. 2024. One-step diffusion policy: Fast visuomotor policies via diffusion distillation. _arXiv preprint arXiv:2410.21257_ (2024). 

- [182] Jianyu Wei, Qingtao Li, Shijie Cao, Lingxiao Ma, Zixu Hao, Yanyong Zhang, Xiaoyan Hu, and Ting Cao. 2025. T-MAN: Enabling End-to-End Low-Bit LLM Inference on NPUs via Unified Table Lookup. 

- [183] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Zhibin Tang, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, et al. 2025. Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ (2025). 

- [184] Samuel Williams, Andrew Waterman, and David Patterson. 2009. Roofline: an insightful visual performance model for multicore architectures. _Commun. ACM_ 52, 4 (2009), 65–76. 

- [185] Kieran Woodward, Eiman Kanjo, Georgios Papandroulidakis, Shady Agwa, and Themis Prodromakis. 2026. A Hybrid Edge Classifier: Combining TinyML-Optimised CNN With RRAM-CMOS ACAM for Energy-Efficient Inference. _IEEE Transactions on Knowledge and Data Engineering_ 38, 4 (2026), 2122–2135. doi:10.1109/TKDE.2026.3655717 

- [186] Philipp Wu, Alejandro Escontrela, Danijar Hafner, Pieter Abbeel, and Ken Goldberg. 2023. Daydreamer: World models for physical robot learning. In _Conference on robot learning_ . PMLR, 2226–2240. 

- [187] Tingting Wu, Chunhe Song, and Peng Zeng. 2023. Efficient federated learning on resource-constrained edge devices based on model pruning. _Complex & Intelligent Systems_ 9, 6 (2023), 6999–7013. 

- [188] Yiming Wu, Huan Wang, Zhenghao Chen, Jianxin Pang, and Dong Xu. 2025. On-device diffusion transformer policy for efficient robot manipulation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . 14073–14083. 

- [189] Guangxuan Xiao, Ji Lin, Mickael Seznec, Hao Wu, Julien Demouth, and Song Han. 2023. Smoothquant: Accurate and efficient post-training quantization for large language models. 38087–38099 pages. 

- [190] Wei Xiao, Tsun-Hsuan Wang, Chuang Gan, Ramin Hasani, Mathias Lechner, and Daniela Rus. 2023. Safediffuser: Safe planning with diffusion probabilistic models. In _The Thirteenth International Conference on Learning Representations_ . 

- [191] Peng Xu, Xiatian Zhu, and David A Clifton. 2023. Multimodal learning with transformers: A survey. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ 45, 10 (2023), 12113–12132. 

- [192] Fengze Yang, Bo Yu, Yang Zhou, Xuewen Luo, Zhengzhong Tu, and Chenxi Liu. 2025. Edge-based multimodal sensor data fusion with vision language models (vlms) for real-time autonomous vehicle accident avoidance. 

- [193] Karren Yang, Wan-Yi Lin, Manash Barman, Filipe Condessa, and Zico Kolter. 2021. Defending multimodal fusion models against single-source adversaries. 3340–3349 pages. 

Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies 

35 

- [194] Sherry Yang, Ofir Nachum, Yilun Du, Jason Wei, Pieter Abbeel, and Dale Schuurmans. 2023. Foundation models for decision making: Problems, methods, and opportunities. _arXiv preprint arXiv:2303.04129_ (2023). 

- [195] Yuan Yao, Tianyu Yu, Ao Zhang, Chongyi Wang, Junbo Cui, Hongji Zhu, Tianchi Cai, Chi Chen, Haoyu Li, Weilin Zhao, et al. 2025. Efficient GPT-4V level multimodal large language model for deployment on edge devices. _Nature Communications_ 16, 1 (2025), 5509. 

- [196] Zhewei Yao, Reza Yazdani Aminabadi, Minjia Zhang, Xiaoxia Wu, Conglong Li, and Yuxiong He. 2022. Zeroquant: Efficient and affordable post-training quantization for large-scale transformers. 27168–27183 pages. 

- [197] Justin Yu, Letian Fu, Huang Huang, Karim El-Refai, Rares Andrei Ambrus, Richard Cheng, Muhammad Zubair Irshad, and Ken Goldberg. 2025. Real2render2real: Scaling robot data without dynamics simulation or robot hardware. _arXiv preprint arXiv:2505.09601_ (2025). 

- [198] Heechul Yun, Waqar Ali, Santosh Gondi, and Siddhartha Biswas. 2016. BWLOCK: A dynamic memory access control framework for soft real-time applications on multicore platforms. _IEEE Trans. Comput._ 66, 7 (2016), 1247–1252. 

- [199] Heechul Yun, Gang Yao, Rodolfo Pellizzoni, Marco Caccamo, and Lui Sha. 2013. Memguard: Memory bandwidth reservation system for efficient performance isolation in multi-core platforms. In _2013 IEEE 19th Real-Time and Embedded Technology and Applications Symposium (RTAS)_ . IEEE, 55–64. 

- [200] Elad Ben Zaken, Yoav Goldberg, and Shauli Ravfogel. 2022. Bitfit: Simple parameter-efficient fine-tuning for transformer-based masked language-models. (2022), 1–9. 

- [201] Shulin Zeng, Jun Liu, Guohao Dai, Xinhao Yang, Tianyu Fu, Hongyi Wang, Wenheng Ma, Hanbo Sun, Shiyao Li, Zixiao Huang, et al. 2024. Flightllm: Efficient large language model inference with a complete mapping flow on fpgas. In _Proceedings of the 2024 ACM/SIGDA International Symposium on Field Programmable Gate Arrays_ . 223–234. 

- [202] Weishuai Zeng, Shunlin Lu, Kangning Yin, Xiaojie Niu, Minyue Dai, Jingbo Wang, and Jiangmiao Pang. 2025. Behavior foundation model for humanoid robots. _arXiv preprint arXiv:2509.13780_ (2025). 

- [203] Boxing Zhang, Ryan Wen Liu, Jingxian Liu, Kwok Tai Chui, and Brij B Gupta. 2025. Multi-Sensor Data Fusion Meets Edge Computing for Intelligent Surface Vehicles. _IEEE Internet of Things Magazine_ (2025). 

- [204] Junhui Zhang, Bardh Hoxha, Georgios Fainekos, and Dimitra Panagou. 2025. Conformal Prediction in the Loop: Risk-Aware Control Barrier Functions for Stochastic Systems with Data-Driven State Estimators. _IEEE Control Systems Letters_ (2025). 

- [205] Qianxue Zhang and Eiman Kanjo. 2026. A Multicore and Edge TPU-Accelerated Multimodal TinyML System for Livestock Behavior Recognition. _IEEE Internet of Things Journal_ 13, 1 (2026), 666–677. doi:10.1109/JIOT.2025.3624811 

- [206] Shaolei Zhang, Qingkai Fang, Zhe Yang, and Yang Feng. 2025. Llava-mini: Efficient image and video large multimodal models with one vision token. _arXiv preprint arXiv:2501.03895_ (2025). 

- [207] Tianyi Zhang, Jonah Yi, Zhaozhuo Xu, and Anshumali Shrivastava. 2024. Kv cache is 1 bit per channel: Efficient large language model inference with coupled quantization. 3304–3331 pages. 

- [208] Wuyang Zhang, Zhezhi He, Luyang Liu, Zhenhua Jia, Yunxin Liu, Marco Gruteser, Dipankar Raychaudhuri, and Yanyong Zhang. 2021. Elf: accelerate high-resolution mobile deep vision with content-aware parallel offloading. In _Proceedings of the 27th Annual International Conference on Mobile Computing and Networking_ . 201–214. 

- [209] Xiang Zhang, Run He, Kai Tong, Shuquan Man, Jingyu Tong, Haodong Li, and Huiping Zhuang. 2024. Complex Motion Planning for Quadruped Robots Using Large Language Models. In _2024 IEEE International Symposium on Circuits and Systems (ISCAS)_ . IEEE, 1–5. 

- [210] Zixing Zhang, Jürgen Geiger, Jouni Pohjalainen, Amr El-Desoky Mousa, Wenyu Jin, and Björn Schuller. 2018. Deep learning for environmentally robust speech recognition: An overview of recent developments. _ACM Transactions on Intelligent Systems and Technology (TIST)_ 9, 5 (2018), 1–28. 

- [211] Xu Zheng, Yexin Liu, Yunfan Lu, Tongyan Hua, Tianbo Pan, Weiming Zhang, Dacheng Tao, and Lin Wang. 2023. Deep learning for event-based vision: A comprehensive survey and benchmarks. _arXiv preprint arXiv:2302.08890_ (2023). 

- [212] Shenghao Zhou, Saimouli Katragadda, and Guoquan Huang. 2025. Learning IMU Bias with Diffusion Model. _arXiv preprint arXiv:2505.11763_ (2025). 

- [213] Ligeng Zhu, Lanxiang Hu, Ji Lin, Wei-Ming Chen, Wei-Chen Wang, Chuang Gan, and Song Han. 2023. PockEngine: Sparse and Efficient Fine-tuning in a Pocket. _2023 56th IEEE/ACM International Symposium on Microarchitecture (MICRO)_ (2023), 1381–1394. 

- [214] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. 2023. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ . PMLR, 2165–2183. 

- [215] Amirhossein Zolfagharian, Manel Abdellatif, Lionel C Briand, et al. 2024. Smarla: A safety monitoring approach for deep reinforcement learning agents. _IEEE Transactions on Software Engineering_ (2024). 

- [216] Alexander Zuepke, Andrea Bastoni, Weifan Chen, Marco Caccamo, and Renato Mancuso. 2024. Mempol: polling-based microsecond-scale per-core memory bandwidth regulation. _Real-Time Systems_ 60, 3 (2024), 369–412. 

