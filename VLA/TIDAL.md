---
title: "TIDAL: Temporally Interleaved Diffusion and Action Loop for High-Frequency VLA Control"
date: "2026-01-21"
authors: "Yuteng Sun; Haoran Wang; Ruofei Bai; Zhengguo Li; Jun Li; Meng Yee Michael Chuah"
url: https://arxiv.org/abs/2601.14945
pdf: https://arxiv.org/pdf/2601.14945
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.14945)** / [論文ページ](https://arxiv.org/abs/2601.14945)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **TIDAL: Temporally Interleaved Diffusion and Action Loop for Dynamic Manipulation** 

Yuteng Sun<sup>1</sup><sup>_,_2</sup> , Haoran Wang<sup>1</sup><sup>_,_3</sup> , Ruofei Bai<sup>1</sup><sup>_,_3</sup> , Zhengguo Li<sup>1</sup> , Jun Li<sup>1</sup> , Wenyu Liang<sup>1</sup> , Meng Yee (Michael) Chuah<sup>1</sup> , and Wei-Yun Yau<sup>1</sup><sup>_,∗_</sup> 

**_Abstract_ — Large-scale Vision-Language-Action (VLA) models offer semantic generalization but suffer from high inference latency because they adopt a low-frequency batch-and-execute paradigm. This frequency mismatch creates an execution blind spot, causing failures in dynamic environments where targets move during the open-loop execution window. We propose TIDAL (Temporally Interleaved Diffusion and Action Loop), a hierarchical framework that decouples semantic reasoning from high-frequency actuation. TIDAL operates as a backbone-agnostic scheduler for diffusion-based VLAs, using a dual-frequency architecture to redistribute the computational budget. Specifically, a low-frequency macro-intent loop caches semantic embeddings, while a high-frequency micro-control loop interleaves single-step flow integration with execution, conditioning on the latest state fused with motion cues. To handle the resulting latency shift, we introduce a temporally misaligned training strategy where the policy learns stalenessaware compensation, conditioning on stale semantic intent alongside real-time proprioception. TIDAL is architectural, making it orthogonal to system-level optimizations. Experiments show an average 2.5x performance gain over open-loop baselines in dynamic interception tasks. Despite a slight decrease in static success rates, our approach yields a 4x increase in feedback frequency and extends the effective horizon of semantic embeddings beyond the native action chunk size. Under nonpaused physics and on a real robot, TIDAL remains robust to unmodeled dynamics, while standard open-loop baselines fail due to latency-induced error accumulation.** 

## I. INTRODUCTION 

The pursuit of generalist embodied agents has been accelerated by Vision-Language-Action models, exemplified by systems like GR00T [1] and _π_ 0 [2]. These models increasingly adopt hierarchical architectures that integrate a large VisionLanguage Model with continuous diffusion or flow-matching heads. While these models offer strong semantic grounding from large-scale pre-training, their scale creates a severe computational bottleneck. Current VLAs typically operate on a batch-and-execute paradigm: the system pauses to process observations and computes an entire long-horizon action chunk, which is then executed open-loop. This introduces a fundamental frequency mismatch. Dynamic manipulation requires high-frequency control, whereas large-scale VLA inference often incurs substantial latency and struggles to satisfy such control demands in practice [3], [4]. In real-world deployment, this bottleneck is worsened by the mandatory execution time of the generated action chunk [5], [6]. The 

> 1Authors are with the Institute of Advanced Intelligence and Computing (IAIC), Agency for Science, Technology and Research (A*STAR), Singapore. 

> 2Tsinghua University, Beijing, China. 

> 3Nanyang Technological University, Singapore. 

> _∗_ Correspondence: Yau_Wei_Yun@a-star.edu.sg. 

combination of inference latency and open-loop execution creates an execution blind spot, where the robot remains unresponsive to environmental changes, often leading to failures. Simply increasing the replanning frequency is often compute-prohibitive. Higher replanning rates can increase end-to-end delay, making newly generated trajectories stale by the time they are executed under non-paused physics, where the environment continues to evolve during policy inference rather than waiting for computation to finish. On edge hardware with a fixed compute budget, increasing the control update rate is better achieved by scheduling rather than by more frequent backbone queries. 

Existing latency mitigation strategies incur significant trade-offs. System-level optimizations, such as quantization (e.g., BitVLA [7]) or token pruning (e.g., FlashVLA [8]), provide speedups but remain bounded by the sequential attention mechanism. Distilling small-scale policies like TinyVLA [9] trades rich semantic priors for throughput. More recently, asynchronous scheduling [5] and dual-system architectures [10] have attempted to decouple execution from reasoning. However, these methods often require careful stream management or separate policy networks. We argue that high-frequency control should not require losing the semantic intelligence of large foundation models, nor should it require training distinct policies. 

We propose TIDAL (Temporally Interleaved Diffusion and Action Loop), a backbone-agnostic framework that bridges this frequency gap via compute-efficient interleaved scheduling. Our core insight is that semantic intent exhibits high temporal persistence, whereas physical state is highly transient. Consequently, the expensive VLM backbone need not be queried at every step. Instead of discarding the semantic context, we extend its lifespan by fusing it with highfrequency, real-time proprioceptive updates. TIDAL employs a dual-frequency scheduling strategy: a low-frequency macroloop caches semantic embeddings, while a high-frequency micro-loop interleaves single-step flow integration with execution. This redistributes the computational budget, refreshing the action chunk every _∼_ 110 ms ( _≈_ 9 Hz) compared to the standard _∼_ 400 ms baseline cycle, yielding a 4 _×_ increase in feedback frequency. Although this imposes a higher optimization burden that slightly impacts static task convergence, it provides the critical reactivity required for dynamic interaction and extends the lifespan of semantic embeddings beyond the native action chunk size. 

Deploying this decoupled architecture introduces a temporal misalignment between the stale semantic condition 


Fig. 1. Comparison of inference paradigms for dynamic interception under target morphology variation given the instruction “grasp the can.” _(Top) Standard Baseline:_ The system performs blocking inference at the start and generates a fixed 16-step action chunk conditioned on the initial macro observation _I_ macro and proprioception _s_ prop via intent _E_ . Open-loop execution follows a stale trajectory and can miss the moving target. _(Bottom) TIDAL (Ours):_ The macro-loop queries the VLM once to cache intent _E_ , while the micro-loop performs single-step interleaved flow integration using the latest fused state _s_ ˜ _∗ t_ from proprioception _s ∗_ prop and motion cues _mt_ . The policy executes only the immediate chunk ( _N_ = 4) and discards the tail, refreshing control at _∼_ 9,Hz for robust interception. 

and the current physical state. To address this, we introduce a temporally misaligned training strategy where the policy learns to compensate for intent staleness, using current proprioception signals to reconcile stale semantic conditions with the rapidly evolving physical state. Additionally, we resolve the velocity insensitivity of static vision encoders by incorporating a Differential Motion Predictor with contactgated injection. 

Our primary contributions are: 

- 1) A serial, time-interleaved scheduler for VLAs that increases control update rate without increasing backbone calls. 

- 2) A training paradigm that enables robust compensation for stale semantic cues under temporal misalignment. 

- 3) A flow-matching inference/training recipe that enables reliable one-step Euler chunk generation for highfrequency interleaving. 

- 4) TIDAL achieves an average 2.5 _×_ performance gain in dynamic interception tasks. Robust performance under non-paused inference evaluation and real-world deployment on a physical manipulator validates its efficacy. 

## II. RELATED WORK 

## _A. Latency Mitigation and Real-Time Inference_ 

Current methods bridge the inference-actuation gap via model simplification, adaptive computation, or parallel scheduling. 

_1) Model Distillation and Architectural Simplification:_ One strategy improves deployment efficiency through lightweight VLA variants, compressed backbones, or efficient architectures, including compact models [9], [11], [12] and state-space 

architectures such as [13]. These methods typically trade model capacity or compatibility for speed, potentially weakening the semantic reasoning of larger backbones. TIDAL instead retains the full backbone and improves responsiveness through scheduling. 

_2) Static Compression and Adaptive Inference:_ Static compression techniques like quantization [7] and token pruning [8], [14] directly reduce memory footprint and computational cost. Dynamic inference mechanisms further accelerate forward passes via confidence-based early exits [15], layer routing [16], and parallel decoding [17]. Alongside system-level kernel fusion [18], these methods reduce per-step computation but remain bound by the sequential observe-thenact bottleneck. TIDAL is orthogonal to these optimizations; it acts as a temporal scheduler that can leverage such accelerated backbones to further densify replanning cycles. 

_3) Asynchronous Pipeline and Future Awareness:_ Recent works optimize the inference pipeline via asynchronous execution to break sequential dependencies. Real-Time Chunking [5] inpaints future actions during execution, while VLASH [6] uses a future-state-aware paradigm. VLASH trains the policy to compensate for latency by conditioning on predicted future states. Similarly, Spec-VLA [19] accelerates decoding via speculative sampling. These approaches reduce latency exposure by overlapping computation with execution or by forecasting future states. In contrast, under a serial compute constraint and non-paused physics, reactive updates from the latest state become critical. TIDAL shares the insight of training with temporal misalignment but diverges in execution. Pipelined approaches require high VLM throughput to minimize the prediction horizon. In contrast, TIDAL’s lightweight micro-loop reduces effective calculation time to 

minimal levels. This allows TIDAL to condition directly on the current fused state, avoiding the complexity and uncertainty of predicting future system states. 

## _B. Decoupled Architectures and Temporal Redundancy_ 

Physical states change rapidly, yet high-level semantic intent persists over time [20]. While methods like VLA-Cache [21] exploit this by reusing visual features, recent frameworks like DuoCore-FS [22] and Fast-in-Slow [10] take this further by decoupling reasoning from motor control. They implement a parallel architecture: a slow VLM updates a semantic buffer, while a fast policy queries it at high frequency. However, running two models concurrently demands significant memory bandwidth and parallel compute, which are often prohibitive for edge devices. 

To avoid parallel execution requirements, TIDAL achieves similar decoupling but shifts from a _parallel_ to an _interleaved_ strategy. By treating the VLM and action head as serial, temporally multiplexed components, we eliminate the need for parallel hardware. We freeze the heavy semantic embedding and use a single-step flow integration mechanism for the high-frequency micro-loop. This approach ensures real-time reactivity within a strict serial backbone compute budget, which we validate under realistic, non-paused physical constraints. 

## _C. Action Chunking and Execution Strategies_ 

Action chunking [23] distributes the computational cost of VLA backbones [24], [25]. Recent works like RealTime Chunking [5] improve throughput by overlapping inference with execution via inpainting or chunk splicing. However, these asynchronous methods condition actions on stale observations captured at the start of the inference delay. 

TIDAL moves away from this rigid predict-then-execute paradigm. Leveraging Flow Matching [26], we reinterpret chunk generation as repeated conditional vector-field queries rather than a single static open-loop rollout. By injecting the latest proprioceptive state into the action head at each microupdate, our interleaved integration enables high-frequency reactivity without the complexity of asynchronous stream management or full sequence regeneration. 

## III. METHODOLOGY 

## _A. Hierarchical Dual-Frequency Inference Scheduling_ 

TIDAL splits VLA inference into two nested processes: a low-frequency macro-intent loop for semantic reasoning and a high-frequency micro-control loop for closed-loop refinement. This decomposition enables high-rate control updates while keeping the 3B-parameter backbone at a low query rate by caching semantic embeddings and interleaving flow matching integration steps. 

_1) Macro-Intent Loop (Semantic Caching):_ The macroloop extracts high-level intent from visual observations. Let _l_ instr denote the natural language instruction and _Itm_ denote the RGB observation at macro-step _m_ . We use a pre-trained 

VLM backbone ΦVLM to map these inputs to a dense intent embedding _Em_ : 


The embedding _Em_ is stored in a latent intent buffer and remains frozen for the macro-cycle (horizon _H_ = 16). This caching strategy isolates the control loop from the high latency of ΦVLM, exploiting the fact that semantic intent persists over short execution horizons. 

_2) Micro-Control Loop (Interleaved Flow Execution):_ The micro-loop functions as a reactive policy that queries the action head at high frequency. To align with the standard execution horizon ( _H_ = 16) while maximizing feedback density, we structure the inference as a cascade of _K_ = 4 interactions per macro-cycle. Within each macro-cycle, we re-index time locally so that the macro observation is at _t_ = 0. Given a cached intent _E_ , the loop iterates through latency stages _k ∈{_ 0 _, . . . , K −_ 1 _}_ . At each stage, the loop observes the current state _s_ ˜ _k·N_ . To reduce inference latency, we bypass multi-step ODE solvers and generate the full-horizon action trajectory **ˆa** _∈_ R<sup>_H×Da_</sup> via a single-step Euler approximation (∆ _τ_ = 1) from _τ_ = 0 to 1: 


where **x** 0 _∼N_ ( **0** _,_ **I** ) is the source noise trajectory at _τ_ = 0, and _vθ_ predicts the conditional flow-matching velocity field along the optimal-transport path. We treat this as a one-step flow map optimized to be accurate near the source frontier ( _τ ≈_ 0), rather than a generic ODE solver. After chunk generation, we execute only the first _N_ steps ( **ˆa** [0 _,N_ )) on the robot hardware, discarding the rest ( **ˆa** [ _N,H_ )). 

TIDAL distributes the typical integration budget across the execution timeline. Inspired by streaming execution paradigms [27], [28], we use a single Euler step as a latency-efficient update for the interleaved control loop at the chosen chunk size. By querying this field at every chunk boundary using the latest state _s_ ˜ _k·N_ , TIDAL actively corrects action chunk drift without increasing the backbone compute budget. 

## _B. Temporally Misaligned Training_ 

Synchronous training creates a distribution shift in our architecture because semantic conditions _E_ ( _It−_ ∆) lag behind the physical state _s_ ˜ _t_ . Inspired by recent findings in asynchronous control [6], [22], we address this via a temporally misaligned training strategy that explicitly decouples visual and physical input timestamps, enabling convergence despite semantic lag. 

_1) Dynamic Latency Injection:_ We simulate variable inference latencies by creating training samples with randomized time-lags. Instead of fixed windows _H_ , we sample extended trajectory segments of length _L_ : _L_ = _H_ + ( _K −_ 1) _× N_ (3) 

where _H_ = 16 is the action horizon predicted by the policy, _N_ = 4 is the prefix executed before the next micro-update, and _K_ = 4 is the number of micro-updates performed under one cached macro intent. _L_ is the training segment length 


Fig. 2. _Temporally Misaligned Training Strategy._ We decouple visual and physical timestamps to handle macro–micro latency. _Latency Injection:_ A frozen semantic intent from _I_ macro at _t_ =0 is reused across latency stages ( _k_ = 0 _, . . . ,_ 3) and paired with later fused states ( _s_ ˜ _∗_ 0 _,_ ˜ _s ∗_ 4 _,_ ˜ _s ∗_ 8 _,_ ˜ _s ∗_ 12). _Optimization Objectives:_ The DiT predicts the flow vector field _vθ_ over the _H_ =16-step horizon, supervised by ( **x** 1 _−_ **x** 0). A horizon-weighted loss emphasizes the immediate execution prefix ( _N_ =4), while time-biased sampling concentrates _τ_ near the noise source for single-step integration. 

**Algorithm 1** TIDAL Hierarchical Inference Logic 

**Require:** VLM Backbone ΦVLM, Policy Vector Field _vθ_ , Prediction Horizon _H_ = 16, Execution Chunk _N_ = 4, Latency Stages _K_ = 4, Micro-Cam Buffer _B_ (singleframe, initialized by warm-up for _N_ steps) 

- 1: **loop** 

- 2: { **Macro-Intent Loop** } 

- 3: Capture high-res image _I_ macro 

- 4: _E ←_ ΦVLM( _I_ macro _, l_ instr) {Freeze semantic intent} 

- 5: { **Micro-Control Loop** } 

- 6: **for** _k_ = 0 **to** _K −_ 1 **do** 

- 7: Capture proprioception _s_ prop and micro frame _Ik·N_ 8: _IB ←B_ {previous micro frame} 

- 9: _B ← Ik·N_ {update buffer} 

- 10: _mk·N ← ϕ_ motion( _T_ ( _Ik·N_ ) _−T_ ( _IB_ )) 

- 11: _s_ ˜ _k·N ←_ Fuse( _s_ prop _, mk·N_ ) {State Fusion} 12: **x** 0 _∼N_ ( **0** _,_ **I** ) {Sample fresh noise trajectory of length _H_ } 

- 13: **ˆv** _← vθ_ ( **x** 0 _, τ_ = 0 _,_ ˜ _sk·N , E_ ) {Query vector field at source frontier} 

- 14: **ˆa** _←_ **x** 0 + **ˆv** _·_ 1 {Single-step Euler integration (∆ _τ_ = 1)} 

- 15: **Execute ˆa** [0 _,N_ ) {Run _N_ steps, discard _H − N_ } 16: **Wait** for execution 

- 17: **end for** 18: **end loop** 

required so that every sampled latency stage still has an H-step supervision target. We set _L_ = 28. 

During training, we discretize the potential delay into fixed stages, sampling a latency index _k ∼U{_ 0 _, K −_ 1 _}_ for each iteration. The policy input tuple consists of: 

- Frozen Intent (at physical step _t_ = 0): Visual backbone input _I_ 0. 

- Current State (at physical step _t_ = _k · N_ ): Proprioceptive state _s_ ˜ _k·N_ . 

- Action Target (at physical step _t_ = _k · N_ ): Ground truth sequence **a** [ _kN, kN_ + _H_ ) (length _H_ ). 

Restricting latency to a fixed set of discrete multiples of _N_ , rather than sampling from a continuous interval, reduces the variance of the learning objective. This simplifies the optimization landscape, allowing the model to converge to distinct compensation modes for each stage of intent staleness, rather than fitting an infinite spectrum of delays. 

_2) Horizon-Weighted & Time-Biased Flow Matching:_ The action chunk generator is implemented using Conditional Flow Matching (CFM) [29], which regresses a timedependent vector field _vθ_ . We define the optimal transport path _ψτ_ ( **x** 0 _,_ **x** 1) = (1 _− τ_ ) **x** 0 + _τ_ **x** 1 between the Gaussian noise source **x** 0 _∼N_ ( **0** _,_ **I** ) and the target action sequence **x** 1. The objective minimizes the expected flow matching error: 


where _τ ∈_ [0 _,_ 1] is the continuous flow time, _k ∈{_ 0 _,_ 1 _,_ 2 _,_ 3 _}_ represents the sampled latency stage, and _i_ indexes the action horizon steps. _s_ ˜ _k·N_ and _E_ 0 denote the time-misaligned proprioception and frozen semantic intent, respectively. The micro-loop executes only the initial chunk of length _N_ = 4 before the next update. Therefore, we apply a horizon-aware mask _wi_ , setting _wi_ = 2 _._ 0 for _i < N_ and 1 _._ 0 otherwise. This asymmetry forces the vector field to prioritize precision in the imminent execution window ( _i < N_ ) over distal trajectory smoothness. 

Standard Flow Matching samples the flow time step _τ_ uniformly ( _τ ∼U_ [0 _,_ 1]), allocating equal capacity across the probability path. However, our micro-loop relies exclusively on single-step Euler integration starting from pure noise ( _τ_ = 0). The policy is only queried at the source frontier. Training capacity spent minimizing error at intermediate flow times (e.g., _τ_ = 0 _._ 5) is therefore wasted, as these states are never visited during inference. To align the objective with our architecture, we bias the sampling distribution _p_ ( _τ_ ) heavily towards the noise source. We sample an auxiliary variable _u ∼_ Beta( _α, β_ ) and set _τ_ = 1 _−u_ . With _α_ = 5 _._ 0 and _β_ = 1 _._ 0, the probability mass concentrates near _τ ≈_ 0. This ensures the vector field is most accurate exactly where the single-step solver queries it, maximizing the efficiency of the limited inference budget. 

## _C. Dynamic Perception via Motion Injection_ 

We introduce a lightweight Differential Motion Predictor ( _ϕ_ motion) to inject high-frequency kinematic features directly into the policy. 

We extract motion cues using temporal difference tensors. The input ∆ _It_ = _T_ ( _It_ ) _−T_ ( _It−δ_ ) is the normalized pixelwise difference between the current frame and a history frame with lag _δ_ = _N_ (i.e., one micro-loop update interval). A lowlatency CNN processes this input into a low-dimensional embedding _mt ∈_ R<sup>64</sup> . We pretrain _ϕ_ motion using a loss to predict the target’s future position and velocity, forcing _mt_ to encode predictive physical dynamics and momentum. 

To prevent control instability during manipulation where relative motion is zero, we employ a hard contact-gating mechanism. Based on a binary contact state _ct ∈{_ 0 _,_ 1 _}_ derived from gripper sensors and the robot’s proprioceptive joint state _s_ prop, we construct the fused policy state _s_ ˜ _t_ via concatenation: 


This formulation enforces a modal switch: the policy attends to the full motion vector during the approach phase ( _ct_ = 0) and receives a zero-masked vector during manipulation ( _ct_ = 1). 

## IV. EXPERIMENTS 

We evaluate whether TIDAL’s decoupling and scheduling enable robust dynamic manipulation without losing generalist capabilities. 

## _A. Experimental Setup_ 

_1) Environments:_ We evaluate TIDAL on two benchmarks in the RoboCasa suite. 

We use 8 long-horizon tasks from the official RoboCasa-GR1 benchmark [1], [30] with stationary targets to verify that our architecture retains generalist capabilities. 

We construct a Dynamic Interception benchmark in which success requires the robot to intercept and grasp a moving target, place it into a drawer, and close the drawer. The target starts with a random cardinal-direction velocity and 

makes random 90-degree turns at boundaries, yielding nondeterministic trajectories. We stratify the benchmark into Easy and Hard tiers; using the left hand makes right/up motions kinematically favorable. 

_2) Data Collection:_ For the dynamic task, we collect 2,000 successful fine-tuning episodes using a paused-simulation oracle that pauses physics at every step to run full VLA inference, producing ideal closed-loop trajectories—a behavior achievable only when computational latency is ignored. 

_3) Baselines and Computational Protocol:_ We use GR00TN1.5-3B [1] as the shared VLA backbone, fixing the prediction horizon at _H_ = 16 to isolate performance gains derived purely from scheduling efficiency. To quantify architectural latency, we use the latency numbers reported for NVIDIA Jetson AGX Orin in [1]. The Effective Update Frequency is derived from the total cycle time ( _T_ cycle = _T_ inference + _T_ execution) at a 50 Hz physical control rate (20 ms per execution step). 

We compare TIDAL against three primary configurations: 

- **Open-Loop Baseline [1]:** Queries the VLM and a 4- step DiT of GR00T-N1.5-3B once at _t_ = 0, generating a 16-step chunk that is executed completely open-loop ( _∼_ 2.4 Hz). 

- **Compute-Heavy Replan:** A short-execution fullreplanning variant that queries the full VLM and 4-step DiT every 4 physical steps. It generates a 16-step chunk but executes only the first 4 steps. It includes our motion predictor for dynamic tracking. 

- **TIDAL (Ours):** Queries the VLM once every 16 steps to cache intent. Every 4 steps, it queries the flow head for a single Euler integration, updating the trajectory based on the latest observation. 

TABLE I 

INFERENCE LATENCY AND REAL-TIME UPDATE PROFILES 

|**Method**|**Cost**|_T_**inf** (ms)|_T_**exec**|_T_**cycle**|**Update**|
|---|---|---|---|---|---|
|Baseline|1.0_×_|93|320|413|_∼_2.4 Hz|
|Comp-Heavy|_>_4.0_×_|93|80|173|_∼_5.8 Hz|
|**TIDAL (Avg)**|_∼_105_×_|_∼_**30**|80|_∼_**110**|_∼_**9.0 Hz**|
|**TIDAL (Micro)**|.|_∼_**19**||_∼_**99**|_∼_**10.1 Hz**|


Table I shows that the Open-Loop Baseline has _T_ cycle=413 ms, while Compute-Heavy reduces it to 173 ms at an unsustainable _>_ 4 _._ 0 _×_ cost. TIDAL remains approximately iso-compute by amortizing one macro-step and four microsteps, with _T_ inf _≈_ 30 ms on average (down to _∼_ 19 ms for micro-steps), enabling an effective _∼_ 9–10 Hz update rate without parallel hardware. 

## _B. Main Results_ 

Table II reports success rates on RoboCasa static tasks and our Dynamic Interception benchmark. To evaluate the true impact of inference latency, we report dynamic performance under two physics protocols: the idealized _Paused_ simulation where the environment waits for computation and the realistic _Non-Paused_ evaluation where physics advances during policy inference, approximating real-world deployment. 

TABLE II 

SUCCESS RATE COMPARISON ON STATIC AND DYNAMIC TASKS UNDER DIFFERENT PHYSICS PROTOCOLS 

|**Method**|**Compute**|**Static Benchmark**|**Dyn**|**amic (Easy)**|**Dynamic (Hard)**|
|---|---|---|---|---|---|
||**Cost**|Standard|**Paused** _(Ideal)_|**Non-Paused** _(Realistic)_|**Paused** _(Ideal)_|
|Open-Loop Baseline|1.0_×_|**0.6088**|0.31|0.09 (_↓_71.0%)|0.16|
|Compute-Heavy Replan|_>_**4.0**_×_|-|**0.63**|0.17 (_↓_73.0%)|-|
|**TIDAL (Ours)**|_∼_1.05_×_|0.5938<br>(_↓_2.5%)|0.61|**0.30** (_↓_50.8%)|**0.36**|


_*Note:_ **Bold** <u>/underline</u> indicate best/second-best. The _>_ **4.0** _×_ compute cost is highlighted as a severe penalty: while brute-force computation performs well in idealized _Paused_ physics, its inference latency leads to a severe _∼_ 73% drop in the realistic **Non-Paused** environment. **TIDAL** robustly maintains performance with minimal compute overhead. 

_1) Static Generalization:_ On the official RoboCasa static benchmark, the Baseline achieves a 60.88% success rate. TIDAL achieves 59.38%, demonstrating that our hierarchical decoupling incurs only a slight drop. The slight drop is expected, as our temporally misaligned training objective and single-step flow integration create a more complex optimization landscape compared to standard open-loop training. However, this negligible trade-off confirms that TIDAL successfully retains the rich semantic priors of the 3B VLA backbone while freeing up computational budget for high-frequency control. 

_2) Dynamic Interception (Idealized Paused Protocol):_ In the standard paused simulation, the Open-Loop Baseline fails in dynamic tasks because it blindly follows an outdated trajectory. To establish an upper performance bound, we introduce Compute-Heavy Replan, which uses aggressive full replanning—querying the full VLM and a 4-step DiT every 4 steps at a _>_ 4 _._ 0 _×_ compute cost—achieving a 0.63 success rate. TIDAL achieves an almost identical 0.61 at _∼_ 1.05 _×_ compute cost. In a paused world, these results suggest that locally updating the flow field can approach the performance of full semantic replanning. 

_3) Dynamic Interception (Realistic Non-Paused Protocol):_ The limitation of compute-heavy replanning is exposed under the non-paused protocol, where the environment continues to evolve during inference. The Baseline collapses to a 9% success rate. The compute-heavy replan also experiences a severe drop from 0.63 to 0.17; although it updates frequently and perceives motion, its massive computational latency means targets move before new plans execute. Simply increasing replanning frequency without solving inference lag fails in physical reality. In contrast, TIDAL sustains a highly robust 0.30 success rate. By isolating high-frequency updates to the lightweight micro-loop, TIDAL minimizes reaction delay, actively correcting positional drift while the cached semantic plan remains valid. 

_4) Failure Modes:_ While interleaving substantially improves reactivity, the task remains a long-horizon manipulation problem and does not saturate even in a static setting (success _∼_ 0.8) due to semantic and appearance variability. In the paused dynamic setting, remaining failures typically happen after interception during transport and placement into the right-side drawer. The object occasionally slips or is 

released, or ends up with a pose error that prevents a clean insert, consistent with suboptimal contact under dynamic grasps and limited grasp stability. Under the non-paused protocol, additional failures occur when the target moves too quickly or changes direction suddenly. 

## _C. Ablation Study_ 

We isolate the contributions of TIDAL’s two core components: hierarchical inference scheduling and differential motion predictor. Table III shows the results on the Dynamic (Easy) task. 

The TIDAL scheduling framework without motion features yields a success rate of 0.33, marginally better than the Baseline. Although operating at _∼_ 9 Hz, it lacks explicit velocity data. Injecting motion features into the Baseline improves performance to 0.43. While motion embeddings provide crucial initial velocity cues at _t_ = 0, open-loop execution prevents any mid-trajectory corrections. TIDAL achieves 0.61, outperforming both variants. This highlights a critical synergy: the motion predictor provides the signal to track dynamics, while the hierarchical architecture provides the computational opportunity to act on that signal reactively. 

TABLE III 

ABLATION ANALYSIS ON DYNAMIC (EASY) TASKS 

|**Configuration**|**Hierarchical**<br>**Micro-Loop**|**Motion**<br>**Predictor**|**Success**<br>**Rate**|**Key Limitation**|
|---|---|---|---|---|
|Baseline|✗|✗|0.31|High Latency + Static Features|
|w/o Motion|✓|✗|0.33|Motion Blindness|
|Base + Motion|✗|✓|0.43|Execution Blind Spot|
|**TIDAL (Full)**|✓|✓|**0.61**|-|


## _D. Semantic Intent Lifespan and Efficiency_ 

We analyze cached intent validity on a single static task from the official suite by increasing the number of physical steps executed per macro intent refresh. This forces the microloop to act longer under stale semantics, testing the policy’s tolerance to intent staleness. 

Fig. 3 shows a stable profile: extending intent lifespan from the standard 16 steps (0.72) to 44 steps (0.60) causes limited degradation. This suggests that cached embeddings remain useful when paired with real-time proprioceptive updates. 

This finding challenges the native action chunk limit. While the GR00T backbone is trained to predict a fixed 16-step 


Fig. 3. Analysis of Semantic Intent Lifespan. The shaded regions indicate the Stable Semantics Zone (green) where intent remains valid, and the Degradation Zone (red) where performance collapses. The native action chunk limit is 16 steps. 


Fig. 4. _Real-World Dynamic Interception Workspace._ The overhead view illustrates the stochastic nature of the task. Colored overlays represent diverse historical trajectories captured during evaluation, highlighting unmodeled non-linearities, decelerations due to friction, and sharp deflections caused by block obstacles. 

chunk, TIDAL’s hierarchical architecture extends the useful horizon of a single intent query to _∼_ 44 steps. The policy uses the old intent to condition new, locally correct flows. A sharp performance cliff appears at 48 steps, indicating where the robot’s state diverges too far from the initial snapshot. Although variance increases at extreme latencies, the trend confirms that control ability degrades as semantic lag exceeds the physical correlation window. 

## _E. Real-World Deployment_ 

To validate interleaved scheduling under unmodeled realworld stochasticity, we deploy TIDAL on a KUKA iiwa 14 with a Robotiq 2F-140 gripper and an RGB camera. 

_1) Task Setup and Environmental Stochasticity:_ As shown in Fig. 4, objects roll down a ramp into a flat workspace with block obstacles, introducing trajectory uncertainty from friction, spin, and obstacle deflections. To isolate scheduling effects, we also equip the open-loop baseline with the motion predictor. It still executes the full 16-step chunk, whereas TIDAL executes only _N_ = 4 steps before each micro-loop update. 

_2) Reactivity and Error Bounding:_ In real-world experiments, TIDAL achieves an 86% success rate, substantially 

Fig. 5. Temporal Degradation of Action Chunks. Tracking error vs. action index diverges for the open-loop 16-step rollout, while TIDAL executes only the first 4 steps to bound error within gripper tolerance. 

outperforming the motion-augmented open-loop baseline (34%) over 100 trials, yielding roughly a 2.5 _×_ improvement in dynamic environments. 

The motion-augmented baseline is accurate under near-linear rolls but fails once real perturbations (friction/spin/collisions) change the target trajectory. Executing a 16-step chunk open-loop, it accumulates tracking error throughout the rollout (Fig. 5). Once the target deviates from its initial motion at _t_ = 0, the later chunk steps effectively become stale open-loop extrapolation. 

TIDAL instead bounds error by truncating execution to _N_ =4 steps and triggering a micro-loop update (Fig. 5). Although tracking error can increase slightly within each 4-step window, the next update reconditions on fresh proprioception and motion, preventing divergence. This frequent refresh keeps error within the gripper’s tolerance under unmodeled disturbances. 

## V. CONCLUSION 

We presented TIDAL, a framework designed to enable high-frequency control with large VLA models. By interleaving single-step flow generation with action execution, our approach achieves a 4x increase in update frequency on edge hardware while maintaining the same backbone computational budget. This significantly reduces the execution blind spot found in standard batch-and-execute baselines. 

We leverage temporally misaligned training to compensate for stale semantics, while single-step flow integration minimizes latency. This results in a 2.5x performance gain on dynamic interception tasks. Our analysis reveals that updating the policy with real-time proprioception effectively extends the lifespan of cached semantic embeddings beyond their native horizon. Since TIDAL is backbone-agnostic, it remains orthogonal to system-level accelerations. TIDAL sustains robust performance under non-paused inference protocols, where compute-heavy baselines degrade sharply due to latency. Furthermore, real-world deployment on a physical manipulator confirms these findings. By caching temporally persistent semantic intent and interleaving low-latency flow updates with execution, TIDAL turns long-horizon VLA plans 

into a high-rate closed-loop controller, keeping tracking error bounded under non-paused inference and unmodeled realworld dynamics without increasing backbone queries. 

## ACKNOWLEDGMENT 

OpenAI’s ChatGPT was used to assist with implementation debugging and English-language editing. All technical content, analyses, and conclusions were reviewed and verified by the authors. This research is partly supported by the National Research Foundation, Singapore, under its Thematic CRP programme award no NRF-T-CRP-2025-0008 and by A*STAR under the National Robotics Programme grant no H25-MNR3495. 

## REFERENCES 

- [1] J. Bjorck, F. Castañeda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang _et al._ , “Gr00t n1: An open foundation model for generalist humanoid robots,” _arXiv preprint arXiv:2503.14734_ , 2025. 

- [2] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A vision-language-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [3] K. Kawaharazuka, J. Oh, J. Yamada, I. Posner, and Y. Zhu, “Visionlanguage-action models for robotics: A review towards real-world applications,” _IEEE Access_ , vol. 13, pp. 162 467–162 504, 2025. 

- [4] R. Shao, W. Li, L. Zhang, R. Zhang, Z. Liu, R. Chen, and L. Nie, “Large vlm-based vision-language-action models for robotic manipulation: A survey,” _arXiv preprint arXiv:2508.13073_ , 2025. 

- [5] K. Black, M. Y. Galliker, and S. Levine, “Real-time execution of action chunking flow policies,” in _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. [Online]. Available: https://openreview.net/forum?id=UkR2zO5uww 

- [6] J. Tang, Y. Sun, Y. Zhao, S. Yang, Y. Lin, Z. Zhang, J. Hou, Y. Lu, Z. Liu, and S. Han, “Vlash: Real-time vlas via future-state-aware asynchronous inference,” _arXiv preprint arXiv:2512.01031_ , 2025. 

- [7] H. Wang, C. Xiong, R. Wang, and X. Chen, “Bitvla: 1-bit visionlanguage-action models for robotics manipulation,” _arXiv preprint arXiv:2506.07530_ , 2025. 

- [8] X. Tan, Y. Yang, P. Ye, J. Zheng, B. Bai, X. Wang, J. Hao, and T. Chen, “Think twice, act once: Token-aware compression and action reuse for efficient inference in vision-language-action models,” _arXiv preprint arXiv:2505.21200_ , 2025. 

- [9] J. Wen, Y. Zhu, J. Li, M. Zhu, Z. Tang, K. Wu, Z. Xu, N. Liu, R. Cheng, C. Shen, Y. Peng, F. Feng, and J. Tang, “Tinyvla: Toward fast, dataefficient vision-language-action models for robotic manipulation,” _IEEE Robotics and Automation Letters_ , vol. 10, no. 4, pp. 3988–3995, 2025. 

- [10] H. Chen, J. Liu, C. Gu, Z. Liu, R. Zhang, X. Li, X. He, Y. Guo, C.-W. Fu, S. Zhang, and P.-A. Heng, “Fast-in-slow: A dual-system VLA model unifying fast manipulation within slow reasoning,” in _The Thirtyninth Annual Conference on Neural Information Processing Systems_ , 2025. [Online]. Available: https://openreview.net/forum?id=4asFznbzJg 

- [11] M. Shukor, D. Aubakirova, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, C. Pascal, M. Russi, A. Marafioti _et al._ , “Smolvla: A vision-language-action model for affordable and efficient robotics,” _arXiv preprint arXiv:2506.01844_ , 2025. 

- [12] C.-Y. Hung, Q. Sun, P. Hong, A. Zadeh, C. Li, U. Tan, N. Majumder, S. Poria _et al._ , “Nora: A small open-sourced generalist vision language action model for embodied tasks,” _arXiv preprint arXiv:2504.19854_ , 2025. 

- [13] J. Liu, M. Liu, Z. Wang, P. An, X. Li, K. Zhou, S. Yang, R. Zhang, Y. Guo, and S. Zhang, “Robomamba: Efficient vision-language-action model for robotic reasoning and manipulation,” in _Advances in Neural Information Processing Systems_ , A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, Eds., vol. 37. Curran Associates, Inc., 2024, pp. 40 085–40 110. [Online]. Available: https://proceedings.neurips.cc/paper_files/paper/2024/file/ 46a126492ea6fb87410e55a58df2e189-Paper-Conference.pdf 

- [14] Y. Yang, Y. Wang, Z. Wen, L. Zhongwei, C. Zou, Z. Zhang, C. Wen, and L. Zhang, “EfficientVLA: Training-free acceleration and compression for vision-language-action models,” in _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. [Online]. Available: https://openreview.net/forum?id=SELYlDHZk2 

- [15] W. Song, J. Chen, P. Ding, Y. Huang, H. Zhao, D. Wang, and H. Li, “Ceed-vla: Consistency vision-language-action model with early-exit decoding,” _arXiv preprint arXiv:2506.13725_ , 2025. 

- [16] R. Zhang, M. Dong, Y. Zhang, L. Heng, X. Chi, G. Dai, L. Du, Y. Du, and S. Zhang, “Mole-vla: Dynamic layer-skipping vision language action model via mixture-of-layers for efficient robot manipulation,” _arXiv preprint arXiv:2503.20384_ , 2025. 

- [17] W. Song, J. Chen, P. Ding, H. Zhao, W. Zhao, Z. Zhong, Z. Ge, Z. Li, D. Wang, L. Wang, J. Ma, and H. Li, “Pd-vla: Accelerating visionlanguage-action model integrated with action chunking via parallel decoding,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2025, pp. 13 162–13 169. 

- [18] Y. Ma, Y. Zhou, Y. Yang, T. Wang, and H. Fan, “Running vlas at real-time speed,” _arXiv preprint arXiv:2510.26742_ , 2025. 

- [19] S. Wang, R. Yu, Z. Yuan, C. Yu, F. Gao, Y. Wang, and D. F. Wong, “Spec-VLA: Speculative decoding for vision-languageaction models with relaxed acceptance,” in _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng, Eds. Suzhou, China: Association for Computational Linguistics, Nov. 2025, pp. 26 928–26 940. [Online]. Available: https://aclanthology.org/2025.emnlp-main.1367/ 

- [20] W. Guan, Q. Hu, A. Li, and J. Cheng, “Efficient vision-languageaction models for embodied manipulation: A systematic survey,” _arXiv preprint arXiv:2510.17111_ , 2025. 

- [21] S. Xu, Y. Wang, C. Xia, D. Zhu, T. Huang, and C. Xu, “VLAcache: Efficient vision-language-action manipulation via adaptive token caching,” in _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. [Online]. Available: https://openreview.net/forum?id=QZYZ0Xm58q 

- [22] T. Zou, H. Zeng, Y. Nong, Y. Li, K. Liu, H. Yang, X. Ling, X. Li, and L. Ma, “Asynchronous fast-slow vision-language-action policies for whole-body robotic manipulation,” _arXiv preprint arXiv:2512.20188_ , 2025. 

- [23] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware,” in _Proceedings of Robotics: Science and Systems_ , Daegu, Republic of Korea, July 2023. 

- [24] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn, “Openvla: An open-source vision-language-action model,” in _Proceedings of The 8th Conference on Robot Learning_ , ser. Proceedings of Machine Learning Research, P. Agrawal, O. Kroemer, and W. Burgard, Eds., vol. 270. PMLR, 06–09 Nov 2025, pp. 2679–2713. [Online]. Available: https://proceedings.mlr.press/v270/kim25c.html 

- [25] R. Xu, J. Zhang, M. Guo, Y. Wen, H. Yang, M. Lin, J. Huang, Z. Li, K. Zhang, L. Wang, Y. Kuang, M. Cao, F. Zheng, and X. Liang, “A0: An affordance-aware hierarchical model for general robotic manipulation,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , October 2025, pp. 13 491–13 501. 

- [26] X. Liu, C. Gong, and qiang liu, “Flow straight and fast: Learning to generate and transfer data with rectified flow,” in _The Eleventh International Conference on Learning Representations_ , 2023. [Online]. Available: https://openreview.net/forum?id=XVjTT1nw5z 

- [27] S. Jiang, X. Fang, N. Roy, T. Lozano-Pérez, L. P. Kaelbling, and S. Ancha, “Streaming flow policy: Simplifying diffusion/flow policies by treating action trajectories as flow trajectories,” in _ICRA 2025 Workshop: Beyond Pick and Place_ , 2025. 

- [28] S. H. Høeg, Y. Du, and O. Egeland, “Fast policy synthesis with variable noise diffusion models,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , 2025, pp. 4821–4828. 

- [29] Y. Lipman, R. T. Q. Chen, H. Ben-Hamu, M. Nickel, and M. Le, “Flow matching for generative modeling,” in _The Eleventh International Conference on Learning Representations_ , 2023. [Online]. Available: https://openreview.net/forum?id=PqvMRDCJT9t 

- [30] S. Nasiriany, A. Maddukuri, L. Zhang, A. Parikh, A. Lo, A. Joshi, A. Mandlekar, and Y. Zhu, “RoboCasa: Large-Scale Simulation of Household Tasks for Generalist Robots,” in _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, July 2024. 

